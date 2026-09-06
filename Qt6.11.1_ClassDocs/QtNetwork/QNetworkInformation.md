# QNetworkInformation

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QNetworkInformation` 是 Qt Network 的“网络Information”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkInformation` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkInformation>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(mytarget PRIVATE Qt6::Network)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

### 状态、生命周期和线程

**生命周期：** manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

**状态与结果：** 请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

**线程与事件循环：** QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

## 3. 直接使用

创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
// manager、reply 和事件循环必须在正确线程中存活。
QNetworkReply *reply = manager->get(request);
connect(reply, &QNetworkReply::finished, this, [reply] {
    const QByteArray body = reply->readAll();
    reply->deleteLater();
});
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum class Feature { Reachability, CaptivePortal, TransportMedium, Metered }`
- `flags Features`
- `enum class Reachability { Unknown, Disconnected, Local, Site, Online }`
- `(since 6.3) enum class TransportMedium { Unknown, Ethernet, Cellular, WiFi, Bluetooth }`

### 属性

- `(since 6.2) isBehindCaptivePortal : bool`
- `(since 6.3) isMetered : bool`
- `reachability : Reachability`
- `(since 6.3) transportMedium : TransportMedium`

### 公有函数

- `QString backendName() const`
- `bool isBehindCaptivePortal() const`
- `bool isMetered() const`
- `QNetworkInformation::Reachability reachability() const`
- `(since 6.3) QNetworkInformation::Features supportedFeatures() const`
- `bool supports(QNetworkInformation::Features features) const`
- `QNetworkInformation::TransportMedium transportMedium() const`

### 信号

- `void isBehindCaptivePortalChanged(bool state)`
- `void isMeteredChanged(bool isMetered)`
- `void reachabilityChanged(QNetworkInformation::Reachability newReachability)`
- `void transportMediumChanged(QNetworkInformation::TransportMedium current)`

### 静态公有成员

- `QStringList availableBackends()`
- `QNetworkInformation * instance()`
- `(since 6.4) bool loadBackendByFeatures(QNetworkInformation::Features features)`
- `(since 6.4) bool loadBackendByName(QStringView backend)`
- `(since 6.3) bool loadDefaultBackend()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QNetworkInformation::Featureflags QNetworkInformation::Features`

**作用与语义：**

列出插件目前可能支持的所有功能。这可以在`QNetworkInformation::loadBackendByFeatures()`中使用。
- `QNetworkInformation::Feature::Reachability`：`0x1`;如果插件支持此功能，那么`reachability`属性将提供有用的结果。否则它总是返回`Reachability::Unknown`。另见`QNetworkInformation::Reachability`。
- `QNetworkInformation::Feature::CaptivePortal`：`0x2`;如果插件支持此功能，那么`isBehindCaptivePortal`属性将提供有用的结果。否则它总是返回`false`。
- `QNetworkInformation::Feature::TransportMedium`：`0x4`;如果插件支持此功能，那么`transportMedium`属性将提供有用的结果。否则它总是返回`TransportMedium::Unknown`。另见`QNetworkInformation::TransportMedium`。
- `QNetworkInformation::Feature::Metered`：`0x8`;如果插件支持此功能，那么`isMetered`属性将提供有用的结果。否则它总是返回`false`。
特征类型是QFlag的typedef<Feature>。它存储了特征值的或组合。

### `enum class QNetworkInformation::Reachability`

**作用与语义：**

- `QNetworkInformation::Reachability::Unknown`：`0`;如果返回该值，则可能已连接，但操作系统尚未确认完全连接，或者该功能不支持。
- `QNetworkInformation::Reachability::Disconnected`：`1`;表示系统可能完全没有连接。
- `QNetworkInformation::Reachability::Local`：`2`;表示系统已连接到网络，但可能只能访问局域网络上的设备。
- `QNetworkInformation::Reachability::Site`：`3`;表示系统已连接到网络，但可能只能访问本地子网或内网上的设备。
- `QNetworkInformation::Reachability::Online`：`4`;表示系统已连接到网络并能够访问互联网。

### `[since 6.3] enum class QNetworkInformation::TransportMedium`

**作用与语义：**

列出目前可连接互联网的已知媒体。
- `QNetworkInformation::TransportMedium::Unknown`：`0`;如果操作系统报告没有活动介质、Qt未识别该活跃介质，或不支持TransportMedium功能，则返回。
- `QNetworkInformation::TransportMedium::Ethernet`：`1`;表示当前激活连接正在使用以太网。注意：当Windows连接到蓝牙个人局网时，该值也可能返回。
- `QNetworkInformation::TransportMedium::Cellular`：`2`;表示当前活跃连接正在使用蜂窝网络。
- `QNetworkInformation::TransportMedium::WiFi`：`3`;表示当前激活连接正在使用Wi-Fi。
- `QNetworkInformation::TransportMedium::Bluetooth`：`4`;表示当前激活连接通过蓝牙连接。
这个枚举是在Qt 6.3引入的。

### `[read-only, since 6.2] isBehindCaptivePortal : bool`

**作用与语义：**

它会告诉你用户的设备是否在囚禁门户后面。
该属性表明用户设备是否已知位于禁闭门户后。此功能依赖操作系统检测禁闭门户，不支持不报告此功能的系统。在不支持此功能的系统中，该功能始终返回`false`。

**如何使用：** 调用 `isBehindCaptivePortal()` 读取当前值；它不会修改应用状态。

### `[read-only, since 6.3] isMetered : bool`

**作用与语义：**

检查当前连接是否被计量。
该属性会返回当前连接是否（已知）计量。你可以以此作为决定应用是否执行某些网络请求或上传的指导因素。例如，在此属性`true`期间，您可能不想上传日志或诊断数据。

**如何使用：** 调用 `isMetered()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 void uploadLogFile()
 {
     ...
 }

 int main(int argc, char *argv[])
 {
     QCoreApplication app(argc, argv);
     ...
         if (netInfo->isMetered()) {
             qWarning() << "Log upload skipped: Current network is metered.";
             app.quit();
         } else {
             uploadLogFile();
         }
     ...
 }
