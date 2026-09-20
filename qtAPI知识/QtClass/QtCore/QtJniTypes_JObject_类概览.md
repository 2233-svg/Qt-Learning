# QtJniTypes::JObject：给 Java 类型建立 C++ 静态映射

`QtJniTypes::JObject<Type>` 是 Qt 6.8 引入的 JNI 模板基类。它不是让你直接写一个未指定 `Type` 的普通对象，而是通过 `Q_DECLARE_JNI_CLASS(Type, JavaSignature)` 宏生成一个具体的 C++ 类型。这个类型知道自己对应哪个 Java 类，因此可以在 JNI 调用中自动参与方法签名推导。

它解决的是 JNI 代码中最容易出错的一部分：Java 类名、方法参数类型和返回类型都要拼成签名字符串，手写既重复又容易错。声明类型后，C++ 代码可以像调用 `QJniObject` 一样调用 Java 实例方法、静态方法和字段，同时让编译器根据 C++ 类型推导 JNI 签名。

```cpp
#include <JObject>

Q_DECLARE_JNI_CLASS(File, "java/io/File")
Q_DECLARE_JNI_CLASS(FileWriter, "java/io/FileWriter")

using namespace QtJniTypes;

File file("/sdcard/example.txt");
if (file.callMethod<bool>("createNewFile")) {
    FileWriter writer(file);
    writer.callMethod("write", 42);
}
```

## 适用范围和前置条件

这组 API 属于 Qt Core 的 Android/JNI 支持，Qt 文档说明它主要为 Android 设计和测试，不能把它当作 Windows、Linux 桌面 JVM 的通用 Java 绑定层。项目需要使用支持 JNI 的 Qt/Android 构建配置，运行时还必须有可访问的 JVM 和对应 Java 类。

最低版本是 Qt 6.8。`Qt 6.11` 进一步支持用 `std::expected<Value, jthrowable>` 在单次调用中显式接收 Java 异常；旧版本代码不要直接照搬这一写法。

JNI 调用在当前线程执行。`JObject` 不会把调用自动切换到 Android 主线程；需要操作只能在主线程访问的 Android UI 对象时，应通过 Qt 的线程投递或 Android 自己的主线程机制完成。

## 声明一个 Java 类型

`Q_DECLARE_JNI_CLASS` 的第二个参数必须是完整的 Java 类签名，并使用 `/` 分隔包名：

```cpp
Q_DECLARE_JNI_CLASS(TestClass, "org/qtproject/qt/TestClass")
Q_DECLARE_JNI_CLASS(SettingsSecure, "android/provider/Settings$Secure")
```

宏会在 `QtJniTypes` 命名空间中生成对应类型。它既是 `QJniObject` 风格的包装器，也是 JNI 类型映射的一部分：

- `TestClass` 可以构造对应的 Java 对象。
- `TestClass` 可以作为其它 JNI 方法的参数，编译器知道它对应哪一个 Java 类。
- `TestClass::callStaticMethod()` 不再需要重复传入类名。
- 对象参数和返回值可参与 JNI 签名自动推导。

不要把 Java 的点号类名传给宏。应写成 `java/lang/String`，内部类使用 `$`，例如 `java/util/Map$Entry`。

## 对象创建和有效性

默认构造 `JObject` 会尝试默认构造对应的 Java 类型。带参数的构造方式则把参数传给 Java 构造函数。构造失败、类不存在或 Java 构造函数抛异常时，应检查 `isValid()`，并查看 Qt/JNI 的异常处理结果。

```cpp
Q_DECLARE_JNI_CLASS(StringBuilder, "java/lang/StringBuilder")
using namespace QtJniTypes;

StringBuilder builder;
if (!builder.isValid())
    return;

builder.callMethod("append", "hello");
```

`fromJObject(jobject)` 从已有 JNI 对象建立包装器；`fromLocalRef(jobject)` 专门用于接管一个 local reference。后者只应传入真正的局部引用，并把这份引用的释放责任交给包装器。原始 JNI 引用的类型和生命周期必须明确，不要把已经失效的 local reference 传进去。

```cpp
jobject local = env->GetObjectArrayElement(array, index);
auto value = QtJniTypes::StringBuilder::fromLocalRef(local);
// local 的释放责任已交给 value；不要再次 DeleteLocalRef(local)
```

Java 对象引用和 C++ 包装器不是同一个生命周期。JNI local reference 通常只在当前 native 方法调用期间有效；需要跨越 native 方法或保存到以后使用时，应让 `JObject`/`QJniObject` 管理合适的引用，或者明确创建和释放 global reference。

## 实例方法与静态方法

实例方法使用 `callMethod<ReturnType>()`。返回 `void` 时可以省略模板返回类型；返回基本 JNI 类型或 Qt 类型时，显式写返回类型通常更清晰。参数类型用于推导方法签名。

