# QJniEnvironment

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“JniEnvironment”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QJniEnvironment` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QJniEnvironment>`
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

- `enum class OutputMode { Silent, Verbose }`

### 公有函数

- `QJniEnvironment()`
- `~QJniEnvironment()`
- `bool checkAndClearExceptions(QJniEnvironment::OutputMode outputMode = OutputMode::Verbose)`
- `jclass findClass(const char *className)`
- `(since 6.4) jfieldID findField(jclass clazz, const char *fieldName)`
- `(since 6.2) jfieldID findField(jclass clazz, const char *fieldName, const char *signature)`
- `(since 6.4) jmethodID findMethod(jclass clazz, const char *methodName)`
- `(since 6.2) jmethodID findMethod(jclass clazz, const char *methodName, const char *signature)`
- `(since 6.4) jfieldID findStaticField(jclass clazz, const char *fieldName)`
- `(since 6.2) jfieldID findStaticField(jclass clazz, const char *fieldName, const char *signature)`
- `(since 6.4) jmethodID findStaticMethod(jclass clazz, const char *methodName)`
- `(since 6.2) jmethodID findStaticMethod(jclass clazz, const char *methodName, const char *signature)`
- `(since 6.2) bool isValid() const`
- `JNIEnv * jniEnv() const`
- `bool registerNativeMethods(std::initializer_list<JNINativeMethod> methods)`
- `bool registerNativeMethods(const char *className, std::initializer_list<JNINativeMethod> methods)`
- `bool registerNativeMethods(jclass clazz, std::initializer_list<JNINativeMethod> methods)`
- `bool registerNativeMethods(const char *className, const JNINativeMethod[] methods, int size)`
- `bool registerNativeMethods(jclass clazz, const JNINativeMethod[] methods, int size)`
- `JNIEnv & operator*() const`
- `JNIEnv * operator->() const`

### 静态公有成员

- `bool checkAndClearExceptions(JNIEnv *env, QJniEnvironment::OutputMode outputMode = OutputMode::Verbose)`
- `JNIEnv * getJniEnv()`
- `JavaVM * javaVM()`
- `QStringList stackTrace(int exception)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QJniEnvironment::QJniEnvironment()`

**作用与语义：**

构建一个新的JNI环境对象，并将当前线程附加到Java虚拟机上。

### `[noexcept] QJniEnvironment::~QJniEnvironment()`

**作用与语义：**

将当前线程与 Java 虚拟机分离，并销毁`QJniEnvironment`对象。通过调用 `checkAndClearExceptions()` 清除任何待处理的异常。

### `bool QJniEnvironment::checkAndClearExceptions(QJniEnvironment::OutputMode outputMode = OutputMode::Verbose)`

**作用与语义：**

根据`outputMode`，会无声地或报告栈回溯，清理任何待处理的异常。
与内部处理异常的`QJniObject`不同，如果你通过`JNIEnv`直接调用JNI，你需要在调用后清除所有潜在异常。有关`JNIEnv`可能抛出异常的调用的更多信息，请参见JNI函数。
退货在处理待处理的例外时才`true`。

### `[static] bool QJniEnvironment::checkAndClearExceptions(JNIEnv *env, QJniEnvironment::OutputMode outputMode = OutputMode::Verbose)`

**作用与语义：**

根据`outputMode`，可以静默地或报告栈回溯，清除`env`的待处理异常。这在你已经有`JNIEnv`指针时非常有用，比如原生函数实现。
与内部处理异常的`QJniObject`不同，如果你通过`JNIEnv`直接调用JNI，你需要在调用后清除所有潜在的异常。有关`JNIEnv`可能抛出异常的调用的更多信息，请参见JNI函数。
退货在处理待处理的例外时才会`true`。

### `jclass QJniEnvironment::findClass(const char *className)`

**作用与语义：**

使用所有可用的类加载器搜索`className`。Android 上的 Qt 使用自定义类加载器加载所有.jar文件，必须使用它来查找该类加载器创建的任何类，因为使用默认类加载器时这些类不可见。
如果找不到`className`，返回类指针或空指针。
该函数的一个用例是寻找一个类来调用一个 JNI 方法，该方法需要一个 `jclass`。这在对同一类对象进行多个 JNI 调用时非常有用，这比每次调用中使用类名稍快一些。此外，该调用会先查找内部缓存的类，然后再调用 JNI 调用，并在找到时返回此类类。以下代码片段创建了该类 `CustomClass` 的实例，然后调用了 `printFromJava()` 方法：
注意：此调用返回的是内部缓存类对类对象的全局引用。

