# QLocale

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“区域设置”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QLocale` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QLocale>`
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

- `enum Country { AnyCountry, AnyTerritory, Afghanistan, AlandIslands, Albania, …, Zimbabwe }`
- `enum CurrencySymbolFormat { CurrencyIsoCode, CurrencySymbol, CurrencyDisplayName }`
- `enum DataSizeFormat { DataSizeIecFormat, DataSizeTraditionalFormat, DataSizeSIFormat }`
- `flags DataSizeFormats`
- `enum FloatingPointPrecisionOption { FloatingPointShortest }`
- `enum FormatType { LongFormat, ShortFormat, NarrowFormat }`
- `enum Language { AnyLanguage, C, Abkhazian, Afan, Afar, …, Zulu }`
- `enum LanguageCodeType { ISO639Part1, ISO639Part2B, ISO639Part2T, ISO639Part3, LegacyLanguageCode, …, AnyLanguageCode }`
- `flags LanguageCodeTypes`
- `enum MeasurementSystem { MetricSystem, ImperialUSSystem, ImperialUKSystem, ImperialSystem }`
- `enum NumberOption { DefaultNumberOptions, OmitGroupSeparator, RejectGroupSeparator, OmitLeadingZeroInExponent, RejectLeadingZeroInExponent, …, RejectTrailingZeroesAfterDot }`
- `flags NumberOptions`
- `enum QuotationStyle { StandardQuotation, AlternateQuotation }`
- `enum Script { AnyScript, AdlamScript, AhomScript, AnatolianHieroglyphsScript, ArabicScript, …, YiScript }`
- `(since 6.7) enum class TagSeparator { Dash, Underscore }`
- `Territory`

### 公有函数

- `QLocale()`
- `(since 6.3) QLocale(QStringView name)`
- `QLocale(QLocale::Language language, QLocale::Territory territory)`
- `QLocale(QLocale::Language language, QLocale::Script script = AnyScript, QLocale::Territory territory = AnyTerritory)`
- `QLocale(const QString &name)`
- `QLocale(const QLocale &other)`
- `~QLocale()`
- `QString amText() const`
- `QString bcp47Name(QLocale::TagSeparator separator = TagSeparator::Dash) const`
- `QLocale collation() const`
- `QString createSeparatedList(const QStringList &list) const`
- `QString currencySymbol(QLocale::CurrencySymbolFormat format = CurrencySymbol) const`
- `QString dateFormat(QLocale::FormatType format = LongFormat) const`
- `QString dateTimeFormat(QLocale::FormatType format = LongFormat) const`
- `QString dayName(int day, QLocale::FormatType type = LongFormat) const`
- `QString decimalPoint() const`
- `QString exponential() const`
- `Qt::DayOfWeek firstDayOfWeek() const`
- `QString formattedDataSize(qint64 bytes, int precision = 2, QLocale::DataSizeFormats format = DataSizeIecFormat) const`
- `QString groupSeparator() const`
- `QLocale::Language language() const`
- `QLocale::MeasurementSystem measurementSystem() const`
- `QString monthName(int month, QLocale::FormatType type = LongFormat) const`
- `QString name(QLocale::TagSeparator separator = TagSeparator::Underscore) const`
- `QString nativeLanguageName() const`
- `(since 6.2) QString nativeTerritoryName() const`
- `QString negativeSign() const`
- `QLocale::NumberOptions numberOptions() const`
- `QString percent() const`
- `QString pmText() const`
- `QString positiveSign() const`
- `QString quoteString(const QString &str, QLocale::QuotationStyle style = StandardQuotation) const`
- `(since 6.0) QString quoteString(QStringView str, QLocale::QuotationStyle style = StandardQuotation) const`
- `QLocale::Script script() const`
- `void setNumberOptions(QLocale::NumberOptions options)`
- `QString standaloneDayName(int day, QLocale::FormatType type = LongFormat) const`
- `QString standaloneMonthName(int month, QLocale::FormatType type = LongFormat) const`
- `void swap(QLocale &other)`
- `(since 6.2) QLocale::Territory territory() const`
- `Qt::LayoutDirection textDirection() const`
- `QString timeFormat(QLocale::FormatType format = LongFormat) const`
- `QString toCurrencyString(qlonglong value, const QString &symbol = QString()) const`
- `QString toCurrencyString(int value, const QString &symbol = QString()) const`
- `QString toCurrencyString(qulonglong value, const QString &symbol = QString()) const`
- `QString toCurrencyString(short value, const QString &symbol = QString()) const`
- `QString toCurrencyString(uint value, const QString &symbol = QString()) const`
- `QString toCurrencyString(ushort value, const QString &symbol = QString()) const`
- `QString toCurrencyString(double value, const QString &symbol = QString(), int precision = -1) const`
- `QString toCurrencyString(float i, const QString &symbol = QString(), int precision = -1) const`
- `QDate toDate(const QString &string, QLocale::FormatType format = LongFormat, int baseYear = DefaultTwoDigitBaseYear) const`
- `QDate toDate(const QString &string, const QString &format, int baseYear = DefaultTwoDigitBaseYear) const`
- `QDate toDate(const QString &string, QLocale::FormatType format, QCalendar cal, int baseYear = DefaultTwoDigitBaseYear) const`
- `QDate toDate(const QString &string, const QString &format, QCalendar cal, int baseYear = DefaultTwoDigitBaseYear) const`
- `QDateTime toDateTime(const QString &string, QLocale::FormatType format = LongFormat, int baseYear = DefaultTwoDigitBaseYear) const`
- `QDateTime toDateTime(const QString &string, const QString &format, int baseYear = DefaultTwoDigitBaseYear) const`
- `QDateTime toDateTime(const QString &string, QLocale::FormatType format, QCalendar cal, int baseYear = DefaultTwoDigitBaseYear) const`
- `QDateTime toDateTime(const QString &string, const QString &format, QCalendar cal, int baseYear = DefaultTwoDigitBaseYear) const`
- `double toDouble(QStringView s, bool *ok = nullptr) const`
- `double toDouble(const QString &s, bool *ok = nullptr) const`
- `float toFloat(QStringView s, bool *ok = nullptr) const`
- `float toFloat(const QString &s, bool *ok = nullptr) const`
- `int toInt(QStringView s, bool *ok = nullptr) const`
- `int toInt(const QString &s, bool *ok = nullptr) const`
- `long toLong(QStringView s, bool *ok = nullptr) const`
- `long toLong(const QString &s, bool *ok = nullptr) const`
- `qlonglong toLongLong(QStringView s, bool *ok = nullptr) const`
- `qlonglong toLongLong(const QString &s, bool *ok = nullptr) const`
- `QString toLower(const QString &str) const`
- `short toShort(QStringView s, bool *ok = nullptr) const`
- `short toShort(const QString &s, bool *ok = nullptr) const`
- `QString toString(qlonglong i) const`
- `QString toString(QDate date, const QString &format) const`
- `QString toString(QTime time, QLocale::FormatType format = LongFormat) const`
- `QString toString(QTime time, QStringView format) const`
- `QString toString(QTime time, const QString &format) const`
- `QString toString(const QDateTime &dateTime, const QString &format) const`
- `QString toString(QDate date, QLocale::FormatType format, QCalendar cal) const`
- `QString toString(QDate date, QStringView format, QCalendar cal) const`
- `QString toString(const QDateTime &dateTime, QLocale::FormatType format, QCalendar cal) const`
- `QString toString(const QDateTime &dateTime, QStringView format, QCalendar cal) const`
- `QString toString(int i) const`
- `QString toString(long i) const`
- `QString toString(qulonglong i) const`
- `QString toString(short i) const`
- `QString toString(uint i) const`
- `QString toString(ulong i) const`
- `QString toString(ushort i) const`
- `QString toString(QDate date, QLocale::FormatType format = LongFormat) const`
- `QString toString(QDate date, QStringView format) const`
- `QString toString(const QDateTime &dateTime, QLocale::FormatType format = LongFormat) const`
- `QString toString(const QDateTime &dateTime, QStringView format) const`
- `QString toString(double f, char format = 'g', int precision = 6) const`
- `QString toString(float f, char format = 'g', int precision = 6) const`
- `QString toString(int number, int fieldWidth, char32_t fillChar) const`
- `QString toString(long number, int fieldWidth, char32_t fillChar) const`
- `QString toString(qlonglong number, int fieldWidth, char32_t fillChar) const`
- `QString toString(qulonglong number, int fieldWidth, char32_t fillChar) const`
- `QString toString(short number, int fieldWidth, char32_t fillChar) const`
- `QString toString(uint number, int fieldWidth, char32_t fillChar) const`
- `QString toString(ulong number, int fieldWidth, char32_t fillChar) const`
- `QString toString(ushort number, int fieldWidth, char32_t fillChar) const`
- `QTime toTime(const QString &string, QLocale::FormatType format = LongFormat) const`
- `QTime toTime(const QString &string, const QString &format) const`
- `uint toUInt(QStringView s, bool *ok = nullptr) const`
- `uint toUInt(const QString &s, bool *ok = nullptr) const`
- `ulong toULong(QStringView s, bool *ok = nullptr) const`
- `ulong toULong(const QString &s, bool *ok = nullptr) const`
- `qulonglong toULongLong(QStringView s, bool *ok = nullptr) const`
- `qulonglong toULongLong(const QString &s, bool *ok = nullptr) const`
- `ushort toUShort(QStringView s, bool *ok = nullptr) const`
- `ushort toUShort(const QString &s, bool *ok = nullptr) const`
- `QString toUpper(const QString &str) const`
- `QStringList uiLanguages(QLocale::TagSeparator separator = TagSeparator::Dash) const`
- `QList<Qt::DayOfWeek> weekdays() const`
- `QString zeroDigit() const`
- `QLocale & operator=(const QLocale &other)`

### 静态公有成员

- `QLocale c()`
- `(since 6.3) QLocale::Language codeToLanguage(QStringView languageCode, QLocale::LanguageCodeTypes codeTypes = AnyLanguageCode)`
- `(since 6.1) QLocale::Script codeToScript(QStringView scriptCode)`
- `(since 6.2) QLocale::Territory codeToTerritory(QStringView territoryCode)`
- `(since 6.3) QString languageToCode(QLocale::Language language, QLocale::LanguageCodeTypes codeTypes = AnyLanguageCode)`
- `QString languageToString(QLocale::Language language)`
- `QList<QLocale> matchingLocales(QLocale::Language language, QLocale::Script script, QLocale::Territory territory)`
- `(since 6.1) QString scriptToCode(QLocale::Script script)`
- `QString scriptToString(QLocale::Script script)`
- `void setDefault(const QLocale &locale)`
- `QLocale system()`
- `(since 6.2) QString territoryToCode(QLocale::Territory territory)`
- `(since 6.2) QString territoryToString(QLocale::Territory territory)`

### 相关非成员函数

- `size_t qHash(const QLocale &key, size_t seed = 0)`
- `bool operator!=(const QLocale &lhs, const QLocale &rhs)`
- `bool operator==(const QLocale &lhs, const QLocale &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QLocale::Country`

**作用与语义：**

