# QAction：把一个命令统一投射到菜单、工具栏和快捷键

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAction>`  
> 模块：Qt GUI，链接 `Qt6::Gui`  
> 继承：`QObject`

## 它解决什么问题

同一个“保存”命令往往同时出现在菜单、工具栏、右键菜单和快捷键中。若每个入口各自维护文本、图标、是否可用和执行代码，很快就会出现一个入口已禁用、另一个入口仍可点击的状态分裂。

`QAction` 是这条命令的单一状态源。它保存显示信息、可用性、可见性、快捷键和可选中状态；把同一动作加入多个界面容器后，各容器会根据动作状态自动同步。真正的业务行为通常连接到 `triggered()` 信号。

它不是菜单项，也不是工具按钮。`QMenu`、`QToolBar`、`QToolButton` 和 `QWidget` 等对象是动作的展示或承载者，`QAction` 才是可复用的命令模型。

## 典型使用方式

动作通常由其使用窗口拥有。先创建动作、设置语义，再将它加入所需的 UI 入口：

```cpp
auto *saveAction = new QAction(
    QIcon::fromTheme("document-save"), tr("&Save"), this);

saveAction->setShortcut(QKeySequence::Save);
saveAction->setStatusTip(tr("Save the current document"));
saveAction->setEnabled(documentIsModified());

fileMenu->addAction(saveAction);
mainToolBar->addAction(saveAction);
addAction(saveAction); // 让窗口注册此动作及其快捷键

