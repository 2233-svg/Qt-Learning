# QQuaternion::EulerAngles：用欧拉角描述旋转

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QQuaternion>`  
> 所属模块：`Qt6::Gui`  
> 类型性质：`QQuaternion` 内部的模板聚合结构体  
> 引入版本：Qt 6.11

`QQuaternion::EulerAngles<T>` 是一个保存三个欧拉角的轻量结构体，字段为 `pitch`、`yaw` 和 `roll`。Qt 用 `EulerAngles<float>` 作为 `QQuaternion::eulerAngles()` 的返回类型，也提供 `QQuaternion::fromEulerAngles(EulerAngles<float>)` 从它构造四元数。

它解决的是“以人和工具更容易理解的三个轴旋转值来交换旋转数据”的问题。四元数更适合连续旋转、插值和组合；欧拉角更适合界面输入、配置文件、调试面板和导入导出。

## 三个字段的准确含义

| 字段 | 旋转轴 | 单位 |
| --- | --- | --- |
| `pitch` | 绕 X 轴 | 度 |
| `yaw` | 绕 Y 轴 | 度 |
| `roll` | 绕 Z 轴 | 度 |

字段顺序 `pitch, yaw, roll` 不等于旋转应用顺序。Qt 的 `fromEulerAngles()` 定义为：绕 Z 轴的 `roll`、绕 X 轴的 `pitch`、绕 Y 轴的 `yaw`，按该顺序组成旋转。不要把三个值当成可随意交换的独立变换。

```cpp
QQuaternion::EulerAngles<float> angles{
    15.0f,  // pitch: X
    30.0f,  // yaw:   Y
    5.0f    // roll:  Z
};

QQuaternion rotation = QQuaternion::fromEulerAngles(angles);
```

角度是度数，不是弧度。若数据来自使用弧度的数学库，转换后再传入：

```cpp
constexpr float radiansToDegrees = 180.0f / 3.14159265358979323846f;
angles.yaw = radians * radiansToDegrees;
```

## 它和四元数、`QVector3D` 的关系

`EulerAngles<T>` 只是三个公开字段，不拥有四元数，也不保存旋转矩阵。它不能自己执行旋转、插值或归一化。实际转换由 `QQuaternion` 完成：

```cpp
const auto angles = rotation.eulerAngles(); // Qt 6.11
QVector3D legacy = rotation.toEulerAngles();

