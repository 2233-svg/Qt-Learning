# Qt QLibrary 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QLibrary>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject`  
> 相关类型：`QFunctionPointer`、`QLibrary::LoadHint`、`QLibrary::LoadHints`

## 1. 先给结论：它解决什么问题

`QLibrary` 用于在程序运行期间**动态加载共享库，并按导出名称解析其中的函数符号**。

它解决的是显式链接场景：

```text
程序启动
  -> 根据文件名查找共享库
  -> 运行时加载共享库
  -> 按符号名取得函数地址
  -> 转换为约定好的函数指针类型
  -> 调用函数
```

典型用途包括：

- 可选功能：只有用户安装了某个后端库时才启用对应功能；
- 插件或扩展模块：主程序不需要在链接阶段依赖所有实现；
- 平台适配：Windows、Linux、macOS 使用不同的动态库文件；
- 第三方库的运行时探测：库不存在时，程序仍可运行并给出降级行为；
- ABI 隔离：通过稳定的 C 导出函数作为模块边界。

它不负责：

- 自动生成插件接口；
- 检查导出函数参数是否和调用方声明一致；
- 解决 C++ 名字改编或 ABI 不兼容；
- 把任意动态库转换成 `QObject` 插件；
- 替代构建阶段的普通链接；
- 管理动态库内部对象的生命周期。

如果目标是 Qt 插件，通常还要比较 `QLibrary` 和 `QPluginLoader`：`QLibrary` 更底层，面向“文件 + 导出符号”；`QPluginLoader` 面向 Qt 插件元数据和插件实例。

## 2. 最小工作模型

一个 `QLibrary` 对象描述一个共享库文件。最常见的调用顺序是：

```cpp
#include <QLibrary>

using InitializeFunction = bool (*)(int);

QLibrary library(QStringLiteral("mybackend"));
const auto symbol = library.resolve("initialize");

if (!symbol) {
    qWarning().noquote() << library.errorString();
    return false;
}

const auto initialize = reinterpret_cast<InitializeFunction>(symbol);
return initialize(1);
```

这里有几个必须同时成立的前提：

1. `mybackend` 能按当前平台的查找规则定位到目标库；
2. 目标库确实导出了名为 `initialize` 的符号；
3. 导出函数的调用约定、参数、返回值和调用方的函数指针类型完全一致；
4. 函数不会在库被卸载后继续被调用。

`resolve()` 会在需要时隐式调用 `load()`，所以这个例子不必先显式调用 `load()`。如果希望在进入业务逻辑前就确认库能否加载，可以把加载步骤拆开。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QLibrary>
```

### 3.3 qmake

```qmake
QT += core
```

动态库本身不需要在主程序的链接命令中作为普通链接输入。主程序链接的是 Qt Core，而目标库由 `QLibrary` 在运行时查找和加载。

## 4. 实际使用场景

### 4.1 可选后端

主程序可以先加载某个后端库；加载失败时选择内置实现：

```cpp
QLibrary backend(QStringLiteral("image_backend"));

if (!backend.load()) {
    qWarning().noquote() << "Use built-in backend:" << backend.errorString();
    return useBuiltInBackend();
}

using CreateFunction = Backend * (*)();
const auto symbol = backend.resolve("backend_create");
if (!symbol) {
    qWarning().noquote() << backend.errorString();
    return useBuiltInBackend();
}

const auto create = reinterpret_cast<CreateFunction>(symbol);
return useBackend(create());
```

真正的接口通常还需要 `destroy`、版本查询和错误码函数。只解析一个创建函数并不等于已经建立了完整的模块契约。

### 4.2 平台相关库名

推荐使用不带平台后缀的基本名称：

```cpp
QLibrary library(QStringLiteral("graphics_backend"));
```

Qt 会根据平台尝试相应的前缀和后缀，例如：

- Unix/Linux：通常涉及 `lib` 前缀和 `.so` 后缀；
- macOS/iOS：通常涉及 `.dylib`、`.bundle` 或 `.so`；
- Windows：通常涉及 `.dll`。

这样同一段代码可以使用平台对应的库文件名，而不用把 `.dll`、`.so` 或 `.dylib` 写死在业务代码中。

### 4.3 版本化共享库

如果平台的库命名或加载机制支持版本信息，可以使用带版本的构造函数或 `setFileNameAndVersion()`：

```cpp
QLibrary library;
library.setFileNameAndVersion(QStringLiteral("mylib"),
                              QStringLiteral("1.2.3"));
