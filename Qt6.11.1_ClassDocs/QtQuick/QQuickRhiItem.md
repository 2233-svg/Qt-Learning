# QQuickRhiItem

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickRhiItem` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickRhiItem` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickRhiItem>`
- 继承自：QQuickItem
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
target_link_libraries(mytarget PRIVATE Qt6::Quick)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

### 状态、生命周期和线程

**生命周期：** QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

**状态与结果：** 属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

**线程与事件循环：** 大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

## 3. 直接使用

需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。 使用时通常按这个过程组织：注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

```cpp
// C++ 侧暴露属性/信号后，在 QML 中建立绑定。
// 变化时发出 notify signal，避免在绑定表达式中直接修改状态。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum class TextureFormat { RGBA8, RGBA16F, RGBA32F, RGB10A2 }`

### 属性

- `alphaBlending : bool`
- `colorBufferFormat : TextureFormat`
- `effectiveColorBufferSize : QSize`
- `fixedColorBufferHeight : int`
- `fixedColorBufferWidth : int`
- `mirrorVertically : bool`
- `sampleCount : int`

### 公有函数

- `QQuickRhiItem(QQuickItem *parent = nullptr)`
- `virtual ~QQuickRhiItem() override`
- `bool alphaBlending() const`
- `QQuickRhiItem::TextureFormat colorBufferFormat() const`
- `QSize effectiveColorBufferSize() const`
- `int fixedColorBufferHeight() const`
- `int fixedColorBufferWidth() const`
- `bool isMirrorVerticallyEnabled() const`
- `int sampleCount() const`
- `void setAlphaBlending(bool enable)`
- `void setColorBufferFormat(QQuickRhiItem::TextureFormat format)`
- `void setFixedColorBufferHeight(int height)`
- `void setFixedColorBufferWidth(int width)`
- `void setMirrorVertically(bool enable)`
- `void setSampleCount(int samples)`

### 重实现的公有函数

- `virtual bool isTextureProvider() const override`
- `virtual QSGTextureProvider * textureProvider() const override`

### 信号

- `void alphaBlendingChanged()`
- `void colorBufferFormatChanged()`
- `void effectiveColorBufferSizeChanged()`
- `void fixedColorBufferHeightChanged()`
- `void fixedColorBufferWidthChanged()`
- `void mirrorVerticallyChanged()`
- `void sampleCountChanged()`

### 保护函数