**官方示例：**

```cpp
 QJniEnvironment env;
 jclass javaClass = env.findClass("org/qtproject/example/android/CustomClass");
 QJniObject javaMessage = QJniObject::fromString("findClass example");
 QJniObject::callStaticMethod<void>(javaClass, "printFromJava",
                                    "(Ljava/lang/String;)V", javaMessage.object<jstring>());
```

### `[since 6.4] template <typename T> jfieldID QJniEnvironment::findField(jclass clazz, const char *fieldName)`

**作用与语义：**

搜索类的成员字段`clazz`。字段由其`fieldName`指定。字段的签名由模板参数推导出来。
如果找不到字段，返回字段 ID 或`nullptr`。

### `[since 6.2] jfieldID QJniEnvironment::findField(jclass clazz, const char *fieldName, const char *signature)`

**作用与语义：**

搜索类 `clazz` 的成员域。该域由其`fieldName`和`signature`指定。
如果找不到字段，返回字段ID或`nullptr`。
这种方法的一个用例是搜索类字段并缓存其 ID，以便以后用于获取和设置字段。

### `[since 6.4] template <typename... Args> jmethodID QJniEnvironment::findMethod(jclass clazz, const char *methodName)`

**作用与语义：**

搜索类的实例方法`clazz`。方法由其`methodName`指定，签名则从模板参数中推导出来。
如果找不到方法，返回方法 ID 或 `nullptr`。

### `[since 6.2] jmethodID QJniEnvironment::findMethod(jclass clazz, const char *methodName, const char *signature)`

**作用与语义：**

搜索类的实例方法`clazz`。该方法由其`methodName`和`signature`指定。
如果找不到方法，返回方法 ID 或 `nullptr`。
该方法的一个用例是搜索类方法并缓存其 ID，以便以后调用这些方法。

### `[since 6.4] template <typename T> jfieldID QJniEnvironment::findStaticField(jclass clazz, const char *fieldName)`

**作用与语义：**

搜索类`clazz`的静态字段。字段由其`fieldName`指定。字段的签名由模板参数推导出来。
如果找不到字段，返回字段 ID 或`nullptr`。

### `[since 6.2] jfieldID QJniEnvironment::findStaticField(jclass clazz, const char *fieldName, const char *signature)`

**作用与语义：**

搜索类`clazz`的静态域。该域由其`fieldName`和`signature`指定。
如果找不到字段，返回字段ID或`nullptr`。
这种方法的一个用例是搜索类字段并缓存其 ID，以便以后用于获取和设置字段。

### `[since 6.4] template <typename... Args> jmethodID QJniEnvironment::findStaticMethod(jclass clazz, const char *methodName)`

**作用与语义：**

搜索类的实例方法`clazz`。方法由其`methodName`指定，签名则从模板参数中推导出来。
如果找不到方法，返回方法 ID 或 `nullptr`。

**官方示例：**

```cpp
 QJniEnvironment env;
 jclass javaClass = env.findClass("org/qtproject/example/android/CustomClass");
 jmethodID methodId = env.findStaticMethod<void, jstring>(javaClass, "staticJavaMethod");
 QJniObject javaMessage = QJniObject::fromString("findStaticMethod example");
 QJniObject::callStaticMethod<void>(javaClass,
                                    methodId,
                                    javaMessage.object<jstring>());
```

### `[since 6.2] jmethodID QJniEnvironment::findStaticMethod(jclass clazz, const char *methodName, const char *signature)`

**作用与语义：**

搜索类`clazz`的静态方法。该方法由其`methodName`和`signature`指定。
如果找不到方法，返回方法 ID 或 `nullptr`。
该方法的一个用例是搜索类方法并缓存其 ID，以便以后调用这些方法。

**官方示例：**

```cpp
 QJniEnvironment env;
 jclass javaClass = env.findClass("org/qtproject/example/android/CustomClass");
 jmethodID methodId = env.findStaticMethod(javaClass,
                                           "staticJavaMethod",
                                           "(Ljava/lang/String;)V");
 QJniObject javaMessage = QJniObject::fromString("findStaticMethod example");
 QJniObject::callStaticMethod<void>(javaClass,
                                    methodId,
                                    javaMessage.object<jstring>());
```

### `[static] JNIEnv *QJniEnvironment::getJniEnv()`

**作用与语义：**

返回当前线程的JNIEnv指针。
当前线程将连接到 Java 虚拟机。

### `[since 6.2] bool QJniEnvironment::isValid() const`

**作用与语义：**

如果该实例包含有效的 JNIEnv 对象，返回`true`。

