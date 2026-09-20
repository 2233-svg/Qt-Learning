# Qt QTextEdit 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QTextEdit>`
> 所属模块：`Qt6::Widgets`
> 继承：`QAbstractScrollArea -> QTextEdit`
> 常见搭档：`QTextDocument`、`QTextCursor`、`QTextCharFormat`

## 1. QTextEdit 解决什么问题

`QTextEdit` 是 Qt 里通用的富文本编辑器。它不只会显示文字，还能处理段落、字体、颜色、对齐、图片、HTML、Markdown、选区格式和光标格式。

它适合放在：

- 富文本编辑器；
- 说明文档编辑器；
- 邮件正文编辑；
- 富文本便签；
- 需要让用户编辑带格式内容的窗口。

和 `QPlainTextEdit` 的分界线很清楚：

- `QPlainTextEdit` 偏向大文本、日志、纯文本；
- `QTextEdit` 偏向格式、排版和可编辑富文本。

如果你的内容不只是“字”，而是“字加样式”，通常就该选它。

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 一个富文本编辑器窗口

```cpp
#include <QApplication>
#include <QTextEdit>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QTextEdit edit;
    edit.setHtml("<h1>Hello</h1><p><b>Qt</b> text edit.</p>");
    edit.show();

    return app.exec();
}
```

### 2.3 用 Markdown 初始化

```cpp
edit.setMarkdown("# Title\n\n- one\n- two");
```

如果你希望内容更接近文档写作体验，`setMarkdown()` 很顺手；如果你要精确控制段落和样式，`setHtml()` 更直接。

## 3. 先理解它的文档模型

### 3.1 QTextDocument 是核心

`QTextEdit` 自己并不直接存“富文本字符串”，真正承载内容的是 `QTextDocument`。这意味着它的很多能力都来自文档对象：

- 撤销/重做；
- 选择和光标；
- 段落格式；
- 字符格式；
- 图片和资源加载；
- HTML / Markdown 转换。

### 3.2 光标比字符串索引更重要

富文本编辑器里真正做编辑操作的对象通常是 `QTextCursor`。它决定了插入位置、选区、移动方向和格式应用范围。

```cpp
QTextCursor cursor = edit.textCursor();
cursor.insertText("Hello");
edit.setTextCursor(cursor);
```

### 3.3 格式状态是编辑器的一部分

`fontPointSize()`、`currentFont()`、`textColor()`、`alignment()`、`currentCharFormat()` 这些函数说明 `QTextEdit` 不是只处理文本内容，还处理“当前将要输入的样式”。

## 4. 常用操作怎么理解

### 4.1 文本入口

```cpp
edit.setPlainText("plain");
edit.setHtml("<b>rich</b>");
edit.setMarkdown("**md**");
edit.setText("text");
```

- `setPlainText()`：纯文本；
- `setHtml()`：HTML；
- `setMarkdown()`：Markdown；
- `setText()`：由 Qt 按内容判断合适的文本形式。

### 4.2 插入和追加

```cpp
edit.insertPlainText("abc");
edit.insertHtml("<i>abc</i>");
edit.append("next paragraph");
```

`append()` 会按段落语义追加，适合邮件正文或说明文档；`insertHtml()` 适合局部富文本插入。

### 4.3 选区和高亮

```cpp
QTextEdit::ExtraSelection sel;
sel.cursor = edit.textCursor();
sel.format.setBackground(Qt::yellow);
edit.setExtraSelections({sel});
```

`ExtraSelection` 适合做搜索高亮、当前行高亮、错误标记，而不是真正修改文档内容。

### 4.4 自动格式化

`AutoFormatting` 主要用来做自动项目符号等行为。它更像编辑器辅助，而不是排版引擎的全部能力。

### 4.5 锚点和资源

```cpp
edit.scrollToAnchor("chapter-2");
edit.loadResource(QTextDocument::ImageResource, QUrl("image.png"));
```

这让 `QTextEdit` 可以支持文档内跳转、图片资源和自定义资源加载。

## 5. 什么时候用 QTextEdit

- 需要用户编辑有样式的内容；
- 需要支持 HTML 或 Markdown；
- 需要局部格式设置；
- 需要高亮、锚点、图片和自定义资源；
- 需要更完整的富文本编辑体验。

