# QTemporaryDir

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QTemporaryDir` 是 文件、设备与流机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QTemporaryDir` 是 文件、设备与流机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QTemporaryDir>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

### 状态、生命周期和线程

**生命周期：** 先设置路径或设备，再 open，成功后读写/定位/刷新，最后 close；析构通常会关闭设备，但关键写入应显式 flush/close 并检查错误。相对路径依赖当前工作目录，资源路径和用户文件路径要区分。

**状态与结果：** 区分设备未打开、打开成功、到达 EOF、暂时无数据、读写失败和写入尚未落盘。`readAll()` 方便小数据但可能占用大量内存，大文件应分块处理并检查返回值。

**线程与事件循环：** 同一个打开设备不要跨线程并发使用，除非类明确保证线程安全；后台 I/O 通过 worker 或异步设备处理，GUI 线程只接收结果。

## 3. 直接使用

构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
QFile file(path);
if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    const QByteArray data = file.readAll();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QTemporaryDir()`
- `QTemporaryDir(const QString &templatePath)`
- `(since 6.4) QTemporaryDir(QTemporaryDir &&other)`
- `~QTemporaryDir()`
- `bool autoRemove() const`
- `QString errorString() const`
- `QString filePath(const QString &fileName) const`
- `bool isValid() const`
- `QString path() const`
- `bool remove()`
- `void setAutoRemove(bool b)`
- `(since 6.4) void swap(QTemporaryDir &other)`
- `(since 6.4) QTemporaryDir & operator=(QTemporaryDir &&other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QTemporaryDir::QTemporaryDir()`

**作用与语义：**

利用`QCoreApplication::applicationName()`返回的应用程序名称作为模板构建 QTemporaryDir（否则`qt_temp`）。该目录存储在系统的临时目录 `QDir::tempPath()`。

### `[explicit] QTemporaryDir::QTemporaryDir(const QString &templatePath)`

**作用与语义：**

构建一个带有`templatePath`模板的QTemporaryDir。
如果 `templatePath` 是相对路径，路径将相对于当前工作目录。如果你愿意，可以使用系统的临时目录，可以用 `QDir::tempPath()` 来构造`templatePath`。
如果`templatePath`以 XXXXXX 结尾，则作为目录名称的动态部分，否则会被附加。与 `QTemporaryFile` 不同，模板字符串中间不支持 XXXXXX。

### `[noexcept, since 6.4] QTemporaryDir::QTemporaryDir(QTemporaryDir &&other)`

**作用与语义：**

从`other`移动构造出新的 QTemporaryDir。
注意：移出对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋值。

### `[noexcept] QTemporaryDir::~QTemporaryDir()`

**作用与语义：**

会销毁临时目录对象。如果设置了自动移除模式，它会自动删除目录及其所有内容。

### `bool QTemporaryDir::autoRemove() const`

**作用与语义：**

如果 `QTemporaryDir` 处于自动删除模式，则返回 `true`。自动删除模式将会在销毁时自动从磁盘删除目录。这使得在栈上创建你的 `QTemporaryDir` 对象、填充文件、处理文件，最后在函数返回时它会自动进行清理变得非常容易。自动删除默认是开启的。

### `QString QTemporaryDir::errorString() const`

**作用与语义：**

如果`isValid()`返回`false`，该函数返回解释临时目录创建失败的错误字符串。否则，该函数返回空字符串。

### `QString QTemporaryDir::filePath(const QString &fileName) const`

**作用与语义：**

返回临时目录中文件的路径名称。不检查文件是否真实存在于目录中。`fileName`中的冗余多重分隔符或“..”和“..”目录不会被移除（参见`QDir::cleanPath()`）。不允许使用绝对路径。
返回的路径将是相对路径或绝对路径`QTemporaryDir`取决于是用相对路径还是绝对路径构造的。

### `bool QTemporaryDir::isValid() const`

**作用与语义：**

如果成功创建了`QTemporaryDir`，则返回`true`。

### `QString QTemporaryDir::path() const`

**作用与语义：**

返回到临时目录的路径。如果无法创建`QTemporaryDir`，则为空。
返回的路径将是相对路径或绝对路径`QTemporaryDir`取决于是用相对路径还是绝对路径构造的。

### `bool QTemporaryDir::remove()`

**作用与语义：**

移除临时目录，包括其所有内容。
如果移除成功，退货`true`。

### `void QTemporaryDir::setAutoRemove(bool b)`

**作用与语义：**

如果`b`为真，`QTemporaryDir`会自动进入自动移除模式。
自动移除默认是开启的。

### `[noexcept, since 6.4] void QTemporaryDir::swap(QTemporaryDir &other)`

**作用与语义：**

将这个临时-dir与`other`交换。这个操作非常快，从不失败。

### `[noexcept, since 6.4] QTemporaryDir &QTemporaryDir::operator=(QTemporaryDir &&other)`

**作用与语义：**

Move-assign `other` 到该`QTemporaryDir`实例。
注意：移出对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋予新值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先设置路径或设备，再 open，成功后读写/定位/刷新，最后 close；析构通常会关闭设备，但关键写入应显式 flush/close 并检查错误。相对路径依赖当前工作目录，资源路径和用户文件路径要区分。

### 状态和错误边界

区分设备未打开、打开成功、到达 EOF、暂时无数据、读写失败和写入尚未落盘。`readAll()` 方便小数据但可能占用大量内存，大文件应分块处理并检查返回值。

### 线程边界

同一个打开设备不要跨线程并发使用，除非类明确保证线程安全；后台 I/O 通过 worker 或异步设备处理，GUI 线程只接收结果。

### 最容易出现的错误

不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QTemporaryDir` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
