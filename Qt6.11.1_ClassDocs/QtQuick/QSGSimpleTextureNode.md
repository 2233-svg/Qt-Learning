# QSGSimpleTextureNode
> Qt 6.11.1 · Qt Quick · 来自 `QSGSimpleTextureNode`

## 作用定位
`QSGSimpleTextureNode` 是显示一张纹理的便利节点，适合把 `QSGTexture` 快速放进自定义 Scene Graph。

## API 速查
| API | 是做什么的 |
|---|---|
| `setTexture()` | 设置显示纹理。|
| `setRect()` | 设置目标矩形。|
| `setSourceRect()` | 设置纹理源区域。|
| `setFiltering()` | 设置采样过滤。|
| `setOwnsTexture()` | 控制纹理释放责任。|

## 使用场景
一次性显示 CPU 生成图像、离屏渲染结果或业务缓存纹理。

## 常见坑与经验
- 它足够方便，但复杂图片布局、九宫格和多纹理效果需要更专门的节点或材质。
- 纹理来自图集时注意源矩形和边缘采样。

## 知识点覆盖
纹理节点、源区域、所有权、过滤模式、快速显示。
