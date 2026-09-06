# QQuickPaintedItem

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickPaintedItem` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickPaintedItem` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickPaintedItem>`
- 继承自：QQuickItem
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
target_link_libraries(mytarget PRIVATE Qt6::Quick)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

### 状态、生命周期和线程

**生命周期：** QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

**状态与结果：** 属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

**线程与事件循环：** 大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

## 3. 直接使用

需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。 使用时通常按这个过程组织：注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

```cpp
// C++ 侧暴露属性/信号后，在 QML 中建立绑定。
// 变化时发出 notify signal，避免在绑定表达式中直接修改状态。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum PerformanceHint { FastFBOResizing }`
- `flags PerformanceHints`
- `enum RenderTarget { Image, FramebufferObject, InvertedYFramebufferObject }`

### 属性

- `fillColor : QColor`
- `renderTarget : RenderTarget`
- `textureSize : QSize`

### 公有函数

- `QQuickPaintedItem(QQuickItem *parent = nullptr)`
- `virtual ~QQuickPaintedItem() override`
- `bool antialiasing() const`
- `QColor fillColor() const`
- `bool mipmap() const`
- `bool opaquePainting() const`
- `virtual void paint(QPainter *painter) = 0`
- `QQuickPaintedItem::PerformanceHints performanceHints() const`
- `QQuickPaintedItem::RenderTarget renderTarget() const`
- `void setAntialiasing(bool enable)`
- `void setFillColor(const QColor &)`
- `void setMipmap(bool enable)`
- `void setOpaquePainting(bool opaque)`
- `void setPerformanceHint(QQuickPaintedItem::PerformanceHint hint, bool enabled = true)`
- `void setPerformanceHints(QQuickPaintedItem::PerformanceHints hints)`
- `void setRenderTarget(QQuickPaintedItem::RenderTarget target)`
- `void setTextureSize(const QSize &size)`
- `QSize textureSize() const`
- `void update(const QRect &rect = QRect())`

### 重实现的公有函数

- `virtual bool isTextureProvider() const override`
- `virtual QSGTextureProvider * textureProvider() const override`

### 信号

- `void fillColorChanged()`
- `void renderTargetChanged()`
- `void textureSizeChanged()`

### 重实现的保护函数

- `virtual void itemChange(QQuickItem::ItemChange change, const QQuickItem::ItemChangeData &value) override`
- `virtual void releaseResources() override`
- `virtual QSGNode * updatePaintNode(QSGNode *oldNode, QQuickItem::UpdatePaintNodeData *data) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QQuickPaintedItem::PerformanceHintflags QQuickPaintedItem::PerformanceHints`

**作用与语义：**

这个枚举描述了你可以启用以提升渲染性能的标志`QQuickPaintedItem`。默认情况下，这些标志都没有被设置。
- `QQuickPaintedItem::FastFBOResizing`：`0x1`;从Qt 6.0开始，该值被忽略。
PerformanceHints 类型是 QFlags 的 typedef<PerformanceHint>。它存储 PerformanceHint 值的 OR 组合。

### `enum QQuickPaintedItem::RenderTarget`

**作用与语义：**

这个枚举描述了`QQuickPaintedItem`的渲染目标。渲染目标是`QPainter`在物体被渲染到屏幕上之前绘制的表面。
- `QQuickPaintedItem::Image`：`0`;默认操作;`QPainter` 使用光栅绘图引擎绘制到一个`QImage`。图像内容需要在之后上传到图形内存，如果物品较大，操作可能会较慢。该渲染目标支持高质量抗锯齿和快速的物品大小调整。
- `QQuickPaintedItem::FramebufferObject`：`1`;从Qt 6.9开始，只要渲染API是OpenGL，该值将支持硬件加速绘画，否则将被忽略。对于Qt 6.0至Qt 6.8版本，所有渲染API都会忽略该值。这通常能带来更好的渲染性能，但代价是抗锯齿质量。
- `QQuickPaintedItem::InvertedYFramebufferObject`：`2`;与FramebufferObject相同，但渲染方向绕X轴反转。

