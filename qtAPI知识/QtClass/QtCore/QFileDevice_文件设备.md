# Qt QFileDevice 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QFileDevice>`  
> 所属模块：`Qt6::Core`  
> 继承：`QIODevice -> QFileDevice`  
> 直接派生类：`QFile`、`QSaveFile`  
> 定位：为“已打开的文件设备”提供位置、大小、句柄、权限、时间和内存映射能力的基类

## 1. QFileDevice 解决什么问题

`QFileDevice` 是 Qt 对文件设备共同能力的抽象。它不负责“一个路径如何复制、重命名或删除”，而是负责一个文件设备已经建立之后的通用操作：

- 查询或清除文件错误状态；
- 读取当前文件位置、文件大小和顺序设备属性；
- 刷新写缓冲；
- 改变文件长度；
- 读取和修改权限、访问时间等元数据；
- 把文件映射到进程地址空间；
- 取得底层原生句柄。

它位于 `QIODevice` 和具体文件类之间：

```text
QIODevice
    |
QFileDevice
    +-- QFile
    +-- QSaveFile
```

因此它解决的是“`QFile` 和 `QSaveFile` 应该共享哪些已打开文件行为”的问题。普通业务代码通常不直接声明 `QFileDevice`，而是使用 `QFile` 或 `QSaveFile`；如果要实现自己的文件设备类，才会继承它。

`QFileDevice` 本身的构造函数受保护，不能直接实例化：

```cpp
// QFileDevice device; // 错误：构造函数受保护

QFile file("data.bin");
QSaveFile saveFile("settings.ini");
```

所有成员函数都是 reentrant。这里的 reentrant 不是“同一个对象可以被多个线程同时调用”：多个线程可以各自操作不同的对象，但同一个打开设备对象的并发读写仍需要调用方同步。

## 2. 它和 QIODevice、QFile 的边界

三层职责可以这样分：

| 类型 | 主要职责 |
| --- | --- |
| `QIODevice` | 统一的打开模式、读写、读取位置、缓冲、事务和等待接口 |
| `QFileDevice` | 文件设备共有的错误、原生句柄、大小、权限、时间和映射接口 |
| `QFile` | 普通文件路径、复制、重命名、删除、链接和文件打开入口 |
| `QSaveFile` | 先写临时文件，再通过 `commit()` 替换目标文件 |

例如，`QFileDevice` 提供 `resize()`，但“把哪个路径复制到哪个路径”是 `QFile` 的职责；`QFileDevice` 提供 `flush()`，但“如何避免配置文件被半写覆盖”是 `QSaveFile` 的职责。

文件内容接口仍然来自 `QIODevice`：

```cpp
QFile file("input.bin");
if (!file.open(QIODevice::ReadOnly)) {
    qWarning() << file.errorString();
    return;
}

const QByteArray data = file.readAll();
```

`QFileDevice` 增加的是文件特有的能力，不会改变 `QIODevice` 的基本规则：`open()`、`read()`、`write()` 等操作都要检查返回值，顺序设备不能假设有可靠的总大小。

## 3. 文件设备的生命周期

典型流程是：

```text
构造 QFile/QSaveFile
        |
        v
调用 open()，检查返回值
        |
        v
读写、seek、resize、flush、查询状态
        |
        v
调用 close() 或由析构函数结束设备
```

构造对象不会自动创建或打开磁盘文件。打开失败是正常的控制流，常见原因有：

- 路径不存在或父目录不存在；
- 路径指向目录或不适合当前打开模式；
- 权限不足；
- 文件被其他程序以不兼容方式占用；
- 路径是资源系统路径，却被当作原生文件路径使用；
- 当前工作目录不是程序以为的目录。

```cpp
QFile file("cache/data.bin");
if (!file.open(QIODevice::ReadWrite)) {
    qWarning() << "open failed:" << file.fileName()
               << file.error()
               << file.errorString();
    return;
}
```

从 Qt 6.10 起，Qt 默认可以让文件打开函数带有 `[[nodiscard]]` 属性，帮助发现没有检查 `open()` 返回值的代码。可以用 `QT_USE_NODISCARD_FILE_OPEN` 或 `QT_NO_USE_NODISCARD_FILE_OPEN` 显式选择，但二者不能同时定义。这个宏影响的是文件打开 API 的诊断，不改变打开失败的运行时语义。

