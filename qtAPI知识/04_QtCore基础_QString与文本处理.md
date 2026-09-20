# Qt Core 基础：QString 与文本处理

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Core  
> 核心类型：`QString`、`QChar`、`QByteArray`、`QStringView`、`QAnyStringView`

## 1. 先分清“文本”和“字节”

这是处理字符串时最重要的概念：

- **文本**表示 Unicode 字符，Qt 中主要使用 `QString`。
- **字节**表示原始二进制序列，Qt 中主要使用 `QByteArray`。
- 编码负责在“字符”与“字节序列”之间转换，例如 UTF-8、UTF-16、Latin-1。

```text
UTF-8 文件或网络数据（QByteArray）
             ↓ 解码 fromUtf8()
       Unicode 文本（QString）
             ↓ 编码 toUtf8()
UTF-8 文件或网络数据（QByteArray）
```

乱码通常不是“QString 不支持中文”，而是某一端用了错误编码解释字节。

## 2. QString 的内部模型

`QString` 保存一串 16 位 `QChar`，每个 `QChar` 对应一个 UTF-16 **代码单元**。

对于基本多文种平面中的字符，一个字符通常占一个代码单元；某些 Unicode 字符需要一对 UTF-16 代理项，因此占两个代码单元。

```cpp
QString text = QStringLiteral("A中");
qDebug() << text.size(); // 2
```

但不能把 `size()` 永远理解为“屏幕上看到几个字”。

```cpp
QString emoji = QString::fromUtf8("😀");
qDebug() << emoji.size(); // UTF-16 中通常为 2
```

更复杂的情况还有组合附加符、变体选择符和零宽连接符。一个用户感知字符可能由多个 Unicode 码点组成。

结论：

> `QString::size()`、索引和切片以 UTF-16 代码单元计算，不等于 Unicode 码点数，也不等于用户感知字符数。

需要按用户感知字符分割时，应研究 `QTextBoundaryFinder`。

## 3. 创建 QString

### 3.1 编译期字符串

推荐：

```cpp
QString title = QStringLiteral("用户设置");
```

`QStringLiteral` 让编译期已知文本直接形成适合 `QString` 的数据，减少运行时分配和转码。

Qt 6 也支持字符串字面量：

```cpp
using namespace Qt::StringLiterals;

QString title = u"用户设置"_s;
```

### 3.2 从 UTF-8 字节创建

```cpp
QByteArray bytes = networkReply->readAll();
QString text = QString::fromUtf8(bytes);
```

明确写 `fromUtf8()` 能让编码边界一目了然。

### 3.3 从 Latin-1 或本地编码创建

```cpp
QString latin = QString::fromLatin1(bytes);
QString local = QString::fromLocal8Bit(bytes);
```

只有数据源确实使用相应编码时才这样做。现代网络协议、JSON 和新文本文件通常优先使用 UTF-8，不要因为中文乱码就盲目改成 `fromLocal8Bit()`。

### 3.4 重复字符和指定长度

```cpp
QString line(20, QLatin1Char('-'));
QString prefix = QStringLiteral("abcdef").left(3);
```

## 4. 空字符串与 null 字符串

历史原因使 `QString` 区分 null 和 empty：

```cpp
QString nullString;
QString emptyString = QStringLiteral("");

qDebug() << nullString.isNull();   // true
qDebug() << nullString.isEmpty();  // true
qDebug() << emptyString.isNull();  // false
qDebug() << emptyString.isEmpty(); // true
```

null 一定 empty，但 empty 不一定 null。

除 `isNull()` 外，大部分 API 将二者同等处理。Qt 官方建议普通业务逻辑优先使用：

```cpp
if (text.isEmpty()) {
    // 没有文本
}
```

只有外部协议明确区分“未提供”和“提供了空值”时，才需要保留 null 语义。

## 5. 读取长度和字符

```cpp
QString text = QStringLiteral("Qt 6");

qsizetype length = text.size();
bool empty = text.isEmpty();
QChar first = text.at(0);
QChar last = text.back();
```

`at(index)` 不会自动进行越界保护。读取前应保证：

```cpp
if (!text.isEmpty()) {
    qDebug() << text.front();
}
```

遍历 UTF-16 代码单元：

```cpp
for (QChar ch : text)
    qDebug() << ch;
```

这仍然不是按完整 Unicode 码点或用户感知字符遍历。

## 6. 拼接字符串

### 6.1 简单拼接

```cpp
QString fullName = firstName + QStringLiteral(" ") + lastName;
```

追加：

```cpp
QString result;
result.append(QStringLiteral("name="));
result += userName;
```

