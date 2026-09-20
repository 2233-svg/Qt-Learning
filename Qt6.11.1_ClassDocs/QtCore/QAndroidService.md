# QAndroidService
> Qt 6.11.1 · Qt Core · 来自 `QAndroidService`

## 作用定位
`QAndroidService` 是实现 Android Service 的 Qt 基类，用于无界面后台任务或被绑定服务。

## API 速查
| API | 是做什么的 |
|---|---|
| `onCreate()` / `onDestroy()` | 响应服务创建和销毁。|
| `onStartCommand()` | 处理启动请求。|
| `onBind()` | 返回可绑定接口。|
| `stopSelf()` | 请求停止自身。|

## 使用场景
Android 专用的播放、同步或设备连接后台服务。

## 常见坑与经验
- Android 后台执行限制与前台服务通知要求由系统版本决定，不能把服务当永久后台线程。

## 知识点覆盖
Android Service、后台限制、绑定服务、生命周期、前台服务。
