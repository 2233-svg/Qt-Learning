# Qt QMetaProperty 属性反射、读写与绑定笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMetaProperty>`  
> 所属模块：`Qt6::Core`  
> 类型性质：`QMetaObject` 中一条 `Q_PROPERTY` 描述的轻量句柄  
> 相关类型：`QMetaObject`、`QObject`、`Q_GADGET`、`QVariant`、`QMetaEnum`、`QMetaMethod`、`QUntypedBindable`

## 1. 它解决什么问题

普通 C++ 代码可以直接调用 getter、setter 和 reset 函数，但通用工具并不知道一个类有哪些属性、属性是什么类型、是否可写、是否有通知信号。`QMetaProperty` 把 `Q_PROPERTY` 声明暴露给元对象系统，支持：

- 按名称或索引发现属性；
- 查询属性类型、读写能力、设计器/脚本/存储标志；
- 通过 `QVariant` 读取和写入 `QObject` 属性；
- 访问 `Q_GADGET` 属性；
- 取得枚举属性对应的 `QMetaEnum`；
- 取得 notify signal；
- 取得 Qt 6 属性绑定的无类型入口；
- 识别 required、constant、final、virtual、override 等元数据。

它不是属性值本身，也不是一个通用的动态字典。`QMetaProperty` 只描述“如何访问某个类型的属性”，实际值仍然存储在目标 `QObject` 或 gadget 实例中。

## 2. 实际使用场景

### 2.1 通用属性编辑器

```cpp
void dumpProperties(QObject *object)
{
    const QMetaObject *meta = object->metaObject();
    for (int i = 0; i < meta->propertyCount(); ++i) {
        const QMetaProperty property = meta->property(i);
        if (!property.isReadable())
            continue;

        const QVariant value = property.read(object);
        qDebug().noquote()
            << property.name()
            << '=' << value;
    }
}
```

属性编辑器应同时检查 `isReadable()` 和 `isWritable()`。`property()` 返回一个描述句柄，不会因为属性不可读而抛出异常；读写失败主要通过无效 `QVariant` 或 `false` 返回值表达。

### 2.2 按名称读写属性

```cpp
const int index =
    object->metaObject()->indexOfProperty("enabled");
if (index >= 0) {
    const QMetaProperty property =
        object->metaObject()->property(index);

    if (property.isWritable()) {
        const bool accepted =
            property.write(object, true);
        Q_ASSERT(accepted);
    }
}
```

`isWritable()` 只是元数据能力检查，真正写入仍可能因为对象类型、值类型转换、只读约束或 setter 内部拒绝而失败。

### 2.3 发现枚举属性的可选值

```cpp
if (property.isEnumType()) {
    const QMetaEnum metaEnum = property.enumerator();
    for (int i = 0; i < metaEnum.keyCount(); ++i)
        qDebug() << metaEnum.key(i);
}
```

`isEnumType()` 为 true 时，`enumerator()` 才有业务意义。枚举属性的 `QVariant` 仍可能需要按属性的 `QMetaType` 读写，不要只把 key 文本直接当作最终值。

### 2.4 根据 notify signal 监听属性变化

```cpp
if (property.hasNotifySignal()) {
    const QMetaMethod signal = property.notifySignal();
    QObject::connect(object, signal, observer,
                     &Observer::propertyChanged);
}
```

实际回调签名必须和 notify signal 参数兼容。很多属性变化信号带一个新值，也有不带参数的 notify signal；不能假定所有属性通知都是 `void changed(T)`。

### 2.5 访问 `Q_GADGET` 属性

```cpp
class SizeValue
{
    Q_GADGET
    Q_PROPERTY(int width MEMBER m_width)
public:
    int m_width = 0;
};

SizeValue value;
const QMetaProperty property =
    SizeValue::staticMetaObject.property(
        SizeValue::staticMetaObject.indexOfProperty("width"));

const QVariant width = property.readOnGadget(&value);
property.writeOnGadget(&value, 42);
```

gadget API 使用 `void *`，不会在运行时验证对象的 C++ 类型。只能把与该属性所属 `QMetaObject` 匹配的实例地址传入。

## 3. `Q_PROPERTY` 与 `QMetaProperty`

### 3.1 READ/WRITE/RESET 形式

