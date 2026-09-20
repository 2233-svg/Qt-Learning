# Qt QMarginsF 浮点边距值类型深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMarginsF>`  
> 所属模块：`Qt6::Core`  
> 类型性质：保存 left/top/right/bottom 四个浮点边距的轻量值类型  
> 相关类型：`QMargins`、`QRectF`、`QSizeF`、`QLayout`、`QDataStream`

## 1. 它解决什么问题

`QMarginsF` 用四个 `qreal` 值表示矩形四条边需要预留的空间：

```text
        top
   +------------+
left|   内容     |right
   +------------+
       bottom
```

它和 `QMargins` 的分工相同，但保留小数，因此适合：

- 设备像素比、缩放变换和高 DPI 布局；
- `QRectF`、`QPainter` 等浮点几何计算；
- 需要亚像素间距的绘制或排版；
- 先用浮点值组合边距，最后才转换为整数像素；
- 在动画、插值或比例计算中避免过早丢失小数。

`QMarginsF` 不是：

- 带位置和尺寸的矩形，矩形应使用 `QRectF`；
- 自动应用到布局或绘制设备的控制器；
- 自动限制为非负的 CSS padding；
- 精确判断浮点相等的结构。它的 `isNull()`、`qFuzzyCompare()` 和 `operator==` 使用浮点模糊比较语义。

## 2. 实际使用场景

### 2.1 按设备缩放逻辑边距

```cpp
const QMarginsF logicalMargins(8.0, 4.0, 8.0, 4.0);
const qreal scale = devicePixelRatio;
const QMarginsF deviceMargins = logicalMargins * scale;
```

保留 `QMarginsF` 可以让中间计算不被整数取整打断。只有在目标 API 只接受 `QMargins` 时，才调用 `toMargins()`。

### 2.2 给浮点矩形增加或移除边距

```cpp
const QRectF contentRect =
    outerRect.marginsRemoved(QMarginsF(12.5, 8.0, 12.5, 8.0));
```

`QMarginsF` 只描述四边偏移，真正改变矩形的是 `QRectF` 的几何 API。若边距总和大于矩形尺寸，结果是否退化由 `QRectF` 的语义决定，`QMarginsF` 本身不会替调用方检查。

### 2.3 合并两层浮点边距

```cpp
const QMarginsF frame(1.5, 1.0, 1.5, 1.0);
const QMarginsF content(8.0, 4.0, 8.0, 4.0);
const QMarginsF total = frame + content;
```

`operator+` 对四个分量分别相加，不会把 left/right 或 top/bottom 自动合并成统一值。

### 2.4 合并“至少需要这么大”的约束

```cpp
const QMarginsF styleMargins(4.0, 6.0, 4.0, 6.0);
const QMarginsF platformMargins(8.0, 4.0, 8.0, 4.0);
const QMarginsF effective = styleMargins | platformMargins;
```

`operator|` 对每一边取较大值，适合合并独立的最小安全约束。它不是浮点位或、边距相加，也不是矩形联合。

### 2.5 最后一步转换为整数像素

```cpp
const QMargins pixelMargins =
    (logicalMargins * devicePixelRatio).toMargins();
```

