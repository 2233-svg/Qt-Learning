# Qt QAccessibleInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleInterface>`  
> 所属模块：`Qt6::Gui`  
> 定位：向辅助技术暴露对象语义、层级、几何与可选能力的抽象核心接口

## 1. 它解决什么问题

`QAccessibleInterface` 是 Qt 无障碍系统的核心抽象。它把一个可被用户感知或操作的 UI 元素表示为可查询的对象：辅助技术可以读取名称、角色、状态、屏幕几何和对象关系，并通过可选的 action、value、text、table 等接口执行交互。

它不是 `QObject` 的替代品，也不要求每个可访问对象都有独立 QWidget：

- 一个 widget 可以有一个或多个 accessible 子元素；
- 一个自定义绘制的对象也能实现该接口；
- `QObject` parent/child 与 accessible parent/child 通常相关，但不保证一一对应；
- 对象间标签、描述、控制关系由 `relations()` 额外表达；
- interface 由 Qt 的无障碍缓存管理，客户端只借用返回指针。

自定义控件通常从 `QAccessibleObject` 或 Qt Widgets 的 `QAccessibleWidget` 派生，而不是从零实现所有 QObject 关联细节。

## 2. 实现时必须保持的四份事实一致

一个可访问对象的接口必须让以下信息彼此一致：

1. **层级**：`parent()`、`childCount()`、`child()` 和 `indexOfChild()` 能互相反查。
2. **几何**：`rect()` 和 `childAt()` 使用同一套屏幕坐标与命中规则。
3. **语义**：`role()`、`state()`、`text()` 与真实 UI 行为一致。
4. **能力**：只有真支持的能力才从 `interface_cast()` 返回对应接口，且 `actionNames()` 不暴露不可执行操作。

辅助技术会以任意顺序、在对象状态变化时重复调用这些函数。实现不应依赖某个固定调用顺序，也不应在查询函数里修改 UI、访问网络或执行阻塞计算。

## 3. 最小实现骨架

```cpp
class BadgeAccessible final : public QAccessibleObject
{
public:
    explicit BadgeAccessible(Badge *badge)
        : QAccessibleObject(badge)
    {
    }

    QAccessibleInterface *parent() const override;
    QAccessibleInterface *child(int index) const override;
    int childCount() const override;
    int indexOfChild(const QAccessibleInterface *child) const override;

    QString text(QAccessible::Text type) const override;
    QAccessible::Role role() const override;
    QAccessible::State state() const override;
};
```

派生类通常还要提供专用 factory，让 `QAccessible::queryAccessibleInterface()` 能创建它。若手工创建子 interface，必须按 `QAccessible::registerAccessibleInterface()` 的缓存规则管理，不能随意 `delete`。

## 4. 生命周期、线程与坐标

### 生命周期

析构函数是 protected，调用方不能把从 Qt 查询到的 `QAccessibleInterface *` 当作自己拥有的对象来删除。对象、接口与缓存的删除由 Qt 无障碍框架协调。

每个公开查询入口都要能应对对象在两次调用之间被销毁：`isValid()` 为 `false` 时，不应继续读取底层 QObject；`child()`、`parent()`、专用 interface accessor 和颜色查询都可能返回空/无效结果。

### 线程

可访问接口通常读取 GUI 对象，因此应在对象所属 GUI 线程使用。后台线程不得直接查询或修改 QWidget、QQuickItem 或其 accessible interface；跨线程请求应排队回 GUI 线程。

### 坐标

`rect()` 和 `childAt(x, y)` 使用**屏幕坐标**，不是控件局部坐标、视口坐标或文档坐标。不可见对象的布局数据可能不可靠；`childAt()` 对不可见对象不应承诺稳定命中结果。

## 5. 层级、命中与关系 API

### `virtual bool isValid() const = 0`

返回实现所依赖的数据是否仍有效，例如底层对象和必要模型索引仍可用。它不是“控件是否 enabled”，启用状态应在 `state().disabled` 中表达。

### `virtual QObject *object() const = 0`

返回被包装的 QObject。返回的是非拥有指针，必须与 `isValid()` 协同使用。无 QObject 的实现可按自己的接口契约返回空，但应确保其他方法仍有明确行为。

### `virtual QWindow *window() const`

返回底层对象关联的窗口，默认实现返回 `nullptr`。某些平台后端会向上遍历 accessible ancestors 寻找一个有效 `QWindow` 以报告状态变化，因此至少某个祖先应能返回窗口。

### `virtual QAccessibleInterface *parent() const = 0`

返回 accessible 树中的父对象；根对象返回 `nullptr`。返回 pointer 由 Qt 管理，不能删除。

### `virtual QAccessibleInterface *child(int index) const = 0`

按 0 起始索引返回直接 child。索引无效或 child 在查询间失效时返回 `nullptr`。它必须与 `childCount()`、`indexOfChild()` 保持一致。

### `virtual int childCount() const = 0`

