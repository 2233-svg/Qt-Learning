# QUnhandledException
> Qt 6.11.1 · Qt Core · 来自 `QUnhandledException`
## 作用定位
`QUnhandledException` 表示 Qt 并发任务中捕获到但未被业务处理的异常，常由 `QFuture` 相关机制向调用方传播。
## API 速查
| API | 是做什么的 |
|---|---|
| 构造/拷贝 | 保存异常传播状态。 |
| `exception()` | 取得底层 `std::exception_ptr`。 |
| `raise()` | 重新抛出封装的异常。 |
## 使用场景
在等待 future 结果时捕获并记录后台任务未处理异常。
## 常见坑与经验
- 不要让异常跨越未知线程边界裸奔；在任务边界转成结果或错误对象更清晰。
- `raise()` 会重新抛出，调用处必须有异常策略。
## 知识点覆盖
Qt Concurrent、异常传播、`exception_ptr`、后台任务错误处理。
