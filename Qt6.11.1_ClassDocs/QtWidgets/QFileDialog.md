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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QFileDialog::FileMode`

**作用与语义：**

这个枚举用于表示用户在文件对话框中可以选择的内容;也就是如果用户点击确定，对话框返回的内容。
- `QFileDialog::AnyFile`：`0`;文件名称，无论是否存在。
- `QFileDialog::ExistingFile`：`1`;单个现有文件的名称。
- `QFileDialog::Directory`：`2`;目录名称。文件和目录都会显示。然而，Windows的原生文件对话框不支持在目录选择器中显示文件。
- `QFileDialog::ExistingFiles`：`3`;零个或多个现有文件的名称。

### `enum QFileDialog::Optionflags QFileDialog::Options`

**作用与语义：**

这些选项会影响对话的行为。
- `QFileDialog::ShowDirsOnly`：`0x00000001`;仅显示目录。默认情况下，文件和目录都会显示。

该选项仅在`Directory`文件模式下有效。
- `QFileDialog::DontResolveSymlinks`：`0x00000002`;不要解析符号链接。默认情况下，符号链接已被解析。
- `QFileDialog::DontConfirmOverwrite`：`0x00000004`;如果已选中已有文件，不要要求确认。默认情况下，会请求确认。

该选项仅在`acceptMode`为`AcceptSave`时有效）。此外，macOS上不用于原生文件对话框。
- `QFileDialog::DontUseNativeDialog`：`0x00000008`;不要使用平台原生的文件对话框，而是使用 Qt 提供的基于控件的对话框。

默认情况下，除非你使用包含`Q_OBJECT`宏的子类`QFileDialog`、设置了全局`AA_DontUseNativeDialogs`应用属性，或平台没有你所需的本地对话框，否则会显示原生文件对话框。

为了让该选项生效，你必须在更改对话框的其他属性或显示对话框之前设置它。
- `QFileDialog::ReadOnly`：`0x00000010`;表示模型为唯读。
- `QFileDialog::HideNameFilterDetails`：`0x00000020`;指示文件名过滤细节是否隐藏。
- `QFileDialog::DontUseCustomDirectoryIcons`：`0x00000040`;始终使用默认目录图标。

部分平台允许用户设置不同的图标，但自定义图标查询可能会在网络或可移动硬盘上造成显著的性能问题。

设置后，`iconProvider()`中的`DontUseCustomDirectoryIcons`选项会被启用。

该枚举值是在第5.2季度添加的。
Options 类型是 QFlags 的 typedef<Option>。它存储 Option 值的 OR 组合。

### `enum QFileDialog::ViewMode`

**作用与语义：**

该枚举描述了文件对话框的视图模式;即显示每个文件的信息。
- `QFileDialog::Detail`：`0`;显示目录中每个项目的图标、名称和详细信息。
- `QFileDialog::List`：`1`;仅显示目录中每个项目的图标和名称。

### `acceptMode : AcceptMode`

**作用与语义：**

该属性表示对话的接受模式。
动作模式定义了对话框是用于打开文件还是保存文件。
默认情况下，该属性设置为`AcceptOpen`。

**如何使用：** 调用 `acceptMode()` 读取当前值；它不会修改应用状态。

### `defaultSuffix : QString`

**作用与语义：**

如果文件名中没有其他后缀，则添加后缀。
该属性指定了如果文件名尚未带有后缀时添加的字符串。后缀通常用于指示文件类型（例如，“txt”表示文本文件）。
如果第一个字符是点（'.'），则该字符被移除。

**如何使用：** 调用 `defaultSuffix()` 读取当前值；它不会修改应用状态。

### `fileMode : FileMode`

**作用与语义：**

该属性保留对话文件模式。
文件模式定义了用户在对话框中应选择的物品数量和类型。
默认情况下，该属性设置为`AnyFile`。
该函数设置`FileName`和`Accept` `DialogLabel`的标签。调用 setFileMode() 后可以设置自定义文本。

**如何使用：** 调用 `fileMode()` 读取当前值；它不会修改应用状态。

### `options : Options`

**作用与语义：**

该属性包含影响对话视觉和感觉的各种选项。
默认情况下，所有选项都是被禁用的。
选项（尤其是`DontUseNativeDialog`选项）应在更改对话框属性或显示对话框之前设置好。
在对话框可见时设置选项并不保证会立即对对话框产生影响（具体取决于选项和平台）。
更改其他属性后设置选项可能使这些值无效。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `supportedSchemes : QStringList`

**作用与语义：**

该属性包含文件对话框应允许导航的 URL 方案。
设置该属性可以限制用户可选择的 URL 类型。这是应用程序声明其支持的获取文件内容协议的一种方式。空列表表示不施加限制（默认）。本地文件（“文件”方案）支持是隐含且始终启用的;不必将其包含在限制中。

**如何使用：** 调用 `supportedSchemes()` 读取当前值；它不会修改应用状态。

### `viewMode : ViewMode`

**作用与语义：**

该属性决定了文件和目录在对话框中的显示方式。
默认情况下，`Detail`模式用于显示文件和目录的信息。

**如何使用：** 调用 `viewMode()` 读取当前值；它不会修改应用状态。

### `QFileDialog::QFileDialog(QWidget *parent, Qt::WindowFlags flags)`

**作用与语义：**

构建包含给定`parent`和控件`flags`的文件对话框。

### `[explicit] QFileDialog::QFileDialog(QWidget *parent = nullptr, const QString &caption = QString(), const QString &directory = QString(), const QString &filter = QString())`

**作用与语义：**

构建一个包含给定`parent`和`caption`的文件对话框，最初显示指定`directory`的内容。目录内容在显示前会被过滤，使用`filter`指定的分号分隔的筛选列表。

### `[virtual noexcept] QFileDialog::~QFileDialog()`

**作用与语义：**

会破坏文件对话框。

### `[override virtual protected] void QFileDialog::accept()`

**作用与语义：**

重装：`QDialog::accept()`。
隐藏模态对话框，并将结果代码设置为`Accepted`。

### `[override virtual protected] void QFileDialog::changeEvent(QEvent *e)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `[signal] void QFileDialog::currentChanged(const QString &path)`

