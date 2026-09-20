# Qt QPersistentModelIndex 可持久追踪模型索引笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPersistentModelIndex>`  
> 所属模块：`Qt6::Core`  
> 类型性质：在模型变化通知下追踪位置的值对象  
> 相关类型：`QModelIndex`、`QAbstractItemModel`、`QModelRoleData`、`QModelRoleDataSpan`

## 1. 它解决什么问题

普通 `QModelIndex` 适合当前调用链中的临时访问，但模型插入、删除、移动、排序或布局变化后，保存下来的普通索引可能不再代表原项目。`QPersistentModelIndex` 为这种场景提供一个由模型维护的追踪句柄：

```text
当前 QModelIndex
        |
        v
QPersistentModelIndex
        |
        +-- 模型移动项目时更新 row/column/parent
        +-- 项目删除或模型 reset 后变为无效
        +-- 仍可读取 data、flags、parent 等信息
```

典型使用场景：

- 排序后仍要保留当前选中项目；
- 异步任务完成后回到模型定位原先项目；
- 布局重排后恢复展开项、焦点项或编辑项；
- 在多个事件循环回调之间保存模型中的某个位置；
- 维护 `QItemSelectionModel` 或复杂视图状态时保存少量稳定索引。

它不是让项目本身永生，而是让模型在**正确发出结构变化通知并维护持久索引**时，有机会把同一个跟踪记录更新到新的位置。

## 2. 它不是什么

`QPersistentModelIndex` 不是：

- 真实节点对象；
- 节点数据的副本；
- 模型或节点的所有权指针；
- 即使模型不发通知也能自动修复的魔法句柄；
- 跨模型、跨进程或跨数据库的业务主键；
- 保证项目永远存在的引用。

正确的身份边界是：

```text
QPersistentModelIndex -> 依附一个具体 QAbstractItemModel
业务 ID              -> 由应用自己定义和持久化
```

如果模型 reset、删除项目或模型销毁，persistent index 也可能失效。需要跨模型重建仍能找回对象时，应该保存业务 ID，再通过模型自己的查找逻辑重新取得索引。

## 3. 从普通索引创建

```cpp
QModelIndex current = model->index(row, column, parent);
QPersistentModelIndex saved(current);
```

如果 `current` 无效，得到的 persistent index 也表示无效位置：

```cpp
QPersistentModelIndex saved;
if (saved.isValid()) {
    // 才能把它作为当前模型项目使用
}
```

创建 persistent index 会让模型开始跟踪这条索引记录。不要为了所有临时读取都创建它；它比普通 `QModelIndex` 有额外的跟踪和维护成本。

## 4. 模型必须配合维护

### 4.1 插入、删除和移动要用 begin/end 协议

模型实现应使用对应的结构变化通知：

```cpp
beginInsertRows(parent, first, last);
// 修改底层数据
endInsertRows();
```

删除和移动同理：

```cpp
beginMoveRows(sourceParent, sourceFirst, sourceLast,
              destinationParent, destinationRow);
// 移动底层数据
endMoveRows();
```

这些 begin/end API 不只是通知视图，也给 Qt 更新 persistent index、选择状态和代理映射提供了时机。

### 4.2 排序和重排要维护旧位置到新位置

如果同一批项目仍然存在，但 row 顺序改变，应使用布局变化协议，并在需要时调用：

```cpp
changePersistentIndex(oldIndex, newIndex);
```

批量重排可以使用：

```cpp
changePersistentIndexList(oldIndexes, newIndexes);
```

`from` 和 `to` 必须按位置一一对应。只发 `layoutChanged()` 而不更新持久索引，可能导致保存的索引落到错误项目。

### 4.3 reset 通常结束旧索引语义

`beginResetModel()` / `endResetModel()` 表示模型整体状态被重建。reset 后不要假设旧 persistent index 还能代表原项目；通用做法是：

1. reset 前保存业务 ID；
2. 执行模型 reset；
3. 根据业务 ID 重新查询新索引。

## 5. 与 `QModelIndex` 的分工

| 场景 | 推荐类型 | 原因 |
| --- | --- | --- |
| 当前函数内读取 data | `QModelIndex` | 轻量、直接、不会建立持久跟踪 |
| 当前事件处理结束前暂存 | `QModelIndex` | 只要模型不会在使用前发生不兼容变化即可 |
| 排序、移动或布局变化后恢复选中项 | `QPersistentModelIndex` | 让模型有机会更新位置 |
| 模型 reset 后仍定位同一业务对象 | 业务 ID | persistent index 不跨整体重建保证身份 |
| 跨线程传递并在另一线程直接访问模型 | 两者都不自动安全 | 模型线程归属和同步协议仍由调用方负责 |

