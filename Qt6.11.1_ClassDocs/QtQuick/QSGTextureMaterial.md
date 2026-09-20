# QSGTextureMaterial
> Qt 6.11.1 · Qt Quick · 来自 `QSGTextureMaterial`

## 作用定位
`QSGTextureMaterial` 用于绘制可能包含透明度的纹理，是贴图节点和自定义纹理几何的常用材质。

## API 速查
| API | 是做什么的 |
|---|---|
| `setTexture()` | 设置被采样纹理。|
| `setFiltering()` | 控制 nearest/linear 过滤。|
| `setMipmapFiltering()` | 控制 mipmap 过滤。|
| `setHorizontalWrapMode()` / `setVerticalWrapMode()` | 控制坐标越界采样。|

## 使用场景
精灵、图标、九宫格外的自定义贴图网格、带 alpha 的图片图元。

## 常见坑与经验
- 半透明纹理对绘制顺序敏感，不要把需要严格叠放的节点交给随意排序。
- 图集中的纹理坐标要使用子区域，避免采到邻近图片边缘。

## 知识点覆盖
alpha 纹理、采样过滤、图集边缘、绘制顺序、纹理坐标。
