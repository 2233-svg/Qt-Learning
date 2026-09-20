# QJsonArray 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QJsonArray>`  
> 模块：`Qt6::Core`  
> 定位：按索引保存 JSON 值的有序序列

## 它解决什么问题

`QJsonArray` 表示 JSON 的 `[...]`。商品列表、批量请求、轨迹点、日志记录等“顺序或位置有含义”的数据，适合放在数组中。

它是值类型并采用隐式共享；数组可包含任意 JSON 类型的元素，既可以全是对象，也可以混有字符串、数值和 `null`。这很适合承接外部 JSON，但业务代码不能据此假定元素同构，读取时仍要验证类型。

```cpp
#include <QJsonArray>
#include <QJsonObject>

QJsonArray products{
    QJsonObject{{"id", 1}, {"name", "Keyboard"}},
    QJsonObject{{"id", 2}, {"name", "Mouse"}},
};

for (const QJsonValue &value : std::as_const(products)) {
    const QJsonObject product = value.toObject();
    qDebug() << product.value("name").toString();
}
```

构建系统只需链接 `Qt6::Core`。

## 索引与边界

数组从 0 开始索引，索引类型为 `qsizetype`。`at(i)` 与 const `operator[](i)` 越界时返回 `QJsonValue::Undefined`，而不是抛异常。

```cpp
const QJsonValue third = products.at(2);
if (third.isUndefined()) {
    // 没有第三项
}
```

`first()`、`last()`、`removeFirst()`、`removeLast()` 要求数组非空。对外部输入或可能为空的列表，先用 `isEmpty()`；需要把越界当协议错误时，显式检查 `i >= 0 && i < array.size()`。

## 添加、替换和移除

`append()` 追加到末尾，`prepend()` 插到开头，`insert(i, value)` 在索引 `i` 前插入，`replace(i, value)` 覆盖一个已有元素。`removeAt(i)` 删除，`takeAt(i)` 删除并返回旧值。

```cpp
QJsonArray queue;
queue.append("normal");
queue.prepend("urgent");
queue.insert(1, "medium");

const QJsonValue processed = queue.takeAt(0);
```

`push_back()`、`push_front()`、`pop_back()`、`pop_front()` 是 STL 风格别名；`operator<<` 与 `operator+=` 也是追加。实际项目建议统一使用 `append()`，组装 JSON 时最容易读懂。

非 const `operator[]` 给出 `QJsonValueRef`，能就地赋值：

```cpp
if (products.at(0).isObject())
    products[0] = QJsonObject{{"id", 1}, {"name", "Updated"}};
```

它只能用于已有索引，且是容器元素的代理，不应跨容器修改长期保存。

## 修改嵌套数据要写回

`toObject()` / `toArray()` 返回副本；改完后必须放回数组：

```cpp
QJsonObject item = products.at(0).toObject();
item.insert("selected", true);
products.replace(0, item);
```

如果 `products.at(0)` 并非对象，`toObject()` 会得到空对象。处理不可信 JSON 时，应先 `isObject()`，否则可能把异常原始数据悄悄替换成看似合法的新对象。

## 遍历与迭代器

只读遍历使用 `const QJsonArray &` 或 `std::as_const(array)`。要就地规范字符串等元素，可使用可写代理：

```cpp
for (QJsonValueRef value : products) {
    if (value.isString())
        value = value.toString().trimmed();
}
```

`append()`、`prepend()`、`insert()`、`removeAt()`、`takeAt()` 等结构修改后，之前取得的迭代器、引用和 `QJsonValueRef` 都不应继续使用。删除遍历中的元素时，使用 `erase()` 返回的后继迭代器，或倒序按索引处理。

## 与 QStringList / QVariantList 的转换

`fromStringList()` 明确地把每个字符串转成 JSON string。`fromVariantList()` / `toVariantList()` 适合动态 Qt 数据接口，但不是协议设计工具：日期、字节数组、自定义类型应由接口明确约定它们的 JSON 表示。

## 常见误区

