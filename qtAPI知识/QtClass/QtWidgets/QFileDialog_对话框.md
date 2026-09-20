# Qt QFileDialog 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QFileDialog>`
> 所属模块：`Qt6::Widgets`
> 继承：`QDialog -> QFileDialog`
> 常见搭档：`QFileDialog::getOpenFileName()`、`QSettings`、`QAbstractProxyModel`

## 1. QFileDialog 解决什么问题

`QFileDialog` 是标准文件选择对话框。它用来让用户选择：

- 一个或多个文件；
- 一个目录；
- 保存路径；
- 远程 URL；
- 在某些平台上还可以直接接触到浏览器/原生选择器的行为。

它解决的不是“怎么读写文件”，而是“怎么让用户选对文件或目录”。真正的 I/O 还是交给 `QFile`、`QSaveFile`、`QTextStream`、网络请求等类。

## 2. 最小可用代码

```cpp
#include <QApplication>
#include <QFileDialog>
#include <QPushButton>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QPushButton button("打开文件");
    QObject::connect(&button, &QPushButton::clicked, [&] {
        QString file = QFileDialog::getOpenFileName(
            &button, QObject::tr("打开图片"), QString(),
            QObject::tr("Images (*.png *.jpg *.bmp)"));
        if (!file.isEmpty())
            qDebug() << file;
    });

    button.show();
    return app.exec();
}
```

静态函数是 `QFileDialog` 最常见的用法；如果只想让用户选一下路径，往往比自己 new 一个对话框更直接。

## 3. 先分清三件事

### 3.1 `fileMode`

```cpp
dialog.setFileMode(QFileDialog::ExistingFile);
```

它决定“用户能选什么”：

- `AnyFile`：任意文件名，存在与否都行；
- `ExistingFile`：单个已存在文件；
- `Directory`：目录；
- `ExistingFiles`：多个已存在文件。

### 3.2 `acceptMode`

```cpp
dialog.setAcceptMode(QFileDialog::AcceptOpen);
dialog.setAcceptMode(QFileDialog::AcceptSave);
```

它决定对话框更像“打开”还是“保存”。  
保存模式下，`defaultSuffix` 往往很重要，因为它会补默认扩展名。

### 3.3 `viewMode`

```cpp
dialog.setViewMode(QFileDialog::Detail);
dialog.setViewMode(QFileDialog::List);
```

`Detail` 更适合看文件信息，`List` 更简洁。  
默认是 `Detail`。

## 4. 目录、过滤器和预选

```cpp
dialog.setDirectory("/home/user");
dialog.selectFile("report.txt");
dialog.setNameFilter("Images (*.png *.jpg *.bmp)");
dialog.setNameFilters({"Images (*.png *.jpg)", "All Files (*)"});
dialog.setMimeTypeFilters({"image/jpeg", "image/png"});
```

- `setDirectory()`：指定初始目录；
- `selectFile()`：预先选中文件；
- `setNameFilter()` / `setNameFilters()`：按文件名通配；
- `setMimeTypeFilters()`：按 MIME 类型过滤，更适合现代格式判断。

`selectedFiles()` 返回的是绝对路径列表。  
如果当前不是多选模式，它通常还是一个路径。

## 5. URL、远程 scheme 和平台差异

```cpp
dialog.setSupportedSchemes({"sftp", "ftp"});
dialog.setDirectoryUrl(QUrl("file:///home/user"));
```

`supportedSchemes` 用来限制用户能导航到哪些 URL scheme。  
`file` scheme 是隐式支持的，不用手动加。

URL 版静态函数包括：

- `getOpenFileUrl()`
- `getOpenFileUrls()`
- `getSaveFileUrl()`
- `getExistingDirectoryUrl()`

如果平台不支持远程文件选择，Qt 会回退到本地文件行为。

## 6. options 里最值得记的

```cpp
dialog.setOption(QFileDialog::DontUseNativeDialog, true);
dialog.setOption(QFileDialog::DontResolveSymlinks, true);
dialog.setOption(QFileDialog::DontConfirmOverwrite, true);
```

常见选项：

