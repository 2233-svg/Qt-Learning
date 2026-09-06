# QMetaMethod

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“MetaMethod”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMetaMethod` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QMetaMethod>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Access { Private, Protected, Public }`
- `enum MethodType { Method, Signal, Slot, Constructor }`

### 公有函数

- `QMetaMethod::Access access() const`
- `(since 6.5) bool invoke(QObject *obj, Args &&... arguments) const`
- `(since 6.5) bool invoke(QObject *obj, QTemplatedMetaMethodReturnArgument<ReturnArg> ret, Args &&... arguments) const`
- `(since 6.5) bool invoke(QObject *obj, Qt::ConnectionType type, Args &&... arguments) const`
- `(since 6.5) bool invoke(QObject *obj, Qt::ConnectionType type, QTemplatedMetaMethodReturnArgument<ReturnArg> ret, Args &&... arguments) const`
- `(since 6.5) bool invokeOnGadget(void *gadget, Args &&... arguments) const`
- `(since 6.5) bool invokeOnGadget(void *gadget, QTemplatedMetaMethodReturnArgument<ReturnArg> ret, Args &&... arguments) const`
- `(since 6.2) bool isConst() const`
- `bool isValid() const`
- `int methodIndex() const`
- `QByteArray methodSignature() const`
- `QMetaMethod::MethodType methodType() const`
- `QByteArray name() const`
- `(since 6.9) QByteArrayView nameView() const`
- `int parameterCount() const`
- `(since 6.0) QMetaType parameterMetaType(int index) const`
- `QList<QByteArray> parameterNames() const`
- `int parameterType(int index) const`
- `(since 6.0) QByteArray parameterTypeName(int index) const`
- `QList<QByteArray> parameterTypes() const`
- `(since 6.0) int relativeMethodIndex() const`
- `(since 6.0) QMetaType returnMetaType() const`
- `int returnType() const`
- `int revision() const`
- `const char * tag() const`
- `const char * typeName() const`

### 静态公有成员

- `QMetaMethod fromSignal(PointerToMemberFunction signal)`

### 相关非成员函数

- `bool operator!=(const QMetaMethod &lhs, const QMetaMethod &rhs)`
- `bool operator==(const QMetaMethod &lhs, const QMetaMethod &rhs)`

### 公开宏

- `Q_METAMETHOD_INVOKE_MAX_ARGS`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QMetaMethod::Access`

**作用与语义：**

该枚举描述方法的访问层级，遵循 C 语言中使用的惯例。
- `QMetaMethod::Private`：`0`
- `QMetaMethod::Protected`：`1`
- `QMetaMethod::Public`：`2`

### `QMetaMethod::Access QMetaMethod::access() const`

**作用与语义：**

返回该方法的访问规范（私有、受保护或公共）。
注意：信号总是公开的，但你应将其视为实现细节。几乎总是从其类别外发出信号是个坏主意。

### `[static] template <typename PointerToMemberFunction> QMetaMethod QMetaMethod::fromSignal(PointerToMemberFunction signal)`

**作用与语义：**

返回对应给定`signal`的元方法，或如果`signal`是`nullptr`或不是该类信号，则返回无效`QMetaMethod`。

**官方示例：**

```cpp
 QMetaMethod destroyedSignal = QMetaMethod::fromSignal(&QObject::destroyed);
