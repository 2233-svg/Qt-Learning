# QToolButton

> Qt 6.11.1 · Qt Widgets · 来自 `QToolButton`

## 1. 先建立直觉

### 这是什么

`QToolButton` 是为工具栏、面板角落和紧凑命令区准备的按钮。它继承 `QAbstractButton`，但比 `QPushButton` 更轻：默认偏向图标显示，可以绑定 `QAction`，可以显示箭头，可以挂菜单，并支持多种菜单弹出模式。

如果 `QPushButton` 表达“清晰的大命令”，`QToolButton` 表达“工具入口”。它常出现在 `QToolBar`、属性面板标题、编辑器小工具条、搜索框右侧按钮里。

### 适合使用的场景

- 工具栏按钮，与 `QAction` 共享图标、文本、快捷键和启用状态。
- 图标按钮或图标加文字的小型命令。
- 需要下拉菜单的工具按钮，例如返回历史、选择画笔、导出格式。
- 需要箭头按钮，例如折叠/展开、上下移动、导航。
- 可选中的工具模式，例如选择工具、画笔工具、橡皮擦工具。

### 不适合的场景

- 对话框主要动作通常用 `QPushButton`，更符合平台习惯。
- 表达布尔设置用 `QCheckBox` 更明确，除非它处在工具栏语境中。
- 表达值选择用 `QComboBox`；工具按钮菜单更偏“动作集合”，不是普通字段输入。

### 最小示例

```cpp
auto *action = new QAction(QIcon(":/icons/zoom-in.svg"), tr("Zoom In"), this);
action->setShortcut(QKeySequence::ZoomIn);

auto *button = new QToolButton(this);
button->setDefaultAction(action);
button->setToolButtonStyle(Qt::ToolButtonIconOnly);
```

绑定 `QAction` 后，按钮会跟随 action 的文本、图标、tooltip、enabled、checked 等状态，适合一处定义、多处呈现。

## 2. 依赖与对象关系

- 头文件：`#include <QToolButton>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QAbstractButton`
- 直接派生类：类页未列出

### 和 QAction 的关系

`QToolButton` 可以有一个 `defaultAction()`。这是工具按钮最重要的协作方式：同一个 `QAction` 可以同时出现在菜单、工具栏、快捷键系统和工具按钮中，状态同步由 Qt 处理。

### 和菜单的关系

工具按钮可以绑定 `QMenu`，并通过 `ToolButtonPopupMode` 决定点击按钮本体和菜单箭头时发生什么。菜单所有权不会自动转移给按钮，应给菜单合适 parent 或外部持有。

### 和 QToolBar 的关系

