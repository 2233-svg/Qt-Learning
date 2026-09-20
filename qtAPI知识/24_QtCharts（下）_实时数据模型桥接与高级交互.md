# Qt Charts（下）：实时数据、模型桥接与高级交互

## 1. 实时曲线的设计目标

实时图表同时面对数据速率、绘制速率和用户交互速率。不要让每条输入消息直接触发一次重绘，而应把数据先写入环形缓冲，再按固定帧率批量刷新。

```cpp
class RealtimePlot : public QObject
{
    Q_OBJECT
public:
    explicit RealtimePlot(QObject *parent = nullptr) : QObject(parent)
    {
        connect(&timer, &QTimer::timeout, this, &RealtimePlot::flush);
        timer.start(33); // 约 30 FPS 的 UI 刷新
    }

    void pushSample(const QPointF &point)
    {
        pending.push_back(point);
        if (pending.size() > 5000)
            pending.erase(pending.begin(), pending.begin() + 1000);
    }

signals:
    void pointsReady(QVector<QPointF> points);

private slots:
    void flush()
    {
        if (pending.isEmpty())
            return;
        emit pointsReady(std::exchange(pending, {}));
    }

private:
    QTimer timer;
    QVector<QPointF> pending;
};
```

在 UI 层收到一批点后再调用 `QXYSeries::replace()`，并同步更新轴范围。数据采集线程不应直接操作图表对象。

## 2. 模型桥接与数据域

图表系列可以作为视图，业务数据应留在模型。推荐流程：

1. 模型保存带时间戳的领域数据；
2. 控制器按可视时间窗生成 `QVector<QPointF>`；
3. 图表层批量替换系列；
4. 用户缩放时只改变窗口，不修改原始数据。

```cpp
QVector<QPointF> pointsForRange(const QVector<QPointF> &all,
                                qreal left, qreal right)
{
    QVector<QPointF> visible;
    for (const QPointF &point : all) {
        if (point.x() >= left && point.x() <= right)
            visible.push_back(point);
    }
    return visible;
}
```

数据量很大时使用二分查找定位时间窗口，并进行抽样或降采样，避免把百万点全部交给绘制层。

## 3. 点、系列和图例交互

```cpp
QObject::connect(series, &QXYSeries::hovered,
                 [chartView](const QPointF &point, bool state) {
    if (state) {
        const QPoint pos = chartView->chart()->mapToPosition(point).toPoint();
        chartView->setToolTip(QStringLiteral("x=%1, y=%2")
                              .arg(point.x()).arg(point.y()));
    } else {
        chartView->setToolTip({});
    }
});
```

`clicked`、`pressed`、`released`、`doubleClicked` 和 `hovered` 都提供领域坐标。工具提示应使用本地化格式，并在鼠标离开时清除。点选择状态可以使用 `selectPoint()`/`deselectPoint()`，但业务选中项仍应由控制器或模型保存。

## 4. 缩放和坐标转换

```cpp
void ChartController::zoomToRect(const QRectF &plotRect)
{
    const QPointF topLeft = chart->mapToValue(plotRect.topLeft());
    const QPointF bottomRight = chart->mapToValue(plotRect.bottomRight());
    axisX->setRange(topLeft.x(), bottomRight.x());
    axisY->setRange(bottomRight.y(), topLeft.y());
}
```

像素坐标原点通常在左上，而数据坐标的 y 轴方向相反，转换时不要手工猜测比例。对于时间轴，使用 `QDateTime` 格式化显示，不要直接把毫秒数显示给用户。

## 5. 模式切换和多轴

一个系列可以同时连接左右两个 Y 轴，但要让颜色、单位和图例保持一致：

```cpp
auto *leftAxis = new QValueAxis;
auto *rightAxis = new QValueAxis;
leftAxis->setTitleText(QStringLiteral("温度 (°C)"));
rightAxis->setTitleText(QStringLiteral("湿度 (%)"));
chart->addAxis(leftAxis, Qt::AlignLeft);
chart->addAxis(rightAxis, Qt::AlignRight);
temperature->attachAxis(leftAxis);
humidity->attachAxis(rightAxis);
```

多轴虽方便比较不同单位，但会增加认知负担。能归一化或拆成小 multiples 时，不要滥用双轴。

## 6. OpenGL 加速的取舍

```cpp
series->setUseOpenGL(true);
```

OpenGL 加速主要适用于 `QLineSeries` 和 `QScatterSeries`。启用后系列绘制到覆盖图表的透明 OpenGL 视图，可能影响叠加项、截图、动画和某些平台合成。加速系列不支持系列动画，应该在目标显卡和窗口系统上验证。

