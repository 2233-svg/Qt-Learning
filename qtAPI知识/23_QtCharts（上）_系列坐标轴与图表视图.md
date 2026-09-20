# Qt Charts（上）：系列、坐标轴与图表视图

> Qt Charts 将数据绘制拆成“系列（Series）+ 坐标轴（Axis）+ 图表（Chart）+ 视图（ChartView）”。先掌握这四层的职责，再处理缩放、交互和高频数据更新。

## 1. 模块和最小折线图

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets Charts)
target_link_libraries(mytarget PRIVATE Qt6::Widgets Qt6::Charts)
```

```cpp
#include <QChart>
#include <QChartView>
#include <QLineSeries>
#include <QValueAxis>

auto *series = new QLineSeries;
series->setName(QStringLiteral("温度"));
series->append(0, 18.5);
series->append(1, 19.2);
series->append(2, 21.0);

auto *chart = new QChart;
chart->addSeries(series);
chart->setTitle(QStringLiteral("一天温度"));

auto *axisX = new QValueAxis;
axisX->setRange(0, 2);
axisX->setTitleText(QStringLiteral("小时"));
auto *axisY = new QValueAxis;
axisY->setRange(0, 30);
axisY->setTitleText(QStringLiteral("摄氏度"));
chart->addAxis(axisX, Qt::AlignBottom);
chart->addAxis(axisY, Qt::AlignLeft);
series->attachAxis(axisX);
series->attachAxis(axisY);

auto *view = new QChartView(chart);
view->setRenderHint(QPainter::Antialiasing);
```

`QLineSeries` 保存数据，`QChart` 管理系列和坐标轴，`QChartView` 负责在 Widgets 中显示和接收交互。对象通常由父子关系管理，不要在图表销毁后继续使用系列指针。

## 2. QXYSeries 与数据更新

`QLineSeries`、`QSplineSeries`、`QScatterSeries` 都继承 `QXYSeries`。常用操作：

```cpp
series->append(points);
series->replace(points);   // 批量替换通常比逐点更新更快
series->removePoints(0, count);
series->clear();
```

高频数据场景应批量更新，并控制可视窗口内的数据量：

```cpp
QVector<QPointF> window = readLatestPoints();
series->replace(window);
axisX->setRange(window.first().x(), window.last().x());
```

逐点 `append()` 会触发多次通知和重绘；可在批量更新期间暂时关闭动画或合并刷新。

## 3. 坐标轴类型

### 3.1 QValueAxis

`QValueAxis` 用于连续数值，核心属性是 `min`、`max`、`tickCount`、`labelFormat` 和 `minorTickCount`。

```cpp
axisY->setLabelFormat(QStringLiteral("%.1f"));
axisY->setTickCount(6);
axisY->setMinorTickCount(1);
```

### 3.2 QBarCategoryAxis

柱状图的分类轴使用字符串类别：

```cpp
auto *axis = new QBarCategoryAxis;
axis->append({QStringLiteral("一月"), QStringLiteral("二月"), QStringLiteral("三月")});
```

### 3.3 QDateTimeAxis

时间序列可以使用 `QDateTimeAxis`，数据点的 x 值仍以毫秒时间戳表示：

```cpp
auto *timeAxis = new QDateTimeAxis;
timeAxis->setFormat(QStringLiteral("MM-dd hh:mm"));
timeAxis->setRange(QDateTime::currentDateTime().addSecs(-3600),
                   QDateTime::currentDateTime());
