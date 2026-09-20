# QHelpSearchResult
> Qt 6.11.1 · Qt Help · 来自 `QHelpSearchResult`

## 1. 先建立直觉

`QHelpSearchResult` 是一条帮助搜索结果：目标 URL、标题和摘要片段。它是搜索完成后给 UI 展示的最小数据单元。

## 2. 类说明

保留类说明：这些 API 来自 `QHelpSearchResult`，属于 Qt Help 模块，用于保存单条帮助搜索结果。

它是值类型，适合放进列表、分页读取、传给结果视图。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QHelpSearchResult()` | 创建空结果。 |
| `QHelpSearchResult(url, title, snippet)` | 创建完整结果。 |
| `url()` | 返回帮助页面链接。 |
| `title()` | 返回页面标题。 |
| `snippet()` | 返回命中片段。 |
| 拷贝/赋值 | 值类型操作。 |

## 4. 使用场景

| 场景 | 用法 |
| --- | --- |
| 搜索结果列表 | 显示 title/snippet，点击打开 url。 |
| 分页加载结果 | `searchResults(start, end)` 返回列表。 |
| 自定义结果排序/过滤 | 在 UI 层处理结果值对象。 |

## 5. 常见坑与经验

snippet 是展示摘要，不是完整正文。打开文档仍要用 `url()` 读取页面。

搜索结果 URL 通常是 qthelp URL，需要你的帮助查看器能处理。

## 6. 知识点覆盖

- 搜索结果的 URL、标题、摘要。
- 结果展示和页面打开的分离。
- 值类型结果数据。
