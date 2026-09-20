# QConcatenateTablesProxyModel 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QConcatenateTablesProxyModel>`  
> 所属模块：`Qt6::Core`  
> 继承：`QAbstractItemModel`

## 它解决什么问题

很多界面会把来源不同、结构相近的数据展示成一张连续表：最近打开的文件和收藏文件、多个设备的日志、多个批次的导入结果。若每次都把源数据复制到一个新模型，数据更新、编辑和拖放的同步会很麻烦。

`QConcatenateTablesProxyModel` 不复制数据。它接收多个源模型，把它们的**行**按加入顺序纵向拼接成一个平坦模型：

```text
源模型 A:  A0  A1
源模型 B:  B0  B1  B2
源模型 C:  C0

代理模型:  A0  A1  B0  B1  B2  C0
```

它适合列表和表格，不支持树模型。代理中的每个索引都能映射回某一个源模型的索引，因此读取、编辑和大多数模型通知仍由实际拥有数据的源模型完成。

它刻意不继承 `QAbstractProxyModel`，原因是后者围绕**单个** source model 设计；本类同时维护多个 source model。

## 使用前先确认三条数据形状规则

1. 行数是所有源模型根节点行数的总和，顺序就是 `addSourceModel()` 的调用顺序。
2. 列数不是最大值，而是所有源模型列数的**最小值**。某个源模型多出来的列会在代理中被忽略。
3. 只能处理平坦模型。传入树模型不会让树的子节点自动拼接；代理没有可用的层级结构。

第二条尤其容易造成“最后几列不见了”的误判。假如前两个表有 5 列，第三个表只有 3 列，代理只有 3 列。应先统一各源模型的列契约，或用自定义代理补齐缺失列。

## 最小示例：把两份列表接成一份

`QStringListModel` 是一个一列的平坦模型，正好能演示拼接与索引映射：

```cpp
#include <QConcatenateTablesProxyModel>
#include <QStringListModel>

void buildCombinedList()
{
    QStringListModel recent(QStringList{"Draft.md", "Readme.md"});
    QStringListModel favorites(QStringList{"Architecture.md", "Ideas.md"});

    QConcatenateTablesProxyModel combined;
    combined.addSourceModel(&recent);
    combined.addSourceModel(&favorites);

    Q_ASSERT(combined.rowCount() == 4);
    Q_ASSERT(combined.columnCount() == 1);

    const QModelIndex favoriteIndex = favorites.index(0, 0);
    const QModelIndex proxyIndex = combined.mapFromSource(favoriteIndex);

    Q_ASSERT(proxyIndex.row() == 2);
    Q_ASSERT(combined.mapToSource(proxyIndex) == favoriteIndex);
}
```

把 `combined` 交给 `QTableView`、`QListView` 或 QML 视图即可显示连续结果。源模型发生标准的数据变化、插入、删除或重置时，代理会据此更新自己的模型状态；前提是源模型本身正确发出 `QAbstractItemModel` 的通知。

## 源模型的所有权和运行时调整

`addSourceModel()` 只登记一个源模型指针，不改变其所有权，也不会把它设为代理的子对象。`removeSourceModel()` 也只解除拼接关系，不会删除模型。

常见的组织方式是让一个更长寿命的文档或控制器拥有所有源模型，再把它们的地址加入代理：

```cpp
class LogDocument : public QObject
{
    Q_OBJECT

public:
    explicit LogDocument(QObject *parent = nullptr)
        : QObject(parent)
        , localLog(this)
        , remoteLog(this)
        , merged(this)
    {
        merged.addSourceModel(&localLog);
        merged.addSourceModel(&remoteLog);
    }

private:
    QStringListModel localLog;
    QStringListModel remoteLog;
    QConcatenateTablesProxyModel merged;
};
```

同一个源模型不能重复加入。需要改变来源顺序时，移除后再按新顺序加入；本类没有“移动第几个 source model”的 API。来源可以在运行时新增和移除，代理会相应调整行数和列数。

作为 `QAbstractItemModel`，它有 `QObject` 线程亲和性。代理、所有源模型以及消费它的视图应在同一线程中使用；后台线程应传递整理后的数据，再让模型所属线程执行模型修改。不要跨线程直接操作模型或让一个模型同时被多个线程读写。

## 索引映射是操作数据的钥匙

