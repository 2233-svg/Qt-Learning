# QGenericMatrix

> Qt 6.11.1 · Qt GUI · 来自 `QGenericMatrix<N, M, T>`

## 1. 先建立直觉

`QGenericMatrix` 是固定尺寸的通用矩阵值类型。它适合小型、维度在编译期已知的数学矩阵，例如颜色变换的 `3x3` 矩阵、图形管线中的 `3x4` 矩阵或自定义线性代数计算；它不是动态矩阵库，也不替代 `QMatrix4x4` 的图形变换接口。

模板参数的顺序非常重要：`QGenericMatrix<N, M, T>` 中 `N` 是**列数**，`M` 是**行数**，元素类型为 `T`。因此 `QGenericMatrix<3, 2, float>` 表示 2 行 3 列，而不是 3 行 2 列。

## 2. 类说明

- 头文件：`#include <QGenericMatrix>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 对象模型：轻量值类型；可按值复制、放在容器中或作为计算结果返回。
- 常用别名：`QMatrix2x2`、`QMatrix3x3`、`QMatrix4x3` 等均是以 `float` 为元素类型的预定义实例。

它的元素索引使用 `matrix(row, column)`，但内部原始存储采用**列主序**。这是本类最关键的约定：索引看起来像普通数学矩阵，`data()` 却适合直接交给使用列主序的图形 API。

## 3. API 速查

| API | 用途 |
|---|---|
| `QGenericMatrix()` | 构造零矩阵。 |
| `QGenericMatrix(values)` | 从**行主序**数组读取元素并构造矩阵。 |
| `operator()(row, column)` | 按数学行、列读取或修改单个元素。 |
| `data()` / `constData()` | 访问内部**列主序**连续内存。 |
| `copyDataTo(values)` | 将内容按**行主序**拷贝到外部数组。 |
| `fill(value)` | 以同一值填满所有元素。 |
| `setToIdentity()` / `isIdentity()` | 设置或检查单位矩阵。 |
| `transposed()` | 返回转置后的 `QGenericMatrix<M, N, T>`。 |
| `+=` / `-=` | 同尺寸矩阵逐元素加减。 |
| `*=` / `/=` | 所有元素乘除同一标量。 |
| `operator*(m1, m2)` | 按线性代数规则相乘；内维度必须匹配。 |
| `operator<<` / `operator>>` | 通过 `QDataStream` 序列化或反序列化。 |

## 4. 关键用法

### 用索引表达矩阵，而不是猜测内存下标

```cpp
#include <QGenericMatrix>

QGenericMatrix<3, 2, float> m; // 2 行、3 列
m.fill(0.0f);
m(0, 0) = 1.0f;
m(0, 1) = 2.0f;
m(1, 2) = 6.0f;
```

`operator()(row, column)` 是业务代码最清楚的访问方式。`row` 必须在 `[0, M)`，`column` 必须在 `[0, N)`；越界属于未定义行为，不能期待运行时检查。

### 行主序输入与列主序原始数据

```cpp
const float rowMajor[] = {
    1, 2, 3,
    4, 5, 6
};

QGenericMatrix<3, 2, float> m(rowMajor);
Q_ASSERT(m(1, 2) == 6.0f);

const float *columnMajor = m.constData();
// columnMajor 为：1, 4, 2, 5, 3, 6
```

构造函数的输入和 `copyDataTo()` 的输出都是行主序，便于与表格、CSV 或多数 CPU 侧算法对接；`data()` / `constData()` 则暴露列主序内存，适合 OpenGL 风格的数据接口。两者不能混用，否则矩阵会表现为转置或产生更隐蔽的错误。

### 单位矩阵、转置与乘法

```cpp
QMatrix3x3 identity;
identity.setToIdentity();

QMatrix3x3 transpose = identity.transposed();
Q_ASSERT(transpose.isIdentity());

QGenericMatrix<2, 3, float> a; // 3 行 2 列
QGenericMatrix<4, 2, float> b; // 2 行 4 列
const auto product = a * b;     // 3 行 4 列，即 QGenericMatrix<4, 3, float>
```

矩阵乘法不是逐元素相乘。`a * b` 只有在 `a` 的列数等于 `b` 的行数时才可编译，返回值的行数来自 `a`，列数来自 `b`。若只是逐元素缩放，使用标量乘法；若需要逐元素矩阵乘法，需要自行明确实现。

## 5. 使用场景

| 场景 | 建议 |
|---|---|
| 自定义颜色校正、坐标基变换 | 用 `QMatrix3x3`，维度固定且代码可读。 |
| 向着色器或图形接口传小矩阵 | 使用 `constData()`，并确认目标接口也按列主序解释。 |
| 与文件、数组、数学教材中的表格交换 | 使用构造函数或 `copyDataTo()`，它们使用行主序。 |
| 常见 4x4 图形变换 | 优先 `QMatrix4x4`；它提供平移、旋转、投影、求逆等高层操作。 |
| 运行时可变维度的数值计算 | 改用专门线性代数库；本类的维度是编译期常量。 |

## 6. 常见坑与经验

- 默认构造得到的是零矩阵，不是单位矩阵。做变换累积前应显式 `setToIdentity()`。
- `QGenericMatrix` 的“`N x M`”命名是列 x 行，阅读别名或乘法表达式时先转换成行 x 列思考。
- 浮点矩阵不宜用 `operator==` 判断计算结果是否“接近”；应逐元素采用容差比较。
- `data()` 返回的是对象内部地址。只要矩阵对象被销毁，该指针立即失效；不要将它保存到异步任务中。
- `operator/=` 的除数不能为零。对浮点数还要防范 NaN 与无穷值进入后续图形或几何运算。

## 7. 知识点覆盖

- 编译期维度与模板类型
- 行、列、转置和矩阵乘法的维度规则
- 行主序数据交换与列主序内存布局
- 值类型生命周期与原始指针有效期
- 图形计算中的单位矩阵、精度与容差比较
