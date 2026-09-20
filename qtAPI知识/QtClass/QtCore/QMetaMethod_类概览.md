# Qt QMetaMethod 元对象方法描述与动态调用笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMetaMethod>`  
> 所属模块：`Qt6::Core`  
> 类型性质：`QMetaObject` 中一条方法、信号、槽或构造函数记录的轻量句柄  
> 相关类型：`QMetaObject`、`QObject`、`Q_GADGET`、`Qt::ConnectionType`、`QMetaType`

## 1. 它解决什么问题

普通 C++ 调用在编译期就确定了函数名、参数类型和目标对象。Qt 的元对象系统还需要支持运行时工具和框架完成这些事情：

- 按签名查找信号、槽或普通方法；
- 判断一个方法是 signal、slot、普通 method 还是 constructor；
- 查看参数名称、参数类型、返回类型、访问级别和 revision；
- 根据成员函数指针取得信号描述；
- 在运行时调用 `QObject` 方法或 `Q_GADGET` 方法；
- 让 Designer、QML、脚本桥接、自动化测试和插件框架不依赖具体 C++ 调用点。

`QMetaMethod` 就是这些元数据的轻量句柄。它不拥有目标对象，也不把方法复制成一个可独立执行的函数对象；它只是引用某个 `QMetaObject` 中的方法记录，真正执行时仍需要传入 `QObject *` 或 gadget 地址。

## 2. 实际使用场景

### 2.1 按签名查找并异步调用槽

```cpp
const QMetaObject *meta = button->metaObject();
const int index = meta->indexOfMethod("animateClick()");
if (index >= 0) {
    const QMetaMethod method = meta->method(index);
    const bool accepted =
        method.invoke(button, Qt::QueuedConnection);
    Q_ASSERT(accepted);
}
```

`Qt::QueuedConnection` 只把调用投递到目标对象所属线程的事件循环，方法不会在当前调用栈中立即执行。目标线程必须有正在运行的事件循环；否则调用可能一直等不到执行。

### 2.2 运行时调用带参数并取得返回值

```cpp
class Calculator : public QObject
{
    Q_OBJECT
public slots:
    QString format(int value, double scale) const
    {
        return QString::number(value * scale, 'f', 2);
    }
};

Calculator calculator;
const QMetaMethod method =
    calculator.metaObject()->method(
        calculator.metaObject()->indexOfMethod(
            "format(int,double)"));

QString result;
const bool accepted =
    method.invoke(&calculator,
                  Qt::DirectConnection,
                  qReturnArg(result),
                  12,
                  1.5);
```

动态调用按元对象记录的参数类型匹配。`result` 的类型必须与元方法返回类型兼容；返回值捕获只适合同步执行，队列调用不能把稍后才产生的结果写回当前栈上的局部变量。

### 2.3 由信号成员函数指针取得方法

```cpp
const QMetaMethod destroyed =
    QMetaMethod::fromSignal(&QObject::destroyed);
Q_ASSERT(destroyed.methodType() == QMetaMethod::Signal);
```

这种方式避免手写 `"destroyed(QObject*)"` 字符串，适合通用连接、信号分类和元对象工具。成员函数指针必须属于带 `Q_OBJECT` 的类型，并且确实指向 signal。

### 2.4 调用 `Q_GADGET` 的静态元方法

```cpp
class Converter
{
    Q_GADGET
public:
    Q_INVOKABLE int toCelsius(int fahrenheit) const
    {
        return (fahrenheit - 32) * 5 / 9;
    }
};

Converter converter;
const QMetaObject &meta = Converter::staticMetaObject;
const int index = meta.indexOfMethod("toCelsius(int)");
if (index >= 0) {
    const QMetaMethod method = meta.method(index);
    int result = 0;
    const bool accepted =
        method.invokeOnGadget(&converter, qReturnArg(result), 212);
}
```

上例中的 `invokeOnGadget()` 目标必须是实际 gadget 对象地址。不要把返回值存储地址、任意普通 C++ 对象地址或临时对象地址当作 gadget。

## 3. 方法从哪里进入元对象

### 3.1 `Q_OBJECT` 类中的信号、槽和 `Q_INVOKABLE`

```cpp
class Worker : public QObject
{
    Q_OBJECT
public:
    Q_INVOKABLE int calculate(int input) const;

public slots:
    void refresh();

signals:
    void finished(int result);
};
```

