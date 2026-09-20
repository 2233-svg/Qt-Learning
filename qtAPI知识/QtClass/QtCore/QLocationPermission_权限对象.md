# Qt QLocationPermission 深入笔记

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.5  
> 头文件：`#include <QPermissions>`  
> 所属模块：`Qt6::Core`  
> 类型性质：描述位置权限需求的轻量值类型  
> 相关类型：`QCoreApplication`、`QPermission`、`Qt::PermissionStatus`、Qt Location

## 1. 它解决什么问题

`QLocationPermission` 描述应用希望访问用户位置的权限范围。它解决的是“应用需要什么级别的位置授权”这个问题，而不是“如何读取经纬度”：

- `Accuracy` 描述希望得到近似位置还是精确位置；
- `Availability` 描述只在应用使用时可用，还是允许后台持续可用；
- `QCoreApplication::checkPermission()` 负责检查当前授权状态；
- `QCoreApplication::requestPermission()` 负责从主线程发起系统请求；
- 真正读取位置仍由 Qt Location、平台位置 API 或其他业务模块完成。

它本身不会弹窗、不会请求权限、不会开启定位服务，也不保存“用户已经授权”的结果。它只是传给权限框架的**请求描述对象**。

## 2. 实际使用场景

### 2.1 前台地图或天气功能

地图中心定位、附近门店、天气定位通常只需要应用处于前台时使用位置：

```cpp
QLocationPermission permission;
permission.setAccuracy(QLocationPermission::Approximate);
permission.setAvailability(QLocationPermission::WhenInUse);
```

这是默认请求：近似精度、仅使用期间可用。它通常比后台精确定位更容易获得用户接受，也更符合最小权限原则。

### 2.2 导航或轨迹记录

需要更高精度时可以请求：

```cpp
QLocationPermission permission;
permission.setAccuracy(QLocationPermission::Precise);
permission.setAvailability(QLocationPermission::Always);
```

这表示应用向系统声明更强的需求，但**不保证平台最终一定提供精确位置或后台位置**。用户设置、系统策略、设备能力、应用声明和平台版本都可能限制最终行为。

### 2.3 正确的检查和请求流程

```cpp
#include <QCoreApplication>
#include <QPermissions>

void requestLocation(QObject *context)
{
    QLocationPermission permission;
    permission.setAccuracy(QLocationPermission::Precise);
    permission.setAvailability(QLocationPermission::WhenInUse);

    QCoreApplication *app = QCoreApplication::instance();
    if (!app)
        return;

    const Qt::PermissionStatus status = app->checkPermission(permission);
    if (status == Qt::PermissionStatus::Granted) {
        // 现在可以尝试启动位置业务。
        return;
    }

    if (status == Qt::PermissionStatus::Denied) {
        // 显示解释或设置入口；不要假装权限已可用。
        return;
    }

    app->requestPermission(permission, context,
        [](const QPermission &result) {
            if (result.status() == Qt::PermissionStatus::Granted) {
                // 只有这里确认授权后，才启动位置业务。
            } else {
                // 请求完成但被拒绝，停止需要位置的操作。
            }
        });
}
```

`checkPermission()` 返回 `Undetermined` 时才表示需要通过 `requestPermission()` 询问用户。请求回调的结果不会是 `Undetermined`，只会是 `Granted` 或 `Denied`。

## 3. 它和权限框架的边界

| 层次 | 类型或 API | 负责什么 | 不负责什么 |
| --- | --- | --- | --- |
| 请求描述 | `QLocationPermission` | 记录精度和可用性需求 | 不检查、不弹窗、不读取位置 |
| 类型擦除包装 | `QPermission` | 传递 typed permission 和结果状态 | 不替代具体权限对象的配置 |
| 状态查询 | `QCoreApplication::checkPermission()` | 查询当前系统授权状态 | 不会主动请求用户 |
| 系统请求 | `QCoreApplication::requestPermission()` | 在系统层请求用户授权 | 不保证系统一定显示对话框 |
| 位置服务 | Qt Location 或平台 API | 获取实际位置、处理 provider | 不负责声明应用权限 |
| 平台声明 | Info.plist、Android manifest 等 | 让系统知道应用用途和能力 | 不等于用户已经授权 |

即使状态是 `Granted`，后续定位仍可能因为没有可用 provider、设备关闭定位服务、网络不可用、权限被系统设置降级或业务对象初始化失败而不能工作。权限成功不是定位成功的同义词。

## 4. 构建与包含

### 4.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 4.2 头文件

```cpp
#include <QPermissions>
```

