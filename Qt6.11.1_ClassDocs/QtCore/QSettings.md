# QSettings

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QSettings` 提供跨平台的应用配置和用户设置持久化，支持键值、分组、数组以及系统/用户范围。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSettings` 提供跨平台的应用配置和用户设置持久化，支持键值、分组、数组以及系统/用户范围。

**内部模型：** QSettings 是配置访问接口，不是数据库。键名是公共契约，格式和 scope 决定数据落在哪里；写入后通常由 Qt 负责同步，但关键时刻可以 sync 并检查 status。

**适用场景：** 保存窗口大小、最近文件、用户偏好、简单功能开关和轻量配置时使用；复杂数据、并发写入或需要查询的内容应使用数据库或专门格式。

**典型调用链：** 构造 settings -> beginGroup -> value/default -> setValue -> endGroup -> sync/读取 status。

**先记住的坑：** 键名和类型要稳定；value 返回 QVariant 要提供默认值；不要把密码等敏感信息明文写入；多进程同时写入需额外设计。

## 2. 依赖与对象关系

- 头文件：`#include <QSettings>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

QSettings 是配置访问接口，不是数据库。键名是公共契约，格式和 scope 决定数据落在哪里；写入后通常由 Qt 负责同步，但关键时刻可以 sync 并检查 status。

### 状态、生命周期和线程

**生命周期：** 容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

**状态与结果：** 要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

**线程与事件循环：** 不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

## 3. 直接使用

保存窗口大小、最近文件、用户偏好、简单功能开关和轻量配置时使用；复杂数据、并发写入或需要查询的内容应使用数据库或专门格式。 使用时通常按这个过程组织：构造 settings -> beginGroup -> value/default -> setValue -> endGroup -> sync/读取 status。

```cpp
QSettings settings;
settings.setValue(QStringLiteral("MainWindow/geometry"), saveGeometry());
restoreGeometry(settings.value(QStringLiteral("MainWindow/geometry")).toByteArray());
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Format { NativeFormat, Registry32Format, Registry64Format, IniFormat, WebLocalStorageFormat, …, InvalidFormat }`
- `ReadFunc`
- `enum Scope { UserScope, SystemScope }`
- `SettingsMap`
- `enum Status { NoError, AccessError, FormatError }`
- `WriteFunc`

### 公有函数

- `QSettings(QObject *parent = nullptr)`
- `QSettings(QSettings::Scope scope, QObject *parent = nullptr)`
- `QSettings(const QString &fileName, QSettings::Format format, QObject *parent = nullptr)`
- `QSettings(const QString &organization, const QString &application = QString(), QObject *parent = nullptr)`
- `QSettings(QSettings::Scope scope, const QString &organization, const QString &application = QString(), QObject *parent = nullptr)`
- `QSettings(QSettings::Format format, QSettings::Scope scope, const QString &organization, const QString &application = QString(), QObject *parent = nullptr)`
- `virtual ~QSettings()`
- `QStringList allKeys() const`
- `QString applicationName() const`
- `void beginGroup(QAnyStringView prefix)`
- `int beginReadArray(QAnyStringView prefix)`
- `void beginWriteArray(QAnyStringView prefix, int size = -1)`
- `QStringList childGroups() const`
- `QStringList childKeys() const`
- `void clear()`
- `bool contains(QAnyStringView key) const`
- `void endArray()`
- `void endGroup()`
- `bool fallbacksEnabled() const`
- `QString fileName() const`
- `QSettings::Format format() const`
- `QString group() const`
- `bool isAtomicSyncRequired() const`
- `bool isWritable() const`
- `QString organizationName() const`
- `void remove(QAnyStringView key)`
- `QSettings::Scope scope() const`
- `void setArrayIndex(int i)`
- `void setAtomicSyncRequired(bool enable)`
- `void setFallbacksEnabled(bool b)`
- `void setValue(QAnyStringView key, const QVariant &value)`
- `QSettings::Status status() const`
- `void sync()`
- `QVariant value(QAnyStringView key) const`
- `QVariant value(QAnyStringView key, const QVariant &defaultValue) const`

### 静态公有成员

- `QSettings::Format defaultFormat()`
- `QSettings::Format registerFormat(const QString &extension, QSettings::ReadFunc readFunc, QSettings::WriteFunc writeFunc, Qt::CaseSensitivity caseSensitivity = Qt::CaseSensitive)`
- `void setDefaultFormat(QSettings::Format format)`
- `void setPath(QSettings::Format format, QSettings::Scope scope, const QString &path)`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSettings::Format`