### 6.2 循环构造长字符串

如果能够估计长度，先预留容量：

```cpp
QString result;
result.reserve(1024);

for (const QString &item : items) {
    result.append(item);
    result.append(QLatin1Char('\n'));
}
```

`reserve()` 只增加容量，不改变 `size()`。不能在 `size()` 之外直接写数据；需要改变逻辑长度时使用 `resize()`。

### 6.3 QStringBuilder

极端高频拼接可以研究 `QStringBuilder`：

```cpp
#include <QStringBuilder>

QString result = first % QStringLiteral("/") % second;
```

它通过延迟计算减少中间对象。普通代码应先保证清晰，并通过测量确认拼接确实是热点，再引入此优化。

启用 QStringBuilder 后，不要轻率地用 `auto` 长期保存拼接表达式，因为推导结果可能是表达式模板而不是独立 `QString`：

```cpp
QString stable = first % second; // 明确生成拥有数据的 QString
```

## 7. 截取和修改

### 7.1 常用截取

```cpp
QString text = QStringLiteral("abcdef");

QString a = text.left(2);       // "ab"
QString b = text.right(2);      // "ef"
QString c = text.mid(2, 3);     // "cde"
QString d = text.sliced(2, 3);  // "cde"
```

`sliced()` 对参数有效性要求更严格，适合调用方已经保证范围正确的代码；处理外部输入时应先检查边界。

### 7.2 插入、移除、替换

```cpp
QString value = QStringLiteral("Qt5");

value.replace(QStringLiteral("Qt5"), QStringLiteral("Qt6"));
value.insert(2, QLatin1Char(' '));
value.remove(2, 1);
```

这些非 const 操作可能触发隐式共享数据分离，并使已有迭代器、字符引用和视图失效。

## 8. 去除与规范化空白

```cpp
QString input = QStringLiteral("  hello   Qt \n");

QString trimmed = input.trimmed();
// "hello   Qt"

QString simplified = input.simplified();
// "hello Qt"
```

- `trimmed()`：去除首尾空白，保留中间空白。
- `simplified()`：去除首尾空白，并把内部连续空白压缩为一个空格。

不要对密码、签名原文、固定格式数据等内容随意 `simplified()`，因为空白可能具有业务意义。

## 9. 查找和判断

```cpp
QString text = QStringLiteral("Hello Qt");

bool hasQt = text.contains(QStringLiteral("Qt"));
bool begins = text.startsWith(QStringLiteral("Hello"));
bool ends = text.endsWith(QStringLiteral("Qt"));
qsizetype index = text.indexOf(QStringLiteral("Qt"));
qsizetype last = text.lastIndexOf(QLatin1Char('l'));
```

大小写不敏感：

```cpp
bool matched = text.contains(QStringLiteral("hello"),
                             Qt::CaseInsensitive);
```

找不到时 `indexOf()` 返回 `-1`：

```cpp
const qsizetype position = text.indexOf(QLatin1Char(':'));
if (position >= 0) {
    // 安全使用 position
}
```

## 10. 分割与连接

```cpp
QString source = QStringLiteral("red,green,blue");
QStringList parts = source.split(QLatin1Char(','));

QString joined = parts.join(QStringLiteral(" | "));
```

忽略空字段：

```cpp
QStringList values =
    QStringLiteral("a,,b").split(QLatin1Char(','),
                                  Qt::SkipEmptyParts);
```

保留空字段适合 CSV 类语义，忽略空字段适合分隔符只是视觉间隔的语义。不要未分析输入格式就默认跳过空值。

高性能只读分词可以进一步学习 `QStringTokenizer`，它返回视图而不是为每一段分配新的 `QString`，但必须更谨慎地管理源字符串生命周期。

## 11. 占位符格式化：QString::arg

```cpp
QString message = QStringLiteral("第 %1 项，共 %2 项：%3")
                      .arg(current)
                      .arg(total)
                      .arg(fileName);
```

每次 `arg()` 替换编号最小且尚未替换的占位符。

它适合可翻译文本，因为翻译者可以调整占位符顺序：

```cpp
tr("Copied %1 files to %2").arg(count).arg(directory);
```

数字进制和宽度：

```cpp
QString hex = QStringLiteral("0x%1").arg(value, 0, 16);
QString padded = QStringLiteral("%1").arg(value, 6, 10, QLatin1Char('0'));
```

不要把用户输入直接当成格式模板反复调用 `arg()`，因为其中的 `%1` 等内容可能被误当占位符。

## 12. 数字与字符串转换

### 12.1 数字转字符串

