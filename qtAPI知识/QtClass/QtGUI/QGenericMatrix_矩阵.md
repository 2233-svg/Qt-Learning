# QGenericMatrix

`QGenericMatrix<N, M, T>` 是固定尺寸的通用矩阵值类型：`N` 表示列数，`M` 表示行数，`T` 是元素类型。Qt 为常见的 `float` 尺寸提供了 `QMatrix2x2` 到 `QMatrix4x3` 等别名。

- 头文件：`#include <QGenericMatrix>`
- 模块：`Qt6::Gui`
- 类型特性：模板值类型，无动态分配、无 `QObject` 生命周期
- 适合：小型固定矩阵、着色器参数、图形算法和 Qt API 间的数据交换

## 它解决的问题

它在编译期固定矩阵维度，使不兼容的加法和乘法直接成为类型错误，并提供转置、逐元素加减、标量运算、矩阵乘法和 Qt 流支持。与 `QMatrix4x4` 相比，它没有专门的三维变换便利函数，适合表达任意小尺寸数值矩阵。

```cpp
QMatrix3x2 a; // 3 列、2 行，默认是矩形“单位矩阵”
a(0, 0) = 2.0f;
a(1, 2) = 5.0f;

const QMatrix2x3 t = a.transposed();
```

矩形矩阵也可构造“单位矩阵”：主对角线为 1，其余为 0，直到较短维度结束。

## 维度和乘法

模板参数顺序容易与数学教材的“行 × 列”写法相反：

```text
QGenericMatrix<列数 N, 行数 M, 元素类型 T>
```

矩阵乘法签名体现了维度约束：

```cpp
QGenericMatrix<NN, M2, T> left;   // M2 行，NN 列
QGenericMatrix<M1, NN, T> right;  // NN 行，M1 列
QGenericMatrix<M1, M2, T> result = left * right;
```

结果为 `M2` 行、`M1` 列。要让代码更易读，可优先使用 Qt 的尺寸别名，或在业务层创建语义化 `using`。

## 行主序输入与列主序内存

这是本类最重要的边界：

- `QGenericMatrix(const T *values)` 假定输入数组为**行主序**。
- `copyDataTo(T *values)` 同样按**行主序**输出。
- `data()` / `constData()` 暴露内部连续存储，内部为**列主序**，与 OpenGL 约定匹配。
- `operator()(row, column)` 始终按数学上的行、列访问，不受存储顺序影响。

```cpp
const float rows[] = {
    1, 2, 3,
    4, 5, 6
};
QMatrix3x2 matrix(rows); // 2 行、3 列

float exported[6];
matrix.copyDataTo(exported); // 仍为 1,2,3,4,5,6

const float *glData = matrix.constData(); // 内部列主序：1,4,2,5,3,6
```

给 OpenGL 上传时可以直接使用 `constData()`；给要求行主序的文件格式、数学库或日志时使用 `copyDataTo()`。不要把两者混用。

## 数值边界

默认构造会调用 `setToIdentity()`。`QGenericMatrix(Qt::Uninitialized)` 只用于需要立刻覆盖全部元素的高性能路径；读取任何未初始化元素都是未定义行为。

`isIdentity()` 和 `operator==` 使用元素的精确 `==` 比较。对浮点运算结果，舍入误差很容易让它们返回 `false`；需要数值近似判断时逐元素使用 `qFuzzyCompare()` 或业务容差。

`operator/=` 和除法运算符不检查除数是否为零；整数 `T` 还会执行整数除法。虽然模板允许不同数值类型，Qt 提供的别名都使用 `float`，也是图形场景的常用选择。

## API 速查表

