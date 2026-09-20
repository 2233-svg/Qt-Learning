# QModelRoleDataSpan
> Qt 6.11.1 · Qt Core · 来自 `QModelRoleDataSpan`

## 作用定位
`QModelRoleDataSpan` 是对连续 `QModelRoleData` 内存的非拥有视图，供模型 `multiData()` 在一次调用内填充多个请求 role。

## API 速查
| API | 是做什么的 |
|---|---|
| `begin()` / `end()` | 遍历请求的 role 数据项。|
| `size()` | 查询请求 role 数量。|
| `operator[]` | 按位置访问 role 数据项。|
| `data()` | 获取连续数组首地址。|

## 使用场景
高频 view/delegate 同时请求多个角色时，模型重实现 `multiData()` 统一读取业务记录并填充 span，减少重复查表。

## 常见坑与经验
- span 不拥有底层数组，不能保存到回调返回之后。
- 只应填充 span 中请求的角色；随意写入未请求角色既无收益也可能破坏调用约定。

## 知识点覆盖
span、模型批量 role、非拥有视图、性能优化、生命周期。
