# QAccessibleTextUpdateEvent

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleTextUpdateEvent`

## 1. 先建立直觉

`QAccessibleTextUpdateEvent` 用于描述一次文本替换：从某个位置移除 `oldText`，再插入 `text`。它比“先删除再插入”更紧凑，适合自动更正、替换选区、格式化重写、输入法提交后替换预编辑内容等场景。

事件携带旧文本和新文本，辅助技术可以据此朗读“某段内容被替换为另一段内容”，而不必把两个孤立事件自行拼起来。

## 2. 类说明

- 头文件：`#include <QAccessibleTextUpdateEvent>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QAccessibleTextCursorEvent`
- 语义：在 `position` 处，`oldText` 被删除，`text` 被插入。

更新事件仍要和最终文本模型一致。发送事件后，`QAccessibleTextInterface::text()` 应能查询到替换完成后的新内容。

## 3. API 速查

| API | 用途 |
|---|---|
| `QAccessibleTextUpdateEvent(object, position, oldText, text)` | 为 QObject 构造文本替换事件。 |
| `QAccessibleTextUpdateEvent(iface, position, oldText, text)` | 为可访问接口构造文本替换事件。 |
| `changePosition()` | 返回替换发生的起始偏移。 |
| `textRemoved()` | 返回被替换掉的旧文本。 |
| `textInserted()` | 返回替换后的新文本。 |
| `cursorPosition()` / `setCursorPosition()` | 读取或设置更新后的光标位置。 |

## 4. 关键用法

```cpp
void Editor::replaceRange(int start, int end, const QString &replacement)
{
    const QString oldText = document()->text(start, end);
    document()->replace(start, end - start, replacement);

    QAccessibleTextUpdateEvent event(this, start, oldText, replacement);
    event.setCursorPosition(start + replacement.size());
    QAccessible::updateAccessibility(&event);
}
```

`oldText` 必须来自替换前的文档。若替换后再读取，就只能拿到新文本，辅助技术会失去“原来是什么”的信息。

## 5. 使用场景

| 场景 | 建议 |
|---|---|
| 自动更正 “teh” -> “the” | 使用更新事件，old/new 都明确。 |
| 粘贴覆盖选区 | 使用更新事件或删除+插入；更新事件上下文更完整。 |
| 输入法提交替换预编辑区域 | 使用更新事件，注意最终光标位置。 |
| 批量格式化整个文档 | 若替换范围很大，考虑是否需要更高层重置或分块通知。 |
| 只改变字体/颜色不改变文本 | 不使用文本更新事件；应更新属性或状态。 |

## 6. 常见坑与经验

- `textRemoved()` 和 `textInserted()` 都是逻辑文本，不是显示 glyph 或按键名称。
- 如果新旧文本相同但属性变化，不应发送文本更新；应通过文本属性或对象状态变化表达。
- 替换后选区通常会改变，必要时再发送选区事件或保证文本接口返回最新选择。
- 对非常长的替换文本要避免过度频繁发送，尤其是实时格式化器和协同编辑场景。
- 处理 Unicode 复杂文本时，`position` 和文本长度应遵循编辑器合法文本边界。

## 7. 知识点覆盖

- 文本替换事件的 old/new 语义
- 替换前保存旧文本和替换后查询新模型
- 自动更正、粘贴覆盖、输入法提交
- 更新事件与删除/插入事件的取舍
- 光标、选区和属性变化的同步
