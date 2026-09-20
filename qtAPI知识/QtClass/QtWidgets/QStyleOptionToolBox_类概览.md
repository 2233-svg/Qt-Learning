# Qt QStyleOptionToolBox 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleOptionToolBox>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionToolBox`  
> 关键词：`QToolBox`、页面标题条、`QStyle`、`CE_ToolBoxTab`

## 1. 先说结论：它画的是 QToolBox 的一条页面标题

`QStyleOptionToolBox` 是 `QStyle` 绘制 `QToolBox` **某个页面标题条**时使用的参数。

`QToolBox` 是一种“手风琴式”的页面容器：它保存多个页面，但一次通常只展示一个页面；每个页面都有一条标题，标题条垂直堆叠。用户点击某个标题，就切换到对应页面。

```text
QToolBox
┌─────────────────────────────────┐
│ [图标] 常规设置                  │  <- 一条页面标题
│  常规设置页内容                  │  <- 当前选中页面
├─────────────────────────────────┤
│ [图标] 网络                      │  <- 一条页面标题
├─────────────────────────────────┤
│ [图标] 高级                      │  <- 一条页面标题
└─────────────────────────────────┘
```

本类描述的正是上图中的“一条页面标题”，而不是整个 `QToolBox` 容器，也不是被展开的页面 widget。

它提供给 style 的信息包括：

- 标题文字 `text`；
- 标题图标 `icon`；
- 该标题在所有标题中的位置 `position`；
- 当前选中标题是否紧挨着它 `selectedPosition`；
- 基类里的矩形、启用状态、选中状态、调色板和布局方向。

职责边界可以这样记：

```text
QToolBox
  ├─ 管理页面 QWidget、当前页和标题数据
  ├─ 在内部为每个页面维护可点击的标题条
  └─ 为标题条构造 QStyleOptionToolBox
        └─ QStyle::drawControl(CE_ToolBoxTab, ...)
```

它不是：

- `QToolBox` 自身的业务 API。页面增删、切换仍使用 `QToolBox`；
- `QTabWidget` 或 `QTabBar` 的 option；
- 一个存储页面 widget 指针的容器；
- 一个可以手动改写后让 `QToolBox` 改变当前页的控制对象。

## 2. QToolBox 适合解决什么问题

`QToolBox` 适合页面数量不多、每页主题清晰、希望用户在同一窄侧栏或设置面板中逐项展开的场景，例如：

- 偏好设置中的“常规 / 网络 / 高级”页面；
- 属性面板中的“布局 / 外观 / 数据”分组；
- 工具窗口中按功能分组的少量配置页。

它不适合：

- 很多页且需要快速随机跳转的情况，此时 `QTabWidget` 或侧边栏导航通常更合适；
- 同时展示多组内容的情况，此时用多个 `QGroupBox` 或自定义布局更直接；
- 单个可折叠区块的情况，此时应做专门的 collapsible section，而不是引入一个页面容器。

普通应用先使用 `QToolBox`，不需要自己创建 `QStyleOptionToolBox`：

```cpp
#include <QFormLayout>
#include <QLabel>
#include <QLineEdit>
#include <QToolBox>
#include <QVBoxLayout>
#include <QWidget>

auto *toolBox = new QToolBox;

auto *generalPage = new QWidget;
auto *generalLayout = new QFormLayout(generalPage);
generalLayout->addRow("名称：", new QLineEdit);

auto *networkPage = new QWidget;
auto *networkLayout = new QVBoxLayout(networkPage);
networkLayout->addWidget(new QLabel("网络代理和连接设置"));
networkLayout->addStretch();

toolBox->addItem(generalPage, "常规");
toolBox->addItem(networkPage, "网络");
toolBox->setCurrentIndex(0);
```

当 Qt 绘制“常规”和“网络”这两条标题时，内部才会构造对应的 `QStyleOptionToolBox`。

## 3. 它与 QTabWidget、QToolButton 的边界

