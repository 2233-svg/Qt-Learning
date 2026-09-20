# Qt QFlags 深入笔记

> 适用版本：Qt 6.11.1  
> 模板：`template <typename Enum> class QFlags`  
> 头文件：`#include <QFlags>`  
> 所属模块：`Qt6::Core`  
> 类型性质：类型安全的枚举位标志值类型

## 1. QFlags 解决什么问题

`QFlags<Enum>` 用来保存同一个枚举类型的多个位标志。它替代了“用 `int` 或 `uint` 手动保存 OR 组合”的旧式写法：

```text
多个 Enum 值
    |
    v
QFlags<Enum>
    |
    +-- OR / AND / XOR / NOT
    +-- testFlag / testAnyFlag
    +-- setFlag / fromInt / toInt
    +-- 编译期阻止不相关枚举混入
```

例如：

```cpp
enum class RenderOption {
    None = 0,
    Antialiasing = 0x1,
    HighQuality = 0x2,
    DebugOverlay = 0x4
};

Q_DECLARE_FLAGS(RenderOptions, RenderOption)
Q_DECLARE_OPERATORS_FOR_FLAGS(RenderOptions)

const RenderOptions options =
    RenderOption::Antialiasing | RenderOption::HighQuality;
```

如果直接用 `int`，任何整数或其他枚举都可能被 OR 进来；使用 `QFlags` 后，接口可以明确要求 `RenderOptions`，调用者也能看到允许的枚举类型。

Qt 中常见的 `Qt::Alignment`、`QIODevice::OpenMode` 和很多 `Permissions` 类型，本质上都是某个枚举的 `QFlags` 别名。

## 2. QFlags 是值类型，不是 QObject

`QFlags` 不拥有资源，不继承 `QObject`，也没有对象树、信号或线程亲和性。它适合按值传递、返回和存入容器：

```cpp
RenderOptions makeOptions(bool debug)
{
    RenderOptions result = RenderOption::Antialiasing;
    if (debug)
        result |= RenderOption::DebugOverlay;
    return result;
}
```

它的构造、位运算和查询函数都是 `constexpr`、`noexcept` 风格的轻量操作。`QFlags` 的存储宽度由枚举底层类型和 Qt 的存储规则决定，不应该把所有 flags 都强制当作 `int`。

## 3. 声明自定义 QFlags

为自定义枚举声明 flags 类型通常需要两个宏：

```cpp
enum class FileOption : quint32 {
    None = 0,
    Read = 0x0001,
    Write = 0x0002,
    Create = 0x0004
};

Q_DECLARE_FLAGS(FileOptions, FileOption)
Q_DECLARE_OPERATORS_FOR_FLAGS(FileOptions)
```

宏的职责不同：

| 宏 | 作用 |
| --- | --- |
| `Q_DECLARE_FLAGS(FileOptions, FileOption)` | 声明 `using` 风格的 `QFlags<FileOption>` 类型别名 |
| `Q_DECLARE_OPERATORS_FOR_FLAGS(FileOptions)` | 声明枚举项之间以及枚举项和 flags 之间的全局位运算符 |

只写 `Q_DECLARE_FLAGS` 而不写第二个宏时，`FileOptions` 类型存在，但 `FileOption::Read | FileOption::Write` 这类表达式可能没有所需的全局运算符。

如果 flags 要作为 QObject 属性、信号参数或 Qt Designer 可编辑的元对象枚举使用，还需要在 QObject 派生类中写：

```cpp
class Editor : public QObject
{
    Q_OBJECT
    Q_FLAG(FileOptions)
};
```

`Q_DECLARE_FLAGS` 本身不会把 flags 暴露给元对象系统。

## 4. 枚举值如何设计

### 4.1 每个独立标志占一个 bit

```cpp
enum class Feature {
    None = 0,
    Search = 1 << 0,
    Replace = 1 << 1,
    Preview = 1 << 2
};
```

不要把多个独立选项赋成同一个非零值，否则 `testFlag()` 和组合判断无法区分它们。

