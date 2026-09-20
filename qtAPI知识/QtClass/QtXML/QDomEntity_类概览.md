# Qt QDomEntity 深入笔记：读取 DTD 中的实体元数据

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDomEntity>`  
> 所属模块：`Qt6::Xml`  
> 继承：`QDomNode -> QDomEntity`  
> 节点性质：只读、没有 parent。

`QDomEntity` 表示 XML/DTD 中的实体本身，可以是已解析实体，也可以是未解析实体。它描述的是实体的 DOM 模型与外部标识信息，不是 XML 内容树中某次 `&name;` 的使用位置。

```text
DTD 中的实体定义  --> QDomEntity
XML 内容中的 &logo; --> QDomEntityReference
```

这一区别很重要：`QDomEntity` 用来审查实体声明、系统标识和 NOTATION 关联；若要处理文档树里某个实体引用，应查看 `QDomEntityReference`。

## 1. 它解决什么问题

在解析含 DTD 的旧式 XML 格式时，应用有时需要了解实体来自哪里、是否是未解析实体、是否声明了 public/system identifier，以及是否依赖某种 NOTATION 格式。`QDomEntity` 就是用来读取这些声明级元数据的节点。

典型 DTD 概念如下：

```xml
<!NOTATION jpeg SYSTEM "image/jpeg">
<!ENTITY logo SYSTEM "logo.jpg" NDATA jpeg>
```

这里 `logo` 对应一个未解析实体，`QDomEntity::notationName()` 会得到 `jpeg`；`systemId()` 可给出其系统标识。它不是在业务 DOM 树中挂一个 `<logo>` 元素。

## 2. 从 document type 中读取实体

实体节点通常由解析出的 `QDomDocumentType` 提供：

```cpp
QDomDocumentType doctype = document.doctype();
QDomNamedNodeMap entities = doctype.entities();

QDomEntity entity = entities.namedItem("logo").toEntity();
if (!entity.isNull()) {
    qDebug() << entity.systemId()
             << entity.publicId()
             << entity.notationName();
}
```

查找失败时 `toEntity()` 得到空节点，因此先调用 `isNull()`。不要用默认构造的 `QDomEntity` 伪造一个实体声明；该类的价值在于读取已存在的 DTD 信息。

## 3. 已解析实体与未解析实体

`notationName()` 是区分点：

- 对**未解析实体**，返回该实体关联的 NOTATION 名称。
- 对**已解析实体**，返回空字符串。

`publicId()` 与 `systemId()` 是实体外部标识。缺失某项时，对应 getter 返回空字符串；空字符串意味着“未指定”，不等于外部资源一定不可用或实体一定无效。

## 4. 它是只读的，不能直接“修改实体”

DOM 不支持编辑 entity node，实体的所有后代也都是只读的；`QDomEntity` 本身没有 parent。

如果业务目标是修改某个实体展开后的内容，不能对 `QDomEntity` 直接做树编辑。Qt 文档给出的方向是：找到每个相关 `QDomEntityReference`，以实体内容的 clone 替换它们，再分别修改这些独立克隆。

这通常意味着你在做的是 XML 结构转换，而不是简单调用一个 setter。对于现代业务 XML，也应重新评估是否真的需要 DTD 实体机制；普通元素、属性或外部资源映射往往更易维护。

## 5. 复制只是共享只读节点句柄

复制构造和赋值都是浅拷贝，多个 `QDomEntity` 句柄引用同一个内部节点。即使使用 `cloneNode()` 获得深复制，也不意味着原始 DTD 声明就变成可随意编辑的业务对象。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDomEntity()` | 创建空实体节点句柄 | 不能用它构造有效 DTD 实体；从 `QDomDocumentType::entities()` 获取真实节点 |
| 构造 | `QDomEntity(const QDomEntity &entity)` | 复制实体节点句柄 | 浅拷贝；复制后仍引用同一个只读实体 |
| 赋值 | `operator=(const QDomEntity &other)` | 让当前句柄引用另一个实体 | 不会复制或修改实体声明 |
| 节点类型 | `nodeType() const` | 返回 `QDomNode::EntityNode` | 遍历 DTD 节点时用于与 `EntityReferenceNode` 区分 |
| NOTATION | `notationName() const` | 返回未解析实体关联的 NOTATION 名称 | 已解析实体返回空字符串；它不是实体内容或文件名 |
| 公共标识 | `publicId() const` | 返回实体声明的 public identifier | 未指定时返回空字符串；这是描述元数据，不是已打开资源的句柄 |
| 系统标识 | `systemId() const` | 返回实体声明的 system identifier | 未指定时返回空字符串；不要把它直接当作可信的本地路径或 URL 使用 |

---

### 一句话总结

`QDomEntity` 是 DTD 实体的只读描述节点，用于读取 public ID、system ID 和未解析实体的 NOTATION 关联。它不代表文档树中的某次实体引用，也不能作为普通可编辑 XML 节点使用。
