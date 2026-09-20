# QSystemSemaphore
> Qt 6.11.1 · Qt Core · 来自 `QSystemSemaphore`

## 作用定位
`QSystemSemaphore` 是跨进程计数信号量，用共享名称协调多个进程对外部资源或共享内存的访问。
## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 以 key、初始值和访问模式打开/创建信号量。 |
| `acquire()` | 跨进程消耗一个令牌，可能阻塞。 |
| `release(n)` | 归还 n 个令牌。 |
| `setKey()` | 切换系统信号量 key。 |
| `error()` / `errorString()` | 诊断平台同步错误。 |
## 使用场景
配合 `QSharedMemory`，读写共享段前先 acquire，完成后 release。
## 常见坑与经验
- 崩溃进程可能留下系统资源或计数异常，启动时要有恢复策略。
- key 是全系统命名空间，命名要包含组织和应用标识。
- GUI 线程不要无限等待跨进程信号量。
## 知识点覆盖
跨进程同步、命名资源、共享内存保护、崩溃恢复、阻塞。