```

### `[since 6.5] template <typename... Args> bool QMetaMethod::invoke(QObject *obj, Args &&... arguments) const`

**作用与语义：**

在对象`object`上调用此方法。返回`true`该成员是否可被调用。返回 `false` 如果没有该成员或参数不匹配。
对于带有QTemplatedMetaMethodReturnArgument参数的超载，`member`函数调用的返回值会放在`ret`中。对于没有该成员的超载，将丢弃被调用函数的返回值（如果有的话）。QTemplatedMetaMethodReturnArgument是一个内部类型，不应直接使用。相反，可以使用qReturnArg()函数。
带有`Qt::ConnectionType` `type`参数的超载允许明确选择调用是否同步：
- 如果`type` `Qt::DirectConnection`，该成员将立即在当前线程中被调用。
- 如果`type` `Qt::QueuedConnection`，应用程序进入该`obj`创建或移动的线程中的事件循环时，会发送`QEvent`并立即调用该成员。
- 如果`type` `Qt::BlockingQueuedConnection`，方法的调用方式与对`Qt::QueuedConnection`相同，但当前线程会阻塞直到事件被传递。使用这种连接类型在同一线程中的对象之间通信会导致死锁。
- 如果`type` `Qt::AutoConnection`，则如果`obj`与调用者在同一线程中，则该成员会被同步调用;否则将异步调用该成员。这就是没有`type`参数的超载的行为。
要异步调用`QPushButton`上的`animateClick()`槽：
异步方法调用中，参数必须是可复制类型，因为Qt需要复制参数以便在幕后事件中存储。自Qt 6.5起，该函数自动注册所使用的类型;但作为副作用，无法使用仅前向声明的类型进行调用。此外，也无法使用非const限定类型作为参数的异步调用。
要同步调用任意对象的`compute(QString, int, double)`槽`obj`检索其返回值：
如果“计算”槽没有按指定顺序恰好取一个`QString`、一个`int`和一个`double`，调用将失败。注意必须明确说明`QString`类型，因为字符的字面值并非完全匹配的类型。如果方法取的是`QByteArray`、`qint64`和`long double`，调用需要写成：
同样的调用也可以通过 `Q_ARG()` 和 `Q_RETURN_ARG()` 宏执行，具体如下：
警告：此方法不会检验参数的有效性：`object`必须是本`QMetaMethod`所构造`QMetaObject`类的实例。

**官方示例：**

```cpp
 int methodIndex = pushButton->metaObject()->indexOfMethod("animateClick()");
 QMetaMethod method = metaObject->method(methodIndex);
 method.invoke(pushButton, Qt::QueuedConnection);
```

### `[since 6.5] template <typename... Args> bool QMetaMethod::invokeOnGadget(void *gadget, Args &&... arguments) const`

**作用与语义：**

在`Q_GADGET`上调用此方法。返回`true`是否可以调用该成员。返回 `false` 如果没有该成员或参数不匹配。
指针`gadget`必须指向该小工具类的一个实例。
祈祷始终是同步的。
对于带有QTemplatedMetaMethodReturnArgument参数的超载，`member`函数调用的返回值放在`ret`。对于没有该参数的超载，被调用函数的返回值（如果有的话）将被丢弃。QTemplatedMetaMethodReturnArgument是一个内部类型，不应直接使用。相反，可以使用qReturnArg()函数。
警告：此方法不会测试参数的有效性：`gadget`必须是构建本`QMetaMethod`所用`QMetaObject`类的一个实例。

### `[since 6.2] bool QMetaMethod::isConst() const`

**作用与语义：**

返回方法是否符合条件条件。
注意：如果 const 方法属于基于旧版 Qt 编译的库，该方法可能会错误返回 `false`。

### `bool QMetaMethod::isValid() const`

**作用与语义：**

如果该方法有效（可内省和调用），返回 `true`，否则返回 `false`。

### `int QMetaMethod::methodIndex() const`

**作用与语义：**

返回该方法的索引。

### `QByteArray QMetaMethod::methodSignature() const`

**作用与语义：**

返回该方法的签名（例如，`setValue(double)`）。

### `QMetaMethod::MethodType QMetaMethod::methodType() const`

**作用与语义：**

返回该方法的类型（信号、槽或方法）。

### `QByteArray QMetaMethod::name() const`

**作用与语义：**

返回该方法的名称。

### `[since 6.9] QByteArrayView QMetaMethod::nameView() const`

**作用与语义：**

返回该方法的名称。返回的`QByteArrayView`只要该方法所属类的元对象有效，就有效。

### `int QMetaMethod::parameterCount() const`

**作用与语义：**

返回该方法的参数数量。

### `[since 6.0] QMetaType QMetaMethod::parameterMetaType(int index) const`

**作用与语义：**

返回给定`index`处参数的元类型。
如果`index`小于零或大于`parameterCount()`，则返回无效`QMetaType`。

### `QList<QByteArray> QMetaMethod::parameterNames() const`

**作用与语义：**

返回参数名称列表。

### `int QMetaMethod::parameterType(int index) const`

**作用与语义：**

返回给定`index`处参数的类型。
返回值是`QMetaType`注册的类型之一，如果类型未注册，则`QMetaType::UnknownType`。

### `[since 6.0] QByteArray QMetaMethod::parameterTypeName(int index) const`

**作用与语义：**

返回位置 `index` 的类型名称 如果 `index` 处无参数，返回空 `QByteArray`。

### `QList<QByteArray> QMetaMethod::parameterTypes() const`

**作用与语义：**

返回参数类型列表。

### `[since 6.0] int QMetaMethod::relativeMethodIndex() const`

**作用与语义：**

返回该方法的本地索引。

### `[since 6.0] QMetaType QMetaMethod::returnMetaType() const`

**作用与语义：**

返回该方法的返回类型。

### `int QMetaMethod::returnType() const`

**作用与语义：**

返回该方法的返回类型。
返回值是`QMetaType`注册的类型之一，如果类型未注册则`QMetaType::UnknownType`。

### `int QMetaMethod::revision() const`

**作用与语义：**

如果`Q_REVISION`指定了方法版本，则返回该版本，否则返回0。自Qt 6.0起，非零值被编码，并可用`QTypeRevision::fromEncodedVersion()`解码。

### `const char *QMetaMethod::tag() const`

**作用与语义：**

返回与该方法关联的标签。
标签是`moc`识别的特殊宏，使得添加方法的更多信息成为可能。
标签信息可以通过函数声明中以下方式添加：
信息可通过以下方式访问：
目前，`moc`会提取并记录所有标签，但不会专门处理其中任何标签。你可以用标签来对方法进行不同的注释，并根据应用的具体需求进行处理。
注意：`moc` 扩展了预处理器宏，因此定义周围必须用 `#ifndef` `Q_MOC_RUN` 包围，如上方示例所示。

