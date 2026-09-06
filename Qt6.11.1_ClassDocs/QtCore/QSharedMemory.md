# QSharedMemory

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QSharedMemory` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSharedMemory` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QSharedMemory>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum AccessMode { ReadOnly, ReadWrite }`
- `enum SharedMemoryError { NoError, PermissionDenied, InvalidSize, KeyError, AlreadyExists, …, UnknownError }`

### 公有函数

- `QSharedMemory(const QString &key, QObject *parent = nullptr)`
- `QSharedMemory(QObject *parent = nullptr)`
- `QSharedMemory(const QNativeIpcKey &key, QObject *parent = nullptr)`
- `virtual ~QSharedMemory()`
- `bool attach(QSharedMemory::AccessMode mode = ReadWrite)`
- `const void * constData() const`
- `bool create(qsizetype size, QSharedMemory::AccessMode mode = ReadWrite)`
- `void * data()`
- `const void * data() const`
- `bool detach()`
- `QSharedMemory::SharedMemoryError error() const`
- `QString errorString() const`
- `bool isAttached() const`
- `QString key() const`
- `bool lock()`
- `(since 6.6) QNativeIpcKey nativeIpcKey() const`
- `QString nativeKey() const`
- `void setKey(const QString &key)`
- `(since 6.6) void setNativeKey(const QNativeIpcKey &key)`
- `void setNativeKey(const QString &key, QNativeIpcKey::Type type = QNativeIpcKey::legacyDefaultTypeForOs())`
- `qsizetype size() const`
- `bool unlock()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QSharedMemory::QSharedMemory(const QString &key, QObject *parent = nullptr)`

**作用与语义：**

构造一个共享内存对象，使用给定的`parent`，遗留键设置为`key`。由于其键被设置，可以调用其`create()`和`attach()`函数。

### `QSharedMemory::QSharedMemory(QObject *parent = nullptr)`

**作用与语义：**

构造一个共享内存对象，并使用给定的`parent`。共享内存对象的密钥不由构造函数设置，因此共享内存对象没有附加底层的共享内存段。密钥必须先用`setNativeKey()`设置，才能使用 `create()` 或 `attach()`。
注意：该功能会超载`QSharedMemory::QSharedMemory()`。

### `QSharedMemory::QSharedMemory(const QNativeIpcKey &key, QObject *parent = nullptr)`

**作用与语义：**

构造一个共享内存对象，其密钥设置为`key` `parent`。由于密钥被设置，可以调用其`create()`和`attach()`函数。

### `[virtual noexcept] QSharedMemory::~QSharedMemory()`

**作用与语义：**

析构函数清除 key，这会强制共享内存对象从其底层共享内存段 `detach`。如果此共享内存对象是连接到该共享内存段的最后一个对象，`detach()` 操作将销毁该共享内存段。

### `bool QSharedMemory::attach(QSharedMemory::AccessMode mode = ReadWrite)`

**作用与语义：**

尝试将进程附加到由传递给构造器或调用`setNativeKey()`的密钥所识别的共享内存段。访问`mode`默认为`ReadWrite`。也可以是`ReadOnly`。如果连接操作成功，返回`true`。如果返回false，调用`error()`以确定发生了哪个错误。附加共享内存段后，可以通过调用`data()`获得共享内存的指针。

### `const void *QSharedMemory::constData() const`

**作用与语义：**

如果连接了共享内存段的内容，返回一个const指针。否则返回空值。该函数返回的值直到`detach`发生时才会变化，因此存储该指针是安全的。
如果内存操作不是原子操作，你可以在读取或写入前用`lock()`锁定共享内存，但记得完成后要用`unlock()`解除锁。

### `bool QSharedMemory::create(qsizetype size, QSharedMemory::AccessMode mode = ReadWrite)`

**作用与语义：**

创建一个`size`字节的共享内存段，密钥传递给构造函数或`setNativeKey()`集合，然后用给定的访问`mode`附加到新的共享内存段并返回`true`。如果密钥识别的共享内存段已存在，则不执行附加操作，返回`false`。当返回值`false`时，调用`error()`以确定发生了哪个错误。

### `void *QSharedMemory::data()`

**作用与语义：**

如果连接共享内存段的内容，返回指向该内存段内容的指针。否则返回空值。该函数返回的值直到`detach`发生时才会变化，因此存储该指针是安全的。
如果内存操作不是原子操作，你可以在读取或写入前用`lock()`锁定共享内存，但完成后记得随`unlock()`解除锁。

### `const void *QSharedMemory::data() const`

**作用与语义：**

注意：该功能会超载`QSharedMemory::data()`。

### `bool QSharedMemory::detach()`

**作用与语义：**

将进程从共享内存段中分离。如果这是连接到共享内存段的最后一个进程，那么系统会释放该共享内存段，即内容被销毁。如果该函数分离了共享内存段，返回`true`。如果返回`false`，通常意味着该段没有被连接，或者被其他进程锁定。

### `QSharedMemory::SharedMemoryError QSharedMemory::error() const`

**作用与语义：**

返回一个值，表示是否发生了错误，如果发生了，以及是哪一个错误。

### `QString QSharedMemory::errorString() const`

**作用与语义：**

返回最后一次错误的文本描述。如果`error()`返回错误值，调用该函数获取描述错误的文本字符串。

### `bool QSharedMemory::isAttached() const`

**作用与语义：**

如果该进程连接到共享内存段，返回`true`。

### `QString QSharedMemory::key() const`

**作用与语义：**

返回与`setKey()`分配到该共享内存的遗留密钥，若未分配密钥或段中使用`nativeKey()`则返回空密钥。密钥是Qt应用程序用来标识共享内存段的标识符。
你可以通过调用`nativeKey()`找到操作系统使用的原生、平台特定的密钥。

### `bool QSharedMemory::lock()`

**作用与语义：**

这是一个信号量，用于锁定共享内存段，供该进程访问并返回`true`。如果其他进程锁定了该段，该函数会阻塞直到锁被释放。然后它获取该锁并返回`true`。如果该函数返回`false`，说明你忽略了`create()`或`attach()`的错误返回，或者你设置了密钥为`setNativeKey()`，或者由于未知系统错误`QSystemSemaphore::acquire()`失败。

### `[since 6.6] QNativeIpcKey QSharedMemory::nativeIpcKey() const`

**作用与语义：**

返回该共享内存对象的键类型。该键类型作为操作系统识别共享内存段的标识符，补充了`nativeKey()`。
您可以使用原生密钥访问未由 Qt 创建的共享内存段，或授予非 Qt 应用程序共享内存访问。更多信息请参见本地 IPC 密钥。

### `QString QSharedMemory::nativeKey() const`

**作用与语义：**

返回该共享内存对象的本地、平台特定密钥。本地密钥是操作系统用来识别共享内存段的标识符。
您可以使用原生密钥访问未由 Qt 创建的共享内存段，或授予非 Qt 应用程序共享内存访问。更多信息请参见本地 IPC 密钥。

### `void QSharedMemory::setKey(const QString &key)`

**作用与语义：**

为该共享内存对象设置遗留`key`。如果`key`与当前键相同，函数会返回而不做任何操作。否则，如果共享内存对象附加在底层共享内存段，它会在设置新键之前从该段`detach`。该函数不执行`attach()`。
你可以调用`key()`来获取遗留密钥。这个函数基本与以下相同：
但它允许通过`key()`获取遗留密钥。

**官方示例：**

```cpp
 shm.setNativeKey(QSharedMemory::legacyNativeKey(key));
