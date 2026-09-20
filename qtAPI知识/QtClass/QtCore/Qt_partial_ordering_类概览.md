# Qt::partial_ordering：允许 unordered 的三路比较结果

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QtCompare>`  
> CMake：`Qt6::Core`  
> 自 Qt 6.7 起提供

`Qt::partial_ordering` 表示三路比较的结果，但承认“有些值彼此无法排序”。最常见的例子是浮点
数里的 NaN：它既不小于、不等于、也不大于另一个数。

它适合比较函数无法保证所有值都有全序关系的类型，例如浮点数、带无效状态的数学对象、集合的
包含关系等。

```cpp
Qt::partial_ordering r = Qt::compareThreeWay(lhs, rhs);

if (r < 0) {
    // lhs 小于 rhs
} else if (r == 0) {
    // lhs 与 rhs 等价
} else if (r > 0) {
    // lhs 大于 rhs
} else {
    // unordered：没有可用排序关系
}
```

## 四种结果

| 值 | 含义 |
| --- | --- |
| `Qt::partial_ordering::less` | 左操作数小于右操作数。 |
| `Qt::partial_ordering::equivalent` | 两个操作数等价。 |
| `Qt::partial_ordering::greater` | 左操作数大于右操作数。 |
| `Qt::partial_ordering::unordered` | 两个操作数没有排序关系。 |

和 `strong_ordering` / `weak_ordering` 相比，它多了 `unordered`。因此只有在确实能处理无序结果时，
才应把比较函数设计为返回 `partial_ordering`。

## 与字面量 0 比较

比较类别的惯用写法是与字面量 `0` 比较：

```cpp
if (order < 0) { ... }
if (is_gteq(order)) { ... }
```

`unordered` 对 `< 0`、`<= 0`、`== 0`、`> 0`、`>= 0` 都不会表现为有序关系。要专门检测无序，
可以与 `Qt::partial_ordering::unordered` 比较，或在小于、等于、大于分支都未命中时进入无序分支。
`is_neq(order)` 等价于 `order != 0`，会把 `unordered` 视为“不是等价”。

不要把 `partial_ordering` 当成整数保存或序列化。内部表示是 Qt 实现细节，公共语义是这些命名值
和比较操作。

## 与 std::partial_ordering 的互操作

在标准库提供 C++20 comparison category 时，可以在 `std::partial_ordering` 与
`Qt::partial_ordering` 之间转换：

```cpp
std::partial_ordering s = std::partial_ordering::unordered;
Qt::partial_ordering q = s;
std::partial_ordering back = q;
```

映射关系一一对应：`less`、`equivalent`、`greater`、`unordered` 保持同义。

## 设计比较函数时的边界

如果返回 `partial_ordering`，调用方必须准备处理 unordered。若业务强行把 unordered 排到最后
或最前，那其实是在定义一种全序策略，应在比较函数里显式实现并返回 `weak_ordering` 或
`strong_ordering`。

浮点比较是典型 partial ordering：

```cpp
Qt::partial_ordering cmp(double a, double b) noexcept
{
    return Qt::compareThreeWay(a, b);
}
```

对容器排序算法而言，partial ordering 往往不够。排序通常需要严格弱序比较器；如果比较结果
可能 unordered，应先定义清楚 unordered 的排序位置。

## 常见错误

### 忽略 unordered 分支

只写 `<`、`==`、`>` 三个分支会让 unordered 静默落空。应显式处理。

### 把 unordered 当 greater

无序不是“更大”，也不是“更小”。把它放到某个位置是应用策略，不是比较类别本身的语义。

### 返回 partial_ordering 后交给普通排序

普通排序需要能决定元素次序。先把 partial result 转成明确的排序谓词。

### 把 `equivalent` 理解为对象完全相同

它只表示比较函数认为等价。对象身份、内部表示和业务字段可能仍不同。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `partial_ordering::less` | 左值小于右值 | `order < 0` 为真。 |
| `partial_ordering::equivalent` | 两值等价 | `order == 0` 为真。 |
| `partial_ordering::greater` | 左值大于右值 | `order > 0` 为真。 |
| `partial_ordering::unordered` | 两值不可排序 | 不是小于、等于或大于；需单独处理。 |
| `partial_ordering(std::partial_ordering)` | 从标准库 partial category 构造 | 映射四个同名语义值。 |
| `operator std::partial_ordering() const` | 转回标准库类型 | 需要标准库 comparison category 支持。 |
| `operator==/!=` | 比较两个 category 值是否同一结果 | 可直接判断是否为 `unordered` 等命名值。 |
| `order < 0` / `<= 0` / `== 0` / `> 0` / `>= 0` | 与字面量 0 做关系判断 | unordered 不满足有序关系；`!= 0` 对 unordered 为真。 |
| `is_eq(order)` | 判断 `order == 0` | 兼容 std comparison category 辅助函数。 |
| `is_neq(order)` | 判断 `order != 0` | unordered 会返回 true。 |
| `is_lt(order)` | 判断 `order < 0` | unordered 返回 false。 |
| `is_lteq(order)` | 判断 `order <= 0` | unordered 返回 false。 |
| `is_gt(order)` | 判断 `order > 0` | unordered 返回 false。 |
| `is_gteq(order)` | 判断 `order >= 0` | unordered 返回 false。 |

一句话总结：`partial_ordering` 的重点不是三路比较，而是第四种结果：无法比较。
