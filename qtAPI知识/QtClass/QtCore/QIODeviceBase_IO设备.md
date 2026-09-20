# Qt QIODeviceBase 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QIODevice>`  
> 所属模块：`Qt6::Core`  
> 继承：无  
> 被继承：`QIODevice`、`QDataStream`、`QDebug`、`QTextStream`  
> 定位：定义 I/O 打开模式的轻量基类

## 1. 它解决什么问题

`QIODeviceBase` 不是一个可以直接打开、读取或写入的设备对象。它的职责很小，也很明确：统一定义 Qt I/O 类型使用的打开模式枚举和标志类型。

它提供两种公开类型：

```cpp
enum OpenModeFlag;
using OpenMode = QFlags<OpenModeFlag>;
```

实际的设备操作仍由 `QIODevice` 及其派生类负责：

```text
QIODeviceBase
    ├─ OpenModeFlag
    └─ OpenMode
          │
          ▼
QIODevice::open(OpenMode)
          │
          ├─ QFile
          ├─ QBuffer
          ├─ QProcess
          ├─ QAbstractSocket
          └─ 其他 QIODevice 派生类
```

因此，阅读这个类时要先记住一句话：

> `QIODeviceBase` 描述“以什么模式使用设备”，不负责“设备本身如何工作”。

它解决的实际问题是让以下 API 使用统一且类型安全的模式参数：

- 文件以只读、读写、追加或独占创建方式打开；
- 内存缓冲区以读写方式使用；
- 进程的标准输入输出采用何种访问模式；
- 文本流或数据流绑定到设备、字节数组或字符串时决定读写方向；
- 自定义 `QIODevice` 派生类使用同一套 Qt 打开模式协议。

## 2. 它不是 `QIODevice`

`QIODeviceBase` 没有以下能力：

- 没有 `open()`；
- 没有 `close()`；
- 没有 `read()` 或 `write()`；
- 没有当前位置、设备大小或错误字符串；
- 没有信号；
- 没有 QObject 身份；
- 没有保存“当前已经打开”的运行时状态。

下面的代码不能表达有意义的设备操作：

```cpp
QIODeviceBase::OpenMode mode = QIODeviceBase::ReadOnly;
```

这只是构造了一个模式值。必须把它交给真正的设备：

```cpp
QFile file("input.txt");
if (!file.open(mode)) {
    qWarning() << file.errorString();
}
```

`QIODeviceBase` 的析构函数是 protected。它是用于统一类型和模式的基类，不是给业务代码直接创建、拥有或通过基类指针删除的独立对象。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)

target_link_libraries(mytarget
    PRIVATE
        Qt6::Core
)
```

### 3.2 qmake

```qmake
QT += core
```

### 3.3 头文件

Qt 6.11.1 类文档列出的头文件是：

```cpp
#include <QIODevice>
```

Qt 6 还安装了转发头：

```cpp
#include <QIODeviceBase>
```

如果代码同时要使用 `QFile`、`QBuffer` 或其他设备，通常直接包含具体设备头文件即可；如果只在接口中使用 `QIODeviceBase::OpenMode` 类型，可使用 `QIODeviceBase` 转发头。需要写出 `ReadOnly | Text` 这类枚举组合时，优先包含 `<QIODevice>`，因为 `QIODevice` 头文件还声明了该 flags 类型常用的枚举按位运算符。为了兼容较早的 Qt 6 代码和遵循类文档，公共示例仍优先使用 `<QIODevice>`。

## 4. 最小使用示例

### 4.1 以只读文本模式打开文件

```cpp
#include <QFile>
#include <QIODevice>

QFile file("input.txt");
const QIODeviceBase::OpenMode mode =
        QIODeviceBase::ReadOnly | QIODeviceBase::Text;

if (!file.open(mode)) {
    qWarning() << "open failed:" << file.errorString();
    return;
}

const QByteArray bytes = file.readAll();
file.close();
```

这里发生了三件不同的事：

1. `QIODeviceBase::ReadOnly | QIODeviceBase::Text` 只是一个位标志组合；
2. `QFile::open()` 根据这个组合尝试打开文件；
3. `QFile` 决定哪些标志有意义，并负责具体的文件系统行为。

### 4.2 以读写模式打开内存缓冲区

```cpp
#include <QBuffer>

