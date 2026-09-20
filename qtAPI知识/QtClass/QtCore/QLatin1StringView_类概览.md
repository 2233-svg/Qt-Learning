# Qt QLatin1StringView 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QLatin1StringView>`  
> 所属模块：`Qt6::Core`  
> 继承：无  
> 相关类型：`QLatin1String`、`QLatin1Char`、`QStringView`、`QString`、`QUtf8StringView`、`QByteArrayView`

## 1. 先给结论：它是什么

`QLatin1StringView` 是一个**不拥有数据的 Latin-1 字符串视图**。它只记录一段 `const char` 数据的起始地址和长度，所有读取、搜索、比较和切片操作都围绕这段外部数据进行。

它解决的不是“如何保存一段字符串”，而是：

1. **明确编码**：把 `char` 数据声明为 Latin-1，而不是让调用方和 API 猜测编码。
2. **避免不必要的复制**：从已有字节区间创建 view、切片或查找时，不必先构造 `QString`。
3. **让固定常量进入 Qt 字符串 API**：尤其适合协议关键字、内部标识、文件格式标记和 ASCII/Latin-1 字面量。
4. **在禁止 ASCII 隐式转换的项目中保持高效**：配合 `_L1` 字面量可以明确表达固定 Latin-1 文本。

最重要的一句话是：

> `QLatin1StringView` 可复制，但不拥有字符；复制它只复制指针和长度，不会延长底层数据的生命周期。

如果需要拥有型 Unicode 文本，使用 `QString`；如果输入明确是 UTF-8，使用 `QUtf8StringView` 或 UTF-8 转换 API；如果只是任意二进制，使用 `QByteArrayView`。

## 2. 它的编码语义

Latin-1 是单字节编码。对 `QLatin1StringView` 来说，每个字节值 `0x00..0xFF` 直接映射到 Unicode 码点 `U+0000..U+00FF`。

例如：

```cpp
const char bytes[] = {'A', char(0xE9), 'B'};
QLatin1StringView view(bytes, 3);
QString text = view.toString();
```

其中 `0xE9` 会转成 `U+00E9`，即 `é`。它不是 UTF-8 解码过程。

这两个字节：

```cpp
const char utf8[] = "\xC3\xA9";
```

若作为 UTF-8 解码，代表一个 `é`；若作为长度为 `2` 的 Latin-1 view，则代表两个 Latin-1 字符 `U+00C3` 和 `U+00A9`。包装类型必须和真实数据编码一致。

## 3. 它解决的实际问题

### 3.1 与 `QString` 比较固定的内部关键字

```cpp
#include <QString>
#include <QLatin1StringView>

bool isCommand(const QString &command)
{
    return command == QLatin1StringView("quit");
}
```

Qt 可以直接把 `QString` 与 Latin-1 view 按文本语义比较，调用方不需要先写出一个临时 `QString`。

Qt 6.4 起，也可以写 `_L1`：

```cpp
#include <QString>
#include <QLatin1StringView>

using namespace Qt::StringLiterals;

bool isCommand(const QString &command)
{
    return command == "quit"_L1;
}
```

### 3.2 处理不以 NUL 结尾的定长字段

```cpp
QLatin1StringView headerField(const char *data, qsizetype size)
{
    return QLatin1StringView(data, size);
}
```

带长度的构造不调用 `strlen()`，因此适合：

- 网络帧中的定长字段；
- 文件格式中的字节区间；
- 可能含有嵌入 `'\0'` 的字段；
- 已经由上层计算出长度的缓冲区。

### 3.3 在不复制的情况下取子串

```cpp
using namespace Qt::StringLiterals;

QLatin1StringView extension(QLatin1StringView path)
{
    const qsizetype dot = path.lastIndexOf(QLatin1Char('.'));
    return dot < 0 ? QLatin1StringView() : path.sliced(dot + 1);
}
```

`sliced()` 返回的仍是 view，不会复制字符。它适合短期读取；若结果需要跨越原始缓冲区生命周期保存，应调用 `toString()`。

### 3.4 在 `QT_NO_CAST_FROM_ASCII` 下表达固定文本

`QT_NO_CAST_FROM_ASCII` 常用于阻止没有明确编码的 `const char *` 隐式进入 `QString`。固定的协议或内部文本可以显式使用 `_L1`：

```cpp
using namespace Qt::StringLiterals;

if (method == "POST"_L1) {
    handlePost();
}
```

这并不意味着 `_L1` 适合用户可见文本。用户界面文本仍应通过翻译系统处理。

## 4. 构建与包含

### 4.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 4.2 头文件

```cpp
#include <QLatin1StringView>
```

需要拥有型转换时通常还要使用 `QString`：

```cpp
#include <QString>
```

使用 `_L1` 时：

```cpp
using namespace Qt::StringLiterals;
```

### 4.3 qmake

```qmake
QT += core
```

## 5. 底层模型：指针加长度

从使用者角度，可以把它理解为：

```cpp
const char *data;
qsizetype size;
```

这不是鼓励访问私有布局，而是帮助理解公开行为：

- 拷贝和传值通常很轻量；
- `size()` 不需要扫描终止 NUL；
- 显式长度可以包含嵌入 NUL；
- 所有子 view 仍引用同一底层数据；
- view 的生命周期不能超过数据；
- `data()` 返回的是只读指针。

### 5.1 非空字符串

```cpp
QLatin1StringView text("abc");
```

通常具有：

- `data() != nullptr`；
- `size() == 3`；
- `isNull() == false`；
- `isEmpty() == false`。

### 5.2 空但非 null

```cpp
QLatin1StringView empty("");
```

通常具有：

- `data() != nullptr`；
- `size() == 0`；
- `isNull() == false`；
- `isEmpty() == true`。

### 5.3 null view

```cpp
QLatin1StringView nullView;
QLatin1StringView anotherNull(nullptr);
```

具有：

- `data() == nullptr`；
- `size() == 0`；
- `isNull() == true`；
- `isEmpty() == true`。

`isNull()` 和 `isEmpty()` 表达不同问题：

- `isNull()`：是否没有引用任何数据；
- `isEmpty()`：是否没有字符。

业务只关心“没有字符”时用 `isEmpty()`；需要区分“未提供数据”和“明确提供了空字符串”时同时检查两者。

## 6. 生命周期与所有权

### 6.1 字符串字面量

字符串字面量在程序运行期间一直有效：

```cpp
constexpr QLatin1StringView name("device");
```

它适合作为函数参数、静态常量或长期保存的 view。

### 6.2 局部数组不能返回为长期 view

```cpp
QLatin1StringView makeInvalidView()
{
    const char local[] = "temporary";
    return QLatin1StringView(local);
} // local 销毁
```

返回值只保存地址和长度；`local` 销毁后，返回的 view 悬空。

需要返回拥有结果时：

```cpp
QString makeOwnedText()
{
    const char local[] = "temporary";
    return QLatin1StringView(local).toString();
}
```

### 6.3 `QByteArray` 的数据地址

```cpp
QByteArray storage = loadBytes();
QLatin1StringView view(storage);
```

这个构造不复制 `storage` 的字符。`view` 有效的前提是：

- `storage` 仍然存在；
- `storage` 没有被赋值为其他数据；
- `storage` 没有发生会改变数据地址的重新分配；
- 没有其他代码把共享数据分离或改写到不再匹配的状态。

如果要把结果保存到 `storage` 之外：

```cpp
QString owned = view.toString();
```

### 6.4 从指针和长度构造

```cpp
QLatin1StringView view(data, size);
```

调用方必须保证：

- `size >= 0`；
- `data` 指向至少 `size` 个可读取的 `char`；
- 这段内存的生命周期覆盖 view 的全部使用；
- 数据不会在 view 使用期间被释放、搬迁或不受控地改写。

