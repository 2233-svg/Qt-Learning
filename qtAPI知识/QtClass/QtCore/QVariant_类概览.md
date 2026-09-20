# Qt QVariant 可变类型值容器笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QVariant>`  
> 所属模块：`Qt6::Core`  
> 类型性质：拥有一个类型擦除值的值语义容器  
> 直接协作：`QMetaType`、`QMetaObject`、`QDataStream`、`QJsonValue`、`QList<QVariant>`、`QMap<QString, QVariant>`

## 1. 它解决什么问题

普通 C++ 变量在编译期就固定了类型。`QVariant` 解决的是“同一个接口需要在运行时承载不同类型的值”：

- 模型的不同 role 返回不同类型的数据；
- 属性编辑器根据运行时类型读取和写回字段；
- 配置、脚本、插件边界需要传递异构值；
- JSON、CBOR、数据流和 Qt 容器之间需要一个统一值接口；
- 自定义类型需要在不暴露具体模板参数的地方保存和传递。

`QVariant` 保存两部分信息：

1. 一个 `QMetaType`，描述当前值是什么类型以及如何构造、拷贝、销毁和转换；
2. 一份该类型的实际对象值。

它不是“任意指针盒子”。`QVariant` 按值拥有自己的内容：把一个 `QString`、结构体或容器放进去后，调用方可以销毁原变量；如果放入的是指针，`QVariant` 保存的是指针值，不会因此接管指向对象的所有权。

## 2. 实际使用场景

### 2.1 模型 role 数据

```cpp
QVariant MyModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid())
        return {};

    if (role == Qt::DisplayRole)
        return QStringLiteral("row %1").arg(index.row());

    if (role == Qt::UserRole)
        return index.row();

    return {};
}
```

返回默认构造的 `QVariant` 表示无效值。模型可以用 `isValid()` 区分“没有数据”和一个有效但内容为空的字符串、列表或日期。

### 2.2 自定义值放入和取出

```cpp
struct UserId
{
    qint64 value = 0;
};

Q_DECLARE_METATYPE(UserId)

QVariant packUserId(UserId id)
{
    return QVariant::fromValue(id);
}

UserId unpackUserId(const QVariant &value)
{
    return value.value<UserId>();
}
```

`Q_DECLARE_METATYPE` 让模板化的 `fromValue()`、`value<T>()`、`qvariant_cast<T>()` 使用自定义类型。取出失败时，`value<T>()` 返回 `T{}`，所以对关键数据应先检查 `metaType()` 或使用 `get_if<T>()`。

### 2.3 配置和属性表

```cpp
QVariantMap settings;
settings.insert(QStringLiteral("timeoutMs"), 1500);
settings.insert(QStringLiteral("enabled"), true);
settings.insert(QStringLiteral("endpoint"),
                QUrl(QStringLiteral("https://example.test")));

const int timeout = settings.value(QStringLiteral("timeoutMs")).toInt();
```

这种接口适合字段数量和类型由配置决定的场景。配置边界应明确转换失败、缺失键和空值的区别，不要把所有失败都默认为 `0` 或空字符串。

### 2.4 原地转换

```cpp
QVariant value = QStringLiteral("42");

if (value.canConvert<int>() && value.convert(QMetaType::fromType<int>())) {
    const int number = value.value<int>();
    Q_ASSERT(number == 42);
}
```

`convert()` 会改变当前 `QVariant` 的类型和值。只想读取转换结果而不改变源值时，用 `value<T>()` 或先复制一个 `QVariant`。

### 2.5 按类型动态构造

```cpp
const QMetaType type = QMetaType::fromType<UserId>();
QVariant value = QVariant::fromMetaType(type);

if (value.isValid())
    value.setValue(UserId{7});
```

Qt 6.7 起，`fromMetaType()` 适合框架代码已经持有 `QMetaType` 的场景。它会按类型描述默认构造或拷贝构造值；不能构造的类型会得到无效结果。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QVariant>
```

按功能补充：

```cpp
#include <QMetaType>  // QMetaType::fromType、QMetaType::Type
#include <QVariantMap>
#include <QVariantList>
#include <QDataStream> // QVariant::save/load
#include <QJsonValue>  // JSON 类型
```

## 4. 先建立使用模型

### 4.1 默认构造是“无效 QVariant”

```cpp
QVariant value;
Q_ASSERT(!value.isValid());
```

无效值没有有效的 `QMetaType`，`typeId()` 为 `0`，`typeName()` 通常返回空指针。它与一个有效的空字符串、空列表或空字节数组不同。

### 4.2 有效和非空是两条不同轴

```cpp
QVariant invalid;
QVariant emptyString = QString();
QVariant nullPointer = QVariant::fromValue(static_cast<QObject *>(nullptr));

// invalid.isValid() == false
// emptyString.isValid() == true
// emptyString.isNull() 反映 QString 的 null 状态
```

`isValid()` 判断是否保存了某种类型；`isNull()` 判断当前值是否处于该类型的 null 状态。不同类型对 null 的表示不同，不应把 `isNull()` 当成统一的“没有数据”判断。

### 4.3 拷贝是值语义，但可能共享底层存储

```cpp
QVariant first = QStringLiteral("hello");
QVariant second = first;

second.setValue(QStringLiteral("changed"));
// first 仍然是 "hello"
```

Qt 可以让两个 `QVariant` 暂时共享隐式共享数据；写入时会分离。调用方只需要依赖值语义，不应依赖具体是内联存储、共享堆存储还是何时发生深拷贝。

### 4.4 `value<T>()`、`get<T>()`、`view<T>()` 不是同一种操作

| API | 语义 |
| --- | --- |
| `value<T>()` / `qvariant_cast<T>()` | 精确取值或尝试元类型转换，返回一个 `T` 值 |
| `get<T>()` | 只接受精确类型，返回引用或右值引用，不执行转换 |
| `get_if<T>()` | 只接受精确类型，失败返回 `nullptr` |
| `view<T>()` | 通过 `QMetaType` 的 view 机制生成目标 view，通常借用源值 |

在不确定类型时，优先 `get_if<T>()` 或先检查 `canConvert<T>()`；不要把 `value<T>()` 返回的默认值当成成功结果。

## 5. 自定义类型的推荐流程

```cpp
struct TaskInfo
{
    QString name;
    int priority = 0;
};

Q_DECLARE_METATYPE(TaskInfo)

