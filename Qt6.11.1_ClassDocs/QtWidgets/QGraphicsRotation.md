# QGraphicsRotation

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsRotation`

## 1. 先建立直觉

`QGraphicsRotation` 是可放入 item 变换链的旋转对象。它把旋转角度、旋转轴和旋转原点做成属性，适合动画和组合变换。

普通 2D 旋转可以直接 `QGraphicsItem::setRotation()`；如果要绕指定点旋转、做翻牌效果、和缩放组成一串可动画变换，就用 `QGraphicsRotation`。

## 2. 类说明

`QGraphicsRotation` 继承自 `QGraphicsTransform`。`angle` 表示角度，`axis` 表示旋转轴，`origin` 表示旋转中心。它通过 `applyTo()` 把旋转累积到矩阵。

虽然 Graphics View 主要是 2D，但这个类使用 `QVector3D`，因此可以表达绕 X/Y/Z 轴的旋转。绕 Z 轴最接近普通平面旋转。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsRotation(QObject *)` | 创建旋转变换对象。 |
| `setAngle(qreal)` / `angle()` | 设置或读取旋转角度。 |
| `setAxis(QVector3D)` / `axis()` | 设置或读取旋转轴。 |
| `setAxis(Qt::Axis)` | 用 `Qt::XAxis/YAxis/ZAxis` 快速设置轴。 |
| `setOrigin(QVector3D)` / `origin()` | 设置或读取旋转中心。 |
| `applyTo(QMatrix4x4 *)` | 把旋转应用到矩阵。 |
| `angleChanged()` | 角度变化时发出。 |
| `axisChanged()` | 旋转轴变化时发出。 |
| `originChanged()` | 原点变化时发出。 |

## 4. 关键用法

```cpp
auto *rotation = new QGraphicsRotation(item);
rotation->setAxis(Qt::ZAxis);
rotation->setOrigin(QVector3D(50, 50, 0));
item->setTransformations({ rotation });

auto *anim = new QPropertyAnimation(rotation, "angle", item);
anim->setStartValue(0);
anim->setEndValue(360);
anim->setDuration(800);
anim->start(QAbstractAnimation::DeleteWhenStopped);
```

翻牌式效果可以绕 Y 轴：

```cpp
rotation->setAxis(Qt::YAxis);
```

## 5. 使用场景

适合旋转动画、图标转动、翻牌/展开效果、节点方向指示、仪表指针、和缩放/平移组合的高级 item 变换。

如果只是静态旋转 15 度，item 自带 `setRotation()` 更简单。这个类的优势在可动画、可组合、可指定轴。

## 6. 常见坑与经验

原点不对时，旋转会像“绕奇怪的点甩出去”。先确认 item 局部坐标和 `origin` 是否匹配。

绕 X/Y 轴旋转会产生 3D 风格投影效果，但 Graphics View 仍是 2D 场景。不要把它当完整 3D 引擎。

多个 transform 的顺序会改变结果。缩放后旋转和旋转后缩放在非等比情况下差别很明显。