### 3.1 关闭和析构

`close()` 会先尝试刷新写缓冲，但会忽略 `flush()` 的失败结果。因此，如果业务必须知道缓冲是否成功写出，应显式调用：

```cpp
if (!file.flush()) {
    qWarning() << "flush failed:" << file.errorString();
    return;
}

file.close();
```

只调用 `close()` 并不能让调用方区分“关闭时刷新成功”和“关闭时刷新失败”。对普通短生命周期输出，析构时关闭通常够用；对重要文件，应该在逻辑边界显式检查 `write()`、`flush()` 或 `QSaveFile::commit()`。

`flush()` 也不等于断电安全。它主要处理 Qt 或底层运行库缓冲；操作系统缓存、文件系统日志和硬件写缓存仍可能影响真正落盘的时机。需要强持久化保证时，应使用平台提供的同步策略。

## 4. 错误状态：FileError 不是异常

`QFileDevice` 用 `FileError` 保存文件操作错误，不会自动抛出 C++ 异常。失败后应立即读取：

```cpp
if (file.write(payload) != payload.size()) {
    const QFileDevice::FileError kind = file.error();
    const QString text = file.errorString();
    qWarning() << kind << text;
}
```

`errorString()` 继承自 `QIODevice`，适合日志和诊断；稳定的程序逻辑应根据返回值以及必要时的 `error()` 判断，不要解析错误字符串。

`unsetError()` 把错误状态清为 `NoError`。它只清除对象保存的错误状态，不会修复文件系统问题，也不会撤销已经发生的部分读写：

```cpp
file.unsetError();
```

错误状态是设备对象的状态，不应被当作全局错误。多个 `QFile` 对象各自维护自己的状态。

### 4.1 FileError 成员

| 枚举值 | 含义 | 常见触发场景 |
| --- | --- | --- |
| `NoError` | 没有错误 | 初始状态或显式清除后 |
| `ReadError` | 读取失败 | 底层读操作失败 |
| `WriteError` | 写入失败 | 磁盘满、设备错误或权限问题 |
| `FatalError` | 致命错误 | 设备无法继续使用 |
| `ResourceError` | 资源错误 | 系统资源或设备资源异常 |
| `OpenError` | 打开失败 | 路径、权限、模式或设备问题 |
| `AbortError` | 操作被中止 | 底层或调用方中止 |
| `TimeOutError` | 操作超时 | 设备或平台操作超时 |
| `UnspecifiedError` | 未分类错误 | 平台没有提供更具体分类 |
| `RemoveError` | 删除失败 | 主要由 `QFile` 的删除操作使用 |
| `RenameError` | 重命名失败 | 主要由 `QFile` 的移动或重命名使用 |
| `PositionError` | 定位失败 | `seek()` 或位置相关操作失败 |
| `ResizeError` | 调整大小失败 | `resize()` 失败 |
| `PermissionsError` | 权限操作失败 | 读取或设置权限失败 |
| `CopyError` | 复制失败 | 主要由 `QFile` 的复制操作使用 |

枚举值不应该被当成跨平台的完整诊断信息。同一个系统错误在不同平台上的映射可能不同；需要用户可读信息时配合 `errorString()`。

## 5. 文件位置、大小和文件尾

### 5.1 随机设备和顺序设备

`isSequential()` 区分是否可以可靠地按位置随机访问：

```cpp
if (!file.isSequential()) {
    file.seek(128);
}
```

普通磁盘文件通常是随机访问设备，`QFile` 返回 `false`。特殊文件、管道或平台设备可能是顺序设备。顺序设备没有可靠的总大小或任意位置概念，不应依赖 `size()`、`seek()` 或“先读大小再读完整内容”的模式。

### 5.2 `pos()`、`seek()` 和 `size()`

- `pos()` 返回当前读写位置；
- `seek(offset)` 尝试移动到绝对偏移；
- `size()` 返回文件当前长度；
- `resize(sz)` 改变文件长度。

```cpp
QFile file("records.bin");
if (!file.open(QIODevice::ReadWrite))
    return;

if (!file.seek(64)) {
    qWarning() << file.errorString();
    return;
}

const QByteArray header = file.read(16);
qInfo() << "position:" << file.pos()
        << "file size:" << file.size();
```

