# QGradient：渐变的公共状态与绘制策略

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QGradient>`

## 它解决什么问题

渐变不仅是一组颜色，还需要回答几个相互独立的问题：

- 颜色在哪些相对位置出现；
- 渐变是线性、径向还是锥形；
- 几何坐标相对于逻辑坐标、对象边界还是设备边界；
- 超出定义区间后是延伸、重复还是镜像；
- 相邻颜色采用哪种插值方式。

`QGradient` 保存这些渐变共有的状态。真正的几何形状由三个派生值类型提供：

- `QLinearGradient`：沿一条轴变化；
- `QRadialGradient`：从圆心或焦点向外变化；
- `QConicalGradient`：围绕中心按角度变化。

通常直接构造具体派生类，再将它交给 `QBrush` 或 `QPainter`。默认构造的 `QGradient` 类型为 `NoGradient`，它不是一个可以表达具体几何形状的通用“渐变生成器”。

## 实际使用场景

- 为图形、路径、文本或控件背景创建线性、径向、锥形填充。
- 让同一个渐变随每个对象的包围矩形自动缩放。
- 使用预设渐变快速建立主题色、状态色或数据可视化色带。
- 通过多个 stop 制作透明度过渡、硬边色带和非均匀颜色变化。
- 设置重复或镜像延展，形成条纹、光晕或周期性纹理。

`QGradient` 是值类型，不拥有 `QPainter`、`QBrush` 或绘制设备。把它传给 `QBrush` 时，画刷保存渐变状态；之后修改原对象不会作为“实时绑定”自动更新已有画刷。

## 基本使用

```cpp
#include <QLinearGradient>
#include <QPainter>

