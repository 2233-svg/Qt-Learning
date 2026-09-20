# QFileSystemModel

> Qt 6.11.1 · Qt GUI · 来自 `QFileSystemModel`

## 1. 先建立直觉

`QFileSystemModel` 是把本地文件系统暴露给 Qt 模型/视图框架的模型。它可以直接接到 `QTreeView`、`QListView`、`QTableView` 或代理模型上，让视图按目录树浏览文件、显示图标、大小、类型和修改时间。

它不是简单的 `QDir::entryList()` 包装。目录内容会按需加载，文件变化可由 watcher 反映到模型，图标和类型文本可能查询平台服务；这些都意味着它既有模型/视图协议，也有真实文件系统副作用和性能边界。

## 2. 类说明

- 头文件：`#include <QFileSystemModel>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QAbstractItemModel`
- 典型视图：目录树、文件列表、文件选择器、资源管理器侧栏。
- 重要协作类：`QFileInfo`、`QDir`、`QAbstractFileIconProvider`、`QModelIndex`。

`QFileSystemModel` 位于 Qt GUI 模块，但经常和 Qt Widgets 视图配合使用。模型应在 GUI 线程被视图访问；不要从后台线程直接改正在显示的模型。

## 3. API 速查

| API | 用途 |
|---|---|
| `setRootPath(path)` | 设置模型监控和加载的根路径，返回该路径索引。 |
| `rootPath()` / `rootDirectory()` | 查询当前根路径。 |
| `index(path, column)` | 将文件路径映射到模型索引。 |
| `filePath(index)` / `fileName(index)` | 从索引取得完整路径或文件名。 |
| `fileInfo(index)` | 返回对应 `QFileInfo`。 |
| `isDir(index)` | 判断索引是否为目录。 |
| `size(index)` / `type(index)` / `lastModified(index)` | 查询大小、类型、修改时间。 |
| `lastModified(index, tz)` | Qt 6.6 起按指定时区返回修改时间。 |
| `fileIcon(index)` | 返回文件或目录图标。 |
| `setIconProvider(provider)` | 替换图标提供策略。 |
| `setFilter(filters)` / `filter()` | 设置 `QDir::Filters`，决定哪些项进入模型。 |
| `setNameFilters(filters)` | 设置名称通配过滤，如 `*.png`。 |
| `setNameFilterDisables(on)` | 不匹配项是禁用还是隐藏。 |
| `setReadOnly(on)` / `isReadOnly()` | 控制是否允许重命名、拖放、删除等写操作。 |
| `mkdir(parent, name)` | 在父目录下创建目录。 |
| `remove(index)` | 删除文件或条目。 |
| `rmdir(index)` | 删除目录。 |
| `setOptions()` / `setOption()` / `testOption()` | 设置 watcher、符号链接、目录图标等行为。 |
| `directoryLoaded(path)` | 异步目录加载完成信号。 |
| `rootPathChanged(path)` | 根路径改变信号。 |
| `fileRenamed(path, oldName, newName)` | 文件成功重命名信号。 |

## 4. 关键用法

### 接到视图并设置视图根

```cpp
auto *model = new QFileSystemModel(this);
const QModelIndex rootIndex = model->setRootPath(QDir::homePath());

treeView->setModel(model);
treeView->setRootIndex(rootIndex);
```

`setRootPath()` 让模型开始监控和加载该路径，但它**不会自动让视图只显示这个目录**。视图要调用 `setRootIndex(rootIndex)`，否则仍可能从模型的顶层结构开始显示。

### 过滤目录和文件

```cpp
model->setFilter(QDir::AllDirs | QDir::Files | QDir::NoDotAndDotDot);
model->setNameFilters({ "*.png", "*.jpg", "*.jpeg" });
model->setNameFilterDisables(false); // 不匹配的项直接隐藏
```

如果想保留目录树导航，`setFilter()` 通常要包含 `QDir::AllDirs`，否则模型可能无法继续读取目录结构。`nameFilterDisables(true)` 会让不匹配项变灰但仍显示；`false` 则隐藏不匹配项。

### 使用数据角色

| Role | 返回内容 |
|---|---|
| `FileIconRole` | 文件图标，等同装饰角色语义。 |
| `FilePathRole` | 完整路径。 |
| `FileNameRole` | 文件名。 |
| `FilePermissions` | `QFileDevice::Permissions`。 |
| `FileInfoRole` | `QFileInfo` 对象。 |

视图展示通常用标准 role；业务逻辑需要路径或 `QFileInfo` 时，优先用专用函数或 role，而不是解析显示文本。

## 5. 选项与性能

| 选项 | 作用 |
|---|---|
| `DontWatchForChanges` | 不安装文件系统监视器，降低开销，但外部变化不会自动反映。 |
| `DontResolveSymlinks` | 不解析符号链接；默认会解析，主要与 Windows 行为相关。 |
| `DontUseCustomDirectoryIcons` | 使用默认目录图标，避免网络盘/移动盘上查询自定义图标造成卡顿。 |

选项应尽量在设置路径和加载目录前配置。图标提供、符号链接解析和 watcher 都可能影响首次加载和滚动体验。

## 6. 文件系统写操作

| API | 注意事项 |
|---|---|
| `setReadOnly(false)` | 允许视图编辑、拖放和删除等写操作；默认只读。 |
| `setData(index, value, Qt::EditRole)` | 常用于重命名，成功后可能触发 `fileRenamed()`。 |
| `mkdir(parent, name)` | 创建真实目录，失败会返回无效索引。 |
| `remove(index)` | 删除真实文件或条目，不移动到回收站。 |
| `rmdir(index)` | 删除真实目录，通常要求目录可删除；也不进入回收站。 |
| 拖放相关重实现 | `dropMimeData()`、`mimeData()`、`supportedDropActions()` 参与文件移动/复制。 |

`remove()` 和 `rmdir()` 是危险 API：它们操作真实文件系统，不是把条目从模型中隐藏。面向用户的文件管理器通常应提供确认、错误提示和撤销/回收站策略，而不是直接调用。

## 7. 常见坑与经验

- 目录加载是按需和异步的。`rowCount()` 初期可能还不是最终结果；需要等待 `directoryLoaded(path)`。
- `QModelIndex` 不是长期文件句柄。文件被删除、模型重置或路径变化后，旧索引可能失效；持久业务引用应保存路径或使用 `QPersistentModelIndex` 并仍做有效性检查。
- `type(index)` 和图标文本是面向用户的本地化信息，不应用作机器判断。判断文件类型应使用 `QMimeDatabase` 或业务规则。
- 网络盘、大目录和自定义目录图标会拖慢界面；必要时设置选项并限制过滤范围。
- `lastModified(index, QTimeZone::UTC)` 可避免本地时间转换，适合内部排序或同步；显示给用户时通常用本地时间。
- 文件系统权限、符号链接、大小写敏感性和隐藏文件规则都有平台差异。

## 8. 知识点覆盖

- 模型/视图索引、数据角色和异步 fetch
- 文件系统 watcher、目录加载和根路径
- 名称过滤、目录过滤和不匹配项显示策略
- 文件图标提供与平台性能
- 真实文件创建、重命名、删除和拖放副作用
- 符号链接、权限、时间区和跨平台差异
