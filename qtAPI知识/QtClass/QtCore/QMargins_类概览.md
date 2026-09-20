# Qt QMargins 四边距值类型深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMargins>`  
> 所属模块：`Qt6::Core`  
> 类型性质：保存 left/top/right/bottom 四个整数边距的轻量值类型  
> 相关类型：`QMarginsF`、`QRect`、`QSize`、`QLayout`、`QDataStream`

## 1. 它解决什么问题

`QMargins` 用四个整数表示一个矩形区域四条边需要预留的空间：

```text
        top
   +------------+
left|   内容     |right
   +------------+
       bottom
```

它主要解决“同一个矩形的四边分别需要多少留白”的问题，常见于：

- 布局的 contents margins；
- 控件边框到内容绘制区域之间的内边距；
- 滚动区域 viewport 的预留空间；
- 文本、图标、装饰线与外框之间的几何间隔；
- 对一个矩形进行 `marginsAdded()`、`marginsRemoved()` 等几何计算时的中间值。

`QMargins` 不是：

- 具有位置和尺寸的矩形，矩形应使用 `QRect`；
- 只有一个统一数值的 spacing，统一间距可直接使用 `int`；
- 像素内容或布局对象，它只保存四个数；
- 自动约束为非负的 CSS padding。它可以保存负值，负值是否合法由使用它的 API 决定；
- 浮点布局边距。需要亚像素或缩放比例时使用 `QMarginsF`。

## 2. 实际使用场景

### 2.1 设置布局内容边距

```cpp
QVBoxLayout *layout = new QVBoxLayout(parent);
layout->setContentsMargins(QMargins(12, 8, 12, 10));
```

这里的四个值分别是左、上、右、下，而不是 `(x, y, width, height)`。左右相同、上下相同的边距也应明确写成四个分量，避免调用方误以为它是一个单值 spacing。

### 2.2 为绘制区域缩小内容矩形

```cpp
QRect contentRect = outerRect.marginsRemoved(
    QMargins(16, 8, 16, 8));
```

`QMargins` 只描述四边偏移，`QRect` 负责真正计算几何区域。边距和矩形的配合必须考虑目标矩形足够大，否则移除边距可能得到空矩形或反转的几何结果，具体行为由 `QRect` API 负责。

### 2.3 叠加两层内边距

```cpp
const QMargins frameMargins(2, 2, 2, 2);
const QMargins contentMargins(8, 4, 8, 4);
const QMargins totalMargins = frameMargins + contentMargins;
```

`operator+` 是四个分量分别相加：

```text
(left1 + left2,
 top1 + top2,
 right1 + right2,
 bottom1 + bottom2)
```

如果边距来自两套独立的包裹层，逐项相加通常比手工分别处理更不容易漏掉某一边。

### 2.4 用浮点边距处理缩放

```cpp
const QMargins logicalMargins(8, 4, 8, 4);
const QMarginsF scaledMargins =
    logicalMargins.toMarginsF() * deviceScale;
```

`QMargins::toMarginsF()` 将四个整数转换为浮点值，不会凭空恢复原本丢失的小数。若最后需要交给只接受整数边距的 API：

```cpp
const QMargins pixelMargins = scaledMargins.toMargins();
```

这一步会进行取整并在超出 `int` 范围时饱和，不能把它理解成无损转换。

### 2.5 选择四边较大的安全边距

```cpp
const QMargins styleMargins(4, 6, 4, 6);
const QMargins platformMargins(8, 4, 8, 4);
const QMargins effective = styleMargins | platformMargins;
```

`operator|` 对每一边取最大值：

```text
effective.left()   = max(style.left(), platform.left())
effective.top()    = max(style.top(), platform.top())
effective.right()  = max(style.right(), platform.right())
effective.bottom() = max(style.bottom(), platform.bottom())
```

