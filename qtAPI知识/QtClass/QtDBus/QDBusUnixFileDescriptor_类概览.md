# Qt QDBusUnixFileDescriptor 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusUnixFileDescriptor>`  
> 所属模块：`Qt6::DBus`  
> 类型特征：隐式共享的值类型，不继承 `QObject`

## 1. 它解决什么问题

普通的 `int` 文件描述符只在当前进程中有意义。若一个 Unix 程序要通过 D-Bus 把已打开的文件、socket、管道或共享内存句柄交给另一个进程，不能把这个整数直接作为普通 `int` 发送；D-Bus 必须知道它是专门的文件描述符类型 `h`，并在底层完成描述符传递。

`QDBusUnixFileDescriptor` 就是 Qt 对 D-Bus `h` 类型的包装。它让 `QDBusConnection` 能把一个 Unix file descriptor 放进方法参数、返回值或已导出的信号中。

它最重要的设计不是“保存一个整数”，而是**隔离所有权**：

1. 传给构造函数或 `setFileDescriptor()` 的原始 fd 仍归调用者所有。
2. Qt 用 `dup(2)` 复制它，包装对象拥有这份副本。
3. 包装对象析构时只关闭自己的副本，调用者仍要关闭原始 fd。

因此它适合“把已经打开的资源交给 D-Bus 对端”，不适合替代 Unix 的 RAII 文件描述符封装。

```text
调用者持有 fd  ── dup(2) ──> QDBusUnixFileDescriptor 持有副本
      │                                      │
      └─ 调用者自己 close(fd)                └─ 析构时关闭副本
```

## 2. 构建与可用性

```cmake
find_package(Qt6 REQUIRED COMPONENTS DBus)
target_link_libraries(mytarget PRIVATE Qt6::DBus)
```

qmake：

```pro
QT += dbus
```

这个类型只有在 Unix 平台才真正持有 fd。`QDBusUnixFileDescriptor::isSupported()` 在非 Unix 平台返回 `false`；此时对象仍可创建，但始终无效，`fileDescriptor()` 始终为 `-1`，也不会占用操作系统资源。

平台支持还不等于**当前 D-Bus 连接**支持传递 fd。发送前还应检查：

```cpp
const auto capabilities = QDBusConnection::sessionBus().connectionCapabilities();
const bool canPassFd = capabilities.testFlag(
    QDBusConnection::UnixFileDescriptorPassing);
```

`isSupported()` 回答“操作系统是否具备 Unix fd”；`UnixFileDescriptorPassing` 回答“这条连接是否可传 fd”。两者缺一不可。

## 3. 最小可用代码

下面以一个已经打开的 Unix fd 为例。`openResource()` 代表你自己的 `open()`、`socket()` 等调用：

```cpp
#include <QDBusConnection>
#include <QDBusUnixFileDescriptor>

int fd = openResource();

QDBusUnixFileDescriptor descriptor(fd);
if (!descriptor.isValid()) {
    closeResource(fd);
    return;
}

// 这里可以把 descriptor 作为 D-Bus 方法参数或返回值使用。
// 原始 fd 仍然由当前代码负责关闭。
closeResource(fd);
```

不能写成“`descriptor.fileDescriptor()` 后自行 `close()`”。`fileDescriptor()` 得到的是包装对象拥有的副本；关闭它会让包装对象内部状态与实际 OS 资源不一致。

## 4. 什么时候使用

### 4.1 将 socket 或文件交给另一个本机服务

例如桌面会话中的服务进程需要把已经连接好的 Unix socket 交给另一个本机进程继续处理。相比重新连接或把大量数据复制到 D-Bus 消息中，传递 fd 可以让对端直接使用同一底层资源。

### 4.2 导出 D-Bus 方法、信号的参数或返回值

注册 `QObject` 到 D-Bus 后，槽函数和信号可使用 `QDBusUnixFileDescriptor`。Qt 会将它映射为 D-Bus `h`。

