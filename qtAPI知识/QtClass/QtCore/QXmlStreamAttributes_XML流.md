# Qt QXmlStreamAttributes：一组 XML 属性及其命名空间查询

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QXmlStreamAttributes>`  
> 所属模块：`Qt6::Core`  
> 继承：`QList<QXmlStreamAttribute>`  
> 类型性质：可复制的值容器；函数可重入

## 它解决的问题

XML 元素的属性不是一个简单的 `QString -> QString` 映射。每个属性至少包含：

- 限定名，例如 `xlink:href`；
- 局部名，例如 `href`；
- 解析后的命名空间 URI；
- 属性值。

`QXmlStreamAttributes` 用一个有序容器保存这些 `QXmlStreamAttribute`，并提供按限定名或按“命名空间 URI + 局部名”查找的便捷函数。它主要连接两个场景：

1. `QXmlStreamReader` 读到开始元素时，使用 `attributes()` 取得当前元素的属性；
2. `QXmlStreamWriter` 写开始元素后，使用 `writeAttributes()` 批量写出属性。

它不是通用的 XML DOM 属性节点，也不维护独立的命名空间作用域。它只是当前属性集合的值容器，命名空间解析和序列化规则仍由读写器负责。

## 真实使用场景

### 读取协议属性

```cpp
QXmlStreamReader reader(device);

while (!reader.atEnd()) {
    reader.readNext();
    if (!reader.isStartElement())
        continue;

    const QXmlStreamAttributes attrs = reader.attributes();
    if (attrs.hasAttribute({}, u"version"_s)) {
        const QString version = attrs.value({}, u"version"_s).toString();
        qDebug() << "version =" << version;
    }
}

if (reader.hasError())
    qWarning() << reader.errorString();
```

这里按空命名空间和局部名查询，表达的是 XML 语义，而不是依赖输入文件里是否写成某个前缀。

### 过滤后再写出

```cpp
QXmlStreamAttributes output;
for (const QXmlStreamAttribute &attribute : reader.attributes()) {
    if (attribute.name() != u"internal"_s)
        output.append(attribute);
}

writer.writeStartElement(reader.qualifiedName());
writer.writeAttributes(output);
writer.writeEndElement();
```

继承的 `QList` `append(const QXmlStreamAttribute &)` 仍然可用。属性顺序会被保留，因此除非协议明确允许，否则不要为了“看起来整齐”而任意排序。

## 对象模型和边界

`QXmlStreamAttributes` 是 `QList<QXmlStreamAttribute>` 的公开派生类。它有一个内联无参构造函数，没有额外的资源所有权，也不拥有 reader 或 writer。复制容器会复制属性值语义，不会让容器绑定到某个流设备。

它继承 `QList` 的大小、索引、迭代器、插入、删除和遍历 API。换句话说，下面这些操作遵守 `QList` 的通常语义：

- `isEmpty()`、`size()`、`count()` 查询容器状态；
- `at()`、`operator[]`、范围 `for` 读取元素；
- `append(QXmlStreamAttribute)`、`prepend()`、`insert()` 增加元素；
- `removeAt()`、`removeAll()`、`clear()` 删除元素。

本类新增的 `append` 重载与继承的 `append(QXmlStreamAttribute)` 共存；头文件通过 `using QList<QXmlStreamAttribute>::append` 避免基类重载被隐藏。容器中的属性可以重复，`value()` 和 `hasAttribute()` 面向查找场景时应把“重复项由业务如何处理”想清楚。

## 限定名查询不是命名空间查询

```cpp
const bool lexical = attrs.hasAttribute(u"xlink:href"_s);
const bool semantic = attrs.hasAttribute(
    u"http://www.w3.org/1999/xlink"_s,
    u"href"_s);
