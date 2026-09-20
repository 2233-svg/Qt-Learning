# QStringListModel：把 QStringList 暴露为可编辑的一列模型

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStringListModel>`  
> CMake：`Qt6::Core`  
> 基类：`QAbstractListModel`

`QStringListModel` 是 Qt Model/View 体系中最轻量的字符串列表模型。它把一个 `QStringList`
包装成“一列、多行”的 item model，让 `QListView`、`QComboBox`、代理模型、拖放和委托编辑器能
通过标准模型接口读取、编辑、插入、删除、移动和排序字符串。

它解决的问题不是“怎样保存字符串”，而是“怎样把字符串列表用视图能理解的协议暴露出来”。如果
只在普通算法里处理数据，用 `QStringList` 足够；如果数据要进入视图、选择模型或代理模型，就应
使用模型类。

## 基本使用场景

```cpp
#include <QStringListModel>

auto *model = new QStringListModel(parent);
model->setStringList({"Debug", "Info", "Warning", "Error"});

listView->setModel(model);
comboBox->setModel(model);
```

模型默认只有一列，行数等于内部字符串数量。每个字符串主要通过 `Qt::DisplayRole` 和
`Qt::EditRole` 暴露；视图显示用前者，编辑器提交通常用后者。

适合它的场景包括：可编辑的名称列表、简单下拉项、标签白名单、路径列表编辑器、设置页里的
单列选项。不适合它的场景包括：每项有图标、状态、颜色、多字段、树结构、异步加载或复杂角色。
这些情况应使用自定义 `QAbstractListModel` 或更通用的 item model。

## 数据所有权与通知

构造函数和 `setStringList()` 都把传入的 `QStringList` 作为模型内部数据来保存。之后修改原来的
列表不会自动影响模型：

```cpp
QStringList values = {"A", "B"};
QStringListModel model(values);

values << "C";                 // 模型仍只有 A、B
model.setStringList(values);    // 这样才会更新模型并通知视图
```

反过来，`stringList()` 返回的是当前内部列表的一个值副本。修改这个副本也不会影响模型，除非再
调用 `setStringList()` 或使用 `setData()`、`insertRows()`、`removeRows()` 等模型 API。

这条边界很重要：视图只响应模型发出的 `dataChanged`、`rowsInserted`、`rowsRemoved`、
`modelReset` 等通知。绕过模型协议改内部数据，视图不会知道。

## 行、列与索引

`QStringListModel` 是 list model：

- 顶层行数等于字符串数量。
- 列数按 `QAbstractListModel` 的约定是 1。
- 对有效父索引调用 `rowCount(parent)` 返回 0，因为它没有子项。
- `sibling(row, column, idx)` 只在一列模型的范围内给出同级索引；超出列范围会得到无效索引。

读取数据的常见流程：

```cpp
QModelIndex index = model.index(row, 0);
QString text = model.data(index, Qt::DisplayRole).toString();
```

无效索引请求 `data()` 会返回无效 `QVariant`。调用方不要把它当作空字符串的同义词；空字符串是
有效值，无效 variant 表示索引或角色不可用。

## 角色与编辑

`data(index, role)` 对显示和编辑角色返回字符串。其他角色通常返回无效 variant。

`setData(index, value, role)` 用于修改指定项。典型角色是 `Qt::EditRole`；编辑成功时模型会发出
`dataChanged()`，并返回 `true`。如果索引无效、角色不支持或值无法作为字符串使用，则返回
`false`。

```cpp
QModelIndex idx = model.index(1, 0);
if (!model.setData(idx, "Release", Qt::EditRole))
    qWarning("Edit failed");
