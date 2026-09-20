# QSGSimpleRectNode：默认后端可用的简单色块

> Qt 6.11.1 · `#include <QSGSimpleRectNode>` · 模块：`Qt6::Quick` · 继承：`QSGGeometryNode`

`QSGSimpleRectNode` 是把矩形和颜色直接封装为一个几何节点的便利类。它能快速实现色块，却不是面向全部 Qt Quick 场景图后端的通用构件。

## 适用与替代

已知应用只运行在 Qt Quick 默认后端或软件后端时，它可用来实现极简自定义 Item 的背景：

```cpp
auto *node = static_cast<QSGSimpleRectNode *>(oldNode);
if (!node)
    node = new QSGSimpleRectNode;
node->setRect(boundingRect());
node->setColor(Qt::steelblue);
return node;
```

若控件会运行在特殊图形后端、嵌入式平台或希望保留长期兼容性，应改用 `window()->createRectangleNode()` 返回的 `QSGRectangleNode`。Qt 文档明确限定 `QSGSimpleRectNode` 只在默认或软件场景图后端正常工作。

## 使用边界

初始颜色为白色。`setRect()` 设置本地目标区域，`setColor()` 更新填充色；二者均应只在渲染线程调用。它不是 `QQuickItem`，不会跟随 Item 自动调整尺寸或颜色，属性变化仍需由 Item 调用 `update()` 后在下一次 `updatePaintNode()` 同步。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QSGSimpleRectNode()` | 创建简单矩形节点，颜色默认白色。 |
| `QSGSimpleRectNode(rect, color)` | 同时给出初始矩形与颜色。 |
| `setRect(const QRectF &rect)` | 设置目标矩形。 |
| `setRect(x, y, width, height)` | 设置矩形的便捷重载。 |
| `rect()` | 返回当前目标矩形。 |
| `setColor(const QColor &color)` | 设置纯色填充。 |
| `color()` | 返回当前填充色。 |
| `QQuickWindow::createRectangleNode()` | 跨后端代码应优先使用的替代方案。 |
