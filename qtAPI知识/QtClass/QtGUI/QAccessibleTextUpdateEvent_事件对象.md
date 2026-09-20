# QAccessibleTextUpdateEvent：通知一段文本被替换

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleTextUpdateEvent>`  
> 模块：Qt GUI，链接 `Qt6::Gui`  
> 继承：`QAccessibleTextCursorEvent`

## 它解决什么问题

一次替换并不是“只插入”或“只删除”：在同一个起点，旧文本被移除，新文本写入。`QAccessibleTextUpdateEvent` 把这两个事实放进一个通知，使辅助技术能够正确更新自身文本缓存，而不必把它猜成两次无关操作。

它在构造后使用 `QAccessible::TextUpdated` 事件类型。该对象不执行替换，调用方仍要先修改真正的文档或文本缓冲区。

## 常见使用场景

选中文本后键入新内容、查找替换、自动格式化替换一段字符、完成输入法候选词替换预编辑文本，都可能是“以新文本替换旧文本”的单一操作。

```cpp
#include <QAccessible>
#include <QAccessibleTextUpdateEvent>

void CodeEditor::replaceAccessibleText(
    int position, int oldLength, const QString &newText)
{
    const QString oldText = m_buffer.mid(position, oldLength);
    m_buffer.replace(position, oldLength, newText); // 先更新模型
    m_caretPosition = position + newText.size();

    QAccessibleTextUpdateEvent event(this, position, oldText, newText);
    QAccessible::updateAccessibility(&event);
}
```

若控件确实把删除和插入作为彼此独立、可感知的操作，才分别发送 `QAccessibleTextRemoveEvent` 和 `QAccessibleTextInsertEvent`。对于原子替换，使用本类更准确。

## 事件载荷如何理解

`changePosition()` 是替换发生的起点。

- `textRemoved()` 返回旧文本，即替换前从起点移除的片段。
- `textInserted()` 返回新文本，即随后从同一位置写入的片段。
- 继承的 `cursorPosition()` 在构造时设为 `position + text.size()`，因此是新文本末尾之后的默认插入点位置。

上述位置都是逻辑文本字符位置，必须匹配该控件的 `QAccessibleTextInterface`。它们不是 UTF-8 字节数、屏幕列或像素坐标。Qt 不会核验 `oldText` 是否真是现有文本，也不会检查 `position` 是否越界，应用必须确保事件所述变更可以从当前可访问文本状态得到验证。

## 生命周期和顺序

两种构造函数分别接受 `QObject *` 与 `QAccessibleInterface *`，但事件均不拥有目标。推荐在状态更新后创建局部事件，并立即用 `QAccessible::updateAccessibility()` 发送。

文本与选区、光标经常同时变化。实际控件应先让自己的可访问接口反映最终状态；再根据对外需要报告替换、选区或光标事件。不要依赖 `QAccessibleTextUpdateEvent` 自动同步这些状态，它只保存构造时的值。

## API 逐项说明

### 构造函数

`QAccessibleTextUpdateEvent(QAccessibleInterface *iface, int position, const QString &oldText, const QString &text)` 和对象版本描述一次替换：从 `position` 删除 `oldText`，并插入 `text`。

- `type()` 为 `QAccessible::TextUpdated`。
- `changePosition()` 为 `position`。
- `textRemoved()` 为 `oldText`。
- `textInserted()` 为 `text`。
- `cursorPosition()` 初始化为 `position + text.size()`。

### `changePosition() const`

返回替换起点。它不是新插入点的别名。

### `textRemoved() const` 与 `textInserted() const`

分别返回旧文本和新文本副本。两者可以长度不同，也可以其中之一为空；空旧文本在语义上接近插入，空新文本接近删除，但仍应按真实编辑操作选择合适的事件类型。

## API 速查表

| API | 含义 | 重点边界 |
| --- | --- | --- |
| `QAccessibleTextUpdateEvent(QAccessibleInterface *iface, int position, const QString &oldText, const QString &text)` | 为接口描述一次文本替换。 | 目标接口在分发期间必须有效。 |
| `QAccessibleTextUpdateEvent(QObject *object, int position, const QString &oldText, const QString &text)` | 为对象描述替换。 | Qt 不校验旧文本和当前模型是否一致。 |
| `int changePosition() const` | 取得替换起点。 | 不等同于默认的更新后光标位置。 |
| `QString textRemoved() const` | 取得替换前移除的文本。 | 返回片段副本，不是旧全文。 |
| `QString textInserted() const` | 取得替换后插入的文本。 | 返回片段副本，不是新全文。 |
| 继承的 `cursorPosition() const` | 取得替换后的默认插入点。 | 构造时为 `position + text.size()`。 |
| 继承的 `setCursorPosition(int)` | 改写事件中附带的光标位置。 | 不会修改控件或验证范围。 |
| 配套调用 `QAccessible::updateAccessibility(QAccessibleEvent *)` | 分发替换通知。 | 先更新可访问文本状态，随后立即调用。 |
