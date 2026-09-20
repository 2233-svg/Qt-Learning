# QQuickPaintedItem
> Qt 6.11.1 · Qt Quick · 来自 `QQuickPaintedItem`

## 作用定位
`QQuickPaintedItem` 让传统 `QPainter` 绘制代码出现在 Qt Quick 场景中。它把 `paint(QPainter *)` 的输出先画入纹理或图像，再由 Scene Graph 显示，适合复用已有 2D 绘制算法。

## 类说明
它是“兼容层”而不是最快的自定义绘制路径。绘制区域大、每帧变化或需要复杂 GPU 效果时，应直接使用 `QQuickItem::updatePaintNode()`。

## API 速查
| API | 是做什么的 |
|---|---|
| `paint(QPainter *)` | 必须重实现的实际绘制入口。|
| `setRenderTarget()` | 选择图像或 FBO 渲染目标；可用性受后端限制。|
| `setContentsSize()` | 设置内部绘制缓冲大小。|
| `setFillColor()` | 设置缓冲未绘制部分的底色。|
| `setAntialiasing()` | 请求抗锯齿绘制。|
| `setOpaquePainting()` | 告知绘制完全不透明，以便优化。|
| `setMipmap()` | 为缩放纹理生成 mipmap。|
| `update()` | 标记内容失效，下一帧会重新调用 `paint()`。|

## 使用场景
```cpp
void PlotItem::paint(QPainter *painter)
{
    painter->setRenderHint(QPainter::Antialiasing);
    painter->drawPath(m_curve);
}
```
用于低频刷新的曲线、打印预览式内容或迁移已有 QPainter 图元；数据变更后调用 `update()`，不要在 `paint()` 中改 QML 属性。

## 常见坑与经验
- 纹理上传是主要成本；动画曲线每帧重画时，性能通常比 Scene Graph 几何差得多。
- `paint()` 的坐标以 item 本地坐标为准，仍要处理高 DPI 和 `contentsSize`。
- `setOpaquePainting(true)` 只有确实覆盖全部像素时才正确，否则会留下脏像素。

## 知识点覆盖
QPainter、纹理化绘制、缓存尺寸、GPU 上传、抗锯齿、Qt Quick 性能分层。
