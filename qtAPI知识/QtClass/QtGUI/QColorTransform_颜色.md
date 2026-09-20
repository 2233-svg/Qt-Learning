# Qt QColorTransform 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QColorTransform>`  
> 所属模块：`Qt6::Gui`  
> 继承：无  
> 定位：颜色空间之间的具体转换器

## 1. 它解决什么问题

`QColorSpace` 描述“颜色是什么空间”，但它不直接承担每个颜色值的转换。`QColorTransform` 是由源颜色空间和目标颜色空间生成的一次具体转换，用来把 `QColor`、`QRgb`、`QRgba64` 或浮点 RGBA 像素从源空间映射到目标空间。

典型关系是：

```text
源 QColorSpace + 目标 QColorSpace
                |
                v
        QColorTransform
                |
                v
     QColor / QRgb / 图像像素
```

它适合以下真实场景：

1. 将相机或图片的 Display P3 颜色转换为 sRGB 后显示或导出；
2. 将多个来源的纹理、图标和照片统一到应用使用的颜色空间；
3. 在图像处理线程中重复转换大量像素；
4. 对单个 `QColor` 做颜色管理，而不必手工实现矩阵、白点适配和传递函数。

转换对象的创建包含预处理，因此不要在逐像素循环中反复生成它。应先创建并缓存 `QColorTransform`，再重复调用 `map()`，或直接交给 `QImage` 的整图转换 API。

## 2. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

```cpp
#include <QColorTransform>
#include <QColorSpace>
```

`QColorTransform` 是隐式共享的值类型，可以复制、移动和按值返回。它没有 QObject 父对象，也不需要手动释放。真正的创建入口通常是 `QColorSpace::transformationToColorSpace()`：

```cpp
const QColorSpace source(QColorSpace::SRgb);
const QColorSpace target(QColorSpace::DisplayP3);
const QColorTransform transform =
    source.transformationToColorSpace(target);
```

## 3. 最小可用代码

```cpp
#include <QColor>
#include <QColorSpace>
#include <QColorTransform>

QColor convertOneColor(const QColor &sourceColor)
{
    const QColorSpace sourceSpace(QColorSpace::SRgb);
    const QColorSpace targetSpace(QColorSpace::DisplayP3);
    const QColorTransform transform =
        sourceSpace.transformationToColorSpace(targetSpace);

    return transform.map(sourceColor);
}
```

这里的 `sourceColor` 应当按 `sourceSpace` 解释，返回的颜色按 `targetSpace` 解释。`QColorTransform` 不会替调用者猜测输入颜色原本属于哪个空间，也不会替 `QImage` 自动更新颜色空间元数据。

## 4. 核心使用模型

### 4.1 先确定源和目标空间

转换方向由创建它的 `QColorSpace` 对象决定：

```cpp
QColorTransform srgbToP3 = srgb.transformationToColorSpace(p3);
QColorTransform p3ToSrgb = p3.transformationToColorSpace(srgb);
```

这两个转换通常不是同一个对象。颜色空间转换一般不是简单的整数通道重排，方向、白点、传递函数和色域压缩都可能影响结果。

如果任一颜色空间无效、缺少必要的转换信息，不能把返回对象当作成功转换的证明。对于 `QImage`，应结合图像的颜色空间状态和转换后的结果检查；对于单值转换，应在业务层确保源、目标空间有效。

### 4.2 缓存转换对象

```cpp
class ImageConverter
{
public:
    ImageConverter()
        : m_transform(QColorSpace(QColorSpace::DisplayP3)
                          .transformationToColorSpace(
                              QColorSpace(QColorSpace::SRgb)))
    {
    }

    QColor convert(const QColor &color) const
    {
        return m_transform.map(color);
    }

private:
    QColorTransform m_transform;
};
```

更实际的程序通常在颜色空间改变时重建缓存，在处理一批颜色或图像时重复使用。`QColorTransform` 的复制成本适合值语义，但这不代表每个像素都应该重新调用 `transformationToColorSpace()`.

### 4.3 单像素转换和整图转换分工

- `map()`：适合单个颜色、像素格式转换循环或自定义缓冲区；
- `QImage::applyColorTransform()`：原地转换图像；
- `QImage::colorTransformed()`：返回转换后的图像，适合保留源图像；
- 需要改变目标存储格式时，使用 `QImage` 提供的带 `toFormat` 重载。

直接用 `map()` 遍历 `QImage` 时，还必须处理图像格式、每行步长、端序和预乘 alpha。能用 `QImage` 的整图 API 时，通常更不容易破坏像素格式契约。

## 5. `map()` 的输入边界

### 5.1 `QRgb` 和 `QRgba64`