```cpp
class Document : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString title
               READ title
               WRITE setTitle
               RESET resetTitle
               NOTIFY titleChanged)
public:
    QString title() const;
    void setTitle(const QString &title);
    void resetTitle();

signals:
    void titleChanged(const QString &title);
};
```

这些关键字决定 `QMetaProperty` 的能力位：

- 有 `READ` 或适用 `MEMBER` 时通常可读；
- 有 `WRITE` 或适用可写 `MEMBER` 时通常可写；
- 有 `RESET` 时 `isResettable()` 为 true；
- 有 `NOTIFY` 时 `hasNotifySignal()` 为 true；
- `CONSTANT`、`FINAL`、`REQUIRED`、`DESIGNABLE`、`SCRIPTABLE`、`STORED`、`USER` 等会反映到对应查询函数。

属性声明进入元对象需要 `Q_OBJECT` 或适用的 `Q_GADGET`，并经过 moc。普通成员变量不因名字像属性就自动成为 `QMetaProperty`。

### 3.2 MEMBER 属性

```cpp
class Item : public QObject
{
    Q_OBJECT
    Q_PROPERTY(int count MEMBER m_count NOTIFY countChanged)
public:
    int m_count = 0;

signals:
    void countChanged();
};
```

`MEMBER` 让元对象直接访问成员。它可以提供读写能力，但业务仍需遵守封装和通知约定：直接通过反射写入成员时，是否发出 notify signal 取决于 Qt 属性系统和声明方式，不应把任意写入都当成业务 setter 的完整逻辑。

### 3.3 BINDABLE 属性

```cpp
class Settings : public QObject
{
    Q_OBJECT
    Q_PROPERTY(int level READ level
               BINDABLE bindableLevel)
public:
    QBindable<int> bindableLevel();
    int level() const;
};
```

`isBindable()` 只说明属性提供绑定接口；`bindable(object)` 返回的是类型擦除的 `QUntypedBindable`。它不是当前属性值，也不是可以随意跨对象保存的独立 binding。使用时需要让 object 和 property 描述匹配。

## 4. 属性索引、继承和所有权

### 4.1 全局索引与相对索引

- `propertyIndex()`：属性在所属元对象可见属性表中的索引；
- `relativePropertyIndex()`：属性在直接声明该属性的类中的相对索引；
- `propertyOffset()`：当前类自有属性的起点；
- `propertyCount()`：当前元对象可见属性总数。

遍历某个类自己声明的属性：

```cpp
const QMetaObject *meta = object->metaObject();
for (int i = meta->propertyOffset();
     i < meta->propertyCount(); ++i) {
    const QMetaProperty property = meta->property(i);
    // 只处理当前类新增的属性
}
```

若要包含基类，沿着 `superClass()` 逐层处理。不要把 `relativePropertyIndex()` 直接传给 `property()`，除非已经加上正确的 offset。

### 4.2 描述句柄不拥有目标对象

```cpp
const QMetaProperty property = meta->property(index);
```

复制 property 只复制元对象描述句柄，不复制属性值、不拥有 object，也不延长动态库或 gadget 类型的生命周期。

### 4.3 `enclosingMetaObject()`

这个 API 返回声明该属性的元对象。它不是当前传入 `read()`/`write()` 的对象，也不一定等于动态类型的最派生元对象。

## 5. 读写、转换与失败判断

### 5.1 `read()` 返回 `QVariant`

```cpp
const QVariant value = property.read(object);
if (!value.isValid()) {
    // 属性不可读、对象类型不匹配或读取失败
}
```

无效 `QVariant` 是重要失败信号。合法的属性值也可能是空值或包含 null 的 QVariant，因此要区分 `isValid()` 与 `isNull()`。

### 5.2 `write()` 的 QVariant 转换

```cpp
if (!property.write(object, QVariant::fromValue(newValue)))
    qWarning() << "property write failed";
```

Qt 可能执行允许的 QVariant 类型转换，但不是任意 C++ 转换都可用。写入失败时返回 false；不要因为 `QVariant` 构造成功就认为属性已更新。

Qt 6.6 起还有 `QVariant &&` 重载，可减少不必要的临时值复制：

```cpp
property.write(object, QVariant(QStringLiteral("new title")));
```

### 5.3 `reset()` 不是写入默认值的通用替代

只有声明了 `RESET` 的属性才能可靠调用 `reset()`。reset 的实际默认值和副作用由类型实现决定；它可能发出 notify signal，也可能执行额外业务逻辑。

