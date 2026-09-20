# Qt QLineF 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QLineF>`  
> 所属模块：`Qt6::Core`  
> 形式：值类型，保存两个 `QPointF` 端点  
> 相关类型：`QLine`、`QPointF`、`QDataStream`

## 1. 先给结论：它解决什么问题

`QLineF` 表示二维平面上的**有限浮点线段**。它在 `QLine` 的两个端点模型上增加了：

- 小数坐标；
- 长度和方向角；
- 两条线段的相交分类；
- 单位向量和法向量；
- 按参数取线段上的点；
- 浮点平移和整数线段转换。

它适合：

- 反锯齿绘制和亚像素定位；
- 鼠标、触摸、图形编辑中的精确几何计算；
- 角度、长度和方向处理；
- 碰撞检测或线段相交测试；
- 将极坐标描述转换成线段；
- 在浮点坐标和整数绘图坐标之间转换。

它仍然是有限线段，不是无限直线。`intersects()` 会同时考虑两条线段的有限端点范围，并通过返回值区分“延长线相交”和“线段本身相交”。

## 2. 最小可用代码

```cpp
#include <QLineF>
#include <QPointF>

QLineF makeGuideLine(const QPointF &start, const QPointF &end)
{
    return QLineF(start, end);
}

void inspectLine(const QLineF &line)
{
    qDebug() << "length:" << line.length()
             << "angle:" << line.angle()
             << "dx/dy:" << line.dx() << line.dy()
             << "null:" << line.isNull();
}
```

默认构造的 `QLineF` 是空线段，两个端点都是 `(0, 0)`。浮点线段的空判断使用模糊比较，因此“接近重合”的端点也可能使 `isNull()` 返回 `true`。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QLineF>
```

### 3.3 qmake

```qmake
QT += core
```

如果使用数据流运算符，还需要：

```cpp
#include <QDataStream>
```

## 4. 端点、方向和浮点精度

### 4.1 端点仍然是有序的

```cpp
const QLineF forward(QPointF(0.0, 0.0),
                     QPointF(10.0, 5.0));
const QLineF backward(QPointF(10.0, 5.0),
                      QPointF(0.0, 0.0));
```

两条线段覆盖同一几何位置，但方向相反：

- `dx()` 和 `dy()` 符号相反；
- `angle()` 通常相差 180 度；
- `operator==` 不把端点反向视为同一有序线段；
- `angleTo()` 会考虑方向。

### 4.2 `qreal` 是 Qt 的浮点类型

`QLineF` 的坐标、长度和角度使用 `qreal`。在常见桌面构建中它通常对应 `double`，但代码应使用 `qreal` 而不是自行假设具体底层类型。

浮点数带来这些边界：

- 计算结果可能存在舍入误差；
- 不要用 `==` 表达“数学上足够接近”的业务判断；
- `isNull()`、`qFuzzyCompare()` 和 `qFuzzyIsNull()` 采用 Qt 的模糊比较规则；
- 需要稳定的容差时，业务代码可能需要自己的误差阈值。

### 4.3 分量、长度和中心点

```cpp
const QLineF line(QPointF(2.0, 3.0),
                  QPointF(8.0, 11.0));

const qreal dx = line.dx();       // 6
const qreal dy = line.dy();       // 8
const qreal length = line.length(); // 10
const QPointF center = line.center();
```

`dx()` 和 `dy()` 是向量分量，不是线段长度。`center()` 返回两个端点的浮点平均值。

## 5. `IntersectionType`：相交不是简单的 bool

```cpp
enum IntersectionType {
    NoIntersection,
    BoundedIntersection,
    UnboundedIntersection
};
```

| 枚举值 | 数值 | 含义 |
| --- | ---: | --- |
| `NoIntersection` | `0` | 两条线段的延长线不产生可用交点，通常表示平行。 |
| `BoundedIntersection` | `1` | 交点同时位于两条有限线段的端点范围内。 |
| `UnboundedIntersection` | `2` | 延长线相交，但交点不在两条线段的有限范围内，或只在其中一条范围内。 |

示例：

```cpp
QPointF point;
const QLineF horizontal(QPointF(0, 0), QPointF(10, 0));
const QLineF vertical(QPointF(5, -2), QPointF(5, 2));

