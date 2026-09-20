# QRangeModelAdapter：在直接操作 C++ 范围时，仍保持 Qt 模型通知正确

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.11  
> 状态：Preliminary，API 仍可能调整  
> 头文件：`#include <QRangeModelAdapter>`  
> 模块：`Qt6::Core`

`QRangeModelAdapter` 将一个 C++ 范围和一个 `QRangeModel` 组合成类型安全的容器式接口。它解决的关键问题是：`QRangeModel` 已经把 `std::vector`、`QList` 或树形范围展示给视图后，业务代码怎样继续按 C++ 容器习惯读写、插入、删除和移动，同时让 `QAbstractItemModel` 正确通知视图、清理缓存、更新或失效持久索引。

不要把它理解为“更方便地拿到原容器”。它刻意阻止你取得可直接修改的裸引用，并使用代理引用、行包装器和受约束的结构修改 API，把变更收束到可发出模型通知的路径上。

## 最小使用

```cpp
#include <QRangeModelAdapter>
#include <QListView>
#include <vector>

std::vector<int> values = {1, 2, 3};
QRangeModelAdapter adapter(&values);

QListView view;
view.setModel(adapter.model());

adapter.at(1) = 42;       // 通过模型写入并发出 dataChanged()
adapter.insertRow(3, 99); // 通过模型插入并发出 rowsInserted()
```

`QRangeModelAdapter` 是类模板，但应依靠类模板参数推导（CTAD），不要手写 `Range`、`Protocol`、`Model` 三个模板参数。引用、指针、智能指针和 `std::reference_wrapper` 会推导出不同类型，并直接影响范围所有权与修改落点。

## 范围与模型的所有权

构造 adapter 时会隐式从同一范围构造一个 `QRangeModel`。adapter **拥有这个 model**；调用 `model()` 得到的只是借用指针，不能 `delete`。

adapter 是值类型，可复制、可移动。所有副本共享同一个 `QRangeModel`，最后一个 adapter 副本销毁时模型才销毁。因此，视图保存了 `adapter.model()` 后，至少要保持一个同源 adapter 活着。

| 构造实参 | model / adapter 实际操作的范围 | 修改会回写原对象吗 |
| --- | --- | --- |
| 普通左值或右值范围 | 范围副本 | 否 |
| 裸指针 | 指针所指范围 | 是 |
| `std::ref(range)` | 外部范围 | 是 |
| 智能指针 | 指针所指范围，寿命由智能指针语义管理 | 是 |

```cpp
QList<Book> books = loadBooks();
QRangeModelAdapter copied(books);       // adapter 内部保存副本
QRangeModelAdapter shared(&books);      // 修改 shared 会改 books
```

当 adapter 按值持有范围时，UI 修改后的数据应从 `adapter.range()` 读取，而不是误以为原始左值已被修改。`range()` 只返回 const 引用，正是为了防止绕过 adapter 直接破坏模型通知。

## 为什么可写访问返回“代理”而非 `T &`

可变 `at()`、可变迭代器解引用和可变行访问不直接给出可修改的元素引用。它们返回 `DataReference`、`RowReference` 等代理：

```cpp
auto book = adapter.at(0);   // 可写代理
Book copy = book;            // 读取为值或 const 视图
copy.setRating(5);
book = copy;                 // 写回，经 model 发出 dataChanged()
```

通过 `operator->()` 只能调用项目的 const 成员。以下做法被有意禁止：

```cpp
// adapter.at(0)->setRating(5); // 绕过 dataChanged()，因此不允许
```

表格或树中的单元格同样如此：`adapter.at(row, column) = value` 走单元格代理。异质行，例如 `std::tuple<int, QString>`，单元格代理读取到的是携带真实值的 `QVariant`，应使用 `toInt()`、`toString()` 等按类型取出。

给整个可变行代理赋值会通知该行所有单元格、所有角色发生变化。对于 `std::vector`、`QList` 等运行时长度行，替换行时必须保持正确列数，否则会破坏模型的表格形状假设。

## 列表、表格和树的定位方式

- 列表：`at(row)`、`data(row, role)`、`setData(row, value, role)`；
- 表格：`at(row, column)`、`data(row, column, role)`、`setData(row, column, value, role)`；
- 树：顶层可用 `row`，嵌套项用 `QSpan<const int>` 路径，例如 `{0, 2, 1}` 表示第 0 个顶层节点的第 2 个子节点的第 1 个子节点。

路径重载要求非空路径且每一级索引有效。它们不是带异常检查的安全访问器；无效索引在调试构建会触发前置条件或断言。处理外部输入前先用 `rowCount()` / `hasChildren()` 验证。