**官方示例：**

```cpp
     // In the class MainWindow declaration
     #ifndef Q_MOC_RUN
     // define the tag text as empty, so the compiler doesn't see it
     #  define MY_CUSTOM_TAG
     #endif
     //...
     private slots:
         MY_CUSTOM_TAG void testFunc();
```

### `const char *QMetaMethod::typeName() const`

**作用与语义：**

返回该方法的返回类型名称。如果该方法是构造函数，该函数返回空字符串（构造函数没有返回类型）。
注意：在Qt 7中，该函数将返回构造函数的空指针。

### `[noexcept] bool operator!=(const QMetaMethod &lhs, const QMetaMethod &rhs)`

**作用与语义：**

如果方法`lhs`与方法`rhs`不等于，返回`true`，否则返回`false`。

### `[noexcept] bool operator==(const QMetaMethod &lhs, const QMetaMethod &rhs)`

**作用与语义：**

如果方法`lhs`等于方法`rhs`，返回`true`，否则返回`false`。

### `Q_METAMETHOD_INVOKE_MAX_ARGS`

**作用与语义：**

等于通过`QMetaMethod::invoke()`执行方法的最大参数数。

### `enum MethodType { Method, Signal, Slot, Constructor }`

**作用与语义：**

- `QMetaMethod::Method`：`QMETHOD_CODE`;该函数是一个普通成员函数。
- `QMetaMethod::Signal`：`1`;该功能是一个信号。
- `QMetaMethod::Slot`：`2`;功能是一个槽。
- `QMetaMethod::Constructor`：`3`;函数是一个构造函数。

### `(since 6.5) bool invoke(QObject *obj, QTemplatedMetaMethodReturnArgument<ReturnArg> ret, Args &&... arguments) const`

**作用与语义：**