```

也可以只指定主版本号：

```cpp
library.setFileNameAndVersion(QStringLiteral("mylib"), 1);
```

版本参数在 Windows 上会被忽略。不要把它当作跨平台、强制性的 ABI 版本验证机制；需要可靠版本协商时，应额外解析版本函数或元数据。

### 4.4 直接调用 C 导出函数

C++ 编译器会对函数名进行名字改编。为了让 `resolve("...")` 使用稳定名称，动态库一侧通常使用 `extern "C"`：

```cpp
extern "C" int backend_version()
{
    return 3;
}
```

Windows 上还需要让符号导出，例如：

```cpp
#ifdef Q_OS_WIN
#  define BACKEND_EXPORT __declspec(dllexport)
#else
#  define BACKEND_EXPORT
#endif

extern "C" BACKEND_EXPORT int backend_version()
{
    return 3;
}
```

调用方必须使用完全匹配的函数指针类型：

```cpp
using VersionFunction = int (*)();
const auto version =
    reinterpret_cast<VersionFunction>(library.resolve("backend_version"));
```

`QLibrary` 不会检查这些类型是否匹配。错误的原型、调用约定或结构体布局可能导致未定义行为。

## 5. 对象、库句柄和加载状态

### 5.1 `QLibrary` 是一个 QObject

`QLibrary` 继承自 `QObject`，因此可以指定 parent：

```cpp
auto *library = new QLibrary(QStringLiteral("mylib"), owner);
```

也可以使用栈对象：

```cpp
QLibrary library(QStringLiteral("mylib"));
```

类是不可复制的。头文件通过 `Q_DISABLE_COPY(QLibrary)` 禁止复制构造和复制赋值；如果需要在多个位置访问同一个库，应共享一个明确的管理对象，或分别创建 `QLibrary` 实例并理解底层库的共享加载规则。

### 5.2 一个物理库可以对应多个实例

多个 `QLibrary` 对象可以访问同一个物理共享库。底层平台通常会复用已加载的库，但每个 `QLibrary` 对象仍有自己的配置和加载状态。

卸载时要特别注意：

- 某个实例调用 `unload()` 不一定能立即从进程地址空间卸载库；
- 如果其他 `QLibrary` 实例仍在使用同一个库，卸载会失败；
- 只有所有相关实例都释放使用关系后，底层库才可能真正卸载；
- macOS 上动态库不能被卸载，`unload()` 可能返回 `true`，但库仍会留在进程中。

库析构时，如果没有显式调用 `unload()`，文档说明库会一直留在内存中，直到应用程序终止。需要控制卸载时，应在销毁函数指针、对象和线程资源后显式调用 `unload()`。

### 5.3 函数指针的生命周期

从 `resolve()` 得到的地址只在相应库保持加载时有效：

```cpp
using ProcessFunction = int (*)(const char *);

auto process = reinterpret_cast<ProcessFunction>(
    library.resolve("process"));

// 在这里调用 process 的前提：library 仍保持加载。
```

不要在 `unload()` 之后继续保存并调用这个函数指针。也不要让动态库创建的对象跨越库卸载边界，除非接口明确规定了这种生命周期。

## 6. 文件名与平台搜索规则

### 6.1 建议省略后缀

`fileName` 属性和构造函数都接受 `QString`。Qt 文档建议通常省略平台后缀：

```cpp
QLibrary library(QStringLiteral("GL"));
```

这比写成某个平台专用的 `libGL.so` 或 `GL.dll` 更便于跨平台部署。

### 6.2 绝对路径

如果文件名是绝对路径，Qt 会先尝试这个路径。找不到时，仍可能继续尝试平台相关的前缀和后缀组合。

```cpp
QLibrary library(QStringLiteral("C:/app/plugins/mybackend"));
```

成功加载后，`fileName()` 会返回成功加载的完整文件名；对于带路径的输入，通常会包含完整路径和平台后缀。

### 6.3 非绝对路径

如果文件名不是绝对路径，Qt 会按照平台相关规则搜索系统库位置，例如 Unix 上的 `LD_LIBRARY_PATH` 等环境配置。相对文件名还会参与平台前缀、后缀的尝试。

这意味着：

- `QLibrary` 的搜索结果受运行环境影响；
- 同一个基本名称可能在不同机器上解析到不同库；
- 对不可信输入使用动态库加载会引入搜索路径和供应链风险；
- 需要加载指定文件时，使用经过验证的绝对路径更明确。

## 7. 加载状态和推荐调用顺序

### 7.1 显式加载

```cpp
QLibrary library(QStringLiteral("mylib"));