`toMargins()` 会对每一边取整并饱和到 `int` 范围。它不是无损转换；如果业务要求明确的向下取整、向上取整或特定舍入规则，应在业务层先处理。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QMarginsF>
#include <QRectF>
#include <QDebug>
```

需要 `QMargins` 转换时，Qt 头文件会提供相应声明；实际项目仍应为直接使用的相关类型包含其公开头文件。

## 4. 数据模型和基本语义

### 4.1 四个分量的顺序固定

| 分量 | 方向 | 通常表示 |
| --- | --- | --- |
| `left` | 左 | 内容区域从左边向内预留的距离 |
| `top` | 上 | 内容区域从上边向内预留的距离 |
| `right` | 右 | 内容区域从右边向内预留的距离 |
| `bottom` | 下 | 内容区域从下边向内预留的距离 |

构造函数的参数顺序始终是：

```cpp
QMarginsF(left, top, right, bottom);
```

它不是 `(x, y, width, height)`，也不是 `(horizontal, vertical)`。

### 4.2 允许负值

```cpp
const QMarginsF overlap(-2.0, 0.0, -2.0, 0.0);
```

构造函数和 setter 不会把负值钳制为零。负边距可以在几何算法中表达向外扩展，但布局、绘制或平台 API 可能有自己的约束。是否允许负值必须在业务边界验证。

### 4.3 浮点值可能带有 NaN 或无穷

`QMarginsF` 是一个轻量值类型，不负责把外部输入清洗成有限数。来自文件、用户输入、动画计算或除法的值应在进入几何 API 前检查：

```cpp
const bool finite =
    std::isfinite(margins.left()) &&
    std::isfinite(margins.top()) &&
    std::isfinite(margins.right()) &&
    std::isfinite(margins.bottom());
```

使用 `std::isfinite` 需要包含 `<cmath>`。NaN 会使比较、`isNull()` 和几何结果难以解释；无穷值也不适合转换成普通像素边距。

### 4.4 `qreal` 是 Qt 的浮点别名

`qreal` 的具体基础类型由 Qt 平台配置决定。代码应使用 `qreal` 的 API 签名，而不要在公共接口中武断地假设它永远是 `float` 或 `double`。

## 5. 值语义、constexpr 和 tuple 协议

### 5.1 它是轻量值类型

```cpp
QMarginsF margins(4.5, 8.0, 4.5, 8.0);
QMarginsF copy = margins;
copy.setTop(12.25);
```

修改 `copy` 不会修改 `margins`。它不具有 QObject 的父子关系、信号槽或所有权语义。

### 5.2 基本操作支持 `constexpr`

构造、读取、setter、算术和许多比较操作在 Qt 6.11.1 头文件中标记为 `constexpr`。这允许满足条件的常量表达式在编译期计算：

```cpp
constexpr QMarginsF defaultMargins(8.0, 6.0, 8.0, 6.0);
static_assert(defaultMargins.left() == 8.0);
```

`constexpr` 不会取消运行时边界：除法仍不能使用零，浮点输入也不应无条件接受 NaN 或无穷。

### 5.3 支持结构化绑定

Qt 6.11.1 为 `QMarginsF` 提供四元素 tuple 协议，顺序是 left、top、right、bottom：

```cpp
const QMarginsF margins(1.5, 2.0, 3.5, 4.0);
const auto [left, top, right, bottom] = margins;
```

四个元素的类型都是 `qreal`。结构化绑定适合一次读取全部分量；需要表达方向语义时，直接写 `margins.left()` 等命名 API 往往更清楚。

## 6. 浮点比较和“零”的边界

### 6.1 `isNull()` 是逐边模糊零判断

```cpp
const QMarginsF almostZero(1e-12, 0.0, -1e-12, 0.0);
```

`isNull()` 会对四个分量分别调用浮点模糊零判断，只有四边都被认为接近零时才返回 `true`。它不是检查四边的精确 bit 表示，也不是检查四边总和。

这意味着：

- 很小的非零值可能被视为 null；
- 负的很小值也可能被视为 null；
- 一个明显非零的分量会使整体返回 `false`；
- NaN 不应被当作零，通常会使判断失败。

### 6.2 `qFuzzyIsNull(const QMarginsF &)`

`qFuzzyIsNull(margins)` 是与 `isNull()` 对应的非成员形式，逐边检查模糊零。它适合在泛型代码或已有 Qt 浮点比较工具链中使用。

```cpp
if (qFuzzyIsNull(margins))
    useDefaultMargins();
