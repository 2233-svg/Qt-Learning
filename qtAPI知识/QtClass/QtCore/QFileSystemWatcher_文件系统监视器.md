# Qt QFileSystemWatcher 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QFileSystemWatcher>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject -> QFileSystemWatcher`  
> 定位：把一组文件或目录加入平台文件系统通知机制，并通过信号报告变化

## 1. QFileSystemWatcher 解决什么问题

`QFileSystemWatcher` 用来监听文件系统中指定路径的变化。它把不同平台的文件通知机制封装成两个 Qt 信号：

- `fileChanged(path)`：某个被监视的文件被修改、重命名或删除；
- `directoryChanged(path)`：某个被监视的目录或目录内容被修改，或者该目录被删除。

典型使用场景：

- 配置文件变化后自动重新加载；
- 日志目录、插件目录、资源目录变化后刷新列表；
- 开发工具监视源码、模板或资源文件；
- 缓存索引在文件变化后失效；
- 文件同步、导入工具在目录变化后触发一次重新扫描。

它解决的是“变化通知”问题，不是“完整审计日志”问题。信号可能合并，平台也可能只告诉你“这个目录变了”，而不是告诉你每个新增、删除、改名的细节。收到信号后，稳妥做法通常是重新读取当前状态。

```text
addPath("settings.ini")
        |
        v
平台文件系统通知
        |
        v
fileChanged("settings.ini")
        |
        v
重新检查 exists / size / lastModified，再决定 reload
```

## 2. 基本使用模型

`QFileSystemWatcher` 是 `QObject`。它依赖对象所属线程的事件循环投递信号，因此常规用法是在有事件循环的线程中创建和使用它：

```cpp
#include <QCoreApplication>
#include <QFileSystemWatcher>
#include <QFileInfo>
#include <QDebug>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    QFileSystemWatcher watcher;
    const QString path = QStringLiteral("settings.ini");

    if (!watcher.addPath(path))
        qWarning() << "cannot watch" << path;

    QObject::connect(&watcher, &QFileSystemWatcher::fileChanged,
                     [&](const QString &changedPath) {
        qInfo() << "changed:" << changedPath;
        QFileInfo info(changedPath);
        qInfo() << "exists:" << info.exists()
                << "modified:" << info.lastModified();
    });

    return app.exec();
}
```

`addPath()` 和 `addPaths()` 只负责向监视器注册路径。它们不会打开文件，不会阻止文件被删除，也不会让路径在变化后自动保持有效。

同一个 watcher 可以同时监视文件和目录：

```cpp
watcher.addPath("settings.ini");
watcher.addPath("plugins");

QObject::connect(&watcher, &QFileSystemWatcher::directoryChanged,
                 this, &PluginManager::reloadPluginList);
```

需要注意的是：目录监视通常适合触发“重新扫描目录”，而不是替代对每个重要文件的内容监视。目录内容变化的粒度和触发条件受平台后端影响。

## 3. 添加路径：必须已经存在

`addPath(path)` 只有在路径存在、尚未被该 watcher 监视，并且平台资源允许时才会成功：

```cpp
if (!watcher.addPath(path)) {
    qWarning() << "watch failed:" << path;
}
```

失败原因通常是系统相关的，可能包括：

- 路径不存在；
- 没有访问权限；
- 该路径已经在这个 watcher 中；
- 平台后端达到可监视数量上限；
- 文件系统或平台不支持相应通知。

`addPath()` 返回 `bool`，但没有提供详细错误枚举。诊断时通常要结合 `QFileInfo`、日志和平台限制。

批量添加使用 `addPaths()`：

```cpp
const QStringList failed =
    watcher.addPaths(QStringList{configPath, pluginDir, themeDir});

for (const QString &path : failed)
    qWarning() << "not watched:" << path;
```

`addPaths()` 的返回值不是“成功列表”，而是“无法监视的路径列表”。这点很容易写反。