只有被元对象系统收集的方法才能通过 `QMetaObject::method()` 得到。普通 public 成员函数如果没有 `Q_INVOKABLE`、slot 或 signal 声明，不会因为访问级别是 public 就自动可调用。

### 3.2 方法签名必须与元对象格式一致

```cpp
const int index =
    object->metaObject()->indexOfMethod(
        "calculate(int)");
```

查找时使用 normalized signature 更稳妥：

```cpp
const QByteArray signature =
    QMetaObject::normalizedSignature(
        "calculate( int )");
const int index =
    object->metaObject()->indexOfMethod(signature);
```

参数类型、`const`、引用以及命名空间必须与元对象记录一致。找不到时返回负索引，不能把负索引直接传给 `method()`。

## 4. 方法类型与属性

### 4.1 `MethodType`

`methodType()` 返回：

| 类型 | 含义 |
| --- | --- |
| `Method` | 普通元方法，通常来自 `Q_INVOKABLE` |
| `Signal` | 信号 |
| `Slot` | 槽 |
| `Constructor` | 元对象可调用的构造函数记录 |

方法类型是元数据分类，不改变 `invoke()` 的调用接口。一个 signal 也可以作为 `QMetaMethod` 被检查和连接，但通常不应把 signal 当普通业务函数直接调用。

### 4.2 `Access`

`access()` 返回 C++ 访问级别 `Private`、`Protected` 或 `Public`。它是元数据中的声明信息，不是运行时权限检查。调用 `invoke()` 时仍应遵守项目的封装边界。

### 4.3 `Attributes`

`attributes()` 返回位掩码：

| 标志 | 值 | 含义 |
| --- | --- | --- |
| `Compatibility` | `0x1` | 为兼容旧版本元对象或旧签名保留的方法 |
| `Cloned` | `0x2` | moc 生成的克隆方法记录 |
| `Scriptable` | `0x4` | 标记为可脚本调用的方法 |

返回的是整数位掩码，不是 `QFlags` 类型。使用按位与判断某一标志：

```cpp
if (method.attributes() & QMetaMethod::Scriptable)
    exposeToScript(method);
```

## 5. `invoke()` 的连接类型语义

### 5.1 `AutoConnection`

默认连接类型。若当前线程就是目标对象线程，通常直接调用；否则投递到目标线程事件循环。它依赖目标对象的线程归属和事件循环状态。

### 5.2 `DirectConnection`

在当前调用线程中立即执行目标方法，不管目标对象的线程归属。它不会自动把执行切换到对象线程，因此对 QObject 状态的访问必须由调用方保证线程安全。

### 5.3 `QueuedConnection`

把调用投递到目标对象线程，当前调用立即返回。参数必须能复制到事件队列中，通常要求类型已经注册为元类型。queued 调用不能安全地依赖栈上对象地址、不可复制引用或在返回后即失效的临时对象。

### 5.4 `BlockingQueuedConnection`

把调用投递到目标对象线程，并阻塞当前线程直到目标方法执行完成。若当前线程和目标对象线程相同，会发生死锁；跨线程使用时也要确保目标事件循环能够处理事件。只在确实需要同步等待时使用。

### 5.5 `invoke()` 的返回值

`invoke()` 返回 `bool`，表示 Qt 是否接受了这次元调用请求，不等于目标方法的业务返回值，也不等于目标方法内部返回了成功。

- 直接调用：通常可以同时得到 `bool` 和 `qReturnArg()` 捕获的返回对象；
- 队列调用：请求成功只表示已投递，不能用当前栈变量捕获未来结果；
- 目标方法内部抛出或业务失败，不会自动转换成 `invoke()` 的错误状态。

## 6. 参数和返回值边界

### 6.1 模板调用与旧式 `Q_ARG`

Qt 6 推荐使用模板化调用：

```cpp
QString result;
method.invoke(&calculator,
              Qt::DirectConnection,
              qReturnArg(result),
              12,
              1.5);
```

兼容旧代码时可以使用 `Q_ARG`/`Q_RETURN_ARG`：

```cpp
QString result;
method.invoke(&calculator,
              Qt::DirectConnection,
              Q_RETURN_ARG(QString, result),
              Q_ARG(int, 12),
              Q_ARG(double, 1.5));
```

两种方式不要混用同一组参数。旧式 API 的参数类型文本必须与元方法签名一致。

### 6.2 参数个数

