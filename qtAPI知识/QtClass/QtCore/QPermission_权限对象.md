# Qt QPermission：在权限请求流程中保留“类型、配置与最终状态”

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.5  
> 头文件：`#include <QPermissions>`  
> 所属模块：`Qt6::Core`  
> 类型性质：可复制的非 `QObject` 值包装器；对具体 typed permission 做类型擦除

## 1. 它解决什么问题

Qt 的权限请求不是只传一个字符串。例如定位权限还包含精度和可用范围，蓝牙权限还包含访问/广播模式。调用方希望：

1. 先用具体类型描述要什么权限；
2. 交给通用的 `QCoreApplication` 查询或请求；
3. 在异步回调中拿到最终状态；
4. 必要时恢复原始具体权限及其配置。

`QPermission` 就是这一步中的不透明通用包装器：

```text
QLocationPermission { Precise, WhenInUse }
              |
              v
QPermission { typed value + PermissionStatus }
              |
              v
QCoreApplication::checkPermission / requestPermission
```

它不打开设备、不显示系统对话框、不持有 OS 权限句柄，也不会自行更新权限。真正执行查询和请求的是 `QCoreApplication`。

日常调用通常根本不需要手工构造 `QPermission`：Qt 会把 `QCameraPermission`、`QLocationPermission` 等 typed permission 自动转换为它。

## 2. 支持的 typed permission

Qt 6.11.1 的 `QPermission` 只接受 Qt 定义的 typed permission 类型：

| 类型 | 表示的能力 | 可配置项 |
| --- | --- | --- |
| `QBluetoothPermission` | 使用蓝牙外设 | `CommunicationModes`：访问、广播或两者 |
| `QCalendarPermission` | 访问日历 | `ReadOnly` / `ReadWrite` |
| `QCameraPermission` | 拍照或录像访问相机 | 无额外配置 |
| `QContactsPermission` | 访问联系人 | `ReadOnly` / `ReadWrite` |
| `QLocationPermission` | 访问位置 | `Approximate` / `Precise`，`WhenInUse` / `Always` |
| `QMicrophonePermission` | 录制或监听声音 | 无额外配置 |

`QPermission` 的模板构造和 `value<T>()` 有编译期约束。任意自定义类、普通 enum 或 `QMetaType` 注册类型都不能伪装成 typed permission。

各平台还需满足自身部署要求，例如 Android manifest 权限声明、Apple usage description 或平台允许的权限范围。`QPermission` 统一 C++ 调用方式，不能绕过系统的权限声明和产品政策。

## 3. 推荐的完整流程

以配置精确、前台位置权限为例：

```cpp
#include <QCoreApplication>
#include <QPermissions>

void MapWidget::startLocation()
{
    QLocationPermission permission;
    permission.setAccuracy(QLocationPermission::Precise);
    permission.setAvailability(QLocationPermission::WhenInUse);

    switch (qApp->checkPermission(permission)) {
    case Qt::PermissionStatus::Granted:
        startPreciseLocation();
        return;

    case Qt::PermissionStatus::Denied:
        showLocationSettingsExplanation();
        return;

    case Qt::PermissionStatus::Undetermined:
        qApp->requestPermission(permission, this,
            [this](const QPermission &result) {
                handleLocationPermission(result);
            });
        return;
    }
}

void MapWidget::handleLocationPermission(const QPermission &result)
{
    if (result.status() != Qt::PermissionStatus::Granted) {
        showLocationSettingsExplanation();
        return;
    }

    const auto requested = result.value<QLocationPermission>();
    if (!requested
            || requested->accuracy() != QLocationPermission::Precise
            || requested->availability() != QLocationPermission::WhenInUse) {
        return;
    }

    startPreciseLocation();
}
```

这个结构的重要点：

- `checkPermission()` 只查询，不请求用户授权；
- `Undetermined` 时才发起 `requestPermission()`；
- 请求结果在回调中处理，不能假定调用后立刻有结果；
- `result.status()` 不是 `Undetermined`；
- `value<QLocationPermission>()` 可验证回调携带的具体权限类型及原始请求配置；
- 调用真实位置 API 时仍必须处理设备、服务和运行时失败。