QByteArray storage;
QBuffer buffer(&storage);

if (!buffer.open(QIODeviceBase::ReadWrite)) {
    return;
}

buffer.write("hello");
buffer.seek(0);
const QByteArray result = buffer.readAll();
```

同一个 `OpenMode` 类型可以用于文件和内存设备，但 `Append`、`Truncate`、`NewOnly` 等模式在不同设备上的意义和支持程度可能不同。

## 5. 实际使用场景

### 5.1 文件读取和写入

`QFile` 是最常见的使用者：

```cpp
QFile input("config.json");
input.open(QIODeviceBase::ReadOnly);

QFile output("result.bin");
output.open(QIODeviceBase::WriteOnly);
```

文件场景尤其要警惕 `WriteOnly`。对文件系统设备来说，单独使用 `WriteOnly` 通常意味着打开前截断旧内容；如果目标是追加，应明确使用 `Append`，如果目标是防止覆盖，应考虑 `NewOnly`。

### 5.2 网络、进程和串口

`QAbstractSocket`、`QProcess`、`QSerialPort` 等类型也使用 `QIODeviceBase::OpenMode`，但它们不是普通文件：

- 套接字通常是顺序设备，不能用 `seek()`；
- 进程的读写方向表示标准输入输出通道；
- 串口的打开模式还受端口状态和平台驱动影响；
- 文件专用的 `NewOnly`、`ExistingOnly` 不应随意传给这些设备。

模式类型可以统一，设备语义不能想当然地统一。

### 5.3 数据流和文本流

`QDataStream` 和 `QTextStream` 可以绑定到 `QIODevice`、`QByteArray` 或 `QString` 等对象。构造函数中的 `OpenMode` 决定流是否允许读取、写入或两者兼有：

```cpp
QByteArray bytes;
QDataStream stream(&bytes, QIODeviceBase::ReadWrite);
```

这里 `OpenMode` 仍然只是访问方向和附加模式的描述；数据格式、字符编码和序列化协议由 `QDataStream` 或 `QTextStream` 自己决定。

### 5.4 自定义设备类

自定义 `QIODevice` 派生类的 `open()` 通常接受：

```cpp
bool open(QIODeviceBase::OpenMode mode);
```

实现时应：

- 检查设备支持的模式；
- 在成功时保存模式状态；
- 对不支持的标志返回失败并设置错误；
- 让 `openMode()` 与真实状态一致；
- 明确 `Text`、`Unbuffered` 和文件专用标志是否有意义。

`QIODeviceBase` 不会替自定义设备验证标志组合，也不会自动拒绝不兼容的模式。

## 6. `OpenMode` 是什么

`OpenMode` 是：

```cpp
QFlags<OpenModeFlag>
```

它可以保存一个或多个 `OpenModeFlag` 的按位或组合：

```cpp
QIODeviceBase::OpenMode mode =
        QIODeviceBase::ReadOnly | QIODeviceBase::Text;
```

读取标志时可以使用 `QFlags` 提供的查询能力：

```cpp
if (mode.testFlag(QIODeviceBase::ReadOnly)) {
    // 允许读取
}

if (mode.testFlag(QIODeviceBase::Text)) {
    // 请求文本换行转换
}
```

`OpenMode` 与普通 `int` 的重要区别是类型更明确。把另一个无关枚举或任意整数直接传给接受 `OpenMode` 的函数，通常会在编译期暴露错误，而不是悄悄把不相关的位混进模式参数。

### 6.1 `NotOpen` 是零值

```cpp
QIODeviceBase::NotOpen == 0x0000
```

它表示没有打开模式。它通常用于表示设备尚未打开或已经关闭的模式状态。

`NotOpen` 不会主动关闭对象，也不会代替 `QIODevice::close()`。真正关闭设备应调用设备的 `close()`。

### 6.2 `ReadWrite` 是组合别名

```cpp
QIODeviceBase::ReadWrite
    == QIODeviceBase::ReadOnly | QIODeviceBase::WriteOnly