如果想监视未来才会创建的文件，不能直接 `addPath()` 一个不存在的文件。常见做法是先监视它的父目录，在目录变化后检查目标文件是否出现，再把目标文件加入监视。

## 4. 文件变化：修改、重命名、删除

`fileChanged(path)` 会在指定文件被修改、重命名或从磁盘删除时发出：

```cpp
QObject::connect(&watcher, &QFileSystemWatcher::fileChanged,
                 nullptr, [&watcher](const QString &path) {
    reloadIfStillReadable(path);

    if (!watcher.files().contains(path) && QFileInfo::exists(path))
        watcher.addPath(path);
});
```

Qt 文档特别提醒：很多应用保存文件时会写入一个新文件，再删除或替换旧文件。这样做可以提升保存安全性，但对 watcher 来说，原来被监视的文件可能已经被重命名或删除。`QFileSystemWatcher` 会在文件被重命名或删除后停止监视它。

因此在槽函数中可以检查：

```cpp
if (!watcher.files().contains(path) && QFileInfo::exists(path))
    watcher.addPath(path);
```

这不是为了“修复信号”，而是为了在文件已经被安全保存流程替换后，把新出现的路径重新纳入监视。

文件变化信号也不表示文件此刻已经可以稳定读取。写入者可能仍在写，或者刚刚替换路径。对配置 reload、索引刷新等逻辑，通常需要短暂 debounce，再重新读取当前状态。

## 5. 目录变化：触发后重新扫描

`directoryChanged(path)` 会在目录本身或其内容发生变化时发出，例如添加或删除文件，也会在目录被移除时发出。

```cpp
QObject::connect(&watcher, &QFileSystemWatcher::directoryChanged,
                 this, [this](const QString &path) {
    scheduleDirectoryRescan(path);
});
```

如果短时间内发生多次变化，某些中间变化可能不会各自发出信号，但变化序列的最后一次会产生信号。换句话说，不能把它当作“一次文件操作一个事件”的队列。

目录监视的稳妥模式是：

```text
directoryChanged
        |
        v
启动或重启短延迟定时器
        |
        v
重新列出目录
        |
        v
与上一次快照比较，更新业务状态
```

如果要监视整棵目录树，不能只添加根目录就假设所有子目录中的变化都会按你的业务粒度报告。应把需要关注的子目录逐个加入 watcher，并在目录结构变化后维护这组 watched paths。

## 6. 当前正在监视什么

`files()` 和 `directories()` 返回当前被监视的文件和目录列表：

```cpp
const QStringList watchedFiles = watcher.files();
const QStringList watchedDirs = watcher.directories();
```

这些列表适合：

- 在调试界面展示当前监视范围；
- 收到 `fileChanged()` 后判断某个文件是否已从 watcher 中移除；
- 批量清理监视项；
- 对外暴露 watcher 的当前状态。

不要把列表当作文件系统实时状态。它只说明 watcher 当前认为自己监视哪些路径，不说明这些路径现在一定存在，也不说明它们可读可写。

路径字符串的比较应尽量使用一致的路径形式。注册时如果混用相对路径、绝对路径和符号链接路径，后续用 `contains()` 判断时容易出现“指向同一个文件但字符串不同”的情况。实际项目中建议在加入 watcher 前统一路径策略，例如使用绝对路径，必要时处理 canonical 路径的空值。

## 7. 移除路径

`removePath(path)` 从 watcher 中移除一个路径：

```cpp
if (!watcher.removePath(path))
    qWarning() << "unwatch failed:" << path;
```

移除失败原因同样是系统相关的，可能包括路径已经被删除、后端状态变化或该路径并没有处在可移除状态。批量移除：

```cpp
const QStringList failed = watcher.removePaths(watcher.files());
```

`removePaths()` 返回“未能移除的路径列表”，不是成功移除的列表。和 `addPaths()` 一样，返回值需要按失败列表理解。

析构 watcher 会销毁监视器并释放对应平台资源。对于长期运行应用，仍建议在业务对象关闭时主动移除不再需要的路径，避免监视范围随着插件、项目或工作区切换不断膨胀。

