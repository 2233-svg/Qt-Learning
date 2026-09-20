# Qt QTemporaryFile 临时文件

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTemporaryFile>`  
> 所属模块：`Qt6::Core`  
> 继承关系：`QFile -> QTemporaryFile`  
> 类型特征：不可复制；所有成员函数可重入  
> 定位：安全创建唯一临时文件，并用 RAII 管理文件句柄和删除责任

## 它解决什么问题

临时文件看起来只是在临时目录里写一个文件，但真正麻烦的是这些边界：文件名不能撞车，不能覆盖已有文件，失败路径要清理，异常或提前返回也要关闭文件，必要时还要把写好的临时文件原子移动到正式位置。

`QTemporaryFile` 把这些事情封装到 `QFile` 子类里：

- 第一次 `open()` 时创建一个唯一文件名，并保证该文件此前不存在。
- 默认析构时自动关闭并删除临时文件。
- 继承 `QFile` 的读写能力，可直接配合 `QTextStream`、`QDataStream`、`QIODevice` API 使用。
- 提供 `rename()` 和 Qt 6.11 的 `renameOverwrite()`，支持“先写临时文件，再原子发布到目标路径”的模式。

和 `QTemporaryDir` 不同，`QTemporaryFile` 的构造函数只保存模板和父对象等状态；真正的文件创建发生在第一次 `open()`。

## 实际使用场景

- 生成下载、导出、转换、压缩过程中的中间文件。
- 把 `:/resources/...` 这类非原生文件复制成可交给只接受本地路径的系统 API 或第三方库的临时文件。
- 先把完整内容写入同一文件系统的临时文件，再用原子 rename 发布，避免其他进程看到半写入文件。
- 单元测试或工具链临时生成输入数据，并在对象离开作用域时自动清理。
- 需要一个继承自 `QFile` 的临时 I/O 设备，直接读写字节、文本或数据流。

如果你要安全保存一个长期存在的正式文件，`QSaveFile` 通常比手动组合 `QTemporaryFile + rename` 更合适；如果需要的是一组临时文件和子目录，使用 `QTemporaryDir` 更自然。

## 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QTemporaryFile>
```

qmake 工程使用：

```qmake
QT += core
```

另外，头文件里有一个实际边界：如果平台头或其他头文件已经把 `open` 定义成宏，再包含 `qtemporaryfile.h` 会报错。需要在这类环境中让 `<QTemporaryFile>` 先于定义 `open` 宏的头文件被包含。

## 最小可用示例

```cpp
#include <QTemporaryFile>

QByteArray roundTrip(const QByteArray &payload)
{
    QTemporaryFile file;
    if (!file.open()) {
        qWarning() << "cannot create temp file:" << file.errorString();
        return {};
    }

    file.write(payload);
    file.seek(0);
    return file.readAll();
} // file 析构：关闭并删除临时文件
```

文件名只有在第一次成功 `open()` 后才有定义；`file.fileName()` 在此之前返回空字符串。

## 文件模板与创建时机

默认模板位于 `QDir::tempPath()` 下，静态部分来自 `QCoreApplication::applicationName()`；应用名为空时使用 `qt_temp`，后面跟 `.XXXXXX`。

自定义模板示例：

```cpp
#include <QDir>
#include <QTemporaryFile>

QTemporaryFile file(QDir(targetDir).filePath("report.XXXXXX"));
if (!file.open())
    return false;
```

模板规则：

- 文件真正创建于第一次 `open()`，不是构造时。
- `XXXXXX` 表示动态部分，要求至少 6 个大写 `X`。
- 如果文件名部分没有 `XXXXXX`，Qt 会自动追加动态部分。
- 只考虑最后一次出现的 `XXXXXX`。
- 相对模板相对于当前工作目录，不会自动放进系统临时目录。
- 若之后要 `rename()` 到正式路径，临时文件模板应放在目标所在的同一文件系统/卷/驱动器。

`fileTemplate()` 返回模板；`fileName()` 返回实际唯一文件名。前者是计划，后者是第一次打开后才确定的结果。