### 4.2 可以定义组合枚举项

```cpp
enum class Permission {
    None = 0,
    Read = 0x1,
    Write = 0x2,
    ReadWrite = Read | Write
};
```

组合项适合作为常用别名，但要理解：

- `testFlag(Permission::ReadWrite)` 要求 Read 和 Write 两个位都存在；
- `testAnyFlag(Permission::ReadWrite)` 只要求其中一个位存在；
- `flags == Permission::ReadWrite` 要求整个 flags 值恰好等于这两个位，额外位会导致 false。

### 4.3 64 位枚举

Qt 6.9 起，`QFlags` 支持最多 64 位的枚举。超过 32 位时，建议显式固定底层类型：

```cpp
enum class Capability : quint64 {
    None = 0,
    Read = quint64(1) << 40,
    Write = quint64(1) << 41
};

Q_DECLARE_FLAGS(Capabilities, Capability)
Q_DECLARE_OPERATORS_FOR_FLAGS(Capabilities)
```

显式底层类型可以避免删除某个枚举项后，编译器改变枚举宽度，进而改变 flags 类型的大小和 ABI。

`QFlag` 只适合 32 位兼容入口，不能用它承载 64 位 flags；64 位整数边界应使用 `QFlags<Enum>::Int`、`fromInt()` 和 `toInt()`。

## 5. 构造和初始化

### 5.1 空 flags

```cpp
RenderOptions none;
RenderOptions alsoNone{};
```

默认构造没有任何位被设置。空 flags 的整数值为零，`!none` 为 true。

### 5.2 从一个枚举项构造

```cpp
RenderOptions options = RenderOption::Antialiasing;
```

这不会自动设置其他枚举项。

### 5.3 从 initializer list 构造

```cpp
const RenderOptions options{
    RenderOption::Antialiasing,
    RenderOption::HighQuality
};
```

initializer list 中的枚举项会进行 OR 组合。它适合构造少量固定选项，也能清晰表达“这是一个 flags 集合”。

### 5.4 从整数构造

`fromInt()` 用于把已经经过边界验证的整数位模式恢复为 `QFlags`：

```cpp
const auto raw = Capability::Int(1ull << 40);
const Capabilities flags = Capabilities::fromInt(raw);
```

它不会检查整数中是否只有已命名枚举项。外部文件、网络或硬件传来的位掩码，应先做版本、保留位和权限校验，再调用 `fromInt()`。

Qt 6.9 起，`std::in_place_t` 构造可用于所有支持的枚举宽度：

```cpp
const Capabilities flags(
    std::in_place,
    Capability::Int(1ull << 40));
```

`QFlags(QFlag)` 是 32 位兼容构造，主要为旧代码和旧属性路径服务；新代码优先用枚举组合或 `fromInt()`。

## 6. 位运算语义

### 6.1 OR：添加选项

```cpp
RenderOptions options = RenderOption::Antialiasing;
options |= RenderOption::HighQuality;

const RenderOptions combined =
    RenderOption::Antialiasing | RenderOption::DebugOverlay;
```

`|` 和 `|=` 把位设置为 1。

### 6.2 AND：保留交集

```cpp
const RenderOptions requested =
    RenderOption::Antialiasing | RenderOption::HighQuality;
const RenderOptions supported =
    RenderOption::Antialiasing | RenderOption::DebugOverlay;

const RenderOptions usable = requested & supported;
```

`&` 返回两个 flags 的共同位。它适合把请求选项限制到实现支持的位集合。

### 6.3 XOR：切换差异

```cpp
options ^= RenderOption::DebugOverlay;
```

`^` 会切换指定位：原来有则清除，原来没有则设置。对“确保打开”或“确保关闭”不要用 XOR，应使用 `setFlag()` 或 OR/AND。

### 6.4 NOT：反转存储宽度内的所有位

```cpp
const RenderOptions inverted = ~options;
```

`~` 会反转 `QFlags` 存储整数中的所有位，不只反转当前枚举已经命名的位。结果中可能包含“未命名保留位”：

