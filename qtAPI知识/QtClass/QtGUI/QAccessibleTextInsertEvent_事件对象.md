# QAccessibleTextInsertEvent：通知文本插入

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleTextInsertEvent>`  
> 模块：Qt GUI，链接 `Qt6::Gui`  
> 继承：`QAccessibleTextCursorEvent`

## 它解决什么问题

辅助技术不能仅凭“光标变了”推断一段文本是否插入、插在何处以及插入了什么。`QAccessibleTextInsertEvent` 用位置和文本内容明确表达一次插入操作，供可访问性后端刷新朗读、盲文输出或缓存。

对象被构造时，事件类型为 `QAccessible::TextInserted`。它记录的是已经发生的变更，不会替编辑器插入字符。

## 实际使用场景

自绘文本控件在键盘输入、粘贴、自动补全、输入法提交或脚本命令后，若其 `QAccessibleTextInterface` 的文本已更新，就可以发送此事件。标准 Qt 文本控件通常自行处理，手写控件才需要主动使用。

```cpp
#include <QAccessible>
#include <QAccessibleTextInsertEvent>

void CodeEditor::insertAccessibleText(int position, const QString &text)
{
    m_buffer.insert(position, text); // 先改变真实模型
    m_caretPosition = position + text.size();

    QAccessibleTextInsertEvent event(this, position, text);
    QAccessible::updateAccessibility(&event);
}
```

## 两个位置的区别

构造参数 `position` 和 `changePosition()` 表示插入开始位置；从该位置开始，`text` 被加入文本。

继承来的 `cursorPosition()` 则被 Qt 初始化为 `position + text.size()`，即插入后的插入点位置。二者相同只会发生在插入空字符串时。读取插入起点请使用 `changePosition()`，不要误用 `cursorPosition()`。

这些值是逻辑文本字符位置，不能以 UTF-8 字节偏移代替；它们也必须和该对象 `QAccessibleTextInterface` 的位置约定一致。

## 构造、所有权与边界

可用 `QObject *` 或 `QAccessibleInterface *` 指定通知对象。事件不拥有目标，且通常应作为栈对象创建，紧接着传给 `QAccessible::updateAccessibility()`。

Qt 在构造时保存 `text` 的值，因此之后修改原 `QString` 不会影响事件。构造函数没有替应用检查 `position` 是否落在插入前文本的合法范围，也不会核对 `text` 是否真的进入了控件模型。若通知与可访问接口读到的内容不一致，辅助技术的状态会错位。

对于多次连续输入，可按实际编辑语义合并为一段插入通知；不要一方面发插入事件，另一方面又用替换事件重复描述同一修改。

## API 逐项说明

### 构造函数

`QAccessibleTextInsertEvent(QAccessibleInterface *iface, int position, const QString &text)` 与 `QAccessibleTextInsertEvent(QObject *object, int position, const QString &text)` 都描述“在 `position` 插入 `text`”。

构造后：

- `type()` 为 `QAccessible::TextInserted`。
- `changePosition()` 为 `position`。
- `textInserted()` 为 `text` 的副本。
- `cursorPosition()` 为 `position + text.size()`。

### `changePosition() const`

返回插入起点。返回值不会随真实文本后续编辑而变化。

### `textInserted() const`

返回插入的完整文本。它不是按字符逐条推送的增量，也不是插入后全文。

## API 速查表

| API | 含义 | 重点边界 |
| --- | --- | --- |
| `QAccessibleTextInsertEvent(QAccessibleInterface *iface, int position, const QString &text)` | 为接口描述从 `position` 开始的文本插入。 | 事件不拥有 `iface`；先更新真实文本。 |
| `QAccessibleTextInsertEvent(QObject *object, int position, const QString &text)` | 为对象描述一次文本插入。 | `position` 是逻辑字符位置，不是 UTF-8 字节位置。 |
| `int changePosition() const` | 取得插入起点。 | 不等同于默认的插入后光标位置。 |
| `QString textInserted() const` | 取得插入的文本副本。 | 返回的是插入片段，不是控件全部文本。 |
| 继承的 `cursorPosition() const` | 取得插入后的默认插入点位置。 | 构造时为 `position + text.size()`。 |
| 继承的 `setCursorPosition(int)` | 手动修改事件记录的光标位置。 | 不修改实际控件状态。 |
| 配套调用 `QAccessible::updateAccessibility(QAccessibleEvent *)` | 分发插入通知。 | 事件通常只在此次同步调用中使用。 |
