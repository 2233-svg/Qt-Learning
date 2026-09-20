# Qt QJniObject 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QJniObject>`  
> 所属模块：`Qt6::Core`  
> 继承：无  
> 引入版本：Qt 6.1  
> 平台提示：该 API 主要面向 Android 设计和测试

## 1. 它解决什么问题

`QJniObject` 是 Java 对象的 Qt 包装。它持有自己的 Java 对象引用，避免对象在包装对象存活期间被垃圾回收，并把大量常见 JNI 样板代码收拢为以下操作：

- 按类名或 `jclass` 创建 Java 对象；
- 调用实例方法和静态方法；
- 读取、写入实例字段和静态字段；
- 在 `QString` 与 Java `String` 之间转换；
- 把 JNI 对象转换为 `jobject`、`jstring` 等具体句柄；
- 从局部引用接管对象生命周期；
- 查询对象的 Java 类名、类对象和有效性。

它是“持有 Java 引用并调用 Java API”的值类型，不是 `JNIEnv` 的替代品，也不是 Java 集合或数组的 C++ 视图。需要直接调用原始 JNI 函数、管理当前线程环境或处理 JNI 异常时，使用 `QJniEnvironment`。

## 2. 实际使用场景

### 2.1 创建 Java 对象并调用实例方法

```cpp
QJniObject text = QJniObject::fromString(u"Hello"_qs);
const jint length = text.callMethod<jint>("length");
const QString result = text.toString();
```

模板参数和实参类型可以让 Qt 在编译期推导 JNI 方法签名；只读返回值直接用 `ReturnType` 接收。

### 2.2 调用静态方法

```cpp
const jint maximum = QJniObject::callStaticMethod<jint>(
    "java/lang/Math", "max", "(II)I", 2, 4);
```

如果返回 Java 对象，可以使用 `callStaticObjectMethod()`，它直接返回一个新的 `QJniObject`：

```cpp
const QJniObject thread = QJniObject::callStaticObjectMethod(
    "java/lang/Thread", "currentThread", "()Ljava/lang/Thread;");
```

### 2.3 读取和写入 Java 字段

```cpp
QJniObject settings("org/qtproject/qt/Settings");
const jint timeout = settings.getField<jint>("TIMEOUT");
settings.setField<jint>("TIMEOUT", 5000);
```

静态字段使用 `getStaticField()`、`getStaticObjectField()` 和 `setStaticField()`。

### 2.4 在 JNI 回调中保存 Java 返回对象

