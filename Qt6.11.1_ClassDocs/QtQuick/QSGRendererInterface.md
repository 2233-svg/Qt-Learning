# QSGRendererInterface

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QSGRendererInterface` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QSGRendererInterface` 是 Qt Quick 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QSGRendererInterface>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
target_link_libraries(mytarget PRIVATE Qt6::Quick)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 场景图节点和材质的有效期受窗口、组件和渲染阶段控制；纹理、材质和几何通常要在正确的 render context 中创建/释放。节点被删除或场景图失效后，底层 GPU 资源不能继续使用。

**状态与结果：** 区分 GUI/同步阶段、渲染阶段、节点 dirty 状态、纹理状态和后端能力。改变节点属性通常要标记更新，不能在错误阶段直接修改资源；材质是否可用还受默认后端限制。

**线程与事件循环：** QSG 类型经常运行在 render thread，不能从 GUI 线程或后台线程随意读写。通过 QQuickItem 的同步接口在规定阶段交换数据，避免跨线程共享 GPU 资源。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum GraphicsApi { Unknown, Software, OpenVG, OpenGL, Direct3D11, …, Null }`
- `enum RenderMode { RenderMode2D, RenderMode2DNoDepthBuffer, RenderMode3D }`
- `enum Resource { DeviceResource, CommandQueueResource, CommandListResource, PainterResource, RhiResource, …, GraphicsQueueIndexResource }`
- `enum ShaderCompilationType { RuntimeCompilation, OfflineCompilation }`
- `flags ShaderCompilationTypes`
- `enum ShaderSourceType { ShaderSourceString, ShaderSourceFile, ShaderByteCode }`
- `flags ShaderSourceTypes`
- `enum ShaderType { UnknownShadingLanguage, GLSL, HLSL, RhiShader }`

### 公有函数

- `virtual void * getResource(QQuickWindow *window, QSGRendererInterface::Resource resource) const`
- `virtual void * getResource(QQuickWindow *window, const char *resource) const`
- `virtual QSGRendererInterface::GraphicsApi graphicsApi() const = 0`
- `virtual QSGRendererInterface::ShaderCompilationTypes shaderCompilationType() const = 0`
- `virtual QSGRendererInterface::ShaderSourceTypes shaderSourceType() const = 0`
- `virtual QSGRendererInterface::ShaderType shaderType() const = 0`

### 静态公有成员

- `bool isApiRhiBased(QSGRendererInterface::GraphicsApi api)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSGRendererInterface::ShaderCompilationTypeflags QSGRendererInterface::ShaderCompilationTypes`

**作用与语义：**

- `QSGRendererInterface::RuntimeCompilation`：`0x01`;支持着色器源代码的运行时编译
- `QSGRendererInterface::OfflineCompilation`：`0x02`;支持预编译字节码
ShaderCompilationTypes 类型是 QFlags 的 typedef<ShaderCompilationType>。它存储 ShaderCompilationType 值的 OR 组合。

### `enum QSGRendererInterface::ShaderSourceTypeflags QSGRendererInterface::ShaderSourceTypes`

**作用与语义：**

- `QSGRendererInterface::ShaderSourceString`: `0x01`；可以将着色器源代码作为字符串提供在 `ShaderEffect` 对应的属性中
- `QSGRendererInterface::ShaderSourceFile`: `0x02`；支持包含着色器源代码的本地或资源文件
- `QSGRendererInterface::ShaderByteCode`: `0x04`；支持包含着色器字节码的本地或资源文件
ShaderSourceTypes 类型是 QFlags<ShaderSourceType> 的 typedef。它存储 ShaderSourceType 值的按位或组合。

### `[virtual] void *QSGRendererInterface::getResource(QQuickWindow *window, QSGRendererInterface::Resource resource) const`

**作用与语义：**

查询`window`中的图形`resource`。当相关资源不被支持或不可用时，返回空。
成功时，返回的指针要么是直接指向接口的指针，要么是指向需要先去引用的不透明句柄的指针（例如，`VkDevice dev = *static_cast<VkDevice *>(result)`）。后者是必要的，因为此类句柄的大小可能与指针不同。
注意：返回指针的所有权永远不会转移给调用者。
注意：该函数只能在渲染线程中调用。

### `[virtual] void *QSGRendererInterface::getResource(QQuickWindow *window, const char *resource) const`

**作用与语义：**

查询图形资源。`resource` 是一个后端专用键。这使得支持资源枚举中未列出的任何未来资源为支持。
注意：返回指针的所有权永远不会转移给调用者。
注意：该函数只能在渲染线程中调用。

### `[pure virtual] QSGRendererInterface::GraphicsApi QSGRendererInterface::graphicsApi() const`

**作用与语义：**

返回 Qt Quick 场景图正在使用的图形 API。
注意：该函数可以在任何线程上调用。

### `[static] bool QSGRendererInterface::isApiRhiBased(QSGRendererInterface::GraphicsApi api)`

**作用与语义：**

如果`api`基于图形抽象层（`QRhi`），而非直接调用本地图形API，则返回为真。
注意：该函数可以在任何线程上调用。

### `[pure virtual] QSGRendererInterface::ShaderCompilationTypes QSGRendererInterface::shaderCompilationType() const`

**作用与语义：**

返回应用程序所用Qt Quick后端支持的着色器编译方法的位遮罩。
注意：该函数可以在任何线程上调用。

### `[pure virtual] QSGRendererInterface::ShaderSourceTypes QSGRendererInterface::shaderSourceType() const`

**作用与语义：**

返回支持的着色器来源方式的位遮罩，显示`ShaderEffect`项中。
注意：该函数可以在任何线程上调用。

### `[pure virtual] QSGRendererInterface::ShaderType QSGRendererInterface::shaderType() const`

**作用与语义：**

返回应用所使用的Qt Quick后端支持的着色语言。
注意：该函数可以在任何线程上调用。

### `enum GraphicsApi { Unknown, Software, OpenVG, OpenGL, Direct3D11, …, Null }`

**作用与语义：**

- `QSGRendererInterface::Unknown`: `0`；正在使用未知的图形 API
- `QSGRendererInterface::Software`: `1`；正在使用 Qt Quick 2D Renderer
- `QSGRendererInterface::OpenVG`: `2`；通过 EGL 使用 OpenVG
- `QSGRendererInterface::OpenGL (since Qt 5.14)`: `3`；通过图形抽象层使用 OpenGL ES 2.0 或更高版本
- `QSGRendererInterface::Direct3D11 (since Qt 5.14)`: `4`；通过图形抽象层使用 Direct3D 11
- `QSGRendererInterface::Direct3D12 (since Qt 6.6)`: `8`；通过图形抽象层使用 Direct3D 12
- `QSGRendererInterface::Vulkan (since Qt 5.14)`: `5`；通过图形抽象层使用 Vulkan 1.0
- `QSGRendererInterface::Metal (since Qt 5.14)`: `6`；通过图形抽象层使用 Metal
- `QSGRendererInterface::Null (since Qt 5.14)`: `7`；通过图形抽象层使用 Null（无输出）

### `enum RenderMode { RenderMode2D, RenderMode2DNoDepthBuffer, RenderMode3D }`

**作用与语义：**

- `QSGRendererInterface::RenderMode2D`：`0`;普通二维渲染
- `QSGRendererInterface::RenderMode2DNoDepthBuffer`：`1`;正常2D渲染，禁用深度缓冲
- `QSGRendererInterface::RenderMode3D`：`2`;场景作为三维图的一部分被渲染

### `enum Resource { DeviceResource, CommandQueueResource, CommandListResource, PainterResource, RhiResource, …, GraphicsQueueIndexResource }`

**作用与语义：**

- `QSGRendererInterface::DeviceResource`：`0`;资源在适用时是指向图形设备的指针。例如，`VkDevice *`、`MTLDevice *`或`ID3D11Device *`。注意，Vulkan返回的值是指向VkDevice的指针，而非句柄本身。这是因为Vulkan的句柄可能不是指针，且可能使用与架构指针大小不同的大小，因此仅仅投射/投射`void *`是错误的。
- `QSGRendererInterface::CommandQueueResource`：`1`;资源是指向场景图使用的图形命令队列的指针（如适用）。例如，`VkQueue *`或`MTLCommandQueue *`。注意，Vulkan 返回的值是指向 VkQueue 的指针，而非句柄本身。
- `QSGRendererInterface::CommandListResource`：`2`;资源是指向场景图使用的命令列表或缓冲区的指针（如适用）。例如，`VkCommandBuffer *`或`MTLCommandBuffer *`。该对象的有效性有限，仅在场景图准备下一帧时有效。注意，Vulkan 返回的值是指向 VkCommandBuffer 的指针，而非句柄本身。
- `QSGRendererInterface::PainterResource`：`3`;资源是指向场景图在软件后端运行时使用的活跃 `QPainter`。
- `QSGRendererInterface::RhiResource (since Qt 5.14)`：`4`;资源是指向场景图所用实例的`QRhi`（如适用时）。
- `QSGRendererInterface::RhiSwapchainResource (since Qt 6.0)`：`5`;资源是指向与窗口相关的QRhiSwapchain实例的指针。当窗口与`QQuickRenderControl`组合使用时，该值为空。
- `QSGRendererInterface::RhiRedirectCommandBuffer (since Qt 6.0)`：`6`;资源是指向与窗口及其`QQuickRenderControl`关联的`QRhiCommandBuffer`实例的指针。当窗口不关联`QQuickRenderControl`时，该值为空。
- `QSGRendererInterface::RhiRedirectRenderTarget (since Qt 6.0)`：`7`;资源是指向与窗口及其`QQuickRenderControl`关联的`QRhiTextureRenderTarget`实例的指针。当窗口未关联`QQuickRenderControl`时，该值为空。注意该值始终反映主纹理渲染目标，且不依赖于Qt Quick场景，这意味着它不考虑由`ShaderEffect`层或`QQuickItem`层生成的额外纹理目标渲染通道。
- `QSGRendererInterface::PhysicalDeviceResource (since Qt 5.14)`：`8`;资源是场景图所用的物理设备对象的指针（如适用）。例如，`VkPhysicalDevice *`。注意，Vulkan 返回的值是指向 VkPhysicalDevice，而非句柄本身。
- `QSGRendererInterface::OpenGLContextResource (since Qt 5.14)`：`9`;资源是指向场景图（渲染线程上）所用`QOpenGLContext`的指针，如适用。
- `QSGRendererInterface::DeviceContextResource (since Qt 5.14)`：`10`;资源是场景图所用设备上下文的指针（如适用）。例如，`ID3D11DeviceContext *`。
- `QSGRendererInterface::CommandEncoderResource (since Qt 5.14)`：`11`;该资源是指向场景图当前激活的渲染命令编码器对象的指针，在适用时使用。例如，`MTLRenderCommandEncoder *`。该对象有效性有限，仅在场景图记录下一帧渲染时有效。
- `QSGRendererInterface::VulkanInstanceResource (since Qt 5.14)`：`12`;资源是指向场景图所用`QVulkanInstance`的指针（如适用）。
- `QSGRendererInterface::RenderPassResource (since Qt 5.14)`：`13`;资源是指向场景图主要渲染通道的指针，描述颜色和深度/模板附件及其使用方式。例如，`VkRenderPass *`。注意，该值始终反映主渲染目标（屏幕窗口或`QQuickRenderControl`重定向的纹理），不依赖于Qt Quick场景，这意味着它不考虑由`ShaderEffect`层或`QQuickItem`层生成的额外纹理目标渲染通道。
- `QSGRendererInterface::RedirectPaintDevice (since Qt 6.4)`：`14`;资源是指向`QPaintDevice`实例的指针，该实例与窗口及其`QQuickRenderControl`关联。当窗口不关联`QQuickRenderControl`时，该值为空。
- `QSGRendererInterface::GraphicsQueueFamilyIndexResource (since Qt 6.6)`：`15`;资源是指向场景图所用图形队列族索引的指针（如适用）。在Vulkan中，这是指向`uint32_t`索引值的指针。
- `QSGRendererInterface::GraphicsQueueIndexResource (since Qt 6.6)`：`16`;资源是指向场景图所用图形队列索引（uint32_t，如适用）。在Vulkan中，这是指向`uint32_t`索引值的指针，实际上是`CommandQueueResource`报告的VkQueue的索引。

### `enum ShaderCompilationType { RuntimeCompilation, OfflineCompilation }`

**作用与语义：**

- `QSGRendererInterface::RuntimeCompilation`：`0x01`;支持着色器源代码的运行时编译
- `QSGRendererInterface::OfflineCompilation`：`0x02`;支持预编译字节码
ShaderCompilationTypes 类型是 QFlags 的 typedef<ShaderCompilationType>。它存储 ShaderCompilationType 值的 OR 组合。

### `flags ShaderCompilationTypes`

**作用与语义：**

- `QSGRendererInterface::RuntimeCompilation`：`0x01`;支持着色器源代码的运行时编译
- `QSGRendererInterface::OfflineCompilation`：`0x02`;支持预编译字节码
ShaderCompilationTypes 类型是 QFlags 的 typedef<ShaderCompilationType>。它存储 ShaderCompilationType 值的 OR 组合。

### `enum ShaderSourceType { ShaderSourceString, ShaderSourceFile, ShaderByteCode }`

**作用与语义：**

- `QSGRendererInterface::ShaderSourceString`: `0x01`；可以将着色器源代码作为字符串提供在 `ShaderEffect` 对应的属性中
- `QSGRendererInterface::ShaderSourceFile`: `0x02`；支持包含着色器源代码的本地或资源文件
- `QSGRendererInterface::ShaderByteCode`: `0x04`；支持包含着色器字节码的本地或资源文件
ShaderSourceTypes 类型是 QFlags<ShaderSourceType> 的 typedef。它存储 ShaderSourceType 值的按位或组合。

### `flags ShaderSourceTypes`

**作用与语义：**

- `QSGRendererInterface::ShaderSourceString`: `0x01`；可以将着色器源代码作为字符串提供在 `ShaderEffect` 对应的属性中
- `QSGRendererInterface::ShaderSourceFile`: `0x02`；支持包含着色器源代码的本地或资源文件
- `QSGRendererInterface::ShaderByteCode`: `0x04`；支持包含着色器字节码的本地或资源文件
ShaderSourceTypes 类型是 QFlags<ShaderSourceType> 的 typedef。它存储 ShaderSourceType 值的按位或组合。

### `enum ShaderType { UnknownShadingLanguage, GLSL, HLSL, RhiShader }`

**作用与语义：**

- `QSGRendererInterface::UnknownShadingLanguage`: `0`；由于没有关联窗口和场景图，目前未知
- `QSGRendererInterface::GLSL`: `1`；GLSL 或 GLSL ES
- `QSGRendererInterface::HLSL`: `2`；HLSL
- `QSGRendererInterface::RhiShader (since Qt 5.14)`: `3`；使用包含多个目标语言和中间格式着色器变体的 `QShader` 实例。

## 6. 深入实践与常见坑

### 生命周期和资源边界

场景图节点和材质的有效期受窗口、组件和渲染阶段控制；纹理、材质和几何通常要在正确的 render context 中创建/释放。节点被删除或场景图失效后，底层 GPU 资源不能继续使用。

### 状态和错误边界

区分 GUI/同步阶段、渲染阶段、节点 dirty 状态、纹理状态和后端能力。改变节点属性通常要标记更新，不能在错误阶段直接修改资源；材质是否可用还受默认后端限制。

### 线程边界

QSG 类型经常运行在 render thread，不能从 GUI 线程或后台线程随意读写。通过 QQuickItem 的同步接口在规定阶段交换数据，避免跨线程共享 GPU 资源。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSGRendererInterface` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
