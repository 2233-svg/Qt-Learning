# Qt QVarLengthArray：小数组优先使用对象内预分配存储

`QVarLengthArray<T, Prealloc>` 是低层的连续可变长数组。它和 `QList` / `QVector` 一样按索引保存 `T`，但核心取舍不同：对象内部预留 `Prealloc` 个元素的位置，小数组无需堆分配；只有元素数量超过该阈值才改用堆内存。

它很适合数量通常很小、但偶尔会增长的临时数组，例如一次绘制中收集顶点、解析单条协议得到的字段、过滤函数的候选项，或性能敏感路径里的短列表。它不适合替代通用业务容器：若元素规模没有可靠的小上限、对象会长期保存大量数据，或代码更看重 Qt 容器的统一语义，`QList` 往往更直观。

```cpp
#include <QVarLengthArray>

QVarLengthArray<int, 8> samples;
samples.append(12);
samples.append(15);
samples.append(18);

for (int value : samples)
    qDebug() << value;
```

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QVarLengthArray>`  
> CMake：`Qt6::Core`  
> 类型：模板值类型，不继承 `QObject`；全部成员函数可重入。

## 它解决什么问题

普通动态数组的第一次写入常常意味着堆分配。对大量短生命周期的小数组来说，分配器开销、缓存局部性和分配碎片可能比元素操作本身更显著。`QVarLengthArray` 将一块固定容量的元素存储直接放进对象：

```cpp
QVarLengthArray<QPointF, 16> polygon;
```

前 16 个 `QPointF` 通常使用对象内存；第 17 个元素才需要可变容量的堆存储。数组之后缩小时，调用 `squeeze()` / `shrink_to_fit()` 可以尝试收缩，尺寸不超过 `Prealloc` 时会回到内嵌存储。

`Prealloc` 是**元素个数**而不是字节数，因此应该按典型元素数量选取，且必须大于 0。默认参数 `QVarLengthArrayDefaultPrealloc` 在 Qt 6.11.1 中是 256；对较大的 `T`，默认值可能让每个对象本身过大。不要不经估算就在成员变量中使用默认预分配。

## 它与 QList / QVector 的关键区别

`QVarLengthArray` 是低层连续数组，元素数据地址就是 `data()` 返回的地址；它不使用隐式共享。复制数组会复制元素，移动可能转移堆存储；任一容器修改都只影响自己。

它的内嵌缓冲区也意味着移动的细节不能想当然：

- 源数组在使用堆存储时，移动通常可接管那块存储；
- 源数组仍在内嵌缓冲区时，元素需要迁移到目标对象自己的内嵌缓冲区；
- 移动后源数组为空，但已保存的指针、引用和迭代器都不能继续使用。

连续存储给 C API 互操作带来便利：

```cpp
QVarLengthArray<char, 64> buffer;
buffer.resize(requiredSize);
fillBuffer(buffer.data(), buffer.size());
```

但 `data()` 没有附带长度，也不保证额外的 NUL 终止元素；C 字符串接口需要调用方自己预留空间并写入 `'\0'`。

## 元素类型、构造和异常边界

这是模板容器，实际可用 API 取决于 `T`：

- 所有元素类型必须是不可抛出析构的；Qt 头文件对会抛异常的析构函数直接施加静态断言。
- `QVarLengthArray(size)` 与无填充值 `resize(size)` 在扩容时要求 `T` 可以默认构造。
- 复制构造、`append(const T &)`, `assign(n, value)`、填充值构造和部分 `resize` 重载要求 `T` 可复制。
- 右值插入、移动构造和移动赋值依赖 `T` 的移动能力；移动操作是否 `noexcept` 也由 `T` 决定。
- `contains()`、查找和删除按值的 API 需要相等比较；排序比较运算需要 `<`；`qHash()` 需要 `T` 可 `qHash`。

整数尺寸参数使用 `qsizetype`。构造、调整大小、插入和删除的位置/数量必须落在有效范围；不要把外部的负数、溢出值或未经验证的协议长度直接传入。很多越界前置条件由断言检查，发布构建中仍应先校验外部输入。

## 何时会分配，何时地址失效

`capacity()` 是已分配槽位数，`size()` 是已构造元素数。`reserve(n)` 只在 `n > capacity()` 时扩容；`resize(n)` 改变元素数量；`squeeze()` 尝试将容量收缩到大小。

任何可能改变容量或移动元素的操作，都应视为会使以下对象失效：

- `data()` / `constData()` 指针；
- 所有迭代器和反向迭代器；
- 指向元素的引用；
- 指向元素的裸指针。

这包括 `append`、`emplace_back`、`insert`、`resize`、`reserve`、`squeeze`、`shrink_to_fit`、`assign`，也包括会在中间搬移元素的 `erase`、`remove`。即便某次运行没有触发扩容，也不要把“地址恰好没变”写成调用者依赖。

典型安全写法是先保存索引，再修改容器：

```cpp
const qsizetype selected = index;
points.append(newPoint);       // 可能重分配
if (selected >= 0 && selected < points.size())
    use(points[selected]);
