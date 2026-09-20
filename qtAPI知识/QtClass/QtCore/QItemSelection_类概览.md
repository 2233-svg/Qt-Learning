# Qt QItemSelection 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QItemSelection>`  
> 所属模块：`Qt6::Core`  
> 继承：`QList<QItemSelectionRange> -> QItemSelection`  
> 定位：用范围描述模型选中项的值类型

## 1. 它解决什么问题

`QItemSelection` 表示模型/视图体系中的一组选中项。它的核心设计不是保存每个 `QModelIndex`，而是保存若干个连续的 `QItemSelectionRange`：

```text
一个选择
  ├─ 范围 A：第 2 至 5 行、第 0 至 3 列
  ├─ 范围 B：第 8 行、第 1 至 1 列
  └─ 范围 C：某个树父项下的连续子项
```

这样做有两个好处：

- 框选一个很大的矩形时，不必立刻为每个单元格保存一份索引；
- 选择模型、代理模型和视图可以在范围层面合并、拆分、映射和比较选择。

`QItemSelection` 主要解决以下场景：

- 让视图或业务代码表示一个矩形区域；
- 把多个局部选择传给 `QItemSelectionModel::select()`；
- 在代理模型和源模型之间转换选择；
- 对选择执行选择、取消选择或切换；
- 从一段选择中减去另一段范围；
- 在需要时把范围展开为具体 `QModelIndex` 列表。

它不是：

- 当前焦点或当前单元格；
- 负责发出 `selectionChanged()` 的对象；
- 保存模型所有权的容器；
- 一定包含每个矩形坐标对应的索引数组；
- 可以混合任意模型索引的通用集合。

真正管理“当前项”和“选择状态”的是 `QItemSelectionModel`。`QItemSelection` 是它使用的值类型之一。

## 2. 先理解它的数据结构

### 2.1 它是范围列表

从类型关系上看：

```cpp
class QItemSelection : public QList<QItemSelectionRange>
```

因此可以遍历或读取它包含的范围：

```cpp
QItemSelection selection(topLeft, bottomRight);

for (const QItemSelectionRange &range : selection) {
    qDebug() << range.top()
             << range.left()
             << range.bottom()
             << range.right();
}
```

继承 `QList` 也意味着它拥有列表的公开操作，例如 `size()`、`isEmpty()`、`at()`、迭代器和 `append()`。但直接操作底层列表可能破坏“范围不重叠”的常见不变量，因此更推荐使用 `select()` 和 `merge()` 表达选择意图。

### 2.2 它本身没有独立的 model 指针

`QItemSelection` 不保存一个单独的 `QAbstractItemModel *` 成员。模型关系来自每个 `QItemSelectionRange` 的端点索引。

因此：

- 空的 `QItemSelection` 没有模型；
- 一个非空选择通常应只包含同一个模型的范围；
- 树模型中，不同父索引下的范围可以同时存在，但每个范围的上下端点必须有相同父项；
- 不要把源模型范围和代理模型范围混放在同一个业务选择中。

### 2.3 选择范围和具体索引是两种表示

构造范围不会立即展开所有索引：

```cpp
QItemSelection selection(topLeft, bottomRight);
```

只有调用：

```cpp
QModelIndexList indexes = selection.indexes();
```

才会展开。对大面积选择，保留范围通常更节省内存；`indexes()` 可能生成大量对象并遍历模型中的每个坐标，应按需要调用。

`QItemSelection` 继承自 Qt 的隐式共享 `QList`，并声明为 shared type。复制一个选择通常只复制共享数据的引用，直到某个副本发生写入才分离；这降低了把选择作为信号参数和值返回值传递的成本，但不改变其中索引对模型生命周期的依赖。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)

target_link_libraries(mytarget
    PRIVATE
        Qt6::Core
)
```

### 3.2 qmake

```qmake
QT += core
```

### 3.3 头文件

```cpp
#include <QItemSelection>
#include <QItemSelectionModel>
#include <QItemSelectionRange>
```

`QItemSelection`、`QItemSelectionRange` 和 `QItemSelectionModel` 的声明实际位于 Qt Core 的 item selection 相关头文件中。使用 `QItemSelection` 时，通常还需要 `QModelIndex` 和 `QItemSelectionModel::SelectionFlags` 的声明，因此直接包含相应的公开头文件最稳妥。

## 4. 最小使用流程

### 4.1 构造一个矩形选择并交给选择模型

```cpp
QModelIndex topLeft = model->index(1, 0);
QModelIndex bottomRight = model->index(3, 2);

