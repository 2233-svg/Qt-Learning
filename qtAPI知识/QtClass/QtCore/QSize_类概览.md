# QSize：表达整数宽高，而不是坐标或矩形

> 适用版本：Qt 6.11.1  
> 所属头文件：`#include <QSize>`  
> 所属模块：Qt Core

`QSize` 是只包含整数 `width` 和 `height` 的轻量值类型。它表达图片尺寸、控件建议大小、表格格子大小、缓冲区分辨率和布局约束，不携带位置；需要位置加尺寸时用 `QRect`，需要连续坐标时用 `QSizeF`。

它的核心边界在于：`valid`、`empty` 和 `null` 不是同义词。零尺寸仍是 valid，默认构造的负尺寸才是 invalid。

## 基本使用

```cpp
QSize thumbnail(320, 180);

if (thumbnail.isValid() && !thumbnail.isEmpty()) {
    renderThumbnail(thumbnail);
}
```

典型用途：

- `QWidget::sizeHint()`、图像和视频帧的像素宽高；
- 在目标框内按比例缩放图片；
- 用最小/最大尺寸约束布局；
- 与 `QRect`、`QMargins` 组合计算绘制或裁剪范围。

不要用 `QSize` 表示“右下角坐标”或“两个点的差”而不先确认符号含义。负宽高可暂时表达未初始化或反向计算结果，但不能直接交给需要真实尺寸的绘制、图像或布局 API。

## 状态：valid、empty 与 null

```cpp
QSize invalid;        // 默认是 (-1, -1)
QSize nullSize(0, 0);
QSize flat(0, 120);
QSize normal(120, 80);
```

| 状态 | 条件 | 示例 | 含义 |
| --- | --- | --- | --- |
| `isValid()` | 宽高都大于等于 0 | `(0, 120)`、`(0, 0)` | 数值合法，可参与尺寸语义。 |
| `isEmpty()` | 宽或高小于等于 0 | `(0, 120)`、`(-1, 4)` | 没有可用面积。 |
| `isNull()` | 宽和高都等于 0 | `(0, 0)` | empty 的特殊情形。 |

因此 `QSize(0, 120)` 同时 valid 和 empty；默认值 `(-1, -1)` invalid 且 empty；`QSize(0, 0)` 则 valid、empty、null。代码若要真实可渲染区域，一般同时判断 `isValid()` 和 `!isEmpty()`。

## 缩放：三种纵横比模式

`scale()` 原地修改，`scaled()` 返回副本。两者都把当前尺寸缩放到目标框内或目标框外，行为由 `Qt::AspectRatioMode` 决定：

```cpp
const QSize source(400, 300);
const QSize box(200, 200);

const QSize stretched = source.scaled(box, Qt::IgnoreAspectRatio);
const QSize fit = source.scaled(box, Qt::KeepAspectRatio);
const QSize cover = source.scaled(box, Qt::KeepAspectRatioByExpanding);
```

| 模式 | 结果 | 常用场景 |
| --- | --- | --- |
| `IgnoreAspectRatio` | 强制等于目标宽高，可能变形。 | 纯布局占位、无需保比例的坐标缩放。 |
| `KeepAspectRatio` | 完整放进目标框，至少一个方向可能留白。 | 图片完整预览、letterbox。 |
| `KeepAspectRatioByExpanding` | 覆盖目标框，至少一个方向会超出。 | 头像或背景图，随后用裁剪框截取。 |

`QSize` 是整数类型，缩放和乘除会产生整数结果并涉及取整。连续缩放、动画或累计比例计算应尽量使用 `QSizeF`，最后一次性转换为 `QSize`；反复在整数尺寸上缩放会累积像素误差。

对 invalid 或 empty 尺寸做按比例缩放没有可用的几何比例。先检查源尺寸和目标框是否具有正宽高，特别是除法、图像解码尺寸和从外部配置读取的值。

## 尺寸约束与 margin

`expandedTo()` 逐分量取最大值，常用于最小尺寸约束；`boundedTo()` 逐分量取最小值，常用于上限约束：

```cpp
const QSize requested(900, 80);
const QSize maxAllowed(640, 480);

const QSize clamped = requested.boundedTo(maxAllowed);
```

这不是保持纵横比的缩放，只是独立地取宽高最大/最小值。对图片等需要比例不变的对象，使用 `scaled()`。

`grownBy(QMargins)` 将左右 margin 加到宽度、上下 margin 加到高度；`shrunkBy()` 做相反操作：

```cpp
const QSize content(200, 100);
const QMargins frame(4, 8, 4, 8);
const QSize outer = content.grownBy(frame); // (208, 116)
```

过度 shrink 会产生零或负尺寸，之后根据使用场景 `boundedTo(QSize())`、拒绝输入或判断 `isEmpty()`，不要默默把 invalid 尺寸传给下游。

## 直接引用与算术运算

`rwidth()`、`rheight()` 返回内部成员引用：

```cpp
QSize size(100, 10);
size.rheight() += 5; // (100, 15)
```