```

不要在 `append(std::move(array[0]))` 这类表达式中移动同一数组里的元素。若扩容或元素迁移先发生，参数所引用对象的有效性和内容都不应依赖；先移到一个临时变量。

## 常用场景

### 绘制或几何计算中的短顶点数组

```cpp
QVarLengthArray<QPointF, 12> points;
points.reserve(12);

for (const Segment &segment : segments)
    points.append(segment.endPoint());

painter.drawPolyline(points.constData(), points.size());
```

这里典型顶点数不超过 12，内嵌缓冲区避免了堆分配；`constData()` 和 `size()` 则适合传给接收连续数组的 Qt API。调用绘制 API 后才允许容器重新分配，避免让对方保留无效指针。

### 用范围 API 替换整个短列表

Qt 6.6 起可以用 `assign()` 覆盖内容：

```cpp
QVarLengthArray<QString, 4> labels;
labels.assign({u"min"_s, u"mean"_s, u"max"_s});
```

若输入迭代器来自同一个数组或其元素，先建立独立副本或确认实现支持该重叠方式；对于可能重分配的容器修改，避免让输入范围依赖当前存储。

### 只读安全取值

`at()` 和 `operator[]` 要求索引有效，适合你已经证明范围正确的热路径。`value(i)` 在越界时返回默认构造的 `T`，`value(i, fallback)` 返回指定回退值，适合边界不确定的读取：

```cpp
const QString label = labels.value(row, u"unknown"_s);
```

不要用 `value()` 静默吞掉本应修复的索引错误；性能关键且范围必然正确时，`at()` 更能表达前置条件。

## API 速查表

### 类型与构造

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QVarLengthArray<T, Prealloc>` | 变长连续数组模板 | `Prealloc > 0`，是对象内预留元素数；默认 256 对大对象可能过大。 |
| `PreallocatedSize` | 编译期预分配数量 | 等于模板参数 `Prealloc`。 |
| `value_type`, `reference`, `const_reference`, `pointer`, `const_pointer` | 元素相关别名 | 分别对应 `T`、引用和指针类型。 |
| `iterator`, `const_iterator` | 正向迭代器别名 | 实际为连续元素指针；容器修改可能失效。 |
| `reverse_iterator`, `const_reverse_iterator` | 反向迭代器别名 | 反向遍历入口仍受迭代器失效规则约束。 |
| `size_type`, `difference_type` | 尺寸与差值别名 | 使用 `qsizetype` / `qptrdiff`，不要窄化到 `int`。 |
| `QVarLengthArray()` | 创建空数组 | 容量先为 `Prealloc`，尚无已构造元素。 |
| `QVarLengthArray(size)` | 创建指定大小数组 | `size >= 0`；新元素默认构造，适合确有完整可写区间时使用。 |
| `QVarLengthArray(size, value)` | 创建 `size` 个相同元素 | Qt 6.4 起；`T` 必须可复制，尺寸必须有效。 |
| `QVarLengthArray({ ... })` | 从初始化列表创建 | 元素按给定顺序复制。 |
| `QVarLengthArray(first, last)` | 从输入迭代器范围创建 | 输入必须是合法输入迭代器范围；元素类型从迭代器值构造。 |
| 复制构造 | 复制另一个数组 | 深拷贝元素，不共享数据。 |
| 移动构造 | 移动另一个数组 | Qt 6.0 起；源数组变为空，原有指针/迭代器失效。 |
| `~QVarLengthArray()` | 析构并释放元素/堆存储 | `T` 必须不可抛出析构。 |
| 复制赋值 | 用另一数组内容覆盖当前数组 | 深拷贝，旧元素被清除。 |
| 移动赋值 | 接管或迁移另一数组内容 | Qt 6.0 起；源数组随后为空。 |
| `operator=(initializer_list)` | 用初始化列表覆盖内容 | 与 `assign(list)` 相同方向，返回自身引用。 |