数据点大量但交互简单时可以尝试加速；若需要复杂点标签、区域系列边缘或严格截图一致性，普通绘制反而更可控。

## 7. QML 与 C++ 数据桥接

### 7.1 C++ 暴露点数组

```cpp
class ChartData : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QVariantList values READ values NOTIFY valuesChanged)
public:
    QVariantList values() const;
signals:
    void valuesChanged();
};
```

QML 可以把 `values` 转换为系列点，但高频大数组会产生复制和 JavaScript 开销。实时场景更适合 C++ 直接持有 `QXYSeries*`（在 GUI 线程）并批量更新，QML 只绑定范围、标题和状态。

### 7.2 QML ChartView 交互

```qml
ChartView {
    id: chartView
    property real lower: 0
    property real upper: 100

    ValueAxis { id: axisY; min: chartView.lower; max: chartView.upper }
    LineSeries { id: line; axisY: axisY }

    MouseArea {
        anchors.fill: parent
        onWheel: function (event) {
            const factor = event.angleDelta.y > 0 ? 0.9 : 1.1
            chartView.lower *= factor
            chartView.upper *= factor
            event.accepted = true
        }
    }
}
```

自定义交互时要避免 MouseArea 覆盖图例、滚动条和其他输入控件。可以在更小的 plot area 上接收事件，或使用 Qt Quick Pointer Handlers 管理抢抓。

## 8. 选择、标记和注释

Qt Charts 没有为所有注释场景提供统一的高层组件。常用做法是把 `QGraphicsSimpleTextItem`、`QGraphicsLineItem` 或自定义 QML Item 叠加到图表上，并在轴范围变化时重新计算位置。

注释对象应订阅 `plotAreaChanged`、轴范围变化和窗口缩放，不能只在创建时计算一次。若注释属于业务数据，保存领域坐标而不是像素坐标。

## 9. 导出图像和数据

```cpp
const QPixmap pixmap = chartView->grab();
pixmap.save(QStringLiteral("chart.png"));

QFile file(QStringLiteral("points.csv"));
if (file.open(QIODevice::WriteOnly | QIODevice::Text)) {
    QTextStream out(&file);
    for (const QPointF &point : series->points())
        out << point.x() << ',' << point.y() << '\n';
}
```

导出前暂停动画并确保布局完成。CSV 的小数点、日期格式和编码应符合目标用户地区；大数据导出不要从图表当前可见点反推完整数据。

## 10. 性能诊断

- 统计输入速率、批量大小和每次刷新耗时；
- 观察系列点数、轴重算次数和动画队列；
- 对 2D 图表使用 profiler 和平台 GPU 工具；
- 关闭图例、点标签和抗锯齿做对照测试；
- 将数据准备、绘制和导出分开计时。

## 11. 常见错误

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| 实时曲线延迟累积 | 每条数据立即重绘 | 定时批量刷新并限制队列 |
| 双轴读数误导 | 单位和颜色不清晰 | 标注单位，统一颜色语义 |
| Tooltip 位置错误 | 把像素坐标当领域坐标 | 使用 `mapToPosition`/`mapToValue` |
| OpenGL 后截图异常 | 加速系列在覆盖视图绘制 | 目标平台验证，必要时关闭加速 |
| QML 卡顿 | 大数组频繁跨 C++/JS 拷贝 | C++ 批量更新系列 |
| 注释漂移 | 只保存像素坐标 | 保存领域坐标并响应轴变化 |

## 12. 自测题

1. 实时图表为什么要限制刷新频率？
2. 业务模型和图表系列应如何分工？
3. mapToValue 与 mapToPosition 各自转换什么？
4. 多 Y 轴的主要风险是什么？
5. OpenGL 加速为什么必须在目标平台验证？

### 参考答案

1. 绘制和布局有成本，逐条刷新会让 UI 线程被重绘占满并产生延迟。
2. 模型保存完整领域数据，系列只承载当前可视窗口的绘制数据。
3. 前者把像素位置转成领域坐标，后者把领域坐标转成像素位置。
4. 不同单位和刻度容易造成视觉误判，必须强化标签和颜色语义。
5. 它依赖平台合成、显卡和覆盖视图，可能影响动画、截图和叠加项。

## 13. 小结

高级图表开发的核心是控制数据流：采集线程负责产生数据，模型负责保存和筛选，GUI 线程批量更新系列，图表负责把领域坐标映射为视觉。缩放、多轴、OpenGL 和导出都是在这条边界上增加能力，不能替代清晰的数据模型。
