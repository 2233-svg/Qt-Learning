# QLinearGradient

> Qt 6.11.1 · Qt GUI · 来自 `QLinearGradient`

## 1. 先建立直觉

`QLinearGradient` 沿一条从 start 到 final stop 的直线插值颜色。渐变线垂直方向上的点拥有相同插值进度，因此它适合顶部到底部、左到右、斜向扫光和条形色带。

start 和 final stop 不是“填充矩形的两个角”这一固定概念，而是渐变参数轴的两个端点。填充区域可以比它大得多，超出端点后的颜色由 `QGradient::spread()` 决定。

## 2. 类说明

`QLinearGradient` 继承自 `QGradient`。颜色 stop、spread、coordinate mode 来自父类；本类只定义渐变轴的 start 和 final stop。

类说明只用于表明这些 API 来自 `QLinearGradient`：要设置颜色调用 `setColorAt()` / `setStops()`，要设置相对坐标行为调用 `setCoordinateMode()`，要将渐变用于绘制则把它作为 `QBrush` 或传给 `QPainter`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QLinearGradient()` | 构造默认从 `(0,0)` 到 `(1,1)` 的线性渐变。 |
| `QLinearGradient(start, finalStop)` | 用两个浮点点构造渐变轴。 |
| `QLinearGradient(x1, y1, x2, y2)` | 用四个坐标构造渐变轴。 |
| `start() const` | 返回渐变轴起点。 |
| `setStart(point)` / `setStart(x, y)` | 设置渐变轴起点。 |
| `finalStop() const` | 返回渐变轴终点。 |
| `setFinalStop(point)` / `setFinalStop(x, y)` | 设置渐变轴终点。 |
| `setColorAt()` / `setStops()` | 来自父类，定义颜色节点。 |
| `setCoordinateMode()` | 来自父类，定义坐标相对于对象还是逻辑空间。 |
| `setSpread()` | 来自父类，定义超出端点范围时的填充。 |

## 4. 关键用法

### 用 ObjectMode 做自适应垂直背景

```cpp
QLinearGradient gradient(0, 0, 0, 1);
gradient.setCoordinateMode(QGradient::ObjectMode);
gradient.setColorAt(0.0, QColor("#ffffff"));
gradient.setColorAt(1.0, QColor("#e5edf8"));

painter.fillRect(rect(), gradient);
```

在 ObjectMode 中，`0` 到 `1` 是对象边界比例。控件无论多高，渐变都会从顶部完整过渡到底部。

### 用 LogicalMode 绑定到场景坐标

```cpp
QLinearGradient horizon(0, 0, 1200, 0);
horizon.setCoordinateMode(QGradient::LogicalMode);
```

逻辑坐标模式适合多个图元共享同一条世界坐标色带，例如地图高度着色、时间轴背景或大画布光照。此时它不应随着每个 item 的边界重置。

### 把渐变轴与形状方向对齐

```cpp
QLineF axis(startPoint, endPoint);
QLinearGradient gradient(axis.p1(), axis.p2());
gradient.setColorAt(0, leftColor);
gradient.setColorAt(1, rightColor);

painter.fillPath(shape, gradient);
```

渐变轴未必与形状 bounding rect 对齐。对于箭头、连接线、斜切按钮等图形，跟随真实方向会更自然。

## 5. 使用场景

`QLinearGradient` 适合面板背景、进度条、按钮填充、柱状图色带、反射高光、阴影淡出、地图标尺、时间轴和沿路径方向的视觉引导。

它也常作为遮罩使用，例如从完全透明到不透明的 alpha 渐变，以实现图片淡入、滚动边缘淡出或文字截断提示。

## 6. 常见坑与经验

不要默认 `(0,0)` 到 `(1,1)` 会覆盖整个控件。只有 ObjectMode / StretchToDeviceMode 下才是比例坐标；默认 LogicalMode 里它只是逻辑空间的一小段。

不要让 start 和 final stop 完全重合。没有长度的渐变轴没有清晰插值方向，结果依赖实现且没有实用意义。

不要在动态动画里每帧反复新建 `QBrush`、渐变和 stop 列表。可更新已有 gradient 或缓存不变部分。

不要用 linear gradient 模拟径向高光。几何不匹配会让视觉显得平；需要中心扩散时应使用 `QRadialGradient`。

不要忽略 spread。填充范围超过渐变轴时，默认 PadSpread 会把边缘颜色延长，很多“颜色为什么铺满后半段”的问题都源于此。

## 7. 知识点覆盖

学习 `QLinearGradient` 应覆盖渐变轴、start/final stop、ObjectMode、LogicalMode、方向性填充、超出范围扩展、alpha 渐变、场景共享坐标和高频绘制缓存。
