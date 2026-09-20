# QCborMap::Iterator
> Qt 6.11.1 · Qt Core · 来自 `QCborMap::Iterator`

## 作用定位
`QCborMap::Iterator` 是可写的 CBOR map 迭代器，用于就地读取或修改现有键的值。

## API 速查
| API | 是做什么的 |
|---|---|
| `key()` | 读取当前键。|
| `value()` | 读取或修改当前值。|
| `operator++()` | 移动到下一项。|
| `operator*()` | 访问当前键值项。|

## 使用场景
协议迁移时遍历 map，替换废弃字段值或清理可识别的无效项。

## 常见坑与经验
- 修改 map 结构时避免继续依赖旧迭代器；删除后以容器 API 返回的位置继续。

## 知识点覆盖
可写 map 迭代、数据迁移、迭代器失效、CBOR。
