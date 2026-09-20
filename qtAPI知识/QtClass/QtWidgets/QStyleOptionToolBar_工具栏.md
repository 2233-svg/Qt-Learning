# Qt QStyleOptionToolBar 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleOptionToolBar>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionToolBar`  
> 关键词：`QToolBar`、`QMainWindow`、`QStyle`、`CE_ToolBar`

## 1. 先说结论：它描述的是工具栏容器，不是工具栏按钮

`QStyleOptionToolBar` 是 `QStyle` 绘制一个完整 `QToolBar` 容器时读取的参数包。

它不创建工具栏、不添加动作，也不处理拖动；它回答的是当前样式需要知道的绘制问题：

- 这个工具栏现在停靠在哪一侧；
- 它所在的停靠区有几条工具栏行；
- 它是所在行的开头、中间、末尾，还是这一行唯一的工具栏；
- 工具栏是否可移动，从而是否应具有拖动手柄的视觉提示；
- 边框主线和中间线应采用多宽。

可以把职责分开：

```text
QMainWindow
  └─ 负责管理四个停靠区、工具栏行和几何
       └─ QToolBar
            ├─ 负责动作、工具按钮、可移动性和自身状态
            └─ initStyleOption()
                 └─ QStyleOptionToolBar
                      └─ QStyle::drawControl(CE_ToolBar, ...)
```

它不是：

- `QToolButton` 的绘制参数。单个工具按钮使用的是 `QStyleOptionToolButton`；
- `QAction` 或按钮文字、图标的配置对象；
- 能改变停靠行为的控制器；
- 可以长期保存的“工具栏状态快照”。

一句话说，`QToolBar` 管行为和内容，`QMainWindow` 管停靠布局，`QStyleOptionToolBar` 只向 style 描述“现在应当画出怎样的工具栏容器”。

## 2. 普通应用通常不需要手工创建它

绝大多数情况下，直接使用 `QMainWindow` 和 `QToolBar`：

```cpp
#include <QAction>
#include <QMainWindow>
#include <QToolBar>

class MainWindow final : public QMainWindow
{
public:
    MainWindow()
    {
        auto *fileToolBar = addToolBar("文件");
        fileToolBar->setObjectName("fileToolBar");
        fileToolBar->setMovable(true);
        fileToolBar->setAllowedAreas(
            Qt::TopToolBarArea | Qt::BottomToolBarArea);

        auto *openAction = fileToolBar->addAction("打开");
        connect(openAction, &QAction::triggered, this, [] {
            // 执行打开操作。
        });

        auto *editToolBar = new QToolBar("编辑", this);
        addToolBar(Qt::TopToolBarArea, editToolBar);
        editToolBar->addAction("撤销");
    }
};
```

在上面的代码中：

- `addToolBar()` 负责把工具栏放进 `QMainWindow` 的某个停靠区；
- `setAllowedAreas()` 限制用户能把它拖到哪些停靠区；
- `setMovable()` 决定用户能否拖动它；
- Qt 在每次需要绘制时由 `QToolBar` 填充 `QStyleOptionToolBar`。

真正需要直接读取本类的场景一般只有三类：

1. 编写 `QProxyStyle` 或自定义 `QStyle`，修改工具栏容器的外观；
2. 继承 `QToolBar`，排查停靠、换行或手柄视觉效果；
3. 排查同一停靠区有多行、多条工具栏时，边框连接或圆角处理不正确的问题。

## 3. 先理解 QMainWindow 的工具栏布局

`QMainWindow` 有四个工具栏停靠区：

```text
                 Qt::TopToolBarArea
    +-------------------------------------------+
    | [工具栏 A][工具栏 B]   <-- 同一条工具栏行 |
    | [工具栏 C]             <-- 另一条工具栏行 |
    +---+-----------------------------------+---+
    |   |                                   |   |
Qt::LeftToolBarArea                    Qt::RightToolBarArea
    |   |            中央区域               |   |
    +---+-----------------------------------+---+
    |         Qt::BottomToolBarArea             |
    +-------------------------------------------+
```

一个停靠区可以有多条行。一条行由方向相同、相邻排列的工具栏组成：

