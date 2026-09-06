# QShortcut

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QShortcut` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QShortcut` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QShortcut>`
- 继承自：QObject
- 直接派生类：未在类页中列出

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

### 属性

- `autoRepeat : bool`
- `context : Qt::ShortcutContext`
- `enabled : bool`
- `key : QKeySequence`

### 公有函数

- `QShortcut(QObject *parent)`
- `(since 6.0) QShortcut(QKeySequence::StandardKey standardKey, QObject *parent, const char *member = nullptr, const char *ambiguousMember = nullptr, Qt::ShortcutContext context = Qt::WindowShortcut)`
- `QShortcut(const QKeySequence &key, QObject *parent, const char *member = nullptr, const char *ambiguousMember = nullptr, Qt::ShortcutContext context = Qt::WindowShortcut)`
- `(since 6.0) QShortcut(QKeySequence::StandardKey key, QObject *parent, Functor functor, Qt::ShortcutContext shortcutContext = Qt::WindowShortcut)`
- `QShortcut(const QKeySequence &key, QObject *parent, Functor functor, Qt::ShortcutContext shortcutContext = Qt::WindowShortcut)`
- `(since 6.0) QShortcut(QKeySequence::StandardKey key, QObject *parent, const QObject *context, Functor functor, Qt::ShortcutContext shortcutContext = Qt::WindowShortcut)`
- `QShortcut(const QKeySequence &key, QObject *parent, const QObject *context, Functor functor, Qt::ShortcutContext shortcutContext = Qt::WindowShortcut)`
- `(since 6.0) QShortcut(QKeySequence::StandardKey key, QObject *parent, const QObject *context, Functor functor, FunctorAmbiguous functorAmbiguous, Qt::ShortcutContext shortcutContext = Qt::WindowShortcut)`
- `QShortcut(const QKeySequence &key, QObject *parent, const QObject *context, Functor functor, FunctorAmbiguous functorAmbiguous, Qt::ShortcutContext shortcutContext = Qt::WindowShortcut)`
- `(since 6.0) QShortcut(QKeySequence::StandardKey key, QObject *parent, const QObject *context1, Functor functor, const QObject *context2, FunctorAmbiguous functorAmbiguous, Qt::ShortcutContext shortcutContext = Qt::WindowShortcut)`
- `QShortcut(const QKeySequence &key, QObject *parent, const QObject *context1, Functor functor, const QObject *context2, FunctorAmbiguous functorAmbiguous, Qt::ShortcutContext shortcutContext = Qt::WindowShortcut)`
- `virtual ~QShortcut()`
- `bool autoRepeat() const`
- `Qt::ShortcutContext context() const`
- `bool isEnabled() const`
- `QKeySequence key() const`
- `(since 6.0) QList<QKeySequence> keys() const`
- `QWidget * parentWidget() const`
- `void setAutoRepeat(bool on)`
- `void setContext(Qt::ShortcutContext context)`
- `void setEnabled(bool enable)`
- `void setKey(const QKeySequence &key)`
- `(since 6.0) void setKeys(QKeySequence::StandardKey key)`
- `(since 6.0) void setKeys(const QList<QKeySequence> &keys)`
- `void setWhatsThis(const QString &text)`
- `QString whatsThis() const`

### 信号

- `void activated()`
- `void activatedAmbiguously()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `autoRepeat : bool`

**作用与语义：**

该属性决定了捷径是否能自动重复。
如果为真，只要系统上启用了键盘自动重复，只要按住快捷键组合，快捷方式会自动重复。默认值为真。

**如何使用：** 调用 `autoRepeat()` 读取当前值；它不会修改应用状态。

### `context : Qt::ShortcutContext`

**作用与语义：**

该属性表示快捷方式有效的上下文。
快捷方式的上下文决定了在何种情况下允许触发快捷方式。正常上下文是`Qt::WindowShortcut`，如果父节点（包含快捷方式的控件）是活跃顶层窗口的子控件，则该快捷方式可以触发。
默认情况下，该属性设置为`Qt::WindowShortcut`。

**如何使用：** 调用 `context()` 读取当前值；它不会修改应用状态。

### `enabled : bool`

**作用与语义：**

