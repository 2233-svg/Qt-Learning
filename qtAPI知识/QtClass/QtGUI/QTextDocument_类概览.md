# QTextDocument 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextDocument>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QObject`

## 1. 它解决什么问题

`QTextDocument` 是 Qt 富文本编辑模型的文档对象。它保存文本、段落、字符格式以及列表、表格、框架、图像和自定义对象等结构，并提供查找、序列化、撤销/重做、资源加载和排版入口。

它解决的是“文本内容如何被结构化、编辑和交给布局系统”的问题，而不是单纯保存一个 `QString`：

- `QString` 适合纯文本数据；
- `QTextDocument` 适合需要富文本格式、段落结构、撤销、打印或可视化布局的数据；
- `QTextEdit`、`QTextBrowser` 等控件通常把它作为内部文档；
- `QTextCursor` 负责在文档上定位和编辑；
- `QAbstractTextDocumentLayout` 负责把文档结构排成行、页并绘制出来。

常见实际场景：

- 富文本编辑器、邮件编辑器和所见即所得编辑器；
- Markdown / HTML 预览和格式转换；
- 代码编辑器中的块级扫描、查找替换和撤销；
- 生成打印文档、分页预览和导出；
- 使用自定义 URL 加载内存图片、样式表或业务资源；
- 通过自定义 `QTextObjectInterface` 显示公式、附件或内嵌控件占位对象。

`QTextDocument` 继承 `QObject`，不能复制。文档通常由一个明确的线程拥有，相关的光标、布局和结构对象都应在该线程中访问。

## 2. 文档模型和对象关系

文档可以理解为以下层次：

```text
QTextDocument
  └─ rootFrame()
      ├─ QTextBlock
      │   ├─ QTextFragment
      │   └─ QTextCharFormat
      ├─ QTextList / QTextTable / QTextFrame
      └─ QTextObject
```

块是最常用的遍历单位。`begin()` / `end()` 返回块迭代器边界，`firstBlock()` / `lastBlock()` 返回首尾块；`findBlock()` 则按文档位置查找包含该位置的块。

文档位置是字符之间的整数位置，`characterCount()` 包含文档结构所需的段落分隔边界，因此它不一定等于 `toPlainText().size()` 的直观字符数。处理光标或块时应使用 Qt 返回的位置，不要自行用字符串长度推算块边界。

## 3. 最小使用方式

```cpp
#include <QTextDocument>
#include <QTextCursor>

QTextDocument document;
document.setPlainText("first paragraph\nsecond paragraph");

QTextCursor cursor(&document);
cursor.movePosition(QTextCursor::End);
cursor.insertBlock();
cursor.insertText("third paragraph");

const QString text = document.toPlainText();
```

把文档交给编辑器时，文档的生命周期必须覆盖控件使用期间：

```cpp
auto *document = new QTextDocument(editor);
document->setMarkdown("# Title\n\nBody");
editor->setDocument(document);
```

如果只是临时转换或测量，栈对象通常更清晰；不要把栈上文档的地址保存到异步任务或长生命周期对象中。

## 4. 文本格式与转换边界

### 4.1 纯文本

`setPlainText()` 清空当前结构并建立纯文本内容；`toPlainText()` 导出适合显示和编辑的纯文本；`toRawText()` 更接近文档内部的原始段落分隔表示，适合需要区分内部段落边界的场景。两者都不会保留字符格式、列表属性或图片对象。

### 4.2 HTML

`setHtml()` 把 Qt 支持的富文本 HTML 解析到文档中，`toHtml()` 导出 Qt 富文本表示。它不是完整浏览器 DOM：

- 只支持 Qt 富文本解析器实现的标签和 CSS 子集；
- 外部图片、样式表等资源通过 `resource()` / `loadResource()` 解析；
- 不可信 HTML 不应直接当作浏览器安全边界，业务层仍需过滤；
- HTML 往返可能改变标签组织、默认样式或空白表示，不能把它当作字节级无损序列化。

### 4.3 Markdown

