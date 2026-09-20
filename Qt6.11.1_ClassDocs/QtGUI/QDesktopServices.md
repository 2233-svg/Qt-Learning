# QDesktopServices

> Qt 6.11.1 · Qt GUI · 来自 `QDesktopServices`

## 1. 先建立直觉

`QDesktopServices` 是把 URL 交给桌面环境处理的工具类。你给它一个 `QUrl`，系统会用默认浏览器、邮件客户端、文件管理器或注册的应用打开。

它不是网络库，也不是文件读取 API。它的职责是“请求系统用合适的外部程序打开这个资源”。

## 2. 类说明

`QDesktopServices` 只有静态函数。最常用的是 `openUrl()`。还可以通过 `setUrlHandler()` 为自定义 scheme 注册应用内处理器。

`openUrl()` 返回 `true` 只表示请求成功提交给系统，不保证外部应用最终真的打开成功。跨平台时尤其要处理失败和权限限制。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `openUrl(const QUrl &)` | 用系统默认处理器打开 URL、文件、mailto 等。 |
| `setUrlHandler(scheme, receiver, method)` | 为某个 URL scheme 注册应用内处理槽。 |
| `unsetUrlHandler(scheme)` | 移除自定义 scheme 处理器。 |
| `QUrl::fromLocalFile()` | 构造本地文件 URL 的推荐方式。 |
| `mailto:` URL | 请求系统邮件客户端打开撰写窗口。 |
| `file:` URL | 请求系统用关联程序打开本地文件。 |

## 4. 关键用法

```cpp
QDesktopServices::openUrl(QUrl("https://www.qt.io"));
```

打开本地文件：

```cpp
QDesktopServices::openUrl(QUrl::fromLocalFile(filePath));
```

自定义 scheme：

```cpp
QDesktopServices::setUrlHandler("myapp", this, "handleAppUrl");
```

对应槽需要接收一个 `QUrl` 参数。

## 5. 使用场景

适合打开网页、帮助链接、用户文档、下载目录、发送邮件、从外部 deep link 回到应用。

如果你要读取网页内容，用 Qt Network；如果要读取文件内容，用 QFile。`QDesktopServices` 只是把资源交给外部程序。

## 6. 常见坑与经验

返回 `true` 不代表外部应用已经成功显示内容。它只是“请求已交给系统”。

本地路径不要手拼 `file:///`，用 `QUrl::fromLocalFile()` 处理空格、分隔符和编码。

移动平台和沙盒系统常有白名单、权限或 Info.plist/manifest 限制。桌面能打开，不代表移动端也能。
