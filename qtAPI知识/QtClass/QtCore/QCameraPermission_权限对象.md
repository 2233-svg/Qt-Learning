# Qt QCameraPermission 深入笔记

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.5  
> 头文件：`#include <QPermissions>`  
> 所属模块：`Qt6::Core`  
> 核心定位：向操作系统请求相机访问权的权限描述对象

## 1. 它解决什么问题

相机不是普通文件或普通 Qt 对象：即使程序能枚举相机设备，操作系统仍可能阻止实际开启镜头、获取预览画面或录像。`QCameraPermission` 用于把“应用需要相机”这件事交给 Qt 的统一权限框架。

它本身不打开设备，也不提供图像数据。真正拍摄仍由 Qt Multimedia 的 `QCamera`、`QMediaCaptureSession` 等类型完成；`QCameraPermission` 应放在它们启动之前。

```text
用户点击“扫描”或“拍照”
          |
          v
checkPermission(QCameraPermission{})
          |
   Granted / Denied / Undetermined
          |
          v
requestPermission() then callback
          |
          v
only after Granted: start QCamera
```

这个分离能让应用准确区分“没有设备”“设备被占用”“用户没有授权”三种完全不同的失败原因。

## 2. 最小使用流程

先检查，再在未决定时异步请求。回调携带的 `QPermission` 才是这次请求的最终状态。

```cpp
#include <QCoreApplication>
#include <QPermission>
#include <QPermissions>

class ScannerController : public QObject
{
public:
    void start()
    {
        const QCameraPermission permission;
        auto *app = QCoreApplication::instance();

        switch (app->checkPermission(permission)) {
        case Qt::PermissionStatus::Granted:
            startCamera();
            return;
        case Qt::PermissionStatus::Denied:
            showCameraDenied();
            return;
        case Qt::PermissionStatus::Undetermined:
            app->requestPermission(permission, this,
                [this](const QPermission &result) {
                    if (result.status() == Qt::PermissionStatus::Granted) {
                        startCamera();
                    } else {
                        showCameraDenied();
                    }
                });
            return;
        }
    }

private:
    void startCamera();
    void showCameraDenied();
};
```

`requestPermission()` 只能从主线程调用。带 `this` 的重载还保证：若控制器在用户回应前销毁，回调不会被调用。这比无 context 的 lambda 更适合页面、控制器和相机预览组件。

## 3. 它和 Qt Multimedia 的边界

| 阶段 | 负责的类型 | 需要处理的问题 | 常见错误 |
| --- | --- | --- | --- |
| 权限检查 | `QCameraPermission` 与 `QCoreApplication` | 系统是否允许访问相机。 | 未获授权就创建并启动采集流程。 |
| 设备选择 | `QMediaDevices` | 当前有哪些可用相机。 | 把没有设备误报为权限被拒绝。 |
| 采集与预览 | `QCamera`、`QMediaCaptureSession` | 打开设备、显示预览或送入图像处理。 | 忽略设备被其他程序占用、断开或启动失败。 |
| 业务处理 | 扫码或拍照逻辑 | 消费帧、保存结果。 | 在权限回调前就访问相机帧。 |

拥有 `Granted` 只是相机启动的必要条件，不是充分条件。授权后仍要处理没有物理相机、设备被占用、系统隐私开关关闭和媒体后端报错。

## 4. 平台声明是必需前置条件

运行时请求之前，应用包还必须声明相机用途：

| 平台 | 需要的构建期声明 | 放置位置 | 作用 |
| --- | --- | --- | --- |
| Apple 平台 | `NSCameraUsageDescription` | 应用的 Info.plist。 | 向系统和用户解释为何使用相机。 |
| Android | `android.permission.CAMERA` | Android manifest。 | 声明应用请求相机能力。 |

未声明时，即使 C++ 中正确调用了 `requestPermission()`，系统也可能拒绝、无法展示预期的对话框，或在打包审核时失败。权限文字应说明真实用途，例如“用于扫描二维码”或“用于拍摄并上传头像”，而不是笼统写“应用需要相机”。

