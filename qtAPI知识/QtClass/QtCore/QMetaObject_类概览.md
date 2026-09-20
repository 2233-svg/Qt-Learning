# Qt QMetaObject 元对象查找、调用与继承索引笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMetaObject>`  
> 所属模块：`Qt6::Core`  
> 类型性质：由 moc 生成的类型级反射描述表  
> 相关类型：`QObject`、`QMetaMethod`、`QMetaProperty`、`QMetaEnum`、`QMetaClassInfo`、`QMetaType`

## 1. 它解决什么问题

`QMetaObject` 是 Qt 反射体系的总入口。对于一个使用 `Q_OBJECT`、`Q_GADGET` 或 `Q_NAMESPACE` 的类型，它保存并暴露：

- 类名、父类元对象和继承关系；
- methods、signals、slots、constructors；
- properties；
- enums/flags；
- `Q_CLASSINFO` 类信息；
- 按名称查找和按索引读取这些描述；
- 动态调用、动态构造、信号连接和自动连接；
- 类型规范化、连接参数检查和翻译入口。

它解决的是“运行时只拿到一个对象或类型名，仍然需要了解其结构并操作它”的问题。`QMetaObject` 不保存普通对象的全部运行时状态，也不是 C++ RTTI 的完全替代；它只包含 Qt 元对象宏和 moc 生成的那部分信息。

## 2. 实际使用场景

### 2.1 枚举、属性和方法检查器

```cpp
void inspectObject(QObject *object)
{
    const QMetaObject *meta = object->metaObject();

    qDebug() << meta->className();

    for (int i = 0; i < meta->propertyCount(); ++i) {
        const QMetaProperty property = meta->property(i);
        qDebug() << property.name()
                 << property.typeName();
    }

    for (int i = 0; i < meta->methodCount(); ++i) {
        const QMetaMethod method = meta->method(i);
        qDebug() << method.methodSignature();
    }
}
```

`propertyCount()`、`methodCount()` 等通常包含基类可见条目；只遍历当前类新增部分时要使用相应的 `Offset()`。

### 2.2 按名称动态调用

```cpp
QString result;
const bool accepted =
    QMetaObject::invokeMethod(
        object,
        "refresh",
        Qt::DirectConnection,
        qReturnArg(result));
```

上例假定元对象中存在一个返回 `QString` 的 `refresh()` 方法。字符串形式适合方法名来自配置、插件协议或脚本的场景，但它失去编译期拼写和参数检查。能在编译期表达目标时，优先使用成员函数指针或 functor 形式。

### 2.3 跨线程投递任务

```cpp
QMetaObject::invokeMethod(
    worker,
    [worker] {
        worker->reload();
    },
    Qt::QueuedConnection);
```

functor 形式由编译器检查调用签名，更适合 Qt 6.7 及以后代码。`QueuedConnection` 仍然依赖 worker 所在线程的事件循环。

### 2.4 从元对象构造 QObject

```cpp
const QMetaObject *meta = Widget::staticMetaObject;
QObject *object = meta->newInstance(QStringLiteral("preview"));
if (!object) {
    // 没有匹配的 Q_INVOKABLE 构造函数，或参数类型不匹配。
}
```

只有被 moc 记录为可调用的构造函数才能通过 `newInstance()` 使用。普通 public 构造函数不会自动进入元对象。

## 3. 元对象从哪里来

### 3.1 `Q_OBJECT`

```cpp
class Panel : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString title READ title WRITE setTitle)
public:
    Q_INVOKABLE explicit Panel(const QString &title);
};
```

`Q_OBJECT` 让 moc 生成 QObject 元对象、信号槽和属性等信息。构建系统必须实际运行 moc；只写宏而没有 moc 生成代码会导致链接或反射行为异常。

### 3.2 `Q_GADGET`

`Q_GADGET` 为非 QObject 类型提供静态元对象，可包含枚举、属性和 invokable 方法，但没有对象树、线程归属、信号槽和 `QObject *` 生命周期。gadget 使用 `Type::staticMetaObject`，不能当作 QObject 使用。

