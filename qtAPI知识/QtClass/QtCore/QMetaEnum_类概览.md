# Qt QMetaEnum 枚举反射与字符串转换笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMetaEnum>`  
> 所属模块：`Qt6::Core`  
> 类型性质：指向元对象中一个枚举描述的轻量值句柄  
> 相关类型：`QMetaObject`、`QMetaType`、`Q_ENUM`、`Q_FLAG`

## 1. 它解决什么问题

C++ 枚举在编译后通常只保留整数值；如果程序还需要把枚举显示成文字、从配置文本解析回枚举、或在调试工具中列出所有枚举项，就需要额外维护一套映射。`QMetaEnum` 把这套映射放进 Qt 元对象系统，提供：

- 枚举类型名、作用域、是否 `enum class`；
- 每个 key 的名称和对应整数值；
- 名称与值之间的转换；
- Flags 的 `A|B|C` 组合转换；
- 64 位底层枚举的完整值访问；
- 枚举对应的 `QMetaType`。

它本身不保存一份枚举值，也不负责把任意 C++ `enum` 自动注册到 Qt。枚举必须通过 `Q_ENUM`、`Q_ENUM_NS`、`Q_FLAG` 或 `Q_FLAG_NS` 等宏进入元对象系统，之后才能通过 `fromType<T>()` 或 `QMetaObject::enumerator()` 取得描述。

## 2. 实际使用场景

### 2.1 配置文本转换为枚举

```cpp
class Server : public QObject
{
    Q_OBJECT
public:
    enum class Mode {
        Development,
        Production
    };
    Q_ENUM(Mode)
};

Server::Mode parseMode(const QByteArray &text, bool *ok)
{
    const QMetaEnum meta = QMetaEnum::fromType<Server::Mode>();
    const auto value = meta.keyToValue64(text.constData());
    if (!value) {
        if (ok)
            *ok = false;
        return Server::Mode::Development;
    }

    if (ok)
        *ok = true;
    return static_cast<Server::Mode>(*value);
}
```

解析失败时不要把 `-1` 或空 `optional` 当作合法枚举值继续使用。对于普通 32 位枚举，`keyToValue()` 也可以使用；如果类型可能扩展为 64 位，统一使用 `keyToValue64()` 更稳妥。

### 2.2 将枚举值写入日志或界面

```cpp
const QMetaEnum meta = QMetaEnum::fromType<Server::Mode>();
const auto mode = Server::Mode::Production;

if (const char *key = meta.valueToKey(static_cast<quint64>(mode)))
    qDebug().noquote() << key;
```

`valueToKey()` 适合普通枚举的单个值；Flags 应使用 `valueToKeys()`，因为组合值通常没有一个单独的 key。

### 2.3 处理 Flags

```cpp
class File : public QObject
{
    Q_OBJECT
public:
    enum Permission {
        Read = 0x1,
        Write = 0x2,
        Execute = 0x4
    };
    Q_ENUM(Permission)

    Q_DECLARE_FLAGS(Permissions, Permission)
    Q_FLAG(Permissions)
};

const QMetaEnum meta = QMetaEnum::fromType<File::Permissions>();
bool ok = false;
const int value = meta.keysToValue("Read|Write", &ok);
if (ok) {
    const auto names = meta.valueToKeys(static_cast<quint64>(value));
    qDebug().noquote() << names;
}
```

Flags 的输入是由 `|` 分隔的 key 列表，函数会按位或合并各项值。`keyToValue()` 只适合单个 key；不要把 `"Read|Write"` 传给它。

### 2.4 构建通用枚举检查器

```cpp
void dumpEnum(const QMetaEnum &meta)
{
    if (!meta.isValid())
        return;

    qDebug() << meta.scope() << meta.name()
             << "flags =" << meta.isFlag()
             << "64-bit =" << meta.is64Bit();

    for (int i = 0; i < meta.keyCount(); ++i) {
        qDebug().noquote()
            << meta.key(i) << '='
            << meta.value64(i).value_or(0);
    }
}
```

遍历时以 `keyCount()` 为边界，并在使用 `key(i)`、`value64(i)` 时保留失败判断。`value(i)` 在 64 位枚举上只提供低 32 位，不适合通用工具。

## 3. 声明、注册与取得描述

### 3.1 类内枚举使用 `Q_ENUM` 或 `Q_FLAG`

