# QSGImageNode

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QSGImageNode` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QSGImageNode` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSGImageNode>`
- 继承自：QSGGeometryNode
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

- `enum TextureCoordinatesTransformFlag { NoTransform, MirrorHorizontally, MirrorVertically }`
- `flags TextureCoordinatesTransformMode`

### 公有函数

- `virtual QSGTexture::AnisotropyLevel anisotropyLevel() const = 0`
- `virtual QSGTexture::Filtering filtering() const = 0`
- `virtual QSGTexture::Filtering mipmapFiltering() const = 0`
- `virtual bool ownsTexture() const = 0`
- `virtual QRectF rect() const = 0`
- `virtual void setAnisotropyLevel(QSGTexture::AnisotropyLevel level) = 0`
- `virtual void setFiltering(QSGTexture::Filtering filtering) = 0`
- `virtual void setMipmapFiltering(QSGTexture::Filtering filtering) = 0`
- `virtual void setOwnsTexture(bool owns) = 0`
- `virtual void setRect(const QRectF &rect) = 0`
- `void setRect(qreal x, qreal y, qreal w, qreal h)`
- `virtual void setSourceRect(const QRectF &rect) = 0`
- `void setSourceRect(qreal x, qreal y, qreal w, qreal h)`
- `virtual void setTexture(QSGTexture *texture) = 0`
- `virtual void setTextureCoordinatesTransform(QSGImageNode::TextureCoordinatesTransformMode mode) = 0`
- `virtual QRectF sourceRect() const = 0`
- `virtual QSGTexture * texture() const = 0`
- `virtual QSGImageNode::TextureCoordinatesTransformMode textureCoordinatesTransform() const = 0`

### 静态公有成员

- `void rebuildGeometry(QSGGeometry *g, QSGTexture *texture, const QRectF &rect, QRectF sourceRect, QSGImageNode::TextureCoordinatesTransformMode texCoordMode)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 22 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QSGImageNode::TextureCoordinatesTransformFlagflags QSGImageNode::TextureCoordinatesTransformMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGImageNode` 暴露的类型声明 `Texture、Coordinates、Transform、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:TextureCoordinatesTransformFlagflags QSGImageNode::TextureCoordinatesTransformMode`。
- 属性名：`QSGImageNode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSGTexture::AnisotropyLevel QSGImageNode::anisotropyLevel() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGImageNode::anisotropyLevel` 用于计算、查询或取得与“anisotropy、Level”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGTexture::AnisotropyLevel`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGTexture::AnisotropyLevel`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSGTexture::Filtering QSGImageNode::filtering() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGImageNode::filtering` 用于计算、查询或取得与“filtering”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGTexture::Filtering`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGTexture::Filtering`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSGTexture::Filtering QSGImageNode::mipmapFiltering() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGImageNode::mipmapFiltering` 用于计算、查询或取得与“mipmap、Filtering”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGTexture::Filtering`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGTexture::Filtering`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] bool QSGImageNode::ownsTexture() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGImageNode::ownsTexture` 用于计算、查询或取得与“owns、Texture”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QSGImageNode::rebuildGeometry(QSGGeometry *g, QSGTexture *texture, const QRectF &rect, QRectF sourceRect, QSGImageNode::TextureCoordinatesTransformMode texCoordMode)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `rebuildGeometry`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `g`：类型为 `QSGGeometry *`。没有默认值，调用时必须提供。传入 `QSGGeometry *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `texture`：类型为 `QSGTexture *`。没有默认值，调用时必须提供。传入 `QSGTexture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。
- 参数 `sourceRect`：类型为 `QRectF`。没有默认值，调用时必须提供。传入 `QRectF` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `texCoordMode`：类型为 `QSGImageNode::TextureCoordinatesTransformMode`。没有默认值，调用时必须提供。传入 `QSGImageNode::TextureCoordinatesTransformMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QRectF QSGImageNode::rect() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGImageNode::rect` 用于计算、查询或取得与“rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGImageNode::setAnisotropyLevel(QSGTexture::AnisotropyLevel level)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAnisotropyLevel`。调用它会改变 `QSGImageNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `level`：类型为 `QSGTexture::AnisotropyLevel`。没有默认值，调用时必须提供。传入 `QSGTexture::AnisotropyLevel` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGImageNode::setFiltering(QSGTexture::Filtering filtering)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFiltering`。调用它会改变 `QSGImageNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `filtering`：类型为 `QSGTexture::Filtering`。没有默认值，调用时必须提供。传入 `QSGTexture::Filtering` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGImageNode::setMipmapFiltering(QSGTexture::Filtering filtering)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMipmapFiltering`。调用它会改变 `QSGImageNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `filtering`：类型为 `QSGTexture::Filtering`。没有默认值，调用时必须提供。传入 `QSGTexture::Filtering` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGImageNode::setOwnsTexture(bool owns)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setOwnsTexture`。调用它会改变 `QSGImageNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `owns`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGImageNode::setRect(const QRectF &rect)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRect`。调用它会改变 `QSGImageNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGImageNode::setRect(qreal x, qreal y, qreal w, qreal h)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRect`。调用它会改变 `QSGImageNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGImageNode::setSourceRect(const QRectF &rect)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSourceRect`。调用它会改变 `QSGImageNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGImageNode::setSourceRect(qreal x, qreal y, qreal w, qreal h)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSourceRect`。调用它会改变 `QSGImageNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGImageNode::setTexture(QSGTexture *texture)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTexture`。调用它会改变 `QSGImageNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `texture`：类型为 `QSGTexture *`。没有默认值，调用时必须提供。传入 `QSGTexture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGImageNode::setTextureCoordinatesTransform(QSGImageNode::TextureCoordinatesTransformMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTextureCoordinatesTransform`。调用它会改变 `QSGImageNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QSGImageNode::TextureCoordinatesTransformMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QRectF QSGImageNode::sourceRect() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGImageNode::sourceRect` 用于计算、查询或取得与“来源、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSGTexture *QSGImageNode::texture() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGImageNode::texture` 用于计算、查询或取得与“texture”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGTexture *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGTexture *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSGImageNode::TextureCoordinatesTransformMode QSGImageNode::textureCoordinatesTransform() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGImageNode::textureCoordinatesTransform` 用于计算、查询或取得与“texture、Coordinates、Transform”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGImageNode::TextureCoordinatesTransformMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGImageNode::TextureCoordinatesTransformMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum TextureCoordinatesTransformFlag { NoTransform, MirrorHorizontally, MirrorVertically }`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGImageNode` 暴露的类型声明 `Texture、Coordinates、Transform、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags TextureCoordinatesTransformMode`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGImageNode` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

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

`QSGImageNode` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
