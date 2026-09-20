# Qt QSizeGrip 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSizeGrip>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QSizeGrip`  
> 定位：顶层窗口尺寸调整手柄

## 1. QSizeGrip 解决什么问题

`QSizeGrip` 是窗口角落里的尺寸调整手柄。用户拖动它时，可以改变顶层窗口的大小。它把“窗口可调整大小”这件事变成一个明确的视觉和交互控件。

它适合：

- 自定义窗口底部右侧的调整大小入口；
- 无边框窗口自己补回缩放手柄；
- 在复杂窗口布局里保留明确的 resize affordance。

```text
顶层窗口
  └─ QSizeGrip
       └─ 鼠标拖动 -> 调整窗口大小
```

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 放进窗口布局

```cpp
#include <QApplication>
#include <QSizeGrip>
#include <QVBoxLayout>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    auto *layout = new QVBoxLayout(&window);
    layout->addStretch();

    auto *grip = new QSizeGrip(&window);
    layout->addWidget(grip, 0, Qt::AlignRight | Qt::AlignBottom);

    window.resize(480, 320);
    window.show();
    return app.exec();
}
```

对于普通有窗口边框的顶层窗口，系统本身通常已经提供调整大小的方式，未必需要额外放一个 `QSizeGrip`。它在无边框窗口或自定义外壳中更有价值。

## 3. 核心使用模型

### 3.1 它调整的是顶层窗口，不是自身大小

手柄本身只是交互入口。用户拖动它时，真正被改变的是它所在顶层窗口的尺寸。

### 3.2 父对象和窗口归属很重要

`QSizeGrip` 通常应该是目标顶层窗口的子控件。若它属于普通中间容器，窗口识别、坐标计算或显示位置可能不符合预期。

### 3.3 `setVisible()` 可能受到窗口状态影响

在最大化、全屏或窗口不可调整大小时，手柄可能隐藏或不产生有效操作。不要把 `isVisible()` 简单理解成“拖动一定有效”。

### 3.4 右下角只是常见位置，不是唯一位置

Qt 会根据布局方向和窗口状态处理手柄位置，但业务界面仍应给它留出稳定的几何空间，不要让它被布局或其他控件遮挡。

## 4. 适合用在哪里

- 无边框主窗口；
- 自绘窗口外壳；
- 需要显式显示 resize affordance 的工具窗口；
- 自定义对话框的底部角落。

## 5. 常见误区

### 5.1 以为普通窗口一定需要它

系统窗口边框通常已经能调整大小，额外放手柄可能重复。

### 5.2 把它放进中央内容区域

它通常应该贴近顶层窗口边缘，否则用户很难理解它在调整什么。

### 5.3 忽略窗口最小/最大尺寸

手柄只能在窗口尺寸约束允许的范围内工作，`minimumSize` 和 `maximumSize` 会直接影响拖动结果。

### 5.4 自己重写鼠标事件却不调用基类

这会很容易破坏 Qt 内部的窗口缩放逻辑。除非确实需要自定义行为，否则不要重写这些事件。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSizeGrip(QWidget *parent)` | 创建一个窗口尺寸调整手柄。 | `parent` 通常是目标顶层窗口。 |
| 析构 | `~QSizeGrip()` | 销毁尺寸调整手柄。 | 通常由父窗口管理。 |
| 尺寸 | `sizeHint() const` | 返回手柄的推荐尺寸。 | 布局时应尊重这个尺寸建议。 |
| 可见性 | `setVisible(bool visible)` | 显示或隐藏尺寸调整手柄。 | 窗口最大化、全屏或不可调整时可能仍受状态影响。 |
| 绘制 | `paintEvent(QPaintEvent *)` | 绘制手柄外观。 | 通常由 Qt 根据当前样式完成。 |
| 鼠标 | `mousePressEvent(QMouseEvent *)` | 开始一次窗口调整操作。 | 通常不需要业务层重写。 |
| 鼠标 | `mouseMoveEvent(QMouseEvent *)` | 根据鼠标移动调整顶层窗口尺寸。 | 依赖窗口尺寸约束和窗口系统支持。 |
| 鼠标 | `mouseReleaseEvent(QMouseEvent *)` | 结束一次窗口调整操作。 | 与按下、移动事件配套。 |
| 窗口状态 | `moveEvent(QMoveEvent *)` | 在窗口或手柄移动时更新内部状态。 | 由框架协调位置。 |
| 窗口状态 | `showEvent(QShowEvent *)` | 处理手柄显示。 | 可能根据窗口状态调整位置。 |
| 窗口状态 | `hideEvent(QHideEvent *)` | 处理手柄隐藏。 | 最大化/全屏时可能触发相关逻辑。 |
| 事件过滤 | `eventFilter(QObject *, QEvent *)` | 监听目标窗口和相关对象的事件。 | 用于同步窗口状态和手柄行为。 |
| 事件 | `event(QEvent *)` | 处理手柄的通用事件。 | 是控件内部状态协调入口。 |

## 7. 一句话总结

`QSizeGrip` 是顶层窗口的尺寸调整手柄，最适合无边框或自定义窗口外壳；它的效果取决于父窗口归属、窗口状态和尺寸约束。