const auto type = horizontal.intersects(vertical, &point);
if (type == QLineF::BoundedIntersection)
    qDebug() << "segment intersection:" << point;
```

需要特别区分：

- `NoIntersection` 不是“两个无限直线一定没有交点”的通用数学定义说明，而是 Qt 该 API 的分类结果；
- `UnboundedIntersection` 表示延长线的交点存在，但有限线段不能在该点相交；
- 如果传入 `intersectionPoint` 指针，平行时交点值未定义；
- 不需要交点坐标时可以传 `nullptr`。

## 6. 角度语义

### 6.1 `angle()` 使用度数

```cpp
const QLineF line(QPointF(0, 0), QPointF(1, 1));
qDebug() << line.angle(); // 约 45
```

Qt 的角度规则是：

- 单位为度，不是弧度；
- 从正 x 轴方向开始；
- 逆时针为正方向；
- 返回范围是 `0.0` 到小于 `360.0`；
- 零度方向是向右。

如果要传给 `std::sin()`、`std::cos()` 等标准库函数，需要先把角度转换为弧度。

### 6.2 `angleTo()` 计算有方向的旋转量

```cpp
const QLineF horizontal(QPointF(0, 0), QPointF(10, 0));
const QLineF vertical(QPointF(0, 0), QPointF(0, 10));

const qreal degrees = horizontal.angleTo(vertical);
```

返回值表示需要从当前线段逆时针旋转多少度，才能得到目标线段的方向。它考虑线段方向；端点反向会改变结果。

如果两条有限线段不在其自身范围内相交，角度计算使用延长线的交点作为参考原点。不要把 `angleTo()` 当作“两个位置之间的角度”，它比较的是方向。

### 6.3 `fromPolar()`

```cpp
const QLineF line = QLineF::fromPolar(10.0, 30.0);
```

它创建一条：

- 起点位于原点 `(0, 0)`；
- 长度为 `length`；
- 方向角为 `angle` 度；
- 正角度表示逆时针；
- 0 度指向正 x 轴；

的线段。

如果要把结果移动到其他起点，再调用 `translate()` 或 `translated()`。

## 7. 长度、单位向量和法向量

### 7.1 `length()`

```cpp
const qreal length = line.length();
```

返回两端点之间的欧氏距离。长度是浮点结果，比较时通常使用容差。

### 7.2 `setLength()`

```cpp
QLineF line(QPointF(1, 2), QPointF(4, 6));
line.setLength(20.0);
```

它保持起点 `p1()` 不变，移动终点 `p2()`，使线段长度变为指定值。

边界：

- `length` 应为有限浮点值；
- 当前线段长度为零时，不执行缩放，终点不会因为无法确定方向而被任意移动；
- 负长度不是通常的几何长度用法，业务代码应使用非负长度；
- 设置长度会改变终点，不会保持终点位置。

### 7.3 `unitVector()`

```cpp
const QLineF unit = line.unitVector();
```

返回从相同起点出发、方向相同、长度为 `1.0` 的线段。

只有非空线段才有明确的单位方向。对空线段调用时不要依赖一个有意义的单位向量结果。

### 7.4 `normalVector()`

```cpp
const QLineF normal = line.normalVector();
```

返回与当前线段垂直、起点相同、长度相同的线段。根据 Qt 头文件实现，其方向向量为：

```text
(dx, dy) -> (dy, -dx)
```

在屏幕坐标系中，“向上”方向的视觉含义可能与数学坐标系不同，所以不要只凭图形直觉判断法向量朝向，应根据坐标系和返回端点验证。

## 8. 参数取点：`pointAt(t)`

```cpp
const QLineF line(QPointF(10, 20),
                  QPointF(30, 40));

