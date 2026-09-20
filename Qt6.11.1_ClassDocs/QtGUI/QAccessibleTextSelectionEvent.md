# QAccessibleTextSelectionEvent

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleTextSelectionEvent`

## 1. 先建立直觉

`QAccessibleTextSelectionEvent` 通知辅助技术：文本对象的选区发生了变化。它记录新的选区起点和终点，并继承光标位置能力，让读屏能知道选择结束后插入点在哪里。

它描述的是文本选区，不是列表项选择。列表、表格、图形对象的选择应使用 `QAccessibleSelectionInterface` 或表格相关接口。

## 2. 类说明

- 头文件：`#include <QAccessibleTextSelectionEvent>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QAccessibleTextCursorEvent`
- 区间规则：选区采用半开区间 `[start, end)`。

大多数控件只有一个选区，但 `QAccessibleTextInterface` 支持多个选区。这个事件表达一段新的选择范围；复杂多选区编辑器还应保证文本接口能查询完整选择列表。

## 3. API 速查

| API | 用途 |
|---|---|
| `QAccessibleTextSelectionEvent(object, start, end)` | 为 QObject 构造选区变化事件。 |
| `QAccessibleTextSelectionEvent(iface, start, end)` | 为可访问接口构造选区变化事件。 |
| `selectionStart()` | 返回选区起始文本偏移。 |
| `selectionEnd()` | 返回选区结束文本偏移。 |
| `setSelection(start, end)` | 修改事件中的选区范围。 |
| `cursorPosition()` / `setCursorPosition()` | 读取或设置事件携带的光标位置。 |

## 4. 关键用法

```cpp
void Editor::setSelection(int anchor, int cursor)
{
    const int start = qMin(anchor, cursor);
    const int end = qMax(anchor, cursor);

    document()->setSelection(start, end);

    QAccessibleTextSelectionEvent event(this, start, end);
    event.setCursorPosition(cursor);
    QAccessible::updateAccessibility(&event);
}
```

选区范围通常按从小到大的文本偏移表示，但光标位置可能位于选区起点或终点，这取决于用户拖选方向或 Shift+方向键的锚点逻辑。若方向对你的编辑器很重要，应正确设置 `cursorPosition()`。

## 5. 使用场景

| 场景 | 建议 |
|---|---|
| 用户拖选文本 | 发送选区事件，可合并高频中间变化。 |
| Shift+方向键扩展选择 | 发送选区事件并设置真实光标端。 |
| Ctrl+A 全选文本 | 范围为 `[0, characterCount())`。 |
| 清除选择但保留光标 | 可发送空范围 `[pos, pos)`。 |
| 多光标/多选区编辑器 | 事件之外，文本接口必须能返回所有选区。 |

## 6. 常见坑与经验

- `selectionEnd()` 是第一个未被选中的偏移，不是最后一个被选中字符的索引。
- 不要把视觉行列坐标当作选区偏移；选区必须与 `QAccessibleTextInterface::selection()` 一致。
- 高频拖选时不要每个鼠标移动都制造大量读屏输出；可在状态稳定时发送或按控件策略节流。
- 文本替换、删除选区时，选区事件和文本更新事件要保持顺序一致。
- 密码输入框通常不应暴露真实选中文本，但仍可表达选择范围或光标位置，具体取决于平台策略。

## 7. 知识点覆盖

- 文本选区事件与文本选择接口
- 半开区间和光标端方向
- 全选、清除选择、多选区编辑器
- 高频选择变化的事件节流
- 选区、删除和替换事件的顺序一致性
