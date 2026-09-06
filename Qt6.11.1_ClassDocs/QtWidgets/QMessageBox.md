# QMessageBox

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QMessageBox` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QMessageBox` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QMessageBox>`
- 继承自：QDialog
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

- `enum ButtonRole { InvalidRole, AcceptRole, RejectRole, DestructiveRole, ActionRole, …, ResetRole }`
- `enum Icon { NoIcon, Question, Information, Warning, Critical }`
- `(since 6.6) enum class Option { DontUseNativeDialog }`
- `flags Options`
- `enum StandardButton { Ok, Open, Save, Cancel, Close, …, ButtonMask }`
- `flags StandardButtons`

### 属性

- `detailedText : QString`
- `icon : Icon`
- `iconPixmap : QPixmap`
- `informativeText : QString`
- `(since 6.6) options : Options`
- `standardButtons : StandardButtons`
- `text : QString`
- `textFormat : Qt::TextFormat`
- `textInteractionFlags : Qt::TextInteractionFlags`

### 公有函数

- `QMessageBox(QWidget *parent = nullptr)`
- `QMessageBox(QMessageBox::Icon icon, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = NoButton, QWidget *parent = nullptr, Qt::WindowFlags f = Qt::Dialog | Qt::MSWindowsFixedSizeDialogHint)`
- `virtual ~QMessageBox()`
- `void addButton(QAbstractButton *button, QMessageBox::ButtonRole role)`
- `QPushButton * addButton(QMessageBox::StandardButton button)`
- `QPushButton * addButton(const QString &text, QMessageBox::ButtonRole role)`
- `QAbstractButton * button(QMessageBox::StandardButton which) const`
- `QMessageBox::ButtonRole buttonRole(QAbstractButton *button) const`
- `QList<QAbstractButton *> buttons() const`
- `QCheckBox * checkBox() const`
- `QAbstractButton * clickedButton() const`
- `QPushButton * defaultButton() const`
- `QString detailedText() const`
- `QAbstractButton * escapeButton() const`
- `QMessageBox::Icon icon() const`
- `QPixmap iconPixmap() const`
- `QString informativeText() const`
- `void open(QObject *receiver, const char *member)`
- `QMessageBox::Options options() const`
- `void removeButton(QAbstractButton *button)`
- `void setCheckBox(QCheckBox *cb)`
- `void setDefaultButton(QMessageBox::StandardButton button)`
- `void setDefaultButton(QPushButton *button)`
- `void setDetailedText(const QString &text)`
- `void setEscapeButton(QAbstractButton *button)`
- `void setEscapeButton(QMessageBox::StandardButton button)`
- `void setIcon(QMessageBox::Icon)`
- `void setIconPixmap(const QPixmap &pixmap)`
- `void setInformativeText(const QString &text)`
- `(since 6.6) void setOption(QMessageBox::Option option, bool on = true)`
- `void setOptions(QMessageBox::Options options)`
- `void setStandardButtons(QMessageBox::StandardButtons buttons)`
- `void setText(const QString &text)`
- `void setTextFormat(Qt::TextFormat format)`
- `void setTextInteractionFlags(Qt::TextInteractionFlags flags)`
- `void setWindowModality(Qt::WindowModality windowModality)`
- `void setWindowTitle(const QString &title)`
- `QMessageBox::StandardButton standardButton(QAbstractButton *button) const`
- `QMessageBox::StandardButtons standardButtons() const`
- `(since 6.6) bool testOption(QMessageBox::Option option) const`
- `QString text() const`
- `Qt::TextFormat textFormat() const`
- `Qt::TextInteractionFlags textInteractionFlags() const`

### 公有槽函数

- `virtual int exec() override`

### 信号

- `void buttonClicked(QAbstractButton *button)`

### 静态公有成员

- `void about(QWidget *parent, const QString &title, const QString &text)`
- `void aboutQt(QWidget *parent, const QString &title = QString())`
- `QMessageBox::StandardButton critical(QWidget *parent, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = Ok, QMessageBox::StandardButton defaultButton = NoButton)`
- `QMessageBox::StandardButton information(QWidget *parent, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = Ok, QMessageBox::StandardButton defaultButton = NoButton)`
- `QMessageBox::StandardButton question(QWidget *parent, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = StandardButtons(Yes | No), QMessageBox::StandardButton defaultButton = NoButton)`
- `QMessageBox::StandardButton warning(QWidget *parent, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = Ok, QMessageBox::StandardButton defaultButton = NoButton)`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *ev) override`
- `virtual void closeEvent(QCloseEvent *e) override`
- `virtual bool event(QEvent *e) override`
- `virtual void keyPressEvent(QKeyEvent *e) override`
- `virtual void resizeEvent(QResizeEvent *event) override`
- `virtual void showEvent(QShowEvent *e) override`

