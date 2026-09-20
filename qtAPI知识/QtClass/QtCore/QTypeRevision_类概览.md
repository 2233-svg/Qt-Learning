# Qt QTypeRevision：表示可带未知段的类型修订号

`QTypeRevision` 是 Qt 6.0 引入的轻量值类型，用两个 8 位段表示一个类型的修订号：高字节是 major，低字节是 minor。每个段都可以是“已知值”或“未知”，因此它比一个简单的 `major.minor` 整数更适合描述元对象系统中的接口版本。

它主要服务于 Qt 元对象信息。`QMetaMethod::revision()` 和 `QMetaProperty::revision()` 返回的非零修订值可以用 `QTypeRevision::fromEncodedVersion()` 解码，从而判断某个方法或属性从哪个 major/minor 修订开始存在。

```cpp
#include <QMetaMethod>
#include <QTypeRevision>

QTypeRevision revision =
    QTypeRevision::fromEncodedVersion(metaMethod.revision());

if (revision.isValid() && revision.hasMajorVersion()) {
    qDebug() << revision.majorVersion();
}
```

## 它解决什么问题

在描述接口演进时，版本信息不总是完整的：

- 可能只知道 major，不知道 minor；
- 可能只知道 minor，不知道 major；
- 可能还没有任何有效修订信息；
- 需要把两个段压缩成元对象系统使用的整数；
- 需要在容器、哈希表或 `QDataStream` 中保存和传输。

`QTypeRevision` 用固定大小的两个字节表达这些状态，不需要分配内存，也不需要解析字符串。它适合作为元数据和协议边界上的值，而不是用来替代完整的产品版本号。

它和 `QVersionNumber` 的职责不同：

- `QTypeRevision` 固定只有 major/minor 两段，并允许每一段未知；
- `QVersionNumber` 可以有任意数量的数字段，更适合软件版本、协议版本或文件格式版本；
- `QTypeRevision` 的编码布局与 Qt 元对象 revision 直接对应。

## 构建与包含

`QTypeRevision` 属于 Qt Core：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QTypeRevision>
```

qmake 工程使用：

```text
QT += core
```

它是一个值类型，不继承 `QObject`，不需要事件循环，也没有线程归属。可以按值复制、作为成员保存和放入 Qt 容器。

## 三种“没有完整版本”的状态

默认构造的对象是无效修订：

```cpp
QTypeRevision invalid;
Q_ASSERT(!invalid.isValid());
Q_ASSERT(!invalid.hasMajorVersion());
Q_ASSERT(!invalid.hasMinorVersion());
```

只知道一个段时，另一个段保持未知：

```cpp
const auto majorOnly = QTypeRevision::fromMajorVersion(2);
const auto minorOnly = QTypeRevision::fromMinorVersion(7);

Q_ASSERT(majorOnly.hasMajorVersion());
Q_ASSERT(!majorOnly.hasMinorVersion());
Q_ASSERT(!minorOnly.hasMajorVersion());
Q_ASSERT(minorOnly.hasMinorVersion());
```

完整的 `2.7` 是两个都已知：

```cpp
const auto complete = QTypeRevision::fromVersion(2, 7);
Q_ASSERT(complete.isValid());
Q_ASSERT(complete.majorVersion() == 2);
Q_ASSERT(complete.minorVersion() == 7);
```

内部用 `0xff` 表示未知，所以 `255` 不能作为普通版本段。合法段范围是 `0 <= segment < 255`，也就是 `0` 到 `254`。

`zero()` 返回的是有效的 `0.0`，不要把它和默认构造的无效对象混为一谈：

```cpp
Q_ASSERT(!QTypeRevision().isValid());
Q_ASSERT(QTypeRevision::zero().isValid());
Q_ASSERT(QTypeRevision::zero().majorVersion() == 0);
Q_ASSERT(QTypeRevision::zero().minorVersion() == 0);
```

## 编码布局与元对象 revision

编码值使用低两字节：

```text
encoded = (major << 8) | minor
```

低字节存 minor，高字节存 major。例如 `2.7` 编码为 `0x0207`：

```cpp
const auto revision = QTypeRevision::fromVersion(2, 7);
const quint16 encoded = revision.toEncodedVersion<quint16>();

