# QJsonObject 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QJsonObject>`  
> 模块：`Qt6::Core`  
> 定位：由字符串键和 JSON 值组成的 JSON 对象

## 它解决什么问题

`QJsonObject` 表示 JSON 中的 `{...}`。接口响应、应用配置、请求参数这类“字段名决定含义”的数据，通常用它承接。它只负责 JSON 的结构和基本值，不负责业务字段是否齐全、类型是否合理、单位是否一致。

它是没有父对象、事件循环和信号槽的值类型。对象复制采用隐式共享，通常不会立刻复制全部数据；任一副本被写入时才分离。这个特性适合在函数间按值传递 JSON，但不等于可以忽略对象内容的实际大小。

```cpp
#include <QJsonObject>

QJsonObject user{
    {"id", 42},
    {"name", "Lin"},
    {"active", true},
};

const QString name = user.value("name").toString("anonymous");
user.insert("lastLogin", "2026-09-09");
```

构建时链接 `Qt6::Core`：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(myapp PRIVATE Qt6::Core)
```

## 读取字段：先分清缺失、null 和类型不匹配

`value(key)` 是只读查询。键不存在时返回 `QJsonValue::Undefined`，而 JSON 文本里的 `"key": null` 返回 `QJsonValue::Null`。这两个状态在 PATCH 请求、配置继承和接口兼容中往往有不同含义。

```cpp
const QJsonValue nickname = user.value("nickname");
if (nickname.isUndefined()) {
    // 服务端没有给出这个字段
} else if (nickname.isNull()) {
    // 服务端明确给出了 null
}
```

`toString(defaultValue)`、`toInt(defaultValue)` 适合给可选字段提供默认值，但类型不匹配时同样会落入默认值。面对不可信网络或文件输入，先 `isString()`、`isDouble()` 等检查类型，再做范围和业务校验。

## 写字段：`insert()` 与下标的区别

`insert(key, value)` 清楚表达“新增或覆盖字段”。`remove(key)` 仅删除，`take(key)` 删除并返回旧值，键不存在时 `take()` 返回 `Undefined`。

```cpp
if (user.contains("token"))
    user.remove("token");

const QJsonValue oldRole = user.take("role");
user.insert("role", "admin");
```

非 const `operator[]` 返回 `QJsonValueRef`，可以赋值回原对象，但只为读取而使用它会创建字段：

```cpp
QJsonObject options;
options["timeout"] = 5000; // 写入
options["missing"];        // 也会插入 "missing": null
```

只读请用 `value()`；const 对象的下标访问也只读取，找不到时返回 `Undefined`。

## 修改嵌套数据时必须写回

`toObject()` 和 `toArray()` 都返回值副本。修改副本后，需要放回父对象：

```cpp
QJsonObject root{{"profile", QJsonObject{{"name", "Lin"}}}};

