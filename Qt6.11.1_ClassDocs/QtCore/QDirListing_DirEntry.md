# QDirListing::DirEntry

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QDirListing::DirEntry` 是 文件、设备与流机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QDirListing::DirEntry` 是 文件、设备与流机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QDirListing>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

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

- `QString absoluteFilePath() const`
- `QString absolutePath() const`
- `QString baseName() const`
- `QDateTime birthTime(const QTimeZone &tz) const`
- `QString bundleName() const`
- `QString canonicalFilePath() const`
- `QString completeBaseName() const`
- `QString completeSuffix() const`
- `bool exists() const`
- `QFileInfo fileInfo() const`
- `QString fileName() const`
- `QString filePath() const`
- `QDateTime fileTime(QFileDevice::FileTime type, const QTimeZone &tz) const`
- `bool isDir() const`
- `bool isExecutable() const`
- `bool isFile() const`
- `bool isHidden() const`
- `bool isReadable() const`
- `bool isSymLink() const`
- `bool isWritable() const`
- `QDateTime lastModified(const QTimeZone &tz) const`
- `QDateTime lastRead(const QTimeZone &tz) const`
- `QDateTime metadataChangeTime(const QTimeZone &tz) const`
- `qint64 size() const`
- `QString suffix() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QDateTime DirEntry::lastRead(const QTimeZone &tz) const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `QString absoluteFilePath() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `QString absolutePath() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `QString baseName() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `QDateTime birthTime(const QTimeZone &tz) const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `QString bundleName() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `QString canonicalFilePath() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `QString completeBaseName() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `QString completeSuffix() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `bool exists() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `QFileInfo fileInfo() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `QString fileName() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `QString filePath() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `QDateTime fileTime(QFileDevice::FileTime type, const QTimeZone &tz) const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `bool isDir() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `bool isExecutable() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `bool isFile() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `bool isHidden() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `bool isReadable() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `bool isSymLink() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `bool isWritable() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `QDateTime lastModified(const QTimeZone &tz) const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `QDateTime metadataChangeTime(const QTimeZone &tz) const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `qint64 size() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

### `QString suffix() const`

**作用与语义：**

请参见同名`QFileInfo`方法。

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

`QDirListing::DirEntry` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
