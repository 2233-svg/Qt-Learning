# Qt QDirListing::DirEntry 深入笔记

> 适用版本：Qt 6.11  
> 头文件：`#include <QDirListing>`  
> 所属模块：`Qt6::Core`  
> 相关类：`QDirListing`、`QFileInfo`、`QFileDevice`、`QTimeZone`

## 1. 它解决什么问题：表示当前枚举到的一个目录条目

`QDirListing::DirEntry` 是 `QDirListing` 迭代过程中返回的条目对象。它提供一组类似 `QFileInfo` 的查询 API，用来读取当前条目的名称、路径、类型、权限、大小和时间。

```cpp
for (const auto &entry : QDirListing(root)) {
    qDebug() << entry.fileName() << entry.size();
}
```

它的价值在于：不必为每个目录项立刻构造完整 `QFileInfo`。如果你只需要文件名，`entry.fileName()` 可能直接使用枚举过程已有的信息；只有当你询问大小、时间或调用 `fileInfo()` 时，才可能触发额外元数据查询。

| 你要做什么 | 优先用什么 | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 按文件名筛选 | `fileName()`、`suffix()` | 读取名称相关字段 | 通常比先 `fileInfo()` 更轻 |
| 打开文件 | `filePath()` 加 `QFile` | 用枚举路径执行实际 I/O | 打开时仍必须处理文件已消失或权限变化 |
| 保留条目信息到循环外 | 拷贝 `QString` 或 `QFileInfo` | 保存稳定的值对象 | 不要保存 `const DirEntry &` |
| 查询多个元数据字段 | `fileInfo()` | 得到完整 QFileInfo 值 | 可能更方便，但也可能更重 |
| 安全边界检查 | `canonicalFilePath()` 加额外验证 | 尝试获得规范真实路径 | 失败可能为空，且仍不能消除 TOCTOU |

## 2. 生命周期：在当前迭代步内消费它

`QDirListing::const_iterator` 解引用返回的是 `const DirEntry &`。它属于当前迭代器状态，不是一个适合长期保存的独立实体。

```cpp
QStringList paths;

for (const auto &entry : QDirListing(root)) {
    paths.append(entry.filePath()); // 复制需要的值
}
```

不要这样写：

```cpp
const QDirListing::DirEntry *saved = nullptr;
for (const auto &entry : QDirListing(root)) {
    saved = &entry; // 不要保存这个地址到循环外
}
```

迭代器推进后，前一次解引用得到的引用不应继续代表那个旧文件。若你需要缓存后续处理队列，保存 `filePath()`、`absoluteFilePath()` 或 `fileInfo()` 的返回值，而不是保存 `DirEntry` 引用。

`DirEntry` 也不是“文件已经锁定”的证明。扫描与后续使用之间，文件系统可能改变；实际打开、读取、写入或删除时仍要重新处理失败。

## 3. 直接查询和 `fileInfo()` 的取舍

```cpp
for (const auto &entry : QDirListing(root, QDirListing::IteratorFlag::Recursive)) {
    if (entry.fileName().endsWith(".conf"_L1)) {
        consume(entry.filePath());
    }
}
```

上面只按名称和路径筛选，直接用 `DirEntry` 成员更合适。下面需要多项元数据，把它转成 `QFileInfo` 会让代码更集中：

```cpp
for (const auto &entry : QDirListing(root)) {
    const QFileInfo info = entry.fileInfo();
    if (info.isFile() && info.size() > maxBytes) {
        reportLargeFile(info.absoluteFilePath(), info.size());
    }
}
```

不要机械地“为了安全”每次都先 `fileInfo()`。`QFileInfo` 只是某个时刻观察到的元数据；如果之后还要打开文件，真正安全的检查仍应在打开和使用点完成。

## 4. 路径 API：字符串形态不同，安全含义也不同

### 4.1 `filePath()` 与 `absoluteFilePath()`

`filePath()` 返回当前条目的路径，通常与构造 `QDirListing` 时传入的路径形态相关。`absoluteFilePath()` 返回绝对路径，但并不代表所有符号链接都已经解析。

```cpp
const QString path = entry.filePath();
QFile file(path);
if (!file.open(QIODevice::ReadOnly))
    return;
```

这是最常见的实际使用方式：把路径交给文件对象，并在打开处处理失败。

### 4.2 `canonicalFilePath()`

`canonicalFilePath()` 会尝试解析符号链接并得到规范路径。目标不存在、权限不足或路径无法规范化时，可能返回空字符串。

```cpp
const QString realPath = entry.canonicalFilePath();
if (realPath.isEmpty())
    return;
```

它常用于判断条目真实位置是否还在某个授权根目录内。但即便 canonical path 检查通过，到实际打开或删除之间仍可能发生替换；安全敏感场景还需要更严格的打开策略、权限控制和平台能力。

