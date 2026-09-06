# QPicture

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QPicture` 是 Qt GUI 绘制体系中的类型，负责画笔、画刷、字体、图像、绘制设备或绘制状态。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPicture` 是 二维绘制状态机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

**适用场景：** 开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

## 2. 依赖与对象关系

- 头文件：`#include <QPicture>`
- 继承自：QPaintDevice
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

- `QPicture(int formatVersion = -1)`
- `QPicture(const QPicture &pic)`
- `virtual ~QPicture()`
- `QRect boundingRect() const`
- `const char * data() const`
- `bool isNull() const`
- `bool load(const QString &fileName)`
- `bool load(QIODevice *dev)`
- `bool play(QPainter *painter)`
- `bool save(const QString &fileName)`
- `bool save(QIODevice *dev)`
- `void setBoundingRect(const QRect &r)`
- `virtual void setData(const char *data, uint size)`
- `uint size() const`
- `void swap(QPicture &other)`
- `QPicture & operator=(QPicture &&other)`
- `QPicture & operator=(const QPicture &p)`

### 相关非成员函数

- `QDataStream & operator<<(QDataStream &s, const QPicture &r)`
- `QDataStream & operator>>(QDataStream &s, QPicture &r)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QPicture::QPicture(int formatVersion = -1)`

**作用与语义：**

构建了一个空洞的画面。
`formatVersion`参数可用于创建一个QPicture，这些QPicture可以被用Qt早期版本编译的应用程序读取。
注意默认格式版本为-1，表示当前版本，即Qt 4.0的格式版本7与默认格式版本-1相同。
Qt 4.0 不支持阅读早期版本 Qt 生成的图片。

### `QPicture::QPicture(const QPicture &pic)`

**作用与语义：**

构建了一份`pic`的复制品。
由于隐式共享，这种构建器速度很快。

### `[virtual noexcept] QPicture::~QPicture()`

**作用与语义：**

毁了整幅画。

### `QRect QPicture::boundingRect() const`

**作用与语义：**

返回图片的边界矩形，若图片无数据则返回无效矩形。

### `const char *QPicture::data() const`

**作用与语义：**

返回指向图片数据的指针。该指针仅在该图像调用下一个非条件函数之前有效。如果图像中没有数据，返回的指针为0。

### `bool QPicture::isNull() const`

**作用与语义：**

如果图片中没有数据，则返回`true`;否则返回 false。

### `bool QPicture::load(const QString &fileName)`

**作用与语义：**

从`fileName`指定的文件加载图片，成功时返回true;否则会使图片失效并返回`false`。

### `bool QPicture::load(QIODevice *dev)`

**作用与语义：**

`dev`是装载的设备。

### `bool QPicture::play(QPainter *painter)`

**作用与语义：**

用`painter`重放图片，成功时返回`true`;否则返回`false`。
该函数在 （x， y） = （0， 0） 时与 `QPainter::drawPicture()` 完全相同。
注意：画家的状态不被该功能保留。

### `bool QPicture::save(const QString &fileName)`

**作用与语义：**

将图片保存到`fileName`指定的文件中，成功时返回true;否则返回`false`。

### `bool QPicture::save(QIODevice *dev)`

**作用与语义：**

`dev`是用于存档的设备。

### `void QPicture::setBoundingRect(const QRect &r)`

**作用与语义：**

将图片的边界矩形设置为`r`。自动计算的值被覆盖。

### `[virtual] void QPicture::setData(const char *data, uint size)`

**作用与语义：**

直接从`data`和`size`设置图像数据。该函数复制输入数据。

### `uint QPicture::size() const`

**作用与语义：**

返回图片数据的大小。

### `[noexcept] void QPicture::swap(QPicture &other)`

**作用与语义：**

把这张图和`other`交换。这个操作非常快，从未失败过。

### `[noexcept] QPicture &QPicture::operator=(QPicture &&other)`

**作用与语义：**

Move-assign `other`到这个`QPicture`实例。

### `QPicture &QPicture::operator=(const QPicture &p)`

**作用与语义：**

为该图片分配图片`p`，并返回对该图片的引用。

### `QDataStream &operator<<(QDataStream &s, const QPicture &r)`

**作用与语义：**

将图片`r`写入流`s`并返回流的引用。

### `QDataStream &operator>>(QDataStream &s, QPicture &r)`

**作用与语义：**

将流的图片`s`读取到图片`r`，并返回对流的引用。

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

`QPicture` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
