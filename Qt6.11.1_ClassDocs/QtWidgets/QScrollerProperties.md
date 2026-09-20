# QScrollerProperties

> Qt 6.11.1 · Qt Widgets · 来自 `QScrollerProperties`

## 1. 先建立直觉

`QScrollerProperties` 是 `QScroller` 的“手感参数表”。它决定滚动从按下到拖动、从释放到减速、越界回弹、吸附位置、帧率等细节。

你可以把 `QScroller` 看成滚动引擎，把 `QScrollerProperties` 看成悬挂、摩擦、速度上限和回弹阻尼。它不直接滚动内容，只影响滚动过程的物理感。

## 2. 类说明

`QScrollerProperties` 是值类型。通过 `scrollMetric()` 读取某个指标，通过 `setScrollMetric()` 修改指标，然后交给 `QScroller::setScrollerProperties()` 生效。

这些指标使用 `QVariant` 承载，类型必须匹配 metric 预期。多数是 `qreal`，但曲线、枚举等指标有各自类型。调参时建议少量修改、反复试用，而不是一次改十几个值。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QScrollerProperties()` | 创建一份默认滚动属性。 |
| `scrollMetric(ScrollMetric)` | 读取某个滚动指标。 |
| `setScrollMetric(ScrollMetric, QVariant)` | 设置某个滚动指标。 |
| `setDefaultScrollerProperties()` | 设置全局默认属性，影响之后创建/使用的 scroller。 |
| `unsetDefaultScrollerProperties()` | 恢复 Qt 默认滚动属性。 |
| `FrameRate` | 控制滚动动画帧率，可选 `Fps60`、`Fps30`、`Fps20`、`Standard`。 |
| `DragStartDistance` | 从按下到开始拖动所需最小距离。 |
| `MousePressEventDelay` | 鼠标按压事件延迟，用于判断点击还是拖动滚动。 |
| `MinimumVelocity` / `MaximumVelocity` | 惯性滚动触发速度和速度上限。 |
| `DecelerationFactor` | 减速强度，影响滑行距离和时间。 |
| `ScrollingCurve` | 减速动画曲线。 |
| `AxisLockThreshold` | 接近水平/垂直移动时锁轴的阈值。 |
| `HorizontalOvershootPolicy` / `VerticalOvershootPolicy` | 控制水平/垂直越界回弹是否允许。 |
| `OvershootDragDistanceFactor` | 拖动越界时最大超出距离比例。 |
| `SnapPositionRatio` / `SnapTime` | 控制吸附到分页/位置点的阈值和时间。 |

## 4. 关键用法

```cpp
auto *scroller = QScroller::scroller(view->viewport());

QScrollerProperties props = scroller->scrollerProperties();
props.setScrollMetric(QScrollerProperties::DragStartDistance, 0.015);
props.setScrollMetric(QScrollerProperties::DecelerationFactor, 0.25);
props.setScrollMetric(QScrollerProperties::FrameRate, QScrollerProperties::Fps60);

scroller->setScrollerProperties(props);
```

关闭越界回弹：

```cpp
props.setScrollMetric(QScrollerProperties::HorizontalOvershootPolicy,
                      QScrollerProperties::OvershootAlwaysOff);
props.setScrollMetric(QScrollerProperties::VerticalOvershootPolicy,
                      QScrollerProperties::OvershootAlwaysOff);
```

## 5. 使用场景

适合给触摸滚动调手感：列表要更稳、图片网格要更轻、分页卡片要吸附、工业触摸屏要减少误拖、低性能设备要降低帧率。

如果只是要滚动到某个位置，不需要改属性，直接用 `QScroller::scrollTo()` 或滚动条 API。属性调的是整体感觉，不是一次性动作。

## 6. 常见坑与经验

metric 的单位不总是像素。很多距离和速度按物理单位或比例表达，这样才能跨 DPI 设备保持手感。不要把它们当普通 widget 坐标随便填。

全局默认属性会影响范围很广。产品统一手感可以用它；单个控件试验时更推荐改具体 scroller 的属性。

调参要有目标：减少误触优先调 `DragStartDistance` 和 `MousePressEventDelay`；想让滚动更短优先调 `DecelerationFactor` 和速度上限；想做分页体验则调 snap 相关指标。
