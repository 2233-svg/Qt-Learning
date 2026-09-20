# QJniEnvironment
> Qt 6.11.1 · Qt Core · 来自 `QJniEnvironment`

## 作用定位
`QJniEnvironment` 提供当前线程的 `JNIEnv*` 访问与 Java 异常检查/清除，负责让 Qt C++ 代码安全进入 Android JNI 边界。

## API 速查
| API | 是做什么的 |
|---|---|
| `operator->()` | 访问底层 `JNIEnv` 函数表。|
| `jniEnv()` | 取得原生 `JNIEnv*`。|
| `checkAndClearExceptions()` | 检查并清除待处理 Java 异常。|
| `findClass()` | 查找 Java 类。|
| `registerNativeMethods()` | 注册 native 方法。|

## 使用场景
调用 Java 平台 API、注册 JNI 回调、检查 Java 侧调用失败。

## 常见坑与经验
- `JNIEnv*` 只对当前已附着线程有效，不能缓存并跨线程传递。
- Java 异常未清除时，后续 JNI 调用往往失败；每个关键调用边界都应检查。
- class loader 上下文在 Android 应用中很关键，原生线程直接 `FindClass` 可能找不到应用类。

## 知识点覆盖
JNI、线程附着、Java 异常、局部引用、class loader、原生回调。
