# QGraphicsObject

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsObject`

## 1. 先建立直觉

`QGraphicsObject` 是“带 QObject 能力的 QGraphicsItem”。普通 `QGraphicsItem` 轻量但没有信号槽、属性系统和对象树；`QGraphicsObject` 把这些能力带进 Graphics View。

当你的图元需要信号、槽、`Q_PROPERTY`、动画、对象名、事件过滤或和 Qt 元对象系统协作时，用它比直接继承 `QGraphicsItem` 更合适。

## 2. 类说明

`QGraphicsObject` 同时继承 `QObject` 和 `QGraphicsItem`，但父子关系要分清：QObject parent 和 graphics parent 不是同一套概念。构造函数参数是 `QGraphicsItem *parent`，用于图元层级；QObject 生命周期仍按 Qt 的实现规则处理。

它本身仍然是抽象图元，子类还要实现 `boundingRect()` 和 `paint()`。它额外把位置、旋转、缩放、透明度、可见性等暴露成属性，并提供对应变化信号，便于动画和绑定式更新。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsObject(QGraphicsItem *parent)` | 创建带元对象能力的图元。 |
| `grabGesture(Qt::GestureType, Qt::GestureFlags)` | 让图元订阅手势事件。 |
| `ungrabGesture(Qt::GestureType)` | 取消订阅某类手势。 |
| `pos/x/y/z` 属性 | 暴露位置和层级，便于动画或属性系统访问。 |
| `rotation` / `scale` 属性 | 暴露变换属性。 |
| `opacity` 属性 | 暴露透明度属性。 |
| `visible` / `enabled` 属性 | 暴露可见和启用状态。 |
| `parent` 属性 | 表示 graphics parent object。 |
| `effect` 属性 | 绑定 `QGraphicsEffect`。 |
| `xChanged/yChanged/zChanged` | 坐标变化信号。 |
| `rotationChanged/scaleChanged` | 变换变化信号。 |
| `opacityChanged/visibleChanged/enabledChanged` | 显示状态变化信号。 |
| `parentChanged` | graphics parent object 变化时发出。 |

## 4. 关键用法

可动画的自定义 item：

```cpp
class BadgeItem : public QGraphicsObject {
    Q_OBJECT
public:
    QRectF boundingRect() const override { return QRectF(-20, -20, 40, 40); }

    void paint(QPainter *p, const QStyleOptionGraphicsItem *, QWidget *) override
    {
        p->setBrush(Qt::red);
        p->drawEllipse(boundingRect());
    }
};
```

属性动画：

```cpp
auto *anim = new QPropertyAnimation(item, "opacity", item);
anim->setStartValue(0.0);
anim->setEndValue(1.0);
anim->start(QAbstractAnimation::DeleteWhenStopped);
```

## 5. 使用场景

适合节点编辑器中会发信号的节点、可动画标记、带属性面板绑定的图形对象、需要手势的场景对象、需要和状态机或动画框架配合的图元。

如果 item 数量极大且不需要元对象能力，直接继承 `QGraphicsItem` 更轻。`QGraphicsObject` 的便利性有成本。

## 6. 常见坑与经验

不要混淆 QObject parent 和 graphics parent。删除、坐标继承、显示层级、事件传播主要看 graphics parent；信号槽对象树是另一条线。

有了属性信号不代表自动重绘。改变影响绘制的自定义数据时仍然要 `update()`，改变几何边界仍然要 `prepareGeometryChange()`。

如果只是想让 item 可点击，不需要 `QGraphicsObject`；普通 item 重写 mouse 事件即可。需要信号时再升级。
