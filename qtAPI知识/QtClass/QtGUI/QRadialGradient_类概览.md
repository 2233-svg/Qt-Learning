# QRadialGradient：以圆形几何定义颜色渐变

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QRadialGradient>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QGradient -> QRadialGradient`

`QRadialGradient` 描述一个径向渐变，通常和 `QBrush` 一起交给 `QPainter` 使用。颜色沿着从焦点到圆周的径向方向插值，适合光晕、按钮高光、圆形仪表、背景聚焦和带中心辐射效果的图形。

它只描述渐变参数，不直接绘制像素：

```cpp
QRadialGradient gradient(QPointF(80, 60), 60);
gradient.setColorAt(0.0, QColor("#ffffff"));
gradient.setColorAt(0.65, QColor("#55aaff"));
gradient.setColorAt(1.0, QColor("#123060"));

QPainter painter(this);
painter.fillRect(rect(), QBrush(gradient));
```

## 它解决的问题

相比手工逐圈绘制，`QRadialGradient` 把以下内容交给 Qt 的绘制后端：

- 以一个中心圆和焦点定义颜色传播方向。
- 在 0 到 1 的 stop 位置之间插值颜色。
- 处理渐变区域之外的填充、重复或镜像。
- 根据逻辑坐标、设备坐标或对象包围盒解释几何。
- 在 `QBrush` 中和其他画刷、变换及 `QPainter` 状态组合。

`QRadialGradient` 不保存目标控件尺寸，也不自动适配窗口大小。窗口尺寸变化时，要么使用对象坐标模式，要么重新设置几何。

## 简单径向渐变与扩展径向渐变

### 简单径向渐变

简单模式有一个中心圆，颜色从焦点向中心圆边缘传播。常用构造函数只需要中心和半径：

```cpp
QRadialGradient gradient(QPointF(100, 100), 80);
```

此时焦点在中心。如果传入一个在圆外的焦点，Qt 会沿中心到焦点的连线，把焦点重新调整到圆周上的交点。

### 扩展径向渐变

扩展模式同时有中心圆和焦点圆：

```cpp
QRadialGradient gradient(
    QPointF(100, 100), 80.0,
    QPointF(70, 80), 12.0);
