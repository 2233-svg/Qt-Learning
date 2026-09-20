# Qt QTemporaryDir 临时目录

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTemporaryDir>`  
> 所属模块：`Qt6::Core`  
> 类型特征：不可复制，Qt 6.4 起可移动；所有成员函数可重入  
> 定位：安全创建唯一目录，并用 RAII 管理整棵临时目录树的清理

## 它解决什么问题

很多操作需要一块短期、互不冲突的磁盘空间，例如解压缩、生成中间文件、准备外部进程输入、运行测试或分阶段导出。如果自己用时间戳、进程号或随机数拼目录名，仍可能碰撞，还要手动处理创建失败和异常路径上的清理。

`QTemporaryDir` 把这些问题合并成一个对象：

- 构造对象时立即创建一个唯一目录，不覆盖已有目录。
- 通过 `isValid()` 明确报告创建是否成功。
- 默认在对象析构时递归删除目录及其全部内容。
- 可根据模板控制目录所在位置和静态名称部分。

它最重要的语义是“构造即创建”，这和 `QTemporaryFile` 的“第一次 `open()` 才创建文件”不同。

## 实际使用场景

- 解压压缩包到隔离目录，校验成功后再把需要的文件移动到目标位置。
- 调用只接受文件路径的第三方库或外部程序，临时生成输入、输出和日志文件。
- 单元测试为每个用例准备独立文件树，并在用例退出时自动清理。
- 安装器、转换器、编译器前端先在临时目录完成多阶段工作，避免污染正式目录。
- GUI 程序生成预览、缩略图或一次性缓存。

如果只需要一个临时文件，使用 `QTemporaryFile`。如果目标是安全替换正式文件，优先考虑 `QSaveFile`，而不是自己用临时目录模拟提交协议。

## 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QTemporaryDir>
```

qmake 工程使用：

```qmake
QT += core
```

## 最小可用示例

```cpp
#include <QFile>
#include <QTemporaryDir>

bool buildPreview()
{
    QTemporaryDir dir;
    if (!dir.isValid()) {
        qWarning() << "cannot create temporary directory:"
                   << dir.errorString();
        return false;
    }

    QFile manifest(dir.filePath("manifest.json"));
    if (!manifest.open(QIODevice::WriteOnly | QIODevice::Truncate))
        return false;

    manifest.write(R"({"temporary":true})");
    return true;
} // manifest 先析构；随后 dir 析构并递归删除目录
```

局部对象的声明顺序很实用：先声明 `QTemporaryDir`，再声明使用该目录的文件对象，这样离开作用域时文件会先关闭，目录再清理。

## 目录模板

### 默认模板

默认构造函数把目录建在 `QDir::tempPath()` 下。静态名称部分来自 `QCoreApplication::applicationName()`；应用名为空时使用 `qt_temp`。Qt 会追加随机部分保证名称唯一。

### 自定义模板

```cpp
#include <QDir>
#include <QTemporaryDir>

QTemporaryDir dir(
    QDir(QDir::tempPath()).filePath("image-import-XXXXXX"));
```

只有模板末尾的 `XXXXXX` 会作为动态部分。若模板不以 `XXXXXX` 结尾，Qt 会自动在末尾追加动态部分。`QTemporaryDir` 不支持把 `XXXXXX` 放在模板中间；这一点和 `QTemporaryFile` 不同。

相对模板相对于进程当前工作目录，而不是自动相对于系统临时目录。服务、插件、测试框架和桌面快捷方式启动的程序，其当前目录可能与你预想的不一样。需要系统临时目录时，应明确与 `QDir::tempPath()` 拼接；需要稳定项目目录时，应传绝对路径。

## 生命周期与所有权

`QTemporaryDir` 默认开启自动删除。对象析构时会删除目录及其所有内容，所以最自然的用法是栈对象。只要控制对象作用域，就同时控制临时目录寿命。

```cpp
QString producePersistentBundle()
{
    QTemporaryDir dir;
    if (!dir.isValid())
        return {};

    // 写入 dir.path() 下的内容……

    dir.setAutoRemove(false);
    return dir.path(); // 调用方现在必须负责最终清理
}
```

关闭自动删除意味着把磁盘清理责任移交给应用或另一个进程。不要只是为了调试长期关闭它而不设计回收策略，否则临时目录会持续积累。

`remove()` 可以提前递归删除目录。删除可能因仍有文件打开、权限不足、杀毒软件或其他进程占用而失败；必须检查返回值。

## 路径 API 的边界

`path()` 返回实际创建出的唯一目录路径；创建失败时返回空字符串。路径是相对还是绝对，取决于构造时的模板。

`filePath(fileName)` 只是把名称拼到临时目录路径下：

- 不检查目标文件是否存在。
- 不创建文件或子目录。
- 不清理重复分隔符、`.` 或 `..`。
- 不接受绝对路径。
- 返回路径的相对/绝对属性跟随临时目录模板。

因此，不要把不可信输入直接交给 `filePath()`：

```cpp
const QString candidate = dir.filePath(userSuppliedName);
```

如果 `userSuppliedName` 含有 `../`，拼出的路径可能逃出临时目录。需要接收外部名称时，应先限制为纯文件名，拒绝路径分隔符和 `.` / `..`，并在清理后验证最终绝对路径仍位于 `dir.path()` 下。

## 失败处理与线程边界

构造后第一件事应当是调用 `isValid()`。不要用 `QDir(dir.path()).exists()` 替代：创建失败时 `path()` 为空，而默认构造的 `QDir` 代表当前目录，当前目录通常存在，容易得到错误的成功判断。

创建失败时，`errorString()` 给出原因；创建成功时返回空字符串。常见失败包括模板父目录不存在、没有写权限、磁盘或文件系统错误。

