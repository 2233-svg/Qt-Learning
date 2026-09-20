# QFont::Tag

`QFont::Tag` 是 Qt 6.7 引入的四字节字体标签值类型。它把 OpenType 的特性名和可变轴名封装成类型安全的键，用于 `QFont::setFeature()`、`setVariableAxis()` 以及相应查询 API。

- 头文件：`#include <QFont>`
- 模块：`Qt6::Gui`
- 起始版本：Qt 6.7
- 类型特性：轻量值类型；可比较、可排序、可哈希、可流式读写

## 它解决的问题

OpenType 约定用四字符标签标识字体能力，例如 `"kern"` 是 kerning，`"liga"` 是标准连字，`"wght"` 是可变字体字重轴。直接使用字符串容易把长度、编码或字节顺序写错；`QFont::Tag` 明确约束这一协议，并能让固定字面量错误在编译期暴露。

```cpp
QFont font;
font.setFeature("tnum", 1);        // 四个 ASCII/Latin-1 字节
font.setVariableAxis("wght", 650);
```

字面量构造函数要求**恰好四个字符**，因此 `"frac"` 正确，`"fra"` 和 `"fraction"` 都会编译失败。运行时字符串则必须用 `fromString()`，因为它可能无效。

## 实际场景

**从配置文件读取特性。** 用户输入、JSON 或数据库里保存的是运行时字符串，先转换为 `std::optional<QFont::Tag>`，只在成功时应用。

```cpp
const auto tag = QFont::Tag::fromString(featureName);
if (tag)
    font.setFeature(*tag, value);
```

**检查可变字体轴。** `QFontInfo::variableAxes()` 返回一组 `QFontVariableAxis`，可用 `axis.tag()` 作键，匹配 `"wght"`、`"wdth"`、`"opsz"` 等轴。

**作为容器键。** `qHash()` 使其可用于 `QHash<QFont::Tag, quint32>`；三路比较支持排序语义。

## 表示与有效性

标签以大端形式压缩为 `quint32`：`"wght"` 对应四个按顺序写入的字节。默认构造的标签数值为 `0`，因此无效。`toString()` 返回的是四个原始字节的 `QByteArray`，不是面向用户翻译的名称。

`fromString()` 要求输入长度恰为四个字符；`fromValue(0)` 也失败。二者以 `std::nullopt` 传达无效输入，不要把无效值默认为某个特性。

标签有效不代表目标字体支持该特性或轴：它只说明键的形状合法。特性支持取决于选中的字体和 shaping 后端；变量轴范围应由 `QFontInfo::variableAxes()` 查询。

## API 速查表

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `Tag()` | 构造默认标签。 | 结果无效，`isValid()` 为 `false`。 |
| `Tag(const char (&str)[N])` | 从四字符窄字符串字面量构造标签。 | `N` 必须为 5（含末尾 `\0`）；只能用于编译期字面量，长度错误会编译失败。 |
| `static fromString(QAnyStringView view)` | 从运行时字符串构造 `std::optional<Tag>`。 | 长度不是四字符或得到零值时返回 `std::nullopt`；必须检查结果。 |
| `static fromValue(quint32 value)` | 从 32 位数值构造 `std::optional<Tag>`。 | `0` 无效；仅在外部协议明确采用同一字节顺序时使用。 |
| `isValid() const` | 判断内部数值是否非零。 | 只验证标签自身，不能验证字体是否提供该能力。 |
| `value() const` | 返回 32 位标签值。 | 适合底层协议/持久化，不适合用户可读显示。 |
| `toString() const` | 返回四字节 `QByteArray` 表示。 | 是原始字节序列，不保证是本地化或可显示文本。 |
| `comparesEqual(lhs, rhs)` | 比较两个标签是否相等。 | 通常直接使用 `==` 即可。 |
| `compareThreeWay(lhs, rhs)` | 提供强三路排序结果。 | 排序按内部数值，不是按语言学语义。 |
| `qHash(key, seed)` | 计算哈希值。 | 用于 `QHash` / `QSet`。 |
| `QDataStream <<` / `>>` | 序列化和反序列化标签。 | 由双方协商流版本；读入后仍可检查有效性。 |

## 易错点

1. 把 `QString` 直接传给字面量构造。运行时输入应使用 `fromString()`。
2. 以为 `"weight"` 是合法轴标签。标准权重轴是 `"wght"`，标签固定四字符。
3. 将无效标签传给 `setFeature()` 后期待自动纠正。应在转换点拒绝无效配置。
4. 认为 `isValid()` 等于“字体支持它”。要区分协议合法性和字体能力。