## 4. 状态模型

状态类型是 `Qt::PermissionStatus`：

| 状态 | 值 | 含义 | 下一步 |
| --- | ---: | --- | --- |
| `Undetermined` | 0 | 当前授权意图尚未确定 | 在合适的用户动作后调用 `requestPermission()` |
| `Granted` | 1 | 用户明确授权，或此平台已知不要求授权 | 可以尝试使用实际能力 |
| `Denied` | 2 | 用户明确拒绝，或该权限在平台上不适用/不可访问 | 提供说明、受限功能或设置入口 |

### 4.1 请求结果不会是 `Undetermined`

`QCoreApplication::requestPermission()` 的回调只会得到：

```text
Granted 或 Denied
```

因此回调不应重复请求 Undetermined；应立即按 Granted/Denied 处理。

### 4.2 Android 的特殊语义

Android 平台 API 没有与 Qt 完全对应的 Undetermined 状态。Qt 的规则是：如果应用尚未真正发起请求而 Android 处于 denied 状态，`checkPermission()` 默认报告 `Undetermined`；调用 `requestPermission()` 后，之后的 `checkPermission()` 才会报告非 Undetermined 状态。

不要把 Android 上的第一次 `Undetermined` 解读为“系统已经确认尚未拒绝”。它表达的是“需要走请求流程才能确定 Qt 应向应用报告的最终状态”。

### 4.3 Granted 不是永久成功保证

`Granted` 只表示权限层面允许尝试，不保证实际操作一定成功：

- 相机、麦克风、蓝牙或定位硬件可能不可用；
- 资源可能被别的应用独占；
- 用户可在系统设置中稍后撤销权限；
- 网络、服务状态、设备策略和平台实现仍可能导致失败。

调用真正的资源 API 时仍要检查其错误结果；权限预检不能代替实际调用。

## 5. `QCoreApplication` 上的查询与请求 API

### 5.1 `checkPermission()`

```cpp
Qt::PermissionStatus QCoreApplication::checkPermission(
    const QPermission &permission);
```

查询权限状态，不展示授权对话框。

```cpp
const auto status = qApp->checkPermission(QCameraPermission{});
if (status == Qt::PermissionStatus::Granted)
    takePhoto();
```

适合在用户点击“拍照”“开始录音”“启用定位”后决定是否立即执行或请求授权。不要在应用启动时批量弹出多个请求；先说明为什么需要权限，再在实际功能入口请求，体验通常更好。

### 5.2 `requestPermission()`：带 context 的重载

```cpp
template <typename Functor>
void QCoreApplication::requestPermission(
    const QPermission &permission,
    const QObject *context,
    Functor &&functor);
```

这是大多数 UI 代码应优先使用的版本：

```cpp
qApp->requestPermission(QCameraPermission{}, this,
    [this](const QPermission &result) {
        if (result.status() == Qt::PermissionStatus::Granted)
            takePhoto();
    });
```

语义与生命周期：

- 只能从主线程请求权限；
- 结果就绪后，以 `functor(const QPermission &)` 调用回调；
- 回调在 `context` 对象所属线程执行；
- `context` 在请求完成前被销毁时，Qt 不调用回调；
- 这避免了 UI 销毁后 lambda 捕获 `this` 的常见悬空访问；
- 回调中仍应检查状态，不要默认用户会授权。

### 5.3 `requestPermission()`：无 context 的重载

```cpp
template <typename Functor>
void QCoreApplication::requestPermission(
    const QPermission &permission,
    Functor &&functor);
```

可传自由函数、静态函数或无 context 的 lambda：

```cpp
qApp->requestPermission(QCameraPermission{},
    [](const QPermission &result) {
        logCameraPermission(result.status());
    });
```

没有 context 时，Qt 无法因某个 UI 对象已销毁而自动抑制回调。捕获 `this`、页面对象或临时引用的 UI 代码不应优先选它。