```cpp
QString decimal = QString::number(42);
QString hex = QString::number(255, 16);
QString floating = QString::number(3.14159, 'f', 2);
```

### 12.2 字符串转数字

```cpp
bool ok = false;
int value = text.toInt(&ok, 10);

if (!ok) {
    qWarning() << "Invalid integer:" << text;
}
```

永远不要用返回的 0 同时表示“合法的零”和“转换失败”；使用 `ok` 区分。

```cpp
double value = text.toDouble(&ok);
```

### 12.3 面向用户的本地化数字

`QString::toDouble()` 等通常按 C locale 规则处理。解析用户界面中的本地化数字时使用 `QLocale`：

```cpp
QLocale locale;
double value = locale.toDouble(userText, &ok);
QString display = locale.toString(value, 'f', 2);
```

机器协议和配置格式应使用协议规定的固定格式；用户显示则使用适当 locale。不要混用这两个边界。

## 13. UTF-8 与 QByteArray 转换

### 13.1 QString 转 UTF-8

```cpp
QString text = QStringLiteral("你好，Qt");
QByteArray utf8 = text.toUtf8();
```

适合网络、JSON、现代文本文件等 UTF-8 边界。

### 13.2 UTF-8 转 QString

```cpp
QByteArray utf8 = readBytes();
QString text = QString::fromUtf8(utf8);
```

### 13.3 临时对象的 constData 陷阱

危险：

```cpp
const char *pointer = text.toUtf8().constData();
useLater(pointer); // pointer 已经悬空
```

`toUtf8()` 返回临时 `QByteArray`，完整表达式结束后临时对象销毁。

正确：

```cpp
QByteArray utf8 = text.toUtf8();
const char *pointer = utf8.constData();
useWhileUtf8IsAlive(pointer);
```

如果 C API 会长期保存指针，仅让局部 `QByteArray` 活到函数返回还不够；必须按该 API 的所有权要求保存数据或复制。

## 14. 不同编码 API 如何选择

| API | 含义 | 常见场景 |
|---|---|---|
| `fromUtf8()` / `toUtf8()` | UTF-8 | 网络、JSON、新文件格式 |
| `fromLatin1()` / `toLatin1()` | Latin-1 | 明确规定为 Latin-1 的旧协议 |
| `fromLocal8Bit()` / `toLocal8Bit()` | 系统本地编码 | 旧系统接口或遗留数据 |
| `QStringDecoder` | 状态化或指定编码解码 | 流式读取和其他编码 |
| `QStringEncoder` | 状态化或指定编码编码 | 流式写出和其他编码 |

Windows 的本地编码取决于当前代码页，不保证跨机器一致。长期保存的数据不应依赖“本机默认编码”。

## 15. 比较、排序与大小写

### 15.1 机器语义比较

```cpp
if (left == right) {
}

int order = QString::compare(left, right, Qt::CaseInsensitive);
```

普通比较按 UTF-16 代码单元字典序，速度快、结果稳定，但不一定符合人类语言排序习惯。

### 15.2 面向用户的排序

```cpp
int order = QString::localeAwareCompare(left, right);
```

大量本地化排序和高级排序规则可使用 `QCollator`，并复用 collator 对象以避免重复配置成本。

### 15.3 大小写转换

```cpp
QString upper = text.toUpper();
QString lower = text.toLower();
QString folded = text.toCaseFolded();
```

`toCaseFolded()` 更适合某些不区分大小写的规范比较，但标识符、用户名、文件名是否允许折叠必须由业务规则决定。不同文件系统的大小写规则也不同。

## 16. Unicode 规范化

视觉上相同的文本可能由不同码点序列组成。例如带重音字符可能是一个预组合码点，也可能是基础字母加组合符号。

```cpp
QString normalized = text.normalized(QString::NormalizationForm_C);
```

适用场景：

- 需要稳定比较的外部 Unicode 数据
- 搜索索引
- 协议明确要求某种规范化形式

不要随意规范化密码、加密签名输入或要求保留原始字节表示的数据。

## 17. 正则表达式

```cpp
QRegularExpression pattern(QStringLiteral(R"(^[A-Za-z0-9_]+$)"));
QRegularExpressionMatch match = pattern.match(userName);

if (match.hasMatch()) {
    qDebug() << "valid";
}
```

替换：

```cpp
QString compact = text;
compact.replace(QRegularExpression(QStringLiteral(R"(\s+)")),
                QStringLiteral(" "));
```

正则适合结构模式，不适合所有文本处理。固定前缀、简单包含和单字符分隔优先使用 `startsWith()`、`contains()`、`split()`，更清晰也更便宜。

频繁使用同一正则时，应复用已构造的 `QRegularExpression`。

