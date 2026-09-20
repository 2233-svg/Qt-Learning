# QDomElement 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDomElement>`  
> 所属模块：`Qt6::Xml`  
> 继承：`QDomNode`

## 它解决什么问题

`QDomElement` 表示 XML 树中的一个元素节点，也就是形如 `<book id="42">...</book>` 的那一层结构。它负责的不是解析整个 XML 文本，而是让你在已经拥有 DOM 树后，读取和修改元素的：

- 标签名，例如 `book`、`ui:widget`；
- 属性，例如 `id="42"`、`enabled="true"`；
- 带命名空间的属性；
- 后代元素与元素文本。

它适合编辑规模不大、需要随机访问和原地修改的 XML：应用配置、项目文件、导入后需要补字段的 XML、简单的元数据格式等。若文件很大或只需顺序读取，`QXmlStreamReader` 的流式方式通常更省内存。

`QDomElement` 是一个轻量的值对象，但它的副本仍指向同一棵 DOM 数据树。复制元素后修改其中一个副本，另一个副本观察到的内容也会变化；要取得独立的子树，使用继承自 `QDomNode` 的 `cloneNode(true)`。

## 创建、解析与修改

不要把默认构造的 `QDomElement` 当成可写元素。它是空节点；一般由 `QDomDocument::createElement()`、`createElementNS()` 创建，或从解析后的文档中取得根元素、子元素。

```cpp
#include <QDomDocument>
#include <QDomElement>

const QString xml = R"(
    <profile name="Ada">
        <setting key="theme">dark</setting>
    </profile>
)";

QDomDocument document;
const auto result = document.setContent(xml);
if (!result) {
    qWarning() << result.errorMessage << result.errorLine << result.errorColumn;
    return;
}

QDomElement profile = document.documentElement();
const QString name = profile.attribute("name", "anonymous");

profile.setAttribute("lastSaved", "true");
QDomElement setting = profile.firstChildElement("setting");
setting.setAttribute("key", "colorScheme");

qDebug() << document.toString(2);
```

这段代码的关键在于：`document` 是整棵树的所有者和创建工厂，`profile`、`setting` 是树中节点的可复制访问句柄。节点句柄可以跨函数传递，但不能在对应 DOM 文档已经被销毁后继续使用。

## 命名空间：不要只看前缀

XML 命名空间的身份由 URI 和本地名决定，不是由 `x:`、`svg:` 这类前缀决定。读取已有带命名空间 XML 时，应在 `QDomDocument::setContent()` 中启用 `QDomDocument::ParseOption::UseNamespaceProcessing`；否则 `namespaceURI()`、`localName()` 以及本类的 `...NS()` 查询可能得不到预期结果。

```cpp
QDomElement image = document.createElementNS(
    "urn:example:media", "m:image");
image.setAttributeNS(
    "urn:example:meta", "meta:rating", 5);

const QString rating = image.attributeNS(
    "urn:example:meta", "rating", "0");
```

`setAttributeNS()` 用 URI 加限定名写入属性；若已有相同 URI 和本地名的属性，它会更新该属性的值，并使用新限定名中的前缀。后续查询应使用 `attributeNS(uri, localName)`，而不是拿显示前缀当作身份。

## 常见使用场景

### 读取可选配置

`attribute(name, defaultValue)` 很适合兼容旧配置：属性缺失时直接得到默认值。若“缺失”和“空字符串”要区别对待，先用 `hasAttribute()` 判断，再读取 `attribute()`。

### 批量寻找后代节点

`elementsByTagName()` 会在当前元素的整棵后代子树中按前序遍历搜索，不只查直接子节点。若只想读取第一个直接子元素，应使用 `firstChildElement()`；若要逐个遍历直接兄弟元素，使用 `nextSiblingElement()`。

### 需要保留属性节点本身

