# QStyleHints

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QStyleHints` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QStyleHints` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QStyleHints>`
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

- `(since 6.10) accessibility : const QAccessibilityHints*`
- `(since 6.5) colorScheme : Qt::ColorScheme`
- `(since 6.8) contextMenuTrigger : Qt::ContextMenuTrigger`
- `cursorFlashTime : int`
- `fontSmoothingGamma : const qreal`
- `(since 6.5) keyboardAutoRepeatRateF : const qreal`
- `keyboardInputInterval : int`
- `(since 6.10) menuSelectionWraps : const bool`
- `mouseDoubleClickDistance : const int`
- `mouseDoubleClickInterval : int`
- `mousePressAndHoldInterval : int`
- `mouseQuickSelectionThreshold : int`
- `passwordMaskCharacter : const QChar`
- `passwordMaskDelay : const int`
- `setFocusOnTouchRelease : const bool`
- `showIsFullScreen : const bool`
- `showIsMaximized : const bool`
- `showShortcutsInContextMenus : bool`
- `singleClickActivation : const bool`
- `startDragDistance : int`
- `startDragTime : int`
- `startDragVelocity : const int`
- `tabFocusBehavior : Qt::TabFocusBehavior`
- `touchDoubleTapDistance : const int`
- `useHoverEffects : bool`
- `useRtlExtensions : const bool`
- `wheelScrollLines : int`

### 公有函数

- `const QAccessibilityHints * accessibility() const`
- `Qt::ColorScheme colorScheme() const`
- `Qt::ContextMenuTrigger contextMenuTrigger() const`
- `int cursorFlashTime() const`
- `qreal fontSmoothingGamma() const`
- `qreal keyboardAutoRepeatRateF() const`
- `int keyboardInputInterval() const`
- `bool menuSelectionWraps() const`
- `int mouseDoubleClickDistance() const`
- `int mouseDoubleClickInterval() const`
- `int mousePressAndHoldInterval() const`
- `int mouseQuickSelectionThreshold() const`
- `QChar passwordMaskCharacter() const`
- `int passwordMaskDelay() const`
- `(since 6.8) void setColorScheme(Qt::ColorScheme scheme)`
- `void setContextMenuTrigger(Qt::ContextMenuTrigger contextMenuTrigger)`
- `bool setFocusOnTouchRelease() const`
- `void setShowShortcutsInContextMenus(bool showShortcutsInContextMenus)`
- `void setUseHoverEffects(bool useHoverEffects)`
- `bool showIsFullScreen() const`
- `bool showIsMaximized() const`
- `bool showShortcutsInContextMenus() const`
- `bool singleClickActivation() const`
- `int startDragDistance() const`
- `int startDragTime() const`
- `int startDragVelocity() const`
- `Qt::TabFocusBehavior tabFocusBehavior() const`
- `int touchDoubleTapDistance() const`
- `(since 6.8) void unsetColorScheme()`
- `bool useHoverEffects() const`
- `bool useRtlExtensions() const`
- `int wheelScrollLines() const`

### 信号

- `void colorSchemeChanged(Qt::ColorScheme colorScheme)`
- `void contextMenuTriggerChanged(Qt::ContextMenuTrigger contextMenuTrigger)`
- `void cursorFlashTimeChanged(int cursorFlashTime)`
- `void keyboardInputIntervalChanged(int keyboardInputInterval)`
- `void mouseDoubleClickIntervalChanged(int mouseDoubleClickInterval)`
- `void mousePressAndHoldIntervalChanged(int mousePressAndHoldInterval)`
- `void mouseQuickSelectionThresholdChanged(int threshold)`
- `void showShortcutsInContextMenusChanged(bool)`
- `void startDragDistanceChanged(int startDragDistance)`
- `void startDragTimeChanged(int startDragTime)`
- `void tabFocusBehaviorChanged(Qt::TabFocusBehavior tabFocusBehavior)`
- `void useHoverEffectsChanged(bool useHoverEffects)`
- `void wheelScrollLinesChanged(int scrollLines)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[read-only, since 6.10] accessibility : const QAccessibilityHints*`

**作用与语义：**

该属性包含应用的可访问性提示。
无障碍提示涵盖了基于平台的无障碍设置，例如用户是否希望应用处于高对比度。

**如何使用：** 调用 `accessibility()` 读取当前值；它不会修改应用状态。

### `[since 6.5] colorScheme : Qt::ColorScheme`

**作用与语义：**

该属性表示应用所使用的配色方案。
默认情况下，这遵循系统的默认配色方案（也称为外观），并在系统配色方案发生变化时（如黄昏或黎明时分）发生变化。将配色方案设置为显式值会覆盖系统设置，忽略系统配色方案的任何变更。不过，这样做是系统提示，且并非所有平台都支持覆盖配色方案。
重置该属性或设置为`Qt::ColorScheme::Unknown`，会移除覆盖，应用程序重新遵循系统默认状态。属性值会变为系统当前的配色方案。
当该属性发生变化时，Qt 会读取系统调色板并更新默认调色板，但不会覆盖应用程序明确设置的调色板条目。当 colorSchemeChange() 信号发出时，旧调色板仍然有效。
应选择应用特定颜色以配合有效调色板，同时考虑当前配色方案。当有效调色板变化时，要更新应用特定颜色，请处理`PaletteChange`或 `ApplicationPaletteChange` 事件。

**如何使用：** 调用 `colorScheme()` 读取当前值；它不会修改应用状态。

### `[since 6.8] contextMenuTrigger : Qt::ContextMenuTrigger`

**作用与语义：**

鼠标事件曾用于触发一个上下文菜单事件。
UNIX 系统的默认设置是鼠标按键事件显示上下文菜单，而在 Windows 上则显示鼠标按钮释放事件。该属性可用于覆盖默认平台行为。
注意：开发者必须非常谨慎地使用该属性，因为它会改变用户在所运行平台上预期的默认交互模式。

**如何使用：** 调用 `contextMenuTrigger()` 读取当前值；它不会修改应用状态。

### `[read-only] cursorFlashTime : int`

**作用与语义：**

该特性将文本光标的闪烁时间以毫秒计。
闪光时间是显示、反转和恢复插入点显示的时间。通常文本光标显示时间为光标闪光时间的一半，然后隐藏时间相同。

**如何使用：** 调用 `cursorFlashTime()` 读取当前值；它不会修改应用状态。

### `[read-only] fontSmoothingGamma : const qreal`

**作用与语义：**

该属性表示字体平滑中使用的伽马值。

**如何使用：** 调用 `fontSmoothingGamma()` 读取当前值；它不会修改应用状态。

### `[read-only, since 6.5] keyboardAutoRepeatRateF : const qreal`

**作用与语义：**

该特性表示，按住按键时，自动产生额外重复按键的速率（单位为每秒事件）。

**如何使用：** 调用 `keyboardAutoRepeatRateF()` 读取当前值；它不会修改应用状态。

### `[read-only] keyboardInputInterval : int`

**作用与语义：**

该特性具有时间限制（以毫秒计），用以区分按键与连续两次按键。

**如何使用：** 调用 `keyboardInputInterval()` 读取当前值；它不会修改应用状态。

### `[read-only, since 6.10] menuSelectionWraps : const bool`

**作用与语义：**

菜单选择环绕。
如果菜单选择被包裹，返回`true`。也就是说，在到达最后一个菜单项后，键导航是否会再次将选择移动到第一个菜单项，反之亦然。

**如何使用：** 调用 `menuSelectionWraps()` 读取当前值；它不会修改应用状态。

### `[read-only] mouseDoubleClickDistance : const int`

**作用与语义：**

该特性限制了鼠标在连续两次点击之间移动的最大距离（像素数），并且仍能被检测为双击。

**如何使用：** 调用 `mouseDoubleClickDistance()` 读取当前值；它不会修改应用状态。

### `[read-only] mouseDoubleClickInterval : int`

**作用与语义：**

该特性具有毫秒的时间限制，将双击点击与连续两次鼠标点击区分开来。

**如何使用：** 调用 `mouseDoubleClickInterval()` 读取当前值；它不会修改应用状态。

### `[read-only] mousePressAndHoldInterval : int`

**作用与语义：**

该特性将触发按按的时间限制（毫秒）限制。

**如何使用：** 调用 `mousePressAndHoldInterval()` 读取当前值；它不会修改应用状态。

### `mouseQuickSelectionThreshold : int`

**作用与语义：**

`QLineEdit` 快速选择鼠标阈值。
该属性定义了在正常`QLineEdit`文本选择中，鼠标光标沿Y轴移动多少，以触发快速选择。
如果属性值小于或等于0，快速选择功能将被禁用。

**如何使用：** 调用 `mouseQuickSelectionThreshold()` 读取当前值；它不会修改应用状态。

### `[read-only] passwordMaskCharacter : const QChar`

**作用与语义：**

该属性包含用于掩盖密码模式下输入文本输入字段字符的字符。

**如何使用：** 调用 `passwordMaskCharacter()` 读取当前值；它不会修改应用状态。

### `[read-only] passwordMaskDelay : const int`

**作用与语义：**

该特性表示输入信件在密码模式下以毫秒为单位显示在文本输入框中，毫秒级。

**如何使用：** 调用 `passwordMaskDelay()` 读取当前值；它不会修改应用状态。

### `[read-only] setFocusOnTouchRelease : const bool`

**作用与语义：**

该属性包含事件，应将输入焦点集中在焦点对象上。
如果焦点对象（如线编辑等）在触控/鼠标释放后应接收输入焦点，该属性`true`。这是触摸平台上的正常行为。在桌面平台上，标准是将焦点设置在触摸/鼠标按键上。

**如何使用：** 调用 `setFocusOnTouchRelease()` 读取当前值；它不会修改应用状态。

### `[read-only] showIsFullScreen : const bool`

**作用与语义：**

该属性适用于平台是否默认使用全屏窗口。
如果平台默认窗口是全屏，否则`false`，该属性`true`。
注意：平台仍可选择非全屏显示某些窗口，如弹窗或对话框。该属性仅报告默认行为。

**如何使用：** 调用 `showIsFullScreen()` 读取当前值；它不会修改应用状态。

### `[read-only] showIsMaximized : const bool`

**作用与语义：**

该属性决定平台默认最大化窗口。
如果平台默认最大化窗口，否则`false`，该属性`true`。
注意：平台仍可选择显示某些窗口未被最大化，如弹窗或对话框。该属性仅报告默认行为。

**如何使用：** 调用 `showIsMaximized()` 读取当前值；它不会修改应用状态。

### `showShortcutsInContextMenus : bool`

**作用与语义：**

`true`平台通常在上下文菜单中显示快捷键序列，否则`false`。
自Qt 5.13起，setShowShortcutsInContextMenus() 函数可用于覆盖平台默认值。

**如何使用：** 调用 `showShortcutsInContextMenus()` 读取当前值；它不会修改应用状态。

### `[read-only] singleClickActivation : const bool`

**作用与语义：**

无论物品是通过单击还是双击激活，这一特性都适用。
如果物品应该通过单击激活，`false`是否应该通过双击激活，这个属性`true`。

**如何使用：** 调用 `singleClickActivation()` 读取当前值；它不会修改应用状态。

### `[read-only] startDragDistance : int`

**作用与语义：**

该属性表示鼠标在按住按钮后移动的距离（像素单位），然后才会开始拖拽操作。
如果你在应用中支持拖放，并且想在用户按住按钮移动光标一定距离后启动拖放操作，你应该用该属性的值作为所需的最小距离。
例如，如果点击的鼠标位置存储在`startPos`中，当前位置（例如鼠标移动事件中）是`currentPos`，你可以通过以下代码判断是否应该开始拖动：

**如何使用：** 调用 `startDragDistance()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 if ((startPos - currentPos).manhattanLength() >=
         QApplication::startDragDistance())
     startTheDrag();
