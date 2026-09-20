# QDragLeaveEvent

> Qt 6.11.1 · Qt GUI · 来自 `QDragLeaveEvent`

## 1. 先建立直觉

`QDragLeaveEvent` 表示拖拽离开了目标控件。它通常没有复杂数据，重点是通知你：之前在 drag enter/move 中显示的高亮、插入线、预览状态该清掉了。

它是拖放体验里很容易被忽略的一环。忘记处理它，界面常会留下“还可以放”的假状态。

## 2. 类说明

`QDragLeaveEvent` 继承自 `QEvent`。它一般进入 `QWidget::dragLeaveEvent()` 或对应窗口/对象事件处理。

Qt 文档提醒不要自己创建它，因为真实拖放事件依赖 Qt 和窗口系统内部状态。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QDragLeaveEvent()` | 构造函数，通常不应由应用手动调用。 |
| `QWidget::dragLeaveEvent()` | 处理拖拽离开的主要入口。 |
| `QEvent::DragLeave` | 事件类型。 |
| `accept()` / `ignore()` | 继承自 `QEvent` 的事件处理状态。 |

## 4. 关键用法

```cpp
void DropArea::dragLeaveEvent(QDragLeaveEvent *event)
{
    clearDropHighlight();
    event->accept();
}
```

如果 move 中显示了插入位置：

```cpp
dropIndicator.clear();
update();
```

## 5. 使用场景

适合清理拖放高亮、隐藏落点预览、恢复光标状态、取消临时滚动或展开计时器。

所有实现了 drag enter/move 视觉反馈的目标，都应该考虑 leave。

## 6. 常见坑与经验

leave 不是 drop。用户可能只是拖走了，不能在这里导入或删除数据。

如果控件销毁或拖放被取消，也要确保临时状态最终能清理；必要时在 drop 和 leave 都调用同一个 cleanup。

不要依赖 leave 里有 MIME 数据。需要数据判断应在 enter/move/drop。
