# Qt QFileOpenEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QFileOpenEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QEvent -> QFileOpenEvent`  
> 定位：操作系统请求应用打开文件或 URL 时的应用级事件

## 1. 它解决什么问题

`QFileOpenEvent` 把操作系统的“请用这个应用打开文件或 URL”请求交给 Qt 应用。例如用户在 macOS Finder 双击关联文件、把文件拖到 Dock 图标，或在 iOS 从另一应用分享文件时，Qt 会向 `QApplication::instance()` 发送该事件。

它只是打开请求通知，不会替你打开文件，也不保证提供的一定是本地路径。应用可以安全地忽略不应处理的请求。

常见场景：

- 文档编辑器处理文件关联和双击打开；
- 图片查看器接收系统分享或“打开方式”请求；
- 支持自定义 URL scheme 的桌面应用；
- 单实例应用将随后到达的打开请求交给现有主窗口。

## 2. 应用级入口

通常在 `QApplication` 子类或应用级事件过滤器中处理：

```cpp
#include <QApplication>
#include <QFileOpenEvent>
#include <QUrl>

class MyApplication : public QApplication
{
public:
    using QApplication::QApplication;

    bool event(QEvent *event) override
    {
        if (event->type() == QEvent::FileOpen) {
            auto *openEvent = static_cast<QFileOpenEvent *>(event);
            handleOpenRequest(openEvent->url(), openEvent->file());
            return true;
        }
        return QApplication::event(event);
    }
};
```

事件指针只在 `event()` 调用期间有效。若应用尚未完成主窗口初始化，可复制 `QUrl` 和 `QString` 后放入待处理队列，不要保存 `QFileOpenEvent *`。

## 3. 优先处理 `url()`，谨慎回退 `file()`

处理顺序建议：

```cpp
void handleOpenRequest(const QUrl &url, const QString &file)
{
    if (url.isLocalFile()) {
        openLocalDocument(url.toLocalFile());
    } else if (url.isValid()) {
        handleSupportedUrl(url);
    } else {
        handleLegacyOpenString(file);
    }
}
```

- `url().isLocalFile()` 为真时，使用 `toLocalFile()` 获取本地路径；
- URL 有效但不是本地文件时，按 scheme 白名单处理；
- `file()` 是来源应用提供的字符串，**不保证**能直接作为 `QFile` 的本地路径。

不要把 `file()` 直接传给 `QFile`，也不要把外部 URL 直接交给浏览器、脚本解释器或文件删除逻辑。

## 4. 安全与业务边界

文件关联和 URL scheme 是外部输入入口。至少应检查：

- URL scheme 是否在支持列表；
- 本地路径是否可读、是否为期望类型；
- 文件大小、格式签名和解析错误；
- 是否需要询问用户或在受限模式打开；
- 自定义 URL 的参数编码与权限令牌。

接收 `QFileOpenEvent` 不等于文件可信，也不等于请求一定来自用户的当前可见操作。应用层应把它当成普通不可信输入。

## 5. 平台配置边界

能否收到事件不仅由 Qt 代码决定，还取决于应用包和操作系统注册。Apple 平台需要在 `Info.plist` 声明能处理的文档类型；iOS 还需要相应的文档浏览支持配置，应用才能出现在“打开方式”等入口。

Windows、Linux、macOS 的文件关联和自定义 scheme 注册方式不同。Qt 只负责把平台请求转成事件，不替代安装器、桌面文件、注册表或应用包元数据。

## 6. 常见错误

- 只读取 `file()` 并假设它一定是本地路径；
- 在事件函数结束后保存事件指针；
- 先打开文件再校验格式或权限；
- 忘记多次事件：应用启动后仍可能收到后续请求；
- 把操作系统注册问题误认为 Qt 事件分发失败；
- 处理完成却继续让基类重复处理同一请求。

## 7. 逐项 API 说明

### 构造函数

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `explicit QFileOpenEvent(const QString &file)` | 以原始文件字符串构造请求。 | 字符串不保证是可直接打开的本地路径。 |
| `explicit QFileOpenEvent(const QUrl &url)` | 以 URL 构造请求。 | 根据 `isLocalFile()` 与 scheme 决定处理方式。 |

### 查询 API

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `QString file() const` | 返回来源提供的文件名或字符串。 | 不保证是本地文件路径。 |
| `QUrl url() const` | 返回请求打开的 URL。 | 优先用它区分本地文件、有效远程 URL 与无效 URL。 |

### 已弃用 API

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `bool openFile(QFile &, QIODevice::OpenMode) const` | 直接以事件信息打开文件。 | Qt 6.6 起弃用；自行解释 `file()` 并明确错误处理。 |

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 入口 | `QApplication::event()` | 接收系统打开请求。 | 判断 `QEvent::FileOpen` 后再转换类型。 |
| 构造 | `QFileOpenEvent(QString)` | 测试原始文件字符串请求。 | 不代表可靠本地路径。 |
| 构造 | `QFileOpenEvent(QUrl)` | 测试 URL 请求。 | 优先检查 scheme 和 `isLocalFile()`。 |
| 查询 | `url()` | 得到结构化打开目标。 | 应作为主处理路径。 |
| 查询 | `file()` | 获取来源应用传来的字符串。 | 仅作回退，先解释再打开。 |
| 兼容 | `openFile()` | 旧代码直接打开文件。 | Qt 6.6 起弃用。 |
| 平台 | 应用文件关联配置 | 让操作系统发送请求。 | Qt 代码不能代替平台注册。 |

---

### 一句话总结

`QFileOpenEvent` 是操作系统交给应用的打开请求：优先按 `QUrl` 分流，只有确认是本地文件后才把它作为路径处理。
