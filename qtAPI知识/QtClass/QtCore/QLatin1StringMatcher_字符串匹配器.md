# Qt QLatin1StringMatcher 字符串匹配器

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.5  
> 头文件：`#include <QLatin1StringMatcher>`  
> 所属模块：`Qt6::Core`  
> 相关类型：`QLatin1StringView`、`QStringView`、`QStringMatcher`、`QByteArrayMatcher`、`QStaticLatin1StringMatcher`

## 1. 先给结论：它解决什么问题

`QLatin1StringMatcher` 是一个**可复用的 Latin-1 子串匹配器**。它把一个待搜索的模式保存为 `QLatin1StringView`，并为这个模式准备内部搜索状态；之后可以在多个 haystack（被搜索字符串）中反复调用 `indexIn()`。

它适合解决的问题是：

- 同一个固定模式要在很多 Latin-1 字符串中反复查找；
- 同一个 haystack 中要循环查找模式的所有出现位置；
- 模式较长、haystack 较长，直接重复调用 `QLatin1StringView::indexOf()` 的预处理成本开始明显；
- 需要显式选择大小写敏感或大小写不敏感。

Qt 文档对它的定位很明确：

> 反复匹配时，`QLatin1StringMatcher::indexIn()` 通常比直接调用 `QLatin1StringView::indexOf()` 更快；只做一次匹配时，它没有额外收益。

因此，选择它的判断不是“它比 `indexOf()` 更高级”，而是：

```text
一次查找                         -> 直接 indexOf()
同一模式重复查找                 -> QLatin1StringMatcher
模式在编译期固定，连一次查找也要优化 -> QStaticLatin1StringMatcher
```

## 2. 最小使用模型

```cpp
#include <QLatin1StringMatcher>
#include <QLatin1StringView>

using namespace Qt::StringLiterals;

bool containsStatus(QLatin1StringView text)
{
    const QLatin1StringMatcher matcher("status="_L1);
    return matcher.indexIn(text) >= 0;
}
```

典型流程只有三步：

1. 准备一个生命周期足够长的 Latin-1 模式；
2. 用模式和大小写规则构造 matcher；
3. 对一个或多个 haystack 调用 `indexIn()`。

matcher 不拥有模式数据。构造时只保存模式 view，并建立与模式相关的搜索状态。因此，模式底层的字符数据必须在 matcher 使用期间保持存在且不被修改。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QLatin1StringMatcher>
```

实际使用时通常还需要：

```cpp
#include <QLatin1StringView>
```

如果模式来自 `_L1` 字面量，需要：

```cpp
using namespace Qt::StringLiterals;
```

### 3.3 qmake

```qmake
QT += core
```

## 4. 它在内部维护什么

从公开语义看，一个 matcher 至少维护三类状态：

1. **模式 view**
   - 模式起始地址；
   - 模式长度；
   - 不拥有底层字节。
2. **大小写规则**
   - `Qt::CaseSensitive`；
   - `Qt::CaseInsensitive`。
3. **模式对应的搜索器状态**
   - 用于快速跳过不可能匹配的位置；
   - 模式或大小写规则改变后需要重新建立。

Qt 6.11 的实现使用基于 Boyer-Moore 思路的跳跃表搜索器。大小写不敏感时还会按 Qt 的 Latin-1 大小写折叠规则处理模式和 haystack。这个算法细节是性能实现，不是 API 契约；代码不应依赖内部缓冲区大小、对象布局或具体跳跃次数。

重要的是：matcher 预处理的是**模式**，不是 haystack。haystack 仍然作为 `QLatin1StringView` 或 `QStringView` 在每次 `indexIn()` 调用时传入。

## 5. 实际使用场景

### 5.1 在许多报文中查找同一个协议字段

```cpp
using namespace Qt::StringLiterals;

class HeaderScanner
{
public:
    HeaderScanner()
        : contentTypeMatcher("Content-Type:"_L1, Qt::CaseInsensitive)
    {
    }

    bool hasContentType(QLatin1StringView headerBlock) const
    {
        return contentTypeMatcher.indexIn(headerBlock) >= 0;
    }

private:
    QLatin1StringMatcher contentTypeMatcher;
};
```

这里 matcher 的生命周期覆盖很多次扫描，预处理模式才有价值。

### 5.2 在同一个 haystack 中查找所有出现位置

```cpp
using namespace Qt::StringLiterals;

