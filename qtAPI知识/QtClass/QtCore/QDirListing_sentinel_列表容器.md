# Qt QDirListing::sentinel 说明

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.8  
> 所属模块：`Qt6::Core`  
> 头文件：不需要单独包含；通过 `#include <QDirListing>` 使用  
> 所属类型：`QDirListing::sentinel`  
> 定位：目录遍历的结束哨兵

## 1. 它解决什么问题

`QDirListing::sentinel` 不是一个用来保存目录信息的容器，也不是需要业务代码主动创建和管理的对象。它是 `QDirListing` 为 C++ range 遍历提供的“结束位置”类型。

`QDirListing::const_iterator` 是单向、单遍的输入迭代器。它不能像传统容器迭代器那样用同一个 iterator 类型表示“当前项”和“末尾”，所以 `QDirListing::end()` / `cend()` 返回一个 `sentinel`，用来判断目录项是否已经遍历完。

```text
QDirListing
  begin() / cbegin() -> const_iterator
  end()   / cend()   -> sentinel
```

这是一种 C++20 range 常见的 iterator/sentinel 组合：

- iterator 表示“当前正在读取的位置”；
- sentinel 只表示“已经到达范围末尾”；
- iterator 与 sentinel 可以比较；
- iterator 等于 sentinel 后不能再解引用。

日常代码通常不需要直接写出 `sentinel`。范围 `for` 会自动处理它：

```cpp
#include <QDirListing>

void scan(const QString &root)
{
    for (const auto &entry : QDirListing(root, QDirListing::IteratorFlag::FilesOnly))
        consume(entry.filePath());
}
```

## 2. 它与 `QDirListing` 的关系

`sentinel` 的意义只有放回 `QDirListing` 的遍历协议中才完整：

```cpp
QDirListing listing(root);
auto it = listing.begin();
auto last = listing.end();

for (; it != last; ++it) {
    const QDirListing::DirEntry &entry = *it;
    consume(entry);
}
```

上面的 `last` 不是一个“指向最后一项的 iterator”。它只是终止标记。目录的最后一个条目仍然要在 `it != last` 时处理；当 `it == last` 后，循环结束。

`sentinel` 不提供文件名、路径、大小或权限查询。所有条目信息都来自当前 iterator 解引用得到的 `QDirListing::DirEntry`。需要理解完整扫描行为时，应同时阅读：

- `QDirListing`：路径、名称过滤器、递归和符号链接策略；
- `QDirListing::const_iterator`：单遍迭代、移动语义和解引用规则；
- `QDirListing::DirEntry`：当前条目的路径、类型和元数据查询。

## 3. 最小可用代码

### 3.1 推荐：范围 `for`

```cpp
#include <QDirListing>

void listCppFiles(const QString &root)
{
    using Flag = QDirListing::IteratorFlag;
    const auto flags = Flag::FilesOnly | Flag::Recursive;

    for (const auto &entry : QDirListing(root, {"*.cpp", "*.h"}, flags))
        process(entry.filePath());
}
```

范围 `for` 会隐式使用 `begin()` 和 `end()`，因此不会把 `sentinel` 误当成目录条目。

### 3.2 需要手动控制迭代时

```cpp
void listManually(const QString &root)
{
    QDirListing listing(root);
    auto it = listing.begin();
    const auto last = listing.end();

    while (it != last) {
        const auto &entry = *it;
        inspect(entry);
        ++it;
    }
}
```

`last` 可以保存到循环中重复比较，但它不包含“最后一项”的信息，也不能被解引用。

## 4. 关键语义与边界

### 4.1 到达末尾后不能解引用

下面的代码是未定义行为：

```cpp
auto it = listing.begin();
auto last = listing.end();

while (it != last)
    ++it;

const auto &entry = *it; // 错误：it 已经等于 sentinel
```

`sentinel` 不代表一个空的 `DirEntry`。它没有文件路径，也不会返回“最后一个条目”。到达末尾后只能结束遍历，或者重新创建/重新开始一次 listing。

### 4.2 它不是普通容器的 `end()` iterator

传统 STL 算法通常要求 `first` 和 `last` 是同一种 iterator 类型。`QDirListing` 的结束值是 sentinel，因此下面这种经典写法不应作为通用方案：