它适合合并“至少需要这么大”的安全留白，不是位运算，也不是矩形联合。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QMargins>
#include <QMarginsF>
#include <QRect>
#include <QDebug>
```

如果只保存或计算边距，只需要 `QMargins`。布局和矩形运算还应包含实际使用的 `QLayout`、`QRect` 等类型头文件。

## 4. 数据模型和四个分量

### 4.1 四个分量没有共享的方向别名

`QMargins` 的字段语义固定为：

| 分量 | 方向 | 增加它通常表示 |
| --- | --- | --- |
| `left` | 左 | 内容区从左侧向内缩 |
| `top` | 上 | 内容区从上侧向内缩 |
| `right` | 右 | 内容区从右侧向内缩 |
| `bottom` | 下 | 内容区从下侧向内缩 |

它不保存“水平边距”和“垂直边距”两个逻辑字段，因此设置对称边距时仍然要分别写 left/right 和 top/bottom。

### 4.2 允许负值

```cpp
QMargins overlap(-2, 0, -2, 0);
```

构造函数和 setter 不会把负数自动钳制为零。负值在某些几何算法中可表示内容向边框外扩，但布局、控件或平台 API 可能有自己的约束。

因此，是否允许负边距要在业务边界决定：

- 纯数学组合可以保留负值；
- 交给布局前确认布局的文档语义；
- 交给绘制代码前确认结果矩形不会造成意外反转；
- 不要把 `isNull()` 当成“所有边距非负”的检查。

### 4.3 `isNull()` 是全零判断

```cpp
QMargins a(0, 0, 0, 0);
QMargins b(-1, 0, 1, 0);

Q_ASSERT(a.isNull());
Q_ASSERT(!b.isNull());
```

只有四个分量都精确等于 0 时，`isNull()` 才返回 `true`。带负值、正负抵消或四边总和为零都不算 null。

## 5. 值语义、constexpr 和结构化绑定

### 5.1 它是轻量值类型

```cpp
QMargins margins(4, 8, 4, 8);
QMargins copy = margins;
copy.setTop(12);
```

`copy` 和 `margins` 是独立的四个整数值。复制不涉及 QObject 所有权、共享资源或事件循环。

### 5.2 大多数基础操作是 `constexpr`

构造、读取、setter、整数算术和许多比较可以在编译期求值：

```cpp
constexpr QMargins defaultMargins(8, 6, 8, 6);
static_assert(defaultMargins.left() == 8);
```

是否真的在编译期执行仍取决于表达式和编译器环境；`constexpr` 不改变运行时的边界条件，例如除零和 checked integer 溢出仍需要避免。

### 5.3 支持 tuple 协议

Qt 6.11.1 的头文件为 `QMargins` 提供四元素 tuple 协议，可以使用结构化绑定：

```cpp
const QMargins margins(1, 2, 3, 4);
const auto [left, top, right, bottom] = margins;
```

四个元素的类型都是 `int`，顺序是 left、top、right、bottom。结构化绑定适合同时读取四个分量；需要表达方向意图时，直接写 `margins.left()` 等命名 API 往往更清楚。

## 6. 整数算术的溢出和除零边界

### 6.1 整数加减乘使用 checked int

Qt 6.11.1 的 `QMargins` 内部使用 checked integer 表示。整数加法、减法、乘法和一元负号在溢出时通过断言报告问题，而不是依赖有符号整数溢出的未定义行为。

```cpp
QMargins huge(std::numeric_limits<int>::max(), 0, 0, 0);

