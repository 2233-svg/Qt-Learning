# Qt QDirListing 深入笔记

> 适用版本：Qt 6.11  
> 头文件：`#include <QDirListing>`  
> 所属模块：`Qt6::Core`  
> 相关类：`QDirIterator`、`QFileInfo`、`QFileDevice`、`QTimeZone`

## 1. 它解决什么问题：现代的、按项产生目录条目的范围

`QDirListing` 是 Qt 6 的目录枚举类。它以 C++ range 的方式一次产生一个 `DirEntry`，适合大目录树、递归扫描、名称过滤和符号链接策略控制。

```cpp
for (const auto &entry : QDirListing(root)) {
    qDebug() << entry.filePath();
}
```

它替代已弃用的 `QDirIterator`。与 `QDir::entryList()` 相比，`QDirListing` 不会先生成完整结果列表，因而在目录很大时更节省内存；代价是它不支持排序、随机访问或可复制的多遍迭代。

| 需求 | 适合的类 | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 新代码按项扫描目录 | `QDirListing` | 以 range 逐项产生条目 | 输入迭代器是单遍的，不能依赖排序 |
| 遗留代码维护 | `QDirIterator` | 旧式 `hasNext()` 加 `next()` 遍历 | Qt 6.11 已弃用，应逐步迁移 |
| 小目录且需要排序列表 | `QDir::entryInfoList()` | 一次收集所有 `QFileInfo` | 结果多时内存和预处理成本更高 |
| 监听目录变更 | `QFileSystemWatcher` | 接收目录变化通知 | 它不替代一次全量扫描 |

## 2. 最小可用代码：只列出递归文件

```cpp
#include <QDirListing>

void scanFiles(const QString &root)
{
    using F = QDirListing::IteratorFlag;
    const auto flags = F::FilesOnly | F::Recursive;

    for (const auto &entry : QDirListing(root, flags)) {
        processFile(entry.filePath());
    }
}
```

`FilesOnly` 决定输出中只保留常规文件；`Recursive` 决定是否进入子目录。两者是独立的：没有递归就只扫描根目录，有递归但不加 `FilesOnly` 则目录、链接和其它条目也可能出现。

与所有文件系统扫描一样，`entry` 只是枚举瞬间的观察结果。真正打开、删除或上传文件前，目标仍可能被其它进程移动、替换或改权限，操作点必须自行处理失败。

## 3. 它是 input range，不是普通容器

`QDirListing::const_iterator` 模型是 C++20 `std::input_iterator`：

- 只能向前、单次遍历；
- 不支持随机访问、倒序或复制迭代器；
- 后置自增返回 `void`，不要写依赖旧值的 `it++` 逻辑；
- `end()` 是 sentinel，不是同类型 iterator；
- 解引用到 `end()` 是未定义行为。

最容易误解的是 `begin()`：在同一个 `QDirListing` 对象上再次调用 `begin()`，会重置内部状态并从头开始。不要在一个正在遍历的 listing 上创建第二个 begin，也不要尝试嵌套遍历同一个 listing。

```cpp
QDirListing listing(root);

for (const auto &entry : listing) {
    // 不要在此处再调用 listing.begin()。
}
```

范围 for 循环是最自然、最不容易误用的写法。需要配合算法时，应使用接受 input range 的 C++20 `std::ranges` 算法；传统 STL 算法通常要求两个同类型 iterator，不能直接配合 iterator/sentinel 组合。

## 4. `DirEntry` 是惰性信息入口，不是应长期保存的快照

每次迭代解引用得到 `const DirEntry &`。`DirEntry` 按需查询文件系统：只拿 `fileName()` 通常比先取 `fileInfo()` 再取文件名更轻，因为后者可能要构造 `QFileInfo` 并执行额外的元数据查询。

