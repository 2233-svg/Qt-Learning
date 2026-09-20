# QHelpSearchEngine：为 Qt Help 提供索引、全文搜索和搜索控件

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHelpSearchEngine>`  
> 所属模块：`Qt6::Help`  
> 继承：`QObject`

## 它解决什么问题

`QHelpSearchEngine` 把帮助文档建立成全文索引，并提供异步搜索、搜索结果读取以及两个可复用的 QWidget：

- `queryWidget()`：用户输入搜索表达式。
- `resultWidget()`：显示搜索结果并发出链接请求。

它依赖一个已经存在的 `QHelpEngineCore` 访问 collection 和已注册文档。搜索引擎不替应用渲染正文，也不替应用决定用户点击链接后使用哪种浏览器。

## 实际使用场景

- 在应用帮助窗口中加入“搜索”页签。
- 首次加载帮助 collection 后建立全文索引，之后响应用户输入。
- 只取前 20 条结果做分页列表，避免一次性把大量结果放进自定义视图。
- 需要更强的排序、过滤或布局时，使用 `searchResults()` 自己构建结果界面。

## 初始化与所有权

构造函数需要 `QHelpEngineCore *`。引擎使用这个核心对象访问文档，并自动连接核心帮助引擎的 `setupFinished()`，使 setup 完成后可以安排索引：

```cpp
auto *helpEngine = new QHelpEngineCore(collectionFile, this);
auto *searchEngine = new QHelpSearchEngine(helpEngine, this);

connect(searchEngine, &QHelpSearchEngine::indexingStarted,
        this, &HelpWindow::showIndexing);
connect(searchEngine, &QHelpSearchEngine::indexingFinished,
        this, &HelpWindow::enableSearch);
connect(searchEngine, &QHelpSearchEngine::searchingFinished,
        this, &HelpWindow::showSearchResults);

helpEngine->setupData();
```

`QHelpSearchEngine` 不拥有传入的 `QHelpEngineCore`。两者必须在搜索引擎使用期间同时存活，通常把它们挂到同一个父对象下。`queryWidget()` 和 `resultWidget()` 返回的控件由搜索引擎管理，不能直接 `delete`，也不能通过公开构造函数自行创建 `QHelpSearchResultWidget`。

这是 QObject 类型，创建、调用和信号槽连接应遵守对象线程归属。搜索任务的完成通过信号通知；不要用定时器轮询猜测搜索是否结束。

## 正确的搜索状态机

1. `QHelpEngineCore` 完成 setup。
2. 搜索引擎发出 `indexingStarted()`，开始建立或更新索引。
3. 收到 `indexingFinished()` 后，才把搜索框当作可用状态。
4. 调用 `search(QString)`，引擎发出 `searchingStarted()`。
5. 收到 `searchingFinished(int)` 后，用结果数量和 `searchResults(start, end)` 读取结果。
6. 下一次搜索会更新当前搜索输入和结果；不要把上一次结果当成永久快照。

`reindexDocumentation()` 会强制重新索引所有帮助文档，适合 collection 内容发生变化或索引损坏后的恢复。`scheduleIndexDocumentation()` 只负责安排一次索引动作，不应被当作“索引已经完成”；完成时仍以 `indexingFinished()` 为准。

## 搜索表达式语义

`search(const QString &searchInput)` 使用 Qt Help 的 SQLite FTS5 查询语法：

- 多个普通词默认按 AND 处理，返回包含所有词的文档。
- `AND`、`OR`、`NOT` 必须写成全大写；小写形式会被当成搜索词的一部分。
- 双引号包住多个词时，按精确短语搜索，例如 `"event loop"`。
- 更复杂的表达式应遵循 SQLite FTS5 的全文查询规则，不能把它当作简单的 `QString::contains()`。

空表达式、语法不完整或尚未建立索引时，结果可能为空或由底层查询规则决定。界面应显示“没有结果”或查询错误状态，不要据此推断 collection 没有文档。

## 结果分页与快照边界

`searchingFinished(int searchResultCount)` 给出当前搜索的结果数量。随后调用 `searchResults(start, end)` 获取指定范围的 `QList<QHelpSearchResult>`。建议将 `start`、`end` 限制在当前结果数量范围内，并在开始下一次搜索后丢弃旧分页数据。

`searchInput()` 返回最近一次传给 `search()` 的搜索短语，不是 `QHelpSearchQueryWidget` 中尚未提交的编辑内容。要得到控件当前内容，应读取 `queryWidget()->searchInput()`。

## 复用官方控件

```cpp
auto *query = searchEngine->queryWidget();
auto *results = searchEngine->resultWidget();
layout->addWidget(query);
layout->addWidget(results);

