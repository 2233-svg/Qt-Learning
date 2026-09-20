# Qt QRegularExpression 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QRegularExpression>`  
> 所属模块：`Qt6::Core`  
> 定位：使用 Perl 兼容正则语法匹配、提取和替换 Unicode 文本

## 1. QRegularExpression 解决什么问题

`QRegularExpression` 用一个可复用的模式描述“文本长什么样”，常用于：

- 校验输入格式，例如 UUID、版本号、日志行。
- 从文本中提取字段和命名捕获组。
- 全局查找多处匹配。
- 把 shell 通配符转换为正则。

它不是所有字符串操作的默认选项。固定前缀、后缀、分隔符或简单替换，优先使用 `startsWith()`、`endsWith()`、`indexOf()`、`split()`、`replace()` 等普通字符串 API；它们更清晰，也避免复杂模式导致性能问题。

## 2. 创建、验证和复用

```cpp
const QRegularExpression re(
    R"(^(?<name>[A-Za-z_]\w*)=(?<value>.+)$)");

if (!re.isValid()) {
    qWarning() << re.errorString()
               << "at" << re.patternErrorOffset();
    return;
}
```

常量或成员形式的正则应创建一次后复用。不要在循环中每次构造同一模式：

```cpp
for (const QString &line : lines) {
    const QRegularExpression re("..."); // 避免
    re.match(line);
}
```

`QRegularExpression` 是隐式共享值类型，复制通常便宜。首用优化由 Qt 管理，极少数性能关键路径可预先调用 `optimize()`，但先用 profiling 确认它确实是瓶颈。

## 3. 一次匹配和命名捕获

```cpp
const QRegularExpression re(
    R"(^(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})$)");

const QRegularExpressionMatch match = re.match("2026-09-09");
if (!match.hasMatch())
    return;

const int year = match.captured("year").toInt();
```

常用结果 API：

- `hasMatch()`：是否完整匹配。
- `hasPartialMatch()`：是否存在可能在更多输入后完成的部分匹配。
- `captured()`：返回捕获文本的拷贝。
- `capturedView()`：返回捕获文本视图，适合减少复制。
- `capturedStart()`、`capturedLength()`、`capturedEnd()`：返回在原文本中的位置。

命名捕获组比数字索引可读性更高，适合长期维护的解析器。捕获组可选时，先 `hasCaptured()`，不要把空字符串与“没有此捕获”混为一谈。

## 4. 全局匹配

```cpp
const QRegularExpression word(R"(\b\w+\b)");
QRegularExpressionMatchIterator it = word.globalMatch(text);

while (it.hasNext()) {
    const QRegularExpressionMatch match = it.next();
    consume(match.capturedView());
}
```

`globalMatch()` 返回迭代器，按顺序产生每个不重叠匹配。不要把迭代器和被匹配的临时 QStringView 生命周期混在一起；使用 `globalMatchView()` 时，原始字符数据必须在迭代和使用捕获视图期间保持有效。

## 5. 模式选项和匹配选项

```cpp
QRegularExpression emailPattern(
    R"(^[^\s@]+@[^\s@]+\.[^\s@]+$)",
    QRegularExpression::CaseInsensitiveOption);
```

常见模式选项：

| 选项 | 是做什么的 | 使用时重点注意 | 典型使用场景 |
| --- | --- | --- | --- |
| `CaseInsensitiveOption` | 忽略大小写匹配。 | Unicode 大小写规则比 ASCII 更复杂，协议规则需明确。 | 用户输入的名称或扩展名比较。 |
| `DotMatchesEverythingOption` | 让 `.` 也匹配换行。 | 容易让模式跨越多行并扩大匹配范围。 | 明确需要读取多行块时。 |
| `MultilineOption` | 让 `^`、`$` 以行为边界工作。 | 它不让 `.` 匹配换行，常与 DotMatchesEverything 分开理解。 | 逐行匹配日志和文本块。 |
| `ExtendedPatternSyntaxOption` | 启用空格和注释更友好的扩展语法。 | 模式里的普通空格将不再表示字面空格。 | 长而复杂、需要维护的模式。 |
| `InvertedGreedinessOption` | 翻转量词默认贪婪性。 | 读者很难从局部理解，通常直接写 `?` 更清晰。 | 遗留模式兼容，少用。 |
| `DontCaptureOption` | 将无命名分组默认视为不捕获。 | 需要的分组改用命名捕获或显式捕获。 | 只验证或大量非捕获分组的模式。 |
| `UseUnicodePropertiesOption` | 使用 Unicode 属性语义处理字符类别。 | 可能改变 `\w` 等类别的匹配范围。 | 国际化文本匹配。 |

