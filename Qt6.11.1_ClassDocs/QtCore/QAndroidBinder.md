# QAndroidBinder
> Qt 6.11.1 · Qt Core · 来自 `QAndroidBinder`

## 作用定位
`QAndroidBinder` 封装 Android Binder IPC 对象，供 Qt Android 服务实现跨进程调用。

## API 速查
| API | 是做什么的 |
|---|---|
| `onTransact()` | 重实现以处理远端事务。|
| `transact()` | 发起 Binder 事务。|
| `queryLocalInterface()` | 查询本地接口实现。|
| `isBinderAlive()` | 判断 binder 是否仍有效。|

## 使用场景
Android 专用后台服务和客户端之间的高性能本地 IPC。

## 常见坑与经验
- Binder 输入必须不可信，需验证 transaction code、长度与权限。
- 平台专属接口应封装在 Android 层，避免污染跨平台业务模型。

## 知识点覆盖
Android Binder、IPC、权限、序列化、服务生命周期。
