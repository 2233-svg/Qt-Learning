# QMetaAssociation::Iterable::Iterator
> Qt 6.11.1 · Qt Core · 来自 `QMetaAssociation::Iterable::Iterator`

## 作用定位
`QMetaAssociation::Iterable::Iterator` 允许通用反射代码在运行时遍历并修改关联容器的当前键值项。

## API 速查
| API | 是做什么的 |
|---|---|
| `key()` | 读取当前键的运行时值。|
| `value()` | 读取或写入当前值。|
| `operator++()` | 前进到下一项。|
| `operator==()` | 比较迭代状态。|

## 使用场景
通用配置迁移器需要遍历未知 `QMap`/`QHash` 类型，并就地规范化可转换的值。

## 常见坑与经验
- 不应通过迭代器修改键；关联容器的键决定其哈希或排序位置。
- 对容器做插入和删除会影响迭代状态，修改结构前先设计安全的遍历策略。

## 知识点覆盖
运行时修改、关联容器、键不变量、迭代器失效、反射工具。
