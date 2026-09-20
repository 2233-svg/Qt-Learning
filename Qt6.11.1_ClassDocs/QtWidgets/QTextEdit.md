# QTextEdit

> Qt 6.11.1 · Qt Widgets · 来自 `QTextEdit`

## 1. 先建立直觉

`QTextEdit` 是 Widgets 里的通用多行文本编辑器：它既能当纯文本编辑框，也能承载 HTML、Markdown、字符格式、段落格式、图片资源和撤销栈。它的核心不是“一个更大的 `QLineEdit`”，而是一个带滚动区域的 `QTextDocument` 视图和编辑入口。

常见使用场景包括富文本备注、邮件正文编辑、简单文档编辑器、带高亮选择的日志查看器、可复制的帮助内容、Markdown 预览前的编辑区域。若文本量很大、主要是代码或日志，优先考虑 `QPlainTextEdit`；若只显示可点击文档并带导航历史，使用 `QTextBrowser`。

使用它时要同时想清三层对象：`QTextEdit` 负责控件、滚动、输入事件和选择；`QTextDocument` 保存文档结构和资源；`QTextCursor` 表示插入点、选择范围和编辑命令。很多“为什么格式没生效”的问题，本质都是把控件状态、文档状态和光标状态混在了一起。

## 2. 类说明

- 头文件：`#include <QTextEdit>`
- 模块：`Qt6::Widgets`
- 继承自：`QAbstractScrollArea`
- 直接派生类：`QTextBrowser`

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

