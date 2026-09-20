# QGraphicsProxyWidget

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsProxyWidget`

## 1. 先建立直觉

`QGraphicsProxyWidget` 是普通 `QWidget` 和 Graphics View 场景之间的桥。它把按钮、编辑框、组合框等 QWidget 嵌入 `QGraphicsScene`，让它们像 item 一样移动、缩放、叠放。

这个能力很方便，也很重。它适合少量嵌入真实控件，例如节点里的一个输入框；不适合把大量复杂 widget 或完整窗口体系全塞进场景。

## 2. 类说明

`QGraphicsProxyWidget` 继承自 `QGraphicsWidget`。它内部持有一个 `QWidget`，负责在 graphics item 世界和 widget 世界之间转发几何、绘制、焦点、鼠标键盘、拖放、输入法和弹出子控件事件。

普通 widget 被代理后，生命周期和几何会由 proxy 协调。widget 的一些平台原生特性、窗口行为和复杂弹窗在场景中可能表现不同，所以要重点测试。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsProxyWidget(QGraphicsItem *, Qt::WindowFlags)` | 创建代理图形 widget。 |
| `setWidget(QWidget *)` | 把普通 QWidget 放入 proxy。 |
| `widget()` | 返回当前被代理的 QWidget。 |
| `createProxyForChildWidget(QWidget *)` | 为已代理 widget 的子 widget 创建代理，常用于弹出类子控件。 |
| `subWidgetRect(const QWidget *)` | 查询某个子 widget 在 proxy 坐标中的矩形。 |
| `setGeometry(const QRectF &)` | 设置 proxy 几何，并同步到内部 widget。 |
| `paint()` | 把内部 widget 绘制到场景中。 |
| `type()` | 返回 item 类型。 |
| `event()` / `eventFilter()` | 转发和协调 widget/graphics 事件。 |
| `focusInEvent()` / `focusOutEvent()` | 处理焦点进入离开。 |
| `inputMethodEvent()` / `inputMethodQuery()` | 支持输入法。 |

## 4. 关键用法

```cpp
auto *edit = new QLineEdit;
edit->setPlaceholderText("Name");

auto *proxy = scene->addWidget(edit);
proxy->setPos(100, 60);
```

或者手动创建：

```cpp
auto *proxy = new QGraphicsProxyWidget;
proxy->setWidget(new QPushButton("Run"));
scene->addItem(proxy);
```

当场景缩放时，proxy 也会跟着变换，这正是它和普通 widget overlay 的区别。

## 5. 使用场景

适合节点编辑器里的少量输入框、图形场景中的浮动按钮、可缩放面板里的简单控件、标注工具里的临时编辑框、需要和 item 坐标绑定的控件。

如果控件数量很多，或需要复杂表格、树、富文本编辑器，优先考虑普通 QWidget 侧边栏、浮动面板，或直接用 Graphics Item 自绘交互。

## 6. 常见坑与经验

代理普通 widget 有性能和行为成本。上百个 `QLineEdit` 代理项通常不是好主意，尤其在缩放、滚动、动画场景中。

弹出控件要重点测试，例如 combo box 下拉、菜单、tooltip、输入法候选窗。它们跨越 widget 和 graphics 两套事件系统。

不要用 proxy 逃避 item 设计。图形场景中的节点、端口、连线通常更适合自定义 item，而不是堆 QWidget。
