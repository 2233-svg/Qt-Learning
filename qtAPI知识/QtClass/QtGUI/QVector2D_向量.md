# QVector2D 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QVector2D>`
> 所属模块：`Qt6::Gui`
> 继承：无

## 它解决什么问题

`QVector2D` 是 Qt GUI 模块里的二维浮点向量值类型，用来表达 2D 空间中的方向、位移、点或顶点。它把 `x`、`y` 两个 `float` 分量和常见向量运算放在一起，适合在绘制、几何计算、触控/鼠标坐标处理、OpenGL/Quick 辅助计算中传递轻量数据。

它不是容器类，虽然名字里有 `Vector`；也不是 `QPointF` 的完全替代品。`QPointF` 偏向几何点和矩形 API，`QVector2D` 偏向向量数学：长度、归一化、点乘、按分量加减乘除以及维度转换。

## 实际使用场景

- 计算两个屏幕坐标之间的距离、方向或单位方向。
- 把 `QPointF` 事件位置转成可参与向量运算的对象。
- 在自定义绘制、图形视图或 Qt Quick 辅助逻辑中保存顶点位置。
- 将 2D 坐标扩展为 `QVector3D` 或 `QVector4D`，交给矩阵、着色器、3D 辅助代码继续处理。

## 使用模型

`QVector2D` 是小型值类型，默认构造得到 `(0, 0)`。拷贝、传值和作为返回值使用都很自然；它没有 QObject 生命周期、父子关系、事件循环或线程亲和性问题。

Qt 文档要求显式坐标、缩放因子等输入为有限浮点数。实际代码里不要把 NaN 或无穷大塞进向量运算，否则比较、归一化、序列化和后续几何计算都会变得不可预期。

下标访问使用 `0` 表示 `x`，`1` 表示 `y`。`operator[]` 不做面向业务的越界恢复，索引必须满足 `0 <= i < 2`。

## 关键 API 语义与边界

`length()` 会开方，适合需要真实距离时使用；如果只是比较长短或判断阈值，`lengthSquared()` 通常更便宜，也能避免不必要的浮点误差。

`normalize()` 原地修改对象，`normalized()` 返回新对象。零向量归一化后仍是零向量；长度已经非常接近 `1` 时，Qt 会直接保留原值，避免无意义扰动。

`dotProduct()` 返回点乘标量，用于夹角、投影、方向相似度等判断。`operator*(QVector2D, QVector2D)` 不是点乘，而是按分量相乘，结果仍然是 `QVector2D`。

`operator==` 和 `operator!=` 使用精确浮点比较。计算结果来自三角函数、矩阵或连续缩放时，优先使用 `qFuzzyCompare()` 或业务容差比较。

`toPoint()` 会把 `x`、`y` 四舍五入为整数；`toPointF()` 保留浮点；`toVector3D()` 和 `toVector4D()` 会把新增分量填为 `0`。

## 常见误区

