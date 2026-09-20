# QGraphicsTransform

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsTransform`

## 1. 先建立直觉

`QGraphicsTransform` 是 Graphics View 的变换组件基类。它不是直接画东西，而是把缩放、旋转这类变换作为 QObject 对象挂到 item 的 transformations 列表里。

相比直接 `setTransform()`，它更适合做属性动画：每个变换对象有自己的属性，可以被 `QPropertyAnimation` 驱动，也可以组合成有顺序的变换链。

## 2. 类说明

`QGraphicsTransform` 继承自 `QObject`。具体子类包括 `QGraphicsScale` 和 `QGraphicsRotation`。框架会调用 `applyTo(QMatrix4x4 *)`，把该变换累积到矩阵中。

如果你需要自定义变换，例如透视、倾斜或业务特定变换，可以继承它并实现 `applyTo()`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsTransform(QObject *)` | 创建变换对象。 |
| `applyTo(QMatrix4x4 *)` | 纯虚函数，把当前变换应用到矩阵。自定义子类必须实现。 |
| `QGraphicsScale` | 内置缩放变换。 |
| `QGraphicsRotation` | 内置旋转变换。 |
| `QGraphicsItem::setTransformations()` | 把多个变换对象应用到 item。 |
| `QGraphicsItem::transformations()` | 读取 item 当前变换链。 |

## 4. 关键用法

```cpp
auto *scale = new QGraphicsScale;
scale->setXScale(1.0);
scale->setYScale(1.0);

item->setTransformations({ scale });

auto *anim = new QPropertyAnimation(scale, "xScale", item);
anim->setEndValue(1.4);
anim->start(QAbstractAnimation::DeleteWhenStopped);
```

变换链顺序很重要。先缩放再旋转，和先旋转再缩放，视觉结果可能不同。

## 5. 使用场景

适合 item 动画、组合变换、3D-ish 旋转、交互式缩放、属性面板调变换参数、需要把变换拆成多个可控对象的编辑器。

如果只是一次性设置简单旋转或缩放，直接用 `QGraphicsItem::setRotation()`、`setScale()` 更简单。

## 6. 常见坑与经验

变换对象是 QObject，注意生命周期。通常让 item 或控制器持有它，避免 item 还在用而对象已删除。

`applyTo()` 操作的是矩阵，不应该有绘制副作用。它只描述几何变换。

item 自带的 pos/rotation/scale 和 transformations 列表会共同作用。复杂场景要约定哪些变换放在哪一层，避免调试困难。
