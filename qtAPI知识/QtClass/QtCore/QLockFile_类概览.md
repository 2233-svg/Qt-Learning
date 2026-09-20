# Qt QLockFile 文件锁与并发资源保护深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QLockFile>`  
> 所属模块：`Qt6::Core`  
> 类型性质：基于锁文件的进程间互斥对象  
> 相关类型：`QString`、`qint64`、`std::chrono::milliseconds`

## 1. 它解决什么问题

`QLockFile` 用一个文件名作为所有协作者都能看到的“占用标记”，让多个进程在访问同一个外部资源前先竞争这个标记。竞争成功的进程进入临界区，其他进程等待、放弃或提示用户。

它适合保护：

- 多个程序共同读写的配置文件、索引文件或缓存数据库；
- 只能由一个进程使用的 socket、端口或本地服务；
- 文件映射的共享内存区域；
- 编辑器中“同一文档只能由一个实例写入”的长时间占用；
- 一次性保存、迁移或检查操作。

它真正提供的是**协作式互斥协议**，不是对资源本身施加的魔法锁：

- 所有访问同一资源的进程都必须使用 `QLockFile`；
- 所有进程必须使用完全相同的锁文件路径；
- `QLockFile` 不会自动阻止一个不遵守协议的程序直接打开或修改资源；
- 它不会替你完成数据读写、事务提交、崩溃恢复或文件内容合并。

例如，保护 `settings.ini` 时通常建立一个旁车锁文件：

```cpp
QLockFile lockFile(QStringLiteral("/data/app/settings.ini.lock"));
```

不要把真实数据文件本身直接作为 `QLockFile` 的 `fileName`。`QLockFile` 会尝试创建这个路径；如果该路径已经是实际存在的数据文件，锁竞争就会把“数据文件存在”误判为“锁被占用”。

## 2. 实际使用场景

### 2.1 短时间保存配置

保存前只需要很短时间的互斥时，可以让 `lock()` 等待已有操作结束：

```cpp
#include <QLockFile>
#include <QString>

bool saveSettings(const QString &settingsPath)
{
    QLockFile lockFile(settingsPath + QStringLiteral(".lock"));

    if (!lockFile.lock())
        return false;

    // 只有拿到锁后才读取、修改和替换 settingsPath。
    // 离开函数时，lockFile 析构并释放锁。
    return writeSettingsFile(settingsPath);
}
```

这种模式适合临界区明确且预计很快完成的工作。若文件写入可能持续数十秒甚至数分钟，应重新估算陈旧锁时间，否则其他进程可能把仍在工作的锁误判为崩溃遗留。

### 2.2 编辑器打开文档的长时间占用

用户打开一个文档后，锁可能要持续到编辑器关闭。此时不应该让界面无限等待，也不应该自动删除一个可能仍由其他编辑器持有的锁：

```cpp
#include <QLockFile>
#include <QString>
#include <chrono>

bool openDocument(const QString &documentPath)
{
    QLockFile lockFile(documentPath + QStringLiteral(".lock"));
    lockFile.setStaleLockTime(std::chrono::milliseconds::zero());

    if (lockFile.tryLock(std::chrono::milliseconds{100}))
        return true;

    if (lockFile.error() == QLockFile::LockFailedError) {
        // 可以调用 getLockInfo()，向用户说明文档可能正在被谁使用。
        showDocumentLockedMessage();
    }
    return false;
}
```

这里的 `QLockFile` 必须活到文档关闭。实际代码通常把它作为文档控制器或文档会话对象的成员，而不是像上例一样在函数结束时销毁。

### 2.3 用户确认后处理遗留锁

长生命周期场景中，用户可以在确认“持有者已经退出或确实要强制打开”后再删除锁：

```cpp
QLockFile lockFile(documentPath + QStringLiteral(".lock"));
lockFile.setStaleLockTime(0);

if (!lockFile.tryLock(std::chrono::milliseconds{100})) {
    if (lockFile.error() == QLockFile::LockFailedError) {
        qint64 pid = 0;
        QString hostname;
        QString appname;

        if (lockFile.getLockInfo(&pid, &hostname, &appname)) {
            showOwner(pid, hostname, appname);
        }

        if (userConfirmedForceOpen()) {
            if (lockFile.removeStaleLockFile())
                lockFile.tryLock(std::chrono::milliseconds{100});
        }
    }
}
```

`removeStaleLockFile()` 是一个明确的强制操作，不应因为第一次 `tryLock()` 失败就无条件调用。

### 2.4 保护共享内存或本地服务