**作用与语义：**

该枚举类型指定`QSettings`使用的存储格式。
- `QSettings::NativeFormat`：`0`;使用最适合平台的存储格式存储设置。在 Windows 上，这意味着系统注册表;在 macOS 和 iOS 上，这意味着 CFPreferences API;在 Unix 上，这意味着 INI 格式的文本配置文件。
- `QSettings::Registry32Format`：`2`;仅限Windows：从运行在64位Windows上的64位应用程序中显式访问32位系统注册表。在32位Windows或64位Windows上的32位应用程序中，这与指定NativeFormat相同。该枚举值在Qt 5.7中加入。
- `QSettings::Registry64Format`：`3`;仅限Windows：从运行在64位Windows上的32位应用程序中显式访问64位系统注册表。在32位Windows或64位Windows上的64位应用程序中，这与指定NativeFormat相同。该枚举值是在Qt 5.7中添加的。
- `QSettings::IniFormat`：`1`;将设置存储在INI文件中。注意，INI文件失去了数字数据与用于编码的字符串之间的区别，因此以数字形式写入的数值应被读回为`QString`。
- `QSettings::WebLocalStorageFormat`：`4`;仅WASM：将当前源区的设置存储在window.localStorage中。如果不允许使用Cookie，则退回到INI格式。这为每个源区提供最多5MiB的存储空间，但访问是同步的，且不需要JSPI。
- `QSettings::WebIndexedDBFormat`：`5`;仅WASM：将当前来源的设置存储在索引数据库中。如果不允许使用cookie，则退回到INI格式。这需要JSPI，但比WebLocalStorageFormat提供更多存储空间。
- `QSettings::InvalidFormat`：`16`;特殊值由`registerFormat()`返回。
在Unix上，NativeFormat和IniFormat含义相同，只是文件扩展名不同（`.conf`代表NativeFormat，`.ini`代表IniFormat）。
INI 文件格式是 Qt 在所有平台上支持的 Windows 文件格式。在缺乏 INI 标准的情况下，我们尽量遵循 Microsoft 的做法，但有以下例外：
- 如果你存储了`QVariant`无法转换为`QString`的类型（例如 `QPoint`、`QRect` 和 `QSize`），Qt 使用基于`@`的语法来编码该类型。例如：
pos = @`QPoint`（100 100）。

为了减少兼容性问题，任何不出现在值首位或没有Qt类型（`Point`、`Rect`、`Size`等）的`@`都被视为正常字符。
- 虽然反斜杠是 INI 文件中的特殊字符，但大多数 Windows 应用程序在文件路径中不会逃逸反斜线（`\`）：
windir = C：\Windows。

`QSettings`始终将反斜线视为特殊字符，且不提供读写此类条目的API。
- INI 文件格式对键的语法有严格限制。Qt 通过在键中使用 `%` 作为转义字符来绕过这些限制。此外，如果你保存顶级设置（如无斜杠的键，如“someKey”），它会出现在 INI 文件的“General”部分。为避免覆盖其他键，如果你用“General/someKey”等键保存内容，键将位于“%General”部分，而非“General”部分。
- 与当今大多数实现一致，`QSettings` 将假定 INI 文件中的值是 UTF-8 编码的。这意味着这些值将被解码为 UTF-8 编码项并以 UTF-8 写回。为了与旧版本 Qt 向后兼容，INI 文件中的键以 %-编码格式写入，但可以以 %-编码和 UTF-8 格式读取。
请注意，这种行为与 Qt 6 之前版本中的 `QSettings` 行为不同。用 Qt 5 或更早版本写的 INI 文件仍可被基于 Qt 6 的应用程序完全读取（除非设置了非 utf8 的 ini 编码）。但是，用 Qt 6 写的 INI 文件只能被旧版本 Qt 读取，如果你将“iniCodec”设置为 UTF-8 文本编码。

### `QSettings::ReadFunc`

**作用与语义：**

Typedef 指针指向具有以下签名的函数：
`ReadFunc` 在 `registerFormat()` 中用作指向读取一组键值对的函数的指针。`ReadFunc`应一次性读取所有选项，并返回 `SettingsMap` 容器中的所有设置，该容器最初是空的。

**官方示例：**

```cpp
 bool myReadFunc(QIODevice &device, QSettings::SettingsMap &map);
