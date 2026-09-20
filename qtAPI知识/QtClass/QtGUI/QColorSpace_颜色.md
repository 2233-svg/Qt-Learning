# QColorSpace：图像颜色数值的解释与转换

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QColorSpace>`  
> 模块：`Qt6::Gui`

`QColorSpace` 描述的是“同一组通道数值该如何被看作颜色”。例如 `(255, 0, 0)` 在 sRGB、Display P3 和 Adobe RGB 中都写作红色通道满值，但它们可表示的色域和实际色度并不相同。`QColorSpace` 用原色、白点和传递函数（gamma/曲线）记录这层解释，并能生成到另一空间的 `QColorTransform`。

它不是 `QColor` 的替代品：`QColor` 表达一个颜色值及其 RGB/HSV/HSL 等模型；`QColorSpace` 表达图像或像素缓冲区采用的色彩空间。两者一起才能避免“数值没变，颜色却在另一块屏幕或另一台机器上偏了”的问题。

## 它解决的问题

典型场景是接收一张带 ICC profile 的照片、在广色域屏幕编辑它、再导出到 sRGB。若把源图像 RGB 数值直接贴到另一个空间中，只是给原始字节换了标签，外观会偏色；应先以源空间和目标空间建立转换，再转换像素。

`QColorSpace` 还适合：

- 读取图片的嵌入 ICC profile，判断 Qt 是否能处理；
- 将内容明确标注为 sRGB、Display P3、Adobe RGB、Rec.2020 或 HDR 的 BT.2100；
- 创建线性 sRGB，用于应在线性光空间完成的混色/合成；
- 为 `QImage`、纹理或打印流程建立可复用的 `QColorTransform`；
- 保存无法由 Qt 完全解释的 ICC 原始数据，交由应用或其他库处理。

它是一个可复制的隐式共享值类型，不依赖事件循环或窗口对象。副本可安全地按值传递；对某一实例调用 `set*()` 时可能发生分离，多个线程仍不能无同步地同时读写**同一实例**。

## 颜色空间由什么组成

对 RGB 空间，关键数据有三组：

1. **原色（primaries）**：红、绿、蓝在色度图上的坐标，决定色域。
2. **白点（white point）**：参考白的色度与亮度基准。
3. **传递函数（transfer function）**：通道值怎样编码为光强。它可能是线性、sRGB、gamma、PQ（ST 2084）、HLG 或自定义查表曲线。

色域更宽不等于一定更好。源数据若本来是 sRGB，只把标签改成 Display P3 并不会创造新颜色；HDR 的 PQ/HLG 也不能被当成普通 sRGB gamma 数据处理。

## 最小使用

```cpp
#include <QColorSpace>
#include <QColorTransform>

