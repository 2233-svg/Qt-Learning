# QExplicitlySharedDataPointer
> Qt 6.11.1 · Qt Core · 来自 `QExplicitlySharedDataPointer`

## 作用定位
`QExplicitlySharedDataPointer<T>` 管理继承 `QSharedData` 的共享私有数据，但不会在非 const 访问时自动 detach；调用者显式决定何时复制。

## API 速查
| API | 是做什么的 |
|---|---|
| `data()` | 取得数据指针。|
| `constData()` | 取得只读数据指针。|
| `detach()` | 显式确保独占数据副本。|
| `reset()` | 改为管理新数据或空指针。|
| `operator->()` | 访问共享数据成员。|

## 使用场景
实现值语义的大对象，并把复制开销延迟到真正修改时；需要精确控制 detach 时机的高性能类型。

## 常见坑与经验
- 非 const `operator->()` 不自动 detach，写入前忘记 `detach()` 会修改其他副本共享的数据。
- 它管理的是 `QSharedData` 引用计数，不是任意 QObject 的共享所有权；不要与 `QSharedPointer` 混为一谈。

## 知识点覆盖
隐式共享、显式 detach、值语义、copy-on-write、引用计数、所有权模型。
