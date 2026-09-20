# QGraphicsWidget

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsWidget`

## 1. 先建立直觉

`QGraphicsWidget` 是 Graphics View 里的“类 widget 图元”。它仍然是 `QGraphicsItem`，但拥有更接近 QWidget 的属性：geometry、layout、size policy、palette、font、window flags、focus policy。

如果普通 item 是“自己画、自己管大小”的图元，`QGraphicsWidget` 则适合做可布局的图形界面元素：浮动面板、节点里的区域布局、图形场景里的小窗口。

## 2. 类说明

`QGraphicsWidget` 继承自 `QGraphicsObject` 和 `QGraphicsLayoutItem`。这意味着它既有 QObject/属性/信号能力，又能参与 `QGraphicsLayout` 家族的布局计算。

它不是 `QWidget`，不能直接放进普通 `QLayout`。它的布局系统是 Graphics View 的布局系统，使用 `QGraphicsLinearLayout`、`QGraphicsGridLayout`、`QGraphicsAnchorLayout` 等。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `setGeometry(const QRectF &)` / `geometry()` | 设置或读取图形 widget 的几何。 |
| `resize()` / `size()` | 调整或读取尺寸。 |
| `setLayout(QGraphicsLayout *)` / `layout()` | 设置图形布局。 |
| `setSizePolicy()` / `sizePolicy()` | 控制在图形布局中的扩展策略。 |
| `setMinimumSize()` / `minimumSize()` | 设置最小尺寸。 |
| `setPreferredSize()` / `preferredSize()` | 设置首选尺寸。 |
| `setMaximumSize()` / `maximumSize()` | 设置最大尺寸。 |
| `setWindowFlags()` / `windowFlags()` | 让图形 widget 表现为场景内窗口。 |
| `setWindowTitle()` / `windowTitle()` | 设置场景内窗口标题。 |
| `setPalette()` / `palette()` | 设置调色板。 |
| `setFont()` / `font()` | 设置字体。 |
| `setAutoFillBackground(bool)` | 控制是否自动填充背景。 |
| `setFocusPolicy()` / `focusPolicy()` | 控制焦点获取方式。 |
| `paintWindowFrame()` | 绘制图形窗口边框，子类可定制。 |
| `geometryChanged()` | 几何变化时发出。 |

## 4. 关键用法

```cpp
auto *panel = new QGraphicsWidget;
auto *layout = new QGraphicsLinearLayout(Qt::Vertical);

layout->addItem(titleItem);
layout->addItem(contentItem);
panel->setLayout(layout);
panel->resize(240, 120);
scene->addItem(panel);
```

作为场景内窗口：

```cpp
panel->setWindowFlags(Qt::Window);
panel->setWindowTitle("Inspector");
```

这会给它窗口语义，但仍然是在 graphics scene 里，不是操作系统顶层窗口。

## 5. 使用场景

适合节点内部布局、图形场景中的浮动面板、可缩放 UI、小型属性窗、可布局的图元组合、需要 Graphics View 坐标变换的界面元素。

如果你只是想用普通按钮、输入框、列表，优先用 QWidget 界面；只有确实要把它们嵌入场景、随场景缩放或和图元混排时，才进入 Graphics Widget 体系。

## 6. 常见坑与经验

`QGraphicsWidget` 和 `QWidget` 名字像，但生态不同。普通 `QHBoxLayout` 不能直接管理它，普通 widget parent 也不是它的图形父子关系。

图形布局里的尺寸是 `QSizeF`，坐标是浮点数。写自定义布局或定位时不要强行转 int，缩放场景时会产生抖动。

`autoFillBackground` 只解决背景填充，不等于完整样式表系统。复杂视觉仍要在 paint 或 style option 中处理。
