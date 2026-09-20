# Qt QMetaType 类型描述、注册与擦除操作笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMetaType>`  
> 所属模块：`Qt6::Core`  
> 类型性质：轻量级的类型描述句柄，不保存具体对象值  
> 相关类型：`QVariant`、`QMetaObject`、`QMetaSequence`、`QMetaAssociation`、`QDataStream`、`QDebug`

## 1. 它解决什么问题

普通 C++ 代码在编译期知道 `T` 是什么，因此可以直接调用构造函数、析构函数、拷贝函数和转换函数。Qt 的很多边界 API 却只能在运行时拿到：

- 一个整数类型 ID；
- 一个类型名字；
- 一个 `QVariant`；
- 一个 queued signal/slot 参数；
- 一个插件或配置文件声明的类型；
- 一块没有静态类型的存储空间。

`QMetaType` 把这些运行时信息集中成一个类型描述句柄。它可以告诉 Qt：

- 这个类型叫什么、大小是多少、需要什么对齐；
- 是否可以默认构造、拷贝构造、移动构造和析构；
- 如何在预分配空间中构造或销毁对象；
- 是否支持比较、调试输出和 `QDataStream`；
- 是否存在从一个类型到另一个类型的转换或可变视图；
- 这个类型是否对应 QObject、gadget 或枚举的 `QMetaObject`。

它本身不是 `QVariant`，也不拥有一个 `T` 对象。可以把它理解成“对 `T` 的操作表的一个小句柄”：真正的值仍然位于调用方提供的地址中。

## 2. 实际使用场景

### 2.1 自定义值放入 `QVariant`

```cpp
#include <QMetaType>
#include <QVariant>

struct Message
{
    QString text;
    int priority = 0;
};

Q_DECLARE_METATYPE(Message)

void storeMessage(const Message &message)
{
    const QVariant value = QVariant::fromValue(message);
    const Message restored = value.value<Message>();
    Q_ASSERT(restored.text == message.text);
}
```

`Q_DECLARE_METATYPE(Message)` 让模板化的 `QVariant::fromValue()`、`value<T>()` 和 `qMetaTypeId<T>()` 能识别这个类型。它不等于已经为按名字查找或 queued 连接完成运行时注册，后者通常还需要 `qRegisterMetaType<Message>()`。

### 2.2 queued signal/slot 传递自定义类型

```cpp
class Producer : public QObject
{
    Q_OBJECT
signals:
    void messageReady(Message message);
};

class Consumer : public QObject
{
    Q_OBJECT
public slots:
    void consume(Message message);
};

void connectProducer(Producer *producer, Consumer *consumer)
{
    qRegisterMetaType<Message>();
    QObject::connect(producer, &Producer::messageReady,
                     consumer, &Consumer::consume,
                     Qt::QueuedConnection);
}
```

注册必须发生在建立连接之前。queued 调用需要在事件队列中复制和销毁参数，因此 `Message` 必须满足相应的可复制、可析构和元类型要求；只声明 `Q_DECLARE_METATYPE` 而没有运行时注册，常常会在连接或投递时失败。

### 2.3 按类型描述动态创建和销毁对象

```cpp
QMetaType type = QMetaType::fromType<Message>();
void *raw = type.create();
if (raw) {
    auto *message = static_cast<Message *>(raw);
    message->priority = 10;
    type.destroy(raw);
}
```

`create()` 返回由 Qt 分配并构造的对象，配对操作是同一个 `QMetaType` 的 `destroy()`。如果使用 `construct()` 在调用方提供的存储中 placement-new，则必须用 `destruct()`，不能用 `destroy()` 去释放并非由 `create()` 分配的地址。

### 2.4 插件、脚本和属性系统中的按名查找

```cpp
const int id = qRegisterMetaType<Message>("Message");
Q_UNUSED(id);

const QMetaType type = QMetaType::fromName("Message");
if (!type.isValid()) {
    return;
}

qDebug() << type.name() << type.sizeOf() << type.alignOf();
```

按名字查找没有编译期检查。名称必须和已经注册的名称或规范化别名一致；如果插件卸载后仍保存着依赖插件类型的描述或函数指针，调用方还必须负责处理模块生命周期。

### 2.5 为 QVariant 或容器提供转换和可变视图

```cpp
struct Celsius
{
    double value = 0.0;
};

struct Fahrenheit
{
    double value = 0.0;
};

Q_DECLARE_METATYPE(Celsius)
Q_DECLARE_METATYPE(Fahrenheit)

void installConverter()
{
    QMetaType::registerConverter<Celsius, Fahrenheit>(
        [](const Celsius &source) {
            return Fahrenheit{source.value * 9.0 / 5.0 + 32.0};
        });
}
```

注册后，`QMetaType::canConvert()` 可以查询“是否存在转换路径”，`QMetaType::convert()` 才会对具体值执行转换。`canConvert()` 说明的是能力，不保证某个输入值一定转换成功，例如数值溢出、用户自定义转换返回失败都可能使实际调用返回 `false`。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QMetaType>
```

常见协作类型还需要按使用场景包含：

```cpp
#include <QDataStream>  // save/load
#include <QDebug>       // debugStream 和 QDebug 输出
#include <QMetaObject>  // metaObject、规范化类型名
#include <QVariant>     // QVariant::fromValue
```

## 4. 先分清四件事：声明、注册、描述和值

这是 `QMetaType` 最容易混淆的部分。

### 4.1 `Q_DECLARE_METATYPE(T)`：让模板 API 认识类型

它通常放在完整定义之后：

```cpp
struct Message
{
    QString text;
};