如果共享对象本身没有提供足够高层的互斥协议，可以约定一个稳定的锁文件路径：

```cpp
QLockFile lockFile(QStringLiteral("/var/run/my-service/cache.lock"));

if (!lockFile.tryLock(std::chrono::milliseconds{50})) {
    // 资源忙，立即返回或排队，不阻塞当前线程。
    return;
}

updateSharedCache();
lockFile.unlock();
```

锁文件只保护“愿意遵守这套约定”的访问者。对于不可信进程或恶意删除锁文件的环境，还需要权限控制、文件系统安全策略和更适合的 IPC/数据库事务机制。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QLockFile>
#include <QString>
#include <chrono>
```

只使用整型毫秒重载时可以不显式包含 `<chrono>`；使用 `std::chrono::milliseconds` 时应让包含关系清晰，不要依赖其他头文件的间接包含。

## 4. 最小可用流程

一个完整的锁使用流程通常是：

1. 为受保护资源构造稳定、专用的锁文件路径；
2. 根据临界区时长选择 `lock()` 或有限等待的 `tryLock()`；
3. 失败时读取 `error()`，区分“被占用”和“无法创建锁文件”；
4. 成功后执行所有需要互斥的操作；
5. 在离开临界区前调用 `unlock()`，并依靠析构函数作为最后一道释放保障。

```cpp
#include <QLockFile>
#include <QString>

bool updateIndex(const QString &indexPath)
{
    QLockFile lockFile(indexPath + QStringLiteral(".lock"));

    if (!lockFile.tryLock(5000)) {
        switch (lockFile.error()) {
        case QLockFile::LockFailedError:
            reportBusy(indexPath);
            break;
        case QLockFile::PermissionError:
            reportPermissionProblem(lockFile.fileName());
            break;
        case QLockFile::UnknownError:
            reportUnknownLockError(lockFile.fileName());
            break;
        case QLockFile::NoError:
            // 正常情况下 tryLock() 返回 false 时不会走到这里。
            break;
        }
        return false;
    }

    rebuildIndex(indexPath);
    lockFile.unlock();
    return true;
}
```

## 5. 先掌握几条核心语义

### 5.1 构造对象不会立即创建锁文件

```cpp
QLockFile lockFile(lockPath);
```

这一步只保存路径并建立“未持有锁”的对象状态。真正尝试创建锁文件的是 `lock()` 或 `tryLock()`。

因此，构造成功不代表资源已经被保护；必须检查加锁函数的返回值。

### 5.2 `fileName` 是锁文件路径，不是被保护资源的抽象句柄

`QLockFile` 不知道“资源”是什么。它只知道一个路径，并把这个路径作为跨进程协调点。下面两段代码只有在路径约定一致时才互相协调：

```cpp
QLockFile first(QStringLiteral("/tmp/report.lock"));
QLockFile second(QStringLiteral("/tmp/report.lock"));
```

如果另一个进程使用了相对路径、符号链接路径或不同的文件名，即使它认为自己保护的是同一资源，也可能没有形成同一把锁。应用应在协议层规定锁路径如何生成。

### 5.3 锁的所有者是当前 `QLockFile` 实例

`isLocked()` 查询的是“这个对象是否成功拿到锁”，不是“这个路径当前是否存在锁文件”。对象销毁、移动到其他抽象层或用另一个对象代替后，都不要把它们混为同一状态。

`QLockFile` 使用 `Q_DISABLE_COPY`，不能复制构造或复制赋值。它也没有可用的公共移动接口。通常应让一个明确的会话对象独占它，并通过指针或引用传递使用权，而不是把它按值传来传去。

### 5.4 所有访问者必须遵守同一协议

下面的代码只能约束也调用 `QLockFile` 的访问者：

```cpp
QLockFile lockFile(resourcePath + QStringLiteral(".lock"));
if (lockFile.lock()) {
    modifyResource(resourcePath);
}
```

另一个程序若直接调用 `QFile::open()`、数据库 API 或平台原生 API 修改 `resourcePath`，`QLockFile` 不会收到通知，也不会自动阻止它。

### 5.5 `lock()` 是可能无限阻塞的调用

`lock()` 会等待其他进程或线程释放锁。等待期间调用线程会被阻塞：

- 工作线程可以在确定等待时间合理时使用；
- GUI 主线程不应对长生命周期资源调用无限等待的 `lock()`；
- 用户可见的打开、导入、同步操作通常更适合有限等待的 `tryLock()`；
- 如果等待本身就是业务要求，要把阻塞时间和取消策略设计清楚。

### 5.6 同一个实例不能递归加锁

在同一个线程中对已经持有锁的同一个 `QLockFile` 再次调用 `lock()`，文档明确指出会死锁；再次调用 `tryLock()` 则会失败。

```cpp
QLockFile lockFile(lockPath);
lockFile.lock();

