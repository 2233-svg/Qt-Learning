# QGradient

> Qt 6.11.1 · Qt GUI · 来自 `QGradient`

## 1. 先建立直觉

`QGradient` 是线性、径向、圆锥渐变共享的配置基类。它不决定几何形状，那由 `QLinearGradient`、`QRadialGradient`、`QConicalGradient` 决定；它决定的是颜色如何沿渐变参数变化、超出渐变范围后怎样填充、坐标相对什么参考系解释。

渐变最容易出问题的地方通常不是 stops，而是坐标模式。相同的 `(0, 0)` 到 `(1, 1)`，在逻辑坐标中可能只是一像素范围，在 ObjectMode 中却会自动覆盖每个被绘制对象的边界。

## 2. 类说明

`QGradient` 是值类型，派生类可直接交给 `QBrush` 或 `QPainter` 使用。`QGradientStop` 是 `(位置, QColor)` 的一对值，`QGradientStops` 是这些 stop 的列表。

类说明只用于表明这些 API 来自 `QGradient`：渐变几何由具体子类维护，画刷变换与填充由 `QBrush` / `QPainter` 协作完成。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGradient(preset)` | 从预定义调色预设创建渐变，默认使用对象相对坐标。 |
| `setColorAt(position, color)` | 设置某个 0.0-1.0 stop 的颜色。 |
| `setStops(stops)` | 一次设置完整 stop 列表。 |
| `stops() const` | 读取当前 stop 列表。 |
| `setSpread(mode)` | 设置渐变范围外的填充策略。 |
| `spread() const` | 读取扩展填充策略。 |
| `setCoordinateMode(mode)` | 设置渐变坐标的参考系。 |
| `coordinateMode() const` | 读取坐标模式。 |
| `type() const` | 返回 Linear、Radial、Conical 或 NoGradient。 |
| `operator==` / `operator!=` | 比较渐变配置。 |

坐标模式：

| 枚举 | 适合什么 |
| --- | --- |
| `LogicalMode` | 默认模式，渐变参数使用当前 painter 逻辑坐标。 |
| `ObjectMode` | 参数 0-1 相对每个被绘制对象的边界，适合可伸缩组件背景。 |
| `StretchToDeviceMode` | 参数 0-1 相对整个 paint device，适合全窗口背景。 |
| `ObjectBoundingMode` | 旧兼容模式，新代码应优先用 `ObjectMode`。 |

扩展策略：

| 枚举 | 作用 |
| --- | --- |
| `PadSpread` | 超出范围后延续两端最近颜色。 |
| `RepeatSpread` | 反复重复 0-1 的渐变周期。 |
| `ReflectSpread` | 镜像往返重复渐变，边界颜色连续性更好。 |

## 4. 关键用法

### 显式定义 stops

```cpp
QLinearGradient gradient(0, 0, 0, 1);
gradient.setCoordinateMode(QGradient::ObjectMode);
gradient.setStops({
    {0.0, QColor("#2563eb")},
    {0.55, QColor("#3b82f6")},
    {1.0, QColor("#bfdbfe")}
});

painter.fillRect(rect(), gradient);
```

stop 位置应在 0.0 到 1.0 范围内，并按位置递增组织。使用 `setStops()` 比多次散落的 `setColorAt()` 更容易审查和复用主题配置。

### 组件背景常用 `ObjectMode`

```cpp
QLinearGradient background(0, 0, 1, 1);
background.setCoordinateMode(QGradient::ObjectMode);
```

同一个 gradient 填充不同尺寸卡片时，ObjectMode 会自动把 `(0,0)` 到 `(1,1)` 映射到各自边界。若仍使用 LogicalMode，控件 resize 后可能只显示渐变的一小段。

### 用 Repeat / Reflect 做规律纹理

```cpp
gradient.setSpread(QGradient::ReflectSpread);
```

Reflect 比 Repeat 在周期交界处更平滑，适合条纹、波纹、镜面色带。大面积、复杂 stop 的重复渐变仍可能增加绘制成本，应按需缓存。

### 预设适合原型，不应替代主题决策

`QGradient::Preset` 提供大量预定义配色，便于快速试验。正式 UI 更应明确颜色、对比度、文字可读性和无障碍要求；预设名称不能替代设计语义。

## 5. 使用场景

`QGradient` 适合背景填充、按钮状态、数据可视化色带、材质高光、图形编辑器、进度条、频谱、仪表盘、渐变遮罩和绘画工具。

线性渐变适合方向性过渡，径向渐变适合聚光与球面感，圆锥渐变适合色轮、角度刻度和环形可视化。共同的 stop、spread、坐标模式都在本类配置。

## 6. 常见坑与经验

不要误以为 stop 颜色会在感知均匀空间插值。常规绘制由 Qt 的颜色与渲染管线处理，专业色彩需求需验证实际结果。

不要在 `paintEvent()` 的每个像素或每个 item 都重新构造复杂 gradient。能缓存就缓存，尤其是静态背景和重复色带。

不要忽略 painter transform。LogicalMode 下，平移、缩放、旋转会一起影响渐变坐标。

不要滥用渐变预设。大面积高饱和渐变可能让数据、文字与控制元素难以辨认。

不要使用已废弃的 ObjectBoundingMode 写新代码，选择 `ObjectMode` 更清晰。

## 7. 知识点覆盖

学习 `QGradient` 应覆盖颜色 stops、位置归一化、坐标模式、逻辑坐标、对象边界坐标、设备坐标、Pad/Repeat/Reflect、渐变预设、画刷变换、绘制缓存和无障碍对比度。
