# QContactsPermission
> Qt 6.11.1 · Qt Core · 来自 `QContactsPermission`

## 作用定位
`QContactsPermission` 表示应用访问系统联系人数据所需的运行时权限。

## API 速查
| API | 是做什么的 |
|---|---|
| `checkPermission()` | 查询联系人授权状态。|
| `requestPermission()` | 异步请求系统授权。|

## 使用场景
导入联系人、匹配号码、邀请好友前，由用户操作触发权限申请。

## 常见坑与经验
- 通讯录是高敏感数据；请求前说明用途，最小化读取、存储与上传范围。
- 被拒绝时不要阻断核心流程，提供手动输入等替代方式。

## 知识点覆盖
联系人隐私、运行时授权、最小权限、降级体验、平台配置。
