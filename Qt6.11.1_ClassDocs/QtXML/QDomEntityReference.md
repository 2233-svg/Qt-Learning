# QDomEntityReference
> Qt 6.11.1 · Qt XML · 来自 `QDomEntityReference`

## 1. 先建立直觉

`QDomEntityReference` 表示 XML 内容中出现的实体引用节点，例如未被展开的 `&foo;`。它是“引用这个实体”的位置，而 `QDomEntity` 是 DTD 里的实体声明。

## 2. 类说明

保留类说明：这些 API 来自 `QDomEntityReference`，属于 Qt XML 模块，用于表示 DOM 树中的实体引用节点。

创建实体引用应使用 `QDomDocument::createEntityReference()`。解析时实体是否展开或保留为引用，取决于实体种类和解析规则。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QDomEntityReference()` | 创建空引用句柄。 |
| `nodeType()` | 返回 `EntityReferenceNode`。 |
| 继承的 `nodeName()` | 通常是实体引用名称。 |

## 4. 典型流程

```cpp
QDomEntityReference ref = doc.createEntityReference("company");
element.appendChild(ref);
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 保留未展开实体引用 | 用引用节点表达 `&name;`。 |
| XML 转换工具 | 识别并处理 entity reference node。 |
| 兼容旧 DTD 文档 | 不强行替换所有实体。 |

## 6. 常见坑与经验

不要把实体引用当普通文本节点。遍历时要检查 `nodeType()`，否则可能漏掉未展开的引用内容。

实体引用是否能被下游系统识别，取决于输出文档是否保留或提供对应 DTD 实体声明。

## 7. 知识点覆盖

- 实体引用节点。
- 与实体声明 `QDomEntity` 的区别。
- DTD 依赖和输出兼容性。