// 错误：同一实例尚未 unlock()，这里不能再次加锁。
lockFile.tryLock(std::chrono::milliseconds::zero());
```

需要可重入临界区时，应重新设计调用层次，或使用专门的进程内递归互斥工具。不要把 `QLockFile` 当作递归锁。

## 6. 短操作和长占用要使用不同策略

### 6.1 短操作：允许自动清理陈旧锁

默认 `staleLockTime()` 为 `30000` 毫秒，也就是 30 秒。`lock()` 和 `tryLock()` 会使用这个时间判断旧锁文件是否可能是崩溃后遗留的锁。

适合短操作的例子：

```cpp
QLockFile lockFile(cachePath + QStringLiteral(".lock"));

if (!lockFile.lock())
    return false;

refreshCache(cachePath);
return true;
```

如果持锁工作通常不会超过 30 秒，默认值可以作为合理起点。但“默认值”不是对所有业务都安全的保证，磁盘、网络文件系统、数据量和机器负载都可能拉长临界区。

### 6.2 长占用：关闭自动陈旧判断，使用短超时

文档推荐长时间保护资源时设置：

```cpp
lockFile.setStaleLockTime(0);
```

这样做的意图是：只要持有者没有显式释放，Qt 就不要仅凭锁文件年龄自动删除它。然后使用短超时 `tryLock()`，让应用有机会向用户解释资源正在被占用。

```cpp
lockFile.setStaleLockTime(std::chrono::milliseconds::zero());

if (!lockFile.tryLock(std::chrono::milliseconds{100})) {
    if (lockFile.error() == QLockFile::LockFailedError)
        showLockedResourceDialog();
}
```

这里的 `0` 不是“立即把锁判定为陈旧”，而是关闭基于年龄的自动陈旧锁处理。之后是否强制清理，必须由用户确认或由业务的恢复策略决定。

### 6.3 持锁时间超过默认值时提高阈值

短操作也可能因为保存大文件、网络盘延迟或迁移数据库而超过 30 秒：

```cpp
lockFile.setStaleLockTime(std::chrono::minutes{3});
```

如果项目最低 Qt 版本不支持其他 `std::chrono` 单位到毫秒的隐式转换，可以明确写成：

```cpp
lockFile.setStaleLockTime(
    std::chrono::duration_cast<std::chrono::milliseconds>(
        std::chrono::minutes{3}));
