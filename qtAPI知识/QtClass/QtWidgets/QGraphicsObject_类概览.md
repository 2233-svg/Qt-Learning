<!-- 依据 Qt 6.11.1 头文件 qgraphicsitem.h 整理。 -->

# QGraphicsObject 深入笔记

> 头文件：`#include <QGraphicsObject>`  
> 模块：`Qt6::Widgets`  
> 多重继承：`QObject + QGraphicsItem -> QGraphicsObject`  
> 性质：抽象图元基类

## 1. 它解决什么问题

`QGraphicsObject` 将 `QGraphicsItem` 的场景图元能力和 `QObject` 的信号槽、元对象、属性动画能力放到同一个基类中。

单独继承 `QGraphicsItem` 可以实现绘制和事件，但没有 `Q_PROPERTY`、通知信号和 `QPropertyAnimation` 的直接支持。需要让一个自绘节点、可拖动卡片、流程图元素既能画在 scene 中，又能对 `pos`、`opacity`、`rotation` 等状态做属性动画时，通常从 `QGraphicsObject` 派生。

```text
QGraphicsItem
  ├─ 场景坐标、绘制、命中测试、父子图元、变换
QObject
  ├─ 信号槽、元对象、动态属性、对象生命周期辅助
  └─ QGraphicsObject
       └─ 你的可动画自绘图元
```

它仍是抽象类：`QGraphicsItem` 的 `boundingRect()` 和 `paint()` 仍须由具体子类实现。

## 2. 最小自定义图元

```cpp
#include <QGraphicsObject>
#include <QPainter>

class StatusNode final : public QGraphicsObject
{
public:
    QRectF boundingRect() const override
    {
        return QRectF(0, 0, 120, 48);
    }

    void paint(QPainter *painter,
               const QStyleOptionGraphicsItem *,
               QWidget *) override
    {
        painter->setBrush(QColor("#d8f0e2"));
        painter->setPen(Qt::NoPen);
        painter->drawRoundedRect(boundingRect(), 6, 6);
    }
};
```

加入场景并动画化：

```cpp
auto *node = new StatusNode;
scene->addItem(node);

auto *animation = new QPropertyAnimation(node, "pos", node);
animation->setStartValue(QPointF(0, 0));
animation->setEndValue(QPointF(240, 0));
animation->setDuration(220);
animation->start(QAbstractAnimation::DeleteWhenStopped);
```

这里不必为 `pos` 自己写 getter、setter 和通知信号；`QGraphicsObject` 已把 `QGraphicsItem` 的位置暴露为 Qt 属性。

## 3. 两套父子关系：最重要的边界

`QGraphicsObject` 同时拥有 QObject 和图元身份，但图元层级应始终使用 `QGraphicsItem` API：

```cpp
child->setParentItem(parent);
QGraphicsItem *parentItem = child->parentItem();
const auto children = parent->childItems();
```

不要用 `QObject::setParent()` 构建 scene 图元层级。`QObject` 父子关系不负责坐标继承、Z 值层叠、可见性传播、scene 归属与绘制变换；这些都属于 `QGraphicsItem` 父子树。

`parent` 属性和 `parentChanged()` 反映的是图元父项的变化。传给 `QGraphicsObject` 构造函数的也是 `QGraphicsItem *parent`，不是 `QObject *parent`。

销毁策略也优先遵守图元树：删除父 `QGraphicsItem` 会删除其子图元。用 `QObject` 连接 lambda 时，仍可把 `QGraphicsObject` 作为 connection context，让连接在对象销毁时自动断开；但不要因此混淆两种树。

## 4. 可动画的图元状态

`QGraphicsObject` 提供以下常用属性，适合直接交给 `QPropertyAnimation`：

| 属性 | 改变什么 | 常见用途 |
| --- | --- | --- |
| `pos` / `x` / `y` | 相对父图元的位置。 | 拖动、平移、吸附动画。 |
| `z` | 同级图元的堆叠顺序。 | 选中项置顶、浮层前景。 |
| `rotation` | 围绕变换原点旋转。 | 指针、卡片翻转前的平面旋转。 |
| `scale` | 围绕变换原点等比缩放。 | 悬停放大、选中反馈。 |
| `transformOriginPoint` | 旋转和缩放的本地中心。 | 从图元中心或边缘开始变换。 |
| `opacity` | 整体绘制透明度。 | 淡入淡出、禁用感。 |
| `visible` | 是否绘制并参与正常可见性传播。 | 临时显示/隐藏。 |
| `enabled` | 是否接收正常输入事件。 | 禁用交互但保留画面。 |

