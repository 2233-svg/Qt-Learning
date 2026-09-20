# QSpan：连续数据的一段非拥有视图

> Qt 6.11.1 | `#include <QSpan>` | 模块：`Qt6::Core` | 模板：`QSpan<T, E = std::size_t(-1)>`

`QSpan` 用一个指针和长度引用一段连续内存。它不分配内存、不复制元素、不拥有元素；数组、`QList`、`QVector`、`std::vector`、`std::array` 等连续数据都可以借给它看。

它解决的是接口设计问题：函数只需要“连续的一段元素”时，没有必要强迫调用者把数据转换成特定容器。

```cpp
void writeSamples(QSpan<const float> samples);

QVector<float> a = loadSamples();
std::array<float, 4> b = { 1, 2, 3, 4 };
writeSamples(a);
writeSamples(b);
```

## 什么时候该用它

- 图像、音频、协议帧、数值算法需要传递连续缓冲区的一段。
- API 只读输入时用 `QSpan<const T>`，既接受多种容器，也明确不修改元素。
- 需要零拷贝子区间时用 `first()`、`last()`、`subspan()` 或 `sliced()`。

不适合用 `QSpan` 来保存“以后再用”的数据所有权。它只是借用关系，不能替代 `QByteArray`、`QString`、`QList` 或 `std::vector`。

## 最小示例

```cpp
#include <QSpan>
#include <QVector>

int sum(QSpan<const int> values)
{
    int result = 0;
    for (int value : values)
        result += value;
    return result;
}

QVector<int> values = { 3, 5, 8 };
const int total = sum(values); // 16，无元素复制
```

## 生命周期：最重要的契约

`QSpan` 只保存地址和长度。被引用的数据一旦析构、重分配或缩短到不再覆盖这段范围，span 就悬空。

```cpp
QSpan<const int> makeBadSpan()
{
    QVector<int> values = { 1, 2, 3 };
    return values; // 错误：返回后 values 已销毁
}

QVector<int> values = { 1, 2, 3 };
QSpan<int> view = values;
values.append(4); // 可能重分配；此前的 view 不应再使用
```

Qt 允许从右值拥有容器构造 `QSpan`，这是为了兼容接受容器的旧接口；它不意味着临时容器会延长生命周期。不要把由临时对象构造的 span 保存到下一条语句以后。

`QSpan` 应按值传递。它通常只有指针和长度，`const QSpan<T>` 既不能延长底层数据寿命，也不会把元素变成只读；真正的只读类型是 `QSpan<const T>`。

## 可变、只读与固定长度

```cpp
int data[] = { 0, 1, 2 };
QSpan<int> writable = data;
QSpan<const int> readable = data;

writable[0] = 42;       // 修改 data
// readable[0] = 42;    // 编译错误

QSpan<int, 3> exactlyThree = data; // 长度是类型的一部分
```

- 可变长度 span 的大小在运行时记录。
- 固定长度 span 的 `E` 是类型的一部分，`extent` 可在编译期获知。
- 固定长度 span 可以隐式转换为可变长度 span；反向转换要求长度匹配。
- 对 `const QSpan<int>` 调用 `front()` 或 `begin()` 仍可修改元素，这是浅层 const 的设计。若要限制写入，使用 `QSpan<const int>` 或 `cbegin()` / `cend()`。

## 边界与并发

`operator[]`、`front()`、`back()`、`first()`、`last()`、`subspan()`、`slice()`、`chop()` 都要求索引和长度在范围内。违约是未定义行为，不能把调试构建中的断言当作运行时错误处理。

`QSpan` 本身没有同步能力。不同线程可以各自持有 span 副本，但必须由外部保证底层内存仍有效、没有数据竞争，并且不存在会导致缓冲区地址变化的并发重分配。

## 版本相关能力

- `as_bytes()` 与 `as_writable_bytes()`：Qt 6.8 起提供。
- `chop()`、`chopped()`、`slice()`：Qt 6.9 起提供，且修改自身的 `slice()`、`chop()` 仅适用于可变长度 span。

## 常见错误

1. **把 span 当容器。** `QSpan` 不保管任何元素，离开原容器的生命周期就失效。
2. **用 `const QSpan<T>` 表示只读。** 它只让 span 对象本身不可重新指向；元素依然可写。
3. **忘记容器扩容会使视图悬空。** 修改拥有容器后，重新获取 span。
4. **把字节视图当序列化许可。** `as_writable_bytes()` 只提供对象表示的字节访问；仍要遵守对象有效性、对齐、端序与协议格式规则。
5. **传递负数或越界的 `qsizetype`。** `QSpan` 的大小和索引是有符号的，先验证外部输入。