- 顶部和底部区域中的工具栏行通常是水平的；
- 左侧和右侧区域中的工具栏行通常是垂直的；
- 同一行中可以有多条 `QToolBar`；
- 同一个区域中也可以有多行。

Qt 的主窗口布局负责计算这些区域、行和工具栏的矩形；`QStyleOptionToolBar` 不重新计算布局，只把计算结果的类别信息提供给 style。

## 4. `toolBarArea`、`positionOfLine`、`positionWithinLine` 是三个不同层级

这是本类最值得弄清楚的一组字段。

| 字段 | 它描述的对象 | 回答的问题 |
| --- | --- | --- |
| `toolBarArea` | 整个工具栏所在的停靠区 | 在窗口的上、下、左还是右？ |
| `positionOfLine` | 当前工具栏所在的行 | 这条行在该停靠区的第一条、中间、最后一条，还是唯一一条？ |
| `positionWithinLine` | 当前工具栏本身 | 它在自己那条行的开始、中间、末尾，还是唯一一条？ |

例如顶部区域有两行：第一行是 `A`、`B`，第二行只有 `C`：

```text
TopToolBarArea

第一行： [ A ][ B ]
第二行： [ C ]
```

它们的语义是：

| 工具栏 | `positionOfLine` | `positionWithinLine` |
| --- | --- | --- |
| `A` | `Beginning` | `Beginning` |
| `B` | `Beginning` | `End` |
| `C` | `End` | `OnlyOne` |

这里“第一行/最后一行”的顺序从父窗口边缘开始计算；行内顺序则是水平行从左到右、垂直行从上到下。布局方向或从右到左的视觉需求不应靠手工猜测这两个字段，而应让 `QMainWindow` 填充真实 option。

### 4.1 `ToolBarPosition` 的四个取值

```cpp
enum QStyleOptionToolBar::ToolBarPosition {
    Beginning,
    Middle,
    End,
    OnlyOne
};
```

| 取值 | 用于 `positionOfLine` 时 | 用于 `positionWithinLine` 时 |
| --- | --- | --- |
| `Beginning` | 当前行是停靠区的第一行。 | 当前工具栏是该行第一个。 |
| `Middle` | 当前行处于多行中的中间。 | 当前工具栏处于同一行的中间。 |
| `End` | 当前行是停靠区的最后一行。 | 当前工具栏是该行最后一个。 |
| `OnlyOne` | 该停靠区只有这一条行。 | 该行只有这一条工具栏。 |

`OnlyOne` 是 `positionOfLine` 和 `positionWithinLine` 的默认值。它不是“尚未设置”的错误状态，而是“没有相邻项可比较”的正常布局情况。

## 5. `features` 只描述可移动性，不设置可移动性

`features` 的类型是 `ToolBarFeatures`，也就是 `QFlags<ToolBarFeature>`：

```cpp
enum QStyleOptionToolBar::ToolBarFeature {
    None = 0x0,
    Movable = 0x1
};
```

| 标志 | 含义 |
| --- | --- |
| `None` | 工具栏不可移动，也是默认值。 |
| `Movable` | 工具栏可移动；样式可以据此绘制或突出拖动手柄。 |

这是一条单向信息流：

```text
QToolBar::setMovable(true)
        |
        v
QToolBar::initStyleOption()
        |
        v
option.features 包含 Movable
        |
        v
QStyle 决定手柄和容器外观
```

因此，下面的代码不会让真实工具栏可拖动：

```cpp
QStyleOptionToolBar option;
option.features |= QStyleOptionToolBar::Movable; // 只改了一个绘制参数副本
```

要改变交互行为，必须修改 `QToolBar`：

```cpp
toolBar->setMovable(true);
toolBar->setAllowedAreas(Qt::TopToolBarArea | Qt::BottomToolBarArea);
```

