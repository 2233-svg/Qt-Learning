# QKeyEvent

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QKeyEvent` 是 Qt 的值类型，围绕“键事件”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QKeyEvent` 是事件或输入数据对象，描述 Qt 在事件分发过程中传递的状态。

**内部模型：** 事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

**适用场景：** 重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。

**典型调用链：** Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。

**先记住的坑：** 不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

## 2. 依赖与对象关系

- 头文件：`#include <QKeyEvent>`
- 继承自：QInputEvent
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。 使用时通常按这个过程组织：Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QKeyEvent(QEvent::Type type, int key, Qt::KeyboardModifiers modifiers, const QString &text = QString(), bool autorep = false, quint16 count = 1)`
- `QKeyEvent(QEvent::Type type, int key, Qt::KeyboardModifiers modifiers, quint32 nativeScanCode, quint32 nativeVirtualKey, quint32 nativeModifiers, const QString &text = QString(), bool autorep = false, quint16 count = 1, const QInputDevice *device = QInputDevice::primaryKeyboard())`
- `int count() const`
- `bool isAutoRepeat() const`
- `int key() const`
- `(since 6.0) QKeyCombination keyCombination() const`
- `bool matches(QKeySequence::StandardKey key) const`
- `Qt::KeyboardModifiers modifiers() const`
- `quint32 nativeModifiers() const`
- `quint32 nativeScanCode() const`
- `quint32 nativeVirtualKey() const`
- `QString text() const`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 12 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QKeyEvent::QKeyEvent(QEvent::Type type, int key, Qt::KeyboardModifiers modifiers, const QString &text = QString(), bool autorep = false, quint16 count = 1)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QKeyEvent` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `type`：类型为 `QEvent::Type`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `key`：类型为 `int`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `modifiers`：类型为 `Qt::KeyboardModifiers`。没有默认值，调用时必须提供。传入 `Qt::KeyboardModifiers` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QString &`。默认值为 `QString()`。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `autorep`：类型为 `bool`。默认值为 `false`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `quint16`。默认值为 `1`。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QKeyEvent::QKeyEvent(QEvent::Type type, int key, Qt::KeyboardModifiers modifiers, quint32 nativeScanCode, quint32 nativeVirtualKey, quint32 nativeModifiers, const QString &text = QString(), bool autorep = false, quint16 count = 1, const QInputDevice *device = QInputDevice::primaryKeyboard())`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QKeyEvent` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `type`：类型为 `QEvent::Type`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `key`：类型为 `int`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `modifiers`：类型为 `Qt::KeyboardModifiers`。没有默认值，调用时必须提供。传入 `Qt::KeyboardModifiers` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `nativeScanCode`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `nativeVirtualKey`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `nativeModifiers`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QString &`。默认值为 `QString()`。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `autorep`：类型为 `bool`。默认值为 `false`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `quint16`。默认值为 `1`。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `device`：类型为 `const QInputDevice *`。默认值为 `QInputDevice::primaryKeyboard()`。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QKeyEvent::count() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QKeyEvent` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QKeyEvent::isAutoRepeat() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isAutoRepeat`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QKeyEvent::key() const`

**API 类别：** 成员函数说明

**中文解读：** `QKeyEvent::key` 用于计算、查询或取得与“key”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QKeyCombination QKeyEvent::keyCombination() const`

**API 类别：** 成员函数说明

**中文解读：** `QKeyEvent::keyCombination` 用于计算、查询或取得与“key、Combination”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QKeyCombination`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QKeyCombination`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QKeyEvent::matches(QKeySequence::StandardKey key) const`

**API 类别：** 成员函数说明

**中文解读：** `QKeyEvent::matches` 用于计算、查询或取得与“matches”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `key`：类型为 `QKeySequence::StandardKey`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::KeyboardModifiers QKeyEvent::modifiers() const`

**API 类别：** 成员函数说明

**中文解读：** `QKeyEvent::modifiers` 用于计算、查询或取得与“modifiers”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::KeyboardModifiers`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::KeyboardModifiers`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint32 QKeyEvent::nativeModifiers() const`

**API 类别：** 成员函数说明

**中文解读：** `QKeyEvent::nativeModifiers` 用于计算、查询或取得与“native、Modifiers”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `quint32`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint32`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint32 QKeyEvent::nativeScanCode() const`

**API 类别：** 成员函数说明

**中文解读：** `QKeyEvent::nativeScanCode` 用于计算、查询或取得与“native、Scan、Code”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `quint32`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint32`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint32 QKeyEvent::nativeVirtualKey() const`

**API 类别：** 成员函数说明

**中文解读：** `QKeyEvent::nativeVirtualKey` 用于计算、查询或取得与“native、Virtual、Key”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `quint32`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint32`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QKeyEvent::text() const`

**API 类别：** 成员函数说明

**中文解读：** `QKeyEvent::text` 用于计算、查询或取得与“文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QKeyEvent` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
