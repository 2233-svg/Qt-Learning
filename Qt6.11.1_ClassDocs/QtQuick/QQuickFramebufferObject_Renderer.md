# QQuickFramebufferObject::Renderer
> Qt 6.11.1 · Qt Quick · 来自 `QQuickFramebufferObject::Renderer`

## 作用定位
`QQuickFramebufferObject::Renderer` 是 FBO 项的 OpenGL 渲染端。它拥有当前 OpenGL 上下文中的资源，并在 Qt Quick 的渲染线程里执行实际绘制。

## API 速查
| API | 是做什么的 |
|---|---|
| `render()` | 必须重实现，向当前 FBO 绘制一帧。|
| `createFramebufferObject(size)` | 创建与项尺寸匹配的 FBO，可自定义格式。|
| `synchronize(item)` | 从 GUI 线程 item 同步本帧状态。|
| `framebufferObject()` | 取得当前 FBO。|
| `update()` | 请求后续一帧。|

## 使用场景
在 `synchronize()` 读取颜色、相机矩阵、数据版本号；在 `render()` 使用已同步的副本绑定 shader、VAO 和纹理并画图。

## 常见坑与经验
- `render()` 开始时不应假设任何 OpenGL 状态，结束时也应恢复或明确设置自己的状态。
- `update()` 形成连续帧循环前要有动画或异步数据依据，否则会空转。
- 不能从 renderer 直接调用 GUI 线程上的 item 方法。

## 知识点覆盖
OpenGL 状态隔离、FBO 生命周期、GUI/渲染线程同步、连续重绘。
