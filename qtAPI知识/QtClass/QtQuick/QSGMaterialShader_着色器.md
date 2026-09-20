# QSGMaterialShader：跨图形 API 的自定义材质着色器

> Qt 6.11.1 · `#include <QSGMaterialShader>` · 模块：`Qt6::Quick`

`QSGMaterialShader` 是 `QSGMaterial` 的渲染实现：它持有顶点/片段着色器，定义 uniform、纹理和有限 pipeline 状态如何随材质与场景图状态更新。Qt Quick 为每个材质类型在一个场景图中按需创建并缓存一个 shader 实例。

## 它解决的问题

一个 `QSGGeometryNode` 可以有很多材质实例，例如每个实例各有颜色、纹理或参数；但它们若共享同一套 shader 程序，就不必分别编译和建立 pipeline。材质对象保存每个绘制实例的值，`QSGMaterialShader` 则将这些值填入 scene graph 管理的 uniform buffer、采样器和 pipeline 配置。

Qt 6 的此类不再是 `QOpenGLShaderProgram` 的封装，不能直接调用 OpenGL、Vulkan、Metal 或 Direct3D。它应保持后端无关，默认流程是用 `qsb` 在构建期将 Vulkan 风格 GLSL 编译成 `.qsb`，并在构造函数中指定顶点和片段 shader 文件。

## 三种更新回调

有 uniform block 时覆写 `updateUniformData()`。它只修改 `RenderState::uniformData()` 返回的字节数组，返回 `true` 表示确有变动；矩阵、透明度等未标为 dirty 时，原缓冲区数据仍有效，不应无条件重复写。

着色器有纹理采样器时覆写 `updateSampledImage()`。它会对每个 binding 调用，`QSGTexture **` 可能是数组，大小由 `combinedImageSamplerCount(binding)` 决定。空元素必须填成有效纹理，所有权不转移；通常还应调用纹理的 `commitTextureOperations()`。

只有需要特定混合或剔除状态时，才开启 `UpdatesGraphicsPipelineState` 并覆写 `updateGraphicsPipelineState()`。它不是任意 GPU 状态的入口，Qt 目前只开放混合、剔除及相关有限状态。

## 构造与生命周期边界

`QSGMaterial::createShader()` 创建 shader 后，场景图会缓存它。应在 shader 构造期间调用 `setShaderFileName()` 或 `setShader()`，不要在之后动态替换着色器，否则已有 pipeline 的行为不可靠。多视图文件重载中的 `viewCount` 只接受 `2`、`3` 或 `4`。

它是场景图渲染侧对象，所有回调均运行在场景图渲染线程。材质中来自 GUI 线程的参数必须在同步阶段形成可安全读取的状态，不能在回调中直接访问仍会并发修改的 Item 数据。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QSGMaterialShader()` / `~QSGMaterialShader()` | 创建/销毁 shader 实现；实例由场景图经 `QSGMaterial::createShader()` 管理。 |
| `setShaderFileName(stage, filename)` | 保护函数；为顶点或片段阶段指定序列化 `QShader` 文件，通常是资源中的 `.qsb`。 |
| `setShaderFileName(stage, filename, viewCount)` | Qt 6.8 起的多视图重载；`viewCount` 应为 `2`、`3` 或 `4`。 |
| `setShader(stage, shader)` | 保护函数；直接设置已加载的 `QShader`。应在构造期间完成。 |
| `updateUniformData(state, newMaterial, oldMaterial)` | 更新 uniform 字节数组；改动数据时返回 `true`，不能在其中发出实际图形命令。 |
| `updateSampledImage(state, binding, texture, newMaterial, oldMaterial)` | 为 shader 的采样 binding 指定纹理；纹理指针数组不转移所有权。 |
| `combinedImageSamplerCount(binding)` | Qt 6.4 起返回 binding 对应 sampler 数组的总元素数。 |
| `updateGraphicsPipelineState(state, ps, newMaterial, oldMaterial)` | 更新允许的 pipeline 状态；仅在启用相应标志后才会调用。 |
| `setFlag(flags, on)` / `setFlags(flags)` / `flags()` | 管理 shader 标志。 |
| `UpdatesGraphicsPipelineState` | 选择加入 `updateGraphicsPipelineState()` 回调；默认关闭。 |
| `VertexStage` / `FragmentStage` | 指定设置的是顶点还是片段 shader。 |