### `fillColor : QColor`

**作用与语义：**

该属性保留物品的背景填充颜色。
默认情况下，填充颜色设置为`Qt::transparent`。
将填充颜色设置为无效颜色（例如 QColor()），以禁用背景填充。这可能会提升性能，如果 `paint()` 函数绘制到每帧的所有像素，这样做是安全的。

**如何使用：** 调用 `fillColor()` 读取当前值；它不会修改应用状态。

### `renderTarget : RenderTarget`

**作用与语义：**

该属性包含了该物品的渲染目标。
该属性定义了`QPainter`渲染的目标，可以是`QQuickPaintedItem::Image`、`QQuickPaintedItem::FramebufferObject`或`QQuickPaintedItem::InvertedYFramebufferObject`。
每种对象都有其优势，通常是性能与质量的区别。使用帧缓冲对象避免了将图像内容上传到图形内存纹理的高成本，同时使用图像实现高质量抗锯齿。
警告：调整帧缓冲区对象大小是一项昂贵操作，如果物品经常被调整大小，请避免使用`QQuickPaintedItem::FramebufferObject`渲染目标。
默认情况下，渲染目标是`QQuickPaintedItem::Image`。

**如何使用：** 调用 `renderTarget()` 读取当前值；它不会修改应用状态。

### `textureSize : QSize`

**作用与语义：**

定义了纹理的大小。
改变贴图大小不会影响`paint()`中使用的坐标系。取而代之的是应用缩放因子，因此绘画应在0,0到`width()`，`height()`之间完成。
默认情况下，纹理大小与该物品大小相同。
注意：如果物品位于一个设备像素比与1不同的窗口上，这个缩放因子会隐含地应用到纹理尺寸上。

**如何使用：** 调用 `textureSize()` 读取当前值；它不会修改应用状态。

### `[explicit] QQuickPaintedItem::QQuickPaintedItem(QQuickItem *parent = nullptr)`

**作用与语义：**

用给定的`parent`项构造一个QQuickPaintedItem。

### `[override virtual noexcept] QQuickPaintedItem::~QQuickPaintedItem()`

**作用与语义：**

摧毁了`QQuickPaintedItem`。

### `bool QQuickPaintedItem::antialiasing() const`

**作用与语义：**

如果启用抗锯齿绘画，则返回 true;否则返回 false。
默认情况下，抗锯齿未被启用。

### `[override virtual] bool QQuickPaintedItem::isTextureProvider() const`

**作用与语义：**

重装：`QQuickItem::isTextureProvider()` const.
如果该项是纹理提供者，则返回 true。默认实现返回 false。
该函数可以从任何线程调用。

### `[override virtual protected] void QQuickPaintedItem::itemChange(QQuickItem::ItemChange change, const QQuickItem::ItemChangeData &value)`

**作用与语义：**

重实现自：`QQuickItem::itemChange`（QQuickItem：：ItemChange change，const QQuickItem：：ItemChangeData &value）。
当`change`发生时调用此物品。
`value`包含与变更相关的额外信息（如适用）。
如果你在子类中重新实现此方法，务必调用。
通常在实现结束时，确保`windowChanged()`信号会被发射。

### `bool QQuickPaintedItem::mipmap() const`

**作用与语义：**

如果启用了 mipmaps，则返回 true;否则，返回 false。
默认情况下，mipmapping 并未被启用。

### `bool QQuickPaintedItem::opaquePainting() const`

**作用与语义：**

如果该项不透明，则返回 true;否则返回 false。
默认情况下，涂装物品不是不透明的。

### `[pure virtual] void QQuickPaintedItem::paint(QPainter *painter)`

**作用与语义：**

