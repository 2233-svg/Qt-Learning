# QMultiMap::key_iterator
> Qt 6.11.1 · Qt Core · 来自 `QMultiMap::key_iterator`

## 作用定位
`QMultiMap::key_iterator` 以键排序顺序遍历多值映射中的键；同一键对应多条关联时会重复出现。

## API 速查
| API | 是做什么的 |
|---|---|
| `operator*()` | 读取当前关联的键。|
| `operator++()` / `operator--()` | 在有序关系中移动。|
| `keyBegin()` / `keyEnd()` | 获取键遍历边界。|

## 使用场景
按键分组统计前遍历全部关系，或以有序方式检查关联的键分布。

## 常见坑与经验
- 该迭代器不会去重；想获取每个键一次应使用 `uniqueKeys()`。
- 任何结构性修改都会影响迭代器有效性。

## 知识点覆盖
多值键、重复键、有序遍历、去重、迭代器失效。
