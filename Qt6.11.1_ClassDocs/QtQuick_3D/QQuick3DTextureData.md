# QQuick3DTextureData

> Qt 6.11.1 · Qt Quick 3D

## 1. 先建立直觉

**一句话定位：** `QQuick3DTextureData` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 3D 在 Qt Quick 中加入 3D 场景、相机、材质、模型和渲染能力。

### 这是什么

`QQuick3DTextureData` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuick3DTextureData>`
- 继承自：QQuick3DObject
- 直接派生类：未在类页中列出

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

### 状态、生命周期和线程

**生命周期：** 场景图节点和材质的有效期受窗口、组件和渲染阶段控制；纹理、材质和几何通常要在正确的 render context 中创建/释放。节点被删除或场景图失效后，底层 GPU 资源不能继续使用。

**状态与结果：** 区分 GUI/同步阶段、渲染阶段、节点 dirty 状态、纹理状态和后端能力。改变节点属性通常要标记更新，不能在错误阶段直接修改资源；材质是否可用还受默认后端限制。

**线程与事件循环：** QSG 类型经常运行在 render thread，不能从 GUI 线程或后台线程随意读写。通过 QQuickItem 的同步接口在规定阶段交换数据，避免跨线程共享 GPU 资源。

## 3. 直接使用

需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。 使用时通常按这个过程组织：注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

```cpp
#include <QQuick3DTextureData>

// QSG 类型只能在 Qt Quick 规定的场景图阶段使用。
// 先确认渲染后端、线程和对象生命周期，再创建或配置对象。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Format { None, RGBA8, RGBA16F, RGBA32F, RGBE8, …, ASTC_12x12 }`

### 公有函数

- `int depth() const`
- `QQuick3DTextureData::Format format() const`
- `bool hasTransparency() const`
- `void setDepth(int depth)`
- `void setFormat(QQuick3DTextureData::Format format)`
- `void setHasTransparency(bool hasTransparency)`
- `void setSize(const QSize &size)`
- `void setTextureData(const QByteArray &data)`
- `QSize size() const`
- `const QByteArray textureData() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QQuick3DTextureData::Format`

**作用与语义：**

