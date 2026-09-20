# Qt QStyleOptionTab 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleOptionTab>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionTab`  
> 常见协作者：`QTabBar`、`QTabWidget`、`QStyle`

## 1. 它解决什么问题

一个 tab 的外观取决于的不只是标题和是否选中。style 还需要知道：

- tab 在视觉序列的首、中、尾，还是正被拖动。
- 它是否紧邻当前选中的 tab，边界应如何衔接。
- tab bar 在上、下、左、右哪一侧，使用圆角还是三角形。
- 是否处于文档模式，是否有 tab bar 角落控件。
- 左右附加按钮占了多少空间，例如关闭按钮。
- 当前调用是在正常绘制还是计算最小尺寸。

`QStyleOptionTab` 把这些因素打包成一次 tab 绘制的上下文，供 `QStyle` 绘制 `CE_TabBarTab`、`CE_TabBarTabShape` 和 `CE_TabBarTabLabel`。

```text
QTabBar
  └─ 每个 tab 组装 QStyleOptionTab
       ├─ 形状、位置、相邻选择关系
       ├─ 标题、图标、左右按钮尺寸
       ├─ document mode、corner widget、尺寸测量标志
       └─ state（选中、启用、悬停、按下等）
  -> QStyle::drawControl()
       ├─ CE_TabBarTabShape
       └─ CE_TabBarTabLabel
```

它不是 tab bar，不管理页面切换、tab 插入删除或拖动重排。要实现这些行为，应使用 `QTabBar` 或 `QTabWidget`。

## 2. 普通应用怎样使用

大多数代码只配置 `QTabBar`：

```cpp
#include <QTabBar>

auto *tabs = new QTabBar;
tabs->addTab("欢迎");
tabs->addTab("日志");
tabs->setMovable(true);
tabs->setTabsClosable(true);
tabs->setDocumentMode(true);
```

由 `QTabBar` 在绘制时填入 `QStyleOptionTab`。直接处理 option 的典型场景是：

1. 继承 `QTabBar`，在重写的绘制/尺寸逻辑中保留 Qt 已计算好的 tab 状态。
2. 实现 `QStyle` 或 `QProxyStyle`，调整 tab 的背景、选中边界、关闭按钮留白或拖动动画视觉。
3. 排查 tab 在文档模式、RTL、关闭按钮或可拖动状态下的几何问题。

## 3. 构建与正确的初始化入口

### 3.1 CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

qmake 工程使用 `QT += widgets`。

### 3.2 `QTabBar` 子类中初始化一项 tab

`QTabBar::initStyleOption(QStyleOptionTab *, int tabIndex)` 会从真实 tab bar 填好该 index 的内容、几何、状态和附加控件尺寸。自定义子类不应手工猜测这些字段。

```cpp
#include <QStyleOptionTab>
#include <QTabBar>

class InspectableTabBar final : public QTabBar
{
public:
    using QTabBar::QTabBar;

protected:
    void inspectTab(int index) const
    {
        QStyleOptionTab option;
        initStyleOption(&option, index);

        // option.text、option.position、option.selectedPosition、
        // option.leftButtonSize 等均来自当前真实 tab。
    }
};
```

若需要自定义整项绘制，通常由 style 接管 `CE_TabBarTab`；若直接重写 `QTabBar` 的绘制流程，应先通过这个函数构建 option，再调用 `style()->drawControl()`，最后才叠加自己的局部内容。

## 4. 先分清三类“位置”

tab 相关字段中最容易混淆的是 `tabIndex`、`position` 与 `selectedPosition`。

| 字段 | 回答的问题 | 不能替代什么 |
| --- | --- | --- |
| `tabIndex` | 当前 option 表示哪个 tab index。 | 不表示它是不是首/尾或是否选中。 |
| `position` | 当前 tab 在视觉序列中的首、中、尾、唯一项或移动中。 | 不表示哪个 tab 被选中。 |
| `selectedPosition` | 选中 tab 是否与当前 tab 相邻。 | 不表示当前 tab 本身是否选中。 |

