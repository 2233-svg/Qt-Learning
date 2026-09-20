# QPushButton

> Qt 6.11.1 · Qt Widgets · 来自 `QPushButton`

## 1. 先建立直觉

### 这是什么

`QPushButton` 是 Qt Widgets 中最标准的“执行命令”按钮。用户点击、按 Space、触发标签快捷键，或在对话框中按 Enter 命中默认按钮时，它会通过继承自 `QAbstractButton` 的信号发出操作意图。

它的核心不是保存状态，而是把一个明确动作暴露给用户：保存、打开、应用、确定、取消、浏览、重试。按钮可以带文本、图标、弹出菜单，也可以在对话框里扮演默认按钮。

### 适合使用的场景

- 离散命令：保存、删除、连接、刷新、浏览文件。
- 对话框动作：确定、取消、应用、帮助。
- 带下拉菜单的命令入口，例如“新建”按钮附带多种新建类型。
- 需要平台原生按钮外观、键盘焦点和默认按钮行为的 Widgets 界面。

### 不适合的场景

- 二态/三态选择用 `QCheckBox` 或 `QRadioButton` 更自然。
- 工具栏里的小图标按钮通常用 `QToolButton`。
- 列表项中的自定义交互不一定要放真实按钮，委托绘制或 action 可能更轻。
- 长任务不要直接在 `clicked()` 槽里阻塞执行，应禁用按钮并把任务交给异步流程。

### 最小示例

```cpp
auto *saveButton = new QPushButton(QIcon(":/icons/save.svg"), tr("&Save"), this);
connect(saveButton, &QPushButton::clicked, this, [this] {
    saveDocument();
});
```

按钮文本中的 `&` 会创建键盘助记符。真正的业务逻辑放在槽里；按钮只负责表达“用户请求保存”。

## 2. 依赖与对象关系

- 头文件：`#include <QPushButton>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QAbstractButton`
- 直接派生类：`QCommandLinkButton`

`QPushButton` 继承了按钮通用能力：`text`、`icon`、`checked`、`checkable`、`clicked()`、`pressed()`、`released()`、`toggled()` 等。本文只说明 `QPushButton` 自己新增或重写的部分；按钮通用状态应参考 `QAbstractButton`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `autoDefault : bool` | 对话框中获得焦点时是否自动成为 Enter 默认按钮候选。 |
| `default : bool` | 是否为对话框当前默认按钮，用户按 Enter 时触发。 |
| `flat : bool` | 是否绘制为扁平按钮，常用于工具区或轻量命令。 |
| `QPushButton(QWidget *parent)` | 创建空文本按钮。 |
| `QPushButton(const QString &text, QWidget *parent)` | 创建文本按钮。 |
| `QPushButton(const QIcon &icon, const QString &text, QWidget *parent)` | 创建带图标和文本的按钮。 |
| `~QPushButton()` | 销毁按钮。 |
| `autoDefault() const` / `setAutoDefault(bool)` | 读取或设置自动默认按钮行为。 |
| `isDefault() const` / `setDefault(bool)` | 读取或设置默认按钮状态。 |
| `isFlat() const` / `setFlat(bool)` | 读取或设置扁平外观。 |
| `menu() const` / `setMenu(QMenu *menu)` | 读取或绑定弹出菜单，把按钮变成菜单按钮。 |
| `showMenu()` | 主动弹出已绑定菜单。 |
| `sizeHint() const` / `minimumSizeHint() const` | 返回按钮推荐尺寸和最小推荐尺寸。 |
| `initStyleOption(QStyleOptionButton *option) const` | 给自定义绘制准备完整 style option。 |
| `hitButton(const QPoint &pos) const` | 判断某点是否落在可点击区域。 |
| `event(QEvent *e)` | 处理通用事件入口。 |
| `focusInEvent(QFocusEvent *e)` / `focusOutEvent(QFocusEvent *e)` | 焦点变化，影响自动默认按钮显示和行为。 |
| `keyPressEvent(QKeyEvent *e)` | 键盘触发按钮行为。 |
| `mouseMoveEvent(QMouseEvent *e)` | 鼠标移动过程中的按钮状态处理。 |
| `paintEvent(QPaintEvent *)` | 使用当前 style 绘制按钮。 |

## 4. API 逐项说明

### `autoDefault : bool`

自动默认按钮主要发生在 `QDialog` 中。按钮获得焦点时，可以临时成为 Enter 键触发的按钮。Qt 会根据平台 style 给这种按钮预留额外边框空间，所以开启后 `sizeHint()` 可能稍大。

对话框里的按钮默认通常启用 `autoDefault`，普通窗口里的按钮默认通常不启用。如果你的按钮行尺寸出现几像素跳动，检查 `autoDefault` 是一个很实用的方向。

### `default : bool`

默认按钮是对话框中按 Enter 会触发的按钮。一个对话框通常只有一个当前默认按钮，常见是“确定”或“保存”。

不要把危险操作设成默认按钮，尤其是删除、覆盖、发送这类不可逆动作。默认按钮应服务最安全、最常见、最符合用户预期的路径。

### `flat : bool`

扁平按钮通常不绘制凸起边框，适合工具区、窄面板、辅助命令。它仍然是按钮，仍会接收点击和键盘操作。

扁平不是禁用。禁用应使用 `setEnabled(false)`；扁平只是视觉弱化。

### `QPushButton(QWidget *parent = nullptr)`

创建没有文本和图标的按钮。通常随后调用继承自 `QAbstractButton` 的 `setText()`、`setIcon()` 配置。

空按钮不利于可访问性，若只显示图标，应至少设置 tooltip、accessible name，或用更适合图标命令的 `QToolButton`。

