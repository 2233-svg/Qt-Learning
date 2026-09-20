# QColor

> Qt 6.11.1 · Qt GUI · 来自 `QColor`

## 1. 先建立直觉

`QColor` 表示一个颜色值及其颜色模型表达。它可以用 RGB、HSV、HSL、CMYK、扩展 RGB 或文本名称构造，并在不同模型之间转换。

最重要的事实是：颜色数值和色彩空间不是一回事。`QColor(255, 0, 0)` 表示一组 RGB 通道，但“这组值在什么色彩空间中解释”由图像、显示设备或 `QColorSpace` 决定。普通 UI 颜色通常可按 sRGB 使用；照片、HDR、印刷和专业图像流程则需要进一步考虑色彩空间。

## 2. 类说明

`QColor` 是可复制值类型。它适合作为画笔、画刷、调色板、样式表、模型数据和设置项中的颜色载体。

类说明只用于表明这些 API 来自 `QColor`：颜色通道与颜色模型属于本类；色域、白点和传递函数属于 `QColorSpace`；对整张图像做色彩空间变换应使用 `QImage`、`QColorTransform` 等更高层工具。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QColor()` | 构造无效颜色，使用前应检查。 |
| `QColor(r, g, b, a)` / `fromRgb(...)` | 用 0-255 整数 RGB(A) 通道创建颜色。 |
| `setRgb(...)` / `getRgb(...)` | 写入或读取 RGB(A) 通道。 |
| `fromRgbF(...)` / `setRgbF(...)` / `getRgbF(...)` | 用 0.0-1.0 浮点 RGB(A) 通道创建、设置或读取颜色。 |
| `fromHsv(...)` / `setHsv(...)` / `getHsv(...)` | 以色相、饱和度、明度/Value 表示颜色，适合色相选择器。 |
| `fromHsl(...)` / `setHsl(...)` / `getHsl(...)` | 以色相、饱和度、亮度/Lightness 表示颜色，适合 UI 配色推导。 |
| `fromCmyk(...)` / `setCmyk(...)` / `getCmyk(...)` | 以 CMYK 表示颜色，适合印刷或相关数据交换。 |
| `red()` / `green()` / `blue()` / `alpha()` | 读取整数 RGBA 通道。 |
| `redF()` / `greenF()` / `blueF()` / `alphaF()` | 读取浮点 RGBA 通道。 |
| `hsvHue()` / `hslHue()` / `saturation()` / `lightness()` / `value()` | 读取 HSV/HSL 分量。 |
| `cyan()` / `magenta()` / `yellow()` / `black()` | 读取 CMYK 分量。 |
| `toRgb()` / `toHsv()` / `toHsl()` / `toCmyk()` | 返回转换到目标颜色模型的副本。 |
| `convertTo(spec)` | 按 `QColor::Spec` 统一转换颜色模型。 |
| `lighter(factor)` / `darker(factor)` | 以 HSV Value 为基础生成较亮或较暗的颜色副本。 |
| `name(HexRgb/HexArgb)` | 格式化为 `#RRGGBB` 或 `#AARRGGBB` 文本。 |
| `fromString(name)` | 解析命名色或十六进制颜色文本。 |
| `isValidColorName(name)` | 在解析前验证颜色文本是否可识别。 |
| `isValid()` | 判断颜色是否有效。 |
| `rgb()` / `rgba()` / `rgba64()` | 导出紧凑整数像素格式。 |
| `qRgb()` / `qRgba()` | 组合 8-bit RGB(A) 像素值。 |
| `qPremultiply()` / `qUnpremultiply()` | 在预乘与非预乘像素格式之间转换。 |
| `colorNames()` | 返回 Qt 支持的命名颜色列表。 |

## 4. 关键用法

### 解析外部颜色文本必须检查有效性

```cpp
QColor parseThemeColor(QStringView value)
{
    const QColor color = QColor::fromString(value);
    return color.isValid() ? color : QColor("#3b82f6");
}
```

用户配置、JSON、样式编辑器和网络数据都可能传入错误颜色。无效 `QColor` 不应悄悄进入画笔或设置模型。

### UI 调色通常用 HSL/HSV，渲染通常回到 RGB

```cpp
QColor accent("#2563eb");
QColor hover = accent.lighter(120);
QColor pressed = accent.darker(125);
```

`lighter()` / `darker()` 内部以 HSV Value 为主做调整，适合快速生成状态色，但不保证感知亮度严格均匀。需要无障碍对比度或专业调色时，应使用实际对比度计算与更明确的色彩策略。

### alpha 是透明度，不是亮度

```cpp
QColor overlay(0, 0, 0);
overlay.setAlphaF(0.35f);
painter.fillRect(rect(), overlay);
```

alpha 只决定和背景混合的程度。半透明黑色在不同背景上视觉效果不同；不要把降低 alpha 当作生成“更浅颜色”的通用办法。

### 选择整数还是浮点 API

UI 配色、配置文件和普通 8-bit 图像用整数 API 足够。HDR、线性光混合、滤镜计算或浮点图像处理宜使用 `*F()` / `QRgba64` / 浮点像素格式，避免早期量化。

### 预乘像素只在正确边界处理

`QRgb` / `QRgba64` 的预乘格式常用于图像内部加速混合。`QColor` 的 `rgb()` / `rgba()` 语义是颜色通道表达，不要不加判断地把预乘像素当非预乘 RGBA 填入颜色；需要时显式 `qUnpremultiply()`。

## 5. 使用场景

`QColor` 用于 `QPainter` 绘制、`QBrush`、`QPen`、`QPalette`、样式表、主题系统、图表调色板、状态色、图像像素采样和配置序列化。

HSV 常用于色轮与吸管工具，HSL 常用于推导 hover/pressed 状态色，CMYK 常用于印刷导出或接收印刷色数据，RGB 则是屏幕绘制和多数 UI 接口的默认工作方式。

## 6. 常见坑与经验

不要把默认构造的 `QColor` 当成黑色可直接使用。它是无效颜色；需要黑色请明确使用 `Qt::black` 或 `QColor(0, 0, 0)`。

不要混淆 HSL 的 lightness 与 HSV 的 value。它们同样叫“亮度”但计算方式不同，直接互换会得到意外颜色。

不要把 `name()` 默认输出当作包含 alpha 的格式。默认是 `#RRGGBB`；需要透明度时使用 `QColor::HexArgb`。

不要把 `lighter()` / `darker()` 用于精确颜色管理。它们是便利函数，factor 非正的结果不适合依赖。

不要因颜色模型转换而期待颜色空间自动转换。RGB 与 HSL/HSV/CMYK 是同一颜色的表达模型转换；显示色域转换属于 `QColorSpace` 工作。

## 7. 知识点覆盖

学习 `QColor` 应覆盖 RGB、RGBA、HSV、HSL、CMYK、alpha、整数与浮点通道、颜色文本解析、无效颜色、状态色推导、紧凑像素格式、预乘 alpha、UI 配色和颜色模型与色彩空间的区别。
