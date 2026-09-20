# QGraphicsItem 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QGraphicsItem>`  
> 模块：`Qt6::Widgets`  
> 继承：无。它是抽象基类；常见派生类有 `QGraphicsRectItem`、`QGraphicsPixmapItem`、`QGraphicsTextItem`、`QGraphicsWidget` 与 `QGraphicsObject`。

`QGraphicsItem` 是 Graphics View 架构里“场景中的一个对象”。`QGraphicsScene` 负责保存、索引和挑选图元，`QGraphicsView` 负责把场景显示到某个视口，而 `QGraphicsItem` 负责描述自身的几何、绘制、层级、命中范围和输入行为。

它不是 `QWidget`：没有窗口句柄，没有布局，也不直接接收操作系统消息。它也不是 `QObject`：不能直接声明信号槽或依赖 `QObject` 父子关系。需要信号槽的自定义图元通常继承 `QGraphicsObject`；需要类似窗口部件能力的图元通常使用 `QGraphicsWidget`。

## 1. 它解决什么问题

在画布、流程图、节点编辑器、拓扑图、游戏地图编辑器中，屏幕上可能同时存在成百上千个可移动、可缩放、可选择、可命中的对象。若每个对象都是一个 `QWidget`，窗口部件树、重绘和事件处理的成本会很快变高。

`QGraphicsItem` 把这些对象压缩成更轻的“图元”模型：

- 只要求图元报告自己的局部边界，并在 `QPainter` 上绘制；
- 允许图元形成父子树，子图元随父图元移动、旋转和缩放；
- 让 `QGraphicsScene` 根据边界进行空间索引和候选筛选；
- 用 `shape()` 提供比矩形更精确的命中和碰撞；
- 让同一个图元同时参与绘制、选择、鼠标、键盘、悬停、拖放和触摸。

因此，它解决的不是“画一条线”这种单一问题，而是让大量可交互的二维对象能在同一场景里稳定协作。

## 2. 先记住两条抽象类契约

自定义 `QGraphicsItem` 至少必须实现：

```cpp
QRectF boundingRect() const override;
void paint(QPainter *painter,
           const QStyleOptionGraphicsItem *option,
           QWidget *widget = nullptr) override;
```

二者职责完全不同：

| 函数 | Qt 用它做什么 | 不能做什么 |
| --- | --- | --- |
| `boundingRect()` | 场景索引、脏区计算、初步裁剪、粗略碰撞候选 | 不能只返回“看起来大致差不多”的区域 |
| `paint()` | 真正把像素画进当前 painter | 不能修改会影响 `boundingRect()` 的几何状态 |

`boundingRect()` 返回的是**图元局部坐标**中的矩形。它必须包含 `paint()` 可能绘制出来的全部像素，包括画笔宽度、阴影、外描边等。比如画一个宽度为 `4` 的 `QPen`，边界通常要向外预留至少 `2` 个逻辑单位；否则边缘可能被裁掉，移动前后的旧像素也可能残留。

更重要的一条规则是：

> 只要某次修改会改变 `boundingRect()` 或 `shape()` 所依赖的几何范围，必须在修改前调用 `prepareGeometryChange()`。

位置变化不属于这条规则，`setPos()` 会由 Qt 自己处理；但“矩形的宽高变了”“路径换了”“线宽改变且边界随之变大”都属于几何变化。

## 3. 一个可调整尺寸的自定义图元

下面的例子不是为了堆功能，而是展示三个最容易被忽略的边界：局部坐标、画笔外扩和几何变更通知。

```cpp
#include <QGraphicsItem>
#include <QPainter>

class NodeItem final : public QGraphicsItem
{
public:
    explicit NodeItem(QGraphicsItem *parent = nullptr)
        : QGraphicsItem(parent)
    {
        setFlags(ItemIsMovable | ItemIsSelectable | ItemSendsGeometryChanges);
        setAcceptHoverEvents(true);
    }

    QRectF boundingRect() const override
    {
        constexpr qreal penWidth = 2.0;
        return m_rect.adjusted(-penWidth / 2, -penWidth / 2,
                              penWidth / 2, penWidth / 2);
    }

    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option,
               QWidget *widget = nullptr) override
    {
        Q_UNUSED(widget);

        const bool selected = option->state & QStyle::State_Selected;
        painter->setPen(QPen(selected ? QColor("#d94f36") : QColor("#30343b"), 2));
        painter->setBrush(m_hovered ? QColor("#d9eef8") : QColor("#f6f8fa"));
        painter->drawRoundedRect(m_rect, 6, 6);
    }

    void setNodeRect(const QRectF &rect)
    {
        if (m_rect == rect)
            return;

        prepareGeometryChange();
        m_rect = rect;
        update();
    }

protected:
    void hoverEnterEvent(QGraphicsSceneHoverEvent *event) override
    {
        m_hovered = true;
        update();
        QGraphicsItem::hoverEnterEvent(event);
    }

    void hoverLeaveEvent(QGraphicsSceneHoverEvent *event) override
    {
        m_hovered = false;
        update();
        QGraphicsItem::hoverLeaveEvent(event);
    }

private:
    QRectF m_rect {0, 0, 160, 72};
    bool m_hovered = false;
};
```

使用时把它加入场景：

```cpp
auto *scene = new QGraphicsScene(this);
auto *node = new NodeItem;
node->setPos(100, 80);
scene->addItem(node);
```

`scene->addItem(node)` 后，场景取得图元的所有权。若图元已有父图元，删除父图元会删除它的所有子图元；不要再把同一个裸指针交给其他所有者重复释放。

## 4. 四套坐标系：很多 bug 都从这里开始

Graphics View 中至少要分清四种坐标：

| 坐标系 | 原点和含义 | 常见 API / 典型问题 |
| --- | --- | --- |
| 图元局部坐标 | 图元自身的 `(0, 0)`；`paint()`、`boundingRect()`、`shape()` 都使用它 | 在 `paint()` 中不能假设 `(0, 0)` 是场景左上角 |
| 父图元坐标 | 父图元的局部坐标 | `pos()` 是当前图元原点在父坐标中的位置 |
| 场景坐标 | 整张 `QGraphicsScene` 共用的坐标 | 顶层图元的 `pos()` 等于其场景位置；鼠标事件常需要 `scenePos()` |
| 设备/视口坐标 | `QGraphicsView` 视口像素相关的坐标 | 视图缩放、旋转、DPR 都会影响；`deviceTransform()` 用于少数设备相关场景 |

例如父图元在场景 `(100, 50)`，子图元 `setPos(20, 10)`，则子图元局部原点的 `scenePos()` 是 `(120, 60)`。父图元再旋转时，`pos()` 仍是父坐标中的 `(20, 10)`，但 `scenePos()` 会随变换重新计算。

### 4.1 `pos()` 不等于绘制矩形的位置

`pos()` 移动的是**图元局部原点**，不是 `boundingRect()` 的左上角。局部边界可以是 `QRectF(-20, -10, 40, 20)`，这时原点位于图元中心。节点、旋转手柄、连接端口这类对象往往故意这样设计，以便围绕原点旋转。

### 4.2 映射矩形时，为什么有时得到 `QPolygonF`

