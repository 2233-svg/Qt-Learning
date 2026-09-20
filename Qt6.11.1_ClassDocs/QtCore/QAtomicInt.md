# QAtomicInt
> Qt 6.11.1 · Qt Core · 来自 `QAtomicInt`

## 作用定位
`QAtomicInt` 是历史兼容的原子整型封装，提供线程间无数据竞争的基本读改写操作。

## API 速查
| API | 是做什么的 |
|---|---|
| `loadRelaxed()` | 无同步语义地读取。|
| `storeRelease()` | 以 release 语义写入。|
| `fetchAndAddRelaxed()` | 原子加并返回旧值。|
| `testAndSetOrdered()` | 比较并交换，带顺序语义。|
| `ref()` / `deref()` | 原子增减，常用于引用计数。|

## 使用场景
兼容旧 Qt 代码的轻量标志或引用计数；新代码通常优先 `QAtomicInteger<T>` 或标准原子类型。

## 常见坑与经验
- 原子性不等于整个算法正确；多个变量存在不变量时仍需锁或更完整的同步设计。

## 知识点覆盖
原子操作、内存序、CAS、引用计数、并发算法边界。
