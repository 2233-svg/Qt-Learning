# Qt QStyleOptionTabWidgetFrame 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleOptionTabWidgetFrame>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionTabWidgetFrame`  
> 关键词：`QTabWidget`、页面框架、`QStyle`、`PE_FrameTabWidget`

## 1. 先说结论：它到底是什么

`QStyleOptionTabWidgetFrame` 是给 `QStyle` 使用的一份**QTabWidget 页面框架绘制参数**。

它描述的不是一个可见控件，也不是 tab bar 中的某一个 tab，而是：

```text
QTabWidget
  ├─ QTabBar
  │    ├─ 每个 tab 的外观：QStyleOptionTab
  │    └─ 独立 tab bar 的底座：QStyleOptionTabBarBase
  └─ 页面区域外围的 frame：QStyleOptionTabWidgetFrame
```

当页面标签位于上方、下方、左侧或右侧时，页面区域的边框怎样绘制、边框要在哪里和 tab bar 衔接、选中的 tab 是否需要覆盖边框、角落控件要占掉多少空间，都需要一份上下文参数。这个类就是把这些信息交给样式系统。

它解决的问题可以概括为：

> `QTabWidget` 负责管理页面和 tab，`QStyleOptionTabWidgetFrame` 负责告诉样式系统“这个 tab widget 的页面框架应该怎样被画出来”。

它不负责：

- 创建或销毁页面；
- 切换当前页；
- 绘制某一个 tab 的标题和图标；
- 管理 tab 的鼠标点击、拖动或关闭；
- 保存一个长期有效的控件状态。

它只是一次绘制或布局计算时使用的**值类型参数对象**。

## 2. 它和另外两个 tab 相关 option 的边界

这三个类名字相近，但绘制对象不同：

| 类 | 描述对象 | 典型绘制入口 | 关注重点 |
| --- | --- | --- | --- |
| `QStyleOptionTab` | 单个 tab | `QStyle::drawControl(CE_TabBarTab, ...)` | 标题、图标、选中状态、相邻关系、关闭按钮空间。 |
| `QStyleOptionTabBarBase` | 独立 `QTabBar` 的共享底座 | `QStyle::drawPrimitive(PE_FrameTabBarBase, ...)` | 整条 tab bar 的底线、选中 tab 对底座的打断关系。 |
| `QStyleOptionTabWidgetFrame` | `QTabWidget` 的页面区域外围 frame | `QStyle::drawPrimitive(PE_FrameTabWidget, ...)` | 页面框架、tab bar 与页面 frame 的衔接、角落控件空间。 |

最容易犯的错误是把 `QStyleOptionTabBarBase` 当成 `QTabWidget` 的页面边框。Qt 文档对 `PE_FrameTabBarBase` 的说明是：它通常用于**不属于 tab widget 的 tab bar**。`QTabWidget` 的页面 frame 使用 `PE_FrameTabWidget`。

同样，`CE_ShapedFrame` 也不是本类的绘制入口。它使用的是 `QStyleOptionFrame`，用于一般的 `QFrame` 形状；本类拥有专门的 `QStyleOptionTabWidgetFrame` 数据和 `PE_FrameTabWidget` primitive。

## 3. 普通应用什么时候需要接触它

普通应用通常不需要手工创建这个 option。直接使用 `QTabWidget` 即可：

```cpp
#include <QTabWidget>
#include <QTextEdit>

auto *tabs = new QTabWidget;
tabs->addTab(new QTextEdit, "编辑器");
tabs->addTab(new QTextEdit, "日志");

tabs->setTabPosition(QTabWidget::North);
tabs->setTabShape(QTabWidget::Rounded);
tabs->setDocumentMode(true);
```

`QTabWidget` 会在自己的绘制流程中准备 `QStyleOptionTabWidgetFrame`，再交给当前 style。

真正需要直接读取这个类的场景主要有三类：

1. 继承 `QTabWidget`，调试或扩展绘制逻辑；
2. 实现 `QProxyStyle` / 自定义 `QStyle`，修改 tab widget 页面 frame 的外观；
3. 排查 tab bar、页面 frame、角落控件之间出现一条线、错位或覆盖关系异常的问题。

## 4. QTabWidget 是怎样提供完整 option 的

`QTabWidget::initStyleOption(QStyleOptionTabWidgetFrame *option) const` 是正确的初始化入口。

Qt 文档对它的定位很明确：它会用当前 `QTabWidget` 的数据初始化 option，供子类在不需要自己填充全部信息时使用。