如果只是显示文本而不编辑，`QTextBrowser` 往往更合适；
如果是海量日志、纯文本源码或输出窗口，`QPlainTextEdit` 往往更合适。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QTextEdit(QWidget *parent = nullptr)` | 创建空的富文本编辑器。 | 最常见的初始化方式。 |
| 构造 | `QTextEdit(const QString &text, QWidget *parent = nullptr)` | 用初始文本创建编辑器。 | 初始文本会按富文本语义进入文档。 |
| 析构 | `~QTextEdit()` | 销毁编辑器。 | QWidget 父子对象规则负责生命周期。 |
| 属性 | `acceptRichText : bool` | 控制是否接受富文本输入。 | 只读/粘贴/编辑行为都受它影响。 |
| 属性 | `autoFormatting : AutoFormatting` | 自动格式化开关和策略。 | 常用于自动项目符号。 |
| 属性 | `cursorWidth : int` | 光标宽度。 | 影响编辑体验。 |
| 属性 | `document : QTextDocument*` | 底层文档对象。 | 富文本的核心承载者。 |
| 属性 | `documentTitle : QString` | 文档标题。 | 与窗口标题不是一回事。 |
| 属性 | `html : QString` | 当前 HTML 内容。 | 适合 HTML 显示和持久化。 |
| 属性 | `lineWrapColumnOrWidth : int` | 换行列宽或像素宽。 | 与换行模式一起看。 |
| 属性 | `lineWrapMode : LineWrapMode` | 换行模式。 | 控制是否按控件宽度换行。 |
| 属性 | `markdown : QString` | 当前 Markdown 内容。 | 从 Qt 6 的 Markdown 支持进入。 |
| 属性 | `overwriteMode : bool` | 插入/覆盖输入模式。 | 编辑器行为差异明显。 |
| 属性 | `placeholderText : QString` | 空内容时的提示文本。 | 只在空文档时可见。 |
| 属性 | `plainText : QString` | 当前纯文本。 | 只是文档内容的另一种视角。 |
| 属性 | `readOnly : bool` | 是否只读。 | 阅读器和编辑器切换时常用。 |
| 属性 | `tabChangesFocus : bool` | Tab 是插入还是切焦点。 | 表单和编辑器语义不同。 |
| 属性 | `tabStopDistance : qreal` | Tab 停靠距离。 | 排版和代码感受会变。 |
| 属性 | `textInteractionFlags : Qt::TextInteractionFlags` | 文本交互能力。 | 影响选择、编辑、链接等。 |
| 属性 | `undoRedoEnabled : bool` | 是否启用撤销/重做。 | 大量程序化写入时可调。 |
| 属性 | `wordWrapMode : QTextOption::WrapMode` | 单词级换行策略。 | 与 `lineWrapMode` 配合。 |
| 查询 | `document() const` | 获取文档对象。 | 进一步定制格式、资源和布局的入口。 |
| 修改 | `setDocument(QTextDocument *document)` | 替换底层文档。 | 要理解文档生命周期和协作关系。 |
| 查询 | `textCursor() const` | 获取当前光标。 | 用于插入、选区和格式控制。 |
| 修改 | `setTextCursor(const QTextCursor &cursor)` | 设置当前光标。 | 常和程序化编辑配合。 |
| 查询 | `currentCharFormat() const` | 当前字符格式。 | 影响后续输入样式。 |
| 修改 | `setCurrentCharFormat(const QTextCharFormat &format)` | 设置当前字符格式。 | 用于改变后续输入样式。 |
| 修改 | `mergeCurrentCharFormat(const QTextCharFormat &modifier)` | 合并当前字符格式。 | 适合局部修改。 |
| 查询 | `fontPointSize()` / `fontFamily()` / `fontWeight()` / `fontUnderline()` / `fontItalic()` | 查询当前字体状态。 | 是编辑器样式状态的一部分。 |
| 查询 | `textColor() const` / `textBackgroundColor() const` | 查询当前文字颜色状态。 | 常用于格式工具栏。 |
| 查询 | `currentFont() const` | 当前字体。 | 与字符格式配合。 |
| 查询 | `alignment() const` | 当前段落对齐方式。 | 段落格式核心属性。 |
| 修改 | `setFontPointSize()` / `setFontFamily()` / `setFontWeight()` / `setFontUnderline()` / `setFontItalic()` | 修改当前输入字体状态。 | 影响后续输入，不是只改已有文本。 |
| 修改 | `setTextColor()` / `setTextBackgroundColor()` | 修改当前输入颜色。 | 常用于富文本工具栏。 |
| 修改 | `setCurrentFont()` | 设置当前字体。 | 便于一次改多个字体属性。 |
| 修改 | `setAlignment()` | 设置段落对齐。 | 对当前段落生效。 |
| 修改 | `setPlainText()` / `setHtml()` / `setMarkdown()` / `setText()` | 设置文档内容。 | 注意各自的格式语义差异。 |
| 查询 | `toPlainText()` / `toHtml()` / `toMarkdown()` | 读取当前内容。 | 导出时最常用。 |
| 槽 | `append()` | 追加一段文本。 | 适合富文本段落追加。 |
| 槽 | `clear()` | 清空文档。 | 会清除现有内容和状态。 |
| 槽 | `copy()` / `cut()` / `paste()` | 剪贴板操作。 | 取决于编辑和选择状态。 |
| 槽 | `undo()` / `redo()` | 撤销和重做。 | 依赖文档撤销栈。 |
| 槽 | `selectAll()` | 全选。 | 导出和批量处理前常用。 |
| 槽 | `insertPlainText()` / `insertHtml()` | 从光标处插入内容。 | 比 `setText()` 更局部。 |
| 槽 | `scrollToAnchor()` | 跳到锚点。 | 文档导航常用。 |
| 槽 | `zoomIn()` / `zoomOut()` | 调整字号。 | 阅读器和编辑器都常用。 |
| 槽 | `setExtraSelections()` | 设置额外高亮。 | 适合搜索命中和当前行高亮。 |
| 查询 | `extraSelections() const` | 获取额外高亮。 | 便于同步工具栏状态。 |
| 查询 | `acceptRichText() const` | 查询是否接受富文本。 | 与编辑和粘贴行为有关。 |
| 修改 | `setAcceptRichText(bool accept)` | 开关富文本接受能力。 | 只读场景通常不需要它。 |
| 查询 | `canPaste() const` | 查询当前是否可粘贴。 | 可用于按钮启用状态。 |
| 查询 | `anchorAt(const QPoint &pos) const` | 查询鼠标位置下的锚点。 | 链接交互和提示常用。 |
| 查询 | `cursorRect()` / `cursorForPosition()` | 光标位置和鼠标位置互转。 | 自定义编辑器很常用。 |
| 查询 | `find(...)` | 查找字符串或正则。 | 文本搜索导航。 |
| 查询 | `loadResource(int type, const QUrl &name)` | 加载外部资源。 | 图片、样式和自定义资源入口。 |
| 查询 | `inputMethodQuery(...)` | 查询输入法相关信息。 | 输入法支持关键。 |
| 受保护函数 | `event(QEvent *e)` | 处理通用事件。 | 编辑器行为的总入口。 |
| 受保护函数 | `timerEvent(QTimerEvent *e)` | 处理定时器事件。 | 内部编辑节奏相关。 |
| 受保护函数 | `keyPressEvent(QKeyEvent *e)` / `keyReleaseEvent(QKeyEvent *e)` | 处理键盘输入。 | 快捷键和编辑逻辑核心。 |
| 受保护函数 | `resizeEvent(QResizeEvent *e)` | 处理尺寸变化。 | 文档重排会受影响。 |
| 受保护函数 | `paintEvent(QPaintEvent *e)` | 处理绘制。 | 自定义外观时重要。 |
| 受保护函数 | `mousePressEvent(QMouseEvent *e)` / `mouseMoveEvent(QMouseEvent *e)` / `mouseReleaseEvent(QMouseEvent *e)` / `mouseDoubleClickEvent(QMouseEvent *e)` | 处理鼠标输入。 | 选择、拖动和光标定位都在这里。 |
| 受保护函数 | `focusNextPrevChild(bool next)` / `focusInEvent(QFocusEvent *e)` / `focusOutEvent(QFocusEvent *e)` | 处理焦点。 | 输入法和键盘交互相关。 |
| 受保护函数 | `contextMenuEvent(QContextMenuEvent *e)` | 处理右键菜单。 | 可定制标准菜单。 |
| 受保护函数 | `dragEnterEvent(...)` / `dragLeaveEvent(...)` / `dragMoveEvent(...)` / `dropEvent(...)` | 处理拖放。 | 富文本粘贴和拖入图片时常用。 |
| 受保护函数 | `showEvent(QShowEvent *)` / `changeEvent(QEvent *e)` / `wheelEvent(QWheelEvent *e)` | 处理显示、状态变化和滚轮。 | 编辑器外观和滚动体验的一部分。 |
| 受保护函数 | `createMimeDataFromSelection()` / `canInsertFromMimeData()` / `insertFromMimeData()` | 控制复制和粘贴数据格式。 | 自定义粘贴和拖放时最关键。 |
| 受保护函数 | `inputMethodEvent(QInputMethodEvent *)` | 处理输入法。 | 中文输入和组合输入关键。 |
| 受保护函数 | `scrollContentsBy(int dx, int dy)` | 处理内容滚动。 | 长文档编辑和性能相关。 |
| 受保护函数 | `doSetTextCursor(const QTextCursor &cursor)` | 设置内部光标。 | 程序化编辑扩展点。 |
| 受保护函数 | `zoomInF(float range)` | 精细缩放字号。 | 一般业务层少直接碰。 |

### 一句话总结

`QTextEdit` 是富文本编辑的主力控件；它处理的不只是文字内容，还有文档结构、格式状态、资源加载和编辑交互。
