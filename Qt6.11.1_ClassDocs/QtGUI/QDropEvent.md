# QDropEvent

> Qt 6.11.1 · Qt GUI · 来自 `QDropEvent`

## 1. 先建立直觉

`QDropEvent` 是拖放目标端收到“用户在这里放下了数据”时的事件。它携带位置、MIME 数据、可能动作、建议动作和源对象。

处理 drop 的核心流程是：检查 `mimeData()`，选择/接受一个 drop action，然后把数据导入到当前位置。

## 2. 类说明

`QDropEvent` 继承自 `QEvent`，`QDragMoveEvent` 又继承它。它不拥有 MIME 数据，只提供读取接口。

drop action 是协商结果：源端声明可能动作，目标端接受建议动作或设置自己的动作。Move/Copy/Link 的业务后果要由源端和目标端一起遵守。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `position()` | drop 在目标坐标系中的位置。 |
| `mimeData()` | 读取拖拽携带的 MIME 数据。 |
| `possibleActions()` | 源端支持的动作集合。 |
| `proposedAction()` | 系统根据源、目标、修饰键建议的动作。 |
| `dropAction()` | 当前目标选择的动作。 |
| `setDropAction()` | 设置目标实际接受的动作。 |
| `acceptProposedAction()` | 接受系统建议动作。 |
| `source()` | 返回拖拽源对象，跨应用时可能为空。 |
| `buttons()` | drop 时鼠标按钮状态。 |
| `modifiers()` | drop 时键盘修饰键。 |

## 4. 关键用法

```cpp
void DropArea::dropEvent(QDropEvent *event)
{
    const QMimeData *data = event->mimeData();
    if (data->hasUrls()) {
        importFiles(data->urls(), event->position());
        event->acceptProposedAction();
    } else {
        event->ignore();
    }
}
```

强制 copy：

```cpp
if (event->possibleActions() & Qt::CopyAction) {
    event->setDropAction(Qt::CopyAction);
    event->accept();
}
```

## 5. 使用场景

适合文件导入、文本粘贴式拖放、素材拖入画布、列表项跨控件移动、跨应用数据交换。

如果只是控件内部重新排序，Qt 的 item view 拖放模型或自定义鼠标拖动可能更轻。

## 6. 常见坑与经验

drop 前通常必须在 dragEnter/dragMove 中接受过对应数据，否则 drop 可能不会到达。

不要假设 `source()` 一定非空。跨应用拖放时目标端只能依赖 MIME 数据。

Move 动作意味着源端可能删除原数据；目标端不要在没有真正导入成功时接受 Move。
