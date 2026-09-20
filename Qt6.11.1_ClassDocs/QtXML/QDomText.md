# QDomText
> Qt 6.11.1 · Qt XML · 来自 `QDomText`

## 1. 先建立直觉

`QDomText` 是普通 XML 文本节点。元素之间的文字、元素内容里的纯文本，通常都用它表示。序列化时，特殊字符会按 XML 规则转义，例如 `<` 会变成文本内容而不是新标签。

## 2. 类说明

保留类说明：这些 API 来自 `QDomText`，属于 Qt XML 模块，用于表示普通文本节点。

它继承 `QDomCharacterData`，所以完整文本读写来自 `data()`/`setData()` 等基类函数。包含内容的文本节点应通过 `QDomDocument::createTextNode()` 创建。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QDomText()` | 创建空文本句柄。 |
| `nodeType()` | 返回 `TextNode`。 |
| `splitText(offset)` | 把当前文本节点从 offset 处拆成两个相邻文本节点。 |
| 继承的 `data()` / `setData()` | 读取或设置文本内容。 |

## 4. 典型流程

```cpp
QDomElement title = doc.createElement("title");
title.appendChild(doc.createTextNode("Qt & XML"));
```

输出时 `&` 会被正确转义，不需要手动写 `&amp;`。

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 元素的普通文本内容 | `appendChild(createTextNode(...))`。 |
| 修改已有文本 | `toText().setData(...)`。 |
| 文本编辑器式 DOM 操作 | `splitText()` 拆分节点。 |

## 6. 常见坑与经验

元素内容可能不止一个文本节点：注释、CDATA、子元素、相邻文本都可能混在一起。简单读取可用 `QDomElement::text()`，精确处理要遍历子节点。

不要把已经转义过的 XML 片段放进 text node，除非你真的希望它作为文本显示；DOM 会再按文本规则转义。

## 7. 知识点覆盖

- 普通文本节点和 XML 转义。
- `QDomCharacterData` 继承接口。
- 相邻文本节点和 `splitText()`。
