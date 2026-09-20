# QMetaSequence::Iterable::Iterator
> Qt 6.11.1 · Qt Core · 来自 `QMetaSequence::Iterable::Iterator`

## 作用定位
`QMetaSequence::Iterable::Iterator` 是通用顺序容器的可写运行时迭代器，支持反射式读取和修改当前位置元素。

## API 速查
| API | 是做什么的 |
|---|---|
| `value()` | 读取当前元素。|
| `setValue()` | 用匹配元类型的数据替换当前元素。|
| `operator++()` | 推进至下一元素。|
| `operator==()` | 判断迭代位置。|

## 使用场景
通用配置升级工具在不依赖具体 `QList<T>` 模板的条件下，原地转换已知元素类型。

## 常见坑与经验
- `setValue()` 的输入类型必须匹配元素 QMetaType；无效转换不能依赖静默默认值。
- 插入、删除或容器 detach 可能使 iterator 失效，复杂迁移应先复制再替换整个容器。

## 知识点覆盖
运行时修改、QMetaType、顺序容器、迭代器失效、配置迁移。
