# Qt QJniArray 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QJniArray>`  
> 所属模块：`Qt6::Core`  
> 继承：`QJniArrayBase`  
> 引入版本：Qt 6.8  
> 类型性质：模板类，`QJniArray<T>` 表示一个 Java 数组

## 1. 它解决什么问题

JNI 中的 Java 数组不是普通的 C++ 容器。它有 Java 对象身份、固定长度、特定的元素类型，并且需要通过 JNI 引用规则管理生命周期。`QJniArray<T>` 把这些细节包装成 Qt 风格的值类型，使 C++ 代码可以：

- 从 `QList<T>`、`QByteArray`、`QStringList` 或初始化列表创建 Java 数组；
- 接收 `QJniObject::callMethod<T[]>()` 返回的 Java 数组；
- 按索引读取、写入和遍历 Java 数组元素；
- 在 Java 数组和 Qt 容器之间复制数据；
- 把同一个数组转换为 `QJniObject` 或合适的 JNI 数组句柄。

它表示的是“Java 数组对象的 Qt 包装”，不是 `QList` 的替代品，也不是可以动态增长的容器。Java 数组长度一旦创建就不能改变；重新赋值只会让包装对象改为引用另一个数组。

## 2. 实际使用场景

### 2.1 调用返回数组的 Java 方法

例如 Java 的 `String.toCharArray()` 返回 `char[]`，在 C++ 侧把返回类型写成 `jchar[]`：

```cpp
const auto chars = stringObject.callMethod<jchar[]>("toCharArray");
```

返回值的实际类型是 `QJniArray<jchar>`，并且包装了一个新的全局 JNI 引用。

### 2.2 把 Qt 容器作为 Java 方法参数

```cpp
QList<jint> values{1, 2, 3};
const auto array = QJniArray<jint>(values);
```

构造过程会创建新的 Java 数组，并把 C++ 容器中的元素复制进去。调用 Java 方法时，可再通过 `array.arrayObject()` 或隐式转为 `QJniObject` 传递。

### 2.3 处理字节、字符串和对象数组

默认 `toContainer()` 通常返回 `QList<T>`，但有明确的特例：

| `QJniArray<T>` | 默认目标容器 |
| --- | --- |
| `QJniArray<jbyte>` | `QByteArray` |
| `QJniArray<char>` | `QByteArray` |
| `QJniArray<jstring>` | `QStringList` |
| `QJniArray<QString>` | `QStringList` |

Java 对象数组可以用 `QJniArray<QJniObject>` 或声明过的 JNI 类类型表示。Java 的 `List`、`ArrayList` 等集合不是数组，不能用 `QJniArray` 包装，应使用 `QJniObject` 调用其类方法。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QJniArray>
```

qmake 工程：

```qmake
QT += core
```

## 4. 最小可用示例

### 4.1 创建并读取 Java 数组

```cpp
QJniArray<jint> numbers{10, 20, 30};

for (const auto &value : numbers)
    qDebug() << value;

const QList<jint> values = numbers.toContainer();
```

### 4.2 创建固定长度数组并逐项写入

```cpp
QJniArray<jint> numbers(3);
for (QJniArrayBase::size_type i = 0; i < numbers.size(); ++i)
    numbers[i] = static_cast<jint>(i * 10);
```

非 const `operator[]` 返回的是代理引用对象。给它赋值会写回 Java 数组；它不是一个可以长期保存并原地修改的普通 `T&`。

### 4.3 从 Java 对象包装数组

```cpp
QJniArray<jint> numbers(javaArray);
if (numbers.isValid())
    qDebug() << numbers.size();
