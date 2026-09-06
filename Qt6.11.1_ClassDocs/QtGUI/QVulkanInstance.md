# QVulkanInstance

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QVulkanInstance` 是 Vulkan 动态函数解析机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QVulkanInstance` 是 Vulkan 动态函数解析机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 不默认静态链接所有 Vulkan 函数，而是通过 `QVulkanInstance` 在运行时解析函数地址。实例级函数由 `QVulkanFunctions` 提供，设备级函数由与具体 `VkDevice` 关联的 `QVulkanDeviceFunctions` 提供。

**适用场景：** 创建并初始化 `QVulkanInstance`，把它绑定到窗口或渲染环境，通过 `functions()` 取得 instance 级函数，通过 `deviceFunctions(device)` 取得 device 级函数，检查返回状态后再调用。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要直接构造 `QVulkanFunctions`/`QVulkanDeviceFunctions`；不要把 instance 级和 device 级函数混用；不要假设扩展函数自动存在；不要忽略平台和驱动能力。

## 2. 依赖与对象关系

- 头文件：`#include <QVulkanInstance>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Qt 不默认静态链接所有 Vulkan 函数，而是通过 `QVulkanInstance` 在运行时解析函数地址。实例级函数由 `QVulkanFunctions` 提供，设备级函数由与具体 `VkDevice` 关联的 `QVulkanDeviceFunctions` 提供。

### 状态、生命周期和线程

**生命周期：** 函数表依赖对应的 Vulkan instance/device 和有效的函数地址。不能直接构造某些函数表对象，也不能在 instance/device 销毁后继续调用；先完成初始化和设备选择，再取得正确层级的函数表。

**状态与结果：** 要区分 Vulkan loader 不存在、instance 未创建、device 未创建、函数版本/扩展不可用和调用本身返回错误。函数是否可调用还受 Vulkan 头文件版本、运行时驱动和启用扩展影响。

**线程与事件循环：** Vulkan 的线程规则由 Vulkan 对象和命令提交方式决定，Qt 的函数表只负责解析和转发，不替你同步设备访问。窗口/渲染对象还要遵守 Qt Quick 或 QWindow 的线程边界。

## 3. 直接使用

创建并初始化 `QVulkanInstance`，把它绑定到窗口或渲染环境，通过 `functions()` 取得 instance 级函数，通过 `deviceFunctions(device)` 取得 device 级函数，检查返回状态后再调用。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
#include <QVulkanFunctions>
#include <QVulkanInstance>

QVulkanInstance instance;
if (instance.create()) {
    QVulkanFunctions *functions = instance.functions();
    // 只有在 instance 初始化完成且函数可用时调用函数表
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `DebugFilter`
- `(since 6.5) enum DebugMessageSeverityFlag { VerboseSeverity, InfoSeverity, WarningSeverity, ErrorSeverity }`
- `flags DebugMessageSeverityFlags`
- `(since 6.5) enum DebugMessageTypeFlag { GeneralMessage, ValidationMessage, PerformanceMessage }`
- `flags DebugMessageTypeFlags`
- `(since 6.5) DebugUtilsFilter`
- `enum Flag { NoDebugOutputRedirect, NoPortabilityDrivers }`
- `flags Flags`

### 公有函数

- `QVulkanInstance()`
- `~QVulkanInstance()`
- `QVersionNumber apiVersion() const`
- `(since 6.5) void clearDebugOutputFilters()`
- `bool create()`
- `void destroy()`
- `QVulkanDeviceFunctions * deviceFunctions(VkDevice device)`
- `VkResult errorCode() const`
- `QByteArrayList extensions() const`
- `QVulkanInstance::Flags flags() const`
- `QVulkanFunctions * functions() const`
- `PFN_vkVoidFunction getInstanceProcAddr(const char *name)`
- `(since 6.5) void installDebugOutputFilter(QVulkanInstance::DebugUtilsFilter filter)`
- `void installDebugOutputFilter(QVulkanInstance::DebugFilter filter)`
- `bool isValid() const`
- `QByteArrayList layers() const`
- `void presentAboutToBeQueued(QWindow *window)`
- `void presentQueued(QWindow *window)`
- `void removeDebugOutputFilter(QVulkanInstance::DebugFilter filter)`
- `void resetDeviceFunctions(VkDevice device)`
- `void setApiVersion(const QVersionNumber &vulkanVersion)`
- `void setExtensions(const QByteArrayList &extensions)`
- `void setFlags(QVulkanInstance::Flags flags)`
- `void setLayers(const QByteArrayList &layers)`
- `void setVkInstance(VkInstance existingVkInstance)`
- `QVersionNumber supportedApiVersion() const`
- `QVulkanInfoVector<QVulkanExtension> supportedExtensions() const`
- `QVulkanInfoVector<QVulkanLayer> supportedLayers() const`
- `bool supportsPresent(VkPhysicalDevice physicalDevice, uint32_t queueFamilyIndex, QWindow *window)`
- `VkInstance vkInstance() const`

### 静态公有成员

- `VkSurfaceKHR surfaceForWindow(QWindow *window)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 44 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QVulkanInstance::DebugFilter`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVulkanInstance` 的配置属性。初始化或状态切换时通过 `setDebugFilter(...)` 设置，之后用 `DebugFilter()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:DebugFilter`。
- 属性名：`QVulkanInstance`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] enum QVulkanInstance::DebugMessageSeverityFlagflags QVulkanInstance::DebugMessageSeverityFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVulkanInstance` 暴露的类型声明 `调试输出、Message、Severity、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:DebugMessageSeverityFlagflags QVulkanInstance::DebugMessageSeverityFlags`。
- 属性名：`QVulkanInstance`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] enum QVulkanInstance::DebugMessageTypeFlagflags QVulkanInstance::DebugMessageTypeFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVulkanInstance` 暴露的类型声明 `调试输出、Message、类型、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:DebugMessageTypeFlagflags QVulkanInstance::DebugMessageTypeFlags`。
- 属性名：`QVulkanInstance`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias, since 6.5] QVulkanInstance::DebugUtilsFilter`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVulkanInstance` 的配置属性。初始化或状态切换时通过 `setDebugUtilsFilter(...)` 设置，之后用 `DebugUtilsFilter()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:DebugUtilsFilter`。
- 属性名：`QVulkanInstance`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QVulkanInstance::Flagflags QVulkanInstance::Flags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVulkanInstance` 暴露的类型声明 `Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Flagflags QVulkanInstance::Flags`。
- 属性名：`QVulkanInstance`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVulkanInstance::QVulkanInstance()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVulkanInstance` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QVulkanInstance::~QVulkanInstance()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVulkanInstance` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVersionNumber QVulkanInstance::apiVersion() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanInstance::apiVersion` 用于计算、查询或取得与“api、Version”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVersionNumber`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVersionNumber`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] void QVulkanInstance::clearDebugOutputFilters()`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanInstance::clearDebugOutputFilters` 用于执行与“清空、调试输出、Output、Filters”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QVulkanInstance::create()`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanInstance::create` 用于计算、查询或取得与“创建”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanInstance::destroy()`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanInstance::destroy` 用于执行与“destroy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVulkanDeviceFunctions *QVulkanInstance::deviceFunctions(VkDevice device)`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanInstance::deviceFunctions` 用于计算、查询或取得与“device、Functions”相关的操作。调用时要先确认当前状态和 `device` 的有效范围；返回类型是 `QVulkanDeviceFunctions *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVulkanDeviceFunctions *`。
- 参数 `device`：类型为 `VkDevice`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkResult QVulkanInstance::errorCode() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanInstance::errorCode` 用于计算、查询或取得与“错误、Code”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `VkResult`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkResult`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArrayList QVulkanInstance::extensions() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanInstance::extensions` 用于计算、查询或取得与“extensions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArrayList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArrayList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVulkanInstance::Flags QVulkanInstance::flags() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanInstance::flags` 用于计算、查询或取得与“标志”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVulkanInstance::Flags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVulkanInstance::Flags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVulkanFunctions *QVulkanInstance::functions() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanInstance::functions` 用于计算、查询或取得与“functions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVulkanFunctions *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVulkanFunctions *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `PFN_vkVoidFunction QVulkanInstance::getInstanceProcAddr(const char *name)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVulkanInstance` 的核心操作 `getInstanceProcAddr`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`PFN_vkVoidFunction`。
- 参数 `name`：类型为 `const char *`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] void QVulkanInstance::installDebugOutputFilter(QVulkanInstance::DebugUtilsFilter filter)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QVulkanInstance` 添加依赖、数据或子对象的 API `installDebugOutputFilter`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `filter`：类型为 `QVulkanInstance::DebugUtilsFilter`。没有默认值，调用时必须提供。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanInstance::installDebugOutputFilter(QVulkanInstance::DebugFilter filter)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QVulkanInstance` 添加依赖、数据或子对象的 API `installDebugOutputFilter`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `filter`：类型为 `QVulkanInstance::DebugFilter`。没有默认值，调用时必须提供。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QVulkanInstance::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArrayList QVulkanInstance::layers() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanInstance::layers` 用于计算、查询或取得与“layers”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArrayList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArrayList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanInstance::presentAboutToBeQueued(QWindow *window)`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanInstance::presentAboutToBeQueued` 用于执行与“present、About、转换输出、Be、Queued”相关的操作。调用时要先确认当前状态和 `window` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `window`：类型为 `QWindow *`。没有默认值，调用时必须提供。传入 `QWindow *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanInstance::presentQueued(QWindow *window)`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanInstance::presentQueued` 用于执行与“present、Queued”相关的操作。调用时要先确认当前状态和 `window` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `window`：类型为 `QWindow *`。没有默认值，调用时必须提供。传入 `QWindow *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanInstance::removeDebugOutputFilter(QVulkanInstance::DebugFilter filter)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeDebugOutputFilter`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `filter`：类型为 `QVulkanInstance::DebugFilter`。没有默认值，调用时必须提供。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanInstance::resetDeviceFunctions(VkDevice device)`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanInstance::resetDeviceFunctions` 用于执行与“重置、Device、Functions”相关的操作。调用时要先确认当前状态和 `device` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `device`：类型为 `VkDevice`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanInstance::setApiVersion(const QVersionNumber &vulkanVersion)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setApiVersion`。调用它会改变 `QVulkanInstance` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `vulkanVersion`：类型为 `const QVersionNumber &`。没有默认值，调用时必须提供。传入 `const QVersionNumber &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanInstance::setExtensions(const QByteArrayList &extensions)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setExtensions`。调用它会改变 `QVulkanInstance` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `extensions`：类型为 `const QByteArrayList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanInstance::setFlags(QVulkanInstance::Flags flags)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFlags`。调用它会改变 `QVulkanInstance` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `flags`：类型为 `QVulkanInstance::Flags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanInstance::setLayers(const QByteArrayList &layers)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setLayers`。调用它会改变 `QVulkanInstance` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `layers`：类型为 `const QByteArrayList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanInstance::setVkInstance(VkInstance existingVkInstance)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVkInstance`。调用它会改变 `QVulkanInstance` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `existingVkInstance`：类型为 `VkInstance`。没有默认值，调用时必须提供。传入 `VkInstance` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVersionNumber QVulkanInstance::supportedApiVersion() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanInstance::supportedApiVersion` 用于计算、查询或取得与“supported、Api、Version”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVersionNumber`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVersionNumber`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVulkanInfoVector<QVulkanExtension> QVulkanInstance::supportedExtensions() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanInstance::supportedExtensions` 用于计算、查询或取得与“supported、Extensions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVulkanInfoVector<QVulkanExtension>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVulkanInfoVector<QVulkanExtension>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVulkanInfoVector<QVulkanLayer> QVulkanInstance::supportedLayers() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanInstance::supportedLayers` 用于计算、查询或取得与“supported、Layers”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVulkanInfoVector<QVulkanLayer>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVulkanInfoVector<QVulkanLayer>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QVulkanInstance::supportsPresent(VkPhysicalDevice physicalDevice, uint32_t queueFamilyIndex, QWindow *window)`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `supportsPresent`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `physicalDevice`：类型为 `VkPhysicalDevice`。没有默认值，调用时必须提供。传入 `VkPhysicalDevice` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `queueFamilyIndex`：类型为 `uint32_t`。没有默认值，调用时必须提供。传入 `uint32_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `window`：类型为 `QWindow *`。没有默认值，调用时必须提供。传入 `QWindow *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] VkSurfaceKHR QVulkanInstance::surfaceForWindow(QWindow *window)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `surfaceForWindow`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`VkSurfaceKHR`。
- 参数 `window`：类型为 `QWindow *`。没有默认值，调用时必须提供。传入 `QWindow *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkInstance QVulkanInstance::vkInstance() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanInstance::vkInstance` 用于计算、查询或取得与“vk、Instance”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `VkInstance`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkInstance`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `DebugFilter`

**API 类别：** 公有类型

**中文解读：** 这是 `QVulkanInstance` 的 `调试输出、Filter` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.5) enum DebugMessageSeverityFlag { VerboseSeverity, InfoSeverity, WarningSeverity, ErrorSeverity }`

