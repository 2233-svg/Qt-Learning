# Qt QItemSelectionRange 选择范围深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QItemSelectionRange>`  
> 所属模块：`Qt6::Core`  
> 类型性质：轻量值类型、可比较、可放入容器  
> 相关类型：`QModelIndex`、`QPersistentModelIndex`、`QItemSelection`、`QItemSelectionModel`

## 1. 它解决什么问题

`QItemSelectionRange` 用一个矩形范围表示模型中的一组连续项目。它描述的是：

```text
同一个父项下面
从 topLeft 到 bottomRight
覆盖若干连续行和若干连续列
```

在表格模型里，它就是一个矩形单元格区域：

```text
        column 1   column 2   column 3
row 2      [x]        [x]        [x]
row 3      [x]        [x]        [x]
row 4      [x]        [x]        [x]
```

它主要解决以下问题：

- 用两个端点压缩表示大面积选择；
- 判断某个模型索引是否落在选择范围内；
- 判断两个范围是否重叠；
- 求两个范围的矩形交集；
- 获取范围的行列边界、宽高和父索引；
- 在需要时把范围展开成 `QModelIndexList`；
- 作为 `QItemSelection` 的元素传给 `QItemSelectionModel`。

它不是：

- 一个选择模型，不保存“当前全部选择”；
- 一个 `QAbstractItemModel`，不提供数据；
- 一个通用的二维数组，不拥有范围内的业务对象；
- 可以跨不同父节点拼接的树节点集合；
- 自动排序或自动修正端点的构造器。

理解这个类最重要的一句话是：

> 一个 `QItemSelectionRange` 是同一模型、同一父项下的一块闭区间矩形。

## 2. 它的内部表示

Qt 的头文件中，`QItemSelectionRange` 主要保存两个 `QPersistentModelIndex`：

```text
topLeft       ─────┐
                   │  矩形范围
bottomRight   ────┘
```

这带来几个直接结论：

- 范围的边界不是四个独立整数；
- `top()`、`left()`、`bottom()`、`right()` 都是从两个端点索引读取的；
- 范围内部保存的是持久索引，模型正确通知结构变化时，边界索引可以跟随项目移动；
- 范围不会复制或拥有模型本身；
- 端点失效后，范围也可能变成无效范围。

### 2.1 闭区间

范围包含端点本身：

```cpp
QItemSelectionRange range(model->index(2, 1),
                          model->index(4, 3));
```

它覆盖：

```text
row:    2, 3, 4
column: 1, 2, 3
```

因此：

```cpp
range.height() == 3;
range.width() == 3;
```

只有在范围有效时，才应把宽高理解为实际覆盖的行列数量。

### 2.2 同一父项约束

在平面表格中，两个端点通常都使用无效父索引：

```cpp
QModelIndex();
```

在树模型中，两个端点必须拥有同一个父索引：

```text
parent A
  ├─ child row 0
  ├─ child row 1  ← topLeft
  └─ child row 2  ← bottomRight
```

下面这种范围不能表达一个合法矩形：

```text
parent A 下的项目  ──┐
                     ├─ 不能拼成一个 QItemSelectionRange
parent B 下的项目  ──┘
```

如果选择涉及不同父节点，应创建多个 `QItemSelectionRange`，放进一个 `QItemSelection`。

### 2.3 端点必须按左上、右下传入

构造函数会直接保存传入的端点，不会自动交换它们：

```cpp
QItemSelectionRange range(topLeft, bottomRight);
```

调用方应保证：

```text
topLeft.row()    <= bottomRight.row()
topLeft.column() <= bottomRight.column()
```

如果行列方向反了，范围会无效。需要先计算边界时，应由调用方构造真正的左上和右下索引，而不是期待类自动归一化。

## 3. 实际使用场景

### 3.1 表格框选

视图或业务代码可以把鼠标拖拽的两个角转成一个范围：

```cpp
const QModelIndex topLeft = model->index(firstRow, firstColumn);
const QModelIndex bottomRight = model->index(lastRow, lastColumn);

const QItemSelectionRange range(topLeft, bottomRight);
```

然后交给选择模型：

```cpp
selectionModel->select(range,
                       QItemSelectionModel::ClearAndSelect);
```

### 3.2 只处理一个矩形

如果业务需要给一个选区内的每个单元格加边框、统计数值或导出数据，可以先使用边界快速判断，再按需展开：