从代理索引回到真正数据模型时调用 `mapToSource()`；拿到源模型索引后再映射到代理展示位置时调用 `mapFromSource()`：

```cpp
const QModelIndex proxyIndex = combined.index(2, 0);
const QModelIndex sourceIndex = combined.mapToSource(proxyIndex);

QAbstractItemModel *owner = const_cast<QAbstractItemModel *>(sourceIndex.model());
owner->setData(sourceIndex, "Renamed.md", Qt::EditRole);
```

在普通业务代码里，更推荐直接使用 `combined.setData(proxyIndex, value)`，因为它会映射并转发到对应 source model。只有需要调用源模型专有 API、定位数据归属或在两个模型层之间传递 `QModelIndex` 时，才手动映射。

映射结果要检查 `isValid()`。来自未加入模型的索引、失效索引、树模型子索引或不属于这个代理的索引都不应该被当作可编辑的目标。模型结构变化后，旧的普通 `QModelIndex` 也可能过期；需要跨变化长期保存位置时，使用 `QPersistentModelIndex` 并仍然准备处理失效情况。

`mapFromSource()` 和 `mapToSource()` 是 `Q_INVOKABLE`，可通过元对象系统和 QML 调用。不过 QML 侧传递模型索引不如 C++ 直观，复杂编辑流程通常仍建议在 C++ 层完成映射。

## 表头、角色和可编辑性来自哪里

`data()`、`itemData()`、`setData()`、`setItemData()` 和有效索引的 `flags()` 都会委托给该行所属的 source model。因此，同一张拼接表的不同区段可以具有不同的可编辑性、颜色角色或自定义角色。

这里有三个“以谁为准”的细节：

- `headerData()` 的水平表头来自第一个 source model；垂直表头来自对应行所属的 source model。
- 对无效索引调用 `flags()` 时，代理返回第一个 source model 的 flags。视图常用这种调用判断能否拖到空白区域。
- `roleNames()` 在 Qt 6.9.0 引入，返回所有源模型角色名的并集。若两个源模型给同一个 role number 起了不同名字，**最后加入的模型覆盖先加入模型的名字**。

因此，给 QML 或代理委托使用时，最好让所有 source model 为同一 role number 约定相同名称和语义。否则表面上角色名一样，某一段数据的含义可能已经变了。

## 拖放行为不是“全部自动合并”

本类会把拖放请求转发给实际的 source model，但转发目标取决于落点：

- 放到某项上，交给该项所在的 source model。
- 放在两行之间，交给落点下方那一行所属的 source model。
- 放在最后一行之后，交给最后一个 source model。

`mimeTypes()` 返回第一个 source model 的 MIME 类型；这意味着多源模型的拖放协议最好一致。

`mimeData()` 只会把调用转发给索引列表中第一个索引所属的 source model，并且默认实现只支持拖动**同一行**。若传入来自多行的索引，尤其是跨 source model 的多行，Qt 会触发断言，因为不同模型的 MIME 数据无法被通用地合并。需要跨表多行拖放时，应在子类中重写 `mimeData()`，定义自己的数据格式和合并规则。

## 什么时候不该用它

