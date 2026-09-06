# QLibrary

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QLibrary` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QLibrary` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QLibrary>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum LoadHint { ResolveAllSymbolsHint, ExportExternalSymbolsHint, LoadArchiveMemberHint, PreventUnloadHint, DeepBindHint }`
- `flags LoadHints`

### 属性

- `fileName : QString`
- `loadHints : LoadHints`

### 公有函数

- `QLibrary(QObject *parent = nullptr)`
- `QLibrary(const QString &fileName, QObject *parent = nullptr)`
- `QLibrary(const QString &fileName, const QString &version, QObject *parent = nullptr)`
- `QLibrary(const QString &fileName, int verNum, QObject *parent = nullptr)`
- `virtual ~QLibrary()`
- `QString errorString() const`
- `QString fileName() const`
- `bool isLoaded() const`
- `bool load()`
- `QLibrary::LoadHints loadHints() const`
- `QFunctionPointer resolve(const char *symbol)`
- `void setFileName(const QString &fileName)`
- `void setFileNameAndVersion(const QString &fileName, const QString &version)`
- `void setFileNameAndVersion(const QString &fileName, int versionNumber)`
- `void setLoadHints(QLibrary::LoadHints hints)`
- `bool unload()`

### 静态公有成员

- `bool isLibrary(const QString &fileName)`
- `QFunctionPointer resolve(const QString &fileName, const char *symbol)`
- `QFunctionPointer resolve(const QString &fileName, const QString &version, const char *symbol)`
- `QFunctionPointer resolve(const QString &fileName, int verNum, const char *symbol)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QLibrary::LoadHintflags QLibrary::LoadHints`

**作用与语义：**

该枚举描述了可用于改变库加载方式的提示。这些值表示库加载时符号的解析方式，并通过`setLoadHints()`函数指定。
- `QLibrary::ResolveAllSymbolsHint`：`0x01`;使库中的所有符号在加载时被解析，而不仅仅是调用`resolve()`。
- `QLibrary::ExportExternalSymbolsHint`：`0x02`;导出库中未解析和外部符号，以便后续加载的其他动态加载库中解析。
- `QLibrary::LoadArchiveMemberHint`：`0x04`;允许库的文件名在归档文件中指定特定对象文件。如果给出了这个提示，库的文件名由一条路径组成，路径是对归档文件的引用，随后是对归档成员的引用。
- `QLibrary::PreventUnloadHint`：`0x08`;如果调用 close() ，防止库从地址空间中卸载。如果以后调用 open()，库的静态变量不会被重新初始化。
- `QLibrary::DeepBindHint`：`0x10`;指示链接器在解析加载库中的外部符号时，优先使用加载库中的定义而非加载应用中的导出定义。该选项仅支持 Linux。
LoadHints 类型是 QFlags 的 typedef<LoadHint>。它存储 LoadHint 值的 OR 组合。

### `fileName : QString`

**作用与语义：**

该属性包含库的文件名。
我们建议在文件名中省略文件的后缀，因为`QLibrary`会自动查找带有相应后缀的文件（见 `isLibrary()`）。
加载库时，`QLibrary`在所有系统特定的库位置进行搜索（例如Unix上的`LD_LIBRARY_PATH`），除非文件名有绝对路径。成功加载库后，fileName() 返回库的完全限定文件名，包括构造函数中给出或传递给 setFileName()的完整路径。
例如，在Unix平台上成功加载“GL”库后，fileName()会返回“libGL.so”。如果文件名最初是“/usr/lib/libGL”，fileName()会返回“/usr/lib/libGL.so”。

**如何使用：** 调用 `fileName()` 读取当前值；它不会修改应用状态。

### `loadHints : LoadHints`

**作用与语义：**

给`load()`函数一些提示，告诉它应该如何表现。
你可以给一些符号解析的提示。通常符号不是在加载时解析，而是懒惰地解析（也就是调用`resolve()`时）。如果你把 loadHints 设为 `ResolveAllSymbolsHint`，那么如果平台支持，所有符号都会在加载时被解析。
设置`ExportExternalSymbolsHint`将使库中的外部符号在后续加载库中可供解析。
如果设置了`LoadArchiveMemberHint`，文件名由两个组件组成：一条路径是指向归档文件的路径，接着是指向归档成员的第二个组件。例如，`fileName` `libGL.a(shr_64.o)`会指向名为 `libGL.a` 的归档文件中的库`shr_64.o`。这仅支持 AIX 平台。
加载提示的解读取决于平台，如果你用它，可能会对编译的平台做出一些假设，所以只有在理解后才使用。
默认情况下，这些标志都未被设置，因此库将加载为懒惰的符号分辨率，且不会导出其他动态加载库中的外部符号以实现分辨率。
注意：只有当该对象不关联文件时，提示才能清除。提示只能在设置文件名后添加（`hints`会用旧提示标记）。
注意：在库加载后设置该属性无效，loadHints() 不会反映这些更改。
注意：该属性在所有引用同一库的`QLibrary`实例中共享。

**如何使用：** 调用 `loadHints()` 读取当前值；它不会修改应用状态。

### `[explicit] QLibrary::QLibrary(QObject *parent = nullptr)`

**作用与语义：**

用给定的 `parent` 构建一个库。

### `[explicit] QLibrary::QLibrary(const QString &fileName, QObject *parent = nullptr)`

**作用与语义：**

构造一个库对象，包含给定的`parent`，加载`fileName`指定的库。
我们建议在`fileName`中省略文件后缀，因为QLibrary会自动根据平台寻找带有相应后缀的文件，例如Unix上的“.so”，macOS和iOS上的“.dylib”，以及Windows上的“.dll”。（参见`fileName`。）。

### `[explicit] QLibrary::QLibrary(const QString &fileName, const QString &version, QObject *parent = nullptr)`

**作用与语义：**

构建一个带有给定`parent`的库对象，加载由`fileName`指定的库和完整版本号`version`。目前，Windows上版本号被忽略。
我们建议在`fileName`中省略文件后缀，因为QLibrary会自动根据平台查找带有相应后缀的文件，例如Unix上的“.so”，macOS和iOS上的“.dylib”，Windows上的“.dll”。（参见`fileName`。）。

### `[explicit] QLibrary::QLibrary(const QString &fileName, int verNum, QObject *parent = nullptr)`

**作用与语义：**

构造一个包含给定`parent`的库对象，加载由`fileName`和主要版本号`verNum`指定的库。目前，Windows上忽略版本号。
我们建议在`fileName`中省略文件后缀，因为QLibrary会自动根据平台查找带有相应后缀的文件，例如Unix上的“.so”、macOS和iOS上的“.dylib”以及Windows上的“.dll”。（参见`fileName`。）。

### `[virtual noexcept] QLibrary::~QLibrary()`

**作用与语义：**

摧毁`QLibrary`物体。
除非`unload()`被明确调用，否则库会一直留在内存中，直到应用程序终止。

### `QString QLibrary::errorString() const`

**作用与语义：**

返回一个包含最后错误描述的文本字符串。目前，只有在`load()`、`unload()`或`resolve()`因某种原因失败时，才会设置errorString。

### `[static] bool QLibrary::isLibrary(const QString &fileName)`

**作用与语义：**

如果 `fileName` 对于可加载库具有有效后缀，则返回 `true`；否则返回 `false`。
- `Platform`：有效后缀
- `Windows`：`.dll`, `.DLL`
- `Unix/Linux`：`.so`
- `AIX`：`.a`
- `HP-UX`：`.sl`, `.so`（HP-UXi）
- `macOS and iOS`：`.dylib`, `.bundle`, `.so`
Unix 系统上会忽略尾随的版本号。

### `bool QLibrary::isLoaded() const`

**作用与语义：**

如果`load()`成功，返回`true`;否则返回`false`。
注意：在Qt 6.6之前，即使没有调用`load()`，如果同一库中的另一个`QLibrary`对象导致该函数被加载，该函数也会返回`true`。

### `bool QLibrary::load()`

**作用与语义：**

加载库并返回`true`如果库成功加载;否则返回`false`。由于`resolve()`总是在解析任何符号前调用该函数，因此无需显式调用。在某些情况下，你可能希望提前加载库，这时你会使用该函数。

### `QFunctionPointer QLibrary::resolve(const char *symbol)`

**作用与语义：**

返回导出符号的地址 `symbol`。如有必要，库会被加载。函数返回 `nullptr` 如果符号无法解析或库无法加载。
符号必须从库导出为 C 函数。这意味着如果库是用 C 编译器编译的，函数必须以 `extern "C"` 封装。在 Windows 上，你还必须用 `__declspec(dllexport)` 编译器指令从 DLL 显式导出函数，例如：
其中`MY_EXPORT`定义为。

**官方示例：**

```cpp
 typedef int (*AvgFunction)(int, int);

 AvgFunction avg = (AvgFunction) library->resolve("avg");
 if (avg)
     return avg(5, 8);
 else
     return -1;