**作用与语义：**

当当前文件因本地操作而更改时，该信号以新文件名作为`path`参数发出。

### `[signal] void QFileDialog::currentUrlChanged(const QUrl &url)`

**作用与语义：**

当前文件发生变化时，该信号以新文件URL作为`url`参数发出。

### `QDir QFileDialog::directory() const`

**作用与语义：**

返回当前对话框中显示的目录。

### `[signal] void QFileDialog::directoryEntered(const QString &directory)`

**作用与语义：**

当用户进入`directory`时，该信号用于本地操作。

### `QUrl QFileDialog::directoryUrl() const`

**作用与语义：**

返回当前对话框中显示的目录的网址。

### `[signal] void QFileDialog::directoryUrlEntered(const QUrl &directory)`

**作用与语义：**

当用户进入`directory`时，该信号会发出。

### `[override virtual protected] void QFileDialog::done(int result)`

**作用与语义：**

重装：`QDialog::done`（int r）。
关闭对话并将结果代码设置为`r`。`finished()`信号会发出`r`;如果`r`是`QDialog::Accepted`或`QDialog::Rejected`，则分别会发出`accepted()`或`rejected()`信号。
如果该对话以`exec()`显示，done() 也会导致本地事件循环结束，`exec()`返回`r`。
与`QWidget::close()`一样，如果设置了`Qt::WA_DeleteOnClose`标志，done() 会删除对话。如果对话框是应用程序的主控件，应用程序将终止。如果对话框是最后关闭的窗口，则发出`QGuiApplication::lastWindowClosed()`信号。

### `[signal] void QFileDialog::fileSelected(const QString &file)`

**作用与语义：**

当选择发生变化且对话被接受时，该信号会随选中的（可能为空的）`file`一起发出。

### `[signal] void QFileDialog::filesSelected(const QStringList &selected)`

**作用与语义：**

当本地操作的选择发生变化且对话被接受时，该信号会随（可能为空的）`selected`文件列表一起发出。

### `QDir::Filters QFileDialog::filter() const`

**作用与语义：**

返回显示文件时使用的过滤器。

### `[signal] void QFileDialog::filterSelected(const QString &filter)`

**作用与语义：**

当用户选择`filter`时，会发出该信号。

### `[static] QString QFileDialog::getExistingDirectory(QWidget *parent = nullptr, const QString &caption = QString(), const QString &dir = QString(), QFileDialog::Options options = ShowDirsOnly)`

**作用与语义：**

这是一个便捷的静态函数，用于返回用户选择的现有目录。 该函数使用给定的 `parent` 小部件创建一个模态文件对话框。如果 `parent` 不是 `nullptr`，则对话框会显示在父小部件的中心。 对话框的工作目录设置为 `dir`，标题设置为 `caption`。这两者都可以是空字符串，在这种情况下，分别使用当前目录和默认标题。 `options` 参数包含有关如何运行对话框的各种选项。有关可以传递的标志的更多信息，请参见 `QFileDialog::Option` 枚举。为了确保原生文件对话框，必须设置 `ShowDirsOnly`。 在 Windows 和 macOS 上，此静态函数使用原生文件对话框而不是 `QFileDialog`。但是，Windows 原生文件对话框不支持在目录选择器中显示文件。您需要传递 `DontUseNativeDialog` 选项，或设置全局 `AA_DontUseNativeDialogs` 应用程序属性以使用 `QFileDialog` 显示文件。 请注意，macOS 原生文件对话框不显示标题栏。 在 Unix/X11 上，文件对话框的正常行为是解析并遵循符号链接。例如，如果 `/usr/tmp` 是 `/var/tmp` 的符号链接，那么在进入 `/usr/tmp` 后，文件对话框会切换到 `/var/tmp`。如果 `options` 包含 `DontResolveSymlinks`，则文件对话框将符号链接视为常规目录。 在 Windows 上，对话框会旋转一个阻塞的模态事件循环，不会分发任何 QTimers，并且如果 `parent` 不是 `nullptr`，则将对话框定位在父窗口标题栏正下方。

**官方示例：**

```cpp
 QString dir = QFileDialog::getExistingDirectory(this, tr("Open Directory"),
                                                 "/home",
                                                 QFileDialog::ShowDirsOnly
                                                 | QFileDialog::DontResolveSymlinks);
```

### `[static] QUrl QFileDialog::getExistingDirectoryUrl(QWidget *parent = nullptr, const QString &caption = QString(), const QUrl &dir = QUrl(), QFileDialog::Options options = ShowDirsOnly, const QStringList &supportedSchemes = QStringList())`

**作用与语义：**