## 打开、重开与 Linux 无名临时文件

公开的 `open()` 以 `QIODeviceBase::ReadWrite` 模式打开临时文件。第一次调用会基于模板创建唯一文件；文件已打开时再次调用返回 `true`；`close()` 后再次 `open()` 会重新打开同一个临时文件，而不是生成新文件。

在 Linux 上，Qt 会尝试创建无名临时文件。成功时 `open()` 返回 `true`，但在调用 `fileName()` 前，`exists()` 可能返回 `false`。一旦调用 `fileName()` 或调用了内部会取得文件名的函数，Qt 会给它物化一个名字。多数应用不需要关心这个细节，但它会影响两类代码：

- 不要用 `exists()` 判断 `open()` 是否成功；看 `open()` 的返回值和 `errorString()`。
- 若你关闭了自动删除并希望文件长期保留，应先调用 `fileName()` 取得真实名字；文档说明某些系统上如果关闭前没有调用 `fileName()`，临时文件仍可能被移除。

## 自动删除与持久化

`autoRemove` 默认开启。对象析构时会关闭文件，并删除磁盘上的临时文件名。栈对象因此非常适合短期工作。

如果要保留文件，必须显式关闭自动删除，并且使用 `fileName()` 获取实际路径：

```cpp
QTemporaryFile file;
if (!file.open())
    return {};

file.write(data);
const QString path = file.fileName();
file.setAutoRemove(false);
return path; // 调用方接管清理责任
```

关闭自动删除后，要有明确的回收策略；否则临时文件会长期留在磁盘上。

## 原子发布：rename 与 renameOverwrite

`rename(newName)` 与 `QFile::rename()` 有一个关键区别：`QTemporaryFile::rename()` 只支持底层系统调用能完成的原子重命名，不会在失败时退化成“复制再删除”。如果目标路径与临时文件不在同一文件系统、卷或驱动器，操作会失败。这是有意设计，用来避免另一个进程看到正在复制中的不完整文件。

`rename(newName)` 在目标已存在时失败。Qt 6.11 起，`renameOverwrite(newName)` 可在原子条件满足时替换已有目标。

常见模式：

```cpp
QTemporaryFile file(QDir(targetDir).filePath("settings.XXXXXX"));
if (!file.open())
    return false;

file.write(serialized);
file.flush();
file.close();

if (!file.renameOverwrite(QDir(targetDir).filePath("settings.json")))
    return false;

file.setAutoRemove(false);
return true;
```

重命名不会自动关闭 `autoRemove`。如果你希望重命名后的目标文件保留，必须在成功重命名后调用 `setAutoRemove(false)`；否则对象析构时仍会删除它。这个规则对 `renameOverwrite()` 也应按同样思路处理，因为它是 `rename()` 的“可覆盖目标”版本。

## createNativeFile 的用途

`createNativeFile()` 用于把非原生文件复制成临时原生文件。典型例子是 Qt 资源系统里的 `:/resources/file.txt`：它不是操作系统路径，许多 C API 或第三方库无法直接打开。`createNativeFile()` 会在临时目录创建一个 `QTemporaryFile`，复制内容并返回指针。

如果传入的文件已经是原生文件，它什么也不做并返回 `nullptr`。返回的 `QTemporaryFile *` 是堆对象；调用方负责删除它。因为默认 `autoRemove` 为 `true`，删除对象时临时副本会一起清理。

```cpp
QFile resource(":/schema/config.json");
std::unique_ptr<QTemporaryFile> native(
    QTemporaryFile::createNativeFile(resource));

if (native)
    passPathToLibrary(native->fileName());
```

## 线程、继承与基类边界

文档将该类标为可重入，表示多个线程可安全使用各自独立的 `QTemporaryFile` 对象。同一个对象仍然需要外部同步。它继承 `QFile`，也继承 `QObject` 的父子对象模型；带 `parent` 的构造函数适合让对象随父对象销毁。

