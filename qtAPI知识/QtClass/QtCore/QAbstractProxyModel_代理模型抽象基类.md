# QAbstractProxyModel 代理模型抽象基类深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractProxyModel>`  
> 所属模块：`Qt6::Core`  
> 继承关系：`QObject -> QAbstractItemModel -> QAbstractProxyModel`  
> 常见派生类：`QIdentityProxyModel`、`QSortFilterProxyModel`、`QTransposeProxyModel`

## 1. 它解决什么问题

`QAbstractProxyModel` 用来在“真实数据模型”和“视图看到的模型”之间加一层转换。它自己通常不保存业务数据，而是拿一个 source model，然后把源模型的数据排序、过滤、重排、转置、包装或改写后，再暴露给视图。

可以把它想成一层可插拔的模型适配器：

```text
真实数据
   ↓
QAbstractItemModel source model
   ↓
QAbstractProxyModel proxy model
   ↓
QTreeView / QTableView / QListView / QML View
```

视图只看见 proxy model。proxy model 内部需要知道每一个 proxy index 对应 source model 的哪个 source index。

这就是代理模型最核心的两件事：

```cpp
QModelIndex mapToSource(const QModelIndex &proxyIndex) const;
QModelIndex mapFromSource(const QModelIndex &sourceIndex) const;
```

如果这两个映射不稳定，代理模型就会出现显示错行、编辑错对象、选择跳动、拖放落错位置、排序后数据错位等问题。

## 2. 什么时候直接继承它，什么时候不要

Qt 文档建议：如果标准代理模型已经接近需求，应优先继承现有类，而不是直接从 `QAbstractProxyModel` 起步。

常见选择：

- 只想透传源模型并在少量函数上加行为：用 `QIdentityProxyModel`。
- 排序和过滤：用 `QSortFilterProxyModel`。
- 行列转置：用 `QTransposeProxyModel`。
- 完全自定义拓扑，例如把树压平成列表、把多模型合并、做复杂分组：才考虑直接继承 `QAbstractProxyModel`。

直接继承它时，不能只实现 `mapToSource()` 和 `mapFromSource()`。因为它仍然是 `QAbstractItemModel` 的子类，你还要根据自己的代理拓扑实现 `index()`、`parent()`、`rowCount()`、`columnCount()` 等模型函数。

## 3. source model：代理模型的数据来源

代理模型通过 `sourceModel` 属性持有源模型指针：

```cpp
proxy->setSourceModel(source);
QAbstractItemModel *source = proxy->sourceModel();
```

几个边界很重要：

- proxy model 通常不拥有 source model，源模型生命周期要由调用者或 QObject 父子关系管理。
- 如果 source model 被删除，或者没有设置 source model，proxy 会在一个空的占位模型上工作。
- 更换 source model 是结构级变化，派生类重写 `setSourceModel()` 时应 reset 自己。
- 源模型和代理模型通常应在同一线程，尤其是连接到 GUI 视图时。

派生类重写 `setSourceModel()` 的典型顺序：

```cpp
void MyProxyModel::setSourceModel(QAbstractItemModel *sourceModel)
{
    beginResetModel();

    disconnect(m_sourceConnections);
    m_sourceConnections.clear();

    QAbstractProxyModel::setSourceModel(sourceModel);

    if (sourceModel) {
        m_sourceConnections += connect(sourceModel,
                                       &QAbstractItemModel::dataChanged,
                                       this,
                                       &MyProxyModel::onSourceDataChanged);
    }

    rebuildMapping();
    endResetModel();
}
```

这个顺序的意义是：视图先知道代理模型要整体失效，然后你断开旧源模型、设置新源模型、重建映射，最后让视图重新查询。

## 4. 双向映射是代理模型的心脏

### 4.1 `mapToSource()`

`mapToSource(proxyIndex)` 把视图看到的索引映射回真实数据索引。编辑、读取数据、拖放、flags、header 等很多默认实现都会依赖这个方向。

```cpp
QVariant MyProxy::data(const QModelIndex &proxyIndex, int role) const
{
    const QModelIndex sourceIndex = mapToSource(proxyIndex);
    return sourceModel()->data(sourceIndex, role);
}
```

### 4.2 `mapFromSource()`

`mapFromSource(sourceIndex)` 把源模型索引映射成代理模型索引。源模型发出 `dataChanged()`、`rowsInserted()`、选择变化映射等场景会依赖这个方向。