### 3.3 `Q_NAMESPACE`

命名空间可以通过 `Q_NAMESPACE` 生成静态元对象，配合 `Q_ENUM_NS`、`Q_FLAG_NS` 等暴露命名空间枚举。命名空间没有实例，通常只通过静态元对象访问。

## 4. `staticMetaObject`、`metaObject()` 与 `QMetaObject`

### 4.1 静态元对象

```cpp
const QMetaObject &staticMeta = Panel::staticMetaObject;
```

它描述编译期类型本身，生命周期通常覆盖类型所在模块。

### 4.2 动态对象元对象

```cpp
const QMetaObject *dynamicMeta = object->metaObject();
```

对普通 QObject，它通常是最派生动态类型的元对象；动态元对象系统（例如某些 QML/插件场景）可能提供额外层级。读取属性或方法时要明确是要“静态类型”还是“对象实际动态类型”。

### 4.3 元对象是描述，不是对象

```cpp
QMetaObject meta = *object->metaObject(); // 通常不这样做
```

`QMetaObject` 的数据由 moc 生成并以描述表形式存在。业务代码通常保存 `const QMetaObject *` 或引用，不需要复制它；复制也不会复制 QObject、属性值或方法实现。

## 5. 继承、计数和 offset

每类元对象的总表通常由基类部分和当前类新增部分组成：

```text
[基类 methods/properties/enums/classinfo]
[当前类新增 methods/properties/enums/classinfo]
```

对应规则：

- `methodCount()`：可见方法总数；
- `methodOffset()`：当前类新增方法起点；
- `propertyCount()`：可见属性总数；
- `propertyOffset()`：当前类新增属性起点；
- `enumeratorCount()` / `enumeratorOffset()`：枚举同理；
- `classInfoCount()` / `classInfoOffset()`：类信息同理；
- `constructorCount()`：元对象构造函数数量，构造函数不继承。

只遍历当前类：

```cpp
for (int i = meta->methodOffset();
     i < meta->methodCount(); ++i) {
    const QMetaMethod method = meta->method(i);
}
```

遍历全部可见方法则从 0 开始。`relativeMethodIndex()`、`relativePropertyIndex()` 等相对索引必须与对应类的 offset 配套，不能直接当作全局索引。

## 6. 查找 API 的索引契约

所有 `indexOf...()` 函数都可能返回负值表示找不到。正确模式：

```cpp
const int index = meta->indexOfProperty("title");
if (index < 0)
    return;

const QMetaProperty property = meta->property(index);
```

名称比较通常要求规范化签名或精确属性名：

- method/signal/slot/constructor 用带参数列表的签名；
- property、enum、class info 用名称；
- `indexOfSignal()` 和 `indexOfSlot()` 限制搜索的方法类别；
- `indexOfMethod()` 搜索更广的元方法集合。

## 7. 动态调用的三种形式

### 7.1 字符串方法名

```cpp
QMetaObject::invokeMethod(
    object,
    "setValue",
    Qt::DirectConnection,
    42);
```

Qt 6.5 起模板参数会从实参推断类型。方法名是裸 `const char *`，不需要把参数签名写进 member 字符串；若要查找索引或使用旧式 API，才使用完整 normalized signature。

### 7.2 成员函数指针

```cpp
QMetaObject::invokeMethod(
    object,
    &Panel::reload,
    Qt::QueuedConnection);
```

Qt 6.7 起支持更完整的 functor/member pointer 参数形式。编译器可以检查对象类型、参数数量和返回类型，优先级高于字符串形式。

### 7.3 functor/lambda

```cpp
QMetaObject::invokeMethod(
    object,
    [path = QStringLiteral("config.json")] {
        qDebug() << path;
    },
    Qt::QueuedConnection);
```

functor 会被包装并按连接类型执行。queued 调用会复制可捕获状态；捕获裸指针时仍需保证目标对象在执行时存活，常用 context/object 作为生命周期锚点。

