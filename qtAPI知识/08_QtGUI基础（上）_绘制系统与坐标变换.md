# Qt GUI 基础（上）：绘制系统与坐标变换

> 适用版本：Qt 6.11.1  
> 所属模块：Qt GUI；示例窗口使用 Qt Widgets  
> 核心类型：`QPainter`、`QPaintDevice`、`QPen`、`QBrush`、`QColor`、`QTransform`、`QPainterPath`

## 1. Qt 绘制体系的三层结构

```text
绘制命令层：QPainter
    drawLine / drawRect / drawText / drawImage / drawPath ...
                    ↓
绘制目标层：QPaintDevice
    QWidget / QImage / QPixmap / QPrinter ...
                    ↓
后端实现层：QPaintEngine
    光栅、打印、平台或其他绘制后端
```

- `QPainter` 描述“画什么、用什么状态画”；
- `QPaintDevice` 表示“画到哪里”；
- `QPaintEngine` 把统一命令翻译成具体后端操作。

日常开发主要使用前两层，不应直接依赖某个 Paint Engine。

## 2. 构建与头文件

只在内存图像上绘制时链接 Qt GUI：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

自定义 `QWidget` 示例需要 Widgets：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

常用头文件：

```cpp
#include <QPainter>
#include <QPaintEvent>
#include <QPainterPath>
#include <QPen>
#include <QBrush>
#include <QTransform>
```

## 3. QPainter 是带状态的绘制器

一个 `QPainter` 同时保存：

- 画笔 `pen`：轮廓线颜色、宽度、线型、端点和连接方式；
- 画刷 `brush`：封闭区域的填充；
- 字体 `font`；
- 不透明度 `opacity`；
- 坐标变换 `transform`；
- 裁剪区域 `clip`；
- 合成模式 `compositionMode`；
- 渲染提示 `renderHints`。

后续绘制命令都使用当时的状态：

```cpp
painter.setPen(Qt::red);
painter.drawLine(0, 0, 100, 0); // 红线

painter.setPen(Qt::blue);
painter.drawLine(0, 20, 100, 20); // 蓝线
```

理解状态机后，很多“为什么第二个图形颜色不对”的问题就能定位为状态泄漏。

## 4. 在 QWidget 中正确绘制

窗口内容需要重绘时，Qt 向控件发送绘制事件，最终调用 `paintEvent()`。

```cpp
void Gauge::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event);
    //告诉 C++ 编译器某个变量虽然已声明，但在当前作用域内是故意不使用的
    QPainter painter(this);
    painter.drawText(rect(), Qt::AlignCenter, tr("42"));
}
```

对于 QWidget，通常只应在 `paintEvent()` 或由绘制事件触发的调用链中创建以该控件为目标的 Painter。

### 4.1 update 与 repaint

```cpp
value_ = value;
update();
```

- `update()` 安排稍后的绘制事件，多个请求可被合并，通常优先使用；
- `repaint()` 尝试立即同步重绘，容易造成重复工作或递归绘制。

业务函数应修改模型状态并调用 `update()`，而不是在鼠标槽里长期保存 Painter 直接画。

## 5. 最小可用代码：自绘进度条

```cpp
#include <QApplication>
#include <QPainter>
#include <QWidget>

class ProgressWidget : public QWidget
{
public:
    using QWidget::QWidget;

    void setValue(int value)
    {
        value_ = qBound(0, value, 100);
        //qBound() 是 Qt 框架提供的一个非常方便的内联函数，定义在 <QtGlobal> 或 <QtCore/qglobal.h> 中，它的作用是限制一个值在一个指定的最小值和最大值之间。它接受三个参数
        update();
    }

protected:
    void paintEvent(QPaintEvent *) override
    {
        QPainter p(this);
        p.setRenderHint(QPainter::Antialiasing);

        const QRectF track = rect().adjusted(8, 8, -8, -8);
        p.setPen(Qt::NoPen);
        p.setBrush(QColor("#d7dbe0"));
        p.drawRoundedRect(track, 4, 4);

        QRectF fill = track;
        fill.setWidth(track.width() * value_ / 100.0);
        p.setBrush(QColor("#16845b"));
        p.drawRoundedRect(fill, 4, 4);

        p.setPen(Qt::black);
        p.drawText(track, Qt::AlignCenter,
                   QString::number(value_) + "%");
    }

private:
    int value_ = 65;
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    ProgressWidget window;
    window.resize(360, 64);
    window.show();
    return app.exec();
}
```

