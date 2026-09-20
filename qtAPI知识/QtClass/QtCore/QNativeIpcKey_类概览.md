# Qt QNativeIpcKey：原生 IPC key 的类型化值对象

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QNativeIpcKey>`  
> 所属模块：`Qt6::Core`  
> 类型性质：可复制、可移动、可比较、可哈希的值类型  
> 主要协作类：`QSharedMemory`、`QSystemSemaphore`

## 1. 它解决什么问题

`QSharedMemory` 和 `QSystemSemaphore` 必须用一个系统范围的标识找到同一项 IPC 资源。这个标识不能只是一段字符串，因为 Unix 上可能同时存在 POSIX Realtime 与 System V 两套后端，同样的字符串在不同后端中代表完全不同的系统对象。

`QNativeIpcKey` 把两部分信息包装在一起：

```text
QNativeIpcKey
  = 原生 key 字符串
  + IPC 后端类型
```

例如：

```cpp
QNativeIpcKey key(QStringLiteral("/org.example.cache"),
                  QNativeIpcKey::Type::PosixRealtime);
```

它本身不创建共享内存或信号量，也不拥有任何操作系统资源。它只是一个可以复制、比较、序列化和跨进程传递的描述值。

## 2. 实际使用场景

### 2.1 为共享内存生成当前平台可用的 key

通常不要手写平台原生格式，而是让具体 IPC 类生成：

```cpp
const QNativeIpcKey key =
    QSharedMemory::platformSafeKey(QStringLiteral("org.example.cache"));

QSharedMemory memory(key);
```

`platformSafeKey()` 的输入是跨平台标识，返回值才是实际应使用的 native key。

### 2.2 把创建者使用的 key 传给另一个 Qt 进程

```cpp
const QString text = memory.nativeIpcKey().toString();

// 通过命令行、约定文件或其他控制通道发送 text。
const QNativeIpcKey received = QNativeIpcKey::fromString(text);
if (!received.isValid())
    return false;
```

不要只传递最初交给 `platformSafeKey()` 的输入字符串。不同 Qt 版本可能采用不同转换规则，接收方重新转换后未必得到同一个系统 key。

### 2.3 对接旧 Qt 程序

Qt 6.6 之前，Unix 上使用哪个 IPC 后端主要由 Qt 的构建选项决定。需要与旧程序互操作时，可以查询旧规则使用的类型：

```cpp
const auto legacyType = QNativeIpcKey::legacyDefaultTypeForOs();
const QNativeIpcKey key =
    QSharedMemory::legacyNativeKey(QStringLiteral("legacy-cache"),
                                   legacyType);
```

双方仍需使用兼容的 Qt 构建选项。`legacyDefaultTypeForOs()` 不是“现代平台推荐值”，而是兼容旧程序的选择。

### 2.4 对接非 Qt 程序

非 Qt 程序需要同时知道：

- `nativeKey()` 返回的原生字符串；
- `type()` 返回的后端类型；
- 对应后端的原生 API 和编码规则。

只交换字符串在 Unix 上不够，因为 POSIX Realtime 与 System V 的解释方式不同。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QNativeIpcKey>
```

qmake 工程使用：

```qmake
QT += core
```

## 4. 三种后端类型

```cpp
enum class QNativeIpcKey::Type : quint16 {
    SystemV       = 0x51,
    PosixRealtime = 0x100,
    Windows       = 0x101
};
```

| 类型 | 对应系统机制 | 典型平台与 native key 形态 |
| --- | --- | --- |
| `SystemV` | XSI / System V IPC | 多数 Unix；key 字符串是文件路径 |
| `PosixRealtime` | POSIX.1b IPC | 多数 Unix；名称通常以 `/` 开头 |
| `Windows` | Win32 kernel object | Windows；名称类似相对路径且区分大小写 |

后端枚举存在不表示当前平台一定支持它。例如 Windows 构建通常不支持 System V，Android 的可用性也有限。真正使用前应调用具体类的：

```cpp
QSharedMemory::isKeyTypeSupported(key.type());
QSystemSemaphore::isKeyTypeSupported(key.type());
```

共享内存与系统信号量对某个后端的支持能力也应通过各自的函数查询，不要用 `QNativeIpcKey::isValid()` 代替。

## 5. `DefaultTypeForOs` 与旧默认值

### 5.1 `DefaultTypeForOs`

Qt 6.11.1 中：

- Windows 上为 `Type::Windows`；
- 其他操作系统上为 `Type::PosixRealtime`。

它是编译期常量，代表 Qt 6.6 之后的默认选择：

```cpp
QNativeIpcKey key(QStringLiteral("/cache"),
                  QNativeIpcKey::DefaultTypeForOs);
```

默认类型仍可能在当前目标系统上不可用，因此必要时还要调用 `isKeyTypeSupported()`。

