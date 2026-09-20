# Qt QFileInfo 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QFileInfo>`  
> 所属模块：`Qt6::Core`  
> 类型性质：值类型、隐式共享、reentrant、可比较  
> 相关类型：`QFile`、`QDir`、`QFileDevice`、`QFileInfoList`

## 1. QFileInfo 解决什么问题

`QFileInfo` 用一个跨平台的值类型表示“某个路径对应的文件系统信息”。它把路径拆分、存在性、类型、权限、所有者、大小、时间和链接目标等查询集中到一个对象中：

```text
路径
  |
  v
QFileInfo
  ├─ 路径拆分：fileName / path / suffix
  ├─ 路径变换：absolute / canonical
  ├─ 类型判断：file / dir / symlink / other
  ├─ 元数据：size / time / owner / permissions
  └─ 缓存控制：caching / refresh / stat
```

它适合：

- 在文件列表、属性面板和导入对话框中展示文件信息；
- 在扫描目录时判断文件类型、扩展名、大小和修改时间；
- 解析符号链接、junction 和平台特有文件类型；
- 在工作线程预取元数据，再把轻量的 `QFileInfo` 值传给 UI 线程。

它不负责：

- 打开、读取或写入文件内容；
- 创建目录、复制、重命名或删除文件；
- 监视文件变化；
- 对不可信路径提供安全授权；
- 保证查询结果在下一次操作时仍然新鲜。

`QFileInfo` 是值类型，不继承 `QObject`，也不参与对象树。它使用隐式共享，复制对象通常很便宜；真正访问文件系统的查询仍然可能有成本。

## 2. 路径文本、文件系统项和元数据快照

`QFileInfo` 保存的是路径及其查询结果。它不是文件本身，也不是一个打开的文件句柄：

```cpp
QFileInfo info("config/settings.ini");

const QString path = info.filePath();
const bool exists = info.exists();
const qint64 bytes = info.size();
```

构造 `QFileInfo` 不会打开文件，也不会锁定路径。其他进程可以在对象创建之后：

- 删除或替换该路径；
- 修改大小、权限或时间；
- 把普通文件换成符号链接；
- 让原来的符号链接变成断链。

因此，`QFileInfo` 的信息应理解为查询时的快照，而不是持续同步的监视器。需要判断最新状态时调用 `refresh()`，但 `refresh()` 和随后操作之间仍存在竞态。

```cpp
QFileInfo info(path);
info.refresh();

if (info.exists()) {
    // 这里仍不能保证下一行打开时文件还存在
    QFile file(info.filePath());
}
```

真正执行打开、读取、写入、删除等动作时，仍然要检查动作本身的返回值。不要把“`exists()` 返回 true”当成授权或成功保证。

## 3. 构造和赋值

常见构造方式：

```cpp
QFileInfo empty;
QFileInfo fromString(QStringLiteral("data/report.csv"));
QFileInfo fromDevice(file);
QFileInfo fromDir(QDir("/var/log"), QStringLiteral("app.log"));
```

Qt 6.0 起，启用 C++17 filesystem 支持时还可以使用 `std::filesystem::path`。`QFileInfo` 的大多数构造函数默认是 `explicit`，这是有意的：构造和后续元数据查询可能有成本，不能让字符串在表达式中悄悄变成文件信息对象。

兼容宏 `QT_IMPLICIT_QFILEINFO_CONSTRUCTION` 可以改变部分构造函数的隐式性，但官方不建议新代码依赖这种模式。显式写出 `QFileInfo(path)` 更能表达“这里要进行文件信息查询”。

```cpp
QFileInfo a(path);
QFileInfo b = a;                 // 便宜的隐式共享复制
QFileInfo c = std::move(b);      // 移动

c.setFile(otherPath);
c.swap(a);
```

`setFile()` 会让同一个对象改为表示新的路径。它不会移动或重命名磁盘上的文件，也不保证旧缓存和新路径之间有任何关联。

## 4. 路径的四种视角

### 4.1 原始路径：`filePath()` 和 `path()`

- `filePath()` 返回对象保存的原始文件路径；
- `path()` 返回原始路径中的目录部分；
- 二者都可以是相对路径；
- 它们主要描述调用方传入的路径文本，不等同于规范化后的真实路径。

```cpp
QFileInfo info("logs/../logs/app.log");

qDebug() << info.filePath(); // 仍保留对象保存的路径语义
qDebug() << info.path();
```

相对路径相对于当前工作目录，而不是相对于可执行文件所在目录。需要应用目录、配置目录或缓存目录时，应使用 `QCoreApplication`、`QStandardPaths` 等 API 得到明确根目录。

### 4.2 绝对路径：`absoluteFilePath()` 和 `absolutePath()`

绝对路径会把相对路径转换为绝对路径，但不一定解析符号链接，也不要求文件存在：

```cpp
QFileInfo info("logs/app.log");

const QString absoluteFile = info.absoluteFilePath();
const QString absoluteDir = info.absolutePath();
```

