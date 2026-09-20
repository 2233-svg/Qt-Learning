# QHelpEngine
> Qt 6.11.1 · Qt Help · 来自 `QHelpEngine`

## 1. 先建立直觉

`QHelpEngine` 是带现成模型和 widget 的帮助引擎。它继承 `QHelpEngineCore` 的后端能力，并提供目录树、索引列表和搜索引擎组件，适合快速搭一个 Qt Assistant 风格的内嵌帮助界面。

## 2. 类说明

保留类说明：这些 API 来自 `QHelpEngine`，属于 Qt Help 模块，用于把帮助后端与内容/索引/搜索 UI 组件组合起来。

如果你只需要读取 qch 资源，用 `QHelpEngineCore` 更轻；如果需要 `contentWidget()`、`indexWidget()`、`searchEngine()`，用 `QHelpEngine`。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QHelpEngine(collectionFile)` | 创建完整帮助引擎。 |
| `contentModel()` | 返回帮助目录树模型。 |
| `contentWidget()` | 返回目录树视图。 |
| `indexModel()` | 返回索引关键词模型。 |
| `indexWidget()` | 返回索引视图。 |
| `searchEngine()` | 返回搜索引擎和搜索 UI 组件。 |
| 继承的 `setupData()` | 初始化 collection 数据。 |
| 继承的 `fileData()` | 读取 qthelp URL 内容。 |

## 4. 典型流程

```cpp
auto *engine = new QHelpEngine("help.qhc", this);
if (!engine->setupData())
    qWarning() << engine->error();

connect(engine->contentWidget(), &QHelpContentWidget::linkActivated,
        this, &HelpWindow::showHelpUrl);
connect(engine->indexWidget(), &QHelpIndexWidget::documentsActivated,
        this, &HelpWindow::showIndexResults);
```

## 5. 使用场景

| 场景 | 为什么适合 |
| --- | --- |
| 内嵌帮助中心 | 目录、索引、搜索组件都现成。 |
| 桌面产品离线文档 | 注册 qch 后用 QTextBrowser/WebEngine 显示 HTML。 |
| 插件化文档 | core 管注册，engine 提供统一 UI。 |

## 6. 常见坑与经验

这些 widget/model 依赖 setup 后的数据。过早取出来连接 UI 可以，但真正显示前要确保 `setupData()` 成功。

`QHelpEngine` 不负责 HTML 渲染器。目录或搜索结果给你 URL，你还需要用 `QTextBrowser`、`QWebEngineView` 或自定义查看器显示 `fileData()`。

## 7. 知识点覆盖

- 完整帮助引擎和 core 的区别。
- 内容树、索引、搜索组件组合。
- qthelp URL 到 HTML 查看器的连接。
