# QSGMaterialShader

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QSGMaterialShader` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QSGMaterialShader` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSGMaterialShader>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
target_link_libraries(mytarget PRIVATE Qt6::Quick)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

### 状态、生命周期和线程

**生命周期：** 场景图节点和材质的有效期受窗口、组件和渲染阶段控制；纹理、材质和几何通常要在正确的 render context 中创建/释放。节点被删除或场景图失效后，底层 GPU 资源不能继续使用。

**状态与结果：** 区分 GUI/同步阶段、渲染阶段、节点 dirty 状态、纹理状态和后端能力。改变节点属性通常要标记更新，不能在错误阶段直接修改资源；材质是否可用还受默认后端限制。

**线程与事件循环：** QSG 类型经常运行在 render thread，不能从 GUI 线程或后台线程随意读写。通过 QQuickItem 的同步接口在规定阶段交换数据，避免跨线程共享 GPU 资源。

## 3. 直接使用

需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。 使用时通常按这个过程组织：注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `struct GraphicsPipelineState`
- `class RenderState`
- `enum Flag { UpdatesGraphicsPipelineState }`
- `flags Flags`

### 公有函数

- `QSGMaterialShader()`
- `(since 6.4) int combinedImageSamplerCount(int binding) const`
- `QSGMaterialShader::Flags flags() const`
- `void setFlag(QSGMaterialShader::Flags flags, bool on = true)`
- `void setFlags(QSGMaterialShader::Flags flags)`
- `virtual bool updateGraphicsPipelineState(QSGMaterialShader::RenderState &state, QSGMaterialShader::GraphicsPipelineState *ps, QSGMaterial *newMaterial, QSGMaterial *oldMaterial)`
- `virtual void updateSampledImage(QSGMaterialShader::RenderState &state, int binding, QSGTexture **texture, QSGMaterial *newMaterial, QSGMaterial *oldMaterial)`
- `virtual bool updateUniformData(QSGMaterialShader::RenderState &state, QSGMaterial *newMaterial, QSGMaterial *oldMaterial)`

### 保护函数

- `void setShader(QSGMaterialShader::Stage stage, const QShader &shader)`
- `void setShaderFileName(QSGMaterialShader::Stage stage, const QString &filename)`
- `(since 6.8) void setShaderFileName(QSGMaterialShader::Stage stage, const QString &filename, int viewCount)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSGMaterialShader::Flagflags QSGMaterialShader::Flags`

**作用与语义：**

标志值用于表示特殊材料属性。
- `QSGMaterialShader::UpdatesGraphicsPipelineState`：`0x0001`;设置此标志后可调用`updateGraphicsPipelineState()`。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `QSGMaterialShader::QSGMaterialShader()`

**作用与语义：**

构建了一个新的QSGMaterialShader。

### `[since 6.4] int QSGMaterialShader::combinedImageSamplerCount(int binding) const`

**作用与语义：**

返回合并图像采样器变量中的元素数，`binding`。该值从着色器代码中内省。变量可以是数组，且可能具有多个维度。
计数反映了变量中合成图像采样器项目的总数。在以下示例中，`srcA`的计数为1，`srcB`为4，`srcC`为6。
这个计数是`QSGMaterialShader::updateSampledImage`纹理参数中的`QSGTexture`指针数量。

**官方示例：**

```cpp
 layout (binding = 0) uniform sampler2D srcA;
 layout (binding = 1) uniform sampler2D srcB[4];
 layout (binding = 2) uniform sampler2D srcC[2][3];
```

### `QSGMaterialShader::Flags QSGMaterialShader::flags() const`

**作用与语义：**

返回当前为该材质着色器设置的标志。

### `void QSGMaterialShader::setFlag(QSGMaterialShader::Flags flags, bool on = true)`

**作用与语义：**

如果该材料着色器`flags`为真`on`;否则清除指定的标志。

### `void QSGMaterialShader::setFlags(QSGMaterialShader::Flags flags)`

**作用与语义：**

设置了该材质着色器的`flags`。

### `[protected] void QSGMaterialShader::setShader(QSGMaterialShader::Stage stage, const QShader &shader)`

**作用与语义：**

为指定`stage`设定`shader`。

### `[protected] void QSGMaterialShader::setShaderFileName(QSGMaterialShader::Stage stage, const QString &filename)`

**作用与语义：**

为指定`stage`设置着色器的着色器`filename`。
文件通常包含序列化的`QShader`。
警告：着色器，包括`.qsb`文件，被假定为可信内容。建议应用开发者在允许加载非应用内容的用户提供内容前，仔细考虑潜在影响。

### `[protected, since 6.8] void QSGMaterialShader::setShaderFileName(QSGMaterialShader::Stage stage, const QString &filename, int viewCount)`

**作用与语义：**

为指定`stage`设置着色器的`filename`。
文件应包含序列化`QShader`。
这种重载用于启用`multiview`渲染，特别是当构建系统的多视图便利选项被使用时。
`viewCount`应该是2、3或4。`filename`会根据这些数据自动调整。
警告：着色器，包括`.qsb`文件，被假定为可信内容。建议应用开发者在允许加载非应用内容前，仔细考虑潜在影响。

### `[virtual] bool QSGMaterialShader::updateGraphicsPipelineState(QSGMaterialShader::RenderState &state, QSGMaterialShader::GraphicsPipelineState *ps, QSGMaterial *newMaterial, QSGMaterial *oldMaterial)`

**作用与语义：**

