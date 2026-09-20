# Qt QLatin1String 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QLatin1String>`  
> 实际实现头文件：`<QtCore/qlatin1stringview.h>`  
> 所属模块：`Qt6::Core`  
> 继承：无  
> 相关类型：`QLatin1StringView`、`QStringView`、`QString`、`QByteArrayView`、`QUtf8StringView`

## 1. 先给结论：`QLatin1String` 是什么

在 Qt 6.11 中，`QLatin1String` 与 `QLatin1StringView` 是同一个类型的两个名称。Qt 文档明确说明，`QLatin1String` 只是为了兼容旧代码而保留，新代码推荐使用 `QLatin1StringView`。

因此，不能把这篇笔记理解成“另一个拥有字符串数据的值类型”。准确的理解是：

> `QLatin1String` 是一段已知采用 Latin-1 解释的 `const char` 字节序列视图；它只保存指针和长度，不拥有、不复制底层字符。

它主要解决三个问题：

1. **明确编码**：告诉 Qt，这段 `char` 数据不是默认按 UTF-8 解释，而是按 Latin-1 解释。
2. **避免不必要的临时 `QString`**：比较、前缀判断、后缀判断和搜索等操作可以直接在 Latin-1 数据上完成。
3. **支持禁用 ASCII 隐式转换的工程**：定义 `QT_NO_CAST_FROM_ASCII` 后，使用 `_L1` 字面量或显式 `QLatin1StringView` 仍然可以高效地表达固定 Latin-1 文本。

如果只是阅读旧代码，看到 `QLatin1String` 可以按 `QLatin1StringView` 理解；如果正在写新代码，优先写 `QLatin1StringView`。

## 2. 它解决的实际问题

### 2.1 在 `QString` 上比较固定的 Latin-1 常量

```cpp
#include <QString>
#include <QLatin1StringView>

bool isKeyword(const QString &word)
{
    return word == QLatin1StringView("while");
}
```

这里的 `QLatin1StringView` 只是一个指针加长度的小对象。`QString` 与 Latin-1 view 的比较可以直接按两种编码的语义比较，不需要先写出一个临时 `QString("while")`。

Qt 6.4 起，更适合使用 `_L1` 字面量：

```cpp
#include <QString>
#include <QLatin1StringView>

using namespace Qt::StringLiterals;

bool isKeyword(const QString &word)
{
    return word == "while"_L1;
}
```

`"while"_L1` 的类型是 `QLatin1StringView`，长度由字符串字面量的编译期长度决定。

### 2.2 在 `QT_NO_CAST_FROM_ASCII` 下表达固定文本

有些项目会定义 `QT_NO_CAST_FROM_ASCII`，防止普通 `const char *` 在不明确编码的情况下隐式进入 `QString`。这可以帮助项目强制区分：

- 用户可见文本：应经过翻译系统，例如 `QObject::tr()`；
- 协议关键字、内部标识、文件格式标记：可以明确声明为 Latin-1 或 UTF-8。

这时可以写：

```cpp
#include <QString>
#include <QLatin1StringView>

using namespace Qt::StringLiterals;

bool isHeaderName(const QString &name)
{
    return name.compare("Content-Type"_L1, Qt::CaseInsensitive) == 0;
}
```

这里的 `_L1` 不是把字符串翻译成用户界面文本，而是声明“这个固定字面量按 Latin-1 处理”。

### 2.3 从已知为 Latin-1 的字节缓冲区中取视图

如果协议、旧式配置文件或设备接口明确规定字段是 Latin-1，可以从带长度的数据建立视图：

```cpp
#include <QLatin1StringView>

QLatin1StringView fieldView(const char *data, qsizetype size)
{
    return QLatin1StringView(data, size);
}
```

这个构造函数不会寻找 `'\0'`，也不会复制数据。因此它适合处理：

- 包含嵌入零字节的定长字段；
- 不以 NUL 结尾的网络帧；
- 已经由上层计算好的 `[data, data + size)` 区间。

但它只有在底层缓冲区仍然存在且没有被修改时才有效。返回 view 后，不能立刻释放或重新分配这块缓冲区。

### 2.4 在不分配新字符串的情况下做扫描和切片

```cpp
#include <QLatin1StringView>

QLatin1StringView fileExtension(QLatin1StringView path)
{
    const qsizetype dot = path.lastIndexOf('.');
    if (dot < 0)
        return {};
    return path.sliced(dot + 1);
}
```

`lastIndexOf()` 返回位置，`sliced()` 返回同一底层数据的一段新 view。两步都不复制字符。需要注意，返回的是 view，不是独立字符串；如果原始 `path` 的数据失效，返回值也会失效。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

旧代码可以继续：

```cpp
#include <QLatin1String>
```

新代码建议直接包含：

```cpp
#include <QLatin1StringView>
```

`<QLatin1String>` 是一个兼容入口，内容导出的是同一套 `QLatin1StringView` 实现。

### 3.3 qmake

```qmake
QT += core
```

## 4. 底层模型：两个字段，三个重要状态

从使用语义上，可以把一个 `QLatin1String` 看成：

```cpp
const char *data;
qsizetype size;
```

实际成员布局和字段顺序属于实现细节，但“指针加长度”的模型很重要。它解释了以下行为：

- 拷贝 view 很便宜，只复制指针和长度；
- view 不负责释放数据；
- `size()` 不需要扫描 `'\0'`；
- 带显式长度的构造可以保留嵌入零字节；
- view 的生命周期不能超过被引用数据；
- 修改底层字符会立即改变 view 看到的内容，前提是修改本身没有违反调用方契约。

### 4.1 非空、非空串

```cpp
QLatin1StringView text("abc");
```

此时：

- `data()` 指向字面量首字符；
- `size()` 为 `3`；
- `isNull()` 为 `false`；
- `isEmpty()` 为 `false`。

### 4.2 空但非 null

```cpp
QLatin1StringView empty("");
```

此时通常是：

- `data()` 非空；
- `size()` 为 `0`；
- `isNull()` 为 `false`；
- `isEmpty()` 为 `true`。

这是“有一个有效的空数据区间”。

### 4.3 null 且为空

```cpp
QLatin1StringView nullView;
QLatin1StringView alsoNull(nullptr);
```

此时：

- `data()` 为 `nullptr`；
- `size()` 为 `0`；
- `isNull()` 为 `true`；
- `isEmpty()` 也为 `true`。

所以 `isEmpty()` 不能区分“空但有指针”和“null”。需要判断是否“没有提供数据”时，使用 `isNull()`；只关心是否没有字符时，使用 `isEmpty()`。

## 5. Latin-1 到 Unicode 的含义

