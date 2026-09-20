# Qt QCalendarPermission 深入笔记

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.5  
> 头文件：`#include <QPermissions>`  
> 所属模块：`Qt6::Core`  
> 核心定位：描述应用请求“读取”或“读取并写入”系统日历数据的权限范围

## 1. 它解决什么问题

日历数据通常属于操作系统保护的个人信息。应用不能因为链接了日历库就自动读取用户的日程，也不能在没有额外授权的情况下写入系统日历。

`QCalendarPermission` 不是权限状态，也不会自己弹出系统对话框。它是一个**请求描述对象**，用来告诉 Qt：

- 要请求哪一类资源：日历。
- 要请求到什么范围：只读，还是读写。

真正的工作流由 `QCoreApplication` 完成：

```text
QCalendarPermission
        |
        | checkPermission()
        v
Granted / Denied / Undetermined
        |
        | requestPermission() only when Undetermined
        v
system permission dialog and asynchronous callback
```

这能避免两个常见问题：不需要授权时反复弹窗，以及用户拒绝后仍然假设日历 API 会可用。

## 2. 读权限与写权限不是一回事

默认构造的 `QCalendarPermission` 请求只读访问。只有确实要创建、修改或删除系统日历条目时，才调用 `setAccessMode(ReadWrite)` 请求更大的范围。

| 访问模式 | 意味着什么 | 适用场景 | 请求原则 |
| --- | --- | --- | --- |
| `ReadOnly` | 读取日历数据，默认值。 | 展示空闲时间、导入日程、仅做冲突检查。 | 能完成需求时优先使用。 |
| `ReadWrite` | 读取并修改日历数据。 | 创建会议、同步待办到系统日历、修改应用创建的事件。 | 仅在用户触发写入功能前请求。 |

权限范围应与当前动作相匹配。一个只展示可用时段的页面没有必要在启动时请求读写权限；延迟到用户进入日历功能或点击“同步”后再请求，既更清楚也更符合最小权限原则。

## 3. 最小可用流程

下面的例子把状态检查、异步请求和回调处理放在一个 `QObject` 中。带 `context` 的重载会在 `context` 销毁后自动放弃回调，避免回调访问已释放的界面或控制器。

```cpp
#include <QCoreApplication>
#include <QPermission>
#include <QPermissions>

class CalendarAccessController : public QObject
{
public:
    void ensureReadAccess()
    {
        QCalendarPermission request; // 默认 ReadOnly
        auto *app = QCoreApplication::instance();
        const auto status = app->checkPermission(request);

        if (status == Qt::PermissionStatus::Granted) {
            loadCalendarEvents();
            return;
        }

        if (status == Qt::PermissionStatus::Denied) {
            showCalendarUnavailable();
            return;
        }

        app->requestPermission(request, this,
            [this](const QPermission &result) {
                if (result.status() == Qt::PermissionStatus::Granted) {
                    loadCalendarEvents();
                } else {
                    showCalendarUnavailable();
                }
            });
    }

private:
    void loadCalendarEvents();
    void showCalendarUnavailable();
};
```

`requestPermission()` 是异步的：不要在调用后紧接着访问日历并假设已授权。只有回调收到 `Granted` 后，才开始读取或写入。

权限请求只能从主线程发起。若业务逻辑在工作线程中发现需要权限，应通过信号槽或 `QMetaObject::invokeMethod()` 回到主线程请求，再把结果传回业务流程。

## 4. 写入日历时的请求方式

```cpp
QCalendarPermission request;
request.setAccessMode(QCalendarPermission::ReadWrite);

const auto status = QCoreApplication::instance()->checkPermission(request);
if (status == Qt::PermissionStatus::Undetermined) {
    QCoreApplication::instance()->requestPermission(
        request, this, [this](const QPermission &result) {
            if (result.status() == Qt::PermissionStatus::Granted) {
                createCalendarEvent();
            }
        });
}
```

更高权限不等于“自动拥有之前的只读授权”。每次进入需要写入的功能，都应按当前的 `ReadWrite` 请求对象检查状态。平台会根据自身授权模型决定是否需要再次提示、是否能升级、或是否直接拒绝。

## 5. 平台声明是运行时请求的前置条件

调用 C++ API 只是运行时步骤。要让系统允许应用请求权限，还要在打包配置中声明用途和系统权限：

| 平台 | 需要的构建期声明 | 与访问模式的关系 | 说明 |
| --- | --- | --- | --- |
| Apple 平台 | `NSCalendarsUsageDescription` 用途说明。 | 无论请求哪种日历访问都需要。 | 向用户说明为什么应用需要日历数据。 |
| Android | `android.permission.READ_CALENDAR`。 | 只读与读写都需要读取声明。 | 声明写在 Android manifest。 |
| Android | `android.permission.WRITE_CALENDAR`。 | `ReadWrite` 时额外需要。 | 仅有 C++ 中的 `ReadWrite` 设置不足以获得写入能力。 |

未完成这些声明时，运行时请求可能被系统拒绝、无法显示预期对话框，或应用在平台审核与打包阶段出现问题。权限属于产品与打包配置的一部分，不只是一个 C++ 分支。

## 6. `QCalendarPermission`、`QPermission` 与状态的关系

