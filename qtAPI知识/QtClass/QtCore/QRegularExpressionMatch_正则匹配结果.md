# Qt QRegularExpressionMatch：正则匹配结果

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QRegularExpressionMatch>`  
> 所属模块：`Qt6::Core`  
> 类型性质：隐式共享的正则匹配结果值类型  
> 关联类型：`QRegularExpression`、`QRegularExpressionMatchIterator`

## 1. 它解决什么问题

`QRegularExpressionMatch` 表示“一次正则匹配尝试的结果”。它不负责定义模式，也不负责继续搜索；它负责回答：

- 正则对象本身是否有效；
- 本次是否得到完整匹配；
- 是否得到部分匹配；
- 整体匹配和各个捕获组捕获了什么；
- 每个捕获组在主题字符串中的起止位置；
- 本次匹配使用了什么匹配类型和选项。

它通常来自两条路径：

```cpp
QRegularExpressionMatch one = re.match(subject);

QRegularExpressionMatchIterator it = re.globalMatch(subject);
QRegularExpressionMatch many = it.next();
```

要注意，`QRegularExpressionMatch` 不是一个“字符串结果”而是一个带状态的结果对象。只读取 `captured(1)` 而不先判断 `hasMatch()`，很容易把“没有匹配”误当成“捕获组为空”。

## 2. 构建与链接

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QRegularExpression>
#include <QRegularExpressionMatch>
```

类声明位于 `qregularexpression.h`；`<QRegularExpressionMatch>` 是 Qt 提供的类级包含入口。

## 3. 最小可用示例

```cpp
const QRegularExpression re(
    R"(^(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})$)");

const QRegularExpressionMatch match = re.match("2026-09-10");

if (!match.isValid()) {
    qWarning() << "regular expression is invalid";
    return;
}

if (!match.hasMatch()) {
    qWarning() << "input has the wrong format";
    return;
}

const QString year = match.captured("year");
const qsizetype monthStart = match.capturedStart("month");
```

格式校验通常应同时检查：

1. `QRegularExpression::isValid()` 或结果的 `isValid()`；
2. `hasMatch()`；
3. 必要时检查捕获组的 `hasCaptured()`。

`isValid()` 和 `hasMatch()` 不是同一个问题：正则有效但主题字符串不匹配时，结果可以有效而 `hasMatch()` 为 `false`。

## 4. 结果状态要分开理解

### 4.1 默认构造结果

默认构造的 `QRegularExpressionMatch` 是一个有效的空结果对象：

- 关联正则是默认构造的 `QRegularExpression`；
- `matchType()` 为 `QRegularExpression::NoMatch`；
- `matchOptions()` 为 `QRegularExpression::NoMatchOption`；
- `hasMatch()` 和 `hasPartialMatch()` 都为 `false`。

“对象有效”不代表“找到匹配”。真正判断完整匹配应使用 `hasMatch()`。

### 4.2 无效正则产生的结果

如果用语法错误的 `QRegularExpression` 调用 `match()` 或 `globalMatch()`，返回的结果或迭代器会处于无效状态，`isValid()` 为 `false`。模式来自配置、脚本或用户输入时，应在执行匹配前检查正则对象本身的 `isValid()` 和 `errorString()`。

### 4.3 正则有效但没有匹配

这是最常见的“正常失败”：

- `isValid()` 为 `true`；
- `hasMatch()` 为 `false`；
- `hasPartialMatch()` 通常也为 `false`；
- `lastCapturedIndex()` 为 `-1`；
- 捕获文本和位置查询不能被当作成功结果使用。

不要用 `isValid()` 代替 `hasMatch()`。

### 4.4 完整匹配

完整匹配时：

- `hasMatch()` 为 `true`；
- `hasPartialMatch()` 为 `false`；
- 捕获组 0 表示整个匹配；
- `capturedStart()`、`capturedLength()` 和 `capturedEnd()` 可以描述捕获区间。

### 4.5 部分匹配

只有调用匹配时明确使用 `PartialPreferCompleteMatch` 或 `PartialPreferFirstMatch`，才可能得到部分匹配。部分匹配时：

- `hasMatch()` 为 `false`；
- `hasPartialMatch()` 为 `true`；
- 如果完整匹配也能成立，Qt 会报告完整匹配，此时 `hasMatch()` 为 `true`、`hasPartialMatch()` 为 `false`；
- 部分匹配不应被当作协议或输入已经完成；
- 捕获组信息不能按完整匹配的规则使用，整体捕获组 0 可能表示已经消耗的部分文本。

