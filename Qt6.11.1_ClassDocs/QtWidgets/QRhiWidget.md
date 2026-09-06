# QRhiWidget

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QRhiWidget` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QRhiWidget` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QRhiWidget>`
- 继承自：QWidget
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum class Api { Null, OpenGL, Metal, Vulkan, Direct3D11, Direct3D12 }`
- `enum class TextureFormat { RGBA8, RGBA16F, RGBA32F, RGB10A2 }`

### 属性

- `autoRenderTarget : bool`
- `colorBufferFormat : TextureFormat`
- `fixedColorBufferSize : QSize`
- `mirrorVertically : bool`
- `sampleCount : int`

### 公有函数

- `QRhiWidget(QWidget *parent = nullptr, Qt::WindowFlags f = {})`
- `virtual ~QRhiWidget() override`
- `QRhiWidget::Api api() const`
- `QRhiWidget::TextureFormat colorBufferFormat() const`
- `QSize fixedColorBufferSize() const`
- `QImage grabFramebuffer() const`
- `bool isDebugLayerEnabled() const`
- `bool isMirrorVerticallyEnabled() const`
- `int sampleCount() const`
- `void setApi(QRhiWidget::Api api)`
- `void setColorBufferFormat(QRhiWidget::TextureFormat format)`
- `void setDebugLayerEnabled(bool enable)`
- `void setFixedColorBufferSize(QSize pixelSize)`
- `void setFixedColorBufferSize(int w, int h)`
- `void setMirrorVertically(bool enabled)`
- `void setSampleCount(int samples)`

### 信号

- `void colorBufferFormatChanged(QRhiWidget::TextureFormat format)`
- `void fixedColorBufferSizeChanged(const QSize &pixelSize)`
- `void frameSubmitted()`
- `void mirrorVerticallyChanged(bool enabled)`
- `void renderFailed()`
- `void sampleCountChanged(int samples)`

### 保护函数