该函数通常由QML场景图调用，它将元素的内容绘制为局部坐标。
底层纹理的大小由设置时的`textureSize`定义，或者物品大小乘以窗口的像素比。
该函数是在物品被填充`fillColor`后调用的。
在`QQuickPaintedItem`子类中重新实现该函数，使用`painter`来实现该物品的绘画实现。
注意：QML场景图使用两个独立线程，主线程负责处理事件或更新动画，另一线程负责实际发布图形资源更新和绘制调用记录。因此，paint()不是从主GUI线程调用，而是调用支持GL的渲染器线程。在调用paint()时，GUI线程被阻塞，因此是线程安全的。
警告：在创建QObject、发射信号、启动计时器等功能时必须极度谨慎，因为这些会与渲染线程产生关联。

### `QQuickPaintedItem::PerformanceHints QQuickPaintedItem::performanceHints() const`

**作用与语义：**

返回性能提示。
默认情况下，不会启用性能提示。

### `[override virtual protected] void QQuickPaintedItem::releaseResources()`

**作用与语义：**

重装：`QQuickItem::releaseResources()`。
当某个项目需要释放尚未由`QQuickItem::updatePaintNode()`返回节点管理的图形资源时，调用该函数。
当该项即将从之前渲染的窗口中移除时，就会发生这种情况。当调用该函数时，该项必定会有`window`。
该函数在图形界面线程中被调用，渲染线程的状态（使用时）未知。对象不应直接删除，而应通过`QQuickWindow::scheduleRenderJob()`调度进行清理。

### `void QQuickPaintedItem::setAntialiasing(bool enable)`

**作用与语义：**

如果`enable`正确，则启用了抗锯齿绘画。
默认情况下，抗锯齿未被启用。

### `void QQuickPaintedItem::setMipmap(bool enable)`

**作用与语义：**

如果`enable`为真，则关联纹理上已启用多频映射。
当物品缩小时，多重映射提升渲染速度并减少锯齿伪影。
默认情况下，mipmapping 并未被启用。

### `void QQuickPaintedItem::setOpaquePainting(bool opaque)`

**作用与语义：**

如果`opaque`为真，则该物品是不透明的;否则，它被视为半透明的。
不透明物品不会与场景其他部分融合，如果物品内容是不透明，你应该将此设置为为真以加快渲染速度。
默认情况下，涂装物品不是不透明的。

### `void QQuickPaintedItem::setPerformanceHint(QQuickPaintedItem::PerformanceHint hint, bool enabled = true)`

**作用与语义：**

如果`enabled`为真，则将该项的给定表现`hint`设定;否则清除性能提示。
默认情况下，没有启用性能提示/。

### `void QQuickPaintedItem::setPerformanceHints(QQuickPaintedItem::PerformanceHints hints)`

**作用与语义：**

将性能提示设置为`hints`。
默认情况下，没有启用性能提示/。

### `[override virtual] QSGTextureProvider *QQuickPaintedItem::textureProvider() const`

**作用与语义：**

重实现自：`QQuickItem::textureProvider()` const.
返回某个物品的纹理提供者。默认实现返回`nullptr`。
该函数只能在渲染线程中调用。

### `void QQuickPaintedItem::update(const QRect &rect = QRect())`

**作用与语义：**

安排重新绘制该物品中`rect`覆盖区域。每当物品需要重新绘制时，比如外观或大小变化，都可以调用此函数。
该函数不会立即绘制;它会安排一个绘画请求，当下一帧渲染时由QML场景图处理。只有当该物品可见时才会被重新绘制。

### `[override virtual protected] QSGNode *QQuickPaintedItem::updatePaintNode(QSGNode *oldNode, QQuickItem::UpdatePaintNodeData *data)`

**作用与语义：**