## 18. 隐式共享与写时复制

`QString` 使用隐式共享：

```cpp
QString first = largeText;
QString second = first; // 通常只增加引用计数
```

二者共享底层数据，直到其中一个被修改：

```cpp
second.append(QLatin1Char('!')); // 必要时分离并复制
```

这意味着按值返回 `QString` 通常是合理的：

```cpp
QString buildTitle()
{
    QString result = QStringLiteral("Report");
    return result;
}
```

现代 C++ 的移动语义、返回值优化和 Qt 隐式共享共同减少不必要复制。不要为了“优化”而返回局部 `QString` 的引用。

## 19. 迭代器和引用失效

对共享字符串执行第一个非 const 操作时可能发生深复制，进而使已有迭代器和字符引用失效：

```cpp
QString text = QStringLiteral("abc");
auto iterator = text.begin();

text.append(QLatin1Char('d'));
// iterator 不能继续使用
```

规则：

- 保存迭代器期间不要调用可能修改字符串的函数。
- 修改后重新获取迭代器。
- 不要长期保存指向 `QString` 内部数据的指针。

## 20. QStringView：零拷贝只读视图

`QStringView` 引用一段 UTF-16 字符数据，但不拥有它。

```cpp
void inspect(QStringView text)
{
    qDebug() << text.size();
}

QString owned = QStringLiteral("hello");
inspect(owned);
```

视图适合作为只读函数参数，可以避免构造新字符串。

### 20.1 生命周期陷阱

危险：

```cpp
QStringView view = makeQString(); // 返回值是临时 QString
// 临时字符串销毁后 view 悬空
```

正确：

```cpp
QString owned = makeQString();
QStringView view = owned;
```

即使源对象仍存在，修改源字符串导致重分配或分离后，旧视图也可能失效。

### 20.2 参数按值传递

视图对象本身很小，通常按值传递：

```cpp
void inspect(QStringView text); // 推荐
```

而不是：

```cpp
void inspect(const QStringView &text); // 通常没有必要
```

## 21. QAnyStringView 和其他视图

| 类型 | 引用的数据编码 | 主要用途 |
|---|---|---|
| `QStringView` | UTF-16 | 查看 QString/UTF-16 数据 |
| `QUtf8StringView` | UTF-8 | 查看 UTF-8 数据 |
| `QLatin1StringView` | Latin-1 | 查看明确的 Latin-1 数据 |
| `QAnyStringView` | UTF-8、UTF-16 或 Latin-1 | 接口参数统一接收多种字符串 |

```cpp
void setLabel(QAnyStringView text)
{
    label_ = text.toString(); // 成员需要长期保存，转换成拥有数据的 QString
}
```

`QAnyStringView` 特别适合作为接口参数，但不推荐随意作为长期成员或返回值。所有视图的共同规则是：被引用数据必须比视图活得更久。

## 22. QString、std::string 和文件路径

UTF-8 `std::string` 转换：

```cpp
std::string bytes = getUtf8Text();
QString text = QString::fromUtf8(bytes);

std::string output = text.toUtf8().toStdString();
```

不要假定任意 `std::string` 都是 UTF-8；它只是字节容器，编码由数据来源决定。

处理文件路径时优先让 Qt API 接收 `QString`：

```cpp
QFile file(pathString);
```

与 `std::filesystem::path` 交互时使用 Qt 提供的明确转换接口，避免通过本地 8 位编码中转而丢失字符。

## 23. 综合示例：清洗并解析用户输入

需求：输入若干逗号分隔的整数，允许首尾空白，拒绝非法项，最后生成本地化摘要。

```cpp
#include <QLocale>
#include <QList>
#include <QString>
#include <QStringList>

struct ParseResult
{
    QList<int> values;
    QString error;
};

ParseResult parseNumbers(QStringView input)
{
    ParseResult result;

    const QStringList parts = input.toString().split(
        QLatin1Char(','), Qt::KeepEmptyParts);

    for (qsizetype i = 0; i < parts.size(); ++i) {
        const QString part = parts.at(i).trimmed();

        if (part.isEmpty()) {
            result.error = QStringLiteral("第 %1 项为空").arg(i + 1);
            return result;
        }

        bool ok = false;
        const int value = part.toInt(&ok);

        if (!ok) {
            result.error = QStringLiteral("第 %1 项不是整数：%2")
                               .arg(i + 1)
                               .arg(part);
            return result;
        }

        result.values.append(value);
    }

    return result;
}
```

调用：