`seek()` 超过文件尾不会立即把文件扩展到目标位置。之后如果在这个位置写入，文件通常会扩大，中间的空洞内容由平台和文件系统决定，不应把它当作可靠的初始化数据。需要确定内容时，应显式写入填充字节或使用 `resize()` 后再写入。

文件可能被其他进程改变，所以 `size()` 只是查询瞬间的结果。打开后再查询一次通常比在打开前缓存大小更可靠，但仍不能替代并发协调。

### 5.3 `atEnd()` 的边界

`atEnd()` 对普通文件通常能表示当前位置是否到达文件尾，但特殊文件可能报告大小为零。Unix 的 `/proc` 等虚拟文件就是典型例子：它们可以有数据，却没有普通意义上的静态大小。

读取特殊文件时不要只依赖：

```cpp
while (!file.atEnd()) {
    // 这种模式对所有特殊文件并不可靠
}
```

更稳妥的方式是持续调用 `read()`，根据返回值区分数据、EOF 和错误，并结合设备类型：

```cpp
for (;;) {
    const QByteArray chunk = file.read(4096);
    if (!chunk.isEmpty()) {
        consume(chunk);
        continue;
    }

    if (file.atEnd())
        break;

    qWarning() << "read failed:" << file.errorString();
    break;
}
```

对于真正的顺序设备，还要配合 `readyRead()` 或底层协议决定“暂时没有数据”和“已经结束”的区别。

## 6. 缓冲、读写和完整写入

`QFileDevice` 继承了 `QIODevice` 的读写接口。`write()` 返回已经被设备接受的字节数，不应默认一次就写完整个缓冲区：

```cpp
qint64 written = 0;
while (written < payload.size()) {
    const qint64 n = file.write(payload.constData() + written,
                                 payload.size() - written);
    if (n <= 0) {
        qWarning() << file.errorString();
        return;
    }
    written += n;
}

if (!file.flush())
    qWarning() << file.errorString();
```

对普通本地文件，常见情况下 `write()` 会接受全部数据，但健壮代码仍然应该处理部分写入和负数返回。`flush()` 把设备缓冲推进到底层，不能替代 `write()` 返回值检查。

如果目标文件不能出现半写状态，不要只依赖 `flush()`：

```cpp
QSaveFile saveFile("settings.ini");
if (!saveFile.open(QIODevice::WriteOnly))
    return false;

if (saveFile.write(serialized) != serialized.size())
    return false;

return saveFile.commit();
```

`QFileDevice` 负责文件设备能力，原子替换更新是 `QSaveFile` 的职责。

## 7. 原生句柄和关闭所有权

`handle()` 返回底层原生文件句柄；设备未打开或发生错误时返回 `-1`。原生句柄是平台交互接口，不是跨平台业务 API：

```cpp
const int nativeHandle = file.handle();
if (nativeHandle == -1) {
    qWarning() << "no valid native handle";
}
```

通过 `QFile` 从 `FILE *` 或原生文件描述符打开时，可以使用 `QFileDevice::FileHandleFlags`：

- `DontCloseHandle`：QFile 关闭时不关闭外部句柄；
- `AutoCloseHandle`：QFile 接管句柄，关闭 QFile 时也关闭它。

句柄所有权必须唯一。下面的生命周期是危险的：

```text
外部代码拥有 fd
        +
QFile 也使用 AutoCloseHandle
        |
QFile 关闭后外部代码继续使用 fd
```

这会产生悬空句柄或句柄编号被系统复用的问题。选择 `AutoCloseHandle` 后，外部代码不能再关闭或继续使用该句柄；选择 `DontCloseHandle` 后，外部代码必须保证句柄至少存活到 QFile 不再使用它。

`FileHandleFlags` 只描述关闭责任，不会把不同平台的句柄类型变成统一的高层 API。与 C 标准库或操作系统 API 集成时，应把平台条件和错误处理写在集成边界内。

## 8. 文件大小和调整长度

`resize(sz)` 用于改变文件长度：

```cpp
if (!file.resize(1024 * 1024)) {
    qWarning() << "resize failed:" << file.errorString();
}
```

边界和副作用：