这里没有保存绘制结果。每次需要重绘时，都根据 `value_` 重新生成画面，这符合 Qt 的保留状态式窗口模型。

## 6. Painter 的开始与结束

两种等价形式：

```cpp
QPainter painter(&image); // 构造时 begin
// 绘制
// 析构时 end
```

```cpp
QPainter painter;
if (painter.begin(&image)) {
    // 绘制
    painter.end();
}
```

优先使用第一种 RAII 形式。可用 `isActive()` 检查是否成功激活。

同一个 Paint Device 通常不能同时被两个 Painter 绘制。Painter 活跃时也不要修改目标图像的底层存储。

## 7. QPaintDevice：绘制目标

常见设备：

| 设备         | 典型用途                 |
| ---------- | -------------------- |
| `QWidget`  | 屏幕控件                 |
| `QImage`   | CPU 内存像素、图像处理、工作线程绘制 |
| `QPixmap`  | 屏幕显示优化、图标和缓存         |
| `QPicture` | 记录并重放绘制命令            |
| `QPrinter` | 打印或输出 PDF            |

设备提供宽高、逻辑 DPI、物理 DPI、设备像素比等指标。不要假设所有目标都是 96 DPI 的屏幕位图。

## 8. 线条：QPen

```cpp
QPen pen(QColor("#20252b"));
pen.setWidthF(2.0);
pen.setStyle(Qt::DashLine);//定义线条的类型。可以使用 setStyle() 方法设置画笔线条的类型，如实线、虚线、点线等。Qt 提供了多种内置样式，如 Qt::SolidLine、Qt::DashLine、Qt::DotLine 等。
pen.setCapStyle(Qt::RoundCap);//设置线条两端的形状。可以是方形、平头或圆形。使用 setCapStyle(Qt::PenCapStyle style) 方法设置线条端点形状
pen.setJoinStyle(Qt::RoundJoin);//设置两条线的连接点的类型。可以是斜角连接、斜接连接或圆角连接。使用 setJoinStyle(Qt::PenJoinStyle style) 方法设置连接点形状。
painter.setPen(pen);
```

### 8.1 width 与 widthF

- `setWidth(int)` 使用整数逻辑单位；
- `setWidthF(qreal)` 支持浮点宽度；
- 宽度 0 表示 cosmetic pen，通常保持约一个设备像素宽，不随世界变换缩放。

需要线条跟随图形一起缩放时，不要使用宽度 0。

### 8.2 端点和连接

`capStyle` 决定开放线段端部：

- `FlatCap`：在端点截断；
- `SquareCap`：超过端点半个线宽；
- `RoundCap`：圆形端部。

`joinStyle` 决定折线拐角：

- `MiterJoin`：尖角；
- `BevelJoin`：削平；
- `RoundJoin`：圆角。

尖锐角度下 Miter 可能拉出很长尖角，可通过 `miterLimit` 限制。

### 8.3 自定义虚线

```cpp
QPen pen(Qt::black, 2.0);
pen.setDashPattern({4, 2, 1, 2});
pen.setDashOffset(0.5);
```

数组交替表示画线和空白长度，并相对笔宽缩放。

## 9. 填充：QBrush

纯色填充：

```cpp
painter.setBrush(QColor("#f4c95d"));
```

无填充：

```cpp
painter.setBrush(Qt::NoBrush);
```

纹理和渐变：

```cpp
QLinearGradient gradient(0, 0, 200, 0);
gradient.setColorAt(0.0, QColor("#16845b"));
gradient.setColorAt(1.0, QColor("#f4c95d"));
painter.setBrush(gradient);
```

画笔控制边界，画刷控制内部：

```cpp
painter.setPen(QPen(Qt::black, 2));
painter.setBrush(Qt::yellow);
painter.drawEllipse(QRectF(10, 10, 80, 80));
```

## 10. QColor 与透明度

```cpp
QColor color(22, 132, 91, 160); // RGBA，alpha 0~255
painter.setBrush(color);
```

也可使用浮点分量：

```cpp
QColor color = QColor::fromRgbF(0.1, 0.5, 0.35, 0.7);
```

