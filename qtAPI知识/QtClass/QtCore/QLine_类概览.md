# Qt QLine 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QLine>`  
> 所属模块：`Qt6::Core`  
> 形式：值类型，保存两个 `QPoint` 端点  
> 相关类型：`QPoint`、`QLineF`、`QDataStream`

## 1. 先给结论：它解决什么问题

`QLine` 表示二维平面上的**有限线段**，两个端点使用 `int` 坐标：

```text
p1 ---------------- p2
起点                 终点
```

它适合：

- 鼠标拖拽的起点和终点；
- 像素网格、整数坐标绘制；
- 直线段的平移、端点编辑和方向分量计算；
- 在 Qt 绘图 API 中传递整数几何数据；
- 用 `QDataStream` 保存或传输 Qt 几何值。

它不是：

- 无限延伸的数学直线；
- 适合亚像素、旋转和精确几何计算的浮点线段；
- 自动进行裁剪、相交计算或绘制的对象；
- 带方向规范化的向量类型；
- `QLineF` 的别名。

如果计算涉及小数坐标、长度、角度、单位向量或线段相交，应使用 `QLineF`。`QLine` 的核心优势是整数坐标和轻量值语义。

## 2. 最小可用代码

```cpp
#include <QLine>
#include <QPoint>

QLine makeSelectionLine(const QPoint &pressPosition,
                        const QPoint &releasePosition)
{
    return QLine(pressPosition, releasePosition);
}

void inspectLine(const QLine &line)
{
    qDebug() << "start:" << line.p1()
             << "end:" << line.p2()
             << "delta:" << line.dx() << line.dy()
             << "null:" << line.isNull();
}
```

`QLine()` 默认构造的是空线段，两个端点都是 `(0, 0)`。空线段可以正常保存和传递，但不代表具有非零长度或明确方向。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QLine>
```

### 3.3 qmake

```qmake
QT += core
```

如果使用流运算符，还需要：

```cpp
#include <QDataStream>
```

## 4. 端点、方向和线段身份

### 4.1 `p1` 和 `p2` 有方向含义

`QLine` 保存的是有序端点：

```cpp
const QLine forward(QPoint(0, 0), QPoint(10, 5));
const QLine backward(QPoint(10, 5), QPoint(0, 0));
```

二者几何覆盖范围相同，但不是同一个有序线段：

```cpp
Q_ASSERT(forward != backward);
```

因此：

- `p1()` 是起点；
- `p2()` 是终点；
- `dx()` 等于 `x2() - x1()`；
- `dy()` 等于 `y2() - y1()`；
- 相等判断同时比较端点值和端点顺序。

如果业务只关心“无方向的两点集合”，需要自行规范化端点或定义无向比较逻辑。

### 4.2 `isNull()` 的真实含义

```cpp
QLine line(QPoint(4, 7), QPoint(4, 7));
Q_ASSERT(line.isNull());
```

`isNull()` 判断两个端点是否完全相等。它不是一个独立的“长度缓存”或“合法性标志”，也不会检查坐标是否落在某个业务矩形中。

### 4.3 `dx()` 和 `dy()` 是分量，不是长度

```cpp
const QLine line(QPoint(2, 3), QPoint(9, 8));
Q_ASSERT(line.dx() == 7);
Q_ASSERT(line.dy() == 5);
```

如果需要欧氏长度，不能把 `dx()` 或 `dy()` 单独当作长度；可以转换为 `QLineF` 后调用 `length()`，或自行使用平方和计算。

## 5. 整数坐标的边界

### 5.1 坐标范围受 `int` 限制

三个构造函数和 `setLine()` 都使用 `int` 坐标。超出 `int` 可表示范围的值在进入 `QPoint` 之前就已经无法正确表达。

### 5.2 差值可能超出 `int`

`dx()` 和 `dy()` 的返回类型也是 `int`。例如：

```cpp
QLine line(QPoint(std::numeric_limits<int>::min(), 0),
           QPoint(std::numeric_limits<int>::max(), 0));
```

这条线段的数学横向差值超出 `int` 范围。Qt 6.11.1 的 `QPoint` 内部使用 checked integer 表示坐标运算，因此这类差值可能触发断言；不要把端点极值下的 `dx()`/`dy()` 当作任意两个 `int` 相减都安全。

### 5.3 `translate()` 也可能越界

```cpp
QLine line(QPoint(std::numeric_limits<int>::max(), 0),
           QPoint(std::numeric_limits<int>::max(), 0));