这两个重载要求输入是**不透明或未预乘**的像素。`QImage::Format_ARGB32_Premultiplied` 和 `QImage::Format_RGBA64_Premultiplied` 中的 RGB 通道已经乘过 alpha，不能直接把它们的通道值当作普通 `QRgb` 或 `QRgba64` 交给 `map()`。

如果输入来自预乘格式，应先转成适合转换的未预乘格式，或者让 `QImage::applyColorTransform()` / `colorTransformed()` 处理格式细节。否则半透明颜色可能出现明显偏差，尤其是 alpha 较小时。

### 5.2 浮点 RGBA

`QRgbaFloat16` 和 `QRgbaFloat32` 用于高动态范围或高精度管线。它们同样要求输入是不透明或未预乘的。使用这些重载前要确认项目的最低 Qt 版本：

- `QRgbaFloat16` 重载：Qt 6.4 起；
- `QRgbaFloat32` 重载：Qt 6.4 起。

浮点分量的有效范围和是否允许超出 0 到 1，取决于具体颜色管线和相关像素类型语义；不要因为类型是浮点就假定转换会自动保留任意超范围值。

### 5.3 `QColor`

`map(const QColor &)` 是最方便的单值入口。它保留 `QColor` 的颜色模型和 alpha 语义，并返回另一个 `QColor`。但调用者仍要确保输入颜色代表源颜色空间；`QColor` 对象本身并不会自动携带一个可以替代 `QColorSpace` 源参数的完整图像上下文。

对于无效的 `QColor`，不要把返回值当作有效颜色使用。先检查 `color.isValid()`，并在业务层决定如何处理无效颜色。

## 6. 身份转换、比较与值语义

### 6.1 `isIdentity()`

如果源空间和目标空间等价，转换可能是 identity transform。`isIdentity()` 用于判断这一点，Qt 6.4 起提供。身份转换并不意味着所有输入都不需要检查：预乘输入规则、颜色对象有效性和图像格式问题仍然存在。

在大量数据的热路径中，可以用它选择快速路径，但不要仅凭它改变 alpha 或像素格式处理逻辑。

### 6.2 比较运算符

Qt 6.4 起提供 `operator==` 和 `operator!=`，用于判断两个对象是否定义相同的颜色转换。它们比较的是转换语义，不应被理解为“两个对象是否共享同一块内部内存”。

### 6.3 隐式共享与线程

`QColorTransform` 使用隐式共享实现值语义。复制一个转换对象不会让调用者接管某个外部资源，也不会产生 QObject 线程归属。只读地在多个线程中使用同一个转换对象通常符合值类型使用方式；如果程序同时替换某个共享变量中的转换对象，应由调用者使用自己的同步策略。

颜色转换计算本身不需要 GUI 事件循环，但如果源数据来自 GUI 对象、屏幕或平台纹理，仍须遵守那些对象的线程和图形上下文规则。

## 7. 常见误区与排查顺序

### 7.1 每个像素重新创建转换

先检查是否在循环内调用 `transformationToColorSpace()`。把创建步骤移到循环外，按源/目标空间缓存转换对象。

### 7.2 把预乘像素直接交给 `map()`

检查 `QImage::format()` 是否带有 `Premultiplied`。如果是，优先使用 `QImage` 的整图转换函数，或先转成未预乘格式。

### 7.3 只转换数值，不更新图像颜色空间

像素数据转换后，图像的 `QColorSpace` 元数据也应反映目标空间。只修改像素而保留旧元数据，会导致后续显示、保存或再次转换时被错误解释。

### 7.4 误把身份转换当成格式转换

`isIdentity()` 只描述颜色空间变换是否为恒等变换，不保证 `QImage` 的存储格式、通道顺序、alpha 表示和目标格式已经改变。

### 7.5 假设 API 会抛异常

Qt 这些 API 不以 C++ 异常报告颜色空间不匹配。要在转换前检查空间和颜色有效性，并对转换后的图像或颜色做业务级验证。

## 8. 与相关类型的协作

- `QColorSpace`：定义源空间和目标空间，并生成 `QColorTransform`。
- `QColor`：进行单个颜色的高层转换。
- `QRgb`、`QRgba64`：进行整数像素转换。
- `QRgbaFloat16`、`QRgbaFloat32`：进行浮点像素转换。
- `QImage`：批量应用颜色转换，并负责图像格式和颜色空间元数据的协作。

## 9. 逐项 API 说明

### `QColorTransform::QColorTransform()`

```cpp
QColorTransform() noexcept
```

**作用：** 创建默认的颜色转换对象。

**边界：**

