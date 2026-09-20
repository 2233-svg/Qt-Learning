# QByteArrayMatcher 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QByteArrayMatcher>`  
> 所属模块：`Qt6::Core`  
> 类型性质：可复用的字节模式查找器，不继承 `QObject`。

## 1. 它解决什么问题

`QByteArrayMatcher` 用于在一段或多段字节数据中反复查找同一个模式。它在设置 pattern 时预处理匹配信息，后续用 `indexIn()` 搜索时可避免每次都从零准备查找算法。

```cpp
QByteArrayMatcher boundary("\r\n\r\n");

for (const QByteArray &chunk : incomingChunks) {
    const qsizetype pos = boundary.indexIn(chunk);
    if (pos >= 0) {
        handleHeaderEnd(pos);
    }
}
```

适用场景：

- 在许多网络包或文件块中反复找同一个二进制边界。
- 协议解析中找固定分隔符，例如 `"\r\n\r\n"`、MIME boundary、帧同步字。
- 对同一大缓冲区从不同起点重复搜索同一模式。
- 性能敏感循环中，模式固定而输入不断变化。

不适合的场景：

- 只查找一次。直接用 `QByteArray::indexOf()` 更短、更自然，`QByteArrayMatcher` 的预处理没有机会回本。
- 需要正则、大小写折叠、Unicode 规则或模糊匹配。应考虑 `QRegularExpression`、`QStringMatcher` 或专用解析器。
- 模式本身每次搜索都不同。反复新建 matcher 通常没有明显收益。

## 2. 和 QByteArray::indexOf() 如何选择

一次性搜索：

```cpp
const qsizetype pos = data.indexOf("\r\n");
```

重复搜索固定模式：

```cpp
QByteArrayMatcher lineEnd("\r\n");

for (const QByteArray &data : manyBuffers) {
    const qsizetype pos = lineEnd.indexIn(data);
    // ...
}
```

`QByteArrayMatcher` 的优势来自“模式固定、多次匹配”。它在内部维护针对模式的跳过表，减少重复查找的准备成本。不要把它理解为对每一次 `indexOf()` 都绝对更快的替代品。

## 3. 构建与最小用法

CMake：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

qmake：

```qmake
QT += core
```

```cpp
#include <QByteArrayMatcher>

QByteArrayMatcher matcher("END");
const QByteArray message = "BEGIN-END";

if (const qsizetype index = matcher.indexIn(message); index != -1) {
    // index == 6
}
```

`indexIn()` 返回第一次匹配开始处的 byte 索引；未找到时返回 `-1`。返回值是 `qsizetype`，不要把它强行存进可能过窄的 `int`。

## 4. 三种模式构造方式，所有权完全不同

### 4.1 从 QByteArray 构造：最稳妥

```cpp
QByteArray pattern = "\r\n\r\n";
QByteArrayMatcher matcher(pattern);
```

这个重载把 `QByteArray` 作为对象状态保存。由于 `QByteArray` 是隐式共享类型，通常不需要立刻深拷贝；而 matcher 自己仍持有一份有效的 `QByteArray` 值。

因此原始 `pattern` 离开作用域、被销毁或之后发生写时复制，并不会让 matcher 悬空：

```cpp
QByteArrayMatcher makeMatcher()
{
    QByteArray local = "marker";
    return QByteArrayMatcher(local);   // 返回后仍可安全使用
}
```

业务代码优先选这个构造函数，除非你明确需要避免任何模式字节拷贝或共享句柄。

### 4.2 从 const char * 构造：matcher 借用外部内存

```cpp
const char marker[] = { char(0xAA), char(0x55) };
QByteArrayMatcher matcher(marker, 2);
```

此重载不拥有 `pattern` 指向的数据。官方明确要求：在 matcher 的整个使用期内，原始字节必须有效。

```cpp
QByteArrayMatcher badMatcher()
{
    QByteArray local = "END";
    return QByteArrayMatcher(local.constData(), local.size());
    // 返回后 local 销毁，matcher 引用悬空内存
}
```

