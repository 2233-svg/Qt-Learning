# QWizardPage

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QWizardPage` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QWizardPage` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QWizardPage>`
- 继承自：QWidget
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

### 属性

- `subTitle : QString`
- `title : QString`

### 公有函数

- `QWizardPage(QWidget *parent = nullptr)`
- `virtual ~QWizardPage()`
- `QString buttonText(QWizard::WizardButton which) const`
- `virtual void cleanupPage()`
- `virtual void initializePage()`
- `bool isCommitPage() const`
- `virtual bool isComplete() const`
- `bool isFinalPage() const`
- `virtual int nextId() const`
- `QPixmap pixmap(QWizard::WizardPixmap which) const`
- `void setButtonText(QWizard::WizardButton which, const QString &text)`
- `void setCommitPage(bool commitPage)`
- `void setFinalPage(bool finalPage)`
- `void setPixmap(QWizard::WizardPixmap which, const QPixmap &pixmap)`
- `void setSubTitle(const QString &subTitle)`
- `void setTitle(const QString &title)`
- `QString subTitle() const`
- `QString title() const`
- `virtual bool validatePage()`

### 信号

- `void completeChanged()`

### 保护函数

- `QVariant field(const QString &name) const`
- `void registerField(const QString &name, QWidget *widget, const char *property = nullptr, const char *changedSignal = nullptr)`
- `void setField(const QString &name, const QVariant &value)`
- `QWizard * wizard() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `subTitle : QString`

**作用与语义：**

该属性包含了该页面的副标题。
字幕通过`QWizard`显示，位于标题和实际页面之间。字幕为可选。在`ClassicStyle`和`ModernStyle`中，使用字幕是让标题显示的必要条件。在 `MacStyle` 中，字幕以文本标签的形式显示在实际页面上方。
副标题可以是纯文本，也可以是HTML，具体取决于`QWizard::subTitleFormat`属性的值。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `subTitle()` 读取当前值；它不会修改应用状态。

### `title : QString`

**作用与语义：**

该属性包含了页面的标题。
标题通过`QWizard`显示，位于实际页面上方。所有页面都应有标题。
标题可以是纯文本，也可以是HTML格式，具体取决于`QWizard::titleFormat`属性的价值。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `title()` 读取当前值；它不会修改应用状态。

### `[explicit] QWizardPage::QWizardPage(QWidget *parent = nullptr)`

**作用与语义：**

用给定的`parent`构建一个向导页面。
当页面通过`QWizard::addPage()`或`QWizard::setPage()`插入向导时，父页面会自动被设置为向导。

### `[virtual noexcept] QWizardPage::~QWizardPage()`

**作用与语义：**

毁灭者。

### `QString QWizardPage::buttonText(QWizard::WizardButton which) const`

**作用与语义：**

返回本页按钮`which`的文字。
如果文本使用 `setButtonText()` 设置了 ben，则返回该文本。否则，如果文本使用 `QWizard::setButtonText()` 设置，则返回该文本。
默认情况下，按钮上的文字取决于`QWizard::wizardStyle`。例如，在macOS上，“下一个”按钮叫做“继续”。

### `[virtual] void QWizardPage::cleanupPage()`

**作用与语义：**

当用户通过点击返回离开页面时（除非设置了`QWizard::IndependentPages`选项），`QWizard::cleanupPage()`会调用这个虚拟功能。
默认实现会将页面字段重置为其原始值（即调用`initializePage()`之前的值）。

### `[signal] void QWizardPage::completeChanged()`

**作用与语义：**

每当页面的完整状态（即`isComplete()`值）发生变化时，该信号就会发出。
如果你重新实现`isComplete()`，确保每当 `isComplete()` 值发生变化时，都发出 completeChanged() `QWizard`，以确保  更新其按钮的启用或禁用状态。

### `[protected] QVariant QWizardPage::field(const QString &name) const`

**作用与语义：**

返回称为 `name` 的字段值。该函数可用于访问向导任一页面的字段。它等价于调用 `wizard()`->field（`name`）。

**官方示例：**

```cpp
         const QString emailAddress = field("details.email").toString();
         licenseText = tr("<u>First-Time License Agreement:</u> "
                          "You can use this software subject to the license "
                          "you will receive by email sent to %1.").arg(emailAddress);
```

### `[virtual] void QWizardPage::initializePage()`

**作用与语义：**

`QWizard::initializePage()`调用该虚拟函数，在页面显示前准备页面，无论是因`QWizard::restart()`被调用，还是用户点击“Next”。（但如果设置了`QWizard::IndependentPages`选项，该函数仅在页面首次显示时调用。）。
通过重新实现该函数，你可以确保页面的字段基于之前页面的字段正确初始化。例如：
默认实现什么都不做。

