# QVector2D

> Qt 6.11.1 · Qt GUI · 来自 `QVector2D`

## 1. 先建立直觉

`QVector2D` 表示二维数学向量 `(x, y)`，用于方向、位移、速度、法线和几何距离计算。名称中的 `Vector` 容易让人想到 Qt 容器，但它与保存多个元素的 `QVector` 无关：它始终只保存两个 `float` 分量。

同一对数字可以被当作“位置”或“方向”，区别来自你的语义。两点相减得到方向；位置加方向得到新位置。写代码时把二者混在一起通常不会报错，却会让变换和距离计算失去意义。

## 2. 类说明

- 头文件：`#include <QVector2D>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 对象模型：无 QObject、无堆资源的值类型。
- 协作类型：`QPoint` / `QPointF` 用于界面坐标，`QVector3D` / `QVector4D` 用于更高维计算，`QVariant` 用于元对象数据传递。

## 3. API 速查

| API | 用途 |
|---|---|
| `QVector2D(x, y)` | 由两个有限浮点分量构造向量。 |
| `x()` / `y()`、`setX()` / `setY()` | 读取或设置分量。 |
| `length()` / `lengthSquared()` | 计算长度或长度平方。 |
| `normalize()` / `normalized()` | 原地或复制后归一化为单位向量。 |
| `dotProduct(a, b)` | 点积；判断夹角、投影和朝向。 |
| `distanceToPoint(point)` | 当前点到目标点的欧氏距离。 |
| `distanceToLine(point, direction)` | 到过 `point` 且沿 `direction` 的直线距离。 |
| `toPoint()` / `toPointF()` | 转为 Qt 2D 坐标类型。 |
| `toVector3D()` / `toVector4D()` | 扩展为更高维向量，新增分量为 0。 |
| `operator[]` | 以 `0 => x`、`1 => y` 访问分量。 |
| `qFuzzyCompare()` | 容忍浮点误差地比较两个向量。 |
| `+`、`-`、标量 `*`、`/` | 向量加减与缩放。 |
| 向量 `*`、`/` | **逐分量**乘除，不是点积。 |

## 4. 关键用法

### 速度、方向与单位向量

```cpp
QVector2D position(20.0f, 10.0f);
QVector2D target(100.0f, 50.0f);

QVector2D direction = target - position;
if (!direction.isNull())
    direction.normalize();

const float speed = 80.0f;
position += direction * speed * deltaSeconds;
```

`normalized()` 返回新对象；`normalize()` 修改当前对象。零向量归一化不会崩溃，但结果仍是零向量，因此不能据此得到有效方向。需要“有没有方向”的逻辑时，应先检查 `isNull()` 或 `lengthSquared()`。

### 用点积区分同向、垂直与反向

```cpp
const QVector2D forward(1.0f, 0.0f);
const QVector2D toTarget = (target - position).normalized();
const float alignment = QVector2D::dotProduct(forward, toTarget);

// alignment 接近 1：同向；接近 0：垂直；接近 -1：反向
```

只有两个向量都已归一化时，点积才直接等于夹角余弦。若只需比较远近或避免开方，优先 `lengthSquared()`；它与距离平方比较等价，通常更便宜也更稳定。

### 点到直线的距离

```cpp
const QVector2D linePoint(0.0f, 20.0f);
const QVector2D lineDirection(1.0f, 0.0f); // 必须是单位方向
const float distance = mousePosition.distanceToLine(linePoint, lineDirection);
```

`distanceToLine()` 假定 `direction` 已经单位化；传入长度为 10 的方向会将结果缩放错误。零方向不代表“任意方向”，Qt 会把它退化为到 `point` 的距离。

## 5. 使用场景

| 场景 | 使用方式 |
|---|---|
| 拖拽、动画与滚动 | 位置差作为位移，归一化后乘速度。 |
| 命中检测、吸附线 | `distanceToPoint()` 或 `distanceToLine()` 与阈值比较。 |
| 2D 朝向与视野判断 | 归一化后使用点积。 |
| `QPainter`/鼠标事件坐标计算 | 在 `QPointF` 与 `QVector2D` 间转换。 |
| 3D 或着色器前的数据准备 | 用 `toVector3D()` / `toVector4D()` 明确补零。 |

## 6. 常见坑与经验

- `operator*(QVector2D, QVector2D)` 是 Hadamard 逐分量乘法；点积必须调用 `dotProduct()`。
- `toPoint()` 会四舍五入，像素精度布局或累计位移应保留 `QPointF`。
- `operator==` 是精确浮点比较；几何结果常应用 `qFuzzyCompare()` 或业务容差。
- 分量除法的除数不能含 0 或 NaN；必要时先逐分量保护。
- 构造和 setter 要求有限数值。不要让未检查的除法结果、NaN 或无穷值流入绘制计算。

## 7. 知识点覆盖

- 向量与点的语义区别
- 欧氏长度、平方长度、距离
- 单位向量与点积的几何含义
- 点到直线距离的前提
- 浮点比较、分量算术和坐标类型转换
