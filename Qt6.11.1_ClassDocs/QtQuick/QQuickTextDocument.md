# QQuickTextDocument

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickTextDocument` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickTextDocument` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickTextDocument>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
target_link_libraries(mytarget PRIVATE Qt6::Quick)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

### 状态、生命周期和线程

**生命周期：** QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

**状态与结果：** 属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

**线程与事件循环：** 大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

## 3. 直接使用

需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。 使用时通常按这个过程组织：注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

```cpp
// C++ 侧暴露属性/信号后，在 QML 中建立绑定。
// 变化时发出 notify signal，避免在绑定表达式中直接修改状态。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `(preliminary) errorString : QString`
- `(preliminary) modified : bool`
- `(preliminary) source : QUrl`
- `(preliminary) status : Status`

### 公有函数

- `QQuickTextDocument(QQuickItem *parent)`
- `QString errorString() const`
- `bool isModified() const`
- `(preliminary) void save()`
- `(preliminary) void saveAs(const QUrl &url)`
- `void setModified(bool modified)`
- `void setSource(const QUrl &url)`
- `(since 6.7) void setTextDocument(QTextDocument *document)`
- `QUrl source() const`
- `QQuickTextDocument::Status status() const`
- `QTextDocument * textDocument() const`

### 信号

- `(preliminary) void errorStringChanged()`
- `(preliminary) void modifiedChanged()`
- `(preliminary) void sourceChanged()`
- `(preliminary) void statusChanged()`
- `(since 6.7) void textDocumentChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[read-only, preliminary] errorString : QString`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性包含一个人类可读字符串，描述加载或保存过程中发生的错误（如果有的话）。
默认情况下，该字符串为空。

**如何使用：** 调用 `errorString()` 读取当前值；它不会修改应用状态。

### `[preliminary] modified : bool`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性决定文档是否被用户修改。
该属性是否被用户修改过，自上次加载或保存以来。默认情况下，该属性为`false`。
和`QTextDocument::modified`一样，你可以设置修改属性：例如，将其设置为`false`，以便将`source`属性设置为不同的URL（从而丢弃用户的更改）。

**如何使用：** 调用 `modified()` 读取当前值；它不会修改应用状态。

### `[preliminary] source : QUrl`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性包含加载文档内容的 URL。
`QQuickTextDocument`可以处理Qt支持的任何文本格式，这些格式可从Qt支持的任何URL方案加载。
在文档`modified`状态`true`时，`source`属性不可更改。如果用户修改了文档内容，应提示用户是否`save()`，否则在将`source`属性设置为其他URL前，先将`modified`设为`false`来丢弃更改。

**如何使用：** 调用 `source()` 读取当前值；它不会修改应用状态。

### `[read-only, preliminary] status : Status`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性具有文件加载或保存状态。
该属性具有文件加载或保存状态。它可以是以下之一：
- `Null`：未加载任何文件
- `Loading`：`source`开始朗读
- `Loaded`：阅读成功结束
- `Saving`：文件写入在`save()`或`saveAs()`之后开始
- `Saved`：写作成功完成
- `ReadError`：读取`source`时发生错误
- `WriteError`：`save()`或`saveAs()`发生错误
- `NonLocalFileError`：`saveAs()` 被调用时，URL指向远程资源，而非本地文件

**如何使用：** 调用 `status()` 读取当前值；它不会修改应用状态。

### `QQuickTextDocument::QQuickTextDocument(QQuickItem *parent)`

**作用与语义：**

构造一个以 `parent` 为父对象的 QQuickTextDocument 对象。

### `[signal, preliminary] void QQuickTextDocument::errorStringChanged()`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性包含一个人类可读字符串，描述加载或保存过程中发生的错误（如果有的话）。
默认情况下，该字符串为空。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `errorString` 的变化，不要把它当作普通函数主动调用。

### `[signal, preliminary] void QQuickTextDocument::modifiedChanged()`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性决定文档是否被用户修改。
该属性是否被用户修改过，自上次加载或保存以来。默认情况下，该属性为`false`。
和`QTextDocument::modified`一样，你可以设置修改属性：例如，将其设置为`false`，以便将`source`属性设置为不同的URL（从而丢弃用户的更改）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `modified` 的变化，不要把它当作普通函数主动调用。

### `[invokable, preliminary] void QQuickTextDocument::save()`

**作用与语义：**

该功能正在开发中，可能会有所调整。
将内容保存到`source`指定的相同文件和格式中。
注意：你只能保存到挂载文件系统上的文件。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable, preliminary] void QQuickTextDocument::saveAs(const QUrl &url)`

**作用与语义：**