旋转或错切后的矩形不再是轴对齐矩形。`mapToScene(const QRectF &)` 返回 `QPolygonF`，保留四个角的实际位置；`mapRectToScene()` 返回 `QRectF`，只是包住该结果的轴对齐外接矩形。

做精确区域运算、橡皮筋框选、连接线端点计算时，优先用多边形或路径映射；仅用于脏区、粗略可见范围时才用 `mapRect...()`。

## 5. 几何、绘制、命中是三件事

初学时容易把 `boundingRect()` 当成图元的一切。实际上 QGraphics View 用的是分层策略：

1. `boundingRect()`：快，适合空间索引和初筛；
2. `shape()`：精确轮廓，适合鼠标命中和精确碰撞；
3. `contains()` / `collidesWithItem()`：最终判断，可按需求重写；
4. `opaqueArea()`：哪些区域完全不透明，用于遮挡优化。

默认 `shape()` 基于 `boundingRect()`，默认 `contains()` 也依赖 `shape()`。对于细线、圆环、星形、带透明孔洞的图元，矩形命中会很不自然，应重写 `shape()`；但不要为了“精确”每次都构造极其复杂的路径，频繁命中测试会直接反映到交互性能上。

`ItemContainsChildrenInShape` 是对场景的一个承诺：你保证所有子图元都位于本图元的 `shape()` 内。Qt 可据此跳过一些碰撞检查。若承诺不成立，查询结果可能错误，因此不要把它当成普通优化开关。

## 6. 父子图元、分组与所有权

`QGraphicsItem` 的父子树决定变换继承、可见性、有效透明度和堆叠关系。它与 `QObject` 父子树是两套概念：

- 图元树使用 `setParentItem()` / `parentItem()`；
- `QGraphicsObject` 虽然也是 `QObject`，但图元层级仍然应该用 `setParentItem()`；
- 设置图元父项会把子图元加入父项所在的场景；从父项脱离后，它仍可能留在原场景；
- 删除一个图元会删除其所有子图元。

`QGraphicsItemGroup` 是把多个现有图元临时作为整体操作的工具。`setGroup()` 可以手动设置组归属，不过日常更常用 `QGraphicsScene::createItemGroup()` 与 `destroyItemGroup()`，因为场景会统一处理成员的父子关系和坐标保持。

## 7. 变换和堆叠：位置、矩阵不是一回事

`setPos()` 只改变图元原点在父坐标中的位置。旋转、缩放、矩阵变换则改变局部坐标如何映射到父坐标。

| 需求 | 合适 API |
| --- | --- |
| 平移一个节点 | `setPos()`、`moveBy()` |
| 绕某点旋转 | `setTransformOriginPoint()` + `setRotation()` |
| 等比缩放 | `setScale()` |
| 一次设置仿射矩阵 | `setTransform()` |
| 拼接多个独立变换对象，例如 `QGraphicsRotation`、`QGraphicsScale` | `setTransformations()` |
| 控制前后遮挡顺序 | `setZValue()`、`stackBefore()` |

变换原点以图元局部坐标表示。若希望一个宽 `160`、高 `72` 的节点绕中心旋转，应设置 `setTransformOriginPoint(80, 36)`，而不是场景坐标。

`ItemIgnoresTransformations` 常用于标签、控制点、拖拽手柄：视图放大时图元的位置仍会随场景走，但它自身保持近似固定的设备大小。此时普通 `sceneTransform()` 不足以判断其屏幕大小，需在绘制或命中相关的少数场景使用 `deviceTransform(viewportTransform)`。

## 8. 可见性、透明度、焦点与输入

图元不可见时不会绘制，也通常不会参与输入。父图元不可见时，子图元即使自身 `isVisible()` 为真，最终也不可见；同理，`effectiveOpacity()` 会综合父项透明度与相关 flags，而 `opacity()` 只是本图元直接设置的值。

可交互性来自多个开关的组合：

- 选择：设置 `ItemIsSelectable`，再由 `setSelected()` 或鼠标操作改变选择状态；
- 拖动：设置 `ItemIsMovable`；默认鼠标处理会在合适情况下移动它；
- 键盘焦点：设置 `ItemIsFocusable`，调用 `setFocus()` 后才能稳定收到键盘事件；
- 悬停：`setAcceptHoverEvents(true)` 后才会收到 `hover...Event()`；
- 拖放：`setAcceptDrops(true)` 后才会收到 `drag...Event()` 和 `dropEvent()`；
- 触摸：`setAcceptTouchEvents(true)` 后才会收到触摸事件分发；
- 输入法：设置 `ItemAcceptsInputMethod`，并实现 `inputMethodEvent()` / `inputMethodQuery()`。

`grabMouse()` 和 `grabKeyboard()` 是强制抓取。它们适合拖拽或临时模式操作，结束时必须对应调用 `ungrabMouse()` / `ungrabKeyboard()`；不要把它们作为常规焦点管理手段。

## 9. 缓存、重绘和效果

`update()` 只是让指定局部区域失效，安排之后重绘；它不会立刻调用 `paint()`。需要即时刷新界面时，应该重新审视交互设计，而不是指望在图元里同步刷屏。

| 缓存模式 | 适合什么 | 代价和限制 |
| --- | --- | --- |
| `NoCache` | 内容经常变、图元很简单 | 每次绘制都重新执行 `paint()` |
| `ItemCoordinateCache` | 局部内容复杂，但缩放/旋转相对少 | 使用局部坐标缓存；缓存尺寸或缩放策略不当会模糊或占内存 |
| `DeviceCoordinateCache` | 视图变换稳定、图元只移动 | 在设备坐标缓存；旋转、缩放等变换会使缓存重建 |

`scroll(dx, dy, rect)` 试图复用本图元缓存中的一部分内容，适合大而稳定的自绘图元局部滚动；普通节点没有必要为了它复杂化实现。

`setGraphicsEffect()` 可安装一个 `QGraphicsEffect`，例如阴影或模糊。效果对象一旦安装，目标图元接管它的所有权；同一个效果对象不能同时服务两个图元。效果扩大视觉范围时，图元自身的 `boundingRect()` 仍应只描述图元的正常局部几何，效果的外扩由效果系统处理。

## 10. flags 不是装饰，它们改变框架行为

### 10.1 `GraphicsItemFlag` 速查