```cpp
class ResourceService : public QObject
{
    Q_OBJECT

public slots:
    QDBusUnixFileDescriptor openForClient();

signals:
    void resourceReady(const QDBusUnixFileDescriptor &descriptor);
};
```

### 4.3 不应该使用它的情况

- 只是想在本进程管理 fd：使用适合项目的 RAII 封装或明确的 `close()` 流程。
- 需要跨机器传递资源：fd 只对本机内核有意义，不能穿过网络变成远端可用的文件。
- 对端不支持 fd 传递：方法调用会得到错误；携带 fd 的信号或方法返回值可能被静默丢弃，不能把它当作可靠降级机制。

## 5. 所有权与生命周期：最容易写错的地方

### 5.1 构造和设置都复制 fd

```cpp
int fd = openResource();
QDBusUnixFileDescriptor wrapped(fd);

// wrapped.fileDescriptor() 通常不等于 fd，因为 Qt 内部复制了一份。
closeResource(fd); // 合法，原始 fd 仍归调用者
```

`setFileDescriptor(fd)` 规则相同：先处置对象原来拥有的副本，再复制传入的 fd；它不会替你关闭传入的原始 fd。

### 5.2 `fileDescriptor()` 不是所有权转移

```cpp
const int borrowedFd = wrapped.fileDescriptor();
useImmediately(borrowedFd);
```

这份 fd 只在 `wrapped` 存活且有效期间可借用。若要缓存得比 `wrapped` 更久，必须用 `dup()`、`dup2()` 或 `dup3()` 复制一份，并由自己的代码关闭那份副本。

### 5.3 拷贝对象的语义

本类是隐式共享值类型，平常可以按值传递、存入容器或返回。不要依据实现细节假定多个包装对象中一定是同一个整数 fd；业务代码应只依赖“每个对象都按自己的生命周期管理可用描述符”这一契约。

## 6. D-Bus 能力与失败模式

传 fd 前建议把“本平台”和“本连接”拆开处理：

```cpp
bool canSendUnixFd(const QDBusConnection &connection)
{
    return QDBusUnixFileDescriptor::isSupported()
        && connection.connectionCapabilities().testFlag(
            QDBusConnection::UnixFileDescriptorPassing);
}
```

即使本连接有能力，远端服务也可能无法接收 fd。此时：

- 把 fd 作为**方法调用参数**发送，通常会收到错误回复。
- 从 D-Bus 方法**返回 fd**，或发送携带 fd 的**信号**，消息可能直接被丢弃。

所以需要业务层的替代方案，例如让对端自行打开可访问的路径，或建立另一个双方都支持的传输通道。

## 7. 常见误区

### 7.1 误区：构造后原 fd 已经交给 Qt

不是。Qt 复制 fd，原 fd 仍由调用者关闭。遗漏关闭原 fd 会泄漏资源。

### 7.2 误区：`isSupported()` 为真就一定能发

不一定。它只检查平台；发送仍要检查 `QDBusConnection::UnixFileDescriptorPassing`，并考虑远端实现。

### 7.3 误区：拿到 `fileDescriptor()` 后自己关闭

不能。它属于 `QDBusUnixFileDescriptor`。需要长期或独立持有时，先 `dup()`。

### 7.4 误区：Windows 上可以退化为普通整数

不能。Windows 下它是无效包装，D-Bus `h` 的 Unix 语义并不会变成普通 `int`。

## 8. 逐项 API 说明

### 构造、赋值与资源交换

#### `QDBusUnixFileDescriptor()`

创建一个不包含 fd 的无效对象，等价于包装 `-1`。适合先声明、稍后用 `setFileDescriptor()` 赋值。

#### `explicit QDBusUnixFileDescriptor(int fileDescriptor)`

复制传入的有效 fd，并让新对象拥有复制品。传入 fd 不会被关闭，且 `fileDescriptor()` 返回的值通常不同于传入值。