Latin-1 是一种单字节编码。对 `QLatin1String` 来说，每个 `unsigned char` 值 `0x00..0xFF` 对应一个 Unicode 码点 `U+0000..U+00FF`。

例如：

```cpp
const char bytes[] = "\xE9";
QLatin1StringView view(bytes, 1);
QString result = view.toString();
```

`0xE9` 会被解释为 `U+00E9`，也就是 `é`。它不会被解释成 UTF-8 的两个或多个字节。

这也是最容易出错的边界：

```cpp
QLatin1StringView wrong("\xC3\xA9", 2);
```

这两个字节如果本来是 UTF-8 的 `é`，在 Latin-1 语义下会变成两个字符 `U+00C3` 和 `U+00A9`，而不是一个 `U+00E9`。

### 5.1 UTF-8 源文件中的非 ASCII 字面量

Qt 文档特别提醒：如果源文件采用 UTF-8，`QLatin1StringView("é")` 里的源代码字符通常会被编译成 UTF-8 字节序列，而不是单个 Latin-1 字节。因此不要把源文件中的非 ASCII 字面量直接交给 `QLatin1String`。

可选做法是：

```cpp
QLatin1StringView latin1("\xE9", 1);
```

或者：

```cpp
QLatin1StringView latin1("\351", 1);
```

对十六进制转义要注意 C++ 的十六进制转义会继续吞掉后续十六进制字符；需要明确长度时，最好同时提供显式长度，或者把字节放进独立数组中。

### 5.2 不是 UTF-8 解码器

`QLatin1String` 不负责：

- 检查输入是否是合法 UTF-8；
- 把 UTF-8 多字节序列解码成 Unicode；
- 按系统区域设置解释字节；
- 猜测调用方真正想使用的编码。

如果输入确定是 UTF-8，应使用 `QUtf8StringView`、`QString::fromUtf8()` 或相应的 UTF-8 API。如果输入只是任意二进制数据，不应使用 `QLatin1String` 伪装成文本。

## 6. 生命周期与所有权

### 6.1 字符串字面量

字符串字面量具有整个程序运行期的生命周期，适合作为 view 的底层数据：

```cpp
constexpr QLatin1StringView name("device");
```

不过，新代码更推荐：

```cpp
using namespace Qt::StringLiterals;
constexpr auto name = "device"_L1;
```

### 6.2 局部数组

局部数组只在作用域内有效：

```cpp
QLatin1StringView makeView()
{
    const char local[] = "temporary";
    return QLatin1StringView(local);
} // local 在这里销毁
```

上面的返回值悬空，调用者不能使用。view 本身没有任何机制延长 `local` 的生命周期。

### 6.3 `QByteArray`

从 `QByteArray` 构造 view 时不会复制数据：

```cpp
QByteArray storage = readPacket();
QLatin1StringView view(storage);
```

`view` 只能在 `storage` 仍然存在、且没有发生会改变数据地址的操作期间使用。下面的操作可能让原有 view 失效或改变它所看到的内容：

- `storage` 被销毁；
- `storage` 重新分配；
- `storage` 被赋值为另一个数组；
- 对共享数据执行写操作并触发分离；
- 其他会修改底层字节的操作。

如果需要跨越 `QByteArray` 生命周期保存文本，应复制成 `QString` 或另一个拥有数据的类型：

```cpp
QString owned = view.toString();
```

### 6.4 指针和显式长度

```cpp
QLatin1StringView view(data, size);
```

调用方必须保证：

- `data` 指向至少 `size` 个可读取的 `char`；
- `size >= 0`；
- 这段内存的生命周期覆盖所有 view 使用；
- 不要在 view 仍然使用时释放、移动或重新分配数据。

构造函数不要求 `data[size]` 存在，也不要求末尾有 NUL。

## 7. 构造函数的选择

### 7.1 默认构造

```cpp
QLatin1StringView view;
```

创建 null view，等价于保存 `nullptr` 和长度 `0`。

### 7.2 `std::nullptr_t`

```cpp
QLatin1StringView view(nullptr);
```

同样创建 null view。这个重载从 Qt 6.4 开始提供，作用是让 `nullptr` 的意图明确且可在 `constexpr` 上下文中使用。

### 7.3 `const char *`

```cpp
QLatin1StringView view("abc");
```

构造函数会从指针开始寻找终止 NUL，并把 NUL 之前的字符作为 view。传入非空指针时，指针必须指向以 NUL 结尾的可读字符序列。

它适合：

- 字符串字面量；
- 确实保证 NUL 结尾的 C 字符串。

它不适合：

- 不带 NUL 的网络字段；
- 可能包含嵌入零字节的数据；
- 不能保证生命周期的临时缓冲区。

### 7.4 `const char *first, const char *last`

```cpp
QLatin1StringView view(first, last);
```

表示半开区间 `[first, last)`，长度是 `last - first`。它不扫描 NUL。

边界要求：

- `last` 不能位于 `first` 之前；
- `first == nullptr` 时，`last` 也必须是 `nullptr`；
- `first == nullptr && last == nullptr` 表示 null view；
- 该范围必须在 view 的整个使用期间保持有效；
- 文档还限制了指针差值不能超过可表示范围。

### 7.5 `const char *data, qsizetype size`

```cpp
QLatin1StringView view(data, size);
```

这是处理定长缓冲区最明确的构造方式。`size` 是字节数，不是以 NUL 结尾的字符串长度猜测值。

嵌入的 `'\0'` 会被包含在 view 中：

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

这个构造函数从 Qt 6.3 开始提供。它直接使用 `QByteArrayView` 的长度，不检查 NUL 终止符。`QByteArrayView` 内部数据也不会被复制，因此生命周期规则与显式指针长度构造相同。

### 7.7 `const QByteArray &`

```cpp
QByteArray bytes = load();
QLatin1StringView view(bytes);
```

这是显式构造，不会复制。它把 `QByteArray` 的现有数据区间视为 Latin-1；不要因为类型叫 `QByteArray` 就自动假设它是 UTF-8 或 NUL 结尾。

## 8. `QLatin1String`、`QLatin1StringView` 和其他字符串类型的边界

| 类型 | 是否拥有数据 | 数据单位 | 主要语义 | 适合场景 |
| --- | --- | --- | --- | --- |
| `QLatin1String` | 否 | `char` | 兼容名称，按 Latin-1 解释 | 维护旧 API |
| `QLatin1StringView` | 否 | `char` | 按 Latin-1 解释的字符串视图 | 新代码中的固定 Latin-1 文本和短期视图 |
| `QStringView` | 否 | UTF-16 `QChar` | Unicode 字符串视图 | 已经有 UTF-16 数据且不想复制 |
| `QString` | 是 | UTF-16 `QChar` | 拥有 Unicode 文本 | 需要跨越生命周期保存文本 |
| `QUtf8StringView` | 否 | UTF-8 字节 | 按 UTF-8 解释 | 输入已明确是 UTF-8 |
| `QByteArrayView` | 否 | 原始字节 | 默认不声明字符编码 | 二进制或未解码协议数据 |
| `QByteArray` | 是 | 原始字节 | 拥有字节数组 | 需要保存、修改或传输字节数据 |
| `QLatin1Char` | 否 | 一个 Latin-1 字节 | 单个 Latin-1 字符 | 与 `QChar` 或字符串 API 比较单字符 |

