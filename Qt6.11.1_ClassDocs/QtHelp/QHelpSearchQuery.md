# QHelpSearchQuery
> Qt 6.11.1 · Qt Help · 来自 `QHelpSearchQuery`

## 1. 先建立直觉

`QHelpSearchQuery` 表示结构化搜索条件：在哪个字段里查，查哪些词。现代常用入口是 `QHelpSearchEngine::search(QString)`，但理解它有助于看旧代码和自定义查询 UI。

## 2. 类说明

保留类说明：这些 API 来自 `QHelpSearchQuery`，属于 Qt Help 模块，用于描述帮助搜索查询项。

它是小值对象，包含 `FieldName` 和词列表。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QHelpSearchQuery()` | 创建空查询。 |
| `QHelpSearchQuery(field, wordList)` | 创建指定字段和关键词列表的查询。 |
| `fieldName` / `wordList` | 公共数据成员，用来表达搜索字段和词。 |

## 4. 使用场景

| 场景 | 用法 |
| --- | --- |
| 兼容旧帮助搜索接口 | 构造结构化查询列表。 |
| 高级搜索 UI | 把不同字段条件拆成多个 query。 |
| 调试搜索输入解析 | 查看用户输入如何变成词列表。 |

## 5. 常见坑与经验

不要把它误认为搜索结果。它只是输入条件；结果是 `QHelpSearchResult`。

搜索语法和分词体验由 Qt Help 搜索引擎决定，不等于数据库全文检索或网页搜索。

## 6. 知识点覆盖

- 帮助搜索条件对象。
- 字段搜索和词列表。
- 查询对象与结果对象的区别。
