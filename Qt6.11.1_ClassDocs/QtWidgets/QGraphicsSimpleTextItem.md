# QGraphicsSimpleTextItem

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsSimpleTextItem`

## 1. 先建立直觉

`QGraphicsSimpleTextItem` 是场景中的轻量文本标签。它显示一段普通文本，支持字体、画笔、填充相关行为，但不提供富文本排版、链接、文本编辑或复杂文档能力。

如果你只需要给节点加名字、给坐标轴加刻度、给图标加短标签，它比 `QGraphicsTextItem` 更直接。

## 2. 类说明

`QGraphicsSimpleTextItem` 继承自 `QAbstractGraphicsShapeItem`。它可以用 `setText()` 设置文字，用 `setFont()` 设置字体，继承来的 `pen` 通常控制文字轮廓，`brush` 可用于填充。

它不是文本编辑器。需要可编辑文本、HTML、自动换行、文本交互和 `QTextDocument` 时，应使用 `QGraphicsTextItem`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsSimpleTextItem(parent)` | 创建空文本图元。 |
| `QGraphicsSimpleTextItem(QString, parent)` | 创建带文本的图元。 |
| `setText(const QString &)` / `text()` | 设置或读取文本。 |
| `setFont(const QFont &)` / `font()` | 设置或读取字体。 |
| `setPen()` / `pen()` | 控制文本轮廓。 |
| `setBrush()` / `brush()` | 控制文本填充。 |
| `boundingRect()` | 返回文本外接区域。 |
| `shape()` | 返回用于命中/碰撞的文本轮廓。 |
| `contains()` | 判断点是否命中文本形状。 |
| `paint()` | 绘制文本。 |
| `type()` | 返回 item 类型。 |

## 4. 关键用法

```cpp
auto *label = scene->addSimpleText("Node A");
label->setFont(QFont("Segoe UI", 10));
label->setBrush(Qt::darkBlue);
label->setPos(node->pos() + QPointF(-20, -36));
```

作为节点子项时：

```cpp
label->setParentItem(node);
label->setPos(-label->boundingRect().width() / 2, -40);
```

## 5. 使用场景

适合短标签、坐标刻度、节点标题、状态文字、调试标记、轻量图形注释。

如果需要文本选择、输入光标、HTML、链接、自动换行或复杂排版，用 `QGraphicsTextItem`。

## 6. 常见坑与经验

文本变化后 `boundingRect()` 也会变化。依赖文本居中的布局要在 `setText()` 后重新计算位置。

它不适合长文本。长说明应使用 `QGraphicsTextItem` 或场景外的普通 widget 面板。

缩放场景时文字也会缩放。如果需要屏幕像素大小恒定的标签，可以考虑 item flag 或在 view 层绘制 overlay。
