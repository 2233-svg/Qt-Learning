# Qt Help：帮助集合、内容索引与全文搜索

Qt Help 模块把多个 Qt Compressed Help（`.qch`）文档组织成一个可查询的帮助集合（collection）。它既能支持类似 Qt Assistant 的桌面帮助浏览器，也能嵌入应用，为自己的产品文档、API 文档和故障排查手册提供目录、索引、关键字跳转和全文搜索。

本文从“打开一个帮助集合”开始，逐步建立一个可用的帮助后端，再介绍内容模型、索引模型和搜索模型如何接入 Qt Widgets。示例只放在 Markdown 代码块中，不生成独立工程文件。

## 1. 先建立整体认识

### 1.1 `.qch`、帮助集合与 Qt Help Engine

Qt Help 的基本链路如下：

```text
HTML/Markdown 文档
        │ qhelpgenerator
        ▼
   module.qch
        │ registerDocumentation()
        ▼
帮助集合 collection（通常是 .qhc）
        │
        ├─ 内容树：章节、页面、层级
        ├─ 索引：关键字到页面的映射
        └─ 全文索引：搜索词到页面的映射
```

`.qch` 是单个文档包，内部包含文档的命名空间、虚拟路径、目录树、索引和页面内容；帮助集合是一个可写的集合数据库，记录当前注册了哪些 `.qch` 文件以及搜索索引。`QHelpEngineCore` 负责底层数据访问，`QHelpEngine` 在此基础上提供面向 Widgets 的模型和控件。

### 1.2 Core 与 Widgets 层的职责

| 类 | 主要职责 | 是否依赖 Qt Widgets |
| --- | --- | --- |
| `QHelpEngineCore` | 注册文档、读取页面、关键字定位、管理集合 | 否 |
| `QHelpEngine` | 创建内容/索引/搜索模型，统一管理引擎 | 否（模块本身提供模型） |
| `QHelpContentModel` | 将目录树暴露为 `QAbstractItemModel` | 否 |
| `QHelpContentWidget` | 显示可展开的目录树 | 是 |
| `QHelpIndexModel` | 将关键字索引暴露为模型 | 否 |
| `QHelpIndexWidget` | 显示和筛选关键字列表 | 是 |
| `QHelpSearchEngine` | 创建全文索引并执行异步搜索 | 否 |
| `QHelpSearchQueryWidget` | 提供搜索输入框和高级筛选控件 | 是 |

如果应用只有命令行或服务端需求，只使用 `QHelpEngineCore` 即可；如果要做类似 Assistant 的浏览窗口，则使用 `QHelpEngine` 配合上述 Widgets。

## 2. 最小可用配置

### 2.1 CMake 配置

Qt 6 的帮助核心和 Widgets 类都在 `Help` 模块中：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core Widgets Help)

target_link_libraries(mytarget PRIVATE
    Qt6::Core
    Qt6::Widgets
    Qt6::Help
)
```

使用 `QHelpEngineCore` 时不需要链接 `Qt6::Widgets`；使用 `QHelpContentWidget`、`QHelpIndexWidget` 或 `QHelpSearchQueryWidget` 时才需要。

### 2.2 选择集合文件位置

帮助集合文件会被引擎写入，因此路径必须可写。不要把用户运行时生成的集合放在安装目录或程序资源系统（`: /`）中。可以使用 `QStandardPaths::AppDataLocation`：

```cpp
#include <QDir>
#include <QStandardPaths>

const QString appData =
    QStandardPaths::writableLocation(QStandardPaths::AppDataLocation);
QDir().mkpath(appData);
const QString collectionFile = appData + "/product-help.qhc";
```

首次运行时集合文件可以不存在，`QHelpEngineCore` 会在初始化时创建它；如果目录不可写，初始化或后续注册操作会失败，应检查 `error()`。

## 3. 创建帮助引擎并检查错误

### 3.1 `QHelpEngineCore` 的生命周期

```cpp
#include <QHelpEngineCore>
#include <QDebug>

