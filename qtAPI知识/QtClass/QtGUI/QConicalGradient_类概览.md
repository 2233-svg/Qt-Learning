# Qt QConicalGradient 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QConicalGradient>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QGradient -> QConicalGradient`  
> 定位：围绕中心点按角度插值的圆锥渐变

## 1. 它解决什么问题

`QConicalGradient` 用一个中心点和一个起始角定义颜色随方向变化的渐变。它适合“绕着一个点转一圈”的视觉，而不是沿一条线或从中心向外按半径变化。

常见使用场景包括：

- 仪表盘、旋钮和环形进度控件的彩色刻度；
- 色轮、HSV 色相环和颜色选择器；
- 雷达、扫描、扇区或极坐标式的背景；
- 用 `QPainter` 绘制具有旋转方向感的装饰图形。

它本身只描述渐变参数，真正绘制通常要把它放进 `QBrush`，再交给 `QPainter`、`QWidget`、`QImage` 或其它绘制设备。它不是一个控件，也不会自动刷新界面。

## 2. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

```cpp
#include <QConicalGradient>
#include <QBrush>
#include <QPainter>
```

`QConicalGradient` 是 `QGradient` 的值类型派生类。它不继承 `QObject`，没有父对象和事件循环要求，可以在栈上创建、复制或作为 `QBrush` 的一部分传递。

## 3. 最小可用代码

```cpp
#include <QBrush>
#include <QConicalGradient>
#include <QPainter>

void paintColorWheel(QPainter &painter, const QRectF &rect)
{
    const QPointF center = rect.center();
    QConicalGradient gradient(center, 0.0);
    gradient.setColorAt(0.0, Qt::red);
    gradient.setColorAt(1.0 / 3.0, Qt::green);
    gradient.setColorAt(2.0 / 3.0, Qt::blue);
    gradient.setColorAt(1.0, Qt::red);

    painter.setBrush(QBrush(gradient));
    painter.setPen(Qt::NoPen);
    painter.drawEllipse(rect);
}
```

这里的中心点和角度使用绘制对象的逻辑坐标。`setColorAt()` 的位置是从 `0` 到 `1` 的归一化渐变位置，不是角度值；角度由 `QConicalGradient` 的 `angle` 控制。

## 4. 渐变如何计算

### 4.1 中心点和方向

渐变以 `center` 为旋转中心，从 `angle` 指定的方向开始插值，并沿逆时针方向覆盖完整的 360 度。中心点只决定“绕哪里转”，不决定渐变的半径。

因此，一个圆形绘制区域可以产生完整色轮；一个矩形区域也会根据每个像素相对于中心点的方向取色，矩形外角仍然属于同一个完整角度周期。

### 4.2 stop 点定义颜色

渐变颜色由 `QGradientStop` 组成，也就是“位置 + 颜色”。位置必须位于 `0` 到 `1` 之间。没有设置 stop 时，Qt 使用位置 `0` 为黑色、位置 `1` 为白色的默认渐变。

颜色轮通常需要让位置 `0` 和 `1` 的颜色相同，这样跨过周期边界时不会出现突然跳变：

```cpp
gradient.setColorAt(0.0, QColor::fromHsv(0, 255, 255));
gradient.setColorAt(0.5, QColor::fromHsv(180, 255, 255));
gradient.setColorAt(1.0, QColor::fromHsv(0, 255, 255));
```

`setStops()` 会替换当前全部 stop，而不是追加。若使用它，位置必须按从小到大排序。

### 4.3 `angle` 的单位和范围

构造函数文档要求角度以度为单位，并在 `0` 到 `360` 之间。不要把弧度直接传给构造函数或 `setAngle()`。

将角度写成 `0`、`90`、`180`、`270` 更容易表达设计意图。若角度来自弧度计算，应先转换：

```cpp
const qreal degrees = radians * 180.0 / M_PI;
gradient.setAngle(degrees);
```

项目若需要允许任意用户输入，应在业务层先归一化到文档要求的范围，并处理 `NaN` 或无穷大输入。

## 5. 坐标模式与画刷变换

`QConicalGradient` 继承 `QGradient` 的坐标模式。默认是 `LogicalMode`，即中心点使用与绘制对象相同的逻辑坐标。

当同一个渐变要适配不同大小的对象时，可考虑：

- `ObjectMode`：让渐变坐标相对对象使用；
- `StretchToDeviceMode`：按绘制设备范围拉伸；
- `ObjectBoundingMode`：历史兼容模式，Qt 文档标记为不应在新代码中使用。

