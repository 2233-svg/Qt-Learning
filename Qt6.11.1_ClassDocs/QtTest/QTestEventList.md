# QTestEventList

> Qt 6.11.1 · Qt Test

## 1. 先建立直觉

**一句话定位：** 这是 Qt Test 中围绕“Test事件列表”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Test 提供单元测试、数据驱动测试、基准测试和 GUI 测试支持。

### 这是什么

`QTestEventList` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QTestEventList>`
- 继承自：QList
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Test)
target_link_libraries(mytarget PRIVATE Qt6::Test)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QTestEventList()`
- `QTestEventList(const QTestEventList &other)`
- `~QTestEventList()`
- `void addDelay(int msecs)`
- `void addKeyClick(Qt::Key qtKey, Qt::KeyboardModifiers modifiers = Qt::NoModifier, int msecs = -1)`
- `void addKeyClick(char ascii, Qt::KeyboardModifiers modifiers = Qt::NoModifier, int msecs = -1)`
- `void addKeyClicks(const QString &keys, Qt::KeyboardModifiers modifiers = Qt::NoModifier, int msecs = -1)`
- `void addKeyPress(Qt::Key qtKey, Qt::KeyboardModifiers modifiers = Qt::NoModifier, int msecs = -1)`
- `void addKeyPress(char ascii, Qt::KeyboardModifiers modifiers = Qt::NoModifier, int msecs = -1)`
- `void addKeyRelease(Qt::Key qtKey, Qt::KeyboardModifiers modifiers = Qt::NoModifier, int msecs = -1)`
- `void addKeyRelease(char ascii, Qt::KeyboardModifiers modifiers = Qt::NoModifier, int msecs = -1)`
- `void addMouseClick(Qt::MouseButton button, Qt::KeyboardModifiers modifiers = Qt::KeyboardModifiers(), QPoint pos = QPoint(), int delay = -1)`
- `void addMouseDClick(Qt::MouseButton button, Qt::KeyboardModifiers modifiers = Qt::KeyboardModifiers(), QPoint pos = QPoint(), int delay = -1)`
- `void addMouseMove(QPoint pos = QPoint(), int delay = -1)`
- `void addMousePress(Qt::MouseButton button, Qt::KeyboardModifiers modifiers = Qt::KeyboardModifiers(), QPoint pos = QPoint(), int delay = -1)`
- `void addMouseRelease(Qt::MouseButton button, Qt::KeyboardModifiers modifiers = Qt::KeyboardModifiers(), QPoint pos = QPoint(), int delay = -1)`
- `void clear()`
- `void simulate(QWidget *w)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QTestEventList::QTestEventList()`

**作用与语义：**

构造一个空的 QTestEventList。

### `QTestEventList::QTestEventList(const QTestEventList &other)`

**作用与语义：**

构建一个新的QTestEventList，作为`other`的副本。

### `[noexcept] QTestEventList::~QTestEventList()`

**作用与语义：**

清空列表并销毁所有存储事件。

### `void QTestEventList::addDelay(int msecs)`

**作用与语义：**

增加了`msecs`毫秒的延迟。

### `void QTestEventList::addKeyClick(Qt::Key qtKey, Qt::KeyboardModifiers modifiers = Qt::NoModifier, int msecs = -1)`

**作用与语义：**

在列表中添加一个新的按键点击。事件会用修饰符`modifiers`模拟按键`qtKey`，然后等待`msecs`毫秒。

### `void QTestEventList::addKeyClick(char ascii, Qt::KeyboardModifiers modifiers = Qt::NoModifier, int msecs = -1)`

**作用与语义：**

在列表中添加一个新的按键点击。事件会用修饰符`modifiers`模拟按键`ascii`，然后等待`msecs`毫秒。

### `void QTestEventList::addKeyClicks(const QString &keys, Qt::KeyboardModifiers modifiers = Qt::NoModifier, int msecs = -1)`

**作用与语义：**

在列表中添加新的键盘条目。事件会按下带有`modifiers`的`keys`，并在每个按键之间等待`msecs`毫秒。

### `void QTestEventList::addKeyPress(Qt::Key qtKey, Qt::KeyboardModifiers modifiers = Qt::NoModifier, int msecs = -1)`

**作用与语义：**

在列表中添加一个新的按键按键。事件会按按键`qtKey`并`modifiers`修饰键，然后等待`msecs`毫秒。

### `void QTestEventList::addKeyPress(char ascii, Qt::KeyboardModifiers modifiers = Qt::NoModifier, int msecs = -1)`

**作用与语义：**

在列表中添加一个新的按键。事件会用修饰符`modifiers`按键`ascii`，然后等待`msecs`毫秒。

### `void QTestEventList::addKeyRelease(Qt::Key qtKey, Qt::KeyboardModifiers modifiers = Qt::NoModifier, int msecs = -1)`

**作用与语义：**

在列表中添加一个新的密钥释放。事件会释放带有修饰符`modifiers`的密钥`qtKey`，然后等待`msecs`毫秒。

### `void QTestEventList::addKeyRelease(char ascii, Qt::KeyboardModifiers modifiers = Qt::NoModifier, int msecs = -1)`

**作用与语义：**

会在列表中添加一个新的密钥释放。事件会释放带有修饰符`modifiers`的密钥`ascii`，然后等待`msecs`毫秒。

### `void QTestEventList::addMouseClick(Qt::MouseButton button, Qt::KeyboardModifiers modifiers = Qt::KeyboardModifiers(), QPoint pos = QPoint(), int delay = -1)`

**作用与语义：**

在列表中添加鼠标点击。事件会点击带有可选`modifiers`的位置`button` `pos`带有可选`delay`的位置。默认位置是小部件的中心。

### `void QTestEventList::addMouseDClick(Qt::MouseButton button, Qt::KeyboardModifiers modifiers = Qt::KeyboardModifiers(), QPoint pos = QPoint(), int delay = -1)`

**作用与语义：**

在列表中添加双击鼠标。事件会双击`button`，并选择在位置`pos` `modifiers`，并带有可选`delay`。默认位置是小部件的中心。

### `void QTestEventList::addMouseMove(QPoint pos = QPoint(), int delay = -1)`

**作用与语义：**

在列表中添加一个鼠标移动。事件会将鼠标移动到位置`pos`。如果设置了`delay`（毫秒级），测试将在移动鼠标后等待。默认位置是控件的中心。

### `void QTestEventList::addMousePress(Qt::MouseButton button, Qt::KeyboardModifiers modifiers = Qt::KeyboardModifiers(), QPoint pos = QPoint(), int delay = -1)`

**作用与语义：**

在列表中添加鼠标按压。事件会在该位置按下`button`，并选择`modifiers` `pos`带有可选`delay`。默认位置是小部件的中心。

### `void QTestEventList::addMouseRelease(Qt::MouseButton button, Qt::KeyboardModifiers modifiers = Qt::KeyboardModifiers(), QPoint pos = QPoint(), int delay = -1)`

**作用与语义：**

向列表中添加鼠标释放。事件会在位置`pos`释放`button`，`modifiers`并带有可选`delay`。默认位置是小部件的中心。

### `void QTestEventList::clear()`

**作用与语义：**

从列表中移除所有事件。

### `void QTestEventList::simulate(QWidget *w)`

**作用与语义：**

在控件`w`上逐一模拟列表中的事件。举个例子，请阅读`QTestEventList`类文档。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QTestEventList` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
