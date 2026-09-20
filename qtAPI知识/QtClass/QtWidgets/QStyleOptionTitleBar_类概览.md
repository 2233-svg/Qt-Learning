# Qt QStyleOptionTitleBar 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QStyleOptionTitleBar>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionComplex -> QStyleOptionTitleBar`  
> 定位：为 `QMdiSubWindow` 等客户端标题栏提供图标、标题、窗口功能与窗口状态的绘制快照

## 1. 它不是操作系统标题栏控制器

`QStyleOptionTitleBar` 不会修改 Windows、macOS 或 Linux 窗口管理器绘制的原生标题栏。Qt 文档中，它主要作为 `QStyle` 绘制 `QMdiSubWindow` 客户端标题栏的数据对象。

```text
QMdiArea
  └─ QMdiSubWindow
       ├─ 标题栏：图标、标题、窗口按钮
       ├─ 中心区域：内部 widget
       └─ style option
            └─ QStyleOptionTitleBar
                 └─ QStyle::drawComplexControl(CC_TitleBar, ...)
```

`QMdiSubWindow` 是 MDI 区域中的子窗口，它的标题栏、窗口装饰、内部 widget 和可能的 size grip 都由 Qt Widgets 自己管理，因而可以交由 `QStyle` 绘制。普通顶级窗口的原生非客户区通常由操作系统处理，不能期待改一个 `QStyleOptionTitleBar` 就改变它。

本类的使用场景：

- 自定义 `QMdiSubWindow` 或自定义 style 的标题栏视觉；
- 通过 `subControlRect()` 查询标题文字、关闭、最小化、最大化、还原、系统菜单等区域；
- 在 `QProxyStyle` 中根据窗口允许的功能与当前状态选择怎样画按钮。

它没有 QObject 生命周期和所有权；一般在栈上创建，用完即销毁。

## 2. 标题栏为何是复杂控件

标题栏不是一段文字加一个关闭图标，而是一组独立命中的子控件：

```text
[应用图标] [窗口标题........................] [_] [□] [x]
    sys menu          label                 min max close
```

`QStyle::CC_TitleBar` 对应的常用子控件包括：

| 子控件 | 作用 |
| --- | --- |
| `SC_TitleBarSysMenu` | 系统菜单入口 |
| `SC_TitleBarLabel` | 窗口图标与标题文字所在区域 |
| `SC_TitleBarMinButton` | 最小化按钮 |
| `SC_TitleBarMaxButton` | 最大化按钮 |
| `SC_TitleBarNormalButton` | 从最大化或最小化状态恢复的按钮 |
| `SC_TitleBarCloseButton` | 关闭按钮 |
| `SC_TitleBarShadeButton` / `SC_TitleBarUnshadeButton` | 折叠到仅显示标题栏、或从该状态恢复 |
| `SC_TitleBarContextHelpButton` | 上下文帮助按钮 |

这些子控件是否出现、位置在哪里、哪个显示为按下或悬停，不能仅由你看到的一张静态截图决定。它依赖 `titleBarFlags`、`titleBarState`、继承的 `subControls`、`activeSubControls`、`state` 和当前 style。

## 3. 最关键的分界：允许什么 vs 当前是什么

### 3.1 `titleBarFlags`：窗口允许哪些能力

`titleBarFlags` 是 `Qt::WindowFlags`，通常反映窗口类型和窗口功能提示，例如是否允许最小化、最大化、关闭、上下文帮助等。

```text
WindowMinimizeButtonHint -> style 可以提供最小化按钮
WindowMaximizeButtonHint -> style 可以提供最大化按钮
WindowCloseButtonHint    -> style 可以提供关闭按钮
WindowContextHelpButtonHint -> style 可以提供帮助按钮
```

这是一组“该窗口具备何种窗口装饰/功能”的描述。它不表示用户现在正按着哪个按钮，也不代表窗口当前是否最大化。

### 3.2 `titleBarState`：窗口当前处于什么状态

`titleBarState` 是 `int` 字段，但语义上保存底层 widget 的窗口状态位组合，即 `Qt::WindowStates`，例如：

```text
Qt::WindowNoState
Qt::WindowMinimized
Qt::WindowMaximized
Qt::WindowFullScreen
Qt::WindowActive
```