## 8. `invokeMethod()` 的连接类型边界

### 8.1 `AutoConnection`

省略连接类型时使用。调用发生在当前线程还是目标对象线程，取决于对象线程归属和当前执行线程。

### 8.2 `DirectConnection`

立即在当前线程执行。它不会把调用切换到 object 所在线程，不能用来“安全地跨线程调用 QObject”。

### 8.3 `QueuedConnection`

把调用投递到目标线程事件循环，当前函数立即返回。参数必须可复制且能被 Qt 元类型系统处理；目标线程没有事件循环时不会按预期执行。

### 8.4 `BlockingQueuedConnection`

投递到目标线程并等待完成。当前线程和目标线程相同时会死锁；跨线程使用时要确保目标事件循环可运行。

### 8.5 `invokeMethod()` 返回值

`bool` 表示请求是否被 Qt 接受或投递，不是被调用方法自己的返回值。同步调用可以配合 `qReturnArg()` 或返回值指针捕获业务结果；queued 调用不要把返回结果写到即将离开作用域的局部变量。

## 9. 参数、返回值和旧式宏

### 9.1 模板化参数

```cpp
QString result;
const bool ok = QMetaObject::invokeMethod(
    object,
    "compute",
    Qt::DirectConnection,
    qReturnArg(result),
    QStringLiteral("sqrt"),
    42,
    9.7);
```

参数类型必须与目标元方法兼容。字符串形式在运行时查找 method，模板只负责把参数包装成 Qt 元类型描述。

### 9.2 `Q_ARG` 与 `Q_RETURN_ARG`

```cpp
QString result;
QMetaObject::invokeMethod(
    object,
    "compute",
    Qt::DirectConnection,
    Q_RETURN_ARG(QString, result),
    Q_ARG(QString, "sqrt"),
    Q_ARG(int, 42),
    Q_ARG(double, 9.7));
```

这是 Qt 6.5 以前常见的旧式 API，Qt 6.11 仍保留兼容入口。宏里的类型名必须和元对象记录的类型名兼容；不要把它们与新式模板参数混用。

### 9.3 队列参数注册

跨线程 queued 调用自定义类型时，应确保类型可以被 Qt 构造、复制并销毁，通常需要 `Q_DECLARE_METATYPE` 和 `qRegisterMetaType<T>()`。传入裸 `const char *` 也不会自动复制其指向的外部字符存储，异步场景应传 `QString`/`QByteArray` 等拥有型对象。

## 10. 动态构造 `newInstance()`

### 10.1 构造函数必须进入元对象

```cpp
class Job : public QObject
{
    Q_OBJECT
public:
    Q_INVOKABLE explicit Job(int priority);
};

QObject *job =
    Job::staticMetaObject.newInstance(5);
```

Qt 6.5 起提供模板化调用。只有 `Q_INVOKABLE` 或适用的元对象构造记录才会被找到；普通 C++ 构造函数不会自动反射。

### 10.2 返回空指针的情况

`newInstance()` 找不到匹配构造函数、参数类型不匹配、返回类型不适合 QObject 或调用失败时返回 `nullptr`。调用方负责确认返回对象的所有权；由 `newInstance()` 创建的 QObject 通常应设置父对象或使用明确的智能指针/对象树管理。

### 10.3 构造函数与继承

构造函数不从基类继承。`constructorCount()` 和 `constructor(index)` 只描述当前元对象登记的构造记录。

## 11. 连接与自动连接

### 11.1 `checkConnectArgs()`

```cpp
if (!QMetaObject::checkConnectArgs(
        "valueChanged(int)", "setValue(int)")) {
    // 参数不兼容
}
```

它检查信号到方法的参数兼容性，不会建立连接，也不检查对象是否存活、线程是否正确或业务逻辑是否安全。

### 11.2 按 `QMetaMethod` 连接