### 大小、存储和数据访问

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `size()` | 返回元素数 | 与 `count()`、`length()` 相同。 |
| `count()` / `length()` | `size()` 的 Qt 兼容别名 | 不要以为返回字节数。 |
| `isEmpty()` / `empty()` | 判断是否无元素 | 后者是 STL 风格别名。 |
| `capacity()` | 返回当前可容纳元素数 | 不等于 `size()`；可能大于 `Prealloc`。 |
| `reserve(size)` | 至少预留指定容量 | 仅增长容量，不改变元素数量；可能使所有地址失效。 |
| `squeeze()` / `shrink_to_fit()` | 尝试收缩容量 | 后者为 STL 别名；可能重分配，也可能回到内嵌缓冲区。 |
| `maxSize()` | 返回允许的最大元素数 | 静态函数，Qt 6.8 起有 STL 命名对应成员。 |
| `max_size()` | 返回 `maxSize()` | Qt 6.8 起，STL 风格名称。 |
| `data()` | 返回可写连续元素指针 | 指针长度是 `size()`；修改容器后可能失效。 |
| `data() const` / `constData()` | 返回只读连续元素指针 | 不附带 NUL 终止，也不能在容器修改后继续使用。 |
| `begin()` / `end()` | 取得正向可写迭代器 | `end()` 是尾后位置，不可解引用。 |
| `begin() const` / `cbegin()` | 取得正向只读迭代器 | 用于只读范围遍历。 |
| `end() const` / `cend()` | 取得只读尾后迭代器 | 与对应 `begin` 成对使用。 |
| `constBegin()` / `constEnd()` | Qt 命名的只读范围端点 | 与 `cbegin()` / `cend()` 等价。 |
| `rbegin()` / `rend()` | 取得反向可写迭代器 | `rend()` 是反向尾后位置。 |
| `rbegin() const` / `crbegin()` | 取得反向只读起点 | 遍历到 `crend()`。 |
| `rend() const` / `crend()` | 取得反向只读终点 | 不可解引用。 |

### 读取、查找和替换

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `operator[](i)` | 取得第 `i` 个元素引用 | `0 <= i < size()` 是前置条件；不做安全回退。 |
| `at(i)` | 取得第 `i` 个只读引用 | 同样要求有效索引；已知合法时比 `value()` 更直接。 |
| `first()` / `front()` | 取得首元素引用 | 数组不能为空；`front()` 为 STL 别名。 |
| `last()` / `back()` | 取得末元素引用 | 数组不能为空；`back()` 为 STL 别名。 |
| `value(i)` | 安全按索引复制读取 | 越界时返回默认构造的 `T`。 |
| `value(i, defaultValue)` | 带指定默认值的安全读取 | 越界返回 `defaultValue`，返回值是副本。 |
| `contains(value)` | 判断是否存在相等元素 | 需要可比较；线性查找。 |
| `indexOf(value, from = 0)` | 从前向后查找 | 找不到返回 `-1`；负 `from` 从尾部相对位置换算。 |
| `lastIndexOf(value, from = -1)` | 从后向前查找 | 默认从末尾；找不到返回 `-1`。 |
| `replace(i, value)` | 替换一个已有元素 | `i` 必须有效，不改变大小。 |

### 追加、插入和构造元素

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `append(const T &)` | 在末尾复制追加 | 可能重分配；不要传入依赖当前数组地址的引用。 |
| `append(T &&)` | 在末尾移动追加 | 同样可能重分配；不要写 `append(std::move(array[i]))`。 |
| `append(const T *buf, size)` | 追加连续缓冲区中的元素 | `buf` 在 `size > 0` 时必须有效，`size >= 0`；元素被复制。 |
| `push_back(const T &)` / `push_back(T &&)` | STL 风格末尾追加 | 分别是 `append` 的拷贝/移动入口。 |
| `operator<<(value)` / `operator+=(value)` | 链式追加 | 返回数组自身；仍可能重分配。 |
| `emplace_back(args...)` | 就地构造末元素 | Qt 6.3 起；返回新元素引用，该引用在后续修改后可能失效。 |
| `insert(i, value)` | 按索引插入一个元素 | `0 <= i <= size()`；中间插入会移动后续元素。 |
| `insert(i, count, value)` | 按索引插入多个副本 | `i` 与 `count` 必须有效；可能重分配。 |
| `insert(before, value)` | 在迭代器前插入一个元素 | `before` 必须来自本数组且可在 `[cbegin(), cend()]`；返回新位置迭代器。 |
| `insert(before, count, value)` | 在迭代器前插入多个副本 | 同样要求有效迭代器；返回第一个新元素。 |
| `emplace(pos, args...)` | 在迭代器位置就地构造 | Qt 6.3 起；`pos` 必须为本数组有效位置。 |
| `prepend(value)` | 在开头插入 | Qt 6.3 起已弃用且较慢；改用 `insert(cbegin(), value)`。 |