```

不要用 `isNull()` 或 `qFuzzyIsNull()` 检查“所有边距非负”；非负是另一条业务条件。

### 6.3 `qFuzzyCompare(const QMarginsF &, const QMarginsF &)`

`qFuzzyCompare` 对四个对应分量逐一进行 Qt 浮点模糊比较：

```cpp
if (qFuzzyCompare(actual, expected))
    acceptLayout();
```

它适合比较经过浮点计算的几何值，不能替代“允许误差是固定业务值”的比较。如果业务明确要求最大绝对误差或相对误差，应在业务层写出那个规则。

### 6.4 `operator==` 和 `operator!=`

`QMarginsF` 的相等比较使用同一套模糊比较语义，而不是简单逐字段精确 `==`。因此两个数值略有差异的边距可能被 `operator==` 判定为相等。

```cpp
if (actual == expected) {
    // 按 QMarginsF 的 fuzzy equality 语义判断
}
```

如果需要严格的 IEEE 浮点逐值比较，必须显式比较四个分量，并自行决定如何处理 `-0.0`、NaN 和无穷。

### 6.5 与 `QMargins` 的比较

Qt 还提供 `QMarginsF` 与 `QMargins` 的可比较语义。比较前可以理解为把整数边距提升为 `QMarginsF`，再按浮点相等规则判断：

```cpp
const QMarginsF floating(8.0, 4.0, 8.0, 4.0);
const QMargins integer(8, 4, 8, 4);
Q_ASSERT(floating == integer);
```

这不表示任意带小数的 `QMarginsF` 都能无损还原成 `QMargins`。

## 7. 逐项成员 API

### 7.1 `QMarginsF()`

```cpp
constexpr QMarginsF() noexcept;
```

构造四边都为 `0` 的边距：

```cpp
const QMarginsF margins;
Q_ASSERT(margins.isNull());
```

它表示没有额外边距，不代表未初始化，也不读取布局或平台默认值。

### 7.2 `QMarginsF(qreal left, qreal top, qreal right, qreal bottom)`

```cpp
constexpr QMarginsF(qreal left, qreal top,
                   qreal right, qreal bottom) noexcept;