```

第一种查询比较属性的原始限定名。它适合处理明确要求保留某个词法形式的旧协议或文本转换，但不是命名空间感知查询。`xlink` 前缀在不同元素作用域中可能绑定到不同 URI；不同前缀也可能绑定到同一个 URI。

第二种查询比较命名空间 URI 和局部名，适合协议判断、格式兼容和跨文档处理。命名空间 URI 参数可以为空，空 URI 表示无命名空间；属性局部名则应传局部名，不要传 `prefix:name`。

同样的区别适用于 `value()`：

- `value(qualifiedName)` 按限定名查找；
- `value(namespaceUri, name)` 按解析后的 URI 和局部名查找。

## `hasAttribute()` 与空值属性

不要用下面的写法判断属性是否存在：

```cpp
if (!attrs.value(u"enabled"_s).isEmpty()) {
    // ...
}
```

XML 允许属性存在但值为空，例如 `enabled=""`。空值和属性不存在是两个不同状态。应使用：

```cpp
if (attrs.hasAttribute(u"enabled"_s)) {
    const QString value = attrs.value(u"enabled"_s).toString();
    // value 可能是空字符串，但属性确实存在
}
```

`value()` 找不到属性时返回空字符串视图。需要区分“未找到”和“找到了空值”时，始终先调用对应的 `hasAttribute()`。

## `QStringView` 的生命周期

两个 `value()` 重载都返回 `QStringView`，它不拥有字符数据。视图适合在当前容器仍然有效、且不跨越相关存储修改的短代码段中读取：

```cpp
const QStringView raw = attrs.value({}, u"id"_s);
const QString id = raw.toString(); // 需要长期保存时复制
```

如果属性来自 reader 当前 token，或容器随后会被清空、重新赋值、销毁，就不要把返回视图保存到更长生命周期的成员中。异步任务、跨线程队列和缓存通常应保存 `QString`，而不是保存 `QStringView`。

`QXmlStreamAttributes` 的函数是可重入的，但这不等于同一个容器可以被多个线程同时修改。跨线程传递时使用值复制，并遵守应用自己的同步规则。

## 构造和添加属性

无参构造得到空容器：

```cpp
QXmlStreamAttributes attributes;
```

按命名空间添加属性时，第二个参数是局部名：

```cpp
attributes.append(
    u"http://www.w3.org/XML/1998/namespace",
    u"id",
    u"book-7");
