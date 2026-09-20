# QGraphicsOpacityEffect

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsOpacityEffect`

## 1. 先建立直觉

`QGraphicsOpacityEffect` 给目标绘制结果应用透明度。它可以让整个 widget 或 item 淡入淡出，也可以用 `opacityMask` 做渐隐遮罩。

对 `QGraphicsItem` 来说，本身就有 `setOpacity()`；`QGraphicsOpacityEffect` 更适合 QWidget 或需要遮罩透明的场景。选择哪个，取决于你是在 item 模型里工作，还是要对最终绘制结果做后处理。

## 2. 类说明

`QGraphicsOpacityEffect` 继承自 `QGraphicsEffect`。`opacity` 通常在 0 到 1 之间，0 完全透明，1 完全不透明。`opacityMask` 是一个 brush，用来按区域改变透明度。

透明效果不自动禁用交互。一个透明度为 0 的控件仍可能接收鼠标和键盘事件，除非你同步设置 enabled/visible 或调整事件处理。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsOpacityEffect(QObject *)` | 创建透明度效果。 |
| `setOpacity(qreal)` / `opacity()` | 设置或读取整体透明度。 |
| `setOpacityMask(const QBrush &)` / `opacityMask()` | 设置或读取透明遮罩。 |
| `opacityChanged(qreal)` | 整体透明度变化时发出。 |
| `opacityMaskChanged(QBrush)` | 遮罩变化时发出。 |
| `setEnabled(bool)` | 继承自 `QGraphicsEffect`，快速开关效果。 |

## 4. 关键用法

```cpp
auto *effect = new QGraphicsOpacityEffect(panel);
effect->setOpacity(0.65);
panel->setGraphicsEffect(effect);
```

淡入动画：

```cpp
auto *anim = new QPropertyAnimation(effect, "opacity", effect);
anim->setStartValue(0.0);
anim->setEndValue(1.0);
anim->setDuration(160);
anim->start(QAbstractAnimation::DeleteWhenStopped);
```

## 5. 使用场景

适合控件淡入淡出、禁用区域弱化、悬浮面板过渡、图片渐隐、场景对象临时透明、遮罩式提示。

如果是 `QGraphicsItem` 的简单整体透明，优先考虑 `QGraphicsItem::setOpacity()`；它更贴近 item 系统，通常也更直接。

## 6. 常见坑与经验

透明不等于不可交互。隐藏时若不想响应点击，应同时 `setVisible(false)` 或禁用目标。

多个透明层叠加会让文字可读性下降。工具类软件里，淡化要服务信息层级，不要牺牲识别。

遮罩透明适合做局部渐隐，但也更容易带来额外绘制成本。大面积动态遮罩要测试性能。
