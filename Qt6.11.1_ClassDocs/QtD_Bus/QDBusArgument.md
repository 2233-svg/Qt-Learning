# QDBusArgument

> Qt 6.11.1 · Qt D-Bus

## 1. 先建立直觉

**一句话定位：** 这是 Qt D-Bus 中围绕“DBusArgument”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** 这是 Qt D-Bus 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QDBusArgument` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QDBusArgument>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS DBus)
target_link_libraries(mytarget PRIVATE Qt6::DBus)
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

- `enum ElementType { BasicType, VariantType, ArrayType, StructureType, MapType, …, UnknownType }`

### 公有函数

- `QDBusArgument()`
- `QDBusArgument(const QDBusArgument &other)`
- `~QDBusArgument()`
- `QVariant asVariant() const`
- `bool atEnd() const`
- `void beginArray() const`
- `void beginArray(QMetaType id)`
- `void beginMap() const`
- `void beginMap(QMetaType keyMetaType, QMetaType valueMetaType)`
- `void beginMapEntry()`
- `void beginMapEntry() const`
- `void beginStructure()`
- `void beginStructure() const`
- `QDBusArgument::ElementType currentType() const`
- `void endArray()`
- `void endArray() const`
- `void endMap()`
- `void endMap() const`
- `void endMapEntry()`
- `void endMapEntry() const`
- `void endStructure()`
- `void endStructure() const`
- `void swap(QDBusArgument &other)`
- `QDBusArgument & operator<<(uchar arg)`
- `QDBusArgument & operator<<(bool arg)`
- `QDBusArgument & operator<<(const QByteArray &arg)`
- `QDBusArgument & operator<<(const QDBusVariant &arg)`
- `QDBusArgument & operator<<(const QString &arg)`
- `QDBusArgument & operator<<(const QStringList &arg)`
- `QDBusArgument & operator<<(double arg)`
- `QDBusArgument & operator<<(int arg)`
- `QDBusArgument & operator<<(qlonglong arg)`
- `QDBusArgument & operator<<(qulonglong arg)`
- `QDBusArgument & operator<<(short arg)`
- `QDBusArgument & operator<<(uint arg)`
- `QDBusArgument & operator<<(ushort arg)`
- `QDBusArgument & operator=(const QDBusArgument &other)`
- `const QDBusArgument & operator>>(uchar &arg) const`
- `const QDBusArgument & operator>>(QByteArray &arg) const`
- `const QDBusArgument & operator>>(QDBusVariant &arg) const`
- `const QDBusArgument & operator>>(QString &arg) const`
- `const QDBusArgument & operator>>(QStringList &arg) const`
- `const QDBusArgument & operator>>(bool &arg) const`
- `const QDBusArgument & operator>>(double &arg) const`
- `const QDBusArgument & operator>>(int &arg) const`
- `const QDBusArgument & operator>>(qlonglong &arg) const`
- `const QDBusArgument & operator>>(qulonglong &arg) const`
- `const QDBusArgument & operator>>(short &arg) const`
- `const QDBusArgument & operator>>(uint &arg) const`
- `const QDBusArgument & operator>>(ushort &arg) const`

### 相关非成员函数

- `QMetaType qDBusRegisterMetaType()`
- `T qdbus_cast(const QDBusArgument &arg)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDBusArgument::ElementType`

**作用与语义：**

该枚举描述了该论元所持有的元素类型。
- `QDBusArgument::BasicType`：`0`;一个基本元素，`QVariant`理解。以下类型被视为基本：bool、byte、short、ushort、int、uint、qint64、quint64、double、`QString`、`QByteArray`、`QDBusObjectPath`、`QDBusSignature`
- `QDBusArgument::VariantType`：`1`;变体元素（`QDBusVariant`）
- `QDBusArgument::ArrayType`：`2`;一个数组元素，通常用`QList`表示<T>。注意：`QByteArray`和关联映射不被视为数组，即使D-总线协议将其传输为数组。
- `QDBusArgument::StructureType`：`3`;一种由结构表示的自定义类型，如 `QDateTime`、`QPoint` 等。
- `QDBusArgument::MapType`：`4`;一个关联容器，如`QMap`<键、值>或`QHash`<键、值>
- `QDBusArgument::MapEntryType`：`5`;关联容器中的一个条目：键和值都构成一个映射条目类型。
- `QDBusArgument::UnknownType`：`-1`;类型未知，或已至列表末尾。

### `QDBusArgument::QDBusArgument()`

**作用与语义：**

构造一个空的QDBusArgument参数。
空的QDBusArgument对象不允许读取或写入。

### `QDBusArgument::QDBusArgument(const QDBusArgument &other)`

**作用与语义：**

构建`other` QDBusArgument对象的副本。
因此，从此两个对象都包含相同的状态。QDBusArguments是显式共享的，因此对任一副本的任何修改都会影响另一份。

### `[noexcept] QDBusArgument::~QDBusArgument()`

**作用与语义：**

处理与该`QDBusArgument`对象相关的资源。

### `QVariant QDBusArgument::asVariant() const`

**作用与语义：**

以`QVariant`的形式返回当前参数。基本类型会在`QVariant`中解码并返回，但对于复杂类型，该函数会返回`QVariant`中的`QDBusArgument`对象。调用者负责解码参数（例如调用其中的 asVariant()。
例如，如果当前参数是INT32，该函数会返回一个类型为`QMetaType::Int`的`QVariant`。对于INT32的数组，它会返回包含`QDBusArgument`的`QVariant`。
如果发生错误或没有更多可解码参数（即参数列表已到末尾），该函数将返回无效`QVariant`。

### `bool QDBusArgument::atEnd() const`

**作用与语义：**

如果没有其他元素需要从该`QDBusArgument`提取，返回`true`。该函数通常用于从`beginMap()`和 `beginArray()`返回的`QDBusArgument`对象。

### `void QDBusArgument::beginArray() const`

**作用与语义：**

递归到D-Bus数组，以便提取数组元素。
该函数通常用于`operator>>`流算子，如下示例：
如果你想分组的类型是`QList`或Qt中任何一个模板参数的容器类，你无需为它声明`operator>>`函数，因为Qt D-Bus提供通用模板来完成数据分组工作。STL的序列容器，如`std::list`、`std::vector`等，情况相同。

**官方示例：**

```cpp
 // Extract a MyArray array of MyElement elements
 const QDBusArgument &operator>>(const QDBusArgument &argument, MyArray &myArray)
 {
     argument.beginArray();
     myArray.clear();

     while (!argument.atEnd()) {
         MyElement element;
         argument >> element;
         myArray.append(element);
     }

     argument.endArray();
     return argument;
 }