- 新大小小于旧大小时，末尾数据被截断，不能恢复；
- 新大小大于旧大小时，新增区域由文件设备写入零；
- 文件必须以允许调整大小的方式打开，权限和文件系统也必须允许；
- 对顺序设备或特殊文件，调整大小通常没有普通文件语义；
- 其他进程可以同时改变文件，调用前后的 `size()` 不能构成锁。

`seek()` 到文件尾之后写入和 `resize()` 的语义不同：前者可能产生文件空洞，后者明确改变文件长度。需要确定文件内容时不要用“越过文件尾再写一个字节”代替初始化整个区域。

## 9. 权限和平台差异

`permissions()` 返回 `QFileDevice::Permissions`，`setPermissions()` 尝试修改它：

```cpp
const auto oldPermissions = file.permissions();
const auto newPermissions =
    oldPermissions | QFileDevice::ReadUser;

if (!file.setPermissions(newPermissions))
    qWarning() << file.errorString();
```

权限位分为 owner、user、group 和 other：

```cpp
QFileDevice::Permissions readableByOwner =
    QFileDevice::ReadOwner;

if (file.permissions() & readableByOwner)
    qInfo() << "owner can read";
```

实际边界：

- Unix 权限位通常对应 mode bits，但仍受 ACL、挂载选项和安全策略影响；
- Windows 的权限结果是 Qt 对 Windows 属性和安全模型的映射，不等同于 Unix mode bits；
- `setPermissions()` 不负责修改完整 ACL；
- “查询到可写”不保证下一次写入一定成功，查询和操作之间可能发生竞态；
- 只读属性、沙箱和安全软件都可能让实际操作失败。

如果要创建文件并指定创建时权限，应使用具体类的 `open()` 重载，并仍然检查打开结果。已存在文件的最终权限还可能受到平台默认权限策略影响。

## 10. 文件时间

`fileTime()` 查询以下时间之一：

- `FileAccessTime`：最后访问时间；
- `FileBirthTime`：创建时间；
- `FileMetadataChangeTime`：元数据改变时间；
- `FileModificationTime`：内容修改时间。

```cpp
const QDateTime modified =
    file.fileTime(QFileDevice::FileModificationTime);

if (!modified.isValid())
    qWarning() << "modification time unavailable";
```

并不是所有平台和文件系统都能提供所有时间。无法取得时返回无效的 `QDateTime`，不能把无效时间格式化成“看起来像有效”的默认值。

`setFileTime()` 要求文件已经打开：

```cpp
if (!file.setFileTime(QDateTime::currentDateTimeUtc(),
                      QFileDevice::FileModificationTime)) {
    qWarning() << "set time failed:" << file.errorString();
}
```

设置时间还受平台权限、文件系统能力和文件打开方式影响。跨时区处理时优先明确使用 UTC 或明确的 `QTimeZone`，不要把本地时间字符串当作稳定的比较值。

## 11. 内存映射

`map(offset, size, flags)` 把文件的一段内容映射到进程地址空间，适合大文件随机访问、只读索引或需要减少显式复制的场景：

```cpp
QFile file("index.dat");
if (!file.open(QIODevice::ReadOnly))
    return;

uchar *view = file.map(0, file.size());
if (!view) {
    qWarning() << "map failed:" << file.errorString();
    return;
}

processMappedBytes(view, file.size());

if (!file.unmap(view))
    qWarning() << "unmap failed:" << file.errorString();
```

### 11.1 映射的生命周期

- 通常应先打开文件再调用 `map()`；
- 成功返回地址，失败返回 `nullptr`；
- 映射建立后可以关闭文件，映射仍可继续使用；
- `QFileDevice` 被销毁，或同一个对象打开另一个文件时，尚未解除的映射会自动解除；
- 应在不再使用时显式 `unmap()`，这样生命周期更清晰，也更容易发现错误；
- 指针只在对应映射有效期间可用，不能保存到映射解除之后。

不要把映射地址当作稳定的文件句柄或跨线程共享协议。映射涉及进程地址空间，使用者仍要保证访问范围不超过 `size`。

### 11.2 `MapPrivateOption`

默认 `map()` 权限跟随文件打开模式。`MapPrivateOption` 用于私有写时复制映射：

```cpp
uchar *privateView = file.map(
    0, file.size(), QFileDevice::MapPrivateOption);
```

对私有映射的修改只对当前进程的映射可见，不会写回磁盘，也不会让其他进程看到；解除映射后修改丢失。它适合临时解析、就地试算或需要可写视图但不想修改原文件的场景。

