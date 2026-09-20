# Qt QTextBrowser 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QTextBrowser>`
> 所属模块：`Qt6::Widgets`
> 继承：`QTextEdit -> QTextBrowser`
> 常见搭档：`QUrl`、`QDesktopServices`、`QTextDocument`

## 1. QTextBrowser 解决什么问题

`QTextBrowser` 是带超链接导航能力的文本浏览器。它不是单纯“能显示富文本”的文本框，而是一个会记住访问历史、会解析链接、会按 URL 找资源的浏览器型控件。

它适合放在：

- 帮助文档查看器；
- 内置说明页或 About 页面；
- 需要点链接跳转的说明面板；
- 轻量级文档阅读器；
- 既要显示 HTML/Markdown，又要保留前进、后退、主页导航的界面。

它和 `QTextEdit` 的差别很关键：

- `QTextEdit` 更像通用富文本编辑器；
- `QTextBrowser` 更像只读阅读器，外加导航逻辑。

如果你的界面需要“显示内容 + 点击链接 + 前进后退”，通常就该想到它。

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 显示一个本地页面

```cpp
#include <QApplication>
#include <QTextBrowser>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QTextBrowser browser;
    browser.setSource(QUrl::fromLocalFile(QStringLiteral("D:/docs/help.html")));
    browser.resize(800, 600);
    browser.show();

    return app.exec();
}
```

### 2.3 让浏览器显示后可以点链接

```cpp
QTextBrowser *browser = new QTextBrowser;
browser->setOpenLinks(true);
browser->setOpenExternalLinks(false);
```

`openLinks` 和 `openExternalLinks` 是两层不同的控制：

- `openLinks` 决定用户点到链接后，浏览器是否自动导航；
- `openExternalLinks` 决定外部链接是否直接交给 `QDesktopServices::openUrl()`。

## 3. 先理解它的导航模型

### 3.1 `source` 是当前页面

`source` 表示当前展示的文档 URL。`setSource()` 会根据 URL 去加载内容；如果 URL 带有锚点，浏览器还会滚动到对应位置。

### 3.2 `searchPaths` 负责找资源

当 URL 不是绝对路径时，`QTextBrowser` 会按搜索路径和当前文档目录去找资源。这个机制特别适合帮助文档：

- 主文档在一个目录；
- 图片、子页面、样式表分散在同一资源树；
- 访问时只写相对路径。

### 3.3 历史记录是它的核心能力

浏览器会记录访问过的页面，形成一个历史栈。于是你就能得到：

- `backward()` / `forward()`；
- `home()`；
- `reload()`；
- `historyTitle()` / `historyUrl()`；
- `backwardHistoryCount()` / `forwardHistoryCount()`。

这就是它和普通文本框最大的分野之一。

### 3.4 `setSource()` 和 `doSetSource()`

在 Qt 6 里，`setSource()` 是公开入口，而真正可重写的是 `doSetSource()`。如果你要定制页面跳转逻辑，应覆写 `doSetSource()`，而不是去碰更上层的调用方式。

## 4. 常见使用方式

### 4.1 作为帮助浏览器

```cpp
browser->setSearchPaths({QStringLiteral("D:/docs/images")});
browser->setSource(QUrl(QStringLiteral("qrc:/docs/index.html")));
```

这种场景里，`QTextBrowser` 负责页面跳转、图片加载和历史管理，外层窗口只需要摆放“返回”“前进”“主页”按钮。

### 4.2 自己接管链接打开

```cpp
browser->setOpenLinks(false);
QObject::connect(browser, &QTextBrowser::anchorClicked,
                 browser, [browser](const QUrl &url) {
                     browser->setSource(url);
                 });
```

这样做适合“点链接但我想先过滤一下”的场景，比如：

- 禁止跳转到某些协议；
- 先做权限判断；
- 先在应用内打开，再决定是否跳外部浏览器。

### 4.3 利用历史状态做按钮联动

```cpp
connect(browser, &QTextBrowser::backwardAvailable,
        backButton, &QPushButton::setEnabled);
connect(browser, &QTextBrowser::forwardAvailable,
        forwardButton, &QPushButton::setEnabled);
```

`historyChanged()`、`backwardAvailable()`、`forwardAvailable()` 这几个信号非常适合驱动工具栏状态。

## 5. 资源加载和链接打开

### 5.1 `loadResource()`

`loadResource()` 会在文档加载时、图片加载时被调用。默认实现会按文件名找资源；如果你重写它，就能把内容从数据库、网络缓存或自定义资源系统里取出来。

这正是 `QTextBrowser` 适合作为“文档外壳”的原因：内容来源不必局限于本地文件。

### 5.2 `openExternalLinks`

这个属性适合“外部链接直接交给系统浏览器”的场景。一般在帮助系统里，站内页面还是留在浏览器内，站外地址才交给系统。

### 5.3 `openLinks`

