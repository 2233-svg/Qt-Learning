# QQuaternion::Axis：四元数使用的三维轴值

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QQuaternion>`  
> 所属模块：`Qt6::Gui`  
> 类型性质：`QQuaternion` 内部的聚合结构体  
> 引入版本：Qt 6.11

`QQuaternion::Axis` 是一个只有 `x`、`y`、`z` 三个 `float` 字段的轻量结构体，用来表达四元数相关 API 使用的三维坐标轴。它和 `QVector3D` 很像，但语义更窄：它表示“作为旋转坐标系轴使用的向量”，而不是任意三维点或方向。

这个类型本身不约束字段值。它可以保存零向量、未归一化向量或任意浮点值；只有把它交给 `QQuaternion::fromAxes()` 等 API 时，调用方才需要遵守这些 API 对轴集合的几何要求。

## 它解决的问题

当旋转数据来自一个三维坐标系时，通常需要同时传递 X、Y、Z 三根轴。`Axis` 让这些向量带有更明确的“坐标轴”语义：

```cpp
QQuaternion::Axes axes{
    QQuaternion::Axis{1.0f, 0.0f, 0.0f},
    QQuaternion::Axis{0.0f, 1.0f, 0.0f},
    QQuaternion::Axis{0.0f, 0.0f, 1.0f}
};

QQuaternion rotation = QQuaternion::fromAxes(axes);
```

它主要用于：

- 和 `QQuaternion::Axes` 组合表示三根旋转基轴。
- 在 `QVector3D` 与四元数轴 API 之间转换。
- 让函数参数表达“这是旋转轴”而不是任意向量。
- 对轴是否接近零向量进行浮点容差判断。

## 它和 `QVector3D` 的区别

`QVector3D` 是通用三维向量，可以表示点、方向、法线、速度等；`Axis` 只是为了给四元数坐标轴增加语义的强类型包装。两者可以廉价、按值转换：

```cpp
QVector3D vector(0.0f, 1.0f, 0.0f);
QQuaternion::Axis axis = QQuaternion::Axis::fromVector3D(vector);
QVector3D roundTrip = axis.toVector3D();
```

转换不会自动归一化、修正正交性或检查是否适合作为旋转基轴。

## 轴值的几何边界

对于 `QQuaternion::fromAxes()`，三根轴通常应构成正交、归一化的右手坐标系。`Axis` 自身不保证这些条件，所以构造值和传给四元数前的验证属于调用方责任：

```cpp
QVector3D xAxis(1.0f, 0.0f, 0.0f);
QVector3D yAxis(0.0f, 1.0f, 0.0f);
QVector3D zAxis = QVector3D::crossProduct(xAxis, yAxis).normalized();

