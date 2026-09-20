# Qt QMdiSubWindow 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QMdiSubWindow>`
> 所属模块：`Qt6::Widgets`
> 继承：`QWidget -> QMdiSubWindow`
> 常见搭档：`QMdiArea`、`QMenu`

## 1. QMdiSubWindow 解决什么问题

`QMdiSubWindow` 是 MDI 区域里的“内部窗口外壳”。它本身像一个普通窗口：有标题栏、系统菜单、最小化/最大化/关闭行为；但它真正展示的内容是内部 widget。

它解决的问题是：

- 给一个普通控件套上 MDI 窗口外观；
- 让控件在 `QMdiArea` 里像窗口一样被移动和缩放；
- 提供 shading、窗口状态变化、键盘交互这些 MDI 专属行为。

大多数情况下你不需要自己手工创建它，而是直接：

```cpp
QMdiSubWindow *subWindow = mdiArea->addSubWindow(editor);
```

如果你要自己控制窗口壳子，再调用 `setWidget()` 也可以。

## 2. 最小可用代码

```cpp
#include <QApplication>
#include <QMdiArea>
#include <QMdiSubWindow>
#include <QTextEdit>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QMdiArea area;
    auto *subWindow = new QMdiSubWindow;
    subWindow->setWidget(new QTextEdit);
    area.addSubWindow(subWindow);
    subWindow->show();

    area.resize(900, 600);
    area.show();
    return app.exec();
}
```

## 3. 内部 widget 和系统菜单

### 3.1 `setWidget`

```cpp
subWindow->setWidget(new QTextEdit);
QWidget *content = subWindow->widget();
```

`setWidget()` 把内容控件装进 MDI 子窗口。替换时，旧的内部 widget 会被移出并重新挂到 root window 下，所以它不会被直接 delete。

这点很重要：

- `QMdiSubWindow` 会暂时接管 `widget`；
- 如果你之后不再使用旧 widget，要自己删；
- 如果你想复用旧 widget，可以重新放回别处。

### 3.2 `setSystemMenu`

```cpp
auto *menu = new QMenu;
subWindow->setSystemMenu(menu);
```

系统菜单用于窗口的标题栏菜单和键盘交互模式。`QMdiSubWindow` 会取得这个菜单的所有权，旧菜单也会被删除。

### 3.3 `mdiArea()`

```cpp
QMdiArea *area = subWindow->mdiArea();
```

用于反查这个子窗口属于哪个 MDI 区域。空指针时说明它还没被放进区域里，或者已经脱离了区域。

## 4. 窗口状态、折叠和激活

```cpp
bool shaded = subWindow->isShaded();
subWindow->showShaded();
```

`showShaded()` 会把窗口折叠成只剩标题栏的状态。它很像桌面环境里的“卷起窗口”。

相关信号：

- `windowStateChanged(oldState, newState)`：最小化、恢复、最大化等状态变化；
- `aboutToActivate()`：窗口即将被激活；

这两个信号通常用来同步窗口菜单、标题状态和外层工具栏。

## 5. 键盘交互和拖动方式

```cpp
subWindow->setKeyboardSingleStep(1);
subWindow->setKeyboardPageStep(10);
subWindow->setOption(QMdiSubWindow::RubberBandMove, true);
subWindow->setOption(QMdiSubWindow::RubberBandResize, true);
```

`keyboardSingleStep` 和 `keyboardPageStep` 决定键盘移动/缩放时每次走多少像素：

- 普通按键用 single step；
- 按住 Shift 时用 page step。

`SubWindowOption` 里真正常用的是：

- `RubberBandMove`
- `RubberBandResize`

它们适合重绘开销大的内容，比如复杂视图、图像或视频区域。拖动时只显示轮廓，松开后才真正重排。

`AllowOutsideAreaHorizontally` 和 `AllowOutsideAreaVertically` 属于内部用途，普通项目不用碰。

## 6. 常见流程

### 6.1 作为 addSubWindow 的结果

```cpp
QMdiSubWindow *subWindow = mdiArea->addSubWindow(new QTextEdit);
subWindow->setWindowTitle(tr("文档"));
subWindow->show();
```

### 6.2 自己创建窗口壳

```cpp
auto *subWindow = new QMdiSubWindow;
subWindow->setWidget(new QTextEdit);
subWindow->setWindowTitle(tr("自定义窗口"));
mdiArea->addSubWindow(subWindow);
```

这种写法适合你要提前挂自定义菜单、定制行为或在添加前调整窗口壳属性。

