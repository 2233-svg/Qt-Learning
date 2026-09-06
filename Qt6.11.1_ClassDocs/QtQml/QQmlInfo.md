# QQmlInfo

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QQmlInfo` 是带 QML 对象上下文的日志流句柄，由 `qmlDebug()`、`qmlInfo()` 或 `qmlWarning()` 返回。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QQmlInfo` 是带 QML 对象上下文的日志流句柄，由 `qmlDebug()`、`qmlInfo()` 或 `qmlWarning()` 返回。

**内部模型：** 它沿用 QDebug 的 `operator<<` 拼接内容。表达式末尾临时 QQmlInfo 析构时，Qt 才把整条消息连同对象对应的 QML 文件和行号上下文输出。它不是一个需要长期保存的日志对象。

**适用场景：** C++ 代码需要报告与某个 QML 对象相关的诊断信息，并希望日志包含 QML 来源位置时使用。

**典型调用链：** 选择 qmlDebug/qmlInfo/qmlWarning -> 传入相关 QObject -> 用 << 追加消息 -> 表达式结束时输出。

**先记住的坑：** 传入对象必须有效；不要长期保存临时日志句柄；日志级别不同，可能受过滤规则影响；不要在日志处理器中递归产生日志。

## 2. 依赖与对象关系

- 头文件：`#include <QQmlInfo>`
- 继承自：QDebug
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Qml)
target_link_libraries(mytarget PRIVATE Qt6::Qml)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

它沿用 QDebug 的 `operator<<` 拼接内容。表达式末尾临时 QQmlInfo 析构时，Qt 才把整条消息连同对象对应的 QML 文件和行号上下文输出。它不是一个需要长期保存的日志对象。

### 状态、生命周期和线程

**生命周期：** 日志上下文通常是一次消息表达式的临时对象；自定义 message handler 的安装和卸载要覆盖整个使用期，处理器内部不要递归调用会再次触发日志的代码。

**状态与结果：** 日志是否输出受级别、类别规则、编译宏和运行时过滤影响。看到某条消息缺失时，要区分代码没有执行、日志级别被过滤、上下文被关闭和 handler 改写输出。

**线程与事件循环：** 日志可能来自多个线程，handler 必须考虑并发、输出原子性和不能阻塞业务线程；不要在 handler 中访问未加锁的 GUI 控件。

## 3. 直接使用

C++ 代码需要报告与某个 QML 对象相关的诊断信息，并希望日志包含 QML 来源位置时使用。 使用时通常按这个过程组织：选择 qmlDebug/qmlInfo/qmlWarning -> 传入相关 QObject -> 用 << 追加消息 -> 表达式结束时输出。

```cpp
#include <QQmlInfo>

qmlWarning(object) << "property value is invalid:" << value;
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 相关非成员函数

- `QQmlInfo qmlDebug(const QObject *object)`
- `QQmlInfo qmlInfo(const QObject *object)`
- `QQmlInfo qmlWarning(const QObject *object)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QQmlInfo qmlDebug(const QObject *object)`

**作用与语义：**

打印包含指定QML文件和行号的调试消息`object`。
当QML类型生成日志消息时，如果包含该实例所处的QML文件和行号，则可提升可追溯性。
要包含文件和行号，必须传递一个对象。如果该实例无法提供文件和行号（要么未被 QML 引擎实例化，要么位置信息被禁用），则会使用“未知位置”。
例如，。
版画。

**官方示例：**

```cpp
 qmlDebug(object) << "Internal state: 42";
```

### `QQmlInfo qmlInfo(const QObject *object)`

**作用与语义：**

打印包含指定QML文件和行号的信息`object`。
当QML类型生成日志消息时，如果包含该实例所处的QML文件和行号，则可提升可追溯性。
要包含文件和行号，必须传递一个对象。如果该实例无法提供文件和行号（要么未被 QML 引擎实例化，要么位置信息被禁用），则会使用“未知位置”。
例如，。
版画。
注意：在Qt 5.9之前的版本中，qmlInfo通过警告`QtMsgType`报告消息。对于Qt 5.9及以上版本，qmlInfo使用信息`QtMsgType`。发送警告请使用`qmlWarning`。

**官方示例：**

```cpp
 qmlInfo(object) << tr("component property is a write-once property");
```

### `QQmlInfo qmlWarning(const QObject *object)`

**作用与语义：**

打印包含指定QML文件和行号的警告消息`object`。
当QML类型生成日志消息时，如果包含该实例所处的QML文件和行号，则可提升可追溯性。
要包含文件和行号，必须传递一个对象。如果该实例无法提供文件和行号（要么未被 QML 引擎实例化，要么位置信息被禁用），则会使用“未知位置”。
例如，。
版画。

**官方示例：**

```cpp
 qmlInfo(object) << tr("property cannot be set to 0");
```

## 6. 深入实践与常见坑

### 生命周期和资源边界

日志上下文通常是一次消息表达式的临时对象；自定义 message handler 的安装和卸载要覆盖整个使用期，处理器内部不要递归调用会再次触发日志的代码。

### 状态和错误边界

日志是否输出受级别、类别规则、编译宏和运行时过滤影响。看到某条消息缺失时，要区分代码没有执行、日志级别被过滤、上下文被关闭和 handler 改写输出。

### 线程边界

日志可能来自多个线程，handler 必须考虑并发、输出原子性和不能阻塞业务线程；不要在 handler 中访问未加锁的 GUI 控件。

### 最容易出现的错误

传入对象必须有效；不要长期保存临时日志句柄；日志级别不同，可能受过滤规则影响；不要在日志处理器中递归产生日志。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QQmlInfo` 所属机制类型：Qt 日志与诊断机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
