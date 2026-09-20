# QDomDocumentType
> Qt 6.11.1 · Qt XML · 来自 `QDomDocumentType`

## 1. 先建立直觉

`QDomDocumentType` 表示 XML 的文档类型声明，也就是 `<!DOCTYPE ...>`。它保存 doctype 名称、public/system id、内部子集，以及 DTD 中声明的实体和 notation。

## 2. 类说明

保留类说明：这些 API 来自 `QDomDocumentType`，属于 Qt XML 模块，用于表示 DOM 文档类型节点。

它继承 `QDomNode`，节点类型是 `DocumentTypeNode`。通常通过 `QDomImplementation::createDocumentType()` 创建，或从解析后的 `QDomDocument::doctype()` 取得。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `name()` | 返回 doctype 名称。 |
| `publicId()` / `systemId()` | 返回外部 DTD 标识。 |
| `internalSubset()` | 返回内部 DTD 子集文本。 |
| `entities()` | 返回实体声明集合。 |
| `notations()` | 返回 notation 声明集合。 |
| `nodeType()` | 返回 `DocumentTypeNode`。 |

## 4. 典型流程

```cpp
QDomDocumentType type = doc.doctype();
if (!type.isNull()) {
    qDebug() << type.name() << type.publicId() << type.systemId();
}
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 保留旧 XML 格式的 DOCTYPE | 解析后输出时不丢文档类型信息。 |
| 检查文档种类 | 用 `name()`、public/system id 判断格式。 |
| 分析 DTD 声明 | 查看 entities/notations。 |

## 6. 常见坑与经验

Qt DOM 能保存 doctype 信息，但这不等于完整 DTD 验证器。需要严格校验 DTD/Schema 时，要引入专门验证流程。

外部 DTD 的 systemId 可能指向网络或本地资源。处理不可信 XML 时，不要盲目按这些标识加载外部资源。

## 7. 知识点覆盖

- XML DOCTYPE、publicId、systemId、internal subset。
- 实体和 notation 声明集合。
- doctype 信息保存与验证职责的区别。