`QLocationPermission` 和 `QPermission` 都由 `QPermissions` 提供，不是单独的 `qlocationpermission.h` 公共头文件。

### 4.3 qmake

```qmake
QT += core
```

项目还必须启用 Qt 的 permissions 配置；常规 Qt 构建默认提供该模块，但裁剪版构建需要确认权限功能没有被禁用。

## 5. 默认值和两种策略枚举

### 5.1 默认权限请求

默认构造的 `QLocationPermission` 请求：

```cpp
QLocationPermission permission;

Q_ASSERT(permission.accuracy() ==
         QLocationPermission::Approximate);
Q_ASSERT(permission.availability() ==
         QLocationPermission::WhenInUse);
```

这两个默认值只描述请求对象，不代表当前系统授权状态。要知道用户是否已授权，必须调用 `checkPermission()`。

### 5.2 `Accuracy`

```cpp
enum Accuracy : quint8 {
    Approximate,
    Precise
};
```

| 值 | 语义 | 常见用途 |
| --- | --- | --- |
| `Approximate` | 请求近似位置 | 附近内容、天气、粗粒度区域推荐 |
| `Precise` | 请求精确位置 | 导航、轨迹、精确地理围栏 |

`Precise` 是应用的期望，不是对最终坐标误差的承诺。平台可能要求用户单独选择精确或近似位置，也可能受设备和系统设置限制。

### 5.3 `Availability`

```cpp
enum Availability : quint8 {
    WhenInUse,
    Always
};
```

| 值 | 语义 | 常见用途 |
| --- | --- | --- |
| `WhenInUse` | 应用处于使用状态时可用 | 前台地图、一次性定位 |
| `Always` | 需要后台也可用 | 后台轨迹、后台地理围栏、持续导航 |

`Always` 会触发更严格的平台声明和用户审核。没有真实后台需求时不要请求它。

## 6. 平台声明是运行时请求的前置条件

构造 `QLocationPermission` 和调用 `requestPermission()` 不能替代平台打包声明。Qt 6.11.1 文档列出的关键要求如下。

### 6.1 macOS

需要在应用的 `Info.plist` 中声明：

```text
NSLocationUsageDescription
```

它用于向系统和用户解释应用为什么需要位置。

### 6.2 iOS

至少需要：

```text
NSLocationWhenInUseUsageDescription
```

如果请求 `QLocationPermission::Always`，还需要：

```text
NSLocationAlwaysAndWhenInUseUsageDescription
```

权限文字应说明真实用途，例如“用于在骑行过程中记录路线”，而不是泛化的“需要位置权限”。

### 6.3 Android

根据请求值声明对应权限：

| Qt 请求 | Android 权限 |
| --- | --- |
| `Approximate` | `android.permission.ACCESS_COARSE_LOCATION` |
| `Precise` | `android.permission.ACCESS_FINE_LOCATION` |
| `Always` | `android.permission.ACCESS_BACKGROUND_LOCATION` |

`ACCESS_BACKGROUND_LOCATION` 需要与 `ACCESS_FINE_LOCATION`、`ACCESS_COARSE_LOCATION` 中的一个或两个组合使用。只声明后台权限而没有前台位置权限，不能构成完整的后台定位请求。

平台声明缺失时，运行时调用可能无法显示预期系统对话框、直接被拒绝或无法通过平台审核。不要把 C++ 权限逻辑当作打包配置的替代品。

## 7. 主线程和异步请求边界

`QCoreApplication::requestPermission()` 只能从主线程调用。系统授权是异步流程，不能写成同步等待：

```cpp
// 错误思路：请求后立刻继续访问位置。
app->requestPermission(permission, this, callback);
startLocationProvider(); // 此时授权结果尚未回调，不应这样假定。
```

应在回调中确认 `Granted` 后，再启动依赖位置的业务：

```cpp
app->requestPermission(permission, this,
    [this](const QPermission &result) {
        if (result.status() != Qt::PermissionStatus::Granted)
            return;

        startLocationProvider();
    });
```

带 `context` 的重载更适合窗口、页面和控制器：如果 `context` 在请求完成前销毁，Qt 不会再调用这个回调。无 context 的重载需要调用方自己保证捕获对象和回调生命周期安全。

## 8. `QPermission` 回调结果如何读取

### 8.1 读取状态

```cpp
void onPermissionResult(const QPermission &permission)
{
    switch (permission.status()) {
    case Qt::PermissionStatus::Granted:
        // 可以继续执行需要位置权限的业务。
        break;
    case Qt::PermissionStatus::Denied:
        // 不能继续执行受保护的位置业务。
        break;
    case Qt::PermissionStatus::Undetermined:
        // requestPermission() 的回调不应出现这个状态。
        break;
    }
}
```