`data[size]` 不需要存在，末尾也不需要有 NUL。

## 7. 构造函数如何选择

### 7.1 默认构造

```cpp
QLatin1StringView view;
```

创建 null view。它与空但非 null view 都是空的，但 `isNull()` 结果不同。

### 7.2 `std::nullptr_t`

```cpp
QLatin1StringView view(nullptr);
```

从 Qt 6.4 起提供，用于明确创建 null view。

### 7.3 `const char *`

```cpp
QLatin1StringView view("abc");
```

从指针开始读取直到第一个 NUL，形成一个以 NUL 终止的 Latin-1 view。

适合：

- 字符串字面量；
- 确定以 NUL 结尾的 C 字符串。

不适合：

- 不保证 NUL 结尾的网络数据；
- 可能含嵌入 NUL 的定长数据；
- 生命周期不明确的临时缓冲区。

### 7.4 `[first, last)` 指针范围

```cpp
QLatin1StringView view(first, last);
```

表示半开区间 `[first, last)`，长度是 `last - first`。它不查找 NUL。

文档要求：

- `last` 不能位于 `first` 之前；
- `first == nullptr` 时，`last` 也必须是 `nullptr`；
- 两个空指针表示 null view；
- 指针范围在 view 的整个生命周期内必须有效；
- 指针差值必须能用 `qsizetype` 表示。

### 7.5 `const char *, qsizetype`

```cpp
QLatin1StringView view(data, size);
```

这是定长字节区间的首选构造。它保留所有 `size` 个字节，包括内部的 `'\0'`：

```cpp
const char field[] = {'A', '\0', 'B'};
QLatin1StringView view(field, 3);

Q_ASSERT(view.size() == 3);
Q_ASSERT(view.at(1) == QLatin1Char('\0'));
```

### 7.6 `QByteArrayView`

```cpp
QByteArrayView bytes(data, size);
QLatin1StringView view(bytes);
```

这个显式构造函数从 Qt 6.3 起提供。它直接使用 `QByteArrayView` 的长度，不检查 NUL，也不复制数据。

### 7.7 `const QByteArray &`

```cpp
QByteArray storage = loadBytes();
QLatin1StringView view(storage);
```

这是显式构造，不复制字节。它只是把 `QByteArray` 的当前数据区间按 Latin-1 解释；`QByteArray` 这个类型本身并不说明数据是 Latin-1。

## 8. UTF-8 源文件与非 ASCII 字面量

Qt 文档特别提醒：如果源文件按 UTF-8 编码，下面的源代码字符：

```cpp
QLatin1StringView("é");
```

通常会被编译成 UTF-8 的两个字节，而不是单个 Latin-1 字节 `0xE9`。把它作为 Latin-1 解释会得到错误文本。

如果确实需要写出 Latin-1 字节，可以使用数值转义并提供显式长度：

```cpp
QLatin1StringView latin1("\xE9", 1);
```

或者：

```cpp
QLatin1StringView latin1("\351", 1);
```

十六进制转义会继续吸收后续十六进制字符，因此在复杂字节序列中应使用独立数组或显式长度，避免转义边界含糊。

如果文本实际是 UTF-8：

```cpp
QUtf8StringView text(utf8Data, utf8Size);
```

不要先包装成 `QLatin1StringView` 再期待 Qt 恢复正确 Unicode 字符。

## 9. 与其他字符串类型的边界

| 类型 | 是否拥有数据 | 数据单位 | 编码/语义 | 适合场景 |
| --- | --- | --- | --- | --- |
| `QLatin1StringView` | 否 | `char` | Latin-1 | 已知为 Latin-1 的短期视图和固定常量 |
| `QLatin1String` | 否 | `char` | `QLatin1StringView` 的兼容名称 | 维护旧代码 |
| `QStringView` | 否 | UTF-16 code unit | Unicode 文本 | 已有 UTF-16 数据 |
| `QString` | 是 | UTF-16 code unit | 拥有型 Unicode 文本 | 跨生命周期保存文本 |
| `QUtf8StringView` | 否 | UTF-8 字节 | UTF-8 文本 | 输入明确是 UTF-8 |
| `QByteArrayView` | 否 | 原始字节 | 不声明编码 | 二进制或尚未解码的数据 |
| `QByteArray` | 是 | 原始字节 | 拥有字节数据 | 保存、修改或传输字节 |
| `QLatin1Char` | 否 | 一个 Latin-1 单元 | 单个字符 | 字符级比较和 API 参数 |

### 9.1 与 `QLatin1String`

Qt 6.11 中 `QLatin1String` 是 `QLatin1StringView` 的兼容名称。二者使用同一套实现和 API。

新代码推荐：

```cpp
QLatin1StringView value("name");
```

旧代码中的：

```cpp
QLatin1String value("name");
```

可以按同样的 view 语义理解。它不是拥有型字符串。

### 9.2 与 `QStringView`

两者都是 view，但元素编码不同：

- `QLatin1StringView`：每个 `char` 按 `U+0000..U+00FF` 解释；
- `QStringView`：每个元素是 UTF-16 code unit。

已经有 `QString` 或 `QChar` 数据时，不要为了调用 Latin-1 API 重新解释内存；使用 `QStringView`。

### 9.3 与 `QByteArrayView`

`QByteArrayView` 表示字节范围，不声明编码。`QLatin1StringView` 表示同样的字节范围，但明确要求按 Latin-1 解释。

```cpp
QByteArrayView packet(data, size);       // 原始字节
QLatin1StringView name(data, size);      // Latin-1 文本
```

选择取决于协议或文件格式，而不是取决于指针类型是 `char *` 还是 `const char *`。

### 9.4 与 `QUtf8StringView`

UTF-8 是变长编码，Latin-1 是单字节映射。对非 ASCII 文本，两种 view 可能拥有相同的底层 `char` 指针，却代表完全不同的字符序列。

### 9.5 与 `QString`

`QString` 拥有数据，`QLatin1StringView` 不拥有数据。需要把 view 存入长期对象、异步任务、跨线程队列或返回给不控制源缓冲区的调用者时，应明确转换：

```cpp
QString saved = view.toString();
```

## 10. `_L1` 字面量

Qt 6.4 起可以使用 `_L1`：

```cpp
#include <QLatin1StringView>

using namespace Qt::StringLiterals;

constexpr auto method = "GET"_L1;
```

它的类型是 `QLatin1StringView`，字面量操作符收到：

- 指向字面量首字符的 `const char *`；
- 不包含末尾 NUL 的 `size_t` 长度。

所以 `_L1` 按字面量长度建立 view，不需要运行时 `strlen()`：

```cpp
using namespace Qt::StringLiterals;

constexpr auto value = "A\0B"_L1;
static_assert(value.size() == 3);
```

使用 `_L1` 时注意：

- 必须引入 `Qt::StringLiterals`；
- 只能给确实按 Latin-1 解释的字面量使用；
- 它不会把 UTF-8 多字节字面量解码成一个 Unicode 字符；
- 用户可见文本仍应使用翻译 API。

## 11. 单字符访问

### 11.1 `at()`

```cpp
const QLatin1Char ch = view.at(pos);
```

`at()` 返回位置 `pos` 的 `QLatin1Char`。文档要求 `0 <= pos < size()`；Qt 的实现会在调试构建中进行断言检查，但调用方不应把越界当作可恢复行为。

### 11.2 `operator[]`

```cpp
const QLatin1Char ch = view[pos];
```

下标访问不做边界检查。`pos < 0` 或 `pos >= size()` 时行为未定义。需要验证外部索引时，先检查后使用 `at()` 或 `operator[]`。

### 11.3 `front()` 与无参数 `first()`

```cpp
const QLatin1Char first = view.front();
const QLatin1Char same = view.first();
```