全局不透明度作用于之后所有绘制：

```cpp
painter.setOpacity(0.5);
painter.drawImage(target, image);
painter.setOpacity(1.0);
```

建议配合 `save()` / `restore()`，避免忘记恢复。

## 11. 常用绘制命令

```cpp
p.drawPoint(point);点
p.drawLine(line);线
p.drawRect(rect);矩形
p.drawRoundedRect(rect, 6, 6);圆角矩形
p.drawEllipse(rect);圆
p.drawArc(rect, startAngle, spanAngle);圆弧
p.drawPie(rect, startAngle, spanAngle);扇形
p.drawPolyline(points);折线
p.drawPolygon(points);多边形
p.drawText(rect, flags, text);文本
p.drawImage(target, image);图片
p.drawPixmap(target, pixmap);绘制图像
p.drawPath(path);画路径
```

`drawArc()`、`drawPie()` 等角度参数以 1/16 度为单位：

```cpp
p.drawArc(rect, 30 * 16, 120 * 16);
```

这是常见陷阱。

## 12. 整数几何与浮点几何

Qt 同时提供 `QPoint` / `QRect` 和 `QPointF` / `QRectF`。

复杂绘制优先使用浮点版本：

```cpp
QRectF r(10.5, 20.5, 100.0, 60.0);
painter.drawEllipse(r);
```

它们在缩放、旋转和动画中可避免过早取整造成的抖动和累计误差。

### 12.1 QRect 的边界历史语义

整数 `QRect::right()` 是 `left() + width() - 1`，`bottom()` 同理。几何运算中尽量使用 `x()`、`y()`、`width()`、`height()`，或改用 `QRectF`，避免边界差一问题。

## 13. 抗锯齿与渲染提示

```cpp
painter.setRenderHint(QPainter::Antialiasing, true);
painter.setRenderHint(QPainter::TextAntialiasing, true);
painter.setRenderHint(QPainter::SmoothPixmapTransform, true);
```

这些是提示，具体后端可能不完全遵循。

- `Antialiasing`：改善矢量边缘；
- `TextAntialiasing`：改善文字边缘；
- `SmoothPixmapTransform`：缩放图像时使用更平滑的采样。

质量通常伴随成本。大量缩略图实时缩放时，最好提前缓存目标尺寸图像，而不是每帧高质量重采样。

## 14. save 与 restore：隔离局部状态

```cpp
painter.save();
painter.translate(center);
painter.rotate(angle);
painter.setOpacity(0.6);
painter.drawPath(shape);
painter.restore();
```

`save()` 把当前状态压栈，`restore()` 恢复。二者必须配对。

把每个独立图元包在自己的状态作用域中，能防止变换、裁剪和颜色影响后续绘制。

可用小型守卫进一步减少遗漏，但简单函数中明确的配对通常最清楚。

## 15. 坐标系统：逻辑坐标到设备坐标

绘制代码提交的是逻辑坐标，Painter 再映射到设备坐标：

```text
图形局部点
  ↓ worldTransform：平移、旋转、缩放、错切
逻辑坐标
  ↓ window / viewport 映射
设备无关坐标
  ↓ 设备像素比和后端映射
实际像素或打印单位
```

普通 QWidget 绘制通常只需世界变换。

## 16. 平移、旋转、缩放与错切

```cpp
painter.translate(100, 80);//是 Qt 绘图系统 QPainter 类中的一个核心函数，用于平移（Translation） 绘图坐标系。 当调用 painter.translate (dx,dy) 时，它会将 QPainter 的当前坐标原点从 (0,0) 移动到新的位置 (dx,dy)。
painter.rotate(30);       // 单位为度，正值通常顺时针
painter.scale(1.5, 1.5);
painter.shear(0.2, 0.0);
```

变换改变坐标系，不直接修改图形数据。之后仍可围绕局部原点绘制：

```cpp
painter.translate(rect().center());
painter.rotate(angle_);
painter.drawRect(QRectF(-40, -20, 80, 40));
```

这样图形自然围绕中心旋转。

### 16.1 变换顺序很重要

“先平移再旋转”与“先旋转再平移”通常结果不同，因为矩阵乘法不可交换。

实践中按局部层次写：

    qpainter所在的widget有自己的坐标系：X轴向右，Y轴向下。qpainter自己也有坐标系，默认和widget是重合的。但是qpainter的坐标系可以做各种变换，如平移（translate），（scale）。

