# Qt QDirIterator 深入笔记

> 适用版本：Qt 6.11  
> 头文件：`#include <QDirIterator>`  
> 所属模块：`Qt6::Core`  
> 状态：已弃用，新的代码应使用 `QDirListing`  
> 相关类：`QDir`、`QDirListing`、`QFileInfo`、`QFile`

## 1. 它解决什么问题：按需、单向地走过目录项

`QDirIterator` 用于逐项枚举一个目录，必要时递归进入子目录。它不会像 `QDir::entryList()` 那样先把整份路径列表收集到内存，而是以单向迭代的方式让调用者一次处理一个目录项。

它曾适合这些场景：

- 遗留工具递归寻找某类文件；
- 对大目录树逐项统计大小、索引或检查扩展名；
- 扫描部署目录中的资源、插件或配置；
- 以 `QFileInfo` 为单位处理每一个发现的文件。

但 Qt 6.11 的官方文档已将它标记为**弃用**，且说明未来版本可能移除。新代码应使用 `QDirListing`，它提供更现代的范围式接口和更清晰的选项模型。本页仍有价值，因为已有 Qt 5 / Qt 6 项目中大量使用 `QDirIterator`，维护时必须正确理解它的过滤、递归和符号链接行为。

| 需求 | 建议选择 | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 新项目递归列目录 | `QDirListing` | 使用现代目录枚举接口 | 不要为新功能继续引入 `QDirIterator` |
| 只需一次拿到小目录的列表 | `QDir::entryList()` 或 `entryInfoList()` | 返回已收集的列表 | 可排序，但会一次占用所有结果的内存 |
| 维护旧代码的流式遍历 | `QDirIterator` | 单向按项返回路径或 `QFileInfo` | 已弃用；迁移计划应纳入技术债 |
| 监控目录变化 | `QFileSystemWatcher` | 监听变化而不是一次扫描 | 监听不等于可靠的全量同步机制 |

## 2. 最小正确循环：先判断，再推进

```cpp
#include <QDir>
#include <QDirIterator>
#include <QFileInfo>

void findJsonFiles(const QString &root)
{
    QDirIterator it(root,
                    {"*.json"},
                    QDir::Files | QDir::Readable,
                    QDirIterator::Subdirectories);

    while (it.hasNext()) {
        const QFileInfo info = it.nextFileInfo();
        if (!info.exists())
            continue; // 扫描与使用之间文件可能被删除

        processJsonFile(info.absoluteFilePath());
    }
}
```

循环协议固定是：

1. `hasNext()` 判断是否还有下一个条目；
2. `next()` 或 `nextFileInfo()` 推进到下一个条目；
3. 使用 `fileName()`、`filePath()`、`fileInfo()` 或推进函数返回值读取当前条目；
4. 不要再期待后退、跳转或按索引访问。

`next()` 在没有更多项时返回空 `QString`，`nextFileInfo()` 则返回空 `QFileInfo`。虽然 API 有这种兜底返回，正常代码仍应始终用 `hasNext()` 保护推进操作；空路径和空文件信息不应被当作“一个正常的空名字文件”继续处理。

## 3. 过滤的两层含义：名称模式与条目类型

构造函数可以同时指定 `nameFilters` 和 `QDir::Filters`：

```cpp
QDirIterator it(
    root,
    {"*.png", "*.jpg", "*.jpeg"},
    QDir::Files | QDir::Readable,
    QDirIterator::Subdirectories);
```

- `nameFilters` 是文件名模式，例如 `*.png`；它不是正则表达式，也不负责决定条目是否为文件或目录。
- `QDir::Filters` 决定保留哪些种类和属性，例如 `QDir::Files`、`QDir::Dirs`、`QDir::Readable`、`QDir::Hidden`、`QDir::NoDotAndDotDot`。
- `IteratorFlags` 决定遍历方式，例如是否递归、是否跟随目录符号链接。

最常见的错误是只写名称模式而不写 `QDir::Files`，然后意外得到同名目录或特殊条目；或者只写 `QDir::Files` 却希望递归，结果只扫描根目录。过滤和递归是两套独立配置。

### 3.1 `QDir` 构造函数的一个细节

```cpp
QDir dir(root);
dir.setNameFilters({"*.cpp"});
dir.setFilter(QDir::Files);
dir.setSorting(QDir::Name);

QDirIterator it(dir);
```

