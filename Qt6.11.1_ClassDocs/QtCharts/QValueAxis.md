# QValueAxis
> Qt 6.11.1 · Qt Charts · 来自 `QValueAxis`

## 作用定位
`QValueAxis` 是连续线性数值轴，适用于 XY、柱状和散点数据的普通数量级。

## API 速查
| API | 是做什么的 |
|---|---|
| `setRange(min, max)` | 设置可见数值区间。|
| `setMin()` / `setMax()` | 单独改变边界。|
| `setTickCount()` | 设置主刻度数量。|
| `setTickAnchor()` / `setTickInterval()` | 精确控制刻度起点与间隔。|
| `setMinorTickCount()` | 在主刻度之间加入次刻度。|
| `setLabelFormat()` | 设置标签格式，如 `%.2f`。|
| `applyNiceNumbers()` | 将范围和刻度调整为易读数值。|

## 使用场景
实时曲线以固定窗口滚动显示：不断更新 `setRange(now - 60, now)` 和 Y 轴的统计范围。

## 常见坑与经验
- `min == max` 无有效范围；更新范围前保证上下界有间隔。
- `applyNiceNumbers()` 会改动你设定的边界，精确工程刻度不要在最后调用它。

## 知识点覆盖
线性坐标、主次刻度、数值格式、实时范围、易读刻度算法。