```

### `enum QSettings::Scope`

**作用与语义：**

该枚举指定设置是用户专属还是同一系统的所有用户共享。
- `QSettings::UserScope`：`0`;将设置存储在当前用户的特定位置（例如用户的主目录中）。
- `QSettings::SystemScope`：`1`;将设置存储在全局位置，使同一台机器上的所有用户都能访问同一套设置。

### `QSettings::SettingsMap`

**作用与语义：**

Typedef 用于`QMap`<`QString`，`QVariant`>。

### `enum QSettings::Status`

**作用与语义：**

以下状态值可能存在：
- `QSettings::NoError`：`0`;未发生错误。
- `QSettings::AccessError`：`1`;发生访问错误（例如尝试写入只读文件）。
- `QSettings::FormatError`：`2`;发生格式错误（例如加载一个格式错误的 INI 文件）。

### `QSettings::WriteFunc`

**作用与语义：**

Typedef 指针指向具有以下签名的函数：
`WriteFunc` 在 `registerFormat()` 中用作指向函数的指针，该函数写入一组键值对。`WriteFunc` 只调用一次，所以你需要一次性输出所有设置。

**官方示例：**

```cpp
 bool myWriteFunc(QIODevice &device, const QSettings::SettingsMap &map);
```

### `[explicit] QSettings::QSettings(QObject *parent = nullptr)`

**作用与语义：**

构建一个QSettings对象，用于访问之前通过调用`QCoreApplication::setOrganizationName()`、`QCoreApplication::setOrganizationDomain()`和`QCoreApplication::setApplicationName()`的应用程序和组织集的设置。
作用域`QSettings::UserScope`，格式为`defaultFormat()`（默认为`QSettings::NativeFormat`）。在调用该构造函数之前，请使用`setDefaultFormat()`来更改该构造函数所使用的默认格式。
代码。
等价于。
如果之前没有调用`QCoreApplication::setOrganizationName()`和`QCoreApplication::setApplicationName()`，QSettings对象将无法读取或写入任何设置，`status()`返回`AccessError`。
你应该同时提供域名（macOS和iOS默认使用）和名称（其他地方默认使用），不过代码如果只提供一个域名，且该域名会被使用（所有平台），这与非默认平台文件命名的做法不一致。

**官方示例：**

```cpp
 QSettings settings("Moose Soft", "Facturo-Pro");
```

### `[explicit] QSettings::QSettings(QSettings::Scope scope, QObject *parent = nullptr)`

**作用与语义：**

构造QSettings对象的方式与QSettings（`QObject` *parent）相同，但采用给定的`scope`。

### `QSettings::QSettings(const QString &fileName, QSettings::Format format, QObject *parent = nullptr)`

**作用与语义：**

构造一个名为 `fileName` 的 QSettings 对象，用于访问文件中存储的设置，并带有父`parent`。如果该文件尚未存在，则会被创建。
如果 `format` 是`QSettings::NativeFormat`，`fileName` 的含义取决于平台。在 Unix 上，`fileName` 是 INI 文件的名称。在 macOS 和 iOS 上，`fileName` 是`.plist`文件的名称。在 Windows 上，`fileName` 是系统注册表中的一条路径。
如果`format` `QSettings::IniFormat`，`fileName` 是 INI 文件的名称。
警告：此功能仅为方便而提供。它在访问由 Qt 生成的 INI 或 `.plist` 文件时表现良好，但在其他程序发起的某些文件中出现的语法上可能会失败。特别请注意以下限制：
- QSettings 不提供读取 INI “路径”条目的方法，即带有未脱义斜杠字符的条目。（这是因为这些条目具有歧义，无法自动解析。）
- 在INI文件中，QSettings在某些上下文中将`@`字符作为元字符来编码Qt特定的数据类型（例如，`@Rect`），因此在纯INI文件中出现时可能会误解。

### `[explicit] QSettings::QSettings(const QString &organization, const QString &application = QString(), QObject *parent = nullptr)`

**作用与语义：**

构建一个QSettings对象，用于访问名为`application`的应用程序设置，来自名为`organization`的组织，并带有父`parent`。
作用域设置为`QSettings::UserScope`，格式设置为`QSettings::NativeFormat`（即在调用该构造函数之前调用`setDefaultFormat()`无效）。

**官方示例：**

```cpp
 QSettings settings("Moose Tech", "Facturo-Pro");