### 公开宏

- `QT_REQUIRE_VERSION(int argc, char **argv, const char *version)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 75 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QMessageBox::ButtonRole`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMessageBox` 暴露的类型声明 `Button、角色`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ButtonRole`。
- 属性名：`QMessageBox`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QMessageBox::Icon`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMessageBox` 暴露的类型声明 `Icon`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Icon`。
- 属性名：`QMessageBox`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] enum class QMessageBox::Optionflags QMessageBox::Options`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMessageBox` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Optionflags QMessageBox::Options`。
- 属性名：`QMessageBox`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QMessageBox::StandardButtonflags QMessageBox::StandardButtons`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QMessageBox` 暴露的类型声明 `Standard、Buttonflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:StandardButtonflags QMessageBox::StandardButtons`。
- 属性名：`QMessageBox`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `detailedText : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QMessageBox` 的配置属性。初始化或状态切换时通过 `setDetailedText(...)` 设置，之后用 `detailedText()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`detailedText`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `icon : Icon`

**API 类别：** 属性说明

**中文解读：** 这是 `QMessageBox` 的配置属性。初始化或状态切换时通过 `setIcon(...)` 设置，之后用 `icon()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Icon`。
- 属性名：`icon`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `iconPixmap : QPixmap`

**API 类别：** 属性说明

**中文解读：** 这是 `QMessageBox` 的配置属性。初始化或状态切换时通过 `setIconPixmap(...)` 设置，之后用 `iconPixmap()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QPixmap`。
- 属性名：`iconPixmap`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `informativeText : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QMessageBox` 的配置属性。初始化或状态切换时通过 `setInformativeText(...)` 设置，之后用 `informativeText()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`informativeText`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] options : Options`

**API 类别：** 属性说明

**中文解读：** 这是 `QMessageBox` 的配置属性。初始化或状态切换时通过 `setOptions(...)` 设置，之后用 `options()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Options`。
- 属性名：`options`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `standardButtons : StandardButtons`

**API 类别：** 属性说明

**中文解读：** 这是 `QMessageBox` 的配置属性。初始化或状态切换时通过 `setStandardButtons(...)` 设置，之后用 `standardButtons()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`StandardButtons`。
- 属性名：`standardButtons`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `text : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QMessageBox` 的配置属性。初始化或状态切换时通过 `setText(...)` 设置，之后用 `text()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`text`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `textFormat : Qt::TextFormat`

**API 类别：** 属性说明

**中文解读：** 这是 `QMessageBox` 的配置属性。初始化或状态切换时通过 `setTextFormat(...)` 设置，之后用 `TextFormat()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::TextFormat`。
- 属性名：`textFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `textInteractionFlags : Qt::TextInteractionFlags`

**API 类别：** 属性说明

