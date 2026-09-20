# QEnableSharedFromThis
> Qt 6.11.1 · Qt Core · 来自 `QEnableSharedFromThis`

## 作用定位
`QEnableSharedFromThis<T>` 让由 `QSharedPointer<T>` 管理的对象能够安全取得指向自己的共享指针，而不是从裸 `this` 再创建一个独立控制块。

## API 速查
| API | 是做什么的 |
|---|---|
| `sharedFromThis()` | 返回共享拥有自身的 `QSharedPointer<T>`。|
| `sharedFromThis() const` | 返回只读共享指针。|

## 使用场景
对象启动异步任务时，需要把自身安全捕获到回调中，确保回调执行前对象不会被提前释放。

## 常见坑与经验
- 对象必须已经由 `QSharedPointer` 管理；在构造函数或栈对象上调用没有有效共享所有权。
- 绝不能对同一个裸指针分别构造多个 `QSharedPointer`，否则会双重删除。
- QObject 父子所有权与 `QSharedPointer` 所有权混用前必须只有一个明确销毁者。

## 知识点覆盖
共享所有权、控制块、异步回调、双重删除、QObject 生命周期。