### 4.3 名称与后缀

`baseName()`、`completeBaseName()`、`suffix()`、`completeSuffix()` 的区别主要体现在多重后缀：

```text
archive.tar.gz
  baseName()         -> archive.tar
  completeBaseName() -> archive
  suffix()           -> gz
  completeSuffix()   -> tar.gz
```

用哪一个取决于业务：压缩包类型识别通常要看完整后缀，普通文档扩展名判断常看最后后缀。不要通过简单字符串截断重新实现这些规则。

`bundleName()` 是平台相关的 bundle 名称，主要在 macOS bundle 语义中有意义；跨平台文件扫描通常不要以它作为唯一标识。

## 5. 类型、权限和存在性：都是预检，不是保证

```cpp
if (entry.isFile() && entry.isReadable()) {
    QFile file(entry.filePath());
    if (file.open(QIODevice::ReadOnly)) {
        consume(file);
    }
}
```

`isFile()`、`isDir()`、`isSymLink()`、`exists()`、`isReadable()`、`isWritable()`、`isExecutable()` 反映的是查询时的文件系统状态。它们可以帮助你跳过明显不合适的条目，但不能保证下一步操作一定成功。

常见的正确处理方式是：

- 用 `FilesOnly`、`DirsOnly`、`ResolveSymlinks` 等 `QDirListing` 标志先缩小枚举范围；
- 在循环中用 `DirEntry` 查询做轻量筛选；
- 真正 I/O 时以 `QFile::open()`、删除 API 或其它系统调用的返回值为准；
- 对失败做可记录、可恢复的处理。

`isExecutable()` 只表示当前环境认为它可执行，不代表这个文件可信或可以安全运行。不可信目录扫描器不要把可执行属性当成执行许可。

## 6. 时间和大小：文件系统能力会影响结果

`size()` 返回条目大小。对常规文件最直观；对目录、设备、特殊文件或正在写入的文件，其含义可能随平台和文件系统变化。

时间 API 都要求传入 `QTimeZone`：

```cpp
const QTimeZone utc = QTimeZone::UTC;
const QDateTime modified = entry.lastModified(utc);
if (modified.isValid()) {
    record(modified);
}
```

- `birthTime()`：文件创建时间，并非所有文件系统都支持；
- `metadataChangeTime()`：元数据变化时间，不等同于内容修改时间；
- `lastModified()`：内容最后修改时间；
- `lastRead()`：最后访问时间，系统可能关闭或延迟更新；
- `fileTime(type, tz)`：按 `QFileDevice::FileTime` 枚举查询任意一种时间。

返回的 `QDateTime` 可能无效。导入或同步系统不要把无效时间自动替换为当前时间；那会掩盖底层文件系统没有提供数据的事实。

## 7. 符号链接与过滤标志会改变类型判断

如果 `QDirListing` 使用了 `ResolveSymlinks`，某些过滤会按符号链接目标的类型来决定是否列出。例如 `FilesOnly` 加 `ResolveSymlinks` 会把指向常规文件的链接也列出来。

但 `entry.isSymLink()` 仍可帮助识别当前条目本身是不是链接。你需要同时明确两件事：

| 问题 | 相关设置或 API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 是否把链接按目标类型过滤 | `ResolveSymlinks` | 决定列举时怎样看待符号链接 | 坏链接默认被排除，除非加 `IncludeBrokenSymlinks` |
| 是否递归进入目录链接 | `FollowDirSymlinks` | 决定递归扫描是否穿过目录链接 | 只有和 `Recursive` 组合才有效 |
| 当前条目本身是不是链接 | `isSymLink()` | 查询条目链接属性 | 不能单独说明目标是否存在 |
| 真实目标路径是什么 | `canonicalFilePath()` | 尝试解析并规范化目标 | 失败可能为空，且要处理 TOCTOU |

## 8. 常见误区

| 误区 | 为什么会出问题 | 应该怎样做 | 使用时重点注意 |
| --- | --- | --- | --- |
| 把 `DirEntry` 引用存到容器里 | 它依赖当前迭代状态 | 保存路径字符串或 `QFileInfo` 值 | 迭代器推进后旧引用不可靠 |
| 先 `exists()` 再无条件读取 | 文件可能在检查后被删除或替换 | 读取时检查 `QFile::open()` 结果 | 这是 TOCTOU 竞态 |
| 认为 `absoluteFilePath()` 已解析链接 | 绝对路径不等于 canonical path | 需要真实路径时调用 `canonicalFilePath()` | canonical 为空也要处理 |
| 用 `isReadable()` 代替错误处理 | 权限可在下一刻变化 | 预检后仍以实际 I/O 返回值为准 | 网络文件系统上尤其明显 |
| 每个条目都调用 `fileInfo()` | 可能触发不必要的元数据查询 | 只查需要的 `DirEntry` 成员 | 大目录下性能差异会被放大 |
| 将无效时间当成当前时间 | 文件系统可能根本不支持该时间 | 保留“时间未知”的业务状态 | 同步和备份软件尤其要谨慎 |

