# QVariant::ConstReference
> Qt 6.11.1 · Qt Core · 来自 `QVariant::ConstReference`
## 作用定位
`QVariant::ConstReference` 是只读引用代理，用于在 QVariant 泛型接口中避免不必要复制，同时保持不可修改语义。
## API 速查
| API | 是做什么的 |
|---|---|
| 读取转换 | 以 `QVariant` 视角读取被引用值。 |
| 比较/传递 | 在代理接口之间传递只读引用。 |
## 使用场景
高级容器或模型辅助代码读取 QVariant 位置而不写回。
## 常见坑与经验
- 它不拥有数据，不能超过源对象生命周期。
- 需要长期保存时拷贝成真正的 `QVariant`。
## 知识点覆盖
引用代理、只读访问、类型擦除、生命周期。
