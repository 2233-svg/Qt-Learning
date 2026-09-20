# QtJniTypes::JObject
> Qt 6.11.1 · Qt Core · 来自 `QtJniTypes::JObject`
## 作用定位
`QtJniTypes::JObject` 是 Qt Android JNI 类型系统中的 Java `Object` 基础包装类型，用于在 C++ 模板签名中表达 Java 对象类型。
## API 速查
| API | 是做什么的 |
|---|---|
| 类型别名/包装 | 表示 Java `java.lang.Object`。 |
| 与 `QJniObject` 协作 | 作为 JNI 调用签名和类型推导的一部分。 |
## 使用场景
编写 Android 平台专用 C++ 与 Java/Kotlin 互操作代码。
## 常见坑与经验
- 只在 Android/JNI 语境有意义，桌面平台应隔离编译。
- JNI 局部/全局引用生命周期必须按 JNI 规则管理。
- Java 异常和线程附加状态需要显式处理。
## 知识点覆盖
Android、JNI、Java 对象签名、平台条件编译、引用生命周期。
