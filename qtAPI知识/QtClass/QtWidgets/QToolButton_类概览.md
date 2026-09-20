# Qt QToolButton 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QToolButton>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QAbstractButton -> QToolButton`  
> 关键词：`QAction`、弹出菜单、分裂按钮、`QToolBar`

## 1. 先说结论：QToolButton 是命令或选项的紧凑入口

`QToolButton` 是强调图标、节省空间的按钮，通常用在 `QToolBar` 中，也可以独立放在任何布局里。

```text
QAction
  └─ QToolButton
       ├─ 单击执行默认命令
       ├─ 可选：长按或箭头弹出菜单
       └─ 可选：作为可选中的工具模式按钮
```

它适合：

- 工具栏中的新建、保存、撤销、对齐、缩放等高频命令；
- 画笔、选择、移动等可切换工具；
- “主要动作 + 更多选项”的分裂按钮；
- 后退、前进等“单击执行默认动作，长按选历史记录”的场景。

它不是普通表单的首选按钮。需要明确文字、确认性操作或主操作时，`QPushButton` 通常更合适。

## 2. 优先关联 QAction，而不是重复配置按钮

```cpp
#include <QAction>
#include <QToolButton>

auto *saveAction = new QAction(QIcon(":/save.svg"), "保存", this);
saveAction->setShortcut(QKeySequence::Save);
connect(saveAction, &QAction::triggered, this, &MainWindow::saveFile);

auto *saveButton = new QToolButton;
saveButton->setDefaultAction(saveAction);
```

设置默认 action 后，action 会同步决定按钮的：

- `checkable`、`checked`、`enabled`；
- `font`、`icon`、`text`；
- `statusTip`、`toolTip`、`whatsThis`；
- action 有 menu 时的 `popupMode`。

`autoRepeat` 等其他按钮属性不由 action 决定。一个 action 可以同时被菜单、快捷键和工具栏按钮使用，命令状态因此保持一致。

`QToolBar::addAction()` 通常会在内部创建这样的 `QToolButton`。如果手工创建按钮再 `addWidget()` 放入工具栏，则该按钮不再自动遵循工具栏的 `toolButtonStyle`。

## 3. 最小用法：图标按钮与可选中工具

```cpp
auto *selectTool = new QToolButton;
selectTool->setIcon(QIcon(":/select.svg"));
selectTool->setText("选择");
selectTool->setToolTip("选择工具");
selectTool->setCheckable(true);
selectTool->setAutoRaise(true);

connect(selectTool, &QToolButton::clicked, this, [this](bool checked) {
    if (checked) {
        setCurrentTool(SelectTool);
    }
});
```

多个互斥工具应使用 `QButtonGroup`，而不是在每个 `clicked` 槽中手工取消其他按钮：

```cpp
auto *tools = new QButtonGroup(this);
tools->setExclusive(true);
tools->addButton(selectTool);
tools->addButton(penTool);
```

## 4. `autoRaise`：为何工具栏里的按钮看起来像没有边框

`autoRaise` 为 `true` 时，按钮一般仅在鼠标悬停或按下时显示立体边框。独立创建的按钮默认 `false`；放入 `QToolBar` 后通常自动启用。

```cpp
button->setAutoRaise(true);
```

这是一种视觉策略，不改变点击、可选中或菜单行为。Qt 6.11.1 文档特别说明：macOS 使用 `QMacStyle` 时该属性目前会被忽略。

## 5. 箭头、图标和文字样式

### 5.1 `arrowType`

`arrowType` 可以用标准箭头代替普通 icon：

```cpp
backButton->setArrowType(Qt::LeftArrow);
```

常见值是 `LeftArrow`、`RightArrow`、`UpArrow`、`DownArrow`；默认是 `Qt::NoArrow`。箭头适合历史导航、折叠/展开、微调等方向明确的操作，不适合用来替代语义模糊的业务图标。

### 5.2 `toolButtonStyle`

```cpp
button->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
```

| 值 | 效果 |
| --- | --- |
| `ToolButtonIconOnly` | 仅图标，默认。 |
| `ToolButtonTextOnly` | 仅文字。 |
| `ToolButtonTextBesideIcon` | 图标在文字旁。 |
| `ToolButtonTextUnderIcon` | 图标在文字上。 |
| `ToolButtonFollowStyle` | 跟随系统/平台设置。 |