Q_DECLARE_METATYPE(Message)
```

它主要解决：

- `QVariant::fromValue()` 和 `QVariant::value<T>()`；
- `qMetaTypeId<T>()`；
- 模板化的元类型查询；
- 类型的编译期声明信息。

该宏要求类型在宏展开处已经完整定义，并且适合值语义使用。面向 `QVariant` 的自定义类型通常应有公开默认构造、拷贝构造和析构。

### 4.2 `qRegisterMetaType<T>()`：把类型名注册到运行时表

```cpp
qRegisterMetaType<Message>();
qRegisterMetaType<Message>("ProtocolMessage");
```

它主要解决：

- queued signal/slot 在运行时按类型名复制参数；
- `QMetaType::fromName()` 按名称查找；
- 运行时属性和其他字符串驱动的元对象 API。

需要在第一次建立 queued 连接之前调用。返回值是运行时类型 ID。

### 4.3 `QMetaType::fromType<T>()`：得到类型描述句柄

```cpp
const QMetaType type = QMetaType::fromType<Message>();
```

这一步得到的是描述，不是对象。`fromType<T>()` 本身是编译期模板入口，但调用 `id()`、`registerType()` 或 `qRegisterMetaType()` 时可能触发运行时 ID 注册。

### 4.4 `QVariant` 或 raw `void *`：真正保存值

`QMetaType` 的 `create()`、`construct()`、`convert()`、`view()` 都需要一个真实地址。地址的对象类型、存储大小、对齐、构造状态必须和传入的 `QMetaType` 严格匹配。

## 5. 生命周期、所有权和线程边界

### 5.1 `QMetaType` 句柄通常很轻

`QMetaType` 内部只是指向类型接口的描述指针。复制一个 `QMetaType` 不会复制任何用户对象，也不会取得某个 `QVariant` 的所有权。

### 5.2 `create()` 与 `destroy()` 成对

```cpp
const QMetaType type = QMetaType::fromType<Message>();
void *data = type.create();
// 使用 data 指向的 Message
type.destroy(data);
```

不要对 `create()` 返回值调用普通 `delete`，也不要把外部栈对象传给 `destroy()`。

### 5.3 `construct()` 与 `destruct()` 只管理对象生命周期

```cpp
alignas(Message) std::byte storage[sizeof(Message)];
const QMetaType type = QMetaType::fromType<Message>();

void *data = type.construct(storage);
if (data) {
    auto *message = static_cast<Message *>(data);
    message->priority = 1;
    type.destruct(data);
}
```

调用方负责提供足够大且正确对齐的存储；`destruct()` 调析构函数，但不释放这块存储。`construct()` 返回的地址通常就是 `where`，但应以返回值是否为空作为成功判断。

### 5.4 类型注册表是线程安全的，不代表值对象自动线程安全

Qt 文档将 `QMetaType` 的函数标为线程安全，但这只覆盖类型描述和注册表的并发访问。由 `void *` 指向的对象是否能跨线程访问，仍由业务代码保证；可变 view 还可能把一个容器的内部存储暴露给另一个线程。

## 6. 类型 ID、名称和有效性

### 6.1 有效和已注册不是同一个问题

```cpp
QMetaType type = QMetaType::fromType<Message>();

if (!type.isValid())
    return;

const char *name = type.name();
const int id = type.id();
const bool registered = type.isRegistered();
```

- `isValid()`：句柄是否指向一个有效类型描述；
- `id()`：取得或分配运行时类型 ID；
- `isRegistered()`：该类型是否已经有运行时注册 ID。

一个 `fromType<T>()` 得到的描述可以有效，但在尚未调用需要运行时 ID 的 API 之前，注册状态和名称查找仍应按实际调用结果检查。

### 6.2 不要硬编码自定义类型 ID

Qt 内置类型使用 `QMetaType::Type` 中的固定枚举值；用户类型从 `QMetaType::User` 起由运行时分配。用户代码应保存 `QMetaType` 或通过 `QMetaType::fromType<T>()` 获取，不应把一个自定义 ID 写死到协议或文件格式中。

### 6.3 类型名称不是任意 C++ 拼写

`name()` 返回元类型记录的名称，通常是规范化后的类型名。`fromName()` 只接受已注册名称或通过注册机制加入的规范化别名；多余空格、别名写法和命名空间差异都可能导致查找失败。

## 7. `QMetaType` 与 `QMetaObject`

`metaObject()` 只有在类型本身带有相关 Qt 元对象信息时才有意义，常见情况包括：

- `QObject` 派生类型或其指针；
- `Q_GADGET` 类型或其指针；
- 使用 `Q_ENUM`/`Q_ENUM_NS` 暴露的枚举；
- 某些 Qt 内置对象类型。

普通结构体的 `metaObject()` 通常返回 `nullptr`。它也不会把任意 C++ 类型自动变成 `QMetaObject`，更不会返回某个具体对象实例的状态。

```cpp
const QMetaType type = QMetaType::fromType<QObject *>();
if (const QMetaObject *meta = type.metaObject())
    qDebug() << meta->className();
```

## 8. 比较能力与流能力

### 8.1 能力查询应优先于直接调用

```cpp
if (type.isEqualityComparable()) {
    const bool same = type.equals(lhs, rhs);
}

if (type.isOrdered()) {
    const QPartialOrdering order = type.compare(lhs, rhs);
}
```

`equals()` 要求 `lhs` 和 `rhs` 都指向该类型的有效对象。`compare()` 返回 `QPartialOrdering`，可能是 `Less`、`Equivalent`、`Greater` 或 `Unordered`。没有可用的 `<` 比较能力，或具体值不可排序时，不应把 `Unordered` 当成“相等”。

### 8.2 调试输出和数据流

```cpp
if (type.hasRegisteredDebugStreamOperator())
    type.debugStream(qDebug(), &message);

if (type.hasRegisteredDataStreamOperators()) {
    type.save(stream, &message);
    type.load(stream, &message);
}
```

Qt 6 会根据可见的 `QDebug`/`QDataStream` 运算符自动建立相应能力。`save()`、`load()` 和 `debugStream()` 都返回 `bool`，必须检查失败。它们不会自动为自定义协议写入版本号、长度或错误恢复策略。

## 9. 转换与 mutable view 的区别

### 9.1 `convert()` 产生目标值

```cpp
const Celsius source{20.0};
Fahrenheit target;

const bool ok = QMetaType::convert(
    QMetaType::fromType<Celsius>(), &source,
    QMetaType::fromType<Fahrenheit>(), &target);
```

转换函数把源对象转换成目标对象。`to` 必须是指向目标类型存储的有效指针；实际使用中通常先构造一个 `Fahrenheit target`，让转换函数给它赋值。

### 9.2 `view()` 生成目标视图

```cpp
struct Packet
{
    QByteArray bytes;
};

Q_DECLARE_METATYPE(Packet)

void registerPacketView()
{
    QMetaType::registerMutableView<Packet, QByteArrayView>(
        [](Packet &packet) {
            return QByteArrayView(packet.bytes);
        });
}

