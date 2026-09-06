# QDialogButtonBox

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QDialogButtonBox` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QDialogButtonBox` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QDialogButtonBox>`
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

### 公有类型

- `enum ButtonLayout { WinLayout, MacLayout, KdeLayout, GnomeLayout, AndroidLayout }`
- `enum ButtonRole { InvalidRole, AcceptRole, RejectRole, DestructiveRole, ActionRole, …, ResetRole }`
- `enum StandardButton { Ok, Open, Save, Cancel, Close, …, NoButton }`
- `flags StandardButtons`

### 属性

- `centerButtons : bool`
- `orientation : Qt::Orientation`
- `standardButtons : StandardButtons`

### 公有函数

- `QDialogButtonBox(QWidget *parent = nullptr)`
- `QDialogButtonBox(QDialogButtonBox::StandardButtons buttons, QWidget *parent = nullptr)`
- `QDialogButtonBox(Qt::Orientation orientation, QWidget *parent = nullptr)`
- `QDialogButtonBox(QDialogButtonBox::StandardButtons buttons, Qt::Orientation orientation, QWidget *parent = nullptr)`
- `virtual ~QDialogButtonBox()`
- `QPushButton * addButton(QDialogButtonBox::StandardButton button)`
- `void addButton(QAbstractButton *button, QDialogButtonBox::ButtonRole role)`
- `QPushButton * addButton(const QString &text, QDialogButtonBox::ButtonRole role)`
- `QPushButton * button(QDialogButtonBox::StandardButton which) const`
- `QDialogButtonBox::ButtonRole buttonRole(QAbstractButton *button) const`
- `QList<QAbstractButton *> buttons() const`
- `bool centerButtons() const`
- `void clear()`
- `Qt::Orientation orientation() const`
- `void removeButton(QAbstractButton *button)`
- `void setCenterButtons(bool center)`
- `void setOrientation(Qt::Orientation orientation)`
- `void setStandardButtons(QDialogButtonBox::StandardButtons buttons)`
- `QDialogButtonBox::StandardButton standardButton(QAbstractButton *button) const`
- `QDialogButtonBox::StandardButtons standardButtons() const`

### 信号

- `void accepted()`
- `void clicked(QAbstractButton *button)`
- `void helpRequested()`
- `void rejected()`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *event) override`
- `virtual bool event(QEvent *event) override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 34 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QDialogButtonBox::ButtonLayout`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QDialogButtonBox` 暴露的类型声明 `Button、Layout`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ButtonLayout`。
- 属性名：`QDialogButtonBox`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QDialogButtonBox::ButtonRole`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QDialogButtonBox` 暴露的类型声明 `Button、角色`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ButtonRole`。
- 属性名：`QDialogButtonBox`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QDialogButtonBox::StandardButtonflags QDialogButtonBox::StandardButtons`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QDialogButtonBox` 暴露的类型声明 `Standard、Buttonflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:StandardButtonflags QDialogButtonBox::StandardButtons`。
- 属性名：`QDialogButtonBox`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `centerButtons : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QDialogButtonBox` 的配置属性。初始化或状态切换时通过 `setCenterButtons(...)` 设置，之后用 `centerButtons()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`centerButtons`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `orientation : Qt::Orientation`

**API 类别：** 属性说明

**中文解读：** 这是 `QDialogButtonBox` 的配置属性。初始化或状态切换时通过 `setOrientation(...)` 设置，之后用 `Orientation()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::Orientation`。
- 属性名：`orientation`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `standardButtons : StandardButtons`

**API 类别：** 属性说明

