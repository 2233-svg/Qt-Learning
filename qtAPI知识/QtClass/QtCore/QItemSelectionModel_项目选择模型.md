# Qt QItemSelectionModel 项目选择模型深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QItemSelectionModel>`  
> 所属模块：`Qt6::Core`  
> 继承关系：`QObject -> QItemSelectionModel`  
> 相关类型：`QAbstractItemModel`、`QModelIndex`、`QItemSelection`、`QItemSelectionRange`

## 1. 它解决什么问题

`QItemSelectionModel` 是 Qt model/view 体系里专门保存“哪些项目被选中、哪个项目是当前项”的状态对象。它不保存业务数据，也不负责绘制选中高亮；它绑定到一个 `QAbstractItemModel`，用模型索引和选择范围描述当前选择状态，然后通过信号把变化通知给视图或业务代码。

可以把它放在这条链路里理解：

```text
QAbstractItemModel
        │ 提供 QModelIndex、flags、行列结构
        ▼
QItemSelectionModel
        │ 保存选择状态和 current index
        ▼
QTreeView / QTableView / QListView / 业务逻辑
```

它主要解决这些实际问题：

- 表格里单击一行、Ctrl 切换多行、Shift 扩展范围；
- 多个视图显示同一个模型，并共享同一组选中项；
- 树模型中记录不同父节点下的多个选择范围；
- 橡皮筋框选、键盘扩展选择等“当前交互选择”；
- 把按钮、菜单、快捷键和当前选择关联起来；
- 在选择变化时获得“新增选中”和“刚取消选中”的增量；
- 与代理模型配合，把代理侧选择映射回源模型处理。

它不是：

- `QAbstractItemModel`，不提供数据、行列数或角色数据；
- `QItemSelection`，不是单纯的范围值对象；
- 视图控件，不知道某一行是否可见、是否隐藏、如何绘制；
- current index 的同义词；
- 线程安全的跨线程选择容器；
- 用来长期保存业务对象身份的数据库。

最容易踩坑的一句话是：

> `QItemSelectionModel` 同时管理选择范围和 current index，但这两件事彼此独立。

## 2. 三个状态要分开看

`QItemSelectionModel` 的行为看起来复杂，主要是因为它内部至少涉及三种状态：

```text
已提交选择 committed selection
        +
当前交互选择 current selection
        =
外部查询看到的选择 selection()

另外还有一个独立状态：

currentIndex()
```

### 2.1 已提交选择

已提交选择是已经稳定进入选择集合的范围。例如用户 Ctrl 单击几行、程序调用 `select(index, Select)`，这些结果会成为普通选择的一部分。它们用 `QItemSelection` 保存，也就是若干个 `QItemSelectionRange`。

### 2.2 当前交互选择

当前交互选择用于描述还在进行中的一段选择动作，例如：

- 按住 Shift 从锚点扩展到另一行；
- 鼠标拖拽框选尚未结束；
- 视图正在根据键盘导航临时更新选择范围。

Qt 文档把这称为 two layer approach。外部的 `selectedIndexes()`、`selection()`、`isSelected()` 等查询会作用在这两层上，因此你通常不需要手动区分它们。

关键规则是 `Current` 标志：

- 命令里带 `QItemSelectionModel::Current`：更新当前交互选择；
- 命令里不带 `Current`：会创建新的当前选择，并把之前的当前选择加入整体选择。

这里的 `Current` 指的是 current selection layer，不是 `currentIndex()` 属性。

### 2.3 current index

`currentIndex()` 表示当前项，常用于键盘导航、焦点指示和视图里的“活动单元格”。它可以被选中，也可以不被选中。

常见例子：

```text
移动键盘焦点：currentIndex 改变，selection 可以不变
清空选择：selection 为空，currentIndex 可以仍然有效
程序选中一行：selection 改变，currentIndex 可以不变
```

改变 current index 的入口是 `setCurrentIndex()` 或视图内部导航，不是普通的 `select()`。

## 3. 构建与包含

### 3.1 CMake

`QItemSelectionModel` 属于 Core 模块：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

如果你在 Qt Widgets 视图里使用它，目标通常还会链接 Widgets：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Core Qt6::Widgets)
```

### 3.2 头文件

```cpp
#include <QItemSelectionModel>
```

这个头文件也让 `QItemSelection`、`QItemSelectionRange` 等相关选择类型可见。实际项目里也经常显式包含：

```cpp
#include <QItemSelection>
#include <QModelIndex>
```

## 4. 最小实际用法

下面的例子创建一个选择模型，监听选择增量，然后选中第 2 行：

```cpp
auto *selectionModel = new QItemSelectionModel(model, parent);

connect(selectionModel,
        &QItemSelectionModel::selectionChanged,
        receiver,
        [receiver](const QItemSelection &selected,
                   const QItemSelection &deselected) {
            receiver->handleSelectionDelta(selected, deselected);
        });

selectionModel->select(model->index(2, 0),
                       QItemSelectionModel::ClearAndSelect
                       | QItemSelectionModel::Rows);

selectionModel->setCurrentIndex(model->index(2, 0),
                                QItemSelectionModel::NoUpdate);
```

注意这里分成了两步：

- `select(..., ClearAndSelect | Rows)` 改变选中状态；
- `setCurrentIndex(..., NoUpdate)` 只移动当前项。

这样写能清楚表达“选中整行”和“让这一行成为当前焦点项”是两件事。

## 5. 与视图的关系

Qt item view 通常会自动创建或持有一个 selection model。也可以显式设置：

```cpp
auto *selectionModel = new QItemSelectionModel(model, parent);

view->setModel(model);
view->setSelectionModel(selectionModel);
```

多个视图可以共享同一个选择模型，前提是它们使用同一个模型：

```cpp
auto *selectionModel = new QItemSelectionModel(model, parent);

