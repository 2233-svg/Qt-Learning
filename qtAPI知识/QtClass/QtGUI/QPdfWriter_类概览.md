# QPdfWriter：把 QPainter 绘制命令写成多页 PDF

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPdfWriter>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Gui)`，并链接 `Qt6::Gui`

`QPdfWriter` 是一个 `QPaintDevice`：把 `QPainter` 对它执行的二维绘制命令转换为 PDF 文档。它同时继承 `QObject` 和 `QPagedPaintDevice`，因此既能用 Qt 对象生命周期管理，也具有页面尺寸、布局、边距、PDF 版本和 `newPage()` 等分页输出能力。

它不负责打印对话框，也不读取现有 PDF 后再编辑；它是一次性的 PDF **生成器**。在 writer 上开始绘制后提交的是新文档页面，输出完成取决于 `QPainter::end()` 与 writer/目标设备正常结束生命周期。

## 最小可用流程

先创建 writer，设置页面和文档属性，再开始 painter。每一页画完调用 `newPage()`，最后结束 painter：

```cpp
#include <QPainter>
#include <QPdfWriter>

void exportReport(const QString &fileName)
{
    QPdfWriter writer(fileName);
    writer.setTitle("Monthly report");
    writer.setCreator("Report Exporter");
    writer.setResolution(300);

    QPainter painter(&writer);
    painter.drawText(QPointF(72, 72), "Page 1");

    if (writer.newPage())
        painter.drawText(QPointF(72, 72), "Page 2");

    painter.end();
}
```

`QPdfWriter` 接受文件名或一个 `QIODevice *`。使用 `QIODevice` 时，调用方负责让该设备在 writer 和关联 painter 的整个使用期间保持打开且存活；writer 不应被视作设备所有者。

## 页面、分辨率与坐标

页面相关 API 来自 `QPagedPaintDevice`，包括 `setPageLayout()`、`setPageSize()`、`setPageMargins()`、`pageLayout()` 和 `newPage()`。它们决定物理页面、方向和可绘制区域。

`setResolution(dpi)` 设置 PDF 设备分辨率，并影响 `QPainter::viewport()` 等所见坐标系统。它不是“把所有矢量图无条件变清晰”的开关：路径和文本本来就是矢量，而栅格图像的最终有效清晰度还取决于其自身像素数和你将它绘制到多大的物理区域。

```cpp
QPdfWriter writer("invoice.pdf");
writer.setResolution(300);
writer.setPageSize(QPageSize(QPageSize::A4));
writer.setPageMargins(QMarginsF(15, 15, 15, 15), QPageLayout::Millimeter);

QPainter painter(&writer);
drawInvoice(painter, writer.pageLayout().paintRectPixels(writer.resolution()));
painter.end();
```

页面尺寸、边距、PDF 版本、分辨率、颜色模型和输出意图都应在 `QPainter` 开始前设定。不要依赖绘制过程中的设置变更会回溯修改已输出页面；需要不同页面几何时，按 `QPagedPaintDevice` 的页面切换规则在新页开始前明确设置并实际验证结果。

## 分页不是重新开始绘制

`newPage()` 结束当前页并开始下一页，返回值表示是否成功。它不是 `QPainter::end()` / `begin()` 的替代，也不会重置 painter 的笔、刷、字体、变换、裁剪或合成状态。

```cpp
QPainter painter(&writer);
drawHeader(painter);
drawFirstPageBody(painter);

if (!writer.newPage()) {
    painter.end();
    return;
}

// 仍是同一 QPainter；若上一页改过状态，按需要显式恢复或重新设置。
drawHeader(painter);
drawSecondPageBody(painter);
painter.end();
```

把每页绘制封装在 `painter.save()` / `restore()` 中，可防止页内变换、裁剪或透明度泄漏到后续页面。`newPage()` 失败后停止继续写入，并用调用方能观测的方式报告导出失败；不要把得到的文件当作完整有效 PDF。

## PDF 版本与颜色模型

`setPdfVersion()` 使用 `QPagedPaintDevice::PdfVersion` 选择目标 PDF 版本，默认是 `PdfVersion_1_4`。选择由下游阅读器、归档或印刷规范决定，不应仅为“版本越新越好”而改动。

Qt 6.8 起可设置 `ColorModel`：

| 模式 | 输出行为 |
| --- | --- |
| `RGB` | 所有颜色转换为 RGB 后写入 PDF。 |
| `Grayscale` | 所有颜色转灰度；为兼容性仍以 R/G/B 三分量相等的 RGB 颜色写出。 |
| `CMYK` | 所有颜色转换为 CMYK 后写入。 |
| `Auto` | RGB 保持 RGB，CMYK 保持 CMYK，其他颜色规格转为 RGB；Qt 6.8 起默认值。 |

颜色模型影响 `QPainter` 的笔和刷如何解释、转换并写出。它不是完整的印前合规检查；PDF/X 或明确的印刷流程还需要正确的输出意图、ICC profile、源色彩空间和外部预检。

## 元数据、标识与附件

`setTitle()`、`setCreator()` 和 Qt 6.9 的 `setAuthor()` 写入常见文档元数据。`setDocumentId()`（Qt 6.8 起）设置文档 UUID，适合需要外部系统追踪输出文件的场景。

XMP 是单独的 XML 元数据通道：

```cpp
writer.setTitle("Design proof");
writer.setCreator("Publishing Tool");
writer.setDocumentXmpMetadata(xmpXml);
```

`setDocumentXmpMetadata()` 不会自动把 title 或 creator 同步进 XMP，反过来也一样。应用程序必须保证这些元数据在需要时彼此一致；XMP 字节内容应是符合目标工作流要求的 XML。

`addFileAttachment(fileName, data, mimeType)` 将原始字节嵌入 PDF 作为附件。附件会增加文档体积，某些查看器、安全策略或归档规范可能隐藏、阻止或不接受附件；不要把它当成向所有读者可靠分发任意文件的渠道。

## 输出意图与 PDF/X

Qt 6.8 起 `setOutputIntent()` 接收 `QPdfOutputIntent`，用于描述文档为哪种印刷条件准备。它包含输出 profile、条件说明、条件标识和注册表信息。

```cpp
QPdfOutputIntent intent;
intent.setOutputProfile(cmykProfile);
intent.setOutputCondition("Coated print condition");
intent.setOutputConditionIdentifier("My-Coated-Profile");

