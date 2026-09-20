# Qt QNtfsPermissionCheckGuard：作用域内启用 Windows NTFS ACL 检查

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.6  
> 头文件：`#include <QNtfsPermissionCheckGuard>`  
> 所属模块：`Qt6::Core`  
> 平台：仅 Windows  
> 类型性质：不可复制、不可移动的 RAII guard

## 1. 它解决什么问题

Windows 的 NTFS 权限由访问控制列表 ACL 表达。完整查询文件所有者和 ACL 比只读取文件属性更昂贵，因此 Qt 默认不会让 `QFile`、`QFileInfo` 及相关类型执行完整 NTFS 权限检查。

关闭完整检查时，一些结果只是快速近似：

- `QFileInfo::isReadable()` 主要反映条目是否存在；
- `QFileInfo::isWritable()` 主要反映 Read Only 属性；
- `permission()` / `permissions()` 可能不准确；
- `owner()` 等所有者查询可能返回空结果。

`QNtfsPermissionCheckGuard` 在自己的生命周期内启用完整 NTFS ownership 和 permission 检查：

```cpp
void inspectFile(const QString &path)
{
    QNtfsPermissionCheckGuard guard;

    QFileInfo info(path);
    qDebug() << info.owner();
    qDebug() << info.permissions();
}
```

离开作用域时 guard 自动撤销自己对应的一次启用。

它不是某个文件的权限句柄，也不会修改 ACL。它控制的是 Qt 文件 API 是否执行更深入的 Windows 权限查询。

## 2. 实际使用场景

### 2.1 显示准确的权限和所有者信息

文件属性页、部署检查工具和诊断程序可能需要展示：

- 当前文件所有者；
- 当前用户是否可读、可写或可执行；
- `QFileDevice::Permissions` 对应的权限标志。

```cpp
FileSecurityInfo inspectSecurity(const QString &path)
{
    QNtfsPermissionCheckGuard guard;
    const QFileInfo info(path);

    return {
        info.owner(),
        info.isReadable(),
        info.isWritable(),
        info.permissions()
    };
}
```

### 2.2 在执行操作前提供更准确的预检提示

```cpp
bool canProbablyReplace(const QString &path)
{
    QNtfsPermissionCheckGuard guard;
    return QFileInfo(path).isWritable();
}
```

这只能改善提示或决策，不能替代真正的文件操作。权限可能在检查后发生变化，网络共享和 Windows 安全策略也可能让最终 `QFile::open()` 失败。

正确模式仍是：

```cpp
QFile file(path);
if (!file.open(QIODevice::WriteOnly)) {
    reportOpenError(file.errorString());
    return false;
}
```

### 2.3 限定昂贵检查的范围

完整 ACL 查询有性能成本，应只覆盖真正需要它的代码：

```cpp
void FileInspector::refreshSecurityPage()
{
    QNtfsPermissionCheckGuard guard;
    refreshOwner();
    refreshPermissionFlags();
}

void FileInspector::refreshSizeAndTimestamps()
{
    // 不需要完整 ACL 时，不创建 guard。
}
```

不要在应用整个生命周期都保持 guard，除非产品确实要求每次 Qt 文件权限查询都执行完整检查并接受成本。

## 3. 构建、包含与平台保护

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#ifdef Q_OS_WIN
#  include <QNtfsPermissionCheckGuard>
#endif
```

该类和三个相关函数只在 Windows 上可用。跨平台源文件应使用条件编译：

```cpp
QFileDevice::Permissions accuratePermissions(const QString &path)
{
#ifdef Q_OS_WIN
    QNtfsPermissionCheckGuard guard;
#endif
    return QFileInfo(path).permissions();
}
```

不要在非 Windows 分支提供一个同名空 guard 来暗示完全相同的文件权限语义。Unix 权限位、Windows ACL、网络文件系统和平台用户模型本来就不同。

## 4. RAII 与引用计数模型

构造函数内部调用：

```cpp
qEnableNtfsPermissionChecks();
```

析构函数内部调用：

```cpp
qDisableNtfsPermissionChecks();
```

低层开关按“使用者数量”配对，而不是简单的单个布尔值。因此 guard 可以安全嵌套：

```text
初始计数 0：检查关闭
外层 guard 构造：计数 1，检查开启
内层 guard 构造：计数 2，检查仍开启
内层 guard 析构：计数 1，检查仍开启
外层 guard 析构：计数 0，检查关闭
```

示例：

```cpp
void outer(const QString &path)
{
    QNtfsPermissionCheckGuard outerGuard;
    inspectOwner(path);

    {
        QNtfsPermissionCheckGuard innerGuard;
        inspectAcl(path);
    } // 只撤销 innerGuard 的一次 enable，检查仍处于开启状态

    inspectPermissions(path);
} // 最后一个 guard 退出后关闭
```

这也是不能用简单“保存旧 bool，析构时恢复 bool”来理解它的原因。系统允许多个独立使用者同时要求开启，只有最后一个使用者退出后才真正关闭。

## 5. 作用域不是文件范围，而是全局行为范围

guard 不保存路径：

```cpp
QNtfsPermissionCheckGuard guard;
```

其存活期间，进程中使用相关 Qt 文件 API 的代码都会观察到 NTFS permission checking 已启用，而不只是当前函数中的某个 `QFileInfo`。

这意味着：

- guard 是作用域管理对象，但底层设置具有进程范围影响；
- 其他线程同时执行的 `QFileInfo` 查询也可能承担更高成本；
- 不应把它当作只影响一个局部对象的配置；
- 缩小 guard 生命周期有助于降低全局性能影响。

如果多个线程各自创建 guard，引用计数会让检查保持开启，直到最后一个 guard 析构。不要依赖某个线程 guard 退出的时间来断言全局状态立即关闭。

## 6. 与 `QFileInfo` 缓存的关系

`QFileInfo` 默认缓存已经查询到的文件元数据。先在未启用完整权限检查时读取，再创建 guard，并不保证同一个已缓存对象自动刷新全部结果：

```cpp
QFileInfo info(path);
const bool approximate = info.isWritable();

