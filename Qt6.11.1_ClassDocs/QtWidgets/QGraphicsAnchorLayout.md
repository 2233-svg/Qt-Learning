# QGraphicsAnchorLayout

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsAnchorLayout`

## 1. 先建立直觉

`QGraphicsAnchorLayout` 是 Graphics View 的锚点布局。它通过“某个 item 的某条边锚到另一个 item 的某条边”来描述位置关系。

它不像线性布局按顺序排，也不像网格布局按行列排；它更像约束布局。适合少量元素之间有明确对齐、贴边、等距、拉伸关系的场景内 UI。

## 2. 类说明

`QGraphicsAnchorLayout` 继承自 `QGraphicsLayout`。添加锚点后，布局会根据各 item 的尺寸提示和锚点关系求解几何。

它可以锚定 item 与 item，也可以锚定 item 与布局自身。`addCornerAnchors()` 适合把两个角对齐，`addAnchors()` 适合同时锚定水平或垂直两条边。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `addAnchor(first, firstEdge, second, secondEdge)` | 添加一条边到边的约束，并返回 `QGraphicsAnchor`。 |
| `anchor(first, firstEdge, second, secondEdge)` | 查询已存在的锚点。 |
| `addAnchors(first, second, orientations)` | 按水平/垂直方向批量添加对应边锚点。 |
| `addCornerAnchors(first, firstCorner, second, secondCorner)` | 把两个角对齐，内部会建立两条边约束。 |
| `setHorizontalSpacing()` / `horizontalSpacing()` | 设置默认水平间距。 |
| `setVerticalSpacing()` / `verticalSpacing()` | 设置默认垂直间距。 |
| `setSpacing(qreal)` | 同时设置默认水平和垂直间距。 |
| `setGeometry(QRectF)` | 求解锚点关系并分配 item 几何。 |
| `count()` / `itemAt()` / `removeAt()` | 管理布局项。 |
| `invalidate()` | 锚点或尺寸变化后标记布局失效。 |

## 4. 关键用法

```cpp
auto *layout = new QGraphicsAnchorLayout;
panel->setLayout(layout);

layout->addAnchor(title, Qt::AnchorLeft, layout, Qt::AnchorLeft)->setSpacing(8);
layout->addAnchor(title, Qt::AnchorTop, layout, Qt::AnchorTop)->setSpacing(8);

layout->addAnchor(body, Qt::AnchorTop, title, Qt::AnchorBottom)->setSpacing(6);
layout->addAnchors(body, layout, Qt::Horizontal);
```

两个控件角对齐：

```cpp
layout->addCornerAnchors(a, Qt::TopLeftCorner, b, Qt::TopRightCorner);
```

## 5. 使用场景

适合浮动面板、场景内 HUD、节点内部不规则布局、图形控件间相对贴靠、需要按边缘关系自适应的界面。

如果元素很多且结构规则，grid layout 更可读。Anchor layout 最适合少量但关系复杂的元素。

## 6. 常见坑与经验

约束不足会让布局自由度过高，结果可能不是你想的；约束过多又可能互相冲突。每个方向至少要能确定位置和尺寸。

锚点布局可读性依赖命名和组织。把相关约束放在一起写，比到处插入 `addAnchor()` 更容易维护。

默认 spacing 会影响未单独设置 spacing 的 anchor。局部间距异常时，先查该 anchor 是否覆盖了默认值。
