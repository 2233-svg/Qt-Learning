# QPolarChart
> Qt 6.11.1 · Qt Charts · 来自 `QPolarChart`

## 作用定位
`QPolarChart` 是极坐标图表容器：一个轴解释角度，另一个轴解释半径。它仍是 `QChart`，但轴方向和坐标映射语义不同。

## API 速查
| API | 是做什么的 |
|---|---|
| `addAxis(axis, PolarOrientation)` | 以角度轴或径向轴身份加入。|
| `axes(orientation, series)` | 查询某方向附着的轴。|
| `PolarOrientationAngular` | 表示绕圆心变化的角度轴。|
| `PolarOrientationRadial` | 表示从圆心向外的半径轴。|

## 使用场景
风向/风速、雷达图式数据、周期信号相位、极坐标散点。

## 常见坑与经验
- 同一 `QValueAxis` 在笛卡尔和极坐标中解释不同；标签格式与范围需按角度或半径设计。
- 序列和轴仍必须显式附着，默认轴未必符合极坐标需求。

## 知识点覆盖
极坐标、角度与半径、轴方向、周期数据、坐标映射。
