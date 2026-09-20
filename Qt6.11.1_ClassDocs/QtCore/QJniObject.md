# QJniObject
> Qt 6.11.1 · Qt Core · 来自 `QJniObject`

## 作用定位
`QJniObject` 是 Java 对象、类引用和方法调用的 C++ RAII 封装，减少手工处理 JNI 引用与方法签名的样板代码。

## API 速查
| API | 是做什么的 |
|---|---|
| `isValid()` | 判断是否持有有效 Java 引用。|
| `object()` | 获取底层 `jobject`。|
| `callMethod()` | 调用实例 Java 方法。|
| `callStaticMethod()` | 调用静态 Java 方法。|
| `getField()` / `setField()` | 读取或写入实例字段。|
| `getStaticField()` | 读取静态字段。|
| `fromString()` / `toString()` | 在 `QString` 与 Java String 间转换。|
| `construct()` | 调用 Java 构造函数创建对象。|

## 使用场景
Qt Android 代码调用系统 Intent、ContentResolver 或应用自定义 Java helper。

## 常见坑与经验
- 方法签名必须与 JVM 描述符匹配；传错签名常表现为方法找不到或 pending exception。
- 不要把 `jobject` 裸引用跨线程或长期保存；交给 `QJniObject` 或显式 global reference 管理。
- Java 调用后使用 `QJniEnvironment::checkAndClearExceptions()` 检查异常。

## 知识点覆盖
JNI 对象、方法签名、RAII、Java String、局部/全局引用、异常检查。