- `virtual QQuickRhiItemRenderer * createRenderer() = 0`
- `bool isAutoRenderTargetEnabled() const`
- `void setAutoRenderTarget(bool enabled)`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`
- `virtual void geometryChange(const QRectF &newGeometry, const QRectF &oldGeometry) override`
- `virtual void releaseResources() override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QQuickRhiItem::TextureFormat`

**作用与语义：**

指定`QQuickRhiItem`渲染的背衬贴图格式。
- `QQuickRhiItem::TextureFormat::RGBA8`：`0`;参见`QRhiTexture::RGBA8`。这是默认。
- `QQuickRhiItem::TextureFormat::RGBA16F`：`1`;参见`QRhiTexture::RGBA16F`。
- `QQuickRhiItem::TextureFormat::RGBA32F`：`2`;参见`QRhiTexture::RGBA32F`。
- `QQuickRhiItem::TextureFormat::RGB10A2`：`3`;参见`QRhiTexture::RGB10A2`。

### `alphaBlending : bool`

**作用与语义：**

如果在绘制四边形时，控制键总是启用，并贴图由`QQuickRhiItem`及其渲染器生成的内容。
默认值为`false`。这是为了性能考虑：如果不涉及半透明，因为`QQuickRhiItemRenderer`会变成不透明的颜色，且从不渲染alpha小于1的片段，那么启用混合就没有意义。
如果`QQuickRhiItemRenderer`子类渲染时涉及半透明，则将该属性设为 true。
注意：在某些条件下，无论该属性的值如何，混合仍然会发生。例如，如果项的`opacity`（更准确地说，是从父链继承的总不透明度）小于1，即使该属性设置为false，混合仍会自动被启用。
注意：Qt Quick 场景图依赖并预期预先乘以 alpha 值。例如，如果意图是将渲染器背景清除到 alpha 值 0.5，则确保将红、绿、蓝的清晰色彩值乘以 0.5。否则混合结果将不正确。

**如何使用：** 调用 `alphaBlending()` 读取当前值；它不会修改应用状态。

### `colorBufferFormat : TextureFormat`

**作用与语义：**

该属性控制用作颜色缓冲区的纹理格式。默认值为`TextureFormat::RGBA8`。`QQuickRhiItem`支持渲染到`QRhiTexture`支持的部分格式。仅应指定`QRhi::isTextureFormatSupported()`报告支持的格式，否则渲染无法正常工作。
注意：当物品及其渲染器已经初始化并渲染完毕，设置新格式意味着渲染器创建的所有`QRhiGraphicsPipeline`对象都可能无法使用，如果相关`QRhiRenderPassDescriptor`因不同的纹理格式而变得不兼容。类似于动态更改`sampleCount`，这意味着initialize()或render()实现必须同时发布现有管线并创建新的管线。

**如何使用：** 调用 `colorBufferFormat()` 读取当前值；它不会修改应用状态。

### `[read-only] effectiveColorBufferSize : QSize`

**作用与语义：**

该属性揭示了底层颜色缓冲区（`QRhiTexture`或`QRhiRenderBuffer`）的像素大小。该特性供用户在GUI（主线程）中使用，通过QML绑定或JavaScript。
注意：`QQuickRhiItemRenderer`实现在场景图渲染线程上运行时，不应使用该属性。这些实现应当查询渲染目标的大小。
注意：从主线程视角，值是异步可用的，因为当渲染在渲染线程上时，值会发生变化。这意味着该属性主要适用于QML绑定。应用代码不应假设`QQuickRhiItem`对象构建时该值已是最新的。
这是一个只读属性。

**如何使用：** 调用 `effectiveColorBufferSize()` 读取当前值；它不会修改应用状态。

### `fixedColorBufferHeight : int`

**作用与语义：**

物品相关纹理的固定高度（像素数）。当需要固定纹理大小且不依赖于物品大小时，这很重要。该尺寸不影响物品的几何体（大小和场景中的位置），这意味着纹理内容会被拉伸（放大）或缩小到物品区域。
默认值为`0`。值为0表示纹理大小跟随物品大小。（`texture size` = `item size` * `device pixel ratio`）。
有关设置固定宽度和高度的使用场景，请参见 `fixedColorBufferWidth`。

**如何使用：** 调用 `fixedColorBufferHeight()` 读取当前值；它不会修改应用状态。

### `fixedColorBufferWidth : int`

**作用与语义：**

物品关联纹理或渲染缓冲区的固定宽度（像素数）。当需要固定颜色缓冲大小且不依赖于物品大小时，这很重要。该大小不影响物品的几何体（大小和场景中的位置），这意味着纹理内容会被拉伸（放大）或缩小到物品区域。
例如，将尺寸设置为正好是物品（像素）大小的两倍，实际上执行了2倍超采样（渲染为分辨率的两倍，然后在对应场景中的元素四边形进行纹理时隐式缩放）。另一方面，将尺寸设置为物品像素大小的一半，实际上实现了以半分辨率渲染并放大结果。
默认情况下，该值为`0`。值为0表示纹理的大小与物品的大小相符。（`texture size` = `item size` * `device pixel ratio`）。
注意：设备像素比率（系统合成器的比例因子）对性能影响很大，因为比例因子为2（200%）意味着渲染分辨率是开发者和UI设计师感知的两倍，然后实际上将内容缩放，类似于在设备像素比为1的系统中将该属性设置为像素大小的两倍。因此，该属性很少用于大于物品像素尺寸的尺寸，因为许多现代桌面系统既不需要也没有性能预算，而系统本来就使用大于1的设备像素比例。相反，该属性的主要用途是设置更小的尺寸，以实现合理的小分辨率渲染，而不是盲目遵循物品（或许是窗口）几何体，无论其多大。

**如何使用：** 调用 `fixedColorBufferWidth()` 读取当前值；它不会修改应用状态。

### `mirrorVertically : bool`

**作用与语义：**

该属性控制绘制纹理四边形时纹理 UV 是否翻转。它不影响幕外色彩缓冲区的内容和`QQuickRhiItemRenderer`实现的渲染。
默认数值为`false`。

**如何使用：** 调用 `mirrorVertically()` 读取当前值；它不会修改应用状态。

### `sampleCount : int`

**作用与语义：**

该属性控制多采样抗锯齿的采样计数。默认值为`1`，这意味着MSAA被禁用。
有效值为1、4、8，有时还有16和32。`QRhi::supportedSampleCounts()`可用于运行时查询支持的样本计数，但通常应用程序应请求1（无MSAA）、4x（正常MSAA）或8x（高MSAA）。
注意：设置新值意味着渲染器创建的所有`QRhiGraphicsPipeline`对象此后必须使用相同的采样计数。现有的采样计数不同`QRhiGraphicsPipeline`对象不得再使用。当值变化时，所有颜色和深度模板缓冲区将被销毁并自动重建，`initialize()`会再次调用。然而，当`isAutoRenderTargetEnabled()` `false`时，是否管理深度模板缓冲区或额外的颜色缓冲区，则由应用程序自行管理。
将样本计数从默认的1改为更高的值意味着`colorTexture()`变为`nullptr`，`msaaColorBuffer()`开始返回有效对象。切回1（或0）则意味着相反：在下一次初始化调用中，msaaColorBuffer() 会返回`nullptr`，而colorTexture()则再次有效。此外，当样本数大于1（即使用MSAA）时，`resolveTexture()`返回有效（非多重采样）`QRhiTexture`。

**如何使用：** 调用 `sampleCount()` 读取当前值；它不会修改应用状态。

### `[explicit] QQuickRhiItem::QQuickRhiItem(QQuickItem *parent = nullptr)`

**作用与语义：**

构造一个带有给定`parent`的新QQuickRhiItem。

### `[override virtual noexcept] QQuickRhiItem::~QQuickRhiItem()`

**作用与语义：**

毁灭者。

### `[pure virtual protected] QQuickRhiItemRenderer *QQuickRhiItem::createRenderer()`

**作用与语义：**

重新实现该函数以创建并返回一个新的 `QQuickRhiItemRenderer` 子类实例。
在GUI线程被阻塞时，该函数会在渲染线程上被调用。

### `[override virtual protected] bool QQuickRhiItem::event(QEvent *e)`

**作用与语义：**

重装：`QQuickItem::event`（QEvent *ev）。

### `[override virtual protected] void QQuickRhiItem::geometryChange(const QRectF &newGeometry, const QRectF &oldGeometry)`

**作用与语义：**

重实现自：`QQuickItem::geometryChange`（QRectF 和 newGeometry 固有，QRectF 和 oldGeometry 固有）。
该函数用于处理该项几何体从`oldGeometry`到`newGeometry`的变化。如果两个几何体相同，则不会产生任何处理。
派生类必须在其实现中调用基类方法。

### `[protected] bool QQuickRhiItem::isAutoRenderTargetEnabled() const`

**作用与语义：**

返回当前自动深度模板缓冲区和渲染目标管理设置。
默认情况下，这个数值是`true`。

### `[override virtual] bool QQuickRhiItem::isTextureProvider() const`

**作用与语义：**

重装：`QQuickItem::isTextureProvider()` const.
如果该项是纹理提供者，则返回 true。默认实现返回 false。
该函数可以从任何线程调用。

### `[override virtual protected] void QQuickRhiItem::releaseResources()`

**作用与语义：**

重装：`QQuickItem::releaseResources()`。
当某个项目需要释放尚未由`QQuickItem::updatePaintNode()`返回节点管理的图形资源时，调用该函数。
当该项即将从之前渲染的窗口中移除时，就会发生这种情况。当调用该函数时，该项必定会有`window`。
该函数在图形界面线程中被调用，渲染线程的状态（使用时）未知。对象不应直接删除，而应通过`QQuickWindow::scheduleRenderJob()`调度进行清理。

### `[protected] void QQuickRhiItem::setAutoRenderTarget(bool enabled)`

**作用与语义：**

控制深度模板`QRhiRenderBuffer`和`QRhiTextureRenderTarget`是否由该项目自动创建和维护。默认值为`true`。早期调用该函数，例如从派生类的构造函数调用，`enabled`设为`false`以禁用此功能。
在自动模式下，深度模板缓冲区的大小和采样数遵循颜色缓冲贴图的设置。在非自动模式下，renderTarget() 和 depthStencilBuffer() 总是返回 `nullptr`，随后由应用程序的 initialize() 实现来设置和管理这些对象。

### `[override virtual] QSGTextureProvider *QQuickRhiItem::textureProvider() const`

**作用与语义：**

重实现自：`QQuickItem::textureProvider()` const.
返回某个物品的纹理提供者。默认实现返回`nullptr`。
该函数只能在渲染线程中调用。

### `bool alphaBlending() const`

**作用与语义：**

如果在绘制四边形时，控制键总是启用，并贴图由`QQuickRhiItem`及其渲染器生成的内容。
默认值为`false`。这是为了性能考虑：如果不涉及半透明，因为`QQuickRhiItemRenderer`会变成不透明的颜色，且从不渲染alpha小于1的片段，那么启用混合就没有意义。
如果`QQuickRhiItemRenderer`子类渲染时涉及半透明，则将该属性设为 true。
注意：在某些条件下，无论该属性的值如何，混合仍然会发生。例如，如果项的`opacity`（更准确地说，是从父链继承的总不透明度）小于1，即使该属性设置为false，混合仍会自动被启用。
注意：Qt Quick 场景图依赖并预期预先乘以 alpha 值。例如，如果意图是将渲染器背景清除到 alpha 值 0.5，则确保将红、绿、蓝的清晰色彩值乘以 0.5。否则混合结果将不正确。

**如何使用：** 调用 `alphaBlending()` 读取当前值；它不会修改应用状态。

### `QQuickRhiItem::TextureFormat colorBufferFormat() const`

**作用与语义：**

该属性控制用作颜色缓冲区的纹理格式。默认值为`TextureFormat::RGBA8`。`QQuickRhiItem`支持渲染到`QRhiTexture`支持的部分格式。仅应指定`QRhi::isTextureFormatSupported()`报告支持的格式，否则渲染无法正常工作。
注意：当物品及其渲染器已经初始化并渲染完毕，设置新格式意味着渲染器创建的所有`QRhiGraphicsPipeline`对象都可能无法使用，如果相关`QRhiRenderPassDescriptor`因不同的纹理格式而变得不兼容。类似于动态更改`sampleCount`，这意味着initialize()或render()实现必须同时发布现有管线并创建新的管线。

**如何使用：** 调用 `colorBufferFormat()` 读取当前值；它不会修改应用状态。

### `QSize effectiveColorBufferSize() const`

**作用与语义：**

该属性揭示了底层颜色缓冲区（`QRhiTexture`或`QRhiRenderBuffer`）的像素大小。该特性供用户在GUI（主线程）中使用，通过QML绑定或JavaScript。
注意：`QQuickRhiItemRenderer`实现在场景图渲染线程上运行时，不应使用该属性。这些实现应当查询渲染目标的大小。
注意：从主线程视角，值是异步可用的，因为当渲染在渲染线程上时，值会发生变化。这意味着该属性主要适用于QML绑定。应用代码不应假设`QQuickRhiItem`对象构建时该值已是最新的。
这是一个只读属性。

**如何使用：** 调用 `effectiveColorBufferSize()` 读取当前值；它不会修改应用状态。

### `int fixedColorBufferHeight() const`

**作用与语义：**

物品相关纹理的固定高度（像素数）。当需要固定纹理大小且不依赖于物品大小时，这很重要。该尺寸不影响物品的几何体（大小和场景中的位置），这意味着纹理内容会被拉伸（放大）或缩小到物品区域。
默认值为`0`。值为0表示纹理大小跟随物品大小。（`texture size` = `item size` * `device pixel ratio`）。
有关设置固定宽度和高度的使用场景，请参见 `fixedColorBufferWidth`。

**如何使用：** 调用 `fixedColorBufferHeight()` 读取当前值；它不会修改应用状态。

### `int fixedColorBufferWidth() const`

**作用与语义：**

物品关联纹理或渲染缓冲区的固定宽度（像素数）。当需要固定颜色缓冲大小且不依赖于物品大小时，这很重要。该大小不影响物品的几何体（大小和场景中的位置），这意味着纹理内容会被拉伸（放大）或缩小到物品区域。
例如，将尺寸设置为正好是物品（像素）大小的两倍，实际上执行了2倍超采样（渲染为分辨率的两倍，然后在对应场景中的元素四边形进行纹理时隐式缩放）。另一方面，将尺寸设置为物品像素大小的一半，实际上实现了以半分辨率渲染并放大结果。
默认情况下，该值为`0`。值为0表示纹理的大小与物品的大小相符。（`texture size` = `item size` * `device pixel ratio`）。
注意：设备像素比率（系统合成器的比例因子）对性能影响很大，因为比例因子为2（200%）意味着渲染分辨率是开发者和UI设计师感知的两倍，然后实际上将内容缩放，类似于在设备像素比为1的系统中将该属性设置为像素大小的两倍。因此，该属性很少用于大于物品像素尺寸的尺寸，因为许多现代桌面系统既不需要也没有性能预算，而系统本来就使用大于1的设备像素比例。相反，该属性的主要用途是设置更小的尺寸，以实现合理的小分辨率渲染，而不是盲目遵循物品（或许是窗口）几何体，无论其多大。

**如何使用：** 调用 `fixedColorBufferWidth()` 读取当前值；它不会修改应用状态。

### `bool isMirrorVerticallyEnabled() const`

**作用与语义：**

该属性控制绘制纹理四边形时纹理 UV 是否翻转。它不影响幕外色彩缓冲区的内容和`QQuickRhiItemRenderer`实现的渲染。
默认数值为`false`。

**如何使用：** 调用 `isMirrorVerticallyEnabled()` 读取当前值；它不会修改应用状态。

### `int sampleCount() const`

**作用与语义：**

该属性控制多采样抗锯齿的采样计数。默认值为`1`，这意味着MSAA被禁用。
有效值为1、4、8，有时还有16和32。`QRhi::supportedSampleCounts()`可用于运行时查询支持的样本计数，但通常应用程序应请求1（无MSAA）、4x（正常MSAA）或8x（高MSAA）。
注意：设置新值意味着渲染器创建的所有`QRhiGraphicsPipeline`对象此后必须使用相同的采样计数。现有的采样计数不同`QRhiGraphicsPipeline`对象不得再使用。当值变化时，所有颜色和深度模板缓冲区将被销毁并自动重建，`initialize()`会再次调用。然而，当`isAutoRenderTargetEnabled()` `false`时，是否管理深度模板缓冲区或额外的颜色缓冲区，则由应用程序自行管理。
将样本计数从默认的1改为更高的值意味着`colorTexture()`变为`nullptr`，`msaaColorBuffer()`开始返回有效对象。切回1（或0）则意味着相反：在下一次初始化调用中，msaaColorBuffer() 会返回`nullptr`，而colorTexture()则再次有效。此外，当样本数大于1（即使用MSAA）时，`resolveTexture()`返回有效（非多重采样）`QRhiTexture`。

**如何使用：** 调用 `sampleCount()` 读取当前值；它不会修改应用状态。

### `void setAlphaBlending(bool enable)`

**作用与语义：**

如果在绘制四边形时，控制键总是启用，并贴图由`QQuickRhiItem`及其渲染器生成的内容。
默认值为`false`。这是为了性能考虑：如果不涉及半透明，因为`QQuickRhiItemRenderer`会变成不透明的颜色，且从不渲染alpha小于1的片段，那么启用混合就没有意义。
如果`QQuickRhiItemRenderer`子类渲染时涉及半透明，则将该属性设为 true。
注意：在某些条件下，无论该属性的值如何，混合仍然会发生。例如，如果项的`opacity`（更准确地说，是从父链继承的总不透明度）小于1，即使该属性设置为false，混合仍会自动被启用。
注意：Qt Quick 场景图依赖并预期预先乘以 alpha 值。例如，如果意图是将渲染器背景清除到 alpha 值 0.5，则确保将红、绿、蓝的清晰色彩值乘以 0.5。否则混合结果将不正确。

**如何使用：** 调用 `setAlphaBlending(...)` 修改 `alphaBlending`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setColorBufferFormat(QQuickRhiItem::TextureFormat format)`