```cpp
if (range.isValid() && !range.isEmpty()) {
    const int rowCount = range.height();
    const int columnCount = range.width();
    Q_UNUSED(rowCount);
    Q_UNUSED(columnCount);
}
```

### 3.3 求两个选择区域的重叠

```cpp
if (first.intersects(second)) {
    const QItemSelectionRange common = first.intersected(second);
    consume(common);
}
```

这适合：

- 判断两个批量操作是否有重叠；
- 计算增量选择的公共部分；
- 做范围差集前先定位交集；
- 代理模型映射后比较选择区域。

### 3.4 树模型的同一父项选择

树模型中的“行”不是全局行号，而是某个父节点下面的兄弟序号：

```cpp
const QModelIndex parent = model->index(parentRow, 0);
const QModelIndex topLeft = model->index(2, 0, parent);
const QModelIndex bottomRight = model->index(5, 2, parent);

QItemSelectionRange range(topLeft, bottomRight);
```

它表示 `parent` 下第 2 至 5 行、第 0 至 2 列，不表示整个树中所有同号行。

## 4. 构建与包含

### 4.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 4.2 头文件

```cpp
#include <QItemSelectionRange>
```

使用 `QItemSelectionModel::SelectionFlags` 或 `QItemSelection` 时，通常还会包含：

```cpp
#include <QItemSelectionModel>
#include <QItemSelection>
```

## 5. 有效、为空和有尺寸不是同一个概念

这三个问题必须分开：

```text
isValid()  ：两个端点和坐标关系是否构成合法范围？
isEmpty()  ：范围里是否没有可选且启用的项目？
width/height：按端点坐标计算出的几何尺寸是多少？
```

### 5.1 `isValid()`

头文件中的有效性条件可以概括为：

- `topLeft()` 有效；
- `bottomRight()` 有效；
- 两个端点的父索引相同；
- `top() <= bottom()`；
- `left() <= right()`。

“同一个模型”是构造和使用时的基本前提。调用方不要把不同模型的索引混进一个范围，即使某些无效父索引的比较结果看起来相同。

### 5.2 `isEmpty()`

官方语义比“范围无效”更细：

> 如果范围没有项目，或者范围内所有项目都被禁用或标记为不可选择，则返回 `true`。

因此一个范围可以同时满足：

```text
isValid() == true
isEmpty() == true
```

例如模型有一个几何上合法的矩形，但所有单元格的 `flags()` 都没有 `Qt::ItemIsSelectable`，或者都没有 `Qt::ItemIsEnabled`。

### 5.3 默认对象的宽高边界

默认构造的 `QItemSelectionRange` 是空的、无效的范围。不要在未检查 `isValid()` 的情况下使用 `width()` 和 `height()` 表示实际选区大小。

原因是这两个函数按端点坐标做简单的闭区间算术，而无效 `QModelIndex` 的行列值不代表真实模型坐标。正确顺序是：

```cpp
if (!range.isValid()) {
    return;
}

const int rows = range.height();
const int columns = range.width();
```

## 6. 与 `QItemSelection` 的关系

`QItemSelection` 本质上是若干个 `QItemSelectionRange` 的列表：

```cpp
QItemSelection selection;
selection.append(QItemSelectionRange(topLeft, bottomRight));
selection.append(QItemSelectionRange(otherTopLeft, otherBottomRight));
```

两者职责不同：

| 类型 | 职责 |
| --- | --- |
| `QItemSelectionRange` | 表示一个父项下的一个连续矩形 |
| `QItemSelection` | 表示多个范围组成的选择值 |
| `QItemSelectionModel` | 管理当前选择、current index 和变化信号 |

`QItemSelectionRange` 不会：

- 自动发出 `selectionChanged()`；
- 自动合并相邻或重叠范围；
- 自动应用到视图；
- 自动把自己变成业务对象列表。

如果需要合并、取消或切换多个范围，应使用 `QItemSelection::merge()` 或 `QItemSelectionModel::select()`。

## 7. 持久索引和模型生命周期

### 7.1 为什么内部使用 `QPersistentModelIndex`

普通 `QModelIndex` 适合即时查询。模型插入、删除、移动或布局变化后，之前保存的普通索引可能不再代表同一个项目。

