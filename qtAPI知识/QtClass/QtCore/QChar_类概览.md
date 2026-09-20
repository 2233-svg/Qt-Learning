# Qt QChar 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QChar>`  
> 所属模块：`Qt6::Core`  
> 核心定位：一个 UTF-16 代码单元及其 Unicode 属性查询工具

## 1. 先把三个概念分开

`QChar` 只有 16 位，保存的是一个 UTF-16 **代码单元**。它不是“任意 Unicode 码点”，更不是“用户眼中一个字符”。

```text
QChar              一个 UTF-16 code unit，范围 0x0000 到 0xFFFF
Unicode code point  一个码点，范围 0x0000 到 0x10FFFF
grapheme cluster    用户看到的一个字符，可能由多个码点组成
```

例如 U+1F600 的表情符号超过基本多文种平面，在 UTF-16 的 `QString` 中要由高代理项和低代理项两个 `QChar` 表示；带组合音标的文字、旗帜和部分 emoji 序列则可能由更多码点组成。

因此 `QChar` 解决的是：

- 逐个检查 `QString` 内的 UTF-16 单元。
- 查询 Unicode 分类、脚本、方向、大小写和数字属性。
- 在需要时手工处理 UTF-16 代理对。

它**不**适合按“用户可见字符数”截断文本，也不应单独存储辅助平面码点。

## 2. 最重要的边界：遍历 `QString` 不等于遍历 Unicode 码点

下面的循环会逐个读取 UTF-16 单元。对 BMP 字符很自然；遇到代理对时，一个实际码点会出现两次。

```cpp
for (QChar ch : text) {
    if (ch.isHighSurrogate()) {
        // 下一个 QChar 才可能组成完整的辅助平面码点。
    }
}
```

需要按 Unicode 码点处理时，先验证高、低代理项配对，再调用 `surrogateToUcs4()`：

```cpp
for (qsizetype i = 0; i < text.size(); ++i) {
    const QChar first = text.at(i);
    char32_t codePoint = first.unicode();

    if (first.isHighSurrogate()
        && i + 1 < text.size()
        && text.at(i + 1).isLowSurrogate()) {
        codePoint = QChar::surrogateToUcs4(first, text.at(++i));
    }

    inspectCodePoint(codePoint);
}
```

若需求是光标移动、删除一个“可见字符”或字符串计数，直接按码点也未必正确；应使用 `QTextBoundaryFinder`、`QStringView` 的合适算法或 Unicode grapheme cluster 规则。

## 3. 创建 `QChar`：优先表达编码意图

`QChar` 的构造函数很多，是为了兼容 C++ 字符类型，而不是鼓励把所有整数随便塞进去。Qt 6 已将多数整数构造变为 `explicit`，Qt 6.9 又收紧了部分隐式转换，目的是避免把数字、`char` 和文本意外混用。

```cpp
const QChar latin = QChar::fromLatin1('A'); // 明确：Latin-1 字节
const QChar unit = QChar::fromUcs2(u'\u4E2D'); // 明确：一个 UTF-16 单元
const QChar tab(QChar::Tabulation);          // 明确：特殊控制字符
```

`char` 不能自动代表 UTF-8 字符。UTF-8 的一个非 ASCII 字符通常占多个 `char`；先把字节序列解码为 `QString`，再处理 `QChar`。`toLatin1()` 对超出 Latin-1 的字符返回 `'\0'`，且无法区分“真的 NUL”和“无法转换”，国际化代码不要把它当作通用编码转换。

## 4. 从 UCS-4 写入 QString：用 `fromUcs4()`，不要截断

给定一个 `char32_t` 码点，`QChar::fromUcs4()` 返回一个临时的双单元结果：

- BMP 码点：包含一个 UTF-16 单元。
- 需要代理对的码点：包含高、低两个 UTF-16 单元。
- 结果可隐式转为 `QStringView`，也可用于范围 for。

```cpp
const char32_t face = U'\U0001F600';

QString text;
text += QChar::fromUcs4(face); // 正确：必要时追加两个 UTF-16 单元
```

不要写 `QChar(face)` 来表示辅助平面码点。`QChar` 只能容纳一个 16 位单元；这种构造只适合数值不超过 `0xFFFF` 的单元。先用 `requiresSurrogates()` 判断，再用 `fromUcs4()` 或 `highSurrogate()`、`lowSurrogate()` 生成完整序列。

## 5. Unicode 分类 API：比 `<cctype>` 更适合文本

`isLetter()`、`isNumber()`、`isSpace()` 等依据 Unicode 数据库，而不是仅处理 ASCII。它们适合输入校验、语法高亮、分词前的粗分类或编辑器规则。