```cpp
class Controller : public QObject
{
    Q_OBJECT
public:
    enum State {
        Idle,
        Running
    };
    Q_ENUM(State)

    enum Option {
        Fast = 0x1,
        Safe = 0x2
    };
    Q_ENUM(Option)

    Q_DECLARE_FLAGS(Options, Option)
    Q_FLAG(Options)
};
```

`Q_ENUM(State)` 注册的是枚举类型；`Q_FLAG(Options)` 注册的是 Flags 类型。对 Flags 来说，`name()` 返回 Flags 类型名，`enumName()` 返回对应枚举名，这两个名字可能不同。

### 3.2 命名空间枚举

```cpp
namespace Protocol {
Q_NAMESPACE

enum Kind {
    Request,
    Response
};
Q_ENUM_NS(Kind)
}

const QMetaEnum meta = QMetaEnum::fromType<Protocol::Kind>();
```

命名空间需要 `Q_NAMESPACE`，枚举需要 `Q_ENUM_NS`。否则 `fromType<T>()` 的编译期约束不会满足。

### 3.3 两种常用取得方式

已知 C++ 类型时优先使用：

```cpp
const QMetaEnum meta = QMetaEnum::fromType<Controller::State>();
```

只知道元对象和枚举名称时使用：

```cpp
const QMetaObject &object = Controller::staticMetaObject;
const int index = object.indexOfEnumerator("State");
if (index >= 0) {
    const QMetaEnum meta = object.enumerator(index);
    // 使用 meta...
}
```

后者必须检查索引。`QMetaEnum` 不提供按名称查找的静态全局函数，查找职责属于 `QMetaObject`。

## 4. 名称、key 和值的三层区别

假设有：

```cpp
enum Permission {
    Read = 0x1,
    Write = 0x2
};
Q_ENUM(Permission)
```

- `scope()`：声明作用域，例如 `File`；
- `name()`：元对象中这个枚举描述的类型名，例如 `Permission`；
- `enumName()`：枚举名。普通枚举通常与 `name()` 相同；Flags 可能不同；
- `key(i)`：某一个枚举项的文字名，例如 `Read`；
- `value(i)`：`key(i)` 对应的整数值。

不要把 `name()` 当成某个枚举项名，也不要把 `key(i)` 当成类型名。

## 5. 32 位与 64 位值

### 5.1 `value()` 和 `value64()` 的区别

`value(index)` 返回 `int`。当枚举的底层类型是 64 位时，它只返回低 32 位。

`value64(index)` 返回 `std::optional<quint64>`，能够表达完整的 64 位值；索引不存在时返回 `std::nullopt`。

同样的区别也存在于：

- `keyToValue()` 与 `keyToValue64()`；
- `keysToValue()` 与 `keysToValue64()`。

通用反射工具不应先调用 32 位 API，再把结果强转成 `quint64`，那样无法恢复已经丢失的高位。

### 5.2 32 位有符号值的符号扩展

Qt 6.9 的 64 位 API 会对有符号 32 位底层枚举进行符号扩展。例如底层值为 `-1` 时，`value64()` 的结果是 `0xffff'ffff'ffff'ffff`，而不是 `0x0000'0000'ffff'ffff`。

Flags 若使用了 bit 31，例如 `0x8000'0000`，不同编译器对默认底层类型的处理可能不同。需要稳定表达高位 Flags 时，显式指定底层类型：

```cpp
enum Permission : quint32 {
    Read = 0x1,
    HighBit = 0x8000'0000u
};
```

### 5.3 `is64Bit()` 是类型能力查询

`is64Bit()` 返回底层枚举是否宽 64 位。它描述元数据中的枚举类型，不是当前某个值是否超过 32 位。

## 6. 有效性、所有权和版本边界

### 6.1 默认构造是无效句柄

```cpp
const QMetaEnum invalid;
Q_ASSERT(!invalid.isValid());
```

默认构造不会绑定当前函数、当前类或某个枚举。使用 `name()`、`key()` 等结果前，应先确认描述有效。

### 6.2 字符串由元对象拥有

`name()`、`enumName()`、`scope()` 和 `key()` 返回 `const char *`。调用方不负责释放，也不能修改。若需要长期保存，或相关插件/动态库可能卸载，应复制成 `QByteArray` 或 `QString`。

`valueToKeys()` 返回一个新的 `QByteArray`，它是拥有型结果；而 `valueToKey()` 返回的是元对象中的非拥有指针。

### 6.3 `metaType()` 的兼容性

`metaType()` 返回枚举类型自身的 `QMetaType`，不是底层整数类型的 `QMetaType`。如果元对象是用 Qt 6.5 或更早版本生成的，返回值可能是无效 `QMetaType`。需要底层整数类型时，再调用：

