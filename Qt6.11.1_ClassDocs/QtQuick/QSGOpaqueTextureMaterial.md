# QSGOpaqueTextureMaterial
> Qt 6.11.1 · Qt Quick · 来自 `QSGOpaqueTextureMaterial`

## 作用定位
`QSGOpaqueTextureMaterial` 用于绘制完全不透明的纹理。它省去 alpha 混合路径，利于排序和批处理优化。

## API 速查
| API | 是做什么的 |
|---|---|
| `setTexture()` | 指定要采样的 `QSGTexture`。|
| `setFiltering()` | 设置纹理缩放采样。|
| `setMipmapFiltering()` | 设置 mipmap 过滤。|
| `setHorizontalWrapMode()` / `setVerticalWrapMode()` | 设置纹理坐标越界模式。|

## 使用场景
背景图、照片、视频帧中确定没有透明通道的部分。

## 常见坑与经验
- 只有像素确实不透明时才使用；否则透明区域会显示错误。
- 与 `QSGTextureMaterial` 的主要区别是 blending 状态，而不是纹理内容来源。

## 知识点覆盖
不透明优化、纹理采样、wrap mode、mipmap、批处理。
