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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `void QQuick3DGeometry::addAttribute(QQuick3DGeometry::Attribute::Semantic semantic, int offset, QQuick3DGeometry::Attribute::ComponentType componentType)`

**作用与语义：**

添加顶点属性描述。每个属性都有一个`semantic`，指定属性的用途及其组件数量，从起点到顶点再到顶点内属性位置的`offset`，以及指定属性类型和大小的`componentType`。
语义可以是以下之一：
- `PositionSemantic`：属性是一个位置。三个分量：x、y 和 z
- `NormalSemantic`：属性是一个法向量。3个分量：x、y和z
- `TexCoord0Semantic`：属性是一个纹理坐标。两个组件：你和 v
- `TexCoord1Semantic`：属性是一个纹理坐标。两个组件：你和 v
- `TangentSemantic`：属性是一个切向量。三个分量：x、y 和 z
- `BinormalSemantic`：属性为双法一向量。三个分量：x、y 和 z
- `JointSemantic`：属性是用于蒙皮的关节索引向量。4个分量：关节索引1-4
- `WeightSemantic`：属性是用于蒙皮的权重矢量。4个组件：关节权重1-4
- `ColorSemantic`：属性是一个顶点颜色矢量。4个分量：r、g、b 和 a
- `TargetPositionSemantic`：属性是第一个变形目标的位置。三个组成部分：x、y 和 z
- `TargetNormalSemantic`：属性是第一个目标的法向量。三个分量：x、y 和 z
- `TargetTangentSemantic`：属性是第一个目标的切向量。3个分量：x、y和z
- `TargetBinormalSemantic`：属性是第一个形态目标的双法向量。3个分量：x、y和z
此外，`semantic`也可以是`IndexSemantic`。在这种情况下，属性不表示顶点缓冲区中的一个条目，而描述索引缓冲区中的索引数据。由于每个顶点总是只有一个索引，`offset`对索引缓冲区来说没有意义，应保持为零。
组件类型可以是以下之一：
- `U16Type`：索引组件类型为无符号的16位整数。仅支持`IndexSemantic`。
- `U32Type`：属性（或索引组件）是一个无符号的32位整数。
- `I32Type`：属性是一个有符号的32位整数。请注意，旧版OpenGL（如2.1或OpenGL ES 2.0）可能不支持该数据类型。
- `F32Type`：属性为单精度浮点。
注意：联合索引数据通常为`I32Type`。`F32Type`也被支持，以便支持不支持整数顶点输入属性的API，如OpenGL ES 2.0。


注意：对于索引数据（`IndexSemantic`），只有U16Type和U32Type是合理的且支持的。


注意：TargetXXX语义将被弃用。`addTargetAttribute`可用于变形目标。这些语义仅支持向后兼容。如果与`addTargetAttribute`和`setTargetData`混合使用，结果无法隔离。

### `void QQuick3DGeometry::addAttribute(const QQuick3DGeometry::Attribute &attribute)`

**作用与语义：**

添加顶点属性描述。每个属性都有语义，指定属性的用途及其组件数量，从起点到顶点的偏移量，再到顶点内属性位置，以及一个 componentType，指定属性的数据类型和大小。

### `void QQuick3DGeometry::addSubset(int offset, int count, const QVector3D &boundsMin, const QVector3D &boundsMax, const QString &name = {})`

**作用与语义：**

向几何体添加新的子集。子集允许用不同材质渲染几何体的部分。材质在`model`中指定。
如果几何体有索引缓冲区，那么`offset`和`count`是该子集中的原始偏移量和索引的计数。如果几何体只有顶点缓冲区，偏移量是顶点偏移量，计数是子集中的顶点数。
边界`boundsMin`和`boundsMax`应该像几何边界一样包围子集。此外，子集可以有一个`name`。

### `[since 6.6] void QQuick3DGeometry::addTargetAttribute(quint32 targetId, QQuick3DGeometry::Attribute::Semantic semantic, int offset, int stride = 0)`

**作用与语义：**

增加了目标属性描述。每个属性都有其所属的`targetId`、`semantic`（指定属性的用途及其组件数量）、从起始到顶点再到顶点内属性位置的`offset`，以及元素间的字节大小`stride`。
注意：targetId应从0增加且不跳过任何数字，所有目标的属性应相同。
注意：语义与顶点属性相同，但目标属性不允许使用索引语义、JointSementic 和 WeightSemantic。
注意：所有目标属性的componentType必须是F32Type。
注意：如果步幅未被赋予或小于零，则该属性被视为紧密填充。

### `[since 6.6] void QQuick3DGeometry::addTargetAttribute(const QQuick3DGeometry::TargetAttribute &attribute)`

**作用与语义：**

新增了变形目标属性描述。每个属性都有一个目标Id（属性所属）、一个语义（指定属性的用途及其组件数量）、从起点到顶点到顶点内属性位置的偏移量，以及一个步幅（元素之间的字节大小）。

### `QQuick3DGeometry::Attribute QQuick3DGeometry::attribute(int index) const`

**作用与语义：**

返回属性定义编号`index`。
属性定义编号从0到`attributeCount() - 1`。

### `int QQuick3DGeometry::attributeCount() const`

**作用与语义：**

返回该几何定义的属性数量。

### `QVector3D QQuick3DGeometry::boundsMax() const`

**作用与语义：**

返回包围体的最大坐标。

### `QVector3D QQuick3DGeometry::boundsMin() const`

**作用与语义：**

返回包围体的最小坐标。

### `void QQuick3DGeometry::clear()`

**作用与语义：**

将几何体重置到初始状态，清除之前设置的顶点和索引数据以及属性。

### `QByteArray QQuick3DGeometry::indexData() const`

**作用与语义：**

返回索引缓冲区数据。

