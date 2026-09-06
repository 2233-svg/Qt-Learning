# QStandardPaths

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QStandardPaths` 是 文件、设备与流机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QStandardPaths` 是 文件、设备与流机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QStandardPaths>`
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

### 公有类型

- `enum LocateOption { LocateFile, LocateDirectory }`
- `flags LocateOptions`
- `enum StandardLocation { DesktopLocation, DocumentsLocation, FontsLocation, ApplicationsLocation, MusicLocation, …, GenericStateLocation }`

### 静态公有成员

- `QString displayName(QStandardPaths::StandardLocation type)`
- `QString findExecutable(const QString &executableName, const QStringList &paths = QStringList())`
- `QString locate(QStandardPaths::StandardLocation type, const QString &fileName, QStandardPaths::LocateOptions options = LocateFile)`
- `QStringList locateAll(QStandardPaths::StandardLocation type, const QString &fileName, QStandardPaths::LocateOptions options = LocateFile)`
- `void setTestModeEnabled(bool testMode)`
- `QStringList standardLocations(QStandardPaths::StandardLocation type)`
- `QString writableLocation(QStandardPaths::StandardLocation type)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 11 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QStandardPaths::LocateOptionflags QStandardPaths::LocateOptions`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QStandardPaths` 暴露的类型声明 `Locate、Optionflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:LocateOptionflags QStandardPaths::LocateOptions`。
- 属性名：`QStandardPaths`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QStandardPaths::StandardLocation`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QStandardPaths` 暴露的类型声明 `Standard、Location`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:StandardLocation`。
- 属性名：`QStandardPaths`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QStandardPaths::displayName(QStandardPaths::StandardLocation type)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `displayName`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `type`：类型为 `QStandardPaths::StandardLocation`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QStandardPaths::findExecutable(const QString &executableName, const QStringList &paths = QStringList())`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `findExecutable`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `executableName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `paths`：类型为 `const QStringList &`。默认值为 `QStringList()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QStandardPaths::locate(QStandardPaths::StandardLocation type, const QString &fileName, QStandardPaths::LocateOptions options = LocateFile)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `locate`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `type`：类型为 `QStandardPaths::StandardLocation`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `options`：类型为 `QStandardPaths::LocateOptions`。默认值为 `LocateFile`。传入 `QStandardPaths::LocateOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QStringList QStandardPaths::locateAll(QStandardPaths::StandardLocation type, const QString &fileName, QStandardPaths::LocateOptions options = LocateFile)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `locateAll`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `type`：类型为 `QStandardPaths::StandardLocation`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `options`：类型为 `QStandardPaths::LocateOptions`。默认值为 `LocateFile`。传入 `QStandardPaths::LocateOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QStandardPaths::setTestModeEnabled(bool testMode)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setTestModeEnabled`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `testMode`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QStringList QStandardPaths::standardLocations(QStandardPaths::StandardLocation type)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `standardLocations`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `type`：类型为 `QStandardPaths::StandardLocation`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QStandardPaths::writableLocation(QStandardPaths::StandardLocation type)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `writableLocation`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `type`：类型为 `QStandardPaths::StandardLocation`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum LocateOption { LocateFile, LocateDirectory }`

**API 类别：** 公有类型

**中文解读：** 这是 `QStandardPaths` 暴露的类型声明 `Locate、Option`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags LocateOptions`

**API 类别：** 公有类型

**中文解读：** 这是 `QStandardPaths` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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

`QStandardPaths` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
