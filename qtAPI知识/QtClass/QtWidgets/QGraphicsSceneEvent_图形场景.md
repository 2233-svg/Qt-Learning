# QGraphicsSceneEvent：Graphics View 场景事件基类

> Qt 6.11.1 · `#include <QGraphicsSceneEvent>` · 模块：`Qt6::Widgets` · 继承：`QEvent`

`QGraphicsSceneEvent` 是 Graphics View 场景事件的公共基类。`QGraphicsView` 收到鼠标、滚轮、拖放、hover、菜单等输入后，会把原始 Qt 事件转换成对应的 `QGraphicsSceneEvent` 派生类，再交给 `QGraphicsScene` 和目标 `QGraphicsItem`。

## 解决的问题

Graphics View 有自己的坐标体系：item 坐标、scene 坐标和屏幕坐标经常同时存在。场景事件体系把原始 widget 事件转换成 item 能直接理解的数据，并补充来源 widget 和时间戳，让 item 不必自己从 viewport 事件反推坐标。

应用层通常不直接创建基类，而是在 `QGraphicsItem::mousePressEvent()`、`wheelEvent()`、`hoverMoveEvent()` 等函数中接收派生类。

## 语义边界

`widget()` 返回事件关联的 widget 上下文，通常是产生事件的 view/viewport，不是目标 item。`timestamp()` 是原始事件时间戳，适合计算连续输入间隔；它不是日期时间。

事件对象只在事件处理期间有效。若要异步使用，复制坐标、按钮、mime data 等值，不要保存事件指针。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QGraphicsSceneEvent(QEvent::Type type)` | 构造场景事件基类部分；业务代码通常处理派生类。 |
| `~QGraphicsSceneEvent()` | 虚析构。 |
| `widget() const` | 返回事件关联的 widget；不是目标 graphics item。 |
| `setWidget(QWidget *)` | 设置关联 widget，主要供事件构造端使用。 |
| `timestamp() const` | 返回原始事件时间戳；无时间戳时可能为 0。 |
| `setTimestamp(quint64)` | 设置时间戳，主要供事件构造端使用。 |
| 派生鼠标事件 | 使用 `QGraphicsSceneMouseEvent` 读取按钮和多坐标位置。 |
| 派生拖放事件 | 使用 `QGraphicsSceneDragDropEvent` 读取 mime data 和 drop action。 |
| 派生几何事件 | `QGraphicsSceneMoveEvent` / `ResizeEvent` 面向 `QGraphicsWidget`。 |
