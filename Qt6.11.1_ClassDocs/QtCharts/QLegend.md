# QLegend
> Qt 6.11.1 · Qt Charts · 来自 `QLegend`

## 作用定位
`QLegend` 显示 chart 中序列或数据项的说明标记，并可参与布局和交互。它由 `QChart` 创建和拥有。

## API 速查
| API | 是做什么的 |
|---|---|
| `setVisible()` | 显示或隐藏图例。|
| `setAlignment()` | 将图例停靠在图表边缘。|
| `setMarkerShape()` | 设置标记的默认形状。|
| `markers()` | 取得所有图例 marker。|
| `setBackgroundVisible()` | 显示图例背景。|
| `setColor()` / `setLabelColor()` | 设置背景或标签颜色。|

## 使用场景
多条曲线图中通过 marker 点击切换序列可见性，或将图例移到下方以释放绘图区宽度。

## 常见坑与经验
- 图例由 chart 管理，不要自己 delete。
- marker 与序列、slice 或 bar set 对应；数据变化时旧 marker 指针可能不再代表原来的项目。

## 知识点覆盖
图例布局、标记、交互、样式、对象所有权。
