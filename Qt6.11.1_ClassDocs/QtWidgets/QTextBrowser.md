# QTextBrowser

> Qt 6.11.1 · Qt Widgets · 来自 `QTextBrowser`

## 1. 先建立直觉

`QTextBrowser` 是 `QTextEdit` 的只读文档浏览版本：它显示富文本、Markdown 或纯文本资源，处理链接点击，并维护前进/后退历史。它适合做帮助页、关于窗口里的许可文本、内嵌文档、轻量的本地知识库，而不是完整网页浏览器。

它和 `QTextEdit` 的差别不只是默认只读。`QTextBrowser` 有 `source`、`searchPaths`、历史栈和链接导航策略；用户点链接时，你可以让它自己跳转，也可以拦截 `anchorClicked()` 交给应用路由。

一个好的判断：内容来自应用内文档、资源文件或本地 HTML/Markdown，选 `QTextBrowser`；内容来自互联网并依赖复杂 CSS、JavaScript、Cookie，选 Qt WebEngine。

## 2. 类说明

- 头文件：`#include <QTextBrowser>`
- 模块：`Qt6::Widgets`
- 继承自：`QTextEdit`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它继承了 `QTextEdit` 的文档、选择、复制、滚动和显示能力，同时增加了文档源加载和浏览历史。默认 `readOnly` 为 `true`，默认不启用撤销重做。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QTextBrowser(parent)` | 创建文本浏览器。 |
| `setSource(url, type)` / `source()` | 加载并记录当前文档源。 |
| `sourceType()` | 读取当前源被识别或指定的资源类型。 |
| `setSearchPaths()` / `searchPaths()` | 设置相对链接、图片、文档的查找路径。 |
| `setOpenLinks()` / `openLinks()` | 控制用户点击链接时是否自动导航。 |
| `setOpenExternalLinks()` / `openExternalLinks()` | 控制外部链接是否交给 `QDesktopServices::openUrl()`。 |
| `anchorClicked(QUrl)` | 链接被激活时发出，适合自定义路由或安全确认。 |
| `highlighted(QUrl)` | 鼠标悬停到链接时发出，可更新状态栏。 |
| `sourceChanged(QUrl)` | 当前文档源变化。 |
| `backward()` / `forward()` / `home()` | 浏览历史导航。 |
| `reload()` | 重新加载当前源。 |
| `clearHistory()` | 清空前进/后退历史。 |
| `backwardHistoryCount()` / `forwardHistoryCount()` | 查询历史两侧数量。 |
| `historyTitle(i)` / `historyUrl(i)` | 查询历史条目的标题和 URL。 |
| `isBackwardAvailable()` / `isForwardAvailable()` | 查询是否可以后退或前进。 |
| `backwardAvailable(bool)` / `forwardAvailable(bool)` | 导航可用状态变化。 |
| `historyChanged()` | 历史栈变化。 |
| `loadResource(type, name)` | 重写资源加载，支持内存文档、数据库、网络缓存等来源。 |
| `doSetSource(url, type)` | 子类化核心加载流程；Qt 6 中用于替代直接重写旧版 `setSource()`。 |
| `setReadOnly()` | 继承自 `QTextEdit`，但浏览器通常保持只读。 |
| `setHtml()` / `setMarkdown()` / `setPlainText()` | 直接设置内容，不一定形成完整导航历史。 |

## 4. 关键用法

### 本地帮助系统：用 `source` 和 `searchPaths`

最典型的用法是把帮助文档放进资源系统或安装目录，然后设置 `searchPaths()`，再调用 `setSource()`。文档里的相对链接和图片会在搜索路径和当前文档目录中查找。这样帮助页可以互相链接，不需要每次手动读文件再 `setHtml()`。

如果文档类型可能混淆，例如一个无扩展名 URL 或动态内容，给 `setSource()` 传入明确的 `QTextDocument::ResourceType`。依赖自动识别虽然方便，但调试时不如显式类型清楚。

### 链接策略：导航、拦截和外部打开要分开想

`openLinks` 控制浏览器是否自动处理用户激活的链接；无论它开不开，`anchorClicked()` 都会发出。需要自定义路由时，把 `openLinks` 设为 `false`，在槽里检查 URL，再决定 `setSource()`、打开对话框或拒绝跳转。

`openExternalLinks` 只影响外部 scheme 的链接，例如 `https:`。在企业软件、管理工具或离线应用里，建议默认保持 `false`，点击外部链接时给用户明确提示，避免文档内容悄悄启动浏览器。

### 历史栈：适合文档，不适合业务状态

`backward()`、`forward()`、`home()` 管的是文档导航历史，不应该拿来保存应用页面状态。比如设置页、向导页、工作区切换，应该由业务路由或 `QStackedWidget` 管理。`QTextBrowser` 的历史更像一本手册里的链接跳转记录。

`historyTitle()` 和 `historyUrl()` 可用来做一个小型历史菜单。索引是相对当前项的历史位置，使用前先看 `backwardHistoryCount()` 和 `forwardHistoryCount()`，避免越界假设。

### 自定义资源加载

重写 `loadResource()` 可以让文档引用 `qrc:`、自定义 scheme、数据库中的图片或内存里的 Markdown。重写 `doSetSource()` 则更适合完全接管“URL 到文档内容”的过程。Qt 6 中应优先重写 `doSetSource()`，因为它才是新的虚函数扩展点。

资源加载要避免阻塞 GUI 线程。若内容来自网络或慢存储，先显示加载状态，后台取回后再投递到 GUI 线程更新文档。

## 5. 常见坑与经验

- `QTextBrowser` 不是 WebView，不执行 JavaScript，对 CSS 支持也有限。
- `setHtml()` 直接塞内容很方便，但如果你希望相对链接、刷新、历史和当前源都可靠，优先用 `setSource()`。
- `anchorClicked()` 发出后浏览器可能仍会自动导航；要拦截就设置 `setOpenLinks(false)`。
- `openExternalLinks(true)` 等于允许文档触发外部 URL 打开，用户可控内容里要谨慎。
- 只读不等于不可交互；用户仍然可以选择、复制、点击链接，交互能力由 `textInteractionFlags` 决定。
