# QTextBrowser

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QTextBrowser` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QTextBrowser` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QTextBrowser>`
- 继承自：QTextEdit
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `modified : bool`
- `openExternalLinks : bool`
- `openLinks : bool`
- `readOnly : bool`
- `searchPaths : QStringList`
- `source : QUrl`
- `sourceType : QTextDocument::ResourceType`
- `undoRedoEnabled : bool`

### 公有函数

- `QTextBrowser(QWidget *parent = nullptr)`
- `int backwardHistoryCount() const`
- `void clearHistory()`
- `int forwardHistoryCount() const`
- `QString historyTitle(int i) const`
- `QUrl historyUrl(int i) const`
- `bool isBackwardAvailable() const`
- `bool isForwardAvailable() const`
- `bool openExternalLinks() const`
- `bool openLinks() const`
- `QStringList searchPaths() const`
- `void setOpenExternalLinks(bool open)`
- `void setOpenLinks(bool open)`
- `void setSearchPaths(const QStringList &paths)`
- `QUrl source() const`
- `QTextDocument::ResourceType sourceType() const`

### 重实现的公有函数

- `virtual QVariant loadResource(int type, const QUrl &name) override`

### 公有槽函数

- `virtual void backward()`
- `virtual void forward()`
- `virtual void home()`
- `virtual void reload()`
- `void setSource(const QUrl &url, QTextDocument::ResourceType type = QTextDocument::UnknownResource)`

### 信号

- `void anchorClicked(const QUrl &link)`
- `void backwardAvailable(bool available)`
- `void forwardAvailable(bool available)`
- `void highlighted(const QUrl &link)`
- `void historyChanged()`
- `void sourceChanged(const QUrl &src)`

### 保护函数

- `virtual void doSetSource(const QUrl &url, QTextDocument::ResourceType type = QTextDocument::UnknownResource)`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`
- `virtual bool focusNextPrevChild(bool next) override`
- `virtual void focusOutEvent(QFocusEvent *ev) override`
- `virtual void keyPressEvent(QKeyEvent *ev) override`
- `virtual void mouseMoveEvent(QMouseEvent *e) override`
- `virtual void mousePressEvent(QMouseEvent *e) override`
- `virtual void mouseReleaseEvent(QMouseEvent *e) override`
- `virtual void paintEvent(QPaintEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[read-only] modified : bool`

**作用与语义：**

该属性决定文本浏览器内容是否被修改。

**如何使用：** 调用 `modified()` 读取当前值；它不会修改应用状态。

### `openExternalLinks : bool`

**作用与语义：**

规定`QTextBrowser`是否应自动使用`QDesktopServices::openUrl()`打开指向外部源的链接，而不是发出`anchorClicked`信号。如果链接的方案既不是文件格式，也不是QRC，则视为外部链接。
默认值为假。

**如何使用：** 调用 `openExternalLinks()` 读取当前值；它不会修改应用状态。

### `openLinks : bool`

**作用与语义：**

该属性指定了用户尝试通过鼠标或键盘激活的链接`QTextBrowser`是否应自动打开。
无论该属性的值如何，`anchorClicked`信号始终会被发射。
默认值为真。

**如何使用：** 调用 `openLinks()` 读取当前值；它不会修改应用状态。

### `readOnly : bool`

**作用与语义：**

该属性决定文本浏览器是否为只读。
默认情况下，该属性为`true`。

**如何使用：** 调用 `readOnly()` 读取当前值；它不会修改应用状态。

### `searchPaths : QStringList`

**作用与语义：**

该属性包含文本浏览器用来查找支持内容的搜索路径。
`QTextBrowser`使用这份名单来查找图片和文献。
默认情况下，该属性包含一个空字符串列表。

**如何使用：** 调用 `searchPaths()` 读取当前值；它不会修改应用状态。

### `source : QUrl`

**作用与语义：**

