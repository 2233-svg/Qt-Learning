# QPermission
> Qt 6.11.1 · Qt Core · 来自 `QPermission`

## 作用定位
`QPermission` 是 Qt 各平台运行时权限类型的共同抽象，配合 `QCoreApplication::checkPermission()` 和 `requestPermission()` 查询或申请系统权限。

## API 速查
| API | 是做什么的 |
|---|---|
| `QPermission::Status` | 表示 Granted、Denied、Undetermined 等授权状态。|
| `checkPermission(permission)` | 查询当前权限结果。|
| `requestPermission(permission, context, callback)` | 异步请求权限并在 context 存活时回调。|

## 使用场景
通用代码以统一流程请求摄像头、麦克风、位置、日历、联系人、蓝牙等不同具体权限类型。

## 常见坑与经验
- `Undetermined` 才意味着可请求；`Denied` 可能表示用户已拒绝或需在系统设置中手动开启。
- 请求成功不保证相关硬件、服务或网络可用，后续操作仍需错误处理。
- 权限只在用户明确触发相关功能时申请，且 callback context 应绑定页面/控制器生命周期。

## 知识点覆盖
运行时权限、异步回调、授权状态、最小权限、context 生命周期、平台差异。