```

### `[read-only] reachability : Reachability`

**作用与语义：**

该属性决定了系统网络连接的当前状态。
表示可预期的连接水平。请注意，这仅基于插件/操作系统报告的数据。在某些情况下，这种检查是已知错误的。例如，在Windows上，默认情况下，Windows通过连接Microsoft拥有的服务器进行“在线”检查。如果该服务器因任何原因被阻挡，系统会假设它没有在线可达性。因此，你不应在尝试连接前先用此检查。

**如何使用：** 调用 `reachability()` 读取当前值；它不会修改应用状态。

### `[read-only, since 6.3] transportMedium : TransportMedium`

**作用与语义：**

该特性为当前应用的主动传输介质提供了支持。
该属性返回应用程序当前的活跃传输介质，在操作系统中提供此类信息。
当当前传输介质发生变化时，信号会发出，例如用户离开`WiFi`网络范围、拔掉以太网线或启用飞行模式时。

**如何使用：** 调用 `transportMedium()` 读取当前值；它不会修改应用状态。

### `[static] QStringList QNetworkInformation::availableBackends()`

**作用与语义：**

返回所有当前可用后端的名称列表。

### `QString QNetworkInformation::backendName() const`

**作用与语义：**

返回当前加载后端的名称。

### `[static] QNetworkInformation *QNetworkInformation::instance()`

**作用与语义：**

返回指向`QNetworkInformation`实例的指针（如果有的话）。如果在后端加载前调用该方法，则返回空指针。

### `[static, since 6.4] bool QNetworkInformation::loadBackendByFeatures(QNetworkInformation::Features features)`

**作用与语义：**

加载支持 `features` 的后端。
如果成功加载所请求的后端或其已经被加载，则返回 `true`。否则返回 `false`。

### `[static, since 6.4] bool QNetworkInformation::loadBackendByName(QStringView backend)`

**作用与语义：**

尝试加载名称与`backend`匹配的后端（大写不敏感）。
返回`true`是否加载了请求的后端，或者是否已经加载。否则返回`false`。

### `[static, since 6.3] bool QNetworkInformation::loadDefaultBackend()`

**作用与语义：**

尝试加载平台默认后端。
注意：从6.7开始，如果平台默认后端不可用或加载失败，它会尝试加载支持`Reachability`的后端。如果也失败，它将退回到只返回所有属性默认值的后端。
这种平台到插件的映射如下：
- `Platform`：插件名称
- `Windows`：networklistmanager
- `Apple (macOS/iOS)`：AppleNetworkInformation
- `Android`：安卓
- `Linux`：网络经理
这个函数是为了方便，之前的逻辑已经足够好了。如果你需要特定插件，应该直接调用`loadBackendByName()`或`loadBackendByFeatures()`。
确定合适的后端加载，并在该后端已加载或成功加载时返回`true`。`false`返回的是其他后端已被加载，或所选后端加载失败。

### `[since 6.3] QNetworkInformation::Features QNetworkInformation::supportedFeatures() const`

**作用与语义：**

返回当前后端支持的所有功能。

### `bool QNetworkInformation::supports(QNetworkInformation::Features features) const`

**作用与语义：**

如果当前加载的后端支持`features`，返回`true`。

### `enum class Feature { Reachability, CaptivePortal, TransportMedium, Metered }`

**作用与语义：**

列出插件目前可能支持的所有功能。这可以在`QNetworkInformation::loadBackendByFeatures()`中使用。
- `QNetworkInformation::Feature::Reachability`：`0x1`;如果插件支持此功能，那么`reachability`属性将提供有用的结果。否则它总是返回`Reachability::Unknown`。另见`QNetworkInformation::Reachability`。
- `QNetworkInformation::Feature::CaptivePortal`：`0x2`;如果插件支持此功能，那么`isBehindCaptivePortal`属性将提供有用的结果。否则它总是返回`false`。
- `QNetworkInformation::Feature::TransportMedium`：`0x4`;如果插件支持此功能，那么`transportMedium`属性将提供有用的结果。否则它总是返回`TransportMedium::Unknown`。另见`QNetworkInformation::TransportMedium`。
- `QNetworkInformation::Feature::Metered`：`0x8`;如果插件支持此功能，那么`isMetered`属性将提供有用的结果。否则它总是返回`false`。
特征类型是QFlag的typedef<Feature>。它存储了特征值的或组合。

### `flags Features`

**作用与语义：**

列出插件目前可能支持的所有功能。这可以在`QNetworkInformation::loadBackendByFeatures()`中使用。
- `QNetworkInformation::Feature::Reachability`：`0x1`;如果插件支持此功能，那么`reachability`属性将提供有用的结果。否则它总是返回`Reachability::Unknown`。另见`QNetworkInformation::Reachability`。
- `QNetworkInformation::Feature::CaptivePortal`：`0x2`;如果插件支持此功能，那么`isBehindCaptivePortal`属性将提供有用的结果。否则它总是返回`false`。
- `QNetworkInformation::Feature::TransportMedium`：`0x4`;如果插件支持此功能，那么`transportMedium`属性将提供有用的结果。否则它总是返回`TransportMedium::Unknown`。另见`QNetworkInformation::TransportMedium`。
- `QNetworkInformation::Feature::Metered`：`0x8`;如果插件支持此功能，那么`isMetered`属性将提供有用的结果。否则它总是返回`false`。
特征类型是QFlag的typedef<Feature>。它存储了特征值的或组合。

### `bool isBehindCaptivePortal() const`

**作用与语义：**

它会告诉你用户的设备是否在囚禁门户后面。
该属性表明用户设备是否已知位于禁闭门户后。此功能依赖操作系统检测禁闭门户，不支持不报告此功能的系统。在不支持此功能的系统中，该功能始终返回`false`。

**如何使用：** 调用 `isBehindCaptivePortal()` 读取当前值；它不会修改应用状态。

### `bool isMetered() const`

**作用与语义：**

检查当前连接是否被计量。
该属性会返回当前连接是否（已知）计量。你可以以此作为决定应用是否执行某些网络请求或上传的指导因素。例如，在此属性`true`期间，您可能不想上传日志或诊断数据。

**如何使用：** 调用 `isMetered()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 void uploadLogFile()
 {
     ...
 }

 int main(int argc, char *argv[])
 {
     QCoreApplication app(argc, argv);
     ...
         if (netInfo->isMetered()) {
             qWarning() << "Log upload skipped: Current network is metered.";
             app.quit();
         } else {
             uploadLogFile();
         }
     ...
 }