```cpp
for (const auto &entry : QDirListing(root)) {
    if (entry.fileName().endsWith(".conf"_L1)) {
        // 只按名字筛选时，无需 fileInfo()。
    }

    if (entry.size() > 4096) {
        // size() 需要元数据；这里再查询是合理的。
    }
}
```

不要把 `const DirEntry &` 保存到循环外或在迭代器推进后继续当成前一个条目使用。需要长期保存时，立即拷贝真正需要的值：

```cpp
QStringList paths;
for (const auto &entry : QDirListing(root)) {
    paths.append(entry.filePath());
}
```

`fileInfo()` 返回一个值类型 `QFileInfo`，适合需要保留多项元数据的场合；只查询一个名称、路径或大小时，优先使用 `DirEntry` 的直接成员。

## 5. 过滤标志：控制“列出什么”与“如何走目录树”

```cpp
using F = QDirListing::IteratorFlag;

const auto flags = F::FilesOnly
                 | F::Recursive
                 | F::ResolveSymlinks
                 | F::IncludeHidden;

for (const auto &entry : QDirListing(root, flags)) {
    use(entry);
}
```

名称过滤器是 glob 模式，如 `"*.cpp"`，并不是正则表达式。Qt 会将它们按 wildcard 规则处理；对于少量固定后缀，先列出条目再用 `QString::endsWith()` 过滤有时更直接，也可能更高效。

### 5.1 文件、目录和其它条目

`FilesOnly` 和 `DirsOnly` 是常用组合标志。它们基于 `ExcludeFiles`、`ExcludeDirs`、`ExcludeOther` 组合而成：

- “other” 在 Unix 可能是 FIFO、socket、字符设备或块设备；
- Windows 上 `.lnk` 文件由于历史原因也被视为 other；
- 面向用户上传、扫描或清理的程序不应默认把特殊文件当普通文件处理。

### 5.2 符号链接的两件事

`ResolveSymlinks` 决定过滤时按链接目标类型判断，坏链接默认会被排除；Qt 6.11 的 `IncludeBrokenSymlinks` 可以将坏链接显式列出来。

`FollowDirSymlinks` 则决定递归时是否进入“指向目录”的符号链接，且只有和 `Recursive` 组合才有作用。Qt 能检测典型链接环并忽略，但这不构成目录沙箱：链接仍可能指向 root 以外的位置，扫描期间文件系统也可能变化。

对安全敏感的导入、删除或执行操作，必须把真实路径、授权根目录和文件打开时的对象身份一起纳入检查；不能只凭 `filePath()` 的字符串前缀相信条目仍位于 root 内。

## 6. 常用筛选方案

### 6.1 找指定类型文件

```cpp
using F = QDirListing::IteratorFlag;

QDirListing listing(
    root,
    {"*.json", "*.yaml", "*.yml"},
    F::FilesOnly | F::Recursive | F::CaseSensitive);

for (const auto &entry : listing) {
    importConfiguration(entry.filePath());
}
```

`CaseSensitive` 只影响构造函数中名称 glob 的大小写匹配。是否应开启取决于业务格式而非操作系统习惯：若协议只承认小写 `.json`，就开启；若产品希望兼容用户保存的 `.JSON`，则不要依赖大小写敏感 glob。

### 6.2 包含隐藏文件和坏链接

```cpp
using F = QDirListing::IteratorFlag;

const auto flags = F::Recursive
                 | F::IncludeHidden
                 | F::IncludeBrokenSymlinks;

for (const auto &entry : QDirListing(root, flags)) {
    report(entry.filePath(), entry.isSymLink(), entry.exists());
}
```

隐藏目录只有在同时指定 `IncludeHidden` 与 `Recursive` 时才会被递归进入。`.` 和 `..` 默认不会列出；需要兼容极少数底层目录工具时才使用 `IncludeDotAndDotDot`，普通扫描不应打开它。

## 7. 时间、路径和元数据的现实边界

