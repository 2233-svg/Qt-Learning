# QDataWidgetMapper

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QDataWidgetMapper` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QDataWidgetMapper` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QDataWidgetMapper>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum SubmitPolicy { AutoSubmit, ManualSubmit }`

### 属性

- `currentIndex : int`
- `orientation : Qt::Orientation`
- `submitPolicy : SubmitPolicy`

### 公有函数

- `QDataWidgetMapper(QObject *parent = nullptr)`
- `virtual ~QDataWidgetMapper()`
- `void addMapping(QWidget *widget, int section)`
- `void addMapping(QWidget *widget, int section, const QByteArray &propertyName)`
- `void clearMapping()`
- `int currentIndex() const`
- `QAbstractItemDelegate * itemDelegate() const`
- `QByteArray mappedPropertyName(QWidget *widget) const`
- `int mappedSection(QWidget *widget) const`
- `QWidget * mappedWidgetAt(int section) const`
- `QAbstractItemModel * model() const`
- `Qt::Orientation orientation() const`
- `void removeMapping(QWidget *widget)`
- `QModelIndex rootIndex() const`
- `void setItemDelegate(QAbstractItemDelegate *delegate)`
- `void setModel(QAbstractItemModel *model)`
- `void setOrientation(Qt::Orientation aOrientation)`
- `void setRootIndex(const QModelIndex &index)`
- `void setSubmitPolicy(QDataWidgetMapper::SubmitPolicy policy)`
- `QDataWidgetMapper::SubmitPolicy submitPolicy() const`

### 公有槽函数

- `void revert()`
- `virtual void setCurrentIndex(int index)`
- `void setCurrentModelIndex(const QModelIndex &index)`
- `bool submit()`
- `void toFirst()`
- `void toLast()`
- `void toNext()`
- `void toPrevious()`

### 信号

- `void currentIndexChanged(int index)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDataWidgetMapper::SubmitPolicy`

**作用与语义：**

本枚举描述了`QDataWidgetMapper`支持的可能提交政策。
- `QDataWidgetMapper::AutoSubmit`：`0`;每当小部件失去焦点时，该小部件的当前值会被设置为物品模型。
- `QDataWidgetMapper::ManualSubmit`：`1`;模型在调用`submit()`之前不会更新。

### `currentIndex : int`

**作用与语义：**

该属性表示当前的行或列。
如果方向是水平的（默认），控件会填充`index`行的数据，否则则填充`index`列的数据。

**如何使用：** 调用 `currentIndex()` 读取当前值；它不会修改应用状态。

### `orientation : Qt::Orientation`

**作用与语义：**

此属性保存模型的方向。
如果方向为 `Qt::Horizontal`（默认值），则小部件将映射到数据模型的一列。小部件将填充来自其映射列以及 `currentIndex()` 指向的行的数据。
对于如下表格数据，使用 `Qt::Horizontal`：
- `1`: Qt 挪威; 奥斯陆
- `2`: Qt 澳大利亚; 布里斯班
- `3`: Qt 美国; 硅谷
- `4`: Qt 中国; 北京
- `5`: Qt 德国; 柏林
如果方向设置为 `Qt::Vertical`，则小部件将映射到一行。调用 `setCurrentIndex()` 将更改当前列。小部件将填充来自其映射行以及 `currentIndex()` 指向的列的数据。
对于如下表格数据，使用 `Qt::Vertical`：
- `1`: 2; 3; 4; 5
- `Qt Norway`: Qt 澳大利亚; Qt 美国; Qt 中国; Qt 德国
- `Oslo`: 布里斯班; 硅谷; 北京; 柏林
更改方向将清除所有现有映射。

**如何使用：** 调用 `orientation()` 读取当前值；它不会修改应用状态。

### `submitPolicy : SubmitPolicy`

**作用与语义：**

该房产实行当前提交政策。
更改当前提交策略会将所有小部件恢复为模型当前数据。

**如何使用：** 调用 `submitPolicy()` 读取当前值；它不会修改应用状态。

### `[explicit] QDataWidgetMapper::QDataWidgetMapper(QObject *parent = nullptr)`

**作用与语义：**

构建一个新的QDataWidgetMapper，父对象为`parent`。默认方向为水平，提交策略为`AutoSubmit`。

### `[virtual noexcept] QDataWidgetMapper::~QDataWidgetMapper()`

**作用与语义：**

摧毁了该物体。

### `void QDataWidgetMapper::addMapping(QWidget *widget, int section)`

**作用与语义：**

在模型中添加`widget`与`section`之间的映射。如果方向是水平的（默认），`section`是模型中的一列，否则是行。
以下例子中，假设模型`myModel`有两列：第一列包含群体中人员的名字，第二列包含他们的年龄。第一列映射到`QLineEdit` `nameLineEdit`，第二列映射到`QSpinBox` `ageSpinBox`：
注释：
- 如果`widget`已经映射到截面，旧映射将被新的映射替换。
- 仅允许部分和小部件之间的一一对应映射。无法将单个小部件映射到多个小部件，也无法将单个小部件映射到多个小部件。

**官方示例：**

```cpp
 QDataWidgetMapper *mapper = new QDataWidgetMapper;
 mapper->setModel(myModel);
 mapper->addMapping(nameLineEdit, 0);
 mapper->addMapping(ageSpinBox, 1);