```

### `QSettings::QSettings(QSettings::Scope scope, const QString &organization, const QString &application = QString(), QObject *parent = nullptr)`

**作用与语义：**

构建一个QSettings对象，用于访问名为`application`的应用程序设置，来自名为`organization`的组织，并带有父`parent`。
如果`scope` `QSettings::UserScope`，QSettings 对象会先搜索用户特定的设置，然后再作为备选搜索系统范围的设置。如果`scope` `QSettings::SystemScope`，QSettings 对象会忽略用户特定的设置，提供系统范围的设置访问。
存储格式设置为`QSettings::NativeFormat`（即在调用该构造函数之前调用`setDefaultFormat()`无效）。
如果没有应用程序名称，QSettings 对象只访问全组织范围的 `locations`。

### `QSettings::QSettings(QSettings::Format format, QSettings::Scope scope, const QString &organization, const QString &application = QString(), QObject *parent = nullptr)`

**作用与语义：**

构建一个QSettings对象，用于访问名为`application`的应用程序设置，来自名为`organization`的组织，并带有父`parent`。
如果`scope` `QSettings::UserScope`，QSettings 对象会先搜索用户特定的设置，然后再搜索系统范围的设置作为备选。如果`scope` `QSettings::SystemScope`，QSettings 对象会忽略用户特定的设置，提供系统范围的设置访问。
如果`format` `QSettings::NativeFormat`，则使用原生API存储设置。如果`format`为`QSettings::IniFormat`，则使用INI格式。
如果没有应用程序名称，QSettings 对象只能访问整个组织的 `locations`。

### `[virtual noexcept] QSettings::~QSettings()`

**作用与语义：**

摧毁`QSettings`物体。
任何未保存的更改最终都会写入永久存储。

### `QStringList QSettings::allKeys() const`

**作用与语义：**

返回所有键的列表，包括子键，这些键可以用`QSettings`对象读取。
如果用`beginGroup()`设置一个组，则只返回组中的键，且不带组前缀：

**官方示例：**

```cpp
 QSettings settings;
 settings.setValue("fridge/color", QColor(Qt::white));
 settings.setValue("fridge/size", QSize(32, 96));
 settings.setValue("sofa", true);
 settings.setValue("tv", false);

 QStringList keys = settings.allKeys();
 // keys: ["fridge/color", "fridge/size", "sofa", "tv"]
```

### `QString QSettings::applicationName() const`

**作用与语义：**

返回用于存储设置的应用程序名称。

### `void QSettings::beginGroup(QAnyStringView prefix)`

**作用与语义：**

附加`prefix`当前组。
当前组会自动加在所有指定为`QSettings`的键前。此外，查询函数如`childGroups()`、`childKeys()`和`allKeys()`基于该组。默认情况下，不会设置组。
组有助于避免反复输入相同的设置路径。例如：
这将设定三个设置的数值：
- `mainwindow/size`
- `mainwindow/active`
- `outputpanel/visible`
调用 `endGroup()` 将当前组重置到对应的 beginGroup() 调用之前的状态。组可以嵌套。
注意：在6.4之前的Qt版本中，该功能是取`QString`，而非取`QAnyStringView`。

**官方示例：**

```cpp
 settings.beginGroup("mainwindow");
 settings.setValue("size", win->size());
 settings.setValue("active", win->isActive());
 settings.endGroup();

 settings.beginGroup("outputpanel");
 settings.setValue("visible", panel->isVisible());
 settings.endGroup();