```cpp
Q_DECLARE_JNI_CLASS(String, "java/lang/String")

using namespace QtJniTypes;
String text("hello");

jint length = text.callMethod<jint>("length");
text.callMethod<void>("notify");
```

静态方法通过类型本身调用：

```cpp
Q_DECLARE_JNI_CLASS(Integer, "java/lang/Integer")

const jint value = Integer::callStaticMethod<jint>("parseInt", "42");
Integer answer = Integer::callStaticMethod<Integer>("valueOf", 42);
```

`JObject` 已经知道 Java 类名，所以静态调用不需要再传 `"java/lang/Integer"`。如果 Java 方法重载较多、C++ 类型不足以唯一确定签名，使用 `QJniObject` 的显式签名形式或检查生成的参数映射。

## 字段访问

实例字段使用 `getField()` 和 `setField()`，静态字段使用对应的 `getStaticField()` 和 `setStaticField()`：

```cpp
const jint count = object.getField<jint>("count");
object.setField("count", count + 1);

const auto version = MyJavaType::getStaticField<jstring>("VERSION");
MyJavaType::setStaticField("enabled", true);
```

字段名和 C++ 类型必须与 Java 声明匹配。JNI 能够找到字段并不意味着类型转换一定正确；类型不匹配可能导致 JNI 异常或错误结果。对对象字段，使用 Qt 的 JNI 对象包装类型或已经声明过的 `QtJniTypes` 类型，让签名推导保持一致。

## JNI 签名推导与显式签名

Java 方法签名遵循：

```text
(参数类型)返回类型
```

例如：

- `int` 是 `I`
- `boolean` 是 `Z`
- `String` 是 `Ljava/lang/String;`
- `String[]` 是 `[Ljava/lang/String;`
- `void` 是 `V`

`JObject` 可以根据返回模板参数和参数类型生成签名，但它不能猜出 Java 的语义重载。如果一个 Java 类存在多个同名方法，而 C++ 参数经过转换后仍可能对应多个签名，就应主动确认最终签名，必要时改用显式签名的 `QJniObject` API。

类映射本身也要准确。`Q_DECLARE_JNI_CLASS(MyType, "a/b/C")` 生成的类型只代表 `a.b.C`，不能用一个声明去覆盖不相关的子类或接口实现。

## Java 异常处理

Java 方法找不到、参数不匹配、字段不存在或方法主动抛异常时，JNI 会产生 pending exception。Qt 的 `QJniObject`/`JObject` 调用默认会处理并清理异常，但“被清理”不等于业务操作成功；调用方仍需检查返回值、对象有效性和日志。

Qt 6.11 起可以把返回类型写成兼容 `std::expected` 的类型，错误类型为 `jthrowable`：

```cpp
using Result = std::expected<QString, jthrowable>;

Result value = settings.callMethod<Result>(
    "getString", resolver, u"enabled_input_methods");

if (!value) {
    // 可把 value.error() 交给 QJniEnvironment 查询堆栈并记录
    return {};
}
return *value;
```

直接使用 `JNIEnv` 时，Qt 不会替你清理 pending exception。异常未处理时继续执行其它 JNI 调用是不安全的，必须使用 `QJniEnvironment::checkAndClearExceptions()` 等方式处理。

## Native 方法注册

`JObject::registerNativeMethods()` 可以把 C++ native 方法注册到宏声明的 Java 类。通常需要配合 `Q_DECLARE_JNI_NATIVE_METHOD` 和 `Q_JNI_NATIVE_METHOD`：

```cpp
Q_DECLARE_JNI_CLASS(NativeBridge, "org/qtproject/qt/NativeBridge")

static void nativePing(JNIEnv *, jobject, jint value)
{
    qInfo() << "from Java:" << value;
}

Q_DECLARE_JNI_NATIVE_METHOD(nativePing)

bool registerBridge()
{
    return QtJniTypes::NativeBridge::registerNativeMethods({
        Q_JNI_NATIVE_METHOD(nativePing)
    });
}
```

Java 侧方法必须声明为 `native`，参数和返回类型也必须匹配。注册失败时返回 `false`，常见原因包括类尚未加载、方法名/签名不一致、函数导出声明不正确或注册时机不对。

需要注册类静态成员函数时，使用 `Q_DECLARE_JNI_NATIVE_METHOD_IN_CURRENT_SCOPE` 和 `Q_JNI_NATIVE_SCOPED_METHOD`，明确传入所属 scope。

## 引用、线程和资源边界

- `JObject` 的包装器可以拷贝，拷贝的是对 Java 对象的管理引用，不是把 Java 对象复制一份。
- local reference 只在当前 JNI 调用作用域内可靠；循环创建大量 local reference 时要及时删除或使用 Qt 提供的接管方式。
- Java 对象可能被垃圾回收，裸 `jobject` 不能替代由包装器管理的长期引用。
- JNI 环境 `JNIEnv*` 与线程关联，不能把一个线程拿到的 `JNIEnv*` 指针缓存到另一个线程使用。
- Java API 的线程限制仍然有效，包装器不会绕过 Android UI 线程规则。
- 类名、方法名和字段名是运行时字符串，编译器只能检查 C++ 侧类型，不能保证 Java 端成员真的存在。

