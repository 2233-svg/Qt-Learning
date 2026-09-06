# QSGTextNode

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QSGTextNode` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QSGTextNode` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSGTextNode>`
- 继承自：QSGTransformNode
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

- `enum RenderType { QtRendering, NativeRendering, CurveRendering }`
- `enum TextStyle { Normal, Outline, Raised, Sunken }`

### 公有函数

- `void addTextDocument(QPointF position, QTextDocument *document, int selectionStart = -1, int selectionCount = -1)`
- `void addTextLayout(QPointF position, QTextLayout *layout, int selectionStart = -1, int selectionCount = -1, int lineStart = 0, int lineCount = -1)`
- `virtual void clear() = 0`
- `virtual QColor color() const = 0`
- `virtual QSGTexture::Filtering filtering() const = 0`
- `virtual QColor linkColor() const = 0`
- `virtual QSGTextNode::RenderType renderType() const = 0`
- `virtual int renderTypeQuality() const = 0`
- `virtual QColor selectionColor() const = 0`
- `virtual QColor selectionTextColor() const = 0`
- `virtual void setColor(QColor color) = 0`
- `virtual void setFiltering(QSGTexture::Filtering filtering) = 0`
- `virtual void setLinkColor(QColor linkColor) = 0`
- `virtual void setRenderType(QSGTextNode::RenderType renderType) = 0`
- `virtual void setRenderTypeQuality(int renderTypeQuality) = 0`
- `virtual void setSelectionColor(QColor color) = 0`
- `virtual void setSelectionTextColor(QColor selectionTextColor) = 0`
- `virtual void setStyleColor(QColor styleColor) = 0`
- `virtual void setTextStyle(QSGTextNode::TextStyle textStyle) = 0`
- `virtual void setViewport(const QRectF &viewport) = 0`
- `virtual QColor styleColor() const = 0`
- `virtual QSGTextNode::TextStyle textStyle() = 0`
- `virtual QRectF viewport() const = 0`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSGTextNode::RenderType`

**作用与语义：**

该枚举类型描述用于渲染文本的字形节点类型。
- `QSGTextNode::QtRendering`：`0`;文本通过每个字形的可缩放距离场来渲染。
- `QSGTextNode::NativeRendering`：`1`;文本采用平台特定技术进行渲染。
- `QSGTextNode::CurveRendering`：`2`;文本通过直接运行在图形硬件上的曲线光栅器渲染。
如果你喜欢文本在目标平台上看起来原生且不需要高级功能如文本转换，选择`NativeRendering`。将这些功能与 NativeRendering 渲染类型结合使用，会导致效果较差，有时甚至出现像素化。
`Text.QtRendering`和`Text.CurveRendering`都是硬件加速技术。`QtRendering`速度更快，但占用更多内存，且在大尺寸时会出现渲染伪影。`CurveRendering`应作为替代方案，适用于`QtRendering`效果不佳或优先减少图形内存消耗的情况。

### `enum QSGTextNode::TextStyle`

**作用与语义：**

该枚举类型描述了可用于文本渲染的样式。
- `QSGTextNode::Normal`：`0`;文字绘制时不使用任何风格。
- `QSGTextNode::Outline`：`1`;文本带有轮廓绘制。
- `QSGTextNode::Raised`：`2`;文本被抬起绘制。
- `QSGTextNode::Sunken`：`3`;文字呈凹槽绘制。

### `void QSGTextNode::addTextDocument(QPointF position, QTextDocument *document, int selectionStart = -1, int selectionCount = -1)`

**作用与语义：**

将`document`的内容添加到`position`的文本节点。如果`selectionStart` >= 0，则标记为`selectionCount`字符数选定区域中的第一个字符。选区以背景填充表示，`selectionColor()`中选中的文本在`selectionTextColor()`中渲染。
该函数将其参数转发给虚拟函数`doAddTextDocument()`。

### `void QSGTextNode::addTextLayout(QPointF position, QTextLayout *layout, int selectionStart = -1, int selectionCount = -1, int lineStart = 0, int lineCount = -1)`

**作用与语义：**

将`layout`的内容添加到`position`的文本节点。如果`selectionStart`为>= 0，则标记为`selectionCount`字符数选中的第一个字符。选区以背景填充表示，`selectionColor()`中选中的文本在`selectionTextColor()`中渲染。
为了方便起见，可以使用`lineStart`和 `lineCount` 来选择从布局中包含的 `QTextLine` 对象范围。这在创建省略布局时非常有用。如果 `lineCount` <为 0，那么节点将包含从`lineStart`到布局末尾的线条。
该函数将其参数转发到虚拟函数 `doAddTextLayout()`。

### `[pure virtual] void QSGTextNode::clear()`

**作用与语义：**

清除节点的内容，删除节点及表示已添加的布局和文档的其他数据。

### `[pure virtual] QColor QSGTextNode::color() const`

**作用与语义：**

返回渲染文本时的主要颜色。

### `[pure virtual private] void QSGTextNode::doAddTextDocument(QPointF position, QTextDocument *document, int selectionStart, int selectionCount)`

**作用与语义：**

`addTextDocument()`调用的虚拟函数，将`document`的内容转换为场景图节点，并将其添加到当前节点`position`。
如果`selectionStart` >= 0，则标记为选定区域中`selectionCount`字符数的第一个字符。选区以背景填充表示，`selectionColor()`中选中的文本在`selectionTextColor()`中渲染。