这种列举类型用于标识领土。
单个领土可以是国家的一个省份、一个国家（这是最常见的情况）或更大的地理实体，部分本地化细节是针对其特定的。
- `QLocale::AnyCountry`：`AnyTerritory`;奥斯博莱特的别名`AnyTerritory`
- `QLocale::AnyTerritory (since Qt 6.2)`：`0`
- `QLocale::Afghanistan`：`1`
- `QLocale::AlandIslands`：`2`
- `QLocale::Albania`：`3`
- `QLocale::Algeria`：`4`
- `QLocale::AmericanSamoa`：`5`
- `QLocale::Andorra`：`6`
- `QLocale::Angola`：`7`
- `QLocale::Anguilla`：`8`
- `QLocale::Antarctica`：`9`
- `QLocale::AntiguaAndBarbuda`：`10`
- `QLocale::Argentina`：`11`
- `QLocale::Armenia`：`12`
- `QLocale::Aruba`：`13`
- `QLocale::AscensionIsland`：`14`
- `QLocale::Australia`：`15`
- `QLocale::Austria`：`16`
- `QLocale::Azerbaijan`：`17`
- `QLocale::Bahamas`：`18`
- `QLocale::Bahrain`：`19`
- `QLocale::Bangladesh`：`20`
- `QLocale::Barbados`：`21`
- `QLocale::Belarus`：`22`
- `QLocale::Belgium`：`23`
- `QLocale::Belize`：`24`
- `QLocale::Benin`：`25`
- `QLocale::Bermuda`：`26`
- `QLocale::Bhutan`：`27`
- `QLocale::Bolivia`：`28`
- `QLocale::Bonaire`：`CaribbeanNetherlands`
- `QLocale::BosniaAndHerzegowina`：`BosniaAndHerzegovina`;过时，请用`BosniaAndHerzegovina`
- `QLocale::BosniaAndHerzegovina (since Qt 6.0)`：`29`
- `QLocale::Botswana`：`30`
- `QLocale::BouvetIsland`：`31`
- `QLocale::Brazil`：`32`
- `QLocale::BritishIndianOceanTerritory`：`33`
- `QLocale::BritishVirginIslands`：`34`
- `QLocale::Brunei`：`35`
- `QLocale::Bulgaria`：`36`
- `QLocale::BurkinaFaso`：`37`
- `QLocale::Burundi`：`38`
- `QLocale::Cambodia`：`39`
- `QLocale::Cameroon`：`40`
- `QLocale::Canada`：`41`
- `QLocale::CanaryIslands`：`42`
- `QLocale::CaribbeanNetherlands`：`44`
- `QLocale::CapeVerde`：`43`
- `QLocale::CaymanIslands`：`45`
- `QLocale::CentralAfricanRepublic`：`46`
- `QLocale::CeutaAndMelilla`：`47`
- `QLocale::Chad`：`48`
- `QLocale::Chile`：`49`
- `QLocale::China`：`50`
- `QLocale::ChristmasIsland`：`51`
- `QLocale::ClippertonIsland`：`52`
- `QLocale::CocosIslands`：`53`
- `QLocale::Colombia`：`54`
- `QLocale::Comoros`：`55`
- `QLocale::CongoBrazzaville`：`56`
- `QLocale::CongoKinshasa`：`57`
- `QLocale::CookIslands`：`58`
- `QLocale::CostaRica`：`59`
- `QLocale::Croatia`：`60`
- `QLocale::Cuba`：`61`
- `QLocale::Curacao (since Qt 6.0)`：`62`
- `QLocale::CuraSao`：`Curacao`;已过时，改用`Curacao`
- `QLocale::Cyprus`：`63`
- `QLocale::Czechia (since Qt 6.0)`：`64`
- `QLocale::CzechRepublic`：`Czechia`;已过时，改用`Czechia`
- `QLocale::DemocraticRepublicOfCongo`：`CongoKinshasa`;已过时，请用`CongoKinshasa`
- `QLocale::DemocraticRepublicOfKorea`：`NorthKorea`;已过时，改用`NorthKorea`
- `QLocale::Denmark`：`65`
- `QLocale::DiegoGarcia`：`66`
- `QLocale::Djibouti`：`67`
- `QLocale::Dominica`：`68`
- `QLocale::DominicanRepublic`：`69`
- `QLocale::EastTimor`：`TimorLeste`
- `QLocale::Ecuador`：`70`
- `QLocale::Egypt`：`71`
- `QLocale::ElSalvador`：`72`
- `QLocale::EquatorialGuinea`：`73`
- `QLocale::Eritrea`：`74`
- `QLocale::Estonia`：`75`
- `QLocale::Eswatini`：`76`
- `QLocale::Ethiopia`：`77`
- `QLocale::EuropeanUnion (since Qt 5.7)`：`79`
- `QLocale::Europe (since Qt 5.12)`：`78`
- `QLocale::FalklandIslands`：`80`
- `QLocale::FaroeIslands`：`81`
- `QLocale::Fiji`：`82`
- `QLocale::Finland`：`83`
- `QLocale::France`：`84`
- `QLocale::FrenchGuiana`：`85`
- `QLocale::FrenchPolynesia`：`86`
- `QLocale::FrenchSouthernTerritories`：`87`
- `QLocale::Gabon`：`88`
- `QLocale::Gambia`：`89`
- `QLocale::Georgia`：`90`
- `QLocale::Germany`：`91`
- `QLocale::Ghana`：`92`
- `QLocale::Gibraltar`：`93`
- `QLocale::Greece`：`94`
- `QLocale::Greenland`：`95`
- `QLocale::Grenada`：`96`
- `QLocale::Guadeloupe`：`97`
- `QLocale::Guam`：`98`
- `QLocale::Guatemala`：`99`
- `QLocale::Guernsey`：`100`
- `QLocale::Guinea`：`102`
- `QLocale::GuineaBissau`：`101`
- `QLocale::Guyana`：`103`
- `QLocale::Haiti`：`104`
- `QLocale::HeardAndMcDonaldIslands`：`105`
- `QLocale::Honduras`：`106`
- `QLocale::HongKong`：`107`
- `QLocale::Hungary`：`108`
- `QLocale::Iceland`：`109`
- `QLocale::India`：`110`
- `QLocale::Indonesia`：`111`
- `QLocale::Iran`：`112`
- `QLocale::Iraq`：`113`
- `QLocale::Ireland`：`114`
- `QLocale::IsleOfMan`：`115`
- `QLocale::Israel`：`116`
- `QLocale::Italy`：`117`
- `QLocale::IvoryCoast`：`118`
- `QLocale::Jamaica`：`119`
- `QLocale::Japan`：`120`
- `QLocale::Jersey`：`121`
- `QLocale::Jordan`：`122`
- `QLocale::Kazakhstan`：`123`
- `QLocale::Kenya`：`124`
- `QLocale::Kiribati`：`125`
- `QLocale::Kosovo (since Qt 5.2)`：`126`
- `QLocale::Kuwait`：`127`
- `QLocale::Kyrgyzstan`：`128`
- `QLocale::Laos`：`129`
- `QLocale::LatinAmerica`：`130`
- `QLocale::LatinAmericaAndTheCaribbean`：`LatinAmerica`;已过时，改用`LatinAmerica`
- `QLocale::Latvia`：`131`
- `QLocale::Lebanon`：`132`
- `QLocale::Lesotho`：`133`
- `QLocale::Liberia`：`134`
- `QLocale::Libya`：`135`
- `QLocale::Liechtenstein`：`136`
- `QLocale::Lithuania`：`137`
- `QLocale::Luxembourg`：`138`
- `QLocale::Macao`：`139`
- `QLocale::Macau`：`Macao`
- `QLocale::Macedonia`：`140`
- `QLocale::Madagascar`：`141`
- `QLocale::Malawi`：`142`
- `QLocale::Malaysia`：`143`
- `QLocale::Maldives`：`144`
- `QLocale::Mali`：`145`
- `QLocale::Malta`：`146`
- `QLocale::MarshallIslands`：`147`
- `QLocale::Martinique`：`148`
- `QLocale::Mauritania`：`149`
- `QLocale::Mauritius`：`150`
- `QLocale::Mayotte`：`151`
- `QLocale::Mexico`：`152`
- `QLocale::Micronesia`：`153`
- `QLocale::Moldova`：`154`
- `QLocale::Monaco`：`155`
- `QLocale::Mongolia`：`156`
- `QLocale::Montenegro`：`157`
- `QLocale::Montserrat`：`158`
- `QLocale::Morocco`：`159`
- `QLocale::Mozambique`：`160`
- `QLocale::Myanmar`：`161`
- `QLocale::Namibia`：`162`
- `QLocale::NauruCountry`：`NauruTerritory`;Osbolete对`NauruTerritory`的别名
- `QLocale::NauruTerritory (since Qt 6.2)`：`163`
- `QLocale::Nepal`：`164`
- `QLocale::Netherlands`：`165`
- `QLocale::NewCaledonia`：`166`
- `QLocale::NewZealand`：`167`
- `QLocale::Nicaragua`：`168`
- `QLocale::Niger`：`170`
- `QLocale::Nigeria`：`169`
- `QLocale::Niue`：`171`
- `QLocale::NorfolkIsland`：`172`
- `QLocale::NorthernMarianaIslands`：`173`
- `QLocale::NorthKorea`：`174`
- `QLocale::Norway`：`175`
- `QLocale::Oman`：`176`
- `QLocale::OutlyingOceania (since Qt 5.7)`：`177`
- `QLocale::Pakistan`：`178`
- `QLocale::Palau`：`179`
- `QLocale::PalestinianTerritories`：`180`
- `QLocale::Panama`：`181`
- `QLocale::PapuaNewGuinea`：`182`
- `QLocale::Paraguay`：`183`
- `QLocale::PeoplesRepublicOfCongo`：`CongoBrazzaville`;过时，改用`CongoBrazzaville`
- `QLocale::Peru`：`184`
- `QLocale::Philippines`：`185`
- `QLocale::Pitcairn`：`186`
- `QLocale::Poland`：`187`
- `QLocale::Portugal`：`188`
- `QLocale::PuertoRico`：`189`
- `QLocale::Qatar`：`190`
- `QLocale::RepublicOfKorea`：`SouthKorea`;已过时，改用`SouthKorea`
- `QLocale::Reunion`：`191`
- `QLocale::Romania`：`192`
- `QLocale::RussianFederation`：`Russia`
- `QLocale::Russia`：`193`
- `QLocale::Rwanda`：`194`
- `QLocale::SaintBarthelemy`：`195`
- `QLocale::SaintHelena`：`196`
- `QLocale::SaintKittsAndNevis`：`197`
- `QLocale::SaintLucia`：`198`
- `QLocale::SaintMartin`：`199`
- `QLocale::SaintPierreAndMiquelon`：`200`
- `QLocale::SaintVincentAndGrenadines`：`201`
- `QLocale::SaintVincentAndTheGrenadines`：`SaintVincentAndGrenadines`
- `QLocale::Samoa`：`202`
- `QLocale::SanMarino`：`203`
- `QLocale::SaoTomeAndPrincipe`：`204`
- `QLocale::SaudiArabia`：`205`
- `QLocale::Senegal`：`206`
- `QLocale::Serbia`：`207`
- `QLocale::Seychelles`：`208`
- `QLocale::SierraLeone`：`209`
- `QLocale::Singapore`：`210`
- `QLocale::SintMaarten`：`211`
- `QLocale::Slovakia`：`212`
- `QLocale::Slovenia`：`213`
- `QLocale::SolomonIslands`：`214`
- `QLocale::Somalia`：`215`
- `QLocale::SouthAfrica`：`216`
- `QLocale::SouthGeorgiaAndSouthSandwichIslands`：`217`
- `QLocale::SouthGeorgiaAndTheSouthSandwichIslands`：`SouthGeorgiaAndSouthSandwichIslands`
- `QLocale::SouthKorea`：`218`
- `QLocale::SouthSudan`：`219`
- `QLocale::Spain`：`220`
- `QLocale::SriLanka`：`221`
- `QLocale::Sudan`：`222`
- `QLocale::Suriname`：`223`
- `QLocale::SvalbardAndJanMayen`：`224`
- `QLocale::SvalbardAndJanMayenIslands`：`SvalbardAndJanMayen`
- `QLocale::Swaziland`：`Eswatini`
- `QLocale::Sweden`：`225`
- `QLocale::Switzerland`：`226`
- `QLocale::Syria`：`227`
- `QLocale::SyrianArabRepublic`：`Syria`;已过时，改用`Syria`
- `QLocale::Taiwan`：`228`
- `QLocale::Tajikistan`：`229`
- `QLocale::Tanzania`：`230`
- `QLocale::Thailand`：`231`
- `QLocale::TimorLeste`：`232`
- `QLocale::Togo`：`233`
- `QLocale::TokelauCountry`：`TokelauTerritory`;Osbolete的别名`TokelauTerritory`
- `QLocale::TokelauTerritory (since Qt 6.2)`：`234`
- `QLocale::Tonga`：`235`
- `QLocale::TrinidadAndTobago`：`236`
- `QLocale::TristanDaCunha`：`237`
- `QLocale::Tunisia`：`238`
- `QLocale::Turkey`：`239`
- `QLocale::Turkmenistan`：`240`
- `QLocale::TurksAndCaicosIslands`：`241`
- `QLocale::TuvaluCountry`：`TuvaluTerritory`;Osbolete，`TuvaluTerritory`
- `QLocale::TuvaluTerritory (since Qt 6.2)`：`242`
- `QLocale::Uganda`：`243`
- `QLocale::Ukraine`：`244`
- `QLocale::UnitedArabEmirates`：`245`
- `QLocale::UnitedKingdom`：`246`
- `QLocale::UnitedStates`：`248`
- `QLocale::UnitedStatesOutlyingIslands`：`247`
- `QLocale::UnitedStatesMinorOutlyingIslands`：`UnitedStatesOutlyingIslands`
- `QLocale::UnitedStatesVirginIslands`：`249`
- `QLocale::Uruguay`：`250`
- `QLocale::Uzbekistan`：`251`
- `QLocale::Vanuatu`：`252`
- `QLocale::VaticanCity`：`253`
- `QLocale::VaticanCityState`：`VaticanCity`
- `QLocale::Venezuela`：`254`
- `QLocale::Vietnam`：`255`
- `QLocale::WallisAndFutuna`：`256`
- `QLocale::WallisAndFutunaIslands`：`WallisAndFutuna`
- `QLocale::WesternSahara`：`257`
- `QLocale::World (since Qt 5.12)`：`258`
- `QLocale::Yemen`：`259`
- `QLocale::Zambia`：`260`
- `QLocale::Zimbabwe`：`261`;注意：在此枚举中尽可能使用领地别名。国家枚举将在后续发布时更名为领地。

### `enum QLocale::CurrencySymbolFormat`

**作用与语义：**

指定货币符号的格式。
- `QLocale::CurrencyIsoCode`：`0`;一种ISO-4217货币代码。
- `QLocale::CurrencySymbol`：`1`;一种货币符号。
- `QLocale::CurrencyDisplayName`：`2`;一个用户可读的货币名称。

### `enum QLocale::DataSizeFormatflags QLocale::DataSizeFormats`

**作用与语义：**

规定数据量的表示格式。
- `QLocale::DataSizeIecFormat`：`0`;采用1024基础和IEC前缀的格式：KiB、MiB、GiB、......
- `QLocale::DataSizeTraditionalFormat`：`DataSizeSIQuantifiers`;采用1024进制和国际单位制前缀格式：kB、MB、GB、...
- `QLocale::DataSizeSIFormat`：`DataSizeBase1000 | DataSizeSIQuantifiers`;格式采用1000进制和国际单位制前缀：kB、MB、GB、...
DataSizeFormats 类型是 QFlags 的 typedef<DataSizeFormat>。它存储 DataSizeFormat 值的 OR 组合。

### `enum QLocale::FloatingPointPrecisionOption`

**作用与语义：**

该枚举定义了一个常数，可以作为`QString::number()`、`QByteArray::number()`和`QLocale::toString()`的精度表示，在转换浮点或双数时，以表示可变数字的精度。
- `QLocale::FloatingPointShortest`：`-128`;转换算法会尝试为给定数字寻找最短且准确的表示。“准确”意味着你通过对生成字符串表示进行逆转换得到的数字完全相同。特别是，尾数零被省略（在指数格式中）。

### `enum QLocale::FormatType`

**作用与语义：**

该枚举描述了将`QDate`、`QTime`、`QDateTime`对象，以及月份和天转换为特定位置字符串时可以使用的不同格式。
- `QLocale::LongFormat`：`0`;格式更长。
- `QLocale::ShortFormat`：`1`;简短格式。
- `QLocale::NarrowFormat`：`2`;空间极度有限时使用的特殊版本。
注意：`NarrowFormat`可能包含不同月份和日期的相同文本。如果地方不支持狭窄名称，它甚至可能是空字符串，因此应避免用它来进行日期格式化。此外，系统区域的格式与`ShortFormat`相同。

### `enum QLocale::Language`

**作用与语义：**

