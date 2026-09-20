# QAccessibleTextInterface：让辅助技术按文本模型读取和操作控件

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleTextInterface>`  
> 模块：Qt GUI，链接 `Qt6::Gui`  
> 类型：抽象接口，通常与 `QAccessibleInterface` 一起实现

## 它解决什么问题

一个普通标签只要通过 `QAccessibleInterface::text(QAccessible::Name)` 给出名称即可；但编辑器、终端、富文本阅读器等控件需要让屏幕阅读器逐字、逐词、逐行读取，获取选择范围和插入点，并把某段文字滚动到可见区域。`QAccessibleTextInterface` 为这类需求定义统一的文本访问契约。

它对应 IAccessibleText 风格的能力。控件的可访问性对象通常既实现 `QAccessibleInterface`，又实现本接口，供平台的辅助技术后端查询。`QLineEdit` 是 Qt 中的一个实现例子。

这是纯虚接口，不能直接实例化。它也不是文本编辑引擎：实现者需要把调用映射到控件已有的文本模型、选择、插入点、布局和滚动逻辑。

## 何时应该实现

适合实现本接口的控件通常具有以下特征：

- 显示的文本超过一个静态名称，用户可能按行、词或句朗读。
- 支持插入点、选择、键盘输入或程序化的文本导航。
- 能够把逻辑文本位置映射到屏幕矩形，并反向根据屏幕点位定位字符。

纯展示型短标签通常不要实现它，应只作为普通可访问对象返回名称。反过来，若编辑器实现了接口却只返回全部字符串，无法正确报告范围、几何和选择，辅助技术体验仍会失效。

## 最重要的统一约定

### 偏移量是半开区间

涉及范围的 API 统一应按 `[startOffset, endOffset)` 实现：`startOffset` 是包含的第一个字符，`endOffset` 是不包含的第一个字符。因此长度为 `endOffset - startOffset`。这同样适用于 `text()` 和 `addSelection()`。

所有偏移量必须基于同一份逻辑文本。不要混用 UTF-8 字节偏移、视觉列号和文档模型位置；含代理对或组合字符的文本尤其容易出错。`characterCount()`、`text()`、选择、光标、事件和几何映射必须彼此可逆且相互一致。

### 坐标是屏幕坐标

`characterRect()` 返回屏幕坐标中的字符矩形，`offsetAtPoint()` 接收的也应是屏幕坐标。不能直接把控件局部坐标、视口坐标或 `QMouseEvent::position()` 原样当作屏幕点位。

### 状态变化要真实生效

`setCursorPosition()`、选择操作和 `scrollToSubstring()` 是辅助技术主动请求控件执行动作的入口，不是只修改一份可访问性缓存。实现后应更新真实控件状态，并按需要发送相应的可访问性通知。

## 文本边界查询的特殊值

`textBeforeOffset()`、`textAtOffset()`、`textAfterOffset()` 按 `QAccessible::TextBoundaryType` 查询字符、词、句、段、行或无边界的文本单元。

这三个函数的基类实现只适合小型文本编辑控件，并且不区分段落和行。富文本编辑器、代码编辑器、虚拟化文档视图应重写为高效且符合自身分行规则的实现。

需要特别遵守两个约定：

- `offset == -2` 表示“以当前光标位置作为 offset”。实现应先转换成 `cursorPosition()`，不能把 `-2` 当作普通索引。
- `offset == -1` 表示文本长度。自定义实现应等价于收到 `characterCount()`。

若不存在对应文本单元，返回空字符串；发生错误时把 `startOffset`、`endOffset` 写为 `-1`。这两个输出指针由调用方提供，调用方可能只关心字符串，但实现者仍应在可写时保持它们与返回片段一致。

## 实现时的常见场景

一个自定义代码编辑器可以将内部缓冲区和布局结果适配到接口：

```cpp
// 设计目标，而不是可直接实例化的完整类。
QString MyAccessibleEditor::text(int start, int end) const
{
    return editor()->documentText().mid(start, end - start);
}