旧式 `QGenericArgument` 重载最多接受 `Q_METAMETHOD_INVOKE_MAX_ARGS` 个参数；Qt 6.5 起的模板重载仍受底层元调用支持的参数数量限制。当前头文件把该宏定义为 `10`。

超过限制时，不应期待 `invoke()` 自动展开任意数量参数；应改为普通 C++ 调用、打包参数对象，或设计专门的接口。

### 6.3 队列参数必须可复制

下面的调用通常不适合 queued：

```cpp
// 例如参数是不可复制的临时对象、裸指针指向短生命周期内存，
// 或类型没有注册到 Qt 元类型系统。
method.invoke(object, Qt::QueuedConnection, value);
```

队列只保存参数副本，不保存调用者局部变量的引用语义。自定义类型应先用 `Q_DECLARE_METATYPE`/`qRegisterMetaType` 等方式让 Qt 能构造和复制它。

### 6.4 返回值只能在同步执行中可靠捕获

```cpp
QString result;
const bool accepted =
    method.invoke(object,
                  Qt::DirectConnection,
                  qReturnArg(result),
                  input);
```

`qReturnArg()` 指向调用方提供的存储。不要把它用于 `QueuedConnection`，因为调用返回后局部变量可能已经销毁；对 `BlockingQueuedConnection`，存储必须在线程等待期间保持有效。

## 7. `QMetaMethod` 与目标对象的生命周期

### 7.1 方法句柄不拥有对象

```cpp
QMetaMethod method = object->metaObject()->method(index);
```

复制 `method` 不会复制 `object`，也不会延长对象生命。调用前必须确认目标对象仍然存在，并且其元对象仍来自加载中的模块。

### 7.2 元对象重建或动态库卸载

静态 moc 元对象通常在类型模块生命周期内稳定。若方法来自动态插件，插件卸载后继续保存和使用方法句柄，以及 `nameView()`、`tag()` 等底层字符串，都是危险的。跨卸载边界时应复制业务需要的字符串并停止使用该句柄。

### 7.3 跨线程访问

读取 `QMetaMethod` 的元数据通常是只读操作，但调用目标方法仍遵守 QObject 线程规则。`QMetaMethod` 不会替调用方加锁，也不保证目标方法本身线程安全。

## 8. 逐项 API 说明

### 8.1 `QMetaMethod()`

```cpp
constexpr QMetaMethod();
```

构造无效方法句柄。默认句柄适合表示“尚未查找到方法”，但不应直接调用 `invoke()` 或读取参数信息。

### 8.2 `access() const`

```cpp
Access access() const;
```

返回方法声明的访问级别：`Private`、`Protected` 或 `Public`。这是元数据，不是运行时授权机制。

### 8.3 `attributes() const`

```cpp
int attributes() const;
```

返回 `Compatibility`、`Cloned` 和 `Scriptable` 等属性位。调用方应按位检查，不要把返回值当作单一枚举。

### 8.4 `enclosingMetaObject() const`

```cpp
const QMetaObject *enclosingMetaObject() const;
```

返回包含该方法记录的元对象。它不是目标对象指针；同一个方法句柄可以描述某个类型的所有实例方法。无效句柄可能返回 `nullptr`。

### 8.5 `fromSignal(signal)`

```cpp
template <typename PointerToMemberFunction>
static QMetaMethod fromSignal(PointerToMemberFunction signal);
```

按 signal 成员函数指针取得 `QMetaMethod`。指针所属类必须带 `Q_OBJECT`，并且确实是该类已由 moc 生成的 signal。相比手写字符串，它能让编译器检查信号成员函数的类型。

### 8.6 `getParameterTypes(int *types) const`

```cpp
void getParameterTypes(int *types) const;
```

把每个参数的旧式 Qt 类型 ID 写入调用方提供的数组。数组至少需要 `parameterCount()` 个 `int` 元素；参数个数为 0 时可以传空指针。它是低层兼容 API，现代代码通常优先使用 `parameterMetaType()` 或 `parameterTypes()`。

### 8.7 `invoke(QObject *, ...) const`

模板重载：

