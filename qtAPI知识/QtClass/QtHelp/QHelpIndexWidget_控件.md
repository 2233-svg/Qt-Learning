# QHelpIndexWidget：把帮助索引词变成可激活的列表

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHelpIndexWidget>`  
> 所属模块：`Qt6::Help`  
> 继承：`QListView`  
> 定位：帮助系统控件

## 它解决什么问题

`QHelpIndexWidget` 是展示 `QHelpIndexModel` 的列表视图。它把帮助文档注册得到的索引关键词呈现给用户，并把“用户激活了哪个关键词”转换成一个或多个 `QHelpLink`，交给应用打开正文。

它只负责索引列表和激活通知，不负责渲染帮助正文。正文可以由 `QTextBrowser`、`QWebEngineView` 或应用自己的文档查看器显示。

## 实际使用场景

- 在帮助窗口左侧放置“索引”页签，让用户按关键词查找 API、类名或概念。
- 用户输入过滤词时调用 `filterIndices()`，把最匹配的索引项设为当前项。
- 激活后只有一个文档时直接跳转；同一关键词对应多个文档时弹出选择列表。
- 与 `QHelpEngine::indexModel()`、`QHelpEngineCore::documentsForKeyword()` 和 `QHelpLink` 配合，建立关键词到正文 URL 的导航链路。

## 创建方式与所有权

`QHelpIndexWidget` 的构造函数是私有的，应用不能直接写 `new QHelpIndexWidget`，也不能在栈上创建。应通过 `QHelpEngine::indexWidget()` 获取：

```cpp
auto *helpEngine = new QHelpEngine(collectionFile, this);
helpEngine->setupData();

auto *indexWidget = helpEngine->indexWidget();
layout->addWidget(indexWidget);

connect(indexWidget, &QHelpIndexWidget::documentActivated,
        this, [this](const QHelpLink &document, const QString &) {
            showHelpDocument(document.url);
        });

connect(indexWidget, &QHelpIndexWidget::documentsActivated,
        this, [this](const QList<QHelpLink> &documents, const QString &) {
            chooseAndShowHelpDocument(documents);
        });