```

### `void QDataWidgetMapper::addMapping(QWidget *widget, int section, const QByteArray &propertyName)`

**作用与语义：**

本质上与 addMapping() 相同，但增加了指定属性并指定 `propertyName` 的可能性。

### `void QDataWidgetMapper::clearMapping()`

**作用与语义：**

清除所有映射。

### `[signal] void QDataWidgetMapper::currentIndexChanged(int index)`

**作用与语义：**

该属性表示当前的行或列。
如果方向是水平的（默认），控件会填充`index`行的数据，否则则填充`index`列的数据。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `currentIndex` 的变化，不要把它当作普通函数主动调用。

### `QAbstractItemDelegate *QDataWidgetMapper::itemDelegate() const`

**作用与语义：**

返回当前的项目委托。

### `QByteArray QDataWidgetMapper::mappedPropertyName(QWidget *widget) const`

**作用与语义：**

返回将数据映射到给定`widget`时所使用的属性名称。

### `int QDataWidgetMapper::mappedSection(QWidget *widget) const`

**作用与语义：**

返回`widget`映射到的部分，如果控件未映射，则返回-1。

### `QWidget *QDataWidgetMapper::mappedWidgetAt(int section) const`

**作用与语义：**

返回映射在`section`的控件，如果该部分没有映射控件，则返回0。

### `QAbstractItemModel *QDataWidgetMapper::model() const`

**作用与语义：**

返回当前型号。

### `void QDataWidgetMapper::removeMapping(QWidget *widget)`

**作用与语义：**

移除给定`widget`的映射。

### `[slot] void QDataWidgetMapper::revert()`

**作用与语义：**

将模型当前数据重新填充所有小部件。所有未提交的更改将丢失。

### `QModelIndex QDataWidgetMapper::rootIndex() const`

**作用与语义：**

返回当前的根索引。

### `[slot] void QDataWidgetMapper::setCurrentModelIndex(const QModelIndex &index)`

**作用与语义：**

如果方向是水平的（默认），则将当前索引设置为`index`的行，否则设置为`index`的列。
调用`setCurrentIndex()`内部。该便利槽可连接至信号`currentRowChanged()`或`currentColumnChanged()`视角选择模型。
以下示例说明了当`QTableView`选择变更时，如何用新数据更新所有小部件`myTableView`：

**官方示例：**

```cpp
 QDataWidgetMapper *mapper = new QDataWidgetMapper;
 connect(myTableView->selectionModel(), &QItemSelectionModel::currentRowChanged,
         mapper, &QDataWidgetMapper::setCurrentModelIndex);