`birthTime()`、`lastModified()`、`lastRead()`、`metadataChangeTime()` 和通用的 `fileTime()` 都接受 `QTimeZone`。传入明确业务时区更可控；显示给用户通常让 UI 层按 locale 和用户时区格式化。

不同文件系统不保证提供每一种时间，尤其 birth time 和 last access time。不要把无效或缺失时间自动当成当前时间，也不要把 metadata change time 误当成内容修改时间。

`canonicalFilePath()` 会解析符号链接并规范化路径，但目标不存在或无法解析时可能返回空值。`absoluteFilePath()` 只生成绝对路径，不等同于“已消除了符号链接”；安全检查要根据业务对真实路径的要求选择二者，并处理失败。

## 8. 常见误区

| 误区 | 为什么会出问题 | 应该怎样做 | 使用时重点注意 |
| --- | --- | --- | --- |
| 把 QDirListing 当可排序容器 | 它按项枚举且不支持 sorting | 收集需要的值后再按业务键排序 | 大目录不要无条件收集全部结果 |
| 保存 `const DirEntry &` 到循环外 | 它属于单遍迭代过程中的当前条目视图 | 立即复制 path、QFileInfo 或所需字段 | 迭代器推进后不要继续代表旧条目 |
| 同一 listing 上嵌套调用 `begin()` | 新 begin 会重置内部遍历状态 | 为嵌套扫描创建独立 QDirListing | 一个 listing 对象一次只承担一条遍历 |
| 认为 `FilesOnly` 会自动进入子目录 | 类型筛选和递归是两组旗标 | 同时使用 `FilesOnly` 与 `Recursive` | 递归大目录应放到合适线程或分块执行 |
| 认为 FollowDirSymlinks 就能安全防环 | 只处理典型环，链接仍可越过 root | 明确验证真实目标及授权边界 | 对删除和执行操作尤其重要 |
| 对每项都先调用 `fileInfo()` | 可能产生不必要的元数据查询 | 只用 `DirEntry` 的直接查询 | 大目录扫描里系统调用成本会累积 |
| 假定列出的路径随后一定存在 | 文件系统随时可能变化 | 打开、读取和删除处分别处理失败 | 典型 TOCTOU 问题，不能靠一次 exists 判断解决 |

## API 速查表
### 9.1 `IteratorFlag` 与 `IteratorFlags`

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 标志 | `Default` | 使用默认列举行为 | 默认不递归、不包含隐藏项和点目录 |
| 标志 | `ExcludeFiles` | 不列出常规文件 | 搭配 `ResolveSymlinks` 时，指向文件的链接也会被排除 |
| 标志 | `ExcludeDirs` | 不列出目录 | 不代表停止递归；递归行为由 `Recursive` 控制 |
| 标志 | `ExcludeOther` | 不列出文件、目录和链接以外的特殊条目 | Qt 6.10 起；Unix 特殊文件和 Windows `.lnk` 有平台差异 |
| 兼容标志 | `ExcludeSpecial` | `ExcludeOther` 的旧名称 | Qt 6.14 起弃用；新代码使用 `ExcludeOther` |
| 标志 | `ResolveSymlinks` | 根据符号链接目标的类型执行筛选 | 坏链接默认排除；不等于递归进入目录链接 |
| 标志 | `FilesOnly` | 只列出常规文件的组合筛选 | 若要把指向文件的链接按文件处理，组合 `ResolveSymlinks` |
| 标志 | `DirsOnly` | 只列出目录的组合筛选 | 若要把指向目录的链接按目录处理，组合 `ResolveSymlinks` |
| 标志 | `IncludeHidden` | 列出隐藏条目 | 与 `Recursive` 组合时也会进入隐藏子目录 |
| 标志 | `IncludeDotAndDotDot` | 列出 `.` 和 `..` | 通常不需要；业务递归时避免把它当普通目录处理 |
| 标志 | `CaseSensitive` | 让名称 glob 使用大小写敏感匹配 | 只影响 name filters，不影响之后手写的字符串判断 |
| 标志 | `Recursive` | 递归列出所有子目录中的条目 | 大目录和网络挂载点可能造成长时间 I/O |
| 标志 | `FollowDirSymlinks` | 递归进入指向目录的符号链接 | 只有与 Recursive 组合有效；环检测不等于安全边界 |
| 标志 | `IncludeBrokenSymlinks` | 把目标不存在的符号链接也列出 | Qt 6.11 起；不支持符号链接的平台会忽略此设置 |
| 内部标志 | `NoNameFiltersForDirs` | 控制目录是否跳过名称过滤 | Qt 内部使用，不应在应用代码中依赖 |
| 标志类型 | `IteratorFlags` | 存储多个 IteratorFlag 的组合 | 用 C++ 按位或运算符组合选择 |

