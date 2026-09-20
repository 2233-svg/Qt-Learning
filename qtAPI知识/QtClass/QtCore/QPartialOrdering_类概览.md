# Qt QPartialOrdering：表达“可比较、等价或根本不可比较”的三路比较结果

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.0  
> 头文件：`#include <QPartialOrdering>`  
> 所属模块：`Qt6::Core`  
> 类型性质：无资源、可复制的轻量状态值；全部核心操作为 `constexpr noexcept`

## 1. 它解决什么问题

普通二元比较只能回答 `lhs < rhs` 或 `lhs == rhs`。一些领域还存在第三种真实状态：两个值无法放在同一排序关系中。

典型例子：

- 浮点数与 `NaN` 比较；
- 不同操作系统家族的 `QOperatingSystemVersion` 比较；
- 元对象系统尝试比较一个未注册排序规则的类型；
- 业务模型中两个对象属于互斥分类，只有同类对象才允许按等级比较。

`QPartialOrdering` 是三路比较函数的返回值，表达四种结果：

```text
less        左操作数小于右操作数
equivalent  比较规则认为两者等价
greater     左操作数大于右操作数
unordered   两者没有排序关系
```

它不是数值差值，也不是布尔值。应将它当作“比较结论”，而不是存储 `-1 / 0 / 1` 的普通整数。

## 2. 为什么是 partial ordering

“partial” 表示排序关系不覆盖所有值对。对于某些输入，既不能说左边小，也不能说右边小，也不能说两者等价。

```cpp
#include <QPartialOrdering>
#include <cmath>

QPartialOrdering compareMeasurement(double lhs, double rhs)
{
    if (std::isnan(lhs) || std::isnan(rhs))
        return QPartialOrdering::unordered;

    if (lhs < rhs)
        return QPartialOrdering::less;
    if (lhs > rhs)
        return QPartialOrdering::greater;
    return QPartialOrdering::equivalent;
}
```

```cpp
const auto result = compareMeasurement(std::nan(""), 42.0);

Q_ASSERT(result == QPartialOrdering::unordered);
Q_ASSERT(!(result < 0));
Q_ASSERT(!(result == 0));
```

若领域保证任意两值都能比较，应选择更强的 `Qt::weak_ordering` 或 `Qt::strong_ordering`。不要为了让容器排序通过而把真正的“不存在顺序”伪装为 less 或 greater。

## 3. 最重要的规则：与零字面量比较

`QPartialOrdering` 的惯用用法是和**字面量 `0`**比较：

```cpp
const QPartialOrdering result = compare(lhs, rhs);

if (result < 0) {
    // lhs 小于 rhs
} else if (result > 0) {
    // lhs 大于 rhs
} else if (result == 0) {
    // lhs 与 rhs 在该比较规则下等价
} else {
    // unordered
}
```

这里的 `0` 是比较协议的一部分，不应把它理解成可任意替换的整数状态码。头文件专门限制比较对象为 zero literal；不要依赖内部表示、强转为整数或和普通变量 `int zero = 0;` 混用。

### 3.1 四种结果的完整真值表

| 结果 | `o == 0` / `is_eq(o)` | `o != 0` / `is_neq(o)` | `o < 0` / `is_lt(o)` | `o <= 0` / `is_lteq(o)` | `o > 0` / `is_gt(o)` | `o >= 0` / `is_gteq(o)` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `less` | false | true | true | true | false | false |
| `equivalent` | true | false | false | true | false | true |
| `greater` | false | true | false | false | true | true |
| `unordered` | false | true | false | false | false | false |

`unordered` 是最容易出错的情况：

```cpp
const auto o = QPartialOrdering::unordered;

Q_ASSERT(o != 0);   // true：它不是 equivalent
Q_ASSERT(!(o < 0));
Q_ASSERT(!(o <= 0));
Q_ASSERT(!(o > 0));
Q_ASSERT(!(o >= 0));
```

因此：

- `o != 0` 的含义是“不是等价”，**包含 unordered**；
- `!(o < 0)` 不代表 `o >= 0`；
- `!(o == 0)` 不代表 `o < 0 || o > 0`；
- 若业务只接受确定的严格不等，应写 `is_lt(o) || is_gt(o)`。

### 3.2 比较结果彼此相等，与和零比较不同

下面比较的是两个**结果类别**：

```cpp
Q_ASSERT(QPartialOrdering::unordered
         == QPartialOrdering::unordered);
```

这为真，因为两个变量都表示同一种“无序”结果。但：