```

### `void QDataWidgetMapper::setItemDelegate(QAbstractItemDelegate *delegate)`

**作用与语义：**

将项目代理设置为`delegate`。代理将用于将模型的数据写入控件，再从控件写入模型，使用`QAbstractItemDelegate::setEditorData()`和`QAbstractItemDelegate::setModelData()`。
任何现有代表都会被移除，但不会被删除。`QDataWidgetMapper`不对`delegate`拥有所有权。
代理还通过`QAbstractItemDelegate::commitData()`和`QAbstractItemDelegate::closeEditor()`决定何时应用数据和何时更改编辑器。
警告：你不应在小部件映射器或视图之间共享同一个代理实例。这样做可能导致错误或不直观的编辑行为，因为连接到某个代理的每个视图都可能收到`closeEditor()`信号，并试图访问、修改或关闭已被关闭的编辑器。

### `void QDataWidgetMapper::setModel(QAbstractItemModel *model)`

**作用与语义：**

将当前模型设置为`model`。如果设置了另一个模型，所有映射到该旧模型的映射都会被清除。

### `void QDataWidgetMapper::setRootIndex(const QModelIndex &index)`

**作用与语义：**

将根项设置为`index`。这可以用来显示树的分支。传递一个无效的模型索引以显示最顶端的分支。

### `[slot] bool QDataWidgetMapper::submit()`

**作用与语义：**

将映射控件的所有更改提交到模型。
对于每个映射的部分，项目代理读取小部件的当前值并将其设置到模型中。最后，调用模型的`submit()`方法。
如果所有值都提交，返回`true`，否则为假。
注意：对于数据库模型，`QSqlQueryModel::lastError()` 可用于检索最后的错误。

### `[slot] void QDataWidgetMapper::toFirst()`

**作用与语义：**

如果模型的朝向是水平的（默认），则用模型第一行的数据填充小部件，否则则用第一列的数据填充。
这相当于称呼`setCurrentIndex(0)`。

### `[slot] void QDataWidgetMapper::toLast()`

**作用与语义：**

如果模型的朝向是水平的（默认），则用模型最后一行的数据填充小部件，否则则用最后一列的数据填充。
电话`setCurrentIndex()`内部。

### `[slot] void QDataWidgetMapper::toNext()`

**作用与语义：**

如果模型的朝向是水平的（默认），则用模型下一行的数据填充小部件，否则则用下一列的数据填充。
调用内部`setCurrentIndex()`。如果模型中没有下一行，则无动于衷。

### `[slot] void QDataWidgetMapper::toPrevious()`

**作用与语义：**

如果模型的方向是水平的（默认），则用模型前一行的数据填充小部件，否则则用上一列的数据填充。
调用`setCurrentIndex()`内部调用。如果模型中没有前一行，它就没有任何作用。

### `int currentIndex() const`

**作用与语义：**

该属性表示当前的行或列。
如果方向是水平的（默认），控件会填充`index`行的数据，否则则填充`index`列的数据。

**如何使用：** 调用 `currentIndex()` 读取当前值；它不会修改应用状态。

### `Qt::Orientation orientation() const`

**作用与语义：**

此属性保存模型的方向。
如果方向为 `Qt::Horizontal`（默认值），则小部件将映射到数据模型的一列。小部件将填充来自其映射列以及 `currentIndex()` 指向的行的数据。
对于如下表格数据，使用 `Qt::Horizontal`：
- `1`: Qt 挪威; 奥斯陆
- `2`: Qt 澳大利亚; 布里斯班
- `3`: Qt 美国; 硅谷
- `4`: Qt 中国; 北京
- `5`: Qt 德国; 柏林
如果方向设置为 `Qt::Vertical`，则小部件将映射到一行。调用 `setCurrentIndex()` 将更改当前列。小部件将填充来自其映射行以及 `currentIndex()` 指向的列的数据。
对于如下表格数据，使用 `Qt::Vertical`：
- `1`: 2; 3; 4; 5
- `Qt Norway`: Qt 澳大利亚; Qt 美国; Qt 中国; Qt 德国
- `Oslo`: 布里斯班; 硅谷; 北京; 柏林
更改方向将清除所有现有映射。

**如何使用：** 调用 `orientation()` 读取当前值；它不会修改应用状态。

### `void setOrientation(Qt::Orientation aOrientation)`

**作用与语义：**

此属性保存模型的方向。
如果方向为 `Qt::Horizontal`（默认值），则小部件将映射到数据模型的一列。小部件将填充来自其映射列以及 `currentIndex()` 指向的行的数据。
对于如下表格数据，使用 `Qt::Horizontal`：
- `1`: Qt 挪威; 奥斯陆
- `2`: Qt 澳大利亚; 布里斯班
- `3`: Qt 美国; 硅谷
- `4`: Qt 中国; 北京
- `5`: Qt 德国; 柏林
如果方向设置为 `Qt::Vertical`，则小部件将映射到一行。调用 `setCurrentIndex()` 将更改当前列。小部件将填充来自其映射行以及 `currentIndex()` 指向的列的数据。
对于如下表格数据，使用 `Qt::Vertical`：
- `1`: 2; 3; 4; 5
- `Qt Norway`: Qt 澳大利亚; Qt 美国; Qt 中国; Qt 德国
- `Oslo`: 布里斯班; 硅谷; 北京; 柏林
更改方向将清除所有现有映射。

**如何使用：** 调用 `setOrientation(...)` 修改 `orientation`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSubmitPolicy(QDataWidgetMapper::SubmitPolicy policy)`

**作用与语义：**

该房产实行当前提交政策。
更改当前提交策略会将所有小部件恢复为模型当前数据。

**如何使用：** 调用 `setSubmitPolicy(...)` 修改 `submitPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QDataWidgetMapper::SubmitPolicy submitPolicy() const`

**作用与语义：**

该房产实行当前提交政策。
更改当前提交策略会将所有小部件恢复为模型当前数据。

**如何使用：** 调用 `submitPolicy()` 读取当前值；它不会修改应用状态。

### `virtual void setCurrentIndex(int index)`

**作用与语义：**

该属性表示当前的行或列。
如果方向是水平的（默认），控件会填充`index`行的数据，否则则填充`index`列的数据。

**如何使用：** 调用 `setCurrentIndex(...)` 修改 `currentIndex`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QDataWidgetMapper` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