### 8.1 与 `QStringView` 的区别

`QLatin1StringView` 通过 `char` 保存每个 Latin-1 单元；`QStringView` 通过 UTF-16 单元保存 Unicode 文本。两者都不拥有数据，但底层编码不同。

这意味着：

- 只有确实知道数据是 Latin-1 时才构造 `QLatin1StringView`；
- 已经有 `QString` 或 UTF-16 数据时，使用 `QStringView` 更直接；
- 二者相互比较时，Qt 会按文本语义处理编码转换，不等价于逐字节比较。

### 8.2 与 `QByteArrayView` 的区别

`QByteArrayView` 只是字节范围，不表达编码。`QLatin1StringView` 则明确表达“这些字节按 Latin-1 解释”。

如果协议字段是二进制：

```cpp
QByteArrayView payload(data, size);
```

如果协议规范明确规定字段是 Latin-1 文本：

```cpp
QLatin1StringView name(data, size);
```

不要仅仅因为数据类型是 `char *` 就选择 `QLatin1StringView`。

### 8.3 与 `QUtf8StringView` 的区别

UTF-8 是变长编码，单个 Unicode 字符可能占多个字节；Latin-1 每个字节直接映射到一个 Unicode 码点。二者不能互换。

```cpp
const char utf8[] = "\xC3\xA9";
QUtf8StringView utf8View(utf8);
QLatin1StringView latin1View(utf8, 2);
```

前者表示一个 UTF-8 字符 `é`，后者表示两个 Latin-1 字符。选择哪一个必须由数据格式决定。

### 8.4 与 `QString` 的区别

`QString` 拥有数据，适合保存结果：

```cpp
QString saved = QLatin1StringView("persistent").toString();
```

`QLatin1StringView` 适合临时读取、比较和扫描。需要把 view 存进对象成员、跨线程传递、异步处理或脱离源缓冲区使用时，应先确认数据生命周期，必要时转换为 `QString`。

## 9. `_L1` 字面量

Qt 6.4 起可以使用 `_L1`：

```cpp
#include <QLatin1StringView>

using namespace Qt::StringLiterals;

constexpr auto method = "GET"_L1;
```

其返回类型是 `QLatin1StringView`。字面量操作符收到的是：

- 指向字面量首字符的 `const char *`；
- 不含末尾终止 NUL 的 `size_t` 长度。

因此 `_L1` 是“按字面量长度创建 view”，而不是运行时调用 `strlen()`。嵌入 NUL 的字面量也能保留：

```cpp
using namespace Qt::StringLiterals;

constexpr auto value = "A\0B"_L1;
static_assert(value.size() == 3);
```

使用 `_L1` 的重点是：

- 需要 `using namespace Qt::StringLiterals;`；
- 只应给确实按 Latin-1 解释的字面量使用；
- `_L1` 不会把 UTF-8 多字节字面量解码成 Unicode；
- 如果文本是用户可见内容，不要用 `_L1` 代替翻译系统。

## 10. 常用使用流程

### 10.1 只比较一个固定标识

```cpp
using namespace Qt::StringLiterals;

bool isMode(const QString &mode)
{
    return mode == "fast"_L1;
}
```

### 10.2 忽略大小写比较

```cpp
using namespace Qt::StringLiterals;

bool isContentType(const QString &value)
{
    return value.compare("application/json"_L1,
                         Qt::CaseInsensitive) == 0;
}
```

大小写不敏感比较是文本比较语义，不要把它理解成简单的 ASCII `tolower()`。输入若包含非 ASCII Latin-1 字符，具体大小写折叠规则仍应以 Qt 的 Unicode 处理为准。

### 10.3 在已有 Latin-1 缓冲区中查找字段

```cpp
qsizetype findSeparator(const char *data, qsizetype size)
{
    QLatin1StringView line(data, size);
    return line.indexOf(':');
}
```

返回值为字符位置，找不到返回 `-1`。位置是 view 内的索引，不是底层文件或网络缓冲区的绝对地址。

### 10.4 取出不拥有数据的子视图

```cpp
QLatin1StringView trimPrefix(QLatin1StringView value)
{
    using namespace Qt::StringLiterals;
    if (value.startsWith("id="_L1))
        return value.sliced(3);
    return value;
}
```

返回结果仍然引用原始数据。如果调用方要保存它，应保存原始拥有者，或者调用 `toString()` 复制。

### 10.5 切分字符串

```cpp
#include <QStringTokenizer>

void visitParts(QLatin1StringView input)
{
    using namespace Qt::StringLiterals;

    auto parts = input.tokenize(","_L1);
    for (QLatin1StringView part : parts)
        consume(part);
}
```

`tokenize()` 返回惰性序列，不是立刻分配并生成 `QStringList`。返回对象和它产生的子视图都依赖原始输入数据有效。

## 11. 查询和索引 API 的边界

### 11.1 `at()` 与 `operator[]`

```cpp
QLatin1Char a = view.at(pos);
QLatin1Char b = view[pos];
```

二者都返回 `QLatin1Char`，不是 `char &`，因为 view 不支持可写迭代器和可写下标。

文档语义是：

- `at(pos)` 在调试构建中会断言 `0 <= pos < size()`；
- 越界行为不应被调用方依赖；
- `operator[]` 不做边界检查，越界是未定义行为。

需要处理不可信索引时，先检查：

```cpp
if (pos >= 0 && pos < view.size())
    use(view.at(pos));
```

### 11.2 `front()`、`back()`、`first()`、`last()`

这些 API 都要求 view 非空：

- `front()` 等价于 `at(0)`；
- `back()` 等价于 `at(size() - 1)`；
- 无参数 `first()` 与 `front()` 等价；
- 无参数 `last()` 与 `back()` 等价。

在空 view 上调用它们是未定义行为。`first(n)` 和 `last(n)` 是范围切片版本，要求 `0 <= n <= size()`。

### 11.3 `isEmpty()`、`empty()`、`isNull()`

```cpp
if (view.isEmpty()) {
    // 没有字符
}

if (view.isNull()) {
    // 没有引用任何数据
}
```

