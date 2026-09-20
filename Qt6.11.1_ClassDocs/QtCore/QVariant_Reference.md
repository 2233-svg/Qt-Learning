# QVariant::Reference
> Qt 6.11.1 · Qt Core · 来自 `QVariant::Reference`
## 作用定位
`QVariant::Reference` 是 `QVariant` 的可写引用代理，让某个存储位置以赋值形式更新变体值。
## API 速查
| API | 是做什么的 |
|---|---|
| 读取转换 | 读出当前值。 |
| `operator=` | 写回新的 QVariant 值。 |
| 代理互操作 | 与 Pointer/ConstReference 等配合。 |
## 使用场景
模型或容器代理中把元素暴露为可写 QVariant 引用。
## 常见坑与经验
- 它不是普通 C++ 引用，背后可能触发转换或 detach。
- 源对象生命周期结束后代理立即失效。
## 知识点覆盖
引用代理、写回、隐式共享、类型擦除。
