# Qt QSharedMemory：多进程共享同一段内存

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSharedMemory>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject`  
> 类型性质：不可复制、按系统 key 标识共享内存段

## 1. 它解决什么问题

普通堆内存只存在于创建它的进程地址空间中。即使两个进程中的指针数值恰好相同，它们通常也不指向同一块物理内存。

`QSharedMemory` 让多个进程通过同一个 `QNativeIpcKey` 创建或附加到同一段系统共享内存：

```text
进程 A                         进程 B
create(key, size)             attach(key)
       |                          |
       +---- 同一共享内存段 ------+
```

它适合：

- 主进程向工作进程共享大块二进制数据；
- 多进程共享图像帧、采样数据、缓存快照或固定状态表；
- 避免通过管道或 socket 反复复制大数据；
- 与已有 POSIX、System V 或 Win32 共享内存互操作。

它不提供：

- 数据结构序列化；
- 变长对象管理；
- 指针修复；
- 消息边界或通知机制；
- 崩溃一致性和事务；
- 自动的多读者/多写者协议。

共享内存只是字节区域。布局、版本、同步和恢复策略都必须由应用协议规定。

## 2. 什么时候不该使用

下列场景通常有更合适的工具：

- 同一进程内线程共享对象：直接共享对象并使用 `QMutex`、`QReadWriteLock` 等；
- 小型命令和事件通知：使用 local socket、管道、DBus 或其他消息 IPC；
- 需要持久化、事务和崩溃恢复：使用数据库或文件格式；
- 需要共享包含普通指针、`QString`、`QVector` 等进程内对象的内存表示：先设计显式的无指针二进制布局。

共享内存性能高，但它把很多正确性责任交给了调用方。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QSharedMemory>
```

qmake 工程使用：

```qmake
QT += core
```

是否真正提供该类取决于 Qt 构建的 `sharedmemory` 特性；`lock()` / `unlock()` 还依赖 `systemsemaphore` 特性。

## 4. 最小的创建者和使用者

### 4.1 创建者

```cpp
#include <QSharedMemory>
#include <cstring>

bool createSharedBlock(QSharedMemory &memory)
{
    const QNativeIpcKey key =
        QSharedMemory::platformSafeKey(QStringLiteral("org.example.block"));
    memory.setNativeKey(key);

    if (!memory.create(4096)) {
        qWarning() << memory.error() << memory.errorString();
        return false;
    }

    if (!memory.lock()) {
        qWarning() << memory.errorString();
        return false;
    }

    std::memset(memory.data(), 0, size_t(memory.size()));
    memory.unlock();
    return true;
}
```

`create()` 成功时已经自动 attach。不要成功后再调用一次 `attach()`。

### 4.2 使用者

接收创建者发送的 `QNativeIpcKey::toString()` 结果：

```cpp
bool attachSharedBlock(QSharedMemory &memory, const QString &serializedKey)
{
    const QNativeIpcKey key = QNativeIpcKey::fromString(serializedKey);
    if (!key.isValid()
            || !QSharedMemory::isKeyTypeSupported(key.type())) {
        return false;
    }

    memory.setNativeKey(key);
    if (!memory.attach(QSharedMemory::ReadOnly)) {
        qWarning() << memory.error() << memory.errorString();
        return false;
    }

    const auto *bytes =
        static_cast<const unsigned char *>(memory.constData());
    consumeBytes(bytes, memory.size());
    return true;
}
```

只读 attach 后必须把映射视为只读。写入该映射不是普通的 `false` 返回错误，文档明确说明会导致程序中止。

## 5. 核心状态机

```text
构造 / 设置 key
       |
       +-- create(size) 成功 --> 已创建并已附加
       |
       +-- attach() 成功 -----> 已附加
                                  |
                                  +-- data()/size()
                                  +-- lock()/unlock()
                                  |
                                  +-- detach() / 析构
                                           |
                                           v
                                        未附加
```

关键结论：

- 构造或 `setKey()` 只设置标识，不会 create 或 attach；
- `create()` 创建新段并在成功时自动 attach；
- `attach()` 只连接已经存在的段；
- `data()` 和 `size()` 只有在 attached 状态才有有效内容；
- `detach()` 后，以前取得的所有指针立即失效；
- `setKey()` / `setNativeKey()` 切换 key 时可能先 detach，但不会自动 attach 新段。

