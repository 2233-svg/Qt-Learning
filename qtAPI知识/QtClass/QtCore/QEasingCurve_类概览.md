# Qt QEasingCurve 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QEasingCurve>`  
> 所属模块：`Qt6::Core`  
> 定位：动画插值的缓动曲线值类型  
> 常见协作类：`QVariantAnimation`、`QPropertyAnimation`

## 1. 它解决什么问题

动画通常先得到一个从 0 到 1 的线性进度，再把这个进度映射成实际的位置、透明度、大小或颜色。如果直接使用线性进度，物体会以恒定速度运动；真实界面往往需要“慢慢开始、快速经过、慢慢停下”或带有回弹、弹性效果。

`QEasingCurve` 保存的就是这条“进度映射函数”：

```text
输入 progress（通常为 0..1）
              |
              v
QEasingCurve::valueForProgress()
              |
              v
effective progress（可能超出 0..1）
```

例如把动画时间进度 `0.5` 交给 `InOutQuad`，得到的有效进度会与 `0.5` 不同；再把这个有效进度用于插值，运动就会先加速再减速。

它可以单独使用，也可以交给动画类：

```cpp
QPropertyAnimation animation(widget, "geometry");
animation.setDuration(400);
animation.setEasingCurve(QEasingCurve::InOutCubic);
```

## 2. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QEasingCurve>
```

如果使用 `QPropertyAnimation` 或 `QVariantAnimation`，还需要链接对应模块；`QEasingCurve` 本身属于 `Qt6::Core`。

## 3. 最小可用代码

```cpp
#include <QEasingCurve>
#include <QDebug>

void printCurve()
{
    const QEasingCurve easing(QEasingCurve::InOutQuad);

    for (qreal progress = 0.0; progress <= 1.0; progress += 0.25)
        qDebug() << progress << "->"
                 << easing.valueForProgress(progress);
}
```

默认构造或使用 `QEasingCurve::Linear` 时，`valueForProgress(t)` 对正常的 `0..1` 输入返回线性进度。选择曲线时，先确定动画希望表现的物理感觉，再考虑是否需要自定义 spline 或函数。

## 4. 曲线类型怎么选

### 4.1 In、Out、InOut 和 OutIn

曲线名称里的方向描述速度变化，而不是坐标方向：

| 前缀 | 含义 | 典型感觉 |
| --- | --- | --- |
| `In` | 从低速开始并逐渐加速 | 物体从静止启动 |
| `Out` | 逐渐减速并停下 | 物体平滑落位 |
| `InOut` | 前半段加速，后半段减速 | 最常用的自然过渡 |
| `OutIn` | 前半段减速，后半段加速 | 特殊节奏，普通 UI 较少使用 |

`Quad`、`Cubic`、`Quart`、`Quint` 表示多项式强度；`Sine`、`Expo`、`Circ` 表示正弦、指数、圆形函数；`Elastic`、`Back`、`Bounce` 会产生弹性、超调或弹跳效果。

### 4.2 超出范围是合法的

输入 `progress` 按文档应在 `0..1` 范围内。某些曲线的返回值可以超出 `0..1`：

- `Back` 可能在开始或结束附近超调；
- `Elastic` 可能出现弹簧式振荡；
- 自定义函数也可以返回范围外的值。

因此不能无条件把返回值 clamp 到 `0..1`，否则会抹掉曲线设计的视觉效果。只有业务对象明确不能接受越界值时，才在插值层决定是否限制。

## 5. 参数适用范围

`amplitude`、`overshoot` 和 `period` 不是所有曲线都使用。设置它们之前必须先确认当前 `type()`：

| 参数 | 生效曲线 | 语义 |
| --- | --- | --- |
| `amplitude` | `InBounce`、`OutBounce`、`InOutBounce`、`OutInBounce`、四种 `Elastic` | 回弹高度或弹簧效果的峰值 |
| `period` | 四种 `Elastic` | 弹性振荡的周期；值越大，频率越低 |
| `overshoot` | 四种 `Back` | 超过终点或起点的幅度；默认值 `1.70158`，产生约 10% 的超调；设置为 0 则无超调 |

对于不适用的曲线，读取这些参数没有业务意义；不要把它们当作所有 `QEasingCurve` 类型都共享的通用配置。

## 6. 自定义曲线

### 6.1 自定义函数

```cpp
static qreal smoothStep(qreal progress)
{
    return progress * progress * (3.0 - 2.0 * progress);
}