`QItemSelectionRange` 内部保存 `QPersistentModelIndex`，是因为选择范围经常要跨越一次模型更新。例如：

```text
用户选中第 5 至 8 行
模型在前面插入 2 行
```

如果模型正确发出结构变化通知，范围端点可以跟随被选中的项目移动到新的行号。

### 7.2 持久索引不是永久有效

持久索引也不是业务 ID：

- 项目被删除后，持久索引可能变为无效；
- 模型 reset 后，原索引通常整体失效；
- 模型对象销毁后，范围不能继续使用；
- 自定义模型如果不正确发出 begin/end 通知，持久索引也无法可靠更新。

因此每次使用范围前，仍建议检查：

```cpp
if (!range.isValid() || !range.model()) {
    return;
}
```

### 7.3 模型不是范围的所有者

`model()` 返回的是非拥有指针。范围只引用端点所属的模型，不负责删除模型，也不延长模型的业务生命周期。

## 8. 逐项 API 说明

### `QItemSelectionRange()`

**作用：** 构造一个空的选择范围。

**关键语义：**

- 不包含任何有效模型索引；
- `isValid()` 返回 `false`；
- `topLeft()` 和 `bottomRight()` 对应无效的持久索引；
- 适合作为“无交集”或“尚未设置范围”的返回值。

**边界：**

- 不要把默认对象当成一个 1×1 单元格；
- 不要直接使用其 `width()` 和 `height()` 代表有效尺寸；
- 传给选择模型前应先判断有效性。

### `explicit QItemSelectionRange(const QModelIndex &index)`

**作用：** 构造只包含一个模型索引的 1×1 范围。

**关键语义：**

```cpp
QItemSelectionRange range(index);
```

等价于把同一个索引同时作为左上角和右下角：

```text
top == bottom == index.row()
left == right == index.column()
```

**边界：**

- `index` 应有效；
- `index` 必须属于要使用的模型；
- 无效索引构造出的范围不会自动变成“根节点范围”；
- 单个索引的可选性和启用状态仍由模型 flags 决定。

### `QItemSelectionRange(const QModelIndex &topLeft, const QModelIndex &bottomRight)`

**作用：** 构造由左上和右下两个端点界定的矩形范围。

**关键语义：**

- 两个端点应属于同一个模型；
- 两个端点应有同一个父索引；
- `topLeft` 应在 `bottomRight` 的左上方；
- 构造函数保存端点，不会自动交换行列；
- 端点使用持久索引语义保存。

**边界：**

- 不同父项不能组成一个树范围；
- 反向端点会得到无效范围；
- 不能用它跨多个树分支表达选择；
- 构造成功不等于 `isValid()` 一定为 `true`，构造后仍可检查。

### `int top() const`

**作用：** 返回范围最上方行的行号。

**关键语义：**

- 对有效范围，等于 `topLeft().row()`；
- 行号是相对于 `parent()` 的局部行号；
- 树模型中不是全局树深度，也不是业务 ID。

**边界：**

- 无效范围不要把返回值当有效行号；
- 模型结构变化后，若持久端点移动，返回行号也可能变化；
- 需要索引身份时保留 `topLeft()`，不要只保存整数。

### `int left() const`

**作用：** 返回范围最左侧列的列号。

**关键语义：**

- 对有效范围，等于 `topLeft().column()`；
- 列号是相对于 `parent()` 的模型列号；
- 视图隐藏列、排序或显示位置不会改变这个模型坐标。

**边界：**

- 无效范围不要把返回值当有效列号；
- 代理模型和源模型的列坐标可能不同；
- 需要跨结构变化保存项目时使用端点索引或业务 ID。

### `int bottom() const`

**作用：** 返回范围最下方行的行号。

**关键语义：**

- 对有效范围，等于 `bottomRight().row()`；
- 端点是闭区间，因此 `height()` 会包含这一行；
- 行号仍然相对于共同父项。

**边界：**

- 反向或无效范围的返回值没有有效几何意义；
- 结构变化后行号可能因持久索引移动而改变；
- 不能把它和另一个父项下的行号直接比较。

### `int right() const`

**作用：** 返回范围最右侧列的列号。

**关键语义：**

- 对有效范围，等于 `bottomRight().column()`；
- 端点是闭区间；
- 是模型列号，不是视图中的可见列序号。

**边界：**