## 8. 平台资源和后端边界

监视文件系统会消耗平台资源。Qt 文档给出的典型边界包括：

- 某些 BSD 系统上，每个被监视文件都需要一个打开的文件描述符；
- 一些系统默认打开文件描述符限制可能很低，例如 256；
- 达到平台限制后，`addPath()` 或 `addPaths()` 会失败；
- 在没有 inotify 支持的 Linux 内核上，被监视路径所在的文件系统可能无法卸载。

这些限制直接影响设计：

- 不要为目录中每个临时文件都长期建立 watcher；
- 大目录树监视要考虑上限和降级策略；
- 用户打开多个项目时要释放旧项目的 watcher；
- watcher 失败时应允许手动刷新或定时扫描作为 fallback。

`QFileSystemWatcher` 不承诺所有平台提供完全一致的事件粒度。跨平台应用应把 watcher 当作“状态可能变化了，请重新检查”的提示。

## 9. 与 QFileInfo、QDir 和 QTimer 配合

### 9.1 用 QFileInfo 重新判断当前状态

收到变化后，重新查询文件状态：

```cpp
void SettingsReloader::onFileChanged(const QString &path)
{
    QFileInfo info(path);
    if (!info.exists()) {
        markMissing(path);
        return;
    }

    if (info.isFile())
        reloadFile(path);
}
```

不要在槽里假设路径还存在。文件删除、替换和权限变化都可能刚刚发生。

### 9.2 用 QDir 重新扫描目录

```cpp
void PluginManager::rescan(const QString &path)
{
    QDir dir(path);
    const QFileInfoList entries =
        dir.entryInfoList(QDir::Files | QDir::NoDotAndDotDot);

    rebuildPluginIndex(entries);
}
```

目录信号只告诉你目录变了，真正的业务差异要通过扫描结果或快照比较得出。

### 9.3 用 QTimer 做 debounce

文件保存经常会产生多个底层事件。直接在每个信号里执行昂贵 reload，可能导致重复工作或读到中间状态。

```cpp
void WatcherOwner::onAnyChanged(const QString &path)
{
    m_pending.insert(path);
    m_reloadTimer.start(150);
}
```

定时器超时后统一处理 `m_pending`，通常比每个信号立刻处理更稳。

## 10. 常见误区

### 10.1 以为它会监视不存在的文件

`addPath()` 要求路径存在。要等待文件创建，先监视父目录，再在目录变化后添加目标文件。

### 10.2 以为重命名或删除后还会继续监视

文件被重命名或删除后，watcher 会停止监视该文件；目录被删除后，也会停止监视该目录。需要继续监视同一路径时，检查路径重新存在后再次 `addPath()`。

### 10.3 以为每个变化都有一个信号

短时间内多次变化可能被合并。设计上应重新读取当前状态，而不是依赖信号次数。

### 10.4 用目录监视替代所有文件监视

目录变化适合触发重新扫描，不适合判断目录内每个文件内容是否已经写完。重要文件仍应单独监视，或通过扫描元数据、校验和、业务事务日志来确认。

### 10.5 忽略 watcher 自身的资源限制

大目录树、临时文件目录和大量项目同时打开时，监视项数量可能触达平台上限。必须处理 `addPath()` 失败，而不是把 watcher 注册当成必然成功。

## 11. API 逐项说明

### 11.1 构造和析构

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `QFileSystemWatcher(QObject *parent = nullptr)` | 创建空的文件系统监视器。 | 需要事件循环接收信号；生命周期可由 QObject parent 管理。 |
| `QFileSystemWatcher(const QStringList &paths, QObject *parent = nullptr)` | 创建 watcher 并尝试监视一组路径。 | 仍可能有路径未被监视；创建后用 `files()` / `directories()` 或重新添加策略确认。 |
| `~QFileSystemWatcher()` | 销毁 watcher。 | 释放平台监视资源；销毁后不会再发出变化信号。 |

