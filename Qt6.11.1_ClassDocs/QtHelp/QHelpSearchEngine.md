# QHelpSearchEngine
> Qt 6.11.1 · Qt Help · 来自 `QHelpSearchEngine`

## 1. 先建立直觉

`QHelpSearchEngine` 是带现成 UI 控件的帮助搜索引擎。它负责索引和搜索，同时提供 `queryWidget()` 和 `resultWidget()`，适合快速搭建帮助中心搜索页。

## 2. 类说明

保留类说明：这些 API 来自 `QHelpSearchEngine`，属于 Qt Help 模块，用于帮助文档搜索并提供搜索输入/结果显示控件。

它和 `QHelpSearchEngineCore` 的核心差异是：多了现成 widget，以及 `searchingFinished(int)` 带结果数量。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QHelpSearchEngine(helpEngine, parent)` | 基于帮助引擎创建搜索引擎。 |
| `queryWidget()` | 返回搜索输入控件。 |
| `resultWidget()` | 返回搜索结果显示控件。 |
| `search(input)` | 开始搜索。 |
| `reindexDocumentation()` | 重建索引。 |
| `cancelIndexing()` / `cancelSearching()` | 取消索引或搜索。 |
| `searchInput()`、`searchResultCount()`、`searchResults()` | 查询搜索状态和结果。 |
| `indexingStarted/Finished`、`searchingStarted/Finished(count)` | 生命周期信号。 |

## 4. 典型流程

```cpp
auto *search = engine->searchEngine();
layout->addWidget(search->queryWidget());
layout->addWidget(search->resultWidget());

connect(search->resultWidget(), &QHelpSearchResultWidget::requestShowLink,
        this, &HelpWindow::showHelpUrl);
```

## 5. 使用场景

| 场景 | 为什么适合 |
| --- | --- |
| 内嵌帮助搜索页 | 输入框和结果列表都现成。 |
| 快速替代 Qt Assistant 部分功能 | 复用搜索 UI。 |
| 简单文档中心 | 目录、索引、搜索三件套都来自 `QHelpEngine`。 |

## 6. 常见坑与经验

query widget 只负责输入，result widget 只负责显示和发链接。真正打开页面仍由你的窗口处理。

首次使用前要确保帮助引擎 setup 成功，并考虑重建索引。索引不完整时，搜索体验会像“文档丢了”。

## 7. 知识点覆盖

- 帮助搜索后端与现成 UI。
- 查询控件、结果控件和页面打开逻辑。
- 索引/搜索状态管理。
