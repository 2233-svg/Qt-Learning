# QIterable
> Qt 6.11.1 · Qt Core · 来自 `QIterable`

## 作用定位
`QIterable` 是容器经 `QVariant` 类型擦除后提供的通用迭代接口，支撑反射式工具对未知具体容器进行遍历。

## API 速查
| API | 是做什么的 |
|---|---|
| `begin()` / `end()` | 获取通用常量迭代器。|
| `mutableBegin()` / `mutableEnd()` | 获取可修改迭代器。|
| `size()` | 查询容器元素数。|
| `canReverseIterate()` | 判断是否支持反向遍历。|
| `metaContainer()` | 查询容器的元类型信息。|

## 使用场景
属性编辑器、通用序列化器、调试面板需要遍历运行时才知道类型的 Qt 容器。

## 常见坑与经验
- 类型擦除带来动态转换和性能成本，业务热路径应直接使用具体容器。
- mutable iterator 是否能修改取决于原 QVariant 是否持有可修改容器副本。

## 知识点覆盖
QVariant、类型擦除、容器反射、通用迭代、性能边界。
