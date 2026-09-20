# QPaintDevice：QPainter 的二维绘制目标抽象

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPaintDevice>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Gui)`，并链接 `Qt6::Gui`  
> 相关类型：`QPainter`、`QPaintEngine`、`QImage`、`QPixmap`、`QWidget`、`QPrinter`

`QPaintDevice` 是 Qt 绘制系统中“可以被 `QPainter` 画上去”的二维目标抽象。它定义目标的尺寸、DPI、颜色深度和设备像素比，并要求派生类提供相应的 `QPaintEngine`。

常见绘制设备包括 `QImage`、`QPixmap`、`QWidget`、`QPicture`、`QPrinter`、`QPaintDeviceWindow` 与 `QOpenGLPaintDevice`。绝大多数应用直接使用这些现成类型；只有实现新的绘制后端时才会直接派生 `QPaintDevice`。

## 它解决的问题

同一段绘制代码可以画到屏幕控件、内存图片、打印机或 PDF，是因为 `QPainter` 面向 `QPaintDevice` 工作：

```cpp
QImage image(QSize(640, 480), QImage::Format_ARGB32_Premultiplied);
image.fill(Qt::white);

QPainter painter(&image);
painter.setPen(Qt::black);
painter.drawText(QRect(0, 0, image.width(), image.height()),
                 Qt::AlignCenter,
                 QStringLiteral("Rendered off-screen"));
```

这里 `QImage` 是具体的 `QPaintDevice`，而 `QPainter` 根据其 `paintEngine()`、大小和分辨率把图元渲染到内存图像。业务代码通常关心“画什么”；`QPaintDevice` 负责向绘制系统说明“画到哪里、目标有多大、怎样解释像素”。

## 实际使用场景

### 1. 用同一绘制函数输出到屏幕、图片和打印机

```cpp
void drawReport(QPainter &painter, const QRectF &area)
{
    painter.drawRect(area.adjusted(8, 8, -8, -8));
    painter.drawText(area, Qt::AlignCenter, QStringLiteral("Quarterly report"));
}

