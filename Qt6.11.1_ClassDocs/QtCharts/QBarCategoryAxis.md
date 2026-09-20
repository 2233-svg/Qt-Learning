# QBarCategoryAxis
> Qt 6.11.1 · Qt Charts · 来自 `QBarCategoryAxis`

## 作用定位
`QBarCategoryAxis` 为柱状图提供离散字符串类别，类别位置对应 bar set 中值的索引。

## API 速查
| API | 是做什么的 |
|---|---|
| `append()` | 添加类别名。|
| `remove()` | 删除类别名。|
| `clear()` | 清空全部类别。|
| `categories()` | 读取当前类别列表。|
| `setCategories()` | 一次替换类别。|
| `count()` | 读取类别数。|

## 使用场景
月度销量、部门比较、问卷选项等固定类别柱状图。

## 常见坑与经验
- 第 N 个类别对应 `QBarSet` 的第 N 个值；两者数量不一致会造成空柱或无标签。
- 类别应是稳定标识的显示文本，不要每次刷新随意变顺序。

## 知识点覆盖
离散轴、索引对齐、柱状图类别、标签管理。
