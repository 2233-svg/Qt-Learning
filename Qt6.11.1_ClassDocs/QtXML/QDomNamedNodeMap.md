# QDomNamedNodeMap
> Qt 6.11.1 · Qt XML · 来自 `QDomNamedNodeMap`

## 1. 先建立直觉

`QDomNamedNodeMap` 是按名称访问节点的集合，最常见用途是元素属性集合：`element.attributes()` 返回的就是它。和 `QDomNodeList` 的按位置列表不同，它强调按名称查找、设置和删除。

## 2. 类说明

保留类说明：这些 API 来自 `QDomNamedNodeMap`，属于 Qt XML 模块，用于表示按名称索引的 DOM 节点集合。

它不是通用 `QMap`。顺序不应作为业务语义依赖；XML 属性本身也不应依赖排列顺序。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `count()` / `length()` / `size()` | 集合大小。 |
| `isEmpty()` | 是否为空。 |
| `item(index)` | 按位置取节点，主要用于遍历。 |
| `namedItem(name)` | 按名称取节点。 |
| `setNamedItem(node)` | 插入或替换同名节点。 |
| `removeNamedItem(name)` | 按名称删除节点。 |
| `contains(name)` | 判断是否有指定名称节点。 |
| `namedItemNS(nsURI, localName)` | 按命名空间和本地名查找。 |
| `setNamedItemNS(node)` | 设置命名空间节点。 |
| `removeNamedItemNS(nsURI, localName)` | 删除命名空间节点。 |

## 4. 典型流程

```cpp
QDomNamedNodeMap attrs = element.attributes();
for (int i = 0; i < attrs.size(); ++i) {
    QDomAttr attr = attrs.item(i).toAttr();
    qDebug() << attr.name() << attr.value();
}
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 遍历全部属性 | `attributes()` + `item(i)`。 |
| 保留未知属性 | 读写 XML 时复制属性集合。 |
| 命名空间属性处理 | 使用 NS 版本查找，避免前缀变化影响。 |

## 6. 常见坑与经验

不要依赖属性顺序。序列化时属性顺序可能变化，XML 语义也不要求顺序有意义。

`namedItem()` 返回的是通用 `QDomNode`，通常还要 `toAttr()` 并检查是否为空。

## 7. 知识点覆盖

- 命名节点集合和属性集合。
- 按名称/命名空间查找。
- 属性遍历、替换和删除。
