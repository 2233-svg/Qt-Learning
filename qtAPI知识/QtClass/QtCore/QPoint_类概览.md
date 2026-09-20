# QPoint：整数坐标与二维位移向量

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPoint>`  
> 模块：`Qt6::Core`  
> 值类型：可拷贝、无 QObject 生命周期；所有成员函数可重入

## 它解决什么问题

`QPoint` 用两个 `int` 表示平面上的一个整数坐标 `(x, y)`。在 Qt 中它既表示像素位置，也常被当作二维整数向量：两个点相减得到位移，点与点相加得到平移后的坐标。

实际使用场景：

- 鼠标、触摸和窗口部件的像素坐标；
- 拖动距离、滚动偏移和网格中的整数单元位置；
- 用 `manhattanLength()` 做低成本的拖动阈值判断；
- 在 `QRect`、`QSize`、绘制和事件 API 之间传递位置。

它没有所有权、线程归属或事件循环要求，是轻量值类型。不同线程各自操作不同的 `QPoint` 副本是安全的；同一对象仍遵守普通 C++ 并发读写规则。

```cpp
#include <QPoint>

const QPoint topLeft(12, 24);
const QPoint dragOffset = QPoint(40, 32) - topLeft; // (28, 8)
```

## 选择 QPoint 还是 QPointF

| 情况 | 使用 |
| --- | --- |
| 像素、索引、格点和本就为整数的坐标 | `QPoint` |
| 缩放、变换、插值、物理计算或子像素位置 | `QPointF` |
| 已有 `QPoint`，只是要交给浮点 API | `toPointF()`（Qt 6.4 起） |
| 需要把浮点结果落到像素格点 | `QPointF::toPoint()`，明确接受四舍五入 |

对 `QPoint` 乘以或除以浮点数时，结果会舍入到最近整数。动画、缩放或累积计算若每一步都使用 `QPoint`，舍入误差会累积；中间过程应使用 `QPointF`，最后再转换。

## 常用模型：位置、位移与拖动阈值

```cpp
QPoint pressPos;

void Editor::mousePressEvent(QMouseEvent *event)
{
    pressPos = event->pos();
}

void Editor::mouseMoveEvent(QMouseEvent *event)
{
    const QPoint delta = event->pos() - pressPos;
    if (delta.manhattanLength() >= 8)
        beginDrag();
}
```

`manhattanLength()` 返回 `abs(x) + abs(y)`。它不是欧氏距离，却不用平方根，常用于“是否移动得足够远”的阈值判断。若算法需要真实长度，应显式计算浮点欧氏距离。

## 构造、访问与修改

默认构造产生空点 `(0, 0)`，`isNull()` 也只表示这两个分量均为零，不表示“未初始化”“无效坐标”或“在屏幕外”。

```cpp
QPoint p(10, 20);
p.setX(12);
p.ry() += 5;             // p 现在为 (12, 25)
```

`setX()` / `setY()` 是清晰的赋值接口。`rx()` / `ry()` 返回分量的非常量引用，适合需要与接受 `int &` 的旧接口协作或做简短原地操作；不要将该引用保存得比 `QPoint` 本身更久。

## 算术语义与边界

`+`、`-`、一元负号以及复合赋值按分量运算。`dotProduct(p1, p2)` 计算 `p1.x()*p2.x() + p1.y()*p2.y()`，可用来判断向量夹角趋势或投影关系，但它返回 `int`。

```cpp
const QPoint velocity(3, 7);
const QPoint direction(-1, 4);
const int projectionNumerator = QPoint::dotProduct(velocity, direction); // 25
```

`QPoint` 的分量和点积都是 `int`。非常大的坐标、相乘或相加可能超出 `int` 可表示范围；不要把它用作大世界坐标或未受限的累计量。除法的除数必须非零；浮点乘除还会舍入，需精度时改用 `QPointF`。

`transposed()` 返回交换横纵坐标的新点，可用于旋转坐标语义或在行列坐标与 x/y 坐标之间转换：

```cpp
const QPoint cell(4, 9);
const QPoint swapped = cell.transposed(); // (9, 4)
```

## 比较、序列化和平台桥接

相等比较比较两个分量。`QPoint` 可以与 `QPointF` 比较，但跨整数/浮点域时应避免把这类比较当作容差判断；需处理浮点误差时，在 `QPointF` 域使用 `qFuzzyCompare()`。

`QDataStream` 的 `<<` / `>>` 可读写点。流格式会受 `QDataStream` 版本、字节序和事务错误处理影响；跨版本或跨设备持久化时，显式设置流版本并检查状态。

在支持 Core Graphics 的 Apple 平台，`toCGPoint()` 可桥接到 `CGPoint`；其可用性取决于平台头文件和构建目标。跨平台核心逻辑不要把 `CGPoint` 放入公共接口。

## 常见误区

### 把 `(0, 0)` 当作“没有坐标”

原点可能是完全有效的位置。若业务需要可选坐标，应使用额外状态、`std::optional<QPoint>` 或明确的有效性标记。

### 用整数点做连续缩放

```cpp
QPoint p(1, 1);
p *= 0.5; // 舍入，信息已经丢失
```

中间计算使用 `QPointF`，只在渲染或命中测试边界转换为 `QPoint`。

### 假定 manhattanLength 是几何长度

它是曼哈顿长度。对斜向移动，它和 `sqrt(x*x + y*y)` 不同；它适合近似阈值和轴对齐网格，不适合精确半径判断。

## API 速查表

| API | 作用 | 语义与边界 |
| --- | --- | --- |
| `QPoint()` | 构造 `(0, 0)` | `isNull()` 随即为真；不是无效值标记。 |
| `QPoint(int x, int y)` | 构造整数坐标 | 用于像素和整数格点。 |
| `x()`, `y()` | 读取分量 | 返回 `int` 值。 |
| `setX(int)`, `setY(int)` | 设置分量 | 明确、可读的原地修改方式。 |
| `rx()`, `ry()` | 取得分量引用 | 返回 `int &`；引用仅在对象存活且未移动时有效。 |
| `isNull()` | 判断是否为原点 | 仅判断 `(0, 0)`，不验证业务有效性。 |
| `manhattanLength()` | 计算 `abs(x)+abs(y)` | 快速近似长度；不是欧氏距离，极值计算应防整数溢出。 |
| `dotProduct(p1, p2)` | 计算点积 | 返回 `int`；大分量相乘可能超范围。 |
| `transposed()` | 交换 x/y | 返回新值，不修改原点。 |
| `toPointF()` | 转为 `QPointF` | Qt 6.4 起；整数到浮点无舍入损失。 |
| `toCGPoint()` | 转为 Apple `CGPoint` | 平台相关；不要作为跨平台 API 依赖。 |
| `operator+=`, `operator-=` | 原地平移 | 按分量加减，返回自身引用。 |
| `operator*=`, `operator/=` | 原地缩放 | `float`/`double` 结果舍入到整数；除数不能为零。 |
| `+`, `-`, 一元 `-` | 返回算术结果 | 不修改操作数，按分量计算。 |
| `operator*`, `operator/` | 返回缩放后的点 | 浮点缩放会舍入；精度敏感时使用 `QPointF`。 |
| `operator==`, `operator!=` | 比较两个点 | 同类型比较基于分量；浮点容差请使用 `QPointF` 的模糊比较。 |
| `QDataStream << / >>` | 二进制流读写 | 处理流状态并固定协议所需的流版本。 |

一句话记忆：`QPoint` 是整数位置也是整数向量；它快速、无状态，但一旦进行浮点缩放就会发生舍入。
