# QMetaType

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“MetaType”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMetaType` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QMetaType>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
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

- `enum Type { Void, Bool, Int, UInt, Double, …, UnknownType }`
- `enum TypeFlag { NeedsConstruction, NeedsCopyConstruction, NeedsMoveConstruction, NeedsDestruction, RelocatableType, …, IsConst }`
- `flags TypeFlags`

### 公有函数

- `(since 6.0) QMetaType()`
- `QMetaType(int typeId)`
- `(since 6.0) qsizetype alignOf() const`
- `(since 6.0) QPartialOrdering compare(const void *lhs, const void *rhs) const`
- `void * construct(void *where, const void *copy = nullptr) const`
- `void * create(const void *copy = nullptr) const`
- `bool debugStream(QDebug &dbg, const void *rhs)`
- `void destroy(void *data) const`
- `void destruct(void *data) const`
- `(since 6.0) bool equals(const void *lhs, const void *rhs) const`
- `QMetaType::TypeFlags flags() const`
- `(since 6.1) bool hasRegisteredDataStreamOperators() const`
- `(since 6.0) bool hasRegisteredDebugStreamOperator() const`
- `int id() const`
- `(since 6.5) bool isCopyConstructible() const`
- `(since 6.5) bool isDefaultConstructible() const`
- `(since 6.5) bool isDestructible() const`
- `bool isEqualityComparable() const`
- `(since 6.5) bool isMoveConstructible() const`
- `bool isOrdered() const`
- `bool isRegistered() const`
- `bool isValid() const`
- `bool load(QDataStream &stream, void *data) const`
- `const QMetaObject * metaObject() const`
- `const char * name() const`
- `(since 6.5) void registerType() const`
- `bool save(QDataStream &stream, const void *data) const`
- `qsizetype sizeOf() const`
- `(since 6.6) QMetaType underlyingType() const`

### 静态公有成员

- `bool canConvert(QMetaType fromType, QMetaType toType)`
- `bool canView(QMetaType fromType, QMetaType toType)`
- `bool convert(QMetaType fromType, const void *from, QMetaType toType, void *to)`
- `QMetaType fromName(QByteArrayView typeName)`
- `QMetaType fromType()`
- `bool hasRegisteredConverterFunction(QMetaType fromType, QMetaType toType)`
- `bool hasRegisteredConverterFunction()`
- `bool hasRegisteredMutableViewFunction(QMetaType fromType, QMetaType toType)`
- `(since 6.0) bool hasRegisteredMutableViewFunction()`
- `bool isRegistered(int type)`
- `bool registerConverter()`
- `bool registerConverter(To (From::*)() const function)`
- `bool registerConverter(To (From::*)(bool *) const function)`
- `bool registerConverter(UnaryFunction function)`
- `(since 6.0) bool registerMutableView(To (From::*)() function)`
- `(since 6.0) bool registerMutableView(UnaryFunction function)`
- `(since 6.0) bool view(QMetaType fromType, void *from, QMetaType toType, void *to)`

### 相关非成员函数

- `(since 6.4) size_t qHash(QMetaType key, size_t seed = 0)`
- `int qMetaTypeId()`
- `int qRegisterMetaType()`
- `(since 6.5) int qRegisterMetaType(QMetaType meta)`
- `bool operator!=(const QMetaType &lhs, const QMetaType &rhs)`
- `(since 6.5) QDebug operator<<(QDebug d, QMetaType m)`
- `bool operator==(const QMetaType &lhs, const QMetaType &rhs)`

### 公开宏

- `Q_DECLARE_ASSOCIATIVE_CONTAINER_METATYPE(Container)`
- `Q_DECLARE_METATYPE(Type)`
- `Q_DECLARE_OPAQUE_POINTER(PointerType)`
- `Q_DECLARE_SEQUENTIAL_CONTAINER_METATYPE(Container)`
- `Q_DECLARE_SMART_POINTER_METATYPE(SmartPointer)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QMetaType::Type`

**作用与语义：**

以下是`QMetaType`支持的内置类型：
- `QMetaType::Void`：`43`;`void`
- `QMetaType::Bool`：`1`;`bool`
- `QMetaType::Int`：`2`;`int`
- `QMetaType::UInt`：`3`;`unsigned int`
- `QMetaType::Double`：`6`;`double`
- `QMetaType::QChar`：`7`;QChar
- `QMetaType::QString`：`10`;QString
- `QMetaType::QByteArray`：`12`;QByte数组
- `QMetaType::Nullptr`：`51`;`std::nullptr_t`
- `QMetaType::VoidStar`：`31`;`void *`
- `QMetaType::Long`：`32`;`long`
- `QMetaType::LongLong`：`4`;朗朗
- `QMetaType::Short`：`33`;`short`
- `QMetaType::Char`：`34`;`char`
- `QMetaType::Char16`：`56`;`char16_t`
- `QMetaType::Char32`：`57`;`char32_t`
- `QMetaType::ULong`：`35`;`unsigned long`
- `QMetaType::ULongLong`：`5`;乌隆隆
- `QMetaType::UShort`：`36`;`unsigned short`
- `QMetaType::SChar`：`40`;`signed char`
- `QMetaType::UChar`：`37`;`unsigned char`
- `QMetaType::Float`：`38`;`float`
- `QMetaType::Float16`：`63`;qfloat16
- `QMetaType::QObjectStar`：`39`;`QObject` *
- `QMetaType::QBitArray`：`13`;QBitArray
- `QMetaType::QBitmap`：`0x1009`;QBitmap
- `QMetaType::QBrush`：`0x1002`;QBrush
- `QMetaType::QByteArrayList`：`49`;QByteArrayList
- `QMetaType::QCborArray`：`54`;QCborArray
- `QMetaType::QCborMap`：`55`;QCborMap
- `QMetaType::QCborSimpleType`：`52`;QCborSimpleType
- `QMetaType::QCborValue`：`53`;QCborValue
- `QMetaType::QColor`：`0x1003`;QColor
- `QMetaType::QColorSpace`：`0x1017`;QColorSpace（于 Qt 5.15 引入）
- `QMetaType::QCursor`：`0x100a`;QCursor
- `QMetaType::QDate`：`14`;QDate
- `QMetaType::QDateTime`：`16`;QDateTime
- `QMetaType::QEasingCurve`：`29`;QEasing曲线
- `QMetaType::QFont`：`0x1000`;QFont
- `QMetaType::QIcon`：`0x1005`;QIcon
- `QMetaType::QImage`：`0x1006`;Q法师
- `QMetaType::QJsonArray`：`47`;QJsonArray
- `QMetaType::QJsonDocument`：`48`;QJson文档
- `QMetaType::QJsonObject`：`46`;QJson对象
- `QMetaType::QJsonValue`：`45`;QJsonValue
- `QMetaType::QKeySequence`：`0x100b`;QKeySequence
- `QMetaType::QLine`：`23`;QLine
- `QMetaType::QLineF`：`24`;QLineF
- `QMetaType::QLocale`：`18`;QLocale
- `QMetaType::QMatrix4x4`：`0x1011`;QMatrix4x4
- `QMetaType::QModelIndex`：`42`;QModelIndex
- `QMetaType::QPalette`：`0x1004`;QPalette
- `QMetaType::QPen`：`0x100c`;QPen
- `QMetaType::QPersistentModelIndex`：`50`;QPersistentModelIndex（在Qt 5.5引入）
- `QMetaType::QPixmap`：`0x1001`;QPixmap
- `QMetaType::QPoint`：`25`;QPoint
- `QMetaType::QPointF`：`26`;QPointF
- `QMetaType::QPolygon`：`0x1007`;QPolygon
- `QMetaType::QPolygonF`：`0x1016`;QPolygonF
- `QMetaType::QQuaternion`：`0x1015`;QQuaternion
- `QMetaType::QRect`：`19`;QRect
- `QMetaType::QRectF`：`20`;QRectF
- `QMetaType::QRegion`：`0x1008`;QRegion
- `QMetaType::QRegularExpression`：`44`;QRegular表达式
- `QMetaType::QSize`：`21`;QSize
- `QMetaType::QSizeF`：`22`;QSizeF
- `QMetaType::QSizePolicy`：`0x2000`;QSizePolicy
- `QMetaType::QStringList`：`11`;QStringList
- `QMetaType::QTextFormat`：`0x100e`;QTextFormat
- `QMetaType::QTextLength`：`0x100d`;QTextLength（量子长度）
- `QMetaType::QTime`：`15`;Qtime
- `QMetaType::QTransform`：`0x1010`;QTransform
- `QMetaType::QUrl`：`17`;QUrl
- `QMetaType::QUuid`：`30`;QUuid
- `QMetaType::QVariant`：`41`;QVariant
- `QMetaType::QVariantHash`：`28`;QVariantHash
- `QMetaType::QVariantList`：`9`;QVariantList
- `QMetaType::QVariantMap`：`8`;QVariantMap
- `QMetaType::QVariantPair`：`58`;QVariantPair
- `QMetaType::QVector2D`：`0x1012`;QVector2D
- `QMetaType::QVector3D`：`0x1013`;QVector3D
- `QMetaType::QVector4D`：`0x1014`;QVector4D
- `QMetaType::User`：`65536`;用户类型的基础值
- `QMetaType::UnknownType`：`0`;这是一个无效的类型ID。对于未注册的类型，`QMetaType`返回该ID。
其他类型可以通过`qRegisterMetaType()`或调用`registerType()`注册。

### `enum QMetaType::TypeFlagflags QMetaType::TypeFlags`

**作用与语义：**

枚举描述由`QMetaType`支持的属性。
- `QMetaType::NeedsConstruction`：`0x1`;该类型有默认构造函数。如果未设置标志，实例可以安全地初始化为 memset为 0。
- `QMetaType::NeedsCopyConstruction (since Qt 6.5)`：`0x4000`;该类型有一个非平凡的复制构造器。如果未设置标志，实例可以用 memcpy 复制。
- `QMetaType::NeedsMoveConstruction (since Qt 6.5)`：`0x8000`;这种类型有一个非平凡的移动构造函数。如果没有设置标志，实例可以用 memcpy 移动。
- `QMetaType::NeedsDestruction`：`0x2`;这种类型有一个非平凡的解构器。如果没有设置该标志，丢弃对象前无需调用该解构器。
- `QMetaType::RelocatableType`：`0x4`;具有该属性的类型实例可以通过 memcpy 安全地迁移到不同的内存位置。
- `QMetaType::IsEnumeration`：`0x10`;这种类型是枚举。
- `QMetaType::IsUnsignedEnumeration`：`0x100`;如果类型是枚举，其底层类型是无符号的。
- `QMetaType::PointerToQObject`：`0x8`;该类型指向由`QObject`派生的类的指针。
- `QMetaType::IsPointer`：`0x800`;该类型指向另一种类型。
- `QMetaType::IsConst`：`0x2000`;表示此类值是不可变的;例如，因为它们是指向const对象的指针。
注意：在Qt 6.5之前，如果复制构造者或解构器中的任意一个非平凡（即类型不平凡），NeedsConstruction和NeedsDestruction标志都会被错误设置。
注意，需求标志可以被设置，但元类型可能没有相关类型的公开可访问构造器或公开可访问的解构器。
TypeFlags 类型是 QFlags 的 typedef<TypeFlag>。它存储 TypeFlag 值的 OR 组合。

### `[constexpr noexcept, since 6.0] QMetaType::QMetaType()`

**作用与语义：**

构造一个默认的、无效的QMetaType对象。

### `[explicit] QMetaType::QMetaType(int typeId)`

**作用与语义：**

构建一个包含类型`typeId`所有信息的QMetaType对象。

### `[constexpr, since 6.0] qsizetype QMetaType::alignOf() const`

**作用与语义：**

返回类型以字节为单位的对齐（即alignof（T），其中T是该`QMetaType`实例所构建的实际类型）。
该函数通常与`construct()`一起使用，用于对类型所用内存进行底层管理。

### `[static] bool QMetaType::canConvert(QMetaType fromType, QMetaType toType)`

**作用与语义：**

如果`QMetaType::convert`能从`fromType`转换到返回`toType`，返回`true`。注意，这主要关乎执行转换的能力，而实际转换尝试时可能失败（例如将浮点数转换为超出其范围的整数）。
`registerConverter()`函数可用于注册额外的转换，无论是内置类型与非内置类型之间，还是两个非内置类型之间。如果转换路径被注册，该函数将返回`true`。
Qt 支持以下转换：
- `Type`：自动投射
- `QMetaType::Bool`：`QMetaType::QChar`、`QMetaType::Double`、`QMetaType::Int`、`QMetaType::LongLong`、`QMetaType::QString`、`QMetaType::UInt`、`QMetaType::ULongLong`
- `QMetaType::QByteArray`：`QMetaType::Double`，`QMetaType::Int`，`QMetaType::LongLong`，`QMetaType::QString`，`QMetaType::UInt`，`QMetaType::ULongLong`，`QMetaType::QUuid`
- `QMetaType::QChar`：`QMetaType::Bool`、`QMetaType::Int`、`QMetaType::UInt`、`QMetaType::LongLong`、`QMetaType::ULongLong`
- `QMetaType::QColor`：`QMetaType::QString`
- `QMetaType::QDate`：`QMetaType::QDateTime`，`QMetaType::QString`
- `QMetaType::QDateTime`：`QMetaType::QDate`，`QMetaType::QString`，`QMetaType::QTime`
- `QMetaType::Double`：`QMetaType::Bool`、`QMetaType::Int`、`QMetaType::LongLong`、`QMetaType::QString`、`QMetaType::UInt`、`QMetaType::ULongLong`
- `QMetaType::QFont`：`QMetaType::QString`
- `QMetaType::Int`：`QMetaType::Bool`、`QMetaType::QChar`、`QMetaType::Double`、`QMetaType::LongLong`、`QMetaType::QString`、`QMetaType::UInt`、`QMetaType::ULongLong`
- `QMetaType::QKeySequence`：`QMetaType::Int`，`QMetaType::QString`
- `QMetaType::QVariantList`：`QMetaType::QStringList`（如果列表中的项目可以转换为QStriings）
- `QMetaType::LongLong`：`QMetaType::Bool`、`QMetaType::QByteArray`、`QMetaType::QChar`、`QMetaType::Double`、`QMetaType::Int`、`QMetaType::QString`、`QMetaType::UInt`、`QMetaType::ULongLong`
- `QMetaType::QPoint`：`QMetaType::QPointF`
- `QMetaType::QRect`：`QMetaType::QRectF`
- `QMetaType::QString`：`QMetaType::Bool`、`QMetaType::QByteArray`、`QMetaType::QChar`、`QMetaType::QColor`、`QMetaType::QDate`、`QMetaType::QDateTime`、`QMetaType::Double`、`QMetaType::QFont`、`QMetaType::Int`、`QMetaType::QKeySequence`、`QMetaType::LongLong`、`QMetaType::QStringList`、`QMetaType::QTime`、`QMetaType::UInt`、`QMetaType::ULongLong`、`QMetaType::QUuid`
- `QMetaType::QStringList`：`QMetaType::QVariantList`，`QMetaType::QString`（如果列表中恰好包含一个项目）
- `QMetaType::QTime`：`QMetaType::QString`
- `QMetaType::UInt`：`QMetaType::Bool`、`QMetaType::QChar`、`QMetaType::Double`、`QMetaType::Int`、`QMetaType::LongLong`、`QMetaType::QString`、`QMetaType::ULongLong`
- `QMetaType::ULongLong`：`QMetaType::Bool`、`QMetaType::QChar`、`QMetaType::Double`、`QMetaType::Int`、`QMetaType::LongLong`、`QMetaType::QString`、`QMetaType::UInt`
- `QMetaType::QUuid`：`QMetaType::QByteArray`，`QMetaType::QString`
其他支持的转换还包括所有原始类型（`int`、`float`、`bool`等，包括所有枚举）以及任何指针类型与`std::nullptr_t`之间的转换。枚举也可以转换为`QString`和`QByteArray`。
如果`fromType`和`toType`都是从`QObject`派生的类型（或指向它们的指针），那么如果其中一个类型是从另一个类型派生的，该函数也会返回`true`。也就是说，如果`static_cast<>`从`fromType`描述的类型到`toType`描述的类型，则该函数返回为真。`convert()`函数的操作方式类似于`qobject_cast()`，并验证`QVariant`指向对象的动态类型。
如果顺序容器的铸造，如果`toType`是`QVariantList`，该函数也会返回真。
类似地，来自关联容器的铸造也会返回该函数的 true，`toType` 为 `QVariantHash` 或 `QVariantMap`。

### `[static] bool QMetaType::canView(QMetaType fromType, QMetaType toType)`

**作用与语义：**

如果`QMetaType::view`能够在类型`fromType`上创建可变的类型`toType`视图，返回`true`。
在从`QObject`派生的类型之间转换时，如果从`fromType`描述的类型成功`qobject_cast`到`toType`描述的类型，则该函数将返回真。
你可以在任何注册给`Q_DECLARE_SEQUENTIAL_CONTAINER_METATYPE()`的容器上创建类型`QMetaSequence::Iterable`的可变视图。
同样，你可以在任何注册给`Q_DECLARE_ASSOCIATIVE_CONTAINER_METATYPE()`的容器上创建类型`QMetaAssociation::Iterable`的可变视图。

### `[since 6.0] QPartialOrdering QMetaType::compare(const void *lhs, const void *rhs) const`

**作用与语义：**

比较`lhs`和`rhs`的对象以进行排序。
如果不支持比较或数值未排序，返回`QPartialOrdering::Unordered`。否则，如果 `lhs` 小于、等价于或大于 `rhs`，则返回`QPartialOrdering::Less`、`QPartialOrdering::Equivalent` 或 `QPartialOrdering::Greater`。
两个对象都必须属于该元类型所描述的类型。如果`lhs`或`rhs` `nullptr`，则值为无序。只有当类型小于算符被元类型声明可见时，才支持比较。
如果该类型的等式算子也可见，只有当等号算符表示值相等时，值才会比较。在没有等号算子的情况下，当任一值都不小于另一方时，值被视为相等;如果等号也存在且两个这样的值不相等，则它们被视为无序，就像浮点类型的 NaN（非数字）值不在其排序之外一样。
注意：如果元类型声明中不小于 算符，即使宣告中可见的等号算符认为值相等，值仍无序：`compare() == 0` 仅在小于 算符可见时与 `equals()`一致。

### `void *QMetaType::construct(void *where, const void *copy = nullptr) const`

**作用与语义：**

在`where`寻址的现有内存中构造该`QMetaType`实例所构造的值，即`copy`的副本，返回`where`。如果`copy`为零，则该值为默认构造值。
这是一个用于显式管理存储类型内存的低级函数。如果你不需要这种级别的控制（即使用“new”而不是“placement new”），可以考虑调用`create()`。
你必须确保`where`指向可以存储新值的位置，并且`where`对齐得当。类型大小可以通过调用`sizeOf()`查询。
对齐的经验法则是，类型对齐到其自然边界，即大于类型的最大2的幂次方，除非该对齐大于平台的最大有用对齐。实际操作中，比对大于2 * sizeof（void*）的对齐仅适用于特殊硬件指令（例如，x86上的对齐SSE加载和存储）。

### `[static] bool QMetaType::convert(QMetaType fromType, const void *from, QMetaType toType, void *to)`

**作用与语义：**

将`from`的对象从`fromType`转换为预分配的空间`to`类型`toType`。如果转换成功，返回`true`，否则返回false。
`from`和`to`都必须是有效的指示。

### `void *QMetaType::create(const void *copy = nullptr) const`

**作用与语义：**

返回一份`copy`副本，前提是该 `QMetaType` 实例的类型。如果`copy` `nullptr`，则创建默认构造实例。

### `bool QMetaType::debugStream(QDebug &dbg, const void *rhs)`

**作用与语义：**

将`rhs`的对象流到调试流`dbg`。成功时返回`true`，否则返回false。

### `void QMetaType::destroy(void *data) const`

**作用与语义：**

如果`data`是本`QMetaType`实例创建时所用的类型，则销毁该。

### `void QMetaType::destruct(void *data) const`

**作用与语义：**

假设该值属于该实例构造所用的类型，则会摧毁位于`data`的值`QMetaType`。
与`destroy()`不同，这个函数只调用该类型的解构函数，不调用删除操作符。

### `[since 6.0] bool QMetaType::equals(const void *lhs, const void *rhs) const`

**作用与语义：**

比较`lhs`和`rhs`的物体以求相等。
两个对象必须属于该元类型描述的类型。只有当元类型声明中可见该类型的小于或等号算子时，才能比较两个对象。否则，元类型永远不会将值视为相等。当元类型声明可见等号算子时，它是权威的;否则，如果小于 且任一值都不小于另一方，则两者视为相等。如果值无序（详见 `compare()`），则两者不相等。
如果两个对象相等，则返回真，否则为真。

### `[constexpr] QMetaType::TypeFlags QMetaType::flags() const`

**作用与语义：**

返回该`QMetaType`实例构建时所依赖类型的标志。要检查特定类型特征，建议使用“is-”函数而非直接使用标志。

### `[static] QMetaType QMetaType::fromName(QByteArrayView typeName)`

**作用与语义：**

返回一个`QMetaType`匹配的`typeName`。如果类型名（typeName）`QMetaType`不知道，返回对象无效。

### `[static constexpr] template <typename T> QMetaType QMetaType::fromType()`

**作用与语义：**

返回模板参数中对应类型的`QMetaType`。

### `[static] bool QMetaType::hasRegisteredConverterFunction(QMetaType fromType, QMetaType toType)`

**作用与语义：**

如果元类型系统注册了从元类型ID `fromType`转换为`toType`，返回`true`。

### `[static] template <typename From, typename To> bool QMetaType::hasRegisteredConverterFunction()`

**作用与语义：**

如果元类型系统有从类型 From 到 To 类型的注册转换，返回`true`。

### `[since 6.1] bool QMetaType::hasRegisteredDataStreamOperators() const`

**作用与语义：**

如果元类型系统为该元类型注册了数据流操作符，返回`true`。

### `[since 6.0] bool QMetaType::hasRegisteredDebugStreamOperator() const`

**作用与语义：**

如果元类型系统有该元类型注册的调试流操作符，则返回`true`。

### `[static] bool QMetaType::hasRegisteredMutableViewFunction(QMetaType fromType, QMetaType toType)`

**作用与语义：**

如果元类型系统对元类型ID有一个注册的可变视图，则返回`true`，`fromType`元类型ID为`toType`。

### `[static, since 6.0] template <typename From, typename To> bool QMetaType::hasRegisteredMutableViewFunction()`

**作用与语义：**

如果元类型系统对类型 From 类型有注册的可变视图，则返回`true`。

### `int QMetaType::id() const`

**作用与语义：**

返回该`QMetaType`实例所持有的 id 类型。

### `[noexcept, since 6.5] bool QMetaType::isCopyConstructible() const`

**作用与语义：**

如果该类型可以被复制构造，则返回为真。如果可以，则`construct()`和`create()`可以与非空的`copy`参数一起使用。

### `[noexcept, since 6.5] bool QMetaType::isDefaultConstructible() const`

**作用与语义：**

如果该类型可以被默认构造，则返回真。如果可以，则`construct()`和`create()`可以与空参数的`copy`一起使用。

### `[noexcept, since 6.5] bool QMetaType::isDestructible() const`

**作用与语义：**

如果该类型可以被销毁，则返回为真。如果可以，则可以调用`destroy()`和 `destruct()`。

### `bool QMetaType::isEqualityComparable() const`

**作用与语义：**

如果元类型描述的类型有小于或等号的算子在元类型声明中可见，返回`true`，否则`false`。

### `[noexcept, since 6.5] bool QMetaType::isMoveConstructible() const`

**作用与语义：**

如果该类型可以通过移动构造，则返回 true。`QMetaType`目前没有 API 来利用该特性。

### `bool QMetaType::isOrdered() const`

**作用与语义：**

如果元类型描述的类型小于算子对元类型声明可见，则返回`true`，否则`false`。

### `[noexcept] bool QMetaType::isRegistered() const`

**作用与语义：**

如果该`QMetaType`对象已注册于 Qt 全局元类型注册表，则返回`true`。注册允许通过类型名称（使用`QMetaType::fromName()`）或通过其 ID（使用构造函数）来查找类型。

### `[static] bool QMetaType::isRegistered(int type)`

**作用与语义：**

如果注册了编号为`type`的数据类型，返回`true`;否则返回`false`。

### `[constexpr noexcept] bool QMetaType::isValid() const`

**作用与语义：**

如果该`QMetaType`对象包含关于某一类型的有效信息，则返回`true`，否则返回为假。

### `bool QMetaType::load(QDataStream &stream, void *data) const`

**作用与语义：**

将该类型的对象从给定`stream`读取到`data`。如果对象成功加载，返回`true`;否则返回`false`。
通常情况下，你不需要直接调用这个函数。相反，可以使用`QVariant`的`operator>>()`，它依赖于 load() 来流式自定义类型。

### `[constexpr] const QMetaObject *QMetaType::metaObject() const`

**作用与语义：**

返回相对于该类型的`QMetaObject`。
如果类型是指向`QObject`子类的指针类型，`flags()`包含`QMetaType::PointerToQObject`，该函数返回相应的`QMetaObject`。这可以与`QMetaObject::newInstance()`结合使用，生成该类型的QObject。
如果类型是`Q_GADGET`，`flags()`包含`QMetaType::IsGadget`。如果类型是指向`Q_GADGET`的指针，`flags()`包含`QMetaType::PointerToGadget`。在这两种情况下，该函数都会返回其`QMetaObject`。这可以用来检索`QMetaMethod`和`QMetaProperty`，并用于此类指针，例如，如 `QVariant::data()` 所示。
如果类型是枚举，`flags()`包含`QMetaType::IsEnumeration`。在这种情况下，如果枚举被注册为`Q_ENUM`，该函数返回包围对象的 `QMetaObject`，否则`nullptr`。

### `[constexpr] const char *QMetaType::name() const`

**作用与语义：**

返回与该`QMetaType`关联的类型名称，若未找到匹配类型则返回空指针。返回的指针不得被删除。

### `[static] template <typename From, typename To> bool QMetaType::registerConverter()`

**作用与语义：**

登记元类型系统中从类型 From 隐式转换为类型 To 的可能性。如果注册成功，返回 `true`，否则返回 false。

**官方示例：**

```cpp
 class Counter {
   int number = 0;
 public:
   int value() const { return number; }
   operator int() const { return value(); }
   void increment() {++number;}
 };
 QMetaType::registerConverter<Counter, int>();
