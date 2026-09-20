# QGraphicsLinearLayout

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsLinearLayout`

## 1. 先建立直觉

`QGraphicsLinearLayout` 是 Graphics View 中的一维布局：要么横向排一排，要么纵向排一列。它类似 QWidget 里的 `QHBoxLayout` / `QVBoxLayout`，但管理的是 `QGraphicsLayoutItem`。

它适合构建场景内面板、节点内部标题/内容/端口列表、浮动工具条等结构。

## 2. 类说明

`QGraphicsLinearLayout` 继承自 `QGraphicsLayout`。它按顺序排列 item，并通过 spacing、stretch factor、alignment 和 size policy 控制空间分配。

方向可以是水平或垂直。复杂二维布局用 `QGraphicsGridLayout`，关系约束布局用 `QGraphicsAnchorLayout`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsLinearLayout(Qt::Orientation)` | 创建水平或垂直图形线性布局。 |
| `addItem(QGraphicsLayoutItem *)` | 在末尾添加布局项。 |
| `insertItem(int, QGraphicsLayoutItem *)` | 在指定位置插入项。 |
| `removeItem(QGraphicsLayoutItem *)` / `removeAt(int)` | 移除布局项。 |
| `itemAt(int)` / `count()` | 读取指定项或项数量。 |
| `setOrientation()` / `orientation()` | 设置或读取布局方向。 |
| `setSpacing(qreal)` / `spacing()` | 设置统一间距。 |
| `setItemSpacing(int, qreal)` / `itemSpacing(int)` | 设置某个位置后的间距。 |
| `setStretchFactor(item, int)` / `stretchFactor(item)` | 设置空间分配权重。 |
| `setAlignment(item, Qt::Alignment)` / `alignment(item)` | 设置某项在分配区域中的对齐。 |
| `setGeometry(QRectF)` | 按当前规则分配子项几何。 |
| `sizeHint()` | 根据子项尺寸提示计算布局尺寸。 |

## 4. 关键用法

```cpp
auto *layout = new QGraphicsLinearLayout(Qt::Vertical);
layout->setSpacing(6);
layout->addItem(title);
layout->addItem(body);
layout->setStretchFactor(body, 1);

panel->setLayout(layout);
```

水平工具条：

```cpp
auto *tools = new QGraphicsLinearLayout(Qt::Horizontal);
tools->addItem(selectButton);
tools->addItem(moveButton);
tools->addItem(zoomButton);
```

## 5. 使用场景

适合场景内属性面板、节点内部纵向区域、按钮条、状态条、标签加输入区等一维排列。

如果需要行列对齐，用 `QGraphicsGridLayout`；如果需要边缘互相锚定，用 `QGraphicsAnchorLayout`。

## 6. 常见坑与经验

stretch factor 只有在有额外空间可分时才明显。子项 maximum size 太小，会限制扩展。

spacing 是布局策略的一部分，不要让每个子 item 自己留硬编码空白，否则整体间距很难统一。

item 顺序就是视觉顺序。动态插入/删除时要同时维护业务模型顺序，避免保存和显示不一致。
