# QStorageInfo：查询挂载卷、空间和文件系统信息

> Qt 6.11.1 | `#include <QStorageInfo>` | 模块：`Qt6::Core`

`QStorageInfo` 描述“某个路径所在的已挂载卷”，而不是文件本身。它可以告诉你挂载点、可用空间、设备名、文件系统类型、卷标、只读状态和就绪状态。

它适合下载前检查用户配额可用空间、选择可写卷、展示磁盘信息、或判断应用目录落在哪个文件系统。它不负责监听卷变化，也不能保证从查询到真正写文件之间空间仍然足够。

## 基本用法

```cpp
#include <QStorageInfo>

QStorageInfo storage(QDir::homePath());
storage.refresh();

if (!storage.isValid() || !storage.isReady() || storage.isReadOnly()) {
    reportStorageUnavailable();
} else if (storage.bytesAvailable() < requiredBytes) {
    reportNotEnoughSpace();
} else {
    saveDocument();
}
```

传给构造函数或 `setPath()` 的可以是挂载点、目录，或该卷内的文件。`rootPath()` 返回的却是实际挂载点，因此它不一定等于输入路径。

## 它解决的实际问题

### 保存文件前的预检

对当前用户而言，最有价值的是 `bytesAvailable()`，不是 `bytesFree()`：前者会考虑文件系统配额，后者是整卷空闲空间，管理员或 root 用户以外的调用者未必能真正使用那么多。

预检只能改善提示。写入时仍可能因为并发占用、配额变化、权限、断连或文件系统错误而失败，因此实际 `QSaveFile::commit()` / `QFile::write()` 的错误处理不能省略。

### 选择所有可写卷

```cpp
for (const QStorageInfo &volume : QStorageInfo::mountedVolumes()) {
    if (volume.isValid() && volume.isReady() && !volume.isReadOnly())
        addCandidate(volume.rootPath(), volume.displayName());
}
```

Windows 上 `mountedVolumes()` 返回“此电脑”中可见的驱动器；Unix 上返回已挂载的文件系统，但排除伪文件系统。不要把这个列表当作“机器上的所有物理磁盘”。

### 显示卷信息

`displayName()` 面向 UI：没有卷名时回退到挂载路径。`name()` 是人类可读的 label，但有些文件系统不支持或未设置 label，所以可能为空。`device()`、`fileSystemType()`、`subvolume()` 都是平台和文件系统相关的诊断数据，不应用来构建跨平台的业务规则。

## 缓存与刷新

`QStorageInfo` 会缓存查询结果。构造对象或调用 `setPath()` 时会读取信息；之后磁盘剩余空间、介质插入状态或挂载状态变化不会自动反映到已有对象，必须调用 `refresh()` 重置内部缓存。

这有两个后果：

- 轮询显示可用空间时，复用对象前要 `refresh()`，并控制频率。
- 多个隐式共享副本可能带着当时的快照；不要把很早之前复制出的对象当实时监控值。

## 有效、就绪与根卷

- `isValid()`：`rootPath()` 指向的卷存在并且正确挂载。
- `isReady()`：卷可以工作；例如没有插入介质的光驱可能有效但未就绪。未就绪时，类型、卷名和空间等信息会是无效数据。
- `isReadOnly()`：当前文件系统受写保护。
- `isRoot()` / `root()`：系统根卷。Unix 是挂载于 `/` 的卷；Windows 是操作系统所在卷，不等价于“任意盘符根目录”。

先检查 `isValid()` 与 `isReady()`，再使用空间和元数据值。对无效对象，`blockSize()`、`bytesTotal()`、`bytesFree()` 和 `bytesAvailable()` 会返回 `-1`。

## 平台与数据解释