QColorTransform makeDisplayTransform(const QColorSpace &source)
{
    const QColorSpace target(QColorSpace::DisplayP3);
    if (!source.isValid() || !target.isValidTarget())
        return {};

    return source.transformationToColorSpace(target);
}
```

取得 transform 后，应使用相应图像或像素 API 实际转换数据。仅对 `QImage` 调用 `setColorSpace(target)` 是“给现有数值重新贴标签”，不是颜色转换；当图像确实已经处于该空间时才应这样做。

## 最常用的预置空间

| 预置值 | 适用场景 | 要点 |
| --- | --- | --- |
| `SRgb` | 桌面 UI、网页、绝大多数普通图片 | Qt 默认工作空间，兼容性最好。 |
| `SRgbLinear` | 线性光混色、物理渲染中间结果 | 原色与 sRGB 相同，但传递函数线性；不能直接当作普通 sRGB 显示。 |
| `AdobeRgb` | 传统摄影与广色域工作流 | 比 sRGB 宽，使用约 2.2 gamma。 |
| `DisplayP3` | 现代广色域显示器与移动设备 | 使用 DCI-P3 原色、sRGB 白点和传递函数。 |
| `ProPhotoRgb` | 高端照片编辑的超宽色域中间空间 | 色域很宽，转换到有限位深格式时要注意裁剪/量化。 |
| `Bt2020` | HDR 电视基础色彩空间 | Qt 6.8 起提供；自身不是 PQ 或 HLG。 |
| `Bt2100Pq` / `Bt2100Hlg` | HDR 视频 | Qt 6.8 起提供；分别使用 PQ（ST 2084）和 HLG 传递函数。 |

## 有效性与转换方向

`isValid()` 与 `isValidTarget()` 不可混为一谈：

- 对 `ThreeComponentMatrix` 形式的传统 RGB 空间，`isValid()` 要求原色和传递函数均有效，也隐含可作为目标空间。
- 对 `ElementListProcessing` 形式的空间，`isValid()` 只代表它有有效的**源**转换；目标方向是否可用需额外检查 `isValidTarget()`。

这在读取 ICC profile 时很重要。`fromIccProfile()` 目前只支持 RGB 或灰度 ICC profile；不支持的 profile 会得到无效 `QColorSpace`，但 `iccProfile()` 仍可取回原始字节，供应用保留或交给更完整的色彩管理实现。

`ColorModel::Cmyk` 仅面向 CMYK 数据（实务上对应 `QImage::Format_CMYK32`），使用 `ElementListProcessing`。不要假设任意 ICC profile 都能同时作为 Qt 转换的源和目标。

## 自定义空间：何时需要，何时不要碰

日常软件优先选 `NamedColorSpace` 或使用图片嵌入的 ICC profile。只有在你能确认色度坐标、白点和传递函数的来源时，才用 `setPrimaries()`、`setWhitePoint()`、`setTransferFunction()` 或构造函数直接拼装空间。

自定义查表曲线 API 接受 `QList<uint16_t>`；三条独立表用于逐通道曲线。它们适合解析已有 profile 的色彩管理工具，不是用来绘制 UI gamma 曲线的快捷接口。自定义数据不完整时，空间可能无效，创建 transform 前必须检查有效性。

## 常见误区

- **把 `QColorSpace` 当颜色值。** 它不包含“红色 #ff0000”，而是定义 RGB 数据中红色通道意味着什么。
- **用 `setColorSpace()` 代替转换。** 设置元数据不会重新计算像素；转换应使用色彩转换 API。
- **只检查 `isValid()`。** 对 Element List 处理模型，还要检查能否作为目标的 `isValidTarget()`。
- **以为所有 ICC 都被支持。** Qt 内建路径只支持 RGB/灰度 ICC；CMYK 或更复杂 profile 需要验证结果和目标能力。
- **把 `gamma()` 当唯一真相。** 对非 `TransferFunction::Gamma` 空间，它只是近似 gamma；未知时返回 `0.0`。
- **误以为 `description()` 是身份。** 描述仅用于名称/短说明，比较与转换依据实际空间数据。

## API 速查表

### 枚举与数据结构

| API | 含义 | 使用边界 |
| --- | --- | --- |
| `NamedColorSpace` | Qt 预置空间枚举 | `SRgb`、`SRgbLinear`、`AdobeRgb`、`DisplayP3`、`ProPhotoRgb`；`Bt2020`、`Bt2100Pq`、`Bt2100Hlg` 自 Qt 6.8 起可用。 |
| `Primaries` | 已知原色组 | `Custom` 表示不匹配预置原色；可取 `SRgb`、`AdobeRgb`、`DciP3D65`、`ProPhotoRgb`、`Bt2020`。 |
| `TransferFunction` | 已知传递函数 | `Linear`、`Gamma`、`SRgb`、`ProPhotoRgb` 及 Qt 6.8 起的 `Bt2020`、`St2084`、`Hlg`；不匹配时为 `Custom`。 |
| `ColorModel` | 数据颜色模型，Qt 6.8 起 | `Rgb`、`Gray`、`Cmyk`、`Undefined`；CMYK 只适用于 CMYK 数据格式。 |
| `TransformModel` | 转换处理模型，Qt 6.8 起 | `ThreeComponentMatrix` 适于传统三分量矩阵空间；`ElementListProcessing` 可能仅具备源方向转换。 |
| `PrimaryPoints` | 白点和 RGB 原色色度坐标，Qt 6.9 起 | `fromPrimaries()` 从预置原色创建；`isValid()` 验证四个点。 |

### 构造、复制与身份

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `QColorSpace()` | 默认构造 | 得到无效空间；使用前检查 `isValid()`。 |
| `QColorSpace(NamedColorSpace)` | 从预置空间创建 | 常规项目的首选入口。 |
| `QColorSpace(Primaries, TransferFunction, gamma)` | 按预置原色和曲线创建 | `Gamma` 时传入 gamma；其他传递函数中 gamma 不应被误解为完整曲线。 |
| `QColorSpace(Primaries, float gamma)` | 按原色和纯 gamma 创建 | 用于明确的 gamma 曲线。 |
| 以 `QPointF` 白点/原色构造 | 自定义色度坐标 | 坐标含义必须来自可靠 profile 或规范；数据错误会产生错误颜色。 |
| 带 `QList<uint16_t>` 的构造 | 自定义一条或三条传递曲线 | Qt 6.1 起可用；适合 profile 处理而非普通主题色。 |
| `QColorSpace(PrimaryPoints, ...)` | 用结构化原色点构造 | Qt 6.9 起可用；减少四个点参数顺序错误。 |
| 拷贝、移动、赋值 | 值语义传递 | 内部隐式共享；修改副本不应改变另一副本。 |
| `swap(QColorSpace&)` | 交换两个空间 | 快速且不失败；常用于赋值实现或容器算法。 |
| `detach()` | 强制当前对象脱离共享数据 | 很少需手动调用；只有明确需要独占数据时使用。 |
| `operator==` / `operator!=` | 比较空间 | 比较空间内容，不应以 `description()` 或 ICC 字节是否原样相同替代语义判断。 |
| `operator QVariant()` | 转为 `QVariant` | 用于属性、模型或动态数据通道。 |

### 查询有效性与元数据

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `isValid()` | 判断空间是否可用作源 | 矩阵空间要求原色和曲线有效；Element List 空间的“有效”未必意味着可作目标。 |
| `isValidTarget()` | 判断能否作为转换目标 | Qt 6.8 起可用；处理复杂 ICC 或 CMYK 时应单独检查。 |
| `colorModel()` | 获取 `ColorModel` | Qt 6.8 起可用；先确认像素格式是否与模型相容。 |
| `transformModel()` | 获取处理模型 | Qt 6.8 起可用；用它理解 `isValid()` 和 `isValidTarget()` 差异。 |
| `primaries()` | 返回匹配的预置原色 | 无匹配时为 `Primaries::Custom`。 |
| `primaryPoints()` | 取白点和 RGB 原色点 | Qt 6.9 起可用；未定义时返回空点。 |
| `whitePoint()` | 取白点 | Qt 6.8 起可用；未定义时返回空 `QPointF`。 |
| `transferFunction()` | 取匹配的预置曲线 | 不匹配预置曲线时为 `Custom`。 |
| `gamma()` | 取 gamma 或近似 gamma | `Gamma` 空间返回设定值；无可用近似时为 `0.0`。 |
| `description()` / `setDescription()` | 读写显示名称 | Qt 6.2 起；设为空后会回退为原始或推测描述，不能当作唯一 ID。 |

### ICC、转换与序列化

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `fromIccProfile(QByteArray)` | 从 ICC 数据创建空间 | 仅支持 RGB/Gray ICC；不支持时返回无效对象。 |
| `iccProfile()` | 导出或保留 ICC 数据 | 若对象从 ICC 创建则返回原 profile；即使空间无效，也可能取回原始 profile。 |
| `transformationToColorSpace(const QColorSpace&)` | 生成到目标空间的 `QColorTransform` | 源与目标均应先检查可用性，尤其目标需检查 `isValidTarget()`。 |
| `QDataStream <<` | 将空间写入流 | 以 ICC profile 形式序列化。 |
| `QDataStream >>` | 从流恢复空间 | 应处理流状态和 ICC 解析后可能无效的情况。 |

### 修改原色与传递函数

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `setPrimaries(Primaries)` | 设为预置原色 | 只改变原色部分，传递函数仍需有效。 |
| `setPrimaries(white, red, green, blue)` | 设置四个色度点 | 参数顺序固定，错误白点或坐标会导致不正确转换。 |
| `setPrimaryPoints(PrimaryPoints)` | 批量设置色度点 | Qt 6.9 起；可先用 `PrimaryPoints::isValid()` 验证。 |
| `setWhitePoint(QPointF)` | 单独修改白点 | Qt 6.8 起；修改后应重新检查空间有效性。 |
| `setTransferFunction(TransferFunction, gamma)` | 设置预置曲线或 gamma | `Gamma` 才需要有意义的 gamma 参数。 |
| `setTransferFunction(QList<uint16_t>)` | 设置统一的查表曲线 | Qt 6.1 起；用于所有通道共用一条曲线。 |
| `setTransferFunctions(r, g, b)` | 设置三条独立查表曲线 | Qt 6.1 起；面向复杂 profile 的逐通道编码。 |
| `withTransferFunction(...)` | 返回只替换曲线的副本 | 不改变原对象；支持预置曲线或单表，单表重载自 Qt 6.1 起。 |
| `withTransferFunctions(r, g, b)` | 返回替换三条曲线的副本 | Qt 6.1 起；适合保留原色、只派生曲线变体。 |

## 一句话总结

`QColorSpace` 给像素数值以正确的色彩解释，并负责生成跨空间转换。优先采用预置空间或嵌入 ICC，区分“标记色彩空间”和“转换像素”，在复杂 profile 场景中同时检查源有效性与目标有效性。