此构造函数会使用 `dir` 的名称过滤器和常规过滤器，但会**忽略排序设置**。`QDirIterator` 不保证枚举顺序，也不能反向或随机访问。若业务需要稳定排序，例如生成可重复的构建清单，应收集结果后自行排序，或使用能提供所需排序语义的方案。

## 4. 递归与符号链接：便利选项也是安全边界

```cpp
const auto flags = QDirIterator::Subdirectories;
QDirIterator it(root, QDir::Files, flags);
```

`Subdirectories` 会递归进入子目录。若再叠加 `FollowSymlinks`，则会跟随子目录符号链接：

```cpp
const auto flags = QDirIterator::Subdirectories
                 | QDirIterator::FollowSymlinks;
```

Qt 会检测并忽略典型的目录符号链接环，例如链接回 `.` 或 `..`，避免明显的无限循环。但这不等于可以把它当成安全的“限制在根目录内”扫描器：

- 链接可以指向根目录外的真实目录；
- 扫描期间文件系统可能变化；
- 权限、挂载点、网络文件系统和平台差异都会影响看到的内容；
- 依赖路径字符串前缀进行安全校验容易被符号链接绕过。

导入用户提供目录、清理文件或执行带权限影响的操作时，应将真实路径规范化，逐项验证其仍位于允许根目录内，并采用最小权限与明确的删除策略。枚举成功不代表随后打开、读取或删除仍安全。

若要列出指向不存在目标的符号链接，过滤器中必须包含 `QDir::System`。这与 `FollowSymlinks` 不同：前者决定是否把这类系统条目列出来，后者决定递归时是否进入可跟随的目录链接。

## 5. 迭代不是目录快照

`QDirIterator` 遍历期间，其他进程或线程可以创建、删除、重命名条目，改变权限或替换符号链接。它不会提供一个原子、一致、可重复的目录树快照。

因此应把每个条目都视为“发现时的线索”，在实际使用前再次验证：

```cpp
while (it.hasNext()) {
    const QFileInfo info = it.nextFileInfo();
    if (!info.isFile())
        continue;

    QFile file(info.filePath());
    if (!file.open(QIODevice::ReadOnly))
        continue; // 文件可能刚消失或权限刚被改变

    consume(file);
}
```

`QDirIterator` 没有错误码 API 来区分“目录为空”“路径无效”“权限不足”“扫描中断”等情况。需要可审计的错误报告时，应在扫描前主动检查根目录，在读取每个文件时处理 `QFile` 的错误，并为新实现评估 `QDirListing` 或更底层的系统 API。

## 6. `next()` 还是 `nextFileInfo()`

```cpp
while (it.hasNext()) {
    const QString path = it.next();
    // 只需要路径时很好。
}
```

```cpp
while (it.hasNext()) {
    const QFileInfo info = it.nextFileInfo();
    // 需要类型、大小、权限、时间或符号链接信息时更直接。
}
```

`nextFileInfo()` 从 Qt 6.3 起提供。若下一步无论如何都要构造 `QFileInfo`，优先使用它能让意图更明确，也避免先取路径再重复构造文件信息对象。

当前条目推进后，`fileName()` 返回只有最后一级名称，`filePath()` 返回当前条目的完整路径，`fileInfo()` 返回当前条目的文件信息。递归遍历时，单独使用 `fileName()` 很容易失去上下文；用于实际访问文件时优先 `filePath()` 或 `fileInfo().filePath()`。

## 7. 常见误区

| 误区 | 为什么会出问题 | 应该怎样做 | 使用时重点注意 |
| --- | --- | --- | --- |
| 在新模块直接选 `QDirIterator` | Qt 6.11 已标记弃用，未来可能移除 | 新代码使用 `QDirListing` | 维护旧调用时同时规划迁移 |
| 以为 `QDir` 的 sorting 会生效 | 迭代器忽略 `QDir` 排序设置 | 收集后按业务键排序 | 文件系统原始枚举顺序不稳定 |
| 不调用 `hasNext()` 直接 `next()` | 到末尾只会得到空结果，错误更隐蔽 | 始终写标准 while 循环 | 空路径不应继续传给文件操作 |
| 递归时只记录 `fileName()` | 同名文件可能来自不同子目录 | 保存完整 `filePath()` 或 `QFileInfo` | 单个文件名只适合显示 |
| 打开 `FollowSymlinks` 就认为安全 | 链接能跨出根目录，文件系统还能并发变化 | 对安全敏感操作验证真实路径和授权范围 | 环检测不等于目录沙箱 |
| 假定枚举出的文件一定还能打开 | 条目可能在扫描后被删除或权限改变 | 打开时重新检查并处理失败 | 这是典型 TOCTOU 场景 |
| 想靠它报告所有扫描错误 | 类没有完整错误诊断 API | 在根目录和每次文件操作处分别记录错误 | 空结果不等同扫描成功 |

