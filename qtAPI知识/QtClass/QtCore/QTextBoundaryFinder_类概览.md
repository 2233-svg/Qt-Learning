# Qt QTextBoundaryFinder Unicode 文本边界查找器

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextBoundaryFinder>`  
> 所属模块：`Qt6::Core`  
> 类型特征：值类型，可复制；Qt 6.11 起支持移动；所有成员函数可重入  
> 定位：按 Unicode 文本边界规则查找字素、单词、句子和换行机会

## 它解决什么问题

用户眼中的“一个字符”“一个词”“一句话”和程序里的 UTF-16 code unit 并不总是一一对应。比如一个看起来像单个字符的文本，可能由基础字符加组合符组成；一行文本可换行的位置也不能只靠空格判断；句子边界更不能简单地按英文句点切分。

`QTextBoundaryFinder` 按 Unicode 文本边界规则在字符串中移动，回答两个问题：

- 当前位置是不是合法边界？
- 下一个或上一个字素、单词、句子、换行边界在哪里？

它适合做文本编辑器光标移动、删除一个用户可见字符、双击选词、自动换行、简单句子边界扫描等底层文本处理。它不是正则表达式，不负责语言学分词，也不会返回子串集合；它只维护一个位置游标，并告诉你这个位置的边界原因。

## 实际使用场景

- 文本编辑器中按“用户可见字符”移动光标，避免把组合字符、变体序列拆坏。
- 删除、选择或高亮一个 grapheme cluster，而不是简单删除一个 `QChar`。
- 根据 Unicode line breaking rules 找到可换行点，配合排版宽度决定实际断行。
- 对 `QVariant`、模型数据或文档文本做单词/句子边界扫描。
- 实现“跳到下一个词”“扩展选区到句末”等文本交互。

如果你的目标是查找某个模式，用 `QRegularExpression`；如果目标是本地化分词或自然语言处理，通常需要更高层的词法工具。

## 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QTextBoundaryFinder>
```

qmake 工程使用：

```qmake
QT += core
```

## 最小可用示例

```cpp
#include <QTextBoundaryFinder>

QList<qsizetype> wordStarts(const QString &text)
{
    QList<qsizetype> positions;
    QTextBoundaryFinder finder(QTextBoundaryFinder::Word, text);

    for (qsizetype pos = finder.toNextBoundary();
         pos != -1;
         pos = finder.toNextBoundary()) {
        if (finder.boundaryReasons().testFlag(QTextBoundaryFinder::StartOfItem))
            positions.append(pos);
    }

    return positions;
}
```

位置值是 `QString` 的 UTF-16 索引，范围从 `0` 到 `string.length()`（含末尾位置）。它不是 Unicode code point 数量，也不是用户可见字符数量。

## 四种边界类型

`BoundaryType` 决定查找器按哪类规则解释文本：

| 类型 | 含义 | 常见用途 |
| --- | --- | --- |
| `Grapheme` | 查找最小用户可见字符单元，也就是 grapheme cluster | 光标移动、退格删除、选择单个可见字符 |
| `Word` | 查找 Unicode 规则下的词边界 | 双击选词、跳词、统计候选词区间 |
| `Sentence` | 查找句子边界 | 粗粒度句子扫描、句级选择 |
| `Line` | 查找可换行位置 | 自动换行、排版前的断行机会分析 |

字符串起点 `0` 总是有效边界，字符串末尾 `length()` 也总是有效边界。起点表示第一个字符之前，末尾表示最后一个字符之后。

## BoundaryReason 如何理解

`BoundaryReasons` 是 `QFlags<BoundaryReason>`，当前位置可能同时具备多个原因。

| 标志 | 值 | 含义 |
| --- | --- | --- |
| `NotAtBoundary` | `0` | 当前不是边界位置 |
| `BreakOpportunity` | `0x1f` | 当前是可断开的机会位置；它也可能同时是 item 开始/结束、强制换行或软连字符位置 |
| `StartOfItem` | `0x20` | 当前位于字素、单词、句子或行项目的开始 |
| `EndOfItem` | `0x40` | 当前位于字素、单词、句子或行项目的结束 |
| `MandatoryBreak` | `0x80` | 当前是强制换行位置；只会出现在 `Line` 类型中 |
| `SoftHyphen` | `0x100` | 当前是软连字符位置；只会出现在 `Line` 类型中 |

`isAtBoundary()` 只回答“是不是边界”。如果你要区分“词开始”还是“词结束”，要读取 `boundaryReasons()`。

## 字符串与缓冲区生命周期

构造方式决定 `QTextBoundaryFinder` 是否自己持有字符串数据：