```

它可以表达不在中心的焦点和有半径的光源区域。两圆定义的锥形之外的点会是透明的。焦点在扩展模式下可以位于中心圆之外，但半径和两圆关系仍应根据实际绘制效果验证。

## 颜色 stop 的语义

stop 位置是归一化的 `qreal`，通常位于 `[0, 1]`：

- `0` 表示渐变起点，径向渐变中对应焦点/焦点圆一侧。
- `1` 表示渐变终点，通常对应中心圆外缘。
- 中间位置按 stop 之间的规则插值。

没有设置 stop 时，`QGradient` 使用黑色在 0、白色在 1 的默认渐变。`setStops()` 会整体替换当前 stop 集合，不是追加；传入的 stop 位置必须按从小到大排序。

```cpp
gradient.setStops({
    {0.0, Qt::white},
    {0.35, QColor(255, 220, 120)},
    {1.0, Qt::transparent}
});
```

渐变区域外的颜色由 `QGradient::Spread` 决定：

- `PadSpread`：使用最近 stop 颜色，默认值。
- `RepeatSpread`：重复渐变。
- `ReflectSpread`：镜像重复渐变。

## 坐标模式

`QGradient` 默认使用 `LogicalMode`，此时中心、焦点和半径使用与绘制对象相同的逻辑坐标。

| 模式 | 几何解释 |
| --- | --- |
| `LogicalMode` | 与对象绘制坐标相同，默认 |
| `StretchToDeviceMode` | 相对于 paint device 包围盒，左上为 `(0,0)`、右下为 `(1,1)` |
| `ObjectMode` | 相对于被绘制对象包围盒，左上为 `(0,0)`、右下为 `(1,1)` |
| `ObjectBoundingMode` | 类似对象包围盒模式，但 brush transform 在逻辑空间应用；已弃用 |

对于随控件尺寸变化的背景，`ObjectMode` 通常比硬编码像素中心更合适：

```cpp
QRadialGradient gradient(QPointF(0.5, 0.4), 0.6);
gradient.setCoordinateMode(QGradient::ObjectMode);
```

半径同样按所选坐标空间解释；不要只把中心改成归一化坐标，却继续把半径当像素使用。

## 几何值与半径边界

`center()`、`focalPoint()`、`centerRadius()` 和 `focalRadius()` 返回逻辑坐标中的值。`radius()` 是 `centerRadius()` 的别名，`setRadius()` 是 `setCenterRadius()` 的别名。

Qt 的接口不会把所有半径错误都转化为异常。业务上应使用非负、有限的半径；零半径会退化成没有有效面积的渐变，负值、NaN 或无穷值可能产生依赖绘制后端的结果。

设置焦点、中心或半径后，已经创建的 `QBrush` 是一个值对象副本，之前从 gradient 构造的 brush 不会神奇地反映之后的修改。修改 gradient 后重新构造 `QBrush` 或重新设置画刷：

```cpp
QBrush brush(gradient);
gradient.setRadius(120);
brush = QBrush(gradient); // 使用新几何
```

## 与 `QBrush` 和 `QPainter` 协作

```cpp
void Widget::paintEvent(QPaintEvent *)
{
    QRadialGradient gradient(rect().center(), rect().width() * 0.5);
    gradient.setColorAt(0.0, QColor(255, 255, 255, 220));
    gradient.setColorAt(1.0, QColor(0, 80, 160, 255));

    QPainter painter(this);
    painter.setBrush(QBrush(gradient));
    painter.setPen(Qt::NoPen);
    painter.drawEllipse(rect().adjusted(4, 4, -4, -4));
}
```

渐变坐标还会受到 `QBrush::transform()`、`QPainter` 的世界变换和坐标模式影响。出现位置偏移时，应按“渐变几何 -> coordinate mode -> brush transform -> painter transform”的顺序排查。

## 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

```cpp
#include <QRadialGradient>
#include <QBrush>
#include <QPainter>
```

`<QRadialGradient>` 是 Qt 提供的导出头，实际类声明位于 GUI 的画刷相关头文件中。

## API 逐项说明

### 构造、析构和几何

#### `QRadialGradient::QRadialGradient()`

构造简单径向渐变，中心和焦点都是 `(0, 0)`，半径为 `1`。

#### `QRadialGradient::QRadialGradient(const QPointF &center, qreal radius)`

构造简单径向渐变，指定中心和半径，焦点位于中心。

#### `QRadialGradient::QRadialGradient(qreal cx, qreal cy, qreal radius)`

上一个构造函数的坐标便捷形式。`cx`、`cy` 和 `radius` 都使用逻辑坐标。

#### `QRadialGradient::QRadialGradient(const QPointF &center, qreal radius, const QPointF &focalPoint)`

构造简单径向渐变，指定中心、半径和焦点。若焦点在中心圆外，Qt 会沿中心到焦点的连线把它调整到圆内/圆周有效位置。

#### `QRadialGradient::QRadialGradient(qreal cx, qreal cy, qreal radius, qreal fx, qreal fy)`

指定中心坐标、半径和焦点坐标的简单渐变构造函数。

#### `QRadialGradient::QRadialGradient(const QPointF &center, qreal centerRadius, const QPointF &focalPoint, qreal focalRadius)`

构造扩展径向渐变，同时指定中心圆、焦点圆和两者半径。焦点可以处于中心圆之外；两圆定义的锥形之外是透明区域。

#### `QRadialGradient::QRadialGradient(qreal cx, qreal cy, qreal centerRadius, qreal fx, qreal fy, qreal focalRadius)`

扩展径向渐变的坐标便捷构造函数。参数顺序中第三个半径是中心半径，最后一个是焦点半径。

#### `QRadialGradient::~QRadialGradient()`

销毁渐变值对象。它不拥有 `QPainter`、`QBrush` 或 paint device。

#### `QPointF QRadialGradient::center() const`

返回渐变中心，使用当前 gradient 坐标空间的逻辑坐标。

#### `void QRadialGradient::setCenter(const QPointF &center)`

设置渐变中心。它只修改 gradient 对象；已经由它构造出的 `QBrush` 不会自动更新。

#### `void QRadialGradient::setCenter(qreal x, qreal y)`

按两个坐标设置中心的便捷重载。

#### `QPointF QRadialGradient::focalPoint() const`

返回焦点位置，使用逻辑坐标。简单渐变的焦点可能已经按 Qt 规则从外部位置调整。

#### `void QRadialGradient::setFocalPoint(const QPointF &focalPoint)`

设置焦点位置。简单径向渐变中，绘制时/设置时若焦点在中心圆外，Qt 会按简单模式规则调整。

#### `void QRadialGradient::setFocalPoint(qreal x, qreal y)`

按两个坐标设置焦点的便捷重载。

#### `qreal QRadialGradient::radius() const`

返回中心半径，等价于 `centerRadius()`。

#### `void QRadialGradient::setRadius(qreal radius)`

设置中心半径，等价于 `setCenterRadius(radius)`。半径应使用非负、有限值。

#### `qreal QRadialGradient::centerRadius() const`

返回中心圆半径，单位取决于当前 coordinate mode。

#### `void QRadialGradient::setCenterRadius(qreal radius)`

设置中心圆半径。它不会修改焦点位置或焦点半径。

#### `qreal QRadialGradient::focalRadius() const`

返回扩展径向渐变的焦点圆半径。简单径向渐变通常使用零焦点半径语义。

#### `void QRadialGradient::setFocalRadius(qreal radius)`

设置焦点圆半径。扩展渐变中应结合中心半径、焦点位置和绘制后端验证结果；普通简单光晕一般保持为零。

### 继承自 `QGradient` 的类型

#### `QGradient::Type`

渐变类型枚举。对 `QRadialGradient` 调用 `type()` 应得到 `QGradient::RadialGradient`。

#### `QGradient::Spread`

渐变区域外的填充策略：`PadSpread`、`ReflectSpread` 和 `RepeatSpread`。

#### `QGradient::CoordinateMode`

定义渐变坐标映射到 paint device、对象包围盒或逻辑空间的方式。

#### `QGradient::InterpolationMode`

定义颜色插值模式。默认是 `ColorInterpolation`；通过 `setInterpolationMode()` 修改时，应在目标平台和目标视觉效果上验证颜色过渡。

#### `QGradient::QGradientStop`

stop 的类型别名，本质上是 `std::pair<qreal, QColor>`，保存位置和颜色。

#### `QGradient::QGradientStops`

stop 列表类型别名，本质上是 `QList<QGradientStop>`。

#### `QGradient::Type QGradient::type() const`

返回渐变类型。对该类返回 `RadialGradient`。

#### `QGradient::CoordinateMode QGradient::coordinateMode() const`

返回坐标模式，默认是 `LogicalMode`。

#### `void QGradient::setCoordinateMode(QGradient::CoordinateMode mode)`

设置坐标模式。切换到 `ObjectMode` 或设备模式后，中心、焦点和半径的数值会在新的坐标空间中解释。

#### `void QGradient::setColorAt(qreal position, const QColor &color)`

创建或更新一个 stop。`position` 必须位于 `0` 到 `1`。调用它不会清空其他 stop。

#### `QGradientStops QGradient::stops() const`

返回当前 stop 列表。如果没有显式 stop，绘制语义仍使用默认的黑到白渐变。

#### `void QGradient::setStops(const QGradientStops &stopPoints)`

整体替换 stop 列表。位置必须在 `[0,1]` 且按升序排列；它不是追加操作。

#### `QGradient::Spread QGradient::spread() const`

返回区域外的 spread 方式，默认是 `PadSpread`。

#### `void QGradient::setSpread(QGradient::Spread method)`

设置区域外的填充方式。对 radial gradient 有效；对 conical gradient 没有同样的边界语义。

#### `QGradient::InterpolationMode QGradient::interpolationMode() const`

返回颜色插值模式。

#### `void QGradient::setInterpolationMode(QGradient::InterpolationMode mode)`

设置颜色插值模式。该设置影响后续使用此 gradient 的绘制结果。

#### `bool QGradient::operator==(const QGradient &gradient) const`

比较两个 gradient 的配置是否相同，包括类型、几何数据、stops 和相关设置。它不是比较某个目标控件上的最终像素。

#### `bool QGradient::operator!=(const QGradient &gradient) const`

返回两个 gradient 配置是否不同。

## 常见错误排查

1. **渐变位置不随窗口变化**：使用 `ObjectMode`，或在尺寸变化时重新设置中心和半径。
2. **焦点看起来被挪动**：简单径向渐变的外部焦点会被 Qt 调整；扩展渐变才能让焦点位于更自由的位置。
3. **把 `radius()` 当作焦点半径**：`radius()` 是 `centerRadius()` 的别名；扩展渐变的焦点半径使用 `focalRadius()`。
4. **stop 设置后旧颜色还在**：`setStops()` 会替换整个列表；若只想改一个位置，使用 `setColorAt()`。
5. **stop 位置越界或未排序**：位置应在 `[0,1]`，`setStops()` 的列表应升序排列。
6. **渐变外颜色不符合预期**：检查 `spread()`，默认是 `PadSpread`，不是自动重复。
7. **把逻辑坐标和对象归一化坐标混用**：切换 coordinate mode 后中心、焦点和半径都要按新空间解释。
8. **修改 gradient 后已有 brush 没变**：`QBrush` 是值语义，修改后重新构造或重新设置 brush。
9. **半径为负或非有限**：这些值没有有用的几何意义，应在进入 Qt 前校验。
10. **把扩展径向渐变当成普通圆外延伸**：两圆定义的锥形之外可能透明，必要时用 spread 或补充背景。
11. **只在一个后端看过效果**：渐变会受 brush/painter 变换和绘制后端影响，跨平台 UI 要实际验证。

## API 速查表

| 类别 | API | 作用 | 关键边界与注意事项 |
| --- | --- | --- | --- |
| 构造 | `QRadialGradient()` | 创建默认简单径向渐变 | 中心/焦点 `(0,0)`，半径 1 |
| 构造 | `QRadialGradient(QPointF, radius)` | 创建中心焦点相同的简单渐变 | 半径使用逻辑坐标 |
| 构造 | `QRadialGradient(cx, cy, radius)` | 简单渐变坐标便捷构造 | 焦点在中心 |
| 构造 | `QRadialGradient(QPointF, radius, QPointF)` | 指定焦点的简单渐变 | 外部焦点会被调整到有效位置 |
| 构造 | `QRadialGradient(cx, cy, radius, fx, fy)` | 指定中心和焦点坐标 | 参数都按当前逻辑空间解释 |
| 构造 | `QRadialGradient(QPointF, centerRadius, QPointF, focalRadius)` | 创建扩展径向渐变 | 焦点可在中心圆外；锥形外可能透明 |
| 构造 | `QRadialGradient(cx, cy, centerRadius, fx, fy, focalRadius)` | 扩展渐变坐标构造 | 区分中心半径和焦点半径 |
| 几何 | `center()` / `setCenter()` | 读写中心 | 修改后已有 `QBrush` 不自动更新 |
| 几何 | `focalPoint()` / `setFocalPoint()` | 读写焦点 | 简单模式外部焦点会被调整 |
| 几何 | `radius()` / `setRadius()` | 读写中心半径别名 | 等价于 centerRadius API |
| 几何 | `centerRadius()` / `setCenterRadius()` | 读写中心圆半径 | 应为非负有限值 |
| 几何 | `focalRadius()` / `setFocalRadius()` | 读写焦点圆半径 | 主要用于扩展渐变 |
| 类型 | `type()` | 查询渐变类型 | 返回 `RadialGradient` |
| stop | `setColorAt(position, color)` | 添加或更新一个 stop | position 必须在 `[0,1]` |
| stop | `setStops(stops)` | 整体替换 stop 列表 | 要求位置在范围内且升序 |
| stop | `stops()` | 获取当前 stop 列表 | 无 stop 时使用默认黑到白 |
| spread | `spread()` / `setSpread()` | 查询或设置区域外策略 | 默认 Pad；radial 有效 |
| 坐标 | `coordinateMode()` / `setCoordinateMode()` | 设置几何坐标空间 | 切换后所有几何值按新空间解释 |
| 插值 | `interpolationMode()` / `setInterpolationMode()` | 查询或设置颜色插值模式 | 视觉结果应跨后端验证 |
| 比较 | `operator==` / `operator!=` | 比较 gradient 配置 | 不比较最终像素 |
| 协作 | `QBrush(gradient)` | 将 gradient 交给 painter | `QBrush` 是值对象，修改后需重新构造 |
| 绘制 | `QPainter::fillRect` / `drawEllipse` | 使用径向渐变填充或绘制 | 还会受 brush/painter transform 影响 |

### 一句话总结

`QRadialGradient` 只描述径向渐变几何和颜色 stops，真正显示要经过 `QBrush` 和 `QPainter`；牢记简单/扩展模式、焦点调整、stop 范围排序、坐标模式以及 brush 的值语义，渐变效果才会稳定可控。
