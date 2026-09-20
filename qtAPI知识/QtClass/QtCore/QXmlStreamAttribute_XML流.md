# Qt QXmlStreamAttribute：保存一个 XML 属性的名字、命名空间和值

`QXmlStreamAttribute` 表示一条 XML 属性，例如：

```xml
<book xml:id="b-7" lang="zh-CN">
```

它保存属性的限定名、局部名、命名空间 URI、前缀和值，并标记该属性是否由 DTD 的 `ATTLIST` 默认值补入。它是 `QXmlStreamReader::attributes()` 返回的列表元素，也是 `QXmlStreamWriter::writeAttribute()` 接受的值类型。

```cpp
const QXmlStreamAttributes attributes = reader.attributes();
for (const QXmlStreamAttribute &attribute : attributes) {
    qDebug() << attribute.namespaceUri()
             << attribute.name()
             << attribute.value();
}
```

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QXmlStreamAttribute>`  
> CMake：`Qt6::Core`  
> 类型：可复制、可比较的 XML 值类型；所有成员函数可重入。

## 它解决什么问题

直接用字符串保存属性名会把三个不同概念混在一起：

- `name`：命名空间无关的局部名；
- `prefix`：文档中出现的前缀，例如 `xml`；
- `namespaceUri`：前缀解析后的命名空间身份。

前缀只在当前 XML 文档上下文中有意义，同一个前缀可以在不同作用域绑定不同 URI，不同前缀也可以绑定相同 URI。因此做 XML 语义判断时，应使用 `namespaceUri()` 与 `name()`，不要用 `qualifiedName()` 作为稳定键。

```cpp
const bool isXmlId =
    attribute.namespaceUri() == u"http://www.w3.org/XML/1998/namespace"_s
    && attribute.name() == u"id"_s;
```

## 构造方式

无参构造产生空属性，通常只是一个临时值，不表示 XML 中存在一条合法属性。普通未命名空间属性可传限定名和值：

```cpp
QXmlStreamAttribute lang(u"lang"_s, u"zh-CN"_s);
```

命名空间属性应分别传 URI、局部名和值：

```cpp
QXmlStreamAttribute id(
    u"http://www.w3.org/XML/1998/namespace"_s,
    u"id"_s,
    u"b-7"_s);
```

带 namespace URI 的构造函数由调用方提供局部名，不会根据某个前缀自动查找 URI。若需要输出限定名和命名空间声明，交给 `QXmlStreamWriter` 的命名空间 API 组织更安全。

## 五个读取 API 的语义

- `namespaceUri()`：返回解析后的命名空间 URI；无命名空间时为空视图。
- `name()`：返回局部名。
- `qualifiedName()`：返回 XML 原文中的限定名，即 `prefix:name` 或无前缀的 `name`。
- `prefix()`：从限定名中取得前缀。
- `value()`：返回属性值。

这些 API 返回 `QStringView`，不是 `QString`。视图不拥有字符数据，不能在属性对象、reader 当前数据或相关字符串存储销毁后继续保存。若要跨越容器/reader 生命周期，复制成 `QString`：

```cpp
const QString stableName = attribute.name().toString();
const QString stableValue = attribute.value().toString();
```

解析器返回的属性对象是当前 token 的值快照；将 `QStringView` 保存到下一次 `readNext()` 之后时，应避免依赖底层缓冲区的生命周期，最稳妥的做法是立即复制。

## `isDefault()` 的边界

`isDefault()` 只有在 XML 解析器根据 DTD 中的 `ATTLIST` 声明补入默认属性时才为 `true`。手工构造的属性通常不是“解析器默认属性”。它不是“属性值等于默认值”的比较器，也不表示属性是否可以被用户覆盖。

如果应用不允许 DTD 或不启用相关解析能力，不要根据该标志推断一定会得到默认属性；业务层还应根据安全策略和 reader 的配置处理外部实体/DTD。

## 比较语义

`QXmlStreamAttribute` 支持 `==` 和 `!=`。比较包括属性值；命名空间属性按 URI 与局部名识别，未解析命名空间的属性按限定名识别。这样不同前缀但同 URI、同局部名和值的属性可以比较为相等。

这也说明 `qualifiedName()` 不应作为通用去重键。若要在应用层判重，先明确输入来自解析器还是手工构造，并统一使用“是否有命名空间 + namespace URI + local name + value”的业务键。

## 与 XML 流读写器协作

读取时，只有在 reader 当前 token 是 `StartElement` 时，`attributes()` 才有当前元素属性的语义。写出时可以把值直接交给 writer：

```cpp
QXmlStreamWriter writer(device);
writer.writeStartElement(u"book"_s);
writer.writeAttribute(QXmlStreamAttribute(
    u"lang"_s, u"zh-CN"_s));
writer.writeEndElement();
```

若使用命名空间 URI 构造属性，写入时应同时正确建立前缀/URI 声明；XML 命名空间的合法序列化由 writer 维护，不能只拼接一个字符串当作完整命名空间处理。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QXmlStreamAttribute()` | 创建空属性 | 各字符串为空；不表示 XML 中已有属性。 |
| `QXmlStreamAttribute(qualifiedName, value)` | 创建无显式命名空间属性 | `qualifiedName` 保存限定名；若手工传 `p:name`，URI 不会自动解析出来。 |
| `QXmlStreamAttribute(namespaceUri, name, value)` | 创建命名空间属性 | 第二个参数是局部名，第一参数是已解析 URI，不是前缀。 |
| `namespaceUri()` | 读取命名空间 URI | 无命名空间时为空 `QStringView`；语义判断优先使用它和 `name()`。 |
| `name()` | 读取局部名 | 返回非拥有的 `QStringView`。 |
| `qualifiedName()` | 读取原始限定名 | 可能包含前缀；前缀不具备跨文档/作用域稳定身份。 |
| `prefix()` | 读取限定名前缀 | 没有前缀时为空；不要用它替代 URI。 |
| `value()` | 读取属性值 | 返回非拥有的 `QStringView`；需要长期保存时复制为 `QString`。 |
| `isDefault()` | 判断是否为 DTD `ATTLIST` 默认属性 | 是解析器来源标志，不是“值等于默认值”的判断。 |
| `operator==` | 比较两个属性 | 比较值以及命名身份；命名空间属性按 URI+局部名，不要按前缀判同。 |
| `operator!=` | 判断两个属性不等 | 与 `operator==` 相反。 |

---

### 一句话总结

`QXmlStreamAttribute` 把 XML 属性的局部名、命名空间 URI、前缀和值分开保存；语义判断用 URI+局部名，`qualifiedName()` 只适合保留原文，而所有 `QStringView` 都要注意非拥有生命周期。
