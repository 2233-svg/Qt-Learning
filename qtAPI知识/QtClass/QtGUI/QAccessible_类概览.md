# Qt QAccessible 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessible>`  
> 所属模块：`Qt6::Gui`  
> 定位：Qt 无障碍系统的静态门面、枚举定义和接口缓存入口

## 1. 它解决什么问题

`QAccessible` 不是要实例化的业务对象。它把 Qt 应用、可访问对象实现和平台辅助技术之间的公共协议集中在一个静态类中：

- 定义角色、状态、事件、文本和关系等无障碍语义；
- 为 `QObject` 查询对应的 `QAccessibleInterface`；
- 管理 accessible interface 的缓存 ID 和生命周期；
- 注册自定义 interface factory；
- 将变化事件通知给平台后端；
- 让应用设置可访问对象树的根。

辅助技术客户端，例如屏幕阅读器或盲文显示器，通过 `QAccessibleInterface` 查询对象信息；应用作为 server 在对象变化后调用 `QAccessible::updateAccessibility()` 发通知。`QAccessible` 本身不绘制 UI、不替代控件逻辑，也不保证每个平台都有相同的无障碍后端。

## 2. 最小使用模型

### 2.1 查询一个 QObject 的无障碍接口

```cpp
QAccessibleInterface *iface =
    QAccessible::queryAccessibleInterface(widget);

if (iface && iface->isValid()) {
    qDebug() << iface->text(QAccessible::Name)
             << iface->role();
}
```

返回的 interface 由 Qt 内部缓存管理，调用方不能删除。它可能为 `nullptr`，也可能在对象销毁、缓存清理或事件循环推进后不再可用；不要把裸指针长期保存。

### 2.2 在状态改变后发送事件

```cpp
void MySlider::setValue(int value)
{
    if (m_value == value)
        return;

    m_value = value;
    update();

    QAccessibleValueChangeEvent event(this, m_value);
    QAccessible::updateAccessibility(&event);
}
```

事件要在真实状态改变之后发送。若要构造事件 payload 的代价较高，可先用 `isActive()` 判断是否有平台请求无障碍信息；即使返回 `false`，仍可以调用 `queryAccessibleInterface()`，只是通知不会送达平台后端。

## 3. 工厂、缓存与所有权

### 3.1 `queryAccessibleInterface()` 是默认入口

它按最近安装优先的顺序调用 factory；如果没有 factory 提供实现，再尝试加载无障碍插件；若对象本身的类没有实现，还会向父类查找。Qt 把找到的 interface 放入内部缓存。

所以普通代码应优先调用 `queryAccessibleInterface()`，不要 `new` 一个 `QAccessibleInterface` 后直接塞给客户端。

### 3.2 手工创建 interface 的例外

如果实现 `QAccessibleInterface::child()` 时必须动态 `new` 子 interface，必须对每个 interface **恰好一次**调用 `registerAccessibleInterface()`，交给 Qt 缓存管理：

```cpp
auto *child = new MyItemAccessible(item);
QAccessible::registerAccessibleInterface(child);
return child;
```

之后不能自己删除它；需要删除时使用 `deleteAccessibleInterface(id)`。删除会从缓存移除并析构 interface，ID 随后无效且可能被复用。

### 3.3 `Id` 不是持久标识

`QAccessible::Id` 是无符号缓存标识，用于临时定位 `QAccessibleInterface`。它不等同于 QObject 地址、业务主键或可序列化 ID。对象被删除或 cache 清理后，旧 ID 不能继续使用。

## 4. 核心类型与枚举

### `State`

`QAccessible::State` 是可访问对象的位字段，由 `QAccessibleInterface::state()` 返回。它的字段、状态组合和变化事件用法见独立笔记：[QAccessible_State_状态.md](D:\笔记\qtAPI知识\QtClass\QtGUI\QAccessible_State_状态.md)。

### `Role`

`Role` 表示对象的语义类别。必须选择最接近真实交互目的的角色，不能只因外观相似就把所有可点击项标成 `Button`。

