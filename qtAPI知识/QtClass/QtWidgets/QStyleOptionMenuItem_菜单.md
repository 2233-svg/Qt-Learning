# Qt QStyleOptionMenuItem 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleOptionMenuItem>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionMenuItem`  
> 常见协作者：`QMenu`、`QAction`、`QActionGroup`、`QStyle`

## 1. 它解决什么问题

一项菜单并不只是“画一行文字”。同一个 `QMenu` 中，普通命令、带图标命令、可勾选项、互斥项、子菜单、分隔线与快捷键需要排在统一的列上；鼠标选中、禁用、按下、滚动提示等状态也要符合当前平台主题。

`QStyleOptionMenuItem` 是 `QMenu` 向 `QStyle` 描述“一次菜单项绘制”的数据包。它让 style 同时知道当前项的内容和整张菜单的公共对齐信息。

```text
QAction / QActionGroup
  └─ 文本、图标、可勾选、已勾选、快捷键、子菜单等业务状态
QMenu
  └─ 计算整张菜单中最大的图标列和快捷键列
QStyleOptionMenuItem
  └─ 汇总为一次 CE_MenuItem 绘制的参数
QStyle
  └─ 按平台主题画背景、文字、图标、勾选符号、子菜单箭头与快捷键
```

它不是 `QAction`，不负责触发命令；也不是 `QMenu`，不保存菜单项和键盘导航状态。它只是短生命周期的绘制快照。

## 2. 什么时候会直接使用

普通应用程序只要配置 `QMenu` 与 `QAction`：

```cpp
auto *fileMenu = menuBar()->addMenu("文件");
auto *openAction = fileMenu->addAction(QIcon(":/icons/open.svg"),
                                       "打开");
openAction->setShortcut(QKeySequence::Open);

auto *showGrid = fileMenu->addAction("显示网格");
showGrid->setCheckable(true);
```

`QMenu` 会自行填充 `QStyleOptionMenuItem`。直接使用本类主要见于：

1. 编写 `QStyle` / `QProxyStyle`，重绘 `QStyle::CE_MenuItem`、`CE_MenuScroller`、`CE_MenuTearoff` 或 `CE_MenuEmptyArea`。
2. 自绘菜单样式的控件，希望沿用当前 Qt style 对菜单项的排版规则。
3. 排查菜单图标、勾选列和快捷键列不对齐的问题。

要实现菜单功能时，优先操作 `QAction`、`QActionGroup` 和 `QMenu`；不要把 option 当成可持久修改的菜单模型。

## 3. 构建与最小绘制流程

### 3.1 CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

qmake 工程使用 `QT += widgets`。

### 3.2 绘制一个菜单风格的命令行

以下例子展示 option 的核心字段如何配合。真实 `QMenu` 会替你计算整张菜单的公共列宽；这里为了说明语义手工设置。

```cpp
#include <QPainter>
#include <QStyle>
#include <QStyleOptionMenuItem>
#include <QWidget>

class MenuRowPreview final : public QWidget
{
public:
    MenuRowPreview()
    {
        setMinimumSize(260, 34);
    }

protected:
    void paintEvent(QPaintEvent *) override
    {
        QPainter painter(this);

        QStyleOptionMenuItem option;
        option.initFrom(this);
        option.rect = rect().adjusted(4, 4, -4, -4);
        option.menuRect = rect();
        option.menuItemType = QStyleOptionMenuItem::Normal;
        option.text = "显示网格\tCtrl+G";
        option.checkType = QStyleOptionMenuItem::NonExclusive;
        option.checked = true;
        option.menuHasCheckableItems = true;
        option.maxIconWidth = 20;
        option.reservedShortcutWidth = fontMetrics().horizontalAdvance("Ctrl+G");

        style()->drawControl(QStyle::CE_MenuItem, &option, &painter, this);
    }
};
```

`text` 里的 `\t` 很关键：前半段是命令标题，后半段是快捷键显示文本。对于真实菜单，优先给 `QAction` 调用 `setShortcut()`，由 `QMenu` 生成正确的绘制文本；不要为了显示快捷键手工把 `"\tCtrl+G"` 拼进 action 文本。

## 4. 先分清：当前项字段与整张菜单字段

### 4.1 当前项自身的信息

| 字段 | 表达的内容 | 默认值 |
| --- | --- | --- |
| `menuItemType` | 这是什么种类的菜单项。 | `Normal` |
| `checkType` | 是否应预留/绘制勾选标记，以及标记是单选还是复选风格。 | `NotCheckable` |
| `checked` | 当前项是否已勾选。 | `false` |
| `text` | 命令文字，快捷键存在时用 `\t` 分隔。 | 空字符串 |
| `icon` | 当前项图标。 | 空 `QIcon` |
| `font` | 主菜单文字所用字体，不包含快捷键部分。 | 应用默认字体 |