当前 tab 是否被选中，应查看继承的 `QStyleOption::state` 中的 `QStyle::State_Selected`。当当前 tab 自己就是选中项时，`selectedPosition` 仍是 `NotAdjacent`；这个字段只帮助 style 处理**相邻未选中 tab 与选中 tab 的接缝**。

```text
视觉顺序： [A] [B] [C] [D]
当前选择：       [B]

A: selectedPosition = NextIsSelected
B: State_Selected，selectedPosition = NotAdjacent
C: selectedPosition = PreviousIsSelected
D: selectedPosition = NotAdjacent
```

## 5. `TabPosition` 与 tab 拖动

`position` 的类型为 `TabPosition`：

| 值 | 含义 | style 为什么需要它 |
| --- | --- | --- |
| `Beginning` | 视觉上的第一项。 | 处理首端圆角、边界和连接线。 |
| `Middle` | 既非第一也非最后。 | 处理与两侧 tab 的普通衔接。 |
| `End` | 视觉上的最后一项。 | 处理末端边界。 |
| `OnlyOneTab` | 同时是第一和最后一项。 | 需要同时具备两端边界语义。 |
| `Moving` | tab 正因鼠标拖动或动画而移动。自 Qt 6.6 起提供。 | style 可提供移动中的过渡外观。 |

`QTabBar::setMovable(true)` 允许用户重排 tab，但不能由应用代码只设置 `position = Moving` 来开启拖动。该字段是 Qt 在拖动/动画期间向 style 传递的状态快照。

## 6. 外观和内容字段

### 6.1 形状、文档模式与基本内容

| 字段 | 含义 | 默认值或要点 |
| --- | --- | --- |
| `shape` | tab 的方向与形状，例如 `RoundedNorth`。 | 默认 `QTabBar::RoundedNorth`。 |
| `text` | tab 标题。 | 默认空字符串。 |
| `icon` | tab 图标。 | 默认空 `QIcon`。 |
| `iconSize` | style 绘制图标时使用的最大尺寸。 | 默认无效 `QSize(-1, -1)`，应由 style 默认值决定。 |
| `documentMode` | 是否采用适合主窗口文档 tab 的视觉提示。 | 默认 `false`；不改变 tab 行为。 |
| `row` | 当前 tab 所在行。 | 目前只能为 `0`，表示前排。 |
| `tabIndex` | 当前代表的 tab index。 | 默认 `-1`，表示未对应 tab bar 内的实际 tab。 |

`documentMode` 是给 style 的外观提示。它通常用于编辑器/浏览器型主窗口中的文档标签，而不是设置对话框的页面标签；在某些平台上会呈现更接近系统文档 tab 的样式。它不负责“文档是否已保存”“是否有关闭确认”等业务语义。

`iconSize` 为无效尺寸时，不等于图标不可见，而是让 style 通过自己的像素度量提供默认尺寸。普通业务代码应设置 `QTabBar::setIconSize()`，不要给一次绘制 option 强塞固定像素。

### 6.2 左右附加按钮

`leftButtonSize` 与 `rightButtonSize` 分别表示 tab 左、右侧附加控件的尺寸，例如关闭按钮、自定义状态按钮或固定图钉。

```cpp
tabs->setTabsClosable(true);  // 通常会出现关闭按钮
tabs->setTabButton(index, QTabBar::RightSide, customButton);
```

style 根据这两个尺寸为标题和图标计算剩余可用矩形，避免文字压到按钮上。它们默认都是无效 `QSize(-1, -1)`。

注意它们只报告尺寸，并不拥有按钮；按钮的创建、所有权和交互仍属于 `QTabBar`。

### 6.3 tab bar 角落控件

`cornerWidgets` 是 `CornerWidgets` 标志组合，表示 tab bar 所在区域是否有左右角落控件：

| 标志 | 值 | 含义 |
| --- | --- | --- |
| `NoCornerWidgets` | `0x00` | 两侧均没有角落控件。 |
| `LeftCornerWidget` | `0x01` | 左侧存在角落控件。 |
| `RightCornerWidget` | `0x02` | 右侧存在角落控件。 |