if (!library.load()) {
    qWarning().noquote() << library.errorString();
    return;
}

if (!library.isLoaded()) {
    return;
}

const auto symbol = library.resolve("mylib_initialize");
```

`load()` 成功返回 `true`，失败返回 `false`。它适合在程序初始化阶段提前检查依赖。

### 7.2 隐式加载

如果只关心某个符号，可以直接调用：

```cpp
const auto symbol = library.resolve("mylib_initialize");
```

实例版 `resolve()` 会在库尚未加载时先尝试加载。符号不存在，或库本身无法加载时，返回 `nullptr`。

### 7.3 `isLoaded()` 的语义

`isLoaded()` 返回当前 `QLibrary` 对象的加载状态：

- `load()` 成功后返回 `true`；
- `load()` 失败后返回 `false`；
- `unload()` 成功后通常回到未加载状态；
- 它不是“系统中是否有任何一个 `QLibrary` 实例加载了同名库”的全局查询。

Qt 6.6 以前的行为曾允许另一个对象加载同一物理库后影响结果；Qt 6.11 文档中的语义应按当前对象的显式加载状态理解。

## 8. `QFunctionPointer` 与符号解析

### 8.1 `QFunctionPointer` 只是通用占位类型

`QFunctionPointer` 的定义是：

```cpp
typedef void (*QFunctionPointer)();
```

它只表达“某个函数地址”，不表达真实参数和返回值。因此不能把它当成目标函数的完整类型安全接口。

推荐先定义准确的函数指针类型，再转换：

```cpp
using AddFunction = int (*)(int, int);

const QFunctionPointer raw = library.resolve("add");
if (!raw) {
    qWarning().noquote() << library.errorString();
    return;
}

const auto add = reinterpret_cast<AddFunction>(raw);
const int result = add(2, 3);
```

### 8.2 符号名称必须匹配导出名称

`resolve()` 使用 `const char *symbol` 查找导出符号。名称匹配通常区分：

- C 与 C++ 的名字改编；
- 大小写；
- Windows 导出名和调用约定；
- 编译器、架构和 ABI；
- 版本脚本或导出列表的最终名称。

找不到符号时不要调用返回的空指针：

```cpp
const auto raw = library.resolve("missing_symbol");
if (raw == nullptr)
    return;
```

### 8.3 函数指针调用约定必须一致

在 Windows 等平台上，`__cdecl`、`__stdcall` 或其他调用约定属于函数类型的一部分。导出方和调用方必须使用相同的调用约定；仅仅让参数列表看起来相同并不够。

跨模块传递 C++ 类、`QString`、STL 容器或由不同编译器/运行库管理的对象时，还要考虑内存分配器、异常、RTTI 和 ABI。更稳妥的边界通常是 C 函数、固定宽度数据和显式的创建/销毁函数。

## 9. `LoadHint` 和 `LoadHints`

`LoadHint` 描述加载方式，`LoadHints` 是 `QFlags<LoadHint>`，可以用按位 OR 组合：

```cpp
library.setLoadHints(QLibrary::ResolveAllSymbolsHint
                     | QLibrary::PreventUnloadHint);