```cpp
const QMetaType enumType = meta.metaType();
const QMetaType underlying = enumType.underlyingType();
```

项目跨动态库或混合 Qt 版本时，不要只根据 Qt 头文件版本判断元对象数据是否已经包含该信息。

## 7. 转换 API 的失败语义

### 7.1 单 key 转整数

```cpp
bool ok = false;
const int value = meta.keyToValue("Read", &ok);
if (!ok) {
    // key 不存在，value 不能作为成功结果使用。
}
```

未找到时，32 位 API 返回 `-1`，并通过 `ok` 报告失败。因为 `-1` 也可能是合法枚举值，所以业务代码必须检查 `ok`，不能只检查返回数值。

64 位版本没有 `ok` 指针，使用 `std::optional`：

```cpp
const auto value = meta.keyToValue64("Read");
if (!value)
    return;
```

### 7.2 多 key 转 Flags

```cpp
bool ok = false;
const int value = meta.keysToValue("Read|Write", &ok);
```

输入字符串应由 `|` 分隔。只要其中一项未定义，整体结果就应按失败处理。不要把任意用户文本直接当作已校验的权限集合；解析成功后仍应检查业务允许的位集合。

### 7.3 整数转 key

`valueToKey()` 对普通枚举寻找一个定义的 key；找不到返回 `nullptr`。对于 Flags 的组合值，优先使用 `valueToKeys()`。

`valueToKeys()` 返回 `|` 分隔的 key 列表。传入 64 位值给底层只有 32 位的枚举时，如果高 32 位存在内容，结果为空；因此调用方应先确认值宽度和类型匹配。

## 8. 逐项 API 说明

### 8.1 `QMetaEnum()`

```cpp
constexpr QMetaEnum();
```

创建无效枚举描述句柄。它适合作为默认值或“尚未取得描述”的状态，不会自动关联任何 `QMetaObject`。

### 8.2 `enclosingMetaObject() const`

```cpp
const QMetaObject *enclosingMetaObject() const;
```

返回包含该枚举描述的元对象。返回的是元对象，不是枚举实例，也不是 `QObject` 实例。无效句柄可能返回 `nullptr`。

### 8.3 `enumName() const`

```cpp
const char *enumName() const;
```

返回枚举名，不含作用域。普通枚举通常与 `name()` 相同；Flags 可能返回底层枚举名，而 `name()` 返回 Flags 类型名。

### 8.4 `fromType<T>()`

```cpp
template <typename T>
static QMetaEnum fromType();
```

按 C++ 类型取得对应元枚举。`T` 必须是通过 `Q_ENUM`、`Q_ENUM_NS`、`Q_FLAG` 或 `Q_FLAG_NS` 注册的枚举或 Flags 类型。未注册类型不是运行时返回无效，而是触发编译期约束失败。

### 8.5 `is64Bit() const`

```cpp
bool is64Bit() const;
```

查询枚举底层类型是否为 64 位。Qt 6.9 引入。为 true 时，读取和转换应优先使用 `value64()`、`keyToValue64()` 和 `keysToValue64()`。

### 8.6 `isFlag() const`

```cpp
bool isFlag() const;
```

查询该描述是否用于 Flags。为 true 时，值可以按位或组合，名称转换应优先使用 `keysToValue()` 和 `valueToKeys()`。

### 8.7 `isScoped() const`

```cpp
bool isScoped() const;
```

查询枚举是否声明为 C++11 `enum class`。它只描述 C++ 枚举声明形式，不改变 `QMetaEnum` 的 key/value 转换 API。

### 8.8 `isValid() const`

```cpp
bool isValid() const;
```

判断该句柄是否关联有效枚举描述。默认构造对象通常无效；从合法元对象索引取得的对象才应继续读取。

### 8.9 `key(int index) const`

```cpp
const char *key(int index) const;
```

返回指定索引处的 key。索引必须满足 `0 <= index < keyCount()`；越界时返回 `nullptr`。

### 8.10 `keyCount() const`

```cpp
int keyCount() const;
```

返回元数据中登记的 key 数量。它是遍历 `key(index)` 和 `value(index)` 的上界。

### 8.11 `keyToValue(const char *key, bool *ok) const`

```cpp
int keyToValue(const char *key, bool *ok = nullptr) const;
```

把单个 key 转为 32 位整数。未定义 key 时返回 `-1`，并在提供 `ok` 时写入 `false`。64 位枚举只返回低 32 位；Flags 的组合输入应改用 `keysToValue()`。

