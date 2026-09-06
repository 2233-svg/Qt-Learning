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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 51 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QSGGeometry::AttributeType`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGGeometry` 暴露的类型声明 `Attribute、类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:AttributeType`。
- 属性名：`QSGGeometry`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QSGGeometry::DataPattern`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGGeometry` 暴露的类型声明 `数据访问、Pattern`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:DataPattern`。
- 属性名：`QSGGeometry`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QSGGeometry::DrawingMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGGeometry` 暴露的类型声明 `Drawing、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:DrawingMode`。
- 属性名：`QSGGeometry`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QSGGeometry::Type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGGeometry` 暴露的类型声明 `类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Type`。
- 属性名：`QSGGeometry`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGGeometry::QSGGeometry(const QSGGeometry::AttributeSet &attributes, int vertexCount, int indexCount = 0, int indexType = UnsignedShortType)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSGGeometry` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `attributes`：类型为 `const QSGGeometry::AttributeSet &`。没有默认值，调用时必须提供。传入 `const QSGGeometry::AttributeSet &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `vertexCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `indexCount`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `indexType`：类型为 `int`。默认值为 `UnsignedShortType`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QSGGeometry::~QSGGeometry()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSGGeometry` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGGeometry::allocate(int vertexCount, int indexCount = 0)`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::allocate` 用于执行与“allocate”相关的操作。调用时要先确认当前状态和 `vertexCount`、`indexCount` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `vertexCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `indexCount`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QSGGeometry::attributeCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::attributeCount` 用于计算、查询或取得与“attribute、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QSGGeometry::Attribute *QSGGeometry::attributes() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::attributes` 用于计算、查询或取得与“attributes”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QSGGeometry::Attribute *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QSGGeometry::Attribute *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] const QSGGeometry::AttributeSet &QSGGeometry::defaultAttributes_ColoredPoint2D()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `defaultAttributes_ColoredPoint2D`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`const QSGGeometry::AttributeSet &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] const QSGGeometry::AttributeSet &QSGGeometry::defaultAttributes_Point2D()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `defaultAttributes_Point2D`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`const QSGGeometry::AttributeSet &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] const QSGGeometry::AttributeSet &QSGGeometry::defaultAttributes_TexturedPoint2D()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `defaultAttributes_TexturedPoint2D`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`const QSGGeometry::AttributeSet &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `unsigned int QSGGeometry::drawingMode() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSGGeometry` 的核心操作 `drawingMode`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`unsigned int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QSGGeometry::indexCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::indexCount` 用于计算、查询或取得与“索引、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void *QSGGeometry::indexData()`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::indexData` 用于计算、查询或取得与“索引、数据访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const void *QSGGeometry::indexData() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::indexData` 用于计算、查询或取得与“索引、数据访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const void *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const void *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `uint *QSGGeometry::indexDataAsUInt()`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::indexDataAsUInt` 用于计算、查询或取得与“索引、数据访问、As、U、Int”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uint *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uint *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const uint *QSGGeometry::indexDataAsUInt() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::indexDataAsUInt` 用于计算、查询或取得与“索引、数据访问、As、U、Int”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const uint *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const uint *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint16 *QSGGeometry::indexDataAsUShort()`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::indexDataAsUShort` 用于计算、查询或取得与“索引、数据访问、As、U、Short”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `quint16 *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint16 *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const quint16 *QSGGeometry::indexDataAsUShort() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::indexDataAsUShort` 用于计算、查询或取得与“索引、数据访问、As、U、Short”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const quint16 *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const quint16 *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGGeometry::DataPattern QSGGeometry::indexDataPattern() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::indexDataPattern` 用于计算、查询或取得与“索引、数据访问、Pattern”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGGeometry::DataPattern`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGGeometry::DataPattern`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QSGGeometry::indexType() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::indexType` 用于计算、查询或取得与“索引、类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `float QSGGeometry::lineWidth() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::lineWidth` 用于计算、查询或取得与“行、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `float`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`float`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGGeometry::markIndexDataDirty()`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::markIndexDataDirty` 用于执行与“mark、索引、数据访问、Dirty”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGGeometry::markVertexDataDirty()`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::markVertexDataDirty` 用于执行与“mark、Vertex、数据访问、Dirty”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGGeometry::setDrawingMode(unsigned int mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDrawingMode`。调用它会改变 `QSGGeometry` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `unsigned int`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] void QSGGeometry::setIndexCount(int count)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setIndexCount`。调用它会改变 `QSGGeometry` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGGeometry::setIndexDataPattern(QSGGeometry::DataPattern p)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setIndexDataPattern`。调用它会改变 `QSGGeometry` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `p`：类型为 `QSGGeometry::DataPattern`。没有默认值，调用时必须提供。传入 `QSGGeometry::DataPattern` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGGeometry::setLineWidth(float width)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setLineWidth`。调用它会改变 `QSGGeometry` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `width`：类型为 `float`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] void QSGGeometry::setVertexCount(int count)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVertexCount`。调用它会改变 `QSGGeometry` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGGeometry::setVertexDataPattern(QSGGeometry::DataPattern p)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVertexDataPattern`。调用它会改变 `QSGGeometry` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `p`：类型为 `QSGGeometry::DataPattern`。没有默认值，调用时必须提供。传入 `QSGGeometry::DataPattern` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QSGGeometry::sizeOfIndex() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::sizeOfIndex` 用于计算、查询或取得与“尺寸或数量、Of、索引”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QSGGeometry::sizeOfVertex() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::sizeOfVertex` 用于计算、查询或取得与“尺寸或数量、Of、Vertex”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QSGGeometry::updateColoredRectGeometry(QSGGeometry *g, const QRectF &rect)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `updateColoredRectGeometry`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `g`：类型为 `QSGGeometry *`。没有默认值，调用时必须提供。传入 `QSGGeometry *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QSGGeometry::updateRectGeometry(QSGGeometry *g, const QRectF &rect)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `updateRectGeometry`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `g`：类型为 `QSGGeometry *`。没有默认值，调用时必须提供。传入 `QSGGeometry *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QSGGeometry::updateTexturedRectGeometry(QSGGeometry *g, const QRectF &rect, const QRectF &textureRect)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `updateTexturedRectGeometry`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `g`：类型为 `QSGGeometry *`。没有默认值，调用时必须提供。传入 `QSGGeometry *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。
- 参数 `textureRect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QSGGeometry::vertexCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::vertexCount` 用于计算、查询或取得与“vertex、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void *QSGGeometry::vertexData()`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::vertexData` 用于计算、查询或取得与“vertex、数据访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const void *QSGGeometry::vertexData() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::vertexData` 用于计算、查询或取得与“vertex、数据访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const void *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const void *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGGeometry::ColoredPoint2D *QSGGeometry::vertexDataAsColoredPoint2D()`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::vertexDataAsColoredPoint2D` 用于计算、查询或取得与“vertex、数据访问、As、Colored、Point、2、D”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGGeometry::ColoredPoint2D *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGGeometry::ColoredPoint2D *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QSGGeometry::ColoredPoint2D *QSGGeometry::vertexDataAsColoredPoint2D() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::vertexDataAsColoredPoint2D` 用于计算、查询或取得与“vertex、数据访问、As、Colored、Point、2、D”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QSGGeometry::ColoredPoint2D *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QSGGeometry::ColoredPoint2D *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGGeometry::Point2D *QSGGeometry::vertexDataAsPoint2D()`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::vertexDataAsPoint2D` 用于计算、查询或取得与“vertex、数据访问、As、Point、2、D”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGGeometry::Point2D *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGGeometry::Point2D *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QSGGeometry::Point2D *QSGGeometry::vertexDataAsPoint2D() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::vertexDataAsPoint2D` 用于计算、查询或取得与“vertex、数据访问、As、Point、2、D”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QSGGeometry::Point2D *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QSGGeometry::Point2D *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGGeometry::TexturedPoint2D *QSGGeometry::vertexDataAsTexturedPoint2D()`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::vertexDataAsTexturedPoint2D` 用于计算、查询或取得与“vertex、数据访问、As、Textured、Point、2、D”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGGeometry::TexturedPoint2D *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGGeometry::TexturedPoint2D *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QSGGeometry::TexturedPoint2D *QSGGeometry::vertexDataAsTexturedPoint2D() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::vertexDataAsTexturedPoint2D` 用于计算、查询或取得与“vertex、数据访问、As、Textured、Point、2、D”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QSGGeometry::TexturedPoint2D *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QSGGeometry::TexturedPoint2D *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGGeometry::DataPattern QSGGeometry::vertexDataPattern() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGGeometry::vertexDataPattern` 用于计算、查询或取得与“vertex、数据访问、Pattern”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGGeometry::DataPattern`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGGeometry::DataPattern`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `struct Attribute`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGGeometry` 的 `Attribute` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `struct AttributeSet`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGGeometry` 的 `Attribute、设置` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `struct ColoredPoint2D`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGGeometry` 的 `Colored、Point、2、D` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `struct Point2D`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGGeometry` 的 `Point、2、D` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `struct TexturedPoint2D`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGGeometry` 的 `Textured、Point、2、D` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

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

`QSGGeometry` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
