# QHelpSearchEngineCore：不带界面的 Qt Help 全文搜索核心

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHelpSearchEngineCore>`  
> 所属模块：`Qt6::Help`  
> 引入版本：Qt 6.8  
> 继承：`QObject`

## 它解决什么问题

`QHelpSearchEngineCore` 只提供 Qt Help 的文档索引和全文搜索能力，不创建搜索输入框或结果控件。它适合后台服务、自定义 QWidget/QML 界面、命令行工具，或希望完全控制结果展示的应用。

它与 `QHelpSearchEngine` 共用相同的搜索模型：都依赖 `QHelpEngineCore` 访问 collection，都在 setup 后建立索引，都使用 SQLite FTS5 查询表达式。区别是 Core 版本没有 `queryWidget()`、`resultWidget()`，也没有带结果数量的 `searchingFinished(int)`。

## 实际使用场景

- 在自定义列表、表格或 QML 页面中显示搜索结果。
- 后台建立帮助索引，界面只接收搜索开始/完成信号。
- 应用不链接 Qt Widgets，却需要查询 qthelp 文档。
- 需要自行做分页、排序、过滤或结果缓存。

## 创建与生命周期

构造函数需要 `QHelpEngineCore *`：

```cpp
auto *helpEngine = new QHelpEngineCore(collectionFile, this);
auto *searchCore = new QHelpSearchEngineCore(helpEngine, this);

connect(searchCore, &QHelpSearchEngineCore::indexingFinished,
        this, &HelpService::enableSearch);
connect(searchCore, &QHelpSearchEngineCore::searchingFinished,
        this, &HelpService::readResults);

helpEngine->setupData();
```

`QHelpSearchEngineCore` 不拥有传入的 `QHelpEngineCore`。两个对象必须同时存活，且应在各自所属线程中调用。它们是 QObject，适合用父子对象管理生命周期；帮助引擎析构后，搜索核心不能继续访问 collection。

构造时会把帮助核心的 `setupFinished()` 与索引流程连接起来。索引和搜索是事件驱动的异步流程，必须运行事件循环并监听信号；不要在调用 `search()` 后立刻读取结果并假定已经完成。

## 工作流程

1. 创建 `QHelpEngineCore` 和 `QHelpSearchEngineCore`。
2. 调用帮助核心的 setup，并等待索引开始、完成信号。
3. 收到 `indexingFinished()` 后调用 `search(QString)`。
4. 收到 `searchingFinished()` 后调用 `searchResultCount()`，再按范围调用 `searchResults(start, end)`。
5. 下一次搜索开始后，旧结果数量和旧结果列表不再代表当前查询。

`reindexDocumentation()` 强制重建所有文档索引。`scheduleIndexDocumentation()` 只是安排索引工作，调用返回不代表索引已完成。取消操作同样通过状态流程处理，不应把取消当作成功完成。

## 搜索表达式

`search()` 的参数是 SQLite FTS5 风格的文本查询：

- 普通多个词默认按 AND 处理。
- `AND`、`OR`、`NOT` 只有全大写时才是逻辑操作符。
- `"exact phrase"` 表示精确短语。
- 更复杂的匹配规则应按 FTS5 查询语法编写。

`searchInput()` 返回最近一次搜索短语，`searchResultCount()` 返回当前搜索结果数量。由于 Core 版的 `searchingFinished()` 没有参数，完成信号槽中应主动读取 `searchResultCount()`。

## 自定义结果界面

```cpp
connect(searchCore, &QHelpSearchEngineCore::searchingFinished,
        this, [this, searchCore] {
            const int count = searchCore->searchResultCount();
            const auto results = searchCore->searchResults(0, count);
            updateResultView(results);
        });

