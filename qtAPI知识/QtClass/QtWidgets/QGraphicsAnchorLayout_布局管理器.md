<!-- 依据 Qt 6.11.1 头文件 qgraphicsanchorlayout.h 整理。 -->

# QGraphicsAnchorLayout 深入笔记

> 头文件：`#include <QGraphicsAnchorLayout>`  
> 模块：`Qt6::Widgets`  
> 继承：`QGraphicsLayoutItem -> QGraphicsLayout -> QGraphicsAnchorLayout`

## 1. 它解决什么问题

`QGraphicsAnchorLayout` 是 Graphics View 体系里的约束式布局。它不按“第 0 个、 第 1 个控件顺序排开”的思路布局，而是表达具体关系：

```text
标题左边  对齐  容器左边
标题右边  到    按钮左边，间隔 12
按钮右边  对齐  容器右边
标题上边、下边  与按钮上边、下边对齐
```

这些关系由 `QGraphicsAnchor` 表示，布局会综合 item 的最小/首选/最大尺寸、尺寸策略、边距和可用空间求解最终几何位置。

它适合：

- `QGraphicsWidget` 组成的检查器、节点详情卡、属性面板。
- 元素的边要精确对齐，但某些间隙要能伸缩。
- 需要在同一布局中混合贴边、对齐、固定间距、可扩张空隙等约束。

它不适合：

- 纯粹的一行或一列排列：`QGraphicsLinearLayout` 更短、更好维护。
- 需要响应屏幕宽度显隐、重排的复杂规则：更适合在上层按状态替换布局或调整锚点。
- 普通 `QWidget` 界面：这里应使用 `QHBoxLayout`、`QGridLayout` 等 QWidget 布局；`QGraphicsAnchorLayout` 面向 `QGraphicsWidget` / `QGraphicsLayoutItem`。

## 2. 三个对象分别负责什么

```text
QGraphicsWidget (根容器)
  └─ QGraphicsAnchorLayout (约束求解器)
       ├─ QGraphicsLayoutItem A
       ├─ QGraphicsLayoutItem B
       └─ QGraphicsAnchor (A 的边 <-> B 的边)
```

- `QGraphicsAnchorLayout`：收集 item 和锚点，计算每个 item 的 `geometry`。
- `QGraphicsLayoutItem`：可被布局的对象；最常见是 `QGraphicsWidget`，也可以是嵌套布局。
- `QGraphicsAnchor`：一条“边到边”的关系，负责局部间距和这段空隙能否伸缩。

调用 `addAnchor()`、`addAnchors()` 或 `addCornerAnchors()` 时，涉及的 item 会自动加入布局。不需要也没有类似 `addWidget()` 的独立入口。

## 3. 从一个可运行的约束模型开始

```cpp
#include <QGraphicsAnchorLayout>
#include <QGraphicsWidget>

auto *root = new QGraphicsWidget;
auto *title = new QGraphicsWidget;
auto *button = new QGraphicsWidget;
auto *layout = new QGraphicsAnchorLayout;

layout->addCornerAnchors(
    title, Qt::TopLeftCorner,
    layout, Qt::TopLeftCorner);

QGraphicsAnchor *gap = layout->addAnchor(
    title, Qt::AnchorRight,
    button, Qt::AnchorLeft);
gap->setSpacing(12.0);

layout->addAnchors(title, button, Qt::Vertical);
layout->addAnchor(
    button, Qt::AnchorRight,
    layout, Qt::AnchorRight);

root->setLayout(layout);
```

这段代码表达的不是固定坐标，而是：

1. `title` 的左上角贴住布局左上角。
2. `title` 右边到 `button` 左边间隔 `12`。
3. 两者上下边对齐。
4. `button` 右边贴住布局右边。

窗口变宽时，哪个 item 变宽、哪个间隙变宽，由它们各自的 `QSizePolicy`、尺寸提示，以及锚点的 `sizePolicy` 共同决定。

## 4. `addAnchor()`：创建一条精确的边关系

```cpp
QGraphicsAnchor *anchor = layout->addAnchor(
    firstItem, Qt::AnchorRight,
    secondItem, Qt::AnchorLeft);
```

`firstEdge` 和 `secondEdge` 使用 `Qt::AnchorPoint`，常见值有：

| 边 | 典型用途 |
| --- | --- |
| `Qt::AnchorLeft` / `Qt::AnchorRight` | 水平方向贴边、左右排列。 |
| `Qt::AnchorTop` / `Qt::AnchorBottom` | 垂直方向贴边、上下排列。 |
| `Qt::AnchorHorizontalCenter` | 水平居中关系。 |
| `Qt::AnchorVerticalCenter` | 垂直居中关系。 |