```

### `[static] template <typename From, typename To> bool QMetaType::registerConverter(To (From::*)() const function)`

**作用与语义：**

寄存方法`function`如 To From：：function() const 作为类型转换器，从 类型从 From 到 类型 To 。如果注册成功，返回 `true`，否则返回 false。

**官方示例：**

```cpp
 struct Coordinates {
   int x;
   int y;
   int z;

   QString toString() const { return u"[x: %1; y: %2, z: %3]"_s.arg(QString::number(x),
     QString::number(y),
     QString::number(z)); }
 };
 QMetaType::registerConverter<Coordinates, QString>(&Coordinates::toString);
```

### `[static] template <typename From, typename To> bool QMetaType::registerConverter(To (From::*)(bool *) const function)`

**作用与语义：**

在元类型系统中，寄存一个`function`方法，类似于 To From：：function（bool *ok） const 作为从 From 类型到类型 To 的转换器。如果注册成功，返回 `true`，否则返回 false。
函数可以使用`ok`指针来表示转换是否成功。

**官方示例：**

```cpp
 struct BigNumber {
     long long l;

     int toInt(bool *ok = nullptr) const {
       const bool canConvertSafely = l < std::numeric_limits<int>::max();
       if (ok)
         *ok = canConvertSafely;
       return l;
     }
 };
 QMetaType::registerConverter<BigNumber, int>(&BigNumber::toInt);
