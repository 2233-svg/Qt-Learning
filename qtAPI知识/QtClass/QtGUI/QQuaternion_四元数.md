# QQuaternion：表示和组合三维旋转

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QQuaternion>`  
> 所属模块：`Qt6::Gui`  
> 类型性质：四个 `float` 分量的值类型

`QQuaternion` 用四个浮点数表示三维旋转，内部由一个三维向量分量 `(x, y, z)` 和一个标量分量 `scalar` 组成。它适合表示姿态、相机方向、物体旋转和动画插值，尤其适合避免欧拉角的万向节锁。

一个用于旋转的四元数通常应是单位四元数：

```text
scalar^2 + x^2 + y^2 + z^2 = 1
```

`QQuaternion` 本身不会强制对象始终是单位四元数。普通构造、分量运算和缩放运算都可能生成非单位值；在用于旋转向量、矩阵或插值前，要根据数据来源决定是否调用 `normalized()` 或 `normalize()`。

## 它解决的问题

### 表示姿态

```cpp
QQuaternion rotation =
    QQuaternion::fromAxisAndAngle(QVector3D(0, 1, 0), 45.0f);
```

这个对象表达绕 Y 轴旋转 45 度。相比保存三个欧拉角，四元数更适合连续更新和组合。

### 组合旋转

```cpp
QQuaternion local = QQuaternion::fromAxisAndAngle(
    QVector3D(0, 0, 1), 30.0f);
QQuaternion parent = QQuaternion::fromAxisAndAngle(
    QVector3D(0, 1, 0), 45.0f);

QQuaternion world = parent * local;
```

四元数乘法不是普通的逐分量乘法，而且不满足交换律。`q1 * q2` 的组合语义要结合 Qt 的坐标约定和你的父子变换约定验证，不能把两个操作数任意交换。

### 旋转向量和插值

```cpp
QVector3D rotated = rotation.rotatedVector(QVector3D(1, 0, 0));