绝对路径适合日志、界面展示和传给需要绝对路径的 API，但“绝对”不等于“规范化”和“真实目标”。

空的 `filePath()` 上调用 `absolutePath()` 的行为未定义。对默认构造的空对象，先检查或设置有效路径，不要把空对象当作当前目录。

### 4.3 规范路径：`canonicalFilePath()` 和 `canonicalPath()`

canonical 路径会解析 `.`、`..` 和符号链接，返回绝对规范路径：

```cpp
QFileInfo info("links/current.log");
const QString realPath = info.canonicalFilePath();
```

对应项不存在、路径中有无法解析的部分或符号链接断裂时，canonical 路径返回空字符串。它适合比较“当前实际解析到哪里”、显示最终目标或做路径边界判断，但返回空值必须作为正常失败分支处理。

不要用字符串拼接模拟 canonical 解析，也不要把 `absoluteFilePath()` 当作符号链接解析结果。安全边界需要同时考虑符号链接、junction、挂载点和检查与操作之间的竞态。

### 4.4 `dir()` 和 `absoluteDir()`

`dir()` 返回包含该路径的 `QDir`，通常沿用原始路径语义；`absoluteDir()` 返回对应的绝对目录。它们适合继续进行目录枚举和路径拼接：

```cpp
const QDir parent = info.absoluteDir();
const QString sibling = parent.filePath("next.dat");
```

需要规范化真实目录时，应使用 `canonicalPath()` 或对目录本身构造 `QFileInfo` 后再判断。

## 5. Qt 资源路径和原生路径

以 `:` 开头的 Qt Resource System 路径被 Qt 视为 absolute，但它不是操作系统原生文件路径：

```cpp
QFileInfo resourceInfo(":/icons/save.png");

Q_ASSERT(resourceInfo.isAbsolute());
qDebug() << resourceInfo.isNativePath(); // 通常为 false
```

`isNativePath()` 判断路径是否能直接交给原生文件系统 API。资源路径、某些 Qt 虚拟文件系统路径和平台不支持的路径通常不是 native path。

这两个概念不要混淆：

- `isAbsolute()` 说的是 Qt 路径语义是否包含根；
- `isNativePath()` 说的是能否直接用于操作系统原生 API。

资源文件可以由 `QFile` 读取，但不能按普通磁盘文件期待其支持原生重命名、权限或内存映射。

## 6. 文件名和扩展名拆分

`QFileInfo` 提供四种常用拆分方式。以 `/tmp/archive.tar.gz` 为例：

| API | 返回值 |
| --- | --- |
| `fileName()` | `archive.tar.gz` |
| `baseName()` | `archive` |
| `completeBaseName()` | `archive.tar` |
| `suffix()` | `gz` |
| `completeSuffix()` | `tar.gz` |

规则重点：

- `fileName()` 不含目录；
- `baseName()` 取第一个 `.` 之前的部分；
- `completeBaseName()` 取最后一个 `.` 之前的部分；
- `suffix()` 取最后一个 `.` 之后的部分；
- `completeSuffix()` 取第一个 `.` 之后的部分；
- 对 `.bashrc` 这类名称，Qt 的规则是 base name 为空、suffix 为 `bashrc`；
- 目录路径以 `/` 结尾时，`fileName()` 可能为空。

```cpp
QFileInfo info("/tmp/archive.tar.gz");
qDebug() << info.baseName();         // archive
qDebug() << info.completeBaseName(); // archive.tar
qDebug() << info.suffix();            // gz
qDebug() << info.completeSuffix();    // tar.gz
```

扩展名只是文件名文本规则，不是文件类型认证。不要因为 `suffix() == "jpg"` 就假设内容一定是 JPEG，也不要用扩展名代替 MIME 检测或协议解析。

## 7. 存在性、文件类型和特殊项

### 7.1 `exists()`

```cpp
QFileInfo info(path);
if (!info.exists())
    return;
```

`exists()` 检查当前路径对应的文件系统项。断链符号链接返回 false，因为目标不存在；它不会告诉你失败是因为路径不存在、权限不足还是其他系统错误。

静态形式：

```cpp
if (QFileInfo::exists(path)) {
    // 只检查存在性
}
```

`QFileInfo::exists(path)` 通常比先构造 `QFileInfo(path)` 再调用 `exists()` 更快，适合只需要一次存在性判断的场景。但它仍然只是瞬时查询，不能消除 TOCTOU。

### 7.2 普通文件、目录和其他项

```cpp
if (info.isFile()) {
    // 普通文件语义
} else if (info.isDir()) {
    // 目录
} else if (info.isOther()) {
    // Qt 6.10 起：其他特殊文件系统项
}
```

- `isFile()` 判断普通文件；
- `isDir()` 判断目录；
- `isOther()` 在 Qt 6.10 起用于不是目录、普通文件或符号链接的特殊项；
- 不存在的项和断链符号链接的 `isOther()` 返回 false。