```

### `[static] template < typename From, typename To, typename UnaryFunction > bool QMetaType::registerConverter(UnaryFunction function)`

**作用与语义：**

在元类型系统中，将一元函数对象`function`作为从 From 类型到类型 To 的转换器注册。如果注册成功，则返回`true`，否则返回 false。
`function`必须接受类型为`From`的实例并返回`To`的实例。它可以是函数指针、λ或函子对象。自Qt 6.5起，`function`还可以返回`std::optional<To>`实例，以表示转换失败。

**官方示例：**

```cpp
 QMetaType::registerConverter<CustomStringType, QString>([](const CustomStringType &str) {
     return QString::fromUtf8(str.data());
 });
 QMetaType::registerConverter<QJsonValue, CustomPointType>(
           [](const QJsonValue &value) -> std::optional<CustomPointType> {
     const auto object = value.toObject();
     if (!object.contains("x") || !object.contains("y"))
         return std::nullopt;  // The conversion fails if the required properties are missing
     return CustomPointType{object["x"].toDouble(), object["y"].toDouble()};
 });
```

### `[static, since 6.0] template <typename From, typename To> bool QMetaType::registerMutableView(To (From::*)() function)`

**作用与语义：**

在元类型系统中，寄存一个方法`function`类似`To From::function()`，作为类型 `To` 在类型 `From` 上的可变视图。如果注册成功，返回 `true`，否则返回`false`。

### `[static, since 6.0] template < typename From, typename To, typename UnaryFunction > bool QMetaType::registerMutableView(UnaryFunction function)`

**作用与语义：**

在元类型系统中，将一元函数对象`function`为类型 To 的可变视图 To 注册。如果注册成功，返回 `true`，否则返回 `false`。

### `[since 6.5] void QMetaType::registerType() const`

**作用与语义：**

将此`QMetaType`注册表注册为类型注册表，以便通过名称查找，使用`QMetaType::fromName()`。

### `bool QMetaType::save(QDataStream &stream, const void *data) const`

**作用与语义：**

将`data`指向的对象写入给定的`stream`。如果目标成功保存，返回`true`;否则返回`false`。
通常，你不需要直接调用这个函数。相反，可以使用`QVariant`的`operator<<()`，它依赖于save()来流式自定义类型。

### `[constexpr] qsizetype QMetaType::sizeOf() const`

**作用与语义：**

返回类型大小（字节单位）（即 sizeof（T），其中 T 是该`QMetaType`实例所构建的实际类型）。
该函数通常与`construct()`一起使用，用于对类型所用内存进行底层管理。

### `[since 6.6] QMetaType QMetaType::underlyingType() const`

**作用与语义：**

如果该元类型代表枚举，该方法返回的元类型是符号性和大小与枚举底层类型相同的数值类。如果代表`QFlags`类型，返回`QMetaType::Int`。在其他所有情况下，返回无效的`QMetaType`。

### `[static, since 6.0] bool QMetaType::view(QMetaType fromType, void *from, QMetaType toType, void *to)`

**作用与语义：**

在预分配空间中`fromType` `from` 的对象创建可变视图`to`类型`toType`。转换成功时返回`true`，否则返回 false。

### `[since 6.4] size_t qHash(QMetaType key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr] template <typename T> int qMetaTypeId()`

**作用与语义：**

在编译时返回类型`T`的元类型ID。如果类型未用`Q_DECLARE_METATYPE()`声明，编译将失败。
典型用法：
QMetaType：：type() 返回与 qMetaTypeId() 相同的 ID，但在运行时根据类型名称进行查找。QMetaType：：type() 稍慢，但如果未注册类型，编译会成功。

**官方示例：**

```cpp
 int id = qMetaTypeId<QString>();    // id is now QMetaType::QString
 id = qMetaTypeId<MyStruct>();       // compile error if MyStruct not declared