### `[static] JavaVM *QJniEnvironment::javaVM()`

**作用与语义：**

返回当前进程的 Java 虚拟机接口。虽然每个进程可能允许多个 Java 虚拟机，但 Android 只允许一个。

### `JNIEnv *QJniEnvironment::jniEnv() const`

**作用与语义：**

返回JNI环境的`JNIEnv`指针。

### `template <typename Class> bool QJniEnvironment::registerNativeMethods(std::initializer_list<JNINativeMethod> methods)`

**作用与语义：**

`methods` Java方法与`Class`表示的Java类注册，并返回注册是否成功。
`Class`类型必须在`QtJniTypes`命名空间内使用 `Q_DECLARE_JNI_CLASS` 宏声明。以自由 C 或 C 函数实现的函数必须使用`Q_DECLARE_JNI_NATIVE_METHOD`宏之一声明，并通过 `Q_JNI_NATIVE_METHOD` 宏传递到注册中。
对于作为静态类成员函数实现的函数，应使用作用域函数的宏。

**官方示例：**

```cpp
 // C++ side

 Q_DECLARE_JNI_CLASS(MyJavaType, "my/java/Type")

 static void nativeFunction(JNIEnv *env, jobject thiz, jlong id)
 {
     // ...
 }
 Q_DECLARE_JNI_NATIVE_METHOD(nativeFunction)

 Q_DECL_EXPORT jint JNICALL JNI_OnLoad(JavaVM *vm, void *reserved)
 {
     QJniEnvironment env;
     env.registerNativeMethods<QtJniTypes::MyJavaType>({
         Q_JNI_NATIVE_METHOD(nativeFunction)
     });
 }

 // Java side
 public class MyJavaType
 {
     native public nativeFunction(long id);
 }
```

### `bool QJniEnvironment::registerNativeMethods(const char *className, std::initializer_list<JNINativeMethod> methods)`

**作用与语义：**

为 Java 类 `className` `methods` 注册本地函数方法。注册成功时返回 `true`，否则返回`false`。

### `bool QJniEnvironment::registerNativeMethods(jclass clazz, std::initializer_list<JNINativeMethod> methods)`

**作用与语义：**

在 Java 类 `clazz` `methods` 中注册本地函数方法。如果注册成功，返回`true`，否则返回`false`。

### `bool QJniEnvironment::registerNativeMethods(const char *className, const JNINativeMethod[] methods, int size)`

**作用与语义：**

在数组中注册大小为`size`的 Java 方法，`methods` 每个方法都可以调用类 `className` 的本地 C 函数。这些方法必须在尝试调用前注册。
如果注册成功，退货`true`，否则就`false`。
方法数组中的每个元素由以下组成：
- Java 方法名称
- 方法签名
- 将要执行的C函数

**官方示例：**

```cpp
 const JNINativeMethod methods[] =
                         {{"callNativeOne", "(I)V", reinterpret_cast<void *>(fromJavaOne)},
                         {"callNativeTwo", "(I)V", reinterpret_cast<void *>(fromJavaTwo)}};
 QJniEnvironment env;
 env.registerNativeMethods("org/qtproject/android/TestJavaClass", methods, 2);
```

### `bool QJniEnvironment::registerNativeMethods(jclass clazz, const JNINativeMethod[] methods, int size)`

**作用与语义：**

该重载使用之前缓存的 jclass 实例`clazz`。

**官方示例：**

```cpp
 JNINativeMethod methods[] {{"callNativeOne", "(I)V", reinterpret_cast<void *>(fromJavaOne)},
                            {"callNativeTwo", "(I)V", reinterpret_cast<void *>(fromJavaTwo)}};
 QJniEnvironment env;
 jclass clazz = env.findClass("org/qtproject/android/TestJavaClass");
 env.registerNativeMethods(clazz, methods, 2);
```

### `[static] QStringList QJniEnvironment::stackTrace(int exception)`

**作用与语义：**

返回导致`exception`被抛弃的栈跟踪。

### `JNIEnv &QJniEnvironment::operator*() const`

**作用与语义：**

返回JNI环境的`JNIEnv`对象。

### `JNIEnv *QJniEnvironment::operator->() const`

**作用与语义：**

提供访问JNI环境的`JNIEnv`指针。

### `enum class OutputMode { Silent, Verbose }`

**作用与语义：**

- `QJniEnvironment::OutputMode::Silent`：`0`;例外被无声清理
- `QJniEnvironment::OutputMode::Verbose`：`1`;将异常及其堆栈回溯作为错误打印到`stderr`流。

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

`QJniEnvironment` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