QItemSelection selection(topLeft, bottomRight);
selectionModel->select(
    selection,
    QItemSelectionModel::ClearAndSelect);
```

这里的职责分工是：

- `QModelIndex` 表示模型中的位置；
- `QItemSelection` 表示要操作的一个或多个范围；
- `QItemSelectionModel` 决定这些范围如何改变当前选择并发出信号。

### 4.2 添加多个不连续范围

```cpp
QItemSelection selection;
selection.select(model->index(0, 0), model->index(0, 2));
selection.select(model->index(4, 1), model->index(6, 2));

selectionModel->select(
    selection,
    QItemSelectionModel::Select);
```

`select()` 可以把范围加入对象，但不会像 `merge()` 那样保证重叠范围被规范化。若范围之间可能重叠，使用 `merge()`。

### 4.3 读取选择

需要判断某个索引是否在选择中时：

```cpp
if (selection.contains(index)) {
    // index 当前属于选择
}
```

需要把选择交给只接受索引列表的 API 时：

```cpp
const QModelIndexList indexes = selection.indexes();
```

如果是大范围复制、批量删除或导出，先遍历范围，再决定是否需要展开所有索引，通常更节省资源。

## 5. `QItemSelection` 与 `QItemSelectionModel` 的关系

### 5.1 `QItemSelection` 是值，`QItemSelectionModel` 是状态对象

```text
QItemSelection
    选择范围值，可以复制、合并、拆分、传信号

QItemSelectionModel
    绑定一个模型，保存当前选择和 current index，发出变化信号
```

不要把它们混为一谈：

- 创建一个 `QItemSelection` 不会自动改变视图选中状态；
- 只有调用 `QItemSelectionModel::select()`，选择才会应用到选择模型；
- `QItemSelection` 不会发出 `selectionChanged()`；
- `QItemSelectionModel::selection()` 返回的是当前选择的值副本。

### 5.2 current index 不在 `QItemSelection` 里

用户按键移动焦点时，current index 可以改变而选择不变；用户按住 Ctrl 或 Shift 修改选择时，选择可以改变而 current index 按另一个规则更新。它们由 `QItemSelectionModel` 分开管理。

### 5.3 选择命令来自 `QItemSelectionModel::SelectionFlags`

`merge()` 和 `QItemSelectionModel::select()` 使用的命令包括：

```cpp
QItemSelectionModel::Select
QItemSelectionModel::Deselect
QItemSelectionModel::Toggle
QItemSelectionModel::ClearAndSelect
```

但要区分：

- `QItemSelection::merge()` 只支持 `Select`、`Deselect`、`Toggle` 三类选择操作；
- `Clear`、`Current`、`Rows`、`Columns` 是选择模型应用选择时的控制标志；
- `SelectCurrent`、`ToggleCurrent`、`ClearAndSelect` 是组合便利值。

例如：

```cpp
selectionModel->select(
    selection,
    QItemSelectionModel::ClearAndSelect
    | QItemSelectionModel::Rows);
```

这里 `Rows` 由选择模型处理，把索引范围扩展到整行；它不是 `QItemSelection` 自己展开的功能。

## 6. 范围的模型和父索引约束

### 6.1 两个端点必须来自同一个模型

构造：

```cpp
QItemSelection selection(topLeft, bottomRight);
```

时，`topLeft` 和 `bottomRight` 应属于同一个 `QAbstractItemModel`。不要把一个源模型索引和一个代理模型索引拼成范围。

### 6.2 两个端点必须有相同父项

对于树模型，范围是“同一个父项下的连续行列矩形”。因此：

```text
topLeft.parent() == bottomRight.parent()
```

必须成立。不能用一个父节点下的第 0 个子项和另一个父节点下的第 3 个子项构造单个范围。

如果要选择不同父项下的项目，应创建多个 `QItemSelectionRange`，分别加入 `QItemSelection`。

### 6.3 行列顺序必须形成有效矩形

有效范围应满足：

```text
top <= bottom
left <= right
```

同时两个端点都应有效，父项相同。否则范围会是无效的，`contains()`、`indexes()` 和合并结果都不能按正常选择理解。

Qt 的 `select(topLeft, bottomRight)` 会把端点按矩形语义处理，但调用者仍应传入同一模型、同一父项的索引，不要依赖它修复跨父项或跨模型输入。

## 7. 选择范围的压缩和展开

### 7.1 为什么不直接使用 `QModelIndexList`

假设用户框选 10000 行、20 列：

```text
10000 x 20 = 200000 个单元格
```

用 `QModelIndexList` 立刻保存 200000 个索引，会产生更多内存和遍历开销；用一个 `QItemSelectionRange` 可以先表达这个矩形。

### 7.2 `indexes()` 会过滤不可选项

`QItemSelection::indexes()` 和 `QItemSelectionRange::indexes()` 不只是简单地生成每个坐标的索引。Qt 会根据模型索引的 flags 过滤项目：

- 没有 `Qt::ItemIsSelectable` 的项不会进入结果；
- 没有 `Qt::ItemIsEnabled` 的项不会进入结果；
- 结果数量可能小于几何矩形的面积。

因此：

```cpp
QItemSelection selection(topLeft, bottomRight);
const int rangeArea =
        (bottomRight.row() - topLeft.row() + 1)
        * (bottomRight.column() - topLeft.column() + 1);
