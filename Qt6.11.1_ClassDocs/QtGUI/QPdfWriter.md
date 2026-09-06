# QPdfWriter

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QPdfWriter` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPdfWriter` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QPdfWriter>`
- 继承自：QObject、QPagedPaintDevice
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `(since 6.8) enum class ColorModel { RGB, Grayscale, CMYK, Auto }`

### 公有函数

- `QPdfWriter(QIODevice *device)`
- `QPdfWriter(const QString &filename)`
- `virtual ~QPdfWriter()`
- `void addFileAttachment(const QString &fileName, const QByteArray &data, const QString &mimeType = QString())`
- `(since 6.9) QString author() const`
- `(since 6.8) QPdfWriter::ColorModel colorModel() const`
- `QString creator() const`
- `(since 6.8) QUuid documentId() const`
- `QByteArray documentXmpMetadata() const`
- `(since 6.8) QPdfOutputIntent outputIntent() const`
- `QPagedPaintDevice::PdfVersion pdfVersion() const`
- `int resolution() const`
- `(since 6.9) void setAuthor(const QString &author)`
- `(since 6.8) void setColorModel(QPdfWriter::ColorModel model)`
- `void setCreator(const QString &creator)`
- `(since 6.8) void setDocumentId(QUuid documentId)`
- `void setDocumentXmpMetadata(const QByteArray &xmpMetadata)`
- `(since 6.8) void setOutputIntent(const QPdfOutputIntent &intent)`
- `void setPdfVersion(QPagedPaintDevice::PdfVersion version)`
- `void setResolution(int resolution)`
- `void setTitle(const QString &title)`
- `QString title() const`

### 重实现的公有函数

- `virtual bool newPage() override`

### 重实现的保护函数

- `virtual QPaintEngine * paintEngine() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.8] enum class QPdfWriter::ColorModel`

**作用与语义：**

该枚举描述了PDF引擎如何解释描写和填充颜色的方式，设置为`QPainter`笔或画笔（通过`QPen`和`QBrush`）。
- `QPdfWriter::ColorModel::RGB`：`0`;所有颜色都转换为RGB格式，并以此格式保存在PDF中。
- `QPdfWriter::ColorModel::Grayscale`：`1`;所有颜色都转换为灰度。为了向后兼容，它们在PDF输出中以RGB颜色形式发出，红、绿、蓝三色的数量相同。
- `QPdfWriter::ColorModel::CMYK`：`2`;所有颜色都转换为CMYK并保存为CMYK。
- `QPdfWriter::ColorModel::Auto`：`3`;RGB 颜色以 RGB 形式发射;CMYK 颜色以 CMYK 形式输出。任何其他颜色规格的颜色都转换为 RGB。这是自 Qt 6.8 起的默认设置。
这个枚举是在Qt 6.8引入的。

### `[explicit] QPdfWriter::QPdfWriter(QIODevice *device)`

**作用与语义：**

构建一个PDF写入器，将pdf写入`device`。

### `[explicit] QPdfWriter::QPdfWriter(const QString &filename)`

**作用与语义：**

构建一个PDF编写器，将PDF写入`filename`。

### `[virtual noexcept] QPdfWriter::~QPdfWriter()`

**作用与语义：**

这会毁掉PDF写入器。

### `void QPdfWriter::addFileAttachment(const QString &fileName, const QByteArray &data, const QString &mimeType = QString())`

**作用与语义：**

添加`fileName`附件，附带（可选）`mimeType`。`data`包含嵌入PDF文件的原始文件数据。

### `[since 6.9] QString QPdfWriter::author() const`

**作用与语义：**

返回文档作者。

### `[since 6.8] QPdfWriter::ColorModel QPdfWriter::colorModel() const`

**作用与语义：**

返回该 PDF 写入者使用的颜色模型。默认为 `QPdfWriter::ColorModel::Auto`。

### `QString QPdfWriter::creator() const`

**作用与语义：**

返回文档创建者。

### `[since 6.8] QUuid QPdfWriter::documentId() const`

**作用与语义：**

返回文档的ID。默认情况下，ID是随机生成的UUID。

### `QByteArray QPdfWriter::documentXmpMetadata() const`

**作用与语义：**

获取文档元数据，因为调用`setDocumentXmpMetadata`时提供了它。它不会返回默认的元数据。

### `[override virtual] bool QPdfWriter::newPage()`

**作用与语义：**

重装：`QPagedPaintDevice::newPage()`。
开始新的一页。成功时`true`回来。

### `[since 6.8] QPdfOutputIntent QPdfWriter::outputIntent() const`

**作用与语义：**

返回该 PDF 编写者使用的输出意图。

### `[override virtual protected] QPaintEngine *QPdfWriter::paintEngine() const`

**作用与语义：**

重实现自：`QPaintDevice::paintEngine()` const.
返回一个指向用于在设备上绘画的绘画引擎的指针。

### `QPagedPaintDevice::PdfVersion QPdfWriter::pdfVersion() const`

**作用与语义：**

为本作者返回PDF版本。默认是`PdfVersion_1_4`。

### `int QPdfWriter::resolution() const`

**作用与语义：**

返回 PDF 的分辨率（DPI）。

### `[since 6.9] void QPdfWriter::setAuthor(const QString &author)`

**作用与语义：**

将文档作者设置为`author`。

### `[since 6.8] void QPdfWriter::setColorModel(QPdfWriter::ColorModel model)`

**作用与语义：**

将该 PDF 写入器使用的颜色模型设置为`model`。

### `void QPdfWriter::setCreator(const QString &creator)`

**作用与语义：**

将文档创建者设置为`creator`。

### `[since 6.8] void QPdfWriter::setDocumentId(QUuid documentId)`

**作用与语义：**

将文档的ID设置为`documentId`。

### `void QPdfWriter::setDocumentXmpMetadata(const QByteArray &xmpMetadata)`

**作用与语义：**

设置文档元数据。这些元数据不受`setTitle`/`setCreator`方法的影响，因此用户需自行保持其一致性。`xmpMetadata`包含可嵌入PDF文件的XML格式元数据。

### `[since 6.8] void QPdfWriter::setOutputIntent(const QPdfOutputIntent &intent)`

**作用与语义：**

将该 PDF 编写者使用的输出意图设置为 `intent`。

### `void QPdfWriter::setPdfVersion(QPagedPaintDevice::PdfVersion version)`

**作用与语义：**

为本文作者设置PDF版本为`version`。
如果`version`值与当前设定相同，则不会有更改。

### `void QPdfWriter::setResolution(int resolution)`

**作用与语义：**

将PDF `resolution`设置为DPI。
该设置影响坐标系，例如返回`QPainter::viewport()`。

### `void QPdfWriter::setTitle(const QString &title)`

**作用与语义：**

将正在创建的文档标题设置为`title`。

### `QString QPdfWriter::title() const`

**作用与语义：**

返回文档标题。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPdfWriter` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