```

### `[read-only] startDragTime : int`

**作用与语义：**

该特性显示，按住鼠标按钮的时间（以毫秒计）才能开始拖放操作。
如果你的应用程序支持拖放，并且想在用户按住鼠标按键一定时间后启动拖放操作，你应该用该属性的值作为延迟。

**如何使用：** 调用 `startDragTime()` 读取当前值；它不会修改应用状态。

### `[read-only] startDragVelocity : const int`

**作用与语义：**

该属性限制了鼠标移动时按住按钮开始拖放操作的速度（像素每秒）。值为0表示没有这种限制。

**如何使用：** 调用 `startDragVelocity()` 读取当前值；它不会修改应用状态。

### `[read-only] tabFocusBehavior : Qt::TabFocusBehavior`

**作用与语义：**

该特性保持按Tab键时的焦点行为。
注意：不要在QML中绑定该值，因为变更通知信号尚未实现。

**如何使用：** 调用 `tabFocusBehavior()` 读取当前值；它不会修改应用状态。

### `[read-only] touchDoubleTapDistance : const int`

**作用与语义：**

该特性决定了手指在连续两次点击间移动的最大距离（像素单位），且仍能检测为双重点击。

**如何使用：** 调用 `touchDoubleTapDistance()` 读取当前值；它不会修改应用状态。

### `useHoverEffects : bool`

**作用与语义：**

该属性是否使用悬停效果，也适用UI元素。
如果 UI 元素应该使用悬浮效果，这个属性`true`。这是桌面平台上的标准行为，而在触摸平台上，悬浮事件传递的开销是可以避免的。

**如何使用：** 调用 `useHoverEffects()` 读取当前值；它不会修改应用状态。

### `[read-only] useRtlExtensions : const bool`

**作用与语义：**

该属性包含写作方向。
如果启用了右向左写入方向，否则`false`，该属性`true`。

**如何使用：** 调用 `useRtlExtensions()` 读取当前值；它不会修改应用状态。

### `[read-only] wheelScrollLines : int`

**作用与语义：**

每次轮子点击默认滚动的行数。

**如何使用：** 调用 `wheelScrollLines()` 读取当前值；它不会修改应用状态。

### `[since 6.8] void QStyleHints::setColorScheme(Qt::ColorScheme scheme)`

**作用与语义：**

该属性表示应用所使用的配色方案。
默认情况下，这遵循系统的默认配色方案（也称为外观），并在系统配色方案发生变化时（如黄昏或黎明时分）发生变化。将配色方案设置为显式值会覆盖系统设置，忽略系统配色方案的任何变更。不过，这样做是系统提示，且并非所有平台都支持覆盖配色方案。
重置该属性或设置为`Qt::ColorScheme::Unknown`，会移除覆盖，应用程序重新遵循系统默认状态。属性值会变为系统当前的配色方案。
当该属性发生变化时，Qt 会读取系统调色板并更新默认调色板，但不会覆盖应用程序明确设置的调色板条目。当 colorSchemeChange() 信号发出时，旧调色板仍然有效。
应选择应用特定颜色以配合有效调色板，同时考虑当前配色方案。当有效调色板变化时，要更新应用特定颜色，请处理`PaletteChange`或 `ApplicationPaletteChange` 事件。

**如何使用：** 调用 `setColorScheme(...)` 修改 `colorScheme`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[since 6.8] void QStyleHints::unsetColorScheme()`