tableA->setModel(model);
tableB->setModel(model);

tableA->setSelectionModel(selectionModel);
tableB->setSelectionModel(selectionModel);
```

这样两个视图会共享选中项和 current index。一个视图里移动 current item，另一个视图也会看到同一个 current item。这正是“几个视图观察同一个模型”的典型用法。

不要把绑定源模型的选择模型直接塞给绑定代理模型的视图。`QModelIndex` 里包含所属模型指针，源模型索引和代理模型索引是两套坐标。需要跨代理处理选择时，用代理模型的选择映射函数：

```cpp
QItemSelection proxySelection = proxySelectionModel->selection();
QItemSelection sourceSelection = proxy->mapSelectionToSource(proxySelection);
```

反向也一样：

```cpp
QItemSelection proxySelection = proxy->mapSelectionFromSource(sourceSelection);
proxySelectionModel->select(proxySelection, QItemSelectionModel::ClearAndSelect);
```

## 6. 模型绑定与生命周期

### 6.1 它绑定一个模型

`QItemSelectionModel` 的所有索引、范围和查询都围绕 `model()` 返回的 `QAbstractItemModel` 展开。调用选择相关函数时，应保证传入的 `QModelIndex` 属于这个模型：

```cpp
Q_ASSERT(index.model() == selectionModel->model());
```

跨模型传索引不是“自动映射”，也不是可靠的 false 查询。它表示调用方把两套坐标混在了一起。

### 6.2 它不拥有模型数据

选择模型保存的是索引和范围，不拥有模型里的业务对象。模型结构变化后，选择模型会依赖模型的变更通知来更新内部状态。因此自定义模型必须正确发出：

- `beginInsertRows()` / `endInsertRows()`；
- `beginRemoveRows()` / `endRemoveRows()`；
- `beginMoveRows()` / `endMoveRows()`；
- `layoutAboutToBeChanged()` / `layoutChanged()`；
- `beginResetModel()` / `endResetModel()`。

如果模型偷偷改内部数据结构而不通知，选择模型、代理模型和视图都可能保留过期索引。

### 6.3 模型 reset 是特殊边界

模型 reset 代表模型内容整体失效。Qt 文档明确说明，模型 reset 时：

- `selectionChanged()` 不会按普通选择变化发出；
- `currentChanged()`、`currentRowChanged()`、`currentColumnChanged()` 也不会按普通 current 变化发出。

如果业务需要在 reset 后恢复选择，应监听模型自己的 `modelReset()`，根据稳定业务 ID 重新查找索引，再重新调用 `select()` 和 `setCurrentIndex()`。

### 6.4 更换模型

`setModel(newModel)` 会把选择模型切到另一个模型，并发出 `modelChanged(newModel)`。旧模型里的 `QModelIndex`、`QItemSelection` 和选择范围不能继续当作新模型的选择使用。

更换模型时最稳妥的做法是把旧选择当作失效状态处理：

```cpp
selectionModel->setModel(newModel);
selectionModel->clear();
```

是否需要额外 `clear()` 取决于具体逻辑，但不要假设旧索引能在新模型上复用。

## 7. `SelectionFlag` 和 `SelectionFlags`

`SelectionFlag` 描述一次选择命令如何改变状态，`SelectionFlags` 是 `QFlags<SelectionFlag>`，可以用按位或组合：

```cpp
selectionModel->select(index,
                       QItemSelectionModel::ClearAndSelect
                       | QItemSelectionModel::Rows);
```

### 7.1 基础动作

| 标志 | 值 | 语义 | 常见用途 |
| --- | --- | --- | --- |
| `NoUpdate` | `0x0000` | 不改变选择 | `setCurrentIndex(index, NoUpdate)` 只移动 current index |
| `Clear` | `0x0001` | 清空完整选择 | 通常和 `Select` 组合成替换选择 |
| `Select` | `0x0002` | 选中指定索引或范围 | 添加选中项 |
| `Deselect` | `0x0004` | 取消选中指定索引或范围 | 从现有选择里减去一块 |
| `Toggle` | `0x0008` | 已选中则取消，未选中则选中 | Ctrl 单击一行或一个单元格 |

`Select`、`Deselect`、`Toggle` 表示集合操作。它们通常只选一种；把多个动作标志硬凑在一起会让代码意图变差，也更容易和视图策略冲突。

### 7.2 当前交互层

| 标志 | 值 | 语义 | 常见用途 |
| --- | --- | --- | --- |
| `Current` | `0x0010` | 更新当前交互选择层 | Shift 扩展、拖拽框选等交互过程 |

再次强调：`Current` 不是 `currentIndex()` 的 setter。它不会把某个索引变成当前项；它控制选择模型内部的 current selection layer。要改变 `currentIndex()`，调用 `setCurrentIndex()`。

### 7.3 行列扩展

| 标志 | 值 | 语义 | 常见用途 |
| --- | --- | --- | --- |
| `Rows` | `0x0020` | 把给定索引或范围扩展到整行 | 表格行选择、列表行选择 |
| `Columns` | `0x0040` | 把给定索引或范围扩展到整列 | 表格列选择 |

在树模型里，“整行”或“整列”仍然是在同一个 `parent` 下扩展，不表示递归选中所有子孙节点。

### 7.4 便利组合

| 组合 | 展开 | 语义 |
| --- | --- | --- |
| `SelectCurrent` | `Select | Current` | 选中并更新当前交互选择 |
| `ToggleCurrent` | `Toggle | Current` | 切换并更新当前交互选择 |
| `ClearAndSelect` | `Clear | Select` | 清空旧选择后选中新范围 |

`ClearAndSelect` 不包含 `Current`。它常用于“替换当前选择”，例如单击表格某行时清除旧选择并选中新行。

## 8. 常见交互命令写法

### 8.1 单击一行

```cpp
const QModelIndex index = model->index(row, 0, parent);