`length = -1` 表示把输入当作以零结尾的 C 字符串并计算长度；它不能用于包含嵌入零字节的模式。二进制模式应明确传长度。

### 4.3 从 QByteArrayView 构造：同样是借用

```cpp
QByteArrayView view = "\r\n\r\n";
QByteArrayMatcher matcher(view);
```

`QByteArrayView` 本身不拥有内存，matcher 也不会替它复制模式字节。因此 view 所引用的字节同样必须在 matcher 生命周期内保持有效且不被改变。

从 Qt 6.3 起，这个重载可用。它适合静态字面量、长期驻留的只读内存，或调用方已明确管理模式缓冲区生命周期的场景。

## 5. 为什么模式字节不能被原地修改

matcher 为模式建立了预处理表。如果以 `const char *` 或 `QByteArrayView` 方式借用内存后，外部代码原地改写模式字节，matcher 的“模式内容”和预处理信息可能不再一致。

因此借用式模式不仅要活得足够久，还应在 matcher 使用期间保持不变。

```cpp
QByteArray pattern = "END";
QByteArrayMatcher matcher(pattern.constData(), pattern.size());

pattern[0] = 'X';     // 不要这样做：matcher 借用的模式数据发生了变化
```

如果模式要变，使用拥有式的 `setPattern()`：

```cpp
matcher.setPattern("NEXT");
```

## 6. indexIn()：数据搜索与起始位置

从字节指针搜索：

```cpp
const char *raw = readOnlyBuffer;
const qsizetype length = readOnlySize;
const qsizetype pos = matcher.indexIn(raw, length, 0);
```

从 Qt 6.3 起，推荐更安全的 `QByteArrayView` 重载：

```cpp
const QByteArrayView data(raw, length);
const qsizetype pos = matcher.indexIn(data, offset);
```

`from` 是开始搜索的 byte 索引。查找重复出现的分隔符时，下一次通常从上次位置加上模式长度开始：

```cpp
QByteArrayMatcher separator("::");
qsizetype from = 0;

while (true) {
    const qsizetype pos = separator.indexIn(data, from);
    if (pos < 0)
        break;

    consumeField(data.sliced(from, pos - from));
    from = pos + separator.pattern().size();
}
```

上面为了教学直接调用 `pattern()` 获取长度。性能热点里应在循环外保存长度，避免重复构造返回值：

```cpp
const QByteArray pattern = "::";
QByteArrayMatcher separator(pattern);
const qsizetype patternLength = pattern.size();
```

`indexIn()` 不修改输入数据，也不保存输入数据指针；输入缓冲只需在本次同步调用期间有效。

## 7. 默认构造与设置新模式

```cpp
QByteArrayMatcher matcher;
```

默认构造得到空 matcher，它不会匹配任何内容。需要后续设置模式：

```cpp
matcher.setPattern("Content-Length:");
```

`setPattern()` 会替换 matcher 的模式并重新准备后续搜索。模式会频繁变化时，应重新评估是否还值得使用 matcher；普通 `indexOf()` 可能更简单。

`pattern()` 返回当前模式的 `QByteArray` 值。对于借用外部内存构造的 matcher，这个返回值尤其有用：它让调用方获得自己的 `QByteArray` 副本，而不是暴露 matcher 内部的借用指针。

## 8. 复制、赋值和生命周期

`QByteArrayMatcher` 是普通 C++ 值对象，可复制、赋值和保存为成员：

```cpp
QByteArrayMatcher a("TOKEN");
QByteArrayMatcher b = a;
b.setPattern("OTHER");
```

复制会保留对应模式与匹配状态。若原 matcher 通过指针或 view 借用模式，复制出来的 matcher同样依赖那片外部内存；复制不把悬空风险变成所有权。

它没有事件循环、线程归属和父对象概念。不同线程使用不同 matcher 实例是自然的；若多个线程共享同一个 matcher，至少应保证不会与 `setPattern()`、赋值或析构并发发生。

## 9. 更偏底层的静态模式优化

