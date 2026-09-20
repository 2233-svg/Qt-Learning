# QByteArrayView 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QByteArrayView>`  
> 所属模块：`Qt6::Core`  
> 引入版本：Qt 6.0  
> 类型性质：只读、非拥有、轻量的连续字节视图；所有成员函数可重入。

## 1. 它解决的核心问题

`QByteArrayView` 用一个指针和一个长度引用一段连续字节。它不复制字节，也不拥有字节，提供 `QByteArray` 的只读子集。

它最适合做接口参数：

```cpp
void parseFrame(QByteArrayView bytes);
```

这一个签名可以自然接受多种字节来源，例如 `QByteArray`、字符串字面量、`std::string`、`std::vector<char>`、`std::array<unsigned char, N>` 或一段原始指针加长度的数据，而不必为每种来源各写一个重载，也不必先构造临时 `QByteArray`。

```cpp
QByteArray packet = readPacket();
parseFrame(packet);

std::string text = "PING";
parseFrame(text);

const unsigned char raw[] = { 0x01, 0x00, 0xFF };
parseFrame(QByteArrayView(raw, 3));
```

它的代价非常低，因此 Qt 明确建议按值传递：

```cpp
void preferred(QByteArrayView view);
```

不建议为了“避免拷贝”写成：

```cpp
void unnecessary(const QByteArrayView &view);
```

视图本身只含少量描述信息，按 const 引用传递反而多了一层间接访问。

## 2. 最重要的规则：它不拥有底层字节

`QByteArrayView` 的安全性完全取决于被引用数据的生命周期。它不会延长 `QByteArray`、`std::string`、数组或外部缓冲区的生存期。

```cpp
QByteArrayView invalidView()
{
    QByteArray local = "payload";
    return local;                 // 错误：返回后 local 已销毁
}
```

正确做法取决于 API 的语义：

- 只在一次同步调用期间查看数据：传 `QByteArrayView` 很合适。
- 需要把数据保存为成员或异步使用：保存拥有者，例如 `QByteArray`。
- 必须返回 view：文档必须承诺底层数据会存活多久，调用方不能超过这个期限保存 view。

```cpp
class Packet {
public:
    QByteArrayView payload() const
    {
        return m_storage.sliced(m_payloadOffset, m_payloadLength);
    }

private:
    QByteArray m_storage;
    qsizetype m_payloadOffset = 0;
    qsizetype m_payloadLength = 0;
};
```

上面返回的 view 只在 `Packet` 和其 `m_storage` 未发生破坏性修改时有效。`Packet` 析构、`m_storage` 被 resize、赋值或引起重分配后，旧 view 都不能继续使用。

## 3. 它是只读视图，不是不可变数据

“只读”说的是通过 `QByteArrayView` 不能修改字节：

```cpp
QByteArrayView view = "hello";
char ch = view[0];                // 可以读
// view[0] = 'H';                 // 不可写
```

但底层数据可能仍被其他持有者修改。例如 view 来自非 const `QByteArray`，调用者后来写入这个数组，view 看到的字节可能变化；若写入导致数组重新分配，view 会悬空。

```cpp
QByteArray bytes = "abc";
QByteArrayView view = bytes;

bytes.append("def");              // 可能使 view 的 data() 失效
```

所以 view 的基本纪律是：

1. 让拥有者活得比 view 久。
2. view 被使用期间，不做可能移动、释放或替换底层存储的操作。
3. 跨线程保存或异步传递时，优先传 `QByteArray`，除非所有权和同步关系已被明确设计。

## 4. 哪些字节类型可以成为视图

Qt 支持以 `char`、`signed char`、`unsigned char` 和 `std::byte` 为元素的连续存储。