QEasingCurve easing;
easing.setCustomType(&smoothStep);
Q_ASSERT(easing.type() == QEasingCurve::Custom);
```

自定义函数签名是：

```cpp
qreal function(qreal progress);
```

`func` 不能是 `nullptr`。输入通常按归一化 `0..1` 解释，返回值通常也按归一化进度解释，但允许在某些效果中超出该范围。

调用 `setCustomType()` 后，`type()` 返回 `Custom`；不能把 `Custom` 作为参数再传给 `setType()`，因为 `Custom` 代表“已经指定了函数”，不是一个内置曲线算法。

### 6.2 Bezier spline

```cpp
QEasingCurve easing(QEasingCurve::BezierSpline);
easing.addCubicBezierSegment(
    QPointF(0.25, 0.1),
    QPointF(0.25, 1.0),
    QPointF(1.0, 1.0));
```

Bezier spline 隐式从 `(0, 0)` 开始。要成为有效的 easing curve，最后必须到达 `(1, 1)`；每个 segment 的控制点和终点共同定义曲线，不是普通的“给几个动画关键帧”接口。

`toCubicSpline()` 可以取回定义自定义 Bezier 曲线的点列表；当前不是 Bezier 自定义曲线时返回空列表。

### 6.3 TCB spline

```cpp
QEasingCurve easing(QEasingCurve::TCBSpline);
easing.addTCBSegment(QPointF(0.5, 0.2),
                     0.0,  // tension
                     0.0,  // continuity
                     0.0); // bias
