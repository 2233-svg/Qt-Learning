# Qt QStylePainter 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStylePainter>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QPainter -> QStylePainter`  
> 定位：带 style 上下文的绘制器

## 1. 先建立整体认识：它解决什么问题

在自定义控件的 `paintEvent()` 里，普通 `QPainter` 只负责“把线、文字、图片画到设备上”。如果要画一个符合当前 Qt 风格的按钮、复选框、焦点框或复杂控件，还要同时拿到：

- 当前 widget 使用的 `QStyle`；
- 这个 widget 作为绘制上下文；
- `QStyleOption` 描述的状态、矩形和交互状态。

`QStylePainter` 把这三者绑在一起。它本质上还是 `QPainter`，但会记住目标 widget 和 widget 当前的 style，因此可以直接调用 `drawPrimitive()`、`drawControl()`、`drawComplexControl()` 等 style 绘制接口。

## 2. 最常见的使用方式

通常在控件的 `paintEvent()` 中构造：

```cpp
void MyButton::paintEvent(QPaintEvent *)
{
    QStylePainter painter(this);

    QStyleOptionButton option;
    option.initFrom(this);
    option.rect = rect();
    option.text = text();
    option.state |= isDown() ? QStyle::State_Sunken : QStyle::State_Raised;

    painter.drawControl(QStyle::CE_PushButton, option);
}
```

这里真正决定外观的是 `QStyleOptionButton` 和 `QStyle::CE_PushButton`；`QStylePainter` 只是让调用更短，并保证 style 收到正确的 widget 上下文。

## 3. 三类绘制入口怎么分

### 3.1 `drawPrimitive()`

画最小的基础元素，例如面板边框、焦点框、箭头、分隔线。它适合“控件的一小块”。

### 3.2 `drawControl()`

画一个标准控件元素，例如 push button、菜单项、复选框指示器。它通常对应 `QStyle::ControlElement`。

### 3.3 `drawComplexControl()`

画由多个子控件组成的复杂控件，例如组合框、滚动条、滑块。需要使用继承自 `QStyleOptionComplex` 的 option，并在 option 中准备好子控件状态。

如果只想画文字或图标，则用 `drawItemText()` 和 `drawItemPixmap()`，它们会把对齐、调色板和启用状态交给当前 style 处理。

## 4. 构造和生命周期

`QStylePainter` 不拥有 widget，也不拥有 style。它只是保存指针，在 painter 生命周期内使用。  
构造函数会调用 `begin()`，开始对目标 paint device 的绘制；对象离开作用域时，继承自 `QPainter` 的析构流程会结束绘制。

默认构造函数不会自动绑定 widget。只有绑定了 widget 后，`style()`、`drawControl()` 等 style 辅助操作才有有效上下文。

## 5. 常见误区

- 不要在 `paintEvent()` 外长期保存 `QStylePainter`，绘制器应当是短生命周期对象；
- `QStyleOption` 的 `rect`、`state`、`palette` 等字段必须先正确填写，painter 不会替你推断控件状态；
- 不能把 `QStylePainter` 拷贝给另一个 painter，它被明确禁止拷贝；
- 如果目标不是 widget，而是普通 `QPaintDevice`，仍需要通过带 widget 的 `begin(pd, widget)` 提供 style 上下文。

## 6. API 逐项说明

### `QStylePainter()`

创建一个尚未开始绘制、也没有绑定 widget 的 painter。适合需要稍后调用 `begin()` 的代码。

### `QStylePainter(QWidget *widget)`

以 widget 自身作为 paint device 和 style 上下文开始绘制。最适合 `paintEvent()`。

### `QStylePainter(QPaintDevice *pd, QWidget *widget)`

在 `pd` 上绘制，但使用 `widget` 的 style 和上下文。适合把某个 widget 的标准外观画到图片或其他 paint device 上。

### `begin(QWidget *widget)`

开始在 widget 上绘制，相当于 `begin(widget, widget)`。

### `begin(QPaintDevice *pd, QWidget *widget)`

开始在 `pd` 上绘制，并记住 `widget` 的 style。`widget` 不能为 `nullptr`；返回值来自 `QPainter::begin()`，表示 paint device 是否成功打开。

