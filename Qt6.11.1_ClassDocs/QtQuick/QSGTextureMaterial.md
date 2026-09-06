# QSGTextureMaterial

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QSGTextureMaterial` 是 Qt Quick 场景图的带透明纹理材质，使用继承自 QSGOpaqueTextureMaterial 的纹理、过滤和环绕设置来绘制纹理几何。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QSGTextureMaterial` 是 Qt Quick 场景图的带透明纹理材质，使用继承自 QSGOpaqueTextureMaterial 的纹理、过滤和环绕设置来绘制纹理几何。

**内部模型：** 材质不拥有几何节点；它描述渲染状态并引用 QSGTexture。与不透明材质相比，它用于需要 alpha 混合的纹理。纹理、材质和节点必须在场景图允许的同步/渲染阶段管理，并遵守渲染线程规则。

**适用场景：** 自定义 QQuickItem 在 `updatePaintNode()` 中构建 QSGGeometryNode，并需要绘制可能带透明度的纹理时使用。

**典型调用链：** 取得/创建 QSGTexture -> 创建 QSGTextureMaterial -> setTexture -> 设置 filtering/mipmap/wrap -> 交给 QSGGeometryNode -> 标记节点拥有材质。

**先记住的坑：** 不要在普通 GUI 业务代码中随意操作；确认材质与纹理透明语义匹配；不要在错误线程销毁 GPU 资源；材质引用的纹理必须保持有效。

## 2. 依赖与对象关系

- 头文件：`#include <QSGTextureMaterial>`
- 继承自：QSGOpaqueTextureMaterial
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
target_link_libraries(mytarget PRIVATE Qt6::Quick)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

材质不拥有几何节点；它描述渲染状态并引用 QSGTexture。与不透明材质相比，它用于需要 alpha 混合的纹理。纹理、材质和节点必须在场景图允许的同步/渲染阶段管理，并遵守渲染线程规则。

### 状态、生命周期和线程

**生命周期：** 场景图节点和材质的有效期受窗口、组件和渲染阶段控制；纹理、材质和几何通常要在正确的 render context 中创建/释放。节点被删除或场景图失效后，底层 GPU 资源不能继续使用。

**状态与结果：** 区分 GUI/同步阶段、渲染阶段、节点 dirty 状态、纹理状态和后端能力。改变节点属性通常要标记更新，不能在错误阶段直接修改资源；材质是否可用还受默认后端限制。

**线程与事件循环：** QSG 类型经常运行在 render thread，不能从 GUI 线程或后台线程随意读写。通过 QQuickItem 的同步接口在规定阶段交换数据，避免跨线程共享 GPU 资源。

## 3. 直接使用

自定义 QQuickItem 在 `updatePaintNode()` 中构建 QSGGeometryNode，并需要绘制可能带透明度的纹理时使用。 使用时通常按这个过程组织：取得/创建 QSGTexture -> 创建 QSGTextureMaterial -> setTexture -> 设置 filtering/mipmap/wrap -> 交给 QSGGeometryNode -> 标记节点拥有材质。

```cpp
auto *material = new QSGTextureMaterial;
material->setTexture(texture);
material->setFiltering(QSGTexture::Linear);
node->setMaterial(material);
node->setFlag(QSGNode::OwnsMaterial);
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 配套与继承 API

- `void QSGOpaqueTextureMaterial::setTexture(QSGTexture *texture)`
- `QSGTexture *QSGOpaqueTextureMaterial::texture() const`
- `void QSGOpaqueTextureMaterial::setFiltering(QSGTexture::Filtering filtering)`
- `void QSGOpaqueTextureMaterial::setMipmapFiltering(QSGTexture::Filtering filtering)`
- `void QSGOpaqueTextureMaterial::setHorizontalWrapMode(QSGTexture::WrapMode mode)`
- `void QSGOpaqueTextureMaterial::setVerticalWrapMode(QSGTexture::WrapMode mode)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `void QSGOpaqueTextureMaterial::setTexture(QSGTexture *texture)`

**作用与语义：**

将这些材料的质地设定为`texture`。
材质并不拥有纹理的所有权。

### `QSGTexture *QSGOpaqueTextureMaterial::texture() const`

**作用与语义：**

返回该纹理材质的纹理。

### `void QSGOpaqueTextureMaterial::setFiltering(QSGTexture::Filtering filtering)`

**作用与语义：**

把过滤设置为`filtering`。
过滤模式是在纹理实例绑定渲染前设置的。

### `void QSGOpaqueTextureMaterial::setMipmapFiltering(QSGTexture::Filtering filtering)`

**作用与语义：**

将mipmap模式设置为`filtering`。
mipmap过滤模式是在纹理实例被绑定渲染之前设置的。
如果纹理不支持mipmapping，启用mipmapping也无效。

### `void QSGOpaqueTextureMaterial::setHorizontalWrapMode(QSGTexture::WrapMode mode)`

**作用与语义：**

将水平包裹模式设置为`mode`。
水平包裹模式是在纹理实例绑定渲染前设置的。

### `void QSGOpaqueTextureMaterial::setVerticalWrapMode(QSGTexture::WrapMode mode)`

**作用与语义：**

将垂直包裹模式设置为`mode`。
垂直包裹模式是在纹理实例绑定渲染前设置的。

## 6. 深入实践与常见坑

### 生命周期和资源边界

场景图节点和材质的有效期受窗口、组件和渲染阶段控制；纹理、材质和几何通常要在正确的 render context 中创建/释放。节点被删除或场景图失效后，底层 GPU 资源不能继续使用。

### 状态和错误边界

区分 GUI/同步阶段、渲染阶段、节点 dirty 状态、纹理状态和后端能力。改变节点属性通常要标记更新，不能在错误阶段直接修改资源；材质是否可用还受默认后端限制。

### 线程边界

QSG 类型经常运行在 render thread，不能从 GUI 线程或后台线程随意读写。通过 QQuickItem 的同步接口在规定阶段交换数据，避免跨线程共享 GPU 资源。

### 最容易出现的错误

不要在普通 GUI 业务代码中随意操作；确认材质与纹理透明语义匹配；不要在错误线程销毁 GPU 资源；材质引用的纹理必须保持有效。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSGTextureMaterial` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