- 需要合并树形层级、文件夹和子节点时，用自定义 `QAbstractItemModel`，或先把数据扁平化。
- 需要按列拼接而不是按行堆叠时，本类不匹配；应设计组合模型或在源数据层聚合。
- 来源列数不同但希望保留所有列时，本类会截断为最小列数，需用专门的适配模型。
- 多个分区的 role 编号语义不同、拖放协议不同且无法统一时，直接拼接会让视图行为不一致。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造与寿命 | `QConcatenateTablesProxyModel(QObject *parent = nullptr)` | 创建一个空的多源表格拼接代理。 | 可设置 `QObject` 父对象；尚未加入源模型时没有可展示数据。 |
| 构造与寿命 | `~QConcatenateTablesProxyModel()` | 销毁代理模型。 | 不拥有已加入的源模型；源模型应由调用方或其父对象管理。 |
| 源模型管理 | `addSourceModel(QAbstractItemModel *)` | 在现有源模型之后加入一个平坦 source model。 | 不改变所有权；同一模型不能重复加入；加入顺序决定行区段顺序。 |
| 源模型管理 | `removeSourceModel(QAbstractItemModel *)` | 移除已登记的 source model。 | 只解除关系，不删除模型；需要改变顺序时移除后重新加入。 |
| 源模型管理 | `sourceModels() const` | 返回当前已加入的源模型列表。 | 列表顺序就是代理行区段顺序；返回指针不代表所有权转移。 |
| 索引映射 | `mapFromSource(const QModelIndex &) const` | 将任一已加入源模型的索引映射到代理索引。 | 仅适用于平坦源模型的有效索引；对无关或失效索引检查返回值是否有效。 |
| 索引映射 | `mapToSource(const QModelIndex &) const` | 将代理索引映射回实际拥有数据的源模型索引。 | 得到的索引属于具体 source model；调用其专有 API 前先检查有效性。 |
| 结构查询 | `rowCount(const QModelIndex &) const` | 返回所有源模型根行数之和。 | 只支持根层；非空 `parent` 不应被当成树形子项查询。 |
| 结构查询 | `columnCount(const QModelIndex &) const` | 返回全部 source model 中最小的列数。 | 任何一个来源列数较少都会截断代理可见列。 |
| 结构查询 | `index(int, int, const QModelIndex &) const` | 为代理中的行列创建 `QModelIndex`。 | 仅使用根父索引；行列必须落在拼接后有效范围内。 |
| 结构查询 | `parent(const QModelIndex &) const` | 返回代理索引的父索引。 | 平坦模型没有层级，正常情况下返回无效索引。 |
| 数据读取 | `data(const QModelIndex &, int) const` | 从该行所属的 source model 读取指定角色的数据。 | `Qt::DisplayRole` 是默认角色；自定义 role 语义应在各来源保持一致。 |
| 数据写入 | `setData(const QModelIndex &, const QVariant &, int)` | 将编辑请求映射并转发到对应 source model。 | 是否成功由源模型决定；索引无效或源模型不可编辑时返回 `false`。 |
| 多角色读取 | `itemData(const QModelIndex &) const` | 读取一个单元格全部可用角色和值。 | 返回内容来自对应 source model；适合批量检查角色，不替代 `data()` 的常用读取。 |
| 多角色写入 | `setItemData(const QModelIndex &, const QMap<int, QVariant> &)` | 一次把多组角色值写入对应 source model。 | 原子性和成功条件由源模型实现决定；需检查返回值。 |
| 交互能力 | `flags(const QModelIndex &) const` | 返回单元格可选、可编辑、可拖放等标志。 | 有效索引使用对应 source model 的 flags；无效索引使用第一个 source model 的 flags。 |
| 表头 | `headerData(int, Qt::Orientation, int) const` | 返回代理的水平或垂直表头数据。 | 水平表头来自第一个源模型；垂直表头来自该行所属源模型。 |
| 角色声明 | `roleNames() const`（Qt 6.9.0 起） | 合并所有 source model 的 role number 到 role name 映射。 | role number 冲突时最后加入模型的名称胜出；QML 项目要统一角色约定。 |
| 拖放检查 | `canDropMimeData(const QMimeData *, Qt::DropAction, int, int, const QModelIndex &) const` | 询问目标落点是否可接受给定 MIME 数据。 | 实际能力依赖相应 source model；与 `dropMimeData()` 的落点规则配合理解。 |
| 拖放执行 | `dropMimeData(const QMimeData *, Qt::DropAction, int, int, const QModelIndex &)` | 将一次放置操作转发给落点对应的 source model。 | 落到项上、行间、末尾时的目标来源不同；跨来源语义需自行设计。 |
| 拖放数据 | `mimeTypes() const` | 返回代理声明支持的 MIME 类型。 | 取自第一个 source model；多个来源最好实现同一 MIME 协议。 |
| 拖放数据 | `mimeData(const QModelIndexList &) const` | 为要拖动的代理索引生成 MIME 数据。 | 默认只支持同一行；跨多行或跨 source model 会触发断言，需子类重写。 |
| 视图布局 | `span(const QModelIndex &) const` | 返回单元格在视图中的跨行跨列尺寸。 | 结果由对应 source model 的实现决定；多数普通表模型使用默认单格跨度。 |

## 一句话记忆

`QConcatenateTablesProxyModel` 把多个平坦 source model 的行按顺序接成一张表，但列数取最小值、数据所有权仍在源模型手中，任何代理索引都应通过映射回到真正的数据归属。
