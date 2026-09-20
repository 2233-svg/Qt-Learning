# QVector3D 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QVector3D>`
> 所属模块：`Qt6::Gui`
> 继承：无

## 它解决什么问题

`QVector3D` 是 Qt GUI 模块中的三维浮点向量值类型，用来表达 3D 空间里的位置、方向、法线、位移或顶点。相比 `QVector2D`，它多了 `z` 分量和 3D 几何常用操作，例如叉乘、平面法线、点到平面距离，以及在对象坐标和窗口坐标之间投影/反投影。

它不是图形资源，也不持有 GPU 内存；它只是一个普通 C++ 值。真正的矩阵变换由 `QMatrix4x4` 等类型完成，`QVector3D` 负责承载向量并提供常见数学辅助。

## 实际使用场景

- 表示模型顶点、相机位置、光照方向、法线方向。
- 计算点到点、点到线、点到平面的距离。
- 用 `crossProduct()` 得到两个方向张成平面的垂直方向。
- 在 OpenGL/Qt Quick 辅助代码中把模型坐标投影到窗口坐标，或把鼠标窗口坐标反投影回模型空间。

## 使用模型

`QVector3D` 是小型值类型，默认构造得到 `(0, 0, 0)`。它没有 QObject 所有权、线程亲和性或事件循环约束，可以放心传值、返回、放入容器。

显式传入的坐标和缩放因子应为有限浮点数。`NaN`、正负无穷会污染后续长度、法线、投影和比较逻辑。

下标访问使用 `0`、`1`、`2` 分别表示 `x`、`y`、`z`。`operator[]` 要求索引满足 `0 <= i < 3`。

## 关键 API 语义与边界

`dotProduct()` 返回标量，主要用于夹角、投影和方向一致性判断。`crossProduct()` 返回与两个输入向量垂直的向量；如果两个向量平行，结果为零向量。

`normal()` 返回单位法线，输入向量或三点定义的平面不能退化为平行/共线。如果不需要单位长度，或者输入可能退化，应先用 `crossProduct()` 并自行检查长度。

`distanceToPlane(QVector3D plane, QVector3D normal)` 假设传入的 `normal` 已经是单位向量。若传普通未归一化方向，结果会按法线长度缩放，不再是真实距离。

`project()` 与 `unproject()` 依赖 `modelView`、`projection` 和 `viewport` 三者一致。它们在裁剪坐标到归一化空间转换时会除以 `w`；当 `w` 为 0 时 Qt 会把它当作 1 来避免除零，这只是数值保护，不代表投影关系一定有几何意义。

`operator*(QVector3D, QVector3D)` 是逐分量乘法，不是点乘，也不是叉乘。点乘用 `dotProduct()`，叉乘用 `crossProduct()`。

## 常见误区