## 6. Partial Match：输入还没收全时

```cpp
const QRegularExpression re(R"(GET\s+\S+\s+HTTP/1\.[01]\r\n)");
const QRegularExpressionMatch match = re.match(
    buffer,
    0,
    QRegularExpression::PartialPreferCompleteMatch);

if (match.hasPartialMatch()) {
    // 缓冲中可能只有半个请求行，继续等待数据。
}
```

部分匹配适合交互输入或流式协议的“还需要更多字符吗”判断。它不是网络协议解析的万能替代品：复杂协议仍应使用长度、状态机和显式上限，避免恶意输入触发高成本匹配。

## 7. 通配符与字面量转义

用户提供的普通文本不能直接拼进正则：

```cpp
const QString exact = QRegularExpression::escape(userText);
const QRegularExpression re("^" + exact + "$");
```

文件名通配符可以转换：

```cpp
const QRegularExpression re =
    QRegularExpression::fromWildcard(
        "*.json",
        Qt::CaseInsensitive);
```

不要把 shell wildcard 与正则混为一谈：`*`、`?`、`[]` 在两个语法中的语义和路径分隔处理都可能不同。

## 8. 性能和安全

某些嵌套量词和模糊模式会在失败输入上产生很高成本，例如：

```text
^(a+)+$
```

不要对不可信、超长输入运行未经审查的复杂正则。缓解方式：

- 先限制输入长度。
- 用锚点明确期望整体匹配还是子串匹配。
- 使用简单、确定的字符类和长度上限，例如 `[A-Za-z0-9_-]{1,32}`。
- 对协议解析优先状态机和长度字段。
- 对热点路径用基准测试，不凭感觉频繁调用 `optimize()`。

## 9. 常见误区

### 忘记 `^` 和 `$`

`match()` 默认在文本中寻找匹配，不代表整个字符串符合格式。校验完整格式时使用锚点或 `anchoredPattern()`。

### 正则拼接用户文本

用户输入中的 `.`、`*`、`[` 会改变模式。使用 `escape()`。

### 用 `captured()` 后反复切片

需要位置或零拷贝时用 `capturedView()` 和 capturedStart/Length。

### 把 `\d`、`\w` 的 Unicode 语义想当然

是否使用 Unicode 属性取决于选项和预期。安全标识符协议常应显式写 ASCII 范围。

### 将 `fromWildcard()` 用作路径安全校验

