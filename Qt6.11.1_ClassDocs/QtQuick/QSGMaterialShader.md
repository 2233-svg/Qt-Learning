# QSGMaterialShader
> Qt 6.11.1 · Qt Quick · 来自 `QSGMaterialShader`

## 作用定位
`QSGMaterialShader` 是 `QSGMaterial` 的渲染实现，负责提供预编译 `QShader`、声明 uniform 并在每帧更新数据。

## API 速查
| API | 是做什么的 |
|---|---|
| `setShaderFileName()` | 指定 `.qsb` shader 包。|
| `setUniformData()` | 写入 uniform buffer 数据。|
| `updateSampledImage()` | 绑定纹理采样器资源。|
| `updateGraphicsPipelineState()` | 调整混合、cull 等管线状态。|
| `attributes()` | 声明需要的顶点属性。|

## 使用场景
以 Qt Shader Tools 编译 `.vert/.frag` 得到 `.qsb`，在 material shader 中更新颜色、变换或纹理。

## 常见坑与经验
- uniform 偏移必须匹配 `.qsb` 的反射布局；不要按猜测硬编码。
- 每帧更新的数据要小而连续；大数组优先考虑纹理或专用缓冲方案。

## 知识点覆盖
QShader、uniform buffer、纹理采样、管线状态、着色器打包。
