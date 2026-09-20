# Qt QPlainTextEdit 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QPlainTextEdit>`
> 所属模块：`Qt6::Widgets`
> 继承：`QAbstractScrollArea -> QPlainTextEdit`
> 常见搭档：`QTextDocument`、`QTextCursor`、`QSyntaxHighlighter`

## 1. QPlainTextEdit 解决什么问题

`QPlainTextEdit` 是专门面向纯文本的大型编辑器。它的重点不是“排版能力最强”，而是“处理大量普通文本时更轻、更快、更适合滚动”。

它适合放在：

- 日志查看器；
- 配置文本编辑器；
- 代码片段输入区；
- 需要高频追加文本的输出窗口；
- 只需要段落级格式，而不需要复杂富文本布局的编辑器。

它和 `QTextEdit` 的方向不同：`QTextEdit` 更适合富文本和复杂排版，`QPlainTextEdit` 更适合纯文本、大文档和增量追加。Qt 官方文档也明确提到，它使用的是更轻量的 `QPlainTextDocumentLayout`。

你可以把它理解成：

```text
QAbstractScrollArea
  └─ QPlainTextEdit
       └─ QTextDocument + QPlainTextDocumentLayout
```

所以它背后的核心对象其实是 `QTextDocument`，而不是一个单纯的字符串缓冲区。

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 一个纯文本编辑器窗口

```cpp
#include <QApplication>
#include <QPlainTextEdit>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QPlainTextEdit edit;
    edit.setPlainText("Hello\nQt");
    edit.show();

    return app.exec();
}
```

### 2.3 一个日志窗口

```cpp
#include <QApplication>
#include <QPlainTextEdit>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QPlainTextEdit log;
    log.setReadOnly(true);
    log.setMaximumBlockCount(1000);
    log.appendPlainText("ready");
    log.show();

    return app.exec();
}
```

`setMaximumBlockCount()` 和 `appendPlainText()` 配合时，非常适合做滚动日志窗口：旧内容会被自动裁掉，避免文本无限增长。

## 3. 先理解它的文本模型

### 3.1 段落不是普通“行号”

`QPlainTextEdit` 的内部文本按 block 组织。一个 block 近似对应一段文本，而不是简单意义上的一行字符。文本换行、插入、删除和高亮，都会围绕 block 进行。

这也是为什么 `blockCount()`、`maximumBlockCount()`、`firstVisibleBlock()` 这些 API 很重要。

### 3.2 `plainText` 只是外部视角

`toPlainText()` / `setPlainText()` 只是最常见的访问方式。更底层的真实承载者是 `QTextDocument`：

```cpp
QTextDocument *doc = edit.document();
edit.setDocument(doc);
```

这说明它并不是“自己存一个 QString”，而是把文本编辑、布局和 undo/redo 交给文档对象。

### 3.3 纯文本不等于不能格式化

虽然它不支持复杂富文本，但仍然可以：

- 使用 `QSyntaxHighlighter` 做语法高亮；
- 用 `appendHtml()` 插入简单 HTML 段落；
- 用 `QTextCursor` 和 `QTextCharFormat` 做局部格式控制。

所以“纯文本”更准确地说是“不做复杂富文本布局”。

## 4. 常用操作怎么理解

### 4.1 追加、插入和清空

```cpp
edit.insertPlainText("abc");
edit.appendPlainText("next line");
edit.clear();
```

- `insertPlainText()`：从当前光标位置插入；
- `appendPlainText()`：追加到末尾，并自动处理换行；
- `clear()`：清空文本内容。

做日志时通常优先用 `appendPlainText()`，因为它更符合“持续追加”的语义。

### 4.2 选中、复制、撤销

```cpp
edit.selectAll();
edit.copy();
edit.undo();
edit.redo();
```

这些操作都围绕编辑状态展开。是否可用，取决于当前文档状态和 `readOnly`、撤销栈、选择状态等因素。

### 4.3 光标和滚动

```cpp
edit.setTextCursor(cursor);
edit.ensureCursorVisible();
edit.centerCursor();
```

- `setTextCursor()`：直接指定当前光标；
- `ensureCursorVisible()`：只保证光标可见；
- `centerCursor()`：尽量把光标滚到中间。

对于实时追加的日志窗口，`centerOnScroll` 和 `maximumBlockCount` 的组合非常实用。