### 8.12 `keyToValue64(const char *key) const`

```cpp
std::optional<quint64> keyToValue64(const char *key) const;
```

Qt 6.9 引入。把单个 key 转为完整值，找不到时返回 `std::nullopt`。有符号 32 位底层值按 Qt 的规则符号扩展到 64 位。

### 8.13 `keysToValue(const char *keys, bool *ok) const`

```cpp
int keysToValue(const char *keys, bool *ok = nullptr) const;
```

解析 `|` 分隔的 key 列表，并按位或合并结果。32 位 API 对 64 位枚举只返回低 32 位；失败时返回 `-1` 并通过 `ok` 报告。

### 8.14 `keysToValue64(const char *keys) const`

```cpp
std::optional<quint64> keysToValue64(const char *keys) const;
```

Qt 6.9 引入。解析 Flags 组合并保留完整 64 位值。输入中的每个 key 都必须可识别，否则返回 `std::nullopt`。

### 8.15 `metaType() const`

```cpp
QMetaType metaType() const;
```

Qt 6.6 引入。返回枚举类型自身的 `QMetaType`。它不是底层整数类型；需要底层类型时使用 `underlyingType()`。旧版本生成的元对象可能让此函数返回无效类型。

### 8.16 `name() const`

```cpp
const char *name() const;
```

返回不含作用域的类型名。对 Flags，它返回 Flags 类型名，而不是底层枚举名。返回指针由元对象拥有。

### 8.17 `scope() const`

```cpp
const char *scope() const;
```

返回枚举声明所在的类或命名空间作用域，不含枚举类型名。返回指针由元对象拥有。

### 8.18 `value(int index) const`

```cpp
int value(int index) const;
```

返回指定 key 的 32 位值。索引无效时返回 `-1`；对于 64 位枚举只返回低 32 位。若 `-1` 可能是合法值，必须结合索引范围或 `value64()` 判断，而不能只看返回值。

### 8.19 `value64(int index) const`

```cpp
std::optional<quint64> value64(int index) const;
```

Qt 6.9 引入。返回指定 key 的完整值；索引不存在时返回 `std::nullopt`。适合通用反射、序列化和可能使用 64 位底层类型的工具。

### 8.20 `valueToKey(quint64 value) const`

```cpp
const char *valueToKey(quint64 value) const;
```

把单个枚举值转换为 key。未定义时返回 `nullptr`；Flags 组合值应使用 `valueToKeys()`。返回指针由元对象拥有。

### 8.21 `valueToKeys(quint64 value) const`

```cpp
QByteArray valueToKeys(quint64 value) const;
```

把值转换成 `|` 分隔的 key 列表，适合 Flags。返回的是拥有型 `QByteArray`。对 32 位枚举传入包含高位的 64 位值时，结果为空。

## 9. 常见错误

### 9.1 没有使用元对象宏

**症状：** `fromType<T>()` 无法编译，或按元对象名称查找不到枚举。

**原因：** C++ 枚举没有自动进入 Qt 元对象系统。

**修复：** 类内使用 `Q_ENUM`/`Q_FLAG`，命名空间使用 `Q_NAMESPACE` 加 `Q_ENUM_NS`/`Q_FLAG_NS`，并确保 `moc` 处理声明。

### 9.2 把 `name()` 当成 key

**症状：** 用 `"Running"` 去比较 `meta.name()`，结果始终不匹配。

**原因：** `name()` 是类型名，key 是 `key(index)` 返回的枚举项名。

**修复：** 类型级比较使用 `name()`，枚举项转换使用 `keyToValue()`/`valueToKey()`。

### 9.3 用 `-1` 判断 32 位转换成功

**症状：** 合法的 `-1` 枚举值被当成失败，或失败值被误接受。

**原因：** `-1` 同时是失败哨兵和可能的合法枚举值。

**修复：** 使用 `bool *ok`，或改用返回 `std::optional` 的 64 位 API。

### 9.4 在 64 位枚举上使用 `value()`

**症状：** 反射工具显示的值缺少高 32 位。

**原因：** `value()` 和 `keyToValue()` 的返回类型是 `int`。

**修复：** 检查 `is64Bit()`，优先使用 `value64()`、`keyToValue64()` 和 `keysToValue64()`。

### 9.5 用 `valueToKey()` 处理 Flags 组合

**症状：** `Read|Write` 的组合值找不到名称。

**原因：** 组合值通常不是某一个单独 key。

