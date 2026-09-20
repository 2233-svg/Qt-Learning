# Qt QSettings 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSettings>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject -> QSettings`  
> 定位：保存应用设置、用户偏好和小型配置数据的键值存储

## 1. QSettings 解决什么问题

`QSettings` 让应用用统一的键值接口读写配置，而不必直接处理 Windows Registry、macOS 偏好设置或 INI 文件细节：

```cpp
QSettings settings;
settings.setValue("editor/fontSize", 14);
settings.setValue("editor/theme", "dark");
settings.sync();
```

它适合：

- 用户偏好、窗口几何、最近打开文件。
- 小型应用配置和功能开关。
- Qt 原生格式或 INI 格式的持久化键值。

它不适合：

- 大型数据库、频繁写入的日志和高并发状态。
- 保存密码、令牌和私钥。需要系统密钥链或专门的安全存储。
- 需要事务、强 schema 和复杂查询的数据。

## 2. 应用元数据决定默认位置

无参构造通常依赖应用级元数据：

```cpp
QCoreApplication::setOrganizationName("ExampleOrg");
QCoreApplication::setApplicationName("Editor");

QSettings settings;
```

如果在创建 `QSettings` 前没有设置组织名和应用名，默认文件位置和名称可能不是你期望的。应用启动早期就设置稳定元数据，库代码不要偷偷修改宿主应用的全局设置。

需要明确路径时：

```cpp
QSettings settings(
    QStandardPaths::writableLocation(QStandardPaths::AppConfigLocation)
        + "/editor.ini",
    QSettings::IniFormat);
```

## 3. 基本读写和类型

```cpp
settings.setValue("window/geometry", window.saveGeometry());
settings.setValue("window/maximized", window.isMaximized());
settings.setValue("recent/files", QStringList{"/a.txt", "/b.txt"});

const bool maximized =
    settings.value("window/maximized", false).toBool();
const QByteArray geometry =
    settings.value("window/geometry").toByteArray();
```

值通过 `QVariant` 保存。读取时应给默认值，并确认类型转换合理：

```cpp
const int size = settings.value("editor/fontSize", 12).toInt();
if (size < 6 || size > 96)
    useDefaultFontSize();
```

配置文件可能被用户手工编辑、旧版本写入或外部程序修改，所以读取设置必须像读取外部输入一样校验范围。

## 4. 分组和数组

### 4.1 分组

```cpp
settings.beginGroup("editor");
settings.setValue("fontSize", 14);
settings.setValue("wordWrap", true);
settings.endGroup();
```

组会改变后续 key 的前缀。函数提前 return 时忘记 `endGroup()`，会让同一个 `QSettings` 对象后续读写写入错误路径。可用局部作用域和 `QSettings::beginGroup()` 的明确配对管理。

### 4.2 数组

```cpp
settings.beginWriteArray("recentProjects");
for (int i = 0; i < projects.size(); ++i) {
    settings.setArrayIndex(i);
    settings.setValue("path", projects[i]);
}
settings.endArray();

const int count = settings.beginReadArray("recentProjects");
for (int i = 0; i < count; ++i) {
    settings.setArrayIndex(i);
    loadProject(settings.value("path").toString());
}
settings.endArray();
```

数组适合结构简单的列表。元素删除、旧数据迁移和最大条目数要由应用自己处理。

## 5. 回退机制和作用域

`QSettings` 可以同时读取用户级和系统级设置，并按回退规则查找。关闭回退：

```cpp
settings.setFallbacksEnabled(false);
```

这适合测试或必须只看当前配置源的场景。不要把系统级配置当作用户输入可信，也不要让系统范围配置无条件覆盖安全关键选项。

常见作用域：

- `UserScope`：当前用户的设置。
- `SystemScope`：机器范围的设置。

格式：

- `NativeFormat`：使用平台原生设置系统。
- `IniFormat`：使用 INI 文件，便于跨平台和人工查看。
- Registry 格式和 Web 格式按平台配置提供。

## 6. 持久化、并发和错误

```cpp
settings.sync();
if (settings.status() != QSettings::NoError)
    qWarning() << "settings sync failed";
```

`setValue()` 修改的是 QSettings 的内存状态，Qt 会按实现策略写出；需要尽快提交时调用 `sync()`。`sync()` 也会读取其他进程对同一设置的修改。

配置写入不是应用级并发事务。多个进程同时更新同一个 key 可能互相覆盖；重要数据应使用数据库、锁或 `QSaveFile` 方案。

## 7. 自定义格式

可以注册自定义格式：

```cpp
QSettings::Format format = QSettings::registerFormat(
    "cfg",
    [](QIODevice &device, QSettings::SettingsMap &map) {
        Q_UNUSED(device);
        Q_UNUSED(map);
        return false;
    },
    [](QIODevice &device, const QSettings::SettingsMap &map) {
        Q_UNUSED(device);
        Q_UNUSED(map);
        return false;
    });
```

自定义读写函数要定义编码、转义、重复键、错误恢复和版本策略。不要只实现“能写出当前数据”，还要设计损坏输入和旧格式迁移。

## 8. 常见误区

### 把 QSettings 当密码库

配置文件和 Registry 通常可被用户或管理员读取。秘密信息使用系统安全存储。

### 忘记 `sync()` 就假设数据已落盘

在应用崩溃、系统断电或其他进程读取场景下，不要依赖未同步的内存状态。

### 读取配置不做范围校验

用户可以直接编辑 INI。对数字、路径、枚举和列表长度设定上限。

### 在组内提前返回

这会留下错误的 group 前缀。让 begin/end 成对出现，或在小函数中封装读写。

### 频繁每帧写设置