```

按 left、top、right、bottom 顺序保存四个值：

```cpp
const QMarginsF margins(12.5, 8.0, 12.5, 10.25);
```

构造函数不负责检查负数、NaN、无穷或是否适合某个矩形。

### 7.3 `QMarginsF(const QMargins &margins)`

```cpp
constexpr QMarginsF(const QMargins &margins) noexcept;
```

把 `QMargins` 的四个整数逐项提升为 `qreal`：

```cpp
const QMargins integerMargins(3, 5, 3, 5);
const QMarginsF floatingMargins(integerMargins);
```

整数到 `qreal` 的转换不会凭空产生小数，也不会改变正负号。

### 7.4 `isNull() const`

```cpp
constexpr bool isNull() const noexcept;
```

当四个分量都通过 Qt 的模糊零判断时返回 `true`。它和 `QMargins::isNull()` 的关键差别是：整数版本要求精确为零，浮点版本允许足够接近零的值。

### 7.5 `left() const`

```cpp
constexpr qreal left() const noexcept;
```

返回左边距值副本。它不返回可写引用，也不会修改任何布局对象。

### 7.6 `top() const`

```cpp
constexpr qreal top() const noexcept;
```

返回上边距值副本。这里的 `top` 是边距方向，不是 `QRectF` 的 top 坐标。

### 7.7 `right() const`

```cpp
constexpr qreal right() const noexcept;
```

返回右边距值副本。

### 7.8 `bottom() const`

```cpp
constexpr qreal bottom() const noexcept;
```

返回下边距值副本。

### 7.9 `setLeft(qreal)`

```cpp
constexpr void setLeft(qreal left) noexcept;
```

替换左边距：

```cpp
margins.setLeft(margins.left() + 2.5);
```

它只修改当前 `QMarginsF` 值，不会自动刷新使用该值的布局或矩形。

### 7.10 `setTop(qreal)`

```cpp
constexpr void setTop(qreal top) noexcept;
```

替换上边距。调用方应自行决定是否允许负值或非有限值。

### 7.11 `setRight(qreal)`

```cpp
constexpr void setRight(qreal right) noexcept;
```

替换右边距。setter 不执行业务层的非负约束。

### 7.12 `setBottom(qreal)`

```cpp
constexpr void setBottom(qreal bottom) noexcept;
```

替换下边距。

### 7.13 `toMargins() const`

```cpp
constexpr QMargins toMargins() const noexcept;
```

把每个浮点边距分别转换为整数边距。Qt 通过 `qSaturateRound` 进行取整并饱和：

- 结果会进行舍入，不应理解为简单截断；
- 超出 `int` 范围的有限结果会饱和到可表示范围；
- 负值仍然可以转换为负整数；
- NaN、无穷等非有限输入不适合依赖转换结果，应在调用前验证。

```cpp
const QMarginsF logical(1.4, 2.5, 3.6, 4.9);
const QMargins pixels = logical.toMargins();
```

如果业务需要 `floor`、`ceil` 或明确的误差预算，应在转换前逐项执行自己的舍入策略。

### 7.14 `operator+=(const QMarginsF &)`

```cpp
constexpr QMarginsF &operator+=(const QMarginsF &margins) noexcept;
```

四边逐项相加并修改当前对象：

```cpp
total += contentMargins;
```

它是边距数值运算，不是把某个 `QRectF` 自动扩大。

### 7.15 `operator-=(const QMarginsF &)`

```cpp
constexpr QMarginsF &operator-=(const QMarginsF &margins) noexcept;
```

四边逐项相减。结果可以为负，是否有业务意义由调用方决定。

### 7.16 `operator+=(qreal)`

```cpp
constexpr QMarginsF &operator+=(qreal addend) noexcept;
```

给四个分量都加上同一个浮点数：

```cpp
margins += 2.0;
```

它不是只增加水平边距或垂直边距；四边都会改变。

### 7.17 `operator-=(qreal)`

```cpp
constexpr QMarginsF &operator-=(qreal subtrahend) noexcept;
```

给四个分量都减去同一个浮点数。传入负数会产生反向效果。

### 7.18 `operator*=(qreal)`

```cpp
constexpr QMarginsF &operator*=(qreal factor) noexcept;
```

四边分别乘以因子：

```cpp
margins *= devicePixelRatio;
```

因子为负数在数学上是允许的，但通常不符合“空间边距”的业务含义。NaN 或无穷因子可能把所有分量传播为不可用值，应在边界处检查。

### 7.19 `operator/=(qreal)`

```cpp
constexpr QMarginsF &operator/=(qreal divisor);
```

四边分别除以除数。除数必须是非零且非 NaN 的浮点值；Qt 头文件中的断言条件要求 `divisor < 0 || divisor > 0`。

```cpp
Q_ASSERT(scale > 0.0);
margins /= scale;
```

发布构建不应把断言当作输入验证机制，外部或计算得到的除数仍应在调用前显式检查。

## 8. 非成员算术和组合 API

### 8.1 `operator+(m1, m2)`

```cpp
QMarginsF operator+(const QMarginsF &m1,
                    const QMarginsF &m2) noexcept;
```

返回两个边距逐边相加的结果，不修改输入对象。

### 8.2 `operator-(m1, m2)`

```cpp
QMarginsF operator-(const QMarginsF &m1,
                    const QMarginsF &m2) noexcept;
```

返回逐边相减的结果，不执行矩形几何移除。

### 8.3 `operator+(margins, qreal)` 和 `operator+(qreal, margins)`

```cpp
QMarginsF operator+(const QMarginsF &margins, qreal addend) noexcept;
QMarginsF operator+(qreal addend, const QMarginsF &margins) noexcept;
```

给四个分量都加同一个浮点数。两种参数顺序语义相同：

```cpp
const QMarginsF expanded = margins + 2.0;
const QMarginsF same = 2.0 + margins;
```

### 8.4 `operator-(margins, qreal)`

```cpp
QMarginsF operator-(const QMarginsF &margins,
                    qreal subtrahend) noexcept;