line.translate(1, 0);
```

平移会对两个端点分别做整数加法。结果超出 `int` 坐标范围时，Qt 的 checked-int 机制可能触发断言。执行平移前应检查坐标范围，或者使用能表达更大范围的业务类型。

### 5.4 `center()` 特别处理了求和溢出

`center()` 的语义等价于两个端点的平均值，但实现使用更宽的中间类型，因此不会因为直接计算 `p1() + p2()` 的中间和而溢出：

```cpp
const QPoint center = line.center();
```

返回值仍然是整数点，使用整数除法得到中心坐标。它不是浮点中点；需要亚像素中心时应转为 `QLineF`。

## 6. 端点读取与设置

### 6.1 点形式和坐标形式

```cpp
const QPoint start = line.p1();
const QPoint end = line.p2();

const int startX = line.x1();
const int startY = line.y1();
const int endX = line.x2();
const int endY = line.y2();
```

`p1()`/`p2()` 适合整体传递给其他几何 API；`x1()`、`y1()`、`x2()`、`y2()` 适合只取单个坐标。

### 6.2 单点修改和成对修改

```cpp
line.setP1(newStart);
line.setP2(newEnd);
```

如果两个端点需要一起更新，使用：

```cpp
line.setPoints(newStart, newEnd);
```

或者：

```cpp
line.setLine(x1, y1, x2, y2);
```

成对设置可以更直接地表达“替换整个线段”。这些 setter 不会自动保持长度、角度或其他派生约束。

## 7. 平移：修改当前对象还是返回副本

### 7.1 `translate()` 修改当前线段

```cpp
line.translate(QPoint(10, -4));
line.translate(10, -4);
```

两个重载都会同时平移 `p1` 和 `p2`，线段方向和长度保持不变，但端点坐标会发生整数加法。

### 7.2 `translated()` 返回新线段

```cpp
const QLine moved = line.translated(QPoint(10, -4));
```

原来的 `line` 不变：

```cpp
Q_ASSERT(moved.p1() == line.p1() + QPoint(10, -4));
```

选择规则：

| 需求 | API |
| --- | --- |
| 就地修改 | `translate()` |
| 保留原线段并得到平移结果 | `translated()` |
| 偏移量已经是点 | `QPoint` 重载 |
| 偏移量是两个整数 | `int, int` 重载 |

## 8. 与 `QLineF` 的转换

### 8.1 `toLineF()` 保留整数坐标

```cpp
const QLine line(QPoint(1, 2), QPoint(8, 5));
const QLineF floatingLine = line.toLineF();
```

`toLineF()` 从 Qt 6.4 开始提供，返回以浮点精度表示的同一组端点：

```text
(1, 2) -> (8, 5)
```

这个方向不会产生舍入误差，因为整数可以精确转换为常见浮点表示中的对应值。

### 8.2 `QLineF` 转回 `QLine` 可能舍入

```cpp
const QLine rounded = floatingLine.toLine();
```

这是另一方向的语义：`QLineF::toLine()` 会把端点舍入到最近整数。需要保留小数坐标时，不要过早转回 `QLine`。

### 8.3 相等比较和类型转换

Qt 文档将 `QLine` 标记为可与 `QLineF` 进行相等比较。跨类型比较表达的是端点值是否相等；如果 `QLineF` 端点带有小数，不能期待它和整数线段相等。

需要长度、角度、单位向量、法向量或相交判断时，直接使用 `QLineF`：

```cpp
const QLineF precise = line.toLineF();
const qreal length = precise.length();
const qreal angle = precise.angle();
```

## 9. 比较、调试输出和数据流

### 9.1 相等比较

```cpp
const QLine a(QPoint(0, 0), QPoint(4, 4));
const QLine b(QPoint(0, 0), QPoint(4, 4));
const QLine c(QPoint(4, 4), QPoint(0, 0));

Q_ASSERT(a == b);
Q_ASSERT(a != c);
```

线段相等要求：

- 起点相等；
- 终点相等；
- 端点顺序相同。

### 9.2 `QDataStream` 运算符

当 Qt 构建没有定义 `QT_NO_DATASTREAM` 时，`QLine` 提供：

```cpp
QDataStream &operator<<(QDataStream &, const QLine &);
QDataStream &operator>>(QDataStream &, QLine &);
```

使用示例：

```cpp
#include <QBuffer>
#include <QDataStream>

