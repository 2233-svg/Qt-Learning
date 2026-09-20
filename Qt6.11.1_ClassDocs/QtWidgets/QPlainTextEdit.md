# QPlainTextEdit

> Qt 6.11.1 · Qt Widgets · 来自 `QPlainTextEdit`

## 1. 先建立直觉

`QPlainTextEdit` 是为“大段纯文本”准备的多行编辑控件。它和 `QTextEdit` 共用不少文本基础设施，但目标不同：`QPlainTextEdit` 关注滚动、追加、按块处理、行号栏和代码/日志类场景；`QTextEdit` 更关注富文本排版。

典型场景包括日志窗口、脚本编辑器、配置文件编辑器、SQL 输入框、调试控制台、纯文本备注。只要你不需要用户直接编辑颜色、字号、表格和图片，`QPlainTextEdit` 往往是更稳的默认选择。

它的关键知识点是“block”。文档按 `QTextBlock` 组织，通常一行就是一个 block。`maximumBlockCount`、`blockCountChanged`、`firstVisibleBlock()`、`blockBoundingGeometry()` 这些 API 都围绕 block 工作，这也是它适合日志和代码编辑器的原因。

## 2. 类说明

- 头文件：`#include <QPlainTextEdit>`
- 模块：`Qt6::Widgets`
- 继承自：`QAbstractScrollArea`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它是滚动区域控件，真实绘制发生在 viewport 中。自定义行号、断点栏、当前行高亮时，要理解视口坐标、滚动偏移和可见 block 的关系。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QPlainTextEdit(parent)` / `QPlainTextEdit(text, parent)` | 创建纯文本编辑器。 |
| `setPlainText()` / `toPlainText()` | 设置或读取完整纯文本。 |
| `appendPlainText()` | 追加纯文本并自动处理段落，适合日志。 |
| `appendHtml()` | 追加 HTML 解析后的文本/格式；慎用于纯文本日志。 |
| `insertPlainText()` | 在当前光标处插入文本。 |
| `clear()` | 清空文档。 |
| `textCursor()` / `setTextCursor()` | 获取或设置当前光标与选区。 |
| `moveCursor()` | 按字符、词、行、文档边界移动光标。 |
| `cursorForPosition()` / `cursorRect()` | 坐标和光标互转，用于补全、悬浮提示、行号定位。 |
| `ensureCursorVisible()` / `centerCursor()` | 滚动到光标，或让光标尽量居中。 |
| `find(QString)` / `find(QRegularExpression)` | 从当前光标继续查找。 |
| `setReadOnly()` / `isReadOnly()` | 切换只读模式，常用于日志查看。 |
| `setMaximumBlockCount()` | 限制保留的文本块数量，做滚动日志非常关键。 |
| `blockCount()` | 获取当前 block 数，可用于行号宽度计算。 |
| `setLineWrapMode()` | 控制是否按控件宽度换行。 |
| `setWordWrapMode()` | 控制换行发生在单词边界还是任意字符。 |
| `setBackgroundVisible()` | 控制文档外区域是否绘制背景。 |
| `setCenterOnScroll()` | 让追加或移动光标时保持居中滚动。 |
| `setTabStopDistance()` / `setTabChangesFocus()` | 控制 Tab 宽度和焦点行为。 |
| `setOverwriteMode()` | 切换覆盖输入。 |
| `setCursorWidth()` | 调整插入光标宽度。 |
| `setPlaceholderText()` | 空内容提示。 |
| `setUndoRedoEnabled()` | 控制撤销栈。 |
| `undo()` / `redo()` | 撤销、重做。 |
| `cut()` / `copy()` / `paste()` / `canPaste()` | 剪贴板操作。 |
| `selectAll()` | 全选。 |
| `zoomIn()` / `zoomOut()` | 缩放显示字号。 |
| `document()` / `setDocument()` | 访问或替换底层 `QTextDocument`。 |
| `setDocumentTitle()` / `documentTitle()` | 文档标题。 |
| `setCurrentCharFormat()` / `mergeCurrentCharFormat()` | 对当前输入或选区应用字符格式。 |
| `setExtraSelections()` / `extraSelections()` | 搜索结果、当前行、诊断信息等额外高亮。 |
| `createStandardContextMenu()` | 创建可扩展的标准右键菜单。 |
| `anchorAt()` | 获取指定位置下的链接。 |
| `print()` | 打印或输出到分页绘图设备。 |
| `firstVisibleBlock()` | 获取第一个可见文本块，行号栏实现的起点。 |
| `blockBoundingGeometry()` / `blockBoundingRect()` | 获取 block 的位置和尺寸。 |
| `contentOffset()` | 当前内容相对视口的偏移。 |
| `getPaintContext()` | 自定义绘制文档相关内容时取得绘制上下文。 |
| `loadResource()` | 子类化加载资源。 |
| `canInsertFromMimeData()` / `insertFromMimeData()` | 自定义粘贴和拖放接收逻辑。 |
| `createMimeDataFromSelection()` | 自定义复制出去的数据。 |
| `textChanged()` | 内容变化。 |
| `modificationChanged(bool)` | 文档修改状态变化，适合未保存提示。 |
| `blockCountChanged(int)` | 行数/block 数变化。 |
| `updateRequest(QRect, int)` | 视口需要更新或滚动，行号栏同步绘制常用。 |
| `cursorPositionChanged()` / `selectionChanged()` | 光标或选择变化。 |
| `copyAvailable(bool)` | 当前是否可复制。 |
| `undoAvailable(bool)` / `redoAvailable(bool)` | 撤销、重做可用性变化。 |

## 4. 关键用法

### 日志窗口：不要无限追加

`appendPlainText()` 是日志面板最常见入口，但真正重要的是 `setMaximumBlockCount()`。没有上限的日志窗口会让文档、撤销栈、布局计算越来越重。设置最大 block 数后，旧行会自动丢弃，界面能长期运行。

只读日志一般这样组合：`setReadOnly(true)`、`setMaximumBlockCount(n)`、按需 `moveCursor(QTextCursor::End)` 或依赖追加后的自动滚动。若用户正在查看旧内容，不要每条日志都强制跳到底部，可以根据滚动条是否接近底部决定是否跟随。

### 代码编辑：围绕 block 扩展

实现行号栏时，监听 `blockCountChanged()` 更新左边距宽度，监听 `updateRequest()` 滚动或重绘行号区域，再从 `firstVisibleBlock()` 开始遍历可见 block。这个组合比按字符串拆行可靠，因为它与控件实际布局一致。

当前行高亮、搜索高亮、错误下划线都适合放进 `ExtraSelection`。这类视觉层不应修改文档内容，也不应偷走用户的真实选区。

### 换行策略影响“行”的含义

`NoWrap` 下，视觉行和 block 更接近；`WidgetWidth` 下，一个很长的 block 可能显示成多条视觉行。做代码编辑器、日志定位、错误行跳转时，通常把“行号”理解为 block 编号，而不是屏幕上折出来的视觉行。

中文、长路径、URL、JSON 等内容可能没有理想的空格断点，这时 `wordWrapMode()` 比 `lineWrapMode()` 更关键。界面上看似“没换行”，常常是 word wrap 策略过于保守。

### 粘贴与输入控制

虽然它叫 PlainTextEdit，仍然有 `appendHtml()` 和字符格式相关 API，因为底层仍是 `QTextDocument`。如果你做的是安全的纯文本输入，建议覆盖 `insertFromMimeData()` 或在粘贴前取 `source->text()`，避免把不需要的格式和资源带进来。

`setTabChangesFocus(true)` 适合表单备注；代码编辑器通常设为 `false` 并自行处理缩进。Tab 宽度用 `setTabStopDistance()`，不要用插入固定数量空格来冒充显示宽度。

## 5. 常见坑与经验

- `QPlainTextEdit` 不是语法高亮器本身；语法高亮通常用 `QSyntaxHighlighter` 绑定到 `document()`。
- `maximumBlockCount` 会删除旧 block，这对日志是优点，对普通编辑器可能是灾难。
- `toPlainText()` 读取全文会复制字符串，大文档中不要在高频信号里反复调用。
- `textChanged()` 对程序写入同样触发。加载文件时如果不想显示“未保存”，加载后调用文档的 modified 状态相关 API 重置。
- 行号栏绘制要使用 `contentOffset()` 和 block geometry，不要假设每行高度固定；字体、缩放、换行都会改变它。
