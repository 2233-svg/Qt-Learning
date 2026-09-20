# Qt::strong_ordering：等价即不可区分的三路比较结果

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QtCompare>`  
> CMake：`Qt6::Core`  
> 自 Qt 6.7 起提供

`Qt::strong_ordering` 表示最强的三路比较类别：任意两值都有确定顺序，并且比较为相等/等价的
值在比较所关心的语义上不可区分。整数、枚举、规范化后的 ID、字节序列字典序通常属于这类。

它适合实现 `<=>`、`compareThreeWay()`、容器字典序比较和需要和 C++20 comparison category
互操作的 Qt 代码。

## 四个命名值

| 值 | 含义 |
| --- | --- |
| `Qt::strong_ordering::less` | 左操作数小于右操作数。 |
| `Qt::strong_ordering::equal` | 两个操作数相等。 |
| `Qt::strong_ordering::equivalent` | 与 `equal` 同义；表示等价且可替换。 |
| `Qt::strong_ordering::greater` | 左操作数大于右操作数。 |

`strong_ordering` 没有 `unordered`，也不会把“按 key 等价但对象仍不同”的情况表达为强等价。
如果等价类里能包含可区分对象，应使用 `weak_ordering`。

## 使用方式

比较类别通常与字面量 0 比较：

```cpp
Qt::strong_ordering r = Qt::compareThreeWay(a, b);

if (r < 0) {
    // a < b
} else if (r == 0) {
    // a == b
} else {
    // a > b
}
```

辅助函数 `is_eq()`、`is_lt()`、`is_gteq()` 等只是把这些判断包装成函数，便于模板代码同时支持
Qt 和 std 的比较类别。

## 降级转换

强排序可以安全转换为弱排序和偏序：

```cpp
Qt::strong_ordering s = Qt::strong_ordering::less;
Qt::weak_ordering w = s;
Qt::partial_ordering p = s;
```

这两个方向都是“丢失承诺”：从 strong 到 weak 会丢掉可替换性语义，从 strong 到 partial 会进入
一个更宽的类型。反向升级不安全，也没有通用转换。

## 与 std::strong_ordering 的互操作

标准库支持 C++20 comparison category 时，`std::strong_ordering` 可转换为 Qt 类型，Qt 类型也
可转回标准库类型。四个语义值按同义映射。

这让 Qt API 可以在未完全依赖 C++20 标准库实现的环境中保持自己的比较类别，同时在需要时参与
标准库三路比较代码。

## 何时选择 strong_ordering

选择它的判断标准不是“有没有 `<`”，而是“等价是否足以替代”：

- 整数 1 与 1：strong。
- 枚举同一枚举值：strong。
- 大小写不敏感字符串 `"abc"` 与 `"ABC"`：通常是 weak，不是 strong。
- 浮点 NaN 与任何值：partial。

若把 weak/partial 情况强行包装成 strong，排序算法可能还能运行，但类型语义会误导调用方。

## 常见错误

### 把 `equal` 和 `equivalent` 当成两个不同结果

在 strong ordering 中它们同义。保留两个名称是为了对应标准库表达。

### 用 strong ordering 表达大小写不敏感排序

大小写不敏感等价不代表原字符串相等。应返回 weak ordering。

### 忽略降级后的语义变化

转换为 `weak_ordering` 或 `partial_ordering` 后，调用方只能依赖目标类型承诺的语义。

### 保存底层数值

使用命名常量和比较操作；底层表示不是公共协议。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `strong_ordering::less` | 左值小于右值 | `order < 0` 为真。 |
| `strong_ordering::equal` | 两值相等 | 与 `equivalent` 同义。 |
| `strong_ordering::equivalent` | 两值等价且可替换 | 与 `equal` 同义，表达标准比较类别语义。 |
| `strong_ordering::greater` | 左值大于右值 | `order > 0` 为真。 |
| `strong_ordering(std::strong_ordering)` | 从标准库 strong category 构造 | 映射 less/equal/equivalent/greater。 |
| `operator Qt::weak_ordering() const` | 降级为弱排序类别 | 保留顺序，丢掉 strong 的可替换性承诺。 |
| `operator Qt::partial_ordering() const` | 降级为偏序类别 | 不会产生 unordered，只是类型更宽。 |
| `operator std::strong_ordering() const` | 转成标准库 strong category | 需要标准库 comparison category 支持。 |
| `operator==/!=` | 比较两个 category 值 | 用于判断是否为同一结果类别。 |
| `order < 0` / `<= 0` / `== 0` / `> 0` / `>= 0` | 与字面量 0 判断关系 | 三路分支可覆盖全部结果。 |
| `is_eq(order)` | 判断相等/等价 | 等同 `order == 0`。 |
| `is_neq(order)` | 判断非等价 | 等同 `order != 0`。 |
| `is_lt(order)` | 判断小于 | 等同 `order < 0`。 |
| `is_lteq(order)` | 判断小于或等价 | 等同 `order <= 0`。 |
| `is_gt(order)` | 判断大于 | 等同 `order > 0`。 |
| `is_gteq(order)` | 判断大于或等价 | 等同 `order >= 0`。 |

一句话总结：`strong_ordering` 是最有承诺的比较结果；只有等价对象真的可互换时才应返回它。
