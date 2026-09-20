# QFileSystemModel

`QFileSystemModel` 把本地文件系统映射为 `QAbstractItemModel`：目录成为父索引，文件和子目录成为行，视图可以直接浏览、排序、重命名、拖放和删除真实文件。

- 头文件：`#include <QFileSystemModel>`
- 模块：`Qt6::Gui`
- 继承：`QAbstractItemModel`
- 对象特性：不可复制的 `QObject`；通常由视图或控制器所在 GUI 线程拥有
- 数据范围：本地文件系统，不是虚拟资源系统或远程文件协议的统一模型

## 它解决的问题

文件浏览器需要同时处理层级、懒加载、系统图标、过滤、排序和外部变更。直接用 `QDir` 扫描只能得到一次性列表；`QFileSystemModel` 在后台收集目录内容，将结果通过模型信号送到所属线程，并借助文件系统监视器更新缓存。

常见用途包括：

- 文件对话框、目录树和资源浏览器；
- 文件路径补全模型；
- 选择工作目录或导入文件的只读列表；
- 允许重命名、拖放复制/移动、新建目录和永久删除的文件管理界面。

它不是文件操作事务层：写操作直接落到真实文件系统，没有撤销、回收站或批量原子提交。

## 基本使用

```cpp
auto *model = new QFileSystemModel(treeView);
model->setReadOnly(true);

const QString path = QDir::homePath();
const QModelIndex root = model->setRootPath(path);

treeView->setModel(model);
treeView->setRootIndex(root);
```

`setRootPath(path)` 启动该路径的扫描和监视，并返回对应索引，但**不会限制模型结构只剩该目录**。视图要从该位置开始显示，仍需调用 `QTreeView::setRootIndex()`。

模型在 `setRootPath()` 前不会主动枚举系统根目录。目录收集在工作线程完成，所以刚设置路径时 `rowCount()` 可能仍为 `0`；所属线程必须运行事件循环以接收结果。需要知道某目录何时完成首轮加载，连接 `directoryLoaded(path)`，不要同步轮询 `rowCount()`。

## 异步加载、索引与线程

后台 gatherer 避免阻塞 GUI，但 `QFileSystemModel` 本身仍是 `QObject`/模型，只应在其所属线程调用。不要因为内部扫描使用线程，就从工作线程直接查询 `data()`、`index()` 或修改过滤器。

目录加载和外部文件变化会插入、删除、移动模型行。短期槽函数中可使用普通 `QModelIndex`；需要跨事件循环保存时使用 `QPersistentModelIndex`，需要作为业务身份长期保存时优先保存规范化路径，并在使用前重新取得 `index(path)`。文件被删除或重命名后，即使持久索引也可能失效。

`index(path)` 依赖该路径已进入模型缓存。异步扫描尚未完成、路径被过滤或文件已不存在时，应准备接收无效索引。

## 过滤与名称过滤

`setFilter(QDir::Filters)` 决定哪些条目类型进入模型。默认值为：

```cpp
QDir::AllEntries | QDir::NoDotAndDotDot | QDir::AllDirs
```

自定义过滤器应保留 `QDir::AllDirs`，否则目录层级可能无法继续展开。`setNameFilters({"*.png", "*.jpg"})` 按名称模式筛选文件。

`nameFilterDisables` 默认为 `true`：不匹配名称过滤器的文件仍显示，但处于禁用状态；设为 `false` 时这些文件会隐藏。名称过滤与 `QDir::Filters` 是两层不同规则。

## 监视、符号链接与图标性能

默认情况下模型为已访问路径安装文件系统监视器，并自动更新缓存。对一次性路径补全、庞大目录树、网络盘或文件监视资源受限的场景，可在扫描前启用 `DontWatchForChanges`，代价是外部变化不会自动出现。

`DontUseCustomDirectoryIcons` 可避免网络盘和可移动设备上昂贵的自定义文件夹图标查询。`DontResolveSymlinks` 关闭符号链接解析；对应的 `resolveSymlinks` 属性在 Qt 6.11 文档中仅与 Windows 相关，默认开启。

这些 `Options` 默认全部关闭，并应在改变其他属性、尤其是设置根路径前配置。

## 只读与破坏性操作

`readOnly` 默认为 `true`。设为 `false` 后，模型才允许根据权限重命名、复制、拖放和删除；这不是安全沙箱，仍需自行限制允许操作的根路径、确认用户意图并处理竞态。

