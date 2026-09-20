# QPaintDevice

> Qt 6.11.1 · Qt GUI · 来自 `QPaintDevice`

## 1. 先建立直觉

`QPaintDevice` 表示“可以被 `QPainter` 当作目标的表面”。`QImage` 是内存表面，`QPixmap` 是显示资源，`QWidget`/`QPaintDeviceWindow` 是窗口表面，`QPdfWriter` 是分页文档表面；它们共享宽高、DPI、DPR、色深和 paint engine 这套底层协议。

应用代码通常只把已有对象传给 `QPainter`，不直接继承 `QPaintDevice`。只有实现新的输出设备或绘制后端时，才需要重载 `paintEngine()` 与 `metric()`，此时设备度量的准确性直接决定文字大小、坐标、缩放和高 DPI 结果。

## 2. 类说明

- 头文件：`#include <QPaintDevice>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：抽象基类；其构造函数和 `metric()` 位于保护区。
- 关键纯虚函数：`paintEngine()` 返回用于该设备的 `QPaintEngine`。
- 常见派生：`QImage`、`QPixmap`、`QPicture`、`QPagedPaintDevice`、`QPaintDeviceWindow`、`QWidget`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `width()` / `height()` | 查询设备默认坐标系中的宽高，窗口/图像通常为像素 |
| `widthMM()` / `heightMM()` | 查询物理尺寸估计，屏幕上可能不可靠 |
| `logicalDpiX/Y()` | 查询绘制与字体布局采用的逻辑 DPI |
| `physicalDpiX/Y()` | 查询设备声称的物理 DPI，适合参考而非精密尺量 |
| `devicePixelRatio()` / `devicePixelRatioF()` | 查询逻辑像素到物理像素的倍率 |
| `depth()` | 查询每像素位深 |
| `colorCount()` | 查询可用颜色数量，过大时可能返回 `INT_MAX` |
| `paintingActive()` | 判断是否有 `QPainter` 正在该设备上工作 |
| `paintEngine()` | 子类必须返回匹配的绘制引擎 |
| `metric(PaintDeviceMetric)` | 子类实现所有公共度量查询的底层入口 |
| `PaintDeviceMetric` | 定义宽高、毫米、色深、DPI、DPR 等查询项 |
| `encodeMetricF()` | Qt 6.8 起，为子类编码浮点 device metric 值 |

## 4. 度量概念速查

| 度量 | 应如何理解 |
| --- | --- |
| 逻辑大小 | `width()/height()` 所在坐标系，`QPainter` 通常以它为基础 |
| 物理像素 | 高 DPI 下可能是逻辑大小乘 DPR，例如 200 px 对应 100 logical px、DPR 2 |
| 逻辑 DPI | 字体 point size、布局和绘制引擎应使用的分辨率 |
| 物理 DPI | 显示器/打印机的硬件信息，显示器报告值可能不精确 |
| 毫米大小 | 从硬件报告推算，不能用于需要真实世界精度的屏幕测量 |

## 5. 关键用法

### 在通用绘制函数中查询目标设备

```cpp
void drawLegend(QPainter &painter)
{
    const QPaintDevice *device = painter.device();
    const qreal dpr = device ? device->devicePixelRatioF() : 1.0;
    const int dpi = device ? device->logicalDpiX() : 96;

    Q_UNUSED(dpr);
    Q_UNUSED(dpi);
    // 使用 painter 的逻辑坐标绘制，不自行再乘 DPR。
}
```

大多数 `QPainter` API 已将目标 device 的 DPR 映射进坐标系。知道 DPR 通常是为了创建与目标匹配的离屏缓存或请求图标，不是让每个 `drawRect()` 坐标再乘一次。

### 实现自定义 device 时正确提供 DPR

```cpp
int MyDevice::metric(PaintDeviceMetric metric) const
{
    switch (metric) {
    case PdmWidth:  return logicalSize.width();
    case PdmHeight: return logicalSize.height();
    case PdmDevicePixelRatioF_EncodedA:
        return encodeMetricF(metric, dpr);
    case PdmDevicePixelRatioF_EncodedB:
        return encodeMetricF(metric, dpr);
    default:
        return 0;
    }
}
```

Qt 6.8 的编码 metric 用于精确传递分数 DPR。自定义设备若只填旧的整数 DPR metric，会在 1.25、1.5 等缩放下产生尺寸或像素缓存误差；实现时应遵循 Qt 对 A/B 编码 metric 的约定。

### 判断绘制会话冲突

```cpp
if (image.paintingActive()) {
    qWarning() << "image already has an active painter";
    return;
}
QPainter p(&image);
```

这适合调试所有权错误，不应取代架构保证。一个设备通常不能安全地被多个 `QPainter` 同时绘制；绘制会话必须清晰开始、结束，尤其是 QPixmap 和窗口设备。

## 6. 使用场景

- 写通用绘制代码时依据目标设备选择缓存、DPI 或导出策略。
- 实现新的 `QPaintDevice` 或测试用的虚拟绘制目标。
- 区分离屏图像、屏幕和打印设备上的字体/尺寸差异。
- 调试双 painter、错误 DPR 或不匹配的 paint engine。

## 7. 常见坑与经验

- **不建议为业务 UI 继承它。** 自绘窗口优先 `QWidget`、`QRasterWindow` 或 `QPaintDeviceWindow`；离屏渲染用 `QImage`。
- **logical 与 physical DPI 不可混用。** 文字与 Qt 坐标通常跟随 logical DPI；打印尺寸或校准才参考 physical DPI。
- **DPR 不等于 DPI。** DPR 表示逻辑/物理像素倍率，DPI 是每英寸点数，二者解决不同问题。
- **屏幕毫米数据不可靠。** 硬件报告、远程桌面、缩放设置都可能使 `widthMM()` 偏差很大。
- **`paintEngine()` 生命周期要稳定。** `QPainter` 活动期间不能更换或释放对应 engine。
- **不要通过 `metric()` 猜格式。** 色深和颜色数不足以说明内存像素布局；对图像直接查询 `QImage::format()`。

## 8. 知识点覆盖

绘制目标抽象、逻辑坐标、DPR、高 DPI、逻辑/物理 DPI、打印与屏幕差异、绘制会话、paint engine、设备度量、扩展自定义输出设备。