```cpp
void MyProxy::onSourceDataChanged(const QModelIndex &sourceTopLeft,
                                  const QModelIndex &sourceBottomRight,
                                  const QList<int> &roles)
{
    const QModelIndex proxyTopLeft = mapFromSource(sourceTopLeft);
    const QModelIndex proxyBottomRight = mapFromSource(sourceBottomRight);

    if (proxyTopLeft.isValid() && proxyBottomRight.isValid())
        emit dataChanged(proxyTopLeft, proxyBottomRight, roles);
}
```

### 4.3 映射必须保持一致

对还存在且可见的项，通常应该满足：

```text
mapToSource(mapFromSource(sourceIndex)) == sourceIndex
mapFromSource(mapToSource(proxyIndex)) == proxyIndex
```

过滤模型有一个例外：被过滤掉的 source index 映射到 proxy 时应返回无效索引。也就是说，映射不是一定覆盖所有 source index，但对可见项必须稳定。

## 5. 默认转发函数做了什么

`QAbstractProxyModel` 重写了许多 `QAbstractItemModel` 函数。大多数默认实现的思路都是：

```text
proxyIndex
    ↓ mapToSource()
sourceIndex
    ↓ 调 sourceModel() 的对应函数
返回数据或结果
```

例如：

- `data(proxyIndex, role)` 通常转到 `sourceModel()->data(sourceIndex, role)`。
- `setData(proxyIndex, value, role)` 通常转到源模型的 `setData()`。
- `flags(proxyIndex)` 通常转到源模型的 `flags()`。
- `itemData(proxyIndex)` 和 `setItemData()` 按索引映射后转发。
- `canFetchMore(parent)` 和 `fetchMore(parent)` 按父索引映射后转发。
- `mimeData(indexes)` 需要把代理索引列表映射成源索引列表。

这让简单代理模型可以少写很多转发代码。但如果代理模型改变了行列结构、过滤掉了部分数据、合并了多个源 index，或者对 role 做了加工，就要重写对应函数，不能盲目依赖默认转发。

## 6. selection 映射

选择模型使用的是 `QItemSelection`，它可能包含多个连续范围。代理模型提供：

```cpp
QItemSelection mapSelectionToSource(const QItemSelection &proxySelection) const;
QItemSelection mapSelectionFromSource(const QItemSelection &sourceSelection) const;
```

默认实现会按索引映射选择范围。对于简单一一对应代理通常够用。复杂代理要小心：

- 过滤后，一个 source 范围可能在 proxy 中变成多个不连续范围。
- 排序后，连续 source 行可能不再连续。
- 树压平列表时，父子层级变化会让范围语义变复杂。
- 合并多个源项时，一个 proxy index 可能没有单一 source index。

这类情况下应重写 selection 映射，否则用户框选、多选、快捷键选择和程序设置选择时会出现错位。

## 7. `createSourceIndex()`：给复杂映射留的工具

```cpp
QModelIndex createSourceIndex(int row, int col, void *internalPtr) const;
```

它等价于在 source model 上创建索引，主要用于代理模型想保留源模型的父子关系或内部指针时。

典型思路是：

```text
mapFromSource(sourceIndex)
    把 sourceIndex.internalPointer() 存进 proxy index

mapToSource(proxyIndex)
    从 proxyIndex.internalPointer() 取回源内部指针
    调 createSourceIndex(row, col, internalPtr) 重新构造 source index
```

为什么需要它？因为 `QAbstractItemModel::createIndex()` 是受保护函数，代理模型不能随便调用源模型的受保护成员。`createSourceIndex()` 给代理模型一个安全入口，用于构造属于 source model 的索引。

它从 Qt 6.2 开始提供。跨 Qt 6.1 或更早版本时，要做版本判断或换一种映射保存策略。

## 8. 源模型变化如何转成代理模型变化

代理模型最难的不是读取数据，而是源模型发生变化时保持同步。

如果源模型发：

- `dataChanged()`：代理模型要把范围映射后发自己的 `dataChanged()`。
- `rowsAboutToBeInserted()` 和 `rowsInserted()`：代理模型要判断这些源行是否会出现在代理里，并发对应 begin/end。
- `rowsAboutToBeRemoved()` 和 `rowsRemoved()`：代理模型要先用旧映射通知即将删除，再改映射。
- `layoutAboutToBeChanged()` 和 `layoutChanged()`：代理模型要更新排序、过滤或层级映射。
- `modelAboutToBeReset()` 和 `modelReset()`：代理模型通常也要 reset。

`QSortFilterProxyModel` 已经处理了大量这类细节。只有当标准代理模型无法表达你的拓扑变化时，才值得自己承担这套同步逻辑。

## 9. 一个极简透传代理轮廓

