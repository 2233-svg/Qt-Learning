# QMetaContainer
> Qt 6.11.1 · Qt Core · 来自 `QMetaContainer`

## 作用定位
`QMetaContainer` 是顺序容器与关联容器元描述的共同基础，提供容器元素类型、容量、尺寸和运行时访问能力。

## API 速查
| API | 是做什么的 |
|---|---|
| `valueMetaType()` | 查询容器元素或映射值的元类型。|
| `size()` | 查询运行时容器大小。|
| `clear()` | 清空容器。|
| `isSequentialContainer()` | 判断是否为序列容器。|
| `isAssociativeContainer()` | 判断是否为关联容器。|
| `canAddValue()` | 查询是否支持添加元素。|

## 使用场景
通用属性编辑器和序列化工具针对 QVariant 持有的任意 Qt 容器决定应以数组还是 map 方式展示。

## 常见坑与经验
- 元容器 API 处理的是运行时实例地址和元类型，不提供模板级别的编译检查。
- 容器实例必须可写且类型匹配，不能把 const 或错误类型地址当作可修改容器传入。

## 知识点覆盖
容器反射、QMetaType、顺序容器、关联容器、类型擦除、运行时访问。