`checkType` 和 `checked` 必须一起理解：

| `checkType` | `checked` | 典型效果 |
| --- | --- | --- |
| `NotCheckable` | 通常忽略 | 无勾选符号。 |
| `Exclusive` | `false` / `true` | 单选组风格，类似单选按钮。 |
| `NonExclusive` | `false` / `true` | 复选项风格，类似复选框。 |

实际业务层面，`QAction::setCheckable()` 决定是否可选中，`QAction::setChecked()` 设置状态，`QActionGroup` 决定互斥策略。不要只靠改 option 的 `checkType` 来实现互斥菜单。

### 4.2 整张菜单统一排版的信息

| 字段 | 表达的内容 | 为什么不是“当前项自己的值” |
| --- | --- | --- |
| `menuRect` | 整个菜单的矩形。 | style 可能据此计算边缘、滚动和空白区域。 |
| `maxIconWidth` | 所有相关菜单项中图标列需要保留的最大宽度。 | 即使当前项没有图标，也要对齐到其他有图标项。 |
| `reservedShortcutWidth` | 菜单中可见项的最大快捷键宽度。 | 每一项都要预留同样宽度，快捷键列才会对齐。 |
| `menuHasCheckableItems` | 整个菜单是否存在可勾选项。 | 没有任何可勾选项时，style 可以省去整列勾选留白。 |

`maxIconWidth` 很容易填错。它不是“本项图标的实际宽度”，而是**菜单图标列宽**；即便本项 `icon` 为空，也必须传入正确列宽，否者文字会相对其他项横向跳动。

`reservedShortcutWidth` 也是同理。`QMenu` 会将它设为所有可见项中最宽快捷键的宽度，而不是当前项快捷键的宽度。

## 5. `MenuItemType`：同一套 option 画不同菜单区域

| 枚举值 | 含义 | 常见绘制元素 |
| --- | --- | --- |
| `Normal` | 普通命令项。 | 文字、图标、快捷键、勾选状态。 |
| `DefaultItem` | `QMenu::defaultAction()` 指定的默认命令。 | style 可能用更醒目的字重或外观。 |
| `Separator` | 分隔线。 | 分割线或分组标题式 separator。 |
| `SubMenu` | 指向子菜单的项。 | 文字、图标与指向子菜单的箭头。 |
| `Scroller` | 弹出菜单滚动区域。 | 向上/向下滚动箭头；目前主要用于 macOS。 |
| `TearOff` | 菜单 tear-off 句柄。 | 可分离菜单的拖拽区域。 |
| `Margin` | 已弃用且不再使用的菜单边距项。 | Qt 6.11 起已弃用，不应在新代码中使用。 |
| `EmptyArea` | 菜单中没有项目覆盖的空白区域。 | 空白背景或占位区域。 |

`EmptyArea` 的数值是 `TearOff + 2`。不要依赖枚举的连续数值；尤其 `Margin` 已在 Qt 6.11 中弃用，未来版本的可见枚举项并不适合用整数序号处理。

`Scroller`、`TearOff`、`EmptyArea` 多数由 Qt 内部菜单逻辑创建。自定义 style 应支持它们的绘制分支，但普通应用代码不应手工伪造这些类型。

## 6. `text`、字体与快捷键列

### 6.1 文本格式

`text` 的格式是：

```text
菜单标题\t快捷键文本
```

例如：

```cpp
option.text = "另存为...\tCtrl+Shift+S";
```

style 可借助制表符把标题和快捷键画在不同列。没有快捷键时，只包含标题文本。

菜单标题中也可能含有 `&` 助记符，例如 `"打开(&O)"` 或 `"&Open"`；助记符具体显示方式由 action、平台规范和 style 共同处理，不要因为 option 文本看起来像普通字符串就丢掉这一层语义。

### 6.2 `font` 不等于整行文字的唯一字体

`font` 是主菜单文字所用的字体，**不包括快捷键部分**。Qt 文档明确指出，快捷键通常使用 `QPainter` 当前字体绘制。自定义 style 若把 `font` 同时强行用于快捷键，可能与平台菜单的典型排版不一致。

## 7. 状态、勾选与子菜单箭头

除本类字段外，style 还从继承的 `QStyleOption::state` 获得交互状态：

| 状态位 | 对菜单项的意义 |
| --- | --- |
| `QStyle::State_Selected` | 当前菜单项正被选中/高亮。 |
| `QStyle::State_Enabled` | 当前 action 可用。 |
| `QStyle::State_UpArrow` | `Scroller` 应绘制向上箭头。 |
| `QStyle::State_DownArrow` | `Scroller` 应绘制向下箭头。 |
| `QStyle::State_HasFocus` | 菜单栏拥有输入焦点时的焦点状态。 |