**作用与语义：**

该属性表示应用所使用的配色方案。
默认情况下，这遵循系统的默认配色方案（也称为外观），并在系统配色方案发生变化时（如黄昏或黎明时分）发生变化。将配色方案设置为显式值会覆盖系统设置，忽略系统配色方案的任何变更。不过，这样做是系统提示，且并非所有平台都支持覆盖配色方案。
重置该属性或设置为`Qt::ColorScheme::Unknown`，会移除覆盖，应用程序重新遵循系统默认状态。属性值会变为系统当前的配色方案。
当该属性发生变化时，Qt 会读取系统调色板并更新默认调色板，但不会覆盖应用程序明确设置的调色板条目。当 colorSchemeChange() 信号发出时，旧调色板仍然有效。
应选择应用特定颜色以配合有效调色板，同时考虑当前配色方案。当有效调色板变化时，要更新应用特定颜色，请处理`PaletteChange`或 `ApplicationPaletteChange` 事件。

**如何使用：** 调用 `unsetColorScheme()` 读取当前值；它不会修改应用状态。

### `const QAccessibilityHints * accessibility() const`

**作用与语义：**

该属性包含应用的可访问性提示。
无障碍提示涵盖了基于平台的无障碍设置，例如用户是否希望应用处于高对比度。