先说下scale。它的作用是改变qpainter的刻度长度

```cpp
p.save();
p.translate(objectPosition);
p.rotate(objectAngle);
p.scale(objectScale, objectScale);
p.drawPath(localShape);
p.restore();
```

把图形定义在局部原点，再用变换摆放，更易维护。

## 17. QTransform：显式二维矩阵

```cpp
QTransform transform;
transform.translate(100, 80);
transform.rotate(45);
transform.scale(2, 2);

painter.setWorldTransform(transform);
```

映射点和矩形：

```cpp
QPointF devicePoint = transform.map(localPoint);
QRectF bounds = transform.mapRect(localRect);
```

反向映射用于命中测试：

```cpp
bool invertible = false;
QTransform inverse = transform.inverted(&invertible);
if (invertible) {
    QPointF local = inverse.map(mousePosition);
    if (shape.contains(local))
        selectObject();
}
```

缩放为 0 等情况会使矩阵不可逆，必须检查返回标志。

## 18. window 与 viewport

- `window`：逻辑坐标范围；
- `viewport`：设备上的目标矩形。

```cpp
painter.setWindow(QRect(0, 0, 1000, 1000));
painter.setViewport(rect());
```

此后可始终在 1000×1000 的逻辑画布中绘制，由 Qt 映射到控件大小。

若 window 与 viewport 宽高比不同，图形会被非等比拉伸。保持比例时应先计算 letterbox 目标区域。

## 19. 裁剪

```cpp
painter.save();
painter.setClipRect(contentRect);
painter.drawImage(largeTarget, image);
painter.restore();
```

也可使用路径或区域：

```cpp
painter.setClipPath(roundShape);
painter.setClipRegion(region);
```

裁剪坐标使用当前 Painter 的逻辑坐标。设置裁剪后再改变变换时，要清楚裁剪是在何种状态下建立的。

读取复杂的组合裁剪路径可能代价较高，因为底层引擎未必以相同形式保存它。不要在热路径反复调用 `clipPath()` 只为查询状态。

## 20. QPainterPath：可复用的复杂形状

```cpp
QPainterPath path;
path.moveTo(10, 80);
path.cubicTo(30, 10, 70, 10, 90, 80);//塞贝曲线
path.lineTo(50, 50);
path.closeSubpath();

painter.setPen(QPen(Qt::black, 2));
painter.setBrush(QColor("#f4c95d"));
painter.drawPath(path);
```

Path 可用于：

- 填充；
- 描边；
- 裁剪；
- 命中测试；
- 布尔运算；
- 重复绘制复杂轮廓。

### 20.1 子路径与当前点

```cpp
path.moveTo(start);       // 开始新子路径
path.lineTo(point);       // 直线
path.quadTo(ctrl, end);   // 二次贝塞尔
path.cubicTo(c1, c2, end);// 三次贝塞尔
path.closeSubpath();      // 闭合当前子路径
```

绘制非连续形状时要使用 `moveTo()`，否则 Qt 会从上一个当前点连接过去。

### 20.2 填充规则

```cpp
path.setFillRule(Qt::OddEvenFill);
// 或 Qt::WindingFill
```

- Odd-Even：从点向外画射线，穿过奇数次边界则在内部；
- Winding：根据边的方向累计环绕数。

自交、多层轮廓和带孔形状可能因规则不同产生完全不同的填充效果。

### 20.3 边界与命中测试

```cpp
QRectF exact = path.boundingRect();
QRectF fast = path.controlPointRect();
bool hit = path.contains(point);
bool overlap = path.intersects(rect);
```

`controlPointRect()` 包含所有控制点，是 `boundingRect()` 的超集，但计算通常更快，适合粗略剔除。

### 20.4 路径布尔运算

```cpp
QPainterPath unionPath = a.united(b);
QPainterPath intersection = a.intersected(b);
QPainterPath difference = a.subtracted(b);
```

这些运算把路径视为填充区域；数值稳定性原因可能把贝塞尔曲线展平为线段。精密 CAD 几何不应无条件把它当作精确计算内核。

## 21. QPainterPathStroker：把线变成区域

命中一条细线时，直接 `path.contains(point)` 往往无效，因为开放路径没有足够填充面积。可生成描边轮廓：