- 无效范围不要依赖返回值；
- 不同父项下相同列号没有同一业务含义；
- 代理列坐标需要先映射。

### `const QPersistentModelIndex &topLeft() const`

**作用：** 返回范围左上角的持久模型索引。

**关键语义：**

- 返回的是 `QPersistentModelIndex` 引用，不是临时 `QModelIndex`；
- 左上角决定 `top()` 和 `left()`；
- 模型正确发送结构通知时，持久索引可以跟随项目变化。

**边界：**

- 引用只在当前范围对象及其内部端点保持稳定时有效；
- 不要在修改、交换或销毁范围后继续保存这个引用；
- 端点项目被删除后，持久索引可能无效；
- 用 `QModelIndex index = range.topLeft();` 复制出即时索引时，仍要考虑后续模型变化。

### `const QPersistentModelIndex &bottomRight() const`

**作用：** 返回范围右下角的持久模型索引。

**关键语义：**

- 返回的是右下角持久索引；
- 右下角决定 `bottom()` 和 `right()`；
- 与 `topLeft()` 一起确定矩形边界。

**边界：**

- 引用不应跨越范围对象的修改和销毁保存；
- 端点必须和 `topLeft()` 处于同一个模型、同一个父项；
- 项目被删除或模型 reset 后可能变为无效。

### `QModelIndex parent() const`

**作用：** 返回范围内所有项目共同的父模型索引。

**关键语义：**

- 对平面表格，通常返回无效索引，表示根层级；
- 对树模型，返回共同父节点；
- 它决定 `top()`、`left()` 等坐标的解释范围。

**边界：**

- 返回的是普通 `QModelIndex` 值；
- 无效父索引不等于“错误”，它通常表示模型根层级；
- 无效范围的父索引不能用来证明范围有效。

### `const QAbstractItemModel *model() const`

**作用：** 返回范围端点所属的模型。

**关键语义：**

- 对有效范围，通常等于端点索引的 `model()`；
- 可用于校验一个范围是否属于当前选择模型；
- 默认空范围通常返回 `nullptr`。

**边界：**

- 返回非拥有指针；
- 不要把它当作范围保存模型的所有权证明；
- 范围和模型生命周期必须协调；
- 业务代码仍应避免跨模型构造范围。

### `int width() const`

**作用：** 返回范围覆盖的列数。

**关键语义：**

```text
width = right - left + 1
```

这是闭区间宽度：

```cpp
QItemSelectionRange range(model->index(2, 1),
                          model->index(4, 3));
Q_ASSERT(range.width() == 3);
```

**边界：**

- 先确认 `isValid()`；
- 无效范围的端点坐标不代表真实尺寸；
- 它计算的是几何列数，不是可选择项目数量；
- 范围内有禁用或不可选择项时，`width()` 仍然按坐标计算。

### `int height() const`

**作用：** 返回范围覆盖的行数。

**关键语义：**

```text
height = bottom - top + 1
```

它与 `width()` 一样使用闭区间：

```cpp
QItemSelectionRange range(model->index(2, 1),
                          model->index(4, 3));
Q_ASSERT(range.height() == 3);
```

**边界：**

- 先确认范围有效；
- 它不是 `indexes().size()` 的替代品；
- 禁用、不可选择或模型空洞不会改变几何高度；
- 树模型中的行数是共同父项下的局部行数。

### `bool contains(const QModelIndex &index) const`

**作用：** 判断给定模型索引是否落在范围内。

**关键语义：**

- 比较索引的行号、列号和父索引；
- 只有同一父项下的坐标才可能包含；
- 不会返回范围外索引；
- 这是几何包含判断，不是对选择模型状态的查询。

**边界：**

- 调用方必须保证 `index` 属于与范围相同的模型；
- 不要把 `contains()` 当成跨模型校验器；
- `index` 的 `flags()` 是否可选不是这个函数的主要判断条件；
- 无效范围通常不包含有效索引。

### `bool contains(int row, int column, const QModelIndex &parentIndex) const`

**作用：** 用行号、列号和父索引判断一个坐标是否落在范围内。

**关键语义：**

```cpp
if (range.contains(row, column, parentIndex)) {
    // 该坐标在矩形范围内
}
```

- `row` 和 `column` 按共同父项解释；
- `parentIndex` 必须和 `range.parent()` 对应；
- 不需要先创建一个新的 `QModelIndex`。

**边界：**