还要区分两个概念：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 可移动性 | `QToolBar::isMovable()` / `features & Movable` | 表示用户能否在停靠区之间拖动工具栏 | `QStyleOptionToolBar::features` 反映绘制时状态，不负责实际拖动逻辑 |
| 可浮动性 | `QToolBar::isFloatable()` | 表示用户能否把工具栏拖成独立浮动窗口 | 这不是 `QStyleOptionToolBar` 的直接字段，样式绘制时不要误读为 `features` |
| 允许区域 | `QToolBar::allowedAreas()` | 返回工具栏允许停靠到哪些区域 | 它是允许集合，不是当前所在区域 |
| 当前区域 | `toolBarArea` | 表示当前正按哪个停靠区域来绘制工具栏 | 它是单个 `Qt::ToolBarArea` 值；不要拿它代替 allowed areas |

## 6. `toolBarArea` 是当前区域，不是允许区域

`toolBarArea` 的类型是 `Qt::ToolBarArea`，默认值为：

```cpp
Qt::TopToolBarArea
```

它表示绘制时工具栏所在的区域，例如：

```cpp
Qt::TopToolBarArea
Qt::BottomToolBarArea
Qt::LeftToolBarArea
Qt::RightToolBarArea
```

它与 `QToolBar::allowedAreas()` 的区别很关键：

```cpp
toolBar->setAllowedAreas(
    Qt::TopToolBarArea | Qt::BottomToolBarArea);
```

上面表示用户可以把工具栏放到顶部或底部；当它当前处于顶部时，填充到 option 的 `toolBarArea` 才是 `Qt::TopToolBarArea`。也就是说：

```text
allowedAreas = “可以去哪里”
toolBarArea  = “现在在哪里”
```

如果 `QToolBar` 没有被 `QMainWindow` 管理，而是普通地放进一个 `QVBoxLayout`，那么“停靠区域、工具栏行”的语义本身就不适用。不要为了自定义绘制而伪造主窗口停靠信息。

## 7. `lineWidth` 和 `midLineWidth` 描述什么

这两个整数是工具栏容器绘制时可供 style 使用的线宽：

| 字段 | 作用 | 默认值 |
| --- | --- | --- |
| `lineWidth` | 主边线宽度。 | `0` |
| `midLineWidth` | 中间线宽度。 | `0` |

它们和 `QStyleOptionFrame` 中同名字段的用途相似，都是给样式提供线宽数据；但它们的类没有继承关系。不要因为两个类都有 `lineWidth`，就把 `QStyleOptionToolBar` 当成 `QStyleOptionFrame` 使用。

默认构造的 `0` 只是 option 的默认状态。对一个实际显示的工具栏，应通过 `QToolBar::initStyleOption()` 读取真实数据，而不是自行猜测当前 style 会采用怎样的边框厚度。

## 8. 真正的绘制链路：容器、手柄、分隔符各自是谁画的

Qt 的工具栏样式由几个不同元素协作，而不是一个 option 负责全部细节：

| 绘制元素 | 用来画什么 | 常见 option |
| --- | --- | --- |
| `QStyle::CE_ToolBar` | 工具栏容器本身。 | `QStyleOptionToolBar` |
| `QStyle::PE_IndicatorToolBarHandle` | 可拖动工具栏的手柄。 | `QStyleOption` |
| `QStyle::PE_IndicatorToolBarSeparator` | 工具栏内部动作之间的分隔符。 | `QStyleOption` |
| `QStyle::PE_FrameMenu` | 工具栏浮动为独立窗口时的 frame。 | 对应绘制路径的 option |
| `QStyle::CE_ToolButtonLabel` | 单个工具按钮的图标和文字。 | `QStyleOptionToolButton` |

所以：

- 想改整个工具栏背景、边框、相邻工具栏衔接时，关注 `CE_ToolBar` 和本类；
- 想改拖动手柄，关注 `PE_IndicatorToolBarHandle`；
- 想改 `addSeparator()` 加出的分隔符，关注 `PE_IndicatorToolBarSeparator`；
- 想改每个按钮的图标、菜单箭头或按下效果，关注 `QStyleOptionToolButton`。

不要在 `CE_ToolBar` 里重新绘制所有工具按钮；也不要试图通过 `QStyleOptionToolBar` 修改一个 `QAction` 的文本或图标。

## 9. 正确初始化：优先使用 QToolBar 的 `initStyleOption()`