它只转换匹配模式，不验证路径规范化、符号链接或访问权限。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QRegularExpression()` | 创建空模式对象。 | 空模式合法但通常无业务意义；使用前设置 pattern。 |
| 构造 | `QRegularExpression(QString, PatternOptions)` | 创建模式并可设置匹配选项。 | 立刻检查 isValid；长期复用同一个已验证对象。 |
| 复制移动 | 拷贝、移动、赋值、`swap()` | 复制、移动或交换正则对象。 | 隐式共享使复制通常便宜；修改模式可能触发分离。 |
| 模式 | `pattern()` | 返回当前正则模式文本。 | 适合日志和诊断；不要依赖输出文本做安全判断。 |
| 模式 | `setPattern(QString)` | 替换正则模式。 | 修改后重新检查 isValid；频繁切换模式会影响可读性和性能。 |
| 模式选项 | `patternOptions()` | 查询当前模式选项。 | 选项会明显改变字符类和锚点语义。 |
| 模式选项 | `setPatternOptions(PatternOptions)` | 设置模式选项。 | 修改后重新验证并确认使用方期望大小写和多行行为。 |
| 验证 | `isValid()` | 判断模式语法是否有效。 | 模式来自配置或用户输入时必须检查。 |
| 验证 | `patternErrorOffset()` | 返回模式错误大致位置。 | 仅在无效模式时有诊断意义。 |
| 验证 | `errorString()` | 返回模式编译错误描述。 | 用于日志和 UI 提示，不要依赖文字分支。 |
| 捕获元数据 | `captureCount()` | 返回捕获组数量。 | 不含整个匹配的第 0 组；优先命名组提高可读性。 |
| 捕获元数据 | `namedCaptureGroups()` | 返回命名捕获组名称列表。 | 可用于调试或通用解析框架；匹配前不代表一定捕获。 |
| 单次匹配 | `match(QString, offset, MatchType, MatchOptions)` | 对 QString 进行一次匹配。 | 完整格式校验要写锚点；offset 是 UTF-16 code unit 位置。 |
| 单次匹配 | `matchView(QStringView, offset, MatchType, MatchOptions)` | 对 QStringView 进行一次匹配，减少复制。 | 原始字符数据必须在 match 与 capturedView 使用期间存活。 |
| 全局匹配 | `globalMatch(QString, offset, MatchType, MatchOptions)` | 返回 QString 上的所有不重叠匹配迭代器。 | 用 hasNext/next 迭代，不要假设空匹配会自动符合业务预期。 |
| 全局匹配 | `globalMatchView(QStringView, offset, MatchType, MatchOptions)` | 返回 QStringView 上的全局匹配迭代器。 | 严格管理源视图生命周期，避免捕获视图悬空。 |
| 优化 | `optimize()` | 提前优化已设置的模式。 | 很少需要手工调用；先通过 profiling 确认性能瓶颈。 |
| 辅助 | `escape(QStringView)` | 将普通文本转义成正则字面量。 | 拼接用户输入、文件名或固定文本时使用，防止意外元字符。 |
| 辅助 | `anchoredPattern(QStringView)` | 为模式包裹完整字符串锚点。 | 适合格式校验；确认模式本身没有不兼容的锚点语义。 |
| 辅助 | `wildcardToRegularExpression(QStringView, options)` | 把通配符文本转换成正则文本。 | 通配符不是正则；路径和非路径 wildcard 选项不同。 |
| 辅助 | `fromWildcard(QStringView, CaseSensitivity, options)` | 从通配符直接创建正则对象。 | 适合文件名筛选；不能替代文件路径安全校验。 |
| 枚举 | `PatternOption` / `PatternOptions` | 控制模式编译行为，例如大小写、多行和 Unicode 属性。 | 只启用真正需要的选项，避免模式语义过于隐蔽。 |
| 枚举 | `MatchType` | 选择普通匹配或偏好部分匹配。 | Partial 模式适合增量输入，不等于完整协议校验。 |
| 枚举 | `MatchOption` / `MatchOptions` | 控制单次匹配的锚定和检查策略。 | `DontCheckSubjectStringMatchOption` 是低层性能选项，普通代码不要用。 |
| 枚举 | `WildcardConversionOption` / `WildcardConversionOptions` | 控制 wildcard 到正则的转换方式。 | 选择是否路径敏感、是否强制整体匹配。 |
| 流 | `operator<<(QDataStream &, QRegularExpression)` | 将正则对象写入 QDataStream。 | 用于 Qt 内部数据传递；不是安全的用户输入格式验证。 |
| 流 | `operator>>(QDataStream &, QRegularExpression &)` | 从 QDataStream 读取正则对象。 | 读取后必须 isValid，尤其是外部或旧版本数据。 |
| 哈希 | `qHash(QRegularExpression)` | 为正则对象提供哈希。 | 可用作 QHash key；模式和选项共同决定相等性。 |

---

### 一句话总结

`QRegularExpression` 是强大的文本模式工具，但不该替代简单字符串操作或协议状态机。复用已验证模式，完整校验时加锚点，拼接外部文本时转义，处理不可信输入时限制长度和模式复杂度，才能既正确又可控。