QHelpEngineCore helpEngine(collectionFile);
if (!helpEngine.setupData()) {
    qWarning() << "无法打开帮助集合:" << helpEngine.error();
    return;
}
```

`setupData()` 会打开或初始化集合数据库。构造函数只保存集合文件名，不代表集合已经准备好。后续所有读取和修改都应在 `setupData()` 成功后进行。

### 3.2 初始化时机与失败处理

常见失败原因包括：

1. 集合目录没有写权限。
2. `.qhc` 文件被其他进程锁定或损坏。
3. `.qch` 文件路径不存在。
4. 注册的命名空间与当前集合冲突。
5. 搜索索引目录不可写。

推荐把初始化封装成一次性函数，并将错误返回给上层，而不是继续使用处于未初始化状态的引擎：

```cpp
bool openHelpCollection(QHelpEngineCore &engine)
{
    if (engine.setupData())
        return true;

    qWarning() << "Help setup failed:" << engine.error();
    return false;
}
```

## 4. 注册、查看和移除文档

### 4.1 注册 `.qch` 文档

```cpp
const QString qchFile = "/opt/product/docs/product.qch";
if (!helpEngine.registerDocumentation(qchFile)) {
    qWarning() << "注册失败:" << helpEngine.error();
}
```

注册成功后，文档中的命名空间会出现在 `registeredDocumentations()` 中。注册操作会更新集合，但不等同于立即建立全文搜索索引；搜索引擎可能在后台继续索引。

### 4.2 查看当前注册的命名空间

```cpp
const QStringList namespaces = helpEngine.registeredDocumentations();
for (const QString &name : namespaces)
    qDebug() << "已注册:" << name;
```

命名空间是跨文档定位的核心标识。两个文档不能注册相同命名空间，否则会发生冲突。应用不应依赖 `.qch` 的文件名推断命名空间，而应通过 `namespaceName()`（由文档工具生成）或实际注册结果确认。

### 4.3 移除文档

```cpp
const QString namespaceName = "com.example.product";
if (!helpEngine.unregisterDocumentation(namespaceName))
    qWarning() << "移除失败:" << helpEngine.error();
```

移除使用命名空间而非文件路径。移除后，内容树、关键字索引和搜索结果都不再包含该文档；若搜索引擎仍在索引，应等待其状态信号或重新创建搜索引擎。

## 5. 读取页面内容与虚拟 URL

### 5.1 用 `fileData()` 读取页面

`.qch` 文档内部使用虚拟 URL，例如 `qthelp://com.example.product/doc/intro.html`。不要直接把它当成本地文件路径使用：

```cpp
const QUrl url("qthelp://com.example.product/doc/intro.html");
const QByteArray html = helpEngine.fileData(url);
if (html.isEmpty())
    qWarning() << "页面为空或不存在:" << url;
```

`fileData()` 返回原始字节。如果页面是 HTML，可以交给 `QTextBrowser::setHtml()`；如果资源是图片、样式表或脚本，则应按二进制资源处理。

### 5.2 使用 `QTextBrowser` 显示帮助页

```cpp
#include <QTextBrowser>

auto *browser = new QTextBrowser;
QObject::connect(browser, &QTextBrowser::anchorClicked,
                 browser, [browser, &helpEngine](const QUrl &url) {
    const QByteArray data = helpEngine.fileData(url);
    if (!data.isEmpty())
        browser->setHtml(QString::fromUtf8(data));
});

const QUrl startUrl("qthelp://com.example.product/doc/index.html");
browser->setHtml(QString::fromUtf8(helpEngine.fileData(startUrl)));
```

实际应用通常还要处理相对链接、后退/前进历史和外部 `http` 链接。若页面中包含相对资源，优先调用 `QTextBrowser::setSource(startUrl)` 并重载资源处理逻辑，避免手动拼接 URL 出错。

## 6. 内容树：`QHelpContentModel` 与 `QHelpContentWidget`

### 6.1 创建内容模型

```cpp
#include <QHelpEngine>
#include <QHelpContentModel>

QHelpEngine helpEngine(collectionFile);
if (!helpEngine.setupData())
    return;

QHelpContentModel *contents = helpEngine.contentModel();
```

`contentModel()` 返回一个模型指针，模型的行、列和父子关系对应帮助文档目录。模型由引擎拥有，调用者不应手动 `delete`。文档注册或集合变化后，模型可能异步重建，界面应监听模型的更新信号。

### 6.2 显示目录控件并打开页面