转换为普通索引：

```cpp
QModelIndex current = saved;
if (current.isValid())
    qDebug() << current.data(Qt::DisplayRole);
```

转换不会复制节点数据。它只是取得 persistent record 当前对应的普通索引快照。

## 6. 默认状态和失效

### 6.1 默认构造是无效 persistent index

```cpp
QPersistentModelIndex invalid;
Q_ASSERT(!invalid.isValid());
Q_ASSERT(invalid.model() == nullptr);
```

默认对象没有跟踪任何模型位置，可以安全地作为成员的初始状态。

### 6.2 失效不等于对象析构

项目被删除、模型 reset 或模型销毁后，persistent index 对象本身仍可存在，但：

```cpp
saved.isValid() == false
```

此时不要继续把 `row()`、`column()`、`internalPointer()` 或 `data()` 当作原项目的信息。先检查有效性，再决定是否重新定位。

### 6.3 `isValid()` 仍然不是业务存在性证明

只要模型仍报告该 persistent record 对应位置有效，`isValid()` 才为 true。它不保证：

- 你的业务对象没有被替换；
- internal pointer 指向的具体节点地址没有变化；
- 数据仍满足你之前缓存的业务条件；
- 这个索引属于你当前想操作的代理模型而不是源模型。

需要模型内部拓扑检查时，仍应使用对应模型的 `checkIndex()` 或重新调用模型查询。

## 7. 实际使用场景

### 7.1 排序后恢复当前项目

```cpp
QPersistentModelIndex selected = selectionModel->currentIndex();
const QString key = selected.data(Qt::UserRole).toString();

model->sort(0, Qt::AscendingOrder);

if (selected.isValid()) {
    selectionModel->setCurrentIndex(
        selected,
        QItemSelectionModel::Current
        | QItemSelectionModel::Select);
} else {
    // 如果模型重建了索引，按 key 重新查找。
    const QModelIndex replacement = model->findByKey(key);
    selectionModel->setCurrentIndex(
        replacement,
        QItemSelectionModel::Current);
}
```

是否能直接依赖 `selected`，取决于模型排序实现是否正确维护 persistent index。保存 `key` 是更稳妥的业务兜底。

### 7.2 异步回调中的短期追踪

```cpp
QPersistentModelIndex target = model->index(row, 0, parent);

QTimer::singleShot(0, model, [target] {
    if (!target.isValid())
        return;

    qDebug() << target.data(Qt::DisplayRole);
});
```

这里 persistent index 解决的是回调之间模型结构可能变化的问题，但它没有解决线程安全问题。回调仍应在模型所属线程执行，或者通过模型线程的 queued 调用访问。

### 7.3 保存多个展开项

```cpp
QList<QPersistentModelIndex> expanded;
for (const QModelIndex &index : expandedIndexes)
    expanded.append(index);
```

当模型发生布局变化时，模型正确维护 persistent index 后，可以重新把仍有效的条目交给视图。项目删除或 reset 后，要清理无效条目。

## 8. 逐项 API 语义

### 8.1 `QPersistentModelIndex()`

```cpp
QPersistentModelIndex();
```

构造不跟踪任何位置的无效对象。它适合成员变量默认初始化和表示“当前没有持久项目”。

### 8.2 `QPersistentModelIndex(const QModelIndex &index)`

```cpp
QPersistentModelIndex(const QModelIndex &index);
```

从普通索引创建持久跟踪记录。源索引所属模型决定跟踪对象；源索引无效时得到无效 persistent index。

它不会复制模型数据，也不会获得模型所有权。

### 8.3 `QPersistentModelIndex(const QPersistentModelIndex &other)`

```cpp
QPersistentModelIndex(const QPersistentModelIndex &other);
```

复制另一个 persistent handle。两个对象跟踪同一个模型位置记录；一个副本析构不会让另一个副本停止跟踪。

复制的是跟踪关系，不是节点内容快照。模型变化后两个副本仍应观察同一个更新后的持久位置。

### 8.4 `~QPersistentModelIndex()`

```cpp
~QPersistentModelIndex();
```

销毁当前持久 handle，并释放它对内部跟踪记录的引用。它不会删除模型项目，也不会调用模型的删除 API。

### 8.5 `QPersistentModelIndex(QPersistentModelIndex &&other)`

```cpp
QPersistentModelIndex(QPersistentModelIndex &&other) noexcept;
```

