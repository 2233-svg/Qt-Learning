# QQuickTextDocument：让 TextEdit/TextArea 读取和保存富文本文件

> Qt 6.11.1 | `#include <QQuickTextDocument>` | CMake: `Qt6::Quick`

`QQuickTextDocument` 是 Qt Quick Controls 中 `TextEdit` 和 `TextArea` 暴露的文档桥接对象。在 QML 里它以 `textDocument` 属性出现，用来把编辑器背后的 `QTextDocument` 与一个可加载、可保存的 URL 联系起来。

它适合实现带“打开、修改标记、保存、另存为、错误提示”的文本或富文本编辑器。`TextDocument` 不是一个能在 QML 中独立构造的类型，只能从 `TextEdit` 或 `TextArea` 取得；加载和保存相关 API 在 Qt 6.7 引入且仍标为 preliminary，升级 Qt 时应复核行为和接口。

## QML 中的使用方式

```qml
TextArea {
    id: editor
    textDocument.source = "file:///C:/notes/today.html"

    onTextChanged: {
        // modified 会随用户编辑反映未保存状态
    }
}
```

设置 `source` 会从 Qt 支持的 URL scheme 加载任何 `QTextDocument` 支持的文本格式。实际应用应监听 `status` 和 `errorString`，不要把“已经发起加载”当成“文件可用”。`Loaded` 与 `ReadError` 才是一次读取的终态。

## 未保存内容会阻止换文件

`modified` 表示自上次加载或保存后用户是否修改过内容，默认是 false。`modified == true` 时不能再设置不同的 `source`，这是为了避免意外丢弃编辑。通常先提示用户保存、放弃或取消；只有确实放弃时才调用 `setModified(false)`，然后切换 URL。

`save()` 写回当前 `source` 指向的同一文件和格式；`saveAs(url)` 写到新 URL，文件扩展名决定格式。两者**只允许写入已挂载文件系统上的本地文件**。向远程 URL `saveAs()` 会得到 `NonLocalFileError`，写入失败则是 `WriteError`；应读取 `errorString` 显示具体原因，而不是只依赖一个布尔结果，因为 API 不返回成功值。

## 和 C++ QTextDocument 协作

`textDocument()` 取出底层 `QTextDocument`，可用于 C++ 层进行查找、高亮、打印或对接现有文档逻辑。Qt 6.7 起 `setTextDocument(document)` 可以替换它，但调用方仍保有 `document` 的所有权，必须保证其生命期覆盖 `QQuickTextDocument` 的使用期。替换实例后监听 `textDocumentChanged()`，不要保留旧指针。

## 状态机

| 状态 | 含义 |
|---|---|
| `Null` | 尚未加载文件 |
| `Loading` / `Loaded` | 正在读取 / 成功读取 |
| `Saving` / `Saved` | 正在写入 / 成功写入 |
| `ReadError` / `WriteError` | 读取 / 写入失败 |
| `NonLocalFileError` | `saveAs()` 的 URL 不是本地文件 |

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `textDocument` | `TextEdit`/`TextArea` 提供的 `QQuickTextDocument` | QML 中不可独立创建；文件操作 API 为 preliminary |
| `source` / `setSource(url)` | 加载文档内容的 URL | `modified` 为 true 时不能改源；本地路径应使用正确的 `file:` URL |
| `modified` / `isModified()` / `setModified()` | 未保存的用户修改标志 | 将其设为 false 可放弃改动并允许切换 `source` |
| `status` / `statusChanged()` | 读取或写入进度与结果 | 根据终态判断成功；不要只在调用 `save()` 后假定写入成功 |
| `errorString` / `errorStringChanged()` | 最近加载或保存失败的可读说明 | 默认空；与 `ReadError`、`WriteError` 等状态配合使用 |
| `save()` | 保存到当前 `source` 的同一文件和格式 | 仅已挂载文件系统上的本地文件可写 |
| `saveAs(url)` | 保存到另一个 URL，并由扩展名决定格式 | 远程 URL 会产生 `NonLocalFileError` |
| `textDocument()` | 获取底层 `QTextDocument *` | 用于 C++ 文档操作；注意对象生命期 |
| `setTextDocument(document)` | 换用调用方提供的 `QTextDocument` | Qt 6.7 起；不转移所有权 |
| `textDocumentChanged()` | 底层 `QTextDocument` 实例已更换 | 清理或更新先前缓存的文档指针 |
