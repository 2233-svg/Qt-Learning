# Qt QBuffer 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QBuffer>`  
> 所属模块：`Qt6::Core`  
> 继承：`QIODevice -> QBuffer`  
> 定位：把 `QByteArray` 包装成可 seek、可读写的内存设备

## 1. QBuffer 解决什么问题

`QBuffer` 让一段内存数据表现得像 `QIODevice`。凡是接受 `QIODevice *` 的 API，都可以用同一套读写逻辑访问 `QByteArray`：

- 用 `QDataStream` 在内存中序列化和反序列化。
- 用 `QTextStream` 生成或解析文本。
- 测试依赖文件、socket 或设备的代码，而不必创建真实文件。
- 对一段字节做 `seek()`、`peek()`、`readLine()` 和增量写入。

它是**随机访问**设备，不是异步网络缓冲。对大文件不要把全部内容先塞进一个 `QByteArray`；那会增加内存峰值。

## 2. 两种数据所有权模式

### 2.1 QBuffer 自己拥有数据

```cpp
QBuffer buffer;
buffer.setData("hello");
buffer.open(QIODevice::ReadOnly);
qDebug() << buffer.readAll();
```

`setData()` 把输入内容放入 QBuffer 自己管理的缓冲区，之后通过 `data()` 或 `buffer()` 读取。

### 2.2 QBuffer 引用外部 QByteArray

```cpp
QByteArray bytes = "abc";
QBuffer buffer(&bytes);
buffer.open(QIODevice::ReadWrite);
buffer.seek(3);
buffer.write("def");
// bytes == "abcdef"
```

此时 QBuffer 不拥有 `bytes`。`bytes` 必须在 buffer 使用期间保持存活，并且不能在外部随意改变导致读写位置、容量和内容假设失效。

如果数据由多个对象共享，明确谁负责修改，必要时在调用前后关闭设备或使用独占的临时副本。

## 3. 和 QDataStream、QTextStream 配合

```cpp
QByteArray packet;
QBuffer buffer(&packet);
buffer.open(QIODevice::WriteOnly);

QDataStream out(&buffer);
out << quint16(0xCAFE) << QStringLiteral("payload");
if (out.status() != QDataStream::Ok)
    return;
```

读回时要重新设置位置：

```cpp
buffer.close();
buffer.open(QIODevice::ReadOnly);
buffer.seek(0);

QDataStream in(&buffer);
quint16 magic = 0;
QString text;
in >> magic >> text;
```

`close()` 不会清空缓冲区，`seek(0)` 才是从头读取的关键。流对象不拥有 QBuffer，所有对象必须覆盖整个读写过程。

## 4. 位置、大小和写入语义

```cpp
QBuffer buffer;
buffer.open(QIODevice::ReadWrite);
buffer.write("abcdef");
buffer.seek(2);
buffer.write("XY");
// buffer.data() == "abXYef"
```

随机写会覆盖当前位置的数据；如果 seek 到末尾，则追加。seek 到超出末尾的位置通常会扩展缓冲区，具体填充行为要按 Qt 版本和设备契约验证，不要用它替代明确的 resize。

`size()` 是缓冲区长度，`pos()` 是当前读写位置，`atEnd()` 表示当前位置已经到达末尾。读取前检查 `bytesAvailable()` 或 `atEnd()`，不要假设一次 `read()` 会返回所需全部内容。

## 5. 测试中的价值

假设业务代码接受 `QIODevice *`：

```cpp
bool readHeader(QIODevice *device, Header *header);
```

测试可以直接构造内存输入：

```cpp
QByteArray encoded = makeHeaderBytes();
QBuffer input(&encoded);
input.open(QIODevice::ReadOnly);

Header header;
QVERIFY(readHeader(&input, &header));
```

这样可以覆盖空输入、截断输入、错误 magic 和多包拼接，而不依赖文件系统时序。

## 6. 常见误区

### 外部 QByteArray 已销毁仍使用 QBuffer