```cpp
const RenderOptions known =
    inverted & (RenderOption::Antialiasing |
                RenderOption::HighQuality |
                RenderOption::DebugOverlay);
```

如果只想得到“所有合法枚举项的补集”，先构造一个明确的 `AllKnown` mask，再与它相与。

### 6.5 禁止加减法

`QFlags` 明确删除了 `+` 和 `-` 相关运算，避免把位标志误当成普通数值相加减：

```cpp
// options + RenderOption::HighQuality; // 编译错误
```

使用 `|` 添加、`&` 过滤、`^` 切换、`setFlag()` 按条件设置。

## 7. testFlag、testAnyFlag、testFlags 和 testAnyFlags

这是 `QFlags` 最容易用错的一组 API。

### 7.1 `testFlag()`：要求 flag 的所有位

```cpp
const RenderOptions options =
    RenderOption::Antialiasing | RenderOption::HighQuality;

Q_ASSERT(options.testFlag(RenderOption::Antialiasing));
```

如果传入的是组合枚举项：

```cpp
Q_ASSERT(options.testFlag(
    RenderOption::Antialiasing | RenderOption::HighQuality));
```

只有组合中的所有位都设置时才返回 true。传入零值时，只有当前 flags 也是零值才返回 true。

### 7.2 `testAnyFlag()`：要求至少一个位

```cpp
const bool hasOne =
    options.testAnyFlag(RenderOption::HighQuality |
                        RenderOption::DebugOverlay);
```

只要传入组合中有任意一位存在，就返回 true。传入零值时总是 false。

`testAnyFlag()` 和 `testAnyFlags()` 从 Qt 6.2 起提供。

### 7.3 `testFlags()`：要求整个 flags 参数的所有位

```cpp
const RenderOptions required =
    RenderOption::Antialiasing | RenderOption::HighQuality;

if (options.testFlags(required)) {
    // options 至少包含 required 的全部位
}
```

它与 `testFlag()` 的区别主要在参数类型：`testFlags()` 接受一个 `QFlags`。当参数为空时，只有当前 flags 也为空才返回 true。

### 7.4 `testAnyFlags()`：两个 flags 的位交集非空

```cpp
const RenderOptions candidates =
    RenderOption::HighQuality | RenderOption::DebugOverlay;

if (options.testAnyFlags(candidates)) {
    // 至少命中一位
}
```

空参数总是 false。

可记成：

| API | 条件 |
| --- | --- |
| `testFlag(f)` | `this` 包含 `f` 的全部位；若 f 为 0，则 this 也必须为 0 |
| `testAnyFlag(f)` | `this` 与 f 至少有一位交集；若 f 为 0，则 false |
| `testFlags(fs)` | `this` 包含 `fs` 的全部位；若 fs 为空，则 this 也必须为空 |
| `testAnyFlags(fs)` | `this` 与 fs 至少有一位交集；若 fs 为空，则 false |

## 8. setFlag：按条件设置或清除

```cpp
RenderOptions options;
options.setFlag(RenderOption::Antialiasing, userPrefersQuality);
options.setFlag(RenderOption::DebugOverlay);
options.setFlag(RenderOption::DebugOverlay, false);
```

`setFlag(flag, true)` 相当于 OR，`setFlag(flag, false)` 会清除 `flag` 包含的所有位。它返回当前对象的引用，适合链式修改。

传入组合枚举项时，`false` 会一次清除组合中的全部位：

```cpp
options.setFlag(
    RenderOption::Antialiasing | RenderOption::HighQuality,
    false);
```

相比 XOR，`setFlag()` 的结果不依赖原来该位是否存在，更适合表达“必须打开”或“必须关闭”。

## 9. toInt、operator Int 和 fromInt

### 9.1 `toInt()`

```cpp
const RenderOptions::Int raw = options.toInt();
```

`toInt()` 返回实际存储的整数类型。它可能是有符号或无符号，取决于枚举底层类型；Qt 6.9 起还会根据枚举宽度选择 32 位或 64 位类型。