返回直接 accessible 子项数量。子项既可以对应 child widget，也可以是同一控件内部的逻辑元素，例如滑块增减按钮、表格单元格或自绘图形元素。

### `virtual int indexOfChild(const QAccessibleInterface *child) const = 0`

返回 `child` 在直接子项中的 0 起始索引；不是子项时返回 `-1`。不要把模型行号或业务 ID 直接作为返回值，除非它恰好与 accessible child 顺序一致。

### `virtual QAccessibleInterface *childAt(int x, int y) const = 0`

返回包含屏幕点 `(x, y)` 的 child。返回者可以是后代而不一定是直接 child，以便跳过中间容器层；没有命中时返回 `nullptr`。

大型表格、树和画布不应简单遍历全部 child 来命中，应使用模型/布局的空间索引。`QAccessibleObject` 提供遍历 QObject 子项的默认实现，适合小型普通对象树。

### `virtual QAccessibleInterface *focusChild() const`

返回当前拥有键盘焦点的对象，可以是自身或任意后代；没有焦点时可返回 `nullptr`。它不是返回“可聚焦 child”，而是当前真实焦点位置。

### `virtual QList<std::pair<QAccessibleInterface *, QAccessible::Relation>> relations(QAccessible::Relation match = QAccessible::AllRelations) const`

返回有意义的非层级关系，可用 `match` 过滤。常见的是 label/labelled、description/described 和 controller/controlled；通常不应把普通 parent/child 重复放入此列表，且绝不能返回自身。

列表中的 interface pointer 只借用。关系方向必须正确：若本对象是标签，用 `Label`；若本对象被标签指向，用 `Labelled`。

## 6. 属性与状态 API

### `virtual QAccessible::Role role() const = 0`

返回对象角色。角色通常稳定，表达对象的交互语义，例如 `Button`、`EditableText`、`Table`、`Heading` 或 `Slider`，不是表面样式。错误角色会让辅助技术提示错误操作方式。

### `virtual QAccessible::State state() const = 0`

返回当前状态位快照。必须忠实反映 enabled、focus、selected、expanded、visible、read-only 等真实状态；详细字段见 [QAccessible_State_状态.md](D:\笔记\qtAPI知识\QtClass\QtGUI\QAccessible_State_状态.md)。

状态改变后，控件还需要发合适的 `QAccessibleStateChangeEvent`，不能只指望客户端轮询。

### `virtual QString text(QAccessible::Text type) const = 0`

返回指定类别的文本。每个对象至少应为 `QAccessible::Name` 提供可识别且在容器内尽量唯一的文本；`Description` 用于补充外观/上下文，`Value` 用于当前值，`Help` 用于用法，`Accelerator` 用于默认动作快捷键，`Identifier` 可用于测试稳定标识。

不要把同一段长文同时塞入 Name、Description 和 Help，也不要把密码、访问令牌等敏感文本暴露为 Value。

### `virtual void setText(QAccessible::Text type, const QString &text) = 0`

尝试设置某种文本属性。大多数对象的文本是只读，因此此函数可以无效果；实现不得为了满足接口而绕过控件的只读、验证、权限和业务限制。

真正发生可访问文本变化后，应发送正确的名称、描述、值或文本变化事件。

### `virtual QRect rect() const = 0`

返回对象的屏幕几何。视觉对象都应提供它；不可见对象可能没有可靠排版结果。返回空/无效矩形通常表示当前没有可用几何，而不是隐藏某个仍能交互的屏幕对象。

### `virtual QColor foregroundColor() const` / `virtual QColor backgroundColor() const`

返回前景或背景色；不适用时返回无效 `QColor`。颜色是补充信息，不能替代名称、角色和状态；自绘控件也不应为了回答查询而强制创建图形资源。

## 7. 专用能力接口

下列便捷函数都通过 `interface_cast()` 取得能力。调用结果可能为 `nullptr`，不转移所有权：

| API | 取得的能力 | 适用对象 |
| --- | --- | --- |
| `textInterface()` | `QAccessibleTextInterface` | 大型/富文本内容和文档视图。 |
| `editableTextInterface()` | `QAccessibleEditableTextInterface` | 真正可编辑的文本对象。 |
| `valueInterface()` | `QAccessibleValueInterface` | slider、scrollbar、spinbox 等数值对象。 |
| `actionInterface()` | `QAccessibleActionInterface` | 能执行 press、toggle、滚动等动作的对象。 |
| `imageInterface()` | `QAccessibleImageInterface` | 有图片描述、位置和尺寸语义的对象。 |
| `tableInterface()` | `QAccessibleTableInterface` | 表、树、列表等行列结构。 |
| `tableCellInterface()` | `QAccessibleTableCellInterface` | 单个表格单元格。 |
| `hyperlinkInterface()` | `QAccessibleHyperlinkInterface` | 超链接。 |
| `selectionInterface()` | `QAccessibleSelectionInterface`，Qt 6.5 起 | 公开集合选择操作的对象。 |
| `attributesInterface()` | `QAccessibleAttributesInterface`，Qt 6.8 起 | 公开对象级 key-value 属性的对象。 |

