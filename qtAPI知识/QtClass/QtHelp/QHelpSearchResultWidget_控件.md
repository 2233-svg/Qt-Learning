# QHelpSearchResultWidget：显示 Qt Help 搜索结果的只读浏览控件

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHelpSearchResultWidget>`  
> 所属模块：`Qt6::Help`  
> 继承：`QWidget`  
> 定位：搜索结果控件

## 它解决什么问题

`QHelpSearchResultWidget` 是 Qt Help 搜索结果的文本浏览器。它由 `QHelpSearchEngine` 连接到搜索结果数据，用于显示标题、摘要和可激活的文档链接，并在用户激活结果时发出 `requestShowLink()`。

它负责结果展示和激活通知，不负责打开正文。应用需要接收 URL，然后交给 `QHelpEngineCore::fileData()`、自己的帮助浏览器或外部 URL 处理器。

## 实际使用场景

- 与 `QHelpSearchEngine::queryWidget()` 一起组成标准搜索页。
- 用户点击搜索结果后，在应用内帮助浏览器中显示对应 qthelp 文档。
- 使用 `linkAt()` 实现状态栏预览、鼠标悬停提示或自定义上下文菜单。
- 不满足官方布局时，改用搜索引擎的 `searchResults()` 自己构建结果界面。

## 只能从搜索引擎取得

该类的构造函数是私有的，应用不能直接 `new QHelpSearchResultWidget`。必须通过与搜索流程匹配的 `QHelpSearchEngine::resultWidget()` 获取：

```cpp
auto *resultWidget = searchEngine->resultWidget();
layout->addWidget(resultWidget);

connect(resultWidget, &QHelpSearchResultWidget::requestShowLink,
        this, [this](const QUrl &url) {
            showHelpUrl(url);
        });
```

这样取得的控件由搜索引擎管理，内部已经建立了显示搜索结果所需的连接。不要删除它，也不要把它从一个搜索引擎挪给另一个搜索引擎使用。搜索引擎析构后，返回指针立即失效。

## 链接请求不是导航动作

当用户激活结果中的链接时，控件发出 `requestShowLink(const QUrl &)`. 这个信号只是请求应用显示 URL，不会自动调用 `QDesktopServices::openUrl()`，也不会自动把内容加载到某个浏览器。

对于 `qthelp://` URL，应用通常应使用帮助引擎读取内容并更新自己的正文查看器；对于外部 scheme，则应按安全策略决定是否交给外部浏览器。

## 坐标查询

`linkAt(const QPoint &point)` 返回给定位置对应链接的 URL；如果该位置没有结果项或链接，则返回空 `QUrl`。传入的点应使用控件坐标系，鼠标事件中的 `event->position().toPoint()` 或 `event->pos()` 通常可以直接使用，跨控件转换后再调用。

返回的是 URL 值，不是内部文本对象的引用。调用者可以保存它，但在应用层仍应按 URL 有效性和安全策略处理。

## 生命周期、线程和事件循环

这是 QWidget，只能在 GUI 线程创建、嵌入布局和访问。虽然构造函数不可公开调用，但 `resultWidget()` 返回的对象仍属于搜索引擎的 QObject 生命周期。鼠标、键盘和链接激活依赖 GUI 事件循环。

结果内容由搜索引擎的搜索状态驱动。开始新搜索后，控件会展示新的结果；不要在自己的逻辑中把旧结果 URL 与新查询混用。

## 常见误区

- 直接构造 `QHelpSearchResultWidget`：构造函数私有，只能从搜索引擎取得。
- 连接 `requestShowLink` 后期待控件自动打开正文：信号需要应用处理。
- 把 `linkAt()` 的空 URL 当成有效链接。
- 向控件手动塞入 `QHelpSearchResult`：该控件没有公开填充 API，需使用搜索引擎或自定义视图。
- 删除 `resultWidget()` 返回的指针，破坏搜索引擎的所有权。
- 在工作线程操作 QWidget 或响应链接时直接更新 GUI。

## 逐项 API 说明

### `[override virtual noexcept] QHelpSearchResultWidget::~QHelpSearchResultWidget()`

销毁搜索结果控件。正常情况下由其搜索引擎或父对象管理生命周期；销毁搜索引擎后不能继续使用该控件指针。

### `QUrl QHelpSearchResultWidget::linkAt(const QPoint &point)`

返回给定控件坐标处链接的 URL。没有对应项时返回空 URL。它适合用于悬停提示、上下文菜单和测试点击位置，不会发出导航信号。

### `[signal] void QHelpSearchResultWidget::requestShowLink(const QUrl &link)`

结果项被激活、需要显示对应链接时发出。它只传出 URL，正文加载、scheme 判断、外部链接策略和窗口切换都由应用负责。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 析构 | `~QHelpSearchResultWidget()` | 销毁结果浏览控件。 | 控件由搜索引擎管理，不能手动提前删除。 |
| 查询 | `QUrl linkAt(const QPoint &point)` | 查询坐标处的链接 URL。 | 无链接返回空 URL；点必须使用控件坐标。 |
| 信号 | `void requestShowLink(const QUrl &link)` | 用户激活结果链接时请求应用显示它。 | 只通知，不负责打开或渲染正文。 |
| 创建约束 | `QHelpSearchEngine::resultWidget()` | 获取已连接到搜索引擎的结果控件。 | 构造函数私有，返回对象不转移所有权。 |

---

### 一句话总结

`QHelpSearchResultWidget` 是搜索结果展示层：从搜索引擎取得，负责显示和发出 URL 请求，实际文档导航仍由应用完成。
