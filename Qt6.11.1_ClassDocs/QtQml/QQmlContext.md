# QQmlContext

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QQmlContext` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QQmlContext` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQmlContext>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Qml)
target_link_libraries(mytarget PRIVATE Qt6::Qml)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

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

- `struct PropertyPair`

### 公有函数

- `QQmlContext(QQmlContext *parentContext, QObject *parent = nullptr)`
- `QQmlContext(QQmlEngine *engine, QObject *parent = nullptr)`
- `virtual ~QQmlContext() override`
- `QUrl baseUrl() const`
- `(since 6.11) QList<QQmlContext *> childContexts() const`
- `QObject * contextObject() const`
- `QVariant contextProperty(const QString &name) const`
- `QQmlEngine * engine() const`
- `(since 6.11) QObject * findObjectRecursively(const QString &id) const`
- `(since 6.11) QList<QObject *> findObjectsRecursively(const QString &id) const`
- `bool isValid() const`
- `QString nameForObject(const QObject *object) const`
- `(since 6.2) QObject * objectForName(const QString &name) const`
- `QQmlContext * parentContext() const`
- `QUrl resolvedUrl(const QUrl &src) const`
- `void setBaseUrl(const QUrl &baseUrl)`
- `void setContextObject(QObject *object)`
- `void setContextProperties(const QList<QQmlContext::PropertyPair> &properties)`
- `void setContextProperty(const QString &name, QObject *value)`
- `void setContextProperty(const QString &name, const QVariant &value)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 21 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QQmlContext::QQmlContext(QQmlContext *parentContext, QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQmlContext` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parentContext`：类型为 `QQmlContext *`。没有默认值，调用时必须提供。传入 `QQmlContext *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQmlContext::QQmlContext(QQmlEngine *engine, QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQmlContext` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `engine`：类型为 `QQmlEngine *`。没有默认值，调用时必须提供。传入 `QQmlEngine *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual noexcept] QQmlContext::~QQmlContext()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQmlContext` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QUrl QQmlContext::baseUrl() const`

**API 类别：** 成员函数说明

**中文解读：** `QQmlContext::baseUrl` 用于计算、查询或取得与“base、Url”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QUrl`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QUrl`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] QList<QQmlContext *> QQmlContext::childContexts() const`

**API 类别：** 成员函数说明

**中文解读：** `QQmlContext::childContexts` 用于计算、查询或取得与“child、Contexts”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QQmlContext *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QQmlContext *>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QObject *QQmlContext::contextObject() const`

**API 类别：** 成员函数说明

**中文解读：** `QQmlContext::contextObject` 用于计算、查询或取得与“context、Object”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QObject *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QObject *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QQmlContext::contextProperty(const QString &name) const`

**API 类别：** 成员函数说明

**中文解读：** `QQmlContext::contextProperty` 用于计算、查询或取得与“context、Property”相关的操作。调用时要先确认当前状态和 `name` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQmlEngine *QQmlContext::engine() const`

**API 类别：** 成员函数说明

**中文解读：** `QQmlContext::engine` 用于计算、查询或取得与“engine”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQmlEngine *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQmlEngine *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] QObject *QQmlContext::findObjectRecursively(const QString &id) const`

**API 类别：** 成员函数说明

**中文解读：** `QQmlContext::findObjectRecursively` 用于计算、查询或取得与“查找、Object、Recursively”相关的操作。调用时要先确认当前状态和 `id` 的有效范围；返回类型是 `QObject *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QObject *`。
- 参数 `id`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] QList<QObject *> QQmlContext::findObjectsRecursively(const QString &id) const`

**API 类别：** 成员函数说明

**中文解读：** `QQmlContext::findObjectsRecursively` 用于计算、查询或取得与“查找、Objects、Recursively”相关的操作。调用时要先确认当前状态和 `id` 的有效范围；返回类型是 `QList<QObject *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QObject *>`。
- 参数 `id`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QQmlContext::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QQmlContext::nameForObject(const QObject *object) const`

**API 类别：** 成员函数说明

**中文解读：** `QQmlContext::nameForObject` 用于计算、查询或取得与“名称、For、Object”相关的操作。调用时要先确认当前状态和 `object` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `object`：类型为 `const QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] QObject *QQmlContext::objectForName(const QString &name) const`

**API 类别：** 成员函数说明

**中文解读：** `QQmlContext::objectForName` 用于计算、查询或取得与“object、For、名称”相关的操作。调用时要先确认当前状态和 `name` 的有效范围；返回类型是 `QObject *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QObject *`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQmlContext *QQmlContext::parentContext() const`

**API 类别：** 成员函数说明

**中文解读：** `QQmlContext::parentContext` 用于计算、查询或取得与“父对象、Context”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQmlContext *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQmlContext *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QUrl QQmlContext::resolvedUrl(const QUrl &src) const`

**API 类别：** 成员函数说明

**中文解读：** `QQmlContext::resolvedUrl` 用于计算、查询或取得与“resolved、Url”相关的操作。调用时要先确认当前状态和 `src` 的有效范围；返回类型是 `QUrl`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QUrl`。
- 参数 `src`：类型为 `const QUrl &`。没有默认值，调用时必须提供。传入 `const QUrl &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQmlContext::setBaseUrl(const QUrl &baseUrl)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBaseUrl`。调用它会改变 `QQmlContext` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `baseUrl`：类型为 `const QUrl &`。没有默认值，调用时必须提供。传入 `const QUrl &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQmlContext::setContextObject(QObject *object)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setContextObject`。调用它会改变 `QQmlContext` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `object`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQmlContext::setContextProperties(const QList<QQmlContext::PropertyPair> &properties)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setContextProperties`。调用它会改变 `QQmlContext` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `properties`：类型为 `const QList<QQmlContext::PropertyPair> &`。没有默认值，调用时必须提供。传入 `const QList<QQmlContext::PropertyPair> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQmlContext::setContextProperty(const QString &name, QObject *value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setContextProperty`。调用它会改变 `QQmlContext` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `value`：类型为 `QObject *`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQmlContext::setContextProperty(const QString &name, const QVariant &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setContextProperty`。调用它会改变 `QQmlContext` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `struct PropertyPair`

**API 类别：** 公有类型

**中文解读：** 这是 `QQmlContext` 的 `Property、Pair` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

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

`QQmlContext` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
