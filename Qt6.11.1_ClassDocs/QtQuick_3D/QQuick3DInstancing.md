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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `depthSortingEnabled : bool`

**作用与语义：**

保持实例表的深度排序启用值。启用时，实例从距离摄像机最远的实例到最近的实例（即从后到前）排序和渲染。如果禁用（这是默认设置），实例将按照实例表中指定的顺序渲染。
注意：实例之间仅相互排序。实例不会与场景中其他对象进行排序。
注意：排序会增加帧准备时间，尤其是在大量实例数下。

**如何使用：** 调用 `depthSortingEnabled()` 读取当前值；它不会修改应用状态。

### `hasTransparency : bool`

**作用与语义：**

如果实例表包含渲染模型时应使用的α值，则将该属性设为true。该属性仅在模型不透明时才有影响：如果模型具有透明的`material`或`opacity`小于1，则无论如何都会使用表中的alpha值。
注意：启用 alpha 混合在实例重叠时可能会引发渲染问题。详情请参见 alpha 混合和实例文档。

**如何使用：** 调用 `hasTransparency()` 读取当前值；它不会修改应用状态。

### `instanceCountOverride : int`

**作用与语义：**

设置该属性限制实例数量，而无需重新生成或重新上传实例表。这允许非常低成本地制作渲染实例数量的动画。

**如何使用：** 调用 `instanceCountOverride()` 读取当前值；它不会修改应用状态。

### `[since 6.9] shadowBoundsMaximum : QVector3D`

**作用与语义：**

设定计算实例表中模型阴影映射边界时所用的最大边界。
默认值：`(-1, -1, -1)`。
注意：只有当 `shadowBoundsMinimum` 的相关分量小于 shadowBoundsMaximum 中时，该属性才被启用。否则边界会自动计算。

**如何使用：** 调用 `shadowBoundsMaximum()` 读取当前值；它不会修改应用状态。

### `[since 6.9] shadowBoundsMinimum : QVector3D`

**作用与语义：**

设置计算实例表中模型阴影映射边界时使用的最小界限。
默认值：`(1, 1, 1)`。
注意：只有当shadowBoundsMinimal的相关分量小于`shadowBoundsMaximum`中时，该属性才被启用。否则边界会自动计算。

**如何使用：** 调用 `shadowBoundsMinimum()` 读取当前值；它不会修改应用状态。

### `[static protected] QQuick3DInstancing::InstanceTableEntry QQuick3DInstancing::calculateTableEntry(const QVector3D &position, const QVector3D &scale, const QVector3D &eulerRotation, const QColor &color, const QVector4D &customData = {})`

**作用与语义：**

将`position` `scale` `eulerRotation` `color`和`customData`转换为标准顶点着色器预期的实例表格式。典型模式：

**官方示例：**

```cpp
 QByteArray MyInstanceTable::getInstanceBuffer(int *instanceCount)
 {
     QByteArray instanceData;

     ...

     auto entry = calculateTableEntry({xPos, yPos, zPos}, {xScale, yScale, zScale}, {xRot, yRot, zRot}, color, {});
     instanceData.append(reinterpret_cast<const char *>(&entry), sizeof(entry));
```

### `[static protected] QQuick3DInstancing::InstanceTableEntry QQuick3DInstancing::calculateTableEntryFromQuaternion(const QVector3D &position, const QVector3D &scale, const QQuaternion &rotation, const QColor &color, const QVector4D &customData = {})`

**作用与语义：**

将`position` `scale` `rotation` `color`和 `customData` 转换为标准顶点着色器预期的实例表格式。
这和`calculateTableEntry()`相同，只是用四元数来指定旋转。

### `[pure virtual protected] QByteArray QQuick3DInstancing::getInstanceBuffer(int *instanceCount)`

**作用与语义：**

实现该函数返回实例表的内容。实例数量应以 `instanceCount` 返回。子类负责如有必要缓存结果。如果实例表发生变化，子类应调用 `markDirty()`。

### `[protected] void QQuick3DInstancing::markDirty()`

**作用与语义：**

标记实例数据已更改，必须重新上传。

### `bool depthSortingEnabled() const`

**作用与语义：**

保持实例表的深度排序启用值。启用时，实例从距离摄像机最远的实例到最近的实例（即从后到前）排序和渲染。如果禁用（这是默认设置），实例将按照实例表中指定的顺序渲染。
注意：实例之间仅相互排序。实例不会与场景中其他对象进行排序。
注意：排序会增加帧准备时间，尤其是在大量实例数下。

**如何使用：** 调用 `depthSortingEnabled()` 读取当前值；它不会修改应用状态。

### `bool hasTransparency() const`

**作用与语义：**

如果实例表包含渲染模型时应使用的α值，则将该属性设为true。该属性仅在模型不透明时才有影响：如果模型具有透明的`material`或`opacity`小于1，则无论如何都会使用表中的alpha值。
注意：启用 alpha 混合在实例重叠时可能会引发渲染问题。详情请参见 alpha 混合和实例文档。

**如何使用：** 调用 `hasTransparency()` 读取当前值；它不会修改应用状态。

### `int instanceCountOverride() const`

**作用与语义：**

设置该属性限制实例数量，而无需重新生成或重新上传实例表。这允许非常低成本地制作渲染实例数量的动画。

**如何使用：** 调用 `instanceCountOverride()` 读取当前值；它不会修改应用状态。