- 把 `normal()` 当成无条件安全函数。输入平行或共线时平面法线没有定义。
- `distanceToPlane()` 传入未归一化法线，距离结果被放大或缩小。
- 误以为 `v1 * v2` 是点乘或叉乘；Qt 这里返回逐分量乘出的 `QVector3D`。
- 用精确 `operator==` 比较矩阵变换后的结果。
- 忽略 `project()`/`unproject()` 的 viewport 坐标系和矩阵配套关系，导致屏幕拾取偏移。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `[constexpr noexcept] QVector3D()` | 构造零向量 `(0, 0, 0)`。 | 默认值是确定的零向量。 |
| `[explicit constexpr noexcept] QVector3D(QPoint point)` | 从 `QPoint` 构造三维向量。 | `z` 填 `0`，整数坐标转 `float`。 |
| `[explicit constexpr noexcept] QVector3D(QPointF point)` | 从 `QPointF` 构造三维向量。 | `z` 填 `0`。 |
| `[explicit constexpr noexcept] QVector3D(QVector2D vector)` | 从 2D 向量构造三维向量。 | `z` 填 `0`。 |
| `[explicit constexpr noexcept] QVector3D(QVector4D vector)` | 从 4D 向量构造三维向量。 | 直接丢弃 `w`，不会做透视除法。 |
| `[constexpr noexcept] QVector3D(QVector2D vector, float zpos)` | 从 2D 向量加指定 `z` 构造。 | `zpos` 应为有限值。 |
| `[constexpr noexcept] QVector3D(float xpos, float ypos, float zpos)` | 用三个浮点分量构造向量。 | 所有参数都应为有限值。 |
| `[static constexpr noexcept] QVector3D crossProduct(QVector3D v1, QVector3D v2)` | 返回两个向量的叉乘。 | 结果垂直于二者张成的平面；输入平行时为零向量。 |
| `[noexcept] float distanceToLine(QVector3D point, QVector3D direction) const` | 计算当前顶点到直线的距离。 | `direction` 应为单位向量；零方向时退化为到 `point` 的距离。 |
| `[constexpr noexcept] float distanceToPlane(QVector3D plane, QVector3D normal) const` | 计算当前顶点到由一点和单位法线定义的平面的距离。 | `normal` 必须已归一化，否则结果不是实际距离。 |
| `[noexcept] float distanceToPlane(QVector3D plane1, QVector3D plane2, QVector3D plane3) const` | 计算当前顶点到三点定义平面的距离。 | 三点不应共线或重合。 |
| `[noexcept] float distanceToPoint(QVector3D point) const` | 计算当前顶点到另一个点的欧氏距离。 | 返回真实距离，会涉及平方根。 |
| `[static constexpr noexcept] float dotProduct(QVector3D v1, QVector3D v2)` | 返回两个向量的点乘标量。 | 用于夹角、投影、方向相似度。 |
| `[constexpr noexcept] bool isNull() const` | 判断 `x`、`y`、`z` 是否为零。 | 不是容差判断。 |
| `[noexcept] float length() const` | 返回向量长度。 | 会开方；比较大小可优先考虑 `lengthSquared()`。 |
| `[constexpr noexcept] float lengthSquared() const` | 返回长度平方。 | 等价于自身点乘，适合阈值比较。 |
| `[static noexcept] QVector3D normal(QVector3D v1, QVector3D v2)` | 返回由 `v1`、`v2` 张成平面的单位法线。 | 两个向量不能平行；不需要单位长度时用 `crossProduct()`。 |
| `[static noexcept] QVector3D normal(QVector3D v1, QVector3D v2, QVector3D v3)` | 返回三点定义平面的单位法线。 | 实际基于 `v2 - v1` 与 `v3 - v1`；三点不能共线。 |
| `[noexcept] void normalize()` | 原地归一化为单位向量。 | 零向量不变；长度接近 `1` 时不扰动。 |
| `[noexcept] QVector3D normalized() const` | 返回归一化后的副本。 | 当前对象不变；零向量返回零向量。 |
| `QVector3D project(const QMatrix4x4 &modelView, const QMatrix4x4 &projection, const QRect &viewport) const` | 把对象/模型坐标转换为窗口坐标。 | 矩阵和 viewport 必须匹配当前渲染状态；`w == 0` 时 Qt 用 1 避免除零。 |
| `[constexpr noexcept] void setX(float x)` | 修改 `x` 分量。 | 参数应为有限值。 |
| `[constexpr noexcept] void setY(float y)` | 修改 `y` 分量。 | 参数应为有限值。 |
| `[constexpr noexcept] void setZ(float z)` | 修改 `z` 分量。 | 参数应为有限值。 |
| `[constexpr noexcept] QPoint toPoint() const` | 转为 `QPoint`。 | 丢弃 `z`，`x`、`y` 四舍五入为整数。 |
| `[constexpr noexcept] QPointF toPointF() const` | 转为 `QPointF`。 | 丢弃 `z`，保留 `x`、`y` 浮点值。 |
| `[constexpr noexcept] QVector2D toVector2D() const` | 降为 2D 向量。 | 丢弃 `z`。 |
| `[constexpr noexcept] QVector4D toVector4D() const` | 扩展为 4D 向量。 | `w` 填 `0`，不是齐次点常见的 `1`。 |
| `QVector3D unproject(const QMatrix4x4 &modelView, const QMatrix4x4 &projection, const QRect &viewport) const` | 把窗口坐标反投影为对象/模型坐标。 | 与 `project()` 使用同一组矩阵和 viewport；常用于拾取。 |
| `[constexpr noexcept] float x() const` | 返回 `x` 分量。 | 只读访问。 |
| `[constexpr noexcept] float y() const` | 返回 `y` 分量。 | 只读访问。 |
| `[constexpr noexcept] float z() const` | 返回 `z` 分量。 | 只读访问。 |
| `operator QVariant() const` | 把向量包装为 `QVariant`。 | 方便属性、模型和动态数据通道。 |
| `[constexpr noexcept] QVector3D &operator*=(float factor)` | 原地按标量缩放。 | `factor` 应为有限值。 |
| `[constexpr noexcept] QVector3D &operator*=(QVector3D vector)` | 原地逐分量相乘。 | 不是点乘或叉乘。 |
| `[constexpr noexcept] QVector3D &operator+=(QVector3D vector)` | 原地逐分量相加。 | 修改自身。 |
| `[constexpr noexcept] QVector3D &operator-=(QVector3D vector)` | 原地逐分量相减。 | 修改自身。 |
| `[constexpr] QVector3D &operator/=(QVector3D vector)` | 原地逐分量相除。 | 除数每个分量都不能为 `0` 或 NaN。 |
| `[constexpr] QVector3D &operator/=(float divisor)` | 原地除以标量。 | `divisor` 不能为 `0` 或 NaN。 |
| `[constexpr] float &operator[](int i)` | 按索引返回可修改分量引用。 | `0`/`1`/`2` 对应 `x`/`y`/`z`；索引必须合法。 |
| `[constexpr] float operator[](int i) const` | 按索引返回分量值。 | `0 <= i < 3`。 |
| `[noexcept] bool qFuzzyCompare(QVector3D v1, QVector3D v2)` | 以 Qt 浮点模糊规则比较两个向量。 | 适合矩阵、归一化等计算结果。 |
| `[constexpr noexcept] bool operator!=(QVector3D v1, QVector3D v2)` | 精确判断两个向量不相等。 | 对浮点计算结果要谨慎。 |
| `[constexpr noexcept] QVector3D operator*(QVector3D v1, QVector3D v2)` | 返回逐分量乘法结果。 | 不是点乘；不是叉乘。 |
| `[constexpr noexcept] QVector3D operator*(QVector3D vector, float factor)` | 返回标量缩放后的副本。 | 不修改原对象。 |
| `[constexpr noexcept] QVector3D operator*(float factor, QVector3D vector)` | 返回标量缩放后的副本。 | 与 `vector * factor` 语义相同。 |
| `[constexpr noexcept] QVector3D operator+(QVector3D v1, QVector3D v2)` | 返回逐分量相加结果。 | 不修改参数。 |
| `[constexpr noexcept] QVector3D operator-(QVector3D v1, QVector3D v2)` | 返回逐分量相减结果。 | 常用于求位移方向。 |
| `[constexpr noexcept] QVector3D operator-(QVector3D vector)` | 返回所有分量取反的新向量。 | 表示反方向。 |
| `[constexpr] QVector3D operator/(QVector3D vector, QVector3D divisor)` | 返回逐分量除法结果。 | `divisor` 每个分量都不能为 `0` 或 NaN。 |
| `[constexpr] QVector3D operator/(QVector3D vector, float divisor)` | 返回除以标量后的副本。 | `divisor` 不能为 `0` 或 NaN。 |
| `QDataStream &operator<<(QDataStream &stream, QVector3D vector)` | 把向量写入数据流。 | 读写双方使用兼容的流版本。 |
| `[constexpr noexcept] bool operator==(QVector3D v1, QVector3D v2)` | 精确判断两个向量相等。 | 直接比较浮点分量；计算结果建议模糊比较。 |
| `QDataStream &operator>>(QDataStream &stream, QVector3D &vector)` | 从数据流读入向量。 | 读取后检查 `QDataStream` 状态。 |

## 一句话总结

`QVector3D` 是 Qt 3D 几何辅助里的基础砖块：它轻量、直接，但法线、投影和浮点比较必须带着数学前提使用。