普通只读映射不应写入；写入映射前要确认打开模式、平台支持和映射选项。内存映射失败不能简单等同于文件为空，可能是权限、范围、地址空间或平台资源问题。

## 12. 常见使用场景

### 12.1 普通文件读取

直接使用 `QFile` 提供路径和打开入口，`QFileDevice` 提供位置、大小和错误能力：

```cpp
QFile file(path);
if (!file.open(QIODevice::ReadOnly))
    return {};

return file.readAll();
```

### 12.2 大文件索引

先用 `size()` 计算范围，再用 `seek()` 或 `map()` 访问固定区域。不要对不断增长的日志文件假设大小不会变化。

### 12.3 安全写入

用 `QSaveFile` 继承的文件设备能力写临时文件，成功后调用 `commit()`。`QFileDevice` 的 `flush()` 只能报告缓冲刷新，不能替代原子替换。

### 12.4 与原生 API 集成

从 `handle()` 或 `QFile::open()` 的句柄重载进入平台 API。进入平台边界后，要明确句柄关闭责任、线程约束和错误转换。

## 13. 常见误区

### 只检查 `open()`，不检查后续写入

打开成功不代表磁盘永远可写。磁盘空间、挂载状态、权限和外部进程都可能在之后改变。关键写入要检查字节数、`flush()` 和最终提交动作。

### 把 `close()` 当作可检查的 flush

`close()` 会尝试刷新，但忽略刷新失败。要判断刷新结果，先显式调用 `flush()`。

### 把 `atEnd()` 当成所有设备的可靠 EOF

特殊文件可能没有普通文件大小。对 `/proc` 等设备要根据实际 `read()` 结果判断，并结合 `atEnd()` 和错误状态。

### 把权限查询当成授权

权限检查和实际操作之间存在 TOCTOU 窗口。对于不可信路径，直接执行目标操作并处理失败，不要只依靠“先 permissions、再写入”完成安全判断。

### 忘记映射指针的有效期

对象销毁、同一对象重新打开文件或显式 `unmap()` 都会结束映射。不能把映射指针交给不知道生命周期的异步任务。

## 14. API 逐项说明

以下先列出 `QFileDevice` 自己声明的公开 API，再列出使用它时最常用的 `QIODevice` 继承 API。受保护的实现钩子单独放在最后。

### 14.1 类型和标志

| API | 语义与边界 |
| --- | --- |
| `enum FileError` | 文件操作错误分类；它是状态枚举，不会自动抛出异常。 |
| `enum FileTime` | 选择访问、创建、元数据变化或内容修改时间。 |
| `enum Permission` | 单个位权限，使用 `Q_DECLARE_FLAGS` 组合为 `Permissions`。 |
| `using Permissions` | `Permission` 的位标志类型，可用 `|` 组合。 |
| `enum FileHandleFlag` | 选择传入原生句柄由 QFile 自动关闭，还是由外部保持所有权。 |
| `using FileHandleFlags` | `FileHandleFlag` 的位标志类型。 |
| `enum MemoryMapFlag` | 内存映射选项，目前主要是 `MapPrivateOption`。 |
| `using MemoryMapFlags` | `MemoryMapFlag` 的位标志类型。 |

### 14.2 生命周期和错误

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `QFileDevice()` | 受保护的默认构造函数。 | 不能直接实例化，通常通过 `QFile` 或 `QSaveFile` 使用。 |
| `QFileDevice(QObject *parent)` | 受保护的带父对象构造函数。 | 只供派生类使用；文件设备对象仍要按 QObject 线程规则使用。 |
| `~QFileDevice()` | 销毁文件设备。 | 结束设备生命周期并清理未解除的映射；重要写入不要只依赖析构。 |
| `error()` | 返回当前 `FileError`。 | 失败后尽快读取；不要把错误字符串当稳定协议。 |
| `unsetError()` | 清除错误状态为 `NoError`。 | 只清状态，不修复底层问题，也不回滚部分读写。 |
| `close()` | 关闭设备。 | 会尝试 `flush()`，但忽略 flush 失败；需要检查时先显式 flush。 |
| `errorString()`（继承） | 返回面向诊断的错误描述。 | 用于日志和提示；内容和语言不适合程序解析。 |

