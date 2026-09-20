# QAccessibleTextRemoveEvent

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleTextRemoveEvent`

## 1. 先建立直觉

`QAccessibleTextRemoveEvent` 通知辅助技术：某段文本已经从文本对象中删除。它携带删除发生的位置、被删除的文本，以及删除后光标所在位置。

这个事件有一个实现细节很容易被忽略：删除完成后，文本模型里已经找不到被删掉的内容了，所以事件里的 `textRemoved()` 必须在删除前或删除过程中保存下来，不能事后再从文档中取。

## 2. 类说明

- 头文件：`#include <QAccessibleTextRemoveEvent>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QAccessibleTextCursorEvent`
- 发送方式：构造后调用 `QAccessible::updateAccessibility(&event)`

默认光标位置为删除起点 `position`。若编辑器删除后把光标放在其他位置，应调用 `setCursorPosition()` 调整。

## 3. API 速查

| API | 用途 |
|---|---|
| `QAccessibleTextRemoveEvent(object, position, text)` | 为 QObject 构造删除事件。 |
| `QAccessibleTextRemoveEvent(iface, position, text)` | 为可访问接口构造删除事件。 |
| `changePosition()` | 返回删除发生的起始偏移。 |
| `textRemoved()` | 返回本次删除的文本。 |
| `cursorPosition()` / `setCursorPosition()` | 读取或设置删除后的光标位置。 |

## 4. 关键用法

```cpp
void Editor::deleteRange(int start, int end)
{
    const QString removed = document()->text(start, end);
    document()->remove(start, end - start);

    QAccessibleTextRemoveEvent event(this, start, removed);
    event.setCursorPosition(start);
    QAccessible::updateAccessibility(&event);
}
```

事件要在文档状态已经改变后发送，但被删除文本要在删除前保存。否则辅助技术收到事件后无法得知到底删掉了哪些字符。

## 5. 使用场景

| 场景 | 建议 |
|---|---|
| Backspace / Delete 删除字符 | 发送删除事件，文本为实际删除内容。 |
| 删除选区 | `position` 为选区起点，`textRemoved()` 为整段选中文本。 |
| 剪切文本 | 发送删除事件；剪贴板变化是另一个语义。 |
| 替换文本 | 可用删除+插入，或用 `QAccessibleTextUpdateEvent` 表达一次替换。 |
| 清空文档 | 范围很大时仍应提供被删内容或选择更合适的重置/更新策略。 |

## 6. 常见坑与经验

- `changePosition()` 是删除前文本中的起始偏移；删除后同一位置通常对应后续文本。
- 不要把删除键名当作 `textRemoved()`；应传入真实被移除文本。
- 删除合成字符、表情或复杂脚本文本时，范围应落在合法文本边界上。
- 密码字段或敏感内容不应无条件暴露真实删除文本。
- 如果删除导致选区变化，也要考虑发送文本选区事件或确保文本接口查询到最新选区。

## 7. 知识点覆盖

- 文本删除事件的位置、内容和最终光标
- 删除前保存被删文本的必要性
- 删除、剪切、替换与选区的事件选择
- Unicode 文本边界和敏感文本保护
- 与 `QAccessibleTextInterface` 状态查询的一致性
