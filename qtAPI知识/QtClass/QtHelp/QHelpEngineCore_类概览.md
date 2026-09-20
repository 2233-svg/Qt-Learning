# QHelpEngineCore：管理 collection 与 qch 文档

> 适用版本：Qt 6.11.1
> 头文件：`#include <QHelpEngineCore>`
> 所属模块：`Qt6::Help`
> 继承：`QObject`

## 它解决什么问题

`QHelpEngineCore` 管理一个 Qt Help collection file，并提供 qch 文档注册、注销、过滤、URL 定位、文件读取、关键词/标识符查询和持久化自定义值。它不包含目录树、索引列表或搜索控件，因此既能服务 GUI 帮助窗口，也能用于命令行工具、后台文档检查和测试程序。

collection file 是运行时数据库；qch 文件是实际文档包。引擎把已注册 qch 的 namespace、虚拟文件夹、索引和过滤信息组织起来，调用方再用 qthelp URL 读取具体文件。

## 初始化流程

构造函数接收 collection file 路径。如果文件不存在，Qt 可以创建它，但文档数据要到 `setupData()` 才正式加载。初始化开始时发出 `setupStarted()`，完成时发出 `setupFinished()`；这段期间不要读取依赖 collection 状态的结果。

某些 getter 会隐式触发 setup，但显式调用 `setupData()` 更适合应用启动流程，因为可以直接根据返回值和 `error()` 处理失败。设置新的 `collectionFile` 会使当前引擎回到未初始化状态，之后要重新 setup。

Qt 6 的 `readOnly` 默认是 `true`。只读模式适合安装在不可写目录中的 collection，但不能注册或注销文档、编辑过滤器或写自定义值。需要修改 collection 时，应在 setup 前调用 `setReadOnly(false)`，并保证文件及目录真的可写。

## 文档注册与 URL 查询

`registerDocumentation()` 注册 qch 文件，namespace 是唯一身份；同一 collection 不能重复注册同 namespace 的文档。`registeredDocumentations()` 返回的是 namespace 列表，不是 qch 文件路径。路径可通过 `documentationFileName(namespace)` 反查。

`documentsForIdentifier()` 和 `documentsForKeyword()` 返回 `QHelpLink` 列表，结果受当前 filter 或指定 filter 影响。`findFile()` 能根据 qthelp URL 中的虚拟文件夹选择最匹配的 namespace，并在文件不存在时返回无效 URL。拿到有效 URL 后再用 `fileData()` 读取字节内容。

`fileData()` 返回空 `QByteArray` 可能代表目标不存在，也可能是文件确实为空；如果业务必须区分两者，应先用 `findFile()`、`files()` 或其他元数据验证。

## 过滤器与持久化设置

新式过滤器由 `QHelpFilterEngine` 管理。调用 `setUsesFilterEngine(true)` 后，相关目录、索引和搜索查询使用它的 active filter。旧的 `currentFilter`、custom filter 和 attribute API 仍存在于头文件中，但新代码应优先围绕 `QHelpFilterEngine` 设计。

`autoSaveFilter` 默认开启时，active filter 的变化会写入 collection。只读模式、写权限不足或 setup 尚未完成时，持久化操作可能失败。`customValue()`、`setCustomValue()` 和 `removeCustomValue()` 使用 collection 的 settings 区域保存应用自己的键值。

## 线程与生命周期

对象是 `QObject`，应在创建它的线程中使用。setup、collection 写入、过滤器切换和查询共享内部数据库状态，不应从多个线程并发直接调用。需要后台工作时，把结果复制出来，并通过 queued signal/slot 回到拥有引擎的线程更新 GUI。

## 常见误区