它是 flags，可组合左右两个标志。style 用此信息避免把 tab 绘制到 `QTabWidget::setCornerWidget()` 等角落区域下面；它不等于 tab 自己的 `leftButtonSize/rightButtonSize`。

## 7. `features`：绘制和尺寸测量有不同上下文

Qt 6.11.1 头文件公开 `TabFeatures features`。该字段在离线类页的变量摘要中未列出，但它确实是类的 public API。

| 标志 | 值 | 含义 |
| --- | --- | --- |
| `None` | `0x00` | 普通 tab。 |
| `HasFrame` | `0x01` | tab 位于 tab frame 上。 |
| `MinimumSizeHint` | `0x02` | 当前是在计算最小尺寸提示，不是常规尺寸提示。自 Qt 6.9 起提供。 |

`MinimumSizeHint` 的用途很容易被误解。它不是“强制该 tab 最小宽度”的设置，而是 Qt 在调用 style 进行最小尺寸测量时给出的上下文，让 style 在计算时采用合适的边距与装饰规则。

同样地，`HasFrame` 描述 tab 与 frame 的关系，帮助 style 处理重叠、底边和衔接；不应用于替代 `QTabWidget` 或手工画 frame。

## 8. 相邻选中关系与边界

`SelectedPosition` 的取值如下：

| 值 | 含义 |
| --- | --- |
| `NotAdjacent` | 当前 tab 不邻接选中 tab，或当前 tab 本身就是选中项。 |
| `NextIsSelected` | 下一个视觉 tab（通常右侧）被选中。 |
| `PreviousIsSelected` | 上一个视觉 tab（通常左侧）被选中。 |

不要只用 index 的加减判断左右相邻。RTL 布局、tab bar 形状和绘制方向都会影响视觉解释；Qt 填充的 option 已经给出了 style 应使用的语义。

## 9. 在自定义 style 中读取

`QStyle::CE_TabBarTab`、`CE_TabBarTabShape` 和 `CE_TabBarTabLabel` 需要 `QStyleOptionTab`。代理 style 中先安全转换：

```cpp
#include <QProxyStyle>
#include <QStyleOptionTab>

class TabAccentStyle final : public QProxyStyle
{
public:
    using QProxyStyle::QProxyStyle;

    void drawControl(ControlElement element,
                     const QStyleOption *option,
                     QPainter *painter,
                     const QWidget *widget = nullptr) const override
    {
        if (element == CE_TabBarTabShape) {
            if (const auto *tab =
                    qstyleoption_cast<const QStyleOptionTab *>(option)) {
                const bool isCurrent = tab->state & State_Selected;

                if (isCurrent && tab->documentMode) {
                    // 可在基础 style 绘制前后增加文档 tab 的局部视觉提示。
                }
            }
        }

        QProxyStyle::drawControl(element, option, painter, widget);
    }
};
```

不要对所有 style option 直接 `static_cast<QStyleOptionTab *>`。style 的入口接收基类指针，`qstyleoption_cast()` 会检查 type 和 version。

## 10. 生命周期、版本与文档勘误

`QStyleOptionTab` 是短生命周期值对象：

- 由 `QTabBar` 在一次绘制或尺寸计算中构造/填充。
- 不继承 `QObject`，没有父对象，不拥有 `QTabBar`、tab 按钮或 `QPainter`。
- 复制构造只复制当前绘制快照。
- option 指针不能保存到本次绘制之外。

Qt 6.11.1 头文件声明：

| 常量 | 值 |
| --- | --- |
| `QStyleOptionTab::Type` | `QStyleOption::SO_Tab` |
| `QStyleOptionTab::Version` | `1` |

离线文档详细说明和 version 的说明列仍写着 version 3，而同页值列和 Qt 6.11.1 头文件均为 `1`。本页按安装头文件记录 `Version = 1`。

## 11. 常见误区与排查

### 11.1 “我设置 `documentMode` 后 tab 就成为文档编辑器了”

不会。它只影响 style 的外观提示。关闭确认、未保存标记、恢复会话等仍需业务层实现。

### 11.2 “关闭按钮挡住了标题”

