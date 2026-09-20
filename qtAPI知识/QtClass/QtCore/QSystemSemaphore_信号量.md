# Qt QSystemSemaphore：跨进程共享的系统信号量

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSystemSemaphore>`  
> 所属模块：`Qt6::Core`  
> 类型性质：不可复制、按系统 key 访问的跨进程计数信号量

## 1. 它解决什么问题

`QSystemSemaphore` 是 `QSemaphore` 的系统级版本。它通过系统范围的 key 标识底层信号量，因此多个线程、多个 Qt 进程，甚至非 Qt 程序，都可以在约定 key 和 key 类型后访问同一组许可。

```cpp
const QNativeIpcKey key =
    QSystemSemaphore::platformSafeKey(QStringLiteral("app-resource"));

QSystemSemaphore semaphore(key, 3, QSystemSemaphore::Create);
if (!semaphore.acquire()) {
    qWarning() << semaphore.errorString();
}
```

它适合：

- 多进程共同限制某类系统资源；
- 进程之间进行简单的许可协调；
- 与共享内存、文件映射或其他 IPC 资源配套；
- 需要接入已有 POSIX、System V 或 Win32 信号量。

如果只需要同一进程内的线程同步，优先使用更轻量的 `QSemaphore`。系统信号量涉及平台对象、key、权限和跨进程生命周期，复杂度和成本都更高。

## 2. key 决定“大家是不是同一个信号量”

系统信号量不是按 C++ 对象地址识别的，而是按 `QNativeIpcKey` 识别：

```text
进程 A: key X -> acquire/release
进程 B: key X -> 访问同一个系统信号量
进程 C: key Y -> 访问另一个系统信号量
```

Qt 6.6 起推荐用 `platformSafeKey()` 从跨平台标识生成 key：

```cpp
QNativeIpcKey key =
    QSystemSemaphore::platformSafeKey(QStringLiteral("cache-slots"));
```

跨进程通信时，不要只把 `platformSafeKey()` 的输入字符串传给另一个进程。不同 Qt 版本可能使用不同转换，应该传递生成后的 `QNativeIpcKey` 字符串表示，或直接传递 native key 和类型。

## 3. `Open` 与 `Create`

### 3.1 `Open`

`Open` 表示打开已有对象；如果对象不存在，则创建并使用 `initialValue` 初始化。Unix 上如果对象因进程崩溃残留，`Open` 不会强制重置已有资源计数。

### 3.2 `Create`

`Create` 表示当前进程承担创建/接管语义，并要求资源计数按 `initialValue` 设置。Unix 上这可以处理“旧对象只是上一个进程崩溃残留”的场景。

Windows 的系统 semaphore 不能以同样方式因进程崩溃残留，文档指出 `Open` 与 `Create` 在 Windows 上行为基本相同，已有对象的初始值不会被重新设置。

因此常见协议是：

```text
第一个已知负责初始化的进程：Create
之后附加的进程：Open
```

不要让多个普通参与者都使用 `Create` 并期待它们各自独立初始化同一个计数器；初始化策略必须由进程协议决定。

## 4. 构造函数

```cpp
QNativeIpcKey key =
    QSystemSemaphore::platformSafeKey(QStringLiteral("jobs"), QNativeIpcKey::DefaultTypeForOs);

QSystemSemaphore semaphore(key, 4, QSystemSemaphore::Create);
```

也可以使用旧式 `QString` key：

```cpp
QSystemSemaphore semaphore(QStringLiteral("legacy-jobs"), 4,
                           QSystemSemaphore::Create);