**中文解读：** 这是 `QMessageBox` 的配置属性。初始化或状态切换时通过 `setTextInteractionFlags(...)` 设置，之后用 `TextInteractionFlags()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::TextInteractionFlags`。
- 属性名：`textInteractionFlags`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QMessageBox::QMessageBox(QWidget *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMessageBox` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMessageBox::QMessageBox(QMessageBox::Icon icon, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = NoButton, QWidget *parent = nullptr, Qt::WindowFlags f = Qt::Dialog | Qt::MSWindowsFixedSizeDialogHint)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMessageBox` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `icon`：类型为 `QMessageBox::Icon`。没有默认值，调用时必须提供。传入 `QMessageBox::Icon` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `title`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `buttons`：类型为 `QMessageBox::StandardButtons`。默认值为 `NoButton`。传入 `QMessageBox::StandardButtons` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `f`：类型为 `Qt::WindowFlags`。默认值为 `Qt::Dialog | Qt::MSWindowsFixedSizeDialogHint`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QMessageBox::~QMessageBox()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMessageBox` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QMessageBox::about(QWidget *parent, const QString &title, const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `about`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `parent`：类型为 `QWidget *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `title`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QMessageBox::aboutQt(QWidget *parent, const QString &title = QString())`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `aboutQt`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `parent`：类型为 `QWidget *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `title`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageBox::addButton(QAbstractButton *button, QMessageBox::ButtonRole role)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMessageBox` 添加依赖、数据或子对象的 API `addButton`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `button`：类型为 `QAbstractButton *`。没有默认值，调用时必须提供。传入 `QAbstractButton *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `role`：类型为 `QMessageBox::ButtonRole`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPushButton *QMessageBox::addButton(QMessageBox::StandardButton button)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMessageBox` 添加依赖、数据或子对象的 API `addButton`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QPushButton *`。
- 参数 `button`：类型为 `QMessageBox::StandardButton`。没有默认值，调用时必须提供。传入 `QMessageBox::StandardButton` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPushButton *QMessageBox::addButton(const QString &text, QMessageBox::ButtonRole role)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QMessageBox` 添加依赖、数据或子对象的 API `addButton`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QPushButton *`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `role`：类型为 `QMessageBox::ButtonRole`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractButton *QMessageBox::button(QMessageBox::StandardButton which) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageBox::button` 用于计算、查询或取得与“button”相关的操作。调用时要先确认当前状态和 `which` 的有效范围；返回类型是 `QAbstractButton *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractButton *`。
- 参数 `which`：类型为 `QMessageBox::StandardButton`。没有默认值，调用时必须提供。传入 `QMessageBox::StandardButton` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QMessageBox::buttonClicked(QAbstractButton *button)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMessageBox` 发出的通知信号 `buttonClicked`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `button`：类型为 `QAbstractButton *`。没有默认值，调用时必须提供。传入 `QAbstractButton *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMessageBox::ButtonRole QMessageBox::buttonRole(QAbstractButton *button) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageBox::buttonRole` 用于计算、查询或取得与“button、角色”相关的操作。调用时要先确认当前状态和 `button` 的有效范围；返回类型是 `QMessageBox::ButtonRole`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMessageBox::ButtonRole`。
- 参数 `button`：类型为 `QAbstractButton *`。没有默认值，调用时必须提供。传入 `QAbstractButton *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QAbstractButton *> QMessageBox::buttons() const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageBox::buttons` 用于计算、查询或取得与“buttons”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QAbstractButton *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QAbstractButton *>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QMessageBox::changeEvent(QEvent *ev)`

**API 类别：** 成员函数说明

**中文解读：** `QMessageBox::changeEvent` 用于执行与“change、Event”相关的操作。调用时要先确认当前状态和 `ev` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `ev`：类型为 `QEvent *`。没有默认值，调用时必须提供。传入 `QEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCheckBox *QMessageBox::checkBox() const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageBox::checkBox` 用于计算、查询或取得与“check、Box”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCheckBox *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCheckBox *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractButton *QMessageBox::clickedButton() const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageBox::clickedButton` 用于计算、查询或取得与“clicked、Button”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractButton *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractButton *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QMessageBox::closeEvent(QCloseEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `closeEvent`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QCloseEvent *`。没有默认值，调用时必须提供。传入 `QCloseEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QMessageBox::StandardButton QMessageBox::critical(QWidget *parent, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = Ok, QMessageBox::StandardButton defaultButton = NoButton)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `critical`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QMessageBox::StandardButton`。
- 参数 `parent`：类型为 `QWidget *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `title`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `buttons`：类型为 `QMessageBox::StandardButtons`。默认值为 `Ok`。传入 `QMessageBox::StandardButtons` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `defaultButton`：类型为 `QMessageBox::StandardButton`。默认值为 `NoButton`。传入 `QMessageBox::StandardButton` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPushButton *QMessageBox::defaultButton() const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageBox::defaultButton` 用于计算、查询或取得与“default、Button”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPushButton *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPushButton *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractButton *QMessageBox::escapeButton() const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageBox::escapeButton` 用于计算、查询或取得与“escape、Button”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractButton *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractButton *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QMessageBox::event(QEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QMessageBox::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `e`：类型为 `QEvent *`。没有默认值，调用时必须提供。传入 `QEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual slot] int QMessageBox::exec()`

**API 类别：** 成员函数说明

**中文解读：** `QMessageBox::exec` 用于计算、查询或取得与“执行”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QMessageBox::StandardButton QMessageBox::information(QWidget *parent, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = Ok, QMessageBox::StandardButton defaultButton = NoButton)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `information`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QMessageBox::StandardButton`。
- 参数 `parent`：类型为 `QWidget *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `title`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `buttons`：类型为 `QMessageBox::StandardButtons`。默认值为 `Ok`。传入 `QMessageBox::StandardButtons` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `defaultButton`：类型为 `QMessageBox::StandardButton`。默认值为 `NoButton`。传入 `QMessageBox::StandardButton` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QMessageBox::keyPressEvent(QKeyEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QMessageBox::keyPressEvent` 用于执行与“key、Press、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。传入 `QKeyEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageBox::open(QObject *receiver, const char *member)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `open`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `receiver`：类型为 `QObject *`。没有默认值，调用时必须提供。接收者对象。它决定槽函数所属线程和连接生命周期，必须在回调使用期间有效。
- 参数 `member`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QMessageBox::StandardButton QMessageBox::question(QWidget *parent, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = StandardButtons(Yes | No), QMessageBox::StandardButton defaultButton = NoButton)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `question`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QMessageBox::StandardButton`。
- 参数 `parent`：类型为 `QWidget *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `title`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `buttons`：类型为 `QMessageBox::StandardButtons`。默认值为 `StandardButtons(Yes | No)`。传入 `QMessageBox::StandardButtons` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `defaultButton`：类型为 `QMessageBox::StandardButton`。默认值为 `NoButton`。传入 `QMessageBox::StandardButton` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageBox::removeButton(QAbstractButton *button)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeButton`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `button`：类型为 `QAbstractButton *`。没有默认值，调用时必须提供。传入 `QAbstractButton *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QMessageBox::resizeEvent(QResizeEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QMessageBox::resizeEvent` 用于执行与“调整尺寸、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QResizeEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageBox::setCheckBox(QCheckBox *cb)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCheckBox`。调用它会改变 `QMessageBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `cb`：类型为 `QCheckBox *`。没有默认值，调用时必须提供。传入 `QCheckBox *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageBox::setDefaultButton(QMessageBox::StandardButton button)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDefaultButton`。调用它会改变 `QMessageBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `button`：类型为 `QMessageBox::StandardButton`。没有默认值，调用时必须提供。传入 `QMessageBox::StandardButton` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageBox::setDefaultButton(QPushButton *button)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDefaultButton`。调用它会改变 `QMessageBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `button`：类型为 `QPushButton *`。没有默认值，调用时必须提供。传入 `QPushButton *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageBox::setEscapeButton(QAbstractButton *button)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setEscapeButton`。调用它会改变 `QMessageBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `button`：类型为 `QAbstractButton *`。没有默认值，调用时必须提供。传入 `QAbstractButton *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageBox::setEscapeButton(QMessageBox::StandardButton button)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setEscapeButton`。调用它会改变 `QMessageBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `button`：类型为 `QMessageBox::StandardButton`。没有默认值，调用时必须提供。传入 `QMessageBox::StandardButton` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] void QMessageBox::setOption(QMessageBox::Option option, bool on = true)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setOption`。调用它会改变 `QMessageBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `option`：类型为 `QMessageBox::Option`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `on`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageBox::setWindowModality(Qt::WindowModality windowModality)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setWindowModality`。调用它会改变 `QMessageBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `windowModality`：类型为 `Qt::WindowModality`。没有默认值，调用时必须提供。传入 `Qt::WindowModality` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMessageBox::setWindowTitle(const QString &title)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setWindowTitle`。调用它会改变 `QMessageBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `title`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QMessageBox::showEvent(QShowEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QMessageBox::showEvent` 用于执行与“显示、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QShowEvent *`。没有默认值，调用时必须提供。传入 `QShowEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `QMessageBox::StandardButton QMessageBox::standardButton(QAbstractButton *button) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageBox::standardButton` 用于计算、查询或取得与“standard、Button”相关的操作。调用时要先确认当前状态和 `button` 的有效范围；返回类型是 `QMessageBox::StandardButton`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMessageBox::StandardButton`。
- 参数 `button`：类型为 `QAbstractButton *`。没有默认值，调用时必须提供。传入 `QAbstractButton *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] bool QMessageBox::testOption(QMessageBox::Option option) const`

**API 类别：** 成员函数说明

**中文解读：** `QMessageBox::testOption` 用于计算、查询或取得与“test、Option”相关的操作。调用时要先确认当前状态和 `option` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `option`：类型为 `QMessageBox::Option`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QMessageBox::StandardButton QMessageBox::warning(QWidget *parent, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = Ok, QMessageBox::StandardButton defaultButton = NoButton)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `warning`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QMessageBox::StandardButton`。
- 参数 `parent`：类型为 `QWidget *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `title`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `buttons`：类型为 `QMessageBox::StandardButtons`。默认值为 `Ok`。传入 `QMessageBox::StandardButtons` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `defaultButton`：类型为 `QMessageBox::StandardButton`。默认值为 `NoButton`。传入 `QMessageBox::StandardButton` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QT_REQUIRE_VERSION(int argc, char **argv, const char *version)`

