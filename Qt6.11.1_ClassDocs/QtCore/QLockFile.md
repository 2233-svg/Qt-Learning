# QLockFile

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Lock文件”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QLockFile` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QLockFile>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
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

### 公有类型

- `enum LockError { NoError, LockFailedError, PermissionError, UnknownError }`

### 公有函数

- `QLockFile(const QString &fileName)`
- `~QLockFile()`
- `QLockFile::LockError error() const`
- `QString fileName() const`
- `bool getLockInfo(qint64 *pid, QString *hostname, QString *appname) const`
- `bool isLocked() const`
- `bool lock()`
- `bool removeStaleLockFile()`
- `void setStaleLockTime(int staleLockTime)`
- `(since 6.2) void setStaleLockTime(std::chrono::milliseconds staleLockTime)`
- `int staleLockTime() const`
- `(since 6.2) std::chrono::milliseconds staleLockTimeAsDuration() const`
- `bool tryLock(int timeout)`
- `(since 6.2) bool tryLock(std::chrono::milliseconds timeout = std::chrono::milliseconds::zero())`
- `void unlock()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QLockFile::LockError`

**作用与语义：**

该枚举描述了最后一次调用`lock()`或 `tryLock()` 的结果。
- `QLockFile::NoError`：`0`;锁成功获得。
- `QLockFile::LockFailedError`：`1`;锁无法被获取，因为其他进程持有该锁。
- `QLockFile::PermissionError`：`2`;由于父目录缺乏权限，锁文件无法被创建。
- `QLockFile::UnknownError`：`3`;又发生了一次错误，例如满分区导致锁文件无法写出。

### `[explicit] QLockFile::QLockFile(const QString &fileName)`

**作用与语义：**

构建一个新的锁文件对象。该对象是在解锁状态下创建的。当调用`lock()`或`tryLock()`时，如果还不存在的锁文件，将创建一个名为`fileName`的锁文件。

### `[noexcept] QLockFile::~QLockFile()`

**作用与语义：**

销毁锁文件对象。如果锁被获取，这将通过删除锁文件来释放锁。

### `QLockFile::LockError QLockFile::error() const`

**作用与语义：**

返回锁文件错误状态。
如果`tryLock()`返回`false`，可以调用该函数来找出锁定失败的原因。

### `QString QLockFile::fileName() const`

**作用与语义：**

返回锁文件的文件名。

### `bool QLockFile::getLockInfo(qint64 *pid, QString *hostname, QString *appname) const`

**作用与语义：**

获取锁文件当前所有者的信息。
如果`tryLock()`返回`false`，`error()`返回`LockFailedError`，则可以调用该函数以获取关于现有锁文件的更多信息：
- 应用程序的PID（`pid`年返回）
- 运行的 `hostname`（在网络文件系统中非常有用），
- 创建该应用的名称（`appname`中返回），
注意，如果没有该PID的应用程序运行，`tryLock()`会自动删除文件，所以只有当有带有该PID的应用程序时才会发生`LockFailedError`（但也可能无关）。
这可以用来通知用户已有锁文件，并让他们选择删除它。使用`removeStaleLockFile()`删除文件后，应用程序可以再次调用`tryLock()`。
如果信息能够成功检索，该函数返回`true`;如果锁文件不存在或不包含预期数据，则返回false。如果锁文件在`tryLock()`失败与调用该函数之间被删除，这种情况就会发生。如果发生这种情况，只需再次调用`tryLock()`。

### `bool QLockFile::isLocked() const`

**作用与语义：**

如果该锁是被该实例获得的，返回`QLockFile` `true`，否则返回`false`。

### `bool QLockFile::lock()`

**作用与语义：**

创建锁文件。
如果其他进程（或其他线程）已经创建了锁文件，该函数将阻塞，直到该进程（或线程）释放锁文件。
在同一线程中同一锁多次调用该函数而不先解锁是不允许的。当文件被递归锁定时，该函数将死锁。
如果锁被获得，则返回`true`;如果由于无法恢复的错误（如父目录无权限），则返回 false。

### `bool QLockFile::removeStaleLockFile()`

**作用与语义：**

试图强制移除已有的锁文件。
在保护短命操作时不建议调用此方法：`QLockFile` 已经负责移除超过`staleLockTime()`的锁文件。
该方法仅在保护资源较长时间时调用，即 `staleLockTime`（0） 且在`tryLock()`返回 `LockFailedError` 且用户同意移除锁文件后。
成功时返回`true`，如果无法移除锁文件则返回 false。这种情况发生在 Windows 上，当拥有该锁的应用程序仍在运行时。

### `void QLockFile::setStaleLockTime(int staleLockTime)`

**作用与语义：**

将`staleLockTime`设置为锁文件过时被视为过时的时间（毫秒）。默认值为30000，即30秒。如果你的应用程序通常将文件锁定超过30秒（例如保存2兆字节数据时），你应使用setStaleLockTime()设置更大的值。
`staleLockTime`的值被`lock()`和`tryLock()`用来判断现有锁文件是否被视为过期，即是进程崩溃后遗留的。这对于PID被重复使用的情况非常有用，因此检测过时锁文件的一种方法是它存在了很长时间。
这是一个重载函数，等价于调用：

**官方示例：**

```cpp
 setStaleLockTime(std::chrono::milliseconds{staleLockTime});