// 调用后会触发溢出检查，不应把它当成正常的环绕运算。
const QMargins result = huge + QMargins(1, 0, 0, 0);
```

工程代码不应利用溢出后的数值。边距来自外部输入、DPI 计算或缩放因子时，应先把结果限制在业务允许的 `int` 范围内。

### 6.2 整数除法需要非零 divisor

```cpp
const QMargins half = margins / 2;
```

整数除法按整数语义作用于每一边，除数为 0 是错误。负数除法的截断方向遵循 C++ 整数除法规则，不要用它替代需要明确四舍五入的浮点缩放。

### 6.3 `qreal` 缩放会四舍五入并饱和

```cpp
const QMargins pixels = margins * 1.5;
```

整数边距乘以 `qreal` 时，Qt 会对每一边做浮点计算，再进行取整并饱和到 `int` 可表示范围。这样可以避免浮点结果转换为 int 时直接产生未定义或越界结果，但它仍然是有损转换。

不要依赖边界值的偶数舍入细节来编码业务规则；需要严格像素策略时，在业务层先定义缩放和舍入规则。

### 6.4 `qreal` 除法也要求非零

```cpp
const QMargins pixels = margins / deviceScale;
```

`deviceScale` 不能为 0，也不能是足够接近 0 而被 Qt 的模糊零判断视为零的值。违反前置条件时调试构建会触发断言。

## 7. 逐项 API 说明

### 7.1 `[constexpr noexcept] QMargins::QMargins()`

```cpp
constexpr QMargins() noexcept;
```

构造四边均为 0 的边距：

```cpp
constexpr QMargins margins;
static_assert(margins.isNull());
```

它表示“没有额外边距”，不是未初始化状态，也不包含任何布局默认值。

### 7.2 `[constexpr noexcept] QMargins::QMargins(int left, int top, int right, int bottom)`

```cpp
constexpr QMargins(int left, int top, int right, int bottom) noexcept;
```

按 left、top、right、bottom 顺序构造边距。

参数可以是负数。构造函数不验证它们是否适合之后的布局或矩形操作。

```cpp
const QMargins margins(12, 8, 12, 10);
```

### 7.3 `[constexpr noexcept] int QMargins::left() const`

```cpp
constexpr int left() const noexcept;
```

返回左边距。返回的是值副本，不是内部字段引用。

### 7.4 `[constexpr noexcept] int QMargins::top() const`

```cpp
constexpr int top() const noexcept;
```

返回上边距。它和 `QRect` 的 top 坐标不是同一个概念；这里表示从矩形上边向内容区域预留的数值。

### 7.5 `[constexpr noexcept] int QMargins::right() const`

```cpp
constexpr int right() const noexcept;
```

返回右边距。

### 7.6 `[constexpr noexcept] int QMargins::bottom() const`

```cpp
constexpr int bottom() const noexcept;
```

返回下边距。

### 7.7 `[constexpr noexcept] void QMargins::setLeft(int left)`

```cpp
constexpr void setLeft(int left) noexcept;
```

替换左边距。它只修改当前值对象，不会通知布局或自动更新任何 `QWidget`。

### 7.8 `[constexpr noexcept] void QMargins::setTop(int top)`

```cpp
constexpr void setTop(int top) noexcept;
```

替换上边距。需要改变布局的实际边距时，还要把修改后的 `QMargins` 传回对应布局 API。

### 7.9 `[constexpr noexcept] void QMargins::setRight(int right)`

```cpp
constexpr void setRight(int right) noexcept;
```

替换右边距。允许负值，是否接受由下游 API 决定。

### 7.10 `[constexpr noexcept] void QMargins::setBottom(int bottom)`

```cpp
constexpr void setBottom(int bottom) noexcept;
```

替换下边距。

### 7.11 `[constexpr noexcept] bool QMargins::isNull() const`

```cpp
constexpr bool isNull() const noexcept;
```

当 left、top、right、bottom 全部为 0 时返回 `true`，否则返回 `false`。

它不判断：

- 是否所有分量都为正；
- 是否四边总和为 0；
- 是否适合一个具体矩形；
- 是否等于某个布局系统的默认边距。

### 7.12 `[constexpr noexcept, since 6.4] QMarginsF QMargins::toMarginsF() const`

```cpp
constexpr QMarginsF toMarginsF() const noexcept;
```

Qt 6.4 起将整数边距转换为浮点边距：

```cpp
const QMargins integerMargins(3, 5, 3, 5);
const QMarginsF floatingMargins = integerMargins.toMarginsF();
```

每个整数会精确转换为对应的 `qreal`。它不会产生小数，也不会改变边距语义。

## 8. 成员复合算术运算

### 8.1 `QMargins &operator+=(const QMargins &margins)`

```cpp
QMargins &operator+=(const QMargins &margins) noexcept;
```

四边分别相加：

```cpp
margins += extra;
```

等价于对 left、top、right、bottom 各自执行加法。整数溢出会触发 checked integer 检查。

### 8.2 `QMargins &operator-=(const QMargins &margins)`

```cpp
QMargins &operator-=(const QMargins &margins) noexcept;
```

四边分别相减。它不是“从矩形中删除 margin”的几何操作，只是边距值的逐项算术。

### 8.3 `QMargins &operator+=(int addend)`

```cpp
QMargins &operator+=(int addend) noexcept;
```

给四个边都加上同一个整数：

```cpp
margins += 2;
```

左、上、右、下都会增加 2。它不表示只调整水平或垂直方向。

### 8.4 `QMargins &operator-=(int subtrahend)`

```cpp
QMargins &operator-=(int subtrahend) noexcept;
```

给四个边都减去同一个整数。负参数会产生反向效果，但为了可读性通常应直接使用加法。

### 8.5 `QMargins &operator*=(int factor)`

```cpp
QMargins &operator*=(int factor) noexcept;
```

四边分别乘以整数因子。整数溢出会触发检查，不会提供可依赖的环绕语义。

### 8.6 `QMargins &operator/=(int divisor)`

```cpp
QMargins &operator/=(int divisor);
```

四边分别除以整数除数。`divisor` 不能为 0；整数结果按整数除法规则处理。

### 8.7 `QMargins &operator*=(qreal factor)`

```cpp
QMargins &operator*=(qreal factor) noexcept;
```

四边分别乘以浮点因子，再取整并饱和到 `int` 范围。常用于把逻辑像素边距按缩放因子转换成整数像素边距。

### 8.8 `QMargins &operator/=(qreal divisor)`

```cpp
QMargins &operator/=(qreal divisor);
```

四边分别除以浮点除数，再取整并饱和。除数不能为 0 或被 Qt 判断为模糊零。

## 9. 非成员算术和组合 API

### 9.1 `QMargins operator+(const QMargins &, const QMargins &)`

返回两个边距逐项相加的结果，不修改输入对象：

```cpp
const QMargins total = outer + inner;
```

### 9.2 `QMargins operator-(const QMargins &, const QMargins &)`

返回两个边距逐项相减的结果，不执行矩形几何运算。

### 9.3 `QMargins operator+(const QMargins &, int)`

给四边都加同一个整数，返回新对象。

### 9.4 `QMargins operator+(int, const QMargins &)`

支持整数写在左侧的对称形式，语义与 `margins + addend` 相同。

### 9.5 `QMargins operator-(const QMargins &, int)`

给四边都减同一个整数，返回新对象。

### 9.6 `QMargins operator*(const QMargins &, int)`

四边分别乘以整数因子。整数溢出会触发 checked integer 检查。

### 9.7 `QMargins operator*(int, const QMargins &)`

支持整数写在左侧的对称形式：

```cpp
const QMargins scaled = 2 * margins;
```

### 9.8 `QMargins operator*(const QMargins &, qreal)`

四边分别乘以浮点因子，再四舍五入并饱和到 `int` 范围：

```cpp
const QMargins scaled = margins * 1.25;
```

### 9.9 `QMargins operator*(qreal, const QMargins &)`

支持浮点因子写在左侧，语义与右侧因子版本相同。

### 9.10 `QMargins operator/(const QMargins &, int)`

四边分别进行整数除法。除数为 0 是错误。

### 9.11 `QMargins operator/(const QMargins &, qreal)`

四边分别进行浮点除法，再取整并饱和。除数不能为零或模糊零。

### 9.12 `QMargins operator|(const QMargins &, const QMargins &)`

逐边取最大值：

```cpp
const QMargins safe = a | b;
```

它适合合并两个“最小安全边距”约束。它不是：

- C++ 位或；
- 四边相加；
- 矩形联合；
- 取四边绝对值。

### 9.13 `QMargins operator+(const QMargins &)`

一元正号直接返回同值副本：

```cpp
const QMargins same = +margins;
```

它不改变任何分量。

### 9.14 `QMargins operator-(const QMargins &)`

一元负号将四个分量分别取负：

```cpp
const QMargins inverted = -margins;
```

如果某个分量等于 `INT_MIN`，取负会触发 checked integer 溢出检查。不要把一元负号当作“把左边换成右边、把上边换成下边”的几何翻转。

## 10. 比较、序列化和调试输出

### 10.1 `operator==` 和 `operator!=`

比较四个分量是否逐一相等：

```cpp
if (margins == QMargins(8, 4, 8, 4))
    useCompactLayout();