这个枚举类型用于指定语言。
- `QLocale::AnyLanguage`：`0`
- `QLocale::C`：`1`;简化的英语地名;参见 `QLocale::c()`
- `QLocale::Abkhazian`：`2`
- `QLocale::Afan`：`Oromo`;已过时，请使用奥罗莫语
- `QLocale::Afar`：`3`
- `QLocale::Afrikaans`：`4`
- `QLocale::Aghem`：`5`
- `QLocale::Akan`：`6`
- `QLocale::Akkadian (since Qt 5.1)`：`7`
- `QLocale::Akoose (since Qt 5.3)`：`8`
- `QLocale::Albanian`：`9`
- `QLocale::AmericanSignLanguage (since Qt 5.7)`：`10`
- `QLocale::Amharic`：`11`
- `QLocale::AncientEgyptian (since Qt 5.1)`：`12`
- `QLocale::AncientGreek (since Qt 5.1)`：`13`
- `QLocale::Anii (since Qt 6.7)`：`341`
- `QLocale::Arabic`：`14`
- `QLocale::Aragonese (since Qt 5.1)`：`15`
- `QLocale::Aramaic (since Qt 5.1)`：`16`
- `QLocale::Armenian`：`17`
- `QLocale::Assamese`：`18`
- `QLocale::Asturian`：`19`
- `QLocale::Asu`：`20`
- `QLocale::Atsam`：`21`
- `QLocale::Avaric`：`22`
- `QLocale::Avestan`：`23`
- `QLocale::Aymara`：`24`
- `QLocale::Azerbaijani`：`25`
- `QLocale::Bafia`：`26`
- `QLocale::Balinese (since Qt 5.1)`：`27`
- `QLocale::Baluchi (since Qt 6.6)`：`337`
- `QLocale::Bambara`：`28`
- `QLocale::Bamun (since Qt 5.1)`：`29`
- `QLocale::Bangla (since Qt 6.0)`：`30`
- `QLocale::Basaa`：`31`
- `QLocale::Bashkir`：`32`
- `QLocale::Basque`：`33`
- `QLocale::BatakToba (since Qt 5.1)`：`34`
- `QLocale::Belarusian`：`35`
- `QLocale::Bemba`：`36`
- `QLocale::Bena`：`37`
- `QLocale::Bengali`：`Bangla`;已过时，请使用孟加拉语
- `QLocale::Bhojpuri (since Qt 5.7)`：`38`
- `QLocale::Bhutani`：`Dzongkha`;已过时，请使用宗卡语
- `QLocale::Bislama`：`39`
- `QLocale::Blin`：`40`
- `QLocale::Bodo`：`41`
- `QLocale::Bosnian`：`42`
- `QLocale::Breton`：`43`
- `QLocale::Buginese (since Qt 5.1)`：`44`
- `QLocale::Bulgarian`：`45`
- `QLocale::Burmese`：`46`
- `QLocale::Byelorussian`：`Belarusian`;已过时，请使用白俄罗斯语
- `QLocale::Cambodian`：`Khmer`;已过时，请使用高棉语
- `QLocale::Cantonese (since Qt 5.7)`：`47`
- `QLocale::Catalan`：`48`
- `QLocale::Cebuano (since Qt 5.14)`：`49`
- `QLocale::CentralAtlasTamazight (since Qt 6.0)`：`50`
- `QLocale::CentralKurdish (since Qt 5.5)`：`51`
- `QLocale::CentralMoroccoTamazight`：`CentralAtlasTamazight`;已过时，请使用CentralAtlasTamazight
- `QLocale::Chakma (since Qt 5.1)`：`52`
- `QLocale::Chamorro`：`53`
- `QLocale::Chechen`：`54`
- `QLocale::Cherokee`：`55`
- `QLocale::Chewa`：`Nyanja`;已过时，请使用 Nyanja
- `QLocale::Chickasaw (since Qt 5.14)`：`56`
- `QLocale::Chiga`：`57`
- `QLocale::Chinese`：`58`;（普通话）
- `QLocale::Church`：`59`
- `QLocale::Chuvash`：`60`
- `QLocale::Colognian`：`61`
- `QLocale::Coptic (since Qt 5.1)`：`62`
- `QLocale::Cornish`：`63`
- `QLocale::Corsican`：`64`
- `QLocale::Cree`：`65`
- `QLocale::Croatian`：`66`
- `QLocale::Czech`：`67`
- `QLocale::Danish`：`68`
- `QLocale::Divehi`：`69`
- `QLocale::Dogri (since Qt 5.1)`：`70`
- `QLocale::Duala`：`71`
- `QLocale::Dutch`：`72`
- `QLocale::Dzongkha`：`73`
- `QLocale::Embu`：`74`
- `QLocale::English`：`75`
- `QLocale::Erzya (since Qt 5.14)`：`76`
- `QLocale::Esperanto`：`77`
- `QLocale::Estonian`：`78`
- `QLocale::Ewe`：`79`
- `QLocale::Ewondo`：`80`
- `QLocale::Faroese`：`81`
- `QLocale::Fijian`：`82`
- `QLocale::Filipino`：`83`
- `QLocale::Finnish`：`84`
- `QLocale::French`：`85`
- `QLocale::Frisian`：`WesternFrisian`;与西弗里斯兰语相同
- `QLocale::Friulian`：`86`
- `QLocale::Fulah`：`87`
- `QLocale::Ga`：`89`
- `QLocale::Gaelic`：`88`
- `QLocale::Galician`：`90`
- `QLocale::Ganda`：`91`
- `QLocale::Geez`：`92`
- `QLocale::Georgian`：`93`
- `QLocale::German`：`94`
- `QLocale::Gothic (since Qt 5.1)`：`95`
- `QLocale::Greek`：`96`
- `QLocale::Greenlandic`：`Kalaallisut`;已过时，请使用 Kalaallisut
- `QLocale::Guarani`：`97`
- `QLocale::Gujarati`：`98`
- `QLocale::Gusii`：`99`
- `QLocale::Haitian`：`100`
- `QLocale::Haryanvi (since Qt 6.5)`：`330`
- `QLocale::Hausa`：`101`
- `QLocale::Hawaiian`：`102`
- `QLocale::Hebrew`：`103`
- `QLocale::Herero`：`104`
- `QLocale::Hindi`：`105`
- `QLocale::HiriMotu`：`106`
- `QLocale::Hungarian`：`107`
- `QLocale::Icelandic`：`108`
- `QLocale::Ido (since Qt 5.12)`：`109`
- `QLocale::Igbo`：`110`
- `QLocale::InariSami (since Qt 5.5)`：`111`
- `QLocale::Indonesian`：`112`
- `QLocale::Ingush (since Qt 5.1)`：`113`
- `QLocale::Interlingua`：`114`
- `QLocale::Interlingue`：`115`
- `QLocale::Inuktitut`：`116`
- `QLocale::Inupiak`：`Inupiaq`;已过时，请使用伊努皮亚克语
- `QLocale::Inupiaq (since Qt 6.0)`：`117`
- `QLocale::Irish`：`118`
- `QLocale::Italian`：`119`
- `QLocale::Japanese`：`120`
- `QLocale::Javanese`：`121`
- `QLocale::Jju`：`122`
- `QLocale::JolaFonyi`：`123`
- `QLocale::Kabuverdianu`：`124`
- `QLocale::Kabyle`：`125`
- `QLocale::Kaingang (since Qt 6.3)`：`328`
- `QLocale::Kako`：`126`
- `QLocale::Kalaallisut (since Qt 6.0)`：`127`
- `QLocale::Kalenjin`：`128`
- `QLocale::Kamba`：`129`
- `QLocale::Kangri (since Qt 6.7)`：`342`
- `QLocale::Kannada`：`130`
- `QLocale::Kanuri`：`131`
- `QLocale::KaraKalpak (since Qt 6.9)`：`345`
- `QLocale::Kashmiri`：`132`
- `QLocale::Kazakh`：`133`
- `QLocale::Kenyang (since Qt 5.5)`：`134`
- `QLocale::Khmer`：`135`
- `QLocale::Kiche (since Qt 5.5)`：`136`
- `QLocale::Kikuyu`：`137`
- `QLocale::Kinyarwanda`：`138`
- `QLocale::Kirghiz`：`Kyrgyz`;已过时，请使用吉尔吉斯语
- `QLocale::Komi`：`139`
- `QLocale::Kongo`：`140`
- `QLocale::Konkani`：`141`
- `QLocale::Korean`：`142`
- `QLocale::Koro`：`143`
- `QLocale::KoyraboroSenni`：`144`
- `QLocale::KoyraChiini`：`145`
- `QLocale::Kpelle`：`146`
- `QLocale::Kuanyama (since Qt 6.0)`：`147`
- `QLocale::Kurdish`：`148`
- `QLocale::Kurundi`：`Rundi`;已过时，请使用伦迪语
- `QLocale::Kuvi (since Qt 6.8)`：`344`
- `QLocale::Kwanyama`：`Kuanyama`;已过时，请使用宽山
- `QLocale::Kwasio`：`149`
- `QLocale::Kyrgyz (since Qt 6.0)`：`150`
- `QLocale::Ladin (since Qt 6.11)`：`347`
- `QLocale::Lakota (since Qt 5.3)`：`151`
- `QLocale::Langi`：`152`
- `QLocale::Lao`：`153`
- `QLocale::Latin`：`154`
- `QLocale::Latvian`：`155`
- `QLocale::Lezghian (since Qt 5.5)`：`156`
- `QLocale::Limburgish`：`157`
- `QLocale::Lingala`：`158`
- `QLocale::Ligurian (since Qt 6.6)`：`338`
- `QLocale::LiteraryChinese (since Qt 5.7)`：`159`
- `QLocale::Lithuanian`：`160`
- `QLocale::Lojban (since Qt 5.12)`：`161`
- `QLocale::LowerSorbian (since Qt 5.5)`：`162`
- `QLocale::LowGerman`：`163`
- `QLocale::LubaKatanga`：`164`
- `QLocale::LuleSami (since Qt 5.5)`：`165`
- `QLocale::Luo`：`166`
- `QLocale::Luxembourgish`：`167`
- `QLocale::Luyia`：`168`
- `QLocale::Macedonian`：`169`
- `QLocale::Machame`：`170`
- `QLocale::Maithili (since Qt 5.5)`：`171`
- `QLocale::MakhuwaMeetto`：`172`
- `QLocale::Makonde`：`173`
- `QLocale::Malagasy`：`174`
- `QLocale::Malay`：`176`
- `QLocale::Malayalam`：`175`
- `QLocale::Maltese`：`177`
- `QLocale::Mandingo (since Qt 5.1)`：`178`
- `QLocale::Manipuri (since Qt 5.1)`：`179`
- `QLocale::Manx`：`180`
- `QLocale::Maori`：`181`
- `QLocale::Mapuche (since Qt 5.5)`：`182`
- `QLocale::Marathi`：`183`
- `QLocale::Marshallese`：`184`
- `QLocale::Masai`：`185`
- `QLocale::Mazanderani (since Qt 5.7)`：`186`
- `QLocale::Mende (since Qt 5.5)`：`187`
- `QLocale::Meru`：`188`
- `QLocale::Meta`：`189`
- `QLocale::Mohawk (since Qt 5.5)`：`190`
- `QLocale::Moksha (since Qt 6.5)`：`333`
- `QLocale::Mongolian`：`191`
- `QLocale::Morisyen`：`192`
- `QLocale::Mundang`：`193`
- `QLocale::Muscogee (since Qt 5.14)`：`194`
- `QLocale::Nama`：`195`
- `QLocale::NauruLanguage`：`196`
- `QLocale::Navaho`：`Navajo`;已过时，请使用纳瓦霍语
- `QLocale::Navajo (since Qt 6.0)`：`197`
- `QLocale::Ndonga`：`198`
- `QLocale::Nepali`：`199`
- `QLocale::Newari (since Qt 5.7)`：`200`
- `QLocale::Ngiemboon`：`201`
- `QLocale::Nheengatu (since Qt 6.3)`：`329`
- `QLocale::NigerianPidgin (since Qt 6.0)`：`203`
- `QLocale::Ngomba`：`202`
- `QLocale::Nko (since Qt 5.5)`：`204`
- `QLocale::NorthernFrisian (since Qt 6.5)`：`331`
- `QLocale::NorthernLuri (since Qt 5.7)`：`205`
- `QLocale::NorthernSami`：`206`
- `QLocale::NorthernSotho`：`207`
- `QLocale::NorthNdebele`：`208`
- `QLocale::NorwegianBokmal`：`209`
- `QLocale::NorwegianNynorsk`：`210`
- `QLocale::Nuer`：`211`
- `QLocale::Nyanja`：`212`
- `QLocale::Nyankole`：`213`
- `QLocale::Obolo (since Qt 6.5)`：`336`
- `QLocale::Occitan`：`214`
- `QLocale::Odia (since Qt 6.0)`：`215`
- `QLocale::Ojibwa`：`216`
- `QLocale::OldIrish (since Qt 5.1)`：`217`
- `QLocale::OldNorse (since Qt 5.1)`：`218`
- `QLocale::OldPersian (since Qt 5.1)`：`219`
- `QLocale::Oriya`：`Odia`;已过时，请使用奥里亚语
- `QLocale::Oromo`：`220`
- `QLocale::Osage (since Qt 5.7)`：`221`
- `QLocale::Ossetic`：`222`
- `QLocale::Pahlavi (since Qt 5.1)`：`223`
- `QLocale::Palauan (since Qt 5.7)`：`224`
- `QLocale::Pali`：`225`
- `QLocale::Papiamento (since Qt 5.7)`：`226`
- `QLocale::Pashto`：`227`
- `QLocale::Persian`：`228`
- `QLocale::Phoenician (since Qt 5.1)`：`229`
- `QLocale::Pijin (since Qt 6.5)`：`335`
- `QLocale::Polish`：`230`
- `QLocale::Portuguese`：`231`
- `QLocale::Prussian (since Qt 5.5)`：`232`
- `QLocale::Punjabi`：`233`
- `QLocale::Quechua`：`234`
- `QLocale::Rajasthani (since Qt 6.5)`：`332`
- `QLocale::RhaetoRomance`：`Romansh`;已过时，请使用罗曼什语
- `QLocale::Rohingya (since Qt 6.6)`：`339`
- `QLocale::Romanian`：`235`
- `QLocale::Romansh`：`236`
- `QLocale::Rombo`：`237`
- `QLocale::Rundi`：`238`
- `QLocale::Russian`：`239`
- `QLocale::Rwa`：`240`
- `QLocale::Saho`：`241`
- `QLocale::Sakha`：`242`
- `QLocale::Samburu`：`243`
- `QLocale::Samoan`：`244`
- `QLocale::Sango`：`245`
- `QLocale::Sangu`：`246`
- `QLocale::Sanskrit`：`247`
- `QLocale::Santali (since Qt 5.1)`：`248`
- `QLocale::Sardinian`：`249`
- `QLocale::Saurashtra (since Qt 5.1)`：`250`
- `QLocale::Sena`：`251`
- `QLocale::Serbian`：`252`
- `QLocale::Shambala`：`253`
- `QLocale::Shan (since Qt 6.11)`：`348`
- `QLocale::Shona`：`254`
- `QLocale::SichuanYi`：`255`
- `QLocale::Sicilian (since Qt 5.12)`：`256`
- `QLocale::Sidamo`：`257`
- `QLocale::Silesian (since Qt 5.14)`：`258`
- `QLocale::Sindhi`：`259`
- `QLocale::Sinhala`：`260`
- `QLocale::SkoltSami (since Qt 5.5)`：`261`
- `QLocale::Slovak`：`262`
- `QLocale::Slovenian`：`263`
- `QLocale::Soga`：`264`
- `QLocale::Somali`：`265`
- `QLocale::SouthernKurdish (since Qt 5.12)`：`266`
- `QLocale::SouthernSami (since Qt 5.5)`：`267`
- `QLocale::SouthernSotho`：`268`
- `QLocale::SouthNdebele`：`269`
- `QLocale::Spanish`：`270`
- `QLocale::StandardMoroccanTamazight (since Qt 5.3)`：`271`
- `QLocale::Sundanese`：`272`
- `QLocale::Swahili`：`273`
- `QLocale::SwampyCree (since Qt 6.9)`：`346`
- `QLocale::Swati`：`274`
- `QLocale::Swedish`：`275`
- `QLocale::SwissGerman`：`276`
- `QLocale::Syriac`：`277`
- `QLocale::Tachelhit`：`278`
- `QLocale::Tahitian`：`279`
- `QLocale::TaiDam (since Qt 5.1)`：`280`
- `QLocale::Taita`：`281`
- `QLocale::Tajik`：`282`
- `QLocale::Tamil`：`283`
- `QLocale::Taroko`：`284`
- `QLocale::Tasawaq`：`285`
- `QLocale::Tatar`：`286`
- `QLocale::Telugu`：`287`
- `QLocale::Teso`：`288`
- `QLocale::Thai`：`289`
- `QLocale::Tibetan`：`290`
- `QLocale::Tigre`：`291`
- `QLocale::Tigrinya`：`292`
- `QLocale::TokelauLanguage (since Qt 5.7)`：`293`
- `QLocale::TokiPona (since Qt 6.5)`：`334`
- `QLocale::TokPisin (since Qt 5.7)`：`294`
- `QLocale::Tongan`：`295`
- `QLocale::Torwali (since Qt 6.6)`：`340`
- `QLocale::Tsonga`：`296`
- `QLocale::Tswana`：`297`
- `QLocale::Turkish`：`298`
- `QLocale::Turkmen`：`299`
- `QLocale::TuvaluLanguage (since Qt 5.7)`：`300`
- `QLocale::Tyap`：`301`
- `QLocale::Ugaritic (since Qt 5.1)`：`302`
- `QLocale::Uighur`：`Uyghur`;已过时，请使用维吾尔语
- `QLocale::Uigur`：`Uyghur`;已过时，请使用维吾尔语
- `QLocale::Ukrainian`：`303`
- `QLocale::UpperSorbian (since Qt 5.5)`：`304`
- `QLocale::Urdu`：`305`
- `QLocale::Uyghur (since Qt 6.0)`：`306`
- `QLocale::Uzbek`：`307`
- `QLocale::Vai`：`308`
- `QLocale::Venda`：`309`
- `QLocale::Venetian (since Qt 6.7)`：`343`
- `QLocale::Vietnamese`：`310`
- `QLocale::Volapuk`：`311`
- `QLocale::Vunjo`：`312`
- `QLocale::Walamo`：`Wolaytta`;已过时，请使用Wolaytta语
- `QLocale::Walloon`：`313`
- `QLocale::Walser`：`314`
- `QLocale::Warlpiri (since Qt 5.5)`：`315`
- `QLocale::Welsh`：`316`
- `QLocale::WesternBalochi (since Qt 5.12)`：`317`
- `QLocale::WesternFrisian`：`318`;与弗里斯兰语相同
- `QLocale::Wolaytta (since Qt 6.0)`：`319`
- `QLocale::Wolof`：`320`
- `QLocale::Xhosa`：`321`
- `QLocale::Yangben`：`322`
- `QLocale::Yiddish`：`323`
- `QLocale::Yoruba`：`324`
- `QLocale::Zarma`：`325`
- `QLocale::Zhuang`：`326`
- `QLocale::Zulu`：`327`