- 调用方应保证坐标属于同一模型的有效坐标空间；
- 不同模型但相同无效父索引的坐标不要混用；
- 负行号、负列号不会变成有效项目；
- 它与 `contains(const QModelIndex &)` 是重载，不是两个不同的选择语义。

### `QModelIndexList indexes() const`

**作用：** 把范围展开成范围内的模型索引列表。

**关键语义：**

- 每个坐标生成一个 `QModelIndex`；
- 返回的是普通索引列表；
- 结果规模通常接近 `width() * height()`；
- 适合真正需要逐项读取或处理的场景。

示例：

```cpp
for (const QModelIndex &index : range.indexes()) {
    const QVariant value = index.data(Qt::DisplayRole);
    consume(value);
}
```

**边界：**

- 大范围展开会产生时间和内存成本；
- 不要在只需要边界时调用；
- 模型在展开期间应保持结构稳定；
- 返回索引不自动延长模型生命周期；
- 需要完整选择而不是单个范围时，使用 `QItemSelectionModel::selectedIndexes()`。

### `bool intersects(const QItemSelectionRange &other) const`

**作用：** 判断两个范围是否有重叠。

**关键语义：**

- 两个范围需要处于相同坐标空间；
- 共同父项不同，不能视为同一个矩形平面的交集；
- 行区间和列区间都重叠时才有交集；
- 仅相邻但不重叠的范围返回 `false`。

例如：

```text
range A: rows 1..4, columns 1..3
range B: rows 3..6, columns 2..5
交集:   rows 3..4, columns 2..3
```

**边界：**

- 调用前应保证同一模型、同一父项；
- “挨着”不等于“重叠”；
- 无效范围不要用来推导业务交集；
- 它只判断几何范围，不检查业务对象内容是否相同。

### `QItemSelectionRange intersected(const QItemSelectionRange &other) const`

**作用：** 返回两个范围的矩形交集。

**关键语义：**

- 交集的上边界取两个 `top()` 的较大值；
- 下边界取两个 `bottom()` 的较小值；
- 左边界取两个 `left()` 的较大值；
- 右边界取两个 `right()` 的较小值；
- 没有交集时返回空或无效范围，应继续检查。

示例：

```cpp
const QItemSelectionRange common = first.intersected(second);

if (common.isValid() && !common.isEmpty()) {
    process(common);
}
```

**边界：**

- 两个范围应属于同一模型和共同父项；
- 交集结果仍然只是值对象，不会修改原范围；
- `intersected()` 不会把两个范围合并成更大范围；
- 交集几何有效不代表范围内存在可选择且启用的项目。

### `bool isValid() const`

**作用：** 判断范围的端点和几何关系是否构成有效范围。

**关键语义：**

有效范围至少应满足：

```text
topLeft 和 bottomRight 都有效
两个端点父项相同
top <= bottom
left <= right
```

**边界：**

- 它不等于“范围内至少有一个可选项目”；
- 合法但全禁用的范围仍可能 `isValid() == true`；
- 它不替代同模型前提的检查；
- 模型 reset 或端点项目删除后，原范围可能失效。

### `bool isEmpty() const`

**作用：** 判断范围是否没有可用的选择项目。

**关键语义：**

- 没有项目时为空；
- 范围内所有项目都禁用时为空；
- 范围内所有项目都不可选择时为空；
- 这个结果可能受模型 `flags()` 改变影响。

**边界：**

- `isEmpty()` 为 true 不一定表示几何范围无效；
- `isValid()` 为 true 也不保证 `isEmpty()` 为 false；
- 它不是简单的 `width() == 0 || height() == 0`；
- 如果模型在别处改变 flags，重新查询才能得到当前结果。

### `void swap(QItemSelectionRange &other) noexcept`

**作用：** 交换两个范围的内容。

**关键语义：**

- 交换两个范围的端点；
- 操作快速且不会失败；
- 不重新构造、不展开范围；
- 不修改模型，也不发出任何选择信号。

示例：

```cpp
range.swap(other);
```

**边界：**

- 交换后两个对象的有效性随内容一起交换；
- 之前保存的端点引用不要跨越交换继续使用；
- 它不是规范化或合并操作；
- 它不会改变 `QItemSelectionModel` 的状态。

### `bool operator==(const QItemSelectionRange &lhs, const QItemSelectionRange &rhs) noexcept`

