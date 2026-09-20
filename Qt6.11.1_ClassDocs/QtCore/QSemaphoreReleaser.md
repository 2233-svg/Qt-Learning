# QSemaphoreReleaser
> Qt 6.11.1 · Qt Core · 来自 `QSemaphoreReleaser`

## 作用定位
`QSemaphoreReleaser` 用 RAII 归还已取得的信号量资源计数，适合令牌式限流和生产者消费者中的异常安全释放。
## API 速查
| API | 是做什么的 |
|---|---|
| `(semaphore, n)` | 析构时对信号量 `release(n)`。 |
| `cancel()` | 放弃自动归还。 |
| `semaphore()` | 查询关联的信号量。 |
| 移动构造/赋值 | 转移归还责任。 |
## 使用场景
```cpp
slots.acquire();
QSemaphoreReleaser release(&slots);
useOneSlot();
```
## 常见坑与经验
- 必须在已成功 `acquire(n)` 后创建同样计数的 releaser。
- `cancel()` 后需要由别处明确归还，否则永久消耗令牌。
- 它不保护共享数据，只管理可用计数。
## 知识点覆盖
信号量、令牌、限流、RAII、异常安全、资源计数。
