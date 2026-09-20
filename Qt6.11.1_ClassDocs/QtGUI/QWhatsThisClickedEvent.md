# QWhatsThisClickedEvent

> Qt 6.11.1 · Qt GUI · 来自 `QWhatsThisClickedEvent`

## 1. 先建立直觉

`QWhatsThisClickedEvent` 表示用户在 Qt 的“这是什么？”帮助文本中点击了一个链接。它把链接地址交给应用，由应用决定打开内部帮助页、跳转到设置项、定位到文档章节，还是交给外部浏览器。

它不是普通鼠标点击事件，也不是 tooltip 事件。它发生在 What's This 帮助内容已经显示之后，负责把帮助文本中的超链接继续连接到应用行为。

## 2. 类说明

`QWhatsThisClickedEvent` 继承自 `QEvent`，事件类型是 `QEvent::WhatsThisClicked`。通常在顶层窗口或帮助控制器的 `event()` 中接收。

类说明只用于表明这些 API 来自 `QWhatsThisClickedEvent`：`href()` 保存被点击的链接，如何解析和导航由应用的帮助系统决定。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QWhatsThisClickedEvent(href)` | 构造一个携带链接地址的 What's This 点击事件。 |
| `href() const` | 返回用户点击的链接地址或锚点。 |
| `type()` | 来自 `QEvent`，通常为 WhatsThisClicked。 |

## 4. 关键用法

### 根据链接决定内部导航还是外部打开

```cpp
bool MainWindow::event(QEvent *event)
{
    if (event->type() == QEvent::WhatsThisClicked) {
        auto *clicked = static_cast<QWhatsThisClickedEvent *>(event);
        const QUrl url(clicked->href());

        if (url.scheme() == "app") {
            helpBrowser->navigateTo(url.path());
        } else {
            QDesktopServices::openUrl(url);
        }
        return true;
    }

    return QMainWindow::event(event);
}
```

应用协议适合内部帮助，`http` / `https` 等外部协议可以交给 `QDesktopServices`。

### 不要盲目信任 href

帮助文本可能来自配置、插件或外部文档。应限制允许的 scheme，必要时校验路径和参数，避免把帮助链接当成任意命令执行入口。

## 5. 使用场景

`QWhatsThisClickedEvent` 适合带有上下文帮助、内置文档浏览器、设置页导航、设计器属性说明、插件帮助和应用内知识库的桌面程序。

它也适合把帮助系统和产品内导航连接起来：用户在某个属性说明中点击“更多信息”，可以直接跳到对应设置页或诊断页面。

## 6. 常见坑与经验

不要只用字符串前缀拼接 URL。使用 `QUrl` 解析 scheme、path 和 query 更安全。

不要无条件把所有 href 交给系统打开。外部链接、内部链接和非法链接应有不同策略。

不要在事件处理里同步加载大型帮助页面。先切换界面，再异步加载内容，避免帮助点击卡住主窗口。

不要把它和普通网页浏览器点击事件混淆。只有 Qt What's This 帮助体系中的链接才会进入该事件。

## 7. 知识点覆盖

学习 `QWhatsThisClickedEvent` 应覆盖 What's This、帮助链接、`href()`、应用内 URL scheme、`QUrl` 校验、`QDesktopServices`、事件过滤、异步帮助加载和安全边界。