const QPointF start = line.pointAt(0.0);
const QPointF middle = line.pointAt(0.5);
const QPointF end = line.pointAt(1.0);
```

参数语义：

```text
pointAt(t) = p1 + t * (p2 - p1)
```

- `t == 0`：起点；
- `t == 1`：终点；
- `0 < t < 1`：线段内部；
- `t < 0`：沿起点方向反向外推；
- `t > 1`：沿终点方向继续外推。

因此 `pointAt()` 不会自动把 `t` 限制在 `[0, 1]`。如果业务只允许线段内部，需要调用方自己检查或裁剪参数。

## 9. 修改端点和移动线段

### 9.1 端点 setter

```cpp
line.setP1(newStart);
line.setP2(newEnd);
line.setPoints(newStart, newEnd);
line.setLine(x1, y1, x2, y2);
```

这些函数只替换端点，不会自动保持原长度、原角度或原方向约束。

### 9.2 `translate()` 和 `translated()`

```cpp
line.translate(QPointF(2.5, -1.0));
line.translate(2.5, -1.0);
```

`translate()` 修改当前对象。

```cpp
const QLineF moved = line.translated(QPointF(2.5, -1.0));
```

`translated()` 返回副本，保留当前对象。

| 需求 | API |
| --- | --- |
| 就地移动 | `translate()` |
| 保留原线段 | `translated()` |
| 偏移量是点 | `QPointF` 重载 |
| 偏移量是两个浮点值 | `qreal, qreal` 重载 |

## 10. `isNull()`、相等和模糊比较

### 10.1 `isNull()` 不是严格零长度判断

```cpp
const QLineF line(QPointF(1.0, 1.0),
                  QPointF(1.0 + 1e-15, 1.0));
```

由于 `QLineF::isNull()` 使用 Qt 的模糊比较，极小但非零的坐标差异可能被视为空线段。文档明确提醒：`isNull()` 可能在线段 `length()` 不为零时仍返回 `true`。

如果业务要求自己的误差阈值，直接检查：

```cpp
const bool almostZero = qAbs(line.length()) <= tolerance;
```

### 10.2 `operator==` 与 `qFuzzyCompare`

`operator==` 比较两个有序线段的端点。浮点几何中更明确的近似比较可以使用 Qt 6.8 起提供的：

```cpp
if (qFuzzyCompare(lhs, rhs))
    handleAlmostSameLine();
```

`qFuzzyCompare()` 比较起点和终点是否近似相等，端点顺序仍然重要。

```cpp
const QLineF a(QPointF(0, 0), QPointF(10, 10));
const QLineF b(QPointF(10, 10), QPointF(0, 0));
Q_ASSERT(!qFuzzyCompare(a, b));
```

### 10.3 `qFuzzyIsNull()`

Qt 6.8 起可以使用：

```cpp
if (qFuzzyIsNull(line))
    handleDegenerateLine();
```

它判断起点和终点是否近似相等。它与 `isNull()` 都反映浮点近似，但 `qFuzzyIsNull()` 作为独立非成员函数更适合和其他 `qFuzzy...` API 一起使用。

## 11. `QLine` 与 `QLineF` 的转换

### 11.1 从 `QLine` 到 `QLineF`

```cpp
const QLineF floatingLine(integerLine);
```

整数端点可以精确转换为浮点端点。也可以使用：

```cpp
const QLineF floatingLine = integerLine.toLineF();
```

### 11.2 从 `QLineF` 到 `QLine`

```cpp
const QLine integerLine = floatingLine.toLine();
```

此转换会把两个浮点端点舍入到最近整数。它可能改变：

- 端点坐标；
- 长度；
- 角度；
- 是否与另一条线段相交；
- 线段是否变成空线段。

需要保留亚像素信息时，不要过早调用 `toLine()`。

## 12. 逐项 API 说明

### 12.1 `QLineF()`

```cpp
constexpr QLineF();
```

构造两个端点均为 `(0, 0)` 的空线段。

### 12.2 `QLineF(const QLine &line)`

```cpp
constexpr QLineF(const QLine &line);
```

把整数线段的端点转换为浮点端点，不产生小数舍入。

### 12.3 `QLineF(const QPointF &p1, const QPointF &p2)`

```cpp
constexpr QLineF(const QPointF &p1, const QPointF &p2);
```

用两个浮点点构造有序线段。

### 12.4 `QLineF(qreal x1, qreal y1, qreal x2, qreal y2)`

```cpp
constexpr QLineF(qreal x1, qreal y1,
                 qreal x2, qreal y2);
