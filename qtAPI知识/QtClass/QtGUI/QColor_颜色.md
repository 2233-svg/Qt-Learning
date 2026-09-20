# QColor：颜色值、格式转换与透明度

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QColor>`  
> 模块：`Qt6::Gui`

`QColor` 是 Qt 绘图 API 传递“颜色”这一值的通用类型。它解决的不是调色板界面本身，而是让画笔、画刷、文本格式、窗口部件和图像像素能用同一套方式表达 RGB、HSV、HSL、CMYK 及 alpha（透明度）。

它是平台和设备无关的轻量值类型：可以按值保存、拷贝和作为函数返回值使用，不依赖 `QObject`、事件循环或 GUI 线程归属。真正把颜色画到屏幕或图像上时，才由 `QPainter`、`QImage`、`QPalette` 等对象决定输出位置和合成方式。

## 它解决的问题

实际项目里颜色的来源通常并不统一：

- 程序主题给出 `#RRGGBB` 或 `#AARRGGBB`；
- 配置文件允许用户输入 `steelblue`、`transparent`；
- 取色器编辑 HSV/HSL，而绘制 API 常消费 RGB；
- 某个控件需要“当前颜色亮 20% 的悬停态”；
- 像素缓冲区里颜色已是 `QRgb` 或 `QRgba64`。

`QColor` 把这些入口收敛为一个值对象。可以保留某种指定方式（通过 `spec()` 观察），也可以显式转换为另一种表示。注意：这里的 RGB、HSV、HSL、CMYK 是**颜色模型表示**，不是 ICC 色彩管理；涉及显示器或图片的色彩空间转换，应配合 `QColorSpace` 与 `QColorTransform`。

## 最小使用

```cpp
#include <QColor>
#include <QPainter>

void paintBadge(QPainter &painter)
{
    const QColor accent = QColor::fromString("#CC2E6D");
    if (!accent.isValid())
        return;

    painter.setBrush(accent.lighter(115));
    painter.setPen(QColor(0, 0, 0, 90));
    painter.drawRoundedRect(QRect(12, 12, 100, 32), 4, 4);
}
```

字符串、配置或网络输入都应先检查 `isValid()`。`QColor()` 默认构造的是无效颜色；Qt 为性能通常不会替你在后续读取、转换或绘制时兜底，使用无效颜色的结果未定义。

## 表示、范围与透明度

### RGB、HSV、HSL、CMYK

- 整数 RGB、饱和度、明度/亮度、CMYK 和 alpha 的合法范围都是 `0..255`。
- 整数 hue 的常规范围是 `0..359`；无彩色（黑、白、灰）没有色相，查询 hue 返回 `-1`。设置或构造时超过一圈的 hue 会按一圈归一化，例如 `360` 等同于 `0`。
- 浮点版本通常使用 `0.0..1.0`；浮点色相以一圈为单位。内部以 16 位分量存储，`set*F()` 后再以 `*F()` 取回时允许有微小舍入差。
- `fromRgbF()` / `setRgbF()` 的 RGB 分量可以小于 `0.0` 或大于 `1.0`，此时颜色成为 `ExtendedRgb`（scRGB）；但 alpha 仍必须处于 `0.0..1.0`。

alpha 为 `0` 时完全透明，为 `255` 或 `1.0` 时完全不透明。透明不是“不画”，而是交给目标绘图设备按其合成规则混合；在不支持 alpha 的目标或图像格式中，效果可能被丢弃或预先合成。

### `QRgb` 不是“永远带 alpha 的 RGB”

`QRgb` 是按 `0xAARRGGBB` 布局保存的 32 位无符号值。`QColor(QRgb)`、`fromRgb(QRgb)` 和 `setRgb(QRgb)` 会**忽略**其中 alpha，并设为不透明；需要保留 alpha 时使用 `fromRgba(QRgb)`、`setRgba(QRgb)` 或 `rgba()`。同理，`rgb()` 返回时也强制 alpha 为不透明，`rgba()` 才返回完整 ARGB。