`empty()` 是 Qt 6.4 起提供的 STL 兼容拼法，与 `isEmpty()` 等价。它不能替代 `isNull()`。

## 12. 搜索、比较和计数

### 12.1 比较结果

```cpp
int result = view.compare(other);
```

`compare()` 的返回值只保证符号：

- 小于 `0`：当前 view 排在参数之前；
- 等于 `0`：内容相等；
- 大于 `0`：当前 view 排在参数之后。

不要把返回值当成“字符差值”或固定的 `-1/0/1`。如果只需要相等判断，直接用 `==`；如果需要排序，使用比较结果的符号。

支持比较：

- `QLatin1StringView`；
- `QStringView`；
- `QChar`；
- Qt 6.5 起的 `QUtf8StringView`。

可以传 `Qt::CaseInsensitive` 做大小写不敏感比较。

### 12.2 `startsWith()` 与 `endsWith()`

这两个 API 支持：

- `QChar`；
- `QLatin1StringView`；
- `QStringView`；
- 可选的 `Qt::CaseSensitivity`。

默认是 `Qt::CaseSensitive`。传入空 view 时，前缀和后缀判断应按“空字符串匹配任意位置”的字符串语义理解；如果业务上不允许空模式，应在调用前自行拒绝。

### 12.3 `indexOf()`

`indexOf()` 查找第一个匹配位置：

```cpp
using namespace Qt::StringLiterals;
const qsizetype pos = view.indexOf("key"_L1);
```

找不到返回 `-1`。`from` 是开始搜索的索引：

- 默认从 `0` 开始；
- `from == -1` 表示从最后一个字符开始；
- `from == -2` 表示从倒数第二个字符开始；
- 更小的负值以相同规则向前推移。

支持搜索 `QChar`、`QLatin1StringView` 和 `QStringView`，并可指定大小写敏感性。

### 12.4 `lastIndexOf()`

`lastIndexOf()` 从后向前查找最后一个匹配位置。对带 `from` 的重载：

- `from == -1` 从最后一个字符开始；
- `from == -2` 从倒数第二个字符开始；
- 找不到返回 `-1`。

空模式有一个容易忽略的边界：当以负数 `from` 搜索零长度字符串时，位于数据末尾的空匹配会被排除，因为它在最后一个字符之后。若需要包含末尾的空匹配，省略 `from` 或使用合适的非负位置。

### 12.5 `contains()`

`contains()` 是“查找位置不等于 `-1`”的布尔接口，支持字符、Latin-1 view 和 UTF-16 view。需要位置时不要先 `contains()` 再 `indexOf()`，直接调用 `indexOf()` 可以避免重复扫描。

### 12.6 `count()`

`count()` 统计字符或子串出现次数，支持大小写敏感性。Qt 文档明确说明，子串匹配可以计入**重叠出现**：

```cpp
using namespace Qt::StringLiterals;
QLatin1StringView value = "aaa"_L1;
const qsizetype count = value.count("aa"_L1); // 2
```

这里的两个匹配分别从位置 `0` 和 `1` 开始，因此是 `2`，不是只取不重叠区间后的 `1`。

## 13. 切片 API：安全边界与快速边界

`QLatin1String` 的切片函数都返回 view，不复制字符。差异主要在于是否对边界做调整或检查。

### 13.1 `mid(start, length)`

`mid()` 是容错型切片：

- `start` 超出字符串长度时返回空 view；
- `length < 0` 表示从 `start` 取到末尾；
- `length` 超过剩余长度时只返回剩余部分；
- 适合参数来自外部、边界不完全确定的情况。

### 13.2 `left(length)` 与 `right(length)`

`left()` 取前 `length` 个字符，`right()` 取后 `length` 个字符。

它们对以下情况做宽松处理：

- `length < 0`：返回整个 view；
- `length >= size()`：返回整个 view。

如果调用方已经证明边界合法，Qt 文档建议新代码优先使用 `first()` 或 `last()`，因为它们表达的前置条件更明确，也更适合性能敏感路径。

### 13.3 `first(n)` 与 `last(n)`

这两个函数是严格切片：

- `first(n)` 返回前 `n` 个字符；
- `last(n)` 返回后 `n` 个字符；
- `n < 0` 或 `n > size()` 是未定义行为。

适合边界已经由算法保证的内部代码。

### 13.4 `sliced(pos)` 与 `sliced(pos, n)`

`sliced()` 是严格的、不做边界修正的切片：

```cpp
auto tail = view.sliced(pos);
auto piece = view.sliced(pos, length);
```

要求：

- `pos >= 0`；
- `pos <= size()`；
- 双参数版本还要求 `n >= 0` 且 `n <= size() - pos`。

Qt 6.0 起提供。已知边界时，它比需要做容错处理的 `mid()` 更适合表达“这里一定合法”。

### 13.5 `chopped(length)` 与 `chop(length)`

- `chopped(length)` 返回去掉末尾 `length` 个字符后的新 view；
- `chop(length)` 直接缩短当前 view；
- 二者都要求 `0 <= length <= size()`。

```cpp
auto withoutSuffix = view.chopped(4);
view.chop(4);
```

`chop()` 只修改当前 view 的长度，不修改底层数据；其他指向同一数据的 view 不会被同步修改。

### 13.6 `truncate(length)`

`truncate(length)` 把当前 view 的长度设为 `length`，等价于保留开头的 `length` 个字符：

```cpp
view.truncate(5);
```

要求 `0 <= length <= size()`。它同样只修改 view 对象本身。

### 13.7 `slice(pos)` 与 `slice(pos, n)`

`slice()` 从 Qt 6.8 起提供，用于原地把当前 view 改成一个子视图：

```cpp
view.slice(prefixLength);
```

它返回 `QLatin1StringView &`，便于链式使用。边界要求与 `sliced()` 相同，越界不是“自动截断”，而是未定义行为。

## 14. 转换 API

### 14.1 `toString()`

```cpp
QString owned = view.toString();
```

把 Latin-1 字节转换为拥有数据的 `QString`。这是解除生命周期依赖的常用出口。

转换过程中，每个 Latin-1 字节被映射到相应 Unicode 码点。若底层数据含 `'\0'`，它会成为 `QString` 中的 `U+0000`，不会因为中间出现 NUL 就被截断。

### 14.2 `toUtf8()`

```cpp
QByteArray utf8 = view.toUtf8();
```

Qt 6.9 起提供。它直接返回 UTF-8 表示，比先转换到 `QString` 再调用 `QString::toUtf8()` 更高效。

这里的结果是一个拥有数据的 `QByteArray`，因此与原 view 的生命周期分离。源数据不合法的问题不会在这个 API 中“被修复”；前提仍然是源字节确实按 Latin-1 解释。

### 14.3 整数转换