### 构造、访问与状态

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `QGenericMatrix()` | 构造 `N` 列、`M` 行的单位矩阵。 | 矩形矩阵的主对角线为 1，其余为 0。 |
| `QGenericMatrix(Qt::Uninitialized)` | 跳过元素初始化。 | 必须在任何读取前覆盖全部 `N * M` 个元素。 |
| `QGenericMatrix(const T *values)` | 从 `N * M` 个元素构造矩阵。 | 输入必须非空且足够长，顺序是行主序。 |
| `operator()(row, column)` | 返回可修改的元素引用。 | 行范围 `[0, M)`，列范围 `[0, N)`；越界只由调试断言检查。 |
| `operator()(row, column) const` | 返回只读元素引用。 | 同样没有发布构建的边界保护。 |
| `fill(value)` | 将全部元素设为同一值。 | `fill(0)` 可创建零矩阵。 |
| `setToIdentity()` | 重置为单位矩阵。 | 适用于方阵和矩形矩阵。 |
| `isIdentity()` | 精确检查是否为单位矩阵。 | 浮点计算后不要将它当作容差比较。 |
| `transposed()` | 返回沿主对角线转置的矩阵。 | 返回类型为 `QGenericMatrix<M, N, T>`。 |

### 数据交换

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `data()` | 返回可修改的内部连续数据。 | 内部是列主序；指针只在矩阵对象存活期间有效。 |
| `data() const` / `constData()` | 返回只读内部数据。 | 列主序，适合 OpenGL 风格接口。 |
| `copyDataTo(T *values)` | 把矩阵复制到调用方数组。 | 输出为行主序；目标空间至少容纳 `N * M` 个元素。 |
| `QDataStream <<` / `>>` | 按行列顺序序列化矩阵。 | 元素先转为 `double` 写入、读出后转为 `T`；可能发生精度或范围转换。 |
| `QDebug <<` | 输出矩阵维度、元素类型和按行排列的值。 | 仅用于诊断，不是稳定持久化格式。 |

### 运算

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `operator+=` / `operator-=` | 对同尺寸矩阵逐元素加减。 | `N`、`M`、`T` 必须匹配。 |
| `operator*=(factor)` | 所有元素乘标量。 | 不表示矩阵乘法。 |
| `operator/=(divisor)` | 所有元素除以标量。 | 不检查零；整数类型会截断。 |
| `operator+` / 二元 `operator-` | 返回同尺寸矩阵的和或差。 | 逐元素计算。 |
| 一元 `operator-` | 返回所有元素取负后的矩阵。 | 无溢出检查。 |
| `matrix * factor` / `factor * matrix` | 返回标量乘法结果。 | 两种参数顺序等价。 |
| `matrix / divisor` | 返回标量除法结果。 | 除零和整数截断由 `T` 的 C++ 语义决定。 |
| `left * right` | 执行矩阵乘法。 | 左矩阵列数必须等于右矩阵行数，结果维度由模板推导。 |
| `operator==` / `!=` | 逐元素精确比较。 | 对浮点近似相等通常不合适。 |

### Qt 提供的别名

| 别名 | 实际类型 |
| --- | --- |
| `QMatrix2x2` | `QGenericMatrix<2, 2, float>` |
| `QMatrix2x3` | `QGenericMatrix<2, 3, float>` |
| `QMatrix2x4` | `QGenericMatrix<2, 4, float>` |
| `QMatrix3x2` | `QGenericMatrix<3, 2, float>` |
| `QMatrix3x3` | `QGenericMatrix<3, 3, float>` |
| `QMatrix3x4` | `QGenericMatrix<3, 4, float>` |
| `QMatrix4x2` | `QGenericMatrix<4, 2, float>` |
| `QMatrix4x3` | `QGenericMatrix<4, 3, float>` |

## 易错点

1. 把第一个模板参数当作行数，导致乘法维度和索引全部反转。
2. 把 `data()` 当作行主序数组传给外部库；需要行主序时用 `copyDataTo()`。
3. 用 `operator==` 验证经过浮点乘法的理论结果。
4. 使用 `Qt::Uninitialized` 后只填部分元素。
5. 除以零或在整数元素矩阵上期待浮点除法。