**官方示例：**

```cpp
 void ConclusionPage::initializePage()
 {
     QString licenseText;

     if (wizard()->hasVisitedPage(LicenseWizard::Page_Evaluate)) {
         licenseText = tr("<u>Evaluation License Agreement:</u> "
                          "You can use this software for 30 days and make one "
                          "backup, but you are not allowed to distribute it.");
     } else if (wizard()->hasVisitedPage(LicenseWizard::Page_Details)) {
         const QString emailAddress = field("details.email").toString();
         licenseText = tr("<u>First-Time License Agreement:</u> "
                          "You can use this software subject to the license "
                          "you will receive by email sent to %1.").arg(emailAddress);
     } else {
         licenseText = tr("<u>Upgrade License Agreement:</u> "
                          "This software is licensed under the terms of your "
                          "current license.");
     }
     bottomLabel->setText(licenseText);
 }
```

### `bool QWizardPage::isCommitPage() const`

**作用与语义：**

如果该页面是提交页面，返回`true`;否则返回`false`。

### `[virtual] bool QWizardPage::isComplete() const`

**作用与语义：**

`QWizard`调用该虚拟功能来决定下一步或完成按钮应启用或禁用。
默认实现返回`true`，如果所有必填字段均已填满;否则返回`false`。
如果你重构该函数，确保每当isComplete()值变化时，从实现的其他部分发出`completeChanged()`。这确保`QWizard`更新按钮的启用或禁用状态。重实现的示例可见此处。

### `bool QWizardPage::isFinalPage() const`

**作用与语义：**

`QWizard`调用该函数来判断该页面是否应该显示完成按钮。
默认情况下，如果没有下一页（即返回`nextId()`返回-1），则返回`true`;否则返回`false`。
通过明确调用 `setFinalPage`（true），用户可以执行“提前完成”。

### `[virtual] int QWizardPage::nextId() const`

**作用与语义：**

`QWizard::nextId()`调用该虚拟功能，以确定用户点击“下一步”按钮时应显示的页面。
返回值为下一页的ID，若无页面后进则为-1。
默认情况下，该函数返回大于当前页面ID的最低ID，如果没有该ID则返回-1。
通过重新实现该函数，你可以指定动态页面顺序。例如：

**官方示例：**

```cpp
 int IntroPage::nextId() const
 {
     if (evaluateRadioButton->isChecked()) {
         return LicenseWizard::Page_Evaluate;
     } else {
         return LicenseWizard::Page_Register;
     }
 }
```

### `QPixmap QWizardPage::pixmap(QWizard::WizardPixmap which) const`

**作用与语义：**

返回角色`which`的像素映射集。
像素映射也可以用`QWizard::setPixmap()`为整个向导设置，这样就适用于所有没有指定像素映射的页面。

### `[protected] void QWizardPage::registerField(const QString &name, QWidget *widget, const char *property = nullptr, const char *changedSignal = nullptr)`

**作用与语义：**

创建一个称为`name`的场，与给定`widget`的给定`property`相关联。从此，该属性通过`field()`和`setField()`变得可访问。
字段是全局覆盖整个向导的，使任何单一页面都能轻松访问另一页面存储的信息，无需将所有逻辑放入`QWizard`，也无需页面间明确知道彼此。
如果`name`以星号（`*`）结尾，则该字段为必填字段。当页面有必填字段时，只有当所有必填字段都填满后，“下一”和/或“结束”按钮才会启用。这需要指定一个`changedSignal`，告诉`QWizard`重新检查强制字段存储的值。
`QWizard`知道最常见的Qt控件。对于这些（或其子类），你无需指定`property`或`changedSignal`。下表列出了这些控件：
- `Widget`：属性;变更通知信号
- `QAbstractButton`：bool `checked`;`toggled()`
- `QAbstractSlider`：智力`value`;`valueChanged()`
- `QComboBox`：智力`currentIndex`;`currentIndexChanged()`
- `QDateTimeEdit`：`QDateTime` `dateTime`;`dateTimeChanged()`
- `QLineEdit`：`QString` `text`;`textChanged()`
- `QListWidget`：智力`currentRow`;`currentRowChanged()`
- `QSpinBox`：智力`value`;`valueChanged()`
你可以用`QWizard::setDefaultProperty()`向该表添加条目或覆盖已有条目。
要将字段视为“已填”，`QWizard`只需检查其当前值是否等于原始值（即调用`initializePage()`前的值）。对于`QLineEdit`，还会检查`hasAcceptableInput()`返回为真，以尊重任何验证者或掩码。
`QWizard`强制字段机制为方便而提供。通过重新实现`QWizardPage::isComplete()`可以绕过。

