# QVideoWidget

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QVideoWidget` 是 Qt Multimedia 的“视频Widget”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QVideoWidget` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QVideoWidget>`
- 继承自：QWidget
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS MultimediaWidgets)
target_link_libraries(mytarget PRIVATE Qt6::MultimediaWidgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 设备或媒体对象要在使用期间保持有效，开始前配置输入/输出和格式，停止后释放会话或解除设备占用。状态、媒体状态和错误信号共同决定下一步操作。

**状态与结果：** 区分无媒体、加载中、已加载、播放中、暂停、停止、结束和错误。进度、时长、缓冲和设备可用性不是同一个状态，不能只用一个 bool 表示。

**线程与事件循环：** 媒体对象通常依赖事件循环和平台线程边界；GUI 展示对象在 GUI 线程，后台处理要使用类明确支持的线程模型。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `aspectRatioMode : Qt::AspectRatioMode`
- `fullScreen : bool`

### 公有函数

- `QVideoWidget(QWidget *parent = nullptr)`
- `virtual ~QVideoWidget() override`
- `Qt::AspectRatioMode aspectRatioMode() const`
- `bool isFullScreen() const`
- `QVideoSink * videoSink() const`

### 重实现的公有函数

- `virtual QSize sizeHint() const override`

### 公有槽函数

- `void setAspectRatioMode(Qt::AspectRatioMode mode)`
- `void setFullScreen(bool fullScreen)`

### 信号

- `void aspectRatioModeChanged(Qt::AspectRatioMode mode)`
- `void fullScreenChanged(bool fullScreen)`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`
- `virtual void hideEvent(QHideEvent *event) override`
- `virtual void moveEvent(QMoveEvent *event) override`
- `virtual void resizeEvent(QResizeEvent *event) override`
- `virtual void showEvent(QShowEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `aspectRatioMode : Qt::AspectRatioMode`

**作用与语义：**

视频如何根据其宽高比进行缩放。

**如何使用：** 调用 `aspectRatioMode()` 读取当前值；它不会修改应用状态。

### `fullScreen : bool`

**作用与语义：**

无论视频显示仅限于窗口还是全屏显示，这一特性都适用。

**如何使用：** 调用 `fullScreen()` 读取当前值；它不会修改应用状态。

### `[explicit] QVideoWidget::QVideoWidget(QWidget *parent = nullptr)`

**作用与语义：**

构建一个新的视频小部件。
`parent`会传给`QWidget`。

### `[override virtual noexcept] QVideoWidget::~QVideoWidget()`

**作用与语义：**

毁坏了一个视频小部件。

### `[override virtual protected] bool QVideoWidget::event(QEvent *event)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。
当前事件`event`。返回基类 `QWidget::event`（`QEvent` *event）函数的值。

### `[override virtual protected] void QVideoWidget::hideEvent(QHideEvent *event)`

**作用与语义：**

重实现自：`QWidget::hideEvent`（QHideEvent *event）。
负责皮毛`event`。

### `[override virtual protected] void QVideoWidget::moveEvent(QMoveEvent *event)`

**作用与语义：**

重实现自：`QWidget::moveEvent`（QMoveEvent *event）。
他负责搬家`event`。

### `[override virtual protected] void QVideoWidget::resizeEvent(QResizeEvent *event)`

**作用与语义：**

重实现自：`QWidget::resizeEvent`（QResizeEvent *event）。
处理缩放的操作`event`。

### `[override virtual protected] void QVideoWidget::showEvent(QShowEvent *event)`

**作用与语义：**

重实现自：`QWidget::showEvent`（QShowEvent *event）。
负责演出`event`。

### `[override virtual] QSize QVideoWidget::sizeHint() const`

**作用与语义：**

重新实现属性访问函数：`QWidget::sizeHint`。
返回当前后端的大小提示（如果有的话），或者返回`QWidget`的大小提示。

### `[invokable] QVideoSink *QVideoWidget::videoSink() const`

**作用与语义：**

返回`QVideoSink`实例。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `Qt::AspectRatioMode aspectRatioMode() const`

**作用与语义：**

视频如何根据其宽高比进行缩放。

**如何使用：** 调用 `aspectRatioMode()` 读取当前值；它不会修改应用状态。

### `bool isFullScreen() const`

**作用与语义：**

无论视频显示仅限于窗口还是全屏显示，这一特性都适用。

**如何使用：** 调用 `isFullScreen()` 读取当前值；它不会修改应用状态。

### `void setAspectRatioMode(Qt::AspectRatioMode mode)`

**作用与语义：**

视频如何根据其宽高比进行缩放。

**如何使用：** 调用 `setAspectRatioMode(...)` 修改 `aspectRatioMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFullScreen(bool fullScreen)`

**作用与语义：**

无论视频显示仅限于窗口还是全屏显示，这一特性都适用。

**如何使用：** 调用 `setFullScreen(...)` 修改 `fullScreen`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void aspectRatioModeChanged(Qt::AspectRatioMode mode)`

**作用与语义：**

视频如何根据其宽高比进行缩放。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `aspectRatioMode` 的变化，不要把它当作普通函数主动调用。

### `void fullScreenChanged(bool fullScreen)`

**作用与语义：**

无论视频显示仅限于窗口还是全屏显示，这一特性都适用。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `fullScreen` 的变化，不要把它当作普通函数主动调用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

设备或媒体对象要在使用期间保持有效，开始前配置输入/输出和格式，停止后释放会话或解除设备占用。状态、媒体状态和错误信号共同决定下一步操作。

### 状态和错误边界

区分无媒体、加载中、已加载、播放中、暂停、停止、结束和错误。进度、时长、缓冲和设备可用性不是同一个状态，不能只用一个 bool 表示。

### 线程边界

媒体对象通常依赖事件循环和平台线程边界；GUI 展示对象在 GUI 线程，后台处理要使用类明确支持的线程模型。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QVideoWidget` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
