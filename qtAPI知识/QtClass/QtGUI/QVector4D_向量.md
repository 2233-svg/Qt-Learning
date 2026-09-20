# QVector4D 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QVector4D>`
> 所属模块：`Qt6::Gui`
> 继承：无

## 它解决什么问题

`QVector4D` 是 Qt GUI 模块中的四维浮点向量值类型，常用于齐次坐标、颜色/参数打包、矩阵变换中间结果，以及需要 `x`、`y`、`z`、`w` 四个分量一起传递的场景。它提供长度、归一化、点乘、按分量运算和向 2D/3D 降维的辅助 API。

四维向量最容易误用的地方是 `w`。在齐次坐标里，`w` 常用于透视除法；但 `QVector4D` 的普通构造和转换 API 不会自动替你判断它是“点”还是“方向”。例如 `QVector3D::toVector4D()` 会把 `w` 设为 `0`，而不是很多图形教材里点坐标常用的 `1`。

## 实际使用场景

- 保存矩阵乘法后的裁剪空间或齐次坐标。
- 表示 RGBA 颜色、四元参数、shader uniform 中的四分量数据。
- 从 3D 坐标加上自定义 `w`，再在需要时做仿射降维。
- 在模型、视图、投影计算之间传递四分量中间值。

## 使用模型

`QVector4D` 是普通值类型，默认构造得到 `(0, 0, 0, 0)`。它没有 QObject 生命周期、父子对象、线程亲和性或事件循环约束。

显式传入的坐标、`w`、缩放因子和除数都应为有限值。任何 NaN 或无穷大都会影响长度、归一化、比较、序列化和降维结果。

下标访问使用 `0`、`1`、`2`、`3` 分别表示 `x`、`y`、`z`、`w`，索引必须满足 `0 <= i < 4`。

## 关键 API 语义与边界

`toVector2D()`、`toVector3D()` 是直接丢弃高维分量；`toVector2DAffine()`、`toVector3DAffine()` 才会按 `w` 做透视/仿射除法。若 `w` 为 0，仿射转换返回零向量，避免除零。

`operator*(QVector4D, QVector4D)` 是按分量相乘，不是点乘。点乘用 `dotProduct()`。四维空间没有这里提供的叉乘 API。

`normalize()` 和 `normalized()` 使用四个分量共同计算长度。零向量归一化仍是零向量；长度接近 `1` 时 Qt 会保留原值。

`operator==` 与 `operator!=` 是精确浮点比较。只要向量来自矩阵、归一化、插值或投影计算，就应考虑 `qFuzzyCompare()` 或业务容差。

`toPoint()` 会丢弃 `z`、`w` 并把 `x`、`y` 四舍五入为整数；这不是用于齐次坐标透视除法的 API。若要按 `w` 降维，先用仿射转换，再转点。

## 常见误区