```

`itemData(index)` / `setItemData(index, roles)` 是一次读写多个角色的通用接口。对这个模型来说，
有意义的仍主要是显示和编辑角色。若 `roles` 同时包含 `Qt::DisplayRole` 与 `Qt::EditRole`，
文档说明 `EditRole` 优先。

`clearItemData(index)` 清除该项数据。在单字符串模型里，可以把它理解为把该行回到空文本或清空
角色数据的模型操作；具体是否成功仍取决于索引有效性。

## flags、拖放与可编辑性

有效项的 flags 包含 enabled、selectable、editable、drag enabled 和 drop enabled。也就是说，
视图默认可以选择、编辑、拖动这些项，并在模型支持的范围内接收放置。

`supportedDropActions()` 返回该模型支持的拖放动作。实际拖放行为还会受视图的 drag/drop 设置、
MIME 数据和默认 `QAbstractItemModel` 行插入逻辑影响。若应用需要复杂拖放语义，例如带额外字段
或跨模型转换，应实现自己的模型。

无效索引的 flags 通常用于表示可在顶层放置数据。不要用 `flags()` 判断某个行号是否存在；行号
有效性应通过 `index()`、`rowCount()` 或 `QModelIndex::isValid()` 判断。

## 插入、删除与移动

`insertRows(row, count, parent)` 在给定位置插入若干空字符串。`parent` 参数只是为匹配
`QAbstractItemModel` 接口存在；对一列顶层列表通常传默认无效索引。成功时模型会按标准协议通知
视图。

```cpp
int row = model.rowCount();
if (model.insertRows(row, 1)) {
    QModelIndex idx = model.index(row, 0);
    model.setData(idx, "New Item", Qt::EditRole);
}
```

`removeRows(row, count, parent)` 删除连续行。`moveRows(sourceParent, sourceRow, count,
destinationParent, destinationChild)` 移动连续行块，适合让视图或业务逻辑重新排序已有项。

这些函数会维护模型索引和通知；不要先取出 `stringList()`、手工改副本、再期望视图保留选择或
持久索引。整表替换可以用 `setStringList()`，小范围变化优先用行操作和 `setData()`。

## 排序

`sort(column, order)` 对内部字符串排序，并通知视图。因为模型只有一列，`column` 应为 0；其他列
没有数据意义。`order` 控制升序或降序。

如果需要大小写不敏感、locale-aware、自然排序或稳定保留某些分组，`QStringListModel` 的默认
排序通常不够。更常见的做法是在其上接 `QSortFilterProxyModel`，或使用自定义模型暴露排序 key。

## 生命周期与线程归属

`QStringListModel` 是 `QObject`，遵守对象树和线程亲和性规则：

- 可指定 `parent`，由父对象负责销毁。
- 不可复制。
- 应在所属线程访问它，尤其是已经连接到视图时通常属于 GUI 线程。
- 从工作线程产生新列表时，把 `QStringList` 通过 queued signal 传回模型所属线程，再调用
  `setStringList()` 或行操作。
- 视图持有的是模型指针；销毁模型前应确保视图不再使用，或让父对象生命周期自然覆盖视图。

模型里的 `QStringList` 仍是隐式共享值，但模型对象本身不是无锁并发容器。

## 常见错误

### 修改 `stringList()` 的返回值后以为模型更新了

返回的是副本。要更新模型，调用 `setStringList()` 或模型的编辑 API。

### 直接替换全部列表来做小改动

`setStringList()` 会通知底层数据变化，可能让选择、展开状态或持久索引受到更大影响。单行改动用
`setData()`，增删用 `insertRows()` / `removeRows()`。

### 在工作线程直接操作连接到视图的模型

模型和视图通常都在 GUI 线程。跨线程更新应发信号，把数据交回模型线程。

### 期望它保存多个角色的复杂数据

`QStringListModel` 主要就是字符串。图标、颜色、ID、校验状态等应使用自定义模型或其他 item
model。

### 把无效 `QVariant` 当成空字符串

无效 variant 表示索引或角色不可用；空字符串是一个有效的显示值。

### 忘记检查行操作返回值

越界插入、删除或移动会失败。之后使用索引前，先确认操作返回 `true`。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QStringListModel(QObject *parent = nullptr)` | 创建空的一列字符串模型 | `QObject` 生命周期；parent 可接管销毁。 |
| `QStringListModel(const QStringList &, QObject *)` | 用现有字符串初始化模型 | 保存为模型数据；之后原列表变化不会自动同步。 |
| `rowCount(parent) const` | 返回行数 | 有效父索引下返回 0；顶层行数等于字符串数量。 |
| `sibling(row, column, idx) const` | 返回同级索引 | 一列模型中只有 column 0 有实际意义。 |
| `data(index, role) const` | 读取某行某角色数据 | 显示/编辑角色返回字符串；无效索引返回无效 variant。 |
| `setData(index, value, role)` | 修改某行数据 | 成功会发 `dataChanged()`；通常使用 `Qt::EditRole`。 |
| `clearItemData(index)` | 清除某项角色数据 | Qt 6.0 起；成功与否取决于有效索引和模型规则。 |
| `flags(index) const` | 返回项能力 | 有效项可用、可选、可编辑、可拖放。 |
| `insertRows(row, count, parent)` | 插入连续空行 | 用模型通知协议更新视图；成功返回 `true`。 |
| `removeRows(row, count, parent)` | 删除连续行 | 越界会失败；成功时视图收到删除通知。 |
| `moveRows(sourceParent, sourceRow, count, destinationParent, destinationChild)` | 移动连续行块 | 适合重排；参数必须描述有效、非冲突的范围。 |
| `itemData(index) const` | 读取一项的角色映射 | 对此模型主要是显示/编辑相关角色。 |
| `setItemData(index, roles)` | 一次设置多个角色 | 同时给 DisplayRole/EditRole 时 EditRole 优先。 |
| `sort(column, order)` | 排序内部字符串 | 只有 column 0 有意义；复杂排序用代理或自定义模型。 |
| `stringList() const` | 返回内部字符串列表副本 | 修改副本不会影响模型。 |
| `setStringList(strings)` | 整体替换模型数据 | 会通知视图底层数据变化；小改动优先用精细 API。 |
| `supportedDropActions() const` | 返回可接受的 drop 动作 | 还需视图和 MIME 机制配合。 |

一句话总结：`QStringListModel` 是把简单字符串数组接入 Model/View 的桥；只要需求超出“一列可编辑
字符串”，就该切换到更明确的数据模型。
