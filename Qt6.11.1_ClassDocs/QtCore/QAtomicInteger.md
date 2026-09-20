# QAtomicInteger
> Qt 6.11.1 · Qt Core · 来自 `QAtomicInteger`

## 作用定位
`QAtomicInteger<T>` 为整型提供原子读写、加减、位操作和比较交换，并可选择内存序。

## API 速查
| API | 是做什么的 |
|---|---|
| `loadAcquire()` / `storeRelease()` | 建立生产者消费者同步。|
| `fetchAndAddOrdered()` | 原子加。|
| `fetchAndAndRelaxed()` | 原子位运算。|
| `testAndSetAcquire()` | 比较交换。|
| `isLockFree()` | 查询当前平台是否无锁实现。|

## 使用场景
取消标志、序列号、计数器和低层并发组件。

## 常见坑与经验
- “Relaxed” 只保证该变量原子，不建立其他数据可见性。
- 业务状态机优先 mutex 或消息传递，避免不必要的无锁复杂度。

## 知识点覆盖
内存序、无锁、CAS、原子位运算、并发状态。
