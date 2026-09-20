# QHelpIndexModel：把帮助索引接入列表模型

> 适用版本：Qt 6.11.1
> 头文件：`#include <QHelpIndexModel>`
> 所属模块：`Qt6::Help`
> 继承：`QStringListModel`

## 它解决什么问题

`QHelpIndexModel` 把已注册帮助文档的索引词转换成 `QStringListModel`，供 `QListView` 或 `QHelpIndexWidget` 展示。用户可以看到关键词列表、输入前缀进行筛选，再激活一个词取得对应的文档链接。

目录模型展示章节树，索引模型展示“主题词到文档”的入口，两者都受帮助引擎 filter 影响。

## 实际使用场景

- 使用 `QHelpEngine::indexModel()` 绑定到自定义 `QListView`。
- 切换 filter 后调用 `createIndexForCurrentFilter()` 重新生成索引。
- 使用 `filter(filter, wildcard)` 根据前缀或通配条件取得匹配索引。
- 在 `indexCreationStarted()` 和 `indexCreated()` 之间显示索引构建状态。

## 生成与索引有效期

构造函数和析构函数由 `QHelpEngine` 管理，应用不能直接创建或删除模型。`createIndex(customFilterName)` 按指定 filter 生成，`createIndexForCurrentFilter()` 使用当前 active filter。生成过程中 `isCreatingIndex()` 为真，列表可能尚未完整。

索引创建完成后，模型中的行和文本才适合交给视图。切换 filter 或 collection 后，旧索引内容和旧 `QModelIndex` 不能继续代表新结果。

`filter()` 返回一个匹配索引项的模型索引，`wildcard` 的具体匹配方式由 Help 索引实现决定；空 wildcard 通常表示按给定 filter 词查询。找不到时应检查返回的 `QModelIndex::isValid()`。

## 常见误区

- 在 `indexCreated()` 之前读取模型行数并当作最终数量。
- 把 `filter()` 的返回索引跨 filter 重建保存。
- 认为索引模型直接返回文档正文；它只提供索引词，链接需通过 engine 查询。
- 忽略当前 filter，导致用户看到的索引和目录不一致。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `void createIndex(const QString &customFilterName)` | 按指定 filter 创建索引列表。 | 生成期间列表可能变化；完成后再使用索引。 |
| `[since 6.8] void createIndexForCurrentFilter()` | 按当前 active filter 创建索引。 | Qt 6.8 起提供；切换 filter 后要重新调用。 |
| `QModelIndex filter(const QString &filter, const QString &wildcard = {})` | 查找符合关键词/通配条件的索引项。 | 返回无效索引表示没有匹配；索引重建后旧索引失效。 |
| `bool isCreatingIndex() const` | 判断索引是否正在生成。 | 只反映当前构建状态，最终可用性以 `indexCreated()` 为准。 |
| `QHelpEngineCore *helpEngine() const` | 返回模型关联的核心帮助引擎。 | 指针由 engine 管理，不转移所有权。 |
| `[signal] void indexCreationStarted()` | 索引创建开始时发出。 | 适合禁用重复请求和显示进度状态。 |
| `[signal] void indexCreated()` | 索引创建完成时发出。 | 在这里刷新视图并重新取得模型索引。 |
| `QStringListModel::rowCount()` / `data()` | 读取索引行数和显示文本。 | 这些是继承 API；模型未完成生成时结果可能暂时为空。 |

## 一句话总结

`QHelpIndexModel` 将帮助关键词变成列表模型；按 filter 生成，等 `indexCreated()` 后使用，索引词对应的文档跳转由 engine 查询完成。