无参数 `first()` 等价于 `front()`。二者都要求 view 非空；空 view 上调用是未定义行为。

### 11.4 `back()` 与无参数 `last()`

```cpp
const QLatin1Char last = view.back();
const QLatin1Char same = view.last();
```

无参数 `last()` 等价于 `back()`。同样要求 view 非空。

## 12. 长度与状态查询

### 12.1 `size()`

```cpp
const qsizetype bytes = view.size();
```

返回 view 的元素数。对于 Latin-1 view，一个元素就是一个 `char` 字节。它不扫描 NUL，所以定长区间中的嵌入 NUL 不会截断长度。

### 12.2 `length()`

```cpp
const qsizetype bytes = view.length();
```

返回与 `size()` 相同的值。它从 Qt 6.4 起提供，用于与其他 Qt 容器或字符串 API 保持命名一致。

### 12.3 `isEmpty()` 与 `empty()`

```cpp
if (view.isEmpty()) {
    // size() == 0
}
```

`empty()` 从 Qt 6.4 起提供，是 STL 风格名称，与 `isEmpty()` 等价。

### 12.4 `isNull()`

```cpp
if (view.isNull()) {
    // data() == nullptr
}
```

它只判断底层指针是否为 null，不判断长度是否为零。空但非 null 的 view 会返回 `false`。

### 12.5 `data()`、`latin1()` 与 `constData()`

```cpp
const char *p1 = view.data();
const char *p2 = view.latin1();
const char *p3 = view.constData();
```

- `data()` 返回底层数据起点；
- `latin1()` 也返回 Latin-1 数据起点；
- `constData()` 从 Qt 6.4 起提供，与 `data()` 等价。

这些函数返回只读指针，不保证存在末尾 NUL。显式长度构造的 view 可能没有 `data()[size()]`，也可能在区间内部包含 NUL。

## 13. 迭代器

### 13.1 类型别名

`QLatin1StringView` 的迭代器全部只读：

- `value_type` 是 `const char`；
- `pointer` 和 `const_pointer` 指向 `const char`；
- `reference` 和 `const_reference` 是 `const char &`；
- `iterator` 与 `const_iterator` 相同；
- `reverse_iterator` 与 `const_reverse_iterator` 相同；
- `difference_type` 和 `size_type` 是 `qsizetype`。

它不是可写容器。即使底层数据本身来自可写数组，`QLatin1StringView` 也不提供通过迭代器修改字符的接口。

### 13.2 正向遍历

```cpp
for (auto it = view.cbegin(); it != view.cend(); ++it) {
    const char byte = *it;
    consume(byte);
}
```

可用 API：

- `begin()`；
- `cbegin()`；
- `end()`；
- `cend()`；
- `constBegin()`；
- `constEnd()`。

`begin()`、`cbegin()` 和 `constBegin()` 指向第一个元素；`end()`、`cend()` 和 `constEnd()` 指向尾后位置。尾后迭代器不能解引用。

### 13.3 反向遍历

```cpp
for (auto it = view.crbegin(); it != view.crend(); ++it)
    consume(*it);
```

可用 API：

- `rbegin()`；
- `crbegin()`；
- `rend()`；
- `crend()`。

它们是只读 STL 风格反向迭代器。空 view 可以有相等的起止迭代器，但不能解引用。

## 14. 比较 API

### 14.1 `compare()` 返回值

```cpp
const int result = view.compare(other);
```

返回值只保证符号：

- 小于 `0`：当前 view 在参数之前；
- 等于 `0`：内容相等；
- 大于 `0`：当前 view 在参数之后。

不要依赖返回值一定是 `-1`、`0` 或 `1`，也不要把它固定解释成某两个字节的差值。

### 14.2 支持的比较对象

`compare()` 支持：

- `QLatin1StringView`；
- `QStringView`；
- `QChar`；
- Qt 6.5 起的 `QUtf8StringView`。

默认是 `Qt::CaseSensitive`，可以传入 `Qt::CaseInsensitive`。

### 14.3 与单个 `QChar` 比较

```cpp
if (view.compare(QChar(u'x')) == 0)
    handleSingleCharacter();
```

空 view 与字符比较时不会相等。只有长度为一且内容相同的 view 才与该字符相等。

### 14.4 前缀和后缀

```cpp
using namespace Qt::StringLiterals;

if (view.startsWith("prefix"_L1))
    handlePrefix();

if (view.endsWith(".ini"_L1, Qt::CaseInsensitive))
    handleIni();
```

`startsWith()` 和 `endsWith()` 支持：

- `QLatin1StringView`；
- `QStringView`；
- `QChar`；
- 可选大小写规则。

空模式按字符串 API 的空模式语义处理；如果业务不允许空前缀或空后缀，应先自行判断模式是否为空。

## 15. 搜索与计数

### 15.1 `indexOf()`

```cpp
using namespace Qt::StringLiterals;

const qsizetype pos = view.indexOf("key"_L1);
```

查找第一个匹配位置，找不到返回 `-1`。

支持：

- `QLatin1StringView`；
- `QStringView`；
- `QChar`；
- 带 `Qt::CaseSensitivity` 的字符搜索重载。

`from` 表示开始搜索的位置：

- 默认从 `0` 开始；
- `from == -1` 表示从最后一个位置开始；
- `from == -2` 表示从倒数第二个位置开始；
- 负值按从末尾偏移的规则解释。

例如：

```cpp
using namespace Qt::StringLiterals;

const QLatin1StringView text = "banana"_L1;
Q_ASSERT(text.indexOf("na"_L1) == 2);
Q_ASSERT(text.indexOf("na"_L1, 3) == -1);
```

`from` 不是“跳过多少个字符”的计数器，而是 haystack 内的候选起始索引。

### 15.2 `lastIndexOf()`

`lastIndexOf()` 从后向前寻找最后一个匹配位置：

```cpp
using namespace Qt::StringLiterals;

const QLatin1StringView text = "banana"_L1;
Q_ASSERT(text.lastIndexOf("na"_L1) == 4);
```

支持：

- `QLatin1StringView`；
- `QStringView`；
- `QChar`；
- 带 `from` 和大小写规则的重载。

对带 `from` 的重载：

- `from == -1` 从最后一个字符开始；
- `from == -2` 从倒数第二个字符开始；
- 找不到返回 `-1`。

零长度模式有特殊边界：末尾的空匹配位于最后一个字符之后，当 `from` 为负数时可能被排除。需要精确处理空模式时，先单独判断模式长度，不要只凭 `-1` 的直觉推导。

### 15.3 `contains()`

```cpp
using namespace Qt::StringLiterals;

if (view.contains("error"_L1, Qt::CaseInsensitive))
    reportError();
```

判断是否包含字符或子串。需要位置时应直接调用 `indexOf()`，不要先 `contains()` 再 `indexOf()`，否则会重复扫描。

### 15.4 `count()`

```cpp
using namespace Qt::StringLiterals;

const QLatin1StringView text = "aaaa"_L1;
const qsizetype n = text.count("aa"_L1);
```

`count()` 从 Qt 6.4 起提供，统计字符或子串出现次数。子串计数可能包含重叠匹配：

```cpp
using namespace Qt::StringLiterals;

Q_ASSERT("aaa"_L1.count("aa"_L1) == 2);
```

调用方不能把它理解成“只计算互不重叠的分段数量”。

## 16. 切片 API：哪些会修正边界，哪些要求严格合法

所有切片结果都是 view，不复制底层字符。区别在于边界处理和是否修改当前 view。

### 16.1 `mid(start, length)`

```cpp
auto part = view.mid(start, length);
```

`mid()` 是相对容错的切片：

- `start` 超过当前长度时返回空 view；
- `length < 0` 表示取到末尾；
- `length` 超过剩余长度时只取剩余部分。