该属性保存显示文档的名称。
如果未显示文档或源未知，则这是一个无效的 URL。
在设置此属性时，`QTextBrowser` 会尝试在 `searchPaths` 属性的路径和当前源目录中查找指定名称的文档，除非该值是绝对文件路径。它还会检查可选的锚点并相应地滚动文档。
如果文档中的第一个标签是 `<qt type=detail>`，则文档作为弹出窗口显示，而不是在浏览器窗口中以新文档的形式显示。否则，文档将在文本浏览器中正常显示，文本设置为 `QTextDocument::setHtml()` 或 `QTextDocument::setMarkdown()` 的命名文档内容，取决于文件名是否以任何已知 Markdown 文件扩展名结尾。
如果您希望避免自动类型检测并明确指定类型，请调用 `setSource()`，而不是设置此属性。
默认情况下，该属性包含一个空 URL。

**如何使用：** 调用 `source()` 读取当前值；它不会修改应用状态。

### `[read-only] sourceType : QTextDocument::ResourceType`

**作用与语义：**

此属性保存所显示文档的类型。
如果没有显示文档或源类型未知，则为 `QTextDocument::UnknownResource`。否则，它保存已检测到的类型，或在调用 `setSource()` 时指定的类型。

**如何使用：** 调用 `sourceType()` 读取当前值；它不会修改应用状态。

### `undoRedoEnabled : bool`

**作用与语义：**

该属性决定文本浏览器是否支持撤销/重做操作。
默认情况下，该属性为`false`。

**如何使用：** 调用 `undoRedoEnabled()` 读取当前值；它不会修改应用状态。

### `[explicit] QTextBrowser::QTextBrowser(QWidget *parent = nullptr)`

**作用与语义：**

构建一个带有父`parent`的空 QTextBrowser。

### `[signal] void QTextBrowser::anchorClicked(const QUrl &link)`

**作用与语义：**

当用户点击锚点时，该信号会发出。锚点所指向的URL会在`link`中传递。
请注意，除非`openLinks`属性设置为false，或者你在连接的slot中调用`setSource()`，否则浏览器会自动处理`link`指定地点的导航。该机制用于覆盖浏览器默认的导航功能。

### `[virtual slot] void QTextBrowser::backward()`

**作用与语义：**

通过导航链接将显示的文档改为之前的文档列表。如果没有之前的文档，则无效。

### `[signal] void QTextBrowser::backwardAvailable(bool available)`

**作用与语义：**

当`backward()`的可用性发生变化时，该信号会发出。当用户处于`home()`时，`available`为假;否则为真。

### `int QTextBrowser::backwardHistoryCount() const`

**作用与语义：**

将历史中的位置数量往回返回。

### `void QTextBrowser::clearHistory()`

**作用与语义：**

清除访问过的文档历史，并禁用前进和后退导航。

### `[virtual protected] void QTextBrowser::doSetSource(const QUrl &url, QTextDocument::ResourceType type = QTextDocument::UnknownResource)`

**作用与语义：**

尝试在指定`url`加载指定`type`。
`setSource()`调用 doSetSource。在第 Qt 5 中，`setSource`（const `QUrl` &url）是虚拟的。在第 Qt 6 中，doSetSource() 是虚拟的，因此可以在子类中被覆盖。

### `[override virtual protected] bool QTextBrowser::event(QEvent *e)`

**作用与语义：**

重装：`QAbstractScrollArea::event`（QEvent *事件）。

### `[override virtual protected] bool QTextBrowser::focusNextPrevChild(bool next)`

**作用与语义：**

重实现自：`QTextEdit::focusNextPrevChild`（下一个布尔）。

### `[override virtual protected] void QTextBrowser::focusOutEvent(QFocusEvent *ev)`

**作用与语义：**

重实现自：`QTextEdit::focusOutEvent`（QFocusEvent *e）。

### `[virtual slot] void QTextBrowser::forward()`

**作用与语义：**

通过导航链接将显示的文档更改为文档列表中的下一个文档。如果没有下一个文档，则无效。

### `[signal] void QTextBrowser::forwardAvailable(bool available)`

**作用与语义：**

当`forward()`的可用性发生变化时，该信号会发出。`available`在用户导航`backward()`后为真，用户导航或`forward()`时为假。

### `int QTextBrowser::forwardHistoryCount() const`

**作用与语义：**

返回历史中前进的位置数量。

### `[signal] void QTextBrowser::highlighted(const QUrl &link)`

**作用与语义：**

当用户在文档中选择但未激活锚点时，会发出该信号。锚点所引用的URL会在`link`中传递。

### `[signal] void QTextBrowser::historyChanged()`

**作用与语义：**

当历史发生变化时，该信号会发出。