QByteArray bytes;
QDataStream out(&bytes, QIODevice::WriteOnly);
out << line;

QDataStream in(&bytes, QIODevice::ReadOnly);
QLine restored;
in >> restored;
```

流的字节格式还受 `QDataStream` 版本和字节序设置影响。需要长期保存或跨语言互操作时，应明确设置流版本并记录格式契约，不要把默认设置当作永久文件格式。

### 9.3 调试输出

Qt 还为 `QLine` 提供调试流输出，但该声明受 `QT_NO_DEBUG_STREAM` 控制：

```cpp
qDebug() << line;
```

它适合日志和调试，不应作为稳定序列化格式。

## 10. 逐项 API 说明

### 10.1 `QLine()`

```cpp
constexpr QLine();
```

构造空线段。两个端点都是 `(0, 0)`，因此 `isNull()` 返回 `true`。

### 10.2 `QLine(const QPoint &p1, const QPoint &p2)`

```cpp
constexpr QLine(const QPoint &p1, const QPoint &p2);
```

构造起点为 `p1`、终点为 `p2` 的线段。端点顺序会保留，并影响 `dx()`、`dy()` 和相等判断。

### 10.3 `QLine(int x1, int y1, int x2, int y2)`

```cpp
constexpr QLine(int x1, int y1, int x2, int y2);
```

用四个整数坐标构造线段：

```cpp
QLine line(10, 20, 80, 40);
```

它等价于用两个 `QPoint` 构造。

### 10.4 `QPoint p1() const`

```cpp
constexpr QPoint p1() const;
```

返回线段起点的副本。

### 10.5 `QPoint p2() const`

```cpp
constexpr QPoint p2() const;
```

返回线段终点的副本。

### 10.6 `int x1() const`

```cpp
constexpr int x1() const;
```

返回起点的 x 坐标。

### 10.7 `int y1() const`

```cpp
constexpr int y1() const;
```

返回起点的 y 坐标。

### 10.8 `int x2() const`

```cpp
constexpr int x2() const;
```

返回终点的 x 坐标。

### 10.9 `int y2() const`

```cpp
constexpr int y2() const;
```

返回终点的 y 坐标。

### 10.10 `QPoint center() const`

```cpp
constexpr QPoint center() const;
```

返回两个端点的整数中心点。实现使用更宽的中间计算，避免直接相加的中间溢出。

### 10.11 `int dx() const`

```cpp
constexpr int dx() const;
```

返回线段向量的水平分量，即终点 x 坐标减去起点 x 坐标。

如果两个极端坐标的差值超出 `int`，不要依赖结果；Qt 6.11.1 的 checked-int 运算可能触发断言。

### 10.12 `int dy() const`

```cpp
constexpr int dy() const;
```

返回线段向量的垂直分量，即终点 y 坐标减去起点 y 坐标。

### 10.13 `bool isNull() const`

```cpp
constexpr bool isNull() const;
```

如果起点和终点完全相同，返回 `true`；否则返回 `false`。

它只判断端点相等，不判断业务层面的“线段是否有效”。

### 10.14 `void setP1(const QPoint &p1)`

```cpp
void setP1(const QPoint &p1);
```

替换起点，终点保持不变。

### 10.15 `void setP2(const QPoint &p2)`

```cpp
void setP2(const QPoint &p2);
```

替换终点，起点保持不变。

### 10.16 `void setLine(int x1, int y1, int x2, int y2)`

```cpp
void setLine(int x1, int y1, int x2, int y2);
```

用四个坐标同时替换起点和终点。

### 10.17 `void setPoints(const QPoint &p1, const QPoint &p2)`

```cpp
void setPoints(const QPoint &p1, const QPoint &p2);
```

用两个点同时替换起点和终点。

### 10.18 `QLineF toLineF() const`

```cpp
constexpr QLineF toLineF() const noexcept;
```

返回一个浮点精度的 `QLineF` 副本。该函数从 Qt 6.4 开始提供，端点坐标保持相同数值。

### 10.19 `void translate(const QPoint &offset)`

```cpp
constexpr void translate(const QPoint &offset);
```

将起点和终点都加上 `offset`，直接修改当前线段。

### 10.20 `void translate(int dx, int dy)`

```cpp
constexpr void translate(int dx, int dy);
```

按给定的水平和垂直偏移量直接修改当前线段：

```cpp
line.translate(5, -2);
```

### 10.21 `QLine translated(const QPoint &offset) const`

```cpp
constexpr QLine translated(const QPoint &offset) const;
```

返回平移后的新线段，不修改当前对象。

### 10.22 `QLine translated(int dx, int dy) const`

```cpp
constexpr QLine translated(int dx, int dy) const;
```

按两个整数偏移量返回新线段，不修改当前对象。

### 10.23 `bool operator==(const QLine &lhs, const QLine &rhs)`

```cpp
constexpr bool operator==(const QLine &lhs,
                          const QLine &rhs) noexcept;