通常读写属性使用字符串接口就够了。只有要访问属性的命名空间、位置或将属性替换为另一个 `QDomAttr` 时，才使用 `attributeNode()`、`setAttributeNode()` 这组 API。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDomElement()` | 构造空元素节点。 | 空节点不能代表一个实际标签；用 `QDomDocument::createElement()` 或解析结果取得有效元素。 |
| 构造 | `QDomElement(const QDomElement &element)` | 复制元素访问句柄。 | 是共享底层 DOM 数据的浅复制，修改任一副本会改到同一元素。 |
| 赋值 | `operator=(const QDomElement &other)` | 让当前句柄指向另一个元素。 | 同样不复制子树；想分离数据请对节点调用 `cloneNode(true)`。 |
| 属性读取 | `attribute(const QString &name, const QString &defValue = {})` | 按属性名取得字符串值；属性不存在时返回默认值。 | 无法仅靠返回值区分“属性不存在”和“属性值为空”；有此需求时配合 `hasAttribute()`。 |
| 命名空间属性读取 | `attributeNS(const QString &nsURI, const QString &localName, const QString &defValue = {})` | 用命名空间 URI 与本地名读取属性。 | 不按前缀匹配；解析已有 XML 时要启用命名空间处理。 |
| 属性节点读取 | `attributeNode(const QString &name)` | 按名称取得对应的 `QDomAttr`。 | 找不到时返回空 `QDomAttr`，先检查 `isNull()`。 |
| 命名空间属性节点读取 | `attributeNodeNS(const QString &nsURI, const QString &localName)` | 用 URI 和本地名取得属性节点。 | 与 `attributeNS()` 相同，URI 才是命名空间身份。 |
| 属性集合 | `attributes()` | 返回该元素全部属性组成的 `QDomNamedNodeMap`。 | 这是属性映射，不要把 `item(index)` 的顺序当作业务顺序。 |
| 后代查询 | `elementsByTagName(const QString &tagName)` | 返回标签名匹配的全部后代元素列表。 | 搜索范围是整棵后代子树，结果按前序遍历排列，不包含当前元素本身。 |
| 命名空间后代查询 | `elementsByTagNameNS(const QString &nsURI, const QString &localName)` | 返回 URI 与本地名匹配的全部后代元素。 | 含命名空间 XML 不应改用前缀字符串匹配。 |
| 属性判断 | `hasAttribute(const QString &name)` | 判断是否存在指定名称的属性。 | 用于区分缺失属性与值为空的属性。 |
| 命名空间属性判断 | `hasAttributeNS(const QString &nsURI, const QString &localName)` | 判断是否存在指定命名空间属性。 | 与 `attributeNS()` 使用相同的 URI 和本地名。 |
| 类型识别 | `nodeType() const` | 返回 `QDomNode::ElementNode`。 | 在通用 `QDomNode` 遍历中，通常先用 `isElement()` 再调用 `toElement()`。 |
| 删除属性 | `removeAttribute(const QString &name)` | 删除指定名称的属性。 | 属性不存在时没有可处理的返回值；若需记录是否实际删除，请先判断 `hasAttribute()`。 |
| 删除命名空间属性 | `removeAttributeNS(const QString &nsURI, const QString &localName)` | 删除 URI 与本地名匹配的属性。 | 不能用前缀代替 URI。 |
| 移除属性节点 | `removeAttributeNode(const QDomAttr &oldAttr)` | 从元素移除指定属性节点，并返回被移除的属性。 | 参数必须是当前元素的属性；失败时返回空属性。 |
| 设置字符串属性 | `setAttribute(const QString &name, const QString &value)` | 新增属性，或覆盖同名属性的值。 | 会直接改写 DOM；输入必须是可表示为 XML 属性的业务数据。 |
| 设置双精度属性 | `setAttribute(const QString &name, double value)` | 将 `double` 转成文本后写为属性。 | 使用 `QLocale::C` 格式化；XML 中保存的是文本，不含数值范围校验。 |
| 设置单精度属性 | `setAttribute(const QString &name, float value)` | 将 `float` 转成文本后写为属性。 | 使用 `QLocale::C` 格式化，适合跨区域设置保存数值。 |
| 设置整型属性 | `setAttribute(const QString &name, int value)` | 将 `int` 转成文本后写为属性。 | XML 属性没有整数类型，读取时仍要自行转换并校验。 |
| 设置长整型属性 | `setAttribute(const QString &name, qlonglong value)` | 将有符号 64 位整数写为属性文本。 | 注意读取端的类型范围。 |
| 设置无符号长整型属性 | `setAttribute(const QString &name, qulonglong value)` | 将无符号 64 位整数写为属性文本。 | 不要让只支持有符号数的消费者读取该字段。 |
| 设置无符号整型属性 | `setAttribute(const QString &name, uint value)` | 将 `uint` 转成属性文本。 | 本质上转发到无符号 64 位重载。 |
| 设置命名空间字符串属性 | `setAttributeNS(const QString &nsURI, const QString &qName, const QString &value)` | 用 URI、限定名和值新增或替换属性。 | 替换键是 URI 加本地名；`qName` 只决定标签显示名和前缀。 |
| 设置命名空间双精度属性 | `setAttributeNS(const QString &nsURI, const QString &qName, double value)` | 将 `double` 写为带命名空间的属性。 | 保存后仍是 XML 文本；保持读写双方使用同一命名空间 URI。 |
| 设置命名空间整型属性 | `setAttributeNS(const QString &nsURI, const QString &qName, int value)` | 将 `int` 写为带命名空间的属性。 | 本质没有 XML 整数类型，读取端需转换。 |
| 设置命名空间长整型属性 | `setAttributeNS(const QString &nsURI, const QString &qName, qlonglong value)` | 将有符号 64 位数值写为命名空间属性。 | 留意读端类型范围。 |
| 设置命名空间无符号长整型属性 | `setAttributeNS(const QString &nsURI, const QString &qName, qulonglong value)` | 将无符号 64 位数值写为命名空间属性。 | 与非命名空间版本一样，XML 保存的是文本。 |
| 设置命名空间无符号整型属性 | `setAttributeNS(const QString &nsURI, const QString &qName, uint value)` | 将 `uint` 写为命名空间属性。 | 本质上转发到无符号 64 位重载。 |
| 安装属性节点 | `setAttributeNode(const QDomAttr &newAttr)` | 将属性节点加入元素；同名属性存在时替换并返回旧属性。 | 无旧属性时返回空属性；需要整个 `QDomAttr` 对象而不是单纯字符串时使用。 |
| 安装命名空间属性节点 | `setAttributeNodeNS(const QDomAttr &newAttr)` | 将属性节点加入元素，按 URI 与本地名替换冲突项。 | 替换规则不同于 `setAttributeNode()`，适用于带命名空间的属性。 |
| 修改标签名 | `setTagName(const QString &name)` | 将当前元素重命名。 | 这是 Qt 扩展；只改标签名，不会自动改子元素、属性名或相关业务引用。 |
| 标签名 | `tagName() const` | 返回元素的限定标签名。 | 对命名空间元素，前缀可能随创建或修改而变；要比较身份时使用 `namespaceURI()` 与 `localName()`。 |
| 文本内容 | `text() const` | 返回元素的文本内容；没有文本时返回空字符串。 | 它不是 XML 序列化结果；不能用它保留嵌套元素的标签结构。 |

## 易错点

1. `elementsByTagName("item")` 不是“拿直接孩子”的 API。它会递归扫描后代；层级明确的配置读取更适合 `firstChildElement()` 加兄弟遍历。
2. 属性值始终是文本。`setAttribute("timeout", 30)` 很方便，但读取时要处理转换失败、缺失值和范围问题。
3. 命名空间前缀可以变化，URI 不应变化。不要把 `meta:version` 中的 `meta` 写死为业务判断条件。
4. `text()` 只适合取文本，不适合复制 XML 片段；需要保留元素结构时操作 `QDomNode` 或序列化相应节点。

### 一句话总结

`QDomElement` 是 DOM 中“一个 XML 标签及其属性”的操作入口：用普通属性 API 处理简单配置，用 `...NS()` API 处理命名空间，并始终分清直接子元素搜索与整棵后代子树搜索。