```cpp
template <typename... Args>
bool invoke(QObject *obj, Args &&... arguments) const;

template <typename... Args>
bool invoke(QObject *obj, Qt::ConnectionType type,
            Args &&... arguments) const;

template <typename ReturnArg, typename... Args>
bool invoke(QObject *obj,
            QTemplatedMetaMethodReturnArgument<ReturnArg> ret,
            Args &&... arguments) const;

template <typename ReturnArg, typename... Args>
bool invoke(QObject *obj, Qt::ConnectionType type,
            QTemplatedMetaMethodReturnArgument<ReturnArg> ret,
            Args &&... arguments) const;
```

在 `QObject` 上执行元方法。省略连接类型时使用 `Qt::AutoConnection`；带返回值的重载把同步结果写入 `ret`。目标必须与该方法所属元对象兼容，方法签名和参数类型必须匹配。

旧式重载还接受 `QGenericArgument` 和 `QGenericReturnArgument`，最多支持 `Q_METAMETHOD_INVOKE_MAX_ARGS` 个参数。新代码优先使用模板重载。

### 8.8 `invokeOnGadget(void *, ...) const`

模板重载：

```cpp
template <typename... Args>
bool invokeOnGadget(void *gadget, Args &&... arguments) const;

template <typename ReturnArg, typename... Args>
bool invokeOnGadget(
    void *gadget,
    QTemplatedMetaMethodReturnArgument<ReturnArg> ret,
    Args &&... arguments) const;
```

在 `Q_GADGET` 的元方法上调用。gadget 地址必须指向方法所属类型的正确对象布局；该 API 不做运行时 C++ 类型检查。它不接受 `Qt::ConnectionType`，因为 gadget 没有 QObject 的线程归属和事件投递模型。

### 8.9 `isConst() const`

```cpp
bool isConst() const;
```

Qt 6.2 引入。报告方法是否在元对象记录中标记为 const。它是反射信息，不会把一个实际的非 const 方法变成 const 调用。

### 8.10 `isValid() const`

```cpp
bool isValid() const;
```

判断句柄是否关联有效方法记录。查找失败、默认构造或不兼容的元对象索引都可能产生无效句柄。

### 8.11 `methodIndex() const`

```cpp
int methodIndex() const;
```

返回方法在所属元对象方法表中的全局索引。这个索引可用于同一 `QMetaObject` 的 `method(index)`，但不要把它当作跨类型稳定 ID。

### 8.12 `methodSignature() const`

```cpp
QByteArray methodSignature() const;
```

返回包含方法名和参数类型的签名，例如 `calculate(int)`。返回值是拥有型 `QByteArray`，适合日志、查找和缓存。

### 8.13 `methodType() const`

```cpp
MethodType methodType() const;
```

返回 `Method`、`Signal`、`Slot` 或 `Constructor`。它不等价于 C++ 访问级别；访问级别由 `access()` 返回。

### 8.14 `name() const`

```cpp
QByteArray name() const;
```

返回不带参数列表的方法名。它是拥有型 `QByteArray`，例如 `calculate`。

### 8.15 `nameView() const`

```cpp
QByteArrayView nameView() const;
```

Qt 6.9 引入。返回指向元对象字符串的非拥有 view，适合短期比较，不能在关联元对象或动态库卸载后继续使用。需要跨边界保存时使用 `name()` 复制。

### 8.16 `parameterCount() const`

```cpp
int parameterCount() const;
```

返回元方法参数个数。它决定 `getParameterTypes()` 的目标数组大小，也可用于验证动态调用参数数量。

### 8.17 `parameterMetaType(int index) const`

```cpp
QMetaType parameterMetaType(int index) const;
```

Qt 6.0 引入。返回参数的 `QMetaType`，索引越界或元对象缺少新式类型数据时可能得到无效类型。相比旧式 `parameterType()`，它能表达更多现代类型信息。

### 8.18 `parameterNames() const`

```cpp
QList<QByteArray> parameterNames() const;
```

返回 moc 记录的参数名称。参数名主要用于工具、文档和脚本映射，不参与 C++ 重载匹配；没有显式参数名时可能为空或使用 moc 可获得的名称。

### 8.19 `parameterType(int index) const`

```cpp
int parameterType(int index) const;
```

返回旧式 Qt 类型 ID。索引无效或类型未注册时可能返回 `QMetaType::UnknownType`。新代码需要完整类型信息时优先使用 `parameterMetaType()`。

### 8.20 `parameterTypeName(int index) const`

```cpp
QByteArray parameterTypeName(int index) const;
```

Qt 6.0 引入。返回参数类型名称的拥有型字节数组。它适合显示和诊断，不应替代真正的 `QMetaType` 能力判断。

