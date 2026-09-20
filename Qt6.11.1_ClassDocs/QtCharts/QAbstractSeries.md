# QAbstractSeries
> Qt 6.11.1 · Qt Charts · 来自 `QAbstractSeries`

## 作用定位
`QAbstractSeries` 是所有 Charts 数据序列的 QObject 基类。它统一提供名称、可见性、图例关联、轴附着和类型识别；实际数据 API 在 `QXYSeries`、`QBarSeries`、`QPieSeries` 等子类。

## API 速查
| API | 是做什么的 |
|---|---|
| `setName()` | 设置图例和标识使用的名称。|
| `setVisible()` | 显示或隐藏整个序列。|
| `setOpacity()` | 设置序列整体透明度。|
| `attachAxis()` / `detachAxis()` | 关联或解除坐标轴。|
| `attachedAxes()` | 查询已附着轴。|
| `chart()` | 返回所属 `QChart`。|
| `type()` | 判断实际序列类型。|

## 使用场景
编写通用图表控制器时，只依赖此类进行序列显示、名称和轴管理；需要写入数据时再用 `qobject_cast` 分派到具体类型。

## 常见坑与经验
- 序列只有在进入 chart 后才能附轴。
- 多条序列可以共享轴，但轴范围应覆盖它们的共同数据尺度。

## 知识点覆盖
多态序列、图表所有权、坐标轴附着、可见性、通用控制层。