下面不是完整生产代码，只是说明直接继承 `QAbstractProxyModel` 时要同时提供模型拓扑和映射。

```cpp
class FirstColumnProxy : public QAbstractProxyModel
{
public:
    using QAbstractProxyModel::QAbstractProxyModel;

    int rowCount(const QModelIndex &parent = QModelIndex()) const override
    {
        if (!sourceModel() || parent.isValid())
            return 0;

        return sourceModel()->rowCount({});
    }

    int columnCount(const QModelIndex &parent = QModelIndex()) const override
    {
        return parent.isValid() ? 0 : 1;
    }

    QModelIndex index(int row, int column,
                      const QModelIndex &parent = QModelIndex()) const override
    {
        if (!hasIndex(row, column, parent))
            return {};

        return createIndex(row, column);
    }

    QModelIndex parent(const QModelIndex &) const override
    {
        return {};
    }

    QModelIndex mapToSource(const QModelIndex &proxyIndex) const override
    {
        if (!proxyIndex.isValid() || !sourceModel())
            return {};

        return sourceModel()->index(proxyIndex.row(), 0);
    }

    QModelIndex mapFromSource(const QModelIndex &sourceIndex) const override
    {
        if (!sourceIndex.isValid() || sourceIndex.column() != 0)
            return {};

        return index(sourceIndex.row(), 0);
    }
};
```

这个例子只把源模型第 0 列暴露成一列列表。真实代理还需要处理源模型插入、删除、重置、排序和选择映射；所以实际项目里，这种需求常常可以由 `QIdentityProxyModel` 或 `QSortFilterProxyModel` 更稳地完成。

## 10. 常见误区

### 10.1 映射只写一个方向

只实现 `mapToSource()` 能读数据，但源模型变化、选择同步和从源索引定位代理索引都会坏。两个方向都必须设计。

### 10.2 过滤后仍返回“看似有效”的代理索引

被过滤掉的 source index 应映射为无效 proxy index。不要为了方便返回某个邻近行，否则视图会显示或编辑错对象。

### 10.3 更换 source model 时不 reset

源模型一换，所有 proxy index、行列数、role 和映射缓存都可能失效。重写 `setSourceModel()` 时应使用 `beginResetModel()` 和 `endResetModel()`。

### 10.4 以为默认转发能覆盖复杂代理

默认转发适合一一对应或简单转换。过滤、分组、合并、多源、树转列表等代理必须重写更多函数和信号转发逻辑。

### 10.5 代理和源模型线程不一致