void inspectPacket(Packet &packet)
{
    QByteArrayView view;
    const bool ok = QMetaType::view(
        QMetaType::fromType<Packet>(), &packet,
        QMetaType::fromType<QByteArrayView>(), &view);
    if (ok)
        qDebug() << view;
}
```

mutable view 的源指针是非 `const`，因为它表达的是可以从源对象建立“可变观察入口”的能力。视图是否真的能修改源对象取决于目标类型和注册函数的语义；`QByteArrayView` 本身只是借用数据，不拥有 `Packet::bytes` 的存储。

### 9.3 `canConvert()` 和 `canView()` 只查询路径

- `canConvert()` 返回是否存在可执行的转换路径；
- `canView()` 返回是否存在可执行的 mutable view；
- 两者都不保证具体输入一定成功；
- `canView()` 为 QObject 指针时还可能表示类似 `qobject_cast()` 的类型关系；
- 已通过 `Q_DECLARE_SEQUENTIAL_CONTAINER_METATYPE()` 或 `Q_DECLARE_ASSOCIATIVE_CONTAINER_METATYPE()` 声明的容器可以获得到 `QMetaSequence::Iterable` 或 `QMetaAssociation::Iterable` 的 view。

## 10. 注册自定义转换

### 10.1 隐式转换

```cpp
QMetaType::registerConverter<Celsius, Fahrenheit>(
    [](const Celsius &source) {
        return Fahrenheit{source.value * 9.0 / 5.0 + 32.0};
    });
```

`registerConverter<From, To>()` 的函数对象可以返回 `To`，也可以返回 `std::optional<To>`。返回空 `std::optional` 表示这一次输入转换失败。

### 10.2 成员函数转换

```cpp
class Version
{
public:
    QString toString() const;
    int toInt(bool *ok) const;
};

Q_DECLARE_METATYPE(Version)
QMetaType::registerConverter<Version, QString>(&Version::toString);
QMetaType::registerConverter<Version, int>(&Version::toInt);
```

`To (From::*)() const` 适合总能成功的成员函数；`To (From::*)(bool *) const` 允许成员函数通过 `bool *` 报告本次输入是否有效，失败时 Qt 会把目标设置为默认构造值。

### 10.3 注册的边界

- Qt 要求至少一端是自定义类型，不能用它覆盖两个内置类型之间的基础转换；
- 同一 `From -> To` 转换通常只能注册一次，重复注册会返回 `false`；
- 转换函数必须可以在 Qt 的擦除调用约定下工作；
- 注册函数不会改变 `From` 对象的生命周期；
- 转换函数捕获的状态必须在注册仍然有效期间保持可用；
- `hasRegisteredConverterFunction()` 只能说明函数是否存在，不能验证函数内部逻辑。

## 11. 容器和智能指针的元类型声明

### 11.1 顺序容器

```cpp
#include <deque>

Q_DECLARE_SEQUENTIAL_CONTAINER_METATYPE(std::deque)
```

声明后，`std::deque<T>` 可以在 `T` 本身已被 `QMetaType` 认识时参与 `QVariant`、容器转换和 `QMetaSequence` 的迭代封装。Qt 容器以及 `std::vector`、`std::list` 已有内置支持，不需要重复声明。

### 11.2 关联容器

```cpp
#include <unordered_map>

Q_DECLARE_ASSOCIATIVE_CONTAINER_METATYPE(std::unordered_map)
```

`T` 和 `U` 都必须是元类型可识别的键和值类型。关联容器的 `QMetaAssociation` view 不等于把容器复制成 `QVariantMap`；它仍然借用原容器，迭代和修改边界由原容器决定。

### 11.3 智能指针

```cpp
#include <memory>

Q_DECLARE_SMART_POINTER_METATYPE(std::shared_ptr)
```

该宏主要面向指向 QObject 派生类的智能指针，并可以建立到 `QObject *` 的转换。它不会替 `std::shared_ptr` 变成 Qt 对象树所有权，也不会延长 QObject 在对象树中的生命周期。

## 12. 逐项 API 说明

以下按 Qt 6.11.1 头文件中的公开入口分组。私有的 `QtPrivate::QMetaTypeInterface` 字段和 `iface()` 不属于普通业务 API。

### 12.1 `enum QMetaType::Type`

`Type` 是内置类型和运行时类型 ID 的兼容枚举。业务代码应使用枚举名字或 `QMetaType` 对象，不应依赖自定义类型的数值。

| 分组 | 常量 |
| --- | --- |
| 无效和用户类型 | `UnknownType`、`User` |
| 基础类型 | `Void`、`Bool`、`Int`、`UInt`、`LongLong`、`ULongLong`、`Double`、`Long`、`Short`、`Char`、`Char16`、`Char32`、`ULong`、`UShort`、`UChar`、`Float`、`SChar`、`Nullptr`、`Float16` |
| 指针和枚举辅助类型 | `VoidStar`、`QObjectStar`、`QCborSimpleType` |
| Core 值类型 | `QChar`、`QString`、`QByteArray`、`QBitArray`、`QDate`、`QTime`、`QDateTime`、`QUrl`、`QLocale`、`QRect`、`QRectF`、`QSize`、`QSizeF`、`QLine`、`QLineF`、`QPoint`、`QPointF`、`QEasingCurve`、`QUuid`、`QVariant`、`QModelIndex`、`QPersistentModelIndex`、`QRegularExpression`、`QJsonValue`、`QJsonObject`、`QJsonArray`、`QJsonDocument`、`QCborValue`、`QCborArray`、`QCborMap` |
| Core 模板类型 | `QVariantMap`、`QVariantList`、`QVariantHash`、`QVariantPair`、`QByteArrayList`、`QStringList` |
| GUI 类型 | `QFont`、`QPixmap`、`QBrush`、`QColor`、`QPalette`、`QIcon`、`QImage`、`QPolygon`、`QRegion`、`QBitmap`、`QCursor`、`QKeySequence`、`QPen`、`QTextLength`、`QTextFormat`、`QTransform`、`QMatrix4x4`、`QVector2D`、`QVector3D`、`QVector4D`、`QQuaternion`、`QPolygonF`、`QColorSpace` |
| Widgets 类型 | `QSizePolicy` |
| 范围和别名 | `FirstCoreType`、`LastCoreType`、`FirstGuiType`、`LastGuiType`、`FirstWidgetsType`、`LastWidgetsType`、`HighestInternalId`、`QReal` |

常用数值约定：

- `UnknownType` 为 `0`；
- 用户类型从 `User`（`65536`）开始由 Qt 分配；
- `QReal` 根据平台上的 `qreal` 大小映射到 `Double` 或 `Float`；
- 其他内置 ID 应通过枚举或 `QMetaType::fromType<T>()` 使用，不应复制到业务协议中。

### 12.2 `enum QMetaType::TypeFlag` 与 `TypeFlags`

| 标志 | 含义 |
| --- | --- |
| `NeedsConstruction` | 默认构造不能只靠简单的零初始化完成，或类型需要显式构造操作 |
| `NeedsDestruction` | 析构时需要调用非平凡析构逻辑 |
| `RelocatableType` | Qt 可以按可移动/可重新定位类型处理其存储 |
| `MovableType` | `RelocatableType` 的旧名称，已弃用 |
| `PointerToQObject` | 类型是指向 QObject 派生类的指针 |
| `IsEnumeration` | 类型是枚举或 `QFlags` |
| `SharedPointerToQObject` | 类型是指向 QObject 派生类的共享指针 |
| `WeakPointerToQObject` | 类型是指向 QObject 派生类的弱指针 |
| `TrackingPointerToQObject` | 类型是 `QPointer<T>` 一类的跟踪指针 |
| `IsUnsignedEnumeration` | 枚举的底层类型是无符号类型 |
| `IsGadget` | 类型带有 gadget 元对象 |
| `PointerToGadget` | 类型是指向 gadget 的指针 |
| `IsPointer` | 类型是指针 |
| `IsQmlList` | 类型被 QML 识别为列表类型 |
| `IsConst` | 指针指向的对象带有 `const` 限定 |
| `NeedsCopyConstruction` | Qt 6.5 起：拷贝构造不是平凡操作 |
| `NeedsMoveConstruction` | Qt 6.5 起：移动构造不是平凡操作 |

`TypeFlags` 是对 `TypeFlag` 的 `QFlags` 封装。Qt 文档建议优先使用 `isDefaultConstructible()`、`isCopyConstructible()`、`isMoveConstructible()`、`isDestructible()`、`isEqualityComparable()` 和 `isOrdered()` 等语义查询，而不是直接组合底层标志。

### 12.3 `QMetaType::ConverterFunction`

```cpp
using ConverterFunction =
    std::function<bool(const void *src, void *target)>;
