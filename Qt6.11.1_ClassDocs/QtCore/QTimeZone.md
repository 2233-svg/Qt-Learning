# QTimeZone

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“TimeZone”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QTimeZone` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QTimeZone>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `struct OffsetData`
- `(since 6.5) enum Initialization { LocalTime, UTC }`
- `enum NameType { DefaultName, LongName, ShortName, OffsetName }`
- `OffsetDataList`
- `enum TimeType { StandardTime, DaylightTime, GenericTime }`

### 公有函数

- `QTimeZone()`
- `(since 6.5) QTimeZone(QTimeZone::Initialization spec)`
- `QTimeZone(const QByteArray &ianaId)`
- `QTimeZone(int offsetSeconds)`
- `QTimeZone(const QByteArray &zoneId, int offsetSeconds, const QString &name, const QString &abbreviation, QLocale::Territory territory = QLocale::AnyTerritory, const QString &comment = QString())`
- `QTimeZone(const QTimeZone &other)`
- `QTimeZone(QTimeZone &&other)`
- `~QTimeZone()`
- `QString abbreviation(const QDateTime &atDateTime) const`
- `(since 6.5) QTimeZone asBackendZone() const`
- `QString comment() const`
- `int daylightTimeOffset(const QDateTime &atDateTime) const`
- `QString displayName(QTimeZone::TimeType timeType, QTimeZone::NameType nameType = DefaultName, const QLocale &locale = QLocale()) const`
- `QString displayName(const QDateTime &atDateTime, QTimeZone::NameType nameType = DefaultName, const QLocale &locale = QLocale()) const`
- `(since 6.5) int fixedSecondsAheadOfUtc() const`
- `(since 6.8) bool hasAlternativeName(QByteArrayView alias) const`
- `bool hasDaylightTime() const`
- `bool hasTransitions() const`
- `QByteArray id() const`
- `bool isDaylightTime(const QDateTime &atDateTime) const`
- `(since 6.5) bool isUtcOrFixedOffset() const`
- `bool isValid() const`
- `QTimeZone::OffsetData nextTransition(const QDateTime &afterDateTime) const`
- `QTimeZone::OffsetData offsetData(const QDateTime &forDateTime) const`
- `int offsetFromUtc(const QDateTime &atDateTime) const`
- `QTimeZone::OffsetData previousTransition(const QDateTime &beforeDateTime) const`
- `int standardTimeOffset(const QDateTime &atDateTime) const`
- `void swap(QTimeZone &other)`
- `(since 6.2) QLocale::Territory territory() const`
- `(since 6.5) Qt::TimeSpec timeSpec() const`
- `CFTimeZoneRef toCFTimeZone() const`
- `NSTimeZone * toNSTimeZone() const`
- `QTimeZone::OffsetDataList transitions(const QDateTime &fromDateTime, const QDateTime &toDateTime) const`
- `QTimeZone & operator=(QTimeZone &&other)`
- `QTimeZone & operator=(const QTimeZone &other)`

### 静态公有成员

- `QList<QByteArray> availableTimeZoneIds()`
- `QList<QByteArray> availableTimeZoneIds(QLocale::Territory territory)`
- `QList<QByteArray> availableTimeZoneIds(int offsetSeconds)`
- `QTimeZone fromCFTimeZone(CFTimeZoneRef timeZone)`
- `(since 6.5) QTimeZone fromDurationAheadOfUtc(std::chrono::seconds offset)`
- `QTimeZone fromNSTimeZone(const NSTimeZone *timeZone)`
- `(since 6.5) QTimeZone fromSecondsAheadOfUtc(int offset)`
- `(since 6.4) QTimeZone fromStdTimeZonePtr(const int *timeZone)`
- `QByteArray ianaIdToWindowsId(const QByteArray &ianaId)`
- `bool isTimeZoneIdAvailable(const QByteArray &ianaId)`
- `(since 6.5) bool isUtcOrFixedOffset(Qt::TimeSpec spec)`
- `QTimeZone systemTimeZone()`
- `QByteArray systemTimeZoneId()`
- `QTimeZone utc()`
- `QByteArray windowsIdToDefaultIanaId(const QByteArray &windowsId)`
- `QByteArray windowsIdToDefaultIanaId(const QByteArray &windowsId, QLocale::Territory territory)`
- `QList<QByteArray> windowsIdToIanaIds(const QByteArray &windowsId)`
- `QList<QByteArray> windowsIdToIanaIds(const QByteArray &windowsId, QLocale::Territory territory)`

### 相关非成员函数

- `bool operator!=(const QTimeZone &lhs, const QTimeZone &rhs)`
- `bool operator==(const QTimeZone &lhs, const QTimeZone &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.5] enum QTimeZone::Initialization`

**作用与语义：**

最简单的轻量级时间表示类型。
该枚举识别了一种轻量级时间表示，传递给`QTimeZone`构造器，无需额外数据。它们对应于`Qt::TimeSpec`中同名成员。
- `QTimeZone::LocalTime`：`0`;该时间表示方式对应于系统函数隐式使用`time_t`和`struct tm`值映射本地时间与UTC时间之间的表示方式。
- `QTimeZone::UTC`：`1`;这种时间表示法，即协调世界时，是所有支持的时间表示法中所指称的民用时间的基础表示。它由国际电信联盟定义。
这个枚举是在Qt 6.5引入的。

### `enum QTimeZone::NameType`

**作用与语义：**

时区名称的类型。
- `QTimeZone::DefaultName`：`0`;时区名称的默认形式，包括LongName、ShortName或OffsetName。
- `QTimeZone::LongName`：`1`;时区名称的长写形式，例如“中欧时间”
- `QTimeZone::ShortName`：`2`;时区名称的简写，通常为缩写，例如“CET”，在区域名称为该区域的地区，否则则是紧凑的GMT偏移形式，如“GMT 1”
- `QTimeZone::OffsetName`：`3`;标准ISO偏移时区名称形式，例如“UTC 01：00”
该类型仅在启用功能`timezone`时可用。

### `QTimeZone::OffsetDataList`

**作用与语义：**

`QList`的同义词<`OffsetData`>。
该类型仅在启用功能`timezone`时可用。

### `enum QTimeZone::TimeType`

**作用与语义：**

时区名称可能随季节变化，以表明其是否使用标准的UTC偏移，或对该偏移量进行夏令时调整。在这种情况下，通常还会有一个适用于其的整体名称，无论季节如何。在请求区域显示名称时，这种类型会指示使用哪一个名称。在不适用夏令时的时区，这三种值可能返回相同的结果。
- `QTimeZone::StandardTime`：`0`;该区的标准时间名称。例如，“太平洋标准时间”。
- `QTimeZone::DaylightTime`：`1`;夏令时实施时的区域名称。例如，“太平洋夏令时”。
- `QTimeZone::GenericTime`：`2`;该区域的名称，与其是否实施任何夏令时调整无关。例如，“太平洋时间”。
这种类型只有在启用功能`timezone`时才可用。

### `[noexcept] QTimeZone::QTimeZone()`

**作用与语义：**

创建一个空/无效的时区实例。

### `[noexcept, since 6.5] QTimeZone::QTimeZone(QTimeZone::Initialization spec)`

**作用与语义：**

创建描述UTC或当地时间的轻量级实例。

### `[explicit] QTimeZone::QTimeZone(const QByteArray &ianaId)`

**作用与语义：**

创建一个带有请求IANA ID `ianaId`的时区实例。
ID必须是可用的系统ID之一或有效的带偏移的UTC ID，否则返回的时区无效。对于带偏移的UTC ID，当它们实际上不是IANA ID，结果实例的`id()`可能与传递给构造器的ID不同。
该构造器仅在启用功能`timezone`时可用。

### `[explicit] QTimeZone::QTimeZone(int offsetSeconds)`

**作用与语义：**

创建一个时区实例，偏移量为`offsetSeconds`，与UTC相符。
UTC的 `offsetSeconds` 必须在 -16 到 16 小时之间，否则会返回无效时区。
该构造函数仅在启用功能`timezone`时可用。返回的实例等价于轻量级时间表示`QTimeZone::fromSecondsAheadOfUtc(offsetSeconds)`，尽管以时区形式实现。

### `QTimeZone::QTimeZone(const QByteArray &zoneId, int offsetSeconds, const QString &name, const QString &abbreviation, QLocale::Territory territory = QLocale::AnyTerritory, const QString &comment = QString())`

**作用与语义：**

创建一个自定义时区实例，固定偏移时间与UTC相符。
返回的时区ID为`zoneId`，UTC的偏移为`offsetSeconds`。`name`是`displayName()`对`LongName`使用的名称，`abbreviation`由`displayName()`用于`ShortName`和`abbreviation()`，可选`territory`由`territory()`使用。`comment`是一个可选备注，可以通过图形界面显示，帮助用户选择时区。
UTC的`offsetSeconds`必须在-16到16小时之间。`zoneId`不能是`isTimeZoneIdAvailable()`为真的ID，除非是UTC偏移的名称，但`availableTimeZoneIds()`中不存在。
如果自定义时区没有特定地区，则将其设置为默认值`QLocale::AnyTerritory`。
该构造函数仅在启用功能`timezone`时可用。

### `[noexcept] QTimeZone::QTimeZone(const QTimeZone &other)`

**作用与语义：**

复制构造器：复制`other`到这里。

### `[noexcept] QTimeZone::QTimeZone(QTimeZone &&other)`

**作用与语义：**

把这个构造器从`other`移开。

### `[noexcept] QTimeZone::~QTimeZone()`

**作用与语义：**

破坏时区。

### `QString QTimeZone::abbreviation(const QDateTime &atDateTime) const`

**作用与语义：**

在给定的时区缩写`atDateTime`返回。
缩写可能会根据夏令时甚至历史事件而变化。
注意：缩写不保证该时区唯一，不应替代ID或显示名称。缩写可能会本地化，具体取决于底层操作系统。为了获得一致的本地化，请使用`displayName(atDateTime, QTimeZone::ShortName, locale)`。
该方法仅在启用功能`timezone`时可用。

### `[since 6.5] QTimeZone QTimeZone::asBackendZone() const`

**作用与语义：**

将此`QTimeZone`转换为`timeSpec()`为`Qt::TimeZone`的。
在所有情况下，结果的`timeSpec()`都是`Qt::TimeZone`。当该`QTimeZone`的`timeSpec()`被`Qt::TimeZone`时，该`QTimeZone`本身被返回。如果`timeSpec()` `Qt::LocalTime`，则返回`systemTimeZone()`。
如果`timeSpec()` `Qt::UTC`，则返回`QTimeZone::utc()`。如果是`Qt::OffsetFromUTC`，则传递 `QTimeZone`（int） 的偏移量，返回结果。
当使用轻量级时间表示——本地时间、UTC时间或与UTC固定偏移的时间——仅支持功能`timezone`支持的方法可能比使用对应时区更昂贵。该方法将轻量级时间表示映射到对应的时区——即基于系统提供的或标准数据的实例。
该方法仅在启用功能`timezone`时可用。

### `[static] QList<QByteArray> QTimeZone::availableTimeZoneIds()`

**作用与语义：**

返回该系统中所有可用的IANA时区ID列表。
该方法仅在启用功能`timezone`时可用。
注意：`QTimeZone`构造器还会接受一些未在返回列表中的UTC偏移ID——列出所有可能的UTC偏移ID是不切实际的。

### `[static] QList<QByteArray> QTimeZone::availableTimeZoneIds(QLocale::Territory territory)`

**作用与语义：**

返回给定`territory`所有可用的IANA时区ID列表。
作为特殊情况，`territory` of `AnyTerritory` 选择那些具有非地域关联的时区，如 UTC，而 `World` 选择那些存在全局默认 IANA ID 的时区。如果你需要所有地区的所有时区 ID 列表，则使用标准的可用 TimeZoneIds() 方法。
该方法仅在启用功能`timezone`时可用。

### `[static] QList<QByteArray> QTimeZone::availableTimeZoneIds(int offsetSeconds)`

**作用与语义：**

返回所有可用的IANA时区ID列表，标准时间偏移为`offsetSeconds`。
在支持给定偏移量的情况下，`QTimeZone(offsetSeconds).id()`会包含在列表中，即使它不是IANA ID。只有当没有带有该偏移的IANAUTC偏移ID时，才会出现这种情况。
该方法仅在启用功能`timezone`时可用。

### `QString QTimeZone::comment() const`

**作用与语义：**

回复任何关于时区的评论。
主机平台可能会提供评论，帮助用户选择正确的时区。根据平台不同，这可能无法本地化。
该方法仅在启用功能`timezone`时可用。

### `int QTimeZone::daylightTimeOffset(const QDateTime &atDateTime) const`

**作用与语义：**

返回给定`atDateTime`的夏令时偏移，即将时间相加于标准时间偏移以获得当地夏令时的秒数。
例如，在“欧洲/柏林”时区，夏令时偏移为3600秒。在标准时间下，daylightTimeOffset()返回0，而在夏令时生效时返回3600秒。
该方法仅在启用功能`timezone`时可用。

### `QString QTimeZone::displayName(QTimeZone::TimeType timeType, QTimeZone::NameType nameType = DefaultName, const QLocale &locale = QLocale()) const`

**作用与语义：**

返回本地化的时区显示名称。
返回的名称是给定`locale`的名称，适用于该`timeType`生效且形式为`nameType`所示。如果时区显示名称随时间变化，则使用当前名称。如果没有相应本地化的名称可用，可以使用其他名称类型，或者返回空字符串。
如果未提供`locale`，则将使用应用默认的区域。对于客户端代码创建的自定义时区，使用构建器提供的数据，因为构造器不会有本地化数据。如果该时区无效，返回空字符串。如果系统时区判定失败，本地时间表示也可能出现这种情况。
该方法仅在启用功能`timezone`时可用。

### `QString QTimeZone::displayName(const QDateTime &atDateTime, QTimeZone::NameType nameType = DefaultName, const QLocale &locale = QLocale()) const`

**作用与语义：**

返回本地化的时区显示名称。
返回的名称是给定`locale`的名称，适用于指定`atDateTime`，且形式为`nameType`所示。显示名称可能会根据夏令时或历史事件而变化。如果没有相应本地化的名称可用，可以使用其他名称类型，或者返回空字符串。
如果未提供`locale`，则使用应用默认的区域。对于客户端代码创建的自定义时区，使用构建器提供的数据，因为没有本地化数据可用。如果该时区无效，则返回空字符串。如果无法确定系统时区，也可能出现在本地时间表示中。
该方法仅在启用功能`timezone`时可用。

### `[constexpr noexcept, since 6.5] int QTimeZone::fixedSecondsAheadOfUtc() const`

**作用与语义：**

对于`timeSpec()`为`Qt::OffsetFromUTC`的轻量级时间表示，返回其所描述的固定UTC偏移量。对于其他时间表示，返回0，即使该时间表示与UTC有常偏移。

### `[static] QTimeZone QTimeZone::fromCFTimeZone(CFTimeZoneRef timeZone)`

**作用与语义：**

构建包含CFTimeZone `timeZone`副本的新`QTimeZone`。

### `[static] QTimeZone QTimeZone::fromNSTimeZone(const NSTimeZone *timeZone)`

**作用与语义：**

构建了一个包含 NSTimeZone `timeZone` 副本的新`QTimeZone`。

### `[static, since 6.5] QTimeZone QTimeZone::fromDurationAheadOfUtc(std::chrono::seconds offset)`

**作用与语义：**

返回一个固定`offset`的时间表示，单位为秒，领先UTC。
UTC的`offset`必须在-16小时到16小时之间，否则返回的时区将是无效的。返回的`QTimeZone`是轻量级时间表示，而非时区（有系统提供或标准数据支持）。
如果偏移量为0，返回实例的`timeSpec()`将`Qt::UTC`。否则，如果`offset`有效，则`timeSpec()`为`Qt::OffsetFromUTC`。无效时区返回时，其`timeSpec()`为`Qt::TimeZone`。

### `[static, since 6.4] QTimeZone QTimeZone::fromStdTimeZonePtr(const int *timeZone)`

**作用与语义：**

返回一个`QTimeZone`对象，代表与`timeZone`相同的时区。`timeZone`的IANA ID必须是可用的系统ID之一，否则返回的时区无效。
该方法仅在启用功能`timezone`时可用。

### `[since 6.8] bool QTimeZone::hasAlternativeName(QByteArrayView alias) const`

**作用与语义：**

如果 `alias` 是此时区的别名，则返回 `timezone`。IANA（前身为 Olson）数据库在其历史中对一些时区进行了重命名。还有一些时区在1970年之前有所不同，但现在被视为同义。有些后端的数据可能追溯到1970年以前，并在后一种情况下产生不同的时区。其他后端可能会生成除 `id()` 外无法区分的时区。此方法用于确定一个 ID 是否指向（至少自1970年以来）与此时区对象描述的相同时区。仅当启用 `timezone` 功能时，此方法才可用。

### `bool QTimeZone::hasDaylightTime() const`

**作用与语义：**

如果该时区曾实行夏令时，返回时间`true`。
该方法仅在启用功能`timezone`时可用。

### `bool QTimeZone::hasTransitions() const`

**作用与语义：**

如果系统后端支持获取转换，返回`true`。
过渡是指时区的变化：发生在夏令时开关以及当局调整时区偏移时。
该方法仅在启用功能`timezone`时可用。

### `[static] QByteArray QTimeZone::ianaIdToWindowsId(const QByteArray &ianaId)`

**作用与语义：**

返回与给定`ianaId`等效的 Windows ID。
该方法仅在启用功能`timezone`时可用。

### `QByteArray QTimeZone::id() const`

**作用与语义：**

返回时区的IANA ID。
IANA ID 在所有平台上都使用。在 Windows 上，这些 ID 会从 Windows ID 转换成时区和地区最匹配的 IANA ID。
如果该时区实例不是由IANA ID构建的，其ID将根据构建方式决定。在大多数情况下，使用构建实例时传递的ID。（自定义区域的构造器使用传递的ID，而该ID不能是IANA ID。）有两个例外。
- 仅通过秒数传递UTC偏移量构建的实例在构建时不传递ID。
- 仅使用 IANA ID 的构造函数也会接受一些实际上并非 IANA ID 的 UTC 偏移 ID：其处理这些 ID 相当于在秒内传递对应的偏移，就像第一个例外一样。
在两种例外情况下，如果存在具有指定偏移量的 IANA UTC 偏移区，构造实例使用该 IANA 区的 ID，尽管这可能与传递给构造器的（非 IANA 的）UTC 偏移 ID 不同。否则，实例使用由偏移合成的 ID，格式为 UTC±hh：mm：ss，且后尾的 ：00 不计任何零秒或零分钟。同样，这可能与传递给构造器的 UTC 偏移 ID。
该方法仅在启用功能`timezone`时可用。

### `bool QTimeZone::isDaylightTime(const QDateTime &atDateTime) const`

**作用与语义：**

返回数据`true` `atDateTime`时是否实施夏令时。
该方法仅在启用功能`timezone`时可用。

### `[static] bool QTimeZone::isTimeZoneIdAvailable(const QByteArray &ianaId)`

**作用与语义：**

如果该系统`ianaId`可用，退货`true`。
这可能包括一些非IANA编号，尤其是UTC偏移ID，这些ID未被列入`availableTimeZoneIds()`。
该方法仅在启用功能`timezone`时可用。

### `[constexpr noexcept, since 6.5] bool QTimeZone::isUtcOrFixedOffset() const`

**作用与语义：**

如果 `timeSpec()` 是 `Qt::UTC` 或 `Qt::OffsetFromUTC`，则返回 `true`。 当它为真时，时间描述不会随时间变化，例如可能发生在本地时间或时区的季节性夏令时更改。 知道这一点可以让调用代码无需进行其他各种检查。

### `[static constexpr noexcept, since 6.5] bool QTimeZone::isUtcOrFixedOffset(Qt::TimeSpec spec)`

**作用与语义：**

如果 `spec` 是 `Qt::UTC` 或 `Qt::OffsetFromUTC`，则返回 `true`。

### `bool QTimeZone::isValid() const`

**作用与语义：**

如果此时区有效，则返回 `true`。

### `QTimeZone::OffsetData QTimeZone::nextTransition(const QDateTime &afterDateTime) const`

**作用与语义：**

在给定`afterDateTime`之后返回第一个时区转换。当你有过渡时间并希望找到之后的过渡时，这最有用。
如果在给定`afterDateTime`后没有过渡，则返回无效`OffsetData`，`atUtc`为无效`QDateTime`。
给定的`afterDateTime`是排他性的。
该方法仅在启用功能`timezone`时可用。

### `QTimeZone::OffsetData QTimeZone::offsetData(const QDateTime &forDateTime) const`

**作用与语义：**

返回给定`forDateTime`的有效偏移信息。
这相当于分别调用`abbreviation()`和三个偏移函数，但可能更高效，并且缩写的定位也可能不同。如果该数据在给定日期时间不可用，则返回无效`OffsetData`，`atUtc`为无效`QDateTime`。
该方法仅在启用功能`timezone`时可用。

### `int QTimeZone::offsetFromUtc(const QDateTime &atDateTime) const`

**作用与语义：**

返回给定`atDateTime`的总有效偏移，即为获得当地时间，需加到UTC的秒数。这包括可能生效的任何夏令时偏移量，即给定日期时间的 `standardTimeOffset()` 和 `daylightTimeOffset()` 之和。
例如，在“欧洲/柏林”时区，标准时间偏移为3600秒，夏令时偏移为3600秒。在标准时间偏移期间，FromUtc()返回3600（UTC 01：00），在DST期间返回7200（UTC 02：00）。
该方法仅在启用功能`timezone`时可用。

### `QTimeZone::OffsetData QTimeZone::previousTransition(const QDateTime &beforeDateTime) const`

**作用与语义：**

返回给定`beforeDateTime`之前的第一个时区转换。当你有过渡时间并希望找到之前的过渡时，这最有用。
如果在给定`beforeDateTime`之前没有过渡，则返回无效`OffsetData`，`QDateTime`为无效`atUtc`。
给定的`beforeDateTime`是排他性的。
该方法仅在启用功能`timezone`时可用。

### `int QTimeZone::standardTimeOffset(const QDateTime &atDateTime) const`

**作用与语义：**

返回给定`atDateTime`的标准时间偏移，即为获得当地标准时间，需加到UTC的秒数。这排除了可能生效的任何夏令时偏移。
例如，在“欧洲/柏林”时区，标准时间偏移为3600秒。在标准时间和夏令时，`offsetFromUtc()`返回3600秒（UTC 01：00）。
该方法仅在启用功能`timezone`时可用。

### `[noexcept] void QTimeZone::swap(QTimeZone &other)`

**作用与语义：**

将这个时区实例与`other`互换。这个操作非常快，从未失败过。

### `[static] QTimeZone QTimeZone::systemTimeZone()`

**作用与语义：**

返回描述本地系统时间的`QTimeZone`对象。
该方法仅在启用功能`timezone`时可用。返回的实例通常等价于轻量级时间表示`QTimeZone(QTimeZone::LocalTime)`，尽管实现为时区。
返回的对象不会因系统时区的后续变化而改变。它代表调用`asBackendZone()`时生效的本地时间。在配置错误的系统中，例如缺少后端所依赖的时区数据的系统，Qt可能无效。在这种情况下，会输出警告。

### `[static] QByteArray QTimeZone::systemTimeZoneId()`

**作用与语义：**

返回当前系统时区IANA ID。
等价于调用`systemTimeZone()`。`id()`，但可能会绕过某些计算来获得它。从返回的字节数组构造一个`QTimeZone`，结果与`systemTimeZone()`相同。
如果后端无法确定正确的系统区域，结果为空。在这种情况下，`systemTimeZone()`。`isValid()`为假，如果调用该`systemTimeZone()`方法，则会输出警告。
如果后端能够确定正确的系统区域但无法确定其名称，则返回一个空字节数组。例如，在 Windows 上，系统原生 ID 会转换为 IANA ID——如果系统 ID 内部翻译代码不知道，结果应为空。在这种情况下，`systemTimeZone()`。`isValid()` 应为真。
该方法仅在启用功能`timezone`时可用。
注意：在第6.7期之前，当无法确定结果时，回传了误导性结果“UTC”。

### `[since 6.2] QLocale::Territory QTimeZone::territory() const`

**作用与语义：**

返回该时区的领地。
返回`AnyTerritory`意味着该区域没有已知的领土关联。在某些情况下，这可能是因为该区域没有关联的领土——例如UTC——或者该区域在多个领土中使用——例如CET。在其他情况下，`QTimeZone`后端可能不知道该区域关联的是哪个领土——例如，因为它不是其所使用领土的主要区域。
该方法仅在启用功能`timezone`时可用。

### `[constexpr noexcept, since 6.5] Qt::TimeSpec QTimeZone::timeSpec() const`

**作用与语义：**

返回识别时间表示类型的`Qt::TimeSpec`。
如果结果是`Qt::TimeZone`，这个时间描述是时区（有系统提供或标准数据支持）;否则，它是轻量级时间表示。如果结果`Qt::LocalTime`，则描述本地时间：详情请参见 `Qt::TimeSpec`。

### `CFTimeZoneRef QTimeZone::toCFTimeZone() const`

**作用与语义：**

从`QTimeZone`创建一个CFTimeZone。
调用者拥有CFTimeZone对象，并负责释放该对象。

### `NSTimeZone *QTimeZone::toNSTimeZone() const`

**作用与语义：**

从`QTimeZone`创建一个NSTimeZone。
NSTimeZone 对象是自动释放的。

### `QTimeZone::OffsetDataList QTimeZone::transitions(const QDateTime &fromDateTime, const QDateTime &toDateTime) const`

**作用与语义：**

返回所有给定日期时间之间的时区转换列表。
给定的`fromDateTime`和`toDateTime`是包含的。每个条目中的`atUtc`成员描述了转移的时刻，即其他成员给出的偏移量和缩写生效的时刻。
该方法仅在启用功能`timezone`时可用。

### `[static] QTimeZone QTimeZone::utc()`

**作用与语义：**

返回一个`QTimeZone`对象，描述UTC为时区。
该方法仅在启用功能`timezone`时可用。它等同于将0传递给`QTimeZone`（整数偏移秒）和轻量级时间表示`QTimeZone`（`QTimeZone::UTC`），尽管它是以时区实现的，而后者则不同。

### `[static] QByteArray QTimeZone::windowsIdToDefaultIanaId(const QByteArray &windowsId)`

**作用与语义：**

返回给定`windowsId`的默认IANA ID。
由于 Windows ID 可以覆盖多个不同区域的多个 IANA ID，该功能返回最常用的 IANA ID，不考虑区域，因此应谨慎使用。通常最好请求特定区域的默认值。
该方法仅在启用功能`timezone`时可用。

### `[static] QByteArray QTimeZone::windowsIdToDefaultIanaId(const QByteArray &windowsId, QLocale::Territory territory)`

**作用与语义：**

返回给定`windowsId`和`territory`的默认IANA ID。
由于 Windows ID 可以覆盖同一区域内多个 IANA ID，因此返回该区域内最常用的 IANA ID。
作为特殊情况，`AnyTerritory`返回那些与非领土关联的IANA ID的默认值，而`World`则返回与该`windowsId`没有特定关联的地区默认值。
如果申报是空的，则该`windowsId`没有针对该`territory`的专用IANA ID。在这种情况下，回退到`windowsIdToDefaultIanaId(windowsId)`是合理的。
该方法仅在启用功能`timezone`时可用。

### `[static] QList<QByteArray> QTimeZone::windowsIdToIanaIds(const QByteArray &windowsId)`

**作用与语义：**

返回给定`windowsId`的所有IANA ID。
返回的列表按字母顺序排列。
该方法仅在启用功能`timezone`时可用。

### `[static] QList<QByteArray> QTimeZone::windowsIdToIanaIds(const QByteArray &windowsId, QLocale::Territory territory)`

**作用与语义：**

返回给定`windowsId`的所有IANA ID，并返回`territory`。
作为特殊情况，`AnyTerritory`选择那些与非领土关联的IANA ID，而`World`则选择与该`windowsId`无特定关联的地区默认ID。
返回的列表按使用频率排序，即领土内较大的区域优先列出。
该方法仅在启用功能`timezone`时可用。

### `[noexcept] QTimeZone &QTimeZone::operator=(QTimeZone &&other)`

**作用与语义：**

Move-Assign `other` 给该`QTimeZone`实例，将其数据的所有权转移给该实例。

### `QTimeZone &QTimeZone::operator=(const QTimeZone &other)`

**作用与语义：**

分配操作员，把`other`分配到这个。

### `const int QTimeZone::MaxUtcOffsetSecs`

**作用与语义：**

预计UTC的时区偏移不会超过这个。
21世纪初任何时区中最高的UTC偏移是14小时（圣诞岛、基里巴斯、基里蒂马蒂），或格林威治以东14小时。
历史上，在1867年俄罗斯将阿拉斯加卖给美国之前，阿拉斯加使用与俄罗斯相同的日期，因此在格林威治以东有超过15小时的偏移。由于阿拉斯加使用当地太阳能平均时间，其偏移量有所变化，但所有时间均在格林尼治以东不到16小时。

### `const int QTimeZone::MinUtcOffsetSecs`

**作用与语义：**

预计UTC的时区偏移不会低于此值。
21世纪初任何时区中最低的UTC偏移是-12小时（美国贝克岛），或格林威治以西12小时。
历史上，直到1844年，菲律宾（当时由西班牙控制）使用与西班牙美国殖民地相同的日期，因此在格林威治以西约16小时的日期相差。由于菲律宾使用当地的太阳能平均时间，其部分周边地区可能在格林威治以西超过16小时处运行，但21世纪初没有哪个时区能追溯到如此极端的历史。

### `[noexcept] bool operator!=(const QTimeZone &lhs, const QTimeZone &rhs)`

**作用与语义：**

如果时区不等于`rhs`时区`lhs`，退货`true`。
如果两个表示在内部描述不同，即使它们对所有时刻的表示一致，它们也存在差异。特别地，轻量级时间表示可能与时区重合，但两者不会相等。

### `[noexcept] bool operator==(const QTimeZone &lhs, const QTimeZone &rhs)`

**作用与语义：**

如果`lhs`时区等于`rhs`时区，返回`true`。
如果两个表示在内部描述不同，即使它们对所有时刻的表示一致，它们也存在差异。特别地，轻量级时间表示可能与时区重合，但两者不会相等。

### `struct OffsetData`

**作用与语义：**

时区偏移数据针对特定时间点。
这提供了在特定时间点可用的时区偏移量和缩写。当函数返回该类型时，可能会使用无效的日期时间表示其回答的查询无有效答案，因此在使用结果前请检查`atUtc.isValid()`。
- OffsetData：：atUTC 偏移数据的UTC时间。
- OffsetData：：offsetFromUTC 在日期时间与UTC的总偏移量。
- OffsetData：：standardTimeOffset 总偏移量中的标准时间偏移分量。
- OffsetData：:d aylightTimeOffset 总偏移量中的 DST 偏移分量。
- OffsetData：：缩写 日期时间生效的缩写。
例如，对于“欧洲/柏林”时区，标准和夏令时的偏移日期可能为：
- atUtc = `QDateTime`（`QDate`（2013， 1）， `QTime`（0， 0）， `QTimeZone::UTC`）
- `offsetFromUtc` = 3600
- `standardTimeOffset` = 3600
- `daylightTimeOffset` = 0
- 缩写 = “CET”
- atUtc = `QDateTime`（`QDate`（2013， 6， 1）， `QTime`（0， 0）， `QTimeZone::UTC`）
- `offsetFromUtc` = 7200
- `daylightTimeOffset` = 3600
- 缩写 = “CEST”
该类型仅在启用功能`timezone`时可用。

### `OffsetDataList`

**作用与语义：**

`QList`的同义词<`OffsetData`>。
该类型仅在启用功能`timezone`时可用。

### `(since 6.5) QTimeZone fromSecondsAheadOfUtc(int offset)`

**作用与语义：**

返回一个固定`offset`的时间表示，单位为秒，领先UTC。
UTC的`offset`必须在-16小时到16小时之间，否则返回的时区将是无效的。返回的`QTimeZone`是轻量级时间表示，而非时区（有系统提供或标准数据支持）。
如果偏移量为0，返回实例的`timeSpec()`将`Qt::UTC`。否则，如果`offset`有效，则`timeSpec()`为`Qt::OffsetFromUTC`。无效时区返回时，其`timeSpec()`为`Qt::TimeZone`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QTimeZone` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