```cpp
#include <QHelpContentWidget>

auto *contentWidget = new QHelpContentWidget;
contentWidget->setModel(helpEngine.contentModel());

QObject::connect(contentWidget, &QHelpContentWidget::linkActivated,
                 browser, [browser](const QUrl &url) {
    browser->setSource(url);
});
```

`QHelpContentWidget` 是一个基于 `QTreeView` 的控件。用户点击目录项时会发出 `linkActivated(QUrl)`，应用可以把 URL 交给 `QTextBrowser` 或自己的页面查看器。

### 6.3 处理当前项变化

如果需要在状态栏显示当前章节标题，可以监听选择模型：

```cpp
QObject::connect(contentWidget->selectionModel(),
                 &QItemSelectionModel::currentChanged,
                 contentWidget,
                 [](const QModelIndex &current,
                    const QModelIndex &) {
    qDebug() << "当前章节:" << current.data().toString();
});
```

不要缓存长期有效的 `QModelIndex`。注册/移除文档或刷新模型后，旧索引可能失效；需要保存位置时使用 `QPersistentModelIndex`，并在模型重置后重新确认它仍然有效。

## 7. 关键字索引：`QHelpIndexModel` 与定位 API

### 7.1 显示索引列表

```cpp
#include <QHelpIndexWidget>

auto *indexWidget = new QHelpIndexWidget;
indexWidget->setModel(helpEngine.indexModel());

QObject::connect(indexWidget, &QHelpIndexWidget::linkActivated,
                 browser, [browser](const QUrl &url) {
    browser->setSource(url);
});
```

索引关键字由 `.qch` 文档生成工具写入，适合“类名、函数名、概念词”这类精确查找。它和全文搜索互补：索引结果通常更稳定，全文搜索则覆盖页面正文。

### 7.2 根据关键字查找文档

底层引擎提供两个常用定位函数：

```cpp
const QList<QHelpLink> byKeyword =
    helpEngine.documentsForKeyword("QBoxLayout");

const QList<QHelpLink> byIdentifier =
    helpEngine.documentsForIdentifier("QBoxLayout::addWidget");

for (const QHelpLink &link : byKeyword)
    qDebug() << link.title << link.url;
```

`documentsForKeyword()` 面向普通关键字，`documentsForIdentifier()` 面向文档标识符。返回值是 `QHelpLink` 列表，一个词可能对应多个重载、模块或版本页面。界面上应让用户选择具体结果，而不是假设列表只有一项。

### 7.3 过滤索引

`QHelpIndexModel` 支持通过 `filter()` 或视图的过滤机制缩小关键字列表。对于大量文档，建议使用 `QSortFilterProxyModel`，把搜索框文本映射到正则表达式或大小写不敏感的字符串匹配：

```cpp
#include <QSortFilterProxyModel>

auto *proxy = new QSortFilterProxyModel(indexWidget);
proxy->setFilterCaseSensitivity(Qt::CaseInsensitive);
proxy->setFilterKeyColumn(0);
proxy->setSourceModel(helpEngine.indexModel());
indexWidget->setModel(proxy);
```

代理模型只是改变显示，不会改变帮助引擎中的索引数据。

## 8. 全文搜索：建立索引与执行查询

### 8.1 获取搜索引擎

```cpp
#include <QHelpSearchEngine>

QHelpSearchEngine *searchEngine = helpEngine.searchEngine();
```

搜索引擎由 `QHelpEngine` 管理。第一次使用时可能需要建立全文索引，这个过程是异步的。不要在 GUI 线程中同步扫描大量文档，也不要在索引未完成时假设结果完整。

### 8.2 监听索引和搜索状态

```cpp
QObject::connect(searchEngine, &QHelpSearchEngine::indexingStarted,
                 [] { qDebug() << "开始建立帮助索引"; });
QObject::connect(searchEngine, &QHelpSearchEngine::indexingFinished,
                 [] { qDebug() << "帮助索引完成"; });
QObject::connect(searchEngine, &QHelpSearchEngine::searchingStarted,
                 [] { qDebug() << "开始搜索"; });
QObject::connect(searchEngine, &QHelpSearchEngine::searchingFinished,
                 [] { qDebug() << "搜索完成"; });
```