## 6. `create()` 与 `attach()`

### 6.1 `create(qsizetype size, AccessMode mode)`

```cpp
if (!memory.create(sizeof(Header) + payloadSize,
                   QSharedMemory::ReadWrite)) {
    handleError(memory.error(), memory.errorString());
}
```

它执行两个动作：

1. 用当前 key 创建 `size` 字节的共享内存段；
2. 以指定访问模式附加到刚创建的段。

成功返回 `true`，此后：

```cpp
memory.isAttached() == true
memory.data() != nullptr
memory.size() > 0
```

创建成功不代表实际 `size()` 必然等于请求值。操作系统可能把段向页大小或其他粒度取整，因此实际大小可以更大。

常见失败：

- `size <= 0` 或平台认为尺寸无效：`InvalidSize`；
- 同 key 的段已经存在：`AlreadyExists`；
- key 不合法：`KeyError`；
- 权限不足：`PermissionDenied`；
- 内存或系统表项不足：`OutOfResources`。

如果 `create()` 因 `AlreadyExists` 失败，并且协议允许复用残留或现有段，可以再 `attach()`：

```cpp
if (!memory.create(4096)) {
    if (memory.error() != QSharedMemory::AlreadyExists
            || !memory.attach()) {
        return false;
    }
}
```

这并不保证现有段具有请求的大小、布局版本或有效内容。attach 后必须验证 `size()` 和自定义 header。

### 6.2 `attach(AccessMode mode)`

```cpp
if (!memory.attach(QSharedMemory::ReadOnly)) {
    qWarning() << memory.errorString();
}
```

它只查找并映射当前 key 对应的现有段，不会在段不存在时创建它。找不到时通常得到 `NotFound`。

默认模式是 `ReadWrite`。只消费数据的进程应优先使用 `ReadOnly`，这样操作系统权限也参与约束错误写入。

### 6.3 不要忽略返回值

失败后继续调用：

```cpp
memory.data();
memory.lock();
```

不会把失败自动修好。`data()` 会返回空指针，`lock()` 可能给出 `LockError`。每一次 create、attach、lock 都应先检查返回值。

## 7. 数据指针与布局协议

### 7.1 `data()`、const `data()` 与 `constData()`

```cpp
void *data();
const void *data() const;
const void *constData() const;
```

attached 时返回整个共享段的起始地址，否则返回 `nullptr`。在下一次 `detach()` 前，返回地址本身保持不变，可以临时保存：

```cpp
auto *header = static_cast<SharedHeader *>(memory.data());
```

但地址稳定不等于内容不变。其他进程仍可以修改同一段字节，因此非原子读取需要锁或无锁协议。

`constData()` 与 const 对象上的 `data()` 都提供 const 指针。它们不会把原本以 `ReadWrite` attach 的系统映射永久改成只读，只是给当前 C++ 调用路径提供 const 访问。

### 7.2 detach 后指针失效

```cpp
const void *p = memory.constData();
memory.detach();

// 错误：p 已经指向解除映射的地址。
consume(p);
```

析构、切换 key 或显式 `detach()` 都可能结束映射。任何指针、引用、`QByteArray::fromRawData()` 视图或 `std::span` 都不得活过这一步。

### 7.3 不能直接共享进程内指针

下面的布局不适合直接放入共享内存：

```cpp
struct BadLayout {
    char *payload;
    QString name;
    QVector<int> values;
};
```

这些成员包含只在当前进程地址空间中有意义的指针或私有堆分配。另一个进程读到同样的位模式也不能安全解引用。

共享布局应使用：

- 固定宽度整数；
- 相对共享段起点的 offset；
- 固定数组或显式长度加紧随其后的字节；
- 明确的 magic、版本号、总长度和状态字段；
- 对齐和字节序约定。

```cpp
struct SharedHeader {
    quint32 magic;
    quint16 version;
    quint16 flags;
    quint32 payloadOffset;
    quint32 payloadSize;
};
```

若不同编译器、架构或语言访问同一段，还必须显式处理结构 padding、对齐、整数宽度和 endianness。

## 8. `lock()` 与 `unlock()`

### 8.1 锁保护的是访问协议

```cpp
if (!memory.lock())
    return false;

updateSharedState(memory.data(), memory.size());

if (!memory.unlock())
    return false;
```

