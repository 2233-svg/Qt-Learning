# QObjectCleanupHandler
> Qt 6.11.1 · Qt Core · 来自 `QObjectCleanupHandler`

## 作用定位
`QObjectCleanupHandler` 集中跟踪一组 QObject，并在 handler 析构或显式清理时删除仍被跟踪的对象；对象自行销毁时会自动从集合移除。

## API 速查
| API | 是做什么的 |
|---|---|
| `add()` | 加入一个需管理的 QObject。|
| `remove()` | 停止跟踪指定对象，不删除它。|
| `isEmpty()` | 判断是否还管理对象。|
| `clear()` | 删除并清空全部仍被管理对象。|

## 使用场景
插件加载、临时创建的后台 helper 或测试夹具需要在某个控制对象结束时统一释放，但对象可能也会提前自毁。

## 常见坑与经验
- 加入 handler 后仍必须明确是否同时有 QObject parent；多个删除责任来源会制造双重释放风险。
- `clear()` 会直接删除对象，不能在其信号回调栈中随意调用。
- 新设计中，清晰的 parent 树或智能指针往往更直观；该类适合动态集合清理。

## 知识点覆盖
QObject 生命周期、集中清理、所有权、提前销毁、插件、测试资源。