因为这个函数是 `protected`，普通外部代码不能直接调用。若要检查真实数据，可以在 `QTabWidget` 子类里调用：

```cpp
#include <QDebug>
#include <QStyleOptionTabWidgetFrame>
#include <QTabWidget>

class InspectableTabWidget final : public QTabWidget
{
public:
    using QTabWidget::QTabWidget;

    void dumpFrameOption() const
    {
        QStyleOptionTabWidgetFrame option;
        initStyleOption(&option);

        qDebug() << "frame rect:" << option.rect;
        qDebug() << "tab bar rect:" << option.tabBarRect;
        qDebug() << "selected tab rect:" << option.selectedTabRect;
        qDebug() << "tab bar size:" << option.tabBarSize;
        qDebug() << "left corner size:" << option.leftCornerWidgetSize;
        qDebug() << "right corner size:" << option.rightCornerWidgetSize;
        qDebug() << "line widths:"
                 << option.lineWidth << option.midLineWidth;
    }
};
```

这段代码的重点不在于打印，而在于使用模型：

```text
QTabWidget 的真实状态
        |
        | initStyleOption()
        v
QStyleOptionTabWidgetFrame
        |
        | QStyle::drawPrimitive(PE_FrameTabWidget, ...)
        v
当前平台 style 绘制页面 frame
```

不要在子类里只创建一个默认 option，然后把它当成当前控件的真实状态。默认构造对象中的矩形和 corner widget 尺寸并没有当前控件的信息。

## 5. 一个 QTabWidget 页面 frame 的绘制链路

页面 frame 的职责可以按顺序理解：

1. `QTabWidget` 确定自身的几何、tab position、tab shape、当前 tab 和 corner widget；
2. `QTabWidget::initStyleOption()` 把这些状态写入 option；
3. `QStyle` 根据 `rect`、`tabBarRect`、`selectedTabRect` 等字段确定 frame 如何与 tab bar 衔接；
4. 当前 style 通过 `PE_FrameTabWidget` 绘制页面区域外围的 frame；
5. tab 本身仍由 `QTabBar` 使用 `QStyleOptionTab` 绘制。

因此，修改 frame 的外观应放在 style 的 primitive 绘制层，而不是把页面 frame 的线条混进每个 tab 的绘制代码。

## 6. 三个几何字段不要混为一谈

### 6.1 `rect`：当前 frame 的绘制区域

`rect` 是继承自 `QStyleOption` 的公共字段。它表示 style 当前要处理的整体绘制区域。

对 `PE_FrameTabWidget` 来说，style 通常先以这个区域作为页面 frame 的画布，再结合 tab 相关矩形决定边框在什么位置与 tab 相接。

它不是：

- 单个 tab 的矩形；
- 整排 tab 的矩形；
- 当前页面内容 widget 的内部可用矩形。

### 6.2 `tabBarRect`：整条 tab bar 的矩形

`tabBarRect` 表示整条 tab bar 所在的矩形。

它包含的是所有 tab 的整体区域，不是当前 tab，也不只是 tab bar 的尺寸数值。style 可以通过它判断页面 frame 与 tab bar 的相对位置。

```text
QTabWidget 的 frame 区域
┌────────────────────────────────────┐
│ tabBarRect                         │
│ [ Tab 1 ][ Tab 2 ][ Tab 3 ]        │
├────────────────────────────────────┤
│                                    │
│ 页面内容区域                       │
│                                    │
└────────────────────────────────────┘
```

实际布局可能是南、东、西侧 tab，图示只表达字段关系，不代表固定方向。

### 6.3 `selectedTabRect`：当前选中 tab 的矩形

`selectedTabRect` 表示当前选中 tab 的矩形，按 Qt 文档定义，它位于 `tabBarRect` 内。

style 使用它处理最关键的视觉连接：

- 选中 tab 是否覆盖 frame 的一小段边线；
- frame 是否在选中 tab 的位置留出缺口；
- tab 和页面内容区域是否看起来连成一个整体；
- 不同 tab position 下，连接发生在上、下、左还是右。

不要用 `selectedTabRect` 推断 tab index。它只有几何信息，不携带“这是第几个 tab”的业务身份。

在默认构造的 option 中，它是 null rectangle。没有有效当前 tab 时，也应允许它为空，不要假设一定存在一个有效选中矩形。

## 7. `tabBarSize` 和 `tabBarRect` 的区别

这两个字段都描述 tab bar，但回答的问题不同：

