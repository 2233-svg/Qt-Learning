# QQuick3DInstancing

> Qt 6.11.1 · Qt Quick 3D

## 1. 先建立直觉

**一句话定位：** `QQuick3DInstancing` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 3D 在 Qt Quick 中加入 3D 场景、相机、材质、模型和渲染能力。

### 这是什么

`QQuick3DInstancing` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuick3DInstancing>`
- 继承自：QQuick3DObject
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

```cpp
#include <QQuick3DInstancing>

// QSG 类型只能在 Qt Quick 规定的场景图阶段使用。
// 先确认渲染后端、线程和对象生命周期，再创建或配置对象。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `depthSortingEnabled : bool`
- `hasTransparency : bool`
- `instanceCountOverride : int`
- `(since 6.9) shadowBoundsMaximum : QVector3D`
- `(since 6.9) shadowBoundsMinimum : QVector3D`

### 公有函数

- `bool depthSortingEnabled() const`
- `bool hasTransparency() const`
- `int instanceCountOverride() const`
- `QVector3D shadowBoundsMaximum() const`
- `QVector3D shadowBoundsMinimum() const`

### 公有槽函数

- `void setDepthSortingEnabled(bool enabled)`
- `void setHasTransparency(bool hasTransparency)`
- `void setInstanceCountOverride(int instanceCountOverride)`
- `void setShadowBoundsMaximum(const QVector3D &newShadowBoundsMinimum)`
- `void setShadowBoundsMinimum(const QVector3D &newShadowBoundsMinimum)`

### 信号

- `void depthSortingEnabledChanged()`
- `void hasTransparencyChanged()`
- `void instanceCountOverrideChanged()`
- `void shadowBoundsMaximumChanged()`
- `void shadowBoundsMinimumChanged()`

### 保护函数

- `virtual QByteArray getInstanceBuffer(int *instanceCount) = 0`
- `void markDirty()`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 24 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `depthSortingEnabled : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuick3DInstancing` 的配置属性。初始化或状态切换时通过 `setDepthSortingEnabled(...)` 设置，之后用 `depthSortingEnabled()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`depthSortingEnabled`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `hasTransparency : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuick3DInstancing` 的状态/能力属性。通常通过 `hasTransparency()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`hasTransparency`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `instanceCountOverride : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuick3DInstancing` 的配置属性。初始化或状态切换时通过 `setInstanceCountOverride(...)` 设置，之后用 `instanceCountOverride()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`instanceCountOverride`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] shadowBoundsMaximum : QVector3D`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuick3DInstancing` 的配置属性。初始化或状态切换时通过 `setShadowBoundsMaximum(...)` 设置，之后用 `shadowBoundsMaximum()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QVector3D`。
- 属性名：`shadowBoundsMaximum`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] shadowBoundsMinimum : QVector3D`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuick3DInstancing` 的配置属性。初始化或状态切换时通过 `setShadowBoundsMinimum(...)` 设置，之后用 `shadowBoundsMinimum()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QVector3D`。
- 属性名：`shadowBoundsMinimum`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static protected] QQuick3DInstancing::InstanceTableEntry QQuick3DInstancing::calculateTableEntry(const QVector3D &position, const QVector3D &scale, const QVector3D &eulerRotation, const QColor &color, const QVector4D &customData = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `calculateTableEntry`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuick3DInstancing::InstanceTableEntry`。
- 参数 `position`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `scale`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `eulerRotation`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `customData`：类型为 `const QVector4D &`。默认值为 `{}`。传入 `const QVector4D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static protected] QQuick3DInstancing::InstanceTableEntry QQuick3DInstancing::calculateTableEntryFromQuaternion(const QVector3D &position, const QVector3D &scale, const QQuaternion &rotation, const QColor &color, const QVector4D &customData = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `calculateTableEntryFromQuaternion`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuick3DInstancing::InstanceTableEntry`。
- 参数 `position`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `scale`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rotation`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `customData`：类型为 `const QVector4D &`。默认值为 `{}`。传入 `const QVector4D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual protected] QByteArray QQuick3DInstancing::getInstanceBuffer(int *instanceCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuick3DInstancing` 的核心操作 `getInstanceBuffer`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `instanceCount`：类型为 `int *`。没有默认值，调用时必须提供。传入 `int *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QQuick3DInstancing::markDirty()`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DInstancing::markDirty` 用于执行与“mark、Dirty”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool depthSortingEnabled() const`

**API 类别：** 公有函数

**中文解读：** `QQuick3DInstancing::depthSortingEnabled` 用于计算、查询或取得与“depth、Sorting、启用状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool hasTransparency() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `hasTransparency`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int instanceCountOverride() const`

**API 类别：** 公有函数

**中文解读：** `QQuick3DInstancing::instanceCountOverride` 用于计算、查询或取得与“instance、数量统计、Override”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVector3D shadowBoundsMaximum() const`

**API 类别：** 公有函数

**中文解读：** `QQuick3DInstancing::shadowBoundsMaximum` 用于计算、查询或取得与“shadow、Bounds、最大值”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVector3D`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVector3D`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVector3D shadowBoundsMinimum() const`

**API 类别：** 公有函数

**中文解读：** `QQuick3DInstancing::shadowBoundsMinimum` 用于计算、查询或取得与“shadow、Bounds、最小值”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVector3D`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVector3D`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDepthSortingEnabled(bool enabled)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setDepthSortingEnabled`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `enabled`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setHasTransparency(bool hasTransparency)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setHasTransparency`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `hasTransparency`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setInstanceCountOverride(int instanceCountOverride)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setInstanceCountOverride`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `instanceCountOverride`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setShadowBoundsMaximum(const QVector3D &newShadowBoundsMinimum)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setShadowBoundsMaximum`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `newShadowBoundsMinimum`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setShadowBoundsMinimum(const QVector3D &newShadowBoundsMinimum)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setShadowBoundsMinimum`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `newShadowBoundsMinimum`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void depthSortingEnabledChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `depthSortingEnabledChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void hasTransparencyChanged()`

**API 类别：** 信号

**中文解读：** 这是查询 API `hasTransparencyChanged`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void instanceCountOverrideChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `instanceCountOverrideChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void shadowBoundsMaximumChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `shadowBoundsMaximumChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void shadowBoundsMinimumChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `shadowBoundsMinimumChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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

`QQuick3DInstancing` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