`QBuffer(&bytes)` 保存的是指针，不是所有权。不要返回一个引用局部 QByteArray 的 QBuffer。

### 写入后不 seek 就读取

读写设备的位置会随着写入移动到末尾。读取刚写入的数据前要 `seek(0)` 或关闭后以 ReadOnly 重新打开。

### 以为 QBuffer 是线程安全队列

它只是一个设备对象。多线程同时读写同一个 QBuffer 需要同步，事件循环不会替你保护 QByteArray。

### 用 QBuffer 模拟无限流

QBuffer 有确定的内存大小和随机位置；要模拟分段到达，测试应分次追加数据并明确通知逻辑，而不是把完整输入一次塞进去。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QBuffer(QObject *parent = nullptr)` | 创建一个内部管理 QByteArray 的内存设备。 | 构造不自动打开，也不包含异步线程能力。 |
| 构造 | `QBuffer(QByteArray *buffer, QObject *parent = nullptr)` | 让 QBuffer 访问外部 QByteArray。 | 外部数组不转移所有权，必须在 QBuffer 使用期间存活。 |
| 析构 | `~QBuffer()` | 销毁缓冲设备。 | 外部 QByteArray 不会被删除；QObject parent 规则仍然适用。 |
| 数据 | `buffer()` | 返回可修改的内部或关联 QByteArray。 | 修改内容可能改变 size、位置和后续读写结果；注意引用有效期。 |
| 数据 | `buffer() const` | 以只读引用返回缓冲区。 | 不拥有返回引用；QBuffer 或外部数组变化时内容也会变化。 |
| 数据 | `setBuffer(QByteArray *)` | 切换 QBuffer 关联的外部 QByteArray。 | 设备应在未打开时切换；新数组生命周期由调用者负责。 |
| 数据 | `setData(const QByteArray &)` | 用数据替换 QBuffer 的内容。 | 会改变缓冲区和位置；使用前确认是否需要保留旧数据。 |
| 数据 | `setData(const char *, qsizetype)` | 用原始字节替换缓冲区内容。 | 明确长度，允许包含零字节；输入指针只在调用期间需要有效。 |
| 数据 | `data()` | 返回缓冲区的只读 QByteArray。 | 适合取最终结果；不要用返回值替代设备位置控制。 |
| 生命周期 | `open(OpenMode)` | 按读写模式打开内存设备。 | 打开不会自动清空数据；WriteOnly 的覆盖/位置语义要按当前位置确认。 |
| 生命周期 | `close()` | 关闭 QBuffer，但保留数据。 | 重新读取时通常要重新 open 并 seek(0)。 |
| 位置 | `size()` | 返回当前缓冲区字节数。 | 外部 QByteArray 改变后大小也可能变化。 |
| 位置 | `pos()` | 返回当前读写位置。 | 写入、读取和 seek 都会改变它。 |
| 位置 | `seek(qint64)` | 移动到指定内存位置。 | 只有在有效范围内或设备允许扩展时才成功；检查返回值。 |
| 结束 | `atEnd()` | 判断当前位置是否位于缓冲末尾。 | 不表示设备已经关闭，也不表示数据格式正确。 |
| 读取 | `canReadLine()` | 判断当前位置后是否存在完整换行行。 | 只按换行判断，不理解业务协议。 |
| 派生接口 | `readData(char *, qint64)` | QBuffer 的底层内存读取实现。 | 通常不直接调用；自定义 QIODevice 才需要重写同名接口。 |
| 派生接口 | `writeData(const char *, qint64)` | QBuffer 的底层内存写入实现。 | 设备会改变 QByteArray 和当前位置；检查上层 write 返回值。 |

---

### 一句话总结

`QBuffer` 是“把 QByteArray 变成 QIODevice”的桥梁：它特别适合内存序列化、协议测试和随机读写。要始终分清内部数据与外部 QByteArray 的所有权，并在写后通过 `seek()` 控制读取位置。