该重载可在 `QT_NO_CONTEXTLESS_CONNECT` 配置中不可用；跨构建配置的库代码应优先使用带 context 的重载。

### 5.4 回调的函数签名

回调必须与下面的形式兼容：

```cpp
void callback(const QPermission &permission);
```

可以是：

- 自由函数；
- 静态成员函数；
- 接受 `const QPermission &` 的 lambda；
- 带 context 的成员函数指针。

不要写成无参 lambda 或接收 `QCameraPermission` 的 lambda；Qt 回传的是通用 `QPermission`，需要时用 `value<T>()` 恢复 typed value。

## 6. `QPermission` 保存了什么

概念上，QPermission 保存两部分：

```text
PermissionStatus
       +
一个 typed permission 的值及其 QMetaType
```

因此，位置请求的精度/可用范围等配置会随请求进入回调：

```cpp
QLocationPermission request;
request.setAccuracy(QLocationPermission::Precise);

qApp->requestPermission(request, this,
    [](const QPermission &result) {
        const auto original = result.value<QLocationPermission>();
        if (original)
            qDebug() << original->accuracy();
    });
```

这不是 OS 授权令牌。`value<T>()` 取回的是 Qt 发起请求时包装的 typed permission 值，而不是系统实时返回的权限详情。

## 7. 生命周期、复制与默认构造

`QPermission` 不是 `QObject`：

- 没有父对象、线程亲和性或信号；
- 可以按值复制、移动、存入容器和跨线程传递；
- 内部通过 `QVariant` 保存 typed permission 值；
- 它不拥有系统资源，也不需要手工释放。

公开头文件还提供：

```cpp
explicit QPermission() = default;
```

默认构造结果的 status 是 `Undetermined`，但没有封装任何 typed permission，`type()` 对应空 `QVariant` 的元类型，`value<T>()` 对所有合法 T 都返回 `std::nullopt`。

这种空对象适合作为“尚未收到回调”的普通值占位，不应传给 `checkPermission()` 或 `requestPermission()` 充当真实权限描述。业务代码应从具体 typed permission 构造请求。

## 8. 常见错误

### 8.1 手工构造 `QPermission` 再传入 API

通常直接传 typed permission：

```cpp
qApp->checkPermission(QMicrophonePermission{});
```

Qt 会转换。只有在通用回调、动态分派或日志中才需要直接处理 QPermission。

### 8.2 把 `checkPermission()` 当作请求

它不弹窗。遇到 `Undetermined` 后，需要调用 `requestPermission()`。

### 8.3 从工作线程调用 `requestPermission()`

权限只能从主线程请求。将用户交互和 request 调用安排到 UI/main thread。

### 8.4 用无 context lambda 捕获页面 `this`

请求完成时页面可能已经销毁。使用 `requestPermission(permission, this, ...)`，让 context 生命周期自动取消回调。

### 8.5 不处理 Android 第一次 Undetermined

Android 第一次检查可能是未请求前的 Qt 映射状态。按通用流程请求一次，再依据最终 Granted/Denied 处理。

### 8.6 在回调中假设结果仍是原始具体类型

回调参数始终是 QPermission。先检查 `status()`，再通过 `value<T>()` 获取 `std::optional<T>`，不能直接静态转换。

### 8.7 把 Denied 全部归因于用户拒绝

Denied 也可能表示该能力对应用不适用、不可访问或平台不支持。提示内容应避免不准确地责怪用户。

### 8.8 获得 Granted 后不检查实际资源 API

权限是前置条件之一，不是设备和服务成功的证明。始终处理相机、位置、蓝牙或媒体 API 自己的错误。

## 9. 逐项 API 说明

### 9.1 `QPermission()`

```cpp
explicit QPermission() = default;
```

构造空权限包装器。

- 初始 `status()` 为 `Undetermined`；
- 不包含 typed permission；
- `value<T>()` 返回 `std::nullopt`；
- 普通权限请求不应使用空对象；
- 可用于延后赋值或泛型容器占位。

### 9.2 `QPermission(const T &type)`

```cpp
template <typename T>
QPermission(const T &type);
```