## 常见错误

- 直接写点号类名，例如 `java.lang.String`。JNI 类名必须使用 `/`。
- 把 local reference 当 global reference 保存。跨 native 调用需要由 `JObject` 或显式 global reference 管理。
- 以为 `callMethod<jobject>()` 返回一个可长期保存的裸引用。对象引用应转成受管理的 Qt JNI 包装器。
- Java 方法重载时只写方法名，不确认参数和返回类型。必要时检查显式签名。
- 忽略 `isValid()` 和异常结果。调用失败不一定通过 C++ 异常表现。
- 在一个线程获取 `JNIEnv*` 后跨线程复用。
- 在非 Android 桌面程序中假定这套 API 可用。Qt 文档明确说明它主要针对 Android。
- 注册 native 方法时 C++ 函数签名与 Java `native` 声明不一致。

## API 速查表

| API/宏 | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `Q_DECLARE_JNI_CLASS(Type, "a/b/C")` | 声明一个 Java 类型映射 | Qt 6.8 起；类名必须是完整 JNI 路径，生成 `QtJniTypes::Type` |
| `JObject()` | 默认构造对应 Java 类型 | 会尝试调用 Java 默认构造函数；失败后检查 `isValid()` 和异常 |
| `JObject(QJniObject &&)` | 从 Qt JNI 包装器移动构造 | 转移包装器管理的引用 |
| `JObject(const QJniObject &)` | 从 Qt JNI 包装器拷贝构造 | 共享/复制管理引用，不复制 Java 对象内容 |
| `JObject(jobject)` | 从 JNI 对象构造 | 明确原始引用的生命周期；local ref 优先使用 `fromLocalRef()` |
| `construct(args...)` | 构造 Java 对象 | 参数映射到 Java 构造函数；返回对应 `JObject<Type>` |
| `fromJObject(jobject)` | 从已有对象建立包装器 | 不要传入已失效的 JNI 引用 |
| `fromLocalRef(jobject)` | 接管 local reference | 只用于 local ref；接管后不要再次释放同一引用 |
| `isValid()` | 判断是否持有有效 Java 对象引用 | 只能说明引用有效，不保证目标方法/字段存在 |
| `isClassAvailable()` | 判断映射的 Java 类是否可用 | 静态函数；适合在可选 Android API 或不同设备版本上探测 |
| `className()` | 获取对应 Java 类名 | 返回 JNI 风格类名，例如 `java/lang/String` |
| `objectClass()` | 获取对象的 `jclass` | 返回的引用仍需遵守 JNI 生命周期规则 |
| `callMethod<Ret>(method, args...)` | 调用实例方法 | 返回类型和参数参与签名推导；对象返回值用受管理包装器处理 |
| `callStaticMethod<Ret>(method, args...)` | 调用声明类的静态方法 | 不需重复传 Java 类名；重载不明确时核对签名 |
| `getField<T>(field)` | 读取实例字段 | C++ 类型必须和 Java 字段类型匹配 |
| `setField<Ret>(field, value)` | 写入实例字段 | 可能触发 Java 异常；检查调用结果和异常 |
| `getStaticField<T>(field)` | 读取静态字段 | 操作的是声明类型的字段 |
| `setStaticField<Ret>(field, value)` | 写入静态字段 | 需要正确的 Java 字段名和类型 |
| `toString()` | 调用 Java 对象的字符串表示 | 是 Java `toString()` 结果，不是 JNI 类名 |
| `registerNativeMethods(methods)` | 注册 C++ native 方法 | 返回 `bool`；类、方法名、签名和加载时机必须匹配 |
| `Q_DECLARE_JNI_NATIVE_METHOD(Method)` | 声明自由函数为 native 方法 | 供 `Q_JNI_NATIVE_METHOD` 生成注册项 |
| `Q_JNI_NATIVE_METHOD(Method)` | 生成自由函数注册描述 | 传给 `registerNativeMethods()` 或 `QJniEnvironment` |
| `Q_DECLARE_JNI_NATIVE_METHOD_IN_CURRENT_SCOPE(Method)` | 声明当前 scope 的静态成员 native 方法 | 配合 scoped 注册宏使用 |
| `Q_JNI_NATIVE_SCOPED_METHOD(Method, Scope)` | 生成带 scope 的注册描述 | `Scope` 必须是成员函数所属类 |
| `std::expected<Value, jthrowable>` 返回类型 | 显式接收 Java 异常 | Qt 6.11 起；需要处理 error 并读取 Java 异常信息 |
