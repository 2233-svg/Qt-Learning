# QSGMaterial

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QSGMaterial` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QSGMaterial` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSGMaterial>`
- 继承自：未在类页中列出
- 直接派生类：QSGFlatColorMaterial、QSGOpaqueTextureMaterial,、QSGVertexColorMaterial

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

- `enum Flag { Blending, RequiresDeterminant, RequiresFullMatrixExceptTranslate, RequiresFullMatrix, NoBatching, CustomCompileStep }`
- `flags Flags`

### 公有函数

- `virtual int compare(const QSGMaterial *other) const`
- `virtual QSGMaterialShader * createShader(QSGRendererInterface::RenderMode renderMode) const = 0`
- `QSGMaterial::Flags flags() const`
- `void setFlag(QSGMaterial::Flags flags, bool on = true)`
- `virtual QSGMaterialType * type() const = 0`
- `(since 6.8) int viewCount() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSGMaterial::Flagflags QSGMaterial::Flags`

**作用与语义：**

- `QSGMaterial::Blending`：`0x0001`;如果材质在渲染时需要启用混合，则将此标志设置为true。
- `QSGMaterial::RequiresDeterminant`：`0x0002`;如果材质依赖于几何节点矩阵的行列式进行渲染，则将该标志设为真。
- `QSGMaterial::RequiresFullMatrixExceptTranslate`：`0x0004 | RequiresDeterminant`;如果材料渲染时依赖于几何节点的完整矩阵（平移部分除外），则将该标志设为true。
- `QSGMaterial::RequiresFullMatrix`：`0x0008 | RequiresFullMatrixExceptTranslate`;如果材质渲染时依赖于几何节点的完整矩阵，则将该标志设为真。
- `QSGMaterial::NoBatching`：`0x0010`;如果材质使用的着色器与场景图的批量处理机制不兼容，则将该标志设置为true。这在某些高级应用中尤为重要，例如直接操作顶点着色器中的`gl_Position.z`。此类解决方案通常与特定场景结构绑定，且在场景中任意内容时可能不安全使用。因此，该标志应仅在适当调查后设置，绝大多数材质从未需要使用。设置该标志可能导致性能下降，因为需要发出更多绘制调用。该标志引入于Qt 6.3。
- `QSGMaterial::CustomCompileStep`：`NoBatching`;在Qt 6中，该标志与NoBatching相同。更倾向于使用NoBatching。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `[virtual] int QSGMaterial::compare(const QSGMaterial *other) const`

**作用与语义：**

将该材料与`other`比较，若相等则返回0;如果该材料应先于`other`排序，则返回1 `other`。
场景图可以重新排序几何节点以最小化状态变化。排序过程中调用比较函数，以便在每次调用QSGMaterialShader：：updateState()时对材料进行排序以最小化状态变化。
这个指针和`other`保证`type()`相同。

### `[pure virtual] QSGMaterialShader *QSGMaterial::createShader(QSGRendererInterface::RenderMode renderMode) const`

**作用与语义：**

该函数返回用于渲染特定 `QSGMaterial` 实现几何体的`QSGMaterialShader`实现的新实例。
该函数对每种材料类型和`renderMode`组合只调用一次，并且会在内部缓存。
对于大多数材质，`renderMode`可以忽略。有些材质可能需要针对特定渲染模式进行自定义处理。例如，如果材质实现了抗锯齿，需要考虑在使用 RenderMode3D 时考虑透视变换。

### `QSGMaterial::Flags QSGMaterial::flags() const`

**作用与语义：**

返回材料的标志。

### `void QSGMaterial::setFlag(QSGMaterial::Flags flags, bool on = true)`

**作用与语义：**

如果该材料为真，则设置`flags` `on`标记;否则清除属性。

### `[pure virtual] QSGMaterialType *QSGMaterial::type() const`

**作用与语义：**

场景图调用该函数查询与`createShader()`实例化`QSGMaterialShader`唯一的标识符。
对于许多材料，典型方法是返回指向静态且全局可用的`QSGMaterialType`实例的指针。`QSGMaterialType`是一个不透明对象。其目的仅作为一种类型安全、简单的方式来生成唯一的材料标识符。

**官方示例：**

```cpp
 QSGMaterialType *type() const override
 {
     static QSGMaterialType type;
     return &type;
 }