`QTemporaryFile` 公开 `open()`，并在受保护区域重写 `open(QIODeviceBase::OpenMode)`。通常外部代码调用无参 `open()`，以读写模式创建临时文件。读写、定位、关闭、错误字符串等通用操作来自 `QFile` / `QFileDevice` / `QIODevice`。

## 常见误区

- 构造后立刻读取 `fileName()`，却忘了文件要到第一次 `open()` 才创建。
- 用 `exists()` 判断临时文件是否已经创建；Linux 无名临时文件会让这个判断失真。
- 使用相对模板时误以为它位于系统临时目录；实际上相对于当前工作目录。
- 准备用 `rename()` 发布到另一个磁盘、分区或网络卷；原子重命名会失败。
- `rename()` 成功后忘记 `setAutoRemove(false)`，导致目标文件在对象析构时被删除。
- 目标文件已存在时调用 `rename()`，却期待覆盖；应使用 Qt 6.11 的 `renameOverwrite()` 或先设计明确替换策略。
- 关闭自动删除后没有记录 `fileName()` 或安排清理。
- 忘记释放 `createNativeFile()` 返回的指针。

## 逐项 API 说明

### `QTemporaryFile()`

构造临时文件对象，使用默认模板。此时尚未创建磁盘文件；第一次成功 `open()` 后才生成唯一文件。

### `explicit QTemporaryFile(QObject *parent)`

构造带 QObject 父对象的临时文件。父对象销毁时会销毁该对象，从而按 `autoRemove` 规则关闭并删除临时文件。

### `explicit QTemporaryFile(const QString &templateName)`

以字符串模板构造对象。模板用于第一次 `open()` 时生成唯一文件名。相对模板相对于当前工作目录。

### `QTemporaryFile(const QString &templateName, QObject *parent)`

同时指定模板和父对象。适合在 QObject 生命周期内管理临时文件。

### `explicit QTemporaryFile(const std::filesystem::path &templateName, QObject *parent = nullptr)`（Qt 6.7）

接受 `std::filesystem::path` 的重载，语义等同于字符串模板版本。需要项目最低版本不低于 Qt 6.7，并且构建配置启用 C++17 filesystem 支持。

### `~QTemporaryFile()`

虚析构函数。必要时先关闭文件；若 `autoRemove()` 为 `true`，删除临时文件名。若需要知道删除是否成功，应在析构前主动调用相关文件操作并检查结果。

### `bool autoRemove() const`

返回析构时是否自动删除文件。默认值为 `true`。

### `void setAutoRemove(bool b)`

设置自动删除状态。设为 `false` 后，应用必须自行清理或把清理责任交给其他进程。若希望保留文件，应使用 `fileName()` 获取实际名字，不要猜测模板替换结果。

### `bool open()`

以 `ReadWrite` 模式打开唯一临时文件。第一次调用会创建文件；文件已打开时返回 `true`；`close()` 后再次调用会打开同一个临时文件。失败时返回 `false`，可通过 `errorString()` 查看原因。

### `bool open(QIODeviceBase::OpenMode mode)`（受保护，重写）

按指定模式打开临时文件的受保护重写。外部调用通常使用无参 `open()`；派生类和 Qt 内部会走这个接口。

### `QString fileName() const`

重写 `QFile::fileName()`。返回实际唯一文件名；第一次打开前为空。返回路径是相对还是绝对，取决于模板。

### `QString fileTemplate() const`

返回当前模板。它不是实际文件名，也不代表文件已经存在。

### `void setFileTemplate(const QString &templateName)`

设置字符串模板。应在第一次 `open()` 前设置；文件名部分没有 `XXXXXX` 时 Qt 会自动追加动态部分。若之后要原子 `rename()`，模板目录应与目标目录在同一文件系统。

### `void setFileTemplate(const std::filesystem::path &name)`（Qt 6.7）

接受 `std::filesystem::path` 的模板设置重载，语义等同于字符串版本。

### `bool rename(const QString &newName)`

把当前临时文件原子重命名为 `newName`。不会退化为复制再删除；跨文件系统或目标已存在时失败。成功后若文件要保留，应调用 `setAutoRemove(false)`。