selectionModel->select(index,
                       QItemSelectionModel::ClearAndSelect
                       | QItemSelectionModel::Rows);
selectionModel->setCurrentIndex(index, QItemSelectionModel::NoUpdate);
```

### 8.2 Ctrl 切换一行

```cpp
selectionModel->select(index,
                       QItemSelectionModel::Toggle
                       | QItemSelectionModel::Rows);
selectionModel->setCurrentIndex(index, QItemSelectionModel::NoUpdate);
```

### 8.3 Shift 扩展一段行选择

```cpp
QItemSelection range(anchor, index);

selectionModel->select(range,
                       QItemSelectionModel::ClearAndSelect
                       | QItemSelectionModel::Rows);
selectionModel->setCurrentIndex(index, QItemSelectionModel::NoUpdate);
```

视图内部的 Shift 选择通常还会使用 current selection layer。业务代码如果只是最终替换选择，`ClearAndSelect | Rows` 往往更直观。

### 8.4 只移动 current index

```cpp
selectionModel->setCurrentIndex(index, QItemSelectionModel::NoUpdate);
```

这不会选中 `index`。它适合键盘焦点、详情面板预览或让视图滚动到活动项。

## 9. 查询选择状态

### 9.1 `selectedIndexes()` 不是排序后的表格坐标

`selectedIndexes()` 返回所有选中的模型索引：

```cpp
const QModelIndexList indexes = selectionModel->selectedIndexes();
```

官方语义是：

- 结果不包含重复索引；
- 结果不保证排序；
- 结果是当前有效选择的展开形式；
- 大范围选择会展开成很多 `QModelIndex`，有时间和内存成本。

如果业务需要按行列处理，应自己排序或改用范围：

```cpp
QItemSelection ranges = selectionModel->selection();
```

### 9.2 `selectedRows(column)` 返回代表索引

`selectedRows(column)` 返回“整行都被选中”的那些行，并且每一行只返回一个位于 `column` 列的 `QModelIndex`：

```cpp
for (const QModelIndex &index : selectionModel->selectedRows(0)) {
    processRow(index.row());
}
```

参数 `column` 不是“只检查这一列是否被选中”，而是“结果里用哪一列的索引代表该行”。判断条件仍然是这一行的所有列都被选中。

### 9.3 `selectedColumns(row)` 返回代表索引

`selectedColumns(row)` 与 `selectedRows()` 对称：它返回“整列都被选中”的那些列，每一列用 `row` 行的索引表示。

```cpp
for (const QModelIndex &index : selectionModel->selectedColumns(0)) {
    processColumn(index.column());
}
```

参数 `row` 是结果代表行，不是只检查这一行。

### 9.4 整行、整列与交集查询

这四个函数很容易混：

```cpp
bool isRowSelected(int row, const QModelIndex &parent = QModelIndex()) const;
bool isColumnSelected(int column, const QModelIndex &parent = QModelIndex()) const;

bool rowIntersectsSelection(int row, const QModelIndex &parent = QModelIndex()) const;
bool columnIntersectsSelection(int column, const QModelIndex &parent = QModelIndex()) const;
```

区别是：

- `isRowSelected()` 要求该行全部可选择项都已选中；
- `isColumnSelected()` 要求该列全部可选择项都已选中；
- `rowIntersectsSelection()` 只要求该行至少有一个选中项；
- `columnIntersectsSelection()` 只要求该列至少有一个选中项。

官方文档特别说明，`isRowSelected()` 和 `isColumnSelected()` 会忽略不可选择项。也就是说，模型的 `flags()` 会影响“整行/整列是否全选”的判断。

`parent` 默认为无效 `QModelIndex()`，表示根层级。树模型里如果要检查某个父节点下的子行，必须传入那个父索引：

```cpp
if (selectionModel->isRowSelected(childRow, parentIndex)) {
    // parentIndex 下的 childRow 已整行选中
}
```

## 10. 信号语义

### 10.1 `selectionChanged(selected, deselected)` 是增量

`selectionChanged()` 的两个参数不是完整选择：

```cpp
void selectionChanged(const QItemSelection &selected,
                      const QItemSelection &deselected);
```

- `selected`：这次变化中新选中的范围；
- `deselected`：这次变化中刚取消选中的范围；
- 当前仍然保持选中的旧范围不会出现在 `selected` 里；
- 当前仍然未选中的范围不会出现在 `deselected` 里。

要拿完整选择，应在槽里查询：

```cpp
connect(selectionModel,
        &QItemSelectionModel::selectionChanged,
        receiver,
        [selectionModel](const QItemSelection &selected,
                         const QItemSelection &deselected) {
            const QItemSelection all = selectionModel->selection();
            Q_UNUSED(selected);
            Q_UNUSED(deselected);
            useCompleteSelection(all);
        });
```

模型布局变化时，如果被选中的项目仍然保持选中但索引坐标变化，信号可能带着空的 `selected` 和空的 `deselected` 发出。不要把“两个参数都空”简单理解成“什么都没发生”。

### 10.2 不要在直接连接的槽里修改模型

Qt 文档明确警告：不要在直接连接到 `selectionChanged()` 的槽里修改模型，例如调用 `setData()` 或做结构修改。

原因是这个信号可能发生在模型正处于删除行列、reset 或其它内部更新过程中。此时嵌套修改模型会让模型、代理模型和选择模型的内部映射处于未定义状态。

如果业务确实需要“选择变化后修改模型”，更稳妥的方式是把动作排到当前信号处理之后：

```cpp
connect(selectionModel,
        &QItemSelectionModel::selectionChanged,
        receiver,
        [receiver] {
            QMetaObject::invokeMethod(receiver,
                                      &Receiver::updateModelAfterSelection,
                                      Qt::QueuedConnection);
        });