## 5. 三种权限状态如何处理

| 状态 | 表示什么 | UI 或业务动作 | 能否启动相机 |
| --- | --- | --- | --- |
| `Granted` | 用户已授权，或该平台不要求授权。 | 继续初始化媒体设备并启动相机。 | 可以尝试启动。 |
| `Denied` | 用户拒绝，或平台不支持或不允许该权限。 | 停止采集流程，显示说明与可选设置入口。 | 不可以。 |
| `Undetermined` | 尚未得到用户选择。 | 在主线程调用 `requestPermission()`。 | 不能假定可以。 |

系统请求的回调最终只会落在 `Granted` 或 `Denied`，不会仍是 `Undetermined`。不要用循环或定时器反复请求；用户拒绝后，应等待用户再次主动触发功能，或引导其到系统设置。

## 6. 值语义、生命周期与版本

`QCameraPermission` 是轻量、可复制和可移动的值类型，没有 `QObject` 父子关系，也不保存“是否已授权”的状态。可以临时构造 `QCameraPermission{}` 传给 `checkPermission()` 和 `requestPermission()`。

该类从 Qt 6.5 起提供。项目若仍要支持 Qt 6.4 或更早版本，不能直接无条件编译这套 API，需要按最低 Qt 版本设计平台权限兼容层。

## 7. 常见误区

### 7.1 `QCameraPermission{}` 会自动弹窗

不会。构造对象只是描述权限；只有 `QCoreApplication::requestPermission()` 才会发起请求。

### 7.2 `checkPermission()` 返回 `Undetermined` 后直接启动相机

`Undetermined` 表示还不知道用户的决定，不是临时允许。必须请求并等待回调。

### 7.3 把“没有相机”当作“权限被拒绝”

这两个状态来自不同层：权限框架回答能否访问，相机设备 API 回答有没有可用硬件。错误提示和恢复方式应不同。

### 7.4 在工作线程请求权限

Qt 要求从主线程请求权限。工作线程只负责后续耗时图像处理，权限交互要回到主线程。

## API 速查表
### 值类型 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QCameraPermission()` | 创建相机权限请求描述。 | 不会检查、请求或授予权限。 |
| 复制 | `QCameraPermission(const QCameraPermission &other) noexcept` | 复制请求对象。 | 复制不会改变系统授权，也不会重复弹窗。 |
| 移动 | `QCameraPermission(QCameraPermission &&other) noexcept` | 移动请求对象的内部状态。 | 一般用临时对象即可，无需手工优化。 |
| 析构 | `~QCameraPermission()` | 销毁请求对象。 | 不会撤销系统中已经授予的权限。 |
| 赋值 | `QCameraPermission &operator=(const QCameraPermission &other) noexcept` | 复制赋值。 | 仅影响本地请求对象。 |
| 赋值 | `QCameraPermission &operator=(QCameraPermission &&other) noexcept` | 移动赋值。 | 移动后源对象只应销毁或重新赋值。 |
| 交换 | `void swap(QCameraPermission &other) noexcept` | 交换两个权限请求对象。 | 主要用于泛型代码或容器算法。 |

### 与权限框架协作

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 查询 | `QCoreApplication::checkPermission(const QPermission &permission)` | 返回相机权限当前的授权状态。 | 只检查，不显示系统对话框。 |
| 请求 | `QCoreApplication::requestPermission(permission, context, functor)` | 异步请求相机权限，完成后调用回调。 | Qt 6.5 起提供；仅主线程调用，推荐提供 `context`。 |
| 结果 | `QPermission::status() const` | 在回调中读取授权结果。 | 只在 `Granted` 时启动 `QCamera`。 |

---

### 一句话总结

`QCameraPermission` 是启动相机前的系统授权门槛：先检查、未决定时从主线程异步请求、获准后再启动 Qt Multimedia 的采集对象，并把权限失败与设备失败分开处理。
