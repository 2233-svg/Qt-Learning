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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSGNode::DirtyStateBitflags QSGNode::DirtyState`

**作用与语义：**

`QSGNode::markDirty()`用来表示场景图的变化。
- `QSGNode::DirtyMatrix`：`0x0100`;`QSGTransformNode`中的矩阵发生了变化。
- `QSGNode::DirtyNodeAdded`：`0x0400`;新增了一个节点。
- `QSGNode::DirtyNodeRemoved`：`0x0800`;一个节点被移除。
- `QSGNode::DirtyGeometry`：`0x1000`;`QSGGeometryNode`的几何形状发生了变化。
- `QSGNode::DirtyMaterial`：`0x2000`;`QSGGeometryNode`的材料发生了变化。
- `QSGNode::DirtyOpacity`：`0x4000`;`QSGOpacityNode`的不透明度发生了变化。
- `QSGNode::DirtySubtreeBlocked`：`0x0080`;子树已被封锁。
DirtyState 类型是 QFlags 的 typedef<DirtyStateBit>。它存储 DirtyStateBit 值的 OR 组合。

### `enum QSGNode::Flagflags QSGNode::Flags`

**作用与语义：**

QSGNode：：Flag enum 描述了 `QSGNode` 上的标志。
- `QSGNode::OwnedByParent`：`0x0001`;该节点归其父节点所有，当父节点被删除时节点也会被删除。
- `QSGNode::UsePreprocess`：`0x0002`;节点的虚拟`preprocess()`函数将在渲染开始前被调用。
- `QSGNode::OwnsGeometry`：`0x00010000`;仅适用于`QSGGeometryNode`和 `QSGClipNode`。节点拥有`QSGGeometry`实例的所有权，当节点被销毁或几何体被分配时，节点会删除该实例。
- `QSGNode::OwnsMaterial`：`0x00020000`;仅适用于`QSGGeometryNode`。节点拥有材料的所有权，当节点被销毁或材料被分配时，节点会删除该材料。
- `QSGNode::OwnsOpaqueMaterial`：`0x00040000`;仅对`QSGGeometryNode`有效。节点拥有不透明材料的所有权，当节点被销毁或材料被分配时，该节点会删除该材料。
- `QSGNode::InternalReserved`：`0x01000000`;保留用于内部使用。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `enum QSGNode::NodeType`

**作用与语义：**

可以用来确定节点类型。
- `QSGNode::BasicNodeType`：`0`;`QSGNode`类型
- `QSGNode::GeometryNodeType`：`1`;`QSGGeometryNode`类型
- `QSGNode::TransformNodeType`：`2`;`QSGTransformNode`类型
- `QSGNode::ClipNodeType`：`3`;`QSGClipNode`类型
- `QSGNode::OpacityNodeType`：`4`;`QSGOpacityNode`类型
- `QSGNode::RenderNodeType`：`6`;`QSGRenderNode`类型

### `QSGNode::QSGNode()`

**作用与语义：**

构造一个新节点。

### `[virtual noexcept] QSGNode::~QSGNode()`

**作用与语义：**

摧毁节点。
该节点中所有设置了`QSGNode::OwnedByParent`标志的子节点也会被删除。

### `void QSGNode::appendChildNode(QSGNode *node)`

**作用与语义：**

将 `node` 附加到该节点的子节点列表中。
节点的排序很重要，因为几何节点会按照添加到场景图的顺序进行渲染。

### `QSGNode *QSGNode::childAtIndex(int i) const`

**作用与语义：**

返回索引`i`的子节点。
子节点内部存储为链表，因此通过索引遍历子节点并不理想。

### `int QSGNode::childCount() const`

**作用与语义：**

返回子节点的数量。

### `QSGNode *QSGNode::firstChild() const`

**作用与语义：**

返回该节点的第一个子节点。
子节点存储在链表中。

### `QSGNode::Flags QSGNode::flags() const`

**作用与语义：**

返回该节点的标志集合。

### `void QSGNode::insertChildNodeAfter(QSGNode *node, QSGNode *after)`

**作用与语义：**

插入 `node` 该节点子节点列表，位于 `after` 指定的节点之后。
节点的排序很重要，因为几何节点会按照添加到场景图的顺序进行渲染。

### `void QSGNode::insertChildNodeBefore(QSGNode *node, QSGNode *before)`

**作用与语义：**

插入`node`该节点的子节点列表，先于`before`指定的节点。
节点的排序很重要，因为几何节点会按照添加到场景图的顺序进行渲染。

### `[virtual] bool QSGNode::isSubtreeBlocked() const`

**作用与语义：**

返回该节点及其子树是否可供使用。
被阻挡的子树不会更新其脏状态，也不会被渲染。
例如，当累积不透明度为0时，`QSGOpacityNode`会返回阻塞的子树。

### `QSGNode *QSGNode::lastChild() const`

**作用与语义：**

返回该节点的最后一个子节点。
子节点存储为链表。

### `void QSGNode::markDirty(QSGNode::DirtyState bits)`

**作用与语义：**

通知所有连接的渲染器该节点有脏`bits`。

### `QSGNode *QSGNode::nextSibling() const`

**作用与语义：**

返回父子节点列表中的节点。
子节点存储为链表。

### `QSGNode *QSGNode::parent() const`

**作用与语义：**

返回该节点的父节点。

### `void QSGNode::prependChildNode(QSGNode *node)`

**作用与语义：**

`node`该节点前加上子节点列表。
节点的排序很重要，因为几何节点会按照添加到场景图的顺序进行渲染。

### `[virtual] void QSGNode::preprocess()`

**作用与语义：**

覆盖该函数，在节点渲染前进行处理。
预处理需要通过设置 `QSGNode::UsePreprocess` 来显式启用。该标志必须在节点添加到场景图之前设置，并且每渲染一帧节点都会调用预处理()函数。
警告：在节点正在进行预处理时，请注意删除节点。在节点自身的预处理调用中，可能会在性能略有下降的情况下删除单个节点。删除包含同样使用预处理节点的子树可能导致分段错误。这是出于性能考虑。

### `QSGNode *QSGNode::previousSibling() const`

**作用与语义：**

返回父节点子节点列表中的前一个节点。
子节点存储为链表。

### `void QSGNode::removeAllChildNodes()`

**作用与语义：**

从该节点的子节点列表中移除所有子节点。

### `void QSGNode::removeChildNode(QSGNode *node)`

**作用与语义：**

从该节点的子节点列表中移除`node`。

### `void QSGNode::setFlag(QSGNode::Flag f, bool enabled = true)`

**作用与语义：**

如果该节点为真，则将该节点的标志设为`f` `enabled`;否则清除该标志。

### `void QSGNode::setFlags(QSGNode::Flags f, bool enabled = true)`

**作用与语义：**

如果该节点为真，则设置该节点`f`的标志`enabled`;否则清除所有标志。

### `QSGNode::NodeType QSGNode::type() const`

**作用与语义：**

返回该节点的类型。节点类型必须是`QSGNode::NodeType`中预定义的类型之一，并且可以安全地将类型投射到对应的类。

### `flags DirtyState`

**作用与语义：**

`QSGNode::markDirty()`用来表示场景图的变化。
- `QSGNode::DirtyMatrix`：`0x0100`;`QSGTransformNode`中的矩阵发生了变化。
- `QSGNode::DirtyNodeAdded`：`0x0400`;新增了一个节点。
- `QSGNode::DirtyNodeRemoved`：`0x0800`;一个节点被移除。
- `QSGNode::DirtyGeometry`：`0x1000`;`QSGGeometryNode`的几何形状发生了变化。
- `QSGNode::DirtyMaterial`：`0x2000`;`QSGGeometryNode`的材料发生了变化。
- `QSGNode::DirtyOpacity`：`0x4000`;`QSGOpacityNode`的不透明度发生了变化。
- `QSGNode::DirtySubtreeBlocked`：`0x0080`;子树已被封锁。
DirtyState 类型是 QFlags 的 typedef<DirtyStateBit>。它存储 DirtyStateBit 值的 OR 组合。

### `enum DirtyStateBit { DirtyMatrix, DirtyNodeAdded, DirtyNodeRemoved, DirtyGeometry, DirtyMaterial, …, DirtySubtreeBlocked }`

**作用与语义：**

`QSGNode::markDirty()`用来表示场景图的变化。
- `QSGNode::DirtyMatrix`：`0x0100`;`QSGTransformNode`中的矩阵发生了变化。
- `QSGNode::DirtyNodeAdded`：`0x0400`;新增了一个节点。
- `QSGNode::DirtyNodeRemoved`：`0x0800`;一个节点被移除。
- `QSGNode::DirtyGeometry`：`0x1000`;`QSGGeometryNode`的几何形状发生了变化。
- `QSGNode::DirtyMaterial`：`0x2000`;`QSGGeometryNode`的材料发生了变化。
- `QSGNode::DirtyOpacity`：`0x4000`;`QSGOpacityNode`的不透明度发生了变化。
- `QSGNode::DirtySubtreeBlocked`：`0x0080`;子树已被封锁。
DirtyState 类型是 QFlags 的 typedef<DirtyStateBit>。它存储 DirtyStateBit 值的 OR 组合。

### `enum Flag { OwnedByParent, UsePreprocess, OwnsGeometry, OwnsMaterial, OwnsOpaqueMaterial, InternalReserved }`

**作用与语义：**

QSGNode：：Flag enum 描述了 `QSGNode` 上的标志。
- `QSGNode::OwnedByParent`：`0x0001`;该节点归其父节点所有，当父节点被删除时节点也会被删除。
- `QSGNode::UsePreprocess`：`0x0002`;节点的虚拟`preprocess()`函数将在渲染开始前被调用。
- `QSGNode::OwnsGeometry`：`0x00010000`;仅适用于`QSGGeometryNode`和 `QSGClipNode`。节点拥有`QSGGeometry`实例的所有权，当节点被销毁或几何体被分配时，节点会删除该实例。
- `QSGNode::OwnsMaterial`：`0x00020000`;仅适用于`QSGGeometryNode`。节点拥有材料的所有权，当节点被销毁或材料被分配时，节点会删除该材料。
- `QSGNode::OwnsOpaqueMaterial`：`0x00040000`;仅对`QSGGeometryNode`有效。节点拥有不透明材料的所有权，当节点被销毁或材料被分配时，该节点会删除该材料。
- `QSGNode::InternalReserved`：`0x01000000`;保留用于内部使用。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `flags Flags`

**作用与语义：**

QSGNode：：Flag enum 描述了 `QSGNode` 上的标志。
- `QSGNode::OwnedByParent`：`0x0001`;该节点归其父节点所有，当父节点被删除时节点也会被删除。
- `QSGNode::UsePreprocess`：`0x0002`;节点的虚拟`preprocess()`函数将在渲染开始前被调用。
- `QSGNode::OwnsGeometry`：`0x00010000`;仅适用于`QSGGeometryNode`和 `QSGClipNode`。节点拥有`QSGGeometry`实例的所有权，当节点被销毁或几何体被分配时，节点会删除该实例。
- `QSGNode::OwnsMaterial`：`0x00020000`;仅适用于`QSGGeometryNode`。节点拥有材料的所有权，当节点被销毁或材料被分配时，节点会删除该材料。
- `QSGNode::OwnsOpaqueMaterial`：`0x00040000`;仅对`QSGGeometryNode`有效。节点拥有不透明材料的所有权，当节点被销毁或材料被分配时，该节点会删除该材料。
- `QSGNode::InternalReserved`：`0x01000000`;保留用于内部使用。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

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
