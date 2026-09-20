# Qt QAccessibleWidget 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QAccessibleWidget>`
> 所属模块：`Qt6::Widgets`
> 继承：`QAccessibleObject`、`QAccessibleActionInterface`

## 它解决什么问题

`QAccessibleWidget` 是 Qt Widgets 可访问性体系里给 `QWidget` 使用的默认适配基类。屏幕阅读器、自动化测试工具、辅助输入设备并不直接理解一个 QWidget 如何绘制，它们需要一个 `QAccessibleInterface` 来回答“这个对象在哪里、叫什么、是什么角色、是否可用、能执行哪些动作、有哪些子对象”。`QAccessibleWidget` 就把 QWidget 的常见信息转换成这些可访问性语义。

普通应用很少直接操作它。你真正会碰到它的场景通常是：写了一个自定义 QWidget，默认可访问性信息不够准确；或者实现一个复合控件，需要给辅助技术暴露更细的角色、文本、状态、动作和关系。此时可以派生 `QAccessibleWidget`，再通过 `QAccessible::installFactory()` 让 Qt 在查询该控件时创建对应接口。

它不是一个可显示控件，也不是给布局使用的对象。它是“控件到辅助技术之间的说明书”。

## 典型使用场景

- 自定义按钮、旋钮、时间轴、图形面板需要被屏幕阅读器正确读出。
- 一个 QWidget 内部绘制了多个虚拟子元素，需要把它们暴露为可访问子对象。
- 控件除了点击以外还有自定义动作，需要通过 `QAccessibleActionInterface` 暴露给键盘和辅助设备。
- 控件之间存在标签、控制、描述等关系，需要在 `relations()` 中返回。

如果只是普通 `QPushButton`、`QLineEdit`、`QComboBox` 等标准控件，Qt 已经提供了相应可访问性实现，不需要自己创建 `QAccessibleWidget`。

## 使用模型

`QAccessibleWidget` 围绕一个 `QWidget *` 工作。构造时传入 widget、角色和可选名称，之后它的大多数函数都从 widget 的几何、状态、父子关系和属性中推导结果。

常见实现方式是派生一个接口类：

- 构造函数把目标 widget 交给 `QAccessibleWidget`。
- 重写 `text()`，返回更准确的 `Name`、`Description`、`Value`。
- 重写 `role()` 或在构造时选择合适的 `QAccessible::Role`。
- 重写 `state()`，补充选中、可展开、忙碌等自定义状态。
- 重写 `actionNames()` 和 `doAction()`，把辅助动作映射到控件行为。
- 如有虚拟子对象，重写 `childCount()`、`child()`、`indexOfChild()`、`focusChild()`。

`widget()` 是受保护函数，派生类通过它取得原 QWidget。调用前应先理解对象有效性：一旦底层 widget 被销毁，接口就不应继续当作有效对象使用。

## 关键语义与边界

### 生命周期

可访问接口通常由 Qt 的可访问性工厂按需创建，并由可访问性框架使用。不要把它当作普通业务对象长期散落保存。它的受保护析构函数也暗示了这一点：代码通常不在栈上直接创建 `QAccessibleWidget`，而是在工厂中返回接口指针。

### 角色和文本

`QAccessible::Role` 决定辅助技术如何理解控件。角色选错时，屏幕阅读器可能用错误方式朗读或操作它。构造函数中的 `name` 可以给对象一个初始可访问名称，但更复杂的控件通常重写 `text()`，按 `QAccessible::Text` 类型分别返回名称、描述、值、帮助文本等。

### 几何坐标

`rect()` 返回屏幕坐标中的矩形，而不是 widget 局部坐标。自定义子对象同样要注意坐标系，否则辅助工具会在错误位置高亮或点击。

### 动作接口

`QAccessibleWidget` 同时实现 `QAccessibleActionInterface`。默认动作通常覆盖标准控件的基本行为；派生类如果增加动作，应保证 `actionNames()` 返回稳定名称，`doAction()` 能真正触发对应操作，`keyBindingsForAction()` 返回用户可以理解的快捷键。

### `QAccessibleWidgetV2`

Qt 还提供 `QAccessibleWidgetV2`，它在 `QAccessibleWidget` 基础上实现 `QAccessibleAttributesInterface`，用于暴露属性键和值。只有当辅助技术需要额外结构化属性时才需要关注它。

## 常见误区

