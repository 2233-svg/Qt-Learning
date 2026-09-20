# QPdfWriter

> Qt 6.11.1 · Qt GUI · 来自 `QPdfWriter`

## 1. 先建立直觉

`QPdfWriter` 是一个 PDF 输出设备：你把它交给 `QPainter`，后续的线条、文字、图片、路径和分页操作就会被写成 PDF。它继承 `QPagedPaintDevice`，所以它的核心不是“保存一个图片文件”，而是“用绘图命令生成一份可分页的 PDF 文档”。

典型流程是：创建 writer、设置页面大小/布局、PDF 版本、元数据、颜色模型和输出意图，然后用 `QPainter painter(&writer)` 绘制第一页；需要下一页时调用 `newPage()`，最后让 painter 结束或析构。

## 2. 类说明

- 头文件：`#include <QPdfWriter>`
- CMake：`Qt6::Gui`
- 继承自：`QObject`、`QPagedPaintDevice`
- 绘制入口：`QPainter`
- 输出目标：文件名或 `QIODevice`
- 相关类：`QPageLayout`、`QPageSize`、`QPdfOutputIntent`、`QPainter`

`QPdfWriter` 是 `QObject`，但它的日常使用更像一个绘制设备。它不能复制；生命周期要覆盖整个绘制过程。绘制时应先设置好文档级属性，避免在已经写出页面内容后再改 PDF 版本、页面参数或元数据。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `QPdfWriter(const QString &filename)` | 直接写入指定 PDF 文件。 |
| `QPdfWriter(QIODevice *device)` | 写入已有设备，适合内存、网络或自定义存储。 |
| `newPage()` | 结束当前页并开始新页；成功返回 `true`。 |
| `setResolution()` / `resolution()` | 设置绘图坐标相关 DPI，影响 painter viewport 等。 |
| `setPdfVersion()` / `pdfVersion()` | 设置 PDF 格式版本，如普通 PDF 或 PDF/X 相关版本。 |
| `setTitle()` / `title()` | 设置文档标题。 |
| `setAuthor()` / `author()` | Qt 6.9 起设置作者元数据。 |
| `setCreator()` / `creator()` | 设置创建者，一般填应用名。 |
| `setDocumentId()` / `documentId()` | Qt 6.8 起设置文档 UUID，默认随机生成。 |
| `setDocumentXmpMetadata()` | 写入自定义 XMP XML 元数据；需要自行保持与普通元数据一致。 |
| `setColorModel()` / `colorModel()` | Qt 6.8 起控制 RGB、灰度、CMYK 或自动颜色输出。 |
| `setOutputIntent()` / `outputIntent()` | Qt 6.8 起设置 PDF 输出意图，常用于 PDF/X 和印刷工作流。 |
| `addFileAttachment()` | 向 PDF 嵌入附件数据和可选 MIME 类型。 |
| `paintEngine()` | 返回内部绘图引擎，通常不直接调用。 |

## 4. 关键用法

### 生成一个多页 PDF

```cpp
QPdfWriter writer("report.pdf");
writer.setPageSize(QPageSize(QPageSize::A4));
writer.setPageMargins(QMarginsF(12, 12, 12, 12), QPageLayout::Millimeter);
writer.setTitle("Monthly Report");
writer.setCreator(QCoreApplication::applicationName());

QPainter p(&writer);
drawCoverPage(&p, writer.pageLayout());

writer.newPage();
drawTablePage(&p, writer.pageLayout());
```

`newPage()` 必须在 active painter 的绘制过程中调用。不要为每页重新创建一个新的 `QPdfWriter`，否则会得到多个文档而不是多页文档。

### 写入 QIODevice

```cpp
QBuffer buffer;
buffer.open(QIODevice::WriteOnly);

QPdfWriter writer(&buffer);
QPainter p(&writer);
p.drawText(QPointF(72, 72), "Hello PDF");
```

设备必须在写入期间保持有效并可写。`QPdfWriter` 不拥有传入的 `QIODevice`，释放顺序要由调用方保证。

### 面向印刷的颜色配置

```cpp
writer.setPdfVersion(QPagedPaintDevice::PdfVersion_X4);
writer.setColorModel(QPdfWriter::ColorModel::CMYK);
writer.setOutputIntent(printIntent);
```

这只是建立 PDF 输出策略；图片和绘制颜色是否真的符合目标 profile，仍然需要应用程序负责。

## 5. 使用场景

- 报表、发票、合同、证书等文档导出。
- 自定义绘制内容转 PDF：图表、路径、文字、图片混排。
- 多页打印预览的 PDF 输出后端。
- PDF/X-4、CMYK、输出意图等印刷交付场景。
- 需要嵌入附件或 XMP 元数据的业务文档。

## 6. 常见坑与经验

- **它是绘制设备，不是 HTML/PDF 排版引擎。** 自动分页、目录、流式布局需要你自己或更高层文档系统处理。
- **先设置文档级属性，再开始画。** 标题、版本、输出意图、颜色模型等最好在 `QPainter` 创建前确定。
- **DPI 影响坐标映射。** PDF 本身是矢量文档，但 `resolution()` 会影响 `QPainter` 的设备度量和一些栅格资源转换。
- **`newPage()` 不是清屏。** 它提交当前页并进入下一页；失败时应停止继续绘制或报告错误。
- **XMP 元数据不会自动同步。** `setTitle()`、`setCreator()` 和 `setDocumentXmpMetadata()` 是两套入口，自定义 XMP 要自己保持一致。
- **`QIODevice` 生命周期归调用方。** 传入 buffer、file 或 socket 时，绘制结束前不要关闭或销毁。
- **颜色模型不是万能转换器。** CMYK/PDF-X 工作流要同时管理图片、profile、输出意图和预检要求。

## 7. 知识点覆盖

- `QPdfWriter` 作为 `QPaintDevice` 和 `QPagedPaintDevice` 的角色
- 用 `QPainter` 绘制 PDF 的生命周期和分页
- 页面尺寸、页边距、分辨率与坐标系统
- PDF 版本、XMP、标题、作者、创建者、文档 ID
- RGB/灰度/CMYK/Auto 颜色模型与输出意图
- 文件输出与 `QIODevice` 输出的所有权边界
