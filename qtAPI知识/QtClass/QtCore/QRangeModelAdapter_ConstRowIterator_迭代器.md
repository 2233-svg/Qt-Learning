# QRangeModelAdapter::ConstRowIterator：按模型行只读遍历列表、表格和树

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.11  
> 状态：Preliminary  
> 所属头文件：`#include <QRangeModelAdapter>`

`QRangeModelAdapter::ConstRowIterator` 是 adapter 的只读行迭代器，建模 `std::random_access_iterator`。它把“按行遍历”统一到列表、表格和树三种模型形状，但解引用结果会随模型形状改变：

- 列表：得到当前项目的 const 数据；
- 表格：得到当前行的 `ConstRowReference`；
- 树：得到当前父节点下某一行的 `ConstRowReference`。

它解决的是遍历现有模型范围时既保留类型信息，又不打开绕过模型通知的写入口。

## 基本使用

```cpp
const auto &readOnly = adapter;

for (const auto &rowOrItem : readOnly) {
    // 列表中是项目数据；
    // 表格或树中是只读行引用。
}
```

显式使用时：

```cpp
for (auto it = adapter.cbegin(); it != adapter.cend(); ++it) {
    const auto itemOrRow = *it;
    // 只读处理
}
```

对树的 `children()` 返回的子 adapter，`cbegin()` / `cend()` 遍历的是该子树根下的直接子行，而不是整个树的深度优先序列。

## 不同模型形状下的解引用

### 列表

列表 adapter 的 `*it` 是项目的 const 数据。若元素是值类型，可直接读取；若元素是指针，得到的是指向 const 项目的视图，不能借此修改项目。

```cpp
for (const auto &book : std::as_const(bookAdapter)) {
    qDebug() << book->title(); // const 成员访问
}
```

### 表格和树

表格、树的 `*it` 是 `ConstRowReference`。它可像一行只读范围一样遍历列：

```cpp
for (const auto &row : std::as_const(tableAdapter)) {
    for (const auto &cell : row) {
        qDebug() << cell;
    }
}
```

这个包装保证即使底层行是 tuple、gadget 或非标准范围，也能用统一列迭代器访问。它不是可修改的底层行引用。

## 随机访问的边界

支持递增、递减、偏移、下标、距离和三路比较：

```cpp
auto first = adapter.cbegin();
auto third = first + 2;
const auto &value = third[0];
```

这些操作的序列语义只对同一个 adapter 根范围成立。树的不同 `children()` adapter 表示不同父节点下的行序列，即使行号相同，也不要把它们混合计算距离。实现的差值操作只按行号相减，调用方必须自行遵守“同一序列”的标准迭代器前置条件。

不能解引用 `cend()`，不能移动到 begin 之前或 end 之后。`operator->()` 也只提供 const 访问。

## 生命周期与线程

迭代器依赖 adapter、其共享的 model 和当前根索引。插入、删除、移动行列，`assign()`、模型 reset、adapter 销毁后，已有迭代器和行引用都不应继续使用。

const 只限制这条 API 的写入能力，不代表模型可从多个线程无同步读取。模型、视图与所有 adapter 操作仍应在 model 所属线程进行。

## 常见错误

1. 假定 `*it` 总是一个项目。表格和树中它是行包装器。
2. 对 const 行引用或其 `operator->()` 调用非 const 成员。
3. 把来自不同树父节点的 row iterator 做距离计算。
4. 结构修改后继续用循环开始前缓存的 `cend()`。
5. 误把 `cbegin()` 当作全树遍历入口，它只遍历当前 adapter 根的直接行。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `iterator_category` | 标记为 `std::random_access_iterator_tag`。 | 随机访问只在同一 adapter 根范围内有意义。 |
| `difference_type` | 行偏移和距离类型，为 `int`。 | 不对不同树子范围的迭代器求差。 |
| `value_type` / `reference` | 列表为 const 项目数据，表格/树为 `ConstRowReference`。 | 先按模型形状确定解引用类型。 |
| `pointer` | 指向或包装 const 解引用结果。 | `operator->()` 不提供写能力。 |
| `operator*()` | 读取当前行或项目。 | 不可解引用 end 或失效 iterator。 |
| `operator->()` | 访问项目或行的 const 成员。 | 不可绕过 adapter 修改底层数据。 |
| `operator[](n)` | 读取偏移 `n` 的行或项目。 | 目标须在当前根范围内有效。 |
| `++` / `--` | 前后移动一行。 | 不可越过 begin/end。 |
| `+`, `-`, `+=`, `-=` | 按行偏移。 | 只在同一行序列范围中使用。 |
| `lhs - rhs` | 计算行号差。 | 调用方须保证来自同一 adapter 根；不同树子范围不可比较。 |
| `==`, `!=`, `<=>` | 比较根索引和行位置。 | 逻辑比较目标是同一范围的游标。 |
| `swap()` | 交换两个迭代器位置。 | 不交换范围内容。 |

## 一句话总结

`ConstRowIterator` 用统一的随机访问接口遍历模型行：列表解引用为 const 项目，表格和树解引用为只读行包装器；它适合遍历和导出，但不能用于写入，也不能跨结构变更或不同树根保存。