```

### `[constexpr] template <typename T> int qRegisterMetaType()`

**作用与语义：**

调用此函数以注册类型 `T`。返回元类型 ID。此函数要求在调用时 `T` 是完全定义的类型。对于指针类型，还要求被指向的类型是完全定义的。使用 `Q_DECLARE_OPAQUE_POINTER()` 可以注册向前声明类型的指针。要在 `QMetaType`、`QVariant` 或 `QObject::property()` API 中使用 `T` 类型，无需注册。要在排队信号与槽连接中使用 `T` 类型，必须在第一次建立连接之前调用 `qRegisterMetaType<T>()`。通常在使用 `T` 的类的构造函数中完成，或在 `main()` 函数中完成。一旦类型注册完成，可以使用 `QMetaType::fromName()` 通过名称找到它。

**官方示例：**

```cpp
 int id = qRegisterMetaType<MyStruct>();
```

### `[since 6.5] int qRegisterMetaType(QMetaType meta)`

**作用与语义：**

注册元类型 `meta`，并返回其类型 Id。
该函数要求调用点的  是完全定义的类型`T`。对于指针类型，也要求指向的类型是完全定义的。使用 `Q_DECLARE_OPAQUE_POINTER()` 来注册指向前发声明的类型。
在`QMetaType`、`QVariant`或`QObject::property()` API中使用类型`T`，无需注册。
要在队列信号和槽函数连接中使用类型`T`，必须在建立第一个连接前调用`qRegisterMetaType<T>()`。这通常在使用 `T` 的类的构造函数中完成，或在 `main()` 函数中完成。
类型注册后，可以通过`QMetaType::fromName()`的名称查找。

### `[noexcept] bool operator!=(const QMetaType &lhs, const QMetaType &rhs)`

**作用与语义：**

如果 `QMetaType` `lhs` 表示的类型与 `QMetaType` `rhs` 不同，则返回 `QMetaType` `rhs`，否则返回 `false`。

### `[since 6.5] QDebug operator<<(QDebug d, QMetaType m)`

**作用与语义：**

将`QMetaType` `m`写入流`d`，并返回流。

### `[noexcept] bool operator==(const QMetaType &lhs, const QMetaType &rhs)`

**作用与语义：**

如果 `QMetaType` `lhs` 表示与 `QMetaType` `rhs` 相同的类型，则返回 `rhs`，否则返回 `false`。

### `Q_DECLARE_ASSOCIATIVE_CONTAINER_METATYPE(Container)`

**作用与语义：**

该宏使容器`Container` `QMetaType`为关联容器。这使得如果 T 和 U 本身已知`QMetaType`，就可以将 Container<T， U> 实例放入`QVariant`。
注意所有 Qt 关联容器本身就内置支持，因此不必使用该宏。std：：map 容器也内置支持。
这个例子展示了Q_DECLARE_ASSOCIATIVE_CONTAINER_METATYPE()的典型用法：

**官方示例：**

```cpp
 #include <unordered_map>

 Q_DECLARE_ASSOCIATIVE_CONTAINER_METATYPE(std::unordered_map)

 void someFunction()
 {
     std::unordered_map<int, bool> container;
     QVariant var = QVariant::fromValue(container);
     // ...
 }
