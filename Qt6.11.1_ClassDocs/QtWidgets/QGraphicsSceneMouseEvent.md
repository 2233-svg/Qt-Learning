# QGraphicsSceneMouseEvent

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsSceneMouseEvent`

## 1. 先建立直觉

`QGraphicsSceneMouseEvent` 是 Graphics View 中传给 item 的鼠标事件。它描述鼠标在 item、scene、screen 三套坐标中的位置，以及按钮、修饰键、按下起点和上一次位置。

自定义 `QGraphicsItem` 的点击、拖动、框选、端口连线，基本都离不开它。

## 2. 类说明

`QGraphicsSceneMouseEvent` 继承自 `QGraphicsSceneEvent`。它通常进入 `mousePressEvent()`、`mouseMoveEvent()`、`mouseReleaseEvent()`、`mouseDoubleClickEvent()`。

它提供多组位置：`pos()` 是当前 item 坐标，`scenePos()` 是当前场景坐标，`lastPos()` 是上一次 item 坐标，`buttonDownPos()` 是某个按钮按下时的位置。拖动逻辑应按场景需求选择坐标系。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `pos()` / `scenePos()` / `screenPos()` | 当前鼠标位置的 item、scene、screen 坐标。 |
| `lastPos()` / `lastScenePos()` / `lastScreenPos()` | 上一次鼠标位置。 |
| `buttonDownPos(button)` | 指定按钮按下时的 item 坐标。 |
| `buttonDownScenePos(button)` | 指定按钮按下时的 scene 坐标。 |
| `button()` | 触发当前事件的按钮。 |
| `buttons()` | 当前按下的所有按钮。 |
| `modifiers()` | 当前键盘修饰键。 |
| `source()` | 事件来源。 |
| `flags()` | 鼠标事件标志。 |

## 4. 关键用法

拖动 item：

```cpp
void NodeItem::mouseMoveEvent(QGraphicsSceneMouseEvent *event)
{
    const QPointF delta = event->scenePos() - event->lastScenePos();
    moveBy(delta.x(), delta.y());
    event->accept();
}
```

判断是否从按下点拖出一定距离：

```cpp
const QPointF start = event->buttonDownScenePos(Qt::LeftButton);
if (QLineF(start, event->scenePos()).length() > 6)
    beginDrag();
```

## 5. 使用场景

适合节点拖动、控制点编辑、连线创建、场景选择、图形对象点击、画布工具实现。

如果是在 `QGraphicsView` 子类里处理视图平移/缩放，普通 `QMouseEvent` 也可能更直接；如果是 item 级交互，用 scene mouse event。

## 6. 常见坑与经验

拖动 item 时优先用 scene delta，避免 item 自身旋转/缩放后局部 delta 变得难理解。

`button()` 和 `buttons()` 不一样。移动事件中 `button()` 可能不是你想要的当前按下集合，判断拖动状态应看 `buttons()`。

双击通常也伴随按下/释放事件。不要让单击逻辑和双击逻辑互相打架。
