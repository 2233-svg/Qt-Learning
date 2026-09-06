# QXYSeries

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** `QXYSeries` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QXYSeries` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QXYSeries>`
- 继承自：QAbstractSeries
- 直接派生类：QLineSeries、QScatterSeries

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `(since 6.2) enum class PointConfiguration { Color, Size, Visibility, LabelVisibility, LabelFormat }`

### 属性

- `(since 6.2) bestFitLineColor : QColor`
- `(since 6.2) bestFitLineVisible : bool`
- `color : QColor`
- `pointLabelsClipping : bool`
- `pointLabelsColor : QColor`
- `pointLabelsFont : QFont`
- `pointLabelsFormat : QString`
- `pointLabelsVisible : bool`
- `pointsVisible : bool`
- `(since 6.2) selectedColor : QColor`

### 公有函数

- `virtual ~QXYSeries()`
- `void append(qreal x, qreal y)`
- `void append(const QList<QPointF> &points)`
- `void append(const QPointF &point)`
- `const QPointF & at(int index) const`
- `QColor bestFitLineColor() const`
- `(since 6.2) QPair<qreal, qreal> bestFitLineEquation(bool &ok) const`
- `bool bestFitLineVisible() const`
- `QBrush brush() const`
- `void clear()`
- `(since 6.2) void clearPointConfiguration(const int index)`
- `(since 6.2) void clearPointConfiguration(const int index, const QXYSeries::PointConfiguration key)`
- `(since 6.2) void clearPointsConfiguration()`
- `(since 6.2) void clearPointsConfiguration(const QXYSeries::PointConfiguration key)`
- `virtual QColor color() const`
- `(since 6.2) void colorBy(const QList<qreal> &sourceData, const QLinearGradient &gradient = QLinearGradient())`
- `int count() const`
- `(since 6.2) void deselectAllPoints()`
- `(since 6.2) void deselectPoint(int index)`
- `(since 6.2) void deselectPoints(const QList<int> &indexes)`
- `void insert(int index, const QPointF &point)`
- `(since 6.2) bool isPointSelected(int index)`
- `(since 6.2) const QImage & lightMarker() const`
- `(since 6.2) qreal markerSize() const`
- `QPen pen() const`
- `(since 6.2) QHash<QXYSeries::PointConfiguration, QVariant> pointConfiguration(const int index) const`
- `bool pointLabelsClipping() const`
- `QColor pointLabelsColor() const`
- `QFont pointLabelsFont() const`
- `QString pointLabelsFormat() const`
- `bool pointLabelsVisible() const`
- `QList<QPointF> points() const`
- `(since 6.2) QXYSeries::PointsConfigurationHash pointsConfiguration() const`
- `bool pointsVisible() const`
- `void remove(const QPointF &point)`
- `void remove(int index)`
- `void remove(qreal x, qreal y)`
- `void removePoints(int index, int count)`
- `void replace(const QList<QPointF> &points)`
- `void replace(const QPointF &oldPoint, const QPointF &newPoint)`
- `void replace(int index, const QPointF &newPoint)`
- `void replace(int index, qreal newX, qreal newY)`
- `void replace(qreal oldX, qreal oldY, qreal newX, qreal newY)`
- `(since 6.2) void selectAllPoints()`
- `(since 6.2) void selectPoint(int index)`
- `(since 6.2) void selectPoints(const QList<int> &indexes)`
- `(since 6.2) const QImage & selectedLightMarker() const`
- `(since 6.2) QList<int> selectedPoints() const`
- `void setBestFitLineColor(const QColor &color)`
- `void setBestFitLineVisible(bool visible = true)`
- `virtual void setBrush(const QBrush &brush)`
- `virtual void setColor(const QColor &color)`
- `(since 6.2) void setLightMarker(const QImage &lightMarker)`
- `(since 6.2) void setMarkerSize(qreal size)`
- `virtual void setPen(const QPen &pen)`
- `(since 6.2) void setPointConfiguration(const int index, const QHash<QXYSeries::PointConfiguration, QVariant> &configuration)`
- `(since 6.2) void setPointConfiguration(const int index, const QXYSeries::PointConfiguration key, const QVariant &value)`
- `void setPointLabelsClipping(bool enabled = true)`
- `void setPointLabelsColor(const QColor &color)`
- `void setPointLabelsFont(const QFont &font)`
- `void setPointLabelsFormat(const QString &format)`
- `void setPointLabelsVisible(bool visible = true)`
- `(since 6.2) void setPointSelected(int index, bool selected)`
- `(since 6.2) void setPointsConfiguration(const QHash<int, QHash<QXYSeries::PointConfiguration, QVariant>> &pointsConfiguration)`
- `void setPointsVisible(bool visible = true)`
- `void setSelectedColor(const QColor &color)`
- `(since 6.2) void setSelectedLightMarker(const QImage &selectedLightMarker)`
- `(since 6.2) void sizeBy(const QList<qreal> &sourceData, const qreal minSize, const qreal maxSize)`
- `(since 6.2) void toggleSelection(const QList<int> &indexes)`
- `QXYSeries & operator<<(const QList<QPointF> &points)`
- `QXYSeries & operator<<(const QPointF &point)`