```

`QString` 构造使用 legacy key 语义。需要明确 key 类型、跨版本或跨非 Qt 程序互操作时，使用 `QNativeIpcKey` 更清楚。

构造后应立即检查 `error()`。构造函数没有返回布尔成功值，key 无效、权限不足、资源不足等问题要通过错误状态诊断。

## 5. `acquire()` 与 `release()`

### 5.1 `acquire()`

```cpp
if (!semaphore.acquire()) {
    qWarning() << semaphore.error() << semaphore.errorString();
    return false;
}
```

每次 `acquire()` 只取得一个许可。如果当前没有可用许可，会阻塞到同 key 的另一个线程或进程释放许可。

它没有超时重载。需要超时的跨进程协议不能简单把它当作 `QSemaphore::tryAcquire()` 使用，应重新设计握手、使用其他 IPC 原语，或让等待发生在可控的辅助线程。

### 5.2 `release(int n)`

```cpp
if (!semaphore.release(2)) {
    qWarning() << semaphore.errorString();
}
```

释放 `n` 个许可，成功返回 `true`，系统错误返回 `false`。与 `QSemaphore` 一样，释放也可以人为增加系统信号量的资源数，但正常资源协议应让 acquire/release 数量匹配。

## 6. 错误处理

```cpp
if (!semaphore.acquire()) {
    switch (semaphore.error()) {
    case QSystemSemaphore::PermissionDenied:
        qWarning() << "permission denied";
        break;
    case QSystemSemaphore::KeyError:
        qWarning() << "invalid key";
        break;
    default:
        qWarning() << semaphore.errorString();
        break;
    }
}
```

错误枚举包括：

- `NoError`；
- `PermissionDenied`；
- `KeyError`；
- `AlreadyExists`；
- `NotFound`；
- `OutOfResources`；
- `UnknownError`。

`error()` 返回最近一次操作的错误分类，`errorString()` 返回面向人的文字说明。错误状态应在失败操作后及时读取，不要把它当作跨线程共享的稳定日志对象。

## 7. key 查询与切换

```cpp
QString legacy = semaphore.key();
QNativeIpcKey native = semaphore.nativeIpcKey();
```

- `key()` 返回 legacy key；
- `nativeIpcKey()` 返回完整的 `QNativeIpcKey`，包含 native key 和 key type。

切换 key：

```cpp
semaphore.setNativeKey(otherKey, 3, QSystemSemaphore::Open);
```

`setKey()` / `setNativeKey()` 会重建当前 `QSystemSemaphore` 对象。新 key 不同于旧 key 时，效果相当于先释放旧对象关联，再请求新对象；不要在仍有业务线程使用旧 key 时随意切换。

## 8. 跨进程传递 key

Qt 进程之间可以用：

```cpp
QString serialized = semaphore.nativeIpcKey().toString();
QNativeIpcKey key = QNativeIpcKey::fromString(serialized);
```

解析后仍应检查 key 是否有效，并用 `isKeyTypeSupported()` 确认当前平台支持该类型。能够解析字符串不代表当前系统一定能创建相应 IPC 对象。

如果对接非 Qt 程序，还必须约定 key 类型。Unix 上 POSIX realtime 和 System V 是不同后端，只有 native key 字符串而没有类型时，可能无法正确互操作。

## 9. 析构和系统对象生命周期

`QSystemSemaphore` 对象析构不一定立即删除底层系统信号量；底层对象通常在该系统信号量的最后一个实例消失时才移除，具体受平台影响。

更重要的是，析构不会替你修复遗漏的 acquire/release：

- Windows 上，如果当前实例 acquire 后没有 release，析构不会自动 release，进程正常退出也不一定归还资源，可能让其他进程永久等待；
- Unix 上，进程退出时系统可能自动释放已取得资源，但不能把平台差异当作业务保障。

因此每次成功 acquire 后都应建立明确的 release 路径，跨进程资源最好使用协议和 watchdog 处理异常退出。

## 10. 静态 key 辅助函数

### 10.1 `platformSafeKey()`

```cpp
QNativeIpcKey key =
    QSystemSemaphore::platformSafeKey(QStringLiteral("shared-jobs"));
```

从跨平台标识生成适合当前平台的 native key。默认使用 `QNativeIpcKey::DefaultTypeForOs`，也可以显式指定类型。

### 10.2 `legacyNativeKey()`

```cpp
QNativeIpcKey legacy =
    QSystemSemaphore::legacyNativeKey(QStringLiteral("old-key"));