### 改变大小、赋值和删除

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `resize(size)` | 改变元素数量 | 扩大时默认构造元素，缩小时销毁尾部元素；可能重分配。 |
| `resize(size, value)` | 用给定值扩展或缩小 | Qt 6.4 起；扩大部分是 `value` 副本。 |
| `assign(count, value)` | 以多个相同值整体替换 | Qt 6.6 起；旧内容被覆盖或销毁。 |
| `assign(first, last)` | 用迭代器范围整体替换 | Qt 6.6 起；输入范围必须有效。 |
| `assign(initializer_list)` | 用初始化列表整体替换 | Qt 6.6 起。 |
| `clear()` | 删除所有元素 | `size()` 变为 0；不承诺释放容量。 |
| `removeLast()` / `pop_back()` | 删除末元素 | 数组不能为空；`pop_back()` 为 STL 别名。 |
| `remove(i, count = 1)` | 删除索引区间 | `i` 与 `count` 必须在有效范围；后续元素向前移动。 |
| `erase(pos)` | 删除迭代器所指元素 | `pos` 必须是本数组可解引用迭代器；返回下一个位置。 |
| `erase(first, last)` | 删除半开迭代器区间 | 两端必须属于本数组且区间顺序有效；返回原 `last` 所在的新位置。 |
| `removeOne(value)` | 删除首个相等元素 | Qt 6.1 起；找到并删除返回 `true`。 |
| `removeAll(value)` | 删除全部相等元素 | Qt 6.1 起；返回删除数量。 |
| `removeIf(predicate)` | 删除谓词为 true 的元素 | Qt 6.1 起；返回删除数量，谓词不得依赖已失效迭代器。 |

### 非成员算法、比较与哈希

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `erase(array, value)` | 删除全部相等元素 | Qt 6.1 起；`value` 不能引用数组内部元素，必要时先复制。 |
| `erase_if(array, predicate)` | 删除满足谓词的元素 | Qt 6.1 起；返回删除数量。 |
| `qHash(array, seed)` | 计算数组内容哈希 | `T` 必须支持 `qHash()`；元素顺序影响结果。 |
| `operator==` / `operator!=` | 比较两个数组是否相等 | 逐元素且顺序相同才相等；允许 `Prealloc` 不同。 |
| `operator<`, `>`, `<=`, `>=` | 字典序比较 | `T` 必须提供相应比较能力；这是顺序比较，不是按容量比较。 |
| `operator<=>` | 三路字典序比较 | 在支持 C++ 三路比较的构建环境下可用；结果取决于元素比较。 |

## 生命周期、线程与常见错误

`QVarLengthArray` 是值类型，不持有 QObject、文件描述符或全局注册资源；离开作用域就析构元素并释放可能使用的堆内存。它的成员函数可重入，意味着不同线程操作不同数组实例是安全的。多个线程读写同一实例仍然是 C++ 数据竞争，必须由调用方加锁或以其他同步方式保护。

常见错误包括：

- 把 `Prealloc` 当作字节数，导致每个对象远超预期；
- 长期保留 `data()`、引用或迭代器并在之后修改容器；
- 以为 `clear()` 会立即还给系统内存，需要时应考虑 `squeeze()`；
- 对空数组调用 `first()`、`last()`、`front()`、`back()` 或 `pop_back()`；
- 将 `operator[]` / `at()` 用在未验证的外部索引上；
- 使用 `append(std::move(array[i]))` 或让插入值别名指向同一容器；
- 用 `QVarLengthArray` 保存大规模、长期数据，只因为它“看起来像 QList”；
- 用同一实例跨线程读写而没有同步。

---

### 一句话总结

`QVarLengthArray` 用对象内预分配换取小数组的低分配开销；选对 `Prealloc`、把所有可能移动元素的修改当作地址失效点，并按 `T` 的构造、比较与哈希能力选择 API。