**作用：** 判断两个范围是否完全相同。

**关键语义：**

- 比较两个范围的左上端点和右下端点；
- 端点相同表示行列边界、父项和索引身份相同；
- 可以用于测试、缓存键比较或避免重复更新。

```cpp
if (first == second) {
    // 两个范围的端点完全相同
}
```

**边界：**

- 这是范围值相等，不是“展开后列表恰好相同”的业务比较；
- 不同模型的同坐标不应被当作同一范围；
- 模型结构变化后持久索引状态变化，比较结果也可能变化；
- 比较无效范围时仍应按索引值语义理解。

### `bool operator!=(const QItemSelectionRange &lhs, const QItemSelectionRange &rhs) noexcept`

**作用：** 判断两个范围是否不同。

**关键语义：**

- 语义上等价于 `!(lhs == rhs)`；
- 可用于缓存失效和测试断言；
- 不会展开范围，也不访问范围内所有单元格。

**边界：**

- 不同端点即不同范围；
- 不等于“两个范围没有交集”；
- 两个不相等的范围仍然可能部分或完全重叠。

## 9. 常见组合写法

### 9.1 构造前规范化行列边界

如果起点和终点来自用户拖拽，不能假设拖拽方向永远是左上到右下：

```cpp
const int top = std::min(first.row(), last.row());
const int bottom = std::max(first.row(), last.row());
const int left = std::min(first.column(), last.column());
const int right = std::max(first.column(), last.column());

const QModelIndex topLeft = model->index(top, left, first.parent());
const QModelIndex bottomRight = model->index(bottom, right, first.parent());
const QItemSelectionRange range(topLeft, bottomRight);
```

前提是两个端点原本属于同一个模型和同一个父项。不同父项不能靠交换整数修正。

### 9.2 先判断交集，再展开

```cpp
if (!first.intersects(second)) {
    return;
}

const QItemSelectionRange common = first.intersected(second);
if (!common.isValid() || common.isEmpty()) {
    return;
}

for (const QModelIndex &index : common.indexes()) {
    process(index);
}
```

这样可以避免为完全不重叠的两个范围提前展开大量索引。

### 9.3 在 `QItemSelection` 中遍历范围

```cpp
const QItemSelection selection = selectionModel->selection();

for (const QItemSelectionRange &range : selection) {
    if (!range.isValid() || range.isEmpty()) {
        continue;
    }

    for (const QModelIndex &index : range.indexes()) {
        process(index);
    }
}
```

如果只需要知道范围大小、父节点或边界，不要调用 `indexes()`。

## 10. 常见误区

### 10.1 以为构造函数会自动排序端点

**现象：** 鼠标从右下拖到左上，构造出的范围无效。

**原因：** 构造函数直接保存 `topLeft` 和 `bottomRight`，不会自动取 min/max。

**处理：** 由调用方先规范化行列边界，再创建真正的左上和右下索引。

### 10.2 把无效范围当成根节点范围

**现象：** 默认构造范围被当成“根节点下的所有项目”。

**原因：** 无效 `QModelIndex()` 在 Qt 模型中常表示根层级，但两个无效端点并不构成一个有效选择矩形。

**处理：** 用 `QModelIndex()` 表示父项根层级，用 `QItemSelectionRange()` 表示空范围，二者不要混淆。

### 10.3 只看 `isValid()` 判断是否有可选内容

**现象：** 范围几何上有效，但选择操作没有效果。

**原因：** 范围内项目可能全部 disabled 或不可选择。

**处理：** 同时考虑 `isValid()`、`isEmpty()` 和模型 `flags()`。

### 10.4 把 `width() * height()` 当成可处理项目数

**现象：** 统计数量比实际可选择项目多。

**原因：** 几何尺寸不排除禁用项、不可选择项，也不替代 `indexes()` 的展开结果。

**处理：** 只需要矩形大小时用宽高；要处理实际索引时调用 `indexes()`。

### 10.5 把不同父项下的同号行拼成一个范围

**现象：** 树模型选择映射错到另一个分支。

**原因：** 行号只在同一个父项坐标空间内有意义。

**处理：** 每个父项创建独立范围，放到同一个 `QItemSelection` 中。

### 10.6 把 `contains()` 当跨模型校验

**现象：** 把另一个模型中相同坐标的索引传入，结果看起来像被包含。