```

用四个浮点坐标构造线段。

### 12.5 `QPointF p1() const`

```cpp
constexpr QPointF p1() const;
```

返回起点副本。

### 12.6 `QPointF p2() const`

```cpp
constexpr QPointF p2() const;
```

返回终点副本。

### 12.7 `qreal x1() const`

```cpp
constexpr qreal x1() const;
```

返回起点 x 坐标。

### 12.8 `qreal y1() const`

```cpp
constexpr qreal y1() const;
```

返回起点 y 坐标。

### 12.9 `qreal x2() const`

```cpp
constexpr qreal x2() const;
```

返回终点 x 坐标。

### 12.10 `qreal y2() const`

```cpp
constexpr qreal y2() const;
```

返回终点 y 坐标。

### 12.11 `qreal dx() const`

```cpp
constexpr qreal dx() const;
```

返回水平分量 `x2() - x1()`。

### 12.12 `qreal dy() const`

```cpp
constexpr qreal dy() const;
```

返回垂直分量 `y2() - y1()`。

### 12.13 `QPointF center() const`

```cpp
constexpr QPointF center() const;
```

返回两个端点的浮点中点。

### 12.14 `bool isNull() const`

```cpp
constexpr bool isNull() const;
```

如果两个端点在 Qt 的模糊比较下没有可区分差异，返回 `true`。不能把它当成严格的 `length() == 0` 判断。

### 12.15 `static QLineF fromPolar(qreal length, qreal angle)`

```cpp
static QLineF fromPolar(qreal length,
                        qreal angle);
```

创建起点为原点、长度为 `length`、角度为 `angle` 度的线段。

### 12.16 `qreal length() const`

```cpp
qreal length() const;
```

返回线段的欧氏长度。

### 12.17 `void setLength(qreal length)`

```cpp
void setLength(qreal length);
```

保持起点不变，移动终点以设置长度。当前长度为零时不执行缩放；传入值应为有限数值。

### 12.18 `qreal angle() const`

```cpp
qreal angle() const;
```

返回方向角，单位是度，范围为 `[0, 360)`，从正 x 轴逆时针测量。

### 12.19 `void setAngle(qreal angle)`

```cpp
void setAngle(qreal angle);
```

改变终点位置，使线段具有指定方向角，同时保持起点和当前长度。

正角度表示逆时针，0 度指向右方。该函数改变 `p2()`，不会把线段平移到新的起点。

### 12.20 `qreal angleTo(const QLineF &line) const`

```cpp
qreal angleTo(const QLineF &line) const;
```

返回从当前线段方向旋转到目标线段方向所需的逆时针角度，单位为度。它考虑端点方向；不要把它理解成两个位置之间的夹角。

### 12.21 `QLineF unitVector() const`

```cpp
QLineF unitVector() const;
```

返回起点相同、方向相同、长度为 `1.0` 的线段。空线段没有可用方向，调用前应先确认线段非空。

### 12.22 `QLineF normalVector() const`

```cpp
constexpr QLineF normalVector() const;
```

返回起点相同、长度相同、与当前线段垂直的线段。Qt 实现使用向量 `(dy, -dx)` 作为法向方向。

### 12.23 `IntersectionType intersects(const QLineF &line, QPointF *intersectionPoint = nullptr) const`

```cpp
IntersectionType intersects(
    const QLineF &line,
    QPointF *intersectionPoint = nullptr) const;
```

判断当前有限线段与目标有限线段的相交分类。

返回：

- `NoIntersection`：无交；
- `BoundedIntersection`：交点在两条线段范围内；
- `UnboundedIntersection`：延长线相交，但交点不在两条线段的共同有限范围内。

如果两条线平行，`intersectionPoint` 的内容未定义。只有需要交点时才传入有效指针。

### 12.24 `QPointF pointAt(qreal t) const`

```cpp
constexpr QPointF pointAt(qreal t) const;
```

按参数返回线段参数化位置：

```text
p1 + t * (p2 - p1)
```

`t` 不会自动限制在 `[0, 1]`。值超出该区间时，函数返回延长线上的点。

### 12.25 `void setP1(const QPointF &p1)`

```cpp
void setP1(const QPointF &p1);
```

替换起点，终点不变。

### 12.26 `void setP2(const QPointF &p2)`

```cpp
void setP2(const QPointF &p2);
```

替换终点，起点不变。

### 12.27 `void setPoints(const QPointF &p1, const QPointF &p2)`

```cpp
void setPoints(const QPointF &p1,
               const QPointF &p2);
