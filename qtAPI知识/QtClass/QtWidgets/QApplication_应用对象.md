# Qt QApplication 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QApplication>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QCoreApplication -> QGuiApplication -> QApplication`  
> 定位：Widgets 程序的全局应用对象

## 1. QApplication 解决什么问题

`QApplication` 是 Qt Widgets 程序的总入口。它负责把命令行参数、事件循环、窗口系统、输入设备、样式、字体、调色板和顶层窗口串起来。

```text
QCoreApplication
  └─ QGuiApplication
       └─ QApplication
```

三个层次可以这样理解：

- `QCoreApplication`：事件循环、事件投递、应用退出；
- `QGuiApplication`：窗口系统、屏幕、键盘鼠标、剪贴板、调色板；
- `QApplication`：Widgets 控件、控件样式、焦点、顶层窗口和 Widgets 级别的输入行为。

一个典型 Widgets 程序必须先创建 `QApplication`，再创建窗口，最后调用 `exec()` 进入事件循环。

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 一个完整的 Widgets 程序

```cpp
#include <QApplication>
#include <QLabel>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QLabel label("Hello Qt Widgets");
    label.resize(240, 80);
    label.show();

    return app.exec();
}
```

`QApplication app(argc, argv)` 要放在绝大多数 GUI 对象之前。它需要先初始化平台插件、字体、样式和事件分发环境；如果先创建控件再创建应用对象，程序通常会直接报错或出现未定义行为。

## 3. 核心使用模型

### 3.1 一个进程通常只需要一个 QApplication

`QApplication` 是应用级单例风格的对象，Qt 通过 `QCoreApplication::instance()` 保存当前应用对象。不要在同一个进程里为了不同窗口反复创建 `QApplication`。

### 3.2 `exec()` 才是 GUI 程序真正开始工作的地方

窗口显示出来并不等于程序已经开始处理交互。鼠标、键盘、重绘、定时器、异步信号和窗口系统消息都要依赖事件循环。

### 3.3 QApplication 不会接管你的所有对象

应用对象会管理 Qt 的全局 GUI 资源和它作为父对象拥有的对象，但并不会自动接管你创建的所有窗口、模型和业务对象。顶层窗口仍然应该明确自己的生命周期。

## 4. 事件循环和事件分发

### 4.1 `exec()`、`notify()`、`event()` 的分工

- `exec()`：启动应用的主事件循环；
- `notify()`：把事件送到目标 `QObject`；
- `event()`：处理发给 `QApplication` 自身的事件。

需要全局拦截事件时可以重写 `notify()`，但必须谨慎并调用基类实现；多数局部需求更适合用事件过滤器。

### 4.2 长时间任务不要堵在主线程

`QApplication` 所在主线程需要持续处理事件。耗时任务应移到工作线程，或者拆成不会阻塞事件循环的步骤。

## 5. 样式、字体和调色板

### 5.1 样式

```cpp
QApplication::setStyle("Fusion");
QStyle *style = QApplication::style();
```

样式会影响控件外观、尺寸策略、间距、滚动条、菜单和标准图标。只改一小部分时，优先考虑 `QProxyStyle` 或局部样式表。

### 5.2 全局字体和调色板

```cpp
QApplication::setFont(QFont("Microsoft YaHei", 10));
QApplication::setPalette(palette);
```

全局设置会影响后续创建的控件以及能够继承该设置的现有控件。需要只影响某一类控件时，可以传入类名。

### 5.3 样式表

```cpp
qApp->setStyleSheet("QPushButton { padding: 6px 12px; }");
```

应用级样式表会影响整个控件树，适合统一主题，不适合把所有局部规则都塞进去。

## 6. 输入参数与交互阈值

这些静态函数读取或修改用户交互的系统级阈值：

- `cursorFlashTime()`：文本光标闪烁周期；
- `doubleClickInterval()`：双击允许的时间间隔；
- `keyboardInputInterval()`：连续键盘输入的间隔；
- `startDragTime()`、`startDragDistance()`：判定拖拽开始的时间和距离；
- `wheelScrollLines()`：滚轮一次滚动的行数。

拖拽判断应该使用这些值，而不是硬编码。

## 7. 窗口、焦点和模态状态

- `activeWindow()`：当前活动顶层窗口；
- `focusWidget()`：当前拥有键盘焦点的控件；
- `activeModalWidget()`：当前活动的模态控件；
- `activePopupWidget()`：当前活动的弹出控件。

这些值粒度不同，不要混着用。

## 8. 典型场景

### 8.1 给应用设置统一主题

```cpp
QApplication app(argc, argv);
app.setStyleSheet(R"(
    QWidget { font-size: 10pt; }
    QPushButton { min-height: 28px; }
)");
```