### 8.21 `parameterTypes() const`

```cpp
QList<QByteArray> parameterTypes() const;
```

返回所有参数类型名称。列表顺序与方法签名顺序一致，适合日志和动态工具展示。

### 8.22 `relativeMethodIndex() const`

```cpp
int relativeMethodIndex() const;
```

Qt 6.0 引入。返回方法在其直接声明类方法表中的相对索引，不包含基类方法。遍历某个类自己声明的方法时，它比全局 `methodIndex()` 更有用；不要把相对索引和其他类比较。

### 8.23 `returnMetaType() const`

```cpp
QMetaType returnMetaType() const;
```

Qt 6.0 引入。返回方法返回类型的 `QMetaType`。无返回值方法通常对应 void 类型。动态调用前可用它确认返回存储类型是否匹配。

### 8.24 `returnType() const`

```cpp
int returnType() const;
```

返回旧式 Qt 返回类型 ID。需要现代类型信息时优先使用 `returnMetaType()`。

### 8.25 `revision() const`

```cpp
int revision() const;
```

返回 moc 记录的方法 revision。它主要服务于版本化元对象、QML 和工具兼容性判断，不是方法调用次数或线程版本。

### 8.26 `tag() const`

```cpp
const char *tag() const;
```

返回方法声明上的自定义 tag 文本。tag 通常由宏在 moc 解析时保留，返回的是元对象拥有的非拥有指针。未定义 tag 时可能为空指针。

### 8.27 `typeName() const`

```cpp
const char *typeName() const;
```

返回返回类型名称的非拥有字符串指针。它是旧式文本信息，不应代替 `returnMetaType()` 做类型安全判断。

## 9. 常见错误

### 9.1 把普通 public 成员函数当成可调用元方法

**症状：** `indexOfMethod()` 找不到一个明明是 public 的成员函数。

**原因：** public 访问级别不会自动把函数放进元对象；它还必须是 signal、slot 或 `Q_INVOKABLE`。

**修复：** 增加适用的元对象声明并重新运行 moc，或直接使用普通 C++ 调用。

### 9.2 把负索引传给 `method()`

**症状：** 找不到方法后仍访问到不可预测的元方法。

**原因：** `indexOfMethod()` 找不到时返回负值。

**修复：** 先检查 `index >= 0`，再调用 `metaObject->method(index)`。

### 9.3 用 queued 调用捕获局部返回值

**症状：** 返回值为空、写入已销毁的对象或出现悬空引用。

**原因：** queued 调用稍后执行，`qReturnArg()` 指向的局部变量可能已经离开作用域。

**修复：** 需要结果时使用 `DirectConnection` 或 `BlockingQueuedConnection`，或让目标方法通过 signal/共享状态异步返回。

### 9.4 把 `DirectConnection` 当作线程切换

**症状：** 在错误线程访问 QObject 状态，出现竞态或 GUI 崩溃。

**原因：** `DirectConnection` 强制在当前线程执行。

**修复：** 使用 `AutoConnection`/`QueuedConnection`，或明确提供锁和线程安全协议。

### 9.5 在同一线程使用 `BlockingQueuedConnection`

**症状：** 调用永久阻塞。

**原因：** 当前线程等待自己处理被投递的调用，形成死锁。

**修复：** 先确认目标线程与当前线程不同；同线程需要立即执行时使用 `DirectConnection`。

### 9.6 gadget 指针类型不匹配

**症状：** `invokeOnGadget()` 返回失败或访问错误内存。

**原因：** API 使用 `void *`，无法在运行时验证指针真实类型。

**修复：** 只把对应 `Q_GADGET` 类型的对象地址传给它，并确保方法来自同一个 `staticMetaObject`。

### 9.7 忽略队列参数的元类型注册

**症状：** queued 调用返回 false，并出现“无法排队参数”类诊断。

**原因：** Qt 无法复制或构造参数类型。

