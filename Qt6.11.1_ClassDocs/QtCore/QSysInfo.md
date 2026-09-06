# QSysInfo

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QSysInfo` 是 Qt 的值类型，围绕“SysInfo”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSysInfo` 是 Qt 值类型与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QSysInfo>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Endian { BigEndian, LittleEndian, ByteOrder }`
- `enum Sizes { WordSize }`

### 静态公有成员

- `QByteArray bootUniqueId()`
- `QString buildAbi()`
- `QString buildCpuArchitecture()`
- `QString currentCpuArchitecture()`
- `QString kernelType()`
- `QString kernelVersion()`
- `QString machineHostName()`
- `QByteArray machineUniqueId()`
- `QString prettyProductName()`
- `QString productType()`
- `QString productVersion()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSysInfo::Sizes`

**作用与语义：**

该枚举提供了关于底层架构所使用数据结构大小的平台特定信息。
- `QSysInfo::WordSize`：`(sizeof(void *)<<3)`;指应用程序编译平台指针的位数（32或64）。

### `[static] QByteArray QSysInfo::bootUniqueId()`

**作用与语义：**

如果可以确定该机器的启动，返回唯一的 ID。如果无法确定唯一 ID，该函数返回一个空字节数组。该值预计每次启动后都会变化，可以视为全局唯一。
该功能目前仅在 Linux 和苹果操作系统上实现。

### `[static] QString QSysInfo::buildAbi()`

**作用与语义：**

返回 Qt 编译时的完整架构字符串。该字符串有助于识别不同且不兼容的构建。例如，它可以用作向服务器请求升级包的标识符。
该函数返回的值保持稳定如下：结果的强制成分在未来版本的 Qt 中不会改变，但可以添加可选后缀。
返回值由三个或更多部分组成，中间用破折号（“-”）分隔。它们是：
- `Component`：价值
- `CPU Architecture`：与`QSysInfo::buildCpuArchitecture()`相同，如“arm”、“i386”、“mips”或“x86_64”
- `Endianness`：“`little_endian`”或“`big_endian`”
- `Word size`：是32位还是64位应用程序。可能的值有：“llp64”（Windows 64位）、“lp64”（Unix 64位）、“ilp32”（32位）
- `(Optional) ABI`：零个或多个组件，识别该架构中可能的不同ABI。目前，Qt为ARM和MIPS处理器提供可选的ABI组件：一个是主ABI（如“eabi”、“o32”、“n32”、“o64”）;另一个是调用约定是否使用硬件浮点寄存器（“hardfloat”）。此外，如果Qt配置为`-qreal float`，则会出现ABI选项标签“qreal_float”。如果Qt配置了其他类型作为qreal，该类型出现在“qreal_”之后，除字母和数字外的所有字符都被下划线跳出，后面跟两个十六进制数字。例如，`-qreal long double`变为“qreal_long_20double”。

### `[static] QString QSysInfo::buildCpuArchitecture()`

**作用与语义：**

返回Qt编译时CPU的架构，以文本格式呈现。注意，如果存在仿真层或CPU支持多种架构（如支持i386应用的x86-64处理器），这可能与实际运行的CPU不匹配。要检测这一点，请使用`currentCpuArchitecture()`。
该函数返回的值是稳定的，不会随时间变化，因此应用程序可以依赖返回值作为标识符，但可能会随着时间添加新的CPU类型。
典型返回的值如下（注：列表并非详尽）：
- “手臂”
- “arm64”
- “i386”
- “ia64”
- “Mips”
- “mips64”
- “权力”
- “Power64”
- “SPARC”
- “sparcv9”
- 《x86_64》

### `[static] QString QSysInfo::currentCpuArchitecture()`

**作用与语义：**

返回应用程序运行的CPU架构，以文本格式呈现。注意，该功能依赖于操作系统将报告的内容，如果操作系统隐藏或无法提供实际的CPU架构，可能无法检测到该信息。例如，运行在64位CPU上的32位操作系统通常无法判断CPU是否真正能够运行64位程序。
该函数返回的值大多是稳定的：会尝试确保它们随时间保持不变，并与`buildCpuArchitecture()`返回的值相匹配。然而，由于所使用的操作系统函数的属性，可能会存在差异。
典型返回的值如下（注：列表并非详尽）：
- “手臂”
- “arm64”
- “i386”
- “ia64”
- “Mips”
- “mips64”
- “权力”
- “Power64”
- “SPARC”
- “sparcv9”
- 《x86_64》

### `[static] QString QSysInfo::kernelType()`

**作用与语义：**

返回Qt编译时所使用的操作系统内核类型。它也是应用程序运行的内核，除非宿主操作系统运行某种兼容性或虚拟化层。
该函数返回的值是稳定的，不会随时间变化，因此应用程序可以依赖返回值作为标识符，但可能会随着时间添加新的操作系统内核类型。
在 Windows 上，该函数返回 Windows 内核类型，如“winnt”。在 Unix 系统中，返回与 `uname -s`（小写）的输出相同。
注意：该函数可能会返回令人惊讶的值：为所有运行Linux的操作系统（包括Android）返回“linux”，为所有运行QNX的操作系统返回“qnx”，为Debian/kFreeBSD返回“freebsd”，为macOS和iOS返回“darwin”。有关该应用运行的产品类型，请参见 `productType()`。

### `[static] QString QSysInfo::kernelVersion()`

**作用与语义：**

返回操作系统内核的发布版本。在 Windows 上，返回 NT 内核的版本。在包括 Android 和 macOS 在内的 Unix 系统中，返回的与 `uname -r` 命令返回的相同。在 VxWorks 上，返回由 kernelVersion() 报告的字符串中的数字部分。
如果无法确定版本，该函数可能会返回空字符串。

### `[static] QString QSysInfo::machineHostName()`

**作用与语义：**

如果配置了主机名，返回该机器的主机名称。注意，主机名不保证全局唯一，尤其是自动配置的。
该函数并不保证返回的主机名是完全限定域名（FQDN）。为此，请使用`QHostInfo`将返回的域名解析为FQDN。
该函数返回的效果与`QHostInfo::localHostName()`相同。

### `[static] QByteArray QSysInfo::machineUniqueId()`

**作用与语义：**

如果可以确定唯一ID，则返回该机器的唯一ID。如果无法确定唯一ID，该函数返回一个空字节数组。与`machineHostName()`不同，该函数返回的值很可能是全局唯一的。
唯一ID在网络操作中非常有用，可以在IP地址可能发生变化或机器拥有多个IP地址时，长时间识别该机器。例如，该ID可用于与服务器通信或在共享网络存储中存储设备特定数据。
请注意，在某些系统中，该值会在重启后持续存在，而在另一些系统则不会。应用程序不应在未验证操作系统能力的情况下盲目依赖这一事实。特别是在 Linux 系统中，该 ID 通常是永久性的，且与 D-Bus 机器 ID 匹配，除非是没有自身存储的节点（复制节点）。

### `[static] QString QSysInfo::prettyProductName()`

**作用与语义：**

返回更漂亮的 `productType()` 和 `productVersion()`，包含操作系统类型、代号及其他信息等令牌。该函数的结果适合向用户展示，但不适合长期存储，因为字符串可能会随着 Qt 更新而变化。
如果`productType()`“未知”，该函数将使用`kernelType()`和`kernelVersion()`函数。

### `[static] QString QSysInfo::productType()`

**作用与语义：**

返回该应用程序运行的操作系统产品名称。如果应用程序运行在某种仿真或虚拟化层（如Unix系统的WINE），该函数会检查仿真/虚拟化层。
该函数返回的值是稳定的，不会随时间变化，因此应用程序可以依赖返回值作为标识符，但可能会随着时间添加新的操作系统类型。
Linux 和 Android 注意：对于运行 Android 用户空间的 Linux 系统，尤其是使用仿生库时，该功能返回“android”。对于所有其他 Linux 系统，无论使用哪种 C 库，它都会尝试确定发行版名称并返回该名称。如果确定发行版名称失败，则返回“未知”。
macOS 注意：该函数为所有 macOS 系统返回“macOS”，无论苹果命名规则如何。在此之前，在第五时间段，它返回的是“osx”，同样与苹果命名规则无关。
Darwin、iOS、tvOS 和 watchOS 注：此功能返回 iOS 系统中的“ios”，tvOS 系统返回“tvos”，watchOS 系统返回“watchos”，如果无法确定系统，则返回“darwin”。
FreeBSD 注：该函数返回 Debian/kFreeBSD 的“debian”，否则返回“未知”。
Windows 说明：此函数返回“windows”。
VxWorks 注：该函数返回“vxworks”。
对于其他 Unix 系统，该函数通常返回“未知”。

### `[static] QString QSysInfo::productVersion()`

**作用与语义：**

返回操作系统的成品版本，以字符串形式返回。如果无法确定版本，该函数返回“未知”。
它将在这些系统上恢复Android、iOS、macOS、VxWorks和Windows的完整版本。
典型返回的值如下（注：列表并非详尽）：
- “12”（人造人12号）
- 《36》（Fedora 36）
- “15.5”（iOS 15.5）
- “12.4”（macOS Monterey）
- “22.04”（Ubuntu 22.04）
- “8.6”（watchOS 8.6）
- “11”（Windows 11）
- “Server 2022”（Windows Server 2022）
- 《24.03》（VxWorks 7 - 24.03）
在 Linux 系统中，它会尝试确定发行版版本并返回。Debian/kFreeBSD 也会这样做，因此该函数会返回 Debian 版本。
在所有其他 Unix 类型系统中，该函数总是返回“未知”。
注意：从该函数返回的版本字符串不保证可排序。在 Linux 上，发行版版本可能会意外跳转，请参阅发行版文档中的版本管理实践。

### `enum Endian { BigEndian, LittleEndian, ByteOrder }`

**作用与语义：**

- `QSysInfo::BigEndian`：`0`;大端字节序（也称为网络字节序）
- `QSysInfo::LittleEndian`：`1`;小端位元组
- `QSysInfo::ByteOrder`：`BigEndian or LittleEndian`;等于BigEndian或LittleEndian，具体取决于平台的字节顺序。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSysInfo` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