```cpp
const QMetaMethod signal =
    sender->metaObject()->method(signalIndex);

const QMetaObject::Connection connection =
    QMetaObject::connect(sender, signal,
                         receiver, &Receiver::onValueChanged);
```

Qt 6.10 起可用的该入口适合已有元方法句柄的框架。回调有 context 时，context 销毁会自动清理连接；连接返回的句柄不应被误解为自动断开 guard。

### 11.3 `connectSlotsByName()`

```cpp
QMetaObject::connectSlotsByName(this);
```

它按对象名和槽名约定查找并连接：

```cpp
void on_<objectName>_<signalName>(<signal parameters>);
```

例如 objectName 为 `button1`、signal 为 `clicked()` 时，槽名是 `on_button1_clicked()`。它依赖命名、签名和 moc 元数据；重命名对象或信号后可能导致自动连接失效。Qt Designer 生成的 UI 通常会调用它。

## 12. 方法、属性、枚举和类信息访问

### 12.1 方法

```cpp
for (int i = 0; i < meta->methodCount(); ++i) {
    const QMetaMethod method = meta->method(i);
    if (method.methodType() == QMetaMethod::Signal)
        qDebug() << method.methodSignature();
}
```

method 句柄不拥有 object，字符串视图也不能跨元对象所属模块的生命周期保存。

### 12.2 属性

```cpp
const int index = meta->indexOfProperty("objectName");
if (index >= 0) {
    const QMetaProperty property = meta->property(index);
    const QVariant value = property.read(object);
}
```

属性读写要使用正确的 object 类型，并检查 `isReadable()`、`isWritable()` 和返回值。

### 12.3 枚举

```cpp
const int index = meta->indexOfEnumerator("State");
if (index >= 0) {
    const QMetaEnum enumeration = meta->enumerator(index);
}
```

`QMetaEnum` 负责 key/value 转换；`QMetaObject` 只负责枚举描述的发现和索引。

### 12.4 类信息

```cpp
const int index = meta->indexOfClassInfo("protocol");
if (index >= 0) {
    const QMetaClassInfo info = meta->classInfo(index);
}
```

类信息来自 `Q_CLASSINFO`，是静态文本，不是可修改运行时字典。

## 13. 类型、名称和翻译

### 13.1 `className()`

返回元对象记录的类名。它是元对象字符串，不是 C++ RTTI 的 `typeid(T).name()`，也不一定包含完整命名空间显示形式。

### 13.2 `metaType()`

Qt 6.2 起返回该元对象对应类型的 `QMetaType`。对于 QObject、gadget 等可注册类型，它可以用于类型比较、创建和反射能力查询；若元对象没有对应类型信息，返回的 `QMetaType` 可能无效。

### 13.3 `tr()`

在启用翻译功能时，使用该元对象所属类的上下文翻译字符串：

```cpp
const QString text =
    Widget::staticMetaObject.tr("Open");
```

它依赖翻译器和上下文名称，不是任意类的全局翻译函数。`QT_NO_TRANSLATION` 构建配置下该接口可能不可用。

### 13.4 `normalizedSignature()` 与 `normalizedType()`

```cpp
const QByteArray signature =
    QMetaObject::normalizedSignature(
        "compute( const QString &, int )");

const QByteArray type =
    QMetaObject::normalizedType(" int    const  *");
```

规范化用于稳定查找和比较签名。它不会验证类型是否已注册，也不会检查某个方法是否存在；仍需调用 `indexOfMethod()` 或 `QMetaType` API。

## 14. 内部低层入口

### 14.1 `static_metacall()` 与 `metacall()`

`static_metacall()`、`metacall()` 和 `Call` 枚举是 moc 生成代码、Qt 元对象运行时和动态元对象实现使用的低层调用协议。它们涉及 `void **` 参数数组、内部索引和属性/方法操作码。

普通应用不应手工调用它们，也不应伪造 `void **` 参数布局。需要动态调用时使用 `invokeMethod()`、`QMetaMethod::invoke()`、`QMetaProperty::read/write()` 等公开 API。