void useTaskInfo()
{
    TaskInfo source{QStringLiteral("index"), 3};
    QVariant value = QVariant::fromValue(source);

    if (value.metaType() == QMetaType::fromType<TaskInfo>()) {
        if (const TaskInfo *task = get_if<TaskInfo>(&value))
            qDebug() << task->name << task->priority;
    }
}
```

`Q_DECLARE_METATYPE` 应放在完整类型定义之后，通常放在公共类型头文件中。`QVariant::fromValue()` 会确保存入的类型有运行时注册信息；如果同一类型还要通过 queued signal/slot 或 `fromName()` 使用，再显式调用 `qRegisterMetaType<TaskInfo>()`。

## 6. 生命周期、所有权和分离边界

### 6.1 `QVariant` 拥有值，不拥有裸指针指向的对象

```cpp
QObject *object = new QObject;
QVariant value = QVariant::fromValue(object);

// value 只保存 QObject* 的指针值。
// delete object 后，value 不会自动变成安全的空指针。
```

如果要表达对象生命周期，应使用 `QPointer<T>`、`QSharedPointer<T>` 等具有明确语义的类型，并考虑它们是否已被 `QMetaType` 支持。裸指针放进 `QVariant` 后，对象销毁不会通知或清空这个值。

### 6.2 `data()` 可能触发分离

```cpp
QVariant first = QStringLiteral("hello");
QVariant second = first;

void *raw = second.data();
Q_UNUSED(raw);
// second 需要可写，必要时会与 first 分离。
```

非 `const` `data()`、`emplace()`、`setValue()` 和某些非 const 代理操作都可能改变共享状态。`constData()` 和 `data() const` 不提供可写地址，也不应通过 `const_cast` 绕过这一约束。

### 6.3 指针和引用返回值不能跨变更保存

以下操作可能使旧的 `data()` 指针、`get()` 引用或 view 失效：

- 给 `QVariant` 赋值；
- `clear()`；
- `convert()`；
- `emplace()`；
- `setValue()`；
- 触发隐式共享分离；
- 变更源对象导致其内部缓冲区重分配。

需要长期保存值时复制出独立的 `T`；需要长期保存 view 时同时管理源 `QVariant` 和源对象的生命周期。

## 7. 转换、读取和失败语义

### 7.1 `canConvert()` 只查询能力

```cpp
const QVariant value = QStringLiteral("not a number");
if (value.canConvert<int>()) {
    bool ok = false;
    const int number = value.toInt(&ok);
    if (!ok) {
        // 具体文本仍然可能无法转换。
    }
}
```

存在一个注册转换路径，不等于每个输入值都能成功。数值溢出、格式错误和自定义转换返回失败都应通过返回值或 `ok` 标记处理。

### 7.2 数值 `toX(bool *ok)` 要检查 `ok`

带 `bool *ok` 的数值转换在失败时通常返回目标类型的默认值或零。这个返回值本身无法区分“转换失败”和“输入确实是零”：

```cpp
bool ok = false;
const int number = value.toInt(&ok);
if (!ok)
    return;
```

### 7.3 对象类型 `toX()` 也可能返回默认对象

`toDate()`、`toUrl()`、`toJsonObject()`、`toMap()` 等没有 `ok` 参数。调用方应先检查 `canConvert<T>()`，并根据目标类型的 `isNull()`、`isEmpty()` 或自身有效性 API 继续判断。

### 7.4 `convert()` 会替换当前类型

```cpp
QVariant value = QStringLiteral("42");
if (value.convert(QMetaType::fromType<int>())) {
    // value.metaType() 现在是 int
}
```

如果转换失败，调用方应把 `false` 作为失败处理，不要假设 variant 已经变成目标类型。转换成功后，之前指向旧值的 raw 指针和引用不再有效。

## 8. `QVariant` 与 `QMetaType`

`QVariant` 的大多数动态行为最终都由 `QMetaType` 完成：

| QVariant 操作 | QMetaType 对应能力 |
| --- | --- |
| `metaType()` / `typeName()` | 类型身份和名称 |
| `fromMetaType()` | 按描述创建值 |
| `value<T>()` | 精确访问或 `QMetaType::convert()` |
| `canConvert()` / `convert()` | `QMetaType::canConvert()` / `convert()` |
| `canView()` / `view()` | `QMetaType::canView()` / `view()` |
| `emplace<T>()` | 按 `QMetaType::fromType<T>()` 准备存储后直接构造 |
| `save()` / `load()` | 类型注册的数据流操作 |

如果动态调用结果不符合预期，先打印：

```cpp
qDebug() << value.metaType().name()
         << value.metaType().id()
         << value.isValid()
         << value.isNull();
```

## 9. 逐项 API 说明

### 9.1 `QVariant::Type` 旧枚举

`QVariant::Type` 在 Qt 6 中已弃用，应使用 `QMetaType::Type` 和 `QMetaType`。旧枚举包含 `Invalid`、`Bool`、`Int`、`String`、`Map`、`List`、`UserType` 等兼容名称，但它不能完整表达现代 Qt 的所有元类型。

不要把 `QVariant::Type` 传给新代码中的类型判断，也不要使用 `QVariant(QMetaType::Type)` 这种已被删除的意图模糊构造方式。

### 9.2 代理类型 `Reference`、`ConstReference`、`Pointer`、`ConstPointer`

这些是 `QVariant` 为间接访问/代理 API 提供的嵌套模板。它们不是 C++ 原生引用，也不是指向 `QVariant` 内部对象的裸指针；它们保存一个 `Indirect` 句柄，并把读取、赋值或转换委托给相应的间接类型。

#### `QVariant::Reference<Indirect>`

- `Reference(const Indirect &referred)`：保存一个可写间接句柄；
- `Reference(Indirect &&referred)`：移动构造间接句柄；
- `operator QVariant()`：把当前代理内容转换成一个 `QVariant` 值；
- `operator=(const QVariant &value)`：把 variant 值写回间接目标；
- `operator=(const Reference &value)`、右值重载：读取源代理，再写入当前目标；
- `operator=(const ConstReference &value)`、右值重载：读取 const 代理，再写入当前目标；
- `swap(Reference other)`：交换两个代理所代表的内容，不是交换代理对象内部句柄；
- `operator*` 不属于 `Reference`，而属于 `Pointer`。

它的核心边界是：代理对象本身通常很短命，真正的写入目标由 `Indirect` 决定。不能把它当成保证长期有效的 `T &`。

#### `QVariant::ConstReference<Indirect>`

- 可以从 `const Indirect &` 或 `Indirect &&` 构造；
- 可以从 `Reference<Indirect>` 转成 const reference；
- 可拷贝构造，但不能移动构造；
- 不能赋值；
- `operator QVariant()` 生成一个值副本或由 `Indirect` 专门化实现的 variant。

它用于只读代理。转换成 `QVariant` 后得到的是值容器，不是对原目标的持续引用。

#### `QVariant::Pointer<Indirect>`

- 从 `Indirect` 的左值或右值构造；
- `operator*()` 返回 `Reference<Indirect>`；
- 可以隐式转换成 `ConstPointer<Indirect>`。

这里的 `operator*()` 返回的是代理，不是 `Indirect` 指针指向对象的 C++ 引用。它适合需要“解引用后读写 variant 值”的容器代理协议。

#### `QVariant::ConstPointer<Indirect>`

- 从 `Indirect` 的左值或右值构造；
- `operator*()` 返回 `ConstReference<Indirect>`；
- 只读，不提供写回入口。

### 9.3 构造函数

#### `QVariant()`

构造无效 variant。它不包含 `QMetaType` 和有效对象值；`isValid()` 返回 `false`。

#### `~QVariant()`

销毁当前 variant，释放或减少内部存储的引用，并调用当前值类型的析构逻辑。若当前值是裸指针，只销毁指针值，不删除指向对象。

#### `explicit QVariant(QMetaType type, const void *copy = nullptr)`

按 `type` 创建一个 variant：

- `copy == nullptr`：尝试默认构造目标值；
- `copy != nullptr`：从同类型对象拷贝构造；
- `type` 无效或类型不能按要求构造时，结果可能无效；
- `copy` 必须指向与 `type` 完全匹配的对象。

新代码不要把 `QMetaType::Type` 整数枚举直接传给这个构造函数；`QVariant(QMetaType::Type)` 已被删除以避免把类型枚举误当成一个 `int` 值。

#### `QVariant(const QVariant &other)`

拷贝 variant 的值语义。实现可以共享内部存储，后续写入时分离；它不会让两个 variant 共享“可见的可变值”。

#### `QVariant(QVariant &&other)`

移动构造，通常转移内部表示并把 `other` 置为有效但无值的默认状态。移动后不要依赖 `other` 仍保存原值；可以安全析构或重新赋值。

#### `QVariant(std::in_place_type_t<T>, Args &&... args)`（Qt 6.6）

直接在 variant 的存储中构造 `T`，避免先构造临时 `T` 再复制：

```cpp
QVariant value(std::in_place_type<QString>, 5, QChar('x'));
Q_ASSERT(value.value<QString>() == QStringLiteral("xxxxx"));
```

`T` 必须可拷贝、可析构并能用给定参数构造；`T` 不能是引用或 `const` 类型。

#### `QVariant(std::in_place_type_t<T>, std::initializer_list<U>, Args &&... args)`（Qt 6.6）

支持使用初始化列表直接构造目标类型，例如：

```cpp
QVariant value(std::in_place_type<QList<int>>,
               {1, 2, 3});