还可以监听 `indexingError`、`searchingError`，并在出错时显示 `QHelpEngineCore::error()`。索引目录路径由搜索引擎管理，部署时要确保它位于可写位置。

### 8.3 构造搜索查询

Qt Help 支持 `QHelpSearchQuery`，常见字段包括搜索字段（例如全部字段、关键词或全文）和搜索短语：

```cpp
#include <QHelpSearchQuery>

QList<QHelpSearchQuery> queries;
queries.append(QHelpSearchQuery(
    QHelpSearchQuery::DEFAULT,
    "QBoxLayout spacing"));

searchEngine->search(queries);
```

搜索接口是异步的，结果准备好后从 `searchResults()` 读取：

```cpp
QObject::connect(searchEngine, &QHelpSearchEngine::searchingFinished,
                 [&] {
    const QList<QHelpSearchResult> results = searchEngine->searchResults();
    for (const QHelpSearchResult &result : results)
        qDebug() << result.title << result.url << result.snippet;
});
```

不同 Qt 版本对搜索字段和结果摘要的支持略有差异，应以本机 Qt 6.11.1 头文件和文档为准。业务层只依赖 `title`、`url` 等稳定字段，避免把内部索引格式写入自己的数据文件。

### 8.4 取消长时间搜索

当用户快速连续输入时，旧搜索结果已经没有意义，应先取消旧请求：

```cpp
searchEngine->cancelSearching();
searchEngine->search(queries);
```

同理，在窗口关闭或文档集合大规模变化时，可调用 `cancelIndexing()`。取消后仍可能收到收尾信号，槽函数中应检查当前查询是否仍是最新的一次。

## 9. 搜索框与结果列表的典型组合

下面的片段展示最小的 Widgets 组合思路：搜索框负责触发查询，结果列表负责显示标题，双击后把 URL 交给浏览器。

```cpp
#include <QLineEdit>
#include <QListWidget>
#include <QHelpSearchEngine>
#include <QHelpSearchQuery>

auto *searchEdit = new QLineEdit;
auto *resultList = new QListWidget;
auto *searchEngine = helpEngine.searchEngine();

QObject::connect(searchEdit, &QLineEdit::returnPressed,
                 searchEdit, [=] {
    searchEngine->cancelSearching();
    const QString text = searchEdit->text().trimmed();
    if (text.isEmpty()) {
        resultList->clear();
        return;
    }

    searchEngine->search({
        QHelpSearchQuery(QHelpSearchQuery::DEFAULT, text)
    });
});

QObject::connect(searchEngine, &QHelpSearchEngine::searchingFinished,
                 resultList, [=] {
    resultList->clear();
    for (const QHelpSearchResult &result : searchEngine->searchResults()) {
        auto *item = new QListWidgetItem(result.title, resultList);
        item->setData(Qt::UserRole, result.url);
    }
});

QObject::connect(resultList, &QListWidget::itemActivated,
                 resultList, [=](QListWidgetItem *item) {
    browser->setSource(item->data(Qt::UserRole).toUrl());
});
```

生产代码还应显示“正在索引/正在搜索”状态、空结果提示和搜索错误，并避免在 `searchingFinished` 中无条件清空用户当前选中的页面。

## 10. 帮助过滤器：按产品版本或角色裁剪文档

当一个集合包含多个产品线、平台或版本时，可以使用 `QHelpFilterData` 设置过滤器。过滤器通常按组件、版本或自定义属性筛选文档：

```cpp
#include <QHelpFilterData>

QHelpFilterData filter;
filter.setComponents({"Widgets", "Desktop"});
filter.setVersions({"6.11"});

helpEngine.setFilterData("desktop-6.11", filter);
helpEngine.setCurrentFilter("desktop-6.11");
```

过滤器的属性名称必须和生成 `.qch` 时写入的元数据一致。切换当前过滤器后，内容模型、索引模型和搜索结果都会随集合范围变化；切换过程中应禁用重复操作或等待模型更新。

## 11. 文档生成与部署要点

### 11.1 从文档源生成 `.qch`

典型流程是准备 `.qhp` 项目文件，再调用 `qhelpgenerator`：

```text
qhelpgenerator product.qhp -o product.qch
```