### 5.4 目标对象必须匹配属性所属类型

`read()`、`write()` 和 `reset()` 传入的 QObject 必须是该属性声明类的实例或其派生类实例。把另一个无关 QObject 的地址传入属于 API 使用错误，不能只依赖返回 false 来保护。

## 6. 属性标志的实际语义

### 6.1 读写与 reset

| 查询 | 表示 |
| --- | --- |
| `isReadable()` | 元对象记录有可读访问路径 |
| `isWritable()` | 元对象记录有可写访问路径 |
| `isResettable()` | 元对象记录有 reset 路径 |

这些函数是能力查询，不是对 getter/setter 内部业务状态的保证。setter 可能仍拒绝某个值。

### 6.2 设计器、脚本和存储标志

- `isDesignable()`：属性是否应显示为可设计属性，可能由静态值或设计器函数决定；
- `isScriptable()`：属性是否标记为可脚本访问；
- `isStored()`：属性是否应作为对象持久化状态保存；
- `isUser()`：属性是否是类的用户主属性。

这些标志主要服务于 Designer、表单编辑器、序列化工具和脚本环境，不会自动改变 C++ 读写权限。

### 6.3 常量、最终、虚拟和 override

- `isConstant()`：属性值在对象生命周期内不应通过写入改变；
- `isFinal()`：属性不应在派生元对象中重新定义；
- `isVirtual()`：元对象将其标记为可虚拟重写的属性访问语义；
- `isOverride()`：该属性在元对象层级中标记为覆盖基类属性。

这些是元对象契约。它们不等价于把所有相关 C++ getter/setter 自动改成虚函数，也不替代 C++ 编译器对访问和重写的检查。

### 6.4 `isRequired()`

`isRequired()` 表示属性被声明为 required，通常用于 QML/组件初始化契约。它不是 C++ 构造函数参数，也不会自动在 QObject 构造时检查属性已经赋值。

### 6.5 `isBindable()`

`isBindable()` 表示可以通过 `BINDABLE` 访问响应式绑定接口。没有 bindable 的属性仍然可以有传统 `NOTIFY` 信号；这两个能力不要混为一谈。

## 7. 枚举属性、通知信号和绑定

### 7.1 `isEnumType()` 与 `isFlagType()`

`isEnumType()` 表示属性类型对应一个枚举；`isFlagType()` 表示它是 Flags。两者影响 `enumerator()` 的解释：

```cpp
const QMetaEnum enumerator = property.enumerator();
if (property.isFlagType()) {
    // 使用 valueToKeys()/keysToValue() 处理组合值
}
```

如果属性类型是一个普通整数，但业务约定它的值像枚举，元对象不会自动把它当作枚举。

### 7.2 `notifySignal()` 的句柄生命周期

`notifySignal()` 返回 `QMetaMethod`。没有 notify signal 时，它通常是无效句柄；先检查 `hasNotifySignal()` 或 `isValid()`。

notify signal 必须属于与 property 兼容的元对象。连接时还需要回调参数兼容，不能只因为它是 notify signal 就连接到任意槽。

### 7.3 `notifySignalIndex()`

返回 notify signal 在所属元对象方法表中的索引。没有 notify signal 时通常为 `-1`。这个索引是元对象内部索引，不是信号的业务 ID。

## 8. gadget 和 QObject API 的边界

### 8.1 QObject 属性

```cpp
QVariant read(const QObject *object) const;
bool write(QObject *object, const QVariant &value) const;
bool reset(QObject *object) const;
```

这些函数可以利用 QObject 的元调用和对象生命周期，但不替代线程安全。GUI 对象仍应在所属线程操作。

### 8.2 gadget 属性

```cpp
QVariant readOnGadget(const void *gadget) const;
bool writeOnGadget(void *gadget, const QVariant &value) const;
bool resetOnGadget(void *gadget) const;
```

gadget 不继承 QObject，没有对象树、线程归属和信号槽连接。`readOnGadget()` 接受 const 地址，写入和 reset 需要可写地址。

### 8.3 不要混用两组 API

不能把 gadget 地址传给 `read()`，也不能把 QObject 地址传给 `readOnGadget()`。两组 API 的 `void *`/`QObject *` 差异正是类型边界的一部分。

## 9. 逐项 API 说明

