# QGraphicsProxyWidget

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsProxyWidget` 是 图形场景与项目机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsProxyWidget` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsProxyWidget>`
- 继承自：QGraphicsWidget
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 场景或父项目通常管理子项目，但视图只是观察者，不一定拥有场景。删除项目、改变父项目或切换场景时要确认索引、指针、选中状态和布局关系是否仍有效。

**状态与结果：** 区分局部坐标、场景坐标、视图/窗口坐标，区分选中、悬停、焦点、可见和碰撞状态。改变几何、变换或数据后通常请求更新，而不是手动强制调用绘制函数。

**线程与事件循环：** 图形对象通常只能在其所属 GUI/场景线程操作；后台线程负责数据准备，结果通过信号投递后再更新场景对象。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum { Type }`

### 公有函数

- `QGraphicsProxyWidget(QGraphicsItem *parent = nullptr, Qt::WindowFlags wFlags = Qt::WindowFlags())`
- `virtual ~QGraphicsProxyWidget()`
- `QGraphicsProxyWidget * createProxyForChildWidget(QWidget *child)`
- `void setWidget(QWidget *widget)`
- `QRectF subWidgetRect(const QWidget *widget) const`
- `QWidget * widget() const`

### 重实现的公有函数

- `virtual void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget) override`
- `virtual void setGeometry(const QRectF &rect) override`
- `virtual int type() const override`

### 重实现的保护函数

