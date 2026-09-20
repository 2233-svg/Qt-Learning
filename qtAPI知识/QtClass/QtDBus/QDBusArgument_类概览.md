# Qt QDBusArgument 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusArgument>`  
> 所属模块：`Qt6::DBus`  
> 类型特征：显式共享的 D-Bus 编码与解码流

## 1. 它解决什么问题

D-Bus 只能在线上传输它定义的类型：基础数值、字符串、对象路径、签名、variant，以及由这些类型组合出的数组、字典和结构体。普通 C++ 自定义结构体并没有自动的 D-Bus 布局。

`QDBusArgument` 是 Qt D-Bus 类型系统的核心流对象。它把 Qt 值写成 D-Bus 数据，或把收到的 D-Bus 数据按顺序读回 Qt 值：

```text
Qt 值 ── operator<< ──> QDBusArgument ──> D-Bus 参数
D-Bus 参数 ── operator>> ──> QDBusArgument ──> Qt 值
```

它通常不会由业务代码直接构造后裸用，而是在为**自定义类型**实现 `operator<<`、`operator>>` 时出现。标准 Qt 容器已经有通用模板支持，只有元素类型本身需要正确编解码。

## 2. 自定义类型的完整使用方式

假设要通过 D-Bus 发送一个订单信息：

```cpp
struct OrderInfo
{
    int id = 0;
    QString customer;
    QStringList itemNames;
};

Q_DECLARE_METATYPE(OrderInfo)
```

在与 `OrderInfo` 相同的命名空间中定义一对流运算符：

```cpp
QDBusArgument &operator<<(QDBusArgument &argument, const OrderInfo &order)
{
    argument.beginStructure();
    argument << order.id << order.customer << order.itemNames;
    argument.endStructure();
    return argument;
}

const QDBusArgument &operator>>(const QDBusArgument &argument, OrderInfo &order)
{
    argument.beginStructure();
    argument >> order.id >> order.customer >> order.itemNames;
    argument.endStructure();
    return argument;
}
```

程序启动后、首次把该类型放入 D-Bus 消息前注册：

```cpp
qDBusRegisterMetaType<OrderInfo>();
```

注册后该类型才能作为方法参数、返回值、已导出信号参数或来自远端的参数正常工作。

## 3. 最重要的规则：读写布局必须严格对称

上例的两个运算符必须保证：

- 都使用 structure。
- 字段顺序完全相同。
- 字段数量完全相同。
- 每个字段对应的 D-Bus 类型相同。
- `begin...()` 与 `end...()` 成对嵌套。

不要根据某个运行时字段是否为空而“少写一个成员”：

```cpp
// 错误示例：写入字段数会变化
if (!order.customer.isEmpty())
    argument << order.customer;
```

如果序列化与反序列化读取的条目数不同，Qt D-Bus 类型系统会被破坏，后续调用或信号可能无明显异常地失败。需要表达可选值时，应在协议中固定一个标志位和固定的后续字段布局，或使用合适的 D-Bus variant。

## 4. 写入与读取：同一 API 名称，方向不同

### 4.1 写入 Qt 到 D-Bus

写入使用非 `const` `QDBusArgument`：

```cpp
argument.beginArray(QMetaType::fromType<OrderInfo>());
for (const OrderInfo &order : orders)
    argument << order;
argument.endArray();
```

`beginArray(QMetaType)`、`beginMap(keyType, valueType)` 和 `beginStructure()` 声明容器布局，随后连续写入元素。

### 4.2 读取 D-Bus 到 Qt

读取函数是 `const`，但这是逻辑 const：读取游标仍会在参数内部向前移动。

```cpp
argument.beginArray();
orders.clear();

while (!argument.atEnd()) {
    OrderInfo order;
    argument >> order;
    orders.append(order);
}

argument.endArray();
```

读取数组或 map 时，`atEnd()` 是判断当前嵌套容器是否读完的正确方式。

## 5. D-Bus 复合类型

### 5.1 Structure

结构体是有序字段组。写入和读取都必须调用对应的 `beginStructure()`、`endStructure()`。

### 5.2 Array

数组只包含一种元素 D-Bus 类型。写入时必须用 `QMetaType` 声明元素类型；读取时进入数组、循环到 `atEnd()`、再退出数组。

`QList<T>`、`QVector<T>`、`std::vector<T>` 等单元素类型容器通常已有通用支持。只有 `T` 需要是可在 D-Bus 中编解码的类型。

### 5.3 Map

字典是 key-value 对的集合。写入 map 时要声明 key、value 的 `QMetaType`，每项都必须在 `beginMapEntry()`、`endMapEntry()` 中写入一对 key 和 value。

`QMap<Key, Value>`、`QHash<Key, Value>`、`std::map<Key, Value>` 等关联容器也有通用模板支持。除非要定义特别的协议布局，一般不必自己重复写它们的流运算符。

### 5.4 Variant

