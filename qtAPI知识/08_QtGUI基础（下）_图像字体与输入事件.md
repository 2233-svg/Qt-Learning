# Qt GUI 基础（下）：图像、字体与输入事件

> 适用版本：Qt 6.11.1  
> 所属模块：Qt GUI；控件示例使用 Qt Widgets  
> 核心类型：`QImage`、`QPixmap`、`QIcon`、`QImageReader`、`QImageWriter`、`QFont`、`QFontMetrics`、`QMouseEvent`、`QKeyEvent`、`QWheelEvent`、`QTouchEvent`

## 1. 先建立选择模型

```text
需要读写像素、编解码、后台处理 → QImage
需要在屏幕控件中高效显示       → QPixmap
需要适配尺寸、状态、主题的图标   → QIcon
需要查询字体实际占用空间         → QFontMetrics / QFontMetricsF
需要处理指针、按键或触摸         → 对应输入事件
```

这些类都属于 Qt GUI，但 `QWidget` 的事件处理函数属于 Qt Widgets 使用方式。

## 2. 构建配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

纯图像处理库可只链接：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

## 3. QImage 与 QPixmap 的本质区别

| 对比 | `QImage` | `QPixmap` |
|---|---|---|
| 主要定位 | I/O 与像素处理 | 屏幕显示 |
| 像素访问 | 直接、明确 | 不作为主要用途 |
| 工作线程 | 适合独占实例处理 | 通常限 GUI 线程使用 |
| 格式 | 多种明确像素格式 | 由窗口系统优化 |
| 典型操作 | 滤镜、编码、逐行处理 | Label、按钮图标、绘制缓存 |

常见流程：

```text
文件 → QImageReader → QImage → 后台处理
                              ↓ 回主线程
                       QPixmap::fromImage → 显示
```

## 4. QImage 基础

```cpp
QImage image(640, 480, QImage::Format_ARGB32_Premultiplied);
image.fill(Qt::transparent);

QPainter painter(&image);
painter.setBrush(Qt::green);
painter.drawEllipse(QRectF(100, 80, 200, 200));
```

新建图像的像素未必初始化，绘制前应 `fill()`。

### 4.1 常用格式

| 格式 | 用途 |
|---|---|
| `Format_RGB32` | 不需要透明度的 32 位图像 |
| `Format_ARGB32` | 直通 alpha |
| `Format_ARGB32_Premultiplied` | 预乘 alpha，QPainter 常用高效格式 |
| `Format_RGBA8888` | 按字节 RGBA，便于外部协议交换 |
| `Format_Grayscale8` | 8 位灰度 |
| `Format_Alpha8` | 仅 alpha 蒙版 |

预乘格式要求颜色通道已乘 alpha。例如半透明红色的红通道也会减小。直接写像素时必须遵守格式定义。

Qt 文档建议把频繁 QPainter 绘制的目标优先转换为 `RGB32` 或 `ARGB32_Premultiplied` 等优化格式。`Indexed8` 和 `CMYK8888` 不能作为 QPainter 的直接绘制目标。

### 4.2 加载与保存

```cpp
QImage image;
if (!image.load("photo.png"))
    qWarning() << "load failed";

if (!image.save("result.webp", "WEBP", 90))
    qWarning() << "save failed";
```

简单 API 适合默认行为。需要错误信息、尺寸限制、裁剪或动画元数据时使用 Reader/Writer。

## 5. QImageReader：可控解码

```cpp
QImageReader reader(path);
reader.setAutoTransform(true); // 应用 EXIF 方向等变换

if (!reader.canRead()) {
    qWarning() << reader.errorString();
    return;
}

QSize size = reader.size();
reader.setScaledSize(size.scaled(800, 800, Qt::KeepAspectRatio));
QImage image = reader.read();
```

解码时缩放通常比先解码巨图再缩放更省内存。面对外部文件，应在读取前检查尺寸，防止恶意压缩图片解码成超大像素缓冲。

可查询支持格式：

```cpp
const auto formats = QImageReader::supportedImageFormats();
```

## 6. QImageWriter：格式和质量

