# QCommonStyle

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QCommonStyle` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QCommonStyle` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QCommonStyle>`
- 继承自：QStyle
- 直接派生类：QProxyStyle

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

### 公有函数

- `QCommonStyle()`
- `virtual ~QCommonStyle()`

### 重实现的公有函数

- `virtual void drawComplexControl(QStyle::ComplexControl cc, const QStyleOptionComplex *opt, QPainter *p, const QWidget *widget = nullptr) const override`
- `virtual void drawControl(QStyle::ControlElement element, const QStyleOption *opt, QPainter *p, const QWidget *widget = nullptr) const override`
- `virtual void drawPrimitive(QStyle::PrimitiveElement pe, const QStyleOption *opt, QPainter *p, const QWidget *widget = nullptr) const override`
- `virtual QPixmap generatedIconPixmap(QIcon::Mode iconMode, const QPixmap &pixmap, const QStyleOption *opt) const override`
- `virtual QStyle::SubControl hitTestComplexControl(QStyle::ComplexControl cc, const QStyleOptionComplex *opt, const QPoint &pt, const QWidget *widget = nullptr) const override`
- `virtual int layoutSpacing(QSizePolicy::ControlType control1, QSizePolicy::ControlType control2, Qt::Orientation orientation, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const override`
- `virtual int pixelMetric(QStyle::PixelMetric m, const QStyleOption *opt = nullptr, const QWidget *widget = nullptr) const override`
- `virtual void polish(QApplication *app) override`
- `virtual void polish(QPalette &pal) override`
- `virtual void polish(QWidget *widget) override`
- `virtual QSize sizeFromContents(QStyle::ContentsType contentsType, const QStyleOption *opt, const QSize &contentsSize, const QWidget *widget = nullptr) const override`
- `virtual QPixmap standardPixmap(QStyle::StandardPixmap sp, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const override`
- `virtual int styleHint(QStyle::StyleHint sh, const QStyleOption *opt = nullptr, const QWidget *widget = nullptr, QStyleHintReturn *hret = nullptr) const override`
- `virtual QRect subControlRect(QStyle::ComplexControl cc, const QStyleOptionComplex *opt, QStyle::SubControl sc, const QWidget *widget = nullptr) const override`
- `virtual QRect subElementRect(QStyle::SubElement sr, const QStyleOption *opt, const QWidget *widget = nullptr) const override`
- `virtual void unpolish(QApplication *application) override`
- `virtual void unpolish(QWidget *widget) override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 19 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QCommonStyle::QCommonStyle()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCommonStyle` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QCommonStyle::~QCommonStyle()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCommonStyle` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QCommonStyle::drawComplexControl(QStyle::ComplexControl cc, const QStyleOptionComplex *opt, QPainter *p, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCommonStyle` 的核心操作 `drawComplexControl`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `cc`：类型为 `QStyle::ComplexControl`。没有默认值，调用时必须提供。传入 `QStyle::ComplexControl` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `opt`：类型为 `const QStyleOptionComplex *`。没有默认值，调用时必须提供。传入 `const QStyleOptionComplex *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `p`：类型为 `QPainter *`。没有默认值，调用时必须提供。传入 `QPainter *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QCommonStyle::drawControl(QStyle::ControlElement element, const QStyleOption *opt, QPainter *p, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCommonStyle` 的核心操作 `drawControl`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `element`：类型为 `QStyle::ControlElement`。没有默认值，调用时必须提供。传入 `QStyle::ControlElement` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `opt`：类型为 `const QStyleOption *`。没有默认值，调用时必须提供。传入 `const QStyleOption *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `p`：类型为 `QPainter *`。没有默认值，调用时必须提供。传入 `QPainter *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QCommonStyle::drawPrimitive(QStyle::PrimitiveElement pe, const QStyleOption *opt, QPainter *p, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCommonStyle` 的核心操作 `drawPrimitive`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `pe`：类型为 `QStyle::PrimitiveElement`。没有默认值，调用时必须提供。传入 `QStyle::PrimitiveElement` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `opt`：类型为 `const QStyleOption *`。没有默认值，调用时必须提供。传入 `const QStyleOption *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `p`：类型为 `QPainter *`。没有默认值，调用时必须提供。传入 `QPainter *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QPixmap QCommonStyle::generatedIconPixmap(QIcon::Mode iconMode, const QPixmap &pixmap, const QStyleOption *opt) const`

**API 类别：** 成员函数说明

**中文解读：** `QCommonStyle::generatedIconPixmap` 用于计算、查询或取得与“generated、Icon、Pixmap”相关的操作。调用时要先确认当前状态和 `iconMode`、`pixmap`、`opt` 的有效范围；返回类型是 `QPixmap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixmap`。
- 参数 `iconMode`：类型为 `QIcon::Mode`。没有默认值，调用时必须提供。传入 `QIcon::Mode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `opt`：类型为 `const QStyleOption *`。没有默认值，调用时必须提供。传入 `const QStyleOption *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QStyle::SubControl QCommonStyle::hitTestComplexControl(QStyle::ComplexControl cc, const QStyleOptionComplex *opt, const QPoint &pt, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QCommonStyle::hitTestComplexControl` 用于计算、查询或取得与“hit、Test、Complex、Control”相关的操作。调用时要先确认当前状态和 `cc`、`opt`、`pt`、`widget` 的有效范围；返回类型是 `QStyle::SubControl`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStyle::SubControl`。
- 参数 `cc`：类型为 `QStyle::ComplexControl`。没有默认值，调用时必须提供。传入 `QStyle::ComplexControl` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `opt`：类型为 `const QStyleOptionComplex *`。没有默认值，调用时必须提供。传入 `const QStyleOptionComplex *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pt`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] int QCommonStyle::layoutSpacing(QSizePolicy::ControlType control1, QSizePolicy::ControlType control2, Qt::Orientation orientation, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QCommonStyle::layoutSpacing` 用于计算、查询或取得与“layout、Spacing”相关的操作。调用时要先确认当前状态和 `control1`、`control2`、`orientation`、`option`、`widget` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `control1`：类型为 `QSizePolicy::ControlType`。没有默认值，调用时必须提供。传入 `QSizePolicy::ControlType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `control2`：类型为 `QSizePolicy::ControlType`。没有默认值，调用时必须提供。传入 `QSizePolicy::ControlType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `orientation`：类型为 `Qt::Orientation`。没有默认值，调用时必须提供。传入 `Qt::Orientation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `option`：类型为 `const QStyleOption *`。默认值为 `nullptr`。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] int QCommonStyle::pixelMetric(QStyle::PixelMetric m, const QStyleOption *opt = nullptr, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QCommonStyle::pixelMetric` 用于计算、查询或取得与“pixel、Metric”相关的操作。调用时要先确认当前状态和 `m`、`opt`、`widget` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `m`：类型为 `QStyle::PixelMetric`。没有默认值，调用时必须提供。传入 `QStyle::PixelMetric` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `opt`：类型为 `const QStyleOption *`。默认值为 `nullptr`。传入 `const QStyleOption *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QCommonStyle::polish(QApplication *app)`

**API 类别：** 成员函数说明

**中文解读：** `QCommonStyle::polish` 用于执行与“polish”相关的操作。调用时要先确认当前状态和 `app` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `app`：类型为 `QApplication *`。没有默认值，调用时必须提供。传入 `QApplication *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QCommonStyle::polish(QPalette &pal)`

**API 类别：** 成员函数说明

**中文解读：** `QCommonStyle::polish` 用于执行与“polish”相关的操作。调用时要先确认当前状态和 `pal` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `pal`：类型为 `QPalette &`。没有默认值，调用时必须提供。传入 `QPalette &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QCommonStyle::polish(QWidget *widget)`

**API 类别：** 成员函数说明

**中文解读：** `QCommonStyle::polish` 用于执行与“polish”相关的操作。调用时要先确认当前状态和 `widget` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QSize QCommonStyle::sizeFromContents(QStyle::ContentsType contentsType, const QStyleOption *opt, const QSize &contentsSize, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QCommonStyle::sizeFromContents` 用于计算、查询或取得与“尺寸或数量、转换进入、Contents”相关的操作。调用时要先确认当前状态和 `contentsType`、`opt`、`contentsSize`、`widget` 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数 `contentsType`：类型为 `QStyle::ContentsType`。没有默认值，调用时必须提供。传入 `QStyle::ContentsType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `opt`：类型为 `const QStyleOption *`。没有默认值，调用时必须提供。传入 `const QStyleOption *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `contentsSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QPixmap QCommonStyle::standardPixmap(QStyle::StandardPixmap sp, const QStyleOption *option = nullptr, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QCommonStyle::standardPixmap` 用于计算、查询或取得与“standard、Pixmap”相关的操作。调用时要先确认当前状态和 `sp`、`option`、`widget` 的有效范围；返回类型是 `QPixmap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixmap`。
- 参数 `sp`：类型为 `QStyle::StandardPixmap`。没有默认值，调用时必须提供。传入 `QStyle::StandardPixmap` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `option`：类型为 `const QStyleOption *`。默认值为 `nullptr`。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] int QCommonStyle::styleHint(QStyle::StyleHint sh, const QStyleOption *opt = nullptr, const QWidget *widget = nullptr, QStyleHintReturn *hret = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QCommonStyle::styleHint` 用于计算、查询或取得与“style、Hint”相关的操作。调用时要先确认当前状态和 `sh`、`opt`、`widget`、`hret` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `sh`：类型为 `QStyle::StyleHint`。没有默认值，调用时必须提供。传入 `QStyle::StyleHint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `opt`：类型为 `const QStyleOption *`。默认值为 `nullptr`。传入 `const QStyleOption *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。
- 参数 `hret`：类型为 `QStyleHintReturn *`。默认值为 `nullptr`。传入 `QStyleHintReturn *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QRect QCommonStyle::subControlRect(QStyle::ComplexControl cc, const QStyleOptionComplex *opt, QStyle::SubControl sc, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QCommonStyle::subControlRect` 用于计算、查询或取得与“sub、Control、Rect”相关的操作。调用时要先确认当前状态和 `cc`、`opt`、`sc`、`widget` 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `cc`：类型为 `QStyle::ComplexControl`。没有默认值，调用时必须提供。传入 `QStyle::ComplexControl` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `opt`：类型为 `const QStyleOptionComplex *`。没有默认值，调用时必须提供。传入 `const QStyleOptionComplex *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sc`：类型为 `QStyle::SubControl`。没有默认值，调用时必须提供。传入 `QStyle::SubControl` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QRect QCommonStyle::subElementRect(QStyle::SubElement sr, const QStyleOption *opt, const QWidget *widget = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QCommonStyle::subElementRect` 用于计算、查询或取得与“sub、Element、Rect”相关的操作。调用时要先确认当前状态和 `sr`、`opt`、`widget` 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `sr`：类型为 `QStyle::SubElement`。没有默认值，调用时必须提供。传入 `QStyle::SubElement` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `opt`：类型为 `const QStyleOption *`。没有默认值，调用时必须提供。传入 `const QStyleOption *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `widget`：类型为 `const QWidget *`。默认值为 `nullptr`。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QCommonStyle::unpolish(QApplication *application)`

**API 类别：** 成员函数说明

**中文解读：** `QCommonStyle::unpolish` 用于执行与“unpolish”相关的操作。调用时要先确认当前状态和 `application` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `application`：类型为 `QApplication *`。没有默认值，调用时必须提供。传入 `QApplication *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QCommonStyle::unpolish(QWidget *widget)`

**API 类别：** 成员函数说明

**中文解读：** `QCommonStyle::unpolish` 用于执行与“unpolish”相关的操作。调用时要先确认当前状态和 `widget` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

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

`QCommonStyle` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