| 枚举值 | 含义 | 什么时候用 / 注意 |
| --- | --- | --- |
| `ItemIsMovable` | 允许默认鼠标逻辑移动图元 | 做可拖动节点；父项被拖动时可移动子项也会随选择处理 |
| `ItemIsSelectable` | 允许被选择 | 选择状态会反映到 `QStyleOptionGraphicsItem::state` |
| `ItemIsFocusable` | 允许取得键盘焦点 | 需要键盘事件时设置 |
| `ItemClipsToShape` | 把本图元绘制裁剪到 `shape()` | 复杂 path 会增加裁剪成本 |
| `ItemClipsChildrenToShape` | 把子图元绘制和事件区域裁剪到本项形状 | 容器图元需要硬裁剪时使用 |
| `ItemIgnoresTransformations` | 忽略视图与祖先的部分变换，保持设备尺寸 | 常用于手柄、标签；设备坐标相关计算要格外谨慎 |
| `ItemIgnoresParentOpacity` | 不继承父项透明度 | 做独立浮层时使用 |
| `ItemDoesntPropagateOpacityToChildren` | 本项透明度不传给子项 | 父项淡出但子项需保持不透明时使用 |
| `ItemStacksBehindParent` | 始终排在父项后面 | 背景、阴影类子项常用 |
| `ItemUsesExtendedStyleOption` | 请求更精确的 `QStyleOptionGraphicsItem` 暴露区域 | 复杂且可局部绘制的图元才可能受益 |
| `ItemHasNoContents` | 声明本项不绘制内容 | 纯容器项；`paint()` 不会用于实际内容 |
| `ItemSendsGeometryChanges` | 让位置、变换等变化进入 `itemChange()` | 想限制移动范围或监听位置必须设置 |
| `ItemAcceptsInputMethod` | 接收输入法事件 | 可编辑文本类图元需要实现对应回调 |
| `ItemNegativeZStacksBehindParent` | `z < 0` 时自动放在父项后 | 让子背景随 z 值自动前后切换 |
| `ItemIsPanel` | 把图元作为面板 | 模态、焦点范围相关的高级场景使用 |
| `ItemIsFocusScope` | 焦点域标记 | Qt 内部使用，不应作为普通业务开关 |
| `ItemSendsScenePositionChanges` | 场景位置变化进入 `itemChange()` | 关心祖先移动造成的最终 scene 位置变化时设置 |
| `ItemStopsClickFocusPropagation` | 阻止点击焦点继续向面板祖先传播 | 面板化界面中的精细焦点控制 |
| `ItemStopsFocusHandling` | 阻止焦点处理继续向祖先传播 | 高级面板焦点逻辑，少用 |
| `ItemContainsChildrenInShape` | 承诺子项都在本项形状内 | 仅在承诺严格成立时启用，错误设置会造成碰撞查询错误 |

### 10.2 `GraphicsItemChange`：在改变前拒绝或改写，在改变后观察

`itemChange(change, value)` 有两类通知：

- 名称不带 `HasChanged` 的通常发生在改变前；返回值可替换将要设置的值；
- 名称带 `HasChanged` 的发生在改变后；此时返回值会被忽略，适合同步附属状态。

不要在 `ItemPositionChange` 回调内再次 `setPos()`，这会造成递归。应直接返回一个修正后的 `QPointF`。

```cpp
QVariant NodeItem::itemChange(GraphicsItemChange change, const QVariant &value)
{
    if (change == ItemPositionChange && scene() && scene()->sceneRect().isValid()) {
        const QRectF bounds = scene()->sceneRect();
        const QPointF wanted = value.toPointF();
        return QPointF(qBound(bounds.left(), wanted.x(), bounds.right()),
                       qBound(bounds.top(), wanted.y(), bounds.bottom()));
    }
    return QGraphicsItem::itemChange(change, value);
}
```

| 枚举值 | 触发时机与 `value` | 用途 |
| --- | --- | --- |
| `ItemPositionChange` | 改位置前，`QPointF` | 约束或吸附位置 |
| `ItemVisibleChange` | 改可见性前，`bool` | 拒绝或调整显示状态 |
| `ItemEnabledChange` | 改启用状态前，`bool` | 控制禁用条件 |
| `ItemSelectedChange` | 改选择状态前，`bool` | 限制选择 |
| `ItemParentChange` | 改父项前，`QGraphicsItem*` | 验证新的图元父项 |
| `ItemChildAddedChange` | 子项加入后，`QGraphicsItem*` | 观察子项进入 |
| `ItemChildRemovedChange` | 子项移除后，`QGraphicsItem*` | 观察子项离开 |
| `ItemTransformChange` | 改矩阵变换前，`QTransform` | 调整矩阵 |
| `ItemPositionHasChanged` | 改位置后，`QPointF` | 跟随更新连线等附属对象 |
| `ItemTransformHasChanged` | 改矩阵后，`QTransform` | 观察变换完成 |
| `ItemSceneChange` | 改场景前，`QGraphicsScene*` | 观察或拒绝迁移场景 |
| `ItemVisibleHasChanged` | 改可见性后，`bool` | 同步外部状态 |
| `ItemEnabledHasChanged` | 改启用后，`bool` | 同步外部状态 |
| `ItemSelectedHasChanged` | 改选择后，`bool` | 更新属性面板等 |
| `ItemParentHasChanged` | 改父项后，`QGraphicsItem*` | 更新与父项的关联 |
| `ItemSceneHasChanged` | 改场景后，`QGraphicsScene*` | 场景资源初始化或解绑 |
| `ItemCursorChange` | 改光标前，`QCursor` | 一般很少重写 |
| `ItemCursorHasChanged` | 改光标后，`QCursor` | 观察光标配置 |
| `ItemToolTipChange` | 改提示前，`QString` | 调整提示文本 |
| `ItemToolTipHasChanged` | 改提示后，`QString` | 观察提示更新 |
| `ItemFlagsChange` | 改 flags 前，`GraphicsItemFlags` | 统一限制标记组合 |
| `ItemFlagsHaveChanged` | 改 flags 后，`GraphicsItemFlags` | 更新依赖 flags 的状态 |
| `ItemZValueChange` | 改 z 值前，`qreal` | 限制层级范围 |
| `ItemZValueHasChanged` | 改 z 值后，`qreal` | 更新层级相关状态 |
| `ItemOpacityChange` | 改不透明度前，`qreal` | 钳制透明度等 |
| `ItemOpacityHasChanged` | 改不透明度后，`qreal` | 观察结果 |
| `ItemScenePositionHasChanged` | 最终场景位置改变后，`QPointF` | 祖先移动也要跟踪时使用；须启用相应 flag |
| `ItemRotationChange` | 改旋转前，`qreal` | 角度吸附 |
| `ItemRotationHasChanged` | 改旋转后，`qreal` | 观察旋转 |
| `ItemScaleChange` | 改缩放前，`qreal` | 限制缩放范围 |
| `ItemScaleHasChanged` | 改缩放后，`qreal` | 观察缩放 |
| `ItemTransformOriginPointChange` | 改变换原点前，`QPointF` | 限制原点 |
| `ItemTransformOriginPointHasChanged` | 改变换原点后，`QPointF` | 观察原点变更 |

## 11. 事件、默认行为和场景事件过滤器

图元事件由 `sceneEvent()` 分发到细分虚函数。通常只重写所需的具体事件，例如 `mousePressEvent()` 或 `hoverMoveEvent()`；只有需要统一拦截多种事件时才重写 `sceneEvent()`。

若覆盖默认行为，要有意识地决定是否调用基类：

- 希望保留 `ItemIsMovable` / `ItemIsSelectable` 的默认鼠标语义时，调用基类事件处理；
- 完全自行实现拖动、框选或多指交互时，接受事件并维护自己的状态；
- 事件未处理时，调用 `event->ignore()` 或交给基类，才可能让其他图元或场景继续处理。

`installSceneEventFilter(filterItem)` 与 `QObject::installEventFilter()` 不同：过滤者和被过滤者都是 `QGraphicsItem`，由场景事件系统调用 `filterItem->sceneEventFilter(watched, event)`。适合实现统一的选框、连接线交互或代理编辑器；不要把它和 QWidget/QObject 事件过滤器混用。