Qt 头文件还提供 `QStaticByteArrayMatcher` 和 `qMakeStaticByteArrayMatcher()`，用于编译期已知的字符串字面量模式：

```cpp
static constexpr auto matcher =
    qMakeStaticByteArrayMatcher("\r\n\r\n");
```

它不是 `QByteArrayMatcher` 的替代 API 表面，而是适用于内部高频固定字面量的更底层工具。普通应用代码先使用 `QByteArrayMatcher`，只有性能分析确认这部分是热点时再考虑静态 matcher。

## 10. 常见错误

### 10.1 为一次搜索创建 matcher

只查一次时直接用 `data.indexOf(pattern)`。matcher 的预处理成本要靠重复搜索才有价值。

### 10.2 用局部 QByteArray 的 constData() 构造

`const char *` 和 `QByteArrayView` 重载都是借用。局部 buffer 离开作用域后 matcher 会指向无效内存。

### 10.3 忘记二进制模式的显式长度

`length = -1` 的 C 字符串模式会在第一个零字节处结束。查找任意二进制序列时必须传真实长度，或改用拥有式 `QByteArray`。

### 10.4 把返回 -1 存成无符号数

`indexIn()` 未找到返回 `-1`。不要转换为 `size_t` 后再判断，否则会变成很大的正数。

### 10.5 修改借用的 pattern 内存

模式一旦被 matcher 预处理，就应保持不变。要切换模式请调用 `setPattern()`。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QByteArrayMatcher()` | 构造空 matcher。 | 它不会匹配任何内容，需随后调用 `setPattern()`。 |
| 构造 | `explicit QByteArrayMatcher(const QByteArray &pattern)` | 从 `QByteArray` 保存一个模式。 | 推荐默认选择；matcher 持有 `QByteArray` 值，不依赖调用方对象生命周期。 |
| 构造 | `explicit QByteArrayMatcher(const char *pattern, qsizetype length = -1)` | 从原始指针和长度借用模式字节。 | 不拥有数据；整个 matcher 生命周期内指针必须有效且内容不变；二进制模式传明确长度。 |
| 构造 | `explicit QByteArrayMatcher(QByteArrayView pattern)` | 从非拥有 `QByteArrayView` 借用模式字节。 | Qt 6.3 起提供；view 的底层数据必须持续有效且不可变。 |
| 构造 | `QByteArrayMatcher(const QByteArrayMatcher &other)` | 拷贝另一个 matcher。 | 若 other 借用外部模式，副本也继承该生命周期约束。 |
| 析构 | `~QByteArrayMatcher() noexcept` | 销毁 matcher。 | 不拥有指针和 view 模式指向的外部字节。 |
| 赋值 | `QByteArrayMatcher &operator=(const QByteArrayMatcher &other)` | 用另一个 matcher 替换当前模式和预处理状态。 | 赋值后旧模式失效；借用式模式的生命周期约束仍保留。 |
| 搜索 | `qsizetype indexIn(const char *str, qsizetype len, qsizetype from = 0) const` | 在原始字节缓冲中查找模式首次出现的位置。 | 输入缓冲本次调用期间必须有效；没找到返回 `-1`。 |
| 搜索 | `qsizetype indexIn(QByteArrayView data, qsizetype from = 0) const` | 在字节视图中查找模式首次出现的位置。 | Qt 6.3 起提供；优先用于有长度的字节范围，没找到返回 `-1`。 |
| 模式 | `QByteArray pattern() const` | 返回当前搜索模式。 | 返回值是 `QByteArray`；高频循环中缓存其长度，避免反复调用。 |
| 模式 | `void setPattern(const QByteArray &pattern)` | 替换模式并重建匹配准备信息。 | 频繁改模式会削弱 matcher 的复用价值。 |

## 12. 一句话总结

`QByteArrayMatcher` 用预处理模式换取重复字节搜索的效率；一次性搜索用 `indexOf()`，反复搜索用 matcher，并始终分清拥有式 `QByteArray` 模式与借用式指针或 view 模式的生命周期。