- `QTextBoundaryFinder(type, const QString &string)` 以 `QString` 创建，适合普通使用。
- `QTextBoundaryFinder(type, QStringView string, buffer, bufferSize)` 不复制 `string`。
- `QTextBoundaryFinder(type, const QChar *chars, length, buffer, bufferSize)` 等价于用 `QStringView(chars, length)` 创建，也不复制字符数组。

使用 `QStringView` 或 `const QChar *` 构造时，调用方必须保证字符数据在查找器整个生命周期内有效。可选 `buffer` 也是非拥有的：如果 `bufferSize >= length + 1`，查找器会使用它作为工作缓冲；否则会自行分配内部缓冲。传入外部缓冲时，同样要保证它活得比查找器久。

```cpp
QTextBoundaryFinder bad(QTextBoundaryFinder::Word,
                        QString("temporary")); // 避免把临时对象转成非拥有视图
```

普通场景优先用 `QString` 重载，只有在你确实要避免复制并能管理生命周期时，再使用 `QStringView` 或裸指针重载。

## 游标模型

`QTextBoundaryFinder` 内部维护一个当前位置。常用移动方式如下：

- `toStart()` 把位置设到 `0`。
- `toEnd()` 把位置设到 `string.length()`。
- `setPosition(pos)` 把位置设到指定值，越界时会被限制到合法范围 `[0, length]`。
- `toNextBoundary()` 移到下一个边界并返回位置；没有下一个边界时返回 `-1`。
- `toPreviousBoundary()` 移到上一个边界并返回位置；没有上一个边界时返回 `-1`。
- `position()` 返回当前游标位置。

如果你需要检查当前位置是否已经在边界上，使用 `isAtBoundary()`；如果你要知道为什么是边界，使用 `boundaryReasons()`。

## 拷贝、移动与线程边界

该类是隐式共享相关的值类型，可复制和赋值。复制后的对象拥有自己的当前位置语义；修改一个对象的游标不会作为共享状态去移动另一个对象。

Qt 6.11 起支持移动构造、移动赋值和 `swap()`。被移动对象处于 partially-formed 状态，只能析构或重新赋值。

文档将所有成员函数标为可重入，表示不同线程可以操作各自独立的 `QTextBoundaryFinder` 对象。同一个对象跨线程并发访问仍需外部同步；如果对象引用外部 `QStringView` 或工作缓冲，也要保证那块数据本身没有并发失效问题。

## 常见误区

- 把 `position()` 当成“第几个字符”。它是 UTF-16 索引，不是 code point 索引，也不是 grapheme 序号。
- 用 `QStringView` 或 `QChar *` 构造后，原字符串或缓冲已经销毁，查找器仍继续使用。
- 只用空格、标点或正则替代 Unicode 边界规则，导致组合字符、软连字符、非拉丁文本处理错误。
- 只看 `isAtBoundary()`，却忽略 `boundaryReasons()`，无法区分 item 开始和结束。
- 在默认构造的无效对象上直接查找边界。默认构造对象是 invalid，应先赋予有效字符串。
- 认为 `Line` 类型会直接生成最终排版行。它只告诉你可能断行的位置；实际断行还要结合字体、宽度、排版策略。
- 移动对象后继续读取源对象。

## 逐项 API 说明

### `enum BoundaryType`

选择边界算法：`Grapheme` 查字素簇，`Word` 查词边界，`Sentence` 查句子边界，`Line` 查可换行位置。枚举值分别为 `0`、`1`、`2`、`3`，其中文档表格常按用途列出 `Line` 和 `Sentence`。

### `enum BoundaryReason` / `BoundaryReasons`

描述当前位置成为边界的原因。`BoundaryReasons` 是可组合标志。`MandatoryBreak` 和 `SoftHyphen` 只与 `Line` 类型相关。

### `QTextBoundaryFinder()`

构造无效对象。`isValid()` 返回 `false`，需要通过赋值或重新构造获得有效查找器。

### `QTextBoundaryFinder(BoundaryType type, const QString &string)`

创建在 `string` 上工作的查找器。普通用法首选该重载，生命周期最不容易出错。

### `QTextBoundaryFinder(BoundaryType type, QStringView string, unsigned char *buffer = nullptr, qsizetype bufferSize = 0)`（Qt 6.0）

创建非拥有字符串视图上的查找器。`string` 和可选 `buffer` 必须在查找器生命周期内保持有效；如果 `bufferSize >= length + 1`，查找器会使用外部缓冲。

### `QTextBoundaryFinder(BoundaryType type, const QChar *chars, qsizetype length, unsigned char *buffer = nullptr, qsizetype bufferSize = 0)`

裸字符数组重载，等价于 `QStringView(chars, length)`。同样不拥有 `chars`。

