# Qt QFile 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QFile>`  
> 所属模块：`Qt6::Core`  
> 继承：`QFileDevice -> QFile`  
> 定位：以 Qt 的 `QIODevice` 接口访问普通文件、路径和文件系统操作

## 1. QFile 解决什么问题

`QFile` 把普通文件接入 Qt 的 I/O 模型。它既能像 `QIODevice` 一样流式读写，也能执行文件系统层面的复制、移动、重命名、删除、链接和权限操作。

```text
路径
  |
  v
QFile
  ├─ open/read/write/seek  文件内容
  ├─ copy/rename/remove     文件系统操作
  ├─ permissions/resize     属性和大小
  └─ symLinkTarget          符号链接
```

它适合：

- 读取配置、脚本、日志和资源文件。
- 写入二进制数据、缓存和导出文件。
- 在安装器、工具程序或后台任务中操作文件路径。

它不负责：

- 原子替换更新文件，写配置时应考虑 `QSaveFile`。
- 自动创建父目录。
- 自动解决编码、文件锁和并发写入。
- 把相对路径变成安装目录。相对路径相对于当前工作目录。

## 2. 打开、读取和错误处理

```cpp
QFile file("input.txt");
if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    qWarning() << "open failed:" << file.fileName()
               << file.errorString();
    return;
}

const QByteArray content = file.readAll();
if (content.isEmpty() && !file.atEnd())
    qWarning() << "read failed:" << file.errorString();
```

文件打开失败是正常控制流的一部分。常见原因包括路径不存在、权限不足、目录而不是普通文件、文件被其他程序锁定，以及路径编码或工作目录错误。

读取文本时，`QFile` 只负责字节；字符编码由 `QTextStream`、`QStringDecoder` 或应用协议决定：

```cpp
QFile file("config.txt");
if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    return;

QTextStream in(&file);
in.setEncoding(QStringConverter::Utf8);
const QString firstLine = in.readLine();
```

## 3. 路径语义

```cpp
QFile relative("data/cache.bin");
QFile absolute("C:/app/data/cache.bin");
```

- 相对路径相对于当前工作目录，不是可执行文件所在目录。
- 资源系统路径 `:/icons/save.png` 不是操作系统文件路径，通常由 `QFile` 读取，但不能按普通路径进行 rename 或 remove。
- 用户配置、缓存和临时文件应使用 `QStandardPaths` 获取目录。
- 需要跨平台路径拼接时使用 `QDir` 或 `QDir::filePath()`，不要手写分隔符。

```cpp
const QString path =
    QStandardPaths::writableLocation(QStandardPaths::AppConfigLocation)
    + "/settings.ini";
```

`QFile::encodeName()` 和 `decodeName()` 主要处理本地文件系统字节表示；新代码通常以 `QString` 路径为主，不要自行把 Unicode 路径压成不明确的本地编码。

## 4. 写文件：为什么要考虑 QSaveFile

直接写目标文件：

```cpp
QFile file("settings.ini");
if (!file.open(QIODevice::WriteOnly | QIODevice::Truncate))
    return false;

if (file.write(serialized) != serialized.size())
    return false;
return file.flush();
```

如果程序在截断旧文件后崩溃，目标文件可能只剩半份内容。对配置、索引和需要避免半写状态的文件，使用 `QSaveFile`：

```cpp
QSaveFile file("settings.ini");
if (!file.open(QIODevice::WriteOnly))
    return false;

if (file.write(serialized) != serialized.size())
    return false;

return file.commit();
```

`commit()` 成功后才替换目标文件。它不是跨进程事务，也不能解决多个进程同时写同一个文件的协调问题；需要锁时另行使用 `QLockFile` 或操作系统机制。

## 5. 文件系统操作和符号链接

```cpp
QFile source("input.dat");
source.copy("backup/input.dat");
source.rename("input.old");
source.remove();
```

这些操作是文件系统层面的动作，不要求文件以 I/O 模式打开。对它们都要检查返回值：

```cpp
if (!QFile::rename(oldPath, newPath))
    qWarning() << "rename failed";
```

符号链接：

```cpp
const QString target = QFile::symLinkTarget("latest.log");
```

`symLinkTarget()` 返回链接指向的路径，不能把它当作“解析后一定存在的普通文件”。在安全边界、临时目录和删除操作中，要考虑链接可能指向目录外部的位置。

## 6. 文件句柄和所有权