Q_ASSERT(encoded == 0x0207);
Q_ASSERT(QTypeRevision::fromEncodedVersion(encoded) == revision);
```

未知段会原样编码为 `0xff`。因此：

```cpp
Q_ASSERT(QTypeRevision::fromMajorVersion(2)
             .toEncodedVersion<quint16>() == 0x02ff);
Q_ASSERT(QTypeRevision::fromMinorVersion(7)
             .toEncodedVersion<quint16>() == 0xff07);
```

这些编码值不是面向用户显示的字符串。显示时应先检查 `hasMajorVersion()` 和 `hasMinorVersion()`，再决定输出 `2`、`2.7`、`.7` 或“未知”等业务格式。

Qt 元对象系统中的非零 `QMetaMethod::revision()` 和 `QMetaProperty::revision()` 使用这种编码。没有通过 `Q_REVISION` 指定 revision 时，元对象 API 返回 `0`；这与“明确指定 `0.0`”在元对象查询层面可能难以区分，因此不要仅凭编码值推断完整的业务版本语义。

## 输入约束：模板不是任意整数转换

`fromVersion()`、`fromMajorVersion()` 和 `fromMinorVersion()` 接受整数模板参数，但运行时会断言传入值是合法段。不要依赖窄化转换把 `255` 或负数“截断成可用值”：

```cpp
const auto revision = QTypeRevision::fromVersion(4, 12);
```

`isValidSegment()` 可以在外部输入进入构造函数前做检查：

```cpp
bool readRevision(int major, int minor, QTypeRevision *out)
{
    if (!QTypeRevision::isValidSegment(major) ||
        !QTypeRevision::isValidSegment(minor))
        return false;

    *out = QTypeRevision::fromVersion(major, minor);
    return true;
}
```

`fromEncodedVersion()` 要求整数类型至少 16 位，并且传入值不能在最低 16 位之外设置比特。带符号类型的最低 16 位也不能带符号位；实际代码优先使用 `quint16`、`quint32` 等无符号类型，避免隐式转换和符号扩展：

```cpp
const quint16 wireValue = readUint16();
const QTypeRevision revision =
    QTypeRevision::fromEncodedVersion(wireValue);
```

同样，`toEncodedVersion<Integer>()` 的 `Integer` 也必须满足 Qt 对编码整数的约束。通常选择 `quint16` 或更宽的无符号整数。

## 比较语义不是简单的字节序

`QTypeRevision` 是 strongly comparable 类型，可以使用 Qt/C++ 的比较运算。比较时先比较 major，再比较 minor；但“未知”不是普通的数值 `255`。

对于同一段，Qt 使用这样的顺序：

```text
正数版本 > 未知 > 0
```

例如在其它段相同的情况下：

```text
1 > 未知 > 0
```

这样可以表达“任何明确的非零修订都比未指定更具体，而未指定又比明确的 0 更高”的接口兼容语义。它意味着：

- 不能把 `toEncodedVersion()` 的结果直接当作普通无符号整数排序；
- 不能用 `majorVersion() == 255` 作为正常的 major 版本；
- 如果业务需要“未知排在最后”或“缺失值优先”，应自己定义排序键，不要假设字节序就是业务顺序。

相等比较则针对两个段的实际编码状态：`2.7` 与另一个 `2.7` 相等，未知段也必须在对应位置都未知才相等。

## 在接口兼容检查中的用法

如果应用要判断某个接口是否至少达到某个完整 revision，先检查段是否已知，再按业务规则比较：

```cpp
bool supportsAtLeast(QTypeRevision actual, QTypeRevision required)
{
    if (!actual.hasMajorVersion() || !actual.hasMinorVersion() ||
        !required.hasMajorVersion() || !required.hasMinorVersion())
        return false;

    return actual >= required;
}
```

这里的“至少支持”是一个业务判断。`QTypeRevision` 本身允许部分未知，所以不能把一个只知道 major 的值自动当成某个具体 minor 来比较。

如果只关心 major：

```cpp
if (revision.hasMajorVersion() && revision.majorVersion() >= 3) {
    enableNewProtocol();
}
```

如果只关心 minor，必须明确 major 是否已经确定。不要在 major 未知时仅比较 minor 并声称接口完整兼容。

## 流序列化、哈希和调试输出

Qt 6.0 起提供 `QDataStream` 的插入和提取运算符：

```cpp
QByteArray bytes;
{
    QDataStream out(&bytes, QIODevice::WriteOnly);
    out << QTypeRevision::fromVersion(2, 7);
}

