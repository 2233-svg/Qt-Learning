# Qt QModelIndex 模型位置句柄笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QModelIndex>`  
> 所属模块：`Qt6::Core`  
> 类型性质：指向模型中一个行列位置的轻量值对象  
> 相关类型：`QAbstractItemModel`、`QPersistentModelIndex`、`QModelRoleData`、`QModelRoleDataSpan`

## 1. 它解决什么问题

`QModelIndex` 是 Qt Model/View 架构里连接“位置”和“模型”的句柄。它不保存一份数据，而是告诉视图、代理模型、委托或业务代码：

```text
哪个模型
  +
哪个父节点下的第几行、第几列
  +
模型实现用来找回真实节点的 internal id 或 pointer
```

模型通常返回 `QModelIndex`：

```cpp
QModelIndex index(int row, int column,
                  const QModelIndex &parent = {}) const override;
```

调用方再用这个索引：

- 读取某个角色的 `data()`；
- 查询可编辑、可选中等 `flags()`；
- 找到父索引或兄弟索引；
- 把索引交给视图、选择模型、代理模型和拖放 API；
- 在调试时检查模型拓扑是否一致。

它解决的是“同一个模型可能是树、表或列表，但上层需要统一表示一个位置”的问题。

## 2. 它不是什么

`QModelIndex` 不是：

- 真实业务节点对象；
- 节点数据的副本；
- 自动拥有模型或节点的智能指针；
- 只凭 `row()` 和 `column()` 就能全局定位的坐标；
- 结构变化后必然继续指向原项目的持久句柄；
- 可以由业务代码任意填写 row、column、pointer 的公开构造对象。

`QModelIndex` 的真正身份由四部分共同决定：

```text
row + column + internalId + model
```

同一个 `(row, column)` 在不同父索引或不同模型下是不同位置。只保存行列而丢掉 `model()` 和父链，不能恢复原索引。

## 3. 创建索引：业务代码不要自己伪造

`QModelIndex` 的默认构造函数是公开的，但带 row、column、internal pointer/id 的构造函数是私有的，只有 `QAbstractItemModel` 能调用。模型实现应通过：

```cpp
return createIndex(row, column, nodePointer);
```

或：

```cpp
return createIndex(row, column, nodeId);
```

调用方应从：

```cpp
model->index(row, column, parent)
```

取得索引，而不是写出类似“自己拼接索引”的代码。

### 3.1 pointer 和 id 是两种不同协议

模型创建索引时可以把一个 `const void *` 或 `quintptr` 交给 `createIndex()`。二者的含义由模型自己约定：

- 指针模式：`internalPointer()` 可以取回模型创建时传入的地址；
- 整数模式：`internalId()` 可以取回模型创建时传入的整数；
- 一个模型应保持自己的约定一致；
- 不要把整数 ID 再强行当成真实对象指针；
- 不要把一个模型的 internal pointer 传给另一个模型解释。

例如：

```cpp
QModelIndex MyModel::index(int row, int column,
                           const QModelIndex &parent) const
{
    Node *node = childNode(parent, row);
    return node ? createIndex(row, column, node) : QModelIndex();
}
```

对应地，模型内部可以使用：

```cpp
auto *node = static_cast<Node *>(index.internalPointer());
```

但这只有在 `index` 确实来自当前模型、模型约定使用 pointer 模式、且 node 生命周期仍由模型保证时才成立。

## 4. 无效索引与有效索引

### 4.1 默认构造是无效索引

```cpp
QModelIndex invalid;
Q_ASSERT(!invalid.isValid());
Q_ASSERT(invalid.row() == -1);
Q_ASSERT(invalid.column() == -1);
Q_ASSERT(invalid.model() == nullptr);
```

空的 `QModelIndex` 常用于：

- 表示根节点的 parent；
- 表示查找失败；
- 表示没有选中项目；
- 表示模型不提供某个兄弟或父位置。

### 4.2 `isValid()` 的判断非常基础

Qt 6.11.1 头文件中的判断等价于：

```cpp
row >= 0 && column >= 0 && model() != nullptr
```

因此 `isValid()` 只说明索引对象携带了非负行列和模型指针，不保证：

- row 仍小于当前 `rowCount(parent)`；
- column 仍小于当前 `columnCount(parent)`；
- internal pointer 仍指向存活节点；
- 索引仍指向业务上原来的项目；
- 父子关系没有被模型实现破坏。

模型实现需要更强检查时使用：

```cpp
Q_ASSERT(checkIndex(index));
```