它适合长度来自外部或边界尚未完全证明的情况。对严格的内部算法，优先考虑 `sliced()`。

### 16.2 `left(length)`

```cpp
auto prefix = view.left(length);
```

返回开头的 `length` 个字符：

- `length < 0` 时返回整个 view；
- `length >= size()` 时返回整个 view。

Qt 文档建议：如果已经知道 `length` 合法，新代码可以优先使用 `first(length)`。

### 16.3 `right(length)`

```cpp
auto suffix = view.right(length);
```

返回末尾的 `length` 个字符：

- `length < 0` 时返回整个 view；
- `length >= size()` 时返回整个 view。

已知边界合法时，可以使用 `last(length)` 表达更严格的前置条件。

### 16.4 `first(n)`

```cpp
auto prefix = view.first(n);
```

返回前 `n` 个字符。要求 `0 <= n <= size()`；越界是未定义行为。无参数 `first()` 是读取首字符的 API，不要与 `first(n)` 混淆。

### 16.5 `last(n)`

```cpp
auto suffix = view.last(n);
```

返回后 `n` 个字符。要求 `0 <= n <= size()`；越界是未定义行为。无参数 `last()` 返回最后一个 `QLatin1Char`。

### 16.6 `sliced(pos)`

```cpp
auto tail = view.sliced(pos);
```

返回从 `pos` 到末尾的 view。要求：

- `pos >= 0`；
- `pos <= size()`。

它不进行自动截断或容错修正。Qt 6.0 起提供。

### 16.7 `sliced(pos, n)`

```cpp
auto piece = view.sliced(pos, n);
```

返回 `[pos, pos + n)` 的 view。要求：

- `pos >= 0`；
- `pos <= size()`；
- `n >= 0`；
- `n <= size() - pos`。

已知边界合法时，它比 `mid()` 更直接，也避免了不必要的边界调整。

### 16.8 `chopped(n)`

```cpp
auto withoutTail = view.chopped(n);
```

返回去掉末尾 `n` 个字符后的新 view。要求 `0 <= n <= size()`。

### 16.9 `chop(n)`

```cpp
view.chop(n);
```

原地缩短当前 view，等价于保留前 `size() - n` 个字符。要求 `0 <= n <= size()`。

它只修改当前 view 对象的指针/长度视图，不修改底层字符，也不会修改其他指向同一数据的 view。

### 16.10 `truncate(n)`

```cpp
view.truncate(n);
```

原地把当前 view 截断为前 `n` 个字符。要求 `0 <= n <= size()`。它同样不修改底层数据。

### 16.11 `slice(pos)`

```cpp
view.slice(pos);
```

从 Qt 6.8 起提供，原地把当前 view 改为从 `pos` 到末尾的子视图，并返回 `QLatin1StringView &`。

它的边界要求与 `sliced(pos)` 相同，不会自动修正越界位置。

### 16.12 `slice(pos, n)`

```cpp
view.slice(pos, n);
```

从 Qt 6.8 起提供，原地把当前 view 改为 `[pos, pos + n)`，返回自身引用。边界要求与双参数 `sliced()` 相同。

### 16.13 `trimmed()`

```cpp
auto clean = view.trimmed();
```

返回去除首尾空白后的新 view，不修改当前对象，不复制数据。空白判断使用 `QChar::isSpace()` 语义，包括常见 ASCII 空白字符：

- 空格；
- `'\t'`；
- `'\n'`；
- `'\v'`；
- `'\f'`；
- `'\r'`。

返回值仍引用原数据，因此只能在原始缓冲区有效期间使用。

## 17. 转换 API

### 17.1 `toString()`

```cpp
QString owned = view.toString();
```

把 Latin-1 view 转换为拥有数据的 `QString`。每个 Latin-1 字节映射为对应 Unicode 码点。

显式长度 view 中的嵌入 NUL 会成为 `QString` 中的 `U+0000`，不会因遇到 NUL 而截断。

### 17.2 `toUtf8()`

```cpp
QByteArray utf8 = view.toUtf8();
```

Qt 6.9 起提供，返回拥有数据的 UTF-8 `QByteArray`。它比先调用 `toString()` 再调用 `QString::toUtf8()` 更直接。

前提仍然是源 view 的字节确实按 Latin-1 解释；这个函数不会把被错误包装的 UTF-8 字节“猜回”正确文本。

### 17.3 整数转换

Qt 6.4 起提供：

- `toShort()`；
- `toUShort()`；
- `toInt()`；
- `toUInt()`；
- `toLong()`；
- `toULong()`；
- `toLongLong()`；
- `toULongLong()`。

示例：

```cpp
using namespace Qt::StringLiterals;

bool ok = false;
const int value = "0x2A"_L1.toInt(&ok, 0);
if (ok)
    useNumber(value);
```

`base` 默认是 `10`，支持 `0` 和 `2..36`：

- `base == 0` 时，`0x` 或 `0X` 表示十六进制；
- `0b` 或 `0B` 表示二进制；
- 以 `0` 开头时按八进制；
- 其他情况按十进制。

转换会忽略首尾空白，按默认 C locale 进行。失败时返回 `0`，所以必须检查 `ok`，否则无法区分合法数值 `0` 与失败。

### 17.4 浮点转换

```cpp
using namespace Qt::StringLiterals;

bool ok = false;
const double value = "3.14"_L1.toDouble(&ok);
```

支持：

- `toFloat()`；
- `toDouble()`。

合法输入应由数值字符、正负号、小数点和科学计数法相关字符组成。混入单位、逗号或业务后缀会导致失败。

失败通常返回 `0.0`；溢出可能返回无穷大。应通过 `ok` 判断结果是否可用。

需要按用户区域设置解析数字时，使用 `QLocale`，不要把 `QLatin1StringView` 的转换函数当作 locale-aware API。

## 18. `arg()` 格式化

```cpp
using namespace Qt::StringLiterals;

QString message = "failed: %1"_L1.arg("timeout"_L1);
```

`arg()` 把当前 view 当作格式模板，替换 `%N` 占位符并返回拥有数据的 `QString`。它不是 view 操作，结果会脱离原始模式数据。

参数的替换遵循 `QString::arg()` 规则。参数可以是能够隐式转换为 `QAnyStringView` 的字符串类型；Qt 6.9 起对 UTF-8 字符串相关参数的支持更完整。跨 Qt 版本编写公共库时要检查目标版本的重载支持。

需要注意：

- `arg()` 返回 `QString`，不是 `QLatin1StringView`；
- 模板中的 Latin-1 字节必须确实按 Latin-1 解释；
- 用户可见内容仍要考虑翻译，而不是把 `_L1` 当作本地化机制。

## 19. `tokenize()` 惰性分词

```cpp
#include <QStringTokenizer>

using namespace Qt::StringLiterals;

void visit(QLatin1StringView input)
{
    auto tokens = input.tokenize(","_L1);
    for (QLatin1StringView token : tokens)
        consume(token);
}
```

`tokenize()` 从 Qt 6.0 起提供，在分隔符出现处切分字符串，并返回惰性序列。它不会先创建 `QStringList`，token 通常也只是引用原始数据的子 view。

返回值建议使用 `auto`：

```cpp
auto tokens = input.tokenize(separator);
```

不要手写 `QStringTokenizer` 的模板参数，因为返回类型依赖具体的分隔符类型、重载和标志推导。

生命周期要求：

- `input` 的底层数据必须在遍历序列期间有效；
- token 不能保存到源数据失效之后；
- token 是只读 view，不能用它修改原始字符。

## 20. 比较运算符

### 20.1 支持的关系

`QLatin1StringView` 提供强比较关系：

```cpp
==  !=  <  <=  >  >=
```

主要可与以下类型比较：

