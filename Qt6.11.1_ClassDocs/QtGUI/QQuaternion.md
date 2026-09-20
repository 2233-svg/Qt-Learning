# QQuaternion

> Qt 6.11.1 · Qt GUI · 来自 `QQuaternion`

## 1. 先建立直觉

`QQuaternion` 用四个数表示三维旋转。与 Euler 角相比，它不会在连续组合旋转时直接遭遇万向节锁；与 3x3/4x4 矩阵相比，存储更小、插值更自然。它最适合相机朝向、物体姿态、骨骼动画和方向平滑。

它不是普通 4D 向量。用于表示旋转时，四元数应保持单位长度；相乘表示旋转组合，顺序决定谁先应用。直接对 x/y/z/scalar 分量做业务运算通常会破坏旋转语义。

## 2. 类说明

- 头文件：`#include <QQuaternion>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：轻量值类型，分量为 scalar `w` 与 vector `(x, y, z)`。
- 默认构造为单位旋转 `(1, 0, 0, 0)`；零四元数 `(0, 0, 0, 0)` 不代表任何有效旋转。
- Qt 6.11 新增具名 `Axis`、`Axes` 与 `EulerAngles` 结构，减少“这三个 float 究竟是什么”的歧义。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QQuaternion()` | 创建单位旋转 |
| `QQuaternion(scalar, x, y, z)` | 直接构造分量；仅适合底层算法/反序列化 |
| `fromAxisAndAngle(axis, degrees)` | 从单位轴与角度创建归一化旋转 |
| `fromEulerAngles(pitch, yaw, roll)` | 从指定顺序的欧拉角创建旋转 |
| `fromDirection(direction, up)` | 根据朝向和上方向构造姿态 |
| `fromAxes(x, y, z)` / `fromAxes(Axes)` | 从正交归一坐标轴构造，Qt 6.11 有具名结构 |
| `fromRotationMatrix()` | 从 3x3 旋转矩阵创建；输入应无缩放 |
| `rotationTo(from, to)` | 获取从一个方向转到另一个方向的最短弧旋转 |
| `rotatedVector(v)` / `operator*(q, v)` | 用旋转变换一个向量 |
| `operator*(q1, q2)` / `*=` | 组合旋转，顺序重要 |
| `normalized()` / `normalize()` | 返回或原地恢复单位长度 |
| `length()` / `lengthSquared()` | 检查范数，诊断数值漂移 |
| `conjugated()` | 反转虚部；单位四元数时等于逆旋转 |
| `inverted()` | 求数学逆；零四元数返回零 |
| `slerp(q1, q2, t)` | 沿最短球面路径匀角速度插值 |
| `nlerp(q1, q2, t)` | 归一化线性插值，快但非匀角速度 |
| `dotProduct()` | 比较方向/决定插值同半球 |
| `toRotationMatrix()` | 转成 3x3 矩阵，未归一化会夹带缩放 |
| `toEulerAngles()` / `eulerAngles()` | 转为欧拉角；表示不唯一且有奇异点 |
| `getAxisAndAngle()` | 提取旋转轴与角度 |
| `toAxes()` | Qt 6.11 起导出正交归一轴 |
| `isIdentity()` / `isNull()` | 判断单位旋转或全零值 |
| `scalar()` / `vector()` / `x/y/z` 及 setter | 访问原始分量，通常需随后归一化 |
| `qFuzzyCompare()` / QVariant / 数据流运算符 | 浮点比较、元类型和存储 |

## 4. 关键用法

### 从轴角创建并旋转一个方向

```cpp
const QQuaternion turn =
    QQuaternion::fromAxisAndAngle(QVector3D(0, 1, 0), 45.0f);

const QVector3D forward(0, 0, -1);
const QVector3D rotated = turn.rotatedVector(forward);
```

