# QGraphicsScale

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsScale`

## 1. 先建立直觉

`QGraphicsScale` 是一个可放进 item 变换链的缩放对象。它把 x/y/z 缩放和缩放原点做成属性，方便用动画框架平滑驱动。

简单缩放一个 item 可以直接 `item->setScale()`；当你需要分别动画 x/y、指定三维原点、和旋转等变换组合时，`QGraphicsScale` 更合适。

## 2. 类说明

`QGraphicsScale` 继承自 `QGraphicsTransform`。它通过 `applyTo()` 把缩放累积到矩阵中。`origin` 是缩放中心，`xScale`、`yScale`、`zScale` 分别控制三个方向。

在 2D Graphics View 中最常用的是 x/y 缩放；z 轴更多用于和 3D 风格变换链配合。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsScale(QObject *)` | 创建缩放变换对象。 |
| `setOrigin(const QVector3D &)` / `origin()` | 设置或读取缩放中心。 |
| `setXScale(qreal)` / `xScale()` | 设置或读取 x 方向缩放。 |
| `setYScale(qreal)` / `yScale()` | 设置或读取 y 方向缩放。 |
| `setZScale(qreal)` / `zScale()` | 设置或读取 z 方向缩放。 |
| `applyTo(QMatrix4x4 *)` | 把缩放应用到矩阵。 |
| `originChanged()` | 缩放中心变化时发出。 |
| `xScaleChanged/yScaleChanged/zScaleChanged` | 对应缩放值变化时发出。 |

## 4. 关键用法

```cpp
auto *scale = new QGraphicsScale(item);
scale->setOrigin(QVector3D(50, 25, 0));
item->setTransformations({ scale });

auto *anim = new QPropertyAnimation(scale, "xScale", item);
anim->setStartValue(1.0);
anim->setEndValue(1.25);
anim->start(QAbstractAnimation::DeleteWhenStopped);
```

同时动画 x/y：

```cpp
scale->setXScale(factor);
scale->setYScale(factor);
```

## 5. 使用场景

适合选中放大、节点 hover 动画、图片预览缩放、图形对象弹入弹出、编辑器里的非等比缩放控制。

如果只是固定设置一个统一比例，`QGraphicsItem::setScale()` 更少代码。

## 6. 常见坑与经验

缩放原点决定视觉感受。按钮从中心放大和从左上角放大，用户感觉完全不同。

负缩放会镜像 item，可能导致文字、箭头和命中区域看起来反直觉。除非确实要镜像，否则避免不小心传入负值。

和 item 自身 scale 混用时，最终比例是组合结果。调试动画时先把一层归零或固定，定位会容易很多。
