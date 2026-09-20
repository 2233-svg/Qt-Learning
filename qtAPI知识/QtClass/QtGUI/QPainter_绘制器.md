# QPainter：在绘制设备上执行二维绘图

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPainter>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Gui)`，并链接 `Qt6::Gui`

`QPainter` 是 Qt 的即时二维绘制器。它把画笔、画刷、字体、裁剪、透明度、合成模式和坐标变换组成一份可变绘制状态，并将点、路径、文本、图像等命令提交到一个 `QPaintDevice`，例如 `QWidget`、`QImage`、`QPixmap`、`QPicture` 或 `QPdfWriter`。

它不是可复制对象，也不拥有传入的绘制设备。一次绘制会话只有在 `begin()` 成功到 `end()` 结束之间有效；构造时传入设备是这对调用的 RAII 简写。一个绘制设备同一时刻只能被一个活动的 `QPainter` 使用。

## 先分清：画在哪里、何时画、画什么

常见目标和用法并不相同：

- `QWidget`：仅能在 `paintEvent()` 或其直接调用链中绘制。窗口系统决定何时需要重画，直接在任意槽函数里用 `QPainter(widget)` 会被下一次重绘覆盖，也违反 Qt 的绘制约束。
- `QImage`：内存中的像素缓冲，适合离屏生成、像素处理和后台计算后再交给 GUI 线程显示。`QImage::Format_Indexed8` 不支持作为 `QPainter` 目标。
- `QPixmap`：面向显示的图像资源，适合作为最终缓存或绘制来源；不要把它和 `QImage` 的纯内存处理职责混为一谈。
- `QPdfWriter` / 打印设备：同一套逻辑坐标可以输出到页面，但分辨率、字体与合成能力和屏幕不同，须按目标设备验证。

```cpp
void MeterWidget::paintEvent(QPaintEvent *)
{
    QPainter painter(this); // 构造即 begin(this)
    painter.setRenderHint(QPainter::Antialiasing);
    painter.setPen(QPen("#263238", 2));
    painter.setBrush(QColor("#80cbc4"));
    painter.drawEllipse(rect().adjusted(8, 8, -8, -8));
} // 析构时结束绘制
```

`QPainter(this)` 只应放在 `paintEvent()` 内。绘制一个 `QWidget` 时，通常也不需要主动清背景；背景是否由控件、样式或父控件处理应交给控件的属性和绘制策略。

## 绘制会话与状态的生命周期

可显式控制会话：

```cpp
QImage image(QSize(640, 360), QImage::Format_ARGB32_Premultiplied);
image.fill(Qt::transparent);

QPainter painter;
if (!painter.begin(&image))
    return;

