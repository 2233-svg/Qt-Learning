# QStackedWidget

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QStackedWidget` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QStackedWidget` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QStackedWidget>`
- 继承自：QFrame
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

**生命周期：** 容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

**状态与结果：** 要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

**线程与事件循环：** 不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

```cpp
#include <QList>

QList<int> values{1, 2, 3};
values.append(4);
for (const int value : values) {
    // 使用 value
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `count : int`
- `currentIndex : int`

### 公有函数

- `QStackedWidget(QWidget *parent = nullptr)`
- `virtual ~QStackedWidget()`
- `int addWidget(QWidget *widget)`
- `int count() const`
- `int currentIndex() const`
- `QWidget * currentWidget() const`
- `int indexOf(const QWidget *widget) const`
- `int insertWidget(int index, QWidget *widget)`
- `void removeWidget(QWidget *widget)`
- `QWidget * widget(int index) const`

### 公有槽函数

- `void setCurrentIndex(int index)`
- `void setCurrentWidget(QWidget *widget)`

### 信号

- `void currentChanged(int index)`
- `(since 6.9) void widgetAdded(int index)`
- `void widgetRemoved(int index)`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[read-only] count : int`

**作用与语义：**

该属性包含该堆叠控件所包含的控件数量。
默认情况下，该属性的值为0。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `currentIndex : int`

**作用与语义：**

该属性表示可见控件的索引位置。
如果没有当前控件，当前索引为-1。
默认情况下，该属性包含 -1 值，因为栈初始为空。

**如何使用：** 调用 `currentIndex()` 读取当前值；它不会修改应用状态。

### `[explicit] QStackedWidget::QStackedWidget(QWidget *parent = nullptr)`

**作用与语义：**

构造一个带有给定`parent`的QStackedWidget。

### `[virtual noexcept] QStackedWidget::~QStackedWidget()`

**作用与语义：**

摧毁这个堆叠小部件，释放所有分配的资源。

### `int QStackedWidget::addWidget(QWidget *widget)`

**作用与语义：**

将给定`widget`附加到`QStackedWidget`上，并返回指数位置。`widget`的所有权转移给`QStackedWidget`。
如果在调用该函数前`QStackedWidget`为空，`widget` 就成为当前的控件。

### `[signal] void QStackedWidget::currentChanged(int index)`

**作用与语义：**

该属性表示可见控件的索引位置。
如果没有当前控件，当前索引为-1。
默认情况下，该属性包含 -1 值，因为栈初始为空。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `currentIndex` 的变化，不要把它当作普通函数主动调用。

### `QWidget *QStackedWidget::currentWidget() const`

**作用与语义：**

返回当前控件，若无子控件则返回`nullptr`。

### `[override virtual protected] bool QStackedWidget::event(QEvent *e)`

**作用与语义：**

重实现自：`QFrame::event`（QEvent *e）。

### `int QStackedWidget::indexOf(const QWidget *widget) const`

**作用与语义：**

返回给定`widget`的索引，如果给定`widget`不是`QStackedWidget`的子节点，则返回-1。

### `int QStackedWidget::insertWidget(int index, QWidget *widget)`

**作用与语义：**

在`QStackedWidget`的指定`index`处插入给定的`widget`。`widget`的所有权传递给`QStackedWidget`。如果`index`超出范围，则附加`widget`（此时返回的是实际的`widget`索引）。
如果调用该函数前`QStackedWidget`为空，则该`widget`即为当前控件。
在索引大小于或等于当前索引处插入新控件，会递增当前索引，但保留当前控件。

### `void QStackedWidget::removeWidget(QWidget *widget)`

**作用与语义：**

将`widget`从`QStackedWidget`中移除。也就是说，`widget`不会被删除，而是直接从堆叠布局中移除，从而使其被隐藏。
注意：`widget`的父对象和父控件仍为`QStackedWidget`。如果应用程序想重用已移除的`widget`，建议重新父级。

### `[slot] void QStackedWidget::setCurrentWidget(QWidget *widget)`

**作用与语义：**

将当前控件设置为指定的`widget`。新的当前控件必须已经包含在这个堆叠控件中。

### `QWidget *QStackedWidget::widget(int index) const`

**作用与语义：**

在给定的`index`返回小部件，若无该小部件则返回`nullptr`。

### `[signal, since 6.9] void QStackedWidget::widgetAdded(int index)`

**作用与语义：**

每当添加或插入小部件时，该信号都会发出。小部件的`index`作为参数传递。

### `[signal] void QStackedWidget::widgetRemoved(int index)`

**作用与语义：**

每当小部件被移除时，该信号都会发出。小部件的 `index` 作为参数传递。

### `int count() const`

**作用与语义：**

该属性包含该堆叠控件所包含的控件数量。
默认情况下，该属性的值为0。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `int currentIndex() const`

**作用与语义：**

该属性表示可见控件的索引位置。
如果没有当前控件，当前索引为-1。
默认情况下，该属性包含 -1 值，因为栈初始为空。

**如何使用：** 调用 `currentIndex()` 读取当前值；它不会修改应用状态。

### `void setCurrentIndex(int index)`

**作用与语义：**

该属性表示可见控件的索引位置。
如果没有当前控件，当前索引为-1。
默认情况下，该属性包含 -1 值，因为栈初始为空。

**如何使用：** 调用 `setCurrentIndex(...)` 修改 `currentIndex`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

### 状态和错误边界

要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

### 线程边界

不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QStackedWidget` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