该属性是否启用了捷径。
启用的快捷方式在出现与快捷方式`key()`序列相符的`QShortcutEvent`时，会发出`activated()`或`activatedAmbiguously()`信号。
如果应用处于`WhatsThis`模式，捷径不会发出信号，而是显示“这是什么？”的文字。
默认情况下，该属性为`true`。

**如何使用：** 调用 `enabled()` 读取当前值；它不会修改应用状态。

### `key : QKeySequence`

**作用与语义：**

该属性包含快捷键的主键序列。
这是一个按键序列，可选组合为Shift、Ctrl和Alt。按键序列可以通过多种方式提供：
默认情况下，该属性包含空密钥序列。

**如何使用：** 调用 `key()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 setKey(0);                  // no signal emitted
 setKey(QKeySequence());     // no signal emitted
 setKey(0x3b1);              // Greek letter alpha
 setKey(Qt::Key_D);              // 'd', e.g. to delete
 setKey('q');                // 'q', e.g. to quit
 setKey(Qt::CTRL | Qt::Key_P);       // Ctrl+P, e.g. to print document
 setKey(tr("Ctrl+P"));           // Ctrl+P, e.g. to print document
```

### `[explicit] QShortcut::QShortcut(QObject *parent)`

**作用与语义：**

为`parent`构造一个QShortcut对象，应该是`QWindow`或`QWidget`。
由于没有指定快捷键序列，快捷键不会发出任何信号。

### `[explicit, since 6.0] QShortcut::QShortcut(QKeySequence::StandardKey standardKey, QObject *parent, const char *member = nullptr, const char *ambiguousMember = nullptr, Qt::ShortcutContext context = Qt::WindowShortcut)`

**作用与语义：**

为`parent`构造一个QShortcut对象，应该是`QWindow`或`QWidget`。
快捷方式会在其父功能上运行，监听与`standardKey`匹配的`QShortcutEvent`。根据事件的歧义，快捷方式会调用`member`函数，或者如果按键在快捷方式的`context`中，则调用`ambiguousMember`函数。

### `[explicit] QShortcut::QShortcut(const QKeySequence &key, QObject *parent, const char *member = nullptr, const char *ambiguousMember = nullptr, Qt::ShortcutContext context = Qt::WindowShortcut)`

**作用与语义：**

为`parent`构造一个QShortcut对象，应该是`QWindow`或`QWidget`。
捷径在其父程序上运行，监听与`key`序列匹配的`QShortcutEvent`。根据事件的歧义，捷径会调用`member`函数，或者如果按键在快捷方式的`context`中，则调用`ambiguousMember`函数。

### `[since 6.0] template <typename Functor> QShortcut::QShortcut(QKeySequence::StandardKey key, QObject *parent, Functor functor, Qt::ShortcutContext shortcutContext = Qt::WindowShortcut)`

**作用与语义：**

这是一个QShortcut便利构造器，将捷径的`activated()`信号连接到`functor`。

### `template <typename Functor> QShortcut::QShortcut(const QKeySequence &key, QObject *parent, Functor functor, Qt::ShortcutContext shortcutContext = Qt::WindowShortcut)`

**作用与语义：**

这是一个QShortcut便利构造器，将捷径的`activated()`信号连接到`functor`。

### `[since 6.0] template <typename Functor> QShortcut::QShortcut(QKeySequence::StandardKey key, QObject *parent, const QObject *context, Functor functor, Qt::ShortcutContext shortcutContext = Qt::WindowShortcut)`

**作用与语义：**

这是一个QShortcut便利构造器，将快捷方式的`activated()`信号连接到`functor`。
`functor`可以是指向`context`对象成员函数的指针。
如果`context`对象被销毁，`functor`不会被调用。

### `template <typename Functor> QShortcut::QShortcut(const QKeySequence &key, QObject *parent, const QObject *context, Functor functor, Qt::ShortcutContext shortcutContext = Qt::WindowShortcut)`

**作用与语义：**

这是一个QShortcut便利构造器，将快捷方式的`activated()`信号连接到`functor`。
`functor`可以是指向`context`对象成员函数的指针。
如果`context`对象被销毁，`functor`不会被调用。

### `[since 6.0] template <typename Functor, typename FunctorAmbiguous> QShortcut::QShortcut(QKeySequence::StandardKey key, QObject *parent, const QObject *context, Functor functor, FunctorAmbiguous functorAmbiguous, Qt::ShortcutContext shortcutContext = Qt::WindowShortcut)`