```cpp
QImageWriter writer("output.jpg", "jpg");
writer.setQuality(88);
writer.setOptimizedWrite(true);

if (!writer.write(image))
    qWarning() << writer.errorString();
```

质量参数的精确含义由插件格式决定，不同格式不能机械比较同一个数值。JPEG 不支持透明度，保存前要决定如何合成背景。

## 7. 直接访问像素

低性能但直观：

```cpp
QColor color = image.pixelColor(x, y);
image.setPixelColor(x, y, color.darker());
```

批量处理应按行访问：

```cpp
QImage image = source.convertToFormat(QImage::Format_RGBA8888);

for (int y = 0; y < image.height(); ++y) {
    uchar *row = image.scanLine(y);
    for (int x = 0; x < image.width(); ++x) {
        uchar *pixel = row + x * 4;
        pixel[0] = 255 - pixel[0]; // R
        pixel[1] = 255 - pixel[1]; // G
        pixel[2] = 255 - pixel[2]; // B
    }
}
```

不能假设所有格式都是每像素 4 字节，也不能忽略 `bytesPerLine()` 的行对齐。先转换到已知格式，再按该格式访问。

只读时使用 `constBits()` / `constScanLine()`，避免触发隐式共享分离。

## 8. 外部内存构造图像

```cpp
QImage view(buffer, width, height, stride,
            QImage::Format_RGBA8888);
```

默认不会复制外部缓冲。缓冲区必须在图像及其未分离副本使用期间保持有效，步长和对齐必须正确。无法证明生命周期时立即复制：

```cpp
QImage owned = view.copy();
```

也可提供 cleanup function 管理外部存储，但它必须线程安全且与真实分配方式匹配。

## 9. 隐式共享与线程

```cpp
QImage a = loadImage();
QImage b = a;          // 先共享像素数据
b.setPixelColor(0, 0, Qt::red); // 写入时分离
```

按值跨线程传递 QImage 通常便宜。但“可重入 + 隐式共享”不等于可以同时修改同一实例：

- 多线程只读共享可以；
- 每个线程修改自己的副本可以；
- 一个线程写、另一个线程读同一实例不可以；
- 调用 `bits()` 可能触发分离并取得可写指针。

## 10. 图像变换与比例

```cpp
QImage thumb = image.scaled(
    QSize(320, 240),
    Qt::KeepAspectRatio,
    Qt::SmoothTransformation);
```

比例模式：

- `IgnoreAspectRatio`：强制目标尺寸，可能变形；
- `KeepAspectRatio`：完整显示，可能留空；
- `KeepAspectRatioByExpanding`：铺满目标，可能需要裁剪。

旋转等任意变换：

```cpp
QTransform t;
t.rotate(90);
QImage rotated = image.transformed(t, Qt::SmoothTransformation);
```

## 11. QPixmap：用于显示

```cpp
QPixmap pixmap = QPixmap::fromImage(image);
label->setPixmap(pixmap);
```

加载屏幕资源也可直接：

```cpp
QPixmap pixmap(":/images/banner.png");
if (pixmap.isNull())
    qWarning() << "invalid pixmap";
```

Pixmap 由 GUI 平台优化，像素处理先转成 QImage：

```cpp
QImage editable = pixmap.toImage();
process(editable);
QPixmap result = QPixmap::fromImage(std::move(editable));
```

频繁来回转换会有成本，应让处理管线长期保持 QImage，只在显示边界转换。

## 12. 高 DPI 图像

```cpp
QPixmap pixmap("icon@2x.png");
pixmap.setDevicePixelRatio(2.0);
```

一个 64×64 像素、DPR 为 2 的 Pixmap 逻辑尺寸为 32×32。使用 `deviceIndependentSize()` 可直接取得逻辑尺寸。

不要同时手动把控件尺寸扩大两倍，否则会重复缩放。

## 13. QIcon：按状态取正确图像

Icon 可保存多个尺寸、Mode 和 State：

