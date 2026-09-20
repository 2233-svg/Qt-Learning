# QSGRendererInterface
> Qt 6.11.1 · Qt Quick · 来自 `QSGRendererInterface`

## 作用定位
`QSGRendererInterface` 提供查询 Qt Quick 当前渲染后端和原生资源的入口。它是高级互操作代码判断“我现在面对的是 Vulkan、Metal、D3D 还是 OpenGL”的方式。

## API 速查
| API | 是做什么的 |
|---|---|
| `graphicsApi()` | 返回当前图形 API。|
| `shaderType()` | 返回 shader 类型和打包方式。|
| `shaderCompilationType()` | 查询 shader 编译策略。|
| `shaderSourceType()` | 查询 shader 源类型。|
| `getResource()` | 取得特定原生资源指针。|
| `getResource(window, Resource)` | 针对窗口取得上下文、设备等资源。|

## 使用场景
在渲染阶段接入外部图形库前，查询当前 API 和资源，再选择对应互操作路径。

## 常见坑与经验
- `getResource()` 返回的是后端相关指针，类型和有效期都必须按文档和帧阶段处理。
- 仅为了画普通自定义内容，不应下探到 renderer interface；用 `QSGMaterial` 或 `QQuickRhiItem` 更可维护。

## 知识点覆盖
后端探测、原生资源、shader 类型、互操作、生命周期。