```cpp
Q_ASSERT(!(QPartialOrdering::unordered == 0));
```

也为真，因为无序不等价于比较对象“相等”。不要把这两种 `operator==` 混为一谈。

## 4. `equivalent` 不等于对象身份完全相同

`equivalent` 的含义是“在当前比较规则下无法区分先后”。它不承诺原始对象的每个表示、字段或身份都相同。

例如大小写不敏感的字符串比较可能把 `"Qt"` 和 `"qt"` 判为 equivalent；它们仍是不同的原始字符串。partial ordering 还允许某些值对 unordered，因此不能把“非 less 且非 greater”简单当作 equivalent。

比较函数的契约应写清：

- 哪些字段参与排序；
- 哪些不同值会被视为 equivalent；
- 哪些输入组合返回 unordered；
- 返回 unordered 时调用方应该拒绝、回退、分组还是进一步检查。

## 5. 实际使用场景

### 5.1 封装领域比较并显式处理无序

```cpp
enum class PriorityDomain { Interactive, Background };

struct JobPriority
{
    PriorityDomain domain;
    int level;
};

QPartialOrdering comparePriority(const JobPriority &lhs,
                                 const JobPriority &rhs)
{
    if (lhs.domain != rhs.domain)
        return QPartialOrdering::unordered;

    if (lhs.level < rhs.level)
        return QPartialOrdering::less;
    if (lhs.level > rhs.level)
        return QPartialOrdering::greater;
    return QPartialOrdering::equivalent;
}
```

调用端不必猜测 false 的含义：

```cpp
const auto order = comparePriority(a, b);

if (order == QPartialOrdering::less) {
    scheduleFirst(a);
} else if (order == QPartialOrdering::greater) {
    scheduleFirst(b);
} else if (order == QPartialOrdering::equivalent) {
    scheduleTie(a, b);
} else {
    Q_ASSERT(order == QPartialOrdering::unordered);
    scheduleSeparately(a, b);
}
```

`QPartialOrdering` 不是 enum，不能直接用于 `switch`。需要显式比较四个命名常量，或封装为自己的分派函数。

### 5.2 使用 `QMetaType::compare()`

`QMetaType::compare()` 返回 `QPartialOrdering`：

```cpp
QMetaType type = QMetaType::fromType<MyType>();
const QPartialOrdering order = type.compare(&left, &right);

if (order == QPartialOrdering::unordered)
    reportUnsupportedOrUnorderedValues();
```

元类型比较可能因缺少可见的排序运算符、空指针或值本身无序而得到 `Unordered`。这不是“两个值相同”，也不是“左边较小”的默认回退。

### 5.3 与 `QOperatingSystemVersion` 的部分序配合

`QOperatingSystemVersion` 的三路比较是部分序：不同 OS 家族不应按版本数字排序。可用逻辑或组合跨平台阈值：

```cpp
using OS = QOperatingSystemVersion;
const auto os = OS::current();

if (os >= OS::MacOSVentura || os >= OS(OS::IOS, 16)) {
    enableAppleModernPath();
}
```

但不能据此把所有 OS 版本放入依赖 `<` 的单一排序序列。

## 6. 与 Qt/C++ 三路比较类型互操作

Qt 6.11.1 同时提供：

- `QPartialOrdering`：Q 前缀的公开比较结果类型，许多既有 Qt API 使用它，例如 `QMetaType::compare()`；
- `Qt::partial_ordering`：Qt 的小写 comparison category；
- `std::partial_ordering`：C++20 标准库比较类别。

应优先匹配被调用 API 的签名。自己设计 API 时，在项目已经采用 `Qt::partial_ordering` 或 C++20 `<compare>` 的情况下，应保持同一比较体系，避免无意义的来回转换。

### 6.1 与 `Qt::partial_ordering`

`QPartialOrdering` 可隐式双向转换为 `Qt::partial_ordering`，并可与其做结果类别相等性比较：

```cpp
Qt::partial_ordering modern = QPartialOrdering::less;
QPartialOrdering legacy = Qt::partial_ordering::unordered;

Q_ASSERT(modern == Qt::partial_ordering::less);
Q_ASSERT(legacy == QPartialOrdering::unordered);
```

### 6.2 与 C++20 `std::partial_ordering`

当编译器和标准库定义 `__cpp_lib_three_way_comparison` 时，`QPartialOrdering` 提供与 `std::partial_ordering` 的隐式转换和相等性比较：

