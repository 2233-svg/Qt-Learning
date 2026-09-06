# QJniObject

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Jni对象”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QJniObject` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QJniObject>`
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

### 公有函数

- `QJniObject()`
- `QJniObject(const char *className)`
- `QJniObject(jclass clazz)`
- `QJniObject(jobject object)`
- `(since 6.4) QJniObject(const char *className, Args &&... args)`
- `(since 6.4) QJniObject(jclass clazz, Args &&... args)`
- `QJniObject(const char *className, const char *signature, ...)`
- `QJniObject(jclass clazz, const char *signature, ...)`
- `~QJniObject()`
- `(since 6.4) auto callMethod(const char *methodName, Args &&... args) const`
- `(since 6.4) auto callMethod(const char *methodName, const char *signature, Args &&... args) const`
- `(since 6.4) QJniObject callObjectMethod(const char *methodName, Args &&... args) const`
- `QJniObject callObjectMethod(const char *methodName, const char *signature, ...) const`
- `(since 6.2) QByteArray className() const`
- `auto getField(const char *fieldName) const`
- `QJniObject getObjectField(const char *fieldName) const`
- `QJniObject getObjectField(const char *fieldName, const char *signature) const`
- `bool isValid() const`
- `jobject object() const`
- `T object() const`
- `(since 6.2) jclass objectClass() const`
- `auto setField(const char *fieldName, Type value)`
- `auto setField(const char *fieldName, const char *signature, Type value)`
- `(since 6.8) void swap(QJniObject &other)`
- `QString toString() const`
- `QJniObject & operator=(T object)`

### 静态公有成员

- `(since 6.7) auto callStaticMethod(const char *methodName, Args &&... args)`
- `(since 6.4) auto callStaticMethod(const char *className, const char *methodName, Args &&... args)`
- `(since 6.4) auto callStaticMethod(jclass clazz, const char *methodName, Args &&... args)`
- `(since 6.4) auto callStaticMethod(jclass clazz, jmethodID methodId, Args &&... args)`
- `(since 6.4) auto callStaticMethod(const char *className, const char *methodName, const char *signature, Args &&... args)`
- `auto callStaticMethod(jclass clazz, const char *methodName, const char *signature, Args &&... args)`
- `(since 6.4) QJniObject callStaticObjectMethod(const char *className, const char *methodName, Args &&... args)`
- `(since 6.4) QJniObject callStaticObjectMethod(jclass clazz, const char *methodName, Args &&... args)`
- `QJniObject callStaticObjectMethod(jclass clazz, jmethodID methodId, ...)`
- `QJniObject callStaticObjectMethod(const char *className, const char *methodName, const char *signature, ...)`
- `QJniObject callStaticObjectMethod(jclass clazz, const char *methodName, const char *signature, ...)`
- `(since 6.4) auto construct(Args &&... args)`
- `QJniObject fromLocalRef(jobject localRef)`
- `QJniObject fromString(const QString &string)`
- `auto getStaticField(const char *fieldName)`
- `auto getStaticField(const char *className, const char *fieldName)`
- `auto getStaticField(jclass clazz, const char *fieldName)`
- `QJniObject getStaticObjectField(const char *className, const char *fieldName)`
- `QJniObject getStaticObjectField(jclass clazz, const char *fieldName)`
- `QJniObject getStaticObjectField(const char *className, const char *fieldName, const char *signature)`
- `QJniObject getStaticObjectField(jclass clazz, const char *fieldName, const char *signature)`
- `bool isClassAvailable(const char *className)`
- `auto setStaticField(const char *fieldName, Type value)`
- `auto setStaticField(const char *className, const char *fieldName, Type value)`
- `auto setStaticField(jclass clazz, const char *fieldName, Type value)`
- `auto setStaticField(const char *className, const char *fieldName, const char *signature, Type value)`
- `auto setStaticField(jclass clazz, const char *fieldName, const char *signature, Type value)`

### 相关非成员函数

- `bool operator!=(const QJniObject &o1, const QJniObject &o2)`
- `bool operator==(const QJniObject &o1, const QJniObject &o2)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QJniObject::QJniObject()`

**作用与语义：**

构造一个无效的 JNI 对象。

### `[explicit] QJniObject::QJniObject(const char *className)`

**作用与语义：**

通过调用默认构造函数 `className` 构建一个新的 JNI 对象。

**官方示例：**

```cpp
 QJniObject myJavaString("java/lang/String");
```

