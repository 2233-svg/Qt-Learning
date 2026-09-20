# QBrush

> Qt 6.11.1 · Qt GUI · 来自 `QBrush`

## 1. 先建立直觉

`QBrush` 描述如何填充形状内部。它可以是纯色、Qt 内置图案、纹理图像或渐变；`QPen` 则描述轮廓线。一个矩形能有蓝色填充和白色边框，前者来自 brush，后者来自 pen。

理解 `QBrush` 的关键是看 style。`SolidPattern` 时 color 有效；`TexturePattern` 时纹理主导，color 通常只对 1-bit `QBitmap` 有影响；渐变样式时真正颜色来自 gradient stops，调用 `setColor()` 不会改变渐变。

## 2. 类说明

`QBrush` 是值类型，常通过 `QPainter::setBrush()`、`fillRect()`、`fillPath()` 或作为 `QPen` 的 stroke brush 使用。它可以携带自己的 `QTransform`，该变换会与 painter transform 共同决定纹理或渐变的映射。

类说明只用于表明这些 API 来自 `QBrush`：颜色值由 `QColor` 表达，渐变由 `QGradient` 子类表达，线条轮廓由 `QPen` 表达。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QBrush()` | 构造 `NoBrush`，不会填充形状。 |
| `QBrush(color, style)` | 构造纯色或内置 pattern 画刷。 |
| `QBrush(gradient)` | 用线性、径向或圆锥渐变构造画刷。 |
| `QBrush(pixmap)` / `QBrush(image)` | 用纹理图像构造画刷。 |
| `style() const` / `setStyle()` | 查询或设置填充样式。 |
| `color() const` / `setColor()` | 查询或设置颜色；对渐变和普通纹理不一定生效。 |
| `gradient() const` | 返回渐变描述；非渐变画刷时为空。 |
| `texture()` / `textureImage()` | 返回纹理 pixmap 或 image；非纹理画刷时为空。 |
| `setTexture(pixmap)` | 设置 pixmap 纹理并切换到 TexturePattern。 |
| `setTextureImage(image)` | 设置 image 纹理并切换到 TexturePattern。 |
| `transform()` / `setTransform()` | 查询或设置画刷局部变换。 |
| `isOpaque()` | 判断画刷是否完全不透明，可辅助选择优化路径。 |
| `swap(other)` | 高效交换画刷。 |
| `operator==` / `operator!=` | 比较画刷样式、颜色、纹理/渐变与变换。 |

## 4. 关键用法

### 填充和描边明确分工

```cpp
painter.setBrush(QColor("#2563eb"));
painter.setPen(QPen(QColor("#1d4ed8"), 2));
painter.drawRoundedRect(rect, 6, 6);
```

`setBrush()` 不会影响边框，`setPen()` 不会影响内部填充。自定义控件里遗漏 `Qt::NoPen` 或 `Qt::NoBrush` 是重复描边/填充的常见原因。

### 用渐变画刷填充形状

```cpp
QLinearGradient gradient(0, 0, 0, 1);
gradient.setCoordinateMode(QGradient::ObjectMode);
gradient.setColorAt(0, QColor("#60a5fa"));
gradient.setColorAt(1, QColor("#1d4ed8"));

painter.setBrush(gradient);
painter.setPen(Qt::NoPen);
painter.drawRoundedRect(rect, 8, 8);
```

渐变画刷的 `color()` 不是渐变 stop 的代替品。修改颜色时应改 gradient，而不是对 brush 调 `setColor()`。

### 纹理变换控制平铺原点与缩放

```cpp
QBrush gridBrush(gridPixmap);
QTransform transform;
transform.translate(-scrollOffset.x(), -scrollOffset.y());
gridBrush.setTransform(transform);

painter.fillRect(viewportRect, gridBrush);
```

画刷 transform 很适合让网格、棋盘格、纸张纹理随内容滚动或固定在视口。不要通过每次裁剪/重建大纹理来模拟简单平移。

### 1-bit bitmap 才受 brush color 着色

对 `QBitmap` 纹理，brush color 可以改变前景颜色；对普通彩色 `QPixmap` / `QImage` 纹理，像素本身颜色主导，`setColor()` 不会为它整体染色。

## 5. 使用场景

`QBrush` 适合控件背景、形状填充、图表区域、选区高亮、纹理地面、棋盘背景、图片遮罩、渐变按钮、数据热区和 `QPen` 的渐变描边。

`NoBrush` 适合只画轮廓，`SolidPattern` 适合大多数普通填充，`TexturePattern` 适合重复材料感，渐变适合方向或中心变化明显的视觉过渡。

## 6. 常见坑与经验

不要把 `QBrush()` 当成默认黑色实心填充。默认是 `Qt::NoBrush`，不会填充任何内容。

不要在渐变或彩色纹理画刷上期待 `setColor()` 改变实际画面。它只对特定样式有意义。

不要忽略 brush transform 与 painter transform 叠加。纹理“跑位”时，要同时检查滚动偏移、painter transform 和 brush transform。

不要为大面积绘制使用带 alpha 的复杂纹理却期望 `isOpaque()` 为真。透明内容会影响合成成本与缓存策略。

不要在后台线程操作正在用于 GUI 绘制的 `QPixmap` 纹理。后台准备纹理时优先使用 `QImage`，回 GUI 线程后再转换。

## 7. 知识点覆盖

学习 `QBrush` 应覆盖填充与描边分工、NoBrush、纯色、图案、纹理、渐变、`QBitmap` 着色、画刷变换、透明性、绘制缓存和 `QPainter` 状态管理。