```

比较的是精确整数值。与 `QMarginsF` 不同，`QMargins` 不需要 fuzzy comparison。

### 10.2 与 `QMarginsF` 的比较边界

`QMarginsF` 使用浮点语义，其相等判断和 `qFuzzyCompare()` 相关。将 `QMargins` 转为 `QMarginsF` 后，不要把整数对象的精确相等直觉无条件套到浮点对象上。

### 10.3 `QDataStream &operator<<(QDataStream &, const QMargins &)`

```cpp
QDataStream &operator<<(QDataStream &out,
                        const QMargins &margins);
```

把四个整数边距写入 Qt 数据流。它适合 Qt 两端都使用明确 `QDataStream` 版本的持久化或 IPC。

数据流仍需要：

- 设置并约定 `QDataStream::Version`；
- 对不可信输入限制数据大小；
- 读取端检查流状态；
- 不要把 Qt 默认二进制布局当作跨语言协议。

### 10.4 `QDataStream &operator>>(QDataStream &, QMargins &)`

```cpp
QDataStream &operator>>(QDataStream &in,
                        QMargins &margins);
```

从数据流读取四个整数边距。读取后应检查 `QDataStream::status()`，因为得到一个 `QMargins` 对象不表示输入一定完整或可信。

### 10.5 `QDebug operator<<(QDebug, const QMargins &)`

```cpp
QDebug operator<<(QDebug debug, const QMargins &margins);
```

支持：

```cpp
qDebug() << margins;
```

它是诊断输出，不是稳定序列化格式。不要解析 `QDebug` 文本来恢复四个边距。

## 11. `QMargins` 与 `QMarginsF` 的转换

### 11.1 整数到浮点是精确提升

```cpp
const QMargins integerMargins(3, 4, 5, 6);
const QMarginsF floatingMargins(integerMargins);
```

也可以调用：

```cpp
const QMarginsF floatingMargins = integerMargins.toMarginsF();
```

每个 int 分量直接转换为 `qreal`。

### 11.2 浮点到整数会取整

```cpp
const QMarginsF floatingMargins(1.4, 2.5, 3.6, 4.9);
const QMargins integerMargins = floatingMargins.toMargins();
```

`toMargins()` 对每一边进行取整并饱和。它不是截断，也不是保证每次都向下取整。

如果业务需要明确的 floor、ceil 或银行家舍入，先在业务层对每个分量使用明确的舍入函数，再构造 `QMargins`。

### 11.3 `QMarginsF::isNull()` 与 `QMargins::isNull()` 不同

`QMargins::isNull()` 要求四个整数精确为 0；`QMarginsF::isNull()` 使用浮点模糊零判断。转换前后的 null 判断在接近 0 的浮点值上可能不同。

## 12. 与矩形和布局 API 的边界

### 12.1 `QMargins` 只保存偏移，不计算矩形

```cpp
const QRect content =
    outer.marginsRemoved(margins);