- 不要把 `QAccessibleWidget` 当作 QWidget 子类；它不绘制、不布局、不接收普通 GUI 输入。
- 不要只返回一个笼统 `Client` 角色；尽量选贴近真实控件的角色。
- 不要在 `text()` 中只返回视觉文本。辅助技术需要的是语义文本，必要时应补上单位、范围和状态。
- 自定义虚拟子对象时，要让 `childCount()`、`child()`、`indexOfChild()` 的索引模型一致。
- 底层 widget 状态变化后，要发送合适的可访问性事件，否则辅助工具可能不知道界面已经变化。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QAccessibleWidget(QWidget *w, QAccessible::Role role = QAccessible::Client)` | 为一个 QWidget 创建可访问接口，并指定角色。 | `w` 必须是接口要描述的真实控件；角色应尽量精确。 |
| 构造 | `QAccessibleWidget(QWidget *w, QAccessible::Role role, const QString &name)` | 创建接口并提供初始可访问名称。 | 名称应面向辅助技术用户，而不是内部对象名。 |
| 有效性 | `bool isValid() const` | 判断底层对象是否仍可作为可访问对象使用。 | 在 widget 生命周期变化后尤其要检查。 |
| 窗口 | `QWindow *window() const` | 返回控件所属窗口。 | 辅助技术用它关联顶层窗口和屏幕。 |
| 层级 | `int childCount() const` | 返回可访问子对象数量。 | 复合控件暴露虚拟子对象时要重写。 |
| 层级 | `QAccessibleInterface *child(int index) const` | 按索引返回子接口。 | 索引必须与 `childCount()` 和 `indexOfChild()` 一致。 |
| 层级 | `int indexOfChild(const QAccessibleInterface *child) const` | 查询子接口的索引。 | 找不到时按可访问性约定返回无效索引。 |
| 层级 | `QAccessibleInterface *parent() const` | 返回可访问父对象。 | 通常对应 QWidget 父子关系或窗口层级。 |
| 焦点 | `QAccessibleInterface *focusChild() const` | 返回当前拥有焦点的可访问子对象。 | 复合控件内部焦点需要由派生类准确暴露。 |
| 几何 | `QRect rect() const` | 返回对象屏幕矩形。 | 使用全局坐标，不是 widget 局部坐标。 |
| 文本 | `QString text(QAccessible::Text t) const` | 返回名称、描述、值等可访问文本。 | 按 `t` 区分语义；不要把所有内容塞进 `Name`。 |
| 角色 | `QAccessible::Role role() const` | 返回对象角色。 | 角色影响屏幕阅读器的朗读和操作模型。 |
| 状态 | `QAccessible::State state() const` | 返回可见、可用、焦点、选中等状态集合。 | 自定义状态变化后应发送可访问性事件。 |
| 颜色 | `QColor foregroundColor() const` | 返回前景色。 | 辅助工具可用于高对比度或视觉分析。 |
| 颜色 | `QColor backgroundColor() const` | 返回背景色。 | 结果来自控件和调色板语义。 |
| 关系 | `relations(QAccessible::Relation match) const` | 返回标签、控制、描述等可访问关系。 | 只返回与 `match` 匹配的关系，避免噪声。 |
| 接口转换 | `void *interface_cast(QAccessible::InterfaceType t)` | 暴露动作接口或其他可访问扩展接口。 | 派生类增加接口时要正确处理类型。 |
| 动作 | `QStringList actionNames() const` | 返回对象支持的可访问动作名称。 | 动作名称要稳定，可被辅助技术调用。 |
| 动作 | `void doAction(const QString &actionName)` | 执行指定可访问动作。 | 未支持的动作应安全忽略或按约定处理。 |
| 动作 | `QStringList keyBindingsForAction(const QString &actionName) const` | 返回某动作对应的快捷键说明。 | 只描述真实可用的用户输入路径。 |
| 派生辅助 | `QWidget *widget() const` | 取得被包装的 QWidget。 | 受保护；派生类使用前要考虑有效性。 |
| 派生辅助 | `QObject *parentObject() const` | 返回用于可访问父级推导的 QObject。 | 自定义层级时可作为基类逻辑参考。 |
| 派生辅助 | `void addControllingSignal(const QString &signal)` | 记录影响控制关系的信号。 | 用于派生接口补充控件间控制语义。 |

## 一句话总结

`QAccessibleWidget` 是自定义 QWidget 接入屏幕阅读器和辅助技术的基类：它不改变控件外观，而是把控件的角色、文本、状态、位置、关系和动作讲清楚。
