# Qt QAccessibleStateChangeEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleStateChangeEvent>`  
> 所属模块：`Qt6::Gui`  
> 基类：`QAccessibleEvent`  
> 定位：携带“哪些状态位发生改变”信息的无障碍通知事件

## 1. 它解决什么问题

`QAccessibleStateChangeEvent` 用于通知辅助技术某个可访问对象的状态发生变化。它的 payload 是 `QAccessible::State`，但这个 payload **不是对象的新完整状态，也不是旧状态**，而是“哪些状态字段发生过变化”的位掩码。

例如对象失去焦点后：

- `QAccessibleInterface::state().focused` 的当前值是 `false`；
- `event.changedStates().focused` 应是 `true`，表示 focused 这个字段发生了变化。

辅助技术收到事件后再调用 `state()` 获取当前真值。把完整 state 直接传入会错误地声明所有当前为 true 的位都发生了变化。

## 2. 基本用法

```cpp
void Toggle::setChecked(bool checked)
{
    if (m_checked == checked)
        return;

    m_checked = checked;
    update();

    QAccessible::State changed;
    changed.checked = true; // 表示 checked 字段改变，不表示新值

    QAccessibleStateChangeEvent event(this, changed);
    QAccessible::updateAccessibility(&event);
}
```

一次调用可标记多个确实同时改变的状态位：

```cpp
QAccessible::State changed;
changed.expanded = true;
changed.collapsed = true;
changed.focused = true;
```

只设置这次真的发生变化的字段。事件必须在对象状态已更新后提交，这样辅助技术随后查询 `state()` 才能拿到新状态。

## 3. 与其他事件的边界

以下情况不应勉强使用 state change event：

- 数值变化需要携带新 `QVariant` 值：用 `QAccessibleValueChangeEvent`；
- 文本插入、删除、更新、光标或选择变化：用相应文本事件；
- 表格模型结构/数据变化：用 `QAccessibleTableModelChangeEvent`；
- 要主动播报一条消息：用 `QAccessibleAnnouncementEvent`；
- 对象创建、隐藏、重排、名称/描述变化等：使用最精确的 `QAccessible::Event` 或相应派生事件。

状态变化不替代正确的 `role()`、`text()`、`rect()` 实现；event 只是通知客户端重新读取这些动态信息。

## 4. 目标、所有权与有效性

可以用 QObject 或 `QAccessibleInterface` 构造。两者都只借用目标，不转移所有权：

- 普通控件代码通常传 `this`；
- 实现代码已经持有 interface 时可传 interface，避免再次查询；
- 目标在调用 `QAccessible::updateAccessibility()` 前必须有效；
- event 通常栈上创建，提交后不长期保存。

对象销毁、跨线程修改或事件晚于状态变化太久都会导致辅助技术读到错误/过期状态。状态改变与事件提交应在同一 GUI 线程、相近的调用路径中完成。

## 5. 逐项 API 说明

### `QAccessibleStateChangeEvent(QObject *object, QAccessible::State state)`

构造针对 `object` 的 `StateChanged` 事件。`state` 是变化位掩码，不是完整状态快照。`object` 必须在提交期间有效。

### `QAccessibleStateChangeEvent(QAccessibleInterface *iface, QAccessible::State state)`

构造针对 `iface` 的状态事件。适合已经持有 interface 的自定义可访问实现；interface 只被借用，不能在 event 提交前销毁。

### `~QAccessibleStateChangeEvent()`

虚析构由基类提供。销毁 event 不会删除对象或 interface。

### `QAccessible::State changedStates() const`

返回变化位掩码。每个为 true 的字段表示该字段的值从旧状态到新状态发生过变化；字段为 false 表示本次没有报告它变化。

要判断对象目前是否 focused、checked、expanded 或 disabled，必须再次调用目标的 `QAccessibleInterface::state()`，不能从 `changedStates()` 推断当前值。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 构造 | `QAccessibleStateChangeEvent(QObject *, State)` | 为 QObject 创建状态变化事件。 | `State` 是变化掩码；目标只借用。 |
| 构造 | `QAccessibleStateChangeEvent(QAccessibleInterface *, State)` | 为 interface 创建状态变化事件。 | interface 必须有效，不转移所有权。 |
| 生命周期 | `~QAccessibleStateChangeEvent()` | 销毁事件。 | 不删除对象或 interface。 |
| 查询 | `changedStates()` | 返回已改变的 state 字段掩码。 | 不能当完整或新 state；当前值从 `state()` 查询。 |
| 提交 | `QAccessible::updateAccessibility(&event)` | 通知无障碍后端。 | 必须在状态更新后、目标有效时调用。 |

### 一句话总结

`QAccessibleStateChangeEvent` 的关键是“变的是哪个字段”，而不是“字段现在是什么值”：只置位真正改变的状态字段，提交后让辅助技术通过 `QAccessibleInterface::state()` 读取当前完整状态。