`checkIndex()` 属于 `QAbstractItemModel`，不是 `QModelIndex` 自己的方法。

### 4.3 无效索引上的成员函数

无效索引调用这些函数时通常得到空或无效结果：

- `data()` 返回空 `QVariant`；
- `flags()` 返回空 `Qt::ItemFlags`；
- `parent()` 返回无效索引；
- `sibling()`、`siblingAtRow()`、`siblingAtColumn()` 返回无效索引；
- `multiData()` 不向任何模型请求数据；
- `model()` 返回 `nullptr`。

不要把这些“安全的空返回”理解成无效索引可以参与正常模型逻辑。需要操作项目时，先判断 `isValid()`。

## 5. 模型结构变化和索引生命周期

### 5.1 普通 `QModelIndex` 适合短期使用

普通索引通常用于一次调用链或一次事件处理：

```cpp
void Controller::activate(const QModelIndex &index)
{
    if (!index.isValid())
        return;

    const QVariant value = index.data(Qt::DisplayRole);
    // 立即处理 value。
}
```

插入、删除、移动、reset、排序和布局调整都可能改变索引语义。视图会根据模型发出的 begin/end、layout 和 reset 通知更新自身，但调用方保存的一份普通 `QModelIndex` 不会自动变成长期稳定的业务引用。

### 5.2 需要跨变化保存时使用 `QPersistentModelIndex`

```cpp
QPersistentModelIndex saved = index;
```

`QPersistentModelIndex` 是专门用于跨模型变化追踪的类型，但它也不是万能的节点所有权对象：

- 模型销毁后它不能继续提供有效项目；
- 模型必须正确发出结构和布局变化通知；
- reset 或项目删除后它可能变为无效；
- 维护成本和存储成本都高于普通 `QModelIndex`；
- 如果只需要在当前函数里读一次数据，不要为了“保险”到处使用 persistent index。

经验规则：

```text
当前调用栈/当前事件 -> QModelIndex
跨排序、移动或布局变化保存选择项 -> QPersistentModelIndex
跨模型重建、跨进程或长期业务身份 -> 自己的稳定业务 ID
```

## 6. 最小使用场景

### 6.1 读取展示文本和编辑能力

```cpp
void inspectIndex(const QModelIndex &index)
{
    if (!index.isValid())
        return;

    const QString text = index.data(Qt::DisplayRole).toString();
    const bool editable =
        index.flags().testFlag(Qt::ItemIsEditable);

    qDebug() << index.row()
             << index.column()
             << text
             << editable;
}
```

`data()` 和 `flags()` 都会委托给 `index.model()`。索引只负责把当前索引传回模型，并不缓存这些结果。

### 6.2 从子项回到父项

```cpp
for (QModelIndex current = index;
     current.isValid();
     current = current.parent()) {
    qDebug() << current.data(Qt::DisplayRole);
}
```

顶层项目的 `parent()` 通常返回无效索引，表示它位于模型根下。树模型必须保证 `parent(child)` 与 `index(row, column, parent)` 的关系互相一致。

### 6.3 获取同一父节点下的兄弟

```cpp
const QModelIndex sameRow =
    index.siblingAtColumn(0);
const QModelIndex sameColumn =
    index.siblingAtRow(index.row() + 1);
```

兄弟索引仍属于同一模型和同一父节点。目标行列不存在时，模型应返回无效索引。

## 7. 逐项 API 语义

### 7.1 `QModelIndex()`

```cpp
constexpr QModelIndex() noexcept;
```

构造无效索引。row 和 column 为 `-1`，internal id 为 `0`，model 为 `nullptr`。它不表示模型根对象本身，而是 Qt 模型 API 里常用的“无父索引/无结果”哨兵。

### 7.2 `row() const`

```cpp
constexpr int row() const noexcept;
```

返回索引在其父项中的行号。对默认无效索引返回 `-1`。

行号不是全局项目编号，也不保证结构变化后仍代表原项目。处理树模型时必须把它和 `parent()`、`model()` 一起理解。

### 7.3 `column() const`

```cpp
constexpr int column() const noexcept;
```

返回索引在其父项中的列号。对默认无效索引返回 `-1`。

列表模型通常只有第 `0` 列；表模型有多个列；树模型可能在每个节点下继续拥有多个列。不要只根据类名猜测列数，应查询模型。

### 7.4 `internalId() const`

```cpp
constexpr quintptr internalId() const noexcept;
```

返回模型创建索引时保存的整数 ID。它是 `quintptr`，适合承载模型设计的整数句柄、数组位置或压缩节点标识。

