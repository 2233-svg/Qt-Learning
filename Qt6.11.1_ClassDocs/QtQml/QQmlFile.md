# QQmlFile
> Qt 6.11.1 · Qt QML · 来自 `QQmlFile`

## 作用定位

`QQmlFile` 提供 QML 相关 URL 与本地文件路径之间的静态辅助函数。它主要解决 `file:`、本地路径、`qrc:` 资源之间的判断和转换问题。

## 类说明

- 头文件：`#include <QQmlFile>`
- CMake：链接 `Qt6::Qml`
- 形式：静态工具类，不需要实例化

## API 速查

| API | 说明 |
| --- | --- |
| `isLocalFile(QString)` | 判断字符串 URL 是否指向本地文件。 |
| `isLocalFile(QUrl)` | 判断 QUrl 是否为本地文件。 |
| `urlToLocalFileOrQrc(QString)` | 把 URL 字符串转成本地路径或 `:/` qrc 路径。 |
| `urlToLocalFileOrQrc(QUrl)` | QUrl 版本转换。 |

## 使用场景

- QML 工具链中把资源 URL 转成可打开的本地路径。
- 支持 `qrc:/` 和 `file:/` 两类资源来源。
- 错误日志或调试器中展示可读文件路径。

## 常见坑与经验

- 网络 URL 不是本地文件，不能强行转成本地路径。
- `qrc:/foo.qml` 与 `:/foo.qml` 表示方式不同，转换时要清楚目标 API 需要哪一种。
- QML 资源 URL 可能经过 interceptor 或 file selector，调试时要看最终 URL。
- 不要用普通字符串拼接 URL，优先用 `QUrl` 处理编码和路径分隔。

## 知识点覆盖

- QML URL 与本地路径
- qrc 资源路径
- 本地文件判断
- 工具链和调试辅助