- `QLatin1StringView`；
- `QChar`；
- `QStringView`；
- `const char *`；
- `QByteArray`；
- Qt 字符串体系中的 `QString` 和其他相关 view。

操作数顺序提供对称重载。

### 20.2 `const char *` 和 `QByteArray` 的编码陷阱

Qt 文档说明，与 `const char *` 和 `QByteArray` 相关的跨类型比较会把字节数组侧按 UTF-8 语义处理，并且相关重载受 `QT_NO_CAST_FROM_ASCII` 配置影响。

因此，如果两侧数据都明确是 Latin-1，优先显式包装两侧：

```cpp
const bool equal =
    QLatin1StringView(leftData, leftSize)
    == QLatin1StringView(rightData, rightSize);
```

如果真正需要的是原始字节比较，不要使用带编码语义的字符串比较，改用 `QByteArrayView` 的字节接口或显式比较长度和字节。

### 20.3 词法顺序

关系运算符按词法顺序比较，不是指针地址比较，也不是简单的“两个内存区是否相同”。如果需要大小写不敏感比较，使用 `compare()` 并传 `Qt::CaseInsensitive`；关系运算符本身不提供大小写参数。

## 21. 静态成员和理论容量

### 21.1 `maxSize()`

```cpp
const qsizetype theoreticalLimit = QLatin1StringView::maxSize();
```

从 Qt 6.8 起提供，返回 view 理论上可表示的最大元素数。实际可用大小还受地址空间、可分配内存和底层连续数据区间限制。

### 21.2 `max_size()`

```cpp
const qsizetype theoreticalLimit = view.max_size();
```

从 Qt 6.8 起提供，是 STL 风格成员，返回与 `maxSize()` 相同的理论上限。

这两个函数都不是分配函数，也不能保证系统真的能提供该大小的缓冲区。

## 22. 版本迁移要点

### 22.1 Qt 6.0

提供：

- `first(qsizetype)`；
- `last(qsizetype)`；
- `sliced(qsizetype)`；
- `sliced(qsizetype, qsizetype)`；
- `toString()`；
- `tokenize()`。

### 22.2 Qt 6.2

提供不带 `from` 的字符串 `lastIndexOf()` 重载：

- `lastIndexOf(QStringView, Qt::CaseSensitivity)`；
- `lastIndexOf(QLatin1StringView, Qt::CaseSensitivity)`。

### 22.3 Qt 6.3

提供：

- `QLatin1StringView(QByteArrayView)`；
- `lastIndexOf(QChar, Qt::CaseSensitivity)`。

### 22.4 Qt 6.4

提供：

- `QLatin1StringView(std::nullptr_t)`；
- `empty()`；
- 无参数 `first()`；
- 无参数 `last()`；
- `length()`；
- `constBegin()`；
- `constData()`；
- `constEnd()`；
- `count()` 的三个重载；
- 数值转换；
- `_L1` 字面量。

### 22.5 Qt 6.5

提供：

- `compare(QUtf8StringView, Qt::CaseSensitivity)`。

### 22.6 Qt 6.7

提供 STL 兼容的：

- `pointer`；
- `const_pointer`。

### 22.7 Qt 6.8

提供：

- `slice(qsizetype)`；
- `slice(qsizetype, qsizetype)`；
- `maxSize()`；
- `max_size()`。

### 22.8 Qt 6.9

提供：

- `toUtf8()`。

## 23. 常见误区与排查顺序

### 23.1 把 view 当成拥有型字符串

看到类型可以复制，不代表字符被复制。先找底层数据拥有者，再判断它是否覆盖 view 的整个使用期。

### 23.2 用 `const char *` 处理定长数据

如果没有 NUL 终止保证：

```cpp
QLatin1StringView view(data);
```

可能越过缓冲区继续寻找 NUL。应使用：

```cpp
QLatin1StringView view(data, size);
```

### 23.3 把 UTF-8 字节包装成 Latin-1

`char *` 只说明元素类型，不说明编码。确认协议编码后再选择 view。

### 23.4 认为 `data()` 一定能传给 C 字符串 API

显式长度构造不保证 NUL 结尾。需要 C 字符串时，应确认底层确实有终止符，或者复制到拥有型并补齐终止符。

### 23.5 在空 view 上访问首尾

`front()`、`back()`、无参数 `first()` 和无参数 `last()` 都要求非空。调用前检查 `!view.isEmpty()`。

### 23.6 混用严格和宽松切片

- 外部或不可信边界：`mid()`、`left()`、`right()`；
- 算法已证明边界合法：`first()`、`last()`、`sliced()`；
- 原地改变当前 view：`slice()`、`chop()`、`truncate()`。

严格 API 越界不是自动截断。

### 23.7 用返回数值判断转换是否成功

合法 `"0"` 和失败都可能返回 `0`。总是传 `bool *ok`。

### 23.8 认为 `count()` 只统计不重叠匹配

字符串子串计数可能包含重叠出现。需要不重叠逻辑时自行推进位置。

### 23.9 把 `trimmed()` 或切片结果当成独立字符串

这些函数返回 view。需要脱离源数据使用时调用 `toString()` 或其他拥有型转换。

### 23.10 把 `_L1` 当作翻译机制

`_L1` 表达编码，不表达语言。用户可见文本仍然需要翻译。

## 24. 逐项 API 说明

### 24.1 构造函数

#### `QLatin1StringView()`

创建 null view，`data() == nullptr`，`size() == 0`。

#### `QLatin1StringView(QByteArrayView str)`

从 Qt 6.3 起提供。引用 `str` 的当前字节区间，不复制，不检查 NUL。`str` 的底层数据必须保持有效且不被不受控地修改。

#### `QLatin1StringView(const QByteArray &str)`

把 `QByteArray` 当前数据区间作为 Latin-1 view，不复制。`QByteArray` 必须在 view 使用期间保持有效。

#### `QLatin1StringView(const char *str)`

引用以 NUL 结尾的 Latin-1 C 字符串。构造时通过终止 NUL 得到长度，源数据必须保持有效。

#### `QLatin1StringView(std::nullptr_t)`

从 Qt 6.4 起提供。显式创建 null view。

#### `QLatin1StringView(const char *first, const char *last)`

引用半开区间 `[first, last)`。不扫描 NUL。指针顺序、空指针组合和生命周期必须符合范围构造要求。

#### `QLatin1StringView(const char *str, qsizetype size)`

按显式长度引用 `size` 个 Latin-1 字节。不要求 NUL，嵌入 NUL 也属于 view 内容。

### 24.2 字符、状态和底层数据

#### `QLatin1Char at(qsizetype pos) const`

读取指定位置。要求 `pos` 在 `[0, size())`。

#### `QLatin1Char operator[](qsizetype pos) const`

只读下标访问。不做边界检查，越界是未定义行为。

#### `QLatin1Char front() const`

返回首字符。空 view 上调用是未定义行为。

#### `QLatin1Char back() const`

返回末字符。空 view 上调用是未定义行为。

#### `QLatin1Char first() const`

Qt 6.4 起提供，等价于 `front()`。空 view 上调用是未定义行为。

#### `QLatin1Char last() const`

Qt 6.4 起提供，等价于 `back()`。空 view 上调用是未定义行为。

#### `bool isNull() const`

判断 `data() == nullptr`。

#### `bool isEmpty() const`

判断 `size() == 0`。

#### `bool empty() const`

Qt 6.4 起提供，等价于 `isEmpty()`。

#### `qsizetype size() const`

返回 view 的字符/字节数量，不扫描 NUL。

#### `qsizetype length() const`

Qt 6.4 起提供，返回 `size()`。

#### `const char *latin1() const`

返回底层 Latin-1 数据起点。不复制，不转码。

#### `const char *data() const`

返回底层数据起点。返回指针只读，且不保证 NUL 结尾。