```

### 9.1 各枚举值

| 枚举值 | 值 | 语义 | 使用边界 |
| --- | ---: | --- | --- |
| `ResolveAllSymbolsHint` | `0x01` | 加载时尽可能解析全部符号，而不是等到 `resolve()` 时再惰性解析。 | 是否生效取决于平台；可能让加载更早失败。 |
| `ExportExternalSymbolsHint` | `0x02` | 使库中的外部符号可供之后加载的动态库解析。 | 会影响后续库的符号解析，不能当作普通性能开关。 |
| `LoadArchiveMemberHint` | `0x04` | 允许文件名同时指定归档文件和归档成员。 | 仅 AIX 支持；其他平台不能依赖。 |
| `PreventUnloadHint` | `0x08` | 阻止库从进程地址空间卸载。 | 适合库的静态状态不能安全重新初始化的场景，但会增加常驻内存。 |
| `DeepBindHint` | `0x10` | 让已加载库中的定义优先于加载应用导出的定义。 | 仅 Linux 支持，改变符号绑定优先级，使用前应理解 ELF 动态链接规则。 |

默认情况下没有设置这些标志。通常采用惰性符号解析，也不会把外部符号导出给后续动态库。

### 9.2 `setLoadHints()` 的时机约束

Qt 文档给出了几个容易忽略的边界：

- 只有在对象尚未关联文件时，hint 才能被清除；
- 只有在文件名已经设置后，hint 才能添加；添加操作会和旧值 OR；
- 库加载后再设置该属性没有效果；
- 加载后调用 `loadHints()` 也不会反映这种无效的修改；
- hint 的解释依赖平台，不能把一个平台上的行为推断到所有平台。

推荐在构造或设置文件名后、第一次 `load()`/`resolve()` 前完成配置：

```cpp
QLibrary library(QStringLiteral("mylib"));
library.setLoadHints(QLibrary::ResolveAllSymbolsHint);

if (!library.load())
    qWarning().noquote() << library.errorString();
```

## 10. 错误处理

### 10.1 `nullptr` 和 `false` 是正常失败信号

动态库加载失败不是 C++ 异常。主要通过返回值判断：

- `load()`：失败返回 `false`；
- `unload()`：无法卸载时返回 `false`；
- `resolve()`：库加载失败或符号不存在时返回 `nullptr`；
- `isLibrary()`：文件名后缀不符合平台可加载库规则时返回 `false`。

### 10.2 `errorString()`

`errorString()` 返回最近一次失败操作的文本说明。Qt 文档指出，它目前只会在以下操作失败时设置：

- `load()`；
- `unload()`；
- `resolve()`。

示例：

```cpp
if (!library.load()) {
    qWarning().noquote()
        << "Cannot load" << library.fileName()
        << ":" << library.errorString();
}
```

不要把 `errorString()` 当作一个永久的错误对象，也不要在没有检查操作返回值时把它当作当前状态的权威来源。

### 10.3 先检查后调用

推荐把解析过程写成明确的检查链：

```cpp
using CreateFunction = Widget * (*)();

QLibrary library(QStringLiteral("widget_backend"));
if (!library.load()) {
    reportLoadFailure(library.errorString());
    return nullptr;
}

const auto raw = library.resolve("widget_create");
if (!raw) {
    reportResolveFailure(library.errorString());
    return nullptr;
}

const auto create = reinterpret_cast<CreateFunction>(raw);
return create();
```

如果一个模块需要多个符号，应逐个检查，或者先解析版本/能力查询函数，确认接口版本后再解析其他符号。

## 11. `isLibrary()` 只检查文件名形式

```cpp
if (QLibrary::isLibrary(fileName)) {
    // 文件名后缀看起来像当前平台的动态库。
}
```

它返回 `true` 的含义是：文件名具有当前平台认可的可加载库后缀；它不表示：

- 文件一定存在；
- 文件一定能被加载；
- 文件一定是合法动态库；
- 库的架构与当前进程匹配；
- 依赖库一定齐全；
- 符号一定存在。

文档列出的常见后缀包括：

| 平台 | 常见有效后缀 |
| --- | --- |
| Windows | `.dll`、`.DLL` |
| Unix/Linux | `.so` |
| AIX | `.a` |
| HP-UX | `.sl`、HP-UXi 上的 `.so` |
| macOS/iOS | `.dylib`、`.bundle`、`.so` |

Unix 上文件名末尾的版本号会被忽略。例如带有版本后缀的共享库文件名仍可能被判断为库文件。

## 12. 逐项 API 说明

### 12.1 `QLibrary(QObject *parent = nullptr)`

```cpp
explicit QLibrary(QObject *parent = nullptr);
```

构造一个尚未指定文件名的 `QLibrary` 对象，并设置 QObject 父对象。

适合先构造对象，再通过 `setFileName()` 或 `setFileNameAndVersion()` 配置目标。

```cpp
QLibrary library;
library.setFileName(QStringLiteral("mylib"));
```

### 12.2 `QLibrary(const QString &fileName, QObject *parent = nullptr)`

```cpp
explicit QLibrary(const QString &fileName, QObject *parent = nullptr);
```

构造一个目标文件名为 `fileName` 的对象，但不会因为构造而立即加载库。

`fileName` 通常建议省略平台后缀。加载时 Qt 会依据平台规则查找文件。

### 12.3 `QLibrary(const QString &fileName, int verNum, QObject *parent = nullptr)`

```cpp
explicit QLibrary(const QString &fileName,
                  int verNum,
                  QObject *parent = nullptr);