### `[explicit] QJniObject::QJniObject(jclass clazz)`

**作用与语义：**

通过调用默认构造函数 `clazz` 来构造一个新的 JNI 对象。
注意：QJniObject 会创建一个新的类引用`clazz`，并在该类被销毁时重新释放。在 QJniObject 之外创建的类的引用需要由调用者管理。

### `QJniObject::QJniObject(jobject object)`

**作用与语义：**

围绕 Java 对象 `object` 构建一个新的 JNI 对象。
注意：QJniObject 会保留对 Java 对象`object`的引用，并在销毁后释放。任何对 QJniObject `object` Java对象的引用都需要由调用者管理。在大多数情况下，除非你打算自己管理本地引用，否则绝不应用本地引用调用该函数。参见关于如何将本地引用转换为 QJniObject 的 `QJniObject::fromLocalRef()`。

### `[explicit, since 6.4] template <typename... Args> QJniObject::QJniObject(const char *className, Args &&... args)`

**作用与语义：**

通过调用`className`的构造函数（参数为`args`）来构造新的JNI对象。该构造器仅在所有`args`均为已知JNI类型时可用。

**官方示例：**

```cpp
 QJniEnvironment env;
 char* str = "Hello";
 jstring myJStringArg = env->NewStringUTF(str);
 QJniObject myNewJavaString("java/lang/String", myJStringArg);
```

### `[explicit, since 6.4] template <typename... Args> QJniObject::QJniObject(jclass clazz, Args &&... args)`

**作用与语义：**

通过调用构造函数，参数为 `args`，构造`clazz`构造新的 JNI 对象。该构造器仅在所有 `args` 均为已知 JNI 类型时可用。

**官方示例：**

```cpp
 QJniEnvironment env;
 jclass myClazz = env.findClass("org/qtproject/qt/TestClass");
 QJniObject(myClazz, 3);
```

### `[explicit] QJniObject::QJniObject(const char *className, const char *signature, ...)`

**作用与语义：**

通过调用`className`的构造函数，并`signature`指定后续参数的类型，构造一个新的JNI对象。

**官方示例：**

```cpp
 QJniEnvironment env;
 char* str = "Hello";
 jstring myJStringArg = env->NewStringUTF(str);
 QJniObject myNewJavaString("java/lang/String", "(Ljava/lang/String;)V", myJStringArg);
```

### `[explicit] QJniObject::QJniObject(jclass clazz, const char *signature, ...)`

**作用与语义：**

通过调用构造函数并指定后续参数的类型`signature`，从`clazz`构造新的JNI对象。

**官方示例：**

```cpp
 QJniEnvironment env;
 jclass myClazz = env.findClass("org/qtproject/qt/TestClass");
 QJniObject(myClazz, "(I)V", 3);
```

### `[noexcept] QJniObject::~QJniObject()`

**作用与语义：**

销毁JNI对象并释放JNI对象所持有的所有引用。

### `[since 6.4] template <typename ReturnType = void, typename... Args> auto QJniObject::callMethod(const char *methodName, Args &&... args) const`

**作用与语义：**

调用`methodName`方法，参数为`args`，返回该值（除非`Ret` `void`）。如果`Ret`是jobject类型，则返回的值将是`QJniObject`。
方法签名是在编译时从 `Ret` 和 `args` 类型推导出来的。`Ret` 可以是 `std::expected` 兼容的类型，返回一个值，也可以是被调用方法抛出的任何 Java 异常。

**官方示例：**

```cpp
 QJniObject myJavaString("org/qtproject/qt/TestClass");
 jint size = myJavaString.callMethod<jint>("length");
```

### `[since 6.4] template <typename ReturnType = void, typename... Args> auto QJniObject::callMethod(const char *methodName, const char *signature, Args &&... args) const`

**作用与语义：**

调用对象的方法`methodName`，`signature`指定后续参数的类型，`args`返回值（除非`Ret`被`void`）。如果`Ret`是jobject类型，则返回的值将是`QJniObject`。

**官方示例：**

```cpp
 QJniObject myJavaString("org/qtproject/qt/TestClass");
 jint index = myJavaString.callMethod<jint>("indexOf", "(I)I", 0x0051);
```

### `[since 6.4] template <typename Ret, typename... Args> QJniObject QJniObject::callObjectMethod(const char *methodName, Args &&... args) const`

**作用与语义：**