**API 类别：** 宏说明

**中文解读：** `QMessageBox::QT_REQUIRE_VERSION` 用于执行与“VERSION”相关的操作。调用时要先确认当前状态和 `argc`、`argv`、`version` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `argc`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `argv`：类型为 `char **`。没有默认值，调用时必须提供。传入 `char **` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `version`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.6) enum class Option { DontUseNativeDialog }`

**API 类别：** 公有类型

**中文解读：** 这是 `QMessageBox` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags Options`

**API 类别：** 公有类型

**中文解读：** 这是 `QMessageBox` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum StandardButton { Ok, Open, Save, Cancel, Close, …, ButtonMask }`

**API 类别：** 公有类型

**中文解读：** 这是 `QMessageBox` 暴露的类型声明 `Standard、Button`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags StandardButtons`

**API 类别：** 公有类型

**中文解读：** 这是 `QMessageBox` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString detailedText() const`

**API 类别：** 公有函数

**中文解读：** `QMessageBox::detailedText` 用于计算、查询或取得与“detailed、文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMessageBox::Icon icon() const`

**API 类别：** 公有函数

**中文解读：** `QMessageBox::icon` 用于计算、查询或取得与“icon”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMessageBox::Icon`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMessageBox::Icon`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPixmap iconPixmap() const`

**API 类别：** 公有函数

**中文解读：** `QMessageBox::iconPixmap` 用于计算、查询或取得与“icon、Pixmap”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPixmap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixmap`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString informativeText() const`

**API 类别：** 公有函数

**中文解读：** `QMessageBox::informativeText` 用于计算、查询或取得与“informative、文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMessageBox::Options options() const`