在 `QToolBar` 中添加 action 时，Qt 通常会为 action 创建工具按钮。主窗口的工具按钮样式变化，也能影响工具按钮文字/图标显示方式。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum ToolButtonPopupMode` | 控制工具按钮菜单如何弹出。 |
| `arrowType : Qt::ArrowType` | 用方向箭头替代普通图标显示。 |
| `autoRaise : bool` | 鼠标悬停时才凸显边框的工具按钮视觉。 |
| `popupMode : ToolButtonPopupMode` | 当前菜单弹出模式。 |
| `toolButtonStyle : Qt::ToolButtonStyle` | 图标/文字显示策略。 |
| `QToolButton(QWidget *parent)` | 创建工具按钮。 |
| `~QToolButton()` | 销毁工具按钮。 |
| `defaultAction() const` / `setDefaultAction(QAction *action)` | 读取或绑定默认 action。 |
| `menu() const` / `setMenu(QMenu *menu)` | 读取或绑定弹出菜单。 |
| `showMenu()` | 主动弹出菜单。 |
| `setArrowType(Qt::ArrowType)` / `arrowType() const` | 设置或读取箭头类型。 |
| `setAutoRaise(bool)` / `autoRaise() const` | 设置或读取自动凸显外观。 |
| `setPopupMode(ToolButtonPopupMode)` / `popupMode() const` | 设置或读取菜单弹出方式。 |
| `setToolButtonStyle(Qt::ToolButtonStyle)` / `toolButtonStyle() const` | 设置或读取图标文字显示方式。 |
| `triggered(QAction *action)` | 菜单或默认 action 被触发时发出。 |
| `sizeHint() const` / `minimumSizeHint() const` | 返回工具按钮推荐尺寸。 |
| `initStyleOption(QStyleOptionToolButton *option) const` | 为自定义绘制准备 style option。 |
| `actionEvent(QActionEvent *event)` | 处理 action 添加、移除、变化。 |
| `checkStateSet()` / `nextCheckState()` | 和 action/checkable 状态同步有关的按钮钩子。 |
| `enterEvent()` / `leaveEvent()` | 支持 auto raise、hover 反馈。 |
| `mousePressEvent()` / `mouseReleaseEvent()` | 处理按钮本体和菜单区域点击。 |
| `paintEvent()` / `timerEvent()` / `event()` / `changeEvent()` / `hitButton()` | 事件、绘制和弹出延迟等底层实现。 |

## 4. API 逐项说明

### `enum QToolButton::ToolButtonPopupMode`

菜单按钮最容易混淆的就是这个枚举。

- `DelayedPopup`：点击按钮先触发默认动作；按住一段时间才弹出菜单，适合“返回”按钮加历史菜单。
- `MenuButtonPopup`：按钮分成主动作区域和小箭头区域；点主区域触发动作，点箭头弹菜单。
- `InstantPopup`：点击立即弹菜单，不触发按钮本体动作，适合纯下拉工具入口。

选择模式时要看用户预期：如果按钮图标代表一个明确动作，用 `DelayedPopup` 或 `MenuButtonPopup`；如果它只是菜单入口，用 `InstantPopup`。

### `arrowType : Qt::ArrowType`

设置后按钮显示方向箭头而非普通图标。常见用途是展开/折叠、上下移动、左右导航。

如果同时设置 icon 和 arrow type，要以实际 style 表现为准。语义上箭头按钮应保持简单，不要承载复杂命令。

### `autoRaise : bool`

开启后，按钮通常在鼠标悬停时才显示凸起边框。这是工具栏和轻量面板里常见的视觉风格。

macOS 的某些 style 可能忽略该属性。跨平台界面不要把 auto raise 当作唯一的状态提示。

### `popupMode : ToolButtonPopupMode`

控制菜单如何弹出。默认是 `DelayedPopup`。

设置了菜单但用户找不到入口时，通常是 popup mode 与视觉设计不匹配。需要明确菜单存在时，`MenuButtonPopup` 的箭头提示更强。

### `toolButtonStyle : Qt::ToolButtonStyle`

决定只显示图标、只显示文字、文字在图标旁边、文字在图标下方，或跟随系统样式。默认通常是 `Qt::ToolButtonIconOnly`。

工具栏上建议遵循主窗口或系统设置；属性面板里的小工具按钮则常用 icon only，并配 tooltip。

### `QToolButton(QWidget *parent = nullptr)` / `~QToolButton()`

创建和销毁工具按钮。创建后通常绑定 action、设置 icon/text、或挂菜单。

没有 action 的工具按钮也能用，但在菜单栏、工具栏和快捷键共享命令时，`QAction` 是更好的中心。

### `defaultAction() const` / `setDefaultAction(QAction *action)`

默认 action 会向按钮同步多项属性：checkable、checked、enabled、font、icon、text、tooltip、status tip、whatsThis；如果 action 有菜单，也会参与菜单相关行为。

不是所有按钮属性都来自 action，例如 `autoRepeat` 不会被 action 控制。把命令语义放进 action，把按钮呈现细节留在按钮上，是最清晰的分工。

### `menu() const` / `setMenu(QMenu *menu)`

设置或读取关联菜单。菜单显示方式取决于 `popupMode`。

菜单所有权不会转移给工具按钮。通常把菜单 parent 设为按钮或窗口，避免悬空指针。

### `showMenu()`

主动弹出关联菜单。没有菜单时不做事；菜单关闭后函数才返回。

适合把快捷键、长按或外部控件连接到同一个菜单入口。

### `setArrowType()` / `arrowType()`

设置或读取箭头类型。箭头类型来自 `Qt::ArrowType`，例如 `UpArrow`、`DownArrow`、`LeftArrow`、`RightArrow`。

箭头按钮如果还有菜单，要保证用户能区分“箭头代表方向动作”还是“箭头代表下拉”。

### `setAutoRaise()` / `autoRaise()`

设置或读取自动凸显。开启后，按钮静止时更轻，hover 或按下时更像按钮。

它适合密集工具区，不适合主要操作按钮。主要按钮需要持续可见的边界和强调。

### `setPopupMode()` / `popupMode()`

设置或读取菜单弹出策略。更改后会影响 mouse press/release 和 timer 行为。

如果使用 `InstantPopup`，按钮的 `clicked()` 语义通常不再代表主动作，业务逻辑应连接菜单 action 的 `triggered()`。

### `setToolButtonStyle()` / `toolButtonStyle()`

设置或读取图标文字组合方式。在 `QMainWindow` 工具栏中，工具按钮可能自动跟随主窗口的工具按钮样式设置。

图标-only 按钮要配 tooltip；文字-only 工具按钮要确保文案足够短。

### `triggered(QAction *action)`

当工具按钮关联的 action 被触发时发出，参数指出触发了哪个 action。带菜单的工具按钮尤其有用，可以统一处理菜单里触发的动作。

如果你已经连接了各个 `QAction::triggered()`，这个信号可选；它更适合从按钮角度集中观察触发。

### `sizeHint()` / `minimumSizeHint()`

返回考虑 icon、text、toolButtonStyle、菜单箭头和 style 后的尺寸。

工具栏尺寸问题通常来自图标尺寸、文字显示策略、主窗口 toolbar style，而不只是按钮自己的 size hint。

### `initStyleOption(QStyleOptionToolButton *option) const`

填充工具按钮绘制所需状态，包括 arrow、popup mode、tool button style、菜单指示、checked、hover 等。

自定义绘制时使用它，比手动组装状态可靠得多。

### `actionEvent(QActionEvent *event)`

处理 action 添加、移除和变化。`setDefaultAction()` 后，action 的 enabled、checked、icon、text 等变化会通过这一套机制反映到按钮上。

普通业务代码不需要重写，除非你在做特殊 action 容器。

### `checkStateSet()` / `nextCheckState()`

处理 checkable 状态变化，并和默认 action 的 checked 状态协同。可选中的工具按钮常用于工具模式，例如“选择”“画笔”“吸管”。

多个工具模式互斥时，应把 action 放进 `QActionGroup`，而不是手动互相取消按钮。

### `enterEvent()` / `leaveEvent()`

鼠标进入和离开事件，常用于 hover、auto raise 和样式更新。

自定义子类重写时要保留基类处理，否则悬停视觉可能不同步。

### `mousePressEvent()` / `mouseReleaseEvent()`

处理按钮本体点击、菜单区域点击、按住弹出菜单等行为。popup mode 的差异主要体现在这里。

重写这些函数容易破坏菜单按钮的细节，优先用 action、menu 和 popup mode 配置表达需求。

### `paintEvent()` / `timerEvent()` / `event()` / `changeEvent()` / `hitButton()`

绘制、延迟弹出、通用事件、状态变化和命中测试的底层实现。`DelayedPopup` 依赖计时器；auto raise 和 style 变化也会触发更新。

自定义外观时，保持 `QStyleOptionToolButton` 和平台 style 是最稳妥的路径。

## 5. 深入实践与常见坑

### QAction 是工具按钮的中心

同一个命令如果会出现在菜单、工具栏、快捷键和上下文菜单中，先建 `QAction`，再让 `QToolButton` 呈现它。这样 enabled、checked、text、icon 不会到处复制。

### 弹出模式要匹配心智

`InstantPopup` 是“这里有菜单”；`MenuButtonPopup` 是“有主动作，也有更多选项”；`DelayedPopup` 是“主动作最重要，长按给历史或变体”。选错模式会让用户误触。

### 图标按钮必须有文字替代

icon-only 工具按钮至少要有 tooltip，最好 action text 也清楚。否则无障碍、键盘用户和新用户都会吃力。

### 可选中工具模式用 QActionGroup

画笔、橡皮擦、选择工具这类互斥模式，不要靠多个按钮互相 `setChecked(false)`；用 `QActionGroup` 或 `QButtonGroup` 表达互斥关系。
