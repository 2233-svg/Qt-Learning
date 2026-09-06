# QAccessible

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QAccessible` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QAccessible>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `struct State`
- `(since 6.8) enum class AnnouncementPoliteness { Polite, Assertive }`
- `(since 6.8) enum class Attribute { Custom, Level, Locale, Orientation }`
- `enum Event { AcceleratorChanged, ActionChanged, ActiveDescendantChanged, Alert, Announcement, …, VisibleDataChanged }`
- `Id`
- `InterfaceFactory`
- `enum InterfaceType { TextInterface, ValueInterface, ActionInterface, TableInterface, TableCellInterface, …, AttributesInterface }`
- `flags Relation`
- `enum RelationFlag { Label, Labelled, Controller, Controlled, DescriptionFor, …, AllRelations }`
- `enum Role { AlertMessage, Animation, Application, Assistant, BlockQuote, …, Window }`
- `enum Text { Name, Description, Value, Help, Accelerator, …, Identifier }`
- `enum TextBoundaryType { CharBoundary, WordBoundary, SentenceBoundary, ParagraphBoundary, LineBoundary, NoBoundary }`

### 静态公有成员

- `QAccessibleInterface * accessibleInterface(QAccessible::Id id)`
- `void deleteAccessibleInterface(QAccessible::Id id)`
- `void installFactory(QAccessible::InterfaceFactory factory)`
- `bool isActive()`
- `QAccessibleInterface * queryAccessibleInterface(QObject *object)`
- `QAccessible::Id registerAccessibleInterface(QAccessibleInterface *iface)`
- `void removeFactory(QAccessible::InterfaceFactory factory)`
- `void setRootObject(QObject *object)`
- `QAccessible::Id uniqueId(QAccessibleInterface *iface)`
- `void updateAccessibility(QAccessibleEvent *event)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.8] enum class QAccessible::AnnouncementPoliteness`

**作用与语义：**

该枚举描述了`QAccessibleAnnouncementEvent`使用的公告优先级。
有了`QAccessible::AnouncementPoliteness::Polite`，辅助技术应在下一个优雅的时刻宣布消息，比如说完当前句子时或用户暂停打字时。礼貌的公告仍可能打断正在进行的礼貌公告。
在指定`QAccessible::AnouncementPoliteness::Assertive`时，辅助技术应立即通知用户。
由于中断可能会使用户迷失方向或无法完成当前任务，除非中断是必须的，否则不应使用`QAccessible::AnouncementPoliteness::Assertive`。
- `QAccessible::AnnouncementPoliteness::Polite`：`0`;公告具有正常优先级。
- `QAccessible::AnnouncementPoliteness::Assertive`：`1`;公告具有高优先级，应立即通知用户，即使这意味着中断用户当前的任务。
这个枚举是在Qt 6.8引入的。

### `[since 6.8] enum class QAccessible::Attribute`

**作用与语义：**

该枚举描述了`QAccessibleAttributesInterface`所使用的不同类型的属性。
这些属性类似于 ARIA、AT-SPI2、IAccessible、UIA 和 NSAccessibility 中存在的属性/（对象）属性概念，并在适用时映射到其平台对应版本。
每个属性作为键值对处理，该枚举的值作为键使用。
属性值以`QVariant`表示。`QVariant`中存储值的类型固定，并在下文为每种属性类型指定。
- `QAccessible::Attribute::Custom`：`0`;值类型：`QHash<QString`，`QString`>`Custom`属性的特殊之处在于它能有效表示多个属性，因为它本身是一个用于表示键值对的`QHash`。对于支持自定义属性键值对的平台，`Custom`属性中的属性会桥接到平台层，而不对平台特定属性进行转换。一般来说，应使用其他更强类型的属性。例如，该属性可用于原型制作，然后正式为特定功能添加新的枚举值。
- `QAccessible::Attribute::Level`：`1`;值类型：`int`定义结构中元素的层级，例如标题的标题层级。该属性在概念上与ARIA中的“咏叹调层级”属性相匹配。
- `QAccessible::Attribute::Locale (since Qt 6.10)`：`2`;值类型：`QLocale` 元素的所在地。这可以用来指定元素的所在地与应用程序默认的区域不同，例如文档中使用与应用界面语言不同的语言的段落。
- `QAccessible::Attribute::Orientation (since Qt 6.11)`：`3`;值类型：`Qt::Orientation` 元素的方向。该属性在概念上与 ARIA 中的“ARIA 方向”属性相符。
这个枚举是在Qt 6.8引入的。

### `enum QAccessible::Event`

**作用与语义：**

该枚举类型定义了可访问事件类型。
- `QAccessible::AcceleratorChanged`：`0x80C0`;操作的键盘加速器已更改。
- `QAccessible::ActionChanged`：`0x0101`;动作被更改。
- `QAccessible::ActiveDescendantChanged`：`0x0102`
- `QAccessible::Alert`：`0x0002`;系统警报（例如，来自`QMessageBox`的消息）
- `QAccessible::Announcement (since Qt 6.8)`：`0x80D0`;请求公告消息。
- `QAccessible::AttributeChanged`：`0x0103`
- `QAccessible::ContextHelpEnd`：`0x000D`;对象的上下文帮助（`QWhatsThis`）已完成。
- `QAccessible::ContextHelpStart`：`0x000C`;启动对象的上下文帮助（`QWhatsThis`）。
- `QAccessible::DefaultActionChanged`：`0x80B0`;可访问对象的默认QAccessible：：Action发生了变化。
- `QAccessible::DescriptionChanged`：`0x800D`;物体`QAccessible::Description`变了。
- `QAccessible::DialogEnd`：`0x0011`;一个对话（`QDialog`）被隐藏
- `QAccessible::DialogStart`：`0x0010`;对话框（`QDialog`）已设置为可见。
- `QAccessible::DocumentContentChanged`：`0x0104`;文本文档的内容发生了变化。
- `QAccessible::DocumentLoadComplete`：`0x0105`;文档已加载。
- `QAccessible::DocumentLoadStopped`：`0x0106`;文档加载已被停止。
- `QAccessible::DocumentReload`：`0x0107`;已启动文档加载。
- `QAccessible::DragDropEnd`：`0x000F`;拖拽操作即将完成。
- `QAccessible::DragDropStart`：`0x000E`;拖拽操作即将启动。
- `QAccessible::Focus`：`0x8005`;一个物体获得了键盘焦点。
- `QAccessible::ForegroundChanged`：`0x0003`;窗口已被激活（即桌面上有新窗口获得焦点）。
- `QAccessible::HelpChanged`：`0x80A0`;对象的`QAccessible::Help`文本属性发生了变化。
- `QAccessible::HyperlinkEndIndexChanged`：`0x0108`;超文本链接显示文本的末端位置发生了变化。
- `QAccessible::HyperlinkNumberOfAnchorsChanged`：`0x0109`;超文本链接中的锚点数量发生了变化，可能是因为显示文本被拆分以提供多个链接。
- `QAccessible::HyperlinkSelectedLinkChanged`：`0x010A`;所选超文本链接的链接已更改。
- `QAccessible::HyperlinkStartIndexChanged`：`0x010D`;超文本链接显示文本的起始位置发生了变化。
- `QAccessible::HypertextChanged`：`0x010E`;超文本链接的显示文本发生了变化。
- `QAccessible::HypertextLinkActivated`：`0x010B`;超文本链接已被激活，可能是通过点击或按键实现的。
- `QAccessible::HypertextLinkSelected`：`0x010C`;已选中超文本链接。
- `QAccessible::HypertextNLinksChanged`：`0x010F`
- `QAccessible::IdentifierChanged (since Qt 6.8)`：`0x80E0`;对象标识符发生变化。
- `QAccessible::LocationChanged`：`0x800B`;屏幕上物体的位置发生变化。
- `QAccessible::MenuCommand`：`0x0018`;菜单项被触发。
- `QAccessible::MenuEnd`：`0x0005`;菜单已被关闭（Qt 对所有菜单使用 PopupMenuEnd 表示）。
- `QAccessible::MenuStart`：`0x0004`;菜单栏已打开（Qt 使用所有菜单的 PopupMenuStart）。
- `QAccessible::NameChanged`：`0x800C`;对象的`QAccessible::Name`属性发生了变化。
- `QAccessible::ObjectAttributeChanged`：`0x0110`
- `QAccessible::ObjectCreated`：`0x8000`;创建一个新对象。
- `QAccessible::ObjectDestroyed`：`0x8001`;一个对象被删除。
- `QAccessible::ObjectHide`：`0x8003`;一个对象被隐藏;例如，带有`QWidget::hide()`。该对象的子节点不会发送该事件。当对象被其他对象遮挡时，不会发送该事件。
- `QAccessible::ObjectReorder`：`0x8004`;布局或项目视图添加了、移除或移动了对象（Qt 不使用此事件）。
- `QAccessible::ObjectShow`：`0x8002`;显示一个对象;例如，带有`QWidget::show()`。
- `QAccessible::PageChanged`：`0x0111`
- `QAccessible::ParentChanged`：`0x800F`;对象的父对象发生变化。
- `QAccessible::PopupMenuEnd`：`0x0007`;弹出菜单已关闭。
- `QAccessible::PopupMenuStart`：`0x0006`;弹出菜单已打开。
- `QAccessible::RoleChanged (since Qt 6.11)`：`0x80E1`;物体的角色发生了变化。
- `QAccessible::ScrollingEnd`：`0x0013`;滚动条滚动操作结束（鼠标松开滑块手柄）。
- `QAccessible::ScrollingStart`：`0x0012`;滚动条滚动操作即将开始;例如，鼠标按压滑块手柄可能导致。
- `QAccessible::SectionChanged`：`0x0112`
- `QAccessible::SelectionAdd`：`0x8007`;在项目视图中，已添加一个项目。
- `QAccessible::SelectionRemove`：`0x8008`;一个项目已从项目视图选择中移除。
- `QAccessible::Selection`：`0x8006`;菜单或物品视图中的选择发生了变化。
- `QAccessible::SelectionWithin`：`0x8009`;在项目视图中，选择发生了多次更改。
- `QAccessible::SoundPlayed`：`0x0001`;物体播放了声音
- `QAccessible::TableCaptionChanged`：`0x0113`;表格说明已更改。
- `QAccessible::TableColumnDescriptionChanged`：`0x0114`;表列的描述通常出现在列头中，已被更改。
- `QAccessible::TableColumnHeaderChanged`：`0x0115`;表列头已更改。
- `QAccessible::TableRowDescriptionChanged`：`0x0117`;通常出现在行头部的表行描述已被更改。
- `QAccessible::TableRowHeaderChanged`：`0x0118`;表行头部已更改。
- `QAccessible::TableSummaryChanged`：`0x0119`;表格的摘要已更改。
- `QAccessible::TextColumnChanged`：`0x011D`;文本列已更改。
- `QAccessible::VisibleDataChanged`：`0x0122`
该枚举的值定义与IAccessible2和MSAA规范中定义相同。

### `QAccessible::Id`

**作用与语义：**

未签名的同义词，`QAccessibleInterface`缓存使用。

### `QAccessible::InterfaceFactory`

**作用与语义：**

这是指向函数签名如下的指针的类型def：
函数接收一个`QString`和一个`QObject`指针，其中`QString`是识别接口的密钥。该`QObject`用于传递给`QAccessibleInterface`，使其能够保存对接口的引用。
如果密钥和`QObject`没有对应的`QAccessibleInterface`，则返回`nullptr`。
安装的工厂由 queryAccessibilityInterface() 调用，直到提供接口。

**官方示例：**

```cpp
 typedef QAccessibleInterface *myFactoryFunction(const QString &key, QObject *);