### 9.1 `QMetaProperty()`

```cpp
constexpr QMetaProperty();
```

构造无效属性句柄。默认构造对象不绑定任何元对象和属性。

### 9.2 `bindable(QObject *) const`

```cpp
QUntypedBindable bindable(QObject *object) const;
```

Qt 6.0 引入。返回属性的无类型绑定入口。调用前应确认 `isBindable()`，并传入拥有该属性的正确 QObject 实例。返回对象不应被理解成属性值或自动延长 object 生命周期。

### 9.3 `enclosingMetaObject() const`

```cpp
const QMetaObject *enclosingMetaObject() const;
```

返回保存该属性描述的元对象。无效属性可能返回 `nullptr`。

### 9.4 `enumerator() const`

```cpp
QMetaEnum enumerator() const;
```

返回属性关联的枚举描述。只有 `isEnumType()` 或 `isFlagType()` 为 true 时才应依赖它；普通属性可能返回无效的 `QMetaEnum`。

### 9.5 `hasNotifySignal() const`

```cpp
bool hasNotifySignal() const;
```

判断属性是否声明了 notify signal。它只说明元对象有通知入口，不保证某次 setter 调用一定发出信号。

### 9.6 `hasStdCppSet() const`

```cpp
bool hasStdCppSet() const;
```

报告元对象是否记录了符合标准 C++ setter 命名约定的 setter。它用于工具和属性系统判断 setter 形态，不等价于 `isWritable()`，也不意味着 setter 对所有 QVariant 输入都接受。

### 9.7 `isAlias() const`

```cpp
bool isAlias() const;
```

报告该元属性是否被元对象标记为 alias。这个标志主要与 QML/动态元对象属性体系协作；普通 C++ `Q_PROPERTY` 不应默认假设为 alias。

### 9.8 `isBindable() const`

```cpp
bool isBindable() const;
```

判断属性是否有 `BINDABLE` 入口。为 false 时不要调用 `bindable()` 期待得到有效绑定接口。

### 9.9 `isConstant() const`

```cpp
bool isConstant() const;
```

判断属性是否声明为 constant。constant 属性通常没有可写路径，也不应依赖运行时变化通知。

### 9.10 `isDesignable() const`

```cpp
bool isDesignable() const;
```

判断属性是否面向设计器暴露。设计器可见性不等于运行时可写性。

### 9.11 `isEnumType() const`

```cpp
bool isEnumType() const;
```

判断属性类型是否为枚举类型。为 true 时可用 `enumerator()` 查询 key/value。

### 9.12 `isFinal() const`

```cpp
bool isFinal() const;
```

判断属性是否标记为 final。它描述元对象继承层级的重新声明约束，不是 QObject 实例的运行时状态。

### 9.13 `isFlagType() const`

```cpp
bool isFlagType() const;
```

判断属性是否为 Flags 类型。组合值应按位处理，并使用关联 `QMetaEnum` 的 `valueToKeys()` 等 API。

### 9.14 `isOverride() const`

```cpp
bool isOverride() const;
```

Qt 6.11 引入。查询属性是否被元对象标记为 override。它是属性反射层的覆盖关系信息，不应替代编译器对 C++ override 的诊断。

### 9.15 `isReadable() const`

```cpp
bool isReadable() const;
```

判断是否存在元对象可用的读取路径。若为 false，不应调用 `read()` 并把无效 QVariant 当成合法值。

### 9.16 `isRequired() const`

```cpp
bool isRequired() const;
```

判断属性是否标记为 required。它通常由 QML/组件工具消费，不会自动改造 C++ 构造过程。

### 9.17 `isResettable() const`

```cpp
bool isResettable() const;
```

判断是否声明了 reset 函数。只有为 true 时，调用 `reset()` 才有明确的元对象契约。

### 9.18 `isScriptable() const`

```cpp
bool isScriptable() const;
```

判断属性是否标记为可脚本访问。它是工具元数据，不是安全沙箱或权限系统。

### 9.19 `isStored() const`

```cpp
bool isStored() const;
```

判断属性是否应视为可存储状态。序列化工具可以据此筛选属性，但最终格式、版本和默认值仍由工具决定。

### 9.20 `isUser() const`

```cpp
bool isUser() const;
```

判断属性是否为类的 user property。它通常供表单、编辑器或通用 UI 工具选择默认编辑属性。