```

构造指定库名和主版本号的对象。

边界：

- `verNum` 表示主版本号，不是完整版本字符串；
- Windows 上版本号会被忽略；
- 版本参数是否能参与实际文件选择取决于平台；
- 需要应用层可靠版本检查时，应解析版本函数或在加载后检查接口版本。

### 12.4 `QLibrary(const QString &fileName, const QString &version, QObject *parent = nullptr)`

```cpp
explicit QLibrary(const QString &fileName,
                  const QString &version,
                  QObject *parent = nullptr);
```

构造指定库名和完整版本号的对象。

`version` 在 Windows 上会被忽略。它不是对导出函数 ABI 的自动验证。

### 12.5 `~QLibrary()`

```cpp
virtual noexcept ~QLibrary();
```

销毁 `QLibrary` 对象。

需要记住：如果没有显式调用 `unload()`，文档说明对应库会保留在内存中，直到应用程序终止。析构对象不等价于立即卸载共享库。

### 12.6 `void setFileName(const QString &fileName)`

```cpp
void setFileName(const QString &fileName);
```

设置 `fileName` 属性，指定后续加载所使用的库名。

使用建议：

- 在第一次 `load()` 或 `resolve()` 之前设置；
- 通常省略平台后缀；
- 需要确定目标时使用已验证的绝对路径；
- 改变文件名后，不要继续使用旧库解析出来的函数指针。

### 12.7 `QString fileName() const`

```cpp
QString fileName() const;
```

返回当前库文件名。

加载成功后，文档说明该函数会返回实际成功加载的完整文件名，可能包含平台后缀和完整路径。不要假设返回值始终等于最初传入的基本名称。

### 12.8 `void setFileNameAndVersion(const QString &fileName, int verNum)`

```cpp
void setFileNameAndVersion(const QString &fileName, int verNum);
```

同时设置文件名和主版本号。`verNum` 在 Windows 上会被忽略。

### 12.9 `void setFileNameAndVersion(const QString &fileName, const QString &version)`

```cpp
void setFileNameAndVersion(const QString &fileName,
                           const QString &version);
```

同时设置文件名和完整版本号。`version` 在 Windows 上会被忽略。

### 12.10 `bool load()`

```cpp
bool load();
```

尝试加载目标共享库：

- 成功返回 `true`；
- 失败返回 `false`；
- 失败原因可通过 `errorString()` 查询；
- 如果已经加载，调用通常不会重新加载同一库；
- `resolve()` 会隐式调用它，因此并非所有场景都需要显式调用。

适合显式调用的情况：

- 启动时验证可选依赖；
- 希望在进入业务逻辑前报告错误；
- 需要先加载所有符号，再执行后续初始化；
- 需要把加载失败和符号缺失区分开。

### 12.11 `bool isLoaded() const`

```cpp
bool isLoaded() const;
```

返回当前 `QLibrary` 对象是否已经成功加载。

它不保证某个符号存在，也不保证库的所有可选依赖都满足。符号是否存在仍要通过 `resolve()` 检查。

### 12.12 `bool unload()`

```cpp
bool unload();
```

尝试卸载库：

- 能够卸载时返回 `true`；
- 因为其他实例仍在使用等原因不能卸载时返回 `false`；
- 失败原因可通过 `errorString()` 查询；
- macOS 上可能返回 `true`，但库仍留在进程地址空间；
- 在卸载前必须停止使用所有从该库取得的函数指针和对象。

一般不需要在进程退出前手动卸载。只有当模块生命周期明确、且确认动态库支持安全卸载时，才主动使用它。

### 12.13 `QFunctionPointer resolve(const char *symbol)`

```cpp
QFunctionPointer resolve(const char *symbol);
```

解析当前库中名为 `symbol` 的导出符号。

行为：

- 如果库尚未加载，会先尝试加载；
- 成功返回符号地址；
- 库无法加载或符号不存在时返回 `nullptr`；
- 返回值需要转换为调用方声明的准确函数指针类型；
- 符号通常应由 `extern "C"` 导出，以避免 C++ 名字改编。

示例：

```cpp
using AverageFunction = int (*)(int, int);