writer.setColorModel(QPdfWriter::ColorModel::CMYK);
writer.setOutputIntent(intent);
```

尤其是 PDF/X-4，文档中所有颜色规格必须与输出 profile 的颜色空间一致，这一约束由应用程序负责保证。仅设置 output intent 不会自动修复已经以不匹配颜色空间绘制的内容。

## 生命周期和线程边界

`QPdfWriter` 是 `QObject`，不支持复制。让 writer、目标 `QIODevice` 和 `QPainter` 在同一线程和明确的作用域内使用。生成文档时避免让其他代码同时读写同一个输出设备。

对文件名构造器，输出目录的创建、可写性、磁盘空间和最终文件替换策略仍由应用处理。需要原子发布时，先写临时文件，成功结束并验证后再由调用方执行适当的替换流程。

## 常见错误

- 在 PDF 还由活动 painter 写入时就把文件交给上传/预览：先 `painter.end()`，再使用输出。
- 以屏幕像素坐标为唯一布局单位：应按页面、DPI、边距和物理尺寸设计布局。
- 忘记检查 `newPage()`：多页报告可能无声地缺少后续页面。
- 把 `setResolution(300)` 当作提升低分辨率 logo 的方法：图像本身仍缺少像素。
- 同时写 title/creator 和 XMP 却不保持一致：阅读器或归档系统可能显示矛盾元数据。
- 仅设置 CMYK 或 output intent 就宣称 PDF/X 合规：仍要保证所有实际绘制颜色与 profile 匹配并进行外部预检。

## API 速查表

### 构造与分页绘制

| API | 语义与使用边界 |
| --- | --- |
| `QPdfWriter(const QString &filename)` | 创建向文件名写入的 PDF 设备。 |
| `QPdfWriter(QIODevice *device)` | 创建向给定设备写入的 PDF 设备；调用方保持设备打开、可写且存活。 |
| `~QPdfWriter()` | 销毁 writer；应先结束所有关联的 `QPainter`。 |
| `newPage()` | 结束当前页并开始下一页；不重置 painter 状态，失败时停止后续输出。 |
| 继承的 `setPageLayout()` / `pageLayout()` | 设置或读取页面尺寸、方向和边距布局。 |
| 继承的 `setPageSize()` / `setPageMargins()` | 分别修改纸张尺寸和页边距。 |
| 继承的 `setPageOrientation()` | 修改页面方向。 |
| 继承的 `setPdfVersion()` / `pdfVersion()` | 设置或读取目标 PDF 版本；默认 `PdfVersion_1_4`。 |

### 输出质量与颜色

| API | 语义与使用边界 |
| --- | --- |
| `setResolution(int)` / `resolution()` | 设置或读取设备 DPI，影响绘图坐标与光栅输出；应在开始绘制前设置。 |
| `setColorModel(ColorModel)` / `colorModel()` | 设置或读取 RGB、灰度、CMYK 或自动颜色写出策略；Qt 6.8 起。 |
| `setOutputIntent(QPdfOutputIntent)` / `outputIntent()` | 设置或读取印刷条件/ICC 输出意图；Qt 6.8 起，不替代 PDF/X 合规验证。 |

### 文档信息与附件

| API | 语义与使用边界 |
| --- | --- |
| `setTitle()` / `title()` | 设置或读取文档标题。 |
| `setCreator()` / `creator()` | 设置或读取生成者信息。 |
| `setAuthor()` / `author()` | 设置或读取作者信息；Qt 6.9 起。 |
| `setDocumentId()` / `documentId()` | 设置或读取文档 UUID；Qt 6.8 起。 |
| `setDocumentXmpMetadata()` / `documentXmpMetadata()` | 设置或读取显式提供的 XMP XML；不会自动和 title/creator 同步。 |
| `addFileAttachment(fileName, data, mimeType)` | 向 PDF 嵌入原始附件字节，可选 MIME 类型；注意体积、查看器与规范限制。 |

### `ColorModel`

| 枚举值 | 含义 |
| --- | --- |
| `RGB` | 强制将所有颜色写为 RGB。 |
| `Grayscale` | 转为灰度，并以相等 RGB 分量写出以保持兼容性。 |
| `CMYK` | 强制将所有颜色写为 CMYK。 |
| `Auto` | 保留 RGB/CMYK，其他颜色转 RGB；Qt 6.8 起默认值。 |