```cpp
QPainterPathStroker stroker;
stroker.setWidth(10.0); // 点击容差
QPainterPath hitArea = stroker.createStroke(path);

if (hitArea.contains(mousePoint))
    selectPath();
```

它也可用来生成可填充的描边形状。

## 22. 合成模式

默认 `CompositionMode_SourceOver`：源图覆盖目标，按 alpha 混合。

```cpp
painter.setCompositionMode(QPainter::CompositionMode_Multiply);
painter.drawImage(target, overlay);
```

常见模式：

| 模式                | 含义           |
| ----------------- | ------------ |
| `SourceOver`      | 普通透明叠加       |
| `DestinationOver` | 画到已有内容后面     |
| `Source`          | 用源直接替换目标区域   |
| `Clear`           | 清除覆盖区域       |
| `Multiply`        | 正片叠底，常用于变暗混色 |
| `Screen`          | 滤色，常用于变亮混色   |

所有合成模式在 `QImage` 光栅目标上支持最完整；不同后端的能力和性能可能不同。

### 22.1 透明边界陷阱

某些合成模式会作用于绘制图元的整个边界矩形，包括源图中完全透明的像素。不要只凭“透明像素看不见”推断目标不会变化，应理解所选 Porter-Duff 或混色公式。

## 23. 高 DPI 与设备像素比

Qt 界面通常使用设备无关像素。高 DPI 屏幕上，一个逻辑单位可能对应多个物理像素。

```cpp
qreal ratio = devicePixelRatioF();
```

创建高分辨率离屏图像时：

```cpp
const QSize logicalSize(200, 100);
const qreal dpr = widget->devicePixelRatioF();

QImage image(logicalSize * dpr,
             QImage::Format_ARGB32_Premultiplied);
image.setDevicePixelRatio(dpr);
image.fill(Qt::transparent);

QPainter p(&image);
p.drawText(QRect(QPoint(0, 0), logicalSize),
           Qt::AlignCenter, "HiDPI");
```

设置 DPR 后，Painter 仍按逻辑尺寸绘制，但底层有更多像素，显示时保持正确大小和清晰度。

## 24. 绘制线程规则

- `QWidget` 和 `QPixmap` 与 GUI 系统关系紧密，通常只在 GUI 线程使用；
- `QImage` 是普通内存像素缓冲，更适合工作线程生成；
- 不同线程可绘制各自独占的不同 `QImage`；
- 不能让多个线程无同步地读写同一图像；
- 工作线程完成后，可按值把 `QImage` 发回主线程显示。

```text
工作线程：创建并绘制 QImage
     ↓ queued signal，按值传递
主线程：转换/显示为 pixmap 或直接 drawImage
```

隐式共享使传值成本较低，但并不允许并发修改同一个实例。

## 25. 性能原则

### 25.1 只绘制需要的区域

`QPaintEvent::region()` 描述待更新区域。复杂画布可先判断图元是否与更新区域相交，避免全量绘制。

### 25.2 缓存昂贵且稳定的内容

复杂路径、文本布局或缩放图像如果长期不变，可缓存为 `QPixmap`、`QImage` 或预构建 Path。状态改变时使缓存失效，而不是每帧重新计算。

### 25.3 不要无条件开启所有质量选项

抗锯齿和平滑缩放只在视觉确有收益处开启。像素风图标或整数对齐表格线有时关闭抗锯齿更清晰。

### 25.4 避免 paintEvent 中做业务 I/O

不要在 `paintEvent()` 读取文件、请求网络或执行重计算。绘制函数应快速、确定地依据已有状态生成画面。

### 25.5 使用浮点坐标，但理解像素对齐

奇数像素宽的线若落在整数坐标上，可能覆盖相邻两个像素并显得发虚。需要极锐利的 1 像素线时，应结合 DPR、抗锯齿和半像素偏移实际测试。

## 26. 常见错误

### 26.1 在 paintEvent 外给 QWidget 画图

绘制可能不会持久保存，下一次系统重绘就消失。应保存模型状态、调用 `update()`，在 `paintEvent()` 重建画面。

### 26.2 忘记 restore

后续图元继承错误变换、透明度或裁剪。每个 `save()` 都要有结构清晰的 `restore()`。

### 26.3 把 brush 当边框