```

### `[since 6.8] int QSGMaterial::viewCount() const`

**作用与语义：**

返回 多视图渲染中使用材质的视图数量。
注意：返回值仅在从`createShader()`调用及之后有效。该值不一定在场景图调用`createShader()`之前是最新的。
通常返回值为`1`。视野计数大于2意味着进行了多视角渲染。支持多视角的材质应在`createShader()`或其`QSGMaterialShader`构造函数中查询viewCount()，并确保选择了合适的着色器。顶点着色器随后需要使用`gl_ViewIndex`来索引模型视图-投影矩阵数组，因为多视图模式下存在多个矩阵。（每个视图一个）。
举例来说，以下简单的顶点着色器：
该着色器准备处理2个视图，且仅2个视图。它与其他视图计数不兼容。在条件着色器时，必须调用`--view-count 2` `qsb`工具，或者如果使用CMake集成，必须在`qt_add_shaders()`命令中指定`VIEW_COUNT 2`。
注意：每当设置2或更多观看次数时，Ly `qsb`会自动注入`#extension GL_EXT_multiview : require`的行。
鼓励开发者使用自动注入的预处理器变量 `QSHADER_VIEW_COUNT` 以简化不同视图数量的处理。例如，如果需要在同一源文件中同时支持非多视图和视野计数为 2 的多视图，可以采取以下措施：
同一个源文件现在可以两次运行 `qsb` 或 `qt_add_shaders()`，一次不指定视图计数，一次设置为 2。材料随后可以根据 viewCount() 在运行时选择合适的 .qsb 文件。
对于 CMake，这可能类似于以下情况。在这个例子中，对应的`QSGMaterialShader`应根据 viewCount() 的值在 `:/shaders/example.vert.qsb` 和 `:/shaders/multiview/example.vert.qsb` 之间做出选择。（片段着色器也是如此）。
注意：片段着色器应与顶点着色器相同处理，尽管片段着色器代码不能依赖于视图计数（`gl_ViewIndex`），以实现最大可移植性。在多视图集中包含片段着色器也有两个原因。一是在同一图形流程中混合不同着色器版本可能会带来问题，具体取决于底层的图形API：例如，在D3D12中，混合着色器5.0和6.1的HLSL着色器会引发错误。另一原因是在片段着色器中定义`QSHADER_VIEW_COUNT`非常有用，例如在顶点和片段阶段共享统一缓冲区布局时。
注意：对于依赖 `gl_ViewIndex` 的顶点着色器，OpenGL 的最低 GLSL 版本是`330`。较低版本可能在构建时被接受，但根据 OpenGL 实现的不同，运行时可能导致错误。
为方便起见，还有一个`MULTIVIEW`选项用于qt_add_shaders()。它首先正常运行`qsb`工具，然后将`VIEW_COUNT`覆盖为`2`，设置`GLSL`、`HLSL`、`MSL`到一些合适的默认值，再次运行`qsb`，这次输出带有后缀的.qsb文件。Material实现可以利用`QSGMaterialShader::setShaderFileName()`重载，取`viewCount`参数，自动选择正确的.qsb文件。
因此，以下内容大体等同于上述示例调用，只是无需指定手动管理的输出文件。注意，有时自动选择的着色语言版本不够，这时应用程序应继续显式指定所有内容。
有关Qt中多视角支持的更多底层细节，请参见 `QRhi::MultiView`、`QRhiColorAttachment::setMultiViewCount()` 和 `QRhiGraphicsPipeline::setMultiViewCount()`。Qt 快速场景图渲染器准备识别多视图渲染目标，前提是通过`QQuickRenderTarget::fromRhiRenderTarget()`指定，或 3D API 特定函数，如`arraySize`参数大于 1 的 `fromVulkanImage()`。渲染器随后会将视图计数传播到图形管道和材质。

