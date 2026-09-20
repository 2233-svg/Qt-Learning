# Qt QDomAttr 深入笔记：把 XML 属性当作可查询的 DOM 节点

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDomAttr>`  
> 所属模块：`Qt6::Xml`  
> 继承：`QDomNode -> QDomAttr`

`QDomAttr` 表示 element 上的一个 XML 属性节点。

```xml
<link href="https://example.test" color="red"/>
      ^^^^^^^^^^^^^^^^^^^^^^^^^^
      QDomAttr：name 为 href，value 为 URL
```

它解决的是“除了按名字读写属性值之外，还需要知道属性节点本身、它属于哪个 element、是否显式设置过”的情况。普通业务代码通常直接使用 `QDomElement::attribute()`、`setAttribute()` 和 `hasAttribute()`；当需要节点级操作或遍历 `QDomNamedNodeMap` 时才使用 `QDomAttr`。

## 1. 属性不是 element 的 child

`QDomAttr` 虽然继承自 `QDomNode`，但 XML DOM 的属性不在 `QDomElement::childNodes()` 里。属性通过 element 的属性接口访问：

```cpp
QDomElement link = document.createElement("link");
link.setAttribute("href", "https://example.test");

QDomAttr href = link.attributeNode("href");
if (!href.isNull()) {
    qDebug() << href.name() << href.value();
}
```

遍历子元素时用 `firstChild()`、`nextSibling()`；遍历属性时用 `attributes()` 返回的 `QDomNamedNodeMap`。把两者混在一起是 DOM 修改代码里常见的误区。

## 2. 什么时候直接用 `QDomElement`，什么时候用 `QDomAttr`

对“按名字存取字符串”的场景，优先使用 element API：

```cpp
link.setAttribute("color", "red");
const QString color = link.attribute("color");
```

使用 `QDomAttr` 的典型场景：

- 需要 `ownerElement()` 反查属性挂在哪个 element 上。
- 需要 `specified()` 区分“值被显式设置”与“未指定”。
- 需要将属性作为一个 DOM 节点传递、克隆或放入属性节点映射。
- 需要配合 `attributeNode()`、`setAttributeNode()`、`removeAttributeNode()` 进行节点级替换。

## 3. 修改 attr 会直接修改 owner element

```cpp
QDomAttr href = link.attributeNode("href");
href.setValue("https://example.test/docs");

Q_ASSERT(link.attribute("href") == "https://example.test/docs");
```

从 `attributeNode()` 获得的是 element 中实际属性节点的共享句柄，不是值的快照。若想尝试修改但不影响 element，先用 `cloneNode()` 得到独立副本，再在副本上操作。

同样地，拷贝构造和赋值也是浅拷贝：

```cpp
QDomAttr alias = href;
alias.setValue("https://example.test/api");
// href 和 link 都会看到新值
```

## 4. 空值、未指定与 `specified()`

`value()` 在属性未指定时返回空字符串，因此仅检查返回值无法区分：

```text
属性不存在 / 未指定
属性存在但值就是 ""
```

`specified()` 用来判断属性值是否由用户通过 `setValue()` 显式设置。对业务 XML 的“是否存在某属性”判断，通常还是 `QDomElement::hasAttribute()` 语义更直接；`specified()` 更接近 DOM 属性默认值与显式赋值的状态。

`ownerElement()` 在属性尚未附着到 element 时返回空节点。处理独立创建、克隆或已移除的属性节点时，先检查它。

## 5. 属性节点的创建与替换

属性一般用 `QDomElement::setAttribute()` 创建。需要把一个现成 `QDomAttr` 作为节点装到 element 上时，可用：

```cpp
QDomAttr attr = document.createAttribute("role");
attr.setValue("admin");
link.setAttributeNode(attr);
```

节点级 API 适合保留、替换或转移属性节点的场景；常规键值写入不必绕一层 `QDomAttr`。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDomAttr()` | 创建空属性节点句柄 | 真实属性通常通过 `QDomDocument::createAttribute()` 或 element 的属性 API 取得 |
| 构造 | `QDomAttr(const QDomAttr &attr)` | 复制属性节点句柄 | 浅拷贝；修改副本会修改同一个底层属性 |
| 赋值 | `operator=(const QDomAttr &other)` | 让当前句柄引用另一个属性节点 | 不是值复制；需要独立节点时用 `cloneNode()` |
| 属性名 | `name() const` | 返回属性名称 | 用于遍历 `QDomNamedNodeMap` 或节点级代码；普通按名访问通常使用 element API |
| 属性值 | `value() const` | 返回属性字符串值 | 未指定属性返回空字符串，不能单独据此判断属性是否存在 |
| 属性值 | `setValue(const QString &value)` | 设置属性值 | 若 attr 已附着到 element，会直接修改该 element 的属性 |
| 显式状态 | `specified() const` | 判断值是否通过 `setValue()` 被显式设置 | 不等价于所有业务意义上的“属性存在”；需要时结合 `hasAttribute()` |
| 所属元素 | `ownerElement() const` | 返回当前属性附着的 element | 独立、克隆或已移除的属性可能没有 owner，返回空节点 |
| 节点类型 | `nodeType() const` | 返回 `QDomNode::AttributeNode` | 属性是 node 但不是 element 的 child；不要在 `childNodes()` 中查找它 |

---

### 一句话总结

`QDomAttr` 让 XML 属性以节点形式被查询和修改。普通键值读写用 `QDomElement` 更简洁；需要 owner、显式设置状态或属性节点替换时再使用 `QDomAttr`，并牢记它与 element 共享底层数据。
