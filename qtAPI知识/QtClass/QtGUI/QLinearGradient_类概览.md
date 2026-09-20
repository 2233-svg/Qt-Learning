# QLinearGradient：沿直线插值的画刷渐变

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QLinearGradient>`  
> 模块：`Qt6::Gui`  
> 继承：`QGradient`  
> 常用协作类型：`QBrush`、`QPainter`、`QColor`、`QGradientStops`

`QLinearGradient` 描述一条从起点到终点的颜色插值轴。它本身不是绘图设备，也不会自动画到窗口上；把它交给 `QBrush` 或直接作为画刷传给 `QPainter`，才会在填充图形时产生渐变。

## 它解决的问题

纯色画刷只能在一个区域使用一种颜色。需要表达深浅过渡、状态层次、进度背景、天际线或仪表盘色带时，可以用线性渐变在两点之间平滑插值多个色标。

`QLinearGradient` 适合：

- 为 `QPainter::fillRect()`、`drawPath()`、`drawRoundedRect()` 提供填充画刷。
- 自定义 `QWidget::paintEvent()` 中绘制按钮、卡片、图表背景或选中状态。
- 通过 `QPalette`、样式或 `QBrush` 向模型/视图/文本格式传递渐变。
- 在较大区域重复、反射或延展一条颜色带。

它不适合：

- 需要从中心向外扩散的效果：使用 `QRadialGradient`。
- 需要围绕中心旋转的色相环：使用 `QConicalGradient`。
- 需要精确控制每个像素的图像处理：使用 `QImage`、着色器或自定义绘制算法。

## 最小绘制示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui Widgets)
target_link_libraries(my_app PRIVATE Qt6::Gui Qt6::Widgets)
```

```cpp
#include <QLinearGradient>
#include <QPainter>
#include <QWidget>

void Panel::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    const QRectF area = rect();

    QLinearGradient gradient(area.topLeft(), area.bottomRight());
    gradient.setColorAt(0.0, QColor("#1677ff"));
    gradient.setColorAt(0.55, QColor("#2fbf9b"));
    gradient.setColorAt(1.0, QColor("#f5c542"));

    painter.fillRect(area, gradient);
}
```

`setColorAt()` 来自基类 `QGradient`。位置是渐变轴上的归一化比例：`0.0` 对应起点，`1.0` 对应终点；中间值表示两者之间的位置。

## 起点、终点与色标是三件事

线性渐变的结果由三个独立维度决定：

1. `start()` / `setStart()`：颜色轴的起点。
2. `finalStop()` / `setFinalStop()`：颜色轴的终点。
3. `QGradient::setColorAt()` 或 `setStops()`：轴上每个比例位置的颜色。

```cpp
QLinearGradient gradient(QPointF(0, 0), QPointF(240, 0));
gradient.setColorAt(0.0, Qt::black);
gradient.setColorAt(0.5, QColor("#5468ff"));
gradient.setColorAt(1.0, Qt::white);
```

这段代码定义的是从左到右的渐变方向，而不是一个固定宽度为 240 像素的“图片”。渐变最终如何映射到设备，还受 `QGradient` 的坐标模式与 `QPainter` 的变换影响。

若完全不设置色标，Qt 使用从位置 0 的黑色到位置 1 的白色的默认渐变。因此“画出来但颜色不对”时，第一步应检查是否确实调用了 `setColorAt()` 或 `setStops()`。

## 坐标模式决定端点如何解释

端点默认使用 `QGradient::LogicalMode`。在这种模式下，`QLinearGradient` 的点位于绘图逻辑坐标系，会随 `QPainter` 的缩放、旋转和平移一起变化。构造函数文档说明传入的数值通常按像素设计，但绘制过程中仍应把它们理解为当前绘图坐标中的位置。

对需要随被填充对象缩放的渐变，可选择对象坐标模式：

```cpp
QLinearGradient gradient(0.0, 0.0, 1.0, 0.0);
gradient.setCoordinateMode(QGradient::ObjectMode);
gradient.setColorAt(0.0, QColor("#20304f"));
gradient.setColorAt(1.0, QColor("#67d4c1"));

painter.fillRect(targetRect, gradient);
```

`ObjectMode` 将坐标解释为目标对象包围框中的比例，通常用 `0..1` 表达左、上、右、下，因此同一份渐变可以用于不同尺寸的矩形。它适合卡片、列表行和可缩放 SVG 风格图形。

不要把两种模式混用：在 `ObjectMode` 下仍传 `(0, 0)` 到 `(300, 0)`，渐变会延伸到目标对象范围之外，视觉上常表现为几乎单色。

## 超出起止点时：`spread()`

只在起点和终点之间插值还不够，填充区域常常比渐变轴更大。继承自 `QGradient` 的 `setSpread()` 决定轴外区域怎么着色：

| 扩展方式 | 轴外效果 | 合适场景 |
| --- | --- | --- |
| `PadSpread` | 延用两端颜色，默认值 | 普通背景、按钮与大多数 UI 填充 |
| `RepeatSpread` | 周期性重复整段渐变 | 条纹、标尺或装饰性色带 |
| `ReflectSpread` | 来回镜像重复渐变 | 避免重复边界发生突变的往返色带 |

```cpp
QLinearGradient stripe(0, 0, 16, 0);
stripe.setColorAt(0.0, QColor("#e7edf6"));
stripe.setColorAt(0.5, QColor("#ffffff"));
stripe.setColorAt(1.0, QColor("#e7edf6"));
stripe.setSpread(QGradient::RepeatSpread);
```

`RepeatSpread` 与 `ReflectSpread` 会随坐标、缩放和绘制区域呈现明显密度变化。若条纹宽度必须恒定，使用逻辑坐标并谨慎管理 `QPainter` 的缩放变换。

