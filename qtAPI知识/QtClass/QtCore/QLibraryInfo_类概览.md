# Qt QLibraryInfo 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QLibraryInfo>`  
> 所属模块：`Qt6::Core`  
> 形式：静态信息查询类  
> 相关类型：`QLibraryInfo::LibraryPath`、`QVersionNumber`、`QStringList`

## 1. 先给结论：它解决什么问题

`QLibraryInfo` 用于查询**当前进程实际使用的 Qt 构建信息、版本信息和安装路径**。

它主要回答这些运行时问题：

- 当前 Qt 是 Debug 构建还是 Release 构建；
- 当前 Qt 是动态构建还是静态构建；
- 当前加载的 Qt 版本是多少；
- Qt 的插件、翻译文件、QML 导入目录和工具目录在哪里；
- `qt.conf` 是否覆盖了 Qt 编译时写入的路径；
- 平台插件在 `qt.conf` 中配置了哪些额外参数。

它不是：

- 用来管理普通共享库的类，普通动态库加载应看 `QLibrary`；
- 用来修改 Qt 安装目录的配置器；
- 用来判断应用程序自身是 Debug 还是 Release 的通用 API；
- 用来保证某个插件、翻译文件或 QML 模块一定存在；
- 用来替代构建系统提供的 `QT_VERSION`、`QT_VERSION_STR` 等编译期宏。

`QLibraryInfo` 的构造函数是 private，不能创建实例。它是一个只提供静态函数的工具类：

```cpp
const QVersionNumber qtVersion = QLibraryInfo::version();
const QString pluginPath =
    QLibraryInfo::path(QLibraryInfo::PluginsPath);
```

## 2. 最小可用代码

```cpp
#include <QLibraryInfo>
#include <QDebug>

void printQtRuntimeInfo()
{
    qDebug() << "Qt version:" << QLibraryInfo::version();
    qDebug() << "Debug build:" << QLibraryInfo::isDebugBuild();
    qDebug() << "Shared build:" << QLibraryInfo::isSharedBuild();
    qDebug() << "Plugins:" << QLibraryInfo::path(
                    QLibraryInfo::PluginsPath);
}
```

查询路径时，如果一个路径类别在 `qt.conf` 中配置了多个目录，`path()` 只返回第一个路径；需要完整列表时使用 Qt 6.8 引入的 `paths()`：

```cpp
const QStringList pluginPaths =
    QLibraryInfo::paths(QLibraryInfo::PluginsPath);
```

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QLibraryInfo>
```

### 3.3 qmake

```qmake
QT += core
```

`QLibraryInfo` 通常不需要显式创建 `QCoreApplication` 才能调用。路径结果来自当前 Qt 构建和可能存在的 `qt.conf`；但如果你的程序还要使用插件、翻译或平台插件，仍应按照对应 Qt 子系统的初始化要求组织调用时机。

## 4. 它和编译期版本信息的区别

### 4.1 `QLibraryInfo::version()`：查询运行时 Qt

```cpp
const QVersionNumber runtimeVersion = QLibraryInfo::version();
```

它返回当前程序实际使用的 Qt 库版本。动态链接程序尤其应该用它确认运行时加载到的 Qt。

### 4.2 `QT_VERSION` 和 `QT_VERSION_STR`：编译期 Qt

```cpp
qDebug() << QT_VERSION_STR;
```

这些宏反映编译当前源文件时使用的 Qt 头文件版本，不等价于运行时一定加载的 Qt 版本。

因此，诊断部署问题时可以同时输出：

```cpp
qDebug() << "Header Qt:" << QT_VERSION_STR;
qDebug() << "Runtime Qt:" << QLibraryInfo::version();
```

如果两者不一致，说明程序的构建环境和运行时库环境可能不同，继续排查库搜索路径、部署目录和 `qt.conf`。

### 4.3 `qVersion()`

`qVersion()` 也用于获取 Qt 版本字符串。`QLibraryInfo::version()` 返回结构化的 `QVersionNumber`，更适合进行版本比较；`qVersion()` 更适合日志和简单展示。

## 5. Qt 路径配置的整体模型

Qt 的路径不是简单地“从可执行文件旁边拼一个固定目录”。它通常由以下信息共同决定：

1. Qt 构建时写入的默认路径；
2. 应用部署位置；
3. `qt.conf` 或版本化的 `qt6.conf`；
4. 当前平台的应用包布局；
5. 某些路径类别配置的多个目录。

`QLibraryInfo` 提供对这些最终路径的查询入口。

### 5.1 `qt.conf` 的作用

`qt.conf` 是 INI 格式配置文件，可以覆盖 Qt 库中编译时写入的路径。Qt 文档列出的查找位置包括：

- 资源系统中的 `:/qt/etc/qt.conf`；
- macOS 应用包的 Resources 目录；
- 包含应用程序可执行文件的目录。

如果同一位置存在 `qt6.conf` 和 `qt.conf`，Qt 6 使用 `qt6.conf`。

一个最小的 `qt.conf` 例子：

```ini
[Paths]
Prefix = .
Plugins = plugins
Translations = translations
```

路径项通常相对于 `Prefix` 解释；绝对路径则按配置中的绝对路径使用。

### 5.2 查询结果不代表目录存在

```cpp
const QString path =
    QLibraryInfo::path(QLibraryInfo::TranslationsPath);
