# QAbstractTextDocumentLayout

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QAbstractTextDocumentLayout` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QAbstractTextDocumentLayout` 是 Qt GUI 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractTextDocumentLayout>`
- 继承自：QObject
- 直接派生类：QPlainTextDocumentLayout

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `struct PaintContext`
- `struct Selection`

### 公有函数

- `QAbstractTextDocumentLayout(QTextDocument *document)`
- `QString anchorAt(const QPointF &position) const`
- `virtual QRectF blockBoundingRect(const QTextBlock &block) const = 0`
- `QTextBlock blockWithMarkerAt(const QPointF &pos) const`
- `QTextDocument * document() const`
- `virtual QSizeF documentSize() const = 0`
- `virtual void draw(QPainter *painter, const QAbstractTextDocumentLayout::PaintContext &context) = 0`
- `QTextFormat formatAt(const QPointF &pos) const`
- `virtual QRectF frameBoundingRect(QTextFrame *frame) const = 0`
- `QTextObjectInterface * handlerForObject(int objectType) const`
- `virtual int hitTest(const QPointF &point, Qt::HitTestAccuracy accuracy) const = 0`
- `QString imageAt(const QPointF &pos) const`
- `virtual int pageCount() const = 0`
- `QPaintDevice * paintDevice() const`
- `void registerHandler(int objectType, QObject *component)`
- `void setPaintDevice(QPaintDevice *device)`
- `void unregisterHandler(int objectType, QObject *component = nullptr)`

### 信号

- `void documentSizeChanged(const QSizeF &newSize)`
- `void pageCountChanged(int newPages)`
- `void update(const QRectF &rect = QRectF(0., 0., 1000000000., 1000000000.))`
- `void updateBlock(const QTextBlock &block)`

### 保护函数

- `virtual void documentChanged(int position, int charsRemoved, int charsAdded) = 0`
- `virtual void drawInlineObject(QPainter *painter, const QRectF &rect, QTextInlineObject object, int posInDocument, const QTextFormat &format)`
- `QTextCharFormat format(int position)`
- `virtual void positionInlineObject(QTextInlineObject item, int posInDocument, const QTextFormat &format)`
- `virtual void resizeInlineObject(QTextInlineObject item, int posInDocument, const QTextFormat &format)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 28 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[explicit] QAbstractTextDocumentLayout::QAbstractTextDocumentLayout(QTextDocument *document)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractTextDocumentLayout` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `document`：类型为 `QTextDocument *`。没有默认值，调用时必须提供。传入 `QTextDocument *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QAbstractTextDocumentLayout::anchorAt(const QPointF &position) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractTextDocumentLayout::anchorAt` 用于计算、查询或取得与“anchor、按位置访问”相关的操作。调用时要先确认当前状态和 `position` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `position`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QRectF QAbstractTextDocumentLayout::blockBoundingRect(const QTextBlock &block) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractTextDocumentLayout::blockBoundingRect` 用于计算、查询或取得与“阻塞或屏蔽、Bounding、Rect”相关的操作。调用时要先确认当前状态和 `block` 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `block`：类型为 `const QTextBlock &`。没有默认值，调用时必须提供。传入 `const QTextBlock &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextBlock QAbstractTextDocumentLayout::blockWithMarkerAt(const QPointF &pos) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractTextDocumentLayout::blockWithMarkerAt` 用于计算、查询或取得与“阻塞或屏蔽、With、Marker、按位置访问”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QTextBlock`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextBlock`。
- 参数 `pos`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextDocument *QAbstractTextDocumentLayout::document() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractTextDocumentLayout::document` 用于计算、查询或取得与“document”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextDocument *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextDocument *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual protected] void QAbstractTextDocumentLayout::documentChanged(int position, int charsRemoved, int charsAdded)`

**API 类别：** 成员函数说明

