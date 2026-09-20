# QCalendarPermission
> Qt 6.11.1 · Qt Core · 来自 `QCalendarPermission`

## 作用定位
`QCalendarPermission` 表示移动平台读取或写入用户日历所需的运行时权限。

## API 速查
| API | 是做什么的 |
|---|---|
| `QCoreApplication::checkPermission()` | 查询权限状态。|
| `QCoreApplication::requestPermission()` | 异步请求系统授权。|

## 使用场景
创建日程、同步会议或读取用户日历前，按功能触发权限申请。

## 常见坑与经验
- Android manifest 或 iOS 的用途说明是前置条件。
- 用户拒绝后应提供本地日程或手动输入的替代体验。

## 知识点覆盖
运行时权限、日历隐私、系统授权、降级策略。
