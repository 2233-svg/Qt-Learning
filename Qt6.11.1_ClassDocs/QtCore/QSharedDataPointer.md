# QSharedDataPointer
> Qt 6.11.1 · Qt Core · 来自 `QSharedDataPointer<T>`
## 作用定位
`QSharedDataPointer` 管理 `QSharedData` 派生私有数据，并在非 const 访问时自动 detach，实现可高效复制的值类型。
## API 速查
| API | 是做什么的 |
|---|---|
| 构造/赋值 | 共享或接管数据块。 |
| `operator->` / `operator*` | 非 const 访问会确保独占副本。 |
| `constData()` | 只读访问，不触发 detach。 |
| `data()` | 取得可写数据并在必要时 detach。 |
| `detach()` | 主动取得独占数据。 |
## 使用场景
值类在 setter 内通过 `d->member = value` 自动隔离副本。
## 常见坑与经验
- 保存来自 `constData()` 的裸指针后再写对象，指针可能不再代表当前数据。
- 隐式共享不是并发写安全；同一实例仍需同步。
## 知识点覆盖
COW、detach、值类型、私有实现、指针失效、线程安全。