原始 JNI 调用多数返回局部引用。若需要把它存入 Qt 对象或跨越当前 native 调用范围使用，应通过 `fromLocalRef()` 接管它，或者构造新的 `QJniObject` 让 Qt 创建自己的引用。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QJniObject>
```

qmake 工程：

```qmake
QT += core
```

## 4. 最小可用示例

### 4.1 编译期推导方法签名

```cpp
QJniObject string = QJniObject::fromString(u"Hello, JNI"_qs);
const jint length = string.callMethod<jint>("length");
const QJniObject upper = string.callObjectMethod<jstring>("toUpperCase");
```

`callObjectMethod<jstring>()` 返回 `QJniObject`，模板参数 `jstring` 用来确定 Java 返回对象的 JNI 类型和签名。

### 4.2 从显式签名调用方法

```cpp
const jint index = string.callMethod<jint>("indexOf", "(I)I", 0x0051);
```

显式签名中的参数和返回类型必须与 Java 方法完全一致。对象签名使用 `L...;`，数组签名以 `[` 开头。

### 4.3 Qt 6.11 显式处理 Java 异常

```cpp
Q_DECLARE_JNI_CLASS(SettingsSecure, "android/provider/Settings$Secure")
using namespace QtJniTypes;

using Result = std::expected<QString, jthrowable>;
SettingsSecure settings;

const Result value = settings.callMethod<Result>(
    "getString", resolver, u"enabled_input_methods"_qs);
if (value) {
    return *value;
}

const QStringList trace = QJniEnvironment::stackTrace(value.error());
```

默认情况下 `QJniObject` 会报告并清除调用过程中产生的异常；把 `std::expected<..., jthrowable>` 作为返回类型则可以由调用方决定如何记录和恢复。

## 5. 核心使用模型

### 5.1 `QJniObject` 管理自己的引用

构造 `QJniObject` 时，Qt 会为包装对象建立并管理自己的 Java 引用；析构时释放由它持有的引用。拷贝、移动和赋值都应按值类型理解，但裸 JNI 句柄的有效性仍取决于持有它的 `QJniObject`。

```cpp
jstring rawString = nullptr;
{
    QJniObject string = QJniObject::fromString(u"Hello"_qs);
    rawString = string.object<jstring>();
    // rawString 在这里有效，因为 string 仍然存活。
}
// rawString 不能再被当作有效对象使用。
```

`object()` 返回的句柄不会额外延长生命周期。需要保存对象时保存 `QJniObject`，不要只保存返回的 `jobject`。

### 5.2 局部引用和 `fromLocalRef()`

`QJniObject(jobject object)` 适用于已经由调用方正确管理的引用；文档特别提醒，不要把未经处理的局部引用直接交给这个构造函数，除非调用方仍明确负责原始局部引用的管理。对 JNI 调用返回的局部引用，使用：

```cpp
jobject localRef = env->GetObjectArrayElement(array, index);
QJniObject element = QJniObject::fromLocalRef(localRef);
```

`fromLocalRef()` 接管局部引用所有权，并在返回前释放该局部引用。只对真正的局部引用使用它，不要把全局引用或其他不属于当前 JNI 局部引用范围的句柄交给它。

### 5.3 invalid 对象是正常的失败结果状态

默认构造、找不到类、构造失败或 JNI 调用返回 null 都可能得到 invalid `QJniObject`：

```cpp
QJniObject object;
if (!object.isValid())
    return;
```

`isValid()` 为 `false` 时，`object()` 返回 null 语义的句柄；继续调用实例方法通常没有意义，应先处理失败。

### 5.4 方法签名的两种来源

不显式传签名的模板重载会根据返回类型和参数类型推导签名。它要求类型是 JNI 内置类型，或已通过 `QtJniTypes` 声明类型映射的自定义类型：

```cpp
Q_DECLARE_JNI_CLASS(TestClass, "org/qtproject/qt/TestClass")
using namespace QtJniTypes;

const TestClass object =
    TestClass::callStaticMethod<TestClass>("create");
```

显式签名重载把签名字符串交给调用方。它适合缓存或复用明确的 Java ABI，但字符串本身不会被编译器验证。

### 5.5 返回对象时选择合适的调用 API

- `callMethod<ReturnType>()`：返回基本类型时直接返回值；如果 `ReturnType` 是 JNI 对象类型，结果是 `QJniObject`。
- `callObjectMethod<Ret>()`：明确表示返回 Java 对象，结果固定是 `QJniObject`。
- `callStaticMethod<ReturnType>()`：调用静态方法，可用于基本值或对象返回。
- `callStaticObjectMethod<Ret>()`：明确表示静态方法返回 Java 对象。

返回 `QJniObject` 不等于返回原始 `jobject`；Qt 会为返回对象建立自己的包装引用。

## 6. Java 方法签名速记

显式 JNI 方法签名的结构是：

```text
(参数类型...)返回类型
```

常见类型：

| C++/JNI 类型 | Java 签名 |
| --- | --- |
| `void` | `V` |
| `jboolean` | `Z` |
| `jbyte` | `B` |
| `jchar` | `C` |
| `jshort` | `S` |
| `jint` | `I` |
| `jlong` | `J` |
| `jfloat` | `F` |
| `jdouble` | `D` |
| `jobject` | `Ljava/lang/Object;` |
| `jclass` | `Ljava/lang/Class;` |
| `jstring` | `Ljava/lang/String;` |
| `jthrowable` | `Ljava/lang/Throwable;` |
| `jobjectArray` | `[Ljava/lang/Object;` |
| `jintArray` | `[I` |
| 自定义对象 | `L完整/类名;` |

类名使用 JNI 内部格式，例如 `java/lang/String`，不能把包名写成 `java.lang.String`。数组类型必须在类型签名前加 `[`。

## 7. Java 异常处理

所有 `QJniObject` 函数默认会处理调用期间的 JNI 异常和 Java 方法主动抛出的异常：报告并清除异常，使后续 JNI 调用可以继续。Qt 6.11 起可选择显式处理：

```cpp
using Result = std::expected<jint, jthrowable>;
const Result result = object.callMethod<Result>("readValue");
if (!result) {
    const QStringList trace = QJniEnvironment::stackTrace(result.error());
    // 按业务需要记录、降级或返回错误
}
```

兼容 `std::expected` 语义的自定义类型也可以使用，但必须提供 `value_type`、`error_type`、`unexpected_type`，能够从值类型以及包含 `jthrowable` 的 `unexpected_type` 构造。

这套自动异常处理只适用于 `QJniObject` API。若直接使用 `JNIEnv`，必须由调用方在异常后调用 `QJniEnvironment::checkAndClearExceptions()`；异常挂起时继续进行其他 JNI 调用是不安全的。

## 8. Java 对象生命周期与引用边界

大多数从 Java 传入 native 方法的对象是局部引用，只保证在当前 native 方法返回前有效。循环中创建大量局部引用时，应在每次迭代后手动删除不再需要的引用，避免耗尽局部引用容量。

通过 `AttachCurrentThread` 附着的线程不一定具有 native 方法返回时自动清理局部引用的边界；在这类线程上创建的局部引用需要调用方管理。

`QJniObject` 只管理它自己创建或持有的引用。若构造时传入的是已有全局或局部引用，Qt 不会替调用方释放那一个原始引用；这也是需要区分普通构造和 `fromLocalRef()` 的原因。

## 9. 常见误区与边界

### 9.1 把类名写成 Java 源码形式

```cpp
QJniObject object("org.example.Test"); // 错误的 JNI 类名形式
QJniObject object("org/example/Test"); // 正确
```

### 9.2 只保存 `object()` 返回的裸句柄

裸句柄的有效期受 `QJniObject` 所持引用约束。需要延长生命周期时保存一个新的 `QJniObject`，或明确创建并释放新的全局引用。

### 9.3 对局部引用错误使用普通构造

对 JNI 原始调用得到的局部引用，优先使用 `fromLocalRef()`。普通 `QJniObject(jobject)` 不会自动替你处理调用方原有引用的生命周期。

### 9.4 把 `callObjectMethod()` 当作任意返回值调用

`callObjectMethod()` 只适合 Java 对象返回值。基本类型方法使用 `callMethod<jint>()`、`callMethod<jboolean>()` 等。

### 9.5 隐式签名推导的类型不在 JNI 类型映射中

Qt 不能从任意 C++ 类自动推导 Java 签名。自定义 Java 类型要通过 `Q_DECLARE_JNI_CLASS` 建立 `QtJniTypes` 映射；否则使用显式签名并手动传递合适的 JNI 句柄。

### 9.6 显式签名与返回模板不一致

```cpp
object.callMethod<jint>("value", "()J"); // 签名与返回类型不一致
```

模板返回类型和显式签名必须描述同一个 Java 方法。字符串签名错误可能造成查找失败、异常或 JNI 层未定义行为。

### 9.7 把 Java `List` 当成 `QJniArray`

Java 集合对象是普通 `QJniObject`。只有 Java 原生数组使用 `QJniArray<T>`；`List` 需要调用其 Java 方法。

### 9.8 忽略静态方法和静态字段的类来源

按类名调用、按 `jclass` 调用、按已缓存 `jmethodID` 调用都要求对应的类和方法 ID 仍然有效。缓存时要明确类引用的生命周期，并在查找失败时处理 null。

### 9.9 忽略平台边界

Qt 6.11.1 文档明确说明该 API 主要为 Android 设计和测试，不能据此假定所有桌面平台都提供等价 JNI 运行环境。

## 10. 与相关类型的协作

- `QJniEnvironment`：提供当前线程的 `JNIEnv`、class loader 查找和显式 JNI 异常清理。
- `QJniArray<T>`：包装 Java 数组，可作为 `QJniObject` 兼容对象参与调用。
- `QtJniTypes`：声明自定义 Java 类映射，支持模板签名推导和类型化静态调用。
- `QString`：通过 `fromString()` 和 `toString()` 与 Java `String` 互转。
- `std::expected`：Qt 6.11 起可作为方法调用返回类型，显式携带 `jthrowable`。

## 11. 逐项 API 说明

### 构造与析构

#### `QJniObject::QJniObject()`

构造 invalid JNI 对象，不持有有效 Java 对象。用 `isValid()` 判断状态。

#### `explicit QJniObject::QJniObject(const char *className)`

按 `className` 查找 Java 类并调用默认构造函数。类名使用 JNI 内部格式；类不存在、默认构造失败或抛异常时结果可能 invalid。

#### `explicit QJniObject::QJniObject(jclass clazz)`

对给定 `jclass` 调用默认构造函数。`QJniObject` 会建立并管理自己的类引用；调用方仍需管理在包装对象之外创建的原始 `jclass` 引用。

#### `QJniObject::QJniObject(jobject object)`

围绕已有 Java 对象建立包装。包装对象会持有并释放自己的引用，但调用方传入的原始引用仍由调用方负责。对局部引用应优先使用 `fromLocalRef()`。

#### `[since 6.4] explicit template <typename... Args> QJniObject::QJniObject(const char *className, Args &&... args)`

查找类并调用带参数构造函数。只有所有参数都属于 JNI 类型或已注册的 `QtJniTypes` 类型时才可用；签名由返回无关的参数类型在编译期推导。

#### `[since 6.4] explicit template <typename... Args> QJniObject::QJniObject(jclass clazz, Args &&... args)`

使用已有 `jclass` 调用带参数构造函数。参数必须是可推导 JNI 类型；类句柄和构造失败都应按 invalid/异常路径处理。

#### `explicit QJniObject::QJniObject(const char *className, const char *signature, ...)`

按显式构造函数签名创建对象。签名只描述构造函数参数，返回部分不写在构造签名中；例如 `"(Ljava/lang/String;)V"`。

#### `explicit QJniObject::QJniObject(jclass clazz, const char *signature, ...)`

使用已有 `jclass` 和显式签名调用构造函数。签名和可变参数必须严格对应 Java 构造函数。

#### `[noexcept] QJniObject::~QJniObject()`

销毁包装并释放由 `QJniObject` 自己持有的引用。不会替调用方释放传入的外部全局/局部引用。

### 实例方法

#### `[since 6.4] template <typename ReturnType = void, typename... Args> auto QJniObject::callMethod(const char *methodName, Args &&... args) const`

调用当前 Java 对象的实例方法，返回 `ReturnType`；`ReturnType = void` 时不返回值。方法签名由返回类型和参数类型推导；若返回类型是 JNI 对象类型，结果包装为 `QJniObject`。Qt 6.11 起 `ReturnType` 还可以是可接收 `jthrowable` 的 expected-like 类型。

#### `[since 6.4] template <typename ReturnType = void, typename... Args> auto QJniObject::callMethod(const char *methodName, const char *signature, Args &&... args) const`

使用显式 JNI 签名调用实例方法。签名必须与方法名、参数和返回类型一致；对象返回仍会包装为 `QJniObject`。

#### `[since 6.4] template <typename Ret, typename... Args> QJniObject QJniObject::callObjectMethod(const char *methodName, Args &&... args) const`

调用返回 Java 对象的实例方法，结果是新的 `QJniObject`。签名由 `Ret` 和参数类型推导；`Ret` 应是对象类型，例如 `jstring`、`jobjectArray` 或映射的 Java 类。

#### `QJniObject QJniObject::callObjectMethod(const char *methodName, const char *signature, ...) const`

使用显式签名调用返回 Java 对象的实例方法。签名必须以对象类型结尾，例如 `"(II)Ljava/lang/String;"`。

### 静态方法

#### `[since 6.7] template <typename Klass, typename ReturnType = void, typename... Args> auto QJniObject::callStaticMethod(const char *methodName, Args &&... args)`

通过 `QtJniTypes::Klass` 的类型映射调用静态方法。`Klass` 必须是已注册 Java 类型；签名由返回类型和参数类型推导。Qt 6.7 起提供。

#### `[since 6.4] template <typename ReturnType = void, typename... Args> auto QJniObject::callStaticMethod(const char *className, const char *methodName, Args &&... args)`

按 JNI 类名调用静态方法，签名由模板返回类型和参数类型推导。返回对象时结果为 `QJniObject`。

#### `[since 6.4] template <typename ReturnType = void, typename... Args> auto QJniObject::callStaticMethod(jclass clazz, const char *methodName, Args &&... args)`

使用已有 `jclass` 调用静态方法，签名由模板类型推导。适合类已经查找或缓存的场景。

#### `[since 6.4] template <typename ReturnType = void, typename... Args> auto QJniObject::callStaticMethod(jclass clazz, jmethodID methodId, Args &&... args)`

使用已经缓存的 `jclass` 和 `jmethodID` 调用静态方法。调用方必须保证方法 ID 属于该类且签名、参数和返回类型一致。

#### `[since 6.4] template <typename Ret = void, typename... Args> auto QJniObject::callStaticMethod(const char *className, const char *methodName, const char *signature, Args &&... args)`

按类名和显式签名调用静态方法。适合签名需要显式保存在代码或协议中的场景。

#### `template <typename Ret = void, typename... Args> auto QJniObject::callStaticMethod(jclass clazz, const char *methodName, const char *signature, Args &&... args)`

按已有 `jclass` 和显式签名调用静态方法。类句柄必须有效，签名必须完整。

#### `[since 6.4] template <typename Ret, typename... Args> QJniObject QJniObject::callStaticObjectMethod(const char *className, const char *methodName, Args &&... args)`

按类名调用返回 Java 对象的静态方法，签名由 `Ret` 和参数类型推导，返回新的 `QJniObject`。

#### `[since 6.4] template <typename Ret, typename... Args> QJniObject QJniObject::callStaticObjectMethod(jclass clazz, const char *methodName, Args &&... args)`

使用已有 `jclass` 调用返回 Java 对象的静态方法，返回新的 `QJniObject`。

#### `QJniObject QJniObject::callStaticObjectMethod(jclass clazz, jmethodID methodId, ...)`

使用已缓存的类和静态方法 ID 调用对象返回方法。适合高频调用；方法 ID 必须与类和对象返回签名匹配。

#### `QJniObject QJniObject::callStaticObjectMethod(const char *className, const char *methodName, const char *signature, ...)`

按类名和显式签名调用返回对象的静态方法。

#### `QJniObject QJniObject::callStaticObjectMethod(jclass clazz, const char *methodName, const char *signature, ...)`

按已有 `jclass` 和显式签名调用返回对象的静态方法。

### 类、对象和字符串

#### `[since 6.2] QByteArray QJniObject::className() const`

返回包装对象的 Java 类名，以 `QByteArray` 表示。invalid 对象不应被当作有效 Java 类查询。

#### `[since 6.4] template <typename Class, typename... Args> auto QJniObject::construct(Args &&... args)`

使用 `Class` 的 `QtJniTypes` 映射构造 Java 对象并返回 `QJniObject`。参数必须是 JNI 类型或已注册映射类型。

#### `[static] QJniObject QJniObject::fromLocalRef(jobject localRef)`

接管一个局部 JNI 引用并在返回前释放该局部引用，同时返回管理对象生命周期的 `QJniObject`。只传入当前 JNI 环境创建的局部引用。

#### `[static] QJniObject QJniObject::fromString(const QString &string)`

创建 Java `String` 并返回包装它的 `QJniObject`。对应的反向操作是 `toString()`。

#### `[static] bool QJniObject::isClassAvailable(const char *className)`

检查指定 JNI 类名是否可用。类名使用 `/` 分隔的内部格式；返回值只表示类是否可找到，不负责创建实例。

#### `bool QJniObject::isValid() const`

判断包装对象是否持有有效 Java 对象。默认对象、找不到类或失败调用产生的 null 结果会返回 `false`。

#### `jobject QJniObject::object() const`

返回包装对象持有的 `jobject`。该句柄的生命周期依赖当前 `QJniObject`，不能在包装销毁后继续使用。

#### `template <typename T> T QJniObject::object() const`

按具体 JNI Object Type 返回对象，例如 `jstring`、`jobjectArray` 或 `jthrowable`。模板类型必须与实际 Java 对象兼容；函数不会进行运行时类型修正。

#### `[since 6.2] jclass QJniObject::objectClass() const`

返回包装对象对应的 Java `jclass`。返回的类对象仍由当前 `QJniObject` 的生命周期支持；需要长期保存时要再建立合适的 `QJniObject` 或全局引用。

#### `QString QJniObject::toString() const`

调用 Java 对象的字符串表示并返回 `QString`。对 Java `String` 对象，这就是字符串内容；对其他对象，结果取决于其 Java `toString()` 实现。

### 实例字段

#### `template <typename Type> auto QJniObject::getField(const char *fieldName) const`

读取当前对象的实例字段，字段类型由模板参数 `Type` 指定并用于推导签名。类型必须与 Java 字段声明一致。

#### `template <typename T> QJniObject QJniObject::getObjectField(const char *fieldName) const`

按模板对象类型读取实例对象字段，并返回新的 `QJniObject`。`T` 用于确定字段的 JNI 对象类型。

#### `QJniObject QJniObject::getObjectField(const char *fieldName, const char *signature) const`

按显式对象签名读取实例字段，适合不希望在调用处写模板类型的场景。签名必须是对象类型，例如 `Ljava/lang/String;`。

#### `template <typename Ret = void, typename Type> auto QJniObject::setField(const char *fieldName, Type value)`

把 `value` 写入实例字段。模板 `Type` 描述字段值类型；可选的 `Ret` 用于匹配 Qt 的 JNI 调用返回约定，通常保持默认 `void`。

#### `template <typename Ret = void, typename Type> auto QJniObject::setField(const char *fieldName, const char *signature, Type value)`

使用显式字段签名写入实例字段。签名必须描述字段类型和 setter 调用约定，并与 `value` 的 JNI 类型一致。

### 静态字段

#### `[static] template <typename Klass, typename T> auto QJniObject::getStaticField(const char *fieldName)`

通过已注册的 `Klass` 类型映射读取静态字段。`Klass` 必须能映射到 Java 类，`T` 指定字段类型。

#### `[static] template <typename Type> auto QJniObject::getStaticField(const char *className, const char *fieldName)`

按类名读取静态字段，字段类型由 `Type` 指定并推导签名。

#### `[static] template <typename Type> auto QJniObject::getStaticField(jclass clazz, const char *fieldName)`

按已有 `jclass` 读取静态字段，字段类型由 `Type` 指定。

#### `[static] template <typename T> QJniObject QJniObject::getStaticObjectField(const char *className, const char *fieldName)`

按类名和模板对象类型读取静态对象字段，返回新的 `QJniObject`。

#### `[static] template <typename T> QJniObject QJniObject::getStaticObjectField(jclass clazz, const char *fieldName)`

按已有 `jclass` 和模板对象类型读取静态对象字段。

#### `[static] QJniObject QJniObject::getStaticObjectField(const char *className, const char *fieldName, const char *signature)`

按类名和显式对象签名读取静态对象字段。该重载不需要模板类型。

#### `[static] QJniObject QJniObject::getStaticObjectField(jclass clazz, const char *fieldName, const char *signature)`

按已有 `jclass` 和显式对象签名读取静态对象字段。

#### `[static] template <typename Klass, typename Ret = void, typename Type> auto QJniObject::setStaticField(const char *fieldName, Type value)`

通过已注册 Java 类型映射写入静态字段。`Klass` 必须有注册类型映射，`Type` 必须与字段类型一致。

#### `[static] template <typename Ret = void, typename Type> auto QJniObject::setStaticField(const char *className, const char *fieldName, Type value)`

按类名写入静态字段，字段签名由 `Type` 推导。

#### `[static] template <typename Ret = void, typename Type> auto QJniObject::setStaticField(jclass clazz, const char *fieldName, Type value)`

按已有 `jclass` 写入静态字段，字段签名由 `Type` 推导。

#### `[static] template <typename Ret = void, typename Type> auto QJniObject::setStaticField(const char *className, const char *fieldName, const char *signature, Type value)`

按类名和显式签名写入静态字段。

#### `[static] template <typename Ret = void, typename Type> auto QJniObject::setStaticField(jclass clazz, const char *fieldName, const char *signature, Type value)`

按已有 `jclass` 和显式签名写入静态字段。

### 交换、赋值和比较

#### `[noexcept, since 6.8] void QJniObject::swap(QJniObject &other)`

交换两个包装对象持有的引用。操作快速且不会失败，不复制 Java 对象内容。

#### `template <typename T, ...> QJniObject &QJniObject::operator=(T object)`

用可转换为 `jobject` 的对象替换当前包装对象。旧对象由 `QJniObject` 释放，新对象由包装对象管理自己的引用语义；调用方仍应明确传入句柄的引用类型和所有权。

#### `bool operator==(const QJniObject &o1, const QJniObject &o2)`

当两个包装对象引用同一个 Java 对象，或两者都为 null 时返回 `true`。比较的是 Java 对象身份，不是 `toString()` 内容，也不是 Java 的 `equals()` 结果。

#### `bool operator!=(const QJniObject &o1, const QJniObject &o2)`

当两个包装对象引用不同 Java 对象时返回 `true`；语义与 `operator==` 相反。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QJniObject()` | 创建 invalid 对象。 | 先用 `isValid()` 判断。 |
| 构造 | `QJniObject(className)` | 调用 Java 默认构造函数。 | 类名用 `/`，失败可能得到 invalid。 |
| 构造 | `QJniObject(clazz)` | 用 `jclass` 调用默认构造函数。 | Qt 管理自己的类引用，外部引用仍由调用方负责。 |
| 构造 | `QJniObject(object)` | 包装已有 Java 对象。 | 局部引用优先用 `fromLocalRef()`。 |
| 构造 | `QJniObject(className, args...)` | 按推导签名调用带参构造函数。 | Qt 6.4 起；参数须是 JNI/映射类型。 |
| 构造 | `QJniObject(clazz, args...)` | 用 `jclass` 调用带参构造函数。 | Qt 6.4 起；类句柄须有效。 |
| 构造 | `QJniObject(className, signature, ...)` | 按显式签名调用构造函数。 | 签名和可变参数必须一致。 |
| 构造 | `QJniObject(clazz, signature, ...)` | 用 `jclass` 和显式签名构造。 | 不要把方法签名写成构造返回签名。 |
| 析构 | `~QJniObject()` | 释放包装对象自己持有的引用。 | 不替调用方释放外部原始引用。 |
| 实例调用 | `callMethod<ReturnType>(name, args...)` | 按推导签名调用实例方法。 | 对象返回会包装为 `QJniObject`；Qt 6.11 可用 expected。 |
| 实例调用 | `callMethod<ReturnType>(name, signature, args...)` | 按显式签名调用实例方法。 | 签名必须完整匹配。 |
| 实例调用 | `callObjectMethod<Ret>(name, args...)` | 调用返回对象的实例方法。 | 只适合对象返回。 |
| 实例调用 | `callObjectMethod(name, signature, ...)` | 按显式签名调用对象返回方法。 | 结果是新的 `QJniObject`。 |
| 静态调用 | `callStaticMethod<Klass, ReturnType>(name, args...)` | 按类型映射调用静态方法。 | Qt 6.7 起；`Klass` 须有映射。 |
| 静态调用 | `callStaticMethod<ReturnType>(className, name, args...)` | 按类名推导签名调用静态方法。 | 类名用 JNI 内部格式。 |
| 静态调用 | `callStaticMethod<ReturnType>(clazz, name, args...)` | 按 `jclass` 推导签名调用。 | `clazz` 生命周期要有效。 |
| 静态调用 | `callStaticMethod<ReturnType>(clazz, methodId, args...)` | 用缓存 ID 调用静态方法。 | ID 必须属于该类。 |
| 静态调用 | `callStaticMethod(className, name, signature, args...)` | 按类名和显式签名调用。 | 字符串签名需自行校验。 |
| 静态调用 | `callStaticMethod(clazz, name, signature, args...)` | 按 `jclass` 和显式签名调用。 | 返回类型仍要与签名一致。 |
| 静态调用 | `callStaticObjectMethod<Ret>(className, name, args...)` | 调用返回对象的静态方法。 | 返回新的 `QJniObject`。 |
| 静态调用 | `callStaticObjectMethod<Ret>(clazz, name, args...)` | 用 `jclass` 调用对象返回静态方法。 | `Ret` 只描述对象类型。 |
| 静态调用 | `callStaticObjectMethod(clazz, methodId, ...)` | 用缓存 ID 调用对象返回静态方法。 | `clazz` 与 `methodId` 必须配套。 |
| 静态调用 | `callStaticObjectMethod(className, name, signature, ...)` | 按类名和签名调用对象返回静态方法。 | 签名结尾必须是对象类型。 |
| 静态调用 | `callStaticObjectMethod(clazz, name, signature, ...)` | 按 `jclass` 和签名调用对象返回方法。 | 失败得到 invalid 对象。 |
| 类信息 | `className()` | 返回 Java 类名。 | Qt 6.2 起；结果是 `QByteArray`。 |
| 构造工厂 | `construct<Class>(args...)` | 按类型映射构造 Java 对象。 | Qt 6.4 起；参数须可推导。 |
| 引用 | `fromLocalRef(localRef)` | 接管并释放局部引用。 | 只传真正的 local reference。 |
| 字符串 | `fromString(string)` | 创建 Java `String`。 | 与 `toString()` 配对使用。 |
| 字段 | `getField<Type>(fieldName)` | 读取实例基本/非对象字段。 | `Type` 必须匹配 Java 字段。 |
| 字段 | `getObjectField<T>(fieldName)` | 读取实例对象字段。 | 返回新的 `QJniObject`。 |
| 字段 | `getObjectField(fieldName, signature)` | 按显式签名读取实例对象字段。 | 签名必须是对象类型。 |
| 静态字段 | `getStaticField<Klass, T>(fieldName)` | 按类型映射读取静态字段。 | `Klass` 须有 Java 映射。 |
| 静态字段 | `getStaticField<Type>(className, fieldName)` | 按类名读取静态字段。 | `Type` 推导字段签名。 |
| 静态字段 | `getStaticField<Type>(clazz, fieldName)` | 按 `jclass` 读取静态字段。 | `clazz` 须有效。 |
| 静态字段 | `getStaticObjectField<T>(className, fieldName)` | 读取静态对象字段。 | 返回新的 `QJniObject`。 |
| 静态字段 | `getStaticObjectField<T>(clazz, fieldName)` | 用 `jclass` 读取静态对象字段。 | `T` 必须匹配字段类型。 |
| 静态字段 | `getStaticObjectField(className, fieldName, signature)` | 按显式签名读取静态对象字段。 | 不需要模板类型。 |
| 静态字段 | `getStaticObjectField(clazz, fieldName, signature)` | 用 `jclass` 和显式签名读取。 | 类句柄必须有效。 |
| 状态 | `isClassAvailable(className)` | 查询 Java 类是否可用。 | 静态检查，不创建对象。 |
| 状态 | `isValid()` | 查询是否持有有效对象。 | invalid 是正常失败状态。 |
| 句柄 | `object()` | 返回 `jobject`。 | 生命周期由当前包装对象保证。 |
| 句柄 | `object<T>()` | 返回具体 JNI 对象类型。 | `T` 只应是兼容的 JNI Object Type。 |
| 类信息 | `objectClass()` | 返回对象的 `jclass`。 | Qt 6.2 起；句柄不能脱离包装长期保存。 |
| 字段 | `setField(fieldName, value)` | 写入实例字段并推导类型。 | 值类型必须匹配字段。 |
| 字段 | `setField(fieldName, signature, value)` | 按显式签名写入实例字段。 | 签名和值必须一致。 |
| 静态字段 | `setStaticField<Klass>(fieldName, value)` | 按类型映射写入静态字段。 | `Klass` 须有映射。 |
| 静态字段 | `setStaticField(className, fieldName, value)` | 按类名写入静态字段。 | 类型由值推导。 |
| 静态字段 | `setStaticField(clazz, fieldName, value)` | 按 `jclass` 写入静态字段。 | 类句柄须有效。 |
| 静态字段 | `setStaticField(className, fieldName, signature, value)` | 按类名和签名写入。 | 适合显式 ABI。 |
| 静态字段 | `setStaticField(clazz, fieldName, signature, value)` | 按 `jclass` 和签名写入。 | 签名和值必须匹配。 |
| 交换 | `swap(other)` | 交换两个包装对象的引用。 | Qt 6.8 起；快速且 `noexcept`。 |
| 字符串 | `toString()` | 调用 Java `toString()` 转为 `QString`。 | 对非 String 对象取决于 Java 实现。 |
| 赋值 | `operator=(T object)` | 用兼容 JNI 对象替换当前对象。 | 旧对象会被释放，外部句柄所有权需明确。 |
| 比较 | `operator==` | 比较是否是同一个 Java 对象，或都为 null。 | 不是 Java `equals()`。 |
| 比较 | `operator!=` | 比较是否引用不同 Java 对象。 | 与 `operator==` 相反。 |

## 13. 使用判断

- 需要保存 Java 对象：使用 `QJniObject`，不要只保存 `jobject`。
- 需要直接调用 `JNIEnv`：使用 `QJniEnvironment`，并手动清理异常。
- 需要从原始 JNI 返回的局部引用创建包装：使用 `fromLocalRef()`。
- 能使用类型映射时优先使用模板重载；签名复杂或需要明确 ABI 时使用显式签名。
- Java 方法可能抛异常且业务需要区分失败原因：Qt 6.11 起使用 `std::expected<..., jthrowable>` 风格返回。
- 比较 Java 对象身份用 `operator==`；需要 Java 业务相等性时显式调用 Java 的 `equals()`。
