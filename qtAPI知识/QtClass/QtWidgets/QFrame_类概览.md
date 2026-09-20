# Qt QFrame 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QFrame>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QFrame`  
> 定位：为内容提供边框、分隔线和基础面板外观的 QWidget

## 1. QFrame 解决什么问题

`QFrame` 是 Qt Widgets 中最基础的“视觉边界”控件。它不管理复杂交互，也不是布局；它解决的是让一块区域看起来像面板、凹槽、凸起边界，或让两个内容区有一条分隔线。

```text
QFrame::StyledPanel | Sunken
+---------------------------+
|  一块有边框的内容区域       |
+---------------------------+

QFrame::HLine
-----------------------------
```

常见用途：

- 在设置页中包住一组相关控件；
- 用 `HLine` / `VLine` 做原生风格分隔线；
- 为自定义 widget、滚动区域或堆叠区提供可选边框；
- 作为 `QLabel`、`QAbstractScrollArea`、`QStackedWidget` 等派生控件的外观基础。

不要把 `QFrame` 当作“卡片布局”。它只负责 frame 的绘制；里面的子控件仍需一个 `QLayout`，内容边距用 `setContentsMargins()`，区域间距用布局的 spacing。

## 2. 最小可用示例：面板与分隔线

```cpp
#include <QFrame>
#include <QLabel>
#include <QVBoxLayout>
#include <QWidget>

auto *panel = new QFrame;
panel->setFrameStyle(QFrame::StyledPanel | QFrame::Sunken);
panel->setLineWidth(1);
panel->setContentsMargins(12, 12, 12, 12);

auto *panelLayout = new QVBoxLayout(panel);
panelLayout->addWidget(new QLabel("连接状态：已连接"));

auto *separator = new QFrame;
separator->setFrameShape(QFrame::HLine);
separator->setFrameShadow(QFrame::Sunken);
```

`StyledPanel` 交给当前 `QStyle` 决定细节，因此比旧式 `WinPanel` 更能适应平台主题。分隔线通常不用手写 `paintEvent()`，一条 `HLine` 或 `VLine` 就够。

## 3. frameStyle 由 Shape 和 Shadow 组成

`frameStyle` 是整数位组合：

```cpp
frame->setFrameStyle(QFrame::Box | QFrame::Raised);

QFrame::Shape shape = frame->frameShape();
QFrame::Shadow shadow = frame->frameShadow();
```

`setFrameStyle()` 等价于一次设置“画什么形状”和“以什么立体效果画”。使用 `frameShape()`、`frameShadow()` 读取时不需要自己做位运算。

| Shape | 画出来是什么 | 常见用途 |
| --- | --- | --- |
| `NoFrame` | 不画 frame。 | 暂时关闭边框。 |
| `Box` | 围住内容的矩形框。 | 简单的传统边框。 |
| `Panel` | 可呈凸起/凹陷感的矩形面板。 | 兼容传统 Widgets 风格的区域。 |
| `StyledPanel` | 由当前 style 决定外观的矩形面板。 | 首选的跨平台面板样式。 |
| `HLine` | 不包内容的水平线。 | 区块之间的分隔线。 |
| `VLine` | 不包内容的竖直线。 | 左右面板之间的分隔线。 |
| `WinPanel` | 旧 Windows 2000 风格面板。 | 兼容用途；新代码优先 `StyledPanel`。 |

| Shadow | 效果 | 说明 |
| --- | --- | --- |
| `Plain` | 平面线条。 | 使用 palette 的 `WindowText` 色，不制造立体感。 |
| `Raised` | 凸起。 | 通过当前色组的亮/暗颜色形成 3D 效果。 |
| `Sunken` | 凹陷。 | 通过亮/暗颜色形成内嵌效果。 |

`NoFrame` 与 `Plain` 的数值组合容易让 `frameStyle()` 返回看起来像 `Plain` 的值；真正是否绘制边框应看 `frameShape()`，不要只比较一个 magic int。

## 4. lineWidth、midLineWidth 和 frameWidth 的关系

三者名字相近，但作用不同：

```text
外线宽度      = lineWidth
中线宽度      = midLineWidth
布局应预留的边框总宽 = frameWidth
```

- `lineWidth`：frame 边线的宽度，默认是 `1`。
- `midLineWidth`：中间附加线宽，默认是 `0`；仅在 `Box`、`HLine`、`VLine` 且 shadow 为 `Raised` 或 `Sunken` 时才会画出。
- `frameWidth`：实际绘制 frame 所占宽度，只读；它取决于 style、shape、lineWidth 与 midLineWidth，不是简单相加。