设备文件、FIFO、socket、挂载点和平台特殊项不要按普通文件随意打开。对不可信路径，先判断类型可以改善用户体验，但实际打开仍需处理失败。

### 7.3 符号链接、shortcut、alias 和 junction

`isSymLink()` 与 `isSymbolicLink()` 是同义 API，用于判断符号链接。`isShortcut()`、`isAlias()`、`isJunction()` 等是平台相关类型判断：

```cpp
if (info.isSymLink()) {
    qDebug() << info.symLinkTarget();
}

if (info.isJunction()) {
    qDebug() << info.junctionTarget();
}
```

普通属性 getter（例如 `size()`、权限和时间）对符号链接通常读取链接目标的信息，而不是链接本身。需要区分链接文本和目标时，要使用专门的链接 API。

`isRoot()` 判断是否为根目录，`isBundle()` 主要服务于支持 bundle 概念的平台。它们不应被当作所有平台都有完全相同语义的通用文件类型。

## 8. 符号链接和 junction 的两个目标 API

### 8.1 `symLinkTarget()`

`symLinkTarget()` 返回解析后的符号链接目标路径，通常是绝对路径。目标本身可以不存在，因此“拿到字符串”不等于目标可打开：

```cpp
const QString target = info.symLinkTarget();
if (!target.isEmpty()) {
    QFileInfo targetInfo(target);
    qDebug() << targetInfo.exists();
}
```

### 8.2 `readSymLink()`

Qt 6.6 起，`readSymLink()` 返回链接中保存的原始目标文本。它不会把相对目标自动解析成相对于链接目录的绝对路径：

```cpp
QFileInfo linkInfo("links/current");
const QString rawTarget = linkInfo.readSymLink();
const QString resolvedTarget = linkInfo.symLinkTarget();
```

这两个 API 解决不同问题：

| API | 结果 |
| --- | --- |
| `readSymLink()` | 链接存储的原始目标文本，保留相对性 |
| `symLinkTarget()` | 解析后的目标路径，便于继续查询 |

### 8.3 Windows junction

Qt 6.2 起，`junctionTarget()` 用于解析 NTFS junction，返回绝对目录路径，但不保证目标目录存在。普通符号链接和 junction 不能混用同一套安全假设。

在删除、导出、归档或限制目录边界时，必须考虑链接可能指向预期目录之外。`QFileInfo` 只提供信息，不替你执行安全授权。

## 9. 元数据：大小、时间、所有者和权限

### 9.1 文件大小

```cpp
const qint64 bytes = info.size();
```

文件不存在或无法获取大小时，`size()` 返回 0。因此不能单独用 `size() == 0` 区分：

- 真实的空文件；
- 文件不存在；
- 权限不足；
- 查询失败。

先用 `exists()` 或实际打开结果区分状态，再解释大小。

### 9.2 时间

常用快捷 API：

```cpp
const QDateTime created = info.birthTime();
const QDateTime changed = info.metadataChangeTime();
const QDateTime modified = info.lastModified();
const QDateTime accessed = info.lastRead();
```

也可以使用通用形式：

```cpp
const QDateTime time =
    info.fileTime(QFile::FileModificationTime);
```

无法取得某种时间时返回 invalid `QDateTime`。创建时间、访问时间和元数据变化时间的可用性取决于平台和文件系统，不能假设四种时间都存在。

Qt 6.6 起，时间 API 提供带 `QTimeZone` 的重载：

```cpp
const QDateTime utcModified =
    info.lastModified(QTimeZone::UTC);
```

跨机器比较或持久化时间时，优先使用 UTC 或明确的时区；界面展示再转换为用户本地时区。

### 9.3 所有者

```cpp
const QString user = info.owner();
const uint userId = info.ownerId();
const QString group = info.group();
const uint groupId = info.groupId();
```

Unix 上按名称查询所有者或组可能涉及系统数据库，可能比读取基本属性慢。Windows 上的 NTFS 权限检查如果未启用，所有者信息可能为空。查询失败或平台不支持时，不要把空字符串解释成“没有所有者”。

### 9.4 权限

`permission()` 可以检查一个或多个权限位：

```cpp
if (info.permission(QFile::ReadOwner | QFile::ReadUser))
    qInfo() << "read permission is present";

const QFile::Permissions all = info.permissions();
```

权限是 Qt 对平台能力的抽象：

- Unix 权限位比较接近 mode bits；
- Windows 结果可能主要映射只读属性或可访问性；
- ACL、沙箱和安全软件不一定完整反映在简单权限位中；
- Windows NTFS 权限查询默认可能关闭，结果不能过度解读；
- Qt 6.6 起旧的全局 NTFS 权限查询开关已 deprecated，跨平台代码不应依赖旧开关名称。