`Undetermined` 只表示当前查询还没有明确结果。它可能出现在 `checkPermission()` 的返回值中，但不会作为一次 `requestPermission()` 完成后的结果返回。

Android 的平台权限 API 没有完全相同的 `Undetermined` 概念，因此 Qt 在某些情况下会在第一次请求前把状态表现为 `Undetermined`；请求完成后再报告明确状态。

### 8.2 恢复原始 typed permission

```cpp
app->requestPermission(permission, this,
    [](const QPermission &result) {
        const std::optional<QLocationPermission> requested =
            result.value<QLocationPermission>();

        if (!requested ||
            result.status() != Qt::PermissionStatus::Granted) {
            return;
        }

        if (requested->accuracy() == QLocationPermission::Precise) {
            // 这是本次请求期望的精度，不是一次位置测量结果。
        }
    });
```

`value<QLocationPermission>()` 返回 `std::optional<QLocationPermission>`：

- 类型匹配且包装中包含该权限时返回值；
- 类型不匹配或包装为空时返回 `std::nullopt`；
- 它恢复的是 typed permission 的请求描述，不是系统测得的经纬度，也不表示平台一定兑现了全部请求级别。

如果只需要判断授权是否成功，读取 `status()` 即可，不必为了普通流程恢复 `value<T>()`。

## 9. 权限请求的推荐工作流

### 9.1 最小权限优先

```cpp
QLocationPermission permission;
permission.setAccuracy(QLocationPermission::Approximate);
permission.setAvailability(QLocationPermission::WhenInUse);
```

只有功能确实需要更精确或后台能力时，才分别升级一个维度。把 `Precise` 和 `Always` 一次性都请求，会增加用户疑虑、平台配置和审核成本。

### 9.2 在用户主动触发时请求

不要在应用启动时无上下文地弹出位置请求。更好的时机是用户点击“使用我的位置”“开始导航”或“记录路线”后，先用界面说明用途，再进行权限检查和请求。

### 9.3 将权限失败和定位失败分开

```cpp
void startLocationFeature()
{
    QLocationPermission permission;
    permission.setAccuracy(QLocationPermission::Approximate);
    permission.setAvailability(QLocationPermission::WhenInUse);

    const Qt::PermissionStatus status =
        QCoreApplication::instance()->checkPermission(permission);

    if (status == Qt::PermissionStatus::Denied) {
        showPermissionDenied();
        return;
    }

    if (status == Qt::PermissionStatus::Undetermined) {
        requestPermissionThenStart(permission);
        return;
    }

    startProviderAndHandleProviderErrors();
}
```

授权通过后仍要处理位置 provider 的错误、无信号、超时、设备设置和服务状态。

## 10. 值语义、生命周期和线程

### 10.1 轻量值对象

`QLocationPermission` 是可复制、可移动、可交换的值类型：

```cpp
QLocationPermission first;
first.setAccuracy(QLocationPermission::Precise);

QLocationPermission second = first;
QLocationPermission third = std::move(second);
first.swap(third);
```

复制、移动和 `swap()` 只操作请求描述对象，不会重复请求权限、撤销权限或修改系统设置。

### 10.2 它不保存授权状态

下面两个概念完全不同：

```cpp
QLocationPermission request; // 需要什么权限

const Qt::PermissionStatus status =
    QCoreApplication::instance()->checkPermission(request); // 系统给了什么状态
```

修改 `request` 的属性不会自动让系统授予权限；系统状态也不会反向写入这个对象的 `accuracy()` 或 `availability()`。

### 10.3 数据竞争和线程边界

值对象本身没有 QObject 线程归属，可以作为参数传递或复制。但权限请求 API 的调用必须发生在主线程，系统回调也应按 Qt 的对象生命周期和事件循环规则处理。后台线程可以处理已经取得的位置数据，但不应直接发起权限交互。

## 11. 常见误区

### 11.1 构造对象会自动弹窗

不会：

```cpp
QLocationPermission permission;
// 这里只创建请求描述，不会展示任何系统 UI。
```

只有 `checkPermission()` 和 `requestPermission()` 与系统权限状态交互；其中只有后者会发起请求流程。

### 11.2 `Granted` 等于“精确位置一定可用”

`Granted` 表示系统接受了这次权限请求或该平台不要求用户授权，不等于每次位置测量都有精确坐标。仍需检查位置 provider 的实际输出和错误。

### 11.3 用 `Always` 代替前台权限