### `void QWizardPage::setButtonText(QWizard::WizardButton which, const QString &text)`

**作用与语义：**

将按钮`which`上的文字设置为`text`于此页面。
默认情况下，按钮上的文字依赖于`QWizard::wizardStyle`，但可以通过`QWizard::setButtonText()`重新定义整个向导。

### `void QWizardPage::setCommitPage(bool commitPage)`

**作用与语义：**

如果`commitPage`为真，则将该页面设置为提交页面;否则，将其设置为普通页面。
提交页面表示一个操作，无法通过点击返回或取消来撤销。
提交按钮取代提交页面上的“下一步”按钮。点击该按钮就像点击下一步一样，直接调用`QWizard::next()`。
直接从提交页面进入的页面会被禁用“返回”按钮。

### `[protected] void QWizardPage::setField(const QString &name, const QVariant &value)`

**作用与语义：**

将称为`name`的字段值设置为`value`。
该函数可用于在向导的任何页面上设置字段。它等价于调用 `wizard()`->setField（`name`， `value`）。

### `void QWizardPage::setFinalPage(bool finalPage)`

**作用与语义：**

如果`finalPage`为真，明确设置该页面为最终页面。
调用 setFinalPage（true） 后，`isFinalPage()` 返回 `true`，完成按钮可见（如果 `isComplete()` 返回 true，则启用）。
调用 setFinalPage（false） 后，`isFinalPage()` 返回 `true`，如果 `nextId()`返回 -1;否则返回 `false`。

### `void QWizardPage::setPixmap(QWizard::WizardPixmap which, const QPixmap &pixmap)`

**作用与语义：**

将角色`which`的像素映射设置为`pixmap`。
像素地图是 `QWizard` 在显示页面时使用的。具体使用哪些像素地图取决于向导的样式。
像素映射也可以用`QWizard::setPixmap()`为整个向导设置，这样就适用于所有没有指定像素映射的页面。

### `[virtual] bool QWizardPage::validatePage()`

**作用与语义：**

当用户点击“下一步”或“完成”进行最后时刻验证时，`QWizard::validateCurrentPage()`调用了这个虚拟功能。如果返回`true`，下一页就会显示（或向导完成）;否则，当前页面保持在线。
默认实现返回`true`。
如果可能，通常禁用 Next 或 Finish 按钮（通过指定强制字段或重新实现 `isComplete()`）比重新实现 validPage() 更合适。

### `[protected] QWizard *QWizardPage::wizard() const`

**作用与语义：**

返回与该页面关联的向导，或者如果该页面尚未入`QWizard`，则返回`nullptr`。

### `void setSubTitle(const QString &subTitle)`

**作用与语义：**

该属性包含了该页面的副标题。
字幕通过`QWizard`显示，位于标题和实际页面之间。字幕为可选。在`ClassicStyle`和`ModernStyle`中，使用字幕是让标题显示的必要条件。在 `MacStyle` 中，字幕以文本标签的形式显示在实际页面上方。
副标题可以是纯文本，也可以是HTML，具体取决于`QWizard::subTitleFormat`属性的值。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `setSubTitle(...)` 修改 `subTitle`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTitle(const QString &title)`

**作用与语义：**

该属性包含了页面的标题。
标题通过`QWizard`显示，位于实际页面上方。所有页面都应有标题。
标题可以是纯文本，也可以是HTML格式，具体取决于`QWizard::titleFormat`属性的价值。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `setTitle(...)` 修改 `title`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QString subTitle() const`

**作用与语义：**

该属性包含了该页面的副标题。
字幕通过`QWizard`显示，位于标题和实际页面之间。字幕为可选。在`ClassicStyle`和`ModernStyle`中，使用字幕是让标题显示的必要条件。在 `MacStyle` 中，字幕以文本标签的形式显示在实际页面上方。
副标题可以是纯文本，也可以是HTML，具体取决于`QWizard::subTitleFormat`属性的值。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `subTitle()` 读取当前值；它不会修改应用状态。

### `QString title() const`

**作用与语义：**

该属性包含了页面的标题。
标题通过`QWizard`显示，位于实际页面上方。所有页面都应有标题。
标题可以是纯文本，也可以是HTML格式，具体取决于`QWizard::titleFormat`属性的价值。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `title()` 读取当前值；它不会修改应用状态。

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

`QWizardPage` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