对树行调用 `children()` 会得到另一个 adapter，它们共享同一个 model，但把该行作为根。该子 adapter 的增删改仍会通知同一个模型。

## 结构修改的编译期约束

插入、删除和移动函数不是“运行时失败版的万能 API”。只有底层范围满足能力约束时，对应模板重载才会参与重载解析：

- 行插入/删除要求范围支持相应的插入/擦除；
- 列插入/删除要求每一行可动态修改；
- 行或列移动要求相关范围支持元素移动，例如 rotate 或 splice；
- 树路径版还要求范围被识别为树。

当函数存在时，`bool` 返回值仍须检查，表示本次模型修改是否成功。对 iterator、reference wrapper、行代理的引用不要跨结构变更保存；插入、删除、移动、`assign()`、adapter/model 销毁后，将它们视为失效。

```cpp
if (!adapter.removeRows(5, 2)) {
    // 范围不支持删除、位置无效，或修改失败
}
```

## `assign()`：整体替换范围的正确入口

`assign(newRange)`、initializer-list 版本和迭代器范围版本会用模型通知包装整段替换。列表和表格通常走 reset；树的子 adapter 会用对应的移除/插入通知维护父节点结构。

```cpp
adapter.assign(std::vector<int>{10, 20, 30});
adapter = {1, 2, 3}; // 可赋值时等价于相应 assign
```

不要获得 `range()` 后通过 `const_cast` 修改，更不要绕开 adapter 给底层容器重新赋值。那会再次回到 `QRangeModel` 最危险的使用方式：视图看到的是过期结构。

## 迭代器接口

`begin()` / `end()` 支持范围 for：

```cpp
for (auto item : adapter) {
    int value = item;  // 代理读取
    item = value + 1;  // 代理写回并通知模型
}
```

对列表，迭代器解引用的是项目代理；对表格和树，解引用的是行代理。行代理又可遍历列；对树行，额外提供 `hasChildren()` 和 `children()`。const adapter / `std::as_const(adapter)` 给出只读视图，适合遍历和调用 const 成员。

循环中可以修改当前单元格或当前行的值，但不要在仍使用该轮迭代器时插入、删除或移动结构。

## 相等性与 Preliminary 状态

两个 adapter 的 `operator==` 比较的是它们是否持有**同一个 model**，不是范围内容是否相等。两个不同根的树子 adapter 只要共享 model，也会相等。adapter 还可在可比较的前提下与其 `range_type` 比较内容。

该类标注为 Preliminary。不要把它的精确模板签名、嵌套代理类型或 ABI 当作长期稳定的公共库接口；将它隔离在应用代码或较薄的适配层中。

## 常见错误