`QFileInfo` 查询到可写，不代表下一次写入一定成功；真正写入仍需检查 `QFile::open()` 和 `write()`。

## 10. 缓存、refresh 和 stat

### 10.1 默认缓存

`QFileInfo` 默认启用缓存。一次查询得到的文件属性可能被缓存，之后其他进程对文件的修改不会自动推送到这个对象：

```cpp
QFileInfo info(path);
const qint64 firstSize = info.size();

// 其他进程可能在这里修改文件
const qint64 cachedSize = info.size();
```

缓存适合目录列表、文件模型和短时间内重复展示同一批属性的场景；它不适合充当文件系统监视器。

### 10.2 `setCaching(false)`

```cpp
info.setCaching(false);
```

禁用缓存后，读取属性会更积极地访问文件系统，但这仍不能形成原子快照：不同属性查询之间文件可能被修改，而且每次查询可能更慢。不要为了“实时”而无条件关闭缓存，先根据工作负载选择策略。

### 10.3 `refresh()`

```cpp
info.refresh();
```

`refresh()` 使后续属性查询重新访问文件系统。它适合在已知文件可能变化后刷新对象，但不会保证刷新后路径在后续操作中仍然存在。

### 10.4 `stat()`

Qt 6.0 起，`stat()` 一次读取所有文件属性：

```cpp
QFileInfo info(path);
info.stat();

const qint64 bytes = info.size();
const QDateTime modified = info.lastModified();
const auto permissions = info.permissions();
```

它适合在 worker 线程预取一组属性，然后把 `QFileInfo` 传给 UI 线程。值类型复制成本低，但不要把 `stat()` 误解为跨属性、跨进程的永恒一致快照；文件仍可能在调用返回后变化。

## 11. 相对路径、绝对路径和安全边界

### 11.1 `isRelative()`、`isAbsolute()`、`makeAbsolute()`

```cpp
QFileInfo info("reports/today.csv");
if (info.isRelative() && info.makeAbsolute()) {
    qDebug() << info.filePath();
}
```

- `isRelative()` 判断保存的路径是否为相对路径；
- `isAbsolute()` 是对应的反向判断；
- `makeAbsolute()` 把相对路径改成绝对路径并返回 true；
- 已经是绝对路径时，`makeAbsolute()` 返回 false。

`makeAbsolute()` 只改变对象保存的路径，不创建文件、不解析符号链接、不验证目标存在。

### 11.2 TOCTOU

下面的模式不能提供安全保证：

```cpp
QFileInfo info(userPath);
if (info.exists() && info.isFile()) {
    QFile file(userPath);
    file.open(QIODevice::ReadOnly);
}
```

检查和打开之间，攻击者或其他进程可能替换路径、插入符号链接或改变文件类型。对于不可信路径：

- 先确定允许的根目录和路径策略；
- 解析并检查符号链接、junction 和规范路径；
- 实际打开时仍检查返回值；
- 必要时使用平台提供的目录句柄、无跟随链接选项或沙箱机制；
- 不把 `QFileInfo` 的结果当作权限授予。

## 12. QFileInfo、QFile 和 QDir 的区别

| 类型 | 主要问题 |
| --- | --- |
| `QFileInfo` | 这个路径对应什么信息？是否存在？大小、时间、权限和类型是什么？ |
| `QFile` | 如何打开、读取、写入、复制、重命名、删除这个文件？ |
| `QDir` | 如何表示目录、拼接路径、列出目录项和进行目录操作？ |

一个常见组合是：

```cpp
QDir dir(root);
const QFileInfoList entries =
    dir.entryInfoList(QDir::Files | QDir::Dirs);

for (const QFileInfo &entry : entries) {
    qInfo() << entry.fileName()
            << entry.size()
            << entry.lastModified();
}
```

目录扫描适合使用 `QFileInfoList`。如果只需要文件名，`QDir` 的名称列表接口可能更轻；如果需要多个属性，直接请求 `QFileInfo` 可以减少重复构造。

## 13. 值语义、隐式共享和比较

`QFileInfo` 复制和移动支持值语义：

```cpp
QFileInfo first(path);
QFileInfo second = first;

// 两个对象可以独立刷新和改变所表示的路径
second.refresh();
```

隐式共享使复制便宜，但它不意味着底层文件系统查询免费，也不意味着两个对象会实时同步。修改一个对象的路径或刷新它，不应当被当作修改另一个对象。

`operator==` 比较两个 `QFileInfo` 是否引用同一个文件系统项，而不是简单比较路径字符串：

- 不同文本路径可能解析到同一个文件系统对象；
- 两个不同符号链接即使指向同一目标，也不应简单当成两个链接对象相等；
- Windows 长路径和短路径表示可能被视为不同项；
- 两个不存在项或空对象的比较结果不应作为业务逻辑依据。

如果业务真正需要比较路径文本，请显式比较 `filePath()`；如果需要比较规范目标，请先取得并验证 `canonicalFilePath()`，并处理空字符串。