**如何使用：** 调用 `accessibility()` 读取当前值；它不会修改应用状态。

### `Qt::ColorScheme colorScheme() const`

**作用与语义：**

该属性表示应用所使用的配色方案。
默认情况下，这遵循系统的默认配色方案（也称为外观），并在系统配色方案发生变化时（如黄昏或黎明时分）发生变化。将配色方案设置为显式值会覆盖系统设置，忽略系统配色方案的任何变更。不过，这样做是系统提示，且并非所有平台都支持覆盖配色方案。
重置该属性或设置为`Qt::ColorScheme::Unknown`，会移除覆盖，应用程序重新遵循系统默认状态。属性值会变为系统当前的配色方案。
当该属性发生变化时，Qt 会读取系统调色板并更新默认调色板，但不会覆盖应用程序明确设置的调色板条目。当 colorSchemeChange() 信号发出时，旧调色板仍然有效。
应选择应用特定颜色以配合有效调色板，同时考虑当前配色方案。当有效调色板变化时，要更新应用特定颜色，请处理`PaletteChange`或 `ApplicationPaletteChange` 事件。

**如何使用：** 调用 `colorScheme()` 读取当前值；它不会修改应用状态。

### `Qt::ContextMenuTrigger contextMenuTrigger() const`

**作用与语义：**