```

当两个线段的起点、终点和端点顺序都相同时返回 `true`。

### 10.24 `bool operator!=(const QLine &lhs, const QLine &rhs)`

```cpp
constexpr bool operator!=(const QLine &lhs,
                          const QLine &rhs) noexcept;
```

当两个线段不完全相同时返回 `true`。端点顺序不同也属于不相同。

### 10.25 `QDataStream &operator<<(QDataStream &, const QLine &)`

```cpp
QDataStream &operator<<(QDataStream &stream,
                        const QLine &line);
```

把 `line` 写入数据流并返回流引用。可用于连续写入多个 Qt 几何值。

### 10.26 `QDataStream &operator>>(QDataStream &, QLine &)`

```cpp
QDataStream &operator>>(QDataStream &stream,
                        QLine &line);
```

从数据流读出一个线段写入 `line`，并返回流引用。读取后应结合 `stream.status()` 检查流是否发生错误。

## 11. 常见误区与排查顺序

### 11.1 把 `QLine` 当作无限直线

`QLine` 只有从 `p1` 到 `p2` 的有限范围。需要无限直线、射线或相交计算时，使用其他几何算法或 `QLineF`。

### 11.2 忽略端点方向

`QLine(p1, p2)` 和 `QLine(p2, p1)` 几何上覆盖同一段，但相等判断不同，`dx()` 和 `dy()` 的符号也相反。

### 11.3 用 `isNull()` 判断“可参与所有几何计算”

`isNull()` 只判断两个端点是否相同。空线段在业务上是否可用，需要由调用方定义。

### 11.4 对极端坐标直接调用 `dx()` 或平移

端点仍是 `int`，差值和加法可能超出可表示范围。先做范围检查，必要时改用更宽的业务计算类型。

### 11.5 需要浮点精度却一直使用 `QLine`

角度、长度、单位向量和相交位置通常需要 `QLineF`。`QLine` 只适合整数坐标表示。

### 11.6 把 `translated()` 当成就地修改

`translated()` 返回副本；要修改当前对象使用 `translate()`。

### 11.7 过早把 `QLineF` 转回 `QLine`

浮点端点转回整数时会舍入。若后续仍需亚像素信息，应保留 `QLineF`。

### 11.8 把 `QDataStream` 默认格式当作跨版本协议

数据流格式受 `QDataStream` 版本和设置影响。长期文件格式应明确版本、字节序和兼容策略。

## API 速查表
### 12.1 构造和读取

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QLine()` | 构造端点为 `(0, 0)` 的空线段。 | `isNull()` 返回 `true`。 |
| `QLine(const QPoint &, const QPoint &)` | 用两个点构造有序线段。 | `p1`/`p2` 顺序会影响方向和相等判断。 |
| `QLine(int x1, int y1, int x2, int y2)` | 用四个整数坐标构造线段。 | 坐标范围是 `int`。 |
| `QPoint p1() const` | 返回起点。 | 返回值是点副本。 |
| `QPoint p2() const` | 返回终点。 | 返回值是点副本。 |
| `int x1() const` | 返回起点 x 坐标。 | 整数精度。 |
| `int y1() const` | 返回起点 y 坐标。 | 整数精度。 |
| `int x2() const` | 返回终点 x 坐标。 | 整数精度。 |
| `int y2() const` | 返回终点 y 坐标。 | 整数精度。 |
| `int dx() const` | 返回终点到起点的水平分量。 | 差值可能超出 `int`。 |
| `int dy() const` | 返回终点到起点的垂直分量。 | 差值可能超出 `int`。 |
| `QPoint center() const` | 返回整数中心点。 | 中间求和避免溢出，但结果仍是整数。 |
| `bool isNull() const` | 判断两个端点是否相同。 | 不是通用几何有效性检查。 |

