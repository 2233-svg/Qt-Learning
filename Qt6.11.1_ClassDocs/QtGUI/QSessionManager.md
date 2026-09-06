# QSessionManager

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QSessionManager` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QSessionManager` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QSessionManager>`
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

### 公有类型

- `enum RestartHint { RestartIfRunning, RestartAnyway, RestartImmediately, RestartNever }`

### 公有函数

- `bool allowsErrorInteraction()`
- `bool allowsInteraction()`
- `void cancel()`
- `QStringList discardCommand() const`
- `bool isPhase2() const`
- `void release()`
- `void requestPhase2()`
- `QStringList restartCommand() const`
- `QSessionManager::RestartHint restartHint() const`
- `QString sessionId() const`
- `QString sessionKey() const`
- `void setDiscardCommand(const QStringList &command)`
- `void setManagerProperty(const QString &name, const QStringList &value)`
- `void setManagerProperty(const QString &name, const QString &value)`
- `void setRestartCommand(const QStringList &command)`
- `void setRestartHint(QSessionManager::RestartHint hint)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSessionManager::RestartHint`

**作用与语义：**

该枚举类型定义了该应用程序希望被会话管理器重启的情形。当前的值为：
- `QSessionManager::RestartIfRunning`：`0`;如果会话关闭时应用程序仍在运行，它希望在下一个会话开始时重新启动。
- `QSessionManager::RestartAnyway`：`1`;无论如何，应用程序都希望在下一次会话开始时启动。（这对启动后立即运行然后退出的工具非常有用。）
- `QSessionManager::RestartImmediately`：`2`;应用程序希望在未运行时立即启动。
- `QSessionManager::RestartNever`：`3`;应用程序不希望被自动重启。
默认提示是`RestartIfRunning`。

### `bool QSessionManager::allowsErrorInteraction()`

**作用与语义：**

如果允许错误交互，返回`true`;否则返回`false`。
这与`allowsInteraction()`类似，但也使应用程序能够告知用户任何发生的错误。会话管理器可能会将错误交互请求赋予更高优先级，这意味着错误交互被允许的可能性更大。然而，你仍然无法保证会话管理器会允许交互。

### `bool QSessionManager::allowsInteraction()`

**作用与语义：**

请求会话管理器允许与用户交互。如果允许交互，返回 true;否则返回 `false`。
该机制的原理是使用户在关机期间能够同步交互。高级会话管理器可以同时要求所有应用程序提交数据，从而实现更快的关机速度。
交互完成后，我们强烈建议通过调用`release()`释放用户交互信号量。这样，其他应用程序可能有机会与用户交互，而你的应用仍在忙于保存数据。（当应用退出时，信号量是隐式释放的。）。
如果用户在交互阶段决定取消关闭进程，你必须通过调用`cancel()`告诉会话管理器此事发生。
以下是应用`QGuiApplication::commitDataRequest()`可能实现的一个示例：
如果应用在保存数据时出现错误，你可以尝试`allowsErrorInteraction()`。

**官方示例：**

```cpp
 MyMainWidget::MyMainWidget(QWidget *parent)
     : QWidget(parent)
 {
     connect(qApp, &QGuiApplication::commitDataRequest,
             this, &MyMainWidget::commitData);
 }

 void MyMainWidget::commitData(QSessionManager& manager)
 {
     if (manager.allowsInteraction()) {
         int ret = QMessageBox::warning(
                     mainWindow,
                     tr("My Application"),
                     tr("Save changes to document?"),
                     QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel);

         switch (ret) {
         case QMessageBox::Save:
             manager.release();
             if (!saveDocument())
                 manager.cancel();
             break;
         case QMessageBox::Discard:
             break;
         case QMessageBox::Cancel:
         default:
             manager.cancel();
         }
     } else {
         // we did not get permission to interact, then
         // do something reasonable instead
     }
 }
```

### `void QSessionManager::cancel()`

**作用与语义：**

告诉会话管理器取消关闭进程。应用程序不应在未先征求用户意见的情况下调用此函数。

### `QStringList QSessionManager::discardCommand() const`

**作用与语义：**

返回当前设置的弃牌命令。

### `bool QSessionManager::isPhase2() const`

**作用与语义：**

如果会话管理器当前正在执行第二个会话管理阶段，返回`true`;否则返回`false`。

### `void QSessionManager::release()`

**作用与语义：**

在交互阶段结束后释放会话管理器的交互信号量。

### `void QSessionManager::requestPhase2()`

**作用与语义：**

请求对应用程序进行第二次会话管理阶段。应用程序随后可以立即从`QGuiApplication::commitDataRequest()`或`QApplication::saveStateRequest()`函数返回，并在大多数或所有其他应用程序完成会话管理后再次调用。
这两个阶段对于需要存储其他应用窗口信息的应用（如X11窗口管理器）非常有用，因此必须等待这些应用程序完成各自的会话管理任务。
注意：如果其他申请请求了第二阶段，可能会在你的申请第二阶段之前、同时或之后调用。

### `QStringList QSessionManager::restartCommand() const`

**作用与语义：**

返回当前设置的重启命令。

### `QSessionManager::RestartHint QSessionManager::restartHint() const`

**作用与语义：**

返回应用程序当前的重启提示。默认是`RestartIfRunning`。

### `QString QSessionManager::sessionId() const`

**作用与语义：**

返回当前会话的标识符。
如果应用程序已从早期会话恢复，该标识符与之前会话相同。

### `QString QSessionManager::sessionKey() const`

**作用与语义：**

返回当前会话中的会话密钥。
如果应用程序是从早期会话恢复的，该密钥与上一个会话结束时相同。
会话密钥会随着每次调用 commitData() 或 saveState() 而变化。

### `void QSessionManager::setDiscardCommand(const QStringList &command)`

**作用与语义：**

将弃牌命令设置为给定的 `command`。

### `void QSessionManager::setManagerProperty(const QString &name, const QStringList &value)`

**作用与语义：**

对应用识别和状态记录的低层写入权限保存在会话管理器中。
称为 `name` 的属性的值设置为字符串列表 的 List，其值设在 Str List `value`。

### `void QSessionManager::setManagerProperty(const QString &name, const QString &value)`

**作用与语义：**

对应用程序识别和状态记录的低级写入权限保存在会话管理器中。
称为`name`的属性的值被设置为字符串`value`。

### `void QSessionManager::setRestartCommand(const QStringList &command)`

**作用与语义：**

如果会话管理器能够恢复会话，它会执行`command`以恢复应用程序。该命令默认为。
`-session`选项是强制的;否则`QGuiApplication`无法判断是否恢复了，也无法判断当前会话标识符是什么。详情请参见`QGuiApplication::isSessionRestored()`和 `QGuiApplication::sessionId()`。
如果你的应用非常简单，可能可以在额外的命令行选项中存储整个应用状态。这通常是个坏主意，因为命令行通常限制在几百字节。相反，可以使用`QSettings`、临时文件或数据库来实现这一点。通过在数据上标记唯一的`sessionId()`，你就能在未来的会话中恢复应用程序。

**官方示例：**

```cpp
 appname -session id
```

### `void QSessionManager::setRestartHint(QSessionManager::RestartHint hint)`

**作用与语义：**

将应用程序的重启提示设置为`hint`。启动应用程序时，提示设置为`RestartIfRunning`。
注意：这些标志只是提示，会话管理器可能会尊重也可能不会。
我们建议在`QGuiApplication::saveStateRequest()`中设置重启提示，因为大多数会话管理器会在应用程序启动后不久执行检查点。

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

`QSessionManager` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
