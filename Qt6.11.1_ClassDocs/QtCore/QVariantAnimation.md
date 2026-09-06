# QVariantAnimation

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QVariantAnimation` 是 动画时间轴机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QVariantAnimation` 是动画框架中的类型，描述时间、状态、插值或动画组装行为。

**内部模型：** 动画通常由时间轴驱动属性变化；先确认动画对象、目标属性、持续时间和停止后的最终值，再组合 easing、loop 和 group。

**适用场景：** 界面过渡、状态变化和可视反馈需要平滑变化时使用。

**典型调用链：** 创建目标 -> 配置 duration/easing/start/end -> connect state/finished -> start/pause/stop -> 管理动画对象生命周期。

**先记住的坑：** 动画对象销毁会立即停止；重复 start 可能重置进度；不要用动画替代业务状态；跨线程动画通常不是正确方向。

## 2. 依赖与对象关系

- 头文件：`#include <QVariantAnimation>`
- 继承自：QAbstractAnimation
- 直接派生类：QPropertyAnimation

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

动画通常由时间轴驱动属性变化；先确认动画对象、目标属性、持续时间和停止后的最终值，再组合 easing、loop 和 group。

### 状态、生命周期和线程

**生命周期：** 动画必须保持目标和动画对象在运行期间有效。父对象、动画组或栈对象的生命周期要覆盖播放过程；删除或替换目标时先停止动画，避免回调访问旧对象。

**状态与结果：** 区分 stopped、running、paused、finished 和 loop 重启。`stop()` 后的当前值和终值取决于具体动画类型及配置，不能把停止当成完成；完成信号才表示时间轴走完。

**线程与事件循环：** 界面动画通常属于 GUI 线程并依赖事件循环；不要用动画对象承担跨线程任务或耗时计算。后台结果应先回到正确线程，再启动属性动画。

## 3. 直接使用

界面过渡、状态变化和可视反馈需要平滑变化时使用。 使用时通常按这个过程组织：创建目标 -> 配置 duration/easing/start/end -> connect state/finished -> start/pause/stop -> 管理动画对象生命周期。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `KeyValue`
- `KeyValues`

### 属性

- `currentValue : QVariant`
- `duration : int`
- `easingCurve : QEasingCurve`
- `endValue : QVariant`
- `startValue : QVariant`

### 公有函数

- `QVariantAnimation(QObject *parent = nullptr)`
- `virtual ~QVariantAnimation()`
- `QBindable<int> bindableDuration()`
- `QBindable<QEasingCurve> bindableEasingCurve()`
- `QVariant currentValue() const`
- `virtual int duration() const override`
- `QEasingCurve easingCurve() const`
- `QVariant endValue() const`
- `QVariant keyValueAt(qreal step) const`
- `QVariantAnimation::KeyValues keyValues() const`
- `void setDuration(int msecs)`
- `void setEasingCurve(const QEasingCurve &easing)`
- `void setEndValue(const QVariant &value)`
- `void setKeyValueAt(qreal step, const QVariant &value)`
- `void setKeyValues(const QVariantAnimation::KeyValues &keyValues)`
- `void setStartValue(const QVariant &value)`
- `QVariant startValue() const`

### 信号

- `void valueChanged(const QVariant &value)`

### 保护函数

- `virtual QVariant interpolated(const QVariant &from, const QVariant &to, qreal progress) const`
- `virtual void updateCurrentValue(const QVariant &value)`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`
- `virtual void updateCurrentTime(int) override`
- `virtual void updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState) override`

### 相关非成员函数

- `void qRegisterAnimationInterpolator(QVariant (*)(const T &, const T &, qreal) func)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 33 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[alias] QVariantAnimation::KeyValue`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVariantAnimation` 的配置属性。初始化或状态切换时通过 `setKeyValue(...)` 设置，之后用 `KeyValue()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:KeyValue`。
- 属性名：`QVariantAnimation`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariantAnimation::KeyValues`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVariantAnimation` 的配置属性。初始化或状态切换时通过 `setKeyValues(...)` 设置，之后用 `KeyValues()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:KeyValues`。
- 属性名：`QVariantAnimation`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] currentValue : QVariant`

**API 类别：** 属性说明

**中文解读：** 这是 `QVariantAnimation` 的状态/能力属性。通常通过 `currentValue()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QVariant`。
- 属性名：`currentValue`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] duration : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QVariantAnimation` 的配置属性。初始化或状态切换时通过 `setDuration(...)` 设置，之后用 `duration()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`duration`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] easingCurve : QEasingCurve`

**API 类别：** 属性说明

**中文解读：** 这是 `QVariantAnimation` 的配置属性。初始化或状态切换时通过 `setEasingCurve(...)` 设置，之后用 `easingCurve()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QEasingCurve`。
- 属性名：`easingCurve`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `endValue : QVariant`

**API 类别：** 属性说明

**中文解读：** 这是 `QVariantAnimation` 的配置属性。初始化或状态切换时通过 `setEndValue(...)` 设置，之后用 `endValue()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QVariant`。
- 属性名：`endValue`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `startValue : QVariant`

**API 类别：** 属性说明