**官方示例：**

```cpp
 #version 440

 layout(location = 0) in vec4 vertexCoord;
 layout(location = 1) in vec4 vertexColor;

 layout(location = 0) out vec4 color;

 layout(std140, binding = 0) uniform buf {
     mat4 matrix[2];
     float opacity;
 };

 void main()
 {
     gl_Position = matrix[gl_ViewIndex] * vertexCoord;
     color = vertexColor * opacity;
 }
```

### `enum Flag { Blending, RequiresDeterminant, RequiresFullMatrixExceptTranslate, RequiresFullMatrix, NoBatching, CustomCompileStep }`

**作用与语义：**

- `QSGMaterial::Blending`：`0x0001`;如果材质在渲染时需要启用混合，则将此标志设置为true。
- `QSGMaterial::RequiresDeterminant`：`0x0002`;如果材质依赖于几何节点矩阵的行列式进行渲染，则将该标志设为真。
- `QSGMaterial::RequiresFullMatrixExceptTranslate`：`0x0004 | RequiresDeterminant`;如果材料渲染时依赖于几何节点的完整矩阵（平移部分除外），则将该标志设为true。
- `QSGMaterial::RequiresFullMatrix`：`0x0008 | RequiresFullMatrixExceptTranslate`;如果材质渲染时依赖于几何节点的完整矩阵，则将该标志设为真。
- `QSGMaterial::NoBatching`：`0x0010`;如果材质使用的着色器与场景图的批量处理机制不兼容，则将该标志设置为true。这在某些高级应用中尤为重要，例如直接操作顶点着色器中的`gl_Position.z`。此类解决方案通常与特定场景结构绑定，且在场景中任意内容时可能不安全使用。因此，该标志应仅在适当调查后设置，绝大多数材质从未需要使用。设置该标志可能导致性能下降，因为需要发出更多绘制调用。该标志引入于Qt 6.3。
- `QSGMaterial::CustomCompileStep`：`NoBatching`;在Qt 6中，该标志与NoBatching相同。更倾向于使用NoBatching。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `flags Flags`

**作用与语义：**

- `QSGMaterial::Blending`：`0x0001`;如果材质在渲染时需要启用混合，则将此标志设置为true。
- `QSGMaterial::RequiresDeterminant`：`0x0002`;如果材质依赖于几何节点矩阵的行列式进行渲染，则将该标志设为真。
- `QSGMaterial::RequiresFullMatrixExceptTranslate`：`0x0004 | RequiresDeterminant`;如果材料渲染时依赖于几何节点的完整矩阵（平移部分除外），则将该标志设为true。
- `QSGMaterial::RequiresFullMatrix`：`0x0008 | RequiresFullMatrixExceptTranslate`;如果材质渲染时依赖于几何节点的完整矩阵，则将该标志设为真。
- `QSGMaterial::NoBatching`：`0x0010`;如果材质使用的着色器与场景图的批量处理机制不兼容，则将该标志设置为true。这在某些高级应用中尤为重要，例如直接操作顶点着色器中的`gl_Position.z`。此类解决方案通常与特定场景结构绑定，且在场景中任意内容时可能不安全使用。因此，该标志应仅在适当调查后设置，绝大多数材质从未需要使用。设置该标志可能导致性能下降，因为需要发出更多绘制调用。该标志引入于Qt 6.3。
- `QSGMaterial::CustomCompileStep`：`NoBatching`;在Qt 6中，该标志与NoBatching相同。更倾向于使用NoBatching。
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

`QSGMaterial` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
