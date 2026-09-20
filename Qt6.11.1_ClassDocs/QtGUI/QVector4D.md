# QVector4D

> Qt 6.11.1 · Qt GUI · 来自 `QVector4D`

## 1. 先建立直觉

`QVector4D` 是四个 `float` 分量组成的数学向量 `(x, y, z, w)`。它可用于 RGBA 数据，也常用于三维图形的**齐次坐标**：位置通常编码为 `(x, y, z, 1)`，方向和法线通常编码为 `(x, y, z, 0)`。

第四分量不是可有可无的附加数字。在被 `QMatrix4x4` 变换时，`w=1` 让平移生效，`w=0` 让平移被忽略。这个规则正是同一矩阵能同时变换位置和方向的原因。

## 2. 类说明

- 头文件：`#include <QVector4D>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 对象模型：无资源所有权的值类型。
- 协作类型：`QVector3D`、`QMatrix4x4`、`QColor` 的 RGBA 语义，以及 `QVariant` / `QDataStream` 的数据传递。

## 3. API 速查

| API | 用途 |
|---|---|
| `QVector4D(x, y, z, w)` | 构造四分量向量。 |
| `x()` / `y()` / `z()` / `w()` 与 setters | 访问或修改单个分量。 |
| `length()` / `lengthSquared()` | 计算四维长度或其平方。 |
| `normalize()` / `normalized()` | 归一化四维向量。 |
| `dotProduct(a, b)` | 四维点积。 |
| `toVector2D()` / `toVector3D()` | 直接丢弃高维分量。 |
| `toVector2DAffine()` | 先以 `w` 除 x、y，再丢弃 z。 |
| `toVector3DAffine()` | 透视除法：`(x/w, y/w, z/w)`。 |
| `operator[]` | 通过 `0..3` 访问 x、y、z、w。 |
| `qFuzzyCompare()` | 近似比较浮点分量。 |
| `+`、`-`、`*`、`/` | 加减、缩放或逐分量算术。 |

## 4. 关键用法

### 明确构造位置与方向

```cpp
const QVector3D position3(3.0f, 2.0f, 1.0f);
const QVector3D direction3(0.0f, 0.0f, -1.0f);

const QVector4D position(position3, 1.0f);
const QVector4D direction(direction3, 0.0f);

const QVector4D movedPosition = transform * position;
const QVector4D movedDirection = transform * direction;
```

对包含平移的 `transform`，`movedPosition` 会移动，`movedDirection` 不会被平移。若误将方向构造成 `w=1`，旋转看似正常，平移一加入就会产生难以解释的方向偏移。

### 齐次坐标转回三维点

```cpp
const QVector4D clipOrHomogeneous(8.0f, 4.0f, 2.0f, 2.0f);
const QVector3D point = clipOrHomogeneous.toVector3DAffine();
// point == (4, 2, 1)
```

`toVector3D()` 只会丢弃 `w`，适合本来就代表普通四元数据的情况；`toVector3DAffine()` 会执行透视除法，适合齐次位置。`w == 0` 时后者返回零向量，避免除零，但这不是“无穷远点被正确转换”的通用表示，调用方应把它作为需要单独处理的状态。

### 颜色与分量运算

```cpp
QVector4D rgba(0.8f, 0.4f, 0.2f, 1.0f);
const QVector4D tint(1.0f, 0.7f, 0.7f, 1.0f);
rgba *= tint; // 每个通道单独相乘
```

向量乘法是逐分量运算，因而很适合颜色调制、每轴缩放与蒙版计算。需要相似度、投影或夹角关系时，应调用 `dotProduct()`，不能把 `operator*` 当成点积。

## 5. 使用场景

| 场景 | 使用方式 |
|---|---|
| 3D 变换管线 | 用 `w=1` 表示位置，`w=0` 表示方向/法线。 |
| 投影后的坐标复原 | 调用 `toVector3DAffine()` 执行透视除法。 |
| RGBA、HDR 或着色器常量 | 四分量颜色、通道乘法和统一参数传递。 |
| 四维插值或特征数据 | 使用长度、点积和标量缩放。 |
| API 数据桥接 | 通过 `QVariant` 或 `QDataStream` 传递和持久化。 |

## 6. 常见坑与经验

- `QVector3D::toVector4D()` 默认补 `w=0`，因此结果表示方向，而不是位置。要表达位置请写 `QVector4D(point3, 1.0f)`。
- `toVector3DAffine()` 与 `toVector3D()` 的语义完全不同；前者会除以 `w`。
- 对投影后的向量做 `normalize()` 通常没有几何意义。应先确认数据是颜色、方向还是齐次位置。
- `operator*(QVector4D, QVector4D)` 是逐分量相乘；点积只能使用 `dotProduct()`。
- 分量除法的除数不得为零或 NaN；透视除法前尤其要检查 `w`。
- 直接 `operator==` 采用精确比较。浮点变换后的结果应使用容差比较。

## 7. 知识点覆盖

- 四维向量与 RGBA 数据
- 齐次坐标、平移和 `w=0/1` 的差异
- 透视除法与无穷远方向
- 逐分量乘法和点积的边界
- 与 `QMatrix4x4`、`QVector3D` 的转换策略