在 `QMainWindow` 的工具栏中，工具按钮会自动响应主窗口的工具按钮样式和图标尺寸变化。独立按钮则由自身属性、父控件和 style 决定。

## 6. 菜单按钮的三种 popupMode

先关联菜单：

```cpp
auto *menu = new QMenu(this);
menu->addAction("12 px");
menu->addAction("16 px");

auto *sizeButton = new QToolButton;
sizeButton->setDefaultAction(currentSizeAction);
sizeButton->setMenu(menu);
```

`setMenu()` 不转移菜单所有权，menu 仍应有可靠 parent，例如主窗口或按钮的父对象。

### 6.1 `DelayedPopup`

默认模式。短按触发按钮自身 action；按住一段时间后才弹出菜单。延迟由 style hint `QStyle::SH_ToolButton_PopupDelay` 决定，不应硬编码时间。

适合“后退 + 历史记录”：

```text
短按：回到上一页
长按：选择更早的历史页
```

### 6.2 `MenuButtonPopup`

分裂按钮：主区域触发默认 action，右侧小箭头区域只弹出菜单。

```cpp
sizeButton->setPopupMode(QToolButton::MenuButtonPopup);
```

style 将它作为复杂控件 `CC_ToolButton`，主区为 `SC_ToolButton`，菜单箭头区为 `SC_ToolButtonMenu`。不要自行假定箭头区宽度；不同 style 使用不同的 `PM_MenuButtonIndicator`。

### 6.3 `InstantPopup`

每次按下都立即弹出菜单，按钮自身 action 不触发：

```cpp
sizeButton->setPopupMode(QToolButton::InstantPopup);
```

适合按钮只承担“打开选项列表”的情况。`showMenu()` 也可以显式弹出关联菜单；没有 menu 时它什么也不做，并且会一直运行到用户关闭菜单。

## 7. 绘制和 QStyleOptionToolButton

`QToolButton` 是复杂控件，style 的主要入口是：

```cpp
QStyle::drawComplexControl(QStyle::CC_ToolButton, ...)
```

对应 option 是 `QStyleOptionToolButton`。在子类中要读取真实绘制状态，使用受保护函数：

```cpp
class InspectableToolButton final : public QToolButton
{
public:
    using QToolButton::QToolButton;

    void dumpOption() const
    {
        QStyleOptionToolButton option;
        initStyleOption(&option);
        qDebug() << option.rect << option.features << option.toolButtonStyle;
    }
};
```

`initStyleOption()` 会填充 action、菜单、箭头、按下、悬停、可选中等完整状态。普通业务代码不需要手工构造它；定制外观应优先用 `QProxyStyle`，不要在 `paintEvent()` 中复刻所有 style 状态。

## 8. 生命周期、所有权和信号

- `QToolButton` 是 `QWidget`，只能在 GUI 线程创建和访问；
- `setDefaultAction()` 不转移 action 所有权；
- `setMenu()` 不转移 menu 所有权；
- `defaultAction()` 与 `menu()` 返回非拥有指针，未设置时为 `nullptr`；
- `triggered(QAction *)` 在关联 action 触发时发出；同一个 action 也可能由菜单、快捷键或其他按钮触发；
- 按钮自身的 `clicked(bool)`、`toggled(bool)` 继承自 `QAbstractButton`，适合观察按钮交互和可选中状态。

若 action/menu 的生命周期短于按钮，应在销毁前清理关联关系或确保 Qt 的 QObject 父子关系能安全销毁它们。

## 9. 常见误区

### 9.1 手工复制 action 的 text、icon、enabled

使用 `setDefaultAction()`。手工复制会在 action 状态变化后失去同步。

### 9.2 以为 InstantPopup 也会触发默认 action

不会。`InstantPopup` 的按下只打开菜单。

### 9.3 以为 setMenu 会接管 menu

不会。menu 所有权仍由调用方安排。

### 9.4 用固定像素判断分裂按钮箭头区

箭头区由 style 计算。需要自定义命中/绘制时使用 `QStyleOptionToolButton` 和 `subControlRect()`。

### 9.5 期望 QToolBar 自动管理手工 addWidget 的按钮风格

工具栏会自动管理 `addAction()` 产生的按钮；手工 `addWidget(new QToolButton)` 的样式、图标尺寸需要你自己配置。

