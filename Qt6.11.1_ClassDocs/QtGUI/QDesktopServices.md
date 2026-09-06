# QDesktopServices

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QDesktopServices` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QDesktopServices>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
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

### 静态公有成员

- `bool openUrl(const QUrl &url)`
- `void setUrlHandler(const QString &scheme, QObject *receiver, const char *method)`
- `void unsetUrlHandler(const QString &scheme)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[static] bool QDesktopServices::openUrl(const QUrl &url)`

**作用与语义：**

在用户的桌面环境中，用适当的 Web 浏览器打开给定的 `url`，如果成功则返回 `true`；否则返回 `false`。
如果 URL 是本地文件的引用（即 URL 方案为 "file"），则将使用合适的应用程序打开，而不是 Web 浏览器。
下面的示例展示了如何打开 Windows 文件系统上路径包含空格的文件：
如果指定了 `mailto` URL，则会使用用户的电子邮件客户端打开一个包含 URL 中指定选项的撰写窗口，类似于 Web 浏览器处理 `mailto` 链接的方式。
例如，以下 URL 包含一个收件人 (`user@foo.com`)、主题 (`Test`) 和邮件正文 (`Just a test`)：
警告：尽管许多电子邮件客户端可以发送附件并支持 Unicode，但用户可能配置了没有这些功能的客户端。此外，某些电子邮件客户端（例如 Lotus Notes）在处理长 URL 时存在问题。
警告：返回值为 `true` 表示应用程序已成功请求操作系统在外部应用程序中打开该 URL。外部应用程序仍可能无法启动或无法打开请求的 URL。此结果不会反馈给应用程序。
警告：在 iOS 上传递给此函数的 URL 如果其方案未列在应用程序 Info.plist 文件的 `LSApplicationQueriesSchemes` 键中，将无法加载。更多信息，请参见 Apple 开发者文档中 canOpenURL: 的说明。例如，以下行启用 HTTPS 方案的 URL：
注意：对于 Android Nougat（SDK 24）及以上版本，具有 `file` 方案的 URL 会通过 FileProvider 打开，该 Provider 会首先尝试获取可共享的 `content` 协议 URI。因此，Qt for Android 定义了一个具有 `${applicationId}.qtprovider` 权限的文件提供器，其中 `applicationId` 是应用程序的包名，以避免名称冲突。更多信息请参见设置文件共享。

**官方示例：**

```cpp
 QDesktopServices::openUrl(QUrl("file:///C:/Program Files", QUrl::TolerantMode));
```

### `[static] void QDesktopServices::setUrlHandler(const QString &scheme, QObject *receiver, const char *method)`

**作用与语义：**

将给定`scheme`的处理程序设置为`receiver`对象提供的处理程序`method`。
该函数提供了一种自定义`openUrl()`行为的方法。如果`openUrl()`被调用并指定`scheme`的URL，那么调用`receiver`对象上的指定`method`，而不是`QDesktopServices`启动外部应用程序。
所提供的方法必须实现为只接受单个`QUrl`参数的槽。
如果 setUrlHandler() 用于为已有处理器的方案设置新的处理器，则现有处理器被替换为新的处理器。由于 `QDesktopServices` 不拥有处理器的所有权，替换处理器时不会删除任何对象。
请注意，处理器总是从调用`QDesktopServices::openUrl()`的同一线程中被调用。
你必须在销毁处理对象前调用`unsetUrlHandler()`，这样处理对象的销毁不会与使用该对象`openUrl()`的并发调用重叠。
要使用此功能接收来自 iOS/macOS 上其他应用的数据，你还需要在 Info.plist 文件的 `CFBundleURLSchemes` 列表中添加自定义方案：
欲了解更多信息，请参阅苹果开发者文档《为你的应用定义自定义URL方案》。
警告：无法声称支持一些知名的URL方案，包括http和https。这仅允许用于通用链接。
要申请对 http 和 https 的支持，不允许在 Info.plist 文件中填写上述条目。这只有在你将域名添加到 Entitlements 文件时才可能：
安装应用后，iOS/macOS会在你的域名上搜索/well-known/apple-app-site-association。如果你想收听`https://your.domain.com/help?topic=ABCDEF`，你需要在那里提供以下内容：
欲了解更多信息，请参阅苹果开发者文档以支持相关域名。
要使用此功能接收来自Android上其他应用的数据，你需要在应用清单中的`activity`中添加一个或多个意图过滤器：
欲了解更多信息，请参阅Android开发者文档中的“创建应用内容深度链接”。
要在Android应用中立即打开对应内容，无需用户选择应用，你需要验证链接。要启用验证，请在意图过滤器中添加一个额外参数：
安卓会在应用安装时查找`https://your.domain.com/.well-known/assetlinks.json`。如果你想收听`https://your.domain.com:1337/help`，需要在那里提供以下内容：
更多信息请参见 Android 开发者文档中的 Verify Android 应用链接。

**官方示例：**

```cpp
 class MyHelpHandler : public QObject
 {
     Q_OBJECT
 public:
     // ...
 public slots:
     void showHelp(const QUrl &url);
 };
```

### `[static] void QDesktopServices::unsetUrlHandler(const QString &scheme)`

**作用与语义：**

移除指定`scheme`之前设置的URL处理程序。
在为`scheme`注册的处理程序对象被销毁之前调用该函数，以防止并发`openUrl()`调用继续调用被销毁的处理程序对象。

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

`QDesktopServices` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