## 14. filesystem API

Qt 6.0 起，启用 C++17 filesystem 支持时，`QFileInfo` 提供一组返回 `std::filesystem::path` 的包装：

```cpp
const std::filesystem::path nativePath =
    info.filesystemFilePath();
const std::filesystem::path absolutePath =
    info.filesystemAbsoluteFilePath();
const std::filesystem::path canonicalPath =
    info.filesystemCanonicalFilePath();
```

对应的路径、链接和 junction API 包括：

- `filesystemPath()`；
- `filesystemAbsolutePath()`；
- `filesystemCanonicalPath()`；
- `filesystemSymLinkTarget()`；
- `filesystemReadSymLink()`；
- `filesystemJunctionTarget()`。

这些函数只是把相应 QString 结果转换为 `std::filesystem::path`，不会改变路径是否存在、是否 canonical 或是否 native 的语义。Qt 6.2 起提供 junction 包装，Qt 6.6 起提供 `filesystemReadSymLink()`。

## 15. 常见使用场景

### 15.1 文件列表属性

```cpp
QFileInfo info(path);
info.stat();

ui->nameLabel->setText(info.fileName());
ui->sizeLabel->setText(QLocale().formattedDataSize(info.size()));
ui->modifiedLabel->setText(
    QLocale().toString(info.lastModified()));
```

UI 线程只拿已经准备好的 `QFileInfo` 或结果值，避免在大量目录项渲染时反复触发昂贵的所有者查询。

### 15.2 根据类型选择处理器

```cpp
QFileInfo info(path);
if (info.isDir()) {
    scanDirectory(info.absoluteFilePath());
} else if (info.isFile()) {
    importFile(info.absoluteFilePath());
} else if (info.isSymLink()) {
    showLink(info.readSymLink());
}
```

实际处理函数仍要对路径变化、权限和打开失败做异常分支。

### 15.3 规范化路径边界

在允许用户选择文件并限制在某个目录时，可以先取得 canonical 路径进行初步判断，但不要把这一步当成完整安全机制：

```cpp
const QString root = QFileInfo(rootPath).canonicalPath();
const QString candidate = QFileInfo(userPath).canonicalFilePath();

if (root.isEmpty() || candidate.isEmpty())
    return false;

const QString prefix = QDir(root).filePath(QString());
return candidate == root || candidate.startsWith(prefix);
```

真实安全实现还需要处理路径分隔符边界、junction、并发替换和平台原生打开选项。`QFileInfo` 只提供组成安全策略所需的信息。

## 16. API 逐项说明

### 16.1 构造、赋值和比较

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `QFileInfo()` | 创建空的文件信息对象。 | 没有有效路径；不要对空路径调用依赖路径的 API。 |
| `QFileInfo(QString)` | 用字符串路径表示一个文件系统项。 | 默认显式构造；不会打开或锁定文件。 |
| `QFileInfo(QFileDevice)` | 从文件设备的文件名构造信息对象。 | 读取的是设备关联路径，不是文件内容快照。 |
| `QFileInfo(QDir, QString)` | 用目录和相对文件名构造路径信息。 | 路径拼接遵循 QDir 语义；不创建文件。 |
| `QFileInfo(std::filesystem::path)` | 用标准库 filesystem 路径构造。 | Qt 6.0 起；需要相应 C++17 filesystem 支持。 |
| `QFileInfo(const QFileInfo &)` | 复制文件信息对象。 | 隐式共享，复制便宜；缓存不会变成实时监视。 |
| `~QFileInfo()` | 销毁文件信息值对象。 | 不会删除或关闭它所表示的文件；仍按值类型生命周期管理。 |
| `operator=` | 复制赋值。 | 让对象表示另一个路径及其缓存状态。 |
| move assignment | 移动赋值。 | 适合转移值对象；源对象仍可析构和重新赋值。 |
| `swap(QFileInfo &)` | 交换两个对象。 | `noexcept`；只交换值对象状态，不触碰文件系统。 |
| `operator==` | 比较是否引用同一个文件系统项。 | 不是简单字符串比较；不存在项的比较不要作为业务依据。 |

### 16.2 设置路径和存在性

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `setFile(QString)` | 让对象改为表示指定路径。 | 只修改对象，不移动或创建磁盘文件。 |
| `setFile(QFileDevice)` | 用文件设备的路径设置对象。 | 设备路径仍可能是相对路径或资源路径。 |
| `setFile(QDir, QString)` | 用目录和文件名设置对象。 | 不执行目录操作。 |
| `setFile(std::filesystem::path)` | 用标准库路径设置对象。 | Qt 6.0 起；转换不改变文件系统语义。 |
| `exists() const` | 判断当前路径对应项是否存在。 | 断链符号链接返回 false；是瞬时检查。 |
| `exists(QString)` | 静态检查指定路径是否存在。 | 单次检查通常更快；不能替代实际操作错误处理。 |
| `refresh()` | 清理缓存，使后续查询重新访问文件系统。 | 不提供锁或原子快照。 |
| `stat()` | 一次读取所有文件属性。 | Qt 6.0 起；适合批量预取，不是永恒快照。 |

