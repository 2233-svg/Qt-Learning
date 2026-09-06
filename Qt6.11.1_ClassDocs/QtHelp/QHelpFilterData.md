# QHelpFilterData

> Qt 6.11.1 · Qt Help

## 1. 先建立直觉

**一句话定位：** `QHelpFilterData` 是 Qt 的值类型，围绕“帮助过滤数据”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** 这是 Qt Help 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QHelpFilterData` 是 Qt 值类型与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QHelpFilterData>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Help)
target_link_libraries(mytarget PRIVATE Qt6::Help)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QHelpFilterData()`
- `QHelpFilterData(const QHelpFilterData &other)`
- `QHelpFilterData(QHelpFilterData &&other)`
- `~QHelpFilterData()`
- `QStringList components() const`
- `void setComponents(const QStringList &components)`
- `void setVersions(const QList<QVersionNumber> &versions)`
- `void swap(QHelpFilterData &other)`
- `QList<QVersionNumber> versions() const`
- `QHelpFilterData & operator=(QHelpFilterData &&other)`
- `QHelpFilterData & operator=(const QHelpFilterData &other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QHelpFilterData::QHelpFilterData()`

**作用与语义：**

构造空过滤器。

### `QHelpFilterData::QHelpFilterData(const QHelpFilterData &other)`

**作用与语义：**

复制了`other`。

### `QHelpFilterData::QHelpFilterData(QHelpFilterData &&other)`

**作用与语义：**

Move-构造一个QHelpFilterData实例，使其指向`other`指向的同一个对象。

### `[noexcept] QHelpFilterData::~QHelpFilterData()`

**作用与语义：**

会破坏过滤器。

### `QStringList QHelpFilterData::components() const`

**作用与语义：**

返回用于筛选搜索结果的组件列表。

### `void QHelpFilterData::setComponents(const QStringList &components)`

**作用与语义：**

指定用于筛选搜索结果的组件列表。仅返回列表中组件`components`的结果。

### `void QHelpFilterData::setVersions(const QList<QVersionNumber> &versions)`

**作用与语义：**

指定用于筛选搜索结果的版本列表。仅返回列表中版本`versions`的结果。

### `[noexcept] void QHelpFilterData::swap(QHelpFilterData &other)`

**作用与语义：**

将过滤器`other`与这个过滤器交换。这个操作非常快，且从未出错。

### `QList<QVersionNumber> QHelpFilterData::versions() const`

**作用与语义：**

返回用于筛选搜索结果的版本列表。

### `QHelpFilterData &QHelpFilterData::operator=(QHelpFilterData &&other)`

**作用与语义：**

Move-assign `other`到该`QHelpFilterData`实例。

### `QHelpFilterData &QHelpFilterData::operator=(const QHelpFilterData &other)`

**作用与语义：**

将`other`分配给该滤波器，并返回对该滤波器的引用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QHelpFilterData` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
