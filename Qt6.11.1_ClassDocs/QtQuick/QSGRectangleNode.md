# QSGRectangleNode
> Qt 6.11.1 · Qt Quick · 来自 `QSGRectangleNode`

## 作用定位
`QSGRectangleNode` 是平台适配的矩形绘制节点。它比自己手写矩形 geometry 更能受益于 Qt Quick 的内部优化。

## API 速查
| API | 是做什么的 |
|---|---|
| `setRect()` | 设置矩形区域。|
| `setColor()` | 设置填充颜色。|

## 使用场景
自定义 item 中需要背景块、进度条、选区框等简单矩形时，优先从 `QQuickWindow::createRectangleNode()` 创建。

## 常见坑与经验
- 它是抽象接口风格的内置节点，具体实现由窗口决定。
- 圆角、描边或复杂渐变不是它的职责。

## 知识点覆盖
内置节点、矩形填充、后端适配、简单图元优化。