| 类型 | 描述对象 | 典型绘制入口 | 何时使用 |
| --- | --- | --- | --- |
| `QStyleOptionToolBox` | QToolBox 中的一条页面标题。 | `CE_ToolBoxTab` | 自定义手风琴式页面标题。 |
| `QStyleOptionTab` | QTabBar 中的一个 tab。 | `CE_TabBarTab` | 自定义 `QTabWidget` / `QTabBar` 标签页。 |
| `QStyleOptionToolButton` | 一个工具按钮。 | `CE_ToolButtonLabel` 等 | 自定义工具栏或普通工具按钮。 |
| `QStyleOptionButton` | 一个普通按钮。 | `CE_PushButton` / `CE_CheckBox` 等 | 自定义普通按钮、复选框、单选按钮。 |

`QToolBox` 的标题虽然可以点击，但不要把它当作应用层的 `QToolButton`。它的绘制语义有两项专属相邻关系：`position` 和 `selectedPosition`。这两项正是本类存在的原因。

## 4. 真正的绘制入口：CE_ToolBoxTab

整个标题条由：

```cpp
QStyle::drawControl(QStyle::CE_ToolBoxTab, option, painter, widget)
```

绘制。Qt 的 style 系统也定义了更细的入口：

| 绘制元素 | 绘制内容 | option 类型 |
| --- | --- | --- |
| `CE_ToolBoxTab` | 完整标题条，包括形状和标签。 | `QStyleOptionToolBox` |
| `CE_ToolBoxTabShape` | 标题条背景、边框和选中连接关系。 | `QStyleOptionToolBox` |
| `CE_ToolBoxTabLabel` | 图标和文字。 | `QStyleOptionToolBox` |
| `SE_ToolBoxTabContents` | 标题条中图标与文字可用的内部矩形。 | `QStyleOptionToolBox` |

自定义 style 时：

- 只想给整条标题加一个轻量效果，优先处理 `CE_ToolBoxTab`；
- 只想改背景和相邻边界，可以处理 `CE_ToolBoxTabShape`；
- 只想改文字、图标或文本布局，可以处理 `CE_ToolBoxTabLabel`；
- 需要获取 label 可用区域时，调用 `subElementRect(SE_ToolBoxTabContents, ...)`。

不要在 `QToolBox::paintEvent()` 里直接把所有标题重画一遍。标题条由 `QToolBox` 的内部结构管理，style 才是改变它们外观的正确扩展点。

## 5. `text` 和 `icon`：当前标题的内容

### 5.1 `text`

`text` 是当前页面标题显示的文本。

它来自应用层对应的：

```cpp
toolBox->addItem(page, "网络");
toolBox->setItemText(index, "连接");
```

它的默认值是空 `QString`。默认构造 option 并不会读取任何 `QToolBox` 中的标题。

style 绘制时不应擅自把它当作永远可完整显示的字符串：

- 标题矩形可能不足；
- 字体和系统缩放会改变文本宽度；
- 文本可能含有 `&` 快捷键标记；
- 右到左布局会影响图标和文字的视觉位置。

如果要自行画 label，应使用 `QStyleOption` 的 `fontMetrics`、`direction`，并基于 `SE_ToolBoxTabContents` 的结果安排内容。

### 5.2 `icon`

`icon` 是当前页面标题的 `QIcon`，来源通常是：

```cpp
toolBox->addItem(page, QIcon(":/icons/network.svg"), "网络");
toolBox->setItemIcon(index, QIcon(":/icons/network.svg"));
```

默认值是空 `QIcon`，没有 pixmap，也没有文件名。

不要把 `icon` 当成某个固定尺寸的 pixmap。`QIcon` 会根据当前屏幕缩放、状态和 style 请求合适的图像；工具箱标题常使用 `QStyle::PM_SmallIconSize` 作为合适的默认尺寸参考。

## 6. `position`：这一条标题在工具箱中的纵向位置

`position` 的类型是 `TabPosition`：

```cpp
enum QStyleOptionToolBox::TabPosition {
    Beginning,
    Middle,
    End,
    OnlyOneTab
};
```

它描述当前标题在所有标题中的位置：

| 取值 | 含义 |
| --- | --- |
| `Beginning` | 当前标题是工具箱最上面的第一条标题。 |
| `Middle` | 当前标题位于中间。 |
| `End` | 当前标题是最下面的一条标题。 |
| `OnlyOneTab` | 工具箱中只有这一条标题。 |

