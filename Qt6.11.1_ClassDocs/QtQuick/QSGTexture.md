# QSGTexture
> Qt 6.11.1 · Qt Quick · 来自 `QSGTexture`

## 作用定位
`QSGTexture` 是 Scene Graph 可采样纹理的抽象。它把图像、RHI 纹理或外部纹理以后端无关形式提供给材质和图像节点。

## API 速查
| API | 是做什么的 |
|---|---|
| `textureSize()` | 返回纹理像素大小。|
| `normalizedTextureSubRect()` | 返回实际内容在纹理中的归一化区域。|
| `setFiltering()` | 设置 nearest/linear 采样。|
| `setMipmapFiltering()` | 设置 mipmap 采样策略。|
| `setHorizontalWrapMode()` / `setVerticalWrapMode()` | 设置纹理坐标越界方式。|
| `commitTextureOperations()` | 提交动态纹理更新。|
| `comparisonKey()` | 返回同一底层纹理的比较键。|

## 使用场景
由 `QQuickWindow::createTextureFromImage()` 创建，随后交给 `QSGTextureMaterial` 或 `QSGImageNode`。

## 常见坑与经验
- 纹理只对创建它的窗口和当前 Scene Graph 有效。
- 放大像素画用 nearest，照片或缩放内容用 linear；错误选择会造成锯齿或模糊。
- 图集纹理的 `normalizedTextureSubRect()` 可能不是完整 0..1。

## 知识点覆盖
纹理采样、mipmap、图集、wrap mode、资源生命周期、图像缩放。