### 9.2 `QDirListing`、范围和迭代器

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDirListing(const QString &path, IteratorFlags flags = Default)` | 创建对 path 的目录枚举范围 | 不检查结果快照；路径不可访问时需在实际文件操作处处理 |
| 构造 | `QDirListing(const QString &path, const QStringList &nameFilters, IteratorFlags flags = Default)` | 创建带文件名 glob 过滤的范围 | glob 不是正则；大小写敏感性由 `CaseSensitive` 控制 |
| 移动构造 | `QDirListing(QDirListing &&other)` | 转移 listing 的内部遍历状态 | 移动源只可析构或重新赋值 |
| 移动赋值 | `operator=(QDirListing &&other)` | 用另一个 listing 的状态替换当前对象 | 会丢弃当前遍历进度；移动源进入部分形成状态 |
| 析构 | `~QDirListing()` | 销毁目录枚举对象 | 相关 iterator 和 DirEntry 不应在此后继续使用 |
| 交换 | `swap(QDirListing &other)` | 高效交换两个 listing 的状态 | 基础路径、旗标和当前遍历进度都会交换 |
| 范围开始 | `begin() const` | 返回可开始枚举的 input iterator | 每次调用会重置该 listing 的内部状态 |
| 范围开始 | `cbegin() const` | const 形式的 begin | 与 begin 语义相同，仍会重置遍历 |
| 范围结束 | `end() const` | 返回表示结束的 sentinel | 不要解引用与 end 相等的 iterator |
| 范围结束 | `cend() const` | const 形式的 end | 与 cend 比较，而非假定它是可解引用 iterator |
| Qt 兼容 | `constBegin() const` | Qt 风格的 begin 别名 | 仍是单遍遍历；调用会重置状态 |
| Qt 兼容 | `constEnd() const` | Qt 风格的 end 别名 | 返回 sentinel，不提供随机访问能力 |
| 配置查询 | `iteratorPath() const` | 返回构造时传入的目录路径 | 不是当前条目的路径，也不一定是 canonical path |
| 配置查询 | `iteratorFlags() const` | 返回构造时选择的标志组合 | 用于诊断配置，不会反映文件系统实际能力 |
| 配置查询 | `nameFilters() const` | 返回构造时的 glob 名称过滤器 | 结果是配置副本，不是动态发现的文件名列表 |
| 迭代器 | `const_iterator` | move-only、单向的输入迭代器 | 不可复制、不可随机访问、不能倒序 |
| 结束标记 | `sentinel` | 表示迭代结束的专用类型 | 用于 range-for 与 C++20 ranges；传统算法未必支持 |

### 9.3 `DirEntry` 路径、类型和访问权限

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 名称 | `fileName()` | 返回最后一级文件名 | 高频按名字筛选优先它，避免不必要的 QFileInfo |
| 名称 | `baseName()` | 返回去掉最后后缀的基础名 | 多重后缀如 `.tar.gz` 只去掉最后一个 |
| 名称 | `completeBaseName()` | 返回去掉完整后缀链的基础名 | 多重后缀处理与 baseName 不同 |
| 名称 | `suffix()` | 返回最后一个后缀 | 不含点号；无后缀时结果为空 |
| 名称 | `completeSuffix()` | 返回所有后缀组成的字符串 | 适合 `.tar.gz` 这类多段后缀判断 |
| 名称 | `bundleName()` | 返回平台相关的 bundle 名称 | 主要与 macOS bundle 语义相关，跨平台不要依赖 |
| 路径 | `filePath()` | 返回当前条目的枚举路径 | 不保证 canonical，也不保证随后仍存在 |
| 路径 | `canonicalFilePath()` | 返回解析链接后的规范路径 | 目标不存在或无法解析时可能为空 |
| 路径 | `absoluteFilePath()` | 返回绝对文件路径 | 不解析所有符号链接，不能单独作为沙箱验证 |
| 路径 | `absolutePath()` | 返回所在目录的绝对路径 | 仅路径计算，不代表访问权限或持久存在 |
| 类型 | `isFile()` | 判断是否为常规文件 | 结果来自枚举时观察，打开前仍可能变化 |
| 类型 | `isDir()` | 判断是否为目录 | 是否把链接按目标目录处理受 ResolveSymlinks 影响 |
| 类型 | `isSymLink()` | 判断是否为符号链接 | 平台不支持链接时行为受平台能力限制 |
| 存在性 | `exists()` | 判断当前条目或链接目标是否存在 | 不能消除 TOCTOU，真实操作仍需检查错误 |
| 可见性 | `isHidden()` | 判断是否为隐藏条目 | “隐藏”规则带平台差异，不能视为安全属性 |
| 权限 | `isReadable()` | 判断当前用户是否可读 | 只是预检；打开时仍可能失败 |
| 权限 | `isWritable()` | 判断当前用户是否可写 | 不等于实际写入一定成功，目录权限也会影响 |
| 权限 | `isExecutable()` | 判断是否可执行 | 不应把它当作执行不可信文件的许可 |

### 9.4 `DirEntry` 元数据与时间

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 元数据 | `fileInfo()` | 返回当前条目的 QFileInfo 值 | 当要保留多项元数据时使用；单字段查询优先 DirEntry |
| 大小 | `size()` | 返回文件大小字节数 | 目录、特殊文件和并发写入文件的含义需按平台处理 |
| 时间 | `birthTime(const QTimeZone &tz)` | 返回创建时间 | 文件系统可能不提供，结果可能无效 |
| 时间 | `metadataChangeTime(const QTimeZone &tz)` | 返回元数据变化时间 | 不等同文件内容修改时间 |
| 时间 | `lastModified(const QTimeZone &tz)` | 返回内容最后修改时间 | 并发写入时只是一个观察时点 |
| 时间 | `lastRead(const QTimeZone &tz)` | 返回最后访问时间 | 系统可能关闭或延迟更新 atime |
| 时间 | `fileTime(QFileDevice::FileTime type, const QTimeZone &tz)` | 按指定 FileTime 枚举查询时间 | 传入业务时区；先检查 QDateTime 是否有效 |

## 10. 一个稳妥的扫描骨架

```cpp
using F = QDirListing::IteratorFlag;

void indexSourceFiles(const QString &root)
{
    const auto flags = F::FilesOnly | F::Recursive | F::ResolveSymlinks;
    QDirListing listing(root, {"*.cpp", "*.h", "*.hpp"}, flags);

    for (const auto &entry : listing) {
        const QString path = entry.filePath();

        QFile file(path);
        if (!file.open(QIODevice::ReadOnly))
            continue;

        indexFile(path, file.readAll());
    }
}
```

这段代码将“筛选”和“使用”分开：listing 负责按目录规则找候选项，`QFile::open()` 负责在真正使用时确认文件仍可读。若业务需要稳定顺序、完整错误报告、取消能力或安全目录边界，应在这个骨架外增加相应的收集、排序、错误对象和路径验证，而不是假定目录遍历类会替你保证这些性质。
