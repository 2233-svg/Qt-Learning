# QCborArray 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCborArray>`  
> 模块：`Qt6::Core`  
> 定位：按顺序保存 `QCborValue` 的 CBOR 数组

## 它解决什么问题

`QCborArray` 表示 CBOR array。它适合消息参数列表、二进制字段集合、坐标序列和嵌套记录等“位置有含义”的 CBOR 数据。元素是 `QCborValue`，因此可保留 JSON 没有的 CBOR 类型，例如 byte string、tag、`Undefined` 与更丰富的数值表达。

它是隐式共享的值类型，复制后任一副本写入时才分离。它没有元素类型约束，读取外部数据时仍须逐项检查类型。

```cpp
QCborArray packet{
    1,
    "sensor-A",
    QByteArray::fromHex("0102"),
    QCborMap{{"ok", true}},
};

packet.append(QCborValue::Null);
```

## 索引、读取和修改

索引从 0 开始，类型为 `qsizetype`。`at(i)` 和 const `operator[]` 越界时返回默认 `QCborValue`，即 `Undefined`；它们不抛出异常。`first()`、`last()`、`removeFirst()`、`removeLast()` 则要求数组非空，调用前先 `isEmpty()`。

非 const `operator[]` 返回 `QCborValueRef`，允许原地写入已有元素：

```cpp
if (packet.at(3).isMap())
    packet[3] = QCborMap{{"ok", false}};
```

`QCborValueRef` 是容器元素代理，不是独立值。数组结构改变后，不要继续保存或使用已有代理、引用和迭代器。

## 增删与嵌套写回

`append()` 在尾部加入，`prepend()` 在头部加入，`insert()` 插入，`replace()` 覆盖已有索引。`removeAt()` 删除，`takeAt()` 删除并返回旧值。`push_back()` 等是 STL 风格别名。

从数组取出 map 或 array 后得到值副本，修改后应显式写回：

```cpp
QCborMap meta = packet.at(3).toMap();
meta.insert("ok", false);
packet.replace(3, meta);
```

处理不可信数据时，先检查 `isMap()` / `isArray()`。否则 `toMap()` 产生的空 map 可能会在写回时覆盖原先的异常数据。

## CBOR 与 JSON 转换边界

`fromJsonArray()` / `toJsonArray()` 方便与 JSON 层互通，但并不是无损 CBOR 传输：byte string、标签、特殊类型或某些数值语义可能无法完整表达。需要保持 CBOR 原始能力时，使用 `toCborValue()` 与 `QCborValue::toCbor()`。

`fromStringList()`、`fromVariantList()`、`toVariantList()` 适合 Qt 动态接口。协议边界上仍应明确约定日期、二进制值和自定义类型的表示。

## 常见误区

- 把 `Undefined` 视作数组越界的异常；它只是返回值，业务层仍应判断边界。
- 在空数组上调用 `first()`、`last()` 或首尾删除接口。
- 修改 `toMap()` 或 `toArray()` 的副本后忘记写回。
- 在遍历过程中插入或删除，继续使用旧迭代器。
- 把 JSON 转换当作 CBOR byte string、tag 等类型的无损通道。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造与赋值 | `QCborArray()`、初始化列表构造、拷贝移动与 `swap()` | 创建、复制或交换数组。 | 元素可为任意 `QCborValue` 类型。 |
| 大小 | `size()`、`isEmpty()`、`empty()`、`clear()` | 查询或清空元素。 | 清空和结构修改会使迭代器与代理失效。 |
| 查询 | `at(qsizetype)`、const `operator[]` | 按索引读取元素。 | 越界返回 `Undefined`，不等于异常处理完成。 |
| 查询 | `first() const`、`last() const` | 读取首尾元素。 | 空数组不可调用。 |
| 查询 | `contains(const QCborValue &)` | 判断是否含有相等元素。 | 比较的是 CBOR 值，不是业务 ID。 |
| 修改 | `append()`、`prepend()` | 在尾部或头部添加元素。 | `prepend()` 会改变现有元素索引。 |
| 修改 | `insert(qsizetype, value)`、迭代器 `insert()` | 在位置前插入元素。 | 后续元素索引变化，旧迭代器可能失效。 |
| 修改 | `replace(qsizetype, value)` | 覆盖已有元素。 | 先确认索引有效。 |
| 修改 | 非 const `operator[]`、非 const `first()`、`last()` | 获取可写 `QCborValueRef`。 | 代理不能在数组修改或销毁后继续使用。 |
| 删除 | `removeAt()`、`removeFirst()`、`removeLast()` | 删除指定或首尾元素。 | 首尾接口不能用于空数组。 |
| 删除 | `takeAt()`、`takeFirst()`、`takeLast()` | 删除并返回旧元素。 | 返回的是独立 `QCborValue`。 |
| 迭代 | `begin/end`、`constBegin/constEnd`、`cbegin/cend` | 获得可写或只读迭代范围。 | 只读遍历优先 const 版本。 |
| 迭代 | `erase(iterator)`、`extract(iterator)` | 删除当前元素，或删除并取回它。 | 遍历删除时接住返回迭代器继续。 |
| STL 便捷 | `push_back/front`、`pop_back/front`、`operator+=`、`operator<<`、`operator+` | 提供 STL 风格添加删除和追加。 | 团队代码最好统一以 `append()` 为主。 |
| JSON 转换 | `fromJsonArray()`、`toJsonArray()` | 在 JSON 数组与 CBOR 数组间转换。 | CBOR 特有类型可能丢失语义。 |
| QVariant 转换 | `fromStringList()`、`fromVariantList()`、`toVariantList()` | 与字符串列表和动态 Qt 列表互转。 | 自定义 QVariant 的协议表达需明确。 |
| CBOR 协作 | `toCborValue()`、`compare()`、比较运算符 | 包装为 CBOR 值或比较数组。 | 比较规则不等于业务排序规则。 |
| 类型别名 | `value_type`、`reference`、`const_reference`、迭代器别名 | 提供 STL 兼容类型。 | 可写引用实际为 `QCborValueRef` 代理。 |

## 一句话总结

`QCborArray` 是有序 CBOR 值序列。用 `append()` 组装、用类型检查保护外部输入、修改嵌套副本后写回；索引越界、代理引用和 JSON 转换损失是最需要留意的边界。