### 9.21 `isValid() const`

```cpp
bool isValid() const;
```

判断属性句柄是否有效。Qt 6.11 头文件中它等价于 `isReadable()`；因此不可读的属性可能被报告为无效，通用代码仍应分别检查读写能力。

### 9.22 `isVirtual() const`

```cpp
bool isVirtual() const;
```

Qt 6.11 引入。查询元属性是否标记为 virtual。它描述 Qt 元对象属性访问语义，不能简单等同于 getter/setter 都是 C++ virtual 函数。

### 9.23 `isWritable() const`

```cpp
bool isWritable() const;
```

判断是否存在元对象可用的写入路径。它不保证给定 QVariant 一定可转换，也不保证 setter 内部业务校验会接受。

### 9.24 `metaType() const`

```cpp
QMetaType metaType() const;
```

Qt 6.0 引入。返回属性值类型的 `QMetaType`。它比 `typeName()` 更适合做类型能力判断、构造 QVariant 和比较类型。

### 9.25 `name() const`

```cpp
const char *name() const;
```

返回属性名称。指针由元对象拥有，不应修改或跨动态库卸载保存。

### 9.26 `notifySignal() const`

```cpp
QMetaMethod notifySignal() const;
```

返回 notify signal 的方法句柄。没有通知信号时通常返回无效方法；先检查 `hasNotifySignal()`。

### 9.27 `notifySignalIndex() const`

```cpp
int notifySignalIndex() const;
```

返回 notify signal 的方法表索引；没有通知信号时通常为 `-1`。索引只在所属元对象中有意义。

### 9.28 `propertyIndex() const`

```cpp
int propertyIndex() const;
```

返回属性在完整元属性表中的索引。它可传回所属 `QMetaObject::property(index)`，但不能跨类型当作稳定编号。

### 9.29 `read(const QObject *) const`

```cpp
QVariant read(const QObject *object) const;
```

读取 QObject 实例的属性值。属性不可读、对象类型不匹配或调用失败时可能返回无效 `QVariant`。读取不会转移 object 所有权。

### 9.30 `readOnGadget(const void *) const`

```cpp
QVariant readOnGadget(const void *gadget) const;
```

读取 gadget 实例的属性。指针必须指向正确类型的 gadget，且 gadget 在调用期间保持存活。

### 9.31 `relativePropertyIndex() const`

```cpp
int relativePropertyIndex() const;
```

返回属性在直接声明类中的相对索引。处理继承元对象时要结合 `propertyOffset()` 使用。

### 9.32 `reset(QObject *) const`

```cpp
bool reset(QObject *object) const;
```

调用 QObject 属性的 RESET 函数。没有 reset 能力、对象不匹配或 reset 执行失败时返回 false。

### 9.33 `resetOnGadget(void *) const`

```cpp
bool resetOnGadget(void *gadget) const;
```

调用 gadget 属性的 RESET 访问路径。只有可写 gadget 地址和正确属性描述才可使用。

### 9.34 `revision() const`

```cpp
int revision() const;
```

返回属性的 revision 元数据，常用于 QML、版本化接口和工具兼容性判断。它不是属性变更次数。

### 9.35 `type() const`

```cpp
QVariant::Type type() const;
```

Qt 6.0 起已弃用的旧 API。它把属性类型压缩到 `QVariant::Type`，无法完整表达现代 `QMetaType`。新代码使用 `metaType()` 或 `typeId()`。

### 9.36 `typeId() const`

```cpp
int typeId() const;
```

返回属性 `QMetaType` 的整数 ID。它是兼容旧 API 的数值入口；需要完整能力时保留 `QMetaType` 对象更合适。

### 9.37 `typeName() const`

```cpp
const char *typeName() const;
```

返回属性类型名称的非拥有字符串。适合显示和诊断，不应用文本比较替代 `QMetaType` 判断。

### 9.38 `userType() const`

```cpp
int userType() const;
```

在 Qt 6.11 头文件中它等价于 `typeId()`。保留这个名称主要是历史兼容；新代码优先使用 `metaType()` 或 `typeId()`。

### 9.39 `write(QObject *, const QVariant &) const`

```cpp
bool write(QObject *object, const QVariant &value) const;
```

通过 QVariant 写入 QObject 属性。返回 true 表示 Qt 接受并完成了写入路径，false 表示属性不可写、对象不匹配、类型无法转换或 setter 拒绝。