QRect MyAccessibleEditor::characterRect(int offset) const
{
    return editor()->characterScreenRect(offset);
}
```

真正的实现还必须覆盖所有纯虚函数，并处理范围边界、滚动位置和选择状态。仅复制这两个函数不足以构成可用接口。

## API 逐项说明

### 选择操作

`selectionCount()` 返回选区数；简单编辑控件通常只有编号为 `0` 的一个选区，多选文本工具可支持更多。`selection()` 读取指定编号的 `[startOffset, endOffset)`，`addSelection()` 新增选择，`setSelection()` 替换指定选择，`removeSelection()` 清除指定选择。

对于不支持多选的控件，`addSelection()` 应替换原有选区，这是 Qt 文档明确要求的行为。实现者要校验 `selectionIndex` 和范围，不能让无效索引破坏选择状态。

### 文本与属性

`text()` 返回半开区间内的文本，`characterCount()` 返回总长度，空格也计入。`attributes()` 返回某一位置的文本属性，并通过输出参数返回该属性连续生效的半开范围。属性字符串的格式应与所服务的平台可访问性后端兼容，不能把应用私有的未约定格式直接泄露出去。

### 光标、几何与可见性

`cursorPosition()` 和 `setCursorPosition()` 读写真实插入点。`characterRect()` 将字符偏移映射到屏幕矩形，`offsetAtPoint()` 执行反向映射。`scrollToSubstring()` 必须确保指定片段在用户可见区域中，而不是只改变一个逻辑滚动值。

## API 速查表

| API | 含义 | 实现重点 |
| --- | --- | --- |
| `virtual ~QAccessibleTextInterface()` | 虚析构函数。 | 通过接口销毁派生对象时必须安全；接口本身不规定文本模型所有权。 |
| `void selection(int selectionIndex, int *startOffset, int *endOffset) const` | 读取指定选区范围。 | 返回的范围应与 `text()` 相同地采用半开区间；校验索引。 |
| `int selectionCount() const` | 返回当前选区数量。 | 普通单选控件通常为 `0` 或 `1`。 |
| `void addSelection(int startOffset, int endOffset)` | 选择一个范围。 | 多选控件追加，单选控件替换旧选区；范围为 `[start, end)`。 |
| `void removeSelection(int selectionIndex)` | 清除指定选区。 | 不应改变其他选区；无效索引需安全处理。 |
| `void setSelection(int selectionIndex, int startOffset, int endOffset)` | 改写指定选区。 | 更新真实控件状态，并保持索引和范围一致。 |
| `int cursorPosition() const` | 返回当前插入点位置。 | 返回值必须与事件和文本范围使用同一坐标体系。 |
| `void setCursorPosition(int position)` | 移动真实插入点。 | 需要处理范围限制和必要的状态通知。 |
| `QString text(int startOffset, int endOffset) const` | 取得一段文本。 | `endOffset` 是第一个不返回的字符。 |
| `QString textBeforeOffset(int offset, TextBoundaryType, int *start, int *end) const` | 取得 offset 前的边界文本单元。 | 支持 `-2` 代表光标、`-1` 代表文本末尾；错误时输出 `-1`。 |
| `QString textAtOffset(int offset, TextBoundaryType, int *start, int *end) const` | 取得包含 offset 的边界文本单元。 | 富文本或大文档应重写默认实现。 |
| `QString textAfterOffset(int offset, TextBoundaryType, int *start, int *end) const` | 取得 offset 后的边界文本单元。 | 不存在单元时返回空字符串。 |
| `int characterCount() const` | 返回文本总长度。 | 空格计入；必须和所有偏移量边界相符。 |
| `QRect characterRect(int offset) const` | 取得一个字符的屏幕矩形。 | 返回屏幕坐标，不是控件局部坐标。 |
| `int offsetAtPoint(const QPoint &point) const` | 取得屏幕点位对应的字符偏移。 | 输入是屏幕坐标，应与 `characterRect()` 互相一致。 |
| `void scrollToSubstring(int startIndex, int endIndex)` | 让一段文本进入可见区域。 | 应滚动真实视图，且正确处理跨行、折行和范围边界。 |
| `QString attributes(int offset, int *startOffset, int *endOffset) const` | 取得位置处的文本属性及其连续范围。 | 属性范围与字符串必须一致，输出范围使用半开区间。 |
