# QDragMoveEvent

> Qt 6.11.1 · Qt GUI · 来自 `QDragMoveEvent`

## 1. 先建立直觉

`QDragMoveEvent` 是拖拽数据在目标控件内部移动时持续发送的事件。目标控件用它更新高亮、插入位置、落点预览，并决定当前位置能不能放下。

它继承自 `QDropEvent`，因此能读取 MIME 数据、位置、动作和修饰键。

## 2. 类说明

`QDragMoveEvent` 的特别之处是可以接受或忽略一个矩形区域。Qt 可以据此减少后续 move 事件频率，目标也能表达“这块区域的反馈相同”。

拖拽移动事件可能非常频繁，处理逻辑应轻量。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `accept()` | 接受当前位置拖放。 |
| `accept(const QRect &)` | 接受指定矩形区域内的拖放。 |
| `ignore()` | 忽略当前位置拖放。 |
| `ignore(const QRect &)` | 忽略指定矩形区域。 |
| `answerRect()` | 返回上次 accept/ignore 指定的区域。 |
| `position()` | 当前拖拽位置，继承自 `QDropEvent`。 |
| `mimeData()` | 读取拖拽数据。 |
| `proposedAction()` / `setDropAction()` | 读取或设置拖放动作。 |

## 4. 关键用法

```cpp
void Canvas::dragMoveEvent(QDragMoveEvent *event)
{
    if (!event->mimeData()->hasFormat("application/x-node")) {
        event->ignore();
        return;
    }

    updateDropPreview(event->position());
    event->acceptProposedAction();
}
```

限制同一区域：

```cpp
event->accept(itemRectAt(event->position().toPoint()));
```

## 5. 使用场景

适合拖拽预览、列表插入线、画布落点高亮、文件拖入目录定位、节点编辑器创建位置提示。

如果目标只需要最终数据，不需要实时反馈，也仍应在 move 中正确 accept/ignore，让系统知道当前位置是否可放。

## 6. 常见坑与经验
不要在每个 move 里做重 IO 或解析大文件。只检查 MIME 类型和位置，真正导入放在 drop。

反馈状态要在 dragLeave/drop 时清理，否则高亮会残留。

接受 move 不代表最终 drop 一定发生；用户可能拖走或取消。