```

### `void QDBusArgument::beginArray(QMetaType id)`

**作用与语义：**

打开一个适合附加元类型`id`元素的新D-总线数组。
该函数通常用于`operator<<`流算子，如下示例：
如果你想编组的类型是`QList`或 Qt 的任何容器类，且它们使用一个模板参数，你无需为它声明`operator<<`函数，因为 Qt D-Bus 提供了通用模板来完成数据编组工作。STL 的序列容器，如 `std::list`、`std::vector` 等，情况也是如此。

**官方示例：**

```cpp
 // Append an array of MyElement types
 QDBusArgument &operator<<(QDBusArgument &argument, const MyArray &myArray)
 {
     argument.beginArray(qMetaTypeId<MyElement>());
     for (const auto &element : myArray)
         argument << element;
     argument.endArray();
     return argument;
 }
```

### `void QDBusArgument::beginMap() const`

**作用与语义：**

递归到D-Bus地图，以便提取地图元素。
该函数通常用于`operator>>`流算子，如下示例：
如果你想去分组的类型是`QMap`或`QHash`，你无需为它声明`operator>>`函数，因为Qt D-Bus提供了通用模板来完成数据的分组工作。

**官方示例：**

```cpp
 // Extract a MyDictionary map that associates integers to MyElement items
 const QDBusArgument &operator>>(const QDBusArgument &argument, MyDictionary &myDict)
 {
     argument.beginMap();
     myDict.clear();

     while (!argument.atEnd()) {
         int key;
         MyElement value;
         argument.beginMapEntry();
         argument >> key >> value;
         argument.endMapEntry();
         myDict.insert(key, value);
     }

     argument.endMap();
     return argument;
 }
