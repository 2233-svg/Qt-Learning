# Qt QDomDocumentType 深入笔记：读取 XML 的 DOCTYPE 与 DTD 索引

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDomDocumentType>`  
> 所属模块：`Qt6::Xml`  
> 继承：`QDomNode -> QDomDocumentType`  
> 节点性质：对 DTD 数据提供只读访问。

`QDomDocumentType` 对应 XML 的 `<!DOCTYPE ...>` 声明。它是 Qt DOM 中读取 DTD 元数据的入口：文档类型名、内部子集、外部子集标识，以及 DTD 声明的 entity 和 notation 映射都从这里获得。

```xml
<!DOCTYPE catalog
  PUBLIC "-//Example//Catalog 1.0//EN" "catalog.dtd"
  [
    <!ENTITY publisher "Example Press">
  ]>
```

上面的五类信息分别对应：

- `name()`：`catalog`
- `publicId()`：外部 DTD 的 public identifier
- `systemId()`：外部 DTD 的 system identifier
- `internalSubset()`：方括号中的内部 DTD 子集
- `entities()` / `notations()`：已声明实体和 NOTATION 的映射

它解决的是“解析后怎样审查 DTD 声明内容”，不是“在现有文档里随意新增、删除或改写 DTD 定义”。

## 1. 从 `QDomDocument` 获取 document type

```cpp
QDomDocumentType doctype = document.doctype();
if (doctype.isNull()) {
    return; // 文档没有 DOCTYPE
}

qDebug() << doctype.name();
qDebug() << doctype.publicId();
qDebug() << doctype.systemId();
qDebug().noquote() << doctype.internalSubset();
```

`doctype()` 返回的是一个 DOM 句柄。没有 DOCTYPE 时应先判断 `isNull()`，不要把空字符串的 `name()` 或 `systemId()` 当成“格式有但值为空”的可靠证据。

## 2. internal subset 与 external subset

DTD 声明可能分两部分：

- **internal subset**：直接写在 XML 文档 DOCTYPE 方括号内的声明，`internalSubset()` 返回其文本；没有时返回空字符串。
- **external subset**：由 public ID / system ID 标识的外部 DTD，`publicId()` 或 `systemId()` 未给出时分别返回空字符串。

这些 getter 返回的是声明中记录的字符串，不等同于 Qt 已经打开、下载、验证或信任对应的外部资源。遇到来自不可信 XML 的 system ID，应用不应据此自行无条件读取文件或网络资源。

## 3. 从映射读取 entities 和 notations

```cpp
QDomNamedNodeMap entities = doctype.entities();
QDomEntity logo = entities.namedItem("logo").toEntity();

QDomNamedNodeMap notations = doctype.notations();
QDomNotation jpeg = notations.namedItem("jpeg").toNotation();
```

`entities()` 给出 DTD 中全部 `QDomEntity`，`notations()` 给出全部 `QDomNotation`。它们是索引入口：

- 要知道未解析实体声明的外部数据格式，读取 `QDomEntity::notationName()`。
- 要获得某个 NOTATION 的外部标识，读取 `QDomNotation::publicId()` 和 `systemId()`。
- 映射里没有指定名称时，转换得到空节点，必须检查。

`QDomDocumentType` 提供的是**只读访问**；不要把返回的 `QDomNamedNodeMap` 当作修改 DTD 的业务接口。

## 4. 它与 `QDomDocument`、`QDomEntity` 的关系

```text
QDomDocument
  └─ doctype() -> QDomDocumentType
                     ├─ entities()  -> QDomEntity
                     └─ notations() -> QDomNotation
```

`QDomDocument` 是整棵 XML 树和节点工厂；`QDomDocumentType` 只负责暴露其中 DTD 声明信息。实体在内容树中的一次使用则是 `QDomEntityReference`，不是 `QDomDocumentType` 的直接 child 编辑对象。

## 5. 复制与生命周期

复制构造和赋值都是浅拷贝，多个 `QDomDocumentType` 句柄共享同一内部 DOM 节点。一般直接将 `QDomDocumentType` 当作从 `QDomDocument` 取出的临时查询句柄即可；若需要长期保存审计信息，复制 `name()`、标识符和 subset 文本到自己的数据结构更直观。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDomDocumentType()` | 创建空 document type 节点句柄 | 常规读取从 `QDomDocument::doctype()` 开始；先检查是否为 null |
| 构造 | `QDomDocumentType(const QDomDocumentType &documentType)` | 复制 document type 句柄 | 浅拷贝；不会复制出独立的 DTD 数据 |
| 赋值 | `operator=(const QDomDocumentType &other)` | 让当前句柄引用另一个 document type | 只改变句柄指向，不编辑原始 DTD |
| 类型名 | `name() const` | 返回 `<!DOCTYPE name>` 中的文档类型名称 | 空节点或没有名称时不要把空字符串误判为有效声明 |
| 内部子集 | `internalSubset() const` | 返回 DOCTYPE 方括号内的内部 DTD 子集文本 | 没有内部子集时返回空字符串；这是文本记录，不是可编辑模型 |
| 外部公有标识 | `publicId() const` | 返回外部 DTD subset 的 public identifier | 未指定时为空；它是声明信息，不代表资源已经校验 |
| 外部系统标识 | `systemId() const` | 返回外部 DTD subset 的 system identifier | 不要把来自不可信文档的值直接当作可信路径或 URL |
| 实体映射 | `entities() const` | 返回 DTD 中全部实体的 `QDomNamedNodeMap` | 通过 `namedItem()` 查找后用 `toEntity()`；映射用于读取，不作为 DTD 修改器 |
| NOTATION 映射 | `notations() const` | 返回 DTD 中全部 notation 的 `QDomNamedNodeMap` | 通过 `toNotation()` 转换；找不到名称时得到空节点 |
| 节点类型 | `nodeType() const` | 返回 `QDomNode::DocumentTypeNode` | 在通用节点遍历中可与 `isDocumentType()` 配合识别 |

---

### 一句话总结

`QDomDocumentType` 是读取 DOCTYPE 和 DTD 声明的只读入口。先从 `QDomDocument::doctype()` 判断文档是否带 DTD，再通过实体与 notation 映射查看元数据；它不负责编辑 DTD，也不自动信任外部 system ID 指向的资源。