流式输入中可以用它判断“是否可能还需要更多字符”，但仍应配合输入长度上限和协议状态机。

## 5. 捕获组的编号和参与状态

### 5.1 捕获组 0 是整个匹配

正则中的隐式捕获组 0 表示整个模式匹配到的文本：

```cpp
const QRegularExpression re(R"((\d{4})-(\d{2}))");
const QRegularExpressionMatch match = re.match("2026-09");

match.captured(0); // "2026-09"
match.captured(1); // "2026"
match.captured(2); // "09"
```

显式捕获组从 1 开始。命名捕获组与数字捕获组指向同一个捕获结果。

### 5.2 “未参与”与“捕获空字符串”不同

```cpp
const QRegularExpression re(R"(([a-z]+)|([A-Z]+))");
const QRegularExpressionMatch match = re.match("UPPER");

match.hasCaptured(0); // true
match.hasCaptured(1); // false
match.hasCaptured(2); // true
```

另一个组可能实际捕获了长度为 0 的字符串。这时：

- `hasCaptured(group)` 为 `true`；
- `capturedLength(group)` 为 `0`；
- `capturedStart(group)` 和 `capturedEnd(group)` 可以相等。

所以不能只用 `capturedLength() == 0` 判断捕获组不存在；应先用 `hasCaptured()` 区分。

### 5.3 `lastCapturedIndex()` 不是捕获组数量

它返回本次匹配中最后一个实际捕获到内容的组索引，包含组 0。它不是 `QRegularExpression::captureCount()`：

- 模式的捕获组总数由正则对象决定；
- 本次匹配中某些分支的捕获组可能未参与；
- `lastCapturedIndex()` 之前的组也可能没有捕获；
- 没有匹配时返回 `-1`。

如果需要遍历全部模式捕获组，使用正则对象的 `captureCount()`；如果只遍历本次可能有结果的索引，可以结合 `lastCapturedIndex()`，但仍需逐组检查 `hasCaptured()`。

## 6. 字符串副本与字符串视图

### 6.1 `captured()` 返回拥有数据的 `QString`

`captured()` 返回 `QString`。它适合：

- 保存到业务对象；
- 跨越匹配对象或主题字符串的生命周期使用；
- 需要修改、拼接或传给拥有型 API。

当组不存在或本次没有捕获时，返回空的 null `QString`，不要只把它当成“正常捕获了空字符串”。

### 6.2 `capturedView()` 返回非拥有的 `QStringView`

`capturedView()` 避免构造捕获文本副本，适合在短作用域内读取：

```cpp
const QString subject = loadLine();
const QRegularExpressionMatch match = re.match(subject);

if (match.hasMatch()) {
    const QStringView value = match.capturedView("value");
    consumeImmediately(value);
}
```

它是视图，不拥有字符数据。尤其当结果来自 `matchView()` 或 `globalMatchView()` 时，原始主题字符串的字符存储必须持续有效，直到所有 `QRegularExpressionMatch` 和 `capturedView()` 使用完毕。

不要把 `QStringView` 保存到成员变量，再让源 `QString` 销毁、被替换或发生可能使字符存储失效的修改。需要跨越生命周期时立即调用 `toString()` 或使用 `captured()`。

### 6.3 `QString` 重载与 Qt 6.8 的字符串参数边界

Qt 6.11.1 的公开现代重载使用 `QAnyStringView`：

```cpp
match.captured("name");
match.capturedView(u"name");
match.hasCaptured("name");
```

Qt 6.8 之前，命名 API 主要使用 `QString` 或 `QStringView`。在面向 Qt 6.8 及更高版本的代码中，笔记和新代码应优先按 `QAnyStringView` 理解；兼容旧版本时再根据最低版本选择重载。

## 7. 位置、长度和 Unicode 边界

```cpp
const qsizetype start = match.capturedStart(1);
const qsizetype length = match.capturedLength(1);
const qsizetype end = match.capturedEnd(1);
```

这些位置是主题字符串中的偏移，按 `QString` 的 UTF-16 code unit 计数，不是 Unicode code point 数，也不一定等于用户可见字符数。

当捕获组不存在或未参与时：

- `capturedStart()` 返回 `-1`；
- `capturedEnd()` 返回 `-1`；
- `capturedLength()` 返回 `0`。

当捕获了空字符串时，长度也为 `0`，但 `hasCaptured()` 为 `true`，且起止位置可能相等。因此处理区间时应先判断捕获是否存在。

