# QDomDocumentFragment
> Qt 6.11.1 · Qt XML · 来自 `QDomDocumentFragment`

## 1. 先建立直觉

`QDomDocumentFragment` 是临时节点片段，可以装一组节点，然后一次性插入到文档树。它本身不是最终 XML 里的一个标签，更像“节点搬运盒”。

## 2. 类说明

保留类说明：这些 API 来自 `QDomDocumentFragment`，属于 Qt XML 模块，用于临时承载一组 DOM 子节点。

片段继承 `QDomNode`，但 `nodeType()` 是 `DocumentFragmentNode`。创建片段应使用 `QDomDocument::createDocumentFragment()`。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QDomDocumentFragment()` | 创建空片段句柄。 |
| `nodeType()` | 返回 `DocumentFragmentNode`。 |
| 继承的 `appendChild()` | 往片段中加入多个节点。 |
| 继承的树插入 API | 将片段插入目标位置。 |

## 4. 典型流程

```cpp
QDomDocumentFragment fragment = doc.createDocumentFragment();
fragment.appendChild(doc.createElement("a"));
fragment.appendChild(doc.createElement("b"));
root.appendChild(fragment);
```

插入后，片段里的孩子进入目标树，而不是额外生成一个 `<fragment>` 元素。

## 5. 使用场景

| 场景 | 为什么适合 |
| --- | --- |
| 批量构造多个兄弟节点 | 先放片段，再一次插入。 |
| XML 转换 | 用片段作为替换节点集合。 |
| 避免临时包装元素 | 不想输出额外标签。 |

## 6. 常见坑与经验

片段不是元素，不能设置 tagName 或属性。如果你需要一个真实包装标签，用 `QDomElement`。

跨文档构造片段仍要注意节点归属。用目标文档创建片段和子节点最省心。

## 7. 知识点覆盖

- DOM 文档片段的临时容器角色。
- 批量插入多个兄弟节点。
- 片段与真实元素的区别。