QNtfsPermissionCheckGuard guard;
info.refresh();
const bool checked = info.isWritable();
```

需要重新读取时：

- 在 guard 作用域内创建新的 `QFileInfo`；
- 或调用 `refresh()`；
- 或按业务需要调用 `setCaching(false)`。

guard 改变查询策略，不负责使所有现存 `QFileInfo` 缓存失效。

## 7. 低层函数的精确语义

### 7.1 `qEnableNtfsPermissionChecks()`

```cpp
bool qEnableNtfsPermissionChecks() noexcept;
```

增加一个“需要完整检查”的使用者。

返回值容易读反：

- 返回 `true`：调用前已经启用，说明还有其他使用者；
- 返回 `false`：调用前未启用，本次调用使其从关闭变为开启。

一般业务代码不应依赖这个返回值管理 guard，直接使用 RAII 类更安全。

### 7.2 `qDisableNtfsPermissionChecks()`

```cpp
bool qDisableNtfsPermissionChecks() noexcept;
```

必须只用于匹配此前的一次 `qEnableNtfsPermissionChecks()`。

- 返回 `true`：撤销后已经没有使用者，检查处于关闭状态；
- 返回 `false`：仍有其他使用者，检查继续开启。

多调用一次 disable 会破坏配对协议；漏调用则会让昂贵检查持续开启。

### 7.3 `qAreNtfsPermissionChecksEnabled()`

```cpp
bool qAreNtfsPermissionChecksEnabled() noexcept;
```

当前至少有一个使用者时返回 `true`。它适合诊断和测试，不应作为“先查询再启用”的竞争式控制逻辑：

```cpp
// 不推荐：查询与启用之间可能有其他线程改变状态。
if (!qAreNtfsPermissionChecksEnabled())
    qEnableNtfsPermissionChecks();
```

直接构造 guard 即可。引用计数就是为了让每个使用者独立配对，而不是先争夺一个布尔开关。

## 8. 线程安全边界

Qt 6.11.1 将三个低层函数标记为 thread-safe，但附带重要条件：不能再有代码并发直接修改旧的 `qt_ntfs_permission_lookup` 全局变量。

Qt 6.6 起该变量已经 deprecated，原因正是它是非原子的，容易产生数据竞争。

因此：

- 新代码只使用 `QNtfsPermissionCheckGuard` 或三个函数；
- 不直接读写 `qt_ntfs_permission_lookup`；
- 迁移旧代码时一次性移除所有手工 `++` / `--`；
- 只要旧变量仍被并发修改，新 API 的线程安全保证就被破坏。

虽然开关操作可以跨线程配对，仍建议让每个 guard 在创建它的作用域和线程中析构。该类不可移动，天然避免了把“应撤销的一次启用”随意转移到另一个所有者。

## 9. 生命周期与类型限制

头文件使用 `Q_DISABLE_COPY_MOVE(QNtfsPermissionCheckGuard)`，因此它：

- 不能复制构造；
- 不能复制赋值；
- 不能移动构造；
- 不能移动赋值。

这是有意设计。每个实例严格代表一次 enable 和一次 disable：

```cpp
QNtfsPermissionCheckGuard guard;