不要把 `checked` 与 `State_Selected` 混为一谈：

- `checked`：持久的命令状态，例如“显示网格”是否启用。
- `State_Selected`：鼠标或键盘当前停留在哪一行，会随导航立即变化。

同理，`SubMenu` 说明该项会展开子菜单；箭头向左还是向右需要考虑 `QStyleOption::direction` 的 LTR/RTL 布局方向。交给 `CE_MenuItem` 可以自动适配 RTL，不要硬编码右箭头。

## 8. 在自定义 style 中使用

自定义 style 应从 `QStyleOption *` 安全转换，并尽量在代理 style 基础上做小范围调整：

```cpp
#include <QProxyStyle>
#include <QStyleOptionMenuItem>

class MenuAccentStyle final : public QProxyStyle
{
public:
    using QProxyStyle::QProxyStyle;

    void drawControl(ControlElement element,
                     const QStyleOption *option,
                     QPainter *painter,
                     const QWidget *widget = nullptr) const override
    {
        if (element == CE_MenuItem) {
            if (const auto *item =
                    qstyleoption_cast<const QStyleOptionMenuItem *>(option)) {
                if (item->menuItemType == QStyleOptionMenuItem::DefaultItem) {
                    // 在保留基础 style 绘制前后，添加默认命令的局部提示。
                }
            }
        }

        QProxyStyle::drawControl(element, option, painter, widget);
    }
};
```

`qstyleoption_cast()` 会检查 option type 与 version。不要把任何 `CE_MenuItem` 的参数都强制转换并长期保存；option 只在当前绘制调用有效。

## 9. 生命周期、所有权与排查

`QStyleOptionMenuItem` 是公开字段的值类型：

- 栈上构造、填写、立即传给 `drawControl()`。
- 不拥有 `QMenu`、`QAction`、`QIcon`、`QPainter` 或 style。
- 复制构造会复制当前绘制快照，不会复制或接管菜单对象。

### 9.1 “菜单文字每行起点不一致”

检查 `maxIconWidth` 是否按整张菜单的最大图标列宽设置，且 `menuHasCheckableItems` 是否与菜单整体一致。只在带图标/勾选的当前项上填这些字段会造成列抖动。

### 9.2 “快捷键贴着标题，或每行位置不同”

检查 `text` 是否用 `\t` 分隔标题和快捷键，以及 `reservedShortcutWidth` 是否来自整张菜单最宽快捷键。不要只用本项的快捷键宽度。

### 9.3 “互斥项画成了复选框”

检查 action 是否属于正确的 `QActionGroup`，并确认绘制时 `checkType == Exclusive`。`checked == true` 只能说明已选中，不能说明应画圆点还是勾。

### 9.4 “我设置了 `DefaultItem`，回车却没有触发它”