1. 显式指定模板参数，结果把值、引用或指针语义写错。优先用 CTAD。
2. 将 `adapter.model()` 交给长期存在的视图，却让所有 adapter 副本先销毁。model 随最后一个 adapter 一起销毁。
3. 从可写 `at()` 取得对象后直接调用非 const setter。代理刻意不允许，正确方式是复制、修改、赋回。
4. 用 `range()` 修改内容。它只给 const 引用；试图绕过它会使模型通知失真。
5. 保存 `DataReference` 或 iterator，随后插入/删除行，再继续使用旧代理。
6. 将“两个 adapter 相等”理解为范围内容相等。该比较检查的是共享的 model 实例。
7. 忽略该 API 的 Preliminary 标记，在长期 ABI 边界中暴露其复杂模板类型。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `QRangeModelAdapter(range)` | 从列表或表格范围创建 adapter 与 model。 | 使用 CTAD；按值/引用和指针构造的所有权语义不同。 |
| `QRangeModelAdapter(range, protocol)` | 从树范围和协议创建 adapter。 | `Protocol` 决定树导航；路径 API 仅适用于树。 |
| `model()` | 返回 adapter 拥有的 `Model *`。 | 借用指针，不能删除；至少保留一个 adapter 副本。 |
| `range()` | 返回被操作范围的 const 引用。 | 用于读取最终数据；不可绕过 adapter 修改。 |
| `range_type` | 被包装范围的类型别名。 | 由推导结果决定，勿假设为原始实参的裸类型。 |
| `assign(newRange)` | 用兼容范围整体替换内容。 | 走模型 reset 或树结构通知；旧代理和迭代器视为失效。 |
| `assign(initializer_list)` | 用初始化列表整体替换。 | 仅在范围可赋值且行类型兼容时存在。 |
| `assign(first, last)` | 用迭代器范围整体替换。 | 输入范围必须可迭代且元素与行类型兼容。 |
| `operator=(newRange)` / `operator=(initializer_list)` | `assign()` 的链式赋值形式。 | 不等于 adapter 间复制赋值；替换的是受管范围内容。 |
| `at(row)`，列表 | 访问列表项。 | const 版读值；可写版返回 `DataReference`，越界是前置条件错误。 |
| `at(row)`，表格/树 | 访问完整行或顶层树行。 | 可写版返回行代理，整体赋值会通知整行。 |
| `at(row, column)`，表格 | 访问表格单元。 | 异质列可能得到 `QVariant` 代理。 |
| `at(path)` / `at(path, column)`，树 | 按非空路径访问树行或单元。 | 每一级必须有效；路径元素表示每层子行号。 |
| `operator[]` | 对应 `at()` 的下标语法。 | 边界契约相同；多维下标形式依赖编译器语言特性。 |
| `data(row, ...)` | 以 `QVariant` 读取列表、表格或树角色数据。 | 适合动态类型调用；选对列表/表格/树的坐标重载。 |
| `setData(row, ..., value, role)` | 通过模型写一个角色值。 | 仅对可变范围存在；检查 `bool` 结果。 |
| `index(row, ...)` | 获取对应的 `QModelIndex`。 | 用于与其他模型 API 交互，非法坐标得到无效索引。 |
| `rowCount()` | 返回顶层行数。 | 树中是顶层行数。 |
| `rowCount(row)` / `rowCount(path)` | 返回指定树行的子行数。 | 仅树 adapter 提供。 |
| `columnCount()` | 返回模型列数。 | 列表通常为 1，表格与行类型决定实际列数。 |
| `hasChildren(row)` / `hasChildren(path)` | 查询树行是否有子项。 | 仅树 adapter 提供。 |
| `begin()` / `end()` | 取得可写行或项目迭代器。 | 结构变更会使迭代过程不可靠；写操作通过代理赋值。 |
| `cbegin()` / `cend()` | 取得只读迭代器。 | 适合遍历，不允许借此绕过模型写入。 |
| `insertRow(before)` | 插入默认构造行。 | 仅动态可插入范围提供。 |
| `insertRow(before, data)` | 插入指定行。 | `data` 必须与行类型兼容；树版 `before` 是路径。 |
| `insertRows(before, rows)` | 插入多行。 | 不支持把范围插入自身；检查范围能力与返回值。 |
| `removeRow(row)` / `removeRow(path)` | 删除一行，树版包含其子树。 | 底层范围必须支持删除；旧行代理失效。 |
| `removeRows(row, count)` / `removeRows(path, count)` | 删除连续行。 | `count` 与坐标必须有效，树版路径定位首行。 |
| `moveRow(source, destination)` | 移动一个行。 | 仅支持移动元素的范围提供，注意目标位置的模型语义。 |
| `moveRows(source, count, destination)` | 移动连续行。 | 树版使用源/目标路径；移动后旧坐标不再代表原项目。 |
| `insertColumn(before)` | 在所有行插入默认列值。 | 行必须动态可插入。 |
| `insertColumn(before, data)` | 在所有行插入列数据。 | 单值或范围数据须与列元素兼容。 |
| `insertColumns(before, columns)` | 插入多列。 | 每一行必须能接收相应列范围。 |
| `removeColumn(column)` / `removeColumns(column, count)` | 从所有行删除列。 | 行必须支持删除元素；固定 tuple / array 行不提供。 |
| `moveColumn(from, to)` / `moveColumns(from, count, to)` | 移动列。 | 行范围须支持移动元素。 |
| `DataReference` | 可写单元格代理类型。 | 赋值会通过 model；读取或 `->` 只提供 const 访问。 |
| `RowReference` / `ConstRowReference` | 可写/只读行代理。 | 可遍历列；可写行应整体赋回而非直接修改内部成员。 |
| `RowIterator` / `ConstRowIterator` | 行级迭代器。 | 表格与树 range-for 的解引用类型。 |
| `ColumnIterator` / `ConstColumnIterator` | 行内列迭代器。 | 仅在行代理上使用，结构变更后失效。 |
| `operator==` / `operator!=` | 比较两个 adapter 是否共享同一个 model。 | 不比较范围内容，也不区分树的不同根。 |

## 一句话总结

`QRangeModelAdapter` 是对 `QRangeModel` 的“受通知容器接口”：所有修改都应经过 adapter 的代理或结构 API，才能让视图、缓存和持久索引保持一致；同时要牢记它是 Preliminary API，adapter 副本共享 model，引用与迭代器不能跨结构修改保存。
