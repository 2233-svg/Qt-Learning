# QStringList：面向字符串集合的 QList<QString>

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStringList>`  
> CMake：`Qt6::Core`  
> 本质：`QList<QString>` 的字符串专用接口

`QStringList` 是 Qt 里最常见的字符串列表类型。它实际就是 `QList<QString>`，但额外提供了一组
更贴合文本集合的便利操作：拼接成一个字符串、按子串或正则过滤、在所有字符串中批量替换、
按大小写敏感性查找和排序。

它适合保存命令行参数、文件名列表、插件 key、环境变量、用户输入候选项、简单表单的一列文本
和配置项。它不适合承载复杂记录；一旦每行需要多个字段、角色或通知视图更新，就应考虑
`QAbstractItemModel`、`QStandardItemModel` 或自定义结构。

## 值语义、隐式共享与线程

`QStringList` 是隐式共享的值类型。复制一个列表通常是常量时间，两个对象先共享同一份数据；
当其中一个对象被修改时，Qt 会执行 copy-on-write，把数据分离后再改。

```cpp
QStringList a = {"Arial", "Helvetica"};
QStringList b = a;      // 便宜，共享底层数据
b << "Courier";         // b 分离，a 不变
```

这使得按值返回 `QStringList` 很自然，也让函数参数可以按值接收后再决定是否修改。

类函数是可重入的：不同线程操作各自的 `QStringList` 实例是安全的。不要让多个线程在没有同步的
情况下同时读写同一个实例；隐式共享并不把一个对象变成并发容器。

迭代器规则沿用 `QList`。修改列表、触发分离或重分配，都可能让旧迭代器、引用和指针失效。
遍历时修改同一个列表要格外谨慎，通常先收集索引，或使用合适的擦除模式。

## 初始化与基础操作

`QStringList` 继承 `QList<QString>` 的大部分能力，因此 `append()`、`prepend()`、`insert()`、
`removeAt()`、`removeAll()`、`operator[]`、`at()`、`size()`、`isEmpty()` 都可直接使用。

```cpp
QStringList fonts = {"Arial", "Helvetica", "Times"};
fonts << "Courier" << "Verdana";

QString first = fonts.at(0);
fonts.removeAll("Times");
```

还有一个从单个 `QString` 构造的便利构造函数：

```cpp
QStringList one(QStringLiteral("only item"));
```

注意它创建的是“包含一个字符串的列表”，不是按分隔符拆分。拆分字符串应使用
`QString::split()` 或 `QStringView::split()`。

## 查找：整项匹配，不是子串搜索

`contains()`、`indexOf()` 和 `lastIndexOf()` 的字符串重载比较的是列表元素本身是否等于目标
字符串；它们不是在每个元素里做子串搜索。

```cpp
QStringList names = {"Bill Murray", "John Doe", "Bill Clinton"};

