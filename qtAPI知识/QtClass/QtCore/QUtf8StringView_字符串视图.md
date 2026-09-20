# Qt QUtf8StringView：零拷贝借用 UTF-8 字节，而不是拥有字符串

`QUtf8StringView` 是一个只读、非拥有的 UTF-8 连续内存视图。它只保存指针和长度，不分配、不复制，也不为数据补 `'\0'`。它的主要价值是让函数用一个参数接受 `QByteArray`、`std::string`、`std::u8string`、UTF-8 字面量及其他兼容的字节容器，而不必为每一种来源写重载或先构造 `QString`。

```cpp
#include <QUtf8StringView>

void writeLabel(QUtf8StringView label)
{
    if (!label.isValidUtf8())
        return;

    consumeUtf8(label.data(), label.size());
}
```

> 适用版本：Qt 6.11.1，类自 Qt 6.0 起提供  
> 头文件：`#include <QUtf8StringView>`  
> CMake：`Qt6::Core`  
> 线程：成员函数可重入；它不解决底层缓冲区的并发写入、重分配或生命周期问题。

## 它解决什么问题

接口若只接受 `const QByteArray &`，调用方往往需要为了兼容而复制 `std::string` 或 `u8"..."`。若只接受 `const char *`，则丢失长度，遇到嵌入 NUL 又需要另加参数。`QUtf8StringView` 将“指针 + 显式长度”的只读借用统一起来：

```cpp
void parseHeader(QUtf8StringView value); // Preferred: pass by value.
```

它适合解析协议字段、日志文本、配置内容、格式化模板和跨 Qt/STL 边界的 UTF-8 输入。若函数真正接受多种**编码**，而非只接受 UTF-8，应考虑 `QAnyStringView`；若函数需要保存、修改或保证终止符，应拥有一份 `QString`、`QByteArray` 或 `std::string`。

`const QUtf8StringView &` 也能工作，却比直接按值传递多一次间接访问，违背这个小型视图类型的设计目的。

## 第一原则：视图不拥有任何字节

下面的代码悬垂：

```cpp
QUtf8StringView makeView()
{
    std::string temporary = "report";
    return QUtf8StringView(temporary); // Wrong: temporary dies on return.
}
```

正确做法是让 owner 活得更久，或在需要跨边界保存时复制：

```cpp
QString copyForLater(QUtf8StringView view)
{
    return view.toString(); // Deep copy.
}
```

任何会改变 owner 的内存地址或销毁 owner 的操作都会使既有 view 失效：局部 `std::string` / `QByteArray` 离开作用域、容器重新分配、`QByteArray::detach()`、把数据搬到其他缓冲区等。视图的副本仍只指向原内存，并不会延长生命周期。

因此它很适合“调用期间借用”的参数，不适合未经约束地作为成员缓存、异步任务捕获值或函数返回值。函数可以返回 `QUtf8StringView`，但必须明确引用的数据由谁持有、会存活到何时。

## UTF-8 视图不等于已验证 UTF-8

构造 `QUtf8StringView` 不会扫描或拒绝非法字节。兼容的字符类型只是 `char`、`signed char`、`unsigned char`，以及 C++20 下的 `char8_t`；它们表示“按 UTF-8 解释的字节源”，不保证内容真的符合 UTF-8。

```cpp
QByteArray bytes = readUntrustedPayload();
QUtf8StringView view(bytes);

if (!view.isValidUtf8()) {
    rejectPayload();
    return;
}
```

`isValidUtf8()` 自 Qt 6.3 起提供。网络协议、持久化格式或安全敏感文本在按 Unicode 语义处理前应验证；仅做原始字节比较时可不验证。`toString()` 会创建 `QString` 深拷贝，但不应把它当作“验证且无损修复”接口。

## 长度和位置按 UTF-8 存储单元，而非用户看到的字符

Qt 文档将这些元素称作 UTF-8 code points，并明确说明一个多字节序列会计为 2、3 或 4 个元素。就内存和 API 行为而言，应把 `size()`、索引和切片长度理解为 **UTF-8 code units / bytes**：

```text
"A中" in UTF-8: 41 E4 B8 AD
size() == 4
```

