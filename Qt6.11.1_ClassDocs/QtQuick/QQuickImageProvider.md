# QQuickImageProvider

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickImageProvider` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickImageProvider` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickImageProvider>`
- 继承自：QQmlImageProviderBase
- 直接派生类：QQuickAsyncImageProvider

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
target_link_libraries(mytarget PRIVATE Qt6::Quick)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

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

### 公有函数

- `QQuickImageProvider(QQmlImageProviderBase::ImageType type, QQmlImageProviderBase::Flags flags = Flags())`
- `virtual ~QQuickImageProvider() override`
- `virtual QImage requestImage(const QString &id, QSize *size, const QSize &requestedSize)`
- `virtual QPixmap requestPixmap(const QString &id, QSize *size, const QSize &requestedSize)`
- `virtual QQuickTextureFactory * requestTexture(const QString &id, QSize *size, const QSize &requestedSize)`

### 重实现的公有函数

- `virtual QQmlImageProviderBase::Flags flags() const override`
- `virtual QQmlImageProviderBase::ImageType imageType() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QQuickImageProvider::QQuickImageProvider(QQmlImageProviderBase::ImageType type, QQmlImageProviderBase::Flags flags = Flags())`

**作用与语义：**

创建一个图像提供商，提供给定`type`的图像，并按照给定`flags`行为。

### `[override virtual noexcept] QQuickImageProvider::~QQuickImageProvider()`

**作用与语义：**

摧毁了`QQuickImageProvider`。
注意：你派生类的解构器必须是线程安全的。

### `[override virtual] QQmlImageProviderBase::Flags QQuickImageProvider::flags() const`

**作用与语义：**

重装：`QQmlImageProviderBase::flags()` const.
返回该提供商设置的标志。

### `[override virtual] QQmlImageProviderBase::ImageType QQuickImageProvider::imageType() const`

**作用与语义：**

重装：`QQmlImageProviderBase::imageType()` const.
返回该提供商支持的图像类型。

### `[virtual] QImage QQuickImageProvider::requestImage(const QString &id, QSize *size, const QSize &requestedSize)`

**作用与语义：**

实现此方法返回带`id`的图像。默认实现返回的是空图像。
`id`是请求的图像源，去除了“image：”方案和提供者标识符。例如，如果图像`source`为“image://myprovider/icons/home”，则给定的`id`为“icons/home”。
`requestedSize`对应于图片项请求的`Image::sourceSize`。如果`requestedSize`是有效大小，返回的图像应为该大小。
无论哪种情况，`size`都必须设置为图像的原始大小。如果相关`Image`的值未被明确设置，这用于设置相关  的`width`和`height`。
注意：该方法可能被多个线程调用，因此确保实现为重入。

### `[virtual] QPixmap QQuickImageProvider::requestPixmap(const QString &id, QSize *size, const QSize &requestedSize)`

**作用与语义：**

实现此方法返回带有`id`的像素映射。默认实现返回的是空像素映射。
`id`是请求的图像源，去除了“image：”方案和提供者标识符。例如，如果图像`source`为“image://myprovider/icons/home”，给定的`id`将是“icons/home”。
`requestedSize`对应于图片项请求的`Image::sourceSize`。如果`requestedSize`是有效大小，返回的图像应当是该大小。
无论哪种情况，`size`都必须设置为图像的原始大小。如果相关`Image`的`width`和`height`未被明确设置，则用于设置这些值。
注意：该方法可能被多个线程调用，因此确保实现为重入。

### `[virtual] QQuickTextureFactory *QQuickImageProvider::requestTexture(const QString &id, QSize *size, const QSize &requestedSize)`

**作用与语义：**

实现此方法以返回纹理`id`。默认实现返回`nullptr`。
`id`是请求的图像源，去除了“image：”方案和提供者标识符。例如，如果图像`source`为“image://myprovider/icons/home”，则给定的`id`为“icons/home”。
`requestedSize`对应于图片项请求的`Image::sourceSize`。如果`requestedSize`是有效大小，返回的图像应当是该大小。
无论哪种情况，`size`都必须设置为图像的原始大小。如果相关`Image`的`width`和`height`未被明确设置，则用于设置这些值。
注意：该方法可能被多个线程调用，因此确保实现为重入。

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

`QQuickImageProvider` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
