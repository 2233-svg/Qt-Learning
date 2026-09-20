# QMultiHash
> Qt 6.11.1 · Qt Core · 来自 `QMultiHash`

## 作用定位
`QMultiHash<Key, T>` 是允许同一键关联多个值的无序哈希容器，适合一对多索引和倒排关系。

## API 速查
| API | 是做什么的 |
|---|---|
| `insert(key, value)` | 追加一条键值关联，不覆盖同键旧值。|
| `values(key)` | 返回某键关联的全部值。|
| `find(key)` | 找到某键的一项。|
| `equal_range(key)` | 获取同键项的迭代范围。|
| `remove(key)` | 删除该键的全部关联。|
| `remove(key, value)` | 删除特定键值对。|
| `replace(key, value)` | 用单个值替换该键现有关联。|
| `uniqueKeys()` | 返回去重的键列表。|

## 使用场景
标签到对象 ID、用户名到多个会话、单词到多个文档位置等一对多索引。

## 常见坑与经验
- 遍历顺序不稳定，输出或协议不能依赖插入顺序。
- `values(key)` 创建副本；高频处理同键大集合可使用 `equal_range()`。
- 自定义 key 的 `qHash` 和相等比较必须一致。

## 知识点覆盖
多值哈希、一对多、equal range、无序迭代、自定义 hash、索引设计。