### `QVector3D shadowBoundsMaximum() const`

**作用与语义：**

设定计算实例表中模型阴影映射边界时所用的最大边界。
默认值：`(-1, -1, -1)`。
注意：只有当 `shadowBoundsMinimum` 的相关分量小于 shadowBoundsMaximum 中时，该属性才被启用。否则边界会自动计算。

**如何使用：** 调用 `shadowBoundsMaximum()` 读取当前值；它不会修改应用状态。

### `QVector3D shadowBoundsMinimum() const`

**作用与语义：**

设置计算实例表中模型阴影映射边界时使用的最小界限。
默认值：`(1, 1, 1)`。
注意：只有当shadowBoundsMinimal的相关分量小于`shadowBoundsMaximum`中时，该属性才被启用。否则边界会自动计算。

**如何使用：** 调用 `shadowBoundsMinimum()` 读取当前值；它不会修改应用状态。

### `void setDepthSortingEnabled(bool enabled)`

**作用与语义：**

保持实例表的深度排序启用值。启用时，实例从距离摄像机最远的实例到最近的实例（即从后到前）排序和渲染。如果禁用（这是默认设置），实例将按照实例表中指定的顺序渲染。
注意：实例之间仅相互排序。实例不会与场景中其他对象进行排序。
注意：排序会增加帧准备时间，尤其是在大量实例数下。

**如何使用：** 调用 `setDepthSortingEnabled(...)` 修改 `depthSortingEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setHasTransparency(bool hasTransparency)`

**作用与语义：**

如果实例表包含渲染模型时应使用的α值，则将该属性设为true。该属性仅在模型不透明时才有影响：如果模型具有透明的`material`或`opacity`小于1，则无论如何都会使用表中的alpha值。
注意：启用 alpha 混合在实例重叠时可能会引发渲染问题。详情请参见 alpha 混合和实例文档。

**如何使用：** 调用 `setHasTransparency(...)` 修改 `hasTransparency`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setInstanceCountOverride(int instanceCountOverride)`

**作用与语义：**

设置该属性限制实例数量，而无需重新生成或重新上传实例表。这允许非常低成本地制作渲染实例数量的动画。

**如何使用：** 调用 `setInstanceCountOverride(...)` 修改 `instanceCountOverride`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setShadowBoundsMaximum(const QVector3D &newShadowBoundsMinimum)`

**作用与语义：**

设定计算实例表中模型阴影映射边界时所用的最大边界。
默认值：`(-1, -1, -1)`。
注意：只有当 `shadowBoundsMinimum` 的相关分量小于 shadowBoundsMaximum 中时，该属性才被启用。否则边界会自动计算。

**如何使用：** 调用 `setShadowBoundsMaximum(...)` 修改 `shadowBoundsMaximum`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setShadowBoundsMinimum(const QVector3D &newShadowBoundsMinimum)`

**作用与语义：**

设置计算实例表中模型阴影映射边界时使用的最小界限。
默认值：`(1, 1, 1)`。
注意：只有当shadowBoundsMinimal的相关分量小于`shadowBoundsMaximum`中时，该属性才被启用。否则边界会自动计算。

**如何使用：** 调用 `setShadowBoundsMinimum(...)` 修改 `shadowBoundsMinimum`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void depthSortingEnabledChanged()`

**作用与语义：**

保持实例表的深度排序启用值。启用时，实例从距离摄像机最远的实例到最近的实例（即从后到前）排序和渲染。如果禁用（这是默认设置），实例将按照实例表中指定的顺序渲染。
注意：实例之间仅相互排序。实例不会与场景中其他对象进行排序。
注意：排序会增加帧准备时间，尤其是在大量实例数下。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `depthSortingEnabled` 的变化，不要把它当作普通函数主动调用。

### `void hasTransparencyChanged()`

**作用与语义：**

如果实例表包含渲染模型时应使用的α值，则将该属性设为true。该属性仅在模型不透明时才有影响：如果模型具有透明的`material`或`opacity`小于1，则无论如何都会使用表中的alpha值。
注意：启用 alpha 混合在实例重叠时可能会引发渲染问题。详情请参见 alpha 混合和实例文档。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `hasTransparency` 的变化，不要把它当作普通函数主动调用。

### `void instanceCountOverrideChanged()`

**作用与语义：**

设置该属性限制实例数量，而无需重新生成或重新上传实例表。这允许非常低成本地制作渲染实例数量的动画。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `instanceCountOverride` 的变化，不要把它当作普通函数主动调用。

### `void shadowBoundsMaximumChanged()`

**作用与语义：**

设定计算实例表中模型阴影映射边界时所用的最大边界。
默认值：`(-1, -1, -1)`。
注意：只有当 `shadowBoundsMinimum` 的相关分量小于 shadowBoundsMaximum 中时，该属性才被启用。否则边界会自动计算。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `shadowBoundsMaximum` 的变化，不要把它当作普通函数主动调用。

### `void shadowBoundsMinimumChanged()`

**作用与语义：**

设置计算实例表中模型阴影映射边界时使用的最小界限。
默认值：`(1, 1, 1)`。
注意：只有当shadowBoundsMinimal的相关分量小于`shadowBoundsMaximum`中时，该属性才被启用。否则边界会自动计算。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `shadowBoundsMinimum` 的变化，不要把它当作普通函数主动调用。

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