**作用与语义：**

该属性控制用作颜色缓冲区的纹理格式。默认值为`TextureFormat::RGBA8`。`QQuickRhiItem`支持渲染到`QRhiTexture`支持的部分格式。仅应指定`QRhi::isTextureFormatSupported()`报告支持的格式，否则渲染无法正常工作。
注意：当物品及其渲染器已经初始化并渲染完毕，设置新格式意味着渲染器创建的所有`QRhiGraphicsPipeline`对象都可能无法使用，如果相关`QRhiRenderPassDescriptor`因不同的纹理格式而变得不兼容。类似于动态更改`sampleCount`，这意味着initialize()或render()实现必须同时发布现有管线并创建新的管线。

**如何使用：** 调用 `setColorBufferFormat(...)` 修改 `colorBufferFormat`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFixedColorBufferHeight(int height)`

**作用与语义：**

物品相关纹理的固定高度（像素数）。当需要固定纹理大小且不依赖于物品大小时，这很重要。该尺寸不影响物品的几何体（大小和场景中的位置），这意味着纹理内容会被拉伸（放大）或缩小到物品区域。
默认值为`0`。值为0表示纹理大小跟随物品大小。（`texture size` = `item size` * `device pixel ratio`）。
有关设置固定宽度和高度的使用场景，请参见 `fixedColorBufferWidth`。

**如何使用：** 调用 `setFixedColorBufferHeight(...)` 修改 `fixedColorBufferHeight`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFixedColorBufferWidth(int width)`

