# QRadialGradient

> Qt 6.11.1 · Qt GUI · 来自 `QRadialGradient`

## 1. 先建立直觉

`QRadialGradient` 从焦点向外扩散到一个圆或两个圆之间。它适合聚光、球体高光、热力图、发光边缘、镜头暗角和柔和阴影。

简单径向渐变由 center、radius、focal point 组成：颜色沿从 focal point 出发、朝外围圆扩张的方向插值。扩展径向渐变还允许 center 与 focal 各自带半径，用来描述两个圆之间的过渡，适合更复杂的环形或偏心光学效果。

## 2. 类说明

`QRadialGradient` 继承自 `QGradient`。stop、spread、coordinate mode 来自父类；本类定义中心、焦点和半径几何。

类说明只用于表明这些 API 来自 `QRadialGradient`：颜色与坐标模式仍在父类设置，绘制时通过 `QBrush` / `QPainter` 应用。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QRadialGradient()` | 构造默认中心/焦点为 `(0,0)`、半径为 1 的渐变。 |
| `QRadialGradient(center, radius)` | 构造简单径向渐变，焦点默认在中心。 |
| `QRadialGradient(center, radius, focalPoint)` | 构造带偏移焦点的简单径向渐变。 |
| `QRadialGradient(center, centerRadius, focalPoint, focalRadius)` | 构造扩展径向渐变，定义两个圆之间的过渡。 |
| `center()` / `setCenter()` | 查询或设置外围圆中心。 |
| `radius()` / `setRadius()` | 查询或设置简单径向渐变的外围半径，等价于 center radius。 |
| `centerRadius()` / `setCenterRadius()` | 查询或设置中心圆半径。 |
| `focalPoint()` / `setFocalPoint()` | 查询或设置颜色扩散起点。 |
| `focalRadius()` / `setFocalRadius()` | 查询或设置焦点圆半径。 |
| `setColorAt()` / `setStops()` | 来自父类，定义由内向外的颜色节点。 |
| `setCoordinateMode()` / `setSpread()` | 来自父类，定义坐标模式和越界填充。 |

## 4. 关键用法

### 居中柔和高光

```cpp
QRadialGradient glow(QPointF(width() / 2.0, height() / 2.0),
                      qMax(width(), height()) / 2.0);
glow.setColorAt(0.0, QColor(255, 255, 255, 180));
glow.setColorAt(0.65, QColor(96, 165, 250, 80));
glow.setColorAt(1.0, QColor(37, 99, 235, 0));

painter.fillRect(rect(), glow);
```

中心 stop 不一定必须完全不透明；把 alpha 也做渐变能自然地叠加在已有背景上。

### 用焦点制造偏心光源

```cpp
QRadialGradient light(
    QPointF(width() * 0.5, height() * 0.5),
    width() * 0.7,
    QPointF(width() * 0.35, height() * 0.28));
```

center 决定外圈边界，focal point 决定颜色最集中处。让 focal 向左上偏移，就能模拟从左上方照来的光，而不是把整个亮区固定在正中心。

### 焦点超出半径会被约束

简单径向渐变里，若 focal point 在外围圆之外，Qt 会把它调整到圆边界附近。不要依赖这种隐式修正来实现特殊效果；需要精确几何时，先在业务代码中约束焦点或选择扩展径向渐变。

### ObjectMode 下用归一化几何

```cpp
QRadialGradient gradient(QPointF(0.5, 0.5), 0.7, QPointF(0.35, 0.3));
gradient.setCoordinateMode(QGradient::ObjectMode);
```

这样同一高光配置能覆盖不同尺寸对象。非正方形对象会把圆形按对象坐标映射成椭圆形视觉效果，这有时正是预期，有时则需要基于实际尺寸重新计算。

## 5. 使用场景

`QRadialGradient` 适合高光球体、圆形按钮、地图热点、热力图、光晕、暗角、进度环背景、仪表盘中心光效、图片遮罩和粒子效果。

扩展径向渐变在专业绘图和特效里更有价值：它可以表现两个偏移圆之间的色带，而不仅是中心到边缘的单圆扩散。

## 6. 常见坑与经验

不要把 focal point 当作外圆中心。它只是插值的焦点，外围几何仍由 center/radius 控制。

不要忘记 radius 与对象尺寸关系。LogicalMode 下固定半径在控件 resize 后不会自动增长；需要自适应时使用 ObjectMode 或在 resize 时重算。

不要在高频鼠标移动中重建巨大径向渐变并全窗口重绘。对于跟随光标的高光，限制脏区域或缓存背景。

不要用 radial gradient 实现精确物理光照。它是 2D 色带工具，能产生视觉暗示，但不包含真实光照模型。

不要忽略 alpha 混合底色。相同 radial gradient 叠在不同背景上，视觉结果会不同。

## 7. 知识点覆盖

学习 `QRadialGradient` 应覆盖中心、焦点、半径、扩展径向渐变、偏心高光、ObjectMode、透明 stop、边界约束、椭圆映射、光晕与热力图绘制。
