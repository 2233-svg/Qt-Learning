# QFutureSynchronizer
> Qt 6.11.1 · Qt Core · 来自 `QFutureSynchronizer`

## 作用定位
`QFutureSynchronizer<T>` 聚合多个 `QFuture<T>`，并在析构或显式等待时统一等待它们结束；可选地在析构前请求取消。

## API 速查
| API | 是做什么的 |
|---|---|
| `addFuture()` | 加入一个待同步任务。|
| `setFuture()` | 替换为单个 future。|
| `futures()` | 查询当前 future 列表。|
| `waitForFinished()` | 阻塞直到全部任务结束。|
| `setCancelOnWait()` | 等待前先请求取消所有任务。|
| `clearFutures()` | 清空聚合集合。|

## 使用场景
后台对象析构前确保其派生的多个任务不再访问该对象；命令行工具在退出前汇合一批独立计算。

## 常见坑与经验
- 析构等待在 GUI 线程会卡界面；UI 任务应使用 watcher/continuation 组织完成状态。
- `setCancelOnWait(true)` 仅请求协作取消，任务仍必须正确响应并结束。

## 知识点覆盖
任务汇合、RAII、析构等待、取消、线程阻塞、异步生命周期。