```

### `void QDBusArgument::beginMap(QMetaType keyMetaType, QMetaType valueMetaType)`

**作用与语义：**

打开一个适合添加元素的新D-总线映射。映射是将一个条目（键）关联到另一个条目（值）的容器，例如Qt的`QMap`或`QHash`值。映射的键和值元类型的id必须分别以`keyMetaType`和值`valueMetaType`传递。
该函数通常用于`operator<<`流算子，如下示例：
通常你不需要为关联容器（如 `QHash` 或 std：：map）提供`operator<<`或`operator>>`函数，因为 Qt D-Bus 提供了通用模板来完成数据编组工作。

**官方示例：**

```cpp
 // Append a dictionary that associates ints to MyValue types
 QDBusArgument &operator<<(QDBusArgument &argument, const MyDictionary &myDict)
 {
     argument.beginMap(QMetaType::fromType<int>(), QMetaType::fromType<MyValue>());
     MyDictionary::const_iterator i;
     for (i = myDict.cbegin(); i != myDict.cend(); ++i) {
         argument.beginMapEntry();
         argument << i.key() << i.value();
         argument.endMapEntry();
     }
     argument.endMap();
     return argument;
 }
```

### `void QDBusArgument::beginMapEntry()`

**作用与语义：**

打开适合附加键和值项的D-Bus映射条目。该函数仅在映射已以`beginMap()`打开时有效。
该函数的用例请参见 `beginMap()`。

### `void QDBusArgument::beginMapEntry() const`

**作用与语义：**

递归到D-Bus映射的条目中，以便提取键和值对。
请参见`beginMap()`，了解该函数通常的使用方式。

### `void QDBusArgument::beginStructure()`

**作用与语义：**

开启一个适合附加新参数的 D-总线结构。
该函数通常用于`operator<<`流算子，如下示例：
结构可以包含其他结构，因此以下代码同样有效：

**官方示例：**

```cpp
 QDBusArgument &operator<<(QDBusArgument &argument, const MyStructure &myStruct)
 {
     argument.beginStructure();
     argument << myStruct.member1 << myStruct.member2;
     argument.endStructure();
     return argument;
 }
```

### `void QDBusArgument::beginStructure() const`

**作用与语义：**

开启适合提取元素的D-总线结构。
该函数通常用于`operator>>`流算子，如下示例：

**官方示例：**

```cpp
 const QDBusArgument &operator>>(const QDBusArgument &argument, MyStructure &myStruct)
 {
     argument.beginStructure();
     argument >> myStruct.member1 >> myStruct.member2 >> myStruct.member3;
     argument.endStructure();
     return argument;
 }