从合法 typed permission 构造通用包装器。

- 仅接受 Qt 支持的权限类型；
- 保存 type 的值和配置，例如 location accuracy；
- 通常由 `checkPermission()` / `requestPermission()` 的形参隐式转换自动完成；
- 不会执行查询、请求或显示对话框；
- 新构造 wrapper 的 status 初始仍是 `Undetermined`，最终状态由 QCoreApplication 在查询/请求流程中产生。

### 9.3 `status() const`

```cpp
Qt::PermissionStatus status() const;
```

返回当前包装器携带的权限状态。

- 查询结果或回调结果的主要判断入口；
- request 回调中只会是 `Granted` 或 `Denied`；
- status 是某时刻的判断，不是永久授权保证；
- 空 wrapper 返回其初始 `Undetermined`。

### 9.4 `type() const`

```cpp
QMetaType type() const;
```

返回内部 typed permission 的元类型。

- 用于运行时动态决定该取哪一种 `value<T>()`；
- 空 wrapper 返回空 `QVariant` 对应的元类型；
- 它返回的是 Qt 类型信息，不是 Android/iOS/Windows 的权限字符串；
- 静态已知类型时，直接调用 `value<T>()` 更简单。

### 9.5 `value<T>() const`

```cpp
template <typename T>
std::optional<T> value() const;
```

尝试按指定 typed permission 类型取回原始请求值。

- 内部类型与 T 匹配时返回值；
- 类型不同或为空时返回 `std::nullopt`；
- T 必须是 Qt 支持的 typed permission；
- 在 request 回调中可验证配置没有被错误地按其它权限处理；
- 返回的是值副本，修改它不会改变已经提交的权限请求。

### 9.6 Debug stream

```cpp
QDebug operator<<(QDebug debug, const QPermission &permission);
```

未定义 `QT_NO_DEBUG_STREAM` 时可用于诊断输出。

- 用于开发日志，不是稳定序列化格式；
- 不应把日志内容当作权限决策依据；
- 日志也应遵循产品隐私策略，避免不必要地记录敏感上下文。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| typed 描述 | `QCameraPermission{}` 等 | 表达要请求的具体能力 | 日常调用直接传 typed permission，不必手工包装 |
| 查询 | `QCoreApplication::checkPermission(permission)` | 同步读取当前状态 | 不弹窗；Undetermined 后才请求 |
| 请求 | `requestPermission(permission, context, callback)` | 发起系统权限流程 | 主线程调用；优先带 context |
| 请求 | `requestPermission(permission, callback)` | 无 context 地发起请求 | 不要捕获可能销毁的 UI 对象 |
| 状态 | `Qt::PermissionStatus::Undetermined` | 尚需请求确定用户意图 | Android 第一次检查有特殊映射 |
| 状态 | `Granted` | 可尝试使用能力 | 仍需处理实际资源 API 失败 |
| 状态 | `Denied` | 拒绝、不可访问或不适用 | 不应一概认定是用户点击拒绝 |
| 包装 | `QPermission(type)` | 保存 typed value 与类型信息 | 不查询、不请求；通常由 API 隐式完成 |
| 回调 | `status()` | 读取本次结果 | 请求回调中不会是 Undetermined |
| 类型 | `type()` | 读取内部 QMetaType | 适合动态分派 |
| 取值 | `value<T>()` | 取回匹配类型的原始 typed permission | 返回 `std::optional<T>`，必须检查 |
| 调试 | `operator<<(QDebug, permission)` | 输出诊断信息 | 不用于持久化或授权决策 |
| 平台配置 | manifest / usage description | 声明平台需要的权限 | QPermission 不能绕过部署配置 |

## 11. 一句话总结

`QPermission` 是 Qt 权限系统中的通用结果包装器：应用以 typed permission 发起查询或请求，在 `QCoreApplication` 的回调里用 `status()` 判断 Granted/Denied，并用 `value<T>()` 安全恢复原始权限类型与配置；权限请求必须在主线程发起，真实资源调用仍要自行处理失败。
