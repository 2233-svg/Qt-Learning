# QVariant

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QVariant` 是带运行时类型信息的通用值容器，可保存已注册到 Qt 元类型系统的值，并在模型、属性、数据库和动态接口之间传递。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QVariant` 是带运行时类型信息的通用值容器，可保存已注册到 Qt 元类型系统的值，并在模型、属性、数据库和动态接口之间传递。

**内部模型：** QVariant 同时保存值和 QMetaType。`isValid()` 表示是否持有类型，`isNull()` 表示所持值是否为空，两者不是一回事。`value<T>()` 适合读取已知类型，`canConvert<T>()`/`convert()` 用于受支持的转换；转换成功仍不代表业务语义有效。

**适用场景：** 接口必须容纳多种类型、模型角色返回值、QObject 动态属性和 SQL 字段时使用；编译期类型固定的业务结构优先使用明确类型或结构体。

**典型调用链：** fromValue/构造保存值 -> metaType/typeName 检查 -> canConvert 判断 -> value/toXxx 读取 -> 检查空值和转换结果。

**先记住的坑：** 不要用 QVariant 掩盖本可静态检查的类型；区分 invalid 和 null；自定义类型先满足 QMetaType 要求；不要假定 `toInt()` 返回 0 就是转换成功，应读取 ok。

## 2. 依赖与对象关系

- 头文件：`#include <QVariant>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

QVariant 同时保存值和 QMetaType。`isValid()` 表示是否持有类型，`isNull()` 表示所持值是否为空，两者不是一回事。`value<T>()` 适合读取已知类型，`canConvert<T>()`/`convert()` 用于受支持的转换；转换成功仍不代表业务语义有效。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

接口必须容纳多种类型、模型角色返回值、QObject 动态属性和 SQL 字段时使用；编译期类型固定的业务结构优先使用明确类型或结构体。 使用时通常按这个过程组织：fromValue/构造保存值 -> metaType/typeName 检查 -> canConvert 判断 -> value/toXxx 读取 -> 检查空值和转换结果。

```cpp
#include <QVariant>