```

阈值应覆盖“正常最慢一次操作”的时间，并留出余量；阈值过大又会让真实崩溃留下的锁等待更久。

## 7. 陈旧锁是如何判断的

锁文件不只表示“文件存在”，Qt 还会写入与持有者有关的信息，用来辅助判断遗留锁。公开文档描述的主要判断依据包括：

- 锁文件中记录的进程 ID 是否仍对应运行中的进程；
- 当前进程名是否与锁记录对应，避免 PID 已被其他程序复用；
- 锁文件最后修改时间是否超过 `staleLockTime()`；
- 平台和文件系统能否可靠地取得这些信息。

因此，陈旧锁判断不是绝对可靠的分布式租约，也不能证明某个进程一定已经失去对资源的所有权。特别是网络文件系统、时钟异常、PID 复用和平台差异都可能影响判断。

Qt 文档还指出：在 Windows 上，如果机器名包含 US-ASCII 之外的字符，检测陈旧锁存在平台限制。需要跨平台可靠工作的产品不能只依赖“自动清理陈旧锁”，还要设计用户可理解的恢复流程。

## 8. 错误状态与控制流

`error()` 描述最近一次 `lock()` 或 `tryLock()` 的锁操作结果。它不是异常，也不是一个可替代返回值检查的全局健康状态。

### 8.1 `NoError`

表示锁成功取得。对 `tryLock()` 来说，返回值为 `true` 时应进入临界区，并在结束后释放锁。

### 8.2 `LockFailedError`

表示因为另一个进程或线程持有锁，当前尝试没有成功。

这是“资源当前忙”的业务状态，不一定是程序错误。短操作可以等待或稍后重试；长生命周期场景通常应向用户显示持有者信息。

### 8.3 `PermissionError`

表示无法在锁文件的父目录中创建锁文件，常见原因包括：

- 目录没有写权限；
- 文件系统是只读的；
- 沙箱或平台权限阻止创建；
- 锁文件路径的父目录不存在或不可访问。

这和“资源被其他进程占用”不同，不应通过删除锁文件来处理。

### 8.4 `UnknownError`

表示发生了其他错误，例如分区已满、写入锁文件内容失败或底层文件系统返回了无法归类的错误。应记录路径和上下文，并把它作为实际 I/O 故障处理。

## 9. 逐项 API 说明

### 9.1 `enum QLockFile::LockError`

```cpp
enum LockError {
    NoError = 0,
    LockFailedError = 1,
    PermissionError = 2,
    UnknownError = 3
};
```

**作用：** 表示最近一次 `lock()` 或 `tryLock()` 的结果。

**边界：**

- `LockFailedError` 表示已有持有者，不等于目录权限错误；
- `PermissionError` 表示锁文件无法创建，不等于资源繁忙；
- `UnknownError` 需要按底层 I/O 故障排查；
- 判断是否拿到锁时优先看 `lock()`/`tryLock()` 的返回值，再用 `error()` 分类失败原因；
- 不要把枚举值持久化为跨版本协议，业务只应依赖枚举名称和语义。

### 9.2 `explicit QLockFile::QLockFile(const QString &fileName)`

```cpp
explicit QLockFile(const QString &fileName);
```

**作用：** 创建一个处于未加锁状态的锁对象，并记录锁文件路径。

**关键语义：**

- 构造函数不会创建文件，也不会检查当前是否存在锁；
- `fileName` 应是专门的锁文件路径；
- 当后续调用 `lock()` 或 `tryLock()` 时，Qt 才尝试创建该文件；
- 多个进程必须使用完全一致的路径才能形成同一把锁；
- 类不可复制，建议让它与被保护资源的生命周期保持一致。

### 9.3 `QLockFile::~QLockFile()`

```cpp
~QLockFile();
```

**作用：** 销毁对象；如果该实例持有锁，析构时会删除锁文件并释放锁。

**关键语义：**

- 它提供 RAII 释放保障；
- 析构函数不会撤销其他实例持有的锁；
- 不要让锁对象在真正的资源操作完成前离开作用域；
- 如果进程在析构前崩溃，正常的释放路径不会执行，后续调用者可能需要陈旧锁恢复流程。

### 9.4 `QString QLockFile::fileName() const`

```cpp
QString fileName() const;
```

**作用：** 返回该对象使用的锁文件路径。

**关键语义：**

- 返回的是锁文件名，不是被保护资源的文件名；
- 可用于错误日志、权限错误提示和诊断；
- 它不会告诉你该路径是否存在，也不会检查锁是否已经被当前对象持有；
- `fileName()` 相同只是形成协作的必要条件，访问者仍需使用 `QLockFile`。

### 9.5 `bool QLockFile::lock()`

```cpp
bool lock();
```

**作用：** 尝试取得锁；如果其他进程或线程已经创建锁文件，会一直等待直到锁可用。

**返回值：**

- `true`：当前实例取得锁；
- `false`：由于不可恢复错误无法取得，例如父目录没有权限。

**关键语义：**

- 这是可能无限阻塞的调用；
- 成功后必须调用 `unlock()`，也可以依赖析构函数作为最终释放；
- 同一个线程对同一个实例递归调用会死锁；
- 失败后用 `error()` 区分权限、占用和未知错误；
- 需要有限等待时使用 `tryLock()`，不要自行用循环调用 `lock()` 模拟超时。

### 9.6 `bool QLockFile::tryLock(int timeout)`

```cpp
bool tryLock(int timeout);
```

**作用：** 尝试取得锁，最多等待 `timeout` 毫秒。

**关键语义：**

- 当前 Qt 6.11 API 中该重载的参数单位是毫秒；
- `timeout == 0` 表示立即尝试，不等待；
- 文档明确规定负数等价于 `lock()`，会无限等待；
- 成功后仍必须 `unlock()`；
- 同一个实例已经持锁时，再次调用会失败，不会递归成功；
- 失败后立即读取 `error()`，必要时再调用 `getLockInfo()`。

示例：

```cpp
if (lockFile.tryLock(250)) {
    updateResource();
    lockFile.unlock();
} else if (lockFile.error() == QLockFile::LockFailedError) {
    retryLater();
}
```

### 9.7 `bool QLockFile::tryLock(std::chrono::milliseconds timeout = std::chrono::milliseconds::zero())`

```cpp
bool tryLock(
    std::chrono::milliseconds timeout =
        std::chrono::milliseconds::zero());