Qt 6.4 起提供：

```cpp
bool ok = false;
const int value = view.toInt(&ok, 0);
```

整数转换成员包括：

- `toShort()`；
- `toUShort()`；
- `toInt()`；
- `toUInt()`；
- `toLong()`；
- `toULong()`；
- `toLongLong()`；
- `toULongLong()`。

`base` 默认是 `10`，支持 `0` 和 `2..36`：

- `base == 0` 时，`0x` 表示十六进制；
- `0b` 表示二进制；
- 以 `0` 开头时按八进制；
- 其他情况按十进制。

转换失败时返回 `0`。传入 `ok` 后，必须检查 `*ok`，否则无法区分“合法的数值 0”和“转换失败”。

Qt 文档说明，转换忽略首尾空白，并按默认 C locale 进行，不使用用户区域设置。需要本地化数字格式时使用 `QLocale`。

### 14.4 浮点转换

```cpp
bool ok = false;
const double value = view.toDouble(&ok);
```

浮点转换成员包括：

- `toFloat()`；
- `toDouble()`。

合法输入应只包含数值字符、正负号、小数点和科学计数法中的 `e` 等内容。混入单位、逗号或其他业务字符会导致失败。

失败时通常返回 `0.0`；溢出可能返回无穷大。应通过 `ok` 判断转换是否成功。

## 15. `arg()`、`trimmed()` 和 `tokenize()`

### 15.1 `arg()`

```cpp
using namespace Qt::StringLiterals;

QString message = "error: %1"_L1.arg("timeout"_L1);
```

`arg()` 会把当前 Latin-1 view 作为格式模板，按 `%N` 占位符替换参数，最终返回 `QString`。它是返回拥有数据的格式化结果，不是无分配的 view 操作。

参数按出现的占位符编号顺序处理，不是简单地把第一个参数永远替换成 `%1`、第二个参数永远替换成 `%2`。具体占位符规则遵循 `QString::arg()`。

Qt 6.9 起，参数可以包含 `QAnyStringView` 和 UTF-8 字符串相关类型；更早的 Qt 6 版本对这类参数的支持不同，跨版本库代码要检查目标 Qt 版本。

### 15.2 `trimmed()`

```cpp
QLatin1StringView clean = view.trimmed();
```

返回去除首尾空白后的新 view，不复制数据，也不修改当前对象。空白判断使用 `QChar::isSpace()` 语义，至少包括 ASCII 的：

- 空格；
- `'\t'`；
- `'\n'`；
- `'\v'`；
- `'\f'`；
- `'\r'`。

由于返回值仍然引用原数据，不能在源缓冲区失效后继续使用。

### 15.3 `tokenize()`

```cpp
using namespace Qt::StringLiterals;

auto tokens = view.tokenize(","_L1);
for (QLatin1StringView token : tokens)
    consume(token);
```

`tokenize()` 返回惰性字符串序列，实际结果类型通常应使用 `auto` 保存。不要手写 `QStringTokenizer` 的模板参数，因为这些模板参数取决于分隔符和重载推导。

它适合：

- 顺序访问分隔字段；
- 避免先构造 `QStringList`；
- 只处理实际遍历到的 token。

它不适合：

- 需要把 token 保存到源数据生命周期之外；
- 需要随机访问并反复遍历；
- 需要修改 token 内容。

## 16. 迭代器与 STL 兼容接口

### 16.1 类型别名

`QLatin1StringView` 的迭代器都是只读的：

- `value_type` 是 `const char`；
- `pointer` 和 `const_pointer` 是指向 `const char` 的指针；
- `reference` 和 `const_reference` 是 `const char &`；
- `iterator` 与 `const_iterator` 相同；
- `reverse_iterator` 与 `const_reverse_iterator` 相同；
- `difference_type` 和 `size_type` 是 `qsizetype`。

它不提供可写迭代器，因为 view 的用途是观察底层文本，而不是通过接口修改字符。

### 16.2 正向迭代

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
- `cend()`。

`begin()` 和 `cbegin()` 都指向首字符；`end()` 和 `cend()` 指向尾后位置。空 view 的 begin/end 可以相等，但不要解引用。

### 16.3 反向迭代

可用 API：

- `rbegin()`；
- `crbegin()`；
- `rend()`；
- `crend()`。

它们提供 STL 风格的只读反向迭代器。反向迭代器本身仍然不拥有任何字符。

### 16.4 `data()`、`constData()`、`constBegin()`、`constEnd()`

这些函数主要服务于不同 API 风格的兼容：

- `data()` 返回底层 `const char *`；
- `constData()` 与 `data()` 等价；
- `constBegin()` 与 `begin()` 等价；
- `constEnd()` 与 `end()` 等价。

返回的指针不应被写入，也不能被当成一定 NUL 结尾的 C 字符串。只有从 NUL 构造函数或字符串字面量得到的 view 才能在满足生命周期条件时当作 C 字符串起点使用；显式长度构造不保证 `data()[size()]` 可读或为 NUL。

## 17. `size()`、`length()`、`maxSize()` 和 `max_size()`

### 17.1 `size()` 和 `length()`

```cpp
qsizetype n1 = view.size();
qsizetype n2 = view.length();
```

二者都返回 view 中的字符数。对 Latin-1 view 来说，一个 `char` 单元对应一个 Latin-1 字节，因此长度也是字节数。

Qt 6 以前相关 API 曾受 `int` 范围限制；Qt 6 使用 `qsizetype`，适合 64 位进程中的更大数据范围。

### 17.2 `maxSize()` 和 `max_size()`

`maxSize()` 是静态函数，返回理论上可表示的最大元素数：

```cpp
const qsizetype limit = QLatin1StringView::maxSize();
```

`max_size()` 是 Qt 6.8 起提供的 STL 兼容成员，返回同一个上限：

```cpp
const qsizetype limit = view.max_size();
```

这是理论限制，不代表系统实际一定能分配这么大的连续内存。

## 18. 比较运算符的语义

类提供强比较关系，主要覆盖：

- `QLatin1StringView` 与 `QLatin1StringView`；
- `QLatin1StringView` 与 `QChar`；
- `QLatin1StringView` 与 `QStringView`；
- `QLatin1StringView` 与 `const char *`；
- `QLatin1StringView` 与 `QByteArray`；
- 以及对称的左右操作数顺序。

可用运算符包括：

```cpp
==  !=  <  <=  >  >=
```

对于 `QLatin1StringView`、`QChar` 和 `QStringView`，比较是词法比较。`const char *` 和 `QByteArray` 的相关重载受 Qt ASCII 转换配置影响，Qt 文档说明字节数组侧会按 UTF-8 语义参与这类跨类型比较；不要把这些运算符当成通用的“两个内存区逐字节比较”。