- 把构造成功当作 setup 成功。
- 在 `setupStarted()` 与 `setupFinished()` 之间读取文档列表。
- 在只读模式下注册文档，却只检查返回的 `false` 不读取 `error()`。
- 把 `registeredDocumentations()` 当作文件路径列表。
- 忽略 filter 对关键词、目录和索引结果的影响。
- 更换 collection file 后继续使用旧模型、旧 URL 或旧结果。
- 以为 `fileData()` 返回空数组一定是文件损坏。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `explicit QHelpEngineCore(const QString &collectionFile, QObject *parent = nullptr)` | 创建使用指定 collection file 的核心引擎。 | 文件可以尚不存在；真正加载由 setup 触发。 |
| `~QHelpEngineCore()` | 释放引擎和内部 collection 资源。 | 销毁后所有返回的 filter engine、模型或查询结果关系都结束。 |
| `bool setupData()` | 解析 collection 并初始化帮助数据。 | 监听 `setupStarted()`/`setupFinished()`；失败后读取 `error()`。 |
| `QString collectionFile() const` / `setCollectionFile(const QString &)` | 读取或更换 collection 路径。 | 更换后引擎失效，需要重新 setup；路径通常应为绝对路径。 |
| `bool isReadOnly() const` / `setReadOnly(bool)` | 查询或设置 collection 是否只读。 | 修改模式应在 setup 前设置；只读会禁止写操作。 |
| `QString error() const` | 返回最近一次错误描述。 | 应在失败返回后立即读取，后续调用可能覆盖错误信息。 |
| `bool registerDocumentation(const QString &documentationFileName)` | 注册 qch 文档包。 | namespace 必须唯一；只读或文件无效时失败。 |
| `bool unregisterDocumentation(const QString &namespaceName)` | 按 namespace 注销 qch。 | 参数是 namespace，不是 qch 文件名；写权限和 setup 必须满足。 |
| `QStringList registeredDocumentations() const` | 返回已注册文档的 namespace 列表。 | 返回的是身份名，不是物理路径。 |
| `QString documentationFileName(const QString &namespaceName)` | 由 namespace 查找 qch 文件绝对路径。 | 未注册时返回空字符串。 |
| `static QString namespaceName(const QString &documentationFileName)` | 从 qch 文件读取 namespace。 | 文件无效时返回空值；不需要 engine。 |
| `static QVariant metaData(const QString &documentationFileName, const QString &name)` | 读取 qch 创建时写入的元数据。 | 没有该字段时返回无效 `QVariant`；元数据不能在这里修改。 |
| `QByteArray fileData(const QUrl &url) const` | 读取 qthelp URL 对应文件的字节内容。 | 找不到文件返回空数组；调用方负责解码和渲染。 |
| `QUrl findFile(const QUrl &url) const` | 解析虚拟文件夹并返回实际存在的 qthelp URL。 | namespace 不匹配或文件不存在时可能返回无效 URL。 |
| `QList<QUrl> files(QString namespaceName, const QString &filterName, const QString &extensionFilter = {})` | 列出指定 namespace 中符合 filter 和扩展名的文件。 | `extensionFilter` 例如 `html`；结果依赖 filter。 |
| `QList<QUrl> files(QString namespaceName, const QStringList &filterAttributes, const QString &extensionFilter = {})` | 使用属性集合列出文档文件。 | 这是旧式过滤接口，新代码优先使用 filter engine。 |
| `QList<QHelpLink> documentsForIdentifier(const QString &id) const` | 按标识符查找当前 filter 下的文档链接。 | 结果可能为空；当前 filter 会影响结果。 |
| `QList<QHelpLink> documentsForIdentifier(const QString &id, const QString &filterName) const` | 按指定 filter 查找标识符对应链接。 | 传空 filter 名称可请求不经过特定 filter 的结果。 |
| `QList<QHelpLink> documentsForKeyword(const QString &keyword) const` | 按关键词查找当前 filter 下的文档链接。 | 关键词索引未注册或 filter 排除文档时会为空。 |
| `QList<QHelpLink> documentsForKeyword(const QString &keyword, const QString &filterName) const` | 按指定 filter 查找关键词链接。 | 注意 filter 名称与 active filter 不是同一个概念。 |
| `QHelpFilterEngine *filterEngine() const` | 返回关联的过滤器引擎。 | 由核心引擎管理；使用新过滤器功能还要启用 `setUsesFilterEngine(true)`。 |
| `void setUsesFilterEngine(bool)` / `bool usesFilterEngine() const` | 开启或查询新式 filter engine。 | 需在依赖过滤结果的目录、索引和搜索操作前统一配置。 |
| `void setAutoSaveFilter(bool)` / `bool autoSaveFilter() const` | 控制 active filter 是否持久化到 collection。 | 默认开启；只读或不可写时保存可能失败。 |
| `QStringList customFilters() const` | 返回旧式自定义 filter 名称。 | 兼容旧 API；新代码优先使用 `QHelpFilterEngine::filters()`。 |
| `bool addCustomFilter(const QString &, const QStringList &)` | 添加旧式 filter 和属性列表。 | 会修改 collection，需可写且 setup 完成。 |
| `bool removeCustomFilter(const QString &)` | 删除旧式自定义 filter。 | 不要与新 filter engine 的名称混用。 |
| `QStringList filterAttributes() const` | 返回所有可用旧式 filter 属性。 | 属性来自已注册文档，适用于兼容旧接口。 |
| `QStringList filterAttributes(const QString &filterName) const` | 返回指定旧式 filter 的属性。 | filter 不存在时返回空列表。 |
| `QList<QStringList> filterAttributeSets(const QString &namespaceName) const` | 返回某 namespace 提供的属性集合。 | 用于旧式属性过滤；不等于新式 `QHelpFilterData`。 |
| `QString currentFilter() const` / `setCurrentFilter(const QString &)` | 读取或修改旧式当前 filter。 | 兼容旧 API；新代码使用 `QHelpFilterEngine::activeFilter()`。 |
| `QVariant customValue(const QString &key, const QVariant &defaultValue = {}) const` | 读取 collection settings 中的应用值。 | 键不存在时返回传入的默认值。 |
| `bool setCustomValue(const QString &key, const QVariant &value)` | 持久化一个应用自定义键值。 | 覆盖同名键；只读或写失败时返回 `false`。 |
| `bool removeCustomValue(const QString &key)` | 删除 collection settings 中的键。 | 键不存在或无法写入时返回 `false`。 |
| `[signal] void setupStarted()` | setup 开始时发出。 | 期间不要把引擎数据当作可用。 |
| `[signal] void setupFinished()` | setup 完成时发出。 | 连接后再刷新目录、索引或搜索组件。 |
| `[signal] void warning(const QString &msg)` | 发生非致命问题时发出。 | 警告不一定让 API 失败，但应记录并结合结果判断。 |
| `[signal] void currentFilterChanged(const QString &)` | 旧式当前 filter 改变时发出。 | 兼容旧 API；新式过滤器监听 `filterActivated`。 |
| `[signal] void readersAboutToBeInvalidated()` | collection reader 即将失效时通知。 | 需要长期读取器的内部集成代码应在此之前停止使用。 |
| `[since Qt 6.8, future] requestContentForCurrentFilter()` | 异步请求当前 filter 的目录数据。 | 仅在启用 future 配置时可用；按 `QFuture` 生命周期消费结果。 |
| `[since Qt 6.8, future] requestContent(const QString &)` | 异步请求指定 filter 的目录数据。 | 结果对应请求时的 filter，不要与后来切换的 active filter 混淆。 |
| `[since Qt 6.8, future] requestIndexForCurrentFilter()` | 异步请求当前 filter 的索引词列表。 | 需要 future 配置和可用 collection。 |
| `[since Qt 6.8, future] requestIndex(const QString &)` | 异步请求指定 filter 的索引词列表。 | 读取结果前确认 future 已完成或正确处理取消。 |

## 一句话总结

`QHelpEngineCore` 的核心节奏是：配置只读模式，调用 `setupData()`，注册 qch，按 filter 查询 qthelp URL，再用 `fileData()` 读取内容。