QList<qsizetype> findAll(QLatin1StringView text)
{
    const QLatin1StringMatcher matcher("TODO"_L1);
    QList<qsizetype> positions;

    qsizetype from = 0;
    while (true) {
        const qsizetype pos = matcher.indexIn(text, from);
        if (pos < 0)
            break;

        positions.append(pos);
        from = pos + 1;
    }

    return positions;
}
```

`from = pos + 1` 的意义是允许匹配重叠出现。例如模式是 `"ana"`，文本是 `"banana"`，继续从前一次位置加一开始，才能找到可能重叠的下一次匹配。

如果业务只允许非重叠匹配，应改为：

```cpp
from = pos + matcher.pattern().size();
```

但要先处理空模式，否则 `pattern().size()` 为零，循环不会前进。

### 5.3 扫描 `QStringView`

Qt 6.8 起，matcher 可以直接接受 `QStringView`：

```cpp
using namespace Qt::StringLiterals;

qsizetype findInUnicodeText(QStringView text)
{
    const QLatin1StringMatcher matcher("error"_L1,
                                       Qt::CaseInsensitive);
    return matcher.indexIn(text);
}
```

这适合模式本身是 Latin-1、而 haystack 已经是 UTF-16 的场景。调用方不需要先把整个 `QStringView` 转成 `QLatin1StringView`，也不能这样做，因为 UTF-16 数据不是 Latin-1 字节序列。

### 5.4 过滤字符串列表

Qt 6.9 起，`QStringList` 提供接受 `QLatin1StringMatcher` 的 `filter()` 重载：

```cpp
#include <QStringList>

using namespace Qt::StringLiterals;

QStringList filterWarnings(const QStringList &lines)
{
    const QLatin1StringMatcher matcher("warning"_L1,
                                       Qt::CaseInsensitive);
    return lines.filter(matcher);
}
```

当列表较大、字符串较长或同一模式反复使用时，这种接口可以把匹配器复用起来。实际收益仍与数据规模有关，应通过基准测试确认。

## 6. 模式生命周期是最重要的边界

### 6.1 字符串字面量是安全模式

```cpp
using namespace Qt::StringLiterals;

const QLatin1StringMatcher matcher("needle"_L1);
```

字符串字面量在整个程序运行期间有效，因此适合作为长期 matcher 的模式。

### 6.2 局部数组不能在 matcher 外销毁

```cpp
QLatin1StringMatcher makeMatcher()
{
    const char pattern[] = "temporary";
    return QLatin1StringMatcher(QLatin1StringView(pattern));
} // pattern 销毁
```

返回的 matcher 内部仍然指向 `pattern`。调用它的 `indexIn()` 会访问已经失效的内存，这是悬空 view 问题，不是 matcher 自动复制失败后的“空匹配”。

如果 matcher 需要返回给调用者，模式也必须由调用者或更长生命周期的对象持有：

```cpp
class SearchContext
{
public:
    explicit SearchContext(QByteArray patternStorage)
        : storage(std::move(patternStorage)),
          matcher(QLatin1StringView(storage))
    {
    }

    qsizetype find(QLatin1StringView haystack) const
    {
        return matcher.indexIn(haystack);
    }

private:
    QByteArray storage;
    QLatin1StringMatcher matcher;
};
```

不过，这种写法还要认真检查成员初始化顺序。C++ 按成员声明顺序初始化，因此拥有模式的 `storage` 必须声明在 `matcher` 之前。

### 6.3 `QByteArray` 不能在使用期间重新分配

```cpp
QByteArray storage = "needle";
QLatin1StringMatcher matcher(QLatin1StringView(storage));
```

上面的 matcher 依赖 `storage` 的数据地址。以下行为可能使 matcher 失效或使它看到错误内容：

- `storage` 被销毁；
- `storage` 被赋值；
- `storage` 扩容并重新分配；
- 共享数据发生分离；
- 通过其他别名修改底层字符。

Qt 文档不仅要求模式“不要销毁”，还要求它在 matcher 被销毁前不要改变。即使地址没有变化，原地改写模式也可能让已经建立的跳跃表与真实字符不一致。

### 6.4 `setPattern()` 不是对临时数据的所有权接管

```cpp
QLatin1StringMatcher matcher;

