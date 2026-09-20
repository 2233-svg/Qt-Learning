# QGraphicsSceneDragDropEvent

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsSceneDragDropEvent`

## 1. 先建立直觉

`QGraphicsSceneDragDropEvent` 是拖放进入 Graphics View 场景或 item 时使用的事件。它承载被拖的数据、拖动来源、允许动作、当前建议动作和坐标。

它用于“把文件拖进画布”“把素材拖到节点上”“从列表拖一个组件到场景里”这类交互。

## 2. 类说明

`QGraphicsSceneDragDropEvent` 继承自 `QGraphicsSceneEvent`。它通常进入 `dragEnterEvent()`、`dragMoveEvent()`、`dragLeaveEvent()`、`dropEvent()`。

真正的数据在 `mimeData()` 里。你需要检查格式，决定是否接受事件，并设置合适的 drop action。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `mimeData()` | 读取拖放数据，如文本、URL、自定义 MIME。 |
| `pos()` / `scenePos()` / `screenPos()` | 读取 item、scene、screen 坐标。 |
| `source()` | 返回拖动来源对象。 |
| `possibleActions()` | 源支持的动作集合。 |
| `proposedAction()` | 系统建议的动作。 |
| `dropAction()` | 当前将执行的动作。 |
| `setDropAction(Qt::DropAction)` | 设置实际 drop 动作。 |
| `acceptProposedAction()` | 接受系统建议动作。 |
| `buttons()` | 拖动时按下的鼠标按钮。 |
| `modifiers()` | 拖动时的键盘修饰键。 |

## 4. 关键用法

```cpp
void CanvasItem::dragEnterEvent(QGraphicsSceneDragDropEvent *event)
{
    if (event->mimeData()->hasUrls())
        event->acceptProposedAction();
    else
        event->ignore();
}

void CanvasItem::dropEvent(QGraphicsSceneDragDropEvent *event)
{
    for (const QUrl &url : event->mimeData()->urls())
        importAt(url, event->scenePos());
    event->acceptProposedAction();
}
```

要让 item 接收 drop，还需要设置：

```cpp
setAcceptDrops(true);
```

## 5. 使用场景

适合拖入文件、素材库拖拽、节点创建、图形对象重排、跨应用拖文本/图片、从外部资源管理器导入内容。

如果只是 scene 内部移动 item，普通鼠标拖动或 item flags 可能更简单；drag/drop 更适合携带 MIME 数据的拖放。

## 6. 常见坑与经验

`dragEnterEvent()` 不接受，后续 move/drop 往往不会到来。先做格式判断并明确 accept。

不要只看文件后缀。拖放数据应先检查 `mimeData()` 能力，再解析内容。

drop 坐标通常用 scene 坐标落点最自然；放到某个 item 内部时再映射到 item 坐标。
