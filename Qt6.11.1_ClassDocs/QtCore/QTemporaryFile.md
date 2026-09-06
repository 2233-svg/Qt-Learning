# QTemporaryFile

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 临时文件设备，负责生成唯一临时路径并在生命周期结束时按设置清理。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QTemporaryFile`：临时文件设备，负责生成唯一临时路径并在生命周期结束时按设置清理。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QTemporaryFile>`
- 继承自：QFile
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

### 状态、生命周期和线程

**生命周期：** 先设置路径或设备，再 open，成功后读写/定位/刷新，最后 close；析构通常会关闭设备，但关键写入应显式 flush/close 并检查错误。相对路径依赖当前工作目录，资源路径和用户文件路径要区分。

**状态与结果：** 区分设备未打开、打开成功、到达 EOF、暂时无数据、读写失败和写入尚未落盘。`readAll()` 方便小数据但可能占用大量内存，大文件应分块处理并检查返回值。

**线程与事件循环：** 同一个打开设备不要跨线程并发使用，除非类明确保证线程安全；后台 I/O 通过 worker 或异步设备处理，GUI 线程只接收结果。

## 3. 直接使用

构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

```cpp
QFile file(path);
if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    const QByteArray data = file.readAll();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QTemporaryFile()`
- `QTemporaryFile(QObject *parent)`
- `QTemporaryFile(const QString &templateName)`
- `QTemporaryFile(const QString &templateName, QObject *parent)`
- `(since 6.7) QTemporaryFile(const std::filesystem::path &templateName, QObject *parent = nullptr)`
- `virtual ~QTemporaryFile()`
- `bool autoRemove() const`
- `QString fileTemplate() const`
- `bool open()`
- `bool rename(const QString &newName)`
- `(since 6.7) bool rename(const std::filesystem::path &newName)`
- `(since 6.11) bool renameOverwrite(const QString &newName)`
- `(since 6.11) bool renameOverwrite(const std::filesystem::path &newName)`
- `void setAutoRemove(bool b)`
- `void setFileTemplate(const QString &templateName)`
- `(since 6.7) void setFileTemplate(const std::filesystem::path &name)`

### 重实现的公有函数

- `virtual QString fileName() const override`

### 静态公有成员

- `QTemporaryFile * createNativeFile(QFile &file)`
- `QTemporaryFile * createNativeFile(const QString &fileName)`
- `(since 6.7) QTemporaryFile * createNativeFile(const std::filesystem::path &fileName)`

### 重实现的保护函数

- `virtual bool open(QIODeviceBase::OpenMode mode) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QTemporaryFile::QTemporaryFile()`

**作用与语义：**

构建一个QTemporaryFile。
默认文件名模板由`QCoreApplication::applicationName()`返回的应用程序名确定（如果应用名为空则返回`"qt_temp"`），后接`".XXXXXX"`。文件存储在系统的临时目录中，由`QDir::tempPath()`返回。

### `[explicit] QTemporaryFile::QTemporaryFile(QObject *parent)`

**作用与语义：**

构造一个带有给定`parent`的QTemporaryFile。
默认文件名模板由应用程序名（`QCoreApplication::applicationName()`返回时确定，若应用名为空则返回`"qt_temp"`），后接`".XXXXXX"`。文件存储在系统临时目录中，由`QDir::tempPath()`返回。

### `[explicit] QTemporaryFile::QTemporaryFile(const QString &templateName)`

**作用与语义：**

构建一个以 `templateName` 为文件名模板的 QTemporaryFile。
打开临时文件后，`templateName` 将被用来创建一个唯一的文件名。
如果文件名（`templateName` 中最后一个目录路径分隔符后的部分）没有包含`"XXXXXX"`，则会自动添加。
`"XXXXXX"`将被文件名的动态部分取代，该部分被计算为唯一。
如果`templateName`是相对路径，路径将相对于当前工作目录。如果你想用系统的临时目录，可以用`QDir::tempPath()`构造`templateName`。
如果调用`rename()`函数，指定正确的目录非常重要，因为 QTemporaryFile 只能在与临时文件创建时相同的卷/文件系统内重命名文件。

### `QTemporaryFile::QTemporaryFile(const QString &templateName, QObject *parent)`

**作用与语义：**

构建一个带有指定`parent`的QTemporaryFile，并`templateName`为文件名模板。
打开临时文件后，`templateName` 将被用来创建一个唯一的文件名。
如果文件名（`templateName` 中最后一个目录路径分隔符后的部分）没有包含 `"XXXXXX"`，它会自动添加。
`"XXXXXX"` 将被文件名中的动态部分取代，该部分被计算为唯一。
如果`templateName`是相对路径，则路径相对于当前工作目录。如果你愿意，可以使用`QDir::tempPath()`构造`templateName`，使用系统的临时目录。如果调用`rename()`函数，指定正确的目录非常重要，因为QTemporaryFile只能在与临时文件创建时相同的卷/文件系统内重命名文件。

### `[explicit, since 6.7] QTemporaryFile::QTemporaryFile(const std::filesystem::path &templateName, QObject *parent = nullptr)`

**作用与语义：**

