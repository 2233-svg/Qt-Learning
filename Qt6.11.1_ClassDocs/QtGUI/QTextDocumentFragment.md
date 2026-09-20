# QTextDocumentFragment
> Qt 6.11.1 · Qt GUI · 来自 `QTextDocumentFragment`

## 1. 先建立直觉

`QTextDocumentFragment` 是一段可插入文档的富文本片段。它可以从纯文本、HTML、Markdown 或 cursor 选区创建，再通过 `QTextCursor::insertFragment()` 插入另一份文档。

它比字符串更懂格式，比完整 `QTextDocument` 更轻。

## 2. 类说明

- 头文件：`#include <QTextDocumentFragment>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：值类型
- 协作类：`QTextCursor`、`QTextDocument`

fragment 常用于剪贴板、拖放、模板插入、富文本转换。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 默认构造 | 创建空片段 |
| `QTextDocumentFragment(cursor)` | 从 cursor 选区创建片段 |
| `fromPlainText()` | 从纯文本创建 |
| `fromHtml()` | 从 HTML 创建 |
| `fromMarkdown()` | 从 Markdown 创建 |
| `isEmpty()` | 是否为空 |
| `toPlainText()` | 导出纯文本 |
| `toHtml()` | 导出 HTML |
| `toMarkdown()` | 导出 Markdown |

## 4. 关键用法

复制选区到另一文档：

```cpp
QTextDocumentFragment frag(cursor);
targetCursor.insertFragment(frag);
```

插入 HTML 模板：

```cpp
auto frag = QTextDocumentFragment::fromHtml("<b>Warning</b>: check input");
cursor.insertFragment(frag);
```

## 5. 使用场景

- 富文本剪贴板和拖放。
- 文档片段模板。
- HTML/Markdown 到 QTextDocument 的局部导入。
- 从选区提取富文本。

## 6. 常见坑与经验

- `toPlainText()` 会丢格式和图片信息。
- HTML 中相对资源引用需要配合文档 base URL 或资源机制。
- 从 cursor 创建时，cursor 没有选区通常得到空或当前位置相关片段，先检查 `hasSelection()`。
- 片段插入会遵循目标 cursor 的位置和当前格式上下文。

## 7. 知识点覆盖

本页覆盖：富文本片段、选区导出、HTML/Markdown/纯文本转换、模板插入、剪贴板基础。