## 常见场景

### 读取主题或用户设置

```cpp
QColor readAccent(const QString &text)
{
    const QColor color = QColor::fromString(text.trimmed());
    return color.isValid() ? color : QColor(Qt::blue);
}
```

`fromString()` 自 Qt 6.4 起可读取 `#RGB`、`#RRGGBB`、`#AARRGGBB`、12 位/16 位 RGB 表示、SVG 颜色名和 `transparent`。解析失败只得到无效值，不抛异常；只想校验文本时用 `isValidColorName()`，避免构造临时对象。

### 根据交互状态生成颜色

`lighter(factor)` 和 `darker(factor)` 返回新对象，不改变原颜色。二者通过 HSV 的 V（value）分量调整亮度，随后转回原来的颜色规格；它们适合生成简单的悬停、按下和禁用变体，但不是感知均匀的调色算法。`factor <= 0` 的返回值未指定，不能把 0 当作“变黑”。

```cpp
const QColor base("#2878C8");
const QColor hover = base.lighter(112);
const QColor pressed = base.darker(125);
```

### 使用取色器的 HSV/HSL 值

HSV 的 `value()` 适合描述“更亮/更暗”，HSL 的 `lightness()` 则是不同的亮度定义；`saturation()` 与 `hsvSaturation()` 同义，不能把它与 `hslSaturation()` 混用。要保存取色器编辑过程中的模型，可使用 `setHsv()` / `setHsl()`；要把同一个颜色值转成另一模型副本，则使用 `toHsv()` / `toHsl()`。

## 关键语义与边界

1. `spec()` 只说明这个 `QColor` 当前以哪种模型指定，并不表示设备色彩空间，也不保证两次模型转换后的各分量能完全逐位还原。
2. `toRgb()`、`toHsv()`、`toHsl()`、`toCmyk()`、`toExtendedRgb()` 与 `convertTo()` 都返回副本；`set*()` 才修改当前对象。
3. `getRgb()`、`getHsv()`、`getHsl()`、`getCmyk()` 及其 `F` 版本会写入调用者提供的非空指针。只需要部分分量时，可把可选 alpha 指针设为 `nullptr`；其余必填输出指针不能为 null。
4. `name(HexRgb)` 生成 `#RRGGBB`，会忽略 alpha；需要往配置中保留透明度时用 `name(HexArgb)`，得到 `#AARRGGBB`。
5. 比较运算符比较颜色值；不要用字符串形式是否相同来判断颜色是否相同，因为名称、十六进制大小写和不同模型都可能表达同一颜色。
6. 多线程中可自由传递各自持有的值副本；若多个线程同时读写**同一个** `QColor` 实例，仍须遵守通常的 C++ 同步规则。

## 常见误区

- **把默认构造当成黑色。** `QColor()` 是无效值，不是 `QColor(Qt::black)`。
- **传入 `QRgb` 后透明度不见了。** 这是 `fromRgb()` / `setRgb()` 的设计，改用 RGBA 对应 API。
- **以为 `name()` 会保留 alpha。** 默认格式是 `HexRgb`，显式传 `QColor::HexArgb`。
- **把 HSV 的 value 当成 HSL 的 lightness。** 两者尺度不同，调色滑条不能直接互换。
- **把 CMYK 用作精确印刷色管理。** `QColor` 可表达 CMYK 分量，但设备配置、ICC profile 和输出转换仍是 `QColorSpace`/打印管线的问题。
- **忽略无彩色 hue 的 `-1`。** 业务代码若把 hue 当数组下标或角度，应先处理这种哨兵值。

## API 速查表