样式用它决定最大化按钮是否应变为“还原”按钮，或标题栏采用活动/非活动外观。它是当前状态，而非功能许可。

```text
titleBarFlags 包含 MaximizeButtonHint
titleBarState 包含 WindowMaximized
  -> 常见结果：显示 SC_TitleBarNormalButton（还原）而非最大化按钮
```

不要手工把两者混为同一个位集合。改变真实窗口功能应使用 `setWindowFlags()`；改变真实窗口状态应使用 `showMaximized()`、`showNormal()`、`showMinimized()` 等 API。修改 option 字段只影响随后的这一次样式绘制。

## 4. 标准用法：交给 style 计算每个按钮的矩形

在自定义 MDI 标题栏绘制中，先取得完整 option，再让 style 绘制基础部分：

```cpp
void MdiTitleStyle::drawComplexControl(
    QStyle::ComplexControl control,
    const QStyleOptionComplex *option,
    QPainter *painter,
    const QWidget *widget) const
{
    if (control == QStyle::CC_TitleBar) {
        const auto *titleBar =
            qstyleoption_cast<const QStyleOptionTitleBar *>(option);

        if (titleBar) {
            const QRect closeRect = subControlRect(
                QStyle::CC_TitleBar,
                titleBar,
                QStyle::SC_TitleBarCloseButton,
                widget);
            drawCloseHoverAccent(closeRect, painter);
        }
    }

    QProxyStyle::drawComplexControl(control, option, painter, widget);
}
```

不要根据标题栏总宽度写死“最后 36 像素是关闭按钮”。平台主题、按钮顺序、DPI、RTL、是否有系统菜单、是否允许最大化以及 shade 支持都会改变这些矩形。

`QMdiSubWindow` 自己会把真实窗口标题、图标、窗口标志、状态和交互状态填入 option。自定义控件或 style 应读取这份数据，而不是重新猜一遍。

## 5. 公开字段各自做什么

### 5.1 `text` 与 `icon`

`text` 是标题栏要绘制的标题，`icon` 是标题栏图标。它们通常来自内部窗口的 `windowTitle` 与 `windowIcon`。

```cpp
option.text = "文档 1";
option.icon = QIcon(":/icons/document.svg");
```

这只影响随后使用该 option 的绘制。不会修改实际窗口标题、任务栏文字、系统菜单标题或 `QMdiSubWindow` 的图标。要持久修改内容，调用 widget 的 `setWindowTitle()`、`setWindowIcon()`。

### 5.2 `titleBarFlags`

它为 style 提供窗口功能提示。默认值是 `Qt::Widget`，这代表普通 widget 类型而非一个完整顶级窗口功能集。手工绘制时若没有设置合理 flags，style 可能不画你期望的窗口按钮。

但不要只为“想画一个关闭符号”就伪造 flags：真正的点击处理也必须遵从真实 widget 的 flags，否则用户会看到可点击的按钮，却发现行为不存在或不允许。

### 5.3 `titleBarState`

默认值 `0` 相当于没有额外窗口状态。它决定标题栏应表现为正常、最小化、最大化、活动或其他状态组合。

对于 `QMdiSubWindow`，shade 有额外含义：shaded 状态下仅标题栏可见。Qt 文档指出，不是所有 style 都支持从界面上退出 shaded 状态；因此仅依赖某个 style 是否画 `SC_TitleBarUnshadeButton` 并不能替代业务逻辑调用恢复 API。

## 6. 绘制数据与真实命令的职责边界

| 需求 | 应使用什么 |
| --- | --- |
| 改变 MDI 子窗口标题 | `QMdiSubWindow::setWindowTitle()` |
| 改变图标 | `setWindowIcon()` |
| 最大化/最小化/还原 | `showMaximized()`、`showMinimized()`、`showNormal()` |
| 折叠为只有标题栏 | `QMdiSubWindow::showShaded()` |
| 显示 MDI 系统菜单 | `QMdiSubWindow::showSystemMenu()` |
| 只改变一帧标题栏外观 | 修改 `QStyleOptionTitleBar` 后调用 `drawComplexControl()` |

