# QDomEntity
> Qt 6.11.1 · Qt XML · 来自 `QDomEntity`

## 1. 先建立直觉

`QDomEntity` 表示 DTD 中声明的实体。它描述实体的 publicId、systemId 和 notationName 等元数据，而不是日常文本里的一个普通字符片段。

## 2. 类说明

保留类说明：这些 API 来自 `QDomEntity`，属于 Qt XML 模块，用于表示 DOM 文档类型中的实体声明。

实体通常通过 `QDomDocumentType::entities()` 返回的 `QDomNamedNodeMap` 访问，而不是手动创建。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `publicId()` | 返回实体 public identifier。 |
| `systemId()` | 返回实体 system identifier。 |
| `notationName()` | 返回未解析实体关联的 notation 名称。 |
| `nodeType()` | 返回 `EntityNode`。 |

## 4. 典型流程

```cpp
QDomNamedNodeMap entities = doc.doctype().entities();
for (int i = 0; i < entities.size(); ++i) {
    QDomEntity entity = entities.item(i).toEntity();
    qDebug() << entity.nodeName() << entity.systemId();
}
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| DTD 分析工具 | 列出实体声明。 |
| 兼容旧 XML 工作流 | 保留实体元数据。 |
| 安全扫描 | 检查外部实体声明是否存在。 |

## 6. 常见坑与经验

实体处理和 XML 安全强相关。外部实体、递归实体、巨大展开都可能造成资源问题；对不可信输入要限制或避免依赖外部实体。

`QDomEntity` 是声明信息，不等同于内容中出现的 `&name;` 引用节点；后者对应 `QDomEntityReference`。

## 7. 知识点覆盖

- DTD 实体声明。
- publicId/systemId/notationName。
- 实体声明和实体引用的区别。
