# QDragEnterEvent

> Qt 6.11.1 · Qt GUI · 来自 `QDragEnterEvent`

## 1. 先建立直觉

`QDragEnterEvent` 是拖拽进入目标控件时发送的事件。目标在这里快速判断“这种数据我能不能接”，并决定是否接受后续拖拽移动和放下。

它是拖放目标端的第一道门。enter 阶段不接受，后续 `dragMoveEvent()` 和 `dropEvent()` 往往不会按你期望发生。

## 2. 类说明

`QDragEnterEvent` 继承自 `QDragMoveEvent`，因此拥有位置、MIME 数据、possible/proposed actions、按钮和修饰键等信息。

Qt 文档提醒不要自己创建它，因为真实拖放事件依赖窗口系统和 Qt 内部状态。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `mimeData()` | 检查拖入数据格式。 |
| `possibleActions()` | 源端支持的动作集合。 |
| `proposedAction()` | 系统建议动作。 |
| `acceptProposedAction()` | 接受建议动作，最常用。 |
| `setDropAction()` | 自行选择 Copy/Move/Link。 |
| `position()` | 拖入位置。 |
| `buttons()` / `modifiers()` | 当前鼠标和键盘状态。 |

## 4. 关键用法

```cpp
void DropArea::dragEnterEvent(QDragEnterEvent *event)
{
    if (event->mimeData()->hasUrls())
        event->acceptProposedAction();
    else
        event->ignore();
}
```

控件还需要开启：

```cpp
setAcceptDrops(true);
```

## 5. 使用场景

适合文件拖入、素材拖入、跨应用文本/图片接收、列表项移动目标判断。

如果控件没有 drop 行为，不要接受 enter；接受会给用户错误反馈。

## 6. 常见坑与经验

enter 里只做轻量格式判断，不要真正导入数据。导入应在 drop。

检查 MIME 类型比检查文件后缀更可靠。后缀可作为第二层判断。

接受了 enter 后，move 阶段仍可根据当前位置继续 accept/ignore。