**API 类别：** 公有函数

**中文解读：** `QMessageBox::options` 用于计算、查询或取得与“options”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMessageBox::Options`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMessageBox::Options`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDetailedText(const QString &text)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDetailedText`。调用它会改变 `QMessageBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setIcon(QMessageBox::Icon)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setIcon`。调用它会改变 `QMessageBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `Icon`：类型为 `QMessageBox::`。没有默认值，调用时必须提供。传入 `QMessageBox::` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setIconPixmap(const QPixmap &pixmap)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setIconPixmap`。调用它会改变 `QMessageBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setInformativeText(const QString &text)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setInformativeText`。调用它会改变 `QMessageBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setOptions(QMessageBox::Options options)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setOptions`。调用它会改变 `QMessageBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `options`：类型为 `QMessageBox::Options`。没有默认值，调用时必须提供。传入 `QMessageBox::Options` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setStandardButtons(QMessageBox::StandardButtons buttons)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setStandardButtons`。调用它会改变 `QMessageBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `buttons`：类型为 `QMessageBox::StandardButtons`。没有默认值，调用时必须提供。传入 `QMessageBox::StandardButtons` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setText(const QString &text)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setText`。调用它会改变 `QMessageBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setTextFormat(Qt::TextFormat format)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setTextFormat`。调用它会改变 `QMessageBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `Qt::TextFormat`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setTextInteractionFlags(Qt::TextInteractionFlags flags)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setTextInteractionFlags`。调用它会改变 `QMessageBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `flags`：类型为 `Qt::TextInteractionFlags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMessageBox::StandardButtons standardButtons() const`

**API 类别：** 公有函数

**中文解读：** `QMessageBox::standardButtons` 用于计算、查询或取得与“standard、Buttons”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMessageBox::StandardButtons`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMessageBox::StandardButtons`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString text() const`

**API 类别：** 公有函数

**中文解读：** `QMessageBox::text` 用于计算、查询或取得与“文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::TextFormat textFormat() const`

**API 类别：** 公有函数

**中文解读：** `QMessageBox::textFormat` 用于计算、查询或取得与“文本、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::TextFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::TextFormat`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::TextInteractionFlags textInteractionFlags() const`

**API 类别：** 公有函数

**中文解读：** `QMessageBox::textInteractionFlags` 用于计算、查询或取得与“文本、Interaction、标志”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::TextInteractionFlags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::TextInteractionFlags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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

`QMessageBox` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