```

边距如何作用到矩形，取决于 `QRect` 的 `marginsAdded()` / `marginsRemoved()` 等几何 API。不要把 `QMargins` 的四个整数自行拼成 `QRect` 的 x/y/width/height，除非你明确需要实现几何算法。

### 12.2 边距总和可能超过矩形尺寸

如果 left + right 大于矩形宽度，或者 top + bottom 大于矩形高度，内容矩形可能退化、为空或出现反向边界。`QMargins` 本身不会阻止这种状态。

在处理用户配置、主题、DPI 或外部布局数据时，可以先验证：

```cpp
const bool fits =
    margins.left() + margins.right() <= rect.width()
    && margins.top() + margins.bottom() <= rect.height();
```

还要注意加法本身可能溢出；对不可信的大整数应先使用更宽的临时类型或提前限制范围。

### 12.3 `QLayout` 的 contents margins 不等于 spacing

布局中至少有两类间距：

- `contentsMargins`：布局边界到内容项的四边留白；
- `spacing`：相邻子项之间的间隔。

把两个概念混为一谈会导致“外边距变大但子控件之间仍太挤”或相反的问题。

### 12.4 `QMargins` 不会自动刷新布局

```cpp
QMargins margins = layout->contentsMargins();
margins.setLeft(margins.left() + 4);
```

这里只修改了一个局部值副本。要修改实际布局，必须：

```cpp
layout->setContentsMargins(margins);
```

这也是 Qt 值类型的典型语义：getter 返回的是值，修改值对象不会反向修改拥有它的 QObject。

## 13. 常见错误与排查顺序

### 13.1 把参数顺序写成 x/y/width/height

**症状：** 左右或上下出现异常大留白。

**原因：** `QMargins(left, top, right, bottom)` 的四个参数都是边距，不是矩形坐标和尺寸。

**修复：** 使用命名局部变量或直接调用四个 setter，确认方向顺序。

### 13.2 修改 getter 返回值却没有更新布局

**症状：** `margins.setLeft()` 执行了，但界面没有变化。

**原因：** getter 得到的是值副本。

**修复：** 修改后把 `QMargins` 传回 `setContentsMargins()` 或相应 setter。

### 13.3 用 `isNull()` 检查“没有负边距”

**症状：** `QMargins(-2, 0, 2, 0)` 被错误地认为是合法零边距。

**原因：** `isNull()` 只检查四边是否全部为 0。

**修复：** 逐边检查 `left() >= 0` 等业务条件。

### 13.4 浮点缩放后直接假设结果精确

**症状：** 1.5 倍、0.75 倍缩放后像素与预期有一边差 1。

**原因：** `QMargins` 的 qreal 运算需要取整。

**修复：** 明确业务的舍入策略，或保留 `QMarginsF` 到最终绘制阶段。

### 13.5 忽略整数溢出

**症状：** 大边距、缩放或累加在调试构建触发断言。

**原因：** Qt 6.11.1 对 QMargins 整数算术进行 checked overflow 检查。

**修复：** 输入验证、使用更宽临时类型计算、在进入 `QMargins` 前限制到有效范围。

### 13.6 用 `/ 0` 试图表示“清除边距”

**症状：** 调试断言或异常行为。

**原因：** 除法 API 要求非零除数。

**修复：** 清除边距使用 `QMargins()` 或显式设置四边为 0。

### 13.7 把 `operator|` 当作加法

**症状：** 合并两个安全边距后结果没有变成两者总和。

**原因：** `|` 是逐边取最大值，表达“至少满足两个约束”。

**修复：**

- 层层包裹的空间叠加用 `+`；
- 独立最小要求的合并用 `|`；
- 需要业务特殊规则时逐边写出规则。

### 13.8 以为 QMargins 只能保存正数

**症状：** 代码遇到负值时错误地把它当成构造失败。

**原因：** QMargins 是数值值类型，不负责业务合法性校验。

**修复：** 在布局或外部输入边界显式验证非负条件。

## 14. 推荐设计模板

### 14.1 用命名常量表达方向

```cpp
constexpr int horizontal = 12;
constexpr int vertical = 8;
const QMargins margins(horizontal, vertical,
                       horizontal, vertical);
