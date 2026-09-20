# QAbstractEventDispatcher
> Qt 6.11.1 · Qt Core · 来自 `QAbstractEventDispatcher`

## 作用定位
`QAbstractEventDispatcher` 是每个有事件循环线程的底层事件分发器接口，负责处理定时器、socket notifier 和投递事件。

## API 速查
| API | 是做什么的 |
|---|---|
| `instance()` | 取得指定线程的 dispatcher。|
| `processEvents()` | 处理一轮待分发事件。|
| `registerTimer()` / `unregisterTimer()` | 注册或移除底层定时器。|
| `registerSocketNotifier()` | 注册 socket 就绪通知。|
| `wakeUp()` | 唤醒阻塞的事件循环。|
| `aboutToBlock()` / `awake()` | 观察事件循环阻塞和唤醒。|

## 使用场景
嵌入自定义平台循环、诊断事件循环卡顿或实现平台相关 dispatcher。

## 常见坑与经验
- 常规业务不应直接调用 `processEvents()` 作为“防卡顿”手段，它会引入重入问题。
- dispatcher 有线程归属；跨线程取得实例并操作并不安全。

## 知识点覆盖
事件循环、定时器、socket notifier、线程归属、重入、平台集成。
