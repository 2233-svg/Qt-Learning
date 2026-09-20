# QDomNamedNodeMap 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDomNamedNodeMap>`  
> 所属模块：`Qt6::Xml`  
> 继承：无

## 它解决什么问题

`QDomNamedNodeMap` 是 DOM 里“按名字访问节点集合”的对象，最常见来源是 `QDomNode::attributes()` 或 `QDomElement::attributes()`。实际使用中，你可以把它理解为 XML 元素属性集合的通用视图：按属性名取、按命名空间取、枚举全部属性、替换属性节点、移除属性节点。

它不是 `QDomNodeList`，也不是普通的 `QMap`。虽然提供 `item(index)`，但 DOM 不保证 `QDomNamedNodeMap` 的节点顺序；索引访问只是方便枚举，不应作为业务顺序、序列化顺序或稳定 ID 使用。

`QDomNamedNodeMap` 和其它 DOM 句柄一样是轻量值对象。通过它取得或修改的节点通常直接关联到底层 DOM 树，例如修改 `attributes()` 返回的映射，会修改对应元素的属性。

## 常见使用路径

```cpp
#include <QDomDocument>
#include <QDomElement>
#include <QDomNamedNodeMap>

QDomDocument document;
document.setContent(R"(<button text="OK" enabled="true"/>)");

QDomElement button = document.documentElement();
QDomNamedNodeMap attributes = button.attributes();

for (int i = 0; i < attributes.length(); ++i) {
    QDomNode node = attributes.item(i);
    qDebug() << node.nodeName() << node.nodeValue();
}

if (attributes.contains("enabled"))
    attributes.removeNamedItem("enabled");
```

这里的 `attributes` 不是一个快照副本。`removeNamedItem("enabled")` 会把 `button` 元素上的 `enabled` 属性真正移除。

## 普通名字与命名空间名字

`contains()`、`namedItem()`、`setNamedItem()`、`removeNamedItem()` 使用 `QDomNode::nodeName()` 做名字匹配。对带前缀的属性来说，这通常是限定名，例如 `meta:version`。

带 `NS` 的版本使用命名空间 URI 和本地名匹配，例如 URI 为 `urn:meta`、本地名为 `version`。这比前缀可靠，因为同一个命名空间可以使用不同前缀。

```cpp
QDomElement item = document.createElementNS("urn:model", "m:item");
item.setAttributeNS("urn:meta", "meta:version", "2");

QDomNamedNodeMap attrs = item.attributes();
QDomNode version = attrs.namedItemNS("urn:meta", "version");
```

## 用它解决哪些问题

### 枚举未知属性

当 XML schema 不固定，或你要把第三方扩展属性全部读取出来时，`QDomNamedNodeMap` 比逐个 `attribute(name)` 更合适。遍历时只依赖 `length()` 和 `item(i)`，不要假设属性顺序。

### 按节点对象替换属性

若只是写属性值，用 `QDomElement::setAttribute()` 更直接。若你已经持有一个 `QDomAttr` 节点，或者要保留其命名空间信息，再使用 `setNamedItem()` 或 `setNamedItemNS()`。

### 删除属性并保留被删节点

`removeNamedItem()` 会返回被移除的节点，这点比 `QDomElement::removeAttribute()` 更适合做撤销、迁移日志或转移属性的逻辑。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDomNamedNodeMap()` | 创建空的命名节点映射。 | 空映射通常只作占位；实际属性集合多来自 `attributes()`。 |
| 构造 | `QDomNamedNodeMap(const QDomNamedNodeMap &namedNodeMap)` | 复制映射句柄。 | 复制后仍关联同一底层集合，修改会影响原 DOM。 |
| 析构 | `~QDomNamedNodeMap()` | 销毁映射句柄。 | 不表示删除元素属性或 DOM 节点。 |
| 查询 | `contains(const QString &name) const` | 判断映射中是否有指定 `nodeName()` 的节点。 | 不考虑命名空间 URI；命名空间场景用 `namedItemNS()` 判断是否为空。 |
| 计数 | `count() const` | 返回节点数量。 | 等价于 `length()`，为 Qt API 一致性提供。 |
| 状态 | `isEmpty() const` | 判断集合是否为空。 | 等价于检查 `length() == 0`。 |
| 索引访问 | `item(int index) const` | 返回指定索引位置的节点。 | 索引只用于枚举，顺序不稳定；越界时返回空节点。 |
| 计数 | `length() const` | 返回映射中的节点数量。 | DOM 风格命名；需要 Qt 风格可用 `size()` 或 `count()`。 |
| 按名访问 | `namedItem(const QString &name) const` | 用 `nodeName()` 查找节点。 | 找不到返回空节点；对命名空间前缀敏感。 |
| 按命名空间访问 | `namedItemNS(const QString &nsURI, const QString &localName) const` | 用命名空间 URI 和本地名查找节点。 | 推荐用于带命名空间属性，不要把前缀当作身份。 |
| 按名删除 | `removeNamedItem(const QString &name)` | 删除指定名称的节点并返回被删除节点。 | 找不到返回空节点；用于属性集合时会真实删除元素属性。 |
| 按命名空间删除 | `removeNamedItemNS(const QString &nsURI, const QString &localName)` | 删除指定 URI 和本地名的节点。 | 找不到返回空节点；适合删除带命名空间属性。 |
| 按名插入 | `setNamedItem(const QDomNode &newNode)` | 把节点加入映射，按 `nodeName()` 替换同名旧节点。 | 替换成功时返回旧节点；通常用于属性节点。 |
| 按命名空间插入 | `setNamedItemNS(const QDomNode &newNode)` | 按 URI 和本地名插入或替换节点。 | 替换规则与 `setNamedItem()` 不同，适合命名空间属性。 |
| 计数 | `size() const` | 返回节点数量。 | 等价于 `length()`。 |
| 比较 | `operator!=(const QDomNamedNodeMap &other) const` | 判断两个映射是否不相等。 | 比较的是映射对象语义，不要用来推断属性顺序。 |
| 赋值 | `operator=(const QDomNamedNodeMap &other)` | 让当前映射句柄指向另一个映射。 | 浅赋值，仍共享底层 DOM 数据。 |
| 比较 | `operator==(const QDomNamedNodeMap &other) const` | 判断两个映射是否相等。 | 不等于逐项按业务规则比较属性内容。 |

## 易错点

1. `item(0)` 不代表“第一个写在 XML 里的属性”。DOM 不保证命名节点映射的顺序。
2. `contains("meta:version")` 是按 `nodeName()` 判断，前缀变化会影响结果；命名空间属性要用 `namedItemNS(uri, "version")`。
3. 从元素拿到的 `attributes()` 不是只读快照；通过映射删除或替换节点会改到元素本身。
4. 只想读写普通属性值时，`QDomElement::attribute()` 和 `setAttribute()` 更简单；`QDomNamedNodeMap` 适合枚举和节点级替换。

### 一句话总结

`QDomNamedNodeMap` 是 DOM 的“按名字访问节点集合”，常用于元素属性；它能枚举、查找、替换和移除节点，但不保证顺序，命名空间场景要优先使用 `NS` 版本。
