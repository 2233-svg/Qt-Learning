# QTextDocumentWriter
> Qt 6.11.1 · Qt GUI · 来自 `QTextDocumentWriter`

## 1. 先建立直觉

`QTextDocumentWriter` 把 `QTextDocument` 写到文件或 `QIODevice`。它是文档导出的便利封装，支持的格式取决于 Qt 构建和平台，常见有 ODF、HTML、纯文本等。

如果你只要一个字符串，`QTextDocument::toHtml()` 或 `toMarkdown()` 更直接；如果要写设备和处理格式选择，用 writer。

## 2. 类说明

- 头文件：`#include <QTextDocumentWriter>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：值类型风格的 I/O 辅助类
- 协作类：`QTextDocument`、`QIODevice`

writer 不拥有文档。写入失败时通过 `write()` 的 bool 返回值判断。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 构造函数 | 以文件名、设备和格式创建 writer |
| `setFileName()` / `fileName()` | 设置或读取目标文件 |
| `setDevice()` / `device()` | 设置或读取目标 I/O 设备 |
| `setFormat()` / `format()` | 设置或读取导出格式 |
| `write(document)` | 写出文档，返回是否成功 |
| `supportedDocumentFormats()` | 静态函数，列出支持的格式 |

## 4. 关键用法

```cpp
QTextDocumentWriter writer("report.odt");
writer.setFormat("ODF");
if (!writer.write(document))
    qWarning() << "export failed";
```

写入内存：

```cpp
QBuffer buffer;
buffer.open(QIODevice::WriteOnly);
QTextDocumentWriter writer(&buffer, "HTML");
writer.write(document);
```

## 5. 使用场景

- 报表导出到 ODF 或 HTML。
- 保存富文本编辑器内容。
- 把 QTextDocument 写入网络、自定义存储或内存缓冲。
- 查询当前 Qt 支持哪些文档格式。

## 6. 常见坑与经验

- 格式名是 `QByteArray`，应来自 `supportedDocumentFormats()` 或明确写已支持值。
- 文件扩展名不一定自动代表格式，稳妥做法是显式 `setFormat()`。
- 复杂 HTML/CSS 和 QTextDocument 支持范围不等同于浏览器。
- 写入失败只有 bool，详细错误通常要结合设备状态判断。

## 7. 知识点覆盖

本页覆盖：文档导出、文件和设备写入、格式选择、支持格式查询、富文本保存边界。
