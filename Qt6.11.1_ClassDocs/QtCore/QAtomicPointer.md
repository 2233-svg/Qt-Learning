# QAtomicPointer
> Qt 6.11.1 · Qt Core · 来自 `QAtomicPointer`

## 作用定位
`QAtomicPointer<T>` 为指针值提供原子加载、替换和比较交换。

## API 速查
| API | 是做什么的 |
|---|---|
| `loadAcquire()` | 以 acquire 语义读取指针。|
| `storeRelease()` | 以 release 语义发布指针。|
| `testAndSetOrdered()` | 原子比较并替换。|
| `fetchAndStoreRelaxed()` | 原子交换并取旧指针。|

## 使用场景
不可变配置快照发布、低层延迟初始化。

## 常见坑与经验
- 原子指针不管理指向对象的生命周期；ABA、释放竞争和内存回收仍是难题。
- 不要把它当作 QObject 跨线程访问的许可。

## 知识点覆盖
原子指针、对象生命周期、ABA、发布订阅、内存回收。