```

给四个分量都减同一个浮点数。

### 8.5 `operator*(margins, qreal)` 和 `operator*(qreal, margins)`

```cpp
QMarginsF operator*(const QMarginsF &margins, qreal factor) noexcept;
QMarginsF operator*(qreal factor, const QMarginsF &margins) noexcept;
```

逐边做浮点乘法：

```cpp
const QMarginsF scaled = margins * scale;
```

结果仍是 `QMarginsF`，不会在此处取整或饱和到 `int`；需要整数结果时再调用 `toMargins()`。

### 8.6 `operator/(margins, qreal)`

```cpp
QMarginsF operator/(const QMarginsF &margins,
                    qreal divisor);
```

逐边做浮点除法。除数必须非零且不能是 NaN；Qt 在实现中通过断言检查其正负关系。

### 8.7 `operator|(m1, m2)`

```cpp
QMarginsF operator|(const QMarginsF &m1,
                    const QMarginsF &m2) noexcept;
```

每一边取 `qMax`：

```cpp
const QMarginsF effective = style | platform;
```

它表达“每一边至少满足两个约束中的较大者”。如果你的需求是叠加两层包裹空间，应使用 `operator+`，不要使用 `|`。

### 8.8 一元 `operator+(margins)`

```cpp
QMarginsF operator+(const QMarginsF &margins) noexcept;
```

返回相同值的副本，不改变任何分量。它主要用于保持算术表达式的一致性，日常代码通常不需要显式写出。

### 8.9 一元 `operator-(margins)`

```cpp
QMarginsF operator-(const QMarginsF &margins) noexcept;
```

将四个分量分别取负：

```cpp
const QMarginsF inverted = -margins;
```

这不是交换 left/right 或 top/bottom，也不是矩形镜像。若输入包含无穷或 NaN，结果仍会传播相应的非有限值。

## 9. 比较、流和调试输出

### 9.1 `qFuzzyCompare`

```cpp
bool qFuzzyCompare(const QMarginsF &lhs,
                   const QMarginsF &rhs) noexcept;
```

逐边进行 Qt 浮点模糊比较。它适合判断几何计算是否足够接近，不能表达固定的业务绝对误差。

### 9.2 `qFuzzyIsNull`

```cpp
bool qFuzzyIsNull(const QMarginsF &margins) noexcept;
```

逐边判断是否接近零，与 `margins.isNull()` 的判断目标一致。

### 9.3 `operator==` 和 `operator!=`

```cpp
bool operator==(const QMarginsF &lhs,
                const QMarginsF &rhs) noexcept;
bool operator!=(const QMarginsF &lhs,
                const QMarginsF &rhs) noexcept;
```

相等比较采用 `qFuzzyCompare` 语义，而不是简单的四次精确 `==`。因此把 `QMarginsF` 用作需要严格 bit-level 区分浮点值的键时要谨慎；它更适合作为几何值使用。

Qt 还支持与 `QMargins` 的可比较形式，整数边距会按浮点值参与比较。

### 9.4 `QDataStream &operator<<`

```cpp
QDataStream &operator<<(QDataStream &out,
                        const QMarginsF &margins);
```

把四个浮点边距写入 Qt 数据流。适合 Qt 两端都约定了 `QDataStream` 版本的持久化或 IPC。

使用时应同时考虑：

- 明确设置并约定 `QDataStream::Version`；
- 读取端检查流状态；
- 对不可信数据限制大小和来源；
- 不要把 `QDebug` 文本当作替代协议；
- 跨语言或长期存档时，应明确浮点格式、字节序和版本兼容策略。

### 9.5 `QDataStream &operator>>`

```cpp
QDataStream &operator>>(QDataStream &in,
                        QMarginsF &margins);
