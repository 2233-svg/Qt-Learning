# QHelpSearchEngineCore
> Qt 6.11.1 · Qt Help · 来自 `QHelpSearchEngineCore`

## 1. 先建立直觉

`QHelpSearchEngineCore` 是无界面的帮助全文搜索引擎。它依靠 `QHelpEngineCore` 访问已注册文档，建立索引，执行搜索，并返回 `QHelpSearchResult` 列表。

## 2. 类说明

保留类说明：这些 API 来自 `QHelpSearchEngineCore`，属于 Qt Help 模块，用于帮助文档索引和搜索的后端能力。

带 UI 的 `QHelpSearchEngine` 在它基础上提供查询控件和结果控件。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QHelpSearchEngineCore(helpEngine, parent)` | 绑定帮助核心引擎创建搜索后端。 |
| `reindexDocumentation()` | 重建搜索索引。 |
| `cancelIndexing()` | 取消索引过程。 |
| `search(input)` | 开始搜索。 |
| `cancelSearching()` | 取消搜索。 |
| `searchInput()` | 返回最近搜索文本。 |
| `searchResultCount()` | 返回结果数量。 |
| `searchResults(start, end)` | 分页取得结果。 |
| `indexingStarted/Finished` | 索引生命周期信号。 |
| `searchingStarted/Finished` | 搜索生命周期信号。 |

## 4. 典型流程

```cpp
auto *search = new QHelpSearchEngineCore(&helpEngine, this);
connect(search, &QHelpSearchEngineCore::searchingFinished, this, [=] {
    auto results = search->searchResults(0, search->searchResultCount() - 1);
    showResults(results);
});
search->reindexDocumentation();
search->search("model view");
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 自定义搜索 UI | 后端用 core，界面完全自己写。 |
| 命令式文档搜索 | 输入字符串，取结果列表。 |
| 文档包动态变化 | 注册/注销 qch 后重建索引。 |

## 6. 常见坑与经验

搜索依赖索引。文档刚注册后不重建索引，结果可能不包含新文档。

索引和搜索是有生命周期的，UI 要处理 started/finished/cancel 状态，避免重复按钮乱点导致状态混乱。

结果区间要合法。结果为空时不要请求 0 到 -1 这种范围。

## 7. 知识点覆盖

- 帮助文档全文索引。
- 搜索生命周期和取消。
- 分页读取搜索结果。