### 信号

- `void bestFitLineColorChanged(const QColor &color)`
- `void bestFitLineVisibilityChanged(bool visible)`
- `void clicked(const QPointF &point)`
- `void colorChanged(QColor color)`
- `void doubleClicked(const QPointF &point)`
- `void hovered(const QPointF &point, bool state)`
- `(since 6.2) void lightMarkerChanged(const QImage &lightMarker)`
- `void markerSizeChanged(qreal size)`
- `void penChanged(const QPen &pen)`
- `void pointAdded(int index)`
- `void pointLabelsClippingChanged(bool clipping)`
- `void pointLabelsColorChanged(const QColor &color)`
- `void pointLabelsFontChanged(const QFont &font)`
- `void pointLabelsFormatChanged(const QString &format)`
- `void pointLabelsVisibilityChanged(bool visible)`
- `void pointRemoved(int index)`
- `void pointReplaced(int index)`
- `void pointsRemoved(int index, int count)`
- `void pointsReplaced()`
- `void pressed(const QPointF &point)`
- `void released(const QPointF &point)`
- `void selectedColorChanged(const QColor &color)`
- `void selectedPointsChanged()`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 105 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[since 6.2] enum class QXYSeries::PointConfiguration`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QXYSeries` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:PointConfiguration`。
- 属性名：`QXYSeries`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] bestFitLineColor : QColor`

**API 类别：** 属性说明

**中文解读：** 这是 `QXYSeries` 的配置属性。初始化或状态切换时通过 `setBestFitLineColor(...)` 设置，之后用 `bestFitLineColor()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QColor`。
- 属性名：`bestFitLineColor`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] bestFitLineVisible : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QXYSeries` 的配置属性。初始化或状态切换时通过 `setBestFitLineVisible(...)` 设置，之后用 `bestFitLineVisible()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`bestFitLineVisible`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `color : QColor`

**API 类别：** 属性说明

**中文解读：** 这是 `QXYSeries` 的配置属性。初始化或状态切换时通过 `setColor(...)` 设置，之后用 `color()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QColor`。
- 属性名：`color`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `pointLabelsClipping : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QXYSeries` 的配置属性。初始化或状态切换时通过 `setPointLabelsClipping(...)` 设置，之后用 `pointLabelsClipping()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`pointLabelsClipping`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `pointLabelsColor : QColor`

**API 类别：** 属性说明

**中文解读：** 这是 `QXYSeries` 的配置属性。初始化或状态切换时通过 `setPointLabelsColor(...)` 设置，之后用 `pointLabelsColor()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QColor`。
- 属性名：`pointLabelsColor`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `pointLabelsFont : QFont`

**API 类别：** 属性说明

**中文解读：** 这是 `QXYSeries` 的配置属性。初始化或状态切换时通过 `setPointLabelsFont(...)` 设置，之后用 `pointLabelsFont()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QFont`。
- 属性名：`pointLabelsFont`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `pointLabelsFormat : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QXYSeries` 的配置属性。初始化或状态切换时通过 `setPointLabelsFormat(...)` 设置，之后用 `pointLabelsFormat()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`pointLabelsFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `pointLabelsVisible : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QXYSeries` 的配置属性。初始化或状态切换时通过 `setPointLabelsVisible(...)` 设置，之后用 `pointLabelsVisible()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`pointLabelsVisible`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `pointsVisible : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QXYSeries` 的配置属性。初始化或状态切换时通过 `setPointsVisible(...)` 设置，之后用 `pointsVisible()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`pointsVisible`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] selectedColor : QColor`

**API 类别：** 属性说明