```

从 Qt 数据流读回四个浮点边距。读取完成后仍应检查 `QDataStream::status()`，因为目标对象被写入不代表输入完整、可信或来自兼容版本。

### 9.6 `QDebug operator<<`

```cpp
QDebug operator<<(QDebug debug,
                  const QMarginsF &margins);
```

支持：

```cpp
qDebug() << margins;
```

输出格式服务于诊断，不是稳定的序列化格式，也不应被业务代码解析。

## 10. 与 `QMargins` 的转换边界

### 10.1 `QMargins` 到 `QMarginsF` 是整数提升

以下两种写法都保留整数值：

```cpp
const QMargins integerMargins(3, 5, 3, 5);
const QMarginsF a(integerMargins);
const QMarginsF b = integerMargins.toMarginsF();
```

转换不会恢复原本不存在的小数，也不会执行额外取整。

### 10.2 `QMarginsF` 到 `QMargins` 会取整和饱和

```cpp
const QMarginsF floatingMargins(1.4, 2.5, 3.6, 4.9);
const QMargins integerMargins = floatingMargins.toMargins();
```

每一边独立处理。结果不能当作“精确逆转换”；浮点中间值、舍入规则和 `int` 范围都会影响最终像素值。

### 10.3 不要过早转换

```cpp
const QMarginsF total =
    QMarginsF(1.25, 1.25, 1.25, 1.25) +
    QMarginsF(0.75, 0.75, 0.75, 0.75);
const QMargins pixels = total.toMargins();
```

如果分别把两个边距先转成 `QMargins` 再相加，可能得到与最后统一转换不同的结果。涉及缩放或多层组合时，通常应保留浮点值到最后一步。

## 11. 与矩形、布局和绘制 API 的边界

### 11.1 `QMarginsF` 不会自动改变矩形

```cpp
const QRectF content = outer.marginsRemoved(margins);
```

只有把它传给 `QRectF` 或其他接受边距的 API，才会发生几何变化。修改一个局部 `QMarginsF` 不会回写原来的矩形或布局。

### 11.2 边距总和可能超过矩形尺寸

当 left + right 大于矩形宽度，或 top + bottom 大于矩形高度时，内容矩形可能退化或出现调用方不期望的几何结果。`QMarginsF` 不会阻止这种状态：

```cpp
const bool fits =
    margins.left() + margins.right() <= rect.width() &&
    margins.top() + margins.bottom() <= rect.height();
