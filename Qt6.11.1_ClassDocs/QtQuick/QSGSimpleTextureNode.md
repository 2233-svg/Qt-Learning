# QSGSimpleTextureNode

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QSGSimpleTextureNode` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QSGSimpleTextureNode` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSGSimpleTextureNode>`
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

- `QSGSimpleTextureNode()`
- `virtual ~QSGSimpleTextureNode() override`
- `QSGTexture::Filtering filtering() const`
- `bool ownsTexture() const`
- `QRectF rect() const`
- `void setFiltering(QSGTexture::Filtering filtering)`
- `void setOwnsTexture(bool owns)`
- `void setRect(const QRectF &r)`
- `void setRect(qreal x, qreal y, qreal w, qreal h)`
- `void setSourceRect(const QRectF &r)`
- `void setSourceRect(qreal x, qreal y, qreal w, qreal h)`
- `void setTexture(QSGTexture *texture)`
- `void setTextureCoordinatesTransform(QSGSimpleTextureNode::TextureCoordinatesTransformMode mode)`
- `QRectF sourceRect() const`
- `QSGTexture * texture() const`
- `QSGSimpleTextureNode::TextureCoordinatesTransformMode textureCoordinatesTransform() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSGSimpleTextureNode::TextureCoordinatesTransformFlagflags QSGSimpleTextureNode::TextureCoordinatesTransformMode`

**作用与语义：**

TextureCoordinatesTransformFlag枚举用于指定生成纹理四边形纹理坐标的模式。
- `QSGSimpleTextureNode::NoTransform`：`0x00`;纹理坐标以窗口坐标定向，即原点位于左上角。
- `QSGSimpleTextureNode::MirrorHorizontally`：`0x01`;纹理坐标相对于窗口坐标在水平轴上反转
- `QSGSimpleTextureNode::MirrorVertically`：`0x02`;纹理坐标在垂直轴上相对于窗口坐标反转
TextureCoordinatesTransformMode 类型是 QFlags 的 typedef<TextureCoordinatesTransformFlag>。它存储 TextureCoordinatesTransformFlag 值的 OR 组合。

### `QSGSimpleTextureNode::QSGSimpleTextureNode()`

**作用与语义：**

构建一个新的简单纹理节点。

### `[override virtual noexcept] QSGSimpleTextureNode::~QSGSimpleTextureNode()`

**作用与语义：**

会破坏纹理节点。

### `QSGTexture::Filtering QSGSimpleTextureNode::filtering() const`

**作用与语义：**

返回当前在该纹理节点上设置的过滤。

### `bool QSGSimpleTextureNode::ownsTexture() const`

**作用与语义：**

如果节点接管纹理，则返回 `true`；否则返回 `false`。

### `QRectF QSGSimpleTextureNode::rect() const`

**作用与语义：**

返回该纹理节点的目标矩形块。

### `void QSGSimpleTextureNode::setFiltering(QSGTexture::Filtering filtering)`

**作用与语义：**

将该纹理节点的过滤设置为`filtering`。
平滑缩放时用`QSGTexture::Linear`;正常缩放时用`QSGTexture::Nearest`。

### `void QSGSimpleTextureNode::setOwnsTexture(bool owns)`

**作用与语义：**

设置节点是否拥有纹理的所有权`owns`。
默认情况下，节点不拥有纹理的所有权。

### `void QSGSimpleTextureNode::setRect(const QRectF &r)`

**作用与语义：**

将该纹理节点的目标rect设置为`r`。

### `void QSGSimpleTextureNode::setRect(qreal x, qreal y, qreal w, qreal h)`

**作用与语义：**

将该纹理节点的矩形设置为起始于（`x`， `y`），宽度为`w`，高度为`h`。

### `void QSGSimpleTextureNode::setSourceRect(const QRectF &r)`

**作用与语义：**

将该纹理节点的源rect设置为`r`。

### `void QSGSimpleTextureNode::setSourceRect(qreal x, qreal y, qreal w, qreal h)`

**作用与语义：**

设置该纹理节点的矩形，显示其纹理来自（`x`， `y`），宽度`w`高度相对于`QSGTexture::textureSize` `h`。

### `void QSGSimpleTextureNode::setTexture(QSGTexture *texture)`

**作用与语义：**

将该纹理节点的纹理设置为`texture`。
使用`setOwnsTexture()`来设置节点是否应该拥有纹理的所有权。默认情况下，节点不拥有所有权。
警告：纹理节点必须先有纹理，才能添加到进行渲染的场景图中。

### `void QSGSimpleTextureNode::setTextureCoordinatesTransform(QSGSimpleTextureNode::TextureCoordinatesTransformMode mode)`

**作用与语义：**

将生成纹理坐标的方法设置为`mode`。这可以用来获得纹理的正确方向。这在使用第三方 OpenGL 库渲染为纹理时很常见，因为 OpenGL 相对于 Qt Quick 的 y 轴是倒置的。

### `QRectF QSGSimpleTextureNode::sourceRect() const`

**作用与语义：**

返回该纹理节点的源矩形。

### `QSGTexture *QSGSimpleTextureNode::texture() const`

**作用与语义：**

返回该纹理节点的纹理。

### `QSGSimpleTextureNode::TextureCoordinatesTransformMode QSGSimpleTextureNode::textureCoordinatesTransform() const`

**作用与语义：**

返回生成该节点纹理坐标的模式。

### `enum TextureCoordinatesTransformFlag { NoTransform, MirrorHorizontally, MirrorVertically }`

**作用与语义：**

TextureCoordinatesTransformFlag枚举用于指定生成纹理四边形纹理坐标的模式。
- `QSGSimpleTextureNode::NoTransform`：`0x00`;纹理坐标以窗口坐标定向，即原点位于左上角。
- `QSGSimpleTextureNode::MirrorHorizontally`：`0x01`;纹理坐标相对于窗口坐标在水平轴上反转
- `QSGSimpleTextureNode::MirrorVertically`：`0x02`;纹理坐标在垂直轴上相对于窗口坐标反转
TextureCoordinatesTransformMode 类型是 QFlags 的 typedef<TextureCoordinatesTransformFlag>。它存储 TextureCoordinatesTransformFlag 值的 OR 组合。

### `flags TextureCoordinatesTransformMode`

**作用与语义：**

TextureCoordinatesTransformFlag枚举用于指定生成纹理四边形纹理坐标的模式。
- `QSGSimpleTextureNode::NoTransform`：`0x00`;纹理坐标以窗口坐标定向，即原点位于左上角。
- `QSGSimpleTextureNode::MirrorHorizontally`：`0x01`;纹理坐标相对于窗口坐标在水平轴上反转
- `QSGSimpleTextureNode::MirrorVertically`：`0x02`;纹理坐标在垂直轴上相对于窗口坐标反转
TextureCoordinatesTransformMode 类型是 QFlags 的 typedef<TextureCoordinatesTransformFlag>。它存储 TextureCoordinatesTransformFlag 值的 OR 组合。

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

`QSGSimpleTextureNode` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