例如有三个页面：

```text
[ 常规 ]  -> Beginning
[ 网络 ]  -> Middle
[ 高级 ]  -> End
```

如果只有一个页面，它的 `position` 是 `OnlyOneTab`。

style 会使用这个信息处理标题条的外部边框，例如顶部圆角、底部圆角、连续边线或相邻标题之间的衔接。它不表示当前页序号，也不表示是否选中。

不要用 `position` 替代 `QToolBox::currentIndex()`：

- `position` 只告诉你第一、中间、最后或唯一；
- `currentIndex()` 才是应用逻辑需要的具体 index。

## 7. `selectedPosition`：选中的标题是否与当前标题相邻

`selectedPosition` 的类型是 `SelectedPosition`：

```cpp
enum QStyleOptionToolBox::SelectedPosition {
    NotAdjacent,
    NextIsSelected,
    PreviousIsSelected
};
```

它回答的不是“当前标题选中了没有”，而是：

> 已选中的那条标题，是否紧挨着当前正在绘制的这条标题？如果紧挨着，在它的上方还是下方？

| 取值 | 含义 |
| --- | --- |
| `NotAdjacent` | 当前标题不紧挨着选中标题，或者当前标题本身就是选中的标题。 |
| `NextIsSelected` | 下一条标题通常是下方标题，且它被选中。 |
| `PreviousIsSelected` | 前一条标题通常是上方标题，且它被选中。 |

把它和 `state` 分开看：

```text
state & State_Selected     -> “当前这条标题是否选中”
selectedPosition           -> “相邻那条标题是否选中”
```

例如当前页是“网络”：

```text
[ 常规 ]  -> NextIsSelected
[ 网络 ]  -> NotAdjacent，同时 state 包含 State_Selected
[ 高级 ]  -> PreviousIsSelected
```

为什么 style 需要这项信息？选中的标题通常与展开页面视觉相连，边框、背景或圆角可能覆盖到相邻标题之间的边界。只知道“我自己是否选中”不足以让 style 正确处理上下两条边线。

最常见的误解是把 `NotAdjacent` 当成“没有选中页面”。它也可以表示当前标题就是选中标题；真正的选中判断应检查：

```cpp
option->state.testFlag(QStyle::State_Selected)
```

## 8. 选择、按下与禁用：应读取基类 state

`QStyleOptionToolBox` 自己没有 `selected` 或 `pressed` 的布尔字段。它使用继承自 `QStyleOption` 的 `state`：

| 状态 | 含义 |
| --- | --- |
| `QStyle::State_Selected` | 当前标题对应当前显示的页面。 |
| `QStyle::State_Sunken` | 用户正用鼠标按下当前标题。 |
| `QStyle::State_Enabled` | 当前标题可用。 |
| `QStyle::State_MouseOver` | 鼠标悬停状态，是否使用由具体控件与 style 决定。 |

这里有两个层次：

1. `QToolBox::setCurrentIndex()` 改变当前显示页面；
2. 绘制时，Qt 将当前标题标为 `State_Selected`，并在它被按住时加入 `State_Sunken`。

应用代码改变当前页应使用：

```cpp
toolBox->setCurrentIndex(index);
toolBox->setCurrentWidget(networkPage);
```

不要通过手动给 `QStyleOptionToolBox::state` 添加 `State_Selected` 来尝试切换页面。那只会影响你当前调用 `drawControl()` 的一份临时绘制数据。

## 9. QToolBox 的页面所有权和标题数据来源

一个常见而重要的模式：

```cpp
auto *page = new QWidget;
toolBox->addItem(page, "常规");
```

页面被加入 `QToolBox` 后会成为其管理的子 widget；页面的显示、隐藏和最终销毁由这个容器关系处理。`QStyleOptionToolBox` 不拥有页面，也不保存页面指针，它仅复制当前标题的文本、图标和绘制状态。

