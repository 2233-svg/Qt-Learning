# QContactsPermission 深入笔记

> 适用版本：Qt 6.5 及以上，本文按 Qt 6.11.1 说明  
> 头文件：`#include <QPermissions>`  
> 所属模块：`Qt6::Core`  
> 类型性质：可拷贝、可移动的权限描述值对象，不是 `QObject`

## 它解决什么问题

`QContactsPermission` 用来描述应用希望访问用户通讯录的权限范围。它不读取联系人，也不弹出系统授权框；它只表达本次请求是只读还是读写，然后交给 `QCoreApplication` 查询或请求。

```cpp
QContactsPermission permission;
permission.setAccessMode(QContactsPermission::ReadOnly);

const auto status =
    QCoreApplication::instance()->checkPermission(permission);
```

分工要分清：

- `QContactsPermission`：描述“我需要读取，还是读取并写入联系人”。
- `QCoreApplication::checkPermission()`：查询当前系统授权状态，不显示对话框。
- `QCoreApplication::requestPermission()`：异步请求系统授权，可能显示系统界面。
- 具体联系人 API 或业务后端：在状态为 `Granted` 后才真正读取或修改通讯录。

因此它不是通讯录管理器，也不会绕过操作系统授权。

## AccessMode：只申请真正需要的范围

默认构造的 `QContactsPermission` 请求 `ReadOnly`。只有应用确实要创建、修改或删除联系人时，才设为 `ReadWrite`。

```cpp
QContactsPermission readPermission; // 默认 ReadOnly

QContactsPermission writePermission;
writePermission.setAccessMode(QContactsPermission::ReadWrite);
```

最小权限原则在这里不只是文案问题。用户点击“从通讯录选择联系人”通常只需要读取；只有“保存到通讯录”这类明确操作才需要读写权限。把两类动作拆开请求，既符合用户预期，也能避免把一个轻量功能变成高敏感授权。

## 完整流程：检查、请求、再继续业务

权限请求应由最接近用户动作的界面或业务入口发起，而不是库初始化时自动发起。下面的写法在申请前后复用同一个函数，授权通过后自然重新进入业务流程。

```cpp
#include <QCoreApplication>
#include <QPermissions>

void ContactImportController::importFromContacts()
{
    QContactsPermission permission;
    permission.setAccessMode(QContactsPermission::ReadOnly);

    QCoreApplication *app = QCoreApplication::instance();
    switch (app->checkPermission(permission)) {
    case Qt::PermissionStatus::Undetermined:
        app->requestPermission(
            permission,
            this,
            [this](const QPermission &result) {
                if (result.status() == Qt::PermissionStatus::Granted)
                    importFromContacts();
                else
                    showContactsPermissionHelp();
            });
        return;

    case Qt::PermissionStatus::Granted:
        beginContactImport();
        return;

    case Qt::PermissionStatus::Denied:
        showContactsPermissionHelp();
        return;
    }
}
```

`requestPermission()` 只能从主线程调用。带 `context` 的重载尤其适合 `QObject` 成员：请求完成时，回调在 `context` 所在线程执行；若 `context` 已销毁，回调不会执行，避免 lambda 捕获 `this` 后悬空。

请求回调的结果只会是 `Granted` 或 `Denied`，不会是 `Undetermined`。`Granted` 表示用户已同意，或当前平台不需要用户授权；`Denied` 也可能表示该权限在当前平台不可用，而不一定只是用户点了拒绝。

## Android 的首次状态要特别看待

Android 的底层 API 没有与 Qt 完全对应的 `Undetermined` 状态。Qt 因而会在应用首次请求前，把被拒绝的检查结果默认报告为 `Undetermined`；在真正调用过 `requestPermission()` 后，后续 `checkPermission()` 才能报告非 `Undetermined` 的最终状态。

所以不要把 Android 上第一次的 `Undetermined` 理解成“用户从未拒绝”。它在 Qt 的语义里表示：应通过一次正式请求来取得用户意图。

## 构建期声明和运行期请求缺一不可

`requestPermission()` 不是平台项目配置的替代品。缺少用途声明或 manifest 权限时，系统无法按预期向用户授权。

### Apple 平台

在 `Info.plist` 中提供通讯录用途说明：

```xml
<key>NSContactsUsageDescription</key>
<string>用于让你从通讯录中选择需要导入的联系人。</string>
```

这段文字会展示给用户，应准确说明实际用途，而不是写笼统的“需要权限”。

### Android

在 `AndroidManifest.xml` 中声明读取通讯录权限：

```xml
<uses-permission android:name="android.permission.READ_CONTACTS" />
```

若 `accessMode()` 为 `ReadWrite`，还需要写入权限：

```xml
<uses-permission android:name="android.permission.WRITE_CONTACTS" />
```

项目使用自定义 Android 清单时，也要保留 Qt 所需的权限插入配置。运行期请求和构建期声明缺少任意一层，都会让权限流程失去意义。

## 值语义、生命周期与 QPermission

`QContactsPermission` 是普通值对象，可以栈上创建、复制、移动、赋值和交换；没有 parent，也不持有一次进行中的系统授权请求。销毁这个对象不会撤销用户已授予的权限，更不会取消系统弹窗。