如果需要明确的 Latin-1 语义，先显式构造：

```cpp
const bool same = QLatin1StringView(leftData, leftSize)
               == QLatin1StringView(rightData, rightSize);
```

如果需要原始字节相等，应使用 `QByteArrayView` 的字节语义或显式比较 `data()` 与 `size()`。

## 19. 常见误区与排查顺序

### 19.1 把它当成拥有字符串的值类型

```cpp
QLatin1StringView saved = getView();
```

这只保存地址和长度。如果 `getView()` 的源数据是局部数组、临时 `QByteArray` 或即将重新分配的缓冲区，`saved` 可能立即悬空。

排查顺序：

1. 找到底层 `data` 的拥有者；
2. 确认拥有者是否覆盖 view 的全部使用期；
3. 检查期间是否可能发生重新分配或分离；
4. 需要长期保存时转换为 `QString` 或 `QByteArray`。

### 19.2 用 `const char *` 构造处理定长数据

如果数据没有保证 NUL 结尾：

```cpp
QLatin1StringView view(data); // 可能越过缓冲区继续读取
```

应改为：

```cpp
QLatin1StringView view(data, size);
```

### 19.3 把 UTF-8 当成 Latin-1

看到 `char *` 不等于看到 Latin-1。协议文档写明 UTF-8 时，应使用 `QUtf8StringView` 或 `QString::fromUtf8()`。

### 19.4 在空 view 上调用 `front()` 或 `back()`

`isEmpty()` 与 `isNull()` 都不保证有字符。访问首尾前先检查：

```cpp
if (!view.isEmpty()) {
    const QLatin1Char first = view.front();
}
```

### 19.5 把 `left()` 的宽松边界和 `first()` 的严格边界混用

- 外部长度不可信：优先 `mid()`、`left()`、`right()`；
- 算法已经证明边界合法：使用 `sliced()`、`first()`、`last()`；
- 不要把越界输入交给严格 API，期待它自动修正。

### 19.6 只用转换返回值判断数字解析成功

`toInt()` 失败和合法输入 `"0"` 都可能返回 `0`。始终传入 `bool *ok` 并检查。

### 19.7 认为 `data()` 一定可当作 C 字符串

显式长度构造的 view 可能没有末尾 NUL，且可能包含嵌入 NUL。传给只接受 C 字符串的第三方 API 前，需要先复制或确认其接口也接受长度。

### 19.8 为了用户界面文本使用 `_L1`

`_L1` 适合协议关键字、内部标识和固定 Latin-1 数据。用户可见字符串应使用 `tr()`、`qsTr()` 或其他本地化机制。

## 20. 版本迁移建议

### 20.1 从 `QLatin1String` 改到 `QLatin1StringView`

旧代码：

```cpp
QLatin1String key("name");
```

新代码：

```cpp
QLatin1StringView key("name");
```

这不是行为改变，而是使用 Qt 推荐的名称表达同一 view 类型。

### 20.2 从显式构造改到 `_L1`

旧代码：

```cpp
QLatin1StringView key("name");
```

Qt 6.4 及以后可以写：

```cpp
using namespace Qt::StringLiterals;
constexpr auto key = "name"_L1;
```

这会保留字面量长度，尤其适合固定比较值。

### 20.3 需要拥有结果时显式转换

旧代码若把 view 存入异步任务或对象成员，不能仅因为类型可拷贝就认为安全：

```cpp
QString owned = view.toString();
```

把这一步写出来，可以清楚地区分“借用输入”和“拥有结果”。

### 20.4 目标版本低于 Qt 6.4

以下 API 需要特别检查目标版本：

- `empty()`：Qt 6.4；
- `first()`、`last()` 无参数重载：Qt 6.4；
- `constBegin()`、`constData()`、`constEnd()`：Qt 6.4；
- `count()`：Qt 6.4；
- 数值转换：Qt 6.4；
- `std::nullptr_t` 构造：Qt 6.4；
- `_L1`：Qt 6.4；
- `compare(QUtf8StringView)`：Qt 6.5；
- `slice()`、`maxSize()`、`max_size()`：Qt 6.8；
- `toUtf8()`：Qt 6.9。

## API 速查表

下表按 Qt 6.11.1 的 `QLatin1StringView` 实际 API 列出。`QLatin1String` 作为兼容名称使用同一套接口。

### 21.1 构造函数

| API | 作用 | 边界与注意 |
| --- | --- | --- |
| `QLatin1StringView()` | 创建 null view。 | `data() == nullptr` 且 `size() == 0`。 |
| `QLatin1StringView(std::nullptr_t)` | 显式创建 null view。 | Qt 6.4 起；不拥有数据。 |
| `QLatin1StringView(const char *str)` | 引用 NUL 结尾的 Latin-1 字符串。 | 会寻找 NUL；不适合无终止符的定长缓冲区。 |
| `QLatin1StringView(const char *first, const char *last)` | 引用 `[first, last)`。 | 不扫描 NUL；两个指针必须构成有效范围。 |
| `QLatin1StringView(const char *str, qsizetype size)` | 按显式字节数建立 view。 | 保留嵌入 NUL；`size` 不能为负。 |
| `QLatin1StringView(const QByteArray &str)` | 把 `QByteArray` 的现有数据视为 Latin-1。 | 显式构造；不复制；必须保证 `QByteArray` 生命周期。 |
| `QLatin1StringView(QByteArrayView str)` | 把 byte view 的现有范围视为 Latin-1。 | Qt 6.3 起；按 view 长度，不检查 NUL。 |

### 21.2 类型别名

| API | 作用 | 边界与注意 |
| --- | --- | --- |
| `value_type` | 元素类型，`const char`。 | view 不能通过迭代器修改字符。 |
| `pointer` | `value_type *`。 | Qt 6.7 起；实际指向 `const char`。 |
| `const_pointer` | `pointer` 的兼容别名。 | Qt 6.7 起。 |
| `reference` | `value_type &`。 | 实际是 `const char &`。 |
| `const_reference` | `reference` 的兼容别名。 | 只读。 |
| `iterator` | 只读正向迭代器。 | 与 `const_iterator` 相同。 |
| `const_iterator` | 只读正向迭代器。 | 指向 `const char`。 |
| `reverse_iterator` | 只读反向迭代器。 | 与 `const_reverse_iterator` 对应。 |
| `const_reverse_iterator` | 只读反向迭代器。 | 不提供可写反向迭代器。 |
| `difference_type` | `qsizetype`。 | STL 兼容类型。 |
| `size_type` | `qsizetype`。 | Qt 6 中不是旧式 `int`。 |

### 21.3 状态、长度与底层数据

