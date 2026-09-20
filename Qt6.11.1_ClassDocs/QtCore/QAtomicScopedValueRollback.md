# QAtomicScopedValueRollback
> Qt 6.11.1 · Qt Core · 来自 `QAtomicScopedValueRollback`

## 作用定位
`QAtomicScopedValueRollback` 在作用域结束时把原子值恢复为构造时或指定值，适合短暂地设置并发标志。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 保存当前值并可立即设置新值。|
| `commit()` | 将当前值设为最终恢复值。|

## 使用场景
临时设置“正在更新”标志，确保异常或提前 return 后恢复。

## 常见坑与经验
- 它不是互斥锁；其他线程仍可改变该值，恢复动作可能覆盖其更新。

## 知识点覆盖
RAII、作用域恢复、原子标志、并发竞态、异常安全。