QByteArray storage = "first";
matcher.setPattern(QLatin1StringView(storage));
```

调用 `setPattern()` 后，`matcher` 仍然只是引用 `storage`。`setPattern()` 不会把 `storage` 复制进 matcher。

如果先设置一个短生命周期模式，再在它销毁前切换到更长生命周期模式，旧模式的生命周期要求可以随切换结束：

```cpp
QLatin1StringMatcher matcher;

{
    QByteArray temporary = "old";
    matcher.setPattern(QLatin1StringView(temporary));

    static constexpr auto permanent = "new"_L1;
    matcher.setPattern(permanent);
} // matcher 当前不再引用 temporary
```

这里的前提是第二次 `setPattern()` 已经把 matcher 切换到新的、仍然有效的模式。

## 7. 大小写规则

### 7.1 构造时指定

```cpp
using namespace Qt::StringLiterals;

QLatin1StringMatcher sensitive("Header"_L1,
                               Qt::CaseSensitive);
QLatin1StringMatcher insensitive("Header"_L1,
                                 Qt::CaseInsensitive);
```

默认值是 `Qt::CaseSensitive`。

### 7.2 Latin-1 大小写不敏感不是“原始字节相等”

大小写不敏感模式会按 Qt 的 Latin-1 字符折叠规则比较，而不是按字节完全相等比较。对于 ASCII 模式，通常就是熟悉的大小写忽略；对于 `0x80..0xFF` 范围的字符，应由数据的 Latin-1 语义和 Qt 的折叠规则决定。

如果协议要求严格匹配原始字节，使用 `Qt::CaseSensitive`。如果数据实际是 UTF-8，不要为了“忽略大小写”把它强行包装为 Latin-1；应使用适合 UTF-8/Unicode 的处理方案。

### 7.3 修改规则会重建搜索状态

```cpp
matcher.setCaseSensitivity(Qt::CaseInsensitive);
```

切换大小写规则会使原模式对应的搜索状态重新准备。频繁在两个规则之间切换，会削弱预处理带来的收益；如果两种规则都需要长期使用，通常建立两个 matcher 更清楚：

```cpp
const QLatin1StringMatcher exact("status"_L1);
const QLatin1StringMatcher folded("status"_L1,
                                  Qt::CaseInsensitive);
```

## 8. `indexIn()` 的返回值与搜索范围

所有 `indexIn()` 重载都返回 `qsizetype`：

- `0` 或更大：匹配起始位置；
- `-1`：没有找到匹配。

位置是 haystack 内的索引，不是底层缓冲区的字节地址。对 `QStringView` haystack，返回的是 UTF-16 code unit 索引；对 `QLatin1StringView` haystack，返回的是 Latin-1 字节索引。

### 8.1 `from == 0`

默认从 haystack 的第一个位置开始：

```cpp
const qsizetype pos = matcher.indexIn(haystack);
```

等价于：

```cpp
const qsizetype pos = matcher.indexIn(haystack, 0);
```

### 8.2 正数 `from`

正数表示从该索引位置开始向后搜索。它不是“跳过 `from` 个字符后再从下一个位置开始”，而是允许从 `from` 这个位置本身形成匹配。

```cpp
using namespace Qt::StringLiterals;

const QLatin1StringMatcher matcher("ana"_L1);
const QLatin1StringView text("banana"_L1);

Q_ASSERT(matcher.indexIn(text, 0) == 1);
Q_ASSERT(matcher.indexIn(text, 2) == 3);
```

### 8.3 负数 `from`

Qt 的字符串搜索 API 支持用负数表示“从末尾向前偏移”：

- `-1`：从最后一个位置开始；
- `-2`：从倒数第二个位置开始；
- 更小的负数继续向前移动。

例如：

```cpp
using namespace Qt::StringLiterals;

const QLatin1StringMatcher matcher("n"_L1);
const QLatin1StringView text("banana"_L1);

