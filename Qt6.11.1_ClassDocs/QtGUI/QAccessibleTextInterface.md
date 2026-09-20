# QAccessibleTextInterface

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleTextInterface`

## 1. 先建立直觉

`QAccessibleTextInterface` 是辅助技术读取和导航文本的核心协议。它回答的问题包括：文本有多长、光标在哪里、某个屏幕点对应哪个字符、某个字符矩形在哪里、当前有哪些选区、按单词或行边界应读哪一段。

它不仅适用于可编辑控件，也适用于长文本、代码编辑器、终端、富文本视图和能选择文本的自绘控件。若文本还可被辅助技术修改，应额外实现 `QAccessibleEditableTextInterface`。

## 2. 类说明

- 头文件：`#include <QAccessibleTextInterface>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 来源类：可访问子接口；通过 `QAccessibleInterface::textInterface()` 获取。
- 坐标规则：字符矩形和点命中使用屏幕坐标。
- 区间规则：文本范围采用半开区间 `[startOffset, endOffset)`。

偏移量必须和组件自己的文本模型一致。它不是 UTF-8 字节偏移，也不应混用屏幕列号、行号或 QTextBlock 局部位置。

## 3. API 速查

| API | 用途 |
|---|---|
| `characterCount()` | 返回文本总长度。 |
| `text(start, end)` | 返回半开区间中的文本。 |
| `cursorPosition()` / `setCursorPosition()` | 查询或移动插入光标。 |
| `characterRect(offset)` | 返回指定字符的屏幕矩形。 |
| `offsetAtPoint(point)` | 将屏幕点映射到文本偏移。 |
| `attributes(offset, &start, &end)` | 查询某位置文本属性及其适用范围。 |
| `selectionCount()` | 返回选区数量。 |
| `selection(index, &start, &end)` | 查询第 `index` 个选区。 |
| `addSelection(start, end)` | 添加或替换选区。 |
| `setSelection(index, start, end)` | 修改某个选区。 |
| `removeSelection(index)` | 移除某个选区。 |
| `scrollToSubstring(start, end)` | 滚动使指定文本范围可见。 |
| `textAtOffset(offset, boundary, &start, &end)` | 返回包含 offset 的字符/词/句/段/行。 |
| `textBeforeOffset(...)` / `textAfterOffset(...)` | 返回指定边界前后相邻文本片段。 |

## 4. 关键用法

### 半开区间是所有文本操作的底线

```cpp
QString AccessibleEditor::text(int start, int end) const
{
    start = qBound(0, start, characterCount());
    end = qBound(start, end, characterCount());
    return editor()->plainText().mid(start, end - start);
}
```

`start` 包含，`end` 不包含。`text(0, characterCount())` 返回全文，`text(4, 4)` 返回空字符串。选区、删除、替换和滚动子串都应遵循同一约定。

### 屏幕坐标和文本偏移互相映射

```cpp
QRect AccessibleEditor::characterRect(int offset) const
{
    const QRect localRect = editor()->cursorRectForOffset(offset);
    return QRect(editor()->mapToGlobal(localRect.topLeft()), localRect.size());
}
```

`characterRect()` 返回全局屏幕坐标。`offsetAtPoint()` 接收的 `QPoint` 也是屏幕坐标。自定义控件经常把 viewport 局部坐标直接返回给辅助技术，结果会导致读屏鼠标探索和放大镜命中完全错位。

### 选区可能不止一个

```cpp
void AccessibleEditor::selection(int index, int *start, int *end) const
{
    const auto ranges = editor()->selectionRanges();
    if (index < 0 || index >= ranges.size()) {
        *start = -1;
        *end = -1;
        return;
    }

    *start = ranges[index].start;
    *end = ranges[index].end;
}
```

多数控件只有一个选区，但协议支持多个选区。代码编辑器、多光标编辑器和文字处理器尤其需要认真处理 `selectionIndex`，不能假设永远为 0。

## 5. 边界文本查询

| 边界类型 | 典型用途 |
|---|---|
| `CharBoundary` | 逐字符朗读、精确移动。 |
| `WordBoundary` | Ctrl+方向、按词朗读。 |
| `SentenceBoundary` | 语音阅读长段落。 |
| `ParagraphBoundary` | 段落导航。 |
| `LineBoundary` | 屏幕行或布局行导航。 |
| `NoBoundary` | 返回全文或按实现约定的大范围文本。 |

`textAtOffset()`、`textBeforeOffset()`、`textAfterOffset()` 的默认实现适合小文本；大型文档、代码编辑器和分页文本应提供高效实现。Qt 文档约定 `offset == -1` 表示文本末尾；`offset == -2` 按约定表示调用方希望使用当前光标位置，自定义实现应先解析成实际光标位置再处理。

## 6. 使用场景

| 场景 | 实现重点 |
|---|---|
| 自定义单行输入框 | 光标、单选区、点命中和文本范围。 |
| 代码编辑器 | 多行布局、滚动、选择、按词/行边界查询。 |
| 富文本视图 | 属性范围、链接/格式边界、字符矩形。 |
| 终端 | 逻辑文本与屏幕缓冲区坐标映射。 |
| 文档阅读器 | 段落、句子、页面可见性和高效边界查询。 |

## 7. 常见坑与经验

- `selection()` 失败时应把输出偏移设为无效值，而不是留下调用方传入的旧值。
- `attributes()` 返回的字符串应稳定描述格式属性，并通过 start/end 告诉属性连续适用范围；不要只返回当前字符信息。
- `scrollToSubstring()` 应滚动到逻辑范围，而不是只移动光标；只移动光标会改变用户编辑状态。
- 光标位置、选区和文本变化后应发送对应无障碍事件，否则辅助技术会继续使用旧状态。
- Unicode 复杂文本要按编辑器合法光标位置处理，避免把偏移落在代理对或组合字符中间。
- 对密码文本，接口暴露策略要遵循控件安全要求，不能因为实现方便而返回真实内容。

## 8. 知识点覆盖

- 可访问文本的读取、光标、选区和范围协议
- 半开区间 `[start, end)` 与无效偏移约定
- 屏幕坐标下的字符矩形和点命中
- 字符、词、句、段、行边界查询
- 多选区、富文本属性、滚动可见性
- Unicode、输入法、密码字段和大文档性能