- `setData(index, newName, Qt::EditRole)` 可通过视图编辑触发重命名。
- `mkdir(parent, name)` 在对应目录创建子目录，失败返回无效索引。
- `remove(index)` 永久删除文件。
- `rmdir(index)` 永久删除目录，实际成功还受目录是否为空和平台权限限制。
- 删除 API **不会移入回收站**，也不提供撤销。

在真正执行前，不要仅凭旧的 `permissions(index)` 决策：文件权限和路径可能在检查后变化，最终以操作返回值为准。`QFileSystemModel` 没有通用 `errorString()`，需要面向用户说明失败原因时，业务层通常应使用更明确的文件 API 执行或补充检查。

## 列、角色与视图协作

标准树视图通常得到名称、大小、类型、最后修改时间等列。路径等机器数据应通过专用角色或便利函数取得，不要解析 `Qt::DisplayRole` 的本地化文本。

| 角色 | 内容 |
| --- | --- |
| `FileIconRole` / `Qt::DecorationRole` | 系统文件图标 |
| `FilePathRole` | 完整路径 |
| `FileNameRole` | 文件名 |
| `FilePermissions` | `QFile::Permissions` 标志 |
| `FileInfoRole` / `Qt::FileInfoRole` | 完整 `QFileInfo` 值 |

Qt 6 与 Qt 7 对部分自定义角色的具体整数值不同，外部代码必须使用枚举名或 `roleNames()`，不要持久化裸角色数字。

## API 速查表

### 根路径、加载和信号

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `QFileSystemModel(QObject *parent = nullptr)` | 创建空模型。 | 在 `setRootPath()` 前不会开始填充；可由 parent 管理生命周期。 |
| `setRootPath(newPath)` | 开始扫描/监视路径并返回其模型索引。 | 不限制模型对视图的可见根；扫描异步。 |
| `rootPath()` / `rootDirectory()` | 返回当前配置的根路径或 `QDir`。 | 表示监视/填充入口，不等于视图 root index。 |
| `rootPathChanged(newPath)` | 根路径配置变化时发出。 | 不表示目录已经加载完成。 |
| `directoryLoaded(path)` | gatherer 完成某目录加载时发出。 | 异步就绪通知；目录之后仍可能因外部变更更新。 |
| `fileRenamed(path, oldName, newName)` | 模型成功重命名文件时发出。 | `path` 是所在目录，不是旧文件完整路径。 |

### 路径、文件信息与索引

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `index(path, column = 0)` | 按文件系统路径取得索引。 | 尚未加载、被过滤或不存在时可能无效。 |
| `filePath(index)` | 返回条目的完整路径。 | 无效索引应先检查。 |
| `fileName(index)` | 返回条目名称。 | 通过 `FileNameRole` 获取。 |
| `fileInfo(index)` | 返回该条目的 `QFileInfo` 快照。 | 外部文件之后可变化，长期使用前需刷新。 |
| `fileIcon(index)` | 返回系统/自定义图标。 | 图标查询在网络盘可能昂贵。 |
| `isDir(index)` | 判断条目是否目录。 | 结果基于模型缓存。 |
| `size(index)` | 返回字节数。 | 文件不存在时返回 `0`，不能据此区分空文件与缺失文件。 |
| `type(index)` | 返回本地化/平台相关类型文本。 | 适合显示，不适合作为业务类型标识。 |
| `lastModified(index)` | 返回本地时区的最后修改时间。 | 无效索引返回无效的默认 `QDateTime`。 |
| `lastModified(index, timeZone)` | 在指定时区返回修改时间。 | Qt 6.6；读取 UTC 可避免本地时区转换成本。 |
| `permissions(index)` | 返回权限标志组合。 | 是检查时快照；最终操作仍可能因竞态失败。 |
| `myComputer(role)` | 返回平台“计算机”根项的角色数据。 | 平台相关，不应硬编码显示文本。 |

