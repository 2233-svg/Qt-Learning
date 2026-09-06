# QLayoutItem

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QLayoutItem` 是 布局管理机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QLayoutItem` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QLayoutItem>`
- 继承自：未在类页中列出
- 直接派生类：QLayout、QSpacerItem,、QWidgetItem

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

**状态与结果：** 布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

**线程与事件循环：** 布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QLayoutItem(Qt::Alignment alignment = Qt::Alignment())`
- `virtual ~QLayoutItem()`
- `Qt::Alignment alignment() const`
- `virtual QSizePolicy::ControlTypes controlTypes() const`
- `virtual Qt::Orientations expandingDirections() const = 0`
- `virtual QRect geometry() const = 0`
- `virtual bool hasHeightForWidth() const`
- `virtual int heightForWidth(int) const`
- `virtual void invalidate()`
- `virtual bool isEmpty() const = 0`
- `virtual QLayout * layout()`
- `virtual QSize maximumSize() const = 0`
- `virtual int minimumHeightForWidth(int w) const`
- `virtual QSize minimumSize() const = 0`
- `void setAlignment(Qt::Alignment alignment)`
- `virtual void setGeometry(const QRect &r) = 0`
- `virtual QSize sizeHint() const = 0`
- `virtual QSpacerItem * spacerItem()`
- `virtual QWidget * widget() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QLayoutItem::QLayoutItem(Qt::Alignment alignment = Qt::Alignment())`

**作用与语义：**

构造一个带有`alignment`的布局物品。并非所有子职业都支持对齐。

### `[virtual noexcept] QLayoutItem::~QLayoutItem()`

**作用与语义：**

毁掉`QLayoutItem`。

### `Qt::Alignment QLayoutItem::alignment() const`

**作用与语义：**

返回该物品的对齐。

### `[virtual] QSizePolicy::ControlTypes QLayoutItem::controlTypes() const`

**作用与语义：**

返回布局项的控制类型。对于`QWidgetItem`，控制类型来源于控件的大小策略;对于`QLayoutItem`，控制类型来源于布局内容。

### `[pure virtual] Qt::Orientations QLayoutItem::expandingDirections() const`

**作用与语义：**

返回该布局项目是否能利用超过`sizeHint()`的空间。值为`Qt::Vertical`或`Qt::Horizontal`表示它只想在一个维度上增长，而`Qt::Vertical` |`Qt::Horizontal`表示它希望在两个维度上都增长。

### `[pure virtual] QRect QLayoutItem::geometry() const`

**作用与语义：**

返回该布局项目覆盖的矩形。

### `[virtual] bool QLayoutItem::hasHeightForWidth() const`

**作用与语义：**

如果该布局的首选高度取决于宽度，则返回`true`;否则返回`false`。默认实现返回false。
在支持宽度高度的布局管理器中重新实现这个功能。

### `[virtual] int QLayoutItem::heightForWidth(int) const`

**作用与语义：**

返回该布局项的首选高度，基于宽度，但默认实现中未使用宽度。
默认实现返回 -1，表示首选高度与物品宽度无关。使用函数 `hasHeightForWidth()` 通常比调用该函数并测试 -1 快得多。
在支持宽度高度的布局管理器中重新实现该函数。典型的实现如下：
强烈建议缓存;没有缓存，布局将耗费指数级时间。

**官方示例：**

```cpp
 int MyLayout::heightForWidth(int w) const
 {
     if (cache_dirty || cached_width != w) {
         MyLayout *that = const_cast<MyLayout *>(this);
         int h = calculateHeightForWidth(w);
         that->cached_hfw = h;
         return h;
     }
     return cached_hfw;
 }
```

### `[virtual] void QLayoutItem::invalidate()`

**作用与语义：**

使该布局项中缓存的信息失效。

### `[pure virtual] bool QLayoutItem::isEmpty() const`

**作用与语义：**

在子类中实现，返回该项是否为空，即是否包含任何控件。

### `[virtual] QLayout *QLayoutItem::layout()`

**作用与语义：**

如果该项是`QLayout`，则返回为`QLayout`;否则返回`nullptr`。该函数提供类型安全的铸造。

### `[pure virtual] QSize QLayoutItem::maximumSize() const`

**作用与语义：**

在子类中实现以返回该项的最大大小。

### `[virtual] int QLayoutItem::minimumHeightForWidth(int w) const`

**作用与语义：**

返回该控件在给定宽度下所需的最小高度，`w`。默认实现仅返回 `heightForWidth`（`w`）。

### `[pure virtual] QSize QLayoutItem::minimumSize() const`

**作用与语义：**

在子类中实现，以返回该项的最小大小。

### `void QLayoutItem::setAlignment(Qt::Alignment alignment)`

**作用与语义：**

将该项目的对齐设置为`alignment`。
注意：项目对齐仅在具有视觉效果的`QLayoutItem`子类中支持。除了`QSpacerItem`，它为布局提供空白空间外，所有继承`QLayoutItem`的公共Qt类都支持项目对齐。

### `[pure virtual] void QLayoutItem::setGeometry(const QRect &r)`

**作用与语义：**

在子职业中实现，将该物品的几何体设置为`r`。

### `[pure virtual] QSize QLayoutItem::sizeHint() const`

**作用与语义：**

在子类中实现，以返回该物品的首选大小。

### `[virtual] QSpacerItem *QLayoutItem::spacerItem()`

**作用与语义：**

如果该项是`QSpacerItem`，则返回为`QSpacerItem`;否则返回`nullptr`。该函数提供类型安全的铸造。

### `[virtual] QWidget *QLayoutItem::widget() const`

**作用与语义：**

如果该项管理`QWidget`，返回该控件。否则，返回`nullptr`。
注意：虽然函数`layout()`和`spacerItem()`执行cast，但该函数返回另一个对象：`QLayout`和`QSpacerItem`继承`QLayoutItem`，而`QWidget`不会。

## 6. 深入实践与常见坑

### 生命周期和资源边界

顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

### 状态和错误边界

布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

### 线程边界

布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QLayoutItem` 所属机制类型：布局管理机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