## API 速查表
### 7.1 类型、构造和内容控件

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `SubWindowOption` | 描述 MDI 子窗口移动和缩放行为的单个选项。 | `AllowOutsideAreaHorizontally/Vertically` 属于内部用途，普通应用主要使用橡皮筋选项。 |
| 类型 | `SubWindowOptions` | `SubWindowOption` 的 flags 集合。 | 多个选项用 `|` 组合；单项查询用 `testOption()`。 |
| 选项 | `RubberBandMove` | 拖动子窗口时先显示轮廓，松开后再真正移动内容。 | 复杂内容或重绘成本高时可以减少拖动过程中的绘制压力。 |
| 选项 | `RubberBandResize` | 调整大小时先显示轮廓，松开后再真正改变内容区域。 | 适合图像、视频或复杂视图；普通表单通常直接实时调整更自然。 |
| 构造 | `QMdiSubWindow(QWidget *parent = nullptr, Qt::WindowFlags flags = {})` | 创建一个 MDI 子窗口外壳。 | 它不是内容 widget；通常还要通过 `setWidget()` 装入真正页面，再加入 `QMdiArea`。 |
| 析构 | `~QMdiSubWindow()` | 销毁窗口壳及其对象树关系。 | 内容控件和系统菜单的实际清理要结合 Qt 的父子关系和当前归属判断。 |
| 尺寸 | `sizeHint()` / `minimumSizeHint()` | 为 MDI 区域提供窗口壳的推荐尺寸和最小尺寸。 | 内容控件过大或最小尺寸过高时，子窗口可能无法缩到预期大小。 |
| 内容 | `setWidget(QWidget *)` / `widget()` | 设置或读取窗口内部真正显示的内容控件。 | 设置新内容时旧 widget 会被移出窗口而不是替你删除；要复用或销毁旧对象都需明确处理。 |

### 7.2 菜单、所属关系和窗口状态

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 系统菜单 | `setSystemMenu(QMenu *)` / `systemMenu()` | 设置或读取标题栏上的系统菜单。 | 子窗口会接管设置进去的菜单；替换旧菜单时不要再手动删除已被接管的对象。 |
| 系统菜单 | `showSystemMenu()` | 显示当前子窗口的系统菜单。 | 适合自定义标题栏按钮或键盘入口；需要 Qt 菜单功能可用。 |
| 所属关系 | `mdiArea()` | 返回当前所属的 `QMdiArea`。 | 未加入 MDI 区域或已被移除时可能返回空指针。 |
| 状态 | `isShaded()` | 判断子窗口是否已卷起为只显示标题栏的状态。 | 卷起不是最小化；恢复和菜单命令要分别处理。 |
| 状态 | `showShaded()` | 把子窗口折叠成标题栏。 | 适合暂时释放工作区空间；并不是关闭内容控件。 |
| 行为 | `setOption(SubWindowOption, bool)` | 开关橡皮筋移动、橡皮筋缩放等子窗口行为。 | 只改变窗口交互方式，不会改变内容 widget 的布局。 |
| 行为 | `testOption(SubWindowOption)` | 查询某个子窗口行为选项是否启用。 | 用于根据当前窗口配置决定菜单勾选或交互逻辑。 |

### 7.3 键盘步长、信号和边界说明

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 键盘步长 | `setKeyboardSingleStep(int)` / `keyboardSingleStep()` | 设置或读取键盘移动、缩放时的普通步长。 | 步长是像素语义；过大时方向键微调会显得跳跃。 |
| 键盘步长 | `setKeyboardPageStep(int)` / `keyboardPageStep()` | 设置或读取键盘操作的页步长。 | 通常用于带修饰键的较大步进，具体触发方式受窗口交互实现影响。 |
| 信号 | `windowStateChanged(Qt::WindowStates oldState, Qt::WindowStates newState)` | 窗口状态改变时通知外部。 | 最小化、最大化、恢复等状态都可能触发；不要只按“是否关闭”理解它。 |
| 信号 | `aboutToActivate()` | 子窗口即将成为活动窗口时发出。 | 适合在激活前准备文档状态、工具栏动作和属性面板。 |
| 事件边界 | `closeEvent(QCloseEvent *)` | 内容或子类可以重写的关闭事件入口。 | 该接口来自 `QWidget`；需要拦截未保存提示时，优先在内容 widget 或子窗口重写关闭流程。 |
| 事件边界 | `changeEvent(QEvent *)` | 窗口状态、字体、样式等发生变化时的事件入口。 | 只有需要响应 MDI 壳状态变化时才重写，普通业务逻辑优先连接公开信号。 |

### 一句话总结

`QMdiSubWindow` 不是内容本身，而是内容外面的“窗口壳”：把控件装进去，给它菜单、状态和拖动行为，再交给 `QMdiArea` 管理。
