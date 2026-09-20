# Qt QDomCharacterData 深入笔记：统一编辑 DOM 字符节点的基类

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDomCharacterData>`  
> 所属模块：`Qt6::Xml`  
> 继承：`QDomNode -> QDomCharacterData`  
> 常见派生：`QDomText`、`QDomComment`、`QDomCDATASection`

`QDomCharacterData` 是 DOM 中“节点内容是一段字符”的公共操作层。它把读取、整体替换、局部插入、删除、替换和截取集中到一套 API 中，供普通文本、XML 注释和 CDATA 节点共同使用。

```text
QDomCharacterData
├─ QDomText          普通 XML 文本
│  └─ QDomCDATASection  原样保存标记字符的文本
└─ QDomComment       XML 注释
```

它解决的是“已经定位到一个字符节点后，怎样只修改其中的一段数据而不重建整个 DOM 树”。它不负责决定节点应以普通文本、注释还是 CDATA 形式序列化；那是具体派生类型的语义。

## 1. 大多数时候通过派生节点使用它

虽然 `QDomCharacterData` 有公开构造函数，但业务代码通常由 `QDomDocument` 创建具体节点：

```cpp
QDomText text = document.createTextNode("draft");
QDomComment comment = document.createComment("Editable section");
QDomCDATASection cdata = document.createCDATASection("<template/>");
```

随后你可以把它们统一当成 `QDomCharacterData` 来编辑：

```cpp
QDomCharacterData data = text.toCharacterData();
data.replaceData(0, 5, "final");
```

这段代码改变的是已有节点存储的字符，不会把 `QDomText` 自动变成 `QDomComment`，也不会改变它在 DOM 树中的父节点或兄弟顺序。

## 2. 整体替换和局部编辑的选择

```text
setData()                         整段换掉
appendData()                      尾部追加
insertData(offset, text)          在位置插入
deleteData(offset, count)         删除一段
replaceData(offset, count, text)  替换一段
substringData(offset, count)      读取一段
```

例如把 `version=1.0` 改成 `version=2.0`：

```cpp
QDomText text = document.createTextNode("version=1.0");
text.replaceData(8, 3, "2.0");
```

对完整字段覆盖使用 `setData()` 最直接。只有编辑器、差量更新或需要保留前后文本时，才使用带 `offset` 和 `count` 的局部操作。

所有位置参数都是 `unsigned long`。从用户输入、`qsizetype` 或其他整型转换前，应自行检查边界和符号；不要依赖越界 offset 的未明确业务语义。开始编辑前可先用 `length()` 获取当前长度。

## 3. 空节点与节点类型

空的 `QDomCharacterData` 句柄没有关联底层 DOM 节点：

- `data()` 返回空字符串。
- `nodeType()` 返回 `QDomNode::CharacterDataNode`。

而由具体派生类型创建的有效节点会有更具体的类型：

- `QDomText` 返回 `TextNode`。
- `QDomComment` 返回 `CommentNode`。
- `QDomCDATASection` 返回 `CDATASectionNode`。

因此，遍历混合 DOM 树时，不应只依据“能不能调用 `data()`”判断节点用途；要检查 `nodeType()`，再决定它应按文本、注释还是 CDATA 处理。

## 4. 句柄复制是浅拷贝

```cpp
QDomCharacterData first = text.toCharacterData();
QDomCharacterData second = first;

second.appendData("!");
// first.data() 也会看到 "!"
```

复制构造和赋值只复制句柄，底层 DOM 数据共享。它适合把节点传给函数或保存在容器中，不会复制整棵 XML 树；但也意味着任何一处修改都会反映到其他指向该节点的句柄上。

若需要独立节点，使用 `QDomNode::cloneNode()` 深复制，并根据实际类型转换回目标节点类型。

## 5. 和树结构 API 的边界

`QDomCharacterData` 的成员只编辑**节点内容**。下列需求属于 `QDomNode` 或具体类型的职责：

- 把节点移到另一个元素下：`appendChild()`、`insertBefore()`、`removeChild()`。
- 把一个普通文本节点切成两个节点：`QDomText::splitText()`。
- 合并相邻普通文本节点：`QDomNode::normalize()`。
- 保留或改变 CDATA/Comment 的节点类型：创建对应具体节点，而不是只调用 `setData()`。

把“改字符”和“改树结构”分开，是避免 DOM 修改代码失控的关键。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDomCharacterData()` | 创建空字符数据节点句柄 | 业务中通常使用 `QDomDocument` 创建具体的 Text、Comment 或 CDATA 节点 |
| 构造 | `QDomCharacterData(const QDomCharacterData &characterData)` | 复制字符数据节点句柄 | 浅拷贝；两个句柄引用同一底层节点 |
| 赋值 | `operator=(const QDomCharacterData &other)` | 让当前句柄引用另一个字符数据节点 | 不会创建独立副本；需要深复制时用 `cloneNode()` |
| 整体写入 | `setData(const QString &data)` | 用新字符串完全替换当前节点内容 | 不改变节点在树中的位置或实际节点类型 |
| 读取 | `data() const` | 返回当前节点存储的字符串 | 空节点返回空字符串；不要据此把空节点和空文本混为一谈 |
| 长度 | `length() const` | 返回当前字符串长度 | 用于校验局部操作的 offset 与 count |
| 追加 | `appendData(const QString &arg)` | 在当前字符串末尾追加内容 | 只改变当前节点，不创建新的 sibling 节点 |
| 插入 | `insertData(unsigned long offset, const QString &arg)` | 在指定字符位置插入内容 | 先检查 offset；参数是无符号类型，负值转换会产生意外结果 |
| 删除 | `deleteData(unsigned long offset, unsigned long count)` | 从指定位置删除一段字符 | 只删字符不删节点；操作前用 `length()` 校验范围 |
| 替换 | `replaceData(unsigned long offset, unsigned long count, const QString &arg)` | 用新内容替换指定范围 | 适合局部编辑；比手动 delete 再 insert 更直观 |
| 截取 | `substringData(unsigned long offset, unsigned long count)` | 返回指定范围的子串 | 只读，不改变数据或 DOM 树 |
| 节点类型 | `nodeType() const` | 返回当前引用节点的 DOM 类型 | 有效派生节点会返回 Text、Comment 或 CDATA 类型；空基类节点返回 `CharacterDataNode` |

---

### 一句话总结

`QDomCharacterData` 是 DOM 字符节点的编辑工具箱。它只改节点内的字符串，不改树结构和节点类别；局部编辑前先核对长度与偏移，复制句柄时牢记它是共享底层节点的浅拷贝。
