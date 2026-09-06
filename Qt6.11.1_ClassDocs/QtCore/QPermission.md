# QPermission

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QPermission` 是平台权限描述类型，用于查询和请求某项设备或系统能力的授权状态。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QPermission` 是 应用权限机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 权限类型本身是描述“要访问什么能力”的轻量值对象，不负责弹窗，也不直接打开摄像头、麦克风或定位设备。真正的状态查询和运行时请求由 `QCoreApplication::checkPermission()`、`requestPermission()` 完成，结果通过回调返回 `QPermission`。

**适用场景：** 先创建具体权限类型，例如 `QCameraPermission{}`，用 `checkPermission()` 查询；未确定时调用 `requestPermission()`，在回调中检查 `permission.status()`，获准后再创建相机、麦克风或定位会话。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 权限描述对象不是设备对象；请求权限不等于设备初始化成功；不要只处理 granted 分支而忽略 denied；还要按平台要求配置构建声明和系统权限说明。

## 2. 依赖与对象关系

- 头文件：`#include <QPermissions>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

权限类型本身是描述“要访问什么能力”的轻量值对象，不负责弹窗，也不直接打开摄像头、麦克风或定位设备。真正的状态查询和运行时请求由 `QCoreApplication::checkPermission()`、`requestPermission()` 完成，结果通过回调返回 `QPermission`。

### 状态、生命周期和线程

**生命周期：** 权限描述对象可以临时构造和按值传递；权限请求的回调必须绑定到仍然有效的 context 或对象生命周期。权限状态可能因平台、用户设置和应用运行阶段改变，不能只在启动时缓存一次。

**状态与结果：** `Granted` 表示当前允许，`Denied` 表示当前拒绝或平台不适用，`Undetermined` 表示还没有得到用户决定。查询得到 `Undetermined` 时要请求权限；请求回调返回后再根据状态决定是否创建真正的设备对象。

**线程与事件循环：** 权限请求依赖应用事件循环和平台 GUI/权限系统，通常在应用主线程发起。回调不要阻塞，也不要在权限结果返回前假定设备已经可用。

## 3. 直接使用

先创建具体权限类型，例如 `QCameraPermission{}`，用 `checkPermission()` 查询；未确定时调用 `requestPermission()`，在回调中检查 `permission.status()`，获准后再创建相机、麦克风或定位会话。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
#include <QCoreApplication>
#include <QPermissions>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    QCameraPermission permission;
    const auto status = app.checkPermission(permission);
    if (status == Qt::PermissionStatus::Undetermined) {
        app.requestPermission(permission, [](const QPermission &result) {
            if (result.status() == Qt::PermissionStatus::Granted) {
                // 现在才创建实际的设备或服务对象
            }
        });
    }
    return app.exec();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QPermission(const T &type)`
- `Qt::PermissionStatus status() const`
- `QMetaType type() const`
- `std::optional<T> value() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `template <typename T, QPermission::if_permission<T> = true> QPermission::QPermission(const T &type)`

**作用与语义：**

从给定的类型许可`type`构建许可。
你不需要显式构造这种类型，因为在检查或请求权限时会自动使用该类型。
只有当 `T` 是类型化权限类之一时，才参与超载解析：
- `QBluetoothPermission`：访问蓝牙外设
- `QCalendarPermission`：访问用户日历
- `QCameraPermission`：使用相机拍照或视频
- `QContactsPermission`：访问用户联系人
- `QLocationPermission`：访问用户位置
- `QMicrophonePermission`：使用麦克风进行监听或录音

### `Qt::PermissionStatus QPermission::status() const`

**作用与语义：**

返回权限状态。

### `QMetaType QPermission::type() const`

**作用与语义：**

返回权限类型。

### `template <typename T, QPermission::if_permission<T> = true> std::optional<T> QPermission::value() const`

**作用与语义：**

返回类型为`T`的类型权限，如果该`QPermission`对象不包含类型许可，则返回`std::nullopt`。
使用`type()`动态选择请求的类型权限。
仅当 `T` 是类型权限类之一时，才参与超载解析：
- `QBluetoothPermission`：访问蓝牙外设
- `QCalendarPermission`：访问用户日历
- `QCameraPermission`：使用相机拍照或视频
- `QContactsPermission`：访问用户联系人
- `QLocationPermission`：访问用户位置
- `QMicrophonePermission`：访问麦克风进行监听或录音

## 6. 深入实践与常见坑

### 生命周期和资源边界

权限描述对象可以临时构造和按值传递；权限请求的回调必须绑定到仍然有效的 context 或对象生命周期。权限状态可能因平台、用户设置和应用运行阶段改变，不能只在启动时缓存一次。

### 状态和错误边界

`Granted` 表示当前允许，`Denied` 表示当前拒绝或平台不适用，`Undetermined` 表示还没有得到用户决定。查询得到 `Undetermined` 时要请求权限；请求回调返回后再根据状态决定是否创建真正的设备对象。

### 线程边界

权限请求依赖应用事件循环和平台 GUI/权限系统，通常在应用主线程发起。回调不要阻塞，也不要在权限结果返回前假定设备已经可用。

### 最容易出现的错误

权限描述对象不是设备对象；请求权限不等于设备初始化成功；不要只处理 granted 分支而忽略 denied；还要按平台要求配置构建声明和系统权限说明。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPermission` 所属机制类型：应用权限机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