searchCore->search(QStringLiteral("QHelpEngine AND setup"));
```

生产代码应根据分页尺寸计算 `end`，不要在结果数量很大时无条件一次性读取全部结果。`QHelpSearchResult` 提供标题、URL 和摘要，正文打开仍由应用负责。

## 与 QHelpSearchEngine 的选择

选择 `QHelpSearchEngineCore`，当你需要纯核心能力、不需要 Qt Widgets，或已经有自己的查询框和结果视图。选择 `QHelpSearchEngine`，当你希望直接复用 Qt Help 提供的 `QHelpSearchQueryWidget` 和 `QHelpSearchResultWidget`。

不要同时为同一个 `QHelpEngineCore` 随意创建多个搜索对象并重复重建索引，除非确实需要隔离查询状态；多个对象会让索引和完成信号的管理更复杂。

## 常见误区

- 把它当作 `QHelpSearchEngine` 使用：它没有 GUI 控件。
- 在 `searchingFinished()` 信号中读取信号参数：该信号没有参数，应调用 `searchResultCount()`。
- 忽略 `setupFinished()` 和 `indexingFinished()`，直接把空结果当成无命中。
- 调用 `scheduleIndexDocumentation()` 后立即访问结果。
- 在新搜索开始后继续显示旧查询的分页数据。
- 在错误线程直接操作 QObject 或底层帮助引擎。

## 逐项 API 说明

### `[explicit] QHelpSearchEngineCore::QHelpSearchEngineCore(QHelpEngineCore *helpEngine, QObject *parent = nullptr)`

创建无界面搜索核心，使用 `helpEngine` 访问需要索引的文档，并安排 setup 完成后的索引流程。`helpEngine` 不转移所有权，生命周期必须覆盖搜索核心。

### `[override virtual noexcept] QHelpSearchEngineCore::~QHelpSearchEngineCore()`

销毁搜索核心及其搜索状态。传入的 `QHelpEngineCore` 由调用者管理，不会因为搜索核心析构而自动成为可用对象。

### `[slot] void QHelpSearchEngineCore::reindexDocumentation()`

强制重新索引所有帮助文档。索引开始和结束由 `indexingStarted()`、`indexingFinished()` 通知。

### `[slot] void QHelpSearchEngineCore::cancelIndexing()`

停止当前索引工作。取消后不能假定索引覆盖了所有文档，需要时重新调用索引接口并等待完成信号。

### `[slot] void QHelpSearchEngineCore::scheduleIndexDocumentation()`

安排索引动作在事件循环中执行。它是排队/调度入口，不是同步完成接口；索引是否结束以 `indexingFinished()` 为准。

### `[slot] void QHelpSearchEngineCore::search(const QString &searchInput)`

按给定 FTS5 查询表达式开始搜索。调用后监听 `searchingStarted()` 和 `searchingFinished()`，不要同步读取结果。

### `[slot] void QHelpSearchEngineCore::cancelSearching()`

停止当前搜索。取消过程后，当前结果状态不应被当成新查询的成功结果。

### `QString QHelpSearchEngineCore::searchInput() const`

返回最近一次提交的搜索表达式，而不是外部编辑控件的草稿内容。

### `int QHelpSearchEngineCore::searchResultCount() const`

返回当前搜索找到的结果数量。由于完成信号不携带数量，通常在 `searchingFinished()` 槽中读取它。

### `QList<QHelpSearchResult> QHelpSearchEngineCore::searchResults(int start, int end) const`

返回指定范围内的结果，用于分页或自定义视图。范围应依据当前的 `searchResultCount()` 计算，新搜索开始后应丢弃旧列表。

### `[signal] void QHelpSearchEngineCore::indexingStarted()`

索引开始时发出，适合更新后台任务状态或暂时禁用搜索。

### `[signal] void QHelpSearchEngineCore::indexingFinished()`

索引完成时发出。此后才适合把搜索功能视为正常可用。

### `[signal] void QHelpSearchEngineCore::searchingStarted()`

搜索开始时发出，适合清理旧的结果视图和显示加载状态。

### `[signal] void QHelpSearchEngineCore::searchingFinished()`

搜索完成时发出，但不携带结果数量。槽函数应调用 `searchResultCount()`，再调用 `searchResults()` 读取结果。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit QHelpSearchEngineCore(QHelpEngineCore *helpEngine, QObject *parent = nullptr)` | 创建无 GUI 的搜索核心。 | 不拥有 `helpEngine`；需要 setup 和事件循环。 |
| 析构 | `~QHelpSearchEngineCore()` | 销毁搜索核心。 | 不会替调用者管理传入的帮助引擎。 |
| 索引槽 | `void reindexDocumentation()` | 强制重建全部文档索引。 | 以 `indexingFinished()` 判断完成。 |
| 索引槽 | `void cancelIndexing()` | 取消索引。 | 取消后不要假定索引完整。 |
| 索引槽 | `void scheduleIndexDocumentation()` | 排队或安排索引动作。 | 不保证立即执行或立即完成。 |
| 搜索槽 | `void search(const QString &searchInput)` | 按 FTS5 表达式启动搜索。 | 普通多词默认 AND，逻辑词必须大写。 |
| 搜索槽 | `void cancelSearching()` | 取消搜索。 | 取消状态不要当作新结果。 |
| 查询 | `QString searchInput() const` | 返回最近一次搜索表达式。 | 与外部输入框草稿不同。 |
| 查询 | `int searchResultCount() const` | 返回当前结果数量。 | Core 版完成信号无参数，需主动读取。 |
| 查询 | `QList<QHelpSearchResult> searchResults(int start, int end) const` | 按范围读取搜索结果。 | 用当前数量计算范围；新搜索后旧列表失效。 |
| 信号 | `void indexingStarted()` | 通知索引开始。 | 更新后台状态。 |
| 信号 | `void indexingFinished()` | 通知索引完成。 | 之后再正常搜索。 |
| 信号 | `void searchingStarted()` | 通知搜索开始。 | 清理旧结果。 |
| 信号 | `void searchingFinished()` | 通知搜索完成。 | 调用 `searchResultCount()` 获取数量。 |

---

### 一句话总结

`QHelpSearchEngineCore` 是 Qt Help 的纯搜索核心：没有 GUI，依赖 `QHelpEngineCore`，通过索引/搜索信号驱动自定义结果界面。