```

同时替换起点和终点。

### 12.28 `void setLine(qreal x1, qreal y1, qreal x2, qreal y2)`

```cpp
void setLine(qreal x1, qreal y1,
             qreal x2, qreal y2);
```

用四个浮点坐标同时替换两个端点。

### 12.29 `QLine toLine() const`

```cpp
constexpr QLine toLine() const;
```

返回整数线段副本。两个端点会舍入到最近整数，因此转换可能改变几何关系。

### 12.30 `void translate(const QPointF &offset)`

```cpp
constexpr void translate(const QPointF &offset);
```

把偏移量加到两个端点，直接修改当前对象。

### 12.31 `void translate(qreal dx, qreal dy)`

```cpp
constexpr void translate(qreal dx, qreal dy);
```

按两个浮点偏移量直接修改当前对象。

### 12.32 `QLineF translated(const QPointF &offset) const`

```cpp
constexpr QLineF translated(const QPointF &offset) const;
```

返回平移后的副本，不修改当前线段。

### 12.33 `QLineF translated(qreal dx, qreal dy) const`

```cpp
constexpr QLineF translated(qreal dx,
                            qreal dy) const;
```

按两个浮点偏移量返回平移副本。

### 12.34 `bool qFuzzyCompare(const QLineF &lhs, const QLineF &rhs)`

```cpp
constexpr bool qFuzzyCompare(
    const QLineF &lhs,
    const QLineF &rhs) noexcept;
```

Qt 6.8 起提供。比较两个线段的起点和终点是否近似相等，端点顺序仍然参与判断。

### 12.35 `bool qFuzzyIsNull(const QLineF &line)`

```cpp
constexpr bool qFuzzyIsNull(
    const QLineF &line) noexcept;
```

Qt 6.8 起提供。判断线段两个端点是否近似相等。

### 12.36 `bool operator==(const QLineF &lhs, const QLineF &rhs)`

```cpp
constexpr bool operator==(
    const QLineF &lhs,
    const QLineF &rhs) noexcept;
```

判断两个有序浮点线段是否相等。浮点几何中，如果业务需要明确容差，优先使用 `qFuzzyCompare()` 或自定义容差。

### 12.37 `bool operator!=(const QLineF &lhs, const QLineF &rhs)`

```cpp
constexpr bool operator!=(
    const QLineF &lhs,
    const QLineF &rhs) noexcept;
```

判断两个有序浮点线段是否不相等。

### 12.38 `QDataStream &operator<<(QDataStream &, const QLineF &)`

```cpp
QDataStream &operator<<(
    QDataStream &stream,
    const QLineF &line);
```

把浮点线段写入数据流并返回流引用。格式受 `QDataStream` 版本和设置影响。

### 12.39 `QDataStream &operator>>(QDataStream &, QLineF &)`

```cpp
QDataStream &operator>>(
    QDataStream &stream,
    QLineF &line);
```

从数据流读取浮点线段。读取后应检查流状态。

### 12.40 `using IntersectType = IntersectionType`

```cpp
using IntersectType = IntersectionType;
```

这是旧名称的兼容别名，已弃用。新代码使用 `IntersectionType`。

## 13. 常见误区与排查顺序

### 13.1 把 `QLineF` 当作无限直线

`QLineF` 仍然只有有限端点。`UnboundedIntersection` 只表示延长线的交点不在双方有限范围内。

### 13.2 把角度当成弧度

`angle()`、`angleTo()`、`setAngle()` 和 `fromPolar()` 都使用度数。传给标准三角函数前要转弧度。

### 13.3 误以为 `pointAt()` 会限制在线段内

`pointAt(-1)` 和 `pointAt(2)` 都是合法的参数化外推。业务需要线段内部时，自己检查 `0 <= t && t <= 1`。

### 13.4 用 `isNull()` 做严格零长度判断

它使用模糊比较，可能对极小非零长度返回 `true`。需要精确业务阈值时使用自定义容差。

### 13.5 对零长度线段调用 `unitVector()`

零长度没有方向。先处理退化线段，再计算单位向量。

### 13.6 以为 `setLength()` 会移动整条线段

它保持起点不变，只调整终点。

### 13.7 忽略 `intersects()` 的输出条件

平行时交点指针指向的值未定义。返回 `NoIntersection` 时不要读取输出点。

### 13.8 过早转换为 `QLine`

`toLine()` 会舍入端点，可能改变相交、长度和空线段判断。只有确定需要整数坐标时再转换。

### 13.9 依赖浮点 `operator==` 表达业务容差

浮点结果来自三角函数、除法和几何运算，业务上的“足够接近”应明确使用 `qFuzzyCompare()` 或项目自己的阈值。

### 13.10 忽略有序端点

反向线段的几何位置相同，但方向、角度、参数化和相等判断都可能不同。

### 13.11 用默认 `QDataStream` 格式做长期协议

长期存储和跨进程协议应固定 `QDataStream` 版本、字节序和兼容策略，不能只依赖当前默认设置。

## 14. 一段完整的线段相交示例

```cpp
#include <QLineF>
#include <QPointF>