### 5.2 `legacyDefaultTypeForOs()`

该函数返回 Qt 6.6 之前 `QSharedMemory` 和 `QSystemSemaphore` 可能使用的后端：

- Windows 仍是 Windows 后端；
- Unix 上结果受 Qt 构建时 IPC 配置影响，许多旧构建使用 System V；
- 只有新旧程序的相关 Qt 构建选项兼容时，结果才足以保证互操作。

新代码没有兼容负担时使用 `DefaultTypeForOs` 和 `platformSafeKey()`；只有明确对接旧程序时才使用 legacy 规则。

## 6. `isEmpty()`、`isValid()` 和“可使用”是三件事

这是本类最重要的边界。

### 6.1 `isEmpty()`

只检查 `nativeKey()` 字符串是否为空：

```cpp
QNativeIpcKey key;
Q_ASSERT(key.isEmpty());
```

它不检查类型，也不检查平台支持能力。

### 6.2 `isValid()`

只检查对象是否包含 Qt 认识的有效 key type。解析失败时，`fromString()` 返回无效对象。

```cpp
const QNativeIpcKey parsed =
    QNativeIpcKey::fromString(QStringLiteral("not-a-key"));

if (!parsed.isValid())
    qWarning() << "cannot parse IPC key";
```

默认构造对象的类型是 `DefaultTypeForOs`，所以它虽然 key 字符串为空，仍然是“类型有效”的：

```cpp
QNativeIpcKey key;
Q_ASSERT(key.isValid());
Q_ASSERT(key.isEmpty());
```

### 6.3 真正可用于创建 IPC 对象

即使：

```cpp
key.isValid() && !key.isEmpty()
```

也不代表操作一定成功。还可能存在：

- 当前平台不支持该后端；
- native key 格式不符合后端规则；
- key 太长并被转换函数截断；
- 权限、沙箱或系统资源限制；
- 对应资源已经存在或不存在。

最终结果必须由 `QSharedMemory` 或 `QSystemSemaphore` 的操作返回值和错误状态判断。

## 7. native key 的平台格式

### 7.1 POSIX Realtime

POSIX 名称通常要求第一个字符是 `/`，后续不应再包含 `/`：

```text
/myapp
/org.example.myapp
```

Apple 平台的长度限制尤其严格，包含开头 `/` 和结尾空字符后，通常只剩 30 个可用字节。非 ASCII 字符按 UTF-8 编码后可能占多个字节。

`platformSafeKey()` 会添加开头的 `/`，并在 Apple 平台按可用长度截断。

### 7.2 Windows

Windows key 是 kernel object name：

- 最长通常为 `MAX_PATH`，即 260 个字符；
- 看起来像相对路径，不以反斜杠或盘符开头；
- 名称区分大小写；
- `QSharedMemory::platformSafeKey()` 与 `QSystemSemaphore::platformSafeKey()` 会添加不同前缀，避免两类资源重名。

### 7.3 System V

System V 的 native key 字符串是文件路径：

- 路径受普通文件路径规则限制；
- 应使用绝对路径，避免不同进程当前目录不同；
- Qt 在创建 IPC 对象时可创建对应 key 文件；
- 与旧 Qt `QSharedMemory` 互操作时，不要借用已有重要文件作为 key 文件，因为旧实现可能删除它。

`platformSafeKey()` 对相对输入添加应用通常可写的目录；绝对输入通常保持为绝对路径。

### 7.4 跨平台标识的约束

传给 `platformSafeKey()` 的标识应接近一个安全的文件名组件，例如：

```text
myapp
org.example.myapp
org.example.myapp-12345
```

通常不要包含 `/` 或 `\`。Apple 沙箱是例外，其 key 必须遵循应用组标识加自定义标识的专用格式。

Qt 可能静默截断过长的输入。应用必须自己限制长度并避免两个长 key 截断成同一个结果。

## 8. 稳定的字符串表示

`toString()` 生成适合保存或发送给其他 Qt 进程的稳定表示：

```text
<type>:<percent-encoded-payload>
```

当前标准类型使用的前缀为：

| 类型 | 前缀 |
| --- | --- |
| `PosixRealtime` | `posix` |
| `SystemV` | `systemv` |
| `Windows` | `windows` |

payload 使用百分号编码，解码结果与当前类型的 `nativeKey()` 相同。

推荐始终按 round-trip API 使用，不要自己拼接或拆解：

```cpp
const QString encoded = key.toString();
const QNativeIpcKey decoded = QNativeIpcKey::fromString(encoded);

if (!decoded.isValid() || decoded != key)
    return false;