```cpp
const ParseResult result =
    parseNumbers(QStringLiteral(" 10, 20, 30 "));

if (!result.error.isEmpty()) {
    qWarning() << result.error;
} else {
    qDebug() << QStringLiteral("成功解析 %1 个整数")
                    .arg(QLocale().toString(result.values.size()));
}
```

该示例体现：

- 参数使用只读视图。
- 明确保留空字段，避免把非法输入静默忽略。
- 每次转换检查 `ok`。
- 错误文本使用编号占位符。
- 对外显示数字使用 `QLocale`。

## 24. 常见乱码排查顺序

1. 数据源实际是什么编码？
2. 读取后保存为 `QByteArray` 还是已经被错误转成文本？
3. 是否使用与来源一致的 `fromUtf8/fromLocal8Bit/fromLatin1`？
4. 输出目标要求什么编码？
5. 控制台本身是否以正确编码显示？
6. 源代码文件是否保存为 UTF-8？
7. 是否错误地把二进制数据当作以 `\0` 结尾的 C 字符串？

要检查字节本身，可以输出十六进制，而不是只观察乱码结果：

```cpp
qDebug() << bytes.toHex(' ');
```

## 25. API 速查

| API | 作用 | 注意点 |
|---|---|---|
| `QStringLiteral()` | 构造编译期文本 | 固定文本优先使用 |
| `fromUtf8()` / `toUtf8()` | UTF-8 解码/编码 | 网络和现代文件常用 |
| `isEmpty()` | 判断长度是否为 0 | 一般优先于 `isNull()` |
| `size()` | UTF-16 代码单元数量 | 不等于用户感知字符数 |
| `left/right/mid/sliced` | 截取文本 | 注意索引边界和代理项 |
| `trimmed()` | 去掉首尾空白 | 不改变内部空白 |
| `simplified()` | 压缩全部空白 | 可能改变业务数据 |
| `contains/indexOf` | 查找 | 找不到索引为 -1 |
| `split()` / `join()` | 分割和连接 | 明确是否保留空项 |
| `arg()` | 替换编号占位符 | 适合可翻译文本 |
| `number()` | 数字转文本 | 机器格式 |
| `toInt/toDouble` | 文本转数字 | 使用 `ok` 检查 |
| `localeAwareCompare()` | 本地化排序比较 | 大量排序可用 `QCollator` |
| `normalized()` | Unicode 规范化 | 按协议和业务需要使用 |
| `reserve()` | 预留容量 | 不改变字符串长度 |
| `QStringView` | UTF-16 只读视图 | 不拥有数据 |
| `QAnyStringView` | 多编码接口视图 | 适合按值传参 |

## 26. 自测题

1. `QString` 与 `QByteArray` 的核心区别是什么？
2. 为什么 `QString::size()` 不一定等于用户看到的字符数？
3. UTF-8 网络响应如何转换为 `QString`？
4. 为什么 `text.toUtf8().constData()` 不能保存后稍后使用？
5. null 字符串和 empty 字符串有什么关系？
6. `trimmed()` 与 `simplified()` 有何区别？
7. `toInt()` 为什么要传入 `ok`？
8. 用户可见字符串排序为什么不一定使用普通 `<`？
9. 修改源字符串为什么可能让 `QStringView` 失效？
10. 隐式共享对复制和修改分别有什么影响？

### 参考答案

1. `QString` 表示 Unicode 文本，`QByteArray` 表示原始字节。
2. 长度按 UTF-16 代码单元计算，一个码点或感知字符可能使用多个代码单元。
3. 读取为 `QByteArray` 后调用 `QString::fromUtf8()`。
4. `toUtf8()` 的临时 `QByteArray` 在完整表达式结束后销毁，其内部指针随即悬空。
5. null 一定 empty，但 empty 不一定 null；普通逻辑优先用 `isEmpty()`。
6. 前者只去首尾空白，后者还会压缩内部连续空白。
7. 返回 0 既可能是合法结果，也可能表示转换失败，需要 `ok` 区分。
8. 普通比较按代码单元顺序，不一定符合用户语言的排序习惯。
9. 修改可能触发分离或重分配，视图原先引用的内存不再有效。
10. 复制通常只共享数据；首次修改共享数据时才发生深复制。

---

## 总结

正确使用 `QString` 的核心是明确编码边界：程序内部使用 Unicode 文本，进入或离开文件、网络和 C API 时显式编码或解码。进一步要理解 `QString` 以 UTF-16 代码单元索引、使用隐式共享，并区分拥有数据的字符串与不拥有数据的视图。大部分字符串错误都可以归结为四类：编码假设错误、索引单位错误、临时对象生命周期错误，以及修改后继续使用已失效的迭代器或视图。