## 构造后修改方向

交互式组件需要跟随尺寸调整时，先保留色标，再更新端点即可：

```cpp
void HeaderWidget::resizeEvent(QResizeEvent *event)
{
    QWidget::resizeEvent(event);

    m_gradient.setStart(0.0, 0.0);
    m_gradient.setFinalStop(width(), 0.0);
}
```

`setStart()` 与 `setFinalStop()` 都有 `QPointF` 以及两个 `qreal` 参数的重载。它们只修改轴端点，不会清空已有色标、扩展方式、插值模式或坐标模式。

默认构造的渐变插值区为 `(0, 0)` 到 `(1, 1)`。这对临时对象和单位坐标场景可用，但在常规像素坐标绘制中往往太短，会使 `PadSpread` 迅速铺满终点色；生产代码通常应显式设置端点或使用 `ObjectMode`。

## 值语义、绘制边界与性能

`QLinearGradient` 是无 parent、无事件循环依赖的值类型。可以作为成员保存，或在 `paintEvent()` 中临时创建；它不拥有 `QPainter`，也不管理任何窗口资源。

- 仅在创建并使用 `QPainter` 的目标对象所属线程中绘制。GUI 控件的 `paintEvent()` 必须在 GUI 线程执行。
- 纯粹构造和配置渐变不等于绘制；后台线程可准备独立的值数据，但不要在后台线程触碰 `QWidget` 或跨线程共用可变对象。
- 每帧设置少量色标通常没有问题。高频动画中，避免每次绘制都构造复杂的 `QGradientStops`、解析颜色字符串或反复分配容器。
- 若要缓存画刷，缓存策略必须把尺寸、设备像素比、坐标模式和 painter transform 的影响考虑进去；缓存错维度常比不缓存更难排查。

## 常见错误

1. **创建了渐变却没有用于画刷。** `QLinearGradient` 只是描述；要传给 `fillRect()`、`setBrush()` 或 `QBrush`。
2. **只设置端点，没设置色标。** 会使用黑到白的默认色标。
3. **以为端点是色标位置。** 端点决定方向和插值轴，色标位置仍然是 `0..1` 比例。
4. **忘记默认 `PadSpread`。** 轴外不是透明，而是保持起点或终点颜色。
5. **在 `ObjectMode` 使用像素端点。** 该模式通常用 `0..1`；像素数会使大部分区域落在轴外。
6. **把渐变旋转问题归因于色标。** 先检查 `QPainter::rotate()`、坐标模式与端点方向。
7. **在工作线程绘制 QWidget。** 渐变值可准备，但控件绘制仍必须回到 GUI 线程。

## API 速查表

| API | 作用 | 使用时的语义与边界 |
| --- | --- | --- |
| `QLinearGradient()` | 构造默认线性渐变。 | 默认插值区为 `(0, 0)` 到 `(1, 1)`；在普通像素坐标中通常需要重新设定端点。 |
| `QLinearGradient(const QPointF &start, const QPointF &finalStop)` | 以两个点构造渐变轴。 | 参数用于定义插值方向与范围；文档期望常规输入按像素设计，实际映射还受坐标模式与 painter transform 影响。 |
| `QLinearGradient(qreal x1, qreal y1, qreal x2, qreal y2)` | 以四个坐标构造渐变轴。 | 与点版本等价，适合端点来自布局计算时直接使用。 |
| `start()` | 返回起点。 | 返回当前逻辑坐标中的 `QPointF`；不是第一个色标的位置。 |
| `setStart(const QPointF &start)` | 设置起点。 | 保留色标、扩展方式和其他基类设置；会改变渐变方向。 |
| `setStart(qreal x, qreal y)` | 以坐标设置起点。 | 是上项的便利重载；适合 `width()`、`height()` 等数值。 |
| `finalStop()` | 返回终点。 | 返回当前逻辑坐标中的 `QPointF`；不是最后一个色标的位置。 |
| `setFinalStop(const QPointF &stop)` | 设置终点。 | 仅改变插值轴终点；起终点相同的视觉结果通常不具备有意义的线性方向。 |
| `setFinalStop(qreal x, qreal y)` | 以坐标设置终点。 | 是点版本的便利重载。 |
| `QGradient::setColorAt(qreal pos, const QColor &color)` | 在比例位置设置单个色标。 | `pos` 应按 `0..1` 设计；重复调用同一位置会覆盖该位置颜色。 |
| `QGradient::setStops(const QGradientStops &stops)` | 一次设置完整色标表。 | 适合动态主题或批量更新；替换现有全部色标。 |
| `QGradient::stops()` | 取得当前完整色标表。 | 用于检查或复制配置；没有显式色标时要注意默认黑到白效果。 |
| `QGradient::setSpread(Spread)` / `spread()` | 设置或查询轴外扩展方式。 | 默认 `PadSpread`；重复或反射模式对坐标缩放敏感。 |
| `QGradient::setCoordinateMode(CoordinateMode)` / `coordinateMode()` | 设置或查询坐标解释方式。 | `LogicalMode` 跟随绘图坐标；`ObjectMode` 常用 `0..1`；切换后需同步检查端点。 |
| `QGradient::setInterpolationMode(InterpolationMode)` | 设置颜色插值空间。 | 影响不同色标间的观感；与端点方向和扩展方式是独立问题。 |
| `QGradient::type()` | 返回渐变类型。 | 对本类返回线性渐变类型；多态处理 `QGradient` 时可据此分支。 |

## 一句话总结

`QLinearGradient` 用起点和终点定义方向，用色标定义颜色，用 `QBrush`/`QPainter` 负责实际绘制；显示异常时依次检查色标、坐标模式、端点和扩展方式。
