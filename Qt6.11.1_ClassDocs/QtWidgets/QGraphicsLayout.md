# QGraphicsLayout

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsLayout`

## 1. 先建立直觉

`QGraphicsLayout` 是 Graphics View 布局管理器的抽象基类。它管理 `QGraphicsLayoutItem`，在 `QGraphicsWidget` 内部安排子项几何。

它对应 QWidget 世界里的 `QLayout`，但工作对象是图形布局项，坐标和尺寸是浮点数，适合可缩放的场景内 UI。

## 2. 类说明

`QGraphicsLayout` 同时是 `QGraphicsLayoutItem`，因此布局可以嵌套。具体排列策略由子类提供，例如 `QGraphicsLinearLayout`、`QGraphicsGridLayout`、`QGraphicsAnchorLayout`。

自定义布局时，需要实现 item 数量、取 item、移除 item、尺寸提示、设置 geometry 等核心行为。多数业务直接用内置布局即可。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `activate()` | 激活布局，重新计算并应用几何。 |
| `invalidate()` | 标记布局失效，下次需要重新计算。 |
| `isActivated()` | 判断布局当前是否已激活。 |
| `updateGeometry()` | 通知上层尺寸提示变化。 |
| `setContentsMargins()` / `getContentsMargins()` | 设置或读取布局内容边距。 |
| `contentsRect()` | 返回扣除边距后的布局区域。 |
| `widgetEvent(QEvent *)` | 接收关联 `QGraphicsWidget` 的事件，布局可据此响应。 |
| `count()` | 子类实现，返回布局项数量。 |
| `itemAt(int)` | 子类实现，按索引返回布局项。 |
| `removeAt(int)` | 子类实现，移除布局项。 |
| `setGeometry(QRectF)` | 布局接收分配区域并安排子项。 |

## 4. 关键用法

通常不直接创建 `QGraphicsLayout`，而是使用子类：

```cpp
auto *panel = new QGraphicsWidget;
auto *layout = new QGraphicsLinearLayout(Qt::Vertical);
layout->setContentsMargins(8, 8, 8, 8);
panel->setLayout(layout);
```

布局内容变化后：

```cpp
layout->invalidate();
layout->activate();
```

多数时候只需 `invalidate()`，Qt 会在合适时机激活。

## 5. 使用场景

适合自定义场景内 UI 布局、可缩放节点面板、图形属性框、复杂图元组合排版。

普通 QWidget 界面继续使用 `QLayout` 家族；不要把 Graphics Layout 当作传统控件布局替代品。

## 6. 常见坑与经验

自定义布局不要在 `setGeometry()` 里改业务数据。它可能被频繁调用，应只做布局计算和分配。

边距属于布局管理器，不属于子 item。子 item 自己再设置边距会叠加，容易让间距超出预期。

布局项没有 QWidget 那样的像素整数约束。使用浮点数能让缩放更平滑，但也要求你别过早取整。