### `enum QLocale::LanguageCodeTypeflags QLocale::LanguageCodeTypes`

**作用与语义：**

该枚举定义了可以用于限制 `codeToLanguage` 和 `languageToCode` 所考虑的语言代码集合的语言代码类型。
- `QLocale::ISO639Part1`: `1 << 0`；ISO 639 第一部分 Alpha 2 代码。
- `QLocale::ISO639Part2B`: `1 << 1`；ISO 639 第二部分文献用 Alpha 3 代码。
- `QLocale::ISO639Part2T`: `1 << 2`；ISO 639 第二部分术语用 Alpha 3 代码。
- `QLocale::ISO639Part3`: `1 << 3`；ISO 639 第三部分 Alpha 3 代码。
- `QLocale::LegacyLanguageCode`: `1 << 15`；不属于上述集合的代码，但过去由 Qt 支持。此值只能由 `codeToLanguage()` 使用。传递给 `languageToCode()` 时将被忽略。
- `QLocale::ISO639Part2`: `ISO639Part2B | ISO639Part2T`；任何 ISO 639 第二部分代码。
- `QLocale::ISO639Alpha2`: `ISO639Part1`；任何 ISO-639 2 字母代码。
- `QLocale::ISO639Alpha3`: `ISO639Part2 | ISO639Part3`；任何 ISO-639 3 字母代码。
- `QLocale::ISO639`: `ISO639Alpha2 | ISO639Alpha3`；任何 ISO 639 代码。
- `QLocale::AnyLanguageCode`: `-1`；指定可以使用任何代码。
LanguageCodeTypes 类型是 QFlags<LanguageCodeType> 的类型定义。它存储 LanguageCodeType 值的 OR 组合。

### `enum QLocale::MeasurementSystem`

**作用与语义：**

该枚举定义了用于测量的单位。
- `QLocale::MetricSystem`：`0`;该值表示基于国际单位制的公制单位，如米、厘米和毫米。
- `QLocale::ImperialUSSystem`：`1`;该数值表示英制单位，如英寸和英里，这些单位在美国使用。
- `QLocale::ImperialUKSystem`：`2`;该数值表示英制单位，如英格兰使用的英寸和英里。
- `QLocale::ImperialSystem`：`ImperialUSSystem`;提供兼容性。与ImperialUSSystem相同

### `enum QLocale::NumberOptionflags QLocale::NumberOptions`

**作用与语义：**

该枚举定义了一组用于数字到字符串和字符串到数字转换的选项。它们可以用`numberOptions()`检索，也可以用`setNumberOptions()`设置。
- `QLocale::DefaultNumberOptions`：`0x0`;该选项代表除C区域外所有区域的默认行为，带有群分隔符，前方一个零位于个位数指数中，且在分数部分末尾无尾随零（存在时）。
- `QLocale::OmitGroupSeparator`：`0x01`;如果设置了这个选项，数字到字符串的函数不会将数字拆分成组。C locale 默认设置了这个选项。其他所有区域的默认是将数字拆分成组，在数字的整数部分，并使用组分隔符。
- `QLocale::RejectGroupSeparator`：`0x02`;如果设置了这个选项，字符串转数字函数如果在输入中遇到群分隔符，就会失败。默认情况下，接受包含正确放置的群分隔符的数字。
- `QLocale::OmitLeadingZeroInExponent`：`0x04`;如果设置了该选项，数字转字符串函数在用科学记号法打印浮点数时不会用零填充指数。默认是将一个前置零加到个位数指数。
- `QLocale::RejectLeadingZeroInExponent`：`0x08`;如果设置了该选项，字符串转数字函数在科学记谱法解析浮点数时遇到带零的指数时将失败。默认情况下接受此类填充。
- `QLocale::IncludeTrailingZeroesAfterDot`：`0x10`;如果设置了这个选项，数字到字符串函数会在“g”或“最简洁”模式下，将带零的数字填充到所需的精度。默认情况下省略尾随的零，这可能导致分数部分留下的数字比要求的精度少。
- `QLocale::RejectTrailingZeroesAfterDot`：`0x20`;如果设置了这个选项，字符串转数字函数在解析科学或十进制表示时，如果在分数部分末尾遇到尾随零，就会失败。默认情况下接受尾随零。
NumberOptions 类型是 QFlag 的 typedef<NumberOption>。它存储 NumberOption 值的 OR 组合。

### `enum QLocale::QuotationStyle`

**作用与语义：**

该枚举定义了一组针对特定地区引用的可能风格。
- `QLocale::StandardQuotation`：`0`;如果设置了这个选项，标准引号将用于引用字符串。
- `QLocale::AlternateQuotation`：`1`;如果设置了这个选项，备用引号将用于引用字符串。

### `enum QLocale::Script`

**作用与语义：**

这种枚举类型用于指定脚本。
- `QLocale::AnyScript`：`0`
- `QLocale::AdlamScript (since Qt 5.7)`：`1`
- `QLocale::AhomScript (since Qt 5.7)`：`2`
- `QLocale::AnatolianHieroglyphsScript (since Qt 5.7)`：`3`
- `QLocale::ArabicScript`：`4`
- `QLocale::ArmenianScript`：`5`
- `QLocale::AvestanScript (since Qt 5.1)`：`6`
- `QLocale::BalineseScript (since Qt 5.1)`：`7`
- `QLocale::BamumScript (since Qt 5.1)`：`8`
- `QLocale::BanglaScript (since Qt 6.0)`：`9`
- `QLocale::BassaVahScript (since Qt 5.5)`：`10`
- `QLocale::BatakScript (since Qt 5.1)`：`11`
- `QLocale::BengaliScript`：`BanglaScript`;已过时，请使用孟加拉文字
- `QLocale::BhaiksukiScript (since Qt 5.7)`：`12`
- `QLocale::BopomofoScript (since Qt 5.1)`：`13`
- `QLocale::BrahmiScript (since Qt 5.1)`：`14`
- `QLocale::BrailleScript (since Qt 5.1)`：`15`
- `QLocale::BugineseScript (since Qt 5.1)`：`16`
- `QLocale::BuhidScript (since Qt 5.1)`：`17`
- `QLocale::CanadianAboriginalScript (since Qt 5.1)`：`18`
- `QLocale::CarianScript (since Qt 5.1)`：`19`
- `QLocale::CaucasianAlbanianScript (since Qt 5.5)`：`20`
- `QLocale::ChakmaScript (since Qt 5.1)`：`21`
- `QLocale::ChamScript (since Qt 5.1)`：`22`
- `QLocale::CherokeeScript`：`23`
- `QLocale::CopticScript (since Qt 5.1)`：`24`
- `QLocale::CuneiformScript (since Qt 5.1)`：`25`
- `QLocale::CypriotScript (since Qt 5.1)`：`26`
- `QLocale::CyrillicScript`：`27`
- `QLocale::DeseretScript (since Qt 5.1)`：`28`
- `QLocale::DevanagariScript`：`29`
- `QLocale::DuployanScript (since Qt 5.5)`：`30`
- `QLocale::EgyptianHieroglyphsScript (since Qt 5.1)`：`31`
- `QLocale::ElbasanScript (since Qt 5.5)`：`32`
- `QLocale::EthiopicScript`：`33`
- `QLocale::FraserScript (since Qt 5.1)`：`34`
- `QLocale::GeorgianScript`：`35`
- `QLocale::GlagoliticScript (since Qt 5.1)`：`36`
- `QLocale::GothicScript (since Qt 5.1)`：`37`
- `QLocale::GranthaScript (since Qt 5.5)`：`38`
- `QLocale::GreekScript`：`39`
- `QLocale::GujaratiScript`：`40`
- `QLocale::GurmukhiScript`：`41`
- `QLocale::HangulScript (since Qt 5.1)`：`42`
- `QLocale::HanifiScript (since Qt 6.6)`：`142`
- `QLocale::HanScript (since Qt 5.1)`：`43`
- `QLocale::HanunooScript (since Qt 5.1)`：`44`
- `QLocale::HanWithBopomofoScript (since Qt 5.7)`：`45`
- `QLocale::HatranScript (since Qt 5.7)`：`46`
- `QLocale::HebrewScript`：`47`
- `QLocale::HiraganaScript (since Qt 5.1)`：`48`
- `QLocale::ImperialAramaicScript (since Qt 5.1)`：`49`
- `QLocale::InscriptionalPahlaviScript (since Qt 5.1)`：`50`
- `QLocale::InscriptionalParthianScript (since Qt 5.1)`：`51`
- `QLocale::JamoScript (since Qt 5.7)`：`52`
- `QLocale::JapaneseScript`：`53`
- `QLocale::JavaneseScript (since Qt 5.1)`：`54`
- `QLocale::KaithiScript (since Qt 5.1)`：`55`
- `QLocale::KannadaScript`：`56`
- `QLocale::KatakanaScript (since Qt 5.1)`：`57`
- `QLocale::KayahLiScript (since Qt 5.1)`：`58`
- `QLocale::KharoshthiScript (since Qt 5.1)`：`59`
- `QLocale::KhmerScript (since Qt 5.1)`：`60`
- `QLocale::KhojkiScript (since Qt 5.5)`：`61`
- `QLocale::KhudawadiScript (since Qt 5.5)`：`62`
- `QLocale::KoreanScript`：`63`
- `QLocale::LannaScript (since Qt 5.1)`：`64`
- `QLocale::LaoScript`：`65`
- `QLocale::LatinScript`：`66`
- `QLocale::LepchaScript (since Qt 5.1)`：`67`
- `QLocale::LimbuScript (since Qt 5.1)`：`68`
- `QLocale::LinearAScript (since Qt 5.5)`：`69`
- `QLocale::LinearBScript (since Qt 5.1)`：`70`
- `QLocale::LycianScript (since Qt 5.1)`：`71`
- `QLocale::LydianScript (since Qt 5.1)`：`72`
- `QLocale::MahajaniScript (since Qt 5.5)`：`73`
- `QLocale::MalayalamScript`：`74`
- `QLocale::MandaeanScript (since Qt 5.1)`：`75`
- `QLocale::ManichaeanScript (since Qt 5.5)`：`76`
- `QLocale::MarchenScript (since Qt 5.7)`：`77`
- `QLocale::MeiteiMayekScript (since Qt 5.1)`：`78`
- `QLocale::MendeScript (since Qt 6.0)`：`79`
- `QLocale::MendeKikakuiScript`：`MendeScript`;已过时，请使用MendeScript
- `QLocale::MeroiticCursiveScript (since Qt 5.1)`：`80`
- `QLocale::MeroiticScript (since Qt 5.1)`：`81`
- `QLocale::ModiScript (since Qt 5.5)`：`82`
- `QLocale::MongolianScript`：`83`
- `QLocale::MroScript (since Qt 5.5)`：`84`
- `QLocale::MultaniScript (since Qt 5.7)`：`85`
- `QLocale::MyanmarScript`：`86`
- `QLocale::NabataeanScript (since Qt 5.5)`：`87`
- `QLocale::NewaScript (since Qt 5.7)`：`88`
- `QLocale::NewTaiLueScript (since Qt 5.1)`：`89`
- `QLocale::NkoScript (since Qt 5.1)`：`90`
- `QLocale::OghamScript (since Qt 5.1)`：`92`
- `QLocale::OlChikiScript (since Qt 5.1)`：`93`
- `QLocale::OldHungarianScript (since Qt 5.7)`：`94`
- `QLocale::OldItalicScript (since Qt 5.1)`：`95`
- `QLocale::OldNorthArabianScript (since Qt 5.5)`：`96`
- `QLocale::OldPermicScript (since Qt 5.5)`：`97`
- `QLocale::OldPersianScript (since Qt 5.1)`：`98`
- `QLocale::OldSouthArabianScript (since Qt 5.1)`：`99`
- `QLocale::OdiaScript (since Qt 6.0)`：`91`
- `QLocale::OriyaScript`：`OdiaScript`;已过时，请使用 OdiaScript
- `QLocale::OrkhonScript (since Qt 5.1)`：`100`
- `QLocale::OsageScript (since Qt 5.7)`：`101`
- `QLocale::OsmanyaScript (since Qt 5.1)`：`102`
- `QLocale::PahawhHmongScript (since Qt 5.5)`：`103`
- `QLocale::PalmyreneScript (since Qt 5.5)`：`104`
- `QLocale::PauCinHauScript (since Qt 5.5)`：`105`
- `QLocale::PhagsPaScript (since Qt 5.1)`：`106`
- `QLocale::PhoenicianScript (since Qt 5.1)`：`107`
- `QLocale::PollardPhoneticScript (since Qt 5.1)`：`108`
- `QLocale::PsalterPahlaviScript (since Qt 5.5)`：`109`
- `QLocale::RejangScript (since Qt 5.1)`：`110`
- `QLocale::RunicScript (since Qt 5.1)`：`111`
- `QLocale::SamaritanScript (since Qt 5.1)`：`112`
- `QLocale::SaurashtraScript (since Qt 5.1)`：`113`
- `QLocale::SharadaScript (since Qt 5.1)`：`114`
- `QLocale::ShavianScript (since Qt 5.1)`：`115`
- `QLocale::SiddhamScript (since Qt 5.5)`：`116`
- `QLocale::SignWritingScript (since Qt 5.7)`：`117`
- `QLocale::SimplifiedChineseScript`：`SimplifiedHanScript`;与简体汉字体相同
- `QLocale::SimplifiedHanScript`：`118`;与简体中文相同
- `QLocale::SinhalaScript`：`119`
- `QLocale::SoraSompengScript (since Qt 5.1)`：`120`
- `QLocale::SundaneseScript (since Qt 5.1)`：`121`
- `QLocale::SylotiNagriScript (since Qt 5.1)`：`122`
- `QLocale::SyriacScript`：`123`
- `QLocale::TagalogScript (since Qt 5.1)`：`124`
- `QLocale::TagbanwaScript (since Qt 5.1)`：`125`
- `QLocale::TaiLeScript (since Qt 5.1)`：`126`
- `QLocale::TaiVietScript (since Qt 5.1)`：`127`
- `QLocale::TakriScript (since Qt 5.1)`：`128`
- `QLocale::TamilScript`：`129`
- `QLocale::TangutScript (since Qt 5.7)`：`130`
- `QLocale::TeluguScript`：`131`
- `QLocale::ThaanaScript`：`132`
- `QLocale::ThaiScript`：`133`
- `QLocale::TibetanScript`：`134`
- `QLocale::TifinaghScript`：`135`
- `QLocale::TirhutaScript (since Qt 5.5)`：`136`
- `QLocale::TraditionalChineseScript`：`TraditionalHanScript`;与传统汉字体相同
- `QLocale::TraditionalHanScript`：`137`;与繁体中文书写相同
- `QLocale::UgariticScript (since Qt 5.1)`：`138`
- `QLocale::VaiScript`：`139`
- `QLocale::VarangKshitiScript (since Qt 5.5)`：`140`
- `QLocale::YiScript`：`141`

