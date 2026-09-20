# Qt QAccessibleEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleEvent>`  
> 所属模块：`Qt6::Gui`  
> 定位：向辅助技术报告变化的不可复制事件基类

## 1. 它解决什么问题

`QAccessibleEvent` 把“哪个可访问对象发生了什么变化”封装为一条通知，并通过 `QAccessible::updateAccessibility()` 交给平台无障碍后端。屏幕阅读器、盲文显示器等工具据此决定何时重新查询对象、朗读什么内容或更新自己的对象缓存。

它是通知对象，不是 `QEvent`，也不通过 `QObject::event()` 投递：

- 创建事件后调用 `QAccessible::updateAccessibility()`；
- 事件描述变化，真正的数据仍由 `QAccessibleInterface` 在被查询时提供；
- 事件不拥有目标 QObject 或 accessible interface；
- 通知应在状态已经改变后发出；
- 对复杂变化应使用派生事件，而不是只用通用 event type。

## 2. 基本用法

```cpp
void MyWidget::setCustomFocus()
{
    applyFocusState();

    QAccessibleEvent event(this, QAccessible::Focus);
    QAccessible::updateAccessibility(&event);
}
```

事件应该是短生命周期栈对象。传给 `updateAccessibility()` 的指针只在调用期间有效；不要用 heap 分配后遗忘释放，也不要让异步任务保存栈事件地址。

对于值、状态、文本和表格模型变化，应使用专门派生类，例如：

- `QAccessibleValueChangeEvent`；
- `QAccessibleStateChangeEvent`；
- `QAccessibleTextCursorEvent`、`QAccessibleTextInsertEvent`、`QAccessibleTextRemoveEvent`、`QAccessibleTextUpdateEvent`、`QAccessibleTextSelectionEvent`；
- `QAccessibleTableModelChangeEvent`；
- `QAccessibleAnnouncementEvent`。

头文件会断言某些需要附加数据的事件类型不能用基类直接构造，正是为了避免丢失变化详情。

## 3. 构造目标的选择

### 传 `QObject *`

普通控件代码优先用这个重载：

```cpp
QAccessibleEvent event(widget, QAccessible::NameChanged);
```

事件保存对象指针，不转移所有权。除 `ObjectDestroyed` 外，目标 QObject 必须非空并且在提交事件时仍有效。

### 传 `QAccessibleInterface *`

当实现代码已经持有 accessible interface，或者对象没有直接可用 QObject 时使用：

```cpp
QAccessibleEvent event(iface, QAccessible::LocationChanged);
```

该重载会关联 interface 的 unique id 和它的 QObject。interface 必须有效，且 event 不拥有它。普通业务代码不需要为了构造事件而额外查询 interface，因为 QObject 重载通常成本更低。

## 4. 类型、子项与生命周期

`type()` 返回 `QAccessible::Event`，应准确说明变化类别。选择错误 type 会导致辅助技术错过更新或作出错误播报，例如值变化应使用 `ValueChanged` 及其专用事件，而不是泛泛发送 `ObjectReorder`。

`child` 默认是 `-1`，表示事件针对对象本身。若变化针对旧式 child index 模型中的特定子项，可用 `setChild()` 设置索引；它不是 QObject 指针、模型 index，也不是层级路径。现代复杂控件更常通过独立 accessible interface 表达子元素。

事件不可复制。它只借用目标，必须在更新调用期间保持目标、接口和相关缓存有效。对象销毁相关通知尤其要谨慎：不要在对象已经释放之后再访问其成员来填充事件数据。

## 5. 逐项 API 说明

### `QAccessibleEvent(QObject *object, QAccessible::Event type)`

构造针对 QObject 的事件。`type` 描述已经发生的变化；除了 `ObjectDestroyed`，`object` 必须非空。

对需要额外 payload 的类型不要使用此构造函数，例如 `ValueChanged`、`StateChanged`、文本变化、表格模型变化和 announcement 都应使用对应派生事件。

### `QAccessibleEvent(QAccessibleInterface *interface, QAccessible::Event type)`

构造针对 accessible interface 的事件。适合已经拥有 interface 的实现路径；可避免重新从 QObject 查询接口。

`interface` 必须非空。事件不拥有 interface，也不保证提交后它仍可被调用方保存。

### `virtual ~QAccessibleEvent()`

虚析构函数。销毁 event 自身状态，不会销毁目标 QObject、interface 或 accessible cache 中的接口实例。

### `virtual QAccessibleInterface *accessibleInterface() const`

返回与事件相关联的 accessible interface。查询可能因为接口不可用、对象已失效或事件只携带不再有效的 id 而返回 `nullptr`。

返回指针由 Qt 的可访问性缓存管理，调用方不能删除、长期保存或跨事件循环无条件使用它。

### `QObject *object() const`

返回事件目标 QObject 指针。它是非拥有指针。普通事件提交期间可用于定位对象，但异步环境中必须先确认对象仍然存在。

### `QAccessible::Event type() const`

返回此通知的事件类型。类型固定描述该事件要报告的变化；不能在构造后改成另一类事件。选择类型时优先用最精确、能携带足够细节的类型。

### `void setChild(int child)`

设置受影响 child 的整数索引。用于对象内部子项语义；调用前应确保索引与该对象的 accessible child 顺序一致。

`-1` 是构造时的默认值，通常表示对象本身。不要把普通模型行号或任意业务 ID 直接塞入。

### `int child() const`

返回当前 child 索引。若为 `-1`，按对象自身处理。该数值只有结合目标对象当时的 accessible child 模型才有意义。

### `QAccessible::Id uniqueId() const`

返回事件关联的 unique id。该 API 出现在 Qt 头文件中，主要供无障碍缓存与后端定位 interface 使用；id 不应被持久化，也不能在接口删除后继续当作有效身份。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 构造 | `QAccessibleEvent(QObject *, Event)` | 为 QObject 创建变化通知。 | 目标只借用；需要 payload 的类型应改用派生事件。 |
| 构造 | `QAccessibleEvent(QAccessibleInterface *, Event)` | 为已有 interface 创建通知。 | interface 非空且不转移所有权。 |
| 生命周期 | `~QAccessibleEvent()` | 虚析构事件。 | 不删除对象、接口或缓存条目。 |
| 查询 | `accessibleInterface()` | 获取关联 interface。 | 可能为 `nullptr`；结果由 Qt 管理。 |
| 查询 | `object()` | 获取关联 QObject。 | 非拥有指针，不能跨异步生命周期盲用。 |
| 查询 | `type()` | 获取变化类型。 | 选择最精确的 `QAccessible::Event`。 |
| 子项 | `setChild(int)` | 设置受影响 child index。 | 不是模型行号或业务 ID；默认 `-1` 表示对象自身。 |
| 子项 | `child()` | 获取 child index。 | 只有结合当时的 accessible 子项顺序才有意义。 |
| 缓存 | `uniqueId()` | 获取 interface 的短期缓存 id。 | 不持久化，不把它当对象所有权或稳定主键。 |
| 提交 | `QAccessible::updateAccessibility(QAccessibleEvent *)` | 将通知交给无障碍后端。 | 必须在状态变化后调用，event 在调用期间有效。 |

### 一句话总结

`QAccessibleEvent` 是无障碍变化通知的基类：用准确的事件类型描述已经发生的状态，用专用派生类携带复杂 payload，事件短暂借用目标并在调用 `updateAccessibility()` 时提交。