```

TCB 的三个参数都应在 `-1..1`：

- `tension` 改变切线长度；
- `continuity` 改变切线过渡的尖锐程度；
- `bias` 改变切线方向。

三个参数都为 0 时得到 Catmull-Rom 风格的 spline。TCB spline 也必须显式从 `(0, 0)` 开始，并在 `(1, 1)` 结束。

## 7. 与动画类协作时的边界

`QEasingCurve` 只负责把时间进度映射成有效进度，不负责计时、属性读写或发出动画信号。真正的动画生命周期由 `QAbstractAnimation`、`QVariantAnimation` 或 `QPropertyAnimation` 管理。

```cpp
auto *animation = new QPropertyAnimation(widget, "windowOpacity");
animation->setStartValue(0.0);
animation->setEndValue(1.0);
animation->setDuration(250);
animation->setEasingCurve(QEasingCurve::OutCubic);
animation->start(QAbstractAnimation::DeleteWhenStopped);
```

如果有效进度超出 `0..1`，最终值是否允许越过 start/end 取决于动画属性类型和插值实现。对颜色、整数、几何尺寸等属性，先确认越界插值是否符合业务预期；不要把 `Back` 或 `Elastic` 无脑用于有硬边界的数值。

## 8. 拷贝、移动、比较与序列化

`QEasingCurve` 是值类型，支持拷贝和移动。拷贝会复制曲线配置；移动后源对象只应继续执行满足 C++ 移动语义的操作，例如析构或重新赋值。

```cpp
QEasingCurve source(QEasingCurve::OutBack);
QEasingCurve copy = source;
QEasingCurve moved = std::move(source);
```

`operator==` / `operator!=` 比较曲线类型以及曲线属性，不只是比较枚举值。自定义函数曲线还涉及函数指针配置，序列化前要确认目标进程是否能解释同一配置。

`QDataStream` 的 `operator<<` / `operator>>` 可用于 Qt 数据流序列化。二进制数据跨版本、跨进程保存时仍需自行管理版本号和失败检查，不能把数据流运算符当作稳定的跨产品协议。

## 9. 常见误区

| 误区 | 为什么会出问题 | 应该怎样做 | 使用时重点注意 |
| --- | --- | --- | --- |
| 把 easing curve 当作计时器 | 它只计算进度映射，不推进时间 | 交给动画类或在自己的采样循环中调用 | 时间节拍由外部负责 |
| 认为返回值永远在 `0..1` | `Back`、`Elastic` 和自定义函数可以越界 | 根据属性边界决定是否 clamp | clamp 会改变视觉效果 |
| 对所有曲线都设置 amplitude/period/overshoot | 这些参数只对特定曲线生效 | 先检查 `type()` | 参数不适用时不要依赖读取结果 |
| 用 `Custom` 调用 `setType()` | `Custom` 是 `setCustomType()` 产生的状态 | 用 `setCustomType(nonNullFunction)` | `func` 不能为 `nullptr` |
| Bezier spline 没有结束在 `(1, 1)` | 得到的曲线不是有效的归一化 easing curve | 最后一个 segment 明确收于 `(1, 1)` | 起点和终点约束不是可选项 |
| 把 overshoot 当成所有曲线通用参数 | 只有 `Back` 曲线使用它 | 仅在四种 `Back` 曲线上调整 | 默认值会产生超调 |

## API 速查表

### 10.1 成员类型与曲线枚举

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型别名 | `using EasingFunction = qreal (*)(qreal progress)` | 表示自定义 easing 函数的函数指针类型 | 函数不能为 `nullptr`；输入和返回值按归一化进度理解 |
| 枚举 | `Linear` | 线性速度，返回值与输入进度相同 | 默认曲线；不产生加速、减速或超调 |
| 枚举 | `InQuad` / `OutQuad` / `InOutQuad` / `OutInQuad` | 二次曲线的加速、减速、组合变体 | 适合普通 UI 过渡，强度低于高次多项式 |
| 枚举 | `InCubic` / `OutCubic` / `InOutCubic` / `OutInCubic` | 三次曲线的加速、减速、组合变体 | 常用于自然的进入和离开 |
| 枚举 | `InQuart` / `OutQuart` / `InOutQuart` / `OutInQuart` | 四次曲线变体 | 加减速比 Cubic 更明显 |
| 枚举 | `InQuint` / `OutQuint` / `InOutQuint` / `OutInQuint` | 五次曲线变体 | 变化更强，长距离动画中要注意突兀感 |
| 枚举 | `InSine` / `OutSine` / `InOutSine` / `OutInSine` | 正弦型曲线变体 | 变化较柔和，适合平滑过渡 |
| 枚举 | `InExpo` / `OutExpo` / `InOutExpo` / `OutInExpo` | 指数型曲线变体 | 起止速度差异明显，短动画中可能显得激烈 |
| 枚举 | `InCirc` / `OutCirc` / `InOutCirc` / `OutInCirc` | 圆函数曲线变体 | 具有明显的圆弧式加减速 |
| 枚举 | `InElastic` / `OutElastic` / `InOutElastic` / `OutInElastic` | 弹簧式振荡曲线 | 可设置 amplitude 和 period；返回值可能越界 |
| 枚举 | `InBack` / `OutBack` / `InOutBack` / `OutInBack` | 带回拉超调的曲线 | 可设置 overshoot；返回值可能越界 |
| 枚举 | `InBounce` / `OutBounce` / `InOutBounce` / `OutInBounce` | 弹跳式曲线 | 可设置 amplitude；不要用于不能越界的硬边界属性 |
| 兼容枚举 | `InCurve` | 头文件保留的历史曲线枚举值（41） | Qt 6.11.1 类页没有提供独立的当前语义；新代码优先使用文档列出的曲线族 |
| 兼容枚举 | `OutCurve` | 头文件保留的历史曲线枚举值（42） | 不要把它与 `OutQuad` 等当前文档化曲线混为一谈 |
| 兼容枚举 | `SineCurve` | 头文件保留的历史曲线枚举值（43） | Qt 6.11.1 类页没有提供独立的当前语义；需要正弦曲线时使用 `InSine` 等类型 |
| 兼容枚举 | `CosineCurve` | 头文件保留的历史曲线枚举值（44） | 新代码不要依赖未在当前类页说明的行为 |
| 枚举 | `BezierSpline` | 使用 cubic Bezier spline 定义曲线 | 通过 `addCubicBezierSegment()` 配置，需从 `(0,0)` 到 `(1,1)` |
| 枚举 | `TCBSpline` | 使用 TCB spline 定义曲线 | 通过 `addTCBSegment()` 配置，参数范围为 `-1..1` |
| 枚举 | `Custom` | `setCustomType()` 设置了自定义函数后的类型 | 可以由 `type()` 返回，不能传给 `setType()` |
| 枚举计数 | `NCurveTypes`（48） | 表示枚举范围末尾的计数值，不是一条可执行的曲线 | 不要传给构造函数、`setType()` 或动画 API |

### 10.2 构造、类型与参数

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QEasingCurve(Type type = Linear)` | 创建指定内置类型的曲线 | `Custom` 不应通过该构造函数使用；自定义函数用 `setCustomType()` |
| 构造 | `QEasingCurve(const QEasingCurve &other)` | 拷贝曲线配置 | 拷贝的是值语义配置，不共享业务生命周期 |
| 构造 | `QEasingCurve(QEasingCurve &&other)` | 移动构造曲线 | 移动源不要继续当作原曲线使用 |
| 析构 | `~QEasingCurve()` | 销毁曲线值对象 | 不拥有动画对象或外部函数指针资源 |
| 查询 | `Type type() const` | 返回当前曲线类型 | 自定义函数曲线返回 `Custom` |
| 设置 | `void setType(Type type)` | 设置内置曲线类型 | 不要传 `Custom`；设置类型后重新考虑专用参数和 spline 数据 |
| 查询 | `qreal amplitude() const` | 读取 bounce/elastic 的幅度 | 只对对应曲线有意义 |
| 设置 | `void setAmplitude(qreal amplitude)` | 设置 bounce/elastic 的幅度 | 值越大，回弹或弹簧峰值越高 |
| 查询 | `qreal overshoot() const` | 读取 Back 曲线超调参数 | 只对四种 `Back` 曲线有意义 |
| 设置 | `void setOvershoot(qreal overshoot)` | 设置 Back 曲线超调 | `0` 表示无超调；默认值为 `1.70158` |
| 查询 | `qreal period() const` | 读取 Elastic 曲线周期 | 只对四种 `Elastic` 曲线有意义 |
| 设置 | `void setPeriod(qreal period)` | 设置 Elastic 曲线周期 | 周期越小频率越高，周期越大频率越低 |

