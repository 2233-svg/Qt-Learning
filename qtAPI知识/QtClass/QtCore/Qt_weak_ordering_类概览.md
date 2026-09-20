# Qt::weak_ordering：允许等价但不要求可替换的排序结果

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QtCompare>`  
> CMake：`Qt6::Core`  
> 自 Qt 6.7 起提供

`Qt::weak_ordering` 表示所有值都能排出顺序，但“等价”不一定代表对象完全不可区分。它适合
大小写不敏感排序、按某个 key 排序、版本对象忽略构建元数据排序等场景。

例如 `"abc"` 和 `"ABC"` 在大小写不敏感比较中等价，但它们不是同一个字符串；显示、序列化或
哈希时仍可区分。

## 三种结果

| 值 | 含义 |
| --- | --- |
| `Qt::weak_ordering::less` | 左操作数排在右操作数之前。 |
| `Qt::weak_ordering::equivalent` | 两个操作数在这个排序规则下等价。 |
| `Qt::weak_ordering::greater` | 左操作数排在右操作数之后。 |

`weak_ordering` 没有 `unordered`，所以每一对值都有顺序关系；但它也没有
`strong_ordering::equal` 的“可替换性”承诺。

## 与 strong 和 partial 的关系

`strong_ordering` 可以隐式降级为 `weak_ordering`，因为强排序一定也是弱排序。
`weak_ordering` 可以降级为 `partial_ordering`，因为全都可排序的弱排序当然也是一种没有
unordered 的 partial ordering。

反过来不成立。`partial_ordering` 可能 unordered，不能安全升级成 weak；`weak_ordering` 的
等价类可能包含可区分对象，不能安全升级成 strong。

```cpp
Qt::weak_ordering weak = Qt::weak_ordering::equivalent;
Qt::partial_ordering partial = weak;
```

## 与字面量 0 比较

比较结果按三路比较惯例与字面量 0 比较：

```cpp
Qt::weak_ordering r = compareCaseInsensitive(a, b);

if (r < 0)
    ...
else if (r == 0)
    ...
else
    ...
```

辅助函数 `is_eq()`、`is_lt()` 等只是把这些判断写成函数形式，方便泛型代码兼容 std comparison
category。

## 何时返回 weak_ordering

当比较规则通过“排序 key”决定次序，而 key 相等时对象仍可能不同，返回 `weak_ordering` 很合适：

```cpp
Qt::weak_ordering compareName(QStringView a, QStringView b) noexcept
{
    const int c = a.compare(b, Qt::CaseInsensitive);
    if (c < 0)
        return Qt::weak_ordering::less;
    if (c > 0)
        return Qt::weak_ordering::greater;
    return Qt::weak_ordering::equivalent;
}
```

如果比较相等意味着两个对象在所有可观察行为上都能互换，返回 `strong_ordering` 更准确。
如果某些值无法排序，返回 `partial_ordering`。

## 与 std::weak_ordering 的互操作

在标准库提供 C++20 comparison category 时，Qt 类型可和 `std::weak_ordering` 双向转换。
`less`、`equivalent`、`greater` 按同名语义映射。

Qt 类型的意义是让 Qt 6 在不同语言标准和平台上提供一致的比较类别接口；需要调用标准库 API
时再转换即可。

## 常见错误

### 把 equivalent 当作 `operator==`

弱等价只表示排序规则下同一等价类，不表示两个对象完全相等。

### 用 weak ordering 表示 NaN 这样的不可比较情况

只要存在 unordered，就应使用 `partial_ordering`。

### 强行升级为 strong ordering

如果等价对象仍可区分，强排序的语义承诺会被破坏。

### 用内部数值代替命名常量

不要依赖 `less` 的底层值。用命名值、与 0 比较或 `is_lt()`。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `weak_ordering::less` | 左值排在右值前 | `order < 0` 为真。 |
| `weak_ordering::equivalent` | 排序规则下等价 | 不承诺对象不可区分。 |
| `weak_ordering::greater` | 左值排在右值后 | `order > 0` 为真。 |
| `weak_ordering(std::weak_ordering)` | 从标准库 weak category 构造 | 映射 less/equivalent/greater。 |
| `operator Qt::partial_ordering() const` | 降级为 partial ordering | 不产生 unordered，只是变成更宽的类别。 |
| `operator std::weak_ordering() const` | 转成标准库类型 | 需要标准库 comparison category 支持。 |
| `operator==/!=` | 比较两个 category 值 | 判断结果类别是否相同。 |
| `order < 0` / `<= 0` / `== 0` / `> 0` / `>= 0` | 与字面量 0 判断关系 | 没有 unordered，三路分支可覆盖所有情况。 |
| `is_eq(order)` | 判断等价 | 等同 `order == 0`。 |
| `is_neq(order)` | 判断非等价 | 等同 `order != 0`。 |
| `is_lt(order)` | 判断小于 | 等同 `order < 0`。 |
| `is_lteq(order)` | 判断小于或等价 | 等同 `order <= 0`。 |
| `is_gt(order)` | 判断大于 | 等同 `order > 0`。 |
| `is_gteq(order)` | 判断大于或等价 | 等同 `order >= 0`。 |

一句话总结：`weak_ordering` 排得出顺序，但“排在同一位置”不代表对象完全一样。
