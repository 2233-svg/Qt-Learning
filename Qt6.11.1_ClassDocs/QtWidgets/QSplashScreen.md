# QSplashScreen

> Qt 6.11.1 · Qt Widgets · 来自 `QSplashScreen`

## 1. 先建立直觉

`QSplashScreen` 是应用启动期间的临时启动页。它给用户一个明确反馈：程序已经启动，正在加载资源、初始化插件、建立连接或恢复会话。它不是主窗口，也不应承担复杂交互。

一个好的 splash screen 解决的是“启动空白期”的不确定感；一个坏的 splash screen 会变成启动速度慢的遮羞布。使用它时，真正要关心的是启动流程拆分、事件循环保持响应、加载完成后可靠关闭。

## 2. 类说明

`QSplashScreen` 继承自 `QWidget`，通常用一张 `QPixmap` 做背景，并可以在上面绘制状态消息。它常在主窗口创建之前显示，等主窗口准备好后通过 `finish(mainWindow)` 关闭。

它支持指定 `QScreen`，这对多显示器环境有用：例如让启动页出现在用户启动应用的屏幕上，而不是默认主屏幕。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QSplashScreen(const QPixmap &, Qt::WindowFlags)` | 用图片创建启动页，常在 `main()` 中构造。 |
| `QSplashScreen(QScreen *, const QPixmap &, Qt::WindowFlags)` | 指定显示在哪块屏幕上，适合多屏应用。 |
| `setPixmap(const QPixmap &)` / `pixmap()` | 设置或读取启动页背景图。 |
| `showMessage(const QString &, int, const QColor &)` | 在启动页上显示当前加载步骤。 |
| `clearMessage()` | 清除当前文字消息。 |
| `message()` | 读取当前消息文本。 |
| `messageChanged(const QString &)` | 消息变化时发出，可用于日志或测试观察。 |
| `finish(QWidget *mainWin)` | 等主窗口显示后关闭启动页，是最常用的收尾方式。 |
| `repaint()` | 立即重绘启动页。启动阶段偶尔配合 `processEvents()` 使用。 |
| `drawContents(QPainter *)` | 子类化时自定义消息绘制方式。 |
| `mousePressEvent()` | 默认点击可隐藏或响应启动页；需要时可重写改变行为。 |

## 4. 典型启动流程

```cpp
int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QSplashScreen splash(QPixmap(":/images/splash.png"));
    splash.show();
    splash.showMessage("Loading plugins...", Qt::AlignBottom | Qt::AlignLeft, Qt::white);
    app.processEvents();

    MainWindow w;
    loadPlugins();
    splash.showMessage("Restoring workspace...", Qt::AlignBottom | Qt::AlignLeft, Qt::white);
    app.processEvents();

    w.show();
    splash.finish(&w);
    return app.exec();
}
```

这段代码的重点是：长初始化被拆成可报告的步骤，并在关键节点让事件循环处理绘制。否则 splash 已经 `show()`，但窗口可能来不及真正显示。

## 5. 使用场景

适合大型桌面软件、IDE、设计器、CAD/EDA 工具、加载插件很多的业务系统、需要恢复上次工作区的应用，以及启动时需要建立设备连接或读取大量配置的程序。

如果应用一两秒内就能启动，splash 可能没有必要。与其显示一个一闪而过的窗口，不如优化启动路径或直接显示主窗口骨架。

## 6. 常见坑与经验

不要把耗时工作一股脑塞在 GUI 线程且不处理事件。那样 splash 可能根本画不出来，用户看到的仍然是卡顿。

`showMessage()` 适合显示阶段性状态，不适合刷大量日志。启动页文字越多，越像错误控制台，也越难让用户快速理解当前状态。

`finish(mainWin)` 的语义是“主窗口出现后让启动页结束”。如果主窗口还没 show，或者传入的 widget 生命周期不清楚，启动页可能关闭时机不符合预期。