| 角色分组 | 枚举值 |
| --- | --- |
| 应用与窗口 | `NoRole`、`Application`、`Window`、`Dialog`、`Client`、`TitleBar`、`Border`、`Pane`、`LayeredPane`、`Desktop`、`ToolTip`、`HelpBalloon`、`Notification` |
| 菜单与命令 | `MenuBar`、`PopupMenu`、`MenuItem`、`ToolBar`、`StatusBar`、`Button`、`ButtonDropDown`、`ButtonMenu`、`ButtonDropGrid`、`CheckBox`、`RadioButton`、`Switch` |
| 输入与值 | `EditableText`、`HotkeyField`、`ComboBox`、`SpinBox`、`Slider`、`Dial`、`ProgressBar`、`ScrollBar`、`Indicator` |
| 文本与文档 | `Document`、`WebDocument`、`Terminal`、`Paragraph`、`Section`、`Heading`、`Footer`、`Form`、`Note`、`BlockQuote`、`StaticText`、`Whitespace`、`Link` |
| 集合与数据 | `List`、`ListItem`、`Tree`、`TreeItem`、`Table`、`Row`、`Column`、`Cell`、`RowHeader`、`ColumnHeader`、`PageTabList`、`PageTab`、`PropertyPage` |
| 图形与布局 | `Graphic`、`Canvas`、`Chart`、`ColorChooser`、`Animation`、`Equation`、`Splitter`、`Separator`、`Grouping`、`Grip` |
| 其他 | `Sound`、`Cursor`、`Caret`、`AlertMessage`、`Assistant`、`Clock`、`ComplementaryContent`、`UserRole` |

头文件中 `PushButton` 是 `Button` 的已弃用别名；新代码用 `Button`。`UserRole` 是用户自定义角色的起始值，使用前必须确认目标平台后端能否理解自定义语义。

### `Text`

`QAccessibleInterface::text()` 与 `setText()` 使用的文本类别：

| 枚举值 | 语义 |
| --- | --- |
| `Name` | 对象名称，供标识或简短朗读。 |
| `Description` | 对象的简短说明。 |
| `Value` | 当前值的文本表示。 |
| `Help` | 更长的使用说明。 |
| `Accelerator` | 触发默认动作的键盘快捷键。 |
| `DebugDescription` | 调试用文本，不应用于普通用户播报。 |
| `Identifier` | 自 Qt 6.8，用于 UI 测试等稳定标识。 |
| `UserText` | 自定义文本类型起始值。 |

名称、描述和值不是可互换字段。比如滑块的可读标签应是 `Name`，当前位置通常是 `Value`。

### `RelationFlag` 与 `Relation`

`Relation` 是 `QFlags<RelationFlag>`，供 `QAccessibleInterface::relations()` 表示对象关系：

| 枚举值 | 方向语义 |
| --- | --- |
| `Label` / `Labelled` | 本对象是别人的标签 / 本对象被另一个对象标注。 |
| `Controller` / `Controlled` | 本对象控制别的对象 / 本对象被控制。 |
| `DescriptionFor` / `Described` | 本对象为别的对象提供描述 / 本对象被描述。 |
| `FlowsFrom` / `FlowsTo` | 阅读或导航顺序从别处流入 / 从本对象流向别处。 |
| `AllRelations` | 查询全部关系。 |

关系方向必须和实际返回对象匹配；不要为了“能被读到”随意建立双向关系。

### `InterfaceType`

`QAccessibleInterface::interface_cast()` 使用的能力类型：

| 枚举值 | 对应能力 |
| --- | --- |
| `TextInterface` | `QAccessibleTextInterface`。 |
| `EditableTextInterface` | `QAccessibleEditableTextInterface`。 |
| `ValueInterface` | `QAccessibleValueInterface`。 |
| `ActionInterface` | `QAccessibleActionInterface`。 |
| `ImageInterface` | `QAccessibleImageInterface`。 |
| `TableInterface` | `QAccessibleTableInterface`。 |
| `TableCellInterface` | `QAccessibleTableCellInterface`。 |
| `HyperlinkInterface` | `QAccessibleHyperlinkInterface`。 |
| `SelectionInterface` | 自 Qt 6.5 的 `QAccessibleSelectionInterface`。 |
| `AttributesInterface` | 自 Qt 6.8 的 `QAccessibleAttributesInterface`。 |