```

字符串格式设计为向前、向后兼容，但有两个限制：

- 老 Qt 无法解析它发布后新增的 key 类型；
- 解析成功只表示格式和类型可识别，不表示当前平台支持创建该后端对象。

无效对象调用 `toString()` 返回 null `QString`。

## 9. 值语义、比较与哈希

`QNativeIpcKey` 是普通值类型：

```cpp
QNativeIpcKey first(QStringLiteral("/cache"),
                    QNativeIpcKey::Type::PosixRealtime);
QNativeIpcKey copy = first;

Q_ASSERT(copy == first);
```

复制不会创建第二个 IPC 系统对象，也不会 attach 到共享内存；只是复制 key 描述。

`operator==` / `operator!=` 比较对象内容。类型不同或 native key 不同的对象不是同一个 key：

```cpp
QNativeIpcKey posix(QStringLiteral("/cache"),
                    QNativeIpcKey::Type::PosixRealtime);
QNativeIpcKey systemV(QStringLiteral("/cache"),
                      QNativeIpcKey::Type::SystemV);

Q_ASSERT(posix != systemV);
```

`qHash()` 与相等比较配套，可以用作 `QHash` 或 `QSet` 的 key：

```cpp
QHash<QNativeIpcKey, QString> owners;
owners.insert(posix, QStringLiteral("worker"));
```

不要只对 `nativeKey()` 做哈希或比较而丢掉 `type()`，否则不同后端可能被错误地合并。

## 10. 生命周期和线程边界

`QNativeIpcKey`：

- 不继承 `QObject`；
- 不需要事件循环；
- 不拥有底层共享内存、信号量或 key 文件；
- 析构只销毁这个值对象；
- 可复制、可移动，可作为返回值和容器元素。

不同线程使用彼此独立的副本没有共享状态问题。多个线程同时读写同一个实例仍属于普通 C++ 数据竞争，调用方必须同步；它不是并发可变配置对象。

把 key 传给 `QSharedMemory` 或 `QSystemSemaphore` 后，修改原来的 `QNativeIpcKey` 不会自动重设已经构造好的 IPC 对象：

```cpp
QNativeIpcKey key = QSharedMemory::platformSafeKey("cache");
QSharedMemory memory(key);

key.setNativeKey(QStringLiteral("/other"));
// memory 仍保存构造时取得的 key。
```

## 11. 常见错误

### 11.1 把 `isValid()` 当作完整校验

`isValid()` 只验证 type，不验证字符串格式、平台支持、权限或资源状态。创建前检查后端支持，创建失败后读取具体 IPC 类的错误。

### 11.2 默认构造后只检查 `isValid()`

默认对象通常 `isValid() == true`，但 `isEmpty() == true`。要作为资源标识使用，还必须设置非空 native key。

### 11.3 跨进程只发送 `nativeKey()`

Unix 上接收方还需要知道它是 POSIX 还是 System V。Qt 进程之间优先发送 `toString()` 结果。

### 11.4 跨进程重新调用 `platformSafeKey()`

不同 Qt 版本可能改变转换规则。由创建者发送已经生成的 `QNativeIpcKey` 字符串表示。

### 11.5 无条件使用 `DefaultTypeForOs`

它是默认选择，不是支持能力证明。目标平台或 Qt 构建可能不支持该类型。

### 11.6 用 legacy 默认值开发新协议

legacy API 用于兼容旧 Qt。新协议应明确使用现代默认值或显式约定后端。

### 11.7 忽略 key 长度和字符限制

`platformSafeKey()` 可能静默截断。跨平台协议应主动限制标识长度，并避免路径分隔符和平台非法字符。

## 12. 逐项 API 说明

### 12.1 类型和默认值

| API | 语义 | 关键边界 |
| --- | --- | --- |
| `enum class Type` | 选择 System V、POSIX Realtime 或 Windows 后端 | 枚举存在不等于平台支持 |
| `Type::SystemV` | 使用 XSI / System V IPC | native key 是文件路径；通常用于 Unix |
| `Type::PosixRealtime` | 使用 POSIX.1b IPC | 名称格式和长度受平台限制 |
| `Type::Windows` | 使用 Win32 kernel objects | 通常只在 Windows 可用，名称区分大小写 |
| `static constexpr Type DefaultTypeForOs` | Qt 6.6 后当前 OS 的默认类型 | Windows 为 Windows，其他系统为 POSIX；仍需检查支持 |
| `static Type legacyDefaultTypeForOs()` | 返回 Qt 6.6 以前可能使用的默认后端 | 只用于旧程序兼容，并依赖兼容的 Qt 构建选项 |

### 12.2 构造、复制和析构

| API | 语义 | 关键边界 |
| --- | --- | --- |
| `QNativeIpcKey()` | 创建默认类型、空字符串的 key | 对象通常有效但为空 |
| `explicit QNativeIpcKey(Type type)` | 创建指定类型、空字符串的 key | type 有效不代表 key 可使用 |
| `QNativeIpcKey(const QString &key, Type type = DefaultTypeForOs)` | 保存 native key 和类型 | 不校验字符串，不创建 IPC 对象 |
| `QNativeIpcKey(const QNativeIpcKey &other)` | 复制完整 key 值 | 不 attach，不复制系统资源 |
| `QNativeIpcKey(QNativeIpcKey &&other)` | 移入完整 key 值 | moved-from 对象只应析构或重新赋值 |
| `operator=(const QNativeIpcKey &other)` | 复制赋值 | 覆盖当前 key 描述，不影响已使用旧值的 IPC 对象 |
| `operator=(QNativeIpcKey &&other)` | 移动赋值 | 通过值语义转移内容 |
| `~QNativeIpcKey()` | 销毁值对象 | 不删除共享内存、信号量或系统 key 文件 |

### 12.3 内容查询与修改

| API | 语义 | 关键边界 |
| --- | --- | --- |
| `bool isEmpty() const` | 判断 `nativeKey()` 是否为空 | 不检查 type 或平台支持 |
| `bool isValid() const` | 判断 key type 是否有效 | 不检查字符串是否符合 OS 规则 |
| `QString nativeKey() const` | 返回原生 key 字符串 | 单独传递时可能丢失后端类型 |
| `void setNativeKey(const QString &newKey)` | 替换原生字符串 | 不校验，也不操作现有 IPC 资源 |
| `Type type() const` | 返回后端类型 | 使用前可交给 `isKeyTypeSupported()` |
| `void setType(Type type)` | 替换后端类型 | 原字符串不会自动转换成新后端格式 |

`setType()` 尤其需要谨慎：

```cpp
QNativeIpcKey key(QStringLiteral("/cache"),
                  QNativeIpcKey::Type::PosixRealtime);