常用页面 API 的职责如下：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 页面添加 | `addItem(QWidget *, const QString &)` | 在工具箱末尾添加一个页面和标题 | 页面会进入 `QToolBox` 管理；返回索引可用于后续配置 |
| 页面添加 | `addItem(QWidget *, const QIcon &, const QString &)` | 添加一个带图标标题的页面 | 图标只影响标题显示，不改变页面 widget 的内容或所有权规则 |
| 页面插入 | `insertItem(int, ...)` | 在指定位置插入页面 | 插入会改变后续页面索引；保存索引的代码要同步更新 |
| 页面移除 | `removeItem(int index)` | 从工具箱移除指定页面 | 只移除，不等于删除页面 widget；后续销毁或迁移由调用方处理 |
| 标题修改 | `setItemText(int, const QString &)` | 修改指定页面的标题文字 | 只影响标题区；助记键和翻译更新要按界面规则处理 |
| 标题修改 | `setItemIcon(int, const QIcon &)` | 修改指定页面标题图标 | 图标状态应和页面可用性、当前主题尺寸匹配 |
| 页面状态 | `setItemEnabled(int, bool)` | 启用或禁用某个页面标题 | 禁用页面仍在容器中，样式选项只反映绘制时状态 |
| 当前页面 | `setCurrentIndex(int)` | 切换当前显示页面 | 索引必须来自当前页面顺序；页面切换会影响后续绘制状态 |

移除页面时尤其要注意：`removeItem()` 只把页面从工具箱移除，不等于自动删除你手里的 `QWidget *`。需要销毁时应根据你的所有权设计显式处理，或将页面重新放到其他父对象中。

## 10. QToolBox 没有公开的 `initStyleOption()`

这点和许多 widget 有所不同。

`QToolBox` 的公开/受保护头文件中没有类似下面的 API：

```cpp
// QToolBox 没有公开这样的函数
// void initStyleOption(QStyleOptionToolBox *option) const;
```

原因在于 `QStyleOptionToolBox` 描述的是**内部的每一条标题**，而不是 `QToolBox` 整体。Qt 内部在为每条标题绘制时构造它，外部的 `QToolBox` 子类没有一个官方入口能够直接取得“第 N 条标题的完整真实 option”。

这意味着：

- 只想使用或配置工具箱时，使用 `QToolBox` API；
- 想观察真实 option，最可靠的位置是自定义 style 的 `drawControl()`；
- 想修改标题外观，也应使用 `QProxyStyle` / `QStyle`；
- 不要仅 `QStyleOptionToolBox option; option.initFrom(toolBox);` 后就认为它等于某条标题的状态。

`initFrom(toolBox)` 只能填充一般 widget 的基类信息，填不了某一条标题的 `text`、`icon`、`position`、`selectedPosition` 或 `State_Selected`。

## 11. 在 QProxyStyle 中读取并定制标题

下面的 style 保留平台默认绘制，再为当前选中的标题加一条左侧强调线：

```cpp
#include <QPainter>
#include <QPen>
#include <QProxyStyle>
#include <QStyleOptionToolBox>

class ToolBoxAccentStyle final : public QProxyStyle
{
public:
    using QProxyStyle::QProxyStyle;

    void drawControl(ControlElement element,
                     const QStyleOption *option,
                     QPainter *painter,
                     const QWidget *widget = nullptr) const override
    {
        if (element == CE_ToolBoxTab) {
            if (const auto *tab =
                    qstyleoption_cast<const QStyleOptionToolBox *>(option)) {
                QProxyStyle::drawControl(element, option, painter, widget);

                if (tab->state.testFlag(QStyle::State_Selected)) {
                    painter->save();
                    painter->setPen(QPen(Qt::darkCyan, 3));
                    painter->drawLine(tab->rect.topLeft(),
                                      tab->rect.bottomLeft());
                    painter->restore();
                }
                return;
            }
        }

        QProxyStyle::drawControl(element, option, painter, widget);
    }
};
```

安装到一个工具箱：

```cpp
toolBox->setStyle(new ToolBoxAccentStyle(toolBox->style()));
```

这里的关键是 `qstyleoption_cast()`：

```cpp
const auto *tab =
    qstyleoption_cast<const QStyleOptionToolBox *>(option);
```

它会验证 `type` 和兼容版本；转换不匹配时返回 `nullptr`。style 的回调参数是基类指针，不能假定所有 `CE_*` 入口都一定携带同一种 option。

若要完整接管标题绘制，必须同时正确处理：