### `[since 6.7] enum class QLocale::TagSeparator`

**作用与语义：**

说明如何组合构成地区标识符的各个部分。
一个地方标识符可能由多个标签组成，表示语言、文字和地区（可能还包括其他细节），这些标签组合起来形成标识符。各种标准和传统形式使用破折号（Unicode HYPHEN-MINUS，U 002D）或下划线（LOW LINE，U 005F）。不同`QLocale`客户端可能需要其中之一。
- `QLocale::TagSeparator::Dash`：`'-'`;使用`'-'`，即破折号或连字符。
- `QLocale::TagSeparator::Underscore`：`'_'`;使用`'_'`，即下划线字符。
注意：虽然在公共标准中（截至2023年）中，只有破折号和下划线使用分隔符，但如果需要非标准ASCII分隔符，也可以将任意ASCII字符铸造为此类。不支持铸造非ASCII字符（小数值大于127）：此类值保留用于未来作为枚举成员，以防某些公共标准使用非ASCII分隔符。当然，也可以用`QString::replace()`替换取该类型参数的函数所用分隔符，使用任意的Unicode字符或字符串。
该枚举于Qt 6.7引入。

### `[alias] QLocale::Territory`

**作用与语义：**

该枚举类型是`Country`的别名，未来发布时将更名为Territory。

### `QLocale::QLocale()`

**作用与语义：**

构建一个以默认区域初始化的 QLocale 对象。
如果没有用`setDefault()`设置默认地点，这个位置将与`system()`返回的相同。

### `[explicit, since 6.3] QLocale::QLocale(QStringView name)`

**作用与语义：**

构造具有指定`name`的QLocale对象。
该名称的格式为“language[_script][_territory][.codeset][@modifier]”或“C”，其中：
- 语言是一种小写的两字母 ISO 639 语言代码（部分三字母代码也被认可），
- 文字是大写的四字母，符合ISO 15924标准，
- 领地是大写的两字母 ISO 3166 领地代码（部分数字代码也被认可），以及
- 忽略代码集和修饰符。
分隔符可以是下划线`'_'`（U 005F，“低行”）或破折号`'-'`（U 002D，“连字符减去”）。如果QLocale没有指定语言、文字和区域组合的数据，则使用最合适的匹配。如果字符串违反locale格式，或找不到指定键的合适数据，则使用“C”locale。
该构造器比QLocale（语言、文字、领土）或QLocale（语言、领土）慢得多。

### `QLocale::QLocale(QLocale::Language language, QLocale::Territory territory)`

**作用与语义：**

为指定的`language`和`territory`构造一个QLocale对象。
如果该组合使用多个脚本，则会选择一个可能的脚本。如果QLocale没有指定`language`的数据，则使用默认的区域。如果QLocale没有指定`language`和`territory`组合的数据，则可使用替代区域。

### `QLocale::QLocale(QLocale::Language language, QLocale::Script script = AnyScript, QLocale::Territory territory = AnyTerritory)`

**作用与语义：**

为指定的`language`、`script`和`territory`构造一个QLocale对象。
如果QLocale没有给定组合的数据，它会尽力寻找尽可能匹配的数据。它会回退到默认的区域，如果。
- `language`是`AnyLanguage`的，无法从语言`script`推断出`territory`
- QLocale 没有该语言的数据，无论是以`language`方式给出，还是如上推断。

### `[explicit] QLocale::QLocale(const QString &name)`

**作用与语义：**

构建一个以默认区域初始化的 QLocale 对象。
如果没有用`setDefault()`设置默认地点，这个位置将与`system()`返回的相同。

### `[noexcept] QLocale::QLocale(const QLocale &other)`

**作用与语义：**

构建一个QLocale对象作为`other`的副本。

### `[noexcept] QLocale::~QLocale()`

**作用与语义：**

毁灭者。

### `QString QLocale::amText() const`

**作用与语义：**

返回“AM”后缀的本地名称，用于根据12小时制约定的时间段。

### `QString QLocale::bcp47Name(QLocale::TagSeparator separator = TagSeparator::Dash) const`

**作用与语义：**

返回BCP47字段名称，并用破折号连接。
这结合了该区域所需的语言、文字和区域（以及可能的其他BCP47字段），以便唯一指定。注意，如果Unicode联盟的可能子标签规则在保留字段时暗示了遗漏字段，则可以省略字段。如需其他格式，请参见`name()`，了解如何从单个字段构造字符串。
与`uiLanguages()`不同，bcp47Name() 返回的值代表`QLocale`数据的本地名称;这不一定是用户界面应使用的语言。
该函数试图使地方名称符合 IETF 最佳通用实践 47，该 47 由 RFC 5646 定义。自 Qt 6.7 起，支持可选的 `separator` 参数，可用于覆盖 BCP47 规定的连字符分隔标签。但在 IETF 定义的协议中使用，默认 `QLocale::TagSeparator::Dash` 应保留。

### `[static noexcept] QLocale QLocale::c()`

**作用与语义：**

返回一个初始化为“C”区域的`QLocale`对象。
该区域基于en_US，但具有自身的各种特点，如简化的数字格式和自身的日期格式。它实现了描述“C”编程语言标准库函数行为的POSIX标准。
其中之一是其排序顺序基于字母的ASCII值，因此（在大小写区分排序中）所有大写字母都会排在任何小写字母之前（而不是每个字母的大写和小写形式相邻排序，然后先排到下一个字母的两个形式）。

### `[static noexcept, since 6.3] QLocale::Language QLocale::codeToLanguage(QStringView languageCode, QLocale::LanguageCodeTypes codeTypes = AnyLanguageCode)`

**作用与语义：**

返回对应 ISO 639 标准中定义的两字母或三字母 `languageCode` 的`QLocale::Language`枚举。
如果指定，`codeTypes`选择考虑换算的编码集合。默认情况下，所有已知的Qt编码都会被考虑。编码按以下顺序匹配：`ISO639Part1`、`ISO639Part2B`、`ISO639Part2T`、`ISO639Part3`、`LegacyLanguageCode`。
如果代码无效或未知，`QLocale::AnyLanguage`会返回。

### `[static noexcept, since 6.1] QLocale::Script QLocale::codeToScript(QStringView scriptCode)`

**作用与语义：**

返回对应于ISO 15924标准定义的四字母文字体`scriptCode`的枚举`QLocale::Script` enum。
如果代码无效或未知，则返回`QLocale::AnyScript`。

### `[static noexcept, since 6.2] QLocale::Territory QLocale::codeToTerritory(QStringView territoryCode)`

**作用与语义：**

返回对应 ISO 3166 标准中定义的两字母或三位数 `territoryCode` 的 `QLocale::Territory` enum。
如果代码无效或未知，`QLocale::AnyTerritory`会返回。

### `QLocale QLocale::collation() const`

**作用与语义：**

返回位置以便进行整理。
结果通常是该位置;但系统区域（通常是默认位置）会返回系统整合的位置。结果适合传递给`QCollator`的构造器。

### `QString QLocale::createSeparatedList(const QStringList &list) const`

**作用与语义：**

返回一个字符串，该字符串表示由给定的`list`字符串使用由地区设置定义的分隔符连接而成的字符串。

### `QString QLocale::currencySymbol(QLocale::CurrencySymbolFormat format = CurrencySymbol) const`

**作用与语义：**

根据`format`返回货币符号。

### `QString QLocale::dateFormat(QLocale::FormatType format = LongFormat) const`

**作用与语义：**

返回当前所在地使用的日期格式。
如果`format`是`LongFormat`，格式会很复杂，否则会很短。例如，`en_US`地`LongFormat`是`dddd, MMMM d, yyyy`，`ShortFormat`是`M/d/yy`。

### `QString QLocale::dateTimeFormat(QLocale::FormatType format = LongFormat) const`

**作用与语义：**

返回当前所在地使用的日期时间格式。
如果`format` `LongFormat`，格式会很复杂，否则会很短。例如，`en_US`地`LongFormat`是`dddd, MMMM d, yyyy h:mm:ss AP t`，`ShortFormat`是`M/d/yy h:mm AP`。

### `QString QLocale::dayName(int day, QLocale::FormatType type = LongFormat) const`

**作用与语义：**

返回`day`的本地名称（其中1代表周一，2代表周二，依此类推），格式由`type`规定。
例如，如果位置是`en_US`且`day`为1，`LongFormat`返回`Monday`、`ShortFormat` `Mon`和`NarrowFormat` `M`。

### `QString QLocale::decimalPoint() const`

**作用与语义：**

返回该位置的分数部分分隔符。
这是区分整数部分与分数部分的符号，用于表示包含小数部分的数字。这通常被称为“小数点字符”——尽管在许多地方它不是“点”（或类似的点）。自Qt 6.0起，它以字符串形式返回，以防某些地点需要多个UTF-16码点来表示其分隔符。

### `QString QLocale::exponential() const`

**作用与语义：**

返回该位置的指数分隔符。
这是用来区分尾数和指数的符号，在某些浮点数值表示中。自Qt 6.0起，它以字符串形式返回，因为在某些地方它不是单一字符——例如，它可能由乘号和“十的幂”算符表示组成。

### `Qt::DayOfWeek QLocale::firstDayOfWeek() const`

**作用与语义：**

根据当前地点，每周第一天返回。

### `QString QLocale::formattedDataSize(qint64 bytes, int precision = 2, QLocale::DataSizeFormats format = DataSizeIecFormat) const`

**作用与语义：**

将字节大小转换为可读的局部字符串，包含一个数字和一个量化单位。量词选择时，数字至少为一，且尽可能小。例如，如果`bytes`为16384，`precision`为2，`format`为`DataSizeIecFormat`（默认），该函数返回“16.00 KiB”;对于1330409069609字节，返回“1.21 GiB”;依此类推。如果`format`为`DataSizeIecFormat`或`DataSizeTraditionalFormat`，则将给定字节数除以1024的幂，结果小于1024;对于`DataSizeSIFormat`，除以1000的幂，结果小于1000。`DataSizeIecFormat`使用新的IEC标准量词Ki、Mi等，而`DataSizeSIFormat`使用较旧的SI量词k、M等，`DataSizeTraditionalFormat`滥用它们。

### `QString QLocale::groupSeparator() const`

**作用与语义：**

返回该位置的数字分组分隔符。
这是一种用于将数字表示中长串数字的符号拆分，以便阅读。在某些区域中，标记可能是空的，表示数字不应以这种方式被分组。在其他地方，它可能是一个间隔字符。自Qt 6.0起，它以字符串形式返回，以防某些区域需要多个UTF-16码点来表示其分隔符。

### `QLocale::Language QLocale::language() const`

**作用与语义：**

还原了该地的语言。

### `[static, since 6.3] QString QLocale::languageToCode(QLocale::Language language, QLocale::LanguageCodeTypes codeTypes = AnyLanguageCode)`

**作用与语义：**

返回`language`的两字母或三字母语言代码，符合ISO 639标准定义。
如果指定，`codeTypes`选择要考虑的编码集。返回定义为`language`的第一个编码。否则，考虑所有ISO-639编码。编码顺序为：`ISO639Part1`、`ISO639Part2B`、`ISO639Part2T`、`ISO639Part3`。`LegacyLanguageCode`被该函数忽略。
注意：对于`QLocale::C`，函数返回`"C"`。对于`QLocale::AnyLanguage`，返回一个空字符串。如果语言在任何选择的代码集中都没有代码，则返回一个空字符串。

### `[static] QString QLocale::languageToString(QLocale::Language language)`

**作用与语义：**

返回包含`language`名称的`QString`。

### `[static] QList<QLocale> QLocale::matchingLocales(QLocale::Language language, QLocale::Script script, QLocale::Territory territory)`

**作用与语义：**

返回与给定`language`、`script`和`territory`匹配的有效位置对象列表。
获取所有地点列表：`QList`<`QLocale`> allLocales = QLocale：：matchingLocales（`QLocale::AnyLanguage`， `QLocale::AnyScript`， `QLocale::AnyTerritory`）;
获取适合俄罗斯的地点列表：`QList`<`QLocale`> locationes = QLocale：：matchingLocales（`QLocale::AnyLanguage`， `QLocale::AnyScript`， `QLocale::Russia`）;

### `QLocale::MeasurementSystem QLocale::measurementSystem() const`

**作用与语义：**

返回该区域的测量系统。

### `QString QLocale::monthName(int month, QLocale::FormatType type = LongFormat) const`

**作用与语义：**

返回`month`的本地化名称，格式由`type`规定。
例如，如果地点是`en_US`，`month`是1，`LongFormat`会返回`January`。`ShortFormat` `Jan`，`NarrowFormat` `J`。

### `QString QLocale::name(QLocale::TagSeparator separator = TagSeparator::Underscore) const`

**作用与语义：**

这个地方的简称。
返回该地点的语言和区域，形式为“language_territory”，其中语言为小写的两字母 ISO 639 语言代码，区域为大写的两字母或三字母 ISO 3166 区域代码。如果所在地没有指定区域，则仅返回语言名称。自 Qt 6.7 起，可选的 `separator` 参数可用于覆盖两个标签之间的默认下划线字符。
即使`QLocale`对象是用显式脚本构建的，name()也不会包含它，出于兼容性原因。如果你需要完整的locale名，或者通过传递locale的`language()`传递给`languageToCode()`构建你想用的词来识别某个locale，可以用`bcp47Name()`来识别，脚本和区域也要做类似的操作。

### `QString QLocale::nativeLanguageName() const`

**作用与语义：**

返回该语言的本地名称。例如，瑞士-德语地点的“Schweizer Hochdeutsch”。

