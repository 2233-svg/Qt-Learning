# QSizeF：用于连续几何和缩放的有限浮点宽高

> 适用版本：Qt 6.11.1  
> 所属头文件：`#include <QSizeF>`  
> 所属模块：Qt Core

`QSizeF` 是 `QSize` 的浮点版本，保存 `qreal` 宽高。它适合高 DPI 缩放、动画插值、矢量绘制、视图变换和连续布局计算。和 `QSize` 一样，它不携带位置；需要位置加尺寸时使用 `QRectF`。

它的关键边界是浮点数：构造、设置与缩放因子要求有限值；相等运算是模糊比较；转回 `QSize` 会饱和并四舍五入。不要把它当作“整数尺寸换成 double 后一切语义不变”。

## 基本使用

```cpp
QSizeF logicalSize(144.0, 81.0);
const qreal scaleFactor = 1.25;

const QSizeF deviceIndependent = logicalSize * scaleFactor;
```

典型场景：

- 缩放和动画中的中间尺寸；
- `QPainter`、`QGraphicsItem`、Qt Quick 的连续几何；
- 根据屏幕缩放因子计算布局；
- 最后一步才转换成 `QSize` 交给像素 API。

如果尺寸从图像像素、窗口大小或整数表格列数直接得到，`QSize` 更合适；不需要小数时不要无故引入浮点比较和取整策略。

## 有限性、有效性、空尺寸

```cpp
QSizeF invalid;           // invalid
QSizeF nullSize(0.0, 0.0);
QSizeF flat(0.0, 24.5);
QSizeF normal(24.5, 10.0);
```

状态条件和 `QSize` 基本一致：

| 状态 | 条件 | 说明 |
| --- | --- | --- |
| `isValid()` | 宽高都大于等于 0 | 零尺寸仍 valid。 |
| `isEmpty()` | 宽或高小于等于 0 | 无可用面积。 |
| `isNull()` | 宽高都是 `0.0`，忽略正负零符号 | empty 的特殊情形。 |

因此 `(0.0, 20.0)` valid 但 empty。需要真实可渲染面积时，检查 `isValid() && !isEmpty()`。

`QSizeF(qreal width, qreal height)`、`setWidth()`、`setHeight()`、`scale()`、乘法相关 API 的输入应是有限数。不要让 `NaN` 或无穷来自除零、未初始化计算或外部 JSON 后进入尺寸；一旦发生，`qMax`、相等、缩放和下游绘制不再有可靠语义。除法的除数不得为 0 或 `NaN`。

## 缩放与纵横比

`scale()` 原地修改，`scaled()` 返回副本：

```cpp
const QSizeF original(10.0, 12.0);
const QSizeF target(60.0, 60.0);

const QSizeF fit = original.scaled(target, Qt::KeepAspectRatio);
const QSizeF cover = original.scaled(target, Qt::KeepAspectRatioByExpanding);
```

三种模式与 `QSize` 相同：

- `IgnoreAspectRatio`：强制匹配目标宽高，可能变形；
- `KeepAspectRatio`：完整容纳在目标内，可能留白；
- `KeepAspectRatioByExpanding`：覆盖目标，可能超出后续裁剪范围。

浮点版本的优势是中间步骤不取整。比如连续动画每帧调整 0.25 像素时，用 `QSizeF` 累积，最后需要像素边界时再明确转换。这避免了每帧转整数导致的卡顿或尺寸抖动。

源或目标为 zero/negative 尺寸时，比例含义不成立。先校验输入，而不是把异常尺寸交给 `scaled()` 再寄望于某种“自动修正”。

## 约束、margin 与转置

`expandedTo()` 和 `boundedTo()` 独立处理两个分量：

```cpp
const QSizeF minimum(48.0, 24.0);
const QSizeF requested(32.5, 90.0);

const QSizeF enforcedMinimum = requested.expandedTo(minimum);
```

它们适用于最小/最大布局约束，不保持纵横比。若对象必须保持比例，应使用 `scaled()`。

`grownBy(QMarginsF)` 增加左右、上下 margin；`shrunkBy(QMarginsF)` 减去它们。过度 shrink 会得到 empty/invalid 尺寸，调用方必须决定是拒绝、截断还是继续以空尺寸处理。

`transpose()` 原地交换宽高；`transposed()` 返回副本。它只交换两个数值，不含旋转、位置改变或坐标变换语义。

## 浮点比较不是精确比较

`QSizeF::operator==` / `operator!=` 使用模糊比较。它适合判断两个布局计算结果在 Qt 容差内是否近似相同：

```cpp
if (currentSize == targetSize) {
    // 近似相等，不是逐位相等
}
```

Qt 6.8 起提供 `qFuzzyCompare(lhs, rhs)` 和 `qFuzzyIsNull(size)`，让代码明确表达近似比较意图。

不要用 `QSizeF` 的 `==` 作为：

- 精确序列化完整性检查；
- 哈希键或缓存键；
- 需要严格传递性的排序/去重规则；
- 单元测试中的严格浮点断言。

这些情形应按业务误差范围比较 `width()`、`height()`，或使用精确整数单位表示尺寸。

## 与 QSize 和平台类型转换

```cpp
const QSizeF logical(127.6, 63.4);
const QSize pixels = logical.toSize();
```