`operator[]`、`at()`、迭代器、`first()`、`last()`、`sliced()`、`slice()`、`chop()` 与 `truncate()` 都按这个单位工作，可能切到一个多字节序列中间。类不会自动阻止这种切割：

```cpp
QUtf8StringView text = u8"A中";
QUtf8StringView broken = text.first(2); // 41 E4, not valid UTF-8.
Q_ASSERT(!broken.isValidUtf8());
```

需要按 Unicode 标量、grapheme cluster 或用户可见字符截断时，应先转换到合适的文本处理层并使用相应的 Unicode API；不要将 UTF-8 byte offset 当作 UI 字符位置。

所有范围 API 都要求参数在 `[0, size()]` 内，`pos + n <= size()`；`front()`、`back()` 还要求非空。违反这些前置条件是未定义行为，不应依赖 debug `Q_ASSERT` 来兜底。

## 构造方式与终止符边界

### 指针构造会扫描 `'\0'`

`QUtf8StringView(const Char *str)` 通过查找第一个零字节确定长度，适合 NUL 终止的字面量和 C 字符串：

```cpp
QUtf8StringView hello("hello");
```

对 `nullptr` 安全，结果为 null view；但指针必须保持有效。此构造不能表示嵌入 NUL 之后的数据，也不适合长度未知或不保证终止的缓冲区。

### 指针加长度或首尾指针适合协议缓冲区

```cpp
QUtf8StringView field(data, length);
QUtf8StringView range(first, last);
```

长度不能为负；`data == nullptr` 时长度必须是 0。首尾指针必须来自同一有效范围，且 `last` 不能在 `first` 之前。它们不会检查 UTF-8，也不会读取终止符，适合有嵌入 NUL 的原始字段。

### 容器、数组与 `fromArray()`

兼容容器需要提供连续 `std::data()`、`std::size()` 与兼容元素类型；常见例子包括 `QByteArray`、`std::string` 和 `std::u8string`。容器构造按其 `size()` 取长度，不需要终止符。

数组构造通常忽略末尾 C 字符串终止符；`fromArray()` 则明确把整个数组大小都纳入 view，适合想保留数组中的 NUL 时使用。两者都不拥有数组。

## null、empty 与 `data()`

null 与 empty 不同：

| 状态 | `data()` | `size()` | 常见来源 |
| --- | --- | --- | --- |
| null | `nullptr` | `0` | 默认构造、`nullptr`、`(nullptr, 0)` |
| empty but non-null | 有效地址 | `0` | 某些空容器或 `(ptr, 0)` |

`isNull()` 只检查 `data() == nullptr`；`empty()` 与 `isEmpty()` 只检查 `size() == 0`。`toString()` 只有在 view 为 null 时才返回 null `QString`，这在需要保留 null/empty 区别时有意义。

`data()`、`begin()` 和 C++20 的 `utf8()` 都不是 C 字符串接口：指向的范围**不保证 NUL 终止**，必须连同 `size()` 使用。把 `data()` 直接传给 `strlen`、`printf("%s")` 或只接受 NUL 终止输入的旧 API 是越界读取风险。

## C++17、C++20 与 STL 互操作

Qt 6 为了兼容不同 C++ 标准提供两个 inline namespace 版本：

- 常规 `QUtf8StringView` 是 `q_no_char8_t::QUtf8StringView`，其存储元素是 `char`，所有 C++ 标准均可用；
- C++20 下可显式使用 `q_has_char8_t::QUtf8StringView`，其元素类型是 `char8_t`；
- 不要在业务代码中直接使用内部模板名 `QBasicUtf8StringView`。

`utf8()` 只在 C++20 下提供 `const char8_t *`，且仍不终止。自 Qt 6.7 起可隐式转为 `std::string_view`；自 Qt 6.10 起，在 C++20 下可转为 `std::u8string_view`。两种转换都是零拷贝，返回 view 与原对象共享相同指针和长度，生命周期风险完全相同。

```cpp
std::string_view bytes = view; // Qt 6.7+, no copy
```

## 常用 API 分组

### 观察与转换

`size()` / `length()`、`empty()` / `isEmpty()`、`isNull()`、`data()` 和 `isValidUtf8()` 不分配内存。`toString()` 是明确的深拷贝。`arg()` 自 Qt 6.9 起提供，按 `QString::arg()` 的格式化语义产出新的 `QString`，并不改变 view。

