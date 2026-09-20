# QTextDocumentFragment 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextDocumentFragment>`  
> 所属模块：`Qt6::Gui`  
> 继承：无（值类型）

## 1. 它解决什么问题

`QTextDocumentFragment` 表示一段可以从富文档中复制、转换和再次插入的内容。它与 `QString` 的区别在于：片段可以保留字符格式、段落格式以及列表、表格、框架等文档结构。

典型场景：

- 富文本编辑器的复制、剪切和粘贴；
- 从一个文档提取选区，插入到另一个文档；
- 把 HTML、Markdown 或纯文本解析成可插入片段；
- 在剪贴板、拖放或中间层中暂存富文本内容；
- 保存“选区”而不是保存整个文档。

片段是值对象，内部数据由 Qt 管理；它不拥有来源文档，也不会让来源文档延长生命周期。用游标构造片段时，片段会复制选区内容，而不是持续引用游标的未来位置。

## 2. 创建与提取

```cpp
QTextCursor cursor = editor->textCursor();
QTextDocumentFragment fragment(cursor);

const QString plain = fragment.toPlainText();
const QString html = fragment.toHtml();
```

用整个文档构造时会复制整个文档内容：

```cpp
QTextDocumentFragment all(document);
```

如果需要复制选区的格式和结构，应使用 `QTextCursor` 构造函数；如果只需要文本，`selectedText()` 或 `toPlainText()` 更直接。

## 3. 从外部格式创建

- `fromPlainText()` 把字符串作为普通文本，不解析标签；
- `fromHtml()` 使用 Qt 富文本 HTML 解析器；
- `fromMarkdown()` 使用指定 Markdown 方言，Qt 6.4 起提供。

`fromHtml()` 的 `resourceProvider` 参数是一个用于解析资源的文档上下文，不是片段的所有者。HTML、Markdown 的支持范围与 `QTextDocument::setHtml()`、`setMarkdown()` 相同，不是完整浏览器或任意第三方 Markdown 引擎。

## 4. 导出和空片段

`isEmpty()` 用于判断片段是否没有内容。空片段导出为空字符串；不要把“纯文本为空”与“片段没有结构”混为一谈，富文本中的空段落、空表格或结构边界可能在不同导出格式中有不同表示。

- `toPlainText()` 导出适合阅读的纯文本；
- `toRawText()` 导出更接近文档内部段落分隔的文本，Qt 6.4 起提供；
- `toHtml()` 导出 Qt 富文本 HTML；
- `toMarkdown()` 导出 Markdown，Qt 6.4 起提供。

格式往返不是字节级无损过程。HTML/CSS、自定义对象、资源 URL 和 Markdown 扩展在目标格式无法表达时可能丢失。

## 5. 生命周期和跨文档插入

片段可在来源文档销毁后继续作为值对象使用，因为它保存的是复制后的片段数据；但片段中的外部资源仍可能需要目标文档或资源 provider 根据 URL 重新解析。

```cpp
QTextDocumentFragment fragment = QTextDocumentFragment::fromHtml(
    "<b>bold</b><br><i>italic</i>");

QTextCursor target(targetDocument);
target.insertFragment(fragment);
```

`insertFragment()` 会把结构插入目标位置，并在有选区时替换选区。片段不会把列表、表格对象指针从来源文档“搬运”到目标文档；目标文档会建立自己的结构对象。

## API 速查表
| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextDocumentFragment()` | 创建空片段。 | `isEmpty()` 为 `true`；不关联文档。 |
| `QTextDocumentFragment(const QTextDocument *document)` | 复制整个文档的内容和格式。 | `document` 只作为来源，不取得所有权；传空指针得到空片段。 |
| `QTextDocumentFragment(const QTextCursor &range)` | 复制光标选区中的结构化内容。 | 无选区时复制的内容范围取决于光标状态；需要明确选区再调用。 |
| `QTextDocumentFragment(const QTextDocumentFragment &rhs)` | 复制片段。 | 值语义；复制成本由 Qt 内部共享机制管理。 |
| `operator=(const QTextDocumentFragment &rhs)` | 替换片段内容。 | 不影响来源文档。 |
| `~QTextDocumentFragment()` | 销毁片段值对象。 | 不销毁来源文档或目标文档。 |
| `isEmpty()` | 判断片段是否为空。 | 不代表某种导出格式的字符串一定为空。 |
| `toPlainText()` | 导出纯文本。 | 不保留字符格式、列表属性、图片和自定义对象。 |
| `toRawText()` | 导出内部风格的原始文本。 | Qt 6.4 起；段落分隔表示可能与普通文本不同。 |
| `toHtml()` | 导出 Qt 富文本 HTML。 | 仅支持 Qt HTML 配置时提供；不是完整浏览器 HTML。 |
| `toMarkdown(MarkdownFeatures features = MarkdownDialectGitHub)` | 导出 Markdown。 | Qt 6.4 起；复杂格式可能无法无损表达。 |
| `fromPlainText(const QString &plainText)` | 从纯文本创建片段。 | 不解析 HTML 标签或 Markdown 标记。 |
| `fromHtml(const QString &html, const QTextDocument *resourceProvider = nullptr)` | 从 Qt 富文本 HTML 创建片段。 | `resourceProvider` 仅用于资源解析上下文，不转移所有权。 |
| `fromMarkdown(const QString &markdown, MarkdownFeatures features = MarkdownDialectGitHub)` | 从 Markdown 创建片段。 | Qt 6.4 起；`features` 决定方言和 HTML 处理策略。 |

## 7. 记忆重点

需要保留格式就用 `QTextDocumentFragment`，只需要字符就用 `QString`。片段是复制出来的值，不是来源文档的活动视图；跨文档插入时，结构会在目标文档中重新建立，资源则按目标文档的资源规则解析。
