# QCborMap 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCborMap>`  
> 模块：`Qt6::Core`  
> 定位：保存 `QCborValue` 键和值的 CBOR map

## 它解决什么问题

`QCborMap` 表示 CBOR 的 map。它与 `QJsonObject` 最大的不同是键不局限于字符串：整数键、字符串键和可表示的 `QCborValue` 键都能使用。因此它适合 CBOR 协议中的紧凑整数键、标准标签数据及保留原始 CBOR 结构的配置或消息。

它是隐式共享值类型。复制 map 通常很轻，修改某个副本时才分离；不需要 QObject 所有权或事件循环。

```cpp
QCborMap message{
    {0, "Hello"},
    {1, 42},
    {"metadata", QCborMap{{"source", "sensor"}}},
};

const QCborValue id = message.value(1);
message.insert("retry", 3);
```

## 键和值的语义

`value(key)` 是只读查询。键不存在时返回默认构造的 `QCborValue`，即 CBOR `Undefined`；它与合法的 CBOR `Null` 不同。用 `contains()` 区分“键缺失”和“键存在但值为空”。

```cpp
if (!message.contains("metadata")) {
    // 缺少字段
} else if (message.value("metadata").isNull()) {
    // 字段明确为 null
}
```

`insert()` 新增或覆盖同一键，`remove()` 只删除，`take()` 删除并返回旧值。非 const `operator[]` 返回 `QCborValueRef`，键不存在时会创建成员；只读时应使用 `value()`，避免无意写入。

## 不要把它当作 JSON object

`toJsonObject()` 和 `fromJsonObject()` 只适合键可以表示为 JSON 字符串的部分数据。整数键、字节串、标签、浮点特殊值等 CBOR 能力在 JSON 转换时可能丢失或改变语义。

`toVariantMap()` / `toVariantHash()` 同样偏向字符串键的 Qt 动态数据模型。需要保留完整 CBOR map 时，用 `QCborValue`、`toCborValue()` 和 `toCbor()` 路径，而不是通过 JSON 或 QVariant 绕行。

## 遍历与修改

`Iterator` 可以改值，`ConstIterator` 只能读取；map 一经修改，已有迭代器及 `QCborValueRef` 都可能失效。需要删除遍历中的成员时，使用 `erase()` 返回的后继迭代器。

Qt 6.10 起的 `asKeyValueRange()` 适合结构化绑定：

```cpp
for (auto [key, value] : message.asKeyValueRange()) {
    if (key.isInteger() && key.toInteger() == 1)
        value = 43;
}
```

键不可通过迭代器就地改写；要改键，取值、删除旧键、插入新键。

## 常见误区

- 假设键总是字符串，丢失整数键的协议优势。
- 查询时使用非 const `operator[]`，意外创建 `Undefined` 成员。
- 通过 JSON 转换保存带非字符串键的 CBOR map。
- 修改容器后继续使用旧迭代器或 `QCborValueRef`。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造与赋值 | `QCborMap()`、初始化列表构造、拷贝移动与 `swap()` | 创建、复制或交换 CBOR map。 | 初始化列表允许整数和字符串键；值类型隐式共享。 |
| 大小 | `size()`、`isEmpty()`、`empty()`、`clear()` | 查询或清空成员。 | `clear()` 使已有迭代器失效。 |
| 键 | `keys()` | 返回所有键的 `QList<QCborValue>`。 | 键不保证是字符串，也不应当作业务排序。 |
| 查询 | `value(qint64 / QString / QLatin1StringView / QCborValue)` | 按键读取值。 | 缺失键返回 `Undefined`；用 `contains()` 区分缺失和 null。 |
| 查询 | `contains(...)` | 判断键是否存在。 | 支持整数、字符串和通用 CBOR 值键。 |
| 查询 | const `operator[](...)` | 按键读取值。 | 不修改 map，缺失时返回 `Undefined`。 |
| 写入 | `insert(value_type)`、`insert(key, value)` | 新增或覆盖键值对。 | 已有相等键会被覆盖；结构修改会影响迭代器。 |
| 写入 | 非 const `operator[](...)` | 返回可写 `QCborValueRef`。 | 缺失键会创建成员；仅读取请用 `value()`。 |
| 删除 | `remove(...)`、`take(...)` | 删除键，或删除并取回旧值。 | `take()` 缺失时返回 `Undefined`。 |
| 查找 | `find()`、`constFind()` | 返回键的迭代器，未命中为 `end()`。 | 遍历时修改 map 后不再使用旧迭代器。 |
| 迭代 | `begin/end`、`constBegin/constEnd`、`cbegin/cend` | 获得可写或只读迭代器范围。 | 只读优先 `ConstIterator`。 |
| 迭代 | `erase(iterator)`、`extract(iterator)` | 删除当前项，或删除并返回它的值。 | 使用返回迭代器继续删除遍历。 |
| 键值遍历，Qt 6.10 起 | `keyValueBegin/End`、`asKeyValueRange()` | 提供键值迭代和结构化绑定。 | 可写范围只有值可修改，键仍只读。 |
| JSON 转换 | `fromJsonObject()`、`toJsonObject()` | 在 JSON object 与 CBOR map 间转换。 | 非字符串键和 CBOR 扩展类型可能无法无损表示。 |
| QVariant 转换 | `fromVariantMap/Hash()`、`toVariantMap/Hash()` | 与 Qt 动态映射类型互转。 | 适合边界层，不替代完整 CBOR 表达。 |
| CBOR 协作 | `toCborValue()`、`compare()`、比较运算符 | 包装为 `QCborValue` 或比较 map。 | 比较规则不等同于业务上的字段排序。 |
| 类型别名 | `key_type`、`mapped_type`、`value_type`、迭代器别名 | 暴露 STL 风格容器类型。 | `value_type` 是键和值的 pair。 |

## 一句话总结

`QCborMap` 是保留 CBOR 键类型能力的映射容器。查询优先 `value()`，写入用 `insert()`，不要把 JSON 转换当作无损通道，并在修改后放弃旧迭代器和引用代理。