所有 `QWidget` 规则仍然适用：只能在 GUI 线程访问；加入布局后交给布局系统管理尺寸；长耗时解析、保存和加载应放到后台，结果通过信号回到 GUI 线程。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QTextEdit(parent)` / `QTextEdit(text, parent)` | 创建空编辑器或用初始文本创建编辑器。 |
| `setPlainText()` / `toPlainText()` | 以纯文本写入和读取内容，会丢弃富文本格式。 |
| `setHtml()` / `toHtml()` | 以 HTML 读写文档，适合富文本保存和恢复。 |
| `setMarkdown()` / `toMarkdown()` | 以 Markdown 读写文档，适合轻量文档编辑流程。 |
| `setText()` | 自动识别纯文本或富文本；输入来源不明确时建议显式用上面三组 API。 |
| `append()` | 在文档末尾追加一段文本，适合消息记录和简单日志。 |
| `insertPlainText()` / `insertHtml()` | 在当前光标位置插入内容。 |
| `textCursor()` / `setTextCursor()` | 读取或替换当前光标，进行选择、移动、插入和格式操作。 |
| `moveCursor()` | 按字符、词、行、段落、文档边界移动光标。 |
| `cursorForPosition()` / `cursorRect()` | 在鼠标位置和文档光标之间转换，常用于悬浮工具、批注、补全。 |
| `ensureCursorVisible()` | 编辑后滚动到当前光标，避免插入位置跑出视口。 |
| `find(QString)` / `find(QRegularExpression)` | 从当前光标开始查找文本或正则。 |
| `setReadOnly()` / `isReadOnly()` | 切换编辑器和阅读器模式。 |
| `setAcceptRichText()` | 控制粘贴、拖放时是否接收富文本。 |
| `setTextInteractionFlags()` | 精细控制选择、链接、键盘编辑等交互能力。 |
| `setCurrentCharFormat()` | 设置当前输入格式，通常影响后续输入。 |
| `mergeCurrentCharFormat()` | 合并格式，不覆盖未指定属性，适合加粗、颜色等按钮。 |
| `currentCharFormat()` | 获取当前光标处字符格式，用于同步工具栏状态。 |
| `setCurrentFont()` / `setFontFamily()` / `setFontPointSize()` | 设置当前输入字体或选中文本字体。 |
| `setFontWeight()` / `setFontItalic()` / `setFontUnderline()` | 常见文字样式控制。 |
| `setTextColor()` / `setTextBackgroundColor()` | 设置前景色和背景色。 |
| `setAlignment()` / `alignment()` | 设置或读取当前段落对齐方式。 |
| `setAutoFormatting()` | 开启自动项目符号等自动格式。 |
| `setLineWrapMode()` / `setLineWrapColumnOrWidth()` | 控制按控件宽度、像素宽度或列宽换行。 |
| `setWordWrapMode()` | 控制单词边界、任意字符等更细的换行策略。 |
| `setTabStopDistance()` / `setTabChangesFocus()` | 控制 Tab 是插入缩进还是切换焦点。 |
| `setOverwriteMode()` | 切换插入/覆盖输入模式。 |
| `setCursorWidth()` | 调整文本光标宽度。 |
| `setPlaceholderText()` | 空内容时显示提示文字。 |
| `setUndoRedoEnabled()` | 启用或禁用撤销栈。 |
| `undo()` / `redo()` | 撤销、重做编辑命令。 |
| `cut()` / `copy()` / `paste()` / `canPaste()` | 剪贴板操作。 |
| `selectAll()` / `clear()` | 全选或清空内容。 |
| `zoomIn()` / `zoomOut()` | 放大或缩小显示字体。 |
| `document()` / `setDocument()` | 访问或替换底层 `QTextDocument`。 |
| `setDocumentTitle()` / `documentTitle()` | 设置或读取文档标题。 |
| `loadResource()` | 子类化时加载图片、样式等外部资源。 |
| `setExtraSelections()` / `extraSelections()` | 添加不改变真实选择的额外高亮。 |
| `createStandardContextMenu()` | 创建标准右键菜单，可在其上追加动作。 |
| `anchorAt()` | 返回某个视口坐标下的链接目标。 |
| `print()` | 将文档输出到 `QPagedPaintDevice`，如打印机或 PDF。 |
| `inputMethodQuery()` | 输入法查询接口，通常只在自定义输入法行为时关心。 |
| `copyAvailable(bool)` | 选择状态变化导致复制能力变化。 |
| `selectionChanged()` | 当前选择范围变化。 |
| `cursorPositionChanged()` | 光标位置变化。 |
| `currentCharFormatChanged()` | 当前格式变化，常用于同步富文本工具栏。 |
| `textChanged()` | 文档内容变化。 |
| `undoAvailable(bool)` / `redoAvailable(bool)` | 撤销、重做可用状态变化。 |
| `canInsertFromMimeData()` / `insertFromMimeData()` | 子类化粘贴、拖放数据接收策略。 |
| `createMimeDataFromSelection()` | 子类化复制出去的数据格式。 |

## 4. 关键用法

### 内容读写：先决定数据格式

`setPlainText()` 最可靠，适合配置、日志、代码、用户备注等只需要字符内容的场景。`setHtml()` 保留富文本结构，适合保存字号、颜色、表格、图片引用。`setMarkdown()` 更适合人类可读的文档交换，但 Markdown 到 `QTextDocument` 再转回 Markdown 不是字节级往返，格式会被规范化。

`setText()` 看起来省事，但它会猜测文本是纯文本还是富文本。只要输入来自用户、网络或文件，最好显式选择格式，避免一段包含尖括号的普通文本被当作 HTML。

### 富文本编辑：格式属于光标，不只属于控件

工具栏按钮通常不要直接改整个文档，而是取出 `QTextCursor`，对选区调用格式命令，或用 `mergeCurrentCharFormat()` 合并当前输入格式。合并比覆盖安全，因为它只修改你关心的属性，例如只改颜色而不意外重置字号。

`currentCharFormatChanged()` 很适合同步加粗、斜体、颜色按钮，但要注意：光标跨越不同格式时，返回的是当前位置上下文，不代表整个选区都一致。专业编辑器通常还会检查选区内格式是否混合。

### 文档模型：`QTextDocument` 是真正的数据容器

`document()` 暴露的是底层文档对象。你可以连接 `QTextDocument::modificationChanged` 做未保存提示，也可以设置默认字体、页面边距、资源加载策略。`setDocument()` 会把另一个文档交给控件显示；这在多视图共享同一文档、或把编辑器临时绑定到不同文档时很有用。

替换文档时要想清所有权。通常让编辑器接管一个新建的 `QTextDocument`，不要把仍被其他对象管理生命周期的文档随手塞进去。

### 光标、选择与查找

`QTextCursor` 是所有精确编辑的入口：移动、选词、选块、插入文本、插入 HTML、合并格式都靠它。`find()` 会从当前光标继续搜索，所以“再次查找”天然可用；若要每次从头查找，先把光标移到文档开始。

`setExtraSelections()` 很适合做搜索结果高亮、当前行高亮、拼写错误波浪线这类视觉标记。它不会改变用户真实选择，体验上比反复调用 `selectAll()` 或修改光标更稳。

### 换行、Tab 与输入体验

`LineWrapMode` 决定是否换行以及按什么宽度换行；`wordWrapMode()` 决定在单词边界还是字符边界断开。普通中文内容常用 `WidgetWidth` 搭配合理的 `QTextOption::WrapAtWordBoundaryOrAnywhere`，代码编辑类界面通常关闭自动换行。

`setTabChangesFocus(true)` 适合表单中的多行备注，Tab 用于跳到下一个控件；`false` 适合编辑器，Tab 插入缩进。这个选择会强烈影响键盘用户的体验，不要只按默认值。

### 剪贴板、拖放和安全

`setAcceptRichText(false)` 可以把粘贴和拖放限制为纯文本，这是做聊天输入、评论输入、命令输入时的常用防线。若需要更强约束，子类化 `canInsertFromMimeData()` 和 `insertFromMimeData()`，统一过滤图片、HTML、文件 URL 或自定义 MIME 数据。

`anchorAt()` 和 `setTextInteractionFlags()` 可用于实现“可点击但不可编辑”的富文本区域。如果链接可能打开外部资源，不要在 `QTextEdit` 里偷偷自动打开，最好让用户明确触发。

## 5. 常见坑与经验

- `QTextEdit` 能处理富文本，但不是完整浏览器；CSS、HTML 标签和外部资源支持都服务于文档显示，不等于网页渲染。
- `toPlainText()` 会丢掉图片、表格和格式；保存用户作品前确认你要的是哪种格式。
- 大体量纯文本用 `QPlainTextEdit` 更合适，它按文本块优化，滚动和追加日志更稳。
- `textChanged()` 在程序调用 `setHtml()`、`setPlainText()` 时也会触发。做“用户已修改”判断时结合 `QTextDocument::isModified()` 更清楚。
- 不要在 `textChanged()` 里无条件再次 `setText()`，容易造成光标跳动、撤销栈混乱和递归更新。
- `zoomIn()` / `zoomOut()` 改的是显示字号效果，不是把原文里的字号全部重写一遍；保存文档时别把它当内容格式。
