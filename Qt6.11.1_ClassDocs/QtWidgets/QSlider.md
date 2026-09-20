# QSlider

> Qt 6.11.1 · Qt Widgets · 来自 `QSlider`

## 1. 先建立直觉

### 这是什么

`QSlider` 是最常见的线性滑块控件。它把 `QAbstractSlider` 的整数范围模型画成水平或垂直轨道，让用户拖动手柄或用键盘/滚轮调节值。

它适合调节“连续感较强但实际可离散成整数”的参数：音量、亮度、缩放、进度预览、阈值。它不显示数值输入框；需要精确输入时常和 `QSpinBox` 联动。

### 适合使用的场景

- 需要快速粗调的参数。
- 用户更关心相对大小而非精确数字。
- 需要可视化范围位置。
- 和 label/spin box 搭配提供既可拖动又可精确输入的体验。

### 不适合的场景

- 必须精确输入数字时，单独 slider 不够。
- 选项数量很少且离散，用 radio button 或 combo box 更清楚。
- 滚动内容不要用 `QSlider`，用 `QScrollBar` 或滚动区域自带滚动条。

## 2. 依赖与对象关系

- 头文件：`#include <QSlider>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QAbstractSlider`
- 直接派生类：类页未列出

`QSlider` 自己新增的 API 主要是刻度显示。范围、步长、tracking、value、orientation、反转控制都来自 `QAbstractSlider`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum TickPosition` | 控制刻度画在滑块哪一侧或不显示。 |
| `tickInterval : int` | 刻度间隔，单位是值，不是像素。 |
| `tickPosition : TickPosition` | 刻度位置。 |
| `QSlider(QWidget *parent)` | 创建默认垂直滑块。 |
| `QSlider(Qt::Orientation, QWidget *parent)` | 创建指定方向滑块。 |
| `setTickInterval(int)` / `tickInterval()` | 设置或读取刻度间隔。 |
| `setTickPosition(TickPosition)` / `tickPosition()` | 设置或读取刻度位置。 |
| `sizeHint()` / `minimumSizeHint()` | 返回推荐尺寸。 |
| `initStyleOption(QStyleOptionSlider *)` | 为自定义绘制准备 style option。 |
| `mousePressEvent()` / `mouseMoveEvent()` / `mouseReleaseEvent()` | 处理拖动手柄。 |
| `paintEvent()` | 绘制轨道、手柄和刻度。 |
| `event()` | 通用事件入口。 |

## 4. API 逐项说明

### `enum QSlider::TickPosition`

控制刻度线位置。水平滑块可在上方、下方或两侧；垂直滑块对应左侧、右侧或两侧；`NoTicks` 不显示刻度。

刻度适合范围有可理解分段的参数。没有明确分段时，刻度只会制造视觉噪声。

### `tickInterval`

刻度间隔，单位是 slider 的值域单位，不是屏幕像素。设置为 10 表示每隔 10 个值画一个刻度。

值为 0 时，Qt 会根据 `singleStep` 和 `pageStep` 选择。范围很大时要手动设置合理间隔，否则刻度可能太密。

### `tickPosition`

指定刻度画在哪里。默认不显示刻度。

如果 slider 旁边已有数值 label 或刻度说明，刻度位置要和文字排版协调；不要让刻度和其他控件挤在一起。

### 构造和析构

无方向构造函数创建默认垂直滑块；带 `Qt::Orientation` 的构造函数更常用，因为它让布局意图直接写在代码里。

水平音量/进度通常用 `Qt::Horizontal`，垂直调音台推子用 `Qt::Vertical`。

### `sizeHint()` / `minimumSizeHint()`

推荐尺寸由方向、style、手柄大小、刻度位置共同决定。

不要用固定尺寸强行压缩手柄，否则可点击区域会变得不舒服。

### `initStyleOption()`

填充 `QStyleOptionSlider`，包含范围、值、方向、刻度、按下状态等。自定义绘制时使用它可以保持和平台 style 一致。

完全手绘 slider 要处理 hover、pressed、disabled、RTL、inverted appearance 等细节，成本不低。

### 鼠标和绘制事件

鼠标事件负责按下、拖动、释放手柄；绘制事件画轨道、手柄和刻度。普通使用不需要重写。

想改变点击轨道是否跳到位置、是否只 page step，通常要研究 style 行为和鼠标事件，别只改 value。

## 5. 深入实践与常见坑

### 搭配数值显示

slider 不显示精确值。参数设置界面常把 `QSlider` 和 `QSpinBox` 连接起来：拖动快速调节，spin box 精确输入。

### 刻度间隔不是像素

`setTickInterval(5)` 是每 5 个值一个刻度。值域 0 到 10000 时，它会非常密。

### 精度需要自己映射

`QSlider` 只存 int。0.0 到 1.0 的浮点参数可以映射成 0 到 1000，显示时再除回来。
