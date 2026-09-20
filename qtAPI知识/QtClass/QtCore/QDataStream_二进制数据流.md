# Qt QDataStream 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDataStream>`  
> 所属模块：`Qt6::Core`  
> 继承：`QIODeviceBase -> QDataStream`  
> 定位：按明确的 Qt 二进制格式读写基础类型、Qt 类型和容器

## 1. QDataStream 解决什么问题

`QDataStream` 把二进制数据编码和设备读写结合起来。它可以写入 `QFile`、`QBuffer`、socket 等 `QIODevice`，也可以直接读写 `QByteArray`：

```cpp
QByteArray bytes;
QDataStream out(&bytes, QIODevice::WriteOnly);
out << qint32(42) << QStringLiteral("hello");

QDataStream in(bytes);
qint32 number = 0;
QString text;
in >> number >> text;
```

它解决的是“双方按同一套二进制协议读写”的问题，不是通用对象持久化框架。写端和读端必须对以下事项达成一致：

- 字段顺序。
- 每个字段的类型和长度。
- `QDataStream::Version`。
- 字节序。
- 浮点精度。
- 版本升级和缺失字段策略。

如果需要人类可读、跨语言、便于手工调试的格式，优先考虑 JSON、CBOR 或文本协议；如果需要紧凑、高速且由 Qt 两端共同消费，`QDataStream` 很合适。

## 2. 绑定设备和字节数组

### 2.1 写入文件

```cpp
QFile file("record.dat");
if (!file.open(QIODevice::WriteOnly)) {
    qWarning() << file.errorString();
    return;
}

QDataStream out(&file);
out.setVersion(QDataStream::Qt_6_11);
out.setByteOrder(QDataStream::LittleEndian);
out << qint32(7) << QStringLiteral("record");

if (out.status() != QDataStream::Ok)
    qWarning() << "serialization failed";
```

`QDataStream` 不拥有通过构造函数传入的 `QIODevice`。设备必须在流使用期间保持有效，并由调用者负责打开和关闭。

### 2.2 读写 QByteArray

```cpp
QByteArray payload;
{
    QDataStream out(&payload, QIODevice::WriteOnly);
    out << quint16(0x1234) << QByteArray("body");
}

QDataStream in(payload);
quint16 magic = 0;
QByteArray body;
in >> magic >> body;
```

从 `QByteArray` 构造的读流读的是一份固定输入；向 `QByteArray *` 写入时，流会把数据追加或按设备位置写入，具体行为取决于打开模式和设备位置。

## 3. 格式兼容：版本号不是应用版本号

```cpp
out.setVersion(QDataStream::Qt_6_6);
in.setVersion(QDataStream::Qt_6_6);
```

`Version` 控制 Qt 类型的序列化格式。它不是你的文件格式版本，也不自动处理字段增删。通常要同时写入自己的 magic 和 schema version：

```cpp
out << quint32(0x52454331); // "REC1"
out << quint16(3);          // application schema version
out << QStringLiteral("name");
```

读取时先验证 magic，再按 schema version 选择字段：

```cpp
quint32 magic = 0;
quint16 schema = 0;
in >> magic >> schema;
if (magic != 0x52454331 || in.status() != QDataStream::Ok)
    return false;

if (schema >= 3)
    in >> newField;
```

不要把当前编译使用的默认版本当作永久文件格式。应用升级后，明确固定 `setVersion()`，并为旧文件保留读取分支。

## 4. 字节序和浮点精度

### 4.1 字节序

```cpp
out.setByteOrder(QDataStream::LittleEndian);
```

字节序影响多字节整数和相关二进制数值的排列。跨平台或跨语言协议应显式设置，不要依赖主机默认字节序。

### 4.2 浮点精度

```cpp
out.setFloatingPointPrecision(QDataStream::DoublePrecision);
```

精度设置影响 float/double 的序列化方式。读端必须使用与写端相容的设置。金额、计数或协议字段通常不应直接用浮点表示，优先使用定点整数或明确的十进制格式。

## 5. 状态：流对象不会抛异常

```cpp
QDataStream in(&file);
qint32 value = 0;
in >> value;

switch (in.status()) {
case QDataStream::Ok:
    break;
case QDataStream::ReadPastEnd:
    // 输入不完整
    break;
case QDataStream::ReadCorruptData:
    // 格式或内容不可信
    break;
case QDataStream::WriteFailed:
    // 底层设备写入失败
    break;
case QDataStream::SizeLimitExceeded:
    // 长度字段超出当前平台或版本可表示范围
    break;
}
```