```cpp
frame->setFrameStyle(QFrame::Box | QFrame::Raised);
frame->setLineWidth(2);
frame->setMidLineWidth(1);

int effective = frame->frameWidth();
```

特别是分隔线，视觉总厚度由 `frameWidth()` 决定。想让布局为分隔线留足高度或宽度时，用 `frameWidth()` 判断比假设 `lineWidth()` 更可靠。

## 5. frameRect、contentsRect 与内容边距

`frameRect` 是 frame 实际画在哪个矩形中，默认等于整个 widget rect：

```cpp
QRect drawnBorder = frame->frameRect();
frame->setFrameRect(QRect(2, 2, 200, 80));
```

注意：

- 设置 `frameRect` 不会触发 widget update；需要立即重绘时调用 `update()`。
- widget resize 时，frameRect 会自动调整。
- 传入空矩形（例如 `QRect(0, 0, 0, 0)`）时，frameRect 等价于 widget rect。
- `frameRect` 调整的是边框绘制范围，不是给子控件做布局的推荐手段。

需要让内容避开边框时，设置 contents margins：

```cpp
frame->setContentsMargins(8, 8, 8, 8);
```

`contentsMargins`、frame 宽度和布局内 spacing 是三层不同空白。很多“边框贴着文字”的问题，是只改了 lineWidth 而没有设置 contents margins。

## 6. 枚举掩码：通常不用，但要会读

`StyleMask` 给旧代码或通用 frame 工具做位拆分：

```cpp
int style = frame->frameStyle();
int shapeBits = style & QFrame::Shape_Mask;
int shadowBits = style & QFrame::Shadow_Mask;
```

正常业务代码优先：

```cpp
frame->frameShape();
frame->frameShadow();
```

这两个 getter 更可读，也避免自己与枚举值耦合。

## 7. 什么时候不该用 QFrame

- 想要可折叠分组标题：使用 `QGroupBox` 或自定义 widget。
- 想要复杂阴影、圆角和响应式卡片外观：优先 style sheet、`QStyle` 或专用自定义控件；传统 QFrame 的 raised/sunken 是经典 Widgets 风格，不是现代卡片系统。
- 只需布局留白：使用 `QLayout::setContentsMargins()` 或 `QSpacerItem`，不要用无意义的空 QFrame 占位。
- 想捕获点击：QFrame 没有按钮语义；用 `QPushButton`、可点击 label 或自定义控件处理交互与无障碍。

## API 速查表
### 8.1 类型、样式与属性

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `Shadow` | 描述 frame 的立体阴影效果。 | 与 shape、lineWidth、midLineWidth 共同决定最终外观。 |
| 枚举值 | `Plain` | 绘制平面边线。 | 不制造 raised/sunken 效果。 |
| 枚举值 | `Raised` | 绘制凸起边缘。 | 传统按钮/面板风格。 |
| 枚举值 | `Sunken` | 绘制凹陷边缘。 | 传统输入区/凹槽风格。 |
| 枚举 | `Shape` | 描述 frame 的几何形状。 | 一般用 `setFrameShape()` 或与 shadow 组合调用 `setFrameStyle()`。 |
| 枚举值 | `NoFrame` | 不绘制边框。 | 关闭 frame；不是隐藏整个 widget。 |
| 枚举值 | `Box` | 绘制矩形框。 | 简单边界。 |
| 枚举值 | `Panel` | 绘制可凸起或凹陷的矩形面板。 | 传统控件区域。 |
| 枚举值 | `StyledPanel` | 由当前 style 绘制面板。 | 新代码的首选面板形状。 |
| 枚举值 | `HLine` | 绘制水平分隔线。 | 列表、表单区块分隔。 |
| 枚举值 | `VLine` | 绘制竖直分隔线。 | 并列内容区分隔。 |
| 枚举值 | `WinPanel` | 旧 Windows 风格面板，设置时 lineWidth 为 2。 | 兼容用途，不建议新代码依赖。 |
| 枚举 | `StyleMask` | 从整数 frame style 中提取 shape / shadow 位。 | 普通代码优先 getter。 |
| 枚举值 | `Shape_Mask` | 取出 shape 部分。 | 工具代码处理 `frameStyle()` 位值。 |
| 枚举值 | `Shadow_Mask` | 取出 shadow 部分。 | 工具代码处理 `frameStyle()` 位值。 |
| 属性 | `frameRect` | frame 绘制使用的矩形。 | 默认 widget rect；设置后不自动 update。 |
| 属性 | `frameShape` | 当前 shape 部分。 | 用 `setFrameShape()` 单独修改。 |
| 属性 | `frameShadow` | 当前 shadow 部分。 | 用 `setFrameShadow()` 单独修改。 |
| 只读属性 | `frameWidth` | 实际 frame 总厚度。 | 受 style、宽度和形状共同影响。 |
| 属性 | `lineWidth` | 边线宽度，默认 1。 | 分隔线总厚度仍看 `frameWidth()`。 |
| 属性 | `midLineWidth` | 中线宽度，默认 0。 | 仅部分 raised/sunken frame 会绘制。 |