Qt 6.4 起，`setMarkdown()` 和 `QTextCursor::insertMarkdown()` 支持按 `MarkdownFeatures` 选择 Markdown 方言；`toMarkdown()` 负责导出。`MarkdownDialectCommonMark` 和 `MarkdownDialectGitHub` 的任务是选择解析/导出规则，不是保证兼容所有第三方 Markdown 扩展。

`MarkdownNoHTML` 可用于禁止 Markdown 中的 HTML 处理。导出后再导入通常能保留主要结构，但复杂 CSS、任意 HTML、部分资源和自定义对象不一定能往返。

## 5. 编辑、修改状态和撤销

`QTextDocument` 的文本编辑通常通过 `QTextCursor` 完成，也可直接调用 `setPlainText()`、`setHtml()` 或 `setMarkdown()` 整体替换内容。整体替换会改变文档结构，适合加载新内容，不适合在用户正在编辑时模拟局部输入。

### 修改状态

- `isModified()` 查询文档是否被标记为修改；
- `setModified(false)` 常用于成功保存后清除脏状态；
- `modificationChanged(bool)` 用于更新窗口标题、保存按钮或离开确认；
- 直接调用 `setModified(true)` 是状态标记，不等同于插入一段文本。

### 撤销栈

`undoRedoEnabled` 控制是否记录撤销/重做。`isUndoAvailable()`、`isRedoAvailable()` 和对应的步数查询适合更新 QAction 状态。`undo()` / `redo()` 有槽版本，也有带 `QTextCursor*` 的版本；带光标的版本可以把撤销操作影响的光标状态写回调用方。

`QTextCursor::beginEditBlock()` 和 `endEditBlock()` 用于把多次局部操作合并为一个用户级撤销命令。`clearUndoRedoStacks()` 可以清理一侧或两侧历史，但会丢失用户恢复路径，应只在加载新文件、建立新编辑会话或明确丢弃历史时使用。

文档内容被整体重置、最大块数触发自动裁剪或撤销被关闭时，应用不应假定旧的撤销历史仍然可用。

## 6. 布局、尺寸和页面

文档内容和文档布局是两层状态：

- `QTextDocument` 保存结构；
- `QAbstractTextDocumentLayout` 根据字体、文本选项和页面约束计算行、页、对象位置。

`documentLayout()` 返回当前布局。`setDocumentLayout()` 替换布局对象；布局必须与该文档匹配，文档会负责其布局对象的对象关系和生命周期管理。自定义布局通常应在构造时关联文档，并避免在布局回调中重入修改文档。

尺寸相关 API 的区别：

- `pageSize()` 是分页边界；宽高为零通常表示相应方向不受固定页面约束；
- `textWidth()` 设置排版宽度，适合单列编辑器或宽度变化时重新排版；
- `idealWidth()` 返回按当前内容和布局计算的理想宽度；
- `size()` 返回当前布局后的文档尺寸；
- `adjustSize()` 根据内容调整文档尺寸；
- `pageCount()` 返回当前页数；
- `lineCount()` 返回布局后的行数，可能因为视觉换行大于块数；
- `setLayoutEnabled(false)` 可在批量修改期间暂时关闭布局更新，完成后恢复并触发布局；
- `markContentsDirty(from, length)` 用于自定义布局或外部状态变化后标记范围需要重新布局。

`drawContents()` 使用当前布局把文档绘制到 `QPainter`。绘制前应准备好 painter 的状态、坐标变换和裁剪区域；它只负责绘制，不会自动创建窗口或打印设备。

`useDesignMetrics` 控制排版是否使用设计度量。需要稳定的排版结果或精确比较时，应在整个文档生命周期内保持策略一致，不要在同一份文档中随意切换。

## 7. 默认字体、文本选项和基线

`defaultFont` 为文档提供默认字体；`defaultTextOption` 控制对齐、换行、制表位、字形方向和空白处理等通用文本选项。它们是文档级默认值，不会简单地覆盖已有字符显式设置的格式。

`defaultCursorMoveStyle` 决定未显式指定移动策略时编辑器光标左右移动的语义，尤其会影响双向文本。