```cpp
#include <compare>

std::partial_ordering stdOrder = QPartialOrdering::greater;
QPartialOrdering qtOrder = std::partial_ordering::unordered;

Q_ASSERT(qtOrder == std::partial_ordering::unordered);
```

不要假设 Qt 内部用与标准库相同的整数编码；应只通过构造、转换和命名常量交互。

### 6.3 与 strong/weak ordering 的转换边界

`Qt::strong_ordering` 和 `Qt::weak_ordering` 没有 unordered 状态，转换到 `QPartialOrdering` 是信息不丢失的：结果仍为 less/equivalent/greater。反过来则不总成立，因为 `unordered` 无法安全降级为总序或弱序。

## 7. 生命周期、线程与存储

`QPartialOrdering` 只保存一个小型比较类别：

- 不分配内存；
- 不持有对象、句柄或指针；
- 可按值返回、复制、捕获和跨线程传递；
- 核心操作不抛异常；
- 不携带“为什么无序”的错误详情。

若调用方需要知道 unordered 的原因，例如“类型不支持排序”“NaN”“跨域比较”，应由比较函数返回额外错误信息、状态枚举或诊断对象。不要把原因编码进某个假定的内部数值。

## 8. 常见错误

### 8.1 把 `unordered` 当成相等

`unordered == 0` 为 false。它说明没有可用排序关系，不表示值相同。

### 8.2 用 `!= 0` 判断“严格不相等”

`unordered != 0` 为 true。需要严格 less/greater 时使用：

```cpp
const bool strictlyOrderedAndDifferent =
        is_lt(result) || is_gt(result);
```

### 8.3 以为关系运算总能二分

对 unordered，`<` 和 `>=` 可以同时为 false。不要写成：

```cpp
// 错误：else 分支可能是 unordered，而不是 lhs >= rhs。
if (result < 0)
    handleLess();
else
    handleGreaterOrEqual();
```

### 8.4 将部分序结果交给排序算法

`std::sort`、`QMap` 的键比较和有序集合通常要求严格弱序或全序。部分序的 unordered 结果不满足这类比较器的传递性/可比较性要求。先过滤、分桶或定义明确的业务 total-order tie-breaker。

### 8.5 把 `equivalent` 当成原对象 `operator==`

比较策略可能忽略大小写、时区表示或某些字段。需要对象身份或精确相等时，调用原类型的 equality API。

### 8.6 依赖内部编码或 `static_cast<int>`

类故意只支持与 zero literal 的比较；unordered 的底层取值可能随标准库和 ABI 条件变化。只用命名常量和辅助函数。

## 9. 逐项 API 说明

### 9.1 四种比较常量

`QPartialOrdering` 同时提供大小写两组拼写：

| 常量 | 等价拼写 | 含义 |
| --- | --- | --- |
| `Less` | `less` | 左操作数小于右操作数 |
| `Equivalent` | `equivalent` | 两者在比较规则下等价 |
| `Greater` | `greater` | 左操作数大于右操作数 |
| `Unordered` | `unordered` | 两者不存在排序关系 |

两组常量表示相同四个结果类别。项目内选一种风格保持一致即可；与 `Qt::partial_ordering` 和 `std::partial_ordering` 交互时，小写名称的视觉含义更接近它们。

### 9.2 与零字面量的关系运算

```cpp
o == 0;  o != 0;
o < 0;   o <= 0;
o > 0;   o >= 0;
```

这些运算检查 `o` 对“等价零”的关系，而不是将对象转换成整数：

- `== 0` 仅对 `equivalent` 为真；
- `!= 0` 对 less、greater、unordered 为真；
- `< 0` 仅对 less 为真；
- `<= 0` 对 less、equivalent 为真；
- `> 0` 仅对 greater 为真；
- `>= 0` 对 greater、equivalent 为真；
- unordered 对除 `!= 0` 外的所有上述关系运算均为 false。

零放在左侧也支持，语义方向相反，例如 `0 < o` 等价于 `o > 0`。

### 9.3 `operator==(QPartialOrdering, QPartialOrdering)` 与 `operator!=`

```cpp
constexpr bool operator==(QPartialOrdering lhs,
                          QPartialOrdering rhs) noexcept;
constexpr bool operator!=(QPartialOrdering lhs,
                          QPartialOrdering rhs) noexcept;
```

比较两个**结果类别**是否一致。

- `unordered == unordered` 为 true；
- `less != greater` 为 true；
- 这不比较产生结果的原始对象；
- 不要将它和 `result == 0` 的“原比较对象是否等价”混淆。

