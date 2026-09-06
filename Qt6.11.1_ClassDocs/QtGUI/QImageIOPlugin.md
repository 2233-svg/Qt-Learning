# QImageIOPlugin

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QImageIOPlugin` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QImageIOPlugin` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QImageIOPlugin>`
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

- `flags Capabilities`
- `enum Capability { CanRead, CanWrite, CanReadIncremental }`

### 公有函数

- `QImageIOPlugin(QObject *parent = nullptr)`
- `virtual ~QImageIOPlugin()`
- `virtual QImageIOPlugin::Capabilities capabilities(QIODevice *device, const QByteArray &format) const = 0`
- `virtual QImageIOHandler * create(QIODevice *device, const QByteArray &format = QByteArray()) const = 0`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QImageIOPlugin::Capabilityflags QImageIOPlugin::Capabilities`

**作用与语义：**

这个枚举描述了`QImageIOPlugin`的能力。
- `QImageIOPlugin::CanRead`：`0x1`;插件可以读取图像。
- `QImageIOPlugin::CanWrite`：`0x2`;插件可以写入图片。
- `QImageIOPlugin::CanReadIncremental`：`0x4`;插件可以逐步读取图像。
能力类型是QFlag的typedef<Capability>。它存储能力值的或组合。

### `[explicit] QImageIOPlugin::QImageIOPlugin(QObject *parent = nullptr)`

**作用与语义：**

用给定的`parent`构建一个图像插件。导出插件的 MOC 生成代码会自动调用该插件。

### `[virtual noexcept] QImageIOPlugin::~QImageIOPlugin()`

**作用与语义：**

会破坏图片格式插件。
你从不需要明确调用它。Qt 会自动销毁插件，当它不再使用时。

### `[pure virtual] QImageIOPlugin::Capabilities QImageIOPlugin::capabilities(QIODevice *device, const QByteArray &format) const`

**作用与语义：**

返回插件的能力，基于`device`中的数据和格式`format`。如果`device` `0`，应仅报告格式是否可读写。否则，应尝试判断给定格式（或插件支持的任何格式，如果`format`空）是否可以从`device`读取或写入。应在不改变`device`状态的情况下完成此操作（通常通过使用`QIODevice::peek()`）。
例如，如果`QImageIOPlugin`支持BMP格式，`format`空或`"bmp"`，且设备中的数据以字符`"BM"`开头，该函数应返回`CanRead`。如果`format` `"bmp"`，`device`为`0`且处理器支持读写，该函数应返回`CanRead` |`CanWrite`。
格式名称总是用小写字母表示。

### `[pure virtual] QImageIOHandler *QImageIOPlugin::create(QIODevice *device, const QByteArray &format = QByteArray()) const`

**作用与语义：**

创建并返回一个`QImageIOHandler`子类，`device` 和 `format` 为集合。`format`必须来自插件元数据中`"Keys"`条目列出的值，否则为空。如果为空，`device` 中的数据必须被 `capabilities()` 方法识别（格式同样为空）。
格式名称总是用小写字母表示。

### `flags Capabilities`

**作用与语义：**

这个枚举描述了`QImageIOPlugin`的能力。
- `QImageIOPlugin::CanRead`：`0x1`;插件可以读取图像。
- `QImageIOPlugin::CanWrite`：`0x2`;插件可以写入图片。
- `QImageIOPlugin::CanReadIncremental`：`0x4`;插件可以逐步读取图像。
能力类型是QFlag的typedef<Capability>。它存储能力值的或组合。

### `enum Capability { CanRead, CanWrite, CanReadIncremental }`

**作用与语义：**

这个枚举描述了`QImageIOPlugin`的能力。
- `QImageIOPlugin::CanRead`：`0x1`;插件可以读取图像。
- `QImageIOPlugin::CanWrite`：`0x2`;插件可以写入图片。
- `QImageIOPlugin::CanReadIncremental`：`0x4`;插件可以逐步读取图像。
能力类型是QFlag的typedef<Capability>。它存储能力值的或组合。

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

`QImageIOPlugin` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