#### `const char *constData() const`

Qt 6.4 起提供，与 `data()` 等价，用于 Qt 容器风格接口兼容。

### 24.3 迭代器

#### `const_iterator begin() const`

返回首元素的只读迭代器。

#### `const_iterator cbegin() const`

返回首元素的 STL 风格只读迭代器，与 `begin()` 等价。

#### `const_iterator end() const`

返回尾后迭代器，不能解引用。

#### `const_iterator cend() const`

返回 STL 风格尾后迭代器，与 `end()` 等价。

#### `const_iterator constBegin() const`

Qt 6.4 起提供，与 `begin()` 等价。

#### `const_iterator constEnd() const`

Qt 6.4 起提供，与 `end()` 等价。

#### `const_reverse_iterator rbegin() const`

返回反向遍历起点的只读迭代器。

#### `const_reverse_iterator crbegin() const`

返回 const 反向起点，与 `rbegin()` 等价。

#### `const_reverse_iterator rend() const`

返回反向尾后迭代器。

#### `const_reverse_iterator crend() const`

返回 const 反向终点，与 `rend()` 等价。

### 24.4 比较、前缀和后缀

#### `int compare(QLatin1StringView, Qt::CaseSensitivity) const`

比较 Latin-1 view，返回值只保证负、零、正。

#### `int compare(QStringView, Qt::CaseSensitivity) const`

按 Unicode 文本语义与 UTF-16 view 比较，不要求先复制成 `QString`。

#### `int compare(QUtf8StringView, Qt::CaseSensitivity) const`

Qt 6.5 起提供，与 UTF-8 view 比较。它不是把 UTF-8 字节当 Latin-1 字节逐个比较。

#### `int compare(QChar) const`

以大小写敏感方式与单个字符比较。

#### `int compare(QChar, Qt::CaseSensitivity) const`

与单个字符比较，并允许指定大小写规则。

#### `bool startsWith(QLatin1StringView, Qt::CaseSensitivity) const`

判断是否以 Latin-1 view 开头。

#### `bool startsWith(QStringView, Qt::CaseSensitivity) const`

判断是否以 UTF-16 view 开头。

#### `bool startsWith(QChar) const`

判断首字符是否匹配给定字符。空 view 返回 `false`。

#### `bool startsWith(QChar, Qt::CaseSensitivity) const`

按指定大小写规则判断单字符前缀。

#### `bool endsWith(QLatin1StringView, Qt::CaseSensitivity) const`

判断是否以 Latin-1 view 结尾。

#### `bool endsWith(QStringView, Qt::CaseSensitivity) const`

判断是否以 UTF-16 view 结尾。

#### `bool endsWith(QChar) const`

判断末字符是否匹配。空 view 返回 `false`。

#### `bool endsWith(QChar, Qt::CaseSensitivity) const`

按指定大小写规则判断单字符后缀。

### 24.5 查找与计数

#### `qsizetype indexOf(QLatin1StringView, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

查找 Latin-1 子串首次出现位置。找不到返回 `-1`。

#### `qsizetype indexOf(QStringView, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

查找 UTF-16 子串首次出现位置。返回的是当前 Latin-1 view 中的索引。

#### `qsizetype indexOf(QChar, qsizetype from = 0) const`

按大小写敏感方式查找字符。

#### `qsizetype indexOf(QChar, qsizetype from, Qt::CaseSensitivity cs) const`

按指定大小写规则查找字符。

#### `qsizetype lastIndexOf(QLatin1StringView, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

从末尾查找 Latin-1 子串最后位置。Qt 6.2 起提供。

#### `qsizetype lastIndexOf(QLatin1StringView, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

从 `from` 位置向前查找 Latin-1 子串。

#### `qsizetype lastIndexOf(QStringView, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

从末尾查找 UTF-16 子串。Qt 6.2 起提供。

#### `qsizetype lastIndexOf(QStringView, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

从 `from` 位置向前查找 UTF-16 子串。

#### `qsizetype lastIndexOf(QChar) const`

从末尾查找字符。

#### `qsizetype lastIndexOf(QChar, Qt::CaseSensitivity cs) const`

按指定大小写规则从末尾查找字符。Qt 6.3 起提供。

#### `qsizetype lastIndexOf(QChar, qsizetype from) const`

从 `from` 位置向前查找字符。

#### `qsizetype lastIndexOf(QChar, qsizetype from, Qt::CaseSensitivity cs) const`

按指定大小写规则从 `from` 位置向前查找字符。

#### `bool contains(QLatin1StringView, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

判断是否包含 Latin-1 子串。

#### `bool contains(QStringView, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

判断是否包含 UTF-16 子串。

#### `bool contains(QChar, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

判断是否包含字符。

#### `qsizetype count(QLatin1StringView, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

统计 Latin-1 子串出现次数。Qt 6.4 起提供，可能包含重叠匹配。

#### `qsizetype count(QStringView, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

统计 UTF-16 子串出现次数。Qt 6.4 起提供。

#### `qsizetype count(QChar, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

统计字符出现次数。Qt 6.4 起提供。

### 24.6 切片和原地调整

#### `QLatin1StringView mid(qsizetype start, qsizetype length = -1) const`

容错地取得子 view。超出剩余长度的部分会被调整，负 `length` 取到末尾。

#### `QLatin1StringView left(qsizetype length) const`

取得前缀。长度小于零或不小于当前长度时返回整个 view。

#### `QLatin1StringView right(qsizetype length) const`

取得后缀。长度小于零或不小于当前长度时返回整个 view。

#### `QLatin1StringView first(qsizetype n) const`

取得前 `n` 个字符。要求 `n` 在合法范围内。Qt 6.0 起提供。

#### `QLatin1StringView last(qsizetype n) const`

取得后 `n` 个字符。要求 `n` 在合法范围内。Qt 6.0 起提供。

#### `QLatin1StringView sliced(qsizetype pos) const`

从 `pos` 取到末尾。越界是未定义行为。Qt 6.0 起提供。

#### `QLatin1StringView sliced(qsizetype pos, qsizetype n) const`

取得固定区间 `[pos, pos + n)`。越界是未定义行为。Qt 6.0 起提供。

#### `QLatin1StringView chopped(qsizetype n) const`

返回去掉末尾 `n` 个字符后的新 view。要求 `n` 合法。

#### `void chop(qsizetype n)`

原地去掉末尾 `n` 个字符。只修改当前 view。

#### `void truncate(qsizetype length)`

原地保留前 `length` 个字符。只修改当前 view。

#### `QLatin1StringView &slice(qsizetype pos)`

Qt 6.8 起提供。原地切到 `pos`，返回当前 view 引用。

#### `QLatin1StringView &slice(qsizetype pos, qsizetype n)`

Qt 6.8 起提供。原地切成固定区间，返回当前 view 引用。

#### `QLatin1StringView trimmed() const`

返回去掉首尾空白的新 view，不修改当前对象，不复制数据。

### 24.7 转换、格式化和分词

#### `QString toString() const`

把 Latin-1 view 转换为拥有型 `QString`。Qt 6.0 起提供。

#### `QByteArray toUtf8() const`

返回 UTF-8 编码的拥有型 `QByteArray`。Qt 6.9 起提供。

#### `short toShort(bool *ok = nullptr, int base = 10) const`

按指定进制转换为 `short`。Qt 6.4 起提供，失败返回 `0`，用 `ok` 判断成功与否。

#### `ushort toUShort(bool *ok = nullptr, int base = 10) const`

转换为 `ushort`。Qt 6.4 起提供。

#### `int toInt(bool *ok = nullptr, int base = 10) const`

转换为 `int`。Qt 6.4 起提供。

#### `uint toUInt(bool *ok = nullptr, int base = 10) const`