调用 Java 对象方法`methodName`，参数`args`，返回返回的 Java 对象的新`QJniObject`。
方法签名是在编译时从 `Ret` 和 `args` 类型推导出来的。`Ret`可以是`std::expected`兼容的类型，返回一个值，也可以是被调用方法抛出的任何 Java 异常。

**官方示例：**

```cpp
 QJniObject myJavaString = QJniObject::fromString("Hello, Java");
 QJniObject myJavaString2 = myJavaString1.callObjectMethod<jstring>("toString");
```

### `QJniObject QJniObject::callObjectMethod(const char *methodName, const char *signature, ...) const`

**作用与语义：**

调用 Java 对象的方法 `methodName`，`signature` 指定后续参数的类型。

**官方示例：**

```cpp
 QJniObject myJavaString = QJniObject::fromString("Hello, Java");
 QJniObject mySubstring = myJavaString.callObjectMethod("substring",
                                                        "(II)Ljava/lang/String;", 7, 11);
```

### `[static, since 6.7] template < typename Klass, typename ReturnType = void, typename... Args > auto QJniObject::callStaticMethod(const char *methodName, Args &&... args)`

**作用与语义：**

调用类`Klass`上的静态方法`methodName`，返回类型`Ret`的值（除非`Ret`是`void`）。如果`Ret`是jobject类型，则返回的值将是`QJniObject`。
方法签名是在编译时从 `Ret` 和 `args` 类型推导出来的。`Klass` 需要是带有映射到 Java 类型的注册类型 C 类型。`Ret` 可以是`std::expected`兼容的类型，返回一个值，也可以是被调用方法抛出的任何 Java 异常。

### `[static, since 6.4] template <typename ReturnType = void, typename... Args> auto QJniObject::callStaticMethod(const char *className, const char *methodName, Args &&... args)`

**作用与语义：**

调用类 `className` 上的静态方法 `methodName`，参数为 `args`，返回类型 `Ret` 的值（除非 `Ret` `void`）。如果 `Ret` 是 jobject 类型，则返回的值将是 `QJniObject`。
方法签名是在编译时从 `Ret` 和 `args` 类型推导出来的。`Ret`可以是`std::expected`兼容的类型，返回一个值，也可以是被调用方法抛出的任何 Java 异常。

**官方示例：**

```cpp
 jint value = QJniObject::callStaticMethod<jint>("MyClass", "staticMethod");
```

### `[static, since 6.4] template <typename ReturnType = void, typename... Args> auto QJniObject::callStaticMethod(jclass clazz, const char *methodName, Args &&... args)`

**作用与语义：**

调用静态方法 `methodName` on `clazz`，返回类型 `Ret` 的值（除非 `Ret` `void`）。如果 `Ret` 是 jobject 类型，则返回的值将是 `QJniObject`。
方法签名是在编译时从 `Ret` 和 `args`类型推导出来的。`Ret`可以是`std::expected`兼容的类型，返回一个值，也可以是被调用方法抛出的任何 Java 异常。

**官方示例：**

```cpp
 QJniEnvironment env;
 jclass javaMathClass = env.findClass("java/lang/Math");
 jdouble randNr = QJniObject::callStaticMethod<jdouble>(javaMathClass, "random");
```

### `[static, since 6.4] template <typename ReturnType = void, typename... Args> auto QJniObject::callStaticMethod(jclass clazz, jmethodID methodId, Args &&... args)`

**作用与语义：**

调用类`clazz`中 `methodId` 识别的静态方法，并返回类型 `Ret`（除非 `Ret` `void`）。如果 `Ret` 是 jobject 类型，则返回的值将是 `QJniObject`。
当`clazz`和`methodId`已经从之前的操作缓存出来时，这非常有用。

**官方示例：**

```cpp
 QJniEnvironment env;
 jclass javaMathClass = env.findClass("java/lang/Math");
 jmethodID methodId = env.findStaticMethod(javaMathClass, "max", "(II)I");
 if (methodId != 0) {
     jint a = 2;
     jint b = 4;
     jint max = QJniObject::callStaticMethod<jint>(javaMathClass, methodId, a, b);
 }
```

### `[static, since 6.4] template <typename Ret = void, typename... Args> auto QJniObject::callStaticMethod(const char *className, const char *methodName, const char *signature, Args &&... args)`

**作用与语义：**

调用静态方法，`methodName` 来自类 `className`，`signature` 指定后续参数的类型`args`。返回方法的结果（除非`Ret` `void`）。如果 `Ret` 是 jobject 类型，则返回的值将是 `QJniObject`。