边界：

- `0` 不等于索引无效；有效索引完全可以使用 ID `0`；
- 如果模型采用 pointer 模式，返回值只是指针位模式，不应按业务整数解释；
- ID 的生命周期、复用和唯一性由模型负责；
- 不要把不同模型的 ID 放进同一个全局命名空间而忘记保存 model。

### 7.5 `internalPointer() const`

```cpp
void *internalPointer() const noexcept;
```

返回模型创建索引时保存的内部指针位模式。它通常用于树模型从索引找回节点对象：

```cpp
Node *node = static_cast<Node *>(index.internalPointer());
```

边界：

- 只对使用 pointer 模式创建的索引有实际指针语义；
- 返回的是非 const `void *`，但不代表模型允许调用方修改节点；
- 不要把它当作所有权指针；
- 不要在模型已销毁或节点已释放后解引用；
- 如果模型使用整数 ID，应该读取 `internalId()`，不要把返回值强转成对象指针。

### 7.6 `constInternalPointer() const`

```cpp
const void *constInternalPointer() const noexcept;
```

返回同一 internal storage 的只读指针形式。它适合只读取模型私有节点：

```cpp
const Node *node =
    static_cast<const Node *>(index.constInternalPointer());
```

它仍然不提供生命周期保证，也不会验证 pointer 类型。`const` 只限制通过该表达式进行的访问，不会把一个本来错误的 internal pointer 变成安全指针。

### 7.7 `model() const`

```cpp
const QAbstractItemModel *model() const noexcept;
```

返回产生该索引的模型指针。返回值是借用指针，`QModelIndex` 不拥有模型，也不会阻止模型析构。

常见用途：

```cpp
if (index.model() == expectedModel)
    useIndex(index);
```

不要把两个来自不同模型、但 row 和 column 相同的索引当成同一个位置。

### 7.8 `isValid() const`

```cpp
constexpr bool isValid() const noexcept;
```

判断索引是否携带非负 row、非负 column 和非空 model。它是快速的结构性判断，不会向模型查询当前边界，也不会检查 internal pointer 指向的对象。

### 7.9 `data(int role) const`

```cpp
QVariant data(int role = Qt::DisplayRole) const;
```

把当前索引和 role 交给模型的 `data(index, role)`。默认 role 是 `Qt::DisplayRole`：

```cpp
const QVariant display = index.data();
const QVariant edit = index.data(Qt::EditRole);
```

语义边界：

- 无效索引返回空 `QVariant`；
- 具体角色是否有数据由模型决定；
- 返回空 QVariant 不一定表示模型出错，也可能是该角色没有值；
- `data()` 不缓存结果，连续调用可能重新计算；
- 如果需要区分“空值”和“没有该角色”，要结合模型协议或自定义 role 处理。

### 7.10 `multiData(QModelRoleDataSpan roleDataSpan) const`

```cpp
void multiData(QModelRoleDataSpan roleDataSpan) const;
```

一次向模型请求多个 role 的数据。传入的 span 指向调用方拥有的 `QModelRoleData` 存储：

```cpp
QModelRoleData roles[] = {
    QModelRoleData(Qt::DisplayRole),
    QModelRoleData(Qt::DecorationRole),
    QModelRoleData(Qt::CheckStateRole)
};

index.multiData(roles);

qDebug() << roles[0].data()
         << roles[1].data()
         << roles[2].data();
```

注意：

- span 不拥有数组，数组必须覆盖调用期间；
- role data 的顺序和 role 值由数组元素自身表达；
- 无效索引调用不会填充模型数据；
- 这是给模型批量实现优化的入口，不能假定每个模型都比多次 `data()` 更快；
- 不要传入已经销毁或长度错误的 span。

### 7.11 `flags() const`

```cpp
Qt::ItemFlags flags() const;
```

把当前索引交给模型的 `flags(index)`，用于判断启用、可选中、可编辑、可拖拽、可放置等能力：

```cpp
if (index.flags().testFlag(Qt::ItemIsEnabled) &&
    index.flags().testFlag(Qt::ItemIsSelectable)) {
    // 可以作为可交互项目处理
}
```

无效索引返回空 flags。flags 是当前模型状态的查询结果，不是永久能力；模型权限、编辑状态或数据结构变化后都可能改变。

### 7.12 `parent() const`

```cpp
QModelIndex parent() const;
```

调用模型的 `parent(*this)` 返回父索引。无效索引没有父项，直接返回无效索引。