Q_ASSERT(matcher.indexIn(text, -1) == -1); // 从位置 5 开始，只有 'a'
Q_ASSERT(matcher.indexIn(text, -2) == 4);  // 从位置 4 开始
```

实际代码应让换算后的位置仍在有效范围内。不要把任意极小负数当作“自动钳制到零”的安全写法；需要从开头搜索时直接传 `0`，需要从某个已知位置搜索时传非负索引。

### 8.4 `from` 到达末尾

对非空模式，`from == haystack.size()` 时已经没有足够位置开始匹配，结果为 `-1`。

空模式是例外：空字符串按字符串匹配语义可以在每个位置匹配，包括末尾位置。Qt 文档明确说明默认构造的空 matcher 会在任意字符串的每个位置匹配。因此处理空模式时，不能把“`from == size()` 返回 `-1`”作为通用规则。

### 8.5 haystack 为空

空 haystack 上：

- 非空模式没有匹配，返回 `-1`；
- 空模式可以匹配唯一的边界位置 `0`。

如果业务上不允许空模式，应在构造或配置阶段主动拒绝，而不要让空 matcher 的语义混入业务逻辑。

## 9. 查找所有匹配：推进规则

### 9.1 允许重叠匹配

```cpp
QList<qsizetype> allOverlapping(QLatin1StringView text,
                                QLatin1StringView pattern)
{
    QLatin1StringMatcher matcher(pattern);
    QList<qsizetype> result;

    for (qsizetype from = 0;;) {
        const qsizetype pos = matcher.indexIn(text, from);
        if (pos < 0)
            break;

        result.append(pos);
        from = pos + 1;
    }

    return result;
}
```

模式为空时，`pos + 1` 仍然会推进；但如果业务不需要收集每个边界位置，最好先单独处理空模式。

### 9.2 不允许重叠匹配

```cpp
QList<qsizetype> allNonOverlapping(QLatin1StringView text,
                                   QLatin1StringView pattern)
{
    QLatin1StringMatcher matcher(pattern);
    QList<qsizetype> result;

    if (pattern.isEmpty())
        return result;

    for (qsizetype from = 0;;) {
        const qsizetype pos = matcher.indexIn(text, from);
        if (pos < 0)
            break;

        result.append(pos);
        from = pos + pattern.size();
    }

    return result;
}
```

### 9.3 不要用 `contains()` 再循环 `indexIn()`

matcher 本身已经提供位置查找。如果需要位置，直接调用 `indexIn()`；先调用布尔查询再调用位置查询会重复扫描。

## 10. 默认构造的空 matcher

```cpp
QLatin1StringMatcher matcher;
```

这不是“无效对象”或“永远匹配失败”的状态。Qt 文档定义它包含空模式，会在任意字符串的每个位置匹配。

可以随后配置：

```cpp
using namespace Qt::StringLiterals;

QLatin1StringMatcher matcher;
matcher.setPattern("needle"_L1);
matcher.setCaseSensitivity(Qt::CaseInsensitive);
```

默认 matcher 的 `pattern()` 是空的 `QLatin1StringView`。如果代码把“默认构造”当作尚未配置状态，应额外用 `pattern().isEmpty()` 或自己的状态位表达业务含义；不要依赖 `indexIn()` 返回 `-1` 来判断是否配置。

## 11. 模式更换的语义

### 11.1 `setPattern()` 会改变后续搜索目标

```cpp
using namespace Qt::StringLiterals;

QLatin1StringMatcher matcher("old"_L1);
Q_ASSERT(matcher.indexIn("old value"_L1) == 0);

matcher.setPattern("new"_L1);
Q_ASSERT(matcher.indexIn("new value"_L1) == 0);
```

更换模式后，后续 `indexIn()` 使用新模式。返回的 `pattern()` 也是新 view。

### 11.2 同一地址同一长度不是安全的“刷新”

模式底层数据不能在 matcher 使用期间改变。一个特别容易被忽略的情况是：

```cpp
char pattern[] = "abc";
QLatin1StringMatcher matcher(QLatin1StringView(pattern));