### 14.3 文件位置、大小和句柄

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `isSequential()` | 判断是否为顺序设备。 | 顺序设备通常没有可靠的随机定位和总大小。 |
| `handle()` | 返回底层原生句柄。 | 未打开或出错时为 `-1`；跨平台使用要留在集成边界。 |
| `fileName()` | 返回设备关联的文件名或路径。 | 常由 `QFile` 实现；不保证路径存在。 |
| `pos()` | 返回当前读写位置。 | 位置是设备状态；并发读写会让它失去可预测性。 |
| `seek(qint64)` | 移到指定绝对位置。 | 失败要检查；越过文件尾不会立即扩展文件。 |
| `atEnd()` | 判断是否到达设备末尾。 | 特殊文件可能报告大小为零，不能单独依赖。 |
| `size()` | 返回文件或设备大小。 | 对顺序设备或查询失败的设备不一定有普通文件语义。 |
| `resize(qint64)` | 改变文件长度。 | 缩小会截断；扩大写入新增区域；平台和权限会影响结果。 |
| `flush()` | 刷新设备缓冲。 | 返回值必须检查；不等同于断电持久化。 |
| `map(qint64, qint64, MemoryMapFlags)` | 把文件范围映射为内存地址。 | 失败返回 `nullptr`；指针不能越过范围或跨越映射生命周期。 |
| `unmap(uchar *)` | 解除一个映射。 | 使用正确的映射地址；解除后旧指针立即失效。 |

### 14.4 权限和时间

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `permissions()` | 获取文件权限位。 | 结果是平台映射，不等于完整 ACL，也不保证后续操作成功。 |
| `setPermissions(Permissions)` | 设置文件权限位。 | 只设置需要的位；Windows、Unix、ACL 语义不同。 |
| `fileTime(FileTime)` | 获取指定文件时间。 | 无法取得时返回 invalid `QDateTime`。 |
| `setFileTime(QDateTime, FileTime)` | 设置指定文件时间。 | 文件必须已打开，并且平台和权限必须支持。 |

### 14.5 常用的 QIODevice 继承 API

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `open(OpenMode)` | 按读写模式打开设备。 | 检查返回值；模式组合要明确是否截断、追加或只读。 |
| `isOpen()` | 判断设备是否处于打开状态。 | 只是状态查询，不代表下一次 I/O 必然成功。 |
| `openMode()` | 返回当前打开模式。 | 用于确认是否可读、可写或文本模式。 |
| `read(char *, qint64)` | 读取指定字节数。 | 可能少于请求值；`-1` 通常表示错误。 |
| `read(qint64)` | 读取并返回字节数组。 | 返回空数组可能是 EOF、暂时无数据或错误，要结合状态判断。 |
| `readAll()` | 读取当前可获得的全部数据。 | 大文件会占用大量内存；不适合无界输入。 |
| `readLine()` | 读取一行。 | 二进制数据不要依赖换行；长行可能需要循环读取。 |
| `write(const char *, qint64)` | 写入字节。 | 处理部分写入和负数返回；不等同于物理落盘。 |
| `write(QByteArrayView)` | 写入字节视图。 | 视图所指数据必须在调用期间有效。 |
| `bytesAvailable()` | 查询当前可读字节数。 | 不是未来文件总大小，也不保证下一次 read 一定返回同样数量。 |
| `bytesToWrite()` | 查询尚未刷到底层的写缓冲量。 | 不是持久化确认；需要结果时调用 `flush()`。 |
| `canReadLine()` | 判断当前是否有可读完整行。 | 只适用于按行协议，不适合作为所有设备的“有数据”判断。 |
| `reset()` | 尝试回到设备起始位置。 | 顺序设备通常不支持；检查返回值。 |

### 14.6 受保护的实现钩子

| API | 用途 |
| --- | --- |
| `readData(char *, qint64)` | 派生类实现底层读取。 |
| `writeData(const char *, qint64)` | 派生类实现底层写入。 |
| `readLineData(char *, qint64)` | 派生类可为按行读取提供专门实现。 |

