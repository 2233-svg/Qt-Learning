# QHelpContentModel：把帮助目录接入 Model/View

> 适用版本：Qt 6.11.1
> 头文件：`#include <QHelpContentModel>`
> 所属模块：`Qt6::Help`
> 继承：`QAbstractItemModel`

## 它解决什么问题

`QHelpContentModel` 把 `QHelpEngineCore` 中的文档目录转换成 Qt 的树模型。视图可以用 `QModelIndex` 展开和选择章节，代理可以通过 `DisplayRole` 等角色取得显示数据，应用再根据节点 URL 打开对应帮助页面。

它把两个生命周期连接起来：帮助引擎负责读取 collection 和过滤结果，模型负责向 `QTreeView` 报告一棵可浏览的树。目录创建可能需要一段时间，因此模型提供开始和完成信号。

## 实际使用场景

- 直接把 `QHelpEngine::contentModel()` 设置给 `QTreeView`。
- 切换用户自定义 filter 后重新生成目录。
- 使用 `contentItemAt()` 从当前索引取得底层节点和帮助 URL。
- 在 `contentsCreationStarted()` 时显示忙碌状态，在 `contentsCreated()` 后恢复交互。

## 创建、刷新与异步状态

构造函数是私有的，模型由 `QHelpEngine` 创建并管理。应用不应直接实例化或删除它。使用前应让帮助引擎完成 `setupData()`；否则模型可能没有可用文档。

`createContents(filter)` 按指定 filter 生成目录；`createContentsForCurrentFilter()` 使用引擎当前 filter。生成期间 `isCreatingContents()` 为真，模型可能处于清空、插入和最终完成之间的过渡状态。不要在 `contentsCreationStarted()` 后立即假定完整树已经可读，应等待 `contentsCreated()`。

模型索引由模型拥有语义。目录重建后，旧 `QModelIndex` 和通过 `contentItemAt()` 得到的节点指针都不应继续使用；视图通常会在模型通知后重新获取索引。

## Model/View 契约

这是一个树模型，根索引使用无效 `QModelIndex`。`rowCount(parent)` 返回父节点的子节点数，`index(row, column, parent)` 生成子节点索引，`parent(index)` 返回上级索引。目录通常只有一列，应用应通过 `columnCount()` 查询而不是写死假设。

`data(index, role)` 的显示内容由模型决定，实际展示主要依赖 `Qt::DisplayRole`。向模型传入无效索引或超出范围的行列时，应接受无效返回，而不是继续把索引当有效节点。

## 常见误区

- 直接 `new QHelpContentModel`，但构造函数并不公开。
- 在目录创建未完成时遍历模型，把临时空树误判成“没有文档”。
- 切换 filter 后继续使用旧 `QModelIndex` 或 `QHelpContentItem *`。
- 在后台线程直接操作模型或绑定视图；模型和视图应在 GUI 线程使用。
- 把 `contentItemAt()` 返回的节点当作应用拥有对象并删除。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `~QHelpContentModel()` | 销毁目录模型。 | 通常由 `QHelpEngine` 负责；视图应先解除不再有效的模型关系。 |
| `void createContents(const QString &customFilterName)` | 使用指定 filter 创建目录树。 | 生成过程通过开始/完成信号观察；完成前模型内容可能不完整。 |
| `[since 6.8] void createContentsForCurrentFilter()` | 使用帮助引擎当前 filter 创建目录树。 | Qt 6.8 起提供；切换 filter 后需重新调用。 |
| `QHelpContentItem *contentItemAt(const QModelIndex &index) const` | 返回模型索引对应的底层目录节点。 | 指针不转移所有权，只在当前目录树生命周期内使用。 |
| `QVariant data(const QModelIndex &index, int role) const` | 返回指定索引和角色的数据。 | 主要读取 `Qt::DisplayRole`；无效索引应返回无效值。 |
| `QModelIndex index(int row, int column, const QModelIndex &parent = {}) const` | 根据父索引和行列生成子索引。 | 先用 `rowCount()`、`columnCount()` 检查范围。 |
| `QModelIndex parent(const QModelIndex &index) const` | 返回索引的父索引。 | 根节点的父索引为空。 |
| `int rowCount(const QModelIndex &parent = {}) const` | 返回父节点下的子节点数。 | 目录模型是树结构；根节点用空父索引查询。 |
| `int columnCount(const QModelIndex &parent = {}) const` | 返回列数。 | 视图布局应以此为准，不要硬编码列数。 |
| `bool isCreatingContents() const` | 判断目录是否正在生成。 | 只适合作为状态提示；最终可用性以 `contentsCreated()` 为准。 |
| `[signal] void contentsCreationStarted()` | 目录生成开始时发出。 | 适合禁用重复刷新和显示忙碌提示。 |
| `[signal] void contentsCreated()` | 目录生成完成时发出。 | 在这里重新获取模型索引和目录节点。 |

## 一句话总结

`QHelpContentModel` 是帮助目录到树模型的桥梁：把它交给 `QTreeView`，用完成信号界定索引有效期，用 filter 重建目录。