它们适合极少量局部就地调整，但会绕开命名清晰的 setter。不要保存这些引用跨越对象移动、销毁或容器重分配；更不要在多线程共享同一 `QSize` 时通过引用修改它。

`+=`、`-=`、`*=`、`/=` 逐分量原地运算；相应的非成员 `+`、`-`、`*`、`/` 返回新值。整数版本的乘除结果会取整，除数为 0 没有有效的业务语义，应在调用前验证。

`QSize` 分量底层是 `int`；超出整数范围的累计 margin、乘法和缩放不可依赖。大图或外部输入先做范围上限控制。

## 平台与类型转换

`toSizeF()` 从 Qt 6.4 起提供，把整数尺寸无损提升为 `QSizeF`，适合进入浮点几何计算。

`toCGSize()` 仅在 Apple 平台可用，用于 Core Graphics 互操作。它不改变整数尺寸语义，也不解除 macOS/iOS 图形 API 自身的线程与坐标系统约束。

`QSize` 是纯值类型，没有 QObject 线程亲和性；但从 `QWidget`、`QWindow`、`QImage` 等对象取得的大小仍必须遵守各自的生命周期和线程规则。

## 常见错误

1. **把 valid 当作有面积。** `(0, n)` valid 但 empty。
2. **以为默认值是 `(0, 0)`。** 默认 `QSize()` 是 invalid。
3. **用 `boundedTo()` 保持图片比例。** 它只是逐分量截断；比例缩放用 `scaled()`。
4. **反复整数缩放。** 会累计取整误差，连续计算用 `QSizeF`。
5. **用 `rwidth()` / `rheight()` 长期保存引用。** 引用只适合短生命周期局部修改。
6. **忽略 shrink 或算术后的负值。** 后续绘制和布局前检查状态。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `QSize()` | 构造 invalid 默认尺寸。 | 默认宽高为负，不是 `(0, 0)`。 |
| `QSize(width, height)` | 构造指定整数宽高。 | 允许负值，但负值不是可用尺寸。 |
| `width()` / `height()` | 读取分量。 | 不保证结果为正。 |
| `setWidth()` / `setHeight()` | 设置单一分量。 | 可能令尺寸 empty 或 invalid。 |
| `rwidth()` / `rheight()` | 返回分量的可写引用。 | 仅作短时局部修改，不长期保存引用。 |
| `isValid()` | 宽高都大于等于 0。 | `(0, n)` 仍 valid。 |
| `isEmpty()` | 宽或高小于等于 0。 | 用于判断没有可用面积。 |
| `isNull()` | 宽高都为 0。 | 是 empty 的特殊情形。 |
| `scale(width, height, mode)` | 原地缩放到目标框。 | 先验证源和目标尺寸；整数结果会取整。 |
| `scale(QSize, mode)` | 以目标 `QSize` 原地缩放。 | 与标量 overload 语义相同。 |
| `scaled(width, height, mode)` | 返回缩放后的副本。 | 保留原 size，适合表达式计算。 |
| `scaled(QSize, mode)` | 以目标 size 返回缩放副本。 | `KeepAspectRatioByExpanding` 后通常还需裁剪。 |
| `expandedTo(other)` | 逐分量取较大值。 | 适合最小尺寸约束，不保持比例。 |
| `boundedTo(other)` | 逐分量取较小值。 | 适合最大尺寸约束，不保持比例。 |
| `grownBy(QMargins)` | 返回加上四边 margin 后的尺寸。 | 宽加 left/right，高加 top/bottom。 |
| `shrunkBy(QMargins)` | 返回减去四边 margin 后的尺寸。 | 结果可能 empty 或 invalid。 |
| `transpose()` | 原地交换宽和高。 | 修改当前对象。 |
| `transposed()` | 返回宽高交换的副本。 | 原对象保持不变。 |
| `operator+=` / `operator-=` | 原地逐分量加/减 size。 | 可能产生负值或溢出。 |
| `operator*=` / `operator/=` | 原地按 `qreal` 缩放。 | 整数结果有取整；除数不能为 0。 |
| `operator+` / `operator-` | 返回逐分量和/差。 | 不是矩形并/差。 |
| `operator*` / `operator/` | 返回缩放后的 size。 | 结果向最近整数取整；避免重复变换。 |
| `==` / `!=` | 精确比较宽和高。 | 与 `QSizeF` 的模糊比较不同。 |
| `toSizeF()` | 转为浮点尺寸。 | Qt 6.4 起；适合进入连续几何计算。 |
| `toCGSize()` | 转为 Apple `CGSize`。 | 仅 Apple 平台可用。 |
| `QDataStream <<` / `>>` | 序列化与反序列化。 | 外部数据读入后应验证尺寸范围。 |

## 一句话总结

`QSize` 只表达整数宽高：默认值 invalid，零尺寸 valid 但 empty；布局约束用 `expandedTo()` / `boundedTo()`，保比例缩放用 `scaled()`，连续比例计算则尽量延后到 `QSizeF`。
