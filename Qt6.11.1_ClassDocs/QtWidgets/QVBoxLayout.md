# QVBoxLayout

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QVBoxLayout` 是从上到下排列控件和子布局的垂直布局。它继承 `QBoxLayout`，因此可以用 stretch 分配高度，用 margins/spacing 控制间距，用嵌套布局组织复杂页面。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QVBoxLayout` 是从上到下排列控件和子布局的垂直布局。它继承 `QBoxLayout`，因此可以用 stretch 分配高度，用 margins/spacing 控制间距，用嵌套布局组织复杂页面。

**内部模型：** 它沿垂直方向分配高度，水平方向通常由控件的 sizePolicy 和 alignment 决定。想让编辑区填满窗口高度，给编辑区或包含它的子布局一个正的 stretch。

**适用场景：** 设置页、表单纵向堆叠、主窗口内容区、上下分区和对话框内容使用。需要同一行放置多个控件时，在垂直布局中嵌套 `QHBoxLayout`。

**典型调用链：** 创建 `QVBoxLayout` -> 依次加入控件/水平子布局 -> 给会伸展的内容设置 stretch -> 设置 margins/spacing -> 窗口变化时由 Qt 自动调整高度。

**先记住的坑：** stretch 只分配高度；只给顶层布局设置 stretch 不会自动让孙控件获得高度，通常要给直接的子布局设置 stretch；不要用固定高度模拟响应式页面。

## 2. 依赖与对象关系

- 头文件：`#include <QVBoxLayout>`
- 继承自：QBoxLayout
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

它沿垂直方向分配高度，水平方向通常由控件的 sizePolicy 和 alignment 决定。想让编辑区填满窗口高度，给编辑区或包含它的子布局一个正的 stretch。

### 状态、生命周期和线程

**生命周期：** 顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

**状态与结果：** 布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

**线程与事件循环：** 布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

## 3. 直接使用

`QVBoxLayout` 的项目顺序就是从上到下的视觉顺序。一个常见页面会把标题、主体和按钮区放成三个项目，并只让主体吸收多余高度：

```cpp
auto *layout = new QVBoxLayout(parentWidget);
layout->addWidget(titleLabel, 0);
layout->addWidget(editor, 1);
layout->addWidget(buttonBar, 0);
```

如果按钮栏本身是多个按钮横向排列，应把它做成 `QHBoxLayout` 后用 `addLayout(buttonBar, 0)` 加入垂直布局。`QVBoxLayout` 仍然遵守 `QBoxLayout` 的所有 stretch、alignment、spacing 和 margins 规则。

```cpp
auto *layout = new QVBoxLayout(parentWidget);
layout->addWidget(titleLabel);
layout->addWidget(editor, 1);
layout->addWidget(buttonBar);
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QVBoxLayout()`
- `QVBoxLayout(QWidget *parent)`
- `virtual ~QVBoxLayout()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QVBoxLayout::QVBoxLayout()`

**作用与语义：**

构建一个新的垂直方框。你必须将其添加到另一个布局中。

### `[explicit] QVBoxLayout::QVBoxLayout(QWidget *parent)`

**作用与语义：**

构建一个带有父`parent`的顶层垂直框。
布局直接设置为`parent`的顶层布局。一个小部件只能有一个顶层布局。它由`QWidget::layout()`返回。

### `[virtual noexcept] QVBoxLayout::~QVBoxLayout()`

**作用与语义：**

破坏了这个盒子布局。
布局中的控件没有被破坏。

## 6. 深入实践与常见坑

### 生命周期和资源边界

顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

### 状态和错误边界

布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

### 线程边界

布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

### 最容易出现的错误

stretch 只分配高度；只给顶层布局设置 stretch 不会自动让孙控件获得高度，通常要给直接的子布局设置 stretch；不要用固定高度模拟响应式页面。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QVBoxLayout` 所属机制类型：布局管理机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
