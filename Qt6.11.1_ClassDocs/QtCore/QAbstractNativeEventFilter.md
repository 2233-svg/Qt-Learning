# QAbstractNativeEventFilter

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是一个抽象接口或框架基类，重点是理解它定义的协议，并通过具体子类、工厂或回调来使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QAbstractNativeEventFilter` 是 Qt Core 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractNativeEventFilter>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QAbstractNativeEventFilter()`
- `virtual ~QAbstractNativeEventFilter()`
- `virtual bool nativeEventFilter(const QByteArray &eventType, void *message, qintptr *result) = 0`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QAbstractNativeEventFilter::QAbstractNativeEventFilter()`

**作用与语义：**

创建了原生事件过滤器。
默认情况下，这不会有任何作用。记得把它安装在应用对象上。

### `[virtual noexcept] QAbstractNativeEventFilter::~QAbstractNativeEventFilter()`

**作用与语义：**

破坏本地事件过滤器。
这会自动从应用中移除它。

### `[pure virtual] bool QAbstractNativeEventFilter::nativeEventFilter(const QByteArray &eventType, void *message, qintptr *result)`

**作用与语义：**

该方法适用于每个本地事件。
注意：这里的过滤函数接收本地消息，例如 MSG 或 XCB 事件结构。
它由 QPA 平台插件调用。在 Windows 上，则由事件调度器调用。
事件`eventType`类型针对运行时选择的平台插件，可用于将`message`投射到正确的类型。
在X11上，`eventType`设置为“xcb_generic_event_t”，`message`可以投射到xcb_generic_event_t指针。
在 Windows 上，`eventType` 设置为发送到顶层 Windows 的消息为“windows_generic_MSG”，系统范围消息（如注册热键的消息）为“windows_dispatcher_MSG”。在这两种情况下，`message`都可以投射为 MSG 指针。`result` 指针仅在 Windows 上使用，对应于 LRESULT 指针。
在macOS上，`eventType`设置为“mac_generic_NSEvent”，`message`可以投射到NSEvent指针。
在你对该函数的重新实现中，如果你想过滤掉`message`，即停止进一步处理，返回true;否则返回false。
Linux 示例。
Windows 示例。
macOS 示例。
mycocoaeventfilter.h：
mycocoaeventfilter.mm：
myapp.pro：

**官方示例：**

```cpp
 class MyXcbEventFilter : public QAbstractNativeEventFilter
 {
 public:
     bool nativeEventFilter(const QByteArray &eventType, void *message, qintptr *) override
     {
         if (eventType == "xcb_generic_event_t") {
             xcb_generic_event_t* ev = static_cast<xcb_generic_event_t *>(message);
             // ...
         }
         return false;
     }
 };
```

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractNativeEventFilter` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
