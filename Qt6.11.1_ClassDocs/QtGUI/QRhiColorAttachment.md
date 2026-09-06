# QRhiColorAttachment

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiColorAttachment` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <rhi/qrhi.h>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS GuiPrivate)
target_link_libraries(mytarget PRIVATE Qt6::GuiPrivate)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QRhiColorAttachment()`
- `QRhiColorAttachment(QRhiRenderBuffer *renderBuffer)`
- `QRhiColorAttachment(QRhiTexture *texture)`
- `int layer() const`
- `int level() const`
- `(since 6.7) int multiViewCount() const`
- `QRhiRenderBuffer * renderBuffer() const`
- `int resolveLayer() const`
- `int resolveLevel() const`
- `QRhiTexture * resolveTexture() const`
- `void setLayer(int layer)`
- `void setLevel(int level)`
- `(since 6.7) void setMultiViewCount(int count)`
- `void setRenderBuffer(QRhiRenderBuffer *rb)`
- `void setResolveLayer(int layer)`
- `void setResolveLevel(int level)`
- `void setResolveTexture(QRhiTexture *tex)`
- `void setTexture(QRhiTexture *tex)`
- `QRhiTexture * texture() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QRhiColorAttachment::QRhiColorAttachment()`

**作用与语义：**

构建一个空的颜色附件描述。

### `QRhiColorAttachment::QRhiColorAttachment(QRhiRenderBuffer *renderBuffer)`

**作用与语义：**

构建颜色附件描述，指定`renderBuffer`作为关联的颜色缓冲区。

### `QRhiColorAttachment::QRhiColorAttachment(QRhiTexture *texture)`

**作用与语义：**

构建一个颜色附件描述，指定`texture`作为对应的颜色缓冲区。

### `int QRhiColorAttachment::layer() const`

**作用与语义：**

返回图层索引（立方体映射、面或数组图层）。默认为0。

### `int QRhiColorAttachment::level() const`

**作用与语义：**

返回 mip 电平。默认为 0。

### `[since 6.7] int QRhiColorAttachment::multiViewCount() const`

**作用与语义：**

返回当前设置的视图数。默认为0，表示带有该颜色附件的渲染目标不会用于多视角渲染。

### `QRhiRenderBuffer *QRhiColorAttachment::renderBuffer() const`

**作用与语义：**

返回该附件描述引用的渲染缓冲区，如果没有则返回`nullptr`。
实际上，在通过多采样`color`渲染缓冲区设置多采样渲染时，将`QRhiRenderBuffer`与`QRhiColorAttachment`关联最为合理，渲染结束时再解析为非多重采样纹理。

### `int QRhiColorAttachment::resolveLayer() const`

**作用与语义：**

返回当前设置的解析纹理图层。默认为0。

### `int QRhiColorAttachment::resolveLevel() const`

**作用与语义：**

返回当前设置的 resolve 纹理 MIP 级别。默认为 0。

### `QRhiTexture *QRhiColorAttachment::resolveTexture() const`

**作用与语义：**

返回该附件描述所引用的解析纹理，若无则返回`nullptr`。
当附件引用多采样纹理或渲染缓冲区时，适用设置非空分辨率纹理。resolveTexture() 中的`QRhiTexture`则是一个非多采样的二维纹理（或纹理数组），大小相同（但采样数为1）。多采样内容在每次渲染结束时自动解析为该纹理。

### `void QRhiColorAttachment::setLayer(int layer)`

**作用与语义：**

设定`layer`索引。

### `void QRhiColorAttachment::setLevel(int level)`

**作用与语义：**

设置MIP的`level`。

### `[since 6.7] void QRhiColorAttachment::setMultiViewCount(int count)`

**作用与语义：**

