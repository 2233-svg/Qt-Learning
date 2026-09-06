# QReadWriteLock

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“ReadWriteLock”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QReadWriteLock` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QReadWriteLock>`
- 继承自：QBasicReadWriteLock
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

- `enum RecursionMode { Recursive, NonRecursive }`

### 公有函数

- `QReadWriteLock(QReadWriteLock::RecursionMode recursionMode = NonRecursive)`
- `~QReadWriteLock()`
- `void lockForRead()`
- `void lockForWrite()`
- `bool tryLockForRead(int timeout)`
- `(since 6.6) bool tryLockForRead(QDeadlineTimer timeout = {})`
- `bool tryLockForWrite(int timeout)`
- `(since 6.6) bool tryLockForWrite(QDeadlineTimer timeout = {})`
- `void unlock()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QReadWriteLock::RecursionMode`

**作用与语义：**

- `QReadWriteLock::Recursive`：`1`;在此模式下，线程可以多次锁定同一个`QReadWriteLock`。`QReadWriteLock`在对应的`unlock()`调用完成后才会解锁。
- `QReadWriteLock::NonRecursive`：`0`;在此模式下，线程只能锁定`QReadWriteLock`一次。

### `[explicit] QReadWriteLock::QReadWriteLock(QReadWriteLock::RecursionMode recursionMode = NonRecursive)`

**作用与语义：**

在给定`recursionMode`中构造一个QReadWriteLock对象。
默认递归模式是`NonRecursive`。

### `[noexcept] QReadWriteLock::~QReadWriteLock()`

**作用与语义：**

摧毁`QReadWriteLock`物体。
警告：销毁正在使用的读写锁可能导致未定义的行为。

### `void QReadWriteLock::lockForRead()`

**作用与语义：**

锁定读取锁。如果有其他线程锁定写入，该函数会阻塞当前线程。
如果线程已经锁定写入，就无法锁定读取。

### `void QReadWriteLock::lockForWrite()`

**作用与语义：**

锁定写入锁。如果有其他线程（包括当前线程）已锁定读写，该函数会阻塞当前线程（除非锁是用`QReadWriteLock::Recursive`模式创建的）。
如果线程已经锁定读，则无法锁定写入。

### `bool QReadWriteLock::tryLockForRead(int timeout)`

**作用与语义：**

尝试锁定读取。如果锁定已获得，该函数返回`true`;否则返回`false`。如果其他线程已锁定写入，该函数最多等待`timeout`毫秒，直到锁定可用。
注意：将负数传递为`timeout`等同于调用`lockForRead()`，即该函数会一直等待，直到锁定锁定读取，而当`timeout`为负时。
如果锁被获得，必须先用`unlock()`解锁锁，其他线程才能成功锁定写入锁。
如果线程已经锁定写入，就无法锁定读取。

### `[since 6.6] bool QReadWriteLock::tryLockForRead(QDeadlineTimer timeout = {})`

**作用与语义：**

尝试锁定读取。如果锁定已获得，该函数返回`true`;否则返回`false`。如果其他线程已锁定写入，该函数将等待`timeout`过期后锁才可用。
如果锁定已被获取，必须先用`unlock()`解锁锁，其他线程才能成功锁定写入。
如果线程已经锁定写入，就无法锁定读取。

### `bool QReadWriteLock::tryLockForWrite(int timeout)`

**作用与语义：**

尝试锁定写入。如果锁定成功，该函数返回`true`;否则返回`false`。如果其他线程已锁定读写，该函数最多等待`timeout`毫秒，锁定可用。
注意：将负数传递为`timeout`等同于调用`lockForWrite()`，即该函数会无限等待，直到锁能够锁定写入，而当`timeout`为负时。
如果锁被获得，必须先用`unlock()`解锁锁，其他线才能成功锁定。
如果线程已经锁定读，则无法锁定写入。

### `[since 6.6] bool QReadWriteLock::tryLockForWrite(QDeadlineTimer timeout = {})`

**作用与语义：**

尝试锁定写入。如果锁定已获得，该函数返回`true`;否则返回`false`。如果其他线程已锁定读写，该函数会等待`timeout`到期后锁可用。
如果锁定成功，必须先用`unlock()`解锁锁，其他线程才能成功锁定。
如果线程已经锁定读，则无法锁定写入。

### `void QReadWriteLock::unlock()`

**作用与语义：**

解锁锁。
尝试解锁未锁定的锁是错误，会导致程序终止。

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

`QReadWriteLock` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