```

生成 legacy key 规则使用的 native key，适合与 Qt 6.6 之前的程序保持兼容。互操作时还要保证双方构建选项和 key 类型协议一致。

### 10.3 `isKeyTypeSupported()`

```cpp
if (!QSystemSemaphore::isKeyTypeSupported(QNativeIpcKey::Type::SystemV)) {
    qWarning() << "backend is unavailable";
}
```

它只判断当前 Qt 平台实现是否支持该 key 类型，不代表某次创建一定成功；权限、key 内容、系统资源和沙箱限制仍可能导致失败。

## 11. 常见错误

### 11.1 只传输入字符串，不传生成后的 key

跨版本 Qt 可能对输入做不同变换。应传递 `QNativeIpcKey::toString()` 的结果，或传递 native key 与类型。

### 11.2 把 `Open` 当成“强制初始化”

Unix 上打开崩溃残留对象时，`Open` 会保留已有计数；需要重置时由协议确定哪个进程使用 `Create`。

### 11.3 只检查构造是否完成

构造函数没有布尔返回。创建失败或 key 错误要检查 `error()` 和 `errorString()`。

### 11.4 以为 acquire 有超时

`QSystemSemaphore::acquire()` 没有 timeout 参数。无限等待必须放在可接受阻塞的执行环境中。

### 11.5 不匹配 release 数量

释放过少会造成许可泄漏，释放过多会人为增加资源数量，跨进程后更难排查。

### 11.6 在仍被使用时切换 key

`setKey()` / `setNativeKey()` 会重建对象。先停止旧 key 的使用者，再切换。

## 12. 逐项 API 语义

### 枚举

| API | 值 | 语义 |
| --- | ---: | --- |
| `Open` | `0` | 打开已有系统信号量；不存在时创建；Unix 残留对象的计数通常不重置。 |
| `Create` | `1` | 创建/接管并按 `initialValue` 初始化；Unix 上用于处理崩溃残留。 |
| `NoError` | `0` | 最近一次操作没有错误。 |
| `PermissionDenied` | `1` | 权限不足。 |
| `KeyError` | `2` | key 无效。 |
| `AlreadyExists` | `3` | 指定 key 的对象已存在，操作无法按请求创建。 |
| `NotFound` | `4` | 指定 key 的对象不存在。 |
| `OutOfResources` | `5` | 系统资源不足。 |
| `UnknownError` | `6` | 其他未分类系统错误。 |

### 构造与重建

| API | 语义 | 边界 |
| --- | --- | --- |
| `QSystemSemaphore(const QNativeIpcKey &key, int initialValue = 0, AccessMode mode = Open)` | 请求 native key 对应的系统信号量。 | 构造后检查错误；不可复制。 |
| `QSystemSemaphore(const QString &key, int initialValue = 0, AccessMode mode = Open)` | 请求 legacy key 对应的系统信号量。 | 适合旧式兼容场景。 |
| `~QSystemSemaphore()` | 释放当前进程实例。 | 不保证自动归还遗漏许可；底层对象删除受平台和实例数影响。 |
| `setNativeKey(key, initialValue, mode)` | 按 native key 重建对象。 | 可能脱离旧 key；先停止旧使用者。 |
| `setKey(key, initialValue, mode)` | 按 legacy key 重建对象。 | 与构造函数使用同样的 mode 规则。 |

### 许可和错误

| API | 语义 | 边界 |
| --- | --- | --- |
| `bool acquire()` | 阻塞并取得一个许可。 | 没有超时重载；失败后检查 error。 |
| `bool release(int n = 1)` | 释放 `n` 个许可。 | 可能创建额外资源；返回系统操作是否成功。 |
| `SystemSemaphoreError error() const` | 返回最近一次错误分类。 | 失败后及时读取。 |
| `QString errorString() const` | 返回最近一次错误的文字说明。 | 面向诊断，不是稳定机器协议。 |

### key 查询和静态辅助

| API | 语义 | 边界 |
| --- | --- | --- |
| `QString key() const` | 返回 legacy key。 | 不能表达完整 native key 类型。 |
| `QNativeIpcKey nativeIpcKey() const` | 返回完整 native key。 | 跨进程传递时优先使用。 |
| `static bool isKeyTypeSupported(QNativeIpcKey::Type type)` | 判断平台是否支持 key backend。 | 不保证创建时权限和资源条件满足。 |
| `static QNativeIpcKey platformSafeKey(const QString &key, QNativeIpcKey::Type type = DefaultTypeForOs)` | 生成当前平台适用的 key。 | 跨进程应传递生成结果，不要只传输入。 |
| `static QNativeIpcKey legacyNativeKey(const QString &key, QNativeIpcKey::Type type = legacyDefaultTypeForOs())` | 生成 legacy 兼容 native key。 | 用于旧程序互操作时明确约定类型。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 创建 | `QSystemSemaphore(key, initialValue, mode)` | 连接或创建系统信号量。 | key、mode、初始化责任必须由进程协议规定。 |
| 取得 | `acquire()` | 阻塞取得一个跨进程许可。 | 没有超时版本。 |
| 释放 | `release(n)` | 释放一个或多个许可。 | 必须和实际 acquire 数量匹配。 |
| 诊断 | `error()` / `errorString()` | 查询最近一次系统错误。 | 构造和失败操作后及时检查。 |
| 重建 | `setKey()` / `setNativeKey()` | 切换到另一个系统信号量。 | 会重建对象，先停用旧 key。 |
| 查询 | `key()` / `nativeIpcKey()` | 获取 legacy 或完整 key。 | 跨进程优先传递 native key。 |
| 平台 | `isKeyTypeSupported()` | 检查 backend 是否支持。 | 支持不等于当前创建必然成功。 |
| 生成 | `platformSafeKey()` | 从跨平台标识生成 key。 | 传递生成后的 key，不是输入字符串。 |
| 兼容 | `legacyNativeKey()` | 生成旧规则 native key。 | 与旧 Qt 程序互操作时使用。 |

---

### 一句话总结

`QSystemSemaphore` 是按系统 key 共享的跨进程信号量：先解决 key 和初始化责任，再处理 acquire/release，最后用错误 API 和平台规则诊断失败。
