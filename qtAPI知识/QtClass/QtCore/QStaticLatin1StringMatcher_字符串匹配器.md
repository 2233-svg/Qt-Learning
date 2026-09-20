# QStaticLatin1StringMatcher：固定 Latin-1 子串的编译期匹配器

> Qt 6.11.1 | `#include <QStaticLatin1StringMatcher>` | 模块：`Qt6::Core` | 模板：`QStaticLatin1StringMatcher<CS, N>`

`QStaticLatin1StringMatcher` 面向编译期已知的 Latin-1 模式，在 `QLatin1StringView` 或 `QStringView` 中高效查找子串。它将模式的匹配预处理放到编译期，适合解析器、标记识别、固定关键字扫描等重复或热点搜索。

它不是通用 Unicode 搜索器。模式来自 Latin-1 字面量，大小写策略和模式在创建后固定；若模式或大小写敏感性需要在运行时改变，应使用 `QLatin1StringMatcher`、`QStringMatcher` 或直接使用字符串的查找 API。

## 推荐写法

```cpp
#include <QStaticLatin1StringMatcher>

static constexpr auto contentType =
    qMakeStaticCaseInsensitiveLatin1StringMatcher("content-type");

bool containsHeader(QStringView line)
{
    return contentType.indexIn(line) >= 0;
}
```

两个工厂函数会自动推导字面量长度与模板参数：

- `qMakeStaticCaseSensitiveLatin1StringMatcher()`：严格区分大小写。
- `qMakeStaticCaseInsensitiveLatin1StringMatcher()`：不区分大小写。

结果应保存到 `static constexpr auto`，这样预计算结果可在编译期完成，也避免每次进入函数都构造匹配器。

## 适合和不适合的场景

适合：

- 在 HTTP、邮件头、配置语言、模板语言中反复查找 ASCII/LATIN-1 关键字。
- 大字符串中常见“前缀多次碰撞”的模式搜索。
- 模式固定在代码中、且不需要正则语义。

不适合：

- 用户输入的关键字或运行时下载的规则。
- 需要 Unicode 大小写折叠、规范化、词边界或正则表达式。
- 单字符模式。实现要求 `N > 2`，也就是字面量模式至少含两个有效字符；单字符直接用现有字符串 API 更直接。

## 返回值、编码与平台边界

`indexIn()` 返回第一个命中的位置，未命中返回 `-1`。`from` 的单位是输入视图的位置；传入外部数据前应验证范围。

`QLatin1StringView` 输入是单字节 Latin-1。`QStringView` 输入是 UTF-16 视图，但待查模式仍是 Latin-1 固定字面量；不要把它误当作任意 Unicode 子串搜索或语言学意义上的大小写比较。

Qt 6.11.1 文档注明：INTEGRITY 操作系统目前不支持该类。跨平台库若需支持该平台，应准备普通字符串查找的替代实现。

## 生命周期与线程

匹配器保存固定模式和预计算状态，不依赖调用时输入的生命周期。静态 `constexpr` 匹配器没有可变状态，可以由多线程同时用于只读搜索；输入的 `QStringView` 或 `QLatin1StringView` 则必须在调用期间保持有效，并遵守其底层字符串的并发访问规则。

## 常见错误

1. **把模式当成可配置项。** 该类没有 `setPattern()` 或 `setCaseSensitivity()`。
2. **用它处理任意 Unicode 规则。** 复杂文本匹配需要选择真正适合的 Unicode/正则 API。
3. **忽略 `-1`。** 未命中后不能直接拿返回值做切片起点。
4. **局部非静态反复构造。** 在热路径中使用 `static constexpr auto` 保存工厂结果。
5. **在 INTEGRITY 目标上无条件依赖它。** 为该平台保留可编译的回退路径。

## API 速查表

| 类别 | API | 语义 | 使用边界 |
| --- | --- | --- | --- |
| 模板参数 | `CS` | 编译期大小写策略，取 `Qt::CaseSensitive` 或 `Qt::CaseInsensitive`。 | 创建后不可修改。 |
| 模板参数 | `N` | 字面量数组长度，用于匹配器与预计算表。 | 实现要求 `N > 2`；工厂函数会自动推导。 |
| 构造 | `QStaticLatin1StringMatcher(QLatin1StringView pattern)` | 直接创建固定模式匹配器。 | 通常优先使用工厂函数，避免手写 `CS`、`N`。 |
| 搜索 | `indexIn(QLatin1StringView haystack, qsizetype from = 0)` | 在 Latin-1 输入中查找模式。 | 返回首个位置或 `-1`；按输入位置计数。 |
| 搜索 | `indexIn(QStringView haystack, qsizetype from = 0)` | 在 UTF-16 `QStringView` 中查找 Latin-1 模式。 | 不是任意 Unicode 正则或规范化搜索。 |
| 工厂 | `qMakeStaticCaseSensitiveLatin1StringMatcher(const char (&)[N])` | 建立大小写敏感的静态匹配器。 | Qt 6.7 起；字面量应是 Latin-1。 |
| 工厂 | `qMakeStaticCaseInsensitiveLatin1StringMatcher(const char (&)[N])` | 建立大小写不敏感的静态匹配器。 | Qt 6.7 起；大小写策略固定。 |

当模式是代码里的固定 Latin-1 关键字时，这个类能让查找接口既清楚又轻量；一旦需求转向动态模式或完整 Unicode 语义，就应换到更合适的工具。