### 14.2 `activate()`

`activate()` 是信号激活的内部索引入口，供 moc 生成的 signal 实现调用。它不是“手工发射任意 signal”的公开业务 API。手写调用可能破坏参数布局、信号索引和线程连接状态。

## 15. 逐项 API 说明

### 15.1 `className() const`

```cpp
const char *className() const;
```

返回元对象中的类名。返回指针由元对象拥有；需要跨插件卸载保存时复制为 `QByteArray`。

### 15.2 `superClass() const`

```cpp
const QMetaObject *superClass() const;
```

返回直接基类元对象；根元对象可能返回 `nullptr`。沿此指针可遍历元对象继承链。

### 15.3 `inherits(const QMetaObject *) const`

```cpp
bool inherits(const QMetaObject *metaObject) const noexcept;
```

判断当前元对象是否属于指定元对象类型或其派生层级。传入空指针没有业务意义；它是 Qt 元对象继承判断，不是 C++ 任意类型转换。

### 15.4 `cast(QObject *) const`

```cpp
QObject *cast(QObject *object) const;
const QObject *cast(const QObject *object) const;
```

如果 object 的动态类型继承自当前元对象，返回转换后的 QObject 指针，否则返回 `nullptr`。它只适用于 QObject 元对象，不会把 gadget 转换成 QObject。

### 15.5 `tr(const char *, const char *, int) const`

```cpp
QString tr(const char *sourceText,
           const char *disambiguation,
           int n = -1) const;
```

以当前元对象的类名作为翻译上下文。`disambiguation` 用于区分同一源文本的不同含义，`n` 用于复数形式。翻译器安装和上下文匹配由应用负责。

### 15.6 `metaType() const`

```cpp
QMetaType metaType() const;
```

Qt 6.2 起返回该元对象对应的 `QMetaType`。无有效注册信息时可能是 invalid。

### 15.7 offset 与 count

```cpp
int methodOffset() const;
int enumeratorOffset() const;
int propertyOffset() const;
int classInfoOffset() const;

int constructorCount() const;
int methodCount() const;
int enumeratorCount() const;
int propertyCount() const;
int classInfoCount() const;
```

`Count()` 描述可访问总数，`Offset()` 描述当前类新增项目的起点；构造函数不继承，通常没有可用于继承遍历的 constructor offset。

### 15.8 index 查找函数

```cpp
int indexOfConstructor(const char *constructor) const;
int indexOfMethod(const char *method) const;
int indexOfSignal(const char *signal) const;
int indexOfSlot(const char *slot) const;
int indexOfEnumerator(const char *name) const;
int indexOfProperty(const char *name) const;
int indexOfClassInfo(const char *name) const;
```

找到时返回非负索引，找不到返回负值。方法类查找通常需要完整签名，例如 `"setValue(int)"`；调用前先做索引合法性检查。

### 15.9 `constructor(int) const`

```cpp
QMetaMethod constructor(int index) const;
```

按索引返回元构造函数描述。索引必须在 `0 <= index < constructorCount()` 范围内；无效索引产生无效方法句柄。

### 15.10 `method(int) const`

```cpp
QMetaMethod method(int index) const;
```

按全局方法索引返回 `QMetaMethod`。该句柄可用于检查、连接或 invoke；不要把相对方法索引直接传入。

### 15.11 `enumerator(int) const`

```cpp
QMetaEnum enumerator(int index) const;
```

按索引取得枚举描述。字符串 key/value 转换由返回的 `QMetaEnum` 完成。

### 15.12 `property(int) const`

```cpp
QMetaProperty property(int index) const;
```

按全局属性索引取得 `QMetaProperty`。属性读写需要再传入目标 QObject/gadget。

### 15.13 `classInfo(int) const`

```cpp
QMetaClassInfo classInfo(int index) const;
```

按索引取得 `Q_CLASSINFO` 条目。返回句柄不拥有 name/value 字符串。

### 15.14 `userProperty() const`

