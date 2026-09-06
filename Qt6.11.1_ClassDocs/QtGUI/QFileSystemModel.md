# QFileSystemModel

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QFileSystemModel` 是 模型/视图协议 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QFileSystemModel` 是模型/视图体系中的数据模型类型，向视图提供索引、角色数据和结构变化通知。

**内部模型：** 视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

**适用场景：** 需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。

**典型调用链：** 准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

**先记住的坑：** 不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

## 2. 依赖与对象关系

- 头文件：`#include <QFileSystemModel>`
- 继承自：QAbstractItemModel
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

### 状态、生命周期和线程

**生命周期：** 模型应比视图活得足够久，视图销毁时不会自动替业务容器释放资源。模型变化必须使用对应的 begin/end 协议或精确通知，不能只改容器后期待视图自行发现。取到的 QModelIndex 只在模型允许的生命周期内有效。

**状态与结果：** 区分当前索引、选择模型、编辑状态、数据角色和模型结构变化。`dataChanged` 表示已有项目的数据变化，行列插入/删除表示结构变化，`modelReset` 会让旧索引整体失效。

**线程与事件循环：** 模型通常在 GUI 线程被视图访问。后台线程不要直接修改正在显示的模型；应在正确线程汇总数据，再通过通知协议更新，或使用线程安全的数据交换层。

## 3. 直接使用

需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。 使用时通常按这个过程组织：准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

```cpp
// 视图通过 QModelIndex 和 role 查询模型。
const QVariant value = model->data(index, Qt::DisplayRole);
// 数据变化时由模型发出 dataChanged 或 begin/end 结构通知。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Option { DontWatchForChanges, DontResolveSymlinks, DontUseCustomDirectoryIcons }`
- `flags Options`
- `enum Roles { FileIconRole, FilePathRole, FileNameRole, FilePermissions, FileInfoRole }`

### 属性

- `nameFilterDisables : bool`
- `options : Options`
- `readOnly : bool`
- `resolveSymlinks : bool`

### 公有函数

- `QFileSystemModel(QObject *parent = nullptr)`
- `virtual ~QFileSystemModel()`
- `QIcon fileIcon(const QModelIndex &index) const`
- `QFileInfo fileInfo(const QModelIndex &index) const`
- `QString fileName(const QModelIndex &index) const`
- `QString filePath(const QModelIndex &index) const`
- `QDir::Filters filter() const`
- `QAbstractFileIconProvider * iconProvider() const`
- `QModelIndex index(const QString &path, int column = 0) const`
- `bool isDir(const QModelIndex &index) const`
- `bool isReadOnly() const`
- `QDateTime lastModified(const QModelIndex &index) const`
- `(since 6.6) QDateTime lastModified(const QModelIndex &index, const QTimeZone &tz) const`
- `QModelIndex mkdir(const QModelIndex &parent, const QString &name)`
- `QVariant myComputer(int role = Qt::DisplayRole) const`
- `bool nameFilterDisables() const`
- `QStringList nameFilters() const`
- `QFileSystemModel::Options options() const`
- `QFileDevice::Permissions permissions(const QModelIndex &index) const`
- `bool remove(const QModelIndex &index)`
- `bool resolveSymlinks() const`
- `bool rmdir(const QModelIndex &index)`
- `QDir rootDirectory() const`
- `QString rootPath() const`
- `void setFilter(QDir::Filters filters)`
- `void setIconProvider(QAbstractFileIconProvider *provider)`
- `void setNameFilterDisables(bool enable)`
- `void setNameFilters(const QStringList &filters)`
- `void setOption(QFileSystemModel::Option option, bool on = true)`
- `void setOptions(QFileSystemModel::Options options)`
- `void setReadOnly(bool enable)`
- `void setResolveSymlinks(bool enable)`
- `QModelIndex setRootPath(const QString &newPath)`
- `qint64 size(const QModelIndex &index) const`
- `bool testOption(QFileSystemModel::Option option) const`
- `QString type(const QModelIndex &index) const`

