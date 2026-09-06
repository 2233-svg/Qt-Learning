# QBackingStore

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QBackingStore` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QBackingStore>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QBackingStore(QWindow *window)`
- `~QBackingStore()`
- `void beginPaint(const QRegion &region)`
- `void endPaint()`
- `void flush(const QRegion &region, QWindow *window = nullptr, const QPoint &offset = QPoint())`
- `QPlatformBackingStore * handle() const`
- `bool hasStaticContents() const`
- `QPaintDevice * paintDevice()`
- `void resize(const QSize &size)`
- `bool scroll(const QRegion &area, int dx, int dy)`
- `void setStaticContents(const QRegion &region)`
- `QSize size() const`
- `QRegion staticContents() const`
- `QWindow * window() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QBackingStore::QBackingStore(QWindow *window)`

**作用与语义：**

为给定的顶层`window`构造一个空曲面。

### `[noexcept] QBackingStore::~QBackingStore()`

**作用与语义：**

会破坏这个表面。

### `void QBackingStore::beginPaint(const QRegion &region)`

**作用与语义：**

在指定`region`开始在背衬表面上作画。
你应该在用`paintDevice()`来绘画之前调用这个函数。

### `void QBackingStore::endPaint()`

**作用与语义：**

画完。
你应该在`paintDevice()`结束后调用这个功能。

### `void QBackingStore::flush(const QRegion &region, QWindow *window = nullptr, const QPoint &offset = QPoint())`

**作用与语义：**

将指定`window`的`region`冲入屏幕。
`window`必须是该 backingstore 代表的顶层窗口，或该窗口的非瞬态子窗口。传递`nullptr`则回归使用backingstore的顶层窗口。
如果 `window` 是子窗口，`region` 应该在子窗口坐标中，`offset` 应该是子窗口相对于 backingstore 顶层窗口的偏移量。
你应该在用`endPaint()`结束绘画后调用这个函数。

### `QPlatformBackingStore *QBackingStore::handle() const`

**作用与语义：**

返回指向 QPlatformBackingStore 实现的指针。

### `bool QBackingStore::hasStaticContents() const`

**作用与语义：**

返回一个布尔值，表示该窗口是否有静态内容。

### `QPaintDevice *QBackingStore::paintDevice()`

**作用与语义：**

退还了该表面的喷漆设备。
警告：该设备仅在调用`beginPaint()`和`endPaint()`之间有效。你不应缓存返回的值。

### `void QBackingStore::resize(const QSize &size)`

**作用与语义：**

将窗户表面的尺寸设置为`size`。

### `bool QBackingStore::scroll(const QRegion &area, int dx, int dy)`

**作用与语义：**

将给定的`area` `dx`像素向右滚动，向下`dy`滚动;`dx`和`dy`都可能是负数。
如果该区域成功滚动，返回`true`;否则返回。

### `void QBackingStore::setStaticContents(const QRegion &region)`

**作用与语义：**

将`region`设为该窗口的静态内容。

### `QSize QBackingStore::size() const`

**作用与语义：**

返回当前窗口表面的大小。

### `QRegion QBackingStore::staticContents() const`

**作用与语义：**

返回一个表示窗口中静态内容区域的`QRegion`。

### `QWindow *QBackingStore::window() const`

**作用与语义：**

返回指向该表面对应的顶层窗口的指针。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QBackingStore` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
