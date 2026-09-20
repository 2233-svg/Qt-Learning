# Qt QCollator 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCollator>`  
> 所属模块：`Qt6::Core`  
> 核心定位：按 `QLocale` 的语言排序规则比较字符串

## 1. 它解决什么问题

按 UTF-16 代码单元比较字符串很快，但不等于人们预期的字典顺序。比如大小写、重音、数字片段、连字符和不同语言的字母顺序，都可能让 `QString::operator<` 的结果不适合显示给用户。

`QCollator` 把一套 `QLocale` 的 collation 规则封装为可复用比较器：

```text
QString values
    |
    | QCollator(locale, options)
    v
locale-aware ordering
    |
    +-- compare() for occasional comparisons
    +-- operator() for std::sort
    +-- sortKey() for repeated comparisons
```

它适合文件列表、联系人、按名称排序的模型、搜索结果和任何“用户会看见排序结果”的列表。它不适合协议字段、数据库唯一键、稳定的跨机器排序或安全比较；这些需求应使用明确且不随 locale 变化的字节或代码点规则。

## 2. 最小可用示例

```cpp
#include <QCollator>
#include <QLocale>
#include <QStringList>
#include <algorithm>

QStringList sortForUser(QStringList names)
{
    QCollator collator(QLocale(QLocale::German, QLocale::Germany));
    collator.setCaseSensitivity(Qt::CaseInsensitive);

    std::sort(names.begin(), names.end(), collator);
    return names;
}
```

`QCollator::operator()` 返回“左边是否应排在右边之前”，所以可直接传给 `std::sort()`。`compare()` 则返回负数、零或正数，适合三路比较、模型排序函数或需要区分相等的代码。

## 3. locale 是排序规则的一部分

默认构造使用默认 locale 的**排序 locale**。系统 locale 的排序规则可能与界面 locale 不同，例如 Unix 环境中 `LC_COLLATE` 可与 `LANG` 不一致。

```cpp
QCollator appOrder;                  // 使用默认 collation locale
QCollator fixedOrder(QLocale::c());  // 使用明确、稳定的 C locale 规则
```

在一个列表生命周期内，最好固定 collator 的 locale 和选项。用户切换应用语言或系统 locale 后，重新构造比较器、重建 sort key 并重新排序；不要让同一已排序容器混用两套不同规则。

## 4. 三个会改变结果的选项

### 4.1 大小写敏感度

默认是 `Qt::CaseSensitive`。设为 `Qt::CaseInsensitive` 后，大小写不再影响主排序结果。

```cpp
collator.setCaseSensitivity(Qt::CaseInsensitive);
```

大小写规则仍依赖 locale。尤其在 C locale 中，大小写敏感时小写字母通常整体排在大写字母之后，可能与用户所在语言预期不同。

### 4.2 数字模式

数字模式让连续数字按数值段比较，而不是逐个字符比较：

```cpp
collator.setNumericMode(true);
```

常见效果是让 `file2` 排在 `file10` 前面。它适合人类文件名、版本标签或章节标题；不适合需要字面词典顺序的协议字段，也不应把它当作严格的语义化版本比较器。

### 4.3 忽略标点

```cpp
collator.setIgnorePunctuation(true);
```

启用后，字符串比较时仿佛移除了标点和符号。它适合联系人或搜索类的宽松排序，但会让不同原始字符串比较为相等；排序后仍需要二级规则，例如原始字符串代码点比较，来得到稳定的最终顺序。

## 5. `compare()` 和 `sortKey()` 如何选择

比较次数决定选择：

| 情况 | 推荐 API | 原因 | 代价 |
| --- | --- | --- | --- |
| 偶尔比较两项 | `compare()` | 不产生额外排序键。 | 每次都执行 locale collation。 |
| `std::sort()` 一组很小或一次性的列表 | `operator()` | 代码简洁，内部调用 `compare()`。 | 可能多次重复处理同一字符串。 |
| 同一批大量字符串反复排序或二分查找 | `sortKey()` | 先把 collation 结果预计算。 | 创建 key 通常比单次 `compare()` 慢且占内存。 |

```cpp
struct Row {
    QString label;
    QCollatorSortKey key;
};

QCollator collator(locale);
for (Row &row : rows) {
    row.key = collator.sortKey(row.label);
}
std::sort(rows.begin(), rows.end(),
          [](const Row &a, const Row &b) { return a.key < b.key; });
```

sort key 只对应生成它时的 collator 语义。改变 locale、case sensitivity、numeric mode 或 punctuation 设置后，旧 key 不应继续与新 key 混合比较，应全部重建。

## 6. 静态默认 API

`defaultCompare()` 和 `defaultSortKey()` 从 Qt 6.3 提供，分别等价于在临时默认构造 `QCollator` 上调用 `compare()` 和 `sortKey()`。

```cpp
const int order = QCollator::defaultCompare(left, right);
```

它们适合一两次直接按当前默认排序 locale 比较。批量排序不要在比较器里反复调用静态函数：保存一个 `QCollator` 能表达配置，也能避免每次重复构造与读取默认 locale。

## 7. 平台后端限制

Qt 在 Unix 上通常使用 ICU；macOS 默认使用等效的 Apple API。但如果 Qt 在编译时没有 ICU，或明确禁用了 ICU，会回退到 POSIX 后端。该后端有实质限制：

- 仅支持 `QLocale::c()` 和 `QLocale::system()`。
- 只支持大小写敏感排序。
- 不支持 numeric mode 和 ignore punctuation。
- 使用不支持的选项时，Qt 会输出警告。

因此跨机器或嵌入式部署中，不要只在开发机验证 locale 排序。若产品依赖特定语言的排序、自然数字顺序或忽略符号，测试目标 Qt 构建的实际后端和 locale 数据。

