# Qt QDomNotation 深入笔记：读取 DTD 对未解析数据格式的声明

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDomNotation>`  
> 所属模块：`Qt6::Xml`  
> 继承：`QDomNode -> QDomNotation`  
> 节点性质：只读、没有 parent。

`QDomNotation` 表示 DTD 中的 NOTATION 声明。NOTATION 用名称描述未解析实体的数据格式，或用于形式化声明处理指令的目标；它不是 XML 内容树里的元素，也不是一个可播放、可解码或可验证的数据格式对象。

```xml
<!NOTATION jpeg SYSTEM "image/jpeg">
<!ENTITY logo SYSTEM "logo.jpg" NDATA jpeg>
```

上例中 `jpeg` 对应一个 `QDomNotation`，而 `logo` 是 `QDomEntity`。实体通过名字引用 notation，notation 再通过 public ID 或 system ID 描述该格式。

## 1. 为什么会遇到它

现代业务 XML 很少主动设计 DTD/NOTATION，但处理旧出版格式、SGML 衍生规范、历史配置文件或需要兼容外部 DTD 的系统时，仍可能看到它。

`QDomNotation` 的作用是让程序读取这类声明元数据，例如：

- 未解析实体声称采用何种外部格式。
- 该格式的 public identifier 是什么。
- 该格式的 system identifier 是什么。

它不负责加载 `systemId()` 指向的资源，也不会根据 `image/jpeg` 自动解析图片。资源定位、验证与安全策略完全是应用自己的职责。

## 2. 从 document type 的 notation 表中获取

NOTATION 通常来自已经解析的 document type：

```cpp
QDomDocumentType doctype = document.doctype();
QDomNamedNodeMap notations = doctype.notations();

QDomNotation notation = notations.namedItem("jpeg").toNotation();
if (!notation.isNull()) {
    qDebug() << notation.publicId()
             << notation.systemId();
}
```

`namedItem()` 找不到名称时，转成 `QDomNotation` 会得到空节点。默认构造的 `QDomNotation` 同样只是空句柄，不能用来手工制造一条有效的 DTD NOTATION 声明。

## 3. 与 `QDomEntity` 的关系

可以把两者的职责理解为：

```text
QDomNotation：声明“某个名字代表一种外部数据格式”
QDomEntity：声明“某个实体引用外部数据，并可关联一个 notation 名字”
```

只有未解析实体才会使用 `QDomEntity::notationName()` 关联 NOTATION。`QDomNotation` 自身没有“有哪些实体使用我”的反向查询 API；若需要这个关系，需要遍历 `QDomDocumentType::entities()` 并比较各实体的 `notationName()`。

## 4. 只读、无 parent、浅拷贝

DOM 不支持编辑 notation node，它也没有 parent。它是从 DTD 读出的声明信息，不是适合插入 `appendChild()` 或用 setter 修改的 DOM 内容节点。

复制构造和赋值都是浅拷贝：多个 `QDomNotation` 句柄指向同一内部声明。要保留独立的数据快照，直接把 `publicId()`、`systemId()` 等字符串复制到你的业务结构里，往往比复制 DOM 节点更清楚。

## 5. 安全边界

`systemId()` 是外部标识字符串，可能像路径、URI 或其他系统标识，但不能因为它存在就直接打开资源。对来自不可信 XML 的 DTD 元数据，应由应用决定是否允许外部资源、允许哪些协议和目录，以及如何记录失败。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDomNotation()` | 创建空 notation 节点句柄 | 真实节点应从 `QDomDocumentType::notations()` 获取 |
| 构造 | `QDomNotation(const QDomNotation &notation)` | 复制 notation 节点句柄 | 浅拷贝；不会生成独立、可编辑的 DTD 声明 |
| 赋值 | `operator=(const QDomNotation &other)` | 让当前句柄引用另一个 notation 节点 | 不改变 DTD 内容；需要业务快照时复制返回的字符串 |
| 节点类型 | `nodeType() const` | 返回 `QDomNode::NotationNode` | 遍历 DTD 元数据时用于识别 NOTATION 节点 |
| 公共标识 | `publicId() const` | 返回 notation 的 public identifier | 是描述信息；空字符串表示声明中未提供该标识 |
| 系统标识 | `systemId() const` | 返回 notation 的 system identifier | 不会自动加载资源；来自不可信 XML 时必须自行执行安全校验 |

---

### 一句话总结

`QDomNotation` 是 DTD 中对未解析数据格式的只读声明。它通过 public ID 和 system ID 提供描述信息，常与 `QDomEntity::notationName()` 配合查看，但并不负责解析、加载或验证外部资源。
