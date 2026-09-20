# QPointF：用于子像素坐标与二维浮点向量

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPointF>`  
> 模块：`Qt6::Core`  
> 值类型：可拷贝；所有成员函数可重入

## 它解决什么问题

`QPointF` 用两个 `qreal` 分量表示二维浮点坐标。它是 `QPoint` 的子像素版本，适合保存缩放、变换、插值和几何计算的中间结果，避免过早把坐标压回整数像素。

常见场景：

- 高 DPI 绘制、缩放视图与坐标变换；
- 拖动、动画、插值和速度向量；
- 几何运算、命中测试前的连续坐标；
- 在 `QPoint`、`QRectF`、`QLineF` 与绘制 API 间传递位置。

`QPointF` 是纯值类型，不需要事件循环或对象所有权管理。它要求坐标和参与缩放的因子是有限浮点数；不要把 `NaN` 或无穷值作为“缺失坐标”哨兵。

## 与 QPoint 的选择和转换

```cpp
const QPoint pixel(10, 21);
QPointF scenePos = pixel;          // 整数精确转换为浮点

scenePos *= 1.25;                  // 中间过程保持小数
const QPoint drawPos = scenePos.toPoint(); // 最近整数舍入
```

`QPointF(const QPoint &) ` 和 `QPoint::toPointF()`（Qt 6.4 起）不会丢失整数信息。反向的 `toPoint()` 会把两个分量舍入到最近整数，因此应只在需要落到像素或整数网格边界时调用。

## 向量操作与距离近似

与 `QPoint` 一样，它支持分量加减、负号、乘除、点积和转置：

```cpp
const QPointF start(4.5, 8.0);
const QPointF end(13.0, 12.5);
const QPointF delta = end - start;

if (delta.manhattanLength() > 6.0)
    startDrag();
```

`manhattanLength()` 返回 `abs(x) + abs(y)`，适合低成本阈值判断，不是欧氏长度。`dotProduct()` 计算向量点积，可用于投影或方向判断。若需要模长，显式使用 `std::hypot(x(), y())`，避免手写平方和造成额外溢出或精度问题。

`operator/=` 和非成员 `/` 的除数不能为零或 `NaN`。乘法因子应是有限数。对于来自外部输入的变换参数，先验证再运算。

## 浮点比较：最容易误解的语义

Qt 6.11.1 中 `QPointF` 的 `operator==` 和 `operator!=` 使用模糊比较，不是严格逐位相等。Qt 6.8 起还提供了显式的：

- `qFuzzyCompare(p1, p2)`：两点是否近似相等；
- `qFuzzyIsNull(point)`：是否近似为 `(0, 0)`。

```cpp
const QPointF expected(10.0, 20.0);
const QPointF actual(10.0 + 1e-14, 20.0);

if (qFuzzyCompare(expected, actual)) {
    // 浮点计算后的近似匹配
}
```

这很适合几何结果判断，却不适合把 `QPointF` 当作精确键、二进制协议标识或严格测试断言。需要严格分量比较时，直接比较 `x()`/`y()`，并自行定义容差策略；该策略必须符合业务尺度，不能盲目套用一个固定 epsilon。

`isNull()` 只判断两个坐标是否为 `0.0`，并忽略零的符号；它不是模糊判断。对计算结果是否“足够接近原点”，使用 `qFuzzyIsNull()`。

## 修改分量的方式

```cpp
QPointF point(1.25, 2.5);
point.setX(3.0);
point.ry() += 0.5;
```

`setX()`、`setY()` 的输入必须为有限浮点数。`rx()`、`ry()` 返回 `qreal &`，因此可以直改分量，但也会绕开可读性更好的 setter；更重要的是，不要经引用写入 `NaN` 或无穷值，也不要让引用超过对象寿命。

`transposed()` 返回 `(y, x)` 的新对象，不修改原对象。

## 序列化与平台桥接

`QDataStream` 的 `<<` 和 `>>` 支持二进制读写。持久化或网络协议中应设置双方一致的流版本、字节序，并检查读取失败状态；浮点值本身还要考虑精度、平台和协议兼容性。

在 Apple 平台且 Core Graphics 可用时，`fromCGPoint()` 与 `toCGPoint()` 可在 `QPointF` 和 `CGPoint` 间桥接。它们属于平台边界代码，不宜出现在跨平台核心接口。

## 常见错误

### 将 `operator==` 当成严格相等

`QPointF` 的等号是模糊比较。测试精确序列化、坐标缓存命中或需要传递性比较的算法时，明确改为分量严格比较或自行定义一致的比较器。

### 用 `isNull()` 判断“接近零”

`isNull()` 只认精确的零。浮点运算后的微小残差需要 `qFuzzyIsNull()`（Qt 6.8 起）或业务容差。

### 把浮点点过早转换为 QPoint

每次 `toPoint()` 都会舍入。连续缩放、动画或拖动计算应保持 `QPointF`，只在显示或整数 API 边界转换一次。

## API 速查表

| API | 作用 | 语义与边界 |
| --- | --- | --- |
| `QPointF()` | 构造 `(0.0, 0.0)` | 是有效原点，不是缺失值。 |
| `QPointF(const QPoint &)` | 从整数点精确转换 | 不引入小数或舍入。 |
| `QPointF(qreal x, qreal y)` | 构造浮点坐标 | 坐标应为有限数。 |
| `x()`, `y()` | 读取分量 | 返回 `qreal`。 |
| `setX(qreal)`, `setY(qreal)` | 设置分量 | 参数必须有限；外部输入先校验。 |
| `rx()`, `ry()` | 返回分量引用 | 返回 `qreal &`；可直接修改，但不要写入非有限值。 |
| `isNull()` | 判断是否精确为原点 | 忽略 `-0.0` 符号；不是模糊比较。 |
| `qFuzzyIsNull(point)` | 判断是否近似原点 | Qt 6.8 起；适合浮点计算结果。 |
| `qFuzzyCompare(p1, p2)` | 判断两点近似相等 | Qt 6.8 起；不要替代严格身份比较。 |
| `manhattanLength()` | 返回 `abs(x)+abs(y)` | 快速近似长度，不是欧氏距离。 |
| `dotProduct(p1, p2)` | 计算点积 | 用于方向或投影；结果为 `qreal`。 |
| `toPoint()` | 转为整数点 | 分量舍入到最近整数，可能丢失信息。 |
| `transposed()` | 交换 x/y | 返回新值。 |
| `operator+=`, `operator-=` | 原地平移 | 分量相加/相减，返回自身引用。 |
| `operator*=`, `operator/=` | 原地缩放 | 因子必须有限；除数不能为零或 `NaN`。 |
| `+`, `-`, 一元 `-`, `*`, `/` | 返回算术结果 | 不修改操作数；对非有限输入不要依赖几何语义。 |
| `operator==`, `operator!=` | 比较点 | 使用模糊比较，不是严格分量相等。 |
| `QDataStream << / >>` | 二进制流读写 | 需要约定流版本并检查错误。 |
| `fromCGPoint()`, `toCGPoint()` | Core Graphics 互转 | Apple 平台相关。 |

## 选择建议

| 需求 | 建议 |
| --- | --- |
| 像素或整数格点 | `QPoint` |
| 连续坐标和几何计算 | `QPointF` |
| 近似几何比较 | `qFuzzyCompare()` 或按业务尺度定义容差 |
| 严格相等或精确键语义 | 直接比较分量，并避免依赖 `QPointF::operator==` |

一句话记忆：`QPointF` 保存连续坐标，转换成 `QPoint` 才舍入；它的等号是模糊比较，精确身份判断必须自己说清楚。
