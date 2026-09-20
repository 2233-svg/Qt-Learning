# QAbstractButton

> Qt 6.11.1 · Qt Widgets · 来自 `QAbstractButton`

## 1. 先建立直觉

### 这是什么

`QAbstractButton` 是所有 Widgets 按钮的共同基类。`QPushButton`、`QCheckBox`、`QRadioButton`、`QToolButton` 的文本、图标、快捷键、按下状态、选中状态、自动重复、点击信号，大多都来自这里。

它是“按钮状态机”的核心：鼠标按下产生 `pressed()`，有效释放产生 `released()` 和 `clicked()`，可选中按钮还会改变 `checked` 并发出 `toggled()`。具体子类负责长相和细节语义，基类负责统一交互协议。

### 适合使用的场景

- 阅读和理解所有按钮子类的共同行为。
- 自定义一种新的按钮控件，并复用 Qt 的键盘、鼠标、快捷键和 checked 状态机制。
- 需要统一处理按钮组、排他选择、自动重复点击等行为。
- 需要区分 `pressed`、`released`、`clicked`、`toggled` 的触发时机。

### 不适合的场景

- 业务代码一般不直接实例化它；它含有纯虚 `paintEvent()`，应使用具体子类。
- 如果只是执行命令，用 `QPushButton`；如果只是布尔选项，用 `QCheckBox`；如果是互斥选项，用 `QRadioButton`。
- 不要把按钮 checked 状态当复杂业务模型；按钮只是 UI 状态入口，持久数据应放在模型或配置对象中。

### 最小示例

```cpp
auto *button = new QPushButton(tr("&Refresh"), this);
button->setAutoRepeat(true);
button->setAutoRepeatDelay(400);
button->setAutoRepeatInterval(80);

connect(button, &QAbstractButton::clicked, this, &Window::refreshPreview);
```