```

目标类型仍需满足 `QVariant` 的可拷贝和可析构要求。

#### 基础数值构造函数

以下构造函数按对应元类型保存值：

- `QVariant(int)`
- `QVariant(uint)`
- `QVariant(qlonglong)`
- `QVariant(qulonglong)`
- `QVariant(bool)`
- `QVariant(double)`
- `QVariant(float)`

注意 `char`、`short`、`long` 等 C++ 基础类型可能经过标准整数提升进入其他构造函数；需要稳定的元类型时，应显式转换成目标 Qt 类型。

#### Core 值类型构造函数

以下构造函数直接保存对应类型：

- `QVariant(QChar)`
- `QVariant(QDate)`
- `QVariant(QTime)`
- `QVariant(const QBitArray &)`
- `QVariant(const QByteArray &)`
- `QVariant(const QDateTime &)`
- `QVariant(const QHash<QString, QVariant> &)`
- `QVariant(const QJsonArray &)`
- `QVariant(const QJsonObject &)`
- `QVariant(const QList<QVariant> &)`
- `QVariant(const QLocale &)`
- `QVariant(const QMap<QString, QVariant> &)`
- `QVariant(const QRegularExpression &)`
- `QVariant(const QString &)`
- `QVariant(const QStringList &)`
- `QVariant(const QUrl &)`
- `QVariant(const QJsonValue &)`
- `QVariant(const QJsonDocument &)`
- `QVariant(const QModelIndex &)`
- `QVariant(const QPersistentModelIndex &)`
- `QVariant(QUuid)`
- `QVariant(QSize)`
- `QVariant(QSizeF)`
- `QVariant(QPoint)`
- `QVariant(QPointF)`
- `QVariant(QLine)`
- `QVariant(QLineF)`
- `QVariant(QRect)`
- `QVariant(QRectF)`

这些构造函数的 `noexcept` 条件由类型存储策略决定；调用方不应把 `noexcept` 当成值转换成功的保证。

#### 条件编译的 Core/GUI 类型构造函数

当相应 Qt 配置启用时，还提供：

- `QVariant(const QEasingCurve &)`
- `QVariant(const QKeySequence &)` 通过其元类型路径使用；
- 其他 GUI 类型通常通过 `QVariant::fromValue()` 或 `QMetaType` 构造。

`QVariant` 的直接构造列表受模块配置和头文件依赖影响；跨模块代码对 GUI 类型应优先显式 `fromValue()`，避免隐式转换选择不清晰。

#### `QVariant(const char *str)`

在允许 ASCII 转换的构建中，把 UTF-8 `const char *` 转为 `QString` 再保存。传入空指针不是有效字符串；需要明确编码和生命周期时，优先使用 `QString`、`QStringView` 或 `QByteArray`。

#### `QVariant(QLatin1StringView string)`

把 Latin-1 字符串视图转换为 `QString` 后保存。它不保存调用方字符串视图的借用关系，variant 拥有转换后的值。

#### 被删除的指针构造

`QVariant(void *)` 以及满足指针/成员指针条件的模板构造被删除，防止：

- 裸指针意外转换成 `bool`；
- 用户误以为 QVariant 自动接管指针；
- `QVariant(nullptr)` 的语义不清晰。

如确实需要保存一个指针值，使用：

```cpp
QVariant value = QVariant::fromValue(static_cast<QObject *>(nullptr));
```

#### 被删除的 Qt 枚举构造

`Qt::GlobalColor`、`Qt::BrushStyle`、`Qt::PenStyle`、`Qt::CursorShape` 等构造被删除，因为直接把它们放入 `QVariant` 容易得到一个 `int` variant，而不是对应的颜色、画刷或样式对象。应先构造正确的目标类型，例如 `QColor(Qt::red)`。

### 9.4 赋值和交换

#### `QVariant &operator=(const QVariant &other)`

执行值语义拷贝赋值。自赋值安全；原内容会按其 `QMetaType` 规则释放或共享。

#### `QVariant &operator=(QVariant &&other)`

移动赋值。移动后 `other` 可以重新使用，但不再保证仍保存原值。

#### `void swap(QVariant &other) noexcept`

交换两个 variant 的内部表示，通常不复制实际值。它不转换类型，也不改变值的相对所有权。

#### `void clear()`

清空当前值，使 variant 变成无效状态。之前由 `data()`、`get()` 或 view 得到的地址/引用不再使用。

### 9.5 类型身份和共享状态

#### `int typeId() const`

返回当前值的运行时类型 ID。无效 variant 返回 `0`。Qt 6 新代码优先使用 `metaType()`，只有与旧接口或 ID 表格交互时才使用它。

#### `int userType() const`

Qt 兼容名称，Qt 6 中直接返回 `typeId()`。名字中虽然有 `user`，但它也会返回内置类型 ID。

#### `const char *typeName() const`

返回当前类型名称；无效 variant 通常返回 `nullptr`。指针由 `QMetaType` 管理，不应释放。长期保存请复制成 `QByteArray`。

#### `QMetaType metaType() const`

Qt 6.0 起返回当前值的 `QMetaType`。这是判断类型的推荐入口：

```cpp
if (value.metaType() == QMetaType::fromType<QString>()) {
    const QString text = value.value<QString>();
}
```

#### `bool isValid() const`

判断 variant 是否包含有效类型和值。默认构造和 `clear()` 后为 `false`。

#### `bool isNull() const`

判断当前值是否处于 null 状态。它与 `isValid()` 独立；一个有效的 null `QString`、空指针或其他支持 null 的类型可能同时满足 `isValid() == true` 和 `isNull() == true`。

#### `void detach()`

确保当前 variant 拥有独立的可写存储。若当前内容没有共享，通常不做额外工作；若共享，可能复制值。

#### `bool isDetached() const`

查询当前存储是否未与其他 variant 共享。它是实现层状态查询，不应作为业务逻辑中的稳定性能承诺。

### 9.6 转换能力和原地转换

#### `template <typename T> bool canConvert() const`

查询当前值是否可以转换到 `T`，模板版本等价于使用 `QMetaType::fromType<T>()`。它只表示存在转换路径，不保证具体输入成功。

#### `bool canConvert(QMetaType targetType) const`

运行时类型版本。传入无效 `targetType` 时应视为不能进行有效转换。

#### `template <typename T> bool canView() const`

查询当前值是否能建立 `T` 类型的 mutable view。它不复制源值，view 的生命周期通常受 variant 和内部存储限制。

#### `bool canView(QMetaType targetType) const`

按运行时目标类型查询 view 能力。

#### `bool convert(QMetaType targetType)`

尝试把当前 variant 原地转换成 `targetType`：

- 成功后 `metaType()` 变为目标类型；
- 失败时返回 `false`，调用方必须按失败路径处理；
- 转换可能分离共享存储；
- 所有指向旧值的地址、引用和 view 都应视为失效。

#### `template <typename T> T view()`

创建 `T` 类型的 view 并按值返回。它不会返回成功标志，因此使用前先调用 `canView<T>()`。返回的 `T` 可能保存指向 variant 内部数据的借用指针，不能超过源 variant 或源对象的生命周期。

#### `static QPartialOrdering compare(const QVariant &lhs, const QVariant &rhs)`

按 QVariant 的类型和值比较规则返回部分序关系。返回值可能是 `Less`、`Equivalent`、`Greater` 或 `Unordered`。异构值、不可排序值和某些浮点值不能简单地当成普通总序排序。

### 9.7 raw 数据访问

#### `void *data()`

返回当前值的可写存储地址，必要时先分离共享存储。无效 variant 没有可用对象地址；调用方不得把返回的 `void *` 当成任意类型。

#### `const void *constData() const`

返回当前值的只读存储地址，不触发可写分离。地址只在 variant 未发生改变且源值仍存在时有效。

#### `const void *data() const`

const 重载，语义等同于 `constData()`。它不会返回可写地址。

### 9.8 `emplace`

#### `template <typename T, typename... Args> T &emplace(Args &&... args)`（Qt 6.6）

销毁旧值并在 variant 中直接构造 `T`，返回新构造对象的引用：

```cpp
QVariant value;
QString &text = value.emplace<QString>(3, QChar('x'));
text += QLatin1StringView("y");
```

注意：

- `T` 不能是引用或 `const`；
- `T` 必须可拷贝和可析构；
- 旧值的 raw 指针、引用和 view 会失效；
- 返回引用只在 variant 不发生再次替换前有效。

#### `template <typename T, typename U, typename... Args> T &emplace(std::initializer_list<U>, Args &&... args)`（Qt 6.6）

使用初始化列表原地构造 `T`。适合 `QList<int>`、`QVector<QString>` 等支持 initializer-list 构造的类型；仍需满足 QVariant 的值语义要求。

### 9.9 设置和读取值

#### `void setValue(const QVariant &value)`

把另一个 variant 的值复制到当前对象。它等价于拷贝赋值的语义。

#### `void setValue(QVariant &&value)`

移动另一个 variant 的值到当前对象。

#### `template <typename T> void setValue(T &&value)`

把 `T` 的值复制或移动到 variant。若当前 variant 已经是同一类型且存储独占，Qt 可能复用现有存储；这只是实现优化，不应依赖其地址稳定性。

对于自定义类型，应先 `Q_DECLARE_METATYPE(T)`。值必须满足 QVariant 的拷贝和析构要求。

#### `template <typename T> T value() const &`

返回一个 `T` 值：

- 当前类型与 `T` 精确相同时，拷贝当前对象；
- 类型不同但有转换路径时，尝试转换；
- 失败时返回 `T{}`；
- 若 `T` 不能默认构造，转换路径可能无法编译。

关键数据建议先检查：

```cpp
if (value.metaType() != QMetaType::fromType<TaskInfo>())
    return;