常见边界：

- 根下的顶层项目通常返回无效父索引；
- 父模型必须返回属于自己的索引；
- `parent(child)` 必须和 `index(row, column, parent)` 的树关系保持一致；
- 模型实现不一致会导致视图展开、选择和拖放行为异常。

### 7.13 `sibling(int row, int column) const`

```cpp
QModelIndex sibling(int row, int column) const;
```

请求与当前索引共享同一父项的目标 row/column。若目标就是当前 row/column，Qt 直接返回当前索引；否则调用模型的 `sibling()`。

当前索引无效时返回无效索引。目标位置不存在时，模型也应返回无效索引。

### 7.14 `siblingAtColumn(int column) const`

```cpp
QModelIndex siblingAtColumn(int column) const;
```

保留当前行和父项，只替换 column。它是：

```cpp
index.sibling(index.row(), column);
```

的方便入口，并在目标 column 与当前 column 相同且索引有效时直接返回当前索引。

### 7.15 `siblingAtRow(int row) const`

```cpp
QModelIndex siblingAtRow(int row) const;
```

保留当前 column 和父项，只替换 row。它是：

```cpp
index.sibling(row, index.column());
```

的方便入口。不能跨父项寻找“相同 row 的项目”，父项关系由当前 index 隐含保留。

## 8. 比较、哈希和列表类型

### 8.1 比较按完整索引身份进行

Qt 6.11.1 为 `QModelIndex` 提供强排序和相等比较支持。比较不能只理解为 row/column 比较，模型和 internal id 也属于索引身份：

```cpp
if (left == right) {
    // 同一个模型、同一位置和同一 internal storage
}
```

两个模型都返回 `(0, 0)` 的索引不会因此相等。排序可用于有序容器，但不应把排序顺序误解成模型中的视觉顺序。

### 8.2 `qHash(const QModelIndex &, size_t seed)`

```cpp
size_t qHash(const QModelIndex &index,
             size_t seed = 0) noexcept;
```

允许把 `QModelIndex` 放入哈希容器或做去重。哈希包含 row、column 和 internal id；使用索引作为 key 时仍应把模型归属纳入业务设计，因为模型指针和业务身份不可被忽略。

普通索引作为哈希 key 的边界：

- 模型结构变化后，索引是否仍指向同一业务项目要重新确认；
- 模型销毁后，不要继续使用保存的索引 key；
- 需要长期保存选择状态时优先考虑 `QPersistentModelIndex` 或业务 ID。

### 8.3 `QModelIndexList`

```cpp
using QModelIndexList = QList<QModelIndex>;
```

它只是索引值的 Qt 列表别名，用于选择、多选、拖放和模型匹配 API。列表复制的是轻量索引对象，不会复制模型数据，也不会自动把普通索引升级成 persistent index。

## 9. 一个模型实现中的完整形状

下面是 pointer 模式树模型的简化轮廓：

```cpp
QModelIndex TreeModel::index(int row, int column,
                             const QModelIndex &parent) const
{
    if (column < 0 || column >= columnCount(parent))
        return {};

    Node *parentNode = nodeFromIndex(parent);
    Node *child = parentNode->child(row);
    return child ? createIndex(row, column, child) : QModelIndex();
}

QModelIndex TreeModel::parent(const QModelIndex &child) const
{
    if (!child.isValid())
        return {};

    const Node *node = nodeFromIndex(child);
    const Node *parentNode = node ? node->parent() : nullptr;
    if (!parentNode || parentNode == m_root)
        return {};

    return createIndex(parentNode->row(), 0, parentNode);
}

QVariant TreeModel::data(const QModelIndex &index, int role) const
{
    if (!checkIndex(index, CheckIndexOption::IndexIsValid))
        return {};

    const Node *node = nodeFromIndex(index);
    if (role == Qt::DisplayRole)
        return node->text(index.column());
    return {};
}
```

这里最重要的不是具体 Node 类型，而是协议必须闭合：

```text
index() 能创建的索引
    -> parent() 能找回正确父项
    -> data()/flags() 能解释同一个索引
    -> 结构变化时 begin/end 通知能维护索引关系
```

## 10. 常见错误

### 10.1 只保存 row 和 column

**问题：** 多个父节点或多个模型下的相同行列被当成同一项目。

**处理：** 始终保留完整 `QModelIndex`；需要业务身份时另存业务 ID。

### 10.2 把 `isValid()` 当成“节点仍存在”

**问题：** 删除或 reset 后继续通过旧索引访问 internal pointer。

