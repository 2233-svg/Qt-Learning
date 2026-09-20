# QGraphicsEffect

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsEffect`

## 1. 先建立直觉

`QGraphicsEffect` 是对 widget 或 graphics item 的绘制结果做后处理的基类。阴影、模糊、着色、透明度都属于这类效果：先把源对象画出来，再对这张结果图做加工。

它不是替代 `paint()` 的绘图接口，也不改变 item 的真实几何。效果可能扩大视觉边界，例如阴影和模糊会超出原对象区域，所以要通过 `boundingRectFor()` 告诉 Qt 需要多大的绘制范围。

## 2. 类说明

`QGraphicsEffect` 继承自 `QObject`。可以通过 `QWidget::setGraphicsEffect()` 或 `QGraphicsItem::setGraphicsEffect()` 应用到目标上。内置子类包括模糊、着色、阴影和透明度效果。

自定义效果通常重写 `draw(QPainter *)`，在其中取得源内容并绘制处理后的结果。效果易用，但有额外渲染成本，尤其在大控件、频繁动画和低端设备上要谨慎。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `setEnabled(bool)` / `isEnabled()` | 启用或禁用效果。禁用时源对象正常绘制。 |
| `boundingRect()` | 返回当前效果后的边界。 |
| `boundingRectFor(const QRectF &)` | 根据源边界计算效果需要的边界；自定义扩散效果要重写。 |
| `update()` | 请求重新绘制效果。 |
| `enabledChanged(bool)` | 启用状态变化时发出。 |
| `draw(QPainter *)` | 子类重写，执行实际效果绘制。 |
| `drawSource(QPainter *)` | 在自定义效果中绘制原始源内容。 |
| `sourcePixmap()` | 获取源内容快照，供像素级处理使用。 |
| `sourceBoundingRect()` | 获取源对象边界。 |
| `updateBoundingRect()` | 效果边界变化时通知框架。 |
| `sourceChanged(ChangeFlags)` | 源对象附加、分离、边界或内容变化时回调。 |
| `PixmapPadMode` | 控制 source pixmap 是否额外填充透明边界。 |

## 4. 关键用法

```cpp
auto *shadow = new QGraphicsDropShadowEffect(button);
shadow->setBlurRadius(18);
shadow->setOffset(0, 4);
button->setGraphicsEffect(shadow);
```

自定义效果的大致形态：

```cpp
void MyEffect::draw(QPainter *painter)
{
    QPoint offset;
    QPixmap pix = sourcePixmap(Qt::LogicalCoordinates, &offset);
    process(pix);
    painter->drawPixmap(offset, pix);
}
```

## 5. 使用场景

适合少量重点元素的视觉强调：选中 glow、弹窗阴影、禁用态淡化、背景模糊、临时高亮。

不适合大量列表项逐个加复杂效果。那类界面更应该用 delegate 自绘、缓存或静态资源。

## 6. 常见坑与经验

效果会增加离屏绘制成本。动画模糊和大面积阴影尤其容易拖慢界面。

视觉边界变化要反映到 `boundingRectFor()`，否则阴影/模糊边缘可能被裁掉。

一个对象通常只能设置一个 graphics effect。需要叠加多个效果时，往往要自定义一个组合效果或调整绘制方案。