只有对象真实实现了该能力时才返回接口指针；调用方必须处理 `nullptr`。

### `TextBoundaryType`

文本接口按边界读取文本时使用：

| 枚举值 | 含义 |
| --- | --- |
| `CharBoundary` | 单个字符边界。 |
| `WordBoundary` | 单词边界。 |
| `SentenceBoundary` | 句子边界。 |
| `ParagraphBoundary` | 段落边界。 |
| `LineBoundary` | 换行边界。 |
| `NoBoundary` | 不按边界切分，使用整体文本。 |

边界算法会受语言、脚本和文本模型影响；位置仍是文档字符偏移，不是字节下标。

### `Attribute`

自 Qt 6.8 起，`QAccessibleAttributesInterface` 使用这些对象级 key，并要求 `QVariant` 值类型严格匹配：

| 键 | `QVariant` 内类型 | 语义 |
| --- | --- | --- |
| `Custom` | `QHash<QString, QString>` | 平台特定的自定义键值对；优先用更强类型的正式键。 |
| `Level` | `int` | 层级，例如 heading level。 |
| `Locale` | `QLocale` | 自 Qt 6.10，对象与应用默认 locale 不同时使用。 |
| `Orientation` | `Qt::Orientation` | 自 Qt 6.11，对象方向。 |

### `AnnouncementPoliteness`

自 Qt 6.8 起，`QAccessibleAnnouncementEvent` 使用：

| 枚举值 | 语义 |
| --- | --- |
| `Polite` | 正常优先级，等待合适时机播报。 |
| `Assertive` | 高优先级，可立即打断用户。 |

### `Event`

`Event` 描述发生了什么变化。构造通知时应选最精确的类型；需要额外数据的类型要使用对应派生 event。

| 分组 | 枚举值 |
| --- | --- |
| 传统 UI 活动 | `SoundPlayed`、`Alert`、`ForegroundChanged`、`MenuStart`、`MenuEnd`、`PopupMenuStart`、`PopupMenuEnd`、`ContextHelpStart`、`ContextHelpEnd`、`DragDropStart`、`DragDropEnd`、`DialogStart`、`DialogEnd`、`ScrollingStart`、`ScrollingEnd`、`MenuCommand` |
| 动作与文档 | `ActionChanged`、`ActiveDescendantChanged`、`AttributeChanged`、`DocumentContentChanged`、`DocumentLoadComplete`、`DocumentLoadStopped`、`DocumentReload`、`PageChanged`、`SectionChanged`、`VisibleDataChanged` |
| 超链接与富文本 | `HyperlinkEndIndexChanged`、`HyperlinkNumberOfAnchorsChanged`、`HyperlinkSelectedLinkChanged`、`HypertextLinkActivated`、`HypertextLinkSelected`、`HyperlinkStartIndexChanged`、`HypertextChanged`、`HypertextNLinksChanged`、`TextAttributeChanged`、`TextColumnChanged` |
| 表格 | `TableCaptionChanged`、`TableColumnDescriptionChanged`、`TableColumnHeaderChanged`、`TableModelChanged`、`TableRowDescriptionChanged`、`TableRowHeaderChanged`、`TableSummaryChanged` |
| 文本 payload | `TextCaretMoved`、`TextInserted`、`TextRemoved`、`TextUpdated`、`TextSelectionChanged`。 | 
| 对象生命周期与状态 | `ObjectCreated`、`ObjectDestroyed`、`ObjectShow`、`ObjectHide`、`ObjectReorder`、`Focus`、`Selection`、`SelectionAdd`、`SelectionRemove`、`SelectionWithin`、`StateChanged`、`LocationChanged`、`NameChanged`、`DescriptionChanged`、`ValueChanged`、`ParentChanged`、`HelpChanged`、`DefaultActionChanged`、`AcceleratorChanged`、`Announcement`、`IdentifierChanged`、`RoleChanged`、`InvalidEvent` |