`QToolBar` 提供了受保护的虚函数：

```cpp
virtual void QToolBar::initStyleOption(
    QStyleOptionToolBar *option) const;
```

它会把当前工具栏的真实状态写入 option，包括本类专有字段和 `QStyleOption` 基类中的通用字段。

因为它是 `protected`，外部普通代码不能直接调用。调试或扩展时，可在子类中调用：

```cpp
#include <QDebug>
#include <QStyleOptionToolBar>
#include <QToolBar>

class InspectableToolBar final : public QToolBar
{
public:
    using QToolBar::QToolBar;

    void dumpStyleOption() const
    {
        QStyleOptionToolBar option;
        initStyleOption(&option);

        qDebug() << "rect:" << option.rect;
        qDebug() << "area:" << option.toolBarArea;
        qDebug() << "line position:" << option.positionOfLine;
        qDebug() << "position in line:" << option.positionWithinLine;
        qDebug() << "movable:"
                 << option.features.testFlag(QStyleOptionToolBar::Movable);
        qDebug() << "line widths:" << option.lineWidth << option.midLineWidth;
        qDebug() << "horizontal:"
                 << option.state.testFlag(QStyle::State_Horizontal);
    }
};
```

只调用基类的 `QStyleOption::initFrom(this)` 并不够：

```cpp
QStyleOptionToolBar option;
option.initFrom(this); // 只初始化 rect、palette、state 等通用字段
```

它不知道 `QMainWindow` 怎样排列工具栏行，也不会自动填充本类的 `toolBarArea`、两个 position 或 `features`。需要真实工具栏状态时，应调用 `QToolBar::initStyleOption()`。

## 10. 横向还是纵向：看 `state`，不要从 area 自己推导

`QStyleOptionToolBar` 没有独立的 `orientation` 字段。工具栏的横向/纵向状态通过继承自 `QStyleOption` 的 `state` 表示：

```cpp
option.state.testFlag(QStyle::State_Horizontal)
```

Qt 的 style reference 说明，除通用状态外，工具栏在水平时会设置 `State_Horizontal`。这通常发生在顶部或底部停靠区。

自定义 style 中应读取该状态，而不是只按 `toolBarArea` 写死规则。这样同一个 style 也能适应工具栏脱离主窗口、布局变化或平台样式的实际状态。

## 11. 在 QProxyStyle 中定制工具栏容器

下例只为不可移动工具栏叠加一条细线，并保留原 style 的大部分平台外观：

```cpp
#include <QPainter>
#include <QProxyStyle>
#include <QStyleOptionToolBar>

class ToolBarAccentStyle final : public QProxyStyle
{
public:
    using QProxyStyle::QProxyStyle;

    void drawControl(ControlElement element,
                     const QStyleOption *option,
                     QPainter *painter,
                     const QWidget *widget = nullptr) const override
    {
        if (element == CE_ToolBar) {
            if (const auto *toolBar =
                    qstyleoption_cast<const QStyleOptionToolBar *>(option)) {
                QProxyStyle::drawControl(element, option, painter, widget);

                if (!toolBar->features.testFlag(QStyleOptionToolBar::Movable)) {
                    painter->save();
                    painter->setPen(QPen(Qt::darkGray, 1));
                    painter->drawLine(toolBar->rect.bottomLeft(),
                                      toolBar->rect.bottomRight());
                    painter->restore();
                }
                return;
            }
        }

        QProxyStyle::drawControl(element, option, painter, widget);
    }
};
```

使用方式：

```cpp
toolBar->setStyle(new ToolBarAccentStyle(toolBar->style()));
```

这个写法有两个要点：

1. `qstyleoption_cast()` 会检查 option 的类型和版本，转换失败就返回 `nullptr`；不要对 `const QStyleOption *` 直接做无条件 `static_cast`。
2. 先让基类画完整工具栏，再叠加一小段装饰。若你自己完整绘制了背景和边框，又继续调用基类，线条和背景很可能会重复。

如果你的目标是手柄纹理，应重写 `drawPrimitive()` 并处理 `PE_IndicatorToolBarHandle`；它不是 `CE_ToolBar` 的同一个绘制入口。

