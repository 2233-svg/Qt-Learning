# QHelpFilterEngine：管理帮助文档过滤器

> 适用版本：Qt 6.11.1
> 头文件：`#include <QHelpFilterEngine>`
> 所属模块：`Qt6::Help`
> 继承：`QObject`

## 它解决什么问题

`QHelpFilterEngine` 为一个 `QHelpEngineCore` 管理命名 filter。每个 filter 由 `QHelpFilterData` 描述，可按 component 和 version 限制文档；其中一个 filter 可以成为 active filter，帮助引擎随后用它过滤目录、索引、关键词和搜索结果。

它解决的是“同一套 qch 文档需要按产品版本、模块或用户角色显示不同内容”的问题。过滤器配置存放在 collection 中，active filter 变化还可以由 `QHelpEngineCore::autoSaveFilter` 持久化。

## 实际使用场景

- 提供“Qt 6.11”“Qt Widgets”“开发者 API”等帮助视图。
- 在设置对话框中新增、编辑、删除用户 filter。
- 用 `availableComponents()` 和 `availableVersions()` 填充筛选项。
- 切换 active filter 后重新生成目录和索引，并重新发起搜索。
- 调试 namespace 与 component/version 的对应关系。

## 与 QHelpEngineCore 的关系

对象由 `QHelpEngineCore` 内部创建并管理，应用通过 `filterEngine()` 取得指针，不应直接构造或删除。调用新式 filter API 前应在 setup 前后按应用流程调用 `setUsesFilterEngine(true)`，并确保 engine 已完成 setup。

`setFilterData(name, data)` 既能更新已有 filter，也能创建新 filter。`setActiveFilter(name)` 只接受已存在的 filter 名称；传空字符串可表示不选 active filter，此时帮助引擎返回未经过该 active filter 的完整结果。

## 结果与持久化边界

`indices()`、`namespacesForFilter()` 等查询是即时读取 collection/filter 状态。切换 active filter 后，已经返回的列表不会自动变化，目录模型和搜索结果也不会自动替换成新内容，应用要主动刷新。

`availableComponents()` 和 `availableVersions()` 汇总所有已注册 qch 的元数据，不是当前 active filter 的结果。`namespaceToComponent()`、`namespaceToVersion()` 可用于解释某个 namespace 为什么匹配或被排除。

## 线程与所有权

它是 QObject，线程归属跟随帮助引擎。不要在工作线程直接修改 filter，也不要在 engine 销毁后缓存指针。连接 `filterActivated` 时使用带 context 的连接，避免界面对象销毁后仍接收通知。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `QMap<QString, QString> namespaceToComponent() const` | 返回 namespace 到 component 的映射。 | 汇总所有注册文档，不代表当前 active filter 的子集。 |
| `QMap<QString, QVersionNumber> namespaceToVersion() const` | 返回 namespace 到 version 的映射。 | 版本来自 qch 元数据；缺失版本需按无效值处理。 |
| `QStringList filters() const` | 返回 engine 中所有 filter 名称。 | 名称是 collection 中的持久化标识。 |
| `QString activeFilter() const` | 返回当前 active filter 名称。 | 空字符串通常表示未选择 active filter。 |
| `bool setActiveFilter(const QString &filterName)` | 切换 active filter。 | filter 不存在或 collection 不可写时可能失败；成功后监听 `filterActivated`。 |
| `QStringList availableComponents() const` | 返回所有已注册文档提供的 component。 | 是全集，不受 active filter 限制。 |
| `QList<QVersionNumber> availableVersions() const` | 返回所有已注册文档提供的 version。 | 用于构建设置选项，不等于当前结果版本。 |
| `QHelpFilterData filterData(const QString &filterName) const` | 读取指定 filter 的条件。 | 未知名称返回空条件；需结合 `filters()` 判断是否存在。 |
| `bool setFilterData(const QString &filterName, const QHelpFilterData &filterData)` | 创建或更新 filter 条件。 | 会修改 collection；写入失败应检查返回值和 engine 错误。 |
| `bool removeFilter(const QString &filterName)` | 删除指定 filter。 | 不要删除当前 active filter 前忽略状态变化；名称不存在时失败。 |
| `QStringList namespacesForFilter(const QString &filterName) const` | 返回匹配指定 filter 的 namespace。 | 用于诊断过滤结果；空 filter 名称的语义要按文档约定处理。 |
| `QStringList indices() const` | 返回当前 active filter 下可用的索引名。 | active filter 改变后旧列表不会自动更新。 |
| `QStringList indices(const QString &filterName) const` | 返回指定 filter 下可用的索引名。 | 传空名称可查询未过滤的索引全集。 |
| `[signal] void filterActivated(const QString &newFilter)` | active filter 成功改变时发出。 | 在这里触发目录/索引刷新和搜索状态更新。 |

## 一句话总结

`QHelpFilterEngine` 管的是“哪些文档可见”：用 `QHelpFilterData` 定义条件，用名称保存配置，用 active filter 驱动整个 Help 查询链。
