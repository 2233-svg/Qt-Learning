# Qt QJniArrayBase 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QJniArrayBase>`  
> 所属模块：`Qt6::Core`  
> 继承：无  
> 派生：`QJniArray<T>`  
> 引入版本：Qt 6.8  
> 类型性质：为 `QJniArray` 提供类型无关的 JNI 数组基础 API

## 1. 它解决什么问题

`QJniArrayBase` 是 `QJniArray<T>` 的非模板基类。它把不依赖元素类型的部分集中起来：

- 判断包装对象是否有效；
- 查询 Java 数组长度；
- 取得底层 `jobject`；
- 在容器和 Java 数组之间建立转换；
- 把数组包装为 `QJniObject`；
- 为派生类提供快速的 `swap()`。

普通业务代码通常直接使用 `QJniArray<T>`，而不是创建 `QJniArrayBase` 对象。基类的价值在于：当代码只关心“这是一个 Java 数组对象”而不关心元素类型时，可以依赖它的公共 API；模板类再补充元素访问、迭代和类型相关的 `arrayObject()`。

## 2. 实际使用场景

### 2.1 写通用的 JNI 数组检查逻辑

```cpp
template <typename Array>
bool canUseArray(const Array &array)
{
    return array.isValid() && !array.isEmpty();
}
```

### 2.2 从 Qt 容器创建 Java 数组

```cpp
QList<jint> values{1, 2, 3};
auto array = QJniArrayBase::fromContainer(values);
```

返回类型由容器元素类型推导，通常是 `QJniArray<jint>`；`QByteArray`、`QStringList` 和 `QList<QJniObject>` 等有专门映射。

### 2.3 把数组交给 Java 方法

```cpp
QJniArray<jint> array{1, 2, 3};
QJniObject object = array;
```