| 字节类型 | 是否可用于 QByteArrayView | 常见来源 | 使用时重点注意 |
| --- | --- | --- | --- |
| `char` | 可以 | `QByteArray`、C 字符串、`std::string`、`std::vector<char>`。 | `char` 的正负号由平台决定；二进制数值计算时注意转换。 |
| `signed char` | 可以 | 某些底层协议缓冲区。 | 读取后若按数值解释，注意符号扩展。 |
| `unsigned char` | 可以 | `uchar` 数组、二进制帧和图像数据。 | 转为 `char` 查看时可能显示为负值，字节本身未改变。 |
| `std::byte` | 可以 | C++ 二进制容器。 | 适合明确表达原始字节，不带文本语义。 |

能自动构造 view 的容器还需要满足“连续存储、可用 `std::data()` 取指针、可用 `std::size()` 取长度”的条件。链表、散列表等非连续容器不能直接成为 `QByteArrayView`。

## 5. 构造视图时，长度规则决定是否保留零字节

### 5.1 从 QByteArray 或兼容容器构造

```cpp
QByteArray bytes("A\0B", 3);
QByteArrayView view(bytes);

view.size();                     // 3，嵌入的零字节被保留
```

从 `QByteArray` 或兼容容器构造时，view 使用容器的真实 `data()` 和 `size()`，因此可以保存嵌入的 `'\0'`。

### 5.2 从 C 指针构造会扫描到第一个零字节

```cpp
const char *text = "A\0B";
QByteArrayView view(text);

view.size();                     // 1
```

只传指针的构造函数把输入视为零结尾序列，会从头扫描到第一个 `Byte(0)`。它适合普通 C 字符串，不适合任意二进制数据。

二进制数据应显式传长度：

```cpp
const char raw[] = { 'A', '\0', 'B' };
QByteArrayView view(raw, 3);
```

### 5.3 字符串字面量构造默认不包含尾部零

```cpp
QByteArrayView text("hello");
text.size();                     // 5
```

`QByteArrayView("hello")` 会创建到第一个零字节之前的视图，因此通常符合“文字内容”的直觉。

但 `fromArray()` 的语义不同：它覆盖完整数组，包括字符串字面量末尾的终止零。

```cpp
const auto raw = QByteArrayView::fromArray("hello");
raw.size();                      // 6，包含最后的 '\0'
```

这正是 `fromArray()` 的价值：当数组每个 byte 都是协议数据时，不要让字符串约定偷偷丢弃尾部零。

### 5.4 指针范围和指针加长度

```cpp
const unsigned char buffer[] = { 0x10, 0x00, 0x20, 0x30 };

QByteArrayView a(buffer + 1, buffer + 3); // 0x00, 0x20
QByteArrayView b(buffer, 4);              // 全部四个 byte
```

`first` 和 `last` 必须来自同一连续范围且 `last` 不在 `first` 之前。`data` 加 `len` 时，`len` 不能为负；`data == nullptr` 只允许配合长度 0。

## 6. 空 view 与 null view

`QByteArrayView` 也区分 empty 和 null：

```cpp
QByteArrayView nullView;
QByteArrayView emptyView("", 0);

nullView.isNull();               // true
nullView.isEmpty();              // true

emptyView.isNull();              // false
emptyView.isEmpty();             // true
```

- `isEmpty()` 表示 `size() == 0`。
- `isNull()` 表示 `data() == nullptr`。

绝大多数业务逻辑只需判断 `isEmpty()`。只有需要把“没有指向任何存储”和“指向一段长度为零的存储”区分开时，才使用 `isNull()`。

`toByteArray()` 也保留该差异：只有 null view 转换出的 `QByteArray` 才是 null。

## 7. 切片不复制，也不修改底层数据

`first()`、`last()`、`sliced()`、`chopped()`、`trimmed()` 都返回新的 view，指向同一片底层字节的不同区间。

```cpp
QByteArray packet = "HEAD:BODY";
QByteArrayView whole = packet;

const qsizetype colon = whole.indexOf(':');
QByteArrayView head = whole.first(colon);
QByteArrayView body = whole.sliced(colon + 1);
```

这没有复制 `HEAD` 或 `BODY`。适合解析协议字段、HTTP 头、日志行和分隔符文本。

`slice()`、`chop()`、`truncate()` 会修改“当前 view 的起点或长度”，但仍不会改底层字节：

