# QPieSlice
> Qt 6.11.1 · Qt Charts · 来自 `QPieSlice`

## 作用定位
`QPieSlice` 是一个饼图数据项，保存标签、数值、颜色、爆炸偏移、标签位置和交互状态。

## API 速查
| API | 是做什么的 |
|---|---|
| `setValue()` | 设置该部分的数值。|
| `percentage()` | 读取其占系列总和的比例。|
| `setLabel()` | 设置标签。|
| `setLabelVisible()` | 单独显示标签。|
| `setExploded()` | 将切片向外偏移以强调。|
| `setExplodeDistanceFactor()` | 设置偏移距离。|
| `setBrush()` / `setPen()` | 设置填充和边框。|
| `clicked()` / `hovered()` | 处理切片交互。|

## 使用场景
点击某一比例项后 `setExploded(true)`，同时在侧栏显示该项的详细数字。

## 常见坑与经验
- `percentage()` 随 series 内任意值变化而变化，不应作为持久业务字段缓存。
- 爆炸效果应只用于少数高亮项，否则视觉会失去层级。

## 知识点覆盖
饼图数据项、比例计算、交互高亮、标签位置、样式。