### `QString QTextBrowser::historyTitle(int i) const`

**作用与语义：**

返回HistoryItem的`documentTitle()`。
- `Input`：回归
- `i` < 0`: `backward()' 历史
- `i` == 0`: current, see `QTextBrowser：：source()'
- `i` > 0`: `forward()的历史

**官方示例：**

```cpp
 backaction.setToolTip(browser.historyTitle(-1));
 forwardaction.setToolTip(browser.historyTitle(+1));
```

### `QUrl QTextBrowser::historyUrl(int i) const`

**作用与语义：**

返回HistoryItem的网址。
- `Input`：回归
- `i` < 0`: `backward()的历史
- `i` == 0`: current, see `QTextBrowser：：source()'
- `i` > 0`: `forward()' 历史

### `[virtual slot] void QTextBrowser::home()`

**作用与语义：**

更改显示为历史中第一个文档的文档。

### `bool QTextBrowser::isBackwardAvailable() const`

**作用与语义：**

返回 `true` 文本浏览器是否能用`backward()`回溯文档历史。

### `bool QTextBrowser::isForwardAvailable() const`

**作用与语义：**

返回 `true` 文本浏览器是否能通过 `forward()` 在文档历史中继续前进。

### `[override virtual protected] void QTextBrowser::keyPressEvent(QKeyEvent *ev)`

**作用与语义：**

Reimpments： `QTextEdit::keyPressEvent`（QKeyEvent *e）.
事件`ev`用于提供以下快捷键：
- `Keypress`：动作
- `Alt+Left Arrow`：`backward()`
- `Alt+Right Arrow`：`forward()`
- `Alt+Up Arrow`：`home()`

### `[override virtual] QVariant QTextBrowser::loadResource(int type, const QUrl &name)`

**作用与语义：**

Reimpments： `QTextEdit::loadResource`（int type， const QUrl &name）.
该函数在文档加载时调用，文档中的每张图片均调用。`type`表示要加载的资源类型。如果无法加载资源，则返回无效`QVariant`。
默认实现忽略`type`，尝试通过将`name`解释为文件名来定位资源。如果路径不是绝对路径，则尝试在`searchPaths`属性的路径中寻找文件，且与当前源代码在同一目录中。成功后，结果是一个`QVariant`，存储包含文件内容的`QByteArray`。
如果你重新实现这个函数，可以返回其他`QVariant`类型。下表显示了根据资源类型支持的变体类型：
- `ResourceType`：`QMetaType::Type`
- `QTextDocument::HtmlResource`：`QString`或`QByteArray`
- `QTextDocument::ImageResource`：`QImage`、`QPixmap`或`QByteArray`
- `QTextDocument::StyleSheetResource`：`QString`或`QByteArray`
- `QTextDocument::MarkdownResource`：`QString`或`QByteArray`
加载由给定`type`和`name`指定的资源。
该函数是`QTextDocument::loadResource()`的扩展。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual protected] void QTextBrowser::mouseMoveEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QTextEdit::mouseMoveEvent`（QMouseEvent *e）。

### `[override virtual protected] void QTextBrowser::mousePressEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QTextEdit::mousePressEvent`（QMouseEvent *e）。

### `[override virtual protected] void QTextBrowser::mouseReleaseEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QTextEdit::mouseReleaseEvent`（QMouseEvent *e）。

### `[override virtual protected] void QTextBrowser::paintEvent(QPaintEvent *e)`

**作用与语义：**

重实现自：`QTextEdit::paintEvent`（QPaintEvent *event）。

### `[virtual slot] void QTextBrowser::reload()`

**作用与语义：**

重新加载当前设定的源码。

### `[slot] void QTextBrowser::setSource(const QUrl &url, QTextDocument::ResourceType type = QTextDocument::UnknownResource)`

**作用与语义：**

该属性保存显示文档的名称。
如果未显示文档或源未知，则这是一个无效的 URL。
在设置此属性时，`QTextBrowser` 会尝试在 `searchPaths` 属性的路径和当前源目录中查找指定名称的文档，除非该值是绝对文件路径。它还会检查可选的锚点并相应地滚动文档。
如果文档中的第一个标签是 `<qt type=detail>`，则文档作为弹出窗口显示，而不是在浏览器窗口中以新文档的形式显示。否则，文档将在文本浏览器中正常显示，文本设置为 `QTextDocument::setHtml()` 或 `QTextDocument::setMarkdown()` 的命名文档内容，取决于文件名是否以任何已知 Markdown 文件扩展名结尾。
如果您希望避免自动类型检测并明确指定类型，请调用 `setSource()`，而不是设置此属性。
默认情况下，该属性包含一个空 URL。

**如何使用：** 调用 `setSource(...)` 修改 `source`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[signal] void QTextBrowser::sourceChanged(const QUrl &src)`