`QCalendarPermission` 是具体类型，携带“日历 + 访问模式”。传给 `checkPermission()` 或 `requestPermission()` 时，它会作为 `QPermission` 被 Qt 统一处理。

回调参数是 `const QPermission &`，使用 `status()` 读取最终结果：

| 状态 | 表示什么 | 下一步 | 是否可访问日历 |
| --- | --- | --- | --- |
| `Qt::PermissionStatus::Granted` | 已获授权，或者该平台不要求用户授权。 | 执行需要日历访问的动作。 | 可以开始访问，但仍处理具体 API 的运行时错误。 |
| `Qt::PermissionStatus::Denied` | 用户拒绝，或平台不支持或不允许此权限。 | 停止访问，展示可理解的降级界面或设置入口。 | 不可访问。 |
| `Qt::PermissionStatus::Undetermined` | 还未得到用户决定。 | 从主线程调用 `requestPermission()`。 | 尚不可假定可以访问。 |

`requestPermission()` 的最终回调不会再得到 `Undetermined`；它只会完成为允许或拒绝。不要把 `Denied` 当成一次性异常后无限重试，尤其要避免用户明确拒绝后立即再次发起请求。

## 7. 值语义和生命周期

`QCalendarPermission` 是可复制、可移动的轻量值类型，内部使用共享数据。它没有 `QObject` 父子关系，也不持有“已经授权”的全局状态；创建多个对象不会产生多个授权。

可以在请求前临时创建它，也可以将它作为配置字段保存。真正决定结果的是系统权限状态及当前请求的访问模式。回调里应以传入的 `QPermission` 状态为准，而不是假设先前某个对象记录的状态仍可靠。

## 8. 常见误区

### 8.1 创建对象就以为已经拿到权限

```cpp
QCalendarPermission permission;
readCalendar(); // 错误：还没有检查或请求系统授权
```

必须先调用 `checkPermission()`，并在 `Undetermined` 时调用 `requestPermission()`。

### 8.2 默认只读请求却尝试写入

默认访问模式是 `ReadOnly`。写入前显式设为 `ReadWrite`，同时确认 Android manifest 中包含写日历权限。

### 8.3 从工作线程弹权限框

权限请求只能从主线程进行。工作线程应通知 UI 或应用主线程协调请求，不要直接调用 `requestPermission()`。

### 8.4 不传回调上下文

无 context 的回调若捕获页面对象，页面先销毁时容易造成悬空访问。界面代码优先使用带 `QObject *context` 的重载。

## API 速查表
### 构造、复制与交换

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QCalendarPermission()` | 创建日历权限请求，默认访问模式为 `ReadOnly`。 | 创建对象不检查也不请求系统权限。 |
| 复制 | `QCalendarPermission(const QCalendarPermission &other) noexcept` | 复制请求描述及其访问模式。 | 复制不会复制系统授权状态，也不会触发新请求。 |
| 移动 | `QCalendarPermission(QCalendarPermission &&other) noexcept` | 转移请求对象的内部数据。 | 普通临时请求通常不必显式使用移动。 |
| 析构 | `~QCalendarPermission()` | 释放请求对象自己的共享数据引用。 | 不会撤销已授予的系统权限。 |
| 赋值 | `QCalendarPermission &operator=(const QCalendarPermission &other) noexcept` | 用另一个请求对象覆盖当前访问模式。 | 覆盖的是请求描述，不是操作系统权限。 |
| 赋值 | `QCalendarPermission &operator=(QCalendarPermission &&other) noexcept` | 通过移动替换当前请求对象。 | 移动后源对象只应销毁或重新赋值。 |
| 交换 | `void swap(QCalendarPermission &other) noexcept` | 交换两个请求对象的内部状态。 | 主要供泛型代码或高效交换使用。 |

### 访问模式

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `QCalendarPermission::ReadOnly` | 表示只读取日历数据，也是默认模式。 | 仅展示或导入数据时选它，避免请求多余权限。 |
| 枚举 | `QCalendarPermission::ReadWrite` | 表示读取并写入日历数据。 | 需要写入功能时才设置；Android 还需声明 `WRITE_CALENDAR`。 |
| 查询 | `AccessMode accessMode() const` | 返回当前请求对象的访问模式。 | 只描述将要检查或请求的范围，不代表已授权。 |
| 设置 | `void setAccessMode(AccessMode mode)` | 将请求范围设为只读或读写。 | 在 `checkPermission()` 和 `requestPermission()` 前设置；修改后应重新检查。 |

### 与权限框架协作

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 状态检查 | `QCoreApplication::checkPermission(const QPermission &permission)` | 查询当前应用对该具体请求的授权状态。 | `Undetermined` 时再发起请求；检查不会显示系统对话框。 |
| 异步请求 | `QCoreApplication::requestPermission(permission, context, functor)` | 发起系统权限请求，并在完成后调用回调。 | Qt 6.5 起提供；只能在主线程调用，优先传 `context` 防止悬空回调。 |
| 结果读取 | `QPermission::status() const` | 从回调的通用权限对象读取最终状态。 | 最终结果不会是 `Undetermined`。 |

---

### 一句话总结

`QCalendarPermission` 只定义“想以什么范围访问日历”；先检查状态，未决定时在主线程异步请求，收到 `Granted` 后才访问数据，并把平台声明与读写范围一并配置好。