## API 速查表
### 9.1 转完整信息与名称拆分

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 元数据 | `fileInfo() const` | 返回当前条目的 `QFileInfo` 值 | 需要多项 QFileInfo 能力时使用；可能比直接查询更重 |
| 名称 | `fileName() const` | 返回最后一级名称 | 高频名称筛选优先用它；递归扫描中名称不唯一 |
| 名称 | `baseName() const` | 返回去掉最后一个后缀后的名称 | `archive.tar.gz` 会得到 `archive.tar` |
| 名称 | `completeBaseName() const` | 返回去掉完整后缀链后的名称 | `archive.tar.gz` 会得到 `archive` |
| 名称 | `suffix() const` | 返回最后一个后缀 | 不包含点号；无后缀时为空 |
| 名称 | `completeSuffix() const` | 返回完整后缀链 | 适合识别 `tar.gz` 这类复合格式 |
| 名称 | `bundleName() const` | 返回平台 bundle 名称 | 主要用于 macOS bundle 语义，跨平台不要依赖 |

### 9.2 路径、类型和权限

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 路径 | `filePath() const` | 返回当前枚举条目的路径 | 常用于交给 `QFile`；打开时仍需处理失败 |
| 路径 | `canonicalFilePath() const` | 返回解析符号链接后的规范路径 | 可能为空；安全检查后仍不能消除并发替换 |
| 路径 | `absoluteFilePath() const` | 返回绝对路径 | 不代表符号链接已解析 |
| 路径 | `absolutePath() const` | 返回所在目录的绝对路径 | 仅路径计算，不能证明目录可访问 |
| 类型 | `isDir() const` | 判断条目是否为目录 | `ResolveSymlinks` 会影响链接的过滤语义 |
| 类型 | `isFile() const` | 判断条目是否为常规文件 | 真正读取前仍以打开结果为准 |
| 类型 | `isSymLink() const` | 判断条目本身是否为符号链接 | 目标是否存在要结合 `exists()` 或 canonical path |
| 存在性 | `exists() const` | 判断条目或目标是否存在 | 只能作为预检，不能保证下一步操作 |
| 可见性 | `isHidden() const` | 判断条目是否隐藏 | 隐藏规则带平台差异，不是安全属性 |
| 权限 | `isReadable() const` | 判断当前用户是否可读 | 实际读取仍可能失败 |
| 权限 | `isWritable() const` | 判断当前用户是否可写 | 实际写入还受目录、锁和并发变化影响 |
| 权限 | `isExecutable() const` | 判断当前用户是否可执行 | 可执行不等于可信，不要自动运行不可信文件 |

### 9.3 大小与时间

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 大小 | `size() const` | 返回条目大小字节数 | 常规文件最可靠；特殊文件和并发写入文件需谨慎解释 |
| 时间 | `fileTime(QFileDevice::FileTime type, const QTimeZone &tz) const` | 按指定时间类型查询文件时间 | 传明确时区，检查返回的 `QDateTime` 是否有效 |
| 时间 | `birthTime(const QTimeZone &tz) const` | 返回创建时间 | 并非所有文件系统都提供 |
| 时间 | `metadataChangeTime(const QTimeZone &tz) const` | 返回元数据变化时间 | 不是内容修改时间 |
| 时间 | `lastModified(const QTimeZone &tz) const` | 返回内容最后修改时间 | 并发写入时只是某个观察点 |
| 时间 | `lastRead(const QTimeZone &tz) const` | 返回最后访问时间 | 系统可能关闭或延迟访问时间更新 |

## 10. 实用模式：轻量筛选，使用点再确认

```cpp
using F = QDirListing::IteratorFlag;

void collectReadableConfigs(const QString &root, QStringList &out)
{
    QDirListing listing(root, {"*.conf"}, F::FilesOnly | F::Recursive);

    for (const auto &entry : listing) {
        if (!entry.isReadable())
            continue;

        QFile file(entry.filePath());
        if (!file.open(QIODevice::ReadOnly))
            continue;

        out.append(entry.filePath());
    }
}
```

这里 `isReadable()` 只是减少无意义的打开尝试，`QFile::open()` 才是真正的判定点。这个思路同样适用于写入、删除、上传和索引：`DirEntry` 帮你快速看到“候选对象像什么”，真正动作必须处理文件系统当下的结果。