两个 item 的“相对边”，例如右边到左边、下边到上边，默认使用布局的同方向间距；两条同侧边或中心线之间的对齐通常不留额外间距。

返回的 `QGraphicsAnchor *` 由布局创建和拥有。它正是设置局部 `spacing`、`sizePolicy` 的对象：

```cpp
anchor->setSpacing(8.0);
anchor->setSizePolicy(QSizePolicy::Fixed);
```

不要手动 `delete anchor`。也不要跨不同 `QGraphicsAnchorLayout` 保存、复用它。

## 5. 批量锚定的两种快捷方式

### `addAnchors()`：对齐两条水平边或两条垂直边

```cpp
layout->addAnchors(title, button, Qt::Vertical);
```

`Qt::Vertical` 表示同时建立顶部对顶部、底部对底部的关系；`Qt::Horizontal` 表示左边对左边、右边对右边。默认同时使用两个方向。

它适合“两个 item 高度一致并上下对齐”或“两个 item 宽度一致并左右对齐”。如果只需单边关系，使用 `addAnchor()` 会更清楚。

### `addCornerAnchors()`：一次锚定两个边

```cpp
layout->addCornerAnchors(
    panel, Qt::TopLeftCorner,
    layout, Qt::TopLeftCorner);
```

它等价于把该角对应的两条边都对齐。适合将 item 固定到布局四角，表达力比连续两次 `addAnchor()` 更直观。

## 6. 全局间距和局部间距

布局默认有横向和纵向间距，分别由：

- `setHorizontalSpacing(qreal)`
- `setVerticalSpacing(qreal)`

统一设置：

```cpp
layout->setSpacing(10.0);
```

局部特例通过 `addAnchor()` 的返回值设置：

```cpp
QGraphicsAnchor *sectionGap = layout->addAnchor(
    header, Qt::AnchorBottom,
    body, Qt::AnchorTop);
sectionGap->setSpacing(16.0);
```

局部 anchor 显式设置了间距后，会覆盖布局的默认间距；调用 `QGraphicsAnchor::unsetSpacing()` 才会恢复使用布局默认值。把局部间距设为 `0` 是“明确不要间隔”，不是“恢复默认”。

合理的组织方式是：先用 `setSpacing()` 建立整个面板的节奏，只对少数特殊关系设置 anchor 间距。为每一条 anchor 都设置数值，会让约束图难以阅读，也失去统一调整的能力。

## 7. 所有权与移除：最容易写错的部分

布局会管理加入的 `QGraphicsLayoutItem`。当 `removeAt(index)` 移除一个 item 时，与该 item 关联的锚点也会移除，但 item 本身的所有权会转交给调用者。

因此正确的思路是：

```cpp
QGraphicsLayoutItem *item = layout->itemAt(index);
layout->removeAt(index);
delete item; // 仅当业务确认不再需要它
```

不要先 `delete item` 再让布局继续引用它，也不要只调用 `removeAt()` 后误以为 item 已被销毁。若仅想暂时隐藏某块内容，通常使用 `QGraphicsItem::setVisible(false)` 更合适，重建锚点的成本和复杂度都更高。

布局自身安装到 `QGraphicsWidget` 后，由该根 widget 管理；与普通 `QLayout` 一样，不应在安装后另行手动删除。

## 8. 布局何时重新计算

`invalidate()` 将布局标记为失效，后续布局激活时会重新计算几何。调用添加、移除锚点、修改间距或 item 尺寸策略等常规 API 时，框架通常会自行完成这件事；业务代码很少需要显式调用它。

`setGeometry(const QRectF &rect)` 是布局引擎把最终可用矩形交给布局时调用的入口。不要把它当成“手工设置 item 位置”的普通函数：手工调用很容易与上层 layout 激活过程对抗。

`sizeHint()` 是受保护接口，用于汇总各 item 和约束得出最小、首选、最大尺寸建议。根 `QGraphicsWidget` 需要根据内容调整大小时，布局会经由这个机制参与计算。

## 9. API 逐项说明