模型相关 API 不线程安全。连接到视图时，proxy 和 source 通常都应在 GUI 线程；后台线程应把数据变化投递给源模型或代理模型所属线程处理。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 属性 | `sourceModel` | 保存被代理的数据模型指针 | proxy 通常不拥有 source；空源模型时使用空占位模型 |
| 构造函数 | `QAbstractProxyModel(QObject *parent = nullptr)` | 构造代理模型基类对象 | 抽象类不能直接实例化，通常继承现有代理类更省事 |
| 析构函数 | `~QAbstractProxyModel()` | 多态销毁代理模型 | 销毁后所有 proxy index 失效，不代表销毁 source model |
| 属性绑定 | `bindableSourceModel()` | 返回 `sourceModel` 的 `QBindable` 接口 | 用于 Qt property binding 场景 |
| 纯虚映射 | `mapToSource(const QModelIndex &proxyIndex) const` | 把代理索引转换成源模型索引 | 读取、编辑、拖放和默认转发都依赖它 |
| 纯虚映射 | `mapFromSource(const QModelIndex &sourceIndex) const` | 把源模型索引转换成代理索引 | 源模型变化和选择映射依赖它；被过滤项返回无效索引 |
| 选择映射 | `mapSelectionToSource(const QItemSelection &selection) const` | 把代理选择范围转换成源模型选择范围 | 过滤或排序导致范围不连续时应重写 |
| 选择映射 | `mapSelectionFromSource(const QItemSelection &selection) const` | 把源模型选择范围转换成代理选择范围 | 复杂拓扑下不能只逐 index 简单映射 |
| 源模型设置 | `setSourceModel(QAbstractItemModel *sourceModel)` | 设置代理要处理的源模型 | 派生类重写时应 reset、断开旧连接、连接新模型并重建映射 |
| 源模型读取 | `sourceModel() const` | 返回当前源模型 | 可能是空占位模型相关状态，使用前仍要确认业务源是否存在 |
| 默认转发 | `data(const QModelIndex &proxyIndex, int role) const` | 返回代理索引的数据 | 默认按 `mapToSource()` 转发到源模型，改写 role 时重写 |
| 默认转发 | `setData(const QModelIndex &index, const QVariant &value, int role)` | 修改代理索引对应的数据 | 默认映射到源模型；成功后变化信号要能回到 proxy |
| 默认转发 | `headerData(int section, Qt::Orientation orientation, int role) const` | 返回代理表头数据 | 行列被重排或隐藏时应重写 |
| 默认转发 | `setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role)` | 修改代理表头数据 | 默认转发到源模型，改列顺序时要映射 section |
| 默认转发 | `itemData(const QModelIndex &index) const` | 返回代理索引的多 role 数据 | 默认映射到源模型 |
| 默认转发 | `setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles)` | 一次设置多个 role 数据 | 默认映射到源模型，成功后要通知 proxy 侧变化 |
| 默认转发 | `clearItemData(const QModelIndex &index)` | 清空代理索引对应的 role 数据 | Qt 6.0 起；默认映射到源模型 |
| 默认转发 | `flags(const QModelIndex &index) const` | 返回代理索引的可选、可编辑、可拖放等能力 | 过滤、只读包装或改写能力时重写 |
| 默认转发 | `buddy(const QModelIndex &index) const` | 返回代理索引对应的编辑 buddy | 源模型 buddy 映射回来后必须仍属于 proxy |
| 默认转发 | `canFetchMore(const QModelIndex &parent) const` | 判断代理父项是否还能加载更多 | 默认映射 parent 到源模型 |
| 默认转发 | `fetchMore(const QModelIndex &parent)` | 触发源模型加载更多数据 | 加载后源模型信号必须被正确转成代理信号 |
| 默认转发 | `sort(int column, Qt::SortOrder order)` | 请求按代理列排序 | 默认转发前后要考虑列映射；排序代理通常用 `QSortFilterProxyModel` |
| 默认转发 | `span(const QModelIndex &index) const` | 返回代理索引跨越行列大小 | 默认映射到源模型，行列变换时可能要重写 |
| 默认转发 | `hasChildren(const QModelIndex &parent) const` | 判断代理父项是否有子项 | 默认映射到源模型，过滤后要反映可见子项 |
| 默认转发 | `sibling(int row, int column, const QModelIndex &idx) const` | 返回代理中的兄弟索引 | 代理行列重排时要保证返回 proxy index |
| 默认转发 | `mimeData(const QModelIndexList &indexes) const` | 把代理索引编码为拖拽数据 | 默认需要映射成源索引，复杂代理可能要自定义格式 |
| 默认转发 | `mimeTypes() const` | 返回拖放支持的 MIME 类型 | 默认来自源模型；包装模型可追加自己的类型 |
| 默认转发 | `canDropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) const` | 判断代理位置能否接受 drop | 必须把代理 row、column、parent 正确转换到源模型位置 |
| 默认转发 | `dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)` | 在代理坐标下处理 drop | 结构改变时要确保 source 和 proxy 信号同步 |
| 默认转发 | `supportedDragActions() const` | 返回代理支持的拖拽动作 | 默认可来自源模型，过滤只读代理可能要收窄能力 |
| 默认转发 | `supportedDropActions() const` | 返回代理支持的 drop 动作 | 默认可来自源模型，目标坐标映射要正确 |
| 默认转发 | `roleNames() const` | 返回代理可见 role 名称 | 改写或新增 role 时必须重写，QML 尤其依赖 |
| 默认转发 | `submit()` | 请求提交代理或源模型缓存修改 | 默认转发到源模型，失败应返回 `false` |
| 默认转发 | `revert()` | 请求撤销代理或源模型缓存修改 | 默认转发到源模型 |
| 信号 | `sourceModelChanged()` | 通知 `sourceModel` 属性发生变化 | 私有信号，可以连接，不能由子类直接发 |
| 受保护函数 | `createSourceIndex(int row, int col, void *internalPtr) const` | 构造属于 source model 的索引 | Qt 6.2 起；适合保留源模型内部指针的复杂映射 |
| 保护构造 | `QAbstractProxyModel(QAbstractProxyModelPrivate &, QObject *parent)` | 供 Qt 内部或高级派生类使用的私有数据构造入口 | 普通代理模型实现不会直接用 |

## 12. 一句话抓住它

`QAbstractProxyModel` 的核心不是“转发 source model”这么简单，而是维护一个可靠的双向映射：视图看到 proxy index，真实数据在 source index，所有读取、编辑、选择和结构变化都必须在这两个坐标系之间准确转换。