QLibrary library(QStringLiteral("math_backend"));
const auto raw = library.resolve("average");
if (!raw)
    return false;

const auto average = reinterpret_cast<AverageFunction>(raw);
const int value = average(5, 8);
```

### 12.14 `static QFunctionPointer resolve(const QString &fileName, const char *symbol)`

```cpp
static QFunctionPointer resolve(const QString &fileName,
                                const char *symbol);
```

加载 `fileName` 指定的库并解析符号，不需要先创建 `QLibrary` 对象。

边界：

- `fileName` 通常不应包含平台专用后缀；
- 找不到库或符号时返回 `nullptr`；
- 静态重载加载的库会一直保持到应用程序退出；
- 没有对象可供你随后调用 `unload()`；
- 返回的函数指针仍然需要转换为准确的函数类型。

```cpp
using VersionFunction = int (*)();

const auto raw = QLibrary::resolve(QStringLiteral("mylib"),
                                   "version");
if (raw) {
    const auto version = reinterpret_cast<VersionFunction>(raw);
    qDebug() << version();
}
```

### 12.15 `static QFunctionPointer resolve(const QString &fileName, int verNum, const char *symbol)`

```cpp
static QFunctionPointer resolve(const QString &fileName,
                                int verNum,
                                const char *symbol);
```

加载指定主版本号的库并解析符号。

`verNum` 在 Windows 上会被忽略；其他平台是否使用它由平台的动态库命名和加载规则决定。

### 12.16 `static QFunctionPointer resolve(const QString &fileName, const QString &version, const char *symbol)`

```cpp
static QFunctionPointer resolve(const QString &fileName,
                                const QString &version,
                                const char *symbol);
```

加载指定完整版本号的库并解析符号。

`version` 在 Windows 上会被忽略。静态解析成功后，库会保持加载到应用退出。

### 12.17 `static bool isLibrary(const QString &fileName)`

```cpp
static bool isLibrary(const QString &fileName);
```

根据当前平台的文件名后缀判断 `fileName` 是否看起来像可加载库。

它只检查名称形式，不执行实际加载，也不验证文件内容、架构、依赖或符号。

### 12.18 `QString errorString() const`

```cpp
QString errorString() const;
```

返回最近一次加载、卸载或符号解析失败的文本说明。

应在失败操作之后立即读取并记录，避免把旧错误误认为新错误。

### 12.19 `void setLoadHints(LoadHints hints)`

```cpp
void setLoadHints(LoadHints hints);
```

设置加载提示。多个提示可以用 `|` 组合：

```cpp
library.setLoadHints(QLibrary::ResolveAllSymbolsHint
                     | QLibrary::PreventUnloadHint);