Reimplements： `QQuickItem::updatePaintNode`（QSGNode *oldNode， QQuickItem：：UpdatePaintNodeData *updatePaintNodeData）.
在渲染线程中调用，当需要将物品状态与场景图同步时。
如果用户在该项上设置了`QQuickItem::ItemHasContents`标志，则该函数是因`QQuickItem::update()`而被调用的。
该函数应返回该项场景图子树的根。大多数实现会返回包含该项视觉表示的单`QSGGeometryNode`。`oldNode` 是函数上次调用时返回的节点。`updatePaintNodeData` 提供指向该`QQuickItem`关联`QSGTransformNode`的指针。
在执行该函数时，主线程会被阻塞，因此可以安全地读取`QQuickItem`实例和主线程中其他对象的值。
如果没有调用 QQuickItem：：updatePaintNode() 而不会导致实际的场景图变化，比如`QSGNode::markDirty()`节点或添加和移除节点，那么底层实现可能会决定不再渲染场景，因为视觉效果是相同的。
警告：图形操作和与场景图的交互必须完全发生在渲染线程上，主要发生在 QQuickItem：：updatePaintNode() 调用期间。最好的经验法则是只在 QQuickItem：：updatePaintNode() 函数中使用带有“QSG” 前缀的类。
警告：该函数在渲染线程中被调用。这意味着任何创建的QObject或线程本地存储都会与渲染线程有关联，因此在此函数中进行除渲染外的其他操作时请谨慎。信号同样，它们会在渲染线程中发出，因此通常通过排队连接传递。
注意：所有带有 QSG 前缀的类应仅用于场景图的渲染线程。更多信息请参见场景图与渲染。

### `enum PerformanceHint { FastFBOResizing }`

**作用与语义：**

这个枚举描述了你可以启用以提升渲染性能的标志`QQuickPaintedItem`。默认情况下，这些标志都没有被设置。
- `QQuickPaintedItem::FastFBOResizing`：`0x1`;从Qt 6.0开始，该值被忽略。
PerformanceHints 类型是 QFlags 的 typedef<PerformanceHint>。它存储 PerformanceHint 值的 OR 组合。

### `flags PerformanceHints`

**作用与语义：**

这个枚举描述了你可以启用以提升渲染性能的标志`QQuickPaintedItem`。默认情况下，这些标志都没有被设置。
- `QQuickPaintedItem::FastFBOResizing`：`0x1`;从Qt 6.0开始，该值被忽略。
PerformanceHints 类型是 QFlags 的 typedef<PerformanceHint>。它存储 PerformanceHint 值的 OR 组合。

### `QColor fillColor() const`

**作用与语义：**

该属性保留物品的背景填充颜色。
默认情况下，填充颜色设置为`Qt::transparent`。
将填充颜色设置为无效颜色（例如 QColor()），以禁用背景填充。这可能会提升性能，如果 `paint()` 函数绘制到每帧的所有像素，这样做是安全的。

**如何使用：** 调用 `fillColor()` 读取当前值；它不会修改应用状态。

### `QQuickPaintedItem::RenderTarget renderTarget() const`

**作用与语义：**

该属性包含了该物品的渲染目标。
该属性定义了`QPainter`渲染的目标，可以是`QQuickPaintedItem::Image`、`QQuickPaintedItem::FramebufferObject`或`QQuickPaintedItem::InvertedYFramebufferObject`。
每种对象都有其优势，通常是性能与质量的区别。使用帧缓冲对象避免了将图像内容上传到图形内存纹理的高成本，同时使用图像实现高质量抗锯齿。
警告：调整帧缓冲区对象大小是一项昂贵操作，如果物品经常被调整大小，请避免使用`QQuickPaintedItem::FramebufferObject`渲染目标。
默认情况下，渲染目标是`QQuickPaintedItem::Image`。

**如何使用：** 调用 `renderTarget()` 读取当前值；它不会修改应用状态。

### `void setFillColor(const QColor &)`

**作用与语义：**

该属性保留物品的背景填充颜色。
默认情况下，填充颜色设置为`Qt::transparent`。
将填充颜色设置为无效颜色（例如 QColor()），以禁用背景填充。这可能会提升性能，如果 `paint()` 函数绘制到每帧的所有像素，这样做是安全的。