```

返回一个配置或推导出的路径，不保证目录当前存在，也不保证目录下已经部署了目标文件。要判断实际文件，仍需配合 `QDir`、`QFileInfo` 或对应模块的加载 API。

### 5.3 `path()` 与 `paths()`

`path()` 适合 Qt 只需要一个搜索根目录的场景：

```cpp
const QString pluginPath =
    QLibraryInfo::path(QLibraryInfo::PluginsPath);
```

如果 `qt.conf` 中同一项包含多个目录，`path()` 只返回第一个。`paths()` 返回全部路径：

```cpp
for (const QString &path :
     QLibraryInfo::paths(QLibraryInfo::PluginsPath)) {
    qDebug() << path;
}
```

不要用 `path()` 推断“Qt 只配置了一个搜索目录”。

## 6. 实际使用场景

### 6.1 诊断插件部署

```cpp
const QStringList pluginRoots =
    QLibraryInfo::paths(QLibraryInfo::PluginsPath);

for (const QString &root : pluginRoots)
    qDebug().noquote() << "Qt plugin root:" << root;
```

这能帮助定位“平台插件找不到”或“图片格式插件未部署”等问题。但输出路径不会自动把目录加入所有 Qt 的搜索机制；具体插件搜索还要看 `QCoreApplication::addLibraryPath()` 等 API。

### 6.2 加载翻译文件

```cpp
const QString translationsPath =
    QLibraryInfo::path(QLibraryInfo::TranslationsPath);

const QString fileName =
    translationsPath + QStringLiteral("/qt_zh_CN.qm");
```

这只是得到 Qt 的翻译目录。应用自己的翻译文件可能位于应用目录或自定义资源中，不应无条件假设和 Qt 翻译放在同一目录。

### 6.3 定位 QML 导入目录

```cpp
const QStringList qmlPaths =
    QLibraryInfo::paths(QLibraryInfo::QmlImportsPath);
```

`QmlImportsPath` 表示安装的 QML 扩展导入路径。`Qml2ImportsPath` 是兼容旧命名的别名，新的代码优先使用 `QmlImportsPath`。

### 6.4 输出运行时构建诊断

```cpp
qDebug().noquote()
    << "Qt build:" << QLibraryInfo::build()
    << "version:" << QLibraryInfo::version()
    << "debug:" << QLibraryInfo::isDebugBuild()
    << "shared:" << QLibraryInfo::isSharedBuild();
```

这类信息适合写入启动日志、崩溃报告和支持工单。`build()` 是构建信息字符串，不应当替代 `version()` 做版本比较。

### 6.5 读取平台插件参数

```cpp
const QStringList arguments =
    QLibraryInfo::platformPluginArguments(QStringLiteral("windows"));

for (const QString &argument : arguments)
    qDebug() << argument;