### 零拷贝子视图

`first()`、`last()`、`sliced()`、`chopped()`、头文件中的 `left()`、`right()`、`mid()` 都返回新的 view，不复制底层数据。`slice()`、`truncate()` 和 `chop()` 改的是当前 view 的起始位置/长度，也不修改底层字符串。

选择 `sliced()` 与 `slice()` 时注意所有 view 副本相互独立：修改一个 view 的窗口，不会改变另一个 view，也不会改变 owner。

### 访问、迭代和比较

`operator[]`、`at()`、`front()`、`back()` 返回一个 UTF-8 storage unit。`begin()` / `end()` 及反向迭代器也是原始单元迭代器。`compare()` 支持 `QUtf8StringView`、`QStringView`、`QLatin1StringView`，并可选大小写敏感；头文件还提供与 `QChar`、`QByteArray` 的比较/相等辅助和强比较运算符。比较并不替代 UTF-8 有效性校验。

## 常见错误

- 将临时 `std::string`、`QByteArray` 或函数内部拼接结果转换为 view 后保存。
- 把 `data()` 当 NUL 终止 C 字符串使用。
- 认为 `size()` 是 Unicode 字符数，或把 `first(n)` 用于用户可见文本截断。
- 在未验证外部字节时调用依赖合法 UTF-8 的文本逻辑。
- 空 view 上调用 `front()` / `back()`，或给切片 API 传越界/负数参数。
- 在底层容器 append、reserve、detach 或析构后继续使用旧 view。
- 因为 `std::string_view` 转换可用，就误以为它拥有数据。
- 在 C++20 中假定普通 `QUtf8StringView::value_type` 必定是 `char8_t`；需要该版本时显式使用 `q_has_char8_t::QUtf8StringView`。

## 逐项 API 说明

### 视图创建与状态

所有构造函数都只借用数据；指针构造扫描终止符，范围/长度构造不扫描。默认构造与 `nullptr` 构造产生 null view。`isEmpty()` 与 `isNull()` 必须分开理解，`isValidUtf8()` 只检查当前范围内的编码有效性。

### 子范围与访问

`first` / `last` / `sliced` / `chopped` 返回新视图；`slice` / `truncate` / `chop` 原地改变本 view。它们按 UTF-8 存储单元计数，所有越界和负参数均是未定义行为。`at`、`operator[]`、`front`、`back` 也不做运行时边界恢复。

### 兼容与版本