| 字段 | 回答的问题 |
| --- | --- |
| `tabBarSize` | tab bar 的尺寸是多少？ |
| `tabBarRect` | tab bar 在当前 frame 坐标中的位置和尺寸是什么？ |

`QSize` 没有位置，`QRect` 同时包含位置和尺寸。因此不要用 `tabBarSize` 去替代 `tabBarRect`，也不要从 `tabBarSize` 推出 tab bar 在 frame 中的偏移位置。

`QStyleOptionTabWidgetFrame` 默认构造时，`tabBarSize` 是 `QSize(-1, -1)`，表示无效尺寸。只有经过 `QTabWidget::initStyleOption()` 填充后，才应把它当成当前控件的有效布局数据。

## 8. 两个 corner widget 尺寸解决什么问题

`QTabWidget` 可以在 tab bar 两侧放置 corner widget，例如：

```cpp
#include <QCheckBox>

auto *compact = new QCheckBox("紧凑");
tabs->setCornerWidget(compact, Qt::TopRightCorner);
```

`leftCornerWidgetSize` 和 `rightCornerWidgetSize` 把这些控件的尺寸告诉 style，使 style 在绘制 tab widget frame 和 tab bar 连接关系时，为角落控件留下空间。

它们只描述尺寸，不拥有控件：

- 控件仍然由 `QTabWidget` 管理；
- option 不会保存控件指针；
- option 复制时不会复制 corner widget；
- corner widget 的可见性和几何仍由 `QTabWidget` 决定。

两个字段的默认值都是 `QSize(-1, -1)`，即 invalid size。

Qt 文档还特别说明，corner widget 主要为 North 和 South tab position 设计；把它用于 East 或 West 方向可能不能正常工作。因此不能只看到这两个字段存在，就推断四个方向都具有同等可靠的 corner widget 布局支持。

## 9. `shape` 保存的是 QTabBar::Shape

`shape` 的类型是 `QTabBar::Shape`，默认值是：

```cpp
QTabBar::RoundedNorth
```

它表达 tab bar 的方向和轮廓形状，例如：

- `RoundedNorth`
- `RoundedSouth`
- `RoundedWest`
- `RoundedEast`
- 对应的 `Triangular...` 变体

不要把它和 `QTabWidget::TabShape` 混为一谈：

| 类型 | 典型值 | 作用 |
| --- | --- | --- |
| `QTabWidget::TabShape` | `Rounded`、`Triangular` | QTabWidget 对外暴露的“圆角还是三角形”配置。 |
| `QTabBar::Shape` | `RoundedNorth`、`TriangularWest` 等 | 已经包含方向的 tab bar 形状，供 style 直接使用。 |

应用层通常通过下面的 API 配置，而不是直接修改 option：

```cpp
tabs->setTabPosition(QTabWidget::South);
tabs->setTabShape(QTabWidget::Triangular);
```

QTabWidget 会把这些高层配置转换成 option 中的 `QTabBar::Shape`。

## 10. `lineWidth` 与 `midLineWidth`

### 10.1 `lineWidth`

`lineWidth` 是绘制 panel/frame 主线的宽度。它表达的是 frame 的主要边线厚度。

默认值为 `0`。默认构造的 option 里这个值只是初始化状态；真实 widget 的样式值应以 `initStyleOption()` 填充结果为准。

### 10.2 `midLineWidth`

`midLineWidth` 是 frame 中间线的宽度。Qt 文档说明它通常用于绘制 sunken 或 raised frame。

默认值同样为 `0`。

这两个字段的语义和 `QStyleOptionFrame` 中的 frame 宽度字段相似，但本类并不继承 `QStyleOptionFrame`，而是直接继承 `QStyleOption`。因此不能把它当作普通 `QFrame` option 来强制转换：

```cpp
// 错误的思路：两者不是继承关系
// auto *frame = qstyleoption_cast<const QStyleOptionFrame *>(option);
```

正确做法是根据绘制入口使用对应类型：

```cpp
const auto *tabWidgetFrame =
    qstyleoption_cast<const QStyleOptionTabWidgetFrame *>(option);
```

## 11. 在 QProxyStyle 中定制页面 frame

`QStyle::PE_FrameTabWidget` 是一个 primitive。自定义 style 可以在 `drawPrimitive()` 中读取 `QStyleOptionTabWidgetFrame`：