- `rect` 和 `SE_ToolBoxTabContents`；
- `text` 的省略和快捷键；
- `icon` 的正常、禁用和高 DPI 显示；
- `State_Selected`、`State_Sunken`、禁用、悬停；
- `position` 和 `selectedPosition` 的上下边界衔接；
- `direction` 带来的左右镜像。

因此，通常更稳妥的做法是先调用基础 style，再叠加少量自定义视觉。

## 12. 与样式提示和尺寸的协作

工具箱标题的字体强调可由 style hint 决定：

```cpp
QStyle::SH_ToolBox_SelectedPageTitleBold
```

它描述“选中页面标题是否应加粗”的样式偏好。应用不应该为了让当前页标题加粗，直接修改 `QStyleOptionToolBox::fontMetrics` 或自行篡改 `state`；应由 style 根据 `State_Selected` 和该 hint 决定最终外观。

若要取标题内容区，使用：

```cpp
const QRect contents = style->subElementRect(
    QStyle::SE_ToolBoxTabContents, option, widget);
```

它比在 `rect` 上硬编码边距更可靠，因为不同 style、平台、字体和 DPI 下，标题条的内边距与图标间距可以不同。

## 13. 生命周期、复制和线程边界

`QStyleOptionToolBox` 是轻量值类型：

- 不继承 `QObject`，没有 parent；
- 不拥有 `QToolBox`、页面 `QWidget`、图标源文件或 `QPainter`；
- 可以在栈上创建；
- 复制构造和赋值会复制文本、图标、枚举和基类绘制字段；
- 绘制回调传入的 option 只应在该回调期间读取；
- 读取或改变真实 widget、绘制 GUI 都要在 GUI 线程完成。

特别注意 `QIcon` 是值类型，但它代表的是图标数据和查找行为；复制 option 并不会把任何页面或控件一并复制。

不要缓存从 `drawControl()` 收到的 `const QStyleOption *` 指针。若要在其他时刻使用信息，应复制所需的值：

```cpp
const QString title = tab->text;
const QIcon titleIcon = tab->icon;
const QRect titleRect = tab->rect;
const bool selected = tab->state.testFlag(QStyle::State_Selected);
```

## 14. 默认值与 Qt 6.11.1 文档勘误

默认构造时，本类直接字段的默认状态可概括为：

| 字段 | 默认状态 |
| --- | --- |
| `text` | 空字符串。 |
| `icon` | 空 `QIcon`。 |
| `position` | `OnlyOneTab`。 |
| `selectedPosition` | `NotAdjacent`。 |

类常量为：

```cpp
QStyleOptionToolBox::Type    // SO_ToolBox
QStyleOptionToolBox::Version // 1
```

Qt 6.11.1 的安装头文件明确声明 `Version = 1`。离线类页面的 `StyleOptionVersion` 说明列写成了 `2`，与实际值不一致；本笔记以 `C:\Qt\6.11.1\msvc2022_64\include\QtWidgets\qstyleoption.h` 中的定义为准。

## 15. 常见误区与排查顺序

### 15.1 “我改变了 `selectedPosition`，为什么当前页没有变化”

它只是相邻选中关系的绘制信息。切换页面要用：

```cpp
toolBox->setCurrentIndex(index);
```

### 15.2 “`NotAdjacent` 就表示当前标题没选中”

不对。当前标题自身被选中时，`selectedPosition` 也会是 `NotAdjacent`。检查 `state & State_Selected` 才能确认它是不是当前标题。

### 15.3 “我可以从 QToolBox 子类调用 `initStyleOption()` 吗”

不可以，`QToolBox` 没有公开或受保护的该函数。真实标题 option 由内部标题条构造；样式扩展应在 `drawControl()` 中读取。

### 15.4 “我把它当作 QStyleOptionTab 使用”

两者都描述可点击标题，但容器、几何和相邻语义不同。`QToolBox` 使用垂直堆叠的页面标题，`QTabBar` 使用 tab bar；对应绘制入口也不同。

### 15.5 “我把 page widget 存进 style option”

本类没有 page 指针。`QToolBox::widget(index)` 和 `currentWidget()` 才是取得页面对象的 API；style option 只携带绘制数据。