**中文解读：** 这是 `QXYSeries` 的配置属性。初始化或状态切换时通过 `setSelectedColor(...)` 设置，之后用 `selectedColor()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QColor`。
- 属性名：`selectedColor`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QXYSeries::~QXYSeries()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXYSeries::append(qreal x, qreal y)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QXYSeries` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXYSeries::append(const QList<QPointF> &points)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QXYSeries` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QList<QPointF> &`。没有默认值，调用时必须提供。传入 `const QList<QPointF> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXYSeries::append(const QPointF &point)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QXYSeries` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QPointF &QXYSeries::at(int index) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `at`，用于取得 `QXYSeries` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`const QPointF &`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::bestFitLineColorChanged(const QColor &color)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `bestFitLineColorChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] QPair<qreal, qreal> QXYSeries::bestFitLineEquation(bool &ok) const`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::bestFitLineEquation` 用于计算、查询或取得与“best、Fit、行、Equation”相关的操作。调用时要先确认当前状态和 `ok` 的有效范围；返回类型是 `QPair<qreal, qreal>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPair<qreal, qreal>`。
- 参数 `ok`：类型为 `bool &`。没有默认值，调用时必须提供。传入 `bool &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::bestFitLineVisibilityChanged(bool visible)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `bestFitLineVisibilityChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `visible`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBrush QXYSeries::brush() const`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::brush` 用于计算、查询或取得与“brush”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QBrush`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QBrush`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXYSeries::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::clearPointConfiguration(const int index)`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::clearPointConfiguration` 用于执行与“清空、Point、Configuration”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::clearPointConfiguration(const int index, const QXYSeries::PointConfiguration key)`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::clearPointConfiguration` 用于执行与“清空、Point、Configuration”相关的操作。调用时要先确认当前状态和 `index`、`key` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `key`：类型为 `const QXYSeries::PointConfiguration`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::clearPointsConfiguration()`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::clearPointsConfiguration` 用于执行与“清空、Points、Configuration”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::clearPointsConfiguration(const QXYSeries::PointConfiguration key)`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::clearPointsConfiguration` 用于执行与“清空、Points、Configuration”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `const QXYSeries::PointConfiguration`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::clicked(const QPointF &point)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `clicked`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::colorBy(const QList<qreal> &sourceData, const QLinearGradient &gradient = QLinearGradient())`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::colorBy` 用于执行与“color、By”相关的操作。调用时要先确认当前状态和 `sourceData`、`gradient` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sourceData`：类型为 `const QList<qreal> &`。没有默认值，调用时必须提供。传入 `const QList<qreal> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `gradient`：类型为 `const QLinearGradient &`。默认值为 `QLinearGradient()`。传入 `const QLinearGradient &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::colorChanged(QColor color)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `colorChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `QColor`。没有默认值，调用时必须提供。传入 `QColor` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QXYSeries::count() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QXYSeries` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::deselectAllPoints()`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::deselectAllPoints` 用于执行与“deselect、All、Points”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::deselectPoint(int index)`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::deselectPoint` 用于执行与“deselect、Point”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::deselectPoints(const QList<int> &indexes)`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::deselectPoints` 用于执行与“deselect、Points”相关的操作。调用时要先确认当前状态和 `indexes` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `indexes`：类型为 `const QList<int> &`。没有默认值，调用时必须提供。传入 `const QList<int> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::doubleClicked(const QPointF &point)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `doubleClicked`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::hovered(const QPointF &point, bool state)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `hovered`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `state`：类型为 `bool`。没有默认值，调用时必须提供。状态值或状态对象；它描述调用时的阶段，不能把某个状态下有效的 API 用到其他阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXYSeries::insert(int index, const QPointF &point)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QXYSeries` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] bool QXYSeries::isPointSelected(int index)`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isPointSelected`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] const QImage &QXYSeries::lightMarker() const`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::lightMarker` 用于计算、查询或取得与“light、Marker”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QImage &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QImage &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal, since 6.2] void QXYSeries::lightMarkerChanged(const QImage &lightMarker)`

**API 类别：** 成员函数说明