后台能力不是前台权限的替代品。Android 需要后台权限与前台位置权限组合；Apple 平台也有单独的用途声明要求。

### 11.4 把 `accuracy()` 当成当前测量精度

```cpp
const auto requested = permission.accuracy();
```

它只回答“这个请求对象希望的精度”。实际位置对象的精度、水平误差和 provider 状态要从位置服务 API 查询。

### 11.5 在工作线程请求权限

`requestPermission()` 只能在主线程调用。工作线程应通过信号、`QMetaObject::invokeMethod()` 或其他主线程调度方式请求主线程执行权限流程。

### 11.6 每次失败都立刻重复请求

系统权限请求不是可以无限重试的普通函数。用户拒绝后应说明原因、提供设置入口或等待用户再次主动触发；不要用定时器不断弹窗。

### 11.7 忽略平台打包声明

C++ API 正确并不代表平台包正确。缺少 Info.plist 或 Android manifest 声明时，运行时行为可能与桌面测试不同。

## 12. 逐项 API 说明

### 12.1 `enum QLocationPermission::Accuracy`

控制请求的位置精度：

| 常量 | 值 | 语义 |
| --- | --- | --- |
| `QLocationPermission::Approximate` | `0` | 请求近似位置。 |
| `QLocationPermission::Precise` | `1` | 请求精确位置。 |

它是请求级别，不是实际位置测量的误差保证。

### 12.2 `enum QLocationPermission::Availability`

控制请求希望在什么时间范围内可用：

| 常量 | 值 | 语义 |
| --- | --- | --- |
| `QLocationPermission::WhenInUse` | `0` | 仅应用使用时请求可用。 |
| `QLocationPermission::Always` | `1` | 请求应用在后台也可使用。 |

后台可用能力需要额外的平台声明和用户授权。

### 12.3 `setAccuracy()`

```cpp
void setAccuracy(QLocationPermission::Accuracy accuracy);
```

设置请求的精度需求。它只修改当前对象，不触发系统请求，也不改变已经授予的权限。

### 12.4 `accuracy()`

```cpp
QLocationPermission::Accuracy accuracy() const;
```

返回当前对象保存的精度需求。默认是 `Approximate`。

### 12.5 `setAvailability()`

```cpp
void setAvailability(QLocationPermission::Availability availability);
```

设置请求的可用性需求。设置为 `Always` 后，调用方仍需提供对应平台声明，并等待系统实际结果。

### 12.6 `availability()`

```cpp
QLocationPermission::Availability availability() const;
```

返回当前对象保存的可用性需求。默认是 `WhenInUse`。

### 12.7 由头文件宏提供的值语义 API

`QPermissions` 头文件通过公共宏为 `QLocationPermission` 提供以下生命周期 API。它们虽然不在 `qlocationpermission-members.html` 的类页成员列表中，但属于实际可用的公开接口：

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `QLocationPermission()` | 构造默认请求 | 默认 `Approximate + WhenInUse`；不请求系统权限。 |
| `QLocationPermission(const QLocationPermission &other) noexcept` | 复制构造 | 只复制请求描述。 |
| `QLocationPermission(QLocationPermission &&other) noexcept` | 移动构造 | 源对象可销毁或重新赋值，不表示权限迁移。 |
| `~QLocationPermission()` | 析构 | 不撤销系统授权。 |
| `QLocationPermission &operator=(const QLocationPermission &other) noexcept` | 复制赋值 | 只修改本地对象。 |
| `QLocationPermission &operator=(QLocationPermission &&other) noexcept` | 移动赋值 | 只转移本地描述状态。 |
| `void swap(QLocationPermission &other) noexcept` | 交换请求对象 | 快速且不触发系统交互。 |

## API 速查表

### 13.1 成员类型

| API | 作用 | 使用时重点 |
| --- | --- | --- |
| `enum QLocationPermission::Accuracy` | 描述精度请求 | `Precise` 是期望，不是实际误差承诺。 |
| `QLocationPermission::Approximate` | 请求近似位置 | 适合附近内容、天气和粗粒度推荐。 |
| `QLocationPermission::Precise` | 请求精确位置 | 适合导航和轨迹，但需要更强平台授权。 |
| `enum QLocationPermission::Availability` | 描述时间范围请求 | `Always` 需要后台声明和更严格用户授权。 |
| `QLocationPermission::WhenInUse` | 仅使用期间可用 | 默认值，适合前台功能。 |
| `QLocationPermission::Always` | 请求后台也可用 | 不是前台权限替代品，平台组合要求更严格。 |

### 13.2 成员函数