D-Bus `VARIANT` 与普通 `QVariant` 不是一回事。若协议要求 D-Bus `v`，使用 `QDBusVariant`；`appendVariant()` 也是面向这一层的低层 API。不要因为变量在 C++ 中是 `QVariant`，就假设在线上自动是 D-Bus variant。

## 6. 值类型、共享状态与检查 API

`QDBusArgument` 是**显式共享**的。复制对象后，两份对象指向同一编解码状态，任何一份继续读写都会影响另一份的当前位置。不要通过复制“保存一个独立游标”：

```cpp
QDBusArgument first = argument;
QDBusArgument second = first; // 不是独立读取位置
```

调试或通用解析时可使用：

- `currentType()`：当前元素的分类。
- `currentSignature()`：当前元素的 D-Bus 签名。
- `asVariant()`：读取当前元素为 `QVariant`。

`asVariant()` 对基础类型会直接返回对应 Qt 值；对数组、map、structure 等复杂类型，返回的 `QVariant` 内仍可能装着另一个 `QDBusArgument`，调用者需要递归解码。

## 7. `qdbus_cast` 与类型注册

`qdbus_cast<T>()` 是“从 `QDBusArgument` 或 `QVariant` 读取一个 `T`”的便捷函数：

```cpp
OrderInfo order = qdbus_cast<OrderInfo>(variant);
```

当 `QVariant` 内部保存的是 `QDBusArgument` 时，它会使用你的 `operator>>`；否则使用普通 `qvariant_cast<T>()`。它适合边界处的一次性转换，但不会替代注册、布局对称或错误处理。

`qDBusRegisterMetaType<T>()` 应在使用类型之前调用。通常放在应用初始化或模块初始化中，而不是每个方法调用前反复调用。

## 8. 常见误区

### 8.1 误区：自定义结构体只要 `Q_DECLARE_METATYPE` 就能上总线

不够。还需要成对的 `operator<<`、`operator>>` 和 `qDBusRegisterMetaType<T>()`。

### 8.2 误区：可以在读写两端按不同条件省略字段

不行。D-Bus structure 是固定序列，读写数量与顺序必须完全一致。

### 8.3 误区：复制 `QDBusArgument` 后可以平行读取

不行。它是显式共享状态，副本共享当前读写位置。

### 8.4 误区：任何 `QVariant` 都会在线上变成 D-Bus `v`

不行。D-Bus `VARIANT` 应显式使用 `QDBusVariant`。

## 9. 逐项 API 说明

### 元素类型

`ElementType` 用于检查解码时当前元素的类别：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举值 | `BasicType` | 表示基础 D-Bus 值。 | 具体基础类型仍由 signature 和读取目标类型决定。 |
| 枚举值 | `VariantType` | 表示 D-Bus `VARIANT`。 | 与 C++ 普通 `QVariant` 的线上类型语义不同。 |
| 枚举值 | `ArrayType` | 表示数组容器。 | 读取要以 `beginArray()`、`atEnd()`、`endArray()` 配对。 |
| 枚举值 | `StructureType` | 表示有序结构体。 | 字段数量、顺序、类型必须和写入端一致。 |
| 枚举值 | `MapType` | 表示字典容器。 | 每个元素由 map entry 的 key-value 对组成。 |
| 枚举值 | `MapEntryType` | 表示字典中的一项。 | 只能在已打开的 map 内进入。 |
| 枚举值 | `UnknownType` | 表示到达末尾、解析失败或写入状态。 | 不能继续把它当可读取数据。 |

### 构造、状态与交换

#### `QDBusArgument()`、复制和赋值

默认构造得到空 argument，既不能读也不能写。复制、复制赋值共享同一状态；移动构造、移动赋值转移状态，移动后的对象只应析构或重新赋值。

#### `swap(QDBusArgument &other)`

快速交换两个 argument 的内部状态。通常只用于泛型代码或实现异常安全赋值。

#### `currentSignature()`、`currentType()`、`atEnd()`

这三个是解码辅助 API。只在 D-Bus 到 Qt 的读取方向有意义；写入过程中 `currentType()` 会是 `UnknownType`。

#### `asVariant()`

将当前元素取为 `QVariant`。基础值直接解码，复合值可能仍是嵌套 `QDBusArgument`；末尾或错误时返回无效 `QVariant`。

### 复合类型边界

写入方向的 `begin...` 和 `end...` 负责声明与关闭容器；读取方向的 `const begin...` 和 `const end...` 负责进入与退出已有容器。每一次 begin 必须有完全匹配的 end。

### 基础流运算符

写入 `operator<<` 和读取 `operator>>` 分别支持下列同一组 D-Bus 基础或特别包装类型：

```text
uchar, bool, short, ushort, int, uint, qlonglong, qulonglong, double,
QString, QDBusVariant, QDBusObjectPath, QDBusSignature,
QDBusUnixFileDescriptor, QStringList, QByteArray
```