#### `QDBusUnixFileDescriptor(const QDBusUnixFileDescriptor &other)`

复制另一个包装对象。适合按值传参或保存到容器；不需要也不应手动复制其裸 fd。

#### `~QDBusUnixFileDescriptor()`

销毁对象并释放它所拥有的 fd 副本。它不会关闭最初传给构造函数或 `setFileDescriptor()` 的原始 fd。

#### `operator=(QDBusUnixFileDescriptor &&other)`

移动赋值，将 `other` 的包装状态交给当前对象。适用于容器重排或明确的移动语义；移动后不要继续依赖 `other` 的 fd 状态。

#### `operator=(const QDBusUnixFileDescriptor &other)`

复制赋值。当前对象先放弃原先拥有的副本，再承接 `other` 的值语义；旧的 `fileDescriptor()` 借用值随之失效。

#### `swap(QDBusUnixFileDescriptor &other)`

快速交换两个包装对象的状态，不会失败。适用于实现异常安全的赋值或算法内部交换，不是日常业务必需 API。

### 状态、访问与配置

#### `int fileDescriptor() const`

返回对象当前拥有的 Unix fd；无效时为 `-1`。返回值是借用句柄，不能超过对象生命周期保存，更不能关闭。

#### `static bool isSupported()`

判断当前平台是否支持 Unix fd。它不验证 D-Bus 连接能力，也不验证远端服务能力。

#### `bool isValid() const`

判断对象是否持有非 `-1` 的有效 fd。发送前可检查它，但还应检查连接能力。

#### `void setFileDescriptor(int fileDescriptor)`

用传入 fd 的副本替换当前内容。原始 fd 不受影响，调用者仍负责关闭它；传入无效 fd 后对象会变为无效。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDBusUnixFileDescriptor()` | 创建不含 fd 的无效包装对象。 | `fileDescriptor()` 为 `-1`，可稍后调用 `setFileDescriptor()`。 |
| 构造 | `explicit QDBusUnixFileDescriptor(int fd)` | 复制 `fd` 并让对象管理副本。 | 原始 `fd` 仍归调用者，必须自行关闭。 |
| 构造 | `QDBusUnixFileDescriptor(const QDBusUnixFileDescriptor &other)` | 按值复制另一个包装对象。 | 使用值语义即可，不要手动管理对方内部 fd。 |
| 析构 | `~QDBusUnixFileDescriptor()` | 释放对象拥有的 fd 副本。 | 不会关闭最初传入的原始 fd。 |
| 移动赋值 | `operator=(QDBusUnixFileDescriptor &&other)` | 将 `other` 的状态移入当前对象。 | 移动后不要继续使用 `other` 中原有的 fd 状态。 |
| 复制赋值 | `operator=(const QDBusUnixFileDescriptor &other)` | 用另一个包装对象替换当前值。 | 当前对象原先借出的裸 fd 不应再继续使用。 |
| 交换 | `swap(QDBusUnixFileDescriptor &other)` | 快速交换两个包装对象。 | 主要用于泛型代码或异常安全实现。 |
| 查询 | `int fileDescriptor() const` | 借用当前对象持有的 Unix fd。 | 不能关闭，不能跨对象生命周期保存；长期使用要 `dup()`。 |
| 静态查询 | `static bool isSupported()` | 判断平台是否支持 Unix fd。 | 这不代表当前 D-Bus 连接或远端支持传 fd。 |
| 状态查询 | `bool isValid() const` | 判断对象是否含有有效 fd。 | 有效也不代表发送一定成功，仍应检查连接能力。 |
| 配置 | `void setFileDescriptor(int fd)` | 用 `fd` 的副本替换当前内容。 | 不接管原始 `fd`，旧的借用句柄会失效。 |

---

### 一句话总结

`QDBusUnixFileDescriptor` 解决的是 D-Bus 的 Unix fd 传递；牢记它会复制而不接管原始 fd，并同时检查平台、连接和远端三层能力。
