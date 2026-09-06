# QTreeWidgetItemIterator

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QTreeWidgetItemIterator` 是容器或范围的迭代器类型，用于按约定遍历元素；重点是有效期、可写性和失效规则。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QTreeWidgetItemIterator` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QTreeWidgetItemIterator>`
- 继承自：未在类页中列出
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

**生命周期：** 迭代器依赖底层容器、目录枚举或视图对象存活；容器修改、隐式共享 detach 或目录资源关闭可能使迭代器失效。sentinel 只用于比较结束，不能解引用。

**状态与结果：** 有效迭代器、尾后迭代器和失效迭代器是不同状态。每次递增前要保证尚未到 end；删除当前元素时使用类提供的 erase/remove 规则，不要继续使用被删除位置。

**线程与事件循环：** 迭代器不提供跨线程同步；后台遍历应拥有稳定的数据快照或独占容器，结果再通过消息传回。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

```cpp
for (auto it = container.cbegin(); it != container.cend(); ++it) {
    // 读取 *it，不要在遍历期间让 container 发生会使迭代器失效的修改
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum IteratorFlag { All, Hidden, NotHidden, Selected, Unselected, …, UserFlag }`
- `flags IteratorFlags`

### 公有函数

- `QTreeWidgetItemIterator(QTreeWidget *widget, QTreeWidgetItemIterator::IteratorFlags flags = All)`
- `QTreeWidgetItemIterator(QTreeWidgetItem *item, QTreeWidgetItemIterator::IteratorFlags flags = All)`
- `QTreeWidgetItemIterator(const QTreeWidgetItemIterator &it)`
- `~QTreeWidgetItemIterator()`
- `QTreeWidgetItem * operator*() const`
- `QTreeWidgetItemIterator & operator++()`
- `const QTreeWidgetItemIterator operator++(int)`
- `QTreeWidgetItemIterator & operator+=(int n)`
- `QTreeWidgetItemIterator & operator--()`
- `const QTreeWidgetItemIterator operator--(int)`
- `QTreeWidgetItemIterator & operator-=(int n)`
- `QTreeWidgetItemIterator & operator=(const QTreeWidgetItemIterator &it)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QTreeWidgetItemIterator::IteratorFlagflags QTreeWidgetItemIterator::IteratorFlags`

**作用与语义：**

这些标志可以传递给 `QTreeWidgetItemIterator` 构造函数（如果使用多个标志，可以进行按位或运算），这样迭代器将只迭代与给定标志匹配的项目。
- `QTreeWidgetItemIterator::All`: `0x00000000`
- `QTreeWidgetItemIterator::Hidden`: `0x00000001`
- `QTreeWidgetItemIterator::NotHidden`: `0x00000002`
- `QTreeWidgetItemIterator::Selected`: `0x00000004`
- `QTreeWidgetItemIterator::Unselected`: `0x00000008`
- `QTreeWidgetItemIterator::Selectable`: `0x00000010`
- `QTreeWidgetItemIterator::NotSelectable`: `0x00000020`
- `QTreeWidgetItemIterator::DragEnabled`: `0x00000040`
- `QTreeWidgetItemIterator::DragDisabled`: `0x00000080`
- `QTreeWidgetItemIterator::DropEnabled`: `0x00000100`
- `QTreeWidgetItemIterator::DropDisabled`: `0x00000200`
- `QTreeWidgetItemIterator::HasChildren`: `0x00000400`
- `QTreeWidgetItemIterator::NoChildren`: `0x00000800`
- `QTreeWidgetItemIterator::Checked`: `0x00001000`
- `QTreeWidgetItemIterator::NotChecked`: `0x00002000`
- `QTreeWidgetItemIterator::Enabled`: `0x00004000`
- `QTreeWidgetItemIterator::Disabled`: `0x00008000`
- `QTreeWidgetItemIterator::Editable`: `0x00010000`
- `QTreeWidgetItemIterator::NotEditable`: `0x00020000`
- `QTreeWidgetItemIterator::UserFlag`: `0x01000000`
IteratorFlags 类型是 QFlags<IteratorFlag> 的 typedef。它存储 IteratorFlag 值的按位或组合。

### `[explicit] QTreeWidgetItemIterator::QTreeWidgetItemIterator(QTreeWidget *widget, QTreeWidgetItemIterator::IteratorFlags flags = All)`

**作用与语义：**

为给定`widget`构建一个迭代器，利用指定`flags`确定迭代过程中找到的物品。迭代器设置为指向控件中包含的第一个顶层项目，或者如果顶层项目与标志不匹配，则指向下一个匹配的项目。

### `[explicit] QTreeWidgetItemIterator::QTreeWidgetItemIterator(QTreeWidgetItem *item, QTreeWidgetItemIterator::IteratorFlags flags = All)`

**作用与语义：**

为给定`item`构建一个迭代器，利用指定`flags`确定迭代过程中发现哪些项目。迭代器指向`item`，或如果`item`与标志不匹配，则指向下一个匹配的项目。

### `QTreeWidgetItemIterator::QTreeWidgetItemIterator(const QTreeWidgetItemIterator &it)`

**作用与语义：**

构造与`it`相同的`QTreeWidget`迭代器。当前迭代项设置为指向当前`it`项。

### `[noexcept] QTreeWidgetItemIterator::~QTreeWidgetItemIterator()`

**作用与语义：**

摧毁迭代器。

### `QTreeWidgetItem *QTreeWidgetItemIterator::operator*() const`

**作用与语义：**

Dereference 操作符。返回当前项目的指针。

### `QTreeWidgetItemIterator &QTreeWidgetItemIterator::operator++()`

**作用与语义：**

前缀 `++` 运算符（`++it`）将迭代器推进到下一个匹配的项，并返回对结果迭代器的引用。如果当前项是最后一个匹配的项，则将当前指针设置为 `nullptr`。

### `const QTreeWidgetItemIterator QTreeWidgetItemIterator::operator++(int)`

**作用与语义：**

后缀操作符（it ）将迭代器推进到下一个匹配的项，并返回一个迭代器到之前当前的项。

### `QTreeWidgetItemIterator &QTreeWidgetItemIterator::operator+=(int n)`

**作用与语义：**

使迭代器通过`n`匹配的项向前移动。（如果n为负，迭代器向后移动。）。
如果当前项超过上一个项，当前项指针设为`nullptr`。返回结果迭代器。

### `QTreeWidgetItemIterator &QTreeWidgetItemIterator::operator--()`

**作用与语义：**

前缀`--`操作符（`--it`）将迭代器推进到上一个匹配的项，并返回对结果迭代器的引用。如果当前条目是第一个匹配的项，则将当前指针设置为`nullptr`。

### `const QTreeWidgetItemIterator QTreeWidgetItemIterator::operator--(int)`

**作用与语义：**

后缀 – 操作符（it–）使前一个匹配的项目为当前，并返回之前当前的项目的迭代器。

### `QTreeWidgetItemIterator &QTreeWidgetItemIterator::operator-=(int n)`

**作用与语义：**

使迭代者通过`n`匹配的项向后移动。（如果n为负，迭代器向前移动。）。
如果当前项比上一个项更前面，则当前项指针设置为`nullptr`。返回结果迭代器。

### `QTreeWidgetItemIterator &QTreeWidgetItemIterator::operator=(const QTreeWidgetItemIterator &it)`

**作用与语义：**

赋值。复制`it`并返回其迭代器的引用。

### `enum IteratorFlag { All, Hidden, NotHidden, Selected, Unselected, …, UserFlag }`

**作用与语义：**

这些标志可以传递给 `QTreeWidgetItemIterator` 构造函数（如果使用多个标志，可以进行按位或运算），这样迭代器将只迭代与给定标志匹配的项目。
- `QTreeWidgetItemIterator::All`: `0x00000000`
- `QTreeWidgetItemIterator::Hidden`: `0x00000001`
- `QTreeWidgetItemIterator::NotHidden`: `0x00000002`
- `QTreeWidgetItemIterator::Selected`: `0x00000004`
- `QTreeWidgetItemIterator::Unselected`: `0x00000008`
- `QTreeWidgetItemIterator::Selectable`: `0x00000010`
- `QTreeWidgetItemIterator::NotSelectable`: `0x00000020`
- `QTreeWidgetItemIterator::DragEnabled`: `0x00000040`
- `QTreeWidgetItemIterator::DragDisabled`: `0x00000080`
- `QTreeWidgetItemIterator::DropEnabled`: `0x00000100`
- `QTreeWidgetItemIterator::DropDisabled`: `0x00000200`
- `QTreeWidgetItemIterator::HasChildren`: `0x00000400`
- `QTreeWidgetItemIterator::NoChildren`: `0x00000800`
- `QTreeWidgetItemIterator::Checked`: `0x00001000`
- `QTreeWidgetItemIterator::NotChecked`: `0x00002000`
- `QTreeWidgetItemIterator::Enabled`: `0x00004000`
- `QTreeWidgetItemIterator::Disabled`: `0x00008000`
- `QTreeWidgetItemIterator::Editable`: `0x00010000`
- `QTreeWidgetItemIterator::NotEditable`: `0x00020000`
- `QTreeWidgetItemIterator::UserFlag`: `0x01000000`
IteratorFlags 类型是 QFlags<IteratorFlag> 的 typedef。它存储 IteratorFlag 值的按位或组合。

### `flags IteratorFlags`

**作用与语义：**

这些标志可以传递给 `QTreeWidgetItemIterator` 构造函数（如果使用多个标志，可以进行按位或运算），这样迭代器将只迭代与给定标志匹配的项目。
- `QTreeWidgetItemIterator::All`: `0x00000000`
- `QTreeWidgetItemIterator::Hidden`: `0x00000001`
- `QTreeWidgetItemIterator::NotHidden`: `0x00000002`
- `QTreeWidgetItemIterator::Selected`: `0x00000004`
- `QTreeWidgetItemIterator::Unselected`: `0x00000008`
- `QTreeWidgetItemIterator::Selectable`: `0x00000010`
- `QTreeWidgetItemIterator::NotSelectable`: `0x00000020`
- `QTreeWidgetItemIterator::DragEnabled`: `0x00000040`
- `QTreeWidgetItemIterator::DragDisabled`: `0x00000080`
- `QTreeWidgetItemIterator::DropEnabled`: `0x00000100`
- `QTreeWidgetItemIterator::DropDisabled`: `0x00000200`
- `QTreeWidgetItemIterator::HasChildren`: `0x00000400`
- `QTreeWidgetItemIterator::NoChildren`: `0x00000800`
- `QTreeWidgetItemIterator::Checked`: `0x00001000`
- `QTreeWidgetItemIterator::NotChecked`: `0x00002000`
- `QTreeWidgetItemIterator::Enabled`: `0x00004000`
- `QTreeWidgetItemIterator::Disabled`: `0x00008000`
- `QTreeWidgetItemIterator::Editable`: `0x00010000`
- `QTreeWidgetItemIterator::NotEditable`: `0x00020000`
- `QTreeWidgetItemIterator::UserFlag`: `0x01000000`
IteratorFlags 类型是 QFlags<IteratorFlag> 的 typedef。它存储 IteratorFlag 值的按位或组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

迭代器依赖底层容器、目录枚举或视图对象存活；容器修改、隐式共享 detach 或目录资源关闭可能使迭代器失效。sentinel 只用于比较结束，不能解引用。

### 状态和错误边界

有效迭代器、尾后迭代器和失效迭代器是不同状态。每次递增前要保证尚未到 end；删除当前元素时使用类提供的 erase/remove 规则，不要继续使用被删除位置。

### 线程边界

迭代器不提供跨线程同步；后台遍历应拥有稳定的数据快照或独占容器，结果再通过消息传回。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QTreeWidgetItemIterator` 所属机制类型：迭代器与范围机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
