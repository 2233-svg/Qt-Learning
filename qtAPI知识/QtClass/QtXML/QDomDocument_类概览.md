# Qt QDomDocument 深入笔记：XML DOM 树的根、工厂与解析入口

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDomDocument>`  
> 所属模块：`Qt6::Xml`  
> 继承：`QDomNode -> QDomDocument`  
> 线程说明：类成员可重入；不同线程使用不同 document 实例可以并行，但同一棵可变 DOM 树不应被并发修改。

`QDomDocument` 表示一整份 XML 文档，也是 Qt DOM 节点的创建者。它负责把 XML 文本解析为可遍历、可编辑的树，并提供 element、attribute、text、comment、CDATA、fragment 等所有节点的工厂函数。

```text
XML 字节 / 字符串 / 设备 / 流
             |
             v
  QDomDocument::setContent()
             |
             v
 QDomDocument
   └─ documentElement()
       └─ QDomElement / QDomText / QDomAttr / ...
```

它适合配置文件、体积有限的行业 XML、需要随机访问和多次编辑的文档。它不适合超大 XML 或纯流式处理：DOM 会把整棵树留在内存中，这类场景通常更适合 `QXmlStreamReader`。

## 1. 两种最常用工作流

### 1.1 解析已有 XML

```cpp
#include <QDomDocument>
#include <QFile>

QFile file("settings.xml");
if (!file.open(QIODevice::ReadOnly)) {
    return;
}

QDomDocument document;
const QDomDocument::ParseResult result = document.setContent(
    &file,
    QDomDocument::ParseOption::UseNamespaceProcessing);

if (!result) {
    qWarning().noquote()
        << file.fileName()
        << result.errorLine << result.errorColumn
        << result.errorMessage;
    return;
}

QDomElement root = document.documentElement();
```

先由 `setContent()` 建树，再从 `documentElement()` 取得根 element。不要在解析失败后继续访问根节点，也不要只把 `errorMessage` 丢到日志里而缺少输入来源与行列位置。

### 1.2 从零构建 XML

```cpp
QDomDocument document;

QDomElement root = document.createElement("settings");
document.appendChild(root);

QDomElement theme = document.createElement("theme");
theme.setAttribute("name", "dark");
theme.appendChild(document.createTextNode("enabled"));
root.appendChild(theme);