## 5. 需要特别注意的几个点

### 5.1 `blockCount` 和 `maximumBlockCount`

`blockCount()` 是当前块数，`maximumBlockCount()` 是上限。设置上限后，旧块会被自动裁剪。这个功能非常适合日志窗口，但如果你做的是全文编辑器，就要谨慎使用。

### 5.2 `lineWrapMode` 和 `wordWrapMode`

`QPlainTextEdit` 提供的是纯文本换行策略。`lineWrapMode()` 决定是否按控件宽度换行，`wordWrapMode()` 决定词语如何断开。不要把它和富文本排版里的复杂布局混成一回事。

### 5.3 `tabStopDistance`

Tab 停靠距离是纯文本编辑体验的重要参数，尤其在代码编辑器里。它不是字体大小，也不是字符数本身，而是“制表符跳到下一个对齐位置”的像素距离。

### 5.4 事件钩子很多，说明它是可定制编辑器

`QPlainTextEdit` 提供了大量受保护重写点：键盘、鼠标、拖放、绘制、滚动、输入法、上下文菜单都能接进去。也就是说，它不是只给你一个黑盒文本框，而是给你一个能做定制编辑器的底座。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QPlainTextEdit(QWidget *parent = nullptr)` | 创建空的纯文本编辑器。 | 最常见的初始化方式。 |
| 构造 | `QPlainTextEdit(const QString &text, QWidget *parent = nullptr)` | 创建编辑器并初始化文本。 | 适合直接展示已有内容。 |
| 析构 | `~QPlainTextEdit()` | 销毁编辑器。 | 由 QWidget 父子关系管理常规生命周期。 |
| 属性 | `tabChangesFocus : bool` | 决定 Tab 是插入制表符还是转移焦点。 | 做表单和代码编辑器时语义不同。 |
| 属性 | `documentTitle : QString` | 文档标题。 | 影响文档元信息，不只是窗口标题。 |
| 属性 | `undoRedoEnabled : bool` | 控制是否启用撤销/重做。 | 纯日志窗口常可关闭。 |
| 属性 | `lineWrapMode : LineWrapMode` | 控制换行模式。 | 直接影响可视宽度和滚动行为。 |
| 属性 | `readOnly : bool` | 设置是否只读。 | 日志查看器通常要设为只读。 |
| 属性 | `plainText : QString` | 当前纯文本内容。 | 对应 `toPlainText()` / `setPlainText()`。 |
| 属性 | `overwriteMode : bool` | 控制插入还是覆盖输入。 | 代码编辑器里偶尔会用到。 |
| 属性 | `tabStopDistance : qreal` | 制表符停靠距离。 | 影响代码对齐体验。 |
| 属性 | `cursorWidth : int` | 光标宽度。 | 影响编辑焦点可见性。 |
| 属性 | `textInteractionFlags : Qt::TextInteractionFlags` | 控制文本交互能力。 | 只读显示和可编辑模式差异大。 |
| 属性 | `blockCount : int` | 当前 block 数量。 | 和行数近似相关。 |
| 属性 | `maximumBlockCount : int` | 限制最大 block 数。 | 做日志窗口时特别有用。 |
| 属性 | `backgroundVisible : bool` | 控制背景是否可见。 | 影响外观和高亮感知。 |
| 属性 | `centerOnScroll : bool` | 控制滚动时是否让光标居中。 | 日志窗口和长文档体验差异明显。 |
| 属性 | `placeholderText : QString` | 没内容时显示的提示文本。 | 只在空内容状态可见。 |
| 查询 | `document() const` | 获取底层 `QTextDocument`。 | 更底层的文本和布局能力从这里进入。 |
| 修改 | `setDocument(QTextDocument *document)` | 替换底层文档。 | 要理解文档所有权和布局策略。 |
| 查询 | `textCursor() const` | 获取当前光标。 | 适合做光标定位和局部编辑。 |
| 修改 | `setTextCursor(const QTextCursor &cursor)` | 设置当前光标。 | 常和查找、选中、跳转配合。 |
| 查询 | `currentCharFormat() const` | 获取当前字符格式。 | 用于局部样式处理。 |
| 修改 | `setCurrentCharFormat(const QTextCharFormat &format)` | 设置当前字符格式。 | 对纯文本编辑器也仍有意义。 |
| 修改 | `mergeCurrentCharFormat(const QTextCharFormat &modifier)` | 合并当前字符格式。 | 适合只改局部属性。 |
| 查询 | `tabChangesFocus() const` | 查询 Tab 键行为。 | 代码编辑器常会关闭。 |
| 修改 | `setTabChangesFocus(bool b)` | 设置 Tab 键行为。 | 表单界面常开，编辑器常关。 |
| 修改 | `setDocumentTitle(const QString &title)` | 设置文档标题元信息。 | 不等于直接改窗口标题。 |
| 查询 | `documentTitle() const` | 返回文档标题。 | 可用于同步标签页标题。 |
| 查询 | `isUndoRedoEnabled() const` | 查询是否启用撤销/重做。 | 通过文档对象实现。 |
| 修改 | `setUndoRedoEnabled(bool enable)` | 打开或关闭撤销/重做。 | 大量追加文本时可考虑关闭。 |
| 修改 | `setMaximumBlockCount(int maximum)` | 限制最大 block 数。 | 可能自动裁掉旧内容。 |
| 查询 | `maximumBlockCount() const` | 返回最大 block 数。 | 和 `blockCount()` 区分开。 |
| 查询 | `lineWrapMode() const` | 查询换行模式。 | 影响布局和可读性。 |
| 修改 | `setLineWrapMode(LineWrapMode mode)` | 设置换行模式。 | 长行代码通常用 `NoWrap`。 |
| 查询 | `wordWrapMode() const` | 查询单词换行策略。 | 与 `lineWrapMode` 配合看。 |
| 修改 | `setWordWrapMode(QTextOption::WrapMode policy)` | 设置单词换行策略。 | 影响英文和长词断行。 |
| 修改 | `setBackgroundVisible(bool visible)` | 控制背景是否可见。 | 更偏显示效果。 |
| 查询 | `backgroundVisible() const` | 查询背景可见性。 | 只反映当前配置。 |
| 修改 | `setCenterOnScroll(bool enabled)` | 控制滚动时光标是否居中。 | 日志窗口常用。 |
| 查询 | `centerOnScroll() const` | 查询居中滚动开关。 | 影响滚动跟随体验。 |
| 查询 | `find(...)` | 查找字符串或正则。 | 搜索定位时很实用。 |
| 槽 | `setPlainText(const QString &text)` | 设置全部纯文本。 | 会替换现有内容。 |
| 槽 | `cut()` | 剪切选中内容。 | 只在可编辑时有意义。 |
| 槽 | `copy()` | 复制选中内容。 | 只读时也可能可用。 |
| 槽 | `paste()` | 粘贴剪贴板内容。 | 取决于可编辑状态。 |
| 槽 | `undo()` | 撤销上一步编辑。 | 依赖撤销栈。 |
| 槽 | `redo()` | 重做上一步编辑。 | 依赖撤销栈。 |
| 槽 | `clear()` | 清空文本。 | 日志重置和编辑器重置都常用。 |
| 槽 | `selectAll()` | 全选文本。 | 便于批量复制或替换。 |
| 槽 | `insertPlainText(const QString &text)` | 从光标处插入纯文本。 | 适合程序化追加局部文本。 |
| 槽 | `appendPlainText(const QString &text)` | 追加纯文本并处理段落。 | 日志输出最常见。 |
| 槽 | `appendHtml(const QString &html)` | 追加简单 HTML 段落。 | 不等于完整富文本编辑器。 |
| 槽 | `centerCursor()` | 让光标尽量居中。 | 长文本滚动体验更自然。 |
| 槽 | `zoomIn(int range = 1)` | 放大字体。 | 适合阅读器和日志查看器。 |
| 槽 | `zoomOut(int range = 1)` | 缩小字体。 | 与 `zoomIn()` 对称。 |
| 受保护函数 | `event(QEvent *e)` | 处理通用事件。 | 派生时保留默认编辑行为。 |
| 受保护函数 | `timerEvent(QTimerEvent *e)` | 处理定时事件。 | 多用于内部超时和交互节奏。 |
| 受保护函数 | `keyPressEvent(QKeyEvent *e)` | 处理按键输入。 | 是定制编辑器的核心入口。 |
| 受保护函数 | `keyReleaseEvent(QKeyEvent *e)` | 处理按键释放。 | 配合快捷键和组合键逻辑。 |
| 受保护函数 | `resizeEvent(QResizeEvent *e)` | 处理尺寸变化。 | 大文档和自动布局会受影响。 |
| 受保护函数 | `paintEvent(QPaintEvent *e)` | 处理绘制。 | 自定义外观时很重要。 |
| 受保护函数 | `mousePressEvent(QMouseEvent *e)` | 处理鼠标按下。 | 光标定位和选择的入口。 |
| 受保护函数 | `mouseMoveEvent(QMouseEvent *e)` | 处理鼠标移动。 | 拖动选择时会走到这里。 |
| 受保护函数 | `mouseReleaseEvent(QMouseEvent *e)` | 处理鼠标释放。 | 结束选择和拖拽。 |
| 受保护函数 | `mouseDoubleClickEvent(QMouseEvent *e)` | 处理双击。 | 常用于选词。 |
| 受保护函数 | `focusNextPrevChild(bool next)` | 处理焦点链切换。 | Tab 行为经常会影响这里。 |
| 受保护函数 | `contextMenuEvent(QContextMenuEvent *e)` | 处理右键菜单。 | 可定制标准菜单。 |
| 受保护函数 | `dragEnterEvent(QDragEnterEvent *e)` | 处理拖入。 | 拖放支持的入口。 |
| 受保护函数 | `dragLeaveEvent(QDragLeaveEvent *e)` | 处理拖离。 | 拖放状态收尾。 |
| 受保护函数 | `dragMoveEvent(QDragMoveEvent *e)` | 处理拖动移动。 | 决定是否接受拖放。 |
| 受保护函数 | `dropEvent(QDropEvent *e)` | 处理放下。 | 实际接收拖放内容。 |
| 受保护函数 | `focusInEvent(QFocusEvent *e)` | 处理获得焦点。 | 影响输入法和光标显示。 |
| 受保护函数 | `focusOutEvent(QFocusEvent *e)` | 处理失去焦点。 | 可能影响提交和选择状态。 |
| 受保护函数 | `showEvent(QShowEvent *e)` | 处理显示。 | 首次显示时会触发一些初始化行为。 |
| 受保护函数 | `changeEvent(QEvent *e)` | 处理状态变化事件。 | 语言切换、样式切换等会经过这里。 |
| 受保护函数 | `wheelEvent(QWheelEvent *e)` | 处理鼠标滚轮。 | 影响滚动和缩放交互。 |
| 受保护函数 | `createMimeDataFromSelection()` | 从当前选择创建拖放数据。 | 自定义复制/拖放格式时常改。 |
| 受保护函数 | `canInsertFromMimeData(const QMimeData *source)` | 判断能否插入剪贴板/拖放数据。 | 决定接受哪些格式。 |
| 受保护函数 | `insertFromMimeData(const QMimeData *source)` | 从剪贴板/拖放插入内容。 | 自定义粘贴逻辑的核心点。 |
| 受保护函数 | `inputMethodEvent(QInputMethodEvent *)` | 处理输入法事件。 | 中文输入和 IME 支持关键。 |
| 受保护函数 | `scrollContentsBy(int dx, int dy)` | 处理内容滚动。 | 与大文档性能关系很大。 |
| 受保护函数 | `doSetTextCursor(const QTextCursor &cursor)` | 设置内部光标。 | 影响选择、定位和内部刷新。 |
| 受保护函数 | `firstVisibleBlock() const` | 返回当前首个可见 block。 | 做行号栏和可视区同步时常用。 |
| 受保护函数 | `contentOffset() const` | 返回内容偏移。 | 自定义绘制时需要对齐坐标。 |
| 受保护函数 | `blockBoundingRect(const QTextBlock &block) const` | 返回 block 的局部矩形。 | 行号、标记、辅助绘制常用。 |
| 受保护函数 | `blockBoundingGeometry(const QTextBlock &block) const` | 返回 block 的场景几何。 | 和滚动位置配合。 |
| 受保护函数 | `getPaintContext() const` | 返回绘制上下文。 | 自定义绘制时读取当前绘制状态。 |

### 一句话总结

`QPlainTextEdit` 是面向大段纯文本和日志流的编辑器底座；它的强项是高效、可追加、可定制，而不是复杂富文本排版。