轴应是非零方向，Qt 会生成归一化旋转。`fromAxisAndAngle()` 的角度是**度**；不要把弧度直接传入。若旋转对象位置，四元数只作用于方向/向量，平移应由 `QMatrix4x4` 或独立 position 管理。

### 组合姿态时明确顺序

```cpp
const QQuaternion yaw =
    QQuaternion::fromAxisAndAngle(0, 1, 0, 30);
const QQuaternion pitch =
    QQuaternion::fromAxisAndAngle(1, 0, 0, -15);

const QQuaternion orientation = yaw * pitch;
```

四元数乘法不交换。组合表达的是一系列旋转，局部轴还是世界轴取决于乘法侧与约定；建立一个小测试，用已知前向/上向向量验证顺序，别凭直觉修改。

### 动画中使用合适插值

```cpp
const float t = std::clamp(progress, 0.0f, 1.0f);
const QQuaternion smooth =
    QQuaternion::slerp(startOrientation, endOrientation, t);
```

`slerp()` 视觉上保持匀角速度，适合相机和大角度姿态动画；`nlerp()` 更便宜，适合小角度、高频插值或能接受速度轻微不均的场景。两者都沿最短路径处理等价的 `q` 与 `-q` 表示。

### 防止累计误差破坏旋转

```cpp
orientation = incrementalTurn * orientation;
if (++framesSinceNormalize == 60) {
    orientation.normalize();
    framesSinceNormalize = 0;
}
```

有限精度下连续乘法会让长度偏离 1，随后 `toRotationMatrix()` 与 `rotatedVector()` 会引入缩放/形变。高频积分应周期性归一化；若输入来自外部或网络，使用前先检查是否接近有效单位四元数。

### 从方向建立相机姿态

```cpp
const QQuaternion viewRotation =
    QQuaternion::fromDirection(target - eye, QVector3D(0, 1, 0));
```

当 `direction` 与 `up` 平行/近似平行时，上方向不再唯一；Qt 会选择新的正交 up。若产品需要稳定的 roll，需在接近退化方向时自行保存上一帧侧向轴或定义明确的 fallback。

## 5. 欧拉角与矩阵边界

| 转换 | 适合 | 风险 |
| --- | --- | --- |
| `fromEulerAngles()` | UI 编辑器输入、简单姿态面板 | 顺序固定且欧拉角有万向节锁 |
| `toEulerAngles()` | 展示/编辑字段 | 同一旋转可有多组角；接近奇异点会跳变 |
| `fromRotationMatrix()` | 从外部 3x3 基变换接入 | 输入必须正交归一，否则会带入缩放 |
| `toRotationMatrix()` | 传给线性代数/渲染 API | 四元数未归一化时矩阵不再是纯旋转 |
| `toAxes()` / `fromAxes()` | 相机 basis、坐标系调试 | 轴必须正交归一 |

## 6. 常见坑与经验

- **单位四元数与零四元数不同。** 默认值是 identity，不是 null；null 不能拿来表示“没有旋转”。
- **`conjugated()` 只对单位旋转等同逆。** 任意四元数要用 `inverted()`；但旋转数据本就应归一化。
- **不要逐帧 `toEulerAngles()` 再 `fromEulerAngles()`。** 会引入角度跳变与锁死；内部状态保留四元数，UI 仅做边界转换。
- **`operator==` 是精确浮点比较。** 旋转相同的 `q` 与 `-q` 分量完全不同；对旋转等价性使用 dot、角度容差或正确的规范化策略。
- **轴、方向、up 均要检查长度。** 传零向量或几乎共线的 basis 会产生不可预期姿态。
- **新 `Axis` 结构不是自动校验器。** Qt 6.11 的强类型提升可读性，但 axis 是否单位、axes 是否正交仍由调用者保证。

## 7. 知识点覆盖

三维旋转、单位四元数、姿态组合、轴角、欧拉角、万向节锁、SLERP/NLERP、数值漂移、方向与上向量、旋转矩阵、坐标基、动画插值。