```

### `int QSettings::beginReadArray(QAnyStringView prefix)`

**作用与语义：**

向当前组添加`prefix`，并开始从数组读取数据。返回数组大小。
首先用`beginWriteArray()`来写入数组。
注意：在6.4之前的Qt版本中，该功能采用`QString`，而非取`QAnyStringView`。

**官方示例：**

```cpp
 struct Login {
     QString userName;
     QString password;
 };
 QList<Login> logins;
 //...
 void some_function()
 {
     //...
     QSettings settings;
     int size = settings.beginReadArray("logins");
     for (int i = 0; i < size; ++i) {
         settings.setArrayIndex(i);
         Login login;
         login.userName = settings.value("userName").toString();
         login.password = settings.value("password").toString();
         logins.append(login);
     }
     settings.endArray();
     //...
 }
```

### `void QSettings::beginWriteArray(QAnyStringView prefix, int size = -1)`

**作用与语义：**

向当前组添加`prefix`，并开始写入大小为`size`的数组。如果`size`为-1（默认值），则根据写入的条目索引自动确定。
如果你某一组密钥多次出现，可以使用数组来简化操作。例如，假设你想保存一个可变长度的用户名和密码列表。你可以写成：
生成的密钥将具有以下形式。
- `logins/size`
- `logins/1/userName`
- `logins/1/password`
- `logins/2/userName`
- `logins/2/password`
- `logins/3/userName`
- `logins/3/password`
- ...
要读取数组，使用`beginReadArray()`。
注意：在6.4之前的Qt版本中，该功能采用`QString`，而非取`QAnyStringView`。

**官方示例：**

```cpp
 struct Login {
     QString userName;
     QString password;
 };
 QList<Login> logins;
 //...
 void some_function()
 {
     //...
     QSettings settings;
     settings.beginWriteArray("logins");
     for (qsizetype i = 0; i < logins.size(); ++i) {
         settings.setArrayIndex(i);
         settings.setValue("userName", logins.at(i).userName);
         settings.setValue("password", logins.at(i).password);
     }
     settings.endArray();
     //...
 }
```

### `QStringList QSettings::childGroups() const`

**作用与语义：**

返回所有包含可用`QSettings`对象读取的键的顶层密钥组列表。
如果用`beginGroup()`设置一个组，则返回该组的第一层键，且不带组前缀。
你可以用 `childKeys()` 和 childGroups() 递归地浏览整个设置层级。

**官方示例：**

```cpp
 QSettings settings;
 settings.setValue("fridge/color", QColor(Qt::white));
 settings.setValue("fridge/size", QSize(32, 96));
 settings.setValue("sofa", true);
 settings.setValue("tv", false);

 QStringList groups = settings.childGroups();
 // groups: ["fridge"]
```

### `QStringList QSettings::childKeys() const`

**作用与语义：**

返回所有可用`QSettings`对象读取的顶层密钥列表。
如果用`beginGroup()`设置一个组，则返回该组的顶层键，但不会带组前缀：
你可以用 childKeys() 和递归方式`childGroups()`整个设置层级。

**官方示例：**

```cpp
 QSettings settings;
 settings.setValue("fridge/color", QColor(Qt::white));
 settings.setValue("fridge/size", QSize(32, 96));
 settings.setValue("sofa", true);
 settings.setValue("tv", false);

 QStringList keys = settings.childKeys();
 // keys: ["sofa", "tv"]
