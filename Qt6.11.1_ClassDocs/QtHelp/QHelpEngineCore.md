# QHelpEngineCore
> Qt 6.11.1 · Qt Help · 来自 `QHelpEngineCore`

## 1. 先建立直觉

`QHelpEngineCore` 是 Qt Help 的无界面核心。它管理 collection 文件 `.qhc`，注册/注销 `.qch` 文档包，按 URL 读取帮助资源，查询关键词链接、命名空间、过滤器，并维护 setup 状态。

如果你要自己做帮助浏览器的 UI，而不是直接用 Qt Assistant，它通常是后端中心。

## 2. 类说明

保留类说明：这些 API 来自 `QHelpEngineCore`，属于 Qt Help 模块，用于管理帮助集合、文档注册、过滤和资源访问。

`QHelpEngine` 继承它并额外提供内容树、索引和搜索相关 widget/model。只需要后端数据时，用 core；需要现成 UI 组件时，用 `QHelpEngine`。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QHelpEngineCore(collectionFile)` | 指定 `.qhc` collection 文件；不存在时可创建。 |
| `setupData()` | 初始化 collection 数据库和已注册文档信息。 |
| `collectionFile()` | 返回 collection 文件路径。 |
| `copyCollectionFile(file)` | 复制 collection 文件。 |
| `registerDocumentation(qch)` | 注册 `.qch` 文档包。 |
| `unregisterDocumentation(namespace)` | 按 namespace 注销文档包。 |
| `registeredDocumentations()` | 列出已注册 namespace。 |
| `documentationFileName(namespace)` | 查询 namespace 对应 qch 文件。 |
| `namespaceName(qch)` | 读取 qch 的 namespace。 |
| `documentsForIdentifier(id)` | 按关键词/标识符找帮助链接。 |
| `documentsForKeyword(keyword)` | 按索引关键词找帮助链接。 |
| `fileData(url)` | 读取帮助资源内容，如 qthelp URL 指向的 HTML。 |
| `files(namespace, filters, extension)` | 查找文档包内文件。 |
| `linksForIdentifier()` / `linksForKeyword()` | 查询标识符或关键词到链接的映射。 |
| `filterEngine()` | 访问过滤器引擎。 |
| `currentFilter()` / `setCurrentFilter()` | 旧式当前过滤器入口，现代代码多看 filter engine。 |
| `error()` | 返回最近错误文本。 |
| `setupStarted()`、`setupFinished()` | 初始化过程信号。 |
| `warning(message)` | 帮助系统警告信号。 |

## 4. 典型流程

```cpp
QHelpEngineCore engine("help.qhc");
if (!engine.setupData()) {
    qWarning() << engine.error();
    return;
}

if (!engine.registerDocumentation("myproduct.qch"))
    qWarning() << engine.error();

QByteArray html = engine.fileData(QUrl("qthelp://com.acme.docs/doc/index.html"));
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 自定义帮助浏览器后端 | setup、register、fileData、links。 |
| 插件文档动态注册 | 插件安装时注册 qch，卸载时注销 namespace。 |
| 离线文档资源读取 | 用 qthelp URL 读 HTML、图片、CSS。 |
| 过滤不同产品/版本文档 | 配合 `QHelpFilterEngine`。 |

## 6. 常见坑与经验

先 `setupData()` 再访问模型、索引、搜索或资源。很多“查不到文档”的问题只是 engine 还没 setup 成功。

collection 文件是可写数据库式状态文件。应用安装目录只读时，把 `.qhc` 放到用户可写目录；`.qch` 可以在只读资源目录中。

注册失败要看 `error()`，常见原因是 namespace 重复、qch 不合法、collection 文件不可写、路径不存在。

`fileData()` 读取的是 help system 资源，不是任意网页下载器。URL 通常是 `qthelp://namespace/path`。

## 7. 知识点覆盖

- `.qhc` collection 与 `.qch` 文档包。
- 文档注册、namespace、资源读取。
- 关键词/标识符链接查询。
- setup 生命周期、错误处理和可写路径。
