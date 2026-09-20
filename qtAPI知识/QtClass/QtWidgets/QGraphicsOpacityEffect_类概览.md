# QGraphicsOpacityEffect：用效果层控制整体透明度

> Qt 6.11.1 · `#include <QGraphicsOpacityEffect>` · 模块：`Qt6::Widgets` · 继承：`QGraphicsEffect`

`QGraphicsOpacityEffect` 让 widget 或 graphics item 以指定透明度绘制，并可通过 mask 让透明度在不同区域变化。它常用于淡入淡出、临时禁用感、悬浮层或视觉过渡。

## 使用场景

安装到目标对象后，用 `setOpacity()` 控制整体透明度，范围应在 0.0 到 1.0：0 完全透明，1 完全不透明。默认透明度是 0.7。需要渐变透明时设置 `opacityMask()`，例如用线性渐变 brush 做上下淡出。

对于 `QGraphicsItem`，如果只是简单整体透明度，也可以考虑 item 自身的 `setOpacity()`；效果对象更适合 widget 或需要 mask 的场景。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QGraphicsOpacityEffect(QObject *parent = nullptr)` | 构造透明度效果。 |
| `~QGraphicsOpacityEffect()` | 销毁效果。 |
| `opacity() const` | 返回整体透明度，建议范围 0.0 到 1.0。 |
| `setOpacity(qreal opacity)` | 设置整体透明度；默认 0.7。 |
| `opacityMask() const` | 返回透明度遮罩 brush；默认无 mask。 |
| `setOpacityMask(const QBrush &mask)` | 设置局部透明度遮罩。 |
| `opacityChanged(qreal)` | 透明度变化信号。 |
| `opacityMaskChanged(const QBrush &)` | mask 变化信号。 |
| `draw(QPainter *)` | 重写的绘制实现；普通使用不直接调用。 |
| 性能边界 | 效果层通常需要额外离屏处理，频繁动画时应测性能。 |