坐标模式会改变中心点如何映射到绘制设备。不要在已经使用像素坐标的 `LogicalMode` 下，误把中心点写成 `0.5, 0.5` 就期待它位于对象中心；这种归一化写法需要匹配相应的对象坐标模式和变换策略。

`QBrush` 还可以拥有自己的变换。调试渐变位置时，应同时检查：

1. `QConicalGradient::center()`；
2. `QConicalGradient::angle()`；
3. `QGradient::coordinateMode()`；
4. `QBrush::transform()`；
5. `QPainter` 当前的世界变换。

## 6. `spread` 的特殊边界

`QGradient::setSpread()` 对线性和径向渐变有意义，但对圆锥渐变没有效果。原因是圆锥渐变天生闭合，已经覆盖从 `0` 到 `360` 度的整圈，不存在在线性或径向渐变中那种“渐变区域之外”的方向边界。

因此：

```cpp
gradient.setSpread(QGradient::RepeatSpread);
```

不会让圆锥渐变出现额外的重复效果。要改变圆周上的颜色周期，应调整 stop 点、起始角或画刷/绘制变换。

## 7. 真实使用场景

### 7.1 环形进度或仪表盘

圆锥渐变可以作为整圈底色，但它不会自动根据进度截断。进度环通常还需要配合：

- `QPainterPath` 和弧线；
- `QPen` 的圆帽和宽度；
- 或先绘制渐变图像，再用遮罩限制可见角度。

如果需求是“沿圆周显示一段颜色”，不要只设置 `QConicalGradient` 就认为它会自动产生进度范围。

### 7.2 颜色选择器

色相环可以将红、黄、绿、青、蓝、品红和红色分别放在等距 stop 点。中心点应与色轮几何中心一致，绘制区域变化时要同步更新中心或选择合适的坐标模式。

### 7.3 自定义控件绘制

在 `QWidget::paintEvent()` 中创建渐变并用 `QPainter` 绘制是常见做法。渐变对象是轻量值类型，但如果 stop 点复杂且控件频繁重绘，可以在尺寸或主题变化时重建 `QBrush`，避免每次绘制都重复配置。

## 8. 生命周期、线程与性能

`QConicalGradient`、`QGradient` 和 `QBrush` 都是值语义对象，不依赖 GUI 线程才能创建或修改。它们可以在工作线程中准备，再把值传给绘制线程；但实际使用 `QPainter` 绘制时，仍要遵守绘制设备和 GUI 对象的线程规则。

修改渐变后，已经复制出去的 `QBrush` 是否反映新值取决于复制时的值语义和后续修改对象；稳妥做法是在完成渐变配置后再构造或更新画刷。

它不负责缓存渲染结果。高频动画中，如果只改变起始角，可以保留 stop 配置并更新角度；如果绘制内容固定，也可以考虑缓存到 `QImage`，但要根据设备缩放和抗锯齿需求决定是否值得缓存。

## 9. 常见误区与排查顺序

### 9.1 把 stop 位置当成角度

`setColorAt(0.25, color)` 表示渐变周期的四分之一位置，不是 0.25 度。起始角要通过构造函数或 `setAngle()` 设置。

### 9.2 忘记设置 `QBrush`

创建 `QConicalGradient` 不会直接绘制。必须将它放进 `QBrush`，再调用 `painter.setBrush()` 或把画刷交给使用画刷的 API。

### 9.3 stop 位置不在 0 到 1

位置超出范围会违反 API 契约。对于整圈连续效果，通常显式设置 `0` 和 `1` 两个端点，并让两端颜色一致。

### 9.4 以为 `setSpread()` 会改变圆锥渐变

圆锥渐变已经闭合，`spread` 对它无效。检查无效设置会浪费排查时间。

### 9.5 角度方向理解反了

Qt 文档描述的是沿逆时针方向插值。若视觉方向与设计稿相反，应调整角度、画布变换或 stop 顺序，而不是盲目修改颜色。

## 10. 与相关类型的协作

- `QGradient`：提供 stop、坐标模式、spread 和通用渐变接口。
- `QBrush`：把渐变包装成可交给绘制系统的画刷。
- `QPainter`：使用画刷填充椭圆、路径、矩形或自定义形状。
- `QLinearGradient`：沿起点到终点的线性方向渐变。
- `QRadialGradient`：围绕中心按半径变化的渐变。
- `QColor`：提供每个 stop 的颜色值。

## 11. 逐项 API 说明

### `QConicalGradient::QConicalGradient()`

```cpp
QConicalGradient()
```

**作用：** 创建中心点为 `(0, 0)`、起始角为 `0` 度的圆锥渐变。

**边界：**

