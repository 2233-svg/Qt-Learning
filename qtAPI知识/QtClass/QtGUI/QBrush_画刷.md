# QBrush：定义 QPainter 如何填充图形内部

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QBrush>`  
> 模块：Qt GUI，链接 `Qt6::Gui`  
> 类型：可复制的值类型

## 它解决什么问题

`QPen` 决定图形边缘怎么画，`QBrush` 决定封闭图形内部怎么填。它可以表示纯色、Qt 内置图案、位图纹理或渐变，并把这份填充描述交给 `QPainter`、`QPalette`、`QGraphicsItem` 等绘制 API。

它不是一次绘制操作，也不直接拥有画布。`QBrush` 只是可复用的填充参数，同一个对象可被多个画家或绘制项复制使用。

```cpp
QPainter painter(this);
painter.setPen(Qt::NoPen);
painter.setBrush(QColor("#2a9d8f"));
painter.drawRoundedRect(rect().adjusted(8, 8, -8, -8), 6, 6);
```

默认构造的画刷是黑色 `Qt::NoBrush`，即**不填充**。不要把默认构造当作黑色实心填充；若需要纯黑应显式使用 `Qt::black` 或 `Qt::SolidPattern`。

## 填充源的四种模型

### 纯色和预定义图案

`QBrush(QColor, Qt::BrushStyle)` 组合颜色与 `Qt::SolidPattern`、`Dense*Pattern`、`HorPattern` 等样式。`Qt::NoBrush` 则表示不填充。

### 渐变

用 `QLinearGradient`、`QRadialGradient` 或 `QConicalGradient` 构造。画刷样式会自动变成相应的 GradientPattern，渐变色标决定实际颜色。

```cpp
QLinearGradient gradient(0, 0, 0, height());
gradient.setColorAt(0.0, QColor("#4cc9f0"));
gradient.setColorAt(1.0, QColor("#4361ee"));