### `drawPrimitive(QStyle::PrimitiveElement pe, const QStyleOption &option)`

调用当前 style 绘制基础元素。`pe` 决定画什么，`option` 提供矩形、状态、调色板等信息。

### `drawControl(QStyle::ControlElement ce, const QStyleOption &option)`

调用当前 style 绘制标准控件元素。需要传入与 `ce` 匹配的 option 派生类型，例如按钮使用 `QStyleOptionButton`。

### `drawComplexControl(QStyle::ComplexControl cc, const QStyleOptionComplex &option)`

调用当前 style 绘制复杂控件。option 通常还要设置 `subControls`、`activeSubControls` 等字段。

### `drawItemText(...)`

按照当前 style 的文字绘制规则，在给定矩形中绘制文字。`flags` 使用 `Qt::Alignment` 等文本布局标志；`enabled` 会影响禁用态颜色。

### `drawItemPixmap(...)`

按照当前 style 的对齐规则绘制 pixmap。它会根据目标矩形和 `flags` 计算 pixmap 的放置位置。

### `style() const`

返回构造或 `begin()` 时绑定的 widget 当前 style。返回的 style 不归 `QStylePainter` 所有。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造函数 | `QStylePainter::QStylePainter()` | 创建尚未绑定 widget 和 paint device 的 painter。 | 之后必须调用 `begin()` 才能进行绘制。 |
| 构造函数 | `explicit QStylePainter::QStylePainter(QWidget *widget)` | 直接在 widget 上开始绘制，并绑定 widget 的 style。 | 常用于 `paintEvent()`；widget 不能为 `nullptr`。 |
| 构造函数 | `QStylePainter::QStylePainter(QPaintDevice *pd, QWidget *widget)` | 在 `pd` 上绘制，同时使用 widget 的 style 上下文。 | `pd` 和 `widget` 可以不是同一个对象，但 widget 必须有效。 |
| 绘制生命周期 | `bool QStylePainter::begin(QWidget *widget)` | 开始对 widget 的绘制。 | 等价于把同一个 widget 同时作为 device 和上下文。 |
| 绘制生命周期 | `bool QStylePainter::begin(QPaintDevice *pd, QWidget *widget)` | 开始对指定 device 绘制，并绑定 widget 的 style。 | 返回值表示 `QPainter` 是否成功开始。 |
| 基础元素 | `void QStylePainter::drawPrimitive(QStyle::PrimitiveElement pe, const QStyleOption &option)` | 绘制焦点框、箭头、边框等基础 style 元素。 | option 的类型和状态必须与 primitive 匹配。 |
| 标准控件 | `void QStylePainter::drawControl(QStyle::ControlElement ce, const QStyleOption &option)` | 绘制按钮、菜单项等标准控件元素。 | 需要使用正确的 `QStyleOption` 派生类。 |
| 复杂控件 | `void QStylePainter::drawComplexControl(QStyle::ComplexControl cc, const QStyleOptionComplex &option)` | 绘制组合框、滚动条、滑块等复杂控件。 | 关注 `subControls` 和 `activeSubControls`。 |
| 文字 | `void QStylePainter::drawItemText(const QRect &rect, int flags, const QPalette &pal, bool enabled, const QString &text, QPalette::ColorRole textRole = QPalette::NoRole)` | 按 style 规则绘制一段带对齐和状态的文字。 | `enabled` 和 `textRole` 会影响最终颜色。 |
| 图片 | `void QStylePainter::drawItemPixmap(const QRect &rect, int flags, const QPixmap &pixmap)` | 按 style 规则对齐并绘制 pixmap。 | 这是对齐绘制，不是缩放策略配置接口。 |
| 查询 | `QStyle *QStylePainter::style() const` | 返回当前绑定的 widget style。 | 指针不由 painter 管理，painter 也不负责销毁它。 |

## 8. 一句话总结

`QStylePainter` 是 `QPainter` 和 `QStyle` 之间的便捷桥梁，让自定义控件可以直接按当前平台风格绘制标准 UI 元素。
