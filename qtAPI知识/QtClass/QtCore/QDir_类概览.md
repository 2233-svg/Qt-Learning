# Qt QDir 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDir>`  
> 所属模块：`Qt6::Core`  
> 继承：无  
> 定位：表示目录路径、筛选目录项并执行目录级文件系统操作的值类型

## 1. QDir 解决什么问题

`QDir` 负责“目录路径如何表示和遍历”，而 `QFile` 负责“单个文件如何打开和读写”。它可以：

- 规范化、拼接和转换目录路径。
- 按名称、类型、权限和隐藏状态筛选目录项。
- 按名称、时间、大小和类型排序。
- 创建、删除、移动目录以及递归删除目录树。
- 返回 `QStringList` 或 `QFileInfoList` 供上层继续处理。

`QDir` 是值类型，复制它不会复制目录内容；复制的是目录查询状态和路径描述。

## 2. 路径、绝对路径和规范路径

```cpp
QDir dir("data");
qDebug() << dir.path();          // 可能仍是相对路径
qDebug() << dir.absolutePath();  // 转成绝对路径
qDebug() << dir.canonicalPath();// 解析符号链接后的真实路径
```

- `path()` 保留 QDir 当前使用的路径形式。
- `absolutePath()` 以当前工作目录为基准补成绝对路径。
- `canonicalPath()` 通常要求路径实际存在，并解析 `.`、`..` 和符号链接；失败时可能返回空字符串。

路径规范化不是安全授权。处理用户输入时仍要检查是否越出允许根目录，以及是否通过符号链接跳到外部。

## 3. 拼接路径不要手写分隔符

```cpp
const QString logPath = dir.filePath("logs/app.log");
const QString absPath = dir.absoluteFilePath("logs/app.log");
```

`filePath()` 会按当前目录拼接文件名，`absoluteFilePath()` 还会转成绝对路径。它们不会自动创建父目录，也不会保证结果指向安全位置。

## 4. 遍历：Filters、nameFilters 和排序

```cpp
QDir dir(root);
dir.setFilter(QDir::Files | QDir::Readable | QDir::NoSymLinks);
dir.setNameFilters({"*.json", "*.ini"});
dir.setSorting(QDir::Name | QDir::IgnoreCase);

for (const QString &name : dir.entryList())
    qDebug() << dir.filePath(name);
```

过滤和排序是两个阶段：

- `Filters` 决定哪些目录项进入结果。
- `nameFilters` 按通配符匹配名称。
- `SortFlags` 决定结果顺序。

如果后续需要大小、权限、修改时间和符号链接信息，使用 `entryInfoList()`，避免再次为每个路径构造 `QFileInfo`：

```cpp
for (const QFileInfo &info : dir.entryInfoList(
         QDir::Files | QDir::Readable,
         QDir::Time | QDir::Reversed)) {
    qDebug() << info.fileName() << info.size();
}
```

大量目录或超大目录不应把全部结果一次装进列表；使用 `QDirIterator` 或 `QDirListing` 流式遍历。

## 5. 创建和删除目录

```cpp
QDir dir;
if (!dir.mkpath("/tmp/myapp/cache"))
    qWarning() << "create directory failed";
```

- `mkdir()` 只创建一个子目录，父目录必须已经存在。
- `mkpath()` 会递归创建缺失的父目录。
- `rmdir()` 删除一个空目录。
- `rmpath()` 删除目录并尝试清理空的父目录。
- `removeRecursively()` 删除当前目录树，风险很高。

删除前一定要确认路径不是空字符串、根目录、工作目录或用户不应失去的目录。对不可信路径不要直接拼接后递归删除。

## 6. 当前目录、搜索路径和资源路径

```cpp
const QString cwd = QDir::currentPath();
QDir::setCurrent(workDirectory);

QDir::addSearchPath("icons", ":/icons");
const QString iconPath = QDir("icons:").filePath("save.png");
```

修改进程当前工作目录会影响所有使用相对路径的代码，库代码通常不应调用 `setCurrent()`。搜索路径前缀适合资源定位，但它不是权限隔离机制。

## 7. 常见误区

### 把 `canonicalPath()` 当作一定成功

路径不存在、权限不足或符号链接无效时可能返回空。使用前检查结果。