```

同一方向不要混用不兼容的轴域，例如在一个方向同时绑定线性值轴和对数轴。

### 3.4 QLogValueAxis

对数轴适合跨多个数量级的数据。所有值必须为正数，零和负数应在业务层过滤或转换；否则图表会出现空白或警告。

## 4. 轴与系列的连接

```cpp
chart->addAxis(axisX, Qt::AlignBottom);
chart->addAxis(axisY, Qt::AlignLeft);
series->attachAxis(axisX);
series->attachAxis(axisY);
```

`createDefaultAxes()` 可以快速创建默认轴：

```cpp
chart->createDefaultAxes();
```

但生产界面通常应显式创建轴，才能控制范围、格式、单位和本地化。一个系列可以绑定多个轴，但要明确每个轴承担的语义。

## 5. 图例与标题

```cpp
chart->legend()->setVisible(true);
chart->legend()->setAlignment(Qt::AlignBottom);
chart->legend()->setMarkerShape(QLegend::MarkerShapeFromSeries);
```

系列名称会显示在图例中。用户点击图例标记时，可以切换系列可见性：

```cpp
for (QLegendMarker *marker : chart->legend()->markers()) {
    QObject::connect(marker, &QLegendMarker::clicked,
                     [marker] { marker->series()->setVisible(!marker->series()->isVisible()); });
}
```

图例文本应表达单位和数据含义，避免只写“系列 1”。

## 6. 柱状图、饼图和散点图

### 6.1 柱状图

```cpp
auto *set = new QBarSet(QStringLiteral("销量"));
*set << 12 << 18 << 15;
auto *bars = new QBarSeries;
bars->append(set);
chart->addSeries(bars);
```

柱状系列通常与 `QBarCategoryAxis` 和 `QValueAxis` 配合。堆叠、百分比和横向柱状图分别使用对应派生类。

### 6.2 饼图

```cpp
auto *pie = new QPieSeries;
pie->append(QStringLiteral("桌面"), 60);
pie->append(QStringLiteral("移动"), 40);
chart->addSeries(pie);
```

饼图不使用坐标轴；切片有 `clicked`、`hovered` 和 `percentageChanged` 等信号。类别过多时饼图可读性迅速下降，应考虑柱状图。

### 6.3 散点图

```cpp
auto *scatter = new QScatterSeries;
scatter->setMarkerSize(10.0);
scatter->append(1.2, 3.4);
scatter->append(2.0, 4.8);
```

散点适合观察离散样本；若点数很大，需评估绘制和交互成本。

## 7. 交互：缩放、滚动和选择

`QChart` 提供 `zoomIn()`、`zoomOut()`、`zoomReset()`、`scroll()` 等方法：

```cpp
chart->zoomIn();
chart->scroll(20, 0);
chart->zoomReset();
```

`QChartView` 可启用橡皮筋缩放：

```cpp
view->setRubberBand(QChartView::RectangleRubberBand);
```

自定义鼠标交互时要把像素坐标转换为领域坐标，使用 `chart->mapToValue()`/`mapToPosition()`，不要直接把窗口坐标当作数据值。

## 8. QML ChartView

```qml
import QtCharts

ChartView {
    anchors.fill: parent
    antialiasing: true
    legend.visible: true

    LineSeries {
        name: qsTr("温度")
        XYPoint { x: 0; y: 18.5 }
        XYPoint { x: 1; y: 19.2 }
    }

    ValueAxis {
        id: axisX
        min: 0
        max: 2
    }
}
```

QML 图表可以直接绑定属性和模型。大量数据不要在 QML 中逐个生成 `XYPoint`，应从 C++ 模型或批量 API 提供数据。

## 9. 主题、动画与渲染

```cpp
chart->setTheme(QChart::ChartThemeDark);
chart->setAnimationOptions(QChart::SeriesAnimations);
```

动画会增加更新成本。实时数据图通常关闭系列动画，避免每个点进入动画队列。启用 OpenGL 加速只适用于部分 `QLineSeries` 和 `QScatterSeries`，而且加速系列不支持系列动画；应在目标硬件上实际评估。

## 10. 常见问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| 曲线不显示 | 未 attachAxis 或轴范围不包含数据 | 连接轴并检查 min/max |
| 时间标签错位 | x 值不是毫秒时间戳 | 使用 `QDateTime::toMSecsSinceEpoch()` |
| 图表更新卡顿 | 逐点更新且每次重绘 | 批量 `replace()` 并降低刷新频率 |
| 图例名称为空 | 系列未设置 name | 设置语义化名称 |
| 缩放后无法恢复 | 忘记 `zoomReset()` | 提供显式重置命令 |
| 对数轴空白 | 数据含零或负数 | 过滤非法值或改用线性轴 |

## 11. 自测题

1. QChart、QChartView 和 QLineSeries 分别负责什么？
2. 为什么高频数据更适合 `replace()` 而不是逐点 append？
3. QDateTimeAxis 的数据点 x 值通常使用什么单位？
4. 饼图为什么不需要坐标轴？
5. OpenGL 加速系列有什么限制？

### 参考答案

1. 图表容器、Widgets 显示视图、具体数据系列。
2. 批量替换减少通知和重绘次数，能降低 UI 抖动。
3. Unix epoch 毫秒时间戳。
4. 饼图用扇区角度/面积表达比例，不依赖二维坐标。
5. 主要支持线和散点系列，且加速系列不支持系列动画。

## 12. 小结

Qt Charts 的稳定用法是先确定数据域和轴域，再添加系列和视图，最后叠加交互与主题。实时场景重点控制批量更新、轴范围和动画；分析场景重点保证单位、时间戳和图例语义准确。
