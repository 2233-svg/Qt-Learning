# QXYSeries
> Qt 6.11.1 · Qt Charts · 来自 `QXYSeries`

## 作用定位
`QXYSeries` 是折线、散点和样条系列的共同数据层，保存有序 `QPointF` 点集并提供点替换、选择和可视化样式。

## API 速查
| API | 是做什么的 |
|---|---|
| `append()` | 添加一个或一批 XY 点。|
| `replace()` | 替换全部、指定索引或指定点。|
| `remove()` / `clear()` | 删除点或清空数据。|
| `points()` | 取得当前点集快照。|
| `at()` | 按索引读取一个点。|
| `setPen()` / `setBrush()` | 设置线或点的画笔、填充。|
| `setPointsVisible()` | 显示每个数据点的标记。|
| `setPointLabelsVisible()` | 显示数据标签。|
| `replace(selectedPoints)` | 批量更新选择状态。|

## 使用场景
实时数据优先累积一批 `QPointF` 后一次 `replace()`，而不是每收到一个采样就反复 `append()` 并触发重绘。

## 常见坑与经验
- 点的 X 顺序决定线段走向，图表不会自动排序。
- `points()` 返回副本；大数据集上频繁读取会有复制成本。
- 单点更新时用 `replace(index, point)`，批量刷新时用 `replace(list)`。

## 知识点覆盖
XY 数据、批量更新、点选择、样式、实时曲线性能、数据排序。
