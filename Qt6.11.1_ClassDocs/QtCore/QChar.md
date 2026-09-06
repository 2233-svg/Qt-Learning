# QChar

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QChar` 是 Qt 的值类型，围绕“Char”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QChar` 是 Qt 值类型与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QChar>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Category { Mark_NonSpacing, Mark_SpacingCombining, Mark_Enclosing, Number_DecimalDigit, Number_Letter, …, Symbol_Other }`
- `enum Decomposition { NoDecomposition, Canonical, Circle, Compat, Final, …, Wide }`
- `enum Direction { DirAL, DirAN, DirB, DirBN, DirCS, …, DirWS }`
- `enum JoiningType { Joining_None, Joining_Causing, Joining_Dual, Joining_Right, Joining_Left, Joining_Transparent }`
- `enum Script { Script_Unknown, Script_Inherited, Script_Common, Script_Adlam, Script_Ahom, …, Script_ZanabazarSquare }`
- `enum SpecialCharacter { Null, Tabulation, LineFeed, FormFeed, CarriageReturn, …, LastValidCodePoint }`
- `enum UnicodeVersion { Unicode_1_1, Unicode_2_0, Unicode_2_1_2, Unicode_3_0, Unicode_3_1, …, Unicode_Unassigned }`

### 公有函数

- `QChar()`
- `QChar(QChar::SpecialCharacter ch)`
- `QChar(QLatin1Char ch)`
- `QChar(char ch)`
- `QChar(char16_t ch)`
- `QChar(char32_t code)`
- `QChar(int code)`
- `QChar(short code)`
- `QChar(uchar ch)`
- `QChar(uint code)`
- `QChar(ushort code)`
- `QChar(wchar_t ch)`
- `QChar(uchar cell, uchar row)`
- `QChar::Category category() const`
- `uchar cell() const`
- `unsigned char combiningClass() const`
- `QString decomposition() const`
- `QChar::Decomposition decompositionTag() const`
- `int digitValue() const`
- `QChar::Direction direction() const`
- `bool hasMirrored() const`
- `bool isDigit() const`
- `bool isHighSurrogate() const`
- `bool isLetter() const`
- `bool isLetterOrNumber() const`
- `bool isLowSurrogate() const`
- `bool isLower() const`
- `bool isMark() const`
- `bool isNonCharacter() const`
- `bool isNull() const`
- `bool isNumber() const`
- `bool isPrint() const`
- `bool isPunct() const`
- `bool isSpace() const`
- `bool isSurrogate() const`
- `bool isSymbol() const`
- `bool isTitleCase() const`
- `bool isUpper() const`
- `QChar::JoiningType joiningType() const`
- `QChar mirroredChar() const`
- `uchar row() const`
- `QChar::Script script() const`
- `QChar toCaseFolded() const`
- `char toLatin1() const`
- `QChar toLower() const`
- `QChar toTitleCase() const`
- `QChar toUpper() const`
- `char16_t & unicode()`
- `char16_t unicode() const`
- `QChar::UnicodeVersion unicodeVersion() const`

### 静态公有成员

- `QChar::Category category(char32_t ucs4)`
- `unsigned char combiningClass(char32_t ucs4)`
- `QChar::UnicodeVersion currentUnicodeVersion()`
- `QString decomposition(char32_t ucs4)`
- `QChar::Decomposition decompositionTag(char32_t ucs4)`
- `int digitValue(char32_t ucs4)`
- `QChar::Direction direction(char32_t ucs4)`
- `QChar fromLatin1(char c)`
- `(since 6.0) QChar fromUcs2(char16_t c)`
- `(since 6.0) auto fromUcs4(char32_t c)`
- `bool hasMirrored(char32_t ucs4)`
- `char16_t highSurrogate(char32_t ucs4)`
- `bool isDigit(char32_t ucs4)`
- `bool isHighSurrogate(char32_t ucs4)`
- `bool isLetter(char32_t ucs4)`
- `bool isLetterOrNumber(char32_t ucs4)`
- `bool isLowSurrogate(char32_t ucs4)`
- `bool isLower(char32_t ucs4)`
- `bool isMark(char32_t ucs4)`
- `bool isNonCharacter(char32_t ucs4)`
- `bool isNumber(char32_t ucs4)`
- `bool isPrint(char32_t ucs4)`
- `bool isPunct(char32_t ucs4)`
- `bool isSpace(char32_t ucs4)`
- `bool isSurrogate(char32_t ucs4)`
- `bool isSymbol(char32_t ucs4)`
- `bool isTitleCase(char32_t ucs4)`
- `bool isUpper(char32_t ucs4)`
- `QChar::JoiningType joiningType(char32_t ucs4)`
- `char16_t lowSurrogate(char32_t ucs4)`
- `char32_t mirroredChar(char32_t ucs4)`
- `bool requiresSurrogates(char32_t ucs4)`
- `QChar::Script script(char32_t ucs4)`
- `char32_t surrogateToUcs4(char16_t high, char16_t low)`
- `char32_t surrogateToUcs4(QChar high, QChar low)`
- `char32_t toCaseFolded(char32_t ucs4)`
- `char32_t toLower(char32_t ucs4)`
- `char32_t toTitleCase(char32_t ucs4)`
- `char32_t toUpper(char32_t ucs4)`
- `QChar::UnicodeVersion unicodeVersion(char32_t ucs4)`

### 相关非成员函数

- `bool operator!=(const QChar &c1, const QChar &c2)`
- `bool operator<(const QChar &c1, const QChar &c2)`
- `QDataStream & operator<<(QDataStream &out, QChar chr)`
- `bool operator<=(const QChar &c1, const QChar &c2)`
- `bool operator==(const QChar &c1, const QChar &c2)`
- `bool operator>(const QChar &c1, const QChar &c2)`
- `bool operator>=(const QChar &c1, const QChar &c2)`
- `QDataStream & operator>>(QDataStream &in, QChar &chr)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QChar::Category`

**作用与语义：**

该枚举映射了 Unicode 字符类别。
以下字符在Unicode中是规范字符：
- `QChar::Mark_NonSpacing`：`0`;Unicode 类名 Mn
- `QChar::Mark_SpacingCombining`：`1`;Unicode 类名 Mc
- `QChar::Mark_Enclosing`：`2`;Unicode 类名 Me
- `QChar::Number_DecimalDigit`：`3`;Unicode 类名 Nd
- `QChar::Number_Letter`：`4`;Unicode 类名 Nl
- `QChar::Number_Other`：`5`;Unicode 类名 No
- `QChar::Separator_Space`：`6`;Unicode 类名 Zs
- `QChar::Separator_Line`：`7`;Unicode 类名 Zl
- `QChar::Separator_Paragraph`：`8`;Unicode 类名 Zp
- `QChar::Other_Control`：`9`;Unicode 类名 Cc
- `QChar::Other_Format`：`10`;Unicode 类名 Cf
- `QChar::Other_Surrogate`：`11`;Unicode 类名 Cs
- `QChar::Other_PrivateUse`：`12`;Unicode 类名 Co
- `QChar::Other_NotAssigned`：`13`;Unicode 类名 Cn
以下类别在Unicode中具有信息价值：
- `QChar::Letter_Uppercase`：`14`;Unicode 类名 Lu
- `QChar::Letter_Lowercase`：`15`;Unicode 类名 Ll
- `QChar::Letter_Titlecase`：`16`;Unicode 类名 Lt（Lt）
- `QChar::Letter_Modifier`：`17`;Unicode 类名 Lm
- `QChar::Letter_Other`：`18`;Unicode 类名 Lo
- `QChar::Punctuation_Connector`：`19`;Unicode 类名 Pc
- `QChar::Punctuation_Dash`：`20`;Unicode 类名 Pd
- `QChar::Punctuation_Open`：`21`;Unicode 类名 Ps
- `QChar::Punctuation_Close`：`22`;Unicode 类名 Pe
- `QChar::Punctuation_InitialQuote`：`23`;Unicode 类名 Pi
- `QChar::Punctuation_FinalQuote`：`24`;Unicode 类名 Pf
- `QChar::Punctuation_Other`：`25`;Unicode 类名 Po
- `QChar::Symbol_Math`：`26`;Unicode 类名 Sm
- `QChar::Symbol_Currency`：`27`;Unicode 类名 Sc。
- `QChar::Symbol_Modifier`：`28`;Unicode 类名 Sk
- `QChar::Symbol_Other`：`29`;Unicode 类名 So

### `enum QChar::Decomposition`

**作用与语义：**

该枚举类型定义了Unicode分解属性。有关数值的描述，请参见Unicode标准。
- `QChar::NoDecomposition`：`0`
- `QChar::Canonical`：`1`
- `QChar::Circle`：`8`
- `QChar::Compat`：`16`
- `QChar::Final`：`6`
- `QChar::Font`：`2`
- `QChar::Fraction`：`17`
- `QChar::Initial`：`4`
- `QChar::Isolated`：`7`
- `QChar::Medial`：`5`
- `QChar::Narrow`：`13`
- `QChar::NoBreak`：`3`
- `QChar::Small`：`14`
- `QChar::Square`：`15`
- `QChar::Sub`：`10`
- `QChar::Super`：`9`
- `QChar::Vertical`：`11`
- `QChar::Wide`：`12`

### `enum QChar::Direction`

**作用与语义：**

该枚举类型定义了Unicode方向属性。有关值的描述，请参见Unicode标准。
为了符合 C/C 命名规范，Unicode 标准中使用的代码前加上了“Dir”。
- `QChar::DirAL`：`13`
- `QChar::DirAN`：`5`
- `QChar::DirB`：`7`
- `QChar::DirBN`：`18`
- `QChar::DirCS`：`6`
- `QChar::DirEN`：`2`
- `QChar::DirES`：`3`
- `QChar::DirET`：`4`
- `QChar::DirFSI (since Qt 5.3)`：`21`
- `QChar::DirL`：`0`
- `QChar::DirLRE`：`11`
- `QChar::DirLRI (since Qt 5.3)`：`19`
- `QChar::DirLRO`：`12`
- `QChar::DirNSM`：`17`
- `QChar::DirON`：`10`
- `QChar::DirPDF`：`16`
- `QChar::DirPDI (since Qt 5.3)`：`22`
- `QChar::DirR`：`1`
- `QChar::DirRLE`：`14`
- `QChar::DirRLI (since Qt 5.3)`：`20`
- `QChar::DirRLO`：`15`
- `QChar::DirS`：`8`
- `QChar::DirWS`：`9`

### `enum QChar::JoiningType`

**作用与语义：**

自5.3版本以来。
该枚举类型定义了Unicode连接类型属性。有关值的描述，请参见Unicode标准。
为了符合 C/C 命名规范，Unicode 标准中使用的代码前加上了“Joining_”。
- `QChar::Joining_None`：`0`
- `QChar::Joining_Causing`：`1`
- `QChar::Joining_Dual`：`2`
- `QChar::Joining_Right`：`3`
- `QChar::Joining_Left`：`4`
- `QChar::Joining_Transparent`：`5`

### `enum QChar::Script`

**作用与语义：**

该枚举类型定义了Unicode脚本的属性值。
有关Unicode文字属性值的详细信息，请参见Unicode标准附录#24。
为了符合 C/C 命名规范，Unicode 标准中使用的代码前加上“Script_”。
- `QChar::Script_Unknown`：`0`;用于未分配、私人使用、非字符和替代代码点。
- `QChar::Script_Inherited`：`1`;适用于可与多个脚本共用且继承前一个字符的字符。这些包括非间距标记、封闭标记以及零宽度连接/非连接字符。
- `QChar::Script_Common`：`2`;适用于可与多个脚本共用且不继承前一字符的字符。
- `QChar::Script_Adlam (since Qt 5.11)`：`132`
- `QChar::Script_Ahom (since Qt 5.6)`：`126`
- `QChar::Script_AnatolianHieroglyphs (since Qt 5.6)`：`127`
- `QChar::Script_Arabic`：`8`
- `QChar::Script_Armenian`：`6`
- `QChar::Script_Avestan`：`80`
- `QChar::Script_Balinese`：`62`
- `QChar::Script_Bamum`：`84`
- `QChar::Script_BassaVah (since Qt 5.5)`：`104`
- `QChar::Script_Batak`：`93`
- `QChar::Script_Bengali`：`12`
- `QChar::Script_BeriaErfe (since Qt 6.11)`：`174`
- `QChar::Script_Bhaiksuki (since Qt 5.11)`：`133`
- `QChar::Script_Bopomofo`：`36`
- `QChar::Script_Brahmi`：`94`
- `QChar::Script_Braille`：`54`
- `QChar::Script_Buginese`：`55`
- `QChar::Script_Buhid`：`44`
- `QChar::Script_CanadianAboriginal`：`29`
- `QChar::Script_Carian`：`75`
- `QChar::Script_CaucasianAlbanian (since Qt 5.5)`：`103`
- `QChar::Script_Chakma`：`96`
- `QChar::Script_Cham`：`77`
- `QChar::Script_Cherokee`：`28`
- `QChar::Script_Chorasmian (since Qt 5.15)`：`153`
- `QChar::Script_Coptic`：`46`
- `QChar::Script_Cuneiform`：`63`
- `QChar::Script_Cypriot`：`53`
- `QChar::Script_CyproMinoan (since Qt 6.3)`：`157`
- `QChar::Script_Cyrillic`：`5`
- `QChar::Script_Deseret`：`41`
- `QChar::Script_Devanagari`：`11`
- `QChar::Script_DivesAkuru (since Qt 5.15)`：`154`
- `QChar::Script_Dogra (since Qt 5.15)`：`142`
- `QChar::Script_Duployan (since Qt 5.5)`：`105`
- `QChar::Script_EgyptianHieroglyphs`：`81`
- `QChar::Script_Elbasan (since Qt 5.5)`：`106`
- `QChar::Script_Elymaic (since Qt 5.15)`：`149`
- `QChar::Script_Ethiopic`：`27`
- `QChar::Script_Garay (since Qt 6.9)`：`164`
- `QChar::Script_Georgian`：`25`
- `QChar::Script_Glagolitic`：`57`
- `QChar::Script_Gothic`：`40`
- `QChar::Script_Grantha (since Qt 5.5)`：`107`
- `QChar::Script_Greek`：`4`
- `QChar::Script_Gujarati`：`14`
- `QChar::Script_GunjalaGondi (since Qt 5.15)`：`143`
- `QChar::Script_Gurmukhi`：`13`
- `QChar::Script_GurungKhema (since Qt 6.9)`：`165`
- `QChar::Script_Han`：`37`
- `QChar::Script_Hangul`：`26`
- `QChar::Script_HanifiRohingya (since Qt 5.15)`：`144`
- `QChar::Script_Hanunoo`：`43`
- `QChar::Script_Hatran (since Qt 5.6)`：`128`
- `QChar::Script_Hebrew`：`7`
- `QChar::Script_Hiragana`：`34`
- `QChar::Script_ImperialAramaic`：`87`
- `QChar::Script_InscriptionalPahlavi`：`90`
- `QChar::Script_InscriptionalParthian`：`89`
- `QChar::Script_Javanese`：`85`
- `QChar::Script_Kaithi`：`92`
- `QChar::Script_Kannada`：`18`
- `QChar::Script_Katakana`：`35`
- `QChar::Script_Kawi (since Qt 6.5)`：`162`
- `QChar::Script_KayahLi`：`72`
- `QChar::Script_Kharoshthi`：`61`
- `QChar::Script_KhitanSmallScript (since Qt 5.15)`：`155`
- `QChar::Script_Khmer`：`32`
- `QChar::Script_Khojki (since Qt 5.5)`：`109`
- `QChar::Script_Khudawadi (since Qt 5.5)`：`123`
- `QChar::Script_KiratRai (since Qt 6.9)`：`166`
- `QChar::Script_Lao`：`22`
- `QChar::Script_Latin`：`3`
- `QChar::Script_Lepcha`：`68`
- `QChar::Script_Limbu`：`47`
- `QChar::Script_LinearA (since Qt 5.5)`：`110`
- `QChar::Script_LinearB`：`49`
- `QChar::Script_Lisu`：`83`
- `QChar::Script_Lycian`：`74`
- `QChar::Script_Lydian`：`76`
- `QChar::Script_Mahajani (since Qt 5.5)`：`111`
- `QChar::Script_Makasar (since Qt 5.15)`：`145`
- `QChar::Script_Malayalam`：`19`
- `QChar::Script_Mandaic`：`95`
- `QChar::Script_Manichaean (since Qt 5.5)`：`112`
- `QChar::Script_Marchen (since Qt 5.11)`：`134`
- `QChar::Script_MasaramGondi (since Qt 5.11)`：`138`
- `QChar::Script_Medefaidrin (since Qt 5.15)`：`146`
- `QChar::Script_MeeteiMayek`：`86`
- `QChar::Script_MendeKikakui (since Qt 5.5)`：`113`
- `QChar::Script_MeroiticCursive`：`97`
- `QChar::Script_MeroiticHieroglyphs`：`98`
- `QChar::Script_Miao`：`99`
- `QChar::Script_Modi (since Qt 5.5)`：`114`
- `QChar::Script_Mongolian`：`33`
- `QChar::Script_Mro (since Qt 5.5)`：`115`
- `QChar::Script_Multani (since Qt 5.6)`：`129`
- `QChar::Script_Myanmar`：`24`
- `QChar::Script_Nabataean (since Qt 5.5)`：`117`
- `QChar::Script_NagMundari (since Qt 6.3)`：`163`
- `QChar::Script_Nandinagari (since Qt 5.15)`：`150`
- `QChar::Script_Newa (since Qt 5.11)`：`135`
- `QChar::Script_NewTaiLue`：`56`
- `QChar::Script_Nko`：`66`
- `QChar::Script_Nushu (since Qt 5.11)`：`139`
- `QChar::Script_NyiakengPuachueHmong (since Qt 5.15)`：`151`
- `QChar::Script_Ogham`：`30`
- `QChar::Script_OlChiki`：`69`
- `QChar::Script_OlOnal (since Qt 6.9)`：`167`
- `QChar::Script_OldHungarian (since Qt 5.6)`：`130`
- `QChar::Script_OldItalic`：`39`
- `QChar::Script_OldNorthArabian (since Qt 5.5)`：`116`
- `QChar::Script_OldPermic (since Qt 5.5)`：`120`
- `QChar::Script_OldPersian`：`60`
- `QChar::Script_OldSogdian (since Qt 5.15)`：`147`
- `QChar::Script_OldSouthArabian`：`88`
- `QChar::Script_OldTurkic`：`91`
- `QChar::Script_OldUyghur (since Qt 6.3)`：`158`
- `QChar::Script_Oriya`：`15`
- `QChar::Script_Osage (since Qt 5.11)`：`136`
- `QChar::Script_Osmanya`：`52`
- `QChar::Script_PahawhHmong (since Qt 5.5)`：`108`
- `QChar::Script_Palmyrene (since Qt 5.5)`：`118`
- `QChar::Script_PauCinHau (since Qt 5.5)`：`119`
- `QChar::Script_PhagsPa`：`65`
- `QChar::Script_Phoenician`：`64`
- `QChar::Script_PsalterPahlavi (since Qt 5.5)`：`121`
- `QChar::Script_Rejang`：`73`
- `QChar::Script_Runic`：`31`
- `QChar::Script_Samaritan`：`82`
- `QChar::Script_Saurashtra`：`71`
- `QChar::Script_Sharada`：`100`
- `QChar::Script_Shavian`：`51`
- `QChar::Script_Siddham (since Qt 5.5)`：`122`
- `QChar::Script_Sidetic (since Qt 6.11)`：`171`
- `QChar::Script_SignWriting (since Qt 5.6)`：`131`
- `QChar::Script_Sinhala`：`20`
- `QChar::Script_Sogdian (since Qt 5.15)`：`148`
- `QChar::Script_SoraSompeng`：`101`
- `QChar::Script_Soyombo (since Qt 5.11)`：`140`
- `QChar::Script_Sundanese`：`67`
- `QChar::Script_Sunuwar (since Qt 6.9)`：`168`
- `QChar::Script_SylotiNagri`：`59`
- `QChar::Script_Syriac`：`9`
- `QChar::Script_Tagalog`：`42`
- `QChar::Script_Tagbanwa`：`45`
- `QChar::Script_TaiLe`：`48`
- `QChar::Script_TaiTham`：`78`
- `QChar::Script_TaiViet`：`79`
- `QChar::Script_TaiYo (since Qt 6.11)`：`172`
- `QChar::Script_Takri`：`102`
- `QChar::Script_Tamil`：`16`
- `QChar::Script_Tangut (since Qt 5.11)`：`137`
- `QChar::Script_Tangsa (since Qt 6.3)`：`159`
- `QChar::Script_Telugu`：`17`
- `QChar::Script_Thaana`：`10`
- `QChar::Script_Thai`：`21`
- `QChar::Script_Tibetan`：`23`
- `QChar::Script_Tifinagh`：`58`
- `QChar::Script_Tirhuta (since Qt 5.5)`：`124`
- `QChar::Script_Todhri (since Qt 6.9)`：`169`
- `QChar::Script_TolongSiki (since Qt 6.11)`：`173`
- `QChar::Script_Toto (since Qt 6.3)`：`160`
- `QChar::Script_TuluTigalari (since Qt 6.9)`：`170`
- `QChar::Script_Ugaritic`：`50`
- `QChar::Script_Vai`：`70`
- `QChar::Script_Vithkuqi (since Qt 6.3)`：`161`
- `QChar::Script_Wancho (since Qt 5.15)`：`152`
- `QChar::Script_WarangCiti (since Qt 5.5)`：`125`
- `QChar::Script_Yezidi (since Qt 5.15)`：`156`
- `QChar::Script_Yi`：`38`
- `QChar::Script_ZanabazarSquare (since Qt 5.11)`：`141`

### `enum QChar::UnicodeVersion`

**作用与语义：**

指定引入某一字符的Unicode标准版本。
- `QChar::Unicode_1_1`：`1`;版本1.1
- `QChar::Unicode_2_0`：`2`;版本2.0
- `QChar::Unicode_2_1_2`：`3`;版本 2.1.2
- `QChar::Unicode_3_0`：`4`;版本3.0
- `QChar::Unicode_3_1`：`5`;版本3.1
- `QChar::Unicode_3_2`：`6`;版本3.2
- `QChar::Unicode_4_0`：`7`;版本4.0
- `QChar::Unicode_4_1`：`8`;版本4.1
- `QChar::Unicode_5_0`：`9`;版本5.0
- `QChar::Unicode_5_1`：`10`;版本5.1
- `QChar::Unicode_5_2`：`11`;版本5.2
- `QChar::Unicode_6_0`：`12`;版本6.0
- `QChar::Unicode_6_1`：`13`;版本 6.1
- `QChar::Unicode_6_2`：`14`;版本6.2
- `QChar::Unicode_6_3 (since Qt 5.3)`：`15`;版本 6.3
- `QChar::Unicode_7_0 (since Qt 5.5)`：`16`;版本7.0
- `QChar::Unicode_8_0 (since Qt 5.6)`：`17`;版本8.0
- `QChar::Unicode_9_0 (since Qt 5.11)`：`18`;版本9.0
- `QChar::Unicode_10_0 (since Qt 5.11)`：`19`;版本10.0
- `QChar::Unicode_11_0 (since Qt 5.15)`：`20`;版本 11.0
- `QChar::Unicode_12_0 (since Qt 5.15)`：`21`;版本12.0
- `QChar::Unicode_12_1 (since Qt 5.15)`：`22`;版本12.1
- `QChar::Unicode_13_0 (since Qt 5.15)`：`23`;版本13.0
- `QChar::Unicode_14_0 (since Qt 6.3)`：`24`;版本14.0
- `QChar::Unicode_15_0 (since Qt 6.5)`：`25`;版本 15.0
- `QChar::Unicode_15_1 (since Qt 6.8)`：`26`;版本15.1
- `QChar::Unicode_16_0 (since Qt 6.9)`：`27`;版本16.0
- `QChar::Unicode_17_0 (since Qt 6.11)`：`28`;版本17.0
- `QChar::Unicode_Unassigned`：`0`;在Unicode 8.0版本中，该值不会分配给任何字符。

### `[constexpr noexcept] QChar::QChar()`

**作用与语义：**

构造一个空 QChar （'\0'）。

### `[constexpr noexcept] QChar::QChar(QChar::SpecialCharacter ch)`

**作用与语义：**

为预定义的字符值`ch`构造一个QChar。
注意：自 Qt 6.9 起，该构造函数禁用隐式转换。这意味着它只接受构造器参数类型，而非所有隐式转换为该类型的。向下兼容的解决方案是显式地转换为 QChar 构造器支持的参数类型之一。

### `[constexpr noexcept] QChar::QChar(QLatin1Char ch)`

**作用与语义：**

构建对应ASCII/拉丁-1字符`ch`的QChar。
注意：自 Qt 6.9 起，该构造函数禁用隐式转换。这意味着它只接受构造器参数类型，而非所有隐式转换为该类型的。向下兼容的解决方案是显式地转换为 QChar 构造器支持的参数类型之一。

### `[constexpr noexcept] QChar::QChar(char ch)`

**作用与语义：**

构建对应ASCII/拉丁-1字符`ch`的QChar。
注意：当`QT_NO_CAST_FROM_ASCII`定义时，该构造器不可用。
注意：自 Qt 6.9 起，该构造函数禁用隐式转换。这意味着它只接受构造器参数类型，而非所有隐式转换为该类型的。向下兼容的解决方案是显式地转换为 QChar 构造器支持的参数类型之一。

### `[constexpr noexcept] QChar::QChar(char16_t ch)`

**作用与语义：**

构建对应UTF-16字符`ch`的QChar。
注意：自 Qt 6.9 起，该构造函数禁用隐式转换。这意味着它只接受构造器参数类型，而非所有隐式转换为该类型的。向下兼容的解决方案是显式地转换为 QChar 构造器支持的参数类型之一。

### `[default] QChar::QChar(char32_t code)`

**作用与语义：**

为字符构建一个带有Unicode代码点`code`的QChar。
注意：自 Qt 6.9 起，该构造函数禁用隐式转换。这意味着它只接受构造器参数类型，而非所有隐式转换为该类型的。向下兼容的解决方案是显式地转换为 QChar 构造器支持的参数类型之一。

### `[explicit constexpr noexcept] QChar::QChar(int code)`

**作用与语义：**

为字符构建一个带有Unicode代码点`code`的QChar。
注意：自 Qt 6.9 起，该构造函数禁用隐式转换。这意味着它只接受构造器参数类型，而非所有隐式转换为该类型的。向下兼容的解决方案是显式地转换为 QChar 构造器支持的参数类型之一。

### `[constexpr noexcept] QChar::QChar(short code)`

**作用与语义：**

为字符构建一个带有Unicode代码点`code`的QChar。
注意：自 Qt 6.9 起，该构造函数禁用隐式转换。这意味着它只接受构造器参数类型，而非所有隐式转换为该类型的。向下兼容的解决方案是显式地转换为 QChar 构造器支持的参数类型之一。

### `[explicit constexpr noexcept] QChar::QChar(uchar ch)`

**作用与语义：**

构建对应ASCII/拉丁-1字符`ch`的QChar。
注意：当定义`QT_NO_CAST_FROM_ASCII`或 `QT_RESTRICTED_CAST_FROM_ASCII`时，该构造器不可用。
注意：自 Qt 6.9 起，该构造函数禁用隐式转换。这意味着它只接受构造器参数类型，而非所有隐式转换为该类型的。向下兼容的解决方案是显式地转换为 QChar 构造器支持的参数类型之一。

### `[explicit constexpr noexcept] QChar::QChar(uint code)`

**作用与语义：**

为字符构建一个带有Unicode代码点`code`的QChar。
注意：自 Qt 6.9 起，该构造函数禁用隐式转换。这意味着它只接受构造器参数类型，而非所有隐式转换为该类型的。向下兼容的解决方案是显式地转换为 QChar 构造器支持的参数类型之一。

### `[constexpr noexcept] QChar::QChar(ushort code)`

**作用与语义：**

为字符构建一个带有Unicode代码点`code`的QChar。
注意：自 Qt 6.9 起，该构造函数禁用隐式转换。这意味着它只接受构造器参数类型，而非所有隐式转换为该类型的。向下兼容的解决方案是显式地转换为 QChar 构造器支持的参数类型之一。

### `[constexpr noexcept] QChar::QChar(wchar_t ch)`

**作用与语义：**

构造对应宽字符`ch`的QChar。
注意：该构造器仅支持Windows。
注意：自 Qt 6.9 起，该构造函数禁用隐式转换。这意味着它只接受构造器参数类型，而非所有隐式转换为该类型的。向下兼容的解决方案是显式地转换为 QChar 构造器支持的参数类型之一。

### `[explicit constexpr noexcept] QChar::QChar(uchar cell, uchar row)`

**作用与语义：**

为第`row`行的Unicode单元格`cell`构建了QChar。

### `[noexcept] QChar::Category QChar::category() const`

**作用与语义：**

返回角色的类别。

### `[static noexcept] QChar::Category QChar::category(char32_t ucs4)`

**作用与语义：**

返回由`ucs4`指定的UCS-4编码字符的类别。
注意：在第6问答之前，该函数采用`uint`论元。

### `[constexpr noexcept] uchar QChar::cell() const`

**作用与语义：**

返回Unicode字符的单元格（最低有效字节）。

### `[noexcept] unsigned char QChar::combiningClass() const`

**作用与语义：**

返回 Unicode 标准定义的字符的组合类。这主要作为附加在基础字符上的标记定位提示。
Qt文本渲染引擎利用这些信息，正确定位基字符周围的非间距标记。

### `[static noexcept] unsigned char QChar::combiningClass(char32_t ucs4)`

**作用与语义：**

返回由 `ucs4` 指定的 UCS-4 编码字符的组合类，该字符定义在 Unicode 标准中。
注意：在Qt 6之前，该函数采用`uint`参数。

### `[static noexcept] QChar::UnicodeVersion QChar::currentUnicodeVersion()`

**作用与语义：**

返回最新支持的Unicode版本。

### `QString QChar::decomposition() const`

**作用与语义：**

将字符分解为其组成部分。如果不存在分解，则返回空字符串。

### `[static] QString QChar::decomposition(char32_t ucs4)`

**作用与语义：**

将 `ucs4` 指定的 UCS-4 编码字符分解为其组成部分。如果不存在分解，返回空字符串。
注：在第6Q之前，该函数采用`uint`参数。

### `[noexcept] QChar::Decomposition QChar::decompositionTag() const`

**作用与语义：**

返回定义角色组成的标签。如果不存在分解，返回`QChar::NoDecomposition`。

### `[static noexcept] QChar::Decomposition QChar::decompositionTag(char32_t ucs4)`

**作用与语义：**

返回定义由`ucs4`指定UCS-4编码字符组合的标签。如果不存在分解，返回`QChar::NoDecomposition`。
注：在第6问答之前，该函数采用`uint`论元。

### `[noexcept] int QChar::digitValue() const`

**作用与语义：**

返回数字的数值，如果字符不是数字，则返回-1。

### `[static noexcept] int QChar::digitValue(char32_t ucs4)`

**作用与语义：**

返回UCS-4编码字符指定的数字值，`ucs4`，如果不是数字则返回-1。
注意：在第6题之前，该函数采用了`uint`的论证。

### `[noexcept] QChar::Direction QChar::direction() const`

**作用与语义：**

返回角色的方向。

### `[static noexcept] QChar::Direction QChar::direction(char32_t ucs4)`

**作用与语义：**

返回由`ucs4`指定UCS-4编码字符的方向。
注：在第6问答之前，该函数采用`uint`参数。

### `[static constexpr noexcept] QChar QChar::fromLatin1(char c)`

**作用与语义：**

将拉丁字母1字符`c`转换为其等效`QChar`。这主要适用于非国际化软件。
另一种选择是使用`QLatin1Char`。

### `[static constexpr noexcept, since 6.0] QChar QChar::fromUcs2(char16_t c)`

**作用与语义：**

由UTF-16字符`c`构造`QChar`。

### `[static constexpr noexcept, since 6.0] auto QChar::fromUcs4(char32_t c)`

**作用与语义：**

返回一个匿名结构。
- 包含`char16_t chars[2]`数组，
- 可以隐式转换为`QStringView`，且
- 通过C 11的远距for循环进行迭代。
如果`c`需要代替，`chars[0]`包含高代体，`chars[1]`低代替，`QStringView`大小为2。否则，`chars[0]`包含`c`，`chars[1]`为`null`，`QStringView`大小为1。
这使得结果的使用变得非常方便：

**官方示例：**

```cpp
 QString s;
 s += QChar::fromUcs4(ch);