```

### `enum QAccessible::InterfaceType`

**作用与语义：**

`QAccessibleInterface`支持多个子接口。为了提供更多关于某些对象的信息，其可访问的表示应实现一个或多个此类接口。
注意：在子类化这些接口时，需要实现`QAccessibleInterface::interface_cast()`。
- `QAccessible::TextInterface`：`0`;适用于支持选择或多行的文本。简单标签无需实现此接口。
- `QAccessible::ValueInterface`：`2`;用于操作值的对象，例如滑块或滚动条。
- `QAccessible::ActionInterface`：`3`;用于允许用户触发动作的交互对象。基本上涵盖所有允许鼠标交互的功能。
- `QAccessible::TableInterface`：`5`;用于列表、表格和树。
- `QAccessible::TableCellInterface`：`6`;用于TableInterface对象中的单元格。
- `QAccessible::HyperlinkInterface`：`7`;对于超链接节点（通常嵌入为文本节点的子节点）
- `QAccessible::SelectionInterface (since Qt 6.5)`：`8`;用于支持子对象选择的非文本对象。
- `QAccessible::AttributesInterface (since Qt 6.8)`：`9`;用于支持对象特定属性的对象。

### `enum QAccessible::RelationFlagflags QAccessible::Relation`

**作用与语义：**

该枚举类型定义了可以组合的位标志，以表示两个可访问对象之间的关系。它被关系()函数使用，该函数返回调用对象的所有相关接口列表，以及每个对象的关系。
列表中的每个条目是一个 std：:p air `second`成员存储由`first`成员表示的`returned`对象与`origin`（调用者）接口/对象之间的关系类型。
在下表中，`returned`对象指的是返回列表中的对象，`origin`对象则是调用接口所代表的对象。
- `QAccessible::Label`：`0x00000001`;`returned`对象是`origin`对象的标签。
- `QAccessible::Labelled`：`0x00000002`;`returned`对象由`origin`对象标记。
- `QAccessible::Controller`：`0x00000004`;`returned`对象控制`origin`对象。
- `QAccessible::Controlled`：`0x00000008`;`returned`对象由`origin`对象控制。
- `QAccessible::DescriptionFor (since Qt 6.6)`：`0x00000010`;`returned`对象为`origin`对象提供描述。
- `QAccessible::Described (since Qt 6.6)`：`0x00000020`;`returned`对象由`origin`对象描述。
- `QAccessible::FlowsFrom (since Qt 6.6)`：`0x00000040`;内容逻辑上从`returned`对象流向`origin`对象。
- `QAccessible::FlowsTo (since Qt 6.6)`：`0x00000080`;内容逻辑上从`origin`对象流向`returned`对象。
- `QAccessible::AllRelations`：`0xffffffff`;用作掩码，表示我们对所有关系的信息感兴趣
关系()的实现返回这些标志的组合。有些值是互斥的。
关系类型是QFlag的typedef<RelationFlag>。它存储了RelationFlag值的或组合。

### `enum QAccessible::Role`

**作用与语义：**

这个枚举定义了可访问对象的角色。角色包括：
- `QAccessible::AlertMessage`：`0x00000008`;用于提醒用户的对象。
- `QAccessible::Animation`：`0x00000036`;显示动画的对象。
- `QAccessible::Application`：`0x0000000E`;应用程序的主窗口。
- `QAccessible::Assistant`：`0x00000020`;一个提供交互式帮助的对象。
- `QAccessible::BlockQuote (since Qt 6.9)`：`0x431`;一段引用自其他来源的内容。
- `QAccessible::Border`：`0x00000013`;表示边界的对象。
- `QAccessible::ButtonDropDown`：`0x00000038`;一个按钮，向下拉出一串物品。
- `QAccessible::ButtonDropGrid`：`0x0000003A`;一个下落网格的按钮。
- `QAccessible::ButtonMenu`：`0x00000039`;一个下拉菜单的按钮。
- `QAccessible::Canvas`：`0x00000035`;一个显示用户可交互图形的对象。
- `QAccessible::Caret`：`0x00000007`;表示系统中心（文本光标）的对象。
- `QAccessible::Cell`：`0x0000001D`;桌子上的一个单元格。
- `QAccessible::Chart`：`0x00000011`;一个显示数据图形表示的对象。
- `QAccessible::CheckBox`：`0x0000002C`;一个表示可被检查或取消勾选的选项的对象。有些选项提供“混合”状态，例如既未勾选也非未勾选。
- `QAccessible::Client`：`0x0000000A`;窗户中的客户区域。
- `QAccessible::Clock`：`0x0000003D`;一个显示时间的时钟。
- `QAccessible::ColorChooser`：`0x404`;一个允许用户选择颜色的对话框。
- `QAccessible::Column`：`0x0000001B`;一列单元格，通常位于表格内。
- `QAccessible::ColumnHeader`：`0x00000019`;数据列的头部。
- `QAccessible::ComboBox`：`0x0000002E`;用户可选择的选项列表。
- `QAccessible::ComplementaryContent`：`0x42C`;文档或网页中与主要内容互补的部分，通常是地标（参见WAI-ARIA）。
- `QAccessible::Cursor`：`0x00000006`;表示鼠标光标的对象。
- `QAccessible::Desktop`：`0x00000082`;该对象代表桌面或工作区。
- `QAccessible::Dial`：`0x00000031`;代表刻度盘或旋钮的物体。
- `QAccessible::Dialog`：`0x00000012`;一个对话框。
- `QAccessible::Document`：`0x0000000F`;例如办公应用中的文档。
- `QAccessible::EditableText`：`0x0000002A`;可编辑文本，如行或文本编辑。
- `QAccessible::Equation`：`0x00000037`;表示数学方程的对象。
- `QAccessible::Footer`：`0x40E`;页面中的页脚（通常见于文档中）。
- `QAccessible::Form`：`0x410`;包含控制功能的网页表单。
- `QAccessible::Graphic`：`0x00000028`;图形或图片，例如图标。
- `QAccessible::Grip`：`0x00000004`;用户可以拖动以改变控件大小的握把。
- `QAccessible::Grouping`：`0x00000014`;表示其他对象逻辑分组的对象。
- `QAccessible::Heading`：`0x414`;文档中的标题。
- `QAccessible::HelpBalloon`：`0x0000001F`;在一个独立且短暂的窗口中显示帮助的物体。
- `QAccessible::HotkeyField`：`0x00000032`;一个快捷键字段，允许用户输入按键序列。
- `QAccessible::Indicator`：`0x00000027`;表示当前值或项目的指示器。
- `QAccessible::LayeredPane`：`0x00000080`;一个可以包含分层子节点的对象，例如堆栈中。
- `QAccessible::Link`：`0x0000001E`;指向其他事物的链接。
- `QAccessible::List`：`0x00000021`;一个项目列表，用户可以从中选择一个或多个项目。
- `QAccessible::ListItem`：`0x00000022`;项目列表中的一项。
- `QAccessible::MenuBar`：`0x00000002`;用户可从菜单栏打开菜单。
- `QAccessible::MenuItem`：`0x0000000C`;菜单或菜单栏中的一项。
- `QAccessible::NoRole`：`0x00000000`;该对象没有角色。这通常表示对象无效。
- `QAccessible::Note`：`0x41B`;内容为括号内或附属于资源主内容的部分。
- `QAccessible::Notification`：`0x00000086`;表示通知的对象（例如系统托盘中的通知）。该角色仅对Linux有影响。
- `QAccessible::PageTab`：`0x00000025`;用户可以选择以切换到对话框中其他页面的页面标签。
- `QAccessible::PageTabList`：`0x0000003C`;页面标签列表。
- `QAccessible::Paragraph`：`0x00000083`;一段文本（通常见于文档中）。
- `QAccessible::Pane`：`0x00000010`;一种通用容器。
- `QAccessible::PopupMenu`：`0x0000000B`;一个菜单，列出用户可以选择执行动作的选项。
- `QAccessible::ProgressBar`：`0x00000030`;该对象显示正在进行的操作进度。
- `QAccessible::PropertyPage`：`0x00000026`;一个属性页面，用户可以在其中更改选项和设置。
- `QAccessible::Button`：`0x0000002B`;一个按钮。
- `QAccessible::RadioButton`：`0x0000002D`;表示与其他选项互斥的对象。
- `QAccessible::Row`：`0x0000001C`;一行单元格，通常位于表格内。
- `QAccessible::RowHeader`：`0x0000001A`;数据行的头部。
- `QAccessible::ScrollBar`：`0x00000003`;一个滚动条，允许用户滚动可见区域。
- `QAccessible::Section`：`0x00000085`;文档中的一个章节。
- `QAccessible::Separator`：`0x00000015`;一个将空间划分为逻辑区域的分隔符。
- `QAccessible::Slider`：`0x00000033`;一个滑块，允许用户在指定范围内选择一个值。
- `QAccessible::Sound`：`0x00000005`;表示声音的物体。
- `QAccessible::SpinBox`：`0x00000034`;一个旋转盒小部件，允许用户在给定范围内输入值。
- `QAccessible::Splitter`：`0x0000003E`;分配器，分配可用空间于其子组件之间。
- `QAccessible::StaticText`：`0x00000029`;静态文本，如其他控件的标签。
- `QAccessible::StatusBar`：`0x00000017`;状态条。
- `QAccessible::Switch (since Qt 6.11)`：`0x00000087`;一个可以开关的开关。
- `QAccessible::Table`：`0x00000018`;表示行列网格中数据的表。
- `QAccessible::Terminal`：`0x00000081`;终端或命令行接口。
- `QAccessible::TitleBar`：`0x00000001`;窗户标题条的标题。
- `QAccessible::ToolBar`：`0x00000016`;一个工具栏，用于将用户频繁访问的小部件分组。
- `QAccessible::ToolTip`：`0x0000000D`;提供其他对象信息的工具提示。
- `QAccessible::Tree`：`0x00000023`;树状结构中的项列表。
- `QAccessible::TreeItem`：`0x00000024`;树状结构中的一个项。
- `QAccessible::UserRole`：`0x0000ffff`;用于用户定义角色的第一个值。
- `QAccessible::WebDocument`：`0x00000084`;HTML 文档，通常在浏览器中。
- `QAccessible::Whitespace`：`0x0000003B`;其他物体之间的空白空间。
- `QAccessible::Window`：`0x00000009`;顶层窗口。

### `enum QAccessible::Text`

**作用与语义：**

该枚举指定可访问对象返回的字符串信息。
- `QAccessible::Name`：`0`;对象名称。这既可以作为标识符，也可以作为可访问客户端的简短描述。
- `QAccessible::Description`：`1`;描述该对象的简短文本。
- `QAccessible::Value`：`2`;物体的价值。
- `QAccessible::Help`：`3`;较长的文本，介绍如何使用该物体。
- `QAccessible::Accelerator`：`4`;执行对象默认动作的快捷键。
- `QAccessible::UserText`：`0x0000ffff`;第一个用于用户定义文本的值。
- `QAccessible::Identifier (since Qt 6.8)`：`6`;用于例如UI测试的对象标识符。

### `enum QAccessible::TextBoundaryType`

**作用与语义：**

该枚举描述了不同类型的文本边界。它遵循IAccessible2 API，并在`QAccessibleTextInterface`中使用。
- `QAccessible::CharBoundary`：`0`;使用单个字符作为边界。
- `QAccessible::WordBoundary`：`1`;用词语作为界限。
- `QAccessible::SentenceBoundary`：`2`;用句子作为边界。
- `QAccessible::ParagraphBoundary`：`3`;用段落作为边界。
- `QAccessible::LineBoundary`：`4`;使用换行作为边界。
- `QAccessible::NoBoundary`：`5`;无边界（请全文使用）。

### `[static] QAccessibleInterface *QAccessible::accessibleInterface(QAccessible::Id id)`

**作用与语义：**

归还属于`id`的`QAccessibleInterface`。
如果ID无效，返回会`nullptr`。

### `[static] void QAccessible::deleteAccessibleInterface(QAccessible::Id id)`

**作用与语义：**

将属于该`id`的接口从缓存中移除并删除。id将失效，且可被缓存重新使用。

### `[static] void QAccessible::installFactory(QAccessible::InterfaceFactory factory)`

**作用与语义：**

安装`InterfaceFactory` `factory`。最后添加的工厂是`queryAccessibleInterface()`使用的第一家。

### `[static] bool QAccessible::isActive()`

**作用与语义：**

如果平台请求无障碍信息，退货`true`。
该函数会返回false，直到屏幕阅读器等工具访问无障碍框架。即使无障碍未激活，仍可使用`QAccessible::queryAccessibleInterface()`。但不会向平台发送通知。
建议使用此功能以防止不必要的`updateAccessibility()`发送昂贵通知。

### `[static] QAccessibleInterface *QAccessible::queryAccessibleInterface(QObject *object)`

**作用与语义：**

如果给定`object`存在`QAccessibleInterface`实现，该函数返回指向该实现的指针;否则返回`nullptr`。
该函数调用所有已安装的工厂函数（从最近安装到最近安装的），直到找到一个为该类`object`提供接口的函数。如果没有工厂能为该类提供无障碍实现，函数会加载已安装的无障碍插件，并测试是否有插件能实现该插件。
如果没有该对象类的实现，函数尝试使用上述策略寻找对象父类的实现。
所有接口均由内部缓存管理，不应被删除。

### `[static] QAccessible::Id QAccessible::registerAccessibleInterface(QAccessibleInterface *iface)`

**作用与语义：**

调用此函数以确保手动创建的接口能够正确管理内存。每个接口 `iface` 只能恰好调用一次。调用 `queryAccessibleInterface` 时会隐式调用此函数，仅在使用 "new" 操作符实例化 QAccessibleInterfaces 时才需要调用此函数。不推荐这样做，尽可能使用默认函数，让 `queryAccessibleInterface()` 处理此事。当必须重新实现 `QAccessibleInterface::child()` 函数并在构建子对象后返回它时，需要调用此函数。

### `[static] void QAccessible::removeFactory(QAccessible::InterfaceFactory factory)`

**作用与语义：**

将`factory`从已安装的接口工厂列表中移除。

### `[static] void QAccessible::setRootObject(QObject *object)`

**作用与语义：**

将该应用可访问对象的根对象设置为`object`。所有其他可访问对象都可以通过根对象的对象导航访问。
通常不需要调用这个函数，因为 Qt 会在事件循环进入 `QApplication::exec()` 前立即将`QApplication`对象设置为根对象。
使用 QAccessible：：installRootObjectHandler() 将函数调用重定向到自定义的处理函数。

### `[static] QAccessible::Id QAccessible::uniqueId(QAccessibleInterface *iface)`

**作用与语义：**

返回`QAccessibleInterface` `iface`的唯一ID。

### `[static] void QAccessible::updateAccessibility(QAccessibleEvent *event)`

**作用与语义：**

通知可能对无障碍客户相关的变化。
`event`提供关于变更的详细信息。这些包括变更的来源和变更的属性。`event`应包含足够的信息，提供有意义的通知。
例如，类型`ValueChange`表示滑块的位置已被更改。
每当你的可访问对象或其子元素的状态被程序化（例如调用`QLabel::setText()`）或用户交互改变时，调用该函数。
如果没有无障碍工具监听该事件，调用该函数的性能损失较小，但如果确定调用参数成本高，可以测试`QAccessible::isActive()`以避免不必要的计算。

### `struct State`

**作用与语义：**

该结构定义了表示可访问对象状态的位标志。这些值如下：
- `active`：物体是容器中的活动窗口或活跃子元素（聚焦容器时会被聚焦）。
- `adjustable`：对象表示可调节值，例如滑块。
- `animated`：物体外观频繁变化。
- `busy`：物体此刻无法接受输入。
- `checkable`：该对象可检查。
- `checked`：勾选了该对象的复选框。
- `checkStateMixed`：第三状态复选框（三状态勾选半勾）。
- `collapsed`：对象被折叠，例如关闭的列表视图项或图标化的窗口。
- `defaultButton`：该对象代表对话中的默认按钮。
- `defunct`：该对象不再存在。
- `editable`：对象有文本卡勒特（通常实现文本接口）。
- `expandable`：该对象可展开，主要用于树状视图中的单元格。
- `expanded`：对象展开，当前其子节点可见。
- `extSelectable`：该对象支持扩展选择。
- `focusable`：物体可以接收焦点。只有处于活动窗口内的物体才能接收焦点。
- `focused`：该物体具有键盘焦点。
- `hasPopup`：该对象打开弹窗。
- `hotTracked`：物体的外观对鼠标光标位置敏感。
- `invalid`：该对象不再有效（因为它已被删除）。
- `invisible`：该对象对用户不可见。
- `linked`：对象与另一个对象（例如超链接）相关联。
- `marqueed`：该对象显示滚动内容，例如日志视图。
- `modal`：对象阻挡来自其他对象的输入。
- `movable`：物体可以移动。
- `multiLine`：对象有多行文本（换行），而不是单行。
- `multiSelectable`：该对象支持多个选中的项目。
- `offscreen`：物体被可见区域裁剪。屏幕外的物体也为隐形。
- `passwordEdit`：对象是一个密码字段，例如用于输入密码的行编辑。
- `playsSound`：物体与之互动时会发出声音。
- `pressed`：物体被压制。
- `readOnly`：对象通常可以编辑，但明确设置为只读。
- `searchEdit`：对象是搜索查询的输入，作为行编辑。
- `selectable`：对象可选择。
- `selectableText`：对象有文本，可以选择。这与可选择不同，可选择对象指的是对象的子节点。
- `selected`：选择对象，这与文本选择无关。
- `selfVoicing`：物体通过语音或声音描述自己。
- `sizeable`：对象可以调整大小，例如顶层窗口。
- `summaryElement`：对象总结窗口状态，应优先处理。
- `supportsAutoCompletion`：该对象具有自动补全功能，例如在行编辑或组合框中。
- `traversed`：物体被链接并被访问过。
- `updatesFrequently`：对象频繁变化，访问时需要刷新。
- `disabled`：该对象对用户不可用，例如禁用的控件。
`QAccessibleInterface::state()`的实现会返回这些标志的组合。

### `Id`

**作用与语义：**

未签名的同义词，`QAccessibleInterface`缓存使用。

### `InterfaceFactory`

**作用与语义：**

这是指向函数签名如下的指针的类型def：
函数接收一个`QString`和一个`QObject`指针，其中`QString`是识别接口的密钥。该`QObject`用于传递给`QAccessibleInterface`，使其能够保存对接口的引用。
如果密钥和`QObject`没有对应的`QAccessibleInterface`，则返回`nullptr`。
安装的工厂由 queryAccessibilityInterface() 调用，直到提供接口。

**官方示例：**

```cpp
 typedef QAccessibleInterface *myFactoryFunction(const QString &key, QObject *);
