# QBluetoothPermission 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPermissions>`  
> 所属模块：`Qt6::Core`  
> 引入版本：Qt 6.5  
> 类型性质：蓝牙权限的可拷贝值对象，不是 `QObject`，也不直接执行扫描、连接或广播。

## 1. 它解决的是什么问题

`QBluetoothPermission` 用来描述应用希望获得的蓝牙系统权限。它交给 `QCoreApplication::checkPermission()` 查询状态，或交给 `QCoreApplication::requestPermission()` 发起系统授权请求。

它本身不会：

- 扫描附近设备。
- 连接蓝牙外设。
- 让其他设备发现本机。
- 弹出权限窗口。

这四件事分别属于具体蓝牙 API、操作系统和 `QCoreApplication` 的权限请求流程。`QBluetoothPermission` 的职责只有一个：把“本次要申请的蓝牙访问范围”表达成一个 Qt 类型。

```cpp
QBluetoothPermission permission;
const auto status = qApp->checkPermission(permission);
```

为什么要专门有这个类型？因为不同平台对蓝牙的授权粒度不同。Qt 用统一的权限对象表达意图，再由平台后端映射到 Android、Apple 等系统的原生权限模型。

## 2. 完整使用流程：先检查，再按需请求

权限请求不应被写成“构造对象后立刻开始工作”。正确的业务流程是：

1. 用户触发一个确实需要蓝牙的动作，例如点击“扫描设备”。
2. 构造并配置 `QBluetoothPermission`。
3. 用 `checkPermission()` 查询当前状态。
4. `Undetermined` 时请求权限，并等待异步回调。
5. `Granted` 时才执行扫描、连接或广播。
6. `Denied` 时降级处理，向用户说明功能不可用或引导其检查系统设置。

```cpp
#include <QBluetoothPermission>
#include <QCoreApplication>

void DevicePage::startScan()
{
    QBluetoothPermission permission;
    permission.setCommunicationModes(QBluetoothPermission::Access);

    switch (qApp->checkPermission(permission)) {
    case Qt::PermissionStatus::Undetermined:
        qApp->requestPermission(permission, this,
                                &DevicePage::startScan);
        return;

    case Qt::PermissionStatus::Denied:
        showBluetoothPermissionHelp();
        return;

    case Qt::PermissionStatus::Granted:
        beginBluetoothDiscovery();
        return;
    }
}
```

这个“回调自己，再重新检查”的写法有一个优点：授权前后都走同一条业务分支，不必复制“权限已允许后开始扫描”的代码。

`requestPermission()` 的结果回调永远不会是 `Undetermined`，只会是 `Granted` 或 `Denied`。权限请求只能从主线程发起。

## 3. 它和 QPermission 的关系

`QBluetoothPermission` 是强类型的权限描述对象。`QPermission` 则是 Qt 在检查和请求时使用的类型擦除包装器。

平时通常不需要手动构造 `QPermission`：

```cpp
QBluetoothPermission bluetoothPermission;
qApp->checkPermission(bluetoothPermission);
```

传入强类型的 `QBluetoothPermission` 后，Qt 自动把它包装成 `QPermission`。请求完成时，回调收到的是 `const QPermission &`；它含有最终状态，并可通过 `value<QBluetoothPermission>()` 取回原来的强类型权限配置。

```cpp
qApp->requestPermission(QBluetoothPermission{}, this,
    [](const QPermission &result) {
        if (result.status() != Qt::PermissionStatus::Granted)
            return;

        const auto requested =
            result.value<QBluetoothPermission>();
        if (!requested)
            return;

        // 根据 requested->communicationModes() 了解请求的范围
    });
```

绝大多数界面代码不必读取 `QPermission::value()`，直接以 `status()` 决定是否继续即可。只有一个回调要处理多种权限类型、或要检查原始权限配置时，才有必要取回。

## 4. CommunicationMode：申请范围的表达

从 Qt 6.6 开始，`QBluetoothPermission` 允许通过 `CommunicationMode` 更精细地描述需要的蓝牙通信范围。

| 枚举值 | 值 | 含义 | 适合的功能 |
| --- | --- | --- | --- |
| `QBluetoothPermission::Access` | `0x01` | 允许本机访问其他蓝牙设备，包括扫描附近设备和连接设备。 | 搜索传感器、连接耳机或外设、读取设备服务。 |
| `QBluetoothPermission::Advertise` | `0x02` | 允许其他蓝牙设备发现本机。 | 把手机或设备作为可发现的蓝牙外设、发出 BLE 广播。 |
| `QBluetoothPermission::Default` | `Access` 加 `Advertise` | Qt 默认采用的配置，同时表达访问外设和被发现的需求。 | 只有确实同时需要两类能力时才使用。 |

`CommunicationModes` 是 `QFlags<CommunicationMode>`，因此可以组合多个模式：