```

### `Q_DECLARE_METATYPE(Type)`

**作用与语义：**

只要该宏提供公共默认构造函数、公共复制构造器和公共结构化器，该类型`Type` `QMetaType`已知。在 `QVariant` 中使用类型 `Type` 作为自定义类型是必要的。
该宏要求`Type`在其使用点是完全定义的类型。对于指针类型，还要求指向的类型必须被完全定义。与`Q_DECLARE_OPAQUE_POINTER()`结合使用，用于注册指向转发声明的类型。
理想情况下，这个宏应放在类或结构体声明的下方。如果无法做到，可以将其放入私有首文件中，每次在`QVariant`中使用该类型时都必须包含该文件。
添加 Q_DECLARE_METATYPE() 后，所有基于模板的函数（包括 `QVariant`）都能知道该类型。注意，如果你打算在队列中的信号和槽函数连接或 `QObject` 的属性系统中使用该类型，也必须调用 `qRegisterMetaType()`，因为这些名称在运行时已解析。
此示例展示了Q_DECLARE_METATYPE()的典型用例：
如果`MyStruct`位于命名空间中，Q_DECLARE_METATYPE()宏必须位于命名空间之外：
由于`MyStruct`现已被`QMetaType`知晓，它可以用于`QVariant`：
有些类型会自动注册，不需要这个宏：
- 指向由`QObject`派生的类的指针
- `QList`<T>、`QQueue`<T>、`QStack`<T>或`QSet`，<T>其中T为注册元类型
- `QHash`<T1、T2>、`QMap`<T1、T2>或std：:p air<T1、T2>其中T1和T2为注册元类型
- `QPointer`<T>、`QSharedPointer`<T>、`QWeakPointer`<T>，其中 T 是从 `QObject` 衍生的类
- 登记在`Q_ENUM`或`Q_FLAG`的列举
- 具有`Q_GADGET`宏的类
注意：如果流和调试操作符在注册时可见，该方法也会注册。由于在某些地方会自动完成，强烈建议在类型本身之后直接声明流操作符。由于C的参数相关查找规则，也强烈建议在与类型相同命名空间中声明操作符。
流操作符应具备以下签名：

**官方示例：**

```cpp
 struct MyStruct
 {
     int i;
     //...
 };

 Q_DECLARE_METATYPE(MyStruct)