```

时机和状态限制：

- 加载后再修改没有效果；
- 添加 hint 通常要求对象已经设置文件名；
- 清除 hint 受对象是否关联文件的限制；
- 解释依赖平台，不能假设所有 hint 在所有平台可用。

### 12.20 `LoadHints loadHints() const`

```cpp
LoadHints loadHints() const;
```

返回当前记录的加载提示组合。

可以用 `testFlag()` 检查单个标志：

```cpp
if (library.loadHints().testFlag(QLibrary::ResolveAllSymbolsHint)) {
    // 已设置加载时解析全部符号的提示。
}
```

加载后对 `setLoadHints()` 的修改不会生效，文档也说明此时 getter 不会反映这种修改。

## 13. 常见误区与排查顺序

### 13.1 把 `isLibrary()` 当作“文件可加载”

`isLibrary()` 只看文件名后缀。真正的验证必须调用 `load()`，然后再调用 `resolve()` 检查符号。

### 13.2 把 `QFunctionPointer` 直接当作目标函数类型

`QFunctionPointer` 是 `void (*)()`。必须转换为准确的函数指针类型，并确认导出方的 ABI、调用约定和数据布局。

### 13.3 忘记检查 `resolve()` 的空指针

库加载成功不等于目标符号存在。每个符号解析都要检查 `nullptr`。

### 13.4 直接解析 C++ 成员函数或改名后的函数

C++ 名字改编、成员函数隐含的 `this` 参数和编译器 ABI 都不适合作为通用动态库边界。优先导出 `extern "C"` 的自由函数。

### 13.5 卸载后继续使用函数指针

卸载会使之前解析的地址失效。调用 `unload()` 前要停止工作线程、销毁模块对象并清空相关函数指针。

### 13.6 以为析构会立即卸载

文档说明，如果没有显式调用 `unload()`，库会保持到应用终止。需要释放时要明确调用，并处理其他实例和平台限制。

### 13.7 过度依赖版本参数

版本参数在 Windows 上被忽略，其他平台也可能只参与名称选择。真正需要 ABI 版本控制时，应提供版本查询函数：

```cpp
using ApiVersionFunction = int (*)();
```

先读取版本，再决定解析哪些后续符号。

### 13.8 加载路径来自不可信输入

动态库搜索路径会受到当前工作目录、环境变量和系统搜索规则影响。不要直接使用不可信用户输入拼接库名；需要加载外部模块时，应校验路径、签名、版本和来源。

### 13.9 在错误平台上使用加载提示

`LoadArchiveMemberHint` 只适用于 AIX；`DeepBindHint` 只支持 Linux。设置了 hint 不表示平台一定会执行对应行为。

### 13.10 把 `QLibrary` 当作 Qt 插件加载器

如果需要 Qt 插件元数据、插件实例创建和插件接口检查，应优先研究 `QPluginLoader`。`QLibrary` 只提供动态库级别的加载和符号解析。

## 14. 一段较完整的动态库封装示例

下面的封装展示了几个重要原则：先显式加载、再解析版本、确认版本后解析接口，并在对象销毁前释放函数指针的使用关系。

```cpp
#include <QLibrary>
#include <QDebug>
#include <QString>

class BackendApi
{
public:
    using VersionFunction = int (*)();
    using InitializeFunction = bool (*)(int);
    using ShutdownFunction = void (*)();

    bool open(const QString &name)
    {
        library.setFileName(name);
        if (!library.load()) {
            qWarning().noquote() << library.errorString();
            return false;
        }

        const auto versionSymbol = library.resolve("backend_version");
        if (!versionSymbol)
            return false;

        const auto version =
            reinterpret_cast<VersionFunction>(versionSymbol);
        if (version() != 3)
            return false;

        const auto initSymbol = library.resolve("backend_initialize");
        const auto shutdownSymbol = library.resolve("backend_shutdown");
        if (!initSymbol || !shutdownSymbol)
            return false;

        initialize =
            reinterpret_cast<InitializeFunction>(initSymbol);
        shutdown =
            reinterpret_cast<ShutdownFunction>(shutdownSymbol);
        return initialize(1);
    }

    void close()
    {
        if (shutdown)
            shutdown();

        initialize = nullptr;
        shutdown = nullptr;
        library.unload();
    }

private:
    QLibrary library;
    InitializeFunction initialize = nullptr;
    ShutdownFunction shutdown = nullptr;
};
```

生产代码还应考虑：初始化失败时的清理、线程停止、库的错误码、接口版本兼容范围、`unload()` 失败处理以及模块是否允许重复初始化。

## API 速查表
### 15.1 构造、生命周期与文件名

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QLibrary(QObject *parent = nullptr)` | 创建未指定库文件的对象。 | 之后需要调用 `setFileName()` 或 `setFileNameAndVersion()`。 |
| `QLibrary(const QString &fileName, QObject *parent = nullptr)` | 创建指定库名的对象。 | 构造不会自动加载；通常省略平台后缀。 |
| `QLibrary(const QString &fileName, int verNum, QObject *parent = nullptr)` | 创建指定库名和主版本号的对象。 | Windows 忽略版本号；平台行为可能不同。 |
| `QLibrary(const QString &fileName, const QString &version, QObject *parent = nullptr)` | 创建指定库名和完整版本号的对象。 | Windows 忽略版本号；不是完整 ABI 校验。 |
| `~QLibrary()` | 销毁对象。 | 不等于立即卸载；未显式 `unload()` 时库可留到应用退出。 |
| `void setFileName(const QString &fileName)` | 设置目标库文件名。 | 重新指定目标后不要继续使用旧库的函数指针。 |
| `QString fileName() const` | 返回当前或成功加载后的库文件名。 | 加载成功后可能变成带路径和后缀的完整名称。 |
| `void setFileNameAndVersion(const QString &, int)` | 同时设置库名和主版本号。 | Windows 忽略版本号。 |
| `void setFileNameAndVersion(const QString &, const QString &)` | 同时设置库名和完整版本号。 | Windows 忽略版本号。 |