QImage preview(QSize(1200, 800), QImage::Format_ARGB32_Premultiplied);
preview.fill(Qt::white);
QPainter imagePainter(&preview);
drawReport(imagePainter, QRectF(QPointF(0, 0), preview.size()));
```

将来换成 `QPrinter` 或某个 `QWidget` 时，绘制函数仍可复用；变化主要在目标设备的尺寸、DPI 与页面布局。

### 2. 查询设备指标，决定输出细节

```cpp
void logDeviceMetrics(const QPaintDevice *device)
{
    qDebug() << "pixels:" << device->width() << 'x' << device->height();
    qDebug() << "logical DPI:" << device->logicalDpiX() << device->logicalDpiY();
    qDebug() << "physical DPI:" << device->physicalDpiX() << device->physicalDpiY();
    qDebug() << "DPR:" << device->devicePixelRatioF();
}
```

逻辑 DPI 影响文本和绘制引擎的坐标映射；物理 DPI 更接近实际设备能力。二者不相同时，正确的映射应由相应 `QPaintEngine` 处理，而不是在业务绘制代码里随意混合乘除。

### 3. 编写新的绘制后端

当现有 `QImage`、`QWidget`、OpenGL 或打印设备都不适合，例如需要把 `QPainter` 图元发送给专有矢量格式或硬件设备时，可以同时实现：

- `QPaintDevice` 派生类：提供目标度量和 `paintEngine()`；
- `QPaintEngine` 派生类：实现线条、路径、文本、图像等实际绘制操作。

这是一项框架级扩展工作，不是仅重写一个函数就能完成的轻量包装。

## 核心模型与边界

### 默认坐标系

`QPaintDevice` 的默认二维坐标系原点在左上角，X 轴向右、Y 轴向下，默认单位为一个像素。`QPainter` 可通过世界变换、窗口/视口和设备 DPI 改变最终映射，因此不要把“默认一个像素”误解为所有绘图始终等于屏幕物理像素。

打印机、PDF 和高 DPI 图像尤其要显式考虑页面尺寸、逻辑 DPI、设备像素比和 `QPainter` 的变换。

### `QPaintDevice` 不是通用画布对象

它是抽象基类，`paintEngine()` 为纯虚函数，不能直接构造使用。若只是想在内存中绘制，选 `QImage`；需要界面重绘，选 `QWidget`、`QRasterWindow` 或 `QOpenGLWindow`；需要打印或 PDF，选 `QPrinter` 或 `QPdfWriter`。

自行派生时，只提供 `QPaintDevice` 还不够：`QPainter` 还需要能实际执行图形操作的 `QPaintEngine`。

### 绘制活动期

当某个 `QPainter` 已对设备成功调用 `begin()`、但尚未调用 `end()` 时，`paintingActive()` 返回 `true`。设备销毁、重分配底层存储或跨线程移交之前，应先让绘制结束：

```cpp
QPainter painter(&image);
// ... 绘制 ...
painter.end(); // 在 image 离开作用域、resize 或交给其他工作前结束
```

通过栈对象的析构自动结束 `QPainter` 通常足够，但不能让仍活跃的 painter 指向已销毁的设备。

### 应用、线程与对象归属

Qt 文档要求在创建绘制设备前已经存在 `QGuiApplication`，因为绘制设备可能访问窗口系统资源。

`QPaintDevice` 不给所有派生类提供统一的线程安全保证。`QWidget`、`QPixmap`、`QWindow` 和打印相关对象通常应在其 GUI / 所属线程中创建与使用；`QImage` 是内存图像，适合许多后台渲染任务，但同一个图像或同一个 `QPainter` 也不能被多个线程同时修改。把具体设备交给工作线程前，应先阅读该派生类的线程规则。

### 逻辑 DPI、物理 DPI 与设备像素比

| 指标 | 表示什么 | 常见用途 |
| --- | --- | --- |
| `logicalDpiX/Y()` | 绘制引擎使用的每英寸点数。 | 字体大小和逻辑坐标映射。 |
| `physicalDpiX/Y()` | 设备实际报告的每英寸分辨率。 | 打印机能力、真实尺寸估算。 |
| `devicePixelRatioF()` | 一个设备独立像素对应的设备像素倍率，可为小数。 | High-DPI 图像/窗口资源选择与尺寸换算。 |
| `width()/height()` | 设备默认坐标单位中的尺寸。 | 创建绘制区域、裁剪和布局基准。 |
| `widthMM()/heightMM()` | 以毫米表示的物理尺寸估计。 | 打印与物理标尺场景。 |

逻辑 DPI 不等于物理 DPI 并不表示设备错误；缩放策略可能使二者不同。业务层不应假定它们恒等，也不应同时按两者重复缩放。

## 关键 API 语义

### 从设备读取度量

`width()`、`height()`、`depth()`、`logicalDpiX()` 等公共查询最终都依赖受保护的 `metric()`。使用现成设备时调用这些便利函数即可；实现派生类时，`metric()` 返回值必须彼此一致，否则文本、图片缩放和裁剪区域会各自使用不同的设备模型。

### High-DPI 的浮点 DPR

`devicePixelRatio()` 返回设备像素比，`devicePixelRatioF()` 用浮点形式表达它。Qt 6.8 起，自定义 `QPaintDevice` 若要支持分数 DPR，应在 `metric()` 中处理：

- `PdmDevicePixelRatioF_EncodedA`
- `PdmDevicePixelRatioF_EncodedB`

对这两个 metric，使用 `encodeMetricF(metric, value)` 返回编码后的整数部分。不要自行用整数比例伪造分数 DPR，也不要把该编码当作普通业务数据。

旧式 `PdmDevicePixelRatioScaled` 使用 `devicePixelRatioFScale()` 的缩放常数表达分数倍率，主要是设备实现细节；应用层读取 DPR 时使用 `devicePixelRatioF()`。

### `paintEngine()` 的所有权

`paintEngine()` 返回用于该设备的绘制引擎指针。调用者不拥有它，也不应手动释放或缓存到设备生命周期之外。对现成设备，业务代码通常无需调用此函数；它主要是 `QPainter` 和后端实现使用的接口。

## 常见错误

### 在 `QGuiApplication` 之前创建绘制设备

```cpp
// 错误的初始化次序示意
QImage preview(...);
QGuiApplication app(argc, argv);
```

先创建应用对象，再创建绘制设备。即使当前目标恰好是纯内存图像，也不要依赖“此平台似乎可行”的初始化顺序。

### 用物理 DPI 直接缩放所有文本

字体和绘制坐标通常基于逻辑 DPI 与绘制引擎映射。直接再乘物理 DPI 会造成不同屏幕、缩放设置或打印机之间的大小不一致。需要真实物理尺寸时，建立明确的毫米/英寸坐标系统或使用页面布局。

### 在活跃绘制中调整设备

对正在被 `QPainter` 使用的图像、窗口或打印目标执行销毁、重新分配或线程转移，都会留下悬空或不一致状态。先结束 painter；重绘窗口时优先走其事件模型。

### 只重写 `paintEngine()`

自定义设备还需要正确的 metric，并需要一个能完成实际绘制的 `QPaintEngine`。返回空指针、复用不兼容引擎或报告错误 DPR，会使 `QPainter` 绘制失败或出现比例错误。

## API 速查表

### `PaintDeviceMetric`

| 枚举项 | 含义 | 派生类实现提示 |
| --- | --- | --- |
| `PdmWidth`、`PdmHeight` | 默认坐标单位中的宽、高。 | 与 `width()` / `height()` 保持一致。 |
| `PdmWidthMM`、`PdmHeightMM` | 毫米宽、高。 | 表示设备物理尺寸估计。 |
| `PdmNumColors` | 可用颜色数。 | 用于 `colorCount()`。 |
| `PdmDepth` | 位深度，即 bit plane 数。 | 用于 `depth()`。 |
| `PdmDpiX`、`PdmDpiY` | 水平、垂直逻辑 DPI。 | 影响绘制引擎的逻辑分辨率。 |
| `PdmPhysicalDpiX`、`PdmPhysicalDpiY` | 水平、垂直物理 DPI。 | 不要求与逻辑 DPI 相同。 |
| `PdmDevicePixelRatio` | 整数设备像素比。 | 普通 1x / 2x 设备的兼容指标。 |
| `PdmDevicePixelRatioScaled` | 乘以 `devicePixelRatioFScale()` 的 DPR。 | 旧式分数 DPR 表达，属于设备实现细节。 |
| `PdmDevicePixelRatioF_EncodedA`、`PdmDevicePixelRatioF_EncodedB` | 编码的 `double` 分数 DPR 两部分。Qt 6.8 起提供。 | 在 `metric()` 中用 `encodeMetricF()` 返回相应部分。 |

### 公共函数

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `~QPaintDevice()` | 虚析构函数。 | 通过基类指针销毁派生对象是安全的；销毁前结束所有 `QPainter`。 |
| `devType() const` | 返回内部设备类型标识。 | 主要供 Qt 内部与后端判断；新代码通常应依赖具体类型能力而非数值分支。 |
| `paintingActive() const` | 是否仍有活跃 `QPainter` 正在该设备上绘制。 | `begin()` 到 `end()` 期间为 `true`。 |
| `paintEngine() const` | 返回该设备使用的绘制引擎。纯虚函数。 | 返回指针不转移所有权；应用代码一般不直接调用。 |
| `width() const` | 返回默认坐标单位中的宽度。 | 不等同于“永远是屏幕逻辑宽度”；结合具体设备和 DPR 理解。 |
| `height() const` | 返回默认坐标单位中的高度。 | 与 `width()` 使用同一坐标单位。 |
| `widthMM() const` | 返回毫米宽度。 | 物理尺寸估计，受设备报告精度影响。 |
| `heightMM() const` | 返回毫米高度。 | 不宜用于像素级布局。 |
| `logicalDpiX() const` | 返回水平逻辑 DPI。 | 用于绘制和字体的逻辑映射。 |
| `logicalDpiY() const` | 返回垂直逻辑 DPI。 | 不假定与 X 一定相同。 |
| `physicalDpiX() const` | 返回水平物理 DPI。 | 打印机时对应物理打印分辨率含义。 |
| `physicalDpiY() const` | 返回垂直物理 DPI。 | 逻辑 DPI 不同时由绘制引擎处理映射。 |
| `devicePixelRatio() const` | 返回设备像素比。 | 常见为 1 或 2；存在分数倍率的设备。 |
| `devicePixelRatioF() const` | 以浮点返回设备像素比。 | 应用层获取 High-DPI 倍率优先使用它。 |
| `colorCount() const` | 返回设备可用颜色数。 | 对现代真彩色设备不应把它当作调色板大小策略。 |
| `depth() const` | 返回设备位深度。 | 表示 bit plane 数，不是 alpha 通道是否存在的充分判断。 |
| `devicePixelRatioFScale()` | 返回 DPR 缩放常数。 | 主要供 `PdmDevicePixelRatioScaled` 的设备实现使用。 |
| `encodeMetricF(PaintDeviceMetric metric, double value)` | 将浮点 metric 编码成 `int`。Qt 6.8 起提供。 | 仅用于 `PdmDevicePixelRatioF_EncodedA/B` 的 `metric()` 实现。 |

### 受保护扩展点

| API | 说明 | 派生类重点 |
| --- | --- | --- |
| `QPaintDevice()` | 受保护构造函数。 | 只能由派生类调用；在创建设备前确保已有 `QGuiApplication`。 |
| `metric(PaintDeviceMetric metric) const` | 返回请求的设备度量。 | 自定义后端必须让尺寸、DPI、DPR 等返回值相互一致。 |
| `initPainter(QPainter *painter) const` | 在 painter 连接设备时初始化它。 | 高级后端钩子；没有明确需求时不要改写。 |
| `redirected(QPoint *offset) const` | 提供重定向后的绘制设备及偏移。 | 用于 Qt 的高级重定向绘制机制。 |
| `sharedPainter() const` | 返回设备共享的 painter（若有）。 | 框架内部协作钩子，避免在业务层依赖。 |
| `getDecodedMetricF(PaintDeviceMetric a, PaintDeviceMetric b) const` | 从两个编码 metric 还原浮点值。 | 与 Qt 6.8 的分数 DPR 编码机制配套。 |

## 与相邻类型的分工

| 需求 | 应选类型 |
| --- | --- |
| 在内存中生成或处理像素图 | `QImage` |
| 在桌面窗口控件上绘制 | `QWidget` 的 `paintEvent()` |
| 在窗口表面进行光栅或 OpenGL 绘制 | `QRasterWindow`、`QOpenGLWindow` |
| 输出 PDF | `QPdfWriter` |
| 输出到打印机 | `QPrinter` |
| 定义新的 `QPainter` 绘制后端 | `QPaintDevice` + `QPaintEngine` |

一句话记忆：`QPaintDevice` 描述“画到哪一种目标上”，`QPaintEngine` 负责“怎样把图元落到该目标上”，`QPainter` 是应用代码实际发出绘制命令的入口。