**官方示例：**

```cpp
 jint a = 2;
 jint b = 4;
 jint max = QJniObject::callStaticMethod<jint>("java/lang/Math", "max", "(II)I", a, b);
```

### `[static] template <typename Ret = void, typename... Args> auto QJniObject::callStaticMethod(jclass clazz, const char *methodName, const char *signature, Args &&... args)`

**作用与语义：**

调用静态方法`methodName` 从 `clazz` 中，`signature` 指定后续参数的类型。返回方法的结果（除非`Ret` `void`）。如果 `Ret` 是 jobject 类型，则返回的值将是 `QJniObject`。

**官方示例：**

```cpp
 QJniEnvironment env;
 jclass javaMathClass = env.findClass("java/lang/Math");
 jint a = 2;
 jint b = 4;
 jint max = QJniObject::callStaticMethod<jint>(javaMathClass, "max", "(II)I", a, b);
```

### `[static, since 6.4] template <typename Ret, typename... Args> QJniObject QJniObject::callStaticObjectMethod(const char *className, const char *methodName, Args &&... args)`

**作用与语义：**

调用类`className`上的静态方法，`methodName`，传递参数`args`，并返回返回的 Java 对象的新 `QJniObject`。
方法签名是在编译时从`Ret`和`args`类型推导出来的。`Ret`可以是`std::expected`兼容的类型，返回一个值，也可以是被调用方法抛出的任何Java异常。

**官方示例：**

```cpp
 QJniObject string = QJniObject::callStaticObjectMethod<jstring>("CustomClass", "getClassName");
```

### `[static, since 6.4] template <typename Ret, typename... Args> QJniObject QJniObject::callStaticObjectMethod(jclass clazz, const char *methodName, Args &&... args)`

**作用与语义：**

调用带有`methodName` `clazz`的静态方法，传递参数`args`，并返回返回的 Java 对象的新 `QJniObject`。

### `[static] QJniObject QJniObject::callStaticObjectMethod(jclass clazz, jmethodID methodId, ...)`

**作用与语义：**

调用由`methodId`识别的静态方法，并`clazz`类中的任意后续参数。当`clazz`和`methodId`已经从之前操作缓存时非常有用。

**官方示例：**

```cpp
 QJniEnvironment env;
 jclass clazz = env.findClass("java/lang/String");
 jmethodID methodId = env.findStaticMethod(clazz, "valueOf", "(I)Ljava/lang/String;");
 if (methodId != 0)
     QJniObject str = QJniObject::callStaticObjectMethod(clazz, methodId, 10);
```

### `[static] QJniObject QJniObject::callStaticObjectMethod(const char *className, const char *methodName, const char *signature, ...)`

**作用与语义：**

调用静态方法`methodName`类`className`，`signature`指定后续参数的类型。

**官方示例：**

```cpp
 QJniObject thread = QJniObject::callStaticObjectMethod("java/lang/Thread", "currentThread",
                                                        "()Ljava/lang/Thread;");
 QJniObject string = QJniObject::callStaticObjectMethod("java/lang/String", "valueOf",
                                                        "(I)Ljava/lang/String;", 10);
```

### `[static] QJniObject QJniObject::callStaticObjectMethod(jclass clazz, const char *methodName, const char *signature, ...)`

**作用与语义：**

调用静态方法，`methodName` 来自类 `clazz`，`signature` 指定后续参数的类型。

### `[since 6.2] QByteArray QJniObject::className() const`

**作用与语义：**

返回`QJniObject`所持有的类对象名称作为`QByteArray`。

### `[static, since 6.4] template <typename Class, typename... Args> auto QJniObject::construct(Args &&... args)`

**作用与语义：**

构造一个等价于 `Class` 的 Java 类实例，返回包含 JNI 对象的`QJniObject`。`args` 中的参数传递给 Java 构造器。
该功能仅在所有`args`均为已知JNI类型时可用。

**官方示例：**

```cpp
 QJniObject javaString = QJniObject::construct<jstring>();
```

### `[static] QJniObject QJniObject::fromLocalRef(jobject localRef)`

**作用与语义：**

从本地JNI引用`localRef`创建`QJniObject`。该函数会获得`localRef`的所有权，并在返回前释放它。
注意：仅在本地 JNI 引用时调用该函数。例如，大多数原始 JNI 调用通过 JNI 环境返回 Java 对象的本地引用。