### 重实现的公有函数

- `virtual bool canFetchMore(const QModelIndex &parent) const override`
- `virtual int columnCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override`
- `virtual bool dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) override`
- `virtual void fetchMore(const QModelIndex &parent) override`
- `virtual Qt::ItemFlags flags(const QModelIndex &index) const override`
- `virtual bool hasChildren(const QModelIndex &parent = QModelIndex()) const override`
- `virtual QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override`
- `virtual QModelIndex index(int row, int column, const QModelIndex &parent = QModelIndex()) const override`
- `virtual QMimeData * mimeData(const QModelIndexList &indexes) const override`
- `virtual QStringList mimeTypes() const override`
- `virtual QModelIndex parent(const QModelIndex &index) const override`
- `virtual QHash<int, QByteArray> roleNames() const override`
- `virtual int rowCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual bool setData(const QModelIndex &idx, const QVariant &value, int role = Qt::EditRole) override`
- `virtual QModelIndex sibling(int row, int column, const QModelIndex &idx) const override`
- `virtual void sort(int column, Qt::SortOrder order = Qt::AscendingOrder) override`
- `virtual Qt::DropActions supportedDropActions() const override`

### 信号

- `void directoryLoaded(const QString &path)`
- `void fileRenamed(const QString &path, const QString &oldName, const QString &newName)`
- `void rootPathChanged(const QString &newPath)`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`
- `virtual void timerEvent(QTimerEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QFileSystemModel::Optionflags QFileSystemModel::Options`

**作用与语义：**

- `QFileSystemModel::DontWatchForChanges`：`0x00000001`;不要在路径中添加文件观察器。这样可以减少模型在执行简单任务如行编辑完成时的开销。
- `QFileSystemModel::DontResolveSymlinks`：`0x00000002`;文件系统模型中不解析符号链接。默认情况下，符号链接已被解析。
- `QFileSystemModel::DontUseCustomDirectoryIcons`：`0x00000004`;始终使用默认目录图标。部分平台允许用户设置不同的图标。自定义图标查找会在网络或可移动驱动器上造成较大的性能影响。这会相应地在图标提供者中设置QFileIconProvider：:D ontUseCustomDirectoryIcons选项。
Options 类型是 QFlags 的 typedef<Option>。它存储 Option 值的 OR 组合。

### `nameFilterDisables : bool`

**作用与语义：**

该属性决定了未通过名称过滤器的文件是隐藏还是禁用。
该属性默认`true`。

**如何使用：** 调用 `nameFilterDisables()` 读取当前值；它不会修改应用状态。

### `options : Options`

**作用与语义：**

该属性包含影响模型的各种选项。
默认情况下，所有选项都是被禁用的。
在更改属性之前，应该先设置好选项。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `readOnly : bool`

**作用与语义：**

该属性是否允许目录模型写入文件系统。
如果该属性设置为 false，目录模型将允许重命名、复制和删除文件和目录。
该属性默认`true`。

**如何使用：** 调用 `readOnly()` 读取当前值；它不会修改应用状态。

### `resolveSymlinks : bool`

**作用与语义：**

该属性决定了目录模型是否应解析符号链接。
这只有在Windows上才适用。
默认情况下，该属性为`true`。

**如何使用：** 调用 `resolveSymlinks()` 读取当前值；它不会修改应用状态。

### `[explicit] QFileSystemModel::QFileSystemModel(QObject *parent = nullptr)`

**作用与语义：**

基于给定`parent`构建文件系统模型。

### `[virtual noexcept] QFileSystemModel::~QFileSystemModel()`

**作用与语义：**

破坏了这个文件系统模型。

### `[override virtual] bool QFileSystemModel::canFetchMore(const QModelIndex &parent) const`

**作用与语义：**

重实现自：Const QModelIndex 和 parent const. `QAbstractItemModel::canFetchMore`（const QModelIndex & parent） const.

### `[override virtual] int QFileSystemModel::columnCount(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::columnCount`（const QModelIndex &parent） const.

### `[override virtual] QVariant QFileSystemModel::data(const QModelIndex &index, int role = Qt::DisplayRole) const`

**作用与语义：**

重实现自：`QAbstractItemModel::data`（const QModelIndex & index， int role） const.

### `[signal] void QFileSystemModel::directoryLoaded(const QString &path)`

**作用与语义：**

当收集线程完成加载`path`时，该信号会发出。

### `[override virtual] bool QFileSystemModel::dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)`

**作用与语义：**

重实现自：`QAbstractItemModel::dropMimeData`（const QMimeData *data， Qt：:D ropAction action， int row， int column， const QModelIndex & parent）.
处理拖放操作提供的`data`，该操作以模型中由`row`、`column`及`parent`索引指定的行的给定`action`结束。如果操作成功，则返回真值。

### `[override virtual protected] bool QFileSystemModel::event(QEvent *event)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。

### `[override virtual] void QFileSystemModel::fetchMore(const QModelIndex &parent)`

**作用与语义：**

重装：`QAbstractItemModel::fetchMore`（const QModelIndex & parent）。

### `QIcon QFileSystemModel::fileIcon(const QModelIndex &index) const`

**作用与语义：**

返回模型中存放物品的图标，显示在给定`index`下。

### `QFileInfo QFileSystemModel::fileInfo(const QModelIndex &index) const`

**作用与语义：**

返回模型中在给定`index`下存储的物品的 `QFileInfo`。

### `QString QFileSystemModel::fileName(const QModelIndex &index) const`

**作用与语义：**

返回模型中所存物品的文件名，该项目在给定`index`下。

### `QString QFileSystemModel::filePath(const QModelIndex &index) const`

**作用与语义：**

返回模型中存储物品的路径，`index`给出。

### `[signal] void QFileSystemModel::fileRenamed(const QString &path, const QString &oldName, const QString &newName)`

**作用与语义：**

每当带有`oldName`的文件成功重命名为`newName`时，都会发出该信号。该文件位于目录`path`中。

### `QDir::Filters QFileSystemModel::filter() const`

**作用与语义：**

返回目录模型指定的过滤器。
如果尚未设置过滤器，默认过滤器为`QDir::AllEntries` |`QDir::NoDotAndDotDot` |`QDir::AllDirs`。

### `[override virtual] Qt::ItemFlags QFileSystemModel::flags(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::flags`（const QModelIndex & index） const.

### `[override virtual] bool QFileSystemModel::hasChildren(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::hasChildren`（const QModelIndex & parent）const.

### `[override virtual] QVariant QFileSystemModel::headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const`

**作用与语义：**

重实现自：`QAbstractItemModel::headerData`（int section，Qt：：Orientation orientation， int role）const.

### `QAbstractFileIconProvider *QFileSystemModel::iconProvider() const`

**作用与语义：**

返回该目录模型的文件图标提供者。

### `[override virtual] QModelIndex QFileSystemModel::index(int row, int column, const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::index`（整数行，整数列，条件 QModelIndex 和父）const.

### `QModelIndex QFileSystemModel::index(const QString &path, int column = 0) const`

**作用与语义：**

返回给定`path`和`column`的模型项索引。

### `bool QFileSystemModel::isDir(const QModelIndex &index) const`

**作用与语义：**

如果模型项目`index`代表目录，返回`true`;否则返回`false`。

### `QDateTime QFileSystemModel::lastModified(const QModelIndex &index) const`

**作用与语义：**

返回`index`最后修改的日期和时间（当地时间）。
这是一个重载函数，等价于调用：
如果`index`无效，则返回默认构造`QDateTime`。

**官方示例：**

```cpp
 lastModified(index, QTimeZone::LocalTime);
```

### `[since 6.6] QDateTime QFileSystemModel::lastModified(const QModelIndex &index, const QTimeZone &tz) const`

**作用与语义：**

返回`tz`时区的日期和时间，`index`最后修改的时间。
`tz`的典型论据是`QTimeZone::UTC`或`QTimeZone::LocalTime`。UTC不需要从本地文件系统API返回的时间进行转换，因此以UTC获取时间可能更快。通常选择本地时间，前提是时间会显示给用户。
如果`index`无效，则返回默认构造`QDateTime`。

### `[override virtual] QMimeData *QFileSystemModel::mimeData(const QModelIndexList &indexes) const`

**作用与语义：**

重实现自：`QAbstractItemModel::mimeData`（const QModelIndexList & indexes） const.
返回一个包含指定`indexes`序列化描述的对象。描述对应索引的项目的格式来自`mimeTypes()`函数。
如果索引列表为空，则返回`nullptr`而非序列化的空列表。

### `[override virtual] QStringList QFileSystemModel::mimeTypes() const`

**作用与语义：**

重装：`QAbstractItemModel::mimeTypes()` const.
返回一个MIME类型列表，可用于描述模型中的项目列表。

### `QModelIndex QFileSystemModel::mkdir(const QModelIndex &parent, const QString &name)`

**作用与语义：**

创建一个目录，`parent`模型索引中包含`name`。

### `QVariant QFileSystemModel::myComputer(int role = Qt::DisplayRole) const`

**作用与语义：**

返回“我的电脑”项目指定`role`下存储的数据。

### `QStringList QFileSystemModel::nameFilters() const`

**作用与语义：**

返回对模型名称应用的过滤器列表。

### `[override virtual] QModelIndex QFileSystemModel::parent(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::parent`（const QModelIndex & index） const.

### `QFileDevice::Permissions QFileSystemModel::permissions(const QModelIndex &index) const`

**作用与语义：**

返回`index`的QFile：:P发射的完整OR-ED组合。

### `bool QFileSystemModel::remove(const QModelIndex &index)`

**作用与语义：**

从文件系统模型中移除模型项`index`，并从文件系统中删除对应文件，成功时返回true。如果无法移除该项，则返回false。
警告：该函数会从文件系统中删除文件;它不会将它们移动到可以恢复的位置。

### `bool QFileSystemModel::rmdir(const QModelIndex &index)`

**作用与语义：**

删除文件系统模型`index`中对应模型项的目录，并从文件系统中删除对应目录，成功时返回 true。如果无法移除该目录，则返回 false。
警告：该函数会从文件系统中删除目录;但它不会将它们移动到可恢复的位置。

### `[override virtual] QHash<int, QByteArray> QFileSystemModel::roleNames() const`

**作用与语义：**

重实现自：`QAbstractItemModel::roleNames()` const.

### `QDir QFileSystemModel::rootDirectory() const`

**作用与语义：**

当前设置的目录。

### `QString QFileSystemModel::rootPath() const`

**作用与语义：**

当前设置的根路径。

### `[signal] void QFileSystemModel::rootPathChanged(const QString &newPath)`

**作用与语义：**

每当根路径被改为`newPath`时，该信号都会发出。

### `[override virtual] int QFileSystemModel::rowCount(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：Const QModelIndex 和 parent const. `QAbstractItemModel::rowCount`（const QModelIndex & parent） const.

### `[override virtual] bool QFileSystemModel::setData(const QModelIndex &idx, const QVariant &value, int role = Qt::EditRole)`

**作用与语义：**

重实现自：`QAbstractItemModel::setData`（const QModelIndex & index，const QVariant & value，int role）。

### `void QFileSystemModel::setFilter(QDir::Filters filters)`

**作用与语义：**

将目录模型的过滤器设置为`filters`指定的内容。
注意你设置的过滤器应始终包含`QDir::AllDirs`枚举值，否则`QFileSystemModel`无法读取目录结构。

### `void QFileSystemModel::setIconProvider(QAbstractFileIconProvider *provider)`

**作用与语义：**

设置目录模型的文件图标`provider`。

### `void QFileSystemModel::setNameFilters(const QStringList &filters)`

**作用与语义：**

设置名称 `filters` 以应用到现有文件中。

### `void QFileSystemModel::setOption(QFileSystemModel::Option option, bool on = true)`

**作用与语义：**

将给定`option`设置为启用，`on`为真;否则，清除给定`option`。
在更改属性之前，应该先设置好选项。

### `QModelIndex QFileSystemModel::setRootPath(const QString &newPath)`

**作用与语义：**

通过安装文件系统监视器，将模型监控的目录设置为`newPath`。该目录中文件和目录的任何更改都会反映在模型中。
如果路径发生变化，`rootPathChanged()`信号就会被发射。
注意：该函数不会改变模型结构或修改视图可用的数据。换句话说，模型的“根”不会只包含文件系统中`newPath`指定的目录中的文件和目录。

### `[override virtual] QModelIndex QFileSystemModel::sibling(int row, int column, const QModelIndex &idx) const`

**作用与语义：**

重实现自：`QAbstractItemModel::sibling`（整数行，整数列，const QModelIndex & index）const.

### `qint64 QFileSystemModel::size(const QModelIndex &index) const`

**作用与语义：**

返回以字节为单位的`index`大小。如果文件不存在，则返回0。

### `[override virtual] void QFileSystemModel::sort(int column, Qt::SortOrder order = Qt::AscendingOrder)`

**作用与语义：**

重实现自：`QAbstractItemModel::sort`（整数列，Qt：：SortOrder order）。

### `[override virtual] Qt::DropActions QFileSystemModel::supportedDropActions() const`

**作用与语义：**

重装：`QAbstractItemModel::supportedDropActions()` const.

### `bool QFileSystemModel::testOption(QFileSystemModel::Option option) const`

**作用与语义：**

如果启用给定`option`，返回 `true`;否则返回 false。

### `[override virtual protected] void QFileSystemModel::timerEvent(QTimerEvent *event)`

**作用与语义：**

重实现自：`QObject::timerEvent`（QTimerEvent *event）。

### `QString QFileSystemModel::type(const QModelIndex &index) const`

**作用与语义：**

返回文件类型`index`如“目录”或“JPEG文件”。

### `enum Option { DontWatchForChanges, DontResolveSymlinks, DontUseCustomDirectoryIcons }`

**作用与语义：**

- `QFileSystemModel::DontWatchForChanges`：`0x00000001`;不要在路径中添加文件观察器。这样可以减少模型在执行简单任务如行编辑完成时的开销。
- `QFileSystemModel::DontResolveSymlinks`：`0x00000002`;文件系统模型中不解析符号链接。默认情况下，符号链接已被解析。
- `QFileSystemModel::DontUseCustomDirectoryIcons`：`0x00000004`;始终使用默认目录图标。部分平台允许用户设置不同的图标。自定义图标查找会在网络或可移动驱动器上造成较大的性能影响。这会相应地在图标提供者中设置QFileIconProvider：:D ontUseCustomDirectoryIcons选项。
Options 类型是 QFlags 的 typedef<Option>。它存储 Option 值的 OR 组合。

### `flags Options`

**作用与语义：**

- `QFileSystemModel::DontWatchForChanges`：`0x00000001`;不要在路径中添加文件观察器。这样可以减少模型在执行简单任务如行编辑完成时的开销。
- `QFileSystemModel::DontResolveSymlinks`：`0x00000002`;文件系统模型中不解析符号链接。默认情况下，符号链接已被解析。
- `QFileSystemModel::DontUseCustomDirectoryIcons`：`0x00000004`;始终使用默认目录图标。部分平台允许用户设置不同的图标。自定义图标查找会在网络或可移动驱动器上造成较大的性能影响。这会相应地在图标提供者中设置QFileIconProvider：:D ontUseCustomDirectoryIcons选项。
Options 类型是 QFlags 的 typedef<Option>。它存储 Option 值的 OR 组合。

### `enum Roles { FileIconRole, FilePathRole, FileNameRole, FilePermissions, FileInfoRole }`

**作用与语义：**

- `QFileSystemModel::FileIconRole`：`Qt::DecorationRole`
- `QFileSystemModel::FilePathRole`：`Qt::UserRole + 1`
- `QFileSystemModel::FileNameRole`：`Qt::UserRole + 2`
- `QFileSystemModel::FilePermissions`：`Qt::UserRole + 3`
- `QFileSystemModel::FileInfoRole`：`Qt::FileInfoRole`;索引的`QFileInfo`对象

### `bool isReadOnly() const`

**作用与语义：**

该属性是否允许目录模型写入文件系统。
如果该属性设置为 false，目录模型将允许重命名、复制和删除文件和目录。
该属性默认`true`。

**如何使用：** 调用 `isReadOnly()` 读取当前值；它不会修改应用状态。

### `bool nameFilterDisables() const`

**作用与语义：**

该属性决定了未通过名称过滤器的文件是隐藏还是禁用。
该属性默认`true`。

**如何使用：** 调用 `nameFilterDisables()` 读取当前值；它不会修改应用状态。

### `QFileSystemModel::Options options() const`

**作用与语义：**

该属性包含影响模型的各种选项。
默认情况下，所有选项都是被禁用的。
在更改属性之前，应该先设置好选项。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `bool resolveSymlinks() const`

**作用与语义：**

该属性决定了目录模型是否应解析符号链接。
这只有在Windows上才适用。
默认情况下，该属性为`true`。

**如何使用：** 调用 `resolveSymlinks()` 读取当前值；它不会修改应用状态。

### `void setNameFilterDisables(bool enable)`

**作用与语义：**

该属性决定了未通过名称过滤器的文件是隐藏还是禁用。
该属性默认`true`。

**如何使用：** 调用 `setNameFilterDisables(...)` 修改 `nameFilterDisables`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOptions(QFileSystemModel::Options options)`

**作用与语义：**

该属性包含影响模型的各种选项。
默认情况下，所有选项都是被禁用的。
在更改属性之前，应该先设置好选项。

**如何使用：** 调用 `setOptions(...)` 修改 `options`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setReadOnly(bool enable)`

**作用与语义：**

该属性是否允许目录模型写入文件系统。
如果该属性设置为 false，目录模型将允许重命名、复制和删除文件和目录。
该属性默认`true`。

**如何使用：** 调用 `setReadOnly(...)` 修改 `readOnly`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setResolveSymlinks(bool enable)`

**作用与语义：**

该属性决定了目录模型是否应解析符号链接。
这只有在Windows上才适用。
默认情况下，该属性为`true`。

**如何使用：** 调用 `setResolveSymlinks(...)` 修改 `resolveSymlinks`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

模型应比视图活得足够久，视图销毁时不会自动替业务容器释放资源。模型变化必须使用对应的 begin/end 协议或精确通知，不能只改容器后期待视图自行发现。取到的 QModelIndex 只在模型允许的生命周期内有效。

### 状态和错误边界

区分当前索引、选择模型、编辑状态、数据角色和模型结构变化。`dataChanged` 表示已有项目的数据变化，行列插入/删除表示结构变化，`modelReset` 会让旧索引整体失效。

### 线程边界

模型通常在 GUI 线程被视图访问。后台线程不要直接修改正在显示的模型；应在正确线程汇总数据，再通过通知协议更新，或使用线程安全的数据交换层。

### 最容易出现的错误

不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QFileSystemModel` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