```cpp
QIcon icon;
icon.addFile(":/icons/save.png", {}, QIcon::Normal, QIcon::Off);
icon.addFile(":/icons/save-disabled.png", {}, QIcon::Disabled, QIcon::Off);
button->setIcon(icon);
```

Mode 包括 `Normal`、`Disabled`、`Active`、`Selected`；State 包括 `On`、`Off`。

主题图标：

```cpp
QIcon icon = QIcon::fromTheme("document-save",
                              QIcon(":/icons/save.png"));
```

提供资源回退，避免目标系统主题缺少图标时按钮为空。

## 14. 字体不是固定像素模板

`QFont` 是字体请求：

```cpp
QFont font("Microsoft YaHei");
font.setPointSizeF(11.0);
font.setWeight(QFont::DemiBold);
font.setItalic(false);
```

系统会根据可用字体匹配实际字形。字体族不存在、字形缺失时会回退，因此不同系统排版可能略有差异。

- point size 适合随 DPI 缩放的界面文本；
- pixel size 适合必须按像素控制的特殊绘制；
- 不要同时依赖两种尺寸。

## 15. QFontMetrics 与 QFontMetricsF

```cpp
QFontMetricsF fm(font);
qreal width = fm.horizontalAdvance(text);
qreal height = fm.height();
QRectF bounds = fm.boundingRect(text);
```

关键区别：

- `horizontalAdvance()`：排版后光标前进距离；
- `boundingRect()`：实际墨迹的包围矩形，可能从负 x 开始；
- `tightBoundingRect()`：更紧的墨迹边界，但通常更贵；
- `height()`：常用行高；
- `ascent()`：基线上方；
- `descent()`：基线下方；
- `leading()`：推荐额外行间距。

布局下一段文字的位置通常使用 advance，不用 bounding width。

省略文本：

```cpp
QString shown = fm.elidedText(text, Qt::ElideRight, availableWidth);
```

## 16. 输入事件的共同规则

输入事件沿 Qt 事件系统送达目标对象。重写专用处理函数时：

```cpp
void Canvas::mousePressEvent(QMouseEvent *event)
{
    if (canHandle(event)) {
        event->accept();
        // 处理
        return;
    }
    QWidget::mousePressEvent(event); // 保留默认行为和传播
}
```

`accept()` 表示当前对象处理了事件；`ignore()` 允许进一步传播。是否调用基类会影响快捷键、焦点、拖拽和父控件行为。

## 17. QMouseEvent

```cpp
void Canvas::mousePressEvent(QMouseEvent *e)
{
    if (e->button() == Qt::LeftButton) {
        dragStart_ = e->position();
        e->accept();
    }
}
```

必须区分：

- `button()`：触发本次按下或释放的那个按钮；移动事件通常是 `NoButton`；
- `buttons()`：事件发生时所有仍按下按钮的位掩码；
- `modifiers()`：Ctrl、Shift、Alt 等修饰键；
- `position()`：接收控件局部浮点坐标；
- `globalPosition()`：屏幕或虚拟桌面坐标。

拖动判断：

```cpp
void Canvas::mouseMoveEvent(QMouseEvent *e)
{
    if (e->buttons().testFlag(Qt::LeftButton))
        moveSelection(e->position());
}
```

需要鼠标未按键时也接收移动事件：

```cpp
setMouseTracking(true);
```

## 18. 坐标转换

控件局部、窗口、全局和场景坐标不可混用。

```cpp
QPoint global = mapToGlobal(localPoint);
QPoint local = mapFromGlobal(global);
```

若画布使用缩放和平移，需要再应用视图矩阵的逆变换，把鼠标位置转为模型坐标：

```cpp
QPointF modelPos = viewTransform.inverted().map(e->position());
```

实际代码必须检查矩阵是否可逆。

## 19. QKeyEvent

```cpp
void Editor::keyPressEvent(QKeyEvent *e)
{
    if (e->matches(QKeySequence::Copy)) {
        copySelection();
        e->accept();
        return;
    }

    if (e->key() == Qt::Key_Escape) {
        cancelOperation();
        return;
    }

    QWidget::keyPressEvent(e);
}
```