构建一个QTemporaryFile。
默认文件名模板由`QCoreApplication::applicationName()`返回的应用程序名确定（如果应用名为空则返回`"qt_temp"`），后接`".XXXXXX"`。文件存储在系统的临时目录中，由`QDir::tempPath()`返回。

### `[virtual noexcept] QTemporaryFile::~QTemporaryFile()`

**作用与语义：**

销毁临时文件对象，必要时自动关闭文件，如果处于自动删除模式，则会自动删除文件。

### `bool QTemporaryFile::autoRemove() const`

**作用与语义：**

如果 `QTemporaryFile` 处于自动删除模式，则返回 `true`。自动删除模式会在对象销毁时自动从磁盘删除文件名。这使得在栈上创建你的 `QTemporaryFile` 对象、填充数据、读取数据变得非常容易，并且在函数返回时它会自动完成自身的清理工作。自动删除默认是开启的。

### `[static] QTemporaryFile *QTemporaryFile::createNativeFile(QFile &file)`

**作用与语义：**

如果`file`还不是原生文件，则会在`QDir::tempPath()`中创建一个`QTemporaryFile`，将`file`的内容复制到其中，并返回指向临时文件的指针。如果已经是本地文件，则返回`file` `0`。

**官方示例：**

```cpp
 QFile f_pointer(":/resources/file.txt");
 QTemporaryFile::createNativeFile(f_pointer); // Returns a pointer to a temporary file

 QFile f0("/users/qt/file.txt");
 QTemporaryFile::createNativeFile(f0); // Returns 0
```

### `[static] QTemporaryFile *QTemporaryFile::createNativeFile(const QString &fileName)`

**作用与语义：**

作用于给定的`fileName`，而非现有的`QFile`对象。

### `[static, since 6.7] QTemporaryFile *QTemporaryFile::createNativeFile(const std::filesystem::path &fileName)`

**作用与语义：**

如果`file`还不是原生文件，则会在`QDir::tempPath()`中创建一个`QTemporaryFile`，将`file`的内容复制到其中，并返回指向临时文件的指针。如果已经是本地文件，则返回`file` `0`。

**官方示例：**

```cpp
 QFile f_pointer(":/resources/file.txt");
 QTemporaryFile::createNativeFile(f_pointer); // Returns a pointer to a temporary file

 QFile f0("/users/qt/file.txt");
 QTemporaryFile::createNativeFile(f0); // Returns 0
```

### `[override virtual] QString QTemporaryFile::fileName() const`

**作用与语义：**

重装：`QFile::fileName()` const.
返回支持`QTemporaryFile`对象的完整唯一文件名。该字符串在`QTemporaryFile`打开前为空，之后包含`fileTemplate()`及额外字符以实现唯一。
该方法返回的文件名是相对的，也取决于用于构造该对象的文件名模板（或传递给`setFileTemplate()`）的相对或绝对。

### `QString QTemporaryFile::fileTemplate() const`

**作用与语义：**

返回文件名模板。
该方法返回的文件名模板，根据用于构造该对象（或传递给`setFileTemplate()`）的文件名模板是相对的，会是绝对的，取决于该模板的相对或绝对。

### `bool QTemporaryFile::open()`

**作用与语义：**

在`QIODeviceBase::ReadWrite`模式下打开文件系统中唯一的临时文件。如果文件成功打开或已经打开，返回`true`。否则返回`false`。
如果第一次调用，open() 会根据 `fileTemplate()` 创建一个唯一的文件名。该文件保证是由该函数创建的（即它以前从未存在过）。
如果调用`close()`后文件被重新打开，同样的文件会再次被打开。

### `[override virtual protected] bool QTemporaryFile::open(QIODeviceBase::OpenMode mode)`

**作用与语义：**

重实现自：`QFile::open`（QIODeviceBase：：OpenMode 模式）。
在文件系统中打开一个带有`mode`标志的唯一临时文件。如果文件已成功打开或已经打开，返回`true`。否则返回`false`。
如果第一次调用，open() 会根据`fileTemplate()`创建一个唯一的文件名，并以`mode`标志打开。该文件保证是由该函数创建的（即之前从未存在过）。
如果调用`close()`后重新打开文件，该文件将再次打开并带有`mode`标志。
如果文件不存在且`mode`意味着创建它，则按照指定的`permissions`创建文件。
在POSIX系统中，实际权限受`umask`值影响。
在Windows上，这些权限是通过ACL模拟的。当该组获得的权限比其他组少时，这些ACL可能处于非规范顺序。当打开属性对话框的安全标签时，带有此类权限的文件和目录会生成警告。将所有授予他人的权限授予该组可以避免此类警告。

### `bool QTemporaryFile::rename(const QString &newName)`

**作用与语义：**