- `addAnchor(...)`：新增一条指定边到指定边的约束，并返回可调的 `QGraphicsAnchor`。
- `anchor(...)`：查询已有的特定边关系；若不存在则返回空指针。
- `addAnchors(...)`：按 `Qt::Horizontal` / `Qt::Vertical` 一次建立两条对齐关系。
- `addCornerAnchors(...)`：把两个角对应的两条边同时关联。
- `setHorizontalSpacing()`、`setVerticalSpacing()`、`setSpacing()`：设置布局默认间距。
- `horizontalSpacing()`、`verticalSpacing()`：查询当前默认间距。
- `count()`、`itemAt()`、`removeAt()`：按索引检查和管理布局中的 item。
- `invalidate()`、`setGeometry()`、`sizeHint()`：布局计算生命周期接口，主要由框架调用。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QGraphicsAnchorLayout(QGraphicsLayoutItem *parent = nullptr)` | 创建锚点布局。 | 通常最后安装到根 `QGraphicsWidget`。 |
| 析构 | `virtual ~QGraphicsAnchorLayout()` | 销毁布局和它管理的锚点关系。 | 已安装到 `QGraphicsWidget` 后通常由根 widget 管理。 |
| 建立约束 | `QGraphicsAnchor *addAnchor(QGraphicsLayoutItem *firstItem, Qt::AnchorPoint firstEdge, QGraphicsLayoutItem *secondItem, Qt::AnchorPoint secondEdge)` | 建立一条边到边关系，并返回该关系的 anchor。 | 返回对象归布局所有，可设置局部间距和 anchor 尺寸策略。 |
| 查询约束 | `QGraphicsAnchor *anchor(QGraphicsLayoutItem *firstItem, Qt::AnchorPoint firstEdge, QGraphicsLayoutItem *secondItem, Qt::AnchorPoint secondEdge)` | 查询已存在的同一条边关系。 | 不存在时返回 `nullptr`；不负责创建。 |
| 批量约束 | `void addAnchors(QGraphicsLayoutItem *firstItem, QGraphicsLayoutItem *secondItem, Qt::Orientations orientations = Qt::Horizontal \| Qt::Vertical)` | 按方向一次创建两条对应边的对齐关系。 | `Qt::Horizontal` 对齐左右边，`Qt::Vertical` 对齐上下边。 |
| 角约束 | `void addCornerAnchors(QGraphicsLayoutItem *firstItem, Qt::Corner firstCorner, QGraphicsLayoutItem *secondItem, Qt::Corner secondCorner)` | 将两个角所对应的两条边同时关联。 | 用于贴四角，比两次 `addAnchor()` 更清晰。 |
| 设置 | `void setHorizontalSpacing(qreal spacing)` | 设置默认横向间距。 | 影响未显式设置局部间距的左右相对边。 |
| 设置 | `void setVerticalSpacing(qreal spacing)` | 设置默认纵向间距。 | 影响未显式设置局部间距的上下相对边。 |
| 设置 | `void setSpacing(qreal spacing)` | 同时设置默认横向、纵向间距。 | 适合建立全局间距规则。 |
| 查询 | `qreal horizontalSpacing() const` | 查询默认横向间距。 | 局部 anchor 的显式间距不会改变此值。 |
| 查询 | `qreal verticalSpacing() const` | 查询默认纵向间距。 | 局部 anchor 的显式间距不会改变此值。 |
| 容器接口 | `int count() const` | 返回布局管理的 item 数量。 | 被锚定的 item 会自动加入布局。 |
| 容器接口 | `QGraphicsLayoutItem *itemAt(int index) const` | 按索引取得 item。 | 越界时返回空指针；不要借此取得 item 的所有权。 |
| 移除 | `void removeAt(int index)` | 从布局移除指定 item 及其关联锚点。 | item 所有权转给调用者；需要时自行删除或重新加入其它布局。 |
| 布局生命周期 | `void invalidate()` | 标记布局需要重新计算。 | 常规约束/间距 API 已会处理，业务代码很少显式调用。 |
| 布局生命周期 | `void setGeometry(const QRectF &rect)` | 接收上层分配的可用矩形并安排各 item。 | 框架调用，不要用它替代布局规则。 |
| 受保护布局接口 | `QSizeF sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const` | 计算最小、首选或最大尺寸建议。 | 供布局系统使用；派生扩展时才需关注。 |

## 11. 排查清单

1. item 不在预期位置：把约束画成“谁的哪条边连到谁的哪条边”，先排查方向是否写反。
2. 两个 item 之间没有间隔：确认是相对边关系，并检查 layout 或该 anchor 的 spacing。
3. 剩余空间分配不对：同时检查 item 的 `QSizePolicy` 和 anchor 的 `sizePolicy`，两者控制不同对象。
4. 移除后崩溃：`removeAt()` 不会删除 item；确认调用者是否正确接管和处理它。
5. 想叠加或覆盖约束：先用 `anchor()` 查已有关系；重复、冲突的锚点会让求解意图难以维护。

### 一句话总结

`QGraphicsAnchorLayout` 用边到边约束描述 Graphics View 中的几何关系：布局拥有锚点，item 被锚定时自动加入，统一间距负责全局节奏，单条 `QGraphicsAnchor` 负责局部例外。
