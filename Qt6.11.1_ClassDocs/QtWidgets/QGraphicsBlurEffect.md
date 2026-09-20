# QGraphicsBlurEffect

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsBlurEffect`

## 1. 先建立直觉

`QGraphicsBlurEffect` 给 widget 或 graphics item 的绘制结果加模糊。它常用于弱化背景、表现失焦、拖拽中的临时状态、动画过渡或不可用区域。

模糊是一种昂贵效果。它需要读取源内容并计算周围像素，半径越大、区域越大、动画越频繁，成本越明显。

## 2. 类说明

`QGraphicsBlurEffect` 继承自 `QGraphicsEffect`。核心属性是 `blurRadius` 和 `blurHints`。半径决定模糊范围，hint 告诉 Qt 优先性能、质量，或是否面向动画优化。

它改变的是视觉结果，不改变目标对象的真实输入区域。被模糊的按钮仍然按原本几何接收事件，除非你另外禁用目标。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsBlurEffect(QObject *)` | 创建模糊效果。 |
| `setBlurRadius(qreal)` / `blurRadius()` | 设置或读取模糊半径。 |
| `setBlurHints(BlurHints)` / `blurHints()` | 设置或读取质量/性能提示。 |
| `PerformanceHint` | 优先性能，适合实时变化或弱设备。 |
| `QualityHint` | 优先质量，适合静态或少量元素。 |
| `AnimationHint` | 告诉 Qt 该效果可能被动画驱动。 |
| `boundingRectFor(QRectF)` | 返回模糊后需要的扩展边界。 |
| `blurRadiusChanged(qreal)` | 半径变化时发出。 |
| `blurHintsChanged(BlurHints)` | hint 变化时发出。 |

## 4. 关键用法

```cpp
auto *blur = new QGraphicsBlurEffect(panel);
blur->setBlurRadius(8);
blur->setBlurHints(QGraphicsBlurEffect::QualityHint);
panel->setGraphicsEffect(blur);
```

动画模糊：

```cpp
auto *anim = new QPropertyAnimation(blur, "blurRadius", blur);
anim->setStartValue(0.0);
anim->setEndValue(12.0);
anim->setDuration(180);
anim->start(QAbstractAnimation::DeleteWhenStopped);
```

## 5. 使用场景

适合模态背景弱化、失焦预览、拖拽中的 ghost、错误状态震动后的淡化、图片或节点选中前后的过渡。

不适合大面积实时背景模糊、列表每行模糊、复杂主界面长期模糊。那通常会让 Widgets 应用明显变慢。

## 6. 常见坑与经验

半径不是越大越高级。桌面工具里小半径弱化通常比大半径糊成一片更清楚。

模糊会扩大绘制边界。边缘被裁掉时，多半是效果边界或父容器裁剪问题。

视觉上“禁用”一个控件时，不要只模糊。还应设置 disabled 或拦截交互，否则用户仍可点击。