- 把 `QVector3D(vector).toVector4D()` 当成齐次点。它的 `w` 是 `0`，更像方向向量扩展。
- 需要透视除法时调用了 `toVector3D()`，结果只是丢掉 `w`。
- 误以为 `v1 * v2` 是点乘；它返回逐分量乘出的四维向量。
- 对 `w == 0` 的向量做仿射降维后忘记检查零向量结果。
- 用精确比较判断矩阵计算后的四维向量是否相等。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `[constexpr noexcept] QVector4D()` | 构造零向量 `(0, 0, 0, 0)`。 | 默认值确定。 |
| `[explicit constexpr noexcept] QVector4D(QPoint point)` | 从 `QPoint` 构造四维向量。 | `z`、`w` 填 `0`。 |
| `[explicit constexpr noexcept] QVector4D(QPointF point)` | 从 `QPointF` 构造四维向量。 | `z`、`w` 填 `0`。 |
| `[explicit constexpr noexcept] QVector4D(QVector2D vector)` | 从 2D 向量构造四维向量。 | `z`、`w` 填 `0`。 |
| `[explicit constexpr noexcept] QVector4D(QVector3D vector)` | 从 3D 向量构造四维向量。 | `w` 填 `0`，不是 `1`。 |
| `[constexpr noexcept] QVector4D(QVector3D vector, float wpos)` | 从 3D 向量加指定 `w` 构造。 | `wpos` 应为有限值；齐次点常显式传 `1`。 |
| `[constexpr noexcept] QVector4D(QVector2D vector, float zpos, float wpos)` | 从 2D 向量加指定 `z`、`w` 构造。 | `zpos`、`wpos` 都应为有限值。 |
| `[constexpr noexcept] QVector4D(float xpos, float ypos, float zpos, float wpos)` | 用四个分量构造向量。 | 所有参数都应为有限值。 |
| `[static constexpr noexcept] float dotProduct(QVector4D v1, QVector4D v2)` | 返回两个四维向量的点乘。 | 返回标量；不要和逐分量乘法混淆。 |
| `[constexpr noexcept] bool isNull() const` | 判断四个分量是否为零。 | 不是容差判断。 |
| `[noexcept] float length() const` | 返回四维长度。 | 会开方；比较时可用 `lengthSquared()`。 |
| `[constexpr noexcept] float lengthSquared() const` | 返回长度平方。 | 等价于自身点乘。 |
| `[noexcept] void normalize()` | 原地归一化为单位长度。 | 零向量不变；长度接近 `1` 时不扰动。 |
| `[noexcept] QVector4D normalized() const` | 返回归一化后的副本。 | 当前对象不变；零向量返回零向量。 |
| `[constexpr noexcept] void setW(float w)` | 修改 `w` 分量。 | 参数应为有限值；会影响仿射降维。 |
| `[constexpr noexcept] void setX(float x)` | 修改 `x` 分量。 | 参数应为有限值。 |
| `[constexpr noexcept] void setY(float y)` | 修改 `y` 分量。 | 参数应为有限值。 |
| `[constexpr noexcept] void setZ(float z)` | 修改 `z` 分量。 | 参数应为有限值。 |
| `[constexpr noexcept] QPoint toPoint() const` | 转为 `QPoint`。 | 丢弃 `z`、`w`，`x`、`y` 四舍五入；不会除以 `w`。 |
| `[constexpr noexcept] QPointF toPointF() const` | 转为 `QPointF`。 | 丢弃 `z`、`w`，保留浮点 `x`、`y`。 |
| `[constexpr noexcept] QVector2D toVector2D() const` | 直接降为 2D 向量。 | 丢弃 `z`、`w`，不会做透视除法。 |
| `[constexpr noexcept] QVector2D toVector2DAffine() const` | 以 `w` 做仿射除法后降为 2D。 | 返回 `(x / w, y / w)`；`w == 0` 时返回零向量。 |
| `[constexpr noexcept] QVector3D toVector3D() const` | 直接降为 3D 向量。 | 丢弃 `w`，不会做透视除法。 |
| `[constexpr noexcept] QVector3D toVector3DAffine() const` | 以 `w` 做仿射除法后降为 3D。 | 返回 `(x / w, y / w, z / w)`；`w == 0` 时返回零向量。 |
| `[constexpr noexcept] float w() const` | 返回 `w` 分量。 | 只读访问。 |
| `[constexpr noexcept] float x() const` | 返回 `x` 分量。 | 只读访问。 |
| `[constexpr noexcept] float y() const` | 返回 `y` 分量。 | 只读访问。 |
| `[constexpr noexcept] float z() const` | 返回 `z` 分量。 | 只读访问。 |
| `operator QVariant() const` | 把四维向量包装为 `QVariant`。 | 方便属性系统、模型数据和动态调用。 |
| `[constexpr noexcept] QVector4D &operator*=(QVector4D vector)` | 原地逐分量乘以另一个向量。 | 不是点乘。 |
| `[constexpr noexcept] QVector4D &operator*=(float factor)` | 原地按标量缩放。 | `factor` 应为有限值。 |
| `[constexpr noexcept] QVector4D &operator+=(QVector4D vector)` | 原地逐分量相加。 | 修改自身。 |
| `[constexpr noexcept] QVector4D &operator-=(QVector4D vector)` | 原地逐分量相减。 | 修改自身。 |
| `[constexpr] QVector4D &operator/=(QVector4D vector)` | 原地逐分量相除。 | 除数每个分量都不能为 `0` 或 NaN。 |
| `[constexpr] QVector4D &operator/=(float divisor)` | 原地除以标量。 | `divisor` 不能为 `0` 或 NaN。 |
| `[constexpr] float &operator[](int i)` | 按索引返回可修改分量引用。 | `0`/`1`/`2`/`3` 对应 `x`/`y`/`z`/`w`；索引必须合法。 |
| `[constexpr] float operator[](int i) const` | 按索引返回分量值。 | `0 <= i < 4`。 |
| `[noexcept] bool qFuzzyCompare(QVector4D v1, QVector4D v2)` | 以 Qt 浮点模糊规则比较两个向量。 | 适合矩阵、归一化、插值后的结果。 |
| `[constexpr noexcept] bool operator!=(QVector4D v1, QVector4D v2)` | 精确判断两个向量不相等。 | 对计算结果要谨慎。 |
| `[constexpr noexcept] QVector4D operator*(QVector4D v1, QVector4D v2)` | 返回逐分量乘法结果。 | 不是点乘；点乘用 `dotProduct()`。 |
| `[constexpr noexcept] QVector4D operator*(QVector4D vector, float factor)` | 返回标量缩放后的副本。 | 不修改原对象。 |
| `[constexpr noexcept] QVector4D operator*(float factor, QVector4D vector)` | 返回标量缩放后的副本。 | 与 `vector * factor` 语义相同。 |
| `[constexpr noexcept] QVector4D operator+(QVector4D v1, QVector4D v2)` | 返回逐分量相加结果。 | 不修改参数。 |
| `[constexpr noexcept] QVector4D operator-(QVector4D v1, QVector4D v2)` | 返回逐分量相减结果。 | 不修改参数。 |
| `[constexpr noexcept] QVector4D operator-(QVector4D vector)` | 返回所有分量取反的新向量。 | 文档描述为改变分量符号。 |
| `[constexpr] QVector4D operator/(QVector4D vector, QVector4D divisor)` | 返回逐分量除法结果。 | `divisor` 每个分量都不能为 `0` 或 NaN。 |
| `[constexpr] QVector4D operator/(QVector4D vector, float divisor)` | 返回除以标量后的副本。 | `divisor` 不能为 `0` 或 NaN。 |
| `QDataStream &operator<<(QDataStream &stream, QVector4D vector)` | 把向量写入数据流。 | 读写双方使用兼容的流版本。 |
| `[constexpr noexcept] bool operator==(QVector4D v1, QVector4D v2)` | 精确判断两个向量相等。 | 直接比较四个浮点分量；计算结果建议模糊比较。 |
| `QDataStream &operator>>(QDataStream &stream, QVector4D &vector)` | 从数据流读入向量。 | 读取后检查 `QDataStream` 状态。 |

## 一句话总结

`QVector4D` 是四分量数据和齐次坐标的轻量载体；真正的关键是永远知道自己是在丢弃 `w`，还是在按 `w` 做仿射降维。
