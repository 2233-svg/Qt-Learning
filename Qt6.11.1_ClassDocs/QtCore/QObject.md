# QObject
> Qt 6.11.1 · Qt Core · 来自 `QObject`

## 作用定位
`QObject` 是 Qt 对象模型的根：它提供父子所有权、信号槽、动态属性、事件过滤、线程亲和性、对象名和元对象反射。绝大多数 Qt 框架对象都继承它。

## API 速查
| API | 是做什么的 |
|---|---|
| `setParent()` / `children()` | 建立和查询 QObject 所有权树。|
| `deleteLater()` | 在对象所属线程事件循环中延后销毁。|
| `connect()` / `disconnect()` | 建立或断开信号槽连接。|
| `moveToThread()` | 改变对象线程亲和性。|
| `thread()` | 查询对象所属线程。|
| `setProperty()` / `property()` | 读写动态属性。|
| `installEventFilter()` | 让另一 QObject 先观察事件。|
| `findChild()` / `findChildren()` | 按类型和对象名查询后代。|
| `objectName()` / `setObjectName()` | 设置用于调试、测试和查找的名称。|
| `destroyed()` | 对象销毁前通知。|

## 使用场景
构建有生命周期的服务对象、连接异步事件、将后台 worker 移至线程并通过 queued signal 回传数据，或给 UI/测试对象附加对象名。

## 常见坑与经验
- QObject 不可复制；所有权应在 parent、栈对象、智能指针中选择一种清晰模型，避免双重销毁。
- `moveToThread()` 只能在对象没有 parent 时调用，且成员 QObject 不会自动跨线程变成安全对象。
- 直接成员函数调用仍在调用方线程执行；跨线程通信应使用 queued connection。
- `deleteLater()` 依赖所属线程事件循环，线程即将退出时要安排销毁顺序。
- parent 树与 Qt Quick 的视觉 `parentItem` 树不是同一概念。

## 知识点覆盖
QObject、父子所有权、信号槽、事件过滤、线程亲和性、动态属性、元对象、延迟销毁。
