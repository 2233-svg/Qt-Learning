# QMetaAssociation
> Qt 6.11.1 · Qt Core · 来自 `QMetaAssociation`

## 作用定位
`QMetaAssociation` 是 Qt 元类型系统对关联容器的运行时描述，允许不知道具体 `QHash`、`QMap` 等模板实参时查询其键值类型和访问能力。

## API 速查
| API | 是做什么的 |
|---|---|
| `keyMetaType()` | 查询键的 `QMetaType`。|
| `mappedMetaType()` | 查询值的 `QMetaType`。|
| `size()` | 查询容器元素数。|
| `containsKey()` | 以运行时键判断存在性。|
| `value()` | 读取某键对应的值。|
| `insertKey()` / `insertKeyValue()` | 通过运行时数据插入成员。|
| `removeKey()` | 删除指定键。|
| `canInsert()` | 查询是否支持插入。|

## 使用场景
通用属性编辑器、序列化框架、调试器或插件系统需要操作由 QVariant/元类型持有的未知关联容器。

## 常见坑与经验
- 参数通常以 `void*` 表达运行时数据，类型与对齐必须和对应 `QMetaType` 一致。
- 这不是替代静态 `QMap`/`QHash` API 的日常工具；类型擦除会削弱编译期检查并增加开销。

## 知识点覆盖
元类型、类型擦除、关联容器反射、QVariant、运行时类型安全、通用工具。
