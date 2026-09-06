# QAccessibleEvent

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QAccessibleEvent` 是 Qt 的值类型，围绕“Accessible事件”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QAccessibleEvent` 是事件或输入数据对象，描述 Qt 在事件分发过程中传递的状态。

**内部模型：** 事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

**适用场景：** 重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。

**典型调用链：** Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。

**先记住的坑：** 不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

## 2. 依赖与对象关系

- 头文件：`#include <QAccessibleEvent>`
- 继承自：未在类页中列出
- 直接派生类：QAccessibleAnnouncementEvent、QAccessibleStateChangeEvent、QAccessibleTableModelChangeEvent、QAccessibleTextCursorEvent,、QAccessibleValueChangeEvent

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

- `QAccessibleEvent(QAccessibleInterface *interface, QAccessible::Event type)`
- `QAccessibleEvent(QObject *object, QAccessible::Event type)`
- `virtual ~QAccessibleEvent()`
- `virtual QAccessibleInterface * accessibleInterface() const`
- `int child() const`
- `QObject * object() const`
- `void setChild(int child)`
- `QAccessible::Event type() const`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 8 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QAccessibleEvent::QAccessibleEvent(QAccessibleInterface *interface, QAccessible::Event type)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAccessibleEvent` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `interface`：类型为 `QAccessibleInterface *`。没有默认值，调用时必须提供。传入 `QAccessibleInterface *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `type`：类型为 `QAccessible::Event`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAccessibleEvent::QAccessibleEvent(QObject *object, QAccessible::Event type)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAccessibleEvent` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `object`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `type`：类型为 `QAccessible::Event`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QAccessibleEvent::~QAccessibleEvent()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAccessibleEvent` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QAccessibleInterface *QAccessibleEvent::accessibleInterface() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleEvent::accessibleInterface` 用于计算、查询或取得与“accessible、Interface”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAccessibleInterface *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessibleInterface *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QAccessibleEvent::child() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleEvent::child` 用于计算、查询或取得与“child”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QObject *QAccessibleEvent::object() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleEvent::object` 用于计算、查询或取得与“object”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QObject *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QObject *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QAccessibleEvent::setChild(int child)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setChild`。调用它会改变 `QAccessibleEvent` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `child`：类型为 `int`。没有默认值，调用时必须提供。子对象或子节点；要确认它是否由父对象接管，以及调用后原指针是否仍有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAccessible::Event QAccessibleEvent::type() const`

**API 类别：** 成员函数说明

**中文解读：** `QAccessibleEvent::type` 用于计算、查询或取得与“类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAccessible::Event`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessible::Event`。
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

`QAccessibleEvent` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