**中文解读：** 这是状态变化通知 `documentChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `int`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `charsRemoved`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `charsAdded`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSizeF QAbstractTextDocumentLayout::documentSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractTextDocumentLayout::documentSize` 用于计算、查询或取得与“document、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSizeF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSizeF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QAbstractTextDocumentLayout::documentSizeChanged(const QSizeF &newSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractTextDocumentLayout` 发出的通知信号 `documentSizeChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `newSize`：类型为 `const QSizeF &`。没有默认值，调用时必须提供。传入 `const QSizeF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QAbstractTextDocumentLayout::draw(QPainter *painter, const QAbstractTextDocumentLayout::PaintContext &context)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractTextDocumentLayout` 的核心操作 `draw`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。
- 参数 `context`：类型为 `const QAbstractTextDocumentLayout::PaintContext &`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QAbstractTextDocumentLayout::drawInlineObject(QPainter *painter, const QRectF &rect, QTextInlineObject object, int posInDocument, const QTextFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractTextDocumentLayout` 的核心操作 `drawInlineObject`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。
- 参数 `object`：类型为 `QTextInlineObject`。没有默认值，调用时必须提供。传入 `QTextInlineObject` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `posInDocument`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `const QTextFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] QTextCharFormat QAbstractTextDocumentLayout::format(int position)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `format`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QTextCharFormat`。
- 参数 `position`：类型为 `int`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextFormat QAbstractTextDocumentLayout::formatAt(const QPointF &pos) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `formatAt`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QTextFormat`。
- 参数 `pos`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QRectF QAbstractTextDocumentLayout::frameBoundingRect(QTextFrame *frame) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractTextDocumentLayout::frameBoundingRect` 用于计算、查询或取得与“frame、Bounding、Rect”相关的操作。调用时要先确认当前状态和 `frame` 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `frame`：类型为 `QTextFrame *`。没有默认值，调用时必须提供。传入 `QTextFrame *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextObjectInterface *QAbstractTextDocumentLayout::handlerForObject(int objectType) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractTextDocumentLayout::handlerForObject` 用于计算、查询或取得与“handler、For、Object”相关的操作。调用时要先确认当前状态和 `objectType` 的有效范围；返回类型是 `QTextObjectInterface *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextObjectInterface *`。
- 参数 `objectType`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] int QAbstractTextDocumentLayout::hitTest(const QPointF &point, Qt::HitTestAccuracy accuracy) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractTextDocumentLayout::hitTest` 用于计算、查询或取得与“hit、Test”相关的操作。调用时要先确认当前状态和 `point`、`accuracy` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `accuracy`：类型为 `Qt::HitTestAccuracy`。没有默认值，调用时必须提供。传入 `Qt::HitTestAccuracy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QAbstractTextDocumentLayout::imageAt(const QPointF &pos) const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractTextDocumentLayout::imageAt` 用于计算、查询或取得与“image、按位置访问”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `pos`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] int QAbstractTextDocumentLayout::pageCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractTextDocumentLayout::pageCount` 用于计算、查询或取得与“page、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QAbstractTextDocumentLayout::pageCountChanged(int newPages)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractTextDocumentLayout` 发出的通知信号 `pageCountChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `newPages`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPaintDevice *QAbstractTextDocumentLayout::paintDevice() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractTextDocumentLayout` 的核心操作 `paintDevice`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QPaintDevice *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QAbstractTextDocumentLayout::positionInlineObject(QTextInlineObject item, int posInDocument, const QTextFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractTextDocumentLayout::positionInlineObject` 用于执行与“position、Inline、Object”相关的操作。调用时要先确认当前状态和 `item`、`posInDocument`、`format` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QTextInlineObject`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。
- 参数 `posInDocument`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `const QTextFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QAbstractTextDocumentLayout::registerHandler(int objectType, QObject *component)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractTextDocumentLayout::registerHandler` 用于执行与“注册、Handler”相关的操作。调用时要先确认当前状态和 `objectType`、`component` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `objectType`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `component`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QAbstractTextDocumentLayout::resizeInlineObject(QTextInlineObject item, int posInDocument, const QTextFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractTextDocumentLayout::resizeInlineObject` 用于执行与“调整尺寸、Inline、Object”相关的操作。调用时要先确认当前状态和 `item`、`posInDocument`、`format` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QTextInlineObject`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。
- 参数 `posInDocument`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `const QTextFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QAbstractTextDocumentLayout::setPaintDevice(QPaintDevice *device)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPaintDevice`。调用它会改变 `QAbstractTextDocumentLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `device`：类型为 `QPaintDevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QAbstractTextDocumentLayout::unregisterHandler(int objectType, QObject *component = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** `QAbstractTextDocumentLayout::unregisterHandler` 用于执行与“取消注册、Handler”相关的操作。调用时要先确认当前状态和 `objectType`、`component` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `objectType`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `component`：类型为 `QObject *`。默认值为 `nullptr`。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QAbstractTextDocumentLayout::update(const QRectF &rect = QRectF(0., 0., 1000000000., 1000000000.))`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractTextDocumentLayout` 发出的通知信号 `update`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRectF &`。默认值为 `QRectF(0., 0., 1000000000., 1000000000.)`。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 通常在数据变化后调用，让 Qt 合并重绘请求；不要直接调用 `paintEvent()`。

### `[signal] void QAbstractTextDocumentLayout::updateBlock(const QTextBlock &block)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAbstractTextDocumentLayout` 发出的通知信号 `updateBlock`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `block`：类型为 `const QTextBlock &`。没有默认值，调用时必须提供。传入 `const QTextBlock &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常在数据变化后调用，让 Qt 合并重绘请求；不要直接调用 `paintEvent()`。

### `struct PaintContext`

**API 类别：** 公有类型

**中文解读：** 这是 `QAbstractTextDocumentLayout` 的 `绘制、Context` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `struct Selection`

**API 类别：** 公有类型

**中文解读：** 这是 `QAbstractTextDocumentLayout` 的 `Selection` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractTextDocumentLayout` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