const TaskInfo task = value.value<TaskInfo>();
```

#### `template <typename T> T value() &&`

从右值 variant 取值。在类型完全匹配且存储独占时可能移动出对象；共享存储、类型转换或不能移动时可能退化为拷贝。不要把它当成一定零拷贝的承诺。

#### `static QVariant fromValue(const T &value)`

按值复制 `value` 到新 variant。类型必须可拷贝和可析构。存入后 variant 会保证类型拥有运行时注册信息。

#### `static QVariant fromValue(T &&value)`（Qt 6.6）

对非 const 右值优先使用移动构造，仍保留 QVariant 的可拷贝值语义约束。传入 `std::move(value)` 后，调用方应按移动后对象处理 `value`。

#### `static QVariant fromMetaType(QMetaType type, const void *copy = nullptr)`（Qt 6.7）

按运行时类型描述创建 variant。`copy` 为空时默认构造，非空时按同类型复制。它适合类型只有在运行时才知道的框架代码；`type` 无效或无法构造时检查返回的 `isValid()`。

#### `static QVariant fromStdVariant(const std::variant<Types...> &value)`

把当前持有的 `std::variant` 分支转换为对应的 `QVariant`。每个可能分支都必须适合 `QVariant::fromValue()`；如果 `std::variant` 为 `valueless_by_exception()`，结果是无效 variant。

#### `static QVariant fromStdVariant(std::variant<Types...> &&value)`（Qt 6.6）

移动当前 `std::variant` 分支中的值到 `QVariant`。它仍然遵守目标类型的 QVariant 值语义要求。

### 9.10 数值读取 API

以下函数执行到目标数值类型的转换；带 `bool *ok` 的版本用它区分失败和零值：

#### `int toInt(bool *ok = nullptr) const`

转为 `int`。检查范围和文本格式，必要时传入 `ok`。

#### `uint toUInt(bool *ok = nullptr) const`

转为 `uint`。负数、溢出和不兼容文本应通过 `ok` 处理。

#### `qlonglong toLongLong(bool *ok = nullptr) const`

转为有符号 64 位整数。

#### `qulonglong toULongLong(bool *ok = nullptr) const`

转为无符号 64 位整数。

#### `bool toBool() const`

转为布尔值。它没有 `ok` 参数，调用方应先确认源类型和转换语义。

#### `double toDouble(bool *ok = nullptr) const`

转为双精度浮点数，检查文本格式和数值范围。

#### `float toFloat(bool *ok = nullptr) const`

转为单精度浮点数，注意精度损失和范围。

#### `qreal toReal(bool *ok = nullptr) const`

按平台 `qreal` 类型转数值；不要把它与固定宽度的 `double` 交换使用。

### 9.11 基础值和容器读取 API

这些函数返回目标值类型；失败时通常返回目标类型默认值或空对象，没有统一 `ok` 输出，因此应配合 `canConvert()`、`metaType()` 或目标类型自己的有效性判断。

#### `QByteArray toByteArray() const`

转换为 `QByteArray`，适合二进制数据。不要把它当作 UTF-8 文本的自动正确编码器。

#### `QBitArray toBitArray() const`

转换为位数组。

#### `QString toString() const`

转换为字符串。数字、日期、字节数组等类型的格式由 Qt 的转换规则决定，不等于业务格式化协议。

#### `QStringList toStringList() const`

转换为字符串列表。单个字符串是否能变成单元素列表取决于 Qt 的转换规则，业务代码应明确约定。

#### `QChar toChar() const`

转换为单个 UTF-16 字符；多字符字符串的转换边界应由调用方验证。

#### `QDate toDate() const`

转换为日期，失败时返回无效日期。

#### `QTime toTime() const`

转换为时间，失败时返回无效时间。

#### `QDateTime toDateTime() const`

转换为日期时间，时区和有效性应由结果对象检查。

#### `QList<QVariant> toList() const`

转换为 `QList<QVariant>`。它不是对任意顺序容器的无条件视图，必要时会产生值转换或副本。

#### `QMap<QString, QVariant> toMap() const`

转换为字符串键 map。非字符串键或不兼容对象不会自动保留为原始容器结构。

#### `QHash<QString, QVariant> toHash() const`

转换为字符串键 hash。它与 `toMap()` 的顺序和查找特性不同。

### 9.12 几何和本地化读取 API

#### `QPoint toPoint() const`

转换为整数点。

#### `QPointF toPointF() const`

转换为浮点点。

#### `QRect toRect() const`

转换为整数矩形。

#### `QRectF toRectF() const`

转换为浮点矩形。

#### `QSize toSize() const`

转换为整数尺寸。

#### `QSizeF toSizeF() const`

转换为浮点尺寸。

#### `QLine toLine() const`

转换为整数线段。

#### `QLineF toLineF() const`

转换为浮点线段。

#### `QLocale toLocale() const`

转换为 `QLocale`，失败时返回默认 locale。

#### `QRegularExpression toRegularExpression() const`

在启用正则表达式模块时，转换为正则表达式。结果的 `isValid()` 仍需检查。

#### `QEasingCurve toEasingCurve() const`

在启用 easing curve 时，转换为缓动曲线。

#### `QUuid toUuid() const`

转换为 UUID，失败时返回 null UUID。

#### `QUrl toUrl() const`

转换为 URL；结果是否有效需调用 `isValid()`。

### 9.13 JSON、CBOR 和模型索引读取 API

#### `QJsonValue toJsonValue() const`

转换为 JSON 值。不能表示为 JSON 的自定义类型不会自动变成可序列化对象。

#### `QJsonObject toJsonObject() const`

转换为 JSON 对象；失败时结果为空或无效，需结合 `canConvert()` 判断。

#### `QJsonArray toJsonArray() const`

转换为 JSON 数组。

#### `QJsonDocument toJsonDocument() const`

转换为 JSON 文档。

#### `QModelIndex toModelIndex() const`

在启用 item model 时转换为模型索引。索引本身是否有效由 `QModelIndex::isValid()` 判断。

#### `QPersistentModelIndex toPersistentModelIndex() const`

转换为持久模型索引；它的持久性仍受模型生命周期和模型变更规则约束。

### 9.14 数据流

#### `void save(QDataStream &ds) const`

把 variant 的类型标签和值写入数据流。自定义类型需要注册可用的数据流运算符；流版本和协议兼容由调用方设置。

#### `void load(QDataStream &ds)`

从数据流读取类型标签和值，替换当前内容。读取失败时应检查 `QDataStream::status()`；不要把不可信数据流当作已验证的类型和对象。

### 9.15 代理和指针访问

#### `T *get_if(QVariant *v) noexcept`

当 `v` 非空且当前类型与 `T` 精确匹配时返回可写指针，否则返回 `nullptr`。它不执行转换：

```cpp
if (UserId *id = get_if<UserId>(&value))
    id->value = 10;
