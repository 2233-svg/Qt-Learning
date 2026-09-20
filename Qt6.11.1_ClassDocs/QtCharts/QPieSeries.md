# QPieSeries
> Qt 6.11.1 · Qt Charts · 来自 `QPieSeries`

## 作用定位
`QPieSeries` 以多个 `QPieSlice` 表示整体的部分构成，可配置起止角、半径、圆心和甜甜圈孔径。

## API 速查
| API | 是做什么的 |
|---|---|
| `append(label, value)` | 创建并加入一个切片。|
| `append(slice)` / `remove(slice)` | 管理切片，加入后 series 取得所有权。|
| `slices()` | 读取当前切片。|
| `setHoleSize()` | 设置甜甜圈孔的相对大小。|
| `setPieSize()` | 设置相对绘图区的半径。|
| `setPieStartAngle()` / `setPieEndAngle()` | 设置绘制扇区范围。|
| `setLabelsVisible()` | 显示所有切片标签。|
| `sum()` | 返回所有切片值之和。|

## 使用场景
展示有限且互斥的组成，例如预算分配或状态占比。类别超过五六个时，排序柱状图通常更易比较。

## 常见坑与经验
- 值为负或总和为零没有可靠的“占比”解释，数据应先校验。
- 饼图主要比较大致份额，读者很难比较相近扇形；不要用它替代精确排名。
- `take()` 会移出而不删除 slice，适合转移所有权。

## 知识点覆盖
部分整体、切片所有权、甜甜圈、角度范围、比例数据、图表选择。