```

对外部输入还应先检查有限性，避免 NaN 使比较结果失去正常的真假含义。

### 11.3 `QLayout` 的内容边距和 spacing 是两回事

即使使用浮点边距的几何计算，也不要把以下概念混淆：

- contents margins：布局边界到内容项的四边留白；
- spacing：相邻内容项之间的间距。

改变一个 `QMarginsF` 局部变量也不会自动调用布局的 setter。

### 11.4 像素对齐不是 `QMarginsF` 的职责

亚像素边距可以适合绘制和变换，但最终栅格化时可能需要像素对齐。是否向下、向上、四舍五入或按设备像素比对齐，应由绘制策略决定，不要把 `toMargins()` 当作所有场景的唯一像素策略。

## 12. 常见错误与排查顺序

### 12.1 把构造参数当成矩形参数

**症状：** 右边距出现巨大值，或内容区域尺寸完全不对。

**原因：** `QMarginsF(left, top, right, bottom)` 的四个参数全部是边距。

**修复：** 明确变量名，矩形位置和尺寸使用 `QRectF`。

### 12.2 期待 setter 自动更新布局

**症状：** `margins.setLeft()` 执行后界面没有变化。

**原因：** `QMarginsF` 是值对象，setter 只修改当前副本。

**修复：** 将修改后的值传回真正拥有它的布局、矩形或绘制流程。

### 12.3 用 `isNull()` 检查非负性

**症状：** 负边距没有被发现，或接近零的值被误判为精确零。

**原因：** `isNull()` 是逐边模糊零检查，不是业务合法性检查。

**修复：** 单独检查有限性、非负性和矩形尺寸约束。

### 12.4 把 `operator|` 当成 `operator+`

**症状：** 合并两组边距后结果没有变成两者总和。

**原因：** `|` 逐边取最大值，表达的是“至少满足两条约束”。

**修复：**

- 包裹层叠加使用 `+`；
- 独立最小约束合并使用 `|`；
- 其他规则逐边写出，不靠运算符猜测。

### 12.5 过早调用 `toMargins()`

**症状：** 多层缩放后某一边出现 1 像素差异。

**原因：** 每次中间转换都会丢失小数并执行舍入。

**修复：** 保持 `QMarginsF` 到最终像素边界，再统一转换。

### 12.6 除数为零、NaN 或不符合业务范围

**症状：** 调试构建触发断言，或结果出现 NaN/无穷。

**原因：** `operator/` 要求有效的非零除数；发布构建的断言也不能代替输入验证。

**修复：** 在除法前检查 `std::isfinite(divisor)` 和 `divisor != 0`，并确认缩放因子符合业务要求。

### 12.7 把 `operator==` 当成严格浮点相等

**症状：** 两个略有差异的 `QMarginsF` 被判定为相等。

**原因：** Qt 对 `QMarginsF` 使用 fuzzy equality。

**修复：** 需要固定误差或严格比较时，显式逐边实现对应策略。

### 12.8 把 `QDebug` 输出当协议

**症状：** Qt 升级或日志格式变化后，解析程序失效。

**原因：** `QDebug` 只用于诊断。

**修复：** 持久化使用 `QDataStream` 或明确设计的协议。

## 13. 推荐设计模板

### 13.1 保持浮点计算到最后

```cpp
QMargins toPixelMargins(const QMarginsF &logical,
                        qreal scale)
{
    Q_ASSERT(std::isfinite(scale));
    Q_ASSERT(scale > 0.0);
    return (logical * scale).toMargins();
}
```

生产代码还应根据输入来源决定如何处理断言失败，而不是只依赖调试构建。

### 13.2 用具名常量表达方向

```cpp
const qreal contentLeft = 16.0;
const qreal contentTop = 8.0;
const qreal contentRight = 16.0;
const qreal contentBottom = 10.0;

const QMarginsF margins(contentLeft, contentTop,
                        contentRight, contentBottom);
```

### 13.3 用 `+` 和 `|` 表达不同意图

```cpp
const QMarginsF wrapped = frameMargins + contentMargins;
const QMarginsF minimum = styleMargins | platformMargins;
```

代码阅读者可以直接从运算符看出是空间叠加，还是逐边选择较大约束。

### 13.4 对结构化绑定保持只读

```cpp
void logMargins(const QMarginsF &margins)
{
    const auto [left, top, right, bottom] = margins;
    qDebug() << "left:" << left
             << "top:" << top
             << "right:" << right
             << "bottom:" << bottom;
}
```

需要逐边修改时，使用 setter 或构造新值比试图通过结构化绑定改变方向语义更清楚。

## API 速查表
### 14.1 构造、读取和修改

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QMarginsF()` | 构造四边为 0 的边距 | 不读取布局默认值 |
| `QMarginsF(qreal left, qreal top, qreal right, qreal bottom)` | 按四边保存浮点值 | 顺序是左、上、右、下；允许负值 |
| `QMarginsF(const QMargins &)` | 把整数边距提升为浮点值 | 不会产生原本不存在的小数 |
| `left() const` | 读取左边距 | 返回 `qreal` 值副本 |
| `top() const` | 读取上边距 | 不是矩形 top 坐标 |
| `right() const` | 读取右边距 | 返回 `qreal` 值副本 |
| `bottom() const` | 读取下边距 | 返回 `qreal` 值副本 |
| `setLeft(qreal)` | 设置左边距 | 不自动更新布局或矩形 |
| `setTop(qreal)` | 设置上边距 | 不执行非负性检查 |
| `setRight(qreal)` | 设置右边距 | 不执行有限性检查 |
| `setBottom(qreal)` | 设置下边距 | 不执行有限性检查 |
| `isNull() const` | 判断四边是否都接近零 | 是模糊零判断，不是精确比较 |
| `toMargins() const` | 转为整数边距 | 逐边舍入并饱和到 `int` |