pattern[0] = 'x'; // 不要这样做
matcher.setPattern(QLatin1StringView(pattern));
```

这里地址和长度都没有变化。实现可能把它视为同一个模式，不会按“内容已经改变”重新建立所有搜索状态。正确做法是：

- 不要在 matcher 存活期间改写模式；
- 使用新的稳定缓冲区并调用 `setPattern()`；
- 或直接创建新的 matcher。

### 11.3 先切换到长生命周期模式，再销毁旧模式

Qt 文档允许通过 `setPattern()` 先改指向另一个生命周期更长的模式，然后销毁旧模式。关键顺序不能反：

```text
旧模式仍有效 -> setPattern(新模式) -> 旧模式销毁
```

不能：

```text
旧模式销毁 -> matcher 仍引用旧模式 -> 再尝试修复
```

## 12. 与 `QLatin1StringView::indexOf()` 的选型

| 情况 | 推荐 API | 原因 |
| --- | --- | --- |
| 只查一次短文本 | `haystack.indexOf(pattern)` | 代码直接，matcher 预处理没有机会摊薄。 |
| 同一模式查很多 haystack | `QLatin1StringMatcher` | 模式搜索状态可以复用。 |
| 同一 haystack 查同一模式的多次位置 | `QLatin1StringMatcher` | 避免每次从头建立模式相关状态。 |
| 模式在编译期固定，甚至只查一次 | `QStaticLatin1StringMatcher` | 内部表示在编译期建立。 |
| 模式需要动态改写或拥有化 | `QString`/`QByteArray` 加相应 matcher | `QLatin1StringMatcher` 不拥有模式。 |
| 输入是 UTF-16，模式是 Latin-1 | Qt 6.8 起 `QLatin1StringMatcher::indexIn(QStringView)` | 不需要复制整个 haystack。 |

是否更快与模式长度、haystack 长度、重复次数和字符分布有关。文档给的是适用方向，不是无条件的性能保证。

## 13. 与相近类型的边界

### 13.1 `QLatin1StringView`

`QLatin1StringView` 是借用型字符串视图，提供通用的 `indexOf()`、比较、切片和转换 API。它适合单次搜索或不需要保存预处理状态的代码。

`QLatin1StringMatcher` 则把“待查找的模式”提升成可复用对象：

```cpp
const qsizetype oneShot =
    text.indexOf(pattern);

const QLatin1StringMatcher reusable(pattern);
const qsizetype repeated =
    reusable.indexIn(text);
```

两者都不拥有模式；`QLatin1StringMatcher` 也不会因为自己是一个命名对象就自动延长模式生命周期。

### 13.2 `QStringMatcher`

`QStringMatcher` 面向 UTF-16/`QStringView` 模式。它通常适合模式本身就是 Unicode 文本、需要 `QString` 所有权或已经处于 UTF-16 数据模型的场景。

选择 `QLatin1StringMatcher` 的前提是模式明确为 Latin-1。不要为了调用某个重载而把任意 UTF-8 字节包装成 Latin-1。

### 13.3 `QByteArrayMatcher`

`QByteArrayMatcher` 的语义是原始字节匹配；它不把字节解释成 Latin-1 字符，也不提供大小写不敏感的文本语义。

| 输入真实含义 | 适合类型 |
| --- | --- |
| 明确是 Latin-1 文本 | `QLatin1StringMatcher` |
| 明确是 UTF-16 文本 | `QStringMatcher` |
| 任意原始字节 | `QByteArrayMatcher` |
| 明确是 UTF-8 文本 | `QUtf8StringView`/Unicode 处理方案 |

### 13.4 `QStaticLatin1StringMatcher`

`QStaticLatin1StringMatcher` 是编译期版本，适合模式是字符串字面量、需要把搜索器状态在编译期准备好的场景。它没有 `setPattern()` 和 `setCaseSensitivity()`，因为模式和大小写规则是类型参数的一部分。

动态 matcher：

```cpp
using namespace Qt::StringLiterals;
const QLatin1StringMatcher matcher("needle"_L1);
```

静态 matcher：

```cpp
constexpr auto matcher =
    qMakeStaticCaseSensitiveLatin1StringMatcher("needle");