- `ShowDirsOnly`：只显示目录；
- `DontResolveSymlinks`：不要自动解析符号链接；
- `DontConfirmOverwrite`：保存时不确认覆盖；
- `DontUseNativeDialog`：强制使用 Qt 自绘对话框；
- `ReadOnly`：只读浏览；
- `HideNameFilterDetails`：隐藏过滤器细节；
- `DontUseCustomDirectoryIcons`：不要自定义目录图标。

如果你要用 Qt 自己的布局、itemDelegate 或代理模型，通常得先设置 `DontUseNativeDialog`。原生对话框在很多平台上不会暴露这些 widget 级 API。

## 7. 事件和结果

```cpp
connect(&dialog, &QFileDialog::fileSelected, [](const QString &file) {
    qDebug() << file;
});
```

常用信号：

- `currentChanged`
- `directoryEntered`
- `fileSelected`
- `filesSelected`
- `currentUrlChanged`
- `directoryUrlEntered`
- `urlSelected`
- `urlsSelected`
- `filterSelected`

它们的用途很直接：显示当前浏览位置、在接受时拿结果、同步 UI 状态。

`open(QObject *receiver, const char *member)` 会把文件选择结果连接到槽函数：

- 单选时走 `fileSelected()`
- 多选时走 `filesSelected()`

这比自己接 `accepted()` 再手动取值更顺手。

## 8. 保存状态和自定义代理

```cpp
dialog.setHistory({"C:/", "D:/Projects"});
dialog.setSidebarUrls({QUrl::fromLocalFile("C:/"), QUrl::fromLocalFile("D:/")});

QByteArray state = dialog.saveState();
dialog.restoreState(state);
```

`saveState()` / `restoreState()` 可以保住对话框的内部状态，比如历史和部分布局信息。  
适合把用户上次的浏览习惯保留下来。

```cpp
dialog.setProxyModel(new QSortFilterProxyModel);
dialog.setItemDelegate(new QStyledItemDelegate);
```

- `setProxyModel()`：可以过滤、加列或改浏览逻辑，且 **QFileDialog 会接管代理模型所有权**；
- `setItemDelegate()`：只替换委托，**不接管所有权**。

这个差别要记牢。

## 9. 什么时候用静态函数，什么时候 new 一个对象

静态函数适合：

- 一次性选文件；
- 代码最短；
- 不关心对话框内部状态。

显式创建对象适合：

- 需要预设目录、筛选器、代理模型；
- 需要保存状态；
- 需要响应 `currentChanged` / `filterSelected`；
- 需要 `open()` 异步打开。

## API 速查表
### 10.1 枚举和属性

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `ViewMode` | 定义文件视图是详细列表还是简单列表。 | 只影响浏览器外观，不改变选择语义。 |
| 枚举值 | `ViewMode::Detail` | 显示文件名、大小等更多信息。 | 适合需要比较文件信息的场景。 |
| 枚举值 | `ViewMode::List` | 用更紧凑的列表展示文件。 | 文件很多或对话框较窄时更省空间。 |
| 类型 | `FileMode` | 定义用户可以选择文件、目录、单个还是多个。 | 它决定选择结果形态，是配置对话框的第一步。 |
| 枚举值 | `FileMode::AnyFile` | 允许选择任意文件名，文件可以尚不存在。 | 保存对话框最常用。 |
| 枚举值 | `FileMode::ExistingFile` | 只允许选择一个已存在文件。 | 单文件打开场景。 |
| 枚举值 | `FileMode::Directory` | 选择目录。 | 目录选择器通常配合 `ShowDirsOnly`。 |
| 枚举值 | `FileMode::ExistingFiles` | 选择多个已存在文件。 | 批量导入、批量处理。 |
| 类型 | `AcceptMode` | 定义对话框是打开资源还是保存资源。 | 影响确认按钮语义和覆盖提示。 |
| 枚举值 | `AcceptMode::AcceptOpen` | 打开模式。 | 适合读取已有文件或目录。 |
| 枚举值 | `AcceptMode::AcceptSave` | 保存模式。 | 配合 `defaultSuffix` 和覆盖确认。 |
| 属性 | `acceptMode() const` / `setAcceptMode(AcceptMode mode)` | 读取或设置打开/保存模式。 | 先确定保存还是打开，再设计其他选项。 |
| 属性 | `fileMode() const` / `setFileMode(FileMode mode)` | 读取或设置可选资源类型。 | `ExistingFiles` 的结果必须用 `selectedFiles()` 列表处理。 |
| 属性 | `defaultSuffix() const` / `setDefaultSuffix(const QString &suffix)` | 读取或设置保存时默认补充的后缀。 | 后缀不要带点更稳妥，例如 `txt`。 |
| 选项 | `options() const` / `setOptions(Options options)` | 批量读取或设置对话框行为选项。 | 需要自定义代理、委托时通常先打开 `DontUseNativeDialog`。 |
| URL | `supportedSchemes() const` / `setSupportedSchemes(const QStringList &schemes)` | 限制文件对话框允许导航的 URL scheme。 | `file` scheme 隐式支持；远程 scheme 是否可用还取决于平台。 |
| 属性 | `viewMode() const` / `setViewMode(ViewMode mode)` | 读取或设置详细/列表浏览模式。 | 原生对话框可能不完全遵守 Qt 视图细节。 |
| 历史 | `history() const` / `setHistory(const QStringList &paths)` | 读取或设置最近浏览路径。 | 适合保存用户习惯，但不要无限累积。 |
| 侧边栏 | `sidebarUrls() const` / `setSidebarUrls(const QList<QUrl> &urls)` | 读取或设置侧边栏快捷位置。 | 路径变化后要考虑清理失效 URL。 |