### 9.2 隐式或显式整数转换

在默认兼容模式下，`QFlags` 可以隐式转换为 `Int`；定义 `QT_TYPESAFE_FLAGS` 后，该转换变为显式：

```cpp
const auto raw = options.toInt(); // 推荐

#ifdef QT_TYPESAFE_FLAGS
const RenderOptions::Int explicitRaw =
    static_cast<RenderOptions::Int>(options);
#endif
```

新代码应优先使用 `toInt()`，不要依赖宏配置下的隐式转换差异。

### 9.3 `fromInt()`

```cpp
const RenderOptions restored =
    RenderOptions::fromInt(raw);
```

`fromInt()` 是“按原始位模式恢复”的入口，不会自动过滤未知位。处理外部输入时，先验证：

```cpp
const auto knownMask =
    RenderOptions::Int(RenderOption::Antialiasing)
    | RenderOptions::Int(RenderOption::HighQuality)
    | RenderOptions::Int(RenderOption::DebugOverlay);

if ((raw & ~knownMask) != 0)
    return false;
```

然后再调用 `fromInt()`。

## 10. QT_TYPESAFE_FLAGS 编译模式

`QT_TYPESAFE_FLAGS` 是 Qt 6 中可选的类型安全增强模式，影响旧式整数兼容：

| 行为 | 默认兼容模式 | 定义 `QT_TYPESAFE_FLAGS` 后 |
| --- | --- | --- |
| 转换到 `Int` | 隐式 | 显式 |
| 布尔判断 | 通过整数兼容 | 显式 `operator bool` |
| `operator&(int/uint)` | 可用，但只覆盖旧式整数宽度 | 禁用 |
| 64 位 flags 与裸 int mask | 容易产生宽度误解 | 强迫使用类型安全 flags |
| 枚举和整数混合 | 通过兼容辅助保护 | 更多表达式直接被删除 |

新项目应尽量使用枚举项、`QFlags` 和 `fromInt()`，不要依赖默认兼容模式下的隐式整数行为。启用宏可能暴露旧代码中的隐式转换问题，但这些报错通常是在帮助修复真实的类型混用。

## 11. QFlags 的存储类型和 ABI

`QFlags<Enum>::Int` 是它的实际整数存储类型：

```cpp
using Storage = RenderOptions::Int;
```

它的选择取决于：

- `Enum` 是否使用有符号或无符号底层类型；
- `Enum` 的大小；
- Qt 对 32 位和 64 位枚举的存储规则。

头文件限制枚举最多 64 位。若枚举底层类型没有显式固定，删除或增加枚举项可能让编译器改变枚举大小，从而改变 `QFlags` 的大小。跨模块 ABI、文件布局或共享内存结构中使用 flags 时，建议使用固定宽度底层类型并明确序列化格式。

## 12. 比较语义

`QFlags` 的相等比较是精确的位掩码比较：

```cpp
const RenderOptions both =
    RenderOption::Antialiasing | RenderOption::HighQuality;

Q_ASSERT(both.testFlag(RenderOption::Antialiasing));
Q_ASSERT(both != RenderOption::Antialiasing);
```

`testFlag()` 表示“包含”，`operator==` 表示“完全相同”。额外设置一位就会让相等比较失败。

QFlags 还提供与枚举项的双向 `==`、`!=`，以及 Qt 6.2 起的 `qHash()`，因此可用于 `QHash` 和 `QSet`：

```cpp
QSet<RenderOptions> supportedSets;
supportedSets.insert(both);
```

hash 表示当前位模式，不应拿来当跨 Qt 版本稳定的文件或网络编码。

## 13. 与 Qt 元对象系统配合

`Q_DECLARE_FLAGS()` 只声明 C++ 类型别名和相关 flags 关系，不会自动让 Qt 元对象系统知道这个类型：

```cpp
class RenderWidget : public QObject
{
    Q_OBJECT
    Q_FLAG(RenderOptions)
};
```

