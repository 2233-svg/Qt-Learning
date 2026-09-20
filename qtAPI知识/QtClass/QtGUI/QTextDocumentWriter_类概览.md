# QTextDocumentWriter 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextDocumentWriter>`  
> 所属模块：`Qt6::Gui`  
> 继承：无

## 1. 它解决什么问题

`QTextDocumentWriter` 把 `QTextDocument` 或 `QTextDocumentFragment` 写入 Qt 支持的文档格式。它把“文档模型”与“输出设备”分开：调用方决定写到文件名还是已有的 `QIODevice`，writer 根据格式选择对应的文档 writer 插件或内置实现。

实际场景：

- 富文本编辑器的“另存为 HTML、ODF 或 Markdown”；
- 把选区导出为独立片段；
- 写入 `QBuffer` 后上传或放入剪贴板；
- 在测试中把文档输出到内存设备；
- 在保存对话框中列出当前 Qt 构建支持的格式。

它只负责写出，不负责保存 UI 状态、原子替换文件、显示错误对话框或自动创建目录。`write()` 的布尔返回值必须检查。

## 2. 基本写文件方式

```cpp
QTextDocumentWriter writer("report.html");
writer.setFormat("html");

if (!writer.write(document)) {
    qWarning() << "write failed";
}
```

格式名通常不区分大小写；也可以使用 `QByteArrayLiteral("odf")`。如果构造时没有显式格式，通常可根据文件名后缀选择格式，但生产代码最好显式设置并检查 `supportedDocumentFormats()`。

## 3. 写入已有设备

```cpp
QBuffer buffer;
buffer.open(QIODevice::WriteOnly);

QTextDocumentWriter writer(&buffer, "markdown");
if (writer.write(&document)) {
    QByteArray payload = buffer.data();
}
```

设备由调用方拥有，writer 不应删除它。设备的打开模式、当前位置、可写能力和错误状态由调用方负责。对需要原子保存的文件，应用层应先写临时文件，成功后再替换目标文件。

## 4. 文档和片段的输出差异

`write(const QTextDocument *)` 输出完整文档，包括文档可表达的结构和格式。`write(const QTextDocumentFragment &)` 只输出片段内容，适合导出选区。

输出格式的表达能力决定结果：

- HTML 可表达一部分字符、段落、图片和表格格式；
- ODF 适合文档交换，但具体支持取决于 Qt 的 writer 插件；
- Markdown 适合结构化文本，复杂字体、颜色和任意对象可能被丢弃；
- 自定义 `QTextObjectInterface` 对象通常需要应用自己定义持久化方案。

## 5. 失败处理和线程边界

`write()` 返回 `false` 表示无法完成写出，例如格式不支持、设备未打开、设备不可写或序列化失败。类本身没有统一的错误字符串 API，因此应结合 `QFile` / `QIODevice` 的状态和应用日志定位原因。

writer 不拥有文档和设备。文档及其资源在整个写入期间必须有效；如果输出图片或其它资源，文档的资源 provider 也必须能在写入期间提供它们。不要在另一个线程同时修改正在写出的文档。

## API 速查表
| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextDocumentWriter()` | 创建未绑定文件和设备的 writer。 | 使用前要设置文件名或设备，并设置可用格式。 |
| `QTextDocumentWriter(QIODevice *device, const QByteArray &format)` | 绑定已有输出设备。 | 不取得设备所有权；设备应由调用方以写模式打开。 |
| `QTextDocumentWriter(const QString &fileName, const QByteArray &format = QByteArray())` | 绑定文件名。 | 格式为空时通常按后缀推断；没有可靠后缀时应显式设置。 |
| `~QTextDocumentWriter()` | 销毁 writer。 | 不关闭或删除调用方提供的设备，不销毁文档。 |
| `setFormat(const QByteArray &format)` | 设置输出格式名。 | 格式名应来自支持列表；通常大小写不敏感。 |
| `format()` | 查询当前格式名。 | 空值表示尚未设置；不要把文件扩展名直接当作一定支持的格式。 |
| `setDevice(QIODevice *device)` | 改用已有输出设备。 | 替换绑定关系，不转移所有权；设备必须可写。 |
| `device()` | 返回当前输出设备。 | 可能为 `nullptr`；返回指针由调用方管理。 |
| `setFileName(const QString &fileName)` | 设置输出文件名。 | 不负责创建父目录；路径权限由文件系统决定。 |
| `fileName()` | 查询当前文件名。 | 使用设备输出时可能为空。 |
| `write(const QTextDocument *document)` | 写出完整文档。 | 文档指针必须有效；必须检查返回值。 |
| `write(const QTextDocumentFragment &fragment)` | 写出富文本片段。 | 只输出片段，不输出来源文档的其它内容。 |
| `supportedDocumentFormats()` | 返回当前构建支持的格式名列表。 | 结果受 Qt 配置、插件和部署环境影响；运行时查询最可靠。 |

## 7. 记忆重点

`QTextDocumentWriter` 的核心流程只有三步：选择输出目标、选择受支持的格式、检查 `write()` 结果。它不替你处理文件原子性、设备生命周期或资源缺失，这些都应由保存流程明确负责。
