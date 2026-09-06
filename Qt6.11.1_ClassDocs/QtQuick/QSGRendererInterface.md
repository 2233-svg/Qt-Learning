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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 17 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QSGRendererInterface::ShaderCompilationTypeflags QSGRendererInterface::ShaderCompilationTypes`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGRendererInterface` 暴露的类型声明 `Shader、Compilation、Typeflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ShaderCompilationTypeflags QSGRendererInterface::ShaderCompilationTypes`。
- 属性名：`QSGRendererInterface`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QSGRendererInterface::ShaderSourceTypeflags QSGRendererInterface::ShaderSourceTypes`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGRendererInterface` 暴露的类型声明 `Shader、来源、Typeflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ShaderSourceTypeflags QSGRendererInterface::ShaderSourceTypes`。
- 属性名：`QSGRendererInterface`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void *QSGRendererInterface::getResource(QQuickWindow *window, QSGRendererInterface::Resource resource) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSGRendererInterface` 的核心操作 `getResource`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void *`。
- 参数 `window`：类型为 `QQuickWindow *`。没有默认值，调用时必须提供。传入 `QQuickWindow *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `resource`：类型为 `QSGRendererInterface::Resource`。没有默认值，调用时必须提供。传入 `QSGRendererInterface::Resource` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void *QSGRendererInterface::getResource(QQuickWindow *window, const char *resource) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSGRendererInterface` 的核心操作 `getResource`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void *`。
- 参数 `window`：类型为 `QQuickWindow *`。没有默认值，调用时必须提供。传入 `QQuickWindow *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `resource`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSGRendererInterface::GraphicsApi QSGRendererInterface::graphicsApi() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGRendererInterface::graphicsApi` 用于计算、查询或取得与“graphics、Api”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGRendererInterface::GraphicsApi`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGRendererInterface::GraphicsApi`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QSGRendererInterface::isApiRhiBased(QSGRendererInterface::GraphicsApi api)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isApiRhiBased`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `api`：类型为 `QSGRendererInterface::GraphicsApi`。没有默认值，调用时必须提供。传入 `QSGRendererInterface::GraphicsApi` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSGRendererInterface::ShaderCompilationTypes QSGRendererInterface::shaderCompilationType() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGRendererInterface::shaderCompilationType` 用于计算、查询或取得与“shader、Compilation、类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGRendererInterface::ShaderCompilationTypes`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGRendererInterface::ShaderCompilationTypes`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSGRendererInterface::ShaderSourceTypes QSGRendererInterface::shaderSourceType() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGRendererInterface::shaderSourceType` 用于计算、查询或取得与“shader、来源、类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGRendererInterface::ShaderSourceTypes`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGRendererInterface::ShaderSourceTypes`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSGRendererInterface::ShaderType QSGRendererInterface::shaderType() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGRendererInterface::shaderType` 用于计算、查询或取得与“shader、类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGRendererInterface::ShaderType`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGRendererInterface::ShaderType`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum GraphicsApi { Unknown, Software, OpenVG, OpenGL, Direct3D11, …, Null }`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGRendererInterface` 暴露的类型声明 `Graphics、Api`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum RenderMode { RenderMode2D, RenderMode2DNoDepthBuffer, RenderMode3D }`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGRendererInterface` 暴露的类型声明 `渲染、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum Resource { DeviceResource, CommandQueueResource, CommandListResource, PainterResource, RhiResource, …, GraphicsQueueIndexResource }`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGRendererInterface` 暴露的类型声明 `Resource`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum ShaderCompilationType { RuntimeCompilation, OfflineCompilation }`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGRendererInterface` 暴露的类型声明 `Shader、Compilation、类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags ShaderCompilationTypes`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGRendererInterface` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum ShaderSourceType { ShaderSourceString, ShaderSourceFile, ShaderByteCode }`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGRendererInterface` 暴露的类型声明 `Shader、来源、类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags ShaderSourceTypes`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGRendererInterface` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum ShaderType { UnknownShadingLanguage, GLSL, HLSL, RhiShader }`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGRendererInterface` 暴露的类型声明 `Shader、类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