```

它不是第三种独立访问能力，而是同时设置读和写位。需要判断读写能力时，可以检查相应位；如果需要判断整个模式是否恰好等于某个组合，还要注意是否存在额外的 `Text`、`Append` 等标志。

### 6.3 标志组合不等于所有设备都支持

`OpenMode` 只负责表达请求。最终是否支持由具体设备类决定：

```cpp
QFile file("data.bin");
file.open(QIODeviceBase::ReadOnly | QIODeviceBase::Unbuffered);
```

这段代码的合法性和效果取决于 `QFile` 及当前平台。不要因为编译通过，就认为设备一定按请求执行了所有标志。

## 7. `OpenModeFlag` 逐项语义

### 7.1 `NotOpen`

```cpp
QIODeviceBase::NotOpen // 0x0000
```

**含义：** 设备没有打开模式。

**使用场景：**

- 表示初始或关闭状态；
- 初始化一个 `OpenMode` 变量；
- 在调试日志中表达设备尚未打开。

**边界：**

- 不会自动调用 `close()`；
- 不会释放文件、套接字或缓冲区；
- 不应把“模式为零”误认为“设备对象已经完成所有清理”。

### 7.2 `ReadOnly`

```cpp
QIODeviceBase::ReadOnly // 0x0001
```

**含义：** 设备以读取方式打开。

**典型场景：**

```cpp
QFile file("config.json");
file.open(QIODeviceBase::ReadOnly);
```

**边界：**

- 不能假设写操作会被静默忽略；写入通常失败；
- 对 `QFile`，以 `ReadOnly` 打开不存在的文件会失败；
- 读取能力不代表数据已经全部可用，顺序设备还要等待 `readyRead()` 或调用 `waitForReadyRead()`；
- 读写位置和是否支持 `seek()` 仍由具体设备决定。

### 7.3 `WriteOnly`

```cpp
QIODeviceBase::WriteOnly // 0x0002
```

**含义：** 设备以写入方式打开。

**最重要的边界：**

- 对文件系统设备，单独使用 `WriteOnly` 通常隐含 `Truncate`；
- 原有文件内容可能在打开时被清空；
- 如果希望追加，应明确考虑 `Append`；
- 如果希望只创建新文件而不覆盖已有文件，应考虑 `NewOnly`；
- 不同设备可以对 `WriteOnly` 采用不同实现。

需要保留旧文件内容时，不要凭经验写成：

```cpp
file.open(QIODeviceBase::WriteOnly);
```

而应根据意图明确选择：

```cpp
file.open(QIODeviceBase::WriteOnly | QIODeviceBase::Append);
```

或者：

```cpp
file.open(QIODeviceBase::WriteOnly | QIODeviceBase::NewOnly);
```

### 7.4 `ReadWrite`

```cpp
QIODeviceBase::ReadWrite // ReadOnly | WriteOnly
```

**含义：** 设备同时允许读取和写入。

**典型场景：**

- 随机访问文件；
- 可读写的 `QBuffer`；
- 需要同时处理输入和输出的设备；
- 读写型 `QDataStream`。

**边界：**

- 同时可读写不代表读写位置自动分离；
- 随机访问设备通常需要在读写之间显式 `seek()`；
- 顺序设备不支持任意位置切换；
- 文件打开的截断、追加或创建语义还要结合 `Append`、`NewOnly` 等标志判断。

### 7.5 `Append`

```cpp
QIODeviceBase::Append // 0x0004
```

**含义：** 写入内容追加到设备末尾。

**典型场景：**

```cpp
QFile logFile("application.log");
if (logFile.open(QIODeviceBase::WriteOnly | QIODeviceBase::Append)) {
    logFile.write("next line\n");
}
```

**边界：**

- 它主要对文件等可追加设备有明确意义；
- 具体设备可能忽略或不支持；
- 追加模式不等于多线程写入安全；
- 多个进程同时追加时的原子性和记录边界要由平台和设备语义确认；
- 追加写入仍然需要写权限，不能只传 `Append` 就假设设备会自行决定访问方向。

### 7.6 `Truncate`

```cpp
QIODeviceBase::Truncate // 0x0008
```

**含义：** 如果设备支持，在打开前截断已有内容。

**风险：**

- 旧数据会丢失；
- 打开成功后通常没有撤销截断的机会；
- 不能把它理解成“写入结束后再截断到最终长度”；
- 对顺序设备或不支持截断的设备可能没有意义。

如果代码只是想覆盖某个文件，仍然应先确认是否真的允许破坏旧内容。需要安全替换时，可以先写临时文件，再用文件系统级替换策略完成提交。

### 7.7 `Text`

```cpp
QIODeviceBase::Text // 0x0010
```

**含义：** 请求文本模式下的换行转换：

- 读取时，把设备中的行结束符转换为 `'\n'`；
- 写入时，把 `'\n'` 转换为本地约定的行结束符，例如 Windows 常见的 `"\r\n"`。

**关键边界：**

- `Text` 处理的是换行，不是字符编码；
- 它不会把 UTF-8、UTF-16 或本地编码自动互相转换；
- 字符编码应由 `QTextStream` 或显式编解码逻辑处理；
- 二进制格式不应随意使用 `Text`，否则字节内容可能被改变；
- 某些设备或平台可能不需要或不支持文本转换。

### 7.8 `Unbuffered`

```cpp
QIODeviceBase::Unbuffered // 0x0020
```

**含义：** 请求绕过设备自身的缓冲。

**它不代表：**

- 每次写入都立即落盘；
- 操作系统完全不缓存；
- 网络数据会立即到达对端；
- `flush()`、同步写或文件系统持久化已经发生。

**边界：**

- 某些设备不支持；
- Qt 文档明确指出 `QTcpSocket` 不支持该模式；
- 在 Windows 上，`QFile` 受平台原生 API 限制，可能不支持；
- 绕过缓冲通常会影响吞吐量，应以测量结果决定是否使用。

### 7.9 `NewOnly`

```cpp
QIODeviceBase::NewOnly // 0x0040
```

**含义：** 只有目标文件不存在时才创建并打开；如果已经存在则失败。

**关键语义：**

- 操作系统提供“只有当前创建者成功”的保证；
- 该标志隐含 `WriteOnly`；
- 与 `ReadWrite` 组合是允许的；
- 自 Qt 5.11 提供；
- Qt 6.11 文档中该标志目前只影响 `QFile`。

**典型场景：**

- 创建一次性输出文件；
- 避免覆盖用户已有文件；
- 在文件系统层面实现独占创建。

**边界：**

- 不要把它传给套接字、进程或一般 `QIODevice` 派生类；
- 对不支持该标志的其他类使用可能产生未定义行为；
- “文件不存在”检查和创建之间的竞态不能用手动 `exists()` 加 `open()` 替代原子创建。

### 7.10 `ExistingOnly`

```cpp
QIODeviceBase::ExistingOnly // 0x0080
```

**含义：** 只有目标文件已经存在时才打开；不存在则失败。

**关键语义：**

- 必须与 `ReadOnly`、`WriteOnly` 或 `ReadWrite` 之一一起使用；
- 对 `QFile` 单独配合 `ReadOnly` 通常是冗余的，因为只读打开不存在文件本来就会失败；
- 自 Qt 5.11 提供；
- Qt 6.11 文档中该标志目前只影响 `QFile`。

**边界：**

- 不应传给当前不支持它的设备类；
- 它表达文件存在性约束，不表达读写权限；
- 文件在检查后可能被其他进程删除，最终仍需检查 `open()` 返回值。

## 8. 常用组合的意图

| 组合 | 典型意图 | 主要风险 |
| --- | --- | --- |
| `ReadOnly` | 读取现有内容 | 不可写；顺序设备可能需要等待数据 |
| `ReadOnly \| Text` | 按文本行读取 | `Text` 改变换行解释，但不处理字符编码 |
| `WriteOnly` | 写出新内容 | 对文件通常会截断旧内容 |
| `WriteOnly \| Append` | 追加日志或记录 | 设备是否支持追加；并发记录边界仍需设计 |
| `ReadWrite` | 同时读写 | 读写位置、seek 和缓存刷新需要明确 |
| `WriteOnly \| NewOnly` | 只创建新文件 | 已存在则失败；目前主要用于 `QFile` |
| `ReadWrite \| ExistingOnly` | 只打开已存在文件并读写 | 目前主要用于 `QFile`；仍需检查打开结果 |
| `ReadOnly \| Unbuffered` | 请求绕过设备缓冲读取 | 设备和平台可能不支持，性能可能下降 |
| `WriteOnly \| Truncate` | 明确清空旧内容后重写 | 旧内容不可恢复，必须确认这是预期行为 |

不要用模式组合的名字推断所有设备都会有相同效果。比如 `Truncate` 对文件清晰，对网络套接字没有等价概念。

## 9. 与 `QIODevice` 的关系

### 9.1 `QIODevice` 继承模式类型

因为 `QIODevice` 继承 `QIODeviceBase`，常见代码也可以写成：

```cpp
QFile file("data.txt");
file.open(QIODevice::ReadOnly | QIODevice::Text);
```

`QIODevice::ReadOnly`、`QIODevice::OpenMode` 等名称来自继承的基类类型。使用 `QIODeviceBase::` 前缀则更直接地表达这些名字的真正定义位置。

### 9.2 设备状态由 `QIODevice` 管理

打开后要通过设备 API 检查状态：

```cpp
if (!file.isOpen())
    return;