### `[since 6.2] QString QLocale::nativeTerritoryName() const`

**作用与语义：**

返回该地区的本地名称。例如“España”表示西班牙/西班牙地区。

### `QString QLocale::negativeSign() const`

**作用与语义：**

返回该地点的负符号指示器。
这是一个标记，推测用作数字前缀，表示该数字为负数。自Qt 6.0起，它以字符串形式返回，因为在某些地区它不是单个字符——例如，因为它包含文本方向控制字符。

### `QLocale::NumberOptions QLocale::numberOptions() const`

**作用与语义：**

返回该`QLocale`实例中与数字转换相关的选项。
默认情况下，标准区域没有设置任何选项，除了“C”区域，该区域默认设置了`OmitGroupSeparator`。

### `QString QLocale::percent() const`

**作用与语义：**

返回该地点的百分比标记。
这是一个标记，假设会附加在数字后以表示百分比。自Qt 6.0起，它以字符串形式返回，因为在某些地区它不是单个字符——例如，因为它包含文本方向控制字符。

### `QString QLocale::pmText() const`

**作用与语义：**

返回“PM”后缀的本地名称，适用于根据12小时制约定的时间。

### `QString QLocale::positiveSign() const`

**作用与语义：**

返回该地点的正符号指示器。
这是一个标记，推测用作数字的前缀，表示该数字为正数。自Qt 6.0起，它以字符串形式返回，因为在某些地区它不是单个字符——例如，因为它包含文本方向控制字符。

### `QString QLocale::quoteString(const QString &str, QLocale::QuotationStyle style = StandardQuotation) const`

**作用与语义：**

报税`str`根据当前地区使用给定的报价`style`进行报价。

### `[since 6.0] QString QLocale::quoteString(QStringView str, QLocale::QuotationStyle style = StandardQuotation) const`

**作用与语义：**

报税`str`根据当前地区使用给定的报价`style`进行报价。

### `QLocale::Script QLocale::script() const`

**作用与语义：**

返回该地点的剧本。

### `[static, since 6.1] QString QLocale::scriptToCode(QLocale::Script script)`

**作用与语义：**

返回ISO 15924标准定义的四字母脚本代码，用于`script`。
注意：对于`QLocale::AnyScript`，返回一个空字符串。

### `[static] QString QLocale::scriptToString(QLocale::Script script)`

**作用与语义：**

返回包含`script`名称的`QString`。

### `[static] void QLocale::setDefault(const QLocale &locale)`

**作用与语义：**

将全局默认地点设置为`locale`。
当构造一个没有参数的`QLocale`对象时，会使用该区域。如果未调用该函数，则使用系统的区域。
警告：在多线程应用中，默认位置应在应用启动时设置，然后才创建任何非图形界面线程。
警告：此函数不重复使用。

### `void QLocale::setNumberOptions(QLocale::NumberOptions options)`

**作用与语义：**

为该`QLocale`实例设置与数字转换相关的 `options`。

### `QString QLocale::standaloneDayName(int day, QLocale::FormatType type = LongFormat) const`

**作用与语义：**

返回`day`的本地化名称（其中1代表周一，2代表周二，依此类推），作为独立文本使用，格式由`type`规定。
如果位置信息未指定独立的日期名称，则返回值与 `dayName()` 中相同。

### `QString QLocale::standaloneMonthName(int month, QLocale::FormatType type = LongFormat) const`

**作用与语义：**

返回作为独立文本使用的`month`的本地化名称，格式由`type`规定。
如果地区信息没有指定独立月份名称，那么返回值和`monthName()`中一样。

### `[noexcept] void QLocale::swap(QLocale &other)`

**作用与语义：**

将该地点与`other`交换。这项操作非常快速，且从未失败。

### `[static] QLocale QLocale::system()`

**作用与语义：**

返回一个初始化到系统区域的`QLocale`对象。
系统所在地可能使用系统特定的来源（如有）获取位置数据，否则则依赖`QLocale`内置的数据库条目，涵盖系统报告的语言、脚本和区域。
例如，在Windows和Mac上，该区域将使用系统配置面板中指定的十进制/分组字符和日期/时间格式。

### `[since 6.2] QLocale::Territory QLocale::territory() const`

**作用与语义：**

归还了该地的领土。

### `[static, since 6.2] QString QLocale::territoryToCode(QLocale::Territory territory)`

**作用与语义：**

返回`territory`的两个字母区域代码，符合ISO 3166标准定义。
注意：对于`QLocale::AnyTerritory`，返回一个空字符串。

### `[static, since 6.2] QString QLocale::territoryToString(QLocale::Territory territory)`

**作用与语义：**

返回包含`territory`名称的`QString`。

### `Qt::LayoutDirection QLocale::textDirection() const`

**作用与语义：**

返回语言的文本方向。

### `QString QLocale::timeFormat(QLocale::FormatType format = LongFormat) const`

**作用与语义：**

返回当前所在地使用的时间格式。
如果`format`是`LongFormat`，格式会很复杂，否则会很短。例如，`en_US`地点的`LongFormat`是`h:mm:ss AP t`，`ShortFormat`是`h:mm AP`。

### `QString QLocale::toCurrencyString(qlonglong value, const QString &symbol = QString()) const`

**作用与语义：**

返回`value`作为货币的局部字符串表示。如果提供了`symbol`，则用它代替默认货币符号。

### `QString QLocale::toCurrencyString(int value, const QString &symbol = QString()) const`

**作用与语义：**

返回`value`作为货币的局部字符串表示。如果提供了`symbol`，则用它代替默认货币符号。

### `QString QLocale::toCurrencyString(qulonglong value, const QString &symbol = QString()) const`

**作用与语义：**

返回`value`作为货币的局部字符串表示。如果提供了`symbol`，则用它代替默认货币符号。

### `QString QLocale::toCurrencyString(short value, const QString &symbol = QString()) const`

**作用与语义：**

返回`value`作为货币的局部字符串表示。如果提供了`symbol`，则用它代替默认货币符号。

### `QString QLocale::toCurrencyString(uint value, const QString &symbol = QString()) const`

**作用与语义：**

返回`value`作为货币的局部字符串表示。如果提供了`symbol`，则用它代替默认货币符号。

### `QString QLocale::toCurrencyString(ushort value, const QString &symbol = QString()) const`

**作用与语义：**

返回`value`作为货币的局部字符串表示。如果提供了`symbol`，则用它代替默认货币符号。

### `QString QLocale::toCurrencyString(double value, const QString &symbol = QString(), int precision = -1) const`

**作用与语义：**

返回`value`作为货币的局部字符串表示。如果提供了`symbol`，则用它代替默认货币符号。如果提供了`precision`，则用于设置货币值的精度。
注意：该功能会超载`QLocale::toCurrencyString()`。

### `QString QLocale::toCurrencyString(float i, const QString &symbol = QString(), int precision = -1) const`

**作用与语义：**

注意：该功能会让`QLocale::toCurrencyString()`重载。

### `QDate QLocale::toDate(const QString &string, QLocale::FormatType format = LongFormat, int baseYear = DefaultTwoDigitBaseYear) const`

**作用与语义：**

`string`读作是特定地区的约会`format`。
解析`string`并返回其代表的日期。日期字符串的格式根据`format`参数选择（参见 `dateFormat()`）。
有些地区，尤其是对于`ShortFormat`，只使用年份的最后两位数字。在这种情况下，首先考虑的候选对象是从`baseYear`开始的100年。在6.7之前没有`baseYear`参数，始终使用1900年。这是`baseYear`的默认选择年份，从1900年到1999年。在某些情况下，其他字段可能会选择下一个或上一个世纪，以获得与所有字段一致的结果。详见 `QDate::fromString()`。
注意：使用月份和日期名称时，必须以当地语言表示。
如果无法解析该日期，则返回无效日期。

### `QDate QLocale::toDate(const QString &string, const QString &format, int baseYear = DefaultTwoDigitBaseYear) const`

**作用与语义：**

`string`读作给定`format`中的日期。
解析`string`并返回其表示的日期。请参见 T `QDate::fromString()` 以了解 `format` 的解释。
当`format`只指定年份的最后两位时，首先考虑的候选对象是从`baseYear`开始的100年。6.7之前没有`baseYear`参数，始终使用1900年。这是`baseYear`的默认选择年份，从1900年到1999年。在某些情况下，其他字段可能会选择下一个或上一个世纪，以获得与所有字段一致的结果。详情请参见 `QDate::fromString()`。
注意：使用月份和日期名称时，必须以当地语言表示。
如果无法解析该日期，则返回无效日期。

### `QDate QLocale::toDate(const QString &string, QLocale::FormatType format, QCalendar cal, int baseYear = DefaultTwoDigitBaseYear) const`

**作用与语义：**

`string`读作是特定地区的约会`format`。
解析`string`并返回其代表的日期。日期字符串的格式根据`format`参数选择（参见 `dateFormat()`）。
有些地区，尤其是对于`ShortFormat`，只使用年份的最后两位数字。在这种情况下，首先考虑的候选对象是从`baseYear`开始的100年。在6.7之前没有`baseYear`参数，始终使用1900年。这是`baseYear`的默认选择年份，从1900年到1999年。在某些情况下，其他字段可能会选择下一个或上一个世纪，以获得与所有字段一致的结果。详见 `QDate::fromString()`。
注意：使用月份和日期名称时，必须以当地语言表示。
如果无法解析该日期，则返回无效日期。

### `QDate QLocale::toDate(const QString &string, const QString &format, QCalendar cal, int baseYear = DefaultTwoDigitBaseYear) const`

**作用与语义：**

`string`读作是特定地区的约会`format`。
解析`string`并返回其代表的日期。日期字符串的格式根据`format`参数选择（参见 `dateFormat()`）。
有些地区，尤其是对于`ShortFormat`，只使用年份的最后两位数字。在这种情况下，首先考虑的候选对象是从`baseYear`开始的100年。在6.7之前没有`baseYear`参数，始终使用1900年。这是`baseYear`的默认选择年份，从1900年到1999年。在某些情况下，其他字段可能会选择下一个或上一个世纪，以获得与所有字段一致的结果。详见 `QDate::fromString()`。
注意：使用月份和日期名称时，必须以当地语言表示。
如果无法解析该日期，则返回无效日期。

### `QDateTime QLocale::toDateTime(const QString &string, QLocale::FormatType format = LongFormat, int baseYear = DefaultTwoDigitBaseYear) const`

**作用与语义：**

`string`读作是特定地区的日期时间`format`。
解析`string`并返回其所代表的日期-时间。日期字符串的格式根据`format`参数选择（参见 `dateFormat()`）。
有些地区，尤其是用于 `ShortFormat`，只使用年份的最后两位数字。在这种情况下，首先考虑的候选对象是从 `baseYear` 开始的 100 年。在 6.7 之前没有`baseYear`参数，始终使用 1900 年。这是`baseYear`的默认选择年份，从那时到1999年。在某些情况下，其他字段可能会选择下一个或上一个世纪，以获得与所有字段结果一致的结果。详情请参见 `QDate::fromString()`。
注意：使用月份和日期名称时，必须以当地语言表示。任何上午/下午指示必须与`amText()`或`pmText()`相符，忽略大小写。
如果字符串无法解析，则返回无效`QDateTime`。

### `QDateTime QLocale::toDateTime(const QString &string, const QString &format, int baseYear = DefaultTwoDigitBaseYear) const`

**作用与语义：**

在给定`format`中，`string`被当作日期时间。
解析`string`并返回其所代表的日期时间。关于`format`的解释，请参见`QDateTime::fromString()`。
当`format`只指定年份的最后两位时，首先考虑的候选对象是从`baseYear`开始的100年。6.7之前没有`baseYear`参数，始终使用1900年。这是`baseYear`的默认选择年份，从那时起到1999年。在某些情况下，其他字段可能会选择下一个或上一个世纪，以获得与所有字段一致的结果。详见 `QDate::fromString()`。
注意：月份和日期名称（如使用）必须以当地语言表示。任何上午/下午指示必须与`amText()`或`pmText()`相符，忽略大小写。
如果字符串无法解析，返回无效`QDateTime`。如果字符串可解析且表示无效日期时间（例如时区跳跃的间隔），则返回无效`QDateTime`，其 toMSecsSinceEpoch() 代表有效的近邻日期时间。将该字符串传递给 fromMSecsSinceEpoch() 会生成一个有效日期时间，但该字符串无法忠实表示。

### `QDateTime QLocale::toDateTime(const QString &string, QLocale::FormatType format, QCalendar cal, int baseYear = DefaultTwoDigitBaseYear) const`

**作用与语义：**

`string`读作是特定地区的日期时间`format`。
解析`string`并返回其所代表的日期-时间。日期字符串的格式根据`format`参数选择（参见 `dateFormat()`）。
有些地区，尤其是用于 `ShortFormat`，只使用年份的最后两位数字。在这种情况下，首先考虑的候选对象是从 `baseYear` 开始的 100 年。在 6.7 之前没有`baseYear`参数，始终使用 1900 年。这是`baseYear`的默认选择年份，从那时到1999年。在某些情况下，其他字段可能会选择下一个或上一个世纪，以获得与所有字段结果一致的结果。详情请参见 `QDate::fromString()`。
注意：使用月份和日期名称时，必须以当地语言表示。任何上午/下午指示必须与`amText()`或`pmText()`相符，忽略大小写。
如果字符串无法解析，则返回无效`QDateTime`。

### `QDateTime QLocale::toDateTime(const QString &string, const QString &format, QCalendar cal, int baseYear = DefaultTwoDigitBaseYear) const`

**作用与语义：**

`string`读作是特定地区的日期时间`format`。
解析`string`并返回其所代表的日期-时间。日期字符串的格式根据`format`参数选择（参见 `dateFormat()`）。
有些地区，尤其是用于 `ShortFormat`，只使用年份的最后两位数字。在这种情况下，首先考虑的候选对象是从 `baseYear` 开始的 100 年。在 6.7 之前没有`baseYear`参数，始终使用 1900 年。这是`baseYear`的默认选择年份，从那时到1999年。在某些情况下，其他字段可能会选择下一个或上一个世纪，以获得与所有字段结果一致的结果。详情请参见 `QDate::fromString()`。
注意：使用月份和日期名称时，必须以当地语言表示。任何上午/下午指示必须与`amText()`或`pmText()`相符，忽略大小写。
如果字符串无法解析，则返回无效`QDateTime`。

### `double QLocale::toDouble(QStringView s, bool *ok = nullptr) const`

**作用与语义：**

返回由局部字符串表示的双重节点 `s`。
如果转换溢出，返回无穷大;如果因其他原因（如下溢）失败，返回0.0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，通过将*`ok`设为`true`来报告成功。
注意最后一次换算返回1234.0，因为“.”是德语地点中的千分组分隔符。
该函数忽略前置和后置的空白。

**官方示例：**

```cpp
 bool ok;
 double d;

 QLocale c(QLocale::C);
 d = c.toDouble(u"1234.56", &ok);  // ok == true,  d == 1234.56
 d = c.toDouble(u"1,234.56", &ok); // ok == true,  d == 1234.56
 d = c.toDouble(u"1234,56", &ok);  // ok == false, d == 0

 QLocale german(QLocale::German);
 d = german.toDouble(u"1234,56", &ok);  // ok == true,  d == 1234.56
 d = german.toDouble(u"1.234,56", &ok); // ok == true,  d == 1234.56
 d = german.toDouble(u"1234.56", &ok);  // ok == false, d == 0

 d = german.toDouble(u"1.234", &ok);    // ok == true,  d == 1234.0
```

