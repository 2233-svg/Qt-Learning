# QBitmap

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QBitmap` 是 Qt GUI 绘制体系中的类型，负责画笔、画刷、字体、图像、绘制设备或绘制状态。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QBitmap` 是 二维绘制状态机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

**适用场景：** 开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

## 2. 依赖与对象关系

- 头文件：`#include <QBitmap>`
- 继承自：QPixmap
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

### 状态、生命周期和线程

**生命周期：** 绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

**状态与结果：** `save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

**线程与事件循环：** 同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

## 3. 直接使用

开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
void Widget::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.save();
    // 设置画笔、画刷、字体或变换后进行绘制
    painter.restore();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QBitmap()`
- `QBitmap(const QSize &size)`
- `QBitmap(const QString &fileName, const char *format = nullptr)`
- `QBitmap(int width, int height)`
- `void clear()`
- `void swap(QBitmap &other)`
- `QBitmap transformed(const QTransform &matrix) const`
- `operator QVariant() const`

### 静态公有成员

- `QBitmap fromData(const QSize &size, const uchar *bits, QImage::Format monoFormat = QImage::Format_MonoLSB)`
- `QBitmap fromImage(const QImage &image, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `QBitmap fromImage(QImage &&image, Qt::ImageConversionFlags flags = Qt::AutoColor)`
- `(since 6.0) QBitmap fromPixmap(const QPixmap &pixmap)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QBitmap::QBitmap()`

**作用与语义：**

构造一个空位图。

### `[explicit] QBitmap::QBitmap(const QSize &size)`

**作用与语义：**

构造一个带有给定`size`的位图。位图中的像素未初始化。

### `[explicit] QBitmap::QBitmap(const QString &fileName, const char *format = nullptr)`

**作用与语义：**

从指定`fileName`指定的文件构建位图。如果文件不存在或格式未知，位图将成为空位图。
`fileName`和`format`参数传递给`QPixmap::load()`函数。如果文件格式每像素使用超过1位，生成的位图将被自动抖动。

### `QBitmap::QBitmap(int width, int height)`

**作用与语义：**

构造一个包含给定`width`和`height`的位图。内部像素未初始化。

### `void QBitmap::clear()`

**作用与语义：**

清除位图，将其所有位设置为 `Qt::color0`。

### `[static] QBitmap QBitmap::fromData(const QSize &size, const uchar *bits, QImage::Format monoFormat = QImage::Format_MonoLSB)`

**作用与语义：**

构造包含给定`size`的位图，并将内容设置为提供的`bits`。
位图数据必须对齐字节，并按照`monoFormat`指定的位序提供。单声道格式必须是 `QImage::Format_Mono` 或 `QImage::Format_MonoLSB`。使用 `QImage::Format_Mono` 来指定 XBM 格式上的数据。

### `[static] QBitmap QBitmap::fromImage(const QImage &image, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

返回使用指定的图像转换`flags`转换为位图的给定`image`副本。

### `[static] QBitmap QBitmap::fromImage(QImage &&image, Qt::ImageConversionFlags flags = Qt::AutoColor)`

**作用与语义：**

返回使用指定的图像转换`flags`转换为位图的给定`image`副本。

### `[static, since 6.0] QBitmap QBitmap::fromPixmap(const QPixmap &pixmap)`

**作用与语义：**

返回已转换成位图的`pixmap`副本。
如果像素图深度大于1，生成的位图将自动抖动。

### `void QBitmap::swap(QBitmap &other)`

**作用与语义：**

将该位图与`other`交换。此操作非常快且从未失败。

### `QBitmap QBitmap::transformed(const QTransform &matrix) const`

**作用与语义：**

返回一份根据给定的 `matrix` 转换的位图副本。

### `QBitmap::operator QVariant() const`

**作用与语义：**

返回位图为`QVariant`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

### 状态和错误边界

`save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

### 线程边界

同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

### 最容易出现的错误

不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QBitmap` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