如果要在原主题字符串上切片，优先使用位置和长度；如果要把结果保存到其他对象，使用 `captured()` 复制出来。

## 8. 典型使用场景

### 8.1 解析日志字段

```cpp
const QRegularExpression re(
    R"(^\[(?<time>[^\]]+)\]\s+(?<level>[A-Z]+)\s+(?<message>.*)$)");
const QRegularExpressionMatch match = re.match(line);

if (!match.hasMatch())
    return false;

LogEntry entry;
entry.time = match.captured("time");
entry.level = match.captured("level");
entry.message = match.captured("message");
return true;
```

日志对象需要脱离当前行的生命周期保存，因此这里使用 `captured()` 而不是 `capturedView()`。

### 8.2 高性能的即时扫描

```cpp
const QRegularExpressionMatch match = re.matchView(QStringView(line));
if (match.hasMatch()) {
    const QStringView key = match.capturedView(1);
    handleKey(key);
}
```

此处 `key` 只在 `line` 和 `match` 都有效的短作用域内使用。不要把它异步提交到一个晚于 `line` 生命周期的任务中。

### 8.3 判断可选分支

```cpp
const QRegularExpression re(R"((?<scheme>[a-z]+)://(?<host>[^/]+)(?<path>/.*)?)");
const QRegularExpressionMatch match = re.match(urlText);

if (match.hasMatch()) {
    const QString host = match.captured("host");
    if (match.hasCaptured("path")) {
        const QString path = match.captured("path");
        usePath(path);
    }
}
```

`hasCaptured("path")` 能区分“路径分支没有参与”和“路径分支参与但捕获为空”。

## 9. 与 `QRegularExpressionMatchIterator` 的关系

`QRegularExpression::match()` 返回一个单次结果；`globalMatch()` 返回迭代器。迭代器的每次 `next()` 都产生一个独立的 `QRegularExpressionMatch`：

```cpp
for (QRegularExpressionMatchIterator it = re.globalMatch(text);
     it.hasNext();) {
    const QRegularExpressionMatch match = it.next();
    if (match.hasMatch())
        consume(match.capturedView());
}
```

匹配结果是值类型，复制和移动通常便宜；但 `capturedView()` 的字符数据生命周期仍需由调用方管理，不能因为复制了 match 就把借用视图变成拥有字符串。

## 10. 常见错误

### 10.1 用 `isValid()` 判断是否匹配成功

`isValid()` 主要回答“正则是否有效并产生了有效结果对象”；完整匹配要看 `hasMatch()`。

### 10.2 用空字符串判断捕获组是否存在

可选组未参与和空字符串捕获都可能看起来像空文本。先调用 `hasCaptured()`。

### 10.3 忽略捕获组 0

组 0 是整个匹配，不是第一个显式括号。显式组 1 才是模式中的第一个捕获括号。

### 10.4 把 `capturedView()` 当作 `QString`

视图不拥有数据，也不适合作为跨线程或异步任务的长期参数。需要保存时转成 `QString`。

### 10.5 把位置当成 Unicode 字符数

`capturedStart()` 等位置按 UTF-16 code unit 计算。与用户可见字符位置、UTF-8 字节偏移互换前必须显式转换。

### 10.6 用部分匹配结果直接提交业务

部分匹配表示输入可能尚未结束，不表示格式已经通过。流式解析应继续等待数据并设置长度上限。

## 11. 逐项 API 语义

### `QRegularExpressionMatch()`

构造有效的空结果对象。它没有完整匹配，也没有部分匹配；关联正则为默认构造对象，匹配类型为 `NoMatch`。

### `QRegularExpressionMatch(const QRegularExpressionMatch &match)`

复制另一个结果对象。该类是隐式共享值类型，复制通常只增加共享数据引用，不应把复制理解为重新执行正则。

### `QRegularExpressionMatch(QRegularExpressionMatch &&match)`

移动结果对象。Qt 6.1 起提供。移动后的源对象只能析构或重新赋值；不要继续调用其他成员函数。

### `~QRegularExpressionMatch()`

销毁结果对象并释放其共享数据引用。它不会修改原始主题字符串，也不会重新执行匹配。

### `operator=(const QRegularExpressionMatch &match)`

复制赋值，把另一个结果的状态、模式和捕获结果赋给当前对象。

### `operator=(QRegularExpressionMatch &&match)`

