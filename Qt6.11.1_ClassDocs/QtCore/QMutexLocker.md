# QMutexLocker
> Qt 6.11.1 · Qt Core · 来自 `QMutexLocker`

## 作用定位
`QMutexLocker<Mutex>` 是锁的 RAII 包装：构造时锁定 mutex，离开作用域时自动解锁，避免 return、异常或分支遗漏 `unlock()`。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 锁定传入的 mutex。|
| `unlock()` | 临时提前释放锁。|
| `relock()` | 再次锁定。|
| `isLocked()` | 查询当前是否持锁。|
| `mutex()` | 返回关联 mutex。|

## 使用场景
```cpp
QMutexLocker lock(&m_mutex);
updateSharedState();
```
用于所有常规临界区，尤其是函数存在多个 early return 的场景。

## 常见坑与经验
- 提前 `unlock()` 后不要忘记是否需要 `relock()`；最好缩小作用域代替复杂手动控制。
- locker 只保证释放锁，不会使被保护对象自动线程安全。
- 不要把 locker 跨越耗时调用、信号发射或阻塞等待。

## 知识点覆盖
RAII、互斥锁、异常安全、临界区范围、手动解锁、线程安全。