```

### `QNetworkInformation::Reachability reachability() const`

**作用与语义：**

该属性决定了系统网络连接的当前状态。
表示可预期的连接水平。请注意，这仅基于插件/操作系统报告的数据。在某些情况下，这种检查是已知错误的。例如，在Windows上，默认情况下，Windows通过连接Microsoft拥有的服务器进行“在线”检查。如果该服务器因任何原因被阻挡，系统会假设它没有在线可达性。因此，你不应在尝试连接前先用此检查。

**如何使用：** 调用 `reachability()` 读取当前值；它不会修改应用状态。

### `QNetworkInformation::TransportMedium transportMedium() const`

**作用与语义：**

该特性为当前应用的主动传输介质提供了支持。
该属性返回应用程序当前的活跃传输介质，在操作系统中提供此类信息。
当当前传输介质发生变化时，信号会发出，例如用户离开`WiFi`网络范围、拔掉以太网线或启用飞行模式时。

**如何使用：** 调用 `transportMedium()` 读取当前值；它不会修改应用状态。

### `void isBehindCaptivePortalChanged(bool state)`

**作用与语义：**

它会告诉你用户的设备是否在囚禁门户后面。
该属性表明用户设备是否已知位于禁闭门户后。此功能依赖操作系统检测禁闭门户，不支持不报告此功能的系统。在不支持此功能的系统中，该功能始终返回`false`。

**如何使用：** 调用 `isBehindCaptivePortalChanged()` 读取当前值；它不会修改应用状态。

### `void isMeteredChanged(bool isMetered)`

**作用与语义：**

检查当前连接是否被计量。
该属性会返回当前连接是否（已知）计量。你可以以此作为决定应用是否执行某些网络请求或上传的指导因素。例如，在此属性`true`期间，您可能不想上传日志或诊断数据。

**如何使用：** 调用 `isMeteredChanged()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 void uploadLogFile()
 {
     ...
 }

 int main(int argc, char *argv[])
 {
     QCoreApplication app(argc, argv);
     ...
         if (netInfo->isMetered()) {
             qWarning() << "Log upload skipped: Current network is metered.";
             app.quit();
         } else {
             uploadLogFile();
         }
     ...
 }
```

### `void reachabilityChanged(QNetworkInformation::Reachability newReachability)`

**作用与语义：**

该属性决定了系统网络连接的当前状态。
表示可预期的连接水平。请注意，这仅基于插件/操作系统报告的数据。在某些情况下，这种检查是已知错误的。例如，在Windows上，默认情况下，Windows通过连接Microsoft拥有的服务器进行“在线”检查。如果该服务器因任何原因被阻挡，系统会假设它没有在线可达性。因此，你不应在尝试连接前先用此检查。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `reachability` 的变化，不要把它当作普通函数主动调用。

### `void transportMediumChanged(QNetworkInformation::TransportMedium current)`

**作用与语义：**

该特性为当前应用的主动传输介质提供了支持。
该属性返回应用程序当前的活跃传输介质，在操作系统中提供此类信息。
当当前传输介质发生变化时，信号会发出，例如用户离开`WiFi`网络范围、拔掉以太网线或启用飞行模式时。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `transportMedium` 的变化，不要把它当作普通函数主动调用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

### 状态和错误边界

请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

### 线程边界

QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

### 最容易出现的错误

不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QNetworkInformation` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
