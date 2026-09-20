# QColorSpace

> Qt 6.11.1 · Qt GUI · 来自 `QColorSpace`

## 1. 先建立直觉

`QColorSpace` 定义“RGB 数值究竟代表什么颜色”。它包含色域原色、白点和传递函数；这三者共同决定同一组三通道值在屏幕、照片、视频或印刷工作流中的视觉含义。

例如 `(1.0, 0.0, 0.0)` 在 sRGB、Display P3、Adobe RGB、BT.2020 中并不是同一种可显示颜色范围。颜色模型回答“用 RGB、CMYK 还是灰度描述”；色彩空间回答“这些通道对应哪组原色和亮度曲线”。

## 2. 类说明

`QColorSpace` 是值类型，常附着在 `QImage` 上，或用于构建 `QColorTransform`。它不是一个显示器对象，也不会自动改变 `QColor`；只有在图像转换或渲染管线中显式使用时才参与颜色管理。

类说明只用于表明这些 API 来自 `QColorSpace`：单个颜色值使用 `QColor`，显示器信息来自 `QScreen`，实际变换由 `transformationToColorSpace()` 产生的 `QColorTransform` 或 `QImage::convertToColorSpace()` 等图像 API 执行。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QColorSpace()` | 构造无效、未定义色彩空间。 |
| `QColorSpace(NamedColorSpace)` | 用预定义空间构造，如 sRGB、Display P3、Adobe RGB、BT.2020、BT.2100 PQ/HLG。 |
| `NamedColorSpace` | 选择常见标准色彩空间。 |
| `ColorModel` | 描述空间的颜色模型：RGB、Gray、CMYK 或 Undefined。 |
| `Primaries` / `primaryPoints()` | 查询或设置 RGB 原色与白点。 |
| `TransferFunction` / `transferFunction()` | 查询或设置亮度编码曲线，如 Linear、sRGB、Gamma、PQ、HLG。 |
| `gamma()` | 返回 Gamma 曲线参数或近似值；非 Gamma 曲线不应据此做精确推导。 |
| `colorModel()` | 返回空间可表达的颜色模型。 |
| `isValid()` | 判断是否有可用源色彩空间定义。 |
| `isValidTarget()` | 判断是否也能作为变换目标。 |
| `transformModel()` | 查询变换模型：快速三分量矩阵或 ICC 元素列表处理。 |
| `transformationToColorSpace(target)` | 构造到目标空间的 `QColorTransform`。 |
| `fromIccProfile(profile)` | 从 ICC 字节流解析色彩空间。 |
| `iccProfile()` | 导出或生成对应 ICC 配置文件。 |
| `description()` / `setDescription()` | 读取或设置空间说明名称。 |
| `withTransferFunction(...)` | 返回保留色域、替换传递函数后的新空间。 |
| `setPrimaries(...)` / `setTransferFunction(...)` | 原地定义自定义空间参数。 |
| `swap(other)` | 高效交换两个色彩空间对象。 |

## 4. 关键用法

### 普通 UI 明确用 sRGB

```cpp
QImage image(":/art/logo.png");
image.setColorSpace(QColorSpace(QColorSpace::SRgb));
```

大部分 UI 资源和屏幕设计稿都以 sRGB 为基准。给来源明确的图片附上正确色彩空间，后续缩放、混合和跨显示器显示才有可预期的基础。

### 显示照片前转换到目标空间

```cpp
QColorSpace source = image.colorSpace();
QColorSpace target(QColorSpace::SRgb);

if (source.isValid() && source != target)
    image.convertToColorSpace(target);
```

如果图片携带 Display P3 或 Adobe RGB ICC profile，却直接按 sRGB 解释，常见结果是饱和度和色相失真。目标空间实际可取决于显示器和渲染路径；sRGB 是兼容性最稳的默认。

### 为线性光合成保留相同原色，改用线性传递函数

```cpp
const QColorSpace srgb(QColorSpace::SRgb);
const QColorSpace linear = srgb.withTransferFunction(
    QColorSpace::TransferFunction::Linear);
```

模糊、渐变、半透明叠加等物理意义更强的计算通常应在线性光空间进行；完成后再转回显示用 sRGB。不要在 sRGB 编码值里直接做所有混合，然后期待亮度正确。

### 从 ICC profile 导入要检查有效性与目标能力

```cpp
QColorSpace profileSpace = QColorSpace::fromIccProfile(iccBytes);
if (!profileSpace.isValid() || !profileSpace.isValidTarget()) {
    profileSpace = QColorSpace(QColorSpace::SRgb);
}
```

Qt 支持的 ICC 范围有限。某些基于元素列表处理的 profile 可能可作为 source，却不能作为转换 target，因此必须分别检查。

## 5. 常用空间怎么选

| 空间 | 适合场景 |
| --- | --- |
| `SRgb` | 普通 UI、网页资源、跨平台默认显示。 |
| `SRgbLinear` | 线性光混合、合成、滤镜中间计算。 |
| `DisplayP3` | 现代广色域屏幕、P3 图片资源与苹果生态媒体。 |
| `AdobeRgb` | 摄影和传统宽色域图像工作流。 |
| `ProPhotoRgb` | 专业 RAW / 极宽色域编辑中间流程，需高位深谨慎使用。 |
| `Bt2020` | UHD / HDR 视频的色域基础。 |
| `Bt2100Pq` | HDR10 / PQ 编码内容。 |
| `Bt2100Hlg` | HLG HDR 广播内容。 |

## 6. 常见坑与经验

不要把 `QColor::toRgb()` 当作色彩空间转换。它只改变颜色模型表达，不把 Display P3 数值映射到 sRGB。

不要为每个像素反复创建 `QColorTransform`。先构造一次 transform，再批量应用到图像或像素数据。

不要把 `gamma()` 当成所有空间完整曲线的替代。sRGB、PQ、HLG 不是简单单一 gamma。

不要默认外部图片没有 profile 就一定是 sRGB。实际产品需要有明确策略：默认猜测 sRGB、提示用户、或保留未标记状态，取决于领域。

不要在 8-bit 图像上随意做多次宽色域/HDR 往返转换。量化与裁剪会累积，专业流程应尽量保留高位深或浮点数据。

不要认为 `isValid()` 即可证明能作为目标。涉及复杂 ICC profile 时还应检查 `isValidTarget()`。

## 7. 知识点覆盖

学习 `QColorSpace` 应覆盖色域、原色、白点、传递函数、sRGB、线性光、Display P3、Adobe RGB、BT.2020、HDR PQ/HLG、ICC profile、源/目标有效性、色彩空间变换、位深与量化误差。