**中文解读：** 这是 `QVariantAnimation` 的配置属性。初始化或状态切换时通过 `setStartValue(...)` 设置，之后用 `startValue()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QVariant`。
- 属性名：`startValue`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariantAnimation::QVariantAnimation(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVariantAnimation` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QVariantAnimation::~QVariantAnimation()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVariantAnimation` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QVariantAnimation::event(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QVariantAnimation::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] QVariant QVariantAnimation::interpolated(const QVariant &from, const QVariant &to, qreal progress) const`

**API 类别：** 成员函数说明

**中文解读：** `QVariantAnimation::interpolated` 用于计算、查询或取得与“interpolated”相关的操作。调用时要先确认当前状态和 `from`、`to`、`progress` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `from`：类型为 `const QVariant &`。没有默认值，调用时必须提供。传入 `const QVariant &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `to`：类型为 `const QVariant &`。没有默认值，调用时必须提供。传入 `const QVariant &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `progress`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QVariantAnimation::keyValueAt(qreal step) const`

**API 类别：** 成员函数说明

**中文解读：** `QVariantAnimation::keyValueAt` 用于计算、查询或取得与“key、值访问、按位置访问”相关的操作。调用时要先确认当前状态和 `step` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `step`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariantAnimation::KeyValues QVariantAnimation::keyValues() const`

**API 类别：** 成员函数说明

**中文解读：** `QVariantAnimation::keyValues` 用于计算、查询或取得与“key、Values”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVariantAnimation::KeyValues`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariantAnimation::KeyValues`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVariantAnimation::setKeyValueAt(qreal step, const QVariant &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setKeyValueAt`。调用它会改变 `QVariantAnimation` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `step`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVariantAnimation::setKeyValues(const QVariantAnimation::KeyValues &keyValues)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setKeyValues`。调用它会改变 `QVariantAnimation` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `keyValues`：类型为 `const QVariantAnimation::KeyValues &`。没有默认值，调用时必须提供。传入 `const QVariantAnimation::KeyValues &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QVariantAnimation::updateCurrentTime(int)`

**API 类别：** 成员函数说明

**中文解读：** `QVariantAnimation::updateCurrentTime` 用于执行与“更新、当前、时间”相关的操作。调用时要先确认当前状态和 `int` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `int`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QVariantAnimation::updateCurrentValue(const QVariant &value)`

**API 类别：** 成员函数说明

**中文解读：** `QVariantAnimation::updateCurrentValue` 用于执行与“更新、当前、值访问”相关的操作。调用时要先确认当前状态和 `value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QVariantAnimation::updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState)`

**API 类别：** 成员函数说明

**中文解读：** `QVariantAnimation::updateState` 用于执行与“更新、State”相关的操作。调用时要先确认当前状态和 `newState`、`oldState` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `newState`：类型为 `QAbstractAnimation::State`。没有默认值，调用时必须提供。传入 `QAbstractAnimation::State` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `oldState`：类型为 `QAbstractAnimation::State`。没有默认值，调用时必须提供。传入 `QAbstractAnimation::State` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QVariantAnimation::valueChanged(const QVariant &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVariantAnimation` 发出的通知信号 `valueChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> void qRegisterAnimationInterpolator(QVariant (*)(const T &, const T &, qreal) func)`

**API 类别：** 相关非成员函数

**中文解读：** `QVariantAnimation::qRegisterAnimationInterpolator` 用于计算、查询或取得与“q、注册、Animation、Interpolator”相关的操作。调用时要先确认当前状态和 `func` 的有效范围；返回类型是 `template <typename T> void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T> void`。
- 参数 `func`：类型为 `QVariant (*)(const T &, const T &, qreal)`。没有默认值，调用时必须提供。传入 `QVariant (*)(const T &, const T &, qreal)` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `KeyValue`

**API 类别：** 公有类型

**中文解读：** 这是 `QVariantAnimation` 的 `Key、值访问` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `KeyValues`

**API 类别：** 公有类型

**中文解读：** 这是 `QVariantAnimation` 的 `Key、Values` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<int> bindableDuration()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableDuration`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<int>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<QEasingCurve> bindableEasingCurve()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableEasingCurve`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<QEasingCurve>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant currentValue() const`

**API 类别：** 公有函数

**中文解读：** `QVariantAnimation::currentValue` 用于计算、查询或取得与“当前、值访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `virtual int duration() const override`

**API 类别：** 公有函数

**中文解读：** `QVariantAnimation::duration` 用于计算、查询或取得与“持续时间”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QEasingCurve easingCurve() const`

**API 类别：** 公有函数

**中文解读：** `QVariantAnimation::easingCurve` 用于计算、查询或取得与“easing、Curve”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QEasingCurve`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QEasingCurve`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant endValue() const`

**API 类别：** 公有函数

**中文解读：** 这是结束/释放/取消 API `endValue`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QVariant`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDuration(int msecs)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDuration`。调用它会改变 `QVariantAnimation` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `msecs`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setEasingCurve(const QEasingCurve &easing)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setEasingCurve`。调用它会改变 `QVariantAnimation` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `easing`：类型为 `const QEasingCurve &`。没有默认值，调用时必须提供。传入 `const QEasingCurve &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setEndValue(const QVariant &value)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setEndValue`。调用它会改变 `QVariantAnimation` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setStartValue(const QVariant &value)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setStartValue`。调用它会改变 `QVariantAnimation` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant startValue() const`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `startValue`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QVariant`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

动画必须保持目标和动画对象在运行期间有效。父对象、动画组或栈对象的生命周期要覆盖播放过程；删除或替换目标时先停止动画，避免回调访问旧对象。

### 状态和错误边界

区分 stopped、running、paused、finished 和 loop 重启。`stop()` 后的当前值和终值取决于具体动画类型及配置，不能把停止当成完成；完成信号才表示时间轴走完。

### 线程边界

界面动画通常属于 GUI 线程并依赖事件循环；不要用动画对象承担跨线程任务或耗时计算。后台结果应先回到正确线程，再启动属性动画。

### 最容易出现的错误

动画对象销毁会立即停止；重复 start 可能重置进度；不要用动画替代业务状态；跨线程动画通常不是正确方向。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QVariantAnimation` 所属机制类型：动画时间轴机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