这是一个便捷的静态函数，用于返回用户选择的现有目录。如果用户按取消，则返回空的 URL。 该函数的使用方式类似于 `QFileDialog::getExistingDirectory()`。特别是 `parent`、`caption`、`dir` 和 `options` 的使用方式完全相同。 与 `QFileDialog::getExistingDirectory()` 的主要区别在于提供给用户选择远程目录的能力。这就是返回类型和 `dir` 类型为 `QUrl` 的原因。 `supportedSchemes` 参数允许限制用户能够选择的 URL 类型。这是应用程序声明其支持获取文件内容协议的一种方式。空列表表示不应用任何限制（默认）。对本地文件（"file" 协议）的支持是隐含的并始终启用；无需在限制中包括它。 在可能的情况下，此静态函数使用原生文件对话框而不是 `QFileDialog`。在不支持选择远程文件的平台上，Qt 仅允许选择本地文件。

### `[static] void QFileDialog::getOpenFileContent(const QString &nameFilter, const std::function<void (const QString &, const QByteArray &)> &fileOpenCompleted, QWidget *parent = nullptr)`

**作用与语义：**

这是一个方便的静态函数，返回用户选择的文件内容。
如果网页沙箱限制文件访问，可以使用此函数访问 WebAssembly 的 Qt 本地文件。其实现允许浏览器中显示原生文件对话框，用户根据 `nameFilter` 参数选择文件。
`parent` 在 Qt 上被忽略，用于 WebAssembly。在其他平台上传递 `parent`，使弹窗成为另一个小部件的子节点。如果平台不支持本地文件对话框，函数会退回到 `QFileDialog`。
该函数是异步的，会立即返回。当文件被选中并其内容被读取到内存时，`fileOpenCompleted`回调才会被调用。

**官方示例：**

```cpp
 auto fileContentReady = [](const QString &fileName, const QByteArray &fileContent) {
     if (fileName.isEmpty()) {
         // No file was selected
     } else {
         // Use fileName and fileContent
     }
 };
 QFileDialog::getOpenFileContent("Images (*.png *.xpm *.jpg)",  fileContentReady);
```

### `[static] QString QFileDialog::getOpenFileName(QWidget *parent = nullptr, const QString &caption = QString(), const QString &dir = QString(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options())`

**作用与语义：**

这是一个方便的静态函数，返回用户选择的现有文件。如果用户按下取消键，会返回一个空字符串。
该函数创建一个带有给定`parent`组件的模态文件对话框。如果`parent`未`nullptr`，对话框会显示在父控件的中心位置。
文件对话框的工作目录设置为`dir`。如果`dir`包含文件名，则选择该文件。仅显示与给定`filter`匹配的文件。所选过滤器设置为`selectedFilter`。参数`dir`、`selectedFilter`和`filter`可能是空字符串。如果你想要多个过滤器，可以用 ';;' 分隔它们，例如：
`options`论证包含多种关于如何运行对话的选项。有关可通过的标志的更多信息，请参见`QFileDialog::Option`枚举。
对话框的标题设置为`caption`。如果未指定`caption`，则使用默认字幕。
在 Windows 和 macOS 上，这个静态功能使用原生文件对话框，而不是`QFileDialog`。注意，macOS 原生文件对话框不显示标题栏。
在 Windows 上，该对话框会旋转一个阻塞模态事件循环，不会调度任何 QTimer，如果`parent`未`nullptr`，则会将对话定位在父标题栏的正下方。
在Unix/X11中，文件对话框的正常行为是解析并跟随符号链接。例如，如果`/usr/tmp`是指向`/var/tmp`的符号链接，文件对话框在进入`/usr/tmp`后会变成`/var/tmp`。如果`options`包含`DontResolveSymlinks`，文件对话框将符号链接视为常规目录。

**官方示例：**

```cpp
 QString fileName = QFileDialog::getOpenFileName(this, tr("Open File"),
                                                 "/home",
                                                 tr("Images (*.png *.xpm *.jpg)"));
```

### `[static] QStringList QFileDialog::getOpenFileNames(QWidget *parent = nullptr, const QString &caption = QString(), const QString &dir = QString(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options())`

**作用与语义：**

这是一个方便的静态函数，返回用户选择的一个或多个现有文件。
该函数创建一个带有给定`parent`控件的模态文件对话框。如果没有`nullptr` `parent`，对话框会显示在父控件的中央。
文件对话框的工作目录设置为`dir`。如果`dir`包含文件名，则选择该文件。过滤器设置为`filter`，仅显示与该过滤器匹配的文件。所选过滤器设置为`selectedFilter`。参数`dir`、`selectedFilter`和`filter`可以是空字符串。如果需要多个过滤器，可以用“;;”分隔，例如：
对话框的字幕设置为`caption`。如果未指定`caption`，则使用默认字幕。
在 Windows 和 macOS 上，这个静态功能使用原生文件对话框，而不是`QFileDialog`。注意，macOS 原生文件对话框不显示标题栏。
在 Windows 上，该对话框会旋转一个阻塞模态事件循环，不会调度任何 QTimer，如果`parent`未`nullptr`，则会将对话定位在父标题栏的正下方。
在 Unix/X11 上，文件对话框的正常行为是解析并跟随符号链接。例如，如果 `/usr/tmp` 是符号链接到 `/var/tmp`，文件对话框进入 `/usr/tmp` 后会变成 `/var/tmp`。`options` 参数包含了多种关于如何运行对话的选项，详见 `QFileDialog::Option` 枚举中关于可传递标志的更多信息。

**官方示例：**

```cpp
 QStringList files = QFileDialog::getOpenFileNames(
                         this,
                         "Select one or more files to open",
                         "/home",
                         "Images (*.png *.xpm *.jpg)");
```