### 过滤、选项与图标提供者

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `filter()` / `setFilter(filters)` | 获取/设置 `QDir` 条目过滤。 | 自定义时保留 `QDir::AllDirs` 以维持层级遍历。 |
| `nameFilters()` / `setNameFilters(patterns)` | 获取/设置名称通配模式。 | 如 `"*.cpp"`；与条目类型过滤分开。 |
| `nameFilterDisables()` / `setNameFilterDisables(on)` | 控制不匹配项禁用还是隐藏。 | 默认 `true`：显示但禁用；`false`：隐藏。 |
| `options()` / `setOptions(options)` | 整体获取/替换性能与解析选项。 | 默认无标志；应在其他属性前设置。 |
| `setOption(option, on)` / `testOption(option)` | 单独设置或查询某标志。 | 适合增量配置。 |
| `resolveSymlinks()` / `setResolveSymlinks(on)` | 控制符号链接解析。 | Qt 6.11 文档称仅与 Windows 相关；默认 `true`。 |
| `iconProvider()` / `setIconProvider(provider)` | 获取/替换文件图标提供者。 | 提供者必须在模型使用期间有效；更换后注意缓存与性能。 |

### 写操作

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `isReadOnly()` / `setReadOnly(on)` | 查询/控制是否禁止模型写文件系统。 | 默认只读；关闭只读不绕过系统权限。 |
| `setData(index, value, Qt::EditRole)` | 编辑名称并尝试重命名。 | 失败返回 `false`；只读模式或权限不足不会成功。 |
| `mkdir(parent, name)` | 创建子目录并返回其索引。 | 失败返回无效索引。 |
| `remove(index)` | 删除对应文件。 | 永久删除，不进入回收站；失败返回 `false`。 |
| `rmdir(index)` | 删除对应目录。 | 永久删除；非空目录或权限受限时通常失败。 |
| `mimeData(indexes)` / `mimeTypes()` | 为拖动导出文件 MIME 数据。 | 返回的 `QMimeData *` 按模型/视图 API 约定由调用方接管。 |
| `dropMimeData(data, action, row, column, parent)` | 在目标目录执行拖放操作。 | 会产生真实复制/移动；必须检查返回值和只读状态。 |
| `supportedDropActions()` | 返回模型支持的拖放动作。 | 视图还需启用 drag/drop，并受文件权限限制。 |

### 模型接口

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `index(row, column, parent)` / `parent(index)` / `sibling(...)` | 导航层级索引。 | 外部变化后不要长期保存普通 `QModelIndex`。 |
| `rowCount(parent)` / `columnCount(parent)` | 返回当前已加载的行列数。 | 异步填充前目录行数可能为 `0`。 |
| `hasChildren(parent)` | 判断是否可能有子项。 | 可能在内容尚未抓取时为真。 |
| `canFetchMore(parent)` / `fetchMore(parent)` | 支持模型按需继续填充目录。 | 通常由视图自动调用。 |
| `data(index, role)` / `roleNames()` | 读取显示或专用角色数据。 | 使用角色名，不依赖 Qt 6 的裸整数值。 |
| `headerData(section, orientation, role)` | 返回列标题等表头数据。 | 显示文本可能本地化。 |
| `flags(index)` | 返回可选、可编辑、可拖放等条目标志。 | 受只读、过滤和权限影响。 |
| `sort(column, order)` | 按列排序当前模型。 | 异步插入的新条目仍会按当前排序进入。 |
| `event(event)` / `timerEvent(event)` | 内部事件与批量更新处理钩子。 | 受保护重写；派生类覆盖时应保留基类处理。 |

### Options 枚举

| 标志 | 含义 |
| --- | --- |
| `DontWatchForChanges` | 不安装文件监视器，降低补全等一次性用途的开销，但不自动同步外部变化。 |
| `DontResolveSymlinks` | 不解析符号链接。 |
| `DontUseCustomDirectoryIcons` | 始终使用默认目录图标，避免网络盘/移动盘上的昂贵查询。 |

## 易错点

1. 只调用 `setRootPath()`，却没有给视图设置 `setRootIndex()`。
2. 设置根路径后立刻断言 `rowCount() > 0`，忽略异步加载。
3. 把模型移动到没有事件循环的线程，导致 gatherer 结果无法送达。
4. 自定义 `QDir::Filters` 时漏掉 `QDir::AllDirs`，目录树无法展开。
5. 将 `nameFilterDisables(false)` 理解为“禁用不匹配项”；它实际会隐藏不匹配项。
6. 调用 `remove()` / `rmdir()` 时以为文件会进入回收站。
7. 长期保存普通 `QModelIndex`，忽略外部重命名和删除。
8. 持久化 `FilePathRole` 的整数值，跨 Qt 6/Qt 7 后角色发生变化。