```cpp
const QChar ch = u'\u0665'; // 阿拉伯-印度数字 5
Q_ASSERT(ch.isDigit());
Q_ASSERT(ch.digitValue() == 5);
```

几个容易混淆的关系：

| API | 判断范围 | 典型误区 | 适合用途 |
| --- | --- | --- | --- |
| `isDigit()` | Unicode 十进制数字类别 `Nd`。 | 不是只识别 ASCII `0` 到 `9`。 | 解析允许国际化数字的单个数字。 |
| `isNumber()` | 全部 `Number_*` 类别。 | 可能是真分数、罗马数字等，不一定能当十进制位。 | 宽松的数字类判断。 |
| `digitValue()` | 返回十进制数值或 `-1`。 | `isNumber()` 为真不保证可当十进制位。 | 将单个 Unicode 数字转为整数。 |
| `isLetterOrNumber()` | `Letter_*` 或 `Number_*`。 | 不包含下划线和组合标记。 | 简单标识符筛选的起点。 |
| `isSpace()` | Unicode 分隔符加少数控制字符。 | 不等同于只检查 `' '`。 | 清理输入、分词和空白处理。 |

若协议明确规定 ASCII，例如 HTTP token、十六进制字面量或编程语言关键字，仍应显式按 ASCII 范围检查；Unicode 宽松判断会接受不属于该协议的字符。

## 6. 大小写、比较与本地化

`QChar::toLower()`、`toUpper()`、`toTitleCase()` 和 `toCaseFolded()` 都只返回**一个** `QChar` 或一个 `char32_t`。有些 Unicode 的完整大小写映射需要多个码点，单字符 API 无法表达这种扩展映射；例如文档明确说明 `toUpper()` 在大写结果需要两个或更多字符时会返回原字符。

```cpp
const QChar c = u'A';
Q_ASSERT(c.toLower() == u'a');
```

- 要对整段 Unicode 文本做大小写变化，使用 `QString::toLower()`、`QString::toUpper()`。
- 要做不区分大小写的匹配，先考虑 `QString::compare(..., Qt::CaseInsensitive)` 或对完整字符串作 case fold。
- `QChar` 的比较运算符只按数值代码单元比较，不是语言排序；按 locale 排序请使用 `QCollator` 或 `QString::localeAwareCompare()`。

## 7. 方向、镜像、脚本与组合标记

这些 API 主要服务文本排版、编辑器、复杂脚本处理和 Unicode 分析工具：

- `direction()` 返回双向文本算法使用的方向属性。
- `hasMirrored()` 和 `mirroredChar()` 用于 RTL 上下文中的括号等镜像字符。
- `joiningType()` 描述阿拉伯文、叙利亚文等字符的连接属性。
- `script()` 返回 Unicode Script 属性；数字、标点常为 `Script_Common`，组合标记可能是 `Script_Inherited`。
- `combiningClass()` 是组合标记相对基字符的定位提示，Qt 文本引擎也会使用它。
- `decomposition()` 与 `decompositionTag()` 给出 Unicode 分解信息；它们不是完整字符串正规化 API。

不要手工据此实现双向排版、阿拉伯连字或 Unicode NFC/NFD 正规化。需要完整行为时使用 Qt 文本布局组件或针对字符串的 Unicode 处理功能。

## 8. 特殊常量和 Unicode 版本

`SpecialCharacter` 提供常用控制与格式常量，例如 `Null`、`Tabulation`、`LineFeed`、`Space`、`Nbsp`、`ReplacementCharacter`、`ByteOrderMark`、`ParagraphSeparator` 与 `LineSeparator`。它们提升可读性，但不改变字符本身的 Unicode 语义。

`unicodeVersion()` 返回某个码点首次出现的 Unicode 版本，`currentUnicodeVersion()` 返回当前 Qt 字符数据支持的最新版本。它们适合兼容性诊断或测试，不适合作为“字体一定能显示此字”的判断；`isPrint()` 也只能说明 Unicode 分类为可打印，不能证明当前字体有字形。

## 9. 常见错误

### 9.1 把 `QChar::isNull()` 当作字符串为空

它只判断当前单元是否为 U+0000。字符串是否为空看 `QString::isEmpty()`；字符串是否全由 NUL 构成又是另一个问题。

### 9.2 用 `toLatin1()` 判断字符是否可转换

返回的 `0` 既可能表示原字符是 NUL，也可能表示转换失败。需要保留原值时使用 `unicode()` 或完整的字符串编码 API。

### 9.3 对代理项调用大小写或分类后当作完整字符

代理项只是 UTF-16 序列的一半。应先组合为码点，然后用带 `char32_t` 参数的静态 API 查询属性。

### 9.4 用 `isPrint()` 判断字体是否支持字符

`isPrint()` 检查 Unicode 类别，不查询任何字体。字体回退、缺字方框和实际渲染结果属于 Qt Gui/文本布局层的问题。