`pos` 使用父图元坐标系；`x`、`y` 是它的两个分量。`z` 不是坐标轴位移，而是堆叠排序值。`opacity` 影响画面透明度，不等于 `visible=false`；隐藏后不绘制，禁用后仍可绘制但不应继续接受常规交互。

## 5. 变换原点与信号

`rotation` 与 `scale` 以 `transformOriginPoint` 为中心。默认原点通常是本地 `(0, 0)`，因此没有设置原点时，图元可能像从左上角旋转或缩放：

```cpp
node->setTransformOriginPoint(node->boundingRect().center());
node->setRotation(12.0);
node->setScale(1.05);
```

下列信号适合连接检查器、动画状态同步或模型回写：

- `xChanged()`、`yChanged()`、`zChanged()`：位置分量或堆叠值改变。
- `rotationChanged()`、`scaleChanged()`：平面变换参数改变。
- `opacityChanged()`：透明度改变。
- `visibleChanged()`、`enabledChanged()`：可见性、交互状态改变。
- `parentChanged()`：图元父项改变。

`pos` 属性没有单独的 `posChanged()` 信号；监听位置变化时组合连接 `xChanged()` 和 `yChanged()`。

## 6. 效果与手势

### `effect`

`effect` 对应 `QGraphicsItem::setGraphicsEffect()`。图元装入 `QGraphicsEffect` 后，效果对象由图元接管，一个图元同一时间只能有一个效果：

```cpp
auto *shadow = new QGraphicsDropShadowEffect;
node->setGraphicsEffect(shadow);
```

阴影、模糊、透明度效果都会增加绘制成本，特别是大面积 item 或连续动画。需要组合多个效果时，拆分父子图元层级或实现自定义 `QGraphicsEffect`，不要期待重复调用 `setGraphicsEffect()` 自动叠加。

### `grabGesture()` / `ungrabGesture()`

```cpp
node->grabGesture(Qt::TapGesture);
node->grabGesture(Qt::PanGesture);
```

调用后，手势识别器可将结果作为 `QGestureEvent` 分派给该对象。应在图元事件处理中检查并接受所需手势；不再需要时用 `ungrabGesture()` 解除。手势状态只在 GUI 线程的事件分派期间有效，不能保存 `QGesture *` 后跨事件循环长期使用。

## 7. 框架扩展点