如果关闭它，链接点击仍会发出 `anchorClicked()`，但不会自动跳转。这个模式适合你想完全掌控导航流程的时候。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QTextBrowser(QWidget *parent = nullptr)` | 创建一个空的文本浏览器。 | 默认就是只读阅读器思路。 |
| 析构 | `~QTextBrowser()` | 销毁浏览器对象。 | 由 QWidget 父子关系管理生命周期。 |
| 属性 | `source : QUrl` | 当前正在显示的文档 URL。 | 相对路径、锚点和资源搜索都围绕它工作。 |
| 属性 | `sourceType : QTextDocument::ResourceType` | 当前源的资源类型。 | 只读；没有页面时通常是 `UnknownResource`。 |
| 属性 | `searchPaths : QStringList` | 搜索资源时使用的路径列表。 | 适合帮助文档、图片和本地资源定位。 |
| 属性 | `openExternalLinks : bool` | 控制外部链接是否直接交给系统打开。 | 一般用于站外链接。 |
| 属性 | `openLinks : bool` | 控制点击链接后是否自动导航。 | 关掉后可自己接管 `anchorClicked()`。 |
| 查询 | `isBackwardAvailable() const` | 当前是否还能后退。 | 适合驱动“后退”按钮。 |
| 查询 | `isForwardAvailable() const` | 当前是否还能前进。 | 适合驱动“前进”按钮。 |
| 查询 | `backwardHistoryCount() const` | 后退历史有多少项。 | 做历史菜单时有用。 |
| 查询 | `forwardHistoryCount() const` | 前进历史有多少项。 | 同上。 |
| 查询 | `historyTitle(int i) const` | 查询历史中某一项的标题。 | `i < 0` 是后退历史，`i > 0` 是前进历史。 |
| 查询 | `historyUrl(int i) const` | 查询历史中某一项的 URL。 | 适合做历史下拉列表。 |
| 修改 | `setSearchPaths(const QStringList &paths)` | 设置资源搜索路径。 | 很多相对路径加载都靠它。 |
| 修改 | `setOpenExternalLinks(bool open)` | 设置是否自动打开外部链接。 | 外部链接是否跳系统浏览器。 |
| 修改 | `setOpenLinks(bool open)` | 设置是否自动打开用户点击的链接。 | 关闭后可自己接管导航。 |
| 修改 | `setSource(const QUrl &name, QTextDocument::ResourceType type = QTextDocument::UnknownResource)` | 打开并显示指定文档。 | 是最常用的页面切换入口。 |
| 槽 | `backward()` | 回到上一页。 | 依赖历史栈。 |
| 槽 | `forward()` | 去下一页。 | 依赖历史栈。 |
| 槽 | `home()` | 回到历史首页。 | 适合“主页”按钮。 |
| 槽 | `reload()` | 重新加载当前源。 | 适合文档热更新。 |
| 信号 | `anchorClicked(const QUrl &link)` | 用户点到链接时发出。 | 可用来接管导航。 |
| 信号 | `backwardAvailable(bool)` | 后退能力变化时发出。 | 工具栏联动常用。 |
| 信号 | `forwardAvailable(bool)` | 前进能力变化时发出。 | 工具栏联动常用。 |
| 信号 | `historyChanged()` | 历史记录发生变化时发出。 | 更新历史菜单或按钮状态。 |
| 信号 | `sourceChanged(const QUrl &src)` | 当前源变化时发出。 | 可同步窗口标题或路径栏。 |
| 信号 | `highlighted(const QUrl &link)` | 鼠标悬停到链接时发出。 | 常用于状态栏提示。 |
| 受保护函数 | `loadResource(int type, const QUrl &name)` | 自定义资源加载。 | 适合从内存、缓存或数据库取内容。 |
| 受保护函数 | `doSetSource(const QUrl &name, QTextDocument::ResourceType type = QTextDocument::UnknownResource)` | 自定义页面切换逻辑。 | Qt 6 推荐的导航扩展点。 |
| 受保护函数 | `event(QEvent *e)` | 处理通用事件。 | 影响链接、导航和焦点行为。 |
| 受保护函数 | `keyPressEvent(QKeyEvent *ev)` | 处理按键。 | 可接管快捷导航。 |
| 受保护函数 | `mouseMoveEvent(QMouseEvent *ev)` | 处理鼠标移动。 | 控制悬停和高亮。 |
| 受保护函数 | `mousePressEvent(QMouseEvent *ev)` | 处理鼠标按下。 | 常与链接点击相关。 |
| 受保护函数 | `mouseReleaseEvent(QMouseEvent *ev)` | 处理鼠标释放。 | 链接激活常会经过这里。 |
| 受保护函数 | `focusOutEvent(QFocusEvent *ev)` | 处理失焦。 | 与导航结束、状态清理有关。 |
| 受保护函数 | `focusNextPrevChild(bool next)` | 处理焦点链切换。 | 文档阅读器的键盘体验常会碰到。 |
| 受保护函数 | `paintEvent(QPaintEvent *e)` | 处理绘制。 | 自定义外观时会用到。 |

### 一句话总结

`QTextBrowser` 是带历史栈和链接导航的只读文本浏览器；它解决的是“文档怎么展示、链接怎么跳、资源怎么找”这一整套问题。