`lock()` 使用系统信号量为该共享内存提供排他访问。若另一进程持锁，它会阻塞到对方解锁。该 API 没有超时重载，不适合在 GUI 线程中执行不可控等待。

锁不会自动包围 `data()` 的每次读写。只有所有参与者都在访问前遵守同一协议，数据才受到保护。

### 8.2 用作用域保证释放

异常、早退和新增分支很容易漏掉 `unlock()`：

```cpp
#include <QScopeGuard>

if (!memory.lock())
    return false;

const auto unlock = qScopeGuard([&memory] {
    if (!memory.unlock())
        qWarning() << memory.errorString();
});

return updateSharedState(memory.data(), memory.size());
```

`QSharedMemory` 的析构负责 detach，不应把它当作正常的 unlock 控制流。持锁时应尽快解锁，不要在临界区中等待用户输入、网络请求或子进程。

### 8.3 不要递归加锁或跨实例随意解锁

`QSharedMemory` 记录当前进程实例是否持有配套锁：

- 当前进程已经持锁时，不要再次调用 `lock()`；
- `unlock()` 只有在该进程持有锁时成功；
- 段未锁或由另一进程持锁时，`unlock()` 不做操作并返回 `false`。

将它视为非递归排他锁。调用方应让一次成功 `lock()` 对应一次 `unlock()`。

### 8.4 native key 与非 Qt 互操作的锁边界

直接通过 `setNativeKey()` 对接非 Qt 共享内存时，不能假设外部程序会自动参与 Qt 创建的配套信号量协议。Qt 官方的 native IPC 互操作说明明确指出，`QSharedMemory` 的 segment locking 对非 Qt 应用不可用。

这种场景应另行约定同步方式，例如：

- 双方共同使用同一个原生 mutex / semaphore；
- 原子序列号加 seqlock 风格协议；
- 单写者、多读者的发布协议；
- 独立 socket 通知和所有权转移。

只共享内存 native key，不会同时把 Qt 的锁协议交给另一个实现。

## 9. key：现代接口、legacy 接口和切换行为

### 9.1 推荐使用完整的 `QNativeIpcKey`

```cpp
const QNativeIpcKey key =
    QSharedMemory::platformSafeKey(QStringLiteral("org.example.frames"));

QSharedMemory memory(key);
```

`nativeIpcKey()` 同时返回原生字符串和后端类型，适合跨进程传递：

```cpp
sendToChild(memory.nativeIpcKey().toString());
```

`nativeKey()` 只返回字符串。Unix 上如果没有另行传递 type，接收方无法知道应按 POSIX 还是 System V 解释。

### 9.2 `QString` key 是 legacy 路径

```cpp
QSharedMemory memory(QStringLiteral("legacy-cache"));
```

该构造函数等价于设置 legacy key 语义。`key()` 只在使用 `setKey()` / `QString` 构造路径时返回 legacy 输入；未设置 key 或使用纯 native key 时返回 null `QString`。

新协议优先使用：

```cpp
QSharedMemory memory(QSharedMemory::platformSafeKey("cache"));
```

需要与 Qt 6.6 之前程序兼容时使用 `legacyNativeKey()` 或 legacy 构造接口。

### 9.3 切换 key 会先脱离旧段

```cpp
memory.setNativeKey(otherKey);
```

如果新 key 与当前 key 不同并且对象已 attached，Qt 会先 detach，再设置新 key。它不会自动 attach 到新段。

因此调用前必须考虑：

- 原数据指针会失效；
- 如果当前实例是最后一个 attachment，旧段可能被销毁；
- detach 失败时需要检查对象状态和错误；
- 业务线程不能仍在使用旧映射；
- 设置完成后仍需显式 `create()` 或 `attach()`。

相同 key 则直接返回，不执行 detach。

## 10. 静态 key 辅助函数

### 10.1 `platformSafeKey()`

```cpp
const QNativeIpcKey key =
    QSharedMemory::platformSafeKey(QStringLiteral("org.example.cache"));
```

将跨平台标识转换为指定后端所需的原生格式。默认 type 是 `QNativeIpcKey::DefaultTypeForOs`。

注意：