鼠标事件曾用于触发一个上下文菜单事件。
UNIX 系统的默认设置是鼠标按键事件显示上下文菜单，而在 Windows 上则显示鼠标按钮释放事件。该属性可用于覆盖默认平台行为。
注意：开发者必须非常谨慎地使用该属性，因为它会改变用户在所运行平台上预期的默认交互模式。

**如何使用：** 调用 `contextMenuTrigger()` 读取当前值；它不会修改应用状态。

### `int cursorFlashTime() const`

**作用与语义：**

该特性将文本光标的闪烁时间以毫秒计。
闪光时间是显示、反转和恢复插入点显示的时间。通常文本光标显示时间为光标闪光时间的一半，然后隐藏时间相同。

**如何使用：** 调用 `cursorFlashTime()` 读取当前值；它不会修改应用状态。

### `qreal fontSmoothingGamma() const`

**作用与语义：**

该属性表示字体平滑中使用的伽马值。

**如何使用：** 调用 `fontSmoothingGamma()` 读取当前值；它不会修改应用状态。

### `qreal keyboardAutoRepeatRateF() const`

**作用与语义：**

该特性表示，按住按键时，自动产生额外重复按键的速率（单位为每秒事件）。

**如何使用：** 调用 `keyboardAutoRepeatRateF()` 读取当前值；它不会修改应用状态。

### `int keyboardInputInterval() const`

**作用与语义：**

该特性具有时间限制（以毫秒计），用以区分按键与连续两次按键。

**如何使用：** 调用 `keyboardInputInterval()` 读取当前值；它不会修改应用状态。

### `bool menuSelectionWraps() const`

**作用与语义：**

菜单选择环绕。
如果菜单选择被包裹，返回`true`。也就是说，在到达最后一个菜单项后，键导航是否会再次将选择移动到第一个菜单项，反之亦然。

**如何使用：** 调用 `menuSelectionWraps()` 读取当前值；它不会修改应用状态。

### `int mouseDoubleClickDistance() const`

**作用与语义：**

该特性限制了鼠标在连续两次点击之间移动的最大距离（像素数），并且仍能被检测为双击。

**如何使用：** 调用 `mouseDoubleClickDistance()` 读取当前值；它不会修改应用状态。

### `int mouseDoubleClickInterval() const`

**作用与语义：**

该特性具有毫秒的时间限制，将双击点击与连续两次鼠标点击区分开来。

**如何使用：** 调用 `mouseDoubleClickInterval()` 读取当前值；它不会修改应用状态。

### `int mousePressAndHoldInterval() const`

**作用与语义：**

该特性将触发按按的时间限制（毫秒）限制。

**如何使用：** 调用 `mousePressAndHoldInterval()` 读取当前值；它不会修改应用状态。

### `int mouseQuickSelectionThreshold() const`

**作用与语义：**

