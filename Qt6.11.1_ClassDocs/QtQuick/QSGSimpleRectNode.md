# QSGSimpleRectNode
> Qt 6.11.1 · Qt Quick · 来自 `QSGSimpleRectNode`

## 作用定位
`QSGSimpleRectNode` 是简单矩形节点的便利实现，内部通常由几何加单色材质组成。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 `QSGSimpleRectNode(rect, color)` | 直接创建一个矩形。|
| `setRect()` | 修改矩形区域。|
| `setColor()` | 修改填充颜色。|

## 使用场景
调试绘制、轻量色块、简单状态指示条。

## 常见坑与经验
- 追求后端最佳优化时，优先使用 `QQuickWindow::createRectangleNode()`。
- 频繁改变尺寸和颜色后要确保节点被标记为 dirty，便利类通常会替你处理。

## 知识点覆盖
便利节点、单色矩形、快速原型、内置材质。
