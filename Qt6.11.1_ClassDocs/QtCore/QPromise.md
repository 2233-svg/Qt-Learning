# QPromise
> Qt 6.11.1 · Qt Core · 来自 `QPromise`

## 作用定位
`QPromise<T>` 是手工生产 `QFuture<T>` 结果的端点。生产者通过它报告开始、进度、一个或多个结果、异常、取消和完成，消费者通过 future 观察。

## API 速查
| API | 是做什么的 |
|---|---|
| `start()` | 标记任务已开始。|
| `addResult()` | 追加一个结果。|
| `setProgressValue()` | 更新进度数值。|
| `setProgressRange()` | 设置进度范围。|
| `setException()` | 向 future 传递异常。|
| `isCanceled()` | 查询消费者是否请求取消。|
| `finish()` | 标记不再产生结果。|
| `future()` | 获取供消费者使用的 `QFuture<T>`。|

## 使用场景
封装回调式 SDK、分阶段解析器或自定义线程任务为 Qt Future API，并向 UI 暴露进度与取消能力。

## 常见坑与经验
- `start()` 与 `finish()` 必须形成完整生命周期；遗漏 `finish()` 会使等待方永久等待。
- 取消是协作式：生产循环应定期检查 `isCanceled()` 并尽快停止。
- 不要在多个线程无协调地同时向同一 promise 写结果；生产者线程模型应明确。
- 将异常传入 promise 后，消费者获取结果时仍需处理重新抛出。

## 知识点覆盖
Promise/Future、生产者消费者、多结果、进度、协作取消、异常传播、线程模型。