### 16.3 路径和名称

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `filePath()` | 返回保存的原始文件路径。 | 可以相对；不一定存在或规范化。 |
| `absoluteFilePath()` | 返回绝对文件路径。 | 不一定解析符号链接；不要求存在。 |
| `canonicalFilePath()` | 返回解析链接、`.`、`..` 后的绝对路径。 | 项不存在或断链时返回空字符串。 |
| `filesystemFilePath()` | 以 `std::filesystem::path` 返回原始文件路径。 | Qt 6.0 起；只是类型转换。 |
| `filesystemAbsoluteFilePath()` | 以 filesystem 路径返回绝对文件路径。 | 仍不等于 canonical 路径。 |
| `filesystemCanonicalFilePath()` | 以 filesystem 路径返回规范文件路径。 | 规范路径为空时得到空 filesystem path。 |
| `fileName()` | 返回不含目录的文件名。 | 目录末尾带分隔符时可能为空。 |
| `baseName()` | 返回第一个点之前的名称部分。 | `.bashrc` 的 base name 为空。 |
| `completeBaseName()` | 返回最后一个点之前的名称部分。 | `archive.tar.gz` 得到 `archive.tar`。 |
| `suffix()` | 返回最后一个点之后的扩展名。 | 只是文本拆分，不是内容识别。 |
| `bundleName()` | 返回平台 bundle 名称。 | 平台相关，普通路径可能为空。 |
| `completeSuffix()` | 返回第一个点之后的扩展名整体。 | `archive.tar.gz` 得到 `tar.gz`。 |
| `path()` | 返回原始目录路径。 | 可以相对；空路径要谨慎。 |
| `absolutePath()` | 返回绝对目录路径。 | 空 `filePath()` 时行为未定义。 |
| `canonicalPath()` | 返回规范化绝对目录路径。 | 不存在或无法解析时返回空字符串。 |
| `filesystemPath()` | 以 filesystem 路径返回原始目录。 | Qt 6.0 起；语义对应 `path()`。 |
| `filesystemAbsolutePath()` | 以 filesystem 路径返回绝对目录。 | 语义对应 `absolutePath()`。 |
| `filesystemCanonicalPath()` | 以 filesystem 路径返回规范目录。 | 语义对应 `canonicalPath()`。 |
| `dir()` | 返回包含该项的 `QDir`。 | 适合继续拼接和枚举；不等于规范目录。 |
| `absoluteDir()` | 返回绝对目录的 `QDir`。 | 绝对不等于 canonical。 |

### 16.4 可访问性和路径形式

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `isReadable()` | 判断是否可读。 | 平台映射结果，不保证稍后打开成功。 |
| `isWritable()` | 判断是否可写。 | 不是写入授权，仍可能受 ACL、锁和竞态影响。 |
| `isExecutable()` | 判断是否可执行。 | 平台相关；目录和文件语义不同。 |
| `isHidden()` | 判断是否隐藏。 | Windows、Unix 和其他平台规则不同。 |
| `isNativePath()` | 判断能否直接用于原生 API。 | Qt 资源路径通常不是 native path。 |
| `isRelative()` | 判断保存的路径是否相对。 | 只描述路径形式。 |
| `isAbsolute()` | 判断保存的路径是否绝对。 | `:` 资源路径也可被视为 absolute。 |
| `makeAbsolute()` | 把相对路径改成绝对路径。 | 返回是否发生改变；不解析链接、不创建文件。 |

### 16.5 类型和链接

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `isFile()` | 判断是否为普通文件。 | 不存在项返回 false。 |
| `isDir()` | 判断是否为目录。 | 符号链接的目标语义要结合链接判断。 |
| `isSymLink()` | 判断是否为符号链接。 | 与 `isSymbolicLink()` 同义。 |
| `isSymbolicLink()` | 判断是否为符号链接。 | 适合需要更直观命名的代码。 |
| `isOther()` | 判断是否为其他特殊项。 | Qt 6.10 起；不存在项和断链返回 false。 |
| `isShortcut()` | 判断平台 shortcut 类型。 | 平台相关，不等同于普通符号链接。 |
| `isAlias()` | 判断平台 alias 类型。 | 主要是平台特有语义。 |
| `isJunction()` | 判断 NTFS junction。 | Windows 语义；其他平台通常为 false。 |
| `isRoot()` | 判断是否为根目录。 | 根的定义受平台路径规则影响。 |
| `isBundle()` | 判断是否为 bundle。 | 平台相关。 |
| `symLinkTarget()` | 返回解析后的符号链接目标。 | 目标可以不存在；不要忽略空结果。 |
| `readSymLink()` | 返回链接保存的原始目标文本。 | Qt 6.6 起；相对目标不会自动绝对化。 |
| `junctionTarget()` | 返回 junction 的绝对目标目录。 | Qt 6.2 起；不保证目标存在。 |
| `filesystemSymLinkTarget()` | 以 filesystem path 返回解析后的链接目标。 | Qt 6.0 起；语义对应 `symLinkTarget()`。 |
| `filesystemReadSymLink()` | 以 filesystem path 返回原始链接文本。 | Qt 6.6 起；保留相对性。 |
| `filesystemJunctionTarget()` | 以 filesystem path 返回 junction 目标。 | Qt 6.2 起；平台相关。 |