`QBrush` 填内部，`QPen` 画轮廓。设置错对象会得到“颜色没生效”的错觉。

### 26.4 角度忘乘 16

弧、扇形等传统 API 以 1/16 度为单位，而 `rotate()` 使用普通度数。

### 26.5 变换顺序错误

矩阵变换不可交换。以局部坐标建模，并按“摆放、旋转、缩放、绘制”写出层次。

### 26.6 高 DPI 离屏图发虚

只按逻辑尺寸创建像素缓冲却在高 DPI 屏幕放大。应按 DPR 增加像素尺寸并设置 `devicePixelRatio`。

### 26.7 工作线程创建或修改 QWidget

GUI 对象只在主线程使用。工作线程只生成数据或独占的 `QImage`。

## 27. API 速查表

| API                        | 用途      | 注意点               |
| -------------------------- | ------- | ----------------- |
| `QPainter(device)`         | 开始绘制    | 作用域结束自动停止         |
| `setPen()`                 | 设置轮廓    | `NoPen` 禁止轮廓      |
| `setBrush()`               | 设置填充    | `NoBrush` 禁止填充    |
| `setRenderHint()`          | 提示渲染质量  | 后端不保证完全遵循         |
| `save()` / `restore()`     | 保存、恢复状态 | 必须配对              |
| `translate()`              | 平移坐标系   | 影响后续绘制            |
| `rotate()`                 | 旋转坐标系   | 参数单位为度            |
| `scale()`                  | 缩放坐标系   | 0 缩放会导致不可逆        |
| `setWorldTransform()`      | 设置矩阵    | 可替换或组合现有变换        |
| `setClipRect()`            | 设置矩形裁剪  | 使用逻辑坐标            |
| `setOpacity()`             | 设置全局透明度 | 用 save/restore 隔离 |
| `setCompositionMode()`     | 设置像素合成  | QImage 支持最完整      |
| `QPainterPath::contains()` | 命中填充区域  | 细线用 Stroker 扩展    |
| `QTransform::inverted()`   | 求逆变换    | 必须检查是否可逆          |
| `QWidget::update()`        | 安排重绘    | 通常优于同步 repaint    |

## 28. 自测题

### 题 1：为什么按钮槽里画的线会消失

<details>
<summary>答案</summary>

窗口内容由绘制事件重建。临时绘制没有成为控件状态，下一次系统重绘会覆盖它。应保存线条数据、调用 `update()`，并在 `paintEvent()` 绘制。

</details>

### 题 2：QPen 和 QBrush 分别负责什么

<details>
<summary>答案</summary>

Pen 负责边界和线条，Brush 负责封闭区域内部填充。

</details>

### 题 3：如何让矩形绕中心旋转

<details>
<summary>答案</summary>

先把坐标原点平移到中心，再旋转，然后绘制以局部原点为中心的矩形，最后恢复 Painter 状态。

</details>

### 题 4：为什么命中开放曲线不能只用 contains

<details>
<summary>答案</summary>

`contains()` 判断的是路径填充区域，开放细线没有合适填充面积。用 `QPainterPathStroker` 按点击容差生成描边区域后测试。

</details>

### 题 5：高 DPI 图像应如何创建

<details>
<summary>答案</summary>

像素尺寸使用“逻辑尺寸 × DPR”，并对图像设置同一 DPR。Painter 继续按逻辑坐标绘制，显示大小正确且像素更清晰。

</details>

## 29. 本篇总结

Qt 绘制的核心不是记住几十个 `draw...()`，而是掌握状态和坐标：

1. 在 `paintEvent()` 中根据持久状态重建 QWidget 画面。
2. Pen 管轮廓，Brush 管填充，Painter 保存全部绘制状态。
3. 用 `save()` / `restore()` 隔离局部变换和样式。
4. 用局部坐标定义图形，再通过 `QTransform` 放置和命中测试。
5. 复杂形状用 `QPainterPath`，细线命中使用 Stroker。
6. 高 DPI 下区分逻辑尺寸、物理像素和设备像素比。
7. GUI 线程绘制 QWidget，后台绘图优先使用各线程独占的 QImage。

下篇将继续讲 `QImage`、`QPixmap`、`QIcon`、图像编解码、字体度量，以及鼠标、键盘、滚轮和触摸输入。