**API 类别：** 公有类型

**中文解读：** 这是 `QVulkanInstance` 暴露的类型声明 `调试输出、Message、Severity、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags DebugMessageSeverityFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QVulkanInstance` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.5) enum DebugMessageTypeFlag { GeneralMessage, ValidationMessage, PerformanceMessage }`

**API 类别：** 公有类型

**中文解读：** 这是 `QVulkanInstance` 暴露的类型声明 `调试输出、Message、类型、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags DebugMessageTypeFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QVulkanInstance` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.5) DebugUtilsFilter`

**API 类别：** 公有类型

**中文解读：** 这是 `QVulkanInstance` 的 `调试输出、Utils、Filter` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum Flag { NoDebugOutputRedirect, NoPortabilityDrivers }`

**API 类别：** 公有类型

**中文解读：** 这是 `QVulkanInstance` 暴露的类型声明 `Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags Flags`

**API 类别：** 公有类型

**中文解读：** 这是 `QVulkanInstance` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

函数表依赖对应的 Vulkan instance/device 和有效的函数地址。不能直接构造某些函数表对象，也不能在 instance/device 销毁后继续调用；先完成初始化和设备选择，再取得正确层级的函数表。

### 状态和错误边界

要区分 Vulkan loader 不存在、instance 未创建、device 未创建、函数版本/扩展不可用和调用本身返回错误。函数是否可调用还受 Vulkan 头文件版本、运行时驱动和启用扩展影响。

### 线程边界

Vulkan 的线程规则由 Vulkan 对象和命令提交方式决定，Qt 的函数表只负责解析和转发，不替你同步设备访问。窗口/渲染对象还要遵守 Qt Quick 或 QWindow 的线程边界。

### 最容易出现的错误

不要直接构造 `QVulkanFunctions`/`QVulkanDeviceFunctions`；不要把 instance 级和 device 级函数混用；不要假设扩展函数自动存在；不要忽略平台和驱动能力。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QVulkanInstance` 所属机制类型：Vulkan 动态函数解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