```cpp
#include <QPainter>
#include <QProxyStyle>
#include <QStyleOptionTabWidgetFrame>

class TabWidgetFrameStyle final : public QProxyStyle
{
public:
    using QProxyStyle::QProxyStyle;

    void drawPrimitive(PrimitiveElement element,
                       const QStyleOption *option,
                       QPainter *painter,
                       const QWidget *widget = nullptr) const override
    {
        if (element == PE_FrameTabWidget) {
            if (const auto *frame =
                    qstyleoption_cast<const QStyleOptionTabWidgetFrame *>(option)) {
                const QRect frameRect = frame->rect;
                const QRect tabsRect = frame->tabBarRect;
                const QRect selectedRect = frame->selectedTabRect;

                Q_UNUSED(widget);
                Q_UNUSED(tabsRect);
                Q_UNUSED(selectedRect);

                // 这里可以根据 frame 的几何字段增加自定义绘制。
                // 仍然交给基础 style 绘制，避免丢失平台主题的其余细节。
                painter->save();
                painter->setPen(QPen(Qt::red, qMax(1, frame->lineWidth)));
                painter->drawRect(frameRect.adjusted(0, 0, -1, -1));
                painter->restore();
            }
        }

        QProxyStyle::drawPrimitive(element, option, painter, widget);
    }
};
```

这个示例故意保留了基础 style 调用，便于理解代理样式的职责。实际项目中，如果自己绘制了完整 frame，又让基础 style 再绘制一遍，可能出现边线加粗；更稳妥的做法是：

- 只叠加一小段自定义装饰，然后调用基础 style；
- 或者完全接管这个 primitive，并明确自己负责所有边框、缺口和方向；
- 不要在 `QTabBar` 的单 tab 绘制中重复绘制整个 `QTabWidget` frame。

`qstyleoption_cast()` 比无条件 `static_cast` 更合适，因为 style 接收到的参数类型是 `const QStyleOption *`，需要根据 option 的 `type` 和 `version` 安全识别具体子类。

## 12. `PE_FrameTabWidget`、`PE_FrameTabBarBase` 和 `CE_ShapedFrame`

可以用下面这张表快速定位：

| 绘制入口 | option 子类 | 画什么 |
| --- | --- | --- |
| `PE_FrameTabWidget` | `QStyleOptionTabWidgetFrame` | QTabWidget 页面区域外围的 frame。 |
| `PE_FrameTabBarBase` | `QStyleOptionTabBarBase` | 通常属于独立 QTabBar 的共享底座。 |
| `CE_TabBarTab` / `CE_TabBarTabShape` / `CE_TabBarTabLabel` | `QStyleOptionTab` | 单个 tab 的整体、形状或标签内容。 |
| `CE_ShapedFrame` | `QStyleOptionFrame` | 一般 QFrame 的形状 frame。 |

如果问题是“QTabWidget 的内容区边框和选中 tab 接不上”，先检查：

1. 是否把 `QStyleOptionTabWidgetFrame` 传给了 `PE_FrameTabWidget`；
2. 是否正确使用 `selectedTabRect`；
3. 是否根据 `shape` 处理了 North、South、West、East；
4. 是否错误地把 `tabBarRect` 当成单个 tab；
5. 是否同时绘制了基础 frame 和自己的完整 frame。

如果问题是“独立 QTabBar 的底线不对”，检查的才是 `QStyleOptionTabBarBase` 和 `PE_FrameTabBarBase`。

## 13. 生命周期、所有权和线程边界

`QStyleOptionTabWidgetFrame` 是一个轻量值类型：

- 不继承 `QObject`；
- 没有 parent；
- 不拥有 `QTabWidget`、`QTabBar`、corner widget 或 `QPainter`；
- 可以在栈上创建；
- 复制构造和赋值只复制字段；
- 不能保存从绘制函数传入的 option 指针，供之后的事件使用；
- 访问真实 widget 状态时仍应遵守 GUI 线程规则。

典型写法是：

```cpp
void MyTabWidget::paintEvent(QPaintEvent *event)
{
    QTabWidget::paintEvent(event);

    QStyleOptionTabWidgetFrame option;
    initStyleOption(&option);
    // 只在当前调用期间读取 option。
}
```

如果要缓存数据，应复制自己真正需要的 `QRect`、`QSize`、整数和枚举，而不是缓存 `option` 指针。

## 14. 默认值和头文件勘误

Qt 6.11.1 头文件中声明：

```cpp
enum StyleOptionType { Type = SO_TabWidgetFrame };
enum StyleOptionVersion { Version = 1 };
```

直接成员的默认值如下：