实现自定义 `QFileDevice` 时，还必须遵守 `QIODevice` 的打开模式、错误返回、位置更新和线程约束。普通应用不要为了“访问一个文件”自行继承，直接使用 `QFile` 或 `QSaveFile`。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `FileError` | 表示文件操作错误类别。 | 结合返回值和 `errorString()` 使用，不要解析字符串。 |
| 类型 | `FileTime` | 选择文件访问、创建、元数据变化或修改时间。 | 平台可能无法提供某种时间。 |
| 类型 | `Permissions` | 组合 owner、user、group、other 权限位。 | 不等于完整 ACL，平台映射不同。 |
| 类型 | `FileHandleFlags` | 指定原生句柄关闭责任。 | `AutoCloseHandle` 与外部所有权不能重复。 |
| 类型 | `MemoryMapFlags` | 指定内存映射选项。 | `MapPrivateOption` 的修改不会写回文件。 |
| 构造 | `QFileDevice()` / `QFileDevice(QObject *)` | 为派生类初始化文件设备。 | 受保护，不能直接创建 `QFileDevice`。 |
| 生命周期 | `~QFileDevice()` | 销毁文件设备。 | 未解除映射会随对象结束；关键写入不要只依赖析构。 |
| 错误 | `error()` | 返回当前错误枚举。 | 失败后及时读取，成功操作不要被误解为异常清除。 |
| 错误 | `unsetError()` | 清除错误状态。 | 不会修复问题或回滚 I/O。 |
| 关闭 | `close()` | 关闭设备并尝试刷新缓冲。 | 忽略 flush 失败；需确认时先调用 `flush()`。 |
| 顺序性 | `isSequential()` | 判断设备是否只能顺序访问。 | 顺序设备不要依赖 `size()` 和 `seek()`。 |
| 句柄 | `handle()` | 取得原生文件句柄。 | 未打开或出错时为 `-1`；平台相关。 |
| 名称 | `fileName()` | 返回设备保存的路径。 | 只表示对象关联名称，不保证存在。 |
| 位置 | `pos()` | 查询当前读写位置。 | 同一对象并发使用会破坏可预测性。 |
| 位置 | `seek(qint64)` | 移动到指定绝对位置。 | 超过文件尾不会立即扩展；检查返回值。 |
| 文件尾 | `atEnd()` | 查询是否到达设备末尾。 | `/proc` 等特殊文件可能过早报告结束。 |
| 缓冲 | `flush()` | 刷新设备写缓冲。 | 检查返回值；不等于断电持久化。 |
| 大小 | `size()` | 查询设备或文件长度。 | 可能因外部进程改变而过时。 |
| 大小 | `resize(qint64)` | 调整文件长度。 | 缩小丢数据，扩大写入新增区域。 |
| 映射 | `map(offset, size, flags)` | 将文件范围映射到内存。 | 成功返回地址；映射指针有严格生命周期。 |
| 映射 | `unmap(address)` | 解除内存映射。 | 解除后地址不能继续访问。 |
| 权限 | `permissions()` | 查询权限位。 | 不能作为未来操作的授权保证。 |
| 权限 | `setPermissions(Permissions)` | 设置权限位。 | 不处理完整 ACL，受平台和权限限制。 |
| 时间 | `fileTime(FileTime)` | 查询一种文件时间。 | 无法获得时返回 invalid `QDateTime`。 |
| 时间 | `setFileTime(QDateTime, FileTime)` | 修改一种文件时间。 | 文件必须打开，平台可能不支持。 |
| 继承 | `open(OpenMode)` | 按 Qt 设备模式打开。 | 必须检查返回值；Qt 6.10 起默认可诊断未检查结果。 |
| 继承 | `read()` / `readAll()` / `readLine()` | 读取文件内容。 | 处理 EOF、暂时无数据、错误和大文件内存占用。 |
| 继承 | `write()` | 写入文件内容。 | 处理部分写入；必要时显式 `flush()`。 |
| 继承 | `bytesAvailable()` | 查询当前可读数据量。 | 不代表完整业务数据或未来总量。 |
| 继承 | `bytesToWrite()` | 查询设备写缓冲量。 | 不代表已落盘。 |

### 一句话总结

`QFileDevice` 是 `QFile` 和 `QSaveFile` 共享的“已打开文件设备能力层”：它负责位置、大小、错误、句柄、权限、时间和映射，但不替你决定原子更新、并发协调、路径安全或持久化策略。普通文件直接用 `QFile`，重要更新用 `QSaveFile`，每个关键 I/O 都检查返回值。