**处理：** 依靠正确模型通知、重新取得索引，或使用 `QPersistentModelIndex`；调试模型时使用 `checkIndex()`。

### 10.3 无论模型约定都读取 `internalPointer()`

**问题：** ID 模式下把整数位模式解释成对象指针。

**处理：** 模型使用 pointer 模式才读取 `internalPointer()`，使用 ID 模式就读取 `internalId()`。

### 10.4 试图从业务代码直接构造有效索引

**问题：** 无法访问私有构造函数，或者绕过模型创建非法索引。

**处理：** 调用 `model->index()`；模型子类内部使用受保护的 `createIndex()`。

### 10.5 把 `data()` 的空 QVariant 当成异常

**问题：** 某个 role 没有数据时误报错误。

**处理：** 先明确 role 协议；空值可能就是合法业务值。

### 10.6 把 `multiData()` 的 span 当成拥有数据

**问题：** 传入局部或越界的角色数据内存。

**处理：** 让 `QModelRoleData` 数组覆盖完整调用；span 只借用，不拥有。

### 10.7 用普通索引跨 reset 保存选择

**问题：** reset 后旧索引不再代表原项目。

**处理：** reset 前后按业务 ID 重新定位，或在模型能支持时使用 persistent index。

### 10.8 误解 sibling 的范围

**问题：** 用 `siblingAtRow()` 试图切换到另一个父节点下的项目。

**处理：** sibling 只在当前索引的同一父项下寻找位置；跨父项要从目标 parent 重新调用 `model->index()`。

## API 速查表
### 11.1 基本状态和模型归属

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QModelIndex()` | 构造无效索引 | 常用作根 parent、失败结果和空哨兵 |
| `row()` | 返回父项中的行号 | 无效索引为 `-1`；不是全局行号 |
| `column()` | 返回父项中的列号 | 无效索引为 `-1`；列表模型通常为 0 |
| `model()` | 返回所属模型借用指针 | 不拥有模型；不同模型的相同行列不是同一位置 |
| `isValid()` | 做基础有效性判断 | 不检查当前边界、节点存活或父子拓扑 |
| `internalId()` | 读取模型保存的整数句柄 | ID `0` 也可能是有效索引；与 pointer 模式区分 |
| `internalPointer()` | 读取模型保存的 pointer 位模式 | 只按模型约定解释；不拥有节点 |
| `constInternalPointer()` | 以只读形式读取内部 pointer | const 不提供生命周期保证 |

### 11.2 数据和导航

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `data(int role = Qt::DisplayRole)` | 读取当前索引的角色数据 | 无效索引返回空 QVariant；空值不一定是错误 |
| `multiData(QModelRoleDataSpan)` | 批量读取多个角色 | span 借用调用方数组；数组必须在调用期间有效 |
| `flags()` | 查询启用、选择、编辑、拖放等项目能力 | 无效索引返回空 flags；结果随模型状态变化 |
| `parent()` | 返回当前项目的父索引 | 顶层项目通常返回无效索引 |
| `sibling(int row, int column)` | 在同一父项下查找目标位置 | 不能跨父项；目标不存在应返回无效索引 |
| `siblingAtRow(int row)` | 保留列和父项，切换行 | 只在当前父项下查找 |
| `siblingAtColumn(int column)` | 保留行和父项，切换列 | 只在当前父项下查找 |

### 11.3 相关非成员和类型

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `operator==` / `operator!=` | 比较完整索引身份 | 不只是比较 row/column；模型和 internal storage 也重要 |
| 三向比较 | 为有序比较提供强排序 | 排序顺序不是模型视觉顺序 |
| `qHash(const QModelIndex &, size_t)` | 计算哈希 | 模型变化或销毁后不要无条件继续使用旧 key |
| `QModelIndexList` | `QList<QModelIndex>` 别名 | 只复制轻量索引，不复制模型数据 |
| `QPersistentModelIndex` | 跨模型变化追踪索引 | 仍依赖模型通知；不是节点所有权或永久业务 ID |

## 12. 一句话总结

`QModelIndex` 是模型返回的轻量位置句柄：它把模型、父项中的行列和模型私有的 internal id/pointer 绑定在一起，负责把视图和业务代码带回模型。使用时不要自己伪造有效索引，不要把 `isValid()` 当成节点仍存活，也不要用普通索引跨结构变化长期保存；需要批量角色读取用 `multiData()`，需要持久追踪再考虑 `QPersistentModelIndex` 或业务 ID。
