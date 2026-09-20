# QGraphicsSceneDragDropEvent：场景 item 的拖放协商事件

> Qt 6.11.1 · `#include <QGraphicsSceneDragDropEvent>` · 模块：`Qt6::Widgets` · 继承：`QGraphicsSceneEvent`

`QGraphicsSceneDragDropEvent` 表示拖拽数据进入、移动、离开或投放到 Graphics View 场景中的 item。它同时携带 MIME 数据、拖放来源、允许动作、建议动作、最终动作和落点坐标。

## 使用场景

item 在 `dragEnterEvent()` 或 `dragMoveEvent()` 中检查 `mimeData()` 和动作集合，决定是否接受；在 `dropEvent()` 中读取数据并执行导入、创建 item、移动对象等业务。外部程序拖入时 `source()` 可能为空，不能假设拖拽源一定来自本应用。

`mimeData()` 是只读且由拖放系统拥有。若需要异步处理，立即复制 `urls()`、`text()` 或自定义字节，不要缓存指针。

## 动作边界

`possibleActions()` 是源允许的动作集合，`proposedAction()` 是当前建议动作，`dropAction()` 是接收端最终选择。建议动作符合需求时调用 `acceptProposedAction()`；需要强制复制/移动时用 `setDropAction()` 后再 `accept()`。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QGraphicsSceneDragDropEvent(QEvent::Type type = None)` | 构造场景拖放事件；通常由 Qt 创建。 |
| `pos()` / `scenePos()` / `screenPos()` | item、scene、屏幕坐标中的拖放位置。 |
| `buttons() const` | 拖放过程中按住的鼠标按钮。 |
| `modifiers() const` | 拖放时的键盘修饰键，常影响 copy/move/link。 |
| `possibleActions() const` | 拖拽源允许的动作集合。 |
| `proposedAction() const` | 源或平台建议动作。 |
| `dropAction() const` | 接收端当前选择的最终动作。 |
| `setDropAction(Qt::DropAction)` | 指定最终动作；应符合业务和源允许动作。 |
| `acceptProposedAction()` | 采用建议动作并接受事件。 |
| `source() const` | 返回拖拽源 widget；外部拖入时可能为空。 |
| `mimeData() const` | 返回只读 MIME 数据；不要缓存或删除。 |
| `set...()` 系列 | 除 `setDropAction()` 外主要供事件构造端使用。 |