```cpp
QByteArrayView cursor = packet;
cursor.slice(5);                 // cursor 现在只看 "BODY"
cursor.chop(1);                  // cursor 现在看 "BOD"
```

不要把它们和 `QByteArray::remove()`、`QByteArray::truncate()` 混淆。前者只是调整一个小视图对象，后者会改变拥有数据的数组。

多数严格切片函数在索引或长度越界时属于未定义行为。外部输入解析时，先检查边界，再调用：

```cpp
if (offset <= view.size() && length <= view.size() - offset) {
    const QByteArrayView field = view.sliced(offset, length);
    consume(field);
}
```

旧式 `left()`、`mid()`、`right()` 会对越界参数采取更宽松的截断规则，但 Qt 6.5 起已弃用；新代码使用 `first()`、`last()`、`sliced()`。

## 8. 查找、比较和 ASCII 语义

`QByteArrayView` 提供零拷贝的查找接口：

```cpp
QByteArrayView line = "Content-Length: 42";

if (line.startsWith("Content-Length:")) {
    const QByteArrayView number =
        line.sliced(QByteArrayView("Content-Length:").size()).trimmed();
}
```

常用规则：

- `indexOf()` 和 `lastIndexOf()` 找不到时返回 `-1`。
- `indexOf()` 的负 `from` 从末尾向前偏移计算，`-1` 表示从最后一个 byte 开始。
- `count(QByteArrayView)` 统计可能重叠的子串出现次数。
- `compare()` 可选择大小写敏感或不敏感比较；不敏感比较遵循 C locale 和 ASCII 语义，不是 Unicode 大小写规则。
- 与 `QString`、`QStringView`、`QChar` 等文本类型比较时，字节内容会被解释为 UTF-8。二进制数据不要混用这类跨字符串比较。

`trimmed()` 只移除 C locale 下的 ASCII 空白，例如空格、制表符、换行、回车、垂直制表符和换页符；不会按 Unicode 空白规则处理。

## 9. 数字转换不需要先复制为 QByteArray

从 Qt 6.3 起，`QByteArrayView` 可以直接解析整数和浮点数：

```cpp
QByteArrayView number = "0xFF";
bool ok = false;
const int value = number.toInt(&ok, 0);  // 255
```

整数转换的规则：

- 支持 `base` 为 2 到 36，默认 10。
- `base == 0` 时，`0x` 前缀识别为十六进制，`0` 前缀识别为八进制，其余按十进制。
- 失败时返回 0，因此必须使用 `ok` 区分“合法的零”和“解析失败”。
- 转换采用默认 C locale，不会根据用户地区处理数字格式。

浮点转换同样使用 C locale。解析失败或下溢等情况会返回 0.0，溢出可得到无穷值；需要传 `ok` 才能可靠判断是否成功。用户可见、本地化格式的数字应使用 `QLocale`。

## 10. 转为拥有数据和 C++ 互操作

当需要让数据独立于原始拥有者存活时，调用：

```cpp
QByteArray owned = view.toByteArray();
```

它会深拷贝当前 view 的字节。只在确实需要所有权、异步保存或写入可修改容器时做这一步。

从 Qt 6.7 起，`QByteArrayView` 可转换为 `std::string_view`：

```cpp
std::string_view standardView = view;
```

两者共享相同指针和长度，没有复制，也共享同样的生命周期风险。`std::string_view` 不要求零结尾，不能把它当成 C 字符串。

## 11. 线程边界

所有函数可重入，意味着不同线程操作不同的 `QByteArrayView` 及其稳定数据来源是安全的。

它不使底层字节自动线程安全。一个线程读取 view，另一个线程释放、resize 或写入其底层缓冲区，仍然是数据竞争或悬空访问。跨线程传递 view 时，要么确保底层数据不可变且生命期受控，要么传 `QByteArray` 这样的拥有类型。

## 12. 常见错误

### 12.1 从临时 QByteArray 返回 view

```cpp
QByteArrayView wrong()
{
    return QByteArray("temporary");
}
```