**作用与语义：**

物品关联纹理或渲染缓冲区的固定宽度（像素数）。当需要固定颜色缓冲大小且不依赖于物品大小时，这很重要。该大小不影响物品的几何体（大小和场景中的位置），这意味着纹理内容会被拉伸（放大）或缩小到物品区域。
例如，将尺寸设置为正好是物品（像素）大小的两倍，实际上执行了2倍超采样（渲染为分辨率的两倍，然后在对应场景中的元素四边形进行纹理时隐式缩放）。另一方面，将尺寸设置为物品像素大小的一半，实际上实现了以半分辨率渲染并放大结果。
默认情况下，该值为`0`。值为0表示纹理的大小与物品的大小相符。（`texture size` = `item size` * `device pixel ratio`）。
注意：设备像素比率（系统合成器的比例因子）对性能影响很大，因为比例因子为2（200%）意味着渲染分辨率是开发者和UI设计师感知的两倍，然后实际上将内容缩放，类似于在设备像素比为1的系统中将该属性设置为像素大小的两倍。因此，该属性很少用于大于物品像素尺寸的尺寸，因为许多现代桌面系统既不需要也没有性能预算，而系统本来就使用大于1的设备像素比例。相反，该属性的主要用途是设置更小的尺寸，以实现合理的小分辨率渲染，而不是盲目遵循物品（或许是窗口）几何体，无论其多大。