移动内部跟踪记录。Qt 6.11.1 的头文件实现通过交换内部指针完成移动，因此 moved-from 对象处于空的无效状态。

### 8.6 `operator=(const QPersistentModelIndex &other)`

```cpp
QPersistentModelIndex &operator=(
    const QPersistentModelIndex &other);
```

让当前对象改为跟踪 `other` 所跟踪的位置。当前对象原先的跟踪关系被释放或替换，但不会删除原项目。

### 8.7 `operator=(QPersistentModelIndex &&other)`

```cpp
QPersistentModelIndex &operator=(
    QPersistentModelIndex &&other) noexcept;
```

移动替换当前跟踪关系。移动后的 `other` 处于可析构但不再跟踪有效位置的状态。

### 8.8 `operator=(const QModelIndex &other)`

```cpp
QPersistentModelIndex &operator=(
    const QModelIndex &other);
```

让当前 persistent index 改为跟踪普通索引指定的位置。传入无效普通索引会清空当前跟踪关系。

### 8.9 `swap(QPersistentModelIndex &other)`

```cpp
void swap(QPersistentModelIndex &other) noexcept;
```

交换两个 persistent handle 的内部跟踪记录。它不移动模型项目，不改变模型结构，也不创建新的跟踪目标。

### 8.10 `operator QModelIndex() const`

```cpp
operator QModelIndex() const;
```

取得当前持久记录对应的普通索引：

```cpp
QModelIndex current = persistent;
```

如果 persistent index 已失效，转换结果是无效 `QModelIndex`。转换得到的是当前状态，不是脱离模型的快照。

### 8.11 `row() const`

```cpp
int row() const;
```

返回当前持久位置在父项中的行号。索引失效时不要把返回值当成有效项目位置。

### 8.12 `column() const`

```cpp
int column() const;
```

返回当前持久位置的列号。它仍然是相对于当前父项的列，不是模型全局列。

### 8.13 `internalId() const`

```cpp
quintptr internalId() const;
```

返回当前持久位置对应的模型 internal id。它的含义完全由模型的 `createIndex()` 约定决定；不要把 ID 当作跨模型通用业务身份。

### 8.14 `internalPointer() const`

```cpp
void *internalPointer() const;
```

返回当前持久位置的 internal pointer 表示。只有模型使用 pointer 模式并且索引有效时，调用方才有理由按模型约定解释它。

它不拥有节点，也不会阻止节点释放。persistent 解决的是位置跟踪，不是节点内存管理。

### 8.15 `constInternalPointer() const`

```cpp
const void *constInternalPointer() const;
```

以只读形式取得当前 internal pointer。`const` 不改变 pointer 的生命周期和类型约定。

### 8.16 `model() const`

```cpp
const QAbstractItemModel *model() const;
```

返回当前 persistent index 所属模型的借用指针。对象不拥有模型；模型销毁后 persistent index 会失效。

### 8.17 `isValid() const`

```cpp
bool isValid() const;
```

判断当前持久记录是否仍代表一个有效模型位置。项目删除、模型 reset 或模型销毁后通常变为 false。

它不表示业务对象仍满足某个条件，也不替代对目标模型和父子关系的检查。

### 8.18 `parent() const`

```cpp
QModelIndex parent() const;
```

返回当前持久位置的父项，但返回类型是普通 `QModelIndex`。如果当前对象无效或已位于根下，通常返回无效索引。

返回的普通父索引只适合当前使用；如果要继续跨变化保存父项，应再构造一个 `QPersistentModelIndex`。

### 8.19 `sibling(int row, int column) const`

```cpp
QModelIndex sibling(int row, int column) const;
```

在当前持久位置的同一父项下请求目标行列，返回普通 `QModelIndex`。它不返回 persistent sibling；需要持久保存时显式构造：

```cpp
QPersistentModelIndex persistentSibling(
    persistent.sibling(targetRow, targetColumn));
```

当前对象无效或目标不存在时返回无效索引。

### 8.20 `data(int role) const`

```cpp
QVariant data(int role = Qt::DisplayRole) const;
```

读取当前持久位置的模型角色数据。它会以当前追踪到的普通索引向模型请求数据：

```cpp
if (persistent.isValid())
    qDebug() << persistent.data(Qt::DisplayRole);
```

无效对象返回空 `QVariant`。返回值不被 persistent index 缓存。

### 8.21 `multiData(QModelRoleDataSpan roleDataSpan) const`

```cpp
void multiData(QModelRoleDataSpan roleDataSpan) const;
```

