# QVariantConstPointer
> Qt 6.11.1 · Qt Core · 来自 `QVariantConstPointer`
## 作用定位
`QVariantConstPointer` 是 QVariant 内部/迭代接口使用的只读指针代理，表达“指向 QVariant 内容但不能修改”。
## API 速查
| API | 是做什么的 |
|---|---|
| 解引用访问 | 只读读取目标 QVariant 值。 |
| 比较/移动 | 配合迭代器或引用代理定位。 |
## 使用场景
主要由 Qt API 返回，普通代码很少主动构造。
## 常见坑与经验
- 它不是拥有型指针，不负责延长容器或 QVariant 生命周期。
- 源对象修改后代理可能失效。
## 知识点覆盖
代理指针、只读访问、类型擦除、生命周期。