这些运算符会按 D-Bus 对应类型连续写入或读取一个元素。读取类型必须与实际协议匹配；不要依赖“看起来可以转换”的 C++ 隐式转换来掩盖协议错误。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDBusArgument()` | 创建空编解码流。 | 空对象不能直接读写，通常由 Qt D-Bus 在序列化边界提供。 |
| 复制构造 | `QDBusArgument(const QDBusArgument &other)` | 创建 `other` 的共享副本。 | 读写位置也共享，不能当作独立游标。 |
| 移动构造 | `QDBusArgument(QDBusArgument &&other)` | 移入 argument 状态。 | 移动后不要再读取或写入源对象。 |
| 复制赋值 | `operator=(const QDBusArgument &other)` | 改为共享 `other` 的状态。 | 会放弃当前状态，副本仍共享游标。 |
| 移动赋值 | `operator=(QDBusArgument &&other)` | 用移动方式替换当前状态。 | 源对象仅可析构或重新赋值。 |
| 析构 | `~QDBusArgument()` | 释放关联的编解码资源。 | 不需要手动释放由 Qt 传入的 argument。 |
| 交换 | `swap(QDBusArgument &other)` | 快速交换两个流状态。 | 用于算法或实现代码，不改变已编码的数据布局。 |
| 类型检查 | `ElementType currentType() const` | 获取当前待读元素的类别。 | 只适合读取方向；错误、末尾、写入时为 `UnknownType`。 |
| 签名检查 | `QString currentSignature() const` | 获取当前元素的 D-Bus 签名。 | 用于调试或动态解析，不替代固定协议的类型化读取。 |
| 末尾检查 | `bool atEnd() const` | 判断当前 array 或 map 是否读完。 | 在 `beginArray()`、`beginMap()` 读取循环中使用。 |
| 动态读取 | `QVariant asVariant() const` | 将当前元素读取为 QVariant。 | 复合类型可能得到嵌套 QDBusArgument；无效时返回 invalid QVariant。 |
| 写结构体 | `beginStructure()` 与 `endStructure()` | 开始并结束结构体编码。 | 读写端字段数、顺序、类型必须严格相同。 |
| 读结构体 | `beginStructure() const` 与 `endStructure() const` | 进入并退出结构体解码。 | 必须和消息中的真实结构布局配对。 |
| 写数组 | `beginArray(QMetaType)` 与 `endArray()` | 声明元素类型并编码数组。 | D-Bus 数组元素类型固定，传入正确的元素 QMetaType。 |
| 读数组 | `beginArray() const` 与 `endArray() const` | 进入并退出数组解码。 | 逐项读取到 `atEnd()` 为止。 |
| 写字典 | `beginMap(keyType, valueType)` 与 `endMap()` | 声明 key-value 类型并编码 map。 | 每项必须包含一对 key 和 value。 |
| 读字典 | `beginMap() const` 与 `endMap() const` | 进入并退出 map 解码。 | 循环内用 map entry API 读取每一项。 |
| 写字典项 | `beginMapEntry()` 与 `endMapEntry()` | 写入一个 key-value 对。 | 只能嵌套在已打开的 map 内。 |
| 读字典项 | `beginMapEntry() const` 与 `endMapEntry() const` | 进入并退出一个 key-value 对。 | 必须按 key 后 value 的顺序读取。 |
| 低层 variant 写入 | `appendVariant(const QVariant &v)` | 向流追加 QVariant 形式的值。 | 用于低层动态类型路径；需要 D-Bus `v` 时确认 QDBusVariant 语义。 |
| 基础写入 | `operator<<(T)` | 写入基础值、Qt 特别类型或 D-Bus 包装类型。 | 支持 `uchar` 到 `double`、QString、QDBusVariant、路径、签名、fd、QStringList、QByteArray。 |
| 基础读取 | `operator>>(T &)` | 读取基础值、Qt 特别类型或 D-Bus 包装类型。 | 目标类型必须与协议签名匹配，读取顺序不可改变。 |
| QVariant 读取 | `operator>>(QVariant &v)` | 解码当前值为 QVariant。 | 复杂类型可能仍表现为 QDBusArgument。 |
| 类型注册 | `qDBusRegisterMetaType<T>()` | 注册自定义类型的 D-Bus 编解码信息。 | 在首次跨 D-Bus 使用前调用，且先定义流运算符。 |
| 便捷转换 | `qdbus_cast<T>(QDBusArgument)` | 通过 `operator>>` 解码一个 T。 | 依赖你的解码运算符和正确的协议布局。 |
| 便捷转换 | `qdbus_cast<T>(QVariant)` | 从 QVariant 或其中的 QDBusArgument 解码 T。 | 普通 QVariant 路径使用 qvariant_cast，不会修复类型不匹配。 |

---

### 一句话总结

`QDBusArgument` 是 Qt 与 D-Bus 类型系统之间的双向流；给自定义类型实现严格对称的读写运算符并提前注册，才能让复杂参数稳定地跨进程传递。