- `key()` 表示逻辑按键；
- `text()` 表示按键产生的文本；
- `modifiers()` 表示修饰键；
- `isAutoRepeat()` 判断长按自动重复；
- `count()` 是本次事件包含的字符数量。

文本输入不应只拼 `key()`，因为输入法组合、键盘布局和 Unicode 文本更复杂。普通文本编辑优先使用 Qt 的编辑控件或输入法事件体系。

## 20. 焦点与快捷键

控件必须有适当焦点策略才能接收键盘事件：

```cpp
setFocusPolicy(Qt::StrongFocus);
```

应用命令优先使用 `QAction` + `QKeySequence`，可统一菜单、工具栏和快捷键状态。只有控件内部编辑语义才直接重写按键事件。

## 21. QWheelEvent

```cpp
void Canvas::wheelEvent(QWheelEvent *e)
{
    if (!e->pixelDelta().isNull()) {
        scrollBy(e->pixelDelta());
    } else {
        const QPoint steps = e->angleDelta() / 120;
        scrollBySteps(steps);
    }
    e->accept();
}
```

- `pixelDelta()`：触控板等设备提供像素级滚动，部分平台为空；
- `angleDelta()`：传统滚轮角度增量，常见一格为 120，但应累积不足一格的小增量；
- `isInverted()`：系统是否启用自然滚动；
- `phase()`：滚动开始、更新、结束阶段；
- `position()`：事件局部位置。

不要只判断 `angleDelta().y() > 0` 就假设所有设备都按固定格移动。

## 22. 触摸与 QEventPoint

Widget 默认需启用触摸事件：

```cpp
setAttribute(Qt::WA_AcceptTouchEvents);
```

`QAbstractScrollArea` 子类应对 `viewport()` 设置该属性。

```cpp
bool Canvas::event(QEvent *event)
{
    switch (event->type()) {
    case QEvent::TouchBegin:
    case QEvent::TouchUpdate:
    case QEvent::TouchEnd: {
        auto *touch = static_cast<QTouchEvent *>(event);
        for (const QEventPoint &point : touch->points()) {
            usePoint(point.id(), point.position(),
                     point.pressure(), point.state());
        }
        return true;
    }
    case QEvent::TouchCancel:
        cancelGesture();
        return true;
    default:
        return QWidget::event(event);
    }
}
```

每个点有稳定 `id()`，状态包括 Pressed、Updated、Stationary、Released。还可查询 `pressPosition()`、`lastPosition()`、`globalPosition()`、速度和压力等，但设备不一定提供所有信息。

如果 `TouchBegin` 未被接受，后续 Update/End 通常不会继续送给该控件。收到 `TouchCancel` 时必须放弃整个当前序列并恢复一致状态。

## 23. 鼠标与触摸合成

平台可能从触摸生成兼容鼠标事件。如果同时处理两套输入，可能让一次触摸执行两遍逻辑。

设计时应决定：

- 只处理统一的指针抽象；
- 或明确接受触摸并阻止对应合成路径；
- 或对来源设备去重。

不要以“某台开发机只收到一种事件”为跨平台依据。

## 24. 输入状态机

拖拽、框选和手势不是单个事件，而是一段序列：

```text
Idle
  └─ Press → Pressed
       ├─ Move 超过阈值 → Dragging
       │       ├─ Move → 更新
       │       └─ Release → Commit → Idle
       ├─ Release → Click → Idle
       └─ Cancel / FocusOut → Rollback → Idle
```

必须处理取消、焦点丢失、窗口停用和触摸取消，否则控件可能永久留在“正在拖动”状态。

拖动阈值应使用 `QStyleHints::startDragDistance()` 等平台设置，而不是硬编码 3 像素。

## 25. 常见错误

### 25.1 逐像素 API 处理大图

`pixelColor()` / `setPixelColor()` 方便但函数调用多。批量滤镜先转已知格式并使用 scan line。

### 25.2 不检查 isNull

加载失败后的空图像继续缩放或显示，会掩盖真实路径和插件错误。使用 Reader 的 `errorString()`。

### 25.3 把 QPixmap 放到工作线程处理

