# QJsonObject::iterator
> Qt 6.11.1 · Qt Core · 来自 `QJsonObject::iterator`

## 作用定位
`QJsonObject::iterator` 是可写 JSON 对象迭代器，可遍历成员并替换当前键的值。

## API 速查
| API | 是做什么的 |
|---|---|
| `key()` | 读取当前成员名。|
| `value()` | 读取或修改当前值。|
| `operator*()` | 访问当前 JSON 值代理。|
| `operator++()` | 移动到下一成员。|

## 使用场景
配置迁移时扫描所有字段，按键名替换废弃值或标准化格式。

## 常见坑与经验
- 当前 value 是代理对象；长期保存时复制为 `QJsonValue`。
- 插入、移除字段可能造成迭代器失效，结构更新应与遍历逻辑分开。

## 知识点覆盖
JSON 修改、键值遍历、代理引用、结构变更、配置迁移。