**修复：** 使用 `valueToKeys()`，输入方向使用 `keysToValue()`。

### 9.6 保存元对象字符串指针跨越模块卸载

**症状：** 插件卸载后，之前保存的 `const char *` 访问崩溃。

**原因：** 字符串由元对象所属模块拥有。

**修复：** 在模块仍加载时复制为 `QByteArray` 或 `QString`。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QMetaEnum()` | 构造无效枚举描述句柄 | 不会自动绑定当前类或枚举 |
| `enclosingMetaObject()` | 返回所属 `QMetaObject` | 返回元对象指针，不是枚举实例；无效句柄可能为空 |
| `enumName()` | 返回枚举名 | Flags 可能与 `name()` 不同；返回非拥有 `const char *` |
| `fromType<T>()` | 按 C++ 枚举/Flags 类型取得描述 | `T` 必须使用 `Q_ENUM`、`Q_ENUM_NS`、`Q_FLAG` 或 `Q_FLAG_NS` 注册 |
| `is64Bit()` | 判断底层类型是否 64 位 | Qt 6.9 起；为 true 时优先使用 64 位 API |
| `isFlag()` | 判断是否是 Flags 描述 | 组合值使用 `keysToValue()`/`valueToKeys()` |
| `isScoped()` | 判断是否为 `enum class` | 只描述 C++ 声明形式 |
| `isValid()` | 判断描述句柄是否有效 | 默认构造对象通常无效 |
| `key(index)` | 按索引取得枚举项名称 | 索引越界返回 `nullptr` |
| `keyCount()` | 返回枚举项数量 | 与 `key()`、`value()` 遍历配套 |
| `keyToValue(key, ok)` | 单 key 转 32 位值 | 失败返回 `-1`；必须检查 `ok`；64 位值会截断 |
| `keyToValue64(key)` | 单 key 转完整 64 位值 | Qt 6.9 起；失败返回 `std::nullopt` |
| `keysToValue(keys, ok)` | 解析 `|` 分隔的 Flags key | 失败返回 `-1`；64 位值会截断 |
| `keysToValue64(keys)` | 解析 Flags 并返回完整值 | Qt 6.9 起；失败返回 `std::nullopt` |
| `metaType()` | 返回枚举自身的 `QMetaType` | Qt 6.6 起；旧元对象可能返回无效类型 |
| `name()` | 返回不含作用域的类型名 | Flags 返回 Flags 类型名；不是某个 key |
| `scope()` | 返回声明作用域 | 返回非拥有 `const char *` |
| `value(index)` | 按索引取得 32 位值 | 64 位枚举只返回低 32 位；无效索引返回 `-1` |
| `value64(index)` | 按索引取得完整值 | Qt 6.9 起；无效索引返回 `std::nullopt` |
| `valueToKey(value)` | 单值转 key | 未定义返回 `nullptr`；Flags 组合使用 `valueToKeys()` |
| `valueToKeys(value)` | 值转 `|` 分隔 key 列表 | 返回拥有型 `QByteArray`；32 位枚举不能接收带高位的 64 位值 |

## 11. 推荐模板

### 11.1 可靠解析普通枚举

```cpp
template <typename Enum>
std::optional<Enum> enumFromKey(const QByteArray &key)
{
    const QMetaEnum meta = QMetaEnum::fromType<Enum>();
    const auto value = meta.keyToValue64(key.constData());
    if (!value)
        return std::nullopt;

    return static_cast<Enum>(*value);
}
```

模板只适合已经注册到元对象的枚举类型。若输入来自不可信配置，还应额外检查结果是否属于业务允许集合。

### 11.2 枚举值转稳定日志文本

```cpp
template <typename Enum>
QByteArray enumToKey(Enum value)
{
    const QMetaEnum meta = QMetaEnum::fromType<Enum>();
    if (const char *key =
            meta.valueToKey(static_cast<quint64>(value))) {
        return QByteArray(key);
    }
    return {};
}
```

对于 Flags，把 `valueToKey()` 改为 `valueToKeys()`；空结果应保留为“没有对应名称”，不要静默替换成任意数字文本。

## 12. 一句话总结

`QMetaEnum` 是 Qt 元对象中的枚举映射句柄：`name()`/`scope()` 描述类型，`key()`/`value()` 描述每个枚举项，`keyToValue*()` 与 `valueToKey*()` 负责转换，Flags 使用 `keysToValue*()`/`valueToKeys()`；涉及 64 位值时必须避开会截断的 32 位 API，并记住所有 `const char *` 都依赖元对象生命周期。
