# QQuick3DGeometry

> Qt 6.11.1 · Qt Quick 3D

## 1. 先建立直觉

**一句话定位：** `QQuick3DGeometry` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 3D 在 Qt Quick 中加入 3D 场景、相机、材质、模型和渲染能力。

### 这是什么

`QQuick3DGeometry` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuick3DGeometry>`
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
#include <QQuick3DGeometry>

// QSG 类型只能在 Qt Quick 规定的场景图阶段使用。
// 先确认渲染后端、线程和对象生命周期，再创建或配置对象。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `void addAttribute(QQuick3DGeometry::Attribute::Semantic semantic, int offset, QQuick3DGeometry::Attribute::ComponentType componentType)`
- `void addAttribute(const QQuick3DGeometry::Attribute &attribute)`
- `void addSubset(int offset, int count, const QVector3D &boundsMin, const QVector3D &boundsMax, const QString &name = {})`
- `(since 6.6) void addTargetAttribute(quint32 targetId, QQuick3DGeometry::Attribute::Semantic semantic, int offset, int stride = 0)`
- `(since 6.6) void addTargetAttribute(const QQuick3DGeometry::TargetAttribute &attribute)`
- `QQuick3DGeometry::Attribute attribute(int index) const`
- `int attributeCount() const`
- `QVector3D boundsMax() const`
- `QVector3D boundsMin() const`
- `void clear()`
- `QByteArray indexData() const`
- `QQuick3DGeometry::PrimitiveType primitiveType() const`
- `void setBounds(const QVector3D &min, const QVector3D &max)`
- `void setIndexData(const QByteArray &data)`
- `void setIndexData(int offset, const QByteArray &data)`
- `void setPrimitiveType(QQuick3DGeometry::PrimitiveType type)`
- `void setStride(int stride)`
- `(since 6.6) void setTargetData(const QByteArray &data)`
- `(since 6.6) void setTargetData(int offset, const QByteArray &data)`
- `void setVertexData(const QByteArray &data)`
- `void setVertexData(int offset, const QByteArray &data)`
- `int stride() const`
- `QVector3D subsetBoundsMax(int subset) const`
- `QVector3D subsetBoundsMin(int subset) const`
- `int subsetCount() const`
- `int subsetCount(int subset) const`
- `QString subsetName(int subset) const`
- `int subsetOffset(int subset) const`
- `(since 6.6) QQuick3DGeometry::TargetAttribute targetAttribute(int index) const`
- `(since 6.6) int targetAttributeCount() const`
- `(since 6.6) QByteArray targetData() const`
- `QByteArray vertexData() const`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 32 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `void QQuick3DGeometry::addAttribute(QQuick3DGeometry::Attribute::Semantic semantic, int offset, QQuick3DGeometry::Attribute::ComponentType componentType)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QQuick3DGeometry` 添加依赖、数据或子对象的 API `addAttribute`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `semantic`：类型为 `QQuick3DGeometry::Attribute::Semantic`。没有默认值，调用时必须提供。传入 `QQuick3DGeometry::Attribute::Semantic` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `offset`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `componentType`：类型为 `QQuick3DGeometry::Attribute::ComponentType`。没有默认值，调用时必须提供。传入 `QQuick3DGeometry::Attribute::ComponentType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuick3DGeometry::addAttribute(const QQuick3DGeometry::Attribute &attribute)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QQuick3DGeometry` 添加依赖、数据或子对象的 API `addAttribute`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `attribute`：类型为 `const QQuick3DGeometry::Attribute &`。没有默认值，调用时必须提供。传入 `const QQuick3DGeometry::Attribute &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuick3DGeometry::addSubset(int offset, int count, const QVector3D &boundsMin, const QVector3D &boundsMax, const QString &name = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QQuick3DGeometry` 添加依赖、数据或子对象的 API `addSubset`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `offset`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `boundsMin`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `boundsMax`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `name`：类型为 `const QString &`。默认值为 `{}`。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] void QQuick3DGeometry::addTargetAttribute(quint32 targetId, QQuick3DGeometry::Attribute::Semantic semantic, int offset, int stride = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QQuick3DGeometry` 添加依赖、数据或子对象的 API `addTargetAttribute`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `targetId`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `semantic`：类型为 `QQuick3DGeometry::Attribute::Semantic`。没有默认值，调用时必须提供。传入 `QQuick3DGeometry::Attribute::Semantic` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `offset`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stride`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] void QQuick3DGeometry::addTargetAttribute(const QQuick3DGeometry::TargetAttribute &attribute)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QQuick3DGeometry` 添加依赖、数据或子对象的 API `addTargetAttribute`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `attribute`：类型为 `const QQuick3DGeometry::TargetAttribute &`。没有默认值，调用时必须提供。传入 `const QQuick3DGeometry::TargetAttribute &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQuick3DGeometry::Attribute QQuick3DGeometry::attribute(int index) const`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DGeometry::attribute` 用于计算、查询或取得与“attribute”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QQuick3DGeometry::Attribute`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuick3DGeometry::Attribute`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QQuick3DGeometry::attributeCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DGeometry::attributeCount` 用于计算、查询或取得与“attribute、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVector3D QQuick3DGeometry::boundsMax() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DGeometry::boundsMax` 用于计算、查询或取得与“bounds、Max”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVector3D`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVector3D`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVector3D QQuick3DGeometry::boundsMin() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DGeometry::boundsMin` 用于计算、查询或取得与“bounds、Min”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVector3D`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVector3D`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuick3DGeometry::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QQuick3DGeometry::indexData() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DGeometry::indexData` 用于计算、查询或取得与“索引、数据访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQuick3DGeometry::PrimitiveType QQuick3DGeometry::primitiveType() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DGeometry::primitiveType` 用于计算、查询或取得与“primitive、类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQuick3DGeometry::PrimitiveType`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuick3DGeometry::PrimitiveType`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuick3DGeometry::setBounds(const QVector3D &min, const QVector3D &max)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBounds`。调用它会改变 `QQuick3DGeometry` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `min`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `max`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuick3DGeometry::setIndexData(const QByteArray &data)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setIndexData`。调用它会改变 `QQuick3DGeometry` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuick3DGeometry::setIndexData(int offset, const QByteArray &data)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setIndexData`。调用它会改变 `QQuick3DGeometry` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `offset`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuick3DGeometry::setPrimitiveType(QQuick3DGeometry::PrimitiveType type)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPrimitiveType`。调用它会改变 `QQuick3DGeometry` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `type`：类型为 `QQuick3DGeometry::PrimitiveType`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuick3DGeometry::setStride(int stride)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStride`。调用它会改变 `QQuick3DGeometry` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `stride`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] void QQuick3DGeometry::setTargetData(const QByteArray &data)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTargetData`。调用它会改变 `QQuick3DGeometry` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] void QQuick3DGeometry::setTargetData(int offset, const QByteArray &data)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTargetData`。调用它会改变 `QQuick3DGeometry` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `offset`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuick3DGeometry::setVertexData(const QByteArray &data)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVertexData`。调用它会改变 `QQuick3DGeometry` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuick3DGeometry::setVertexData(int offset, const QByteArray &data)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVertexData`。调用它会改变 `QQuick3DGeometry` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `offset`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QQuick3DGeometry::stride() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DGeometry::stride` 用于计算、查询或取得与“stride”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVector3D QQuick3DGeometry::subsetBoundsMax(int subset) const`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DGeometry::subsetBoundsMax` 用于计算、查询或取得与“subset、Bounds、Max”相关的操作。调用时要先确认当前状态和 `subset` 的有效范围；返回类型是 `QVector3D`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVector3D`。
- 参数 `subset`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVector3D QQuick3DGeometry::subsetBoundsMin(int subset) const`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DGeometry::subsetBoundsMin` 用于计算、查询或取得与“subset、Bounds、Min”相关的操作。调用时要先确认当前状态和 `subset` 的有效范围；返回类型是 `QVector3D`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVector3D`。
- 参数 `subset`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QQuick3DGeometry::subsetCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DGeometry::subsetCount` 用于计算、查询或取得与“subset、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QQuick3DGeometry::subsetCount(int subset) const`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DGeometry::subsetCount` 用于计算、查询或取得与“subset、数量统计”相关的操作。调用时要先确认当前状态和 `subset` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `subset`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QQuick3DGeometry::subsetName(int subset) const`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DGeometry::subsetName` 用于计算、查询或取得与“subset、名称”相关的操作。调用时要先确认当前状态和 `subset` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `subset`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QQuick3DGeometry::subsetOffset(int subset) const`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DGeometry::subsetOffset` 用于计算、查询或取得与“subset、Offset”相关的操作。调用时要先确认当前状态和 `subset` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `subset`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QQuick3DGeometry::TargetAttribute QQuick3DGeometry::targetAttribute(int index) const`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DGeometry::targetAttribute` 用于计算、查询或取得与“目标、Attribute”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QQuick3DGeometry::TargetAttribute`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuick3DGeometry::TargetAttribute`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] int QQuick3DGeometry::targetAttributeCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DGeometry::targetAttributeCount` 用于计算、查询或取得与“目标、Attribute、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QByteArray QQuick3DGeometry::targetData() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DGeometry::targetData` 用于计算、查询或取得与“目标、数据访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QQuick3DGeometry::vertexData() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuick3DGeometry::vertexData` 用于计算、查询或取得与“vertex、数据访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
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

`QQuick3DGeometry` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