`DefaultItem` 是绘制语义；实际默认 action 应通过 `QMenu::setDefaultAction()` 设置。不要把 style option 当作行为控制器。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QStyleOptionMenuItem()` | 创建并以默认值初始化一份菜单项绘制参数。 | 通常由 `QMenu` 内部填充；自绘时可在栈上创建并在当前调用中使用。 |
| 构造 | `QStyleOptionMenuItem(const QStyleOptionMenuItem &other)` | 创建另一个菜单项 option 的值副本。 | 复制绘制快照，不拥有 `QMenu`、`QAction`、painter 或 style。 |
| 枚举 | `CheckType` | 指定菜单项是否需要勾选标记，以及采用互斥还是非互斥样式。 | 必须和 `checked` 一起理解；真正的可勾选和互斥行为由 `QAction`、`QActionGroup` 管理。 |
| 枚举值 | `NotCheckable` | 表示当前菜单项不绘制勾选标记。 | 不代表 action 一定不可触发；它只描述当前 style 绘制语义。 |
| 枚举值 | `Exclusive` | 表示当前项采用互斥选择项的视觉形式，类似单选按钮。 | 通常来自互斥 `QActionGroup`；改 option 不会创建互斥关系。 |
| 枚举值 | `NonExclusive` | 表示当前项采用独立复选项的视觉形式。 | 常用于开关类 action；是否真的可切换仍看 action 配置。 |
| 枚举 | `MenuItemType` | 定义当前 option 描述的是普通项、分隔线、子菜单或菜单特殊区域。 | style 应按类型选择绘制路径，普通业务代码很少手工伪造特殊类型。 |
| 枚举值 | `Normal` | 表示普通命令菜单项。 | 是最常见的默认类型。 |
| 枚举值 | `DefaultItem` | 表示 `QMenu::defaultAction()` 指定的默认命令项。 | 只影响外观；默认 action 要通过 `QMenu` 配置。 |
| 枚举值 | `Separator` | 表示菜单分隔线或分组分隔区域。 | 不是可触发命令，通常由 `QAction::setSeparator()` 产生。 |
| 枚举值 | `SubMenu` | 表示指向子菜单的菜单项。 | 箭头方向和位置应交给 style 结合 `direction` 处理。 |
| 枚举值 | `Scroller` | 表示弹出菜单的滚动区域。 | 主要由 Qt 内部菜单逻辑使用，普通应用通常不手工设置。 |
| 枚举值 | `TearOff` | 表示菜单 tear-off 分离句柄。 | 只有启用相应菜单行为和 style 支持时才有意义。 |
| 枚举值 | `Margin` | 已弃用且未使用的菜单边距类型。 | Qt 6.11 起不应在新代码中依赖它。 |
| 枚举值 | `EmptyArea` | 表示菜单中没有菜单项覆盖的空白区域。 | 主要由 Qt 内部用于补足菜单绘制区域。 |
| 类型常量 | `StyleOptionType::Type` | 提供值为 `SO_MenuItem` 的运行时类型标识。 | style 端优先用 `qstyleoption_cast()` 识别。 |
| 类型常量 | `StyleOptionVersion::Version` | 表示菜单项 option 的数据布局版本，Qt 6.11.1 中为 `1`。 | 参与兼容性判断，不要手工改写。 |
| 公共字段 | `CheckType checkType` | 描述当前项的勾选标记类型。 | `Exclusive` 和 `NonExclusive` 只表达绘制风格，行为仍由 action 层完成。 |
| 公共字段 | `bool checked` | 表示当前菜单项是否处于已勾选状态。 | 与鼠标/键盘当前高亮的 `State_Selected` 完全不同。 |
| 公共字段 | `QFont font` | 提供菜单标题文字使用的字体。 | 快捷键部分通常按 painter 当前字体绘制，不要无条件共用此字段。 |
| 公共字段 | `QIcon icon` | 提供当前菜单项的图标。 | 实际图标列宽由 `maxIconWidth` 统一，不能只按当前图标尺寸排版。 |
| 公共字段 | `int maxIconWidth` | 提供整张菜单图标列需要保留的最大宽度。 | 即使当前项没有图标也要保持全菜单一致，否则每行标题会横向跳动。 |
| 公共字段 | `bool menuHasCheckableItems` | 表示整张菜单是否包含可勾选菜单项。 | style 可据此决定是否保留勾选列；它不是当前项的 `checkType`。 |
| 公共字段 | `MenuItemType menuItemType` | 提供当前菜单项或特殊菜单区域的类型。 | 决定 normal、separator、submenu 等绘制分支。 |
| 公共字段 | `QRect menuRect` | 提供整张菜单的矩形。 | 与当前项的 `rect` 不同；可用于菜单边缘、滚动和空白区域判断。 |
| 公共字段 | `int reservedShortcutWidth` | 提供整张菜单快捷键列需要预留的宽度。 | 应按菜单中最宽的可见快捷键计算，而不是只看当前项。 |
| 公共字段 | `QString text` | 提供菜单标题以及可选的快捷键显示文本。 | 快捷键通常按 `标题\t快捷键` 分隔；实际快捷键优先由 `QAction::setShortcut()` 提供。 |
| 继承字段 | `QStyleOption::rect` | 提供当前菜单项自身的绘制矩形。 | 与 `menuRect` 区分；它只覆盖当前行或特殊区域。 |
| 继承字段 | `QStyleOption::state` | 提供选中、启用、按下、滚动箭头等当前交互状态。 | 不要把 `State_Selected` 或 `State_Sunken` 和持久 `checked` 混为一谈。 |
| 绘制 | `QStyle::drawControl(QStyle::CE_MenuItem, ...)` | 让当前 style 绘制菜单项的背景、图标、勾选符号、文字、快捷键和子菜单箭头。 | 会结合主题、palette、direction 和 option 字段；自定义 style 应尽量保留基类绘制。 |
| 类型转换 | `qstyleoption_cast<const QStyleOptionMenuItem *>(option)` | 从基类 option 安全识别菜单项 option。 | 失败返回空指针；只在当前绘制调用期间读取，不要保存 option 指针。 |

---

### 一句话总结

`QStyleOptionMenuItem` 让 `QStyle` 同时看见一项菜单的命令状态和整张菜单的列对齐信息：用 `checkType/checked` 区分选择样式与持久状态，用 `text` 的制表符分隔标题和快捷键，用 `maxIconWidth` 与 `reservedShortcutWidth` 保证所有行对齐；普通应用只配置 `QAction` 和 `QMenu`，自绘或自定义 style 才直接处理它。