## 12. 类型、数据和运行时识别

`QGraphicsItem` 没有 RTTI 强制要求。Qt 为常见图元分配了 `Type` 值；自定义类应从 `UserType` 往上定义自己的常量，并重写 `type()`：

```cpp
class PortItem final : public QGraphicsItem
{
public:
    enum { Type = QGraphicsItem::UserType + 1 };

    int type() const override { return Type; }
    // ...
};

QGraphicsItem *item = /* scene()->itemAt(...) */;
if (auto *port = qgraphicsitem_cast<PortItem *>(item)) {
    // 这里已经确认 item->type() 与 PortItem::Type 匹配。
}
```

`qgraphicsitem_cast` 检查的是 `type()` 值，不是通用的 C++ 继承关系检查。不同自定义类绝不能返回同一个 `Type`；若类层次很复杂，也可以用 `dynamic_cast`，前提是工程启用了 RTTI。

`data(int key)` / `setData(int key, const QVariant &)` 是图元的轻量附加数据槽。它适合存放业务 ID、临时标记等少量元信息；不要把它当成完整的数据模型，也不要让互不相关的模块无约定地复用同一个 key。

## 13. 常见失误

| 现象 | 真正原因 | 处理方式 |
| --- | --- | --- |
| 改宽高后旧位置有残影，或 scene 查询不到新区域 | 修改几何前没调用 `prepareGeometryChange()` | 在改变几何成员前调用它 |
| 线条点击很难选中 | 默认矩形或路径不符合实际线宽 | 重写 `shape()`，使用 `QPainterPathStroker` 建立可点区域 |
| 图元旋转后框选区域奇怪 | 把旋转后的区域当成普通 `QRectF` | 用 `mapToScene(rect)` 的多边形结果 |
| `itemChange()` 没有收到位置通知 | 没有设置 `ItemSendsGeometryChanges` | 在构造时启用该 flag |
| 子项“自己可见”却没有显示 | 父项不可见、透明、被裁剪或在面板外 | 检查祖先可见性、`effectiveOpacity()` 和裁剪 flags |
| 单击后键盘事件仍到不了图元 | 仅重写键盘事件，没设置可聚焦或获取焦点 | 设置 `ItemIsFocusable`，合适时调用 `setFocus()` |
| 图元尺寸随视图缩放而变化但希望保持固定 | 图元仍参与 view transform | 考虑 `ItemIgnoresTransformations`，同时处理设备坐标差异 |

## API 速查表
下表按 Qt 6.11.1 的 `qgraphicsitem.h` 直接声明整理。坐标映射的 `qreal x, y, w, h` 版本只是 `QPointF` 或 `QRectF` 版本的内联便利重载，仍单列以免在查 API 时误解返回类型。