`QLineEdit` 快速选择鼠标阈值。
该属性定义了在正常`QLineEdit`文本选择中，鼠标光标沿Y轴移动多少，以触发快速选择。
如果属性值小于或等于0，快速选择功能将被禁用。

**如何使用：** 调用 `mouseQuickSelectionThreshold()` 读取当前值；它不会修改应用状态。

### `QChar passwordMaskCharacter() const`

**作用与语义：**

该属性包含用于掩盖密码模式下输入文本输入字段字符的字符。

**如何使用：** 调用 `passwordMaskCharacter()` 读取当前值；它不会修改应用状态。

### `int passwordMaskDelay() const`

**作用与语义：**

该特性表示输入信件在密码模式下以毫秒为单位显示在文本输入框中，毫秒级。

**如何使用：** 调用 `passwordMaskDelay()` 读取当前值；它不会修改应用状态。

### `void setContextMenuTrigger(Qt::ContextMenuTrigger contextMenuTrigger)`

**作用与语义：**

鼠标事件曾用于触发一个上下文菜单事件。
UNIX 系统的默认设置是鼠标按键事件显示上下文菜单，而在 Windows 上则显示鼠标按钮释放事件。该属性可用于覆盖默认平台行为。
注意：开发者必须非常谨慎地使用该属性，因为它会改变用户在所运行平台上预期的默认交互模式。

**如何使用：** 调用 `setContextMenuTrigger(...)` 修改 `contextMenuTrigger`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool setFocusOnTouchRelease() const`

**作用与语义：**

该属性包含事件，应将输入焦点集中在焦点对象上。
如果焦点对象（如线编辑等）在触控/鼠标释放后应接收输入焦点，该属性`true`。这是触摸平台上的正常行为。在桌面平台上，标准是将焦点设置在触摸/鼠标按键上。

**如何使用：** 调用 `setFocusOnTouchRelease()` 读取当前值；它不会修改应用状态。

### `void setShowShortcutsInContextMenus(bool showShortcutsInContextMenus)`

**作用与语义：**

`true`平台通常在上下文菜单中显示快捷键序列，否则`false`。
自Qt 5.13起，setShowShortcutsInContextMenus() 函数可用于覆盖平台默认值。

**如何使用：** 调用 `setShowShortcutsInContextMenus(...)` 修改 `showShortcutsInContextMenus`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setUseHoverEffects(bool useHoverEffects)`

**作用与语义：**

该属性是否使用悬停效果，也适用UI元素。
如果 UI 元素应该使用悬浮效果，这个属性`true`。这是桌面平台上的标准行为，而在触摸平台上，悬浮事件传递的开销是可以避免的。

**如何使用：** 调用 `setUseHoverEffects(...)` 修改 `useHoverEffects`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool showIsFullScreen() const`

**作用与语义：**

该属性适用于平台是否默认使用全屏窗口。
如果平台默认窗口是全屏，否则`false`，该属性`true`。
注意：平台仍可选择非全屏显示某些窗口，如弹窗或对话框。该属性仅报告默认行为。

**如何使用：** 调用 `showIsFullScreen()` 读取当前值；它不会修改应用状态。

### `bool showIsMaximized() const`

**作用与语义：**

该属性决定平台默认最大化窗口。
如果平台默认最大化窗口，否则`false`，该属性`true`。
注意：平台仍可选择显示某些窗口未被最大化，如弹窗或对话框。该属性仅报告默认行为。

**如何使用：** 调用 `showIsMaximized()` 读取当前值；它不会修改应用状态。

### `bool showShortcutsInContextMenus() const`

**作用与语义：**

`true`平台通常在上下文菜单中显示快捷键序列，否则`false`。
自Qt 5.13起，setShowShortcutsInContextMenus() 函数可用于覆盖平台默认值。

**如何使用：** 调用 `showShortcutsInContextMenus()` 读取当前值；它不会修改应用状态。

### `bool singleClickActivation() const`

**作用与语义：**

无论物品是通过单击还是双击激活，这一特性都适用。
如果物品应该通过单击激活，`false`是否应该通过双击激活，这个属性`true`。

**如何使用：** 调用 `singleClickActivation()` 读取当前值；它不会修改应用状态。

### `int startDragDistance() const`

**作用与语义：**

该属性表示鼠标在按住按钮后移动的距离（像素单位），然后才会开始拖拽操作。
如果你在应用中支持拖放，并且想在用户按住按钮移动光标一定距离后启动拖放操作，你应该用该属性的值作为所需的最小距离。
例如，如果点击的鼠标位置存储在`startPos`中，当前位置（例如鼠标移动事件中）是`currentPos`，你可以通过以下代码判断是否应该开始拖动：

**如何使用：** 调用 `startDragDistance()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 if ((startPos - currentPos).manhattanLength() >=
         QApplication::startDragDistance())
     startTheDrag();