如果要让 flags 出现在 QObject 属性、信号槽元类型或 Qt Widgets Designer 中，需要在对应 QObject 派生类的 `Q_OBJECT` 区域使用 `Q_FLAG(RenderOptions)`。

这三个层次不要混在一起：

| 层次 | 负责什么 |
| --- | --- |
| C++ enum | 单个命名标志及其底层值 |
| `Q_DECLARE_FLAGS` / `Q_DECLARE_OPERATORS_FOR_FLAGS` | C++ 位组合和类型别名 |
| `Q_FLAG` | QObject 元对象系统中的 flags 注册 |

## 14. 常见使用场景

### 14.1 API 接收可组合选项

```cpp
void openFile(const QString &path, FileOptions options);

openFile(path, FileOption::Read | FileOption::Create);
```

调用者既能组合选项，编译器又能阻止把另一组 enum 传进来。

### 14.2 过滤支持能力

```cpp
const FileOptions usable = requested & supported;
```

这比手动 `static_cast<int>` 更能表达“取共同能力”。

### 14.3 外部位掩码边界

```cpp
FileOptions parseOptions(quint32 raw)
{
    constexpr quint32 known =
        quint32(FileOption::Read)
        | quint32(FileOption::Write)
        | quint32(FileOption::Create);

    if (raw & ~known)
        return {};

    return FileOptions::fromInt(
        FileOptions::Int(raw));
}
```

外部输入先验证未知位，再进入 `QFlags`。不要因为 `fromInt()` 能接受任意整数，就把它当作验证函数。

## 15. 常见误区

### 15.1 把 testFlag 当成“任意一位”

组合 flag 需要所有位。要检测任意一位，用 `testAnyFlag()` 或 `testAnyFlags()`。

### 15.2 把相等比较当成包含判断

`flags == Option::Read` 要求 flags 恰好只有 Read；要判断至少包含 Read，用 `testFlag(Read)`。

### 15.3 把空 flag 传给 testAnyFlag

空 flag 没有任何位，所以 `testAnyFlag()` 和 `testAnyFlags()` 总是 false；`testFlag()` / `testFlags()` 对空参数则要求当前对象也为空。

### 15.4 无限制使用 operator~

`~` 会把存储宽度内的保留位也设为 1。需要合法选项集合时，和明确的 `AllKnown` mask 相与。

### 15.5 把 64 位 flags 截断成 int

Qt 6.9 起可以有 64 位 flags。不要通过 `int(flags)`、`operator&(int)` 或 QFlag 处理它们。使用 `QFlags::Int` 和类型安全重载。

### 15.6 只声明 Q_DECLARE_FLAGS

没有 `Q_DECLARE_OPERATORS_FOR_FLAGS`，枚举项之间的组合表达式可能不可用；没有 `Q_FLAG`，元对象系统也看不到该 flags 类型。

## 16. API 逐项说明

### 16.1 类型和构造

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `using enum_type` | 暴露模板参数 `Enum`。 | 用于宏和泛型代码；不是运行时状态。 |
| `using Int` | 暴露 flags 的实际整数存储类型。 | 可能是有符号或无符号，Qt 6.9 起也可能是 64 位。 |
| `QFlags()` | 创建无标志对象。 | 所有位为 0。 |
| `QFlags(Enum flags)` | 从一个枚举项创建 flags。 | 只设置该枚举项的位。 |
| `QFlags(QFlag flag)` | 从旧式整数兼容包装创建 flags。 | 只对 32 位 Enum 可用；新代码优先用 `fromInt()`。 |
| `QFlags(std::initializer_list<Enum>)` | OR 组合列表中的枚举项。 | 适合 `{ Enum::A, Enum::B }`。 |
| `QFlags(std::in_place_t, Int flags)` | 按实际整数构造 flags。 | Qt 6.9 起；适合所有支持的枚举宽度。 |
| copy/move 构造和赋值 | 复制或移动 flags 值。 | 只复制位模式，不复制任何资源。 |

