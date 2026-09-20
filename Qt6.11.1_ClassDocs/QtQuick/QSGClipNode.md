# QSGClipNode
> Qt 6.11.1 · Qt Quick · 来自 `QSGClipNode`

## 作用定位
`QSGClipNode` 为子树定义裁剪区域，可用矩形或几何形状限制后续节点的可见像素。

## API 速查
| API | 是做什么的 |
|---|---|
| `setClipRect()` | 设置矩形裁剪范围。|
| `setGeometry()` | 使用几何定义非矩形裁剪。|
| `setIsRectangular()` | 告知是否为矩形，以便优化。|
| `setClipList()` | 设置额外裁剪链。|

## 使用场景
滚动视口、仪表盘窗口或复杂自定义遮罩。

## 常见坑与经验
- 非矩形裁剪可能使用 stencil，成本明显高于矩形 scissor。
- 裁剪只限制绘制，不会自动改变鼠标命中区域。

## 知识点覆盖
scissor、stencil、视口裁剪、渲染状态成本、交互边界。