QTypeRevision restored;
{
    QDataStream in(bytes);
    in >> restored;
}
```

序列化格式属于 `QDataStream` 的类型协议。跨进程、跨版本或持久化到磁盘时，应统一 `QDataStream::Version`、字节序和错误处理；不要把它当成一个可以随意与其他语言互换的文本格式。

头文件还提供 `qHash(const QTypeRevision &, size_t)`，因此可以作为 `QHash` 的键。哈希只要求相等对象得到相同哈希，不代表哈希值具有版本排序意义。

启用调试流时可以直接交给 `QDebug` 输出。调试输出适合日志和诊断，不要把它当稳定的序列化协议或机器解析格式。

## 生命周期、线程和边界

这是两个字节大小的可复制值类型，不持有外部资源，不需要手工释放，也不受 QObject 生命周期影响。

它的线程安全性来自值语义：不同线程各自持有副本没有问题。共享同一个可变变量时，仍然要遵守 C++ 的数据竞争规则；Qt 的小对象并不会自动给你的共享内存加锁。

最重要的边界是输入验证：

- 外部数据可能是负数、`255` 或超出 16 位；
- 默认构造对象是无效修订，不等于 `0.0`；
- 未知段不是普通版本 `255`；
- `majorVersion()` 和 `minorVersion()` 会返回底层 8 位值，读取前应先检查对应的 `has...Version()`；
- `from...()` 的断言不应被当成用户输入校验机制，发布版中也不应依赖断言来处理恶意数据。

## 常见场景

### 读取元对象中的方法或属性修订

这是本类最直接的场景：从 `QMetaMethod::revision()` 或 `QMetaProperty::revision()` 读取编码值，然后解码出 major/minor。

### 描述部分已知的协议能力

插件或远程端可能只报告 major，或只报告 minor。用 `fromMajorVersion()` / `fromMinorVersion()` 保存这种不完整事实，比伪造一个 `0` 更诚实。

### 作为 Qt 容器键

可以使用 `QHash<QTypeRevision, Metadata>` 保存不同 revision 的元数据。键比较和哈希都按值语义工作。

### 轻量二进制协议字段

在协议本身采用 Qt 数据流并且双方都使用兼容 Qt 版本时，可以直接通过 `QDataStream` 读写；若协议需要语言无关的稳定格式，应明确写出两个字节的端序和未知值约定。

## 常见错误与排查顺序

- 把默认构造的 `QTypeRevision` 当成 `0.0`。先区分 `isValid()` 和 `zero()`。
- 把 `255` 当成合法版本段。`255` 保留给未知值，合法范围是 `0..254`。
- 直接读取 `majorVersion()` 或 `minorVersion()` 而不检查 `has...Version()`。
- 把编码值 `0x02ff` 当成 `2.255`，它表示 major 为 2、minor 未知。
- 用编码整数大小代替 `QTypeRevision` 的比较语义。未知段不是普通的 255。
- 用 `fromEncodedVersion()` 接收带符号或超过 16 位范围的未验证外部整数。
- 认为 `QTypeRevision` 可以表示任意长度版本。需要 `2.1.4` 等版本时使用 `QVersionNumber`。
- 只比较 minor 就断言接口兼容，忽略 major 未知或不匹配。
- 把 `QDataStream` 序列化结果当成跨语言公共协议。
- 在多线程之间共享一个可变 `QTypeRevision` 却没有同步。

## 逐项 API 说明

### 构造与创建

#### `QTypeRevision::QTypeRevision()`

构造一个无效 revision。major 和 minor 都是未知状态，不是 `0.0`。

#### `QTypeRevision::fromVersion(Major majorVersion, Minor minorVersion)`

创建两个版本段都已知的 revision。两个参数必须是整数，并且都满足 `0 <= value < 255`；不满足时触发断言。模板约束会在编译期排除非整数类型。

#### `QTypeRevision::fromMajorVersion(Major majorVersion)`

创建只知道 major 的 revision，minor 保持未知。major 必须是合法段。

#### `QTypeRevision::fromMinorVersion(Minor minorVersion)`

创建只知道 minor 的 revision，major 保持未知。minor 必须是合法段。

#### `QTypeRevision::zero()`

返回完整的 `0.0` revision。它是有效值，适合在确实要表达零版本时使用。

#### `QTypeRevision::fromEncodedVersion(Integer value)`

从编码整数解码 revision。低字节是 minor，高字节是 major；除最低两字节外不得有其它位，整数至少 16 位且最低 16 位不能带符号位。无效段会被解码为未知，而不是被拒绝为普通 `255`。

### 状态查询

#### `bool QTypeRevision::hasMajorVersion() const`

返回 major 是否已知。未知时 `majorVersion()` 返回内部哨兵值 `255`，但该值不能当作正常 major 使用。

#### `quint8 QTypeRevision::majorVersion() const`

返回编码中的 major 字节。调用方应先用 `hasMajorVersion()` 确认它有效。

#### `bool QTypeRevision::hasMinorVersion() const`

返回 minor 是否已知。未知时 `minorVersion()` 返回内部哨兵值 `255`。

#### `quint8 QTypeRevision::minorVersion() const`

返回编码中的 minor 字节。调用方应先用 `hasMinorVersion()` 确认它有效。

#### `bool QTypeRevision::isValid() const`

只要 major 或 minor 至少有一个已知就返回 `true`。因此“有效”不等于“两段都完整”。

#### `QTypeRevision::isValidSegment(Integer segment)`

判断整数能否作为版本段。合法范围是 `0..254`；负数和 `255` 及以上都无效。

### 编码与流

#### `Integer QTypeRevision::toEncodedVersion() const`

把 minor 放进低字节、major 放进高字节，返回指定整数类型。未知段会编码为 `0xff`。通常使用 `quint16` 或更宽的无符号整数。

#### `QDataStream &operator<<(QDataStream &out, const QTypeRevision &revision)`

把 revision 写入 Qt 数据流。该非成员运算符自 Qt 6.0 提供；跨版本或跨语言使用时必须明确数据流协议。

#### `QDataStream &operator>>(QDataStream &in, QTypeRevision &revision)`

从 Qt 数据流读取 revision。读取结果包括未知段状态；应检查数据流状态，不能把损坏输入当成有效 revision。

#### `qHash(const QTypeRevision &key, size_t seed = 0)`

为 revision 计算哈希值，支持 `QHash` 等哈希容器。哈希值不用于版本大小比较。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QTypeRevision()` | 创建无效 revision | major/minor 都未知，不等于 `0.0` |
| `fromVersion(major, minor)` | 创建完整 revision | 两段都必须在 `0..254` |
| `fromMajorVersion(major)` | 创建只含 major 的 revision | minor 为未知 |
| `fromMinorVersion(minor)` | 创建只含 minor 的 revision | major 为未知 |
| `zero()` | 创建 `0.0` | 是有效值，与默认构造不同 |
| `fromEncodedVersion(value)` | 从整数解码 | minor 在低字节，major 在高字节；仅允许最低两字节有位 |
| `hasMajorVersion()` | 判断 major 是否已知 | 未知时不要读取结果当作 255 |
| `majorVersion()` | 读取 major 段 | 先检查 `hasMajorVersion()` |
| `hasMinorVersion()` | 判断 minor 是否已知 | 未知时不要读取结果当作 255 |
| `minorVersion()` | 读取 minor 段 | 先检查 `hasMinorVersion()` |
| `isValid()` | 判断是否至少有一段已知 | 部分已知也返回 true |
| `isValidSegment(segment)` | 验证版本段 | 合法范围是 `0..254`，255 是未知哨兵 |
| `toEncodedVersion<Integer>()` | 编码为整数 | 未知段编码为 `0xff`；优先使用无符号整数 |
| `operator==` 等强比较运算 | 比较两个 revision | major 优先；未知的排序语义不是普通数值 255 |
| `operator<<(QDataStream &, const QTypeRevision &)` | 写入数据流 | Qt 6.0 起提供；遵守 QDataStream 协议 |
| `operator>>(QDataStream &, QTypeRevision &)` | 从数据流读取 | 检查流状态和输入可信度 |
| `qHash(const QTypeRevision &, size_t)` | 计算哈希 | 可作 `QHash` 键；没有排序含义 |
| `QMetaMethod::revision()` | 获取方法修订编码 | 非零值可用 `fromEncodedVersion()` 解码 |
| `QMetaProperty::revision()` | 获取属性修订编码 | 非零值可用 `fromEncodedVersion()` 解码 |

---

### 一句话总结

`QTypeRevision` 用两个可分别未知的 8 位段表达类型修订；记住 `255` 是未知、默认构造无效、`zero()` 才是 `0.0`，以及编码低字节为 minor。