## API 速查表
### 类型、常量和构造

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `Category` | Unicode 通用类别，例如 `Letter_*`、`Number_*`、`Mark_*`、`Punctuation_*`、`Symbol_*`。 | 用 `category()` 做细分；不要用枚举数值作为持久化协议。 |
| 枚举 | `Direction` | Unicode 双向属性，如 `DirL`、`DirR`、`DirAL`、`DirEN`。 | 适合分析文本；完整双向布局交给文本引擎。 |
| 枚举 | `JoiningType` | 字符在阿拉伯文或叙利亚文等脚本中的连接属性。 | 不能替代完整的 shaping 规则。 |
| 枚举 | `Script` | Unicode Script 属性，例如 Latin、Han、Arabic、Common、Inherited。 | 标点和组合标记不一定归属周围文字的脚本。 |
| 枚举 | `Decomposition` | Unicode 分解标签，例如 Canonical、Compat、Font、Wide。 | 只描述映射类型；字符串正规化应使用高层 API。 |
| 枚举 | `UnicodeVersion` | 字符首次被 Unicode 收录的版本。 | 与字体支持和操作系统版本不是同一件事。 |
| 枚举 | `SpecialCharacter` | 常用控制、分隔与替换字符常量。 | 用命名常量代替难读的十六进制字面量。 |
| 构造 | `QChar()` | 创建 U+0000。 | 默认构造不是“未初始化”。 |
| 构造 | `QChar(SpecialCharacter)`、`QChar(QLatin1Char)` | 从特殊常量或明确的 Latin-1 字符创建单元。 | 适合表达明确的字符来源。 |
| 构造 | `QChar(char)`、`QChar(uchar)` | 从单个 8 位值创建单元。 | 这不是 UTF-8 解码；受 ASCII 转换宏配置影响。 |
| 构造 | `QChar(char16_t)`、`QChar(ushort)`、`QChar(short)`、`QChar(wchar_t)` | 从 16 位字符或兼容整型创建单元。 | `wchar_t` 宽度随平台不同；不要把它假定为完整 Unicode 码点。 |
| 构造 | `explicit QChar(char32_t)`、`QChar(int)`、`QChar(uint)` | 从数值代码单元构造。 | 仅适合不超过 `0xFFFF` 的值；Qt 6.9 收紧了隐式转换。 |
| 构造 | `explicit QChar(uchar cell, uchar row)` | 由低字节 cell 和高字节 row 组成一个 UTF-16 单元。 | 是旧式 16 位拆分接口，不是 Unicode 平面与码点拆分。 |

### 编码与 UTF-16 处理

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 创建 | `static QChar fromLatin1(char c)` | 将 Latin-1 字节转换为相同数值的 UTF-16 单元。 | 明确表达 Latin-1；不能用于 UTF-8 多字节序列。 |
| 创建 | `static QChar fromUcs2(char16_t c)` | 从一个 UTF-16 单元创建 `QChar`。 | Qt 6.0 起提供；代理项仍只是一个序列的一半。 |
| 创建 | `static auto fromUcs4(char32_t c)` | 生成可表示一个 UCS-4 码点的一或两个 UTF-16 单元。 | 结果可转 `QStringView`；辅助平面字符不要截成单个 `QChar`。 |
| 读取 | `char16_t unicode() const` | 返回当前 UTF-16 单元数值。 | 返回的是 code unit，不一定是完整码点。 |
| 修改 | `char16_t &unicode()` | 返回底层单元的可写引用。 | 直接改值会绕开语义检查；不要制造孤立代理项。 |
| 读取 | `char toLatin1() const` | 返回 Latin-1 值，超出范围时为 0。 | 0 与真正 NUL 不可区分，国际化代码避免依赖它。 |
| 读取 | `uchar row() const`、`uchar cell() const` | 读取 UTF-16 单元的高字节和低字节。 | 仅用于旧式位级处理。 |
| 修改 | `void setRow(uchar)`、`void setCell(uchar)` | 改写 UTF-16 单元的高字节或低字节。 | 容易产生任意单元，正常文本代码不应使用。 |
| 代理项 | `static bool requiresSurrogates(char32_t)` | 判断 UCS-4 码点是否需要 UTF-16 代理对。 | 对 `0x10000` 及以上返回真。 |
| 代理项 | `static char16_t highSurrogate(char32_t)`、`lowSurrogate(char32_t)` | 取得辅助平面码点的两个 UTF-16 单元。 | 小于 `0x10000` 时结果未定义；先调用 `requiresSurrogates()`。 |
| 代理项 | `static char32_t surrogateToUcs4(char16_t, char16_t)`、`surrogateToUcs4(QChar, QChar)` | 将高、低代理项还原为 UCS-4 码点。 | 调用方必须先确认两个参数分别是真正的高、低代理项。 |
| 代理项 | `isHighSurrogate()`、`isLowSurrogate()`、`isSurrogate()` 及 `char32_t` 静态重载 | 判断单元或码点是否落在代理项范围。 | 代理项本身不是可独立显示的 Unicode 标量值。 |

