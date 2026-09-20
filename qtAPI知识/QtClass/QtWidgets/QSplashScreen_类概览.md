# Qt QSplashScreen 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QSplashScreen>`
> 所属模块：`Qt6::Widgets`
> 继承：`QWidget`

## 它解决什么问题

`QSplashScreen` 用来在主窗口真正可用之前显示启动图和简短状态信息。它解决的是桌面程序启动阶段的反馈问题：初始化插件、加载资源、连接数据库、建立主窗口可能需要时间，用户需要知道程序已经开始工作，而不是误以为没有响应。

它不是进度对话框，也不是主界面的替代品。启动完成后，应调用 `finish(mainWindow)` 或主动关闭，让主窗口接管交互。

## 实际使用场景

- 大型桌面软件启动时显示品牌图、版本和加载状态。
- 初始化多个模块时通过 `showMessage()` 展示当前阶段。
- 多屏环境中把启动画面显示到指定 `QScreen`。
- 在主窗口创建完成前先给用户一个可见反馈。

如果初始化很快，启动屏可能反而制造闪烁；如果初始化很慢，则应考虑把耗时任务拆到后台线程，并提供可取消或更详细的进度 UI。

## 基本使用流程

常见流程是：先创建 `QApplication`，再创建带 pixmap 的 `QSplashScreen`，立即 `show()`，必要时调用 `QCoreApplication::processEvents()` 让窗口实际绘制；随后执行初始化步骤，期间用 `showMessage()` 更新状态；最后显示主窗口并调用 `finish(&mainWindow)`。

`finish(QWidget *w)` 会让启动屏在目标主窗口显示后结束，避免启动屏过早消失造成空白间隔。

## 消息绘制

`showMessage(message, alignment, color)` 在启动图上叠加一段文本。`alignment` 使用 Qt 对齐标志，例如左下、居中、右下；`color` 控制文字颜色。`messageChanged()` 会在消息变化时发出，适合测试或附加状态同步。

默认绘制不满足需求时，可以派生并重写 `drawContents(QPainter *painter)`。这适合自定义字体、阴影、进度条、版本号位置等场景。重写时要记住：背景 pixmap 和窗口本身仍由 `QSplashScreen` 管理，`drawContents()` 主要负责内容叠加。

## 交互与边界

默认情况下，用户点击启动屏会触发鼠标事件，Qt 的实现允许启动屏被隐藏。若产品要求启动阶段不能被点击隐藏，可以派生并重写 `mousePressEvent()`。

启动屏显示期间仍然是 GUI 线程窗口。不要在 GUI 线程里长时间阻塞而完全不处理事件，否则启动屏也无法刷新。短初始化阶段可以少量调用 `processEvents()`，更长任务应考虑线程、任务队列或异步初始化。

多屏构造函数 `QSplashScreen(QScreen *screen, ...)` 用来指定在哪块屏幕上显示。未指定时通常使用默认屏幕。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSplashScreen(const QPixmap &pixmap = QPixmap(), Qt::WindowFlags f = {})` | 用启动图创建 splash 窗口。 | 未指定屏幕时使用默认屏幕；flags 可调整窗口行为。 |
| 构造 | `QSplashScreen(QScreen *screen, const QPixmap &pixmap = QPixmap(), Qt::WindowFlags f = {})` | 在指定屏幕上创建 splash。 | 多屏应用可用它控制启动屏位置。 |
| 析构 | `~QSplashScreen()` | 销毁启动屏。 | 一般在主窗口显示后关闭或随对象生命周期结束。 |
| 图像 | `void setPixmap(const QPixmap &pixmap)` | 替换启动屏背景图。 | 图片尺寸会影响窗口视觉尺寸和布局感受。 |
| 图像 | `const QPixmap pixmap() const` | 返回当前背景图。 | 返回值是 pixmap 值，不是内部可修改引用。 |
| 结束 | `void finish(QWidget *mainWin)` | 在主窗口显示后关闭启动屏。 | `mainWin` 应是即将接管界面的主窗口。 |
| 刷新 | `void repaint()` | 立即重绘启动屏。 | 启动期间更新消息后可用；不要在高频循环滥用。 |
| 消息 | `QString message() const` | 返回当前显示的消息文本。 | 空字符串表示当前无消息。 |
| 消息 | `void showMessage(const QString &message, int alignment = Qt::AlignLeft, const QColor &color = Qt::black)` | 在启动屏上显示状态文本。 | 对齐是 Qt 对齐标志；颜色要与背景图有足够对比。 |
| 消息 | `void clearMessage()` | 清除当前状态文本。 | 会触发重新绘制和消息变化通知。 |
| 信号 | `void messageChanged(const QString &message)` | 消息文本变化时发出。 | 可用于测试、日志或外部状态同步。 |
| 绘制扩展 | `void drawContents(QPainter *painter)` | 自定义消息或叠加内容绘制。 | 派生类重写时保持绘制区域和高 DPI 显示效果。 |
| 事件 | `bool event(QEvent *event)` | 处理内部事件。 | 一般不需要重写，除非要深度定制行为。 |
| 鼠标 | `void mousePressEvent(QMouseEvent *)` | 处理点击启动屏。 | 想禁止点击隐藏时可在派生类中改写。 |

## 一句话总结

`QSplashScreen` 是启动阶段的轻量反馈窗口：显示一张图和几行状态，让主窗口准备好之后尽快退场。
