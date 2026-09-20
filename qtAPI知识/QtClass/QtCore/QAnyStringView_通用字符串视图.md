# QAnyStringView 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAnyStringView>`  
> 模块：`Qt6::Core`  
> 定位：统一接收 Latin-1、UTF-8、UTF-16 文本的只读非拥有视图

## 它解决什么问题

`QAnyStringView` 解决的是接口层的字符串类型爆炸问题。一个函数若希望同时接收 `QString`、`QStringView`、`QByteArray`、`QUtf8StringView`、`QLatin1StringView`、C 字符串和字符串字面量，过去常需要很多重载；把参数写成 `QAnyStringView` 后，可以统一接收这些来源，而不必先复制或转换成 `QString`。

```cpp
void setTitle(QAnyStringView title);

setTitle(u"设置");                 // UTF-16 字面量
setTitle("Settings");             // char 数据按 UTF-8 理解
setTitle(QString(u"高级设置"));   // QString
setTitle(QByteArray("Network"));  // UTF-8 字节串
```

它只是“看见一段连续字符数据”的轻量值对象，不拥有字符内存，也不会延长源字符串生命周期。最适合做**函数入参**，一般按值传递：

```cpp
void setTitle(QAnyStringView title);        // 推荐
void setTitle(const QAnyStringView &title); // 没有收益，通常不需要
```

若函数必须保存文本，应该复制：

```cpp
class SettingsPage
{
public:
    void setTitle(QAnyStringView title)
    {
        m_title = title.toString(); // 持有独立的 QString 数据
    }

private:
    QString m_title;
};
```

## 它能引用哪些编码

`QAnyStringView` 可表示：

- UTF-8：`char`、`char8_t`、`QByteArray`、`QUtf8StringView`。
- UTF-16：`QChar`、`char16_t`、`ushort`、Windows 上 16 位的 `wchar_t`、`QString`、`QStringView`。
- Latin-1：`QLatin1StringView`。

普通 `char` 数据默认按 **UTF-8** 解释；若实际字节是 Latin-1，应显式包装为 `QLatin1StringView`，否则比较和转换结果可能不符合预期。Qt 6.4 起，纯 US-ASCII 的 UTF-8 字面量可在编译期按 Latin-1 优化存储；这是实现优化，不改变接口使用方式。

长度、位置、`first()`、`sliced()` 等 API 的单位是当前编码的 **code unit**，不是 Unicode 用户感知的“字符数”。例如 UTF-16 代理对占两个 code unit，UTF-8 多字节字符占二到四个 code unit。因此不要用这些索引处理字素簇、表情符号边界或用户可见字符计数。

## 生命周期：本类最容易出错的地方

视图不拥有数据，源字符串、数组或容器必须比视图活得久：

```cpp
QString source = u"文件名";
QAnyStringView view(source); // 安全，只要 source 未销毁或修改到使数据失效
```

把临时对象或单字符视图存起来会悬挂：

```cpp
QAnyStringView bad = QString(u"临时文本"); // 错误：临时 QString 已销毁
QAnyStringView alsoBad = u'9';             // 错误：单字符构造可能引用临时存储
```

但把临时值直接传给只在此次调用中使用视图的函数是安全的：

```cpp
setTitle(QString(u"临时文本")); // 安全：临时对象活到完整表达式结束
setTitle(u'9');                 // 安全：函数不保存 view 时
```

单字符构造尤其要谨慎。对 `char32_t` 等不能放进一个 UTF-16 code unit 的字符，Qt 会临时生成一个 UTF-16 序列；该临时缓冲区同样只活到完整表达式结束。需要保存时，先把数据固定在具名对象里，或直接保存 `QString`。

## 空视图与空字符串不是一回事

```cpp
QAnyStringView nullView;
QAnyStringView emptyView(u"");
```

- `nullView.isNull()` 和 `nullView.isEmpty()` 都是 `true`。
- `emptyView.isNull()` 是 `false`，但 `emptyView.isEmpty()` 是 `true`。

这种差异与 `QString` 类似：null 表示“没有底层数据”，empty 表示“有一个长度为 0 的字符串”。绝大多数显示、比较场景只需 `isEmpty()`；只有 API 需要区分“未提供”与“明确提供空值”时才检查 `isNull()`。

## 常用读取、比较和截取

```cpp
QAnyStringView name = u"report.txt";

if (!name.isEmpty() && name.back() == u't') {
    QAnyStringView base = name.chopped(4); // report
    QString owned = base.toString();       // 此时复制并取得所有权
}
```