返回`textureData`属性中分配的纹理数据的颜色格式。
- `QQuick3DTextureData::None`：`0`;颜色格式未定义
- `QQuick3DTextureData::RGBA8`：`1`;彩色格式在R、G、B和alpha通道中被视为8位整数。
- `QQuick3DTextureData::RGBA16F`：`2`;彩色格式在R、G、B和alpha通道中被视为16位浮点。
- `QQuick3DTextureData::RGBA32F`：`3`;颜色格式在R、G、B和alpha通道中被视为32位浮点。
- `QQuick3DTextureData::RGBE8`：`4`;颜色格式在R、G和B通道中被视为8位尾数，8位共享指数。
- `QQuick3DTextureData::R8`：`5`;颜色格式在R通道中被视为8位整数。
- `QQuick3DTextureData::R16`：`6`;颜色格式在R通道中被视为16位整数。
- `QQuick3DTextureData::R16F`：`7`;色彩格式被视为R通道中的16位浮点。
- `QQuick3DTextureData::R32F`：`8`;彩色格式被视为32位浮点R通道。
- `QQuick3DTextureData::BC1`：`9`;彩色格式为BC1压缩格式，包含R、G、B和Alpha通道。
- `QQuick3DTextureData::BC2`：`10`;彩色格式为BC2压缩格式，包含R、G、B和Alpha通道。
- `QQuick3DTextureData::BC3`：`11`;彩色格式为BC3压缩格式，包含R、G、B和Alpha通道。
- `QQuick3DTextureData::BC4`：`12`;彩色格式为BC4压缩格式，带有一个彩色通道。
- `QQuick3DTextureData::BC5`：`13`;彩色格式为BC5压缩格式，带有两个色彩通道。
- `QQuick3DTextureData::BC6H`：`14`;色彩格式为BC6H压缩格式，拥有三个高动态范围色彩通道。
- `QQuick3DTextureData::BC7`：`15`;彩色格式为BC7压缩格式，包含R、G、B和Alpha通道。
- `QQuick3DTextureData::DXT1_RGBA`：`16`;彩色格式被视为带有R、G、B和alpha通道的DXT1压缩格式。
- `QQuick3DTextureData::DXT1_RGB`：`17`;彩色格式被视为带有R、G和B通道的DXT1压缩格式。
- `QQuick3DTextureData::DXT3_RGBA`：`18`;彩色格式被视为带有R、G、B和alpha通道的DXT3压缩格式。
- `QQuick3DTextureData::DXT5_RGBA`：`19`;彩色格式被视为带有R、G、B和alpha通道的DXT5压缩格式。
- `QQuick3DTextureData::ETC2_RGB8`：`20`;彩色格式被视为 ETC2 压缩格式，用于 RGB888 数据
- `QQuick3DTextureData::ETC2_RGB8A1`：`21`;颜色格式被视为 ETC2 压缩格式，用于 RGBA 数据，其中 alpha 为 1 位。
- `QQuick3DTextureData::ETC2_RGBA8`：`22`;彩色格式被视为带有RGBA8888数据的ETC2压缩格式。
- `QQuick3DTextureData::ASTC_4x4`：`23`;彩色格式被视为带有4x4块面积的ASTC压缩格式。
- `QQuick3DTextureData::ASTC_5x4`：`24`;彩色格式被视为ASTC压缩格式，采用5x4块封装。
- `QQuick3DTextureData::ASTC_5x5`：`25`;彩色格式被视为ASTC压缩格式，块尺寸为5x5。
- `QQuick3DTextureData::ASTC_6x5`：`26`;彩色格式被视为ASTC压缩格式，采用6x5块封装。
- `QQuick3DTextureData::ASTC_6x6`：`27`;彩色格式被视为ASTC压缩格式，块尺寸为6x6。
- `QQuick3DTextureData::ASTC_8x5`：`28`;彩色格式被视为ASTC压缩格式，采用8x5块封面积。
- `QQuick3DTextureData::ASTC_8x6`：`29`;彩色格式被视为ASTC压缩格式，尺寸为8x6块。
- `QQuick3DTextureData::ASTC_8x8`：`30`;彩色格式被视为ASTC压缩格式，采用8x8块封装。
- `QQuick3DTextureData::ASTC_10x5`：`31`;彩色格式被视为带有10x5块封面积的ASTC压缩格式。
- `QQuick3DTextureData::ASTC_10x6`：`32`;彩色格式被视为带有10x6块面积的ASTC压缩格式。
- `QQuick3DTextureData::ASTC_10x8`：`33`;彩色格式被视为ASTC压缩格式，具有10x8块的面积。
- `QQuick3DTextureData::ASTC_10x10`：`34`;彩色格式被视为ASTC压缩格式，块面积为10x10。
- `QQuick3DTextureData::ASTC_12x10`：`35`;彩色格式被视为ASTC压缩格式，采用12x10块封装。
- `QQuick3DTextureData::ASTC_12x12`：`36`;彩色格式被视为ASTC压缩格式，块尺寸为12x12。
注意：除`RGBA8`外，并非所有格式在运行时都支持，因为这取决于所使用的后端以及所使用的硬件。


注意：`RGBE`内部表示为`RGBA8`，但当用作光探针或天空盒纹理时，则如描述所述。


注意：使用`None`值时，默认值为`RGBA8`。

### `int QQuick3DTextureData::depth() const`

**作用与语义：**

返回纹理数据的像素深度。

### `QQuick3DTextureData::Format QQuick3DTextureData::format() const`

**作用与语义：**

返回纹理数据的格式。

### `bool QQuick3DTextureData::hasTransparency() const`

**作用与语义：**

如果纹理数据是透明的，返回`true`。
默认值是`false`。

### `void QQuick3DTextureData::setDepth(int depth)`

**作用与语义：**

设置纹理数据的像素数`depth`。将深度设为0意味着纹理被处理为3D纹理。

### `void QQuick3DTextureData::setFormat(QQuick3DTextureData::Format format)`

**作用与语义：**

设置纹理数据的`format`。
默认格式为 /c RGBA8。

### `void QQuick3DTextureData::setHasTransparency(bool hasTransparency)`

**作用与语义：**

如果纹理数据有活动的 alpha 通道且非不透明值，则将 `hasTransparency` 设为 true。
引擎将此作为优化，使支持alpha通道的格式无需检查每个值是否为非不透明值。

### `void QQuick3DTextureData::setSize(const QSize &size)`

**作用与语义：**

设置纹理数据的像素数（像素）的 `size`。

### `void QQuick3DTextureData::setTextureData(const QByteArray &data)`

**作用与语义：**

设置纹理数据。`data`的内容必须尊重`size`和`format`属性，因为后端会尝试上传并使用这些数据，就像是尺寸和格式的纹理一样，如果有任何偏差，结果很可能介于纹理渲染错误或崩溃之间。

### `QSize QQuick3DTextureData::size() const`

**作用与语义：**

返回纹理数据的像素大小。

### `const QByteArray QQuick3DTextureData::textureData() const`

**作用与语义：**

返回该项定义的当前纹理数据。

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

`QQuick3DTextureData` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