### 14.1 构造、归属与状态

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QGraphicsItem(QGraphicsItem *parent = nullptr)` | 创建图元，可立即指定图元父项 | 抽象类不能直接实例化；父项不是 `QObject` 父对象 |
| 生命周期 | `virtual ~QGraphicsItem()` | 虚析构并删除子图元 | 场景或父图元拥有时，不要重复 `delete` |
| 场景 | `scene() const` | 返回当前所属场景 | 图元尚未加入场景时返回空指针 |
| 层级 | `parentItem() const` | 返回直接图元父项 | 图元坐标的直接参考系 |
| 层级 | `topLevelItem() const` | 返回最顶层图元 | 顶层图元没有图元父项 |
| 层级 | `parentObject() const` | 父项是 `QGraphicsObject` 时返回它 | 否则返回空；不是普通 QObject 父子查询 |
| 层级 | `parentWidget() const` | 父项是 `QGraphicsWidget` 时返回它 | 不会把普通 `QGraphicsItem` 转成 widget |
| 层级 | `topLevelWidget() const` | 返回最顶层 `QGraphicsWidget` | 图元不在 widget 层级下时为空 |
| 层级 | `window() const` | 返回所属顶层图形窗口部件 | 仅适用于 widget 图元树 |
| 面板 | `panel() const` | 返回所属面板项 | 不在 panel 内时为空 |
| 层级 | `setParentItem(QGraphicsItem *parent)` | 设置图元父项 | 改变继承变换与所有权；重设时要考虑坐标是否要保持 |
| 层级 | `childItems() const` | 返回直接子图元列表 | 返回的是列表副本，不要依赖它的排序做长期存储 |
| 类型 | `isWidget() const` | 判断是否为 `QGraphicsWidget` | 只做类型能力判断 |
| 类型 | `isWindow() const` | 判断是否为图形窗口部件 | 与顶层 `QWidget` 概念相近但不是同一对象体系 |
| 类型 | `isPanel() const` | 判断是否设置为面板 | 对应 `ItemIsPanel` |
| 类型 | `toGraphicsObject()` | 尝试转成非 const `QGraphicsObject*` | 失败返回空；需要 QObject 能力时用它 |
| 类型 | `toGraphicsObject() const` | 尝试转成 const `QGraphicsObject*` | 保留 const 性 |
| 分组 | `group() const` | 返回当前所属 `QGraphicsItemGroup` | 仅表示分组关系 |
| 分组 | `setGroup(QGraphicsItemGroup *group)` | 设置所属组 | 更常由 `QGraphicsScene::createItemGroup()` 管理 |
| 标记 | `flags() const` | 返回全部 `GraphicsItemFlags` | 用按位测试判断某个 flag |
| 标记 | `setFlag(GraphicsItemFlag flag, bool enabled = true)` | 开关单个 flag | 不影响未提及的其他 flags |
| 标记 | `setFlags(GraphicsItemFlags flags)` | 一次替换全部 flags | 会清掉未包含的旧 flags |
| 缓存 | `cacheMode() const` | 读取当前缓存模式 | 不是绘制质量设置 |
| 缓存 | `setCacheMode(CacheMode mode, const QSize &cacheSize = QSize())` | 配置绘制缓存和可选缓存大小 | 先验证缓存是否真的减少了绘制成本 |
| 面板 | `panelModality() const` | 读取面板模态级别 | 仅对 panel 场景有意义 |
| 面板 | `setPanelModality(PanelModality panelModality)` | 设置非模态、面板模态或场景模态 | 需要先理解整个 scene 的焦点和输入路径 |
| 面板 | `isBlockedByModalPanel(QGraphicsItem **blockingPanel = nullptr) const` | 判断是否被模态面板阻塞 | 可取回阻塞者；用于高级交互判断 |
| 提示 | `toolTip() const` | 读取悬停提示文本 | Qt 构建启用 tooltip 时可用 |
| 提示 | `setToolTip(const QString &toolTip)` | 设置悬停提示文本 | 空字符串可清除提示 |
| 光标 | `cursor() const` | 读取图元光标 | 取决于 Qt 是否启用 cursor 支持 |
| 光标 | `setCursor(const QCursor &cursor)` | 图元悬停时使用指定光标 | 只影响命中到该图元时的光标 |
| 光标 | `hasCursor() const` | 是否显式设置过光标 | 可区分继承或默认光标 |
| 光标 | `unsetCursor()` | 移除图元自己的光标设置 | 恢复由祖先或视图决定的光标 |
| 可见性 | `isVisible() const` | 本图元是否标记为可见 | 不代表祖先可见后的最终结果 |
| 可见性 | `isVisibleTo(const QGraphicsItem *parent) const` | 到指定祖先路径上是否都可见 | `parent` 必须是祖先或空指针，适合检查继承可见性 |
| 可见性 | `setVisible(bool visible)` | 设置可见状态 | 父项不可见仍会使它最终不可见 |
| 可见性 | `hide()` | `setVisible(false)` 的便利函数 | 内联别名 |
| 可见性 | `show()` | `setVisible(true)` 的便利函数 | 内联别名 |
| 启用 | `isEnabled() const` | 是否可接收普通输入 | 禁用会影响子项和事件分发 |
| 启用 | `setEnabled(bool enabled)` | 设置启用状态 | 不等于可见性 |
| 选择 | `isSelected() const` | 是否处于选中状态 | 必须允许选择或由代码强制设定 |
| 选择 | `setSelected(bool selected)` | 设置选择状态 | 多选规则由场景和交互代码共同决定 |
| 拖放 | `acceptDrops() const` | 是否接收拖放事件 | 未开启时不会进入拖放虚函数 |
| 拖放 | `setAcceptDrops(bool on)` | 开关拖放接收 | 还要在事件中接受合适的 mime 数据 |
| 透明度 | `opacity() const` | 读取本项直接透明度 | 不含父项影响 |
| 透明度 | `effectiveOpacity() const` | 读取考虑祖先 flags 后的有效透明度 | 用它判断最终绘制透明度 |
| 透明度 | `setOpacity(qreal opacity)` | 设置本项透明度 | 一般取 `0.0` 到 `1.0` |
| 效果 | `graphicsEffect() const` | 返回安装的图形效果 | Qt 构建启用 graphic effect 时可用 |
| 效果 | `setGraphicsEffect(QGraphicsEffect *effect)` | 安装或移除图形效果 | 安装后图元接管效果对象；一个效果只能有一个目标 |

### 14.2 输入、焦点、位置与变换

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 鼠标 | `acceptedMouseButtons() const` | 读取接受的鼠标按键集合 | 只影响按键过滤，不等同于接受全部鼠标事件 |
| 鼠标 | `setAcceptedMouseButtons(Qt::MouseButtons buttons)` | 设置接受的鼠标按键 | 设置为 `Qt::NoButton` 可拒绝鼠标按钮事件 |
| 悬停 | `acceptHoverEvents() const` | 是否接受悬停事件 | 不需要按下鼠标 |
| 悬停 | `setAcceptHoverEvents(bool enabled)` | 开关悬停事件 | 开启后才会收到 enter/move/leave |
| 触摸 | `acceptTouchEvents() const` | 是否接受触摸事件 | 触摸与鼠标模拟策略依赖平台 |
| 触摸 | `setAcceptTouchEvents(bool enabled)` | 开关触摸事件 | 需要处理触摸时才打开 |
| 子事件 | `filtersChildEvents() const` | 是否作为子项场景事件过滤者 | 与 `installSceneEventFilter()` 的逐项过滤不同 |
| 子事件 | `setFiltersChildEvents(bool enabled)` | 让本项过滤子项事件 | 适合容器统一截获子项交互 |
| 子事件 | `handlesChildEvents() const` | 是否处理子项事件 | 高级容器行为；一般不需要手动开 |
| 子事件 | `setHandlesChildEvents(bool enabled)` | 设置处理子项事件的行为 | 可能改变事件目标，使用前先设计好传播规则 |
| 激活 | `isActive() const` | 是否属于当前活跃面板 | 多面板场景中的状态，不是焦点状态 |
| 激活 | `setActive(bool active)` | 设置活跃状态 | 通常由 panel 或 scene 焦点管理驱动 |
| 焦点 | `hasFocus() const` | 是否拥有键盘焦点 | 需具备 `ItemIsFocusable` 才能正常取得焦点 |
| 焦点 | `setFocus(Qt::FocusReason reason = Qt::OtherFocusReason)` | 请求键盘焦点 | 传入原因可影响样式和焦点逻辑 |
| 焦点 | `clearFocus()` | 清除本项焦点 | 焦点可能转移到其他合适图元 |
| 焦点 | `focusProxy() const` | 返回焦点代理图元 | 代理把焦点交给另一个 item |
| 焦点 | `setFocusProxy(QGraphicsItem *item)` | 设置焦点代理 | 不要形成代理循环 |
| 焦点 | `focusItem() const` | 返回此焦点域内当前焦点项 | 在非焦点域中语义受祖先范围影响 |
| 焦点 | `focusScopeItem() const` | 返回所属焦点域 | 普通图元常返回相关祖先或空 |
| 抓取 | `grabMouse()` | 强制抓取鼠标 | 被删除、隐藏或禁用时抓取会失效；结束应释放 |
| 抓取 | `ungrabMouse()` | 释放鼠标抓取 | 只释放自己持有的抓取 |
| 抓取 | `grabKeyboard()` | 强制抓取键盘 | 不等于设置焦点，但会截获键盘事件 |
| 抓取 | `ungrabKeyboard()` | 释放键盘抓取 | 与 `grabKeyboard()` 配对 |
| 位置 | `pos() const` | 返回局部原点在父坐标中的位置 | 顶层图元时也是场景坐标 |
| 位置 | `x() const` | 返回 `pos().x()` | 内联便利函数 |
| 位置 | `setX(qreal x)` | 只修改父坐标中的 x | 不改变 y |
| 位置 | `y() const` | 返回 `pos().y()` | 内联便利函数 |
| 位置 | `setY(qreal y)` | 只修改父坐标中的 y | 不改变 x |
| 位置 | `scenePos() const` | 返回局部原点的场景坐标 | 已包含祖先变换 |
| 位置 | `setPos(const QPointF &pos)` | 设置父坐标中的位置 | 位置限制应在 `ItemPositionChange` 返回修正值 |
| 位置 | `setPos(qreal x, qreal y)` | 用两个数设置位置 | `QPointF` 重载的便利形式 |
| 位置 | `moveBy(qreal dx, qreal dy)` | 相对当前位置平移 | 多次调用会累积浮点误差 |
| 视图可见 | `ensureVisible(const QRectF &rect = {}, int xmargin = 50, int ymargin = 50)` | 让图元局部矩形在 view 中可见 | 有多个 view 时，各 view 的结果取决于其策略 |
| 视图可见 | `ensureVisible(qreal x, qreal y, qreal w, qreal h, int xmargin = 50, int ymargin = 50)` | 数值版确保局部矩形可见 | 内联转发给 `QRectF` 版本 |
| 变换 | `transform() const` | 读取本项局部 `QTransform` | 不含祖先变换 |
| 变换 | `sceneTransform() const` | 读取到场景的合成变换 | 包含祖先变换 |
| 变换 | `deviceTransform(const QTransform &viewportTransform) const` | 计算到设备的合成变换 | 对 `ItemIgnoresTransformations` 图元尤其重要 |
| 变换 | `itemTransform(const QGraphicsItem *other, bool *ok = nullptr) const` | 求本项到另一个图元坐标的变换 | 无公共祖先或不可逆时通过 `ok` 判断 |
| 变换 | `setTransform(const QTransform &matrix, bool combine = false)` | 设置或组合本项矩阵 | `combine=true` 是在现有矩阵基础上组合 |
| 变换 | `resetTransform()` | 重置本项矩阵 | 不会重置 `rotation()`、`scale()` 等独立属性 |
| 变换 | `setRotation(qreal angle)` | 设置围绕变换原点的旋转角度 | 单位是度 |
| 变换 | `rotation() const` | 读取旋转角度 | 角度不必限制在 `0..360` |
| 变换 | `setScale(qreal scale)` | 设置围绕变换原点的缩放 | `0` 或负值会带来退化或翻转语义，应谨慎 |
| 变换 | `scale() const` | 读取缩放因子 | 不包含矩阵中可能已有的缩放 |
| 变换 | `transformations() const` | 读取 `QGraphicsTransform` 列表 | 返回列表副本 |
| 变换 | `setTransformations(const QList<QGraphicsTransform *> &list)` | 设置复合变换对象链 | 图元接管列表中变换对象的所有权 |
| 变换 | `transformOriginPoint() const` | 读取变换原点的局部坐标 | 不是场景坐标 |
| 变换 | `setTransformOriginPoint(const QPointF &origin)` | 设置变换原点 | 影响旋转和缩放 |
| 变换 | `setTransformOriginPoint(qreal x, qreal y)` | 数值版设置变换原点 | 内联转发给 `QPointF` 版本 |
| 动画 | `advance(int phase)` | 接收场景两阶段 advance 调用 | `phase=0` 用于准备，`phase=1` 再推进状态 |
| 堆叠 | `zValue() const` | 读取 z 层级 | 值高的一般在前；父子和 flags 也会影响最终顺序 |
| 堆叠 | `setZValue(qreal z)` | 设置 z 层级 | 不要用极端 z 值代替清晰的层级设计 |
| 堆叠 | `stackBefore(const QGraphicsItem *sibling)` | 在同父且同 z 条件下排到兄弟项前 | `sibling` 必须是可比较的兄弟项 |

### 14.3 几何、命中、绘制与数据

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 几何 | `boundingRect() const` | 返回局部绘制外接矩形 | 纯虚函数；变化前必须 `prepareGeometryChange()` |
| 几何 | `childrenBoundingRect() const` | 返回所有子项在本项坐标中的合并边界 | 不含本项自己的 `boundingRect()` |
| 几何 | `sceneBoundingRect() const` | 返回本项在场景中的轴对齐外接矩形 | 旋转后是外接矩形，不是精确四边形 |
| 命中 | `shape() const` | 返回局部精确形状 | 默认基于边界；复杂图元可重写 |
| 裁剪 | `isClipped() const` | 是否受到祖先形状裁剪 | 检查 `ItemClipsToShape` 等综合结果 |
| 裁剪 | `clipPath() const` | 返回当前有效裁剪路径 | 可能因祖先变换而较复杂 |
| 命中 | `contains(const QPointF &point) const` | 判断局部点是否在图元内 | 点必须先映射到本项局部坐标 |
| 碰撞 | `collidesWithItem(const QGraphicsItem *other, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const` | 判断与另一图元是否碰撞 | `mode` 决定按 shape 还是 bounding rect 判断 |
| 碰撞 | `collidesWithPath(const QPainterPath &path, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const` | 判断与局部路径是否碰撞 | `path` 使用本图元局部坐标 |
| 碰撞 | `collidingItems(Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const` | 返回发生碰撞的场景图元 | 大量调用可能昂贵 |
| 遮挡 | `isObscured(const QRectF &rect = {}) const` | 判断本项局部区域是否被完全遮挡 | 空矩形表示考察整个图元 |
| 遮挡 | `isObscured(qreal x, qreal y, qreal w, qreal h) const` | 数值版遮挡判断 | 内联转发给矩形版本 |
| 遮挡 | `isObscuredBy(const QGraphicsItem *item) const` | 判断是否被指定图元遮挡 | 可为特殊不透明图元重写 |
| 遮挡 | `opaqueArea() const` | 返回保证不透明的局部区域 | 返回过大将导致错误的优化判断 |
| 绘制优化 | `boundingRegion(const QTransform &itemToDeviceTransform) const` | 把边界转成设备区域 | 用于绘制或索引优化，不是常规业务 API |
| 绘制优化 | `boundingRegionGranularity() const` | 读取边界区域颗粒度 | 值影响优化精度和计算量 |
| 绘制优化 | `setBoundingRegionGranularity(qreal granularity)` | 设置边界区域颗粒度 | 只在确实测得收益时调整 |
| 绘制 | `paint(QPainter *, const QStyleOptionGraphicsItem *, QWidget * = nullptr)` | 在局部坐标绘制图元 | 纯虚函数；不要修改几何或长期改变外部 painter 状态 |
| 绘制 | `update(const QRectF &rect = {})` | 标记局部区域待重绘 | 异步调度，不会立即画 |
| 绘制 | `update(qreal x, qreal y, qreal width, qreal height)` | 数值版标记重绘 | 内联转发给矩形版本 |
| 绘制 | `scroll(qreal dx, qreal dy, const QRectF &rect = {})` | 在缓存中滚动局部内容 | 适用于可复用缓存的大图元 |
| 层级 | `isAncestorOf(const QGraphicsItem *child) const` | 判断是否为 `child` 的祖先 | 不包含自身 |
| 层级 | `commonAncestorItem(const QGraphicsItem *other) const` | 返回最近公共图元祖先 | 无公共祖先时返回空 |
| 鼠标 | `isUnderMouse() const` | 判断鼠标是否正位于图元上 | 受可见性、shape、事件目标等影响 |
| 数据 | `data(int key) const` | 读取自定义 `QVariant` 数据 | 未设置的 key 返回无效 QVariant |
| 数据 | `setData(int key, const QVariant &value)` | 写入自定义数据 | 约定 key 的归属，避免模块冲突 |
| 输入法 | `inputMethodHints() const` | 读取输入法提示 | 通常仅可编辑图元需要 |
| 输入法 | `setInputMethodHints(Qt::InputMethodHints hints)` | 设置输入法提示 | 与 `ItemAcceptsInputMethod` 配合 |
| 类型 | `type() const` | 返回运行时图元类型号 | 自定义类重写并返回唯一 `UserType + n` |
| 场景过滤 | `installSceneEventFilter(QGraphicsItem *filterItem)` | 让另一图元过滤本项场景事件 | 过滤项和被过滤项应在同一场景生命周期内 |
| 场景过滤 | `removeSceneEventFilter(QGraphicsItem *filterItem)` | 移除指定场景事件过滤项 | 销毁前解除复杂关系可让逻辑更清楚 |

### 14.4 坐标映射 API

`mapTo...` 的意思是“把**本图元局部坐标**送到目标坐标”；`mapFrom...` 则是“把目标坐标取回到**本图元局部坐标**”。`item` 参数为 `nullptr` 时，不应把它当成任意坐标系；请传入明确对象或使用 `Parent` / `Scene` 专用 API。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 点映射 | `mapToItem(const QGraphicsItem *item, const QPointF &point)` | 本项局部点映射到另一图元局部坐标 | 两项应在可建立变换关系的图元树或场景中 |
| 点映射 | `mapToParent(const QPointF &point)` | 本项局部点映射到父坐标 | 顶层项的父坐标等同场景坐标 |
| 点映射 | `mapToScene(const QPointF &point)` | 本项局部点映射到场景 | 计算连接线端点的常用 API |
| 矩形映射 | `mapToItem(const QGraphicsItem *item, const QRectF &rect)` | 本项局部矩形映射到另一图元 | 返回 `QPolygonF` 保留旋转后的四角 |
| 矩形映射 | `mapToParent(const QRectF &rect)` | 本项矩形映射到父坐标 | 返回多边形而非矩形 |
| 矩形映射 | `mapToScene(const QRectF &rect)` | 本项矩形映射到场景 | 适合精确框选轮廓 |
| 外接矩形 | `mapRectToItem(const QGraphicsItem *item, const QRectF &rect)` | 映射矩形并返回轴对齐外接矩形 | 变换后通常比真实区域大 |
| 外接矩形 | `mapRectToParent(const QRectF &rect)` | 映射到父坐标的外接矩形 | 只适合粗略范围 |
| 外接矩形 | `mapRectToScene(const QRectF &rect)` | 映射到场景的外接矩形 | 不保留旋转信息 |
| 多边形映射 | `mapToItem(const QGraphicsItem *item, const QPolygonF &polygon)` | 本项多边形映射到另一图元 | 保留每个顶点 |
| 多边形映射 | `mapToParent(const QPolygonF &polygon)` | 多边形映射到父坐标 | 用于准确轮廓 |
| 多边形映射 | `mapToScene(const QPolygonF &polygon)` | 多边形映射到场景 | 常用于选择区域 |
| 路径映射 | `mapToItem(const QGraphicsItem *item, const QPainterPath &path)` | 本项路径映射到另一图元 | 复杂路径映射有成本 |
| 路径映射 | `mapToParent(const QPainterPath &path)` | 路径映射到父坐标 | 保留曲线语义 |
| 路径映射 | `mapToScene(const QPainterPath &path)` | 路径映射到场景 | 精确碰撞或覆盖判断可用 |
| 点映射 | `mapFromItem(const QGraphicsItem *item, const QPointF &point)` | 另一图元局部点映射到本项 | 是 `mapToItem` 的反方向 |
| 点映射 | `mapFromParent(const QPointF &point)` | 父坐标点映射到本项 | 处理父项局部输入时使用 |
| 点映射 | `mapFromScene(const QPointF &point)` | 场景点映射到本项 | 将鼠标 `scenePos()` 转为局部点 |
| 矩形映射 | `mapFromItem(const QGraphicsItem *item, const QRectF &rect)` | 另一项矩形映射到本项 | 返回 `QPolygonF` |
| 矩形映射 | `mapFromParent(const QRectF &rect)` | 父坐标矩形映射到本项 | 旋转后仍是多边形 |
| 矩形映射 | `mapFromScene(const QRectF &rect)` | 场景矩形映射到本项 | 适合本项局部精确判定 |
| 外接矩形 | `mapRectFromItem(const QGraphicsItem *item, const QRectF &rect)` | 另一项矩形映射到本项外接矩形 | 返回值会丢失旋转信息 |
| 外接矩形 | `mapRectFromParent(const QRectF &rect)` | 父矩形映射到本项外接矩形 | 用于粗略区域 |
| 外接矩形 | `mapRectFromScene(const QRectF &rect)` | 场景矩形映射到本项外接矩形 | 不适合精确命中 |
| 多边形映射 | `mapFromItem(const QGraphicsItem *item, const QPolygonF &polygon)` | 另一项多边形映射到本项 | 保留顶点 |
| 多边形映射 | `mapFromParent(const QPolygonF &polygon)` | 父多边形映射到本项 | 保留顶点 |
| 多边形映射 | `mapFromScene(const QPolygonF &polygon)` | 场景多边形映射到本项 | 保留顶点 |
| 路径映射 | `mapFromItem(const QGraphicsItem *item, const QPainterPath &path)` | 另一项路径映射到本项 | 适合 shape 的跨项比较 |
| 路径映射 | `mapFromParent(const QPainterPath &path)` | 父路径映射到本项 | 保留曲线语义 |
| 路径映射 | `mapFromScene(const QPainterPath &path)` | 场景路径映射到本项 | 保留曲线语义 |
| 数值点映射 | `mapToItem(item, qreal x, qreal y)` | 数值版本项点到另一项 | 等价于传 `QPointF(x, y)` |
| 数值点映射 | `mapToParent(qreal x, qreal y)` | 数值版本项点到父项 | 等价于传 `QPointF` |
| 数值点映射 | `mapToScene(qreal x, qreal y)` | 数值版本项点到场景 | 等价于传 `QPointF` |
| 数值矩形映射 | `mapToItem(item, qreal x, qreal y, qreal w, qreal h)` | 数值版本项矩形到另一项 | 返回 `QPolygonF` |
| 数值矩形映射 | `mapToParent(qreal x, qreal y, qreal w, qreal h)` | 数值版本项矩形到父项 | 返回 `QPolygonF` |
| 数值矩形映射 | `mapToScene(qreal x, qreal y, qreal w, qreal h)` | 数值版本项矩形到场景 | 返回 `QPolygonF` |
| 数值外接矩形 | `mapRectToItem(item, qreal x, qreal y, qreal w, qreal h)` | 数值版矩形到另一项的外接矩形 | 等价于传 `QRectF` |
| 数值外接矩形 | `mapRectToParent(qreal x, qreal y, qreal w, qreal h)` | 数值版矩形到父项的外接矩形 | 等价于传 `QRectF` |
| 数值外接矩形 | `mapRectToScene(qreal x, qreal y, qreal w, qreal h)` | 数值版矩形到场景的外接矩形 | 等价于传 `QRectF` |
| 数值点映射 | `mapFromItem(item, qreal x, qreal y)` | 数值版另一项点到本项 | 等价于传 `QPointF` |
| 数值点映射 | `mapFromParent(qreal x, qreal y)` | 数值版父点到本项 | 等价于传 `QPointF` |
| 数值点映射 | `mapFromScene(qreal x, qreal y)` | 数值版场景点到本项 | 等价于传 `QPointF` |
| 数值矩形映射 | `mapFromItem(item, qreal x, qreal y, qreal w, qreal h)` | 数值版另一项矩形到本项 | 返回 `QPolygonF` |
| 数值矩形映射 | `mapFromParent(qreal x, qreal y, qreal w, qreal h)` | 数值版父矩形到本项 | 返回 `QPolygonF` |
| 数值矩形映射 | `mapFromScene(qreal x, qreal y, qreal w, qreal h)` | 数值版场景矩形到本项 | 返回 `QPolygonF` |
| 数值外接矩形 | `mapRectFromItem(item, qreal x, qreal y, qreal w, qreal h)` | 数值版另一项矩形到本项外接矩形 | 等价于传 `QRectF` |
| 数值外接矩形 | `mapRectFromParent(qreal x, qreal y, qreal w, qreal h)` | 数值版父矩形到本项外接矩形 | 等价于传 `QRectF` |
| 数值外接矩形 | `mapRectFromScene(qreal x, qreal y, qreal w, qreal h)` | 数值版场景矩形到本项外接矩形 | 等价于传 `QRectF` |

### 14.5 受保护扩展点

这些函数不是在外部“调用图元功能”的入口，而是派生类接入框架生命周期的地方。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 输入法 | `updateMicroFocus()` | 通知输入法微焦点区域发生变化 | 改变光标或文本编辑位置后使用；`QGraphicsObject` 也暴露槽版本 |
| 场景事件 | `sceneEventFilter(QGraphicsItem *watched, QEvent *event)` | 处理被过滤图元的场景事件 | 由 `installSceneEventFilter()` 建立关系 |
| 场景事件 | `sceneEvent(QEvent *event)` | 所有场景事件的总分发入口 | 优先重写更具体的事件函数 |
| 菜单 | `contextMenuEvent(QGraphicsSceneContextMenuEvent *event)` | 处理上下文菜单事件 | 按需要接受或忽略事件 |
| 拖放 | `dragEnterEvent(QGraphicsSceneDragDropEvent *event)` | 拖入边界时触发 | 检查 mime 数据后接受合适动作 |
| 拖放 | `dragLeaveEvent(QGraphicsSceneDragDropEvent *event)` | 拖离边界时触发 | 清理拖放高亮 |
| 拖放 | `dragMoveEvent(QGraphicsSceneDragDropEvent *event)` | 在图元上拖动时触发 | 可按局部位置显示插入提示 |
| 拖放 | `dropEvent(QGraphicsSceneDragDropEvent *event)` | 放下数据时触发 | 仅接受已验证的数据和动作 |
| 焦点 | `focusInEvent(QFocusEvent *event)` | 获得焦点时触发 | 更新外观后通常调用基类保留默认处理 |
| 焦点 | `focusOutEvent(QFocusEvent *event)` | 失去焦点时触发 | 提交或取消临时编辑状态 |
| 悬停 | `hoverEnterEvent(QGraphicsSceneHoverEvent *event)` | 鼠标进入时触发 | 须先 `setAcceptHoverEvents(true)` |
| 悬停 | `hoverMoveEvent(QGraphicsSceneHoverEvent *event)` | 鼠标悬停移动时触发 | 使用 `event->pos()` 获得局部位置 |
| 悬停 | `hoverLeaveEvent(QGraphicsSceneHoverEvent *event)` | 鼠标离开时触发 | 适合清理 hover 状态 |
| 键盘 | `keyPressEvent(QKeyEvent *event)` | 按键按下时触发 | 通常需要图元拥有焦点 |
| 键盘 | `keyReleaseEvent(QKeyEvent *event)` | 按键释放时触发 | 不要只处理按下而遗忘状态恢复 |
| 鼠标 | `mousePressEvent(QGraphicsSceneMouseEvent *event)` | 鼠标按下时触发 | 若保留默认移动或选择，调用基类 |
| 鼠标 | `mouseMoveEvent(QGraphicsSceneMouseEvent *event)` | 鼠标移动时触发 | 拖动时注意 `pos()` 与 `scenePos()` 的区别 |
| 鼠标 | `mouseReleaseEvent(QGraphicsSceneMouseEvent *event)` | 鼠标释放时触发 | 成对结束内部拖动状态 |
| 鼠标 | `mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event)` | 双击时触发 | 可打开编辑器；注意基类默认行为是否需要保留 |
| 滚轮 | `wheelEvent(QGraphicsSceneWheelEvent *event)` | 滚轮事件 | 不接受时可让 view 或祖先继续处理 |
| 输入法 | `inputMethodEvent(QInputMethodEvent *event)` | 收到输入法提交或预编辑文本 | 需启用 `ItemAcceptsInputMethod` |
| 输入法 | `inputMethodQuery(Qt::InputMethodQuery query) const` | 回答输入法对光标、周围文本等查询 | 可编辑图元应准确返回局部几何 |
| 变化通知 | `itemChange(GraphicsItemChange change, const QVariant &value)` | 在状态改变前后拦截或观察 | 位置通知须开启 `ItemSendsGeometryChanges`；前置回调直接返回新值 |
| 扩展 | `supportsExtension(Extension extension) const` | 声明是否支持扩展协议 | Qt 内部或特定派生类扩展点；业务代码很少需要 |
| 扩展 | `setExtension(Extension extension, const QVariant &value)` | 写入扩展值 | 与 `supportsExtension()` 配套 |
| 扩展 | `extension(const QVariant &variant) const` | 读取扩展结果 | 参数是扩展查询载体，遵循对应协议 |
| 几何通知 | `prepareGeometryChange()` | 在改变边界相关几何前通知场景 | 必须在修改前调用；不可用它替代 `update()` |
| 索引 | `addToIndex()` | 把图元加入场景索引 | 框架内部辅助入口，普通派生类不应调用 |
| 索引 | `removeFromIndex()` | 从场景索引移除图元 | 框架内部辅助入口，普通派生类不应调用 |
| 派生构造 | `QGraphicsItem(QGraphicsItemPrivate &dd, QGraphicsItem *parent)` | 供 Qt 内部派生类传入私有实现 | 普通自定义图元使用公开构造函数 |

### 14.6 非成员工具与枚举

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型转换 | `qgraphicsitem_cast<T>(QGraphicsItem *item)` | 通过 `item->type()` 尝试转为 `T` | `T` 应为图元指针类型，且目标类要有唯一 `Type` |
| 类型转换 | `qgraphicsitem_cast<T>(const QGraphicsItem *item)` | const 版本的安全类型转换 | 返回 const 指针，不能借此绕过 const |
| 类型常量 | `QGraphicsItem::Type` | 基类的类型号，值为 `1` | 基类转换时使用 |
| 类型常量 | `QGraphicsItem::UserType` | 用户自定义类型号起点，值为 `65536` | 每个自定义图元分配不同的 `UserType + n` |
| 缓存枚举 | `NoCache` | 不缓存绘制 | 内容频繁变化时的默认选择 |
| 缓存枚举 | `ItemCoordinateCache` | 使用图元坐标缓存 | 适合复杂、相对稳定的局部内容 |
| 缓存枚举 | `DeviceCoordinateCache` | 使用设备坐标缓存 | 适合主要平移、视图变换稳定的图元 |
| 面板枚举 | `NonModal` | 面板不阻塞其他面板 | 默认的非模态行为 |
| 面板枚举 | `PanelModal` | 阻塞同一面板层级中的其他面板 | 高级面板 UI |
| 面板枚举 | `SceneModal` | 阻塞整个场景的其他面板 | 使用时要提供明确的关闭路径 |
| 扩展枚举 | `UserExtension` | 用户扩展编号起点 | 仅在实现扩展协议时使用 |

## 15. 学习顺序建议

第一次写自定义图元时，先只掌握 `boundingRect()`、`paint()`、`setPos()`、`setFlags()`、`shape()` 和 `prepareGeometryChange()`。它们已经覆盖了可绘制、可拖动、可选择、可命中的绝大多数节点需求。

第二阶段再引入父子项、`mapToScene()` / `mapFromScene()` 和 `itemChange()`，解决连接线跟随、嵌套容器和位置约束。缓存、面板、输入法、事件过滤器属于更专门的工具，遇到明确场景再使用，代码会更容易保持清醒。
