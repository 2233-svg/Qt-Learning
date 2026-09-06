# QQuick3DObject

> Qt 6.11.1 · Qt Quick 3D

## 1. 先建立直觉

**一句话定位：** `QQuick3DObject` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 3D 在 Qt Quick 中加入 3D 场景、相机、材质、模型和渲染能力。

### 这是什么

`QQuick3DObject` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuick3DObject>`
- 继承自：QObject、QQmlParserStatus
- 直接派生类：QQuick3DGeometry、QQuick3DInstancing、QQuick3DRenderExtension,、QQuick3DTextureData

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

### 状态、生命周期和线程

**生命周期：** 场景图节点和材质的有效期受窗口、组件和渲染阶段控制；纹理、材质和几何通常要在正确的 render context 中创建/释放。节点被删除或场景图失效后，底层 GPU 资源不能继续使用。

**状态与结果：** 区分 GUI/同步阶段、渲染阶段、节点 dirty 状态、纹理状态和后端能力。改变节点属性通常要标记更新，不能在错误阶段直接修改资源；材质是否可用还受默认后端限制。

**线程与事件循环：** QSG 类型经常运行在 render thread，不能从 GUI 线程或后台线程随意读写。通过 QQuickItem 的同步接口在规定阶段交换数据，避免跨线程共享 GPU 资源。

## 3. 直接使用

需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。 使用时通常按这个过程组织：注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

```cpp
#include <QQuick3DObject>

// QSG 类型只能在 Qt Quick 规定的场景图阶段使用。
// 先确认渲染后端、线程和对象生命周期，再创建或配置对象。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `parent : QQuick3DObject*`
- `state : QString`

### 公有函数

- `QQuick3DObject * parentItem() const`
- `void setState(const QString &state)`
- `QString state() const`

### 公有槽函数

- `void setParentItem(QQuick3DObject *parentItem)`

### 信号

- `void parentChanged()`
- `void stateChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `parent : QQuick3DObject*`

**作用与语义：**

该属性在三维场景中保持`Object3D`的父节点。
注意：`Object3D`的父节点不一定与其对象父节点相同。这是必要的，因为对象父节点可能是非类型`Object3D`的项目，例如场景中的根对象。
注意：目前，为了让场景管理器在从C语言中为3D对象做父级时正确处理3D项目，必须在`QObject::setParent`之前调用QQuick3DObject：：setParentItem。不过这一要求可能会在未来版本中有所变化。

**如何使用：** 调用 `parent()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QQuick3DObject *newItem = new QQuick3DObject();
 newItem->setParentItem(parentItem);
 newItem->setParent(parentItem);
```

### `state : QString`

**作用与语义：**

该属性保存对象当前状态的名称。
如果项目处于默认状态，即未设置任何显式状态，则该属性保存为空字符串。同样，可以通过将此属性设置为空字符串将项目恢复到默认状态。

**如何使用：** 调用 `state()` 读取当前值；它不会修改应用状态。

### `QQuick3DObject * parentItem() const`

**作用与语义：**

该属性在三维场景中保持`Object3D`的父节点。
注意：`Object3D`的父节点不一定与其对象父节点相同。这是必要的，因为对象父节点可能是非类型`Object3D`的项目，例如场景中的根对象。
注意：目前，为了让场景管理器在从C语言中为3D对象做父级时正确处理3D项目，必须在`QObject::setParent`之前调用QQuick3DObject：：setParentItem。不过这一要求可能会在未来版本中有所变化。

**如何使用：** 调用 `parentItem()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QQuick3DObject *newItem = new QQuick3DObject();
 newItem->setParentItem(parentItem);
 newItem->setParent(parentItem);
```

### `void setState(const QString &state)`

**作用与语义：**

该属性保存对象当前状态的名称。
如果项目处于默认状态，即未设置任何显式状态，则该属性保存为空字符串。同样，可以通过将此属性设置为空字符串将项目恢复到默认状态。

**如何使用：** 调用 `setState(...)` 修改 `state`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QString state() const`

**作用与语义：**

该属性保存对象当前状态的名称。
如果项目处于默认状态，即未设置任何显式状态，则该属性保存为空字符串。同样，可以通过将此属性设置为空字符串将项目恢复到默认状态。

**如何使用：** 调用 `state()` 读取当前值；它不会修改应用状态。

### `void setParentItem(QQuick3DObject *parentItem)`

**作用与语义：**

该属性在三维场景中保持`Object3D`的父节点。
注意：`Object3D`的父节点不一定与其对象父节点相同。这是必要的，因为对象父节点可能是非类型`Object3D`的项目，例如场景中的根对象。
注意：目前，为了让场景管理器在从C语言中为3D对象做父级时正确处理3D项目，必须在`QObject::setParent`之前调用QQuick3DObject：：setParentItem。不过这一要求可能会在未来版本中有所变化。

**如何使用：** 调用 `setParentItem(...)` 修改 `parent`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 QQuick3DObject *newItem = new QQuick3DObject();
 newItem->setParentItem(parentItem);
 newItem->setParent(parentItem);
```

### `void parentChanged()`

**作用与语义：**

该属性在三维场景中保持`Object3D`的父节点。
注意：`Object3D`的父节点不一定与其对象父节点相同。这是必要的，因为对象父节点可能是非类型`Object3D`的项目，例如场景中的根对象。
注意：目前，为了让场景管理器在从C语言中为3D对象做父级时正确处理3D项目，必须在`QObject::setParent`之前调用QQuick3DObject：：setParentItem。不过这一要求可能会在未来版本中有所变化。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `parent` 的变化，不要把它当作普通函数主动调用。

**官方示例：**

```cpp
 QQuick3DObject *newItem = new QQuick3DObject();
 newItem->setParentItem(parentItem);
 newItem->setParent(parentItem);
```

### `void stateChanged()`

**作用与语义：**

该属性保存对象当前状态的名称。
如果项目处于默认状态，即未设置任何显式状态，则该属性保存为空字符串。同样，可以通过将此属性设置为空字符串将项目恢复到默认状态。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `state` 的变化，不要把它当作普通函数主动调用。

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

`QQuick3DObject` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