**原因：** 范围判断围绕行、列和父索引坐标展开，调用方必须保证同一模型前提。

**处理：** 先检查 `index.model() == range.model()`，再调用 `contains()`。

### 10.7 把 `intersects()` 当“相邻也算重叠”

**现象：** 两个首尾相接的范围被错误合并。

**原因：** `intersects()` 判断的是闭区间真正有共同坐标，不是是否可以相邻拼接。

**处理：** 如果业务需要合并相邻范围，先实现明确的相邻判断，再使用 `QItemSelection::merge()` 等集合操作。

### 10.8 保存端点引用太久

**现象：** `topLeft()` 返回的引用在交换或对象销毁后继续使用。

**原因：** API 返回的是范围内部端点的 const 引用。

**处理：** 需要保存时复制成 `QPersistentModelIndex` 或 `QModelIndex`，并管理模型生命周期。

## API 速查表
| API | 类型 | 作用 | 使用重点 |
| --- | --- | --- | --- |
| `QItemSelectionRange()` | 构造函数 | 创建空范围 | `isValid()` 为 false；不要把默认宽高当真实尺寸 |
| `QItemSelectionRange(index)` | 构造函数 | 创建单个索引的 1×1 范围 | 索引应有效且属于目标模型 |
| `QItemSelectionRange(topLeft, bottomRight)` | 构造函数 | 创建闭区间矩形 | 同模型、同父项；调用方保证左上到右下 |
| `top()` | 边界查询 | 返回最上方行号 | 相对于共同父项；无效范围不要使用 |
| `left()` | 边界查询 | 返回最左侧列号 | 是模型列号，不是视图显示位置 |
| `bottom()` | 边界查询 | 返回最下方行号 | 闭区间包含该行 |
| `right()` | 边界查询 | 返回最右侧列号 | 闭区间包含该列 |
| `topLeft()` | 端点查询 | 返回左上持久索引 | 返回内部 const 引用；端点删除后可能失效 |
| `bottomRight()` | 端点查询 | 返回右下持久索引 | 与 `topLeft()` 一起确定矩形 |
| `parent()` | 关系查询 | 返回共同父索引 | 树模型坐标按它解释；无效表示根层级 |
| `model()` | 关系查询 | 返回端点所属模型 | 非拥有指针；空范围通常为 null |
| `width()` | 几何查询 | 返回覆盖列数 | 先检查 `isValid()`；不等于可选项目数 |
| `height()` | 几何查询 | 返回覆盖行数 | 先检查 `isValid()`；不等于 `indexes().size()` |
| `contains(index)` | 包含查询 | 判断索引是否在范围内 | 调用方保证同模型；比较行列和父项 |
| `contains(row, column, parent)` | 包含查询 | 判断坐标是否在范围内 | `parent` 必须属于同一坐标空间 |
| `indexes()` | 展开 | 返回范围内的 `QModelIndexList` | 大范围有展开成本；返回普通索引 |
| `intersects(other)` | 交集查询 | 判断两个范围是否重叠 | 同模型、同父项；相邻不等于重叠 |
| `intersected(other)` | 交集运算 | 返回两个范围的矩形交集 | 无交集后检查 `isValid()` / `isEmpty()` |
| `isValid()` | 状态查询 | 判断端点和几何关系是否合法 | 不保证范围内存在可选项目 |
| `isEmpty()` | 状态查询 | 判断没有可选且启用的项目 | 可能 valid 但 empty；受 `flags()` 影响 |
| `swap(other)` | 值操作 | 交换两个范围的内容 | `noexcept`、快速、不发信号、不做合并 |
| `operator==(lhs, rhs)` | 比较 | 判断端点是否完全相同 | 不等于是否无交集 |
| `operator!=(lhs, rhs)` | 比较 | 判断端点是否不同 | 语义上等价于 `!(lhs == rhs)` |

## 12. 一句话总结

`QItemSelectionRange` 是 Qt 模型选择中的“单个矩形值对象”：它用同一模型、同一父项下的左上和右下持久索引描述闭区间范围，用 `contains()` 判断坐标归属，用 `intersects()` / `intersected()` 做几何交集，用 `indexes()` 在需要时展开。实际使用时先保证同模型、同父项和正确端点顺序，再分别理解 `isValid()`、`isEmpty()` 与几何宽高。