QQuaternion rotation = QQuaternion::fromAxes(xAxis, yAxis, zAxis);
```

`qFuzzyIsNull(axis)` 只能判断轴是否接近 `(0, 0, 0)`，不能判断它是否归一化、是否和另外两根轴正交。

## 值初始化与未初始化

由于 `Axis` 是聚合结构体，没有自定义构造函数，下面两种写法语义不同：

```cpp
QQuaternion::Axis zero{};       // x、y、z 都是 0
QQuaternion::Axis xAxis{1, 0, 0}; // 明确初始化
```

而局部变量 `QQuaternion::Axis axis;` 不会自动初始化字段。使用前必须显式初始化，否则 `x`、`y`、`z` 的值不确定。

## 被删除的比较与哈希接口

Qt 6.11.1 头文件故意删除了 `Axis` 的 `operator==`、`operator!=`、`qHash`、`qFuzzyCompare` 和 `comparesEqual` 相关实现，并明确要求用户不要自行实现这些接口。

因此不能把 `Axis` 直接作为 `QHash` 键，也不能直接写：

```cpp
// 不可用：Qt 6.11.1 中这些运算符被删除
// if (axis1 == axis2) { ... }
```

如果业务需要比较，应明确选择逐分量精确比较、逐分量 `qFuzzyCompare`，或比较转换后的 `QVector3D`，并把比较规则写在业务函数中。不要向 Qt 类型命名空间自行添加被 Qt 删除的重载。

## 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

```cpp
#include <QQuaternion>
#include <QVector3D>
```

## API 逐项说明

### 公共字段

#### `float QQuaternion::Axis::x`

保存三维轴的 X 分量。字段公开可读写，不会自动限制范围，也不会自动执行归一化。

#### `float QQuaternion::Axis::y`

保存三维轴的 Y 分量。字段公开可读写，修改后是否仍满足旋转基轴要求由调用方负责。

#### `float QQuaternion::Axis::z`

保存三维轴的 Z 分量。字段公开可读写，零值或未归一化值在结构体层面都是合法存储状态。

### 转换

#### `static constexpr noexcept QQuaternion::Axis QQuaternion::Axis::fromVector3D(QVector3D v)`

按 `v.x()`、`v.y()`、`v.z()` 构造 `Axis`。参数按值传递，适合直接从 `QVector3D` 转换；不会复制之外的资源，也不会归一化向量。

#### `constexpr noexcept QVector3D QQuaternion::Axis::toVector3D() const`

返回一个分量相同的 `QVector3D`。它是值返回，不会让返回值引用 `Axis` 内部字段。

### 浮点状态

#### `bool qFuzzyIsNull(QQuaternion::Axis axis) noexcept`

判断 `axis` 是否退化，即三个分量都在浮点容差内接近零。它适合拒绝零轴或识别退化输入，不适合验证正交归一坐标系。

该函数从 Qt 6.11 起提供。

### 明确不可用的接口

#### `operator==`、`operator!=`

Qt 6.11.1 中有意删除。不要直接比较两个 `Axis`，也不要自己在 Qt 命名空间补实现。

#### `qHash`、`qFuzzyCompare`、`comparesEqual`

Qt 6.11.1 中同样被有意删除。`Axis` 不是可直接哈希或模糊比较的通用值类型；需要这些能力时在业务层定义明确的包装或比较策略。

## 常见错误排查

1. **把 `Axis` 当成自动归一化向量**：它只是三个公开 `float` 字段，所有几何约束都由调用方负责。
2. **把一个轴传给 `fromAxes()` 就期待得到正确旋转**：该 API 需要三根轴，且通常要求它们构成正交归一坐标系。
3. **把 `qFuzzyIsNull()` 当作归一化检查**：它只判断是否接近零。
4. **局部声明后直接读取字段**：`Axis axis;` 的字段未初始化，使用 `Axis{}` 或逐字段初始化。
5. **直接写 `axis1 == axis2`**：Qt 6.11.1 删除了比较接口；按业务选择逐分量精确或容差比较。
6. **尝试把 `Axis` 放进 `QHash`**：Qt 删除了 `qHash`；使用 `QVector3D`、自定义键或显式序列化的业务包装。
7. **修改字段后忘记验证基轴**：公开字段允许产生非正交、非单位甚至零轴，传给旋转 API 前应检查。

## API 速查表

| 类别 | API | 作用 | 关键边界与注意事项 |
| --- | --- | --- | --- |
| 字段 | `float x` | 保存轴的 X 分量 | 公开可写；不自动归一化 |
| 字段 | `float y` | 保存轴的 Y 分量 | 公开可写；不自动检查正交性 |
| 字段 | `float z` | 保存轴的 Z 分量 | 公开可写；零值在结构体层面合法 |
| 转换 | `Axis::fromVector3D(QVector3D)` | `QVector3D` 转 `Axis` | `constexpr noexcept`；不归一化 |
| 转换 | `Axis::toVector3D()` | `Axis` 转 `QVector3D` | 返回分量副本 |
| 浮点判断 | `qFuzzyIsNull(Axis)` | 判断是否接近零轴 | Qt 6.11 起；不验证单位长度或正交 |
| 初始化 | `Axis{}` / `Axis{x, y, z}` | 值初始化轴 | 避免 `Axis axis;` 的未初始化字段 |
| 比较 | `operator==` / `operator!=` | 直接比较轴 | Qt 6.11.1 明确删除，不要自行补实现 |
| 哈希 | `qHash(Axis)` | 把轴作为哈希键 | Qt 6.11.1 明确删除 |
| 浮点比较 | `qFuzzyCompare(Axis)` | 模糊比较轴 | Qt 6.11.1 明确删除；在业务层定义规则 |

### 一句话总结

`QQuaternion::Axis` 是带旋转语义的三维浮点轴值，不替你归一化、不检查正交，也不提供比较和哈希；初始化好字段、用 `QVector3D` 做显式转换，并在交给四元数 API 前验证坐标系质量。
