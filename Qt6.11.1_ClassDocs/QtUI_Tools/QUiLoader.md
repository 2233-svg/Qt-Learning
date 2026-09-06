# QUiLoader

> Qt 6.11.1 · Qt UI Tools

## 1. 先建立直觉

**一句话定位：** `QUiLoader` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt UI Tools 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QUiLoader` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QUiLoader>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS UiTools)
target_link_libraries(mytarget PRIVATE Qt6::UiTools)
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

- `QUiLoader(QObject *parent = nullptr)`
- `virtual ~QUiLoader() override`
- `void addPluginPath(const QString &path)`
- `QStringList availableLayouts() const`
- `QStringList availableWidgets() const`
- `void clearPluginPaths()`
- `virtual QAction * createAction(QObject *parent = nullptr, const QString &name = QString())`
- `virtual QActionGroup * createActionGroup(QObject *parent = nullptr, const QString &name = QString())`
- `virtual QLayout * createLayout(const QString &className, QObject *parent = nullptr, const QString &name = QString())`
- `virtual QWidget * createWidget(const QString &className, QWidget *parent = nullptr, const QString &name = QString())`
- `QString errorString() const`
- `bool isLanguageChangeEnabled() const`
- `QWidget * load(QIODevice *device, QWidget *parentWidget = nullptr)`
- `QStringList pluginPaths() const`
- `void setLanguageChangeEnabled(bool enabled)`
- `void setWorkingDirectory(const QDir &dir)`
- `QDir workingDirectory() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QUiLoader::QUiLoader(QObject *parent = nullptr)`

**作用与语义：**

用给定的`parent`创建一个表单加载器。

### `[override virtual noexcept] QUiLoader::~QUiLoader()`

**作用与语义：**

会毁掉装载机。

### `void QUiLoader::addPluginPath(const QString &path)`

**作用与语义：**

将给定`path`添加到加载器寻找插件时将要搜索的路径列表中。

### `QStringList QUiLoader::availableLayouts() const`

**作用与语义：**

返回一个列表，列出所有可用布局，这些布局可通过 `createLayout()` 函数构建。

### `QStringList QUiLoader::availableWidgets() const`

**作用与语义：**

返回一个列表，列出所有可用控件，这些控件可以通过`createWidget()`函数构建，即在给定插件路径内指定的控件。

### `void QUiLoader::clearPluginPaths()`

**作用与语义：**

清除加载器在寻找插件时将要搜索的路径列表。

### `[virtual] QAction *QUiLoader::createAction(QObject *parent = nullptr, const QString &name = QString())`

**作用与语义：**

用给定的`parent`和`name`创建一个新的动作。
该函数在`QUiLoader`类创建小部件时也会在内部使用。因此，你可以子类 `QUiLoader` 并重新实现该函数，以干预构建用户界面或小部件的过程。然而，在实现过程中，确保先调用 `QUiLoader` 的版本。

### `[virtual] QActionGroup *QUiLoader::createActionGroup(QObject *parent = nullptr, const QString &name = QString())`

**作用与语义：**

创建一个包含给定`parent`和`name`的新动作组。
该函数在`QUiLoader`类创建小部件时也会在内部使用。因此，你可以子类 `QUiLoader`并重新实现该函数，以干预构建用户界面或小部件的过程。但在实现中，确保先调用 `QUiLoader` 的版本。

### `[virtual] QLayout *QUiLoader::createLayout(const QString &className, QObject *parent = nullptr, const QString &name = QString())`

**作用与语义：**

使用`className`指定的类创建一个新的布局，使用给定的`parent`和`name`。
该函数也被`QUiLoader`类在创建小部件时内部使用。因此，你可以子类 `QUiLoader` 并重新实现该函数，以干预构建用户界面或小部件的过程。不过，在实现中，确保先调用 `QUiLoader` 版本。

### `[virtual] QWidget *QUiLoader::createWidget(const QString &className, QWidget *parent = nullptr, const QString &name = QString())`

**作用与语义：**

用`className`指定的类创建一个带有指定`parent`和`name`的新控件。你可以用这个函数创建`availableWidgets()`函数返回的任何控件。
该函数也被`QUiLoader`类在创建小部件时内部使用。因此，你可以子类 `QUiLoader`并重新实现该函数，以干预构建用户界面或小部件的过程。但在实现中，确保先调用 `QUiLoader` 版本。

### `QString QUiLoader::errorString() const`

**作用与语义：**

返回`load()`年最后一次错误的人类可读描述。

### `bool QUiLoader::isLanguageChangeEnabled() const`

**作用与语义：**

如果启用了语言变化动态重翻译，则返回真;否则返回假。

### `QWidget *QUiLoader::load(QIODevice *device, QWidget *parentWidget = nullptr)`

**作用与语义：**

从给定`device`加载表单，并创建一个带有指定`parentWidget`的新控件来存放其内容。

### `QStringList QUiLoader::pluginPaths() const`

**作用与语义：**

返回一个列表，命名加载器在寻找自定义控件插件时将搜索的路径。

### `void QUiLoader::setLanguageChangeEnabled(bool enabled)`

**作用与语义：**

如果`enabled`为真，该加载器加载的用户界面在收到语言变更事件后会自动重新翻译。否则，用户界面不会被重新翻译。

### `void QUiLoader::setWorkingDirectory(const QDir &dir)`

**作用与语义：**

将加载器的工作目录设置为`dir`。加载器会在相对于该目录的路径中寻找其他资源，如图标和资源文件。

### `QDir QUiLoader::workingDirectory() const`

**作用与语义：**

返回加载器的工作目录。

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

`QUiLoader` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
