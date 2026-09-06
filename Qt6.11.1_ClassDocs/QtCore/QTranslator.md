# QTranslator

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QTranslator` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QTranslator` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QTranslator>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
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

### 公有函数

- `QTranslator(QObject *parent = nullptr)`
- `virtual ~QTranslator()`
- `QString filePath() const`
- `virtual bool isEmpty() const`
- `QString language() const`
- `bool load(const QString &filename, const QString &directory = QString(), const QString &search_delimiters = QString(), const QString &suffix = QString())`
- `bool load(const QLocale &locale, const QString &filename, const QString &prefix = QString(), const QString &directory = QString(), const QString &suffix = QString())`
- `bool load(const uchar *data, int len, const QString &directory = QString())`
- `virtual QString translate(const char *context, const char *sourceText, const char *disambiguation = nullptr, int n = -1) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QTranslator::QTranslator(QObject *parent = nullptr)`

**作用与语义：**

构造一个带有父 `parent`、不与任何文件相连的空消息文件对象。

### `[virtual noexcept] QTranslator::~QTranslator()`

**作用与语义：**

摧毁该物体并释放所有分配的资源。

### `QString QTranslator::filePath() const`

**作用与语义：**

返回加载的翻译文件路径。
如果还没有加载翻译、加载失败，或没有从文件加载转换，则该文件路径为空。

### `[virtual] bool QTranslator::isEmpty() const`

**作用与语义：**

如果此翻译器为空，则返回 `true`，否则返回 `false`。

### `QString QTranslator::language() const`

**作用与语义：**

返回翻译文件中存储的目标语言。

### `bool QTranslator::load(const QString &filename, const QString &directory = QString(), const QString &search_delimiters = QString(), const QString &suffix = QString())`

**作用与语义：**

加载`filename` `suffix`（“如果未指定`suffix`则为”.qm“），该文件名可以是绝对文件名或相对于`directory`。如果翻译成功加载，返回`true`;否则返回`false`。
如果未指定`directory`，则使用当前目录（即`currentPath()`）。
该翻译器对象的先前内容被丢弃。
如果该文件名不存在，则按以下顺序尝试其他文件名：
- 文件名，不加附加`suffix`。
- 文件名中字符后带文本`search_delimiters`剥离（“如果是空字符串，则默认用_.”作为`search_delimiters`）并`suffix`。
- 文件名剥离且未添加`suffix`。
- 进一步剥离文件名等。
例如，在fr_CA地区（法语区加拿大）运行的应用程序可能会调用 load（“foo.fr_ca”， “/opt/foolib”）。load() 则会尝试从该列表中打开第一个可读的文件：
- `/opt/foolib/foo.fr_ca.qm`
- `/opt/foolib/foo.fr_ca`
- `/opt/foolib/foo.fr.qm`
- `/opt/foolib/foo.fr`
- `/opt/foolib/foo.qm`
- `/opt/foolib/foo`
通常，更好的做法是使用 QTranslator：：load（const `QLocale` &， const `QString` &， const `QString` &， const `QString` &， const `QString` &） 函数，因为它使用`QLocale::uiLanguages()`而不仅仅是地方名，后者指的是日期和数字的格式化，而不一定是界面语言。

### `bool QTranslator::load(const QLocale &locale, const QString &filename, const QString &prefix = QString(), const QString &directory = QString(), const QString &suffix = QString())`

**作用与语义：**

加载`filename` `prefix` ui 语言名称 `suffix`（“如果未指定`suffix`则为”.qm“），该名称可以是绝对文件名或相对于 `directory` 的。如果翻译成功加载，返回 `true`;否则返回 `false`。
该翻译器对象的先前内容被丢弃。
如果该文件名不存在，则按以下顺序尝试其他文件名：
- 文件名无`suffix`。
- 文件名，带有 UI 语言部分，后面是“_”字符，去除并`suffix`。
- 文件名，去除 UI 语言部分，不附加`suffix`。
- 文件名，UI语言部分进一步简化，等等。
例如，在`locale`中运行的应用程序使用以下 ui 语言——“es”、“fr-CA”、“de”，可能会调用 load（QLocale()、“foo”、“.”、“/opt/foolib”、“.qm”。load() 会将 UI 语言中的 '-'（破折号）替换为 '_'（下划线），然后尝试打开该列表中第一个可读的文件：
- `/opt/foolib/foo.es.qm`
- `/opt/foolib/foo.es`
- `/opt/foolib/foo.fr_CA.qm`
- `/opt/foolib/foo.fr_CA`
- `/opt/foolib/foo.fr.qm`
- `/opt/foolib/foo.fr`
- `/opt/foolib/foo.de.qm`
- `/opt/foolib/foo.de`
- `/opt/foolib/foo.qm`
- `/opt/foolib/foo`。
- `/opt/foolib/foo`
在文件系统区分大小写的操作系统上，`QTranslator` 还会尝试加载小写版本的本地名称。

### `bool QTranslator::load(const uchar *data, int len, const QString &directory = QString())`

**作用与语义：**

将长度为`len`的量子力学文件数据`data`加载到翻译器中。
数据不会被复制。调用者必须能够保证`data`不会被删除或修改。
`directory` 仅用于在加载量子管理文件的依赖时指定基础目录。如果文件没有依赖，则忽略该参数。
注意：此功能会让`QTranslator::load()`重载。

### `[virtual] QString QTranslator::translate(const char *context, const char *sourceText, const char *disambiguation = nullptr, int n = -1) const`

**作用与语义：**

返回键的平移（`context`， `sourceText`， `disambiguation`）。如果未找到，也尝试 （`context`， `sourceText`， “）。如果仍失败，返回空字符串。
注意：不完整的翻译可能导致意外行为：如果没有提供 （`context`， `sourceText`， “”）的翻译，方法在这种情况下可能会返回不同`disambiguation`的翻译。
如果`n`不是-1，则用于选择合适的翻译形式（例如“找到了 %n 个文件”与“找到了 %n 个文件”）。
如果你需要在`QTranslator`中程序化插入翻译，这个函数可以重新实现。
注意：该功能是线程安全的。

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

`QTranslator` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
