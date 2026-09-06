# QOperatingSystemVersion

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Operating系统Version”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QOperatingSystemVersion` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QOperatingSystemVersion>`
- 继承自：QOperatingSystemVersionBase
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum OSType { Android, IOS, MacOS, TvOS, WatchOS, …, Unknown }`

### 公有函数

- `QOperatingSystemVersion(QOperatingSystemVersion::OSType osType, int vmajor, int vminor = -1, int vmicro = -1)`
- `bool isAnyOfType(std::initializer_list<QOperatingSystemVersion::OSType> types) const`
- `int majorVersion() const`
- `int microVersion() const`
- `int minorVersion() const`
- `QString name() const`
- `int segmentCount() const`
- `QOperatingSystemVersion::OSType type() const`
- `(since 6.1) QVersionNumber version() const`

### 静态公有成员

- `QOperatingSystemVersion current()`
- `QOperatingSystemVersion::OSType currentType()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QOperatingSystemVersion::OSType`

**作用与语义：**

该枚举为`QOperatingSystemVersion`支持的各种操作系统家族提供了符号名称。
- `QOperatingSystemVersion::Android`：`6`;谷歌安卓操作系统。
- `QOperatingSystemVersion::IOS`：`3`;苹果iOS操作系统。
- `QOperatingSystemVersion::MacOS`：`2`;苹果macOS操作系统。
- `QOperatingSystemVersion::TvOS`：`4`;Apple tvOS 操作系统。
- `QOperatingSystemVersion::WatchOS`：`5`;Apple watchOS 操作系统。
- `QOperatingSystemVersion::VisionOS`：`7`;苹果visionOS操作系统。
- `QOperatingSystemVersion::Windows`：`1`;Microsoft Windows 操作系统。
- `QOperatingSystemVersion::Unknown`：`0`;未知或不支持的操作系统。

### `[constexpr] QOperatingSystemVersion::QOperatingSystemVersion(QOperatingSystemVersion::OSType osType, int vmajor, int vminor = -1, int vmicro = -1)`

**作用与语义：**

构建一个QOperatingSystemVersion，包含操作系统类型`osType`，以及主、次、微版本号分别为`vmajor`、`vminor`和微型`vmicro`。

### `[static] QOperatingSystemVersion QOperatingSystemVersion::current()`

**作用与语义：**

返回一个`QOperatingSystemVersion`，表示当前操作系统及其版本号。

### `[static constexpr] QOperatingSystemVersion::OSType QOperatingSystemVersion::currentType()`

**作用与语义：**

返回当前操作系统类型，无需构建`QOperatingSystemVersion`实例。

### `bool QOperatingSystemVersion::isAnyOfType(std::initializer_list<QOperatingSystemVersion::OSType> types) const`

**作用与语义：**

返回`QOperatingSystemVersion`识别的操作系统类型是否匹配`types`中的任何操作系统类型。

### `[constexpr] int QOperatingSystemVersion::majorVersion() const`

**作用与语义：**

返回主要版本号，即操作系统版本号的第一段。
请参阅主类文档，了解特定操作系统的主要版本号。
-1表示版本号组件未知或缺失。

### `[constexpr] int QOperatingSystemVersion::microVersion() const`

**作用与语义：**

返回微版本号，即操作系统版本号的第三段。
请参阅主类文档，了解某个操作系统的微版本号。
-1表示版本号组件未知或缺失。

### `[constexpr] int QOperatingSystemVersion::minorVersion() const`

**作用与语义：**

返回次要版本号，即操作系统版本号的第二段。
请参阅主类文档，了解特定操作系统的次要版本号。
-1表示版本号组件未知或缺失。

### `QString QOperatingSystemVersion::name() const`

**作用与语义：**

返回由`QOperatingSystemVersion`标识的操作系统类型的字符串表示。

### `[constexpr] int QOperatingSystemVersion::segmentCount() const`

**作用与语义：**

返回版本号中存储的整数。

### `[constexpr] QOperatingSystemVersion::OSType QOperatingSystemVersion::type() const`

**作用与语义：**

返回`QOperatingSystemVersion`识别的操作系统类型。

### `[since 6.1] QVersionNumber QOperatingSystemVersion::version() const`

**作用与语义：**

返回操作系统的版本号。
请参阅主类文档，了解某个操作系统的版本号。

### `[since 6.1] const QOperatingSystemVersion QOperatingSystemVersion::Android10`

**作用与语义：**

该变量对应于 Android 10（版本 10.0，API 级别 29）。
该变量在Qt 6.1中引入。

### `[since 6.1] const QOperatingSystemVersion QOperatingSystemVersion::Android11`

**作用与语义：**

该变量包含对应于 Android 11（版本 11.0，API 级别 30）的版本。
该变量在Qt 6.1中引入。

### `[since 6.5] const QOperatingSystemVersionBase QOperatingSystemVersion::Android12`

**作用与语义：**

该变量对应于 Android 12（版本 12.0，API 级别 31）。
该变量在Qt 6.5引入。

### `[since 6.5] const QOperatingSystemVersionBase QOperatingSystemVersion::Android13`

**作用与语义：**

该变量对应于 Android 13（版本 13.0，API 级别 33）。
该变量在Qt 6.5引入。

### `[since 6.7] const QOperatingSystemVersionBase QOperatingSystemVersion::Android14`

**作用与语义：**

该变量对应于 Android 14（版本 14.0，API 级别 34）。
该变量在Qt 6.7中引入。

### `[since 6.5] const QOperatingSystemVersionBase QOperatingSystemVersion::Android12L`

**作用与语义：**

该变量持有对应于 Android 12L（版本 12.0，API 级别 32）的版本。
该变量在Qt 6.5引入。

### `const QOperatingSystemVersion QOperatingSystemVersion::AndroidJellyBean`

**作用与语义：**

该变量对应于 Android Jelly Bean（版本 4.1，API 级别 16）。

### `const QOperatingSystemVersion QOperatingSystemVersion::AndroidJellyBean_MR1`

**作用与语义：**

该变量对应于 Android Jelly Bean 维护版本 1（版本 4.2，API 级别 17）。

### `const QOperatingSystemVersion QOperatingSystemVersion::AndroidJellyBean_MR2`

**作用与语义：**

该变量对应于 Android Jelly Bean 维护版本 2（版本 4.3，API 级别 18）。

### `const QOperatingSystemVersion QOperatingSystemVersion::AndroidKitKat`

**作用与语义：**

该变量对应于 Android KitKat 的版本（版本 4.4 和 4.4W，API 级别 19 和 20）。

### `const QOperatingSystemVersion QOperatingSystemVersion::AndroidLollipop`

**作用与语义：**

该变量持有对应于 Android Lollipop（版本 5.0，API 级别 21）的版本。

### `const QOperatingSystemVersion QOperatingSystemVersion::AndroidLollipop_MR1`

**作用与语义：**

该变量包含对应于 Android Lollipop 维护版本 1（版本 5.1，API 级别 22）的版本。

### `const QOperatingSystemVersion QOperatingSystemVersion::AndroidMarshmallow`

**作用与语义：**

该变量包含对应于 Android Marshmallow（版本 6.0，API 级别 23）的版本。

### `const QOperatingSystemVersion QOperatingSystemVersion::AndroidNougat`

**作用与语义：**

该变量对应于 Android Nougat（版本 7.0，API 级别 24）。

### `const QOperatingSystemVersion QOperatingSystemVersion::AndroidNougat_MR1`

**作用与语义：**

该变量对应于 Android Nougat 维护版本 1（版本 7.0，API 级别 25）。

### `const QOperatingSystemVersion QOperatingSystemVersion::AndroidOreo`

**作用与语义：**

该变量对应于 Android Oreo 版本（8.0 版，API 级别 26）。

### `[since 6.1] const QOperatingSystemVersion QOperatingSystemVersion::AndroidOreo_MR1`

**作用与语义：**

该变量持有对应 Android Oreo_MR1（版本 8.1，API 级别 27）的版本。
该变量在Qt 6.1中引入。

### `[since 6.1] const QOperatingSystemVersion QOperatingSystemVersion::AndroidPie`

**作用与语义：**

该变量包含对应 Android Pie 版本（版本 9.0，API 级别 28）。
该变量在Qt 6.1中引入。

### `[since 6.0] const QOperatingSystemVersion QOperatingSystemVersion::MacOSBigSur`

**作用与语义：**

该变量对应macOS Big Sur（版本11）。
该变量在Qt 6.0中引入。

### `const QOperatingSystemVersion QOperatingSystemVersion::MacOSCatalina`

**作用与语义：**

该变量持有对应于 macOS Catalina（版本 10.15）的版本。

### `const QOperatingSystemVersion QOperatingSystemVersion::MacOSHighSierra`

**作用与语义：**

该变量对应于 macOS High Sierra（版本 10.13）。

### `const QOperatingSystemVersion QOperatingSystemVersion::MacOSMojave`

**作用与语义：**

该变量持有对应macOS Mojave（版本10.14）的版本。

### `[since 6.3] const QOperatingSystemVersion QOperatingSystemVersion::MacOSMonterey`

**作用与语义：**

该变量对应于 macOS Monterey（版本 12）。
该变量在Qt 6.3引入。

### `[since 6.8] const QOperatingSystemVersionBase QOperatingSystemVersion::MacOSSequoia`

**作用与语义：**

该变量对应于 macOS Sequoia（版本 15）。
该变量在Qt 6.8引入。

### `const QOperatingSystemVersion QOperatingSystemVersion::MacOSSierra`

**作用与语义：**

该变量对应于 macOS Sierra（版本 10.12）。

### `[since 6.5] const QOperatingSystemVersionBase QOperatingSystemVersion::MacOSSonoma`

**作用与语义：**

该变量对应于 macOS Sonoma（版本 14）。
该变量在Qt 6.5引入。

### `[since 6.10] const QOperatingSystemVersionBase QOperatingSystemVersion::MacOSTahoe`

**作用与语义：**

该变量对应于 macOS Tahoe（版本 26）。
该变量在Qt 6.10引入。

### `[since 6.4] const QOperatingSystemVersionBase QOperatingSystemVersion::MacOSVentura`

**作用与语义：**

该变量对应于 macOS Ventura（版本 13）。
该变量在Qt 6.4中引入。

### `const QOperatingSystemVersion QOperatingSystemVersion::OSXElCapitan`

**作用与语义：**

该变量对应OS X El Capitan（版本10.11）。

### `const QOperatingSystemVersion QOperatingSystemVersion::OSXMavericks`

**作用与语义：**

该变量对应于OS X Mavericks（版本10.9）。

### `const QOperatingSystemVersion QOperatingSystemVersion::OSXYosemite`

**作用与语义：**

该变量对应于 OS X Yosemite（版本 10.10）。

### `const QOperatingSystemVersion QOperatingSystemVersion::Windows7`

**作用与语义：**

该变量对应于Windows 7（6.1版本）。

### `const QOperatingSystemVersion QOperatingSystemVersion::Windows8`

**作用与语义：**

该变量包含对应Windows 8（6.2版本）的版本。

### `const QOperatingSystemVersion QOperatingSystemVersion::Windows10`

**作用与语义：**

该变量持有对应通用Windows 10（版本10.0）的版本。

### `[since 6.3] const QOperatingSystemVersionBase QOperatingSystemVersion::Windows11`

**作用与语义：**

该变量保存一个对应Windows 11初始版本（版本10.0.22000）的版本。
该变量在Qt 6.3引入。

### `[since 6.3] const QOperatingSystemVersionBase QOperatingSystemVersion::Windows10_1809`

**作用与语义：**

该变量包含对应Windows 10 2018年10月更新版本1809（版本10.0.17763）的版本。
该变量在Qt 6.3引入。

### `[since 6.3] const QOperatingSystemVersionBase QOperatingSystemVersion::Windows10_1903`

**作用与语义：**

该变量对应于 Windows 10 2019 年 5 月更新版本 1903（版本 10.0.18362）。
该变量在Qt 6.3引入。

### `[since 6.3] const QOperatingSystemVersionBase QOperatingSystemVersion::Windows10_1909`

**作用与语义：**

该变量对应于Windows 10 2019年11月更新版本1909（版本10.0.18363）。
该变量在Qt 6.3引入。

### `[since 6.3] const QOperatingSystemVersionBase QOperatingSystemVersion::Windows10_20H2`

**作用与语义：**

该变量对应Windows 10 2020年10月更新版本20H2（版本10.0.19042）。
该变量在Qt 6.3引入。

### `[since 6.3] const QOperatingSystemVersionBase QOperatingSystemVersion::Windows10_2004`

**作用与语义：**

该变量对应于Windows 10 2020年5月更新版本2004（版本10.0.19041）。
该变量在Qt 6.3引入。

### `[since 6.3] const QOperatingSystemVersionBase QOperatingSystemVersion::Windows10_21H1`

**作用与语义：**

该变量持有对应Windows 10 2021年5月更新版本21H1（版本10.0.19043）的版本。
该变量在Qt 6.3引入。

### `[since 6.3] const QOperatingSystemVersionBase QOperatingSystemVersion::Windows10_21H2`

**作用与语义：**

该变量对应于 Windows 10 2021 年 11 月更新版本 21H2（版本 10.0.19044）。
该变量在Qt 6.3引入。

### `[since 6.5] const QOperatingSystemVersionBase QOperatingSystemVersion::Windows10_22H2`

**作用与语义：**

该变量包含对应Windows 10 2022年10月更新版本22H2（版本10.0.19045）的版本。
该变量在Qt 6.5引入。

### `[since 6.4] const QOperatingSystemVersionBase QOperatingSystemVersion::Windows11_21H2`

**作用与语义：**

该变量对应于 Windows 11 版本 21H2（版本 10.0.22000）。
该变量在Qt 6.4中引入。

### `[since 6.4] const QOperatingSystemVersionBase QOperatingSystemVersion::Windows11_22H2`

**作用与语义：**

该变量持有对应Windows 11版本22H2（版本10.0.22621）的版本。
该变量在Qt 6.4中引入。

### `[since 6.6] const QOperatingSystemVersionBase QOperatingSystemVersion::Windows11_23H2`

**作用与语义：**

该变量包含一个对应Windows 11版本23H2（版本10.0.22631）的版本。
该变量在Qt 6.6引入。

### `[since 6.8.1] const QOperatingSystemVersionBase QOperatingSystemVersion::Windows11_24H2`

**作用与语义：**

该变量包含对应Windows 11版本24H2（版本10.0.26100）的版本。
该变量在Qt 6.8.1中引入。

### `[since 6.11] const QOperatingSystemVersionBase QOperatingSystemVersion::Windows11_25H2`

**作用与语义：**

该变量对应于 Windows 11 版本 25H2（版本 10.0.26200）。
该变量在Qt 6.11中引入。

### `const QOperatingSystemVersion QOperatingSystemVersion::Windows8_1`

**作用与语义：**

该变量对应Windows 8.1（版本6.3）。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QOperatingSystemVersion` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