```

这仍然要求你确认模型当时处于稳定状态，而不是简单把所有模型修改都塞进队列。

### 10.3 current 相关信号

`currentChanged(current, previous)` 在当前项变化时发出。

`currentRowChanged(current, previous)` 只在 current 的行发生变化时发出。

`currentColumnChanged(current, previous)` 只在 current 的列发生变化时发出。

这些信号也不会在模型 reset 时按普通变化发出。需要 reset 后重建 current item 的业务，应监听模型 reset，而不是等待 `currentChanged()`。

## 11. 属性语义

`QItemSelectionModel` 在元对象系统中公开这些属性：

| 属性 | 访问 | 通知 | 语义 |
| --- | --- | --- | --- |
| `model` | read/write/bindable | `modelChanged(QAbstractItemModel *)` | 当前绑定的模型 |
| `hasSelection` | read-only | `selectionChanged(...)` | 当前是否存在任何选中项 |
| `currentIndex` | read-only | `currentChanged(...)` | 当前项；没有当前项时为无效索引 |
| `selection` | read-only | `selectionChanged(...)` | 当前选择范围 |
| `selectedIndexes` | read-only | `selectionChanged(...)` | 当前选择展开后的索引列表 |

这些属性适合 QML、属性绑定或通用 QObject 反射场景。普通 C++ 代码通常直接调用成员函数更清楚。

`model` 属性提供 `bindableModel()`。Qt 6 C++ 属性绑定可以通过它观察或绑定当前模型指针。选择状态本身没有单独的 bindable 接口，主要通过信号通知。

## 12. 逐项 API 说明

### `enum SelectionFlag` / `SelectionFlags`

**作用：** 描述一次选择命令如何更新选择模型。

**关键语义：**

- `SelectionFlags` 是 `QFlags<SelectionFlag>`；
- `Select`、`Deselect`、`Toggle` 是选择集合操作；
- `Clear` 是清空修饰；
- `Current` 控制当前交互选择层；
- `Rows`、`Columns` 控制行列扩展；
- `SelectCurrent`、`ToggleCurrent`、`ClearAndSelect` 是便利组合。

**边界：**

- `Current` 不是 current index；
- `ClearAndSelect` 不包含 `Current`；
- 行列扩展发生在同一模型父项范围内；
- 命令应表达单一意图，不要随意组合互相冲突的动作标志。

### `QItemSelectionModel(QAbstractItemModel *model = nullptr)`

**作用：** 创建一个选择模型，并让它操作指定的 item model。

**关键语义：**

- `model` 可以为 `nullptr`；
- 没有模型时，选择相关操作没有实际数据坐标可用；
- 单参数构造适合选择模型生命周期跟随模型的常见场景；
- 选择模型仍然只是保存选择状态，不拥有模型里的业务数据。

**边界：**

- 模型销毁后不要继续使用指向旧模型的索引；
- 如果选择模型要跟随视图或控制器生命周期，优先使用带 `parent` 的重载；
- `QItemSelectionModel` 是 `QObject`，不可复制。

### `QItemSelectionModel(QAbstractItemModel *model, QObject *parent)`

**作用：** 创建一个操作 `model` 的选择模型，并指定 QObject 父对象。

**关键语义：**

- `parent` 管理选择模型本身的生命周期；
- `model` 决定选择模型使用哪套 `QModelIndex` 坐标；
- `parent` 不必等于 `model`，但二者生命周期要协调。

**边界：**

- 选择模型不会替你拥有或重建模型数据；
- 如果 `parent` 比 `model` 活得更久，要确保模型销毁前解除或更换绑定；
- 不要把一个选择模型同时用于不同模型的视图。

### `~QItemSelectionModel()`

**作用：** 销毁选择模型。

**关键语义：**

- 析构会释放选择模型内部保存的范围和连接；
- 不会删除它所操作的模型，除非那是 QObject 父子关系的反向生命周期结果；
- 视图如果还引用这个 selection model，应先换掉或随它一起销毁。

**边界：**

- 不要手动删除仍被视图使用的选择模型；
- 不要把它放进按值容器；QObject 子类不可复制。

### `QModelIndex currentIndex() const`

**作用：** 返回当前项索引。

**关键语义：**

- 没有当前项时返回无效 `QModelIndex`；
- current item 用于键盘导航和焦点指示；
- current item 可以未选中；
- current item 可以和选择变化分别通知。

**边界：**

- 返回的是普通 `QModelIndex`，结构变化后不要长期保存；
- 不要用它代表“所有选中项”；
- 模型 reset 时不会按普通 current 变化发信号。

### `bool isSelected(const QModelIndex &index) const`

**作用：** 判断指定索引当前是否被选中。

**关键语义：**

- 检查的是当前选择模型的选择状态；
- 查询会覆盖已提交选择和当前交互选择；
- `index` 应属于 `model()`。

**边界：**

- 无效索引通常返回 `false`；
- 跨模型索引不应传入；
- 它不替代 `model()->flags(index)` 的可选性判断。

### `bool isRowSelected(int row, const QModelIndex &parent = QModelIndex()) const`

**作用：** 判断某个父项下的指定行是否整行选中。

**关键语义：**

- `parent` 默认无效索引，表示根层级；
- 需要该行所有可选择项都处于选中状态；
- 不可选择项会被忽略；
- 通常比逐列调用 `isSelected()` 更高效。

**边界：**

- 树模型中必须传对父索引；
- `row` 越界时结果不应当成有效选择；
- 视图隐藏列不改变模型层面的列数量和 flags。

### `bool isColumnSelected(int column, const QModelIndex &parent = QModelIndex()) const`

**作用：** 判断某个父项下的指定列是否整列选中。

**关键语义：**

- 需要该列所有可选择项都处于选中状态；
- 不可选择项会被忽略；
- `parent` 控制树模型中的检查层级。

**边界：**

- `column` 是模型列号，不是视图显示位置；
- 代理模型排序或隐藏不自动映射到源模型坐标；
- 越界列通常不会得到有效的整列选中结果。

### `bool rowIntersectsSelection(int row, const QModelIndex &parent = QModelIndex()) const`

**作用：** 判断某行是否和当前选择有任何交集。

**关键语义：**

- 只要该行至少一个项目被选中就返回 `true`；
- 比 `isRowSelected()` 要求低；
- 适合判断行是否需要局部刷新或显示半选状态。

**边界：**

- `parent` 必须对应模型层级；
- 它不说明该行是否整行选中；
- 结果仍然基于选择模型绑定的模型。

### `bool columnIntersectsSelection(int column, const QModelIndex &parent = QModelIndex()) const`

**作用：** 判断某列是否和当前选择有任何交集。

**关键语义：**

- 只要该列至少一个项目被选中就返回 `true`；
- 比 `isColumnSelected()` 要求低；
- 适合列标题状态、统计或局部更新。

**边界：**

- `column` 是模型列号；
- 不代表整列已选中；
- 代理模型坐标要先映射。

### `bool hasSelection() const`

**作用：** 判断当前是否有任何选中项。

**关键语义：**

- 是 `hasSelection` 属性的读取函数；
- 可用于启用删除、复制、导出等依赖选择的动作；
- 状态变化由 `selectionChanged()` 通知。

**边界：**

- current index 有效不代表 `hasSelection()` 为 true；
- 模型 reset 后不要依赖普通选择信号更新业务状态；
- 如果动作依赖完整行，继续使用 `selectedRows()` 或 `isRowSelected()` 判断。

### `QModelIndexList selectedIndexes() const`

**作用：** 返回当前所有选中项的展开索引列表。

**关键语义：**

- 返回列表无重复；
- 返回列表不排序；
- 展开的是当前有效选择，包括当前交互选择层；
- 是 `selectedIndexes` 属性的 getter。

**边界：**

- 大范围选择会产生大量索引；
- 返回的普通索引不适合跨结构变化长期保存；
- 需要保留业务身份时，保存稳定 ID 或使用 `QPersistentModelIndex` 并确认模型正确维护它。

### `QModelIndexList selectedRows(int column = 0) const`

**作用：** 返回整行被选中的行，每行用指定列的索引表示。

**关键语义：**

- `column` 是结果代表列；
- 只有“所有列都被选中”的行才会返回；
- 返回值适合逐行执行业务操作。

**边界：**

- 不要把它理解成“返回 column 列所有选中项”；
- 如果只是某行一个单元格被选中，这一行不会出现在结果里；
- `column` 越界或在对应父项下无效时结果可能为空。

### `QModelIndexList selectedColumns(int row = 0) const`

**作用：** 返回整列被选中的列，每列用指定行的索引表示。

**关键语义：**

- `row` 是结果代表行；
- 只有“所有行都被选中”的列才会返回；
- 与 `selectedRows()` 对称。

**边界：**

- 不要把它理解成“返回 row 行所有选中项”；
- 如果只是某列一个单元格被选中，这一列不会出现在结果里；
- `row` 越界或在对应父项下无效时结果可能为空。

### `const QItemSelection selection() const`

**作用：** 返回选择模型保存的选择范围。

**关键语义：**

- 返回的是 `QItemSelection` 值；
- 比 `selectedIndexes()` 更适合表达大面积连续选择；
- 可用于代理模型的 `mapSelectionToSource()` / `mapSelectionFromSource()`；
- 修改返回值不会自动修改选择模型。

**边界：**

- 范围里的索引仍然依赖模型生命周期；
- 不要把源模型选择范围直接交给代理模型选择模型；
- 需要修改状态时调用 `select()`，不是改返回值。

### `QAbstractItemModel *model()`

**作用：** 返回选择模型当前操作的模型指针。

**关键语义：**

- 非 const 重载返回可修改模型指针；
- 可用于创建索引、读取 flags 或连接模型信号；
- 没有绑定模型时可能为 `nullptr`。

**边界：**

- 不要通过这个指针在 `selectionChanged()` 的直接连接槽里修改模型；
- 指针不表达所有权；
- 跨线程访问仍受 QObject 和模型规则限制。

### `const QAbstractItemModel *model() const`

**作用：** 在 const 上下文中返回当前模型指针。

**关键语义：**

- 适合只读查询；
- 返回值和非 const 重载指向同一个模型；
- 可用于校验 `index.model()`。

**边界：**

- 返回 `nullptr` 时不能继续调用模型成员；
- const 指针不意味着模型结构不会被其它代码改变。

### `QBindable<QAbstractItemModel *> bindableModel()`

**作用：** 返回 `model` 属性的 Qt 6 绑定接口。

**关键语义：**

- 用于 C++ 属性绑定系统；
- 观察或绑定的是模型指针本身；
- 模型指针变化仍会通过 `modelChanged()` 通知。

**边界：**

- 它不提供选择范围的绑定接口；
- 绑定模型指针不等于迁移旧选择；
- 更换模型后旧索引仍然不可复用。

### `void setModel(QAbstractItemModel *model)`

**作用：** 更换选择模型操作的 item model。

**关键语义：**

- 成功设置后发出 `modelChanged(model)`；
- 后续选择、查询和 current index 都围绕新模型；
- 旧模型索引与新模型索引不能混用。

**边界：**

- 更换模型是状态边界，业务通常需要清理或重建选择；
- 不要在多个不同模型之间复用同一批 `QModelIndex`；
- 如果视图已经设置模型，也要保证视图和选择模型指向同一个模型。

### `void setCurrentIndex(const QModelIndex &index, SelectionFlags command)`

**作用：** 设置当前项，并按命令可选地修改选择。

**关键语义：**

- 会让 `index` 成为 current item；
- current item 用于键盘导航和焦点指示；
- current item 与选中状态独立；
- 根据 `command`，该索引也可以进入选择；
- current 改变时发出 `currentChanged()`，行列变化时还会发出对应行列信号。

**边界：**

- `setCurrentIndex(index, NoUpdate)` 只移动 current index；
- 要同时选中，使用 `Select`、`ClearAndSelect`、`Toggle` 等命令；
- `index` 应属于当前模型；
- 传无效索引会让 current item 变为无效，语义上更清楚的写法是 `clearCurrentIndex()`。

### `void select(const QModelIndex &index, SelectionFlags command)`

**作用：** 按命令修改单个索引对应的选择状态。

**关键语义：**

- 是公开槽，也是重载函数；
- `Rows` 可以把这个索引扩展为整行；
- `Columns` 可以把这个索引扩展为整列；
- 选择变化时发出 `selectionChanged()`；
- 不负责改变 `currentIndex()`。

**边界：**

- 连接这个重载时要用 `qOverload` 或 lambda 指明签名；
- `index` 应属于当前模型；
- `ClearAndSelect` 常用于替换选择，但不会自动移动 current index。

重载连接写法：

```cpp
connect(sender,
        &SenderClass::signal,
        selectionModel,
        qOverload<const QModelIndex &,
                  QItemSelectionModel::SelectionFlags>(
            &QItemSelectionModel::select));