### 9.40 `write(QObject *, QVariant &&) const`

```cpp
bool write(QObject *object, QVariant &&value) const;
```

Qt 6.6 引入的移动值重载。它允许 Qt 在适用时复用 QVariant 的存储，但不改变写入失败语义；仍需检查返回值。

### 9.41 `writeOnGadget(void *, const QVariant &) const`

```cpp
bool writeOnGadget(void *gadget,
                   const QVariant &value) const;
```

通过 QVariant 写入 gadget 属性。gadget 地址必须可写且类型匹配。

### 9.42 `writeOnGadget(void *, QVariant &&) const`

```cpp
bool writeOnGadget(void *gadget,
                   QVariant &&value) const;
```

Qt 6.6 引入的 gadget 移动值重载。它只优化 QVariant 传递方式，不会降低 gadget 指针和属性类型匹配要求。

## 10. 常见错误

### 10.1 把属性描述当成属性值

**症状：** 保存一个 `QMetaProperty` 后，以为它包含某个对象当前值。

**原因：** property 是元对象句柄，不保存实例数据。

**修复：** 在目标 object 上调用 `read()`，需要持久化时复制 `QVariant`。

### 10.2 忽略 `isWritable()` 和 `write()` 返回值

**症状：** UI 显示写入成功，但对象状态没有变化。

**原因：** 属性只读、类型无法转换或 setter 拒绝。

**修复：** 先检查能力，再检查 `write()` 的 bool 结果，并记录实际类型。

### 10.3 把 `isReadable()` 当作“永远可读”

**症状：** `read()` 返回无效 QVariant。

**原因：** object 类型不匹配、目标已销毁或属性访问在当前状态失败。

**修复：** 验证 object 类型和生命周期，并检查 QVariant 的 `isValid()`。

### 10.4 用错误的 API 访问 gadget

**症状：** 读取异常、写入错误内存或行为未定义。

**原因：** gadget 与 QObject API 混用，或者 `void *` 指向错误类型。

**修复：** gadget 只使用 `readOnGadget()`/`writeOnGadget()`/`resetOnGadget()`，并确保地址类型匹配。

### 10.5 把 `hasNotifySignal()` 当成每次写入都发信号

**症状：** 监听器没有收到预期变化通知。

**原因：** notify signal 只是可用的通知入口；setter 可能在值未变化时不发信号，也可能业务实现没有正确发射。

**修复：** 检查 setter 的通知契约，不要只依赖 property 元数据。

### 10.6 用 `typeName()` 判断类型

**症状：** typedef、命名空间或跨模块类型比较失败。

**原因：**类型文本不是完整的类型身份判断。

