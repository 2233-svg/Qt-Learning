# QHBoxLayout

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QHBoxLayout` 是从左到右排列控件和子布局的水平布局。它继承 `QBoxLayout`，因此 margins、spacing、stretch、alignment、插入/移除项目等规则全部适用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QHBoxLayout` 是从左到右排列控件和子布局的水平布局。它继承 `QBoxLayout`，因此 margins、spacing、stretch、alignment、插入/移除项目等规则全部适用。

**内部模型：** 它沿水平方向分配宽度，垂直方向主要由控件的 sizeHint、sizePolicy 和 alignment 决定。想让某个控件变宽，给它正的 stretch；想让按钮靠右，在按钮前放 `addStretch(1)`。

**适用场景：** 按钮行、工具栏、标签加输入框、左右分栏和一行状态信息使用。需要垂直排列时用 `QVBoxLayout`，需要运行时切换方向时用 `QBoxLayout`。

**典型调用链：** 创建 `QHBoxLayout` -> 设置 margins/spacing -> addWidget 或 addLayout -> 用 stretch 分配宽度 -> 用 alignment 控制项目在单元格中的位置。

**先记住的坑：** stretch 只分配宽度；没有正 stretch 时输入框是否变宽还取决于 sizePolicy；项目太多时不要用大量固定 spacing 代替布局层次。

## 2. 依赖与对象关系

- 头文件：`#include <QHBoxLayout>`
- 继承自：QBoxLayout
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

它沿水平方向分配宽度，垂直方向主要由控件的 sizeHint、sizePolicy 和 alignment 决定。想让某个控件变宽，给它正的 stretch；想让按钮靠右，在按钮前放 `addStretch(1)`。

### 状态、生命周期和线程

**生命周期：** 顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

**状态与结果：** 布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

**线程与事件循环：** 布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

## 3. 直接使用

`QHBoxLayout` 不需要传方向，构造后就是从左到右。下面的 `1:3` 是左右项目争取剩余宽度的比例；它们仍然会受到最小和最大尺寸限制。

```cpp
auto *layout = new QHBoxLayout(parentWidget);
layout->setContentsMargins(12, 8, 12, 8);
layout->setSpacing(6);
layout->addWidget(sidebar, 1);
layout->addWidget(mainPanel, 3);
```

右对齐命令按钮时，通常让 stretch 占据按钮前面的空间：

```cpp
layout->addStretch(1);
layout->addWidget(okButton);
```

所有具体的 stretch、spacing、alignment 和 size constraint 规则都由 `QBoxLayout` 提供。

```cpp
auto *layout = new QHBoxLayout(parentWidget);
layout->addWidget(leftWidget, 1);
layout->addWidget(rightWidget, 3);
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QHBoxLayout()`
- `QHBoxLayout(QWidget *parent)`
- `virtual ~QHBoxLayout()`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 3 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QHBoxLayout::QHBoxLayout()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QHBoxLayout` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QHBoxLayout::QHBoxLayout(QWidget *parent)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QHBoxLayout` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QWidget *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QHBoxLayout::~QHBoxLayout()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QHBoxLayout` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

### 状态和错误边界

布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

### 线程边界

布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

### 最容易出现的错误

stretch 只分配宽度；没有正 stretch 时输入框是否变宽还取决于 sizePolicy；项目太多时不要用大量固定 spacing 代替布局层次。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QHBoxLayout` 所属机制类型：布局管理机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
