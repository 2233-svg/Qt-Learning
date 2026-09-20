# Qt QDomEntityReference 深入笔记：DOM 树中保留下来的实体引用

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDomEntityReference>`  
> 所属模块：`Qt6::Xml`  
> 继承：`QDomNode -> QDomEntityReference`  
> 节点性质：后代只读；解析器不保证一定保留此类节点。

`QDomEntityReference` 表示 XML 内容树中的一次实体引用，例如源 XML 里的 `&companyLogo;`。它和 `QDomEntity` 的关系类似“使用处”和“声明信息”：

```text
DTD 中定义实体         QDomEntity
XML 中某次 &name; 使用  QDomEntityReference
```

它解决的是“DOM 需要保留某次实体引用的结构信息”这一类兼容需求。多数现代 XML 处理并不应依赖它，因为解析器可能已把引用展开成普通字符或普通子树。

## 1. 先理解：不一定会在树里看到它

Qt 文档明确指出：

- 字符引用和预定义实体会被 XML 处理器展开为对应的 Unicode 字符，不保留为实体引用节点。
- XML 处理器也可能在构建 DOM 时直接展开其他实体引用。

因此，下面的 XML：

```xml
<message>Tom &amp; Jerry</message>
```

通常不会在 DOM 中出现 `QDomEntityReference` 来代表 `&amp;`，而是得到包含 `&` 字符的 `QDomText`。

这意味着业务代码不应把“存在一个 `EntityReferenceNode`”当作语义判断条件。若业务只关心最终文本，读取 `QDomElement::text()` 或对应字符节点；只有要兼容保留引用结构的 XML/DTD 流程时，才专门处理该节点。

## 2. 创建和插入

如果你确实需要在 DOM 中放入一个实体引用，可通过 document 创建：

```cpp
QDomEntityReference reference =
    document.createEntityReference("companyLogo");
parent.appendChild(reference);
```

不要使用默认构造去伪造一个有效引用。实体名必须符合 XML 名称规则；无效名称的处理受 `QDomImplementation::InvalidDataPolicy` 影响。

读取引用名称时，可使用继承的 `nodeName()`。对实体引用节点，它表示被引用的实体名称。

## 3. 引用内容与只读边界

若文档中存在对应的 `QDomEntity`，entity reference 的 child list 与该 entity 的 child list 相同；这些后代和实体后代一样都是只读的。

所以“通过 `firstChild()` 找到 entity reference 的内容后直接编辑”不是可靠的方式。需要修改展开内容时，应把实体引用节点替换成可编辑的节点副本，再修改副本。这个操作是在重写文档结构，不是更新实体声明。

## 4. 与 `QDomEntity` 的区分

- `QDomEntity`：DTD 声明侧的实体元数据，可读取 public ID、system ID 和 NOTATION 名称。
- `QDomEntityReference`：内容树侧的某次引用，可以通过 `nodeName()` 得到引用名。

## 5. 浅拷贝与遍历策略

复制构造和赋值都是浅拷贝，多个句柄会指向同一个内部引用节点。遍历时先判断 `nodeType() == QDomNode::EntityReferenceNode`，再调用 `toEntityReference()`；转换失败得到的是空节点。

但最重要的策略仍是：即便原 XML 写了实体引用，也同时准备好“解析后没有该节点”的路径。解析器展开与否并不是应用可以依赖的稳定业务协议。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDomEntityReference()` | 创建空实体引用节点句柄 | 有效引用应由 `QDomDocument::createEntityReference()` 创建 |
| 构造 | `QDomEntityReference(const QDomEntityReference &entityReference)` | 复制实体引用节点句柄 | 浅拷贝；多个句柄指向同一内部节点 |
| 赋值 | `operator=(const QDomEntityReference &other)` | 让当前句柄引用另一个实体引用节点 | 不会复制实体内容，也不能借此绕过只读后代 |
| 节点类型 | `nodeType() const` | 返回 `QDomNode::EntityReferenceNode` | 解析器可能已展开实体，因此不能假定遍历时一定会遇到此类型 |
| 继承：名称 | `nodeName() const` | 返回被引用实体的名称 | 仅在确实得到实体引用节点时使用；不能用它判断预定义实体是否出现在源 XML |
| 继承：子节点 | `childNodes() const` | 读取引用关联的子节点列表 | 后代是只读的；若要修改内容，应替换引用节点为可编辑副本 |
| 继承：转换 | `toEntityReference() const` | 将通用 `QDomNode` 转为实体引用句柄 | 先检查 `nodeType()` 或 `isEntityReference()`；类型不匹配时返回空节点 |

---

### 一句话总结

`QDomEntityReference` 是 DOM 中可能保留的一次实体使用位置，不是实体声明本身。预定义实体和许多普通实体常在解析时已经展开，所以它是兼容 DTD 的专门节点，不能作为常规 XML 文本处理的必经分支。