names.contains("Bill");          // false
names.indexOf("John Doe");       // 1
names.filter("Bill");            // ["Bill Murray", "Bill Clinton"]
```

若要找“包含某个片段的元素”，使用 `filter()`；若要找第一个满足复杂条件的元素，可手写循环。

`Qt::CaseSensitivity` 控制大小写敏感性。Qt 6.7 起，带 `cs` 的 `indexOf()` / `lastIndexOf()`
重载会遮蔽一部分从 `QList` 继承的旧形态；旧代码通常仍可编译，但新代码应明确传入需要的签名。

正则表达式重载的 `indexOf(const QRegularExpression &)` 和 `lastIndexOf(...)` 查找“整个字符串与
正则匹配”的项，而不是返回每个字符串内部的匹配位置。

## 过滤：返回新列表

`filter()` 不修改原列表，它返回一个只包含匹配项的新 `QStringList`。

```cpp
QStringList files = {"main.cpp", "main.h", "readme.md"};
QStringList headers = files.filter(".h", Qt::CaseInsensitive);
```

常用重载：

- `filter(QStringView / QString / QLatin1StringView, cs)`：保留包含该子串的项。
- `filter(const QRegularExpression &)`：保留匹配正则的项。
- `filter(const QStringMatcher &)`：Qt 6.7 起，适合在很长列表上重复使用同一个匹配器。
- `filter(const QLatin1StringMatcher &)`：Qt 6.9 起，适合 Latin-1 needle 的重复匹配。

对大量数据反复过滤同一模式时，预先构造 `QStringMatcher` 或 `QLatin1StringMatcher` 可以避免
每次重新准备匹配器。对一次性小列表，普通子串重载更直观。

## 拼接与拆分的边界

`join()` 把所有元素按分隔符拼成一个 `QString`。空列表返回空字符串；分隔符不会出现在开头或
结尾。

```cpp
QStringList fonts = {"Arial", "Helvetica", "Times"};
QString csv = fonts.join(", ");
```

可传 `QString`、`QStringView`、`QLatin1StringView` 或单个 `QChar` 分隔符。`join()` 只是简单连接，
不会做 CSV 转义、引号处理或路径规范化。要生成真正 CSV、shell 参数或 URL 查询，必须使用相应
格式的转义规则。

拆分是 `QString` / `QStringView` 的职责：

```cpp
QStringList fields = line.split(',');
```

注意 `split()` 的空字段保留策略和大小写规则，不要假设所有拆分都会自动丢弃空项。

## 批量替换：原地修改每个字符串

`replaceInStrings()` 对列表中的每个 `QString` 调用替换操作，并返回 `*this`，方便链式调用：

```cpp
QStringList paths = {"$QTDIR/src/moc/moc.y", "$QTDIR/include/qconfig.h"};
paths.replaceInStrings("$QTDIR", "/usr/lib/qt");
```

字符串重载支持大小写敏感性。正则重载支持捕获组替换：

```cpp
QStringList people = {"Murray, Bill"};
people.replaceInStrings(QRegularExpression("^(.*), (.*)$"), "\\2 \\1");
```

一个容易踩的边界是空 `before`：它会在每个字符串的每个字符前后插入 `after`，通常会制造出远比
预期长的结果。用户输入作为搜索文本时，应先拒绝空模式或单独处理。

## 去重与排序

`removeDuplicates()` 原地移除重复项，保留第一次出现的顺序，返回被删除的数量。列表不需要预先
排序。

```cpp
QStringList tags = {"qt", "core", "qt"};
qsizetype removed = tags.removeDuplicates(); // removed == 1, tags == ["qt", "core"]
```

比较是否重复按 `QString` 的相等语义进行，大小写不同的字符串不是同一个值。若要大小写不敏感
去重，需要自己维护归一化 key，例如用小写字符串放进 `QSet`。

`sort(cs)` 原地升序排序，平均复杂度为 O(n log n)。`Qt::CaseInsensitive` 会改变比较规则，但不
提供 locale-aware 的自然排序，也不保证按数字大小排序 `"2"` 和 `"10"`。需要自定义顺序时，使用
`std::sort()` 配合自定义比较器，或把数据放进能表达排序 key 的结构中。

## 与模型、变体和 API 的关系

很多 Qt API 使用 `QStringList` 表达“若干字符串”：`QCoreApplication::arguments()`、插件 key、
文件筛选器、路径列表、进程参数等。`QVariant` 也有 `QStringList` 的原生类型。

如果要在视图中展示并允许编辑简单字符串列表，使用 `QStringListModel`。不要把一个已传给模型的
`QStringList` 当成“模型内部列表的引用”；模型保存自己的副本，之后修改原列表不会通知视图。

## 常见错误

### 把 `contains("abc")` 当成子串搜索

它检查是否存在等于 `"abc"` 的元素。子串筛选用 `filter("abc")` 或手写循环。

### 忽略隐式共享导致的分离成本

复制很便宜，但修改共享列表会线性复制。性能敏感代码中，避免在大列表的多个共享副本上交替修改。

### 持有迭代器后修改列表

插入、删除、排序、去重和分离都可能让迭代器失效。修改前重新取得迭代器。

### 用 `join()` 生成协议文本

`join()` 不转义分隔符。CSV、shell、URL 和 SQL 都有自己的编码规则。

### 对空 `replaceInStrings(before, after)` 没防护

空 `before` 会在每个字符周围插入 `after`，容易造成数据膨胀。

### 以为 `QStringList` 是 UI 模型

它只是值容器。视图需要通知和索引协议，应使用 `QStringListModel` 或其他 item model。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QStringList()` | 创建空字符串列表 | 继承 `QList<QString>` 的默认构造能力。 |
| `QStringList(const QString &str)` | 创建只含一个元素的列表 | 不会按分隔符拆分字符串。 |
| `QStringList(const QList<QString> &other)` | 从 `QList<QString>` 拷贝构造 | 隐式共享，初始拷贝通常为常量时间；修改时分离。 |
| `QStringList(QList<QString> &&other)` | 从 `QList<QString>` 移动构造 | 移动后源列表内容不再适合继续依赖。 |
| `operator=(const QList<QString> &)` | 从普通字符串列表赋值 | 结果与源相等；共享数据直到修改。 |
| `operator=(QList<QString> &&)` | 移动赋值 | 文档说明移动后源列表为空。 |
| `operator<<(const QString &)` | 追加一个字符串并返回自身 | 会修改列表，可能触发分离。 |
| `operator<<(const QStringList &)` | 追加另一个 `QStringList` | 保留追加顺序。 |
| `operator<<(const QList<QString> &)` | 追加普通 `QList<QString>` | 与逐个 `append()` 等价但更紧凑。 |
| `operator+(const QStringList &)` | 返回两个列表连接后的新列表 | 原列表不变；结果包含两边所有元素。 |
| `contains(QString / QStringView / QLatin1StringView, cs)` | 判断是否存在相等元素 | 整项匹配，不是子串搜索。 |
| `indexOf(QString / QStringView / QLatin1StringView, from, cs)` | 从前向后找相等元素 | 找不到返回 `-1`；`from` 是起始索引。 |
| `lastIndexOf(QString / QStringView / QLatin1StringView, from, cs)` | 从后向前找相等元素 | 默认 `from = -1` 表示从最后一项开始。 |
| `indexOf(const QRegularExpression &, from)` | 找第一个正则匹配项 | 返回列表索引，不返回字符串内部位置。 |
| `lastIndexOf(const QRegularExpression &, from)` | 找最后一个正则匹配项 | 找不到返回 `-1`。 |
| `filter(QString / QStringView / QLatin1StringView, cs)` | 返回包含子串的所有项 | 不修改原列表。 |
| `filter(const QRegularExpression &)` | 返回匹配正则的所有项 | 正则对象可预编译复用。 |
| `filter(const QStringMatcher &)` | 用预建匹配器过滤 | Qt 6.7 起；适合大列表重复搜索。 |
| `filter(const QLatin1StringMatcher &)` | 用 Latin-1 匹配器过滤 | Qt 6.9 起。 |
| `join(QString / QStringView / QLatin1StringView / QChar)` | 把列表拼成一个字符串 | 不做 CSV 或协议转义。 |
| `replaceInStrings(before, after, cs)` | 在每个元素内替换普通子串 | 原地修改；空 `before` 有特殊插入行为。 |
| `replaceInStrings(const QRegularExpression &, after)` | 对每个元素做正则替换 | `after` 可使用捕获组引用。 |
| `removeDuplicates()` | 原地去除重复元素 | 保留首次出现顺序，返回删除数量。 |
| `sort(cs)` | 原地升序排序 | 平均 O(n log n)，不是 locale-aware 自然排序。 |
| `QStringListIterator` | Java 风格只读迭代器别名 | 即 `QListIterator<QString>`。 |
| `QMutableStringListIterator` | Java 风格可变迭代器别名 | 即 `QMutableListIterator<QString>`；受 Java-style iterator 机制影响。 |

一句话总结：`QStringList` 是“字符串集合的日常手工具”，但它仍然是值容器；需要数据变更通知、
多列、多角色或自定义排序时，要上模型或结构化类型。
