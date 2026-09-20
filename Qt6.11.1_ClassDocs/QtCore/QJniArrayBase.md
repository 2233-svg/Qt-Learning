# QJniArrayBase
> Qt 6.11.1 · Qt Core · 来自 `QJniArrayBase`

## 作用定位
`QJniArrayBase` 是 Java JNI 数组封装的共同基础，统一管理数组对象引用、长度和基础访问。

## API 速查
| API | 是做什么的 |
|---|---|
| `isValid()` | 判断是否持有有效 Java 数组。|
| `size()` | 查询数组长度。|
| `object()` | 取得底层 `jarray`。|
| `operator jobject()` | 用于与原生 JNI API 互操作。|

## 使用场景
写通用 JNI 工具时，仅需查询 Java 数组引用和长度，而不关心具体元素类型。

## 常见坑与经验
- 数组对象引用仍遵守 JNI 线程与引用生命周期规则；不要把裸 `jarray` 随意缓存。
- 访问元素应使用对应的 `QJniArray<T>` 或受控 JNI 调用，而不是假设内存连续可直接映射。

## 知识点覆盖
JNI 数组、对象引用、长度查询、线程边界、类型化封装。