移动赋值并接管另一个结果的内部数据。移动后的源对象只能析构或重新赋值。

### `swap(QRegularExpressionMatch &other)`

以常数级开销交换两个结果对象，适合实现值类型的交换或异常安全赋值。

### `regularExpression() const`

返回产生该结果的 `QRegularExpression` 值对象。返回的是正则对象副本/共享值，不是对外暴露的可修改引用。

### `matchType() const`

返回本次匹配使用的 `QRegularExpression::MatchType`，例如 `NormalMatch`、`PartialPreferCompleteMatch` 或 `PartialPreferFirstMatch`。它描述调用参数，不代表最终一定得到部分匹配。

### `matchOptions() const`

返回本次匹配使用的 `QRegularExpression::MatchOptions`。它可用于诊断结果为何从某个 offset 开始、是否使用了锚定选项等。

### `hasMatch() const`

返回是否有完整匹配。格式校验、业务解析和全局匹配结果通常首先检查它。

### `hasPartialMatch() const`

返回是否有部分匹配。只有显式请求部分匹配时才有意义；如果同时存在完整匹配，完整匹配优先报告为 `hasMatch() == true`。

### `isValid() const`

返回结果是否来自有效的 `QRegularExpression`。无效正则产生的结果为 `false`；它不等价于 `hasMatch()`。

### `lastCapturedIndex() const`

返回本次实际捕获到内容的最高捕获组索引，包含组 0；没有匹配时返回 `-1`。它不保证小于该索引的每个组都参与了匹配。

### `hasCaptured(int nth) const`

判断编号为 `nth` 的捕获组是否实际参与并捕获了字符串。组 0 表示整体匹配；不存在的组返回 `false`。空字符串捕获仍返回 `true`。Qt 6.3 起提供。

### `hasCaptured(QAnyStringView name) const`

按命名捕获组判断是否实际捕获。名称不存在或该分支未参与时返回 `false`；空字符串捕获仍返回 `true`。Qt 6.3 起提供，Qt 6.8 起现代公开参数类型为 `QAnyStringView`。

### `captured(int nth = 0) const`

返回编号捕获组的 `QString` 副本。默认组 0 是整个匹配；组不存在或未捕获时返回 null `QString`。

### `captured(QAnyStringView name) const`

返回命名捕获组的 `QString` 副本。名称不存在或未捕获时返回 null `QString`。

### `capturedView(int nth = 0) const`

返回编号捕获组的 `QStringView`。默认组 0 是整个匹配；没有捕获时返回 null view。视图不拥有字符数据，使用范围不能超出对应主题字符串和结果对象的安全生命周期。

### `capturedView(QAnyStringView name) const`

按名称返回捕获组的 `QStringView`。名称不存在或未捕获时返回 null view；Qt 6.8 起现代公开参数类型为 `QAnyStringView`。

### `capturedTexts() const`

返回所有捕获文本的 `QStringList`，顺序与捕获组编号一致，并包含组 0。它会创建字符串列表和文本副本，单个字段读取时不要为了方便而无条件调用它。

### `capturedStart(int nth = 0) const`

返回编号捕获组在主题字符串中的起始 UTF-16 偏移。组不存在或未捕获时返回 `-1`。

### `capturedStart(QAnyStringView name) const`

返回命名捕获组的起始 UTF-16 偏移。组不存在或未捕获时返回 `-1`。

### `capturedLength(int nth = 0) const`

返回编号捕获组的长度，单位是 UTF-16 code unit。组不存在或未捕获时返回 `0`；空字符串捕获也返回 `0`，需要结合 `hasCaptured()` 判断。

### `capturedLength(QAnyStringView name) const`

返回命名捕获组的 UTF-16 长度。组不存在或未捕获时返回 `0`；Qt 6.8 起现代公开参数类型为 `QAnyStringView`。

### `capturedEnd(int nth = 0) const`

返回编号捕获组结束位置之后的 UTF-16 偏移，通常等于 `capturedStart() + capturedLength()`。组不存在或未捕获时返回 `-1`。

### `capturedEnd(QAnyStringView name) const`

返回命名捕获组结束位置之后的 UTF-16 偏移。组不存在或未捕获时返回 `-1`。

### `operator<<(QDebug, const QRegularExpressionMatch &match)`