**如何使用：** 调用 `setFixedColorBufferWidth(...)` 修改 `fixedColorBufferWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMirrorVertically(bool enable)`

**作用与语义：**

该属性控制绘制纹理四边形时纹理 UV 是否翻转。它不影响幕外色彩缓冲区的内容和`QQuickRhiItemRenderer`实现的渲染。
默认数值为`false`。

**如何使用：** 调用 `setMirrorVertically(...)` 修改 `mirrorVertically`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSampleCount(int samples)`

**作用与语义：**

该属性控制多采样抗锯齿的采样计数。默认值为`1`，这意味着MSAA被禁用。
有效值为1、4、8，有时还有16和32。`QRhi::supportedSampleCounts()`可用于运行时查询支持的样本计数，但通常应用程序应请求1（无MSAA）、4x（正常MSAA）或8x（高MSAA）。
注意：设置新值意味着渲染器创建的所有`QRhiGraphicsPipeline`对象此后必须使用相同的采样计数。现有的采样计数不同`QRhiGraphicsPipeline`对象不得再使用。当值变化时，所有颜色和深度模板缓冲区将被销毁并自动重建，`initialize()`会再次调用。然而，当`isAutoRenderTargetEnabled()` `false`时，是否管理深度模板缓冲区或额外的颜色缓冲区，则由应用程序自行管理。
将样本计数从默认的1改为更高的值意味着`colorTexture()`变为`nullptr`，`msaaColorBuffer()`开始返回有效对象。切回1（或0）则意味着相反：在下一次初始化调用中，msaaColorBuffer() 会返回`nullptr`，而colorTexture()则再次有效。此外，当样本数大于1（即使用MSAA）时，`resolveTexture()`返回有效（非多重采样）`QRhiTexture`。

**如何使用：** 调用 `setSampleCount(...)` 修改 `sampleCount`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void alphaBlendingChanged()`

