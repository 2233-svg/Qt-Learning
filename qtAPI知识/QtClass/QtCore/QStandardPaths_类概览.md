# Qt QStandardPaths 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStandardPaths>`  
> 所属模块：`Qt6::Core`  
> 继承：无  
> 定位：为配置、缓存、数据、下载和临时文件选择平台正确的标准目录

## 1. 为什么不能自己拼目录

不同平台对用户数据和缓存的位置约定不同。把配置写到当前工作目录、可执行文件目录或硬编码的 `C:/Users/...`，会在安装、沙箱、权限和多用户环境中失效。

`QStandardPaths` 根据平台和应用信息提供目录类别：

```cpp
const QString configDir =
    QStandardPaths::writableLocation(
        QStandardPaths::AppConfigLocation);
const QString cacheDir =
    QStandardPaths::writableLocation(
        QStandardPaths::CacheLocation);
```

它只返回建议位置，不会自动创建目录、不保证路径可写，也不替你决定文件名。

## 2. 常用位置怎么选

| 需求 | 推荐位置 | 说明 | 关键边界 |
| --- | --- | --- | --- |
| 用户偏好和配置 | `AppConfigLocation` | 应用专属配置 | 启动早期设置应用名和组织名 |
| 用户持久数据 | `AppDataLocation` | 应用专属数据 | 不应当作临时缓存随意清理 |
| 多应用共享数据 | `GenericDataLocation` | 需要明确共享格式和权限 | 共享格式和访问权限要单独设计 |
| 可重建缓存 | `CacheLocation` | 不应存放唯一用户数据 | 系统清理后应用必须能恢复 |
| 临时工作文件 | `TempLocation` | 进程或系统清理策略可能删除 | 文件名和权限仍需安全处理 |
| 下载文件 | `DownloadLocation` | 面向用户的下载目录 | 不代表目录一定存在或可写 |
| 日志/状态 | `StateLocation` | Qt 6.7 起，平台不一定提供独立目录 | 不要依赖所有平台都有该目录 |

应用名和组织信息会影响应用专属路径：

```cpp
QCoreApplication::setOrganizationName("ExampleOrg");
QCoreApplication::setApplicationName("Editor");
```

应在第一次查询标准路径前设置稳定元数据。

## 3. 创建目录并组合文件名

```cpp
const QString dirPath =
    QStandardPaths::writableLocation(
        QStandardPaths::AppConfigLocation);

if (dirPath.isEmpty())
    return false;

QDir dir(dirPath);
if (!dir.mkpath("."))
    return false;

QFile file(dir.filePath("settings.ini"));
```

`writableLocation()` 返回的目录可能尚不存在，所以使用前常要 `QDir::mkpath()`。目录创建失败时要报告错误，不要悄悄退回当前目录，否则可能把用户数据写到错误位置。

## 4. `standardLocations()` 和多候选路径

```cpp
const QStringList candidates =
    QStandardPaths::standardLocations(
        QStandardPaths::GenericDataLocation);
```

多个候选位置适合读取系统级和用户级资源。写入时通常只使用 `writableLocation()` 返回的首选可写位置，不要把数据随机写到候选列表中的任意项。

## 5. 查找和可执行文件

```cpp
const QString theme =
    QStandardPaths::locate(
        QStandardPaths::AppDataLocation,
        "themes/dark.json",
        QStandardPaths::LocateFile);

const QStringList allThemes =
    QStandardPaths::locateAll(
        QStandardPaths::AppDataLocation,
        "themes/dark.json");
```

`locate()` 查找已经存在的文件或目录；它不会创建资源。`findExecutable()` 用于按 PATH 或指定路径查找可执行文件：

```cpp
const QString ffmpeg =
    QStandardPaths::findExecutable("ffmpeg");
```

找到可执行文件不代表它可信。运行外部程序前仍要校验来源、参数和权限。

## 6. 测试模式

```cpp
QStandardPaths::setTestModeEnabled(true);
```

测试模式让 Qt 使用隔离的测试目录，避免测试污染真实用户配置。它是进程级设置，应在创建依赖路径的对象前启用，并在测试之间明确清理。

## 7. 常见误区

### 把返回路径当成已创建目录

必须自己 `mkpath()`，并检查权限和错误。

### 把 CacheLocation 当唯一数据目录

缓存可以被系统清理。不可丢失的数据应放在 AppData 或明确的持久化位置。

### 用 TempLocation 保存用户文件

临时目录生命周期不稳定，可能权限开放或被清理。

### 在库中修改测试模式或全局应用名

这些是宿主进程级设置。库应使用已有应用上下文，不要改变全局路径策略。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 可写目录 | `writableLocation(StandardLocation)` | 返回某类标准目录的首选可写路径。 | 可能为空或尚不存在；调用者负责创建并检查可写性。 |
| 多候选 | `standardLocations(StandardLocation)` | 返回该位置类别的候选路径列表。 | 适合读取搜索；写入通常选 writableLocation。 |
| 查找 | `locate(StandardLocation, fileName, LocateOptions)` | 在标准目录中查找第一个匹配文件或目录。 | 只查找已有项；相对文件名不要包含意外路径穿越。 |
| 查找 | `locateAll(StandardLocation, fileName, LocateOptions)` | 返回所有匹配路径。 | 结果顺序和平台候选路径有关；不要直接当稳定优先级。 |
| 展示 | `displayName(StandardLocation)` | 返回适合展示给用户的目录名称。 | 这是 UI 文本，不是实际路径。 |
| 可执行文件 | `findExecutable(QString, QStringList)` | 在 PATH 或指定目录中查找可执行文件。 | 找到后仍要检查可信来源和参数注入风险。 |
| 测试 | `setTestModeEnabled(bool)` | 启用或关闭隔离测试路径。 | 进程级全局设置；应在创建路径依赖对象前调用。 |
| 测试 | `isTestModeEnabled()` | 查询测试路径模式是否启用。 | 只表示 Qt 的模式，不代表测试目录已经创建。 |
| 枚举 | `StandardLocation` | 表示桌面、文档、应用数据、配置、缓存、临时和状态等位置。 | 选择类别时按数据生命周期和可丢失性判断。 |
| 枚举 | `LocateOption` / `LocateOptions` | 指定查找文件、目录或组合类型。 | `LocateFile` 和 `LocateDirectory` 影响匹配结果。 |

---

### 一句话总结

`QStandardPaths` 解决的是“数据应该放在哪个平台目录”的问题，不负责创建和授权。先按数据生命周期选择位置，再创建目录、拼接文件名并检查错误，才能让应用在不同平台和安装方式下稳定工作。