### 15.2 加载和卸载

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `bool load()` | 加载共享库。 | 失败返回 `false`，用 `errorString()` 获取原因。 |
| `bool isLoaded() const` | 查询当前对象是否成功加载。 | 不表示某个符号存在，也不是全局库状态查询。 |
| `bool unload()` | 尝试卸载共享库。 | 其他实例、平台限制或 `PreventUnloadHint` 可能阻止实际卸载。 |
| `QString errorString() const` | 返回最近一次加载、卸载或解析失败的说明。 | 在失败操作后立即读取，避免误用旧错误。 |

### 15.3 实例符号解析

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QFunctionPointer resolve(const char *symbol)` | 在当前库中解析导出符号。 | 必要时隐式加载；失败返回 `nullptr`；需转换为准确函数类型。 |

### 15.4 静态符号解析

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `static QFunctionPointer resolve(const QString &, const char *)` | 加载库并解析符号。 | 成功后库保持到应用退出；没有对象可调用 `unload()`。 |
| `static QFunctionPointer resolve(const QString &, int, const char *)` | 按主版本加载库并解析符号。 | Windows 忽略版本号；仍需检查空指针。 |
| `static QFunctionPointer resolve(const QString &, const QString &, const char *)` | 按完整版本加载库并解析符号。 | Windows 忽略版本号；库通常保持到应用退出。 |

### 15.5 库名判断

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `static bool isLibrary(const QString &fileName)` | 判断文件名后缀是否像当前平台的动态库。 | 不检查文件存在、格式、架构、依赖或符号。 |

### 15.6 加载提示

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `void setLoadHints(LoadHints hints)` | 设置加载提示组合。 | 应在首次加载前设置；平台相关。 |
| `LoadHints loadHints() const` | 读取当前加载提示组合。 | 加载后修改 hint 不生效，getter 也不反映该无效修改。 |
| `QLibrary::ResolveAllSymbolsHint` | 加载时尽可能解析全部符号。 | 平台支持时生效，可能让加载更早失败。 |
| `QLibrary::ExportExternalSymbolsHint` | 向后续动态库导出外部符号。 | 会影响后续符号绑定。 |
| `QLibrary::LoadArchiveMemberHint` | 加载归档中的指定成员。 | 仅 AIX 支持。 |
| `QLibrary::PreventUnloadHint` | 阻止库卸载。 | 可能造成库常驻和静态状态保留。 |
| `QLibrary::DeepBindHint` | 优先使用已加载库自身的符号定义。 | 仅 Linux 支持，改变符号绑定规则。 |
| `QLibrary::LoadHints` | `QFlags<LoadHint>` 标志组合类型。 | 使用 `|` 组合，使用 `testFlag()` 查询。 |

## 16. 最后的选型规则

1. 需要运行时加载共享库并按名称取得 C 函数地址时，使用 `QLibrary`。
2. 需要 Qt 插件元数据和插件实例管理时，优先研究 `QPluginLoader`。
3. 文件名通常省略平台后缀；需要确定目标时使用经过验证的绝对路径。
4. 把 `load()`、`resolve()` 的返回值当作必须检查的失败信号。
5. 把 `QFunctionPointer` 转换为准确的函数指针类型，并让导出方使用稳定的 C ABI。
6. 在 `unload()` 前停止所有调用、销毁模块对象和工作线程。
7. 不要把版本参数当作跨平台 ABI 兼容性验证；提供版本查询函数更可靠。
8. `LoadHint` 是平台相关提示，必须在第一次加载前设置。
9. `isLibrary()` 只判断名称后缀，不能替代实际加载测试。
10. 不可信路径、环境变量和动态库来源需要额外的安全校验。

`QLibrary` 的核心价值是把“共享库的运行时加载”和“导出符号的运行时解析”放在一个跨平台 Qt API 中。真正可靠的动态模块系统，还需要调用方自己定义稳定的 ABI、版本协商、错误处理、线程停止和卸载策略。