### `virtual void *interface_cast(QAccessible::InterfaceType type)`

默认返回 `nullptr`。实现多个专用接口时按 `type` 返回正确的接口地址：

```cpp
void *EditorAccessible::interface_cast(QAccessible::InterfaceType type)
{
    if (type == QAccessible::TextInterface)
        return static_cast<QAccessibleTextInterface *>(this);
    if (type == QAccessible::EditableTextInterface)
        return static_cast<QAccessibleEditableTextInterface *>(this);
    return QAccessibleObject::interface_cast(type);
}
```

返回的地址必须确实实现请求的接口；不要用不相关指针配合 `reinterpret_cast` 伪造能力。若接口有条件可用，状态变化时也要确保返回值与 `state()`、action 列表一致。

### `virtual void virtual_hook(int id, void *data)`

Qt 预留的二进制兼容扩展钩子。普通应用和自定义 accessible object 不应依赖、调用或覆盖它来定义业务协议；未来 Qt 可能使用 `id` 和 `data` 承载内部扩展。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- |
| 生命周期 | `~QAccessibleInterface()` | 受保护虚析构。 | 由 Qt 缓存/派生实现管理，客户端不可删除查询结果。 |
| 有效性 | `isValid()` | 判断底层数据是否仍可用。 | 不等于 enabled；失效后不要继续查询对象。 |
| 关联 | `object()` | 返回被包装 QObject。 | 非拥有指针，可能为空或失效。 |
| 窗口 | `window()` | 返回关联 QWindow。 | 默认 `nullptr`；祖先中应有可用窗口。 |
| 层级 | `parent()` | 返回 accessible 父项。 | 根返回 `nullptr`。 |
| 层级 | `child(int)` | 按 0 起始索引返回直接 child。 | 无效/已失效 child 返回 `nullptr`。 |
| 层级 | `childCount()` | 返回直接 child 数。 | 必须与 `child()`、`indexOfChild()` 一致。 |
| 层级 | `indexOfChild(...)` | 查 child 的 0 起始索引。 | 非 child 返回 `-1`。 |
| 命中 | `childAt(int, int)` | 按屏幕坐标命中 child/后代。 | 只对可见对象可靠；不是局部坐标。 |
| 焦点 | `focusChild()` | 返回当前焦点对象或后代。 | 没有焦点可为 `nullptr`。 |
| 关系 | `relations(Relation)` | 返回非层级语义关系。 | 不返回自身；方向和 filter 要正确。 |
| 语义 | `role()` | 返回对象角色。 | 依据真实交互语义选择。 |
| 状态 | `state()` | 返回状态位快照。 | 改变后需额外发无障碍事件。 |
| 文本 | `text(Text)` | 返回名称、值、帮助等文本。 | Name 必须清晰；避免泄露敏感 Value。 |
| 文本 | `setText(Text, QString)` | 尝试修改文本属性。 | 大多只读；不得绕过业务约束。 |
| 几何 | `rect()` | 返回屏幕几何。 | 不可见对象可能不可靠。 |
| 颜色 | `foregroundColor()` / `backgroundColor()` | 返回可选颜色信息。 | 不适用时返回无效 QColor。 |
| 能力 | `textInterface()` | 取得文本接口。 | 不支持时 `nullptr`。 |
| 能力 | `editableTextInterface()` | 取得可编辑文本接口。 | 只在真实可编辑对象上提供。 |
| 能力 | `valueInterface()` | 取得数值接口。 | 不支持时 `nullptr`。 |
| 能力 | `actionInterface()` | 取得动作接口。 | 动作列表不含不可执行项。 |
| 能力 | `imageInterface()` | 取得图片接口。 | 不支持时 `nullptr`。 |
| 能力 | `tableInterface()` / `tableCellInterface()` | 取得表/单元格接口。 | 行列模型与 child 树语义保持一致。 |
| 能力 | `hyperlinkInterface()` | 取得链接接口。 | 不支持时 `nullptr`。 |
| 能力 | `selectionInterface()` | 取得选择接口。 | Qt 6.5 起，可能为 `nullptr`。 |
| 能力 | `attributesInterface()` | 取得对象属性接口。 | Qt 6.8 起，可能为 `nullptr`。 |
| 扩展 | `interface_cast(InterfaceType)` | 暴露实际实现的专用接口。 | 默认空；返回地址类型必须正确。 |
| 扩展 | `virtual_hook(int, void *)` | Qt 内部兼容扩展。 | 普通应用不要依赖或覆盖。 |

### 一句话总结

`QAccessibleInterface` 是辅助技术看到的对象模型：实现时要让层级、几何、角色、状态、文本和可选能力始终与真实 UI 同步，并把所有返回接口视为 Qt 缓存管理的短期借用对象。
