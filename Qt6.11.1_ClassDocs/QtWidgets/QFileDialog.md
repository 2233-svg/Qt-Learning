# QFileDialog

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QFileDialog` 是 文件、设备与流机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QFileDialog` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QFileDialog>`
- 继承自：QDialog
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 先设置路径或设备，再 open，成功后读写/定位/刷新，最后 close；析构通常会关闭设备，但关键写入应显式 flush/close 并检查错误。相对路径依赖当前工作目录，资源路径和用户文件路径要区分。

**状态与结果：** 区分设备未打开、打开成功、到达 EOF、暂时无数据、读写失败和写入尚未落盘。`readAll()` 方便小数据但可能占用大量内存，大文件应分块处理并检查返回值。

**线程与事件循环：** 同一个打开设备不要跨线程并发使用，除非类明确保证线程安全；后台 I/O 通过 worker 或异步设备处理，GUI 线程只接收结果。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

```cpp
QFile file(path);
if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    const QByteArray data = file.readAll();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum AcceptMode { AcceptOpen, AcceptSave }`
- `enum DialogLabel { LookIn, FileName, FileType, Accept, Reject }`
- `enum FileMode { AnyFile, ExistingFile, Directory, ExistingFiles }`
- `enum Option { ShowDirsOnly, DontResolveSymlinks, DontConfirmOverwrite, DontUseNativeDialog, ReadOnly, …, DontUseCustomDirectoryIcons }`
- `flags Options`
- `enum ViewMode { Detail, List }`

### 属性

- `acceptMode : AcceptMode`
- `defaultSuffix : QString`
- `fileMode : FileMode`
- `options : Options`
- `supportedSchemes : QStringList`
- `viewMode : ViewMode`

### 公有函数

- `QFileDialog(QWidget *parent, Qt::WindowFlags flags)`
- `QFileDialog(QWidget *parent = nullptr, const QString &caption = QString(), const QString &directory = QString(), const QString &filter = QString())`
- `virtual ~QFileDialog()`
- `QFileDialog::AcceptMode acceptMode() const`
- `QString defaultSuffix() const`
- `QDir directory() const`
- `QUrl directoryUrl() const`
- `QFileDialog::FileMode fileMode() const`
- `QDir::Filters filter() const`
- `QStringList history() const`
- `QAbstractFileIconProvider * iconProvider() const`
- `QAbstractItemDelegate * itemDelegate() const`
- `QString labelText(QFileDialog::DialogLabel label) const`
- `QStringList mimeTypeFilters() const`
- `QStringList nameFilters() const`
- `void open(QObject *receiver, const char *member)`
- `QFileDialog::Options options() const`
- `QAbstractProxyModel * proxyModel() const`
- `bool restoreState(const QByteArray &state)`
- `QByteArray saveState() const`
- `void selectFile(const QString &filename)`
- `void selectMimeTypeFilter(const QString &filter)`
- `void selectNameFilter(const QString &filter)`
- `void selectUrl(const QUrl &url)`
- `QStringList selectedFiles() const`
- `QString selectedMimeTypeFilter() const`
- `QString selectedNameFilter() const`
- `QList<QUrl> selectedUrls() const`
- `void setAcceptMode(QFileDialog::AcceptMode mode)`
- `void setDefaultSuffix(const QString &suffix)`
- `void setDirectory(const QString &directory)`
- `void setDirectory(const QDir &directory)`
- `void setDirectoryUrl(const QUrl &directory)`
- `void setFileMode(QFileDialog::FileMode mode)`
- `void setFilter(QDir::Filters filters)`
- `void setHistory(const QStringList &paths)`
- `void setIconProvider(QAbstractFileIconProvider *provider)`
- `void setItemDelegate(QAbstractItemDelegate *delegate)`
- `void setLabelText(QFileDialog::DialogLabel label, const QString &text)`
- `void setMimeTypeFilters(const QStringList &filters)`
- `void setNameFilter(const QString &filter)`
- `void setNameFilters(const QStringList &filters)`
- `void setOption(QFileDialog::Option option, bool on = true)`
- `void setOptions(QFileDialog::Options options)`
- `void setProxyModel(QAbstractProxyModel *proxyModel)`
- `void setSidebarUrls(const QList<QUrl> &urls)`
- `void setSupportedSchemes(const QStringList &schemes)`
- `void setViewMode(QFileDialog::ViewMode mode)`
- `QList<QUrl> sidebarUrls() const`
- `QStringList supportedSchemes() const`
- `bool testOption(QFileDialog::Option option) const`
- `QFileDialog::ViewMode viewMode() const`

### 重实现的公有函数

- `virtual void setVisible(bool visible) override`

### 信号

- `void currentChanged(const QString &path)`
- `void currentUrlChanged(const QUrl &url)`
- `void directoryEntered(const QString &directory)`
- `void directoryUrlEntered(const QUrl &directory)`
- `void fileSelected(const QString &file)`
- `void filesSelected(const QStringList &selected)`
- `void filterSelected(const QString &filter)`
- `void urlSelected(const QUrl &url)`
- `void urlsSelected(const QList<QUrl> &urls)`

### 静态公有成员

- `QString getExistingDirectory(QWidget *parent = nullptr, const QString &caption = QString(), const QString &dir = QString(), QFileDialog::Options options = ShowDirsOnly)`
- `QUrl getExistingDirectoryUrl(QWidget *parent = nullptr, const QString &caption = QString(), const QUrl &dir = QUrl(), QFileDialog::Options options = ShowDirsOnly, const QStringList &supportedSchemes = QStringList())`
- `void getOpenFileContent(const QString &nameFilter, const std::function<void (const QString &, const QByteArray &)> &fileOpenCompleted, QWidget *parent = nullptr)`
- `QString getOpenFileName(QWidget *parent = nullptr, const QString &caption = QString(), const QString &dir = QString(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options())`
- `QStringList getOpenFileNames(QWidget *parent = nullptr, const QString &caption = QString(), const QString &dir = QString(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options())`
- `QUrl getOpenFileUrl(QWidget *parent = nullptr, const QString &caption = QString(), const QUrl &dir = QUrl(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options(), const QStringList &supportedSchemes = QStringList())`
- `QList<QUrl> getOpenFileUrls(QWidget *parent = nullptr, const QString &caption = QString(), const QUrl &dir = QUrl(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options(), const QStringList &supportedSchemes = QStringList())`
- `QString getSaveFileName(QWidget *parent = nullptr, const QString &caption = QString(), const QString &dir = QString(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options())`
- `QUrl getSaveFileUrl(QWidget *parent = nullptr, const QString &caption = QString(), const QUrl &dir = QUrl(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options(), const QStringList &supportedSchemes = QStringList())`
- `void saveFileContent(const QByteArray &fileContent, const QString &fileNameHint, QWidget *parent = nullptr)`

### 重实现的保护函数

- `virtual void accept() override`
- `virtual void changeEvent(QEvent *e) override`
- `virtual void done(int result) override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 88 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QFileDialog::FileMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QFileDialog` 暴露的类型声明 `File、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:FileMode`。
- 属性名：`QFileDialog`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QFileDialog::Optionflags QFileDialog::Options`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QFileDialog` 暴露的类型声明 `Optionflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Optionflags QFileDialog::Options`。
- 属性名：`QFileDialog`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QFileDialog::ViewMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QFileDialog` 暴露的类型声明 `View、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ViewMode`。
- 属性名：`QFileDialog`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `acceptMode : AcceptMode`

**API 类别：** 属性说明

**中文解读：** 这是 `QFileDialog` 的配置属性。初始化或状态切换时通过 `setAcceptMode(...)` 设置，之后用 `acceptMode()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`AcceptMode`。
- 属性名：`acceptMode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `defaultSuffix : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QFileDialog` 的配置属性。初始化或状态切换时通过 `setDefaultSuffix(...)` 设置，之后用 `defaultSuffix()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`defaultSuffix`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `fileMode : FileMode`

**API 类别：** 属性说明

**中文解读：** 这是 `QFileDialog` 的配置属性。初始化或状态切换时通过 `setFileMode(...)` 设置，之后用 `fileMode()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`FileMode`。
- 属性名：`fileMode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `options : Options`

**API 类别：** 属性说明

**中文解读：** 这是 `QFileDialog` 的配置属性。初始化或状态切换时通过 `setOptions(...)` 设置，之后用 `options()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Options`。
- 属性名：`options`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `supportedSchemes : QStringList`

**API 类别：** 属性说明

**中文解读：** 这是 `QFileDialog` 的配置属性。初始化或状态切换时通过 `setSupportedSchemes(...)` 设置，之后用 `supportedSchemes()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QStringList`。
- 属性名：`supportedSchemes`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `viewMode : ViewMode`

**API 类别：** 属性说明

**中文解读：** 这是 `QFileDialog` 的配置属性。初始化或状态切换时通过 `setViewMode(...)` 设置，之后用 `viewMode()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`ViewMode`。
- 属性名：`viewMode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFileDialog::QFileDialog(QWidget *parent, Qt::WindowFlags flags)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileDialog` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QWidget *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `flags`：类型为 `Qt::WindowFlags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QFileDialog::QFileDialog(QWidget *parent = nullptr, const QString &caption = QString(), const QString &directory = QString(), const QString &filter = QString())`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileDialog` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `caption`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `directory`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `filter`：类型为 `const QString &`。默认值为 `QString()`。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QFileDialog::~QFileDialog()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileDialog` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QFileDialog::accept()`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::accept` 用于执行与“接受”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QFileDialog::changeEvent(QEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::changeEvent` 用于执行与“change、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QEvent *`。没有默认值，调用时必须提供。传入 `QEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFileDialog::currentChanged(const QString &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileDialog` 发出的通知信号 `currentChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFileDialog::currentUrlChanged(const QUrl &url)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileDialog` 发出的通知信号 `currentUrlChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `url`：类型为 `const QUrl &`。没有默认值，调用时必须提供。资源地址。要确认 scheme、编码、相对路径、重定向和是否包含敏感信息。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDir QFileDialog::directory() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::directory` 用于计算、查询或取得与“directory”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDir`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDir`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFileDialog::directoryEntered(const QString &directory)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileDialog` 发出的通知信号 `directoryEntered`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `directory`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QUrl QFileDialog::directoryUrl() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::directoryUrl` 用于计算、查询或取得与“directory、Url”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QUrl`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QUrl`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFileDialog::directoryUrlEntered(const QUrl &directory)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileDialog` 发出的通知信号 `directoryUrlEntered`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `directory`：类型为 `const QUrl &`。没有默认值，调用时必须提供。传入 `const QUrl &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QFileDialog::done(int result)`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::done` 用于执行与“done”相关的操作。调用时要先确认当前状态和 `result` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `result`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFileDialog::fileSelected(const QString &file)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileDialog` 发出的通知信号 `fileSelected`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `file`：类型为 `const QString &`。没有默认值，调用时必须提供。文件或设备对象。要确认打开状态、读写模式、当前位置和错误状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFileDialog::filesSelected(const QStringList &selected)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileDialog` 发出的通知信号 `filesSelected`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `selected`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDir::Filters QFileDialog::filter() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::filter` 用于计算、查询或取得与“filter”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDir::Filters`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDir::Filters`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFileDialog::filterSelected(const QString &filter)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileDialog` 发出的通知信号 `filterSelected`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `filter`：类型为 `const QString &`。没有默认值，调用时必须提供。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QFileDialog::getExistingDirectory(QWidget *parent = nullptr, const QString &caption = QString(), const QString &dir = QString(), QFileDialog::Options options = ShowDirsOnly)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getExistingDirectory`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `caption`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `dir`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `options`：类型为 `QFileDialog::Options`。默认值为 `ShowDirsOnly`。传入 `QFileDialog::Options` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QUrl QFileDialog::getExistingDirectoryUrl(QWidget *parent = nullptr, const QString &caption = QString(), const QUrl &dir = QUrl(), QFileDialog::Options options = ShowDirsOnly, const QStringList &supportedSchemes = QStringList())`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getExistingDirectoryUrl`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QUrl`。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `caption`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `dir`：类型为 `const QUrl &`。默认值为 `QUrl()`。传入 `const QUrl &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `options`：类型为 `QFileDialog::Options`。默认值为 `ShowDirsOnly`。传入 `QFileDialog::Options` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `supportedSchemes`：类型为 `const QStringList &`。默认值为 `QStringList()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QFileDialog::getOpenFileContent(const QString &nameFilter, const std::function<void (const QString &, const QByteArray &)> &fileOpenCompleted, QWidget *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getOpenFileContent`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `nameFilter`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `fileOpenCompleted`：类型为 `const std::function<void (const QString &, const QByteArray &)> &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QFileDialog::getOpenFileName(QWidget *parent = nullptr, const QString &caption = QString(), const QString &dir = QString(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options())`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getOpenFileName`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `caption`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `dir`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `filter`：类型为 `const QString &`。默认值为 `QString()`。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。
- 参数 `selectedFilter`：类型为 `QString *`。默认值为 `nullptr`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `options`：类型为 `QFileDialog::Options`。默认值为 `Options()`。传入 `QFileDialog::Options` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QStringList QFileDialog::getOpenFileNames(QWidget *parent = nullptr, const QString &caption = QString(), const QString &dir = QString(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options())`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getOpenFileNames`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `caption`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `dir`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `filter`：类型为 `const QString &`。默认值为 `QString()`。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。
- 参数 `selectedFilter`：类型为 `QString *`。默认值为 `nullptr`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `options`：类型为 `QFileDialog::Options`。默认值为 `Options()`。传入 `QFileDialog::Options` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QUrl QFileDialog::getOpenFileUrl(QWidget *parent = nullptr, const QString &caption = QString(), const QUrl &dir = QUrl(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options(), const QStringList &supportedSchemes = QStringList())`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getOpenFileUrl`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QUrl`。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `caption`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `dir`：类型为 `const QUrl &`。默认值为 `QUrl()`。传入 `const QUrl &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `filter`：类型为 `const QString &`。默认值为 `QString()`。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。
- 参数 `selectedFilter`：类型为 `QString *`。默认值为 `nullptr`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `options`：类型为 `QFileDialog::Options`。默认值为 `Options()`。传入 `QFileDialog::Options` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `supportedSchemes`：类型为 `const QStringList &`。默认值为 `QStringList()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QList<QUrl> QFileDialog::getOpenFileUrls(QWidget *parent = nullptr, const QString &caption = QString(), const QUrl &dir = QUrl(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options(), const QStringList &supportedSchemes = QStringList())`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getOpenFileUrls`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QList<QUrl>`。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `caption`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `dir`：类型为 `const QUrl &`。默认值为 `QUrl()`。传入 `const QUrl &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `filter`：类型为 `const QString &`。默认值为 `QString()`。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。
- 参数 `selectedFilter`：类型为 `QString *`。默认值为 `nullptr`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `options`：类型为 `QFileDialog::Options`。默认值为 `Options()`。传入 `QFileDialog::Options` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `supportedSchemes`：类型为 `const QStringList &`。默认值为 `QStringList()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QFileDialog::getSaveFileName(QWidget *parent = nullptr, const QString &caption = QString(), const QString &dir = QString(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options())`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getSaveFileName`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `caption`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `dir`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `filter`：类型为 `const QString &`。默认值为 `QString()`。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。
- 参数 `selectedFilter`：类型为 `QString *`。默认值为 `nullptr`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `options`：类型为 `QFileDialog::Options`。默认值为 `Options()`。传入 `QFileDialog::Options` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QUrl QFileDialog::getSaveFileUrl(QWidget *parent = nullptr, const QString &caption = QString(), const QUrl &dir = QUrl(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options(), const QStringList &supportedSchemes = QStringList())`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getSaveFileUrl`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QUrl`。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `caption`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `dir`：类型为 `const QUrl &`。默认值为 `QUrl()`。传入 `const QUrl &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `filter`：类型为 `const QString &`。默认值为 `QString()`。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。
- 参数 `selectedFilter`：类型为 `QString *`。默认值为 `nullptr`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `options`：类型为 `QFileDialog::Options`。默认值为 `Options()`。传入 `QFileDialog::Options` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `supportedSchemes`：类型为 `const QStringList &`。默认值为 `QStringList()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QFileDialog::history() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::history` 用于计算、查询或取得与“history”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractFileIconProvider *QFileDialog::iconProvider() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::iconProvider` 用于计算、查询或取得与“icon、Provider”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractFileIconProvider *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractFileIconProvider *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractItemDelegate *QFileDialog::itemDelegate() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::itemDelegate` 用于计算、查询或取得与“项目访问、Delegate”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractItemDelegate *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractItemDelegate *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileDialog::labelText(QFileDialog::DialogLabel label) const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::labelText` 用于计算、查询或取得与“label、文本”相关的操作。调用时要先确认当前状态和 `label` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `label`：类型为 `QFileDialog::DialogLabel`。没有默认值，调用时必须提供。传入 `QFileDialog::DialogLabel` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QFileDialog::mimeTypeFilters() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::mimeTypeFilters` 用于计算、查询或取得与“mime、类型、Filters”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QFileDialog::nameFilters() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::nameFilters` 用于计算、查询或取得与“名称、Filters”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::open(QObject *receiver, const char *member)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `open`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `receiver`：类型为 `QObject *`。没有默认值，调用时必须提供。接收者对象。它决定槽函数所属线程和连接生命周期，必须在回调使用期间有效。
- 参数 `member`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 成功后才能 read/write/seek；失败时检查 `errorString()`，结束时 close 或让对象安全析构。

### `QAbstractProxyModel *QFileDialog::proxyModel() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::proxyModel` 用于计算、查询或取得与“proxy、Model”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractProxyModel *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractProxyModel *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileDialog::restoreState(const QByteArray &state)`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::restoreState` 用于计算、查询或取得与“恢复、State”相关的操作。调用时要先确认当前状态和 `state` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `state`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。状态值或状态对象；它描述调用时的阶段，不能把某个状态下有效的 API 用到其他阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QFileDialog::saveFileContent(const QByteArray &fileContent, const QString &fileNameHint, QWidget *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `saveFileContent`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `fileContent`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `fileNameHint`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QFileDialog::saveState() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::saveState` 用于计算、查询或取得与“保存、State”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::selectFile(const QString &filename)`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::selectFile` 用于执行与“select、File”相关的操作。调用时要先确认当前状态和 `filename` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `filename`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::selectMimeTypeFilter(const QString &filter)`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::selectMimeTypeFilter` 用于执行与“select、Mime、类型、Filter”相关的操作。调用时要先确认当前状态和 `filter` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `filter`：类型为 `const QString &`。没有默认值，调用时必须提供。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::selectNameFilter(const QString &filter)`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::selectNameFilter` 用于执行与“select、名称、Filter”相关的操作。调用时要先确认当前状态和 `filter` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `filter`：类型为 `const QString &`。没有默认值，调用时必须提供。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::selectUrl(const QUrl &url)`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::selectUrl` 用于执行与“select、Url”相关的操作。调用时要先确认当前状态和 `url` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `url`：类型为 `const QUrl &`。没有默认值，调用时必须提供。资源地址。要确认 scheme、编码、相对路径、重定向和是否包含敏感信息。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QFileDialog::selectedFiles() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::selectedFiles` 用于计算、查询或取得与“selected、Files”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileDialog::selectedMimeTypeFilter() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::selectedMimeTypeFilter` 用于计算、查询或取得与“selected、Mime、类型、Filter”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileDialog::selectedNameFilter() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::selectedNameFilter` 用于计算、查询或取得与“selected、名称、Filter”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QUrl> QFileDialog::selectedUrls() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::selectedUrls` 用于计算、查询或取得与“selected、Urls”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QUrl>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QUrl>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::setDirectory(const QString &directory)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDirectory`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `directory`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::setDirectory(const QDir &directory)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDirectory`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `directory`：类型为 `const QDir &`。没有默认值，调用时必须提供。传入 `const QDir &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::setDirectoryUrl(const QUrl &directory)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDirectoryUrl`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `directory`：类型为 `const QUrl &`。没有默认值，调用时必须提供。传入 `const QUrl &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::setFilter(QDir::Filters filters)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFilter`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `filters`：类型为 `QDir::Filters`。没有默认值，调用时必须提供。传入 `QDir::Filters` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::setHistory(const QStringList &paths)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHistory`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `paths`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::setIconProvider(QAbstractFileIconProvider *provider)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setIconProvider`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `provider`：类型为 `QAbstractFileIconProvider *`。没有默认值，调用时必须提供。传入 `QAbstractFileIconProvider *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::setItemDelegate(QAbstractItemDelegate *delegate)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setItemDelegate`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `delegate`：类型为 `QAbstractItemDelegate *`。没有默认值，调用时必须提供。传入 `QAbstractItemDelegate *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::setLabelText(QFileDialog::DialogLabel label, const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setLabelText`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `label`：类型为 `QFileDialog::DialogLabel`。没有默认值，调用时必须提供。传入 `QFileDialog::DialogLabel` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::setMimeTypeFilters(const QStringList &filters)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMimeTypeFilters`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `filters`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::setNameFilter(const QString &filter)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNameFilter`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `filter`：类型为 `const QString &`。没有默认值，调用时必须提供。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::setNameFilters(const QStringList &filters)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNameFilters`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `filters`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::setOption(QFileDialog::Option option, bool on = true)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setOption`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `option`：类型为 `QFileDialog::Option`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `on`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::setProxyModel(QAbstractProxyModel *proxyModel)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setProxyModel`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `proxyModel`：类型为 `QAbstractProxyModel *`。没有默认值，调用时必须提供。传入 `QAbstractProxyModel *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDialog::setSidebarUrls(const QList<QUrl> &urls)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSidebarUrls`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `urls`：类型为 `const QList<QUrl> &`。没有默认值，调用时必须提供。传入 `const QList<QUrl> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QFileDialog::setVisible(bool visible)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVisible`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `visible`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QUrl> QFileDialog::sidebarUrls() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::sidebarUrls` 用于计算、查询或取得与“sidebar、Urls”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QUrl>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QUrl>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileDialog::testOption(QFileDialog::Option option) const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDialog::testOption` 用于计算、查询或取得与“test、Option”相关的操作。调用时要先确认当前状态和 `option` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `option`：类型为 `QFileDialog::Option`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFileDialog::urlSelected(const QUrl &url)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileDialog` 发出的通知信号 `urlSelected`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `url`：类型为 `const QUrl &`。没有默认值，调用时必须提供。资源地址。要确认 scheme、编码、相对路径、重定向和是否包含敏感信息。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QFileDialog::urlsSelected(const QList<QUrl> &urls)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileDialog` 发出的通知信号 `urlsSelected`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `urls`：类型为 `const QList<QUrl> &`。没有默认值，调用时必须提供。传入 `const QList<QUrl> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum AcceptMode { AcceptOpen, AcceptSave }`

**API 类别：** 公有类型

**中文解读：** 这是 `QFileDialog` 暴露的类型声明 `接受、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum DialogLabel { LookIn, FileName, FileType, Accept, Reject }`

**API 类别：** 公有类型

**中文解读：** 这是 `QFileDialog` 暴露的类型声明 `Dialog、Label`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum Option { ShowDirsOnly, DontResolveSymlinks, DontConfirmOverwrite, DontUseNativeDialog, ReadOnly, …, DontUseCustomDirectoryIcons }`

**API 类别：** 公有类型

**中文解读：** 这是 `QFileDialog` 暴露的类型声明 `Option`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags Options`

**API 类别：** 公有类型

**中文解读：** 这是 `QFileDialog` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFileDialog::AcceptMode acceptMode() const`

**API 类别：** 公有函数

**中文解读：** `QFileDialog::acceptMode` 用于计算、查询或取得与“接受、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFileDialog::AcceptMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFileDialog::AcceptMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString defaultSuffix() const`

**API 类别：** 公有函数

**中文解读：** `QFileDialog::defaultSuffix` 用于计算、查询或取得与“default、Suffix”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFileDialog::FileMode fileMode() const`

**API 类别：** 公有函数

**中文解读：** `QFileDialog::fileMode` 用于计算、查询或取得与“file、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFileDialog::FileMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFileDialog::FileMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFileDialog::Options options() const`

**API 类别：** 公有函数

**中文解读：** `QFileDialog::options` 用于计算、查询或取得与“options”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFileDialog::Options`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFileDialog::Options`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAcceptMode(QFileDialog::AcceptMode mode)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setAcceptMode`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QFileDialog::AcceptMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDefaultSuffix(const QString &suffix)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDefaultSuffix`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `suffix`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setFileMode(QFileDialog::FileMode mode)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setFileMode`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QFileDialog::FileMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setOptions(QFileDialog::Options options)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setOptions`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `options`：类型为 `QFileDialog::Options`。没有默认值，调用时必须提供。传入 `QFileDialog::Options` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSupportedSchemes(const QStringList &schemes)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSupportedSchemes`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `schemes`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setViewMode(QFileDialog::ViewMode mode)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setViewMode`。调用它会改变 `QFileDialog` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QFileDialog::ViewMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList supportedSchemes() const`

**API 类别：** 公有函数

**中文解读：** `QFileDialog::supportedSchemes` 用于计算、查询或取得与“supported、Schemes”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFileDialog::ViewMode viewMode() const`

**API 类别：** 公有函数

**中文解读：** `QFileDialog::viewMode` 用于计算、查询或取得与“view、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFileDialog::ViewMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFileDialog::ViewMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先设置路径或设备，再 open，成功后读写/定位/刷新，最后 close；析构通常会关闭设备，但关键写入应显式 flush/close 并检查错误。相对路径依赖当前工作目录，资源路径和用户文件路径要区分。

### 状态和错误边界

区分设备未打开、打开成功、到达 EOF、暂时无数据、读写失败和写入尚未落盘。`readAll()` 方便小数据但可能占用大量内存，大文件应分块处理并检查返回值。

### 线程边界

同一个打开设备不要跨线程并发使用，除非类明确保证线程安全；后台 I/O 通过 worker 或异步设备处理，GUI 线程只接收结果。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QFileDialog` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