`toString()` 返回深拷贝的 `QString`，是把短生命周期视图安全保存到成员、异步任务或容器中的标准方式。`data()` 与 `size_bytes()` 可用于只读序列化或哈希，但 `data()` 的静态类型是 `const void *`，并且调用方必须知道实际编码和源内存仍然有效。

`compare()` 和比较运算符可以跨支持的字符串类型比较；若需要忽略大小写，使用 `compare(lhs, rhs, Qt::CaseInsensitive)`。它们比较文本内容，不取得数据所有权。

## 子串 API：先检查边界

`first(n)`、`last(n)`、`chopped(n)`、`sliced(pos, n)`、`slice(pos, n)`、`truncate(n)`、`chop(n)` 都不做容错截断。`n < 0`、`pos < 0` 或范围超出 `size()` 时是未定义行为。

```cpp
QAnyStringView safePrefix(QAnyStringView text, qsizetype n)
{
    n = qBound<qsizetype>(0, n, text.size());
    return text.first(n);
}
```

选择原则很简单：

- `sliced()`、`first()`、`last()`、`chopped()`：返回一个新的视图，原视图不变。
- `slice()`、`truncate()`、`chop()`：原地修改视图的起点或长度，但绝不修改底层字符串内容。
- `mid()`、`left()`、`right()` 也在头文件中提供，带有更接近 Qt 容器的边界调整语义；需要严格前置条件时优先使用本页列出的 `sliced()` 系列并自行检查。

## `visit()`：按真实编码分派

`QAnyStringView` 为统一接口隐藏了真实编码；当性能敏感的底层逻辑要避免统一转换为 `QString` 时，可用 `visit()` 获取实际视图类型：

```cpp
void appendToLog(QAnyStringView text)
{
    text.visit([](auto concreteView) {
        processText(concreteView); // 参数是 QStringView、QUtf8StringView 或 QLatin1StringView
    });
}
```

所有可能的 lambda 实例化必须有同一个返回类型。若不同编码分支推导出不同类型，给 lambda 明确写返回类型，或在返回前统一转换。

## 何时不要用它

- 需要持久保存、跨线程投递或异步使用字符串时：用 `QString`、`QByteArray` 等拥有数据的类型。
- 调用方和实现方都明确只接受 UTF-16 时：`QStringView` 往往更清楚。
- 明确只接受 UTF-8 时：`QUtf8StringView` 更准确。
- 需要修改文本时：本类只读，应使用拥有数据的字符串类型。