```

这是类型擦除后的转换回调签名。`src` 指向源对象，`target` 指向已经准备好的目标存储。它适合元类型基础设施；普通业务优先使用模板化的 `registerConverter<From, To>()`，让编译器检查类型。

### 12.4 `QMetaType::MutableViewFunction`

```cpp
using MutableViewFunction =
    std::function<bool(void *src, void *target)>;
```

与 `ConverterFunction` 的关键区别是源对象不是 `const`。回调可以根据源对象建立一个目标 view；是否共享存储、是否允许修改、view 的有效期，都必须由注册函数和目标类型的语义明确保证。

### 12.5 构造函数

#### `QMetaType::QMetaType()`

构造一个无效的 `QMetaType`。默认构造结果可以用作“尚未找到类型”的哨兵：

```cpp
QMetaType type;
if (!type.isValid()) {
    // 尚未绑定到任何类型
}
```

#### `explicit QMetaType::QMetaType(int typeId)`

根据运行时类型 ID 创建描述句柄。传入未知或无效 ID 时，必须通过 `isValid()` 检查结果；不要假定任意整数都对应一个合法类型。

### 12.6 身份、名称和描述查询

#### `bool isValid() const`

判断句柄是否有类型描述。默认构造的句柄和 `fromName()` 查找失败的结果通常无效。

#### `bool isRegistered() const`

判断当前描述是否已有运行时注册 ID。它不是“这个类型能不能放进 QVariant”的唯一判断，也不替代 `isValid()`。

#### `static bool isRegistered(int type)`

按整数 ID 查询注册状态。传入 `0` 或未知 ID 时应按 `false` 处理。

#### `int id() const`

返回运行时类型 ID。对自定义类型，调用它可能触发注册；无效类型返回 `0`。不要让返回的自定义 ID 脱离当前进程当作稳定持久化值。

#### `void registerType() const`

Qt 6.5 起，确保当前类型进入运行时注册表。它没有返回值；需要 ID 时随后调用 `id()`，或直接使用 `qRegisterMetaType(QMetaType)`。

#### `static QMetaType fromType<T>()`

按编译期类型生成描述句柄。`T` 必须在调用点满足 Qt 的完整类型和指针规则；指向前置声明类型的指针通常需要 `Q_DECLARE_OPAQUE_POINTER`。它不保存 `T` 的对象值。

#### `static QMetaType fromName(QByteArrayView typeName)`

按运行时名称查找类型。找不到时返回无效句柄。它不会因为一个 C++ 类型“存在”就自动知道该类型，必须先完成相应的运行时注册。

#### `const char *name() const`

返回元类型保存的名称。指针由 Qt 的元类型描述拥有，不应由调用方释放；如果要跨模块卸载或长期保存，应复制到 `QByteArray`。

#### `const QMetaObject *metaObject() const`

返回该类型关联的元对象；普通值类型通常返回 `nullptr`。返回指针由类型所属模块的元对象系统管理，不要删除。

#### `qsizetype sizeOf() const`

返回实际类型的 `sizeof(T)`。无效句柄返回 `0`。可与 `construct()` 一起用于分配 raw 存储，但还必须同时满足 `alignOf()`。

#### `qsizetype alignOf() const`

返回实际类型的对齐要求。无效句柄返回 `0`。只分配足够字节数而没有满足对齐要求，会导致未定义行为。

#### `TypeFlags flags() const`

返回类型属性标志。它适合做底层能力检查；需要具体语义时优先调用相应的 `is...()` 函数。

#### `QMetaType underlyingType() const`

Qt 6.6 起取得枚举的底层数值类型。对普通枚举返回具有相同位宽和有符号性的数值元类型；对 `QFlags` 返回 `Int`；如果当前类型不是枚举或 flags，返回无效 `QMetaType`。

### 12.7 构造、销毁和存储操作

#### `void *create(const void *copy = nullptr) const`

分配并构造一个当前类型的对象：

- `copy == nullptr` 时尝试默认构造；
- `copy != nullptr` 时从同类型对象拷贝构造；
- 失败时返回 `nullptr`；
- 返回的地址必须交给同一个 `QMetaType::destroy()`。

`copy` 必须确实指向当前类型的对象，不能只因为内存大小相同就传入另一种类型。

#### `void destroy(void *data) const`

销毁并释放 `create()` 得到的对象。`data == nullptr` 可以作为无对象状态处理，但非空指针必须来自匹配类型和匹配分配方式。

#### `void *construct(void *where, const void *copy = nullptr) const`

在调用方提供的 `where` 中构造当前类型。`where` 必须满足 `sizeOf()` 和 `alignOf()`；如果 `copy` 非空，它执行拷贝构造，否则执行默认构造。它只构造，不负责分配存储。

#### `void destruct(void *data) const`

调用当前类型的析构逻辑，但不释放 `data` 指向的存储。它必须和 placement construction 或 `construct()` 配对，不能用来替代 `destroy()` 释放堆内存。

### 12.8 可构造性和比较能力

#### `bool isDefaultConstructible() const noexcept`

判断元类型是否记录了默认构造能力。返回 `true` 不代表调用方提供的存储已经准备好；调用 `construct()` 仍需满足地址和生命周期规则。

#### `bool isCopyConstructible() const noexcept`

判断是否可以通过元类型执行拷贝构造。queued 参数和 `QVariant` 值语义通常需要这项能力。

#### `bool isMoveConstructible() const noexcept`

Qt 6.5 起，判断是否记录了移动构造能力。它不表示 Qt 一定会在每个容器路径上使用移动构造。

#### `bool isDestructible() const noexcept`

判断是否可以正确执行析构。无效句柄返回 `false`。

#### `bool isEqualityComparable() const`

判断是否有可用的相等比较操作。只有返回 `true` 时才应把 `equals()` 作为有效业务判断。

#### `bool isOrdered() const`

判断是否有可用的顺序比较操作。浮点 NaN 等具体值仍可能使 `compare()` 返回 `Unordered`。

#### `QPartialOrdering compare(const void *lhs, const void *rhs) const`

比较两个当前类型的对象，返回 `Less`、`Equivalent`、`Greater` 或 `Unordered`。`lhs`、`rhs` 必须是有效对象地址；不能把 `nullptr` 当作“空值”传入。

#### `bool equals(const void *lhs, const void *rhs) const`

使用元类型记录的相等比较操作。无相等操作时不要调用；未排序值的相等语义和顺序比较语义也不能混为一谈。

### 12.9 数据流和调试流

#### `bool save(QDataStream &stream, const void *data) const`

把 `data` 指向的当前类型对象写入数据流。没有注册或自动发现数据流运算符时返回 `false`。`data` 必须指向已构造的当前类型对象。

#### `bool load(QDataStream &stream, void *data) const`

从数据流加载到已构造的当前类型对象。它不会替调用方分配 `data`，也不会自动回滚一个已经部分修改的对象。

#### `bool hasRegisteredDataStreamOperators() const`

查询当前类型是否有可用的 `QDataStream` 输入输出运算符。它只表示能力存在，不表示当前流状态一定正常。

#### `bool debugStream(QDebug &dbg, const void *rhs)`

把对象写入调试流。没有可用 debug stream operator 时返回 `false`。Qt 构建时若禁用了 debug stream，这组 API 可能不可用。

#### `bool hasRegisteredDebugStreamOperator() const`

查询是否存在可用的 debug stream operator。

### 12.10 转换和 mutable view

#### `static bool canConvert(QMetaType fromType, QMetaType toType)`

查询是否存在从 `fromType` 到 `toType` 的转换路径。它不执行转换，也不保证某个具体值一定成功。

#### `static bool convert(QMetaType fromType, const void *from, QMetaType toType, void *to)`

把 `from` 指向的源对象转换到 `to` 指向的目标存储。两端指针都必须有效，类型必须和对应 `QMetaType` 完全匹配；目标对象的构造、存储和最终销毁由调用方负责。

#### `static bool canView(QMetaType fromType, QMetaType toType)`

查询是否存在从源对象建立目标 mutable view 的能力。view 的生命周期通常受源对象限制，不能像独立值一样长期保存。

#### `static bool view(QMetaType fromType, void *from, QMetaType toType, void *to)`

在 `to` 指向的预分配目标存储中创建 view。源 `from` 必须是非 `const` 有效对象，目标类型必须与注册的 view 约定一致。

#### `static bool hasRegisteredConverterFunction(QMetaType fromType, QMetaType toType)`

查询指定两个 `QMetaType` 之间是否有显式注册的转换函数。它不包含所有内置转换规则的全部语义，不应单独用来代替 `canConvert()`。

#### `static bool hasRegisteredConverterFunction<From, To>()`

模板化的类型版本，避免手工构造两个 `QMetaType`。

#### `static bool hasRegisteredMutableViewFunction(QMetaType fromType, QMetaType toType)`

查询两个类型之间是否有显式注册的 mutable view 函数。

#### `static bool hasRegisteredMutableViewFunction<From, To>()`

模板化的 mutable view 能力查询。

### 12.11 注册转换和 view

#### `static bool registerConverter<From, To>()`

注册可由 C++ 隐式转换表达的 `From -> To` 转换。Qt 对内置类型之间的基础转换已有规则，这个模板主要用于至少包含一个自定义类型的转换。

#### `static bool registerConverter<From, To>(To (From::*)() const function)`

把无参数、`const` 成员函数注册为转换函数，例如 `Version::toString() const`。成员函数的返回值必须能赋给 `To`。

#### `static bool registerConverter<From, To>(To (From::*)(bool *) const function)`

注册带 `bool *` 成功标记的 `const` 成员函数。返回失败时 Qt 会把目标设置为 `To()`，因此 `To` 需要适合默认构造。

#### `static bool registerConverter<From, To>(UnaryFunction function)`

注册函数对象、lambda 或函数指针。返回 `To` 表示成功返回值；返回 `std::optional<To>` 时，空值表示本次转换失败。

#### `static bool registerMutableView<From, To>(To (From::*)() function)`

把非 `const` 成员函数注册为 mutable view 生成器。源对象以非 `const` 方式传入，目标 view 的借用关系和有效期由函数实现保证。

#### `static bool registerMutableView<From, To>(UnaryFunction function)`

注册函数对象或 lambda 作为 mutable view 生成器。它只描述怎样写入目标 view，不负责自动延长源对象寿命。

### 12.12 低层类型擦除注册入口

#### `static bool registerConverterFunction(const ConverterFunction &f, QMetaType from, QMetaType to)`

直接安装类型擦除转换回调。它是模板 `registerConverter()` 的底层入口，通常只适合 Qt 容器、框架适配层或需要动态保存回调的基础设施。

#### `static void unregisterConverterFunction(QMetaType from, QMetaType to)`

移除显式注册的转换函数。普通业务通常不应随意撤销全局转换，因为其他模块可能仍在使用这条转换路径。

#### `static bool registerMutableViewFunction(const MutableViewFunction &f, QMetaType from, QMetaType to)`

直接安装类型擦除 mutable view 回调。调用方必须保证函数对象所依赖的代码和状态在注册期间有效。

#### `static void unregisterMutableViewFunction(QMetaType from, QMetaType to)`

移除显式注册的 mutable view 函数。与转换撤销一样，必须明确模块间的注册所有权。

#### `static void unregisterMetaType(QMetaType type)`

从运行时注册机制中撤销一个类型。它属于低层生命周期管理入口；如果仍有 `QVariant`、queued 事件、插件回调或其他模块持有该类型信息，撤销可能造成运行时错误，普通应用通常不应调用。

#### `static void registerNormalizedTypedef(const QByteArray &normalizedTypeName, QMetaType type)`

为已有类型登记一个规范化别名。该函数主要服务于 `qRegisterMetaType<T>(typeName)` 和 Qt 内部注册流程；普通代码优先使用模板注册入口，避免手工维护类型别名表。

### 12.13 旧式兼容 API

Qt 6.11.1 仍可能在启用弃用 API 时提供以下入口，但新代码应使用对应的 `QMetaType` 对象 API：

| 旧入口 | 推荐替代 |
| --- | --- |
| `QMetaType::type(const char *)`、`type(const QByteArray &)` | `QMetaType::fromName(name).id()` |
| `QMetaType::typeName(int)` | `QMetaType(typeId).name()` |
| `QMetaType::sizeOf(int)` | `QMetaType(typeId).sizeOf()` |
| `QMetaType::typeFlags(int)` | `QMetaType(typeId).flags()` |
| `QMetaType::metaObjectForType(int)` | `QMetaType(typeId).metaObject()` |
| `QMetaType::create(int, ...)`、`destroy(int, ...)` | `QMetaType(typeId).create()`、`destroy()` |
| `QMetaType::construct(int, ...)`、`destruct(int, ...)` | `QMetaType(typeId).construct()`、`destruct()` |
| `QMetaType::save(stream, int, data)`、`load(stream, int, data)` | `QMetaType(typeId).save()`、`load()` |
| `QMetaType::debugStream(dbg, data, typeId)` | `QMetaType(typeId).debugStream()` |
| `QMetaType::hasRegisteredDebugStreamOperator(int)` | `QMetaType(typeId).hasRegisteredDebugStreamOperator()` |
| `QMetaType::convert(from, fromId, to, toId)` | `QMetaType::convert(fromType, from, toType, to)` |
| 旧式静态 `compare/equals` | `QMetaType(typeId).compare()`、`equals()` |

兼容入口中的整数 ID、raw 指针和所有权规则与新 API 完全相同；换成旧函数不会降低参数错误的风险。

## 13. 相关非成员 API

### 13.1 `qMetaTypeId<T>()`

```cpp
const int id = qMetaTypeId<Message>();
```

返回编译期已声明类型的元类型 ID。内置类型可以直接使用；自定义类型通常必须先写 `Q_DECLARE_METATYPE(Message)`。它适合模板代码，不适合根据字符串动态查找。

### 13.2 `qRegisterMetaType<T>()`

```cpp
const int id = qRegisterMetaType<Message>();
const int aliasId = qRegisterMetaType<Message>("ProtocolMessage");
```

把类型注册到运行时表并返回 ID。`T` 必须在调用点完整定义；指针类型还要求被指向类型完整，除非使用 `Q_DECLARE_OPAQUE_POINTER`。

需要注意：

- `Q_DECLARE_METATYPE` 解决模板识别；
- `qRegisterMetaType` 解决运行时按名注册；
- queued 连接要在第一次建立连接前注册；
- 不需要为了 `QVariant` 的普通模板存取而盲目提前注册，但属性和运行时名称路径要按其要求注册。

### 13.3 `qRegisterMetaType(QMetaType meta)`

Qt 6.5 起，把已有 `QMetaType` 句柄注册到运行时表并返回 ID。它适合框架代码已经持有描述句柄的情况。

### 13.4 `qHash(QMetaType key, size_t seed = 0)`

Qt 6.4 起为 `QMetaType` 提供哈希。哈希基于类型 ID，适合把 `QMetaType` 作为哈希容器的键；它不对类型所描述的对象值做哈希。

### 13.5 `operator==`、`operator!=`

`QMetaType` 是可相等比较的。两个无效句柄相等；两个有效句柄按元类型身份比较。句柄相等只说明“描述的是同一元类型”，不表示两个 `T` 对象的值相等，值相等要使用 `equals()`。

### 13.6 `QDebug operator<<(QDebug, QMetaType)`

在启用 debug stream 时可把类型描述输出到 `QDebug`。它输出的是元类型信息，不会把某个 `T` 对象值输出出来。

## 14. 相关宏逐项说明

### 14.1 `Q_DECLARE_METATYPE(Type)`

让自定义类型成为模板化 Qt 类型系统的一部分。要求 `Type` 完整定义，且通常应具备公开默认构造、拷贝构造和析构。

适用：

- `QVariant::fromValue()`；
- `QVariant::value<T>()`；
- `qMetaTypeId<T>()`；
- 模板化元类型查询。

不自动完成：

- queued signal/slot 的运行时名称注册；
- 通过字符串调用的全部类型查找；
- QObject 的对象树所有权；
- 自定义序列化协议。

### 14.2 `Q_DECLARE_OPAQUE_POINTER(PointerType)`

告诉 Qt：这个指针可以作为不检查所指向完整对象布局的 opaque pointer 注册。它适用于前置声明类型的指针，但不负责解引用、不提供析构器，也不让不完整类型变得可安全访问。

不要把它当作 QObject/gadget 指针的通用替代方案；对于已有 Qt 元对象的对象指针，应让 Qt 使用其正常的 QObject/gadget 类型信息。

### 14.3 `Q_DECLARE_SEQUENTIAL_CONTAINER_METATYPE(Container)`

把单模板参数容器标记为顺序容器，并为 `Container<T>` 建立元类型支持。元素 `T` 必须先能被 `QMetaType` 识别。

Qt 的常用容器以及 `std::vector`、`std::list` 已有支持；对 `std::deque` 等其他容器可按需声明。

### 14.4 `Q_DECLARE_ASSOCIATIVE_CONTAINER_METATYPE(Container)`

把双模板参数容器标记为关联容器，并为 `Container<Key, Value>` 建立元类型支持。键和值类型都必须满足元类型要求。

Qt 关联容器以及 `std::map` 已有支持；例如 `std::unordered_map` 可显式声明。

### 14.5 `Q_DECLARE_SMART_POINTER_METATYPE(SmartPointer)`

为智能指针模板建立元类型支持，主要用于指向 QObject 派生类的智能指针及其到 `QObject *` 的转换。它不改变智能指针本身的所有权语义。

## 15. 常见错误与排查顺序

### 15.1 只写 `Q_DECLARE_METATYPE`，没有运行时注册

**症状：** `QVariant` 模板存取正常，但 queued 连接、属性或 `fromName()` 失败。

**原因：** 模板声明和运行时名称注册是两件事。

**修复：**

```cpp
Q_DECLARE_METATYPE(Message)
qRegisterMetaType<Message>();
```

把注册放在第一次建立 queued 连接之前。

### 15.2 用 `create()` 创建后调用普通 `delete`

**症状：** 内存释放方式不匹配，或析构流程不完整。

**原因：** `create()` 的分配与 `destroy()` 是配对协议。

**修复：** 用同一个 `QMetaType` 调用 `destroy()`。

### 15.3 把 `destroy()` 用在栈对象或 placement-new 存储上

**症状：** 双重释放或堆损坏。

**原因：** `destroy()` 既析构又释放；外部存储只应使用 `destruct()`。

**修复：** `construct()`/外部存储配 `destruct()`，`create()`/Qt 分配配 `destroy()`。

### 15.4 `void *` 地址类型不匹配

**症状：** 转换结果错误、崩溃、析构调用到错误类型。

**原因：** raw API 不带 C++ 编译期类型检查。

**修复：** 同时核对 `QMetaType`、对象实际类型、存储大小、对齐和构造状态。

### 15.5 把 `canConvert()` 当成“本次必然成功”

**症状：** `canConvert()` 为 `true`，但 `convert()` 返回 `false`。

**原因：** 能力查询只说明有一条转换路径；具体值可能溢出或被自定义函数拒绝。

**修复：** 始终检查 `convert()` 返回值。

### 15.6 把 mutable view 当作拥有型副本

**症状：** 源容器销毁或扩容后，view 访问悬空数据。

**原因：** view 通常借用源对象内部存储，不延长源对象寿命。

**修复：** 让源对象在 view 使用期间保持有效；源容器发生可能导致迭代器或内部指针失效的修改后，重新创建 view。

### 15.7 把 `QMetaType` 相等当成值相等

**症状：** 两个相同类型但不同内容的 `QMetaType` 被误判为对象值相等。

**原因：** `operator==` 比较的是类型描述，`equals()` 才比较地址上的两个对象。

**修复：** 明确区分“类型身份”和“对象值”。

### 15.8 把自定义类型 ID 写进文件或网络协议

**症状：** 换进程、插件或构建版本后 ID 不再匹配。

**原因：** 用户类型 ID 是运行时分配的。

**修复：** 持久化稳定的类型名字或业务枚举，读取后通过明确的注册表映射到 `QMetaType`。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `QMetaType::Type` | 描述内置类型和 ID 范围 | 自定义 ID 不稳定，不要硬编码 |
| 枚举 | `QMetaType::TypeFlag` / `TypeFlags` | 描述构造、析构、指针、gadget、枚举等能力 | 具体能力优先使用 `is...()` 查询 |
| 类型别名 | `ConverterFunction` | 类型擦除转换回调 | `src`/`target` 地址类型必须匹配 |
| 类型别名 | `MutableViewFunction` | 类型擦除 mutable view 回调 | 源对象非 const，view 通常借用生命周期 |
| 构造 | `QMetaType()` | 创建无效句柄 | 用 `isValid()` 判断 |
| 构造 | `QMetaType(int typeId)` | 按 ID 创建句柄 | 未知 ID 可能无效 |
| 查询 | `isValid()` | 判断句柄是否有效 | 查找失败和默认句柄都要检查 |
| 查询 | `isRegistered()` | 判断是否已有运行时注册 ID | 不等于值对象可跨线程 |
| 查询 | `isRegistered(int)` | 按 ID 查询注册状态 | 不要传入业务自定义的猜测 ID |
| 注册 | `id()` | 获取或触发运行时 ID | 自定义 ID 只在当前运行时稳定 |
| 注册 | `registerType()` | Qt 6.5 起确保类型注册 | 无返回值，需要 ID 时再调用 `id()` |
| 类型 | `fromType<T>()` | 从编译期类型得到描述 | 要满足完整类型和指针规则 |
| 类型 | `fromName(name)` | 按名称查找描述 | 必须先注册，失败返回无效句柄 |
| 查询 | `name()` | 返回元类型名称 | 返回非拥有 `const char *` |
| 查询 | `metaObject()` | 返回关联元对象 | 普通值类型通常为空 |
| 查询 | `sizeOf()` | 返回类型大小 | 与 `alignOf()` 一起用于 raw 存储 |
| 查询 | `alignOf()` | 返回类型对齐 | 错误对齐会产生未定义行为 |
| 查询 | `flags()` | 返回底层类型标志 | 不要只靠 flag 推断全部语义 |
| 查询 | `underlyingType()` | Qt 6.6 起返回枚举底层数值类型 | 非枚举返回无效；QFlags 返回 `Int` |
| 存储 | `create(copy)` | 分配并构造对象 | 用匹配的 `destroy()` 释放 |
| 存储 | `destroy(data)` | 析构并释放 Qt 分配对象 | 不用于栈或外部存储 |
| 存储 | `construct(where, copy)` | 在外部存储中构造 | 调用方负责大小、对齐和存储 |
| 存储 | `destruct(data)` | 只析构外部存储对象 | 不释放内存 |
| 能力 | `isDefaultConstructible()` | 查询默认构造能力 | 不替代存储检查 |
| 能力 | `isCopyConstructible()` | 查询拷贝构造能力 | queued/QVariant 值语义常需要 |
| 能力 | `isMoveConstructible()` | Qt 6.5 起查询移动构造能力 | 不保证每条路径都会移动 |
| 能力 | `isDestructible()` | 查询析构能力 | 无效句柄为 false |
| 能力 | `isEqualityComparable()` | 查询相等比较能力 | 为 false 时不要调用 `equals()` |
| 能力 | `isOrdered()` | 查询顺序比较能力 | 具体值仍可能 `Unordered` |
| 比较 | `compare(lhs, rhs)` | 返回三向部分序关系 | 处理 `QPartialOrdering::Unordered` |
| 比较 | `equals(lhs, rhs)` | 比较两个对象值 | 地址必须指向同一元类型的对象 |
| 数据流 | `save(stream, data)` | 写出对象 | 检查 bool；不负责协议版本 |
| 数据流 | `load(stream, data)` | 读入对象 | 目标对象和流状态由调用方管理 |
| 数据流 | `hasRegisteredDataStreamOperators()` | 查询数据流能力 | 不等于当前流操作必成功 |
| 调试 | `debugStream(dbg, data)` | 输出对象调试信息 | 无 operator 时返回 false |
| 调试 | `hasRegisteredDebugStreamOperator()` | 查询 debug 输出能力 | 受构建配置影响 |
| 转换 | `canConvert(from, to)` | 查询转换路径 | 不保证具体值成功 |
| 转换 | `convert(fromType, from, toType, to)` | 执行类型转换 | 两端地址和目标存储必须有效 |
| view | `canView(from, to)` | 查询 mutable view 路径 | 不延长源对象生命周期 |
| view | `view(fromType, from, toType, to)` | 写入目标 view | 源必须是非 const，有效期由源决定 |
| 转换注册 | `registerConverter<From, To>()` | 注册隐式转换 | 至少一端应是自定义类型 |
| 转换注册 | `registerConverter(member)` | 注册 const 成员转换 | 成员返回值必须可赋给目标 |
| 转换注册 | `registerConverter(member(bool *))` | 注册带成功标记的转换 | 失败时目标为默认值 |
| 转换注册 | `registerConverter(function)` | 注册 lambda/函数对象 | 可返回 `To` 或 `optional<To>` |
| view 注册 | `registerMutableView(member)` | 注册非 const 成员 view | 不自动维持源生命周期 |
| view 注册 | `registerMutableView(function)` | 注册 lambda/函数对象 view | 目标对象必须预先可写 |
| 能力查询 | `hasRegisteredConverterFunction(...)` | 查询显式转换回调 | 不覆盖全部内置转换语义 |
| 能力查询 | `hasRegisteredMutableViewFunction(...)` | 查询显式 view 回调 | 不保证 view 使用时源仍有效 |
| 非成员 | `qMetaTypeId<T>()` | 获取已声明类型的 ID | 自定义类型通常需要 `Q_DECLARE_METATYPE` |
| 非成员 | `qRegisterMetaType<T>()` | 注册类型和名称 | queued 连接前调用 |
| 非成员 | `qRegisterMetaType(QMetaType)` | 注册已有描述句柄 | Qt 6.5 起 |
| 非成员 | `qHash(QMetaType, seed)` | 哈希类型句柄 | 哈希类型身份，不是对象值 |
| 非成员 | `operator==` / `operator!=` | 比较类型身份 | 不比较 `T` 对象内容 |
| 宏 | `Q_DECLARE_METATYPE(Type)` | 声明自定义值类型 | 完整类型；常需默认/拷贝/析构 |
| 宏 | `Q_DECLARE_OPAQUE_POINTER(PointerType)` | 声明不透明指针 | 不提供解引用和对象元信息 |
| 宏 | `Q_DECLARE_SEQUENTIAL_CONTAINER_METATYPE(Container)` | 声明顺序容器模板 | 元素类型也必须可识别 |
| 宏 | `Q_DECLARE_ASSOCIATIVE_CONTAINER_METATYPE(Container)` | 声明关联容器模板 | Key/Value 都必须可识别 |
| 宏 | `Q_DECLARE_SMART_POINTER_METATYPE(SmartPointer)` | 声明智能指针模板 | 主要面向 QObject 派生对象 |

## 17. 推荐模板

### 17.1 自定义类型的完整注册模板

```cpp
struct SettingsValue
{
    QString key;
    QVariant value;
};