## 12. 生命周期、所有权和线程边界

`QStyleOptionToolBar` 是一个轻量的值类型：

- 它不继承 `QObject`，没有 parent；
- 它不拥有 `QToolBar`、`QMainWindow`、`QAction`、`QWidget` 或 `QPainter`；
- 可以在栈上创建；
- 复制构造和赋值只复制字段值；
- 在 style 绘制函数中接收到的 `option` 指针只应在本次调用期间读取；
- 访问实际 `QToolBar`、修改 style 或绘制 GUI，仍应在 GUI 线程完成。

正确的缓存方式是复制你真正需要的数据：

```cpp
const QRect toolbarRect = option->rect;
const bool movable =
    option->features.testFlag(QStyleOptionToolBar::Movable);
```

不要把 `drawControl()` 参数中的 `option` 指针保存到成员变量，留给稍后的事件或定时器使用。那块内存通常来自当前绘制栈帧，离开函数后就不再有效。

## 13. 默认值和直接字段速览

Qt 6.11.1 中默认构造的本类直接字段如下：

| 字段 | 默认值 | 说明 |
| --- | --- | --- |
| `positionOfLine` | `OnlyOne` | 所在停靠区只有一条工具栏行。 |
| `positionWithinLine` | `OnlyOne` | 所在行只有当前这条工具栏。 |
| `toolBarArea` | `Qt::TopToolBarArea` | 默认绘制区域。 |
| `features` | `None` | 默认不具备可移动标志。 |
| `lineWidth` | `0` | 默认主线宽度。 |
| `midLineWidth` | `0` | 默认中间线宽度。 |

同时，类常量为：

```cpp
QStyleOptionToolBar::Type    // SO_ToolBar
QStyleOptionToolBar::Version // 1
```

`Type` 和 `Version` 的主要用途是 `QStyleOption` 家族和 `qstyleoption_cast()` 的运行时识别与兼容判断。普通应用代码不应通过手工改写它们伪造另一种 option。

## 14. 常见误区与排查顺序

### 14.1 “设置了 `option.features`，工具栏还是不能拖”

这是正常的。option 是绘制数据，不是行为设置。调用：

```cpp
toolBar->setMovable(true);
```

若还需要限制目标区域，再设置 `setAllowedAreas()`。

### 14.2 “`toolBarArea` 为什么不是 `allowedAreas()`”

前者是当前区域的单值，后者是允许的区域集合。需要当前停靠区域时可由 `QMainWindow::toolBarArea(toolBar)` 查询；绘制路径则从 option 读取对应状态。

### 14.3 “同一个工具栏单独时是 `OnlyOne`，加了另一条后外观变了”

这是 style 收到了不同的 `positionWithinLine`。它可能据此调整边界、分隔线或相邻工具栏的连接方式。先打印 `positionOfLine` 和 `positionWithinLine`，不要只看 `toolBarArea`。

### 14.4 “我只创建了默认 option，为什么它总是 Top 和 OnlyOne”

这些正是默认值，不是当前 widget 的真实布局。应在 `QToolBar` 子类内通过 `initStyleOption()` 填充。

### 14.5 “我在 `CE_ToolBar` 里改了样式，为什么 separator 没变化”

separator 有独立的 `PE_IndicatorToolBarSeparator` 绘制入口。手柄同理，使用 `PE_IndicatorToolBarHandle`。

### 14.6 “为什么把工具栏放进 QVBoxLayout 后，停靠信息不可靠”

工具栏放进普通布局时不由 `QMainWindow` 的停靠布局管理。`ToolBarArea` 和两层 position 的意义来自主窗口工具栏框架；不要将它们误用为一般 `QWidget` 布局坐标。