QIODeviceBase::OpenMode actualMode = file.openMode();
```

模式变量本身没有“已经成功”的信息。即使构造了一个 `ReadOnly`，也不代表目标资源存在或已经成功打开。

### 9.3 `openMode()` 可能包含设备实际状态

`QIODevice::openMode()` 返回设备当前的 `OpenMode`。它可以用于查看设备当前是否读、写、文本或追加，但不要只通过比较整个 flags 值判断能力：

```cpp
if (file.openMode().testFlag(QIODeviceBase::ReadOnly)) {
    // 当前模式包含读取能力
}
```

如果要判断“只读且没有其他标志”，才适合进行完整组合比较，而且应明确这种严格比较是否真的是业务意图。

## 10. 与 `QTextStream` 的关系：Text 不等于编码

这是 `QIODeviceBase` 最容易产生的概念混淆之一。

```cpp
QFile file("notes.txt");
file.open(QIODeviceBase::ReadOnly | QIODeviceBase::Text);

QTextStream stream(&file);
stream.setEncoding(QStringConverter::Utf8);
const QString text = stream.readAll();
```

在这里：

- `Text` 负责设备层面的换行转换；
- `QStringConverter::Utf8` 负责字节和 Unicode 文本之间的编码转换；
- `QTextStream` 负责按文本语义读取。

如果文件是二进制协议，通常不应设置 `Text`，也不应把二进制字节交给文本流解释。

## 11. 自定义 `QIODevice` 时如何使用这些标志

如果实现自定义设备，应把 `OpenMode` 当成一个请求，而不是无条件接受的承诺：

```cpp
class MyDevice : public QIODevice
{
public:
    using QIODevice::QIODevice;