```

该函数读取 `qt.conf` 的 `[Platforms]` 配置。平台名为 `windows` 时，对应的配置键是 `WindowsArguments`；平台名为 `xcb` 时，对应 `XcbArguments`。

例如：

```ini
[Platforms]
WindowsArguments = fontengine=freetype
```

应用通常不需要手动消费这些参数；它们主要供 Qt 平台插件启动时读取。直接修改或重复解释参数，可能让应用行为和 Qt 自身的配置产生分歧。

## 7. `LibraryPath` 枚举

`LibraryPath` 用于指定要查询哪一种 Qt 安装路径：

| 枚举值 | 数值 | 含义 | 使用重点 |
| --- | ---: | --- | --- |
| `PrefixPath` | `0` | 所有路径的默认前缀。 | 常作为其他相对路径的基准。 |
| `DocumentationPath` | `1` | Qt 安装后的文档目录。 | 目标部署通常不一定包含文档。 |
| `HeadersPath` | `2` | Qt 头文件目录。 | 运行时应用通常不应依赖它。 |
| `LibrariesPath` | `3` | 已安装 Qt 库目录。 | 不等于当前进程所有依赖库的搜索路径。 |
| `LibraryExecutablesPath` | `4` | Qt 库运行时需要的辅助可执行文件目录。 | 用于 Qt 安装布局，不等于应用可执行文件目录。 |
| `BinariesPath` | `5` | Qt 工具和应用程序等二进制文件目录。 | 适合诊断 Qt 安装。 |
| `PluginsPath` | `6` | Qt 插件安装目录。 | 仅返回路径，不负责注册搜索路径。 |
| `QmlImportsPath` | `7` | QML 扩展导入目录。 | 新代码优先使用此名称。 |
| `Qml2ImportsPath` | `7` | `QmlImportsPath` 的兼容别名。 | 文档标记为过时，使用 `QmlImportsPath`。 |
| `ArchDataPath` | `8` | 与架构相关的 Qt 数据目录。 | 和平台/架构相关的数据放置有关。 |
| `DataPath` | `9` | 与架构无关的 Qt 通用数据目录。 | 不等于应用自己的数据目录。 |
| `TranslationsPath` | `10` | Qt 字符串翻译信息目录。 | 应用翻译可能使用其他目录。 |
| `ExamplesPath` | `11` | Qt 安装后的示例目录。 | 发行版通常不会部署它。 |
| `TestsPath` | `12` | Qt 安装后的测试用例目录。 | 通常只在开发环境有意义。 |
| `SettingsPath` | `100` | Qt 设置目录。 | Windows 上不适用。 |

`Qml2ImportsPath` 与 `QmlImportsPath` 是同一个枚举值，不是两个独立搜索目录。

## 8. 构建类型信息

### 8.1 `isDebugBuild()`

```cpp
if (QLibraryInfo::isDebugBuild()) {
    qDebug() << "Qt was built with debugging enabled";
}
```

它回答的是“当前 Qt 构建是否启用了调试”，不是“当前应用的编译器宏是否定义了 `_DEBUG`”。

不要用它决定所有应用逻辑。应用和 Qt 可能以不同配置构建，生产功能通常应由明确的应用配置或能力检测控制。

### 8.2 `isSharedBuild()`

```cpp
const bool usesSharedQt = QLibraryInfo::isSharedBuild();
```

它返回当前 Qt 是否为共享库构建。该函数从 Qt 6.5 开始提供。

它不直接回答：

- 当前某一个 Qt 模块文件的具体路径；
- 应用是否静态链接了自己的第三方库；
- 某个插件是否一定能被加载；
- 目标机器是否安装了开发文件。

## 9. 逐项 API 说明

### 9.1 `const char *build() noexcept`

```cpp
static const char *build() noexcept;
```

返回 Qt 构建信息字符串。

使用时注意：

- 返回类型是 `const char *`，调用方不要释放或修改它；
- 适合日志、诊断和环境报告；
- 它不是结构化版本对象；
- 要比较 Qt 版本，使用 `version()`；
- 具体字符串内容属于 Qt 构建信息，不应写死为固定格式。

```cpp
qDebug().noquote() << QLibraryInfo::build();
```

### 9.2 `bool isDebugBuild() noexcept`

```cpp
static bool isDebugBuild() noexcept;
```

如果当前 Qt 是启用调试的构建，返回 `true`；如果是 Release 构建，返回 `false`。

它反映 Qt 本身，而不是应用程序自身的构建模式。

### 9.3 `bool isSharedBuild() noexcept`

```cpp
static bool isSharedBuild() noexcept;
```

如果当前 Qt 是共享库构建，返回 `true`；否则返回 `false`。

该 API 从 Qt 6.5 开始提供。需要支持更低 Qt 版本时，应使用版本条件或其他兼容方案。

### 9.4 `QVersionNumber version() noexcept`

```cpp
static QVersionNumber version() noexcept;
```

返回当前运行时 Qt 库的版本。

```cpp
const QVersionNumber version = QLibraryInfo::version();
if (version >= QVersionNumber(6, 8))
    useNewBehavior();
