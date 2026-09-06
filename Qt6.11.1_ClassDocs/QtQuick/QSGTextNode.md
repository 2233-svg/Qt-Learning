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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 27 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QSGTextNode::RenderType`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGTextNode` 暴露的类型声明 `渲染、类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:RenderType`。
- 属性名：`QSGTextNode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QSGTextNode::TextStyle`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGTextNode` 暴露的类型声明 `文本、Style`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:TextStyle`。
- 属性名：`QSGTextNode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGTextNode::addTextDocument(QPointF position, QTextDocument *document, int selectionStart = -1, int selectionCount = -1)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QSGTextNode` 添加依赖、数据或子对象的 API `addTextDocument`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `QPointF`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `document`：类型为 `QTextDocument *`。没有默认值，调用时必须提供。传入 `QTextDocument *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `selectionStart`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `selectionCount`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGTextNode::addTextLayout(QPointF position, QTextLayout *layout, int selectionStart = -1, int selectionCount = -1, int lineStart = 0, int lineCount = -1)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QSGTextNode` 添加依赖、数据或子对象的 API `addTextLayout`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `QPointF`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `layout`：类型为 `QTextLayout *`。没有默认值，调用时必须提供。参与操作的布局对象。通常表示整个子布局的几何区域和所有权，不等于子布局里的某一个控件。
- 参数 `selectionStart`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `selectionCount`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `lineStart`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `lineCount`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGTextNode::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QColor QSGTextNode::color() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGTextNode::color` 用于计算、查询或取得与“color”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual private] void QSGTextNode::doAddTextDocument(QPointF position, QTextDocument *document, int selectionStart, int selectionCount)`

**API 类别：** 成员函数说明

**中文解读：** `QSGTextNode::doAddTextDocument` 用于执行与“do、添加、文本、Document”相关的操作。调用时要先确认当前状态和 `position`、`document`、`selectionStart`、`selectionCount` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `QPointF`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `document`：类型为 `QTextDocument *`。没有默认值，调用时必须提供。传入 `QTextDocument *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `selectionStart`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `selectionCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual private] void QSGTextNode::doAddTextLayout(QPointF position, QTextLayout *layout, int selectionStart, int selectionCount, int lineStart, int lineCount)`

**API 类别：** 成员函数说明

**中文解读：** `QSGTextNode::doAddTextLayout` 用于执行与“do、添加、文本、Layout”相关的操作。调用时要先确认当前状态和 `position`、`layout`、`selectionStart`、`selectionCount`、`lineStart`、`lineCount` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `QPointF`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `layout`：类型为 `QTextLayout *`。没有默认值，调用时必须提供。参与操作的布局对象。通常表示整个子布局的几何区域和所有权，不等于子布局里的某一个控件。
- 参数 `selectionStart`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `selectionCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `lineStart`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `lineCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSGTexture::Filtering QSGTextNode::filtering() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGTextNode::filtering` 用于计算、查询或取得与“filtering”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGTexture::Filtering`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGTexture::Filtering`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QColor QSGTextNode::linkColor() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGTextNode::linkColor` 用于计算、查询或取得与“link、Color”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSGTextNode::RenderType QSGTextNode::renderType() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSGTextNode` 的核心操作 `renderType`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QSGTextNode::RenderType`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] int QSGTextNode::renderTypeQuality() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSGTextNode` 的核心操作 `renderTypeQuality`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QColor QSGTextNode::selectionColor() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGTextNode::selectionColor` 用于计算、查询或取得与“selection、Color”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QColor QSGTextNode::selectionTextColor() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGTextNode::selectionTextColor` 用于计算、查询或取得与“selection、文本、Color”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGTextNode::setColor(QColor color)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setColor`。调用它会改变 `QSGTextNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `QColor`。没有默认值，调用时必须提供。传入 `QColor` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGTextNode::setFiltering(QSGTexture::Filtering filtering)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFiltering`。调用它会改变 `QSGTextNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `filtering`：类型为 `QSGTexture::Filtering`。没有默认值，调用时必须提供。传入 `QSGTexture::Filtering` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGTextNode::setLinkColor(QColor linkColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setLinkColor`。调用它会改变 `QSGTextNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `linkColor`：类型为 `QColor`。没有默认值，调用时必须提供。传入 `QColor` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGTextNode::setRenderType(QSGTextNode::RenderType renderType)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRenderType`。调用它会改变 `QSGTextNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `renderType`：类型为 `QSGTextNode::RenderType`。没有默认值，调用时必须提供。传入 `QSGTextNode::RenderType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGTextNode::setRenderTypeQuality(int renderTypeQuality)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRenderTypeQuality`。调用它会改变 `QSGTextNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `renderTypeQuality`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGTextNode::setSelectionColor(QColor color)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSelectionColor`。调用它会改变 `QSGTextNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `QColor`。没有默认值，调用时必须提供。传入 `QColor` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGTextNode::setSelectionTextColor(QColor selectionTextColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSelectionTextColor`。调用它会改变 `QSGTextNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `selectionTextColor`：类型为 `QColor`。没有默认值，调用时必须提供。传入 `QColor` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGTextNode::setStyleColor(QColor styleColor)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStyleColor`。调用它会改变 `QSGTextNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `styleColor`：类型为 `QColor`。没有默认值，调用时必须提供。传入 `QColor` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGTextNode::setTextStyle(QSGTextNode::TextStyle textStyle)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTextStyle`。调用它会改变 `QSGTextNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `textStyle`：类型为 `QSGTextNode::TextStyle`。没有默认值，调用时必须提供。传入 `QSGTextNode::TextStyle` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGTextNode::setViewport(const QRectF &viewport)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setViewport`。调用它会改变 `QSGTextNode` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `viewport`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QColor QSGTextNode::styleColor() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGTextNode::styleColor` 用于计算、查询或取得与“style、Color”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSGTextNode::TextStyle QSGTextNode::textStyle()`

**API 类别：** 成员函数说明

**中文解读：** `QSGTextNode::textStyle` 用于计算、查询或取得与“文本、Style”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGTextNode::TextStyle`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGTextNode::TextStyle`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QRectF QSGTextNode::viewport() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGTextNode::viewport` 用于计算、查询或取得与“viewport”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