connect(query, &QHelpSearchQueryWidget::search, this, [=] {
    searchEngine->search(query->searchInput());
});
connect(results, &QHelpSearchResultWidget::requestShowLink,
        this, &HelpWindow::showHelpUrl);
```

结果控件的内部连接由搜索引擎建立。若需要完全自定义结果界面，可以不使用 `resultWidget()`，在 `searchingFinished()` 中读取 `searchResults()`，再将 URL 交给自己的视图。

## 常见误区

- `QHelpSearchEngine` 构造函数不接受 collection 文件名，必须传入 `QHelpEngineCore`。
- 未等待索引完成就搜索，把空结果误判成搜索失败。
- 把 `setSearchInput()` 当成执行搜索；它只更新查询控件的输入。
- 直接构造或删除 `QHelpSearchResultWidget`；它只能从该搜索引擎取得并由引擎管理。
- 把 `searchingFinished(int)` 的数量当成永久有效；下一次搜索会替换当前结果。
- 连接 `search` 槽的旧重载时不消除歧义；Qt 6.7 以后推荐 `QString` 重载。

## 逐项 API 说明

### `[explicit] QHelpSearchEngine::QHelpSearchEngine(QHelpEngineCore *helpEngine, QObject *parent = nullptr)`

创建搜索引擎，使用 `helpEngine` 访问需要索引的帮助文档，并建立与帮助引擎 setup 完成信号的协作。`helpEngine` 不是所有权转移参数，必须保证其生命周期覆盖搜索引擎。

### `[virtual noexcept] QHelpSearchEngine::~QHelpSearchEngine()`

销毁搜索引擎及其内部状态。由 `queryWidget()` 和 `resultWidget()` 返回的控件也属于搜索引擎管理范围，销毁搜索引擎后不能继续使用。

### `QHelpSearchQueryWidget *QHelpSearchEngine::queryWidget()`

返回可复用的搜索输入控件。控件的扩展搜索状态由该控件自己管理；返回指针不转移所有权，应将它放入布局而不是手动删除。

### `QHelpSearchResultWidget *QHelpSearchEngine::resultWidget()`

返回显示搜索结果的控件。该控件不能直接构造，因为搜索引擎需要为它建立内部连接；应用只需取得指针并放入布局。

### `[slot] void QHelpSearchEngine::reindexDocumentation()`

强制重新索引所有帮助文档。索引过程是状态变化流程，使用 `indexingStarted()` 和 `indexingFinished()` 判断开始和结束；调用本身不返回索引结果。

### `[slot] void QHelpSearchEngine::cancelIndexing()`

停止当前索引过程。取消后不能把已有索引当作刚刚完成的完整索引，应用应根据后续状态决定是否重新安排索引。

### `[slot] void QHelpSearchEngine::search(const QString &searchInput)`

使用给定表达式启动搜索。它是异步工作流的入口，开始和完成分别由 `searchingStarted()`、`searchingFinished(int)` 通知。该槽存在旧的 `QList<QHelpSearchQuery>` 重载，连接时要明确选择 `QString` 重载。

### `[slot] void QHelpSearchEngine::cancelSearching()`

停止当前搜索过程。取消后不要继续使用原搜索请求对应的结果数量作为新结果；下一次搜索仍应等待新的完成信号。

### `[slot] void QHelpSearchEngine::scheduleIndexDocumentation()`

安排索引文档动作，使索引在合适的事件循环时机执行。它不是同步索引调用，也不保证调用返回时已产生可搜索结果；使用 `indexingFinished()` 判断完成。

### `QString QHelpSearchEngine::searchInput() const`

返回最近一次提交给 `search()` 的搜索表达式。它反映引擎的当前查询，不等同于输入控件中用户尚未点击搜索按钮的文本。

### `int QHelpSearchEngine::searchResultCount() const`

返回当前搜索找到的结果数量。通常在 `searchingFinished(int)` 后读取或直接使用信号参数；新搜索开始后该数量可能被更新。

### `QList<QHelpSearchResult> QHelpSearchEngine::searchResults(int start, int end) const`

返回 `start` 到 `end` 范围内的搜索结果。返回值是按值传递的结果列表，适合分页；应使用当前搜索的结果数量约束范围，并在新搜索开始后丢弃旧结果。

### `[signal] void QHelpSearchEngine::indexingStarted()`

索引过程开始时发出。适合禁用搜索、显示忙碌状态或阻止重复索引请求。

### `[signal] void QHelpSearchEngine::indexingFinished()`

索引过程完成时发出。收到该信号后，搜索索引才适合用于正常搜索。

### `[signal] void QHelpSearchEngine::searchingStarted()`

搜索过程开始时发出。适合清空旧结果、显示加载状态和禁用重复提交。

### `[signal] void QHelpSearchEngine::searchingFinished(int searchResultCount)`

搜索完成时发出，参数是当前结果数量。收到信号后调用 `searchResults()` 读取具体的 `QHelpSearchResult`。

## 过时接口与迁移

Qt 6.7 起推荐使用字符串查询表达式和 `QHelpSearchResult`。以下接口保留旧代码兼容性，不应用于新代码：

- `SearchHit`：`QPair<QString, QString>`，旧结果只保存文档路径和页面标题，使用 `QHelpSearchResult` 替代。
- `hitsCount()`、`hitCount()`：使用 `searchResultCount()`。
- `hits(start, end)`：使用 `searchResults(start, end)`。
- `query()`：使用 `searchInput()`。
- `search(const QList<QHelpSearchQuery> &)`：使用 `search(const QString &)`。
- `QHelpSearchQuery` 的 `fieldName` 和 `wordList`：改写为 SQLite FTS5 查询表达式。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit QHelpSearchEngine(QHelpEngineCore *helpEngine, QObject *parent = nullptr)` | 创建连接到帮助核心引擎的搜索引擎。 | 不转移 `helpEngine` 所有权；需保证其先完成 setup。 |
| 析构 | `~QHelpSearchEngine()` | 销毁搜索引擎和其管理的搜索控件。 | 返回的控件不能脱离引擎继续使用。 |
| 获取控件 | `QHelpSearchQueryWidget *queryWidget()` | 返回搜索输入控件。 | 放入布局即可，不要手动删除。 |
| 获取控件 | `QHelpSearchResultWidget *resultWidget()` | 返回搜索结果控件。 | 不能直接构造，内部连接由引擎建立。 |
| 索引槽 | `void reindexDocumentation()` | 强制重建全部文档索引。 | 以 `indexingFinished()` 判断完成。 |
| 索引槽 | `void cancelIndexing()` | 取消当前索引。 | 取消后不要假定索引完整。 |
| 索引槽 | `void scheduleIndexDocumentation()` | 排队或安排索引动作。 | 不保证立即执行或立即完成。 |
| 搜索槽 | `void search(const QString &searchInput)` | 按 FTS5 表达式启动搜索。 | 普通多词默认 AND；逻辑词须大写。 |
| 搜索槽 | `void cancelSearching()` | 取消当前搜索。 | 取消后的结果不能当作新请求结果。 |
| 查询 | `QString searchInput() const` | 返回最近一次提交的搜索表达式。 | 不是查询控件里尚未提交的文本。 |
| 查询 | `int searchResultCount() const` | 返回当前结果数量。 | 通常在完成信号后读取。 |
| 查询 | `QList<QHelpSearchResult> searchResults(int start, int end) const` | 按范围取得结果，用于分页或自定义视图。 | 受当前搜索快照影响，新搜索后应丢弃旧列表。 |
| 信号 | `void indexingStarted()` | 通知索引开始。 | 更新界面忙碌状态。 |
| 信号 | `void indexingFinished()` | 通知索引完成。 | 之后再进行正常搜索。 |
| 信号 | `void searchingStarted()` | 通知搜索开始。 | 清理旧结果并显示加载状态。 |
| 信号 | `void searchingFinished(int searchResultCount)` | 通知搜索完成并给出数量。 | 在此后读取 `searchResults()`。 |
| 已废弃 | `SearchHit`、`hitsCount()`、`hitCount()`、`hits()` | 旧版路径/标题结果接口。 | 用 `QHelpSearchResult` 和对应新 API 替代。 |
| 已废弃 | `query()`、`search(const QList<QHelpSearchQuery> &)` | 旧版结构化查询接口。 | 用 `QString` FTS5 查询表达式替代。 |

---

### 一句话总结

`QHelpSearchEngine` 管理 Qt Help 的全文索引和搜索流程：先完成 setup 与索引，再搜索，最后在完成信号中分页读取结果或使用引擎管理的搜索控件。
