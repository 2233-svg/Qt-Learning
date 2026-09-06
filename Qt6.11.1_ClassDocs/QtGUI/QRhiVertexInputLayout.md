# QRhiVertexInputLayout

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QRhiVertexInputLayout` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiVertexInputLayout` 是 Qt Widgets 界面机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

**适用场景：** 创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

## 2. 依赖与对象关系

- 头文件：`#include <rhi/qrhi.h>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS GuiPrivate)
target_link_libraries(mytarget PRIVATE Qt6::GuiPrivate)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QRhiVertexInputLayout()`
- `const QRhiVertexInputAttribute * attributeAt(qsizetype index) const`
- `qsizetype attributeCount() const`
- `const QRhiVertexInputBinding * bindingAt(qsizetype index) const`
- `qsizetype bindingCount() const`
- `const QRhiVertexInputAttribute * cbeginAttributes() const`
- `const QRhiVertexInputBinding * cbeginBindings() const`
- `const QRhiVertexInputAttribute * cendAttributes() const`
- `const QRhiVertexInputBinding * cendBindings() const`
- `void setAttributes(std::initializer_list<QRhiVertexInputAttribute> list)`
- `void setAttributes(InputIterator first, InputIterator last)`
- `void setBindings(std::initializer_list<QRhiVertexInputBinding> list)`
- `void setBindings(InputIterator first, InputIterator last)`

### 相关非成员函数

- `size_t qHash(const QRhiVertexInputLayout &key, size_t seed = 0)`
- `bool operator!=(const QRhiVertexInputLayout &a, const QRhiVertexInputLayout &b)`
- `bool operator==(const QRhiVertexInputLayout &a, const QRhiVertexInputLayout &b)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QRhiVertexInputLayout::QRhiVertexInputLayout()`

**作用与语义：**

构造一个空顶点输入布局描述。

### `const QRhiVertexInputAttribute *QRhiVertexInputLayout::attributeAt(qsizetype index) const`

**作用与语义：**

返回给定`index`的属性。

### `qsizetype QRhiVertexInputLayout::attributeCount() const`

**作用与语义：**

返回属性数量。

### `const QRhiVertexInputBinding *QRhiVertexInputLayout::bindingAt(qsizetype index) const`

**作用与语义：**

在给定的`index`归还绑定。

### `qsizetype QRhiVertexInputLayout::bindingCount() const`

**作用与语义：**

返回绑定数量。

### `const QRhiVertexInputAttribute *QRhiVertexInputLayout::cbeginAttributes() const`

**作用与语义：**

返回指向属性列表第一个项目的const迭代器。

### `const QRhiVertexInputBinding *QRhiVertexInputLayout::cbeginBindings() const`

**作用与语义：**

返回一个 const 迭代器，指向绑定列表中的第一个项。

### `const QRhiVertexInputAttribute *QRhiVertexInputLayout::cendAttributes() const`

**作用与语义：**

返回一个 const 迭代器，指向属性列表中最后一个项目之后。

### `const QRhiVertexInputBinding *QRhiVertexInputLayout::cendBindings() const`

**作用与语义：**

返回一个连接迭代器，指向绑定列表最后一项之后。

### `void QRhiVertexInputLayout::setAttributes(std::initializer_list<QRhiVertexInputAttribute> list)`

**作用与语义：**

设置指定`list`的属性。

### `template <typename InputIterator> void QRhiVertexInputLayout::setAttributes(InputIterator first, InputIterator last)`

**作用与语义：**

使用迭代器`first`和`last`来设置属性。

### `void QRhiVertexInputLayout::setBindings(std::initializer_list<QRhiVertexInputBinding> list)`

**作用与语义：**

设置指定`list`的绑定。

### `template <typename InputIterator> void QRhiVertexInputLayout::setBindings(InputIterator first, InputIterator last)`

**作用与语义：**

使用迭代器`first`和`last`来设置绑定。

### `[noexcept] size_t qHash(const QRhiVertexInputLayout &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] bool operator!=(const QRhiVertexInputLayout &a, const QRhiVertexInputLayout &b)`

**作用与语义：**

如果两个 `QRhiVertexInputLayout` 对象 `a` 和 `b` 中的值相等，则返回 `false`；否则返回 `true`。

### `[noexcept] bool operator==(const QRhiVertexInputLayout &a, const QRhiVertexInputLayout &b)`

**作用与语义：**

如果两个`QRhiVertexInputLayout`对象`a`和`b`的值相等，返回`true`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QRhiVertexInputLayout` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