QJsonObject profile = root.value("profile").toObject();
profile.insert("name", "Ming");
root.insert("profile", profile);
```

`root["profile"]["name"] = "Ming";` 也能写回，但路径中缺少键或类型不对时容易隐式创建数据。处理外部输入时，显式取出、检查类型、修改、写回的流程更容易发现协议错误。

## 遍历与迭代器

JSON object 不应被当成有业务顺序的容器。若需要排序显示或稳定签名，取得 `keys()` 后自行排序。

Qt 6.10 起，`asKeyValueRange()` 支持键和值的结构化绑定：

```cpp
for (auto [key, value] : user.asKeyValueRange()) {
    if (key == "active" && value.isBool())
        value = false;
}
```

`value` 是可写代理，会修改原对象。`insert()`、`remove()`、`take()` 等结构修改可能让已取得的迭代器和 `QJsonValueRef` 失效；遍历删除时使用 `erase()` 的返回迭代器继续，而不要继续使用旧迭代器。

## QVariant 转换的边界

`fromVariantMap()` / `toVariantMap()` 和 `fromVariantHash()` / `toVariantHash()` 便于和动态 Qt 数据接口衔接。它们不是任意 `QVariant` 的无损 JSON 协议。日期、自定义类型、二进制值等应先约定明确的文本或对象格式，再转换。

## 常见误区

- `value("x")` 得到空字符串，不代表键一定存在；检查 `Undefined` 与 `Null`。
- 只读时调用非 const `object["x"]`，意外写入 `null` 字段。
- 修改 `toObject()` 的结果后忘记插回父对象。
- 把迭代顺序当作业务顺序。
- 将 `QJsonValueRef` 保存到对象修改或销毁之后；需要长期持有时转成 `QJsonValue`。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造与赋值 | `QJsonObject()` | 创建空对象。 | 空对象可直接 `insert()`。 |
| 构造与赋值 | `QJsonObject(std::initializer_list<std::pair<QString, QJsonValue>>)` | 以键值对列表构造对象。 | 用于小型固定结构最清晰。 |
| 构造与赋值 | 拷贝、移动构造和 `operator=` | 复制或转移对象值。 | 值类型且隐式共享，修改副本不改原对象。 |
| 构造与赋值 | `swap(QJsonObject &)` | 交换两个对象内容。 | 交换后变量对应的数据互换。 |
| 查询 | `size()`、`count()`、`length()` | 返回成员数量。 | 三者在本类中等价，常用 `size()`。 |
| 查询 | `isEmpty()`、`empty()` | 判断对象是否没有成员。 | `empty()` 是 STL 风格别名。 |
| 查询 | `keys()` | 返回所有键。 | 不把返回顺序当成 JSON 的业务顺序。 |
| 查询 | `value(QString / QStringView / QLatin1StringView)` | 按键读取 JSON 值。 | 不修改对象；未找到返回 `Undefined`。 |
| 查询 | `contains(QString / QStringView / QLatin1StringView)` | 判断键是否存在。 | 用于区分缺失字段和字段值为 `null`。 |
| 查询 | const `operator[](QString / QStringView / QLatin1StringView)` | 按键读取值。 | 返回独立 `QJsonValue`，缺失时为 `Undefined`。 |
| 修改 | `insert(QString / QStringView / QLatin1StringView, const QJsonValue &)` | 新增或覆盖一个成员。 | 可写入任何 JSON 值；结构修改后旧迭代器可能失效。 |
| 修改 | 非 const `operator[](QString / QStringView / QLatin1StringView)` | 取得可写的 `QJsonValueRef`。 | 缺失键会被创建为 `null`，只读请改用 `value()`。 |
| 修改 | `remove(QString / QStringView / QLatin1StringView)` | 删除指定键。 | 键不存在时无效果。 |
| 修改 | `take(QString / QStringView / QLatin1StringView)` | 删除指定键并取回旧值。 | 键不存在返回 `Undefined`。 |
| 迭代 | `begin()`、`end()` | 返回可写范围的起止迭代器。 | 非 const `begin()` 获取可写数据；避免遍历中随意改结构。 |
| 迭代 | const `begin()`、const `end()`、`constBegin()`、`constEnd()` | 返回只读迭代器。 | 只读遍历优先使用。 |
| 迭代 | `find()`、`constFind()` | 查找键，未命中返回 `end()`。 | 迭代器可用 `key()`、`keyView()` 和 `value()` 取内容。 |
| 迭代 | `erase(iterator)` | 删除当前位置并返回后继迭代器。 | 用于遍历中删除。 |
| 键值遍历，Qt 6.10 起 | `keyValueBegin()`、`keyValueEnd()` | 返回可读写键值迭代器。 | 解引用可得到键和值，值仍受迭代器有效期约束。 |
| 键值遍历，Qt 6.10 起 | `constKeyValueBegin()`、`constKeyValueEnd()` | 返回只读键值迭代器。 | 避免复制键和值。 |
| 键值范围，Qt 6.10 起 | `asKeyValueRange()` 的四个重载 | 提供可结构化绑定的键值范围。 | 左值范围引用原对象；右值范围接管临时对象避免悬垂。 |
| QVariant 转换 | `fromVariantMap()`、`fromVariantHash()` | 从 Qt 映射类型生成 JSON 对象。 | 只对 JSON 可表达的数据期待稳定含义。 |
| QVariant 转换 | `toVariantMap()`、`toVariantHash()` | 转成 Qt 动态映射类型。 | 适合边界层，不替代强类型业务模型。 |
| 类型别名 | `Iterator`、`ConstIterator`、`key_type`、`mapped_type`、`size_type` | 提供 STL 风格的迭代器和容器类型名。 | 业务代码通常用 `auto` 或范围 for 即可。 |
| 散列、调试与流 | `qHash()`、`QDebug operator<<`、`QDataStream << / >>` | 支持哈希、调试输出和 Qt 二进制流。 | `QDataStream` 不是 JSON 文本协议。 |

## 一句话总结

`QJsonObject` 用字段名组织 JSON。读取用 `value()`，写入用 `insert()`，嵌套副本修改后写回；把 `Undefined`、`null` 和 `QJsonValueRef` 的边界分清，代码会可靠得多。
