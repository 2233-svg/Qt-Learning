# QHelpEngine：完整的 Qt Help GUI 外壳

> 适用版本：Qt 6.11.1
> 头文件：`#include <QHelpEngine>`
> 所属模块：`Qt6::Help`
> 继承：`QHelpEngineCore`

## 它解决什么问题

`QHelpEngine` 在 `QHelpEngineCore` 的 collection、文档注册、过滤和内容读取能力之上，提供目录模型、索引模型、目录控件、索引控件和搜索引擎。它适合直接搭建应用内帮助中心，不必自己把多个模型和 QWidget 组装起来。

如果程序只需要后台查询帮助文件，使用 `QHelpEngineCore` 更合适；`QHelpEngine` 的附加对象依赖 Widgets 和 GUI 事件循环。

## 实际使用场景

- 创建一个带目录、索引、搜索和正文浏览器的帮助窗口。
- 使用 `contentModel()`、`indexModel()` 自定义左右面板。
- 直接把 `contentWidget()`、`indexWidget()` 放入 `QTabWidget` 或侧边栏。
- 调用继承自 `QHelpEngineCore` 的 API 读取 qthelp URL 对应内容。

## 初始化与对象所有权

构造函数只指定 collection file。使用前仍应调用 `setupData()`，并等待 `setupFinished()`；虽然部分 getter 会隐式触发 setup，但显式初始化更容易处理错误和显示加载状态。

模型、控件和搜索引擎由 `QHelpEngine` 内部创建和管理，返回的指针不转移所有权。它们依赖同一个 engine 的 collection、filter 和生命周期；不要删除，也不要把一个 engine 的模型和另一个 engine 混搭。

所有 GUI 控件和模型操作应在 GUI 线程中进行。帮助引擎析构后，返回的模型、控件和搜索对象都不能继续使用。

## 组件之间如何协作

目录控件使用内容模型，索引控件使用索引模型，搜索控件和结果控件使用搜索引擎。切换 filter 后，目录、索引和搜索结果不会凭空保持旧状态；应用应重新生成相应模型或重新发起搜索，并在完成信号后更新界面。

正文查看通常由应用自己的 `QTextBrowser`、`QWebEngineView` 或其他浏览器完成。引擎提供 `fileData()`、`findFile()` 等内容查询能力，不替应用决定 HTML 渲染和外部链接策略。

## 常见误区

- 忘记 `setupData()`，把空目录或空搜索结果误判为没有文档。
- 删除 `contentWidget()`、`indexModel()` 等引擎拥有的对象。
- 切换 collection file 后继续使用旧模型索引和旧文档 URL。
- 只刷新目录，不刷新索引和搜索状态，造成界面各区域使用不同 filter。
- 在工作线程直接操作 QWidget 或模型。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `explicit QHelpEngine(const QString &collectionFile, QObject *parent = nullptr)` | 创建完整帮助引擎并指定 collection file。 | 不等于已完成初始化；随后调用 `setupData()` 并处理错误。 |
| `~QHelpEngine()` | 销毁引擎及其内部模型、控件和搜索对象。 | 返回的子对象由引擎管理，不应单独删除。 |
| `QHelpContentModel *contentModel() const` | 返回帮助目录模型。 | 指针由 engine 持有；切换 collection 或重建目录后索引需重新获取。 |
| `QHelpIndexModel *indexModel() const` | 返回帮助索引模型。 | 与当前 engine/filter 绑定，不能跨 engine 使用。 |
| `QHelpContentWidget *contentWidget()` | 返回目录树控件。 | 返回的 QWidget 由 engine 管理，适合直接放入布局。 |
| `QHelpIndexWidget *indexWidget()` | 返回索引列表控件。 | 通过 `documentActivated` 等信号把结果交给正文浏览器。 |
| `QHelpSearchEngine *searchEngine()` | 返回搜索引擎及其查询/结果控件入口。 | 搜索索引可能需要先建立；监听开始/完成信号。 |
| `QHelpEngineCore::setupData()` | 初始化 collection、注册文档和过滤数据。 | 在 `setupFinished()` 前数据处于不可依赖状态。 |
| `QHelpEngineCore::filterEngine()` | 访问过滤器管理对象。 | 使用新过滤器功能前启用 `setUsesFilterEngine(true)`。 |
| `QHelpEngineCore::fileData(const QUrl &)` | 读取 qthelp URL 的文件内容。 | 空字节数组可能表示文件不存在；需结合 URL 和错误日志判断。 |

## 一句话总结

`QHelpEngine` 是 Qt Help 的 GUI 组装层：一个 engine 统一管理 collection、目录、索引和搜索对象，应用负责把链接结果呈现给正文浏览器。