### 10.2 常用函数

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QFileDialog(QWidget *parent, Qt::WindowFlags f)` | 创建文件选择对话框。 | 适合需要逐项配置的对象式用法。 |
| 构造 | `QFileDialog(QWidget *parent, const QString &caption, const QString &directory, const QString &filter)` | 创建并设置标题、初始目录和名称过滤器。 | 快速搭建对象式对话框。 |
| 目录 | `directory() const` / `setDirectory(const QString &directory)` | 读取或设置当前本地目录。 | 路径应尽量使用绝对路径；远程 URL 用 `directoryUrl()`。 |
| 目录 | `directoryUrl() const` / `setDirectoryUrl(const QUrl &directory)` | 读取或设置当前 URL 目录。 | 支持远程 scheme 时使用。 |
| 预选 | `selectFile(const QString &filename)` | 预先选中或填入一个本地文件名。 | 保存对话框里常用于填默认文件名。 |
| 结果 | `selectedFiles() const` | 读取用户选择的本地路径列表。 | 单选也返回列表；先判断为空。 |
| 预选 | `selectUrl(const QUrl &url)` | 预先选中某个 URL。 | URL 版对象式对话框使用。 |
| 结果 | `selectedUrls() const` | 读取用户选择的 URL 列表。 | 远程资源选择不要只读 `selectedFiles()`。 |
| 过滤 | `setNameFilter(const QString &filter)` / `setNameFilters(const QStringList &filters)` | 设置文件名通配符过滤器。 | 例如 `Images (*.png *.jpg)`；多个过滤器让用户切换。 |
| 过滤 | `nameFilters() const` | 查询当前文件名过滤器列表。 | 调试或保存用户上次选择时使用。 |
| 过滤 | `setMimeTypeFilters(...)` / `mimeTypeFilters() const` | 按 MIME 类型过滤文件。 | 比文件名后缀更适合格式语义判断，但受 MIME 数据库支持影响。 |
| 过滤 | `selectNameFilter(...)` / `selectedNameFilter() const` | 预选或读取当前名称过滤器。 | 保存用户上次选择的格式时有用。 |
| 过滤 | `selectMimeTypeFilter(...)` / `selectedMimeTypeFilter() const` | 预选或读取当前 MIME 过滤器。 | 和 MIME 过滤器列表配套。 |
| 目录过滤 | `filter() const` / `setFilter(QDir::Filters filters)` | 控制文件对话框显示哪些文件系统条目。 | 可进一步限制隐藏文件、目录等。 |
| 状态 | `saveState() const` / `restoreState(const QByteArray &state)` | 保存或恢复对话框内部浏览状态。 | 恢复失败要允许使用默认状态继续。 |
| 委托 | `setItemDelegate(QAbstractItemDelegate *delegate)` / `itemDelegate() const` | 替换文件视图的 item delegate。 | 不接管 delegate 所有权；原生对话框下可能不生效。 |
| 图标 | `setIconProvider(QAbstractFileIconProvider *provider)` / `iconProvider() const` | 设置文件和目录图标提供者。 | 自定义 provider 的生命周期要单独管理。 |
| 文本 | `setLabelText(DialogLabel label, const QString &text)` / `labelText(...) const` | 修改对话框内固定标签和按钮文字。 | 本地化或业务术语定制时使用。 |
| 代理 | `setProxyModel(QAbstractProxyModel *model)` / `proxyModel() const` | 用代理模型过滤、扩展或重排文件视图。 | `QFileDialog` 会接管代理模型所有权；通常需关闭原生对话框。 |
| 选项 | `setOption(Option option, bool on = true)` / `testOption(Option option) const` | 开关或查询单个对话框选项。 | `DontUseNativeDialog` 是自定义内部视图时最关键的选项。 |
| 异步打开 | `open(QObject *receiver, const char *member)` | 非阻塞打开并把结果信号连接到旧式槽。 | 单选和多选会走不同结果信号，槽签名要匹配。 |
| 显示 | `setVisible(bool visible)` | 控制对话框是否显示。 | 对象式用法可以配合 `open()` 或 `show()`，不要和静态函数混用。 |

### 10.3 静态函数和信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 静态选择 | `getOpenFileName(...)` | 一次性选择一个本地文件。 | 返回空字符串表示取消；适合最短代码路径。 |
| 静态选择 | `getOpenFileNames(...)` | 一次性选择多个本地文件。 | 返回空列表表示取消；结果是绝对路径列表。 |
| 静态选择 | `getOpenFileUrl(...)` | 一次性选择一个 URL 资源。 | 适合需要支持远程 scheme 的场景。 |
| 静态选择 | `getOpenFileUrls(...)` | 一次性选择多个 URL 资源。 | 支持能力取决于平台和 scheme。 |
| 静态保存 | `getSaveFileName(...)` | 一次性选择本地保存路径。 | 配合默认后缀和覆盖确认。 |
| 静态保存 | `getSaveFileUrl(...)` | 一次性选择 URL 保存位置。 | 适合远程保存或平台文件服务。 |
| 静态目录 | `getExistingDirectory(...)` | 一次性选择本地目录。 | 取消时返回空字符串。 |
| 静态目录 | `getExistingDirectoryUrl(...)` | 一次性选择 URL 目录。 | 远程目录能力受平台支持限制。 |
| WebAssembly | `getOpenFileContent(...)` | 让用户选文件并通过回调取得内容。 | 适合浏览器环境，回调里的内容由调用者处理。 |
| WebAssembly | `saveFileContent(...)` | 让平台保存一段内存内容。 | 适合浏览器下载流程，不等同于桌面 `QFile` 写盘。 |
| 信号 | `currentChanged(const QString &path)` | 当前浏览文件变化时通知。 | 本地文件浏览；不要把它当作最终选择。 |
| 信号 | `currentUrlChanged(const QUrl &url)` | 当前浏览 URL 变化时通知。 | URL 版浏览状态联动。 |
| 信号 | `directoryEntered(const QString &directory)` | 用户进入本地目录时通知。 | 可更新面包屑、权限提示或异步加载。 |
| 信号 | `directoryUrlEntered(const QUrl &directory)` | 用户进入 URL 目录时通知。 | 远程目录导航联动。 |
| 信号 | `fileSelected(const QString &file)` | 用户确认单个本地文件时通知。 | 单选打开/保存结果入口。 |
| 信号 | `filesSelected(const QStringList &files)` | 用户确认多个本地文件时通知。 | 多选批处理入口。 |
| 信号 | `urlSelected(const QUrl &url)` | 用户确认单个 URL 时通知。 | URL 资源单选入口。 |
| 信号 | `urlsSelected(const QList<QUrl> &urls)` | 用户确认多个 URL 时通知。 | URL 批量处理入口。 |
| 信号 | `filterSelected(const QString &filter)` | 用户切换文件过滤器时通知。 | 可以保存用户最后选择的格式。 |

### 一句话总结

`QFileDialog` 的重点不是“弹一个对话框”，而是把“用户能选什么、默认去哪、用本地还是原生、结果怎么取”这些事一次讲清楚。