**中文解读：** 这是状态变化通知 `lightMarkerChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `lightMarker`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] qreal QXYSeries::markerSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::markerSize` 用于计算、查询或取得与“marker、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::markerSizeChanged(qreal size)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `markerSizeChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qreal`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPen QXYSeries::pen() const`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::pen` 用于计算、查询或取得与“pen”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPen`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPen`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::penChanged(const QPen &pen)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `penChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `pen`：类型为 `const QPen &`。没有默认值，调用时必须提供。传入 `const QPen &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::pointAdded(int index)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `pointAdded`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] QHash<QXYSeries::PointConfiguration, QVariant> QXYSeries::pointConfiguration(const int index) const`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::pointConfiguration` 用于计算、查询或取得与“point、Configuration”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QHash<QXYSeries::PointConfiguration, QVariant>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QHash<QXYSeries::PointConfiguration, QVariant>`。
- 参数 `index`：类型为 `const int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::pointLabelsClippingChanged(bool clipping)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `pointLabelsClippingChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `clipping`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::pointLabelsColorChanged(const QColor &color)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `pointLabelsColorChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::pointLabelsFontChanged(const QFont &font)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `pointLabelsFontChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `font`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::pointLabelsFormatChanged(const QString &format)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `pointLabelsFormatChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `const QString &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::pointLabelsVisibilityChanged(bool visible)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `pointLabelsVisibilityChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `visible`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::pointRemoved(int index)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `pointRemoved`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::pointReplaced(int index)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `pointReplaced`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QPointF> QXYSeries::points() const`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::points` 用于计算、查询或取得与“points”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QPointF>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QPointF>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] QXYSeries::PointsConfigurationHash QXYSeries::pointsConfiguration() const`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::pointsConfiguration` 用于计算、查询或取得与“points、Configuration”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QXYSeries::PointsConfigurationHash`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QXYSeries::PointsConfigurationHash`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::pointsRemoved(int index, int count)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `pointsRemoved`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::pointsReplaced()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `pointsReplaced`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::pressed(const QPointF &point)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `pressed`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::released(const QPointF &point)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `released`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXYSeries::remove(const QPointF &point)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXYSeries::remove(int index)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXYSeries::remove(qreal x, qreal y)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXYSeries::removePoints(int index, int count)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removePoints`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXYSeries::replace(const QList<QPointF> &points)`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::replace` 用于执行与“替换”相关的操作。调用时要先确认当前状态和 `points` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `points`：类型为 `const QList<QPointF> &`。没有默认值，调用时必须提供。传入 `const QList<QPointF> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXYSeries::replace(const QPointF &oldPoint, const QPointF &newPoint)`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::replace` 用于执行与“替换”相关的操作。调用时要先确认当前状态和 `oldPoint`、`newPoint` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `oldPoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `newPoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXYSeries::replace(int index, const QPointF &newPoint)`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::replace` 用于执行与“替换”相关的操作。调用时要先确认当前状态和 `index`、`newPoint` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `newPoint`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXYSeries::replace(int index, qreal newX, qreal newY)`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::replace` 用于执行与“替换”相关的操作。调用时要先确认当前状态和 `index`、`newX`、`newY` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `newX`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `newY`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QXYSeries::replace(qreal oldX, qreal oldY, qreal newX, qreal newY)`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::replace` 用于执行与“替换”相关的操作。调用时要先确认当前状态和 `oldX`、`oldY`、`newX`、`newY` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `oldX`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `oldY`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `newX`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `newY`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::selectAllPoints()`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::selectAllPoints` 用于执行与“select、All、Points”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::selectPoint(int index)`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::selectPoint` 用于执行与“select、Point”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::selectPoints(const QList<int> &indexes)`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::selectPoints` 用于执行与“select、Points”相关的操作。调用时要先确认当前状态和 `indexes` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `indexes`：类型为 `const QList<int> &`。没有默认值，调用时必须提供。传入 `const QList<int> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] const QImage &QXYSeries::selectedLightMarker() const`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::selectedLightMarker` 用于计算、查询或取得与“selected、Light、Marker”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QImage &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QImage &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] QList<int> QXYSeries::selectedPoints() const`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::selectedPoints` 用于计算、查询或取得与“selected、Points”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<int>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<int>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QXYSeries::selectedPointsChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 发出的通知信号 `selectedPointsChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QXYSeries::setBrush(const QBrush &brush)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBrush`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `brush`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::setLightMarker(const QImage &lightMarker)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setLightMarker`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `lightMarker`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::setMarkerSize(qreal size)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMarkerSize`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qreal`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QXYSeries::setPen(const QPen &pen)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPen`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `pen`：类型为 `const QPen &`。没有默认值，调用时必须提供。传入 `const QPen &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::setPointConfiguration(const int index, const QHash<QXYSeries::PointConfiguration, QVariant> &configuration)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPointConfiguration`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `configuration`：类型为 `const QHash<QXYSeries::PointConfiguration, QVariant> &`。没有默认值，调用时必须提供。传入 `const QHash<QXYSeries::PointConfiguration, QVariant> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::setPointConfiguration(const int index, const QXYSeries::PointConfiguration key, const QVariant &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPointConfiguration`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `const int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `key`：类型为 `const QXYSeries::PointConfiguration`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::setPointSelected(int index, bool selected)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPointSelected`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `selected`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::setPointsConfiguration(const QHash<int, QHash<QXYSeries::PointConfiguration, QVariant>> &pointsConfiguration)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPointsConfiguration`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `pointsConfiguration`：类型为 `const QHash<int, QHash<QXYSeries::PointConfiguration, QVariant>> &`。没有默认值，调用时必须提供。传入 `const QHash<int, QHash<QXYSeries::PointConfiguration, QVariant>> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::setSelectedLightMarker(const QImage &selectedLightMarker)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSelectedLightMarker`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `selectedLightMarker`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::sizeBy(const QList<qreal> &sourceData, const qreal minSize, const qreal maxSize)`

**API 类别：** 成员函数说明

**中文解读：** `QXYSeries::sizeBy` 用于执行与“尺寸或数量、By”相关的操作。调用时要先确认当前状态和 `sourceData`、`minSize`、`maxSize` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sourceData`：类型为 `const QList<qreal> &`。没有默认值，调用时必须提供。传入 `const QList<qreal> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `minSize`：类型为 `const qreal`。没有默认值，调用时必须提供。传入 `const qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `maxSize`：类型为 `const qreal`。没有默认值，调用时必须提供。传入 `const qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QXYSeries::toggleSelection(const QList<int> &indexes)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toggleSelection`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`void`。
- 参数 `indexes`：类型为 `const QList<int> &`。没有默认值，调用时必须提供。传入 `const QList<int> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QXYSeries &QXYSeries::operator<<(const QList<QPointF> &points)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QXYSeries &`。
- 参数 `points`：类型为 `const QList<QPointF> &`。没有默认值，调用时必须提供。传入 `const QList<QPointF> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QXYSeries &QXYSeries::operator<<(const QPointF &point)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QXYSeries` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QXYSeries &`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QColor bestFitLineColor() const`

**API 类别：** 公有函数

**中文解读：** `QXYSeries::bestFitLineColor` 用于计算、查询或取得与“best、Fit、行、Color”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool bestFitLineVisible() const`

**API 类别：** 公有函数

**中文解读：** `QXYSeries::bestFitLineVisible` 用于计算、查询或取得与“best、Fit、行、可见状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `virtual QColor color() const`

**API 类别：** 公有函数

**中文解读：** `QXYSeries::color` 用于计算、查询或取得与“color”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool pointLabelsClipping() const`

**API 类别：** 公有函数

**中文解读：** `QXYSeries::pointLabelsClipping` 用于计算、查询或取得与“point、Labels、Clipping”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QColor pointLabelsColor() const`

**API 类别：** 公有函数

**中文解读：** `QXYSeries::pointLabelsColor` 用于计算、查询或取得与“point、Labels、Color”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont pointLabelsFont() const`

**API 类别：** 公有函数

**中文解读：** `QXYSeries::pointLabelsFont` 用于计算、查询或取得与“point、Labels、字体”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString pointLabelsFormat() const`

**API 类别：** 公有函数

**中文解读：** `QXYSeries::pointLabelsFormat` 用于计算、查询或取得与“point、Labels、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool pointLabelsVisible() const`

**API 类别：** 公有函数

**中文解读：** `QXYSeries::pointLabelsVisible` 用于计算、查询或取得与“point、Labels、可见状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool pointsVisible() const`

**API 类别：** 公有函数

**中文解读：** `QXYSeries::pointsVisible` 用于计算、查询或取得与“points、可见状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setBestFitLineColor(const QColor &color)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setBestFitLineColor`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setBestFitLineVisible(bool visible = true)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setBestFitLineVisible`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `visible`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `virtual void setColor(const QColor &color)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setColor`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setPointLabelsClipping(bool enabled = true)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setPointLabelsClipping`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enabled`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setPointLabelsColor(const QColor &color)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setPointLabelsColor`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setPointLabelsFont(const QFont &font)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setPointLabelsFont`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `font`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setPointLabelsFormat(const QString &format)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setPointLabelsFormat`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `const QString &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setPointLabelsVisible(bool visible = true)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setPointLabelsVisible`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `visible`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setPointsVisible(bool visible = true)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setPointsVisible`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `visible`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSelectedColor(const QColor &color)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSelectedColor`。调用它会改变 `QXYSeries` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void selectedColorChanged(const QColor &color)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `selectedColorChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QXYSeries` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