void paintBadge(QPainter &painter, const QRectF &rect)
{
    QLinearGradient gradient(QPointF(0.0, 0.0), QPointF(1.0, 1.0));
    gradient.setCoordinateMode(QGradient::ObjectMode);
    gradient.setColorAt(0.0, QColor("#1f6feb"));
    gradient.setColorAt(0.55, QColor("#55c2a4"));
    gradient.setColorAt(1.0, QColor("#ffd166"));

    painter.fillRect(rect, QBrush(gradient));
}
```

这里使用 `ObjectMode`，所以 `(0, 0)` 和 `(1, 1)` 分别映射到每个被绘制对象包围矩形的左上角和右下角。同一渐变可自然适配不同大小的矩形。

## Stop：颜色过渡的关键帧

`QGradientStop` 是 `std::pair<qreal, QColor>`，第一项是 `[0, 1]` 内的位置，第二项是颜色；`QGradientStops` 是 stop 列表。

```cpp
QGradientStops stops{
    {0.0, Qt::black},
    {0.35, QColor(20, 120, 255)},
    {1.0, Qt::white}
};
gradient.setStops(stops);
```

需要注意：

- `setColorAt(position, color)` 添加或更新单个位置的颜色；
- `setStops()` 会**替换全部**现有 stop；
- 传给 `setStops()` 的位置必须在 `[0, 1]` 内，并按位置升序排列；
- 没有显式 stop 时，渲染使用位置 0 的黑色到位置 1 的白色；
- `stops()` 返回实际保存的 stop 列表；默认黑白过渡是渲染回退规则，不等于对象内部一定保存了两项。

重复位置可用于制造突变边界，但结果还会受绘制后端、抗锯齿和缩放影响。若需要像素级硬边，应在目标设备上验证。

## 坐标模式

坐标模式决定派生渐变的点、中心、半径等数值在哪个坐标系中解释。

| 模式 | 坐标语义 | 适合场景 |
| --- | --- | --- |
| `LogicalMode` | 使用当前画家的逻辑坐标，默认值 | 需要渐变与场景或路径坐标严格对齐 |
| `ObjectMode` | `(0,0)` 到 `(1,1)` 映射到当前对象包围矩形 | 同一渐变适配不同大小对象 |
| `StretchToDeviceMode` | `(0,0)` 到 `(1,1)` 映射到整个绘制设备 | 跨多个对象保持整幅画布级渐变 |
| `ObjectBoundingMode` | 与 `ObjectMode` 类似，但画刷变换在逻辑空间应用 | 已弃用；新代码不要使用 |

`ObjectMode` 依赖“正在绘制对象”的包围矩形，因此同一画刷分别绘制两个对象时，每个对象会得到各自缩放后的渐变。`StretchToDeviceMode` 则绑定设备范围，窗口或图片尺寸改变时视觉比例也会改变。

坐标模式只解释几何数据，不替你设置渐变轴、中心或半径。应在 `QLinearGradient`、`QRadialGradient` 或 `QConicalGradient` 上设置这些参数。

## Spread：定义区间之外怎样填充

| 模式 | 区间外行为 |
| --- | --- |
| `PadSpread` | 使用最近 stop 的颜色继续填充，默认值 |
| `RepeatSpread` | 周期性重复完整渐变 |
| `ReflectSpread` | 镜像往返重复，避免每个周期首尾直接跳变 |

`Spread` 只对线性和径向渐变有效。锥形渐变天然覆盖完整的 0 到 360 度，调用 `setSpread()` 不会改变其绘制效果。

## 插值模式

Qt 6.11.1 的公开头文件提供：

- `ColorInterpolation`：默认策略，按颜色语义完成 stop 间过渡；
- `ComponentInterpolation`：分别按颜色分量进行插值。

透明或半透明 stop 在两种策略下可能产生不同的中间颜色。选择模式时应以目标视觉效果为准，并在实际使用的 raster、OpenGL、RHI 或打印后端上验证。`setInterpolationMode()` 只改变 stop 之间的颜色计算，不改变 stop、坐标模式或渐变几何。

## 预设渐变

`QGradient::Preset` 提供一组来自 webgradients.com 的预定义渐变，例如 `WarmFlame`、`NightFade`、`JuicyPeach`、`DeepBlue` 和 `PerfectBlue`。枚举数量很大，使用时按名称选择即可，没有必要把每个名称当成不同 API 学习。

```cpp
QGradient preset(QGradient::JuicyPeach);
QBrush brush(preset);
```

预设构造函数同时设置预定义的颜色、方向和 stop，并把坐标模式设为 `ObjectMode`，所以可以适配任意对象尺寸。若设计要求稳定的品牌颜色，不应假定预设内容永远等同于外部网站当前版本；可读取 `stops()` 后固化为项目自己的色值。

## 类型与复制边界

`type()` 返回 `LinearGradient`、`RadialGradient`、`ConicalGradient` 或 `NoGradient`。类型由实际构造方式决定，不应通过对基类做不安全强制转换来猜测派生类型。

`QGradient` 及其派生类型是普通值对象，可以复制和比较。比较运算检查渐变状态是否相等，不是“渲染后肉眼看起来是否相同”的比较。两个参数不同的渐变可能在某个特定小区域内偶然呈现相同像素，也仍然是不相等的。

## 常见错误

- 默认构造 `QGradient` 后期待它自动成为线性渐变；默认类型是 `NoGradient`。
- 将 stop 位置写成百分数 `50`；正确范围是 `0.0` 到 `1.0`。
- 给 `setStops()` 传入未排序列表，或误以为它会在旧 stop 基础上追加。
- 看到 `stops()` 为空就认为不会绘制；空 stop 使用默认黑到白过渡。
- 在 `LogicalMode` 下使用 `(0,0)` 到 `(1,1)`，结果只在一个逻辑单位内完成渐变。
- 对锥形渐变设置 `RepeatSpread` 或 `ReflectSpread` 并期待变化。
- 新代码继续使用已弃用的 `ObjectBoundingMode`。
- 混淆对象边界与设备边界，导致多个图元各自渐变或整幅画布渐变与预期相反。
- 修改原渐变后期待已构造的 `QBrush` 自动同步。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 别名 | `QGradientStop` | `std::pair<qreal, QColor>`；位置必须在 `[0, 1]` 内。 |
| 别名 | `QGradientStops` | `QList<QGradientStop>`；传给 `setStops()` 时需按位置升序。 |
| 类型 | `Type` | `LinearGradient`、`RadialGradient`、`ConicalGradient`、`NoGradient`。 |
| 类型 | `Spread` | `PadSpread`、`ReflectSpread`、`RepeatSpread`；只影响线性和径向渐变。 |
| 类型 | `CoordinateMode` | `LogicalMode`、`StretchToDeviceMode`、`ObjectMode`，以及已弃用的 `ObjectBoundingMode`。 |
| 类型 | `InterpolationMode` | `ColorInterpolation` 或 `ComponentInterpolation`；控制 stop 之间的颜色计算。 |
| 类型 | `Preset` | 大型预设渐变枚举；代表预定义几何与颜色组合，`NumPresets` 是计数哨兵而非视觉预设。 |
| 构造 | `QGradient()` | 构造 `NoGradient`；默认 spread 为 `PadSpread`，坐标模式为 `LogicalMode`，插值模式为 `ColorInterpolation`。 |
| 构造 | `QGradient(Preset preset)` | 按预设构造渐变，并使用 `ObjectMode` 适配对象边界。 |
| 析构 | `~QGradient()` | 销毁值对象；不拥有画家、设备或已由其他对象复制的画刷状态。 |
| 类型查询 | `type() const` | 返回当前渐变几何类型。 |
| 延展 | `setSpread(Spread spread)` | 设置定义区间外的填充规则；对锥形渐变无效果。 |
| 延展 | `spread() const` | 返回延展规则；默认 `PadSpread`。 |
| Stop | `setColorAt(qreal pos, const QColor &color)` | 设置单个 stop；`pos` 必须位于 `[0, 1]`。 |
| Stop | `setStops(const QGradientStops &stops)` | 替换全部 stop；位置必须有效且升序排列。 |
| Stop | `stops() const` | 返回保存的 stop；空列表绘制时仍有默认黑白过渡。 |
| 坐标 | `coordinateMode() const` | 返回坐标解释方式；默认 `LogicalMode`。 |
| 坐标 | `setCoordinateMode(CoordinateMode mode)` | 切换坐标解释方式；不会改写已有几何数值。 |
| 插值 | `interpolationMode() const` | 返回当前颜色插值模式；默认 `ColorInterpolation`。 |
| 插值 | `setInterpolationMode(InterpolationMode mode)` | 设置颜色插值策略；不改变 stop 和几何。 |
| 比较 | `operator==(const QGradient &gradient) const` | 比较渐变状态是否相等，不做视觉近似判断。 |
| 比较 | `operator!=(const QGradient &gradient) const` | `operator==` 的逻辑取反。 |

## 相关类

- `QLinearGradient`：定义起点和终点。
- `QRadialGradient`：定义中心、半径与焦点。
- `QConicalGradient`：定义中心和起始角。
- `QBrush`：把渐变变成可供 `QPainter` 使用的填充样式。
- `QPainter`：实际绘制渐变画刷。

使用 `QGradient` 时，最重要的是把 stop、几何类型和坐标模式分开思考。颜色正确但坐标模式错误，通常正是“渐变看起来像纯色或位置不对”的根源。