| API | 作用 | 边界与注意 |
| --- | --- | --- |
| `isNull()` | 判断 `data() == nullptr`。 | 与“是否为空”不同。 |
| `isEmpty()` | 判断 `size() == 0`。 | null view 也为空。 |
| `empty()` | `isEmpty()` 的 STL 风格名称。 | Qt 6.4 起。 |
| `size()` | 返回字符/字节数量。 | 返回 `qsizetype`；不扫描 NUL。 |
| `length()` | 返回 `size()`。 | Qt 6.4 起；兼容其他 Qt 容器。 |
| `data()` | 返回底层 `const char *`。 | 不保证 NUL 结尾；不得写入。 |
| `latin1()` | 返回底层 Latin-1 数据起点。 | 与 `data()` 类似；不转码。 |
| `constData()` | 返回底层 `const char *`。 | Qt 6.4 起；与 `data()` 等价。 |
| `maxSize()` | 返回理论最大元素数。 | 静态函数；Qt 6.8 起。 |
| `max_size()` | 返回 `maxSize()`。 | Qt 6.8 起；STL 兼容。 |

### 21.4 单字符访问

| API | 作用 | 边界与注意 |
| --- | --- | --- |
| `at(qsizetype pos)` | 读取指定位置的 `QLatin1Char`。 | `pos` 必须在 `[0, size())`；越界不应依赖。 |
| `operator[](qsizetype pos)` | 下标读取指定字符。 | 不做边界检查；越界是未定义行为。 |
| `front()` | 读取第一个字符。 | 空 view 上调用是未定义行为。 |
| `back()` | 读取最后一个字符。 | 空 view 上调用是未定义行为。 |
| `first()` | 无参数版本等价于 `front()`。 | Qt 6.4 起；空 view 上调用是未定义行为。 |
| `last()` | 无参数版本等价于 `back()`。 | Qt 6.4 起；空 view 上调用是未定义行为。 |
| `first(qsizetype n)` | 返回前 `n` 个字符的 view。 | `0 <= n <= size()`。 |
| `last(qsizetype n)` | 返回后 `n` 个字符的 view。 | `0 <= n <= size()`。 |

### 21.5 迭代器

| API | 作用 | 边界与注意 |
| --- | --- | --- |
| `begin()` | 指向首字符的只读迭代器。 | 空 view 时可与 `end()` 相等。 |
| `cbegin()` | STL 风格只读起点。 | 与 `begin()` 等价。 |
| `end()` | 指向尾后位置。 | 不得解引用。 |
| `cend()` | STL 风格只读终点。 | 与 `end()` 等价。 |
| `rbegin()` | 指向反向遍历首字符。 | 只读。 |
| `crbegin()` | const 反向起点。 | 与 `rbegin()` 等价。 |
| `rend()` | 反向尾后位置。 | 不得解引用。 |
| `crend()` | const 反向终点。 | 与 `rend()` 等价。 |
| `constBegin()` | Qt 风格 const 起点。 | Qt 6.4 起；与 `begin()` 等价。 |
| `constEnd()` | Qt 风格 const 终点。 | Qt 6.4 起；与 `end()` 等价。 |

### 21.6 比较与前后缀

| API | 作用 | 边界与注意 |
| --- | --- | --- |
| `compare(QLatin1StringView, Qt::CaseSensitivity)` | 比较两个 Latin-1 view。 | 返回值只保证负、零、正。 |
| `compare(QStringView, Qt::CaseSensitivity)` | 与 UTF-16 view 比较。 | 按文本语义比较。 |
| `compare(QUtf8StringView, Qt::CaseSensitivity)` | 与 UTF-8 view 比较。 | Qt 6.5 起；不是逐字节 Latin-1 比较。 |
| `compare(QChar)` | 与单个字符比较。 | 空 view 小于字符。 |
| `compare(QChar, Qt::CaseSensitivity)` | 大小写敏感性可配置的字符比较。 | 默认重载是大小写敏感。 |
| `startsWith(QLatin1StringView, Qt::CaseSensitivity)` | 判断 Latin-1 前缀。 | 默认大小写敏感。 |
| `startsWith(QStringView, Qt::CaseSensitivity)` | 判断 UTF-16 前缀。 | 不要求先转换为 `QString`。 |
| `startsWith(QChar)` | 判断单字符前缀。 | 空 view 返回 `false`。 |
| `startsWith(QChar, Qt::CaseSensitivity)` | 按指定大小写规则判断字符前缀。 | 适合不区分大小写的文本检查。 |
| `endsWith(QLatin1StringView, Qt::CaseSensitivity)` | 判断 Latin-1 后缀。 | 默认大小写敏感。 |
| `endsWith(QStringView, Qt::CaseSensitivity)` | 判断 UTF-16 后缀。 | 不需要创建 `QString`。 |
| `endsWith(QChar)` | 判断单字符后缀。 | 空 view 返回 `false`。 |
| `endsWith(QChar, Qt::CaseSensitivity)` | 按指定大小写规则判断字符后缀。 | 默认重载是大小写敏感。 |

### 21.7 查找与计数

| API | 作用 | 边界与注意 |
| --- | --- | --- |
| `indexOf(QLatin1StringView, qsizetype from, Qt::CaseSensitivity)` | 查找 Latin-1 子串首次出现位置。 | 找不到返回 `-1`。 |
| `indexOf(QStringView, qsizetype from, Qt::CaseSensitivity)` | 查找 UTF-16 子串。 | `from` 支持负数相对位置。 |
| `indexOf(QChar, qsizetype from)` | 查找字符。 | 默认从 `0` 开始。 |
| `indexOf(QChar, qsizetype from, Qt::CaseSensitivity)` | 按大小写规则查找字符。 | 大小写不敏感时按文本语义处理。 |
| `lastIndexOf(QLatin1StringView, Qt::CaseSensitivity)` | 查找 Latin-1 子串最后出现位置。 | Qt 6.2 起。 |
| `lastIndexOf(QLatin1StringView, qsizetype from, Qt::CaseSensitivity)` | 从指定位置向前查找 Latin-1 子串。 | 空模式与负 `from` 有特殊边界。 |
| `lastIndexOf(QStringView, Qt::CaseSensitivity)` | 查找 UTF-16 子串最后位置。 | Qt 6.2 起。 |
| `lastIndexOf(QStringView, qsizetype from, Qt::CaseSensitivity)` | 从指定位置反向查找 UTF-16 子串。 | 找不到返回 `-1`。 |
| `lastIndexOf(QChar)` | 查找字符最后出现位置。 | 默认从末尾开始。 |
| `lastIndexOf(QChar, Qt::CaseSensitivity)` | 按大小写规则反向查找字符。 | Qt 6.3 起提供该重载。 |
| `lastIndexOf(QChar, qsizetype from)` | 从指定位置反向查找字符。 | `-1` 表示最后一个字符。 |
| `lastIndexOf(QChar, qsizetype from, Qt::CaseSensitivity)` | 带大小写规则的反向字符查找。 | 找不到返回 `-1`。 |
| `contains(QLatin1StringView, Qt::CaseSensitivity)` | 判断是否包含 Latin-1 子串。 | 只需布尔结果时使用。 |
| `contains(QStringView, Qt::CaseSensitivity)` | 判断是否包含 UTF-16 子串。 | 默认大小写敏感。 |
| `contains(QChar, Qt::CaseSensitivity)` | 判断是否包含字符。 | 默认大小写敏感。 |
| `count(QLatin1StringView, Qt::CaseSensitivity)` | 统计 Latin-1 子串出现次数。 | Qt 6.4 起；可能计入重叠匹配。 |
| `count(QStringView, Qt::CaseSensitivity)` | 统计 UTF-16 子串出现次数。 | Qt 6.4 起。 |
| `count(QChar, Qt::CaseSensitivity)` | 统计字符出现次数。 | Qt 6.4 起。 |