### 15.6 “我自己用 rect 减去固定边距画文字”

不同 style 的标题内边距和图标区大小不同。应优先读取 `SE_ToolBoxTabContents`，并处理 `direction`、字体度量和文本省略。

## API 速查表
### 16.1 本类直接 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `QStyleOptionToolBox::StyleOptionType` | 表示工具箱标题 option 类型的枚举。 | 具体类型值通过 `Type` 提供。 |
| 类型值 | `QStyleOptionToolBox::Type` | 提供值为 `SO_ToolBox` 的运行时类型标识。 | 供 Qt 和 `qstyleoption_cast()` 安全识别。 |
| 类型 | `QStyleOptionToolBox::StyleOptionVersion` | 表示工具箱 option 数据布局版本的枚举。 | 具体版本值通过 `Version` 提供。 |
| 类型值 | `QStyleOptionToolBox::Version` | 提供当前版本常量，Qt 6.11.1 中为 `1`。 | 以安装头文件为准，不要采用离线说明列误写的 `2`。 |
| 枚举 | `QStyleOptionToolBox::TabPosition` | 描述当前标题在所有工具箱标题中的纵向位置。 | 和 `QToolBox` 的 page index 不是一回事。 |
| 枚举值 | `Beginning` | 表示最上面第一条标题。 | style 可据此处理首条标题的外边界。 |
| 枚举值 | `Middle` | 表示位于中间的标题。 | 中间可以有多条标题。 |
| 枚举值 | `End` | 表示最下面的一条标题。 | style 可据此处理末条标题的外边界。 |
| 枚举值 | `OnlyOneTab` | 表示工具箱中只有一条标题。 | 是 `position` 的默认且有效语义。 |
| 枚举 | `QStyleOptionToolBox::SelectedPosition` | 描述当前标题与选中标题的相邻关系。 | 不等同于当前标题自身是否选中。 |
| 枚举值 | `NotAdjacent` | 表示不邻接选中标题，或当前标题自身就是选中项。 | 当前是否选中应读取 `state` 的 `State_Selected`。 |
| 枚举值 | `NextIsSelected` | 表示下一条标题通常位于下方且已选中。 | 用于处理当前标题下边界与选中背景的衔接。 |
| 枚举值 | `PreviousIsSelected` | 表示上一条标题通常位于上方且已选中。 | 用于处理当前标题上边界与选中背景的衔接。 |
| 公共字段 | `QString text` | 提供当前页面标题文字。 | 默认为空；自绘时要考虑省略、助记符和 RTL。 |
| 公共字段 | `QIcon icon` | 提供当前页面标题图标。 | 默认为空；实际 pixmap 尺寸由 style、DPI 和 icon mode 决定。 |
| 公共字段 | `TabPosition position` | 提供当前标题在标题列表中的位置。 | 只表示首、中、末或唯一，不是 page index。 |
| 公共字段 | `SelectedPosition selectedPosition` | 提供选中标题相对于当前标题的视觉邻接关系。 | 不能用来判断当前标题是否选中。 |
| 构造 | `QStyleOptionToolBox()` | 创建带默认字段值的工具箱标题绘制参数。 | 不会读取任何 QToolBox 页面标题或当前页状态。 |
| 构造 | `QStyleOptionToolBox(const QStyleOptionToolBox &other)` | 创建另一份 option 的值副本。 | 复制文字、图标和绘制状态，不复制页面 widget。 |
| 赋值 | `operator=(const QStyleOptionToolBox &other)` | 将另一个 option 的字段复制到当前对象。 | 仍然只是值复制，不转移 QToolBox 所有权。 |
| 保护构造 | `QStyleOptionToolBox(int version)` | 按指定版本构造，供兼容扩展使用。 | `protected`，普通业务代码不能直接调用。 |

