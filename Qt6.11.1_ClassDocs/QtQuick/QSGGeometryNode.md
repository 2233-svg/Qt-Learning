# QSGGeometryNode

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QSGGeometryNode` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QSGGeometryNode` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSGGeometryNode>`
- 继承自：QSGBasicGeometryNode
- 直接派生类：QSGImageNode、QSGRectangleNode、QSGSimpleRectNode,、QSGSimpleTextureNode

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

### 公有函数

- `QSGGeometryNode()`
- `virtual ~QSGGeometryNode() override`
- `QSGMaterial * material() const`
- `QSGMaterial * opaqueMaterial() const`
- `void setMaterial(QSGMaterial *material)`
- `void setOpaqueMaterial(QSGMaterial *material)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QSGGeometryNode::QSGGeometryNode()`

**作用与语义：**

创建一个没有几何体和材质的新几何节点。

### `[override virtual noexcept] QSGGeometryNode::~QSGGeometryNode()`

**作用与语义：**

删除该几何节点。
`QSGNode::OwnsMaterial`、`QSGNode::OwnsOpaqueMaterial`和`QSGNode::OwnsGeometry`这些标志决定几何节点是否也应该删除材质和几何体。默认情况下，这些标志是禁用的。

### `QSGMaterial *QSGGeometryNode::material() const`

**作用与语义：**

归还`QSGGeometryNode`材料。

### `QSGMaterial *QSGGeometryNode::opaqueMaterial() const`

**作用与语义：**

返回`QSGGeometryNode`的不透明材料。

### `void QSGGeometryNode::setMaterial(QSGMaterial *material)`

**作用与语义：**

将该几何节点的材质设置为`material`。
几何节点必须先有材质，才能添加到场景图中。
如果材料在未再次调用 setMaterial() 的情况下更改，用户还必须使用 `QSGNode::markDirty()` 标记该材质为脏材料。

### `void QSGGeometryNode::setOpaqueMaterial(QSGMaterial *material)`

**作用与语义：**

将该几何形状的不透明材料设置为`material`。
如果不透明度非空且几何体的继承不透明度为1，渲染器会优先选择不透明材质而非默认材质（如`material()`函数返回）。
不透明度指的是场景图的不透明度，但材质仍允许将`QSGMaterial::Blending`设为真并绘制透明像素。
如果在未再次调用 setOpaqueMaterial() 的情况下更改材质，用户还必须用 `QSGNode::markDirty()` 标记该不透明材料为脏材料。

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

`QSGGeometryNode` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