Q_DECLARE_METATYPE(SettingsValue)

void registerSettingsValue()
{
    const int id = qRegisterMetaType<SettingsValue>("SettingsValue");
    Q_ASSERT(id != QMetaType::UnknownType);
}
```

把 `Q_DECLARE_METATYPE` 放在公共类型头文件，把 `qRegisterMetaType` 放在应用启动、线程连接初始化或明确的类型注册函数中。

### 17.2 安全的动态创建模板

```cpp
void *createDefault(QMetaType type)
{
    if (!type.isValid() || !type.isDefaultConstructible())
        return nullptr;
    return type.create();
}

void destroyCreated(QMetaType type, void *data)
{
    if (data)
        type.destroy(data);
}
```

调用方仍需保证 `type` 在 `data` 的整个生命周期内保持匹配；不要把类型句柄和任意 raw 地址拆开传递而丢失配对关系。

### 17.3 转换前后都检查结果

```cpp
bool convertMessage(const Message &source, QString *result)
{
    if (!result)
        return false;

    const QMetaType from = QMetaType::fromType<Message>();
    const QMetaType to = QMetaType::fromType<QString>();
    if (!QMetaType::canConvert(from, to))
        return false;

    return QMetaType::convert(from, &source, to, result);
}
```

## 18. 一句话总结

`QMetaType` 是 Qt 的运行时类型描述和类型擦除操作入口：`Q_DECLARE_METATYPE` 解决模板识别，`qRegisterMetaType` 解决运行时名称和 queued 参数，`fromType/fromName` 提供描述句柄，`create/construct` 管理动态对象，`convert/view` 扩展类型之间的协作；最重要的边界是区分句柄、类型 ID、真实对象存储以及它们各自的生命周期。

## 19. 核对依据

- Qt 6.11.1 本机头文件：`C:\Qt\6.11.1\msvc2022_64\include\QtCore\qmetatype.h`
- [Qt 6.11.1 QMetaType 文档](https://doc.qt.io/qt-6/qmetatype.html)
- [Qt 6.11.1 Creating Custom Qt Types](https://doc.qt.io/qt-6/custom-types.html)