```

### `Q_DECLARE_OPAQUE_POINTER(PointerType)`

**作用与语义：**

该宏允许通过`Q_DECLARE_METATYPE()`或`qRegisterMetaType()`向`QMetaType`注册指向前向声明类型（`PointerType`）的指针。
不要用该宏来避免MOC对不完整属性类型提出的投诉或错误，尤其是在该pointee类型被用作程序其他上下文的完全类型时。当类型的完整定义可用，但你更倾向于在头部使用前向声明以减少编译时间时，应使用`Q_MOC_INCLUDE`。
警告：不要使用带有指向`Q_OBJECT`或小工具类的指针的 Q_DECLARE_OPAQUE_POINTERT的 S ，因为这可能导致元类型系统中的信息不一致。

### `Q_DECLARE_SEQUENTIAL_CONTAINER_METATYPE(Container)`

**作用与语义：**

该宏使容器`Container` `QMetaType`为顺序容器。<T>这使得如果 T 本身已知`QMetaType`，可以将容器实例放入`QVariant`。
注意，所有 Qt 顺序容器都已内置支持，且不必使用该宏。std：：vector 和 std：：list 容器也内置支持。
这个例子展示了Q_DECLARE_SEQUENTIAL_CONTAINER_METATYPE()的典型用法：

**官方示例：**

```cpp
 #include <deque>

 Q_DECLARE_SEQUENTIAL_CONTAINER_METATYPE(std::deque)

 void someFunc()
 {
     std::deque<QFile*> container;
     QVariant var = QVariant::fromValue(container);
     // ...
 }