// 错误：不能复制，否则会出现两个析构与一次 enable 不匹配。
// auto copy = guard;
```

不要：

- 按值返回 guard；
- 把它放入要求移动元素的普通容器；
- 用 `new` 创建后忘记释放；
- 让它比需要完整检查的代码活得更久。

栈上局部变量是最自然、最可靠的用法。

## 10. 它不提供什么安全保证

### 10.1 不修改 ACL

guard 只启用查询。它不会授予当前用户读写权限，也不会调用 Windows ACL 修改 API。

### 10.2 不保证后续操作成功

权限检查与文件操作之间存在 TOCTOU 窗口：

```text
检查可写 -> 另一个进程修改 ACL -> 当前进程尝试写入
```

始终以真实 `open()`、`rename()`、`remove()` 等操作结果为准。

### 10.3 不统一不同文件系统的语义

路径可能位于 FAT、ReFS、网络共享、虚拟文件系统或设备路径。类名强调 NTFS；不要把结果解释成所有 Windows 存储后端都具有完全一致的 ACL 行为。

### 10.4 不保护文件免受并发修改

它不是 mutex，也不是 `QLockFile`。需要跨进程互斥时另行使用合适的锁或事务协议。

## 11. 常见错误

### 11.1 把它当成某个文件的权限检查器

构造函数没有路径参数。它只是临时改变 Qt 文件 API 的查询深度，真正查询仍由 `QFileInfo` 等对象完成。

### 11.2 让 guard 覆盖整个应用生命周期

这会让所有相关查询持续承担 ACL 成本。只包围必须取得准确权限或所有者信息的操作。

### 11.3 依赖 `isWritable()` 后不检查 `open()`

权限可能变化，文件可能被删除、锁定或被安全软件拦截。预检只用于体验优化，真实操作返回值才是最终依据。

### 11.4 在 guard 构造前已经读取并缓存结果

对同一个 `QFileInfo` 调用 `refresh()`，或在 guard 作用域内重新构造它。

### 11.5 手工 enable 后忘记 disable

除非正在封装低层基础设施，否则使用 `QNtfsPermissionCheckGuard`，让异常和早退也能正确配对。

### 11.6 混用新 API 与旧全局变量

直接修改 deprecated 的 `qt_ntfs_permission_lookup` 会破坏线程安全保证和引用计数协议。迁移后不要保留两套控制方式。

### 11.7 在非 Windows 平台无条件引用

该类只在 Windows 上存在。跨平台代码必须用 `#ifdef Q_OS_WIN` 保护。

## 12. 逐项 API 说明

### 12.1 `QNtfsPermissionCheckGuard()`

```cpp
QNtfsPermissionCheckGuard();
```

构造 guard，并调用 `qEnableNtfsPermissionChecks()` 增加一次使用计数。

边界：

- 从此处到析构期间，进程中的相关 Qt 文件查询启用完整 NTFS 检查；
- 构造不检查特定路径；
- 对象不可复制、不可移动；
- 应用通常不需要读取底层函数返回值。

### 12.2 `~QNtfsPermissionCheckGuard()`

```cpp
~QNtfsPermissionCheckGuard() noexcept;
```

调用 `qDisableNtfsPermissionChecks()` 撤销本实例对应的一次启用。

边界：

- 只有最后一个使用者退出时才真正关闭；
- 析构不抛异常；
- 它不刷新 `QFileInfo` 缓存；
- 它不撤销或修改文件本身的权限。

### 12.3 禁止的复制与移动 API

```cpp
QNtfsPermissionCheckGuard(const QNtfsPermissionCheckGuard &) = delete;
QNtfsPermissionCheckGuard &operator=(const QNtfsPermissionCheckGuard &) = delete;
QNtfsPermissionCheckGuard(QNtfsPermissionCheckGuard &&) = delete;
QNtfsPermissionCheckGuard &operator=(QNtfsPermissionCheckGuard &&) = delete;
```

禁止这些操作确保一次构造严格对应一次析构，避免引用计数失配。

### 12.4 相关低层函数

| API | 作用 | 返回值和边界 |
| --- | --- | --- |
| `bool qEnableNtfsPermissionChecks() noexcept` | 增加一次完整检查使用计数 | `true` 表示调用前已经开启；优先用 guard |
| `bool qDisableNtfsPermissionChecks() noexcept` | 匹配并撤销一次 enable | `true` 表示已无使用者并关闭；不能无配对调用 |
| `bool qAreNtfsPermissionChecksEnabled() noexcept` | 查询当前是否至少有一个使用者 | 用于诊断；不要写 check-then-enable 竞争逻辑 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 作用域 | `QNtfsPermissionCheckGuard guard;` | 在当前作用域启用完整 NTFS ACL/所有者检查 | 进程范围有影响，尽量缩短生命周期 |
| 析构 | `~QNtfsPermissionCheckGuard()` | 自动撤销本实例的一次启用 | 嵌套 guard 中只有最后一个退出才关闭 |
| 类型 | 复制、移动操作 | 全部删除 | 每个对象严格对应一对 enable/disable |
| 查询 | `qAreNtfsPermissionChecksEnabled()` | 查看全局检查是否开启 | 不要用它代替 RAII |
| 低层开启 | `qEnableNtfsPermissionChecks()` | 增加使用者计数 | 返回 true 表示之前已经开启 |
| 低层关闭 | `qDisableNtfsPermissionChecks()` | 减少使用者计数 | 只能匹配先前 enable |
| 缓存 | `QFileInfo::refresh()` | 重新读取文件信息 | guard 不自动清除旧缓存 |
| 实际操作 | `QFile::open()` 等 | 验证真实访问能否成功 | 预检不能替代操作返回值 |

## 14. 一句话总结

`QNtfsPermissionCheckGuard` 是 Windows 专用的引用计数式 RAII 开关：只在需要准确 NTFS ACL 和所有者信息的短作用域中创建它，让 `QFileInfo` 等执行完整检查；它不修改权限、不锁文件，也不能替代真实文件操作的成功判断。