**作用与语义：**

如果在绘制四边形时，控制键总是启用，并贴图由`QQuickRhiItem`及其渲染器生成的内容。
默认值为`false`。这是为了性能考虑：如果不涉及半透明，因为`QQuickRhiItemRenderer`会变成不透明的颜色，且从不渲染alpha小于1的片段，那么启用混合就没有意义。
如果`QQuickRhiItemRenderer`子类渲染时涉及半透明，则将该属性设为 true。
注意：在某些条件下，无论该属性的值如何，混合仍然会发生。例如，如果项的`opacity`（更准确地说，是从父链继承的总不透明度）小于1，即使该属性设置为false，混合仍会自动被启用。
注意：Qt Quick 场景图依赖并预期预先乘以 alpha 值。例如，如果意图是将渲染器背景清除到 alpha 值 0.5，则确保将红、绿、蓝的清晰色彩值乘以 0.5。否则混合结果将不正确。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `alphaBlending` 的变化，不要把它当作普通函数主动调用。

### `void colorBufferFormatChanged()`

**作用与语义：**

该属性控制用作颜色缓冲区的纹理格式。默认值为`TextureFormat::RGBA8`。`QQuickRhiItem`支持渲染到`QRhiTexture`支持的部分格式。仅应指定`QRhi::isTextureFormatSupported()`报告支持的格式，否则渲染无法正常工作。
注意：当物品及其渲染器已经初始化并渲染完毕，设置新格式意味着渲染器创建的所有`QRhiGraphicsPipeline`对象都可能无法使用，如果相关`QRhiRenderPassDescriptor`因不同的纹理格式而变得不兼容。类似于动态更改`sampleCount`，这意味着initialize()或render()实现必须同时发布现有管线并创建新的管线。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `colorBufferFormat` 的变化，不要把它当作普通函数主动调用。