### `QTextBoundaryFinder(const QTextBoundaryFinder &other)`

复制查找器。复制对象可独立移动位置。

### `QTextBoundaryFinder(QTextBoundaryFinder &&other)`（Qt 6.11）

移动构造。源对象之后只能析构或重新赋值。

### `~QTextBoundaryFinder()`

释放查找器管理的内部状态。如果使用了调用方传入的字符串或外部缓冲，它不会替调用方释放那些数据。

### `bool isValid() const`

判断查找器是否有效。默认构造对象无效。

### `BoundaryType type() const`

返回当前查找器使用的边界类型。

### `QString string() const`

返回查找器操作的字符串内容。即使对象内部使用视图，该函数也返回一个 `QString` 值。

### `qsizetype position() const`

返回当前位置，范围是 `0` 到字符串长度（含末尾位置）。

### `void setPosition(qsizetype position)`

设置当前位置。越界值会被限制到合法范围，而不是保持非法索引。

### `void toStart()`

移动到字符串起点，等价于 `setPosition(0)`。

### `void toEnd()`

移动到字符串末尾，等价于 `setPosition(string.length())`。

### `qsizetype toNextBoundary()`

移动到下一个边界并返回该位置；不存在下一个边界时返回 `-1`。

### `qsizetype toPreviousBoundary()`

移动到上一个边界并返回该位置；不存在上一个边界时返回 `-1`。

### `bool isAtBoundary() const`

判断当前位置是否是当前 `BoundaryType` 下的有效文本边界。

### `BoundaryReasons boundaryReasons() const`

返回当前位置的边界原因标志。当前位置不是边界时通常得到 `NotAtBoundary`。

### `void swap(QTextBoundaryFinder &other)`（Qt 6.11）

快速交换两个查找器的状态，`noexcept`。

### `QTextBoundaryFinder &operator=(const QTextBoundaryFinder &other)`

复制赋值，把 `other` 的查找器状态赋给当前对象。

### `QTextBoundaryFinder &operator=(QTextBoundaryFinder &&other)`（Qt 6.11）

移动赋值。源对象进入只能析构或重新赋值的状态。

## API 速查表

| API | 作用 | 重点边界 |
| --- | --- | --- |
| `BoundaryType` | 选择字素、单词、句子或换行边界 | `position()` 仍是 UTF-16 索引 |
| `BoundaryReason` / `BoundaryReasons` | 描述当前位置为何是边界 | 是标志组合，`MandatoryBreak` / `SoftHyphen` 只适用于 `Line` |
| 默认构造 | 创建无效查找器 | 使用前检查或重新赋值 |
| `QTextBoundaryFinder(type, QString)` | 在字符串上创建查找器 | 普通场景首选 |
| `QTextBoundaryFinder(type, QStringView, buffer, size)` | 在非拥有视图上创建查找器 | 字符串和缓冲必须比查找器活得久 |
| `QTextBoundaryFinder(type, QChar *, length, buffer, size)` | 裸字符数组重载 | 不拥有 `chars` |
| 复制构造 / 复制赋值 | 复制查找器状态 | 复制后游标可独立移动 |
| 移动构造 / 移动赋值（Qt 6.11） | 转移查找器状态 | 源对象只能析构或重新赋值 |
| 析构 | 释放内部状态 | 不释放调用方拥有的外部字符串或缓冲 |
| `isValid()` | 查询对象是否有效 | 默认构造返回 `false` |
| `type()` | 返回边界类型 | 用于确认当前算法 |
| `string()` | 返回当前操作的字符串 | 返回 `QString` 值 |
| `position()` | 返回当前 UTF-16 位置 | 范围 `0..length` |
| `setPosition()` | 设置当前位置 | 越界会被夹到合法范围 |
| `toStart()` | 移到起点 | 等价于 `setPosition(0)` |
| `toEnd()` | 移到末尾 | 等价于 `setPosition(length)` |
| `toNextBoundary()` | 移到下一个边界 | 无下一个返回 `-1` |
| `toPreviousBoundary()` | 移到上一个边界 | 无上一个返回 `-1` |
| `isAtBoundary()` | 判断当前位置是否是边界 | 不说明边界原因 |
| `boundaryReasons()` | 返回边界原因标志 | 区分开始、结束、强制换行等 |
| `swap()`（Qt 6.11） | 交换两个对象状态 | 快速且 `noexcept` |

## 一句话总结

`QTextBoundaryFinder` 是面向 Unicode 文本边界的游标工具：它不分词、不排版，只按指定边界类型在 UTF-16 位置上移动；正确使用的关键是管好输入字符串生命周期，并用 `boundaryReasons()` 解读边界含义。