把结果对象写入 Qt 调试流，适合诊断模式、匹配状态和捕获结果。它是调试输出，不应作为稳定的序列化格式或业务协议。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QRegularExpressionMatch()` | 创建有效的空结果对象。 | 有效不等于找到匹配；`hasMatch()` 和 `hasPartialMatch()` 都为 `false`。 |
| 构造 | `QRegularExpressionMatch(const QRegularExpressionMatch &)` | 复制匹配结果。 | 隐式共享，复制不重新执行正则。 |
| 构造 | `QRegularExpressionMatch(QRegularExpressionMatch &&)` | 移动匹配结果。 | Qt 6.1 起；源对象移动后只能析构或赋值。 |
| 生命周期 | `~QRegularExpressionMatch()` | 销毁结果对象。 | 不会修改主题字符串。 |
| 赋值 | `operator=(const QRegularExpressionMatch &)` | 复制赋值。 | 覆盖当前结果状态。 |
| 赋值 | `operator=(QRegularExpressionMatch &&)` | 移动赋值。 | 源对象移动后不要再查询。 |
| 交换 | `swap()` | 交换两个结果对象。 | 快速且不重新匹配。 |
| 元数据 | `regularExpression()` | 返回产生结果的正则对象。 | 返回值类型，不是可修改引用。 |
| 元数据 | `matchType()` | 返回本次匹配类型。 | 描述调用参数，不代表一定有部分匹配。 |
| 元数据 | `matchOptions()` | 返回本次匹配选项。 | 可用于诊断 offset、锚定等行为。 |
| 状态 | `isValid()` | 判断结果是否来自有效正则。 | 不等于匹配成功。 |
| 状态 | `hasMatch()` | 判断是否完整匹配。 | 格式校验通常以它为主要成功条件。 |
| 状态 | `hasPartialMatch()` | 判断是否部分匹配。 | 仅部分匹配模式可能产生；不能直接提交业务。 |
| 捕获状态 | `lastCapturedIndex()` | 返回最后一个实际捕获组索引。 | 无匹配返回 `-1`；之前的组仍可能未参与。 |
| 捕获状态 | `hasCaptured(int)` | 判断编号组是否参与并捕获。 | 空字符串捕获返回 `true`；组 0 是整体匹配。 |
| 捕获状态 | `hasCaptured(QAnyStringView)` | 判断命名组是否参与并捕获。 | Qt 6.3 起；Qt 6.8 起公开现代参数为 `QAnyStringView`。 |
| 文本副本 | `captured(int)` | 返回编号组的 `QString`。 | 不存在或未捕获返回 null `QString`。 |
| 文本副本 | `captured(QAnyStringView)` | 返回命名组的 `QString`。 | 适合保存到长期对象。 |
| 文本视图 | `capturedView(int)` | 返回编号组的 `QStringView`。 | 不拥有数据；视图 API 的源字符串必须保持有效。 |
| 文本视图 | `capturedView(QAnyStringView)` | 返回命名组的 `QStringView`。 | 不存在或未捕获返回 null view。 |
| 批量文本 | `capturedTexts()` | 返回全部捕获文本列表。 | 包含组 0，并会产生列表和字符串副本。 |
| 位置 | `capturedStart(int)` | 返回编号组起始 UTF-16 偏移。 | 未捕获或不存在返回 `-1`。 |
| 位置 | `capturedStart(QAnyStringView)` | 返回命名组起始 UTF-16 偏移。 | 不要把偏移当 Unicode code point 或 UTF-8 字节偏移。 |
| 位置 | `capturedLength(int)` | 返回编号组 UTF-16 长度。 | 未捕获和空捕获都可能为 `0`，结合 `hasCaptured()`。 |
| 位置 | `capturedLength(QAnyStringView)` | 返回命名组 UTF-16 长度。 | Qt 6.8 起现代公开参数为 `QAnyStringView`。 |
| 位置 | `capturedEnd(int)` | 返回编号组结束后的 UTF-16 偏移。 | 未捕获或不存在返回 `-1`。 |
| 位置 | `capturedEnd(QAnyStringView)` | 返回命名组结束后的 UTF-16 偏移。 | 通常为 start + length。 |
| 调试 | `operator<<(QDebug, const QRegularExpressionMatch &)` | 输出调试信息。 | 不是稳定序列化格式。 |

## 13. 一句话总结

`QRegularExpressionMatch` 是一次正则匹配的结果快照：先用 `isValid()` 区分正则错误，再用 `hasMatch()` / `hasPartialMatch()` 判断结果类型；读取可选捕获组时用 `hasCaptured()`，需要长期保存用 `captured()`，短期零拷贝读取才用 `capturedView()`。
