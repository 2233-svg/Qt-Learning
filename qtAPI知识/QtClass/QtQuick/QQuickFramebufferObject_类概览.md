# QQuickFramebufferObject：将遗留 OpenGL FBO 渲染嵌进 Qt Quick

> Qt 6.11.1 | `#include <QQuickFramebufferObject>` | CMake: `Qt6::Quick`

`QQuickFramebufferObject` 是把自定义 OpenGL 绘制结果作为 Qt Quick texture 显示的便利类。它解决 Qt 5 风格 OpenGL renderer 与 QML scene graph 的衔接问题：业务属性留在 item，GL 命令留在独立 `Renderer`，后者渲染进 FBO 后由 Quick 合成。

这是**仅 OpenGL 可用的遗留类**。使用 Vulkan、Metal、Direct3D 或软件后端时它不工作；新项目的跨后端自定义渲染优先考虑 RHI 路径，如 `QQuickRhiItem`。

## Item 与 Renderer 必须分离

```cpp
class ScopeItem final : public QQuickFramebufferObject
{
    Q_OBJECT
    Q_PROPERTY(float gain READ gain WRITE setGain NOTIFY gainChanged)

public:
    Renderer *createRenderer() const override;

    float gain() const { return m_gain; }
    void setGain(float gain) { m_gain = gain; update(); }

private:
    float m_gain = 1.0f;
};
```

`ScopeItem` 在 GUI 线程接收 QML 属性变化；`Renderer` 大多在 scene graph 渲染线程调用 OpenGL。两者不能在任意时刻共享读写成员。用 `item->update()` 请求下一帧，再由 `Renderer::synchronize()` 在 GUI 线程被阻塞时复制必要状态。

`createRenderer()` 自身也在渲染线程、GUI 线程被阻塞时调用。Renderer 与 FBO 都由 Qt 内部管理，派生类不应手工 delete。

## 尺寸与纹理消费

默认 `textureFollowsItemSize` 为 true，item 尺寸变化就重建 FBO。固定分辨率的离屏内容可设为 false，并由 `Renderer::createFramebufferObject()` 返回期望尺寸；但需要自行处理缩放、清晰度和资源使用。

`mirrorVertically` 默认 false，用于纠正第三方 OpenGL 绘制坐标原点与 Quick 纹理方向不一致的问题。它只处理显示方向，不修复投影矩阵、内容裁切或 readback 坐标。

该 item 是 texture provider，可直接供 `ShaderEffect` 等纹理消费者使用。

## API 速查表

| API | 语义 | 关键边界 |
|---|---|---|
| `createRenderer()` | 创建本 item 的渲染器 | 纯虚；在渲染线程调用，不能读取不受保护的 GUI 状态 |
| `textureFollowsItemSize` | FBO 是否随 item 尺寸重建 | true 为默认；频繁 resize 会导致资源反复创建 |
| `setTextureFollowsItemSize(false)` | 使用 renderer 自定义 FBO 尺寸 | 需要自行保证清晰度和缩放语义 |
| `mirrorVertically` | 合成时垂直镜像 FBO 内容 | 适合原点方向差异，不改变 OpenGL 实际绘制 |
| `update()` | 从 item 请求后续渲染 | 用于 GUI 线程状态变化；不立即执行 GL |
| `isTextureProvider()` / `textureProvider()` | 将 FBO 结果公开为 Quick 纹理 | 只在 OpenGL scene graph 中有意义 |

## 使用边界

- 不要把它误作抽象的 GPU 渲染接口；后端限定是硬条件。
- item 与 renderer 的共享数据只在 `synchronize()` 安全交接，或使用明确的线程同步。
- FBO 的样本数、附件和纹理生存期由 renderer 合约管理，不应和外部 GL 资源混淆。
