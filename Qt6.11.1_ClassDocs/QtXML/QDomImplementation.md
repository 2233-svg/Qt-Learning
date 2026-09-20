# QDomImplementation
> Qt 6.11.1 · Qt XML · 来自 `QDomImplementation`

## 1. 先建立直觉

`QDomImplementation` 表示 Qt DOM 实现对象。它很少出现在日常 XML 读写里，主要用于创建带 doctype 的文档、创建 `QDomDocumentType`，以及控制无效 XML 字符进入 DOM 工厂函数时的策略。

## 2. 类说明

保留类说明：这些 API 来自 `QDomImplementation`，属于 Qt XML 模块，用于创建 DOM 文档类型、文档，并配置无效数据策略。

`QDomDocument::implementation()` 可取得与文档相关的 implementation。默认构造的 implementation 可能是空对象。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `createDocument(nsURI, qName, doctype)` | 创建带根元素和 doctype 的文档。 |
| `createDocumentType(qName, publicId, systemId)` | 创建文档类型声明对象。 |
| `hasFeature(feature, version)` | 查询 DOM 实现特性，例如 XML 1.0。 |
| `isNull()` | 判断 implementation 是否为空。 |
| `invalidDataPolicy()` / `setInvalidDataPolicy()` | 查询或设置全局无效数据策略。 |
| `AcceptInvalidChars` | 接受无效字符，可能输出非良构 XML。 |
| `DropInvalidChars` | 丢弃无效字符。 |
| `ReturnNullNode` | 工厂函数遇到无效数据时返回空节点。 |

## 4. 典型流程

```cpp
QDomImplementation impl;
QDomDocumentType type = impl.createDocumentType(
    "note", "-//demo//DTD note//EN", "note.dtd");
QDomDocument doc = impl.createDocument(QString(), "note", type);
```

无效数据策略：

```cpp
QDomImplementation::setInvalidDataPolicy(QDomImplementation::ReturnNullNode);
QDomElement e = doc.createElement("bad name");
QVERIFY(e.isNull());
```

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 生成带 DOCTYPE 的 XML | createDocumentType + createDocument。 |
| 严格控制非法 XML 字符 | 设置 invalid data policy。 |
| DOM 兼容性检查 | `hasFeature("XML", "1.0")`。 |

## 6. 常见坑与经验

`setInvalidDataPolicy()` 是全局策略，会影响已有和未来的 `QDomDocument` 工厂函数。库代码里随意修改它，可能影响调用者。

接受无效字符可能让最终输出不是良构 XML。导出给外部系统时，优先选择丢弃或返回空节点并报错。

## 7. 知识点覆盖

- DOM implementation 和 doctype 创建。
- 无效 XML 数据策略。
- 全局设置的影响范围。