```

### `QDBusArgument::ElementType QDBusArgument::currentType() const`

**作用与语义：**

返回当前元素类型的分类。如果解码该类型出现错误，或者参数结束时，该函数返回`QDBusArgument::UnknownType`。
该函数仅在参数分组时才有意义。如果在编组时使用它，它总是返回`UnknownType`。

### `void QDBusArgument::endArray()`

**作用与语义：**

关闭以`beginArray()`打开的D总线数组。该函数必须被调用次数与`beginArray()`相同次数。

### `void QDBusArgument::endArray() const`

**作用与语义：**

关闭 D-总线数组，允许提取数组之后的下一个元素。

### `void QDBusArgument::endMap()`

**作用与语义：**

闭合以`beginMap()`打开的D-总线映射。该函数必须被调用次数与`beginMap()`相同次数。

### `void QDBusArgument::endMap() const`

**作用与语义：**

关闭 D-Bus 映射，允许提取映射后的下一个元素。

### `void QDBusArgument::endMapEntry()`

**作用与语义：**

关闭以 `beginMapEntry()` 打开的 D-总线映射条目。该函数必须被调用次数与 `beginMapEntry()` 相同次数。

### `void QDBusArgument::endMapEntry() const`

**作用与语义：**

关闭D-Bus地图条目，允许提取地图上的下一个元素。

### `void QDBusArgument::endStructure()`

**作用与语义：**

闭合一个以`beginStructure()`开启的D-总线结构。该函数必须被调用次数与`beginStructure()`相同次数。

### `void QDBusArgument::endStructure() const`

**作用与语义：**

关闭D-总线结构，允许提取结构之后的下一个元素。

### `[noexcept] void QDBusArgument::swap(QDBusArgument &other)`

**作用与语义：**

将这个论点与`other`交换。这个操作非常快，从不失败。

### `QDBusArgument &QDBusArgument::operator<<(uchar arg)`

**作用与语义：**

将类型为`BYTE`的原始值`arg`附加到D-总线流中。

### `QDBusArgument &QDBusArgument::operator<<(bool arg)`

**作用与语义：**

将类型为`BOOLEAN`的原始值`arg`附加到D-总线流上。

### `QDBusArgument &QDBusArgument::operator<<(const QByteArray &arg)`

**作用与语义：**

附加`arg`作为`ARRAY of BYTE`给出的D-Bus流的`QByteArray`。
`QStringList`和`QByteArray`是`QDBusArgument`唯一直接支持的非原始类型，因为它们在Qt应用中被广泛使用。
其他阵列通过Qt D-Bus中的复合类型支持。

### `QDBusArgument &QDBusArgument::operator<<(const QDBusVariant &arg)`

**作用与语义：**

将类型为`VARIANT`的原始值 `arg` 附加到 D-Bus 流上。
D-总线变体类型可以包含任何类型，包括其他变体。它类似于Qt `QVariant`类型。

### `QDBusArgument &QDBusArgument::operator<<(const QString &arg)`

**作用与语义：**

将类型`arg` `STRING`（Unicode字符字符串）的原始值附加到D-Bus流中。

### `QDBusArgument &QDBusArgument::operator<<(const QStringList &arg)`

**作用与语义：**

附加`arg`给出的`QStringList`作为D-Bus流的`ARRAY of STRING`。
`QStringList`和 `QByteArray` 是`QDBusArgument`唯一直接支持的两种非原始类型，因为它们在量子技术应用中被广泛使用。
其他阵列通过Qt D-Bus中的复合类型支持。

### `QDBusArgument &QDBusArgument::operator<<(double arg)`

**作用与语义：**

将类型`DOUBLE`（双精度浮点）的原始值`arg`附加到D-Bus流上。

### `QDBusArgument &QDBusArgument::operator<<(int arg)`

**作用与语义：**

将类型为`INT32`的原始值`arg`附加到D-总线流中。

### `QDBusArgument &QDBusArgument::operator<<(qlonglong arg)`

**作用与语义：**

将类型为`INT64`的原始值`arg`附加到D-总线流上。

### `QDBusArgument &QDBusArgument::operator<<(qulonglong arg)`

**作用与语义：**

将类型为`UINT64`的原始值 `arg` 附加到 D-总线流上。

### `QDBusArgument &QDBusArgument::operator<<(short arg)`

**作用与语义：**

将类型为`INT16`的原始值`arg`附加到D-总线流上。

### `QDBusArgument &QDBusArgument::operator<<(uint arg)`

**作用与语义：**

将类型`UINT32`的原始值`arg`附加到D-Bus流中。

### `QDBusArgument &QDBusArgument::operator<<(ushort arg)`

**作用与语义：**

将类型为`UINT16`的原始值`arg`附加到D-总线流上。

### `QDBusArgument &QDBusArgument::operator=(const QDBusArgument &other)`

**作用与语义：**

把`other` `QDBusArgument`对象复制到这个里面。
因此，从此两个对象都包含相同的状态。QDBusArguments是显式共享的，因此对任一副本的任何修改都会影响另一份。

### `const QDBusArgument &QDBusArgument::operator>>(uchar &arg) const`

**作用与语义：**

从D-总线流中提取一个类型为`BYTE`的D-Bus原始参数并将其置于`arg`中。

### `const QDBusArgument &QDBusArgument::operator>>(QByteArray &arg) const`

**作用与语义：**

从D-Bus流中提取字节数组并返回为`QByteArray`。
`QStringList`和`QByteArray`是`QDBusArgument`唯一直接支持的两种非原始类型，因为它们在量子技术应用中被广泛使用。
其他阵列通过Qt D-Bus中的复合类型支持。

### `const QDBusArgument &QDBusArgument::operator>>(QDBusVariant &arg) const`

**作用与语义：**

从 D-总线流中提取一个类型为 `VARIANT` 的 D-总线原始参数。
D-总线变体类型可以包含任何类型，包括其他变体。它类似于Qt `QVariant`类型。
如果变体包含`QDBusArgument`不直接支持的类型，返回的`QDBusVariant`值将包含另一个`QDBusArgument`。你有责任进一步将其分解成另一种类型。

### `const QDBusArgument &QDBusArgument::operator>>(QString &arg) const`

**作用与语义：**

从D-总线流中提取一个类型为`STRING`的D-Bus原始参数（Unicode字符字符串）。

### `const QDBusArgument &QDBusArgument::operator>>(QStringList &arg) const`

**作用与语义：**

从D-Bus流中提取字符串数组，并返回为`QStringList`。
`QStringList`和`QByteArray`是`QDBusArgument`唯一直接支持的两种非原始类型，因为它们在Qt应用中被广泛使用。
其他阵列通过Qt D-Bus中的复合类型支持。

### `const QDBusArgument &QDBusArgument::operator>>(bool &arg) const`

**作用与语义：**

从D-总线流中提取一个类型为`BOOLEAN`的D-Bus原始参数。

### `const QDBusArgument &QDBusArgument::operator>>(double &arg) const`

**作用与语义：**

从D-总线流中提取一个类型为`DOUBLE`的D-Bus原始参数（双精度浮点）。

### `const QDBusArgument &QDBusArgument::operator>>(int &arg) const`

**作用与语义：**

从D-总线流中提取一个类型为`INT32`的D-总线原始参数。

### `const QDBusArgument &QDBusArgument::operator>>(qlonglong &arg) const`

**作用与语义：**

从D-总线流中提取一个类型为`INT64`的D-Bus原始参数。

### `const QDBusArgument &QDBusArgument::operator>>(qulonglong &arg) const`

**作用与语义：**

从 D-总线流中提取一个类型为 `UINT64` 的 D-Bus 原始参数。

### `const QDBusArgument &QDBusArgument::operator>>(short &arg) const`

**作用与语义：**

从D-总线流中提取一个类型为`INT16`的D-总线原始参数。

### `const QDBusArgument &QDBusArgument::operator>>(uint &arg) const`

**作用与语义：**

从 D-总线流中提取一个类型为 `UINT32` 的 D-总线原始参数。

### `const QDBusArgument &QDBusArgument::operator>>(ushort &arg) const`

**作用与语义：**

从D-总线流中提取一个类型为`UINT16`的D-总线原始参数。

### `template <typename T> QMetaType qDBusRegisterMetaType()`

**作用与语义：**

如果尚未注册，则`T` Qt D-总线类型系统和 Qt 元类型系统注册。
要注册一个类型，必须用`Q_DECLARE_METATYPE()`宏声明为元类型，然后像下面的示例那样注册：
如果`T`不是Qt的容器类之一，`T`和`QDBusArgument`之间的`operator<<`和`operator>>`流算子必须已经声明。有关如何声明此类类型的更多信息，请参见Qt D-Bus类型系统页面。
该函数返回该类型的Qt元类型id（与`qRegisterMetaType()`返回的值相同）。
注意`T`：继承流式类型（包括容器`QList`、`QHash`或`QMap`）可以无需自定义`operator<<`和`operator>>`流式传输的功能，自Qt 5.7起被弃用，因为它忽略了除基类外的其他`T`。没有诊断功能。你应始终为所有类型提供这些操作符，而不是依赖Qt提供的流操作符来处理基类。
注意：该功能是线程安全的。

**官方示例：**

```cpp
 #include <QDBusMetaType>

 qDBusRegisterMetaType<MyClass>();
```

### `template <typename T> T qdbus_cast(const QDBusArgument &arg)`

**作用与语义：**

尝试将`arg`内容重新分组为类型`T`。例如：
注意它等价于以下内容：

**官方示例：**

```cpp
 MyType item = qdbus_cast<Type>(argument);
```

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

`QDBusArgument` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