**修复：** 使用 `metaType()`、`typeId()` 和适用的 `QMetaType` 比较。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QMetaProperty()` | 构造无效属性句柄 | 不绑定 object 或属性值 |
| `bindable(QObject *)` | 取得属性的无类型绑定入口 | Qt 6.0 起；先检查 `isBindable()`，object 必须匹配 |
| `enclosingMetaObject()` | 返回所属元对象 | 不拥有 object；动态库卸载后不要继续使用 |
| `enumerator()` | 返回关联枚举描述 | 仅对 `isEnumType()`/`isFlagType()` 有意义 |
| `hasNotifySignal()` | 查询是否有 notify signal | 不保证每次写入都发射 |
| `hasStdCppSet()` | 查询是否有标准命名 setter | 不等于属性可写或值一定接受 |
| `isAlias()` | 查询元属性 alias 标记 | 主要服务 QML/动态元对象 |
| `isBindable()` | 查询是否支持 BINDABLE | 与传统 NOTIFY 独立 |
| `isConstant()` | 查询 constant 标志 | 通常不应依赖运行时写入 |
| `isDesignable()` | 查询设计器可见标志 | 不等于运行时可写 |
| `isEnumType()` | 查询是否枚举类型 | 可配合 `enumerator()` |
| `isFinal()` | 查询 final 标志 | 是元对象继承约束，不是实例状态 |
| `isFlagType()` | 查询是否 Flags 类型 | 组合值按位处理 |
| `isOverride()` | 查询 override 标志 | Qt 6.11 起；不替代 C++ override 检查 |
| `isReadable()` | 查询元对象读取能力 | 仍需检查 `read()` 返回值 |
| `isRequired()` | 查询 required 标志 | 不自动改变 C++ 构造流程 |
| `isResettable()` | 查询是否有 RESET | 只有为 true 才应调用 reset |
| `isScriptable()` | 查询脚本可见标志 | 不是安全权限控制 |
| `isStored()` | 查询是否应视作存储属性 | 序列化工具仍需定义格式 |
| `isUser()` | 查询 user property 标志 | 常供编辑器选择主属性 |
| `isValid()` | 查询句柄是否有效 | Qt 6.11 中等价于 `isReadable()` |
| `isVirtual()` | 查询 virtual 元属性标志 | Qt 6.11 起；不等同于所有访问器是 C++ virtual |
| `isWritable()` | 查询元对象写入能力 | 仍需检查 QVariant 转换和 setter 结果 |
| `metaType()` | 返回属性值的 `QMetaType` | 现代类型判断优先使用它 |
| `name()` | 返回属性名 | 非拥有 `const char *` |
| `notifySignal()` | 返回 notify signal 描述 | 没有通知时通常无效 |
| `notifySignalIndex()` | 返回 notify signal 方法索引 | 无通知时通常为 `-1` |
| `propertyIndex()` | 返回完整属性表索引 | 只在所属元对象中有意义 |
| `read(QObject *)` | 读取 QObject 属性 | 失败可能返回无效 QVariant |
| `readOnGadget(const void *)` | 读取 gadget 属性 | 地址和元对象类型必须匹配 |
| `relativePropertyIndex()` | 返回直接声明类中的相对索引 | 与 property offset 配合 |
| `reset(QObject *)` | 调用 QObject 属性 RESET | 需要 `isResettable()`；检查 bool |
| `resetOnGadget(void *)` | 调用 gadget 属性 RESET | 需要可写且类型匹配的地址 |
| `revision()` | 返回属性 revision | 用于版本化元对象/QML |
| `type()` | 返回旧式 `QVariant::Type` | Qt 6.0 起弃用，改用 `metaType()` |
| `typeId()` | 返回属性类型 ID | 数值兼容入口 |
| `typeName()` | 返回属性类型文本 | 诊断用，不替代 `QMetaType` |
| `userType()` | 返回类型 ID 的历史别名 | Qt 6.11 头文件中等价于 `typeId()` |
| `write(QObject *, const QVariant &)` | 写入 QObject 属性 | 检查能力、类型转换和 bool 结果 |
| `write(QObject *, QVariant &&)` | 移动 QVariant 写入 QObject | Qt 6.6 起；只是传递优化 |
| `writeOnGadget(void *, const QVariant &)` | 写入 gadget 属性 | 使用正确可写地址 |
| `writeOnGadget(void *, QVariant &&)` | 移动 QVariant 写入 gadget | Qt 6.6 起；不降低类型要求 |

## 12. 推荐模板

### 12.1 通用安全读写

```cpp
bool setPropertyByName(QObject *object,
                       const char *name,
                       const QVariant &value)
{
    const QMetaObject *meta = object->metaObject();
    const int index = meta->indexOfProperty(name);
    if (index < 0)
        return false;

    const QMetaProperty property = meta->property(index);
    if (!property.isWritable())
        return false;

    return property.write(object, value);
}
```

实际工具还可以比较 `property.metaType()` 和 `value.metaType()`，在允许的转换集合之外提前报错。

### 12.2 枚举属性编辑

```cpp
QList<QByteArray> enumKeys(const QMetaProperty &property)
{
    if (!property.isEnumType() && !property.isFlagType())
        return {};

    const QMetaEnum meta = property.enumerator();
    QList<QByteArray> result;
    for (int i = 0; i < meta.keyCount(); ++i)
        result.append(meta.key(i));
    return result;
}
```

Flags 属性还需要在写入时使用 `keysToValue()` 处理组合，不要只允许单个 key。

## 13. 一句话总结

`QMetaProperty` 是 `Q_PROPERTY` 的元对象句柄：它描述属性能力和类型，并把 QObject/gadget 的读写、reset、枚举、notify signal 与 binding 入口统一暴露出来；它不拥有实例值，`isReadable()`/`isWritable()` 只是能力提示，真正的 `read()`、`write()`、`reset()` 结果仍必须检查，`void *` gadget API 更必须严格匹配真实类型。