### `void effectiveColorBufferSizeChanged()`

**作用与语义：**

该属性揭示了底层颜色缓冲区（`QRhiTexture`或`QRhiRenderBuffer`）的像素大小。该特性供用户在GUI（主线程）中使用，通过QML绑定或JavaScript。
注意：`QQuickRhiItemRenderer`实现在场景图渲染线程上运行时，不应使用该属性。这些实现应当查询渲染目标的大小。
注意：从主线程视角，值是异步可用的，因为当渲染在渲染线程上时，值会发生变化。这意味着该属性主要适用于QML绑定。应用代码不应假设`QQuickRhiItem`对象构建时该值已是最新的。
这是一个只读属性。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `effectiveColorBufferSize` 的变化，不要把它当作普通函数主动调用。

### `void fixedColorBufferHeightChanged()`

**作用与语义：**

物品相关纹理的固定高度（像素数）。当需要固定纹理大小且不依赖于物品大小时，这很重要。该尺寸不影响物品的几何体（大小和场景中的位置），这意味着纹理内容会被拉伸（放大）或缩小到物品区域。
默认值为`0`。值为0表示纹理大小跟随物品大小。（`texture size` = `item size` * `device pixel ratio`）。
有关设置固定宽度和高度的使用场景，请参见 `fixedColorBufferWidth`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `fixedColorBufferHeight` 的变化，不要把它当作普通函数主动调用。