文档将该类标为可重入，含义是多个线程可以操作各自独立的 `QTemporaryDir` 对象。它不意味着同一个对象可被多个线程无同步并发读写，也不意味着目录中的文件天然具备并发安全性。

## 移动语义

Qt 6.4 起支持移动构造、移动赋值和 `swap()`。移动会把目录管理责任转移给新对象。被移动对象处于 partially-formed 状态，只能析构或重新赋值，不能再调用 `path()`、`isValid()` 等普通成员。

```cpp
QTemporaryDir makeWorkspace()
{
    QTemporaryDir dir;
    return dir; // 移动或返回值消除
}
```

移动赋值还会替换目标对象原来管理的状态。若目标对象原本持有另一个自动删除目录，其旧状态在赋值过程中会按对象生命周期规则被释放；不要在外部仍依赖旧路径时贸然覆盖对象。

## 常见误区

- 构造后直接使用 `path()`，没有先检查 `isValid()`。
- 用 `QDir::exists()` 判断临时目录创建是否成功。
- 认为自定义相对模板仍会放到 `QDir::tempPath()`；实际上它相对于当前工作目录。
- 把 `XXXXXX` 放在模板中间，期望它被替换；`QTemporaryDir` 只识别末尾动态段。
- 认为 `filePath()` 会规范化路径或阻止 `..` 越界；它只是路径拼接辅助函数。
- `setAutoRemove(false)` 后没有安排清理责任。
- 目录中仍有打开文件、外部进程仍在使用文件时调用 `remove()` 或让对象析构，并忽略删除失败。
- 移动对象后继续使用源对象。

## 逐项 API 说明

### `QTemporaryDir()`

立即在 `QDir::tempPath()` 下创建唯一目录。模板静态部分来自应用名，应用名为空时使用 `qt_temp`。构造后必须检查 `isValid()`。

### `explicit QTemporaryDir(const QString &templatePath)`

按模板立即创建唯一目录。相对模板相对于当前工作目录；末尾 `XXXXXX` 是动态段，不存在时会自动追加。模板中间的 `XXXXXX` 不受支持。

### `QTemporaryDir(QTemporaryDir &&other)`（Qt 6.4）

转移 `other` 管理的目录和自动删除责任。源对象之后只能析构或重新赋值。

### `~QTemporaryDir()`

销毁管理对象。若 `autoRemove()` 为 `true`，会递归删除临时目录及其全部内容。析构没有可供调用方检查的返回值；若必须知道清理是否成功，应在析构前显式调用 `remove()`。

### `bool isValid() const`

返回构造时是否成功创建目录。它是创建结果的权威检查方式。

### `QString errorString() const`

创建失败时返回错误说明；创建成功时返回空字符串。它描述的是目录创建错误，不是所有后续文件操作的统一错误通道。

### `QString path() const`

返回实际创建的唯一目录路径；创建失败时为空。返回相对路径还是绝对路径，由模板决定。

### `QString filePath(const QString &fileName) const`

返回目录内候选文件的拼接路径。它不检查存在性、不创建文件、不清理 `.` / `..`，并且不允许绝对 `fileName`。不要直接传入不可信路径片段。

### `bool autoRemove() const`

返回析构时是否自动删除目录。默认值为 `true`。

### `void setAutoRemove(bool b)`

开启或关闭析构自动删除。设为 `false` 后，调用方必须明确接管清理责任。

### `bool remove()`

立即递归删除临时目录及全部内容，成功返回 `true`。调用前应关闭目录中的文件并结束使用该目录的外部进程。

### `void swap(QTemporaryDir &other)`（Qt 6.4）

常量时间交换两个对象管理的目录状态，`noexcept`。交换后，每个对象会在析构时处理对方原先管理的目录。

### `QTemporaryDir &operator=(QTemporaryDir &&other)`（Qt 6.4）

把 `other` 的目录管理状态移动到当前对象；源对象进入只能析构或重新赋值的状态。返回当前对象。

## API 速查表

| API | 作用 | 重点边界 |
| --- | --- | --- |
| `QTemporaryDir()` | 在系统临时目录立即创建唯一目录 | 构造后检查 `isValid()` |
| `QTemporaryDir(templatePath)` | 按模板立即创建唯一目录 | 相对路径基于 CWD；只识别末尾 `XXXXXX` |
| 移动构造（Qt 6.4） | 转移目录管理权 | 源对象只能析构或重新赋值 |
| `~QTemporaryDir()` | 按配置自动递归删除目录 | 默认删除全部内容；无法读取析构清理结果 |
| `isValid()` | 查询创建是否成功 | 不要用 `QDir::exists()` 替代 |
| `errorString()` | 获取创建失败原因 | 成功时为空 |
| `path()` | 获取实际唯一目录路径 | 创建失败为空；相对/绝对跟随模板 |
| `filePath(name)` | 拼接目录内路径 | 不校验存在性，不清理 `.` / `..`，拒绝绝对路径 |
| `autoRemove()` | 查询自动删除状态 | 默认 `true` |
| `setAutoRemove(bool)` | 配置析构时是否删除 | 关闭后必须自行回收 |
| `remove()` | 立即递归删除目录树 | 检查返回值，先关闭占用文件 |
| `swap()`（Qt 6.4） | 交换两个对象的管理状态 | 快速且 `noexcept` |
| 移动赋值（Qt 6.4） | 用另一个对象的状态替换当前状态 | 源对象进入 partially-formed 状态 |

## 一句话总结

`QTemporaryDir` 用“构造即创建、析构即清理”的 RAII 模型提供唯一工作目录；正确使用的关键是立即检查 `isValid()`、明确模板相对路径含义，并把 `filePath()` 当作普通拼接函数而不是路径安全检查器。