### 10.3 计算与自定义 spline

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 计算 | `qreal valueForProgress(qreal progress) const` | 把输入进度映射为有效进度 | 输入按 `0..1` 使用；输出允许超出 `0..1` |
| 自定义函数 | `void setCustomType(EasingFunction func)` | 设置用户自定义进度函数 | `func` 不能为 `nullptr`；调用后 `type()` 为 `Custom` |
| 查询 | `EasingFunction customType() const` | 返回当前自定义函数指针 | 当前类型不是 `Custom` 时返回空指针 |
| Bezier | `void addCubicBezierSegment(const QPointF &c1, const QPointF &c2, const QPointF &endPoint)` | 向 Bezier spline 添加一个三次曲线段 | 仅适用于 `BezierSpline`；曲线隐式从 `(0,0)` 开始并应以 `(1,1)` 结束 |
| TCB | `void addTCBSegment(const QPointF &nextPoint, qreal t, qreal c, qreal b)` | 向 TCB spline 添加一个曲线段 | 仅适用于 `TCBSpline`；t/c/b 均在 `-1..1` |
| 查询 | `QList<QPointF> toCubicSpline() const` | 返回定义自定义 Bezier 曲线的点列表 | 非 Bezier 自定义曲线时返回空列表 |

### 10.4 值语义、比较与数据流

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 交换 | `void swap(QEasingCurve &other)` | 快速交换两个曲线对象 | 不抛出异常；两者的全部曲线配置都会交换 |
| 赋值 | `QEasingCurve &operator=(const QEasingCurve &other)` | 拷贝赋值 | 保持值语义，目标原配置被替换 |
| 赋值 | `QEasingCurve &operator=(QEasingCurve &&other)` | 移动赋值 | 移动源进入可析构或重新赋值状态 |
| 比较 | `operator==(lhs, rhs)` | 比较类型及曲线属性是否相同 | 不只是比较 `type()` |
| 比较 | `operator!=(lhs, rhs)` | 判断两条曲线配置是否不同 | 与 `operator==` 成对使用 |
| 序列化 | `operator<<(QDataStream &, const QEasingCurve &)` | 把曲线写入 Qt 数据流 | 需要自行管理数据流版本和跨版本兼容 |
| 反序列化 | `operator>>(QDataStream &, QEasingCurve &)` | 从 Qt 数据流读取曲线 | 检查数据流状态，不要把不可信字节流直接当作配置 |

## 11. 一句话总结

`QEasingCurve` 把 `0..1` 的时间进度映射成更自然的有效进度；先选 In/Out 语义，再根据曲线类型使用 amplitude、period、overshoot 或自定义 spline，并牢记返回值可能越界。