- 默认 stop 仍由 `QGradient` 的规则决定；
- `(0, 0)` 是逻辑坐标，不一定是绘制对象左上角以外的任何特定位置；
- 需要实际绘制时还要配置 stop 并交给 `QBrush`。

### `QConicalGradient::QConicalGradient(const QPointF &center, qreal angle)`

```cpp
QConicalGradient(const QPointF &center, qreal angle)
```

**作用：** 使用给定中心点和起始角构造渐变。

**参数边界：**

- `center` 使用逻辑坐标；
- `angle` 使用度，文档要求在 `0` 到 `360` 之间；
- 角度表示从哪里开始沿圆周插值，不是 stop 位置。

### `QConicalGradient::QConicalGradient(qreal cx, qreal cy, qreal angle)`

```cpp
QConicalGradient(qreal cx, qreal cy, qreal angle)
```

**作用：** 使用 `(cx, cy)` 作为中心点的便捷构造函数。

**边界：**

- `cx` 和 `cy` 是逻辑坐标；
- `angle` 的单位和范围与 `QPointF` 重载相同；
- 与 `QPointF(cx, cy)` 重载表达同一类状态。

### `QConicalGradient::angle()`

```cpp
qreal angle() const
```

**作用：** 返回圆锥渐变的起始角，单位是度，坐标含义是逻辑坐标系中的方向。

它不会返回当前绘制设备上的屏幕角度，也不会返回某个 stop 的位置。

### `QConicalGradient::center()`

```cpp
QPointF center() const
```

**作用：** 返回渐变中心点的逻辑坐标。

如果返回的点看起来不在目标图形中心，先检查坐标模式、画刷变换和 painter 变换，而不是先修改 stop。

### `QConicalGradient::setAngle(qreal angle)`

```cpp
void setAngle(qreal angle)
```

**作用：** 修改渐变的起始角。

**边界：**

- 使用度而不是弧度；
- 文档要求值位于 `0` 到 `360`；
- 修改后只改变渐变状态，不会自动触发控件重绘；控件场景需要由调用者安排更新。

### `QConicalGradient::setCenter(const QPointF &center)`

```cpp
void setCenter(const QPointF &center)
```

**作用：** 设置逻辑坐标中的渐变中心。

它只改变中心，不改变 stop、起始角或坐标模式。

### `QConicalGradient::setCenter(qreal x, qreal y)`

```cpp
void setCenter(qreal x, qreal y)
```

**作用：** 以两个坐标分量设置渐变中心，是 `QPointF` 重载的便捷形式。

**边界：** `x`、`y` 仍然是逻辑坐标；它与 `setCenter(QPointF(x, y))` 的语义相同。

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QConicalGradient()` | 创建默认中心和起始角的圆锥渐变。 | 默认中心是 `(0, 0)`，还需配置画刷和 stop。 |
| 构造 | `QConicalGradient(const QPointF &center, qreal angle)` | 指定中心点和起始角。 | 中心使用逻辑坐标；角度是 0 到 360 度。 |
| 构造 | `QConicalGradient(qreal cx, qreal cy, qreal angle)` | 用两个坐标分量指定中心。 | 与 `QPointF` 重载语义相同。 |
| 查询 | `qreal angle() const` | 读取起始角。 | 返回度数，不是 stop 位置或弧度。 |
| 查询 | `QPointF center() const` | 读取逻辑坐标中的中心点。 | 同时检查坐标模式和变换。 |
| 设置 | `void setAngle(qreal angle)` | 改变颜色插值的起始方向。 | 使用度；改变对象不会自动刷新控件。 |
| 设置 | `void setCenter(const QPointF &center)` | 设置渐变中心。 | 不改变 stop 和坐标模式。 |
| 设置 | `void setCenter(qreal x, qreal y)` | 以两个坐标分量设置中心。 | 坐标仍是逻辑坐标。 |
| 继承接口 | `QGradient::setColorAt()` | 添加或替换单个渐变 stop。 | position 必须在 0 到 1；不是角度。 |
| 继承接口 | `QGradient::setStops()` | 一次替换全部 stop。 | 位置必须在 0 到 1 且按升序排列。 |
| 继承接口 | `QGradient::setCoordinateMode()` | 控制渐变坐标映射方式。 | 默认是 `LogicalMode`；影响中心如何落到设备上。 |
| 继承接口 | `QGradient::setSpread()` | 设置区域外的扩展方式。 | 对圆锥渐变无效。 |

---

### 一句话总结

`QConicalGradient` 用中心点、起始角和归一化 stop 定义一整圈的角度渐变；它要通过 `QBrush` 交给绘制系统，且 `spread` 对这种闭合渐变不起作用。