在对象`object`上调用此方法。返回`true`该成员是否可被调用。返回 `false` 如果没有该成员或参数不匹配。
对于带有QTemplatedMetaMethodReturnArgument参数的超载，`member`函数调用的返回值会放在`ret`中。对于没有该成员的超载，将丢弃被调用函数的返回值（如果有的话）。QTemplatedMetaMethodReturnArgument是一个内部类型，不应直接使用。相反，可以使用qReturnArg()函数。
带有`Qt::ConnectionType` `type`参数的超载允许明确选择调用是否同步：
- 如果`type` `Qt::DirectConnection`，该成员将立即在当前线程中被调用。
- 如果`type` `Qt::QueuedConnection`，应用程序进入该`obj`创建或移动的线程中的事件循环时，会发送`QEvent`并立即调用该成员。
- 如果`type` `Qt::BlockingQueuedConnection`，方法的调用方式与对`Qt::QueuedConnection`相同，但当前线程会阻塞直到事件被传递。使用这种连接类型在同一线程中的对象之间通信会导致死锁。
- 如果`type` `Qt::AutoConnection`，则如果`obj`与调用者在同一线程中，则该成员会被同步调用;否则将异步调用该成员。这就是没有`type`参数的超载的行为。
要异步调用`QPushButton`上的`animateClick()`槽：
异步方法调用中，参数必须是可复制类型，因为Qt需要复制参数以便在幕后事件中存储。自Qt 6.5起，该函数自动注册所使用的类型;但作为副作用，无法使用仅前向声明的类型进行调用。此外，也无法使用非const限定类型作为参数的异步调用。
要同步调用任意对象的`compute(QString, int, double)`槽`obj`检索其返回值：
如果“计算”槽没有按指定顺序恰好取一个`QString`、一个`int`和一个`double`，调用将失败。注意必须明确说明`QString`类型，因为字符的字面值并非完全匹配的类型。如果方法取的是`QByteArray`、`qint64`和`long double`，调用需要写成：
同样的调用也可以通过 `Q_ARG()` 和 `Q_RETURN_ARG()` 宏执行，具体如下：
警告：此方法不会检验参数的有效性：`object`必须是本`QMetaMethod`所构造`QMetaObject`类的实例。

**官方示例：**

```cpp
 int methodIndex = pushButton->metaObject()->indexOfMethod("animateClick()");
 QMetaMethod method = metaObject->method(methodIndex);
 method.invoke(pushButton, Qt::QueuedConnection);
```

### `(since 6.5) bool invoke(QObject *obj, Qt::ConnectionType type, Args &&... arguments) const`

**作用与语义：**

在对象`object`上调用此方法。返回`true`该成员是否可被调用。返回 `false` 如果没有该成员或参数不匹配。
对于带有QTemplatedMetaMethodReturnArgument参数的超载，`member`函数调用的返回值会放在`ret`中。对于没有该成员的超载，将丢弃被调用函数的返回值（如果有的话）。QTemplatedMetaMethodReturnArgument是一个内部类型，不应直接使用。相反，可以使用qReturnArg()函数。
带有`Qt::ConnectionType` `type`参数的超载允许明确选择调用是否同步：
- 如果`type` `Qt::DirectConnection`，该成员将立即在当前线程中被调用。
- 如果`type` `Qt::QueuedConnection`，应用程序进入该`obj`创建或移动的线程中的事件循环时，会发送`QEvent`并立即调用该成员。
- 如果`type` `Qt::BlockingQueuedConnection`，方法的调用方式与对`Qt::QueuedConnection`相同，但当前线程会阻塞直到事件被传递。使用这种连接类型在同一线程中的对象之间通信会导致死锁。
- 如果`type` `Qt::AutoConnection`，则如果`obj`与调用者在同一线程中，则该成员会被同步调用;否则将异步调用该成员。这就是没有`type`参数的超载的行为。
要异步调用`QPushButton`上的`animateClick()`槽：
异步方法调用中，参数必须是可复制类型，因为Qt需要复制参数以便在幕后事件中存储。自Qt 6.5起，该函数自动注册所使用的类型;但作为副作用，无法使用仅前向声明的类型进行调用。此外，也无法使用非const限定类型作为参数的异步调用。
要同步调用任意对象的`compute(QString, int, double)`槽`obj`检索其返回值：
如果“计算”槽没有按指定顺序恰好取一个`QString`、一个`int`和一个`double`，调用将失败。注意必须明确说明`QString`类型，因为字符的字面值并非完全匹配的类型。如果方法取的是`QByteArray`、`qint64`和`long double`，调用需要写成：
同样的调用也可以通过 `Q_ARG()` 和 `Q_RETURN_ARG()` 宏执行，具体如下：
警告：此方法不会检验参数的有效性：`object`必须是本`QMetaMethod`所构造`QMetaObject`类的实例。