`compare()` 的文档列出三种字符串视图重载，自 Qt 6.5 起；`arg()` 自 Qt 6.9 起；`maxSize()` / `max_size()` 与 `slice()` 自 Qt 6.8 起；标准库 view 转换分别要求 Qt 6.7 和 6.10，后者还要求 C++20。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QUtf8StringView()` / `QUtf8StringView(nullptr)` | 创建 null view | `data()==nullptr`、`size()==0`，不拥有数据。 |
| `QUtf8StringView(const Char *)` | 从 NUL 终止指针借用 | 扫描首个 NUL；`nullptr` 安全；不能表示其后的嵌入 NUL 数据。 |
| `QUtf8StringView(const Char *, qsizetype)` | 借用指针和指定长度 | 不扫描终止符；负长度或空指针配正长度是未定义行为。 |
| `QUtf8StringView(first, last)` | 借用半开区间 | 两指针必须是同一有效范围，且 `last >= first`。 |
| `QUtf8StringView(const Container &)` | 借用连续兼容容器 | 容器重分配/析构后 view 失效。 |
| `QUtf8StringView(const Char (&)[N])` | 从字符数组构造 | 借用数组，通常不包含 C 终止符。 |
| `fromArray(array)` | 从整个数组创建 view | 把数组完整长度纳入，适合需要保留 NUL 的数组。 |
| `size()` / `length()` | 返回存储单元数量 | 多字节 UTF-8 字符计为多个单位。 |
| `empty()` / `isEmpty()` | 判断长度是否为 0 | 不等于 null。 |
| `isNull()` | 判断指针是否为空 | empty view 可能仍非 null。 |
| `data()` | 返回首单元指针 | 不保证 NUL 终止；必须搭配 `size()`。 |
| `utf8()` | 返回 `const char8_t *` | 仅 C++20；不终止，不拥有。 |
| `isValidUtf8()` | 验证 UTF-8 编码 | Qt 6.3 起；构造不会自动验证。 |
| `toString()` | 深拷贝为 `QString` | null view 对应 null `QString`；用于延长数据寿命。 |
| `arg(args...)` | 按 `QString::arg` 格式化 | Qt 6.9 起；返回新 `QString`。 |
| `operator[]` / `at()` | 读取指定存储单元 | 越界未定义；不是 Unicode 字符迭代。 |
| `front()` / `back()` | 读取首/尾单元 | 空 view 调用未定义。 |
| `begin()` / `end()` / `cbegin()` / `cend()` | 正向只读迭代 | 迭代器按 UTF-8 单元移动。 |
| `rbegin()` / `rend()` / `crbegin()` / `crend()` | 反向只读迭代 | 同样按原始单元，而非 Unicode grapheme。 |
| `first(n)` / `last(n)` | 返回前/后 `n` 单元的新 view | `0 <= n <= size()`；可能切断多字节序列。 |
| `sliced(pos[, n])` | 返回子 view | 范围越界或负数未定义；不复制。 |
| `chopped(n)` | 返回移除末尾 `n` 单元的新 view | 不修改原 view；`n` 必须在范围内。 |
| `left(n)` / `right(n)` / `mid(pos[, n])` | Qt 兼容子 view API | 头文件公开的零拷贝窗口操作；仍按存储单元。 |
| `slice(pos[, n])` | 原地改为子 view | Qt 6.8 起；只修改当前 view 的窗口。 |
| `truncate(n)` / `chop(n)` | 原地保留前 `n` / 去掉后 `n` 单元 | 不修改底层数据；参数越界未定义。 |
| `compare(QUtf8StringView, cs)` | 比较两个 UTF-8 view | Qt 6.5 起；`cs` 默认大小写敏感。 |
| `compare(QStringView, cs)` / `compare(QLatin1StringView, cs)` | 跨字符串编码比较 | Qt 6.5 起；不产生长期拥有关系。 |
| `compare(QChar, cs)` / `compare(QByteArray, cs)` | 头文件中的补充比较重载 | 适合单字符或 byte array 比较；数据仍按 UTF-8 解释。 |
| `equal(QChar/QStringView/QLatin1StringView/QByteArray)` | 判断相等的辅助 API | 头文件公开；强比较运算符也覆盖常见字符串视图。 |
| `maxSize()` / `max_size()` | 查询理论最大可表示长度 | Qt 6.8 起；实际受进程可用内存限制。 |
| `operator std::string_view()` | 转为 STL 字节 view | Qt 6.7 起；零拷贝且生命周期不变。 |
| `operator std::u8string_view()` | 转为 C++20 UTF-8 STL view | Qt 6.10 起且仅 C++20；零拷贝。 |
| `storage_type` / `value_type` | 视图存储单元类型 | Qt 6 的普通别名跨标准为 `char`；C++20 `char8_t` 版本需显式 namespace。 |
| `pointer` / `const_pointer` / `reference` / `const_reference` | 原始单元指针与引用别名 | 不代表拥有或可修改底层数据。 |
| `iterator` / `const_iterator` / `reverse_iterator` / `const_reverse_iterator` | STL 迭代器别名 | 指向 UTF-8 存储单元。 |
| `size_type` / `difference_type` | 长度与差值类型别名 | 与 `qsizetype` / `qptrdiff` 对应。 |
| `q_no_char8_t::QUtf8StringView` | 普通 Qt 6 UTF-8 view | 全 C++ 标准可用，存储类型为 `char`。 |
| `q_has_char8_t::QUtf8StringView` | C++20 `char8_t` 版 view | 仅 C++20；需要显式写 namespace。 |

---

### 一句话总结

`QUtf8StringView` 用零拷贝方式借用 UTF-8 字节，最适合作为按值传递的接口参数；先保证底层数据存活，再区分 byte offset 与 Unicode 字符边界，并把 `data()` 始终和 `size()` 一起使用。