```cpp
QBluetoothPermission permission;
permission.setCommunicationModes(
    QBluetoothPermission::Access
    | QBluetoothPermission::Advertise);
```

如果应用只扫描和连接设备，应明确只申请 `Access`：

```cpp
permission.setCommunicationModes(QBluetoothPermission::Access);
```

这不仅更符合最小权限原则，也能让代码清楚表明产品功能边界。

## 5. Default 不是“空 flags”

`Default` 表示 `Access` 与 `Advertise` 的组合。它不是默认构造的空 `CommunicationModes{}`。

```cpp
QBluetoothPermission permission;

permission.setCommunicationModes({});  // 不要这样写
```

官方规定，向 `setCommunicationModes()` 传递默认构造的空 flags 没有意义：Qt 会发出 `qWarning()`，并回退使用 `Default` 模式。

如果想要默认范围，直接不设置，或显式传入 `Default`：

```cpp
permission.setCommunicationModes(QBluetoothPermission::Default);
```

## 6. 平台差异：模式不是每个平台都能细分

`Access` 和 `Advertise` 的细粒度区分目前主要由 Android 12 及以后版本支持。

- Android 12 之前，任何模式都会映射为完整蓝牙访问。
- Apple 平台上，任何模式同样都会得到完整蓝牙访问的语义。
- 因此，设置 `Access` 不能保证旧 Android 或 Apple 系统只请求“访问其他设备”这一小块能力。

这不是 Qt API 的错误，而是各操作系统权限模型粒度不同。应用仍应按最小意图配置模式，因为在支持细粒度授权的平台上，这个配置会实际影响权限范围。

## 7. 构建期声明和运行期请求缺一不可

运行期调用 `requestPermission()` 不会替代平台项目文件里的权限声明。缺少声明时，系统可能无法正确授权，或者相关权限后端无法正常工作。

### 7.1 Apple 平台

需要在 `Info.plist` 提供蓝牙用途说明：

```xml
<key>NSBluetoothAlwaysUsageDescription</key>
<string>用于搜索并连接附近的设备。</string>
```

用途说明不是装饰文字。它会被系统展示给用户，应准确说明应用为何需要蓝牙。

### 7.2 Android

在 `AndroidManifest.xml` 中声明相应的权限。

Android 11 及以下，也就是 API Level 小于 31，Qt 文档列出：

```xml
<uses-permission android:name="android.permission.BLUETOOTH" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
```

Android 12 及以上，也就是 API Level 大于等于 31，Qt 文档列出：

```xml
<uses-permission android:name="android.permission.BLUETOOTH_ADVERTISE" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
<uses-permission android:name="android.permission.BLUETOOTH_SCAN" />
```

从 Qt 6.8.1 起，针对 API Level 大于等于 31，Qt 不再自动请求 `ACCESS_FINE_LOCATION`。这可能限制部分蓝牙扫描结果。确实需要这些结果时，需要单独请求精确位置权限，并确保 `BLUETOOTH_SCAN` 没有设置 `android:usesPermissionFlags="neverForLocation"`。

使用自定义 Android 清单时，Qt 的权限插入标记也必须保留：

```xml
<!-- %%INSERT_PERMISSIONS -->
```

## 8. 生命周期、线程和回调上下文

`QBluetoothPermission` 是普通值类型。可在栈上构造、复制、移动、保存到成员变量；没有父对象，也不拥有系统资源。

真正要注意的是请求回调：

```cpp
qApp->requestPermission(permission, this,
    [this](const QPermission &result) {
        if (result.status() == Qt::PermissionStatus::Granted)
            beginBluetoothDiscovery();
    });
```

带 `context` 的重载更适合 `QObject` 成员函数：

- 回调在 `context` 所在线程执行。
- 若请求完成前 `context` 已销毁，回调不会被调用。
- 可以避免 lambda 捕获 `this` 后对象已销毁的典型悬空访问问题。

权限请求本身只能由主线程发起。即使蓝牙扫描逻辑随后在工作线程处理，弹出系统权限请求这一动作仍应留在主线程。

## 9. 使用策略：从用户动作出发

不要在应用启动时一次性申请蓝牙、定位、相机等所有权限。更合理的顺序是让用户先表达意图，例如点击“添加设备”后，再说明会搜索附近设备并请求蓝牙权限。

这也决定了库代码的边界：

- 应用界面或业务入口负责请求权限，因为那里最接近用户，能解释原因。
- 库可以用 `checkPermission()` 验证前置条件。
- 库发现未授权时，应通过返回值、错误对象或状态通知上层，而不是自己弹系统授权框。

## 10. 常见错误

### 10.1 把权限对象当蓝牙管理器

`QBluetoothPermission` 不提供扫描、连接、广播 API。它只描述权限请求。实际操作要使用相应 Qt Bluetooth 类型。

### 10.2 忽略 Denied 分支

被拒绝不是异常路径，而是正常的用户选择或平台结果。代码必须有明确降级体验，不能假设请求后一定可以开始扫描。