**官方示例：**

```cpp
 jobject localRef = env->GetObjectArrayElement(array, index);
 QJniObject element = QJniObject::fromLocalRef(localRef);
```

### `[static] QJniObject QJniObject::fromString(const QString &string)`

**作用与语义：**

从`QString` `string`创建一个 Java 字符串，并返回包含该字符串的`QJniObject`。

**官方示例：**

```cpp
 QString myQString = "QString";
 QJniObject myJavaString = QJniObject::fromString(myQString);
```

### `template <typename Type> auto QJniObject::getField(const char *fieldName) const`

**作用与语义：**

检索场`fieldName`的值。

**官方示例：**

```cpp
 QJniObject volumeControl("org/qtproject/qt/TestClass");
 jint fieldValue = volumeControl.getField<jint>("FIELD_NAME");
```

### `template <typename T> QJniObject QJniObject::getObjectField(const char *fieldName) const`

**作用与语义：**

从场`fieldName`中检索一个JNI对象。

**官方示例：**

```cpp
 QJniObject field = jniObject.getObjectField<jstring>("FIELD_NAME");
```

### `QJniObject QJniObject::getObjectField(const char *fieldName, const char *signature) const`

**作用与语义：**

从场中`fieldName`与`signature`检索一个JNI对象。
注意：该函数可在不使用模板类型的情况下使用。

**官方示例：**

```cpp
 QJniObject field = jniObject.getObjectField("FIELD_NAME", "Ljava/lang/String;");
```

### `[static] template <typename Klass, typename T> auto QJniObject::getStaticField(const char *fieldName)`

**作用与语义：**

从类`Klass`的静态字段`fieldName`中获取值。
`Klass`需要是C类型，并且有注册类型映射到Java类型。

### `[static] template <typename Type> auto QJniObject::getStaticField(const char *className, const char *fieldName)`

**作用与语义：**

从类`className`的静态字段`fieldName`中获取该值。

### `[static] template <typename Type> auto QJniObject::getStaticField(jclass clazz, const char *fieldName)`

**作用与语义：**

从`clazz`的静态场`fieldName`中获取该值。

### `[static] template <typename T> QJniObject QJniObject::getStaticObjectField(const char *className, const char *fieldName)`

**作用与语义：**

从类`className`上的字段`fieldName`中检索对象。

**官方示例：**

```cpp
 QJniObject jobj = QJniObject::getStaticObjectField<jstring>("class/with/Fields", "FIELD_NAME");
```

### `[static] template <typename T> QJniObject QJniObject::getStaticObjectField(jclass clazz, const char *fieldName)`

**作用与语义：**

从`clazz`场`fieldName`中取回该物体。

**官方示例：**

```cpp
 QJniObject jobj = QJniObject::getStaticObjectField<jstring>(clazz, "FIELD_NAME");
```

### `[static] QJniObject QJniObject::getStaticObjectField(const char *className, const char *fieldName, const char *signature)`

**作用与语义：**

从场`fieldName`中获取带有类`className` `signature`的JNI对象。
注意：该函数可在不使用模板类型的情况下使用。

**官方示例：**

```cpp
 QJniObject jobj = QJniObject::getStaticObjectField("class/with/Fields", "FIELD_NAME",
                                                    "Ljava/lang/String;");
```

### `[static] QJniObject QJniObject::getStaticObjectField(jclass clazz, const char *fieldName, const char *signature)`

**作用与语义：**

从场`fieldName`中检索JNI对象，`signature`来自类`clazz`。
注意：该函数可在不使用模板类型的情况下使用。

**官方示例：**

```cpp
 QJniObject jobj = QJniObject::getStaticObjectField(clazz, "FIELD_NAME", "Ljava/lang/String;");
```

### `[static] bool QJniObject::isClassAvailable(const char *className)`

**作用与语义：**

如果 Java 类 `className` 可用，则返回 true。

**官方示例：**

```cpp
 if (QJniObject::isClassAvailable("java/lang/String")) {
     // condition statement
 }
```

### `bool QJniObject::isValid() const`

**作用与语义：**

如果该实例包含有效的 Java 对象，则返回为真。

**官方示例：**

```cpp
 QJniObject qjniObject;                        // ==> isValid() == false
 QJniObject qjniObject(0)                      // ==> isValid() == false
 QJniObject qjniObject("could/not/find/Class") // ==> isValid() == false
```

