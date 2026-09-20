# QSGRectangleNode：由窗口后端创建的矩形节点接口

> Qt 6.11.1 · `#include <QSGRectangleNode>` · 模块：`Qt6::Quick` · 继承：`QSGGeometryNode`

`QSGRectangleNode` 表示一个纯色矩形，但它的价值不只是“四个顶点”。它是 Qt Quick 为不同图形后端保留的抽象接口：窗口可以提供最适合当前渲染器的实现。

## 实际使用

在自定义 `QQuickItem` 中需要画背景、色块、占位条或选区时，从承载该 Item 的窗口取得节点：

```cpp
auto *node = static_cast<QSGRectangleNode *>(oldNode);
if (!node)
    node = window()->createRectangleNode();

node->setRect(boundingRect());
node->setColor(m_background);
return node;
```

通过 `QQuickWindow::createRectangleNode()` 创建，比自行实例化旧的实用节点更能兼容图形 API、软件渲染器及将来的特殊场景图后端。

## 语义与边界

这是抽象类，`setRect()`、`rect()`、`setColor()`、`color()` 都由后端实现。默认颜色是白色。几何尺寸属于 Item 的局部坐标系；父节点若有变换或裁剪，最终显示还会受到它们影响。

节点仍受场景图线程规则约束，且通常由 `updatePaintNode()` 返回给 Qt Quick 管理。不要跨帧在 GUI 线程改颜色；要由 GUI 线程触发重绘，应更新 Item 属性后调用 `update()`。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QQuickWindow::createRectangleNode()` | 推荐的构造入口，按当前场景图后端返回实现。 |
| `setRect(const QRectF &rect)` | 设置目标矩形区域。 |
| `setRect(x, y, width, height)` | `QRectF` 形式的便捷重载。 |
| `rect()` | 返回节点当前矩形。 |
| `setColor(const QColor &color)` | 设置填充色；初始颜色为白色。 |
| `color()` | 返回当前填充色。 |
| 继承的 `setGeometry()` / `setMaterial()` | 后端实现所依赖的低层接口；通常不应绕过矩形节点公开 API 自行替换。 |
