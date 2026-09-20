# QAccessibleTextInsertEvent

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleTextInsertEvent`

## 1. 先建立直觉

`QAccessibleTextInsertEvent` 通知辅助技术：某段文本已经插入到文本对象中。它不仅说明插入位置和插入内容，还继承了光标位置能力，用于告诉读屏插入后插入点在哪里。

它适合自定义文本编辑器、终端输入区、富文本编辑器或代码编辑器。标准 Qt 文本控件通常已经处理这些事件，不需要应用重复发送。

## 2. 类说明

- 头文件：`#include <QAccessibleTextInsertEvent>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QAccessibleTextCursorEvent`
- 发送方式：构造后调用 `QAccessible::updateAccessibility(&event)`

构造函数默认认为光标移动到插入文本的末尾。如果你的编辑器因为自动补全、成对括号、格式化或输入法组合而将光标放在其他位置，应调用 `setCursorPosition()` 修正。

## 3. API 速查

| API | 用途 |
|---|---|
| `QAccessibleTextInsertEvent(object, position, text)` | 为 QObject 构造文本插入事件。 |
| `QAccessibleTextInsertEvent(iface, position, text)` | 为可访问接口构造文本插入事件。 |
| `changePosition()` | 返回插入发生的起始偏移。 |
| `textInserted()` | 返回本次插入的文本。 |
| `cursorPosition()` / `setCursorPosition()` | 读取或设置插入后的光标位置。 |

## 4. 关键用法

```cpp
void Editor::insertText(int position, const QString &text)
{
    document()->insert(position, text);

    QAccessibleTextInsertEvent event(this, position, text);
    event.setCursorPosition(position + text.size());
    QAccessible::updateAccessibility(&event);
}
```

事件应在文本模型已经插入成功后发送。否则辅助技术收到事件后立即查询 `QAccessibleTextInterface::text()` 时，会读到旧内容，造成“事件说插入了，但接口查不到”的不一致。

```cpp
QAccessibleTextInsertEvent event(this, pos, u"()"_s);
event.setCursorPosition(pos + 1); // 光标放在括号中间
QAccessible::updateAccessibility(&event);
```

对自动补全或成对插入，要显式设置光标位置，不能让默认“移动到插入末尾”的假设误导用户。

## 5. 使用场景

| 场景 | 建议 |
|---|---|
| 普通键入、粘贴、输入法提交 | 发送插入事件，文本为实际进入文档的内容。 |
| 自动补全插入多字符 | 插入完整文本，并设置最终光标位置。 |
| 富文本插入对象占位符 | 文本应对应可访问文本模型中的逻辑表示。 |
| 替换选区 | 可组合删除+插入事件，或使用文本更新事件表达替换。 |
| 未改变文档的预编辑文本 | 不应当作已插入正文，需按控件策略处理。 |

## 6. 常见坑与经验

- `changePosition()` 是插入前的逻辑文本偏移，不是插入后的光标位置。
- `textInserted()` 应是最终写入文档的文本，不是用户按下的键名。
- `QString::size()` 使用 UTF-16 code unit 数。若编辑器以 grapheme cluster 为边界，光标计算应使用编辑器自身合法偏移。
- 不要在输入法预编辑阶段反复发送插入事件；等文本提交到文档后再通知。
- 对密码字段要谨慎，平台和控件策略可能不应暴露插入的真实字符。

## 7. 知识点覆盖

- 文本插入事件、位置和最终光标
- 输入法、粘贴、自动补全与成对字符
- 逻辑文本模型和可访问文本接口一致性
- UTF-16 长度与编辑器文本边界
- 密码和敏感文本的暴露边界
