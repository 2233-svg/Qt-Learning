# QVariantRef
> Qt 6.11.1 · Qt Core · 来自 `QVariantRef`
## 作用定位
`QVariantRef` 是类似引用的代理对象，允许把某个 QVariant 存储位置当作左值赋新值。
## API 速查
| API | 是做什么的 |
|---|---|
| `operator QVariant()` | 读取当前位置值。 |
| `operator=` | 写回新 QVariant。 |
| 指针/引用辅助 | 与 QVariant 迭代代理配合。 |
## 使用场景
遍历可写 QVariant 序列时用赋值语义更新元素。
## 常见坑与经验
- 它是代理，不是独立 QVariant；源容器改变后不要继续使用。
- 赋值可能触发 detach 或类型转换。
## 知识点覆盖
引用代理、写回语义、隐式共享、类型擦除、迭代修改。