**作用与语义：**

这是一个QShortcut便利构造器，将快捷方式的`activated()`信号连接到`functor`，`activatedAmbiguously()`信号连接到`functorAmbiguous`。
`functor` 和 `functorAmbiguous` 可以作为指向`context`对象成员函数的指针。
如果`context`对象被销毁，`functor`和`functorAmbiguous`不会被调用。

### `template <typename Functor, typename FunctorAmbiguous> QShortcut::QShortcut(const QKeySequence &key, QObject *parent, const QObject *context, Functor functor, FunctorAmbiguous functorAmbiguous, Qt::ShortcutContext shortcutContext = Qt::WindowShortcut)`

**作用与语义：**

这是一个QShortcut便利构造器，将快捷方式的`activated()`信号连接到`functor`，`activatedAmbiguously()`信号连接到`functorAmbiguous`。
`functor` 和 `functorAmbiguous` 可以作为指向`context`对象成员函数的指针。
如果`context`对象被销毁，`functor`和`functorAmbiguous`不会被调用。

### `[since 6.0] template <typename Functor, typename FunctorAmbiguous> QShortcut::QShortcut(QKeySequence::StandardKey key, QObject *parent, const QObject *context1, Functor functor, const QObject *context2, FunctorAmbiguous functorAmbiguous, Qt::ShortcutContext shortcutContext = Qt::WindowShortcut)`

**作用与语义：**

这是一个QShortcut便利构造器，将快捷路的`activated()`信号连接到`functor`，`activatedAmbiguously()`信号连接到`functorAmbiguous`。
`functor`可以是指向`context1`对象成员函数的指针。`functorAmbiguous`可以指向`context2`对象的成员函数。
如果`context1`对象被摧毁，`functor`不会被调用。如果`context2`对象被摧毁，`functorAmbiguous`不会被调用。

### `template <typename Functor, typename FunctorAmbiguous> QShortcut::QShortcut(const QKeySequence &key, QObject *parent, const QObject *context1, Functor functor, const QObject *context2, FunctorAmbiguous functorAmbiguous, Qt::ShortcutContext shortcutContext = Qt::WindowShortcut)`

**作用与语义：**

这是一个QShortcut便利构造器，将快捷路的`activated()`信号连接到`functor`，`activatedAmbiguously()`信号连接到`functorAmbiguous`。
`functor`可以是指向`context1`对象成员函数的指针。`functorAmbiguous`可以指向`context2`对象的成员函数。
如果`context1`对象被摧毁，`functor`不会被调用。如果`context2`对象被摧毁，`functorAmbiguous`不会被调用。

### `[virtual noexcept] QShortcut::~QShortcut()`

**作用与语义：**

破坏捷径。

### `[signal] void QShortcut::activated()`

**作用与语义：**

当用户输入快捷键的按键序列时，该信号会发出。

### `[signal] void QShortcut::activatedAmbiguously()`

**作用与语义：**

当键盘输入一个按键序列时，只要它与多个快捷键的开头相符，就称为歧义。
当快捷键序列完成时，如果快捷键序列仍然模糊（即一个或多个快捷键的起点），则会发出激活Ambiguously()。此时不会发出`activated()`信号。

### `[since 6.0] QList<QKeySequence> QShortcut::keys() const`

**作用与语义：**

返回触发该快捷方式的密钥序列列表。

### `QWidget *QShortcut::parentWidget() const`

**作用与语义：**

返回快捷方式的父控件。

### `[since 6.0] void QShortcut::setKeys(QKeySequence::StandardKey key)`

**作用与语义：**

设置触发条件与标准密钥`key`匹配。

### `[since 6.0] void QShortcut::setKeys(const QList<QKeySequence> &keys)`

**作用与语义：**

将`keys`设置为触发快捷方式的按键序列列表。

### `void QShortcut::setWhatsThis(const QString &text)`

**作用与语义：**

设置快捷方式“这是什么？”帮助`text`。
当小部件应用处于“这是什么？”模式，用户输入快捷方式`key()`序列时，文本将会显示。
要在菜单项上设置“这是什么？”帮助（有快捷键或无快捷键），请将帮助设置在该项的动作上。
默认情况下，帮助文本是空字符串。
该函数在不使用控件的应用程序中没有影响。