```

### `[static] QFunctionPointer QLibrary::resolve(const QString &fileName, const char *symbol)`

**作用与语义：**

加载库`fileName`并返回导出符号的地址`symbol`。注意`fileName`不应包含平台特定文件后缀;（参见 `fileName`）。库会一直加载到应用程序退出。
如果符号无法解析或库无法加载，函数返回`nullptr`。

### `[static] QFunctionPointer QLibrary::resolve(const QString &fileName, const QString &version, const char *symbol)`

**作用与语义：**

加载库`fileName`，完整版本号`version`，并返回导出符号的地址`symbol`。注意`fileName`不应包含平台特定文件后缀;（参见 `fileName`）。库会一直加载，直到应用程序退出。`version`在 Windows 上被忽略。
如果符号无法解析或库无法加载，函数返回`nullptr`。

### `[static] QFunctionPointer QLibrary::resolve(const QString &fileName, int verNum, const char *symbol)`

**作用与语义：**

加载库`fileName`，主要版本号为`verNum`，并返回导出符号的地址`symbol`。注意`fileName`不应包含平台特定文件后缀;（见 `fileName`）。库会一直加载，直到应用程序退出。`verNum`在 Windows 上被忽略。
如果符号无法解析或库无法加载，函数返回`nullptr`。

### `void QLibrary::setFileNameAndVersion(const QString &fileName, const QString &version)`

**作用与语义：**

将`fileName`属性和完整版本号分别设置为`fileName`和`version`。Windows上忽略`version`参数。

### `void QLibrary::setFileNameAndVersion(const QString &fileName, int versionNumber)`

**作用与语义：**

将`fileName`属性和主要版本号分别设置为`fileName`和`versionNumber`。Windows上忽略了`versionNumber`。

### `bool QLibrary::unload()`

**作用与语义：**

卸载库并返回`true`如果库可以卸载;否则返回`false`。
这在应用终止时会自动发生，所以通常不需要调用这个函数。
如果其他`QLibrary`实例使用同一库，调用将失败，且卸载仅在每个实例都调用 unload()。
注意，在macOS上，动态库无法卸载。QLibrary：：unload()会返回`true`，但库仍会加载到进程中。

### `enum LoadHint { ResolveAllSymbolsHint, ExportExternalSymbolsHint, LoadArchiveMemberHint, PreventUnloadHint, DeepBindHint }`

**作用与语义：**

该枚举描述了可用于改变库加载方式的提示。这些值表示库加载时符号的解析方式，并通过`setLoadHints()`函数指定。
- `QLibrary::ResolveAllSymbolsHint`：`0x01`;使库中的所有符号在加载时被解析，而不仅仅是调用`resolve()`。
- `QLibrary::ExportExternalSymbolsHint`：`0x02`;导出库中未解析和外部符号，以便后续加载的其他动态加载库中解析。
- `QLibrary::LoadArchiveMemberHint`：`0x04`;允许库的文件名在归档文件中指定特定对象文件。如果给出了这个提示，库的文件名由一条路径组成，路径是对归档文件的引用，随后是对归档成员的引用。
- `QLibrary::PreventUnloadHint`：`0x08`;如果调用 close() ，防止库从地址空间中卸载。如果以后调用 open()，库的静态变量不会被重新初始化。
- `QLibrary::DeepBindHint`：`0x10`;指示链接器在解析加载库中的外部符号时，优先使用加载库中的定义而非加载应用中的导出定义。该选项仅支持 Linux。
LoadHints 类型是 QFlags 的 typedef<LoadHint>。它存储 LoadHint 值的 OR 组合。

### `flags LoadHints`

**作用与语义：**

该枚举描述了可用于改变库加载方式的提示。这些值表示库加载时符号的解析方式，并通过`setLoadHints()`函数指定。
- `QLibrary::ResolveAllSymbolsHint`：`0x01`;使库中的所有符号在加载时被解析，而不仅仅是调用`resolve()`。
- `QLibrary::ExportExternalSymbolsHint`：`0x02`;导出库中未解析和外部符号，以便后续加载的其他动态加载库中解析。
- `QLibrary::LoadArchiveMemberHint`：`0x04`;允许库的文件名在归档文件中指定特定对象文件。如果给出了这个提示，库的文件名由一条路径组成，路径是对归档文件的引用，随后是对归档成员的引用。
- `QLibrary::PreventUnloadHint`：`0x08`;如果调用 close() ，防止库从地址空间中卸载。如果以后调用 open()，库的静态变量不会被重新初始化。
- `QLibrary::DeepBindHint`：`0x10`;指示链接器在解析加载库中的外部符号时，优先使用加载库中的定义而非加载应用中的导出定义。该选项仅支持 Linux。
LoadHints 类型是 QFlags 的 typedef<LoadHint>。它存储 LoadHint 值的 OR 组合。

### `QString fileName() const`

**作用与语义：**

该属性包含库的文件名。
我们建议在文件名中省略文件的后缀，因为`QLibrary`会自动查找带有相应后缀的文件（见 `isLibrary()`）。
加载库时，`QLibrary`在所有系统特定的库位置进行搜索（例如Unix上的`LD_LIBRARY_PATH`），除非文件名有绝对路径。成功加载库后，fileName() 返回库的完全限定文件名，包括构造函数中给出或传递给 setFileName()的完整路径。
例如，在Unix平台上成功加载“GL”库后，fileName()会返回“libGL.so”。如果文件名最初是“/usr/lib/libGL”，fileName()会返回“/usr/lib/libGL.so”。

**如何使用：** 调用 `fileName()` 读取当前值；它不会修改应用状态。

### `QLibrary::LoadHints loadHints() const`

**作用与语义：**

给`load()`函数一些提示，告诉它应该如何表现。
你可以给一些符号解析的提示。通常符号不是在加载时解析，而是懒惰地解析（也就是调用`resolve()`时）。如果你把 loadHints 设为 `ResolveAllSymbolsHint`，那么如果平台支持，所有符号都会在加载时被解析。
设置`ExportExternalSymbolsHint`将使库中的外部符号在后续加载库中可供解析。
如果设置了`LoadArchiveMemberHint`，文件名由两个组件组成：一条路径是指向归档文件的路径，接着是指向归档成员的第二个组件。例如，`fileName` `libGL.a(shr_64.o)`会指向名为 `libGL.a` 的归档文件中的库`shr_64.o`。这仅支持 AIX 平台。
加载提示的解读取决于平台，如果你用它，可能会对编译的平台做出一些假设，所以只有在理解后才使用。
默认情况下，这些标志都未被设置，因此库将加载为懒惰的符号分辨率，且不会导出其他动态加载库中的外部符号以实现分辨率。
注意：只有当该对象不关联文件时，提示才能清除。提示只能在设置文件名后添加（`hints`会用旧提示标记）。
注意：在库加载后设置该属性无效，loadHints() 不会反映这些更改。
注意：该属性在所有引用同一库的`QLibrary`实例中共享。

**如何使用：** 调用 `loadHints()` 读取当前值；它不会修改应用状态。

### `void setFileName(const QString &fileName)`

**作用与语义：**

该属性包含库的文件名。
我们建议在文件名中省略文件的后缀，因为`QLibrary`会自动查找带有相应后缀的文件（见 `isLibrary()`）。
加载库时，`QLibrary`在所有系统特定的库位置进行搜索（例如Unix上的`LD_LIBRARY_PATH`），除非文件名有绝对路径。成功加载库后，fileName() 返回库的完全限定文件名，包括构造函数中给出或传递给 setFileName()的完整路径。
例如，在Unix平台上成功加载“GL”库后，fileName()会返回“libGL.so”。如果文件名最初是“/usr/lib/libGL”，fileName()会返回“/usr/lib/libGL.so”。

**如何使用：** 调用 `setFileName(...)` 修改 `fileName`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLoadHints(QLibrary::LoadHints hints)`