```

静态版本要求模式长度满足其实现约束，不能把它当作动态 matcher 的完全替代品。尤其是很短的单字符模式没有必要使用 Boyer-Moore 风格的 matcher。

## 14. `QStringView` haystack 重载的版本边界

```cpp
qsizetype indexIn(QStringView haystack, qsizetype from = 0) const;
```

这是 Qt 6.8 新增的重载。它允许：

- 模式仍然是 Latin-1；
- haystack 是 UTF-16；
- 返回 UTF-16 code unit 索引；
- 不先复制或整体转换 haystack。

它不表示 matcher 可以接受任意 `QString`、`QUtf8StringView` 或 `QByteArray` 的隐式重载。需要使用其他编码时，应选择相应类型的 matcher 或先明确转换。

## 15. 线程、重入与并发修改

matcher 是普通值类型风格对象，不依赖事件循环，也不是 QObject。搜索调用本身不需要 GUI 线程或事件循环。

但“普通对象”不等于“可以无锁共享并同时修改”：

- 并发线程只读同一个 matcher 和同一模式，通常符合只读使用模型；
- 一个线程调用 `setPattern()` 或 `setCaseSensitivity()`，另一个线程同时调用 `indexIn()`，需要外部同步；
- 模式底层缓冲区不能被另一个线程同时修改；
- haystack view 的底层数据也必须在搜索期间保持有效。

如果模式是共享的 `QByteArray`，还要考虑另一个线程的写操作是否触发隐式共享分离或重新分配。

## 16. 性能使用建议

### 16.1 让 matcher 跨越真正的重复工作

不推荐：

```cpp
for (QLatin1StringView line : lines) {
    QLatin1StringMatcher matcher("error"_L1);
    if (matcher.indexIn(line) >= 0)
        handle(line);
}
```

推荐：

```cpp
const QLatin1StringMatcher matcher("error"_L1,
                                   Qt::CaseInsensitive);
for (QLatin1StringView line : lines) {
    if (matcher.indexIn(line) >= 0)
        handle(line);
}
```

### 16.2 不要为了“一次查找”过度抽象

```cpp
if (text.indexOf("error"_L1) >= 0)
    handle();
```

这通常比创建一次性 matcher 更简单。matcher 的收益来自模式状态的复用，不来自类型名称本身。

### 16.3 长模式和大量候选文本更容易体现收益

模式越长、haystack 越长、重复搜索越多，跳跃表越有机会减少比较次数。短字符串或很少重复的搜索，函数调用、对象初始化和数据分布可能让差异不明显。

### 16.4 以基准测试决定

若性能是选择 matcher 的理由，应使用项目真实数据测试：

- 模式长度；
- haystack 长度；
- 命中率；
- 匹配位置分布；
- 大小写规则；
- 是否重复搜索同一个 haystack；
- 编译器和目标平台。

不要仅凭“Boyer-Moore 一定更快”做结论。

## 17. 常见误区与排查顺序

### 17.1 把 matcher 当成拥有模式的容器

错误假设：

```text
matcher 保存了 pattern 的副本，因此原 QByteArray 可以随时销毁。
```

正确理解：matcher 保存 view 和搜索状态，模式底层数据必须继续有效。

排查顺序：

1. 找到 `pattern` 的实际拥有者；
2. 确认拥有者比 matcher 活得更久；
3. 检查是否有重新分配、赋值、分离或原地修改；
4. 若无法保证，改为保存 `QString`/`QByteArray` 并让它先于 matcher 构造。

### 17.2 模式是 UTF-8 却使用 Latin-1 matcher

```cpp
const char utf8[] = "\xC3\xA9";
QLatin1StringMatcher matcher(QLatin1StringView(utf8, 2));
```

这里匹配的是两个 Latin-1 字符，不是 Unicode 字符 `é`。编码必须由输入协议决定。

### 17.3 用 `setPattern()` 修复已被改写的同一缓冲区

如果模式地址和长度都没变，重新传入同一个 view 不一定触发搜索状态重建。不要修改模式后再调用 `setPattern()` 期待刷新；使用新缓冲区或新 matcher。

### 17.4 负 `from` 误当作任意安全输入

负数是相对末尾的索引表达，不是“自动从零开始”的错误恢复机制。外部输入未经验证时，应先规范化为合法的非负索引。

### 17.5 空 matcher 被误判为未初始化

默认构造 matcher 的模式是空模式，文档定义它可以在每个位置匹配。若业务有“尚未设置模式”的状态，单独表示这个状态。

### 17.6 收集所有匹配时循环不前进

非重叠循环如果写成：

```cpp
from = pos + pattern.size();
```

必须先排除空模式。否则 `pattern.size()` 为零，下一轮仍从同一位置开始。

### 17.7 把大小写不敏感当成 locale-aware 比较

`QLatin1StringMatcher` 是 Latin-1 专用匹配器，不是面向用户语言排序、区域规则或复杂 Unicode 正规化的工具。需要本地化文本比较、大小写折叠或规范化时，应使用适合 Unicode 的 API。

## 18. 逐项 API 说明

### 18.1 默认构造

```cpp
QLatin1StringMatcher()
```

构造一个空 Latin-1 matcher。它的模式为空，按文档语义可以在任意 haystack 的每个位置匹配。

它适合：

- 先默认构造，再通过 `setPattern()` 配置；
- 作为需要可重新配置的成员对象。

它不适合被当成“没有模式就永远失败”的哨兵。需要这种业务语义时，应显式增加状态。

### 18.2 带模式构造

```cpp
explicit QLatin1StringMatcher(
    QLatin1StringView pattern,
    Qt::CaseSensitivity cs = Qt::CaseSensitive)
