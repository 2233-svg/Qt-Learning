# QValidator

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QValidator` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QValidator` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QValidator>`
- 继承自：QObject
- 直接派生类：QDoubleValidator、QIntValidator,、QRegularExpressionValidator

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum State { Invalid, Intermediate, Acceptable }`

### 公有函数

- `QValidator(QObject *parent = nullptr)`
- `virtual ~QValidator()`
- `virtual void fixup(QString &input) const`
- `QLocale locale() const`
- `void setLocale(const QLocale &locale)`
- `virtual QValidator::State validate(QString &input, int &pos) const = 0`

### 信号

- `void changed()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QValidator::State`

**作用与语义：**

该枚举类型定义了验证字符串可以存在的状态。
- `QValidator::Invalid`：`0`;字符串显然无效。
- `QValidator::Intermediate`：`1`;字符串是一个合理的中间值。
- `QValidator::Acceptable`：`2`;字符串作为最终结果是可接受的;即有效。

### `[explicit] QValidator::QValidator(QObject *parent = nullptr)`

**作用与语义：**

建立验证器。`parent`参数传递给`QObject`构造器。

### `[virtual noexcept] QValidator::~QValidator()`

**作用与语义：**

销毁验证程序，释放所有存储和其他资源。

### `[signal] void QValidator::changed()`

**作用与语义：**

当任何可能影响字符串有效性的属性发生变化时，该信号就会发出。

### `[virtual] void QValidator::fixup(QString &input) const`

**作用与语义：**

该函数尝试根据该验证者的规则将`input`变为有效。它不一定生成有效字符串：调用该函数的人必须事后重新测试;默认值不做任何事。
该函数的重实现即使不产生有效字符串，也可能发生`input`变化。例如，ISBN验证器可能希望删除除数字和“-”以外的所有字符，即使结果仍不是有效的ISBN;姓氏验证器可能希望去除字符串开头和结尾的空白，即使该字符串不在接受的姓氏列表中。

### `QLocale QValidator::locale() const`

**作用与语义：**

返回验证者的区域。该位置默认初始化为与 QLocale() 相同的位置。

### `void QValidator::setLocale(const QLocale &locale)`

**作用与语义：**

设置将用于验证器的`locale`。除非调用了 setLocale，验证器将使用带有 `QLocale::setDefault()` 的默认区域集。如果没有设置默认区域，则该区域是操作系统的区域。

### `[pure virtual] QValidator::State QValidator::validate(QString &input, int &pos) const`

**作用与语义：**

如果`input`根据该验证者的规则无效，`Intermediate`如果稍作编辑能使输入可接受（例如用户在接受整数介于 10 到 99 的小部件中输入“4”），以及`Acceptable`输入是否有效，该虚拟函数会返回`Invalid`。
该函数可以同时改变`input`和`pos`（光标位置）如有需要。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QValidator` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