### 16.2 创建和查询

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `fromInt(Int i)` | 从整数位模式创建 flags。 | Qt 6.2 起；不验证未知位。 |
| `toInt()` | 取得内部存储整数。 | Qt 6.2 起；返回类型可能有符号或 64 位。 |
| `operator Int()` | 把 flags 转为内部整数。 | 默认模式可能隐式；`QT_TYPESAFE_FLAGS` 下显式。 |
| `operator!()` | 判断是否没有任何位。 | 无 flags 时 true；类型安全模式使用显式 bool 语义。 |
| `operator bool()` | 类型安全模式下进行布尔上下文判断。 | 由 `QT_TYPESAFE_FLAGS` 控制，优先写 `if (flags)` 或显式比较。 |

### 16.3 设置和匹配

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `setFlag(Enum flag, bool on = true)` | 按 bool 设置或清除枚举项的全部位。 | 比 XOR 更适合表达确定的开关状态。 |
| `testFlag(Enum flag)` | 检查枚举项的全部位是否存在。 | 组合项要求所有位；零项要求当前为空。 |
| `testAnyFlag(Enum flag)` | 检查枚举项中是否至少一位存在。 | Qt 6.2 起；零项总是 false。 |
| `testFlags(QFlags flags)` | 检查参数 flags 的全部位是否存在。 | Qt 6.2 起；空参数要求当前也为空。 |
| `testAnyFlags(QFlags flags)` | 检查两个 flags 是否有任意交集。 | Qt 6.2 起；空参数总是 false。 |

### 16.4 位运算成员

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `operator|=(QFlags)` | OR 合并另一个 flags。 | 添加位。 |
| `operator|=(Enum)` | OR 合并一个枚举项。 | 添加该枚举的所有位。 |
| `operator&=(QFlags)` | AND 保留共同位。 | 过滤位。 |
| `operator&=(Enum)` | 与枚举项做 AND。 | 保留指定 mask 中的位。 |
| `operator&=(int/uint)` | 与裸整数做 AND。 | 兼容模式 API；受 `QT_TYPESAFE_FLAGS` 和 32 位限制影响。 |
| `operator^=(QFlags)` | XOR 切换位。 | 结果依赖原状态。 |
| `operator^=(Enum)` | XOR 切换枚举项的位。 | 不等同于确保打开或关闭。 |
| `operator|(QFlags/Enum)` | 返回 OR 组合。 | 不修改操作数。 |
| `operator&(QFlags/Enum)` | 返回 AND 结果。 | 64 位应使用类型安全重载。 |
| `operator&(int/uint)` | 返回与整数 mask 的 AND。 | 默认兼容模式的旧式重载。 |
| `operator^(QFlags/Enum)` | 返回 XOR 结果。 | 用于切换位。 |
| `operator~()` | 返回存储宽度内的按位取反。 | 可能产生未命名保留位。 |
| `operator+` / `operator-` | 被显式删除。 | 防止把 flags 当普通数值运算。 |

### 16.5 比较和哈希

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `operator==(QFlags, QFlags)` | 精确比较位模式。 | 不是“是否包含”。 |
| `operator==(QFlags, Enum)` | 与单个枚举项精确比较。 | flags 有额外位时为 false。 |
| `operator==(Enum, QFlags)` | 上述比较的对称形式。 | 语义相同。 |
| `operator!=` 的三组形式 | 精确判断位模式不同。 | Qt 6.2 起的相关非成员重载。 |
| `qHash(QFlags, size_t seed)` | 为 QHash/QSet 提供哈希。 | Qt 6.2 起；不要作为稳定外部编码。 |