```cpp
QMetaProperty userProperty() const;
```

返回元对象标记为 user property 的属性；没有时返回无效属性。它常供表单或设计器选择默认编辑字段，不代表业务上的“主属性”。

### 15.15 `checkConnectArgs()` 两个重载

```cpp
static bool checkConnectArgs(
    const char *signal, const char *method);

static bool checkConnectArgs(
    const QMetaMethod &signal,
    const QMetaMethod &method);
```

检查 signal 的参数是否能传给目标 method。字符串重载要求签名格式正确；方法重载要求句柄有效。该函数不创建连接，也不检查线程和对象生命周期。

### 15.16 `connect()` 的 `QMetaMethod`/functor 重载

```cpp
template <typename Func>
static QMetaObject::Connection connect(
    const QObject *sender,
    const QMetaMethod &signal,
    const QObject *context,
    Func &&slot,
    Qt::ConnectionType type = Qt::AutoConnection);
```

Qt 6.10 起，按已有 `QMetaMethod` 连接成员函数或 functor。context 用于生命周期管理和 queued 调度；返回连接句柄，句柄析构不会自动断开。

### 15.17 `connectSlotsByName(QObject *)`

```cpp
static void connectSlotsByName(QObject *object);
```

按照 `on_<objectName>_<signalName>(...)` 命名约定建立自动连接。它不返回连接列表，调试自动连接问题时检查 objectName、槽签名、moc 和重复调用。

### 15.18 `invokeMethod()` 字符串重载

Qt 6.5 起的核心形式：

```cpp
template <typename... Args>
static bool invokeMethod(
    QObject *object,
    const char *member,
    Qt::ConnectionType type,
    Args &&... args);

template <typename ReturnArg, typename... Args>
static bool invokeMethod(
    QObject *object,
    const char *member,
    Qt::ConnectionType type,
    QTemplatedMetaMethodReturnArgument<ReturnArg> ret,
    Args &&... args);
```

省略 connection type 时使用 AutoConnection；省略返回参数时表示不关心返回值。`member` 只写方法名，不写参数列表。目标方法必须是元对象中的 method/signal/slot/可调用构造以外的 QObject 方法。

### 15.19 `invokeMethod()` functor/member pointer 重载

Qt 6.7 起支持：

```cpp
template <typename Func, typename... Args>
static bool invokeMethod(
    QObject *context,
    Func &&function,
    Qt::ConnectionType type,
    Args &&... args);
```

还提供带 `qReturnArg()` 或返回值指针的变体。成员函数指针和 lambda 的参数在编译期检查；context 决定调用线程和生命周期。对于 queued functor，捕获内容必须可安全复制到事件队列。

### 15.20 `newInstance(Args &&...) const`

```cpp
template <typename... Args>
QObject *newInstance(Args &&... arguments) const;
```

Qt 6.5 起按元对象中的构造记录创建 QObject。构造函数需要被 moc 收集，找不到匹配项返回 `nullptr`。创建后应立即设置父对象或交给明确的所有权管理。

### 15.21 `normalizedSignature(const char *)`

```cpp
static QByteArray normalizedSignature(const char *method);
```

规范化方法签名的空格、引用和类型书写，返回拥有型 `QByteArray`。它不查找方法，也不验证签名语义。

### 15.22 `normalizedType(const char *)`

```cpp
static QByteArray normalizedType(const char *type);
```

规范化类型文本，例如把多余空格整理成稳定形式。它不负责注册类型，也不保证字符串可用于 queued 调用。

### 15.23 `Q_ARG(Type, value)`

```cpp
QMetaMethodArgument Q_ARG(Type, const Type &value);
```

构造旧式动态调用参数描述。它保存传入值地址和类型名，调用期间值必须保持有效；queued 场景还必须满足参数复制/注册要求。

### 15.24 `Q_RETURN_ARG(Type, value)`

```cpp
QMetaMethodReturnArgument Q_RETURN_ARG(Type, Type &value);
```

