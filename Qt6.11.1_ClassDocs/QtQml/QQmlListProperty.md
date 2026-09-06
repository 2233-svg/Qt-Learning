# QQmlListProperty

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QQmlListProperty` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QQmlListProperty` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQmlListProperty>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Qml)
target_link_libraries(mytarget PRIVATE Qt6::Qml)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

### 状态、生命周期和线程

**生命周期：** QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

**状态与结果：** 属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

**线程与事件循环：** 大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

## 3. 直接使用

需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。 使用时通常按这个过程组织：注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

```cpp
// C++ 侧暴露属性/信号后，在 QML 中建立绑定。
// 变化时发出 notify signal，避免在绑定表达式中直接修改状态。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `AppendFunction`
- `AtFunction`
- `ClearFunction`
- `CountFunction`
- `RemoveLastFunction`
- `ReplaceFunction`

### 公有函数

- `QQmlListProperty(QObject *object, QList<T *> *list)`
- `QQmlListProperty(QObject *object, void *data, QQmlListProperty<T>::CountFunction count, QQmlListProperty<T>::AtFunction at)`
- `QQmlListProperty(QObject *object, void *data, QQmlListProperty<T>::AppendFunction append, QQmlListProperty<T>::CountFunction count, QQmlListProperty<T>::AtFunction at, QQmlListProperty<T>::ClearFunction clear)`
- `QQmlListProperty(QObject *object, void *data, QQmlListProperty<T>::AppendFunction append, QQmlListProperty<T>::CountFunction count, QQmlListProperty<T>::AtFunction at, QQmlListProperty<T>::ClearFunction clear, QQmlListProperty<T>::ReplaceFunction replace, QQmlListProperty<T>::RemoveLastFunction removeLast)`
- `bool operator==(const QQmlListProperty<T> &other) const`

### 公开宏

- `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_APPEND`
- `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_REPLACE`
- `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_REPLACE_IF_NOT_DEFAULT`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 22 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[alias] QQmlListProperty::AppendFunction`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QQmlListProperty` 的配置属性。初始化或状态切换时通过 `setAppendFunction(...)` 设置，之后用 `AppendFunction()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:AppendFunction`。
- 属性名：`QQmlListProperty`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QQmlListProperty::AtFunction`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QQmlListProperty` 的配置属性。初始化或状态切换时通过 `setAtFunction(...)` 设置，之后用 `AtFunction()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:AtFunction`。
- 属性名：`QQmlListProperty`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QQmlListProperty::ClearFunction`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QQmlListProperty` 的配置属性。初始化或状态切换时通过 `setClearFunction(...)` 设置，之后用 `ClearFunction()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:ClearFunction`。
- 属性名：`QQmlListProperty`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QQmlListProperty::CountFunction`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QQmlListProperty` 的配置属性。初始化或状态切换时通过 `setCountFunction(...)` 设置，之后用 `CountFunction()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:CountFunction`。
- 属性名：`QQmlListProperty`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QQmlListProperty::RemoveLastFunction`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QQmlListProperty` 的配置属性。初始化或状态切换时通过 `setRemoveLastFunction(...)` 设置，之后用 `RemoveLastFunction()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:RemoveLastFunction`。
- 属性名：`QQmlListProperty`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QQmlListProperty::ReplaceFunction`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QQmlListProperty` 的配置属性。初始化或状态切换时通过 `setReplaceFunction(...)` 设置，之后用 `ReplaceFunction()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:ReplaceFunction`。
- 属性名：`QQmlListProperty`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQmlListProperty::QQmlListProperty(QObject *object, QList<T *> *list)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQmlListProperty` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `object`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `list`：类型为 `QList<T *> *`。没有默认值，调用时必须提供。传入 `QList<T *> *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQmlListProperty::QQmlListProperty(QObject *object, void *data, QQmlListProperty<T>::CountFunction count, QQmlListProperty<T>::AtFunction at)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQmlListProperty` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `object`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `data`：类型为 `void *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `count`：类型为 `QQmlListProperty<T>::CountFunction`。没有默认值，调用时必须提供。传入 `QQmlListProperty<T>::CountFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `at`：类型为 `QQmlListProperty<T>::AtFunction`。没有默认值，调用时必须提供。传入 `QQmlListProperty<T>::AtFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQmlListProperty::QQmlListProperty(QObject *object, void *data, QQmlListProperty<T>::AppendFunction append, QQmlListProperty<T>::CountFunction count, QQmlListProperty<T>::AtFunction at, QQmlListProperty<T>::ClearFunction clear)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQmlListProperty` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `object`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `data`：类型为 `void *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `append`：类型为 `QQmlListProperty<T>::AppendFunction`。没有默认值，调用时必须提供。传入 `QQmlListProperty<T>::AppendFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `QQmlListProperty<T>::CountFunction`。没有默认值，调用时必须提供。传入 `QQmlListProperty<T>::CountFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `at`：类型为 `QQmlListProperty<T>::AtFunction`。没有默认值，调用时必须提供。传入 `QQmlListProperty<T>::AtFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `clear`：类型为 `QQmlListProperty<T>::ClearFunction`。没有默认值，调用时必须提供。传入 `QQmlListProperty<T>::ClearFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQmlListProperty::QQmlListProperty(QObject *object, void *data, QQmlListProperty<T>::AppendFunction append, QQmlListProperty<T>::CountFunction count, QQmlListProperty<T>::AtFunction at, QQmlListProperty<T>::ClearFunction clear, QQmlListProperty<T>::ReplaceFunction replace, QQmlListProperty<T>::RemoveLastFunction removeLast)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQmlListProperty` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `object`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `data`：类型为 `void *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `append`：类型为 `QQmlListProperty<T>::AppendFunction`。没有默认值，调用时必须提供。传入 `QQmlListProperty<T>::AppendFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `QQmlListProperty<T>::CountFunction`。没有默认值，调用时必须提供。传入 `QQmlListProperty<T>::CountFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `at`：类型为 `QQmlListProperty<T>::AtFunction`。没有默认值，调用时必须提供。传入 `QQmlListProperty<T>::AtFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `clear`：类型为 `QQmlListProperty<T>::ClearFunction`。没有默认值，调用时必须提供。传入 `QQmlListProperty<T>::ClearFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `replace`：类型为 `QQmlListProperty<T>::ReplaceFunction`。没有默认值，调用时必须提供。传入 `QQmlListProperty<T>::ReplaceFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `removeLast`：类型为 `QQmlListProperty<T>::RemoveLastFunction`。没有默认值，调用时必须提供。传入 `QQmlListProperty<T>::RemoveLastFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QQmlListProperty::operator==(const QQmlListProperty<T> &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQmlListProperty` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QQmlListProperty<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void *QQmlListProperty::data`

**API 类别：** Member Variable Documentation

**中文解读：** 这是 `QQmlListProperty` 的配置属性。初始化或状态切换时通过 `setData(...)` 设置，之后用 `data()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 成员类型：`void *`。
- 成员名：`data`；读取前确认所属对象或命名空间仍有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QObject *QQmlListProperty::object`

**API 类别：** Member Variable Documentation

**中文解读：** 这是 `QQmlListProperty` 的配置属性。初始化或状态切换时通过 `setObject(...)` 设置，之后用 `object()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 成员类型：`QObject *`。
- 成员名：`object`；读取前确认所属对象或命名空间仍有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_APPEND`

**API 类别：** 宏说明

**中文解读：** 这是 `QQmlListProperty` 的 `追加` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_REPLACE`

