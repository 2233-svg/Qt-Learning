# QSharedData
> Qt 6.11.1 · Qt Core · 来自 `QSharedData`
## 作用定位
`QSharedData` 是隐式共享私有数据的引用计数基类，通常和 `QSharedDataPointer` 实现按值 API、写时复制内部状态。
## API 速查
| API | 是做什么的 |
|---|---|
| 默认构造 | 创建引用计数数据块。 |
| 拷贝构造 | 为 detach 后的副本构造基础部分。 |
| 虚析构 | 允许通过基类安全销毁。 |
## 使用场景
把私有实现类 `Data : QSharedData`，将大型可复制值对象的存储放在 Data 中。
## 常见坑与经验
- `QSharedData` 不会自动深拷贝你的成员；detach 后的复制构造要确保成员具有正确语义。
- 非 const 写入前必须经 `QSharedDataPointer` 触发 detach。
## 知识点覆盖
隐式共享、引用计数、写时复制、pimpl、值语义。