虽然对象是 `QPushButton`，但自动重复和 `clicked()` 语义来自 `QAbstractButton`。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractButton>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QWidget`
- 直接派生类：`QCheckBox`、`QPushButton`、`QRadioButton`、`QToolButton`

### 状态机

按钮至少有两个层次的状态：瞬时状态 `down`，表示当前是否处于按下视觉/交互状态；持久状态 `checked`，表示可选中按钮是否被选中。普通按钮通常只关心点击，复选框和单选按钮会长期保存 checked。

### 排他关系

`autoExclusive` 和 `QButtonGroup` 都能表达互斥选择。`autoExclusive` 只在同一父控件下的可选中按钮之间自动生效，典型是 radio button；`QButtonGroup` 更明确，能跨父控件组织按钮，也能绑定 id。

### 绘制责任

`QAbstractButton` 有纯虚 `paintEvent()`，所以它不定义具体外观。子类必须绘制自己，通常通过 `QStyleOptionButton` 和当前 style 保持平台一致。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `autoExclusive : bool` | 同父控件下可选中按钮是否自动互斥。 |
| `autoRepeat : bool` | 按住按钮时是否重复发出点击序列。 |
| `autoRepeatDelay : int` | 自动重复开始前的毫秒延迟。 |
| `autoRepeatInterval : int` | 自动重复触发间隔，单位毫秒。 |
| `checkable : bool` | 按钮是否拥有可切换的 checked 状态。 |
| `checked : bool` | 可选中按钮当前是否选中。 |
| `down : bool` | 按钮当前是否处于按下状态。 |
| `icon : QIcon` | 按钮显示的图标。 |
| `iconSize : QSize` | 图标最大显示尺寸。 |
| `shortcut : QKeySequence` | 触发按钮的快捷键。 |
| `text : QString` | 按钮文本，也可通过 `&` 生成助记符。 |
| `QAbstractButton(QWidget *parent)` | 构造抽象按钮基类部分。 |
| `~QAbstractButton()` | 销毁按钮对象。 |
| `group() const` | 返回按钮所属的 `QButtonGroup`。 |
| `click()` | 程序化执行一次点击语义。 |
| `animateClick()` | 程序化执行一次带按下动画的点击。 |
| `toggle()` | 切换 checked 状态。 |
| `setChecked(bool)` | 设置 checked 状态。 |
| `setIconSize(const QSize &size)` | 设置图标最大显示尺寸。 |
| `clicked(bool checked)` | 完成一次有效点击时发出。 |
| `pressed()` | 按钮进入按下状态时发出。 |
| `released()` | 按钮从按下状态释放时发出。 |
| `toggled(bool checked)` | checked 状态变化时发出。 |
| `checkStateSet()` | 子类钩子：`setChecked()` 后调整内部状态。 |
| `nextCheckState()` | 子类钩子：定义下一次点击如何改变 checked。 |
| `hitButton(const QPoint &pos) const` | 判断坐标是否在可点击区域。 |
| `paintEvent(QPaintEvent *e)` | 纯虚绘制入口，具体子类必须实现。 |
| `changeEvent()` / `event()` | 处理通用状态和事件变化。 |
| `focusInEvent()` / `focusOutEvent()` | 处理键盘焦点变化。 |
| `keyPressEvent()` / `keyReleaseEvent()` | 处理键盘触发按钮。 |
| `mousePressEvent()` / `mouseReleaseEvent()` / `mouseMoveEvent()` | 处理鼠标按下、释放和拖出拖回。 |
| `timerEvent()` | 支撑自动重复点击计时。 |

## 4. API 逐项说明

### `autoExclusive : bool`

开启后，同一个父控件下的可选中按钮表现为互斥组：选中一个会取消另一个。`QRadioButton` 默认启用，普通按钮默认不启用。

如果按钮已经放进 `QButtonGroup`，应优先按 group 的规则理解互斥关系。复杂界面中，显式 `QButtonGroup` 比依赖同父对象更可维护。

### `autoRepeat : bool` / `autoRepeatDelay : int` / `autoRepeatInterval : int`

自动重复让用户按住按钮时持续触发 `pressed()`、`released()`、`clicked()` 序列。延迟控制第一次重复前等多久，间隔控制后续触发频率。

它适合微调数值、连续移动、按住滚动这类操作。不适合保存、删除、提交订单等不可重复命令。

### `checkable : bool`

决定按钮是否可以保存 checked 状态。`QCheckBox`、`QRadioButton` 天然是可选中按钮；`QPushButton` 也可以设为 checkable，变成类似开关的按钮。

如果按钮表达的是“执行一次动作”，不要设置 checkable。否则用户会误以为动作有持续开关状态。

### `checked : bool`

表示可选中按钮当前是否选中。只有 `checkable` 为真时这个状态才有用户意义。

程序化调用 `setChecked()` 会改变状态并触发 `toggled()`，但不会触发 `clicked()`。这能区分“用户点击”与“代码同步状态”。

### `down : bool`

表示按钮正处于按下状态。它通常由鼠标、键盘或 `animateClick()` 自动管理。

手动 `setDown(true)` 只改变按下状态，不会发出 `pressed()` 或 `clicked()`。除非你在实现特殊控件，不要用它模拟用户点击。

### `icon : QIcon` / `iconSize : QSize`

按钮可以同时显示图标和文本。`iconSize` 是最大显示尺寸，小图标不会被强行放大。

图标应当服务识别，不应替代文字。只显示图标的按钮要配 tooltip 和 accessible name。

### `shortcut : QKeySequence` / `text : QString`

`shortcut` 是显式快捷键；`text` 中的 `&` 可以创建助记符。例如 `tr("&Open")` 常生成 Alt+O。

要显示字面量 `&`，使用 `&&`。翻译文本时要注意助记符冲突，尤其是一个对话框里多个按钮或字段标签共存时。

### `QAbstractButton(QWidget *parent = nullptr)` / `~QAbstractButton()`

构造和销毁按钮基类部分。由于 `paintEvent()` 是纯虚函数，应用代码不会直接创建 `QAbstractButton`，而是创建具体子类。

父控件负责 QObject 生命周期；信号连接会在对象销毁时自动断开。

### `group() const`

返回按钮所属 `QButtonGroup`，没有则返回 `nullptr`。按钮组能统一管理互斥、id 映射和批量信号。

当按钮不共享同一个父控件，或你需要把按钮映射到枚举/id 时，应使用 `QButtonGroup`。

### `click()`

程序化执行一次点击。如果按钮禁用，不会生效。对 checkable 按钮，点击会按规则切换 checked。

测试或快捷命令可以调用它；同步状态不要调用 `click()`，应调用 `setChecked()` 或业务函数，避免误触发用户点击语义。

### `animateClick()`

和 `click()` 类似，但会短暂显示按下动画，默认约 100 ms 后释放。多次调用会重置释放计时。

它适合让键盘、远程命令或教学引导看起来像真实按下按钮。纯业务触发通常不需要动画。

### `setChecked(bool)` / `toggle()`

`setChecked()` 设置明确状态，`toggle()` 反转状态。二者都面向 checkable 按钮。

互斥按钮里，取消当前选中项可能受 group 或 autoExclusive 规则限制。不要假设每次 `toggle()` 都会得到你想要的最终状态，尤其是 radio button。

### `setIconSize(const QSize &size)`

设置图标最大尺寸。它会影响 size hint 和绘制，但按钮最终大小仍由布局、文本、style 和 size policy 决定。

统一工具区图标尺寸时，优先在一组按钮上使用相同尺寸，不要让每个图标原始像素决定按钮大小。

### `clicked(bool checked)`

有效点击完成时发出：鼠标按下后在按钮内释放、快捷键触发、调用 `click()` 或 `animateClick()` 都可能发出。`checked` 参数反映点击后的 checked 状态。

业务命令最常连接这个信号。注意 `setChecked()`、`setDown()`、`toggle()` 不会发出 `clicked()`，这正是区分用户动作和程序状态变更的关键。

### `pressed()` / `released()`

`pressed()` 在进入按下状态时发出，`released()` 在释放时发出。自动重复开启时，这两个信号会随重复节奏一起出现。

这两个信号适合做按住预览、临时高亮、连续控制；提交类业务应使用 `clicked()`。

### `toggled(bool checked)`

checked 状态变化时发出，不要求一定来自用户点击。程序调用 `setChecked()` 也会触发。

它适合同步 UI 状态，例如勾选按钮控制面板显示隐藏。需要只响应用户动作时，用 `clicked(bool)` 更合适。

### `checkStateSet()`

保护虚函数，在 `setChecked()` 之后调用，除非该设置发生在 `nextCheckState()` 内。子类可用它清理中间状态。

普通应用代码不会调用。自定义三态或特殊按钮时才需要理解它。

### `nextCheckState()`

保护虚函数，定义用户激活按钮后 checked 状态如何前进。默认通常是二态切换。

`QCheckBox` 的三态行为就属于这类扩展思路。自定义多态按钮时，重写它比在 `clicked()` 槽里反复修正状态更干净。

### `hitButton(const QPoint &pos) const`

判断某个坐标是否算作点击按钮。默认通常是按钮矩形。

非矩形按钮、圆形按钮或带特殊热区的按钮可以重写它。命中区域要和视觉一致，否则用户会觉得按钮“点不准”。

### `paintEvent(QPaintEvent *e)`

纯虚绘制入口。具体按钮子类必须实现。标准子类通常通过 style 系统绘制，以获得原生主题、焦点框、禁用状态、高 DPI 支持。

自定义按钮如果完全手绘，要主动考虑文本省略、图标缩放、焦点可见性、无障碍和右到左布局。

### `changeEvent()` / `event()`

处理语言、字体、样式、启用状态等通用事件。按钮文本翻译、图标文字、style sheet 改变都可能走这些入口。

子类重写时未处理事件应交给基类。

### `focusInEvent()` / `focusOutEvent()`

处理焦点进入和离开。焦点决定键盘是否能触发按钮，也影响绘制出的焦点框。

对话框里的默认按钮和自动默认按钮也会受焦点变化影响。

### `keyPressEvent()` / `keyReleaseEvent()`

处理键盘按下和释放。Space、Enter、助记符和快捷键共同构成按钮键盘可达性的一部分。

重写时不要破坏 Space 触发按钮的基本规则，除非你明确在设计一种非标准控件。

### `mousePressEvent()` / `mouseReleaseEvent()` / `mouseMoveEvent()`

处理鼠标状态机：按下、拖出按钮、拖回按钮、释放。只有满足按钮命中规则的释放才形成有效点击。

这也是 `clicked()` 比简单监听 mouse release 更可靠的原因。

### `timerEvent(QTimerEvent *e)`

用于自动重复。开启 auto repeat 时，内部计时器负责延迟和周期触发。

普通子类很少需要重写；若重写，要注意不要干扰基类重复点击逻辑。

## 5. 深入实践与常见坑

### `clicked` 和 `toggled` 不是同义词

`clicked` 是一次用户/程序点击动作，`toggled` 是 checked 状态变化。程序同步状态时可能只有 `toggled`，没有 `clicked`。

### 排他选择优先用 QButtonGroup

`autoExclusive` 依赖同父控件，界面层级稍微复杂就不够显式。`QButtonGroup` 能表达清楚的分组和 id，更适合长期维护。

### 自动重复只给可重复动作

按住按钮连续触发很方便，但只适合“增加一点、继续滚动、连续移动”。提交、保存、删除这类动作不要开启。

### 自定义按钮别忘了可访问性

如果你继承 `QAbstractButton` 手绘外观，仍然要提供清晰文本、焦点反馈、键盘行为和可访问名称。看起来漂亮但键盘不能用的按钮，在桌面应用里就是坏控件。