### `double QLocale::toDouble(const QString &s, bool *ok = nullptr) const`

**作用与语义：**

返回由局部字符串表示的双重节点 `s`。
如果转换溢出，返回无穷大;如果因其他原因（如下溢）失败，返回0.0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，通过将*`ok`设为`true`来报告成功。
注意最后一次换算返回1234.0，因为“.”是德语地点中的千分组分隔符。
该函数忽略前置和后置的空白。

**官方示例：**

```cpp
 bool ok;
 double d;

 QLocale c(QLocale::C);
 d = c.toDouble("1234.56", &ok);  // ok == true,  d == 1234.56
 d = c.toDouble("1,234.56", &ok); // ok == true,  d == 1234.56
 d = c.toDouble("1234,56", &ok);  // ok == false, d == 0

 QLocale german(QLocale::German);
 d = german.toDouble("1234,56", &ok);  // ok == true,  d == 1234.56
 d = german.toDouble("1.234,56", &ok); // ok == true,  d == 1234.56
 d = german.toDouble("1234.56", &ok);  // ok == false, d == 0

 d = german.toDouble("1.234", &ok);    // ok == true,  d == 1234.0
```

### `float QLocale::toFloat(QStringView s, bool *ok = nullptr) const`

**作用与语义：**

返回由局部字符串`s`表示的浮点数。
如果转换溢出，返回无穷大;如果因其他原因（如下溢）失败，返回0.0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
该函数忽略前置和后置的空白。

### `float QLocale::toFloat(const QString &s, bool *ok = nullptr) const`

**作用与语义：**

返回由局部字符串`s`表示的浮点数。
如果转换溢出，返回无穷大;如果因其他原因（如下溢）失败，返回0.0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
该函数忽略前置和后置的空白。

### `int QLocale::toInt(QStringView s, bool *ok = nullptr) const`

**作用与语义：**

返回由局部字符串表示的整数 `s`。
如果转换失败，函数返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功通过将*`ok`设为`true`来报告。
该函数忽略前置和后置的空白。

### `int QLocale::toInt(const QString &s, bool *ok = nullptr) const`

**作用与语义：**

返回由局部字符串表示的整数 `s`。
如果转换失败，函数返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
该函数忽略前置和后置的空白。

### `long QLocale::toLong(QStringView s, bool *ok = nullptr) const`

**作用与语义：**

返回由局部字符串`s`表示的长整数。
如果转换失败，函数返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
该函数忽略前置和后置的空白。

### `long QLocale::toLong(const QString &s, bool *ok = nullptr) const`

**作用与语义：**

返回由局部字符串`s`表示的长整数。
如果转换失败，函数返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
该函数忽略前置和后置的空白。

### `qlonglong QLocale::toLongLong(QStringView s, bool *ok = nullptr) const`

**作用与语义：**

返回由局部字符串`s`表示的长长整数。
如果转换失败，函数返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`来报告失败，成功则将*`ok`设为`true`。
该函数忽略前置和后置的空白。

### `qlonglong QLocale::toLongLong(const QString &s, bool *ok = nullptr) const`

**作用与语义：**

返回由局部字符串表示的长长整数（long int）`s`。
如果转换失败，函数返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`来报告失败，成功则将*`ok`设为`true`。
该函数忽略前置和后置的空白。

### `QString QLocale::toLower(const QString &str) const`

**作用与语义：**

返回`str`的小写副本。
如果 Qt Core 使用 ICU 库，则会根据当前区域的规则进行转换。否则转换可能依赖平台，`QString::toLower()` 作为通用的备用。

### `short QLocale::toShort(QStringView s, bool *ok = nullptr) const`

**作用与语义：**

返回由局部字符串`s`表示的短int。
如果转换失败，函数返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
该函数忽略前置和后置的空白。

### `short QLocale::toShort(const QString &s, bool *ok = nullptr) const`

**作用与语义：**

返回由局部字符串`s`表示的短int。
如果转换失败，函数返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
该函数忽略前置和后置的空白。

### `QString QLocale::toString(qlonglong i) const`

**作用与语义：**

返回`i`的局部字符串表示。

### `QString QLocale::toString(QDate date, const QString &format) const`

**作用与语义：**

返回指定`format`中给定`date`的局部字符串表示。如果`format`是空字符串，则返回空字符串。

### `QString QLocale::toString(QTime time, QLocale::FormatType format = LongFormat) const`

**作用与语义：**

返回指定`format`中给定`time`的局部字符串表示（参见 `timeFormat()`）。

### `QString QLocale::toString(QTime time, QStringView format) const`

**作用与语义：**

返回根据指定`format`返回给定`time`的局部字符串表示。如果`format`是空字符串，则返回空字符串。

### `QString QLocale::toString(QTime time, const QString &format) const`

**作用与语义：**

返回根据指定`format`返回给定`time`的局部字符串表示。如果`format`是空字符串，则返回空字符串。

### `QString QLocale::toString(const QDateTime &dateTime, const QString &format) const`

**作用与语义：**

返回根据指定`format`返回给定`dateTime`的局部字符串表示。如果`format`是空字符串，则返回空字符串。

### `QString QLocale::toString(QDate date, QLocale::FormatType format, QCalendar cal) const`

**作用与语义：**

根据指定`format`返回给定`date`的局部字符串表示（参见 `dateFormat()`），可选择指定日历`cal`。
注意：有些地方可能使用限制所代表年份范围的格式。

### `QString QLocale::toString(QDate date, QStringView format, QCalendar cal) const`

**作用与语义：**

返回指定`format`中给定`date`的局部字符串表示，针对指定日历`cal`可选择性返回。如果`format`是空字符串，则返回空字符串。

### `QString QLocale::toString(const QDateTime &dateTime, QLocale::FormatType format, QCalendar cal) const`

**作用与语义：**

根据指定`format`返回给定`dateTime`的局部字符串表示（参见`dateTimeFormat()`），可选择指定日历`cal`。
注意：有些地方可能使用限制所代表年份范围的格式。

### `QString QLocale::toString(const QDateTime &dateTime, QStringView format, QCalendar cal) const`

**作用与语义：**

根据指定`format`返回给定`dateTime`的局部字符串表示，针对指定日历`cal`可选择性地返回。如果`format`是空字符串，则返回空字符串。

### `QString QLocale::toString(int i) const`

**作用与语义：**

返回`i`的局部字符串表示。

### `QString QLocale::toString(long i) const`

**作用与语义：**

返回`i`的局部字符串表示。

### `QString QLocale::toString(qulonglong i) const`

**作用与语义：**

返回`i`的局部字符串表示。

### `QString QLocale::toString(short i) const`

**作用与语义：**

返回`i`的局部字符串表示。

### `QString QLocale::toString(uint i) const`

**作用与语义：**

返回`i`的局部字符串表示。

### `QString QLocale::toString(ulong i) const`

**作用与语义：**

返回`i`的局部字符串表示。

### `QString QLocale::toString(ushort i) const`

**作用与语义：**

返回`i`的局部字符串表示。

### `QString QLocale::toString(QDate date, QLocale::FormatType format = LongFormat) const`

**作用与语义：**

返回`i`的局部字符串表示。

### `QString QLocale::toString(QDate date, QStringView format) const`

**作用与语义：**

返回`i`的局部字符串表示。

### `QString QLocale::toString(const QDateTime &dateTime, QLocale::FormatType format = LongFormat) const`

**作用与语义：**

返回`i`的局部字符串表示。

### `QString QLocale::toString(const QDateTime &dateTime, QStringView format) const`

**作用与语义：**

返回`i`的局部字符串表示。

### `QString QLocale::toString(double f, char format = 'g', int precision = 6) const`

**作用与语义：**

返回表示浮点数 `f` 的字符串。 该表示形式由 `format` 和 `precision` 参数控制。 `format` 默认为 `'g'`。它可以是以下任意一种：
- `Format`：含义；`precision` 的含义
- `'e'`：格式为 [-]9.9e[ |-]999；小数点后的位数
- `'E'`：格式为 [-]9.9E[ |-]999；
- `'f'`：格式为 [-]9.9；
- `'F'`：与 `'f'` 相同，除了 INF 和 NAN（见下文）；
- `'g'`：使用 `'e'` 或 `'f'` 格式，以更简洁者为准；最多有效数字（省略尾随零）
- `'G'`：使用 `'E'` 或 `'F'` 格式，以更简洁者为准；
特殊 `precision` 值 `QLocale::FloatingPointShortest` 选择最短表示形式，当其被读取为数字时，可以恢复原始浮点值。除此之外，任何负的 `precision` 都会被忽略，默认为 6。
对于 `'e'`、`'f'` 和 `'g'` 格式，正无穷大表示为 "inf"，负无穷大表示为 "-inf"，浮点 NaN（非数字）值表示为 "nan"。对于 `'E'`、`'F'` 和 `'G'` 格式，则使用 "INF" 和 "NAN"。此表示形式不随区域设置变化。

### `QString QLocale::toString(float f, char format = 'g', int precision = 6) const`

**作用与语义：**

返回一个表示浮点数`f`的字符串。
`format`和`precision`与`toString`中描述的含义相同（双、字符、int）。

### `QString QLocale::toString(qlonglong number, int fieldWidth, char32_t fillChar) const`

**作用与语义：**

返回给定`number`的字符串表示。
字符串的长度至少应为绝对值`fieldWidth`，如果`number`位数较少，则使用`fillChar`作为填充。如果`fillChar` `'0'`，则该位置的零位作为填充。如果`fieldWidth`为负，字符串从其表示`number`开始，如果更短，则填充到长度`-fieldWidth`，并用给定的`fillChar`。对于正fieldWidth，填充出现在`number`表示之前。当`number`为负且`fieldWidth`为正时，若`fillChar`为`'0'`，填充会插入该位置的负号与数字开头之间。
注意：该功能会让`QLocale::toString()`重载。

### `QString QLocale::toString(qulonglong number, int fieldWidth, char32_t fillChar) const`

**作用与语义：**

返回给定`number`的字符串表示。
字符串的长度至少应是`fieldWidth`的绝对值，如果`number`数字较少，则使用`fillChar`作为填充。如果`fillChar` `'0'`该位置的零位数字作为填充。如果`fieldWidth`为负，字符串从其表示的`number`开始，如果较短，则填充到长度`-fieldWidth`，并用给定的`fillChar`。对于正场宽，填充出现在`number`表示之前。
注意：该功能会让`QLocale::toString()`重载。

### `QString QLocale::toString(long number, int fieldWidth, char32_t fillChar) const`

**作用与语义：**

返回给定`number`的字符串表示。
字符串的长度至少为`fieldWidth`的绝对值，如果`number`位数较少，则使用`fillChar`作为填充。如果`fillChar` `'0'`该位置的零位数字作为填充。如果`fieldWidth`为负，字符串从其表示`number`开始，如果较短，则填充至长度`-fieldWidth`，并以给定`fillChar`。对于正fieldWidth，填充出现在`number`表示之前。当`number`为负且`fieldWidth`为正时，若`fillChar`为`'0'`，填充会插入该位置的负号与数字数字开头之间。

### `QString QLocale::toString(ulong number, int fieldWidth, char32_t fillChar) const`

**作用与语义：**

返回给定`number`的字符串表示。
字符串的长度至少为`fieldWidth`的绝对值，如果`number`位数较少，则使用`fillChar`作为填充。如果`fillChar` `'0'`该位置的零位数字作为填充。如果`fieldWidth`为负，字符串从其表示`number`开始，如果较短，则填充至长度`-fieldWidth`，并以给定`fillChar`。对于正fieldWidth，填充出现在`number`表示之前。当`number`为负且`fieldWidth`为正时，若`fillChar`为`'0'`，填充会插入该位置的负号与数字数字开头之间。

### `QTime QLocale::toTime(const QString &string, QLocale::FormatType format = LongFormat) const`

**作用与语义：**

`string`读作是特定地区的时间`format`。
解析`string`并返回其所代表的时间。时间字符串的格式根据`format`参数选择（参见 `timeFormat()`）。
注意：任何早晚指示器必须与`amText()`或`pmText()`相符，忽略大小写。
如果无法解析时间，则返回无效时间。

### `QTime QLocale::toTime(const QString &string, const QString &format) const`

**作用与语义：**

读作`string`在给定`format`中的一个时间。
解析`string`并返回其所代表的时间。参见`QTime::fromString()` `format`的解释。
注意：任何早晚指示器必须与`amText()`或`pmText()`相符，忽略格。
如果无法解析时间，则返回无效时间。

### `uint QLocale::toUInt(QStringView s, bool *ok = nullptr) const`

**作用与语义：**

返回由本地字符串`s`表示的无符号整数。
如果转换失败，函数返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
该函数忽略前置和后置的空白。

### `uint QLocale::toUInt(const QString &s, bool *ok = nullptr) const`

**作用与语义：**

返回由局部字符串`s`表示的无符号整数。
如果转换失败，函数返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`来报告失败，成功则将*`ok`设为`true`。
该函数忽略前置和后置的空白。

### `ulong QLocale::toULong(QStringView s, bool *ok = nullptr) const`

**作用与语义：**

返回由本地字符串`s`表示的无符号长整数。
如果转换失败，函数返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`来报告失败，成功则将*`ok`设为`true`。
该函数忽略前置和后置的空白。

### `ulong QLocale::toULong(const QString &s, bool *ok = nullptr) const`

**作用与语义：**

返回由本地字符串`s`表示的无符号长整数。
如果转换失败，函数返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`来报告失败，成功则将*`ok`设为`true`。
该函数忽略前置和后置的空白。

### `qulonglong QLocale::toULongLong(QStringView s, bool *ok = nullptr) const`

**作用与语义：**

返回由局部字符串`s`表示的无符号长长int。
如果转换失败，函数返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
该函数忽略前置和后置的空白。

### `qulonglong QLocale::toULongLong(const QString &s, bool *ok = nullptr) const`

**作用与语义：**

返回由局部字符串`s`表示的无符号长长整数。
如果转换失败，函数返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`来报告失败，成功则将*`ok`设为`true`。
该函数忽略前置和后置的空白。

### `ushort QLocale::toUShort(QStringView s, bool *ok = nullptr) const`

**作用与语义：**

返回由本地字符串`s`表示的无符号短int。
如果转换失败，函数返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
该函数忽略前置和后置的空白。

### `ushort QLocale::toUShort(const QString &s, bool *ok = nullptr) const`

**作用与语义：**

返回由局部字符串`s`表示的无符号短int。
如果转换失败，函数返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
该函数忽略前置和后置的空白。

### `QString QLocale::toUpper(const QString &str) const`

**作用与语义：**

返回一份大写的`str`。
如果 Qt Core 使用 ICU 库，则会根据当前区域的规则进行转换。否则转换可能依赖平台，`QString::toUpper()` 作为通用的备用。
注意：在某些情况下，字符串的大写形式可能比原字母更长。

