# QDomAttr
> Qt 6.11.1 · Qt XML · 来自 `QDomAttr`

## 1. 先建立直觉

`QDomAttr` 表示 XML 元素的属性节点，例如 `<item id="42">` 中的 `id="42"`。日常读写属性时通常用 `QDomElement::attribute()` 和 `setAttribute()`，只有需要把属性当节点处理时才直接用 `QDomAttr`。

## 2. 类说明

保留类说明：这些 API 来自 `QDomAttr`，属于 Qt XML 模块，用于表示 DOM 属性节点。

属性节点继承 `QDomNode`，但它不是元素的普通 child。它属于元素的属性集合，通过 `ownerElement()` 找到所属元素。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `name()` | 返回属性名。 |
| `value()` / `setValue()` | 读取或设置属性值。 |
| `ownerElement()` | 返回拥有该属性的元素。 |
| `specified()` | 判断属性是否被显式指定。 |
| `nodeType()` | 返回 `AttributeNode`。 |

## 4. 典型流程

```cpp
QDomAttr attr = doc.createAttribute("id");
attr.setValue("42");
element.setAttributeNode(attr);
```

多数时候更简单：

```cpp
element.setAttribute("id", "42");
```

## 5. 使用场景

| 场景 | 为什么用 attr 节点 |
| --- | --- |
| 需要遍历属性集合 | 从 `QDomNamedNodeMap` 取出并转为 attr。 |
| 移动/替换属性节点 | 使用 `setAttributeNode()`。 |
| 区分属性节点和普通元素子节点 | 通用 DOM 工具里按 nodeType 分派。 |

## 6. 常见坑与经验

属性不是 child node。`element.childNodes()` 不会列出属性；要用 `element.attributes()` 或属性专用 API。

属性值永远是字符串层面的 XML 属性值。需要 int、bool、enum 时要自己转换并校验失败情况。

## 7. 知识点覆盖

- XML 属性节点和元素属性 API。
- owner element、specified、AttributeNode。
- 属性集合与子节点的区别。
