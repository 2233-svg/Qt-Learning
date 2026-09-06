# QWindowsMimeConverter

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QWindowsMimeConverter` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QWindowsMimeConverter>`
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

- `QWindowsMimeConverter()`
- `virtual ~QWindowsMimeConverter()`
- `virtual bool canConvertFromMime(const FORMATETC &formatetc, const QMimeData *mimeData) const = 0`
- `virtual bool canConvertToMime(const QString &mimeType, IDataObject *pDataObj) const = 0`
- `virtual bool convertFromMime(const FORMATETC &formatetc, const QMimeData *mimeData, STGMEDIUM *pmedium) const = 0`
- `virtual QVariant convertToMime(const QString &mimeType, IDataObject *pDataObj, QMetaType preferredType) const = 0`
- `virtual QList<FORMATETC> formatsForMime(const QString &mimeType, const QMimeData *mimeData) const = 0`
- `virtual QString mimeForFormat(const FORMATETC &formatetc) const = 0`

### 静态公有成员

- `int registerMimeType(const QString &mimeType)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QWindowsMimeConverter::QWindowsMimeConverter()`

**作用与语义：**

构建一个QWindowsMimeConverter实例。
该实例会自动注册，并在剪贴板或拖放操作中被调用以转换数据。
创建`QGuiApplication`后再调用这个构造器。

### `[virtual noexcept] QWindowsMimeConverter::~QWindowsMimeConverter()`

**作用与语义：**

构建一个`QWindowsMimeConverter`实例。
该实例会自动取消注册。

### `[pure virtual] bool QWindowsMimeConverter::canConvertFromMime(const FORMATETC &formatetc, const QMimeData *mimeData) const`

**作用与语义：**

如果转换器能从`mimeData`转换为 `formatetc` 指定的格式，返回`true`。
所有子类都必须重新实现这个纯虚拟函数。

### `[pure virtual] bool QWindowsMimeConverter::canConvertToMime(const QString &mimeType, IDataObject *pDataObj) const`

**作用与语义：**

退货`true`转换器能否从现有格式转换为`pDataObj` `mimeType`。
所有子类都必须重新实现这个纯虚拟函数。

### `[pure virtual] bool QWindowsMimeConverter::convertFromMime(const FORMATETC &formatetc, const QMimeData *mimeData, STGMEDIUM *pmedium) const`

**作用与语义：**

将`mimeData`转换为`formatetc`指定格式。转换后的数据应被放入`pmedium`结构中。
如果转换成功，则返回true。
所有子类都必须重新实现这个纯虚拟函数。

### `[pure virtual] QVariant QWindowsMimeConverter::convertToMime(const QString &mimeType, IDataObject *pDataObj, QMetaType preferredType) const`

**作用与语义：**

返回包含`pDataObj`转换后数据的`QVariant`，`mimeType`。如果可能，`QVariant`应`preferredType`以避免不必要的转换。
所有子类都必须重新实现这个纯虚拟函数。

### `[pure virtual] QList<FORMATETC> QWindowsMimeConverter::formatsForMime(const QString &mimeType, const QMimeData *mimeData) const`

**作用与语义：**

返回`QList` FORMATETC 结构，代表`mimeData`中可为`mimeType`提供的不同 Windows 剪贴板格式。
所有子类都必须重新实现这个纯虚拟函数。

### `[pure virtual] QString QWindowsMimeConverter::mimeForFormat(const FORMATETC &formatetc) const`

**作用与语义：**

返回将根据 `formatetc` 中指定格式创建的 mime 类型，或者如果该转换器不支持 `formatetc`，则返回空字符串。
所有子类都必须重新实现这个纯虚拟函数。

### `[static] int QWindowsMimeConverter::registerMimeType(const QString &mimeType)`

**作用与语义：**

注册MIME类型`mimeType`，并返回识别Windows格式的ID编号。
哑剧类型的`application/x-qt-windows-mime;value="WindowsType"`将被注册为`WindowsType`的剪贴板格式。

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

`QWindowsMimeConverter` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
