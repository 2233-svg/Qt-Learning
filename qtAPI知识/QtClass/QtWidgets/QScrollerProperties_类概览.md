# QScrollerProperties：配置动量滚动的物理参数

> Qt 6.11.1 · `#include <QScrollerProperties>` · 模块：`Qt6::Widgets`

`QScrollerProperties` 是 `QScroller` 的参数集合，控制按下延迟、拖动阈值、速度平滑、减速、吸附、overshoot 和帧率等滚动行为。它是可拷贝的值类型，通过 `QScroller::setScrollerProperties()` 应用到某个 scroller。

## 使用建议

Qt 的默认值是平台相关的，目的是模拟当前平台的滚动手感。大多数应用不需要全量调参。真正需要修改时，优先只改一两个明确影响体验的 metric，例如关闭 overshoot、降低最高速度、设置帧率，而不是复制一套“看起来合理”的参数。

metric 大多使用物理单位：米、秒、米/秒，`QScroller` 会按 DPI 转成像素。某些窗口系统报告的 DPI 可能并不物理准确，所以调参要在目标设备上验证。

## 全局默认与局部设置

`setDefaultScrollerProperties()` 只影响之后新建的 `QScrollerProperties` 默认值，不会修改已经存在的 properties 或 scroller。若只想修改某个 scroller，读取它的 properties，改 metric，再设置回该 scroller。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QScrollerProperties()` | 构造平台默认参数集合。 |
| `QScrollerProperties(const QScrollerProperties &)` | 拷贝参数集合。 |
| `operator=(const QScrollerProperties &)` | 赋值。 |
| `operator==` / `operator!=` | 比较两个参数集合。 |
| `scrollMetric(ScrollMetric) const` | 读取指定 metric，返回 `QVariant`。 |
| `setScrollMetric(ScrollMetric, const QVariant &)` | 设置指定 metric；类型需匹配该 metric 语义。 |
| `setDefaultScrollerProperties(const QScrollerProperties &)` | 修改之后新建 properties 的全局默认值。 |
| `unsetDefaultScrollerProperties()` | 恢复平台默认参数。 |
| `OvershootWhenScrollable` | 只有内容可滚动时允许 overshoot。 |
| `OvershootAlwaysOff` | 禁用 overshoot。 |
| `OvershootAlwaysOn` | 始终允许 overshoot。 |
| `FrameRates` | `Standard`、`Fps60`、`Fps30`、`Fps20`，控制滚动更新频率。 |
| `MousePressEventDelay` | 鼠标按下延迟，单位秒。 |
| `DragStartDistance` | 开始拖动所需距离，单位米。 |
| `DragVelocitySmoothingFactor` | 速度平滑系数。 |
| `AxisLockThreshold` | 轴锁定阈值。 |
| `ScrollingCurve` | 滚动曲线，值类型为 `QEasingCurve`。 |
| `DecelerationFactor` | 减速强度。 |
| `MinimumVelocity` / `MaximumVelocity` | 最小/最大滚动速度，单位米/秒。 |
| `SnapPositionRatio` / `SnapTime` | 吸附位置选择和吸附耗时。 |
| `HorizontalOvershootPolicy` / `VerticalOvershootPolicy` | 分轴控制 overshoot。 |
| `FrameRate` | 设置动画更新帧率。 |