### 8.2 监听应用焦点变化

```cpp
QObject::connect(&app, &QApplication::focusChanged,
                 [](QWidget *oldWidget, QWidget *newWidget) {
    Q_UNUSED(oldWidget);
    if (newWidget)
        qDebug() << newWidget->objectName();
});
```

### 8.3 弹出 Qt 关于对话框

```cpp
QApplication::aboutQt();
```

## 9. 常见误区

### 9.1 用 QCoreApplication 跑 QWidget

只要程序创建 QWidget，就应该使用 `QApplication`。

### 9.2 在主线程里做长时间工作

事件循环需要保持畅通，不能把界面线程当计算线程。

### 9.3 把 `qApp` 当成任意类型应用对象

在 `QApplication` 上下文里，`qApp` 是当前 `QApplication *`，但它并不能掩盖对象生命周期问题。

### 9.4 过早访问全局 GUI 状态

应用对象尚未构造完成时，很多全局 GUI 查询都没有可靠意义。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 属性 | `cursorFlashTime : int` | 读取或设置文本光标闪烁周期。 | 属于应用级交互参数。 |
| 属性 | `doubleClickInterval : int` | 读取或设置双击时间阈值。 | 自定义双击逻辑时优先使用它。 |
| 属性 | `keyboardInputInterval : int` | 读取或设置连续键盘输入间隔。 | 会影响按键连击判定。 |
| 属性 | `wheelScrollLines : int` | 读取或设置滚轮滚动行数。 | 只在支持 wheel 事件时可用。 |
| 属性 | `startDragTime : int` | 读取或设置拖拽启动时间阈值。 | 要和 `startDragDistance` 一起判断。 |
| 属性 | `startDragDistance : int` | 读取或设置拖拽启动距离阈值。 | 不要用固定常数替代平台设置。 |
| 属性 | `styleSheet : QString` | 读取或设置应用级样式表。 | 会影响整个控件树。 |
| 属性 | `autoSipEnabled : bool` | 控制是否自动显示软件输入面板。 | 主要面向触摸/嵌入式场景。 |
| 构造 | `QApplication(int &argc, char **argv, int = ApplicationFlags)` | 创建 Widgets 应用环境并处理启动参数。 | 每个进程通常只创建一个，而且要早于所有 QWidget。 |
| 析构 | `~QApplication()` | 销毁应用对象并清理 GUI 运行环境。 | 应用对象销毁后不要再访问窗口和全局 GUI 状态。 |
| 样式 | `style()` | 返回当前应用使用的 `QStyle`。 | 返回的是应用当前样式。 |
| 样式 | `setStyle(QStyle *style)` | 安装一个样式对象。 | 要确认样式对象生命周期。 |
| 样式 | `setStyle(const QString &style)` | 按名称创建并安装样式。 | 名称不存在时可能失败。 |
| 字体 | `font()` | 返回应用默认字体。 | 不带参数时是应用级默认字体。 |
| 字体 | `font(const QWidget *widget)` | 查询指定控件最终使用的字体。 | 适合检查控件实际字体。 |
| 字体 | `font(const char *className)` | 查询指定控件类的应用字体。 | 类名必须匹配 Qt 元对象名。 |
| 字体 | `setFont(const QFont &font, const char *className = nullptr)` | 设置应用或某类控件的字体。 | `className == nullptr` 影响范围更大。 |
| 字体 | `fontMetrics()` | 返回应用字体的旧式整数字体度量。 | Qt 6.0 起已弃用。 |
| 调色板 | `palette(const QWidget *widget)` | 查询指定控件的调色板。 | 返回的是控件层级解析后的结果。 |
| 调色板 | `palette(const char *className)` | 查询指定控件类的调色板。 | 用于检查类级别的颜色覆盖。 |
| 调色板 | `setPalette(const QPalette &, const char *className = nullptr)` | 设置应用或某类控件的调色板。 | 样式表和控件自身 palette 可能覆盖它。 |
| 窗口查询 | `allWidgets()` | 返回当前应用中所有已创建的 Widgets。 | 遍历时注意对象可能被删除。 |
| 窗口查询 | `topLevelWidgets()` | 返回所有顶层 Widgets。 | 顶层窗口不一定都可见。 |
| 窗口查询 | `activePopupWidget()` | 返回当前活动的弹出控件。 | 没有时返回 `nullptr`。 |
| 窗口查询 | `activeModalWidget()` | 返回当前活动的模态控件。 | 只表示当前模态层。 |
| 窗口查询 | `focusWidget()` | 返回当前拥有键盘焦点的控件。 | 没有焦点控件时返回 `nullptr`。 |
| 窗口查询 | `activeWindow()` | 返回当前活动的顶层窗口。 | 和 `focusWidget()` 粒度不同。 |
| 窗口查询 | `widgetAt(const QPoint &p)` | 按全局屏幕坐标返回最上层的控件。 | 传入的是全局坐标。 |
| 窗口查询 | `widgetAt(int x, int y)` | 用两个坐标值调用 `widgetAt(QPoint)`。 | 同样使用全局屏幕坐标。 |
| 窗口查询 | `topLevelAt(const QPoint &p)` | 按全局屏幕坐标返回所在的顶层窗口。 | 适合判断鼠标位于哪个窗口。 |
| 窗口查询 | `topLevelAt(int x, int y)` | 用两个坐标值调用 `topLevelAt(QPoint)`。 | 同样使用全局屏幕坐标。 |
| 窗口控制 | `closeAllWindows()` | 请求关闭所有顶层窗口。 | 不是强制销毁，窗口可以拒绝关闭。 |
| 窗口控制 | `setActiveWindow(QWidget *act)` | 旧式地请求某个窗口成为活动窗口。 | Qt 6.5 起弃用，优先用 `QWidget::activateWindow()`。 |
| 窗口控制 | `aboutQt()` | 显示 Qt 自身版本和版权信息对话框。 | 适合作为“关于 Qt”菜单项动作。 |
| 焦点通知 | `focusChanged(QWidget *old, QWidget *now)` | 在应用焦点控件发生变化时发出信号。 | 不要在槽里造成焦点循环。 |
| 事件分发 | `event(QEvent *)` | 处理发给 `QApplication` 自身的事件。 | 属于应用对象自身事件入口。 |
| 输入反馈 | `beep()` | 发出系统提示音。 | 表现由平台决定。 |
| 输入反馈 | `alert(QWidget *widget, int duration = 0)` | 提醒用户某个窗口需要关注。 | 平台可能通过闪烁任务栏等方式表现。 |
| 交互参数 | `setCursorFlashTime(int)` / `cursorFlashTime()` | 设置或读取光标闪烁周期。 | 通常应尊重系统默认值。 |
| 交互参数 | `setDoubleClickInterval(int)` / `doubleClickInterval()` | 设置或读取双击时间阈值。 | 自定义双击识别时使用当前值。 |
| 交互参数 | `setKeyboardInputInterval(int)` / `keyboardInputInterval()` | 设置或读取键盘输入间隔。 | 会影响连续输入行为。 |
| 交互参数 | `setWheelScrollLines(int)` / `wheelScrollLines()` | 设置或读取滚轮滚动行数。 | 受滚轮事件配置影响。 |
| 交互参数 | `setStartDragTime(int ms)` / `startDragTime()` | 设置或读取拖拽启动时间阈值。 | 与鼠标移动距离一起判断。 |
| 交互参数 | `setStartDragDistance(int l)` / `startDragDistance()` | 设置或读取拖拽启动距离阈值。 | 不要用固定常数替代平台设置。 |
| 键盘导航 | `setNavigationMode(Qt::NavigationMode mode)` | 设置键盘导航模式。 | 仅在启用 `QT_KEYPAD_NAVIGATION` 时可用。 |
| 键盘导航 | `navigationMode()` | 读取当前键盘导航模式。 | 仅在启用 `QT_KEYPAD_NAVIGATION` 时可用。 |
| 动画效果 | `isEffectEnabled(Qt::UIEffect effect)` | 查询指定 UI 效果是否启用。 | 平台设置可能影响默认值。 |
| 动画效果 | `setEffectEnabled(Qt::UIEffect effect, bool enable = true)` | 启用或禁用指定 UI 效果。 | 不要假设所有平台都支持相同效果。 |
| 事件循环 | `exec()` | 启动应用主事件循环并返回退出码。 | 主线程需要保持可响应。 |
| 事件分发 | `notify(QObject *, QEvent *)` | 把事件分发给目标对象。 | 全局重写时必须谨慎处理。 |
| 受保护函数 | `compressEvent(QEvent *, QObject *, QPostEventList *)` | 旧式地压缩待处理事件。 | Qt 6.10 起已弃用，Qt 7 将移除。 |
| 槽 | `setStyleSheet(const QString &sheet)` | 设置应用级样式表。 | 改动会影响整个控件树。 |
| 槽 | `setAutoSipEnabled(bool enabled)` | 设置是否自动显示软件输入面板。 | 更偏触摸/嵌入式场景。 |
| 宏 | `qApp` | 获取当前 `QApplication` 实例的便捷指针。 | 只能在应用对象已经创建后使用。 |

## 11. 一句话总结

`QApplication` 是 Widgets 程序的运行底座：先正确创建它，再依靠它的事件循环、窗口状态、输入阈值和全局样式资源让整个控件体系运转起来。
