# Qt::totally_ordered_wrapper：给指针比较补上严格全序

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QtCompare>`  
> CMake：`Qt6::Core`  
> 自 Qt 6.8 起提供

`Qt::totally_ordered_wrapper<P>` 是一个只接受指针类型 `P` 的小包装器。它保存一个指针，但把
关系比较委托给 `std::less`、`std::less_equal`、`std::compare_three_way` 等函数对象，从而为
指针提供标准库定义的严格全序比较。

它的主要用途是避免默认成员比较或字典序比较在无关对象指针上直接调用语言级 `<` / `<=>`，因为
无关对象地址的直接关系比较不适合作为可移植的排序语义。

## 解决的问题

下面的结构如果默认生成 `<=>`，成员 `ptr` 可能被直接比较：

```cpp
template <typename T>
struct Bad {
    int id;
    T *ptr;
    auto operator<=>(const Bad &) const = default;
};
```

把指针包起来后，成员比较使用 wrapper 的关系运算符：

```cpp
template <typename T>
struct Good {
    int id;
    Qt::totally_ordered_wrapper<T *> ptr;
    auto operator<=>(const Good &) const = default;
};
```

这并不让指针指向的对象参与比较；比较的是指针值在标准库定义的总顺序中的位置。

## 它不拥有指针

wrapper 只是保存指针值，不负责释放对象，也不延长对象生命周期：

```cpp
Qt::totally_ordered_wrapper<QObject *> w(obj);
if (w)
    w->objectName();
```

`operator->` 和 `operator*` 只是访问当前指针。空指针解引用仍是错误。`operator*` 对 `void *`
这类无法解引用为对象引用的指针类型不可用。

若你需要所有权，请使用智能指针；若你需要比较对象内容，请写比较函数解引用并比较对象字段。

## 构造、访问与重置

模板参数必须是指针类型：

```cpp
Qt::totally_ordered_wrapper<int *> p(nullptr);
int value = 42;
p.reset(&value);
```

默认构造会默认初始化内部指针；对普通指针成员而言这意味着它不会自动变成安全的有效对象。
需要明确空指针时使用 `nullptr` 构造或 `reset(nullptr)`。

`get()` 返回原始指针，`reset()` 替换保存的指针，显式 `operator bool()` 用来判断是否非空。

## 比较与哈希

wrapper 支持与兼容指针、兼容 wrapper 和 `nullptr` 比较：

```cpp
Qt::totally_ordered_wrapper<Base *> a(base);
Qt::totally_ordered_wrapper<Derived *> b(derived);

bool same = (a == b);
bool before = (a < b);
auto order = Qt::compareThreeWay(a, b);
```

兼容性要求指针类型可相互转换或存在基类/派生类关系。Qt 还为 wrapper 提供 `qHash`，并在
`std::hash` 中提供对应支持，使其可用于 Qt 和 STL 哈希容器。

排序结果只对“指针身份”有意义，不代表对象内容大小，也不代表对象创建时间或地址空间布局的
业务含义。

## 与 Qt::compareThreeWay

Qt 6.8 开始，指针版 `compareThreeWay` 推荐通过 `totally_ordered_wrapper` 使用。头文件中旧的
直接指针重载被标记为弃用方向：把指针包起来，才能明确告诉比较工具你需要的是指针值全序，而非
对象内容比较。

这对字典序比较尤其重要。容器里若存的是裸指针，而你只是想得到稳定的总顺序，可以在比较层包
一层 wrapper；若你想按对象字段排序，应比较 `*ptr` 的字段，并先处理空指针。

## 常见错误

### 以为 wrapper 管理对象生命周期

它不是智能指针。对象释放后，wrapper 内部仍只是悬垂指针值。

### 解引用空指针

`operator bool()` 只能帮你检查非空，不能保证对象还活着。

### 把指针顺序当业务顺序

地址总序只适合作为技术排序键，不应被写进文件或协议当成业务含义。

### 用它替代对象内容比较

如果排序要看对象 ID、名称或时间戳，请比较那些字段，而不是指针地址。

### 忽略模板参数必须是指针

`totally_ordered_wrapper<int>` 不成立；应是 `totally_ordered_wrapper<int *>`。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `totally_ordered_wrapper<P>` | 包装一个指针类型 | `P` 必须是指针；Qt 6.8 起。 |
| `totally_ordered_wrapper()` | 默认构造 wrapper | 内部指针默认初始化；建议需要空值时显式传 `nullptr`。 |
| `totally_ordered_wrapper(nullptr)` | 构造为空指针 | 适合初始化空状态。 |
| `explicit totally_ordered_wrapper(P)` | 保存给定指针 | 不取得所有权，不延长生命周期。 |
| `get() const` | 返回原始指针 | 可用于传给需要裸指针的 API。 |
| `reset(P)` | 替换内部指针 | 不删除旧指针指向对象。 |
| `operator->() const` | 访问指向对象成员 | 指针必须非空且对象存活。 |
| `operator*() const` | 解引用指针 | 不适用于 `void *`；空或悬垂指针仍是错误。 |
| `explicit operator bool() const` | 判断指针是否非空 | 不保证对象生命周期有效。 |
| `operator==/!=` | 比较指针身份 | 可与兼容 wrapper、兼容裸指针和 `nullptr` 比较。 |
| `operator< <= > >=` | 提供指针总序关系 | 使用标准库函数对象，避免无关对象指针直接关系比较的问题。 |
| `operator<=>` | 三路比较指针顺序 | 仅在标准库三路比较可用时提供。 |
| `compareThreeWay(wrapper, wrapper/pointer/nullptr)` | 返回 `Qt::strong_ordering` | 用于 Qt 比较工具的指针全序语义。 |
| `qHash(wrapper, seed)` | Qt 哈希支持 | 哈希内部指针值。 |
| `std::hash<totally_ordered_wrapper<P>>` | STL 哈希支持 | 便于放入标准无序容器。 |
| `swap()` | 交换两个 wrapper 的指针值 | 只交换指针，不移动对象。 |

一句话总结：`totally_ordered_wrapper` 让“比较指针值”这件事显式且可定义，但它既不拥有对象，也
不替你比较对象内容。