### 16.6 所有者、权限、大小和时间

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `owner()` | 返回所有者名称。 | 可能耗时或为空；平台支持不同。 |
| `ownerId()` | 返回所有者数值 ID。 | ID 语义平台相关。 |
| `group()` | 返回组名称。 | 可能耗时或为空。 |
| `groupId()` | 返回组数值 ID。 | 平台相关。 |
| `permission(QFile::Permissions)` | 检查一个或多个权限位。 | 支持 OR 组合；不代表完整 ACL。 |
| `permissions()` | 返回权限位组合。 | Windows 映射结果不要按 Unix 精确解读。 |
| `size()` | 返回文件大小。 | 失败或不存在也可能返回 0。 |
| `birthTime()` | 返回创建时间。 | 不支持时为 invalid `QDateTime`。 |
| `metadataChangeTime()` | 返回元数据变化时间。 | 平台和文件系统可用性不同。 |
| `lastModified()` | 返回内容修改时间。 | 用时区重载明确显示或比较时区。 |
| `lastRead()` | 返回最后访问时间。 | 访问时间可能被文件系统策略关闭或延迟更新。 |
| `fileTime(QFile::FileTime)` | 按枚举查询一种时间。 | 无法获取时返回 invalid 时间。 |
| `birthTime(QTimeZone)` | 按指定时区返回创建时间。 | Qt 6.6 起；UTC 适合跨机器比较。 |
| `metadataChangeTime(QTimeZone)` | 按指定时区返回元数据变化时间。 | Qt 6.6 起。 |
| `lastModified(QTimeZone)` | 按指定时区返回修改时间。 | Qt 6.6 起。 |
| `lastRead(QTimeZone)` | 按指定时区返回访问时间。 | Qt 6.6 起。 |
| `fileTime(QFile::FileTime, QTimeZone)` | 按枚举和时区查询时间。 | Qt 6.6 起；仍可能返回 invalid。 |