Qt 可以从 C `FILE *` 或原生文件描述符打开：

```cpp
QFile file;
if (!file.open(fd, QIODevice::ReadOnly,
               QFileDevice::AutoCloseHandle)) {
    qWarning() << file.errorString();
}
```

`handleFlags` 决定 QFile 是否负责关闭传入句柄：

- `DontCloseHandle`：QFile 关闭时不关闭外部句柄。
- `AutoCloseHandle`：QFile 接管句柄关闭责任。

不要让外部代码和 QFile 同时认为自己拥有同一个句柄。跨平台代码优先使用 Qt 自己的路径和设备接口，只有与现有 C/OS API 集成时才传入句柄。

## 7. 权限、大小和删除

```cpp
const QFileDevice::Permissions current = file.permissions();
file.setPermissions(current | QFileDevice::WriteUser);

if (!file.resize(1024))
    qWarning() << file.errorString();
```

权限位受平台影响：

- Unix 的权限位语义较直接。
- Windows 的权限映射不完全等同于 Unix。
- ACL、只读属性和安全软件可能让“权限看起来允许”但实际操作仍失败。

`resize()` 会改变文件长度，扩展部分通常以零填充，截断会丢弃末尾数据。对重要文件先确认路径和备份策略。

## 8. 原子性、并发和安全

### 8.1 原子更新

使用 `QSaveFile` 写入配置和索引，避免程序崩溃留下半文件。

### 8.2 并发读取

多个读取者通常可以同时打开文件，但是否能读到一致内容取决于写入者和平台。需要一致快照时，写入者应使用临时文件加原子替换。

### 8.3 不可信路径

用户提供的路径需要考虑：

- `..` 穿越。
- 符号链接跳出预期目录。
- 设备文件或特殊文件。
- 超长路径和非法字符。
- 覆盖已有文件。

`QFile` 提供文件操作，不自动替你完成路径授权和沙箱安全策略。

## 9. 常见误区

### 把 `fileName()` 当成真实存在路径

它只是对象当前保存的名称。文件是否存在看 `exists()`，打开是否成功看 `open()`。

### 用 `applicationDirPath()` 保存用户数据

安装目录可能只读，也不适合保存每个用户的配置。使用 `QStandardPaths`。

### `flush()` 等于断电不丢数据

`flush()` 主要把 Qt/运行库缓冲提交到底层；是否落盘还受操作系统和硬件缓存影响。强持久化需要平台级同步策略。

### 直接截断覆盖重要文件

崩溃会留下半文件。配置和索引更新优先 `QSaveFile::commit()`。

### 以为 `exists()` 后再操作就是安全的