### `template <typename T> T QJniObject::object() const`

**作用与语义：**

返回`QJniObject`所持有的对象，可以作为jobject或类型T。T可以是JNI对象类型之一。
注意：返回的对象仍会被该`QJniObject`保持存活。为了让该对象在该`QJniObject`的生命周期之外保持存活，例如记录以备后用，最简单的方法是将其存储在另一个具有适当生命周期的`QJniObject`中。或者，你也可以创建一个新的全局引用并存储该对象，完成后注意将其释放。

**官方示例：**

```cpp
 QJniObject string = QJniObject::fromString("Hello, JNI");
 jstring jstring = string.object<jstring>();
```

### `[since 6.2] jclass QJniObject::objectClass() const`

**作用与语义：**

返回`QJniObject`所持有的类对象作为`jclass`。
注意：返回的对象仍会被该`QJniObject`保持存活。为了让该对象在该`QJniObject`的生命周期之外保持存活，例如记录以备后用，最简单的方法是将其存储在另一个具有适当寿命的`QJniObject`中。或者，你可以创建一个新的全局引用并存储该对象，完成后注意将其释放。

### `template <typename Ret = void, typename Type> auto QJniObject::setField(const char *fieldName, Type value)`

**作用与语义：**

将`fieldName`的值设为`value`。

**官方示例：**

```cpp
 QJniObject obj;
 obj.setField<jint>("AN_INT_FIELD", 10);
 jstring myString = ...;
 obj.setField<jstring>("A_STRING_FIELD", myString);
```

### `template <typename Ret = void, typename Type> auto QJniObject::setField(const char *fieldName, const char *signature, Type value)`

**作用与语义：**

将`fieldName` 的值设为`value` `signature`。

**官方示例：**

```cpp
 QJniObject stringArray = ...;
 QJniObject obj = ...;
 obj.setObjectField<jobjectArray>("KEY_VALUES", "([Ljava/lang/String;)V",
                            stringArray.object<jobjectArray>())
```

### `[static] template < typename Klass, typename Ret = void, typename Type > auto QJniObject::setStaticField(const char *fieldName, Type value)`

**作用与语义：**

将类`Klass`的静态场`fieldName`设为`value`。
`Klass`需要是一个C类型，并且有一个注册型映射到Java类型。

### `[static] template <typename Ret = void, typename Type> auto QJniObject::setStaticField(const char *className, const char *fieldName, Type value)`

**作用与语义：**

将类的静态场`fieldName`设为`className`为`value`。

### `[static] template <typename Ret = void, typename Type> auto QJniObject::setStaticField(jclass clazz, const char *fieldName, Type value)`

**作用与语义：**

将类`clazz`的静态场`fieldName`设置为`value`。

### `[static] template <typename Ret = void, typename Type> auto QJniObject::setStaticField(const char *className, const char *fieldName, const char *signature, Type value)`

**作用与语义：**

用`signature`的设定器设置班级`className`的静态场`fieldName`为`value`。

### `[static] template <typename Ret = void, typename Type> auto QJniObject::setStaticField(jclass clazz, const char *fieldName, const char *signature, Type value)`

**作用与语义：**

用`signature`设置者设置`clazz`的静态场`fieldName`为`value`。

### `[noexcept, since 6.8] void QJniObject::swap(QJniObject &other)`

**作用与语义：**

将该对象与`other`交换。此操作非常快速且从未失败。

### `QString QJniObject::toString() const`

**作用与语义：**

返回一个带有 Java 对象字符串表示的 `QString`。调用 Java String 对象的函数是获取实际字符串数据的便捷方式。

**官方示例：**

```cpp
 QJniObject string = ...; //  "Hello Java"
 QString qstring = string.toString(); // "Hello Java"
```

### `template <typename T, std::enable_if_t<std::is_convertible_v<T, jobject>, bool> = true> QJniObject &QJniObject::operator=(T object)`

**作用与语义：**

用 `object` 替换当前对象。旧的 Java 对象将被释放。

### `bool operator!=(const QJniObject &o1, const QJniObject &o2)`

**作用与语义：**

如果`o1`持有与`o2`不同的对象引用，则返回为真。

### `bool operator==(const QJniObject &o1, const QJniObject &o2)`

**作用与语义：**

如果两个对象 `o1` 和 `o2` 引用同一个 Java 对象，或者两者都是 NULL，则返回 true。其他情况下，返回 false。

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

`QJniObject` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
