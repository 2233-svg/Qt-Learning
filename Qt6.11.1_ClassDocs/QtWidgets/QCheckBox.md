# QCheckBox

> Qt 6.11.1 · Qt Widgets · 来自 `QCheckBox`

## 1. 先建立直觉

### 这是什么

`QCheckBox` 是用于表达“可独立开关的选项”的按钮控件。它继承 `QAbstractButton`，因此拥有文本、快捷键、点击、checked 状态等通用按钮能力；同时它增加了 `Qt::CheckState`，可以表示未选中、部分选中、选中三种状态。

二态复选框表达布尔选项：启用自动保存、记住密码、显示网格。三态复选框表达“混合/部分应用”的状态：树形选择里父节点的部分子项被选中，批量编辑时多个对象当前值不一致。

### 适合使用的场景

- 用户可以独立开启或关闭某个选项。
- 多个选项可以同时成立，不需要互斥。
- 需要表示部分选中或混合状态。
- 设置页、过滤面板、权限勾选、树形选择的节点状态。

### 不适合的场景

- 多个选项只能选一个时，用 `QRadioButton` 或 `QButtonGroup`。
- 执行一次命令时，用 `QPushButton`。
- 工具栏里的紧凑切换按钮，可能用 checkable `QToolButton` 更合适。

### 最小示例

```cpp
auto *checkBox = new QCheckBox(tr("&Enable notifications"), this);
checkBox->setChecked(settings.notificationsEnabled());

connect(checkBox, &QCheckBox::checkStateChanged, this, [this](Qt::CheckState state) {
    settings.setNotificationsEnabled(state == Qt::Checked);
});
```

Qt 6.7 起 `checkStateChanged(Qt::CheckState)` 直接给出三态状态，比只看 `toggled(bool)` 更完整。

## 2. 依赖与对象关系

- 头文件：`#include <QCheckBox>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QAbstractButton`
- 直接派生类：类页未列出

`QCheckBox` 的大多数按钮行为来自 `QAbstractButton`。如果只需要二态，`isChecked()` / `setChecked()` 足够；如果启用三态，应使用 `checkState()` / `setCheckState()`，否则会丢失 `PartiallyChecked`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `tristate : bool` | 是否允许第三种“部分选中”状态。 |
| `QCheckBox(QWidget *parent)` | 创建无文本复选框。 |
| `QCheckBox(const QString &text, QWidget *parent)` | 创建带文本复选框。 |
| `~QCheckBox()` | 销毁复选框。 |
| `checkState() const` | 返回 `Unchecked`、`PartiallyChecked` 或 `Checked`。 |
| `setCheckState(Qt::CheckState state)` | 设置完整三态状态。 |
| `isTristate() const` / `setTristate(bool)` | 读取或启用三态能力。 |
| `checkStateChanged(Qt::CheckState state)` | Qt 6.7 起，状态变化时发出完整 check state。 |
| `sizeHint() const` / `minimumSizeHint() const` | 返回复选框推荐尺寸。 |
| `initStyleOption(QStyleOptionButton *option) const` | 为自定义绘制准备 style option。 |
| `nextCheckState()` | 定义用户点击后状态如何推进。 |
| `checkStateSet()` | 程序设置状态后的子类钩子。 |
| `hitButton(const QPoint &pos) const` | 判断点击坐标是否命中复选框。 |
| `event()` / `mouseMoveEvent()` / `paintEvent()` | 事件处理与绘制实现。 |

## 4. API 逐项说明

### `tristate : bool`

启用后，复选框可以处于 `Qt::PartiallyChecked`。这不是“不确定是否选中”的模糊布尔值，而是一个明确 UI 语义：当前范围内有一部分被选中。

三态适合聚合状态，不适合普通 yes/no 设置。滥用三态会让用户不知道点击后会发生什么。

### `QCheckBox(QWidget *parent = nullptr)` / `QCheckBox(const QString &text, QWidget *parent = nullptr)`

创建复选框。带文本构造函数最常用，文本可使用 `&` 设置助记符。

无文本复选框通常只适合表格列、紧凑列表或旁边已经有清楚说明的场景；否则可访问性和可理解性都较弱。

### `~QCheckBox()`

销毁复选框。通常由父控件负责，不需要手动删除。

状态要保存到设置或模型里，不能依赖控件对象长期存在。

### `checkState() const`

返回完整状态：`Qt::Unchecked`、`Qt::PartiallyChecked`、`Qt::Checked`。

只要启用了三态，就优先用这个函数而不是 `isChecked()`。`isChecked()` 只能表达布尔结果，容易把部分选中处理错。

### `setCheckState(Qt::CheckState state)`

设置完整三态状态。传入 `PartiallyChecked` 时通常应先启用 `setTristate(true)`，让用户和 style 都能正确表达第三态。

用于同步模型到界面时很常见，例如父节点根据子节点选择情况更新自己状态。

### `isTristate() const` / `setTristate(bool y = true)`

读取或设置是否允许三态。启用后，用户点击时状态循环会包含部分选中；具体顺序由 `nextCheckState()` 控制。

如果第三态只是程序显示的中间状态，而不希望用户循环到它，可以通过子类重写 `nextCheckState()` 实现更精确的行为。

### `checkStateChanged(Qt::CheckState state)`

Qt 6.7 起提供，状态变化时发出完整 `Qt::CheckState`。它比 `toggled(bool)` 更适合三态复选框。

二态复选框也可以用它，代码会更一致；但如果你只关心布尔开关，`toggled(bool)` 仍然简单。

### `sizeHint()` / `minimumSizeHint()`

返回包含指示框、文本、字体、style 间距的推荐尺寸。不同平台复选框大小和文本间距可能不同。

布局里不要手动把复选框固定到某个像素高度；让 style 决定更像原生应用。

### `initStyleOption(QStyleOptionButton *option) const`

为自定义绘制填充当前复选框状态，包括 checked、三态、文本、图标、启用和焦点等信息。

子类绘制时应优先使用它，避免漏掉 `PartiallyChecked` 或禁用状态的视觉。

### `nextCheckState()` / `checkStateSet()`

`nextCheckState()` 定义用户激活控件时状态如何变化；`checkStateSet()` 处理程序设置状态后的钩子。

自定义三态循环、父子树选择规则、或“部分选中点击后直接全选”的行为，可以从这里入手。

### `hitButton()` / `event()` / `mouseMoveEvent()` / `paintEvent()`

这些是命中测试、事件和绘制相关的底层接口。普通使用不需要重写。

如果重写，要保持文本区域也可点击，这是复选框的常见用户预期；只让小方框可点会降低可用性。

## 5. 深入实践与常见坑

### 多选用复选框，单选用单选按钮

一组复选框默认可以同时选中多个。若业务规则只能选一个，用 `QRadioButton` 或 `QButtonGroup`，不要在每个 `toggled()` 里手动取消其他复选框。

### 三态要有真实语义

`PartiallyChecked` 应表示“部分应用”或“混合值”。如果只是“未知”，更适合显示说明文字或禁用状态，而不是让用户猜第三态。

### 保存配置时别丢状态

二态配置保存 bool 即可；三态配置要保存 `Qt::CheckState` 或自己的枚举。把部分选中压成 true/false 会丢信息。