```

它比对字符串更适合版本比较。需要区分编译期和运行时版本时，同时输出 `QT_VERSION_STR` 和本函数的结果。

### 9.5 `QString path(QLibraryInfo::LibraryPath p)`

```cpp
static QString path(QLibraryInfo::LibraryPath p);
```

返回枚举 `p` 指定的 Qt 路径。

边界：

- Qt 6.0 开始提供；
- 如果 `qt.conf` 为该项配置了多个路径，只返回第一个；
- 返回路径不保证存在；
- `SettingsPath` 在 Windows 上不适用；
- 路径可能受 `qt.conf`、平台布局和部署位置影响。

```cpp
const QString path =
    QLibraryInfo::path(QLibraryInfo::PluginsPath);
```

### 9.6 `QStringList paths(QLibraryInfo::LibraryPath p)`

```cpp
static QStringList paths(QLibraryInfo::LibraryPath p);
```

返回枚举 `p` 指定的全部 Qt 路径。

该函数从 Qt 6.8 开始提供。对于可能在 `qt.conf` 中配置多个目录的项目，使用它而不是假设 `path()` 已经包含完整搜索列表。

```cpp
const QStringList paths =
    QLibraryInfo::paths(QLibraryInfo::PluginsPath);
```

如果没有配置有效路径，返回的列表可能为空；不要把空列表当成 Qt 安装损坏，先结合具体路径类别和平台判断。

### 9.7 `QStringList platformPluginArguments(const QString &platformName)`

```cpp
static QStringList platformPluginArguments(
    const QString &platformName);
```

读取指定平台插件在 `qt.conf` 中配置的参数列表。

参数名的形成规则是：平台插件名称首字母大写，再加上 `Arguments`。例如：

```text
platformName = "windows"
配置键       = "WindowsArguments"
```

配置示例：

```ini
[Platforms]
WindowsArguments = fontengine=freetype,verbose=true
```

该函数返回解析后的参数列表。没有对应配置时通常得到空列表。参数内容和含义由平台插件解释，`QLibraryInfo` 不负责验证每个参数是否有效。

### 9.8 `using LibraryLocation = LibraryPath`

```cpp
using LibraryLocation = LibraryPath;
```

这是旧 API 的兼容别名，Qt 6.0 起弃用。新代码直接使用 `LibraryPath`。

### 9.9 `QString location(LibraryLocation location)`

```cpp
static QString location(LibraryLocation location);
```

这是旧的路径查询名称，Qt 6.0 起弃用，等价于使用 `path()`：

```cpp
const QString oldStyle =
    QLibraryInfo::location(QLibraryInfo::PluginsPath);

const QString currentStyle =
    QLibraryInfo::path(QLibraryInfo::PluginsPath);
```

新代码使用 `path()`；如果要获得多个路径，则使用 Qt 6.8 起的 `paths()`。

## 10. `qt.conf` 路径覆盖示例

假设应用目录为：

```text
myapp/
  myapp.exe
  qt.conf
  plugins/
  translations/