connect(saveAction, &QAction::triggered, this, &MainWindow::saveDocument);
```

即使使用 `Qt::ApplicationShortcut`，动作也必须先加入某个 widget，快捷键才能生效。窗口中动作状态变动时，菜单和工具栏会跟着更新，无须分别修改它们。

## 命令动作、开关动作与动作组

默认动作是命令动作，触发时只发出 `triggered()`，例如“保存”或“打印”。调用 `setCheckable(true)` 后，它可维护开与关的状态，适合粗体、显示网格等切换命令。

```cpp
auto *boldAction = new QAction(tr("&Bold"), this);
boldAction->setCheckable(true);
connect(boldAction, &QAction::toggled, editor, &Editor::setBold);
```

只有可选中动作才能处于 checked 状态。`setChecked()` 和 `toggle()` 改变状态会发出 `toggled()` 与 `changed()`，但**不会**发出 `triggered()`。需要表达用户或代码真正执行命令时，监听 `triggered(bool)`；需要表达状态本身变化时，监听 `toggled(bool)`。

将多个可选中动作放进 `QActionGroup` 可实现互斥，例如左对齐、居中和右对齐。动作组约束的是可选中状态，不能替代各动作自身的业务实现。

## 触发、悬停与禁用的区别

`trigger()` 是 `activate(QAction::Trigger)` 的便捷槽，走正常触发路径并发出 `triggered()`。对于可选中动作，信号参数携带当前 checked 状态。

`hover()` 是 `activate(QAction::Hover)` 的便捷槽，只发出 `hovered()`，适合状态栏预览和菜单高亮反馈，不执行命令。

`enabled` 为 `false` 的动作在菜单和工具栏中通常仍显示为灰色，用户不能选择，快捷键也不能触发它；`visible` 为 `false` 的动作则完全不显示，也不能选择。两者不是同一回事。

动作被加入的所有 widget 都禁用或不可见时，Qt 会使动作不可用。`resetEnabled()` 用来清除显式设置，让这种由关联宿主决定的可用性重新生效；它不是单纯的 `setEnabled(true)`。

## 文本、图标和平台表现

`text` 是菜单和按钮的主要描述。带 `&` 的文本可由支持助记符的 UI 创建快捷访问键，例如 `tr("&Open")`；需要显示字面量 `&` 时写成 `&&`。

`iconText` 是工具栏显示文字及若干回退场景使用的短描述；未显式设置时通常从 `text` 派生。`toolTip` 未显式设置时使用动作文本，`statusTip` 用于状态栏，`whatsThis` 则可提供富文本帮助。

图标是否显示在菜单中默认跟随应用属性 `Qt::AA_DontShowIconsInMenus`，`setIconVisibleInMenu()` 可以为单个动作覆盖它。右键菜单中的快捷键显示也可由 `shortcutVisibleInContextMenu` 单独覆盖应用属性。

`font` 和 `priority` 都是展示提示，具体样式和平台可以不完全采纳。例如工具栏采用图标旁文字模式时，低优先级动作可能不显示文字。

## 快捷键的边界

`setShortcut()` 设置唯一主快捷键。`setShortcuts(const QList<QKeySequence> &)` 可设置多个，列表第一个是主快捷键；`setShortcuts(QKeySequence::StandardKey)` 则根据当前平台填入该标准命令的按键组合。

`shortcutContext` 默认是 `Qt::WindowShortcut`。将范围扩大到应用级之前，要排查同一快捷键是否在其他窗口或插件中已被占用。`autoRepeat` 默认开启，用户持续按住快捷键且系统允许按键重复时，会重复触发动作；对保存、删除等不应重复执行的命令，应考虑关闭它。

## 生命周期、关联对象与菜单角色

建议把动作创建为主窗口或明确拥有者的子对象。动作可以同时添加到多个菜单、工具栏或 widget，但这些关联对象不拥有动作本身；动作析构时会从它们中解除。

`associatedObjects()` 返回当前添加过此动作的对象列表，是 Qt 6 的通用查询接口。不要为了“找宿主”长期保存该列表里的裸指针，关联可能在运行时改变。

将动作的 parent 设为 `QActionGroup`，会自动加入该组。`setActionGroup()` 也会建立组关联。`data` 是业务自定义的 `QVariant` 附加数据，例如枚举、文档 ID 或命令参数，不参与 UI 展示。

`menuRole` 影响 macOS 应用菜单中关于、偏好设置、退出等系统菜单项的放置。它只对菜单栏直接菜单中的动作有效，且在 macOS 上必须在动作进入菜单栏之前设置，通常就是首个窗口显示之前。

## 常见误区

- 为菜单、工具栏各建一个“保存”动作。应复用一个 `QAction`，让状态自动同步。
- 仅创建动作却未将其加入任何 widget，随后期待快捷键生效。
- 将 `setChecked()` 当作执行命令，误以为它会发 `triggered()`。
- 把 `visible(false)` 当作“暂时不可用”。前者会隐藏入口，后者应该用 `setEnabled(false)`。
- 将 `QAction` 放入 `QActionGroup` 却忘记 `setCheckable(true)`，互斥规则不会产生可见效果。
- 在 macOS 菜单栏展示后再修改 `menuRole`，期望系统重排应用菜单。

## API 速查表

| 类别 | API | 含义 | 使用重点 |
| --- | --- | --- | --- |
| 枚举 | `ActionEvent::Trigger` | 激活时发送触发相关信号。 | `activate()` 的常用参数，等价于 `trigger()` 路径。 |
| 枚举 | `ActionEvent::Hover` | 激活时发送悬停相关信号。 | 等价于 `hover()` 路径，不执行命令。 |
| 枚举 | `MenuRole::NoRole` | 不放入 macOS 应用菜单。 | 仅影响对应平台的菜单栏整合。 |
| 枚举 | `MenuRole::TextHeuristicRole` | 根据文本推断 macOS 应用菜单角色。 | 默认值，依赖菜单文本和平台规则。 |
| 枚举 | `MenuRole::ApplicationSpecificRole` | 标记为应用特定角色。 | 用于应用菜单整合。 |
| 枚举 | `MenuRole::AboutQtRole` | 表示“关于 Qt”动作。 | 供 macOS 应用菜单处理。 |
| 枚举 | `MenuRole::AboutRole` | 表示“关于本应用”动作。 | macOS 可改用应用名称生成菜单文本。 |
| 枚举 | `MenuRole::PreferencesRole` | 表示偏好设置动作。 | 应在首次放入 macOS 菜单栏前设置。 |
| 枚举 | `MenuRole::QuitRole` | 表示退出动作。 | 应在首次放入 macOS 菜单栏前设置。 |
| 枚举 | `Priority::LowPriority` | 低 UI 优先级。 | 工具栏可能隐藏文字标签。 |
| 枚举 | `Priority::NormalPriority` | 普通 UI 优先级。 | 默认的中性优先级。 |
| 枚举 | `Priority::HighPriority` | 高 UI 优先级。 | 仅为展示优先级提示。 |
| 构造 | `QAction(QObject *parent = nullptr)` | 创建空描述的动作。 | 建议指定拥有窗口或动作组作为 parent。 |
| 构造 | `QAction(const QString &text, QObject *parent = nullptr)` | 创建带文本的动作。 | 文本会派生默认工具提示和图标文字。 |
| 构造 | `QAction(const QIcon &icon, const QString &text, QObject *parent = nullptr)` | 创建带图标和文本的动作。 | 父对象为动作组时会自动加入组。 |
| 生命周期 | `~QAction()` | 销毁动作并解除关联。 | 宿主不拥有动作，避免重复释放。 |
| 关联 | `QList<QObject *> associatedObjects() const` | 返回已添加该动作的对象。 | Qt 6 起可用；返回的是非拥有对象指针快照。 |
| 关联 | `void setActionGroup(QActionGroup *group)` | 加入或切换所属动作组。 | 组内可选中动作可受互斥策略约束。 |
| 关联 | `QActionGroup *actionGroup() const` | 返回所属动作组。 | 未被组管理时为 `nullptr`。 |
| 展示 | `void setIcon(const QIcon &icon)` / `QIcon icon() const` | 读写动作图标。 | 空图标会清除图标；菜单显示还受可见设置影响。 |
| 展示 | `void setText(const QString &text)` / `QString text() const` | 读写主描述文本。 | `&` 可定义助记符，`&&` 显示字面量 `&`。 |
| 展示 | `void setIconText(const QString &text)` / `QString iconText() const` | 读写工具栏等处的短描述。 | 未显式设置时会回退到主文本。 |
| 展示 | `void setToolTip(const QString &tip)` / `QString toolTip() const` | 读写工具提示。 | 未单独设置时通常回退为动作文本。 |
| 展示 | `void setStatusTip(const QString &tip)` / `QString statusTip() const` | 读写状态栏提示。 | 用 `showStatusText()` 可主动发送状态提示事件。 |
| 展示 | `void setWhatsThis(const QString &text)` / `QString whatsThis() const` | 读写 What's This 帮助文本。 | 可以使用富文本。 |
| 展示 | `void setFont(const QFont &font)` / `QFont font() const` | 读写动作文字字体提示。 | 样式或平台可忽略这项提示。 |
| 展示 | `void setPriority(Priority priority)` / `Priority priority() const` | 读写界面展示优先级。 | 不影响执行顺序或业务优先级。 |
| 分隔 | `void setSeparator(bool on)` / `bool isSeparator() const` | 将动作标记为分隔符。 | 多数容器会忽略其文本、图标和子菜单。 |
| 快捷键 | `void setShortcut(const QKeySequence &shortcut)` / `QKeySequence shortcut() const` | 设置或读取唯一主快捷键。 | 会替换其他快捷键。 |
| 快捷键 | `void setShortcuts(const QList<QKeySequence> &shortcuts)` | 设置多个触发快捷键。 | 第一个是主快捷键。 |
| 快捷键 | `void setShortcuts(QKeySequence::StandardKey key)` | 按平台标准命令填入快捷键列表。 | 结果随运行平台而变。 |
| 快捷键 | `QList<QKeySequence> shortcuts() const` | 返回全部快捷键。 | 用于展示、冲突检查或复制配置。 |
| 快捷键 | `void setShortcutContext(Qt::ShortcutContext context)` / `Qt::ShortcutContext shortcutContext() const` | 设置或读取快捷键作用范围。 | 默认 `Qt::WindowShortcut`；扩大范围前检查冲突。 |
| 快捷键 | `void setAutoRepeat(bool on)` / `bool autoRepeat() const` | 控制按住快捷键时是否重复触发。 | 默认 `true`，不宜重复的命令可关闭。 |
| 状态 | `void setCheckable(bool on)` / `bool isCheckable() const` | 设置或读取是否支持选中状态。 | 默认 `false`；互斥组只约束可选中动作。 |
| 状态 | `void setChecked(bool on)` / `bool isChecked() const` | 设置或读取选中状态。 | 只对可选中动作有意义，改变时发 `toggled()`，不发 `triggered()`。 |
| 状态 | `void toggle()` | 翻转选中状态的槽。 | 连接前应确保动作可选中。 |
| 状态 | `void setEnabled(bool on)` / `bool isEnabled() const` | 显式设置或读取是否可用。 | 禁用后仍显示但不可触发，快捷键也失效。 |
| 状态 | `void setDisabled(bool disabled)` | `setEnabled(!disabled)` 的便捷槽。 | 适合直接连接信号。 |
| 状态 | `void resetEnabled()` | 清除显式可用性设置。 | 恢复由关联 widget 状态决定的自动行为。 |
| 状态 | `void setVisible(bool on)` / `bool isVisible() const` | 设置或读取是否显示。 | 隐藏后不显示也不能选择，不等于禁用。 |
| 数据 | `void setData(const QVariant &data)` / `QVariant data() const` | 写入或读取业务附加数据。 | 仅供应用使用，不自动显示或持久化。 |
| 激活 | `void activate(ActionEvent event)` | 按 `Trigger` 或 `Hover` 发送相应信号。 | 面向动作控件的底层入口。 |
| 激活 | `void trigger()` | 触发动作的槽。 | 调用 `activate(Trigger)`，会发 `triggered()`。 |
| 激活 | `void hover()` | 高亮动作的槽。 | 调用 `activate(Hover)`，只发 `hovered()`。 |
| 菜单 | `void setMenu(QMenu *menu)` / `QMenu *menu() const` | 设置或取得动作携带的子菜单。 | 主要用于 widget 应用中的子菜单或工具栏弹出菜单。 |
| 菜单 | `void setMenuRole(MenuRole role)` / `MenuRole menuRole() const` | 设置或读取 macOS 应用菜单角色。 | 仅菜单栏直接菜单有效，需在首次加入前设置。 |
| 菜单 | `void setIconVisibleInMenu(bool on)` / `bool isIconVisibleInMenu() const` | 控制本动作菜单中是否显示图标。 | 显式设置会覆盖应用级图标显示属性。 |
| 菜单 | `void setShortcutVisibleInContextMenu(bool on)` / `bool isShortcutVisibleInContextMenu() const` | 控制右键菜单中是否显示快捷键。 | 显式设置会覆盖应用级显示偏好。 |
| 状态栏 | `bool showStatusText(QObject *object = nullptr)` | 向相关状态栏发送 `QStatusTipEvent`。 | 成功发送返回 `true`；空对象时发给动作 parent。 |
| 信号 | `void changed()` | 动作的大部分展示和快捷键属性发生变化时发出。 | 需要刷新动作视图时可监听；选中改变还会同时触发它。 |
| 信号 | `void enabledChanged(bool enabled)` | 可用性变化时发出。 | 不要通过轮询 `isEnabled()` 代替。 |
| 信号 | `void checkableChanged(bool checkable)` | 是否可选中变化时发出。 | 与 `toggled()` 不同，后者是 checked 状态变化。 |
| 信号 | `void visibleChanged()` | 可见性变化时发出。 | 隐藏和禁用是不同状态。 |
| 信号 | `void triggered(bool checked = false)` | 动作被用户或 `trigger()` 激活时发出。 | `setChecked()`、`toggle()` 不会发出它。 |
| 信号 | `void hovered()` | 动作被用户高亮时发出。 | 不表示命令已执行。 |
| 信号 | `void toggled(bool checked)` | 可选中动作的 checked 状态变化时发出。 | `setChecked()` 和用户切换都会触发。 |
| 受保护 | `bool event(QEvent *event)` | `QObject::event()` 的重写。 | 仅子类扩展内部事件行为时使用，通常无需重写。 |