`operator bool()` 等价于 `status() == Ok`：

```cpp
if (!(in >> value))
    return false;
```

读取外部或不可信数据时，不能只检查一个字段。长度字段、容器大小和嵌套结构都可能触发超大分配或读取超界；应在协议层增加合理上限。

## 6. 基础类型和 Qt 类型的运算符

```cpp
out << qint8(-1)
    << quint32(100)
    << true
    << 3.14f
    << QStringLiteral("Qt");
```

基础类型的运算符负责固定的二进制编码。对自定义类型，按字段顺序定义非成员运算符：

```cpp
struct UserRecord
{
    QString name;
    qint32 age = 0;
};

QDataStream &operator<<(QDataStream &out, const UserRecord &record)
{
    return out << record.name << record.age;
}

QDataStream &operator>>(QDataStream &in, UserRecord &record)
{
    return in >> record.name >> record.age;
}
```

读取时不要在读完所有字段前把半初始化对象发布给其他线程或业务代码。读取失败时要决定是清空对象、保留旧值，还是直接返回错误。

## 7. 长度字段和 raw API

字符串、`QByteArray` 和容器通常会写入长度信息。原始接口适合协议已经定义好长度的场景：

```cpp
const QByteArray payload = getPayload();
out.writeRawData(payload.constData(), payload.size());

QByteArray restored(payload.size(), Qt::Uninitialized);
const qint64 count = in.readRawData(restored.data(), restored.size());
if (count != restored.size())
    return false;
```

`writeBytes()` 会写入长度和内容，`readBytes()` 负责读取这种配对格式：

```cpp
out.writeBytes(payload.constData(), payload.size());

char *data = nullptr;
qint64 length = 0;
in.readBytes(data, length);
QByteArray restored(data, qsizetype(length));
delete[] data;
```

外部输入必须限制 `length`。如果格式是你自己设计的，优先使用明确的 `quint32` 或 `quint64` 长度，并在读取前检查上限，不要无条件按输入长度分配内存。

## 8. 事务：适合流式设备中的半包读取

```cpp
stream.startTransaction();

quint16 type = 0;
quint32 length = 0;
stream >> type >> length;

if (stream.status() == QDataStream::ReadPastEnd) {
    stream.rollbackTransaction();
    return; // 等下一批数据
}

if (length > 1024 * 1024) {
    stream.abortTransaction();
    return; // 协议长度不可信
}

QByteArray payload;
stream >> payload;
if (!stream.commitTransaction())
    handleCorruptFrame();
```

事务让读取失败时可以重新尝试，但它不替你做协议校验，也不回滚已经对外执行的副作用。`rollbackTransaction()` 适合“输入还不完整”，`abortTransaction()` 适合“输入已经损坏或不应继续”。

嵌套事务会增加复杂度。一个解析函数最好明确由谁开始和结束事务，不要让多个层级都假设自己拥有整个设备的事务。

## 9. 容器和版本演进

Qt 容器可以直接流式读写：

```cpp
QList<QString> names;
out << names;
in >> names;
```

常见支持包括 `QList`、`QSet`、`QHash`、`QMultiHash`、`QMap`、`QMultiMap` 和 `std::pair`，前提是元素类型本身有对应流运算符。

容器格式包含元素数量。读不可信数据时要防止：

- 数量字段导致巨量内存预留。
- 元素类型读取失败后留下部分容器。
- 旧版本字段顺序与新版本不一致。
- 哈希或映射的顺序被误当成稳定序列化顺序。

如果文件需要长期保存，使用显式 schema version，并对容器大小、字符串长度和嵌套深度设定应用层限制。

## 10. 常见误区

### 用默认版本读写永久文件

Qt 默认版本会随构建环境变化。持久化文件必须固定 `setVersion()` 并维护自己的 schema version。

### 只判断 `atEnd()`

`atEnd()` 不能说明格式正确，也不能替代 `status()`。读取字段后检查流状态。

### 把 `readBytes()` 的长度当成可信

长度来自输入，可能导致超大分配。先读取到受控长度，或在自定义格式中自行验证上限。