- 把 `QVector2D` 当成 `QVector<T>` 容器使用。它只是二维数学值类型。
- 误以为 `v1 * v2` 是点乘。Qt 这里返回的是按分量乘出的向量。
- 用 `operator==` 比较复杂计算后的浮点结果，导致“看起来一样”的向量比较失败。
- 对除法传入 `0` 或含 NaN 的分量；相关 API 明确要求除数有效。
- 把 `toPoint()` 当成无损转换；它会舍入成整数。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `[constexpr noexcept] QVector2D()` | 构造零向量 `(0, 0)`。 | 适合默认初始化；不是未初始化内存。 |
| `[explicit constexpr noexcept] QVector2D(QPoint point)` | 从整数点提取 `x`、`y` 构造向量。 | 整数坐标转为 `float`。 |
| `[explicit constexpr noexcept] QVector2D(QPointF point)` | 从浮点点提取 `x`、`y` 构造向量。 | 语义从“点”转为“可参与向量运算的坐标”。 |
| `[explicit constexpr noexcept] QVector2D(QVector3D vector)` | 从 3D 向量构造 2D 向量。 | 丢弃 `z` 分量。 |
| `[explicit constexpr noexcept] QVector2D(QVector4D vector)` | 从 4D 向量构造 2D 向量。 | 丢弃 `z` 与 `w` 分量。 |
| `[constexpr noexcept] QVector2D(float xpos, float ypos)` | 用两个浮点分量构造向量。 | 两个坐标都应为有限值。 |
| `[noexcept] float distanceToLine(QVector2D point, QVector2D direction) const` | 计算当前顶点到由 `point` 和单位方向 `direction` 定义的直线的距离。 | `direction` 应是单位向量；若是零向量，则退化为到 `point` 的距离。 |
| `[noexcept] float distanceToPoint(QVector2D point) const` | 计算当前顶点到另一个点的欧氏距离。 | 需要真实距离；大量比较时可考虑平方距离思路自行优化。 |
| `[static constexpr noexcept] float dotProduct(QVector2D v1, QVector2D v2)` | 返回两个向量的点乘标量。 | 用于夹角、投影和方向相似度；区别于按分量乘法。 |
| `[constexpr noexcept] bool isNull() const` | 判断 `x`、`y` 是否为零。 | 不等同于“足够接近零”的容差判断。 |
| `[noexcept] float length() const` | 返回从原点到该向量的长度。 | 会开方；性能敏感比较可用 `lengthSquared()`。 |
| `[constexpr noexcept] float lengthSquared() const` | 返回长度平方。 | 等价于向量与自身点乘，适合比较阈值。 |
| `[noexcept] void normalize()` | 把当前对象原地归一化为单位向量。 | 零向量不变；长度接近 `1` 时不扰动。 |
| `[noexcept] QVector2D normalized() const` | 返回归一化后的新向量。 | 当前对象不变；零向量返回零向量。 |
| `[constexpr noexcept] void setX(float x)` | 修改 `x` 分量。 | 参数应为有限值。 |
| `[constexpr noexcept] void setY(float y)` | 修改 `y` 分量。 | 参数应为有限值。 |
| `[constexpr noexcept] QPoint toPoint() const` | 转为 `QPoint`。 | `x`、`y` 会四舍五入到整数。 |
| `[constexpr noexcept] QPointF toPointF() const` | 转为 `QPointF`。 | 保留浮点坐标。 |
| `[constexpr noexcept] QVector3D toVector3D() const` | 扩展为 3D 向量。 | `z` 填 `0`。 |
| `[constexpr noexcept] QVector4D toVector4D() const` | 扩展为 4D 向量。 | `z`、`w` 都填 `0`。 |
| `[constexpr noexcept] float x() const` | 返回 `x` 分量。 | 只读访问。 |
| `[constexpr noexcept] float y() const` | 返回 `y` 分量。 | 只读访问。 |
| `operator QVariant() const` | 把向量包装成 `QVariant`。 | 方便属性系统、模型数据和动态 API 传递。 |
| `[constexpr noexcept] QVector2D &operator*=(QVector2D vector)` | 当前向量逐分量乘以另一个向量。 | 不是点乘；返回引用便于链式调用。 |
| `[constexpr noexcept] QVector2D &operator*=(float factor)` | 当前向量按标量缩放。 | `factor` 应为有限值。 |
| `[constexpr noexcept] QVector2D &operator+=(QVector2D vector)` | 当前向量逐分量加上另一个向量。 | 修改自身。 |
| `[constexpr noexcept] QVector2D &operator-=(QVector2D vector)` | 当前向量逐分量减去另一个向量。 | 修改自身。 |
| `[constexpr] QVector2D &operator/=(QVector2D vector)` | 当前向量逐分量除以另一个向量。 | 除数向量的每个分量都不能为 `0` 或 NaN。 |
| `[constexpr] QVector2D &operator/=(float divisor)` | 当前向量除以标量。 | `divisor` 不能为 `0` 或 NaN。 |
| `[constexpr] float &operator[](int i)` | 按索引返回可修改分量引用。 | `0` 是 `x`，`1` 是 `y`；索引必须在范围内。 |
| `[constexpr] float operator[](int i) const` | 按索引返回分量值。 | `0 <= i < 2`。 |
| `[noexcept] bool qFuzzyCompare(QVector2D v1, QVector2D v2)` | 以 Qt 的浮点模糊比较规则比较两个向量。 | 适合计算结果比较；不是自定义业务容差。 |
| `[constexpr noexcept] bool operator!=(QVector2D v1, QVector2D v2)` | 精确判断两个向量不相等。 | 对浮点计算结果要谨慎。 |
| `[constexpr noexcept] QVector2D operator*(QVector2D v1, QVector2D v2)` | 返回逐分量乘法结果。 | 不是点乘；点乘用 `dotProduct()`。 |
| `[constexpr noexcept] QVector2D operator*(QVector2D vector, float factor)` | 返回标量缩放后的副本。 | 不修改原对象。 |
| `[constexpr noexcept] QVector2D operator*(float factor, QVector2D vector)` | 返回标量缩放后的副本。 | 与 `vector * factor` 语义相同。 |
| `[constexpr noexcept] QVector2D operator+(QVector2D v1, QVector2D v2)` | 返回逐分量相加结果。 | 不修改参数。 |
| `[constexpr noexcept] QVector2D operator-(QVector2D v1, QVector2D v2)` | 返回逐分量相减结果。 | 表示位移差时很常用。 |
| `[constexpr noexcept] QVector2D operator-(QVector2D vector)` | 返回所有分量取反的新向量。 | 等价于从零向量减去它。 |
| `[constexpr] QVector2D operator/(QVector2D vector, QVector2D divisor)` | 返回逐分量除法结果。 | `divisor` 每个分量都不能为 `0` 或 NaN。 |
| `[constexpr] QVector2D operator/(QVector2D vector, float divisor)` | 返回除以标量后的副本。 | `divisor` 不能为 `0` 或 NaN。 |
| `QDataStream &operator<<(QDataStream &stream, QVector2D vector)` | 把向量写入数据流。 | 读写双方应使用兼容的 `QDataStream` 版本。 |
| `[constexpr noexcept] bool operator==(QVector2D v1, QVector2D v2)` | 精确判断两个向量相等。 | 直接比较浮点分量；计算结果更适合模糊比较。 |
| `QDataStream &operator>>(QDataStream &stream, QVector2D &vector)` | 从数据流读入向量。 | 失败状态由 `QDataStream` 承载，读取后应检查流状态。 |

## 一句话总结

`QVector2D` 是二维坐标进入向量数学世界的轻量值类型：好用，但浮点比较、除法和维度转换都要按数学语义来读。