### 先 `exists()` 再 `remove()`

这是典型的 TOCTOU 窗口。直接执行操作并处理返回值更可靠。

### 把 entryList 顺序当稳定 ID

文件新增、删除、时间精度和平台排序都会影响顺序。需要稳定标识时使用文件内容、明确 ID 或 canonical path。

### 用 QDir 递归删除用户输入目录

`removeRecursively()` 是高风险操作。先规范化路径、校验允许根目录，再执行，并记录实际目标。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDir(QString path = {})` | 创建表示目录路径的值对象。 | 不会验证目录存在，也不会创建目录。 |
| 构造 | `QDir(QString, QString, SortFlags, Filters)` | 创建带名称过滤、排序和类型过滤的目录查询对象。 | 查询参数只影响之后的 entryList/entryInfoList。 |
| 路径 | `setPath(QString)` | 修改 QDir 当前路径。 | 只改对象状态，不移动或创建磁盘目录。 |
| 路径 | `path()` | 返回当前路径字符串。 | 可能是相对路径或包含未解析的符号链接。 |
| 路径 | `absolutePath()` | 返回基于当前工作目录的绝对路径。 | 当前工作目录变化会影响相对路径结果。 |
| 路径 | `canonicalPath()` | 返回解析符号链接、`.` 和 `..` 后的真实路径。 | 路径不存在或无法访问时可能为空；不等同于安全授权。 |
| 路径 | `filesystemPath()` / `filesystemAbsolutePath()` / `filesystemCanonicalPath()` | 以标准库 path 返回对应路径。 | 需要 filesystem 支持；仍需处理空 canonical path。 |
| 拼接 | `dirName()` | 返回当前路径的最后一级目录名。 | 根目录和特殊路径的结果要在目标平台测试。 |
| 拼接 | `filePath(QString)` | 将文件名拼接到当前目录。 | 不创建父目录；文件名包含 `..` 时仍需安全校验。 |
| 拼接 | `absoluteFilePath(QString)` | 拼接并返回绝对文件路径。 | 不解析符号链接；需要真实路径时使用 QFileInfo/QDir canonical API。 |
| 拼接 | `relativeFilePath(QString)` | 返回相对于当前目录的路径。 | 结果可能包含 `..`；不要直接用于授权判断。 |
| 分隔符 | `toNativeSeparators(QString)` | 转换为平台原生分隔符。 | 仅处理表示形式，不做路径存在性检查。 |
| 分隔符 | `fromNativeSeparators(QString)` | 把平台分隔符转成 Qt 统一形式。 | 不会解析 `.`、`..` 或符号链接。 |
| 目录移动 | `cd(QString)` | 让 QDir 进入子目录。 | 目标必须存在且可访问；只改变 QDir 对象路径。 |
| 目录移动 | `cdUp()` | 进入父目录。 | 到根目录时可能无法继续上移；不要用它替代安全根判断。 |
| 查询 | `nameFilters()` / `setNameFilters()` | 读取或设置通配符名称过滤。 | 过滤模式不是正则；多个模式通常是 OR 关系。 |
| 查询 | `filter()` / `setFilter()` | 读取或设置文件类型、权限、隐藏项等过滤。 | `Dirs`、`Files`、`NoDotAndDotDot` 等组合要明确。 |
| 查询 | `sorting()` / `setSorting()` | 读取或设置结果排序规则。 | `Unsorted` 仍不保证文件系统返回顺序稳定。 |
| 查询 | `count()` | 返回当前查询结果数量。 | 会触发目录枚举；大目录高频调用应避免。 |
| 查询 | `isEmpty(Filters)` | 判断过滤后的目录结果是否为空。 | 只描述当前快照，之后目录可能发生变化。 |
| 遍历 | `entryList()` | 返回匹配项名称列表。 | 不包含完整属性；需要大小和权限时用 entryInfoList。 |
| 遍历 | `entryInfoList()` | 返回匹配项 QFileInfo 列表。 | 枚举和属性读取都有成本；不要对超大目录一次加载全部。 |
| 遍历 | `operator[](qsizetype)` | 按结果索引访问一个名称。 | 索引越界和查询状态变化要小心；新代码更推荐遍历列表。 |
| 过滤 | `nameFiltersFromString(QString)` | 把字符串形式的过滤器拆成列表。 | 输入格式仍是通配符，不是正则表达式。 |
| 创建 | `mkdir(QString)` | 创建当前目录下的一个子目录。 | 父目录必须存在；失败检查返回值。 |
| 创建 | `mkpath(QString)` | 递归创建目录路径。 | 不会修复错误路径；用户输入要防止越界和绝对路径替换。 |
| 删除 | `rmdir(QString)` | 删除一个空的子目录。 | 非空目录通常失败；不要与递归删除混用。 |
| 删除 | `rmpath(QString)` | 删除目录并尝试清理空的父路径。 | 只处理空目录，必须确认目标范围。 |
| 删除 | `removeRecursively()` | 删除当前目录及所有内容。 | 高风险且不可逆；执行前做严格路径校验和备份策略。 |
| 文件操作 | `remove(QString)` | 删除当前目录下指定文件。 | 直接处理返回值，避免只依赖 exists 检查。 |
| 文件操作 | `rename(QString, QString)` | 重命名当前目录下的文件或目录。 | 目标覆盖、跨文件系统和权限行为依平台不同。 |
| 状态 | `isReadable()` | 判断当前目录是否可读。 | 是瞬时能力检查，实际枚举仍可能失败。 |
| 状态 | `exists()` | 判断当前路径是否存在。 | 不代表可写、可枚举或随后操作一定成功。 |
| 状态 | `isRoot()` | 判断当前路径是否是根目录。 | 适合删除前的安全保护；不替代允许根目录校验。 |
| 状态 | `isRelativePath()` / `isAbsolutePath()` | 判断字符串路径是否相对或绝对。 | 不等于路径存在，也不等于规范化完成。 |
| 状态 | `isRelative()` / `isAbsolute()` | 判断 QDir 当前路径形式。 | 当前目录变化会影响相对路径解析。 |
| 状态 | `makeAbsolute()` | 将当前 QDir 路径改为绝对路径。 | 只改变对象，不解析符号链接。 |
| 全局 | `drives()` | 返回平台可见的根驱动器或挂载点。 | 平台差异明显；不要把它当作固定盘符列表。 |
| 全局 | `currentPath()` / `current()` | 获取当前进程工作目录。 | 进程全局状态；库代码避免修改。 |
| 全局 | `setCurrent(QString)` | 修改当前进程工作目录。 | 会影响其他组件的相对路径，应极其谨慎。 |
| 全局 | `homePath()` / `home()` | 获取用户主目录。 | 用户数据应优先按具体 StandardLocation 选择。 |
| 全局 | `rootPath()` / `root()` | 获取平台根目录。 | Windows 与 Unix 语义不同。 |
| 全局 | `tempPath()` / `temp()` | 获取临时目录。 | 不代表文件自动安全；临时文件名和权限仍需处理。 |
| 搜索 | `setSearchPaths()` / `addSearchPath()` / `searchPaths()` | 管理前缀到路径列表的搜索映射。 | 适合资源定位，不是访问控制；路径顺序会影响结果。 |
| 匹配 | `match(filter, fileName)` / `match(filters, fileName)` | 用通配符匹配一个名称。 | 不是正则；平台大小写语义需按 QDir 规则理解。 |
| 规范化 | `cleanPath(QString)` | 清理重复分隔符、`.` 和部分 `..`。 | 不解析符号链接，也不保证结果位于某个安全根目录。 |
| 刷新 | `refresh()` | 清除目录枚举缓存，要求下次重新读取。 | 外部目录发生变化后使用；不能阻止竞态。 |
| 枚举 | `Filter` / `Filters` | 描述目录项类型、隐藏项和权限筛选。 | 用位组合；不要把过滤条件误当访问授权。 |
| 枚举 | `SortFlag` / `SortFlags` | 描述名称、时间、大小、类型和方向排序。 | 排序成本和大小写/本地化规则要考虑。 |

---

### 一句话总结

`QDir` 是目录查询和值语义的工具，不是安全沙箱。用 `filePath()` 拼接、用过滤器和 `entryInfoList()` 获取结果、用 `QDirIterator` 处理大目录，并在递归删除和用户路径场景中单独做严格的安全边界校验。