### 直接序列化裸指针

流运算符对指针通常不表达对象所有权和对象内容。要写对象，写它的稳定字段；不要把地址当作可移植数据。

### 用 `QDataStream` 传输跨语言协议却不写协议说明

另一语言必须知道每个字段的字节序、长度编码、字符串格式和版本。必要时使用更明确的协议格式。

### 忘记检查 `write()` 的底层状态

`operator<<` 返回流本身，不代表成功。序列化结束后检查 `status()` 或 `operator bool()`。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDataStream()` | 创建未绑定设备的流。 | 使用读写运算符前必须 `setDevice()` 或绑定 QByteArray。 |
| 构造 | `QDataStream(QIODevice *)` | 把流绑定到已有 QIODevice。 | 流不拥有设备；设备必须在流使用期间存活并处于合适模式。 |
| 构造 | `QDataStream(QByteArray *, OpenMode)` | 将流绑定到可写 QByteArray 设备。 | QByteArray 指针必须有效；写入位置和模式决定是否覆盖或追加。 |
| 构造 | `QDataStream(const QByteArray &)` | 从 QByteArray 创建只读输入流。 | 输入数据不会因流读取而自动补充；需要新数据要重新构造或使用设备。 |
| 析构 | `~QDataStream()` | 释放流自身状态。 | 不关闭或删除外部 QIODevice。 |
| 设备 | `device()` | 返回当前绑定设备。 | 返回指针不转移所有权；可能为空。 |
| 设备 | `setDevice(QIODevice *)` | 更换当前绑定设备。 | 更换前处理好旧设备位置、状态和事务；流格式设置仍保留。 |
| 状态 | `status()` | 读取 `Ok`、`ReadPastEnd`、`ReadCorruptData`、`WriteFailed` 或 `SizeLimitExceeded`。 | Qt 6.8 起可直接使用；外部输入要区分不完整与损坏。 |
| 状态 | `setStatus(Status)` | 设置流状态。 | 主要给自定义解析或测试使用；不要用它掩盖真实 I/O 错误。 |
| 状态 | `resetStatus()` | 把流状态恢复为 Ok。 | 只清除状态标志，不会恢复已消费的数据或修复设备错误。 |
| 状态 | `operator bool()` | 判断流状态是否为 Ok。 | 适合 `if (!(stream >> value))`；不能说明业务字段值合法。 |
| 格式 | `version()` | 查询当前 Qt 数据流版本。 | 这是 Qt 编码版本，不是应用文件 schema 版本。 |
| 格式 | `setVersion(int)` | 固定 Qt 类型的序列化版本。 | 持久化格式要显式设置，并让读写两端保持一致。 |
| 格式 | `byteOrder()` | 查询当前多字节数据的字节序。 | 跨平台协议应显式配置，不要依赖主机默认。 |
| 格式 | `setByteOrder(ByteOrder)` | 设置 BigEndian 或 LittleEndian。 | 读写端必须一致；字符串和原始字节不会因它自动转换编码。 |
| 格式 | `floatingPointPrecision()` | 查询浮点精度策略。 | 只影响浮点流格式，不替代数值范围和精度设计。 |
| 格式 | `setFloatingPointPrecision(FloatingPointPrecision)` | 设置 SinglePrecision 或 DoublePrecision。 | Qt 6.8 起可用；读端必须匹配协议约定。 |
| 输入输出 | `operator>>(char/qint8/quint8/qint16/quint16/qint32/quint32/qint64/quint64)` | 读取固定宽度整数或字符。 | 使用明确的 qint 类型设计协议，避免 `int` 大小和符号歧义。 |
| 输入输出 | `operator<<(char/qint8/quint8/qint16/quint16/qint32/quint32/qint64/quint64)` | 写入固定宽度整数或字符。 | 字节序影响多字节数值；协议字段顺序必须固定。 |
| 输入输出 | `operator>>(bool)` / `operator<<(bool)` | 读写布尔值。 | 两端都使用同一流版本；不要把任意非零整数自动当作协议合法布尔值。 |
| 输入输出 | `operator>>(float/double)` / `operator<<(float/double)` | 读写浮点数。 | 精度和 NaN、Infinity 处理要纳入协议约定。 |
| 输入输出 | `operator>>(char16_t/char32_t)` / `operator<<(char16_t/char32_t)` | 读写 UTF-16 或 UTF-32 代码单元。 | 代码单元不等同于完整 Unicode 字素；文本编码应有明确边界。 |
| 输入输出 | `operator>>(char *&)` / `operator<<(const char *)` | 读写以流格式编码的 C 字符串。 | 读出的内存需要释放；不要把不可信内容当无界 C 字符串使用。 |
| Qt 类型 | `operator>>(QString/QByteArray)` / `operator<<(QString/QByteArray)` | 读写 Qt 字符串和字节数组。 | 包含长度；外部输入必须限制长度和总分配量。 |
| 容器 | `operator>>(QList/QSet)` / `operator<<(QList/QSet)` | 读写顺序容器或集合。 | 元素必须可流式读写；读取失败时要检查容器状态和大小。 |
| 容器 | `operator>>(QHash/QMultiHash)` / `operator<<(QHash/QMultiHash)` | 读写哈希容器。 | 迭代顺序不应当作为持久化格式的稳定顺序。 |
| 容器 | `operator>>(QMap/QMultiMap)` / `operator<<(QMap/QMultiMap)` | 读写有序映射容器。 | key/value 类型都必须有流运算符；多值映射要明确重复 key 语义。 |
| 辅助类型 | `operator>>(std::pair)` / `operator<<(std::pair)` | 按 first、second 顺序读写 pair。 | 两端字段顺序固定；元素类型必须支持流运算符。 |
| 原始数据 | `readRawData(char *, qint64)` | 读取指定长度的原始字节，不附带长度。 | 调用者提供缓冲区和长度；返回值可能小于请求长度。 |
| 原始数据 | `writeRawData(const char *, qint64)` | 写入指定长度的原始字节，不附带长度。 | 适合已有协议长度字段的 payload；检查返回值和流状态。 |
| 原始数据 | `skipRawData(qint64)` | 跳过指定长度原始字节。 | 输入不足或错误时检查返回值；不能跳过负长度。 |
| 长度数据 | `readBytes(char *&, qint64 &)` | 读取带长度前缀的字节块并分配结果缓冲区。 | 长度来自输入，必须限制；调用者负责释放分配的内存。 |
| 长度数据 | `writeBytes(const char *, qint64)` | 写入长度前缀和字节块。 | 读端必须使用对应格式；旧版本对超大长度有上限。 |
| 长度数据 | `readBytes(char *&, uint &)` | 兼容旧的 uint 长度读取接口。 | Qt 6.11 已弃用方向明确；新代码使用 qint64 重载。 |
| 事务 | `startTransaction()` | 开始读取事务。 | 适合流式半包解析；不要嵌套到无法说明所有权的多层函数中。 |
| 事务 | `commitTransaction()` | 尝试提交读取事务并返回是否成功。 | 若数据不完整可能提交失败；仍要检查 `status()`。 |
| 事务 | `rollbackTransaction()` | 回退当前读取事务。 | 用于等待更多数据；不撤销已经执行的业务副作用。 |
| 事务 | `abortTransaction()` | 放弃当前事务并将流置为错误状态。 | 适合检测到格式损坏或长度不可信时终止解析。 |
| 事务 | `isDeviceTransactionStarted()` | 查询底层设备是否存在活动事务。 | 只反映设备事务状态；不等同于当前 QDataStream 没有错误。 |
| 枚举 | `Version` | 表示 Qt 1.0 到 Qt 6.11 的流格式版本。 | 选择具体版本作为协议兼容策略，不要自动跟随编译环境。 |
| 枚举 | `ByteOrder` | 表示 BigEndian 或 LittleEndian。 | 跨平台二进制协议必须固定。 |
| 枚举 | `Status` | 表示正常、读到末尾、损坏、写失败或长度超限。 | 把不同状态映射到不同错误处理路径。 |
| 枚举 | `FloatingPointPrecision` | 表示单精度或双精度浮点格式。 | 与协议精度和兼容性一起设计。 |

---

### 一句话总结

`QDataStream` 负责“按约定编码和解码”，不负责替你设计协议。固定 Qt stream version，另写应用 schema version，显式设置字节序和浮点精度，读取所有状态并限制输入长度，才能让二进制文件和网络帧在升级、跨平台和异常输入下仍然可靠。