窗口拖动、光标移动等高频信号不要每次都 `setValue()` 和 `sync()`。在状态稳定或退出时批量保存。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSettings()` | 按应用元数据创建默认配置对象。 | 组织名、应用名应在构造前设置；默认位置由平台决定。 |
| 构造 | `QSettings(QString organization, QString application)` | 按组织和应用身份选择设置存储。 | 两个字符串影响默认路径和系统集成。 |
| 构造 | `QSettings(Scope, QString, QString)` | 指定用户或系统作用域创建设置对象。 | SystemScope 可能需要权限，读到的内容不一定可信。 |
| 构造 | `QSettings(Format, Scope, QString, QString)` | 同时固定格式和作用域。 | 跨平台文件格式通常选 IniFormat；注意迁移策略。 |
| 构造 | `QSettings(QString fileName, Format)` | 直接操作指定配置文件。 | 父目录可能不存在；路径和权限由调用者负责。 |
| 析构 | `~QSettings()` | 释放设置对象状态。 | 重要修改应在析构前显式 sync，避免把落盘时机交给不明显的生命周期。 |
| 写入 | `setValue(key, value)` | 设置一个键值。 | QVariant 类型应稳定；写入外部输入前先规范化。 |
| 读取 | `value(key)` | 获取键值，缺失时返回无效 QVariant。 | 检查 `isValid()` 并验证类型。 |
| 读取 | `value(key, defaultValue)` | 获取键值，缺失时返回默认值。 | 默认值也要与业务范围一致。 |
| 删除 | `remove(key)` | 删除指定键或组前缀下的内容。 | 删除前确认 key 路径；不会自动迁移旧版本数据。 |
| 查询 | `contains(key)` | 判断设置中是否存在键。 | 存在不代表值类型正确或值满足业务约束。 |
| 组 | `beginGroup(prefix)` | 为后续 key 增加组前缀。 | 必须与 `endGroup()` 配对，尤其注意提前 return。 |
| 组 | `endGroup()` | 退出当前设置组。 | 不能多调用；组嵌套要保持清晰。 |
| 组 | `group()` | 返回当前组前缀。 | 主要用于诊断和构造动态 key。 |
| 数组 | `beginWriteArray(prefix, size)` | 开始写入数组设置。 | 用 `setArrayIndex()` 写每个元素，结束时必须 `endArray()`。 |
| 数组 | `beginReadArray(prefix)` | 开始读取数组并返回元素数量。 | 数量来自配置，读取前要限制最大数量。 |
| 数组 | `setArrayIndex(int)` | 选择当前数组元素索引。 | 索引越界会形成错误 key 或空值，按返回 count 遍历。 |
| 数组 | `endArray()` | 结束数组读写上下文。 | 与 beginReadArray/beginWriteArray 配对。 |
| 枚举键 | `allKeys()` | 返回当前作用域可见的所有键。 | 可能包含回退源；大配置读取会有成本。 |
| 枚举键 | `childKeys()` | 返回当前组的直接键。 | 不递归列出子组中的所有键。 |
| 枚举组 | `childGroups()` | 返回当前组的直接子组。 | 结果是快照，配置可能随后改变。 |
| 同步 | `sync()` | 将修改写出，并刷新外部修改到内存。 | 检查 status；频繁调用会增加 I/O 和竞态。 |
| 状态 | `status()` | 返回 NoError、AccessError 或 FormatError。 | 文本设置错误要记录日志；不要只看 sync 返回无返回值。 |
| 状态 | `isWritable()` | 判断当前配置源是否可写。 | 只是一种能力检查，实际写入仍可能失败。 |
| 状态 | `isAtomicSyncRequired()` | 查询是否要求原子同步。 | 平台和格式相关；不是通用事务保证。 |
| 状态 | `setAtomicSyncRequired(bool)` | 请求原子同步策略。 | 可能增加临时文件和写入成本；失败时要处理状态。 |
| 回退 | `fallbacksEnabled()` | 查询是否启用回退设置。 | 只影响查找来源，不改变已有内存值。 |
| 回退 | `setFallbacksEnabled(bool)` | 开启或关闭回退查找。 | 测试和隔离配置时有用；注意系统设置影响。 |
| 信息 | `fileName()` | 返回实际使用的配置文件名。 | NativeFormat 可能是平台存储路径；不要假设一定是普通文件。 |
| 信息 | `format()` / `scope()` | 查询配置格式和作用域。 | 适合诊断部署行为。 |
| 信息 | `organizationName()` / `applicationName()` | 查询配置身份。 | 与 QCoreApplication 的元数据和构造参数相关。 |
| 全局 | `setDefaultFormat(Format)` / `defaultFormat()` | 设置或查询无参 QSettings 的默认格式。 | 应在创建设置对象前设置；全局状态会影响其他代码。 |
| 全局 | `setPath(Format, Scope, QString)` | 为格式和作用域设置自定义基础路径。 | 进程全局配置；库不应随意修改宿主路径。 |
| 扩展 | `registerFormat(extension, read, write, caseSensitivity)` | 注册自定义设置格式。 | 读写函数要定义完整格式契约和错误处理。 |
| 枚举 | `Format` | 表示 Native、INI、Registry、Web 和自定义格式。 | 具体可用项依平台编译配置。 |
| 枚举 | `Scope` | 表示 UserScope 或 SystemScope。 | 系统范围设置可能需要权限并受管理员控制。 |
| 枚举 | `Status` | 表示无错误、访问错误或格式错误。 | 把错误当作正常配置恢复流程处理。 |

---

### 一句话总结

`QSettings` 适合轻量偏好和配置，不是秘密存储、数据库或并发事务系统。先确定配置位置和作用域，再用稳定 key、默认值、范围校验、显式 `sync()` 和版本迁移把它用稳。