```

如果四边有不同语义，直接使用四个有意义的变量：

```cpp
const int contentLeft = 16;
const int contentTop = 8;
const int contentRight = 16;
const int contentBottom = 10;

const QMargins contentMargins(contentLeft, contentTop,
                              contentRight, contentBottom);
```

### 14.2 叠加包裹层边距

```cpp
QMargins calculateTotalMargins(const QMargins &frame,
                               const QMargins &content)
{
    return frame + content;
}
```

这里明确表达的是四边叠加，不应改写成统一 addend，除非四边确实是相同规则。

### 14.3 从浮点布局保守转换到像素

```cpp
QMargins toPixelMargins(const QMarginsF &logical,
                        qreal scale)
{
    Q_ASSERT(scale > 0);
    return (logical * scale).toMargins();
}
```

如果 `QMarginsF` 的乘法可能产生 NaN、无穷或异常大的值，应在业务层先验证输入，再调用 `toMargins()`。

### 14.4 结构化绑定只读读取

```cpp
void logMargins(const QMargins &margins)
{
    const auto [left, top, right, bottom] = margins;
    qDebug() << "left:" << left
             << "top:" << top
             << "right:" << right
             << "bottom:" << bottom;
}
```

需要按方向执行不同逻辑时，结构化绑定可以减少重复 getter；公共接口和复杂业务判断通常仍更适合显式调用 `left()` 等命名函数。

## API 速查表
### 15.1 构造、读取与修改

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QMargins()` | 构造四边为 0 的边距 | `isNull()` 为 true；不是未初始化状态 |
| `QMargins(int left, int top, int right, int bottom)` | 按四个方向构造 | 顺序是左、上、右、下；允许负值 |
| `left() const` | 读取左边距 | 返回 int 值副本 |
| `top() const` | 读取上边距 | 不是矩形 top 坐标 |
| `right() const` | 读取右边距 | 返回 int 值副本 |
| `bottom() const` | 读取下边距 | 返回 int 值副本 |
| `setLeft(int)` | 设置左边距 | 不自动更新布局对象 |
| `setTop(int)` | 设置上边距 | 不自动更新布局对象 |
| `setRight(int)` | 设置右边距 | 允许负值 |
| `setBottom(int)` | 设置下边距 | 允许负值 |
| `isNull() const` | 判断四边是否全为 0 | 不等于“所有值非负” |
| `[since 6.4] toMarginsF() const` | 转为浮点边距 | 整数到浮点是精确提升 |