## API 速查表
### 8.1 枚举与标志

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 标志 | `NoIteratorFlags` | 默认非递归、不跟随符号链接的遍历方式 | 只枚举所给目录层级，具体条目仍受 `QDir::Filters` 限制 |
| 标志 | `Subdirectories` | 递归枚举所有子目录中的条目 | 目录树很大时耗时和 I/O 很高，不能在 GUI 主线程无节制运行 |
| 标志 | `FollowSymlinks` | 在递归模式下进入目录符号链接 | 只和 `Subdirectories` 组合才有意义；可能遍历根目录外的位置 |
| 标志类型 | `IteratorFlags` | 存储多个 `IteratorFlag` 的按位或组合 | 使用 C++ 按位或运算符组合，例如递归加跟随符号链接 |

### 8.2 构造、推进和当前条目

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDirIterator(const QDir &dir, IteratorFlags flags = NoIteratorFlags)` | 使用 QDir 的路径、名称过滤和条目过滤构造迭代器 | 忽略 `dir` 的 sorting；不要依赖顺序 |
| 构造 | `QDirIterator(const QString &path, IteratorFlags flags = NoIteratorFlags)` | 枚举给定路径，使用默认 QDir 过滤规则 | 路径无效或不可访问时可能表现为空结果，需自行预检和记录 |
| 构造 | `QDirIterator(const QString &path, QDir::Filters filters, IteratorFlags flags = NoIteratorFlags)` | 用指定条目过滤器枚举路径 | `filters` 控制文件、目录、隐藏项等；它不等于名称模式 |
| 构造 | `QDirIterator(const QString &path, const QStringList &nameFilters, QDir::Filters filters = QDir::NoFilter, IteratorFlags flags = NoIteratorFlags)` | 同时按通配名称和条目属性过滤 | 名称模式不是正则；找文件通常加 `QDir::Files` |
| 析构 | `~QDirIterator()` | 释放迭代器内部扫描资源 | 不拥有由构造参数传入的 QDir 或字符串 |
| 推进判断 | `hasNext() const` | 判断是否存在尚未读取的下一个条目 | 正常推进前必须调用；文件系统变化仍可能影响之后操作 |
| 推进 | `next()` | 前进到下一个条目并返回其完整路径 | 末尾返回空 QString；只需要路径时使用 |
| 推进 | `nextFileInfo()` | 前进到下一个条目并返回其 QFileInfo | Qt 6.3 起；需要元数据时优先它，末尾返回空 QFileInfo |
| 当前条目 | `fileName() const` | 返回当前条目的最后一级名称 | 递归扫描中不唯一，不适合定位实际文件 |
| 当前条目 | `filePath() const` | 返回当前条目的完整路径 | 实际打开前仍要处理删除、权限变化和符号链接问题 |
| 当前条目 | `fileInfo() const` | 返回当前条目的 QFileInfo | 这是一个观察值，不保证稍后仍与文件系统一致 |
| 根路径 | `path() const` | 返回迭代器构造时的基础目录 | 它不是当前递归子目录，也不是当前条目路径 |

## 9. 维护遗留代码时的迁移原则

```cpp
// 旧：可维护，但不要在新接口中继续扩散。
QDirIterator it(root, {"*.qml"}, QDir::Files,
                QDirIterator::Subdirectories);

// 新：优先学习并采用 QDirListing 的范围式枚举模型。
```

迁移时不要机械地把构造函数名称替换掉。先写清楚旧代码真正依赖的行为：是否递归、是否包含隐藏文件、是否接受符号链接、是否需要稳定排序、是否要报告权限失败。把这些决定显式映射到新接口，迁移才不会在“看起来能编译”的情况下悄悄改变扫描结果。
