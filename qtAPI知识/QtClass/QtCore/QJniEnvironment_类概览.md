# Qt QJniEnvironment 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QJniEnvironment>`  
> 所属模块：`Qt6::Core`  
> 继承：无  
> 引入版本：Qt 6.1  
> 平台提示：该 API 主要面向 Android 设计和测试

## 1. 它解决什么问题

JNI 的 `JNIEnv` 是“当前线程的 JNI 函数表入口”，不是可以在任意线程之间共享的普通上下文对象。每个 native 函数通常会收到一个 `JNIEnv *`，而从 C++ 主动进入 Java 时，还需要确保当前线程已经附着到 Java VM，并在 JNI 调用后处理可能挂起的 Java 异常。

`QJniEnvironment` 把这组容易出错的边界集中起来：

- 构造对象时为当前线程取得 JNI 环境，并在需要时附着线程；
- 通过 `jniEnv()`、`operator->()` 和 `operator*()` 访问原始 `JNIEnv`；
- 使用 Qt 的 class loader 查找 Java 类；
- 按显式签名或模板参数查找字段和方法 ID；
- 直接 JNI 调用后检查、打印并清除待处理异常；
- 注册 Java native 方法；
- 查询当前进程的 `JavaVM`。

它不是 Java 对象包装类。需要保存 Java 对象、处理全局引用或调用实例方法时，使用 `QJniObject`；需要直接操作 JNI 函数表时，使用 `QJniEnvironment`。

## 2. 实际使用场景

### 2.1 在 C++ 中直接调用 JNI

```cpp
QJniEnvironment env;
jclass clazz = env.findClass("org/qtproject/example/android/CustomClass");

if (clazz) {
    QJniObject message = QJniObject::fromString("hello from C++");
    QJniObject::callStaticMethod<void>(
        clazz,
        "printFromJava",
        "(Ljava/lang/String;)V",
        message.object<jstring>());
}

env.checkAndClearExceptions();
```

`findClass()` 使用 Qt 在 Android 上配置的 class loader，更适合查找由 Qt 应用加载的 Java 类。

### 2.2 缓存字段或方法 ID

当同一个类会被频繁访问时，可以先查找 `jfieldID` 或 `jmethodID`，之后把 ID 传给 JNI 或 `QJniObject` 的调用接口，避免每次按名称和签名重新查找。

```cpp
QJniEnvironment env;
jclass clazz = env.findClass("org/qtproject/example/android/Counter");
jmethodID increment = env.findMethod<void>(clazz, "increment");
```

模板重载会根据模板参数推导 JNI 签名；也可以使用显式签名重载。

### 2.3 注册 Java native 方法

在 `JNI_OnLoad` 或等价初始化路径中，通过 `registerNativeMethods()` 把 Java 方法名、签名和 C++ 函数地址绑定起来。注册必须发生在 Java 尝试调用这些 native 方法之前。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QJniEnvironment>
```

qmake 工程：

```qmake
QT += core
```

## 4. 最小可用示例

### 4.1 检查环境并调用原始 JNI

```cpp
QJniEnvironment env;
if (!env.isValid())
    return;

jclass clazz = env->FindClass("java/lang/String");
if (!clazz) {
    env.checkAndClearExceptions(QJniEnvironment::OutputMode::Silent);
    return;
}