### 类型、构造与有效性

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QColor()` | 默认构造 | 得到 `Invalid`；alpha 未指定，先调用 `isValid()`。 |
| `QColor(int r, int g, int b, int a = 255)` / `fromRgb(...)` | 整数 RGB | 分量必须为 `0..255`；不合法会得到无效颜色。 |
| `QColor(Qt::GlobalColor)` / `operator=(Qt::GlobalColor)` | 使用 Qt 预定义颜色 | 适合 `Qt::red`、`Qt::transparent` 等常量。 |
| `QColor(QRgb)` / `fromRgb(QRgb)` / `setRgb(QRgb)` | 从 packed RGB 建色 | 忽略 `QRgb` 的 alpha，并改为不透明。 |
| `QColor(QRgba64)` / `fromRgba64(...)` / `setRgba64()` | 64 位 RGBA | 使用每通道 16 位精度，保留 alpha。 |
| `QColor(QString/QStringView/QLatin1StringView/const char *)` | 从文本构造 | 与 `fromString()` 相同；无法解析时为无效颜色。 |
| `fromString(QAnyStringView)` | 解析颜色文本 | Qt 6.4 起可用；支持十六进制、SVG 名和 `transparent`。 |
| `isValid()` | 检查值可否使用 | 对外部输入、范围不明的构造参数和解析结果必须先检查。 |
| `isValidColorName(QAnyStringView)` | 仅验证文本 | Qt 6.4 起可用；不需要颜色对象时使用。 |
| `colorNames()` | 枚举 Qt 支持的颜色名 | 返回 `QStringList`，适合做颜色名称补全或选择器。 |
| `Spec` / `spec()` | 查询当前指定模型 | 取值为 `Invalid`、`Rgb`、`Hsv`、`Cmyk`、`Hsl`、`ExtendedRgb`；不等同于 `QColorSpace`。 |
| `NameFormat` | 控制 `name()` 输出 | `HexRgb` 为 `#RRGGBB`，`HexArgb` 为 `#AARRGGBB`。 |

### RGB 与打包颜色

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `red()` / `green()` / `blue()` / `alpha()` | 查询 8 位分量 | 返回 `0..255`；仅对有效颜色有意义。 |
| `redF()` / `greenF()` / `blueF()` / `alphaF()` | 查询浮点分量 | 常规范围 `0.0..1.0`；允许 16 位存储带来的舍入差。 |
| `setRed()`、`setGreen()`、`setBlue()`、`setAlpha()` | 修改单个 8 位分量 | 参数应在 `0..255`，会改变当前颜色。 |
| `setRedF()`、`setGreenF()`、`setBlueF()`、`setAlphaF()` | 修改单个浮点分量 | 常规范围 `0.0..1.0`；alpha 不能越界。 |
| `getRgb()` / `getRgbF()` | 批量取得 RGB(A) | 将结果写入传入指针；alpha 输出参数可为 `nullptr`。 |
| `setRgb(int, int, int, int)` / `setRgbF(...)` | 批量设置 RGB(A) | 8 位版需在范围内；浮点 RGB 越界会转为 `ExtendedRgb`。 |
| `rgba()` / `setRgba(QRgb)` | 读写 32 位 ARGB | 保留 alpha；布局为 `0xAARRGGBB`。 |
| `rgb()` | 获取不透明 packed RGB | 返回值 alpha 固定为 `0xFF`。 |
| `rgba64()` | 取得 16 位 RGBA | 用于高精度像素数据，不要误当作 `QRgb`。 |
| `fromRgba(QRgb)` | 从 32 位 ARGB 建色 | 与 `fromRgb(QRgb)` 的关键差别是保留 alpha。 |