设置视图`count`。设置大于1的值表示带有该颜色附件的渲染目标将用于多视角渲染。默认值为0。小于2的值表示没有多视角渲染。
当`count`设置为`2`或更大时，颜色附件必须关联到二维纹理数组。`layer()`和`multiViewCount()`共同定义了多视角渲染中被针对的纹理数组元素范围。
例如，如果`layer`是`0`，`multiViewCount`是`2`，则纹理数组必须包含2个（或更多）元素，多视角渲染将针对元素0和1。着色器中的`gl_ViewIndex`变量值为`0`或`1`，其中视图`0`对应纹理数组元素`0`，视图`1`对应数组元素`1`。
注意：设置大于1的`count`，使用纹理数组作为`texture()`，并在带有该颜色附件的`QRhiTextureRenderTarget`上调用`beginPass()`，意味着整个渲染过程都需进行多视图渲染`multiViewCount()`。除非需要多视图渲染，否则不应设置多视图。多视图不能用于除二维纹理数组以外的纹理类型。（虽然三维纹理可能可行，但具体取决于图形API和后端;但建议应用程序不要依赖这些，仅使用二维纹理数组作为多视图渲染的渲染目标）。
关于多视图渲染的更多细节，请参见 GL_OVR_multiview。请注意，Qt 在 OpenGL（ES）上运行时也需要GL_OVR_multiview2。
多视图渲染仅在 `isFeatureSupported()` 报告支持`MultiView`功能时可用。
注意：为了便携性，请注意部分图形API对多视角渲染存在限制。建议多视图渲染过程不要依赖GL_OVR_multiview声明为不支持的任何功能。唯一的例外是除`gl_Position`外，取决于`gl_ViewIndex`的着色器阶段输出：这可以依赖（即使是OpenGL），因为`QRhi`从未在未同时出现`GL_OVR_multiview2`的情况下报告支持多视角。
注意：多视图渲染不支持与镶嵌或几何着色器结合使用，尽管某些图形API的实现可能允许这样做。

### `void QRhiColorAttachment::setRenderBuffer(QRhiRenderBuffer *rb)`

**作用与语义：**

设置渲染缓冲区`rb`。
注意：`texture()` 和 `renderBuffer()` 不能同时被设定（即非空）。

### `void QRhiColorAttachment::setResolveLayer(int layer)`

**作用与语义：**

设置了 Resolve 纹理的 `layer` 来使用。

### `void QRhiColorAttachment::setResolveLevel(int level)`

**作用与语义：**

设置分辨率纹理 MIP `level` 来使用。

### `void QRhiColorAttachment::setResolveTexture(QRhiTexture *tex)`

**作用与语义：**

设置了分辨率纹理`tex`。
`tex`预期是二维纹理或二维纹理数组。无论哪种情况，解析目标都是`tex`中单层（数组元素）的单个MIP级别。MIP级别和数组层由`resolveLevel()`和`resolveLayer()`指定。
`multiview`例外：当颜色附件关联到纹理数组且启用多视图时，解析纹理也必须是具有足够元素支持所有视图的纹理数组。在这种情况下，所有对应视图的元素都会自动解析;其行为类似于以下伪代码：
在渲染结束时，设置非多采样纹理自动解析多采样纹理或渲染缓冲区，通常比处理多采样纹理（而不设置解析纹理）更为可取，因为这避免了专门处理多采样纹理（`sampler2DMS`、`texelFetch`等）的专用片段着色器，而允许使用与附件纹理未多重采样时相同的着色器。这会牺牲额外的资源（非多重采样`tex`）。

**官方示例：**

```cpp
 for (i = 0; i < multiViewCount(); ++i)
     resolve texture's layer() + i into resolveTexture's resolveLayer() + i
```

### `void QRhiColorAttachment::setTexture(QRhiTexture *tex)`

**作用与语义：**

这样可以`tex`质感。
注意：`texture()` 和 `renderBuffer()` 不能同时被设定（即非空）。

### `QRhiTexture *QRhiColorAttachment::texture() const`

**作用与语义：**

返回该附件描述所引用的纹理，或者如果没有纹理则返回`nullptr`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QRhiColorAttachment` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
