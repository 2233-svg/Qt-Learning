# QButtonGroup

> Qt 6.11.1 · Qt Widgets · 来自 `QButtonGroup`

## 1. 先建立直觉

`QButtonGroup` 是按钮的“逻辑分组器”，不是可见容器。它不会画边框，不会参与布局，也不会改变按钮摆放位置；它负责把若干 `QAbstractButton` 组织成一组，并统一处理互斥关系、整数 id 映射和点击信号。

如果你想要视觉上的分组，用 `QGroupBox`。如果你想让散落在不同布局位置的几个按钮仍然像一组选项一样互斥，就用 `QButtonGroup`。这个区别非常实用：视觉结构归布局和容器，选择规则归 button group。

## 2. 类说明

`QButtonGroup` 继承自 `QObject`。它可以管理 `QRadioButton`、`QCheckBox`、`QPushButton`、`QToolButton` 等继承自 `QAbstractButton` 的对象。

默认 `exclusive` 为 `true`，也就是组内一次只能选中一个按钮。对单选按钮来说这很自然；对复选框来说，如果你把它们放进互斥组，它们也会表现成单选逻辑。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QButtonGroup(QObject *)` | 创建一个逻辑按钮组。父对象只管理生命周期，不代表视觉父子关系。 |
| `addButton(QAbstractButton *, int id = -1)` | 把按钮加入组，并可分配业务 id。未指定 id 时 Qt 自动分配负数。 |
| `removeButton(QAbstractButton *)` | 从组中移除按钮，不会删除按钮本身。 |
| `buttons()` | 返回组内所有按钮。适合批量启用、禁用或同步样式。 |
| `button(int)` | 通过 id 找按钮。适合从配置值恢复 UI。 |
| `id(QAbstractButton *)` | 查询按钮对应 id。 |
| `setId(QAbstractButton *, int)` | 修改按钮 id。建议业务 id 使用正数，避开自动负数。 |
| `checkedButton()` | 返回当前选中的按钮；没有选中时返回 `nullptr`。 |
| `checkedId()` | 返回当前选中按钮的 id；没有选中时通常为 `-1`。 |
| `setExclusive(bool)` / `exclusive()` | 设置或读取互斥模式。 |
| `buttonClicked(QAbstractButton *)` | 任意按钮被点击时发出，适合需要对象指针的处理。 |
| `idClicked(int)` | 任意按钮被点击时发出，适合用枚举或配置值驱动业务。 |
| `buttonToggled(QAbstractButton *, bool)` | 按钮选中状态变化时发出。 |
| `idToggled(int, bool)` | id 版本的 toggled 信号，更适合保存设置。 |

## 4. 关键用法

用 id 把 UI 选项映射到业务枚举，是 `QButtonGroup` 最舒服的用法：

```cpp
auto *group = new QButtonGroup(this);
group->addButton(ui->fastModeRadio, 0);
group->addButton(ui->balancedModeRadio, 1);
group->addButton(ui->qualityModeRadio, 2);

connect(group, &QButtonGroup::idClicked, this, [this](int id) {
    setRenderMode(static_cast<RenderMode>(id));
});
```

如果只是让同一个父控件下的 `QRadioButton` 互斥，Qt 已经会按父对象做自动排他；但一旦按钮跨布局、跨容器，或者你想要稳定 id，显式 `QButtonGroup` 就更清楚。

## 5. 使用场景

它适合设置页中的模式选择、工具栏上的互斥工具、分布在不同面板里的单选状态、把按钮和枚举值绑定、多个 check box 需要“最多选一个”的特殊配置。

如果你只是想显示一个标题边框，不要用 `QButtonGroup`；它不可见。需要视觉容器时用 `QGroupBox`，需要按钮排列时用布局，三者可以组合但职责不同。

## 6. 常见坑与经验

`removeButton()` 不会销毁按钮，只是解除组关系。按钮生命周期仍由它自己的 parent 管理。

自动 id 是负数，从而给你留出正数作为业务 id。手动 id 建议一直用正数或明确的枚举值，不要混用隐式负数和业务值。

互斥组里用户不能通过再次点击当前按钮来取消选择。如果你需要“可取消的单选”，通常要自己设计状态逻辑，或者使用非互斥组加手动约束。