env.checkAndClearExceptions();
```

`env->FindClass()` 等价于通过 `jniEnv()` 取得 `JNIEnv *` 后调用 JNI 成员；如果 JNI 调用可能抛出 Java 异常，应立即检查。

### 4.2 使用静态检查函数

```cpp
void nativeFunction(JNIEnv *jni)
{
    jclass clazz = jni->FindClass("java/lang/String");
    if (!QJniEnvironment::checkAndClearExceptions(
            jni, QJniEnvironment::OutputMode::Verbose)) {
        // 没有待处理异常
    }
    (void)clazz;
}
```

静态重载适合已经从 JNI 回调参数中拿到 `JNIEnv *` 的函数，不需要再创建一个环境包装对象。

## 5. 核心使用模型

### 5.1 `JNIEnv` 绑定当前线程

JNI 环境不能在线程之间共享。`QJniEnvironment` 的实例只应在创建它的线程中使用。构造函数会构造一个新的环境对象并把当前线程附着到 Java VM；析构时会分离当前线程，并清除仍然挂起的 Java 异常。

因此不要把 `JNIEnv *` 保存到成员变量后在另一个线程使用，也不要把一个线程的 `QJniEnvironment` 传给工作线程。每个需要 JNI 的线程都应在自己的调用范围内建立环境。

### 5.2 析构会清异常，但不应依赖它代替显式检查

析构函数会通过 `checkAndClearExceptions()` 清除待处理异常。这可以避免异常状态泄漏到后续 JNI 调用，但也意味着如果代码完全不显式检查，错误可能只在环境销毁时被静默处理或统一打印。

直接使用 `JNIEnv` 的代码应在可能抛异常的调用后立刻检查，以便把错误和具体操作对应起来。`QJniObject` 的调用接口会自行处理异常，与直接 JNI 调用的责任不同。

### 5.3 `OutputMode` 决定清异常时的输出

| 取值 | 值 | 行为 |
| --- | ---: | --- |
| `Silent` | `0` | 清除异常，不输出堆栈回溯。 |
| `Verbose` | `1` | 清除异常，并把异常及堆栈回溯作为错误写到 `stderr`。 |

默认值是 `Verbose`。库代码若需要自己记录或转换错误，可以显式使用 `Silent`，但必须确保异常不会因此被无声吞掉。

### 5.4 类查找和签名查找是两个不同层次

`findClass()` 只负责找到 `jclass`。字段和方法的 `jfieldID`、`jmethodID` 查找还需要名称以及类型签名：

- 显式签名重载直接接收 JNI 签名字符串；
- Qt 6.4 起的模板重载根据模板参数推导签名；
- 找不到目标时返回 `nullptr`，不会返回一个可继续调用的占位 ID。

签名必须与 Java 声明完全一致，包括实例/静态方法、参数顺序、返回类型和对象描述符。

### 5.5 注册 native 方法要求名称和签名严格一致

`JNINativeMethod` 的每一项由 Java 方法名、JNI 方法签名和 C++ 函数地址组成。注册成功只说明绑定操作成功，不代表 C++ 函数内部没有异常或参数错误；Java 方法声明、签名和 C++ 函数 ABI 仍必须互相匹配。

使用模板版注册时，Java 类类型必须通过 `Q_DECLARE_JNI_CLASS` 声明在 `QtJniTypes` 命名空间中，native 函数还要使用相应的 `Q_DECLARE_JNI_NATIVE_METHOD` 宏声明。

## 6. 常见误区与边界

### 6.1 把 `JNIEnv *` 当成跨线程句柄

这是最重要的错误。`JNIEnv` 与线程绑定，不能从一个线程传给另一个线程。跨线程任务应在目标线程重新构造 `QJniEnvironment`，并确保目标线程可以附着到 Java VM。

### 6.2 用默认 class loader 查找 Qt 加载的类

Android 上 Qt 使用自定义 class loader 加载应用中的部分 `.jar` 和 Java 类。直接调用原始 `JNIEnv::FindClass()` 可能找不到这些类；优先使用 `QJniEnvironment::findClass()`，因为它会搜索可用的 class loader，并优先使用 Qt 的缓存。

### 6.3 忽略 JNI 异常后的“连锁故障”

JNI 中有待处理异常时，后续许多 JNI 操作会失败或产生误导性的结果。不要只判断返回值，还要在可能抛异常的调用后调用：

```cpp
if (env.checkAndClearExceptions())
    return;