- 假定 JSON 数组元素类型一致；外部数据应先 `isObject()`、`isString()` 等检查。
- 在空数组上调用 `first()`、`last()` 或 `removeLast()`。
- 改了 `toObject()` / `toArray()` 返回值却没有 `replace()` 回去。
- 在范围 for 内追加或删除，导致代理和迭代器失效。
- 把 `at()` 越界后的 `Undefined` 当成完整的错误处理。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造与赋值 | `QJsonArray()` | 创建空数组。 | 之后可用 `append()` 逐项构建。 |
| 构造与赋值 | `QJsonArray(std::initializer_list<QJsonValue>)` | 用初始值列表构造数组。 | 适合元素很少且结构固定的数组。 |
| 构造与赋值 | 拷贝、移动构造和 `operator=` | 复制或转移数组值。 | 值语义与隐式共享，修改副本不影响原数组。 |
| 构造与赋值 | `swap(QJsonArray &)` | 交换两个数组内容。 | 交换整个容器，不是逐元素交换。 |
| 查询 | `size()`、`count()` | 返回元素数量。 | 两者等价，通常选 `size()`。 |
| 查询 | `isEmpty()`、`empty()` | 判断是否为空。 | `empty()` 是 STL 风格别名。 |
| 查询 | `at(qsizetype)` | 读取指定索引元素。 | 越界返回 `Undefined`。 |
| 查询 | const `operator[](qsizetype)` | 读取指定索引元素。 | 同样越界返回 `Undefined`，返回值为副本。 |
| 查询 | `first()`、`last()` | 读取首尾元素。 | 数组为空时不可调用。 |
| 查询 | `contains(const QJsonValue &)` | 判断数组是否含有相等的 JSON 值。 | 比较的是 JSON 内容，不是业务对象标识。 |
| 修改 | `append(const QJsonValue &)` | 在末尾追加元素。 | 构建 JSON 列表的首选接口。 |
| 修改 | `prepend(const QJsonValue &)` | 在开头插入元素。 | 后面元素的索引整体右移。 |
| 修改 | `insert(qsizetype, const QJsonValue &)` | 在指定位置前插入元素。 | 插入后后续元素索引会变化。 |
| 修改 | `replace(qsizetype, const QJsonValue &)` | 覆盖已有索引的元素。 | 仅用于有效索引，不把它当成追加。 |
| 修改 | 非 const `operator[](qsizetype)` | 返回可写的 `QJsonValueRef`。 | 索引必须有效；代理不应跨修改长期保存。 |
| 修改 | `removeAt(qsizetype)` | 删除指定索引元素。 | 删除后后续元素左移，先检查边界。 |
| 修改 | `takeAt(qsizetype)` | 删除指定索引并返回旧元素。 | 返回独立值，适合取出后继续处理。 |
| 修改 | `removeFirst()`、`removeLast()` | 删除首尾元素。 | 空数组不可调用。 |
| STL 便捷接口 | `push_back()`、`push_front()` | 分别等价于 `append()`、`prepend()`。 | 选择一种团队风格保持一致。 |
| STL 便捷接口 | `pop_back()`、`pop_front()` | 分别删除末尾、开头元素。 | 空数组不可调用。 |
| 追加运算符 | `operator+`、`operator+=`、`operator<<` | 复制后追加，或向当前数组追加。 | `operator+` 会产生新数组；批量构建更宜用 `append()`。 |
| 迭代 | `begin()`、`end()` | 返回可写迭代器范围。 | 结构修改后此前迭代器可能失效。 |
| 迭代 | const `begin()`、const `end()`、`constBegin()`、`constEnd()`、`cbegin()`、`cend()` | 返回只读迭代器范围。 | 只读遍历优先使用，避免无意分离数据。 |
| 迭代 | `insert(iterator, const QJsonValue &)` | 在迭代器位置前插入并返回位置迭代器。 | 传入的迭代器必须属于当前数组且仍有效。 |
| 迭代 | `erase(iterator)` | 删除迭代器位置并返回后继迭代器。 | 删除遍历时使用返回值继续。 |
| QVariant 转换 | `fromStringList()` | 从 `QStringList` 构建 JSON 字符串数组。 | 每个元素都成为 JSON string。 |
| QVariant 转换 | `fromVariantList()`、`toVariantList()` | 在 `QVariantList` 与 JSON 数组之间转换。 | 自定义 `QVariant` 类型的语义须另行约定。 |
| 类型别名 | `Iterator`、`ConstIterator` 和 STL 兼容别名 | 提供迭代器、引用及大小类型。 | 常规代码用 `auto` 和范围 for 即可。 |
| 散列、调试与流 | `qHash()`、`QDebug operator<<`、`QDataStream << / >>` | 支持哈希、调试输出和 Qt 二进制流。 | 二进制流不是 JSON 文本。 |

## 一句话总结

`QJsonArray` 是有序的 JSON 值集合。用 `append()` 组装，读取外部数据时检查类型和边界，修改嵌套值后写回；数组的引用与迭代器有效期需要格外小心。
