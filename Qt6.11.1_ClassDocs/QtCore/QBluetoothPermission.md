# QBluetoothPermission
> Qt 6.11.1 · Qt Core · 来自 `QBluetoothPermission`

## 作用定位
`QBluetoothPermission` 描述应用访问蓝牙的运行时权限请求，特别面向移动平台。

## API 速查
| API | 是做什么的 |
|---|---|
| `setCommunicationModes()` | 申请扫描、连接等所需模式。|
| `communicationModes()` | 读取权限范围。|
| `QCoreApplication::requestPermission()` | 异步请求系统授权。|
| `checkPermission()` | 查询当前状态。|

## 使用场景
开始扫描或连接设备前按平台流程请求权限。

## 常见坑与经验
- 不同平台的 manifest/Info.plist 说明仍是前置条件；运行时 API 不能替代配置。
- 拒绝后应保留无蓝牙可用路径，不要循环弹窗。

## 知识点覆盖
运行时权限、移动平台、蓝牙扫描、授权状态、降级体验。