```

返回 `true` 表示确实清除了一项待处理异常。

### 6.4 把 `jclass`、`jfieldID` 和 `jmethodID` 当成同一种资源

`jclass` 是 Java 对象引用，受 JNI 引用生命周期影响；`jfieldID` 和 `jmethodID` 是运行时标识，不是普通 Java 对象引用。保存和释放策略不能混用。`findClass()` 返回缓存类时，Qt 文档明确说明可能返回缓存中的全局引用。

### 6.5 模板推导不能修正 Java 声明

```cpp
env.findMethod<jint>(clazz, "value");
```

这只表示“按推导出的 JNI 签名查找”，不会把 Java 中实际返回 `jlong` 的方法转换成 `jint`。如果推导类型与 Java 声明不一致，查找会失败，或者错误的手写签名会导致 JNI 层面的未定义行为。

### 6.6 注册 native 方法太晚

必须在 Java 第一次调用相应 native 方法之前注册。注册失败应检查返回值并记录类名、方法名和签名，否则 Java 侧通常只能看到笼统的 `UnsatisfiedLinkError`。

### 6.7 把 API 当作通用桌面 JNI 层

Qt 6.11.1 文档说明该 API 主要为 Android 设计和测试，其他平台不应默认拥有同样的运行时支持和验证范围。跨平台代码应把 JNI 调用隔离在 Android 平台实现中。

## 7. 与相关类型的协作

- `QJniObject`：保存 Java 对象、调用实例/静态方法，并对调用异常进行更高层封装。
- `QJniArray<T>`：包装 Java 数组，使用 `QJniEnvironment` 时可通过底层 JNI 句柄协作。
- `QtJniTypes`：通过 `Q_DECLARE_JNI_CLASS` 声明 Java 类类型，供模板查找和 native 方法注册使用。
- `JNINativeMethod`：描述 Java native 方法的名称、签名和 C++ 函数地址。
- `JNIEnv`、`JavaVM`：JNI 原始接口，分别受线程绑定和进程 VM 生命周期约束。

## 8. 逐项 API 说明

### 成员类型

#### `enum class QJniEnvironment::OutputMode`

控制 `checkAndClearExceptions()` 的输出策略：

- `Silent`：值为 `0`，清异常但不打印堆栈；
- `Verbose`：值为 `1`，把异常和堆栈回溯输出到 `stderr`。

### 构造与析构

#### `QJniEnvironment::QJniEnvironment()`

构造 JNI 环境对象，并把当前线程附着到 Java VM。对象只能在当前线程使用；如果环境无效，应使用 `isValid()` 检查。

#### `QJniEnvironment::~QJniEnvironment()`

`noexcept` 析构。析构前会清除待处理 Java 异常，并处理当前线程与 Java VM 的分离。不要把异常留到析构才检查，因为这样会丢失异常对应的具体 JNI 操作上下文。

### 异常处理

#### `bool QJniEnvironment::checkAndClearExceptions(OutputMode outputMode = OutputMode::Verbose)`

检查当前环境是否有待处理 Java 异常；如果有，则按 `outputMode` 清除异常并可打印堆栈。返回 `true` 表示清除过异常，返回 `false` 表示没有待处理异常。

#### `[static] bool QJniEnvironment::checkAndClearExceptions(JNIEnv *env, OutputMode outputMode = OutputMode::Verbose)`

检查并清除指定 `JNIEnv *` 上的待处理异常。适合已经在 native 函数参数中获得 `JNIEnv *` 的代码；返回值与成员重载相同。

### 类、字段和方法查找

#### `jclass QJniEnvironment::findClass(const char *className)`

通过可用 class loader 查找 Java 类，返回 `jclass`，找不到时返回 null。Qt Android 自定义 class loader 加载的类应优先使用此函数查找。对于内部缓存的类，函数可能返回缓存的全局引用。

类名使用 JNI 内部形式，例如 `org/qtproject/example/android/CustomClass`，不是 Java 源代码中的点号形式。

#### `[since 6.4] template <typename T> jfieldID QJniEnvironment::findField(jclass clazz, const char *fieldName)`

查找实例字段，字段签名由模板参数 `T` 推导。找不到字段返回 `nullptr`。模板类型必须与 Java 字段类型一致。

#### `[since 6.2] jfieldID QJniEnvironment::findField(jclass clazz, const char *fieldName, const char *signature)`

使用显式 JNI 签名查找实例字段。找不到字段返回 `nullptr`。适合签名需要清晰可见、或类型不能方便用模板表达的场景。

#### `[since 6.4] template <typename... Args> jmethodID QJniEnvironment::findMethod(jclass clazz, const char *methodName)`

查找实例方法，返回类型和参数类型由模板参数 `Args...` 推导。找不到方法返回 `nullptr`。模板参数顺序和 Qt 的 JNI 调用约定必须与 Java 方法声明一致。

#### `[since 6.2] jmethodID QJniEnvironment::findMethod(jclass clazz, const char *methodName, const char *signature)`

使用显式 JNI 签名查找实例方法。签名必须包括参数列表和返回类型，例如 `"(Ljava/lang/String;)V"`。

#### `[since 6.4] template <typename T> jfieldID QJniEnvironment::findStaticField(jclass clazz, const char *fieldName)`

查找静态字段，字段签名由模板参数 `T` 推导。找不到时返回 `nullptr`，并不会把实例字段当成静态字段匹配。

#### `[since 6.2] jfieldID QJniEnvironment::findStaticField(jclass clazz, const char *fieldName, const char *signature)`

使用显式签名查找静态字段。类、字段名、静态性质和签名必须全部匹配。

#### `[since 6.4] template <typename... Args> jmethodID QJniEnvironment::findStaticMethod(jclass clazz, const char *methodName)`

查找静态方法，签名由模板参数推导。找不到时返回 `nullptr`。调用时可把返回的 `jmethodID` 传给 `QJniObject::callStaticMethod()` 等接口。

#### `[since 6.2] jmethodID QJniEnvironment::findStaticMethod(jclass clazz, const char *methodName, const char *signature)`

使用显式签名查找静态方法。它只匹配静态方法，适合缓存类方法 ID 后反复调用。

### 环境和 VM

#### `[static] JNIEnv *QJniEnvironment::getJniEnv()`

返回当前线程的 `JNIEnv *`，并把当前线程附着到 Java VM。它适合需要一个原始指针而不需要完整环境对象生命周期管理的低层代码；返回的指针仍然不能跨线程使用。

#### `[since 6.2] bool QJniEnvironment::isValid() const`

判断该实例是否持有有效的 `JNIEnv` 对象。构造后若运行环境不可用，应先检查此值再解引用或调用查找函数。

#### `[static] JavaVM *QJniEnvironment::javaVM()`

返回当前进程的 Java VM 接口。Android 只允许一个 Java VM；该函数返回进程级接口，不是当前线程专属的 `JNIEnv`。

#### `JNIEnv *QJniEnvironment::jniEnv() const`

返回当前环境持有的 `JNIEnv *`。指针有效性和线程归属仍由 `QJniEnvironment` 对象及当前线程决定。

#### `JNIEnv &QJniEnvironment::operator*() const`

返回 JNI 环境对象的引用，允许写出 `(*env).FindClass(...)` 这类原始 JNI 调用。

#### `JNIEnv *QJniEnvironment::operator->() const`

返回 JNI 环境指针，允许直接写出 `env->FindClass(...)`、`env->GetMethodID(...)` 等调用。不要把返回指针保存到其他线程。

### native 方法注册

#### `template <typename Class> bool QJniEnvironment::registerNativeMethods(std::initializer_list<JNINativeMethod> methods)`

把 `methods` 注册到由 `QtJniTypes::Class` 表示的 Java 类。`Class` 必须通过 `Q_DECLARE_JNI_CLASS` 声明；普通自由函数使用 `Q_DECLARE_JNI_NATIVE_METHOD`，类静态成员函数使用当前作用域对应的 JNI native method 宏。

返回 `true` 表示注册成功，`false` 表示失败。

#### `bool QJniEnvironment::registerNativeMethods(const char *className, std::initializer_list<JNINativeMethod> methods)`

按 JNI 内部格式的类名注册一组 native 方法。方法数组由初始化列表提供，返回注册是否成功。

#### `bool QJniEnvironment::registerNativeMethods(jclass clazz, std::initializer_list<JNINativeMethod> methods)`

使用已有的 `jclass` 注册一组 native 方法。适合类已经通过 `findClass()` 查找并缓存的场景。

#### `bool QJniEnvironment::registerNativeMethods(const char *className, const JNINativeMethod[] methods, int size)`

按类名注册 C 数组形式的 `JNINativeMethod`，`size` 指明数组元素数量。每一项包含 Java 方法名、JNI 签名和要调用的 C++ 函数地址；必须在 Java 调用这些方法前完成注册。

#### `bool QJniEnvironment::registerNativeMethods(jclass clazz, const JNINativeMethod[] methods, int size)`

使用已有 `jclass` 和 C 数组注册 native 方法。除类来源不同外，规则与按类名的数组重载相同。

### 堆栈信息

#### `[static] QStringList QJniEnvironment::stackTrace(int exception)`

根据异常对象句柄返回该异常产生的 Java 堆栈信息。通常用于自定义异常记录；若只需要标准的检查和打印行为，直接使用 `checkAndClearExceptions()`。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成员类型 | `OutputMode` | 指定清理异常时是否输出堆栈。 | `Silent` 不打印，`Verbose` 写入 `stderr`。 |
| 构造 | `QJniEnvironment()` | 为当前线程取得 JNI 环境并附着到 Java VM。 | `JNIEnv` 不能跨线程共享。 |
| 析构 | `~QJniEnvironment()` | 清理待处理异常并处理线程分离。 | 不要依赖析构代替显式错误检查。 |
| 异常 | `checkAndClearExceptions(mode)` | 检查、清除当前环境的 Java 异常。 | 返回 `true` 表示确实清除过异常。 |
| 异常 | `checkAndClearExceptions(env, mode)` | 检查、清除指定 `JNIEnv *` 的异常。 | 适合已有 JNI 回调参数的函数。 |
| 查类 | `findClass(className)` | 使用可用 class loader 查找 Java 类。 | 使用 JNI `/` 类名；失败返回 null。 |
| 查字段 | `findField(clazz, name)` | 按模板推导签名查找实例字段。 | Qt 6.4 起；类型必须匹配。 |
| 查字段 | `findField(clazz, name, signature)` | 按显式签名查找实例字段。 | Qt 6.2 起；签名必须完整。 |
| 查方法 | `findMethod<Args...>(clazz, name)` | 按模板推导签名查找实例方法。 | Qt 6.4 起；返回/参数必须对应 Java 声明。 |
| 查方法 | `findMethod(clazz, name, signature)` | 按显式签名查找实例方法。 | Qt 6.2 起；失败返回 `nullptr`。 |
| 查字段 | `findStaticField(clazz, name)` | 按模板推导签名查找静态字段。 | Qt 6.4 起；不会匹配实例字段。 |
| 查字段 | `findStaticField(clazz, name, signature)` | 按显式签名查找静态字段。 | Qt 6.2 起；静态性质必须匹配。 |
| 查方法 | `findStaticMethod<Args...>(clazz, name)` | 按模板推导签名查找静态方法。 | Qt 6.4 起；失败返回 `nullptr`。 |
| 查方法 | `findStaticMethod(clazz, name, signature)` | 按显式签名查找静态方法。 | Qt 6.2 起；签名包含返回类型。 |
| 环境 | `getJniEnv()` | 获取并附着当前线程的 `JNIEnv *`。 | 指针只能在当前线程使用。 |
| 环境 | `isValid()` | 判断环境是否有效。 | 无效时不要使用 `operator->()`。 |
| VM | `javaVM()` | 返回当前进程的 `JavaVM *`。 | Android 进程通常只有一个 VM。 |
| 环境 | `jniEnv()` | 返回当前环境的 `JNIEnv *`。 | 不要跨线程保存。 |
| 注册 | `registerNativeMethods<Class>(methods)` | 按声明的 JNI 类注册 native 方法。 | 需要 `Q_DECLARE_JNI_CLASS` 和 native method 宏。 |
| 注册 | `registerNativeMethods(className, methods)` | 按类名注册初始化列表中的方法。 | Java 调用前必须完成。 |
| 注册 | `registerNativeMethods(clazz, methods)` | 按已有 `jclass` 注册方法。 | 先确认 `clazz` 有效。 |
| 注册 | `registerNativeMethods(className, methods, size)` | 按类名注册 C 数组方法。 | `size` 必须是数组元素数。 |
| 注册 | `registerNativeMethods(clazz, methods, size)` | 按已有 `jclass` 注册 C 数组方法。 | 返回 `false` 时立即处理错误。 |
| 堆栈 | `stackTrace(exception)` | 返回 Java 异常的堆栈信息。 | 需要有效异常句柄。 |
| 运算符 | `operator*()` | 以引用方式访问 `JNIEnv`。 | 仍受当前线程生命周期约束。 |
| 运算符 | `operator->()` | 以指针方式调用 JNI 函数。 | 不能把结果当跨线程句柄。 |

## 10. 使用判断

- 已经在 native 回调中拿到 `JNIEnv *`：使用静态 `checkAndClearExceptions()`，或在当前线程构造环境对象。
- 需要从普通 C++ 线程进入 Java：在该线程建立 `QJniEnvironment`，检查 `isValid()`，用完后显式检查异常。
- 需要频繁调用同一类的方法：查找并缓存 `jclass`、`jmethodID` 或 `jfieldID`，同时明确引用生命周期。
- 需要保存 Java 对象：使用 `QJniObject`，不要保存裸 `JNIEnv *`。
- 需要注册 native 方法：在 Java 首次调用前完成注册，并检查每个注册函数的返回值。