```

返回的控件由 `QHelpEngine` 管理，所有权不转移。帮助引擎销毁后，该控件、它使用的模型以及其中的索引项都不能继续访问。应在 GUI 线程中创建、放置和调用控件。

## 工作流程与边界

1. 先让 `QHelpEngine` 完成 `setupData()`，使 collection、文档注册和当前 filter 可用。
2. 从同一个 engine 取得 `indexWidget()`，把它交给布局管理。
3. 根据输入调用 `filterIndices()`；它会筛选索引，并把最佳匹配项设为当前项。
4. 用户双击、按回车或调用 `activateCurrentItem()` 后，连接 `documentActivated` 或 `documentsActivated`。
5. 应用读取 `QHelpLink::url`，决定如何加载正文；不要把激活信号当成“控件已经打开网页”。

`documentsActivated` 表示同一个关键词关联多个文档，参数中的每个 `QHelpLink` 都带有文档标题和 URL。应用需要自己决定显示哪个文档，或者向用户展示候选文档。

## 关键 API 语义

### `filterIndices()`

`filterIndices(filter, wildcard)` 将筛选请求交给索引模型，并把最佳匹配项设置为当前项。`wildcard` 默认是空字符串；调用者可以按自己的输入策略使用普通过滤词或通配条件。它不负责创建索引，索引生成应由 `QHelpIndexModel` 和 `QHelpEngine` 的流程完成。

筛选结果为空时，控件不会凭空生成文档链接。此时当前项可能无效，后续调用 `activateCurrentItem()` 不应假设一定会发出信号。

### `activateCurrentItem()`

该槽激活当前列表项，效果等同于用户触发当前项。当前项无效、索引尚未准备好或当前 filter 下没有关联文档时，不能假设会得到有效导航结果。

### `documentActivated()` 与 `documentsActivated()`

- `documentActivated(document, keyword)`：激活项对应一个应显示的文档。`keyword` 是触发导航的索引词。
- `documentsActivated(documents, keyword)`：激活项对应多个文档。列表中的对象只携带标题和 URL，不替应用完成选择或导航。

新的代码应优先使用这两个信号。旧版的 `linkActivated()` 和 `linksActivated()` 仍可能出现在头文件中，但已废弃。

## 常见误区

- 直接构造 `QHelpIndexWidget`：构造函数是私有的，只能从 `QHelpEngine` 获取。
- 把 `QHelpIndexWidget` 当作正文浏览器：它只展示关键词，正文加载需要应用处理。
- 在 `setupData()` 或索引创建完成前把空列表当成“没有帮助文档”。
- 只连接 `documentActivated`，忽略一个关键词对应多个文档时的 `documentsActivated`。
- 保存旧的 `QModelIndex` 或旧 URL，在切换 collection/filter 后继续使用。
- 删除 `indexWidget()` 返回的对象，造成与帮助引擎的所有权冲突。

## 与相关类型的分工

- `QHelpEngine`：创建并持有该控件和索引模型。
- `QHelpIndexModel`：提供关键词列表及索引筛选能力。
- `QHelpLink`：描述一个文档的标题和目标 URL。
- `QHelpEngineCore`：可按关键词查询文档链接，也负责 collection 和 filter 数据。
- `QListView`：提供模型视图、当前项、选择和键盘激活等通用行为。

## 逐项 API 说明

### `[slot] void QHelpIndexWidget::filterIndices(const QString &filter, const QString &wildcard = {})`

按 `filter` 或 `wildcard` 筛选索引项，并将最佳匹配项设为当前项。该调用改变列表的筛选状态，不会启动文档索引构建。传入空条件、尚未完成初始化或没有匹配项时，应按“当前项可能无效”处理。

### `[slot] void QHelpIndexWidget::activateCurrentItem()`

激活当前索引项，并根据该关键词关联文档的数量发出激活信号。它适合绑定自定义“打开”按钮或在测试中模拟用户按回车；调用前应确认 `currentIndex().isValid()`。

### `[signal] void QHelpIndexWidget::documentActivated(const QHelpLink &document, const QString &keyword)`

当前索引项被激活且需要显示一个文档时发出。`document.title` 是文档标题，`document.url` 是目标 URL；`keyword` 是用户激活的索引关键词。

### `[signal] void QHelpIndexWidget::documentsActivated(const QList<QHelpLink> &documents, const QString &keyword)`

当前索引项被激活且同一关键词关联多个文档时发出。应用通常应先让用户选择文档，再使用所选 `QHelpLink::url` 导航。

### `[deprecated] void QHelpIndexWidget::linkActivated(const QUrl &link, const QString &keyword)`

旧版单文档激活信号，Qt 5.15 起废弃。新代码使用 `documentActivated()`，因为新信号同时传递文档标题和 URL。

### `[deprecated] void QHelpIndexWidget::linksActivated(const QMultiMap<QString, QUrl> &links, const QString &keyword)`

旧版多文档激活信号，Qt 5.15 起废弃。新代码使用 `documentsActivated()`，从 `QList<QHelpLink>` 中同时取得标题和 URL。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 槽 | `void filterIndices(const QString &filter, const QString &wildcard = {})` | 筛选索引并将最佳匹配设为当前项。 | 不负责创建索引；无匹配时当前项可能无效。 |
| 槽 | `void activateCurrentItem()` | 激活当前索引项并发出相应文档信号。 | 调用前检查当前项和索引是否准备完成。 |
| 信号 | `void documentActivated(const QHelpLink &document, const QString &keyword)` | 单个文档被激活时通知应用。 | 应用读取 `document.url` 自己打开正文。 |
| 信号 | `void documentsActivated(const QList<QHelpLink> &documents, const QString &keyword)` | 一个关键词对应多个文档时通知应用。 | 必须处理候选选择，不能只取列表第一个而不说明策略。 |
| 信号，已废弃 | `void linkActivated(const QUrl &link, const QString &keyword)` | 旧版单文档链接通知。 | Qt 5.15 起废弃，改用 `documentActivated()`。 |
| 信号，已废弃 | `void linksActivated(const QMultiMap<QString, QUrl> &links, const QString &keyword)` | 旧版多文档链接通知。 | Qt 5.15 起废弃，改用 `documentsActivated()`。 |
| 继承 API | `QListView` 的 `model()`、`currentIndex()`、选择和视图接口 | 读取模型、控制当前项和视图行为。 | 控件本身由 `QHelpEngine` 管理，不要替换成另一个 engine 的模型。 |

---

### 一句话总结

`QHelpIndexWidget` 是帮助索引的交互列表：engine 负责创建和持有它，控件负责筛选和发出文档激活通知，应用负责处理 URL 和正文显示。