事件数值映射含平台兼容历史，绝不能在持久化格式或业务协议中依赖整数值。

## 5. 静态 API 说明

### `void installFactory(InterfaceFactory factory)` / `void removeFactory(InterfaceFactory factory)`

安装或移除自定义 accessible interface 工厂。factory 的签名是：

```cpp
QAccessibleInterface *factory(const QString &key, QObject *object);
```

最近安装的 factory 最先被 `queryAccessibleInterface()` 调用。factory 应只在能处理对象时创建并返回 interface，否则返回 `nullptr` 让后续 factory/插件继续尝试。安装后工厂函数指针必须一直有效，移除时必须传入同一函数指针。

不要在 factory 中执行昂贵 IO、重复注册同一 interface，或返回由临时对象拥有的指针。

### `QAccessibleInterface *queryAccessibleInterface(QObject *object)`

查询对象的可访问接口，找不到时返回 `nullptr`。返回 interface 由 Qt 缓存管理，调用方不得删除。

`object` 应在调用过程中有效。该函数可在无障碍系统未 active 时使用；它用于读取和测试，不意味着会启用平台播报。

### `Id registerAccessibleInterface(QAccessibleInterface *iface)`

把手工创建的 interface 注册进缓存并返回 ID。每个 interface 只能注册一次。常规场景不要调用，`queryAccessibleInterface()` 已隐式完成注册。

注册后所有权交由缓存管理；失败、重复注册或 interface 生命周期处理不当都会造成悬垂指针或重复释放风险。

### `Id uniqueId(QAccessibleInterface *iface)`

返回 interface 当前的唯一缓存 ID。它不创建业务身份，也不保证脱离 cache 后仍有效。`iface` 必须是有效的可访问接口。

### `QAccessibleInterface *accessibleInterface(Id id)`

通过 cache ID 返回 interface；ID 无效时返回 `nullptr`。结果仍归 Qt 管理，不能删除或长期保存。

### `void deleteAccessibleInterface(Id id)`

从缓存移除并删除 ID 对应 interface。删除后 ID 失效且可能被复用。仅用于已按 Qt 规则手工注册、且应当销毁的 interface；不要删除由 Qt 默认工厂/插件生命周期管理的任意对象。

### `void updateAccessibility(QAccessibleEvent *event)`

把变化通知给可访问性后端。事件必须包含足够信息，且要在对象真实变化之后发送。没有监听工具时开销通常很小；若准备事件 payload 很昂贵，先检查 `isActive()`。

函数不取得 event 所有权，常规用法是在栈上创建事件并传地址。

### `bool isActive()`

当平台已经请求无障碍信息时返回 `true`。在屏幕阅读器等工具尚未访问框架前，它可以为 `false`。

它适合作为避免昂贵通知准备工作的优化，不应用来拒绝所有无障碍查询或改变控件本身的正确语义。

### `void setRootObject(QObject *object)`

设置应用可访问对象树的根，其他对象应能从根通过 navigation 到达。通常 Qt 会在 `QApplication::exec()` 进入事件循环前自动以 application 对象设置根，普通 QWidget 程序无需手动调用。

嵌入式、非典型对象树或自定义桥接时才考虑使用。root object 必须在无障碍系统使用期间有效。

## 6. 头文件公开的低层钩子

下面的 API 在 Qt 头文件中公开，但不属于普通 widget 应用的常规入口。除非正在编写平台桥接、测试后端或 Qt 集成层，否则不要安装它们：