```cpp
// 传统算法通常无法接受 iterator + sentinel 的异构组合。
std::for_each(listing.begin(), listing.end(), callback);
```

在 C++20 中使用支持 range/sentinel 的 `std::ranges` 算法：

```cpp
#include <algorithm>
#include <ranges>

std::ranges::for_each(listing, [](const auto &entry) {
    process(entry.filePath());
});
```

如果项目仍是 C++17，优先使用范围 `for`；不要为了迎合传统算法而把整个目录结果无条件收集到 `QList` 或 `std::vector`。收集结果会改变原本的流式、低内存特性，只有业务确实需要排序、随机访问或多次遍历时才这样做。

### 4.3 iterator 的单遍语义仍然适用

`sentinel` 只负责表示结束，并不会让 `QDirListing` 变成可复制、可回退的普通容器。仍需遵守：

- iterator 只能向前推进；
- 不能倒序或随机跳转；
- 当前 `DirEntry` 引用只适合在当前迭代步内消费；
- 同一个 listing 上重新调用 `begin()` 可能重置内部遍历状态；
- 目录扫描期间文件系统仍可能变化，结束标记不代表之前读到的路径永远有效。

## 5. 常见使用场景

### 5.1 只扫描并立即处理

这是 `sentinel` 最自然的使用方式：范围 `for` 自动比较结束标记，处理完当前条目后继续向前。

```cpp
using Flag = QDirListing::IteratorFlag;

for (const auto &entry :
     QDirListing(root, Flag::FilesOnly | Flag::Recursive)) {
    QFile file(entry.filePath());
    if (!file.open(QIODevice::ReadOnly))
        continue;
    index(file.readAll());
}
```

`sentinel` 只控制“什么时候停止枚举”；文件是否仍存在、是否可打开，必须由真正的 I/O 调用确认。

### 5.2 使用 C++20 ranges 做轻量算法

```cpp
auto listing = QDirListing(
    root,
    {"*.json"},
    QDirListing::IteratorFlag::FilesOnly);

const auto count = std::ranges::distance(listing);
```

这类算法必须符合 input range 的要求。`distance` 会消耗单遍范围，不能把它当成普通容器的常数时间 `size()`；统计完后不要再假设同一遍历状态仍可继续使用。

## 6. 与几个相似概念的区别

| 概念 | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `QDirListing::const_iterator` | 指向当前目录条目的单向输入迭代器 | move-only、单遍、不能随机访问 |
| `QDirListing::sentinel` | 表示遍历结束 | 不能解引用，不是最后一个条目 |
| `QDirListing::DirEntry` | 表示当前解引用得到的目录条目 | 不要保存迭代过程中的引用 |
| `QDir::entryInfoList()` 返回值 | 一次收集出的 `QFileInfo` 列表 | 可排序、可多次遍历，但会占用结果存储 |
| `QDirIterator::hasNext()` | 旧式迭代器的结束判断 | 与 `QDirListing` 的 range/sentinel 模型不同 |

## API 速查表
`QDirListing::sentinel` 类页没有独立的公共构造函数、属性或成员函数。它的可用 API 体现在产生它的 `QDirListing` 范围接口和 iterator 比较操作中。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 结束接口 | `QDirListing::end() const` | 返回表示目录遍历结束的 `QDirListing::sentinel` | 不要解引用与它相等的 iterator |
| 结束接口 | `QDirListing::cend() const` | 以 const 形式返回结束哨兵 | 仍然只是终止标记，不代表最后一个条目 |
| 比较 | `iterator != sentinel` | 判断当前 iterator 是否仍有条目可读 | 进入循环体前比较；比较为 false 后不能解引用 |
| 比较 | `iterator == sentinel` | 判断是否已到达遍历末尾 | 到达末尾后只能结束当前遍历 |
| 类型本身 | `QDirListing::sentinel` | 保存 range 的结束位置语义 | 不提供路径、文件信息或随机访问能力 |

## 8. 一句话总结

`QDirListing::sentinel` 是 `QDirListing` 的结束哨兵：它只负责告诉 iterator “目录已经遍历完”，不代表最后一个目录项，也不能被解引用；日常优先使用范围 `for`，需要算法时使用支持 iterator/sentinel 的 C++20 ranges。