const int actualCount = selection.indexes().size();
```

`actualCount` 不一定等于 `rangeArea`。

### 7.3 `contains()` 也会考虑可选择性

判断一个索引是否包含在范围内时，几何位置相同还不一定足够。`QItemSelection::contains()` 会先检查索引同时具有 `Qt::ItemIsSelectable` 和 `Qt::ItemIsEnabled`。

`contains()` 和 `QItemSelectionRange::contains()` 的调用前提仍是索引属于同一个模型。范围几何判断主要比较 row、column 和 parent；不要把它们当作跨模型索引的安全校验器，尤其不要依赖两个根项都使用无效 parent 时的偶然结果。

这意味着 `QItemSelection` 表达的是“模型允许作为选择的项目”，不是一个无条件的坐标矩形集合。

### 7.4 展开是有成本的

以下操作可能需要遍历大量索引：

- `selection.indexes()`；
- 每次循环都对大范围调用 `contains()`；
- 对每个展开索引调用复杂的 `data()`；
- 把大选择跨线程复制并序列化。

能使用范围边界解决的问题，优先使用 `top()`、`left()`、`bottom()`、`right()` 和 `parent()`；确实需要逐项处理时再展开。

## 8. `select()` 与 `merge()` 的区别

### 8.1 `select(topLeft, bottomRight)`：追加一个范围

```cpp
QItemSelection selection;
selection.select(topLeft, bottomRight);
```

它把指定矩形加入选择对象。适合：

- 从零开始构造几个已知范围；
- 调用者确定范围之间不重叠；
- 需要保留每次追加的原始范围边界。

它不是选择状态操作，不会发出任何信号，也不会修改 `QItemSelectionModel`。

### 8.2 `merge(other, command)`：规范化地合并选择

```cpp
selection.merge(other, QItemSelectionModel::Select);
```

`merge()` 会根据 `command` 对两个选择做集合操作，并保证结果中没有重叠范围：

- `Select`：把 `other` 加入；
- `Deselect`：从当前选择中去掉 `other`；
- `Toggle`：当前选中的部分去掉，未选中的部分加入。

它只支持这三个选择命令。不要把 `Clear`、`Current`、`Rows` 或 `Columns` 当成 `merge()` 的替代参数。

### 8.3 `merge()` 可能拆成多个矩形

例如当前选择是一个大矩形，取消其中间一块后，结果可能变成上、下、左、右四个矩形：

```text
原范围：      ########
去掉中间：    ##    ##
结果：        ########
```

一个矩形不能表达带洞的选择，因此 `merge()` 会使用多个不重叠范围表示同一个集合。

### 8.4 直接继承 QList 操作的风险

下面的代码可以通过继承的 `append()` 加入范围：

```cpp
selection.append(QItemSelectionRange(topLeft, bottomRight));
```

但它不会自动拆分重叠区域，也不会执行 `Select` / `Deselect` / `Toggle` 语义。想维护规范化选择时，应使用 `merge()`。

## 9. `split()`：从范围中减去另一个范围

```cpp
QItemSelection result;
QItemSelection::split(range, other, &result);
```

它执行近似集合差：

```text
range - other
```

结果中保留 `range` 内不属于 `other` 的部分，并把这些剩余矩形追加到 `result`。

### 9.1 使用边界

- `range` 和 `other` 应属于同一模型、同一父项；
- `result` 必须是有效的非空指针；
- `split()` 不会自动清空 `result`，如果只想得到本次差集，先创建空的 `QItemSelection`；
- `other` 不相交时，结果通常保留原范围；
- `other` 覆盖整个 `range` 时，不产生剩余范围；
- 部分重叠时，剩余部分可能是多个矩形。

### 9.2 典型用途

- 实现取消选择；
- 在选择缓存中去掉一个局部矩形；
- 调试 `merge(Deselect)` 的范围变化；
- 把一个大范围分解成多个可独立处理的部分。

通常业务代码不需要直接调用 `split()`，让 `merge()` 处理选择集合更安全；只有自定义范围算法需要精确控制差集时才直接使用它。

## 10. 选择和代理模型

代理模型有两个选择坐标系：

```text
source selection
      ⇅ mapSelectionFromSource / mapSelectionToSource