painter.fillRect(image.rect(), Qt::white);
painter.end();
```

`begin()` 会把绘制器设为活动状态，并从设备复制初始属性（例如默认字体、布局方向等）；`end()` 结束会话并释放绘制引擎所需的资源。若 `begin()` 失败，`isActive()` 为假，后续绘制调用没有可依赖的效果。析构函数会尝试结束仍活动的绘制器，但在需要确认写出、释放设备或切换会话的代码中，应显式 `end()` 并处理 `false` 返回值。

不要在同一设备上嵌套两个 `QPainter`，也不要在第一个未结束时再次 `begin()` 到另一个设备。若需要暂时切换目标，先完整结束当前会话。

## 绘制状态：优先用 `save()` / `restore()` 隔离局部修改

一支 `QPainter` 保存如下状态：`QPen`、`QBrush`、字体、背景、裁剪、世界/视图变换、渲染提示、透明度、合成模式以及布局方向等。状态会持续影响此后的每个命令。

```cpp
void drawMarker(QPainter &painter, const QPointF &center)
{
    painter.save();
    painter.translate(center);
    painter.rotate(45);
    painter.setPen(Qt::NoPen);
    painter.setBrush(QColor("#ef5350"));
    painter.drawRect(QRectF(-6, -6, 12, 12));
    painter.restore();
}
```

每个 `save()` 必须有一个对应的 `restore()`，且 `restore()` 不能越过状态栈底。局部绘制函数应当在自身内部配对，而不是要求调用方猜测状态有没有被改掉。Qt 6.9 及以上可以在简单作用域中使用 `QPainterStateGuard`，但不要再混入手工恢复其所保存的同一层状态。

## 笔、刷与不透明度

`QPen` 决定轮廓线的颜色、宽度、虚线、端点和连接方式；`QBrush` 决定封闭图形的填充，可为纯色、纹理或渐变。`Qt::NoPen` 禁止描边，`Qt::NoBrush` 禁止填充。

`drawRect()`、`drawPath()`、`drawEllipse()` 等形状绘制同时使用当前笔和刷；`strokePath()` 只用给定笔，`fillPath()` 只用给定刷；`fillRect()` 直接以传入刷或颜色填充，不读取当前笔和刷，适合明确的背景填充。

`setOpacity()` 设置后续绘制的全局不透明度。它会与颜色、图像或画刷自身 alpha 共同作用；不要为了“恢复正常透明度”而猜测旧值，局部使用时用 `save()` / `restore()`。

## 坐标系统：变换应围绕局部对象建立

QPainter 区分逻辑坐标与设备坐标。常规控件绘制中，直接使用逻辑像素坐标即可；缩放、旋转、平移对象时，应在局部保存状态后变换：

```cpp
painter.save();
painter.translate(rect().center());
painter.scale(1.5, 1.5);
painter.rotate(-20);
painter.drawPath(iconPath.translated(-iconCenter));
painter.restore();
```

- `translate()`、`scale()`、`rotate()`、`shear()` 组合修改当前世界变换。
- `setTransform()` / `setWorldTransform()` 以替换或组合方式设定变换；`resetTransform()` 回到单位变换。
- `setWindow()` 定义逻辑窗口，`setViewport()` 定义它映射到设备上的视口。两者一起用于把固定逻辑坐标映射到不同尺寸的设备；它会引入缩放，非等比例矩形也会拉伸图形。
- `deviceTransform()` 是与设备相关的变换，`combinedTransform()` 是当前绘制所用的组合变换。它们主要用于需要与原生坐标互操作的高级代码。

在已缩放的坐标系中，普通笔宽也会缩放。需要接近设备像素宽度的线时，理解 `QPen` 的 cosmetic pen 规则，并在高 DPI、打印和导出目标上分别验证。

## 裁剪：限制输出，不是廉价的几何查询

`setClipRect()`、`setClipRegion()`、`setClipPath()` 限制后续绘制的可见区域；第二个参数是 `Qt::ReplaceClip`、`IntersectClip`、`UniteClip` 等组合方式。实际有效裁剪由底层 `QPaintEngine` 管理，`clipPath()` 和 `clipRegion()` 可能需要重建、反变换，频繁查询可能很昂贵。

```cpp
painter.save();
painter.setClipPath(chartArea, Qt::IntersectClip);
drawSeries(painter);
painter.restore();
```

绘制代码通常只设置裁剪而不读取回裁剪状态。以 `save()` / `restore()` 限制其作用域，比依赖当前设备的复杂组合裁剪更可靠。

## 合成模式与渲染提示

默认 `CompositionMode_SourceOver` 按源覆盖目标的 alpha 混合，是大多数 UI 绘制的正确选择。`CompositionMode_Clear` 清除目标区域；`Source` 完全使用源；`Destination` 保留目标；`SourceIn`、`SourceOut`、`DestinationIn` 等为 Porter-Duff 规则；`Multiply`、`Screen`、`Overlay` 等为混色模式。

并非每个绘制引擎完整支持所有模式。`QImage` 作为目标时对合成模式的支持最完整；RasterOp 模式有平台和后端限制。做擦除、遮罩或混色特效前，确认目标有 alpha 通道，且用预乘 alpha 格式和实际目标验证结果。

`setRenderHint()` 是偏好而非绝对保证：

- `Antialiasing` 改善形状边缘。
- `TextAntialiasing` 控制文本抗锯齿偏好。
- `SmoothPixmapTransform` 在缩放图像时请求平滑采样，质量更高但更慢。
- `VerticalSubpixelPositioning` 允许文本进行更精细的垂直定位。
- `LosslessImageRendering` 请求避免图像的有损转换。
- `NonCosmeticBrushPatterns` 使图案刷随几何变换而变化。

只为确实需要的区域启用开销较高的提示，并把效果看作后端能力与性能之间的请求。

## 图元、图像和文本的使用边界

- `drawPoint(s)`、`drawLine(s)`、`drawPolyline()` 主要受当前笔影响，不会自动形成填充区域。
- `drawRect(s)`、`drawEllipse()`、`drawPolygon()`、`drawPath()` 同时使用笔和刷；`drawConvexPolygon()` 的输入必须真的是凸多边形。
- `drawArc()`、`drawPie()`、`drawChord()` 的起始角和跨度使用 **1/16 度**，不是普通浮点度数；正角度为逆时针。
- `drawPixmap()` 适合绘制显示用像素图，`drawImage()` 接受内存图像并可指定颜色转换标志。给出目标和源矩形时是裁切并缩放；只给位置时使用原尺寸。
- 多个相同 `QPixmap` 的精灵绘制可用 `drawPixmapFragments()`，避免重复状态设置。`OpaqueHint` 只能在全部片段内容确实不透明时设置。
- `drawText(point, text)` 的点是文本**基线**位置；`drawText(rect, flags, text)` 在矩形内布局，返回/写出的包围矩形可用于后续对齐。不要把两者的纵坐标混用。
- `drawStaticText()` 适合重复绘制预处理过的静态文本；`drawGlyphRun()` 是面向已经完成字形选择与定位的高级接口；`drawTextItem()` 通常由文本布局内部代码使用。

## 原生绘制互操作

在 OpenGL、Vulkan 以外的特定后端或平台 API 互操作中，`beginNativePainting()` / `endNativePainting()` 划出一段原生绘制区间。它们不是“更快的 QPainter 模式”，而是让调用方暂时接管底层上下文的同步边界。

原生调用可能破坏 QPainter 假设的状态。成对调用、限制范围、在返回后重新建立所需的原生状态；不要指望 Qt 自动恢复所有平台 API 状态。正常 2D 绘制不需要使用它们。

## 常见错误

- 在鼠标事件或定时器中直接绘制 `QWidget`：应更新状态后调用 `update()`，由 `paintEvent()` 绘制。
- 忘记 `restore()`：后续图形突然偏移、裁剪或透明，通常是状态泄漏。
- 把 `QPainterPath`、`QRect` 等逻辑坐标又手工乘缩放比，同时已调用 `scale()`：会发生双重缩放。
- 用 `CompositionMode_Clear` 却看不到透明洞：检查目标像素格式、背景重绘和 alpha 合成链路。
- 调用 `clipPath()` 来判断当前裁剪：它可能昂贵；自行保存业务区域或只使用 `clipBoundingRect()` 做粗略判断。
- 对同一设备并发或嵌套创建绘制器：先结束已有会话。

## API 速查表

### 生命周期与设备

| API | 语义与使用边界 |
| --- | --- |
| `QPainter()` | 创建未激活绘制器，之后以 `begin(device)` 开始会话。 |
| `QPainter(QPaintDevice *device)` | 等价于创建后尝试 `begin(device)`；构造后仍应在必要时检查 `isActive()`。 |
| `~QPainter()` | 结束仍活动的会话；需要检测结束失败时显式调用 `end()`。 |
| `device()` | 返回当前目标设备；无活动目标时不能据此推断可绘制性。 |
| `begin(QPaintDevice *)` | 启动绘制会话并复制设备初始属性；同一设备不能已有活动绘制器。 |
| `end()` | 结束会话并返回是否成功；结束后不能继续绘制。 |
| `isActive()` | 判断绘制器是否已成功开始且未结束。 |
| `paintEngine()` | 返回底层绘制引擎，主要供高级/后端代码使用。 |

### 绘制状态

| API | 语义与使用边界 |
| --- | --- |
| `save()` / `restore()` | 压入/弹出完整绘制状态；调用次数必须严格配对。 |
| `setPen(QPen)` / `setPen(QColor)` / `setPen(Qt::PenStyle)` | 设置当前笔；`Qt::NoPen` 关闭描边。 |
| `pen()` | 返回当前笔的只读引用，修改请先复制或再次 `setPen()`。 |
| `setBrush(QBrush)` / `setBrush(QColor)` / `setBrush(Qt::BrushStyle)` | 设置当前刷；`Qt::NoBrush` 关闭填充。 |
| `brush()` | 返回当前画刷的只读引用。 |
| `setFont(QFont)` / `font()` | 设置或读取当前字体。 |
| `fontMetrics()` / `fontInfo()` | 返回当前字体在目标设备上的度量或实际匹配信息；依赖活动设备。 |
| `setOpacity(qreal)` / `opacity()` | 设置或读取全局不透明度；局部调整用状态栈恢复。 |
| `setBackground(QBrush)` / `background()` | 设置或读取背景刷，主要影响使用背景模式的操作。 |
| `setBackgroundMode(Qt::BGMode)` / `backgroundMode()` | 设置或读取 `OpaqueMode`、`TransparentMode` 等背景模式。 |
| `setBrushOrigin(...)` / `brushOrigin()` / `brushOriginF()` | 设置或读取图案/纹理刷原点；会影响图案相位。 |
| `setLayoutDirection()` / `layoutDirection()` | 设置或读取文本等操作使用的布局方向。 |
| `setCompositionMode()` / `compositionMode()` | 设置或读取颜色合成规则；后端支持度和 alpha 格式会影响效果。 |

### 裁剪与坐标变换

| API | 语义与使用边界 |
| --- | --- |
| `setClipRect(QRectF/QRect/坐标, op)` | 以矩形替换或组合裁剪区域。 |
| `setClipRegion(QRegion, op)` | 以整数区域设置或组合裁剪。 |
| `setClipPath(QPainterPath, op)` | 以任意路径设置或组合裁剪；复杂路径有额外开销。 |
| `setClipping(bool)` / `hasClipping()` | 开关或查询裁剪是否启用。 |
| `clipBoundingRect()` | 返回当前裁剪的逻辑包围矩形，适合粗略范围判断。 |
| `clipRegion()` / `clipPath()` | 返回组合裁剪；可能需要重建和坐标变换，不适合高频查询。 |
| `setTransform(transform, combine)` / `transform()` | 设置或读取当前世界变换；`combine=true` 表示与当前变换组合。 |
| `setWorldTransform(matrix, combine)` / `worldTransform()` | `setTransform()` 的世界变换命名接口。 |
| `resetTransform()` | 恢复单位世界变换。 |
| `deviceTransform()` | 返回到设备坐标的变换，主要用于高级互操作。 |
| `combinedTransform()` | 返回当前组合变换。 |
| `setWorldMatrixEnabled()` / `worldMatrixEnabled()` | 开关世界矩阵作用；高级兼容接口，常规绘制优先用变换和状态栈。 |
| `translate(...)` / `scale()` / `rotate()` / `shear()` | 在当前坐标系叠加平移、缩放、旋转、错切。 |
| `setWindow(QRect/坐标)` / `window()` | 设置或读取逻辑窗口。 |
| `setViewport(QRect/坐标)` / `viewport()` | 设置或读取映射到设备的视口。 |
| `setViewTransformEnabled()` / `viewTransformEnabled()` | 开关窗口到视口的视图变换。 |

### 路径和基本图元

| API | 语义与使用边界 |
| --- | --- |
| `strokePath(path, pen)` | 用给定笔描边路径，不改当前笔。 |
| `fillPath(path, brush)` | 用给定刷填充路径，不改当前刷。 |
| `drawPath(path)` | 用当前笔和刷绘制路径。 |
| `drawPoint(...)` / `drawPoints(pointer, count)` / `drawPoints(QPolygon/F)` | 绘制点集；指针数组和计数必须有效。 |
| `drawLine(...)` / `drawLines(pointer, count)` / `drawLines(QList)` | 绘制线或线集；点对重载按两点一条线解释，奇数尾点不会构成完整线段。 |
| `drawRect(...)` / `drawRects(pointer, count)` / `drawRects(QList)` | 用当前笔和刷绘制矩形或矩形集。 |
| `drawEllipse(...)` | 在矩形或中心半径指定的范围绘制椭圆。 |
| `drawPolyline(pointer, count)` / `drawPolyline(QPolygon/F)` | 绘制开放折线，不做填充。 |
| `drawPolygon(pointer, count, fillRule)` / `drawPolygon(QPolygon/F, fillRule)` | 绘制闭合多边形；填充规则只影响其内部。 |
| `drawConvexPolygon(...)` | 绘制凸多边形；输入非凸时结果不应依赖。 |
| `drawArc(rect, start, span)` | 绘制椭圆弧；角度参数单位是 1/16 度。 |
| `drawPie(rect, start, span)` | 绘制由圆弧和圆心组成的扇形；角度单位是 1/16 度。 |
| `drawChord(rect, start, span)` | 绘制由圆弧和端点连线组成的弓形；角度单位是 1/16 度。 |
| `drawRoundedRect(rect, xRadius, yRadius, mode)` | 绘制圆角矩形；`mode` 决定半径解释方式。 |
| `fillRect(rect, QBrush/QColor/Qt::GlobalColor/Qt::BrushStyle/QGradient::Preset)` | 直接填充矩形，忽略当前笔和刷。 |
| `eraseRect(...)` | 用当前背景刷擦除矩形；透明清除需求通常应选合成模式并明确 alpha 目标。 |

### 图像、像素图与图片

| API | 语义与使用边界 |
| --- | --- |
| `drawTiledPixmap(rect, pixmap, offset)` | 平铺像素图填满目标矩形，`offset` 控制起始相位。 |
| `drawPicture(point, QPicture)` | 重放 `QPicture` 记录的绘制命令；Qt 禁用 Picture 支持时不可用。 |
| `drawPixmap(target, pixmap, source)` 及位置/矩形重载 | 绘制像素图；目标与源矩形不同大小时发生缩放。 |
| `drawPixmapFragments(fragments, count, pixmap, hints)` | 批量绘制同一像素图的片段；`OpaqueHint` 只能用于真实不透明内容。 |
| `drawImage(target, image, source, flags)` 及位置/矩形重载 | 绘制 `QImage`，可指定颜色转换标志；按源/目标矩形裁切缩放。 |

### 文本与字形

| API | 语义与使用边界 |
| --- | --- |
| `drawText(point, text)` 及点坐标重载 | 在基线位置绘制单行文本。 |
| `drawText(rect, flags, text, boundingRect)` 及坐标重载 | 在矩形中按标志布局文本；可获得实际包围矩形。 |
| `drawText(rect, text, QTextOption)` | 使用 `QTextOption` 的换行、对齐等布局规则。 |
| `boundingRect(rect, flags, text)` | 计算对应矩形文本布局的边界，不绘制。 |
| `boundingRect(rect, text, QTextOption)` | 按 `QTextOption` 计算文本边界，不绘制。 |
| `drawStaticText(position, QStaticText)` | 绘制可预处理的静态文本，适合重复内容。 |
| `drawGlyphRun(position, QGlyphRun)` | 绘制已完成字形选择与定位的字形串；需启用 Raw Font 支持。 |
| `drawTextItem(position, QTextItem)` | 绘制文本项，通常由高级文本布局内部使用。 |

### 渲染引擎与原生互操作

| API | 语义与使用边界 |
| --- | --- |
| `setRenderHint(hint, on)` | 开关一个渲染提示，后端可按能力选择实现。 |
| `setRenderHints(hints, on)` | 批量开关渲染提示。 |
| `renderHints()` / `testRenderHint(hint)` | 返回或测试当前请求的提示位；不等价于后端已经保证的最终质量。 |
| `beginNativePainting()` | 开始临时原生绘制区间；仅供明确的底层 API 互操作。 |
| `endNativePainting()` | 结束原生绘制区间；必须与开始调用配对。 |

### 枚举与辅助类型

| 项目 | 用途 |
| --- | --- |
| `RenderHint` / `RenderHints` | 渲染质量和行为请求：抗锯齿、平滑缩放、文本定位等。 |
| `CompositionMode` | Porter-Duff、混色与 RasterOp 合成规则；选用前考虑目标设备支持。 |
| `PixmapFragment` | `drawPixmapFragments()` 的单片段描述，含目标中心、源矩形、缩放、旋转与不透明度。 |
| `PixmapFragment::create()` | 以位置和源矩形安全创建片段描述。 |
| `PixmapFragmentHint` / `PixmapFragmentHints` | 片段批量绘制提示；目前 `OpaqueHint` 表示源内容不透明。 |