```

### `void QSettings::clear()`

**作用与语义：**

移除与该`QSettings`对象关联的主位置中的所有条目。
备选位置的条目不会被删除。
如果你只想删除当前`group()`中的条目，可以用 remove（“”） 代替。

### `bool QSettings::contains(QAnyStringView key) const`

**作用与语义：**

如果存在名为 `key` 的设置，则返回 `true`;否则返回 false。
如果用`beginGroup()`来设置一个群，则取`key`相对于该群。
密钥查找会根据文件格式和操作系统的不同，对大小写敏感或不敏感。为避免可移植性问题，请参见章节和密钥语法规则。
注意：在6.4之前的Qt版本中，该功能采用`QString`，而非取`QAnyStringView`。

### `[static] QSettings::Format QSettings::defaultFormat()`

**作用与语义：**

返回用于存储 `QSettings`（`QObject` *） 构造函数设置的默认文件格式。如果未设置默认格式，则使用 `QSettings::NativeFormat`。

### `void QSettings::endArray()`

**作用与语义：**

关闭用`beginReadArray()`或`beginWriteArray()`开始的数组。

### `void QSettings::endGroup()`

**作用与语义：**

将组重置到相应`beginGroup()`调用前的状态。

**官方示例：**

```cpp
 settings.beginGroup("alpha");
 // settings.group() == "alpha"

 settings.beginGroup("beta");
 // settings.group() == "alpha/beta"

 settings.endGroup();
 // settings.group() == "alpha"

 settings.endGroup();
 // settings.group() == ""
```

### `[override virtual protected] bool QSettings::event(QEvent *event)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。
该虚拟函数接收对象事件，如果事件`e`被识别并处理，应返回真。
event() 函数可以重新实现，以自定义对象的行为。
确保你调用所有未处理的事件的父事件类实现。

### `bool QSettings::fallbacksEnabled() const`

**作用与语义：**

如果启用了备援，返回`true`;否则返回`false`。
默认情况下，备援是启用的。

### `QString QSettings::fileName() const`

**作用与语义：**

返回使用该`QSettings`对象编写设置的路径。
在 Windows 上，如果格式是`QSettings::NativeFormat`，返回值是系统注册表路径，而不是文件路径。

### `QSettings::Format QSettings::format() const`

**作用与语义：**

返回存储设置的格式。

### `QString QSettings::group() const`

**作用与语义：**

返回当前的组别。

### `bool QSettings::isAtomicSyncRequired() const`

**作用与语义：**

如果`QSettings`仅允许执行设置的原子保存和重载（同步），则返回`true`。如果允许将设置内容直接保存到配置文件中，则返回`false`。默认值为`true`。

### `bool QSettings::isWritable() const`

**作用与语义：**

如果可以使用该`QSettings`对象编写设置，返回`true`;否则返回`false`。
isWritable() 可能返回 false 的一个原因是 `QSettings` 操作只读文件。
警告：该功能并非完全可靠，因为文件权限可能随时发生变化。

### `QString QSettings::organizationName() const`

**作用与语义：**

返回用于存储设置的组织名称。

### `[static] QSettings::Format QSettings::registerFormat(const QString &extension, QSettings::ReadFunc readFunc, QSettings::WriteFunc writeFunc, Qt::CaseSensitivity caseSensitivity = Qt::CaseSensitive)`

**作用与语义：**

注册自定义存储格式。成功时，返回一个特殊的格式值，随后可传递给`QSettings`构造器。失败时，返回`InvalidFormat`。
`extension`是与格式相关的文件扩展名（不含“.”）。
`readFunc`和`writeFunc`参数是读取和写入一组键值对的函数的指针。读写函数的`QIODevice`参数总是以二进制模式打开（即不带`QIODeviceBase::Text`标志）。
`caseSensitivity`参数指定键是否区分大小写。这在使用`QSettings`查找值时会产生影响。默认是区分大小写。在Unix系统上，参数必须`Qt::CaseSensitive`。
默认情况下，如果你使用以组织名称和应用程序名称为单位的构造函数，文件系统位置与`IniFormat`相同。使用`setPath()`来指定其他位置。
注意：该功能是线程安全的。

**官方示例：**

```cpp
 bool readXmlFile(QIODevice &device, QSettings::SettingsMap &map);
 bool writeXmlFile(QIODevice &device, const QSettings::SettingsMap &map);

 int main(int argc, char *argv[])
 {
     const QSettings::Format XmlFormat =
             QSettings::registerFormat("xml", readXmlFile, writeXmlFile);

     QSettings settings(XmlFormat, QSettings::UserScope, "MySoft",
                        "Star Runner");

     //...
 }
```