### `QStringList QLocale::uiLanguages(QLocale::TagSeparator separator = TagSeparator::Dash) const`

**作用与语义：**

用于选择翻译的区域名称列表。
返回列表中的每个条目都是适合用户将界面翻译为所选语言的区域名称。如果列表中的名称由多个标签组成，它们将按照 `separator` 所示方式连接。在 Qt 6.7 之前，使用破折号作为分隔符。
例如，使用默认分隔符 `QLocale::TagSeparator::Dash`，如果用户将系统配置为使用美国英语，则列表为 "en-Latn-US"、"en-US"、"en-Latn"、"en"。条目的顺序表示检查翻译的顺序；列表中靠前的条目优先于靠后的条目。如果你的翻译文件（或其他特定于区域的资源）使用下划线而非破折号来分隔区域标签，请将 `QLocale::TagSeparator::Underscore` 作为 `separator` 传入。
返回区域名称列表。该列表可能包含多种语言，尤其是在系统区域配置了多种 UI 翻译语言时。条目的顺序很重要。例如，对于系统区域，它反映了用户的偏好。
在 Qt 6.9 之前，列表仅包含显式配置的区域及其等效项。这导致一些调用者添加了截断（例如将 'en-Latn-DE' 截断为 'en'）作为备用。这有时可能导致不合适的选择，尤其是在这些截断尝试早于更合适的后续条目时。
从 Qt 6.9 开始，合理的截断会包含在返回列表中，位于所有与显式指定区域等效的条目之后。此更改允许在无需调用者进行任何截断的情况下提供更准确的备用选项。
用户可以在系统配置中显式包含首选的备用区域（例如 en-US）以控制优先顺序。建议你依赖 uiLanguages() 中条目的顺序，而不是使用自定义的备用方法。
你很可能不需要直接使用此函数，只需将 `QLocale` 对象传递给 `QTranslator::load()` 函数即可。

### `QList<Qt::DayOfWeek> QLocale::weekdays() const`

**作用与语义：**

返回根据当前地点被视为工作日的日期列表。

### `QString QLocale::zeroDigit() const`

**作用与语义：**

返回该位置的零位字符。
这是一个单一的Unicode字符，但可以作为代节点编码，因此（自Qt 6.0起）以字符串形式返回。在大多数地区，其他数字在Unicode排序中紧随其后——然而，一些数字系统，尤其是以U 3007为零的数字，数字不连续。使用`toString()`来获得合适的数字表示，而不是试图从这个零数字构建数字。

### `[noexcept] QLocale &QLocale::operator=(const QLocale &other)`

**作用与语义：**

将`other`分配到该`QLocale`对象，并返回对该`QLocale`对象的引用。

### `[since 6.7] const int QLocale::DefaultTwoDigitBaseYear`

**作用与语义：**

该变量为采用两位数年份格式所选择的世纪默认起始年份。常数值为`1900`。
有些地区，尤其是`ShortFormat`，只使用年份的最后两位数字。从6.7开始，1900年一直是此类情况下的基准年份。现在各种`QLocale`和`QDate`函数都有超载，允许调用者指定基准年，该常数作为默认值。
该变量在Qt 6.7中引入。

### `[noexcept] size_t qHash(const QLocale &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] bool operator!=(const QLocale &lhs, const QLocale &rhs)`

**作用与语义：**

如果两个`QLocale`对象`lhs`和`rhs`不同，返回`true`;否则返回`false`。
注意：系统区域不等于由其`language()`构建的`QLocale`对象，即`script()`和`territory()`，即使两者在所有数据字段中一致。两个不同数字选项的区域也不相等。

### `[noexcept] bool operator==(const QLocale &lhs, const QLocale &rhs)`

**作用与语义：**

如果两个`QLocale`对象`lhs`和`rhs`相同，返回`true`;否则返回`false`。
注意：系统区域不等于由其`language()`构建的`QLocale`对象，`script()`和`territory()`，即使两者在所有数据字段中一致。两个不同数字选项的地点也不相等。

### `enum DataSizeFormat { DataSizeIecFormat, DataSizeTraditionalFormat, DataSizeSIFormat }`

**作用与语义：**

规定数据量的表示格式。
- `QLocale::DataSizeIecFormat`：`0`;采用1024基础和IEC前缀的格式：KiB、MiB、GiB、......
- `QLocale::DataSizeTraditionalFormat`：`DataSizeSIQuantifiers`;采用1024进制和国际单位制前缀格式：kB、MB、GB、...
- `QLocale::DataSizeSIFormat`：`DataSizeBase1000 | DataSizeSIQuantifiers`;格式采用1000进制和国际单位制前缀：kB、MB、GB、...
DataSizeFormats 类型是 QFlags 的 typedef<DataSizeFormat>。它存储 DataSizeFormat 值的 OR 组合。

### `flags DataSizeFormats`

**作用与语义：**

规定数据量的表示格式。
- `QLocale::DataSizeIecFormat`：`0`;采用1024基础和IEC前缀的格式：KiB、MiB、GiB、......
- `QLocale::DataSizeTraditionalFormat`：`DataSizeSIQuantifiers`;采用1024进制和国际单位制前缀格式：kB、MB、GB、...
- `QLocale::DataSizeSIFormat`：`DataSizeBase1000 | DataSizeSIQuantifiers`;格式采用1000进制和国际单位制前缀：kB、MB、GB、...
DataSizeFormats 类型是 QFlags 的 typedef<DataSizeFormat>。它存储 DataSizeFormat 值的 OR 组合。

### `enum LanguageCodeType { ISO639Part1, ISO639Part2B, ISO639Part2T, ISO639Part3, LegacyLanguageCode, …, AnyLanguageCode }`

**作用与语义：**

该枚举定义了可以用于限制 `codeToLanguage` 和 `languageToCode` 所考虑的语言代码集合的语言代码类型。
- `QLocale::ISO639Part1`: `1 << 0`；ISO 639 第一部分 Alpha 2 代码。
- `QLocale::ISO639Part2B`: `1 << 1`；ISO 639 第二部分文献用 Alpha 3 代码。
- `QLocale::ISO639Part2T`: `1 << 2`；ISO 639 第二部分术语用 Alpha 3 代码。
- `QLocale::ISO639Part3`: `1 << 3`；ISO 639 第三部分 Alpha 3 代码。
- `QLocale::LegacyLanguageCode`: `1 << 15`；不属于上述集合的代码，但过去由 Qt 支持。此值只能由 `codeToLanguage()` 使用。传递给 `languageToCode()` 时将被忽略。
- `QLocale::ISO639Part2`: `ISO639Part2B | ISO639Part2T`；任何 ISO 639 第二部分代码。
- `QLocale::ISO639Alpha2`: `ISO639Part1`；任何 ISO-639 2 字母代码。
- `QLocale::ISO639Alpha3`: `ISO639Part2 | ISO639Part3`；任何 ISO-639 3 字母代码。
- `QLocale::ISO639`: `ISO639Alpha2 | ISO639Alpha3`；任何 ISO 639 代码。
- `QLocale::AnyLanguageCode`: `-1`；指定可以使用任何代码。
LanguageCodeTypes 类型是 QFlags<LanguageCodeType> 的类型定义。它存储 LanguageCodeType 值的 OR 组合。

### `flags LanguageCodeTypes`

**作用与语义：**

该枚举定义了可以用于限制 `codeToLanguage` 和 `languageToCode` 所考虑的语言代码集合的语言代码类型。
- `QLocale::ISO639Part1`: `1 << 0`；ISO 639 第一部分 Alpha 2 代码。
- `QLocale::ISO639Part2B`: `1 << 1`；ISO 639 第二部分文献用 Alpha 3 代码。
- `QLocale::ISO639Part2T`: `1 << 2`；ISO 639 第二部分术语用 Alpha 3 代码。
- `QLocale::ISO639Part3`: `1 << 3`；ISO 639 第三部分 Alpha 3 代码。
- `QLocale::LegacyLanguageCode`: `1 << 15`；不属于上述集合的代码，但过去由 Qt 支持。此值只能由 `codeToLanguage()` 使用。传递给 `languageToCode()` 时将被忽略。
- `QLocale::ISO639Part2`: `ISO639Part2B | ISO639Part2T`；任何 ISO 639 第二部分代码。
- `QLocale::ISO639Alpha2`: `ISO639Part1`；任何 ISO-639 2 字母代码。
- `QLocale::ISO639Alpha3`: `ISO639Part2 | ISO639Part3`；任何 ISO-639 3 字母代码。
- `QLocale::ISO639`: `ISO639Alpha2 | ISO639Alpha3`；任何 ISO 639 代码。
- `QLocale::AnyLanguageCode`: `-1`；指定可以使用任何代码。
LanguageCodeTypes 类型是 QFlags<LanguageCodeType> 的类型定义。它存储 LanguageCodeType 值的 OR 组合。

### `enum NumberOption { DefaultNumberOptions, OmitGroupSeparator, RejectGroupSeparator, OmitLeadingZeroInExponent, RejectLeadingZeroInExponent, …, RejectTrailingZeroesAfterDot }`

**作用与语义：**

该枚举定义了一组用于数字到字符串和字符串到数字转换的选项。它们可以用`numberOptions()`检索，也可以用`setNumberOptions()`设置。
- `QLocale::DefaultNumberOptions`：`0x0`;该选项代表除C区域外所有区域的默认行为，带有群分隔符，前方一个零位于个位数指数中，且在分数部分末尾无尾随零（存在时）。
- `QLocale::OmitGroupSeparator`：`0x01`;如果设置了这个选项，数字到字符串的函数不会将数字拆分成组。C locale 默认设置了这个选项。其他所有区域的默认是将数字拆分成组，在数字的整数部分，并使用组分隔符。
- `QLocale::RejectGroupSeparator`：`0x02`;如果设置了这个选项，字符串转数字函数如果在输入中遇到群分隔符，就会失败。默认情况下，接受包含正确放置的群分隔符的数字。
- `QLocale::OmitLeadingZeroInExponent`：`0x04`;如果设置了该选项，数字转字符串函数在用科学记号法打印浮点数时不会用零填充指数。默认是将一个前置零加到个位数指数。
- `QLocale::RejectLeadingZeroInExponent`：`0x08`;如果设置了该选项，字符串转数字函数在科学记谱法解析浮点数时遇到带零的指数时将失败。默认情况下接受此类填充。
- `QLocale::IncludeTrailingZeroesAfterDot`：`0x10`;如果设置了这个选项，数字到字符串函数会在“g”或“最简洁”模式下，将带零的数字填充到所需的精度。默认情况下省略尾随的零，这可能导致分数部分留下的数字比要求的精度少。
- `QLocale::RejectTrailingZeroesAfterDot`：`0x20`;如果设置了这个选项，字符串转数字函数在解析科学或十进制表示时，如果在分数部分末尾遇到尾随零，就会失败。默认情况下接受尾随零。
NumberOptions 类型是 QFlag 的 typedef<NumberOption>。它存储 NumberOption 值的 OR 组合。

### `flags NumberOptions`

**作用与语义：**

该枚举定义了一组用于数字到字符串和字符串到数字转换的选项。它们可以用`numberOptions()`检索，也可以用`setNumberOptions()`设置。
- `QLocale::DefaultNumberOptions`：`0x0`;该选项代表除C区域外所有区域的默认行为，带有群分隔符，前方一个零位于个位数指数中，且在分数部分末尾无尾随零（存在时）。
- `QLocale::OmitGroupSeparator`：`0x01`;如果设置了这个选项，数字到字符串的函数不会将数字拆分成组。C locale 默认设置了这个选项。其他所有区域的默认是将数字拆分成组，在数字的整数部分，并使用组分隔符。
- `QLocale::RejectGroupSeparator`：`0x02`;如果设置了这个选项，字符串转数字函数如果在输入中遇到群分隔符，就会失败。默认情况下，接受包含正确放置的群分隔符的数字。
- `QLocale::OmitLeadingZeroInExponent`：`0x04`;如果设置了该选项，数字转字符串函数在用科学记号法打印浮点数时不会用零填充指数。默认是将一个前置零加到个位数指数。
- `QLocale::RejectLeadingZeroInExponent`：`0x08`;如果设置了该选项，字符串转数字函数在科学记谱法解析浮点数时遇到带零的指数时将失败。默认情况下接受此类填充。
- `QLocale::IncludeTrailingZeroesAfterDot`：`0x10`;如果设置了这个选项，数字到字符串函数会在“g”或“最简洁”模式下，将带零的数字填充到所需的精度。默认情况下省略尾随的零，这可能导致分数部分留下的数字比要求的精度少。
- `QLocale::RejectTrailingZeroesAfterDot`：`0x20`;如果设置了这个选项，字符串转数字函数在解析科学或十进制表示时，如果在分数部分末尾遇到尾随零，就会失败。默认情况下接受尾随零。
NumberOptions 类型是 QFlag 的 typedef<NumberOption>。它存储 NumberOption 值的 OR 组合。

### `Territory`

**作用与语义：**

该枚举类型是`Country`的别名，未来发布时将更名为Territory。

### `QString toString(int number, int fieldWidth, char32_t fillChar) const`

**作用与语义：**

返回给定`number`的字符串表示。
字符串的长度至少为`fieldWidth`的绝对值，如果`number`位数较少，则使用`fillChar`作为填充。如果`fillChar` `'0'`该位置的零位数字作为填充。如果`fieldWidth`为负，字符串从其表示`number`开始，如果较短，则填充至长度`-fieldWidth`，并以给定`fillChar`。对于正fieldWidth，填充出现在`number`表示之前。当`number`为负且`fieldWidth`为正时，若`fillChar`为`'0'`，填充会插入该位置的负号与数字数字开头之间。

### `QString toString(short number, int fieldWidth, char32_t fillChar) const`

**作用与语义：**

返回给定`number`的字符串表示。
字符串的长度至少应为`fieldWidth`的绝对值，如果`number`位数较少，则使用`fillChar`作为填充。如果`fillChar` `'0'`该位置的零位数字作为填充。如果`fieldWidth`为负，字符串从其表示的 `number` 开始，若较短，则填充至长度`-fieldWidth`，并用给定的`fillChar`。对于正场宽，填充出现在`number`表示之前。

### `QString toString(uint number, int fieldWidth, char32_t fillChar) const`

**作用与语义：**

返回给定`number`的字符串表示。
字符串的长度至少应为`fieldWidth`的绝对值，如果`number`位数较少，则使用`fillChar`作为填充。如果`fillChar` `'0'`该位置的零位数字作为填充。如果`fieldWidth`为负，字符串从其表示的 `number` 开始，若较短，则填充至长度`-fieldWidth`，并用给定的`fillChar`。对于正场宽，填充出现在`number`表示之前。

### `QString toString(ushort number, int fieldWidth, char32_t fillChar) const`

**作用与语义：**

返回给定`number`的字符串表示。
字符串的长度至少应为`fieldWidth`的绝对值，如果`number`位数较少，则使用`fillChar`作为填充。如果`fillChar` `'0'`该位置的零位数字作为填充。如果`fieldWidth`为负，字符串从其表示的 `number` 开始，若较短，则填充至长度`-fieldWidth`，并用给定的`fillChar`。对于正场宽，填充出现在`number`表示之前。

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

`QLocale` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