## 8. 值语义、复制与线程

`QCollator` 是隐式共享值类型，可以复制、赋值和移动。复制表示得到同一配置的独立值语义对象；修改某一个副本的配置时，Qt 会按需要分离其共享数据。

它不依赖事件循环，也没有 QObject 线程归属。为了让排序结果可复现，仍应避免多线程在同一实例上同时调用 setter 和 compare；常见模式是先配置完成，再把副本按值交给各个只读排序任务。

移动后的 `QCollator` 只允许析构或重新赋值，不能继续当作完整可用比较器使用。

## 9. 常见错误

### 9.1 用 `QString::operator<` 给用户排序

它按代码单元顺序，不会遵循当前语言的 collation。显示名、文件名和联系人等用户界面数据使用 `QCollator`。

### 9.2 把 locale 排序结果用作持久化顺序

语言规则和系统库版本都可能变化。数据库主键、同步协议和审计日志需要显式稳定规则，而非用户 locale。

### 9.3 反复为同一字符串创建 sort key

sort key 适合缓存；若每次比较都新建 key，通常比直接 `compare()` 更慢。字段或配置变化时再失效重建。

### 9.4 忽略 POSIX 后备实现的警告

警告表示你设置的排序语义没有生效。不要让开发环境 ICU 的结果掩盖部署环境的实际限制。

## API 速查表
### 构造、复制与配置

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QCollator()` | 使用默认 locale 的 collation locale 构造比较器。 | 系统 locale 的 `LC_COLLATE` 可能与界面语言不同。 |
| 构造 | `explicit QCollator(const QLocale &locale)` | 使用指定 locale 构造比较器。 | 面向用户的排序尽量显式指定当前产品 locale。 |
| 复制 | `QCollator(const QCollator &other)` | 复制 collator 的 locale 和选项。 | 值语义，适合给独立排序任务使用。 |
| 移动 | `QCollator(QCollator &&other) noexcept` | 移动 collator 的内部状态。 | 移动后的对象仅应析构或重新赋值。 |
| 析构 | `~QCollator() noexcept` | 销毁 collator。 | 没有 QObject 生命周期或事件循环依赖。 |
| 赋值 | `QCollator &operator=(const QCollator &other)` | 复制另一套排序配置。 | 覆盖后应让相关 sort key 失效重建。 |
| 赋值 | `QCollator &operator=(QCollator &&other) noexcept` | 移动赋值另一套排序配置。 | 源对象进入部分形成状态。 |
| 交换 | `void swap(QCollator &other) noexcept` | 快速交换两个 collator 配置。 | 交换后两边对应的 sort key 语义也随之改变。 |
| locale | `void setLocale(const QLocale &locale)` | 修改排序 locale。 | 修改后重新排序并重建所有缓存的 sort key。 |
| locale | `QLocale locale() const` | 返回当前排序 locale。 | 未设置时是系统默认 collation locale。 |
| 大小写 | `void setCaseSensitivity(Qt::CaseSensitivity cs)` | 设置大小写是否影响排序。 | C locale 的大小写排序与多数自然语言可能不同。 |
| 大小写 | `Qt::CaseSensitivity caseSensitivity() const` | 返回当前大小写敏感度。 | 默认是 `Qt::CaseSensitive`。 |
| 数字 | `void setNumericMode(bool on)` | 让连续数字按数值段排序。 | POSIX 后端可能不支持；不是 semver 比较器。 |
| 数字 | `bool numericMode() const` | 返回是否启用数字模式。 | 需要在目标平台确认后端确实支持。 |
| 标点 | `void setIgnorePunctuation(bool on)` | 设置比较时是否忽略标点和符号。 | 可能增加相等项，必要时添加稳定的二级比较。 |
| 标点 | `bool ignorePunctuation() const` | 返回是否忽略标点。 | POSIX 后端可能不支持。 |

### 比较与排序键

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 三路比较 | `int compare(QStringView s1, QStringView s2) const` | 按配置 locale 比较两个字符串。 | 返回负、零、正；适合临时视图且不分配字符串。 |
| 三路比较 | `int compare(const QString &s1, const QString &s2) const` | 以 `QString` 重载进行相同的 locale 比较。 | 语义与 `QStringView` 重载相同。 |
| 三路比较 | `int compare(const QChar *s1, qsizetype len1, const QChar *s2, qsizetype len2) const` | 比较两段长度明确的 UTF-16 单元范围。 | 指针必须在调用期间有效；Qt 6.4 前长度类型是 `int`。 |
| 排序谓词 | `bool operator()(QStringView s1, QStringView s2) const` | 返回 `s1` 是否排在 `s2` 之前。 | 可直接传给 `std::sort()`。 |
| 排序谓词 | `bool operator()(const QString &s1, const QString &s2) const` | 为 `QString` 提供排序谓词重载。 | 等价于 `compare(s1, s2) < 0`。 |
| 排序键 | `QCollatorSortKey sortKey(const QString &string) const` | 为字符串生成可缓存的比较键。 | 多次比较才值得生成；配置变化后必须重建。 |
| 默认比较 | `static int defaultCompare(QStringView s1, QStringView s2)` | 用默认构造 collator 比较两个字符串。 | Qt 6.3 起提供；批量排序优先复用实例。 |
| 默认排序键 | `static QCollatorSortKey defaultSortKey(QStringView key)` | 用默认构造 collator 生成排序键。 | Qt 6.3 起提供；同样受默认 locale 变化影响。 |

---

### 一句话总结

`QCollator` 用 locale 规则把字符串排成用户真正期望的顺序：一次比较用 `compare()`，批量排序可当谓词，反复比较则缓存 `sortKey()`，同时务必把 locale 与后端能力当成排序语义的一部分。