临时对象在表达式结束后销毁。返回拥有的 `QByteArray`，或让 view 指向调用方拥有的稳定存储。

### 12.2 对二进制数据使用只传指针的构造函数

它会扫描到第一个零字节。二进制协议必须使用指针加长度、指针范围、`QByteArray` 或 `fromArray()`。

### 12.3 把 data() 当 C 字符串

`data()` 和 `constData()` 指向的内存不保证以 `'\0'` 结束。只能访问 `[0, size())`，不能直接传给只接受零结尾字符串的 C API。

### 12.4 切片越界

`first()`、`last()`、`sliced()`、`slice()`、`chop()` 和 `truncate()` 的严格边界函数不会替你修正错误参数。解析不可信输入前必须检查长度。

### 12.5 误以为 slice() 会修改 packet

`slice()` 只改 view 自己的指针和长度；底层 `QByteArray` 内容完全不变。

## API 速查表
### 13.1 类型别名

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型别名 | `storage_type` | 内部存储字节类型别名，为 `char`。 | 描述 view 的底层字符存储表示，不表示编码。 |
| 类型别名 | `value_type` | 只读元素类型别名，为 `const char`。 | 元素不可通过 view 修改。 |
| 类型别名 | `size_type` | 长度类型别名，为 `qsizetype`。 | 与 `size()` 返回类型一致，避免缩窄为 `int`。 |
| 类型别名 | `difference_type` | 迭代器差值类型别名，为 `qptrdiff`。 | 主要供泛型算法和迭代器运算使用。 |
| 类型别名 | `pointer` | 只读元素指针别名。 | 即使名字是 pointer，也不能借此改写字节。 |
| 类型别名 | `const_pointer` | const 字节指针别名。 | 对应 `data()` 和 `constData()` 的返回类型。 |
| 类型别名 | `reference` | 只读元素引用别名。 | 不能赋值，view 没有可写元素访问。 |
| 类型别名 | `const_reference` | const 元素引用别名。 | 用于只读泛型接口。 |
| 类型别名 | `iterator` | 只读前向迭代器别名。 | 实际指向 const 字节，不能通过迭代器修改内容。 |
| 类型别名 | `const_iterator` | const 前向迭代器别名。 | 与 `iterator` 都是只读语义。 |
| 类型别名 | `reverse_iterator` | 只读反向迭代器别名。 | 用于从尾到头遍历。 |
| 类型别名 | `const_reverse_iterator` | const 反向迭代器别名。 | 适合 const 上下文的反向遍历。 |

