# QWeakPointer
> Qt 6.11.1 · Qt Core · 来自 `QWeakPointer<T>`
## 作用定位
`QWeakPointer` 是不延长对象生命周期的弱引用，与 `QSharedPointer` 配合打破循环引用或观察对象是否仍存在。
## API 速查
| API | 是做什么的 |
|---|---|
| `toStrongRef()` | 尝试提升为 `QSharedPointer`。 |
| `isNull()` | 判断是否没有可观察对象。 |
| `clear()` | 清空弱引用。 |
| 比较 | 判断是否引用同一控制块。 |
## 使用场景
异步回调保存弱引用，执行时先提升，失败说明对象已销毁。
## 常见坑与经验
- 使用对象前必须提升为强引用，不能直接解引用弱指针。
- 对 QObject 观察可考虑 `QPointer`，语义更贴近 parent/delete。
- 弱引用不能解决没有 shared 控制块的裸指针生命周期。
## 知识点覆盖
弱引用、共享所有权、循环引用、异步回调、QObject 观察。
