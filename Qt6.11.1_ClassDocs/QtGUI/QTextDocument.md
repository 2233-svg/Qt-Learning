# QTextDocument
> Qt 6.11.1 · Qt GUI · 来自 `QTextDocument`

## 1. 先建立直觉

`QTextDocument` 是 Qt 富文本系统的核心数据结构。`QTextEdit`、`QPlainTextEdit`、打印、HTML/Markdown 导入导出、语法高亮、文本布局，最终都围绕它工作。

它不是一个控件，而是一份可编辑、可排版、可撤销、可序列化的文档模型。界面负责显示，`QTextCursor` 负责编辑，`QTextDocumentLayout` 负责排版。

## 2. 类说明

- 头文件：`#include <QTextDocument>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QObject`
- 协作类：`QTextCursor`、`QTextBlock`、`QTextFrame`、`QTextDocumentFragment`、`QTextOption`

文档由 block、frame、list、table、fragment 和 format 组成。普通段落是 `QTextBlock`；字符范围是 `QTextFragment`；复杂结构挂在 root frame 下。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `setPlainText()` / `toPlainText()` | 设置或导出纯文本 |
| `setHtml()` / `toHtml()` | 设置或导出 HTML |
| `setMarkdown()` / `toMarkdown()` | 设置或导出 Markdown |
| `clear()` / `isEmpty()` | 清空和判空 |
| `find()` | 按字符串或正则查找，返回 cursor |
| `begin()` / `end()` / `firstBlock()` / `lastBlock()` | 遍历文本块 |
| `findBlock()` / `findBlockByNumber()` / `findBlockByLineNumber()` | 按位置、块号或行号找 block |
| `rootFrame()` / `frameAt()` | 访问 frame 结构 |
| `documentLayout()` / `setDocumentLayout()` | 读取或替换布局引擎 |
| `setDefaultFont()` / `defaultFont()` | 默认字体 |
| `setDefaultTextOption()` / `defaultTextOption()` | 换行、对齐、tab 等默认文本选项 |
| `setPageSize()` / `pageSize()` | 分页排版尺寸 |
| `setTextWidth()` / `textWidth()` | 设置布局宽度 |
| `size()` / `idealWidth()` | 读取布局结果尺寸 |
| `setUndoRedoEnabled()` / `undo()` / `redo()` | 撤销重做 |
| `markContentsDirty()` / `adjustSize()` | 标记重新布局和调整尺寸 |
| `addResource()` / `resource()` | 管理图片、样式等外部资源 |
| `print()` / `drawContents()` | 打印或绘制文档 |
| `contentsChanged` / `contentsChange` / `undoAvailable` | 监听内容和撤销状态 |

## 4. 关键用法

编辑文档应优先通过 cursor：

```cpp
QTextDocument doc;
QTextCursor c(&doc);
c.insertText("Title");
c.insertBlock();
c.insertHtml("<b>Hello</b>");
```

查找并替换：

```cpp
QTextCursor hit = doc.find("old");
if (!hit.isNull())
    hit.insertText("new");
```

资源加载：

```cpp
doc.addResource(QTextDocument::ImageResource, QUrl("logo"), image);
doc.setHtml("<img src=\"logo\">");
```

## 5. 使用场景

- 富文本编辑器、邮件正文、报表预览。
- HTML/Markdown 转换和打印。
- 代码编辑器中的文本模型和高亮载体。
- 自动生成文档并绘制到 `QPainter`。
- 自定义对象插入、图片资源管理、撤销重做栈。

## 6. 常见坑与经验

- `setPlainText()`、`setHtml()` 会重置文档内容和撤销历史，局部改动用 `QTextCursor`。
- `toPlainText()` 会丢失格式、图片、表格结构等富文本信息。
- 文档尺寸依赖布局宽度、默认字体和 page size；没有设宽度时结果可能不是你预期的换行。
- `contentsChanged` 是总通知，`contentsChange(pos, removed, added)` 才适合做增量分析。
- 自定义资源 URL 要稳定，否则 HTML 中的 `src` 无法对应到资源。

## 7. 知识点覆盖

本页覆盖：富文本文档模型、block/frame 结构、cursor 编辑、HTML/Markdown、资源、布局尺寸、撤销重做、打印绘制、变化通知。