```

**作用：** 使用类型安全的毫秒时长尝试取得锁。该重载自 Qt 6.2 提供。

**关键语义：**

- 默认参数是 `0ms`，因此不传参数时执行立即尝试；
- 返回值和失败分类与整型重载相同；
- 使用 `std::chrono` 可以避免把秒、毫秒和微秒混淆；
- 需要表达“无限等待”时优先调用 `lock()`，不要让调用者猜测负时长的意图；
- 如果项目还要兼容 Qt 6.1 或更低版本，不能直接依赖该重载。

```cpp
using namespace std::chrono_literals;

if (!lockFile.tryLock(200ms)) {
    const QLockFile::LockError reason = lockFile.error();
    handleLockFailure(reason);
}
```

### 9.8 `void QLockFile::unlock()`

```cpp
void unlock();
```

**作用：** 释放当前实例持有的锁，通常表现为删除锁文件。

**关键语义：**

- 没有持有锁时调用不会产生作用；
- 应在临界区结束后尽快调用，不要把无关耗时工作放在锁内；
- `unlock()` 只释放当前实例成功取得的锁；
- 依赖析构函数释放时，要确认对象的生命周期覆盖整个临界区；
- 解锁后不要继续假设资源仍受保护。

### 9.9 `void QLockFile::setStaleLockTime(int staleLockTime)`

```cpp
void setStaleLockTime(int staleLockTime);
```

**作用：** 以毫秒设置锁文件被视为陈旧的时间间隔。

**关键语义：**

- 默认值是 `30000` 毫秒，也就是 30 秒；
- `lock()` 和 `tryLock()` 会使用它判断旧锁是否可能来自崩溃进程；
- 短操作可以保留默认值，也可以按正常最长耗时增加；
- 长时间持有资源时通常设为 `0`，关闭基于年龄的自动陈旧判断；
- 它只影响陈旧锁判断，不会给当前锁设置自动过期时间；
- 它不会在到期瞬间主动删除当前仍在使用的锁。

### 9.10 `void QLockFile::setStaleLockTime(std::chrono::milliseconds staleLockTime)`

```cpp
void setStaleLockTime(std::chrono::milliseconds staleLockTime);
```

**作用：** 以 `std::chrono::milliseconds` 设置陈旧锁时间。该重载自 Qt 6.2 提供。

**关键语义：**

- 语义等价于整型毫秒重载；
- `std::chrono::milliseconds::zero()` 等价于设置 `0`；
- 该值用于后续 `lock()`/`tryLock()` 的陈旧判断；
- 它不替代长生命周期场景中的用户确认和强制恢复策略。

```cpp
lockFile.setStaleLockTime(std::chrono::seconds{90});
```

如果传入的时长不能直接转换为 `milliseconds`，应显式使用 `duration_cast`，让精度损失成为代码中可见的决定。

### 9.11 `int QLockFile::staleLockTime() const`

```cpp
int staleLockTime() const;
```

**作用：** 返回陈旧锁判断使用的毫秒数。

**关键语义：**

- 默认返回 `30000`；
- 返回 `0` 表示关闭基于年龄的自动陈旧判断；
- 返回值是配置策略，不是当前锁文件的年龄；
- 不要用它推断锁还剩多少有效时间，`QLockFile` 没有租约续期语义。

### 9.12 `std::chrono::milliseconds QLockFile::staleLockTimeAsDuration() const`

```cpp
std::chrono::milliseconds staleLockTimeAsDuration() const;
```

**作用：** 以 `std::chrono::milliseconds` 返回陈旧锁时间。该函数自 Qt 6.2 提供。

**关键语义：**

- 与 `staleLockTime()` 表达同一配置；
- 适合直接与 `std::chrono` 时长比较或传给其他时间 API；
- 返回的是设置值，不是锁文件的实际修改时间；
- 如果需要兼容 Qt 6.1 或更低版本，应使用整型 API。

### 9.13 `bool QLockFile::isLocked() const`

```cpp
bool isLocked() const;
```

**作用：** 判断当前 `QLockFile` 实例是否已经成功取得锁。

**关键语义：**

- `true` 只表示这个实例曾成功取得并仍记录为持有；
- 它不是对任意同路径锁文件的全局查询；
- 它不能代替 `tryLock()` 的竞争操作；
- 它不能保证被保护资源的内容没有被不遵守协议的程序修改；
- 需要在业务开始前取得锁时，仍应检查 `lock()` 或 `tryLock()` 返回值。

### 9.14 `bool QLockFile::getLockInfo(qint64 *pid, QString *hostname, QString *appname) const`

```cpp
bool getLockInfo(
    qint64 *pid,
    QString *hostname,
    QString *appname) const;