const QByteArray output = document.toByteArray(2);
```

默认构造的其他 QDom 节点只是空句柄。应由**同一个** `QDomDocument` 的工厂函数创建节点，再用 `appendChild()`、`insertBefore()` 等树操作接入文档。

## 2. 解析选项会改变你看到的树

Qt 6.5 起，新的 `setContent()` 重载接收 `ParseOptions`：

- `Default`：没有额外选项。默认**不**做 namespace 处理。
- `UseNamespaceProcessing`：填充 element/attribute 的 `prefix()`、`localName()`、`namespaceURI()`。
- `PreserveSpacingOnlyNodes`：保留仅由空白字符组成的文本节点。

若没有启用 namespace 处理，`prefix()`、`localName()` 与 `namespaceURI()` 都会返回空字符串，即使源 XML 中写了 namespace。因此，项目若按 namespace URI 查找节点，必须在解析时显式传入 `UseNamespaceProcessing`。

默认情况下，只含空白字符的 text node 会被丢弃。需要保留格式化空白、编辑器往返保存或严格比较节点序列时，加入 `PreserveSpacingOnlyNodes`。

新版 `setContent()` 解析失败返回 `ParseResult`。Qt 6.8 起，旧的 `bool + 错误输出参数` 重载已经弃用；新代码应统一使用结果对象。

对于 `QIODevice *` 重载，调用方应自己在调用前打开设备。Qt 6.11.1 会尝试以只读方式打开未打开的设备，但 Qt 文档说明 Qt 7 将不再这么做。

## 3. 节点工厂：先创建，再插入

`QDomDocument` 的工厂函数只创建属于本 document 的节点；创建后通常还没有 parent，需要你决定插入位置。

```text
createElement()              普通元素
createElementNS()            带 namespace 的元素
createAttribute()            普通属性节点
createAttributeNS()          带 namespace 的属性节点
createTextNode()             普通 XML 文本
createCDATASection()         CDATA 文本
createComment()              注释
createProcessingInstruction() 处理指令
createEntityReference()      实体引用
createDocumentFragment()     临时批量节点容器
```

这些工厂遇到非法 XML 名称或不能容纳的字符时，受 `QDomImplementation::InvalidDataPolicy` 这个**全局**策略影响。不要把输入清洗寄托给工厂函数；应用应在业务边界验证名字、文本与外部输入。

`createElementNS()` 的 `qName` 为空时，会直接返回空 element，不受非法数据策略影响。

## 4. 查询：根节点、标签搜索和 ID 陷阱

### 4.1 根节点

`documentElement()` 返回文档根 element。空文档或解析失败后它是空 element；使用前检查 `isNull()`。

### 4.2 标签搜索

`elementsByTagName()` 与 `elementsByTagNameNS()` 返回整份 document 中的匹配节点，顺序是 element 树的前序遍历顺序。它们适合一次性收集同类节点；只想遍历某个局部子树时，使用 `QDomElement` 上对应的查询 API 更合适。

### 4.3 `elementById()` 在当前实现里不能当索引

Qt 6.11.1 文档明确说明，QDom classes 不知道哪些属性属于 XML ID 类型，因此 `elementById()` 当前总会返回空 element。不要把它当作 HTML DOM 的 `getElementById()` 使用。

需要按业务 `id` 属性查找时，自己遍历或建立 `QHash<QString, QDomElement>` 索引：

```cpp
QHash<QString, QDomElement> byId;
const QDomNodeList nodes = document.elementsByTagName("item");
for (int i = 0; i < nodes.size(); ++i) {
    const QDomElement item = nodes.at(i).toElement();
    byId.insert(item.attribute("id"), item);
}
```

## 5. 跨 document 复制：`importNode()`

节点不能直接作为另一份 document 的 child 使用。需要把来自另一棵 DOM 树的节点接入当前 document 时，使用 `importNode()`：

```cpp
QDomNode imported = target.importNode(sourceElement, true);
target.documentElement().appendChild(imported);
```

它复制节点，源节点仍留在原 document。返回节点属于 target document、初始没有 parent；`deep == true` 时一并复制后代，`false` 时只复制当前节点。

不能导入 `QDomDocument` 和 `QDomDocumentType`，传入它们或空节点会得到空结果。不要跳过返回值检查。

## 6. DTD、实体与 implementation

`doctype()` 返回本 document 的 `QDomDocumentType`，用来读取 DOCTYPE、DTD entity 与 notation 的声明信息。它不是用来查询普通 element 的入口。

`implementation()` 返回 `QDomImplementation`，主要用于 DOM feature 查询、创建带 document type 的新文档，以及查看/设置全局非法数据策略。普通 XML 编辑流程通常不需要它。

解析实体时，Qt 会把内容中的字符引用和内部通用实体转换为 `QDomText` 中的对应字符；未解析实体引用会被替换为空字符串。因此，业务代码不应依赖“源 XML 写了实体引用，就一定会在 DOM 中看到 `QDomEntityReference`”。

## 7. 序列化与浅拷贝

`toByteArray()` 以 UTF-8 返回 XML 字节，适合写文件、网络或哈希；`toString()` 返回 `QString`，适合日志、界面与调试。

- `indent` 是子元素的缩进空格数。
- `toString(-1)` 不额外添加任何空白。

拷贝构造与赋值都是浅拷贝，多个 `QDomDocument` 句柄共享同一内部树。若要独立副本，使用 `cloneNode(true)` 深复制，而不是简单 `QDomDocument copy = original;`。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 解析选项 | `ParseOption::Default` | 不启用额外解析选项 | 默认不做 namespace 处理，纯空白 text node 也会被丢弃 |
| 解析选项 | `ParseOption::UseNamespaceProcessing` | 解析并保存 prefix、local name、namespace URI | 需要按 namespace 查询或访问这些字段时必须启用 |
| 解析选项 | `ParseOption::PreserveSpacingOnlyNodes` | 保留只包含空白字符的文本节点 | 编辑器、格式往返或严格节点比较时使用；树会包含更多 text node |
| 解析选项 | `ParseOptions` | 多个 `ParseOption` 的 flags 组合类型 | 传给新版 `setContent()`；可按位组合多个选项 |
| 解析结果 | `ParseResult` | 保存 `setContent()` 的成功状态与错误位置 | Qt 6.5 起可用；详细字段见 `QDomDocument::ParseResult` 笔记 |
| 构造 | `QDomDocument()` | 创建空 document | 之后用 `setContent()` 解析，或用工厂函数创建节点并插入 root |
| 构造 | `QDomDocument(const QString &name)` | 创建 document 并设置 document type 名称 | 适合需要该名称的文档；不等于已创建根 element |
| 构造 | `QDomDocument(const QDomDocumentType &doctype)` | 创建带给定 document type 的 document | 用于 DTD 场景；根 element 仍需按流程创建或解析 |
| 构造 | `QDomDocument(const QDomDocument &document)` | 复制 document 句柄 | 浅拷贝；修改一份会影响另一份 |
| 赋值 | `operator=(const QDomDocument &other)` | 让当前 document 句柄引用另一份内部树 | 同样是浅拷贝；独立副本应深复制 |
| 析构 | `~QDomDocument()` | 释放 document 句柄所持资源 | 内部树会在 document 与所有引用它的 QDom 句柄都释放后销毁 |
| 节点工厂 | `createElement(const QString &tagName)` | 创建普通 element | 节点初始没有 parent；用 `appendChild()` 等接入树；无效名称受全局非法数据策略影响 |
| 节点工厂 | `createElementNS(const QString &nsURI, const QString &qName)` | 创建带 namespace 的 element | `qName` 为空时直接返回空 element；会设置 prefix 与 local name |
| 节点工厂 | `createAttribute(const QString &name)` | 创建普通属性节点 | 通过 `setAttributeNode()` 接到 element；普通键值写入直接用 `setAttribute()` 更简洁 |
| 节点工厂 | `createAttributeNS(const QString &nsURI, const QString &qName)` | 创建带 namespace 的属性节点 | 用于 namespace 属性；无效 qName 受全局非法数据策略影响 |
| 节点工厂 | `createTextNode(const QString &value)` | 创建普通 XML 文本节点 | 用于 element 内容；特殊字符按 XML 规则序列化 |
| 节点工厂 | `createCDATASection(const QString &value)` | 创建 CDATA 节点 | 内容必须满足 CDATA 限制；无效数据的处理受全局策略影响 |
| 节点工厂 | `createComment(const QString &value)` | 创建 XML 注释节点 | 注释内容必须满足 XML 注释语法；不应用作业务数据存储 |
| 节点工厂 | `createProcessingInstruction(const QString &target, const QString &data)` | 创建处理指令节点 | target 与 data 都要满足 XML 处理指令限制；一般只为兼容特定 XML 格式使用 |
| 节点工厂 | `createEntityReference(const QString &name)` | 创建实体引用节点 | 解析后的实体引用可能已被展开；仅用于需要保留引用结构的 DTD 场景 |
| 节点工厂 | `createDocumentFragment()` | 创建临时多节点容器 | 传给树插入 API 时 child 会被展开插入，fragment 随后变空 |
| 文档查询 | `documentElement() const` | 返回根 element | 空文档时返回空 element；解析失败后不要继续假设它有效 |
| 文档查询 | `doctype() const` | 返回 document type / DTD 入口 | 通过它读取 entity、notation、public ID 与 system ID；没有 DOCTYPE 时为空 |
| 文档查询 | `implementation() const` | 返回 DOM implementation 句柄 | 用于 feature、DTD 文档工厂和全局非法数据策略；普通编辑很少需要 |
| 文档查询 | `elementById(const QString &elementId)` | 按 XML ID 查找 element | Qt 6.11.1 当前实现始终返回空 element；请自己遍历或建索引 |
| 文档查询 | `elementsByTagName(const QString &tagName) const` | 返回整份 document 中同名 element 的列表 | 结果按前序遍历排序；大量重复查询时应建立业务索引 |
| 文档查询 | `elementsByTagNameNS(const QString &nsURI, const QString &localName)` | 返回指定 namespace URI 与 local name 的 element 列表 | 解析阶段必须启用 namespace 处理，才能可靠按 namespace 工作 |
| 跨文档 | `importNode(const QDomNode &importedNode, bool deep)` | 复制另一份 document 的节点到当前 document | 源节点不移动；返回节点无 parent；document 与 document type 不能导入，失败返回空节点 |
| 节点类型 | `nodeType() const` | 返回 `QDomNode::DocumentNode` | 在通用节点遍历时识别整份 document 节点 |
| 解析 | `setContent(const QByteArray &data, ParseOptions options)` | 从 XML 字节解析并设置 document 内容 | Qt 6.5 起返回 `ParseResult`；编码按 XML 规则检测，失败先检查结果对象 |
| 解析 | `setContent(QAnyStringView text, ParseOptions options)` | 从 XML 字符串视图解析并设置内容 | 字符串生命周期只需覆盖调用；成功后 document 自己持有解析树 |
| 解析 | `setContent(QIODevice *device, ParseOptions options)` | 从已打开的 I/O 设备解析 XML | 应由调用方先以只读方式打开；Qt 7 不再自动打开未打开设备 |
| 解析 | `setContent(QXmlStreamReader *reader, ParseOptions options)` | 从 XML 流读取器解析并设置内容 | 调用方负责 reader 状态与生命周期；仍会生成完整 DOM 树 |
| 序列化 | `toByteArray(int indent = 1) const` | 将 document 转为 UTF-8 XML 字节 | 适合写文件和网络；indent 是每层缩进空格数 |
| 序列化 | `toString(int indent = 1) const` | 将 document 转为 `QString` XML 文本 | `indent == -1` 时不额外添加空白，适合紧凑输出 |

---

### 一句话总结

`QDomDocument` 是 Qt XML DOM 的中心：它解析整份 XML、创建所有同属一棵树的节点、支持查询与跨文档复制，并负责输出文本。真正要记住的是 parse options 会改变树形态、`elementById()` 当前不可用、`importNode()` 复制不移动，以及 document 复制是共享内部树的浅拷贝。