```

### `Q_DECLARE_SMART_POINTER_METATYPE(SmartPointer)`

**作用与语义：**

该宏使得智能指针`SmartPointer`被`QMetaType`为智能指针。这使得如果 T 是一个继承 `QObject` 的类型，就可以将 SmartPointer<T> 实例放入`QVariant`中。
请注意，`QWeakPointer`、`QSharedPointer`和`QPointer`已经内置支持，因此不必使用该宏。
此示例展示了Q_DECLARE_SMART_POINTER_METATYPE()的典型用法：

**官方示例：**

```cpp
 #include <memory>

 Q_DECLARE_SMART_POINTER_METATYPE(std::shared_ptr)

 void someMethod()
 {
     auto smart_ptr = std::make_shared<QFile>();
     QVariant var = QVariant::fromValue(smart_ptr);
     // ...
     if (var.canConvert<QObject*>()) {
         QObject *sp = var.value<QObject*>();
         qDebug() << sp->metaObject()->className(); // Prints 'QFile'.
     }
 }
```

### `enum TypeFlag { NeedsConstruction, NeedsCopyConstruction, NeedsMoveConstruction, NeedsDestruction, RelocatableType, …, IsConst }`

**作用与语义：**

枚举描述由`QMetaType`支持的属性。
- `QMetaType::NeedsConstruction`：`0x1`;该类型有默认构造函数。如果未设置标志，实例可以安全地初始化为 memset为 0。
- `QMetaType::NeedsCopyConstruction (since Qt 6.5)`：`0x4000`;该类型有一个非平凡的复制构造器。如果未设置标志，实例可以用 memcpy 复制。
- `QMetaType::NeedsMoveConstruction (since Qt 6.5)`：`0x8000`;这种类型有一个非平凡的移动构造函数。如果没有设置标志，实例可以用 memcpy 移动。
- `QMetaType::NeedsDestruction`：`0x2`;这种类型有一个非平凡的解构器。如果没有设置该标志，丢弃对象前无需调用该解构器。
- `QMetaType::RelocatableType`：`0x4`;具有该属性的类型实例可以通过 memcpy 安全地迁移到不同的内存位置。
- `QMetaType::IsEnumeration`：`0x10`;这种类型是枚举。
- `QMetaType::IsUnsignedEnumeration`：`0x100`;如果类型是枚举，其底层类型是无符号的。
- `QMetaType::PointerToQObject`：`0x8`;该类型指向由`QObject`派生的类的指针。
- `QMetaType::IsPointer`：`0x800`;该类型指向另一种类型。
- `QMetaType::IsConst`：`0x2000`;表示此类值是不可变的;例如，因为它们是指向const对象的指针。
注意：在Qt 6.5之前，如果复制构造者或解构器中的任意一个非平凡（即类型不平凡），NeedsConstruction和NeedsDestruction标志都会被错误设置。
注意，需求标志可以被设置，但元类型可能没有相关类型的公开可访问构造器或公开可访问的解构器。
TypeFlags 类型是 QFlags 的 typedef<TypeFlag>。它存储 TypeFlag 值的 OR 组合。

### `flags TypeFlags`

**作用与语义：**

枚举描述由`QMetaType`支持的属性。
- `QMetaType::NeedsConstruction`：`0x1`;该类型有默认构造函数。如果未设置标志，实例可以安全地初始化为 memset为 0。
- `QMetaType::NeedsCopyConstruction (since Qt 6.5)`：`0x4000`;该类型有一个非平凡的复制构造器。如果未设置标志，实例可以用 memcpy 复制。
- `QMetaType::NeedsMoveConstruction (since Qt 6.5)`：`0x8000`;这种类型有一个非平凡的移动构造函数。如果没有设置标志，实例可以用 memcpy 移动。
- `QMetaType::NeedsDestruction`：`0x2`;这种类型有一个非平凡的解构器。如果没有设置该标志，丢弃对象前无需调用该解构器。
- `QMetaType::RelocatableType`：`0x4`;具有该属性的类型实例可以通过 memcpy 安全地迁移到不同的内存位置。
- `QMetaType::IsEnumeration`：`0x10`;这种类型是枚举。
- `QMetaType::IsUnsignedEnumeration`：`0x100`;如果类型是枚举，其底层类型是无符号的。
- `QMetaType::PointerToQObject`：`0x8`;该类型指向由`QObject`派生的类的指针。
- `QMetaType::IsPointer`：`0x800`;该类型指向另一种类型。
- `QMetaType::IsConst`：`0x2000`;表示此类值是不可变的;例如，因为它们是指向const对象的指针。
注意：在Qt 6.5之前，如果复制构造者或解构器中的任意一个非平凡（即类型不平凡），NeedsConstruction和NeedsDestruction标志都会被错误设置。
注意，需求标志可以被设置，但元类型可能没有相关类型的公开可访问构造器或公开可访问的解构器。
TypeFlags 类型是 QFlags 的 typedef<TypeFlag>。它存储 TypeFlag 值的 OR 组合。

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

`QMetaType` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
