# Qt QShortcutEvent：快捷键匹配结果的事件对象

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QShortcutEvent>`  
> 所属模块：`Qt6::Gui`，需要启用 shortcut 配置  
> 继承：`QEvent`  
> 类型定位：向 `QShortcut` 或事件接收者报告快捷键匹配结果

## 1. 它解决什么问题

`QShortcutEvent` 表示一次已经被 Qt 快捷键系统识别的快捷键事件。它携带三类信息：

- 用户按下的 `QKeySequence`；
- 对应的 shortcut 对象或旧式 shortcut ID；
- 当前匹配是否存在歧义。

它是快捷键分发链中的事件对象，不是普通键盘按键事件。`QKeyEvent` 表示一个物理/逻辑按键，`QShortcutEvent` 表示 Qt 已经把一组按键匹配为 shortcut 后的结果。

## 2. 事件分发位置

通常应用不需要手工创建它。Qt 的快捷键管理器根据 `QShortcut` 的 key、context、enabled 和 autoRepeat 状态生成事件，再由 shortcut 对象处理并发出 `activated()` 或 `activatedAmbiguously()`。

只有在做自定义事件过滤器、调试快捷键分发或编写 Qt 集成代码时，才通常需要检查它：

```cpp
bool Filter::eventFilter(QObject *watched, QEvent *event)
{
    if (event->type() == QEvent::Shortcut) {
        auto *shortcutEvent = static_cast<QShortcutEvent *>(event);
        qDebug() << shortcutEvent->key()
                 << shortcutEvent->isAmbiguous();
    }
    return QObject::eventFilter(watched, event);
}
```

事件指针只在当前事件处理期间有效，不要保存裸指针供异步代码使用。若需要保存信息，应复制 `key()` 或 `isAmbiguous()` 的结果。

## 3. 构造函数

### `QShortcutEvent(const QKeySequence &key, const QShortcut *shortcut = nullptr, bool ambiguous = false)`

创建与 `QShortcut` 对象关联的快捷键事件。`shortcut` 可以为空，表示事件没有关联到具体 shortcut 对象。`ambiguous` 为 `true` 时，`isAmbiguous()` 返回 `true`。

这个构造器适合需要把事件和 shortcut 对象关联的内部/测试代码。应用通常不应通过手工发送它来模拟正常快捷键，因为这样会绕过 context、enabled、焦点和冲突解析。

### `QShortcutEvent(const QKeySequence &key, int id, bool ambiguous = false)`

使用旧式整数 shortcut ID 创建事件。该构造器在公开头文件中保留，但属于弃用的旧路径，主要是为了内部或兼容代码。新代码不要用 `QShortcut::id()` 建立业务逻辑。

## 4. 成员函数

### `const QKeySequence &key() const`

返回事件携带的快捷键序列，以 const 引用形式提供。引用只在事件对象仍然存在时有效；若要跨事件处理阶段使用，应复制：

```cpp
const QKeySequence sequence = shortcutEvent->key();
```

返回的是匹配到的序列，不是 `QShortcut::keys()` 的完整候选列表。

### `bool isAmbiguous() const`

返回当前快捷键匹配是否有歧义。为 `true` 时，应用不应把事件当作明确的命令执行结果。对 `QShortcut` 而言，这通常对应 `activatedAmbiguously()`，而不是 `activated()`。

### `int shortcutId() const`

返回旧式整数 shortcut ID。该 getter 与整数构造器属于弃用兼容接口。ID 是运行时注册标识，不是稳定的文件 ID、命令 ID 或跨进程协议字段。新代码应保存 `QShortcut *`、命令对象或显式业务枚举。

## 5. 与 `QKeyEvent`、`QShortcut` 的区别

| 类型 | 表达的层次 | 典型用途 |
| --- | --- | --- |
| `QKeyEvent` | 一次按键/释放事件 | 文本输入、方向键、物理按键处理 |
| `QShortcutEvent` | shortcut 匹配后的结果 | shortcut 内部激活和事件过滤 |
| `QShortcut` | 注册 key/context 并发出信号的对象 | 应用命令快捷键 |

不要在 `QKeyEvent` 处理器中直接假设某个序列已经匹配，也不要把 `QShortcutEvent::key()` 当成单个键码。

## 6. 歧义语义

歧义可能来自：

- 多个 `QShortcut` 使用相同或重叠序列；
- widget、window、application shortcut context 重叠；
- 多步序列的前缀冲突；
- 多个候选序列同时满足当前按键输入。

`isAmbiguous()` 只是当前事件的结果标志。它不会告诉你是哪几个 shortcut 冲突，也不会自动选择优先级。诊断冲突时，应结合对象树、shortcut context、`QShortcut::keys()` 和菜单 action 的快捷键设置检查。

## 7. 事件接受和手工发送

它继承 `QEvent` 的 accepted 状态，但快捷键是否激活主要由 Qt 的 shortcut 匹配和 `QShortcut` 处理逻辑决定。简单地对一个手工创建的 `QShortcutEvent` 调用 `accept()`，不会生成真实键盘输入，也不会修正 shortcut 注册冲突。

如果必须测试事件处理，优先测试 `QShortcut` 的信号、键序列和 context；只有测试底层事件过滤逻辑时才手工构造事件。

## 8. 生命周期和线程

事件对象通常由 Qt 在 GUI 事件分发期间创建和销毁，接收者不拥有它。不要把事件指针放进队列、定时器或 lambda 延后读取。

快捷键事件来自 GUI 事件循环。跨线程触发命令时，应把业务命令通过 queued signal/slot 发送给目标线程，而不是把 `QShortcutEvent *` 跨线程传递。

## 9. 常见误区

- 把它当成 `QKeyEvent`，按 `key()` 返回整数键码处理。
- 把 `key()` 引用保存到事件生命周期之外。
- 看到 `isAmbiguous()` 为 `true` 仍执行明确命令。
- 用 `shortcutId()` 作为持久化命令 ID。
- 手工发送事件期待 Qt 自动完成 shortcut context 和冲突解析。
- 认为事件能告诉应用全部冲突对象：它只携带当前匹配结果。
- 忽略 `QShortcut` 的 `enabled`、`context` 和父 widget 状态。

## API 速查表
| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QShortcutEvent(const QKeySequence &, const QShortcut *, bool)` | 创建与 shortcut 关联的事件 | 通常由 Qt 内部产生，手工发送会绕过匹配逻辑 |
| 构造 | `QShortcutEvent(const QKeySequence &, int, bool)` | 用旧式 ID 创建事件 | 弃用兼容路径，不要用于新业务代码 |
| 查询 | `key() const` | 获取匹配的完整键序列 | 返回引用只在事件生命周期内有效 |
| 查询 | `isAmbiguous() const` | 判断是否存在歧义 | 歧义时不要当作明确激活 |
| 查询 | `shortcutId() const` | 获取旧式运行时 ID | 弃用，不是稳定业务标识 |
| 事件类型 | `QEvent::Shortcut` | 标识 shortcut 事件 | 与 `QKeyEvent` 的键盘事件层次不同 |

---

### 一句话总结

`QShortcutEvent` 表示“Qt 已经把按键序列匹配成快捷键”的结果：`key()` 是完整序列，`isAmbiguous()` 是冲突标志，`shortcutId()` 是弃用的旧接口；普通应用优先使用 `QShortcut` 信号，而不是手工发送或长期保存事件对象。
