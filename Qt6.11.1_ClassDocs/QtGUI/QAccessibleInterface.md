# QAccessibleInterface

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是一个抽象接口或框架基类，重点是理解它定义的协议，并通过具体子类、工厂或回调来使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QAccessibleInterface` 是 Qt GUI 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAccessibleInterface>`
- 继承自：未在类页中列出
- 直接派生类：QAccessibleObject

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QAccessibleActionInterface * actionInterface()`
- `virtual QColor backgroundColor() const`
- `virtual QAccessibleInterface * child(int index) const = 0`
- `virtual QAccessibleInterface * childAt(int x, int y) const = 0`
- `virtual int childCount() const = 0`
- `virtual QAccessibleInterface * focusChild() const`
- `virtual QColor foregroundColor() const`
- `virtual int indexOfChild(const QAccessibleInterface *child) const = 0`
- `virtual void * interface_cast(QAccessible::InterfaceType type)`
- `virtual bool isValid() const = 0`
- `virtual QObject * object() const = 0`
- `virtual QAccessibleInterface * parent() const = 0`
- `virtual QRect rect() const = 0`
- `virtual QList<std::pair<QAccessibleInterface *, QAccessible::Relation>> relations(QAccessible::Relation match = QAccessible::AllRelations) const`
- `virtual QAccessible::Role role() const = 0`
- `(since 6.5) QAccessibleSelectionInterface * selectionInterface()`
- `virtual void setText(QAccessible::Text t, const QString &text) = 0`
- `virtual QAccessible::State state() const = 0`
- `QAccessibleTableCellInterface * tableCellInterface()`
- `QAccessibleTableInterface * tableInterface()`
- `virtual QString text(QAccessible::Text t) const = 0`
- `QAccessibleTextInterface * textInterface()`
- `QAccessibleValueInterface * valueInterface()`
- `virtual QWindow * window() const`

### 保护函数

- `virtual ~QAccessibleInterface()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[virtual noexcept protected] QAccessibleInterface::~QAccessibleInterface()`

**作用与语义：**

摧毁了`QAccessibleInterface`。

### `[virtual] QColor QAccessibleInterface::backgroundColor() const`

**作用与语义：**

如果适用，返回可访问者的背景色，或者返回无效`QColor`。

### `[pure virtual] QAccessibleInterface *QAccessibleInterface::child(int index) const`

**作用与语义：**

返回索引为`index`的可访问子节点。基于0的索引。对象的子节点数可以用`childCount`检查。
当请求无效子嗣时（例如子嗣在此期间变得无效时），返回`nullptr`。

### `[pure virtual] QAccessibleInterface *QAccessibleInterface::childAt(int x, int y) const`

**作用与语义：**

返回包含屏幕坐标（`x`，`y`）的子节点的子节点`QAccessibleInterface`。如果该位置没有子节点，该函数返回`nullptr`。返回的可访问对象必须是子节点，但不一定是直接子节点。
该函数仅对可见物体可靠（隐形物体可能布局不正确）。
所有视觉对象都能提供这些信息。
为继承`QAccessibleObject`的对象提供了默认实现。这将遍历所有子节点。如果控件管理其子节点（例如表），编写专用实现将更高效。

### `[pure virtual] int QAccessibleInterface::childCount() const`

**作用与语义：**

返回属于该对象的子节点数量。子节点可以单独提供可访问性信息（例如子控件），也可以作为该可访问对象的子元素。
所有对象都提供这些信息。

### `[virtual] QAccessibleInterface *QAccessibleInterface::focusChild() const`

**作用与语义：**

返回带有键盘焦点的对象。
返回的对象可以是任何后代，包括它自己。

### `[virtual] QColor QAccessibleInterface::foregroundColor() const`

**作用与语义：**

如果适用，返回可达的前景颜色，或者返回无效`QColor`。

### `[pure virtual] int QAccessibleInterface::indexOfChild(const QAccessibleInterface *child) const`

**作用与语义：**

返回该对象子列表中`child`的基于0的索引，如果`child`不是该对象的子节点，则返回-1。
所有物体都会提供关于其子女的信息。

### `[virtual] void *QAccessibleInterface::interface_cast(QAccessible::InterfaceType type)`

**作用与语义：**

返回一个`type`通用`QAccessibleInterface`的专用无障碍界面。
当通过专用接口提供关于控件或对象的更多信息时，必须重新实现该函数。例如，行编辑应实现`QAccessibleTextInterface`。

### `[pure virtual] bool QAccessibleInterface::isValid() const`

**作用与语义：**

如果使用该接口实现所需的所有数据都有效（例如所有指针非空），返回`true`;否则返回`false`。

### `[pure virtual] QObject *QAccessibleInterface::object() const`

**作用与语义：**

返回指向该接口实现所提供信息的`QObject`的指针。

### `[pure virtual] QAccessibleInterface *QAccessibleInterface::parent() const`

**作用与语义：**

返回可访问对象层级中父节点的 `QAccessibleInterface`。
如果没有父对象（例如顶层应用对象），返回`nullptr`。

### `[pure virtual] QRect QAccessibleInterface::rect() const`

**作用与语义：**

返回物体的几何形状。几何体以屏幕坐标表示。
该功能仅对可见物体可靠（隐形物体可能布局不正确）。
所有视觉对象都能提供这些信息。

### `[virtual] QList<std::pair<QAccessibleInterface *, QAccessible::Relation>> QAccessibleInterface::relations(QAccessible::Relation match = QAccessible::AllRelations) const`

**作用与语义：**

返回有意义的关系到其他控件。通常这不会返回父/子关系，除非它们以特定方式处理，比如树视图中。它通常会返回标签-by和label关系。
可以通过可选参数`match`来过滤关系。它不应返回自身。

### `[pure virtual] QAccessible::Role QAccessibleInterface::role() const`

**作用与语义：**

返回对象的角色。对象的角色通常是静态的。
所有可访问的对象都有其角色。

### `[since 6.5] QAccessibleSelectionInterface *QAccessibleInterface::selectionInterface()`

**作用与语义：**

取得当前可访问对象的选择专用接口。对象支持这项能力时返回相应接口指针，否则返回 `nullptr`；调用专用方法前必须判空，返回指针由可访问性对象管理，不要自行删除。

### `[pure virtual] void QAccessibleInterface::setText(QAccessible::Text t, const QString &text)`

**作用与语义：**

将对象`t`的文本属性设置为`text`。
注意，大多数对象的文本属性是只读的，因此调用该函数可能没有影响。

### `[pure virtual] QAccessible::State QAccessibleInterface::state() const`

**作用与语义：**

返回对象当前状态。返回的值是 QAccessible：：StateFlag 枚举中标志的组合。
所有可访问对象都有一个状态。

### `[pure virtual] QString QAccessibleInterface::text(QAccessible::Text t) const`

**作用与语义：**

返回对象文本属性`t`值。
`QAccessible::Name`是客户端用来识别、查找或向用户宣布可访问对象的字符串。所有对象必须在其容器内拥有唯一的名称。客户端的名称可能不同，因此名称应既能简短描述对象，又应当是唯一。
可访问物体的`QAccessible::Description`提供关于物体视觉外观的文本信息。该描述主要用于为视障用户提供更丰富的上下文，也用于上下文搜索或其他应用。并非所有物体都有描述。“确定”按钮不需要描述，但显示笑脸图片的工具按钮则需要。
可访问对象的 `QAccessible::Value` 表示对象中包含的视觉信息，例如行编辑中的文本。通常，用户可以修改该值。并非所有对象都有值，例如静态文本标签没有，有些对象的状态已经是该值，例如切换按钮。
`QAccessible::Help`文本提供了关于可访问对象功能和用途的信息。并非所有对象都提供这些信息。
`QAccessible::Accelerator`是激活对象默认动作的键盘快捷方式。键盘快捷键是菜单、菜单项或小部件文本中划线的字符，可以是字符本身，也可以是该字符与修饰键（如Alt、Ctrl或Shift）的组合。命令控件如工具按钮也有快捷键，通常会在提示中显示。
`QAccessible::Identifier`可以被显式设置为为辅助技术提供ID。这在UI测试中尤其有用。如果没有明确设置标识符，相应接口会根据`QObject::objectName`或其类名以及父链中父的`QObject::objectName`或类名，将标识符设置为ID。
所有对象都为`QAccessible::Name`提供字符串。

### `[virtual] QWindow *QAccessibleInterface::window() const`

**作用与语义：**

返回与底层对象关联的窗口。例如，`QAccessibleWidget` 重新实现了该窗口，返回了`QWidget`的 windowHandle()。
在某些平台上，它用于通知AT客户端状态变化。后端会遍历所有祖先，直到找到窗口。（这意味着祖先中至少有一个接口应返回有效的`QWindow`指针。）。
默认实现返回`nullptr`。

### `QAccessibleActionInterface * actionInterface()`

**作用与语义：**

取得当前可访问对象的动作专用接口。对象支持这项能力时返回相应接口指针，否则返回 `nullptr`；调用专用方法前必须判空，返回指针由可访问性对象管理，不要自行删除。

### `QAccessibleTableCellInterface * tableCellInterface()`

**作用与语义：**

取得当前可访问对象的表格单元格专用接口。对象支持这项能力时返回相应接口指针，否则返回 `nullptr`；调用专用方法前必须判空，返回指针由可访问性对象管理，不要自行删除。

### `QAccessibleTableInterface * tableInterface()`

**作用与语义：**

取得当前可访问对象的表格专用接口。对象支持这项能力时返回相应接口指针，否则返回 `nullptr`；调用专用方法前必须判空，返回指针由可访问性对象管理，不要自行删除。

### `QAccessibleTextInterface * textInterface()`

**作用与语义：**

取得当前可访问对象的文本专用接口。对象支持这项能力时返回相应接口指针，否则返回 `nullptr`；调用专用方法前必须判空，返回指针由可访问性对象管理，不要自行删除。

### `QAccessibleValueInterface * valueInterface()`

**作用与语义：**

取得当前可访问对象的数值专用接口。对象支持这项能力时返回相应接口指针，否则返回 `nullptr`；调用专用方法前必须判空，返回指针由可访问性对象管理，不要自行删除。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAccessibleInterface` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
