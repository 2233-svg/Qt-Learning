# QSharedPointer
> Qt 6.11.1 · Qt Core · 来自 `QSharedPointer<T>`
## 作用定位
`QSharedPointer` 以引用计数共享对象所有权；最后一个强引用释放时销毁对象。它适合确有共享生命周期的非 QObject 或跨层对象，不应替代清晰的单一所有者。
## API 速查
| API | 是做什么的 |
|---|---|
| `create()` | 原位创建共享对象。 |
| `data()` / `operator->` | 访问对象。 |
| `isNull()` | 判断是否为空。 |
| `reset()` / `clear()` | 放弃当前强引用。 |
| `toWeakRef()` | 创建不延长生命周期的弱引用。 |
| `dynamicCast/staticCast` | 在共享控制块下进行指针转换。 |
## 使用场景
多个异步消费者都需要一个结果对象，且最后一个消费者结束时才销毁。
## 常见坑与经验
- 循环强引用永远不会释放，用 `QWeakPointer` 断环。
- 不要同时以 `QObject` parent 和 shared pointer 管理同一个对象。
- 从同一裸指针创建两份 shared pointer 会双重删除。
## 知识点覆盖
引用计数、共享所有权、弱引用、循环引用、QObject 所有权冲突、异步生命周期。
