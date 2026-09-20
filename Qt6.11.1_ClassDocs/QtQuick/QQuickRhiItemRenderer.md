# QQuickRhiItemRenderer
> Qt 6.11.1 · Qt Quick · 来自 `QQuickRhiItemRenderer`

## 作用定位
`QQuickRhiItemRenderer` 是 `QQuickRhiItem` 的渲染端对象。它创建 QRhi 资源、接收 GUI 线程同步出的状态，并在每帧向目标纹理录制绘制命令。

## API 速查
| API | 是做什么的 |
|---|---|
| `initialize()` | 目标或 RHI 改变后创建/重建 GPU 资源。|
| `synchronize(item)` | 从对应 item 复制本帧需要的状态。|
| `render(commandBuffer)` | 录制当前帧绘制命令。|
| `update()` | 请求 item 再渲染一帧。|
| `rhi()` | 取得当前 QRhi。|
| `renderTarget()` | 取得当前离屏渲染目标。|
| `colorTexture()` | 取得输出颜色纹理。|
| `pixelSize()` | 取得当前目标像素尺寸。|

## 使用场景
`synchronize()` 只复制 POD 参数、不可变快照或经锁保护的数据；`render()` 只使用 renderer 自己拥有的 GPU 资源。这种切分让 GUI 线程更新属性而不阻塞渲染线程。

## 常见坑与经验
- `initialize()` 不只会调用一次，窗口重建或尺寸变动都可能触发；资源创建代码必须可重复执行。
- `render()` 里不要访问 `QQuickItem`，所有输入都应在 `synchronize()` 带过来。
- 调用 `update()` 是请求下一帧，不应在静止内容上形成无限刷新循环。

## 知识点覆盖
双线程状态同步、GPU 资源生命周期、命令缓冲、离屏纹理、帧请求。