将当前临时文件重命名为`newName`，成功时返回true。
该功能与`QFile::rename()`有一个重要区别：如果低级系统调用文件重命名失败，它不会执行复制删除，这种情况可能发生在`newName`指定文件位于与临时文件创建时不同的卷或文件系统。换句话说，`QTemporaryFile`只支持原子文件重命名。
此功能旨在支持将目标文件具现化所有内容，使其他进程无法看到正在写入的未完成文件。`QSaveFile`类也可以用于类似目的，尤其是当目标文件不是临时文件时。
注意：调用 rename() 并不会禁用 `autoRemove`。如果你想让重命名的文件持续存在，必须在调用 rename() 后调用 `setAutoRemove` 并将其设置为 `false`。否则，当 `QTemporaryFile` 对象被销毁时，该文件将被删除。
如果`newName`已经存在，这个函数将失败。要替换它，可以用`renameOverwrite()`代替。

### `[since 6.7] bool QTemporaryFile::rename(const std::filesystem::path &newName)`

**作用与语义：**

将当前临时文件重命名为`newName`，成功时返回true。
该功能与`QFile::rename()`有一个重要区别：如果低级系统调用文件重命名失败，它不会执行复制删除，这种情况可能发生在`newName`指定文件位于与临时文件创建时不同的卷或文件系统。换句话说，`QTemporaryFile`只支持原子文件重命名。
此功能旨在支持将目标文件具现化所有内容，使其他进程无法看到正在写入的未完成文件。`QSaveFile`类也可以用于类似目的，尤其是当目标文件不是临时文件时。
注意：调用 rename() 并不会禁用 `autoRemove`。如果你想让重命名的文件持续存在，必须在调用 rename() 后调用 `setAutoRemove` 并将其设置为 `false`。否则，当 `QTemporaryFile` 对象被销毁时，该文件将被删除。
如果`newName`已经存在，这个函数将失败。要替换它，可以用`renameOverwrite()`代替。

### `[since 6.11] bool QTemporaryFile::renameOverwrite(const QString &newName)`

**作用与语义：**

这和`rename()`一样，只不过如果`newName`已经存在，它会原子层面地替换它，就像`QSaveFile::commit()`一样。
如果重命名无法原子方式执行（例如，临时文件和目标文件名分别存在于不同的文件系统/卷/驱动器上），返回`false`。

### `[since 6.11] bool QTemporaryFile::renameOverwrite(const std::filesystem::path &newName)`

**作用与语义：**

这和`rename()`一样，只不过如果`newName`已经存在，它会原子层面地替换它，就像`QSaveFile::commit()`一样。
如果重命名无法原子方式执行（例如，临时文件和目标文件名分别存在于不同的文件系统/卷/驱动器上），返回`false`。

### `void QTemporaryFile::setAutoRemove(bool b)`

**作用与语义：**

如果`true` `b`，会将`QTemporaryFile`设置为自动移除模式。
自动移除默认是开启的。
如果你将该属性设置为`false`，确保应用程序提供在文件不再需要时移除该文件的方法，包括将责任交给其他进程。始终使用`fileName()`函数获取名称，切勿试图猜测`QTemporaryFile`生成的名称。
在某些系统中，如果在关闭文件前未调用`fileName()`，无论该属性的状态如何，临时文件都可能被移除。不应依赖这种行为，因此应用代码应调用`fileName()`或保持自动移除功能为开启。

### `void QTemporaryFile::setFileTemplate(const QString &templateName)`

**作用与语义：**

将文件名模板设置为`templateName`。
如果文件名（`templateName` 中最后一个目录路径分隔符后的部分）没有包含 `"XXXXXX"`，则会自动添加。
`"XXXXXX"`会被文件名中的动态部分取代，该部分被计算为唯一。
如果 `templateName` 是相对路径，路径将相对于当前工作目录。如果你愿意，可以使用 `QDir::tempPath()` 构建`templateName`，使用系统的临时目录。如果调用 `rename()` 函数，指定正确的目录非常重要，因为`QTemporaryFile`只能重命名与临时文件创建时相同的卷/文件系统内的文件。

### `[since 6.7] void QTemporaryFile::setFileTemplate(const std::filesystem::path &name)`

**作用与语义：**

将文件名模板设置为`templateName`。
如果文件名（`templateName` 中最后一个目录路径分隔符后的部分）没有包含 `"XXXXXX"`，则会自动添加。
`"XXXXXX"`会被文件名中的动态部分取代，该部分被计算为唯一。
如果 `templateName` 是相对路径，路径将相对于当前工作目录。如果你愿意，可以使用 `QDir::tempPath()` 构建`templateName`，使用系统的临时目录。如果调用 `rename()` 函数，指定正确的目录非常重要，因为`QTemporaryFile`只能重命名与临时文件创建时相同的卷/文件系统内的文件。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先设置路径或设备，再 open，成功后读写/定位/刷新，最后 close；析构通常会关闭设备，但关键写入应显式 flush/close 并检查错误。相对路径依赖当前工作目录，资源路径和用户文件路径要区分。

### 状态和错误边界

区分设备未打开、打开成功、到达 EOF、暂时无数据、读写失败和写入尚未落盘。`readAll()` 方便小数据但可能占用大量内存，大文件应分块处理并检查返回值。

### 线程边界

同一个打开设备不要跨线程并发使用，除非类明确保证线程安全；后台 I/O 通过 worker 或异步设备处理，GUI 线程只接收结果。

### 最容易出现的错误

不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QTemporaryFile` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