```

返回指针在 variant 改变、分离或销毁后失效。

#### `const T *get_if(const QVariant *v) noexcept`

只读版本，同样只接受精确类型。`v == nullptr` 或类型不匹配时返回 `nullptr`。

#### `T &get(QVariant &v)`

精确类型访问，返回可写左值引用。调用方必须先确认类型精确匹配；它不是 `value<T>()` 的可写转换版本。

#### `const T &get(const QVariant &v)`

精确类型访问，返回 const 左值引用。类型不匹配时不能继续使用返回结果。

#### `T &&get(QVariant &&v)`

从右值 variant 取得精确类型的右值引用。源 variant 和返回引用之间存在生命周期约束，调用方应立即消费，不要跨越对源 variant 的其他操作。

#### `const T &&get(const QVariant &&v)`

const 右值访问，通常只在泛型代码转发值类别时使用。它不会执行转换。

#### `T qvariant_cast(const QVariant &v)`

返回 `value<T>()` 等价的值语义结果：精确类型直接取值，存在转换时尝试转换，失败返回默认构造值。

#### `T qvariant_cast(QVariant &&v)`

右值版本，精确匹配且条件允许时可能移动出值，否则执行拷贝或转换。

### 9.16 低层布局辅助入口

#### `QVariant::PrivateShared`

这是 Qt 内部管理共享存储的布局辅助类型。它的字段和静态函数不属于普通应用的值操作 API，不应自行创建、释放或依赖其布局。

#### `QVariant::Private`

这是 variant 内部表示，包含小对象内联存储、共享存储、类型信息和 null 标志。它暴露在头文件中主要服务于 Qt 实现和 ABI 机制，业务代码不应读写其位字段。

#### `using QVariant::DataPtr = Private`

兼容性别名，用于暴露内部数据表示。

#### `DataPtr &data_ptr()` 与 `const DataPtr &data_ptr() const`

返回内部表示引用。它不是对当前值的类型安全访问器；使用它会把代码绑定到 Qt 的内部布局，不推荐用于业务、插件 ABI 或持久化。

## 10. 旧式兼容 API

### 10.1 旧类型入口

以下 API 已弃用：

| 旧 API | 推荐替代 |
| --- | --- |
| `QVariant::Type` | `QMetaType::Type`、`metaType()` |
| `QVariant(Type type)` | `QVariant(QMetaType type, ...)` 或 `fromMetaType()` |
| `type()` | `typeId()` 或 `metaType()` |
| `typeToName(int)` | `QMetaType(typeId).name()` |
| `nameToType(const char *)` | `QMetaType::fromName(name)` |
| `canConvert(int)` | `canConvert(QMetaType)` |
| `convert(int)` | `convert(QMetaType)` |

不要使用旧枚举的数值判断自定义类型；`UserType` 只表示“用户类型起点”的兼容范围。

### 10.2 `QVariantRef`、`QVariantPointer` 和 `QVariantConstPointer`

这些是 Qt 6.15 起标为弃用的全局兼容代理，推荐使用 `QVariant::Reference`、`QVariant::Pointer` 和 `QVariant::ConstPointer`。如果旧代码仍在使用：

- `QVariantRef<Pointer>` 保存的是一个指向间接目标的地址；
- `QVariantPointer<Pointer>::operator*()` 返回 `QVariantRef`；
- `QVariantPointer::operator->()` 返回 `Pointer` 的代理访问；
- `QVariantConstPointer` 通过 `operator*()` 和 `operator->()` 提供只读 `QVariant` 访问。

它们都不是所有权管理工具，所指向的容器或间接对象必须在代理使用期间保持有效。

## 11. 非成员 API 和流运算符

### 11.1 `swap(QVariant &, QVariant &)`

非成员 `swap` 调用成员 `swap`，适合泛型代码和标准库算法。它只交换 variant 表示，不复制或转换内容。

### 11.2 `operator==` 与 `operator!=`

比较两个 variant 的值和类型语义。它不是简单比较 `typeId()`；相同或可比较的类型会按值比较，不可比较或部分有序值可能不能得到普通布尔总序。

需要排序时使用 `QVariant::compare()` 并处理 `QPartialOrdering::Unordered`，不要用 `operator<` 假设所有 QVariant 都能形成总序。

### 11.3 `QDataStream &operator<<(QDataStream &, const QVariant &)`

把 QVariant 类型标签和值写入数据流。写入自定义类型前，要确认其元类型和数据流操作符已经注册，并设置稳定的 `QDataStream` 版本。

### 11.4 `QDataStream &operator>>(QDataStream &, QVariant &)`

从数据流恢复 QVariant。对不可信输入应检查流状态和应用层允许的类型集合，不能仅因为 Qt 能读取类型标签就把数据视为安全业务对象。

### 11.5 `QDebug operator<<(QDebug, const QVariant &)`

在启用 debug stream 时输出 variant 的类型和值的调试表示。它不是稳定序列化格式，日志内容不应被程序解析。

## 12. 常见错误与排查顺序

### 12.1 用 `isNull()` 判断“有没有数据”

**问题：** 有效的 null 字符串、空指针和无效 variant 被混为一谈。

**修复：**

```cpp
if (!value.isValid()) {
    // 没有类型和值
} else if (value.isNull()) {
    // 有类型，但当前值处于 null 状态
}
```

### 12.2 忽略 `toInt(bool *ok)` 的成功标记

**问题：** `"bad"` 和 `"0"` 都可能读出 `0`。

**修复：** 对数值转换始终传 `bool *ok`，或先用明确格式验证。

### 12.3 把 `value<T>()` 的默认值当成成功结果

**问题：** 类型不匹配或转换失败时得到 `T{}`，调用方误以为真的存了一个默认值。

**修复：** 用 `metaType()` 做精确判断，或先检查 `canConvert<T>()`；需要无歧义结果时使用 `get_if<T>()`。

### 12.4 用 `get<T>()` 期待自动转换

**问题：** `get<int>(QVariant(QStringLiteral("1")))` 不会把字符串转换为整数。

**修复：** 用 `value<int>()`、`canConvert<int>()` 或显式 `convert()`。

### 12.5 保存 `data()` 指针后继续修改 QVariant

**问题：** 赋值、分离、转换或 `emplace()` 后旧指针悬空或指向旧值。

**修复：** 缩短指针使用范围，修改前后重新获取；不要把它保存到长期对象中。

### 12.6 把裸指针放进 QVariant 当成对象所有权

**问题：** QObject 被销毁后 variant 仍保存悬空地址。

**修复：** 使用 `QPointer`、共享指针或明确的 QObject 父子关系；需要传递裸指针时明确注明借用生命周期。

### 12.7 直接使用 `QVariant(QMetaType::Int)`

**问题：** 类型枚举可能被误读成一个整数值，Qt 已删除这类构造。

**修复：**

```cpp
QVariant value(QMetaType::fromType<int>());
```

### 12.8 直接把 Qt 枚举放进 QVariant

**问题：** `QVariant(Qt::red)` 可能选择整数构造，得到 `int` variant。

**修复：**

```cpp
QVariant value = QColor(Qt::red);
```

### 12.9 把 `view<T>()` 当成复制

**问题：** view 可能借用 variant 内部数据，源 variant 或内部容器变化后失效。

**修复：** 需要独立值时用 `value<T>()`；只有在能控制源生命周期时才保存 view。

### 12.10 把 QVariant 比较当成全序排序

**问题：** 不同类型、不可比较类型或 `Unordered` 值进入排序器。

**修复：** 先按业务定义类型优先级，再使用 `QVariant::compare()`，并处理 `QPartialOrdering::Unordered`。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `QVariant::Type` | Qt 5 兼容类型枚举 | Qt 6 已弃用，使用 `QMetaType` |
| 构造 | `QVariant()` | 创建无效 variant | `isValid()` 为 false |
| 构造 | `~QVariant()` | 销毁当前值 | 裸指针不会被 delete |
| 构造 | `QVariant(QMetaType, const void *)` | 按运行时类型默认/拷贝构造 | `copy` 必须同类型 |
| 构造 | `QVariant(const QVariant &)` | 拷贝值 | 可能隐式共享，写时分离 |
| 构造 | `QVariant(QVariant &&)` | 移动值 | 源对象可用但不保留原值 |
| 构造 | `QVariant(std::in_place_type_t<T>, ...)` | Qt 6.6 起原地构造 | `T` 要可拷贝、可析构 |
| 构造 | initializer-list `in_place` | Qt 6.6 起用列表原地构造 | 目标类型必须支持列表构造 |
| 构造 | `QVariant(int)` | 保存 `int` | 其他整数可能发生提升 |
| 构造 | `QVariant(uint)` | 保存 `uint` | 与有符号整数转换需明确 |
| 构造 | `QVariant(qlonglong)` | 保存有符号 64 位整数 | 读取时检查范围 |
| 构造 | `QVariant(qulonglong)` | 保存无符号 64 位整数 | 负数转换失败边界 |
| 构造 | `QVariant(bool)` | 保存布尔值 | 不要让指针隐式转 bool |
| 构造 | `QVariant(double)` | 保存双精度值 | 精度和 NaN 边界 |
| 构造 | `QVariant(float)` | 保存单精度值 | 可能发生精度损失 |
| 构造 | `QVariant(QChar)` | 保存 UTF-16 字符 | 不等于多字符字符串 |
| 构造 | `QVariant(QDate)` | 保存日期 | 无效日期仍可能是有效 variant |
| 构造 | `QVariant(QTime)` | 保存时间 | 检查结果有效性 |
| 构造 | `QVariant(QByteArray)` | 保存字节数组 | 不自动表示文本编码 |
| 构造 | `QVariant(QString)` | 保存字符串 | null 与 empty 可区分 |
| 构造 | `QVariant(QStringList)` | 保存字符串列表 | 列表值语义 |
| 构造 | `QVariant(QDateTime)` | 保存日期时间 | 注意时区 |
| 构造 | `QVariant(QBitArray)` | 保存位数组 | 不等同 QByteArray |
| 构造 | `QVariant(QHash<QString, QVariant>)` | 保存 QVariant hash | 共享/拷贝由容器决定 |
| 构造 | `QVariant(QMap<QString, QVariant>)` | 保存 QVariant map | 有序 map 与 hash 不同 |
| 构造 | `QVariant(QList<QVariant>)` | 保存 QVariant 列表 | 元素可异构 |
| 构造 | `QVariant(QJsonValue)` | 保存 JSON 值 | JSON 可表示范围有限 |
| 构造 | `QVariant(QJsonObject)` | 保存 JSON 对象 | 不是任意自定义对象 |
| 构造 | `QVariant(QJsonArray)` | 保存 JSON 数组 | 元素需符合 JSON 语义 |
| 构造 | `QVariant(QJsonDocument)` | 保存 JSON 文档 | 文档有效性独立检查 |
| 构造 | `QVariant(QRegularExpression)` | 保存正则表达式 | 受模块配置影响 |
| 构造 | `QVariant(QLocale)` | 保存 locale | 不等于全局 locale |
| 构造 | `QVariant(QUrl)` | 保存 URL | 检查 `isValid()` |
| 构造 | `QVariant(QUuid)` | 保存 UUID | null UUID 仍有类型 |
| 构造 | `QVariant(QPoint/QPointF)` | 保存点 | 整数与浮点类型不同 |
| 构造 | `QVariant(QRect/QRectF)` | 保存矩形 | 整数与浮点类型不同 |
| 构造 | `QVariant(QSize/QSizeF)` | 保存尺寸 | 检查负尺寸语义 |
| 构造 | `QVariant(QLine/QLineF)` | 保存线段 | 整数与浮点类型不同 |
| 构造 | `QVariant(QModelIndex)` | 保存模型索引 | 检查索引有效性 |
| 构造 | `QVariant(QPersistentModelIndex)` | 保存持久索引 | 模型生命周期仍重要 |
| 构造 | `QVariant(const char *)` | UTF-8 转 QString | 空指针和编码需明确 |
| 构造 | `QVariant(QLatin1StringView)` | Latin-1 转 QString | 保存的是转换后的拥有值 |
| 代理 | `Reference<Indirect>` | 可写间接代理 | 不是原生 `T &` |
| 代理 | `ConstReference<Indirect>` | 只读间接代理 | 不能赋值，转 QVariant 是值语义 |
| 代理 | `Pointer<Indirect>` | 可写代理指针 | `operator*` 返回 Reference |
| 代理 | `ConstPointer<Indirect>` | 只读代理指针 | `operator*` 返回 ConstReference |
| 赋值 | `operator=(const QVariant &)` | 拷贝赋值 | 旧值被替换 |
| 赋值 | `operator=(QVariant &&)` | 移动赋值 | 源值不再可依赖 |
| 交换 | `swap(QVariant &)` | 交换内部表示 | 不做类型转换 |
| 状态 | `typeId()` | 返回当前类型 ID | 无效为 0 |
| 状态 | `userType()` | `typeId()` 的兼容别名 | 名称有 user 但也返回内置类型 |
| 状态 | `typeName()` | 返回类型名称 | 非拥有字符串 |
| 状态 | `metaType()` | 返回 `QMetaType` | Qt 6 推荐类型判断入口 |
| 状态 | `isValid()` | 判断是否有有效值类型 | 默认/clear 后 false |
| 状态 | `isNull()` | 判断当前值是否 null | 不等于无效 |
| 共享 | `detach()` | 强制独占存储 | 可能复制数据 |
| 共享 | `isDetached()` | 查询是否独占 | 不作为性能契约 |
| 转换 | `canConvert<T>()` | 查询到 T 的转换路径 | 不保证具体值成功 |
| 转换 | `canConvert(QMetaType)` | 运行时查询转换路径 | 目标类型应有效 |
| 转换 | `convert(QMetaType)` | 原地转换当前值 | 成功后类型改变 |
| view | `canView<T>()` | 查询 T view 能力 | view 通常借用源存储 |
| view | `canView(QMetaType)` | 运行时查询 view | 不延长生命周期 |
| view | `view<T>()` | 返回 T 类型 view | 先检查 canView |
| raw | `data()` | 可写 raw 地址 | 可能分离；地址会失效 |
| raw | `constData()` | 只读 raw 地址 | 不触发分离 |
| raw | `data() const` | constData 别名 | 不可写 |
| 构造 | `emplace<T>(args...)` | Qt 6.6 起原地构造 | 旧引用/pointer/view 失效 |
| 构造 | `emplace<T>(initializer_list, ...)` | Qt 6.6 起列表原地构造 | T 需满足 QVariant 值语义 |
| 赋值 | `setValue(const QVariant &)` | 复制 variant 值 | 等价拷贝赋值语义 |
| 赋值 | `setValue(QVariant &&)` | 移动 variant 值 | 源被移动 |
| 赋值 | `setValue(T &&)` | 设置自定义或内置值 | T 需适合 QVariant |
| 读取 | `value<T>() const &` | 精确取值或转换 | 失败返回 T{} |
| 读取 | `value<T>() &&` | 右值取值，可能移动 | 不保证零拷贝 |
| 创建 | `fromValue(const T &)` | 复制 T 到 variant | T 需可拷贝、可析构 |
| 创建 | `fromValue(T &&)` | Qt 6.6 起移动 T | 移动后源值不应依赖 |
| 创建 | `fromMetaType(type, copy)` | Qt 6.7 起按描述创建 | 检查返回值有效性 |
| 创建 | `fromStdVariant(const std::variant &)` | 保存当前分支值 | valueless 分支变无效 |
| 创建 | `fromStdVariant(std::variant &&)` | Qt 6.6 起移动当前分支 | 仍需 QVariant 值语义 |
| 数值 | `toInt(bool *)` | 转 int | 必须检查 ok |
| 数值 | `toUInt(bool *)` | 转 uint | 必须检查 ok |
| 数值 | `toLongLong(bool *)` | 转 qlonglong | 必须检查 ok |
| 数值 | `toULongLong(bool *)` | 转 qulonglong | 必须检查 ok |
| 数值 | `toBool()` | 转 bool | 没有 ok 标记 |
| 数值 | `toDouble(bool *)` | 转 double | 必须检查 ok |
| 数值 | `toFloat(bool *)` | 转 float | 精度/范围边界 |
| 数值 | `toReal(bool *)` | 转 qreal | 平台相关 |
| 值 | `toByteArray()` | 转 QByteArray | 文本编码需明确 |
| 值 | `toBitArray()` | 转 QBitArray | 类型语义不同 |
| 值 | `toString()` | 转 QString | 不是稳定序列化 |
| 值 | `toStringList()` | 转 QStringList | 检查转换语义 |
| 值 | `toChar()` | 转 QChar | 单字符边界 |
| 值 | `toDate()` / `toTime()` | 转日期/时间 | 检查结果有效性 |
| 值 | `toDateTime()` | 转日期时间 | 注意时区 |
| 容器 | `toList()` | 转 QVariant 列表 | 可能复制/转换 |
| 容器 | `toMap()` | 转 QVariant map | 字符串键语义 |
| 容器 | `toHash()` | 转 QVariant hash | 顺序不同 |
| 几何 | `toPoint()` / `toPointF()` | 转点 | 整数/浮点不同 |
| 几何 | `toRect()` / `toRectF()` | 转矩形 | 整数/浮点不同 |
| 几何 | `toSize()` / `toSizeF()` | 转尺寸 | 检查有效性 |
| 几何 | `toLine()` / `toLineF()` | 转线段 | 整数/浮点不同 |
| 其他 | `toLocale()` | 转 locale | 与全局 locale 无关 |
| 其他 | `toRegularExpression()` | 转正则 | 检查正则有效性 |
| 其他 | `toEasingCurve()` | 转缓动曲线 | 受配置影响 |
| 其他 | `toUuid()` | 转 UUID | 检查 null UUID |
| 其他 | `toUrl()` | 转 URL | 检查 `isValid()` |
| JSON | `toJsonValue()` | 转 JSON 值 | 自定义类型不可任意映射 |
| JSON | `toJsonObject()` | 转 JSON 对象 | 失败时为空/无效 |
| JSON | `toJsonArray()` | 转 JSON 数组 | 需符合 JSON 语义 |
| JSON | `toJsonDocument()` | 转 JSON 文档 | 检查文档有效性 |
| 模型 | `toModelIndex()` | 转模型索引 | 检查 `isValid()` |
| 模型 | `toPersistentModelIndex()` | 转持久索引 | 依赖模型生命周期 |
| 数据流 | `save(QDataStream &)` | 写入类型和值 | 检查流和类型注册 |
| 数据流 | `load(QDataStream &)` | 读取类型和值 | 检查流状态和输入来源 |
| 比较 | `compare(lhs, rhs)` | 返回部分序关系 | 处理 Unordered |
| 访问 | `get_if<T>(QVariant *)` | 精确类型指针访问 | 失败返回 nullptr，不转换 |
| 访问 | `get<T>(QVariant &)` | 精确类型引用访问 | 先确保类型匹配 |
| 访问 | `qvariant_cast<T>()` | 值读取/转换 | 失败返回默认值 |
| 兼容 | `QVariant::Type`、`type()` | Qt 5 类型兼容 | 新代码不要使用 |
| 兼容 | `QVariantRef` 等 | 旧代理类型 | 使用嵌套新代理替代 |
| 内部 | `data_ptr()` | 暴露内部表示 | 不要绑定实现布局 |

## 14. 推荐模板

### 14.1 精确读取自定义值

```cpp
std::optional<UserId> readUserId(const QVariant &value)
{
    if (value.metaType() != QMetaType::fromType<UserId>())
        return std::nullopt;

    if (const UserId *id = get_if<UserId>(&value))
        return *id;

    return std::nullopt;
}
```

### 14.2 可靠的数值转换

```cpp
std::optional<int> readInt(const QVariant &value)
{
    if (!value.canConvert<int>())
        return std::nullopt;

    bool ok = false;
    const int result = value.toInt(&ok);
    if (!ok)
        return std::nullopt;

    return result;
}
```

### 14.3 从运行时类型创建 variant

```cpp
QVariant makeDefaultValue(QMetaType type)
{
    if (!type.isValid() || !type.isDefaultConstructible())
        return {};

    return QVariant::fromMetaType(type);
}
```

### 14.4 安全地使用 view

```cpp
QByteArrayView asBytes(QVariant &value)
{
    const QMetaType target = QMetaType::fromType<QByteArrayView>();
    if (!value.canView(target))
        return {};

    return value.view<QByteArrayView>();
}
```

调用方必须保证 `value` 和其内部字节存储在返回的 `QByteArrayView` 使用期间不被替换、分离或销毁。

## 15. 一句话总结

`QVariant` 是一个按值拥有、按 `QMetaType` 描述的运行时值容器：用 `fromValue/value` 做普通值传递，用 `get/get_if` 做精确无转换访问，用 `canConvert/convert` 做可检查转换，用 `emplace` 做原地构造，用 `view` 做受生命周期约束的借用访问；最重要的是始终区分无效、null、转换失败、共享分离和裸指针所有权。

## 16. 核对依据

- Qt 6.11.1 本机头文件：`C:\Qt\6.11.1\msvc2022_64\include\QtCore\qvariant.h`
- [Qt 6 QVariant 文档](https://doc.qt.io/qt-6/qvariant.html)
- [Qt 6 QMetaType 文档](https://doc.qt.io/qt-6/qmetatype.html)