### 13.2 构造与原始数据

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QByteArrayView()` | 构造 null 且 empty 的 view。 | `data()` 为 null；不能由此访问任何字节。 |
| 构造 | `QByteArrayView(std::nullptr_t)` | 从 `nullptr` 构造 null view。 | 等价于默认构造的 null 状态。 |
| 构造 | `QByteArrayView(const QByteArray &byteArray)` | 查看一个 `QByteArray` 的全部有效字节。 | 不复制；数组必须在 view 使用期内存活且不能发生使存储失效的修改。 |
| 构造 | `QByteArrayView(const Container &container)` | 查看兼容连续容器的 data 和 size。 | 容器元素须是兼容 byte 类型，容器本身必须持续有效。 |
| 构造 | `QByteArrayView(const Byte *data)` | 从零结尾 byte 指针构造 view。 | 扫描到第一个零字节；仅适合 C 风格字节字符串。 |
| 构造 | `QByteArrayView(const char (&data)[Size])` | 从 char 数组字面量构造到第一个零字节之前的 view。 | 普通字符串字面量不含尾部零；嵌入零后面的数据也不会纳入。 |
| 构造 | `QByteArrayView(const Byte (&data)[])` | 从未知边界的兼容 byte 数组构造 view。 | Qt 6.9 起提供；按零结尾规则确定长度，数组必须持续有效。 |
| 构造 | `QByteArrayView(const Byte *first, const Byte *last)` | 从首尾指针描述一段连续 byte 范围。 | 指针必须来自同一范围，`last` 不得在 `first` 前；双空指针产生 null view。 |
| 构造 | `QByteArrayView(const Byte *data, qsizetype len)` | 从指针和显式长度构造 view。 | 二进制数据首选；允许嵌入零；`len` 不得为负，空指针只配长度 0。 |
| 工厂 | `static QByteArrayView fromArray(const Byte (&data)[Size])` | 查看数组的全部元素。 | 包含字符串字面量尾部零；需要原始数组完整字节时使用。 |
| 数据 | `const char *data() const` | 返回首字节的只读指针。 | 不保证零结尾，只能访问小于 `size()` 的索引。 |
| 数据 | `const char *constData() const` | 返回首字节的只读指针。 | 与 `data()` 相同；不拥有指针，也不能写入。 |
| 转拥有 | `QByteArray toByteArray() const` | 深拷贝当前 view 数据为拥有的 `QByteArray`。 | 需要跨异步边界或长期保存时使用；null view 才得到 null QByteArray。 |

### 13.3 容量、读取和迭代

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 容量 | `qsizetype size() const` | 返回 view 中的 byte 数。 | 不是底层缓冲容量，也不包含 view 之外数据。 |
| 容量 | `qsizetype length() const` | `size()` 的 Qt 兼容别名。 | 新代码通常统一使用 `size()`。 |
| 容量 | `bool empty() const` | 判断是否没有 byte。 | 与 `isEmpty()` 等价。 |
| 容量 | `bool isEmpty() const` | 判断 `size() == 0`。 | 业务上判断空内容优先用它。 |
| 状态 | `bool isNull() const` | 判断 `data() == nullptr`。 | null 一定 empty，empty 不一定 null。 |
| 容量 | `static qsizetype maxSize()` | 返回一个 view 可表示的最大长度。 | Qt 6.8 起提供；通常只供防御性容量检查。 |
| 容量 | `qsizetype max_size() const` | `maxSize()` 的 STL 风格成员版本。 | Qt 6.8 起提供；不代表当前底层缓冲区实际可用长度。 |
| 读取 | `char operator[](qsizetype n) const` | 读取第 `n` 个 byte。 | 越界属于未定义行为；外部输入先检查边界。 |
| 读取 | `char at(qsizetype n) const` | 读取第 `n` 个 byte。 | 同样要求索引有效，不提供可恢复的越界结果。 |
| 读取 | `char front() const` | 返回第一个 byte。 | 空 view 调用无效，先检查 `isEmpty()`。 |
| 读取 | `char back() const` | 返回最后一个 byte。 | 空 view 调用无效，先检查 `isEmpty()`。 |
| 遍历 | `begin()` | 返回只读起始迭代器。 | 迭代器依赖底层数据稳定；底层重分配后失效。 |
| 遍历 | `end()` | 返回只读尾后迭代器。 | 与 `begin()` 一起用于半开区间。 |
| 遍历 | `cbegin()` | 返回 const 起始迭代器。 | 语义同 `begin()`。 |
| 遍历 | `cend()` | 返回 const 尾后迭代器。 | 语义同 `end()`。 |
| 遍历 | `rbegin()` | 返回只读反向起始迭代器。 | 从最后一个 byte 向前遍历。 |
| 遍历 | `rend()` | 返回只读反向尾后迭代器。 | 与 `rbegin()` 配对。 |
| 遍历 | `crbegin()` | 返回 const 反向起始迭代器。 | 语义同 `rbegin()`。 |
| 遍历 | `crend()` | 返回 const 反向尾后迭代器。 | 语义同 `rend()`。 |

### 13.4 零拷贝切片

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 取子 view | `QByteArrayView first(qsizetype n) const` | 返回前 `n` 个 byte 的新 view。 | `n` 必须在 0 到 `size()` 之间，否则未定义行为。 |
| 取子 view | `QByteArrayView last(qsizetype n) const` | 返回后 `n` 个 byte 的新 view。 | `n` 必须在 0 到 `size()` 之间，否则未定义行为。 |
| 取子 view | `QByteArrayView sliced(qsizetype pos) const` | 返回从 `pos` 到末尾的新 view。 | `pos` 必须在 0 到 `size()` 之间。 |
| 取子 view | `QByteArrayView sliced(qsizetype pos, qsizetype n) const` | 返回从 `pos` 开始、长度为 `n` 的新 view。 | `pos` 和 `n` 必须构成有效范围；不复制底层字节。 |
| 改 view | `QByteArrayView &slice(qsizetype pos)` | 将当前 view 改为从 `pos` 到末尾。 | Qt 6.8 起提供；只改 view 描述，不改底层字节。 |
| 改 view | `QByteArrayView &slice(qsizetype pos, qsizetype n)` | 将当前 view 改为指定子范围。 | Qt 6.8 起提供；越界未定义行为。 |
| 取子 view | `QByteArrayView chopped(qsizetype length) const` | 返回去掉尾部 `length` 个 byte 的新 view。 | `length` 必须合法；不修改当前对象。 |
| 改 view | `void chop(qsizetype length)` | 从当前 view 尾部缩短 `length` 个 byte。 | 只修改当前 view 长度，底层数据不变。 |
| 改 view | `void truncate(qsizetype length)` | 将当前 view 长度截断为 `length`。 | 只修改当前 view；长度必须在有效范围内。 |
| 过时切片 | `QByteArrayView left(qsizetype length) const` | 返回开头指定长度的子 view。 | Qt 6.5 起弃用；新代码使用 `first()`。 |
| 过时切片 | `QByteArrayView right(qsizetype length) const` | 返回末尾指定长度的子 view。 | Qt 6.5 起弃用；新代码使用 `last()`。 |
| 过时切片 | `QByteArrayView mid(qsizetype start, qsizetype length = -1) const` | 返回中间范围的子 view。 | Qt 6.5 起弃用；新代码使用 `sliced()`；旧 API 对越界更宽松。 |

### 13.5 查找、统计与比较

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 前缀 | `bool startsWith(QByteArrayView value) const` | 判断是否以一段 byte 序列开头。 | 按 byte 比较，不自动按文本编码规范化。 |
| 前缀 | `bool startsWith(char ch) const` | 判断首 byte 是否等于 `ch`。 | 空 view 返回 false。 |
| 后缀 | `bool endsWith(QByteArrayView value) const` | 判断是否以一段 byte 序列结尾。 | 按 byte 比较，不自动处理文本换行或编码。 |
| 后缀 | `bool endsWith(char ch) const` | 判断尾 byte 是否等于 `ch`。 | 空 view 返回 false。 |
| 查找 | `qsizetype indexOf(QByteArrayView value, qsizetype from = 0) const` | 向后找子序列第一次出现的位置。 | 找不到返回 `-1`；负 `from` 从末尾偏移计算。 |
| 查找 | `qsizetype indexOf(char ch, qsizetype from = 0) const` | 向后找 byte 第一次出现的位置。 | 找不到返回 `-1`；不要把结果存为无符号类型。 |
| 查找 | `qsizetype lastIndexOf(QByteArrayView value) const` | 查找子序列最后一次出现的位置。 | Qt 6.2 起提供；找不到返回 `-1`。 |
| 查找 | `qsizetype lastIndexOf(QByteArrayView value, qsizetype from) const` | 从指定位置向前找子序列。 | `from` 的负值相对末尾计算；确认起始索引语义。 |
| 查找 | `qsizetype lastIndexOf(char ch, qsizetype from = -1) const` | 从指定位置向前找 byte。 | 默认从最后一个 byte 开始；找不到返回 `-1`。 |
| 判断 | `bool contains(QByteArrayView value) const` | 判断是否包含子序列。 | 等价于检查 `indexOf(value) != -1`。 |
| 判断 | `bool contains(char ch) const` | 判断是否包含某个 byte。 | 二进制零字节同样可被查找。 |
| 统计 | `qsizetype count(QByteArrayView value) const` | 统计子序列出现次数。 | 会统计可能重叠的出现位置。 |
| 统计 | `qsizetype count(char ch) const` | 统计一个 byte 出现次数。 | 仅按字节值统计，不处理字符编码。 |
| 比较 | `int compare(QByteArrayView value, Qt::CaseSensitivity cs = Qt::CaseSensitive) const` | 按字典序比较两个 view。 | Qt 6.2 起提供；大小写不敏感时遵循 C locale 和 ASCII 语义。 |
| 比较 | `operator==` | 判断两个 view 字节内容和长度是否相同。 | 比较内容，不比较是否指向同一块内存。 |
| 比较 | `operator!=` | 判断两个 view 是否不同。 | 是相等比较的反面。 |
| 比较 | `operator<` | 按字典序判断左侧是否更小。 | 用于排序；二进制数据按 byte 顺序比较。 |
| 比较 | `operator<=` | 按字典序判断左侧是否不大于右侧。 | 不涉及编码规范化。 |
| 比较 | `operator>` | 按字典序判断左侧是否更大。 | 不涉及编码规范化。 |
| 比较 | `operator>=` | 按字典序判断左侧是否不小于右侧。 | 不涉及编码规范化。 |

### 13.6 文本检查与数值转换

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 编码检查 | `bool isValidUtf8() const` | 判断字节是否是有效 UTF-8。 | Qt 6.3 起提供；有效 UTF-8 不等于适合业务文本语义。 |
| 空白裁剪 | `QByteArrayView trimmed() const` | 返回去掉两端 C locale ASCII 空白后的新 view。 | Qt 6.3 起提供；不复制字节，也不是 Unicode 空白裁剪。 |
| 整数转换 | `short toShort(bool *ok = nullptr, int base = 10) const` | 解析为有符号短整数。 | Qt 6.3 起提供；失败返回 0，传 `ok` 区分。 |
| 整数转换 | `ushort toUShort(bool *ok = nullptr, int base = 10) const` | 解析为无符号短整数。 | Qt 6.3 起提供；支持 base 0 或 2 到 36。 |
| 整数转换 | `int toInt(bool *ok = nullptr, int base = 10) const` | 解析为 `int`。 | Qt 6.3 起提供；C locale 解析，失败返回 0。 |
| 整数转换 | `uint toUInt(bool *ok = nullptr, int base = 10) const` | 解析为 `uint`。 | Qt 6.3 起提供；输入负号或溢出时检查 `ok`。 |
| 整数转换 | `long toLong(bool *ok = nullptr, int base = 10) const` | 解析为 `long`。 | Qt 6.3 起提供；`long` 位宽依赖平台。 |
| 整数转换 | `ulong toULong(bool *ok = nullptr, int base = 10) const` | 解析为 `ulong`。 | Qt 6.3 起提供；跨平台协议字段优先固定宽度整数。 |
| 整数转换 | `qlonglong toLongLong(bool *ok = nullptr, int base = 10) const` | 解析为 64 位有符号 Qt 整数。 | Qt 6.3 起提供；失败时不只看返回 0。 |
| 整数转换 | `qulonglong toULongLong(bool *ok = nullptr, int base = 10) const` | 解析为 64 位无符号 Qt 整数。 | Qt 6.3 起提供；验证范围并检查 `ok`。 |
| 浮点转换 | `float toFloat(bool *ok = nullptr) const` | 解析为 `float`。 | Qt 6.3 起提供；失败或下溢会返回 0.0，溢出可能为无穷值。 |
| 浮点转换 | `double toDouble(bool *ok = nullptr) const` | 解析为 `double`。 | Qt 6.3 起提供；采用 C locale，用户地区格式请用 `QLocale`。 |
| 标准库互操作 | `operator std::string_view() const` | 零拷贝转换为 `std::string_view`。 | Qt 6.7 起提供；新 view 共享同一生命周期风险，不保证零结尾。 |

## 14. 一句话总结

`QByteArrayView` 是零拷贝的只读 byte 参数类型：用它统一接收连续字节数据，用显式长度保护二进制零字节，用切片避免复制，并始终让底层拥有者活得比 view 久。