**官方示例：**

```cpp
 int methodIndex = pushButton->metaObject()->indexOfMethod("animateClick()");
 QMetaMethod method = metaObject->method(methodIndex);
 method.invoke(pushButton, Qt::QueuedConnection);
```

### `(since 6.5) bool invoke(QObject *obj, Qt::ConnectionType type, QTemplatedMetaMethodReturnArgument<ReturnArg> ret, Args &&... arguments) const`

**作用与语义：**

在对象`object`上调用此方法。返回`true`该成员是否可被调用。返回 `false` 如果没有该成员或参数不匹配。
对于带有QTemplatedMetaMethodReturnArgument参数的超载，`member`函数调用的返回值会放在`ret`中。对于没有该成员的超载，将丢弃被调用函数的返回值（如果有的话）。QTemplatedMetaMethodReturnArgument是一个内部类型，不应直接使用。相反，可以使用qReturnArg()函数。
带有`Qt::ConnectionType` `type`参数的超载允许明确选择调用是否同步：
- 如果`type` `Qt::DirectConnection`，该成员将立即在当前线程中被调用。
- 如果`type` `Qt::QueuedConnection`，应用程序进入该`obj`创建或移动的线程中的事件循环时，会发送`QEvent`并立即调用该成员。
- 如果`type` `Qt::BlockingQueuedConnection`，方法的调用方式与对`Qt::QueuedConnection`相同，但当前线程会阻塞直到事件被传递。使用这种连接类型在同一线程中的对象之间通信会导致死锁。
- 如果`type` `Qt::AutoConnection`，则如果`obj`与调用者在同一线程中，则该成员会被同步调用;否则将异步调用该成员。这就是没有`type`参数的超载的行为。
要异步调用`QPushButton`上的`animateClick()`槽：
异步方法调用中，参数必须是可复制类型，因为Qt需要复制参数以便在幕后事件中存储。自Qt 6.5起，该函数自动注册所使用的类型;但作为副作用，无法使用仅前向声明的类型进行调用。此外，也无法使用非const限定类型作为参数的异步调用。
要同步调用任意对象的`compute(QString, int, double)`槽`obj`检索其返回值：
如果“计算”槽没有按指定顺序恰好取一个`QString`、一个`int`和一个`double`，调用将失败。注意必须明确说明`QString`类型，因为字符的字面值并非完全匹配的类型。如果方法取的是`QByteArray`、`qint64`和`long double`，调用需要写成：
同样的调用也可以通过 `Q_ARG()` 和 `Q_RETURN_ARG()` 宏执行，具体如下：
警告：此方法不会检验参数的有效性：`object`必须是本`QMetaMethod`所构造`QMetaObject`类的实例。

**官方示例：**

```cpp
 int methodIndex = pushButton->metaObject()->indexOfMethod("animateClick()");
 QMetaMethod method = metaObject->method(methodIndex);
 method.invoke(pushButton, Qt::QueuedConnection);
```

### `(since 6.5) bool invokeOnGadget(void *gadget, QTemplatedMetaMethodReturnArgument<ReturnArg> ret, Args &&... arguments) const`

**作用与语义：**

在`Q_GADGET`上调用此方法。返回`true`是否可以调用该成员。返回 `false` 如果没有该成员或参数不匹配。
指针`gadget`必须指向该小工具类的一个实例。
祈祷始终是同步的。
对于带有QTemplatedMetaMethodReturnArgument参数的超载，`member`函数调用的返回值放在`ret`。对于没有该参数的超载，被调用函数的返回值（如果有的话）将被丢弃。QTemplatedMetaMethodReturnArgument是一个内部类型，不应直接使用。相反，可以使用qReturnArg()函数。
警告：此方法不会测试参数的有效性：`gadget`必须是构建本`QMetaMethod`所用`QMetaObject`类的一个实例。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QMetaMethod` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
