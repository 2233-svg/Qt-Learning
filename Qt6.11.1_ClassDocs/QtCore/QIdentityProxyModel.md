# QIdentityProxyModel
> Qt 6.11.1 · Qt Core · 来自 `QIdentityProxyModel`

## 作用定位
`QIdentityProxyModel` 保持源模型索引、行列与数据的同一映射，是为局部改写角色、表头或 flags 而不改变结构的代理基类。

## API 速查
| API | 是做什么的 |
|---|---|
| `setSourceModel()` | 绑定源模型。|
| `mapToSource()` | 将代理索引原样映射回源索引。|
| `mapFromSource()` | 将源索引映射到代理索引。|
| `data()` | 可重实现以改写某些 role。|
| `headerData()` | 可重实现以改写表头。|
| `flags()` | 可重实现以改变交互能力。|

## 使用场景
给既有模型增加派生显示文本、将某个 role 格式化成用户可读字符串、临时禁用编辑而不重写复杂模型。

## 常见坑与经验
- 它不负责筛选、排序或结构重排；这些需求使用专门的 proxy。
- 若在 `data()` 中访问源模型又触发源模型更新，注意避免递归或循环通知。

## 知识点覆盖
身份代理、角色改写、索引映射、模型装饰、通知循环。
