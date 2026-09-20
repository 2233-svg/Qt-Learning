# QGraphicsColorizeEffect：给源内容叠加统一色调

> Qt 6.11.1 · `#include <QGraphicsColorizeEffect>` · 模块：`Qt6::Widgets` · 继承：`QGraphicsEffect`

`QGraphicsColorizeEffect` 把 widget 或 graphics item 的绘制结果重新着色，形成统一 tint。它适合表达禁用态、选中态、警告态、夜间模式预览等“整体染色”效果。

## 使用场景

通过 `QWidget::setGraphicsEffect()` 或 `QGraphicsItem::setGraphicsEffect()` 安装到目标上。`color` 决定染色颜色，`strength` 决定染色强度。默认颜色是深蓝色 `QColor(0, 0, 192)`，默认强度是 1.0。

效果是在源内容绘制后再处理像素，通常比直接改 palette、style 或 item 绘制更重。大量 item 同时使用或频繁动画时要注意性能。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QGraphicsColorizeEffect(QObject *parent = nullptr)` | 构造染色效果对象。 |
| `~QGraphicsColorizeEffect()` | 销毁效果；目标不应继续使用已销毁效果。 |
| `color() const` | 返回当前染色颜色。 |
| `setColor(const QColor &)` | 设置染色颜色并触发重绘。 |
| `strength() const` | 返回染色强度。 |
| `setStrength(qreal)` | 设置强度；0.0 等于无效果，1.0 为完全染色。 |
| `colorChanged(const QColor &)` | 颜色变化信号。 |
| `strengthChanged(qreal)` | 强度变化信号。 |
| `draw(QPainter *)` | 重写的绘制实现；普通使用不直接调用。 |
| 性能边界 | 像素后处理效果，不适合大量频繁变化对象滥用。 |
