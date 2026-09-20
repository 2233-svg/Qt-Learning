# QAccessibleTextCursorEvent：通知文本插入点移动

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleTextCursorEvent>`  
> 模块：Qt GUI，链接 `Qt6::Gui`  
> 继承：`QAccessibleEvent`

## 它解决什么问题

文本编辑器里的插入点移动，对视觉用户通常只是细窄光标换了位置；屏幕阅读器等辅助技术却需要知道新的位置，才能朗读当前字符、行或上下文。`QAccessibleTextCursorEvent` 就是这项通知的载体。

它描述的是“光标已经移动到哪里”，并不移动控件的光标，也不修改文本。应用应先完成自身的编辑状态更新，再创建事件并交给 `QAccessible::updateAccessibility()` 分发。

这个类对应的事件类型固定为 `QAccessible::TextCaretMoved`。

## 典型场景

- 自绘代码编辑器实现了自己的光标、文本缓冲区和 `QAccessibleTextInterface`。
- 富文本或文档控件没有使用 Qt 已提供的可访问性实现，需要补发通知。
- 输入法提交文本、键盘导航或程序调用改变了插入点，且辅助技术需要同步获知。

普通 `QLineEdit`、`QTextEdit` 等标准控件已有相应实现。业务代码通常不应为了“保险”重复发送事件，否则会造成重复播报。

## 构造、分发与生命周期

构造函数可接受 `QObject *` 或已经取得的 `QAccessibleInterface *`。前者适合控件对象仍然存在的常见情形；后者适用于实现层已持有接口的场景。事件对象不拥有这两个目标。

`QAccessible::updateAccessibility()` 在当前调用中消费事件，因此通常创建栈对象即可。不要缓存事件，也不要在目标对象或接口已经失效后再分发。

```cpp
#include <QAccessible>
#include <QAccessibleTextCursorEvent>

void CodeEditor::moveCaretTo(int position)
{
    // 先更新真实的编辑器状态，并保证 position 与可访问文本使用同一坐标体系。
    m_caretPosition = position;

    QAccessibleTextCursorEvent event(this, position);
    QAccessible::updateAccessibility(&event);
}
```

`cursorPos` 和 `cursorPosition()` 使用的是文本字符位置，不是 UTF-8 字节偏移。它必须与同一对象的 `QAccessibleTextInterface` 所报告的文本位置一致。对于代理对、组合字符等情况，辅助技术看见的“一个字形”未必等于一个位置，不能把字节索引或屏幕列号直接传入。

## API 语义与边界

### 构造函数

`QAccessibleTextCursorEvent(QAccessibleInterface *iface, int cursorPos)` 和 `QAccessibleTextCursorEvent(QObject *object, int cursorPos)` 创建一个面向目标对象的插入点移动通知。

- `cursorPos` 表示新的插入点位置。
- 构造后 `type()` 为 `QAccessible::TextCaretMoved`。
- Qt 不会在构造函数中读取、修改或校验目标文本；调用方负责确保位置在自己的文本模型中有意义。

### `cursorPosition() const`

返回事件携带的新插入点位置。它只是读取载荷，不会查询控件当前的光标，因此事件创建后控件再次移动也不会改变返回值。

### `setCursorPosition(int position)`

修改事件中记录的位置。适合在事件分发前修正载荷；它不会同步修改控件，也不会重新计算任何文本状态。这个 setter 不做范围检查，传入负值或越界位置仍会被保存，错误会延后表现为辅助技术得到不一致的信息。

## 使用时容易混淆的点

- 这是可访问性事件，不是 `QEvent` 事件循环里的键盘或鼠标事件，不能通过 `QObject::event()` 截获它。
- 它表示插入点移动，不表示选区变化。选区改变应使用 `QAccessibleTextSelectionEvent`。
- 仅文本内容变化而插入点不变时，应使用插入、删除或替换事件，而不是借由光标事件暗示内容变化。
- 事件名称里的 cursor 是逻辑文本位置，不是像素坐标，也不是 `QTextCursor` 对象。

## API 速查表

| API | 含义 | 重点边界 |
| --- | --- | --- |
| `QAccessibleTextCursorEvent(QAccessibleInterface *iface, int cursorPos)` | 为可访问性接口创建光标移动通知。 | `iface` 不被事件拥有，分发前必须有效。 |
| `QAccessibleTextCursorEvent(QObject *object, int cursorPos)` | 为 `QObject` 创建光标移动通知。 | 目标对象应具有对应的可访问性实现。 |
| `int cursorPosition() const` | 取得事件记录的新插入点位置。 | 返回的是快照，不会随控件后续状态改变。 |
| `void setCursorPosition(int position)` | 改写事件的插入点位置。 | 不校验范围，也不移动真实光标。 |
| 继承的 `type()` | 读取事件类型。 | 本类构造后固定为 `QAccessible::TextCaretMoved`。 |
| 配套调用 `QAccessible::updateAccessibility(QAccessibleEvent *)` | 将事件发送给可访问性框架。 | 先更新真实状态，再立即分发短生命周期事件。 |