```

### `int startDragTime() const`

**作用与语义：**

该特性显示，按住鼠标按钮的时间（以毫秒计）才能开始拖放操作。
如果你的应用程序支持拖放，并且想在用户按住鼠标按键一定时间后启动拖放操作，你应该用该属性的值作为延迟。

**如何使用：** 调用 `startDragTime()` 读取当前值；它不会修改应用状态。

### `int startDragVelocity() const`

**作用与语义：**

该属性限制了鼠标移动时按住按钮开始拖放操作的速度（像素每秒）。值为0表示没有这种限制。

**如何使用：** 调用 `startDragVelocity()` 读取当前值；它不会修改应用状态。

### `Qt::TabFocusBehavior tabFocusBehavior() const`

**作用与语义：**

该特性保持按Tab键时的焦点行为。
注意：不要在QML中绑定该值，因为变更通知信号尚未实现。

**如何使用：** 调用 `tabFocusBehavior()` 读取当前值；它不会修改应用状态。

### `int touchDoubleTapDistance() const`

**作用与语义：**

该特性决定了手指在连续两次点击间移动的最大距离（像素单位），且仍能检测为双重点击。

**如何使用：** 调用 `touchDoubleTapDistance()` 读取当前值；它不会修改应用状态。

### `bool useHoverEffects() const`

**作用与语义：**

该属性是否使用悬停效果，也适用UI元素。
如果 UI 元素应该使用悬浮效果，这个属性`true`。这是桌面平台上的标准行为，而在触摸平台上，悬浮事件传递的开销是可以避免的。

**如何使用：** 调用 `useHoverEffects()` 读取当前值；它不会修改应用状态。

### `bool useRtlExtensions() const`

**作用与语义：**

该属性包含写作方向。
如果启用了右向左写入方向，否则`false`，该属性`true`。

**如何使用：** 调用 `useRtlExtensions()` 读取当前值；它不会修改应用状态。

### `int wheelScrollLines() const`

**作用与语义：**

每次轮子点击默认滚动的行数。

**如何使用：** 调用 `wheelScrollLines()` 读取当前值；它不会修改应用状态。

### `void colorSchemeChanged(Qt::ColorScheme colorScheme)`

**作用与语义：**

该属性表示应用所使用的配色方案。
默认情况下，这遵循系统的默认配色方案（也称为外观），并在系统配色方案发生变化时（如黄昏或黎明时分）发生变化。将配色方案设置为显式值会覆盖系统设置，忽略系统配色方案的任何变更。不过，这样做是系统提示，且并非所有平台都支持覆盖配色方案。
重置该属性或设置为`Qt::ColorScheme::Unknown`，会移除覆盖，应用程序重新遵循系统默认状态。属性值会变为系统当前的配色方案。
当该属性发生变化时，Qt 会读取系统调色板并更新默认调色板，但不会覆盖应用程序明确设置的调色板条目。当 colorSchemeChange() 信号发出时，旧调色板仍然有效。
应选择应用特定颜色以配合有效调色板，同时考虑当前配色方案。当有效调色板变化时，要更新应用特定颜色，请处理`PaletteChange`或 `ApplicationPaletteChange` 事件。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `colorScheme` 的变化，不要把它当作普通函数主动调用。

### `void contextMenuTriggerChanged(Qt::ContextMenuTrigger contextMenuTrigger)`

**作用与语义：**

鼠标事件曾用于触发一个上下文菜单事件。
UNIX 系统的默认设置是鼠标按键事件显示上下文菜单，而在 Windows 上则显示鼠标按钮释放事件。该属性可用于覆盖默认平台行为。
注意：开发者必须非常谨慎地使用该属性，因为它会改变用户在所运行平台上预期的默认交互模式。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `contextMenuTrigger` 的变化，不要把它当作普通函数主动调用。

### `void cursorFlashTimeChanged(int cursorFlashTime)`

**作用与语义：**

该特性将文本光标的闪烁时间以毫秒计。
闪光时间是显示、反转和恢复插入点显示的时间。通常文本光标显示时间为光标闪光时间的一半，然后隐藏时间相同。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `cursorFlashTime` 的变化，不要把它当作普通函数主动调用。

### `void keyboardInputIntervalChanged(int keyboardInputInterval)`

**作用与语义：**

该特性具有时间限制（以毫秒计），用以区分按键与连续两次按键。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `keyboardInputInterval` 的变化，不要把它当作普通函数主动调用。

### `void mouseDoubleClickIntervalChanged(int mouseDoubleClickInterval)`

**作用与语义：**

该特性具有毫秒的时间限制，将双击点击与连续两次鼠标点击区分开来。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `mouseDoubleClickInterval` 的变化，不要把它当作普通函数主动调用。

### `void mousePressAndHoldIntervalChanged(int mousePressAndHoldInterval)`

**作用与语义：**

该特性将触发按按的时间限制（毫秒）限制。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `mousePressAndHoldInterval` 的变化，不要把它当作普通函数主动调用。

### `void mouseQuickSelectionThresholdChanged(int threshold)`

**作用与语义：**

`QLineEdit` 快速选择鼠标阈值。
该属性定义了在正常`QLineEdit`文本选择中，鼠标光标沿Y轴移动多少，以触发快速选择。
如果属性值小于或等于0，快速选择功能将被禁用。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `mouseQuickSelectionThreshold` 的变化，不要把它当作普通函数主动调用。

### `void showShortcutsInContextMenusChanged(bool)`

**作用与语义：**

`true`平台通常在上下文菜单中显示快捷键序列，否则`false`。
自Qt 5.13起，setShowShortcutsInContextMenus() 函数可用于覆盖平台默认值。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `showShortcutsInContextMenus` 的变化，不要把它当作普通函数主动调用。

### `void startDragDistanceChanged(int startDragDistance)`

**作用与语义：**

该属性表示鼠标在按住按钮后移动的距离（像素单位），然后才会开始拖拽操作。
如果你在应用中支持拖放，并且想在用户按住按钮移动光标一定距离后启动拖放操作，你应该用该属性的值作为所需的最小距离。
例如，如果点击的鼠标位置存储在`startPos`中，当前位置（例如鼠标移动事件中）是`currentPos`，你可以通过以下代码判断是否应该开始拖动：

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `startDragDistance` 的变化，不要把它当作普通函数主动调用。

**官方示例：**

```cpp
 if ((startPos - currentPos).manhattanLength() >=
         QApplication::startDragDistance())
     startTheDrag();
