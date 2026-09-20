# QActionEvent

> Qt 6.11.1 · Qt GUI · 来自 `QActionEvent`

## 1. 先建立直觉

`QActionEvent` 是 Qt 在 action 容器发生变化时发送的事件。比如某个 widget、menu、toolbar 增加了 action、移除了 action，或 action 状态变化，Qt 会用它通知相关对象。

普通应用很少手动创建它；自定义能承载 actions 的控件时，才需要在 `actionEvent()` 里读取它。

## 2. 类说明

`QActionEvent` 继承自 `QEvent`。它携带两个指针：`action()` 是被添加/移除/修改的 action，`before()` 表示插入位置之前的 action。

事件类型通常是 `QEvent::ActionAdded`、`ActionRemoved`、`ActionChanged`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QActionEvent(int type, QAction *action, QAction *before)` | 构造 action 事件。通常由 Qt 内部使用。 |
| `action()` | 返回发生变化的 action。 |
| `before()` | 返回插入时位于其后的 action；为空表示追加或无位置含义。 |
| `QWidget::actionEvent()` | QWidget 接收 action 变化的处理入口。 |
| `QEvent::ActionAdded` | action 被加入。 |
| `QEvent::ActionRemoved` | action 被移除。 |
| `QEvent::ActionChanged` | action 属性发生变化。 |

## 4. 关键用法

```cpp
void CommandBar::actionEvent(QActionEvent *event)
{
    if (event->type() == QEvent::ActionAdded)
        insertButtonFor(event->action(), event->before());
    else if (event->type() == QEvent::ActionRemoved)
        removeButtonFor(event->action());
    else if (event->type() == QEvent::ActionChanged)
        updateButtonFor(event->action());
}
```

## 5. 使用场景

适合自定义工具栏、命令栏、可显示 actions 的控件、需要同步 action 列表和 UI 子控件的容器。

普通菜单和工具栏已经处理这些事件，不需要你手写。

## 6. 常见坑与经验

`before()` 只在插入语义中有意义。处理 changed/removed 时不要依赖它。

事件里的 action 指针不代表所有权转移。删除 action 仍由 parent 或创建者负责。

自定义 action 容器要同时处理 added、removed、changed，否则 UI 很容易和命令状态不同步。
