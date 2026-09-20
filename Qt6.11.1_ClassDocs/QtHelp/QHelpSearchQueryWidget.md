# QHelpSearchQueryWidget
> Qt 6.11.1 · Qt Help · 来自 `QHelpSearchQueryWidget`

## 1. 先建立直觉

`QHelpSearchQueryWidget` 是帮助搜索输入控件。用户在这里输入搜索词，它发出信号告诉搜索引擎开始搜索。

## 2. 类说明

保留类说明：这些 API 来自 `QHelpSearchQueryWidget`，属于 Qt Help 模块，用于提供帮助搜索输入 UI。

通常通过 `QHelpSearchEngine::queryWidget()` 获取。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `collapseExtendedSearch()` / `expandExtendedSearch()` | 折叠或展开高级搜索区域。 |
| `searchInput()` | 返回当前输入文本。 |
| `search()` | 用户请求搜索时发出。 |

## 4. 使用场景

| 场景 | 用法 |
| --- | --- |
| 帮助搜索栏 | 直接嵌入界面。 |
| 高级搜索开关 | 展开/折叠扩展搜索条件。 |
| 自定义触发搜索 | 连接 `search()` 到 search engine。 |

## 5. 常见坑与经验

控件发出搜索请求，不代表搜索一定完成。结果要监听 search engine 的 finished 信号。

如果你不用现成 `QHelpSearchEngine` 组合，也可以读取 `searchInput()` 后调用自己的搜索后端。

## 6. 知识点覆盖

- 搜索输入 UI。
- 简单/扩展搜索区域。
- 输入控件和搜索后端的分工。