### HSV、HSL 与 CMYK

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `hue()` / `hueF()` | 查询 HSV hue | 无彩色返回 `-1`；整数 hue 为 `0..359`。 |
| `saturation()` / `saturationF()` | 查询 HSV 饱和度 | `saturation()` 是 `hsvSaturation()` 的同义查询。 |
| `hsvHue()`、`hsvSaturation()`、`value()` 及 `F` 版 | 查询 HSV 分量 | `value` 是 HSV 的亮度定义。 |
| `getHsv()` / `getHsvF()` | 批量读取 HSV(A) | 输出指针规则同 `getRgb()`。 |
| `setHsv()` / `setHsvF()` / `fromHsv()` / `fromHsvF()` | 设置或创建 HSV 色 | 8 位的 `s/v/a` 为 `0..255`，hue 常规为 `0..359`。 |
| `hslHue()`、`hslSaturation()`、`lightness()` 及 `F` 版 | 查询 HSL 分量 | HSL saturation/lightness 与 HSV 的定义不同；无彩色 hue 仍为 `-1`。 |
| `getHsl()` / `getHslF()` | 批量读取 HSL(A) | 用于取色器或序列化 HSL 状态。 |
| `setHsl()` / `setHslF()` / `fromHsl()` / `fromHslF()` | 设置或创建 HSL 色 | 8 位分量应在合法范围；浮点版通常为 `0.0..1.0`。 |
| `cyan()`、`magenta()`、`yellow()`、`black()` 及 `F` 版 | 查询 CMYK 分量 | 是按 CMYK 模型获取的分量，不是 RGB 通道别名。 |
| `getCmyk()` / `getCmykF()` | 批量读取 CMYK(A) | 适合输出或 CMYK 编辑界面；不替代 ICC 管理。 |
| `setCmyk()` / `setCmykF()` / `fromCmyk()` / `fromCmykF()` | 设置或创建 CMYK 色 | 8 位各分量 `0..255`，浮点版 `0.0..1.0`。 |

### 转换、输出和色调变换

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `toRgb()` / `toHsv()` / `toHsl()` / `toCmyk()` | 转成指定模型副本 | 不修改原对象；转换可能存在表示精度差。 |
| `toExtendedRgb()` | 转成扩展 RGB 副本 | 用于可表示普通 RGB 范围外分量的场景。 |
| `convertTo(Spec)` | 按枚举转换副本 | 统一入口；传入应是有意义的目标 `Spec`。 |
| `lighter(int factor = 150)` | 产生更亮色 | 基于 HSV V 分量；`>100` 更亮，`<100` 会变暗，`<=0` 未指定。 |
| `darker(int factor = 200)` | 产生更暗色 | 基于 HSV V 分量；`>100` 更暗，`<100` 会变亮，`<=0` 未指定。 |
| `name(NameFormat = HexRgb)` | 输出十六进制文本 | 默认不含 alpha；需透明度时选 `HexArgb`。 |
| `operator QVariant()` | 转为 `QVariant` | 便于属性系统、模型数据和动态参数传递。 |
| `operator==` / `operator!=` | 比较颜色 | 比较颜色值，不应以输入字符串作为等价性依据。 |

### `QRgb` 辅助函数

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `qRgb(r, g, b)` / `qRgba(r, g, b, a)` | 打包 8 位分量 | 生成 `QRgb`；前者 alpha 固定为不透明。 |
| `qRed()` / `qGreen()` / `qBlue()` / `qAlpha()` | 解包单个通道 | 从 `QRgb` 读取 `0..255` 分量。 |
| `qGray(QRgb)` / `qGray(r, g, b)` | 计算灰度 | 适合快速亮度近似，不代表 HSL lightness。 |
| `qIsGray(QRgb)` | 判断 RGB 三通道是否相等 | 不检查 alpha，也不等价于所有视觉意义上的灰色。 |
| `qPremultiply()` / `qUnpremultiply()` | 预乘与还原 alpha | 用于特定图像像素格式和合成路径；不要对普通非预乘数据重复预乘。 |

## 一句话总结

把 `QColor` 当作“可验证、可转换、可携带透明度的颜色值”。先验证外部输入，再根据业务使用 RGB、HSV、HSL 或 CMYK；涉及色彩空间管理、预乘像素和实际绘制时，分别交给 `QColorSpace`、图像格式和 `QPainter` 的对应 API。