struct IntersectionResult
{
    bool hit = false;
    bool onBothSegments = false;
    QPointF point;
};

IntersectionResult intersectSegments(const QLineF &a,
                                     const QLineF &b)
{
    IntersectionResult result;
    const auto type = a.intersects(b, &result.point);

    if (type == QLineF::NoIntersection)
        return result;

    result.hit = true;
    result.onBothSegments =
        type == QLineF::BoundedIntersection;
    return result;
}
```

如果业务要把延长线交点也作为有效结果，`UnboundedIntersection` 需要单独处理；不能把返回值简单转换成“线段命中”的布尔值。

## 15. 一段完整的方向和长度示例

```cpp
#include <QLineF>
#include <QtMath>

QLineF makeArrow(const QPointF &start,
                 qreal length,
                 qreal angleDegrees)
{
    QLineF arrow =
        QLineF::fromPolar(length, angleDegrees);
    arrow.translate(start);
    return arrow;
}

QLineF normalize(const QLineF &line)
{
    if (line.isNull())
        return {};
    return line.unitVector();
}
```

这个例子把 `fromPolar()` 的原点起线段移动到指定起点，并在归一化前排除退化线段。

## API 速查表
### 16.1 构造与基本读取

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QLineF()` | 构造空线段。 | 两个端点为 `(0, 0)`。 |
| `QLineF(const QLine &line)` | 从整数线段构造浮点线段。 | 不产生小数舍入。 |
| `QLineF(const QPointF &, const QPointF &)` | 用两个浮点点构造有序线段。 | 端点顺序影响方向。 |
| `QLineF(qreal, qreal, qreal, qreal)` | 用四个浮点坐标构造线段。 | 使用 `qreal`，不要假设固定底层类型。 |
| `QPointF p1() const` | 返回起点。 | 返回点副本。 |
| `QPointF p2() const` | 返回终点。 | 返回点副本。 |
| `qreal x1() const` | 返回起点 x。 | 浮点精度。 |
| `qreal y1() const` | 返回起点 y。 | 浮点精度。 |
| `qreal x2() const` | 返回终点 x。 | 浮点精度。 |
| `qreal y2() const` | 返回终点 y。 | 浮点精度。 |
| `qreal dx() const` | 返回水平分量。 | 不是长度。 |
| `qreal dy() const` | 返回垂直分量。 | 不是长度。 |
| `QPointF center() const` | 返回浮点中点。 | 端点平均值。 |
| `bool isNull() const` | 模糊判断两端点是否重合。 | 非零极小长度也可能返回 `true`。 |

### 16.2 长度和角度

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `static QLineF fromPolar(qreal length, qreal angle)` | 从原点创建指定长度和角度的线段。 | 角度是度数，0 度向右。 |
| `qreal length() const` | 返回欧氏长度。 | 浮点结果，比较通常需要容差。 |
| `void setLength(qreal length)` | 保持起点不变，设置线段长度。 | 当前长度为零时不缩放；输入应有限。 |
| `qreal angle() const` | 返回方向角。 | 范围 `[0, 360)`，单位度。 |
| `void setAngle(qreal angle)` | 保持起点和长度，改变终点方向。 | 正角度逆时针。 |
| `qreal angleTo(const QLineF &line) const` | 返回两个有向线段的逆时针方向差。 | 比较方向，不是位置夹角。 |

