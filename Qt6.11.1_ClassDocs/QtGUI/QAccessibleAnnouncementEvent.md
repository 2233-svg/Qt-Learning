# QAccessibleAnnouncementEvent

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleAnnouncementEvent`

## 1. 先建立直觉

`QAccessibleAnnouncementEvent` 用于请求辅助技术播报一条临时信息。例如保存完成、筛选结果数量变化、后台任务失败或表单验证提示。它不会改变控件本身的 Name、Value 或 Description，而是补充一条“现在应让用户听到”的消息。

公告适合反馈重要但不一定有焦点移动的变化；它不应成为每次重绘、鼠标悬停或计时器更新的旁白。

## 2. 类说明

- 头文件：`#include <QAccessibleAnnouncementEvent>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QAccessibleEvent`
- 版本：公告事件和 `AnnouncementPoliteness` 在 Qt 6.8 引入。
- 发送方式：构造事件后调用 `QAccessible::updateAccessibility(&event)`。

事件关联一个 `QObject` 或 `QAccessibleInterface`，使平台知道这条消息属于哪一个可访问对象。

## 3. API 速查

| API | 用途 |
|---|---|
| `QAccessibleAnnouncementEvent(object, message)` | 以 QObject 为来源构造公告，默认 `Polite`。 |
| `QAccessibleAnnouncementEvent(iface, message)` | 以可访问接口为来源构造公告。 |
| `message()` | 读取要播报的消息。 |
| `politeness()` | 读取播报优先级。 |
| `setPoliteness(value)` | 设置 `Polite` 或 `Assertive`。 |
| `QAccessible::updateAccessibility()` | 将事件提交给平台辅助技术。 |

## 4. 关键用法

```cpp
void SearchPanel::showResultCount(int count)
{
    resultLabel->setText(tr("%n result(s)", nullptr, count));

    QAccessibleAnnouncementEvent event(
        resultLabel, tr("%n result(s) found", nullptr, count));
    QAccessible::updateAccessibility(&event);
}
```

默认 `Polite` 会让读屏在合适的间隙播报，不应打断用户正在输入或阅读的内容。它适用于普通完成信息、搜索结果和非紧急状态变化。

```cpp
QAccessibleAnnouncementEvent event(
    passwordField, tr("Password must contain at least 12 characters"));
event.setPoliteness(QAccessible::AnnouncementPoliteness::Assertive);
QAccessible::updateAccessibility(&event);
```

`Assertive` 会要求立即播报，可能打断当前朗读。仅适合需要用户立刻处理的错误、危险或会阻止任务继续的反馈。

## 5. 使用场景

| 场景 | 优先级建议 |
|---|---|
| 保存成功、刷新完成、结果数更新 | `Polite`。 |
| 异步加载失败但界面仍可操作 | 通常 `Polite`，同时在界面保留可见错误文本。 |
| 无法提交表单、连接中断、数据将丢失 | 根据紧急度使用 `Assertive`。 |
| 倒计时、动画帧、进度每个百分点 | 不应逐条公告；选择阶段节点或结束事件。 |
| 焦点本身已经移到错误控件 | 通常不需额外公告，避免重复朗读。 |

## 6. 常见坑与经验

- 公告不是 toast 的替代品。视觉用户和辅助技术用户都需要可定位、可再次查看的反馈。
- 同一信息不要同时更改焦点、修改 Name、发送 ValueChange 再发送公告，否则读屏往往会重复朗读。
- 消息应简短、具体并本地化，例如“导出失败：没有写入权限”，而非“发生错误”。
- 事件对象通常可放在栈上；`updateAccessibility()` 调用后不要保存其地址。
- 平台可能没有活动辅助技术或对公告支持不同。核心业务反馈不能只依赖这条 API。

## 7. 知识点覆盖

- 临时无障碍公告与对象持久语义的区别
- `Polite` 和 `Assertive` 的中断策略
- 无障碍事件提交与栈对象生命周期
- 异步结果、表单错误和状态反馈设计
- 避免重复播报与公告风暴