传入 `checkPermission()` 或 `requestPermission()` 时，Qt 会把强类型权限对象包装成 `QPermission`。异步回调拿到的也是 `const QPermission &`：

```cpp
app->requestPermission(QContactsPermission{}, this,
    [](const QPermission &result) {
        if (result.status() != Qt::PermissionStatus::Granted)
            return;

        const auto requested =
            result.value<QContactsPermission>();
        if (!requested)
            return;

        if (requested->accessMode() ==
            QContactsPermission::ReadWrite) {
            // 回调需要区分原始的读写范围时再检查它。
        }
    });
```

多数单一权限请求只需看 `result.status()`。`value<QContactsPermission>()` 适合一个共用回调要处理多种权限，或要根据原始的 `AccessMode` 路由后续逻辑时使用；类型不匹配会得到 `std::nullopt`。

## 常见错误

- 把 `QContactsPermission` 当成能读取联系人数据的对象。它只描述请求范围。
- 在应用启动时立刻弹授权框。应等待用户点击导入、选择或保存联系人等明确动作。
- 总是申请 `ReadWrite`。只读导入无需写权限。
- 只调用 `requestPermission()`，却没写 `Info.plist` 或 `AndroidManifest.xml`。
- 忽略 `Denied`。拒绝是正常状态，应该提供降级体验或指引用户去系统设置处理。
- 在工作线程请求权限。权限请求只能从主线程发起；后台线程应把需要授权的动作交回主线程。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QContactsPermission()` | 创建一个默认只读的通讯录权限描述。 | 不会检查或请求系统权限；默认 `accessMode()` 是 `ReadOnly`。 |
| 构造 | `QContactsPermission(const QContactsPermission &)` | 拷贝另一个权限描述对象。 | 是值语义，适合按值保存或传给权限 API。 |
| 构造 | `QContactsPermission(QContactsPermission &&)` | 移动构造并接管另一个对象的本地配置。 | 被移动对象只应再析构、赋值或重新配置。 |
| 析构 | `~QContactsPermission()` | 销毁权限描述对象。 | 不会撤销系统授权，也不会取消已经发出的请求。 |
| 赋值 | `operator=(const QContactsPermission &)` | 用另一个权限配置覆盖当前对象。 | 只修改本地值，不触发新的系统授权。 |
| 赋值 | `operator=(QContactsPermission &&)` | 移动赋值当前对象。 | 不要继续依赖被移动对象原有的访问模式。 |
| 交换 | `swap(QContactsPermission &) noexcept` | 交换两个权限对象的本地配置。 | 不涉及系统调用或授权状态。 |
| 枚举 | `AccessMode` | 表示请求通讯录访问的范围。 | 它描述请求意图，不代表当前权限已获准。 |
| 枚举值 | `ReadOnly` | 申请读取联系人数据的权限。 | 默认值；用于选择、导入或展示联系人。 |
| 枚举值 | `ReadWrite` | 申请读取并写入联系人数据的权限。 | 仅在创建或修改联系人时使用；Android 需额外声明 `WRITE_CONTACTS`。 |
| 查询 | `accessMode() const` | 返回当前配置的只读或读写范围。 | 返回的是请求配置，不是 `Granted` 或 `Denied` 状态。 |
| 配置 | `setAccessMode(AccessMode)` | 设置本次权限描述请求的访问范围。 | 在 `checkPermission()` 或 `requestPermission()` 前完成配置。 |

## 相关但不属于本类的关键 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 权限查询 | `QCoreApplication::checkPermission(permission)` | 查询当前授权状态。 | 不会弹系统对话框；`Undetermined` 时再考虑发起请求。 |
| 权限请求 | `QCoreApplication::requestPermission(permission, functor)` | 异步请求系统权限，完成后调用回调。 | 只能在主线程调用；回调参数是 `const QPermission &`。 |
| 权限请求 | `QCoreApplication::requestPermission(permission, context, functor)` | 带对象上下文地异步请求权限。 | `context` 销毁后不调用回调，且回调在它所属线程执行。 |
| 结果状态 | `Qt::PermissionStatus::Undetermined` | 系统授权状态尚未确定。 | Android 首次检查有特殊语义；通过 `requestPermission()` 获取正式结果。 |
| 结果状态 | `Qt::PermissionStatus::Granted` | 用户已同意，或平台不需用户授权。 | 之后仍要处理实际联系人操作的失败。 |
| 结果状态 | `Qt::PermissionStatus::Denied` | 用户拒绝，或当前平台不支持或不允许该权限。 | 提供明确降级路径，不要继续访问通讯录。 |
| 结果包装 | `QPermission::status()` | 读取异步权限请求的最终状态。 | 回调中优先检查是否为 `Granted`。 |
| 结果包装 | `QPermission::value<QContactsPermission>()` | 尝试取回回调内原始的强类型权限描述。 | 类型不匹配得到 `std::nullopt`；单一请求通常不需要读取。 |

## 一句话记忆

`QContactsPermission` 只表达通讯录访问范围：默认只读，确需修改联系人时才设为读写；由主线程在用户动作触发后通过 `QCoreApplication` 检查和异步请求，并同时完成 Apple、Android 的构建期声明。