**如何使用：** 调用 `setFillColor(...)` 修改 `fillColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setRenderTarget(QQuickPaintedItem::RenderTarget target)`

**作用与语义：**

该属性包含了该物品的渲染目标。
该属性定义了`QPainter`渲染的目标，可以是`QQuickPaintedItem::Image`、`QQuickPaintedItem::FramebufferObject`或`QQuickPaintedItem::InvertedYFramebufferObject`。
每种对象都有其优势，通常是性能与质量的区别。使用帧缓冲对象避免了将图像内容上传到图形内存纹理的高成本，同时使用图像实现高质量抗锯齿。
警告：调整帧缓冲区对象大小是一项昂贵操作，如果物品经常被调整大小，请避免使用`QQuickPaintedItem::FramebufferObject`渲染目标。
默认情况下，渲染目标是`QQuickPaintedItem::Image`。

**如何使用：** 调用 `setRenderTarget(...)` 修改 `renderTarget`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTextureSize(const QSize &size)`

**作用与语义：**

定义了纹理的大小。
改变贴图大小不会影响`paint()`中使用的坐标系。取而代之的是应用缩放因子，因此绘画应在0,0到`width()`，`height()`之间完成。
默认情况下，纹理大小与该物品大小相同。
注意：如果物品位于一个设备像素比与1不同的窗口上，这个缩放因子会隐含地应用到纹理尺寸上。

**如何使用：** 调用 `setTextureSize(...)` 修改 `textureSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QSize textureSize() const`

**作用与语义：**

定义了纹理的大小。
改变贴图大小不会影响`paint()`中使用的坐标系。取而代之的是应用缩放因子，因此绘画应在0,0到`width()`，`height()`之间完成。
默认情况下，纹理大小与该物品大小相同。
注意：如果物品位于一个设备像素比与1不同的窗口上，这个缩放因子会隐含地应用到纹理尺寸上。

**如何使用：** 调用 `textureSize()` 读取当前值；它不会修改应用状态。

### `void fillColorChanged()`

**作用与语义：**

该属性保留物品的背景填充颜色。
默认情况下，填充颜色设置为`Qt::transparent`。
将填充颜色设置为无效颜色（例如 QColor()），以禁用背景填充。这可能会提升性能，如果 `paint()` 函数绘制到每帧的所有像素，这样做是安全的。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `fillColor` 的变化，不要把它当作普通函数主动调用。

### `void renderTargetChanged()`

**作用与语义：**

该属性包含了该物品的渲染目标。
该属性定义了`QPainter`渲染的目标，可以是`QQuickPaintedItem::Image`、`QQuickPaintedItem::FramebufferObject`或`QQuickPaintedItem::InvertedYFramebufferObject`。
每种对象都有其优势，通常是性能与质量的区别。使用帧缓冲对象避免了将图像内容上传到图形内存纹理的高成本，同时使用图像实现高质量抗锯齿。
警告：调整帧缓冲区对象大小是一项昂贵操作，如果物品经常被调整大小，请避免使用`QQuickPaintedItem::FramebufferObject`渲染目标。
默认情况下，渲染目标是`QQuickPaintedItem::Image`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `renderTarget` 的变化，不要把它当作普通函数主动调用。

### `void textureSizeChanged()`

**作用与语义：**

定义了纹理的大小。
改变贴图大小不会影响`paint()`中使用的坐标系。取而代之的是应用缩放因子，因此绘画应在0,0到`width()`，`height()`之间完成。
默认情况下，纹理大小与该物品大小相同。
注意：如果物品位于一个设备像素比与1不同的窗口上，这个缩放因子会隐含地应用到纹理尺寸上。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `textureSize` 的变化，不要把它当作普通函数主动调用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

### 状态和错误边界

属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

### 线程边界

大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

### 最容易出现的错误

不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QQuickPaintedItem` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
