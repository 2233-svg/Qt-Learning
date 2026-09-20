# QShortcutEvent

> Qt 6.11.1 · Qt GUI · 来自 `QShortcutEvent`

## 1. 先建立直觉

`QShortcutEvent` 是快捷键匹配后送到对象的事件。它告诉接收者哪个 `QKeySequence` 被触发，以及这次匹配是否有歧义。

大多数时候你只连接 `QShortcut::activated()` 或 `QAction::triggered()`；只有自定义事件处理、快捷键管理器或调试冲突时，才直接关心这个事件。

## 2. 类说明

`QShortcutEvent` 继承自 `QEvent`。它包含触发的 key sequence、相关 `QShortcut` 指针，以及 ambiguous 标志。

ambiguous 表示同一个按键序列匹配多个快捷键。此时 Qt 不一定能明确知道用户想触发哪一个命令。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QShortcutEvent(QKeySequence, QShortcut *, bool ambiguous)` | 创建快捷键事件，Qt 6.5 起提供。 |
| `key()` | 返回触发的按键序列。 |
| `isAmbiguous()` | 返回这次匹配是否存在歧义。 |
| `QShortcut::activated()` | 非歧义快捷键触发信号。 |
| `QShortcut::activatedAmbiguously()` | 歧义快捷键触发信号。 |
| `QEvent::Shortcut` | 快捷键事件类型。 |

## 4. 关键用法

```cpp
bool ShortcutDebugger::eventFilter(QObject *obj, QEvent *event)
{
    if (event->type() == QEvent::Shortcut) {
        auto *shortcutEvent = static_cast<QShortcutEvent *>(event);
        qDebug() << shortcutEvent->key()
                 << "ambiguous:" << shortcutEvent->isAmbiguous();
    }
    return QObject::eventFilter(obj, event);
}
```

## 5. 使用场景

适合快捷键调试工具、命令系统、事件过滤器、自定义快捷键冲突提示、特殊输入路由。

普通命令触发不需要处理它，用 `QAction` 或 `QShortcut` 信号更清楚。

## 6. 常见坑与经验

不要保存事件指针。事件处理完就失效，需要记录就保存 key 或自己的命令 id。

歧义不是错误崩溃，而是快捷键设计冲突。最好在设置页或启动检查中提前发现。

快捷键上下文会影响是否匹配。调试时同时检查 key sequence 和 `Qt::ShortcutContext`。