```

### `[since 6.6] void QSharedMemory::setNativeKey(const QNativeIpcKey &key)`

**作用与语义：**

为该共享内存对象设置本地、平台特定的`key`。如果`key`与当前本地键相同，函数会返回而不做任何操作。否则，如果共享内存对象连接到底层共享内存段，它会在设置新密钥前从该段中取`detach`。该函数不执行`attach()`。
如果本地密钥是从其他进程共享的，这个功能非常有用。更多信息请参见本地IPC密钥。
可移植的原生密钥可以通过 platformSafeKey() 获得。
你可以调用`nativeKey()`来获取本地密钥。

### `void QSharedMemory::setNativeKey(const QString &key, QNativeIpcKey::Type type = QNativeIpcKey::legacyDefaultTypeForOs())`

**作用与语义：**

为该类型`type`共享内存对象设置本地、平台特定的`key`（类型参数自Qt 6.6起可用）。如果`key`与当前本地键相同，函数返回时不做任何操作。否则，如果共享内存对象附加在底层共享内存段，则会在设置新键前从该段`detach`。该函数不做`attach()`。
如果本地密钥是从另一个进程共享的，这个功能很有用，但应用程序必须确保密钥类型与另一个进程的预期一致。更多信息请参见本地IPC密钥。
可移植的原生密钥可以通过 platformSafeKey() 获得。
你可以调用`nativeKey()`获取本地密钥。

### `qsizetype QSharedMemory::size() const`

**作用与语义：**

返回所连接共享内存段的大小。如果没有连接共享内存段，则返回0。
注意：段的大小可能大于传递给`create()`的请求大小。

### `bool QSharedMemory::unlock()`

**作用与语义：**

如果该进程当前持有该锁，则释放共享内存段的锁并返回`true`。如果该段未被锁定，或者锁被其他进程持有，则不会发生任何事，返回 false。

### `enum AccessMode { ReadOnly, ReadWrite }`

**作用与语义：**

- `QSharedMemory::ReadOnly`：`0`;共享内存段为只读。不允许写入共享内存段。尝试写入用ReadOnly创建的共享内存段会导致程序中止。
- `QSharedMemory::ReadWrite`：`1`;共享内存段的读写均被允许。

### `enum SharedMemoryError { NoError, PermissionDenied, InvalidSize, KeyError, AlreadyExists, …, UnknownError }`

**作用与语义：**

- `QSharedMemory::NoError`：`0`;没有发生错误。
- `QSharedMemory::PermissionDenied`：`1`;操作失败，因为调用者没有所需的权限。
- `QSharedMemory::InvalidSize`：`2`;创建操作失败，因为请求的大小无效。
- `QSharedMemory::KeyError`：`3`;由于密钥无效，操作失败。
- `QSharedMemory::AlreadyExists`：`4`;`create()`操作失败，因为已有具有指定密钥的共享内存段存在。
- `QSharedMemory::NotFound`：`5`;`attach()`失败是因为找不到带有指定密钥的共享内存段。
- `QSharedMemory::LockError`：`6`;尝试`lock()`共享内存段失败，因为`create()`或`attach()`失败并返回为假，或因系统错误发生`QSystemSemaphore::acquire()`。
- `QSharedMemory::OutOfResources`：`7`;`create()`操作失败，因为内存不足以填充请求。
- `QSharedMemory::UnknownError`：`8`;还有别的事发生了，情况很糟。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSharedMemory` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