```

### `flags Relation`

**作用与语义：**

该枚举类型定义了可以组合的位标志，以表示两个可访问对象之间的关系。它被关系()函数使用，该函数返回调用对象的所有相关接口列表，以及每个对象的关系。
列表中的每个条目是一个 std：:p air `second`成员存储由`first`成员表示的`returned`对象与`origin`（调用者）接口/对象之间的关系类型。
在下表中，`returned`对象指的是返回列表中的对象，`origin`对象则是调用接口所代表的对象。
- `QAccessible::Label`：`0x00000001`;`returned`对象是`origin`对象的标签。
- `QAccessible::Labelled`：`0x00000002`;`returned`对象由`origin`对象标记。
- `QAccessible::Controller`：`0x00000004`;`returned`对象控制`origin`对象。
- `QAccessible::Controlled`：`0x00000008`;`returned`对象由`origin`对象控制。
- `QAccessible::DescriptionFor (since Qt 6.6)`：`0x00000010`;`returned`对象为`origin`对象提供描述。
- `QAccessible::Described (since Qt 6.6)`：`0x00000020`;`returned`对象由`origin`对象描述。
- `QAccessible::FlowsFrom (since Qt 6.6)`：`0x00000040`;内容逻辑上从`returned`对象流向`origin`对象。
- `QAccessible::FlowsTo (since Qt 6.6)`：`0x00000080`;内容逻辑上从`origin`对象流向`returned`对象。
- `QAccessible::AllRelations`：`0xffffffff`;用作掩码，表示我们对所有关系的信息感兴趣
关系()的实现返回这些标志的组合。有些值是互斥的。
关系类型是QFlag的typedef<RelationFlag>。它存储了RelationFlag值的或组合。

### `enum RelationFlag { Label, Labelled, Controller, Controlled, DescriptionFor, …, AllRelations }`

**作用与语义：**

该枚举类型定义了可以组合的位标志，以表示两个可访问对象之间的关系。它被关系()函数使用，该函数返回调用对象的所有相关接口列表，以及每个对象的关系。
列表中的每个条目是一个 std：:p air `second`成员存储由`first`成员表示的`returned`对象与`origin`（调用者）接口/对象之间的关系类型。
在下表中，`returned`对象指的是返回列表中的对象，`origin`对象则是调用接口所代表的对象。
- `QAccessible::Label`：`0x00000001`;`returned`对象是`origin`对象的标签。
- `QAccessible::Labelled`：`0x00000002`;`returned`对象由`origin`对象标记。
- `QAccessible::Controller`：`0x00000004`;`returned`对象控制`origin`对象。
- `QAccessible::Controlled`：`0x00000008`;`returned`对象由`origin`对象控制。
- `QAccessible::DescriptionFor (since Qt 6.6)`：`0x00000010`;`returned`对象为`origin`对象提供描述。
- `QAccessible::Described (since Qt 6.6)`：`0x00000020`;`returned`对象由`origin`对象描述。
- `QAccessible::FlowsFrom (since Qt 6.6)`：`0x00000040`;内容逻辑上从`returned`对象流向`origin`对象。
- `QAccessible::FlowsTo (since Qt 6.6)`：`0x00000080`;内容逻辑上从`origin`对象流向`returned`对象。
- `QAccessible::AllRelations`：`0xffffffff`;用作掩码，表示我们对所有关系的信息感兴趣
关系()的实现返回这些标志的组合。有些值是互斥的。
关系类型是QFlag的typedef<RelationFlag>。它存储了RelationFlag值的或组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAccessible` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