- 输入应类似合法文件名组件；
- 普通情况下不要包含 `/` 或 `\`；
- Apple 平台的可用长度很短；
- 过长 key 可能被静默截断；
- 不同 Qt 版本可能采用不同转换；
- 跨进程应发送返回结果，而不是让接收方重新转换输入。

### 10.2 `legacyNativeKey()`

生成与旧式 `QString` key 规则兼容的 native key：

```cpp
const QNativeIpcKey key =
    QSharedMemory::legacyNativeKey(QStringLiteral("old-cache"));
```

它适合和 Qt 6.6 之前的程序互操作，不是新协议的默认首选。

### 10.3 `isKeyTypeSupported()`

```cpp
if (!QSharedMemory::isKeyTypeSupported(key.type()))
    return false;
```

它只回答当前 Qt 构建及运行平台是否支持该共享内存后端。它不验证：

- key 字符串格式；
- 当前用户权限；
- 请求尺寸；
- 系统剩余资源；
- 同 key 段是否存在。

## 11. 生命周期和平台差异

### 11.1 正常析构

`~QSharedMemory()` 会清除 key，并迫使当前对象从已附加段 detach。若这是最后一个连接者，默认清理策略通常会销毁共享内存段。

QObject parent 可以决定 C++ 对象何时析构，但 `QSharedMemory` 不依赖事件循环，也不通过信号槽自动同步数据。

### 11.2 Windows

Windows 由操作系统拥有共享内存对象。最后一个 handle 关闭后，系统清理对象。正常析构或 detach 会关闭当前实例的 handle。

### 11.3 System V

Qt 以协作方式管理共享内存对象：

- 最后一个 attachment 负责移除对象；
- Qt 还会处理作为 key 的文件；
- 异常退出可能绕过负责清理的 C++ 对象，使对象或 key 文件残留。

进程重启后 `create()` 可能得到 `AlreadyExists`。只有业务协议能够验证旧段大小、版本和状态时，才应 attach 到它。

### 11.4 POSIX Realtime

POSIX shared memory 名称独立于使用它的进程存在。Qt 无法可靠知道该对象是否仍被其他使用者需要，因此清理名称时可能让新的进程无法再 attach，但已经映射的进程可继续使用现有映射。

异常退出也可能留下命名对象。不要把“最后一个 Qt 对象析构时会自动清理”当作崩溃恢复保证。

### 11.5 创建者崩溃

Unix 上负责创建和清理的进程异常退出后，段可能残留。恢复流程一般是：

1. `create()`；
2. 若为 `AlreadyExists`，判断是否允许恢复旧段；
3. `attach()`；
4. 检查实际 `size()`；
5. 锁定或按无锁协议读取 header；
6. 校验 magic、版本、状态和内容完整性；
7. 无法验证时不要把残留字节当作有效业务数据。

## 12. 线程和进程边界

### 12.1 同一对象不要并发调用

`QSharedMemory` 继承 `QObject` 且保存 attach、错误和持锁状态。不要让多个线程无保护地同时对同一个实例调用 `attach()`、`detach()`、`setNativeKey()`、`lock()` 或 `unlock()`。

可选择：

- 让一个明确线程独占 `QSharedMemory` 实例；
- 在实例外使用进程内 mutex 串行化成员调用；
- 每个线程使用自己的 `QSharedMemory` 对象 attach 到同一段。

第三种做法只让对象状态彼此独立，并不会自动保护共享段中的业务数据，仍需跨线程/跨进程同步协议。

### 12.2 锁住后也不能保存进程地址

`lock()` 解决并发访问，不解决地址空间差异。共享段内仍只能保存跨进程可解释的数据布局。

### 12.3 原子操作仍要约定内存模型

对共享段中的整数使用原子操作时，必须保证：

- 对象对齐满足原子类型要求；
- 该原子实现在目标平台上可跨进程工作；
- 所有访问者使用兼容的原子宽度和 memory order；
- 初始化和销毁协议明确。

不能因为单次整数读写在某 CPU 上看起来原子，就省略整个发布和版本协议。

## 13. 错误枚举

| 枚举值 | 值 | 含义与典型触发点 |
| --- | ---: | --- |
| `NoError` | `0` | 最近操作没有错误 |
| `PermissionDenied` | `1` | 当前用户或进程没有所需权限 |
| `InvalidSize` | `2` | `create()` 请求的尺寸无效 |
| `KeyError` | `3` | key 无效或不符合当前后端要求 |
| `AlreadyExists` | `4` | `create()` 时同 key 段已经存在 |
| `NotFound` | `5` | `attach()` 时找不到同 key 段 |
| `LockError` | `6` | 未成功 create/attach、使用 native key 的锁限制，或底层信号量失败 |
| `OutOfResources` | `7` | 内存、句柄、系统 IPC 表项等资源不足 |
| `UnknownError` | `8` | 其他未分类的系统错误 |

`error()` 是机器可分支的类别，`errorString()` 是面向人的诊断文本。失败后应立即读取，不要把旧错误长期缓存为当前对象状态。

## 14. 常见错误

### 14.1 `create()` 成功后又调用 `attach()`

`create()` 已经创建并附加。重复 attach 不是初始化所需步骤。

### 14.2 `AlreadyExists` 后直接相信旧段

旧段可能由正常运行的其他实例创建，也可能是崩溃残留；其尺寸、布局版本和数据状态都要验证。

### 14.3 把本进程对象直接 `memcpy` 到共享内存

包含指针、Qt 隐式共享对象、虚函数表或私有堆分配的数据不能被另一个进程直接解释。

### 14.4 保存 `data()` 指针后切换 key

`setKey()` / `setNativeKey()` 可能 detach，旧指针随即失效。

### 14.5 以为 `constData()` 会阻止其他进程写

它只返回 const C++ 指针。映射权限由 `attach(ReadOnly)` 决定，其他进程是否可写取决于它们自己的映射和系统权限。

### 14.6 在 `ReadOnly` 映射上强制写入

通过 `const_cast` 或保存错误类型的指针写入只读映射会导致程序中止，不是可恢复的 Qt 错误。

### 14.7 漏掉 `unlock()`

早退、异常和错误分支可能让其他进程永久等待。使用作用域 guard，并缩短临界区。

### 14.8 在 GUI 线程调用 `lock()`

它没有 timeout；另一个进程卡住或崩溃处理异常时，界面可能长期无响应。

### 14.9 认为非 Qt 程序会参与 Qt 的锁

共享 native memory 可以互操作，但 Qt 的配套 segment lock 不能自动扩展到非 Qt 实现。同步协议必须另行约定。

### 14.10 只传递 `nativeKey()`，遗漏 type

Unix 上相同字符串在 POSIX 与 System V 后端中含义不同。Qt 进程间优先传递 `nativeIpcKey().toString()`。

## 15. 逐项 API 说明

### 15.1 枚举

| API | 语义 | 关键边界 |
| --- | --- | --- |
| `AccessMode::ReadOnly` | 以只读权限 attach 或创建后映射 | 写入会导致程序中止 |
| `AccessMode::ReadWrite` | 允许读取和写入 | 不等于自动同步并发访问 |
| `SharedMemoryError` | 对最近失败进行分类 | 与操作返回值一起判断 |

### 15.2 构造和析构

| API | 语义 | 关键边界 |
| --- | --- | --- |
| `QSharedMemory(QObject *parent = nullptr)` | 创建未设置 key、未附加的对象 | 先 `setNativeKey()`，再 create/attach |
| `QSharedMemory(const QNativeIpcKey &key, QObject *parent = nullptr)` | 保存完整 native key | 不自动 create 或 attach |
| `QSharedMemory(const QString &key, QObject *parent = nullptr)` | 保存 legacy key | 新协议优先使用 `QNativeIpcKey` |
| `~QSharedMemory()` | 清除 key 并从已附加段 detach | 最后连接者可能触发段清理；崩溃时不保证执行 |
| 复制构造和复制赋值 | 由 `Q_DISABLE_COPY` 禁止 | 每个实例独立管理其系统 attachment |

### 15.3 创建、附加和脱离

| API | 语义 | 关键边界 |
| --- | --- | --- |
| `bool create(qsizetype size, AccessMode mode = ReadWrite)` | 创建指定大小的新段并自动 attach | 已存在时返回 false，不会改为 attach；实际大小可能更大 |
| `bool attach(AccessMode mode = ReadWrite)` | attach 到现有段 | 不创建；失败后检查 `error()` |
| `bool isAttached() const` | 查询当前进程实例是否已附加 | 不表示其他进程是否 attached |
| `bool detach()` | 解除当前映射 | 旧指针失效；最后连接者可能销毁段；未附加或锁冲突时可能失败 |

### 15.4 数据和尺寸

| API | 语义 | 关键边界 |
| --- | --- | --- |
| `void *data()` | 返回可写起始地址 | 未附加返回 `nullptr`；ReadOnly 映射不得写 |
| `const void *data() const` | const 对象上的只读视图 | 指针只保证到 detach 前地址不变 |
| `const void *constData() const` | 返回只读起始地址 | 不会阻止其他进程修改内容 |
| `qsizetype size() const` | 返回已附加段的实际大小 | 未附加返回 0；可能大于 create 请求值 |

### 15.5 锁和错误

| API | 语义 | 关键边界 |
| --- | --- | --- |
| `bool lock()` | 阻塞取得 Qt 配套的跨进程排他锁 | 无 timeout；非递归；native 非 Qt 互操作不能依赖该协议 |
| `bool unlock()` | 释放当前进程持有的锁 | 未持有或由其他进程持有时返回 false |
| `SharedMemoryError error() const` | 返回最近错误类别 | 失败操作后及时读取 |
| `QString errorString() const` | 返回最近错误说明 | 用于日志和用户诊断，不作为稳定协议 |

### 15.6 key 查询和设置

| API | 语义 | 关键边界 |
| --- | --- | --- |
| `void setKey(const QString &key)` | 设置 legacy key | key 改变时先 detach；不自动 attach |
| `QString key() const` | 返回 legacy 输入 key | 使用纯 native key 时返回 null |
| `void setNativeKey(const QNativeIpcKey &key)` | 设置完整 native key | Qt 6.6 起；改变时先 detach |
| `void setNativeKey(const QString &key, Type type = legacyDefaultTypeForOs())` | 设置 native 字符串和类型 | 默认参数走 legacy 类型；必须确保 type 匹配 |
| `QString nativeKey() const` | 返回原生字符串 | 不包含后端类型 |
| `QNativeIpcKey nativeIpcKey() const` | 返回完整 native key | Qt 6.6 起；跨 Qt 进程传递时优先使用 |

### 15.7 静态辅助

| API | 语义 | 关键边界 |
| --- | --- | --- |
| `static bool isKeyTypeSupported(Type type)` | 查询当前共享内存实现是否支持后端 | 不检查 key、权限或系统资源 |
| `static QNativeIpcKey platformSafeKey(const QString &key, Type type = DefaultTypeForOs)` | 生成现代跨平台 native key | 输入过长可能静默截断；传递生成结果 |
| `static QNativeIpcKey legacyNativeKey(const QString &key, Type type = legacyDefaultTypeForOs())` | 生成旧规则兼容 key | 仅用于 legacy 互操作 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 创建 | `create(size, mode)` | 新建并自动附加共享段 | `AlreadyExists` 不会自动 attach |
| 连接 | `attach(mode)` | 连接现有共享段 | `ReadOnly` 映射绝不能写 |
| 状态 | `isAttached()` | 查询本实例是否已附加 | 不是系统全局查询 |
| 数据 | `data()` / `constData()` | 获取共享字节起始地址 | 只在 detach 前有效 |
| 大小 | `size()` | 获取实际映射大小 | 未附加为 0，可能大于请求值 |
| 同步 | `lock()` / `unlock()` | Qt 进程间排他访问 | 无超时、非递归、保证释放 |
| 脱离 | `detach()` | 解除映射 | 所有旧指针立即失效 |
| 错误 | `error()` / `errorString()` | 诊断最近失败 | 先检查操作返回值 |
| key | `setNativeKey()` / `nativeIpcKey()` | 设置或获取完整系统 key | 改 key 会先 detach，不会自动重连 |
| legacy | `setKey()` / `key()` | 使用旧式跨平台 key | 新协议不优先使用 |
| 平台 | `isKeyTypeSupported()` | 检查共享内存后端可用性 | 支持不代表本次操作成功 |
| 生成 | `platformSafeKey()` | 生成现代平台 key | 跨进程发送返回值 |
| 兼容 | `legacyNativeKey()` | 生成旧 Qt 兼容 key | 明确用于兼容场景 |

## 17. 一句话总结

`QSharedMemory` 负责让多个进程映射同一段字节：一个参与者 `create()` 并自动 attach，其他参与者 `attach()`；所有指针只活到 detach，所有数据布局和同步都必须由协议定义，Qt 的 `lock()` 只在参与者共同遵守其配套锁规则时才真正保护共享数据。