- 默认构造不等于“已配置一个有意义的源到目标空间转换”；
- 通常应使用 `QColorSpace::transformationToColorSpace()` 得到实际转换；
- 调用 `map()` 前应确认该对象确实对应预期的颜色空间关系。

### `QColorTransform::isIdentity()`

```cpp
bool isIdentity() const noexcept
```

**作用：** 判断转换是否为恒等颜色变换。

**边界：**

- Qt 6.4 起提供；
- `true` 只说明颜色空间变换不改变颜色值的语义，不代表图像格式或 alpha 存储方式相同；
- 函数不修改对象，也不抛异常。

### `QColorTransform::map(QRgb)`

```cpp
QRgb map(QRgb argb) const
```

**作用：** 将一个 `QRgb` 像素应用颜色空间转换。

**参数语义：**

- 参数是 ARGB 打包的 8 位整数像素；
- 输入必须是不透明或未预乘数据；
- 不要直接传入 `Format_ARGB32_Premultiplied` 的预乘通道。

### `QColorTransform::map(QRgba64)`

```cpp
QRgba64 map(QRgba64 rgba64) const
```

**作用：** 将一个 16 位通道 RGBA 像素应用颜色空间转换。

**边界：**

- 输入必须是不透明或未预乘；
- 适合高于 8 位通道精度的像素处理；
- 若原数据来自预乘图像格式，应先处理 alpha/格式契约。

### `QColorTransform::map(QRgbaFloat16)`

```cpp
QRgbaFloat16 map(QRgbaFloat16 rgbafp16) const
```

**作用：** 转换半精度浮点 RGBA 像素。

**版本：** Qt 6.4 起。

**边界：** 输入应是不透明或未预乘；适用于浮点图像管线，不应与预乘浮点格式混用。

### `QColorTransform::map(QRgbaFloat32)`

```cpp
QRgbaFloat32 map(QRgbaFloat32 rgbafp32) const
```

**作用：** 转换单精度浮点 RGBA 像素。

**版本：** Qt 6.4 起。

**边界：** 输入应是不透明或未预乘；是否需要限制超范围值由你的图像管线决定。

### `QColorTransform::map(const QColor &)`

```cpp
QColor map(const QColor &color) const
```

**作用：** 将一个 `QColor` 从创建转换器时约定的源空间映射到目标空间。

**边界：**

- 输入颜色应当有效，并且确实按源颜色空间解释；
- 返回值是新的 `QColor`，不会修改传入对象；
- 不负责为图像或外部缓冲区更新颜色空间元数据。

### `QColorTransform::swap()`

```cpp
void swap(QColorTransform &other) noexcept
```

**作用：** 交换两个转换对象的内部值。

**边界：** 只交换转换对象，不改变任何已经通过 `map()` 产生的颜色或图像。

### `operator==` 与 `operator!=`

```cpp
bool operator==(const QColorTransform &a, const QColorTransform &b)
bool operator!=(const QColorTransform &a, const QColorTransform &b)
```

**作用：** 判断两个转换对象是否定义相同的颜色变换。

**版本：** Qt 6.4 起。

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QColorTransform()` | 创建默认值对象。 | 默认对象不等于已明确配置的源到目标转换。 |
| 查询 | `bool isIdentity() const noexcept` | 判断是否为恒等颜色变换。 | Qt 6.4 起；不代表图像格式或 alpha 存储格式相同。 |
| 转换 | `QRgb map(QRgb argb) const` | 转换 8 位打包像素。 | 输入必须不透明或未预乘。 |
| 转换 | `QRgba64 map(QRgba64 rgba64) const` | 转换 16 位通道像素。 | 不要直接传预乘通道。 |
| 转换 | `QRgbaFloat16 map(QRgbaFloat16 rgbafp16) const` | 转换半精度浮点像素。 | Qt 6.4 起；输入应未预乘。 |
| 转换 | `QRgbaFloat32 map(QRgbaFloat32 rgbafp32) const` | 转换单精度浮点像素。 | Qt 6.4 起；确认浮点范围策略。 |
| 转换 | `QColor map(const QColor &color) const` | 转换单个高层颜色值。 | 输入必须按源颜色空间解释并保持有效。 |
| 值操作 | `void swap(QColorTransform &other) noexcept` | 交换两个转换器。 | 不影响已经产生的结果。 |
| 比较 | `operator==` | 判断是否定义相同变换。 | Qt 6.4 起，比较语义而非对象地址。 |
| 比较 | `operator!=` | 判断变换是否不同。 | Qt 6.4 起，与 `operator==` 配套。 |

---

### 一句话总结

`QColorTransform` 是一次具体的颜色空间转换；先由 `QColorSpace` 创建并缓存它，再根据输入是否预乘选择 `map()` 或 `QImage` 的整图转换 API。