后台处理使用 QImage，回主线程后再转换为 Pixmap。

### 25.4 用 boundingRect 宽度排下一个词

墨迹边界与排版前进量不同。文本串接位置使用 `horizontalAdvance()`。

### 25.5 mouseMoveEvent 检查 button

移动事件的 `button()` 通常是 NoButton；判断拖动使用 `buttons()`。

### 25.6 忽略滚轮小增量

高精度设备可能多次提供小于 120 的角度增量。应累积，或优先使用 pixel delta。

### 25.7 吞掉所有按键

无条件 accept 会破坏 Tab 焦点导航、父控件快捷键等。只消费真正处理的事件，其余调用基类。

## 26. API 速查表

| API | 作用 | 注意点 |
|---|---|---|
| `QImage::load/save` | 简单编解码 | 失败检查返回值 |
| `QImageReader::read` | 可控解码 | 检查尺寸和错误字符串 |
| `convertToFormat()` | 转像素格式 | 可能分配并转换整图 |
| `scanLine()` | 可写行指针 | 严格匹配 format 和 stride |
| `constScanLine()` | 只读行指针 | 避免无意分离 |
| `QPixmap::fromImage()` | 转屏幕图像 | 通常在 GUI 线程 |
| `QIcon::fromTheme()` | 读取主题图标 | 提供 fallback |
| `horizontalAdvance()` | 文本前进距离 | 用于排版位置 |
| `boundingRect()` | 字形墨迹边界 | 不等于 advance |
| `QMouseEvent::button()` | 本次变化按钮 | Move 通常 NoButton |
| `buttons()` | 当前按下按钮集合 | 用于拖动 |
| `QWheelEvent::pixelDelta()` | 像素滚动 | 可能为空 |
| `angleDelta()` | 角度滚动 | 支持累积小增量 |
| `QTouchEvent::points()` | 当前触点列表 | TouchCancel 时可能为空 |
| `QEvent::accept/ignore` | 控制处理和传播 | 未处理事件交给基类 |

## 27. 自测题

### 题 1：滤镜和显示分别选什么

<details><summary>答案</summary>

滤镜处理使用 QImage；主线程屏幕显示可转换为 QPixmap，按钮等多状态资源使用 QIcon。
</details>

### 题 2：为什么使用 horizontalAdvance

<details><summary>答案</summary>

它表示排版后下一个位置的前进距离。boundingRect 是实际墨迹边界，可能有负边距或与逻辑前进量不同。
</details>

### 题 3：拖动时检查哪个鼠标属性

<details><summary>答案</summary>

检查 `buttons()` 是否包含 LeftButton；`button()` 表示触发当前事件的按钮，在移动事件中通常为 NoButton。
</details>

### 题 4：TouchBegin 为何重要

<details><summary>答案</summary>

它决定控件是否接管本次触摸序列。未接受 Begin 时，后续 Update 和 End 通常不会继续发送给该控件。
</details>

### 题 5：外部缓冲 QImage 最大风险是什么

<details><summary>答案</summary>

QImage 默认不复制该内存，缓冲必须在所有相关图像使用期间有效，且 stride、格式和清理方式必须正确。无法保证时调用 `copy()` 获得自有数据。
</details>

## 28. 本篇总结

1. QImage 面向像素、I/O 和后台处理，QPixmap 面向屏幕，QIcon 面向状态化图标。
2. 批量像素处理先统一格式，再按 scan line 和真实 stride 访问。
3. 隐式共享降低传值成本，但不允许多个线程并发修改同一实例。
4. 字体测量中 advance 用于排版推进，bounding rect 用于墨迹范围。
5. 鼠标事件的 button 与 buttons、局部与全局坐标不能混淆。
6. 滚轮需要兼容像素增量和高精度角度增量。
7. 输入交互应按完整状态序列设计，并处理取消和焦点丢失。

至此，Qt GUI 的绘制、图像、字体和基础输入主线已经完整建立。下一章进入 Qt Widgets，讲清 `QWidget`、顶层窗口、几何、可见性、焦点、样式和窗口生命周期。