### 8.2 创建、查询与配置

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QFrame(QWidget *parent = nullptr, Qt::WindowFlags flags = {})` | 创建默认 `NoFrame` 的 frame | 默认 `lineWidth` 为 1；通常把它加入 layout 或作为派生控件基类 |
| 生命周期 | `~QFrame()` | 销毁 frame | 子控件按 QObject 父子关系处理 |
| 几何 | `frameRect() const` | 返回 frame 绘制矩形 | 通常与 widget rect 相同 |
| 几何 | `setFrameRect(const QRect &rect)` | 设置 frame 绘制矩形 | 不会自动触发 `update()`；不应用来手工布局子控件 |
| 形状 | `frameShape() const` | 返回当前 frame 形状 | 判断是否实际绘制边框应看它，而不是只比较 `frameStyle()` 整数 |
| 形状 | `setFrameShape(Shape shape)` | 设置 frame 形状 | 可与 `setFrameShadow()` 分开调用 |
| 阴影 | `frameShadow() const` | 返回当前 frame 阴影效果 | `NoFrame` 下视觉上无意义 |
| 阴影 | `setFrameShadow(Shadow shadow)` | 设置 frame 阴影效果 | 与 shape 共同决定最终外观 |
| 组合样式 | `frameStyle() const` | 返回 shape 与 shadow 组合后的整数样式 | 优先用 `frameShape()` / `frameShadow()`，避免手动比较 magic int |
| 组合样式 | `setFrameStyle(int style)` | 一次设置 shape 和 shadow 的位组合 | 例如 `QFrame::StyledPanel | QFrame::Sunken` |
| 线宽 | `lineWidth() const` | 返回边线宽度 | 默认 1；分隔线实际总厚度仍要看 `frameWidth()` |
| 线宽 | `setLineWidth(int width)` | 设置边线宽度 | 会影响某些 style 下的 `frameWidth()` |
| 中线 | `midLineWidth() const` | 返回中线宽度 | 默认 0；不是所有 shape/shadow 都会绘制中线 |
| 中线 | `setMidLineWidth(int width)` | 设置附加中线宽度 | 只对 `Box`、`HLine`、`VLine` 的 raised/sunken 组合有效 |
| 实际宽度 | `frameWidth() const` | 返回最终实际 frame 宽度 | 只读；受 style、shape、lineWidth、midLineWidth 共同影响 |
| 尺寸 | `sizeHint() const` | 返回 frame 推荐尺寸 | 已考虑 frame 对整体尺寸的影响 |

### 8.3 子类扩展点

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 受保护构造 | `QFrame(QFramePrivate &dd, QWidget *parent = nullptr, Qt::WindowFlags f = {})` | 供 Qt 内部或深度派生类使用的 d-pointer 构造入口 | 普通应用代码不会用；自定义控件通常使用公开构造函数 |
| 样式 | `initStyleOption(QStyleOptionFrame *option) const` | 用当前 `QFrame` 状态初始化 style option | 自定义派生控件借 Qt style 绘制时使用 |
| 绘制 | `drawFrame(QPainter *painter)` | 使用当前样式绘制 frame 本身 | 派生类自绘内容但仍想保留标准边框时可调用 |
| 状态变化 | `changeEvent(QEvent *event)` | 处理样式、字体、调色板等状态变化 | 子类重写时一般保留基类调用 |
| 事件 | `event(QEvent *event)` | 通用事件分发 | 仅在需要处理多类底层事件时重写 |
| 绘制 | `paintEvent(QPaintEvent *event)` | 绘制 frame | 自定义绘制时要决定是否调用基类保持边框 |