### `void QSettings::remove(QAnyStringView key)`

**作用与语义：**

移除设置`key`及`key`的任何子设置。
请注意，如果某个备用位置包含相同键的设置，调用 remove() 后该设置将被可见。
如果 `key` 是空字符串，当前 `group()` 中的所有键都会被移除。例如：
密钥查找会根据文件格式和操作系统的不同，对大小写敏感或不敏感。为避免可移植性问题，请参见章节和密钥语法规则。
注意：在6.4之前的Qt版本中，该功能采用`QString`，而非取`QAnyStringView`。

**官方示例：**

```cpp
 QSettings settings;
 settings.setValue("ape", 0);
 settings.setValue("monkey", 1);
 settings.setValue("monkey/sea", 2);
 settings.setValue("monkey/doe", 4);

 settings.remove("monkey");
 QStringList keys = settings.allKeys();
 // keys: ["ape"]
```

### `QSettings::Scope QSettings::scope() const`

**作用与语义：**

返回用于存储设置的示波器。

### `void QSettings::setArrayIndex(int i)`

**作用与语义：**

将当前数组索引设置为`i`。调用 `setValue()`、`value()`、`remove()` 和 `contains()` 等函数时，将对该索引的数组条目进行操作。
您必须先调用`beginReadArray()`或`beginWriteArray()`才能调用此功能。

### `void QSettings::setAtomicSyncRequired(bool enable)`

**作用与语义：**

配置是否需要`QSettings`来执行设置的原子保存和重新加载（同步）。如果`enable`参数为`true`（默认），`sync()`只执行原子同步操作。如果无法实现，`sync()`将失败，`status()`将成为错误状态。
将该属性设置为`false`，`QSettings`可以直接写入配置文件，并忽略试图与其他进程同时写入时锁定配置文件的错误。由于可能存在损坏风险，该选项应谨慎使用，但在某些情况下是必需的，比如存在于不可写目录中的`QSettings::IniFormat`配置文件或NTFS备用数据流。
有关该功能的更多信息，请参见`QSaveFile`。

### `[static] void QSettings::setDefaultFormat(QSettings::Format format)`

**作用与语义：**

将默认文件格式设置为给定的`format`，用于存储 `QSettings`（`QObject` *） 构造函数的设置。
如果没有设置默认格式，则使用 `QSettings::NativeFormat`。请参阅你所使用的`QSettings`构造函数的文档，看看该构造函数是否会忽略该函数。

### `void QSettings::setFallbacksEnabled(bool b)`

**作用与语义：**

设置是否启用了`b`的备选。
默认情况下，备援是启用的。

### `[static] void QSettings::setPath(QSettings::Format format, QSettings::Scope scope, const QString &path)`

**作用与语义：**

将存储给定`format`和`scope`设置的路径设置为`path`。`format`可以是自定义格式。
下表总结了默认值：
- `Platform`：格式;范围;路径
- `Windows`：`IniFormat`;`UserScope`;`FOLDERID_RoamingAppData`
- `SystemScope`：`FOLDERID_ProgramData`
- `Unix`：`NativeFormat`，`IniFormat`;`UserScope`;`$HOME/.config`
- `SystemScope`：`/etc/xdg`
- `macOS and iOS`：`IniFormat`;`UserScope`;`$HOME/.config`
- `SystemScope`：`/etc/xdg`
Unix、macOS 和 iOS 上的默认 `UserScope` 路径（`$HOME/.config` 或 $HOME/设置）可以通过设置 `XDG_CONFIG_HOME` 环境变量被用户覆盖。Unix、macOS 和 iOS（`/etc/xdg`）上的默认 `SystemScope` 路径可以在使用 `configure` 脚本的 `-sysconfdir` 标志构建 Qt 库时被覆盖（详见 `QLibraryInfo` 部分）。
在Windows、macOS和iOS上设置`NativeFormat`路径都没有影响。
警告：此函数不影响现有的`QSettings`对象。

### `void QSettings::setValue(QAnyStringView key, const QVariant &value)`

**作用与语义：**

