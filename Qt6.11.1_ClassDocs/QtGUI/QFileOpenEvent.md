# QFileOpenEvent

> Qt 6.11.1 · Qt GUI · 来自 `QFileOpenEvent`

## 1. 先建立直觉

`QFileOpenEvent` 表示操作系统要求应用打开某个资源。它常见于用户双击与应用关联的文件、从文件管理器“打开方式”启动应用、拖入系统文件，或平台把 URL / deep link 转交给已运行应用。

它不是 `QFile` 的打开结果，也不保证资源一定是本地文件。`file()` 是兼容接口，`url()` 才是更完整的表达：资源可能是 `file:` URL、网页 URL、自定义 scheme，甚至没有适合直接映射为本地路径的内容。

## 2. 类说明

`QFileOpenEvent` 继承自 `QEvent`，类型为 `QEvent::FileOpen`。在 Qt GUI 应用中，常由 `QGuiApplication` 或主窗口的 `event()` 接收。

类说明只用于表明这些 API 来自 `QFileOpenEvent`：事件只传递要打开的资源标识；权限检查、格式识别、最近文件、异步加载和错误 UI 都由应用负责。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `url() const` | 返回应用应该打开的完整 `QUrl`，优先使用。 |
| `file() const` | 返回资源的文件名表示；不保证是可直接用 `QFile` 打开的本地路径。 |
| `type()` | 来自 `QEvent`，通常为 `QEvent::FileOpen`。 |

## 4. 关键用法

### 优先按 URL 路由

```cpp
bool AppController::event(QEvent *event)
{
    if (event->type() == QEvent::FileOpen) {
        auto *openEvent = static_cast<QFileOpenEvent *>(event);
        openResource(openEvent->url());
        return true;
    }

    return QObject::event(event);
}

void AppController::openResource(const QUrl &url)
{
    if (url.isLocalFile()) {
        openDocument(url.toLocalFile());
    } else if (url.scheme() == "myapp") {
        openDeepLink(url);
    } else {
        showUnsupportedUrl(url);
    }
}
```

这样既能处理文件关联，也能自然扩展到自定义 URI scheme。

### 做启动早期的请求缓冲

文件打开事件可能在主窗口完全准备好前到达。应用可以把 URL 暂存，等文档控制器、会话恢复、权限初始化完成后再打开，避免在半初始化状态直接创建文档。

### 文件访问仍要做错误处理

系统把 URL 交给应用不代表它可读：文件可能已删除、无权限、被占用，或者 URL 指向不支持的协议。`QFileOpenEvent` 只是请求，不是成功保证。

## 5. 使用场景

`QFileOpenEvent` 适合文档编辑器、图片查看器、播放器、IDE、设计工具、浏览器式桌面应用和支持 deep link 的客户端。

它在 macOS 文件关联、桌面文件管理器打开、单实例应用接收后续打开请求等场景尤其重要。不要只在 `main()` 读取命令行参数，否则已运行应用收到的新打开请求会漏掉。

## 6. 常见坑与经验

不要只调用 `file()` 后直接 `QFile::open()`。优先读取 `url()`，再通过 `isLocalFile()` 判断是否能安全转换为本地路径。

不要把事件里的路径当成可信输入。文件类型、大小、符号链接、权限和自定义 URI 参数都应按应用安全策略验证。

不要阻塞事件处理去同步加载超大文件。收到事件后可启动异步加载，并及时给出加载状态或错误反馈。

不要忽略单实例语义。新文件打开请求应该进入现有会话的文档管理流程，而不是隐式创建互相独立的全局状态。

## 7. 知识点覆盖

学习 `QFileOpenEvent` 应覆盖文件关联、URL 与本地路径、deep link、单实例应用、启动时序、异步文档加载、文件权限、资源路由和跨平台桌面集成。
