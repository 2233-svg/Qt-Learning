# QAccessibleTextRemoveEvent：通知文本删除

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleTextRemoveEvent>`  
> 模块：Qt GUI，链接 `Qt6::Gui`  
> 继承：`QAccessibleTextCursorEvent`

## 它解决什么问题

文本被删除后，辅助技术需要知道删除位置和被删内容，才能更新朗读上下文、盲文显示和自身的文本缓存。`QAccessibleTextRemoveEvent` 把这次删除封装为可访问性通知。

它构造后的事件类型是 `QAccessible::TextRemoved`。这个对象不会删除任何字符，只负责描述已经写入控件文本模型的结果。

## 适合何时发送

例如自定义编辑器执行退格、Delete、剪切或批量删除时，可以在真实模型更新后发送：

```cpp
#include <QAccessible>
#include <QAccessibleTextRemoveEvent>

void CodeEditor::removeAccessibleText(int position, int length)
{
    const QString removed = m_buffer.mid(position, length);
    m_buffer.remove(position, length);
    m_caretPosition = position;

    QAccessibleTextRemoveEvent event(this, position, removed);
    QAccessible::updateAccessibility(&event);
}
```

要传入删除前保存的内容。若先修改模型再去查询被删范围，通常已经取不到正确的 `text`，此时事件虽能发出，但对辅助技术没有足够的信息。

## 坐标和光标语义

`changePosition()` 是删除开始位置，`textRemoved()` 是从这个位置移除的文本。

与插入事件不同，本类继承来的 `cursorPosition()` 在构造时就是 `position`，因为删除后通常插入点停留在删除区间的起点。不要从被删文本长度推导它，直接读取该函数即可。

位置使用逻辑文本字符位置，应与该对象 `QAccessibleTextInterface` 的字符位置一致，不能使用 UTF-8 字节数、行列坐标或像素坐标。Qt 不验证 `position` 和文本长度是否对应当前模型，调用方必须保持一致。

## 目标与生命周期

构造时可传 `QObject *`，也可传 `QAccessibleInterface *`。二者的所有权都不转移到事件中。典型写法是栈上创建事件并立刻调用 `QAccessible::updateAccessibility(&event)`；不要跨异步边界保存该事件或已失效的接口指针。

一次替换操作应使用 `QAccessibleTextUpdateEvent`，以便在单个通知中同时携带旧文本和新文本。将替换拆成删除和插入只有在控件确实把它们作为两个独立编辑步骤时才合适。

## API 逐项说明

### 构造函数

`QAccessibleTextRemoveEvent(QAccessibleInterface *iface, int position, const QString &text)` 与 `QAccessibleTextRemoveEvent(QObject *object, int position, const QString &text)` 描述“从 `position` 删除 `text`”。

- `type()` 固定为 `QAccessible::TextRemoved`。
- `changePosition()` 保存 `position`。
- `textRemoved()` 保存 `text` 的副本。
- `cursorPosition()` 初始为 `position`。

### `changePosition() const`

返回删除所在的起点，不查询当前控件状态。

### `textRemoved() const`

返回被删除的文本片段。即使字符串为空，事件仍可构造，但空删除一般没有需要通知的语义，应由控件决定是否跳过。

## API 速查表

| API | 含义 | 重点边界 |
| --- | --- | --- |
| `QAccessibleTextRemoveEvent(QAccessibleInterface *iface, int position, const QString &text)` | 为接口描述从位置开始的删除。 | `iface` 必须在分发期间有效。 |
| `QAccessibleTextRemoveEvent(QObject *object, int position, const QString &text)` | 为对象描述一次删除。 | `text` 应是删除前的实际片段。 |
| `int changePosition() const` | 取得删除起点。 | 是逻辑字符位置，不是字节偏移。 |
| `QString textRemoved() const` | 取得被删除的文本副本。 | 不返回删除后的全文。 |
| 继承的 `cursorPosition() const` | 取得删除后的默认插入点位置。 | 构造时等于 `position`。 |
| 继承的 `setCursorPosition(int)` | 改写事件光标位置。 | 不会修改真实控件光标。 |
| 配套调用 `QAccessible::updateAccessibility(QAccessibleEvent *)` | 分发删除通知。 | 先完成模型变更，再发送。 |
