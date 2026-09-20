# QGraphicsLayoutItem

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsLayoutItem`

## 1. 先建立直觉

`QGraphicsLayoutItem` 是 Graphics View 布局系统的基础接口。它描述一个对象在图形布局里需要多大、能放到哪里、由哪个布局管理。

它不是普通 QWidget 布局里的 `QLayoutItem`。它工作在 `QGraphicsWidget`、`QGraphicsLayout`、`QGraphicsLinearLayout`、`QGraphicsGridLayout`、`QGraphicsAnchorLayout` 这一套场景内布局体系中。

## 2. 类说明

`QGraphicsLayoutItem` 可以由 `QGraphicsWidget` 继承，也可以由 `QGraphicsLayout` 继承。换句话说，一个图形 widget 可以是布局项，一个布局本身也可以被嵌套进另一个布局。

它围绕三个尺寸工作：minimum、preferred、maximum。布局根据这些尺寸和 `QSizePolicy` 分配 geometry。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `setGeometry(const QRectF &)` / `geometry()` | 设置或读取布局分配给该项的几何。 |
| `effectiveSizeHint(Qt::SizeHint, QSizeF)` | 读取综合约束后的尺寸提示。 |
| `setMinimumSize()` / `minimumSize()` | 设置或读取最小尺寸。 |
| `setPreferredSize()` / `preferredSize()` | 设置或读取首选尺寸。 |
| `setMaximumSize()` / `maximumSize()` | 设置或读取最大尺寸。 |
| `setSizePolicy()` / `sizePolicy()` | 控制该项在布局中如何扩展。 |
| `setOwnedByLayout(bool)` | 控制布局是否拥有该 item。 |
| `ownedByLayout()` | 判断是否由布局负责生命周期。 |
| `setParentLayoutItem()` / `parentLayoutItem()` | 设置或读取父布局项。 |
| `updateGeometry()` | 尺寸提示变化后通知布局重新计算。 |
| `isLayout()` | 判断该项是否本身就是布局。 |
| `graphicsItem()` | 若该项对应 `QGraphicsItem`，返回它。 |

## 4. 关键用法

自定义可布局图形对象时，通常继承 `QGraphicsWidget`，因为它已经实现了 `QGraphicsLayoutItem` 的大部分行为：

```cpp
auto *panel = new QGraphicsWidget;
panel->setPreferredSize(240, 120);
panel->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
```

尺寸变化后：

```cpp
setPreferredSize(newSize);
updateGeometry();
```

## 5. 使用场景

适合图形场景中的面板、节点内部布局、可缩放 UI、浮动工具条、需要 item 参与布局计算的自定义控件。

如果你的对象只是自由摆放的图元，不需要自动布局，就不必直接关心它。

## 6. 常见坑与经验

修改尺寸提示后要 `updateGeometry()`，否则父布局可能不知道需要重新排布。

`ownedByLayout` 影响生命周期。把 item 交给布局管理前，要明确谁负责删除。

Graphics View 布局使用浮点几何，和 QWidget 布局的整数像素直觉不同；缩放场景时这正是它的优势。