- `QRhiTexture * colorTexture() const`
- `QRhiRenderBuffer * depthStencilBuffer() const`
- `virtual void initialize(QRhiCommandBuffer *cb)`
- `QRhiRenderBuffer * msaaColorBuffer() const`
- `virtual void releaseResources()`
- `virtual void render(QRhiCommandBuffer *cb)`
- `QRhiRenderTarget * renderTarget() const`
- `QRhiTexture * resolveTexture() const`
- `QRhi * rhi() const`
- `void setAutoRenderTarget(bool enabled)`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`
- `virtual void paintEvent(QPaintEvent *e) override`
- `virtual void resizeEvent(QResizeEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QRhiWidget::Api`

**作用与语义：**

指定了3D API和`QRhi`后端的使用方式。
- `QRhiWidget::Api::Null`：`0`
- `QRhiWidget::Api::OpenGL`：`1`
- `QRhiWidget::Api::Metal`：`2`
- `QRhiWidget::Api::Vulkan`：`3`
- `QRhiWidget::Api::Direct3D11`：`4`
- `QRhiWidget::Api::Direct3D12`：`5`

### `enum class QRhiWidget::TextureFormat`

**作用与语义：**

指定`QRhiWidget`渲染的纹理格式。
- `QRhiWidget::TextureFormat::RGBA8`：`0`;参见`QRhiTexture::RGBA8`。
- `QRhiWidget::TextureFormat::RGBA16F`：`1`;参见`QRhiTexture::RGBA16F`。
- `QRhiWidget::TextureFormat::RGBA32F`：`2`;参见`QRhiTexture::RGBA32F`。
- `QRhiWidget::TextureFormat::RGB10A2`：`3`;参见`QRhiTexture::RGB10A2`。

### `autoRenderTarget : bool`

**作用与语义：**

当前设置为自动深度模板缓冲和渲染目标维护。
默认值是`true`。

**如何使用：** 调用 `autoRenderTarget()` 读取当前值；它不会修改应用状态。

### `colorBufferFormat : TextureFormat`

**作用与语义：**

该属性控制用作颜色缓冲区的纹理（或渲染缓冲区）的纹理格式。默认值为`TextureFormat::RGBA8`。`QRhiWidget`支持渲染`QRhiTexture`支持的部分格式。仅应指定`QRhi::isTextureFormatSupported()`报告支持的格式，否则渲染无法正常工作。
注意：当控件已经初始化并渲染完成时设置新格式，意味着渲染器创建的所有`QRhiGraphicsPipeline`对象都可能变得不可用，因为相关`QRhiRenderPassDescriptor`因不同的纹理格式而变得不兼容。类似于动态更改`sampleCount`，这意味着`initialize()`或`render()`实现必须同时发布现有的管线并创建新的。

**如何使用：** 调用 `colorBufferFormat()` 读取当前值；它不会修改应用状态。

### `fixedColorBufferSize : QSize`

**作用与语义：**

`QRhiWidget`对应纹理的固定像素大小。当需要固定纹理大小且不依赖于控件大小时，这很重要。该尺寸不影响控件的几何体（其在顶层窗口中的大小和位置），这意味着纹理内容会被拉伸（放大）或缩小到控件区域。
例如，将大小设置为小部件（像素）大小的两倍，实际上执行了2倍超采样（先以两倍分辨率渲染，然后在对应小部件的四边形进行贴图时隐式缩放）。另一方面，将大小设置为小部件大小的一半，实际上实现了半分辨率渲染，然后对结果进行放大。
默认情况下，该值为空`QSize`。空`QSize`表示纹理大小与`QRhiWidget`大小相符。（`texture size` = `widget size` * `device pixel ratio`）。
注意：设备像素比率（系统合成器的缩放因子）对性能有很大影响，因为缩放因子为2（200%）意味着渲染分辨率是开发者和UI设计师感知到的两倍，然后实际上将内容缩放，类似于在设备像素比为1的系统中将该属性设置为小部件像素大小的两倍。因此，该特性很少用于大于小部件像素大小的尺寸，因为许多现代桌面系统既没有需求，也没有性能预算，而系统本来就使用大于1的设备像素比例。相反，该属性的主要用途是设置较小的尺寸，以实现合理的分辨率渲染，而不是盲目遵循窗口几何体，无论窗口多大。

**如何使用：** 调用 `fixedColorBufferSize()` 读取当前值；它不会修改应用状态。

### `mirrorVertically : bool`

**作用与语义：**

启用时，在顶层窗口中将`QRhiWidget`的背板纹理与其他控件内容合成时，会将图像绕X轴翻转。
默认数值为`false`。

**如何使用：** 调用 `mirrorVertically()` 读取当前值；它不会修改应用状态。

### `sampleCount : int`

**作用与语义：**

该属性控制多采样抗锯齿的采样计数。默认值为`1`，这意味着MSAA被禁用。
有效值为1、4、8，有时还有16和32。`QRhi::supportedSampleCounts()`可用于运行时查询支持的样本计数，但通常应用程序应请求1（无MSAA）、4x（正常MSAA）或8x（高MSAA）。
注意：设置新值意味着渲染器创建的所有`QRhiGraphicsPipeline`对象此后必须使用相同的采样计数。使用不同采样计数创建的现有`QRhiGraphicsPipeline`对象不得再使用。当值变更时，所有颜色和深度模板缓冲区会自动被销毁并重新创建，`initialize()`会再次调用。然而，当`autoRenderTarget` `false`时，是否管理深度模板缓冲区或额外的颜色缓冲区将由应用程序自行管理。
将样本计数从默认1改为更高值意味着`colorTexture()`变为`nullptr`，`msaaColorBuffer()`开始返回有效对象。切回1（或0）则意味着相反：下一次调用`initialize()` `msaaColorBuffer()`返回`nullptr`，而`colorTexture()`再次有效。此外，当样本计数大于1（即使用MSAA）时，`resolveTexture()`返回有效的（非多重采样）`QRhiTexture`。

**如何使用：** 调用 `sampleCount()` 读取当前值；它不会修改应用状态。

### `[explicit] QRhiWidget::QRhiWidget(QWidget *parent = nullptr, Qt::WindowFlags f = {})`

**作用与语义：**

构建一个小部件，该小部件是`parent`的子节点，小部件标志设置为`f`。

### `[override virtual noexcept] QRhiWidget::~QRhiWidget()`

**作用与语义：**

毁灭者。

### `QRhiWidget::Api QRhiWidget::api() const`

**作用与语义：**

返回当前设置的图形API（`QRhi`后端）。

### `[protected] QRhiTexture *QRhiWidget::colorTexture() const`

**作用与语义：**

返回纹理，作为控件的颜色缓冲。
只能在`initialize()`和`render()`中调用。
与深度模板缓冲区和`QRhiRenderTarget`不同，该纹理始终可用，由`QRhiWidget`管理，与`autoRenderTarget`值无关。
注意：当`sampleCount`大于1且启用多采样抗锯齿时，返回值为`nullptr`。相反，请通过调用`msaaColorBuffer()`查询`QRhiRenderBuffer`。
注意：背景纹理大小和采样计数也可以通过从`renderTarget()`返回的`QRhiRenderTarget`查询。这比从 `QRhiTexture` 或 `QRhiRenderBuffer`查询更方便、更紧凑，因为无论是否使用多重采样，它都能正常工作。

### `[protected] QRhiRenderBuffer *QRhiWidget::depthStencilBuffer() const`

**作用与语义：**

返回控件渲染时使用的深度模板缓冲区。
只能从`initialize()`和`render()`打电话。
仅在`autoRenderTarget`被`true`时可用。否则返回的值`nullptr`，需要重新实现`initialize()`来创建和管理深度模板缓冲区和`QRhiTextureRenderTarget`。

### `[override virtual protected] bool QRhiWidget::event(QEvent *e)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[signal] void QRhiWidget::frameSubmitted()`

**作用与语义：**

该信号是在小部件顶层窗口完成合成并提交一帧后发出的。

### `QImage QRhiWidget::grabFramebuffer() const`

**作用与语义：**

渲染一个新帧，读取纹理内容，然后返回为`QImage`。
当发生错误时，会返回一个空`QImage`。
返`QImage`的格式将根据`colorBufferFormat()`不同，分为`QImage::Format_RGBA8888`、`QImage::Format_RGBA16FPx4`、`QImage::Format_RGBA32FPx4`或`QImage::Format_BGR30`。
`QRhiWidget`不知道渲染器的混合和合成方法，因此无法知道输出中是否有预先在RGB颜色值中加了alpha。因此，即使合适的格式，`_Premultiplied` `QImage`格式也不会用于返回的`QImage`。调用者可以根据自己的意愿重新解释结果数据。
注意：当`QRhiWidget`未添加到属于屏幕顶层窗口的小部件层级时，也可以调用该函数。这允许从3D渲染中生成画面。
该函数名为 grabFramebuffer()，以与 `QOpenGLWidget` 和 `QQuickWidget` 保持一致。它并不是从`QRhiWidget`内容中获取 CPU 端图像数据的唯一方式：调用`QRhiWidget`上的 `QWidget::grab()` 或其前身也是可行的（返回 `QPixmap`）。除了直接与 `QImage` 协作外，grabFramebuffer() 的另一个优点是性能可能略高一些，因为它无需经过`QWidget`基础设施的其他部分，可以立即触发渲染新帧并进行回读。

### `[virtual protected] void QRhiWidget::initialize(QRhiCommandBuffer *cb)`

**作用与语义：**

当控件首次初始化、相关纹理的大小、格式或采样计数发生变化，或`QRhi`和纹理因任何原因发生变化时调用。该函数预计维护（如果尚未创建则创建，大小变化时调整和重建）渲染代码在`render()`中使用的图形资源。
要查询`QRhi`、`QRhiTexture`及其他相关对象，调用`rhi()`、`colorTexture()`、`depthStencilBuffer()`和`renderTarget()`。
当控件大小变化时，`QRhi`对象、颜色缓冲纹理和深度模板缓冲对象都是相同的实例（因此获取者返回相同的指针），但颜色和深度/模板缓冲区很可能已经重建，这意味着`size`和底层的原生纹理资源可能与上次调用时不同。
重实现时还应准备，`QRhi`对象和颜色缓冲贴图在调用该函数之间可能会发生变化。一个特殊情况是，当对尚未显示的控件进行`grabFramebuffer()`，然后在顶层控件中显示该控件时，对象会有所不同。此时抓取会通过专用`QRhi`实现，随后在后续初始化()和`render()`调用中被顶层窗口关联的`QRhi`替换。另一种更常见的情况是控件被重新父级化，使其属于新的顶层窗口。在这种情况下，`QRhiWidget`管理的所有`QRhi`及相关资源在后续调用该函数时将与之前不同。因此，重要的是销毁所有由子类之前创建的`QRhi`资源，因为它们属于之前的`QRhi`，而这些资源不应再被控件使用。
当默认情况下`autoRenderTarget` `true`时，深度模板`QRhiRenderBuffer`和与`colorTexture()`（或`msaaColorBuffer()`）及深度模板缓冲区相关的`QRhiTextureRenderTarget`会自动创建和管理。initialize() 和 `render()` 的重实现可以通过 `depthStencilBuffer()` 和 `renderTarget()` 查询这些对象。当`autoRenderTarget`设置为`false`时，这些对象不再自动创建和管理。相反，initialize() 实现将自行创建缓冲区并根据需要设置渲染目标。在手动管理渲染目标的额外颜色或深度模板附加时，其大小和采样数必须始终遵循 `colorTexture()` / `msaaColorBuffer()` 的大小和采样数，否则渲染或 3D API 验证时可能会出现错误。
子类创建的图形资源预计会在子类的解构器实现中发布。
`cb` 是该控件当前帧的 `QRhiCommandBuffer`。该函数在记录帧时调用，但没有主动渲染通道。命令缓冲区主要是为了允许在不依赖 `render()` 的情况下进行资源队列更新。

### `bool QRhiWidget::isDebugLayerEnabled() const`

**作用与语义：**

如果将请求调试层或验证层（若适用于所用图形API），则返回true。

### `[protected] QRhiRenderBuffer *QRhiWidget::msaaColorBuffer() const`

**作用与语义：**

返回渲染缓冲区，作为控件的多重采样颜色缓冲区。
只能在`initialize()`和`render()`中调用。
当`sampleCount`大于1，并启用多重采样抗取样时，返回的`QRhiRenderBuffer`具有匹配的采样计数，并作为颜色缓冲区。用于渲染到该缓冲区的图形管线必须使用相同的采样计数创建，深度模板缓冲区的采样计数也必须匹配。多采样内容预计会被解析为从`resolveTexture()`返回的纹理。当`autoRenderTarget` `true`时，`renderTarget()`会自动设置，方法是将 msaaColorBuffer() 设置为颜色附件 0 的`renderbuffer`，`resolveTexture()` 作为其`resolveTexture`。
当MSAA未被使用时，返回值`nullptr`。那就用`colorTexture()`吧。
根据底层的3D图形API，多采样纹理和采样计数大于1的颜色渲染缓冲区之间可能没有实际区别（`QRhi`两者可能直接映射到相同的本地资源类型）。不过，一些较早的API可能会区分纹理和渲染缓冲区。为了支持OpenGL ES 3.0，在多采样渲染缓冲区可用但多采样纹理不存在的情况下，`QRhiWidget`总是通过使用多采样`QRhiRenderBuffer`作为颜色附件来执行MSAA（从不使用多采样`QRhiTexture`）。
注意：背面纹理的大小和采样数也可以通过从`renderTarget()`返回的`QRhiRenderTarget`查询。这比从 `QRhiTexture` 或 `QRhiRenderBuffer`查询更方便、更简洁，因为无论是否使用多重采样，它都能正常工作。

### `[override virtual protected] void QRhiWidget::paintEvent(QPaintEvent *e)`

**作用与语义：**

重新实现: `QWidget::paintEvent`(QPaintEvent *event)。
处理绘制事件。
调用 `QWidget::update()` 将导致发送绘制事件 `e`，从而调用此函数。事件的发送是异步的，并将在从 `update()` 返回后某个时间发生。然后，此函数将在进行一些准备工作后调用虚函数 `render()` 来更新 `QRhiWidget` 关联纹理的内容。小部件的顶级窗口随后将把纹理与窗口的其余部分合成。
可以在子类中重新实现此事件处理程序，以接收传入的 `event` 的绘制事件。
绘制事件是请求重绘小部件的全部或部分内容。它可能因以下原因之一发生:
- 调用了 `repaint()` 或 `update()`，
- 小部件被遮挡后现在又被揭开，或
- 其他许多原因。
许多小部件在被请求时可以简单地重绘整个表面，但一些运行缓慢的小部件需要通过仅绘制请求区域来优化: `QPaintEvent::region()`。此速度优化并不改变结果，因为绘制将在事件处理中被裁剪到该区域。例如，`QListView` 和 `QTableView` 就是这样做的。
Qt 还试图通过将多个绘制事件合并为一个来加快绘制速度。当多次调用 `update()` 或窗口系统发送多个绘制事件时，Qt 会将这些事件合并为一个具有更大区域的事件（参见 `QRegion::united()`）。`repaint()` 函数不允许这种优化，因此我们建议在可能的情况下使用 `update()`。
当绘制事件发生时，更新区域通常已被擦除，因此你是在小部件的背景上进行绘制。
背景可以使用 `setBackgroundRole()` 和 `setPalette()` 设置。
自 Qt 4.0 起，`QWidget` 自动对其绘制进行双缓冲，因此无需在 paintEvent() 中编写双缓冲代码来避免闪烁。
注意: 通常，你应避免在 paintEvent() 内调用 `update()` 或 `repaint()`。例如，在 paintEvent() 中对子对象调用 `update()` 或 `repaint()` 会导致未定义行为；子对象可能会或可能不会接收绘制事件。
警告: 如果使用没有 Qt 背景存储的自定义绘制引擎，必须设置 `Qt::WA_PaintOnScreen`。否则，`QWidget::paintEngine()` 将不会被调用；而是将使用背景存储。

### `[virtual protected] void QRhiWidget::releaseResources()`

**作用与语义：**

当需要提前释放图形资源时调用。 这通常不会发生在被添加到顶层小部件子层级中并随后在其生命周期及顶层小部件的生命周期内保持不变的 `QRhiWidget` 上。因此在许多情况下无需重新实现此函数，例如应用程序始终只有一个顶层小部件（本地窗口）。然而，当涉及小部件（或其祖先）的重新父化时，在健壮且编写良好的 `QRhiWidget` 子类中重新实现此函数将变得必要。 当调用此函数时，期望实现销毁所有 `QRhi` 资源（`QRhiBuffer`、`QRhiTexture` 等对象），类似于析构函数中应执行的操作。同时还需要将其置空、使用智能指针或设置 `resources-invalid` 标志，因为 `initialize()` 最终会在之后被调用。但是请注意，将资源释放延迟到随后的 `initialize()` 是错误的。如果调用此函数，则必须在返回之前释放资源。还应注意，实现此函数并不能替代类析构函数（或智能指针）：图形资源仍必须在两者中释放。 请参见 Cube RHI Widget 示例以查看此功能的实际应用。在那里，切换 `QRhiWidget` 在作为子小部件（由于有父小部件）和作为顶层小部件（由于无父小部件）之间的按钮，会在 `QRhiWidget` 生命周期内触发调用此函数，因为相关的顶层小部件、本地窗口和 `QRhi` 都会发生变化，之前使用的 `QRhi` 被销毁，这意味着仍然存活的 `QRhiWidget` 所管理的相关资源被提前释放。 另一种调用此函数的情况是，当 `grabFramebuffer()` 与未添加到可见窗口的 `QRhiWidget` 一起使用时，即渲染在屏幕外进行。如果之后此 `QRhiWidget` 变为可见，或被添加到可见的小部件层级中，相关 `QRhi` 将从用于屏幕外渲染的临时资源更改为窗口的专用资源，从而触发此函数。

### `[virtual protected] void QRhiWidget::render(QRhiCommandBuffer *cb)`

**作用与语义：**

当小部件内容（即纹理内容）需要更新时调用。 在调用此函数之前，始终至少会调用一次 `initialize()`。 要请求更新，请调用 `QWidget::update()`。在 render() 内调用 `update()` 将导致持续更新，并由垂直同步进行节流。 `cb` 是小部件当前帧的 `QRhiCommandBuffer`。该函数在录制帧期间被调用，但没有活动的渲染过程。

### `[signal] void QRhiWidget::renderFailed()`

**作用与语义：**

每当小部件应渲染到其背后纹理时（无论是由于小部件更新还是调用`grabFramebuffer()`），但小部件没有可用的`QRhi`，可能是与图形配置相关的问题。
当出现问题时，该信号可能会多次发出。不要假设它只发出一次。如果错误处理代码只通知一次，请与`Qt::SingleShotConnection`连接。

### `[protected] QRhiRenderTarget *QRhiWidget::renderTarget() const`

**作用与语义：**

返回必须与`QRhiCommandBuffer::beginPass()`一起在`render()`实现中使用渲染目标对象。
只能从`initialize()`和`render()`打电话。
仅在`autoRenderTarget`被`true`时可用。否则返回的值`nullptr`需重新实现`initialize()`来创建和管理深度模板缓冲区和`QRhiTextureRenderTarget`。
创建图形流水线时需要`QRhiRenderPassDescriptor`。可以通过调用`renderPassDescriptor()`从返回的`QRhiTextureRenderTarget`查询。

### `[override virtual protected] void QRhiWidget::resizeEvent(QResizeEvent *e)`

**作用与语义：**

重实现自：`QWidget::resizeEvent`（QResizeEvent *event）。
处理传递在`e`事件参数中的事件大小调整。调用虚拟函数 `initialize()`。
注意：避免在派生类中覆盖该函数。如果不可行，确保调用`QRhiWidget`的实现。否则底层纹理对象和相关资源的大小无法正确调整，导致渲染错误。
该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件调整大小事件。当调用 resizeEvent() 时，控件已经拥有新的几何体。旧的大小可以通过 `QResizeEvent::oldSize()` 访问。
控件会被擦除，并在处理调整尺寸事件后立即接收绘图事件。不需要（也不应该）在这个处理程序中进行绘图。

### `[protected] QRhiTexture *QRhiWidget::resolveTexture() const`

**作用与语义：**

返回非多采样纹理，多采样内容被解析为该纹理。
当未启用多重采样抗锯齿时，结果会被`nullptr`。
只能从`initialize()`和`render()`打来。
启用MSAA时，该纹理会与屏幕上其他`QWidget`内容合成。然而，`QRhiWidget`的渲染必须针对从`msaaColorBuffer()`返回的（多重采样）`QRhiRenderBuffer`。当`autoRenderTarget`被`true`时，`renderTarget()`返回的`QRhiRenderTarget`会处理。否则，则由子类代码正确配置带有色彩缓冲和解析纹理的渲染目标对象。

### `[protected] QRhi *QRhiWidget::rhi() const`

**作用与语义：**

返回当前`QRhi`对象。
只能从`initialize()`和 `render()` 打电话。

### `void QRhiWidget::setApi(QRhiWidget::Api api)`

**作用与语义：**

设置图形API和`QRhi`后端的使用方式`api`。
警告：该函数必须在小部件加入小部件层级并显示之前足够早地调用。例如，目标是调用子类构造函数的函数。如果调用太晚，该函数将无效。
默认值取决于平台：macOS 和 iOS 用 Metal，Windows 用 Direct 3D 11，其他用 OpenGL。
该`api`只能为小部件及其顶层窗口设置一次，一旦设置完成并生效，窗口只能使用该 API 和`QRhi`后端进行渲染。尝试设置另一个值，或添加另一个带有不同`api`的 `QRhiWidget`，都无法正常工作。

### `[protected] void QRhiWidget::setAutoRenderTarget(bool enabled)`

**作用与语义：**

控件自动创建并维护深度模板`QRhiRenderBuffer`和`QRhiTextureRenderTarget`。默认值为`true`。
在自动模式下，深度模板缓冲区的大小和采样数会跟随颜色缓冲区纹理的设置。在非自动模式下，`renderTarget()`和`depthStencilBuffer()`总是返回`nullptr`，随后由应用程序对`initialize()`的实现来负责设置和管理这些对象。
调用该函数，`enabled` 设置为 `false` 的早期函数，例如在衍生类的构造函数中，以禁用自动模式。

### `void QRhiWidget::setDebugLayerEnabled(bool enable)`

**作用与语义：**

当 `enable` 为真时，请求底层图形 API 的调试或验证层。
警告：该函数必须在小部件加入小部件层级并显示之前足够早地调用。例如，目标是调用子类构造函数的函数。如果调用太晚，该函数将无效。
适用于Vulkan和直接3D。
默认情况下，这个功能是被禁用的。

### `QRhiWidget::TextureFormat colorBufferFormat() const`

**作用与语义：**

该属性控制用作颜色缓冲区的纹理（或渲染缓冲区）的纹理格式。默认值为`TextureFormat::RGBA8`。`QRhiWidget`支持渲染`QRhiTexture`支持的部分格式。仅应指定`QRhi::isTextureFormatSupported()`报告支持的格式，否则渲染无法正常工作。
注意：当控件已经初始化并渲染完成时设置新格式，意味着渲染器创建的所有`QRhiGraphicsPipeline`对象都可能变得不可用，因为相关`QRhiRenderPassDescriptor`因不同的纹理格式而变得不兼容。类似于动态更改`sampleCount`，这意味着`initialize()`或`render()`实现必须同时发布现有的管线并创建新的。

**如何使用：** 调用 `colorBufferFormat()` 读取当前值；它不会修改应用状态。

### `QSize fixedColorBufferSize() const`

**作用与语义：**

`QRhiWidget`对应纹理的固定像素大小。当需要固定纹理大小且不依赖于控件大小时，这很重要。该尺寸不影响控件的几何体（其在顶层窗口中的大小和位置），这意味着纹理内容会被拉伸（放大）或缩小到控件区域。
例如，将大小设置为小部件（像素）大小的两倍，实际上执行了2倍超采样（先以两倍分辨率渲染，然后在对应小部件的四边形进行贴图时隐式缩放）。另一方面，将大小设置为小部件大小的一半，实际上实现了半分辨率渲染，然后对结果进行放大。
默认情况下，该值为空`QSize`。空`QSize`表示纹理大小与`QRhiWidget`大小相符。（`texture size` = `widget size` * `device pixel ratio`）。
注意：设备像素比率（系统合成器的缩放因子）对性能有很大影响，因为缩放因子为2（200%）意味着渲染分辨率是开发者和UI设计师感知到的两倍，然后实际上将内容缩放，类似于在设备像素比为1的系统中将该属性设置为小部件像素大小的两倍。因此，该特性很少用于大于小部件像素大小的尺寸，因为许多现代桌面系统既没有需求，也没有性能预算，而系统本来就使用大于1的设备像素比例。相反，该属性的主要用途是设置较小的尺寸，以实现合理的分辨率渲染，而不是盲目遵循窗口几何体，无论窗口多大。

**如何使用：** 调用 `fixedColorBufferSize()` 读取当前值；它不会修改应用状态。

### `bool isMirrorVerticallyEnabled() const`

**作用与语义：**

启用时，在顶层窗口中将`QRhiWidget`的背板纹理与其他控件内容合成时，会将图像绕X轴翻转。
默认数值为`false`。

**如何使用：** 调用 `isMirrorVerticallyEnabled()` 读取当前值；它不会修改应用状态。

### `int sampleCount() const`

**作用与语义：**

该属性控制多采样抗锯齿的采样计数。默认值为`1`，这意味着MSAA被禁用。
有效值为1、4、8，有时还有16和32。`QRhi::supportedSampleCounts()`可用于运行时查询支持的样本计数，但通常应用程序应请求1（无MSAA）、4x（正常MSAA）或8x（高MSAA）。
注意：设置新值意味着渲染器创建的所有`QRhiGraphicsPipeline`对象此后必须使用相同的采样计数。使用不同采样计数创建的现有`QRhiGraphicsPipeline`对象不得再使用。当值变更时，所有颜色和深度模板缓冲区会自动被销毁并重新创建，`initialize()`会再次调用。然而，当`autoRenderTarget` `false`时，是否管理深度模板缓冲区或额外的颜色缓冲区将由应用程序自行管理。
将样本计数从默认1改为更高值意味着`colorTexture()`变为`nullptr`，`msaaColorBuffer()`开始返回有效对象。切回1（或0）则意味着相反：下一次调用`initialize()` `msaaColorBuffer()`返回`nullptr`，而`colorTexture()`再次有效。此外，当样本计数大于1（即使用MSAA）时，`resolveTexture()`返回有效的（非多重采样）`QRhiTexture`。

**如何使用：** 调用 `sampleCount()` 读取当前值；它不会修改应用状态。

### `void setColorBufferFormat(QRhiWidget::TextureFormat format)`

**作用与语义：**

该属性控制用作颜色缓冲区的纹理（或渲染缓冲区）的纹理格式。默认值为`TextureFormat::RGBA8`。`QRhiWidget`支持渲染`QRhiTexture`支持的部分格式。仅应指定`QRhi::isTextureFormatSupported()`报告支持的格式，否则渲染无法正常工作。
注意：当控件已经初始化并渲染完成时设置新格式，意味着渲染器创建的所有`QRhiGraphicsPipeline`对象都可能变得不可用，因为相关`QRhiRenderPassDescriptor`因不同的纹理格式而变得不兼容。类似于动态更改`sampleCount`，这意味着`initialize()`或`render()`实现必须同时发布现有的管线并创建新的。

**如何使用：** 调用 `setColorBufferFormat(...)` 修改 `colorBufferFormat`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFixedColorBufferSize(QSize pixelSize)`

**作用与语义：**

`QRhiWidget`对应纹理的固定像素大小。当需要固定纹理大小且不依赖于控件大小时，这很重要。该尺寸不影响控件的几何体（其在顶层窗口中的大小和位置），这意味着纹理内容会被拉伸（放大）或缩小到控件区域。
例如，将大小设置为小部件（像素）大小的两倍，实际上执行了2倍超采样（先以两倍分辨率渲染，然后在对应小部件的四边形进行贴图时隐式缩放）。另一方面，将大小设置为小部件大小的一半，实际上实现了半分辨率渲染，然后对结果进行放大。
默认情况下，该值为空`QSize`。空`QSize`表示纹理大小与`QRhiWidget`大小相符。（`texture size` = `widget size` * `device pixel ratio`）。
注意：设备像素比率（系统合成器的缩放因子）对性能有很大影响，因为缩放因子为2（200%）意味着渲染分辨率是开发者和UI设计师感知到的两倍，然后实际上将内容缩放，类似于在设备像素比为1的系统中将该属性设置为小部件像素大小的两倍。因此，该特性很少用于大于小部件像素大小的尺寸，因为许多现代桌面系统既没有需求，也没有性能预算，而系统本来就使用大于1的设备像素比例。相反，该属性的主要用途是设置较小的尺寸，以实现合理的分辨率渲染，而不是盲目遵循窗口几何体，无论窗口多大。

**如何使用：** 调用 `setFixedColorBufferSize(...)` 修改 `fixedColorBufferSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFixedColorBufferSize(int w, int h)`

**作用与语义：**

`QRhiWidget`对应纹理的固定像素大小。当需要固定纹理大小且不依赖于控件大小时，这很重要。该尺寸不影响控件的几何体（其在顶层窗口中的大小和位置），这意味着纹理内容会被拉伸（放大）或缩小到控件区域。
例如，将大小设置为小部件（像素）大小的两倍，实际上执行了2倍超采样（先以两倍分辨率渲染，然后在对应小部件的四边形进行贴图时隐式缩放）。另一方面，将大小设置为小部件大小的一半，实际上实现了半分辨率渲染，然后对结果进行放大。
默认情况下，该值为空`QSize`。空`QSize`表示纹理大小与`QRhiWidget`大小相符。（`texture size` = `widget size` * `device pixel ratio`）。
注意：设备像素比率（系统合成器的缩放因子）对性能有很大影响，因为缩放因子为2（200%）意味着渲染分辨率是开发者和UI设计师感知到的两倍，然后实际上将内容缩放，类似于在设备像素比为1的系统中将该属性设置为小部件像素大小的两倍。因此，该特性很少用于大于小部件像素大小的尺寸，因为许多现代桌面系统既没有需求，也没有性能预算，而系统本来就使用大于1的设备像素比例。相反，该属性的主要用途是设置较小的尺寸，以实现合理的分辨率渲染，而不是盲目遵循窗口几何体，无论窗口多大。

**如何使用：** 调用 `setFixedColorBufferSize(...)` 修改 `fixedColorBufferSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMirrorVertically(bool enabled)`

**作用与语义：**

启用时，在顶层窗口中将`QRhiWidget`的背板纹理与其他控件内容合成时，会将图像绕X轴翻转。
默认数值为`false`。

**如何使用：** 调用 `setMirrorVertically(...)` 修改 `mirrorVertically`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSampleCount(int samples)`

**作用与语义：**

该属性控制多采样抗锯齿的采样计数。默认值为`1`，这意味着MSAA被禁用。
有效值为1、4、8，有时还有16和32。`QRhi::supportedSampleCounts()`可用于运行时查询支持的样本计数，但通常应用程序应请求1（无MSAA）、4x（正常MSAA）或8x（高MSAA）。
注意：设置新值意味着渲染器创建的所有`QRhiGraphicsPipeline`对象此后必须使用相同的采样计数。使用不同采样计数创建的现有`QRhiGraphicsPipeline`对象不得再使用。当值变更时，所有颜色和深度模板缓冲区会自动被销毁并重新创建，`initialize()`会再次调用。然而，当`autoRenderTarget` `false`时，是否管理深度模板缓冲区或额外的颜色缓冲区将由应用程序自行管理。
将样本计数从默认1改为更高值意味着`colorTexture()`变为`nullptr`，`msaaColorBuffer()`开始返回有效对象。切回1（或0）则意味着相反：下一次调用`initialize()` `msaaColorBuffer()`返回`nullptr`，而`colorTexture()`再次有效。此外，当样本计数大于1（即使用MSAA）时，`resolveTexture()`返回有效的（非多重采样）`QRhiTexture`。

**如何使用：** 调用 `setSampleCount(...)` 修改 `sampleCount`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void colorBufferFormatChanged(QRhiWidget::TextureFormat format)`

**作用与语义：**

该属性控制用作颜色缓冲区的纹理（或渲染缓冲区）的纹理格式。默认值为`TextureFormat::RGBA8`。`QRhiWidget`支持渲染`QRhiTexture`支持的部分格式。仅应指定`QRhi::isTextureFormatSupported()`报告支持的格式，否则渲染无法正常工作。
注意：当控件已经初始化并渲染完成时设置新格式，意味着渲染器创建的所有`QRhiGraphicsPipeline`对象都可能变得不可用，因为相关`QRhiRenderPassDescriptor`因不同的纹理格式而变得不兼容。类似于动态更改`sampleCount`，这意味着`initialize()`或`render()`实现必须同时发布现有的管线并创建新的。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `colorBufferFormat` 的变化，不要把它当作普通函数主动调用。

### `void fixedColorBufferSizeChanged(const QSize &pixelSize)`

**作用与语义：**

`QRhiWidget`对应纹理的固定像素大小。当需要固定纹理大小且不依赖于控件大小时，这很重要。该尺寸不影响控件的几何体（其在顶层窗口中的大小和位置），这意味着纹理内容会被拉伸（放大）或缩小到控件区域。
例如，将大小设置为小部件（像素）大小的两倍，实际上执行了2倍超采样（先以两倍分辨率渲染，然后在对应小部件的四边形进行贴图时隐式缩放）。另一方面，将大小设置为小部件大小的一半，实际上实现了半分辨率渲染，然后对结果进行放大。
默认情况下，该值为空`QSize`。空`QSize`表示纹理大小与`QRhiWidget`大小相符。（`texture size` = `widget size` * `device pixel ratio`）。
注意：设备像素比率（系统合成器的缩放因子）对性能有很大影响，因为缩放因子为2（200%）意味着渲染分辨率是开发者和UI设计师感知到的两倍，然后实际上将内容缩放，类似于在设备像素比为1的系统中将该属性设置为小部件像素大小的两倍。因此，该特性很少用于大于小部件像素大小的尺寸，因为许多现代桌面系统既没有需求，也没有性能预算，而系统本来就使用大于1的设备像素比例。相反，该属性的主要用途是设置较小的尺寸，以实现合理的分辨率渲染，而不是盲目遵循窗口几何体，无论窗口多大。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `fixedColorBufferSize` 的变化，不要把它当作普通函数主动调用。

### `void mirrorVerticallyChanged(bool enabled)`

**作用与语义：**

启用时，在顶层窗口中将`QRhiWidget`的背板纹理与其他控件内容合成时，会将图像绕X轴翻转。
默认数值为`false`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `mirrorVertically` 的变化，不要把它当作普通函数主动调用。

### `void sampleCountChanged(int samples)`

**作用与语义：**

该属性控制多采样抗锯齿的采样计数。默认值为`1`，这意味着MSAA被禁用。
有效值为1、4、8，有时还有16和32。`QRhi::supportedSampleCounts()`可用于运行时查询支持的样本计数，但通常应用程序应请求1（无MSAA）、4x（正常MSAA）或8x（高MSAA）。
注意：设置新值意味着渲染器创建的所有`QRhiGraphicsPipeline`对象此后必须使用相同的采样计数。使用不同采样计数创建的现有`QRhiGraphicsPipeline`对象不得再使用。当值变更时，所有颜色和深度模板缓冲区会自动被销毁并重新创建，`initialize()`会再次调用。然而，当`autoRenderTarget` `false`时，是否管理深度模板缓冲区或额外的颜色缓冲区将由应用程序自行管理。
将样本计数从默认1改为更高值意味着`colorTexture()`变为`nullptr`，`msaaColorBuffer()`开始返回有效对象。切回1（或0）则意味着相反：下一次调用`initialize()` `msaaColorBuffer()`返回`nullptr`，而`colorTexture()`再次有效。此外，当样本计数大于1（即使用MSAA）时，`resolveTexture()`返回有效的（非多重采样）`QRhiTexture`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `sampleCount` 的变化，不要把它当作普通函数主动调用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QRhiWidget` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