### `[static] QUrl QFileDialog::getOpenFileUrl(QWidget *parent = nullptr, const QString &caption = QString(), const QUrl &dir = QUrl(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options(), const QStringList &supportedSchemes = QStringList())`

**作用与语义：**

这是一个方便的静态函数，返回用户选择的现有文件。如果用户按下取消键，会返回一个空的 URL。
该函数的使用方式与`QFileDialog::getOpenFileName()`类似。特别是 `parent`、`caption`、`dir`、`filter`、`selectedFilter` 和 `options` 的使用方式完全相同。
`QFileDialog::getOpenFileName()`的主要区别在于用户可以选择远程文件。这就是为什么返回类型和`dir`类型`QUrl`。
`supportedSchemes`参数允许限制用户可选择的 URL 类型。这是应用程序声明其支持的协议以获取文件内容的一种方式。空列表表示不施加限制（默认）。本地文件（“文件”方案）支持是隐式且始终启用的;不必将其包含在限制中。
在可能的情况下，这个静态函数使用原生文件对话框，而不是`QFileDialog`。在不支持选择远程文件的平台上，Qt 只允许选择本地文件。

### `[static] QList<QUrl> QFileDialog::getOpenFileUrls(QWidget *parent = nullptr, const QString &caption = QString(), const QUrl &dir = QUrl(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options(), const QStringList &supportedSchemes = QStringList())`

**作用与语义：**

这是一个方便的静态函数，返回用户选择的一个或多个现有文件。如果用户按下取消键，会返回一个空列表。
该函数的使用方式与`QFileDialog::getOpenFileNames()`类似。特别是`parent`、`caption`、`dir`、`filter`、`selectedFilter`和`options`的使用方式完全相同。
`QFileDialog::getOpenFileNames()`的主要区别在于用户选择远程文件的能力。这就是为什么返回类型和`dir`类型分别是<`QUrl`>`QList`和 `QUrl`。
`supportedSchemes`参数允许限制用户可选择的 URL 类型。这是应用程序声明其支持的协议以获取文件内容的一种方式。空列表表示不施加限制（默认）。对本地文件（“文件”方案）的支持是隐含且始终启用的;不必将其包含在限制中。
在可能的情况下，这个静态函数使用原生文件对话框，而不是`QFileDialog`。在不支持选择远程文件的平台上，Qt 只允许选择本地文件。

### `[static] QString QFileDialog::getSaveFileName(QWidget *parent = nullptr, const QString &caption = QString(), const QString &dir = QString(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options())`

**作用与语义：**

这是一个方便的静态函数，返回用户选择的文件名。文件不必存在。
它会创建一个带有给定`parent`小部件的模态文件对话框。如果`parent`未`nullptr`，对话框将以父小部件居中显示。
文件对话框的工作目录设置为`dir`。如果`dir`包含文件名，则选择该文件。仅显示与`filter`匹配的文件。所选过滤器设置为`selectedFilter`。参数`dir`、`selectedFilter`和`filter`可以是空字符串。多个过滤器用“;;”分隔。例如：
`options`论点包含了多种关于如何运行对话的选项，请参见`QFileDialog::Option`枚举中关于可以传递的标志的更多信息。
默认过滤器可以通过设置`selectedFilter`为所需值来选择。
对话框的字幕设置为`caption`。如果未指定`caption`，则使用默认字幕。
在 Windows 和 macOS 上，这个静态函数使用原生文件对话框，而不是`QFileDialog`。
在 Windows 上，该对话框会旋转一个阻塞模态事件循环，不会派遣任何 QTimer，如果`parent`未`nullptr`，则会将对话框定位在父标题栏的正下方。在 macOS 上，原生文件对话框中，过滤器参数被忽略。
在Unix/X11上，文件对话框的正常行为是解析并跟随符号链接。例如，如果`/usr/tmp`是指向`/var/tmp`的符号链接，进入`/usr/tmp`后文件对话框会变成`/var/tmp`。如果`options`包含`DontResolveSymlinks`，文件对话框将符号链接视为常规目录。

**官方示例：**

```cpp
 QString fileName = QFileDialog::getSaveFileName(this, tr("Save File"),
                                                 "/home/jana/untitled.png",
                                                 tr("Images (*.png *.xpm *.jpg)"));
```

### `[static] QUrl QFileDialog::getSaveFileUrl(QWidget *parent = nullptr, const QString &caption = QString(), const QUrl &dir = QUrl(), const QString &filter = QString(), QString *selectedFilter = nullptr, QFileDialog::Options options = Options(), const QStringList &supportedSchemes = QStringList())`

**作用与语义：**

这是一个方便的静态函数，返回用户选择的文件。文件不必存在。如果用户点击取消，会返回空的 URL。
该函数的使用方式与`QFileDialog::getSaveFileName()`类似。特别是 `parent`、`caption`、`dir`、`filter`、`selectedFilter` 和 `options` 的使用方式完全相同。
`QFileDialog::getSaveFileName()`的主要区别在于用户可以选择远程文件。这就是为什么返回类型和`dir`类型`QUrl`。
`supportedSchemes`参数允许限制用户可选择的 URL 类型。这是应用程序声明其支持的协议以保存文件内容的一种方式。空列表表示不施加限制（默认）。对本地文件（“文件”方案）的支持是隐含且始终启用的;不必将其包含在限制中。
在可能的情况下，这个静态函数使用原生文件对话框，而不是`QFileDialog`。在不支持选择远程文件的平台上，Qt 只允许选择本地文件。

### `QStringList QFileDialog::history() const`

**作用与语义：**