## API 速查表
### 15.1 本类直接 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `QStyleOptionToolBar::StyleOptionType` | 表示工具栏 option 的类型枚举。 | 具体类型值通过 `Type` 提供。 |
| 类型值 | `QStyleOptionToolBar::Type` | 提供值为 `SO_ToolBar` 的运行时类型标识。 | 供 Qt 和 `qstyleoption_cast()` 识别，不是业务状态。 |
| 类型 | `QStyleOptionToolBar::StyleOptionVersion` | 表示工具栏 option 数据布局版本的枚举。 | 具体版本值通过 `Version` 提供。 |
| 类型值 | `QStyleOptionToolBar::Version` | 提供当前 option 版本，Qt 6.11.1 中为 `1`。 | 自定义 style 通常交给 `qstyleoption_cast()` 检查。 |
| 枚举 | `QStyleOptionToolBar::ToolBarPosition` | 描述工具栏行在停靠区中的位置，或工具栏在行内的位置。 | 同时供 `positionOfLine` 和 `positionWithinLine` 使用，但两个字段语境不同。 |
| 枚举值 | `Beginning` | 表示第一条行，或一条行中的第一个工具栏。 | 是视觉位置语义，不是创建顺序。 |
| 枚举值 | `Middle` | 表示中间的行，或行内中间的工具栏。 | 可以有多个中间项。 |
| 枚举值 | `End` | 表示最后一条行，或一条行中的最后一个工具栏。 | 是边界绘制提示，不是允许停靠区域。 |
| 枚举值 | `OnlyOne` | 表示停靠区只有一条行，或该行只有一条工具栏。 | 是两个 position 字段的默认且有效状态。 |
| 枚举 | `QStyleOptionToolBar::ToolBarFeature` | 描述工具栏容器的绘制特征。 | 当前公开特征主要是可移动性。 |
| 枚举值 | `None` | 表示没有额外工具栏绘制特征。 | 是 `features` 的默认值，不代表工具栏对象不存在。 |
| 枚举值 | `Movable` | 表示工具栏可移动，style 可以据此绘制手柄或拖动提示。 | 只反映 `QToolBar` 状态，不会反向开启拖动。 |
| 标志类型 | `QStyleOptionToolBar::ToolBarFeatures` | `ToolBarFeature` 的 `QFlags` 集合。 | 使用 `testFlag(Movable)` 或按位运算查询。 |
| 公共字段 | `positionOfLine` | 提供当前工具栏所在行在停靠区中的位置。 | 描述的是“第几条行”，不是当前工具栏在行内的位置。 |
| 公共字段 | `positionWithinLine` | 提供当前工具栏在所属行内的位置。 | 描述的是“行内第几个工具栏”，不是整行位置。 |
| 公共字段 | `toolBarArea` | 提供当前工具栏绘制所在的 `Qt::ToolBarArea`。 | 是当前所在区域，不是 `QToolBar::allowedAreas()` 的允许集合。 |
| 公共字段 | `features` | 提供本次绘制应考虑的工具栏特征集合。 | 默认 `None`；修改它只影响绘制副本。 |
| 公共字段 | `lineWidth` | 提供工具栏主边线宽度。 | 默认 `0`；真实工具栏值应由 `QToolBar::initStyleOption()` 填充。 |
| 公共字段 | `midLineWidth` | 提供工具栏中间线宽度。 | 默认 `0`；不要把它和普通 `QStyleOptionFrame` 互相强转。 |
| 构造 | `QStyleOptionToolBar()` | 创建具有默认字段值的工具栏容器绘制参数。 | 不会绑定或读取任何 `QToolBar` 的停靠状态。 |
| 构造 | `QStyleOptionToolBar(const QStyleOptionToolBar &other)` | 创建另一个工具栏 option 的值副本。 | 复制绘制数据，不复制工具栏、动作或 painter。 |
| 赋值 | `operator=(const QStyleOptionToolBar &other)` | 将另一个 option 的字段复制到当前对象。 | 仍然只是值复制，不转移控件所有权。 |
| 保护构造 | `QStyleOptionToolBar(int version)` | 按指定版本构造，支持 Qt 的兼容扩展。 | `protected`，普通业务代码不能直接调用。 |