### 15.2 成员算术

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `operator+=(const QMargins &)` | 四边逐项相加 | 可能触发整数溢出检查 |
| `operator-=(const QMargins &)` | 四边逐项相减 | 不是矩形移除操作 |
| `operator+=(int)` | 四边都加同一整数 | 不是只加水平或垂直方向 |
| `operator-=(int)` | 四边都减同一整数 | 负参数会反向增加 |
| `operator*=(int)` | 四边逐项乘整数 | 溢出会触发 checked 检查 |
| `operator/=(int)` | 四边逐项做整数除法 | 除数不能为 0；结果为整数 |
| `operator*=(qreal)` | 四边浮点缩放 | 取整并饱和到 int 范围 |
| `operator/=(qreal)` | 四边浮点除法 | 除数不能为零或模糊零 |

### 15.3 非成员算术和组合

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `operator+(m1, m2)` | 两个边距逐项相加 | 用于叠加包裹层 |
| `operator-(m1, m2)` | 两个边距逐项相减 | 结果可能为负 |
| `operator+(margins, int)` | 四边加同一整数 | 返回新对象 |
| `operator+(int, margins)` | 对称加法写法 | 语义同右侧版本 |
| `operator-(margins, int)` | 四边减同一整数 | 返回新对象 |
| `operator*(margins, int)` | 整数缩放 | 溢出会触发检查 |
| `operator*(int, margins)` | 对称整数缩放 | 语义同右侧版本 |
| `operator*(margins, qreal)` | 浮点缩放 | 取整并饱和 |
| `operator*(qreal, margins)` | 对称浮点缩放 | 语义同右侧版本 |
| `operator/(margins, int)` | 整数除法 | 除数非零；按整数规则取值 |
| `operator/(margins, qreal)` | 浮点除法 | 除数非零；取整并饱和 |
| `operator|(m1, m2)` | 每边取最大值 | 不是位或，也不是相加 |
| `operator+(margins)` | 一元正号 | 返回相同值副本 |
| `operator-(margins)` | 四边取负 | `INT_MIN` 取负会溢出 |

### 15.4 比较、转换和流

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `operator==(lhs, rhs)` | 比较四边精确相等 | 逐个 int 比较 |
| `operator!=(lhs, rhs)` | 比较四边不等 | 与 equality 配套 |
| `toMarginsF()` | 整数转浮点 | Qt 6.4 起；不产生小数 |
| `QDataStream << QMargins` | 写入四个边距 | 设置流版本并管理协议 |
| `QDataStream >> QMargins` | 读取四个边距 | 检查流状态和输入来源 |
| `QDebug << QMargins` | 调试打印 | 不是稳定序列化格式 |
| tuple `get<0..3>()` | 结构化绑定读取四边 | 顺序是 left/top/right/bottom |

## 16. 一句话总结

`QMargins` 是保存 left/top/right/bottom 四个整数边距的轻量值类型：用 getter/setter 管理方向分量，用 `+` 叠加包裹层、用 `|` 合并逐边最小约束，用 `QMarginsF` 处理浮点缩放，并在整数溢出、除零、负边距和布局对象值拷贝这些边界上保持明确。