返回 filedialog 的浏览历史，作为路径列表。

### `QAbstractFileIconProvider *QFileDialog::iconProvider() const`

**作用与语义：**

返回文件对话框使用的图标提供者。

### `QAbstractItemDelegate *QFileDialog::itemDelegate() const`

**作用与语义：**

返回用于在文件对话框中渲染视图中的物品代理。

### `QString QFileDialog::labelText(QFileDialog::DialogLabel label) const`

**作用与语义：**

返回指定`label`文件对话框中显示的文本。

### `QStringList QFileDialog::mimeTypeFilters() const`

**作用与语义：**

返回该文件对话框中正在运行的 MIME 类型过滤器。

### `QStringList QFileDialog::nameFilters() const`

**作用与语义：**

返回该文件对话框中正在运行的文件类型过滤器。

### `void QFileDialog::open(QObject *receiver, const char *member)`

**作用与语义：**

该功能显示对话，并将`receiver`和`member`指定的槽函数与通知选择变化的信号连接起来。如果`fileMode`是`ExistingFiles`，这就是`filesSelected()`信号，否则是`fileSelected()`信号。
当对话关闭时，信号会与槽函数断开连接。

### `QAbstractProxyModel *QFileDialog::proxyModel() const`

**作用与语义：**

返回文件对话框中使用的代理模型。默认情况下，没有设置代理。

### `bool QFileDialog::restoreState(const QByteArray &state)`

**作用与语义：**

将对话框的布局、历史和当前目录恢复到指定的`state`。
通常这与`QSettings`结合使用，以恢复上一次会话的大小。
如果有错误，返回`false`。

### `[static] void QFileDialog::saveFileContent(const QByteArray &fileContent, const QString &fileNameHint, QWidget *parent = nullptr)`

**作用与语义：**

这是一个方便的静态功能，将`fileContent`保存到文件中，使用用户选择的文件名和位置。`fileNameHint`可以向用户推荐文件名。
如果网页沙箱限制了文件访问，使用该函数将内容保存到本地文件中的 Qt for WebAssembly。其实现允许在浏览器中显示原生文件对话框，用户根据 `fileNameHint` 参数指定输出文件。
`parent`在 Qt 上被忽略，只用于 WebAssembly。在其他平台上传递 `parent`，使弹窗成为另一个小部件的子节点。如果平台不支持原生文件对话框，函数会退回到 `QFileDialog`。
该函数是异步的，且能立即返回。

**官方示例：**

```cpp
 QByteArray imageData; // obtained from e.g. QImage::save()
 QFileDialog::saveFileContent(imageData, "myimage.png");
```

### `QByteArray QFileDialog::saveState() const`

**作用与语义：**

保存对话框的布局、历史和当前目录的状态。
通常与`QSettings`结合使用，以记住未来会话的大小。版本号作为数据的一部分存储。

### `void QFileDialog::selectFile(const QString &filename)`

**作用与语义：**

在文件对话框中选择给定的`filename`。

### `void QFileDialog::selectMimeTypeFilter(const QString &filter)`

**作用与语义：**

设置当前的MIME类型`filter`。

### `void QFileDialog::selectNameFilter(const QString &filter)`

**作用与语义：**

设置当前文件类型 `filter`。通过分号或空格分隔，可以通过多个过滤器`filter`传递。

### `void QFileDialog::selectUrl(const QUrl &url)`

**作用与语义：**

在文件对话框中选择给定的`url`。
注意：非原生`QFileDialog`仅支持本地文件。

### `QStringList QFileDialog::selectedFiles() const`

**作用与语义：**

返回对话框中所选文件的绝对路径字符串列表。如果未选择文件，或模式未`ExistingFiles`或未`ExistingFile`，selectFiles() 包含视口中的当前路径。

### `QString QFileDialog::selectedMimeTypeFilter() const`

**作用与语义：**

返回用户在文件对话框中选择的文件的 mimetype 类型。

### `QString QFileDialog::selectedNameFilter() const`

**作用与语义：**

返回用户在文件对话框中选择的过滤器。

### `QList<QUrl> QFileDialog::selectedUrls() const`

**作用与语义：**

返回对话框中包含所选文件的URL列表。如果未选择文件，或模式未`ExistingFiles`或未`ExistingFile`，selectUrls()包含视口中的当前路径。

### `void QFileDialog::setDirectory(const QString &directory)`

**作用与语义：**

设置文件对话框当前的 `directory`。
注意：在 iOS 上，如果你将 `directory` 设置为 QStandardPaths：：standardLocations（QStandardPaths：:P icturesLocation）.last()，则会使用原生图片选择器对话框来访问用户的照片相册。返回的文件名可以通过 `QFile` 及相关 API 加载。要启用此功能，项目文件中分配给 QMAKE_INFO_PLIST 的 Info.plist 必须包含密钥 `NSPhotoLibraryUsageDescription`。有关该密钥的更多信息，请参阅苹果的 Info.plist 文档。该功能于 Qt 5.5 中加入。

### `void QFileDialog::setDirectory(const QDir &directory)`

**作用与语义：**

设置文件对话框当前的 `directory`。
注意：在 iOS 上，如果你将 `directory` 设置为 QStandardPaths：：standardLocations（QStandardPaths：:P icturesLocation）.last()，则会使用原生图片选择器对话框来访问用户的照片相册。返回的文件名可以通过 `QFile` 及相关 API 加载。要启用此功能，项目文件中分配给 QMAKE_INFO_PLIST 的 Info.plist 必须包含密钥 `NSPhotoLibraryUsageDescription`。有关该密钥的更多信息，请参阅苹果的 Info.plist 文档。该功能于 Qt 5.5 中加入。