```

使用给定 Latin-1 模式和大小写规则构造 matcher。

注意：

- `pattern` 只是 view；
- 模式数据不能在 matcher 销毁前销毁或修改；
- `cs` 默认是 `Qt::CaseSensitive`；
- 该构造函数从 Qt 6.5 开始提供。

### 18.3 析构函数

```cpp
~QLatin1StringMatcher()
```

销毁 matcher 并释放其内部搜索器状态。它不会释放模式数据，因为模式数据不由 matcher 拥有。

如果 matcher 和模式拥有者是同一对象的成员，声明顺序必须让模式拥有者先构造、后析构：

```cpp
class GoodOrder
{
    QByteArray storage;
    QLatin1StringMatcher matcher;
};
```

### 18.4 `caseSensitivity()`

```cpp
Qt::CaseSensitivity caseSensitivity() const
```

返回 matcher 当前使用的大小写规则：

- `Qt::CaseSensitive`；
- `Qt::CaseInsensitive`。

它只查询配置，不执行搜索。

### 18.5 `indexIn(QLatin1StringView, qsizetype)`

```cpp
qsizetype indexIn(QLatin1StringView haystack,
                  qsizetype from = 0) const
```

在 Latin-1 haystack 中，从 `from` 位置开始查找 matcher 的模式，返回首次匹配位置；找不到返回 `-1`。

使用时重点确认：

- haystack 的数据在调用期间有效；
- `from` 是 haystack 内索引；
- 结果是索引而不是指针；
- 负 `from` 表示从末尾反向偏移；
- 空模式有独立的边界语义；
- 同一 matcher 可以安全地对多个 haystack 重复调用，只要模式和 matcher 配置不被并发修改。

### 18.6 `indexIn(QStringView, qsizetype)`

```cpp
qsizetype indexIn(QStringView haystack,
                  qsizetype from = 0) const
```

在 UTF-16 `QStringView` haystack 中查找 Latin-1 模式。返回位置是 `QStringView` 的 UTF-16 code unit 索引。

该重载从 Qt 6.8 开始提供。它避免了为了搜索而复制或整体转换 UTF-16 haystack。

它不改变 matcher 模式的编码：模式仍然是 Latin-1，haystack 才是 UTF-16。

### 18.7 `pattern()`

```cpp
QLatin1StringView pattern() const
```

返回当前模式的非拥有 view。

```cpp
const auto current = matcher.pattern();
```

返回值仍然依赖原模式数据。把 `pattern()` 返回值保存起来不会延长底层数据生命周期。

### 18.8 `setCaseSensitivity(Qt::CaseSensitivity)`

```cpp
void setCaseSensitivity(Qt::CaseSensitivity cs)
```

修改后续搜索使用的大小写规则，并按需要重建内部搜索状态。

它不会复制或改变模式数据。若模式缓冲区已经失效，先调用这个函数也不能修复悬空引用。

### 18.9 `setPattern(QLatin1StringView)`

```cpp
void setPattern(QLatin1StringView pattern)
```

把 matcher 的搜索目标改为新的 Latin-1 模式，并更新内部搜索状态。

调用方必须保证：

- 新模式数据在 matcher 后续使用期间有效；
- 新模式内容不被修改；
- 若要让旧模式立即失效，必须先切换到有效的新模式；
- 不要通过原地修改同一地址同一长度的数据来“更新模式”。

## API 速查表
下表按 Qt 6.11.1 的公开 API 逐项列出。

| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QLatin1StringMatcher()` | 构造空模式 matcher。 | 空模式可在每个位置匹配，不等于“永远失败”。 |
| 构造 | `explicit QLatin1StringMatcher(QLatin1StringView pattern, Qt::CaseSensitivity cs = Qt::CaseSensitive)` | 为 Latin-1 模式建立可复用搜索器。 | `pattern` 不被复制；必须保持有效且不被修改。 |
| 析构 | `~QLatin1StringMatcher()` | 销毁 matcher 的内部搜索状态。 | 不释放模式底层数据。 |
| 查询 | `Qt::CaseSensitivity caseSensitivity() const` | 返回当前大小写规则。 | 只查询配置，不执行匹配。 |
| 搜索 | `qsizetype indexIn(QLatin1StringView haystack, qsizetype from = 0) const` | 在 Latin-1 haystack 中查找模式。 | 找不到返回 `-1`；可反复调用；负 `from` 按末尾偏移。 |
| 搜索 | `qsizetype indexIn(QStringView haystack, qsizetype from = 0) const` | 在 UTF-16 haystack 中查找 Latin-1 模式。 | Qt 6.8 起；返回 UTF-16 code unit 索引。 |
| 查询 | `QLatin1StringView pattern() const` | 返回当前模式 view。 | 不拥有数据，不延长生命周期。 |
| 配置 | `void setCaseSensitivity(Qt::CaseSensitivity cs)` | 修改大小写规则并更新搜索状态。 | 频繁切换会削弱预处理收益；并发调用需同步。 |
| 配置 | `void setPattern(QLatin1StringView pattern)` | 替换搜索模式并更新搜索状态。 | 新模式必须有效；不要原地改写同地址同长度的旧模式。 |