构造旧式返回值存储描述。它指向调用方变量；只适合同步或阻塞调用，不能让 queued 调用写入已离开作用域的变量。

### 15.25 `activate()` 与 `Call`

```cpp
static void activate(QObject *sender, ...);
enum Call { InvokeMetaMethod, ReadProperty, ... };
```

这些是 moc/Qt 内部元调用协议。普通业务代码不要手工调用，也不要构造 `void **` 参数数组；应使用公开的 invoke、property 和 signal API。

## 16. 常见错误

### 16.1 把 count 当成当前类自己的数量

**症状：** 遍历子类属性时重复处理基类属性。

**原因：** `propertyCount()` 通常包含继承属性。

**修复：** 只处理当前类时从 `propertyOffset()` 开始；其他 method/enum/class info 同理。

### 16.2 忽略查找失败的负索引

**症状：** `method(-1)` 或 `property(-1)` 产生无效句柄后仍被调用。

**原因：** `indexOf...()` 的失败哨兵是负值。

**修复：** 先检查索引，再取得对应描述。

### 16.3 把字符串 `invokeMethod` 当作普通函数调用

**症状：** 方法找不到、返回 false 或参数不匹配。

**原因：** 目标没有进入元对象、member 名称拼写错误、参数类型不兼容或使用了错误连接类型。

**修复：** 能用成员函数指针/functor 时优先使用；字符串场景先检查 moc 和签名。

### 16.4 用 `DirectConnection` 跨线程碰 QObject

**症状：** 数据竞争、GUI 崩溃或对象状态损坏。

**原因：** DirectConnection 在当前线程执行，不会自动切换到对象线程。

**修复：** 使用 Auto/Queued，或提供明确锁和线程协议。

### 16.5 queued 调用携带不可复制参数

**症状：** invokeMethod 返回 false，或运行时报告无法排队参数。

**原因：** 参数类型未注册或不能复制。

**修复：** 使用拥有型 Qt 类型，注册自定义类型，并让线程事件循环运行。

### 16.6 误以为 `Connection` 是 scope guard

**症状：** 覆盖或析构句柄后旧回调仍然存在。

**原因：** 连接句柄析构不自动断开。

**修复：** 显式 `QObject::disconnect()` 或使用单独的 RAII wrapper。

### 16.7 用 `QMetaObject` 复制对象或属性

**症状：** 希望修改复制后的元对象来改变类型行为。

**原因：** 元对象是静态/动态描述表，不是运行时类型实例。

