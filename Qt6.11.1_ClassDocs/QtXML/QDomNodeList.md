# QDomNodeList
> Qt 6.11.1 · Qt XML · 来自 `QDomNodeList`

## 1. 先建立直觉

`QDomNodeList` 是一组 DOM 节点的列表视图。常见来源是 `childNodes()`、`elementsByTagName()` 和 `elementsByTagNameNS()`。它让你按索引读取节点和查询数量。

## 2. 类说明

保留类说明：这些 API 来自 `QDomNodeList`，属于 Qt XML 模块，用于表示 DOM 查询或子节点产生的节点列表。

它是值对象式句柄，不拥有独立 XML 数据；列表里的节点仍属于原 DOM 文档。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `count()` / `length()` / `size()` | 返回列表长度。 |
| `at(index)` / `item(index)` | 返回指定位置节点；越界返回空节点。 |
| `isEmpty()` | 判断列表是否为空。 |
| `operator==` / `operator!=` | 比较两个列表句柄。 |

## 4. 典型流程

```cpp
QDomNodeList items = root.elementsByTagName("item");
for (int i = 0; i < items.size(); ++i) {
    QDomElement item = items.at(i).toElement();
    if (!item.isNull())
        handle(item);
}
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 遍历所有匹配元素 | `elementsByTagName()` 返回列表。 |
| 遍历直接子节点 | `childNodes()` 返回列表。 |
| DOM 工具类输出节点集合 | 用列表做只读遍历接口。 |

## 6. 常见坑与经验

`elementsByTagName()` 得到的是所有后代，不只是直接孩子。直接子元素请遍历 `firstChild()`/`nextSibling()`。

`item()` 越界不会抛异常，而是返回空节点。使用前检查 `isNull()`。

## 7. 知识点覆盖

- DOM 节点列表读取。
- 后代查询和直接子节点的区别。
- 空节点和越界处理。
