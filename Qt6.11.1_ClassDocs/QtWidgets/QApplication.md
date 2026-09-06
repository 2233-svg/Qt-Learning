# QApplication

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QApplication` 是 Qt Widgets 应用程序的全局入口，管理桌面平台资源、控件风格、输入事件和主事件循环。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QApplication` 是 Qt Widgets 应用程序的全局入口，管理桌面平台资源、控件风格、输入事件和主事件循环。

**内部模型：** 它不是某个窗口的父类，而是整个 Widgets 进程的应用对象。所有 QWidget 都应在 QApplication 创建后使用，并且通常在主线程中创建。

**适用场景：** 任何使用 QWidget、QMainWindow、QDialog 或标准桌面控件的程序都应先创建 QApplication。

**典型调用链：** 构造 QApplication -> 创建主窗口/控件 -> show() -> app.exec() -> 退出时由栈对象清理。

**先记住的坑：** 不要在 QApplication 前创建 QWidget；不要在 GUI 线程执行耗时循环；高 DPI、平台风格和命令行参数应在构造或显示窗口前配置。

## 2. 依赖与对象关系

- 头文件：`#include <QApplication>`
- 继承自：QGuiApplication
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

它不是某个窗口的父类，而是整个 Widgets 进程的应用对象。所有 QWidget 都应在 QApplication 创建后使用，并且通常在主线程中创建。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

任何使用 QWidget、QMainWindow、QDialog 或标准桌面控件的程序都应先创建 QApplication。 使用时通常按这个过程组织：构造 QApplication -> 创建主窗口/控件 -> show() -> app.exec() -> 退出时由栈对象清理。

```cpp
#include <QApplication>
#include <QMainWindow>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QMainWindow window;
    window.resize(800, 600);
    window.show();
    return app.exec();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `autoSipEnabled : bool`
- `cursorFlashTime : int`
- `doubleClickInterval : int`
- `keyboardInputInterval : int`
- `startDragDistance : int`
- `startDragTime : int`
- `styleSheet : QString`
- `wheelScrollLines : int`

### 公有函数

- `QApplication(int &argc, char **argv)`
- `virtual ~QApplication()`
- `bool autoSipEnabled() const`
- `QString styleSheet() const`

### 重实现的公有函数

- `virtual bool notify(QObject *receiver, QEvent *e) override`

### 公有槽函数

- `void aboutQt()`
- `void closeAllWindows()`
- `void setAutoSipEnabled(const bool enabled)`
- `void setStyleSheet(const QString &sheet)`

### 信号

- `void focusChanged(QWidget *old, QWidget *now)`

### 静态公有成员

- `QWidget * activeModalWidget()`
- `QWidget * activePopupWidget()`
- `QWidget * activeWindow()`
- `void alert(QWidget *widget, int msec = 0)`
- `QWidgetList allWidgets()`
- `void beep()`
- `int cursorFlashTime()`
- `int doubleClickInterval()`
- `int exec()`
- `QWidget * focusWidget()`
- `QFont font()`
- `QFont font(const QWidget *widget)`
- `QFont font(const char *className)`
- `bool isEffectEnabled(Qt::UIEffect effect)`
- `int keyboardInputInterval()`
- `Qt::NavigationMode navigationMode()`
- `QPalette palette(const QWidget *widget)`
- `QPalette palette(const char *className)`
- `void setCursorFlashTime(int)`
- `void setDoubleClickInterval(int)`
- `void setEffectEnabled(Qt::UIEffect effect, bool enable = true)`
- `void setFont(const QFont &font, const char *className = nullptr)`
- `void setKeyboardInputInterval(int)`
- `void setNavigationMode(Qt::NavigationMode mode)`
- `void setPalette(const QPalette &palette, const char *className = nullptr)`
- `void setStartDragDistance(int l)`
- `void setStartDragTime(int ms)`
- `void setStyle(QStyle *style)`
- `QStyle * setStyle(const QString &style)`
- `void setWheelScrollLines(int)`
- `int startDragDistance()`
- `int startDragTime()`
- `QStyle * style()`
- `QWidget * topLevelAt(const QPoint &point)`
- `QWidget * topLevelAt(int x, int y)`
- `QWidgetList topLevelWidgets()`
- `int wheelScrollLines()`
- `QWidget * widgetAt(const QPoint &point)`
- `QWidget * widgetAt(int x, int y)`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`

