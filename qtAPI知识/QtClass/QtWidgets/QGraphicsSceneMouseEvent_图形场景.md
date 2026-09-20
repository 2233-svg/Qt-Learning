# QGraphicsSceneMouseEvent：Graphics View 的鼠标事件

> Qt 6.11.1 · `#include <QGraphicsSceneMouseEvent>` · 模块：`Qt6::Widgets` · 继承：`QGraphicsSceneEvent`

`QGraphicsSceneMouseEvent` 是 `QGraphicsView` 把 `QMouseEvent` 转给场景和 item 后形成的事件对象。它同时保存 item、scene、screen 三套坐标，以及上一帧位置、按下位置、按钮状态和事件来源。

## 使用场景

在 `QGraphicsItem::mousePressEvent()`、`mouseMoveEvent()`、`mouseReleaseEvent()`、`mouseDoubleClickEvent()` 中读取它。拖动 item 内部内容时用 `pos()`；创建或对齐场景对象时用 `scenePos()`；弹出系统菜单或跨窗口定位时用 `screenPos()`。

`button()` 是触发当前事件的按钮；`buttons()` 是事件发生时仍处于按下状态的按钮集合。拖拽判断通常看 `buttons()`，单次按下/释放判断看 `button()`。

## 坐标边界

`buttonDownPos(button)`、`buttonDownScenePos(button)`、`buttonDownScreenPos(button)` 返回指定按钮最初按下的位置，适合计算拖动距离。`lastPos()` 系列是 view 收到的上一鼠标事件位置，适合做增量移动。

合成鼠标事件可以通过 `source()` 和 `flags()` 识别，例如触摸转鼠标。不要默认所有鼠标事件都来自真实鼠标设备。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QGraphicsSceneMouseEvent(QEvent::Type type = None)` | 构造场景鼠标事件；通常由 Qt 创建。 |
| `pos()` / `setPos()` | item 局部坐标位置。 |
| `scenePos()` / `setScenePos()` | scene 坐标位置。 |
| `screenPos()` / `setScreenPos()` | 屏幕坐标位置。 |
| `lastPos()` / `lastScenePos()` / `lastScreenPos()` | 上一次鼠标事件的位置，用于增量计算。 |
| `buttonDownPos(button)` | 指定按钮按下时的 item 坐标。 |
| `buttonDownScenePos(button)` | 指定按钮按下时的 scene 坐标。 |
| `buttonDownScreenPos(button)` | 指定按钮按下时的 screen 坐标。 |
| `button() const` | 触发当前 press/release/doubleClick 的按钮。 |
| `buttons() const` | 当前处于按下状态的按钮集合。 |
| `modifiers() const` | 事件发生时的键盘修饰键。 |
| `source() const` | 鼠标事件来源，可区分真实/合成事件。 |
| `flags() const` | 附加鼠标事件标志。 |
| `set...()` 系列 | 主要供框架、测试或自定义事件构造使用。 |