### `bool rename(const std::filesystem::path &newName)`（Qt 6.7）

接受 `std::filesystem::path` 的重载，语义等同于字符串版本。

### `bool renameOverwrite(const QString &newName)`（Qt 6.11）

类似 `rename()`，但目标已存在时会在平台支持的情况下原子替换。无法原子完成时返回 `false`，例如临时文件与目标位于不同文件系统。

### `bool renameOverwrite(const std::filesystem::path &newName)`（Qt 6.11）

接受 `std::filesystem::path` 的覆盖式重命名重载。

### `static QTemporaryFile *createNativeFile(QFile &file)`

若 `file` 不是原生文件，复制内容到系统临时目录中的 `QTemporaryFile` 并返回新对象指针；若已经是原生文件，返回 `nullptr`。调用方拥有返回指针。

### `static QTemporaryFile *createNativeFile(const QString &fileName)`

按文件名构造 `QFile` 后执行同样逻辑。常用于资源路径或其他非原生路径。

### `static QTemporaryFile *createNativeFile(const std::filesystem::path &fileName)`（Qt 6.7）

接受 `std::filesystem::path` 的静态重载。

## API 速查表

| API | 作用 | 重点边界 |
| --- | --- | --- |
| `QTemporaryFile()` | 创建对象并保存默认模板 | 磁盘文件尚未创建 |
| `QTemporaryFile(QObject *parent)` | 绑定 QObject 父对象生命周期 | 父对象销毁会触发自动删除规则 |
| `QTemporaryFile(QString)` | 使用字符串模板 | 相对模板基于当前工作目录 |
| `QTemporaryFile(QString, QObject *)` | 同时指定模板和父对象 | 文件仍在第一次 `open()` 时创建 |
| `QTemporaryFile(std::filesystem::path, QObject *)`（Qt 6.7） | filesystem 路径模板重载 | 需要 Qt 6.7+ |
| `~QTemporaryFile()` | 关闭并按配置删除临时文件 | 默认会删除 |
| `autoRemove()` | 查询自动删除状态 | 默认 `true` |
| `setAutoRemove(bool)` | 设置是否析构删除 | 关闭后必须自行清理 |
| `open()` | 以 `ReadWrite` 创建/打开唯一临时文件 | 看返回值，不要用 `exists()` 判断 |
| `open(OpenMode)`（protected） | 指定模式打开的重写 | 外部通常不能直接调用 |
| `fileName()` | 返回实际唯一文件名 | 第一次打开前为空；Linux 可触发命名 |
| `fileTemplate()` | 返回模板 | 不是实际文件名 |
| `setFileTemplate(QString)` | 设置模板 | 通常在第一次打开前设置 |
| `setFileTemplate(std::filesystem::path)`（Qt 6.7） | filesystem 模板重载 | 需要 Qt 6.7+ |
| `rename(QString)` | 原子重命名到目标 | 目标存在或跨文件系统会失败 |
| `rename(std::filesystem::path)`（Qt 6.7） | filesystem 重命名重载 | 语义同字符串版本 |
| `renameOverwrite(QString)`（Qt 6.11） | 原子替换目标 | 无法原子替换时失败 |
| `renameOverwrite(std::filesystem::path)`（Qt 6.11） | filesystem 覆盖式重命名重载 | 需要 Qt 6.11+ |
| `createNativeFile(QFile &)` | 非原生文件复制成临时原生文件 | 返回指针由调用方删除；原生文件返回 `nullptr` |
| `createNativeFile(QString)` | 按名称创建原生临时副本 | 常用于 Qt 资源路径 |
| `createNativeFile(std::filesystem::path)`（Qt 6.7） | filesystem 静态重载 | 需要 Qt 6.7+ |

## 一句话总结

`QTemporaryFile` 是带唯一命名、自动清理和原子发布能力的 `QFile`；正确使用的关键是记住“第一次 `open()` 才创建文件”、保留文件时关闭 `autoRemove`，以及把 `rename()`/`renameOverwrite()` 限定在同一文件系统内。
