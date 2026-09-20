# Qt QDomImplementation 深入笔记：DOM 能力查询、DTD 工厂与非法数据策略

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDomImplementation>`  
> 所属模块：`Qt6::Xml`  
> 类型性质：值类型；普通成员可重入，`invalidDataPolicy()` 与 `setInvalidDataPolicy()` 例外。

`QDomImplementation` 描述 Qt DOM 实现支持什么能力，并提供两个不那么常用、但影响很大的能力：

- 创建带 document type 的 `QDomDocument`。
- 设置 DOM 工厂遇到非法 XML 数据时的全局处理策略。

普通 XML 编辑通常从 `QDomDocument`、`QDomElement` 开始，不需要手动创建它。最常见的获取方式是：

```cpp
QDomImplementation implementation = document.implementation();
```

它解决的是“当前 DOM 支持哪些标准特性、如何构造携带 DOCTYPE 的文档、工厂遇到非法名称或内容时如何处理”的问题，不是一个常规 XML 节点类型。

## 1. 能力查询：不要把它当作泛用版本检测

```cpp
if (implementation.hasFeature("XML", "1.0")) {
    // 当前 Qt DOM 声明支持 XML 1.0
}
```

Qt 6.11.1 文档列出的受支持 feature/version 是 `XML` / `1.0`。`hasFeature()` 用于 DOM feature 查询，不是 Qt 运行库版本判断、XML schema 验证，也不表示某份输入文档一定符合要求。

## 2. 创建带 DOCTYPE 的文档

常规文档直接默认构造并创建根 element 即可。只有确实需要 DTD document type 时，才使用这组工厂：

```cpp
QDomImplementation impl;

QDomDocumentType doctype = impl.createDocumentType(
    "catalog",
    "-//Example//Catalog 1.0//EN",
    "catalog.dtd");

QDomDocument document = impl.createDocument(
    "urn:example:catalog",
    "catalog",
    doctype);
```

`createDocument()` 会创建 document type，并添加 qualified name 为 `qName`、命名空间为 `nsURI` 的根 element。`createDocumentType()` 单独得到的 document type 不能像普通节点一样随意塞进文档；它的正式用途是作为 `createDocument()` 的参数。

若 `systemId` 为空，`publicId` 也会被置为空，因为 public identifier 不能脱离 system identifier 单独存在。

## 3. `InvalidDataPolicy`：全局工厂行为，不是局部容错

`QDomDocument` 的工厂函数收到非法 XML 数据，例如不合法 tag 名或无法放入某种节点的数据时，行为由这个枚举决定：

- `AcceptInvalidChars`：仍将数据存入 DOM，生成的 XML 可能不再是良构文档。这是默认值。
- `DropInvalidChars`：删除非法字符后继续创建。
- `ReturnNullNode`：工厂直接返回空节点。

```cpp
QDomImplementation::setInvalidDataPolicy(
    QDomImplementation::ReturnNullNode);

QDomElement element = document.createElement("not valid~name");
if (element.isNull()) {
    qWarning() << "Invalid element name";
}
```

最容易出错的地方是作用范围：`setInvalidDataPolicy()` 影响进程内**所有已存在和未来创建的** `QDomDocument` 实例，不是某个 document 的私有设置。它和对应的 `invalidDataPolicy()` 都不是可重入 API；多线程程序不能把它当成可随意临时切换的线程局部开关。

实际应用应尽量在初始化阶段确定一次策略。对需要严谨输出的程序，`ReturnNullNode` 往往比静默删除字符或生成不良构 XML 更容易暴露问题。

## 4. 空 implementation 和相等比较

默认构造的 `QDomImplementation` 是 null。由 `QDomDocument::implementation()` 获得的对象则不是 null。

`operator==` 与 `operator!=` 判断的是两个 implementation 是否来自同一个 `QDomDocument`，不是比较两个文档的 XML 内容、DOCTYPE 字符串或 feature 集合。它们适用于确认句柄来源，不适合作为文档内容相等判断。

## 5. 与 `QDomDocument` 的关系

```text
QDomDocument
  ├─ implementation() -> QDomImplementation
  ├─ doctype()        -> QDomDocumentType
  └─ createElement()  -> QDomElement
```

对于绝大多数构建 XML 的需求，直接用 `QDomDocument` 的工厂函数。只有需要 document type、DOM feature 查询，或必须明确非法输入策略时，才进入 `QDomImplementation` 这一层。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 策略枚举 | `AcceptInvalidChars` | 非法数据仍写入 DOM | 默认值；最终文档可能不再良构，通常不适合作为严格输出策略 |
| 策略枚举 | `DropInvalidChars` | 从输入中删除非法字符后再创建节点 | 会静默改变数据；需要审计原始输入时要谨慎 |
| 策略枚举 | `ReturnNullNode` | 遇到非法数据时让工厂返回空节点 | 调用方必须检查 `isNull()`，适合尽早暴露无效数据 |
| 构造 | `QDomImplementation()` | 创建默认的 implementation 句柄 | 默认对象是 null；通常从 `QDomDocument::implementation()` 获取有效对象 |
| 构造 | `QDomImplementation(const QDomImplementation &implementation)` | 复制 implementation 句柄 | 复制的是实现句柄，不是复制 XML 文档 |
| 析构 | `~QDomImplementation()` | 销毁 implementation 值对象 | 没有 QObject 所有权语义 |
| 功能查询 | `hasFeature(const QString &feature, const QString &version) const` | 查询 Qt DOM 是否支持某个 DOM feature/version | Qt 6.11.1 文档列出 `XML` / `1.0`；它不是 schema 或输入合法性检查 |
| DTD 工厂 | `createDocumentType(const QString &qName, const QString &publicId, const QString &systemId)` | 创建可用于新文档的 document type | 要和 `createDocument()` 配套；没有 system ID 时 public ID 会被清空 |
| 文档工厂 | `createDocument(const QString &nsURI, const QString &qName, const QDomDocumentType &doctype)` | 创建带 document type 和根 element 的 DOM document | 自动添加 root element；仅在需要 DOCTYPE 时比默认构造更合适 |
| 全局策略 | `invalidDataPolicy()` | 返回当前全局非法数据处理策略 | 非可重入 API；不要在多线程环境把它当作无锁查询 |
| 全局策略 | `setInvalidDataPolicy(InvalidDataPolicy policy)` | 设置所有现有与未来 `QDomDocument` 工厂的非法数据策略 | 非可重入且是全局副作用；在应用初始化阶段设置并避免运行时来回切换 |
| 有效性 | `isNull()` | 判断 implementation 是否为 null | `QDomDocument::implementation()` 获取的对象返回 `false`；默认构造对象返回 `true` |
| 比较 | `operator==(const QDomImplementation &other) const` | 判断两个 implementation 是否来自同一个 document | 不比较 XML 内容或文档结构 |
| 比较 | `operator!=(const QDomImplementation &other) const` | 判断两个 implementation 是否来自不同 document | 是 `operator==` 的反向判断，仍不等于文档内容不同 |
| 赋值 | `operator=(const QDomImplementation &other)` | 让当前值对象引用另一个 implementation | 用于值对象复制，不会合并或替换任何 DOM 树 |

---

### 一句话总结

`QDomImplementation` 是 Qt DOM 的能力与工厂层。日常 XML 读写不必常碰它；真正需要谨慎的是 `InvalidDataPolicy`，因为它是影响全部 `QDomDocument` 的非可重入全局设置。