将 `key` 设为 `value` 的值。如果`key`已经存在，则覆盖之前的值。
密钥查找会根据文件格式和操作系统的不同，对大小写敏感或不敏感。为避免可移植性问题，请参见章节和密钥语法规则。
注意：在6.4之前的Qt版本中，该功能采用了`QString`，而非 `QAnyStringView`。

**官方示例：**

```cpp
 QSettings settings;
 settings.setValue("interval", 30);
 settings.value("interval").toInt();     // returns 30

 settings.setValue("interval", 6.55);
 settings.value("interval").toDouble();  // returns 6.55
```

### `QSettings::Status QSettings::status() const`

**作用与语义：**

返回状态码，表示`QSettings`遇到的第一个错误，若未发生错误则返回`QSettings::NoError`。
请注意，`QSettings`会延迟执行某些操作。因此，你可能需要先调用`sync()`，确保存储在`QSettings`中的数据已经写入磁盘，再调用状态()。

### `void QSettings::sync()`

**作用与语义：**

将未保存的更改写入永久存储，并重新加载其他应用程序在此期间更改的设置。
这个函数会从`QSettings`的解构器和事件循环定期调用，所以通常你不需要自己调用它。

### `QVariant QSettings::value(QAnyStringView key, const QVariant &defaultValue) const`

**作用与语义：**

返回设置`key`的值。如果设置不存在，返回`defaultValue`。
如果没有指定默认值，则返回一个默认的`QVariant`。
密钥查找会根据文件格式和操作系统的不同，对大小写敏感或不敏感。为避免可移植性问题，请参见章节和密钥语法规则。
注意：在 6.4 之前的 Qt 版本中，该功能采用了 `QString` 的频率，而非 `QAnyStringView`。

**官方示例：**

```cpp
 QSettings settings;
 settings.setValue("animal/snake", 58);
 settings.value("animal/snake", 1024).toInt();   // returns 58
 settings.value("animal/zebra", 1024).toInt();   // returns 1024
 settings.value("animal/zebra").toInt();         // returns 0
```

### `ReadFunc`

**作用与语义：**

Typedef 指针指向具有以下签名的函数：
`ReadFunc` 在 `registerFormat()` 中用作指向读取一组键值对的函数的指针。`ReadFunc`应一次性读取所有选项，并返回 `SettingsMap` 容器中的所有设置，该容器最初是空的。

**官方示例：**

```cpp
 bool myReadFunc(QIODevice &device, QSettings::SettingsMap &map);
```

### `SettingsMap`

**作用与语义：**

Typedef 用于`QMap`<`QString`，`QVariant`>。

### `WriteFunc`

**作用与语义：**

Typedef 指针指向具有以下签名的函数：
`WriteFunc` 在 `registerFormat()` 中用作指向函数的指针，该函数写入一组键值对。`WriteFunc` 只调用一次，所以你需要一次性输出所有设置。

**官方示例：**

```cpp
 bool myWriteFunc(QIODevice &device, const QSettings::SettingsMap &map);
```

### `QVariant value(QAnyStringView key) const`

**作用与语义：**

返回设置`key`的值。如果设置不存在，返回`defaultValue`。
如果没有指定默认值，则返回一个默认的`QVariant`。
密钥查找会根据文件格式和操作系统的不同，对大小写敏感或不敏感。为避免可移植性问题，请参见章节和密钥语法规则。
注意：在 6.4 之前的 Qt 版本中，该功能采用了 `QString` 的频率，而非 `QAnyStringView`。

**官方示例：**

```cpp
 QSettings settings;
 settings.setValue("animal/snake", 58);
 settings.value("animal/snake", 1024).toInt();   // returns 58
 settings.value("animal/zebra", 1024).toInt();   // returns 1024
 settings.value("animal/zebra").toInt();         // returns 0
```

## 6. 深入实践与常见坑

### 生命周期和资源边界

容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

### 状态和错误边界

要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

### 线程边界

不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

### 最容易出现的错误

键名和类型要稳定；value 返回 QVariant 要提供默认值；不要把密码等敏感信息明文写入；多进程同时写入需额外设计。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSettings` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