### `QQuick3DGeometry::PrimitiveType QQuick3DGeometry::primitiveType() const`

**作用与语义：**

返回渲染时使用的原始类型。默认是`Triangles`。

### `void QQuick3DGeometry::setBounds(const QVector3D &min, const QVector3D &max)`

**作用与语义：**

将几何体的包围体积设置为由点`min`和`max`定义的立方体。这用于`picking`。

### `void QQuick3DGeometry::setIndexData(const QByteArray &data)`

**作用与语义：**

将索引缓冲区设置为`data`。要使用索引绘图，添加带有`IndexSemantic`的属性。

### `void QQuick3DGeometry::setIndexData(int offset, const QByteArray &data)`

**作用与语义：**

更新索引缓冲区的一个子集。`offset` 指定偏移量（字节），`data` 表示大小和数据。
该函数不会调整缓冲区大小。如果`offset + data.size()`大于缓冲区当前大小，超额数据将被忽略。
注意：顶点、索引和形态目标数据的部分更新函数无法保证这些变更在内部如何实现。根据底层实现，即使是部分更改也可能导致整个图形资源更新。

### `void QQuick3DGeometry::setPrimitiveType(QQuick3DGeometry::PrimitiveType type)`

**作用与语义：**

将用于渲染的原始类型设置为`type`。
- `Points`：原元是点。
- `LineStrip`：图元是条状中的线。
- `Lines`：原语是列表中的行。
- `TriangleStrip`：这些原件是条状中的三角形。
- `TriangleFan`：这些原语是风扇中的三角形。请注意，运行时可能不支持三角风扇，具体取决于底层图形 API。
- `Triangles`：原语是列表中的三角形。
初始值为`Triangles`。
注意：请注意，三角风扇（TriangleFan）在运行时可能不支持，具体取决于底层的图形API。例如，对于Direct 3D，这种拓扑结构将完全无法使用。
注意：点的点大小以及线条和线条的线宽由`material`控制。但请注意，运行时可能不支持非1的大小，具体取决于底层图形API。

### `void QQuick3DGeometry::setStride(int stride)`

**作用与语义：**

将顶点缓冲区的步幅设置为`stride`，单位为字节。这是缓冲区中两个连续顶点之间的距离。
例如，对于使用`PositionSemantic`、`IndexSemantic`和`ColorSemantic`的几何体，紧密填充、交错的顶点缓冲区步幅为`28`（共七个浮点：三个用于位置，四个用于颜色，索引不包含在顶点缓冲区中）。
注意：`QQuick3DGeometry`期望并仅适用于带有交错属性布局的顶点数据。

### `[since 6.6] void QQuick3DGeometry::setTargetData(const QByteArray &data)`

**作用与语义：**

设置形态目标缓冲区`data`。缓冲区应存储所有形态目标数据。

### `[since 6.6] void QQuick3DGeometry::setTargetData(int offset, const QByteArray &data)`

**作用与语义：**

更新目标缓冲区的子集。`offset` 指定以字节为单位的偏移量，`data` 表示大小和数据。
该函数不会调整缓冲区大小。如果`offset + data.size()`大于缓冲区当前大小，超额数据将被忽略。
注意：顶点、索引和形态目标数据的部分更新函数无法保证这些变更在内部如何实现。根据底层实现，即使是部分更改也可能导致整个图形资源更新。

### `void QQuick3DGeometry::setVertexData(const QByteArray &data)`

**作用与语义：**

设置顶点缓冲区`data`。缓冲区应存储数组中打包的所有顶点数据，如属性定义所述。注意，这不包括带有`IndexSemantic`的属性，这些属性属于索引缓冲区。

### `void QQuick3DGeometry::setVertexData(int offset, const QByteArray &data)`

**作用与语义：**

更新顶点缓冲区的一个子集。`offset` 指定以字节为单位的偏移量，`data` 表示大小和数据。
该函数不会调整缓冲区大小。如果`offset + data.size()`大于缓冲区当前大小，超额数据将被忽略。
注意：顶点、索引和变形目标数据的部分更新函数无法保证这些变更在内部如何实现。根据底层实现，即使是部分更改也可能导致整个图形资源更新。

### `int QQuick3DGeometry::stride() const`

**作用与语义：**

返回顶点缓冲区的字节步幅。

### `QVector3D QQuick3DGeometry::subsetBoundsMax(int subset) const`

**作用与语义：**

返回`subset`的最大界限数。

### `QVector3D QQuick3DGeometry::subsetBoundsMin(int subset) const`

**作用与语义：**

返回`subset`的最小界限数。

### `int QQuick3DGeometry::subsetCount() const`

**作用与语义：**

返回子集的数量。

### `int QQuick3DGeometry::subsetCount(int subset) const`

**作用与语义：**

返回子集的原始计数。

### `QString QQuick3DGeometry::subsetName(int subset) const`

**作用与语义：**

还原`subset`名。

### `int QQuick3DGeometry::subsetOffset(int subset) const`

**作用与语义：**

返回`subset`偏移量到顶点或索引缓冲区。

### `[since 6.6] QQuick3DGeometry::TargetAttribute QQuick3DGeometry::targetAttribute(int index) const`

**作用与语义：**

返回变形目标属性定义编号`index`。
属性定义编号从0到`attributeCount() - 1`。

### `[since 6.6] int QQuick3DGeometry::targetAttributeCount() const`

**作用与语义：**

返回该几何体定义的变形目标属性数量。

### `[since 6.6] QByteArray QQuick3DGeometry::targetData() const`

**作用与语义：**

返回目标缓冲区数据集，按`setTargetData`返回。

### `QByteArray QQuick3DGeometry::vertexData() const`

**作用与语义：**

返回由`setVertexData`返回顶点缓冲区数据集。

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