- `virtual void contextMenuEvent(QGraphicsSceneContextMenuEvent *event) override`
- `virtual void dragEnterEvent(QGraphicsSceneDragDropEvent *event) override`
- `virtual void dragLeaveEvent(QGraphicsSceneDragDropEvent *event) override`
- `virtual void dragMoveEvent(QGraphicsSceneDragDropEvent *event) override`
- `virtual void dropEvent(QGraphicsSceneDragDropEvent *event) override`
- `virtual bool event(QEvent *event) override`
- `virtual bool eventFilter(QObject *object, QEvent *event) override`
- `virtual void focusInEvent(QFocusEvent *event) override`
- `virtual bool focusNextPrevChild(bool next) override`
- `virtual void focusOutEvent(QFocusEvent *event) override`
- `virtual void grabMouseEvent(QEvent *event) override`
- `virtual void hideEvent(QHideEvent *event) override`
- `virtual void hoverEnterEvent(QGraphicsSceneHoverEvent *event) override`
- `virtual void hoverLeaveEvent(QGraphicsSceneHoverEvent *event) override`
- `virtual void hoverMoveEvent(QGraphicsSceneHoverEvent *event) override`
- `virtual void inputMethodEvent(QInputMethodEvent *event) override`
- `virtual QVariant inputMethodQuery(Qt::InputMethodQuery query) const override`
- `virtual QVariant itemChange(QGraphicsItem::GraphicsItemChange change, const QVariant &value) override`
- `virtual void keyPressEvent(QKeyEvent *event) override`
- `virtual void keyReleaseEvent(QKeyEvent *event) override`
- `virtual void mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event) override`
- `virtual void mouseMoveEvent(QGraphicsSceneMouseEvent *event) override`
- `virtual void mousePressEvent(QGraphicsSceneMouseEvent *event) override`
- `virtual void mouseReleaseEvent(QGraphicsSceneMouseEvent *event) override`
- `virtual void resizeEvent(QGraphicsSceneResizeEvent *event) override`
- `virtual void showEvent(QShowEvent *event) override`
- `virtual QSizeF sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const override`
- `virtual void ungrabMouseEvent(QEvent *event) override`
- `virtual void wheelEvent(QGraphicsSceneWheelEvent *event) override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 41 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[anonymous] enum`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QGraphicsProxyWidget` 暴露的类型声明 `enum`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsProxyWidget::QGraphicsProxyWidget(QGraphicsItem *parent = nullptr, Qt::WindowFlags wFlags = Qt::WindowFlags())`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsProxyWidget` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QGraphicsItem *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `wFlags`：类型为 `Qt::WindowFlags`。默认值为 `Qt::WindowFlags()`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QGraphicsProxyWidget::~QGraphicsProxyWidget()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsProxyWidget` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::contextMenuEvent(QGraphicsSceneContextMenuEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::contextMenuEvent` 用于执行与“context、Menu、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneContextMenuEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsProxyWidget *QGraphicsProxyWidget::createProxyForChildWidget(QWidget *child)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::createProxyForChildWidget` 用于计算、查询或取得与“创建、Proxy、For、Child、Widget”相关的操作。调用时要先确认当前状态和 `child` 的有效范围；返回类型是 `QGraphicsProxyWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QGraphicsProxyWidget *`。
- 参数 `child`：类型为 `QWidget *`。没有默认值，调用时必须提供。子对象或子节点；要确认它是否由父对象接管，以及调用后原指针是否仍有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::dragEnterEvent(QGraphicsSceneDragDropEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::dragEnterEvent` 用于执行与“drag、Enter、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneDragDropEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::dragLeaveEvent(QGraphicsSceneDragDropEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::dragLeaveEvent` 用于执行与“drag、Leave、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneDragDropEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::dragMoveEvent(QGraphicsSceneDragDropEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::dragMoveEvent` 用于执行与“drag、移动、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneDragDropEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::dropEvent(QGraphicsSceneDragDropEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::dropEvent` 用于执行与“drop、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneDragDropEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QGraphicsProxyWidget::event(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QGraphicsProxyWidget::eventFilter(QObject *object, QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::eventFilter` 用于计算、查询或取得与“event、Filter”相关的操作。调用时要先确认当前状态和 `object`、`event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `object`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::focusInEvent(QFocusEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::focusInEvent` 用于执行与“focus、In、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QFocusEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QGraphicsProxyWidget::focusNextPrevChild(bool next)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::focusNextPrevChild` 用于计算、查询或取得与“focus、移动到下一项、Prev、Child”相关的操作。调用时要先确认当前状态和 `next` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `next`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::focusOutEvent(QFocusEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::focusOutEvent` 用于执行与“focus、Out、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QFocusEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::grabMouseEvent(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::grabMouseEvent` 用于执行与“抓取、Mouse、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::hideEvent(QHideEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::hideEvent` 用于执行与“隐藏、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QHideEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::hoverEnterEvent(QGraphicsSceneHoverEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::hoverEnterEvent` 用于执行与“hover、Enter、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneHoverEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::hoverLeaveEvent(QGraphicsSceneHoverEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::hoverLeaveEvent` 用于执行与“hover、Leave、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneHoverEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::hoverMoveEvent(QGraphicsSceneHoverEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::hoverMoveEvent` 用于执行与“hover、移动、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneHoverEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::inputMethodEvent(QInputMethodEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::inputMethodEvent` 用于执行与“input、Method、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QInputMethodEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] QVariant QGraphicsProxyWidget::inputMethodQuery(Qt::InputMethodQuery query) const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::inputMethodQuery` 用于计算、查询或取得与“input、Method、查询”相关的操作。调用时要先确认当前状态和 `query` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `query`：类型为 `Qt::InputMethodQuery`。没有默认值，调用时必须提供。传入 `Qt::InputMethodQuery` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] QVariant QGraphicsProxyWidget::itemChange(QGraphicsItem::GraphicsItemChange change, const QVariant &value)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::itemChange` 用于计算、查询或取得与“项目访问、Change”相关的操作。调用时要先确认当前状态和 `change`、`value` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `change`：类型为 `QGraphicsItem::GraphicsItemChange`。没有默认值，调用时必须提供。传入 `QGraphicsItem::GraphicsItemChange` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::keyPressEvent(QKeyEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::keyPressEvent` 用于执行与“key、Press、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::keyReleaseEvent(QKeyEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::keyReleaseEvent` 用于执行与“key、释放、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::mouseDoubleClickEvent` 用于执行与“mouse、Double、Click、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::mouseMoveEvent(QGraphicsSceneMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::mouseMoveEvent` 用于执行与“mouse、移动、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::mousePressEvent(QGraphicsSceneMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::mousePressEvent` 用于执行与“mouse、Press、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::mouseReleaseEvent(QGraphicsSceneMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::mouseReleaseEvent` 用于执行与“mouse、释放、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected slot] QGraphicsProxyWidget *QGraphicsProxyWidget::newProxyWidget(const QWidget *child)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::newProxyWidget` 用于计算、查询或取得与“new、Proxy、Widget”相关的操作。调用时要先确认当前状态和 `child` 的有效范围；返回类型是 `QGraphicsProxyWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QGraphicsProxyWidget *`。
- 参数 `child`：类型为 `const QWidget *`。没有默认值，调用时必须提供。子对象或子节点；要确认它是否由父对象接管，以及调用后原指针是否仍有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QGraphicsProxyWidget::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsProxyWidget` 的核心操作 `paint`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。
- 参数 `option`：类型为 `const QStyleOptionGraphicsItem *`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::resizeEvent(QGraphicsSceneResizeEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::resizeEvent` 用于执行与“调整尺寸、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneResizeEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QGraphicsProxyWidget::setGeometry(const QRectF &rect)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setGeometry`。调用它会改变 `QGraphicsProxyWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsProxyWidget::setWidget(QWidget *widget)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setWidget`。调用它会改变 `QGraphicsProxyWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::showEvent(QShowEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::showEvent` 用于执行与“显示、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QShowEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] QSizeF QGraphicsProxyWidget::sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::sizeHint` 用于计算、查询或取得与“尺寸或数量、Hint”相关的操作。调用时要先确认当前状态和 `which`、`constraint` 的有效范围；返回类型是 `QSizeF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSizeF`。
- 参数 `which`：类型为 `Qt::SizeHint`。没有默认值，调用时必须提供。传入 `Qt::SizeHint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `constraint`：类型为 `const QSizeF &`。默认值为 `QSizeF()`。传入 `const QSizeF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QGraphicsProxyWidget::subWidgetRect(const QWidget *widget) const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::subWidgetRect` 用于计算、查询或取得与“sub、Widget、Rect”相关的操作。调用时要先确认当前状态和 `widget` 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `widget`：类型为 `const QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] int QGraphicsProxyWidget::type() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::type` 用于计算、查询或取得与“类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::ungrabMouseEvent(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::ungrabMouseEvent` 用于执行与“ungrab、Mouse、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QGraphicsProxyWidget::wheelEvent(QGraphicsSceneWheelEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::wheelEvent` 用于执行与“wheel、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneWheelEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QGraphicsProxyWidget::widget() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsProxyWidget::widget` 用于计算、查询或取得与“widget”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum { Type }`

**API 类别：** 公有类型

**中文解读：** 这是 `QGraphicsProxyWidget` 暴露的类型声明 `enum`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

场景或父项目通常管理子项目，但视图只是观察者，不一定拥有场景。删除项目、改变父项目或切换场景时要确认索引、指针、选中状态和布局关系是否仍有效。

### 状态和错误边界

区分局部坐标、场景坐标、视图/窗口坐标，区分选中、悬停、焦点、可见和碰撞状态。改变几何、变换或数据后通常请求更新，而不是手动强制调用绘制函数。

### 线程边界

图形对象通常只能在其所属 GUI/场景线程操作；后台线程负责数据准备，结果通过信号投递后再更新场景对象。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QGraphicsProxyWidget` 所属机制类型：图形场景与项目机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
