# QHelpContentWidget
> Qt 6.11.1 · Qt Help · 来自 `QHelpContentWidget`

## 1. 先建立直觉

`QHelpContentWidget` 是帮助目录树的现成 `QTreeView`。用户点击目录项时，它发出链接信号，应用负责把 URL 显示到 HTML 查看器里。

## 2. 类说明

保留类说明：这些 API 来自 `QHelpContentWidget`，属于 Qt Help 模块，用于显示帮助目录树。

它通常由 `QHelpEngine::contentWidget()` 创建和管理，已经和 content model 配好。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `indexOf(link)` | 查找某个帮助链接对应的目录索引。 |
| `linkActivated(link)` | 用户激活目录项时发出。 |

## 4. 典型流程

```cpp
connect(engine->contentWidget(), &QHelpContentWidget::linkActivated,
        this, &HelpWindow::showHelpUrl);
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 帮助侧栏目录 | 直接嵌入 splitter 或 dock。 |
| 当前页面同步目录 | `indexOf(url)` 后选中/展开。 |
| 多文档包统一目录 | 依赖 engine 注册的 qch 和 active filter。 |

## 6. 常见坑与经验

它只显示目录，不显示页面内容。你需要自己实现 `showHelpUrl()`，通常用 `fileData()` 取 HTML。

`indexOf()` 找不到时返回无效索引，要检查 `isValid()`。

## 7. 知识点覆盖

- 目录树视图和链接激活。
- URL 到目录项同步。
- 与 HTML 查看器的分工。
