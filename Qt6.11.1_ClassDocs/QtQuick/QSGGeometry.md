# QSGGeometry

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QSGGeometry` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QSGGeometry` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSGGeometry>`
- 继承自：未在类页中列出
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

- `struct Attribute`
- `struct AttributeSet`
- `struct ColoredPoint2D`
- `struct Point2D`
- `struct TexturedPoint2D`
- `enum AttributeType { UnknownAttribute, PositionAttribute, ColorAttribute, TexCoordAttribute, TexCoord1Attribute, TexCoord2Attribute }`
- `enum DataPattern { AlwaysUploadPattern, DynamicPattern, StaticPattern, StreamPattern }`
- `enum DrawingMode { DrawPoints, DrawLines, DrawLineStrip, DrawTriangles, DrawTriangleStrip }`
- `enum Type { ByteType, UnsignedByteType, ShortType, UnsignedShortType, IntType, …, DoubleType }`

### 公有函数

- `QSGGeometry(const QSGGeometry::AttributeSet &attributes, int vertexCount, int indexCount = 0, int indexType = UnsignedShortType)`
- `virtual ~QSGGeometry()`
- `void allocate(int vertexCount, int indexCount = 0)`
- `int attributeCount() const`
- `const QSGGeometry::Attribute * attributes() const`
- `unsigned int drawingMode() const`
- `int indexCount() const`
- `void * indexData()`
- `const void * indexData() const`
- `uint * indexDataAsUInt()`
- `const uint * indexDataAsUInt() const`
- `quint16 * indexDataAsUShort()`
- `const quint16 * indexDataAsUShort() const`
- `QSGGeometry::DataPattern indexDataPattern() const`
- `int indexType() const`
- `float lineWidth() const`
- `void markIndexDataDirty()`
- `void markVertexDataDirty()`
- `void setDrawingMode(unsigned int mode)`
- `(since 6.10) void setIndexCount(int count)`
- `void setIndexDataPattern(QSGGeometry::DataPattern p)`
- `void setLineWidth(float width)`
- `(since 6.10) void setVertexCount(int count)`
- `void setVertexDataPattern(QSGGeometry::DataPattern p)`
- `int sizeOfIndex() const`
- `int sizeOfVertex() const`
- `int vertexCount() const`
- `void * vertexData()`
- `const void * vertexData() const`
- `QSGGeometry::ColoredPoint2D * vertexDataAsColoredPoint2D()`
- `const QSGGeometry::ColoredPoint2D * vertexDataAsColoredPoint2D() const`
- `QSGGeometry::Point2D * vertexDataAsPoint2D()`
- `const QSGGeometry::Point2D * vertexDataAsPoint2D() const`
- `QSGGeometry::TexturedPoint2D * vertexDataAsTexturedPoint2D()`
- `const QSGGeometry::TexturedPoint2D * vertexDataAsTexturedPoint2D() const`
- `QSGGeometry::DataPattern vertexDataPattern() const`

### 静态公有成员

- `const QSGGeometry::AttributeSet & defaultAttributes_ColoredPoint2D()`
- `const QSGGeometry::AttributeSet & defaultAttributes_Point2D()`
- `const QSGGeometry::AttributeSet & defaultAttributes_TexturedPoint2D()`
- `void updateColoredRectGeometry(QSGGeometry *g, const QRectF &rect)`
- `void updateRectGeometry(QSGGeometry *g, const QRectF &rect)`
- `void updateTexturedRectGeometry(QSGGeometry *g, const QRectF &rect, const QRectF &textureRect)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSGGeometry::AttributeType`

**作用与语义：**

该枚举识别了几种属性类型。
- `QSGGeometry::UnknownAttribute`：`0`;不在乎
- `QSGGeometry::PositionAttribute`：`1`;位置
- `QSGGeometry::ColorAttribute`：`2`;颜色
- `QSGGeometry::TexCoordAttribute`：`3`;纹理坐标
- `QSGGeometry::TexCoord1Attribute`：`4`;纹理坐标1
- `QSGGeometry::TexCoord2Attribute`：`5`;纹理坐标2

### `enum QSGGeometry::DataPattern`

**作用与语义：**

DataPattern 枚举用于指定几何对象中顶点和索引数据的使用模式。
- `QSGGeometry::AlwaysUploadPattern`: `0`；数据总是上传。这意味着用户在修改后无需显式标记索引和顶点数据为脏。此为默认值。
- `QSGGeometry::DynamicPattern`: `2`；数据被重复修改并绘制多次。这是一个可能提供更好性能的提示。设置此选项时，用户必须确保在修改后标记数据为脏。
- `QSGGeometry::StaticPattern`: `3`；数据被修改一次并绘制多次。这是一个可能提供更好性能的提示。设置此选项时，用户必须确保在修改后标记数据为脏。
- `QSGGeometry::StreamPattern`: `1`；数据几乎每次绘制前都会被修改。这是一个可能提供更好性能的提示。设置此选项时，用户必须确保在修改后标记数据为脏。

### `enum QSGGeometry::DrawingMode`

**作用与语义：**

指定绘图模式，也称为原始拓扑。
注意：从Qt 6开始，场景图只暴露了所有支持的3D图形API都支持的拓扑。因此，`DrawLineLoop`和`DrawTriangleFan`这两个值在Qt 6的运行时不再支持，尽管枚举值本身仍然存在。
- `QSGGeometry::DrawPoints`：`0x0000`
- `QSGGeometry::DrawLines`：`0x0001`
- `QSGGeometry::DrawLineStrip`：`0x0003`
- `QSGGeometry::DrawTriangles`：`0x0004`
- `QSGGeometry::DrawTriangleStrip`：`0x0005`

### `enum QSGGeometry::Type`

**作用与语义：**

指定顶点数据中的组件类型。
- `QSGGeometry::ByteType`：`0x1400`
- `QSGGeometry::UnsignedByteType`：`0x1401`
- `QSGGeometry::ShortType`：`0x1402`
- `QSGGeometry::UnsignedShortType`：`0x1403`
- `QSGGeometry::IntType`：`0x1404`
- `QSGGeometry::UnsignedIntType`：`0x1405`
- `QSGGeometry::FloatType`：`0x1406`
- `QSGGeometry::Bytes2Type`：`0x1407`;于第5.14节新增。
- `QSGGeometry::Bytes3Type`：`0x1408`;新增于第5.14节。
- `QSGGeometry::Bytes4Type`：`0x1409`;第5.14季度新增。
- `QSGGeometry::DoubleType`：`0x140A`;于第5.14季度新增。

### `QSGGeometry::QSGGeometry(const QSGGeometry::AttributeSet &attributes, int vertexCount, int indexCount = 0, int indexType = UnsignedShortType)`

**作用与语义：**

基于`attributes`构造几何对象。
对象根据累计大小（`attributes`）和`indexCount`的体积为`vertexCount`顶点分配空间。
`indexType`可以是`UnsignedShortType`或`UnsignedIntType`。后者的支持取决于运行时使用的图形API实现，且可能并不总是可用。
几何对象默认以`DrawTriangleStrip`为绘制模式构建。
注意：`attributes`及其引用的`Attribute`对象必须在整个QSGGeometry生命周期内保持有效。QSGGeometry存储`attributes`的引用，不删除`Attribute`对象。

### `[virtual noexcept] QSGGeometry::~QSGGeometry()`

**作用与语义：**

销毁几何对象及其分配的顶点和索引数据。

### `void QSGGeometry::allocate(int vertexCount, int indexCount = 0)`

**作用与语义：**

调整该几何对象的顶点和索引数据大小，使其适合`vertexCount`顶点和`indexCount`指标，并相应设置顶点和指标的数量。
使用`setVertexCount()`或`setIndexCount()`来更改顶点或索引的数量，而无需再次调用 allocate()。
调用后顶点和索引数据将失效，调用者必须通过调用`node->markDirty(QSGNode::DirtyGeometry)`标记关联几何节点为脏节点，以确保渲染器有机会更新内部缓冲区。

### `int QSGGeometry::attributeCount() const`

**作用与语义：**

返回该几何所用的attrbute集合中的属性数量。

### `const QSGGeometry::Attribute *QSGGeometry::attributes() const`

**作用与语义：**

返回一个带有该几何属性的数组。数组大小以 `attributeCount()` 表示。

### `[static] const QSGGeometry::AttributeSet &QSGGeometry::defaultAttributes_ColoredPoint2D()`

**作用与语义：**

便利函数，返回用于每顶点着色的二维绘图属性。

### `[static] const QSGGeometry::AttributeSet &QSGGeometry::defaultAttributes_Point2D()`

**作用与语义：**

方便功能，返回用于二维纯色绘图的属性。

### `[static] const QSGGeometry::AttributeSet &QSGGeometry::defaultAttributes_TexturedPoint2D()`

**作用与语义：**

便利函数，返回用于纹理二维绘图的属性。

### `unsigned int QSGGeometry::drawingMode() const`

**作用与语义：**

返回该几何形状的绘图模式。
默认值是`DrawTriangleStrip`。

### `int QSGGeometry::indexCount() const`

**作用与语义：**

返回渲染几何对象时处理的索引数量。

### `void *QSGGeometry::indexData()`

**作用与语义：**

返回指向该几何对象原始索引数据的指针。

### `const void *QSGGeometry::indexData() const`

**作用与语义：**

返回指向该几何对象原始索引数据的指针。

### `uint *QSGGeometry::indexDataAsUInt()`

**作用与语义：**

方便函数，将索引数据作为一个可变的32位无符号整数数组访问。

### `const uint *QSGGeometry::indexDataAsUInt() const`

**作用与语义：**

方便函数，将索引数据作为一个不可变的32位无符号整数数组访问。

### `quint16 *QSGGeometry::indexDataAsUShort()`

**作用与语义：**

方便函数，将索引数据作为可变的16位无符号整数数组访问。

### `const quint16 *QSGGeometry::indexDataAsUShort() const`

**作用与语义：**

方便函数可访问索引数据，作为16位无符号整数的不可变数组。

### `QSGGeometry::DataPattern QSGGeometry::indexDataPattern() const`

**作用与语义：**

返回该几何中索引的使用模式。默认模式为`AlwaysUploadPattern`。

### `int QSGGeometry::indexType() const`

**作用与语义：**

返回该几何对象中用于索引的原始类型。

### `float QSGGeometry::lineWidth() const`

**作用与语义：**

获取当前的线或点宽度，或用于该几何形状。该属性仅适用于`drawingMode`为`DrawLines`或`DrawLineStrip`时的线宽。在支持时，当`drawingMode`为`DrawPoints`时，也适用于点的大小。
默认值为`1.0`。
注意：根据平台和图形API，对点和线条绘制的支持在运行时可能有限。例如，有些API不支持点精灵，因此无法设置非1的大小。
注意：`1.0`宽度始终受支持。

### `void QSGGeometry::markIndexDataDirty()`

**作用与语义：**

标记该几何体中的顶点发生变化，必须重新上传。
该函数仅在顶点使用模式为 StaticData 且渲染该几何体的渲染器将几何体上传到顶点缓冲对象（VBO）时才有效。

### `void QSGGeometry::markVertexDataDirty()`

**作用与语义：**

标记该几何体中的顶点发生变化，必须重新上传。
该函数仅在顶点使用模式为 StaticData 且渲染该几何体的渲染器将几何体上传到顶点缓冲对象（VBO）时才有效。

### `void QSGGeometry::setDrawingMode(unsigned int mode)`

**作用与语义：**

设置用于绘制该几何形状的 `mode`。
默认值是`QSGGeometry::DrawTriangleStrip`。

### `[since 6.10] void QSGGeometry::setIndexCount(int count)`

**作用与语义：**

设置每次渲染几何对象时要处理的索引数量。
`count`未经过验证，用户有责任确保仅指定介于零和分配索引数量之间的值。
此调用后顶点和索引数据不会失效，但调用者必须通过调用`node->markDirty(QSGNode::DirtyGeometry)`标记几何节点为脏节点，以确保渲染器有机会更新内部缓冲区。

### `void QSGGeometry::setIndexDataPattern(QSGGeometry::DataPattern p)`

**作用与语义：**

将索引的使用模式设置为`p`。
默认是`AlwaysUploadPattern`。当设置为非默认值时，用户必须在更改索引数据后调用`markIndexDataDirty()`，同时还要用`QSGNode::DirtyGeometry`调用`QSGNode::markDirty()`。

### `void QSGGeometry::setLineWidth(float width)`

**作用与语义：**

设置该几何体所用的线或点宽度为`width`。该属性仅适用于`drawingMode`为`DrawLines`或`DrawLineStrip`时的线宽。支持时，也适用于`drawingMode` `DrawPoints`时点的大小。
注意：根据平台和图形API，对点和线条绘制的支持在运行时可能有限。例如，有些API不支持点精灵，因此无法设置非1的大小。
注意：`1.0`宽度始终受支持。

### `[since 6.10] void QSGGeometry::setVertexCount(int count)`

**作用与语义：**

设置要渲染的顶点数。
`count`不会被验证，用户有责任确保只指定介于零和分配顶点数之间的值。
调用后顶点数据不会失效，但调用者必须通过调用`node->markDirty(QSGNode::DirtyGeometry)`将几何节点标记为脏节点，以确保渲染器有机会更新内部缓冲区。

### `void QSGGeometry::setVertexDataPattern(QSGGeometry::DataPattern p)`

**作用与语义：**

将顶点的使用模式设置为`p`。
默认是`AlwaysUploadPattern`。当设置为非默认值时，用户必须在更改顶点数据后调用`markVertexDataDirty()`，同时还要用`QSGNode::DirtyGeometry`调用`QSGNode::markDirty()`。

### `int QSGGeometry::sizeOfIndex() const`

**作用与语义：**

返回索引类型的字节大小。
当索引类型为`UnsignedShortType`时，该值为`2`;当索引类型为`UnsignedIntType`时为`4`。

### `int QSGGeometry::sizeOfVertex() const`

**作用与语义：**

返回一个顶点的字节大小。
这个数值来自属性。

### `[static] void QSGGeometry::updateColoredRectGeometry(QSGGeometry *g, const QRectF &rect)`

**作用与语义：**

`rect`中更新几何体`g`坐标。
该函数假设几何对象包含一条由`QSGGeometry::ColoredPoint2D`顶点组成的三角形带。

### `[static] void QSGGeometry::updateRectGeometry(QSGGeometry *g, const QRectF &rect)`

**作用与语义：**

`rect`中用坐标更新几何`g`。
该函数假设几何对象包含一条由`QSGGeometry::Point2D`顶点组成的三角形带。

### `[static] void QSGGeometry::updateTexturedRectGeometry(QSGGeometry *g, const QRectF &rect, const QRectF &textureRect)`

**作用与语义：**

更新几何体`g`，包含`rect`坐标和`textureRect`的纹理坐标。
`textureRect`应该在归一化坐标内。
`g`假设为一个由四个顶点组成的`QSGGeometry::TexturedPoint2D`型三角形带。

### `int QSGGeometry::vertexCount() const`

**作用与语义：**

返回可渲染的顶点数，或者如果使用索引，则返回通过索引可访问的顶点数。

### `void *QSGGeometry::vertexData()`

**作用与语义：**

返回指向该几何对象原始顶点数据的指针。

### `const void *QSGGeometry::vertexData() const`

**作用与语义：**

返回指向该几何对象原始顶点数据的指针。

### `QSGGeometry::ColoredPoint2D *QSGGeometry::vertexDataAsColoredPoint2D()`

**作用与语义：**

方便函数以可变数组`QSGGeometry::ColoredPoint2D`访问顶点数据。

### `const QSGGeometry::ColoredPoint2D *QSGGeometry::vertexDataAsColoredPoint2D() const`

**作用与语义：**

方便函数将顶点数据作为不可变的`QSGGeometry::ColoredPoint2D`数组访问。

### `QSGGeometry::Point2D *QSGGeometry::vertexDataAsPoint2D()`

**作用与语义：**

方便函数以可变数组`QSGGeometry::Point2D`访问顶点数据。

### `const QSGGeometry::Point2D *QSGGeometry::vertexDataAsPoint2D() const`

**作用与语义：**

方便函数以不可变数组`QSGGeometry::Point2D`访问顶点数据。

### `QSGGeometry::TexturedPoint2D *QSGGeometry::vertexDataAsTexturedPoint2D()`

**作用与语义：**

方便函数以可变数组`QSGGeometry::TexturedPoint2D`访问顶点数据。

### `const QSGGeometry::TexturedPoint2D *QSGGeometry::vertexDataAsTexturedPoint2D() const`

**作用与语义：**

方便函数将顶点数据作为不可变的数组访问`QSGGeometry::TexturedPoint2D`。

### `QSGGeometry::DataPattern QSGGeometry::vertexDataPattern() const`

**作用与语义：**

返回该几何体中顶点的使用模式。默认模式为`AlwaysUploadPattern`。

### `struct Attribute`

**作用与语义：**

QSGGeometry：：Attribute 描述了 QSGGeometry 中的单个顶点属性。
`QSGGeometry::Attribute`结构体描述了属性寄存器的位置、属性元组的大小和属性类型。
如果该属性是描述位置的属性，它还会向渲染器提供提示。场景图渲染器可能会利用这些信息进行优化。
它包含若干位，保留以供未来使用。

### `struct AttributeSet`

**作用与语义：**

QSGGeometry：：AttributeSet 描述了 QSGGeometry 中顶点的构建方式。

### `struct ColoredPoint2D`

**作用与语义：**

QSGGeometry：：ColoredPoint2D 结构体是一个方便访问带有颜色的二维点的结构体。

### `struct Point2D`

**作用与语义：**

QSGGeometry：:P oint2D struct 是一个方便访问 2D 点的结构体。

### `struct TexturedPoint2D`

**作用与语义：**

QSGGeometry：：TexturedPoint2D 结构体是一个方便的结构体，用于访问带有纹理坐标的二维点。

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

`QSGGeometry` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