proxy selection
```

例如：

```cpp
QItemSelection proxySelection = selectionModel->selection();
QItemSelection sourceSelection =
        proxyModel->mapSelectionToSource(proxySelection);
```

使用规则：

- 绑定代理模型的视图和选择模型使用代理选择；
- 修改源模型时使用源选择；
- `QItemSelection` 中的所有索引必须属于对应那一层模型；
- 过滤或排序代理可能把一个连续源范围变成多个代理范围；
- 不要把代理选择直接交给源模型的 `select()`。

对 `QIdentityProxyModel`，结构保持一一对应，选择转换通常简单；对 `QSortFilterProxyModel` 或复杂自定义代理，不能假设范围端点按行列直接复制。

## 11. 选择、模型变化与索引生命周期

`QItemSelectionRange` 内部使用 `QPersistentModelIndex` 保存端点，因此范围比普通临时 `QModelIndex` 更能跨越部分模型变化。但这不是永久有效保证：

- 删除范围覆盖的项后，持久索引可能失效；
- model reset 后，原选择通常应视为失效；
- 更换 `QItemSelectionModel` 的模型后，旧选择不能交给新模型；
- 代理模型更换源模型后，跨层选择需要重新映射或重建。

`QItemSelection` 的值拷贝不会把模型复制一份，也不会锁住模型生命周期。模型必须在使用其索引期间保持有效。

## 12. 典型实际场景

### 12.1 批量导出用户框选区域

```cpp
const QItemSelection selection = selectionModel->selection();

for (const QItemSelectionRange &range : selection) {
    for (int row = range.top(); row <= range.bottom(); ++row) {
        for (int column = range.left(); column <= range.right(); ++column) {
            const QModelIndex index =
                    model->index(row, column, range.parent());
            if (!index.isValid() || !selection.contains(index))
                continue;

            exportCell(index);
        }
    }
}
```

如果必须保持选择模型的可选/可用过滤，调用 `selection.indexes()` 会更直接；如果数据量很大，应评估逐格调用的成本。

### 12.2 程序化选择整行

```cpp
const int row = 4;
QItemSelection rowSelection(
        model->index(row, 0),
        model->index(row, model->columnCount() - 1));

selectionModel->select(
    rowSelection,
    QItemSelectionModel::ClearAndSelect);
```

对树模型，最后一个列索引必须使用同一个父项；对具有隐藏列或不可选择列的模型，实际 selected indexes 可能少于整行几何范围。

也可以让选择模型按整行扩展：

```cpp
selectionModel->select(
    model->index(row, 0),
    QItemSelectionModel::ClearAndSelect
    | QItemSelectionModel::Rows);
```

### 12.3 计算增量选择

`QItemSelectionModel::selectionChanged(selected, deselected)` 给出两个 `QItemSelection`：

```cpp
connect(selectionModel,
        &QItemSelectionModel::selectionChanged,
        this,
        [this](const QItemSelection &selected,
               const QItemSelection &deselected) {
            updateAddedRanges(selected);
            updateRemovedRanges(deselected);
        });
```

这里的 `selected` 和 `deselected` 是变化增量，不一定等于变化后的完整选择。需要完整状态时调用 `selectionModel->selection()`。

## 13. 常见误区与排查顺序

### 13.1 把 `QItemSelection` 当成索引列表

**现象：** 直接按下标访问时得到的是 `QItemSelectionRange`，不是 `QModelIndex`。

**处理：**

```cpp
for (const QItemSelectionRange &range : selection) {
    // 先处理范围
}

