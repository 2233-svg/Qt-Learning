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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSGImageNode::TextureCoordinatesTransformFlagflags QSGImageNode::TextureCoordinatesTransformMode`

**作用与语义：**

TextureCoordinatesTransformFlag枚举用于指定生成纹理四边形纹理坐标的模式。
- `QSGImageNode::NoTransform`：`0x00`;纹理坐标以窗口坐标定向，即原点位于左上角。
- `QSGImageNode::MirrorHorizontally`：`0x01`;纹理坐标相对于窗口坐标在水平轴上反转
- `QSGImageNode::MirrorVertically`：`0x02`;纹理坐标在垂直轴上相对于窗口坐标进行倒置
TextureCoordinatesTransformMode 类型是 QFlags 的 typedef<TextureCoordinatesTransformFlag>。它存储 TextureCoordinatesTransformFlag 值的 OR 组合。

### `[pure virtual] QSGTexture::AnisotropyLevel QSGImageNode::anisotropyLevel() const`

**作用与语义：**

返回该图像节点的斜纹层。

### `[pure virtual] QSGTexture::Filtering QSGImageNode::filtering() const`

**作用与语义：**

返回该图像节点的过滤结果。

### `[pure virtual] QSGTexture::Filtering QSGImageNode::mipmapFiltering() const`

**作用与语义：**

返回该图像节点的 mipmap 过滤结果。

### `[pure virtual] bool QSGImageNode::ownsTexture() const`

**作用与语义：**

如果节点接管了纹理，则返回 `true`；否则返回 `false`。

### `[static] void QSGImageNode::rebuildGeometry(QSGGeometry *g, QSGTexture *texture, const QRectF &rect, QRectF sourceRect, QSGImageNode::TextureCoordinatesTransformMode texCoordMode)`

**作用与语义：**

更新几何体`g`，包含`texture`、`rect`坐标和`sourceRect`的纹理坐标。
`g`假设为一个由四个顶点组成的三角形条带，类型为`QSGGeometry::TexturedPoint2D`。
`texCoordMode`用于规范`sourceRect`。

### `[pure virtual] QRectF QSGImageNode::rect() const`

**作用与语义：**

返回该图像节点的目标矩形。

### `[pure virtual] void QSGImageNode::setAnisotropyLevel(QSGTexture::AnisotropyLevel level)`

**作用与语义：**

将该图像节点的暗角层设置为`level`。

### `[pure virtual] void QSGImageNode::setFiltering(QSGTexture::Filtering filtering)`

**作用与语义：**

将该图像节点的过滤设置为`filtering`。
想要平滑缩放，可以用`QSGTexture::Linear`。正常缩放时用`QSGTexture::Nearest`。

### `[pure virtual] void QSGImageNode::setMipmapFiltering(QSGTexture::Filtering filtering)`

**作用与语义：**

将该图像节点用于的mipmap滤波设置为`filtering`。
为了实现MIP映射之间的平滑缩放，使用`QSGTexture::Linear`。对于正常缩放，使用`QSGTexture::Nearest`。

### `[pure virtual] void QSGImageNode::setOwnsTexture(bool owns)`

**作用与语义：**

设置节点是否拥有纹理的所有权`owns`。
默认情况下，节点不拥有纹理的所有权。

### `[pure virtual] void QSGImageNode::setRect(const QRectF &rect)`

**作用与语义：**

将该图像节点的目标rect设置为`rect`。

### `void QSGImageNode::setRect(qreal x, qreal y, qreal w, qreal h)`

**作用与语义：**

将该图像节点的矩形设置为从（`x`， `y`）开始，宽度为`w`，高度为`h`。

### `[pure virtual] void QSGImageNode::setSourceRect(const QRectF &rect)`

**作用与语义：**

将该图像节点的源rect设置为`rect`。

### `void QSGImageNode::setSourceRect(qreal x, qreal y, qreal w, qreal h)`

**作用与语义：**

设置该图像节点的矩形以显示其纹理，从（`x`， `y`）中获得，宽度`w`高度相对于`QSGTexture::textureSize` `h`。

### `[pure virtual] void QSGImageNode::setTexture(QSGTexture *texture)`

**作用与语义：**

将该图像节点的纹理设置为`texture`。
用`setOwnsTexture()`来设置节点是否应该拥有纹理的所有权。默认情况下，节点不会拥有所有权。
警告：图像节点必须先有纹理，才能添加到进行渲染的场景图中。

### `[pure virtual] void QSGImageNode::setTextureCoordinatesTransform(QSGImageNode::TextureCoordinatesTransformMode mode)`

**作用与语义：**

将生成纹理坐标的方法设置为`mode`。这可以用来获得纹理的正确方向。当使用第三方 OpenGL 库渲染为纹理时，这很常见，因为 OpenGL 的 y 轴相对于 Qt Quick 是倒置的。

### `[pure virtual] QRectF QSGImageNode::sourceRect() const`

**作用与语义：**

返回该图像节点的源rect。

### `[pure virtual] QSGTexture *QSGImageNode::texture() const`

**作用与语义：**

返回该图像节点的纹理。

### `[pure virtual] QSGImageNode::TextureCoordinatesTransformMode QSGImageNode::textureCoordinatesTransform() const`

**作用与语义：**

返回生成该节点纹理坐标的模式。

### `enum TextureCoordinatesTransformFlag { NoTransform, MirrorHorizontally, MirrorVertically }`

**作用与语义：**

TextureCoordinatesTransformFlag枚举用于指定生成纹理四边形纹理坐标的模式。
- `QSGImageNode::NoTransform`：`0x00`;纹理坐标以窗口坐标定向，即原点位于左上角。
- `QSGImageNode::MirrorHorizontally`：`0x01`;纹理坐标相对于窗口坐标在水平轴上反转
- `QSGImageNode::MirrorVertically`：`0x02`;纹理坐标在垂直轴上相对于窗口坐标进行倒置
TextureCoordinatesTransformMode 类型是 QFlags 的 typedef<TextureCoordinatesTransformFlag>。它存储 TextureCoordinatesTransformFlag 值的 OR 组合。

### `flags TextureCoordinatesTransformMode`

**作用与语义：**

TextureCoordinatesTransformFlag枚举用于指定生成纹理四边形纹理坐标的模式。
- `QSGImageNode::NoTransform`：`0x00`;纹理坐标以窗口坐标定向，即原点位于左上角。
- `QSGImageNode::MirrorHorizontally`：`0x01`;纹理坐标相对于窗口坐标在水平轴上反转
- `QSGImageNode::MirrorVertically`：`0x02`;纹理坐标在垂直轴上相对于窗口坐标进行倒置
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

`QSGImageNode` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