```

也可以用 lambda：

```cpp
connect(sender,
        &SenderClass::signal,
        selectionModel,
        [selectionModel](const QModelIndex &index,
                         QItemSelectionModel::SelectionFlags command) {
            selectionModel->select(index, command);
        });
```

### `void select(const QItemSelection &selection, SelectionFlags command)`

**作用：** 按命令修改一个范围选择。

**关键语义：**

- 用于矩形范围、多范围选择和代理选择映射结果；
- `QItemSelection` 可以包含多个 `QItemSelectionRange`；
- `Rows`、`Columns` 会对范围做行列扩展；
- 选择变化时发出 `selectionChanged()`；
- 不直接改变 `currentIndex()`。

**边界：**

- `selection` 里的索引应属于当前模型；
- 不要混入源模型和代理模型的范围；
- 大范围不会立刻变成业务对象列表，除非你调用 `selectedIndexes()` 或 `selection.indexes()` 展开。

重载连接写法：

```cpp
connect(sender,
        &SenderClass::signal,
        selectionModel,
        qOverload<const QItemSelection &,
                  QItemSelectionModel::SelectionFlags>(
            &QItemSelectionModel::select));
```

### `void clear()`

**作用：** 清空选择模型，包括选择和 current index。

**关键语义：**

- 清除所有选中项；
- 清除当前项；
- 发出 `selectionChanged()`；
- 发出 `currentChanged()`。

**边界：**

- 如果只想清选择，使用 `clearSelection()`；
- 如果只想清 current item，使用 `clearCurrentIndex()`；
- 相关行列 current 信号是否发出取决于 current 的行列是否发生变化。

### `void clearSelection()`

**作用：** 只清空选择状态。

**关键语义：**

- current index 保持不变；
- 发出 `selectionChanged()`；
- 适合“取消选中但保留焦点项”的交互。

**边界：**

- `hasSelection()` 会变为 false；
- `currentIndex()` 仍可能有效；
- 不要用它替代模型 reset。

### `void clearCurrentIndex()`

**作用：** 只清空 current index。

**关键语义：**

- 让 current item 变为无效；
- 发出 `currentChanged()`；
- 不清除已选中项。

**边界：**

- `hasSelection()` 可能仍为 true；
- 如果 UI 动作依赖选中项，不应只看 current index；
- 模型 reset 时不会通过这个信号路径通知你。

### `void reset()`

**作用：** 清空选择模型内部状态，但不发出任何信号。

**关键语义：**

- 清除选择；
- 清除 current index；
- 静默完成，不发 `selectionChanged()` 或 current 相关信号；
- 适合模型 reset 等内部同步场景。

**边界：**

- 业务代码通常不应把它当成“通知式清空”；
- 需要让外界响应清空时用 `clear()`；
- 调用后观察者不会自动收到状态变化信号。

### `void selectionChanged(const QItemSelection &selected, const QItemSelection &deselected)`

**作用：** 通知选择状态发生变化。

**关键语义：**

- `selected` 是本次新增选中的范围；
- `deselected` 是本次取消选中的范围；
- 参数是增量，不是完整选择；
- 是 `hasSelection`、`selection`、`selectedIndexes` 属性的通知信号。

**边界：**

- current index 改变不一定触发它；
- 模型 reset 时不会按普通选择变化触发；
- 直接连接槽里不要修改模型；
- 两个参数都空仍可能表示索引坐标变化等内部状态更新。

### `void currentChanged(const QModelIndex &current, const QModelIndex &previous)`

**作用：** 通知 current item 变化。

**关键语义：**

- `current` 是新的当前项；
- `previous` 是旧的当前项；
- 是 `currentIndex` 属性的通知信号；
- 只描述 current item，不描述完整选择。

**边界：**

- 选择变化不一定触发它；
- 模型 reset 时不会按普通变化触发；
- `current` 可能是无效索引。

### `void currentRowChanged(const QModelIndex &current, const QModelIndex &previous)`

**作用：** 通知 current item 的行发生变化。

**关键语义：**

- current item 变化且行号不同才发出；
- 适合按当前行刷新详情面板；
- 参数仍然是完整索引，不只是行号。

**边界：**

- 同一行不同列之间移动不会触发它；
- 模型 reset 时不会按普通变化触发；
- 树模型里同 row 不一定表示同一个父项下的业务对象，仍要看 `parent()`。

### `void currentColumnChanged(const QModelIndex &current, const QModelIndex &previous)`

**作用：** 通知 current item 的列发生变化。

**关键语义：**

- current item 变化且列号不同才发出；
- 适合按当前列更新工具栏、字段说明或编辑状态；
- 参数是 `QModelIndex`。

**边界：**

- 同一列不同行之间移动不会触发它；
- 代理模型坐标和源模型坐标不同；
- 模型 reset 时不会按普通变化触发。

### `void modelChanged(QAbstractItemModel *model)`

**作用：** 通知选择模型绑定的模型已经被设置。

**关键语义：**

- 由 `setModel()` 成功设置模型后发出；
- `model` 是新的模型指针；
- 是 `model` 属性的通知信号。

**边界：**

- 它不表示模型数据内容变化；
- 模型内容变化应监听 `QAbstractItemModel` 自身的信号；
- 更换模型后旧选择需要按业务规则重建。

### `QItemSelectionModel(QItemSelectionModelPrivate &dd, QAbstractItemModel *model)`

**作用：** 受保护构造函数，用于 Qt 内部 d-pointer 扩展。

**关键语义：**

- 需要 `QItemSelectionModelPrivate`；
- 普通业务子类通常不会也不应该调用它；
- 外部代码使用公开构造函数即可。

**边界：**

- `QItemSelectionModelPrivate` 是私有实现类型；
- 依赖它会把代码绑到 Qt 内部实现细节；
- 自定义选择行为通常通过组合或重写公开虚函数完成。

### `void emitSelectionChanged(const QItemSelection &newSelection, const QItemSelection &oldSelection)`

**作用：** 受保护辅助函数，比较新旧完整选择并发出增量 `selectionChanged()`。

**关键语义：**

- 参数是完整的新选择和旧选择；
- 函数会计算新增和取消的范围；
- 发出的信号参数顺序是 `selected, deselected`；
- 适合派生类维护自定义选择状态后复用 Qt 的差异计算。

**边界：**

- 不要把 `selected`、`deselected` 两个增量直接当作 `newSelection`、`oldSelection` 传入；
- 如果新旧选择相同，不应期待有实际变化通知；
- 派生类仍需维护基类选择模型契约。

## 13. 常见误区

### 13.1 把 `Current` 当成 current index

**现象：** 调用 `select(index, SelectCurrent)` 后，以为 `currentIndex()` 一定变成了 `index`。

**原因：** `Current` 控制的是当前交互选择层，不是 current item。

**处理：** 需要移动 current item 时显式调用 `setCurrentIndex()`。

### 13.2 把 `selectionChanged()` 参数当完整选择

**现象：** 选中第二行后，槽里只处理 `selected`，结果忘了第一行仍然选中。

**原因：** `selected` 和 `deselected` 是增量。

**处理：** 增量用于局部更新；完整状态用 `selection()` 或 `selectedIndexes()` 查询。

### 13.3 在选择变化槽里直接改模型

**现象：** 删除行、过滤代理或 reset 时偶发崩溃、选择错乱、代理映射断言。

**原因：** `selectionChanged()` 可能在模型更新过程中发出，直接嵌套修改模型会破坏内部状态。

**处理：** 直接槽里只记录意图或更新非模型 UI；必须改模型时排队到之后，并确保模型已经稳定。

### 13.4 混用源模型索引和代理模型索引

**现象：** 选中代理视图第 3 行，却操作了源模型另一行。

**原因：** 代理模型排序、过滤后，代理坐标不等于源模型坐标。

**处理：** 使用 `mapToSource()`、`mapFromSource()`、`mapSelectionToSource()`、`mapSelectionFromSource()`。

### 13.5 用 `selectedRows()` 查“某列被选中的项”

**现象：** 只选了某一列的几个单元格，`selectedRows(column)` 返回为空。

**原因：** `selectedRows(column)` 查询整行选择，只是用 `column` 作为结果代表列。

**处理：** 单元格选择用 `selectedIndexes()` 或 `selection()`；整行选择才用 `selectedRows()`。

### 13.6 清空选择后还看到焦点项

**现象：** 调用 `clearSelection()` 后，视图里仍有一个虚线框或当前项。

**原因：** current index 和 selection 是独立状态。

**处理：** 如果要全部清掉，用 `clear()`；如果只想清 current，用 `clearCurrentIndex()`。

### 13.7 依赖 `selectedIndexes()` 的顺序

**现象：** 多范围选择后，处理顺序和用户看到的行列顺序不一致。

**原因：** 官方语义只保证无重复，不保证排序。

**处理：** 需要顺序时按 `parent`、`row`、`column` 自己排序，或在范围层面处理。

### 13.8 模型 reset 后等不到清空信号

**现象：** reset 模型后按钮状态没有更新，因为没收到 `selectionChanged()`。

**原因：** Qt 明确说明模型 reset 不按普通 selection/current 变化发信号。

**处理：** 同时监听模型的 `modelReset()`，在 reset 后重新同步 UI 状态。

## API 速查表
| API | 类型 | 作用 | 使用重点 |
| --- | --- | --- | --- |
| `SelectionFlag` | 枚举 | 描述一次选择命令 | 区分集合动作、`Current` 交互层、行列扩展 |
| `SelectionFlags` | flags | 保存多个 `SelectionFlag` 的按位或组合 | 常用 `ClearAndSelect | Rows`、`Toggle | Rows` |
| `NoUpdate` | 枚举值 | 不改变选择 | 配合 `setCurrentIndex()` 可只移动 current item |
| `Clear` | 枚举值 | 清空完整选择 | 通常与 `Select` 组合 |
| `Select` | 枚举值 | 选中指定索引或范围 | 不自动移动 current index |
| `Deselect` | 枚举值 | 取消选中指定索引或范围 | 用于从选择中减去一块 |
| `Toggle` | 枚举值 | 切换指定索引或范围 | 常用于 Ctrl 单击 |
| `Current` | 枚举值 | 更新当前交互选择层 | 不是 `currentIndex()` setter |
| `Rows` | 枚举值 | 扩展到整行 | 树模型中只在同一父项下扩展 |
| `Columns` | 枚举值 | 扩展到整列 | 使用模型列号，不是视图显示位置 |
| `SelectCurrent` | 便利组合 | `Select | Current` | 选中并更新当前交互层 |
| `ToggleCurrent` | 便利组合 | `Toggle | Current` | 切换并更新当前交互层 |
| `ClearAndSelect` | 便利组合 | `Clear | Select` | 替换当前选择；不包含 `Current` |
| `QItemSelectionModel(model)` | 构造函数 | 创建操作指定模型的选择模型 | `model` 可为空；选择坐标来自该模型 |
| `QItemSelectionModel(model, parent)` | 构造函数 | 创建选择模型并指定父对象 | 生命周期和模型绑定要协调 |
| `~QItemSelectionModel()` | 析构函数 | 销毁选择模型 | 不要让视图继续引用已销毁对象 |
| `model` 属性 | 属性 | 当前绑定的模型 | read/write/bindable；通知 `modelChanged()` |
| `hasSelection` 属性 | 属性 | 是否有选中项 | read-only；通知 `selectionChanged()` |
| `currentIndex` 属性 | 属性 | 当前项 | read-only；通知 `currentChanged()` |
| `selection` 属性 | 属性 | 当前选择范围 | read-only；返回范围值 |
| `selectedIndexes` 属性 | 属性 | 当前选择展开后的索引 | read-only；无重复但不排序 |
| `currentIndex()` | 查询 | 返回 current item | 无当前项时无效；独立于选择 |
| `isSelected(index)` | 查询 | 判断索引是否被选中 | `index` 应属于当前模型 |
| `isRowSelected(row, parent)` | 查询 | 判断整行是否选中 | 忽略不可选择项；树模型传对 parent |
| `isColumnSelected(column, parent)` | 查询 | 判断整列是否选中 | 忽略不可选择项；使用模型列号 |
| `rowIntersectsSelection(row, parent)` | 查询 | 判断行是否有任意交集 | 不代表整行选中 |
| `columnIntersectsSelection(column, parent)` | 查询 | 判断列是否有任意交集 | 不代表整列选中 |
| `hasSelection()` | 查询 | 是否存在选中项 | current index 有效不代表有选择 |
| `selectedIndexes()` | 查询 | 返回全部选中索引 | 无重复、不排序；大范围有展开成本 |
| `selectedRows(column)` | 查询 | 返回整行选中的行代表索引 | `column` 是代表列，不是检查列 |
| `selectedColumns(row)` | 查询 | 返回整列选中的列代表索引 | `row` 是代表行，不是检查行 |
| `selection()` | 查询 | 返回选择范围 | 修改返回值不会修改选择模型 |
| `model()` | 查询 | 返回当前模型指针 | 可能为 null；指针不表达所有权 |
| `model() const` | 查询 | const 上下文返回模型指针 | 用于只读校验和查询 |
| `bindableModel()` | 绑定 | 返回 `model` 属性绑定接口 | 只绑定模型指针，不迁移旧选择 |
| `setModel(model)` | 设置 | 更换当前模型 | 发 `modelChanged()`；旧索引不可复用 |
| `setCurrentIndex(index, command)` | 槽 | 设置 current item，并可按命令修改选择 | `NoUpdate` 只移动 current；索引应属当前模型 |
| `select(index, command)` | 槽 | 修改单个索引的选择状态 | 重载槽连接要指定签名；不改 current index |
| `select(selection, command)` | 槽 | 修改范围选择状态 | 适合多范围和代理选择映射 |
| `clear()` | 槽 | 清空选择和 current index | 发 `selectionChanged()` 与 `currentChanged()` |
| `clearSelection()` | 槽 | 只清空选择 | current index 保持不变 |
| `clearCurrentIndex()` | 槽 | 只清空 current index | 选择保持不变 |
| `reset()` | 槽 | 静默清空内部状态 | 不发任何信号 |
| `selectionChanged(selected, deselected)` | 信号 | 选择变化增量通知 | 参数不是完整选择；直接槽里不要改模型 |
| `currentChanged(current, previous)` | 信号 | current item 变化 | 模型 reset 时不按普通变化发出 |
| `currentRowChanged(current, previous)` | 信号 | current 行变化 | 同行换列不触发 |
| `currentColumnChanged(current, previous)` | 信号 | current 列变化 | 同列换行不触发 |
| `modelChanged(model)` | 信号 | 当前模型改变 | 不表示模型数据内容变化 |
| `QItemSelectionModel(dd, model)` | 受保护构造 | Qt 私有实现扩展入口 | 普通业务代码不要依赖 |
| `emitSelectionChanged(newSelection, oldSelection)` | 受保护函数 | 比较新旧完整选择并发出增量信号 | 参数是完整选择，不是增量 |

## 15. 一句话总结

`QItemSelectionModel` 是绑定到 `QAbstractItemModel` 的选择状态机：它用 `QItemSelection` 范围保存已提交选择和当前交互选择，用 `currentIndex()` 单独记录焦点项，并通过 `SelectionFlags` 精确表达清空、选中、取消、切换、行列扩展等操作。使用时最重要的是别混淆 `Current` 与 `currentIndex`，别把 `selectionChanged()` 的增量当完整选择，也别把源模型和代理模型索引混在一起。