**修复：** 注册自定义类型，或者改用可复制的 Qt 元类型；不要把无法复制的引用参数投递到队列。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QMetaMethod()` | 构造无效方法句柄 | 不会自动绑定对象或方法 |
| `access()` | 查询 C++ 访问级别 | 不是运行时权限控制 |
| `attributes()` | 查询 `Compatibility`/`Cloned`/`Scriptable` 位 | 用按位与判断，不是单一枚举 |
| `enclosingMetaObject()` | 返回所属 `QMetaObject` | 不拥有目标 QObject；动态库卸载后不要继续使用 |
| `fromSignal(signal)` | 从 signal 成员函数指针取得描述 | 所属类需要 `Q_OBJECT` 且指针必须确实是 signal |
| `getParameterTypes(types)` | 把参数类型 ID 写入数组 | 数组至少有 `parameterCount()` 个元素；现代代码优先 `parameterMetaType()` |
| `invoke(QObject *, ...)` | 在 QObject 上动态调用方法 | 检查目标生命周期、参数类型和连接类型 |
| `invokeOnGadget(void *, ...)` | 在 `Q_GADGET` 上动态调用 | `void *` 必须是正确 gadget 地址；没有线程投递 |
| `isConst()` | 查询方法是否为 const | Qt 6.2 起；只是元数据 |
| `isValid()` | 查询句柄是否有效 | 查找失败或默认构造句柄无效 |
| `methodIndex()` | 返回方法表全局索引 | 只在所属 `QMetaObject` 范围内有意义 |
| `methodSignature()` | 返回名称加参数类型签名 | 拥有型 `QByteArray`；适合查找和日志 |
| `methodType()` | 区分 method/signal/slot/constructor | 不等同于访问级别 |
| `name()` | 返回不带参数的方法名 | 拥有型 `QByteArray` |
| `nameView()` | 返回方法名的非拥有 view | Qt 6.9 起；不要跨元对象生命周期保存 |
| `parameterCount()` | 返回参数数量 | 与参数数组和动态调用校验配套 |
| `parameterMetaType(index)` | 返回参数 `QMetaType` | Qt 6.0 起；越界或旧元对象可能无效 |
| `parameterNames()` | 返回参数名称列表 | 仅用于工具展示，不参与重载匹配 |
| `parameterType(index)` | 返回旧式参数类型 ID | 现代代码优先 `parameterMetaType()` |
| `parameterTypeName(index)` | 返回参数类型名称 | Qt 6.0 起；文本不等于类型安全检查 |
| `parameterTypes()` | 返回全部参数类型名称 | 顺序与签名一致，适合诊断 |
| `relativeMethodIndex()` | 返回直接声明类中的相对索引 | Qt 6.0 起；不跨类比较 |
| `returnMetaType()` | 返回返回类型 `QMetaType` | Qt 6.0 起；同步返回值捕获前可用于校验 |
| `returnType()` | 返回旧式返回类型 ID | 现代代码优先 `returnMetaType()` |
| `revision()` | 返回方法 revision | 主要用于版本化元对象和工具 |
| `tag()` | 返回自定义 tag | 非拥有 `const char *`；可能为空 |
| `typeName()` | 返回返回类型名称 | 非拥有文本；不代替 `returnMetaType()` |
| `Q_METAMETHOD_INVOKE_MAX_ARGS` | 旧式动态调用的最大参数数 | Qt 6.11 头文件中为 `10`；超出应改设计 |

## 11. 推荐模板

### 11.1 安全按签名查找方法

```cpp
std::optional<QMetaMethod> findMethod(
    const QObject &object,
    const QByteArray &signature)
{
    const QMetaObject *meta = object.metaObject();
    const int index = meta->indexOfMethod(signature);
    if (index < 0)
        return std::nullopt;

    const QMetaMethod method = meta->method(index);
    if (!method.isValid())
        return std::nullopt;

    return method;
}
```

调用方仍需保证对象在实际 invoke 前没有被销毁，且签名中的参数与调用参数一致。

### 11.2 跨线程只投递无返回值调用

```cpp
bool postRefresh(QObject *target)
{
    const int index =
        target->metaObject()->indexOfMethod("refresh()");
    if (index < 0)
        return false;

    const QMetaMethod method = target->metaObject()->method(index);
    return method.invoke(target, Qt::QueuedConnection);
}
```

需要返回结果时，优先为类设计一个信号或异步任务结果，而不是把栈变量地址交给 queued 调用。

## 12. 一句话总结

`QMetaMethod` 是 `QMetaObject` 中一条方法记录的轻量句柄：它负责描述方法、信号、槽和构造函数，并可通过 `invoke()` 或 `invokeOnGadget()` 进行动态调用；真正的难点不在“能不能找到方法”，而在目标线程、队列参数可复制性、同步返回值生命周期、gadget 指针类型和元对象所属模块的生命周期。