**作用与语义：**

当信号源发生变化时发出，`src`成为新的信号源。
源代码的更改既可以在调用`setSource()`、`forward()`、`backward()`或`home()`时，也包括用户点击链接或按等效键序列时。

### `bool openExternalLinks() const`

**作用与语义：**

规定`QTextBrowser`是否应自动使用`QDesktopServices::openUrl()`打开指向外部源的链接，而不是发出`anchorClicked`信号。如果链接的方案既不是文件格式，也不是QRC，则视为外部链接。
默认值为假。

**如何使用：** 调用 `openExternalLinks()` 读取当前值；它不会修改应用状态。

### `bool openLinks() const`

**作用与语义：**

该属性指定了用户尝试通过鼠标或键盘激活的链接`QTextBrowser`是否应自动打开。
无论该属性的值如何，`anchorClicked`信号始终会被发射。
默认值为真。

**如何使用：** 调用 `openLinks()` 读取当前值；它不会修改应用状态。

### `QStringList searchPaths() const`

**作用与语义：**

该属性包含文本浏览器用来查找支持内容的搜索路径。
`QTextBrowser`使用这份名单来查找图片和文献。
默认情况下，该属性包含一个空字符串列表。

**如何使用：** 调用 `searchPaths()` 读取当前值；它不会修改应用状态。

### `void setOpenExternalLinks(bool open)`

**作用与语义：**

规定`QTextBrowser`是否应自动使用`QDesktopServices::openUrl()`打开指向外部源的链接，而不是发出`anchorClicked`信号。如果链接的方案既不是文件格式，也不是QRC，则视为外部链接。
默认值为假。

**如何使用：** 调用 `setOpenExternalLinks(...)` 修改 `openExternalLinks`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOpenLinks(bool open)`

**作用与语义：**

该属性指定了用户尝试通过鼠标或键盘激活的链接`QTextBrowser`是否应自动打开。
无论该属性的值如何，`anchorClicked`信号始终会被发射。
默认值为真。

**如何使用：** 调用 `setOpenLinks(...)` 修改 `openLinks`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSearchPaths(const QStringList &paths)`

**作用与语义：**

该属性包含文本浏览器用来查找支持内容的搜索路径。
`QTextBrowser`使用这份名单来查找图片和文献。
默认情况下，该属性包含一个空字符串列表。

**如何使用：** 调用 `setSearchPaths(...)` 修改 `searchPaths`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QUrl source() const`

**作用与语义：**

该属性保存显示文档的名称。
如果未显示文档或源未知，则这是一个无效的 URL。
在设置此属性时，`QTextBrowser` 会尝试在 `searchPaths` 属性的路径和当前源目录中查找指定名称的文档，除非该值是绝对文件路径。它还会检查可选的锚点并相应地滚动文档。
如果文档中的第一个标签是 `<qt type=detail>`，则文档作为弹出窗口显示，而不是在浏览器窗口中以新文档的形式显示。否则，文档将在文本浏览器中正常显示，文本设置为 `QTextDocument::setHtml()` 或 `QTextDocument::setMarkdown()` 的命名文档内容，取决于文件名是否以任何已知 Markdown 文件扩展名结尾。
如果您希望避免自动类型检测并明确指定类型，请调用 `setSource()`，而不是设置此属性。
默认情况下，该属性包含一个空 URL。

**如何使用：** 调用 `source()` 读取当前值；它不会修改应用状态。

### `QTextDocument::ResourceType sourceType() const`

**作用与语义：**

此属性保存所显示文档的类型。
如果没有显示文档或源类型未知，则为 `QTextDocument::UnknownResource`。否则，它保存已检测到的类型，或在调用 `setSource()` 时指定的类型。

**如何使用：** 调用 `sourceType()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QTextBrowser` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
