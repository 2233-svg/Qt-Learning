# QGraphicsItemGroup

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsItemGroup`

## 1. 先建立直觉

`QGraphicsItemGroup` 是把多个 `QGraphicsItem` 临时或永久组合成一个整体的图元。组合后，移动、选择、变换 group，就像操作一个 item。

它适合“用户框选多个对象后一起拖动/旋转/缩放”的图形编辑场景。它不是布局容器，也不会自动排列子项；它只是建立一层统一操作的父 item。

## 2. 类说明

`QGraphicsItemGroup` 继承自 `QGraphicsItem`。调用 `addToGroup()` 会把 item 加为 group 子项，同时尽量保持 item 在场景中的视觉位置不变；`removeFromGroup()` 则解除组合，同样保持场景变换。

场景也提供 `createItemGroup()` / `destroyItemGroup()` 便捷函数。复杂编辑器中，临时组合和业务模型中的“组对象”要区分：前者是交互便利，后者是文档结构。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsItemGroup(QGraphicsItem *parent)` | 创建图元组合。 |
| `addToGroup(QGraphicsItem *)` | 把 item 加入组，并保持场景中的视觉位置。 |
| `removeFromGroup(QGraphicsItem *)` | 从组中移除 item，并保持场景中的视觉位置。 |
| `boundingRect()` | 返回组内子项联合边界。 |
| `paint()` | group 自身通常不绘制内容，子项各自绘制。 |
| `opaqueArea()` | 返回不透明区域，供绘制优化使用。 |
| `isObscuredBy()` | 判断组是否被其他 item 遮挡。 |
| `type()` | 返回 group 类型。 |
| `setFlags()` | 继承自 `QGraphicsItem`，常用于让整个组可移动/可选择。 |

## 4. 关键用法

```cpp
auto *group = new QGraphicsItemGroup;
scene->addItem(group);

group->addToGroup(rectItem);
group->addToGroup(textItem);
group->setFlag(QGraphicsItem::ItemIsMovable);
group->setFlag(QGraphicsItem::ItemIsSelectable);
```

临时组合选中项：

```cpp
auto *group = scene->createItemGroup(scene->selectedItems());
group->setFlag(QGraphicsItem::ItemIsMovable);
```

## 5. 使用场景

适合图形编辑器的组合/解组、批量移动、临时选择组、节点和标签打包、多个图元作为一个控件拖动。

如果目的是自动布局多个 item，用 `QGraphicsLayout`；如果目的是表达业务层级，最好让文档模型也有对应结构，不要只依赖 group。

## 6. 常见坑与经验

组合会改变 item 的 parent item。依赖父子关系做坐标映射或业务归属时，要同步更新你的模型。

group 不会替你管理子项的语义。删除组、解组、保存文档时，要明确组和成员的生命周期。

对大量 item 频繁组合/解组会带来索引和变换更新成本。交互中可以临时 group，完成后再还原或固化。