## 20. 常用代码模板

### 20.1 多个 haystack 复用一个模式

```cpp
using namespace Qt::StringLiterals;

const QLatin1StringMatcher matcher("timeout"_L1,
                                   Qt::CaseInsensitive);

for (QLatin1StringView message : messages) {
    if (matcher.indexIn(message) >= 0)
        handleTimeout(message);
}
```

### 20.2 在 `QStringView` 中查找 Latin-1 模式

```cpp
using namespace Qt::StringLiterals;

const QLatin1StringMatcher matcher("http"_L1,
                                   Qt::CaseInsensitive);
const qsizetype position = matcher.indexIn(QStringView(document));
```

### 20.3 可重新配置但保持拥有者顺序

```cpp
class Parser
{
public:
    explicit Parser(QByteArray keyword)
        : keywordStorage(std::move(keyword)),
          matcher(QLatin1StringView(keywordStorage))
    {
    }

    void setKeyword(QByteArray keyword)
    {
        keywordStorage = std::move(keyword);
        matcher.setPattern(QLatin1StringView(keywordStorage));
    }

private:
    QByteArray keywordStorage;
    QLatin1StringMatcher matcher;
};
```

这个示例的 `setKeyword()` 会先替换拥有者，再让 matcher 指向新的存储。实际工程还应保证在 matcher 使用期间没有其他线程读取或修改这两个对象。

### 20.4 一次性查找使用 `indexOf()`

```cpp
using namespace Qt::StringLiterals;

if (line.indexOf("ERROR"_L1) >= 0)
    report(line);
```

不需要为一次搜索创建 matcher。

## 21. 最后记住这几条

1. `QLatin1StringMatcher` 的价值在于**重复搜索同一模式**。
2. 它只借用模式数据，不拥有模式。
3. 模式在 matcher 使用期间不能销毁，也不能修改。
4. `setPattern()` 会切换模式，但不会接管字符串所有权。
5. `setCaseSensitivity()` 改变后续匹配规则，并需要更新搜索状态。
6. `indexIn()` 找不到返回 `-1`，返回位置是 haystack 内索引。
7. `QStringView` 重载从 Qt 6.8 开始提供，返回 UTF-16 code unit 索引。
8. 空 matcher 的模式为空，按文档语义可以在每个位置匹配。
9. 一次性匹配通常直接用 `QLatin1StringView::indexOf()`。
10. 编译期固定模式优先比较 `QStaticLatin1StringMatcher` 是否更合适。

`QLatin1StringMatcher` 可以看成“带模式预处理的 Latin-1 `indexOf()`”。只要把模式的编码、所有权、生命周期和重复次数判断清楚，它的适用边界就很明确：**动态但稳定的 Latin-1 模式，配合多次搜索；一次性查找则保持简单。**