```

从已有 `jarray` 或 `QJniObject` 构造时，Qt 不会验证实际 Java 数组的元素类型是否真的与 `T` 匹配。类型不匹配后继续访问属于未定义行为，调用方必须保证类型正确。

## 5. 核心使用模型

### 5.1 `T` 决定 JNI 数组类型和访问方式

`T` 可以是 JNI 基本类型、等价的 C++ 类型、`QJniObject` 或声明过的 JNI 类类型。`arrayObject()` 会按照 `T` 返回对应的 JNI 数组类型，例如：

- `jbyte` 对应 `jbyteArray`；
- `jchar` 对应 `jcharArray`；
- `jobject`、`QJniObject` 或 JNI 类声明类型对应 `jobjectArray`。

不要把 `QJniArray<QString>` 当作“Java `String[]` 的裸指针数组”；Qt 会负责元素转换和 JNI 访问，但 Java 侧仍然是对象数组。

### 5.2 数组内容和包装对象是两层状态

拷贝构造和拷贝赋值不会复制 Java 数组内容，而是让两个 `QJniArray` 包装同一个 Java 数组对象。通过一个可变包装对象写入元素，另一个包装对象读取时会看到同一 Java 数组中的修改。

移动构造和移动赋值则转移包装对象持有的引用；被移动对象变为 invalid。析构时，`QJniArray` 会释放它持有的 Java 数组引用。

### 5.3 const 访问和 mutable 访问的区别

const 数组的元素访问通常更高效，因为不需要为可能写回的访问建立可变代理。只读场景优先使用：

```cpp
const QJniArray<jint> numbers = object.callMethod<jint[]>("getNumbers");
const jint first = numbers.at(0);
```

非 const `operator[]` 用于写回：

```cpp
QJniArray<jint> numbers(2);
numbers[0] = 42;
numbers[1] = 84;
```

如果只是调用元素对象的成员函数而不是替换数组槽位，需要先解引用代理。例如 `QJniArray<QString>` 的 `numbers[0]` 是引用代理，`(*numbers[0]).isEmpty()` 才是对取出的 `QString` 调用成员函数。

### 5.4 invalid、empty 和数组长度

默认构造对象是 invalid。invalid 数组：

- `isValid()` 返回 `false`；
- `isEmpty()` 返回 `true`；
- `size()` 为 0；
- `object()` 返回 `nullptr`；
- `begin()` 与 `end()` 相同，遍历是安全的；
- `toContainer()` 返回空容器。

valid 但长度为 0 的 Java 数组与 invalid 数组都满足 `isEmpty()`，因此需要区分对象是否可用时必须检查 `isValid()`。

Java 数组长度受 JNI 的 `jsize` 限制，`QJniArrayBase::size_type` 是 32 位整数。把超过 `2^32` 个元素的 C++ 容器转换为 Java 数组会触发运行时断言，而不是得到一个更大的数组。

## 6. 常见误区与边界

### 6.1 把 Java 集合当成数组

`List`、`ArrayList` 等是普通 Java 对象，不是 Java 数组。它们不能用 `QJniArray` 表示，应使用 `QJniObject` 调用 `size()`、`get()`、`add()` 等类方法。

### 6.2 从 `jarray` 构造但没有验证元素类型

```cpp
QJniArray<jint> numbers(someArray);
```

这段代码只建立包装，不检查 `someArray` 是否真的是 `int[]`。如果实际对象是 `long[]`、`String[]` 或其他不兼容数组，之后读取或写入的行为未定义。类型保证必须来自 Java 方法签名、JNI 声明或调用方自己的协议。

### 6.3 越界访问

`at()` 和两个 `operator[]` 都要求 `0 <= i < size()`。文档把索引前置条件写成“必须有效”，不要把它们当作自动扩容或带边界修复的接口。创建固定长度数组后只能修改已有位置，不能追加元素。

### 6.4 把代理引用当成普通引用

非 const `operator[]` 返回 `reference` 代理。读取时它通常可以隐式转换为值；赋值时会写回数组槽位。但对代理本身调用可变成员函数不会修改数组元素，需先解引用取得值对象：

```cpp
QJniArray<QString> strings(1);
strings[0] = u"old";
(*strings[0]).replace(u"old", u"new");
```

更清晰、也更不容易误解的写法是先复制到局部变量，修改后再赋回数组。

### 6.5 反向迭代器的 `operator->()`

反向迭代器返回代理对象。C++17 的 `reverse_iterator` 不支持对这类代理使用 `operator->()`；需要通过 `operator->()` 访问时，使用 C++20，或者改用解引用和显式局部变量。

### 6.6 误以为 `toContainer()` 是零拷贝视图

`toContainer()` 会把 Java 数组数据复制到 C++ 容器。传入左值容器时填充该容器并返回引用；传入临时容器或不传参数时填充后按值返回。它不是 Java 数组的共享视图。

### 6.7 超过 Java 数组的 JNI 生命周期

`QJniArray` 自己持有 Java 数组的引用，析构时释放引用；但 `arrayObject()` 返回的 JNI 句柄仍然受 JNI 当前线程和引用规则约束。不要把局部 JNI 引用跨线程或跨越其有效作用域长期保存，必要时使用 Qt 的 JNI 对象包装和明确的全局引用所有权。

## 7. 与相关类型的协作

- `QJniArrayBase`：提供类型无关的有效性、大小、底层对象和容器转换基础 API。
- `QJniObject`：用于调用返回数组的方法、传递数组对象，以及操作 Java `List` 等非数组集合。
- `QByteArray`：与 `QJniArray<jbyte>` 或 `QJniArray<char>` 互转。
- `QStringList`：与 `QJniArray<jstring>` 或 `QJniArray<QString>` 互转。
- `QList<T>`：默认承载大多数 `QJniArray<T>::toContainer()` 的结果。

## 8. 逐项 API 说明

### 成员类型

#### `QJniArray::const_iterator`、`QJniArray::iterator`

随机访问迭代器。const 版本只能读取，非 const 版本可通过代理对象写回 Java 数组元素。对 invalid 数组，`begin()` 与 `end()` 相同。

#### `QJniArray::const_reverse_iterator`、`QJniArray::reverse_iterator`

反向随机访问迭代器。C++17 下对代理元素使用 `operator->()` 有限制，涉及该操作时使用 C++20 或改用解引用。

### 构造与析构

#### `QJniArray::QJniArray()`

创建 invalid 数组包装。它不代表一个长度为 0 的 valid Java 数组；需要区分两种状态时使用 `isValid()`。

#### `template <typename Container, ...> explicit QJniArray::QJniArray(Container &&container)`

从兼容 C++ 容器创建新的 Java 数组并复制元素。容器需要提供前向迭代器，元素必须是 JNI 类型或兼容的 C++ 类型。容器过大超过 `jsize` 能表达的范围时会触发运行时断言。

#### `template <typename Other, ...> QJniArray::QJniArray(QJniArray<Other> &&other)`

移动构造并转移 Java 数组包装。只有 `Other` 可转换为 `T` 时参与重载选择，但不会执行元素转换；移动后的 `other` 变为 invalid。

#### `explicit QJniArray::QJniArray(QJniArrayBase::size_type size)`

Qt 6.9 引入。创建指定长度、元素尚未填充的 Java 数组，之后可用非 const `operator[]` 逐项写入。Java 数组长度固定，不能追加。

#### `explicit noexcept QJniArray::QJniArray(QJniObject &&object)`

从右值 `QJniObject` 包装同一个 Java 数组并建立新的全局引用。不会验证对象是否是与 `T` 匹配的数组；类型不匹配时访问是未定义行为。

#### `template <typename Other, ...> QJniArray::QJniArray(const QJniArray<Other> &other)`

拷贝构造并共享同一个 Java 数组对象。模板约束要求 `Other` 可转换为 `T`，但不会进行实际元素转换。

#### `explicit QJniArray::QJniArray(const QJniObject &object)`

从 `QJniObject` 包装同一个 Java 数组并建立新的全局引用。对象的 Java 数组元素类型必须由调用方保证。

#### `explicit QJniArray::QJniArray(jarray array)`

从 JNI 数组句柄包装 Java 数组，并为其建立新的全局引用。不会进行元素类型检查；传入 null 或不匹配对象后，应先检查有效性并避免按错误类型访问。

#### `QJniArray::QJniArray(std::initializer_list<T> &list)`

从初始化列表创建新的 Java 数组并复制元素。常见写法是 `QJniArray<jint> values{1, 2, 3};`。

#### `QJniArray::~QJniArray()`

销毁包装对象并释放其持有的 Java 数组引用。它不会改变 Java 数组的固定长度语义。

### 底层对象与元素访问

#### `auto QJniArray::arrayObject() const`

返回与 `T` 对应的 JNI 数组句柄类型，如 `jbyteArray`、`jcharArray` 或 `jobjectArray`。这是把数组传给 JNI/Java 调用的直接入口。

#### `QJniArray<T>::const_reference QJniArray::at(size_type i) const`

读取位置 `i` 的元素。索引必须有效；返回 const 访问结果，不提供写回能力。

#### `QJniArray<T>::reference QJniArray::operator[](size_type i)`（Qt 6.9）

返回位置 `i` 的可写代理引用。读取时可转换为值，赋值时覆盖 Java 数组中的槽位；索引必须有效。代理自身的成员函数调用不会自动写回槽位。

#### `QJniArray<T>::const_reference QJniArray::operator[](size_type i) const`

读取位置 `i` 的 const 元素访问，语义与 `at()` 相同。索引必须有效。

### 迭代器

#### `begin()`、`constBegin()`、`cbegin()`

返回指向第一个元素的正向迭代器。非 const `begin()` 可用于通过代理写回；invalid 数组的 `begin()` 等于 `end()`。

#### `end()`、`constEnd()`、`cend()`

返回尾后迭代器。它只用于和同一数组的起始迭代器比较，不能解引用。

#### `rbegin()`、`crbegin()`

返回指向最后一个元素的反向迭代器。invalid 数组的 `rbegin()` 等于 `rend()`。

#### `rend()`、`crend()`

返回反向尾后迭代器，不能解引用。

### 容器转换与赋值

#### `template <typename Container = QJniArrayBase::ToContainerType<T>, ...> Container QJniArray::toContainer(Container &&container = {}) const`

复制 Java 数组内容到 C++ 容器。默认目标容器按 `T` 推导；传入左值容器时填充并返回该容器的引用，传入右值或省略参数时返回填充后的容器。invalid 数组立即返回空容器或未改变的目标容器。

#### `QJniArray<T> &operator=(QJniArray<Other> &&other)`

移动赋值并转移数组包装；移动后的 `other` 变为 invalid。模板约束只保证元素类型可转换，不代表会逐元素转换。

#### `QJniArray<T> &operator=(const QJniArray<Other> &other)`

拷贝赋值，使两个包装对象引用同一个 Java 数组对象。它不会复制数组内容，也不会创建独立数组。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成员类型 | `const_iterator`、`iterator` | 正向随机访问迭代器。 | 非 const 迭代器涉及代理写回；invalid 数组为空迭代区间。 |
| 成员类型 | `const_reverse_iterator`、`reverse_iterator` | 反向随机访问迭代器。 | C++17 对代理使用 `operator->()` 受限。 |
| 构造 | `QJniArray()` | 创建 invalid 包装。 | 与 valid 的零长度数组不同。 |
| 构造 | `QJniArray(Container &&)` | 从 C++ 容器创建并填充 Java 数组。 | 元素须兼容 JNI 类型，长度受 32 位 `jsize` 限制。 |
| 构造 | `QJniArray(QJniArray<Other> &&)` | 移动包装对象。 | 源对象变为 invalid，不做元素转换。 |
| 构造 | `QJniArray(size_type size)` | 创建固定长度 Java 数组。 | Qt 6.9 起；不能追加元素。 |
| 构造 | `QJniArray(QJniObject &&)` | 从对象包装 Java 数组。 | 不检查元素类型。 |
| 构造 | `QJniArray(const QJniArray<Other> &)` | 复制包装并共享 Java 数组。 | 两个对象引用同一数组。 |
| 构造 | `QJniArray(const QJniObject &)` | 从对象包装 Java 数组。 | 必须自行保证对象确实是匹配的数组。 |
| 构造 | `QJniArray(jarray)` | 从 JNI 数组句柄包装数组。 | 建立新的全局引用；不做类型检查。 |
| 构造 | `QJniArray(std::initializer_list<T> &)` | 从初始化列表创建数组。 | 创建的是新的 Java 数组。 |
| 析构 | `~QJniArray()` | 释放包装对象持有的 Java 引用。 | 句柄和数组生命周期仍遵守 JNI 规则。 |
| 对象 | `arrayObject()` | 返回对应的 JNI 数组句柄。 | `T` 决定返回的 `j*Array` 类型。 |
| 访问 | `at(i)` | const 读取元素。 | `i` 必须在 `[0, size())` 内。 |
| 访问 | `operator[](i)` | 非 const 读取或写回元素。 | 返回代理；赋值写回，代理成员调用不等于槽位修改。 |
| 访问 | `operator[](i) const` | const 读取元素。 | 不提供写回能力；索引必须有效。 |
| 迭代 | `begin()`、`constBegin()`、`cbegin()` | 获取正向起始迭代器。 | invalid 数组返回与 `end()` 相同的迭代器。 |
| 迭代 | `end()`、`constEnd()`、`cend()` | 获取正向尾后迭代器。 | 不能解引用。 |
| 迭代 | `rbegin()`、`crbegin()` | 获取反向起始迭代器。 | C++17 下代理的 `operator->()` 有限制。 |
| 迭代 | `rend()`、`crend()` | 获取反向尾后迭代器。 | 不能解引用。 |
| 转换 | `toContainer(container)` | 把数组内容复制到 Qt/C++ 容器。 | 默认类型有 `QByteArray`、`QStringList` 特例；不是零拷贝。 |
| 赋值 | `operator=(QJniArray<Other> &&)` | 移动赋值包装对象。 | 源对象变 invalid，不做元素转换。 |
| 赋值 | `operator=(const QJniArray<Other> &)` | 共享 Java 数组的拷贝赋值。 | 两个包装引用同一数组。 |

## 10. 使用判断

- 需要处理 Java 原生数组：使用 `QJniArray<T>`。
- 需要动态增删元素：在 Java 侧使用 `List` 等集合，并用 `QJniObject` 操作。
- 只读且追求较低访问开销：尽量使用 const `QJniArray`。
- 需要把整个数组交给 C++ 算法：调用 `toContainer()`，并明确这是一次复制。
- 从 JNI 句柄或 `QJniObject` 构造：先确认 Java 实际数组类型，再访问。