转换为 `uint`。Qt 6.4 起提供。

#### `long toLong(bool *ok = nullptr, int base = 10) const`

转换为 `long`。Qt 6.4 起提供。

#### `ulong toULong(bool *ok = nullptr, int base = 10) const`

转换为 `ulong`。Qt 6.4 起提供。

#### `qlonglong toLongLong(bool *ok = nullptr, int base = 10) const`

转换为 `qlonglong`。Qt 6.4 起提供。

#### `qulonglong toULongLong(bool *ok = nullptr, int base = 10) const`

转换为 `qulonglong`。Qt 6.4 起提供。

#### `float toFloat(bool *ok = nullptr) const`

转换为 `float`。Qt 6.4 起提供。

#### `double toDouble(bool *ok = nullptr) const`

转换为 `double`。Qt 6.4 起提供。

#### `QString arg(Args &&... args) const`

按 `QString::arg()` 规则替换格式占位符，返回拥有型 `QString`。

#### `auto tokenize(Needle &&sep, Flags... flags) const`

按分隔符返回惰性 token 序列。Qt 6.0 起提供，建议用 `auto` 接收。

### 24.8 静态公共成员

#### `static qsizetype maxSize()`

Qt 6.8 起提供，返回理论最大元素数。

#### `qsizetype max_size() const`

Qt 6.8 起提供，返回与 `maxSize()` 相同的理论上限，服务于 STL 兼容。

## API 速查表
### 25.1 构造函数

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QLatin1StringView()` | 创建 null view。 | `data() == nullptr`，但仍然是空 view。 |
| `QLatin1StringView(QByteArrayView str)` | 引用 byte view 的当前区间。 | Qt 6.3 起；不复制、不查找 NUL。 |
| `QLatin1StringView(const QByteArray &str)` | 把 `QByteArray` 当前数据按 Latin-1 解释。 | 显式构造；源数组必须保持有效。 |
| `QLatin1StringView(const char *str)` | 引用 NUL 结尾的 Latin-1 C 字符串。 | 会依赖终止 NUL；不适合定长无终止数据。 |
| `QLatin1StringView(std::nullptr_t)` | 显式创建 null view。 | Qt 6.4 起。 |
| `QLatin1StringView(const char *first, const char *last)` | 引用半开区间 `[first, last)`。 | 不检查 NUL；指针范围必须有效。 |
| `QLatin1StringView(const char *str, qsizetype size)` | 引用显式长度的 Latin-1 字节区间。 | 保留嵌入 NUL；`size` 不得为负。 |

### 25.2 成员类型

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `value_type` | 元素类型 `const char`。 | 只读。 |
| `pointer` | 指向 `const char` 的指针类型。 | Qt 6.7 起；不是可写指针。 |
| `const_pointer` | `pointer` 的兼容别名。 | Qt 6.7 起。 |
| `reference` | `const char &`。 | 不可写。 |
| `const_reference` | `reference` 的兼容别名。 | 只读。 |
| `iterator` | 只读正向迭代器。 | 与 `const_iterator` 相同。 |
| `const_iterator` | 只读正向迭代器。 | 尾后位置不可解引用。 |
| `reverse_iterator` | 只读反向迭代器。 | 与 const 版本相同。 |
| `const_reverse_iterator` | 只读反向迭代器。 | 不提供可写反向迭代。 |
| `difference_type` | `qsizetype`。 | STL 兼容。 |
| `size_type` | `qsizetype`。 | Qt 6 使用可表示更大范围的类型。 |

### 25.3 状态、长度与数据

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `bool isNull() const` | 判断底层指针是否为 null。 | 与 `isEmpty()` 不同。 |
| `bool isEmpty() const` | 判断 `size() == 0`。 | null view 也为空。 |
| `bool empty() const` | `isEmpty()` 的 STL 风格名称。 | Qt 6.4 起。 |
| `qsizetype size() const` | 返回元素/字节数量。 | 不扫描 NUL。 |
| `qsizetype length() const` | 返回 `size()`。 | Qt 6.4 起。 |
| `const char *latin1() const` | 返回 Latin-1 数据起点。 | 不复制、不转码。 |
| `const char *data() const` | 返回底层数据起点。 | 不保证 NUL 结尾。 |
| `const char *constData() const` | 返回底层数据起点。 | Qt 6.4 起；与 `data()` 等价。 |
| `static qsizetype maxSize()` | 返回理论最大元素数。 | Qt 6.8 起；不是实际可分配保证。 |
| `qsizetype max_size() const` | 返回 `maxSize()`。 | Qt 6.8 起；STL 兼容。 |

### 25.4 字符访问

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QLatin1Char at(qsizetype pos) const` | 读取指定字符。 | `pos` 必须在 `[0, size())`。 |
| `QLatin1Char operator[](qsizetype pos) const` | 下标读取。 | 不做边界检查；越界未定义。 |
| `QLatin1Char front() const` | 读取首字符。 | 空 view 上未定义。 |
| `QLatin1Char back() const` | 读取末字符。 | 空 view 上未定义。 |
| `QLatin1Char first() const` | 无参数首字符访问。 | Qt 6.4 起；空 view 上未定义。 |
| `QLatin1Char last() const` | 无参数末字符访问。 | Qt 6.4 起；空 view 上未定义。 |
| `QLatin1StringView first(qsizetype n) const` | 返回前 `n` 个字符的 view。 | Qt 6.0 起；`n` 必须合法。 |
| `QLatin1StringView last(qsizetype n) const` | 返回后 `n` 个字符的 view。 | Qt 6.0 起；`n` 必须合法。 |

### 25.5 迭代器

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `const_iterator begin() const` | 正向遍历起点。 | 只读。 |
| `const_iterator cbegin() const` | STL 风格正向起点。 | 与 `begin()` 等价。 |
| `const_iterator end() const` | 正向尾后位置。 | 不可解引用。 |
| `const_iterator cend() const` | STL 风格正向尾后位置。 | 与 `end()` 等价。 |
| `const_iterator constBegin() const` | Qt 风格 const 起点。 | Qt 6.4 起。 |
| `const_iterator constEnd() const` | Qt 风格 const 尾后位置。 | Qt 6.4 起。 |
| `const_reverse_iterator rbegin() const` | 反向遍历起点。 | 只读。 |
| `const_reverse_iterator crbegin() const` | const 反向起点。 | 与 `rbegin()` 等价。 |
| `const_reverse_iterator rend() const` | 反向尾后位置。 | 不可解引用。 |
| `const_reverse_iterator crend() const` | const 反向尾后位置。 | 与 `rend()` 等价。 |

### 25.6 比较与前后缀

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `compare(QLatin1StringView, Qt::CaseSensitivity)` | 比较两个 Latin-1 view。 | 返回值只保证负、零、正。 |
| `compare(QStringView, Qt::CaseSensitivity)` | 与 UTF-16 view 比较。 | 按文本语义比较。 |
| `compare(QUtf8StringView, Qt::CaseSensitivity)` | 与 UTF-8 view 比较。 | Qt 6.5 起；不是逐字节 Latin-1 比较。 |
| `compare(QChar)` | 与单字符比较。 | 默认大小写敏感。 |
| `compare(QChar, Qt::CaseSensitivity)` | 按指定规则与单字符比较。 | 空 view 不等于字符。 |
| `startsWith(QLatin1StringView, Qt::CaseSensitivity)` | 判断 Latin-1 前缀。 | 默认大小写敏感。 |
| `startsWith(QStringView, Qt::CaseSensitivity)` | 判断 UTF-16 前缀。 | 不需要先复制。 |
| `startsWith(QChar)` | 判断单字符前缀。 | 空 view 返回 `false`。 |
| `startsWith(QChar, Qt::CaseSensitivity)` | 按指定规则判断单字符前缀。 | 文本大小写语义。 |
| `endsWith(QLatin1StringView, Qt::CaseSensitivity)` | 判断 Latin-1 后缀。 | 默认大小写敏感。 |
| `endsWith(QStringView, Qt::CaseSensitivity)` | 判断 UTF-16 后缀。 | 不需要先复制。 |
| `endsWith(QChar)` | 判断单字符后缀。 | 空 view 返回 `false`。 |
| `endsWith(QChar, Qt::CaseSensitivity)` | 按指定规则判断单字符后缀。 | 文本大小写语义。 |

