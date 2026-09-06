# QStandardPaths

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QStandardPaths` 是 文件、设备与流机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QStandardPaths` 是 文件、设备与流机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QStandardPaths>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

### 状态、生命周期和线程

**生命周期：** 先设置路径或设备，再 open，成功后读写/定位/刷新，最后 close；析构通常会关闭设备，但关键写入应显式 flush/close 并检查错误。相对路径依赖当前工作目录，资源路径和用户文件路径要区分。

**状态与结果：** 区分设备未打开、打开成功、到达 EOF、暂时无数据、读写失败和写入尚未落盘。`readAll()` 方便小数据但可能占用大量内存，大文件应分块处理并检查返回值。

**线程与事件循环：** 同一个打开设备不要跨线程并发使用，除非类明确保证线程安全；后台 I/O 通过 worker 或异步设备处理，GUI 线程只接收结果。

## 3. 直接使用

构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
QFile file(path);
if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    const QByteArray data = file.readAll();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum LocateOption { LocateFile, LocateDirectory }`
- `flags LocateOptions`
- `enum StandardLocation { DesktopLocation, DocumentsLocation, FontsLocation, ApplicationsLocation, MusicLocation, …, GenericStateLocation }`

### 静态公有成员

- `QString displayName(QStandardPaths::StandardLocation type)`
- `QString findExecutable(const QString &executableName, const QStringList &paths = QStringList())`
- `QString locate(QStandardPaths::StandardLocation type, const QString &fileName, QStandardPaths::LocateOptions options = LocateFile)`
- `QStringList locateAll(QStandardPaths::StandardLocation type, const QString &fileName, QStandardPaths::LocateOptions options = LocateFile)`
- `void setTestModeEnabled(bool testMode)`
- `QStringList standardLocations(QStandardPaths::StandardLocation type)`
- `QString writableLocation(QStandardPaths::StandardLocation type)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QStandardPaths::LocateOptionflags QStandardPaths::LocateOptions`

**作用与语义：**

本枚举描述了可用于控制`QStandardPaths::locate`和 `QStandardPaths::locateAll`行为的不同标志。
- `QStandardPaths::LocateFile`：`0x0`;仅返回文件
- `QStandardPaths::LocateDirectory`：`0x1`;仅返回目录
LocateOptions 类型是 QFlags 的 typedef<LocateOption>。它存储 LocateOption 值的 OR 组合。

### `enum QStandardPaths::StandardLocation`

**作用与语义：**

该枚举描述了可以使用`QStandardPaths::writableLocation`、`QStandardPaths::standardLocations`和`QStandardPaths::displayName`等方法查询的不同位置。
该枚举中的部分值代表用户配置。这些枚举值在不同应用中会返回相同的路径，因此可用于与其他应用共享数据。其他值则针对该应用。下表中的每个枚举值说明它是应用程序特定值还是通用值。
应用专用目录应假设其他应用程序无法访问。因此，放置于该目录的文件可能无法被其他应用程序读取，即使同一用户运行。另一方面，通用目录应假设该用户运行的所有应用程序都能访问，但应仍假设其他用户无法访问应用程序。
与其他用户的数据交换不在`QStandardPaths`范围内。
- `QStandardPaths::DesktopLocation`：`0`;返回用户的桌面目录。这是一个通用值。在没有桌面概念的系统中，这与QStandardPaths：：HomeLocation相同。
- `QStandardPaths::DocumentsLocation`：`1`;返回包含用户文档文件的目录。这是一个通用值。返回的路径永远不会是空的。
- `QStandardPaths::FontsLocation`：`2`;返回包含用户字体的目录。这是一个通用值。请注意，安装字体可能需要额外的平台特定操作。
- `QStandardPaths::ApplicationsLocation`：`3`;返回包含用户应用程序的目录（可执行文件、应用包或快捷方式）。这是一个通用值。请注意，安装应用程序可能需要额外的平台特定操作。该目录中的文件、文件夹或快捷方式是平台特定的。
- `QStandardPaths::MusicLocation`：`4`;返回包含用户音乐或其他音频文件的目录。这是一个通用值。如果没有专门存放音乐文件的目录，则返回一个合理的用户文档存储备份。
- `QStandardPaths::MoviesLocation`：`5`;返回包含用户电影和视频的目录。这是一个通用值。如果不存在专门用于电影文件的目录，则返回一个合理的用户文档存储备份。
- `QStandardPaths::PicturesLocation`：`6`;返回包含用户照片的目录。这是一个通用值。如果没有专门用于图片文件的目录，则返回一个合理的用户文档存储备份。
- `QStandardPaths::TempLocation`：`7`;返回一个可存储临时文件的目录。返回的值可能是应用程序特定的，也可以是该用户的其他应用程序共享，甚至是系统范围的。返回路径永远不会是空的。
- `QStandardPaths::HomeLocation`：`8`;返回用户的主目录（与`QDir::homePath()`相同）。在Unix系统中，这等于HOME环境变量。该值可能是通用的或特定应用的，但返回路径从不空。
- `QStandardPaths::AppLocalDataLocation`：`9`;返回Windows操作系统的本地设置路径。在所有其他平台上，返回的值与AppDataLocation相同。该枚举值是在Qt 5.4中添加的。
- `QStandardPaths::CacheLocation`：`10`;返回一个目录位置，应写入用户特定的非必要（缓存）数据。这是一个应用程序特定的目录。返回路径永远不会为空。
- `QStandardPaths::GenericCacheLocation`：`15`;返回一个目录位置，应写入用户特定的非必要（缓存）数据，这些数据在应用间共享。这是一个通用值。注意，如果系统没有共享缓存的概念，返回路径可能是空的。
- `QStandardPaths::GenericDataLocation`：`11`;返回一个目录位置，用于存储跨应用共享的持久数据。这是一个通用值。返回的路径从未为空。
- `QStandardPaths::RuntimeLocation`：`12`;返回一个目录位置，用于编写运行时通信文件，如Unix本地套接字。这是一个通用值。在某些系统上，返回路径可能是空的。
- `QStandardPaths::ConfigLocation`：`13`;返回一个目录位置，用户专用配置文件应在此编写。该位置可以是通用值或应用程序特定值，返回路径永远不会是空的。
- `QStandardPaths::DownloadLocation`：`14`;返回用户下载文件目录。这是一个通用值。如果不存在专门用于下载的目录，则返回一个合理的用户文档存储备份。
- `QStandardPaths::GenericConfigLocation`：`16`;返回一个目录位置，多个应用程序之间共享的用户特定配置文件应在此写入。这是一个通用值，返回路径永远不会是空的。
- `QStandardPaths::AppDataLocation`：`17`;返回一个目录位置，可以存储持久应用数据。这是一个应用程序特定的目录。要获取存储数据的路径以便与其他应用程序共享，请使用 QStandardPaths：：GenericDataLocation。返回的路径永远不会是空的。在 Windows 操作系统上，这会返回漫游路径。该枚举值是在 Qt 5.4 中添加的。
- `QStandardPaths::AppConfigLocation`：`18`;返回一个目录位置，用户特定的配置文件应在此编写。这是一个应用程序特定的目录，返回路径永远不会是空的。该枚举值是在Qt 5.5中添加的。
- `QStandardPaths::PublicShareLocation`：`19`;返回一个目录位置，用于存储用户特定的公开共享文件和目录。这是一个通用值。注意，如果系统没有公共共享位置的概念，返回路径可能是空的。该枚举值是在Qt 6.4中添加的。
- `QStandardPaths::TemplatesLocation`：`20`;返回一个目录位置，用于存储用户专用的模板文件。这是一个通用值。注意，如果系统不了解模板位置，返回路径可能是空的。该枚举值是在Qt 6.4中添加的。
- `QStandardPaths::StateLocation (since Qt 6.7)`：`21`;返回一个目录位置，用户特定的应用状态文件应在此写入。这是一个应用程序特定的目录，返回路径永远不会是空的。
- `QStandardPaths::GenericStateLocation (since Qt 6.7)`：`22`;返回一个目录位置，应用间应写入共享状态数据文件。该值可能是通用的或应用特定的，但返回路径从不空。
下表给出了不同操作系统上的路径示例。第一条路径是可写路径（除非特别注明）。其他额外路径（如有）表示不可写位置。
- `Path type`：macOS;Windows
- `DesktopLocation`：“~/桌面”;“C：/用户/<USER>/桌面”
- `DocumentsLocation`：“~/文档”;“C：/用户/<USER>/文档”
- `FontsLocation`：“/System/Library/Fonts”（不可写）;“C：/Windows/Fonts”（不可写）
- `ApplicationsLocation`：“/应用程序”（不可写写）;“C：/用户/<USER>/应用数据/漫游/Microsoft/Windows/开始菜单/程序”
- `MusicLocation`：“~/音乐”;“C：/用户/<USER>/音乐”
- `MoviesLocation`：“~/电影”;“C：/用户/<USER>/视频”
- `PicturesLocation`：“~/图片”;“C：/用户/<USER>/图片”
- `TempLocation`：由操作系统随机生成;“C：/用户/<USER>/AppData/本地/临时”
- `HomeLocation`：“~”;“C：/用户<USER>/”
- `AppLocalDataLocation`：“~/库/应用支持/<APPNAME>”，“/库/应用支持/<APPNAME>”。<APPDIR>/../资源“;”C：/用户/<USER>/AppData/本地<APPNAME>/“，”C：/ProgramData/<APPNAME>“，”<APPDIR>“，”/<APPDIR>数据“，”<APPDIR>/data/<APPNAME>”
- `CacheLocation`：“~/Library/Caches/<APPNAME>”，“/Library/Caches/<APPNAME>”;C：/Users/<USER>/AppData/Local/<APPNAME>/cache”
- `StateLocation`：“~/Library/Preferences/<APPNAME>/State”;“C：/Users/<USER>/AppData/Local/<APPNAME>/State”，“C：/ProgramData/<APPNAME>/状态”
- `GenericDataLocation`：“~/Library/Application Support”，“/Library/Application Support”;“C：/Users/<USER>/AppData/Local”，“C：/ProgramData”，“<APPDIR>”“，”<APPDIR>/data”
- `RuntimeLocation`：“~/库/应用支持”;“C：/用户/<USER>”
- `ConfigLocation`：“~/Library/Preferences”;“C：/Users/<USER>/AppData/Local<APPNAME>/”，“C：/ProgramData/<APPNAME>”
- `GenericConfigLocation`：“~/库/偏好设置”;“C：/用户/<USER>/AppData/本地”，“C：/程序数据”
- `DownloadLocation`：“~/下载”;“C：/用户/<USER>/下载”
- `GenericCacheLocation`：“~/Library/Caches”，“/Library/Caches”;“C：/Users/<USER>/AppData/Local/cache”
- `GenericStateLocation`：“~/Library/Preferences/State”;“C：/Users/<USER>/AppData/Local/State”，“C：/ProgramData/State”
- `AppDataLocation`：“~/库/应用支持/<APPNAME>”、“/库/应用支持/<APPNAME>”。<APPDIR>/../资源“;”C：/用户/<USER>/AppData/漫游<APPNAME>/“、”C：/ProgramData/<APPNAME>“、”“、”/<APPDIR><APPDIR>data“、”<APPDIR>/data/<APPNAME>”
- `AppConfigLocation`：“~/Library/Preferences/<APPNAME>”;C：/Users/<USER>/AppData/Local/<APPNAME>“，”C：/ProgramData/<APPNAME>”
- `PublicShareLocation`：“~/公共”;“C：/用户/公共”
- `TemplatesLocation`：“~/模板”;“C：/用户/<USER>/AppData/漫游/Microsoft/Windows/模板”
- `Path type`：Linux 及其他 UNIX 操作系统
- `DesktopLocation`：“~/桌面”
- `DocumentsLocation`：“~/文件”
- `FontsLocation`：“~/.fonts”，“~/.local/share/fonts”，“/usr/local/share/fonts”，“/usr/share/fonts”
- `ApplicationsLocation`：“~/.local/share/applications”，“/usr/local/share/applications”，“/usr/share/applications”
- `MusicLocation`：“~/音乐”
- `MoviesLocation`：“~/视频”
- `PicturesLocation`：“~/图片”
- `TempLocation`：“/tmp”
- `HomeLocation`：“~”
- `AppLocalDataLocation`：“~/.local/share/<APPNAME>”，“/usr/local/share<APPNAME>/”，“/usr/share/<APPNAME>”
- `CacheLocation`：“~/.cache<APPNAME>/”
- `StateLocation`：“~/.local/state<APPNAME>/”
- `GenericDataLocation`：“~/.local/share”、“/usr/local/share”、“/usr/share”
- `RuntimeLocation`：“/run/user<USER>/”
- `ConfigLocation`：“~/.config”、“/etc/xdg”
- `GenericConfigLocation`：“~/.config”， “/etc/xdg”
- `DownloadLocation`：“~/下载”
- `GenericCacheLocation`：“~/.cache”
- `GenericStateLocation`：“~/.local/state”
- `AppDataLocation`：“~/.local/share/<APPNAME>”，“/usr/local/share<APPNAME>/”，“/usr/share/<APPNAME>”
- `AppConfigLocation`：“~/.config/<APPNAME>”、“/etc/xdg/<APPNAME>”
- `PublicShareLocation`：“~/公共”
- `TemplatesLocation`：“~/模板”
- `Path type`：安卓;iOS
- `DesktopLocation`：“<APPROOT>/files”;“<APPROOT>/文档/桌面”
- `DocumentsLocation`：“<USER>/文档” [*]，“<USER>/<APPNAME>/文档”;“<APPROOT>/文档”
- `FontsLocation`：“/system/fonts”（不可写）;“<APPROOT>/library/fonts”
- `ApplicationsLocation`：不支持（目录不可读）;不支持
- `MusicLocation`：“<USER>/音乐” [*]， “<USER>/<APPNAME>/Music”;“<APPROOT>/文档/音乐”
- `MoviesLocation`：“<USER>/电影” [*]， “<USER>/<APPNAME>/电影”;“<APPROOT>/文档/电影”
- `PicturesLocation`：“<USER>/图片” [*]， “<USER>/<APPNAME>/图片”;“<APPROOT>/文档/图片”、“assets-library/”
- `TempLocation`：“<APPROOT>/cache”;“<APPROOT>/tmp”
- `HomeLocation`：“<APPROOT>/files”;系统定义
- `AppLocalDataLocation`：“<APPROOT>/files”、“<USER>/<APPNAME>/files”;“<APPROOT>/library/Application Support”
- `CacheLocation`：“<APPROOT>/cache”、“<USER>/<APPNAME>/cache”;“<APPROOT>/library/caches”
- `StateLocation`：“<APPROOT>/files/state”
- `GenericStateLocation (there is shared state)`：“<APPROOT>/files/state”
- `GenericDataLocation`：“<USER>” [*] 或 <USER>“/<APPNAME>/files”;<APPROOT>/库/应用支持
- `RuntimeLocation`：“<APPROOT>/cache”;不支持
- `ConfigLocation`：“<APPROOT>/files/settings”;“<APPROOT>/library/preferences”
- `GenericConfigLocation`：“<APPROOT>/files/settings”（没有共享设置）;“<APPROOT>/library/偏好设置”
- `DownloadLocation`：“<USER>/下载” [*]， “<USER>/<APPNAME>/下载”;“<APPROOT>/文档/下载”
- `GenericCacheLocation`：“<APPROOT>/cache”（没有共享缓存）;“<APPROOT>/Library/Caches”
- `AppDataLocation`：“<APPROOT>/files”、“<USER>/<APPNAME>/files”;“<APPROOT>/library/Application Support”
- `AppConfigLocation`：“<APPROOT>/files/settings”;“<APPROOT>/library/preferences<APPNAME>/”
- `PublicShareLocation`：不支持;不支持
- `TemplatesLocation`：不支持;不支持
在上表中，`<APPNAME>`通常是组织名称、应用程序名称，或两者兼有，或打包时生成的唯一名称。同样， <APPROOT> 是该应用程序安装的位置（通常是沙盒）。<APPDIR>是包含应用可执行文件的目录。
以上路径不应完全依赖，因为它们可能会根据操作系统配置、位置不同而变化，或者在未来的 Qt 版本中发生变化。
注意：在安卓上，外部存储（位置）上打开文件的应用程序<USER>如果卸载该存储会被终止。
注意：在Android 6.0（API 23）或更高版本上，使用`QStandardPaths::writableLocation`或`QStandardPaths::standardLocations`时必须在运行时请求“WRITE_EXTERNAL_STORAGE”权限。
注意：在Android上，读取/写入GenericDataLocation需要获得READ_EXTERNAL_STORAGE/WRITE_EXTERNAL_STORAGE权限。
注意：[*] 在 Android 11 及以上版本中，公共目录不再直接用于有范围存储模式。因此，形式为 `"<USER>/DirName"` 的路径不会返回。相反，您可以使用使用 Storage Access Framework（SAF）的 `QFileDialog` 来访问此类目录。
注意：在 iOS 上，如果你将 `QStandardPaths::standardLocations(QStandardPaths::PicturesLocation).last()` 作为参数传递给 `QFileDialog::setDirectory()`，将使用原生图片选择器对话框来访问用户相册。返回的文件名可以通过 `QFile` 及相关 API 加载。此功能于 Qt 5.5 中加入。

### `[static] QString QStandardPaths::displayName(QStandardPaths::StandardLocation type)`

**作用与语义：**

返回给定位置的本地显示名称`type`若找不到相关位置则返回空`QString`。

### `[static] QString QStandardPaths::findExecutable(const QString &executableName, const QStringList &paths = QStringList())`

**作用与语义：**

在指定`paths`中找到名为`executableName`的可执行文件，或者如果`paths`空，则找到系统路径。
在大多数操作系统中，系统路径由`PATH`环境变量决定。搜索可执行文件的目录可以在路径参数中设置。要同时搜索自己的路径和系统路径，调用两次findExecutable，一次路径设置，一次路径为空。为了保留行为依赖于调用名称的可执行文件的行为，不解析符号链接。
注意：在 Windows 上，通常的可执行扩展（来自 PATHEXT 环境变量）会自动附加。例如，findExecutable（“foo”）调用会查找 `foo.exe` 或 `foo.bat`（如果存在）。
返回可执行文件的绝对路径，或如果找不到则返回空字符串。
如果给定`executableName`是指向可执行文件的绝对路径，则返回其干净路径。

### `[static] QString QStandardPaths::locate(QStandardPaths::StandardLocation type, const QString &fileName, QStandardPaths::LocateOptions options = LocateFile)`

**作用与语义：**

在标准位置找到名为`fileName`的文件或目录，`type`。
`options`标志可以指定是查找文件还是目录。默认情况下，该标志设置为`LocateFile`。
返回第一个找到的文件或目录的绝对路径，否则返回空字符串。

### `[static] QStringList QStandardPaths::locateAll(QStandardPaths::StandardLocation type, const QString &fileName, QStandardPaths::LocateOptions options = LocateFile)`

**作用与语义：**

在`type`的标准位置中，查找所有以`fileName`为名的文件或目录。
`options`标志允许你指定是查找文件还是目录。默认情况下，该标志设置为`LocateFile`。
返回所有找到的文件列表。

### `[static] void QStandardPaths::setTestModeEnabled(bool testMode)`

**作用与语义：**

如果`testMode` `true`，这会启用`QStandardPaths`中的特殊“测试模式”，将可写位置切换到测试目录。这防止自动测试读取或写入当前用户的配置。
它影响测试程序可能写入文件的位置：`GenericDataLocation`、`AppDataLocation`、`ConfigLocation`、`GenericConfigLocation`、`AppConfigLocation`、`StateLocation`、`GenericStateLocation`、`GenericCacheLocation`和`CacheLocation`。其他地点不受影响。
在Unix上，`XDG_DATA_HOME`设置为`~/.qttest/share`，`XDG_CONFIG_HOME`设为`~/.qttest/config`，`XDG_STATE_HOME`设为`~/.qttest/state`，`XDG_CACHE_HOME`设为`~/.qttest/cache`。
在macOS上，数据会送到`~/.qttest/Application Support`，缓存会送到`~/.qttest/Cache`，配置会送到`~/.qttest/Preferences`。
在Windows上，所有内容都放在`%APPDATA%`下的“qttest”目录。

### `[static] QStringList QStandardPaths::standardLocations(QStandardPaths::StandardLocation type)`

**作用与语义：**

返回所有存放`type`文件的目录。
目录列表按高优先级到低优先级排序，如果能确定，从`writableLocation()`开始。如果没有定义类型位置，该列表为空。

### `[static] QString QStandardPaths::writableLocation(QStandardPaths::StandardLocation type)`

**作用与语义：**

返回应写入`type`文件的目录，若无法确定位置则返回空字符串。
注意：返回的存储位置可能不存在;也就是说，可能需要由系统或用户创建。

### `enum LocateOption { LocateFile, LocateDirectory }`

**作用与语义：**

本枚举描述了可用于控制`QStandardPaths::locate`和 `QStandardPaths::locateAll`行为的不同标志。
- `QStandardPaths::LocateFile`：`0x0`;仅返回文件
- `QStandardPaths::LocateDirectory`：`0x1`;仅返回目录
LocateOptions 类型是 QFlags 的 typedef<LocateOption>。它存储 LocateOption 值的 OR 组合。

### `flags LocateOptions`

**作用与语义：**

本枚举描述了可用于控制`QStandardPaths::locate`和 `QStandardPaths::locateAll`行为的不同标志。
- `QStandardPaths::LocateFile`：`0x0`;仅返回文件
- `QStandardPaths::LocateDirectory`：`0x1`;仅返回目录
LocateOptions 类型是 QFlags 的 typedef<LocateOption>。它存储 LocateOption 值的 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先设置路径或设备，再 open，成功后读写/定位/刷新，最后 close；析构通常会关闭设备，但关键写入应显式 flush/close 并检查错误。相对路径依赖当前工作目录，资源路径和用户文件路径要区分。

### 状态和错误边界

区分设备未打开、打开成功、到达 EOF、暂时无数据、读写失败和写入尚未落盘。`readAll()` 方便小数据但可能占用大量内存，大文件应分块处理并检查返回值。

### 线程边界

同一个打开设备不要跨线程并发使用，除非类明确保证线程安全；后台 I/O 通过 worker 或异步设备处理，GUI 线程只接收结果。

### 最容易出现的错误

不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QStandardPaths` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
