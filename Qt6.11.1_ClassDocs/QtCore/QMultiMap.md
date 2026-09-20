# QMultiMap
> Qt 6.11.1 · Qt Core · 来自 `QMultiMap`

## 作用定位
`QMultiMap<Key, T>` 是按键排序、允许一键对应多个值的关联容器，适合有序一对多关系和按键范围遍历。

## API 速查
| API | 是做什么的 |
|---|---|
| `insert(key, value)` | 增加一条键值关联。|
| `values(key)` | 返回某键全部值。|
| `find(key)` / `lowerBound()` | 查找键或范围起点。|
| `equal_range(key)` | 获取同键关联区间。|
| `remove(key)` | 删除该键全部值。|
| `remove(key, value)` | 删除特定关联。|
| `replace(key, value)` | 将同键关系替换为一个值。|
| `uniqueKeys()` | 返回去重且排序的键列表。|

## 使用场景
按时间、层级或排序 ID 保存多个记录，并需要按键区间读取、稳定导出或分组显示。

## 常见坑与经验
- 它的有序性来自 key 比较，不代表同键多个 value 的业务顺序契约。
- 若只需快速一对多查找且无需有序遍历，`QMultiHash` 通常更合适。
- 自定义 key 比较必须满足严格弱序，否则 equal range 与顺序行为不可靠。

## 知识点覆盖
有序多值映射、一对多、范围查询、键比较、稳定输出、复杂度取舍。