| API | 作用 | 使用时重点 |
| --- | --- | --- |
| `void setAccuracy(Accuracy accuracy)` | 设置精度需求 | 只改当前请求对象，不会请求或授予权限。 |
| `Accuracy accuracy() const` | 读取精度需求 | 默认 `Approximate`；不是当前位置测量精度。 |
| `void setAvailability(Availability availability)` | 设置可用性需求 | `Always` 需要平台声明和实际用户授权。 |
| `Availability availability() const` | 读取可用性需求 | 默认 `WhenInUse`；不是系统当前授权状态。 |

### 13.3 头文件公开的生命周期 API

| API | 作用 | 使用时重点 |
| --- | --- | --- |
| `QLocationPermission()` | 构造请求对象 | 不弹窗、不检查、不改变系统状态。 |
| `QLocationPermission(const QLocationPermission &) noexcept` | 复制对象 | 不会重复请求权限。 |
| `QLocationPermission(QLocationPermission &&) noexcept` | 移动对象 | 仅移动本地描述状态。 |
| `~QLocationPermission()` | 销毁对象 | 不撤销已经授予的权限。 |
| `operator=(const QLocationPermission &) noexcept` | 复制赋值 | 不影响系统权限。 |
| `operator=(QLocationPermission &&) noexcept` | 移动赋值 | 只影响本地对象。 |
| `swap(QLocationPermission &) noexcept` | 交换对象 | 不触发系统交互。 |

### 13.4 必要的协作 API

| API | 作用 | 使用时重点 |
| --- | --- | --- |
| `QCoreApplication::checkPermission(const QPermission &)` | 查询授权状态 | `Undetermined` 时应请求；只检查，不弹窗。 |
| `QCoreApplication::requestPermission(const QPermission &, Functor &&)` | 异步请求权限 | Qt 6.5；只能主线程调用；回调收到 `const QPermission &`。 |
| `QCoreApplication::requestPermission(const QPermission &, const QObject *, Functor)` | 带生命周期上下文地请求 | 上下文销毁后不再调用回调，适合页面和控制器。 |
| `QPermission::status() const` | 读取系统请求结果 | 回调结果只应是 `Granted` 或 `Denied`。 |
| `QPermission::type() const` | 查询包装内的元类型 | 适合动态判断权限类型。 |
| `QPermission::value<QLocationPermission>() const` | 恢复原始 typed permission | 返回 `std::optional`；恢复的是请求描述，不是实际位置。 |

## 14. 完整示例：精确前台定位请求

```cpp
#include <QCoreApplication>
#include <QPermissions>

class LocationController : public QObject
{
public:
    void ensureLocationPermission()
    {
        QLocationPermission permission;
        permission.setAccuracy(QLocationPermission::Precise);
        permission.setAvailability(QLocationPermission::WhenInUse);

        QCoreApplication *app = QCoreApplication::instance();
        if (!app)
            return;

        switch (app->checkPermission(permission)) {
        case Qt::PermissionStatus::Granted:
            startLocationProvider();
            return;
        case Qt::PermissionStatus::Denied:
            showPermissionDenied();
            return;
        case Qt::PermissionStatus::Undetermined:
            app->requestPermission(permission, this,
                [this](const QPermission &result) {
                    if (result.status() ==
                        Qt::PermissionStatus::Granted) {
                        startLocationProvider();
                    } else {
                        showPermissionDenied();
                    }
                });
            return;
        }
    }

private:
    void startLocationProvider();
    void showPermissionDenied();
};
```

这段流程把四个边界分开：

1. `QLocationPermission` 只描述需要什么；
2. `checkPermission()` 读取当前系统状态；
3. `requestPermission()` 异步询问用户；
4. 位置 provider 在授权成功后独立处理实际定位错误。

## 15. 选型结论

1. `QLocationPermission` 是权限请求描述，不是定位对象。
2. 默认请求是 `Approximate + WhenInUse`，符合最小权限策略。
3. 只有确实需要时才请求 `Precise` 或 `Always`，并同步准备平台声明。
4. `requestPermission()` 只能在主线程调用，结果通过异步回调取得。
5. 回调中的 `QPermission::status()` 才是本次请求的授权结果。
6. `QPermission::value<QLocationPermission>()` 返回原始请求描述，不表示平台兑现了精度或后台能力。
7. `Granted` 只说明权限层通过，不能代替 provider、设备和定位服务错误处理。
8. `Always` 需要前台权限配合，尤其在 Android 上不能只声明后台权限。
9. 权限对象的复制、移动、赋值和析构不会弹窗、授权或撤销权限。
10. 用户拒绝后应解释用途并引导设置或等待下一次主动操作，不要循环重试。