painter.setBrush(QBrush(gradient));
painter.drawRect(rect());
```

### `QPixmap` 或 `QBitmap` 纹理

以 `QPixmap` 或 `QBitmap` 作为重复纹理时，样式为 `Qt::TexturePattern`。普通彩色 pixmap 自带颜色，画刷的 `color` 不会给它重新着色；若纹理是 1-bit 的 `QBitmap`，画刷颜色才会决定前景色。

### `QImage` 纹理

`setTextureImage()` 也会设置 `TexturePattern`，但单色 `QImage` 与 `QBitmap` 不同：画刷颜色不影响它。若需要给单色图案换色，应转成 `QBitmap` 再调用 `setTexture()`，或改动 `QImage` 的颜色表。

## `setColor()` 并不总会改变画面

`setColor()` 只修改画刷保存的颜色。它的可视效果取决于当前填充源：

- 纯色和内置图案：会改变绘制颜色。
- 渐变：不会改变，因为颜色由渐变色标决定。
- 普通 `QPixmap` 纹理：不会改变，因为纹理自带颜色。
- `QBitmap` 纹理：会改变前景颜色。

这是一类很隐蔽的错误：代码看到 `brush.setColor(Qt::red)` 成功执行，却仍然画出原渐变或原纹理，并不是 QPainter 没刷新。

## 坐标与透明度

`setTransform()` 设置画刷自己的局部变换，例如平移纹理原点、缩放棋盘格、旋转图案。它会与 `QPainter` 的世界变换共同影响最终效果，因此调试纹理错位时，应同时检查画家变换和画刷变换。

`isOpaque()` 用于判断填充是否完全不透明。Qt 的判断包括颜色 alpha 为 255、纹理没有 alpha 且不是 `QBitmap`、渐变所有颜色均不透明，或扩展径向渐变等条件。它是优化提示，不应代替业务对颜色或像素内容的精确判断。

## 值语义、共享和比较

`QBrush` 是值类型，允许复制、赋值和放入容器；拷贝成本通常很低。修改副本会触发必要的数据分离，不会意外改动已复制出去的画刷。

`swap()` 高效地交换两个画刷。相等比较会比较样式、颜色、变换，以及当前样式所需的纹理或渐变，不是只比较 `color()`。

自 Qt 6.9 起，可以直接给画刷赋 `QColor`、`Qt::GlobalColor` 或 `Qt::BrushStyle`：

```cpp
QBrush brush;
brush = QColor("#f72585");   // 变为该颜色的实心画刷
brush = Qt::Dense4Pattern;   // 变为黑色的该图案画刷
```

这类赋值会重设画刷模型，不能把它视为单纯更新原纹理或渐变的一个字段。

## 常见误区

- 默认 `QBrush()` 不填充，而不是黑色实心填充。
- 对渐变或普通彩色纹理调用 `setColor()` 后，期待颜色变化。
- 混淆 `QBitmap` 与单色 `QImage` 的着色行为。
- 忘记画刷自身 transform，导致纹理在不同绘制项上无法对齐。
- 只比较 `color()` 判断两个画刷是否相同，遗漏样式、纹理、渐变与变换。

## API 速查表

| API | 含义 | 重点边界 |
| --- | --- | --- |
| `QBrush()` | 创建黑色 `Qt::NoBrush`。 | 不填充任何区域。 |
| `QBrush(Qt::BrushStyle style)` | 创建黑色的指定样式画刷。 | `NoBrush` 不填充，图案和实心样式才会绘制。 |
| `QBrush(const QColor &color, Qt::BrushStyle style = Qt::SolidPattern)` | 创建颜色和样式组合的画刷。 | 对纯色和预定义图案最常用。 |
| `QBrush(Qt::GlobalColor color, Qt::BrushStyle style = Qt::SolidPattern)` | 以 Qt 全局色创建画刷。 | 与 `QColor` 重载语义相同。 |
| `QBrush(const QGradient &gradient)` | 从渐变创建画刷。 | 自动使用对应的渐变样式。 |
| `QBrush(const QPixmap &pixmap)` | 从 pixmap 创建纹理画刷。 | 样式设为 `TexturePattern`；彩色纹理不受画刷颜色影响。 |
| `QBrush(const QImage &image)` | 从 image 创建纹理画刷。 | 样式设为 `TexturePattern`；单色 image 也不会被 `setColor()` 着色。 |
| `QBrush(const QColor &color, const QPixmap &pixmap)` | 创建带颜色与 pixmap 纹理的画刷。 | `color` 只会影响 1-bit `QBitmap` 纹理。 |
| `QBrush(Qt::GlobalColor color, const QPixmap &pixmap)` | 上述纹理构造的全局色重载。 | 对普通彩色 pixmap，颜色没有可视效果。 |
| `QBrush(const QBrush &other)` / `operator=(const QBrush &)` | 复制或复制赋值画刷。 | 值语义，复制后可独立修改。 |
| `operator=(QBrush &&other)` | 移动赋值画刷。 | `noexcept`，适合容器内部移动。 |
| `operator=(QColor)` / `operator=(Qt::GlobalColor)` | 设为指定颜色的实心画刷。 | Qt 6.9 起可用，会重置为 SolidPattern。 |
| `operator=(Qt::BrushStyle)` | 设为黑色的指定样式画刷。 | Qt 6.9 起可用，会替换原纹理或渐变模型。 |
| `Qt::BrushStyle style() const` | 返回当前填充样式。 | 用于区分无填充、图案、纹理和渐变。 |
| `void setStyle(Qt::BrushStyle style)` | 修改填充样式。 | 改为 `NoBrush` 后不再填充。 |
| `const QColor &color() const` | 返回画刷保存的颜色。 | 不代表渐变或彩色纹理的实际每个像素颜色。 |
| `void setColor(const QColor &color)` / `void setColor(Qt::GlobalColor color)` | 设置画刷颜色。 | 对渐变和普通纹理无可视效果，`QBitmap` 纹理例外。 |
| `const QGradient *gradient() const` | 返回关联渐变。 | 非渐变画刷通常无可用渐变；不要修改或长期保存返回指针。 |
| `void setTexture(const QPixmap &pixmap)` | 设置 pixmap 纹理。 | 自动设为 `TexturePattern`；只有单色 pixmap 受画刷颜色影响。 |
| `QPixmap texture() const` | 返回自定义 pixmap 纹理。 | 未设置时返回 null pixmap。 |
| `void setTextureImage(const QImage &image)` | 设置 image 纹理。 | 自动设为 `TexturePattern`；单色 image 的颜色不受画刷颜色影响。 |
| `QImage textureImage() const` | 返回纹理图像。 | pixmap 纹理会按需转换为 image。 |
| `void setTransform(const QTransform &matrix)` | 设置画刷局部变换。 | 与 painter 的世界变换共同决定纹理和渐变坐标。 |
| `QTransform transform() const` | 返回画刷局部变换。 | 调试图案错位时与 painter transform 一并检查。 |
| `bool isOpaque() const` | 判断画刷是否完全不透明。 | 是优化性质的判断，受 alpha、纹理和渐变条件影响。 |
| `void swap(QBrush &other)` | 高效交换两个画刷。 | `noexcept`，不会失败。 |
| `operator QVariant() const` | 将画刷包装为 `QVariant`。 | 适合 QVariant 传递与属性存储，不等于持久化格式。 |
| `bool operator==(const QBrush &other) const` | 比较两个画刷是否相等。 | 比较样式、颜色、变换及相应纹理或渐变。 |
| `bool operator!=(const QBrush &other) const` | 比较两个画刷是否不同。 | 是相等比较的反面，不只比较颜色。 |
| `QDataStream &operator<<(QDataStream &, const QBrush &)` | 将画刷写入数据流。 | 序列化前后应保持一致的数据流版本。 |
| `QDataStream &operator>>(QDataStream &, QBrush &)` | 从数据流读取画刷。 | 输入数据需来自兼容的 Qt 数据流格式。 |