    bool open(QIODeviceBase::OpenMode mode) override
    {
        if (mode.testFlag(QIODeviceBase::Append)
            && !supportsAppend())
            return false;

        if (mode.testFlag(QIODeviceBase::Truncate)
            && !supportsTruncate())
            return false;

        if (!backendOpen(mode))
            return false;

        setOpenMode(mode);
        return true;
    }

protected:
    qint64 readData(char *data, qint64 maxSize) override;
    qint64 writeData(const char *data, qint64 maxSize) override;
};
```

实现时还要注意：

- `ReadOnly`、`WriteOnly`、`ReadWrite` 的冲突和支持关系；
- 是否允许 `NotOpen` 作为输入；
- `Text` 是否由设备处理，还是交给上层；
- `Unbuffered` 是否真的能由后端实现；
- `NewOnly`、`ExistingOnly` 是否应拒绝；
- 失败时是否设置有用的错误信息；
- 成功时是否调用 `setOpenMode()` 同步内部状态。

不要因为 `OpenMode` 是 `QFlags` 就接受所有位组合。设备的能力边界应该由实现明确表达。

## 12. 生命周期、所有权与线程边界

`QIODeviceBase` 本身不拥有文件、套接字或缓冲区，它只提供类型定义。真正的生命周期规则由使用它的设备或流决定：

- `QFile` 对象销毁时关闭它所管理的文件句柄；
- `QBuffer` 是否拥有外部 `QByteArray` 取决于构造方式和对象生命周期；
- `QProcess` 的打开模式描述进程通道，而不是外部文件的所有权；
- `QTextStream` 绑定设备时，流通常不负责删除调用者提供的设备；
- 多线程访问同一设备还要遵循具体设备的线程和重入规则。

`OpenMode` 是一个轻量值，可以按值传递、保存和返回；但它不延长任何设备、文件或底层资源的生命周期。

## 13. 常见误区与排查顺序

### 13.1 把 `QIODeviceBase` 当成可用设备

**问题：** 试图在 `QIODeviceBase` 上调用 `open()`、`read()` 或 `close()`。

**处理：** 使用 `QFile`、`QBuffer`、`QProcess`、套接字等真正的设备类；`QIODeviceBase` 只提供模式类型。

### 13.2 `WriteOnly` 清空了已有文件

**问题：** 打开日志或缓存文件后旧内容消失。

**原因：** 文件系统设备的 `WriteOnly` 通常隐含截断。

**处理：** 追加使用 `WriteOnly | Append`，防覆盖使用 `WriteOnly | NewOnly`，重写文件前明确确认数据损失是预期行为。

### 13.3 把 `Text` 当成 UTF-8 开关

**问题：** 设置了 `Text`，却仍然出现中文乱码。

**原因：** `Text` 只处理换行，不处理字符编码。

**处理：** 使用 `QTextStream` 的编码设置或显式转换器。

### 13.4 对所有设备使用 `NewOnly` 或 `ExistingOnly`

**问题：** 非文件设备打开失败、行为不一致，或落入未定义行为。

**原因：** Qt 6.11 文档明确说明这两个标志目前只影响 `QFile`。

**处理：** 仅对支持它们的文件设备使用；对其他设备先查对应类文档。

### 13.5 以为 `Unbuffered` 等于立即落盘

**问题：** 设置了 `Unbuffered`，但数据仍未立即出现在磁盘或对端。

**原因：** Qt 设备缓冲、操作系统缓存、文件系统持久化和网络栈是不同层次。

**处理：** 根据目标要求分别考虑设备 flush、平台同步 API、协议确认和持久化策略。

### 13.6 只构造模式值，不检查 `open()`

**问题：** 继续读写一个实际没有打开的设备。

**处理：**

```cpp
if (!device.open(mode)) {
    qWarning() << device.errorString();
    return;
}
```

模式值没有成功状态，只有 `open()` 的返回值和设备状态能回答“是否真的打开”。

### 13.7 依赖完整 flags 相等比较

**问题：** `openMode() == QIODeviceBase::ReadOnly` 在加入 `Text` 后突然失败。

**原因：** `OpenMode` 可以同时包含访问方向和附加标志。

**处理：** 判断能力用 `testFlag()`；只有业务确实要求“恰好这个组合”时才做完整比较。

## 14. 版本边界

### Qt 5.11

`NewOnly` 和 `ExistingOnly` 在 Qt 5.11 引入。需要兼容更早 Qt 版本时，不能无条件引用这两个枚举值。

### Qt 6

`QIODeviceBase` 作为独立的模式基类用于承载 `QIODevice`、`QDataStream`、`QDebug` 和 `QTextStream` 共享的 `OpenMode` 类型。Qt 6.11.1 的 public header 中仍然只有枚举、flags 别名和 protected 析构函数。

### Qt 6.11.1

在 Qt 6.11.1 文档中：

- `NewOnly`、`ExistingOnly` 当前主要影响 `QFile`；
- `Unbuffered`、`Truncate` 等标志对部分设备没有意义；
- 标志的最终效果由具体设备类和平台实现决定；
- 文本换行转换与字符编码仍是两个独立问题。

## 15. API 逐项说明

### `protected ~QIODeviceBase()`

**作用：** 提供受保护的默认析构函数，使 `QIODeviceBase` 适合作为其他 I/O 类型的基类。

**关键语义：**

- 析构函数不是公共 API；
- `QIODeviceBase` 不应该被当作普通独立对象创建和销毁；
- 不能安全地通过 `QIODeviceBase *` 删除一个派生对象；
- 它不负责释放任何设备资源。

### `enum QIODeviceBase::OpenModeFlag`

**作用：** 定义设备打开时可使用的访问方向和附加模式。

**关键语义：**

- 枚举值是位标志，可以用 `|` 组合；
- 单独的访问方向包括 `ReadOnly`、`WriteOnly` 和组合别名 `ReadWrite`；
- `Append`、`Truncate`、`Text`、`Unbuffered`、`NewOnly`、`ExistingOnly` 是附加模式；
- 具体设备可以拒绝或忽略不支持的组合。

### `QIODeviceBase::OpenMode`

**作用：** `QFlags<OpenModeFlag>` 的别名，用于保存一个或多个打开模式。

**关键语义：**

- 可由枚举值按位或构造；
- 可传给 `QIODevice::open()`、`QFile::open()` 等 API；
- 可以使用 `testFlag()` 等 `QFlags` 查询；
- 只是值类型，不保存设备指针、打开结果或错误信息；
- 不会替调用者保持底层资源存活。

## API 速查表
### 生命周期与公开类型

| API | 类型 | 作用 | 使用重点 |
| --- | --- | --- | --- |
| `protected ~QIODeviceBase()` | 保护析构函数 | 作为 I/O 模式基类的默认析构入口 | 不是普通独立对象；不要通过 `QIODeviceBase *` 删除派生设备 |
| `enum QIODeviceBase::OpenModeFlag` | 枚举 | 定义打开方向和附加模式 | 具体含义由接收该模式的设备类最终解释 |
| `QIODeviceBase::OpenMode` | `QFlags<OpenModeFlag>` 别名 | 保存多个 `OpenModeFlag` 的组合 | 使用 `|` 组合，使用 `testFlag()` 查询；不包含打开结果 |

### `OpenModeFlag` 枚举值

| 枚举值 | 数值/组合 | 作用 | 使用重点 |
| --- | --- | --- | --- |
| `QIODeviceBase::NotOpen` | `0x0000` | 表示没有打开模式 | 不等于调用了 `close()`，也不会释放设备资源 |
| `QIODeviceBase::ReadOnly` | `0x0001` | 允许读取设备 | 文件不存在时通常打开失败；顺序设备可能还要等待数据 |
| `QIODeviceBase::WriteOnly` | `0x0002` | 允许写入设备 | 对文件通常隐含截断；避免无意清空旧内容 |
| `QIODeviceBase::ReadWrite` | `ReadOnly \| WriteOnly` | 同时允许读写 | 读写位置和设备是否支持 seek 仍需单独处理 |
| `QIODeviceBase::Append` | `0x0004` | 写入到设备末尾 | 主要用于文件；并发追加不自动保证记录原子性 |
| `QIODeviceBase::Truncate` | `0x0008` | 打开前截断已有内容 | 可能造成不可恢复的数据丢失 |
| `QIODeviceBase::Text` | `0x0010` | 启用换行转换 | 只处理换行，不负责 UTF-8 等字符编码 |
| `QIODeviceBase::Unbuffered` | `0x0020` | 请求绕过设备缓冲 | 设备和平台可能不支持；不等于立即落盘 |
| `QIODeviceBase::NewOnly` | `0x0040` | 仅在文件不存在时创建 | Qt 5.11 起；目前主要影响 `QFile`；隐含写入意图 |
| `QIODeviceBase::ExistingOnly` | `0x0080` | 仅打开已存在文件 | Qt 5.11 起；目前主要影响 `QFile`；需与读写标志组合 |

## 17. 一句话总结

`QIODeviceBase` 不是设备实现，而是 Qt I/O 体系共享的打开模式定义：用 `OpenModeFlag` 表达访问方向和附加语义，用 `OpenMode` 组合这些标志，再交给 `QFile`、`QBuffer`、`QProcess` 或其他真实设备执行。最需要记住的是 `WriteOnly` 的文件截断风险、`Text` 不等于字符编码，以及 `NewOnly`、`ExistingOnly`、`Unbuffered` 等标志的设备和平台边界。