### 11.2 添加和移除

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `addPath(const QString &path)` | 添加一个文件或目录到监视列表。 | 路径必须存在且未被监视；失败返回 false。 |
| `addPaths(const QStringList &paths)` | 批量添加文件或目录。 | 返回无法监视的路径列表，不是成功列表。 |
| `removePath(const QString &path)` | 从监视列表移除一个路径。 | 成功返回 true；路径已删除等情况可能失败。 |
| `removePaths(const QStringList &paths)` | 批量移除路径。 | 返回未能移除的路径列表。 |

### 11.3 查询当前监视列表

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `files() const` | 返回当前被监视的文件路径列表。 | 适合判断文件被替换后是否还在 watcher 中。 |
| `directories() const` | 返回当前被监视的目录路径列表。 | 只表示 watcher 状态，不保证目录当前存在。 |

### 11.4 信号

| 信号 | 何时发出 | 使用时重点注意 |
| --- | --- | --- |
| `fileChanged(const QString &path)` | 文件被修改、重命名或删除。 | 文件重命名或删除后 watcher 停止监视；需要时重新添加。 |
| `directoryChanged(const QString &path)` | 目录或目录内容被修改，或目录被删除。 | 多个短时间变化可能合并；槽中应重新扫描目录。 |

两个信号在文档中标记为 private signal。普通代码可以连接它们，但不应该由用户代码主动发出。

### 11.5 相关继承能力

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `QObject` parent | 用对象树管理 watcher 生命周期。 | 父对象销毁会销毁 watcher；注意线程亲和性。 |
| `moveToThread()` | 改变 watcher 所属线程。 | 目标线程需要事件循环；跨线程调用用信号槽排队更清晰。 |
| `deleteLater()` | 在事件循环中延迟销毁。 | 适合从信号槽中安全结束 watcher 生命周期。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QFileSystemWatcher()` | 创建空 watcher。 | 需要事件循环分发变化信号。 |
| 构造 | `QFileSystemWatcher(paths)` | 创建并添加一组初始路径。 | 仍要确认哪些路径实际被监视。 |
| 析构 | `~QFileSystemWatcher()` | 销毁 watcher 并释放资源。 | 不再接收变化通知。 |
| 添加 | `addPath(path)` | 添加一个存在的文件或目录。 | 不存在、重复、权限不足或达到上限会失败。 |
| 添加 | `addPaths(paths)` | 批量添加路径。 | 返回失败列表。 |
| 移除 | `removePath(path)` | 移除一个 watched path。 | 成功返回 true；已删除路径可能移除失败。 |
| 移除 | `removePaths(paths)` | 批量移除路径。 | 返回未能移除的列表。 |
| 查询 | `files()` | 返回当前被监视的文件。 | 文件被替换后可用它判断是否需要 re-add。 |
| 查询 | `directories()` | 返回当前被监视的目录。 | 不代表目录一定还存在。 |
| 信号 | `fileChanged(path)` | 文件修改、重命名或删除时通知。 | rename/remove 后停止监视该文件。 |
| 信号 | `directoryChanged(path)` | 目录或目录内容修改、目录删除时通知。 | 信号可能合并，收到后重新扫描。 |
| 边界 | 平台资源限制 | 监视消耗平台资源。 | 大量监视项必须处理失败和降级策略。 |
| 边界 | 非递归设计 | 只添加明确路径。 | 目录树监视需要维护子目录列表。 |
| 协作 | `QFileInfo` | 收到信号后查询当前状态。 | `exists()`、`isFile()` 等仍是瞬时结果。 |
| 协作 | `QDir` | 目录变化后重新枚举。 | 通过快照比较得出业务差异。 |
| 协作 | `QTimer` | 合并短时间内多个变化。 | 避免重复 reload 和读取中间状态。 |

### 一句话总结

`QFileSystemWatcher` 是“变化提醒器”，不是文件系统事件日志。把存在的文件或目录加入 watcher，收到信号后重新检查当前状态；重命名、删除、批量保存、平台资源上限和信号合并都要作为正常边界处理。
