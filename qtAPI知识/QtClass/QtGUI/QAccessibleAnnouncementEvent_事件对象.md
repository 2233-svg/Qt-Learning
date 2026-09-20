# Qt QAccessibleAnnouncementEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleAnnouncementEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QAccessibleEvent`  
> 自 Qt 6.8 引入  
> 定位：请求辅助技术播报一条临时消息的事件对象

## 1. 它解决什么问题

`QAccessibleAnnouncementEvent` 让应用主动请求屏幕阅读器等辅助技术播报一条消息。它适用于界面变化已经发生，但变化本身不一定能通过焦点、名称、值或状态变化自然传达给用户的场景。

常见例子包括：

- 文件上传完成、后台同步失败或操作已撤销；
- 表单校验结果需要马上告知，但焦点不应跳走；
- 搜索结果数量更新；
- 动态状态区域的短消息；
- 自定义控件完成异步操作。

它不是普通通知系统，也不保证消息一定被朗读：

- 是否支持、何时播报、如何合并相邻播报由平台和辅助技术决定；
- 它不会显示 visual toast、对话框或状态栏文本；
- 不应把每一帧变化或日志逐条包装成 announcement；
- 不能替代对真实对象的 `NameChanged`、`ValueChanged`、`StateChanged` 等精确事件。

## 2. 基本用法

```cpp
void UploadWidget::finishUpload()
{
    updateUiAfterUpload();

    QAccessibleAnnouncementEvent event(
        this, tr("Upload completed"));
    QAccessible::updateAccessibility(&event);
}
```

事件应在 UI 状态已经更新之后发送。这样进程内屏幕阅读器在接收通知时，查询到的是新状态而不是旧状态。

紧急且必须中断当前播报的消息可明确提高优先级：

```cpp
QAccessibleAnnouncementEvent event(
    this, tr("Connection lost"));
event.setPoliteness(QAccessible::AnnouncementPoliteness::Assertive);
QAccessible::updateAccessibility(&event);
```

## 3. `Polite` 与 `Assertive`

事件默认使用 `QAccessible::AnnouncementPoliteness::Polite`：

| 优先级 | 语义 | 使用建议 |
| --- | --- | --- |
| `Polite` | 辅助技术应在合适时机播报，例如当前句子结束或用户暂停输入时。 | 普通完成、结果更新、非阻断提示的默认选择。 |
| `Assertive` | 辅助技术应立即播报，即使可能打断当前任务或正在播报的内容。 | 仅用于必须立刻知道的严重或阻断性信息。 |

`Assertive` 会打断用户，过度使用会让任何真正紧急的提示失去价值。绝大多数 UI 消息应保持 `Polite`，并通过内容简洁、去重和合并避免播报噪声。

## 4. 目标对象与生命周期

两个构造函数都只借用目标：

- 传 `QObject *` 时，事件记录该对象；
- 传 `QAccessibleInterface *` 时，事件记录接口的可访问唯一标识及关联对象。

两者都不转移对象或接口的所有权。`QAccessibleInterface *` 已经可用时可以避免再次查找接口；普通控件代码通常直接传 `this` 更自然。

事件是不可复制对象，应在栈上创建并在调用 `QAccessible::updateAccessibility(&event)` 的过程中保持有效。调用后不要假设平台长期保存了该 C++ event 指针，也不要在目标对象销毁后复用事件。

## 5. 逐项 API 说明

### `explicit QAccessibleAnnouncementEvent(QObject *object, const QString &message)`

构造一个目标为 `object` 的 announcement，事件类型固定为 `QAccessible::Announcement`，优先级默认 `Polite`。

`object` 必须有效；消息是按值保存的 `QString`，调用后可以销毁或修改原始字符串。若目标是普通 QObject 或 QWidget，这个重载通常更方便。

### `explicit QAccessibleAnnouncementEvent(QAccessibleInterface *iface, const QString &message)`

构造一个目标为 `iface` 的 announcement，默认优先级同样为 `Polite`。适合实现自定义 accessible interface 的代码已经持有接口时使用。

`iface` 必须有效。该构造不会让 event 拥有 interface；不要在事件仍要使用时销毁或解除注册该接口。

### `~QAccessibleAnnouncementEvent() override`

虚析构函数。析构只释放事件自己的消息与基类状态，不会销毁目标 QObject、accessible interface 或其缓存条目。

### `QString message() const`

返回要播报的消息副本。消息应描述用户真正需要知道的结果，例如“下载完成”或“名称不能为空”；不要用内部错误码、无上下文缩写或重复的控件名称填充它。

空消息通常没有有效播报价值，调用方应在创建事件前避免这种情况。

### `QAccessible::AnnouncementPoliteness politeness() const`

返回当前播报优先级。默认是 `Polite`。

### `void setPoliteness(QAccessible::AnnouncementPoliteness politeness)`

设置播报请求的优先级。应在调用 `QAccessible::updateAccessibility()` 前完成设置；修改一个已经发送的栈上事件不会改变已提交的通知。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 构造 | `QAccessibleAnnouncementEvent(QObject *, QString)` | 为 QObject 创建播报请求。 | 目标只借用；默认 `Polite`。 |
| 构造 | `QAccessibleAnnouncementEvent(QAccessibleInterface *, QString)` | 为已知 accessible interface 创建播报请求。 | 不拥有 interface；它必须保持有效。 |
| 生命周期 | `~QAccessibleAnnouncementEvent()` | 销毁事件。 | 不销毁目标对象或接口。 |
| 查询 | `message()` | 返回播报消息。 | 应简洁、用户可理解且非空。 |
| 查询 | `politeness()` | 返回当前优先级。 | 默认 `Polite`。 |
| 设置 | `setPoliteness(...)` | 修改 `Polite` 或 `Assertive`。 | 必须在提交事件前设置；`Assertive` 仅限紧急场景。 |
| 提交 | `QAccessible::updateAccessibility(&event)` | 把事件通知给可访问性后端。 | 状态改变后发送；不保证每个平台都会播报。 |

### 一句话总结

`QAccessibleAnnouncementEvent` 用于让辅助技术播报界面中难以从普通状态变化推断的消息：默认礼貌播报，真正紧急才使用 `Assertive`，并始终在 UI 状态已经更新后通过 `QAccessible::updateAccessibility()` 提交。
