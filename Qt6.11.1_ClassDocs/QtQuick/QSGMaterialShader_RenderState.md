# QSGMaterialShader::RenderState

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QSGMaterialShader::RenderState` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QSGMaterialShader::RenderState` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSGMaterialShader>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

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

- `enum DirtyState { DirtyMatrix, DirtyOpacity, DirtyCachedMaterialData, DirtyAll }`
- `flags DirtyStates`

### 公有函数

- `QMatrix4x4 combinedMatrix() const`
- `float determinant() const`
- `float devicePixelRatio() const`
- `QRect deviceRect() const`
- `QSGMaterialShader::RenderState::DirtyStates dirtyStates() const`
- `bool isMatrixDirty() const`
- `bool isOpacityDirty() const`
- `QMatrix4x4 modelViewMatrix() const`
- `float opacity() const`
- `QMatrix4x4 projectionMatrix() const`
- `QRhiResourceUpdateBatch * resourceUpdateBatch()`
- `QRhi * rhi()`
- `QByteArray * uniformData()`
- `QRect viewportRect() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum RenderState::DirtyStateflags RenderState::DirtyStates`

**作用与语义：**

- `QSGMaterialShader::RenderState::DirtyMatrix`：`0x0001`;用于表示矩阵发生变化，需要更新。
- `QSGMaterialShader::RenderState::DirtyOpacity`：`0x0002`;用于表示不透明度发生变化，需要更新。
- `QSGMaterialShader::RenderState::DirtyCachedMaterialData`：`0x0004`;用于表示缓存材料状态发生变化，必须更新。
- `QSGMaterialShader::RenderState::DirtyAll`：`0xFFFF`;用于表示所有内容都需要更新。
DirtyStates类型是QFlag的typedef<DirtyState>。它存储DirtyState值的OR组合。

### `QMatrix4x4 RenderState::combinedMatrix() const`

**作用与语义：**

返回由模型视图矩阵和项目矩阵合并后的矩阵。

### `float RenderState::determinant() const`

**作用与语义：**

返回用于渲染的模型视图行列式。

### `float RenderState::devicePixelRatio() const`

**作用与语义：**

返回用于渲染的物理像素与设备无关像素的比例。

### `QRect RenderState::deviceRect() const`

**作用与语义：**

返回正在渲染表面的设备rect。

### `QSGMaterialShader::RenderState::DirtyStates RenderState::dirtyStates() const`

**作用与语义：**

返回了渲染状态的变化，需要更新，以便用该材质渲染的几何体符合当前渲染状态。

### `bool RenderState::isMatrixDirty() const`

**作用与语义：**

如果 `dirtyStates()` 包含脏矩阵状态，则返回 `true`，否则返回 `false`。

### `bool RenderState::isOpacityDirty() const`

**作用与语义：**

如果 `dirtyStates()` 包含脏不透明状态，则返回 `true`，否则返回 `false`。

### `QMatrix4x4 RenderState::modelViewMatrix() const`

**作用与语义：**

返回模型视图矩阵。
如果材质设置了 RequiresFullMatrix 标志，则保证是从场景图计算出的完整变换矩阵。
然而，如果该标志未被设置，渲染器可能会选择修改该矩阵。例如，它可以在CPU上预先变换顶点并将该矩阵设置为恒例。
在上述情况下，仍可通过在材料中设置RequiresDeterminant标志并调用`determinant()`访问器来获取实际矩阵行列式。

### `float RenderState::opacity() const`

**作用与语义：**

返回用于渲染的累计不透明度。

### `QMatrix4x4 RenderState::projectionMatrix() const`

**作用与语义：**

返回投影矩阵。

### `QRhiResourceUpdateBatch *RenderState::resourceUpdateBatch()`

**作用与语义：**

返回一个资源更新批次，可以排队上传和复制操作。通常`QSGMaterialShader::updateSampledImage()`用来排队纹理图像内容更新。

### `QRhi *RenderState::rhi()`

**作用与语义：**

返回当前`QRhi`。

### `QByteArray *RenderState::uniformData()`

**作用与语义：**

返回着色器中均匀（常量）缓冲区的数据指针。统一数据只需从`QSGMaterialShader::updateUniformData()`更新。返回值在其他可重实现函数中为空，如`QSGMaterialShader::updateSampledImage()`。
注意：强烈建议在着色器中声明带有`std140`的统一块，并仔细研究OpenGL规范7.6.2.2节中描述的标准统一块布局。确保数据在`QByteArray`中正确放置，`QSGMaterialShader`实现需考虑对齐要求。翻译成其他着色语言的着色器代码应使用相同的块成员偏移量，即使目标语言默认使用不同的打包规则。
注意：为了同时更新多个成员，避免从C POD类型（如struct）复制，除非已验证C结构体的布局与GLSL统一块一致。

### `QRect RenderState::viewportRect() const`

**作用与语义：**

返回被渲染表面的视口矩形。

### `enum DirtyState { DirtyMatrix, DirtyOpacity, DirtyCachedMaterialData, DirtyAll }`

**作用与语义：**

- `QSGMaterialShader::RenderState::DirtyMatrix`：`0x0001`;用于表示矩阵发生变化，需要更新。
- `QSGMaterialShader::RenderState::DirtyOpacity`：`0x0002`;用于表示不透明度发生变化，需要更新。
- `QSGMaterialShader::RenderState::DirtyCachedMaterialData`：`0x0004`;用于表示缓存材料状态发生变化，必须更新。
- `QSGMaterialShader::RenderState::DirtyAll`：`0xFFFF`;用于表示所有内容都需要更新。
DirtyStates类型是QFlag的typedef<DirtyState>。它存储DirtyState值的OR组合。

### `flags DirtyStates`

**作用与语义：**

- `QSGMaterialShader::RenderState::DirtyMatrix`：`0x0001`;用于表示矩阵发生变化，需要更新。
- `QSGMaterialShader::RenderState::DirtyOpacity`：`0x0002`;用于表示不透明度发生变化，需要更新。
- `QSGMaterialShader::RenderState::DirtyCachedMaterialData`：`0x0004`;用于表示缓存材料状态发生变化，必须更新。
- `QSGMaterialShader::RenderState::DirtyAll`：`0xFFFF`;用于表示所有内容都需要更新。
DirtyStates类型是QFlag的typedef<DirtyState>。它存储DirtyState值的OR组合。

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

`QSGMaterialShader::RenderState` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