### `void QFileDialog::setDirectoryUrl(const QUrl &directory)`

**作用与语义：**

设置文件对话框当前的`directory` URL。
注意：非原生`QFileDialog`仅支持本地文件。
注意：在 Windows 上，可以传递代表某个虚拟文件夹的 URL，如“Computer”或“Network”。这是通过通过方案 `clsid` 传递一个 `QUrl`，然后是去除大括号的 CLSID 值来实现。例如，URL `clsid:374DE290-123F-4565-9164-39C4925E467B` 表示下载位置。有关所有可能值的完整列表，请参见 MSDN 文档中的 KNOWNFOLDERID。该功能是在 Qt 5.5 中添加的。

### `void QFileDialog::setFilter(QDir::Filters filters)`

**作用与语义：**

将模型使用的过滤器设置为`filters`。过滤器用于指定应展示的文件类型。

### `void QFileDialog::setHistory(const QStringList &paths)`

**作用与语义：**

设置文件对话的浏览历史，包含给定的`paths`。

### `void QFileDialog::setIconProvider(QAbstractFileIconProvider *provider)`

**作用与语义：**

将文件对话中使用的图标提供者设置为指定的`provider`。

### `void QFileDialog::setItemDelegate(QAbstractItemDelegate *delegate)`

**作用与语义：**

将用于渲染文件对话框视图中物品的物品代理设置为给定的`delegate`。
任何现有的代表都会被移除，但不会被删除。`QFileDialog`不对`delegate`拥有所有权。
警告：你不应在不同视图之间共享同一个代理实例。这样做可能导致错误或不直观的编辑行为，因为连接到某个代理的每个视图都可能收到`closeEditor()`信号，并试图访问、修改或关闭已被关闭的编辑器。
请注意，所用模型是`QFileSystemModel`。它有自定义的物品数据角色，这些角色由`Roles`枚举描述。如果你只想要自定义图标，可以使用`QFileIconProvider`。

### `void QFileDialog::setLabelText(QFileDialog::DialogLabel label, const QString &text)`

**作用与语义：**

设置指定`label`文件对话框中显示的`text`。

### `void QFileDialog::setMimeTypeFilters(const QStringList &filters)`

**作用与语义：**

从MIME类型列表中设置文件对话框中使用的 `filters`。
方便`setNameFilters()`方法。利用`QMimeType`从每种MIME类型定义的球状模式和描述中创建名称过滤器。
使用application/octet-stream来设置“所有文件（*）”过滤器，因为这是所有文件的基础MIME类型。
调用 setMimeTypeFilters 会覆盖之前设置的所有名称过滤器，并改变 `nameFilters()` 的返回值。

**官方示例：**

```cpp
 QStringList mimeTypeFilters({"image/jpeg", // will show "JPEG image (*.jpeg *.jpg *.jpe)
                              "image/png",  // will show "PNG image (*.png)"
                              "application/octet-stream" // will show "All files (*)"
                             });

 QFileDialog dialog(this);
 dialog.setMimeTypeFilters(mimeTypeFilters);
 dialog.exec();
```

### `void QFileDialog::setNameFilter(const QString &filter)`

**作用与语义：**

将文件对话框中使用的过滤器设置为给定的`filter`。
如果`filter`包含一对包含一个或多个文件名-万用符模式的括号，且中间用空格分隔，则只使用括号内的文本作为过滤器。这意味着这些调用都是等价的：
注意：在 Android 原生文件对话框中，使用与名字过滤器匹配的哑剧类型，因为只支持哑剧类型。

**官方示例：**

```cpp
 dialog.setNameFilter("All C++ files (*.cpp *.cc *.C *.cxx *.c++)");
 dialog.setNameFilter("*.cpp *.cc *.C *.cxx *.c++");
```

### `void QFileDialog::setNameFilters(const QStringList &filters)`

**作用与语义：**

设置文件对话框中使用的`filters`。
注意，滤波器 *.* 不可移植，因为历史上文件扩展名决定文件类型的假设在每个操作系统上并不一致。文件名称中可能没有点（例如，`Makefile`）。在原生 Windows 文件对话框中，*.* 匹配此类文件，而在其他类型的文件对话框中可能不匹配。因此，如果你指的是选择任意文件，最好使用*。
`setMimeTypeFilters()` 的优点是为每种文件类型提供了所有可能的名称过滤器。例如，JPEG 图像有三种可能的扩展名;如果你的应用程序能打开这些文件，选择 `image/jpeg` mime 类型作为过滤器可以打开所有文件。

**官方示例：**

```cpp
 const QStringList filters({"Image files (*.png *.xpm *.jpg)",
                            "Text files (*.txt)",
                            "Any files (*)"
                           });
 QFileDialog dialog(this);
 dialog.setNameFilters(filters);
 dialog.exec();
```

### `void QFileDialog::setOption(QFileDialog::Option option, bool on = true)`

**作用与语义：**

如果 为真，则将给定`option`设置为启用`on`;否则，清除给定`option`。
在更改对话框属性或显示对话框之前，应先设置选项（尤其是`DontUseNativeDialog`选项）。
在对话框可见时设置选项并不保证会立即对对话框产生影响（具体取决于选项和平台）。
更改其他属性后设置选项可能使这些值无效。

### `void QFileDialog::setProxyModel(QAbstractProxyModel *proxyModel)`

**作用与语义：**

