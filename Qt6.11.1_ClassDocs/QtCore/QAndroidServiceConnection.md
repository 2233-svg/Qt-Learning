# QAndroidServiceConnection
> Qt 6.11.1 · Qt Core · 来自 `QAndroidServiceConnection`

## 作用定位
`QAndroidServiceConnection` 处理客户端绑定 Android Service 后的连接与断开回调。

## API 速查
| API | 是做什么的 |
|---|---|
| `onServiceConnected()` | 取得已连接 Binder。|
| `onServiceDisconnected()` | 处理服务异常断开。|
| `bindService()` | 发起绑定。|
| `unbindService()` | 解除绑定。|

## 使用场景
界面进程绑定后台 Qt Android service 并调用 Binder 接口。

## 常见坑与经验
- Service 随时可能断开，客户端必须能够重新绑定和恢复状态。

## 知识点覆盖
服务绑定、Binder、断线恢复、Android 生命周期。