这张边界表能避开一个常见误会：style option 是输出给绘制层的数据，并不是窗口命令对象。

## 7. 安全转换与事件处理

`QStyle::drawComplexControl()` 接收 `QStyleOptionComplex` 基类指针，会处理工具按钮、组合框、滚动条、滑块等多种控件。必须用 `qstyleoption_cast()` 检查：

```cpp
const auto *titleBar =
    qstyleoption_cast<const QStyleOptionTitleBar *>(option);
if (!titleBar)
    return;
```

`Type = SO_TitleBar` 与 `Version = 1` 是这项检查的依据。不要对任意 complex option 直接做 `static_cast`。

另外，style 的职责通常是计算几何与绘制。需要响应点击时，使用 `hitTestComplexControl(CC_TitleBar, ...)` 判断具体的 titlebar subcontrol，并将对应真实命令交回 `QMdiSubWindow` 或窗口管理逻辑执行；不要只因鼠标落在你手画的图标上就擅自关闭窗口。

## 8. 常见错误

### 8.1 试图修改原生窗口标题栏

症状：自定义 style 只影响 MDI 子窗口，普通顶级窗口标题栏没有变化。

原因：原生非客户区一般由操作系统窗口管理器绘制，`QStyleOptionTitleBar` 文档的直接目标是 `QMdiSubWindow`。

处理：若需要跨平台自定义顶级窗口标题栏，应设计无边框窗口和完整的拖动、缩放、系统菜单与可访问性方案；这不是修改本 option 即可完成的任务。

### 8.2 总是画最大化按钮

症状：窗口已经最大化却仍显示最大化图标，或不允许最大化的窗口也有该按钮。

原因：只看某个视觉偏好，忽略了 `titleBarFlags` 和 `titleBarState`。

处理：让当前 style 根据完整 option 选择 `SC_TitleBarMaxButton` 或 `SC_TitleBarNormalButton`。

### 8.3 用标题文字矩形覆盖所有空白区域

症状：长标题压住最小化或关闭按钮。

原因：标题栏按钮的实际可用区域随 style 和 flags 变化。

处理：调用 `subControlRect()` 获取各按钮和 `SC_TitleBarLabel` 的矩形，再考虑文本省略。

## API 速查表
以下列出 Qt 6.11.1 类文档中 `QStyleOptionTitleBar` 直接声明的类型、构造函数和公开字段。`QStyleOptionComplex` 的子控件状态及 `QStyleOption` 的通用绘制状态不在此表内。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举常量 | `StyleOptionType::Type = SO_TitleBar` | 标识这是标题栏 style option。 | 供 `qstyleoption_cast()` 与样式系统识别。 |
| 枚举常量 | `StyleOptionVersion::Version = 1` | 标识本结构版本。 | 普通代码不需要自行检查版本。 |
| 构造 | `QStyleOptionTitleBar()` | 创建并以默认值初始化标题栏绘制数据。 | 默认文字和图标为空，flags 为 `Qt::Widget`，state 为 `0`。 |
| 构造 | `QStyleOptionTitleBar(const QStyleOptionTitleBar &other)` | 复制一份标题栏绘制状态。 | 是值复制，不拥有窗口或内部 widget。 |
| 公开字段 | `QIcon icon` | 保存标题栏本次要绘制的图标。 | 修改不影响真实窗口图标。 |
| 公开字段 | `QString text` | 保存标题栏本次要绘制的标题。 | 修改不影响 `windowTitle` 或系统菜单文字。 |
| 公开字段 | `Qt::WindowFlags titleBarFlags` | 保存窗口类型与可用窗口装饰/功能提示。 | 决定哪些按钮有资格出现；不是当前最大化或按下状态。 |
| 公开字段 | `int titleBarState` | 保存底层窗口当前状态。 | 语义上是 `Qt::WindowStates` 位组合；应与 flags 区分。 |

## 10. 一句话总结

`QStyleOptionTitleBar` 是 `QMdiSubWindow` 客户端标题栏的绘制契约：`titleBarFlags` 说明窗口允许什么，`titleBarState` 说明窗口当前是什么状态，文字与图标提供内容，而标题栏按钮的真实几何和行为必须由 `QStyle`、命中测试与窗口命令共同完成。