- `event(QEvent *)`：`QObject` 事件分发入口。通常重写具体的 Graphics View 事件处理函数；只有需要统一拦截 Qt 事件时才重写它，并应保留基类处理。
- `updateMicroFocus()`：受保护槽，用于通知输入法更新微焦点区域。文本输入型图元、`QGraphicsWidget` 子类才可能涉及；普通图形节点不应手动调用。
- 受保护构造 `QGraphicsObject(QGraphicsItemPrivate &, QGraphicsItem *)`：Qt 私有实现路径，普通应用不使用。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit QGraphicsObject(QGraphicsItem *parent = nullptr)` | 构造可动画的图元基类，并设置图元父项。 | 抽象类；父参数属于 `QGraphicsItem` 树，不是 QObject 父对象。 |
| 析构 | `~QGraphicsObject()` | 销毁图元对象。 | 父图元销毁会删除子图元；避免与其它所有权模型重复删除。 |
| 属性 | `parent : QGraphicsObject *` | 表示图元父对象。 | 用 `setParentItem()` 管理，不能用 `QObject::setParent()` 替代。 |
| 属性 | `pos : QPointF` | 表示相对父图元的位置。 | 没有 `posChanged()`；监听位置用 `xChanged()` 和 `yChanged()`。 |
| 属性 | `x : qreal` | `pos` 的 X 分量。 | 使用父图元坐标系。 |
| 属性 | `y : qreal` | `pos` 的 Y 分量。 | 使用父图元坐标系。 |
| 属性 | `z : qreal` | 表示同级图元的堆叠顺序。 | 不是空间坐标位移；值高通常更靠前绘制。 |
| 属性 | `rotation : qreal` | 表示平面旋转角度。 | 围绕 `transformOriginPoint` 旋转。 |
| 属性 | `scale : qreal` | 表示等比缩放倍率。 | 围绕变换原点；负值会镜像。 |
| 属性 | `transformOriginPoint : QPointF` | 表示旋转、缩放的本地原点。 | 常设为 `boundingRect().center()`。 |
| 属性 | `opacity : qreal` | 表示整体绘制透明度。 | 淡出不等于隐藏，仍可能参与事件和布局。 |
| 属性 | `visible : bool` | 表示图元是否可见。 | 隐藏会影响绘制与可见性传播。 |
| 属性 | `enabled : bool` | 表示图元是否启用交互。 | 禁用通常仍可绘制，但不应接收常规输入。 |
| 属性 | `effect : QGraphicsEffect *` | 表示附加的图形效果。 | 图元接管效果所有权；同一时间仅能安装一个。 |
| 手势 | `void grabGesture(Qt::GestureType type, Qt::GestureFlags flags = {})` | 请求识别并向本图元分派指定手势。 | 还需在事件处理中接收手势；只在 GUI 线程使用。 |
| 手势 | `void ungrabGesture(Qt::GestureType type)` | 取消对指定手势的请求。 | 移除交互模式或对象销毁前无需额外重复调用。 |
| 信号 | `void parentChanged()` | 通知图元父项变化。 | 用于同步与父图元相关的业务状态。 |
| 信号 | `void opacityChanged()` | 通知透明度改变。 | 属性动画过程中会高频发射。 |
| 信号 | `void visibleChanged()` | 通知可见性改变。 | 不能替代场景进入/离开的生命周期通知。 |
| 信号 | `void enabledChanged()` | 通知启用状态改变。 | 适合同步外部操作控件。 |
| 信号 | `void xChanged()` | 通知 X 位置改变。 | 与 `yChanged()` 组合观察 `pos`。 |
| 信号 | `void yChanged()` | 通知 Y 位置改变。 | 与 `xChanged()` 组合观察 `pos`。 |
| 信号 | `void zChanged()` | 通知堆叠值改变。 | 改变的是绘制顺序，不是位置。 |
| 信号 | `void rotationChanged()` | 通知旋转角改变。 | 与 transform origin 一起检查视觉结果。 |
| 信号 | `void scaleChanged()` | 通知缩放倍率改变。 | 注意对命中区域、子图元坐标的影响。 |
| 受保护事件 | `bool event(QEvent *ev)` | Qt 事件分发入口。 | 普通场景交互优先重写具体图元事件函数。 |
| 受保护槽 | `void updateMicroFocus()` | 通知输入法更新微焦点。 | 面向文本输入图元；普通图元无需调用。 |
| 受保护构造 | `QGraphicsObject(QGraphicsItemPrivate &, QGraphicsItem *)` | Qt 内部私有实现构造入口。 | 私有参数类型，不属于应用层 API。 |

## 9. 排查清单

1. 图元动画不动：确认目标是 `QGraphicsObject` 派生类、属性名正确，且动画事件循环正在运行。
2. 旋转像绕角落发生：为 `transformOriginPoint` 设置 `boundingRect().center()`。
3. 子图元没有随父图元一起移动：检查是否用了 `setParentItem()`，而不是 `QObject::setParent()`。
4. 设置了阴影却消失：确认图元未被后续 `setGraphicsEffect()` 替换，且效果对象没有被手动删除。
5. 监听不到 `pos`：连接 `xChanged()` 和 `yChanged()`，或在 `itemChange()` 中统一处理。

### 一句话总结

`QGraphicsObject` 是“带 QObject 能力的场景图元”基类：用它实现可绘制、可交互、可发信号、可做属性动画的自定义 item；关键边界是图元树不等于 QObject 树，位置/变换属性不等于绘制边界，效果对象由图元独占管理。