**修复：** 使用 `QMetaObjectBuilder` 等明确的动态元对象机制，且理解其生命周期；普通业务不应直接修改 moc 数据。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `className()` | 返回元对象类名 | 返回非拥有字符串，必要时复制 |
| `superClass()` | 返回直接基类元对象 | 根元对象可能为空 |
| `inherits(metaObject)` | 判断元对象继承关系 | 不是任意 C++ 类型转换 |
| `cast(QObject *)` | 按元对象类型安全转换 QObject | 不适用于 gadget |
| `tr()` | 以类名为上下文翻译文本 | 依赖翻译器和构建配置 |
| `metaType()` | 返回对应 `QMetaType` | Qt 6.2 起；可能 invalid |
| `methodOffset()`/`methodCount()` | 当前类 method 起点/总数 | count 含继承部分 |
| `enumeratorOffset()`/`enumeratorCount()` | 当前类 enum 起点/总数 | 与 `enumerator(index)` 配套 |
| `propertyOffset()`/`propertyCount()` | 当前类 property 起点/总数 | count 含继承部分 |
| `classInfoOffset()`/`classInfoCount()` | 当前类 class info 起点/总数 | 继承遍历需沿 superClass |
| `constructorCount()` | 元构造函数数量 | 构造函数不继承 |
| `indexOfConstructor()` | 按签名查构造函数 | 找不到返回负值 |
| `indexOfMethod()` | 按完整方法签名查方法 | 建议先规范化签名 |
| `indexOfSignal()` | 按签名查 signal | 只搜索 signal |
| `indexOfSlot()` | 按签名查 slot | 只搜索 slot |
| `indexOfEnumerator()` | 按名称查 enum/flags | 找不到返回负值 |
| `indexOfProperty()` | 按名称查属性 | 找不到返回负值 |
| `indexOfClassInfo()` | 按名称查 Q_CLASSINFO | 找不到返回负值 |
| `constructor(index)` | 取得构造方法描述 | 验证索引范围 |
| `method(index)` | 取得 `QMetaMethod` | 使用全局索引 |
| `enumerator(index)` | 取得 `QMetaEnum` | key/value 转换由它完成 |
| `property(index)` | 取得 `QMetaProperty` | 读写还需目标实例 |
| `classInfo(index)` | 取得 `QMetaClassInfo` | name/value 非拥有 |
| `userProperty()` | 取得 user property | 没有时返回无效 property |
| `checkConnectArgs()` | 检查信号/方法参数兼容性 | 不建立连接，不检查线程 |
| `connect(sender, signal, context, slot, type)` | 按 `QMetaMethod` 建立连接 | Qt 6.10 起；保存句柄需显式断开 |
| `connectSlotsByName(object)` | 按命名规则自动连接槽 | 依赖 objectName、签名和 moc |
| `invokeMethod(object, member, ...)` | 按字符串动态调用 | Qt 6.5 起模板化；参数/线程需匹配 |
| `invokeMethod(context, functor, ...)` | 调用成员指针或 functor | Qt 6.7 起丰富重载；queued 捕获需可复制 |
| `newInstance(args...)` | 调用元对象构造函数创建 QObject | Qt 6.5 起；没有匹配构造返回 nullptr |
| `normalizedSignature()` | 规范化完整方法签名 | 不查找、不注册类型 |
| `normalizedType()` | 规范化类型文本 | 不等于类型已注册 |
| `Q_ARG(Type, value)` | 旧式动态调用参数包装 | 值和类型名需在调用期间有效 |
| `Q_RETURN_ARG(Type, value)` | 旧式动态调用返回值包装 | 不用于悬空的 queued 返回存储 |
| `activate()`/`Call` | moc 低层信号/元调用协议 | 普通业务不要手工调用 |

## 18. 推荐模板

### 18.1 只读取当前类新增方法

```cpp
QList<QByteArray> ownMethodSignatures(const QMetaObject &meta)
{
    QList<QByteArray> result;
    for (int i = meta.methodOffset();
         i < meta.methodCount(); ++i) {
        result.append(meta.method(i).methodSignature());
    }
    return result;
}
```

### 18.2 可靠的字符串调用

```cpp
bool invokeRefresh(QObject *object)
{
    if (!object)
        return false;

    const QMetaObject *meta = object->metaObject();
    const int index = meta->indexOfMethod("refresh()");
    if (index < 0)
        return false;

    const QMetaMethod method = meta->method(index);
    if (!method.isValid())
        return false;

    return method.invoke(object, Qt::QueuedConnection);
}
```

### 18.3 使用 functor 投递拥有型数据

```cpp
void postText(QObject *context, QString text)
{
    QMetaObject::invokeMethod(
        context,
        [text = std::move(text)] {
            qDebug() << text;
        },
        Qt::QueuedConnection);
}
```

捕获 `QString` 等拥有型值可以避免 queued 调用依赖调用者局部缓冲区。context 被销毁时，待执行回调也会按 Qt 的对象生命周期规则清理。

## 19. 一句话总结

`QMetaObject` 是 Qt 元对象系统的总目录和调度入口：它用 count/offset 管理继承层级，用 index 查找 methods、properties、enums 和 class info，用 `invokeMethod()`/`newInstance()`/连接 API 把描述转成运行时动作；使用时最重要的是检查负索引、区分全局索引和相对索引、正确选择线程连接类型，并把 `activate()` 等 moc 内部协议留给 Qt 自己。
