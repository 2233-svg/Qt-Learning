# QJniArray
> Qt 6.11.1 · Qt Core · 来自 `QJniArray`

## 作用定位
`QJniArray<T>` 是 Java 基本类型或对象数组的类型化 C++ 封装，提供安全的长度查询、元素读写和与 JNI 数组对象的互操作。

## API 速查
| API | 是做什么的 |
|---|---|
| `size()` | 查询元素数。|
| `at()` | 读取一个元素。|
| `operator[]` | 按索引访问元素。|
| `setValue()` | 写入一个元素。|
| `toContainer()` | 转换为对应 Qt/C++ 容器副本。|
| `fromContainer()` | 从 C++ 容器创建 Java 数组。|
| `object()` | 获取底层 JNI 数组引用。|

## 使用场景
在 Qt Android 与 Java helper 之间传递 `int[]`、`byte[]`、字符串数组或对象数组。

## 常见坑与经验
- 单元素 JNI 访问可能代价较高；大量数据应批量转换或使用合适的 JNI 批处理 API。
- `toContainer()` 会复制所有元素，大数组需评估内存峰值。
- Java 数组内容和 C++ 副本不会自动双向同步。

## 知识点覆盖
JNI 数组、类型化访问、批量转换、复制成本、Android 互操作。