| API | 用途与边界 |
| --- | --- |
| `installUpdateHandler(UpdateHandler)` | 替换/安装 accessibility 更新处理函数；返回旧 handler。handler 不拥有 event，必须遵守同步生命周期。 |
| `installRootObjectHandler(RootObjectHandler)` | 替换 root object 设置处理函数；返回旧 handler。 |
| `ActivationObserver` | 抽象观察者，覆写 `accessibilityActiveChanged(bool)` 接收 active 状态变化。 |
| `installActivationObserver(ActivationObserver *)` / `removeActivationObserver(...)` | 注册/移除非拥有观察者；观察者销毁前必须移除。 |
| `setActive(bool)` | 强制设置 active 状态，主要供平台后端或测试；普通应用不应伪造辅助技术活跃状态。 |
| `cleanup()` | 清理全局无障碍资源，通常由 Qt 关闭流程调用；运行中的应用不要随意调用。 |
| `qAccessibleTextBoundaryHelper(const QTextCursor &, TextBoundaryType)` | 根据 `QTextCursor` 求文本边界的低层 helper，返回起止位置 pair；普通 text interface 实现优先遵循自己的文本模型，不应把它当通用分词器。 |

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 语义类型 | `Role` | 描述对象语义角色。 | 选真实语义，不依赖枚举数值。 |
| 语义类型 | `State` | 描述当前状态位。 | 见独立 `State` 笔记；变化要发事件。 |
| 语义类型 | `Text` | 指定名称、说明、值等文本类别。 | 不混用 `Name`、`Description` 和 `Value`。 |
| 语义类型 | `RelationFlag` / `Relation` | 描述对象关系。 | 方向必须和实际对象关系一致。 |
| 语义类型 | `InterfaceType` | 查询可选能力接口。 | 未实现能力时处理 `nullptr`。 |
| 语义类型 | `TextBoundaryType` | 指定文本边界。 | 使用字符偏移，不是字节下标。 |
| 语义类型 | `Attribute` | 对象级属性键。 | QVariant 类型必须严格匹配键定义。 |
| 语义类型 | `AnnouncementPoliteness` | 控制播报优先级。 | `Assertive` 只用于紧急消息。 |
| 语义类型 | `Event` | 描述变化类型。 | 选择最精确类型，复杂 payload 用派生 event。 |
| 工厂 | `installFactory()` | 安装 interface factory。 | 后装先查；不支持时返回 `nullptr`。 |
| 工厂 | `removeFactory()` | 移除 factory。 | 传入同一函数指针。 |
| 查询 | `queryAccessibleInterface()` | 查询 QObject 的 interface。 | 返回值由 Qt 缓存管理，可能为 `nullptr`。 |
| 缓存 | `registerAccessibleInterface()` | 注册手工创建的 interface。 | 每个 interface 恰好一次；常规代码不需要。 |
| 缓存 | `uniqueId()` | 取得 interface 的临时 ID。 | 不是可持久化业务 ID。 |
| 缓存 | `accessibleInterface()` | 用 ID 查 interface。 | 无效 ID 返回 `nullptr`。 |
| 缓存 | `deleteAccessibleInterface()` | 删除已注册的 cache interface。 | ID 随后无效且可能被复用。 |
| 通知 | `updateAccessibility()` | 提交无障碍变化通知。 | 事件不转移所有权，变化后发送。 |
| 状态 | `isActive()` | 查询平台是否请求无障碍信息。 | 仅用于优化；不会禁止接口查询。 |
| 根 | `setRootObject()` | 设置可访问树根。 | 普通 Qt 应用通常无需调用。 |
| 低层 | `installUpdateHandler()` / `installRootObjectHandler()` | 替换后端回调。 | 平台集成/测试用途。 |
| 低层 | `ActivationObserver` 与 install/remove API | 观察 active 状态。 | 非拥有观察者，销毁前移除。 |
| 低层 | `setActive()`、`cleanup()`、`qAccessibleTextBoundaryHelper()` | 后端和内部辅助 API。 | 普通应用不应随意调用。 |

### 一句话总结

`QAccessible` 是 Qt 无障碍系统的协议与调度中心：日常代码用它查询 interface、在真实变化后发送精确事件；自定义控件通过 factory 和 `QAccessibleInterface` 接入；缓存 ID、后端 handler 与 active 状态则属于需要严格生命周期管理的低层能力。
