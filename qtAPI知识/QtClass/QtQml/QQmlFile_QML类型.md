# QQmlFile：按 QML 引擎规则判断 URL 是否可由 QFile 打开

> Qt 6.11.1 · `#include <QQmlFile>` · 模块：`Qt6::Qml`

`QQmlFile` 是一组静态 URL 分类工具。它解决的是 C++ 桥接层不能只凭 `QUrl::isLocalFile()` 判断“QML 会把这个 URL 当作可本地打开的资源”的问题。

QML 引擎将 `file:` 和 `qrc:` URL 视为可由 `QFile` 打开的本地文件；Android 上还会把 `assets:` 和 `content:` 视为本地文件。需要在 C++ 中复用 QML 的这一判定时使用它。

```cpp
#include <QQmlFile>
#include <QFile>

const QUrl url(u"qrc:/assets/config.json"_s);
const QString path = QQmlFile::urlToLocalFileOrQrc(url);
if (!path.isEmpty()) {
    QFile file(path);
    file.open(QIODevice::ReadOnly);
}
```

工程链接 `Qt6::Qml`；qmake 使用 `QT += qml`。

## 使用边界

`isLocalFile()` 表示“该 URL 可按 QML 的本地资源语义交给 `QFile`”，不是“资源一定存在、可读或安全”。真正打开前仍要检查 `QFile::open()` 的结果。

`urlToLocalFileOrQrc()` 对非本地 URL 返回空字符串。空结果不能与有效但为空的路径混为一谈；它应触发网络/自定义 scheme 的另一条处理路径，而不是继续把原始 URL 当普通文件名传给 `QFile`。

不要用它决定访问授权。`file:`、`qrc:`、Android `content:` 的可访问性仍受平台、沙箱和应用策略控制。

## API 速查表

| API | 用途 | 语义与边界 |
| --- | --- | --- |
| `isLocalFile(const QUrl&)` | 判断 URL 是否可由 QFile 打开 | 识别 `file:`、`qrc:`；Android 还识别 `assets:`、`content:`。 |
| `isLocalFile(const QString&)` | 判断 URL 字符串 | 适合尚未解析为 QUrl 的输入。 |
| `urlToLocalFileOrQrc(const QUrl&)` | 转为 QFile 可用路径 | 非本地 URL 返回空字符串。 |
| `urlToLocalFileOrQrc(const QString&)` | 从字符串转本地/qrc 路径 | 转换成功也仍需检查文件是否存在和可读。 |

它的职责仅是复刻 QML 的资源分类规则；资源加载、网络回退、权限和错误处理仍属于调用方。