QVariant value = 42;
bool ok = false;
const int number = value.toInt(&ok);
if (ok && value.metaType() == QMetaType::fromType<int>()) {
    // number 可以按整数语义使用
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `(since 6.11) class ConstPointer`
- `(since 6.11) class ConstReference`
- `(since 6.11) class Pointer`
- `(since 6.11) class Reference`

### 公有函数

- `QVariant()`
- `QVariant(QChar c)`
- `QVariant(const char *val)`
- `QVariant(double val)`
- `QVariant(float val)`
- `QVariant(int val)`
- `QVariant(qlonglong val)`
- `QVariant(qulonglong val)`
- `QVariant(uint val)`
- `QVariant(QMetaType type, const void *copy = nullptr)`
- `(since 6.6) QVariant(std::in_place_type_t<T>, Args &&... args)`
- `(since 6.6) QVariant(std::in_place_type_t<T>, std::initializer_list<U> il, Args &&... args)`
- `QVariant(QDate val)`
- `QVariant(QLatin1StringView val)`
- `QVariant(QLine val)`
- `QVariant(QLineF val)`
- `QVariant(QPoint val)`
- `QVariant(QPointF val)`
- `QVariant(QRect val)`
- `QVariant(QRectF val)`
- `QVariant(QSize val)`
- `QVariant(QSizeF val)`
- `QVariant(QTime val)`
- `QVariant(QUuid val)`
- `QVariant(bool val)`
- `QVariant(const QBitArray &val)`
- `QVariant(const QByteArray &val)`
- `QVariant(const QDateTime &val)`
- `QVariant(const QEasingCurve &val)`
- `QVariant(const QHash<QString, QVariant> &val)`
- `QVariant(const QJsonArray &val)`
- `QVariant(const QJsonDocument &val)`
- `QVariant(const QJsonObject &val)`
- `QVariant(const QJsonValue &val)`
- `QVariant(const QList<QVariant> &val)`
- `QVariant(const QLocale &l)`
- `QVariant(const QMap<QString, QVariant> &val)`
- `QVariant(const QModelIndex &val)`
- `QVariant(const QPersistentModelIndex &val)`
- `QVariant(const QRegularExpression &re)`
- `QVariant(const QString &val)`
- `QVariant(const QStringList &val)`
- `QVariant(const QUrl &val)`
- `QVariant(const QVariant &p)`
- `QVariant(QVariant &&other)`
- `~QVariant()`
- `bool canConvert() const`
- `(since 6.0) bool canConvert(QMetaType type) const`
- `bool canView() const`
- `void clear()`
- `const void * constData() const`
- `(since 6.0) bool convert(QMetaType targetType)`
- `void * data()`
- `const void * data() const`
- `(since 6.6) T & emplace(Args &&... args)`
- `(since 6.6) T & emplace(std::initializer_list<U> list, Args &&... args)`
- `bool isNull() const`
- `bool isValid() const`
- `(since 6.0) QMetaType metaType() const`
- `void setValue(QVariant &&value)`
- `void setValue(T &&value)`
- `void setValue(const QVariant &value)`
- `void swap(QVariant &other)`
- `QBitArray toBitArray() const`
- `bool toBool() const`
- `QByteArray toByteArray() const`
- `QChar toChar() const`
- `QDate toDate() const`
- `QDateTime toDateTime() const`
- `double toDouble(bool *ok = nullptr) const`
- `QEasingCurve toEasingCurve() const`
- `float toFloat(bool *ok = nullptr) const`
- `QHash<QString, QVariant> toHash() const`
- `int toInt(bool *ok = nullptr) const`
- `QJsonArray toJsonArray() const`
- `QJsonDocument toJsonDocument() const`
- `QJsonObject toJsonObject() const`
- `QJsonValue toJsonValue() const`
- `QLine toLine() const`
- `QLineF toLineF() const`
- `QList<QVariant> toList() const`
- `QLocale toLocale() const`
- `qlonglong toLongLong(bool *ok = nullptr) const`
- `QMap<QString, QVariant> toMap() const`
- `QModelIndex toModelIndex() const`
- `QPersistentModelIndex toPersistentModelIndex() const`
- `QPoint toPoint() const`
- `QPointF toPointF() const`
- `qreal toReal(bool *ok = nullptr) const`
- `QRect toRect() const`
- `QRectF toRectF() const`
- `QRegularExpression toRegularExpression() const`
- `QSize toSize() const`
- `QSizeF toSizeF() const`
- `QString toString() const`
- `QStringList toStringList() const`
- `QTime toTime() const`
- `uint toUInt(bool *ok = nullptr) const`
- `qulonglong toULongLong(bool *ok = nullptr) const`
- `QUrl toUrl() const`
- `QUuid toUuid() const`
- `int typeId() const`
- `const char * typeName() const`
- `int userType() const`
- `T value() const &`
- `T view()`
- `QVariant & operator=(QVariant &&other)`
- `QVariant & operator=(const QVariant &variant)`

### 静态公有成员

- `(since 6.0) QPartialOrdering compare(const QVariant &lhs, const QVariant &rhs)`
- `(since 6.7) QVariant fromMetaType(QMetaType type, const void *copy = nullptr)`
- `QVariant fromStdVariant(const std::variant<Types...> &value)`
- `(since 6.6) QVariant fromStdVariant(std::variant<Types...> &&value)`
- `QVariant fromValue(const T &value)`
- `(since 6.6) QVariant fromValue(T &&value)`

### 相关非成员函数

- `QVariantHash`
- `QVariantList`
- `QVariantMap`
- `(since 6.6) T & get(QVariant &v)`
- `(since 6.6) T && get(QVariant &&v)`
- `(since 6.6) const T & get(const QVariant &v)`
- `(since 6.6) const T && get(const QVariant &&v)`
- `(since 6.6) T * get_if(QVariant *v)`
- `(since 6.6) const T * get_if(const QVariant *v)`
- `T qvariant_cast(const QVariant &value)`
- `(since 6.7) T qvariant_cast(QVariant &&value)`
- `bool operator!=(const QVariant &lhs, const QVariant &rhs)`
- `QDataStream & operator<<(QDataStream &s, const QVariant &p)`
- `bool operator==(const QVariant &lhs, const QVariant &rhs)`
- `QDataStream & operator>>(QDataStream &s, QVariant &p)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[noexcept] QVariant::QVariant()`

**作用与语义：**

构造一个无效的变体。

### `[noexcept] QVariant::QVariant(QChar c)`

**作用与语义：**

构造一个带有字符值的新变体，`c`。

### `QVariant::QVariant(const char *val)`

**作用与语义：**

构造字符串值为`val`的新变体。该变体将`val`创建到一个`QString`中，假设输入`val`采用UTF-8编码。
注意，`val` 在变体中被转换为存储的 `QString`，`QVariant::userType()` 会返回变体中的 `QMetaType::QString`。
你可以通过编译应用程序时定义`QT_NO_CAST_FROM_ASCII`来禁用这个操作符。

### `[noexcept] QVariant::QVariant(double val)`

**作用与语义：**

构造一个浮点值`val`的新变体。

### `[noexcept] QVariant::QVariant(float val)`

**作用与语义：**

构造一个浮点值`val`的新变体。

### `[noexcept] QVariant::QVariant(int val)`

**作用与语义：**

构造一个整数值的新变体，`val`。

### `[noexcept] QVariant::QVariant(qlonglong val)`

**作用与语义：**

构造一个长长整数值的新变体，`val`。

### `[noexcept] QVariant::QVariant(qulonglong val)`

**作用与语义：**

构造一个带有无符号长整数值的新变体，`val`。

### `[noexcept] QVariant::QVariant(uint val)`

**作用与语义：**

构造一个无符号整数值的新变体，`val`。

### `[explicit] QVariant::QVariant(QMetaType type, const void *copy = nullptr)`

**作用与语义：**

构造类型为`type`的变体，如果`copy`不是`nullptr`，则用`*copy`的副本初始化（此时`copy`必须指向类型`type`的对象）。
注意你必须传递你想存储对象的地址。
通常，你不必使用这个构造函数，而是用`QVariant::fromValue()`来构造由`QMetaType::VoidStar`表示的指针类型和`QMetaType::QObjectStar`的变体。
如果`type`不支持复制构造且`copy`不`nullptr`，变体无效。同样，如果`copy` `nullptr`且`type`不支持默认构造，变体无效。

### `[explicit noexcept(...), since 6.6] template < typename T, typename... Args, QVariant::if_constructible<T, Args...> = true > QVariant::QVariant(std::in_place_type_t<T>, Args &&... args)`

**作用与语义：**

构造一个包含类型为`T`值的新变体。所包含的值以参数`std::forward<Args>(args)...`初始化。
该构造器支持 STL/std：：任何兼容性。
只有当`T`能从`args`构造时，才参与重载决议。
注意：该功能仅在`is_noexcept_constructible<q20::remove_cvref_t<T>, Args...>::value` `true`时才适用。

### `[explicit noexcept(...), since 6.6] template < typename T, typename U, typename... Args, QVariant::if_constructible<T, std::initializer_list<U> &, Args...> = true > QVariant::QVariant(std::in_place_type_t<T>, std::initializer_list<U> il, Args &&... args)`

**作用与语义：**

此重载存在是为了支持构造函数接受 `initializer_list` 的类型。它的行为与非初始化列表 `in_place_type_t` 重载基本相同。
注意：当 `is_noexcept_constructible<q20::remove_cvref_t<T>, std::initializer_list<U> &, Args...>::value` is `true` 时，此函数为 noexcept。

### `[noexcept] QVariant::QVariant(QDate val)`

**作用与语义：**

构造一个带有日期值`val`的新变体。

### `QVariant::QVariant(QLatin1StringView val)`

**作用与语义：**

构造了一个带有`QString`值的新变体，取自`val`所见的拉丁-1字符串。

### `[noexcept(...)] QVariant::QVariant(QLine val)`

**作用与语义：**

构造一个线值为`val`的新变体。
注意：该功能仅在`Private::FitsInInternalSize<sizeof(int) * 4>`为`true`时使用。

### `[noexcept(...)] QVariant::QVariant(QLineF val)`

**作用与语义：**

构造一个线值为`val`的新变体。
注意：该功能仅在`Private::FitsInInternalSize<sizeof(qreal) * 4>` 为`true`时使用。

### `[noexcept] QVariant::QVariant(QPoint val)`

**作用与语义：**

构造一个点数值为`val`的新变体。

### `[noexcept(...)] QVariant::QVariant(QPointF val)`

**作用与语义：**

构造一个点数值为`val`的新变体。
注意：该功能仅在`Private::FitsInInternalSize<sizeof(qreal) * 2>` `true`时使用。

### `[noexcept(...)] QVariant::QVariant(QRect val)`

**作用与语义：**

构造一个矩阵值为`val`的新变体。
注意：该功能仅在`Private::FitsInInternalSize<sizeof(int) * 4>` `true`时使用。

### `[noexcept(...)] QVariant::QVariant(QRectF val)`

**作用与语义：**

构造一个矩形值为`val`的新变体。
注意：该功能仅在`Private::FitsInInternalSize<sizeof(qreal) * 4>` 被`true`时使用。

### `[noexcept] QVariant::QVariant(QSize val)`

**作用与语义：**

构造一个尺寸值为`val`的新变体。

### `[noexcept(...)] QVariant::QVariant(QSizeF val)`

**作用与语义：**

构造一个尺寸值为`val`的新变体。
注意：该函数仅在`Private::FitsInInternalSize<sizeof(qreal) * 2>`为`true`时使用。

### `[noexcept] QVariant::QVariant(QTime val)`

**作用与语义：**

构造一个带有时间值`val`的新变体。

### `[noexcept(...)] QVariant::QVariant(QUuid val)`

**作用与语义：**

构造一个带有uuid值`val`的新变体。
注意：该函数仅在`Private::FitsInInternalSize<16>` `true`时使用。

### `[noexcept] QVariant::QVariant(bool val)`

**作用与语义：**

构造一个布尔值`val`的新变体。

### `[noexcept] QVariant::QVariant(const QBitArray &val)`

**作用与语义：**

构造一个带有位数组值`val`的新变体。

### `[noexcept] QVariant::QVariant(const QByteArray &val)`

**作用与语义：**

构造一个具有比特雷射线值的新变异体，`val`。

### `[noexcept] QVariant::QVariant(const QDateTime &val)`

**作用与语义：**

构造一个带有日期/时间值的新变体，`val`。

### `QVariant::QVariant(const QEasingCurve &val)`

**作用与语义：**

构造一个带有宽松曲线值的新变体，`val`。

### `[noexcept] QVariant::QVariant(const QHash<QString, QVariant> &val)`

**作用与语义：**

构造了一个新的变体，哈希为`QVariant`s，`val`。

### `[noexcept] QVariant::QVariant(const QJsonArray &val)`

**作用与语义：**

构造一个带有json数组值`val`的新变体。

### `QVariant::QVariant(const QJsonDocument &val)`

**作用与语义：**

构建一个带有json文档值的新变体，`val`。

### `[noexcept] QVariant::QVariant(const QJsonObject &val)`

**作用与语义：**

构建一个带有json对象值的新变体，`val`。

### `[noexcept(...)] QVariant::QVariant(const QJsonValue &val)`

**作用与语义：**

构造一个带有json值`val`的新变体。
注意：该功能仅在`Private::FitsInInternalSize<sizeof(CborValueStandIn)>` 为`true`时才生效。

### `[noexcept] QVariant::QVariant(const QList<QVariant> &val)`

**作用与语义：**

构造一个带有列表值的新变体，`val`。

### `[noexcept] QVariant::QVariant(const QLocale &l)`

**作用与语义：**

构造一个带有局部值`l`的新变体。

### `[noexcept] QVariant::QVariant(const QMap<QString, QVariant> &val)`

**作用与语义：**

构建了一个带有`QVariant`s映射的新变体，`val`。

### `[noexcept(...)] QVariant::QVariant(const QModelIndex &val)`

**作用与语义：**

构造一个`QModelIndex`值的新变体，`val`。
注意：该函数只有在`Private::FitsInInternalSize<8 + 2 * sizeof(quintptr)>` `true`时才会生效。

### `QVariant::QVariant(const QPersistentModelIndex &val)`

**作用与语义：**

构造一个`QPersistentModelIndex`值的新变体，`val`。

### `[noexcept] QVariant::QVariant(const QRegularExpression &re)`

**作用与语义：**

构造一个正则表达式值为`re`的新变体。

### `[noexcept] QVariant::QVariant(const QString &val)`

**作用与语义：**

构造一个字符串值`val`的新变体。

### `[noexcept] QVariant::QVariant(const QStringList &val)`

**作用与语义：**

构造一个带有字符串列表值的新变体，`val`。

### `[noexcept] QVariant::QVariant(const QUrl &val)`

**作用与语义：**

构建一个URL值为`val`的新变体。

### `QVariant::QVariant(const QVariant &p)`

**作用与语义：**

构造变体`p`的副本，作为该构造函数的参数传递。

### `[noexcept] QVariant::QVariant(QVariant &&other)`

**作用与语义：**

Move构造一个QVariant实例，使其指向`other`所指向的同一个对象。

### `[noexcept] QVariant::~QVariant()`

**作用与语义：**

摧毁`QVariant`和被封存的物体。

### `template <typename T> bool QVariant::canConvert() const`

**作用与语义：**

如果变体可以转换为模板类型 `T`，则返回`true`，否则为 false。
包含指向从 `QObject` 派生的类型指针的`QVariant`，如果对模板类型 `T` 的 `qobject_cast`成功，则该函数也会返回 true。注意，这只适用于使用 `Q_OBJECT` 宏的`QObject`子类。

**官方示例：**

```cpp
 QVariant v = 42;

 v.canConvert<int>();              // returns true
 v.canConvert<QString>();          // returns true

 MyCustomStruct s;
 v.setValue(s);

 v.canConvert<int>();              // returns false
 v.canConvert<MyCustomStruct>();   // returns true
```

### `[since 6.0] bool QVariant::canConvert(QMetaType type) const`

**作用与语义：**

如果变体的类型可以转换为请求的类型，`type` 返回`true`。当调用`toInt()`、`toBool()`、...方法时，这种投射是自动完成的。
注意，该函数仅对变体类型操作，不对内容进行操作。它表示从该变体到`type`的转换路径是否存在，而非尝试转换是否成功。

### `template <typename T> bool QVariant::canView() const`

**作用与语义：**

返回`true`是否能在此变体上创建模板类型`T`的可变视图，否则`false`。

### `void QVariant::clear()`

**作用与语义：**

将该变体转换为类型`QMetaType::UnknownType`，释放所有资源。

### `[static, since 6.0] QPartialOrdering QVariant::compare(const QVariant &lhs, const QVariant &rhs)`

**作用与语义：**

比较`lhs`和`rhs`的对象以进行排序。
如果不支持比较或价值未排序，返回`QPartialOrdering::Unordered`。否则，如果`lhs`小于、等价于或大于`rhs`，则返回`QPartialOrdering::Less`、`QPartialOrdering::Equivalent`或`QPartialOrdering::Greater`。
如果变体包含不同元类型的数据，则视为无序，除非它们都是数值类型或指针类型，否则会使用常规的数值或指针比较规则。
注意：如果进行数值比较且至少有一个值是NaN，则返回`QPartialOrdering::Unordered`。
如果两个变体都包含相同的元类型数据，方法将使用`QMetaType::compare`方法来确定两个变体的顺序，这也可能表明无法在两个值之间建立排序。

### `const void *QVariant::data() const`

**作用与语义：**

返回指向所包含对象的指针，作为一个无法写入的通用空*。

### `[since 6.0] bool QVariant::convert(QMetaType targetType)`

**作用与语义：**

将变体铸造为请求的类型 `targetType`。如果无法执行，变体仍会被更改为请求的类型，但保持在类似于 `QVariant`（Type） 构造的清除空状态。
如果当前类型的变体成功施放，返回`true`;否则返回`false`。
包含指向由`QObject`派生的类型指针的`QVariant`如果成功`qobject_cast`到`targetType`描述的类型，也将转换并返回该函数的true。注意，这仅适用于使用`Q_OBJECT`宏的`QObject`子类。
注意：因未初始化或之前转换失败而为空的QVariant将始终失败，改变类型，保持空，返回`false`。

### `void *QVariant::data()`

**作用与语义：**

返回指向包含对象的指针，作为一个可写入的通用空*。
该函数会分离`QVariant`。当调用`null-QVariant`时，调用后`QVariant`不会为空。

### `[since 6.6] template < typename T, typename... Args, QVariant::if_constructible<T, Args...> = true > T &QVariant::emplace(Args &&... args)`

**作用与语义：**

用`*this` `T`型对象替换当前持有的对象，该对象由`args``...`构造而成。如果`*this`非空，之前持有的对象首先被销毁。如果可能，该方法会重用`QVariant`分配的内存。返回新创建对象的引用。

### `[since 6.6] template < typename T, typename U, typename... Args, QVariant::if_constructible<T, std::initializer_list<U> &, Args...> = true > T &QVariant::emplace(std::initializer_list<U> list, Args &&... args)`

**作用与语义：**

此重载存在是为了支持构造函数接受 `initializer_list` 的类型。它的行为与非初始化列表重载基本相同。

### `[static, since 6.7] QVariant QVariant::fromMetaType(QMetaType type, const void *copy = nullptr)`

**作用与语义：**

创建类型为`type`的变体，如果`copy`未被`nullptr`，则用`*copy`的副本初始化（此时`copy`必须指向类型`type`的对象）。
注意你必须传递你想存储对象的地址。
通常，你不必使用这个构造函数，而是用`QVariant::fromValue()`来构造由`QMetaType::VoidStar`表示的指针类型构造变体，`QMetaType::QObjectStar`。
如果`type`不支持复制构造且`copy`不`nullptr`，变体无效。同样，如果`copy`为`nullptr`且`type`不支持默认构造，变体无效。
返回上述创建的`QVariant`。

### `[static] template <typename... Types> QVariant QVariant::fromStdVariant(const std::variant<Types...> &value)`

**作用与语义：**

返回一个包含`value`活跃变体类型和值的`QVariant`。如果激活类型是 std：：monostate，则返回默认`QVariant`。
注意：使用此方法，你不需要将变体注册为 Qt 元类型，因为 std：：variant 在存储前已被解析。但组件类型应被注册。

### `[static, since 6.6] template <typename... Types> QVariant QVariant::fromStdVariant(std::variant<Types...> &&value)`

**作用与语义：**

返回一个包含`value`活跃变体类型和值的`QVariant`。如果激活类型是 std：：monostate，则返回默认`QVariant`。
注意：使用此方法，你不需要将变体注册为 Qt 元类型，因为 std：：variant 在存储前已被解析。但组件类型应被注册。

### `[static] template <typename T> QVariant QVariant::fromValue(const T &value)`

**作用与语义：**

返回包含`value`副本的`QVariant`。表现与`setValue()`完全相同。

**官方示例：**

```cpp
 MyCustomStruct s;
 return QVariant::fromValue(s);
```

### `[static, since 6.6] template <typename T, QVariant::if_rvalue<T> = true> QVariant QVariant::fromValue(T &&value)`

**作用与语义：**

返回包含`value`副本的`QVariant`。表现与`setValue()`完全相同。

**官方示例：**

```cpp
 MyCustomStruct s;
 return QVariant::fromValue(s);
```

### `bool QVariant::isNull() const`

**作用与语义：**

如果这是空变体，返回`true`，否则返回假。
如果一个变体没有初始化值或空指针，则该变体被视为空。
注意：此行为已从Qt 5更改，其中如果变体包含带有isNull()方法的内置对象且返回true，isNull()也会返回true。

### `bool QVariant::isValid() const`

**作用与语义：**

如果该变体的存储类型不`QMetaType::UnknownType`，返回`true`;否则返回`false`。

### `[since 6.0] QMetaType QVariant::metaType() const`

**作用与语义：**

返回变体中存储值的`QMetaType`。

### `void QVariant::setValue(QVariant &&value)`

**作用与语义：**

移动`value`基于该`QVariant`。这等价于简单地将`value`分配到该`QVariant`。

### `template <typename T, typename = std::enable_if_t<!std::is_same_v<std::decay_t<T>, QVariant>>> void QVariant::setValue(T &&value)`

**作用与语义：**

存储`value`的副本。如果`T`是`QVariant`不支持的类型，则用`QMetaType`来存储该值。如果`QMetaType`不处理该类型，编译时会发生错误。

**官方示例：**

```cpp
 QVariant v;

 v.setValue(5);
 int i = v.toInt();         // i is now 5
 QString s = v.toString();  // s is now "5"

 MyCustomStruct c;
 v.setValue(c);

 //...

 MyCustomStruct c2 = v.value<MyCustomStruct>();
```

### `void QVariant::setValue(const QVariant &value)`

**作用与语义：**

复制品`value`于该`QVariant`。这相当于简单地将`value`分配到该`QVariant`。

### `[noexcept] void QVariant::swap(QVariant &other)`

**作用与语义：**

将该变体与`other`互换。此操作非常快速且从未失败。

### `QBitArray QVariant::toBitArray() const`

**作用与语义：**

如果变体有`userType()` `QMetaType::QBitArray`，则返回该变体为`QBitArray`;否则返回空位数组。

### `bool QVariant::toBool() const`

**作用与语义：**

如果变体有 `userType()` Bool，则返回该变体为布尔。
如果变体具有`userType()` `QMetaType::Bool`、`QMetaType::QChar`、`QMetaType::Double`、`QMetaType::Int`、`QMetaType::LongLong`、`QMetaType::UInt`或`QMetaType::ULongLong`且值非零，或者变体类型为`QMetaType::QString`或`QMetaType::QByteArray`且其小写内容不属于以下之一，则返回`true`：空、“0”或“false”;否则返回`false`。

### `QByteArray QVariant::toByteArray() const`

**作用与语义：**

如果变体有 `userType()` `QMetaType::QByteArray` 或 `QMetaType::QString`（用 `QString::fromUtf8()` 转换），则返回 `QByteArray` 返回;否则返回空字节数组。

### `QChar QVariant::toChar() const`

**作用与语义：**

如果变体有`userType()` `QMetaType::QChar`、`QMetaType::Int`或`QMetaType::UInt`，则返回`QChar`;否则返回无效`QChar`。

### `QDate QVariant::toDate() const`

**作用与语义：**

如果变体有`userType()` `QMetaType::QDate`、`QMetaType::QDateTime`或`QMetaType::QString`，则返回`QDate`;否则返回无效日期。
如果`metaType()` `QMetaType::QString`，字符串无法解析为`Qt::ISODate`格式日期，则返回无效日期。

### `QDateTime QVariant::toDateTime() const`

**作用与语义：**

如果变体有`userType()` `QMetaType::QDateTime`、`QMetaType::QDate`或`QMetaType::QString`，则返回`QDateTime`;否则返回无效的日期/时间。
如果`metaType()` `QMetaType::QString`，字符串无法解析为`Qt::ISODate`格式日期/时间，则返回无效日期/时间。

### `double QVariant::toDouble(bool *ok = nullptr) const`

**作用与语义：**

如果变体具有`userType()` `QMetaType::Double`、`QMetaType::Float`、`QMetaType::Bool`、`QMetaType::QByteArray`、`QMetaType::Int`、`QMetaType::LongLong`、`QMetaType::QString`、`QMetaType::UInt`或`QMetaType::ULongLong`，则返回为双倍;否则返回0.0。
如果`ok`非空：`*``ok`设为真，且该值可转换为双重值;否则`*``ok`设为假。

### `QEasingCurve QVariant::toEasingCurve() const`

**作用与语义：**

如果变体有`userType()` `QMetaType::QEasingCurve`，则返回该变体作为`QEasingCurve`;否则返回默认的缓曲线。

### `float QVariant::toFloat(bool *ok = nullptr) const`

**作用与语义：**

如果变体具有`userType()` `QMetaType::Double`、`QMetaType::Float`、`QMetaType::Bool`、`QMetaType::QByteArray`、`QMetaType::Int`、`QMetaType::LongLong`、`QMetaType::QString`、`QMetaType::UInt`或`QMetaType::ULongLong`，则返回浮点数;否则返回0.0。
如果`ok`非空：`*``ok`设为真，且该值可转换为双重值;否则`*``ok`设为假。

### `QHash<QString, QVariant> QVariant::toHash() const`

**作用与语义：**

如果变体有  ，`QVariant`> 返回 变体 的 `QHash`<`QString`，`metaType()` `QMetaType::QVariantHash`。如果没有，`QVariant` 会尝试将类型转换为哈希，然后返回。对于任何注册了转换为 `QVariantHash` 或用 `Q_DECLARE_ASSOCIATIVE_CONTAINER_METATYPE` 声明为关联容器的类型，该方法都将成功。如果以上条件都不成立，该函数将返回空哈希。

### `int QVariant::toInt(bool *ok = nullptr) const`

**作用与语义：**

如果变体有 `userType()` `QMetaType::Int`、`QMetaType::Bool`、`QMetaType::QByteArray`、`QMetaType::QChar`、`QMetaType::Double`、`QMetaType::LongLong`、`QMetaType::QString`、`QMetaType::UInt` 或 `QMetaType::ULongLong`，则返回 int;否则返回 0。
如果`ok`非空：`*``ok`设为真，且该值可以转换为整数;否则`*``ok`设为假。
警告：如果该值可转换为`QMetaType::LongLong`但过大无法用整数表示，所得的算术溢出不会反映在`ok`中。一个简单的变通方法是使用`QString::toInt()`。

### `QJsonArray QVariant::toJsonArray() const`

**作用与语义：**

如果变体有`userType()` `QJsonArray`，则返回该变体作为`QJsonArray`;否则返回默认构造`QJsonArray`。

### `QJsonDocument QVariant::toJsonDocument() const`

**作用与语义：**

如果变体有`userType()` `QJsonDocument`，则返回变体为`QJsonDocument`;否则返回默认构造`QJsonDocument`。

### `QJsonObject QVariant::toJsonObject() const`

**作用与语义：**

如果变体有`userType()` `QJsonObject`，则返回该变体作为`QJsonObject`;否则返回默认构造`QJsonObject`。

### `QJsonValue QVariant::toJsonValue() const`

**作用与语义：**

如果变体有`userType()` `QJsonValue`，则返回该变体作为`QJsonValue`;否则返回默认构造`QJsonValue`。

### `QLine QVariant::toLine() const`

**作用与语义：**

如果变体有 `userType()` `QMetaType::QLine`，则返回该变体为`QLine`;否则返回无效的`QLine`。

### `QLineF QVariant::toLineF() const`

**作用与语义：**

如果变体有`userType()` `QMetaType::QLineF`，则返回该变体为`QLineF`;否则返回无效`QLineF`。

### `QList<QVariant> QVariant::toList() const`

**作用与语义：**

如果变体有 `userType()` `QMetaType::QVariantList`，则返回该变体作为`QVariantList`。如果没有，`QVariant` 会尝试将该类型转换为列表，然后返回。对于任何注册了转换为 `QVariantList` 或用 `Q_DECLARE_SEQUENTIAL_CONTAINER_METATYPE` 声明为顺序容器的类型，该方法都将成功。如果这些条件都不成立，该函数将返回一个空列表。

### `QLocale QVariant::toLocale() const`

**作用与语义：**

如果变体有 `userType()` `QMetaType::QLocale`，则返回该变体为`QLocale`;否则返回无效`QLocale`。

### `qlonglong QVariant::toLongLong(bool *ok = nullptr) const`

**作用与语义：**

如果变体具有`userType()` `QMetaType::LongLong`、`QMetaType::Bool`、`QMetaType::QByteArray`、`QMetaType::QChar`、`QMetaType::Double`、`QMetaType::Int`、`QMetaType::QString`、`QMetaType::UInt`或`QMetaType::ULongLong`，则返回长long整数;否则返回0。
如果`ok`非空：`*``ok` 设为真，且该值可转换为整数;否则 `*``ok` 设为假。

### `QMap<QString, QVariant> QVariant::toMap() const`

**作用与语义：**

如果变体有 `metaType()` `QMetaType::QVariantMap`，则返回变体为`QVariantMap`。如果没有，`QVariant` 会尝试将类型转换为映射，然后返回。对于任何注册了转换为 `QVariantMap` 或用 `Q_DECLARE_ASSOCIATIVE_CONTAINER_METATYPE` 声明为关联容器的类型，该方法都将成功。如果这些条件都不成立，该函数将返回一个空映射。

### `QModelIndex QVariant::toModelIndex() const`

**作用与语义：**

如果变体有`userType()` `QModelIndex`，则返回该变体作为`QModelIndex`;否则返回默认构造`QModelIndex`。

### `QPersistentModelIndex QVariant::toPersistentModelIndex() const`

**作用与语义：**

如果变体有`userType()` `QPersistentModelIndex`，则返回该变体作为`QPersistentModelIndex`;否则返回默认构造`QPersistentModelIndex`。

### `QPoint QVariant::toPoint() const`

**作用与语义：**

如果变体有`userType()` `QMetaType::QPoint`或`QMetaType::QPointF`，则返回该变体为`QPoint`;否则返回空`QPoint`。

### `QPointF QVariant::toPointF() const`

**作用与语义：**

如果变体有`userType()` `QMetaType::QPoint`或`QMetaType::QPointF`，则返回该变体为`QPointF`;否则返回空`QPointF`。

### `qreal QVariant::toReal(bool *ok = nullptr) const`

**作用与语义：**

如果变体具有`userType()` `QMetaType::Double`、`QMetaType::Float`、`QMetaType::Bool`、`QMetaType::QByteArray`、`QMetaType::Int`、`QMetaType::LongLong`、`QMetaType::QString`、`QMetaType::UInt`或`QMetaType::ULongLong`，则返回qreal;否则返回0.0。
如果`ok`非空：`*``ok`设为真，且该值可转换为双重值;否则`*``ok`设为假。

### `QRect QVariant::toRect() const`

**作用与语义：**

如果变体有`userType()` `QMetaType::QRect`，则返回该变体作为`QRect`;否则返回无效`QRect`。

### `QRectF QVariant::toRectF() const`

**作用与语义：**

如果变体有`userType()` `QMetaType::QRect`或`QMetaType::QRectF`，则返回该变体作为`QRectF`;否则返回无效`QRectF`。

### `QRegularExpression QVariant::toRegularExpression() const`

**作用与语义：**

如果变体有`userType()` `QRegularExpression`，则返回该变体为`QRegularExpression`;否则返回空`QRegularExpression`。

### `QSize QVariant::toSize() const`

**作用与语义：**

如果变体有`userType()` `QMetaType::QSize`，则返回该变体为`QSize`;否则返回无效`QSize`。

### `QSizeF QVariant::toSizeF() const`

**作用与语义：**

如果变体有`userType()` `QMetaType::QSizeF`，则返回该变体为`QSizeF`;否则返回无效`QSizeF`。

### `QString QVariant::toString() const`

**作用与语义：**

如果变体的`userType()`包括但不限于以下，则返回该变体作为`QString`返回：
`QMetaType::QString`、`QMetaType::Bool`、`QMetaType::QByteArray`、`QMetaType::QChar`、`QMetaType::QDate`、`QMetaType::QDateTime`、`QMetaType::Double`、`QMetaType::Int`、`QMetaType::LongLong`、`QMetaType::QStringList`、`QMetaType::QTime`、`QMetaType::UInt`或`QMetaType::ULongLong`。
在不支持的变体上调用 QVariant：：toString() 会返回一个空字符串。

### `QStringList QVariant::toStringList() const`

**作用与语义：**

如果变体有`userType()` `QMetaType::QStringList`、`QMetaType::QString`或`QMetaType::QVariantList`类型且可转换为`QString`，则返回该变体作为`QStringList`返回;否则返回空列表。

### `QTime QVariant::toTime() const`

**作用与语义：**

如果变体有`userType()` `QMetaType::QTime`、`QMetaType::QDateTime`或`QMetaType::QString`，则返回该变体为`QTime`;否则返回无效时间。
如果`metaType()` `QMetaType::QString`，字符串无法解析为`Qt::ISODate`格式时间，则返回无效时间。

### `uint QVariant::toUInt(bool *ok = nullptr) const`

**作用与语义：**

如果变体具有`userType()` `QMetaType::UInt`、`QMetaType::Bool`、`QMetaType::QByteArray`、`QMetaType::QChar`、`QMetaType::Double`、`QMetaType::Int`、`QMetaType::LongLong`、`QMetaType::QString`或`QMetaType::ULongLong`，则返回无符号整数;否则返回0。
如果`ok`非空：`*``ok`设为真，且该值可以转换为无符号整数;否则`*``ok`设为假。
警告：如果该值可转换为`QMetaType::ULongLong`但过大无法用无符号整数表示，所得的算术溢出不会反映在`ok`中。一个简单的变通方法是使用`QString::toUInt()`。

### `qulonglong QVariant::toULongLong(bool *ok = nullptr) const`

**作用与语义：**

如果变体具有`metaType()` `QMetaType::ULongLong`、`QMetaType::Bool`、`QMetaType::QByteArray`、`QMetaType::QChar`、`QMetaType::Double`、`QMetaType::Int`、`QMetaType::LongLong`、`QMetaType::QString`或`QMetaType::UInt`，则返回无符号的long long int;否则返回0。
如果`ok`非空：如果该值可以转换为整数，则`*``ok`设为真;否则`*``ok`设为假。

### `QUrl QVariant::toUrl() const`

**作用与语义：**

如果变体有 `userType()` `QMetaType::QUrl`，则返回该变体为`QUrl`;否则返回无效的`QUrl`。

### `QUuid QVariant::toUuid() const`

**作用与语义：**

如果变体有`metaType()` `QMetaType::QUuid`、`QMetaType::QByteArray`或`QMetaType::QString`，则返回`QUuid`;否则返回默认构造的`QUuid`。

### `const char *QVariant::typeName() const`

**作用与语义：**

返回变体中存储的类型名称。返回的字符串描述用于存储数据的C语言数据类型：例如，“`QFont`”、“`QString`”或“`QVariantList`”。无效变体返回0。

### `int QVariant::typeId() const`

**作用与语义：**

返回变体中存储值的存储类型。这与 `metaType()`.id() 相同。

### `template <typename T> T QVariant::value() const &`

**作用与语义：**

返回转换为模板类型`T`的存储值。调用`canConvert()`以确定类型是否可以转换。如果无法转换，将返回默认构造值。
如果类型`T`由`QVariant`支持，该函数的表现与`toString()`、`toInt()`等完全相同。
如果`QVariant`包含指向由`QObject`派生的类型指针，那么`T`可以是任意`QObject`类型。如果存储在`QVariant`中的指针可以`qobject_cast`到T，则返回该结果。否则返回`nullptr`。注意，这只适用于使用`Q_OBJECT`宏的`QObject`子类。
如果`QVariant`包含顺序容器且`T` `QVariantList`，容器的元素将转换为`QVariant`并返回为`QVariantList`。

**官方示例：**

```cpp
 QVariant v;

 MyCustomStruct c;
 if (v.canConvert<MyCustomStruct>())
     c = v.value<MyCustomStruct>();

 v = 7;
 int i = v.value<int>();                        // same as v.toInt()
 QString s = v.value<QString>();                // same as v.toString(), s is now "7"
 MyCustomStruct c2 = v.value<MyCustomStruct>(); // conversion failed, c2 is empty
```

### `template <typename T> T QVariant::view()`

**作用与语义：**

返回存储值中模板类型`T`的可变视图。调用`canView()`以确定是否支持此类视图。如果无法创建此类视图，返回转换为模板类型`T`的存储值。调用`canConvert()`以确定类型是否可以转换。如果该值既无法查看也无法转换，则返回默认构造的值。

### `[noexcept] QVariant &QVariant::operator=(QVariant &&other)`

**作用与语义：**

移动分配`other`到该`QVariant`实例。

### `QVariant &QVariant::operator=(const QVariant &variant)`

**作用与语义：**

将变体的值分配给该变体`variant`。

### `[alias] QVariantHash`

**作用与语义：**

`QHash`<`QString`的同义词是`QVariant`>。

### `[alias] QVariantList`

**作用与语义：**

`QList`的同义<`QVariant`>词。

### `[alias] QVariantMap`

**作用与语义：**

`QMap`<`QString`的同义词是`QVariant`>。

### `[since 6.6] template <typename T> const T &&get(const QVariant &&v)`

**作用与语义：**

如果`v`包含类型为`T`的对象，则返回对所包含对象的引用，否则调用行为未定义。
取可变`v`的超载会分离`v`：当调用类型匹配`T`的 `null` `v`时，调用后`v`不会为空。
这些功能是为了与`std::variant`兼容而提供。

### `[noexcept, since 6.6] template <typename T> T *get_if(QVariant *v)`

**作用与语义：**

如果`v`包含类型为`T`的对象，则返回指向所含对象的指针，否则返回`nullptr`。
取可变`v`的超载使得脱离`v`：当调用类型匹配`T`的`null` `v`时，调用后`v`不会为空。
这些功能是为了与`std::variant`兼容而提供。

### `template <typename T> T qvariant_cast(const QVariant &value)`

**作用与语义：**

返回已转换为模板类型`T`的给定 `value`。
该函数等价于`QVariant::value()`。

### `[since 6.7] template <typename T> T qvariant_cast(QVariant &&value)`

**作用与语义：**

返回已转换成模板类型`value` `T`。

### `[noexcept] bool operator!=(const QVariant &lhs, const QVariant &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 相等，则返回 `false`；否则返回 `true`。
`QVariant` 使用所包含的 `metaType()` 的等号运算符来检查是否相等。
不同类型的变体通常会被比较为不相等，但有一些例外：
- 如果两种类型都是数值类型（整数和浮点数），Qt 将使用标准 C 类型提升规则来比较这些类型。
- 如果一个类型是数值类型而另一个是 `QString`，Qt 将尝试将 `QString` 转换为匹配的数值类型，如果成功则进行比较。
- 如果两个变体都包含指向 `QObject` 派生类型的指针，`QVariant` 将检查这些类型是否相关并且指向同一对象。

### `QDataStream &operator<<(QDataStream &s, const QVariant &p)`

**作用与语义：**

写入一个变体`p`流`s`。

### `[noexcept] bool operator==(const QVariant &lhs, const QVariant &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 相等，则返回 `true`；否则返回 `false`。
`QVariant` 使用所包含的 `metaType()` 的相等运算符来检查是否相等。
不同类型的变量总是被比较为不相等，但有一些例外：
- 如果两者都是数值类型（整数和浮点数），Qt 将使用标准的 C 类型提升规则来比较这些类型。
- 如果一个类型是数值型，而另一个是 `QString`，Qt 将尝试将 `QString` 转换为匹配的数值类型，如果成功则进行比较。
- 如果两个变量都包含指向 `QObject` 派生类型的指针，`QVariant` 将检查这些类型是否相关并指向同一个对象。
函数的结果不受 `QVariant::isNull` 结果的影响，这意味着即使一个值为 null 而另一个不为 null，它们也可以相等。

### `QDataStream &operator>>(QDataStream &s, QVariant &p)`

**作用与语义：**

读取流`s`的变体`p`。
注意：如果流中包含非内置类型（见 `QMetaType::Type`），必须用 `qRegisterMetaType()` 或 `QMetaType::registerType()` 注册这些类型，变体才能正确加载。如果发现未注册类型，`QVariant` 会在流中设置损坏标志，停止处理并打印警告。例如，对于`QList`<int>，它会打印以下内容：

### `(since 6.11) class ConstPointer`

**作用与语义：**

QVariant：：ConstPointer 是一个模板类，模拟了指向 QVariant 的 const 指针。
`QVariant::ConstPointer` 包裹指向值，并返回其运算符*()的 `QVariant::ConstReference`。这使得它适合作为实际指针的替代。我们无法从泛型迭代器返回实际指针，因为迭代器不持有实际`QVariant`。

### `(since 6.11) class ConstReference`

**作用与语义：**

QVariant::ConstReference 充当 QVariant 的常量引用。
由于通用迭代器在每步操作中实际上并未实例化 `QVariant`，因此无法从 operator*() 返回对它的引用。`QVariant::ConstReference` 提供与对 `QVariant` 的实际引用相同的功能，但其支持由模板参数提供的被引用值。该模板适用于 QMetaSequence::ConstIterator、QMetaSequence::Iterator、QMetaAssociation::ConstIterator 和 QMetaAssociation::Iterator。

### `(since 6.11) class Pointer`

**作用与语义：**

QVariant：:P ointer 是一个模板类，它模拟了一个指向 QVariant 的非一致性指针。
`QVariant::Pointer` 包裹指向值，并返回其运算符*()的`QVariant::Reference`。这使得它适合替代实际指针。我们无法从泛型迭代器返回实际指针，因为迭代器不持有实际`QVariant`。

### `(since 6.11) class Reference`

**作用与语义：**

QVariant::Reference 充当 QVariant 的非常量引用。
由于通用迭代器在每步操作中实际上并未实例化 `QVariant`，因此无法从 operator*() 返回对它的引用。`QVariant::Reference` 提供与对 `QVariant` 的实际引用相同的功能，但其支持由模板参数提供的被引用值。该模板适用于 QMetaSequence::Iterator 和 QMetaAssociation::Iterator。

### `const void * constData() const`

**作用与语义：**

返回指向所包含对象的指针，作为一个无法写入的通用空*。

### `int userType() const`

**作用与语义：**

返回变体中存储值的存储类型。这与 `metaType()`.id() 相同。

### `(since 6.6) T & get(QVariant &v)`

**作用与语义：**

如果`v`包含类型为`T`的对象，则返回对所包含对象的引用，否则调用行为未定义。
取可变`v`的超载会分离`v`：当调用类型匹配`T`的 `null` `v`时，调用后`v`不会为空。
这些功能是为了与`std::variant`兼容而提供。

### `(since 6.6) T && get(QVariant &&v)`

**作用与语义：**

如果`v`包含类型为`T`的对象，则返回对所包含对象的引用，否则调用行为未定义。
取可变`v`的超载会分离`v`：当调用类型匹配`T`的 `null` `v`时，调用后`v`不会为空。
这些功能是为了与`std::variant`兼容而提供。

### `(since 6.6) const T & get(const QVariant &v)`

**作用与语义：**

如果`v`包含类型为`T`的对象，则返回对所包含对象的引用，否则调用行为未定义。
取可变`v`的超载会分离`v`：当调用类型匹配`T`的 `null` `v`时，调用后`v`不会为空。
这些功能是为了与`std::variant`兼容而提供。

### `(since 6.6) const T * get_if(const QVariant *v)`

**作用与语义：**

如果`v`包含类型为`T`的对象，则返回指向所含对象的指针，否则返回`nullptr`。
取可变`v`的超载使得脱离`v`：当调用类型匹配`T`的`null` `v`时，调用后`v`不会为空。
这些功能是为了与`std::variant`兼容而提供。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要用 QVariant 掩盖本可静态检查的类型；区分 invalid 和 null；自定义类型先满足 QMetaType 要求；不要假定 `toInt()` 返回 0 就是转换成功，应读取 ok。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QVariant` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
