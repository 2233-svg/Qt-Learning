# QAccessibleInterface

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleInterface`

## 1. 先建立直觉

`QAccessibleInterface` 是一个对象在无障碍树中的“语义代理”。它不负责画控件，而是向辅助技术描述对象的角色、名称、状态、屏幕位置、父子关系和可选能力。一个复杂自绘组件可能在视觉上是一个画布，在无障碍树中却需要成为一组可导航的按钮、表格单元格或文本元素。

这是实现自定义控件无障碍支持的核心协议。标准控件已有实现；只有标准映射不够时才应继承或使用 `QAccessibleObject`。

## 2. 类说明

- 头文件：`#include <QAccessibleInterface>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 来源类：抽象接口，通常通过 `QAccessible::queryAccessibleInterface()` 获取。
- 常用基类：`QAccessibleObject` 将接口关联到一个 `QObject`。
- 生命周期：Qt 缓存查询到的接口；调用者通常不拥有返回的接口指针。

可访问树不必等于 QObject 树。比如一个绘制在单一 QWidget 上的表格，应该暴露行、列和单元格等虚拟子节点；反过来，纯装饰子 QWidget 不一定值得进入可访问树。

## 3. API 速查

| API | 用途 |
|---|---|
| `isValid()` | 判断接口及其底层数据是否仍可用。 |
| `object()` | 返回关联 QObject。 |
| `role()` | 返回对象类别，如 Button、Heading、Table、TreeItem。 |
| `state()` | 返回焦点、禁用、选中、展开等状态位。 |
| `text(type)` | 读取 Name、Description、Value、Help、Identifier 等文本。 |
| `setText(type, text)` | 尝试设置可写文本属性；多数属性可能只读。 |
| `rect()` | 返回对象的**屏幕坐标**矩形。 |
| `parent()` / `childCount()` / `child(i)` | 浏览可访问树。 |
| `indexOfChild(child)` | 将子接口映射回直接子索引。 |
| `childAt(x, y)` | 通过屏幕坐标命中可访问后代。 |
| `focusChild()` | 返回当前拥有键盘焦点的后代或自身。 |
| `relations(mask)` | 查询标签、描述、控制等非父子关系。 |
| `interface_cast(type)` | 暴露动作、文本、值、表格、选择、属性等专用接口。 |
| `actionInterface()` 等辅助函数 | 对 `interface_cast()` 的类型安全快捷查询，可能返回 `nullptr`。 |
| `foregroundColor()` / `backgroundColor()` | 需要时返回可见颜色，否则无效颜色。 |
| `window()` | 返回关联窗口，供平台后端定位。 |

## 4. 关键用法

### 查询与安全使用

```cpp
QAccessibleInterface *iface =
    QAccessible::queryAccessibleInterface(customWidget);

if (iface && iface->isValid()) {
    const QRect screenRect = iface->rect();
    const QString title = iface->text(QAccessible::Name);

    if (auto *actions = iface->actionInterface())
        actions->doAction(QAccessibleActionInterface::pressAction());
}
```

专用接口指针不需要也不能由调用者删除。它们只在主接口有效期间可用；对象销毁、视图模型重置或虚拟子项更新后，旧指针都不应长期缓存。

### 自定义接口应维持的最小闭环

```cpp
QAccessible::Role AccessibleChip::role() const
{
    return QAccessible::Button;
}

QAccessible::State AccessibleChip::state() const
{
    QAccessible::State state;
    state.focusable = chip()->focusPolicy() != Qt::NoFocus;
    state.focused = chip()->hasFocus();
    state.disabled = !chip()->isEnabled();
    state.checked = chip()->isChecked();
    return state;
}
```

Role、State、Text、Rect 和树导航必须相互匹配。若报告 `Role::Button`，通常至少应有可识别 Name、正确禁用/焦点状态以及可选的 ActionInterface；若报告子节点，`childCount()`、`child()`、`indexOfChild()` 和 `parent()` 必须互相可逆。

## 5. 常见专用接口

| 能力 | 何时提供 |
|---|---|
| `QAccessibleActionInterface` | 对象可被激活、切换、增减或滚动。 |
| `QAccessibleTextInterface` | 文本可被读取、定位、选择或查询边界。 |
| `QAccessibleEditableTextInterface` | 文本可由辅助技术编辑。 |
| `QAccessibleValueInterface` | 有当前值、最小值、最大值和步进。 |
| `QAccessibleTableInterface` | 行列网格、表头、单元格语义。 |
| `QAccessibleTableCellInterface` | 单元格的行列位置、跨度与表归属。 |
| `QAccessibleSelectionInterface` | 非文本对象支持选择子项。 |
| `QAccessibleAttributesInterface` | 提供层级、语言、方向等扩展语义。 |

## 6. 常见坑与经验

- `rect()` 和 `childAt()` 使用全局屏幕坐标，不是 QWidget 局部坐标；多显示器和高 DPI 下更不能混用。
- `childAt()` 可以返回任意后代而非只返回直接孩子。表格、图表等大量虚拟项应重写为高效命中算法，避免线性遍历。
- Role 多数是稳定的，State 是动态的。不要每帧改变 Role 来描述外观变化。
- Name 需要短而可识别；Description 用于额外解释；Value 用于当前数据。三者混写会导致读屏冗长。
- `isValid()` 为 false 后必须停止使用接口；不要借由保存裸指针跨越对象或模型生命周期。
- `relations()` 是标签/描述/控制关系，不要用它重复表示普通父子树。
- 所有与 GUI 状态和可访问对象相关的读取、更新应遵守 GUI 线程边界。

## 7. 知识点覆盖

- 无障碍语义树与 QObject/视觉树的区别
- Role、State、Text、屏幕几何和树导航契约
- 专用接口的能力发现与安全指针使用
- 虚拟子节点、表格/画布的可访问建模
- 屏幕坐标、高 DPI、缓存有效期与事件同步