### 25.7 查找与计数

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `indexOf(QLatin1StringView, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive)` | 查找 Latin-1 子串首次位置。 | 找不到返回 `-1`。 |
| `indexOf(QStringView, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive)` | 查找 UTF-16 子串首次位置。 | 返回当前 view 的索引。 |
| `indexOf(QChar, qsizetype from = 0)` | 查找字符。 | 默认大小写敏感。 |
| `indexOf(QChar, qsizetype from, Qt::CaseSensitivity cs)` | 按大小写规则查找字符。 | 支持负 `from`。 |
| `lastIndexOf(QLatin1StringView, Qt::CaseSensitivity cs = Qt::CaseSensitive)` | 查找 Latin-1 子串最后位置。 | Qt 6.2 起。 |
| `lastIndexOf(QLatin1StringView, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive)` | 从位置向前查找 Latin-1 子串。 | 空模式和负 `from` 有边界细节。 |
| `lastIndexOf(QStringView, Qt::CaseSensitivity cs = Qt::CaseSensitive)` | 查找 UTF-16 子串最后位置。 | Qt 6.2 起。 |
| `lastIndexOf(QStringView, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive)` | 从位置向前查找 UTF-16 子串。 | 找不到返回 `-1`。 |
| `lastIndexOf(QChar)` | 查找字符最后位置。 | 默认从末尾开始。 |
| `lastIndexOf(QChar, Qt::CaseSensitivity cs)` | 按大小写规则反向查找字符。 | Qt 6.3 起。 |
| `lastIndexOf(QChar, qsizetype from)` | 从指定位置反向查找字符。 | `-1` 表示末位置。 |
| `lastIndexOf(QChar, qsizetype from, Qt::CaseSensitivity cs)` | 带规则反向查找字符。 | 找不到返回 `-1`。 |
| `contains(QLatin1StringView, Qt::CaseSensitivity cs = Qt::CaseSensitive)` | 判断是否包含 Latin-1 子串。 | 只要布尔结果时使用。 |
| `contains(QStringView, Qt::CaseSensitivity cs = Qt::CaseSensitive)` | 判断是否包含 UTF-16 子串。 | 默认大小写敏感。 |
| `contains(QChar, Qt::CaseSensitivity cs = Qt::CaseSensitive)` | 判断是否包含字符。 | 需要位置时改用 `indexOf()`。 |
| `count(QLatin1StringView, Qt::CaseSensitivity cs = Qt::CaseSensitive)` | 统计 Latin-1 子串。 | Qt 6.4 起；可能重叠计数。 |
| `count(QStringView, Qt::CaseSensitivity cs = Qt::CaseSensitive)` | 统计 UTF-16 子串。 | Qt 6.4 起。 |
| `count(QChar, Qt::CaseSensitivity cs = Qt::CaseSensitive)` | 统计字符。 | Qt 6.4 起。 |

### 25.8 切片与 view 调整

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `mid(qsizetype start, qsizetype length = -1)` | 容错地获取子 view。 | 超界长度会调整；负长度到末尾。 |
| `left(qsizetype length)` | 获取前缀 view。 | 负数或过大时返回整个 view。 |
| `right(qsizetype length)` | 获取后缀 view。 | 负数或过大时返回整个 view。 |
| `sliced(qsizetype pos)` | 从位置取到末尾。 | Qt 6.0 起；严格边界。 |
| `sliced(qsizetype pos, qsizetype n)` | 获取固定区间 view。 | Qt 6.0 起；严格边界。 |
| `chopped(qsizetype n)` | 返回去掉末尾字符的新 view。 | `n` 必须合法。 |
| `chop(qsizetype n)` | 原地去掉末尾字符。 | 只修改当前 view。 |
| `truncate(qsizetype length)` | 原地保留前缀。 | 长度越界未定义。 |
| `slice(qsizetype pos)` | 原地切到末尾。 | Qt 6.8 起；严格边界。 |
| `slice(qsizetype pos, qsizetype n)` | 原地切成固定区间。 | Qt 6.8 起；严格边界。 |
| `trimmed()` | 返回去掉首尾空白的新 view。 | 不复制、不修改源数据。 |

### 25.9 转换、格式化和分词

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QString toString() const` | 转换为拥有型 `QString`。 | Qt 6.0 起；解除生命周期依赖。 |
| `QByteArray toUtf8() const` | 转换为拥有型 UTF-8 字节数组。 | Qt 6.9 起。 |
| `short toShort(bool *ok = nullptr, int base = 10) const` | 转换为 `short`。 | Qt 6.4 起；检查 `ok`。 |
| `ushort toUShort(bool *ok = nullptr, int base = 10) const` | 转换为 `ushort`。 | Qt 6.4 起。 |
| `int toInt(bool *ok = nullptr, int base = 10) const` | 转换为 `int`。 | Qt 6.4 起；支持自动进制。 |
| `uint toUInt(bool *ok = nullptr, int base = 10) const` | 转换为 `uint`。 | Qt 6.4 起。 |
| `long toLong(bool *ok = nullptr, int base = 10) const` | 转换为 `long`。 | Qt 6.4 起。 |
| `ulong toULong(bool *ok = nullptr, int base = 10) const` | 转换为 `ulong`。 | Qt 6.4 起。 |
| `qlonglong toLongLong(bool *ok = nullptr, int base = 10) const` | 转换为 `qlonglong`。 | Qt 6.4 起。 |
| `qulonglong toULongLong(bool *ok = nullptr, int base = 10) const` | 转换为 `qulonglong`。 | Qt 6.4 起。 |
| `float toFloat(bool *ok = nullptr) const` | 转换为 `float`。 | Qt 6.4 起；失败检查 `ok`。 |
| `double toDouble(bool *ok = nullptr) const` | 转换为 `double`。 | Qt 6.4 起；溢出可能为无穷大。 |
| `QString arg(Args &&... args) const` | 替换 `%N` 并返回 `QString`。 | 遵循 `QString::arg()` 规则。 |
| `auto tokenize(Needle &&sep, Flags... flags) const` | 返回惰性分词序列。 | Qt 6.0 起；用 `auto` 接收。 |

### 25.10 非成员比较和字面量

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `operator==` | 比较 view、`QChar`、`QStringView`、`const char *`、`QByteArray` 等。 | 跨编码比较要明确数据语义。 |
| `operator!=` | 不等比较。 | 有对称操作数重载。 |
| `operator<` | 词法小于比较。 | 不是指针或原始地址比较。 |
| `operator<=` | 词法小于等于比较。 | 不是大小写不敏感比较。 |
| `operator>` | 词法大于比较。 | 关系运算符不接受大小写参数。 |
| `operator>=` | 词法大于等于比较。 | 需要忽略大小写时用 `compare()`。 |
| `operator""_L1(const char *str, size_t size)` | 从字面量创建 Latin-1 view。 | Qt 6.4 起；长度不含终止 NUL。 |

`QLatin1StringView` 的核心可以归纳为：**它把一段已知为 Latin-1 的外部字节区间，包装成可与 Qt Unicode API 协作的只读 view。** 只要先确认编码，再确认生命周期，最后根据边界选择严格或容错 API，就不会把它误用成拥有型字符串或 UTF-8 解码器。