**中文解读：** 这是 `QDialogButtonBox` 的配置属性。初始化或状态切换时通过 `setStandardButtons(...)` 设置，之后用 `standardButtons()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`StandardButtons`。
- 属性名：`standardButtons`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDialogButtonBox::QDialogButtonBox(QWidget *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDialogButtonBox` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QDialogButtonBox::QDialogButtonBox(QDialogButtonBox::StandardButtons buttons, QWidget *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDialogButtonBox` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `buttons`：类型为 `QDialogButtonBox::StandardButtons`。没有默认值，调用时必须提供。传入 `QDialogButtonBox::StandardButtons` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDialogButtonBox::QDialogButtonBox(Qt::Orientation orientation, QWidget *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDialogButtonBox` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `orientation`：类型为 `Qt::Orientation`。没有默认值，调用时必须提供。传入 `Qt::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDialogButtonBox::QDialogButtonBox(QDialogButtonBox::StandardButtons buttons, Qt::Orientation orientation, QWidget *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDialogButtonBox` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `buttons`：类型为 `QDialogButtonBox::StandardButtons`。没有默认值，调用时必须提供。传入 `QDialogButtonBox::StandardButtons` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `orientation`：类型为 `Qt::Orientation`。没有默认值，调用时必须提供。传入 `Qt::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QDialogButtonBox::~QDialogButtonBox()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDialogButtonBox` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QDialogButtonBox::accepted()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDialogButtonBox` 发出的通知信号 `accepted`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPushButton *QDialogButtonBox::addButton(QDialogButtonBox::StandardButton button)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QDialogButtonBox` 添加依赖、数据或子对象的 API `addButton`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QPushButton *`。
- 参数 `button`：类型为 `QDialogButtonBox::StandardButton`。没有默认值，调用时必须提供。传入 `QDialogButtonBox::StandardButton` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDialogButtonBox::addButton(QAbstractButton *button, QDialogButtonBox::ButtonRole role)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QDialogButtonBox` 添加依赖、数据或子对象的 API `addButton`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `button`：类型为 `QAbstractButton *`。没有默认值，调用时必须提供。传入 `QAbstractButton *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `role`：类型为 `QDialogButtonBox::ButtonRole`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPushButton *QDialogButtonBox::addButton(const QString &text, QDialogButtonBox::ButtonRole role)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QDialogButtonBox` 添加依赖、数据或子对象的 API `addButton`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QPushButton *`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `role`：类型为 `QDialogButtonBox::ButtonRole`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPushButton *QDialogButtonBox::button(QDialogButtonBox::StandardButton which) const`

**API 类别：** 成员函数说明

**中文解读：** `QDialogButtonBox::button` 用于计算、查询或取得与“button”相关的操作。调用时要先确认当前状态和 `which` 的有效范围；返回类型是 `QPushButton *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPushButton *`。
- 参数 `which`：类型为 `QDialogButtonBox::StandardButton`。没有默认值，调用时必须提供。传入 `QDialogButtonBox::StandardButton` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDialogButtonBox::ButtonRole QDialogButtonBox::buttonRole(QAbstractButton *button) const`

**API 类别：** 成员函数说明

**中文解读：** `QDialogButtonBox::buttonRole` 用于计算、查询或取得与“button、角色”相关的操作。调用时要先确认当前状态和 `button` 的有效范围；返回类型是 `QDialogButtonBox::ButtonRole`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDialogButtonBox::ButtonRole`。
- 参数 `button`：类型为 `QAbstractButton *`。没有默认值，调用时必须提供。传入 `QAbstractButton *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QAbstractButton *> QDialogButtonBox::buttons() const`

**API 类别：** 成员函数说明

**中文解读：** `QDialogButtonBox::buttons` 用于计算、查询或取得与“buttons”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QAbstractButton *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QAbstractButton *>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QDialogButtonBox::changeEvent(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QDialogButtonBox::changeEvent` 用于执行与“change、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDialogButtonBox::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QDialogButtonBox::clicked(QAbstractButton *button)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDialogButtonBox` 发出的通知信号 `clicked`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `button`：类型为 `QAbstractButton *`。没有默认值，调用时必须提供。传入 `QAbstractButton *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QDialogButtonBox::event(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QDialogButtonBox::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QDialogButtonBox::helpRequested()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDialogButtonBox` 发出的通知信号 `helpRequested`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QDialogButtonBox::rejected()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDialogButtonBox` 发出的通知信号 `rejected`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDialogButtonBox::removeButton(QAbstractButton *button)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeButton`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `button`：类型为 `QAbstractButton *`。没有默认值，调用时必须提供。传入 `QAbstractButton *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDialogButtonBox::StandardButton QDialogButtonBox::standardButton(QAbstractButton *button) const`

**API 类别：** 成员函数说明

**中文解读：** `QDialogButtonBox::standardButton` 用于计算、查询或取得与“standard、Button”相关的操作。调用时要先确认当前状态和 `button` 的有效范围；返回类型是 `QDialogButtonBox::StandardButton`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDialogButtonBox::StandardButton`。
- 参数 `button`：类型为 `QAbstractButton *`。没有默认值，调用时必须提供。传入 `QAbstractButton *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum StandardButton { Ok, Open, Save, Cancel, Close, …, NoButton }`

**API 类别：** 公有类型

**中文解读：** 这是 `QDialogButtonBox` 暴露的类型声明 `Standard、Button`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags StandardButtons`

**API 类别：** 公有类型

**中文解读：** 这是 `QDialogButtonBox` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool centerButtons() const`

**API 类别：** 公有函数

**中文解读：** `QDialogButtonBox::centerButtons` 用于计算、查询或取得与“center、Buttons”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::Orientation orientation() const`

**API 类别：** 公有函数

**中文解读：** `QDialogButtonBox::orientation` 用于计算、查询或取得与“orientation”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::Orientation`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::Orientation`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setCenterButtons(bool center)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setCenterButtons`。调用它会改变 `QDialogButtonBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `center`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setOrientation(Qt::Orientation orientation)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setOrientation`。调用它会改变 `QDialogButtonBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `orientation`：类型为 `Qt::Orientation`。没有默认值，调用时必须提供。传入 `Qt::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setStandardButtons(QDialogButtonBox::StandardButtons buttons)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setStandardButtons`。调用它会改变 `QDialogButtonBox` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `buttons`：类型为 `QDialogButtonBox::StandardButtons`。没有默认值，调用时必须提供。传入 `QDialogButtonBox::StandardButtons` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDialogButtonBox::StandardButtons standardButtons() const`

**API 类别：** 公有函数

**中文解读：** `QDialogButtonBox::standardButtons` 用于计算、查询或取得与“standard、Buttons”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDialogButtonBox::StandardButtons`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDialogButtonBox::StandardButtons`。
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

`QDialogButtonBox` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