### 公开宏

- `qApp`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 59 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `autoSipEnabled : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QApplication` 的配置属性。初始化或状态切换时通过 `setAutoSipEnabled(...)` 设置，之后用 `autoSipEnabled()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`autoSipEnabled`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `cursorFlashTime : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QApplication` 的配置属性。初始化或状态切换时通过 `setCursorFlashTime(...)` 设置，之后用 `cursorFlashTime()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`cursorFlashTime`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `doubleClickInterval : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QApplication` 的配置属性。初始化或状态切换时通过 `setDoubleClickInterval(...)` 设置，之后用 `doubleClickInterval()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`doubleClickInterval`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `keyboardInputInterval : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QApplication` 的配置属性。初始化或状态切换时通过 `setKeyboardInputInterval(...)` 设置，之后用 `keyboardInputInterval()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`keyboardInputInterval`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `startDragDistance : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QApplication` 的配置属性。初始化或状态切换时通过 `setStartDragDistance(...)` 设置，之后用 `startDragDistance()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`startDragDistance`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `startDragTime : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QApplication` 的配置属性。初始化或状态切换时通过 `setStartDragTime(...)` 设置，之后用 `startDragTime()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`startDragTime`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `styleSheet : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QApplication` 的配置属性。初始化或状态切换时通过 `setStyleSheet(...)` 设置，之后用 `styleSheet()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`styleSheet`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `wheelScrollLines : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QApplication` 的配置属性。初始化或状态切换时通过 `setWheelScrollLines(...)` 设置，之后用 `wheelScrollLines()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`wheelScrollLines`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QApplication::QApplication(int &argc, char **argv)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QApplication` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `argc`：类型为 `int &`。没有默认值，调用时必须提供。传入 `int &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `argv`：类型为 `char **`。没有默认值，调用时必须提供。传入 `char **` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QApplication::~QApplication()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QApplication` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static slot] void QApplication::aboutQt()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `aboutQt`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QWidget *QApplication::activeModalWidget()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `activeModalWidget`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QWidget *QApplication::activePopupWidget()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `activePopupWidget`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QWidget *QApplication::activeWindow()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `activeWindow`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QApplication::alert(QWidget *widget, int msec = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `alert`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。
- 参数 `msec`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QWidgetList QApplication::allWidgets()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `allWidgets`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QWidgetList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QApplication::beep()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `beep`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static slot] void QApplication::closeAllWindows()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `closeAllWindows`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QApplication::event(QEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QApplication::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `e`：类型为 `QEvent *`。没有默认值，调用时必须提供。传入 `QEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] int QApplication::exec()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `exec`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QApplication::focusChanged(QWidget *old, QWidget *now)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QApplication` 发出的通知信号 `focusChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `old`：类型为 `QWidget *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `now`：类型为 `QWidget *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QWidget *QApplication::focusWidget()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `focusWidget`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QFont QApplication::font()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `font`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QFont`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QFont QApplication::font(const QWidget *widget)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `font`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QFont`。
- 参数 `widget`：类型为 `const QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QFont QApplication::font(const char *className)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `font`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QFont`。
- 参数 `className`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QApplication::isEffectEnabled(Qt::UIEffect effect)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isEffectEnabled`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `effect`：类型为 `Qt::UIEffect`。没有默认值，调用时必须提供。传入 `Qt::UIEffect` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] Qt::NavigationMode QApplication::navigationMode()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `navigationMode`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`Qt::NavigationMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QApplication::notify(QObject *receiver, QEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QApplication::notify` 用于计算、查询或取得与“notify”相关的操作。调用时要先确认当前状态和 `receiver`、`e` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `receiver`：类型为 `QObject *`。没有默认值，调用时必须提供。接收者对象。它决定槽函数所属线程和连接生命周期，必须在回调使用期间有效。
- 参数 `e`：类型为 `QEvent *`。没有默认值，调用时必须提供。传入 `QEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QPalette QApplication::palette(const QWidget *widget)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `palette`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QPalette`。
- 参数 `widget`：类型为 `const QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QPalette QApplication::palette(const char *className)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `palette`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QPalette`。
- 参数 `className`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QApplication::setEffectEnabled(Qt::UIEffect effect, bool enable = true)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setEffectEnabled`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `effect`：类型为 `Qt::UIEffect`。没有默认值，调用时必须提供。传入 `Qt::UIEffect` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `enable`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QApplication::setFont(const QFont &font, const char *className = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setFont`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `font`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `className`：类型为 `const char *`。默认值为 `nullptr`。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QApplication::setNavigationMode(Qt::NavigationMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setNavigationMode`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `Qt::NavigationMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QApplication::setPalette(const QPalette &palette, const char *className = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setPalette`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `palette`：类型为 `const QPalette &`。没有默认值，调用时必须提供。传入 `const QPalette &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `className`：类型为 `const char *`。默认值为 `nullptr`。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QApplication::setStyle(QStyle *style)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setStyle`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `style`：类型为 `QStyle *`。没有默认值，调用时必须提供。传入 `QStyle *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QStyle *QApplication::setStyle(const QString &style)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setStyle`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QStyle *`。
- 参数 `style`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QStyle *QApplication::style()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `style`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QStyle *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QWidget *QApplication::topLevelAt(const QPoint &point)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `topLevelAt`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数 `point`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QWidget *QApplication::topLevelAt(int x, int y)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `topLevelAt`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QWidgetList QApplication::topLevelWidgets()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `topLevelWidgets`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QWidgetList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QWidget *QApplication::widgetAt(const QPoint &point)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `widgetAt`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数 `point`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QWidget *QApplication::widgetAt(int x, int y)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `widgetAt`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qApp`

**API 类别：** 宏说明

**中文解读：** 这是 `QApplication` 的 `q、App` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool autoSipEnabled() const`

**API 类别：** 公有函数

**中文解读：** `QApplication::autoSipEnabled` 用于计算、查询或取得与“auto、Sip、启用状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString styleSheet() const`

**API 类别：** 公有函数

**中文解读：** `QApplication::styleSheet` 用于计算、查询或取得与“style、Sheet”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAutoSipEnabled(const bool enabled)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setAutoSipEnabled`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `enabled`：类型为 `const bool`。没有默认值，调用时必须提供。传入 `const bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setStyleSheet(const QString &sheet)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setStyleSheet`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `sheet`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int cursorFlashTime()`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `cursorFlashTime`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int doubleClickInterval()`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `doubleClickInterval`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int keyboardInputInterval()`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `keyboardInputInterval`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setCursorFlashTime(int)`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `setCursorFlashTime`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `int`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDoubleClickInterval(int)`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `setDoubleClickInterval`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `int`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setKeyboardInputInterval(int)`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `setKeyboardInputInterval`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `int`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setStartDragDistance(int l)`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `setStartDragDistance`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `l`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setStartDragTime(int ms)`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `setStartDragTime`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `ms`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setWheelScrollLines(int)`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `setWheelScrollLines`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `int`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int startDragDistance()`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `startDragDistance`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int startDragTime()`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `startDragTime`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int wheelScrollLines()`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `wheelScrollLines`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要在 QApplication 前创建 QWidget；不要在 GUI 线程执行耗时循环；高 DPI、平台风格和命令行参数应在构造或显示窗口前配置。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QApplication` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
