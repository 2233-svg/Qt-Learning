# QInputMethod

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QInputMethod` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QInputMethod` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QInputMethod>`
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

- `enum Action { Click, ContextMenu }`

### 属性

- `anchorRectangle : QRectF`
- `animating : bool`
- `cursorRectangle : QRectF`
- `inputDirection : Qt::LayoutDirection`
- `inputItemClipRectangle : QRectF`
- `keyboardRectangle : QRectF`
- `locale : QLocale`
- `visible : bool`

### 公有函数

- `QRectF anchorRectangle() const`
- `QRectF cursorRectangle() const`
- `Qt::LayoutDirection inputDirection() const`
- `QRectF inputItemClipRectangle() const`
- `QRectF inputItemRectangle() const`
- `QTransform inputItemTransform() const`
- `bool isAnimating() const`
- `bool isVisible() const`
- `QRectF keyboardRectangle() const`
- `QLocale locale() const`
- `void setInputItemRectangle(const QRectF &rect)`
- `void setInputItemTransform(const QTransform &transform)`
- `void setVisible(bool visible)`

### 公有槽函数

- `void commit()`
- `void hide()`
- `void invokeAction(QInputMethod::Action a, int cursorPosition)`
- `void reset()`
- `void show()`
- `void update(Qt::InputMethodQueries queries)`

### 信号

- `void anchorRectangleChanged()`
- `void animatingChanged()`
- `void cursorRectangleChanged()`
- `void inputDirectionChanged(Qt::LayoutDirection newDirection)`
- `void inputItemClipRectangleChanged()`
- `void keyboardRectangleChanged()`
- `void localeChanged()`
- `void visibleChanged()`

### 静态公有成员

- `QVariant queryFocusObject(Qt::InputMethodQuery query, const QVariant &argument)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QInputMethod::Action`

**作用与语义：**

表示用户所执行的操作类型。
- `QInputMethod::Click`：`0`;普通的点击/轻敲
- `QInputMethod::ContextMenu`：`1`;右键点击/点击（例如右键或长按）

### `[read-only] anchorRectangle : QRectF`

**作用与语义：**

在窗口坐标中输入项目的锚点矩形。
锚矩形常被各种文本编辑控件使用，比如文本预测弹窗，用于跟踪文本选择。

**如何使用：** 调用 `anchorRectangle()` 读取当前值；它不会修改应用状态。

### `[read-only] animating : bool`

**作用与语义：**

当虚拟键盘被打开或关闭时，这点确实如此。
当键盘完全打开或关闭时，动画为假。当`animating` `true`且`visibility`为`true`打开键盘时。当`animating` `true`且`visibility`为假时，键盘关闭。

**如何使用：** 调用 `animating()` 读取当前值；它不会修改应用状态。

### `[read-only] cursorRectangle : QRectF`

**作用与语义：**

在窗口坐标中输入物品的光标矩形。
光标矩形常被各种文本编辑控件使用，比如文本预测弹窗，用于跟踪正在输入的文本。

**如何使用：** 调用 `cursorRectangle()` 读取当前值；它不会修改应用状态。

### `[read-only] inputDirection : Qt::LayoutDirection`

**作用与语义：**

当前输入方向。

**如何使用：** 调用 `inputDirection()` 读取当前值；它不会修改应用状态。

### `[read-only] inputItemClipRectangle : QRectF`

**作用与语义：**

输入窗口坐标中物品裁剪的矩形。
裁剪输入矩形常被各种输入法用来确定输入法可用的屏幕空间（例如虚拟键盘）。

**如何使用：** 调用 `inputItemClipRectangle()` 读取当前值；它不会修改应用状态。

### `[read-only] keyboardRectangle : QRectF`

**作用与语义：**

虚拟键盘在窗口坐标中的几何体。
如果无法知道键盘的几何形状，这可能是一个空矩形。安卓上的浮动键盘就是这种情况。

**如何使用：** 调用 `keyboardRectangle()` 读取当前值；它不会修改应用状态。

### `[read-only] locale : QLocale`

**作用与语义：**

当前输入地点。

**如何使用：** 调用 `locale()` 读取当前值；它不会修改应用状态。

### `[read-only] visible : bool`

**作用与语义：**

虚拟键盘在屏幕上的可见性。
对于没有虚拟键盘的设备，输入法的可见性依然为假。

**如何使用：** 调用 `visible()` 读取当前值；它不会修改应用状态。

### `[slot] void QInputMethod::commit()`

**作用与语义：**

将用户当前正在撰写的词提交给编辑器。该函数主要用于具有文本预测功能的输入方法，以及用于输入字符的脚本与实际附加到编辑器的脚本不同的方法。任何中断文本写作的动作都需要通过调用commit()函数来清除写作状态，例如当光标移动到其他地方时。

### `[slot] void QInputMethod::hide()`

**作用与语义：**

请求虚拟键盘关闭。
通常应用程序不需要调用此函数，键盘应在文本编辑器失去焦点时自动关闭，例如当父视图关闭时。

### `QRectF QInputMethod::inputItemRectangle() const`

**作用与语义：**

返回输入物品的几何体，输入项坐标。

### `QTransform QInputMethod::inputItemTransform() const`

**作用与语义：**

返回从输入项坐标到窗口坐标的变换。

### `[slot] void QInputMethod::invokeAction(QInputMethod::Action a, int cursorPosition)`

**作用与语义：**

当用户点击当前构写的单词时，输入项调用该词，动作`a`和给定`cursorPosition`指示。输入法通常利用这些信息向用户提供更多单词建议。

### `[static] QVariant QInputMethod::queryFocusObject(Qt::InputMethodQuery query, const QVariant &argument)`

**作用与语义：**

将`query`发送到当前焦点对象，参数`argument`并返回结果。

### `[slot] void QInputMethod::reset()`

**作用与语义：**

重置输入法状态。例如，文本编辑器通常在插入文本前调用该方法，使控件准备好接受文本。
当聚焦编辑器发生变化时，输入法会自动重置。

### `void QInputMethod::setInputItemRectangle(const QRectF &rect)`

**作用与语义：**

将输入物品的几何体设置为`rect`，位于输入的物品坐标内。每当场景内物品移动或焦点变化时，需要通过聚焦窗口（如QQuickCanvas）更新。

### `void QInputMethod::setInputItemTransform(const QTransform &transform)`

**作用与语义：**

设置从输入物品坐标到窗口坐标的变换为`transform`。每当物品在场景内移动时，聚焦窗口（如QQuickCanvas）都需要更新物品变换。

### `void QInputMethod::setVisible(bool visible)`

**作用与语义：**

控制键盘的可见性。相当于调用`show()`（如果`visible`是`true`）或`hide()`（如果`visible`是`false`）。

### `[slot] void QInputMethod::show()`

**作用与语义：**

请求虚拟键盘打开。如果平台不提供虚拟键盘，可见性依然是假的。
通常应用程序不需要调用这个功能，键盘应当文本编辑器聚焦时自动打开。

### `[slot] void QInputMethod::update(Qt::InputMethodQueries queries)`

**作用与语义：**

输入项调用该参数，以通知平台输入方法在编辑器输入方法查询属性发生状态变化时使用。调用函数时，必须使用`queries`参数来判断哪些参数有变化，哪个输入方法可以用来查询它感兴趣的属性`QInputMethodQueryEvent`。
特别是，每次光标位置变化时调用更新非常重要，因为这通常会导致周围文本和文本选择等其他查询属性也发生变化。为了方便起见，经常随光标位置变化的属性被归类在`Qt::ImQueryInput`值中。

### `QRectF anchorRectangle() const`

**作用与语义：**

在窗口坐标中输入项目的锚点矩形。
锚矩形常被各种文本编辑控件使用，比如文本预测弹窗，用于跟踪文本选择。

**如何使用：** 调用 `anchorRectangle()` 读取当前值；它不会修改应用状态。

### `QRectF cursorRectangle() const`

**作用与语义：**

在窗口坐标中输入物品的光标矩形。
光标矩形常被各种文本编辑控件使用，比如文本预测弹窗，用于跟踪正在输入的文本。

**如何使用：** 调用 `cursorRectangle()` 读取当前值；它不会修改应用状态。

### `Qt::LayoutDirection inputDirection() const`

**作用与语义：**

当前输入方向。

**如何使用：** 调用 `inputDirection()` 读取当前值；它不会修改应用状态。

### `QRectF inputItemClipRectangle() const`

**作用与语义：**

输入窗口坐标中物品裁剪的矩形。
裁剪输入矩形常被各种输入法用来确定输入法可用的屏幕空间（例如虚拟键盘）。

**如何使用：** 调用 `inputItemClipRectangle()` 读取当前值；它不会修改应用状态。

### `bool isAnimating() const`

**作用与语义：**

当虚拟键盘被打开或关闭时，这点确实如此。
当键盘完全打开或关闭时，动画为假。当`animating` `true`且`visibility`为`true`打开键盘时。当`animating` `true`且`visibility`为假时，键盘关闭。

**如何使用：** 调用 `isAnimating()` 读取当前值；它不会修改应用状态。

### `bool isVisible() const`

**作用与语义：**

虚拟键盘在屏幕上的可见性。
对于没有虚拟键盘的设备，输入法的可见性依然为假。

**如何使用：** 调用 `isVisible()` 读取当前值；它不会修改应用状态。

### `QRectF keyboardRectangle() const`

**作用与语义：**

虚拟键盘在窗口坐标中的几何体。
如果无法知道键盘的几何形状，这可能是一个空矩形。安卓上的浮动键盘就是这种情况。

**如何使用：** 调用 `keyboardRectangle()` 读取当前值；它不会修改应用状态。

### `QLocale locale() const`

**作用与语义：**

当前输入地点。

**如何使用：** 调用 `locale()` 读取当前值；它不会修改应用状态。

### `void anchorRectangleChanged()`

**作用与语义：**

在窗口坐标中输入项目的锚点矩形。
锚矩形常被各种文本编辑控件使用，比如文本预测弹窗，用于跟踪文本选择。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `anchorRectangle` 的变化，不要把它当作普通函数主动调用。

### `void animatingChanged()`

**作用与语义：**

当虚拟键盘被打开或关闭时，这点确实如此。
当键盘完全打开或关闭时，动画为假。当`animating` `true`且`visibility`为`true`打开键盘时。当`animating` `true`且`visibility`为假时，键盘关闭。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `animating` 的变化，不要把它当作普通函数主动调用。

### `void cursorRectangleChanged()`

**作用与语义：**

在窗口坐标中输入物品的光标矩形。
光标矩形常被各种文本编辑控件使用，比如文本预测弹窗，用于跟踪正在输入的文本。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `cursorRectangle` 的变化，不要把它当作普通函数主动调用。

### `void inputDirectionChanged(Qt::LayoutDirection newDirection)`

**作用与语义：**

当前输入方向。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `inputDirection` 的变化，不要把它当作普通函数主动调用。

### `void inputItemClipRectangleChanged()`

**作用与语义：**

输入窗口坐标中物品裁剪的矩形。
裁剪输入矩形常被各种输入法用来确定输入法可用的屏幕空间（例如虚拟键盘）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `inputItemClipRectangle` 的变化，不要把它当作普通函数主动调用。

### `void keyboardRectangleChanged()`

**作用与语义：**

虚拟键盘在窗口坐标中的几何体。
如果无法知道键盘的几何形状，这可能是一个空矩形。安卓上的浮动键盘就是这种情况。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `keyboardRectangle` 的变化，不要把它当作普通函数主动调用。

### `void localeChanged()`

**作用与语义：**

当前输入地点。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `locale` 的变化，不要把它当作普通函数主动调用。

### `void visibleChanged()`

**作用与语义：**

虚拟键盘在屏幕上的可见性。
对于没有虚拟键盘的设备，输入法的可见性依然为假。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `visible` 的变化，不要把它当作普通函数主动调用。

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

`QInputMethod` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
