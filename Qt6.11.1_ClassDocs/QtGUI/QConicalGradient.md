# QConicalGradient

> Qt 6.11.1 · Qt GUI · 来自 `QConicalGradient`

## 1. 先建立直觉

`QConicalGradient` 围绕一个中心按角度插值颜色。它像一张铺在圆盘上的色轮：从起始 angle 对应的方向开始，沿角度绕一整圈回到起点。

它适合颜色选择器、环形仪表、方向盘、极坐标图、角度刻度和旋转纹理。与线性、径向渐变不同，圆锥渐变天然是周期性的；因此 stop 0 和 stop 1 的颜色是否连续，直接决定圆周接缝是否明显。

## 2. 类说明

`QConicalGradient` 继承自 `QGradient`。颜色 stops、坐标模式等共享配置来自父类；本类只定义中心和起始角度。

类说明只用于表明这些 API 来自 `QConicalGradient`：渐变本身不裁剪为圆形，画成圆盘、圆环或任意路径由 `QPainter` 的填充形状决定。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QConicalGradient()` | 构造中心为 `(0,0)`、起始角为 0 度的圆锥渐变。 |
| `QConicalGradient(center, angle)` | 用中心点和起始角构造渐变。 |
| `QConicalGradient(cx, cy, angle)` | 用数值坐标构造渐变。 |
| `center() const` | 返回圆锥渐变中心。 |
| `setCenter(point)` / `setCenter(x, y)` | 设置渐变中心。 |
| `angle() const` | 返回起始角度。 |
| `setAngle(angle)` | 设置起始角度。 |
| `setColorAt()` / `setStops()` | 来自父类，定义绕圆周的色带。 |
| `setCoordinateMode()` | 来自父类，定义中心和角度参数使用哪套坐标。 |

## 4. 关键用法

### 构造连续色轮

```cpp
QConicalGradient wheel(QPointF(width() / 2.0, height() / 2.0), 0);
wheel.setStops({
    {0.00, Qt::red},
    {0.16, Qt::yellow},
    {0.33, Qt::green},
    {0.50, Qt::cyan},
    {0.66, Qt::blue},
    {0.83, Qt::magenta},
    {1.00, Qt::red}
});

painter.setBrush(wheel);
painter.setPen(Qt::NoPen);
painter.drawEllipse(rect());
```

stop 0 和 1 都是 red，使圆周闭合时没有突兀色缝。色轮只表达 hue，通常还需额外叠加径向白色/透明或黑色遮罩表现饱和度与明度。

### 用 angle 旋转色带

```cpp
wheel.setAngle(m_rotationDegrees);
```

改变 angle 会整体旋转颜色起点。它适合仪表盘主题切换、方向高亮、扇区动画；比逐个重算所有 stop 更直接。

### 渐变中心和绘制形状是两回事

```cpp
painter.fillPath(customRingPath, wheel);
```

圆锥渐变可填充任意 path。即使形状是星形、圆环或扇形，颜色仍按相对于 center 的角度分布。

## 5. 使用场景

`QConicalGradient` 适合 HSV 色轮、圆形调色板、角度仪表、旋钮、环形状态图、极坐标可视化、雷达扇区、方向导航和旋转视觉效果。

它也可用于圆形 loading 或装饰色带，但功能性 UI 中应保证文本与关键状态不只依赖颜色区分。

## 6. 常见坑与经验

不要遗漏首尾颜色连续性。0 与 1 的 stop 不协调时，会在起始 angle 形成明显接缝。

不要期待 `RepeatSpread` / `ReflectSpread` 像线性渐变一样改变圆锥渐变外部区域。圆锥渐变按完整角度周期工作，核心是环形 stop 配置。

不要误以为渐变自身绘制圆。它只是颜色源，最终填充轮廓由你调用 `drawEllipse()`、`drawPath()` 或 `fillRect()` 决定。

不要把 angle 与数学坐标系方向想当然对应。屏幕坐标 y 轴向下，实际视觉方向应在目标平台和绘制上下文中验证。

不要在色轮上只靠 hue 表示状态。色觉差异用户仍需要文字、形状或位置等冗余信息。

## 7. 知识点覆盖

学习 `QConicalGradient` 应覆盖角度插值、中心与起始角、色轮闭合、首尾 stop、圆环与路径填充、旋转色带、HSV 调色器、屏幕坐标方向和无障碍色彩设计。