不要在自定义 tab label 绘制中假设整个 `option.rect` 都可用于文字。使用 Qt 已初始化的 `leftButtonSize/rightButtonSize`，或直接让 `CE_TabBarTabLabel` 处理标准布局。

### 11.3 “选中项左右的边框接不上”

不要只看 `State_Selected`。未选中但紧邻选中项的 tab 应依据 `selectedPosition` 绘制不同边界。

### 11.4 “拖动 tab 时我手工把 `position` 改为 `Moving`”

这不会启动重排或动画。拖动由 `QTabBar::setMovable(true)` 与事件处理实现；`Moving` 只是 Qt 报告给 style 的绘制状态。

### 11.5 “版本常量到底是 1 还是 3”

对 Qt 6.11.1，使用 `QStyleOptionTab::Version == 1`。离线文档的“3”是内容不一致，不应据此手写兼容性判断。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QStyleOptionTab()` | 创建并以默认值初始化一份 tab 绘制参数。 | 自定义 `QTabBar` 中应继续调用 `initStyleOption()` 填充真实 tab 状态。 |
| 构造 | `QStyleOptionTab(const QStyleOptionTab &other)` | 创建另一个 tab option 的值副本。 | 复制绘制快照，不拥有 tab bar、页面或附加按钮。 |
| 枚举 | `TabPosition` | 描述当前 tab 在视觉序列中的首、中、尾或移动状态。 | 它不表示当前 tab 是否选中。 |
| 枚举值 | `Beginning` | 表示视觉顺序中的第一个 tab。 | style 可据此处理首端边界和圆角。 |
| 枚举值 | `Middle` | 表示视觉顺序中间的 tab。 | 用于与两侧 tab 的普通衔接。 |
| 枚举值 | `End` | 表示视觉顺序中的最后一个 tab。 | style 可据此处理末端边界和圆角。 |
| 枚举值 | `OnlyOneTab` | 表示 tab bar 中只有这一项。 | 同时具备首端和末端语义。 |
| 枚举值 | `Moving` | 表示 tab 正因拖动或动画处于移动状态。 | Qt 6.6 起提供；它只是绘制状态，不会启动拖动。 |
| 枚举 | `SelectedPosition` | 描述选中 tab 与当前 tab 的视觉邻接关系。 | 当前 tab 自己选中时通常为 `NotAdjacent`，是否选中看 `state`。 |
| 枚举值 | `NotAdjacent` | 表示不邻接选中 tab，或当前 tab 自身就是选中项。 | 不能替代 `QStyle::State_Selected`。 |
| 枚举值 | `NextIsSelected` | 表示下一个视觉 tab 被选中。 | 用于处理与选中项相接的边界。 |
| 枚举值 | `PreviousIsSelected` | 表示上一个视觉 tab 被选中。 | 用于处理与选中项相接的另一侧边界。 |
| 枚举 | `CornerWidget` / `CornerWidgets` | 表示 tab bar 左右角落控件的 flags 集合。 | 可同时组合左右标志，和 tab 自身的左右按钮尺寸不同。 |
| 枚举值 | `NoCornerWidgets` | 表示 tab bar 没有角落控件。 | 是默认角落特征。 |
| 枚举值 | `LeftCornerWidget` | 表示存在左侧角落控件。 | style 应为角落区域保留空间。 |
| 枚举值 | `RightCornerWidget` | 表示存在右侧角落控件。 | style 应为角落区域保留空间。 |
| 枚举 | `TabFeature` / `TabFeatures` | 描述 tab 与 frame 的关系以及当前是否处于最小尺寸测量。 | 是绘制/测量输入，不是业务配置 API。 |
| 枚举值 | `None` | 表示没有额外 tab 特征。 | 是默认特征集合。 |
| 枚举值 | `HasFrame` | 表示 tab 位于 tab frame 上。 | style 可据此处理 frame 衔接和重叠。 |
| 枚举值 | `MinimumSizeHint` | 表示当前调用用于计算最小尺寸提示。 | Qt 6.9 起提供；不表示把 tab 最小宽度设成某个值。 |
| 类型常量 | `StyleOptionType::Type` | 提供值为 `SO_Tab` 的运行时类型标识。 | style 端用 `qstyleoption_cast()` 安全识别。 |
| 类型常量 | `StyleOptionVersion::Version` | 表示 tab option 数据布局版本，Qt 6.11.1 中为 `1`。 | 以安装头文件为准；离线说明中的其他版本值不应直接采用。 |
| 公共字段 | `QTabBar::Shape shape` | 提供 tab 的方向和轮廓形状。 | 默认 `RoundedNorth`；真实配置通过 `QTabBar::setShape()` 完成。 |
| 公共字段 | `QString text` | 提供 tab 标题文字。 | 修改真实标题应调用 `QTabBar::setTabText()`，不要改临时 option。 |
| 公共字段 | `QIcon icon` | 提供 tab 图标。 | 实际绘制尺寸由 `iconSize`、DPI 和当前 style 共同决定。 |
| 公共字段 | `int row` | 提供当前 tab 所在行。 | 当前 Qt 实现通常为 `0`；不要用它替代 tab index。 |
| 公共字段 | `TabPosition position` | 提供 tab 的视觉位置或移动状态。 | 不要从 index 数字手工推断，拖动和 RTL 会改变视觉语义。 |
| 公共字段 | `SelectedPosition selectedPosition` | 提供当前 tab 与选中 tab 的视觉邻接关系。 | 不表示当前 tab 自身是否被选中。 |
| 公共字段 | `CornerWidgets cornerWidgets` | 提供 tab bar 是否有左右角落控件的信息。 | 可包含左右两个 flags；不拥有角落控件。 |
| 公共字段 | `QSize iconSize` | 提供 style 绘制 tab 图标时使用的最大尺寸。 | 无效尺寸表示使用 style 默认值，不表示图标不可见。 |
| 公共字段 | `bool documentMode` | 提供是否采用文档式 tab 外观的样式提示。 | 只影响外观，不代表文档保存或关闭业务状态。 |
| 公共字段 | `QSize leftButtonSize` | 提供 tab 左侧附加按钮所占尺寸。 | 影响标题可用区域，但 option 不拥有按钮。 |
| 公共字段 | `QSize rightButtonSize` | 提供 tab 右侧附加按钮所占尺寸。 | 关闭按钮常位于此侧；尺寸只用于布局。 |
| 公共字段 | `TabFeatures features` | 提供 tab frame 关系和尺寸测量特征集合。 | 头文件公开的绘制上下文，不会反向改变 QTabBar。 |
| 公共字段 | `int tabIndex` | 提供当前 option 所代表的 tab index。 | 默认 `-1` 表示未关联实际 tab；它仍不同于视觉位置。 |
| 继承字段 | `QStyleOption::rect` | 指定当前 tab 的绘制矩形。 | 不等于整个 tab bar 区域，也不只代表文本区域。 |
| 继承字段 | `QStyleOption::state` | 提供选中、启用、悬停和按下等通用状态。 | `State_Selected` 才表示当前 tab 被选中。 |
| 初始化 | `QTabBar::initStyleOption(QStyleOptionTab *, int)` | 根据真实 tab index 填充完整 option。 | `QTabBar` 子类的首选入口，避免手工重建相邻关系和按钮几何。 |
| 行为配置 | `QTabBar::setMovable(bool)` | 设置用户能否拖动重排 tab。 | 不应通过把 `position` 改成 `Moving` 来代替。 |
| 绘制 | `QStyle::drawControl(QStyle::CE_TabBarTab, ...)` | 使用当前 style 绘制完整 tab。 | style 会结合 shape、state、相邻关系和按钮尺寸处理主题与 RTL。 |
| 类型转换 | `qstyleoption_cast<const QStyleOptionTab *>(option)` | 从基类 option 安全识别 tab option。 | 失败返回空指针，不能无条件 `static_cast`。 |

---

### 一句话总结

`QStyleOptionTab` 是一项 tab 的完整绘制快照：`position` 解决首尾和移动状态，`selectedPosition` 解决与当前选中项的接缝，按钮尺寸和 corner flags 解决可用内容区域，`features` 区分 frame 与最小尺寸测量；普通应用配置 `QTabBar`，自定义绘制时再让 style 读取这份上下文。