场景图调用该函数，使材质能够提供自定义的图形状态。可通过材质自定义的状态集合仅限于混合和相关设置。
注意：只有当`UpdatesGraphicsPipelineState`标志通过`setFlags()`启用时，才调用此功能。默认情况下，该函数未被设置，因此从未调用。
每当对`ps`中的任何成员发生变更时，返回值必须`true`。
注意：`ps` 的内容在调用该函数之间不持久。
当前渲染`state`是从场景图传递的。
子类专属状态可以从`newMaterial`中提取。当`oldMaterial`为空时，这个着色器刚刚被激活。

### `[virtual] void QSGMaterialShader::updateSampledImage(QSGMaterialShader::RenderState &state, int binding, QSGTexture **texture, QSGMaterial *newMaterial, QSGMaterial *oldMaterial)`

**作用与语义：**

场景图调用该函数，用于准备在着色器中使用采样图像，通常以组合图像采样器的形式出现。
`binding` 是采样器的绑定编号。该函数为与 `QSGMaterialShader` 关联的着色器代码中的每个合并图像采样器变量调用。
`texture` 是一个由`QSGTexture`指针组成的数组。数组中的元素数与着色器代码中指定的图像采样器变量中的元素数相匹配。该变量可以是一个数组，并且可以有多个维度。数组中的元素数量可以通过`QSGMaterialShader::combinedImageSamplerCount` 找到。
当`texture`中的元素为空时，必须将其设置为有效的`QSGTexture`指针后才能返回。当非空时，材料自行决定是否存储新的`QSGTexture *`，或是否更新已知`QSGTexture`上的某些参数。`QSGTexture`的所有权不会转移。
当前的渲染`state`是从场景图传递过来的。在相关情况下，由材质触发通过`QSGTexture::commitTextureOperations()`上传的队列纹理数据。
子职业专属状态可以从`newMaterial`中提取。
`oldMaterial`可以用来最小化变更。当`oldMaterial`为空时，这个着色器只是被激活了。

### `[virtual] bool QSGMaterialShader::updateUniformData(QSGMaterialShader::RenderState &state, QSGMaterial *newMaterial, QSGMaterial *oldMaterial)`

**作用与语义：**

场景图调用该函数以更新着色器程序的统一缓冲区内容。实现不执行任何实际图形操作，仅负责将数据复制到返回`RenderState::uniformData()`返回的`QByteArray`。场景图负责使该缓冲区在着色器中可见。
当前渲染`state`从场景图传递。如果该状态表明任何相关状态为脏状态，实现必须更新通过`RenderState::uniformData()`访问的缓冲区中相应区域。当某个状态（如矩阵或不透明度）不脏时，无需操作对应区域，因为数据是持久的。
每当对统一数据做出任何更改时，返回值必须`true`。
子类特定的状态，例如平面颜色材质的颜色，应从`newMaterial`中提取，以便相应更新缓冲区中的相关区域。
`oldMaterial`可以用来最小化缓冲区的变化（通常是memcpy调用），在更新材质状态时。当`oldMaterial`为空时，这个着色器刚刚被激活。

### `struct GraphicsPipelineState`

**作用与语义：**

描述材质希望应用于当前活跃图形管线状态的状态变化。
与`QSGMaterialShader`不同，`QSGMaterialShader`无法直接通过底层图形API发出状态更改命令。这主要是因为可单独更改状态的概念已被现代图形API支持，已被弃用。
因此，有权`QSGMaterialShader`暴露一个包含支持状态集的数据结构，材质可以在其 updatePipelineState() 实现中更改这些状态（如果有的话）。场景图随后会在内部将这些变化应用到活跃的图形流水线状态，然后根据需要回滚。
当调用`updateGraphicsPipelineState()`时，结构体的所有成员都设置为一个有效值，以反映渲染器的当前状态。如果没有更改任何值（或没有重新实现函数），说明材质对默认值是正常的（不过默认值是动态的，例如根据`QSGMaterial`标志而定）。

### `class RenderState`

**作用与语义：**

在调用QSGMaterialShader：：updateUniformData()和其他更新类型函数时，封装当前渲染状态。
渲染状态包含多个访问器，着色器需要遵守这些访问器，以符合当前场景图的状态。

### `enum Flag { UpdatesGraphicsPipelineState }`

**作用与语义：**

标志值用于表示特殊材料属性。
- `QSGMaterialShader::UpdatesGraphicsPipelineState`：`0x0001`;设置此标志后可调用`updateGraphicsPipelineState()`。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `flags Flags`

**作用与语义：**

标志值用于表示特殊材料属性。
- `QSGMaterialShader::UpdatesGraphicsPipelineState`：`0x0001`;设置此标志后可调用`updateGraphicsPipelineState()`。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

场景图节点和材质的有效期受窗口、组件和渲染阶段控制；纹理、材质和几何通常要在正确的 render context 中创建/释放。节点被删除或场景图失效后，底层 GPU 资源不能继续使用。

### 状态和错误边界

区分 GUI/同步阶段、渲染阶段、节点 dirty 状态、纹理状态和后端能力。改变节点属性通常要标记更新，不能在错误阶段直接修改资源；材质是否可用还受默认后端限制。

### 线程边界

QSG 类型经常运行在 render thread，不能从 GUI 线程或后台线程随意读写。通过 QQuickItem 的同步接口在规定阶段交换数据，避免跨线程共享 GPU 资源。

### 最容易出现的错误

不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSGMaterialShader` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