```

不要把 `xml:id` 作为第二个参数传给这个重载。若要直接保留限定名，使用另一个重载：

```cpp
attributes.append(u"xml:id", u"book-7");
```

这两个调用表达的是不同输入模型：前者提供已解析的 URI 和局部名，后者提供原始限定名。前者不会根据某个前缀字符串自动推导 URI，后者也不会替你验证前缀绑定是否符合当前文档上下文。

## 与 writer 的协作

`writeAttributes()` 会按照容器当前顺序写出属性。用 `QXmlStreamAttribute` 携带命名空间信息时，命名空间声明、前缀选择和元素上下文仍应交给 `QXmlStreamWriter` 的命名空间 API 管理。不要把属性容器当作一段可随意拼接的 XML 文本。

如果只是把 reader 的属性复制到另一个 writer，需明确目标文档是否保留原始限定名，还是要按 URI 和局部名重新序列化。两种需求对应不同的 API 选择，不能只靠 `qualifiedName()` 作为长期身份。

## API 逐项说明

### `QXmlStreamAttributes()`

构造空的属性容器。它不接收设备、reader 或初始容量参数，也不代表当前存在一个 XML 元素。

### `append(const QString &namespaceUri, const QString &name, const QString &value)`

追加一个属性。`namespaceUri` 是命名空间 URI，可以为空；`name` 是局部名；`value` 是属性值。该函数适合调用方已经拥有命名空间解析结果的场景。

它不会替现有属性去重，也不会检查同一元素上是否已经有相同的命名身份。XML 合法性和重复属性约束应由输入校验或上层逻辑负责。

### `append(const QString &qualifiedName, const QString &value)`

按限定名追加属性。`qualifiedName` 是 XML 中的词法名称，可能包含 `prefix:`。这个重载保存的是调用方提供的限定名，不负责根据前缀解析命名空间 URI。

### `hasAttribute(QAnyStringView qualifiedName) const`

当容器中有与 `qualifiedName` 相同的限定名时返回 `true`。这是词法查询，不是命名空间感知查询。找不到时返回 `false`。

### `hasAttribute(QAnyStringView namespaceUri, QAnyStringView name) const`

当容器中有命名空间 URI 和局部名均匹配的属性时返回 `true`。这是协议代码更应优先使用的查询形式。空 URI 表示无命名空间。

### `value(QAnyStringView qualifiedName) const noexcept`

按限定名查找并返回属性值。找不到时返回空字符串视图；返回值不拥有底层字符数据。它是 `noexcept`，但这不改变视图的生命周期约束。

### `value(QAnyStringView namespaceUri, QAnyStringView name) const noexcept`

按命名空间 URI 和局部名查找并返回属性值。找不到时返回空字符串视图。第二个参数是局部名，不是限定名；需要判断属性存在时配合同签名的 `hasAttribute()`。

## 继承自 `QList` 的常用公开 API

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `isEmpty()` / `size()` / `count()` | 查询属性数量和空状态 | 容器可能为空；数量不等于 XML 元素是否合法。 |
| `at(i)` / `operator[](i)` | 按位置访问属性 | 访问边界遵守 `QList` 语义；`operator[]` 的可写形式可修改元素。 |
| `begin()` / `end()` | 遍历属性 | 顺序是容器顺序；范围 `for` 最适合只读遍历。 |
| `append(const QXmlStreamAttribute &)` | 追加已有属性对象 | 这是继承自 `QList` 的重载，与本类两个字符串重载同时可用。 |
| `prepend()` / `insert()` | 在指定位置添加属性 | 会改变写出顺序；不负责 XML 语义去重。 |
| `removeAt()` / `removeAll()` / `clear()` | 删除属性 | 删除后原有迭代器、引用或相关视图可能不再适合继续使用。 |

## API 速查表

| 类别 | API | 用途 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QXmlStreamAttributes()` | 创建空属性容器 | 不绑定 reader、writer 或设备。 |
| 添加 | `append(const QString &namespaceUri, const QString &name, const QString &value)` | 用 URI、局部名和值追加属性 | `name` 是局部名；空 URI 表示无命名空间；不自动去重。 |
| 添加 | `append(const QString &qualifiedName, const QString &value)` | 用原始限定名和值追加属性 | 不根据前缀解析 URI，也不替调用方验证命名空间绑定。 |
| 查询 | `hasAttribute(QAnyStringView qualifiedName) const` | 按限定名判断属性存在 | 词法查询，不等同于 URI+局部名查询。 |
| 查询 | `hasAttribute(QAnyStringView namespaceUri, QAnyStringView name) const` | 按命名空间 URI 和局部名判断存在 | 第二个参数是局部名；空 URI 代表无命名空间。 |
| 取值 | `QStringView value(QAnyStringView qualifiedName) const noexcept` | 按限定名取得值 | 找不到返回空视图；不要用空值判断存在性。 |
| 取值 | `QStringView value(QAnyStringView namespaceUri, QAnyStringView name) const noexcept` | 按 URI 和局部名取得值 | 返回非拥有视图；跨生命周期保存请转为 `QString`。 |
| 继承 | `QList<QXmlStreamAttribute>` 的遍历、索引、插入、删除 API | 管理属性序列 | 遵守 `QList` 语义；属性顺序会影响写出顺序，容器允许重复项。 |

### 一句话总结

`QXmlStreamAttributes` 是有序的 XML 属性值容器：语义判断优先使用“命名空间 URI + 局部名”，词法保留才使用限定名；空属性值与属性不存在必须分开处理，`QStringView` 也不能脱离底层对象长期保存。