### 15.2 继承字段和协作 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 继承字段 | `QStyleOption::rect` | 指定当前工具栏容器的整体绘制矩形。 | 这是 `CE_ToolBar` 的画布，不是某个工具按钮的矩形。 |
| 继承字段 | `QStyleOption::state` | 提供启用、激活、鼠标状态和方向等通用 style 状态。 | 通常用 `State_Horizontal` 判断横向绘制；不要只按 area 猜方向。 |
| 继承字段 | `QStyleOption::palette` | 提供工具栏绘制时使用的调色板。 | 自定义 style 应读取 palette，避免硬编码主题颜色。 |
| 继承字段 | `QStyleOption::direction` | 提供左到右或右到左的布局方向。 | 自定义几何应配合 `visualRect()` 等 API 处理 RTL。 |
| 初始化 | `QToolBar::initStyleOption(QStyleOptionToolBar *) const` | 用当前 QToolBar 和 QMainWindow 停靠状态填充完整 option。 | `protected`；QToolBar 子类获取真实行位置和特征的正确入口。 |
| 初始化 | `QStyleOption::initFrom(const QWidget *)` | 从 QWidget 填充通用基类状态。 | 不知道主窗口工具栏行、停靠区和可移动特征，不能单独替代专属初始化。 |
| 绘制 | `QStyle::drawControl(QStyle::CE_ToolBar, ...)` | 绘制整个工具栏容器。 | option 应安全转换为本类；工具按钮自身由其他绘制入口处理。 |
| 绘制 | `QStyle::drawPrimitive(QStyle::PE_IndicatorToolBarHandle, ...)` | 绘制工具栏拖动手柄。 | 手柄是独立 primitive，不要把它混入整个容器背景绘制。 |
| 绘制 | `QStyle::drawPrimitive(QStyle::PE_IndicatorToolBarSeparator, ...)` | 绘制工具栏动作之间的分隔符。 | 对应 `addSeparator()` 等产生的 separator，和容器 frame 是不同入口。 |
| 类型转换 | `qstyleoption_cast<const QStyleOptionToolBar *>(option)` | 从基类指针安全获取工具栏 option。 | 会检查 type/version，失败返回 `nullptr`。 |
| 配置行为 | `QToolBar::setMovable(bool)` | 设置用户是否可以移动工具栏。 | 真实决定 option 是否包含 `Movable` 特征。 |
| 查询行为 | `QToolBar::isMovable() const` | 查询工具栏是否可移动。 | 不要通过修改 option 代替真实行为配置。 |
| 配置区域 | `QToolBar::setAllowedAreas(Qt::ToolBarAreas)` | 限制工具栏可停靠的目标区域集合。 | 只在 QMainWindow 工具栏停靠场景中具有该语义。 |
| 查询区域 | `QToolBar::allowedAreas() const` | 获取允许停靠区域的 flags 集合。 | 与 `toolBarArea` 的当前单一位置不同。 |
| 查询区域 | `QMainWindow::toolBarArea(const QToolBar *) const` | 获取工具栏当前停靠的区域。 | 业务逻辑可用；style 绘制通常直接读取 option。 |
| 停靠 | `QMainWindow::addToolBar(Qt::ToolBarArea, QToolBar *)` | 将工具栏放入指定停靠区，由主窗口继续管理行布局。 | 只有被 QMainWindow 管理后，行位置字段才有可靠意义。 |
| 内容 | `QToolBar::addAction(...)` | 向工具栏添加动作并生成对应工具按钮。 | action 和按钮内容不保存在本 option 中。 |
| 内容 | `QToolBar::addSeparator()` | 向工具栏添加动作分隔符。 | separator 使用 `PE_IndicatorToolBarSeparator` 单独绘制。 |
| 对比 | `QStyleOptionToolButton` | 描述单个工具按钮的绘制参数。 | 按钮图标、文字和菜单箭头问题不要误用本类。 |

---

### 一句话总结

`QStyleOptionToolBar` 是整个 `QToolBar` 容器的临时绘制状态：`toolBarArea` 说明它当前停靠在哪一侧，`positionOfLine` 说明所在行的位置，`positionWithinLine` 说明它在行内的位置，`features` 反映可移动性。行为由 `QToolBar` 和 `QMainWindow` 配置，自定义 style 则在 `CE_ToolBar` 中安全读取这个 option。
