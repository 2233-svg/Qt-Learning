# QDBusArgument
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusArgument`

## 作用定位

`QDBusArgument` 是 Qt D-Bus 的底层序列化游标。它负责把 C++/Qt 类型写进 D-Bus 消息，也负责从 D-Bus 消息里按协议结构读出来。普通的 `int`、`QString`、`QStringList` 等基础类型通常自动处理；一旦遇到自定义结构、结构数组、map、variant，就需要 `QDBusArgument` 和 `qDBusRegisterMetaType()`。

可以把它理解成“带 D-Bus 类型签名的输入/输出流”，但它比普通 `QDataStream` 更严格：读写顺序、结构边界、map entry 边界必须一一对应。

## 类说明

- 头文件：`#include <QDBusArgument>`
- CMake：链接 `Qt6::DBus`
- 继承：无公开 QObject 继承
- 相关函数：`qDBusRegisterMetaType<T>()`、`qdbus_cast<T>()`

## API 速查

| API | 说明 |
| --- | --- |
| `beginStructure()` / `endStructure()` | 写入或读取 D-Bus struct 边界。自定义聚合类型最常用。 |
| `beginArray(QMetaType)` / `endArray()` | 写数组边界并声明元素类型。 |
| `beginArray() const` / `endArray() const` | 读取数组边界。 |
| `beginMap(keyType, valueType)` / `endMap()` | 写 map 容器。 |
| `beginMap() const` / `endMap() const` | 读取 map 容器。 |
| `beginMapEntry()` / `endMapEntry()` | 写或读 map 中一项 key/value。 |
| `currentType()` | 读取当前位置元素类型，适合调试动态结构。 |
| `atEnd()` | 读取数组或 map 时判断是否结束。 |
| `asVariant()` | 把当前内容作为 `QVariant` 取出。 |
| `operator<<` | 写入基础类型、字符串、字节数组、`QDBusVariant` 等。 |
| `operator>>` | 读取基础类型、字符串、字节数组、`QDBusVariant` 等。 |
| `swap()` | 快速交换两个 argument。 |
| `qDBusRegisterMetaType<T>()` | 注册自定义类型的 D-Bus 封送函数。 |
| `qdbus_cast<T>()` | 从 `QDBusArgument` 转成目标 C++ 类型。 |

## 元素类型

| `ElementType` | 说明 |
| --- | --- |
| `BasicType` | 基础类型，如整数、布尔、double、字符串、对象路径、签名。 |
| `VariantType` | D-Bus variant，对应 `QDBusVariant`。 |
| `ArrayType` | 数组或列表。注意 `QByteArray` 在 Qt 里被当作基础字节数组处理。 |
| `StructureType` | struct，常用于自定义聚合类型。 |
| `MapType` | 字典或关联容器。 |
| `MapEntryType` | map 里的一个 key/value 条目。 |
| `UnknownType` | 未知或已到末尾。 |

## 自定义类型写法

```cpp
struct UserInfo
{
    QString name;
    uint uid;
};

Q_DECLARE_METATYPE(UserInfo)

QDBusArgument &operator<<(QDBusArgument &argument, const UserInfo &info)
{
    argument.beginStructure();
    argument << info.name << info.uid;
    argument.endStructure();
    return argument;
}

const QDBusArgument &operator>>(const QDBusArgument &argument, UserInfo &info)
{
    argument.beginStructure();
    argument >> info.name >> info.uid;
    argument.endStructure();
    return argument;
}

qDBusRegisterMetaType<UserInfo>();
```

顺序就是协议。写入是 `name, uid`，读取也必须是 `name, uid`；改字段顺序会改变 D-Bus 签名和兼容性。

## 使用场景

- 远端接口返回结构体、结构体数组、字典。
- 自定义 C++ 类型需要作为 D-Bus 参数传递。
- 动态读取不确定结构时检查 `currentType()`。
- 从 `QVariant` 中拿到 `QDBusArgument` 后转成具体类型。

## 常见坑与经验

- begin/end 必须配对，结构、数组、map、map entry 少一个边界都会导致签名错乱。
- `qDBusRegisterMetaType<T>()` 不是可选步骤；只声明 `Q_DECLARE_METATYPE` 不足以让 D-Bus 知道如何封送。
- 自定义类型的字段顺序一旦发布就应视为协议，随便插字段会破坏旧客户端。
- map 的 key 类型必须是 D-Bus 允许的基础类型；不能随意用复杂结构当 key。
- 读取时 `atEnd()` 只在容器语境里有意义，不能替代整体消息是否有效的检查。
- 出现 `InvalidSignature` 时，先核对模板类型、stream operator 顺序和注册时机。

## 知识点覆盖

- D-Bus 基础类型、数组、struct、dict entry
- Qt 元类型系统与 D-Bus 封送
- 自定义类型注册和 stream operator
- QVariant、QDBusVariant、QDBusArgument 的关系
- D-Bus 签名兼容性设计
