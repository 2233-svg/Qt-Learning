# QGraphicsItemAnimation

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsItemAnimation`

## 1. 先建立直觉

`QGraphicsItemAnimation` 是早期 Graphics View 用来驱动 item 变换的动画类。它把时间轴上的步骤映射到 item 的位置、旋转、缩放、剪切和平移。

现代 Qt 代码中，很多场景会优先使用 `QPropertyAnimation`、`QGraphicsObject` 属性或 `QVariantAnimation`。但读老项目、维护基于 `QTimeLine` 的场景动画时，仍会遇到它。

## 2. 类说明

`QGraphicsItemAnimation` 继承自 `QObject`。它绑定一个 `QGraphicsItem` 和一个 `QTimeLine`，按 0 到 1 的 step 值插值应用变换。

它不是通用动画框架，而是专门面向 `QGraphicsItem` 的变换表。你可以为不同 step 设置 pos、rotation、scale、shear、translation，然后时间线推进时应用。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `setItem(QGraphicsItem *)` / `item()` | 设置或读取被动画驱动的 item。 |
| `setTimeLine(QTimeLine *)` / `timeLine()` | 设置或读取时间线。 |
| `setPosAt(step, QPointF)` / `posAt(step)` | 设置或读取某个进度的位置。 |
| `setRotationAt(step, qreal)` / `rotationAt(step)` | 设置或读取某进度旋转角。 |
| `setScaleAt(step, sx, sy)` / `scaleAt(step)` | 设置或读取某进度缩放。 |
| `setShearAt(step, sh, sv)` / `shearAt(step)` | 设置或读取某进度剪切。 |
| `setTranslationAt(step, dx, dy)` / `translationAt(step)` | 设置或读取某进度平移。 |
| `setStep(qreal)` | 手动应用某个进度的动画状态。 |
| `clear()` | 清除所有记录的动画步骤。 |
| `beforeAnimationStep(qreal)` / `afterAnimationStep(qreal)` | 子类钩子，可在 step 应用前后插入逻辑。 |

## 4. 关键用法

```cpp
auto *timeline = new QTimeLine(500, this);
timeline->setFrameRange(0, 100);

auto *anim = new QGraphicsItemAnimation(this);
anim->setItem(item);
anim->setTimeLine(timeline);
anim->setPosAt(0.0, QPointF(0, 0));
anim->setPosAt(1.0, QPointF(200, 80));

timeline->start();
```

step 通常在 0.0 到 1.0 之间，表示动画进度。

## 5. 使用场景

适合维护旧的 Graphics View 动画、基于 `QTimeLine` 的场景演示、简单 item 变换序列。

新代码如果 item 继承 `QGraphicsObject`，通常用 `QPropertyAnimation` 更自然；如果 item 不是 QObject，可用 `QVariantAnimation` 手动更新。

## 6. 常见坑与经验

它主要动画变换，不适合驱动任意业务属性。复杂状态动画用现代动画框架更清楚。

绑定的 item 和 timeline 生命周期要明确。动画过程中删除 item 会让后续 step 无意义，甚至造成悬空访问风险。

多个变换来源叠加时要小心：item 自己的 transform、动画设置、父 item 变换会共同决定最终位置。