```

**作用：** 读取锁文件中记录的当前持有者信息。

**输出信息：**

- `pid`：持有者进程 ID；
- `hostname`：持有者所在主机名，对网络文件系统尤其有帮助；
- `appname`：创建锁的应用名称。

**推荐调用条件：**

```cpp
if (!lockFile.tryLock(100)
        && lockFile.error() == QLockFile::LockFailedError) {
    qint64 pid = 0;
    QString hostname;
    QString appname;

    if (lockFile.getLockInfo(&pid, &hostname, &appname))
        showLockOwner(pid, hostname, appname);
}
```

**关键边界：**

- 它主要用于 `tryLock()` 失败且错误为 `LockFailedError` 的场景；
- 锁文件可能在 `tryLock()` 失败后、读取信息前被删除，因此返回 `false` 不一定是新的严重错误；
- 读取失败时应重新尝试 `tryLock()`，不要继续使用过期的持有者信息；
- 输出参数可以按需传入空指针，以忽略不需要的字段；
- 这些信息用于提示和诊断，不能单独作为强制删除锁的充分依据。

### 9.15 `bool QLockFile::removeStaleLockFile()`

```cpp
bool removeStaleLockFile();
```

**作用：** 强制尝试删除已有的锁文件。

**推荐条件：**

1. 这是长时间保护资源的场景；
2. 已经调用 `setStaleLockTime(0)`；
3. `tryLock()` 返回 `false` 且 `error()` 为 `LockFailedError`；
4. 已向用户显示持有者信息或执行了明确的恢复策略；
5. 用户或可信业务逻辑同意强制处理。

**关键边界：**

- 不推荐把它用于短操作，因为短操作的陈旧锁通常由 `lock()`/`tryLock()` 自动处理；
- 当前实例已经持有锁时调用它是错误流程，会失败；
- 在 Windows 上，如果持有锁的应用仍在运行，删除可能失败；
- 返回 `true` 只表示删除操作成功，不表示当前实例已经取得新锁；
- 删除成功后仍必须重新调用 `tryLock()`，并再次检查返回值。

```cpp
if (lockFile.removeStaleLockFile()) {
    if (!lockFile.tryLock(std::chrono::milliseconds{100}))
        reportLockRace();
}
```

两个进程可能同时观察到“看起来可以清理”的锁，因此删除后重新竞争是必需的。

### 9.16 `QLockFile::LockError QLockFile::error() const`

```cpp
QLockFile::LockError error() const;
```

**作用：** 返回最近一次 `lock()` 或 `tryLock()` 的错误状态。

**关键语义：**

- 只在加锁操作失败后读取最有意义；
- 应与返回值结合使用，而不是只看 `error()`；
- `LockFailedError` 通常进入“资源忙”分支；
- `PermissionError` 和 `UnknownError` 应进入“环境或 I/O 故障”分支；
- 如果随后又调用了新的加锁操作，旧错误状态就不应继续代表新操作。

## 10. 状态机与生命周期

可以把一个实例的主要状态简化为：

```text
构造
  |
  v
未持有锁 --lock()/tryLock() 成功--> 持有锁
   ^                                  |
   |                                  |
   +---------- unlock()/析构 ----------+
```

失败分支不会进入“持有锁”状态：

```text
未持有锁 --tryLock() 失败--> 读取 error()
       |
       +--> LockFailedError --> getLockInfo()/提示/重试
       |
       +--> PermissionError 或 UnknownError --> 处理环境故障
