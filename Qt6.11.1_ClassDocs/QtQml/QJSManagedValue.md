# QJSManagedValue

> Qt 6.11.1 · Qt Qml

## 1. 先建立直觉

**一句话定位：** `QJSManagedValue` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Qml 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QJSManagedValue` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QJSManagedValue>`
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
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Type { Undefined, Boolean, Number, String, Object, …, Function }`

### 公有函数

- `QJSManagedValue()`
- `QJSManagedValue(QJSValue value, QJSEngine *engine)`
- `QJSManagedValue(const QJSPrimitiveValue &value, QJSEngine *engine)`
- `QJSManagedValue(const QString &string, QJSEngine *engine)`
- `QJSManagedValue(const QVariant &variant, QJSEngine *engine)`
- `QJSManagedValue(QJSManagedValue &&other)`
- `~QJSManagedValue()`
- `QJSValue call(const QJSValueList &arguments = {}) const`
- `QJSValue callAsConstructor(const QJSValueList &arguments = {}) const`
- `QJSValue callWithInstance(const QJSValue &instance, const QJSValueList &arguments = {}) const`
- `bool deleteProperty(const QString &name)`
- `bool deleteProperty(quint32 arrayIndex)`
- `QJSEngine * engine() const`
- `bool equals(const QJSManagedValue &other) const`
- `bool hasOwnProperty(const QString &name) const`
- `bool hasOwnProperty(quint32 arrayIndex) const`
- `bool hasProperty(const QString &name) const`
- `bool hasProperty(quint32 arrayIndex) const`
- `bool isArray() const`
- `bool isBoolean() const`
- `bool isDate() const`
- `bool isError() const`
- `bool isFunction() const`
- `bool isInteger() const`
- `bool isNull() const`
- `bool isNumber() const`
- `bool isObject() const`
- `bool isQMetaObject() const`
- `bool isQObject() const`
- `bool isRegularExpression() const`
- `bool isString() const`
- `bool isSymbol() const`
- `bool isUndefined() const`
- `bool isUrl() const`
- `bool isVariant() const`
- `QJSValue property(const QString &name) const`
- `QJSValue property(quint32 arrayIndex) const`
- `QJSManagedValue prototype() const`
- `void setProperty(const QString &name, const QJSValue &value)`
- `void setProperty(quint32 arrayIndex, const QJSValue &value)`
- `void setPrototype(const QJSManagedValue &prototype)`
- `bool strictlyEquals(const QJSManagedValue &other) const`
- `bool toBoolean() const`
- `QDateTime toDateTime() const`
- `int toInteger() const`
- `QJSValue toJSValue() const`
- `double toNumber() const`
- `QJSPrimitiveValue toPrimitive() const`
- `const QMetaObject * toQMetaObject() const`
- `QObject * toQObject() const`
- `QRegularExpression toRegularExpression() const`
- `QString toString() const`
- `QUrl toUrl() const`
- `QVariant toVariant() const`
- `QJSManagedValue::Type type() const`
- `QJSManagedValue & operator=(QJSManagedValue &&other)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 57 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QJSManagedValue::Type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QJSManagedValue` 暴露的类型声明 `类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Type`。
- 属性名：`QJSManagedValue`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QJSManagedValue::QJSManagedValue()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJSManagedValue` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSManagedValue::QJSManagedValue(QJSValue value, QJSEngine *engine)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJSManagedValue` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `value`：类型为 `QJSValue`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。
- 参数 `engine`：类型为 `QJSEngine *`。没有默认值，调用时必须提供。传入 `QJSEngine *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSManagedValue::QJSManagedValue(const QJSPrimitiveValue &value, QJSEngine *engine)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJSManagedValue` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `value`：类型为 `const QJSPrimitiveValue &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。
- 参数 `engine`：类型为 `QJSEngine *`。没有默认值，调用时必须提供。传入 `QJSEngine *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSManagedValue::QJSManagedValue(const QString &string, QJSEngine *engine)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJSManagedValue` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `engine`：类型为 `QJSEngine *`。没有默认值，调用时必须提供。传入 `QJSEngine *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSManagedValue::QJSManagedValue(const QVariant &variant, QJSEngine *engine)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJSManagedValue` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `variant`：类型为 `const QVariant &`。没有默认值，调用时必须提供。传入 `const QVariant &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `engine`：类型为 `QJSEngine *`。没有默认值，调用时必须提供。传入 `QJSEngine *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSManagedValue::QJSManagedValue(QJSManagedValue &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJSManagedValue` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QJSManagedValue &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QJSManagedValue::~QJSManagedValue()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJSManagedValue` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSValue QJSManagedValue::call(const QJSValueList &arguments = {}) const`

**API 类别：** 成员函数说明

**中文解读：** `QJSManagedValue::call` 用于计算、查询或取得与“call”相关的操作。调用时要先确认当前状态和 `arguments` 的有效范围；返回类型是 `QJSValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSValue`。
- 参数 `arguments`：类型为 `const QJSValueList &`。默认值为 `{}`。传入 `const QJSValueList &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSValue QJSManagedValue::callAsConstructor(const QJSValueList &arguments = {}) const`

**API 类别：** 成员函数说明

**中文解读：** `QJSManagedValue::callAsConstructor` 用于计算、查询或取得与“call、As、Constructor”相关的操作。调用时要先确认当前状态和 `arguments` 的有效范围；返回类型是 `QJSValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSValue`。
- 参数 `arguments`：类型为 `const QJSValueList &`。默认值为 `{}`。传入 `const QJSValueList &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSValue QJSManagedValue::callWithInstance(const QJSValue &instance, const QJSValueList &arguments = {}) const`

**API 类别：** 成员函数说明

**中文解读：** `QJSManagedValue::callWithInstance` 用于计算、查询或取得与“call、With、Instance”相关的操作。调用时要先确认当前状态和 `instance`、`arguments` 的有效范围；返回类型是 `QJSValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSValue`。
- 参数 `instance`：类型为 `const QJSValue &`。没有默认值，调用时必须提供。传入 `const QJSValue &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `arguments`：类型为 `const QJSValueList &`。默认值为 `{}`。传入 `const QJSValueList &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::deleteProperty(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `deleteProperty`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::deleteProperty(quint32 arrayIndex)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `deleteProperty`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `arrayIndex`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSEngine *QJSManagedValue::engine() const`

**API 类别：** 成员函数说明

**中文解读：** `QJSManagedValue::engine` 用于计算、查询或取得与“engine”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QJSEngine *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSEngine *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::equals(const QJSManagedValue &other) const`

**API 类别：** 成员函数说明

**中文解读：** `QJSManagedValue::equals` 用于计算、查询或取得与“equals”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QJSManagedValue &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::hasOwnProperty(const QString &name) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasOwnProperty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::hasOwnProperty(quint32 arrayIndex) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasOwnProperty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `arrayIndex`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::hasProperty(const QString &name) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasProperty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::hasProperty(quint32 arrayIndex) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasProperty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `arrayIndex`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::isArray() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isArray`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::isBoolean() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isBoolean`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::isDate() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isDate`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::isError() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isError`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::isFunction() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isFunction`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::isInteger() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isInteger`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::isNull() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNull`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::isNumber() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNumber`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::isObject() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isObject`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::isQMetaObject() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isQMetaObject`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::isQObject() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isQObject`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::isRegularExpression() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isRegularExpression`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::isString() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isString`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::isSymbol() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSymbol`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::isUndefined() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isUndefined`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::isUrl() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isUrl`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::isVariant() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isVariant`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSValue QJSManagedValue::property(const QString &name) const`

**API 类别：** 成员函数说明

**中文解读：** `QJSManagedValue::property` 用于计算、查询或取得与“property”相关的操作。调用时要先确认当前状态和 `name` 的有效范围；返回类型是 `QJSValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSValue`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSValue QJSManagedValue::property(quint32 arrayIndex) const`

**API 类别：** 成员函数说明

**中文解读：** `QJSManagedValue::property` 用于计算、查询或取得与“property”相关的操作。调用时要先确认当前状态和 `arrayIndex` 的有效范围；返回类型是 `QJSValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSValue`。
- 参数 `arrayIndex`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSManagedValue QJSManagedValue::prototype() const`

**API 类别：** 成员函数说明

**中文解读：** `QJSManagedValue::prototype` 用于计算、查询或取得与“prototype”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QJSManagedValue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSManagedValue`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QJSManagedValue::setProperty(const QString &name, const QJSValue &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setProperty`。调用它会改变 `QJSManagedValue` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `value`：类型为 `const QJSValue &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QJSManagedValue::setProperty(quint32 arrayIndex, const QJSValue &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setProperty`。调用它会改变 `QJSManagedValue` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `arrayIndex`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const QJSValue &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QJSManagedValue::setPrototype(const QJSManagedValue &prototype)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPrototype`。调用它会改变 `QJSManagedValue` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `prototype`：类型为 `const QJSManagedValue &`。没有默认值，调用时必须提供。传入 `const QJSManagedValue &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::strictlyEquals(const QJSManagedValue &other) const`

**API 类别：** 成员函数说明

**中文解读：** `QJSManagedValue::strictlyEquals` 用于计算、查询或取得与“strictly、Equals”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QJSManagedValue &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QJSManagedValue::toBoolean() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toBoolean`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QJSManagedValue::toDateTime() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toDateTime`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QJSManagedValue::toInteger() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toInteger`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSValue QJSManagedValue::toJSValue() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toJSValue`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QJSValue`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `double QJSManagedValue::toNumber() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toNumber`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`double`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSPrimitiveValue QJSManagedValue::toPrimitive() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toPrimitive`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QJSPrimitiveValue`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QMetaObject *QJSManagedValue::toQMetaObject() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toQMetaObject`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`const QMetaObject *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QObject *QJSManagedValue::toQObject() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toQObject`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QObject *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRegularExpression QJSManagedValue::toRegularExpression() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toRegularExpression`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QRegularExpression`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QJSManagedValue::toString() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toString`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QUrl QJSManagedValue::toUrl() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toUrl`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QUrl`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QJSManagedValue::toVariant() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toVariant`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QVariant`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSManagedValue::Type QJSManagedValue::type() const`

**API 类别：** 成员函数说明

**中文解读：** `QJSManagedValue::type` 用于计算、查询或取得与“类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QJSManagedValue::Type`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QJSManagedValue::Type`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QJSManagedValue &QJSManagedValue::operator=(QJSManagedValue &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QJSManagedValue` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QJSManagedValue &`。
- 参数 `other`：类型为 `QJSManagedValue &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

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

`QJSManagedValue` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