### `void fixedColorBufferWidthChanged()`

**作用与语义：**

物品关联纹理或渲染缓冲区的固定宽度（像素数）。当需要固定颜色缓冲大小且不依赖于物品大小时，这很重要。该大小不影响物品的几何体（大小和场景中的位置），这意味着纹理内容会被拉伸（放大）或缩小到物品区域。
例如，将尺寸设置为正好是物品（像素）大小的两倍，实际上执行了2倍超采样（渲染为分辨率的两倍，然后在对应场景中的元素四边形进行纹理时隐式缩放）。另一方面，将尺寸设置为物品像素大小的一半，实际上实现了以半分辨率渲染并放大结果。
默认情况下，该值为`0`。值为0表示纹理的大小与物品的大小相符。（`texture size` = `item size` * `device pixel ratio`）。
注意：设备像素比率（系统合成器的比例因子）对性能影响很大，因为比例因子为2（200%）意味着渲染分辨率是开发者和UI设计师感知的两倍，然后实际上将内容缩放，类似于在设备像素比为1的系统中将该属性设置为像素大小的两倍。因此，该属性很少用于大于物品像素尺寸的尺寸，因为许多现代桌面系统既不需要也没有性能预算，而系统本来就使用大于1的设备像素比例。相反，该属性的主要用途是设置更小的尺寸，以实现合理的小分辨率渲染，而不是盲目遵循物品（或许是窗口）几何体，无论其多大。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `fixedColorBufferWidth` 的变化，不要把它当作普通函数主动调用。

### `void mirrorVerticallyChanged()`

**作用与语义：**

该属性控制绘制纹理四边形时纹理 UV 是否翻转。它不影响幕外色彩缓冲区的内容和`QQuickRhiItemRenderer`实现的渲染。
默认数值为`false`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `mirrorVertically` 的变化，不要把它当作普通函数主动调用。

### `void sampleCountChanged()`

**作用与语义：**

该属性控制多采样抗锯齿的采样计数。默认值为`1`，这意味着MSAA被禁用。
有效值为1、4、8，有时还有16和32。`QRhi::supportedSampleCounts()`可用于运行时查询支持的样本计数，但通常应用程序应请求1（无MSAA）、4x（正常MSAA）或8x（高MSAA）。
注意：设置新值意味着渲染器创建的所有`QRhiGraphicsPipeline`对象此后必须使用相同的采样计数。现有的采样计数不同`QRhiGraphicsPipeline`对象不得再使用。当值变化时，所有颜色和深度模板缓冲区将被销毁并自动重建，`initialize()`会再次调用。然而，当`isAutoRenderTargetEnabled()` `false`时，是否管理深度模板缓冲区或额外的颜色缓冲区，则由应用程序自行管理。
将样本计数从默认的1改为更高的值意味着`colorTexture()`变为`nullptr`，`msaaColorBuffer()`开始返回有效对象。切回1（或0）则意味着相反：在下一次初始化调用中，msaaColorBuffer() 会返回`nullptr`，而colorTexture()则再次有效。此外，当样本数大于1（即使用MSAA）时，`resolveTexture()`返回有效（非多重采样）`QRhiTexture`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `sampleCount` 的变化，不要把它当作普通函数主动调用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

### 状态和错误边界

属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

### 线程边界

大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

### 最容易出现的错误

不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QQuickRhiItem` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