```

几个生命周期结论：

- 构造对象不加锁；
- 成功加锁后，锁的有效期至少覆盖当前实例存活并保持持有状态的时间；
- `unlock()` 结束当前实例的持锁状态；
- 析构函数会作为最后的释放路径；
- 进程崩溃可能留下锁文件，需要陈旧锁判断或显式恢复；
- 任何需要共享资源保护的操作都必须位于成功加锁与解锁之间。

## 11. 线程、进程与文件系统边界

### 11.1 它主要是进程间协议，不是进程内互斥的首选

如果所有竞争者都在同一个进程内，优先考虑：

- `QMutex`；
- `QRecursiveMutex`；
- `QReadWriteLock`；
- `std::mutex` 或其他标准库同步工具。

`QLockFile` 更适合必须跨进程协调的资源。把它用于大量高频的进程内短临界区，通常会引入不必要的文件系统开销。

### 11.2 不要无保护地跨线程共享一个实例

`QLockFile` 没有把“多个线程同时调用同一个对象的所有成员”作为业务级同步方案。应让负责资源会话的线程独占实例，或者在外层用明确的线程同步保护调用顺序。

特别要避免：

- 一个线程调用 `lock()`，另一个线程调用同一实例的 `unlock()`；
- 一个线程持锁时，另一个线程复用该实例再次竞争；
- 用同一实例的 `isLocked()` 结果作为其他线程的授权凭据。

若不同线程各自构造对象并使用同一锁路径，它们可以通过文件协议竞争，但更应确认这是不是有意设计，而不是偶然共享。

### 11.3 路径所在目录必须可创建、可写、可协作

创建锁文件不仅需要路径字符串，还需要：

- 父目录存在；
- 当前用户有创建文件的权限；
- 文件系统允许排他创建；
- 网络文件系统对原子创建、删除和修改时间的语义足够可靠；
- 所有参与者看到的是同一个文件系统命名空间。

目录不可写时，应该修复路径或权限，而不是调用 `removeStaleLockFile()`。

### 11.4 网络文件系统不是无条件等价于本地磁盘

锁文件依赖文件创建、读取、修改时间、进程和主机信息。网络文件系统可能有缓存、延迟和主机视图差异。对跨主机共享的关键数据，必须验证目标文件系统的锁语义，必要时选择数据库、服务端租约或专用分布式协调服务。

## 12. 常见错误与排查顺序

### 12.1 把资源路径直接传给 `QLockFile`

**症状：** 资源已经存在时总是得到 `LockFailedError`。

**原因：** `QLockFile` 认为这个已存在路径就是锁文件。

**修复：** 规定独立的旁车锁路径，例如 `resourcePath + ".lock"`，并让所有访问者一致使用。

### 12.2 加锁失败后无条件删除文件

**症状：** 两个正常运行的编辑器互相破坏对方的锁。

**原因：** 把暂时占用当成崩溃遗留，并在没有用户确认的情况下调用 `removeStaleLockFile()`。

**修复：** 先检查 `error()`，长占用场景读取 `getLockInfo()`，确认后才执行强制恢复。

### 12.3 对长生命周期资源使用默认陈旧时间

**症状：** 程序仍在保存或编辑时，另一个进程认为锁已过期。

**原因：** 默认 30 秒只适合短操作的起点，不是长期占用的通用值。

**修复：** 长占用使用 `setStaleLockTime(0)`；预计可能较慢但仍是短操作时增加阈值。

### 12.4 在 GUI 线程调用无限等待的 `lock()`

**症状：** 窗口无响应，用户无法取消。

**原因：** `lock()` 会等待到资源释放，没有超时。

**修复：** 使用短超时 `tryLock()`，显示占用提示或转移到专门的工作线程。

### 12.5 把 `isLocked()` 当成全局查询

**症状：** 新建的另一个 `QLockFile` 对象返回未持锁，于是代码错误地认为路径没有锁。

**原因：** `isLocked()` 查询的是当前实例，不是路径的全局状态。

**修复：** 用 `tryLock()` 进行真正的竞争。

### 12.6 读到锁信息后不重新竞争

**症状：** 显示的 PID 或主机名已经过时，随后仍然直接打开资源。

**原因：** `getLockInfo()` 是诊断接口，不会替你取得锁。

**修复：** 诊断后仍调用 `tryLock()`，只有成功后才进入临界区。

### 12.7 持锁期间执行无关的慢操作

**症状：** 其他进程长时间等待，锁文件频繁被认为异常。

**原因：** 临界区包含网络请求、用户交互、等待子进程或不必要的计算。

**修复：** 在锁外准备数据，在锁内只做必须串行化的检查和提交；不能把需要用户点击的流程放在锁内。

### 12.8 认为析构函数能处理所有异常

**症状：** 进程崩溃后仍然存在锁文件。

**原因：** 崩溃不会执行正常的 C++ 析构路径。

**修复：** 为短操作配置合理的陈旧判断，为长操作提供明确的用户恢复和诊断流程。

## 13. 推荐的设计模板

### 13.1 短事务型资源更新

```cpp
bool updateFile(const QString &resourcePath)
{
    QLockFile lockFile(resourcePath + QStringLiteral(".lock"));
    lockFile.setStaleLockTime(std::chrono::seconds{60});

    if (!lockFile.tryLock(std::chrono::seconds{5})) {
        switch (lockFile.error()) {
        case QLockFile::LockFailedError:
            return false; // 可以由上层稍后重试
        case QLockFile::PermissionError:
        case QLockFile::UnknownError:
        case QLockFile::NoError:
            return false;
        }
    }

    const bool ok = readModifyAndCommit(resourcePath);
    lockFile.unlock();
    return ok;
}
```

这里的锁对象在函数内创建，适合临界区完全包含在函数中的短事务。

### 13.2 长生命周期文档会话

```cpp
class DocumentSession
{
public:
    explicit DocumentSession(const QString &documentPath)
        : m_lock(documentPath + QStringLiteral(".lock"))
    {
        m_lock.setStaleLockTime(0);
    }