| 字段 | 默认值 |
| --- | --- |
| `lineWidth` | `0` |
| `midLineWidth` | `0` |
| `shape` | `QTabBar::RoundedNorth` |
| `tabBarSize` | `QSize(-1, -1)` |
| `rightCornerWidgetSize` | `QSize(-1, -1)` |
| `leftCornerWidgetSize` | `QSize(-1, -1)` |
| `tabBarRect` | null `QRect` |
| `selectedTabRect` | null `QRect` |

需要注意，Qt 6.11.1 离线类文档的 `Version` 说明列存在不一致：值列和安装头文件都是 `1`，说明列写成了 `2`。本笔记以实际头文件的 `Version = 1` 为准。

## 15. 常见误区与排查

### 15.1 “我创建了 option，为什么字段都是空的”

默认构造只会写入默认值，不会自动读取某个 `QTabWidget`。

在 `QTabWidget` 子类中调用：

```cpp
QStyleOptionTabWidgetFrame option;
initStyleOption(&option);
```

### 15.2 “我把 `tabBarSize` 当成 tab bar 的位置”

`tabBarSize` 只有尺寸。需要位置和尺寸时使用 `tabBarRect`。

### 15.3 “我用 `selectedTabRect` 判断当前 tab index”

它只是一块矩形。要获取当前 index，应使用 `QTabWidget::currentIndex()` 或 `QTabBar::currentIndex()`。

### 15.4 “我把 `QStyleOptionTabWidgetFrame` 转成了 `QStyleOptionFrame`”

两者都和 frame 有关，但不是继承关系。使用 `PE_FrameTabWidget` 时要转换成 `QStyleOptionTabWidgetFrame`。

### 15.5 “我把独立 QTabBar 的 base 逻辑复制到 QTabWidget”

独立 `QTabBar` 的 base 和 `QTabWidget` 的页面 frame 是两个绘制职责。前者使用 `QStyleOptionTabBarBase`，后者使用本类。

### 15.6 “我只修改了 `QTabWidget::setTabShape()`，但 frame 仍然错位”

frame 还受到 tab position、当前选中 tab 几何、corner widget 和 style 的边框宽度影响。不要只检查形状枚举，应该把 `shape`、`tabBarRect`、`selectedTabRect` 和两个 corner size 一起打印出来。

## API 速查表
### 16.1 本类直接 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `QStyleOptionTabWidgetFrame::StyleOptionType` | 描述页面 frame option 类型的枚举。 | 该类的 `Type` 值是 `SO_TabWidgetFrame`。 |
| 类型值 | `QStyleOptionTabWidgetFrame::Type` | 提供本类的运行时类型标识。 | 供 Qt 和 `qstyleoption_cast()` 安全识别。 |
| 类型 | `QStyleOptionTabWidgetFrame::StyleOptionVersion` | 描述 option 数据布局版本的枚举。 | Qt 6.11.1 基类版本值为 `1`。 |
| 类型值 | `QStyleOptionTabWidgetFrame::Version` | 提供当前 option 的数据布局版本常量。 | 以安装头文件为准；版本用于兼容识别，不是 Qt 版本号。 |
| 构造 | `QStyleOptionTabWidgetFrame()` | 创建一个带默认字段值的 `QTabWidget` 页面 frame option。 | 不会自动绑定或读取任何 `QTabWidget`，默认矩形和尺寸可能无效。 |
| 构造 | `QStyleOptionTabWidgetFrame(const QStyleOptionTabWidgetFrame &other)` | 创建另一个页面 frame option 的字段副本。 | 只复制绘制参数，不复制 `QTabWidget`、tab bar、corner widget 或 painter。 |
| 赋值 | `operator=(const QStyleOptionTabWidgetFrame &other)` | 将另一个 option 的字段复制到当前对象。 | 是值复制，不转移任何控件所有权。 |
| 保护构造 | `QStyleOptionTabWidgetFrame(int version)` | 按指定版本构造 option，供兼容扩展使用。 | `protected`，普通业务代码不能直接调用。 |
| 公共字段 | `int lineWidth` | 提供页面 frame 主边线的绘制宽度。 | 默认 `0`；真实 widget 的值应由 `QTabWidget::initStyleOption()` 填充。 |
| 公共字段 | `int midLineWidth` | 提供页面 frame 中间线的绘制宽度。 | 常用于 raised/sunken frame；默认 `0`，不要把它当内容边距。 |
| 公共字段 | `QTabBar::Shape shape` | 提供 tab bar 的方向和轮廓形状。 | 默认 `QTabBar::RoundedNorth`；不同于 `QTabWidget::TabShape`。 |
| 公共字段 | `QSize tabBarSize` | 提供 tab bar 的宽高。 | 只有尺寸没有位置；默认 invalid size，位置要看 `tabBarRect`。 |
| 公共字段 | `QSize rightCornerWidgetSize` | 提供右侧 corner widget 占用的尺寸。 | 只提供布局信息，不拥有真实 widget；默认 invalid size。 |
| 公共字段 | `QSize leftCornerWidgetSize` | 提供左侧 corner widget 占用的尺寸。 | 只提供布局信息，不拥有真实 widget；默认 invalid size。 |
| 公共字段 | `QRect tabBarRect` | 提供整条 tab bar 在当前 frame 坐标中的矩形。 | 表示所有 tab 的整体区域，不是单个 tab 或 tab bar size。 |
| 公共字段 | `QRect selectedTabRect` | 提供当前选中 tab 的矩形。 | 用于 frame 与选中 tab 的连接或缺口；默认可能是 null rectangle。 |