检查和实际操作之间可能发生竞态。对不可信路径不要依赖 TOCTOU 检查，直接执行并处理失败。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QFile()` | 创建没有预设路径的 QFile 对象。 | 仍需 `setFileName()` 或使用带路径构造；不创建磁盘文件。 |
| 构造 | `QFile(QString)` / `QFile(QString, QObject *)` | 创建并保存一个文件路径。 | 构造不会打开文件；路径是否存在要单独检查。 |
| 构造 | `QFile(std::filesystem::path)` | 用标准库路径构造 QFile。 | Qt 6.0 起可用；跨平台路径仍要注意编码和规范化。 |
| 析构 | `~QFile()` | 销毁 QFile 对象并结束其文件设备生命周期。 | 重要写入应先显式关闭或确认写出；句柄关闭责任由打开标志决定。 |
| 路径 | `fileName()` | 返回当前保存的文件名或路径。 | 不保证文件存在，也不保证是绝对路径。 |
| 路径 | `filesystemFileName()` | 以 `std::filesystem::path` 返回文件路径。 | Qt 配置需启用 C++17 filesystem；不要混用不同编码约定。 |
| 路径 | `setFileName(QString)` | 修改 QFile 关联的路径。 | 已打开设备不应随意改路径；修改不会移动磁盘文件。 |
| 编码 | `encodeName(QString)` | 把 Qt 字符串编码为本地文件系统字节。 | 平台相关；新代码优先保留 QString 路径。 |
| 编码 | `decodeName(QByteArray)` / `decodeName(const char *)` | 把本地文件系统字节解码为 QString。 | 编码由平台决定；不适合解析任意未知编码文本。 |
| 存在性 | `exists() const` | 判断当前路径是否存在。 | 是瞬时检查，不能替代实际操作的错误处理。 |
| 存在性 | `exists(QString)` | 判断指定路径是否存在。 | 不区分所有文件系统失败原因；不应单独作为安全授权。 |
| 打开 | `open(OpenMode)` | 按 QIODevice 模式打开文件。 | 失败后读取 `errorString()`；ReadWrite、Truncate 等组合要明确。 |
| 打开 | `open(OpenMode, Permissions)` | 打开文件并指定创建时权限。 | 只在创建文件时有意义；实际权限还受平台和 umask 影响。 |
| 打开 | `open(FILE *, OpenMode, FileHandleFlags)` | 从 C 标准库文件句柄建立 QFile。 | 明确是否 AutoCloseHandle；外部句柄必须在 QFile 生命周期内有效。 |
| 打开 | `open(int, OpenMode, FileHandleFlags)` | 从原生文件描述符建立 QFile。 | 句柄归属和关闭责任必须唯一；平台差异要单独测试。 |
| 大小 | `size()` | 返回文件当前大小。 | 文件可能在其他进程中改变；打开前后结果可能不同。 |
| 大小 | `resize(qint64)` | 改变文件长度。 | 截断会丢数据；扩展和权限受平台影响。 |
| 大小 | `resize(QString, qint64)` | 直接改变指定文件长度。 | 失败需检查返回值；不要把路径检查和 resize 分成安全授权依据。 |
| 复制 | `copy(QString)` | 将当前文件复制到新路径。 | 目标存在时通常失败；不会自动创建父目录。 |
| 复制 | `copy(QString, QString)` | 复制指定文件到目标路径。 | 复制成功不等于业务层元数据全部相同。 |
| 移动 | `rename(QString)` | 把当前文件重命名或移动到新路径。 | 跨文件系统移动可能失败；不要假设目标覆盖策略。 |
| 移动 | `rename(QString, QString)` | 重命名或移动指定文件。 | 目标目录必须存在；检查跨平台覆盖和权限差异。 |
| 删除 | `remove()` | 删除当前路径对应的文件。 | 文件打开、权限和符号链接语义会影响结果；删除前确认路径。 |
| 删除 | `remove(QString)` | 删除指定文件。 | 返回 false 时读取错误来源；不要只依赖 exists。 |
| 链接 | `link(QString)` | 为当前文件创建链接。 | 平台支持和链接类型不同；不要把链接当作复制。 |
| 链接 | `link(QString, QString)` | 为指定文件创建链接。 | 需要考虑权限、目标类型和符号链接安全。 |
| 链接 | `symLinkTarget()` | 返回当前符号链接指向的路径。 | 目标可能不存在或跳出预期目录。 |
| 链接 | `symLinkTarget(QString)` | 返回指定符号链接的目标。 | 只解析链接，不保证目标可打开。 |
| 回收站 | `supportsMoveToTrash()` | 查询平台是否支持移动到回收站。 | 支持能力不是每次操作都成功；按返回值处理。 |
| 回收站 | `moveToTrash()` | 将当前文件移入系统回收站。 | 不是永久删除；路径和平台行为不同。 |
| 回收站 | `moveToTrash(QString, QString *)` | 将指定文件移入回收站并可返回回收站路径。 | 返回路径是可选输出；失败仍要处理原文件状态。 |
| 权限 | `permissions()` | 读取当前文件权限。 | 平台映射不完全一致；不能据此保证下一次操作成功。 |
| 权限 | `permissions(QString)` | 读取指定文件权限。 | 文件不存在或权限不足时返回结果要结合平台验证。 |
| 权限 | `setPermissions(Permissions)` | 修改当前文件权限。 | Windows、Unix 和 ACL 语义不同；只设置需要的位。 |
| 权限 | `setPermissions(QString, Permissions)` | 修改指定文件权限。 | 失败原因通过返回值和错误诊断处理。 |
| 一致写入 | `QSaveFile` | 通过临时文件和提交替换实现更可靠的文件更新。 | 需要 `commit()`；不能解决多进程写冲突或所有持久化问题。 |

---

### 一句话总结

`QFile` 同时覆盖文件内容和文件系统操作，但它不会替你决定路径、编码、权限、并发和原子性。普通读取直接用 `QFile`，重要更新用 `QSaveFile`，用户数据目录用 `QStandardPaths`，每一步都检查返回值和 `errorString()`。