## API 速查表

| 类别 | API | 语义 | 使用边界 |
| --- | --- | --- | --- |
| 类型参数 | `T` | 元素类型；可写性由 `T` 是否为 `const` 决定。 | 只读接口使用 `QSpan<const T>`。 |
| 类型参数 | `E` | 固定长度，默认动态长度。 | 固定 span 的长度必须与构造来源匹配。 |
| 常量 | `extent` | 第二模板参数 `E`，类型为 `std::size_t`。 | 其他大小与索引使用 `qsizetype`。 |
| 构造 | `QSpan()` | 创建空 span；固定长度版本仅在长度为 0 时可空构造。 | 空 span 没有可访问元素。 |
| 构造 | `QSpan(It first, qsizetype count)` / `QSpan(It first, It last)` | 从兼容随机访问迭代器引用一段元素。 | 迭代器范围必须连续、有效且长度正确。 |
| 构造 | `QSpan(T (&)[N])` / `QSpan(std::array)` | 从 C 数组或 `std::array` 借用数据。 | 原数组或 array 必须存活。 |
| 构造 | `QSpan(Range &&)` | 从兼容连续范围借用数据。 | 右值范围只可在完整表达式内即时使用。 |
| 构造 | `QSpan(QSpan)` / `QSpan(std::span)` | 复制视图或与 `std::span` 互转。 | 复制的是借用，不复制元素。 |
| 构造 | `QSpan(std::initializer_list)` | 仅对 `QSpan<const T>` 参与重载。 | 不要保存指向 initializer list 临时数组的结果。 |
| 观察 | `size()` / `size_bytes()` | 返回元素数或字节数。 | `size_bytes()` 是 `size() * sizeof(T)`。 |
| 观察 | `empty()` / `isEmpty()` | 测试是否没有元素。 | 调用 `front()`、`back()` 前必须为假。 |
| 数据 | `data()` | 返回首元素指针，空 span 可为 `nullptr`。 | 指针不拥有数据，也不保证比底层容器更长寿。 |
| 元素 | `operator[]` | 返回指定元素引用。 | 要求 `0 <= idx < size()`，越界未定义。 |
| 元素 | `front()` / `back()` | 返回首/尾元素引用。 | 空 span 上调用未定义。 |
| 正向迭代 | `begin()` / `end()` | 取得可由 `T` 决定写权限的迭代器。 | `const QSpan<T>` 仍可能给出可写迭代器。 |
| 只读迭代 | `cbegin()` / `cend()` | 返回 const iterator。 | 适合在可写 span 上强制只读遍历。 |
| 反向迭代 | `rbegin()` / `rend()` / `crbegin()` / `crend()` | 从末尾向前遍历。 | 与普通迭代器一样依赖底层内存稳定。 |
| 前段 | `first<Count>()` / `first(n)` | 返回前 `Count` 或 `n` 个元素的子视图。 | 必须不超过当前大小。 |
| 后段 | `last<Count>()` / `last(n)` | 返回后 `Count` 或 `n` 个元素的子视图。 | 必须不超过当前大小。 |
| 子段 | `subspan<Offset, Count>()` / `subspan(pos, n)` | 返回中间子视图。 | `pos`、`n` 非负，且 `pos + n <= size()`。 |
| Qt 命名 | `sliced(pos, n)` | 与运行时参数的 `subspan()` 等价。 | 返回动态长度子视图。 |
| 尾部裁剪 | `chopped(n)` | 返回去掉末尾 `n` 个元素的新视图。 | Qt 6.9 起；`n` 必须在范围内。 |
| 修改自身 | `slice(pos, n)` / `chop(n)` | 让当前 span 改为子段或去掉末尾。 | Qt 6.9 起；只适用于动态长度 span。 |
| 赋值 | `operator=(QSpan)` | 改变本 span 的指针和长度。 | 不复制元素，也不延长底层生命周期。 |
| 字节只读视图 | `as_bytes(QSpan)` | 返回 `QSpan<const std::byte>`。 | Qt 6.8 起；只访问对象表示。 |
| 字节可写视图 | `as_writable_bytes(QSpan)` | 返回 `QSpan<std::byte>`。 | Qt 6.8 起，且 `T` 不能是 const。 |

`QSpan` 的使用原则可以压缩成一句话：让函数拿到恰好需要的数据范围，但把“谁拥有数据、数据何时失效”始终留在调用方清楚表达。
