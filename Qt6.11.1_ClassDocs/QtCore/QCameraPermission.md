# QCameraPermission
> Qt 6.11.1 · Qt Core · 来自 `QCameraPermission`

## 作用定位
`QCameraPermission` 表示应用访问摄像头的运行时权限。

## API 速查
| API | 是做什么的 |
|---|---|
| `checkPermission()` | 查询当前授权状态。|
| `requestPermission()` | 触发系统授权流程。|

## 使用场景
扫码、拍照和视频预览功能在用户主动启动时申请摄像头权限。

## 常见坑与经验
- 获得权限不代表硬件一定可用；仍需处理设备占用、无摄像头或被系统禁用。

## 知识点覆盖
摄像头、移动隐私、运行时授权、设备状态。
