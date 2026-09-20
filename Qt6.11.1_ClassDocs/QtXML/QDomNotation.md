# QDomNotation
> Qt 6.11.1 · Qt XML · 来自 `QDomNotation`

## 1. 先建立直觉

`QDomNotation` 表示 DTD 中的 notation 声明。notation 用于描述非 XML 数据格式或未解析实体的外部标识，在现代应用中不常直接使用，但解析旧 XML/DTD 时可能遇到。

## 2. 类说明

保留类说明：这些 API 来自 `QDomNotation`，属于 Qt XML 模块，用于表示 DOM 文档类型中的 notation 声明。

它通常从 `QDomDocumentType::notations()` 返回的命名节点集合中取得。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `publicId()` | 返回 notation 的 public identifier。 |
| `systemId()` | 返回 notation 的 system identifier。 |
| `nodeType()` | 返回 `NotationNode`。 |

## 4. 典型流程

```cpp
QDomNamedNodeMap notations = doc.doctype().notations();
for (int i = 0; i < notations.size(); ++i) {
    QDomNotation notation = notations.item(i).toNotation();
    qDebug() << notation.nodeName() << notation.publicId() << notation.systemId();
}
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 旧 XML/DTD 兼容 | 保留 notation 声明。 |
| DTD 分析工具 | 展示 notation 列表和外部标识。 |
| 未解析实体处理 | 根据 entity 的 notationName 关联 notation。 |

## 6. 常见坑与经验

notation 是 DTD 元数据，不是 XML 元素。不要用元素查询 API 找它。

多数现代 XML 配置格式不使用 notation。遇到它时通常说明你在处理较老或较正式的 DTD 文档体系。

## 7. 知识点覆盖

- DTD notation 声明。
- publicId/systemId。
- notation 与未解析实体的关系。