### `QString QShortcut::whatsThis() const`

**作用与语义：**

返回快捷方式的“这是什么？”帮助文本。

### `bool autoRepeat() const`

**作用与语义：**

该属性决定了捷径是否能自动重复。
如果为真，只要系统上启用了键盘自动重复，只要按住快捷键组合，快捷方式会自动重复。默认值为真。

**如何使用：** 调用 `autoRepeat()` 读取当前值；它不会修改应用状态。

### `Qt::ShortcutContext context() const`

**作用与语义：**

该属性表示快捷方式有效的上下文。
快捷方式的上下文决定了在何种情况下允许触发快捷方式。正常上下文是`Qt::WindowShortcut`，如果父节点（包含快捷方式的控件）是活跃顶层窗口的子控件，则该快捷方式可以触发。
默认情况下，该属性设置为`Qt::WindowShortcut`。

**如何使用：** 调用 `context()` 读取当前值；它不会修改应用状态。

### `bool isEnabled() const`

**作用与语义：**

该属性是否启用了捷径。
启用的快捷方式在出现与快捷方式`key()`序列相符的`QShortcutEvent`时，会发出`activated()`或`activatedAmbiguously()`信号。
如果应用处于`WhatsThis`模式，捷径不会发出信号，而是显示“这是什么？”的文字。
默认情况下，该属性为`true`。

**如何使用：** 调用 `isEnabled()` 读取当前值；它不会修改应用状态。

### `QKeySequence key() const`

**作用与语义：**

该属性包含快捷键的主键序列。
这是一个按键序列，可选组合为Shift、Ctrl和Alt。按键序列可以通过多种方式提供：
默认情况下，该属性包含空密钥序列。

**如何使用：** 调用 `key()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 setKey(0);                  // no signal emitted
 setKey(QKeySequence());     // no signal emitted
 setKey(0x3b1);              // Greek letter alpha
 setKey(Qt::Key_D);              // 'd', e.g. to delete
 setKey('q');                // 'q', e.g. to quit
 setKey(Qt::CTRL | Qt::Key_P);       // Ctrl+P, e.g. to print document
 setKey(tr("Ctrl+P"));           // Ctrl+P, e.g. to print document
```

### `void setAutoRepeat(bool on)`

**作用与语义：**

该属性决定了捷径是否能自动重复。
如果为真，只要系统上启用了键盘自动重复，只要按住快捷键组合，快捷方式会自动重复。默认值为真。

**如何使用：** 调用 `setAutoRepeat(...)` 修改 `autoRepeat`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setContext(Qt::ShortcutContext context)`

**作用与语义：**

该属性表示快捷方式有效的上下文。
快捷方式的上下文决定了在何种情况下允许触发快捷方式。正常上下文是`Qt::WindowShortcut`，如果父节点（包含快捷方式的控件）是活跃顶层窗口的子控件，则该快捷方式可以触发。
默认情况下，该属性设置为`Qt::WindowShortcut`。

**如何使用：** 调用 `setContext(...)` 修改 `context`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setEnabled(bool enable)`

**作用与语义：**

该属性是否启用了捷径。
启用的快捷方式在出现与快捷方式`key()`序列相符的`QShortcutEvent`时，会发出`activated()`或`activatedAmbiguously()`信号。
如果应用处于`WhatsThis`模式，捷径不会发出信号，而是显示“这是什么？”的文字。
默认情况下，该属性为`true`。

**如何使用：** 调用 `setEnabled(...)` 修改 `enabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setKey(const QKeySequence &key)`

**作用与语义：**

该属性包含快捷键的主键序列。
这是一个按键序列，可选组合为Shift、Ctrl和Alt。按键序列可以通过多种方式提供：
默认情况下，该属性包含空密钥序列。

**如何使用：** 调用 `setKey(...)` 修改 `key`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 setKey(0);                  // no signal emitted
 setKey(QKeySequence());     // no signal emitted
 setKey(0x3b1);              // Greek letter alpha
 setKey(Qt::Key_D);              // 'd', e.g. to delete
 setKey('q');                // 'q', e.g. to quit
 setKey(Qt::CTRL | Qt::Key_P);       // Ctrl+P, e.g. to print document
 setKey(tr("Ctrl+P"));           // Ctrl+P, e.g. to print document
```

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

`QShortcut` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
