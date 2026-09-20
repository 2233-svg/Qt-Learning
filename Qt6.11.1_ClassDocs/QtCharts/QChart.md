# QChart
> Qt 6.11.1 · Qt Charts · 来自 `QChart`

## 作用定位
`QChart` 是图表的场景容器：它持有序列、坐标轴、图例和绘图区，并协调主题、动画、缩放和坐标映射。数据本身在 `QAbstractSeries` 子类中，轴只在附着到序列后才真正决定数据坐标。

## API 速查
| API | 是做什么的 |
|---|---|
| `addSeries()` / `removeSeries()` | 管理图表中的数据序列；加入后图表取得所有权。|
| `addAxis()` / `removeAxis()` | 管理坐标轴。|
| `setAxisX()` / `setAxisY()` | 便捷地将轴附着到指定序列。|
| `createDefaultAxes()` | 根据现有序列创建合适的默认轴。|
| `axes()` / `series()` | 查询当前组成。|
| `setTitle()` / `setTheme()` | 设置标题与整体视觉主题。|
| `legend()` | 取得图例对象。|
| `zoomIn()` / `zoomOut()` / `zoomReset()` | 操作显示范围。|
| `scroll()` | 平移当前可见坐标范围。|
| `mapToPosition()` / `mapToValue()` | 在数据坐标和绘图区像素坐标间转换。|

## 使用场景
```cpp
auto *series = new QLineSeries;
series->append({0, 3}); series->append({1, 5});
QChart chart;
chart.addSeries(series);
chart.createDefaultAxes();
chart.setTitle("Hourly throughput");
```

## 常见坑与经验
- 添加序列后由 chart 管理其生命周期；不要再手动删除。
- `createDefaultAxes()` 会替换/创建轴，已有精细配置时应手工创建并 `attachAxis()`。
- 缩放是修改显示范围，不会删除数据；实时图应自己维护数据窗口和轴范围。

## 知识点覆盖
图表组合、序列所有权、坐标轴附着、缩放、像素/数据坐标映射、主题与图例。
