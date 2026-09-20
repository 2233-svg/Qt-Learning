# QVariant::ConstPointer
> Qt 6.11.1 · Qt Core · 来自 `QVariant::ConstPointer`
## 作用定位
`QVariant::ConstPointer` 是 `QVariant` 命名空间下的只读指针代理类型，用于泛型接口统一表达 QVariant 内容访问。
## API 速查
| API | 是做什么的 |
|---|---|
| 解引用 | 只读取得目标值。 |
| 比较 | 判断代理是否指向同一位置。 |
## 使用场景
通常出现在 Qt 内部或高级泛型代码中，普通应用只需知道它不拥有数据。
## 常见坑与经验
- 不要保存超过源 QVariant/容器生命周期。
- 要修改值应使用对应可写代理或直接操作 QVariant。
## 知识点覆盖
只读代理、QVariant、生命周期、泛型接口。
