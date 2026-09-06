# QClipboard

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QClipboard` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QClipboard` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QClipboard>`
- 继承自：QObject
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

- `enum Mode { Clipboard, Selection, FindBuffer }`

### 公有函数

- `void clear(QClipboard::Mode mode = Clipboard)`
- `QImage image(QClipboard::Mode mode = Clipboard) const`
- `const QMimeData * mimeData(QClipboard::Mode mode = Clipboard) const`
- `bool ownsClipboard() const`
- `bool ownsFindBuffer() const`
- `bool ownsSelection() const`
- `QPixmap pixmap(QClipboard::Mode mode = Clipboard) const`
- `void setImage(const QImage &image, QClipboard::Mode mode = Clipboard)`
- `void setMimeData(QMimeData *src, QClipboard::Mode mode = Clipboard)`
- `void setPixmap(const QPixmap &pixmap, QClipboard::Mode mode = Clipboard)`
- `void setText(const QString &text, QClipboard::Mode mode = Clipboard)`
- `bool supportsFindBuffer() const`
- `bool supportsSelection() const`
- `QString text(QClipboard::Mode mode = Clipboard) const`
- `QString text(QString &subtype, QClipboard::Mode mode = Clipboard) const`

### 信号

- `void changed(QClipboard::Mode mode)`
- `void dataChanged()`
- `void findBufferChanged()`
- `void selectionChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QClipboard::Mode`

**作用与语义：**

该枚举类型用于控制系统剪贴板中`QClipboard::mimeData()`、`QClipboard::setMimeData()`及相关功能使用的部分。
- `QClipboard::Clipboard`：`0`;表示数据应存储并从全局剪贴板检索。
- `QClipboard::Selection`：`1`;表示数据应存储并从全局鼠标选择中检索。仅在拥有全局鼠标选择的系统（例如 X11）上支持 `Selection`。
- `QClipboard::FindBuffer`：`2`;表示数据应存储并从查找缓冲区检索。该模式用于在macOS上保留搜索字符串。

### `[signal] void QClipboard::changed(QClipboard::Mode mode)`

**作用与语义：**

当给定剪贴板`mode`的数据发生变化时，会发出该信号。

### `void QClipboard::clear(QClipboard::Mode mode = Clipboard)`

**作用与语义：**

清理剪贴板里的内容。
`mode`参数用于控制系统剪贴板的哪个部分被使用。如果`mode`为`QClipboard::Clipboard`，该函数会清除全局剪贴板内容。如果`mode` `QClipboard::Selection`，该函数会清除全局鼠标选择内容。如果`mode` `QClipboard::FindBuffer`，该函数会清除搜索字符串缓冲区。

### `[signal] void QClipboard::dataChanged()`

**作用与语义：**

当剪贴板数据被更改时，会发出该信号。
在macOS及Qt 4.3及以上版本中，只有在应用程序激活时，其他应用程序所做的剪贴板更改才会被检测到。

### `[signal] void QClipboard::findBufferChanged()`

**作用与语义：**

当查找缓冲区发生变化时，该信号会发出。这只适用于macOS。
在Qt 4.3及以上版本中，只有在应用程序被激活时，其他应用程序所做的剪贴板更改才会被检测到。

### `QImage QClipboard::image(QClipboard::Mode mode = Clipboard) const`

**作用与语义：**

返回剪贴板图像，或者如果剪贴板中没有图片或包含不支持的图片格式的图片，则返回空图像。
`mode`参数用于控制系统剪贴板的哪个部分被使用。如果`mode` `QClipboard::Clipboard`，则从全局剪贴板中检索图像。如果`mode` `QClipboard::Selection`，则从全局鼠标选择中检索图像。

### `const QMimeData *QClipboard::mimeData(QClipboard::Mode mode = Clipboard) const`

**作用与语义：**

返回指向当前剪贴板数据的`QMimeData`表示（如果平台不支持给定`mode`，可以返回`nullptr`）。
`mode`参数用于控制系统剪贴板的哪个部分被使用。如果`mode` `QClipboard::Clipboard`，数据从全局剪贴板中检索。如果`mode` `QClipboard::Selection`，则从全局鼠标选择中检索数据。如果`mode` `QClipboard::FindBuffer`，则从搜索字符串缓冲区检索数据。
`text()`、`image()`和`pixmap()`功能是更简单的封装器，用于检索文本、图像和像素地图数据。
注意：当剪贴板内容发生变化时，返回的指针可能会失效;无论是调用某个设置器函数，还是系统剪贴板的外部更改。

### `bool QClipboard::ownsClipboard() const`

**作用与语义：**

如果该剪贴板对象拥有剪贴板数据，则返回`true`;否则返回`false`。

### `bool QClipboard::ownsFindBuffer() const`

**作用与语义：**

如果该剪贴板对象拥有查找缓冲区数据，则返回`true`;否则返回`false`。

### `bool QClipboard::ownsSelection() const`

**作用与语义：**

如果该剪贴板对象拥有鼠标选择数据，返回`true`;否则返回`false`。

### `QPixmap QClipboard::pixmap(QClipboard::Mode mode = Clipboard) const`

**作用与语义：**

返回剪贴板像素映射，如果夹板中没有像素映射，则返回空。注意这可能会丢失信息。例如，如果图像是24位，显示是8位，结果会转换成8位;如果图像有alpha通道，结果则带有遮罩。
`mode`参数用于控制系统剪贴板的哪个部分被使用。如果`mode`是`QClipboard::Clipboard`，则从全局剪贴板中检索像素地图。如果`mode` `QClipboard::Selection`，则从全局鼠标选择中获取像素地图。

### `[signal] void QClipboard::selectionChanged()`

**作用与语义：**

当选择发生变化时，会发出该信号。这只适用于支持选择的窗口系统，例如 X11。Windows 和 macOS 不支持选择。

### `void QClipboard::setImage(const QImage &image, QClipboard::Mode mode = Clipboard)`

**作用与语义：**

把`image`复制到剪贴板里。
`mode`参数用于控制系统剪贴板的哪个部分被使用。如果`mode` `QClipboard::Clipboard`，图像存储在全局剪贴板中。如果`mode` `QClipboard::Selection`，数据存储在全局鼠标选择中。
这是以下的简写：

**官方示例：**

```cpp
 QMimeData *data = new QMimeData;
 data->setImageData(image);
 clipboard->setMimeData(data, mode);