### 12.2 修改和变换

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `void setP1(const QPoint &p1)` | 设置起点。 | 终点不变，可能使线段变为空。 |
| `void setP2(const QPoint &p2)` | 设置终点。 | 起点不变，可能使线段变为空。 |
| `void setPoints(const QPoint &, const QPoint &)` | 同时设置两个端点。 | 适合整体替换线段。 |
| `void setLine(int, int, int, int)` | 用坐标同时设置两个端点。 | 坐标必须可由 `int` 表达。 |
| `void translate(const QPoint &offset)` | 就地平移当前线段。 | 两个端点都会加偏移量，可能越界。 |
| `void translate(int dx, int dy)` | 按整数偏移量就地平移。 | 可能触发坐标加法边界。 |
| `QLine translated(const QPoint &offset) const` | 返回平移副本。 | 原对象不变，结果仍是整数坐标。 |
| `QLine translated(int dx, int dy) const` | 按整数偏移量返回副本。 | 可能触发坐标加法边界。 |

### 12.3 精度转换和比较

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QLineF toLineF() const` | 转换为浮点精度线段。 | Qt 6.4 起提供；整数端点不会产生舍入。 |
| `operator==(const QLine &, const QLine &)` | 判断两个有序线段完全相同。 | 端点顺序参与比较。 |
| `operator!=(const QLine &, const QLine &)` | 判断两个有序线段不相同。 | 反向线段通常不相等。 |
| `QLineF::toLine()` | 将浮点线段转为整数线段。 | 端点会舍入到最近整数。 |

### 12.4 流与调试

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `operator<<(QDataStream &, const QLine &)` | 将线段写入数据流。 | 受 `QDataStream` 版本、设置和 `QT_NO_DATASTREAM` 影响。 |
| `operator>>(QDataStream &, QLine &)` | 从数据流读取线段。 | 读取后检查 `QDataStream::status()`。 |
| `operator<<(QDebug, const QLine &)` | 输出调试信息。 | 受 `QT_NO_DEBUG_STREAM` 控制，不是稳定格式。 |

## 13. 一段完整的拖拽选择示例

```cpp
#include <QLine>
#include <QLineF>
#include <QPoint>

class DragSelection
{
public:
    void begin(const QPoint &position)
    {
        start = position;
        current = position;
    }

    void update(const QPoint &position)
    {
        current = position;
    }

    QLine integerLine() const
    {
        return QLine(start, current);
    }

    QLineF preciseLine() const
    {
        return integerLine().toLineF();
    }

    bool movedEnough(int pixels) const
    {
        const QLine line(start, current);
        return line.dx() * line.dx() + line.dy() * line.dy()
            >= pixels * pixels;
    }

private:
    QPoint start;
    QPoint current;
};
```

这个示例中的平方距离适合坐标范围较小的拖拽场景。对接近 `int` 极值的坐标或很大的阈值，不应直接让平方乘法在 `int` 中进行；应改用更宽的整数类型，并先处理乘法溢出边界。

## 14. 最后的选型规则

1. 整数坐标的有限线段使用 `QLine`。
2. 小数坐标、长度、角度、单位向量和相交运算使用 `QLineF`。
3. 把 `p1` 和 `p2` 当作有序端点；反向线段不自动视为相等。
4. `dx()`/`dy()` 是方向分量，不是欧氏长度。
5. 极端整数坐标下，差值和平移可能触发 checked-int 边界，先做范围检查。
6. `center()` 使用更宽的中间计算，但返回的仍是整数点。
7. `translate()` 修改当前对象，`translated()` 返回新对象。
8. `toLineF()` 不舍入；`QLineF::toLine()` 可能舍入。
9. `QDataStream` 适合 Qt 值类型流化，长期协议仍需明确流版本和格式。
10. `isNull()` 只表示两个端点相同，不是业务有效性验证。

`QLine` 的核心价值是用一个轻量值对象表达“有序的整数线段”。理解端点方向、整数边界和与 `QLineF` 的精度分工后，它就能稳定地服务于绘图、拖拽、网格和几何数据传递。