以当前持久位置向模型批量请求多个角色。span 的数组生命周期仍由调用方负责：

```cpp
QModelRoleData roles[] = {
    QModelRoleData(Qt::DisplayRole),
    QModelRoleData(Qt::EditRole)
};

persistent.multiData(roles);
```

对象无效时不要期待数组被填充；如果模型可能在异步期间删除项目，调用前先检查 `isValid()`。

### 8.22 `flags() const`

```cpp
Qt::ItemFlags flags() const;
```

读取当前持久位置的项目 flags。它反映当前模型状态，不是创建 persistent index 时的永久快照。

### 8.23 `operator==`、`operator!=` 和三向比较

Qt 6.11.1 默认兼容配置下提供 persistent index 的相等和强排序比较，也提供与 `QModelIndex` 的比较重载。头文件使用 `QT_CORE_REMOVED_SINCE(6, 8)` 控制部分旧式成员运算符，因此启用更高版本移除宏时，旧的 `operator<`/`operator==` 成员形式可能不可用；应优先使用当前 Qt 支持的比较表达式和 `compareThreeWay` 体系。

比较的重点是跟踪记录身份，而不是简单比较当前 row/column：

```cpp
if (saved == currentIndex) {
    // 表示两者指向同一个持久位置
}
```

比较不同模型的相同行列不会得到“同一个项目”。

### 8.24 `qHash(const QPersistentModelIndex &, size_t)`

```cpp
size_t qHash(const QPersistentModelIndex &index,
             size_t seed = 0) noexcept;
```

头文件中的实现按内部 `QPersistentModelIndexData *` 计算哈希：

```cpp
return qHash(index.d, seed);
```

这意味着哈希关注的是持久跟踪记录，而不是每次模型移动后的 row/column 数值。模型正确维护该记录时，项目移动不会因为行列改变而自动变成另一个哈希 key。

仍需注意：

- 项目删除或 reset 后索引可能无效；
- 模型销毁后不要继续把它当业务 key 使用；
- 哈希稳定不等于业务对象身份跨 reset 稳定；
- 不要把 persistent index 当数据库主键持久化到磁盘。

## 9. 复制、移动和容器使用

### 9.1 适合少量长期状态，不适合无节制缓存

```cpp
QPersistentModelIndex current = index;
QList<QPersistentModelIndex> expanded;
expanded.append(current);
```

persistent index 适合保存少量 UI 状态。对几十万条数据为每个项目都建立 persistent index，会增加模型维护和内存成本，应改用业务 ID、行号映射或专用选择结构。

### 9.2 作为哈希 key

```cpp
QHash<QPersistentModelIndex, QByteArray> annotations;
annotations.insert(index, "marked");
```

这适合把短期 UI 标记绑定到具体跟踪项。模型 reset 或项目删除后，要主动清理失效项，不能假设哈希容器会自动删除它们。

### 9.3 线程边界

`QPersistentModelIndex` 的值对象可以被复制和移动，但它不把模型访问变成线程安全操作：

- `data()`、`flags()`、`parent()` 等仍然是在模型上执行；
- 通常应在模型所属线程使用；
- 不要一个线程修改模型、另一个线程同时读取 persistent index 而没有同步；
- 跨线程传递时，传递业务 ID 通常比直接操作模型索引更清晰。

## 10. 常见错误

### 10.1 以为 persistent index 能阻止项目删除

**问题：** 删除项目后继续从 persistent index 读取数据。

**原因：** 它只跟踪模型通知允许跟踪的位置，不能拥有或保护项目。

**处理：** 删除后检查 `isValid()`；若需要恢复业务对象，保存业务 ID。

### 10.2 模型排序只发 `layoutChanged()`

**问题：** 保存的索引在排序后指向错误项目。

**原因：** 模型没有在布局变化期间调用 `changePersistentIndex()` 或等价批量维护。

**处理：** 按旧索引和新索引一一对应更新 persistent index，再完成布局通知。

### 10.3 reset 后仍相信旧 persistent index

**问题：** `isValid()` 变 false，或者即使有效也不再是原业务项目。

**原因：** reset 代表模型整体状态重建，不是普通行移动。

**处理：** 使用业务 ID 在新模型中重新定位。

### 10.4 把 row/column 当成持久身份

**问题：** 行移动后用旧行号更新业务缓存。

**原因：** persistent 的意义是跟踪项目，当前 row/column 只是当前位置。

**处理：** 通过 persistent index 当前的 `row()`、`parent()` 读取最新位置，业务唯一性另用 ID。