### 14.2 成员算术

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `operator+=(const QMarginsF &)` | 四边逐项相加 | 修改当前对象，不是矩形运算 |
| `operator-=(const QMarginsF &)` | 四边逐项相减 | 结果可能为负 |
| `operator+=(qreal)` | 四边都加同一个值 | 不是只调整水平或垂直边 |
| `operator-=(qreal)` | 四边都减同一个值 | 负参数会反向增加 |
| `operator*=(qreal)` | 四边逐项浮点缩放 | 不在此处转成整数 |
| `operator/=(qreal)` | 四边逐项浮点除法 | 除数不能为零或 NaN |

### 14.3 非成员算术和组合

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `operator+(m1, m2)` | 两个边距逐项相加 | 用于叠加包裹层 |
| `operator-(m1, m2)` | 两个边距逐项相减 | 不是 `QRectF` 的移除操作 |
| `operator+(margins, qreal)` | 四边加同一浮点数 | 返回新对象 |
| `operator+(qreal, margins)` | 对称加法 | 语义同右侧版本 |
| `operator-(margins, qreal)` | 四边减同一浮点数 | 结果可能为负 |
| `operator*(margins, qreal)` | 四边浮点缩放 | 结果仍是 `QMarginsF` |
| `operator*(qreal, margins)` | 对称浮点缩放 | 语义同右侧版本 |
| `operator/(margins, qreal)` | 四边浮点除法 | 除数必须有效且非零 |
| `operator|(m1, m2)` | 每边取较大值 | 不是相加，不是位或 |
| `operator+(margins)` | 返回相同值副本 | 一元正号 |
| `operator-(margins)` | 四边分别取负 | 不是交换方向 |

### 14.4 比较、转换、流和 tuple

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `qFuzzyCompare(lhs, rhs)` | 逐边浮点模糊比较 | 不是固定业务误差比较 |
| `qFuzzyIsNull(margins)` | 逐边模糊判断零 | 不检查非负性 |
| `operator==(lhs, rhs)` | 按 fuzzy equality 判断相等 | 不是严格 bit-level 相等 |
| `operator!=(lhs, rhs)` | 相等判断的反面 | 与 `operator==` 语义配套 |
| `operator==(QMarginsF, QMargins)` | 与整数边距比较 | 整数值先提升为浮点语义 |
| `QDataStream << QMarginsF` | 写入四个边距 | 约定流版本并检查协议 |
| `QDataStream >> QMarginsF` | 读回四个边距 | 检查流状态和输入来源 |
| `QDebug << QMarginsF` | 调试输出 | 不是稳定序列化格式 |
| `get<0..3>()` | tuple 协议访问分量 | 顺序是 left/top/right/bottom |
| `std::tuple_size<QMarginsF>` | tuple 元素数量 | 固定为 4 |
| `std::tuple_element<I, QMarginsF>` | tuple 元素类型 | 四个元素都是 `qreal` |

## 15. 一句话总结

`QMarginsF` 是保存四个浮点边距的轻量值类型：用它保留缩放和几何计算中的小数，用 `+` 叠加空间、用 `|` 合并逐边最小约束，用 `qFuzzyCompare` 处理浮点相等，最后在明确舍入策略后通过 `toMargins()` 转成整数像素。