**API 类别：** 宏说明

**中文解读：** 这是 `QQmlListProperty` 的 `替换` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QML_LIST_PROPERTY_ASSIGN_BEHAVIOR_REPLACE_IF_NOT_DEFAULT`

**API 类别：** 宏说明

**中文解读：** 这是 `QQmlListProperty` 的 `DEFAULT` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `AppendFunction`

**API 类别：** 公有类型

**中文解读：** 这是 `QQmlListProperty` 的 `追加、Function` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `AtFunction`

**API 类别：** 公有类型

**中文解读：** 这是 `QQmlListProperty` 的 `按位置访问、Function` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `ClearFunction`

**API 类别：** 公有类型

**中文解读：** 这是 `QQmlListProperty` 的 `清空、Function` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `CountFunction`

**API 类别：** 公有类型

**中文解读：** 这是 `QQmlListProperty` 的 `数量统计、Function` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `RemoveLastFunction`

**API 类别：** 公有类型

**中文解读：** 这是 `QQmlListProperty` 的 `移除、末项、Function` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `ReplaceFunction`

**API 类别：** 公有类型

**中文解读：** 这是 `QQmlListProperty` 的 `替换、Function` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

### 状态和错误边界

属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

### 线程边界

大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

### 最容易出现的错误

不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QQmlListProperty` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