`toSize()` 按最近整数转换，并对超出 `int` 范围的值做饱和处理。它不保证“完整覆盖”原浮点尺寸；若转换用于绘制覆盖范围，结合 `QRectF::toAlignedRect()` 选择更合适的外扩策略，而不是只转换尺寸后猜测位置与边界。

从 `QSize` 构造或比较 `QSizeF` 时，整数值可精确提升为浮点表示。`QSize::toSizeF()` 从 Qt 6.4 起提供。

`fromCGSize()` / `toCGSize()` 仅在 Apple 平台可用，用于 Core Graphics 互操作。它们只转换尺寸值，不代表任何 GUI 对象可以跨线程或跨坐标系统直接使用。

## 直接引用、算术与生命周期

`rwidth()` / `rheight()` 返回可写 `qreal &`，仅适合短小局部更新：

```cpp
QSizeF size(100.0, 10.2);
size.rheight() += 5.5;
```

不要把引用保存到对象外，也不要把它作为跨线程共享状态的修改入口。

`+=`、`-=`、`*=`、`/=` 和对应非成员运算符逐分量计算。乘数必须有限，除数不能是 0 或 NaN。算术之后依然需要检查 `isValid()` / `isEmpty()`，因为减法、负 factor 或 margin 收缩都可以产生负尺寸。

`QSizeF` 是纯值类型，无 QObject 生命周期和线程亲和性；同一实例的并发读写仍需要同步。

## 常见错误

1. **把浮点 size 当作自动容忍 NaN 的容器。** API 约定有限输入。
2. **把 `==` 当严格比较。** QSizeF 的相等是模糊的。
3. **把 `toSize()` 当保守外扩。** 它是就近取整；完整覆盖要在矩形/位置层面处理。
4. **反复 `toSize()` 再转回 `QSizeF`。** 会持续丢失小数信息。
5. **忘记 zero 尺寸 valid 但 empty。** 布局或绘制前常需同时检查。
6. **除以 0 或 NaN。** 先校验缩放参数。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `QSizeF()` | 构造 invalid 默认尺寸。 | 默认不是 `(0.0, 0.0)`。 |
| `QSizeF(QSize)` | 从整数尺寸无损提升。 | 适合开始连续计算。 |
| `QSizeF(width, height)` | 构造浮点尺寸。 | 宽高必须有限。 |
| `width()` / `height()` | 读取 `qreal` 分量。 | 不保证正值或有限性由外部输入自动保证。 |
| `setWidth()` / `setHeight()` | 设置单一浮点分量。 | 传入值必须有限，可能产生 empty/invalid。 |
| `rwidth()` / `rheight()` | 取得可写分量引用。 | 仅短时局部使用，不能保存。 |
| `isValid()` | 宽高都大于等于 0。 | 零尺寸仍 valid。 |
| `isEmpty()` | 宽或高小于等于 0。 | 作为“没有面积”判断。 |
| `isNull()` | 宽高均为 0，忽略正负零。 | 近似零用 `qFuzzyIsNull()`。 |
| `scale(width, height, mode)` | 原地按目标框缩放。 | 参数必须有限；连续计算保留浮点精度。 |
| `scale(QSizeF, mode)` | 按目标 size 原地缩放。 | 先确认源和目标的比例可定义。 |
| `scaled(width, height, mode)` | 返回缩放副本。 | 不改变原对象。 |
| `scaled(QSizeF, mode)` | 按目标 size 返回缩放副本。 | 覆盖模式后通常仍需裁剪。 |
| `expandedTo(other)` | 逐分量取较大值。 | 用于最小尺寸限制，不保持比例。 |
| `boundedTo(other)` | 逐分量取较小值。 | 用于最大尺寸限制，不保持比例。 |
| `grownBy(QMarginsF)` | 返回加 margin 后的尺寸。 | 宽加左右，高加上下。 |
| `shrunkBy(QMarginsF)` | 返回减 margin 后的尺寸。 | 过度收缩可能无效。 |
| `transpose()` / `transposed()` | 原地或副本式交换宽高。 | 不是几何旋转。 |
| `operator+=` / `operator-=` | 原地逐分量加减。 | 算后检查尺寸状态。 |
| `operator*=` / `operator/=` | 原地乘除 factor。 | factor 必须有限；除数不能为 0 或 NaN。 |
| `operator+` / `operator-` | 返回逐分量和/差。 | 不是矩形区域运算。 |
| `operator*` / `operator/` | 返回缩放后的浮点 size。 | 保留小数，但仍受有限因子/除数前置条件约束。 |
| `qFuzzyCompare(lhs, rhs)` | 近似比较两个尺寸。 | Qt 6.8 起；适合显式容差语义。 |
| `qFuzzyIsNull(size)` | 判断宽高是否都近似零。 | Qt 6.8 起；不同于严格 `isNull()`。 |
| `==` / `!=` | 模糊相等/不等比较。 | 不可作严格身份或哈希键判断。 |
| `toSize()` | 转为整数 size。 | 饱和并就近取整；可能丢失小数与覆盖关系。 |
| `fromCGSize()` / `toCGSize()` | 与 Apple `CGSize` 转换。 | 仅 Apple 平台可用。 |
| `QDataStream <<` / `>>` | 序列化与反序列化。 | 读取外部浮点值后验证有限性与合理范围。 |

## 一句话总结

`QSizeF` 用于把尺寸计算留在连续坐标中：只接受有限数，零尺寸 valid 但 empty，比较是模糊的，转回 `QSize` 会饱和取整；把取整留到真正进入像素 API 的最后一步。