### 21.8 切片与修改 view

| API | 作用 | 边界与注意 |
| --- | --- | --- |
| `mid(qsizetype start, qsizetype length = -1)` | 容错地取得子 view。 | 超界会调整或返回空 view。 |
| `left(qsizetype length)` | 取得前缀 view。 | 长度小于零或过大时返回整个 view。 |
| `right(qsizetype length)` | 取得后缀 view。 | 长度小于零或过大时返回整个 view。 |
| `sliced(qsizetype pos)` | 从 `pos` 取到末尾。 | Qt 6.0 起；边界必须合法。 |
| `sliced(qsizetype pos, qsizetype n)` | 取得固定长度子 view。 | Qt 6.0 起；边界必须合法。 |
| `chopped(qsizetype length)` | 返回去掉末尾长度后的 view。 | `length` 必须在 `[0, size()]`。 |
| `chop(qsizetype length)` | 原地去掉末尾长度。 | 只改当前 view，不改底层数据。 |
| `truncate(qsizetype length)` | 原地保留前 `length` 个字符。 | `length` 越界是未定义行为。 |
| `slice(qsizetype pos)` | 原地切到 `pos` 之后。 | Qt 6.8 起；严格边界。 |
| `slice(qsizetype pos, qsizetype n)` | 原地切成 `[pos, pos+n)`。 | Qt 6.8 起；严格边界。 |
| `trimmed()` | 返回去掉首尾空白的新 view。 | 不复制、不修改源数据。 |

### 21.9 转换、格式化与分词

| API | 作用 | 边界与注意 |
| --- | --- | --- |
| `toString()` | 转换为拥有数据的 `QString`。 | Qt 6.0 起；解除 view 生命周期依赖。 |
| `toUtf8()` | 转换为拥有数据的 UTF-8 `QByteArray`。 | Qt 6.9 起；比先转 `QString` 再转 UTF-8 更直接。 |
| `toShort(bool *ok, int base)` | 转换为 `short`。 | Qt 6.4 起；失败返回 `0`，检查 `ok`。 |
| `toUShort(bool *ok, int base)` | 转换为 `ushort`。 | Qt 6.4 起；支持 base `0` 和 `2..36`。 |
| `toInt(bool *ok, int base)` | 转换为 `int`。 | Qt 6.4 起；默认十进制。 |
| `toUInt(bool *ok, int base)` | 转换为 `uint`。 | Qt 6.4 起；失败需看 `ok`。 |
| `toLong(bool *ok, int base)` | 转换为 `long`。 | Qt 6.4 起；按默认 C locale。 |
| `toULong(bool *ok, int base)` | 转换为 `ulong`。 | Qt 6.4 起；首尾空白会忽略。 |
| `toLongLong(bool *ok, int base)` | 转换为 `qlonglong`。 | Qt 6.4 起；支持自动进制。 |
| `toULongLong(bool *ok, int base)` | 转换为 `qulonglong`。 | Qt 6.4 起；支持自动进制。 |
| `toFloat(bool *ok)` | 转换为 `float`。 | Qt 6.4 起；非法字符会失败。 |
| `toDouble(bool *ok)` | 转换为 `double`。 | Qt 6.4 起；溢出可能得到无穷大。 |
| `arg(Args &&...args)` | 替换 `%N` 占位符并返回 `QString`。 | 会产生拥有结果；遵循 `QString::arg()` 规则。 |
| `tokenize(Needle &&sep, Flags... flags)` | 返回按分隔符切分的惰性序列。 | Qt 6.0 起；用 `auto` 接收结果。 |

### 21.10 非成员比较与字面量

| API | 作用 | 边界与注意 |
| --- | --- | --- |
| `operator==` | 比较 `QLatin1StringView` 与 view、`QChar`、`QStringView`、`const char *` 或 `QByteArray`。 | 跨类型字节数组比较受 ASCII/UTF-8 规则影响。 |
| `operator!=` | `operator==` 的否定关系。 | 操作数顺序有对称重载。 |
| `operator<` | 词法小于比较。 | 适合排序；不要当作原始字节比较。 |
| `operator<=` | 词法小于等于比较。 | 同上。 |
| `operator>` | 词法大于比较。 | 同上。 |
| `operator>=` | 词法大于等于比较。 | 同上。 |
| `operator""_L1(const char *str, size_t size)` | 从字符串字面量创建 `QLatin1StringView`。 | Qt 6.4 起；长度不含终止 NUL。 |

## 22. 最后的选型口诀

可以用下面几条规则快速决定是否使用 `QLatin1String`：

1. **只是旧代码兼容名**：新代码写 `QLatin1StringView`。
2. **数据明确是 Latin-1**：可以使用 `QLatin1StringView`。
3. **数据明确是 UTF-8**：使用 `QUtf8StringView` 或 UTF-8 转换 API。
4. **数据是二进制**：使用 `QByteArrayView`，不要伪装成字符串。
5. **只处理固定 ASCII/Latin-1 常量**：优先使用 `_L1`。
6. **需要跨生命周期保存结果**：转换为 `QString` 或 `QByteArray`。
7. **长度来自外部数据**：使用显式长度构造，不要依赖 NUL 终止。
8. **调用 `front()`、`back()`、严格切片或下标**：先确认边界已经成立。

`QLatin1String` 的核心价值不是“另一种字符串容器”，而是把编码意图和借用生命周期明确地放进接口类型中。理解这一点后，它的所有 API 都可以归到同一个模型：**不拥有数据、按 Latin-1 解释、以 view 方式完成读取和比较，必要时显式转换为拥有型结果**。