key.setType(QNativeIpcKey::Type::SystemV);
```

此时 `"/cache"` 被解释为 System V 文件路径，Qt 不会替你执行 `platformSafeKey()` 的转换。

### 12.4 序列化

| API | 语义 | 关键边界 |
| --- | --- | --- |
| `QString toString() const` | 生成包含类型和百分号编码 payload 的稳定字符串 | 无效对象返回 null 字符串 |
| `static QNativeIpcKey fromString(const QString &text)` | 解析 `toString()` 格式 | 失败返回无效对象；成功不代表后端可用 |

### 12.5 交换、比较和哈希

| API | 语义 | 关键边界 |
| --- | --- | --- |
| `void swap(QNativeIpcKey &other)` | 交换两个对象的全部内容 | 很快、`noexcept`，不操作 IPC 资源 |
| `swap(value1, value2)` | 非成员交换函数 | 与成员 `swap()` 语义相同 |
| `operator==` / `operator!=` | 比较两个 key 的内容 | 后端类型也是身份的一部分 |
| `qHash(const QNativeIpcKey &key, size_t seed = 0)` | 计算与相等语义一致的哈希 | 使用调用方提供的 seed；适合 `QHash` / `QSet` |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `Type` | 指定 IPC 后端 | System V、POSIX、Windows 不是同一个命名空间 |
| 默认 | `DefaultTypeForOs` | 取得现代默认后端 | 默认不等于当前构建一定支持 |
| 兼容 | `legacyDefaultTypeForOs()` | 取得 Qt 6.6 前的默认后端 | 仅用于兼容旧程序 |
| 构造 | `QNativeIpcKey()` | 创建空 key | 有效与非空是两个条件 |
| 构造 | `QNativeIpcKey(key, type)` | 包装原生 key 和后端 | 不校验，不创建资源 |
| 状态 | `isEmpty()` | 检查 native 字符串是否为空 | 不检查类型 |
| 状态 | `isValid()` | 检查类型是否可识别 | 不检查平台支持和字符串合法性 |
| 内容 | `nativeKey()` / `setNativeKey()` | 读写原生字符串 | 修改不会自动重连 IPC 对象 |
| 类型 | `type()` / `setType()` | 读写后端类型 | 改类型不会转换原字符串 |
| 传递 | `toString()` / `fromString()` | 跨 Qt 进程传递完整 key | 解析后仍检查平台支持 |
| 比较 | `==` / `!=` | 比较完整 key 内容 | 不要只比较字符串 |
| 容器 | `qHash()` | 支持哈希容器 | 哈希语义包含完整 key |
| 交换 | `swap()` | 快速交换两个 key | 不接触系统资源 |

## 14. 一句话总结

`QNativeIpcKey` 只负责准确表达“哪个后端中的哪个原生 key”：`isEmpty()` 看字符串，`isValid()` 看类型，真正能否创建资源则必须由 `QSharedMemory` 或 `QSystemSemaphore` 的平台支持检查和操作结果决定。