## API 速查表
### 10.1 公开 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QToolButton(QWidget *parent = nullptr)` | 创建空工具按钮 | 建议设置 parent 或放入布局 |
| 生命周期 | `~QToolButton()` | 销毁按钮 | 不拥有 default action 和 menu |
| 枚举 | `ToolButtonPopupMode` | 菜单弹出策略枚举 | 只有关联 menu 时有意义 |
| 枚举值 | `DelayedPopup` | 短按 action，长按弹出菜单 | 延迟由 `SH_ToolButton_PopupDelay` 决定 |
| 枚举值 | `MenuButtonPopup` | 主按钮 action + 箭头菜单的分裂按钮 | 箭头区域由 style 计算 |
| 枚举值 | `InstantPopup` | 按下立即弹出菜单 | 自身 action 不触发 |
| 动作 | `setDefaultAction(QAction *)` | 关联默认 action，并同步其主要显示和状态属性 | 不转移 action 所有权 |
| 动作 | `defaultAction()` | 获取默认 action | 未设置时返回 `nullptr` |
| 菜单 | `setMenu(QMenu *)` | 关联弹出菜单 | 不转移 menu 所有权 |
| 菜单 | `menu()` | 获取关联菜单 | 未设置时返回 `nullptr` |
| 菜单模式 | `setPopupMode(mode)` / `popupMode()` | 设置或获取菜单弹出方式 | 默认 `DelayedPopup` |
| 菜单 | `showMenu()` | 立即弹出关联菜单 | 无菜单时无操作；调用会阻塞到菜单关闭 |
| 外观 | `setAutoRaise(bool)` / `autoRaise()` | 设置或查询悬停时才凸起的视觉效果 | 独立按钮默认 false，工具栏内通常自动启用 |
| 外观 | `setArrowType(Qt::ArrowType)` / `arrowType()` | 设置或获取标准箭头图标 | 默认 `Qt::NoArrow` |
| 外观 | `setToolButtonStyle(Qt::ToolButtonStyle)` / `toolButtonStyle()` | 设置或获取图标与文字布局 | 默认 `ToolButtonIconOnly` |
| 尺寸 | `sizeHint()` | 给布局的理想尺寸 | 由 style、图标、文字和菜单箭头共同决定 |
| 尺寸 | `minimumSizeHint()` | 给布局的最小建议尺寸 | 不要用固定大小替代 |
| 信号 | `triggered(QAction *)` | 关联 action 被触发时发出 | action 可能来自其他入口 |

### 10.2 继承与受保护扩展点

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 选择 | `setCheckable()` / `setChecked()` | 来自 `QAbstractButton` 的可选中状态 API | 工具选择应配合 `QButtonGroup` 互斥管理 |
| 信号 | `clicked(bool)` / `toggled(bool)` | 来自 `QAbstractButton` 的交互信号 | 适合按钮状态逻辑，不等于 action 的全局触发 |
| 内容 | `setIcon()` / `setText()` | 直接设置按钮内容 | 有默认 action 时优先更新 action |
| 样式 | `initStyleOption(QStyleOptionToolButton *)` | 用当前按钮状态填充 style option | `protected`；子类/自定义 style 的正确入口 |
| 绘制 | `paintEvent(QPaintEvent *)` | 绘制按钮 | 外观定制优先 style，不要重绘全部控件 |
| 命中 | `hitButton(const QPoint &)` | 判断点击位置是否命中 | 分裂按钮命中逻辑不应硬编码 |
| 鼠标 | `mousePressEvent()` / `mouseReleaseEvent()` | 处理点击和 popup 交互 | 重写时要保留基类菜单行为 |
| 定时 | `timerEvent()` | 处理长按菜单的内部计时 | 不应被业务代码当成 popup 延迟机制 |
| 动作事件 | `actionEvent()` | 响应关联 action 的增删或变化 | action 同步由 Qt 管理 |
| 状态变化 | `changeEvent()` / `enterEvent()` / `leaveEvent()` / `event()` | 风格、悬停和通用事件入口 | 仅高级子类定制时重写 |
| 选择状态 | `checkStateSet()` / `nextCheckState()` | 可选中状态变化钩子 | 改写后要保持 `QAbstractButton` 契约 |

---

### 一句话总结

`QToolButton` 是紧凑的命令入口：用 `setDefaultAction()` 共享命令状态，用 `popupMode` 选择短按、分裂或立即菜单行为；在工具栏中通常由 Qt 自动创建和同步，手工嵌入时则由你负责样式和生命周期。
