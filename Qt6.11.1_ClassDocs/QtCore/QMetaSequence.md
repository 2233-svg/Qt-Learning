# QMetaSequence
> Qt 6.11.1 · Qt Core · 来自 `QMetaSequence`

## 作用定位
`QMetaSequence` 是顺序容器的运行时元描述，允许通用代码操作未知具体元素类型的 `QList`、`QVector` 等序列容器。

## API 速查
| API | 是做什么的 |
|---|---|
| `valueMetaType()` | 查询元素元类型。|
| `size()` | 查询元素数量。|
| `atIndex()` | 按索引读取元素到运行时缓冲。|
| `setValueAtIndex()` | 按索引修改元素。|
| `addValue()` | 在末尾添加元素。|
| `removeValueAtIndex()` | 删除指定元素。|
| `canAddValue()` | 判断是否支持追加。|
| `isRandomAccess()` | 判断是否支持高效索引访问。|

## 使用场景
通用属性表单、序列化器、脚本绑定或调试器需要在运行时浏览和编辑 QVariant 中的未知顺序容器。

## 常见坑与经验
- 运行时值通过 `void*` 与 QMetaType 协作，调用方必须提供正确构造和对齐的存储。
- 这类反射调用不适合性能关键循环；业务逻辑优先使用具体容器 API。

## 知识点覆盖
顺序容器反射、QMetaType、类型擦除、随机访问、运行时编辑。
