# QMultiHash::key_iterator
> Qt 6.11.1 · Qt Core · 来自 `QMultiHash::key_iterator`

## 作用定位
`QMultiHash::key_iterator` 只遍历多值哈希中每条关联的键，因此相同键会重复出现。

## API 速查
| API | 是做什么的 |
|---|---|
| `operator*()` | 读取当前关联的键。|
| `operator++()` | 移到下一条关联。|
| `keyBegin()` / `keyEnd()` | 获取键遍历边界。|

## 使用场景
统计每个键出现次数，或遍历所有关联但只关心所属分类。

## 常见坑与经验
- 它不会自动去重；需要唯一键时用 `uniqueKeys()` 或另建 `QSet`。
- 无序遍历与结构修改导致的失效规则同 `QMultiHash` 主容器。

## 知识点覆盖
多值键、重复键、无序遍历、去重、迭代器生命周期。