```

### `void QClipboard::setMimeData(QMimeData *src, QClipboard::Mode mode = Clipboard)`

**作用与语义：**

将剪贴板数据设置为`src`。数据的所有权转移到剪贴板上。如果你想删除数据，可以调用`clear()`，或者再次调用 setMimeData()，并带上新数据。
`mode`参数用于控制系统剪贴板的哪个部分被使用。如果`mode` `QClipboard::Clipboard`，数据存储在全局剪贴板中。如果`mode` `QClipboard::Selection`，数据存储在全局鼠标选择中。如果`mode` `QClipboard::FindBuffer`，数据存储在搜索字符串缓冲区。
`setText()`、`setImage()`和`setPixmap()`功能分别是更简单的文本、图像和像素地图数据的封装器。

### `void QClipboard::setPixmap(const QPixmap &pixmap, QClipboard::Mode mode = Clipboard)`

**作用与语义：**

复制`pixmap`到剪贴板中。注意这比`setImage()`慢，因为需要先把`QPixmap`转换成`QImage`。
`mode`参数用于控制系统剪贴板的哪个部分被使用。如果`mode` `QClipboard::Clipboard`，像素地图存储在全局剪贴板中。如果`mode` `QClipboard::Selection`，像素映射存储在全局鼠标选择中。

### `void QClipboard::setText(const QString &text, QClipboard::Mode mode = Clipboard)`

**作用与语义：**

副本`text`在剪贴板中以纯文本形式呈现。
`mode`参数用于控制系统剪贴板的哪个部分被使用。如果`mode`是`QClipboard::Clipboard`，文本存储在全局剪贴板中。如果`mode` `QClipboard::Selection`，文本存储在全局鼠标选择中。如果`mode` `QClipboard::FindBuffer`，文本存储在搜索字符串缓冲区中。

### `bool QClipboard::supportsFindBuffer() const`

**作用与语义：**

如果剪贴板支持独立的搜索缓冲区，返回`true`;否则返回`false`。

### `bool QClipboard::supportsSelection() const`

**作用与语义：**

如果剪贴板支持鼠标选择，返回`true`;否则返回`false`。

### `QString QClipboard::text(QClipboard::Mode mode = Clipboard) const`

**作用与语义：**

以纯文本形式返回剪贴板文本，若夹板中没有文本则返回空字符串。
`mode`参数用于控制系统剪贴板的哪个部分被使用。如果`mode`是`QClipboard::Clipboard`，文本会从全局剪贴板中检索。如果`mode` `QClipboard::Selection`，文本会从全局鼠标选择中检索。如果`mode` `QClipboard::FindBuffer`，文本会从搜索字符串缓冲区中检索。

### `QString QClipboard::text(QString &subtype, QClipboard::Mode mode = Clipboard) const`

**作用与语义：**

返回剪贴板文本的子类型`subtype`，或者如果夹板中没有文本，则返回空字符串。如果`subtype`为空，则任何子类型都可接受，`subtype`被设置为所选子类型。
`mode`参数用于控制系统剪贴板的哪个部分被使用。如果`mode`为`QClipboard::Clipboard`，文本从全局剪贴板中检索。如果`mode`为`QClipboard::Selection`，文本从全局鼠标选择中检索。
`subtype`常见的数值是“plain”和“html”。
注意，反复调用该函数，例如从密钥事件处理程序中调用，可能会很慢。在这种情况下，你应该使用`dataChanged()`信号。

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

`QClipboard` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