`documentMargin` 是文档外边距；`indentWidth` 是段落缩进换算使用的默认宽度。它们参与布局，不是对纯文本内容插入空格。

Qt 6 提供以下基线参数来控制上下标的基线偏移：

- `superScriptBaseline()` / `setSuperScriptBaseline()`；
- `subScriptBaseline()` / `setSubScriptBaseline()`；
- `baselineOffset()` / `setBaselineOffset()`。

这些值影响排版位置，不会改变文本内容，也不会替代 `QTextCharFormat` 的上下标属性。

## 8. 资源系统

文档中的图像、样式表和其它外部内容通过资源类型与 `QUrl` 名称定位：

```cpp
document->addResource(
    QTextDocument::ImageResource,
    QUrl("memory://logo"),
    QVariant::fromValue(image));

QTextCursor cursor(&document);
QTextImageFormat imageFormat;
imageFormat.setName("memory://logo");
cursor.insertImage(imageFormat);
```

`resource()` 先查询文档已有资源，必要时可能通过 `loadResource()` 或 provider 加载。`addResource()` 写入的是当前文档的资源缓存，不等于把资源嵌入 HTML/Markdown 字符串。

Qt 6.1 起可以通过 `setResourceProvider()` 为文档设置按 URL 返回 `QVariant` 的函数；静态 `setDefaultResourceProvider()` 设置进程级默认 provider。文档级 provider 与默认 provider 的优先级和回退关系应按项目约定处理，不要在 provider 中执行阻塞网络请求或修改同一文档，以免造成重入和卡顿。

重写 `loadResource()` 是更细粒度的扩展点，可根据资源类型和 URL 返回图片、HTML、样式表等资源。重写时应尽量只做加载和缓存，不要在加载回调中修改文档结构。返回空 `QVariant` 表示无法提供资源。

`ResourceType` 中 `UserResource`（值为 100）及更大的类型值可用于应用自定义资源，但生产代码应集中定义类型常量，避免与其它模块冲突。

## 9. 查找、块遍历和对象查询

`find()` 返回一个 `QTextCursor`。成功时光标通常选中匹配文本；失败时返回无效/空选区光标，调用方应检查 `isNull()` 或 `document()`，不要只看 `hasSelection()`。

字符串查找支持：

- 从整数位置开始；
- 以另一个光标的位置和方向为起点；
- `FindBackward` 反向查找；
- `FindCaseSensitively` 区分大小写；
- `FindWholeWords` 只匹配完整单词。

正则查找需要 Qt 的正则表达式配置。查找结果的选区仍然使用文档位置，修改文档后旧查找结果可能被调整或失效。

块查询的边界：

- `findBlock(pos)` 查找包含位置的块；
- `findBlockByNumber(number)` 按从零开始的块编号查找；
- `findBlockByLineNumber(number)` 按布局行号查找，视觉换行会使行号与块号不同；
- `begin()` 与 `end()` 是块迭代边界，`end()` 不是一个可编辑块；
- `firstBlock()` 与 `lastBlock()` 用于首尾访问。

`object(index)` 按对象索引查询文档对象，`objectForFormat(format)` 根据格式中的对象索引查找对象，`frameAt(pos)` 查找某个位置的框架，`rootFrame()` 返回文档根框架。返回的对象由文档管理，不应手动删除。

## 10. 文档元信息和最大块数

`MetaInformation` 用于保存文档标题、文档 URL、CSS 媒体类型和前置元数据：

- `DocumentTitle`：标题；
- `DocumentUrl`：文档来源 URL；
- `CssMedia`：CSS 媒体环境；
- `FrontMatter`：Markdown 等格式的前置元数据。

这些值是文档元数据，不会自动变成正文，也不会保证在所有格式之间往返保存。

`maximumBlockCount` 设置最大块数。设置为正数时，文档超出上限后会从开头移除多余块，适合日志窗口或终端输出。自动裁剪会让最早内容和相关光标、格式、撤销历史不可恢复；不要把它用于需要完整保存的编辑器。设置为 `0` 通常表示不限制块数。