QQuaternion current = QQuaternion::slerp(start, target, progress);
```

`rotatedVector()` 适合直接旋转一个三维向量；`slerp()` 和 `nlerp()` 适合动画、相机和姿态平滑过渡。

## 内部表示和构造

默认构造得到单位四元数 `(scalar=1, x=0, y=0, z=0)`，也就是恒等旋转。不要把默认构造误认为“零旋转数据未初始化”。

```cpp
QQuaternion identity;
Q_ASSERT(identity.isIdentity());
```

`QQuaternion(Qt::Uninitialized)` 是显式的未初始化构造，调用后四个分量都不应读取，直到调用方完整写入它们。它只适用于确定会立即覆盖所有分量的低层或性能敏感路径：

```cpp
QQuaternion q(Qt::Uninitialized);
q.setScalar(1.0f);
q.setVector(0.0f, 0.0f, 0.0f);
```

通常应优先使用普通默认构造或完整分量构造，避免未初始化数据流入计算。

## 单位、逆和共轭

共轭是：

```text
conjugated(s, x, y, z) = (s, -x, -y, -z)
```

对于单位四元数，共轭就是逆；对于一般四元数，真正的逆还要除以长度平方。`inverted()` 会执行一般逆运算；如果对象是 null quaternion，则返回 null quaternion。

```cpp
QQuaternion inverse = rotation.inverted();
QQuaternion conjugate = rotation.conjugated();
```

用于旋转时，优先保证 `rotation` 是单位四元数。`isNull()` 判断的是四个分量全为 0，而不是“不是有效旋转”；null quaternion 和 identity quaternion 是两个完全不同的状态。

## 矩阵、轴角和欧拉角

### 轴角

`fromAxisAndAngle()` 的角度单位是度，返回归一化四元数。`getAxisAndAngle()` 反向提取轴和角度时，所有输出指针都必须非 null 且有效。

### 欧拉角

Qt 使用 `pitch` 绕 X、`yaw` 绕 Y、`roll` 绕 Z，单位为度。`fromEulerAngles()` 定义的组合顺序是 roll(Z)、pitch(X)、yaw(Y)。欧拉角表示不唯一，四元数反解出来的值不一定逐项等于原始输入。

### 旋转矩阵

`toRotationMatrix()` 和 `fromRotationMatrix()` 之间应使用真正的旋转矩阵。若四元数或输入矩阵没有归一化，缩放信息可能被带进结果：

```cpp
QQuaternion rotation = source.normalized();
QMatrix3x3 matrix = rotation.toRotationMatrix();
QQuaternion restored = QQuaternion::fromRotationMatrix(matrix);
```

## 归一化和数值边界

### `normalized()` 与 `normalize()`

- `normalized()` 返回新对象，不改变原对象。
- `normalize()` 原地修改对象。
- null quaternion 调用 `normalized()` 会得到 null quaternion。
- 如果长度已经非常接近 1，Qt 可能直接返回原值或不做额外修改。

每次逐帧修改分量后都归一化可能有成本；更好的做法是让旋转路径保持单位性质，或在累积一段误差后再归一化。

### `lengthSquared()` 的溢出风险

`lengthSquared()` 便宜，但直接累加平方可能更容易溢出或下溢；`length()` 在一些极端值下更稳健。只需比较大小时可使用平方长度，但要注意输入范围。

## `slerp` 和 `nlerp`

两个函数的 `t` 都建议位于 `[0, 1]`：

- `t <= 0` 返回 `q1`。
- `t >= 1` 返回 `q2`。
- `slerp()` 沿最短球面路径插值，角速度性质更好，但通常更慢。
- `nlerp()` 沿最短线性路径并归一化，通常更快，是球面插值的近似。

用于旋转插值时，输入应是代表旋转的归一化四元数。若两个输入未归一化或包含缩放信息，结果不应被当作可靠姿态。

## 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

```cpp
#include <QQuaternion>
#include <QVector3D>
#include <QVector4D>
#include <QMatrix4x4>
```

## API 逐项说明

### 构造和状态

#### `constexpr noexcept QQuaternion::QQuaternion()`

构造单位四元数 `(1, 0, 0, 0)`，代表恒等旋转。

#### `explicit QQuaternion::QQuaternion(Qt::Initialization)`

使用 `Qt::Uninitialized` 标签构造不初始化的四元数。四个分量在写入前不可读取；它不是 null quaternion，也不是 identity quaternion。

#### `constexpr noexcept QQuaternion::QQuaternion(float scalar, float x, float y, float z)`

用标量和向量三个分量构造四元数。参数不会自动归一化，调用方需要确保该值适合作为旋转。

#### `constexpr noexcept QQuaternion::QQuaternion(float scalar, const QVector3D &vector)`

用标量和 `QVector3D` 的向量分量构造四元数。不会自动归一化。

#### `explicit constexpr noexcept QQuaternion::QQuaternion(const QVector4D &vector)`

从四维向量构造四元数。按 Qt 的实现，向量的 `x/y/z` 成为四元数向量分量，`w` 成为 scalar 分量。

#### `QQuaternion` 的拷贝、移动和赋值

这是轻量值类型，编译器生成的拷贝、移动构造和赋值即可按值使用。复制不会产生 QObject 所有权或外部资源问题。

#### `bool QQuaternion::isNull() const noexcept`

当 scalar、x、y、z 四个分量都为 `0.0f` 时返回 `true`。这是代数上的零四元数，不代表恒等旋转。

#### `bool QQuaternion::isIdentity() const noexcept`

当 scalar 为 `1.0f` 且 x、y、z 都为 `0.0f` 时返回 `true`。它使用精确分量判断，不是带容差的姿态判断。

### 分量读取和修改

#### `float QQuaternion::scalar() const noexcept`

返回标量分量。旋转轴角表示中它通常与半角余弦相关，但不要在未归一化数据上直接套用单位四元数公式。

#### `QVector3D QQuaternion::vector() const noexcept`

返回 `(x, y, z)` 向量分量的值副本。

#### `float QQuaternion::x() const noexcept`

返回向量分量的 X 值。

#### `float QQuaternion::y() const noexcept`

返回向量分量的 Y 值。

#### `float QQuaternion::z() const noexcept`

返回向量分量的 Z 值。

#### `void QQuaternion::setScalar(float scalar) noexcept`

设置标量分量。修改后不会自动归一化。

#### `void QQuaternion::setVector(const QVector3D &vector) noexcept`

一次设置 x、y、z 三个向量分量。不会修改 scalar，也不会自动归一化。

#### `void QQuaternion::setVector(float x, float y, float z) noexcept`

按三个浮点值设置向量分量。不会修改 scalar。

#### `void QQuaternion::setX(float x) noexcept`

设置向量的 X 分量。不会自动维护单位长度。

#### `void QQuaternion::setY(float y) noexcept`

设置向量的 Y 分量。不会自动维护单位长度。

#### `void QQuaternion::setZ(float z) noexcept`

设置向量的 Z 分量。不会自动维护单位长度。

#### `QVector4D QQuaternion::toVector4D() const noexcept`

返回四维向量形式。Qt 的构造和转换约定是 `QQuaternion(QVector4D(x, y, z, scalar))`，所以读取时注意 `QVector4D::w()` 对应 scalar。

#### `operator QVariant() const`

把四元数包装为 `QVariant`，用于属性系统或通用 Qt 数据容器。该接口受 Qt 构建配置和版本宏影响，业务代码应确认目标 Qt 版本。

### 长度和代数运算

#### `float QQuaternion::length() const`

返回四元数范数。它是四个分量平方和的平方根。

#### `float QQuaternion::lengthSquared() const`

返回范数平方。计算便宜，但在极端浮点值下比 `length()` 更容易溢出或下溢。

#### `static constexpr float QQuaternion::dotProduct(const QQuaternion &q1, const QQuaternion &q2) noexcept`

返回四个分量的点积。可用于判断角度关系、插值路径和长度关系，但不自动归一化输入。

#### `QQuaternion QQuaternion::normalized() const`

返回单位长度副本。null quaternion 返回 null quaternion；长度已接近 1 时可能原样返回。

#### `void QQuaternion::normalize()`

原地归一化。null quaternion 不会变成有效旋转；长度接近 1 时通常无需修改。

#### `QQuaternion QQuaternion::inverted() const noexcept`

返回一般四元数的逆。null quaternion 返回 null quaternion。对于单位旋转四元数，结果等于 `conjugated()`。

#### `QQuaternion QQuaternion::conjugated() const noexcept`

返回 `(scalar, -x, -y, -z)`。它不除以长度平方，因此非单位四元数上它不是一般逆。

#### `QQuaternion &QQuaternion::operator+=(const QQuaternion &quaternion)`

逐分量相加。它是代数向量运算，不是旋转组合；相加后通常不是单位四元数。

#### `QQuaternion &QQuaternion::operator-=(const QQuaternion &quaternion)`

逐分量相减。它是代数向量运算，不是旋转组合。

#### `QQuaternion &QQuaternion::operator*=(float factor)`

把四个分量都乘以 `factor`。它改变长度，通常会破坏单位旋转性质。

#### `QQuaternion &QQuaternion::operator*=(const QQuaternion &quaternion)`

执行四元数乘法并把结果写回当前对象。乘法表示旋转组合，且不满足交换律。

#### `QQuaternion &QQuaternion::operator/=(float divisor)`

把四个分量都除以 `divisor`。调用方必须避免除以零或极小值；该操作不会自动归一化。

### 由轴角、方向和矩阵创建

#### `static QQuaternion QQuaternion::fromAxisAndAngle(const QVector3D &axis, float angle)`

创建绕三维 `axis` 旋转 `angle` 度的归一化四元数。角度单位是度；轴应表达有效方向，零轴属于退化输入，应由调用方避免。

#### `static QQuaternion QQuaternion::fromAxisAndAngle(float x, float y, float z, float angle)`

`QVector3D` 轴版本的分量便捷形式。角度单位是度，结果是归一化四元数。

#### `void QQuaternion::getAxisAndAngle(QVector3D *axis, float *angle) const`

把当前四元数分解成三维轴和角度，角度单位为度。`axis` 和 `angle` 都必须是有效的非 null 指针，否则行为未定义。

#### `void QQuaternion::getAxisAndAngle(float *x, float *y, float *z, float *angle) const`

轴角分解的四个输出指针版本。四个指针都必须非 null 且可写，否则行为未定义。

#### `static QQuaternion QQuaternion::fromDirection(const QVector3D &direction, const QVector3D &up)`

根据 forward `direction` 和 upward `up` 构造方向四元数。如果 upward 未提供或与 forward 共线，Qt 会生成新的正交 upward 方向。方向和 up 的坐标系约定必须与渲染场景一致。

#### `static QQuaternion QQuaternion::rotationTo(const QVector3D &from, const QVector3D &to)`

返回把 `from` 方向旋转到 `to` 方向的最短弧四元数。零向量、近零向量和相反方向等退化输入应由调用方预先处理或测试。

#### `static QQuaternion QQuaternion::fromRotationMatrix(const QMatrix3x3 &rot3x3)`

从 3x3 旋转矩阵创建四元数。矩阵应是归一化的纯旋转矩阵；如果含有缩放，生成的四元数会包含缩放信息。

#### `QMatrix3x3 QQuaternion::toRotationMatrix() const`

把四元数转成 3x3 旋转矩阵。四元数不归一化时，结果矩阵可能含有缩放信息；需要纯旋转时先 `normalized()`。

### 欧拉角

#### `static QQuaternion QQuaternion::fromEulerAngles(float pitch, float yaw, float roll)`

从三个角度创建四元数，单位是度。Qt 定义的组合顺序为 roll 绕 Z、pitch 绕 X、yaw 绕 Y。

#### `static QQuaternion QQuaternion::fromEulerAngles(const QVector3D &angles)`

从向量创建四元数，`angles.x()` 是 pitch，`angles.y()` 是 yaw，`angles.z()` 是 roll；单位为度，组合顺序仍是 Z/roll、X/pitch、Y/yaw。

#### `static QQuaternion QQuaternion::fromEulerAngles(EulerAngles<float> angles)`

从 Qt 6.11 的欧拉角结构创建四元数，等价于 `fromEulerAngles(angles.pitch, angles.yaw, angles.roll)`。

#### `QVector3D QQuaternion::toEulerAngles() const`

返回 `(pitch, yaw, roll)` 排列的三维向量，单位是度。欧拉角分解不唯一，返回值不保证逐项恢复输入。

#### `QQuaternion::EulerAngles<float> QQuaternion::eulerAngles() const`

从 Qt 6.11 起返回带字段名称的欧拉角结构，单位是度。它和 `toEulerAngles()` 的轴映射相同，但表达更清晰。

#### `void QQuaternion::getEulerAngles(float *pitch, float *yaw, float *roll) const`

把欧拉角写入三个输出指针，单位是度。三个指针都必须有效且非 null；该接口适合与旧式 C 风格输出 API 对接。

### 坐标轴

#### `static QQuaternion QQuaternion::fromAxes(QQuaternion::Axes axes)`

从三根 `Axis` 构造四元数。Qt 假设这些轴是正交归一的；`Axes` 本身不负责检查。该 API 从 Qt 6.11 起提供。

#### `static QQuaternion QQuaternion::fromAxes(const QVector3D &xAxis, const QVector3D &yAxis, const QVector3D &zAxis)`

从三个 `QVector3D` 轴构造四元数，语义等价于转换成 `Axes` 后调用结构体重载。调用方应提供正交归一轴。

#### `QQuaternion::Axes QQuaternion::toAxes() const`

返回定义当前四元数的三根正交轴。该 API 从 Qt 6.11 起提供，适合与新式 `Axis`/`Axes` 接口协作。

#### `void QQuaternion::getAxes(QVector3D *xAxis, QVector3D *yAxis, QVector3D *zAxis) const`

把三根轴写入输出指针。三个指针都必须有效且非 null；返回的轴可用于坐标系或调试，但不要把输出指针当作内部存储引用。

### 向量旋转

#### `QVector3D QQuaternion::rotatedVector(const QVector3D &vector) const`

用当前四元数旋转三维向量并返回新向量。用于纯旋转时应使用归一化四元数；非单位四元数可能产生缩放或非预期结果。

#### `QVector3D operator*(const QQuaternion &quaternion, const QVector3D &vec)`

是 `rotatedVector()` 的运算符形式：`quaternion * vec` 返回旋转后的向量。它不是把四元数和向量做普通标量乘法。

### 插值

#### `static QQuaternion QQuaternion::slerp(const QQuaternion &q1, const QQuaternion &q2, float t)`

沿两个旋转姿态之间的最短球面路径插值。`t <= 0` 返回 `q1`，`t >= 1` 返回 `q2`；中间值通常取 `[0, 1]`。输入应是单位旋转四元数。

#### `static QQuaternion QQuaternion::nlerp(const QQuaternion &q1, const QQuaternion &q2, float t)`

沿最短线性路径近似插值并归一化结果。通常比 `slerp()` 快，适合对球面精度要求较低的动画。边界 `t <= 0` 和 `t >= 1` 同样直接返回端点。

### 比较、算术和序列化非成员

#### `bool operator==(const QQuaternion &q1, const QQuaternion &q2)`

逐分量精确比较。浮点计算产生的等价姿态不一定逐分量完全相等；近似比较使用 `qFuzzyCompare()`。

#### `bool operator!=(const QQuaternion &q1, const QQuaternion &q2)`

逐分量精确不等比较。它不是带容差的几何姿态比较。

#### `bool qFuzzyCompare(const QQuaternion &q1, const QQuaternion &q2)`

按浮点容差比较四个分量。它比较的是分量近似，而不是自动识别所有等价旋转表示；四元数 `q` 与 `-q` 表示同一旋转，但不应假设该函数会把它们当作相等。

#### `QQuaternion operator*(const QQuaternion &q1, const QQuaternion &q2)`

执行四元数乘法，用于组合旋转。乘法不满足交换律，顺序必须与场景的局部/世界坐标约定一致。

#### `QQuaternion operator*(const QQuaternion &quaternion, float factor)`

返回四个分量乘以 `factor` 的副本。它是代数缩放，不是旋转大小调整。

#### `QQuaternion operator*(float factor, const QQuaternion &quaternion)`

上一个标量乘法的交换写法，结果同样是逐分量缩放。

#### `QQuaternion operator+(const QQuaternion &q1, const QQuaternion &q2)`

逐分量相加并返回新对象。不是旋转组合，结果通常需要重新归一化后才可作为旋转使用。

#### `QQuaternion operator-(const QQuaternion &q1, const QQuaternion &q2)`

逐分量相减并返回新对象。不是旋转组合。

#### `QQuaternion operator-(const QQuaternion &quaternion)`

返回四个分量取负的副本。对于旋转表示，`q` 与 `-q` 可代表相同姿态，但该运算本身仍是分量取负。

#### `QQuaternion operator/(const QQuaternion &quaternion, float divisor)`

把四个分量都除以 `divisor`。调用方应避免除零和极小除数；不会自动归一化。

#### `QDataStream &operator<<(QDataStream &, const QQuaternion &)`

把四元数写入数据流，用于 Qt 类型序列化。流版本应由应用统一管理。

#### `QDataStream &operator>>(QDataStream &, QQuaternion &)`

从数据流读入四元数。读取后如要用于旋转，应根据数据来源检查或归一化。

#### `QDebug operator<<(QDebug, const QQuaternion &)`

输出四元数的调试表示，适合日志和诊断，不是稳定的序列化格式。

## 常见错误排查

1. **把默认构造当成未初始化**：默认构造是 identity `(1,0,0,0)`；只有 `Qt::Uninitialized` 才是不初始化。
2. **把 null quaternion 当成零旋转**：零旋转是 identity，不是四个分量全零的 null quaternion。
3. **用非单位四元数转矩阵或旋转向量**：可能把缩放带入结果，先调用 `normalized()`。
4. **把 `conjugated()` 当成所有情况下的逆**：只有单位四元数的共轭才等于逆；一般值使用 `inverted()`。
5. **交换乘法操作数**：四元数乘法不满足交换律，组合父子旋转前先明确坐标约定。
6. **把 `operator+` 当作旋转叠加**：逐分量加法不是姿态组合，姿态组合使用四元数乘法。
7. **角度传弧度**：轴角和欧拉角接口都使用度。
8. **误读欧拉角顺序**：Qt 字段是 pitch(X)、yaw(Y)、roll(Z)，组合顺序是 roll、pitch、yaw。
9. **忽略矩阵缩放信息**：非归一化矩阵或四元数会使转换结果包含缩放。
10. **输出指针传 null**：`getAxisAndAngle()`、`getEulerAngles()` 和 `getAxes()` 的输出指针必须有效。
11. **把 `operator==` 当作姿态近似比较**：它是精确浮点比较；需要容差时使用 `qFuzzyCompare()`，还要考虑 `q`/`-q` 等价。
12. **插值输入不是单位四元数**：`slerp()`/`nlerp()` 应接收代表旋转的归一化值。
13. **旋转到零方向**：`rotationTo()` 对零向量等退化输入没有可用的方向语义，调用前先验证输入。

## API 速查表

| 类别 | API | 作用 | 关键边界与注意事项 |
| --- | --- | --- | --- |
| 构造 | `QQuaternion()` | 创建恒等旋转 | `(scalar=1, vector=0)` |
| 构造 | `QQuaternion(Qt::Uninitialized)` | 不初始化四个分量 | 写入全部分量前不可读取 |
| 构造 | `QQuaternion(scalar, x, y, z)` | 按四个分量构造 | 不自动归一化 |
| 构造 | `QQuaternion(scalar, QVector3D)` | 按 scalar 和向量构造 | 不自动归一化 |
| 构造 | `QQuaternion(QVector4D)` | 从四维向量构造 | `w` 对应 scalar |
| 状态 | `isNull()` | 判断四个分量是否全为零 | 不代表恒等旋转 |
| 状态 | `isIdentity()` | 判断是否为 `(1,0,0,0)` | 精确比较，不带容差 |
| 读取 | `scalar()` / `vector()` | 获取标量或向量分量 | 返回值不改变对象 |
| 读取 | `x()` / `y()` / `z()` | 获取向量分量 | 单独读取分量 |
| 写入 | `setScalar()` | 修改标量分量 | 不自动归一化 |
| 写入 | `setVector(QVector3D)` | 修改三个向量分量 | 不修改 scalar |
| 写入 | `setVector(x, y, z)` | 修改三个向量分量 | 不修改 scalar |
| 写入 | `setX()` / `setY()` / `setZ()` | 修改单个向量分量 | 可能破坏单位长度 |
| 转换 | `toVector4D()` | 转为四维向量 | `x/y/z` 是向量，`w` 是 scalar |
| 转换 | `operator QVariant()` | 放入 `QVariant` | 受 Qt 构建配置影响 |
| 长度 | `length()` | 获取范数 | 极端值下比平方长度更稳健 |
| 长度 | `lengthSquared()` | 获取范数平方 | 便宜但更易溢出/下溢 |
| 代数 | `dotProduct(q1, q2)` | 计算四元数点积 | 不自动归一化 |
| 归一化 | `normalized()` | 返回单位四元数副本 | null 输入返回 null |
| 归一化 | `normalize()` | 原地归一化 | null 不会变成有效旋转 |
| 逆 | `inverted()` | 求一般四元数逆 | null 输入返回 null |
| 逆 | `conjugated()` | 取共轭 | 非单位值上不等于一般逆 |
| 组合 | `operator*(QQuaternion, QQuaternion)` | 组合旋转 | 不满足交换律 |
| 旋转 | `rotatedVector()` / `operator*(QQuaternion, QVector3D)` | 旋转向量 | 先保证四元数适合纯旋转 |
| 轴角 | `fromAxisAndAngle(axis, angle)` | 创建轴角旋转 | 角度为度；结果归一化 |
| 轴角 | `getAxisAndAngle()` | 提取轴和角度 | 输出指针不得为 null |
| 方向 | `fromDirection(direction, up)` | 从 forward/up 构造姿态 | 共线 up 会自动生成替代方向 |
| 最短弧 | `rotationTo(from, to)` | 求 from 到 to 的最短旋转 | 零方向等退化输入需预处理 |
| 欧拉角 | `fromEulerAngles(float, float, float)` | 从 pitch/yaw/roll 创建 | 度；组合顺序 Z、X、Y |
| 欧拉角 | `fromEulerAngles(QVector3D)` | 从 `(pitch,yaw,roll)` 向量创建 | x=pitch、y=yaw、z=roll |
| 欧拉角 | `fromEulerAngles(EulerAngles<float>)` | 从字段结构创建 | Qt 6.11 起 |
| 欧拉角 | `toEulerAngles()` | 返回 `(pitch,yaw,roll)` | 分解不唯一；单位为度 |
| 欧拉角 | `eulerAngles()` | 返回 `EulerAngles<float>` | Qt 6.11 起；单位为度 |
| 欧拉角 | `getEulerAngles()` | 写入三个角度指针 | 指针必须有效；单位为度 |
| 坐标轴 | `fromAxes(Axes)` | 从三根 `Axis` 创建旋转 | 假设轴正交归一；Qt 6.11 起 |
| 坐标轴 | `fromAxes(QVector3D, QVector3D, QVector3D)` | 从三个向量轴创建 | 调用方负责轴质量 |
| 坐标轴 | `toAxes()` | 返回三根正交轴 | Qt 6.11 起 |
| 坐标轴 | `getAxes()` | 输出三个向量轴 | 三个输出指针不得为 null |
| 矩阵 | `fromRotationMatrix(QMatrix3x3)` | 从矩阵创建四元数 | 非归一化矩阵会带入缩放 |
| 矩阵 | `toRotationMatrix()` | 转为 3x3 矩阵 | 非单位四元数可能产生缩放 |
| 插值 | `slerp(q1, q2, t)` | 最短球面路径插值 | `t<=0`/`t>=1` 返回端点 |
| 插值 | `nlerp(q1, q2, t)` | 快速线性近似插值 | 结果归一化；精度低于 slerp |
| 比较 | `operator==` / `operator!=` | 精确分量比较 | 不是容差比较，也不是姿态等价判断 |
| 比较 | `qFuzzyCompare()` | 浮点容差比较 | 仍要考虑 `q` 与 `-q` 的旋转等价 |
| 算术 | `operator+` / `operator-` | 逐分量加减 | 不是旋转组合 |
| 算术 | `operator*` / `operator/` 与标量 | 逐分量缩放 | 可能破坏单位长度 |
| 序列化 | `QDataStream` 插入/提取运算符 | 读写四元数 | 管理流版本，读取后按需归一化 |
| 调试 | `QDebug operator<<` | 输出调试信息 | 不是稳定序列化格式 |

### 一句话总结

`QQuaternion` 是三维旋转的稳定表示：用单位四元数做姿态和插值，用欧拉角服务于人机交互，用轴角/矩阵对接其他几何系统；始终区分 identity、null、共轭、逆和非单位值，旋转组合才不会悄悄带入错误的缩放或方向。