### `[pure virtual private] void QSGTextNode::doAddTextLayout(QPointF position, QTextLayout *layout, int selectionStart, int selectionCount, int lineStart, int lineCount)`

**作用与语义：**

`addTextLayout()`调用虚拟函数，将`layout`的内容转换为场景图节点，并将其添加到当前节点`position`。
如果`selectionStart` >= 0，则标记`selectionCount`字符数选中的第一个字符。选区以背景填充表示，并以`selectionColor()`填充，选中的文本在`selectionTextColor()`中渲染。
为了方便，可以使用`lineStart`和`lineCount`选择从布局中包含的`QTextLine`对象范围。这在创建省略布局时非常有用。如果`lineCount` < 0，则该节点将包含从`lineStart`到布局末尾的行。

### `[pure virtual] QSGTexture::Filtering QSGTextNode::filtering() const`

**作用与语义：**

返回用于缩放显示文本图像时使用的采样模式。

### `[pure virtual] QColor QSGTextNode::linkColor() const`

**作用与语义：**

返回文本中超链接的颜色。

### `[pure virtual] QSGTextNode::RenderType QSGTextNode::renderType() const`

**作用与语义：**

返回用于渲染文本的字形节点类型。

### `[pure virtual] int QSGTextNode::renderTypeQuality() const`

**作用与语义：**

返回节点的渲染类型质量。详情请参见 `setRenderTypeQuality()`。

### `[pure virtual] QColor QSGTextNode::selectionColor() const`

**作用与语义：**

当文本任一部分被标记为已选时，返回选区背景的颜色。

### `[pure virtual] QColor QSGTextNode::selectionTextColor() const`

**作用与语义：**

当文本任一部分被标记为被选中时，返回所选文本的颜色。

### `[pure virtual] void QSGTextNode::setColor(QColor color)`

**作用与语义：**

将主色设置为渲染文本时的`color`。
默认是黑色：`QColor(0, 0, 0)`。

### `[pure virtual] void QSGTextNode::setFiltering(QSGTexture::Filtering filtering)`

**作用与语义：**

设置用于对显示文本中图像缩放时使用的采样模式`filtering`。对于平滑缩放的图像，请使用这里`QSGTexture::Linear`。
默认是`QSGTexture::Nearest`。

### `[pure virtual] void QSGTextNode::setLinkColor(QColor linkColor)`

**作用与语义：**

将文本中的超链接颜色或超链接设置为`linkColor`。
默认是蓝色：`QColor(0, 0, 255)`。

### `[pure virtual] void QSGTextNode::setRenderType(QSGTextNode::RenderType renderType)`

**作用与语义：**

将所用字形节点类型设置为`renderType`。
默认是`QtRendering`。

### `[pure virtual] void QSGTextNode::setRenderTypeQuality(int renderTypeQuality)`

**作用与语义：**

如果使用的`renderType()`支持，则设置该质量以在渲染文本时使用。支持时，可以用来用视觉细节换取执行速度或内存。
当`renderTypeQuality`为<0时，使用默认质量。
`renderTypeQuality`可以是任意整数，尽管如果设置极端值，可能会遇到底层图形硬件的限制。Qt 快速文本元素的预定义值如下：
- `DefaultRenderTypeQuality`：-1（默认）
- `LowRenderTypeQuality`：26
- `NormalRenderTypeQuality`：52
- `HighRenderTypeQuality`：104
- `VeryHighRenderTypeQuality`：208
目前该值仅由`QtRendering`渲染类型尊重。设置它会改变用于表示字形的距离场分辨率。将其设为高于正常值会增加内存消耗，但减少了非常大文本中的过滤伪影。
默认值是-1。

### `[pure virtual] void QSGTextNode::setSelectionColor(QColor color)`

**作用与语义：**

当文本任一部分被标记为选中时，将选区背景颜色设置为`color`。
默认是深蓝色：`QColor(0, 0, 128)`。

### `[pure virtual] void QSGTextNode::setSelectionTextColor(QColor selectionTextColor)`

**作用与语义：**

当文本任一部分被标记为已选中时，将选区文本的颜色设置为`selectionTextColor`。
默认是白色：`QColor(255, 255, 255)`。

### `[pure virtual] void QSGTextNode::setStyleColor(QColor styleColor)`

**作用与语义：**

设置样式颜色，用于渲染文本时使用，转为`styleColor`。
默认是黑色：`QColor(0, 0, 0)`。

### `[pure virtual] void QSGTextNode::setTextStyle(QSGTextNode::TextStyle textStyle)`

**作用与语义：**

将渲染文本的样式设置为`textStyle`。默认是`Normal`。

### `[pure virtual] void QSGTextNode::setViewport(const QRectF &viewport)`

**作用与语义：**

将视口的边界矩阵（rect）设置为`viewport`。提供这些信息使 `QSGTextNode` 能够优化文本布局或文档中哪些部分包含在场景图中。
默认为默认构造的`QRectF`。对于该视口，所有内容都包含在图中。

### `[pure virtual] QColor QSGTextNode::styleColor() const`

**作用与语义：**

返回渲染文本时使用的样式颜色。

### `[pure virtual] QSGTextNode::TextStyle QSGTextNode::textStyle()`

**作用与语义：**

返回渲染后的文本样式。

### `[pure virtual] QRectF QSGTextNode::viewport() const`

**作用与语义：**

返回该`QSGTextNode`当前的视口设置。

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

`QSGTextNode` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
