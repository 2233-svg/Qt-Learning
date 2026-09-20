# QMetaAssociation::Iterable
> Qt 6.11.1 · Qt Core · 来自 `QMetaAssociation::Iterable`

## 作用定位
`QMetaAssociation::Iterable` 是关联容器运行时遍历范围，封装容器实例与 `QMetaAssociation` 描述，使通用代码能取得键值迭代器。

## API 速查
| API | 是做什么的 |
|---|---|
| `begin()` / `end()` | 获取可写键值迭代范围。|
| `constBegin()` / `constEnd()` | 获取只读遍历范围。|
| `metaAssociation()` | 查询容器元描述。|
| `container()` | 访问被包装容器的运行时地址。|

## 使用场景
通用对象检查器拿到 QVariant 中的 map 后，遍历未知键和值以生成表单或 JSON。

## 常见坑与经验
- range 只在被包装容器仍有效时可用；不能把 iterable 脱离 QVariant/对象生命周期保存。
- 修改容器时遵守底层关联容器的迭代器失效规则。

## 知识点覆盖
运行时迭代、关联容器、元类型、生命周期、类型擦除。