### 16.7 缓存控制和辅助类型

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `caching()` | 查询是否启用属性缓存。 | 默认通常开启；缓存不等于实时监视。 |
| `setCaching(bool)` | 开启或关闭属性缓存。 | 关闭可能增加系统调用；仍不提供原子快照。 |
| `refresh()` | 使后续查询更新属性缓存。 | 不能消除刷新与实际操作之间的竞态。 |
| `stat()` | 一次预取所有属性。 | 适合 worker 线程批量准备元数据。 |
| `QFileInfoList` | `QList<QFileInfo>` 的类型别名。 | 适合目录 API 返回多个文件信息对象。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 定位 | `QFileInfo` | 表示路径对应的文件系统信息。 | 值类型，不打开文件，不锁定路径。 |
| 构造 | `QFileInfo()` | 创建空对象。 | 空路径不适合直接做路径查询。 |
| 构造 | `QFileInfo(QString)` | 从 QString 路径创建对象。 | 默认显式；构造不会创建文件。 |
| 构造 | `QFileInfo(QFileDevice)` | 从文件设备路径创建对象。 | 表示设备关联路径，不读取内容。 |
| 构造 | `QFileInfo(QDir, QString)` | 从目录和文件名创建对象。 | 只拼出路径，不进行目录操作。 |
| 构造 | `QFileInfo(std::filesystem::path)` | 从标准库路径创建对象。 | Qt 6.0 起，需要 filesystem 支持。 |
| 复制 | `operator=` / move assignment | 复制或移动值对象。 | 隐式共享复制便宜，但查询仍可能有成本。 |
| 交换 | `swap()` | 交换两个对象状态。 | `noexcept`；不触碰磁盘。 |
| 比较 | `operator==` | 比较是否引用同一文件系统项。 | 不是路径字符串比较；不存在项不要依赖结果。 |
| 设置 | `setFile()` | 改变对象表示的路径。 | 不移动、不创建、不打开文件。 |
| 存在性 | `exists()` | 检查当前项是否存在。 | 断链返回 false；不能消除 TOCTOU。 |
| 存在性 | `QFileInfo::exists(path)` | 一次性检查指定路径。 | 通常更快；只适合简单存在性判断。 |
| 路径 | `filePath()` | 返回原始路径。 | 可相对、可为资源路径，不保证存在。 |
| 路径 | `absoluteFilePath()` | 返回绝对路径。 | 不一定解析符号链接。 |
| 路径 | `canonicalFilePath()` | 返回解析后的规范绝对路径。 | 不存在或断链时为空。 |
| 目录 | `path()` / `absolutePath()` | 返回原始或绝对目录路径。 | 空 `filePath()` 的 `absolutePath()` 行为未定义。 |
| 目录 | `canonicalPath()` | 返回规范目录路径。 | 解析失败时为空。 |
| 目录 | `dir()` / `absoluteDir()` | 返回相应的 QDir。 | absolute 不等于 canonical。 |
| 文件名 | `fileName()` | 返回不含目录的名称。 | 目录末尾分隔符可能得到空字符串。 |
| 文件名 | `baseName()` | 取第一个点之前。 | `.bashrc` 的 base name 为空。 |
| 文件名 | `completeBaseName()` | 取最后一个点之前。 | 适合处理多段扩展名。 |
| 扩展名 | `suffix()` | 取最后一个点之后。 | 只是文本规则，不是内容检测。 |
| 扩展名 | `completeSuffix()` | 取第一个点之后。 | `tar.gz` 会整体返回。 |
| 路径形式 | `isRelative()` / `isAbsolute()` | 判断相对或绝对路径。 | 资源路径 `:/...` 可被视为 absolute。 |
| 路径形式 | `makeAbsolute()` | 将相对路径改成绝对路径。 | 不解析链接，不验证存在。 |
| 原生性 | `isNativePath()` | 判断能否用于原生 API。 | Qt 资源路径通常为 false。 |
| 类型 | `isFile()` | 判断普通文件。 | 不存在项返回 false。 |
| 类型 | `isDir()` | 判断目录。 | 与符号链接目标语义结合使用。 |
| 类型 | `isSymLink()` / `isSymbolicLink()` | 判断符号链接。 | 两者同义。 |
| 类型 | `isOther()` | 判断其他特殊文件系统项。 | Qt 6.10 起；不存在项为 false。 |
| 类型 | `isShortcut()` / `isAlias()` | 判断平台特有链接类型。 | 跨平台语义不同。 |
| 类型 | `isJunction()` | 判断 NTFS junction。 | Windows 平台相关。 |
| 类型 | `isRoot()` / `isBundle()` | 判断根目录或 bundle。 | 平台路径模型不同。 |
| 链接 | `symLinkTarget()` | 返回解析后的链接目标。 | 目标可能不存在。 |
| 链接 | `readSymLink()` | 返回原始链接目标文本。 | Qt 6.6 起；不会自动绝对化。 |
| 链接 | `junctionTarget()` | 返回 junction 绝对目标。 | Qt 6.2 起；不保证存在。 |
| 元数据 | `size()` | 返回文件大小。 | 失败、不存在和空文件都可能得到 0。 |
| 元数据 | `birthTime()` | 返回创建时间。 | 可能无效。 |
| 元数据 | `lastModified()` | 返回内容修改时间。 | 用时区重载明确时区。 |
| 元数据 | `lastRead()` | 返回访问时间。 | 访问时间可能不更新或不可用。 |
| 元数据 | `metadataChangeTime()` | 返回元数据变化时间。 | 平台和文件系统支持不同。 |
| 元数据 | `fileTime()` | 按枚举查询时间。 | 无法取得时返回 invalid。 |
| 所有者 | `owner()` / `ownerId()` | 查询所有者名称或 ID。 | Unix 可能耗时，Windows 可能为空。 |
| 所有者 | `group()` / `groupId()` | 查询组名称或 ID。 | 平台相关。 |
| 权限 | `permission()` | 查询一个或多个权限位。 | 不等同完整 ACL，不保证实际操作成功。 |
| 权限 | `permissions()` | 返回权限位组合。 | Windows 结果不要按 Unix 精确解释。 |
| 缓存 | `caching()` | 查询是否缓存属性。 | 默认通常开启。 |
| 缓存 | `setCaching(bool)` | 开启或关闭缓存。 | 关闭缓存可能增加系统调用。 |
| 缓存 | `refresh()` | 刷新后续查询。 | 不提供文件锁或实时同步。 |
| 批量查询 | `stat()` | 一次预取全部属性。 | Qt 6.0 起；适合后台线程预取。 |
| filesystem | `filesystem*` API | 以 `std::filesystem::path` 暴露同一语义。 | 只是路径类型转换，版本和配置有要求。 |
| 列表 | `QFileInfoList` | `QList<QFileInfo>` 别名。 | 适合目录枚举结果。 |

### 一句话总结

`QFileInfo` 是跨平台的文件系统元数据值对象：它擅长回答“这个路径是什么、在哪里、有什么属性”，但不负责打开文件，也不保证信息永远新鲜。把它用于展示、筛选和预取；把真正的读写、删除和安全授权交给对应操作，并始终处理 TOCTOU 和平台差异。
