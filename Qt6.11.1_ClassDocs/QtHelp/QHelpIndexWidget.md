# QHelpIndexWidget
> Qt 6.11.1 · Qt Help · 来自 `QHelpIndexWidget`

## 1. 先建立直觉

`QHelpIndexWidget` 是帮助索引的现成 `QListView`。它显示关键词，支持过滤，并在用户激活条目时发出一个或多个帮助文档链接。

## 2. 类说明

保留类说明：这些 API 来自 `QHelpIndexWidget`，属于 Qt Help 模块，用于显示和激活帮助索引关键词。

它通常由 `QHelpEngine::indexWidget()` 提供。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `filterIndices(filter, wildcard)` | 按输入文本过滤索引项。 |
| `activateCurrentItem()` | 激活当前选中的索引项。 |
| `documentActivated(document, keyword)` | 激活后只有一个匹配文档时发出。 |
| `documentsActivated(documents, keyword)` | 激活后有多个匹配文档时发出。 |

## 4. 典型流程

```cpp
connect(indexWidget, &QHelpIndexWidget::documentsActivated,
        this, &HelpWindow::showIndexChoices);
indexWidget->filterIndices(searchEdit->text());
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 帮助索引侧栏 | 嵌入 QListView 风格索引。 |
| 关键词快速跳转 | 用户输入过滤并回车激活。 |
| 多候选文档 | 展示 choices，让用户选具体页面。 |

## 6. 常见坑与经验

不要假设关键词唯一。许多 API 名或概念可能在多个模块文档中出现。

`filterIndices()` 的 wildcard 参数适合高级匹配，但普通搜索框先用简单 filter 更直观。

## 7. 知识点覆盖

- 帮助索引 UI。
- 关键词过滤和激活。
- 单文档/多文档结果处理。