### 9.4 `is_eq()`、`is_neq()`、`is_lt()`、`is_lteq()`、`is_gt()`、`is_gteq()`

```cpp
bool is_eq(QPartialOrdering o) noexcept;    // Qt 6.7 起
bool is_neq(QPartialOrdering o) noexcept;
bool is_lt(QPartialOrdering o) noexcept;
bool is_lteq(QPartialOrdering o) noexcept;
bool is_gt(QPartialOrdering o) noexcept;
bool is_gteq(QPartialOrdering o) noexcept;
```

这些无成员函数分别等价于 `o == 0`、`o != 0`、`o < 0`、`o <= 0`、`o > 0`、`o >= 0`。

- 适合写泛型比较代码并对齐标准库命名；
- `is_neq()` 包含 unordered；
- 无单独公开的 `is_ordered()`；需要时用 `is_lt(o) || is_eq(o) || is_gt(o)` 判断；
- Qt 6.6 及以下没有这组 QPartialOrdering 辅助函数，使用零字面量关系运算。

### 9.5 `QPartialOrdering(Qt::partial_ordering)`

```cpp
constexpr QPartialOrdering(Qt::partial_ordering order) noexcept;
```

从 Qt 小写 partial ordering 构造。

- less/equivalent/greater/unordered 一一映射；
- 不分配资源；
- 支持隐式转换；
- 是与采用 `<QtCompare>` 的 Qt 比较 API 对接的直接方式。

### 9.6 `operator Qt::partial_ordering()`

```cpp
constexpr operator Qt::partial_ordering() const noexcept;
```

转换到 Qt 小写 partial ordering。

- 四个结果一一映射；
- unordered 保持 unordered；
- 不要通过内部数值手工转换。

### 9.7 C++20 互操作 API

当 C++20 三路比较功能可用时，头文件还提供：

```cpp
constexpr QPartialOrdering(std::partial_ordering) noexcept;
constexpr QPartialOrdering(std::weak_ordering) noexcept;
constexpr QPartialOrdering(std::strong_ordering) noexcept;
constexpr operator std::partial_ordering() const noexcept;
```

以及与 `std::partial_ordering` 的 `==` / `!=`。

- `std::partial_ordering::unordered` 可完整保留；
- strong/weak 只能提供有序的三种结果；
- 可用性取决于编译器标准库的三路比较特性宏；
- C++17 项目用 `Qt::partial_ordering` 或直接用 QPartialOrdering 即可。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 结果常量 | `Less` / `less` | 左小于右 | `o < 0` 与 `is_lt(o)` 为真 |
| 结果常量 | `Equivalent` / `equivalent` | 当前规则下等价 | 不保证原对象的所有表示相同 |
| 结果常量 | `Greater` / `greater` | 左大于右 | `o > 0` 与 `is_gt(o)` 为真 |
| 结果常量 | `Unordered` / `unordered` | 没有排序关系 | 所有有序关系运算为 false，唯 `o != 0` 为 true |
| 结果比较 | `o == 0`、`o < 0` 等 | 判断对零字面量的关系 | 用 literal `0`；别依赖底层整数编码 |
| 结果比较 | `o == QPartialOrdering::unordered` | 判断结果类别 | 与 `unordered == 0` 的语义不同 |
| 辅助函数 | `is_eq()` / `is_neq()` | 判断等价/非等价 | Qt 6.7 起；`is_neq()` 包含 unordered |
| 辅助函数 | `is_lt()` / `is_lteq()` | 判断小于/小于等于 | unordered 都为 false |
| 辅助函数 | `is_gt()` / `is_gteq()` | 判断大于/大于等于 | unordered 都为 false |
| Qt 转换 | 构造/转换 `Qt::partial_ordering` | 与 Qt 比较类别互操作 | 四种状态无损映射 |
| C++20 转换 | 构造/转换 `std::partial_ordering` | 与标准三路比较互操作 | 要求 C++20 comparison feature |
| 排序 | 作为排序比较器结果 | 表达可能无序的关系 | 不能直接满足需要严格弱序的排序容器/算法 |

## 11. 一句话总结

`QPartialOrdering` 用四个状态表达三路比较的真实结论：less、equivalent、greater 或 unordered。与 `0` 比较时要把 unordered 单独处理，尤其不能把 `!= 0` 当成“严格不相等”，也不能把部分序结果直接拿去做全序排序。
