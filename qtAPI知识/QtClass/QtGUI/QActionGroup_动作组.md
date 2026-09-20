# QActionGroup：管理一组动作的互斥与共同状态

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QActionGroup>`  
> 模块：Qt GUI，链接 `Qt6::Gui`  
> 继承：`QObject`

## 它解决什么问题

`QAction` 表示一个命令或可切换状态，但“左对齐、居中、右对齐”这类选项之间存在关系：它们应只选一个，或最多选一个。`QActionGroup` 把这批动作组织成一组，集中处理互斥检查、共同可用性、共同可见性以及组级的触发和悬停信号。

它不是菜单或工具栏。组本身不产生界面，也不会把动作自动放进菜单；动作仍要分别添加到 `QMenu`、`QToolBar` 或控件中。

## 最常见的使用方式

```cpp
#include <QAction>
#include <QActionGroup>

auto *alignment = new QActionGroup(this);
alignment->setExclusionPolicy(QActionGroup::ExclusionPolicy::Exclusive);

auto *left = alignment->addAction(tr("Left"));
auto *center = alignment->addAction(tr("Center"));
auto *right = alignment->addAction(tr("Right"));

for (QAction *action : alignment->actions())
    action->setCheckable(true);

left->setChecked(true);
connect(alignment, &QActionGroup::triggered, this,
        [this](QAction *action) { applyAlignment(action); });
```

这里三项必须设为可选中，互斥策略才有实际对象可约束。动作组并不会把普通命令动作变成可选中动作。

## 三种排斥策略

`ExclusionPolicy` 决定组内可选中动作之间的关系：

| 策略 | 语义 | 适合场景 |
| --- | --- | --- |
| `None` | 每个动作可以独立选中或取消选中。 | 多个独立开关，例如显示网格和吸附网格。 |
| `Exclusive` | 任意时刻恰好一个动作被选中，是默认策略。 | 对齐方式、绘图工具、单选模式。 |
| `ExclusiveOptional` | 最多一个动作被选中，但可以全都不选。 | 可取消的单选过滤器。 |

`isExclusive()` 对 `Exclusive` 和 `ExclusiveOptional` 都返回 `true`，因此它无法区分“必须有一项”与“可以全不选”。需要这个差别时应读取 `exclusionPolicy()`。

旧式 `setExclusive(true)` 等价于将策略设为 `Exclusive`，`setExclusive(false)` 等价于设为 `None`。它不能表达 `ExclusiveOptional`，新代码优先使用 `setExclusionPolicy()`。

## 组状态如何影响动作

`enabled` 和 `visible` 是组级控制：

- 组禁用时，成员动作会被禁用，除非该动作本身已经被显式禁用。
- 组隐藏时，成员动作会跟随隐藏，除非该动作本身已被显式隐藏。

这意味着组状态是额外约束，不应把它当成批量覆盖所有成员属性的简单赋值。要判断某个动作能否使用，应仍读取该动作的最终 `isEnabled()`、`isVisible()`。

## 加入、移除与所有权

创建动作时以组为父对象是最直观的做法，组析构时会一起销毁这些动作。`addAction(const QString &)` 和图标重载也会创建以组为父对象的动作。

`addAction(QAction *)` 用于把已有动作加入组。移除时 `removeAction()` 会使该动作不再属于组，且文档规定它随后没有 parent。因此若调用方仍要保留该动作，必须在移除前后重新安排其生命周期，例如设置新的父对象；不能假定它仍会被原组销毁。

`actions()` 返回动作指针列表的快照，列表本身可自由使用，但其中元素仍由各自动作的所有权关系管理。

## 信号语义

`triggered(QAction *)` 在组内某动作被用户激活时发出，适合把多个同类命令集中到一个槽处理。程序直接调用 `QAction::trigger()` 也会走相同的动作激活路径。

`hovered(QAction *)` 在用户高亮组内动作时发出，例如菜单项悬停、工具栏按钮悬停或使用其快捷键时。它不代表动作被执行。

组的信号只便于集中处理，业务仍可同时连接单个动作的 `triggered(bool)` 或 `toggled(bool)`，尤其当每项有不同业务逻辑时。

## API 速查表

| API | 含义 | 重点边界 |
| --- | --- | --- |
| `QActionGroup(QObject *parent)` | 创建动作组。 | 默认策略为 `Exclusive`；建议以窗口或拥有者为 parent。 |
| `~QActionGroup()` | 销毁动作组。 | 以组为 parent 的成员动作也会销毁。 |
| `QList<QAction *> actions() const` | 返回组内动作列表。 | 列表可为空，动作指针不因返回列表而转移所有权。 |
| `QAction *addAction(QAction *action)` | 将已有动作加入组并返回它。 | 适合已有动作；应明确后续 parent 和生命周期。 |
| `QAction *addAction(const QString &text)` | 创建文字动作并加入组。 | 新动作是组的子对象。 |
| `QAction *addAction(const QIcon &icon, const QString &text)` | 创建带图标的动作并加入组。 | 新动作是组的子对象。 |
| `void removeAction(QAction *action)` | 把动作从组移除。 | 移除后动作没有 parent，必要时立即重新指定所有者。 |
| `QAction *checkedAction() const` | 返回当前被选中的动作。 | 没有选中项时返回 `nullptr`。 |
| `ExclusionPolicy exclusionPolicy() const` | 读取排斥策略。 | 用它区分 `Exclusive` 和 `ExclusiveOptional`。 |
| `void setExclusionPolicy(ExclusionPolicy policy)` | 设置排斥策略。 | 只约束可选中的动作。 |
| `bool isExclusive() const` | 判断是否为某种互斥组。 | 对 `ExclusiveOptional` 同样为 `true`。 |
| `void setExclusive(bool on)` | 旧式互斥快捷设置。 | `true` 对应 `Exclusive`，`false` 对应 `None`，无法设可选互斥。 |
| `bool isEnabled() const` / `void setEnabled(bool)` | 读取或设置组可用性。 | 影响成员，除非成员本身已显式禁用。 |
| `void setDisabled(bool disabled)` | `setEnabled(!disabled)` 的槽函数形式。 | 适合直接连接信号。 |
| `bool isVisible() const` / `void setVisible(bool)` | 读取或设置组可见性。 | 影响成员，除非成员本身已显式隐藏。 |
| `void triggered(QAction *action)` | 组内动作被激活时发出的信号。 | 适合集中处理命令，不等同于 `toggled`。 |
| `void hovered(QAction *action)` | 组内动作被高亮时发出的信号。 | 仅表示悬停或高亮，不执行命令。 |