```

### `[since 6.2] void QLockFile::setStaleLockTime(std::chrono::milliseconds staleLockTime)`

**作用与语义：**

设定锁文件在该时间点后被视为`staleLockTime`过时。默认值为30秒。
如果你的应用程序通常会将文件锁定超过30秒（例如保存数兆字节数据2分钟），你应该用 setStaleLockTime() 设置更大的值。
`staleLockTime()`的值被`lock()`和`tryLock()`用来判断现有锁文件是否被视为过期，即是进程崩溃后遗留的。这对于PID被重复使用的情况非常有用，因此检测过时锁文件的一种方法是它存在了很长时间。

### `int QLockFile::staleLockTime() const`

**作用与语义：**

返回锁文件过时被视为过时的时间（毫秒）。

### `[since 6.2] std::chrono::milliseconds QLockFile::staleLockTimeAsDuration() const`

**作用与语义：**

返回一个 std：：chrono：：毫秒对象，表示锁文件在多久后被视为过时。

### `bool QLockFile::tryLock(int timeout)`

**作用与语义：**

尝试创建锁文件。如果获得锁，该函数返回`true`;否则返回`false`。如果其他进程（或线程）已经创建了锁文件，该函数最多会等待`timeout`毫秒，等待锁文件的可用时间。
注意：将负数传递为`timeout`等同于调用`lock()`，即该函数会无限等待，直到锁文件能够被锁定，且`timeout`为负。
如果锁定已被获得，必须随`unlock()`释放锁，其他进程（或线程）才能成功锁定。
在同一线程中多次调用同一锁且未先解锁该函数是不允许的，该函数在递归锁定文件时总是返回 false。

### `[since 6.2] bool QLockFile::tryLock(std::chrono::milliseconds timeout = std::chrono::milliseconds::zero())`

**作用与语义：**

尝试创建锁文件。如果获得锁，该函数返回`true`;否则返回`false`。如果其他进程（或线程）已经创建了锁文件，该函数最多等待`timeout`才能获得锁文件。
如果锁定已被获得，必须在其他进程（或线程）成功锁定之前，释放`unlock()`锁。
在同一线程中多次调用同一锁且未先解锁该函数是不允许的，该函数在递归锁定文件时总是返回 false。

### `void QLockFile::unlock()`

**作用与语义：**

通过删除锁文件释放锁。
在没有先锁定文件的情况下调用 unlock() 是没有任何作用的。

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

`QLockFile` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