### 分类、数字与文本属性

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 分类 | `category() const`、`static category(char32_t)` | 返回 Unicode 通用类别。 | 静态重载能正确处理辅助平面码点。 |
| 分类 | `isPrint()`、`isMark()`、`isPunct()`、`isSymbol()` 及静态重载 | 判断可打印、组合标记、标点或符号类别。 | `isPrint()` 不代表当前字体可显示。 |
| 分类 | `isSpace()` 及静态重载 | 判断 Unicode 空白和少数控制空白。 | 不只匹配 ASCII 空格。 |
| 分类 | `isLetter()`、`isNumber()`、`isLetterOrNumber()` 及静态重载 | 判断字母、数字或二者之一。 | 用于 Unicode 宽松规则；协议校验需按协议限定。 |
| 分类 | `isDigit()` 及静态重载 | 判断十进制数字 `Nd`。 | 与 `isNumber()` 范围不同。 |
| 数值 | `digitValue() const`、`static digitValue(char32_t)` | 返回十进制数字值，非数字为 `-1`。 | 先检查 `-1`，不要把任意 Number 类别当作十进制位。 |
| 状态 | `isNull() const` | 判断是否为 U+0000。 | 不等同于字符串为空。 |
| 状态 | `isNonCharacter()` 及静态重载 | 判断 Unicode noncharacter 保留码点。 | 可供内部用途，但不应用于文本交换。 |
| 大小写 | `isLower()`、`isUpper()`、`isTitleCase()` 及静态重载 | 判断 Unicode 大小写类别。 | 仅是单码点属性，不能表达完整语言规则。 |

### 方向、分解、映射和元数据

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 双向 | `direction() const`、`static direction(char32_t)` | 返回 Unicode 双向属性。 | 分析或调试可用；不要据此自行实现双向算法。 |
| 双向 | `hasMirrored()`、`mirroredChar()` 及静态重载 | 查询或取得 RTL 环境的镜像对应字符。 | 只处理字符镜像，不能完成整段 RTL 排版。 |
| 字体脚本 | `joiningType()`、`script()` 及静态重载 | 查询连接属性与 Unicode Script。 | 适合分析和字体选择提示，不能替代 shaping。 |
| 组合 | `combiningClass()` 及静态重载 | 返回组合类，提示标记相对基字符的位置。 | 普通应用不应自行排布组合标记。 |
| 分解 | `decomposition()`、`decompositionTag()` 及静态重载 | 返回 Unicode 分解序列与其分解标签。 | 无分解时字符串为空；不是 NFC 或 NFD 的完整字符串正规化。 |
| 映射 | `toLower()`、`toUpper()`、`toTitleCase()`、`toCaseFolded()` 及静态重载 | 执行单码点大小写或 case-fold 映射。 | 多码点映射会丢失，整段文本使用 `QString` API。 |
| 版本 | `unicodeVersion()` 及静态重载 | 返回字符被引入的 Unicode 版本。 | 支持版本不保证字体有对应字形。 |
| 版本 | `static currentUnicodeVersion()` | 返回 Qt 当前字符数据库支持的最新 Unicode 版本。 | 用于诊断、测试或功能门槛判断。 |

### 比较与流

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 比较 | `operator==`、`!=`、`<`、`<=`、`>`、`>=` | 按 UTF-16 单元数值比较两个 `QChar`。 | 不是语言学排序，也不会按字符串或 grapheme cluster 比较。 |
| 排序 | `comparesEqual()`、`compareThreeWay()` | 提供 Qt 强排序框架使用的相等与三路比较。 | 语义同样是数值单元比较。 |
| 序列化 | `QDataStream &operator<<(QDataStream &, QChar)` | 将一个 UTF-16 单元写入数据流。 | 流版本与端序由 `QDataStream` 配置控制。 |
| 反序列化 | `QDataStream &operator>>(QDataStream &, QChar &)` | 从数据流读回一个 UTF-16 单元。 | 得到的单元可能是代理项；文本有效性仍由上层保证。 |
| 哈希 | `std::hash<QChar>` | 为标准库散列表提供哈希支持。 | 仅按 `unicode()` 单元值哈希。 |

---

### 一句话总结

`QChar` 是 Unicode 文本处理中最底层的 UTF-16 单元工具：它擅长查属性和处理代理对，但不等于一个完整码点或用户可见字符；面向字符串语义时，应优先使用 `QString` 与文本边界工具。