### 10.3 请求时没有声明平台权限

`Info.plist`、`AndroidManifest.xml` 等构建期配置和运行期 `requestPermission()` 是两层机制，缺一不可。

### 10.4 使用空 CommunicationModes

空 flags 没有业务含义，会产生警告并回退到默认模式。想表达一个模式时，明确使用 `Access`、`Advertise` 或 `Default`。

### 10.5 在工作线程请求

`QCoreApplication::requestPermission()` 只能在主线程调用。后台线程应把“需要授权”的请求交回 UI 或应用主线程处理。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QBluetoothPermission()` | 构造一个蓝牙权限描述对象。 | 默认权限配置为 `Default` 语义；对象本身不会检查或请求系统权限。 |
| 构造 | `QBluetoothPermission(const QBluetoothPermission &other)` | 拷贝另一个权限描述对象。 | 是值语义，适合按值传入 `checkPermission()` 或 `requestPermission()`。 |
| 构造 | `QBluetoothPermission(QBluetoothPermission &&other)` | 移动构造并接管另一个对象的状态。 | 被移动对象只保证可析构或重新赋值。 |
| 析构 | `~QBluetoothPermission()` | 销毁权限描述对象。 | 不撤销已授予的系统权限，也不取消已发出的请求。 |
| 赋值 | `operator=(const QBluetoothPermission &other)` | 拷贝赋值当前权限描述。 | 只是改本地配置，不会自动再次请求系统权限。 |
| 赋值 | `operator=(QBluetoothPermission &&other)` | 移动赋值当前权限描述。 | 不要继续依赖被移动对象原有配置。 |
| 交换 | `void swap(QBluetoothPermission &other) noexcept` | 交换两个权限对象的配置。 | 只交换值对象状态，不触发系统调用。 |
| 枚举 | `CommunicationMode` | 定义蓝牙通信范围枚举。 | Qt 6.6 引入；不同平台对细粒度范围的支持不同。 |
| 枚举值 | `Access` | 允许访问其他蓝牙设备，包括扫描和连接。 | 扫描或连接外设时选择它；不是蓝牙操作 API。 |
| 枚举值 | `Advertise` | 允许其他蓝牙设备发现本机。 | 设备需要被发现或发送 BLE 广播时选择它。 |
| 枚举值 | `Default` | `Access` 和 `Advertise` 的组合，是 Qt 默认配置。 | 不要把它误当成空 flags；只申请实际需要的最小范围。 |
| 标志类型 | `CommunicationModes` | `QFlags<CommunicationMode>`，用于组合通信模式。 | 不能为空；空值会警告并退回 `Default`。 |
| 查询 | `CommunicationModes communicationModes() const` | 返回当前允许请求的蓝牙通信模式。 | Qt 6.6 引入；返回的是配置值，不代表用户已经授权。 |
| 配置 | `void setCommunicationModes(CommunicationModes modes)` | 设置本次权限描述要求的通信模式。 | Qt 6.6 引入；调用后仍须交给 `QCoreApplication` 检查或请求。 |

## 12. 相关但不属于本类的关键 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 权限查询 | `QCoreApplication::checkPermission(permission)` | 返回当前权限状态。 | `Undetermined` 时才应按需请求；它不弹系统对话框。 |
| 权限请求 | `QCoreApplication::requestPermission(permission, functor)` | 异步请求系统权限，完成后调用回调。 | 只能从主线程请求；回调参数是 `const QPermission &`。 |
| 权限请求 | `QCoreApplication::requestPermission(permission, context, functor)` | 带 `QObject` 上下文的异步权限请求。 | `context` 销毁后不调用回调；回调在 context 所在线程执行。 |
| 结果状态 | `Qt::PermissionStatus::Undetermined` | 当前系统尚未确定权限结果。 | 用 `requestPermission()` 取得用户意图；请求回调不会返回它。 |
| 结果状态 | `Qt::PermissionStatus::Granted` | 权限已授予，或平台无需用户授权。 | 仍要处理具体蓝牙操作可能失败的情况。 |
| 结果状态 | `Qt::PermissionStatus::Denied` | 用户拒绝，或平台不支持或不允许该权限。 | 提供降级路径和清晰说明，不要继续假定可访问蓝牙。 |
| 结果包装 | `QPermission::status()` | 读取异步请求完成后的状态。 | 回调中最常用；先判断是否 `Granted`。 |
| 结果包装 | `QPermission::value<QBluetoothPermission>()` | 尝试取回回调中封装的强类型权限配置。 | 类型不匹配返回 `std::nullopt`；多数单一权限回调不必使用。 |

## 13. 一句话总结

`QBluetoothPermission` 是蓝牙权限范围的声明对象：把最小必要的 `Access` 或 `Advertise` 配好，在主线程按用户动作调用 `checkPermission()` 和 `requestPermission()`，并同时完成 Apple 或 Android 的构建期权限声明。