**作用与语义：**

给`load()`函数一些提示，告诉它应该如何表现。
你可以给一些符号解析的提示。通常符号不是在加载时解析，而是懒惰地解析（也就是调用`resolve()`时）。如果你把 loadHints 设为 `ResolveAllSymbolsHint`，那么如果平台支持，所有符号都会在加载时被解析。
设置`ExportExternalSymbolsHint`将使库中的外部符号在后续加载库中可供解析。
如果设置了`LoadArchiveMemberHint`，文件名由两个组件组成：一条路径是指向归档文件的路径，接着是指向归档成员的第二个组件。例如，`fileName` `libGL.a(shr_64.o)`会指向名为 `libGL.a` 的归档文件中的库`shr_64.o`。这仅支持 AIX 平台。
加载提示的解读取决于平台，如果你用它，可能会对编译的平台做出一些假设，所以只有在理解后才使用。
默认情况下，这些标志都未被设置，因此库将加载为懒惰的符号分辨率，且不会导出其他动态加载库中的外部符号以实现分辨率。
注意：只有当该对象不关联文件时，提示才能清除。提示只能在设置文件名后添加（`hints`会用旧提示标记）。
注意：在库加载后设置该属性无效，loadHints() 不会反映这些更改。
注意：该属性在所有引用同一库的`QLibrary`实例中共享。

**如何使用：** 调用 `setLoadHints(...)` 修改 `loadHints`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QLibrary` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