- `device()` 在 Unix/macOS 本地存储上常类似 `/dev/sda0`；Windows 本地卷常是以 `\\?\` 开头的卷 GUID 路径。它不是面向用户的显示字符串。
- `fileSystemType()` 是平台相关名称。同一个 NTFS 卷在 Linux 可能显示为 `ntfs-3g` 或 `fuseblk`，不能据此写死跨平台判断。
- `subvolume()` 仅当文件系统可检测到子卷时才有意义，例如 Btrfs 子卷或 Unix bind mount；格式由文件系统决定。
- `blockSize()` 是推荐传输块大小，不是保证的分配单元，也不是应用缓冲区必须使用的大小。

## 值语义与线程

`QStorageInfo` 是隐式共享值类型，可复制、移动和比较。复制并不意味着持续同步，比较表示是否指向同一驱动器或卷；两个无效对象比较相等是文档定义的特殊情况，不能把它当作同一真实卷。

它不关联事件循环或 `QObject` 线程亲和性。不同线程各自查询不同值对象通常没有问题；若共享同一实例并且某个线程调用 `refresh()` 或 `setPath()`，仍应由调用方同步访问。

## 常见错误

1. **使用 `bytesFree()` 判断可写配额。** 需要检查当前用户可用空间时使用 `bytesAvailable()`。
2. **创建后从不刷新。** 长寿命对象返回的是缓存数据。
3. **只检查 `isValid()`。** 可移动介质或网络卷还可能尚未就绪。
4. **把 `device()` 或文件系统类型展示给普通用户。** 优先 `displayName()` 和 `rootPath()`。
5. **把预检当作写入成功保证。** 实际写入必须处理失败和空间变化。
6. **假定 `mountedVolumes()` 枚举物理磁盘。** 它枚举的是已挂载、平台可见的文件系统。

## API 速查表

| 类别 | API | 语义 | 使用边界 |
| --- | --- | --- | --- |
| 构造 | `QStorageInfo()` | 创建空、无效对象。 | 先 `setPath()`，或直接用带路径构造。 |
| 构造 | `QStorageInfo(const QString &path)` / `QStorageInfo(const QDir &dir)` | 获取 `path` 或 `dir` 所在卷的信息。 | 输入可为文件、目录或挂载点；之后检查有效且就绪。 |
| 值语义 | 拷贝/移动构造、`operator=`、`swap()` | 复制、移动或交换卷信息快照。 | 移动后的对象只可析构或重新赋值；副本不自动刷新。 |
| 路径 | `setPath(const QString &path)` | 让对象改为描述该路径所在卷。 | 会重新建立缓存；路径不存在时可能无效。 |
| 挂载点 | `rootPath()` | 返回真实挂载点。 | 不保证等于传入的文件或目录路径。 |
| 设备 | `device()` | 返回卷对应设备标识。 | 格式平台相关，不适合 UI 或持久化协议。 |
| 子卷 | `subvolume()` | 返回可检测的子卷名。 | 并非所有文件系统支持，格式文件系统相关。 |
| 文件系统 | `fileSystemType()` | 返回文件系统类型名。 | 名称随平台、驱动和实现变化。 |
| 卷标 | `name()` | 返回人类可读的文件系统 label。 | 不支持或未设置时为空。 |
| 显示名称 | `displayName()` | 返回卷名；无名称时回退到根路径。 | 面向显示，不应作为稳定 ID。 |
| 总空间 | `bytesTotal()` | 返回卷总字节数。 | 无效对象返回 `-1`；值随刷新时刻变化。 |
| 整卷空闲 | `bytesFree()` | 返回整卷剩余字节数。 | 配额环境下可能大于当前用户可用空间。 |
| 用户可用 | `bytesAvailable()` | 返回当前用户可用字节数。 | 保存预检优先使用；仍不保证后续写入成功。 |
| 块大小 | `blockSize()` | 返回文件系统最佳传输块大小。 | 无法确定或无效时为 `-1`。 |
| 写保护 | `isReadOnly()` | 判断文件系统是否禁止写入。 | 即使为 false，写入仍可能受权限和配额限制。 |
| 就绪 | `isReady()` | 判断卷当前是否可工作。 | 介质未插入等情况会为 false；空间等数据不可用。 |
| 有效性 | `isValid()` | 判断挂载卷是否存在且正确挂载。 | 访问其余元数据前先检查。 |
| 根卷 | `isRoot()` | 判断是否为系统根卷。 | Windows 上指系统所在卷；不是任意根目录。 |
| 刷新 | `refresh()` | 使缓存失效并重新获取存储信息。 | 长寿命或轮询对象需主动调用。 |
| 枚举 | `mountedVolumes()` | 返回当前挂载卷列表。 | Windows 是可见驱动器；Unix 排除伪文件系统。 |
| 系统根 | `root()` | 返回系统根卷的信息。 | Unix 是 `/`，Windows 是 OS 所在卷。 |
| 比较 | `operator==` / `operator!=` | 比较是否表示同一卷或驱动器。 | 两个无效对象比较相等，不能据此确认实际卷。 |

`QStorageInfo` 给的是一次查询快照。把它用于友好的预检和诊断，同时把真正的可靠性留给实际的文件写入、错误处理和必要的重试策略。