### 16.2 继承字段和协作 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 继承字段 | `QStyleOption::rect` | 指定 `PE_FrameTabWidget` 当前要处理的整体绘制区域。 | 不等于 `tabBarRect`，也不等于页面内容 widget 的内部矩形。 |
| 继承字段 | `QStyleOption::state` | 提供启用、活动、焦点等通用 style 状态。 | frame style 可结合它决定状态外观，但页面切换仍由 QTabWidget 完成。 |
| 继承字段 | `QStyleOption::type` | 提供运行时 option 类型编号。 | 不要手工猜类型，优先使用 `qstyleoption_cast()`。 |
| 继承字段 | `QStyleOption::version` | 提供 option 数据布局版本。 | 用于 style option 兼容识别，不是业务版本号。 |
| 初始化 | `QTabWidget::initStyleOption(QStyleOptionTabWidgetFrame *option) const` | 用真实 QTabWidget 的 tab position、frame、当前 tab 和 corner widget 状态填充 option。 | `protected`；QTabWidget 子类读取当前 frame 参数的首选入口。 |
| 初始化 | `QStyleOption::initFrom(const QWidget *widget)` | 用 widget 填充方向、矩形、调色板、字体等基类状态。 | 不能替代 QTabWidget 专属字段的初始化。 |
| 绘制 | `QStyle::drawPrimitive(QStyle::PE_FrameTabWidget, ...)` | 绘制 QTabWidget 页面区域外围 frame。 | option 必须是本类；不要把独立 tab bar base option 传进来。 |
| 类型转换 | `qstyleoption_cast<const QStyleOptionTabWidgetFrame *>(option)` | 从基类 option 安全获取页面 frame option。 | 会检查 type/version；失败返回 `nullptr`。 |
| 配置 | `QTabWidget::setTabPosition(QTabWidget::TabPosition)` | 设置 tab 位于 North、South、West 或 East。 | 会改变 `shape`、tabBarRect、selectedTabRect 和 frame 衔接方向。 |
| 配置 | `QTabWidget::setTabShape(QTabWidget::TabShape)` | 设置 tab 采用 Rounded 或 Triangular 形状。 | QTabWidget 会把高层配置转换成 `QTabBar::Shape`。 |
| 配置 | `QTabWidget::setCornerWidget(QWidget *, Qt::Corner)` | 在 tab widget 角落放置控件。 | 主要为 North/South 设计；控件所有权和几何由 QTabWidget 管理。 |
| 配置 | `QTabWidget::setDocumentMode(bool)` | 设置文档式 tab 外观提示。 | 影响 style 表现，不会改变 option 的生命周期或所有权。 |
| 对比 | `QStyle::PE_FrameTabBarBase` | 绘制独立 QTabBar 的共享底座。 | 使用 `QStyleOptionTabBarBase`，不能用本类替代。 |
| 对比 | `QStyle::CE_ShapedFrame` | 绘制一般 QFrame 的形状 frame。 | 使用 `QStyleOptionFrame`，和本类不是继承关系。 |

---

### 一句话总结

`QStyleOptionTabWidgetFrame` 是 `QTabWidget` 页面 frame 的一次性绘制参数：`rect` 是整体绘制区域，`tabBarRect` 是整条 tab bar，`selectedTabRect` 是当前选中 tab，两个 corner size 用来给角落控件留空间，`lineWidth` 和 `midLineWidth` 描述 frame 线宽。普通代码通过 `QTabWidget` 配置它，自定义 style 则在 `PE_FrameTabWidget` 中读取它。