### 16.6 声明宏

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `Q_DECLARE_FLAGS(Flags, Enum)` | 声明 `Flags` 为 `QFlags<Enum>`。 | 不自动注册元对象。 |
| `Q_DECLARE_OPERATORS_FOR_FLAGS(Flags)` | 声明全局 `|`、`&`、`^`、`~` 及赋值运算符。 | 通常在 flags 别名后使用。 |
| `Q_FLAG(Flags)` | 在 QObject 元对象中注册 flags。 | 需要 `Q_OBJECT` 类；属于 QObject 宏体系。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 定位 | `QFlags<Enum>` | 类型安全保存枚举位组合。 | 不要用 int 替代。 |
| 类型 | `enum_type` | 模板枚举类型别名。 | 用于宏和泛型代码。 |
| 类型 | `Int` | 实际整数存储类型。 | 可能有符号、无符号、32 位或 64 位。 |
| 构造 | `QFlags()` | 创建空 flags。 | 所有位为 0。 |
| 构造 | `QFlags(Enum)` | 从枚举项创建 flags。 | 只设置该项的位。 |
| 构造 | `QFlags(initializer_list)` | OR 组合多个枚举项。 | 可读性好，适合固定组合。 |
| 构造 | `QFlags(QFlag)` | 32 位旧式整数兼容入口。 | 新代码优先 `fromInt()`。 |
| 构造 | `QFlags(in_place, Int)` | 按整数构造任意支持宽度的 flags。 | Qt 6.9 起；不验证未知位。 |
| 创建 | `fromInt(Int)` | 从原始位模式恢复。 | Qt 6.2 起；外部输入需先校验。 |
| 查询 | `toInt()` | 返回内部整数位模式。 | 返回类型随枚举底层类型和宽度变化。 |
| 查询 | `operator Int()` | 转成内部整数。 | `QT_TYPESAFE_FLAGS` 下变为显式。 |
| 查询 | `operator!()` | 判断是否为空。 | 空 flags 为 true。 |
| 设置 | `setFlag(flag, on)` | 确定地设置或清除位。 | 比 XOR 更不易出错。 |
| 匹配 | `testFlag(flag)` | 要求 flag 全部位存在。 | 组合项是 all-of；零项要求当前为空。 |
| 匹配 | `testAnyFlag(flag)` | 要求 flag 任一位存在。 | Qt 6.2 起；零项总是 false。 |
| 匹配 | `testFlags(flags)` | 要求参数 flags 全部位存在。 | Qt 6.2 起；空参数要求当前为空。 |
| 匹配 | `testAnyFlags(flags)` | 要求两个 flags 有任一交集。 | Qt 6.2 起；空参数总是 false。 |
| 位运算 | `|` / `|=` | 添加或合并位。 | 适合打开选项。 |
| 位运算 | `&` / `&=` | 取交集或应用 mask。 | 64 位优先用类型安全重载。 |
| 位运算 | `^` / `^=` | 切换位。 | 不表达确定的 on/off。 |
| 位运算 | `~` | 反转存储宽度内所有位。 | 可能包含保留位。 |
| 安全性 | `operator+/-` | 被删除以禁止数值加减。 | 使用位运算代替。 |
| 比较 | `operator==` / `!=` | 精确比较位模式。 | 不等同于包含判断。 |
| 哈希 | `qHash()` | 支持 QHash/QSet。 | Qt 6.2 起；不作为协议 hash。 |
| 声明 | `Q_DECLARE_FLAGS` | 创建 flags 类型别名。 | 不自动进元对象系统。 |
| 声明 | `Q_DECLARE_OPERATORS_FOR_FLAGS` | 创建枚举组合运算符。 | 通常紧跟 flags 别名。 |
| 元对象 | `Q_FLAG` | 注册 QObject flags 属性。 | 需要在 QObject 类中使用。 |
| 编译模式 | `QT_TYPESAFE_FLAGS` | 收紧整数兼容和 mask 运算。 | 可能暴露旧代码隐式转换问题。 |
| 版本边界 | Qt 6.9 64 位支持 | 支持最多 64 位枚举。 | 固定底层类型以保护 ABI。 |

### 一句话总结

`QFlags` 是“同一枚举的位组合值”，不是整数别名。用 `|` 组合、用 `testFlag` 判断全部、用 `testAnyFlag` 判断任一、用 `setFlag` 表达确定开关；跨整数边界时使用 `Int`、`fromInt()`、`toInt()`，需要元对象支持时再加 `Q_FLAG`。