该功能正在开发中，可能会有所调整。
将内容保存到`url`指定的文件和格式中。
`url` 中的文件扩展名指定文件格式（由 `QMimeDatabase::mimeTypeForUrl()` 确定）。
注意：你只能保存到挂载文件系统上的文件。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[since 6.7] void QQuickTextDocument::setTextDocument(QTextDocument *document)`

**作用与语义：**

设定给定的`document`。
调用者保留文档的所有权。

### `[signal, preliminary] void QQuickTextDocument::sourceChanged()`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性包含加载文档内容的 URL。
`QQuickTextDocument`可以处理Qt支持的任何文本格式，这些格式可从Qt支持的任何URL方案加载。
在文档`modified`状态`true`时，`source`属性不可更改。如果用户修改了文档内容，应提示用户是否`save()`，否则在将`source`属性设置为其他URL前，先将`modified`设为`false`来丢弃更改。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `source` 的变化，不要把它当作普通函数主动调用。

### `[signal, preliminary] void QQuickTextDocument::statusChanged()`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性具有文件加载或保存状态。
该属性具有文件加载或保存状态。它可以是以下之一：
- `Null`：未加载任何文件
- `Loading`：`source`开始朗读
- `Loaded`：阅读成功结束
- `Saving`：文件写入在`save()`或`saveAs()`之后开始
- `Saved`：写作成功完成
- `ReadError`：读取`source`时发生错误
- `WriteError`：`save()`或`saveAs()`发生错误
- `NonLocalFileError`：`saveAs()` 被调用时，URL指向远程资源，而非本地文件

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `status` 的变化，不要把它当作普通函数主动调用。

### `QTextDocument *QQuickTextDocument::textDocument() const`

**作用与语义：**

返回指向`QTextDocument`对象的指针。

### `[signal, since 6.7] void QQuickTextDocument::textDocumentChanged()`

**作用与语义：**

当底层`QTextDocument`被替换为其他实例时，该信号会发出。

### `(preliminary) errorString : QString`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性包含一个人类可读字符串，描述加载或保存过程中发生的错误（如果有的话）。
默认情况下，该字符串为空。

**如何使用：** 调用 `errorString()` 读取当前值；它不会修改应用状态。

### `(preliminary) modified : bool`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性决定文档是否被用户修改。
该属性是否被用户修改过，自上次加载或保存以来。默认情况下，该属性为`false`。
和`QTextDocument::modified`一样，你可以设置修改属性：例如，将其设置为`false`，以便将`source`属性设置为不同的URL（从而丢弃用户的更改）。

**如何使用：** 调用 `modified()` 读取当前值；它不会修改应用状态。

### `(preliminary) source : QUrl`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性包含加载文档内容的 URL。
`QQuickTextDocument`可以处理Qt支持的任何文本格式，这些格式可从Qt支持的任何URL方案加载。
在文档`modified`状态`true`时，`source`属性不可更改。如果用户修改了文档内容，应提示用户是否`save()`，否则在将`source`属性设置为其他URL前，先将`modified`设为`false`来丢弃更改。

**如何使用：** 调用 `source()` 读取当前值；它不会修改应用状态。

### `(preliminary) status : Status`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性具有文件加载或保存状态。
该属性具有文件加载或保存状态。它可以是以下之一：
- `Null`：未加载任何文件
- `Loading`：`source`开始朗读
- `Loaded`：阅读成功结束
- `Saving`：文件写入在`save()`或`saveAs()`之后开始
- `Saved`：写作成功完成
- `ReadError`：读取`source`时发生错误
- `WriteError`：`save()`或`saveAs()`发生错误
- `NonLocalFileError`：`saveAs()` 被调用时，URL指向远程资源，而非本地文件

**如何使用：** 调用 `status()` 读取当前值；它不会修改应用状态。

### `QString errorString() const`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性包含一个人类可读字符串，描述加载或保存过程中发生的错误（如果有的话）。
默认情况下，该字符串为空。

**如何使用：** 调用 `errorString()` 读取当前值；它不会修改应用状态。

### `bool isModified() const`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性决定文档是否被用户修改。
该属性是否被用户修改过，自上次加载或保存以来。默认情况下，该属性为`false`。
和`QTextDocument::modified`一样，你可以设置修改属性：例如，将其设置为`false`，以便将`source`属性设置为不同的URL（从而丢弃用户的更改）。

**如何使用：** 调用 `isModified()` 读取当前值；它不会修改应用状态。

### `void setModified(bool modified)`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性决定文档是否被用户修改。
该属性是否被用户修改过，自上次加载或保存以来。默认情况下，该属性为`false`。
和`QTextDocument::modified`一样，你可以设置修改属性：例如，将其设置为`false`，以便将`source`属性设置为不同的URL（从而丢弃用户的更改）。

**如何使用：** 调用 `setModified(...)` 修改 `modified`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSource(const QUrl &url)`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性包含加载文档内容的 URL。
`QQuickTextDocument`可以处理Qt支持的任何文本格式，这些格式可从Qt支持的任何URL方案加载。
在文档`modified`状态`true`时，`source`属性不可更改。如果用户修改了文档内容，应提示用户是否`save()`，否则在将`source`属性设置为其他URL前，先将`modified`设为`false`来丢弃更改。

**如何使用：** 调用 `setSource(...)` 修改 `source`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QUrl source() const`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性包含加载文档内容的 URL。
`QQuickTextDocument`可以处理Qt支持的任何文本格式，这些格式可从Qt支持的任何URL方案加载。
在文档`modified`状态`true`时，`source`属性不可更改。如果用户修改了文档内容，应提示用户是否`save()`，否则在将`source`属性设置为其他URL前，先将`modified`设为`false`来丢弃更改。

**如何使用：** 调用 `source()` 读取当前值；它不会修改应用状态。

### `QQuickTextDocument::Status status() const`

**作用与语义：**

该物业正在开发中，可能会有所变更。
该属性具有文件加载或保存状态。
该属性具有文件加载或保存状态。它可以是以下之一：
- `Null`：未加载任何文件
- `Loading`：`source`开始朗读
- `Loaded`：阅读成功结束
- `Saving`：文件写入在`save()`或`saveAs()`之后开始
- `Saved`：写作成功完成
- `ReadError`：读取`source`时发生错误
- `WriteError`：`save()`或`saveAs()`发生错误
- `NonLocalFileError`：`saveAs()` 被调用时，URL指向远程资源，而非本地文件

**如何使用：** 调用 `status()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

### 状态和错误边界

属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

### 线程边界

大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

### 最容易出现的错误

不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QQuickTextDocument` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