将视图的模型设置为给定的`proxyModel`。如果你想修改底层模型，这非常有用;例如，添加列、过滤数据或添加驱动器。
任何现有的代理模型都会被移除，但不会被删除。文件对话框会获得`proxyModel`的所有权。

### `void QFileDialog::setSidebarUrls(const QList<QUrl> &urls)`

**作用与语义：**

设置侧边栏里的`urls`。
例如：
然后文件对话框如下：

**官方示例：**

```cpp
 QList<QUrl> urls;
 urls << QUrl::fromLocalFile("/Users/foo/Code/qt5")
      << QUrl::fromLocalFile(QStandardPaths::standardLocations(QStandardPaths::MusicLocation).first());

 QFileDialog dialog;
 dialog.setSidebarUrls(urls);
 dialog.setFileMode(QFileDialog::AnyFile);
 if (dialog.exec()) {
     // ...
 }
```

### `[override virtual] void QFileDialog::setVisible(bool visible)`

**作用与语义：**

重实现自：`QDialog::setVisible`（bool可见）。
重新实现了属性的访问函数：`QWidget::visible`。

### `QList<QUrl> QFileDialog::sidebarUrls() const`

**作用与语义：**

返回侧边栏当前的URL列表。

### `bool QFileDialog::testOption(QFileDialog::Option option) const`

**作用与语义：**

如果启用给定`option`，返回 `true`;否则返回 false。

### `[signal] void QFileDialog::urlSelected(const QUrl &url)`

**作用与语义：**

当选择发生变化且对话被接受时，该信号会随选中的（可能为空的）`url`一起发出。

### `[signal] void QFileDialog::urlsSelected(const QList<QUrl> &urls)`

**作用与语义：**

当选择发生变化且对话被接受时，该信号会与（可能为空的）选中`urls`列表一起发出。

### `enum AcceptMode { AcceptOpen, AcceptSave }`

**作用与语义：**

决定文件对话框是在选择要打开的内容还是选择保存目标。`AcceptOpen` 使用打开语义，`AcceptSave` 使用保存语义，后者会影响确认按钮文字、文件存在检查和覆盖确认。

### `enum DialogLabel { LookIn, FileName, FileType, Accept, Reject }`

**作用与语义：**

标识文件对话框中可改写的文字位置：查找目录、文件名、文件类型、接受按钮和拒绝按钮。把枚举值传给 `setLabelText()` 自定义对应标签；未设置的位置继续使用平台翻译。

### `enum Option { ShowDirsOnly, DontResolveSymlinks, DontConfirmOverwrite, DontUseNativeDialog, ReadOnly, …, DontUseCustomDirectoryIcons }`

**作用与语义：**

这些选项会影响对话的行为。
- `QFileDialog::ShowDirsOnly`：`0x00000001`;仅显示目录。默认情况下，文件和目录都会显示。

该选项仅在`Directory`文件模式下有效。
- `QFileDialog::DontResolveSymlinks`：`0x00000002`;不要解析符号链接。默认情况下，符号链接已被解析。
- `QFileDialog::DontConfirmOverwrite`：`0x00000004`;如果已选中已有文件，不要要求确认。默认情况下，会请求确认。

该选项仅在`acceptMode`为`AcceptSave`时有效）。此外，macOS上不用于原生文件对话框。
- `QFileDialog::DontUseNativeDialog`：`0x00000008`;不要使用平台原生的文件对话框，而是使用 Qt 提供的基于控件的对话框。

默认情况下，除非你使用包含`Q_OBJECT`宏的子类`QFileDialog`、设置了全局`AA_DontUseNativeDialogs`应用属性，或平台没有你所需的本地对话框，否则会显示原生文件对话框。

为了让该选项生效，你必须在更改对话框的其他属性或显示对话框之前设置它。
- `QFileDialog::ReadOnly`：`0x00000010`;表示模型为唯读。
- `QFileDialog::HideNameFilterDetails`：`0x00000020`;指示文件名过滤细节是否隐藏。
- `QFileDialog::DontUseCustomDirectoryIcons`：`0x00000040`;始终使用默认目录图标。

部分平台允许用户设置不同的图标，但自定义图标查询可能会在网络或可移动硬盘上造成显著的性能问题。

设置后，`iconProvider()`中的`DontUseCustomDirectoryIcons`选项会被启用。

该枚举值是在第5.2季度添加的。
Options 类型是 QFlags 的 typedef<Option>。它存储 Option 值的 OR 组合。

### `flags Options`

**作用与语义：**

这些选项会影响对话的行为。
- `QFileDialog::ShowDirsOnly`：`0x00000001`;仅显示目录。默认情况下，文件和目录都会显示。

该选项仅在`Directory`文件模式下有效。
- `QFileDialog::DontResolveSymlinks`：`0x00000002`;不要解析符号链接。默认情况下，符号链接已被解析。
- `QFileDialog::DontConfirmOverwrite`：`0x00000004`;如果已选中已有文件，不要要求确认。默认情况下，会请求确认。

该选项仅在`acceptMode`为`AcceptSave`时有效）。此外，macOS上不用于原生文件对话框。
- `QFileDialog::DontUseNativeDialog`：`0x00000008`;不要使用平台原生的文件对话框，而是使用 Qt 提供的基于控件的对话框。

默认情况下，除非你使用包含`Q_OBJECT`宏的子类`QFileDialog`、设置了全局`AA_DontUseNativeDialogs`应用属性，或平台没有你所需的本地对话框，否则会显示原生文件对话框。