    bool acquire()
    {
        return m_lock.tryLock(std::chrono::milliseconds{100});
    }

    bool locked() const
    {
        return m_lock.isLocked();
    }

    void release()
    {
        m_lock.unlock();
    }

    QLockFile &lockFile()
    {
        return m_lock;
    }

private:
    QLockFile m_lock;
};
```

真正的产品代码还应在 `acquire()` 失败后读取 `error()`，必要时通过 `lockFile()` 获取持有者信息，并把强制删除放到明确的用户确认分支。

## API 速查表

### 14.1 类型与生命周期

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `enum QLockFile::LockError` | 表示最近一次加锁操作的结果 | 先看 `lock()`/`tryLock()` 返回值，再用枚举分类失败 |
| `QLockFile(const QString &fileName)` | 创建未持锁的锁对象 | 不创建文件；路径必须是专用锁文件路径 |
| `~QLockFile()` | 销毁对象并在必要时释放锁 | 进程崩溃时不会执行正常析构 |
| `QLockFile` 的复制操作 | 由 `Q_DISABLE_COPY` 禁止 | 不要按值复制或把锁所有权隐式传递 |

### 14.2 加锁与解锁

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `bool lock()` | 无限等待直到取得锁或发生不可恢复错误 | 可能阻塞很久；同一实例递归调用会死锁 |
| `bool tryLock(int timeout)` | 最多等待指定毫秒数 | 负数等价于 `lock()`；`0` 表示立即尝试 |
| `bool tryLock(std::chrono::milliseconds timeout = std::chrono::milliseconds::zero())` | 使用类型安全的毫秒时长尝试加锁 | Qt 6.2 起；默认 `0ms`；同一实例不可递归加锁 |
| `void unlock()` | 释放当前实例持有的锁 | 未持锁时无操作；释放后必须重新竞争才能进入临界区 |
| `bool isLocked() const` | 查询当前实例是否持锁 | 不是同路径全局状态查询 |

### 14.3 路径、错误和持有者信息

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `QString fileName() const` | 返回锁文件路径 | 不返回受保护资源路径，也不代表文件当前存在 |
| `QLockFile::LockError error() const` | 返回最近一次 `lock()`/`tryLock()` 的结果 | 新的加锁操作会改变它；和返回值配合使用 |
| `bool getLockInfo(qint64 *, QString *, QString *) const` | 读取 PID、主机名和应用名 | 适合 `LockFailedError` 后诊断；锁可能在读取前消失 |
| `bool removeStaleLockFile()` | 强制尝试删除现有锁文件 | 长占用、`staleLockTime(0)`、用户确认后使用；删除后还要重新 `tryLock()` |

### 14.4 陈旧锁策略

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `void setStaleLockTime(int staleLockTime)` | 以毫秒设置陈旧判断阈值 | 默认 `30000`；`0` 关闭基于年龄的自动判断 |
| `void setStaleLockTime(std::chrono::milliseconds staleLockTime)` | 使用 chrono 时长设置阈值 | Qt 6.2 起；不代表锁的自动租约过期时间 |
| `int staleLockTime() const` | 读取毫秒阈值 | 返回策略配置，不是锁文件实际年龄 |
| `std::chrono::milliseconds staleLockTimeAsDuration() const` | 以 chrono 读取阈值 | Qt 6.2 起；与整型读取表达同一设置 |

## 15. 一句话总结

`QLockFile` 是一个基于文件路径的协作式进程间锁：短操作可以用 `lock()` 或有限等待的 `tryLock()`，长时间占用应使用 `setStaleLockTime(0)`、短超时竞争和用户可见的持有者诊断；任何成功加锁后的代码都必须在正确的生命周期内释放锁，并且所有访问者必须遵守同一锁路径协议。