转换结果包装同一个 Java 对象，可用于需要 `QJniObject` 的 JNI 调用路径。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QJniArrayBase>
```

qmake 工程：

```qmake
QT += core
```

多数情况下包含 `<QJniArray>` 已经足够，因为 `QJniArray` 继承自该基类；只有直接使用基类接口或 `fromContainer()` 时才需要显式包含。

## 4. 核心使用模型

### 4.1 `size_type` 是 JNI 的 32 位大小类型

`QJniArrayBase::size_type` 是 32 位整数类型，对应 JNI 的 `jsize` 语义。Java 数组的长度不是 Qt 容器那种可扩展的任意大小；尝试从超过 `2^32` 个元素的 C++ 容器创建数组会触发运行时断言。

### 4.2 invalid 不等于 valid 的空数组

默认构造的 `QJniArray<T>` 是 invalid，表示没有包装有效 `jobject`。一个合法的 Java 零长度数组则是 valid，但 `isEmpty()` 同样返回 `true`。因此：

```cpp
if (!array.isValid()) {
    // 没有可用的 Java 数组对象
} else if (array.isEmpty()) {
    // 有效对象，但长度为 0
}
```

基类明确规定 invalid 数组的 `object()` 返回 `nullptr`，安全迭代时 `begin()` 等于 `end()`，`toContainer()` 返回空容器。

### 4.3 Java 数组对象身份由派生类管理

基类不提供元素访问，也不负责确认 `T` 与实际 Java 数组类型匹配。类型相关的句柄由 `QJniArray<T>::arrayObject()` 提供，元素访问由派生类的 `at()`、`operator[]` 和迭代器提供。

从 `jarray` 或 `QJniObject` 构造时，`QJniArray` 不会验证元素类型；基类 API 只能帮助检查对象是否有效，不能替代类型协议。

## 5. 常见误区与边界

### 5.1 不能把基类当作完整容器

`QJniArrayBase` 没有 `operator[]`、`begin()` 或元素类型。需要访问元素时使用 `QJniArray<T>`。

### 5.2 `object()` 的模板参数必须是 JNI 对象类型

`object<T>()` 返回底层对象，并允许用适合的 JNI Object Type 指定返回类型。类型参数必须与实际 JNI 对象类型兼容；它不是运行时类型转换器，也不会把错误类型修正为正确句柄。

### 5.3 `fromContainer()` 是复制转换

`fromContainer()` 会创建 Java 数组并复制容器数据，不会让 Java 数组直接引用 C++ 容器内存。源容器生命周期结束后，Java 数组仍然独立存在。

### 5.4 `fromContainer()` 的类型映射有例外

常见映射如下：

| 输入容器 | 推导的 `QJniArray` |
| --- | --- |
| `Container<T>`，其中 `T` 是 JNI 类型或等价 C++ 类型 | 通常是 `QJniArray<T>` |
| `QByteArray` | `QJniArray<jbyte>` |
| `QStringList` | `QJniArray<jstring>` |
| 元素类型为 `QJniObject` 的容器 | `QJniArray<jobject>` |

容器必须提供前向迭代器，且元素类型必须是支持的 JNI 类型或等价类型。

### 5.5 不要跨线程误用底层 JNI 句柄

`object()` 返回的是 JNI 对象句柄语义，能否使用取决于当前 JNI 环境和引用类型。跨线程传递时应传递 Qt 的对象包装并在目标线程使用有效 JNI 环境，不要把局部 JNI 引用当成永久句柄。

## 6. 与相关类型的协作

- `QJniArray<T>`：唯一的标准派生类，补充元素类型和迭代器操作。
- `QJniObject`：承载同一个 Java 对象，可用于 JNI 方法调用。
- `QByteArray`、`QStringList`、`QList<T>`：作为 `fromContainer()` 的输入或 `QJniArray::toContainer()` 的输出。

## 7. 逐项 API 说明

### 成员类型

#### `[alias] QJniArrayBase::size_type`

Java 数组长度和索引使用的 32 位整数类型，具有 JNI `jsize` 的边界。它不是 `qsizetype`，不能假设在 64 位平台上自动扩展。

### 静态成员

#### `[static] template <typename Container, ...> auto QJniArrayBase::fromContainer(Container &&container)`

创建一个新的 Java 数组并复制 `container` 中的数据，返回相应的 `QJniArray<...>`。只有容器提供前向迭代器且元素为 JNI 类型或兼容 C++ 类型时才参与重载。

常见推导规则：

- `QList<jint>` 通常得到 `QJniArray<jint>`；
- `QByteArray` 得到 `QJniArray<jbyte>`；
- `QStringList` 得到 `QJniArray<jstring>`；
- 元素类型为 `QJniObject` 的容器得到 `QJniArray<jobject>`。

它是创建新 Java 数组的工厂，不是对输入容器建立共享视图。数组大小仍受 32 位 JNI `jsize` 限制。

### 公共函数

#### `bool QJniArrayBase::isEmpty() const`

当 Java 数组长度为 0 时返回 `true`。invalid 数组也总是返回 `true`，因此不能单独用它判断是否包装了有效对象。

#### `bool QJniArrayBase::isValid() const`

判断包装对象是否持有有效 `jobject`。invalid 时 `object()` 返回 `nullptr`，迭代和 `toContainer()` 仍按空数组处理。

#### `template <typename T = jobject> T QJniArrayBase::object() const`

返回底层 Java 对象，并按模板参数 `T` 指定适合的 JNI Object Type。invalid 对象返回 `nullptr`。调用者需保证模板参数和实际对象兼容。

#### `QJniArrayBase::size_type QJniArrayBase::size() const`

返回 Java 数组长度。对 invalid 数组按基类的空数组语义处理，实际使用前应先检查 `isValid()`。

#### `QJniArrayBase::operator QJniObject() const`

把基类包装的同一个 `jobject` 转换为 `QJniObject`。这是包装转换，不是 Java 数组内容复制。

### 受保护函数

#### `[noexcept protected] void QJniArrayBase::swap(QJniArrayBase &other)`

交换两个数组包装对象持有的 Java 引用。操作快速且不会失败，供派生类实现交换或移动辅助逻辑使用；普通代码通常通过 `QJniArray` 的值语义间接使用。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成员类型 | `size_type` | 表示 Java 数组长度和索引的 32 位类型。 | 受 JNI `jsize` 限制，不等同于 64 位 `qsizetype`。 |
| 静态成员 | `fromContainer(container)` | 从 C++ 容器创建并填充新的 Java 数组。 | 复制数据；需要前向迭代器和兼容元素类型。 |
| 状态 | `isEmpty()` | 判断数组长度是否为 0。 | invalid 数组也返回 `true`。 |
| 状态 | `isValid()` | 判断是否包装有效 `jobject`。 | 需要区分 invalid 与 valid 零长度数组时必须调用。 |
| 对象 | `object<T>()` | 返回底层 JNI 对象句柄。 | `T` 必须是兼容的 JNI Object Type。 |
| 大小 | `size()` | 返回 Java 数组长度。 | 长度为 32 位 JNI `jsize` 语义。 |
| 转换 | `operator QJniObject()` | 包装同一个 Java 对象为 `QJniObject`。 | 不复制数组内容。 |
| 受保护 | `swap(other)` | 交换两个包装对象的引用。 | 仅派生类可直接调用；快速且 `noexcept`。 |

## 9. 使用判断

- 只需要判断数组是否有效、查询大小或转成 `QJniObject`：依赖 `QJniArrayBase` 接口。
- 需要元素访问、迭代或按 `T` 返回 JNI 数组句柄：使用 `QJniArray<T>`。
- 需要从容器创建数组：优先 `QJniArrayBase::fromContainer()` 或直接构造 `QJniArray<T>`。
- 需要处理 Java 集合而不是数组：使用 `QJniObject`，不要强行套用该基类。