### 16.2 继承字段和协作 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 继承字段 | `QStyleOption::rect` | 指定当前标题条的整体绘制矩形。 | 不是展开页面 widget 的矩形。 |
| 继承字段 | `QStyleOption::state` | 提供选中、按下、启用和悬停等通用状态。 | `State_Selected` 判断当前标题，`State_Sunken` 表示按下反馈。 |
| 继承字段 | `QStyleOption::fontMetrics` | 提供当前标题文字的字体度量。 | 自绘标题时用它计算宽度和省略，不要猜固定字号。 |
| 继承字段 | `QStyleOption::direction` | 提供左到右或右到左布局方向。 | 图标和文字的水平位置应支持 RTL。 |
| 继承字段 | `QStyleOption::palette` | 提供标题绘制使用的调色板。 | 自定义 style 应使用 palette 角色，而不是硬编码主题颜色。 |
| 绘制 | `QStyle::drawControl(QStyle::CE_ToolBoxTab, ...)` | 绘制完整工具箱标题条。 | option 应为本类；通常先调用基础 style 再叠加局部装饰。 |
| 绘制 | `QStyle::CE_ToolBoxTabShape` | 绘制标题条背景、形状和相邻边界。 | 完整接管时要同时处理 `position` 和 `selectedPosition`。 |
| 绘制 | `QStyle::CE_ToolBoxTabLabel` | 绘制标题条的图标和文字。 | 需结合 `icon`、`text`、字体度量和内容矩形。 |
| 几何 | `QStyle::subElementRect(QStyle::SE_ToolBoxTabContents, ...)` | 获取标题内部图标和文字的标准可用区域。 | 比在 `rect` 上硬编码固定内边距更能适配 style、DPI 和 RTL。 |
| 样式提示 | `QStyle::SH_ToolBox_SelectedPageTitleBold` | 指示选中页面标题是否采用粗体。 | 由 style 结合 `State_Selected` 决定最终外观。 |
| 类型转换 | `qstyleoption_cast<const QStyleOptionToolBox *>(option)` | 从基类 option 安全取得工具箱标题 option。 | 失败返回 `nullptr`；不能把普通 `QStyleOption` 无条件强转。 |
| 页面创建 | `QToolBox::addItem(QWidget *, text)` | 在末尾添加页面和标题。 | QToolBox 管理页面的显示和父子关系，option 不拥有页面。 |
| 页面创建 | `QToolBox::addItem(QWidget *, icon, text)` | 添加带图标和标题的页面。 | 图标会成为对应标题 option 的 `icon`。 |
| 页面插入 | `QToolBox::insertItem(index, ...)` | 在指定位置插入页面。 | 会改变其他标题的 index 和视觉 `position`。 |
| 页面移除 | `QToolBox::removeItem(index)` | 从工具箱移除指定页面。 | 移除不等于自动删除页面 widget；所有权需由调用方明确处理。 |
| 标题配置 | `QToolBox::setItemText(index, text)` | 修改页面标题文字。 | 下一次绘制会反映到 `option.text`，不会修改旧快照。 |
| 标题配置 | `QToolBox::setItemIcon(index, icon)` | 修改页面标题图标。 | 下一次绘制会反映到 `option.icon`。 |
| 标题配置 | `QToolBox::setItemEnabled(index, enabled)` | 设置页面标题是否可用。 | style 通常通过基类 `state` 绘制禁用状态。 |
| 页面切换 | `QToolBox::setCurrentIndex(index)` | 切换当前展示页面。 | 会改变标题的 `State_Selected` 和相邻关系。 |
| 页面切换 | `QToolBox::setCurrentWidget(widget)` | 通过页面 widget 切换当前页。 | widget 必须属于该工具箱。 |
| 查询 | `QToolBox::currentIndex() const` | 获取当前显示页面的 index。 | 用于业务逻辑，不要用 `position` 代替。 |
| 查询 | `QToolBox::currentWidget() const` | 获取当前显示页面 widget。 | 返回的是页面对象，不是标题 option。 |
| 通知 | `QToolBox::currentChanged(int)` | 当前页面改变时发出信号。 | 适合同步属性面板、导航状态和业务逻辑。 |

---

### 一句话总结

`QStyleOptionToolBox` 是 `QToolBox` 一条页面标题的临时绘制参数：`text` 和 `icon` 是标题内容，`position` 表示它在标题列中的纵向位置，`selectedPosition` 描述它与选中标题的相邻关系，真正的选中状态在 `state` 的 `State_Selected` 中。应用用 `QToolBox` 管页面，自定义外观则在 `CE_ToolBoxTab` 中读取本类。
