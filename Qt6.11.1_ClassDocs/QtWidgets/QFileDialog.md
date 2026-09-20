# QFileDialog

> Qt 6.11.1 · Qt Widgets · 来自 `QFileDialog`

## 1. 先建立直觉

`QFileDialog` 是让用户选择文件、多个文件、目录或保存路径的标准对话框。它不负责读写文件内容，而是负责得到用户确认后的路径或 URL。

常见使用场景包括打开文档、导入图片、选择导出目录、保存文件、选择远程 URL。静态函数适合一次性选择；实例化对话框适合自定义侧边栏、过滤器、代理模型、非阻塞打开或保存恢复状态。

## 2. 类说明

- 头文件：`#include <QFileDialog>`
- 模块：`Qt6::Widgets`
- 继承自：`QDialog`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

文件对话框可能使用平台原生实现；某些自定义能力只有 Qt 非原生对话框中完全可控。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `getOpenFileName()` / `getOpenFileNames()` | 快速选择一个或多个本地文件路径。 |
| `getSaveFileName()` | 快速选择保存路径。 |
| `getExistingDirectory()` | 快速选择本地目录。 |
| `getOpenFileUrl()` / `getOpenFileUrls()` | 选择 URL，支持本地或指定 scheme。 |
| `getSaveFileUrl()` / `getExistingDirectoryUrl()` | 保存或选择目录的 URL 版本。 |
| `getOpenFileContent()` / `saveFileContent()` | 适合平台抽象文件访问的内容级打开/保存。 |
| `setAcceptMode()` | 打开模式或保存模式。 |
| `setFileMode()` | 允许选择任意文件、现有文件、目录或多个文件。 |
| `setDirectory()` / `setDirectoryUrl()` | 设置初始目录。 |
| `selectedFiles()` / `selectedUrls()` | 对话框接受后读取选择结果。 |
| `selectFile()` / `selectUrl()` | 预选文件或 URL。 |
| `setNameFilter()` / `setNameFilters()` | 设置按名称/扩展名过滤。 |
| `selectedNameFilter()` / `selectNameFilter()` | 读取或指定当前名称过滤器。 |
| `setMimeTypeFilters()` / `selectedMimeTypeFilter()` | 使用 MIME 类型过滤。 |
| `setDefaultSuffix()` | 保存时用户未写后缀则自动补。 |
| `setViewMode()` | 列表或详细信息视图。 |
| `setOptions()` / `setOption()` / `testOption()` | 控制原生对话框、只读、符号链接、覆盖确认等。 |
| `setSupportedSchemes()` | URL 对话框允许哪些 scheme。 |
| `setSidebarUrls()` / `sidebarUrls()` | 设置侧边栏常用位置。 |
| `setHistory()` / `history()` | 读写访问历史。 |
| `setProxyModel()` / `proxyModel()` | 使用代理模型过滤或排序文件项。 |
| `setIconProvider()` / `iconProvider()` | 自定义文件图标来源。 |
| `setItemDelegate()` | 自定义非原生文件列表绘制。 |
| `setLabelText()` / `labelText()` | 改写界面标签文本。 |
| `saveState()` / `restoreState()` | 保存恢复对话框布局状态。 |
| `open(receiver, member)` | 异步打开。 |
| `fileSelected()` / `filesSelected()` | 本地路径选择完成。 |
| `urlSelected()` / `urlsSelected()` | URL 选择完成。 |
| `currentChanged()` / `directoryEntered()` | 当前项或目录变化。 |
| `filterSelected()` | 过滤器变化。 |

## 4. 关键用法

### 打开、保存、目录选择要分清

`AcceptOpen` 搭配 `ExistingFile` 或 `ExistingFiles` 是打开；`AcceptSave` 搭配 `AnyFile` 是保存；选择目录用 `Directory` 或静态 `getExistingDirectory()`。保存路径不代表文件已经创建，拿到路径后仍要自己写文件并处理失败。

### 过滤器是用户体验，也是输入约束提示

名称过滤器如 `"Images (*.png *.jpg);;Text files (*.txt)"` 主要帮助用户筛选视图，不是安全校验。真正打开或保存前仍要检查扩展名、MIME、权限和文件存在性。

`defaultSuffix` 只在保存时用户没写后缀才补。不要把它当成强制文件类型；用户仍可能手动输入别的后缀。

### 本地路径和 URL 不要混用

`selectedFiles()` 返回本地路径字符串；`selectedUrls()` 返回 `QUrl`，可以表达非本地 scheme。需要远程位置、沙盒平台或门户文件访问时优先考虑 URL 版本和内容级 API。

### 原生对话框的取舍

原生对话框外观和系统体验最好，但可定制性有限。需要代理模型、自定义 delegate、某些标签或行为控制时，可能要设置 `DontUseNativeDialog`。该选项要在显示前尽早设置。

### 保存状态

实例化对话框时，`saveState()` / `restoreState()` 可以保存大小、视图模式等 UI 状态。目录历史和最近使用路径通常放在 `QSettings` 中，下一次作为初始目录传入。

## 5. 常见坑与经验

- 用户取消时静态函数通常返回空字符串/空列表，要先判断。
- 选择保存路径后必须自己确认写入是否成功。
- `DontConfirmOverwrite` 会跳过覆盖确认，保存重要文件时慎用。
- 网络目录和自定义图标查询可能很慢，必要时使用 `DontUseCustomDirectoryIcons`。
- 原生文件对话框的平台行为差异很正常，不要依赖内部 widget 结构。