```

`qt.conf` 可以写成：

```ini
[Paths]
Prefix = .
Plugins = plugins
Translations = translations
```

应用中查询：

```cpp
const QString pluginPath =
    QLibraryInfo::path(QLibraryInfo::PluginsPath);
const QString translationPath =
    QLibraryInfo::path(QLibraryInfo::TranslationsPath);

qDebug() << pluginPath << translationPath;
```

这里的相对路径会根据 Qt 的 `Prefix` 规则解释。不要仅凭当前工作目录拼接路径，因为应用从快捷方式、服务管理器或其他工作目录启动时，当前工作目录可能不同。

## 11. 常见误区与排查顺序

### 11.1 把 `version()` 当成头文件版本

`QLibraryInfo::version()` 查询运行时 Qt；`QT_VERSION_STR` 反映编译期头文件。动态部署问题应同时记录两者。

### 11.2 把 `isDebugBuild()` 当成应用 Debug 状态

它只描述 Qt 构建本身。应用和 Qt 可以用不同配置构建，不能用它替代应用自己的构建标志。

### 11.3 认为 `path()` 一定是唯一完整路径

`path()` 在多路径配置下只返回第一项。需要全部搜索路径时使用 `paths()`。

### 11.4 认为返回路径一定存在

`QLibraryInfo` 报告的是 Qt 配置路径，不负责创建目录，也不保证部署文件已经复制到那里。实际使用前检查目录或让对应加载器报告错误。

### 11.5 用 `QLibraryInfo` 修改插件搜索路径

`QLibraryInfo::path()` 和 `paths()` 只是查询。需要改变应用插件搜索路径时，应研究 `QCoreApplication::addLibraryPath()`、`setLibraryPaths()` 等 API。

### 11.6 把 `PluginsPath` 当成所有插件都在同一级目录

Qt 插件通常还按类型放在 `platforms`、`imageformats`、`styles` 等子目录。得到 `PluginsPath` 后，仍要遵守各插件类别的目录结构。

### 11.7 忽略 `qt.conf`

开发机上得到的硬编码安装路径，和部署包中通过 `qt.conf` 覆盖后的路径可能完全不同。排查插件或翻译问题时，应记录实际的 `QLibraryInfo` 查询结果。

### 11.8 把 `Qml2ImportsPath` 当作新 API

它是旧命名的兼容别名，使用 `QmlImportsPath` 更清楚。

### 11.9 把 `SettingsPath` 用在 Windows

文档明确说明 `SettingsPath` 不适用于 Windows。跨平台代码应为该枚举值提供平台分支，不要假设总能得到有意义的目录。

### 11.10 手动重复解释平台插件参数

`platformPluginArguments()` 读取的是给平台插件的配置。应用如果自行解析并再次应用，可能造成参数重复或语义冲突；除非确实在实现自定义平台集成，否则通常只让 Qt 平台插件消费它。

### 11.11 用字符串比较版本

字符串比较会把 `6.10` 和 `6.9` 的顺序处理错。使用 `QVersionNumber` 比较：

```cpp
if (QLibraryInfo::version() >= QVersionNumber(6, 10))
    useFeature();