QModelIndexList indexes = selection.indexes();
```

### 13.2 忽略 `select()` 与 `merge()` 的区别

**现象：** 选择对象中出现重叠范围，取消选择后结果难以理解。

**原因：** `select()` 只是加入范围，`merge()` 才进行选择集合运算并保证不重叠。

### 13.3 传入跨模型索引

**现象：** `contains()` 结果异常，映射选择后选择错位，或调试构建出现警告。

**处理：** 检查每个端点和待查询索引的 `model()`，代理选择先映射到正确的模型层。不要把 `contains()` 当作跨模型输入的防线。

### 13.4 用不同父项的索引构造一个范围

**现象：** 树模型中的选择为空或无效。

**原因：** 一个 `QItemSelectionRange` 必须描述同一父项下的矩形。

### 13.5 以为 `indexes()` 等于矩形面积

**现象：** 选择 10 个坐标，却只得到 7 个索引。

**原因：** `indexes()` 只返回同时具有 `Qt::ItemIsSelectable` 和 `Qt::ItemIsEnabled` 的索引。

### 13.6 以为复制选择会延长模型生命周期

**现象：** 模型删除后继续使用保存的选择。

**原因：** `QItemSelection` 只复制范围和持久索引，不拥有模型。

### 13.7 把 current index 当成选择范围

**现象：** 清除选择后仍然有焦点项，或移动 current index 时选中状态没有按预期变化。

**处理：** 使用 `QItemSelectionModel::currentIndex()` 与 `selection()` 分别读取两个状态。

### 13.8 直接用 `QList::append()` 维护复杂选择

**现象：** 范围重叠、`deselected` 增量不稳定或后续算法需要处理大量重复区域。

**处理：** 用 `merge()` 进行选择、取消选择和切换；仅在明确需要保留原始范围时使用继承的列表操作。

## 14. 线程边界

`QItemSelection` 是值类型，复制和传递本身不需要 QObject 线程归属；但它里面的 `QModelIndex` 和 `QPersistentModelIndex` 仍然引用具体模型。

因此：

- 不要把 GUI 模型的选择当作可在任意线程直接使用的快照；
- 后台线程处理业务数据时，优先把业务主键或普通数据副本传过去；
- 如果必须读取索引对应的数据，应在模型所属线程完成；
- 跨线程传递选择后，模型可能已经 reset 或删除项目，使用前仍要验证有效性。

## 15. API 逐项说明

下面按 Qt 6.11.1 的 `QItemSelection` 直接成员展开。继承自 `QList<QItemSelectionRange>` 的通用列表 API 不重复逐项列出，但会在使用边界中说明。

### `QItemSelection()`

**作用：** 构造一个空选择。

**关键语义：**

- 不包含任何范围；
- 没有可查询的模型；
- 可以随后用 `select()`、`append()` 或 `merge()` 加入范围；
- 作为 `QItemSelectionModel::select()` 的空输入时不会选中任何项目。

**边界：** 空选择与“选择了一个面积为零的范围”不是同一概念；有效范围至少包含一个有效模型索引。

### `QItemSelection(const QModelIndex &topLeft, const QModelIndex &bottomRight)`

**作用：** 用两个端点构造一个范围选择。

**关键语义：**

- 范围包含从左上到右下的矩形；
- 两个索引必须来自同一模型；
- 两个索引必须有相同父项；
- 结果内部保存一个 `QItemSelectionRange`。

**边界：**

- 端点无效、父项不同或模型不同会得到无效/不可用选择；
- 不会自动把多个父项下的项目拼成一个范围；
- 不会自动修改 `QItemSelectionModel` 的状态。

### `bool contains(const QModelIndex &index) const`

**作用：** 判断选择是否包含指定模型索引。

**关键语义：**

- 检查索引是否位于某个范围的行列和父项内；
- 会检查索引是否同时具有 `Qt::ItemIsSelectable` 和 `Qt::ItemIsEnabled`；
- 输入索引必须属于与范围相同的模型。
- 实现不会替调用者完成完整的跨模型校验。

**边界：**

- 不要把跨模型索引传入并依赖它返回 false；
- 无效索引通常返回 false，因为没有可选择 flags；
- 缺少 `Qt::ItemIsSelectable` 或 `Qt::ItemIsEnabled` 都会被此函数排除。

### `QModelIndexList indexes() const`

**作用：** 把选择范围展开为具体模型索引列表。

**关键语义：**

- 遍历选择中的每个范围；
- 返回可选择且启用的模型索引；
- 结果可能不按业务语义排序，不应依赖跨范围的特殊顺序；
- 对大范围可能产生较高内存和时间成本。

**边界：**

- 不会返回不可选或禁用项；
- 模型在展开期间应保持结构稳定；
- 返回的索引属于范围所引用的模型，不属于 `QItemSelection` 自身。

### `void merge(const QItemSelection &other, QItemSelectionModel::SelectionFlags command)`

**作用：** 按选择命令把 `other` 合并到当前选择。

**支持的命令：**

- `QItemSelectionModel::Select`；
- `QItemSelectionModel::Deselect`；
- `QItemSelectionModel::Toggle`。

**关键语义：**

- `Select` 做集合并集；
- `Deselect` 做集合差；
- `Toggle` 对交集取消、对差集加入；
- 结果保证范围之间不重叠。

**边界：**

- 不负责发信号；
- 不应把 `Clear`、`Current`、`Rows`、`Columns` 当作 merge 命令；
- `other` 与当前选择应针对同一个模型；
- 复杂差集可能产生多个范围。

### `void select(const QModelIndex &topLeft, const QModelIndex &bottomRight)`

**作用：** 把一个矩形范围加入选择对象。

**关键语义：**

- 创建 `QItemSelectionRange` 并加入列表；
- 两个端点必须有相同父项；
- 不会清理已有重叠范围；
- 不会发出选择变化信号。

**边界：**

- 跨模型或跨父项输入不应使用；
- 需要不重叠规范化时改用 `merge()`；
- 它与 `QItemSelectionModel::select()` 同名但职责不同，前者修改值对象，后者修改选择状态。

### `static void split(const QItemSelectionRange &range, const QItemSelectionRange &other, QItemSelection *result)`

**作用：** 从 `range` 中减去 `other`，把剩余范围追加到 `result`。

**关键语义：**

- 相交部分被移除；
- 结果可以是零个、一个或多个矩形；
- `result` 是输出容器，不会自动清空；
- 可用于实现精确的范围差集。

**边界：**

- `result` 不能是 null；
- 两个输入范围应属于同一模型和父项；
- 如果调用者希望只得到本次结果，应先清空输出；
- 普通选择修改优先使用 `merge(Deselect)`。

## API 速查表
| API | 类型 | 作用 | 使用重点 |
| --- | --- | --- | --- |
| `QItemSelection()` | 构造函数 | 创建空选择 | 空选择没有模型归属；不会改变选择模型 |
| `QItemSelection(const QModelIndex &topLeft, const QModelIndex &bottomRight)` | 构造函数 | 创建一个矩形范围选择 | 两个端点必须同模型、同父项；不会自动应用到视图 |
| `contains(const QModelIndex &index) const` | 查询 | 判断索引是否属于选择 | 检查 `ItemIsSelectable` 和 `ItemIsEnabled`；调用前必须保证索引属于同一模型 |
| `indexes() const` | 展开 | 返回选择中的具体索引 | 过滤不可选/禁用项；大范围展开有成本 |
| `merge(const QItemSelection &other, QItemSelectionModel::SelectionFlags command)` | 集合运算 | 选择、取消选择或切换范围 | 只支持 Select/Deselect/Toggle；结果范围不重叠 |
| `select(const QModelIndex &topLeft, const QModelIndex &bottomRight)` | 范围追加 | 把一个矩形加入列表 | 只追加，不做重叠规范化，也不发信号 |
| `static split(const QItemSelectionRange &range, const QItemSelectionRange &other, QItemSelection *result)` | 静态集合运算 | 从一个范围中减去另一个范围 | result 不自动清空；输出可能包含多个范围 |
| 继承的 `QList<QItemSelectionRange>` API | 列表操作 | 遍历、读取或直接修改范围列表 | 直接 append/insert 可能破坏不重叠等选择不变量 |

## 17. 一句话总结

`QItemSelection` 是模型选择的“范围值对象”：它用多个 `QItemSelectionRange` 压缩表示选中区域，用 `merge()` 执行选择集合运算，用 `split()` 做范围差集，必要时再通过 `indexes()` 展开。使用时最重要的是保持同一模型和同一父项约束，并记住 `select()` 只是追加范围，而 `QItemSelectionModel` 才真正管理选择状态和变化信号。
