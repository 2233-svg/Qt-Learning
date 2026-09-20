# QSemaphore
> Qt 6.11.1 · Qt Core · 来自 `QSemaphore`

## 作用定位
`QSemaphore` 是计数型同步原语：`acquire(n)` 消耗资源令牌，`release(n)` 归还令牌。它适合限制并发量和协调生产/消费，不保存数据本身。
## API 速查
| API | 是做什么的 |
|---|---|
| `acquire(n)` | 阻塞直到获得 n 个令牌。 |
| `tryAcquire(n)` | 非阻塞尝试。 |
| `tryAcquire(n, timeout)` | 在超时内尝试。 |
| `release(n)` | 增加 n 个可用令牌。 |
| `available()` | 查询当前近似可用数，不可据此做无锁决策。 |
## 使用场景
```cpp
QSemaphore connections(4); // 最多四个并发连接
connections.acquire();
QSemaphoreReleaser release(&connections);
performRequest();
```
## 常见坑与经验
- `available()` 与下一次 acquire 之间不是原子事务。
- 取得和归还计数必须配平，异常路径用 releaser。
- 不要在 GUI 线程无限期 `acquire()`。
## 知识点覆盖
计数同步、限流、生产者消费者、阻塞、超时、RAII。