为了让该选项生效，你必须在更改对话框的其他属性或显示对话框之前设置它。
- `QFileDialog::ReadOnly`：`0x00000010`;表示模型为唯读。
- `QFileDialog::HideNameFilterDetails`：`0x00000020`;指示文件名过滤细节是否隐藏。
- `QFileDialog::DontUseCustomDirectoryIcons`：`0x00000040`;始终使用默认目录图标。

部分平台允许用户设置不同的图标，但自定义图标查询可能会在网络或可移动硬盘上造成显著的性能问题。

设置后，`iconProvider()`中的`DontUseCustomDirectoryIcons`选项会被启用。

该枚举值是在第5.2季度添加的。
Options 类型是 QFlags 的 typedef<Option>。它存储 Option 值的 OR 组合。

### `QFileDialog::AcceptMode acceptMode() const`

**作用与语义：**

该属性表示对话的接受模式。
动作模式定义了对话框是用于打开文件还是保存文件。
默认情况下，该属性设置为`AcceptOpen`。

**如何使用：** 调用 `acceptMode()` 读取当前值；它不会修改应用状态。

### `QString defaultSuffix() const`

**作用与语义：**

如果文件名中没有其他后缀，则添加后缀。
该属性指定了如果文件名尚未带有后缀时添加的字符串。后缀通常用于指示文件类型（例如，“txt”表示文本文件）。
如果第一个字符是点（'.'），则该字符被移除。

**如何使用：** 调用 `defaultSuffix()` 读取当前值；它不会修改应用状态。

### `QFileDialog::FileMode fileMode() const`

**作用与语义：**

该属性保留对话文件模式。
文件模式定义了用户在对话框中应选择的物品数量和类型。
默认情况下，该属性设置为`AnyFile`。
该函数设置`FileName`和`Accept` `DialogLabel`的标签。调用 setFileMode() 后可以设置自定义文本。

**如何使用：** 调用 `fileMode()` 读取当前值；它不会修改应用状态。

### `QFileDialog::Options options() const`

**作用与语义：**

该属性包含影响对话视觉和感觉的各种选项。
默认情况下，所有选项都是被禁用的。
选项（尤其是`DontUseNativeDialog`选项）应在更改对话框属性或显示对话框之前设置好。
在对话框可见时设置选项并不保证会立即对对话框产生影响（具体取决于选项和平台）。
更改其他属性后设置选项可能使这些值无效。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `void setAcceptMode(QFileDialog::AcceptMode mode)`

**作用与语义：**

该属性表示对话的接受模式。
动作模式定义了对话框是用于打开文件还是保存文件。
默认情况下，该属性设置为`AcceptOpen`。

**如何使用：** 调用 `setAcceptMode(...)` 修改 `acceptMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDefaultSuffix(const QString &suffix)`

**作用与语义：**

如果文件名中没有其他后缀，则添加后缀。
该属性指定了如果文件名尚未带有后缀时添加的字符串。后缀通常用于指示文件类型（例如，“txt”表示文本文件）。
如果第一个字符是点（'.'），则该字符被移除。

**如何使用：** 调用 `setDefaultSuffix(...)` 修改 `defaultSuffix`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFileMode(QFileDialog::FileMode mode)`

**作用与语义：**

该属性保留对话文件模式。
文件模式定义了用户在对话框中应选择的物品数量和类型。
默认情况下，该属性设置为`AnyFile`。
该函数设置`FileName`和`Accept` `DialogLabel`的标签。调用 setFileMode() 后可以设置自定义文本。

**如何使用：** 调用 `setFileMode(...)` 修改 `fileMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOptions(QFileDialog::Options options)`

**作用与语义：**

该属性包含影响对话视觉和感觉的各种选项。
默认情况下，所有选项都是被禁用的。
选项（尤其是`DontUseNativeDialog`选项）应在更改对话框属性或显示对话框之前设置好。
在对话框可见时设置选项并不保证会立即对对话框产生影响（具体取决于选项和平台）。
更改其他属性后设置选项可能使这些值无效。

**如何使用：** 调用 `setOptions(...)` 修改 `options`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSupportedSchemes(const QStringList &schemes)`

**作用与语义：**

该属性包含文件对话框应允许导航的 URL 方案。
设置该属性可以限制用户可选择的 URL 类型。这是应用程序声明其支持的获取文件内容协议的一种方式。空列表表示不施加限制（默认）。本地文件（“文件”方案）支持是隐含且始终启用的;不必将其包含在限制中。

**如何使用：** 调用 `setSupportedSchemes(...)` 修改 `supportedSchemes`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setViewMode(QFileDialog::ViewMode mode)`

**作用与语义：**

该属性决定了文件和目录在对话框中的显示方式。
默认情况下，`Detail`模式用于显示文件和目录的信息。

**如何使用：** 调用 `setViewMode(...)` 修改 `viewMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QStringList supportedSchemes() const`

**作用与语义：**

该属性包含文件对话框应允许导航的 URL 方案。
设置该属性可以限制用户可选择的 URL 类型。这是应用程序声明其支持的获取文件内容协议的一种方式。空列表表示不施加限制（默认）。本地文件（“文件”方案）支持是隐含且始终启用的;不必将其包含在限制中。

**如何使用：** 调用 `supportedSchemes()` 读取当前值；它不会修改应用状态。

### `QFileDialog::ViewMode viewMode() const`

**作用与语义：**

该属性决定了文件和目录在对话框中的显示方式。
默认情况下，`Detail`模式用于显示文件和目录的信息。

**如何使用：** 调用 `viewMode()` 读取当前值；它不会修改应用状态。

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
