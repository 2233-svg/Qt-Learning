# QRgbaFloat

> Qt 6.11.1 · Qt GUI · 来自 `QRgbaFloat`

## 1. 先建立直觉

`QRgbaFloat<T>` 是用浮点通道保存 RGBA 的轻量颜色值，常见别名有 `QRgbaFloat16` 和 `QRgbaFloat32`。它面向半浮点/全浮点图像格式、HDR 中间计算、线性颜色处理和需要避免整数通道量化的场景。

和 `QRgba64` 的 16 位整数不同，`QRgbaFloat` 的通道是浮点值。很多普通颜色在 `0.0..1.0` 范围内，但浮点图像或 HDR 数据可能出现超过 1 的值；因此读取时要分清 `red()` 这类原始值和 `redNormalized()` 这类归一化值。

## 2. 类说明

- 头文件：`#include <QRgbaFloat>`
- CMake：`Qt6::Gui`
- 类型性质：模板值类型，通道类型由 `T` 决定
- 常用别名：`QRgbaFloat16`、`QRgbaFloat32`
- 典型场景：浮点 `QImage` 格式、HDR、颜色处理、渲染中间结果

`QRgbaFloat` 更偏底层像素/颜色计算，不提供 `QColor` 那种颜色模型转换和命名色能力。它适合在你明确知道通道语义时使用。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `FastType` | 计算时更快的浮点类型别名，便于内部实现和高效访问。 |
| `fromRgba(r,g,b,a)` | 从 8 位通道创建浮点颜色。 |
| `fromRgba64(r,g,b,a)` | 从 16 位整数通道创建浮点颜色。 |
| `fromArgb32(uint)` | 从 32 位 ARGB 创建。 |
| `red()` / `green()` / `blue()` / `alpha()` | 读取原始浮点通道值。 |
| `redNormalized()` / `greenNormalized()` / `blueNormalized()` / `alphaNormalized()` | 读取归一化到常规范围的通道值。 |
| `red8()` / `green8()` / `blue8()` / `alpha8()` | 转成 8 位通道。 |
| `red16()` / `green16()` / `blue16()` / `alpha16()` | 转成 16 位整数通道。 |
| `setRed()` / `setGreen()` / `setBlue()` / `setAlpha()` | 设置浮点通道。 |
| `isOpaque()` | alpha 是否为完全不透明。 |
| `isTransparent()` | alpha 是否为完全透明。 |
| `premultiplied()` | 返回预乘 alpha 后的颜色。 |
| `unpremultiplied()` | 从预乘形式还原为非预乘颜色。 |
| `toArgb32()` | 转为传统 32 位 ARGB，会量化/裁剪。 |
| `QRgbaFloat16` | 半浮点版本，内存更省，精度低于 32 位 float。 |
| `QRgbaFloat32` | 单精度 float 版本，适合更高精度计算。 |

## 4. 关键用法

### 浮点颜色计算

```cpp
QRgbaFloat32 c = QRgbaFloat32::fromRgba(128, 64, 32, 255);
c.setRed(c.red() * 1.2f);
```

浮点通道适合做连续计算。输出到 8 位或 16 位时再调用 `toArgb32()`、`red8()`、`red16()` 等转换函数。

### normalized 读取

```cpp
float displayRed = color.redNormalized();
```

当源数据可能超出常规范围时，normalized 访问器更适合用于 UI 显示、预览或转换到普通颜色范围。原始 `red()` 则保留计算值。

### 预乘 alpha

```cpp
QRgbaFloat16 pm = color.premultiplied();
```

浮点颜色同样要区分预乘和非预乘。图像合成、滤镜链路、GPU 上传格式不一致时，半透明边缘错误往往就来自这个边界。

## 5. 使用场景

- HDR 或浮点图像格式的像素处理。
- 在线性颜色空间中做滤镜、混合、曝光、色调映射。
- 需要半浮点节省内存的中间缓存。
- 需要全浮点保持高精度的渲染/图像计算。
- 从 8/16 位颜色转换到浮点域做处理。

## 6. 常见坑与经验

- **浮点值不一定限制在 0..1。** HDR 或中间计算可能超过 1，也可能出现需要裁剪的值。
- **normalized 和原始值用途不同。** 原始值用于计算，normalized 更适合输出/显示语义。
- **转 8 位会量化。** `red8()` 和 `toArgb32()` 都会损失浮点精度。
- **半浮点更省内存但精度有限。** 大量中间处理或敏感渐变时，`QRgbaFloat32` 更稳。
- **预乘状态要贯穿管线。** 不要把 premultiplied 和 straight alpha 混在同一条计算链里。
- **它不是颜色管理系统。** 色彩空间、ICC、显示转换需要 `QColorSpace` 或更高层逻辑配合。

## 7. 知识点覆盖

- 浮点 RGBA 与整数 RGBA 的差异
- `QRgbaFloat16`、`QRgbaFloat32` 的精度/内存取舍
- HDR、线性颜色、normalized 输出和通道裁剪
- premultiplied alpha 在浮点管线中的语义
- 8 位、16 位、32 位 ARGB 与浮点通道互转
- 与 `QImage` 浮点格式和颜色处理流程的关系