```

### `[noexcept] bool QChar::hasMirrored() const`

**作用与语义：**

返回`true`如果文本方向反转，字符是否应反转;否则返回`false`。
稍快的等价于（ch.`mirroredChar()` ！= ch）。

### `[static noexcept] bool QChar::hasMirrored(char32_t ucs4)`

**作用与语义：**

如果`ucs4`指定的UCS-4编码字符在文本方向反转时应反转，返回`true`;否则返回`false`。
稍快的等价物是 （`QChar::mirroredChar`（ucs4） ！= ucs4）。
注：在第6问之前，该函数采用`uint`论证。

### `[static constexpr noexcept] char16_t QChar::highSurrogate(char32_t ucs4)`

**作用与语义：**

返回UCS-4编码码点中的高代节点部分。如果`ucs4`小于0x10000，返回的结果为未定义。
注：在第6问答之前，该函数接受`uint`参数并返回`ushort`。

### `[constexpr noexcept] bool QChar::isDigit() const`

**作用与语义：**

如果字符是十进制数字（`Number_DecimalDigit`），返回`true`;否则返回`false`。

### `[static constexpr noexcept] bool QChar::isDigit(char32_t ucs4)`

**作用与语义：**

如果`ucs4`指定的UCS-4编码字符是十进制数字（`Number_DecimalDigit`），返回`true`;否则返回`false`。
注意：在第6问答之前，该函数采用`uint`论证。

### `[constexpr noexcept] bool QChar::isHighSurrogate() const`

**作用与语义：**

如果`QChar`是UTF16代理的最高部分（例如其码点在范围内[0xd800..0xdbff]）;否则返回`true`。

### `[static constexpr noexcept] bool QChar::isHighSurrogate(char32_t ucs4)`

**作用与语义：**

如果`ucs4`指定的UCS-4编码字符是UTF16代理的最高部分（例如其码点在范围内[0xd800..0xdbff]）;否则返回`true`。
注：在第6问之前，该函数采用了`uint`论元。

### `[constexpr noexcept] bool QChar::isLetter() const`

**作用与语义：**

如果字符是字母（Letter_*类别），返回`true`;否则返回`false`。

### `[static constexpr noexcept] bool QChar::isLetter(char32_t ucs4)`

**作用与语义：**

如果`ucs4`指定的UCS-4编码字符是字母（Letter_*类别），返回`true`;否则返回`false`。
注意：在第6题之前，该函数采用`uint`参数。

### `[constexpr noexcept] bool QChar::isLetterOrNumber() const`

**作用与语义：**

如果字符是字母或数字（Letter_*或Number_*类别），返回`true`;否则返回`false`。

### `[static constexpr noexcept] bool QChar::isLetterOrNumber(char32_t ucs4)`

**作用与语义：**

如果`ucs4`指定的UCS-4编码字符是字母或数字（Letter_*或Number_*类别），返回`true`;否则返回`false`。
注：在第6问答之前，该函数采用了`uint`的论元。

### `[constexpr noexcept] bool QChar::isLowSurrogate() const`

**作用与语义：**

如果`QChar`是UTF16代理的最低部分（例如其码点在范围内[0xdc00..0xdfff]）;否则返回`true`。

### `[static constexpr noexcept] bool QChar::isLowSurrogate(char32_t ucs4)`

**作用与语义：**

如果`ucs4`指定的UCS-4编码字符是UTF16代理的低端（例如其码点在范围内[0xdc00..0xdfff]）;否则返回`true`;否则为假。
注意：在第6问卷之前，该函数采用`uint`参数。

### `[constexpr noexcept] bool QChar::isLower() const`

**作用与语义：**

如果字符是小写字母，例如`category()`是`Letter_Lowercase`，则返回`true`。

### `[static constexpr noexcept] bool QChar::isLower(char32_t ucs4)`

**作用与语义：**

如果`ucs4`指定的UCS-4编码字符是小写字母，例如`category()`为`Letter_Lowercase`，返回`true`。
注意：在第6问答之前，该函数采用`uint`参数。

### `[noexcept] bool QChar::isMark() const`

**作用与语义：**

如果角色是标记（Mark_*类别），返回`true`;否则返回`false`。
有关评分的更多信息，请参见`QChar::Category`。

### `[static noexcept] bool QChar::isMark(char32_t ucs4)`

**作用与语义：**

如果由`ucs4`指定的UCS-4编码字符是标记（Mark_*类别），返回 `true`;否则返回 `false`。
注：在第6问之前，该函数采用了`uint`的参数。

### `[constexpr noexcept] bool QChar::isNonCharacter() const`

**作用与语义：**

如果`QChar`非字符，返回`true`;否则返回 false。
Unicode 有一定数量的代码点被归类为“非字符”：也就是说，它们可以在应用程序内部使用，但不能用于文本交换。这些是每个 Unicode 平面（[0xfffe..0xffff]、[0x1fffe..0x1ffff]等）的最后两个条目。以及范围内的条目 [0xfdd0..0xfdef]。

### `[static constexpr noexcept] bool QChar::isNonCharacter(char32_t ucs4)`

**作用与语义：**

如果`ucs4`指定的UCS-4编码字符是非字符，返回`true`;否则为假。
Unicode 有一定数量的代码点被归类为“非字符”：也就是说，它们可以在应用程序内部使用，但不能用于文本交换。这些是每个 Unicode 平面（[0xfffe..0xffff]、[0x1fffe..0x1ffff]等）的最后两个条目。以及范围内的条目 [0xfdd0..0xfdef]。
注：在第6题之前，该函数采用`uint`论元。

### `[constexpr noexcept] bool QChar::isNull() const`

**作用与语义：**

如果字符是 Unicode 字符 0x0000 （'\0'），则返回 `true`;否则返回 `false`。

### `[constexpr noexcept] bool QChar::isNumber() const`

**作用与语义：**

如果字符是数字（Number_*类别，而非仅0-9），返回`true`;否则返回`false`。

### `[static constexpr noexcept] bool QChar::isNumber(char32_t ucs4)`

**作用与语义：**

如果`ucs4`指定的UCS-4编码字符是一个数字（Number_*类别，而不仅仅是0-9），则返回`true`;否则返回`false`。
注：在第6题之前，该函数采用`uint`论证。

### `[noexcept] bool QChar::isPrint() const`

**作用与语义：**

如果该字符是可打印字符，返回`true`;否则返回 ，返回`false`。这是任何不属于`Other_`*类别的字符。
注意，这并不能说明该字符是否在特定字体中可用。

### `[static noexcept] bool QChar::isPrint(char32_t ucs4)`

**作用与语义：**

如果`ucs4`指定的UCS-4编码字符是可打印字符，返回`true`;否则返回`false`。这是任何非类别`Other_`*的字符。
注意，这并不能说明该字符是否在特定字体中可用。
注意：在第6问答之前，该函数需要`uint`论证。

### `[noexcept] bool QChar::isPunct() const`

**作用与语义：**

如果该字符是标点符号（Punctuation_* 类别），返回`true`;否则返回`false`。

### `[static noexcept] bool QChar::isPunct(char32_t ucs4)`

**作用与语义：**

如果`ucs4`指定的UCS-4编码字符是标点符号（Punctuation_*类别），返回`true`;否则返回`false`。
注：在Qt 6之前，该函数采用`uint`参数。

### `[constexpr noexcept] bool QChar::isSpace() const`

**作用与语义：**

如果字符是分隔符（Separator_*类别或`Other_Control`类别中的某些码点），返回`true`;否则返回`false`。

### `[static constexpr noexcept] bool QChar::isSpace(char32_t ucs4)`

**作用与语义：**

如果`ucs4`指定的UCS-4编码字符是分隔符（Separator_*类别或`Other_Control`类别中的某些码点），返回`true`;否则返回`false`。
注意：在第6问答之前，该函数采用`uint`论元。

### `[constexpr noexcept] bool QChar::isSurrogate() const`

**作用与语义：**

如果`QChar`包含位于UTF-16代理范围的高频或低频码点（例如，当其码点在[0xd800..0xdfff]范围内时，返回`true`）;否则为假。

### `[static constexpr noexcept] bool QChar::isSurrogate(char32_t ucs4)`

**作用与语义：**

如果由`ucs4`指定的UCS-4编码字符包含位于UTF-16替代范围的高频或低端的码点（例如，如果其码点在[0xd800..0xdfff]范围内），返回`true`;否则为假。
注：在第6题之前，该函数采用`uint`参数。

### `[noexcept] bool QChar::isSymbol() const`

**作用与语义：**

如果字符是符号（Symbol_*类别），返回`true`;否则返回`false`。

### `[static noexcept] bool QChar::isSymbol(char32_t ucs4)`

**作用与语义：**

如果由`ucs4`指定的UCS-4编码字符是符号（Symbol_*类别），返回 `true`;否则返回`false`。
注意：在第6问之前，该函数采用`uint`论元。

### `[constexpr noexcept] bool QChar::isTitleCase() const`

**作用与语义：**

如果字符是标题格字母，例如，`category()` 是`Letter_Titlecase`，则返回`true`。

### `[static constexpr noexcept] bool QChar::isTitleCase(char32_t ucs4)`

**作用与语义：**

如果`ucs4`指定的UCS-4编码字符是标题大小写，例如`category()`为`Letter_Titlecase`，返回`true`。
注意：在第6题之前，该函数采用`uint`参数。

### `[constexpr noexcept] bool QChar::isUpper() const`

**作用与语义：**

如果字符是大写字母，例如`category()`为`Letter_Uppercase`，则返回`true`。

### `[static constexpr noexcept] bool QChar::isUpper(char32_t ucs4)`

**作用与语义：**

如果`ucs4`指定的UCS-4编码字符是大写字母，例如`category()`为`Letter_Uppercase`，返回`true`。
注意：在Qt 6之前，该函数采用`uint`参数。

### `[noexcept] QChar::JoiningType QChar::joiningType() const`

**作用与语义：**

返回关于字符的连接类型属性的信息（某些语言如阿拉伯语或叙利亚语需要）。

### `[static noexcept] QChar::JoiningType QChar::joiningType(char32_t ucs4)`

**作用与语义：**

返回由`ucs4`指定、UCS-4编码字符的连接类型属性信息（某些语言如阿拉伯语或叙利亚语需要）。
注意：在第6问答之前，该函数采用了`uint`论元。

### `[static constexpr noexcept] char16_t QChar::lowSurrogate(char32_t ucs4)`

**作用与语义：**

返回UCS-4编码码点中的低代节点部分。如果`ucs4`小于0x10000，返回的结果为未定义。
注：在第6问答之前，该函数接收`uint`参数并返回`ushort`。

### `[noexcept] QChar QChar::mirroredChar() const`

**作用与语义：**

如果镜像字符是镜像字符，则返回该字符;否则返回字符本身。

### `[static noexcept] char32_t QChar::mirroredChar(char32_t ucs4)`

**作用与语义：**

如果`ucs4`指定的UCS-4编码字符是镜像字符，则返回镜像字符;否则返回字符本身。
注意：在第6问之前，该函数接收`uint`参数并返回`uint`。

### `[static constexpr noexcept] bool QChar::requiresSurrogates(char32_t ucs4)`

**作用与语义：**

如果`ucs4`指定的UCS-4编码字符可以拆分为UTF16代理的最高和低频部分（例如其码点大于或等于0x10000时），返回`true`;否则为假。
注：在第6题之前，该函数采用`uint`论证。

### `[constexpr noexcept] uchar QChar::row() const`

**作用与语义：**

返回Unicode字符的行（最高字节）。

### `[noexcept] QChar::Script QChar::script() const`

**作用与语义：**

返回该字符的Unicode脚本属性值。

### `[static noexcept] QChar::Script QChar::script(char32_t ucs4)`

**作用与语义：**

返回 UCS-4 编码形式中字符的 Unicode 脚本属性值，作为 `ucs4`。
注意：在第6问答之前，这个函数需要`uint`论证。

### `[static constexpr noexcept] char32_t QChar::surrogateToUcs4(char16_t high, char16_t low)`

**作用与语义：**

将UTF16代理对转换为其UCS-4编码的代码点，`high`和`low`值。
注意：在Qt 6之前，该函数接收`ushort`参数并返回`uint`。

### `[static constexpr noexcept] char32_t QChar::surrogateToUcs4(QChar high, QChar low)`

**作用与语义：**

将一对UTF16代理（`high`、`low`）转换为其UCS-4编码的代码点。
注：在第6Q之前，该函数返回`uint`。

### `[noexcept] QChar QChar::toCaseFolded() const`

**作用与语义：**

返回字符的大小写折叠等价值。对于大多数Unicode字符，这与`toLower()`相同。

### `[static noexcept] char32_t QChar::toCaseFolded(char32_t ucs4)`

**作用与语义：**

返回由`ucs4`指定的UCS-4编码字符的大小折叠等价值。对于大多数Unicode字符，这与`toLower()`相同。
注意：在第6问之前，该函数接受`uint`参数并返回`uint`。

### `[constexpr noexcept] char QChar::toLatin1() const`

**作用与语义：**

返回与 `QChar` 等价的拉丁字母 1 字符，即 0。这主要适用于非国际化软件。
注意：无法区分非拉丁-1字符和拉丁-1 0（NUL）字符。建议使用`unicode()`，因为它没有这种歧义。

### `[noexcept] QChar QChar::toLower() const`

**作用与语义：**

如果字符为大写或标题大写，则返回小写等价字符;否则返回字符本身。

### `[static noexcept] char32_t QChar::toLower(char32_t ucs4)`

**作用与语义：**

如果字符是大写或标题大小写，返回 `ucs4` 指定的 UCS-4 编码字符的小写等价值;否则返回字符本身。
注：在第6问答之前，该函数接受`uint`参数并返回`uint`。

### `[noexcept] QChar QChar::toTitleCase() const`

**作用与语义：**

如果字符是小写或大写，则返回标题大小写;否则返回字符本身。

### `[static noexcept] char32_t QChar::toTitleCase(char32_t ucs4)`

**作用与语义：**

如果字符是小写或大写，返回 `ucs4` 指定的 UCS-4 编码字符的标题大小写等价值;否则返回字符本身。
注：在第6问答之前，该函数接收`uint`参数并返回`uint`。

### `[noexcept] QChar QChar::toUpper() const`

**作用与语义：**

如果字符为小写或标题大小写，则返回大写等价字符;否则返回字符本身。
注意：该函数在极少数需要两个或以上字符的大写字符时，也会返回原始字符。

### `[static noexcept] char32_t QChar::toUpper(char32_t ucs4)`

**作用与语义：**

如果该字符为小写或标题大小写，返回由`ucs4`指定的UCS-4编码字符的大写等价值;否则返回字符本身。
注意：该函数在极少数需要两个或以上字符的大写字符时，也会返回原始字符。
注：在第6问答之前，该函数接受`uint`参数并返回`uint`。

### `[constexpr noexcept] char16_t &QChar::unicode()`

**作用与语义：**

返回`QChar`的数值Unicode值。

### `[constexpr noexcept] char16_t QChar::unicode() const`

**作用与语义：**

返回`QChar`的数值Unicode值。

### `[noexcept] QChar::UnicodeVersion QChar::unicodeVersion() const`

**作用与语义：**

返回引入该字符的Unicode版本。

### `[static noexcept] QChar::UnicodeVersion QChar::unicodeVersion(char32_t ucs4)`

**作用与语义：**

返回引入UCS-4编码形式字符的Unicode版本，作为`ucs4`。
注：在第6Q之前，该函数采用`uint`参数。

### `[constexpr noexcept] bool operator!=(const QChar &c1, const QChar &c2)`

**作用与语义：**

返回`true`如果`c1`和`c2`不是相同的 Unicode 字符；否则返回`false`.

### `[constexpr noexcept] bool operator<(const QChar &c1, const QChar &c2)`

**作用与语义：**

返回`true`如果数字 Unicode 值为`c1`小于`c2`; 否则返回 `false`.

### `QDataStream &operator<<(QDataStream &out, QChar chr)`

**作用与语义：**

将字符 `chr` 写入流 `out`。

### `[constexpr noexcept] bool operator<=(const QChar &c1, const QChar &c2)`

**作用与语义：**

如果 `c1` 的数字 Unicode 值小于或等于 `c2` 的数字 Unicode 值，则返回 `true`；否则返回 `false`。

### `[constexpr noexcept] bool operator==(const QChar &c1, const QChar &c2)`

**作用与语义：**

如果 `c1` 和 `c2` 是相同的 Unicode 字符，则返回 `true`；否则返回 `false`。

### `[constexpr noexcept] bool operator>(const QChar &c1, const QChar &c2)`

**作用与语义：**

如果 `c1` 的数字 Unicode 值大于 `c2` 的数字 Unicode 值，则返回 `true`；否则返回 `false`。

### `[constexpr noexcept] bool operator>=(const QChar &c1, const QChar &c2)`

**作用与语义：**

如果 `c1` 的数字 Unicode 值大于或等于 `c2`，则返回 `true`；否则返回 `false`。

### `QDataStream &operator>>(QDataStream &in, QChar &chr)`

**作用与语义：**

它会把溪流`in`的烧焦读成烧焦`chr`。

### `enum SpecialCharacter { Null, Tabulation, LineFeed, FormFeed, CarriageReturn, …, LastValidCodePoint }`

**作用与语义：**

- `QChar::Null`：`0x0000`;具有此值`isNull()`的`QChar`。
- `QChar::Tabulation`：`0x0009`;字符统计。
- `QChar::LineFeed`：`0x000a`
- `QChar::FormFeed`：`0x000c`
- `QChar::CarriageReturn`：`0x000d`
- `QChar::Space`：`0x0020`
- `QChar::Nbsp`：`0x00a0`;不间断的空格。
- `QChar::SoftHyphen`：`0x00ad`
- `QChar::ReplacementCharacter`：`0xfffd`;当字体没有某个码点的字形时显示的字符。通常会使用特殊的问号字符。当输入数据无法在Unicode中表示时，编解码器会使用该码点。
- `QChar::ObjectReplacementCharacter`：`0xfffc`;用于表示无法呈现的对象，如图像。
- `QChar::ByteOrderMark`：`0xfeff`
- `QChar::ByteOrderSwapped`：`0xfffe`
- `QChar::ParagraphSeparator`：`0x2029`
- `QChar::LineSeparator`：`0x2028`
- `QChar::VisualTabCharacter (since Qt 6.2)`：`0x2192`;用于将表格表示为水平箭头。
- `QChar::LastValidCodePoint`：`0x10ffff`

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QChar` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
