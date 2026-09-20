# QSGImageNode
> Qt 6.11.1 · Qt Quick · 来自 `QSGImageNode`

## 作用定位
`QSGImageNode` 是 Qt Quick 提供的图片绘制节点，封装纹理、源矩形、目标矩形和过滤模式，比手写 geometry 加 texture material 更直接。

## API 速查
| API | 是做什么的 |
|---|---|
| `setTexture()` | 设置图片纹理。|
| `setRect()` | 设置绘制到 item 中的目标矩形。|
| `setSourceRect()` | 设置纹理源区域。|
| `setFiltering()` | 设置缩放过滤。|
| `setMipmapFiltering()` | 设置 mipmap 过滤。|
| `setOwnsTexture()` | 决定节点是否负责释放纹理。|

## 使用场景
自定义 item 中显示一张或多张由 C++ 生成的图片，尤其是需要源区域裁剪时。

## 常见坑与经验
- 使用 `QQuickWindow::createImageNode()` 创建，确保节点适配当前渲染后端。
- 纹理所有权要明确；窗口释放后纹理也要跟随失效。

## 知识点覆盖
图片节点、源矩形、目标矩形、纹理所有权、采样过滤。
