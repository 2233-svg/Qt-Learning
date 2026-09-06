# QSGNode

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QSGNode` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QSGNode` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSGNode>`
- 继承自：未在类页中列出
- 直接派生类：QSGBasicGeometryNode、QSGOpacityNode、QSGRenderNode,、QSGTransformNode

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

- `flags DirtyState`
- `enum DirtyStateBit { DirtyMatrix, DirtyNodeAdded, DirtyNodeRemoved, DirtyGeometry, DirtyMaterial, …, DirtySubtreeBlocked }`
- `enum Flag { OwnedByParent, UsePreprocess, OwnsGeometry, OwnsMaterial, OwnsOpaqueMaterial, InternalReserved }`
- `flags Flags`
- `enum NodeType { BasicNodeType, GeometryNodeType, TransformNodeType, ClipNodeType, OpacityNodeType, RenderNodeType }`

### 公有函数

- `QSGNode()`
- `virtual ~QSGNode()`
- `void appendChildNode(QSGNode *node)`
- `QSGNode * childAtIndex(int i) const`
- `int childCount() const`
- `QSGNode * firstChild() const`
- `QSGNode::Flags flags() const`
- `void insertChildNodeAfter(QSGNode *node, QSGNode *after)`
- `void insertChildNodeBefore(QSGNode *node, QSGNode *before)`
- `virtual bool isSubtreeBlocked() const`
- `QSGNode * lastChild() const`
- `void markDirty(QSGNode::DirtyState bits)`
- `QSGNode * nextSibling() const`
- `QSGNode * parent() const`
- `void prependChildNode(QSGNode *node)`
- `virtual void preprocess()`
- `QSGNode * previousSibling() const`
- `void removeAllChildNodes()`
- `void removeChildNode(QSGNode *node)`
- `void setFlag(QSGNode::Flag f, bool enabled = true)`
- `void setFlags(QSGNode::Flags f, bool enabled = true)`
- `QSGNode::NodeType type() const`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 29 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QSGNode::DirtyStateBitflags QSGNode::DirtyState`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGNode` 暴露的类型声明 `Dirty、State、Bitflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:DirtyStateBitflags QSGNode::DirtyState`。
- 属性名：`QSGNode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QSGNode::Flagflags QSGNode::Flags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGNode` 暴露的类型声明 `Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Flagflags QSGNode::Flags`。
- 属性名：`QSGNode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QSGNode::NodeType`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGNode` 暴露的类型声明 `Node、类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:NodeType`。
- 属性名：`QSGNode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGNode::QSGNode()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSGNode` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QSGNode::~QSGNode()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSGNode` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGNode::appendChildNode(QSGNode *node)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QSGNode` 添加依赖、数据或子对象的 API `appendChildNode`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `node`：类型为 `QSGNode *`。没有默认值，调用时必须提供。传入 `QSGNode *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGNode *QSGNode::childAtIndex(int i) const`

**API 类别：** 成员函数说明

**中文解读：** `QSGNode::childAtIndex` 用于计算、查询或取得与“child、按位置访问、索引”相关的操作。调用时要先确认当前状态和 `i` 的有效范围；返回类型是 `QSGNode *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGNode *`。
- 参数 `i`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QSGNode::childCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGNode::childCount` 用于计算、查询或取得与“child、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGNode *QSGNode::firstChild() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGNode::firstChild` 用于计算、查询或取得与“首项、Child”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGNode *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGNode *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGNode::Flags QSGNode::flags() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGNode::flags` 用于计算、查询或取得与“标志”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGNode::Flags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGNode::Flags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGNode::insertChildNodeAfter(QSGNode *node, QSGNode *after)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QSGNode` 添加依赖、数据或子对象的 API `insertChildNodeAfter`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `node`：类型为 `QSGNode *`。没有默认值，调用时必须提供。传入 `QSGNode *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `after`：类型为 `QSGNode *`。没有默认值，调用时必须提供。传入 `QSGNode *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGNode::insertChildNodeBefore(QSGNode *node, QSGNode *before)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QSGNode` 添加依赖、数据或子对象的 API `insertChildNodeBefore`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `node`：类型为 `QSGNode *`。没有默认值，调用时必须提供。传入 `QSGNode *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `before`：类型为 `QSGNode *`。没有默认值，调用时必须提供。传入 `QSGNode *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] bool QSGNode::isSubtreeBlocked() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSubtreeBlocked`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGNode *QSGNode::lastChild() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGNode::lastChild` 用于计算、查询或取得与“末项、Child”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGNode *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGNode *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGNode::markDirty(QSGNode::DirtyState bits)`

**API 类别：** 成员函数说明

**中文解读：** `QSGNode::markDirty` 用于执行与“mark、Dirty”相关的操作。调用时要先确认当前状态和 `bits` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `bits`：类型为 `QSGNode::DirtyState`。没有默认值，调用时必须提供。传入 `QSGNode::DirtyState` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGNode *QSGNode::nextSibling() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGNode::nextSibling` 用于计算、查询或取得与“移动到下一项、Sibling”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGNode *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGNode *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGNode *QSGNode::parent() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGNode::parent` 用于计算、查询或取得与“父对象”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGNode *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGNode *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGNode::prependChildNode(QSGNode *node)`

**API 类别：** 成员函数说明

**中文解读：** `QSGNode::prependChildNode` 用于执行与“前置追加、Child、Node”相关的操作。调用时要先确认当前状态和 `node` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `node`：类型为 `QSGNode *`。没有默认值，调用时必须提供。传入 `QSGNode *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QSGNode::preprocess()`

**API 类别：** 成员函数说明

**中文解读：** `QSGNode::preprocess` 用于执行与“preprocess”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGNode *QSGNode::previousSibling() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGNode::previousSibling` 用于计算、查询或取得与“previous、Sibling”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGNode *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGNode *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGNode::removeAllChildNodes()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeAllChildNodes`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGNode::removeChildNode(QSGNode *node)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeChildNode`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `node`：类型为 `QSGNode *`。没有默认值，调用时必须提供。传入 `QSGNode *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGNode::setFlag(QSGNode::Flag f, bool enabled = true)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFlag`。调用它会改变 `QSGNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `f`：类型为 `QSGNode::Flag`。没有默认值，调用时必须提供。传入 `QSGNode::Flag` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `enabled`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGNode::setFlags(QSGNode::Flags f, bool enabled = true)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFlags`。调用它会改变 `QSGNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `f`：类型为 `QSGNode::Flags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `enabled`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGNode::NodeType QSGNode::type() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGNode::type` 用于计算、查询或取得与“类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGNode::NodeType`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGNode::NodeType`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags DirtyState`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGNode` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum DirtyStateBit { DirtyMatrix, DirtyNodeAdded, DirtyNodeRemoved, DirtyGeometry, DirtyMaterial, …, DirtySubtreeBlocked }`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGNode` 暴露的类型声明 `Dirty、State、Bit`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum Flag { OwnedByParent, UsePreprocess, OwnsGeometry, OwnsMaterial, OwnsOpaqueMaterial, InternalReserved }`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGNode` 暴露的类型声明 `Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags Flags`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGNode` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

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

`QSGNode` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
