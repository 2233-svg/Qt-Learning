# Qt QCollatorSortKey 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCollatorSortKey>`  
> 所属模块：`Qt6::Core`  
> 核心定位：预计算的本地化字符串排序键

## 1. 它解决什么问题

按语言规则比较两个字符串可能不便宜：比较器要处理 locale、大小写、重音、数字段和标点规则。对几十万行模型做排序时，同一字符串会被重复比较很多次，重复执行这些规则会成为热点。

`QCollatorSortKey` 是 `QCollator::sortKey()` 生成的预计算结果。创建 key 的成本通常高于一次 `compare()`，但之后比较两个 key 很快，适合“一批文本需要互相多次比较”的场景。

```text
QCollator configuration
       |
       | sortKey(label)
       v
QCollatorSortKey for each label
       |
       | compare() or operator<
       v
fast repeated ordering
```

它不是字符串，不可自行构造，也不能用来恢复原始文本；它只是某套排序规则下的比较令牌。

## 2. 最重要的契约：必须来自同一个 collator

两个 `QCollatorSortKey` 只有在由**同一个 `QCollator` 的 `sortKey()`** 产生时，才允许通过 `compare()` 或 `operator<` 比较。

这里的“同一个”不仅是类型相同，更是同一套排序语义：

- 相同的 locale。
- 相同的大小写敏感度。
- 相同的 numeric mode。
- 相同的 ignore punctuation 设置。

```cpp
QCollator english(QLocale::English);
QCollator french(QLocale::French);

const auto enKey = english.sortKey("resume");
const auto frKey = french.sortKey("resume");

// enKey.compare(frKey); // 不允许：创建者不是同一个 QCollator。
```

改了 collator 的任一设置后，旧 key 也应全部视为过期并重建。不要把 key 写进数据库、跨进程发送或在应用升级后复用，因为底层 locale 数据与 collation 实现也可能变化。

## 3. 最小可用示例

```cpp
#include <QCollator>
#include <QCollatorSortKey>
#include <QString>
#include <QVector>
#include <algorithm>

struct Item {
    QString title;
    QCollatorSortKey key;
};

void sortItems(QVector<Item> &items, const QLocale &locale)
{
    QCollator collator(locale);
    collator.setNumericMode(true);

    for (Item &item : items) {
        item.key = collator.sortKey(item.title);
    }

    std::sort(items.begin(), items.end(),
              [](const Item &left, const Item &right) {
                  return left.key < right.key;
              });
}
```

如果 `title` 被编辑，或用户切换了语言、数字排序、大小写敏感度，必须为受影响条目重新调用 `sortKey()`。仅更新 `title` 而保留旧 key，会让列表的显示文字与实际排序依据脱节。

## 4. 何时值得缓存 key

| 情况 | 是否推荐 | 原因 | 方案 |
| --- | --- | --- | --- |
| 比较两个字符串一次 | 不推荐 | 生成 key 的开销通常更高。 | 直接 `QCollator::compare()`。 |
| 对小列表排序一次 | 视情况而定 | 比较次数有限，直接用 collator 常已足够。 | `std::sort(..., collator)`。 |
| 大列表频繁排序、筛选或二分查询 | 推荐 | 将复杂 collation 从重复比较移到预计算阶段。 | 缓存每项 `QCollatorSortKey`。 |
| locale 或排序选项经常变化 | 谨慎 | key 需要整体失效重建。 | 先衡量重建成本，必要时延迟重建。 |

它是一种时间换空间的缓存。保存 key 会占额外内存，并增加数据变更时的失效管理；只有实际测量显示排序比较是瓶颈时才需要引入。

## 5. 复制、移动与生命周期

`QCollatorSortKey` 是隐式共享值类型，能复制、赋值、移动和交换。它不依赖 `QObject`、事件循环或线程 affinity，可以作为模型条目的普通成员。

但是“值对象可以复制”不等于“可以任意混用”。复制只保留同一 key 的排序语义；它不会让来自不同 collator 的 key 变得可比较。

移动构造与移动赋值从 Qt 6.8 起明确提供。被移动后的对象进入部分形成状态，只应销毁或被重新赋值。

## 6. 常见错误

### 6.1 用不同 locale 的 key 做比较

这违反 API 契约，结果没有定义为哪一种语言规则。把 key 与生成它的排序配置视为同一个缓存域。

### 6.2 以为 key 会随原字符串自动更新

不会。它是生成时的快照；源字符串改动后需要重新生成。

### 6.3 一次性排序也批量生成 key

创建 key 通常比直接 compare 慢。先用 `QCollator` 谓词排序，只有多次比较场景才缓存 key。

### 6.4 把 key 当作可持久化的排序字段

locale 数据、Qt 版本、系统后端或配置变化都可能改变 key 的意义。持久化原始字符串和排序配置，运行时重建 key。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 创建来源 | `QCollator::sortKey(const QString &string) const` | 用某个 collator 的当前配置为字符串生成排序键。 | key 只可与同一 collator 生成的 key 比较；配置变化后必须重建。 |
| 复制 | `QCollatorSortKey(const QCollatorSortKey &other)` | 复制一个排序键。 | 保留同一排序语义，但不保存或引用原始字符串。 |
| 移动 | `QCollatorSortKey(QCollatorSortKey &&other) noexcept` | 移动构造排序键。 | Qt 6.8 起提供；源对象之后只应析构或赋新值。 |
| 析构 | `~QCollatorSortKey() noexcept` | 销毁排序键。 | 无 QObject 生命周期或事件循环依赖。 |
| 复制赋值 | `QCollatorSortKey &operator=(const QCollatorSortKey &other)` | 用另一 key 覆盖当前 key。 | 覆盖后它对应的原字符串和排序配置也随之改变。 |
| 移动赋值 | `QCollatorSortKey &operator=(QCollatorSortKey &&other) noexcept` | 移动赋值另一 key。 | 移动后源对象处于部分形成状态。 |
| 比较 | `int compare(const QCollatorSortKey &otherKey) const` | 按创建它们的 collator 规则三路比较两个 key。 | 两边必须由同一个 collator 的 `sortKey()` 创建。 |
| 排序 | `bool operator<(const QCollatorSortKey &lhs, const QCollatorSortKey &rhs)` | 判断左 key 是否应排在右 key 前。 | 同样要求同一 collator 来源，可直接用于 `std::sort()`。 |
| 交换 | `void swap(QCollatorSortKey &other) noexcept` | 快速交换两个 key 的内部数据。 | 交换后每个变量对应的原始文本和缓存域也随之交换。 |

---

### 一句话总结

`QCollatorSortKey` 是本地化排序的缓存结果：生成慢、重复比较快；它必须与生成它的那一套 `QCollator` 配置绑定，数据或排序规则变化后就要重建。