本类的函数是可重入的：不同线程各自操作不同的视图实例没有问题。但如果某线程修改或销毁底层 `QString` / `QByteArray`，另一线程持有的视图仍会失效；可重入不等于底层数据自动线程安全。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `difference_type` | `std::ptrdiff_t` 的别名，供 STL 风格代码使用。 | 表示差值，不是文本长度的首选类型。 |
| 类型 | `size_type` | `qsizetype` 的别名，供 STL 风格代码使用。 | 与 `size()`、位置和长度参数配套使用。 |
| 构造 | `QAnyStringView()`、`QAnyStringView(std::nullptr_t)` | 构造 null 视图。 | `isNull()` 与 `isEmpty()` 都为真。 |
| 构造 | `QAnyStringView(const Char &ch)` | 引用一个单字符的文本表示。 | 仅适合立即传参；保存该视图可能引用完整表达式结束后已销毁的临时数据。 |
| 构造 | `QAnyStringView(const Char (&string)[N])` | 从以零结尾的字符数组或字面量创建视图。 | 到首个 `Char(0)` 为止；若要包含数组内嵌的零值，使用 `fromArray()`。 |
| 构造 | `QAnyStringView(const Char *str)` | 从零结尾字符指针创建视图。 | 会扫描寻找零终止符；指针必须有效且在视图存活期间不失效。 |
| 构造 | `QAnyStringView(const Container &str)` | 从兼容的连续字符串容器创建视图。 | 不复制容器数据；容器重分配、修改或销毁都会使视图失效。 |
| 构造 | `QAnyStringView(const QByteArray &str)` | 将 `QByteArray` 作为 UTF-8 数据引用。 | 不是 Latin-1 解释；需要 Latin-1 时显式使用 `QLatin1StringView`。 |
| 构造 | `QAnyStringView(const QString &str)` | 将 `QString` 的 UTF-16 数据作为视图引用。 | 不增加 `QString` 引用计数，也不延长其生命周期。 |
| 构造 | `QAnyStringView(const Char *first, const Char *last)` | 用首尾指针范围创建视图。 | 两指针必须来自同一连续范围，且 `last >= first`。 |
| 构造 | `QAnyStringView(const Char *str, qsizetype len)` | 用指针和明确长度创建视图。 | 不扫描零终止符；`str` 与 `len` 必须匹配有效内存范围。 |
| 格式化 | `arg(Args &&... args) const` | 按 `QString::arg()` 风格替换占位符并返回新的 `QString`。 | Qt 6.9 引入；这是创建拥有数据的结果，不再只是 view。 |
| 访问 | `front() const`、`back() const` | 返回首个或最后一个 UTF-16 `QChar`。 | 空视图上调用无效；返回单位不是完整 Unicode 字素。 |
| 查询 | `data() const` | 返回底层数据地址。 | 类型为 `const void *`；必须知道实际编码，并确保源数据继续有效。 |
| 查询 | `size() const`、`length() const` | 返回 code unit 数；`length()` 等同于 `size()`。 | UTF-8 多字节字符和 UTF-16 代理对会占多个单位。 |
| 查询 | `size_bytes() const` | 返回底层文本占用的字节数。 | 可与 `data()` 用于哈希或序列化，不代表用户可见字符数量。 |
| 查询 | `empty() const`、`isEmpty() const` | 判断长度是否为 0。 | 两者语义相同；不区分 null 和显式空字符串。 |
| 查询 | `isNull() const` | 判断是否没有底层数据。 | 仅在业务需要区分 null 与 empty 时使用。 |
| 查询 | `max_size() const` | 返回该编码下理论可表示的最大元素数。 | Qt 6.8 引入；不同编码视图的结果可能不同，实际内存限制通常更早到达。 |
| 截取 | `first(qsizetype n)`、`last(qsizetype n)` | 返回前或后 `n` 个 code unit 的新视图。 | Qt 6.5 引入；`n` 越界或为负是未定义行为。 |
| 截取 | `sliced(qsizetype pos)` | 返回从 `pos` 到末尾的新视图。 | Qt 6.5 引入；要求 `0 <= pos <= size()`。 |
| 截取 | `sliced(qsizetype pos, qsizetype n)` | 返回从 `pos` 起长为 `n` 的新视图。 | Qt 6.5 引入；必须满足 `pos + n <= size()`。 |
| 截取 | `chopped(qsizetype n)` | 返回去掉末尾 `n` 个 code unit 的新视图。 | Qt 6.5 引入；不会修改原对象，`n` 必须在合法范围内。 |
| 原地截取 | `slice(qsizetype pos)` | 将当前视图改为从 `pos` 到末尾。 | Qt 6.8 引入；只改 view 元数据，不改源字符串。 |
| 原地截取 | `slice(qsizetype pos, qsizetype n)` | 将当前视图改为指定子范围。 | Qt 6.8 引入；范围不合法是未定义行为。 |
| 原地截取 | `truncate(qsizetype n)` | 将当前视图长度截为 `n`。 | Qt 6.5 引入；等价于保留 `first(n)`，不修改底层字符。 |
| 原地截取 | `chop(qsizetype n)` | 从当前视图末尾去掉 `n` 个 code unit。 | Qt 6.5 引入；不是删除源字符串内容。 |
| 转换 | `toString() const` | 将视图深拷贝为 `QString`。 | 保存、跨线程或异步使用前的安全转换；仅当 view 为 null 时结果也为 null。 |
| 静态比较 | `compare(lhs, rhs, cs)` | 按大小写敏感策略比较两段文本。 | 返回值小于、等于、大于 0 分别表示小于、相等、大于；默认大小写敏感。 |
| 静态构造 | `fromArray(const Char (&string)[Size])` | 从整个数组创建视图，保留数组长度内的内嵌零值。 | 与数组构造不同，不在首个零字符处停止；数组仍须持续有效。 |
| 编码分派 | `visit(Visitor &&v) const` | 以真实编码的具体视图类型调用访问器。 | 所有可能实例化分支必须返回同一类型；适合避免不必要的文本转换。 |
| 比较运算符 | `==`、`!=`、`<`、`<=`、`>`、`>=` | 比较两个 `QAnyStringView` 的文本内容。 | 可与支持类型强比较；不取得所有权，编码差异可能影响性能。 |
| 调试输出 | `operator<<(QDebug, QAnyStringView)` | 将视图写入调试流。 | Qt 6.7 引入；启用带引号字符串输出时，调试信息可能标示实际编码。 |

## 一句话总结

`QAnyStringView` 是用于函数边界的通用只读字符串借用类型：它消除多编码重载，却不拥有任何字符数据。把它按值传入、立即消费；需要保存时立即 `toString()`。