```

### `void startDragTimeChanged(int startDragTime)`

**作用与语义：**

该特性显示，按住鼠标按钮的时间（以毫秒计）才能开始拖放操作。
如果你的应用程序支持拖放，并且想在用户按住鼠标按键一定时间后启动拖放操作，你应该用该属性的值作为延迟。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `startDragTime` 的变化，不要把它当作普通函数主动调用。

### `void tabFocusBehaviorChanged(Qt::TabFocusBehavior tabFocusBehavior)`

**作用与语义：**

该特性保持按Tab键时的焦点行为。
注意：不要在QML中绑定该值，因为变更通知信号尚未实现。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `tabFocusBehavior` 的变化，不要把它当作普通函数主动调用。

### `void useHoverEffectsChanged(bool useHoverEffects)`

**作用与语义：**

该属性是否使用悬停效果，也适用UI元素。
如果 UI 元素应该使用悬浮效果，这个属性`true`。这是桌面平台上的标准行为，而在触摸平台上，悬浮事件传递的开销是可以避免的。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `useHoverEffects` 的变化，不要把它当作普通函数主动调用。

### `void wheelScrollLinesChanged(int scrollLines)`

**作用与语义：**

每次轮子点击默认滚动的行数。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `wheelScrollLines` 的变化，不要把它当作普通函数主动调用。

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

`QStyleHints` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