`.qhp` 中应声明命名空间、虚拟文件、目录树（`<section>`）和关键字索引（`<keyword>`）。源文件路径、虚拟路径和实际链接要保持一致，否则页面能显示但目录跳转或图片加载会失败。

### 11.2 安装时注册，卸载时移除

应用首次启动可以注册随程序安装的 `.qch`，卸载或版本升级时按命名空间移除旧文档。不要每次启动都反复注册同一个文件；先比较 `registeredDocumentations()`，只在缺失或版本变化时更新。

### 11.3 版本升级策略

推荐把集合文件和搜索索引放在应用数据目录，并在文档版本变化时：

1. 取消正在进行的索引和搜索。
2. 按旧命名空间移除旧 `.qch`。
3. 注册新 `.qch`。
4. 等待索引完成，再启用搜索入口。

这样可以避免旧页面和新页面同时出现在结果中，也避免程序更新目录中的文件后仍使用旧集合缓存。

## 12. 常见问题与排查方法

### 12.1 目录为空

- 检查 `setupData()` 是否成功。
- 检查 `.qch` 是否已经注册。
- 检查 `.qhp` 是否生成了 `<toc>` 内容。
- 检查注册文档的命名空间是否冲突。
- 在模型更新完成前不要读取最终行数。

### 12.2 页面 URL 能看到但内容为空

- 确认 URL 使用 `qthelp://` 协议，并且命名空间与 `.qch` 一致。
- 确认虚拟路径大小写和 `.qhp` 中声明的一致。
- 使用 `fileData(url)` 检查返回字节是否为空。
- 不要把 `qthelp://` URL 直接交给 `QFile`。

### 12.3 搜索没有结果

- 首次运行需等待 `indexingFinished`。
- 确认搜索索引目录可写。
- 取消旧搜索后再发起新搜索。
- 检查过滤器是否把文档全部排除了。
- 检查查询文本是否只包含停用词或过短的片段。

### 12.4 GUI 退出时崩溃

确保 `QHelpEngine`、内容/索引控件和页面浏览器的父子关系明确。搜索完成槽函数不要捕获已经销毁的裸指针；优先使用 QObject 父对象、`QPointer` 或断开连接。

## 13. 进一步延伸

### 13.1 自定义帮助浏览器

可以把 `QHelpContentWidget`、`QHelpIndexWidget` 和搜索结果列表放在 `QSplitter` 中，把 `QTextBrowser` 放在右侧，并在 URL 变化时同步目录选中状态。目录、索引和搜索都通过同一个 `QHelpEngine`，这样文档过滤和版本切换天然保持一致。

### 13.2 在 QML 中复用帮助后端

`QHelpEngineCore` 不依赖 Widgets，可以包装成 `QObject` 服务，通过 `Q_INVOKABLE` 暴露 `fileData()`、关键字查询和当前文档列表；页面内容再转为 `QString` 或临时 URL 提供给 QML。注意不要把任意本地文件读取接口直接暴露给 QML，必须限制在 `qthelp://` URL 和已注册命名空间内。

### 13.3 离线文档与在线文档的边界

帮助引擎适合稳定的离线文档。对于在线内容，建议在浏览器中明确区分 `qthelp://` 与 `https://`，并通过白名单控制外链，避免帮助页面成为任意网页跳转入口。

## 14. 速查表

| 目标 | API |
| --- | --- |
| 打开/初始化集合 | `QHelpEngineCore::setupData()` |
| 注册 `.qch` | `registerDocumentation()` |
| 列出已注册文档 | `registeredDocumentations()` |
| 移除文档 | `unregisterDocumentation()` |
| 读取页面/资源 | `fileData(QUrl)` |
| 关键字定位 | `documentsForKeyword()` |
| 标识符定位 | `documentsForIdentifier()` |
| 内容模型 | `QHelpEngine::contentModel()` |
| 索引模型 | `QHelpEngine::indexModel()` |
| 全文搜索 | `QHelpEngine::searchEngine()->search()` |
| 取消搜索/索引 | `cancelSearching()` / `cancelIndexing()` |
| 按属性过滤 | `QHelpFilterData`、`setCurrentFilter()` |

掌握这些 API 后，就能从“把 `.qch` 打开”扩展到“构建带目录、索引、全文搜索、版本过滤和安全页面导航的离线帮助中心”。
