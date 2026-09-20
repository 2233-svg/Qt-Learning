# QColorTransform

> Qt 6.11.1 · Qt GUI · 来自 `QColorTransform`

## 1. 先建立直觉

`QColorTransform` 是预先计算好的颜色变换对象。它通常由源 `QColorSpace` 调用 `transformationToColorSpace(target)` 得到，然后被重复应用到颜色、8-bit 像素、16-bit 像素或浮点像素。

它的意义是把“理解两个色彩空间差异”的成本从每次映射中抽出来。对一整张图、视频帧或大量色样做转换时，应构造一次 transform 并复用，而不是每个像素重新推导色彩空间关系。

## 2. 类说明

`QColorTransform` 是值类型，不继承 `QObject`。它没有公开构造器，通常由 `QColorSpace::transformationToColorSpace()` 获得。

类说明只用于表明这些 API 来自 `QColorTransform`：它只负责映射颜色数据；色彩空间的定义、ICC profile 解析和图像批处理由 `QColorSpace`、`QImage` 或你的图像管线负责。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `isIdentity() const` | 判断是否为恒等变换，可跳过无意义映射。 |
| `map(QColor)` | 映射一个 `QColor`。 |
| `map(QRgb)` | 映射一个 8-bit 非预乘或不透明 ARGB 像素。 |
| `map(QRgba64)` | 映射一个 16-bit 非预乘或不透明 RGBA 像素。 |
| `map(QRgbaFloat16)` | 映射一个 half-float RGBA 像素。 |
| `map(QRgbaFloat32)` | 映射一个 float RGBA 像素。 |
| `operator==` / `operator!=` | 比较两个 transform 的变换定义是否相同。 |

## 4. 关键用法

### 从源空间创建到目标空间的 transform

```cpp
const QColorSpace source(QColorSpace::DisplayP3);
const QColorSpace target(QColorSpace::SRgb);
const QColorTransform transform = source.transformationToColorSpace(target);

const QColor converted = transform.map(QColor("#ff4d4f"));
```

实际项目中，颜色值必须确实按 source space 解释。给一个“默认 sRGB 的 QColor”套 Display P3 transform 并不会自动让它变成正确的 P3 颜色。

### 批量像素处理时缓存 transform

```cpp
const QColorTransform transform =
    sourceSpace.transformationToColorSpace(targetSpace);

for (QRgb &pixel : pixels) {
    pixel = transform.map(pixel);
}
```

若 `transform.isIdentity()` 为真，可以直接跳过循环，避免额外读写和色彩计算。

### 高动态范围和浮点像素使用浮点重载

```cpp
QRgbaFloat32 pixel = readLinearPixel();
pixel = transform.map(pixel);
```

HDR 或宽色域中间处理不要过早压缩到 `QRgb`。8-bit 映射会带来量化和超色域裁剪风险；尽量在高位深或浮点格式完成处理后再输出。

## 5. 使用场景

`QColorTransform` 适合图像查看器、照片导入、HDR 预览、颜色采样工具、色彩校正、打印预处理、视频帧处理、跨显示器显示和专业图形软件。

它也适合将一个稳定的调色板从工作色彩空间转换为目标显示空间。不过普通 GUI 主题通常使用 sRGB，不应为了简单按钮颜色引入复杂颜色管理。

## 6. 常见坑与经验

不要把预乘 alpha 像素直接传给 `map(QRgb)` / `map(QRgba64)`。这些重载期望不透明或非预乘输入；需要时先 unpremultiply，再按你的管线重新 premultiply。

不要期望 `map(QColor)` 保存图像级 ICC 元数据。它只映射颜色值；整张图的色彩空间标签和像素格式要由图像 API 维护。

不要每个像素构造 transform。变换构建比单次 map 更昂贵，应按源/目标空间组合缓存。

不要忽略 identity 变换。源目标相同时跳过转换既更快，也减少不必要的数值舍入。

不要把颜色空间映射与 alpha 合成混成同一步。通常应在适当的线性空间中做合成，再按显示空间编码输出。

## 7. 知识点覆盖

学习 `QColorTransform` 应覆盖源/目标色彩空间、恒等变换、像素位深、8-bit/16-bit/浮点 RGBA、预乘 alpha、transform 缓存、HDR、宽色域、批量图像处理和线性光合成。