## 11. 线程和生命周期边界

文档是 `QObject`，parent 负责其 QObject 生命周期，但 parent 不会替换文档内部结构对象的语义。布局、光标、块、列表和表格对象都不能越过文档生命周期使用。

同一文档不应在多个线程中并发读写。即便某个 API 看起来是 `const`，它也可能触发布局、资源加载或内部缓存更新。GUI 文档通常在 GUI 线程创建和使用；后台处理请先复制文本或克隆独立文档，完成后把结果通过 queued signal/slot 交回。

`clone()` 会创建一个独立的文档副本，可指定新的 parent。它适合后台测量、预览或保存前生成副本，但克隆后的文档不再与原文档共享撤销状态或光标位置。

## API 速查表
| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextDocument(QObject *parent = nullptr)` | 创建空文档。 | QObject parent 可选；文档不可复制。 |
| `QTextDocument(const QString &text, QObject *parent = nullptr)` | 用纯文本初始化文档。 | 文本按纯文本处理，不解析 HTML 或 Markdown。 |
| `~QTextDocument()` | 销毁文档及其管理的结构、布局和资源状态。 | 所有关联光标、块和对象指针随之失效。 |
| `clone(QObject *parent = nullptr) const` | 创建独立文档副本。 | 不共享原文档的编辑状态；新文档由调用方或 parent 管理。 |
| `isEmpty()` | 判断文档是否没有有效内容。 | 不要把它等同于某个序列化字符串长度。 |
| `clear()` | 清空文档内容和结构。 | 虚函数；派生类可扩展清理行为。 |
| `setUndoRedoEnabled(bool enable)` | 开关撤销/重做记录。 | 关闭后不能依赖新操作生成历史。 |
| `isUndoRedoEnabled()` | 查询撤销/重做是否启用。 | 与当前是否有可撤销步骤是两个概念。 |
| `isUndoAvailable()` | 查询是否有可撤销命令。 | 应用于启用 Undo QAction。 |
| `isRedoAvailable()` | 查询是否有可重做命令。 | 新编辑通常会清除重做分支。 |
| `availableUndoSteps()` | 返回可撤销步骤数。 | 是命令步数，不是字符数。 |
| `availableRedoSteps()` | 返回可重做步骤数。 | 受编辑块合并影响。 |
| `revision()` | 返回文档修订号。 | 适合比较文档内部修改进度，不应直接当持久化版本号。 |
| `setDocumentLayout(QAbstractTextDocumentLayout *layout)` | 替换文档布局后端。 | 布局必须服务于该文档；对象关系和生命周期需交给文档管理。 |
| `documentLayout()` | 返回当前布局。 | 返回指针不由调用方删除。 |
| `setMetaInformation(MetaInformation info, const QString &value)` | 设置标题、URL、CSS 媒体或前置元信息。 | 元信息不等同于正文，格式导出不一定完整保留。 |
| `metaInformation(MetaInformation info)` | 读取指定元信息。 | 未设置时返回空字符串。 |
| `toHtml()` | 将文档导出为 Qt 富文本 HTML。 | 仅在启用 HTML parser 时可用；不是浏览器级 HTML 序列化。 |
| `setHtml(const QString &html)` | 用 Qt 富文本 HTML 替换文档。 | 会重建内容结构；资源按文档资源系统解析。 |
| `toMarkdown(MarkdownFeatures features = MarkdownDialectGitHub)` | 导出 Markdown。 | Qt 6.4 相关配置起提供；复杂富文本可能无法无损表达。 |
| `setMarkdown(const QString &, MarkdownFeatures features = MarkdownDialectGitHub)` | 解析 Markdown 替换文档。 | 方言由 features 决定；不是完整第三方 Markdown 扩展集合。 |
| `toRawText()` | 导出接近文档内部的原始文本表示。 | 适合区分段落分隔；不保留富文本格式。 |
| `toPlainText()` | 导出用户意义上的纯文本。 | 不保留格式、图片和对象属性。 |
| `setPlainText(const QString &text)` | 用纯文本重建文档。 | 会替换原结构并影响撤销、修改状态和光标位置。 |
| `characterAt(int pos)` | 查询文档位置上的字符。 | 位置必须在有效范围内；结构边界可能返回段落分隔字符。 |
| `find(const QString &, int from = 0, FindFlags options = {}) const` | 从位置开始查找字符串。 | 失败返回无效结果光标；`FindBackward` 改变方向。 |
| `find(const QString &, const QTextCursor &, FindFlags options = {}) const` | 以光标位置作为查找起点。 | 光标必须属于当前文档语境。 |
| `find(const QRegularExpression &, int from = 0, FindFlags options = {}) const` | 从位置开始进行正则查找。 | 需要正则表达式模块配置；结果仍是文档光标选区。 |
| `find(const QRegularExpression &, const QTextCursor &, FindFlags options = {}) const` | 以光标位置开始进行正则查找。 | 正则匹配规则与文档位置边界都需处理。 |
| `frameAt(int pos)` | 查找位置所在的框架。 | 找不到返回 `nullptr`；结果由文档管理。 |
| `rootFrame()` | 返回文档根框架。 | 根框架由文档拥有，不能删除。 |
| `object(int objectIndex)` | 按对象索引查询嵌入对象。 | 不存在时返回 `nullptr`。 |
| `objectForFormat(const QTextFormat &format)` | 用格式中的对象索引查找对象。 | 只有包含有效对象索引的格式才能得到对象。 |
| `findBlock(int pos)` | 查找包含文档位置的块。 | 超出范围时返回无效 `QTextBlock`。 |
| `findBlockByNumber(int blockNumber)` | 按块编号查找块。 | 编号通常从零开始，越界返回无效块。 |
| `findBlockByLineNumber(int lineNumber)` | 按布局后的视觉行号查找块。 | 视觉行与段落块不是一一对应。 |
| `begin()` | 返回文档块遍历起点。 | 与 `end()` 配合；返回值是 `QTextBlock` 值对象。 |
| `end()` | 返回块遍历终点。 | 是哨兵，不是可编辑块。 |
| `firstBlock()` | 返回首块。 | 空文档时可能返回无效块。 |
| `lastBlock()` | 返回末块。 | 块编号和视觉行号不要混用。 |
| `setPageSize(const QSizeF &size)` | 设置页面尺寸。 | 零尺寸方向通常表示不限制该方向；影响分页和布局。 |
| `pageSize()` | 查询页面尺寸。 | 不等于当前 `size()`。 |
| `setDefaultFont(const QFont &font)` | 设置文档默认字体。 | 不会简单覆盖已有显式字符格式。 |
| `defaultFont()` | 查询默认字体。 | 参与新内容和未显式设定内容的布局。 |
| `setSuperScriptBaseline(qreal baseline)` | 设置上标基线偏移参数。 | 影响布局，不改文本；Qt 6 起提供。 |
| `superScriptBaseline()` | 查询上标基线偏移。 | 与字符格式上下标属性配合使用。 |
| `setSubScriptBaseline(qreal baseline)` | 设置下标基线偏移参数。 | 影响布局，不改文本；Qt 6 起提供。 |
| `subScriptBaseline()` | 查询下标基线偏移。 | 不等同于字体大小或行高。 |
| `setBaselineOffset(qreal baseline)` | 设置普通基线偏移。 | 影响整体排版基线；Qt 6 起提供。 |
| `baselineOffset()` | 查询普通基线偏移。 | 默认通常为零语义，具体排版仍由布局决定。 |
| `pageCount()` | 查询当前页数。 | 依赖页面尺寸和布局；未布局完成时不要假定最终值。 |
| `isModified()` | 查询脏状态。 | 与内容是否非空无关。 |
| `print(QPagedPaintDevice *printer)` | 将文档按页绘制到打印设备。 | 需要打印模块配置；设备必须有效且由调用方准备好。 |
| `resource(int type, const QUrl &name)` | 查询或加载文档资源。 | 找不到时返回空 `QVariant`；provider 中不应阻塞或重入编辑。 |
| `addResource(int type, const QUrl &name, const QVariant &resource)` | 向文档资源缓存加入资源。 | 不会自动修改正文；资源由文档管理其引用关系。 |
| `resourceProvider()` | 查询文档级资源 provider。 | Qt 6.1 起；provider 是函数对象，不应捕获失效对象。 |
| `setResourceProvider(const ResourceProvider &provider)` | 设置文档级资源解析函数。 | provider 返回空值表示无法提供；注意线程和生命周期。 |
| `defaultResourceProvider()` | 查询静态默认资源 provider。 | 是进程级默认策略，不宜被库代码随意全局修改。 |
| `setDefaultResourceProvider(const ResourceProvider &provider)` | 设置静态默认资源 provider。 | 会影响未自行配置 provider 的文档；应在应用初始化阶段统一设置。 |
| `allFormats()` | 返回文档格式集合。 | 返回值是列表副本；不通过它直接修改文档格式。 |
| `markContentsDirty(int from, int length)` | 标记内容范围需要重新布局。 | 适合布局或外部度量变化；位置和长度必须在文档语境内。 |
| `setUseDesignMetrics(bool b)` | 设置是否使用设计度量排版。 | 改变布局度量；统一文档策略后再比较尺寸。 |
| `useDesignMetrics()` | 查询设计度量策略。 | 不等于设备像素度量。 |
| `setLayoutEnabled(bool b)` | 开关布局更新。 | 批量修改时可暂时关闭，完成后必须恢复。 |
| `isLayoutEnabled()` | 查询布局是否启用。 | 关闭时尺寸、页数和绘制结果可能不是最终状态。 |
| `drawContents(QPainter *painter, const QRectF &rect = {})` | 将指定区域的文档内容绘制到 painter。 | painter 必须有效；rect 为空表示按布局绘制全部相关内容。 |
| `setTextWidth(qreal width)` | 设置文档排版宽度。 | 影响自动换行和高度；零或负值语义应按当前布局约定处理。 |
| `textWidth()` | 查询排版宽度。 | 不等于页面宽度，也不等于理想宽度。 |
| `idealWidth()` | 查询内容理想宽度。 | 依赖布局和当前字体、格式。 |
| `indentWidth()` | 查询默认缩进宽度。 | 用于段落缩进换算。 |
| `setIndentWidth(qreal width)` | 设置默认缩进宽度。 | 不会把缩进转换成正文空格。 |
| `documentMargin()` | 查询文档外边距。 | 参与布局和绘制边界。 |
| `setDocumentMargin(qreal margin)` | 设置文档外边距。 | 非负值更符合常规布局预期。 |
| `adjustSize()` | 根据内容调整文档尺寸。 | 调整后尺寸仍受布局、页面和文本宽度策略影响。 |
| `size()` | 查询布局后的文档尺寸。 | 布局关闭或尚未更新时可能不是最终值。 |
| `blockCount()` | 查询段落块数量。 | 与视觉行数、字符数不同。 |
| `lineCount()` | 查询布局后的视觉行数量。 | 自动换行、表格和对象会影响结果。 |
| `characterCount()` | 查询文档内部字符位置总数。 | 包含结构边界；不要简单等同于 `QString::size()`。 |
| `setDefaultStyleSheet(const QString &sheet)` | 设置 Qt 富文本默认样式表。 | 仅在 CSS parser 可用时提供；影响未被更具体样式覆盖的内容。 |
| `defaultStyleSheet()` | 查询默认样式表。 | 返回字符串副本。 |
| `undo(QTextCursor *cursor)` | 撤销并可写回受影响的光标状态。 | 指针可为空；没有历史时不产生有效撤销。 |
| `redo(QTextCursor *cursor)` | 重做并可写回受影响的光标状态。 | 新编辑可能清除 redo 分支。 |
| `undo()` | 撤销最新命令的槽。 | 适合连接 QAction；没有可撤销命令时无效果。 |
| `redo()` | 重做最新命令的槽。 | 没有可重做命令时无效果。 |
| `appendUndoItem(QAbstractUndoItem *)` | 向文档撤销系统追加自定义撤销项。 | 传入对象的所有权和调用契约必须与 Qt 文档撤销栈匹配，不应随意复用或手动重复释放。 |
| `setModified(bool m = true)` | 设置文档脏状态。 | 状态标记不是内容编辑；成功保存后通常传 `false`。 |
| `clearUndoRedoStacks(Stacks stacksToClear = UndoAndRedoStacks)` | 清理 undo、redo 或两者。 | 会丢失恢复路径；只在明确需要时调用。 |
| `maximumBlockCount()` | 查询块数上限。 | `0` 通常表示不限制。 |
| `setMaximumBlockCount(int maximum)` | 设置块数上限并自动裁剪旧块。 | 正数超限时从文档开头移除块；日志场景适用，完整编辑场景慎用。 |
| `defaultTextOption()` | 查询文档默认文本选项。 | 返回值类型是隐式共享值对象。 |
| `setDefaultTextOption(const QTextOption &option)` | 设置文档默认文本选项。 | 影响换行、对齐、制表位等布局；不等于修改每个块格式。 |
| `baseUrl()` | 查询相对资源解析的基础 URL。 | 影响 HTML/Markdown 资源引用的解析。 |
| `setBaseUrl(const QUrl &url)` | 设置基础 URL。 | 改变相对 URL 解析，不会自动下载资源。 |
| `defaultCursorMoveStyle()` | 查询默认光标移动样式。 | 影响编辑器左右移动，尤其是双向文本。 |
| `setDefaultCursorMoveStyle(Qt::CursorMoveStyle style)` | 设置默认光标移动样式。 | 文档级默认策略，控件也可能提供自己的覆盖逻辑。 |
| `contentsChange(int from, int charsRemoved, int charsAdded)` | 精确通知文档内容范围变化。 | 信号处理函数不要在同一变更回调中进行大规模重入编辑。 |
| `contentsChanged()` | 通知文档内容发生变化。 | 适合刷新预览或保存状态；需要范围信息时使用 `contentsChange`。 |
| `undoAvailable(bool)` | 通知是否存在可撤销命令。 | 用于启用/禁用撤销动作。 |
| `redoAvailable(bool)` | 通知是否存在可重做命令。 | 用于启用/禁用重做动作。 |
| `undoCommandAdded()` | 通知撤销栈添加了命令。 | 适合记录编辑会话或更新撤销相关 UI。 |
| `modificationChanged(bool)` | 通知 `modified` 状态变化。 | 不要仅用 `contentsChanged` 推断是否已保存。 |
| `cursorPositionChanged(const QTextCursor &cursor)` | 通知光标位置变化。 | 通常由编辑控件或文档控制器转发给 UI。 |
| `blockCountChanged(int newBlockCount)` | 通知块数变化。 | 日志裁剪和段落插入都可能触发。 |
| `baseUrlChanged(const QUrl &url)` | 通知基础 URL 变化。 | 资源引用可能需要重新加载或重新布局。 |
| `documentLayoutChanged()` | 通知布局对象被替换。 | 依赖布局的视图应重新连接布局信号。 |
| `createObject(const QTextFormat &format)` | 受保护虚函数，用于根据对象格式创建文档对象。 | 自定义对象格式时重写；遵守文档对象的生命周期和格式契约。 |
| `loadResource(int type, const QUrl &name)` | 受保护可调用虚函数，按类型和 URL 加载资源。 | 返回空值表示失败；避免阻塞、重入和跨线程访问。 |

## 13. 记忆重点

`QTextDocument` 是“内容模型 + 撤销状态 + 资源入口 + 布局入口”的组合，而不是一个带样式的字符串。实际编程时先决定文档是编辑模型、转换模型还是打印模型，再配套设置文本格式、资源 provider、页面尺寸和撤销策略；这样查找、光标、绘制和导出才会共享同一套位置与生命周期规则。