QQuaternion a = QQuaternion::fromEulerAngles(angles);
QQuaternion b = QQuaternion::fromEulerAngles(legacy);
```

`toEulerAngles()` 返回的 `QVector3D` 分量约定为 `(pitch, yaw, roll)`，分别对应 X、Y、Z 轴；不要误读成常见的 `(roll, pitch, yaw)` 排列。

模板参数 `T` 没有被结构体自身限制，可以写成 `EulerAngles<double>`，但 Qt 当前按值接收的便捷构造重载是 `EulerAngles<float>`。需要使用其他精度时，应显式转换：

```cpp
QQuaternion::EulerAngles<double> precise{pitch, yaw, roll};
QQuaternion::EulerAngles<float> qtAngles{
    static_cast<float>(precise.pitch),
    static_cast<float>(precise.yaw),
    static_cast<float>(precise.roll)
};
```

## 欧拉角的固有边界

### 表示不唯一

同一个空间姿态可能对应多组欧拉角。四元数转换回欧拉角时，返回的是 Qt 选择的一组表示，不保证与最初输入的每个数值完全相同。若需要稳定保存姿态，优先保存四元数或矩阵；若面向用户显示，接受角度范围规范化和跳变处理。

### 万向节锁

欧拉角按固定轴顺序分解，在特定姿态附近可能出现自由度耦合，也就是万向节锁。动画插值、相机连续旋转和物理姿态通常应使用四元数 `slerp()`/`nlerp()`，不要在每一帧把欧拉角相加后再转换。

### 输入范围

`EulerAngles<T>` 不限制字段范围。`370` 度、`-90` 度或超大值在结构体层面都能存储；是否规范化、限制到 `[-180, 180)` 或其他范围由界面和业务决定。转换时 Qt 会按三角函数处理这些值。

## 初始化与数据安全

这是模板聚合结构体，没有自定义构造函数。推荐使用值初始化或完整的聚合初始化：

```cpp
QQuaternion::EulerAngles<float> zero{};       // 三个字段为 0
QQuaternion::EulerAngles<float> angles{10, 20, 30};
```

局部变量 `QQuaternion::EulerAngles<float> angles;` 的字段未初始化，不能直接读取或传给 `fromEulerAngles()`。

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

### 模板字段

#### `T QQuaternion::EulerAngles<T>::pitch`

保存绕 X 轴的旋转角，单位为度。字段公开可读写，结构体不会自动归一化或限制范围。

#### `T QQuaternion::EulerAngles<T>::yaw`

保存绕 Y 轴的旋转角，单位为度。不要将其与某个 UI 框架约定的“水平角”直接等同，最终要遵守调用方使用的坐标系。

#### `T QQuaternion::EulerAngles<T>::roll`

保存绕 Z 轴的旋转角，单位为度。它在 Qt 的 `fromEulerAngles()` 组合顺序中先参与 Z 轴旋转。

### 与 `QQuaternion` 协作的 API

#### `QQuaternion::EulerAngles<float> QQuaternion::eulerAngles() const`

从四元数返回欧拉角结构，三个字段单位都是度。该函数从 Qt 6.11 起提供。由于欧拉角表示不唯一，返回值不一定和构造该四元数时的原始角度逐项相同。

#### `static QQuaternion QQuaternion::fromEulerAngles(QQuaternion::EulerAngles<float> angles)`

从结构体字段构造四元数，等价于调用：

```cpp
QQuaternion::fromEulerAngles(angles.pitch, angles.yaw, angles.roll);
```

该重载从 Qt 6.11 起提供。旋转组合顺序和单位由三参数重载定义：`roll` 绕 Z、`pitch` 绕 X、`yaw` 绕 Y，按该顺序应用。

#### `static QQuaternion QQuaternion::fromEulerAngles(float pitch, float yaw, float roll)`

这是结构体重载的底层便捷形式。三个参数都是度数，Qt 定义的应用顺序是 Z/roll、X/pitch、Y/yaw。输入字段不要求在固定范围内。

#### `static QQuaternion QQuaternion::fromEulerAngles(const QVector3D &angles)`

使用 `QVector3D` 表示欧拉角时，`angles.x()` 是 pitch，`angles.y()` 是 yaw，`angles.z()` 是 roll；仍按 Z、X、Y 的 Qt 顺序组合，单位仍为度。

#### `QVector3D QQuaternion::toEulerAngles() const`

返回 `(pitch, yaw, roll)` 排列的 `QVector3D`，单位是度。它是旧式或向量接口；需要字段名称更清晰时使用 Qt 6.11 的 `eulerAngles()`。

## 实际场景建议

### 属性面板和配置文件

欧拉角适合作为用户输入：

```cpp
QQuaternion::EulerAngles<float> readAnglesFromUi()
{
    return {
        pitchSpinBox->value(),
        yawSpinBox->value(),
        rollSpinBox->value()
    };
}
```

把它转成四元数后用于渲染或姿态计算；不要把 UI 三个角度作为动画内部状态的唯一表示。

### 动画插值

```cpp
QQuaternion from = QQuaternion::fromEulerAngles(startAngles);
QQuaternion to = QQuaternion::fromEulerAngles(endAngles);
QQuaternion current = QQuaternion::slerp(from, to, progress);
```

插值在四元数空间进行，最后一刻再转换为矩阵或传给渲染 API。直接分别插值 `pitch/yaw/roll` 可能产生错误的旋转路径和角度跳变。

## 常见错误排查

1. **把角度按弧度传入**：Qt `fromEulerAngles()` 和 `eulerAngles()` 使用度。
2. **把字段顺序当成应用顺序**：字段是 pitch/yaw/roll，Qt 组合定义是 roll(Z)、pitch(X)、yaw(Y)。
3. **把 `QVector3D` 当成 `(roll, pitch, yaw)`**：Qt 约定 `x=pitch`、`y=yaw`、`z=roll`。
4. **期待转换后得到原始角度**：欧拉角表示不唯一，反向分解可能选择另一组等价角度。
5. **逐帧对欧拉角做线性插值**：可能出现万向节锁和不自然路径，动画使用四元数插值。
6. **声明后直接读取字段**：聚合结构体没有默认初始化，使用 `EulerAngles<float>{}`。
7. **把 `EulerAngles<double>` 直接传给 Qt 重载**：当前便捷重载接收 `EulerAngles<float>`，需要显式转换。
8. **以为结构体会限制范围或归一化**：字段公开，输入范围和规范化策略由业务决定。

## API 速查表

| 类别 | API | 作用 | 关键边界与注意事项 |
| --- | --- | --- | --- |
| 字段 | `EulerAngles<T>::pitch` | 保存绕 X 轴的角度 | 单位是度；不自动限制或归一化 |
| 字段 | `EulerAngles<T>::yaw` | 保存绕 Y 轴的角度 | 需遵守调用方坐标系；不等于固定 UI 语义 |
| 字段 | `EulerAngles<T>::roll` | 保存绕 Z 轴的角度 | Qt 组合中先参与 Z 轴旋转 |
| 初始化 | `EulerAngles<T>{}` | 值初始化三个角度 | 避免局部未初始化字段 |
| 查询 | `QQuaternion::eulerAngles()` | 四元数分解为 `EulerAngles<float>` | Qt 6.11 起；表示不唯一，单位为度 |
| 构造 | `QQuaternion::fromEulerAngles(EulerAngles<float>)` | 从结构体创建四元数 | 等价于三参数重载；按 Z、X、Y 组合 |
| 构造 | `QQuaternion::fromEulerAngles(float, float, float)` | 从 pitch/yaw/roll 创建四元数 | 参数为度；顺序是 roll(Z)、pitch(X)、yaw(Y) |
| 构造 | `QQuaternion::fromEulerAngles(QVector3D)` | 从向量创建四元数 | `x=pitch`、`y=yaw`、`z=roll` |
| 转换 | `QQuaternion::toEulerAngles()` | 返回 `(pitch, yaw, roll)` 向量 | 单位为度；不是 roll/pitch/yaw 排列 |
| 动画 | `QQuaternion::slerp()` / `nlerp()` | 在四元数空间插值 | 避免逐字段欧拉角插值的锁和跳变 |
| 精度 | `EulerAngles<double>` 到 `EulerAngles<float>` | 显式精度转换 | 当前 Qt 结构体便捷重载使用 `float` |

### 一句话总结

`QQuaternion::EulerAngles<T>` 只是三个带轴语义的角度字段：pitch 是 X、yaw 是 Y、roll 是 Z，单位为度；它适合人机交互和配置交换，连续旋转与插值仍应让四元数承担。