### 16.3 向量、参数化和相交

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QLineF unitVector() const` | 返回同起点、同方向、长度为 1 的线段。 | 空线段没有有效方向。 |
| `QLineF normalVector() const` | 返回同起点、同长度的垂直线段。 | 方向为 `(dy, -dx)`。 |
| `QPointF pointAt(qreal t) const` | 按参数返回线段或延长线上的点。 | `t` 不自动限制在 `[0, 1]`。 |
| `IntersectionType intersects(const QLineF &, QPointF * = nullptr) const` | 分类两条线段是否相交。 | 区分有限范围相交和延长线相交；平行时交点未定义。 |
| `NoIntersection` | 表示无相交。 | 数值 `0`。 |
| `BoundedIntersection` | 交点在两条有限线段范围内。 | 数值 `1`。 |
| `UnboundedIntersection` | 延长线相交但有限线段范围不同时包含交点。 | 数值 `2`。 |

### 16.4 修改和转换

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `void setP1(const QPointF &p1)` | 设置起点。 | 终点不变。 |
| `void setP2(const QPointF &p2)` | 设置终点。 | 起点不变。 |
| `void setPoints(const QPointF &, const QPointF &)` | 同时设置两个端点。 | 不保持原长度或角度。 |
| `void setLine(qreal, qreal, qreal, qreal)` | 用四个坐标设置两个端点。 | 坐标为浮点。 |
| `QLine toLine() const` | 转为整数线段。 | 端点舍入，可能改变几何结果。 |
| `void translate(const QPointF &offset)` | 就地浮点平移。 | 两端点都改变。 |
| `void translate(qreal dx, qreal dy)` | 就地按分量平移。 | 两端点都改变。 |
| `QLineF translated(const QPointF &offset) const` | 返回平移副本。 | 原对象不变。 |
| `QLineF translated(qreal dx, qreal dy) const` | 返回按分量平移副本。 | 原对象不变。 |

### 16.5 比较、流和兼容 API

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `qFuzzyCompare(const QLineF &, const QLineF &)` | Qt 6.8 起进行线段近似比较。 | 起点、终点和顺序都参与比较。 |
| `qFuzzyIsNull(const QLineF &)` | Qt 6.8 起判断线段是否近似退化。 | 仍是浮点模糊语义。 |
| `operator==(const QLineF &, const QLineF &)` | 比较两个有序线段。 | 业务容差应明确使用模糊比较。 |
| `operator!=(const QLineF &, const QLineF &)` | 判断两个有序线段不等。 | 反向线段不自动相等。 |
| `operator<<(QDataStream &, const QLineF &)` | 写入数据流。 | 受流版本、设置和编译选项影响。 |
| `operator>>(QDataStream &, QLineF &)` | 从数据流读取。 | 读取后检查流状态。 |
| `using IntersectType = IntersectionType` | 旧枚举类型别名。 | 已弃用，新代码使用 `IntersectionType`。 |

## 17. 最后的选型规则

1. 需要小数坐标、长度、角度或精确几何运算时使用 `QLineF`。
2. `QLineF` 表示有限线段，不是无限直线。
3. `angle()`、`angleTo()`、`setAngle()` 和 `fromPolar()` 使用度数。
4. `pointAt(t)` 允许 `t` 超出 `[0, 1]`，业务需要时自行限制参数。
5. `intersects()` 的 `BoundedIntersection` 才表示交点位于两条有限线段内。
6. 空线段没有有效方向，计算单位向量前先处理退化情况。
7. `setLength()` 保持起点不变，只移动终点；零长度线段不执行缩放。
8. `isNull()`、`qFuzzyCompare()` 和 `qFuzzyIsNull()` 都涉及浮点模糊语义。
9. `toLine()` 会舍入端点，可能改变长度、交点和端点关系。
10. `IntersectType` 已弃用，新代码使用 `IntersectionType`。

`QLineF` 的核心价值是把线段从“整数坐标容器”提升为可进行长度、方向、参数化和相交分析的浮点几何值。真正使用时，最重要的是分清有限线段与延长线、角度单位、模糊比较和退化线段这四组边界。
