# QBarSet
> Qt 6.11.1 · Qt Charts · 来自 `QBarSet`

## 作用定位
`QBarSet` 是柱状系列中的一个数据维度：其第 N 个数值对应类别轴的第 N 个类别。一个系列包含多个 set，决定并排或堆叠的多个组成。

## API 速查
| API | 是做什么的 |
|---|---|
| `append()` | 在末尾添加一个或多个值。|
| `replace(index, value)` | 修改指定类别的值。|
| `remove(first, count)` | 删除一段值。|
| `at(index)` | 读取一个类别值。|
| `count()` | 查询值数量。|
| `setLabel()` | 设置图例显示名。|
| `setColor()` / `setBorderColor()` | 设置柱体外观。|
| `setSelectedBars()` | 标记某些索引柱为选中。|

## 使用场景
```cpp
auto *actual = new QBarSet("Actual");
*actual << 42 << 55 << 47;
series->append(actual);
```

## 常见坑与经验
- 缺失值与零值语义不同；不要无条件用 `0` 填补未采集数据。
- `operator<<` 很方便，但批量数据导入时应校验长度与类别轴同步。

## 知识点覆盖
类别索引、数据集、柱体样式、选择状态、缺失值语义。
