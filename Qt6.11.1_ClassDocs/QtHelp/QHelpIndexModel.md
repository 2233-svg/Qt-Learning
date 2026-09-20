# QHelpIndexModel
> Qt 6.11.1 · Qt Help · 来自 `QHelpIndexModel`

## 1. 先建立直觉

`QHelpIndexModel` 是帮助索引关键词列表的 model。它把 `.qch` 中的 keyword/index 信息整理成可显示和可过滤的数据源。

## 2. 类说明

保留类说明：这些 API 来自 `QHelpIndexModel`，属于 Qt Help 模块，用于提供帮助索引关键词数据。

现成视图是 `QHelpIndexWidget`；自定义 UI 可以直接使用 model。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `createIndex(customFilterName)` | 按过滤器创建索引。 |
| `filter(filter, wildcard)` | 对索引关键词做文本过滤。 |
| `indexCreated()` / `indexCreationStarted()` | 索引创建完成/开始信号。 |
| `isCreatingIndex()` | 是否正在创建索引。 |
| `linksForKeyword(keyword)` | 查询关键词对应的帮助链接。 |

## 4. 典型流程

```cpp
auto *model = engine->indexModel();
model->createIndex(engine->filterEngine()->activeFilter());
auto links = model->linksForKeyword("QWidget");
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 自定义索引搜索框 | `filter()` 后显示关键词列表。 |
| 关键词跳转 | `linksForKeyword()` 找候选文档。 |
| filter 切换 | 重新 `createIndex()`。 |

## 6. 常见坑与经验

一个关键词可能对应多个文档，UI 要能让用户选择或展示候选列表。

索引创建状态要处理好。大型文档集里马上查询可能拿不到完整结果。

## 7. 知识点覆盖

- 帮助索引关键词模型。
- 关键词到链接的一对多关系。
- 索引创建和过滤。
