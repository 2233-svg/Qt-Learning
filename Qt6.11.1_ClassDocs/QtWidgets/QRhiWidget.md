# QRhiWidget

> Qt 6.11.1 · Qt Widgets · 来自 `QRhiWidget`

## 1. 先建立直觉

`QRhiWidget` 是把 Qt RHI 渲染嵌入 QWidget 界面的控件。RHI 是 Qt 对多种图形后端的抽象层，可以落到 OpenGL、Vulkan、Metal、Direct3D 等 API。

它适合在传统 Widgets 应用里放一块 GPU 渲染区域：实时预览、可视化、2D/3D 画布、图形调试面板。它不是 `QPainter` 的替代品，也不是给普通按钮/表单加速的开关；它面向你确实要提交 GPU 命令的场景。

## 2. 类说明

`QRhiWidget` 继承自 `QWidget`。使用时通常继承它，并重写 `initialize()`、`render()`、`releaseResources()`。Qt 负责创建渲染目标和在合适时机调用你的渲染函数，你负责准备管线、资源、uniform、纹理和绘制命令。

这个类的关键边界是生命周期。GPU 资源可能因为窗口重建、后端变化、尺寸变化而需要重建，不能把它当成普通成员对象随便长期持有而不响应释放。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `setApi(Api)` / `api()` | 指定或读取图形后端：`OpenGL`、`Vulkan`、`Metal`、`Direct3D11/12`、`Null`。 |
| `setDebugLayerEnabled(bool)` / `isDebugLayerEnabled()` | 启用底层图形 API 调试层，开发期排错用。 |
| `setColorBufferFormat(TextureFormat)` | 设置颜色缓冲格式，例如 `RGBA8`、`RGBA16F`、`RGBA32F`、`RGB10A2`。 |
| `setSampleCount(int)` / `sampleCount()` | 设置 MSAA 采样数。高质量边缘和性能之间要权衡。 |
| `setFixedColorBufferSize(QSize)` | 固定颜色缓冲像素尺寸，适合离屏式或特定分辨率渲染。 |
| `setMirrorVertically(bool)` | 控制最终图像是否垂直镜像，常用于后端坐标差异适配。 |
| `grabFramebuffer()` | 抓取当前帧为 `QImage`，适合截图、测试或缩略图。 |
| `rhi()` | 在渲染生命周期中取得 `QRhi` 实例。 |
| `renderTarget()` | 获取当前渲染目标。 |
| `colorTexture()` / `resolveTexture()` | 获取颜色纹理或 MSAA resolve 后纹理。 |
| `depthStencilBuffer()` | 获取深度模板缓冲。 |
| `initialize(QRhiCommandBuffer *)` | 初始化或重建 GPU 资源。子类通常重写。 |
| `render(QRhiCommandBuffer *)` | 提交每帧渲染命令。子类通常重写。 |
| `releaseResources()` | 释放 GPU 资源。窗口/后端变化和析构时会用到。 |
| `frameSubmitted()` | 一帧提交后发出。 |
| `renderFailed()` | 渲染无法继续时发出，适合降级提示。 |

## 4. 关键用法

```cpp
class PreviewWidget : public QRhiWidget {
protected:
    void initialize(QRhiCommandBuffer *cb) override
    {
        Q_UNUSED(cb);
        // 创建 QRhiBuffer、QRhiTexture、QRhiGraphicsPipeline 等资源。
    }

    void render(QRhiCommandBuffer *cb) override
    {
        // 使用 renderTarget() 开始 render pass，并提交绘制命令。
    }

    void releaseResources() override
    {
        // 释放所有依赖 QRhi 的资源。
    }
};
```

创建后端时要尽早设置：

```cpp
auto *view = new PreviewWidget(this);
view->setApi(QRhiWidget::Api::Vulkan);
view->setSampleCount(4);
```

后端、采样数、缓冲格式这类设置可能触发资源重建，因此不要在每帧随意切换。

## 5. 使用场景

适合 CAD/建模预览、图像滤镜预览、shader 调试器、科学可视化、节点编辑器预览、实时曲面/点云显示，以及需要在现有 Widgets 应用中嵌入现代 GPU 渲染的工具。

如果只是画简单线条、图标、控件背景，优先用 `QPainter` 或普通 widget 绘制。`QRhiWidget` 的复杂度来自 GPU 生命周期，不值得为轻量绘制引入。

## 6. 常见坑与经验

GPU 资源要在正确生命周期里创建和释放。不要在构造函数里假设 `rhi()`、render target 或尺寸已经可用。

高 DPI 下 widget 逻辑尺寸和颜色缓冲像素尺寸可能不同。涉及截图、鼠标拾取、纹理大小时要明确使用的是哪套坐标。

打开 debug layer 很适合开发期找资源状态和 API 用法问题，但发布版要评估性能和平台可用性。