```

## 12. 与相关 API 的分工

| 需求 | 更合适的 API |
| --- | --- |
| 查询当前运行时 Qt 版本 | `QLibraryInfo::version()` |
| 查询 Qt 安装路径 | `QLibraryInfo::path()` / `paths()` |
| 修改应用插件搜索路径 | `QCoreApplication::addLibraryPath()` / `setLibraryPaths()` |
| 加载普通共享库 | `QLibrary` |
| 加载 Qt 插件实例 | `QPluginLoader` |
| 查询操作系统和 CPU 信息 | `QSysInfo` |
| 比较结构化版本号 | `QVersionNumber` |
| 读取编译期 Qt 版本 | `QT_VERSION` / `QT_VERSION_STR` |
| 获取简单版本字符串 | `qVersion()` |

## API 速查表
### 13.1 构建和版本信息

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `static const char *build() noexcept` | 返回 Qt 构建信息字符串。 | 只用于诊断和日志；不要当版本号比较；不要释放返回指针。 |
| `static bool isDebugBuild() noexcept` | 判断当前 Qt 是否为 Debug 构建。 | 描述 Qt，不描述应用自身构建模式。 |
| `static bool isSharedBuild() noexcept` | 判断当前 Qt 是否为共享库构建。 | Qt 6.5 起提供；不等于所有依赖都能加载。 |
| `static QVersionNumber version() noexcept` | 返回当前运行时 Qt 版本。 | 与 `QT_VERSION_STR` 区分；适合结构化比较。 |

### 13.2 路径查询

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `static QString path(LibraryPath p)` | 返回指定类别的 Qt 路径。 | 多路径配置时只返回第一项；路径不保证存在。 |
| `static QStringList paths(LibraryPath p)` | 返回指定类别的全部 Qt 路径。 | Qt 6.8 起提供；可能返回空列表。 |
| `LibraryPath` | 路径类别枚举。 | `Qml2ImportsPath` 是兼容别名；`SettingsPath` 不适用于 Windows。 |

### 13.3 平台插件配置

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `static QStringList platformPluginArguments(const QString &platformName)` | 读取 `qt.conf` `[Platforms]` 中指定平台的参数。 | 键名按首字母大写的平台名加 `Arguments` 生成；参数由平台插件解释。 |

### 13.4 过时兼容 API

| API | 状态 | 新代码 |
| --- | --- | --- |
| `using LibraryLocation = LibraryPath` | Qt 6.0 起弃用。 | 使用 `LibraryPath`。 |
| `static QString location(LibraryLocation location)` | Qt 6.0 起弃用。 | 使用 `path()`；需要多项时使用 `paths()`。 |

### 13.5 `LibraryPath` 常量

| 常量 | 数值 | 查询内容 |
| --- | ---: | --- |
| `PrefixPath` | `0` | 默认路径前缀。 |
| `DocumentationPath` | `1` | 文档目录。 |
| `HeadersPath` | `2` | 头文件目录。 |
| `LibrariesPath` | `3` | Qt 库目录。 |
| `LibraryExecutablesPath` | `4` | Qt 库需要的辅助可执行文件目录。 |
| `BinariesPath` | `5` | Qt 工具和应用二进制目录。 |
| `PluginsPath` | `6` | Qt 插件目录。 |
| `QmlImportsPath` | `7` | QML 导入目录。 |
| `Qml2ImportsPath` | `7` | `QmlImportsPath` 的旧别名。 |
| `ArchDataPath` | `8` | 架构相关数据目录。 |
| `DataPath` | `9` | 架构无关数据目录。 |
| `TranslationsPath` | `10` | Qt 翻译目录。 |
| `ExamplesPath` | `11` | 示例目录。 |
| `TestsPath` | `12` | 测试目录。 |
| `SettingsPath` | `100` | Qt 设置目录，Windows 不适用。 |

## 14. 最后的选型规则

1. 查询运行时 Qt 版本时使用 `QLibraryInfo::version()`，不要只看编译期宏。
2. 查询一个路径用 `path()`，可能存在多个路径时用 `paths()`。
3. 把返回路径当作配置结果，不要假设目录或文件一定存在。
4. 排查部署问题时检查 `qt.conf` 和 `qt6.conf` 的覆盖效果。
5. `PluginsPath` 是插件根目录，不自动替代插件搜索路径设置。
6. `Qml2ImportsPath` 是旧别名，新代码使用 `QmlImportsPath`。
7. `isDebugBuild()` 和 `isSharedBuild()` 描述 Qt 构建，不是应用所有依赖的状态。
8. `build()` 适合写入诊断日志，版本比较使用 `QVersionNumber`。
9. 普通共享库用 `QLibrary`，Qt 插件用 `QPluginLoader`。
10. 让平台插件消费 `platformPluginArguments()` 的配置，避免应用重复解释同一组参数。

`QLibraryInfo` 的核心价值是把“当前 Qt 到底来自哪里、是什么构建、有哪些运行时路径”变成可查询的信息。它最适合用于部署诊断、插件和翻译路径定位，以及运行环境报告；它报告配置，不替你完成文件部署、插件注册或动态库加载。