### `QPushButton(const QString &text, QWidget *parent = nullptr)`

创建文本按钮。文本可以包含 `&` 助记符，例如 `tr("&Open")`。

按钮文案应使用动词或明确命令，不要让用户猜“OK”到底会保存、上传还是删除。

### `QPushButton(const QIcon &icon, const QString &text, QWidget *parent = nullptr)`

创建带图标和文本的按钮。图标应强化命令含义，而不是替代文本含义；跨平台桌面应用里，文本仍然是理解命令的主渠道。

图标尺寸由 style 和按钮属性共同决定，通常不要为单个按钮硬编码 pixmap。

### `~QPushButton()`

销毁按钮对象。按钮如果在布局和父控件下，通常由父控件负责销毁。

按钮被销毁会自动断开 QObject 信号连接，但业务任务不会因为按钮销毁自动取消；长任务要有自己的取消和生命周期管理。

### `autoDefault()` / `setAutoDefault(bool)`

读取或设置自动默认行为。若按钮在对话框中只是辅助动作，例如“浏览...”“高级...”，通常可以关闭 `autoDefault`，避免用户按 Enter 时触发意外动作。

在按钮很多的对话框里，明确设置默认按钮和辅助按钮的 auto default 状态，能让键盘行为更可预测。

### `isDefault()` / `setDefault(bool)`

读取或设置当前默认按钮。常见写法是在确定按钮上调用 `setDefault(true)`。

如果表单校验失败，不一定要取消默认按钮；更常见做法是保持默认按钮，但点击后显示错误并不关闭对话框。若操作当前不可用，应禁用按钮。

### `isFlat()` / `setFlat(bool)`

读取或设置扁平外观。适用于视觉层级较低的命令，例如搜索框旁的清除按钮、标题栏内部的小命令。

扁平按钮在某些 style 下按下反馈较弱，因此主要动作不建议设置为 flat。

### `menu()` / `setMenu(QMenu *menu)`

绑定菜单后，按钮成为菜单按钮，通常会显示下拉指示。菜单所有权不会自动转移给按钮，所以建议给菜单设置合适 parent，或由外部对象持有。

菜单按钮适合“一个主入口，多种变体”的动作，例如“导出”下有 PDF、图片、CSV。若每个选项都同等重要，可以直接放多个按钮或使用菜单栏。

### `showMenu()`

主动弹出已绑定菜单。没有菜单时不做事。它会等菜单关闭后返回，因此不要在 GUI 线程里把它和长阻塞逻辑混在一起。

常见用途是把某个键盘快捷键或辅助按钮连接到主按钮菜单。

### `sizeHint()` / `minimumSizeHint()`

返回推荐尺寸和最小推荐尺寸。文本、图标、字体、style、default/autoDefault 边框都会影响结果。

布局中按钮大小异常时，先检查文本是否过长、是否开启默认按钮边框、是否有全局 style sheet 改了 padding。

### `initStyleOption(QStyleOptionButton *option) const`

给 `QStyleOptionButton` 填入当前按钮状态，供自定义绘制或子类扩展使用。使用它可以保持和平台 style 一致，不必手动拼所有状态位。

自定义按钮外观时，优先用 style option 加 `QStyle::drawControl()`；完全手绘按钮很容易丢失焦点框、默认按钮、高 DPI 和禁用状态细节。

### `hitButton(const QPoint &pos) const`

判断坐标是否在按钮可点击区域。默认按钮通常整个矩形都可点。

子类可以重写它实现非矩形点击区域，但这会影响可用性。视觉上可点击的区域和实际命中区域应保持一致。

### `event()` / `focusInEvent()` / `focusOutEvent()`

这些重写函数处理通用事件和焦点变化。焦点变化会影响自动默认按钮状态，也会影响 style 绘制出的焦点框。

如果子类重写这些函数，未处理事件应交回基类，否则默认按钮、快捷键、可访问性状态可能出现细小但难查的问题。

### `keyPressEvent(QKeyEvent *e)`

处理键盘触发。按钮获得焦点时，Space 通常触发按钮；在对话框中，Enter 可能触发默认按钮。

不要在子类里随意吞掉 Space/Enter，除非你明确要改变按钮的键盘语义。

### `mouseMoveEvent(QMouseEvent *e)`

处理鼠标移动导致的 hover、pressed 状态变化。普通应用代码很少重写。

需要拖拽行为时要非常小心：按钮的“按下、移出、释放”状态机是用户熟悉的反馈，破坏它会让点击手感怪异。

### `paintEvent(QPaintEvent *)`

绘制按钮。默认实现通过当前平台 style 绘制文本、图标、边框、焦点框、默认按钮边框和菜单指示。

自定义绘制时，尽量保留 `QStyleOptionButton` 和 `QStyle`，这样能继续尊重主题、高 DPI、禁用状态和系统视觉。

## 5. 深入实践与常见坑

### `clicked()` 才是最常用信号

`pressed()` 表示按下瞬间，`released()` 表示释放，`clicked()` 表示完成一次点击语义。业务命令通常连 `clicked()`，避免用户按下后移出按钮再释放仍触发动作。

### 默认按钮要谨慎

Enter 触发默认按钮非常高效，也非常危险。确认类按钮适合默认；破坏性按钮应降低默认触发概率，必要时要求显式点击。

### 菜单按钮不是组合框

按钮菜单表达“执行某个命令变体”；`QComboBox` 表达“选择一个值”。不要因为都能下拉就混用。

### 长任务要反馈状态

点击后立即禁用按钮、显示忙碌状态或进度，并在任务结束后恢复。否则用户可能重复点击，制造重复请求。