### 10.5 把 internal pointer 当所有权指针

**问题：** 通过 pointer 删除节点，或在模型销毁后继续解引用。

**原因：** internal pointer 只是模型内部索引协议的一部分。

**处理：** 由模型管理节点生命周期；调用方只把 pointer 当短期读取入口。

### 10.6 认为复制 persistent index 会复制项目

**问题：** 误以为修改一个副本不会影响另一个副本的跟踪。

**原因：** 复制的是同一持久位置的另一个 handle，不是项目快照。

**处理：** 需要独立业务快照时复制 `data()` 或自己的业务对象。

### 10.7 把它直接当跨程序序列化格式

**问题：** 保存 persistent index 到文件，下一次启动试图恢复。

**原因：** 它依附当前进程中的具体模型和内部跟踪记录。

**处理：** 序列化稳定业务 ID、路径或模型定义的键。

## API 速查表
### 11.1 构造和所有权

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QPersistentModelIndex()` | 构造无效持久索引 | 适合作为成员初始状态 |
| `QPersistentModelIndex(const QModelIndex &)` | 从普通索引建立持久跟踪 | 不复制节点；模型销毁后仍会失效 |
| `QPersistentModelIndex(const QPersistentModelIndex &)` | 复制跟踪 handle | 两个对象跟踪同一持久位置 |
| `QPersistentModelIndex(QPersistentModelIndex &&)` | 移动跟踪 handle | moved-from 对象为空且无效 |
| `~QPersistentModelIndex()` | 释放当前跟踪引用 | 不删除模型项目 |
| `operator=(const QPersistentModelIndex &)` | 复制替换跟踪关系 | 不影响源对象和模型项目 |
| `operator=(QPersistentModelIndex &&)` | 移动替换跟踪关系 | 源对象不再跟踪位置 |
| `operator=(const QModelIndex &)` | 改为跟踪普通索引 | 传入无效索引会清空当前状态 |
| `swap()` | 交换两个跟踪关系 | 不移动模型数据 |
| `operator QModelIndex()` | 取得当前普通索引 | 失效时得到无效普通索引 |

### 11.2 位置和模型

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `row()` | 返回当前父项中的行 | 这是动态位置，不是业务 ID |
| `column()` | 返回当前父项中的列 | 结合 `parent()` 和 `model()` 理解 |
| `internalId()` | 取得模型约定的整数句柄 | 不保证跨模型或跨 reset 稳定 |
| `internalPointer()` | 取得模型约定的内部指针 | 不拥有节点；只能按模型 pointer 协议解释 |
| `constInternalPointer()` | 只读取得内部指针 | const 不改变生命周期 |
| `model()` | 返回所属模型借用指针 | 不拥有模型 |
| `isValid()` | 判断当前跟踪位置是否有效 | 不等于业务对象永远存在 |

### 11.3 数据和导航

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `data(int role = Qt::DisplayRole)` | 读取当前角色数据 | 读取的是模型当前状态，不是创建时快照 |
| `multiData(QModelRoleDataSpan)` | 批量读取多个角色 | span 借用调用方存储；对象无效时不要期待填充 |
| `flags()` | 查询当前项目能力 | flags 会随模型状态改变 |
| `parent()` | 取得当前父索引 | 返回普通 `QModelIndex`；需持久保存要重新包装 |
| `sibling(int row, int column)` | 在同一父项下查找兄弟 | 返回普通 `QModelIndex` |

### 11.4 比较和哈希

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `operator==` / `operator!=` | 比较持久位置身份 | 部分旧式成员比较受移除宏控制 |
| 与 `QModelIndex` 的比较 | 判断持久位置和当前普通索引是否对应 | 先确认两者都属于同一模型语义 |
| 三向比较 | 提供有序比较 | 排序顺序不代表模型视觉顺序 |
| `qHash(const QPersistentModelIndex &, size_t)` | 对内部持久记录计算哈希 | 移动位置时可保持跟踪记录 hash；失效后仍要清理 |
| `Q_DECLARE_SHARED` 支持 | 允许 Qt 共享持久索引对象状态 | 共享的是跟踪记录，不是节点数据 |

## 12. 一句话总结

`QPersistentModelIndex` 是由具体模型维护的长期位置句柄：在模型正确发出插入、删除、移动和布局变化通知时，它可以跟随同一项目更新 row、column 和 parent；项目删除、reset 或模型销毁后仍会失效。它适合保存少量 UI 状态，不是节点所有权、跨模型业务 ID 或跨进程序列化格式。
