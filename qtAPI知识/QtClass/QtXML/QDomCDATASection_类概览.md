# Qt QDomCDATASection 深入笔记：保留原始标记字符的 CDATA 节点

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDomCDATASection>`  
> 所属模块：`Qt6::Xml`  
> 继承：`QDomNode -> QDomCharacterData -> QDomText -> QDomCDATASection`

`QDomCDATASection` 表示 XML 的 CDATA 段：

```xml
<template><![CDATA[<item id="42">& raw-looking text</item>]]></template>
```

它的用途是把包含 `<`、`&` 等看起来像 XML 标记的内容按原样放进 XML，不必把每个分隔符都转义。CDATA 仍然是一个 DOM 节点，不是“跳过 XML 处理的万能字符串容器”。

## 1. 什么时候应该用 CDATA

适合的场景：

- 在配置文件中嵌入一小段 XML、HTML、脚本或模板片段。
- 保存格式化文本，且希望保留其中大量 `<`、`&` 字符的原貌。
- 与已约定使用 CDATA 的外部 XML 格式对接。

不适合的场景：

- 普通标题、用户名、路径、说明文字：用 `QDomText`，让 XML 正常转义即可。
- 大型二进制数据：用 Base64、外部文件或专用容器，不要硬塞进 CDATA。
- 不可信内容的安全隔离：CDATA 只是 XML 表示法，不会验证或清理其中的脚本、SQL 或 HTML。

## 2. 创建 CDATA 节点

创建者仍然是 `QDomDocument`：

```cpp
#include <QDomCDATASection>
#include <QDomDocument>

QDomDocument document;
QDomElement script = document.createElement("script");
document.appendChild(script);

QDomCDATASection cdata =
    document.createCDATASection("if (a < b && b < c) { run(); }");
script.appendChild(cdata);
```

默认构造只产生空句柄。使用 `createCDATASection()` 才能创建属于该 document 的节点，再通过 DOM 插入 API 放到目标元素下。

## 3. 最重要的边界：`]]>` 会结束 CDATA

CDATA 内唯一被识别的分隔符就是结尾 `]]>`。因此：

- CDATA 不能嵌套。
- 内容中不能直接出现 `]]>`。

如果外部内容可能包含该字符串，必须先按格式要求拆分成多个 CDATA 节点或改用普通文本转义。不要把“CDATA 能原样放文本”误解为“任何字节序列都能直接放进去”。

## 4. 它和 `QDomText` 的不同

两者都能保存字符数据，也都可以通过继承的 `data()`、`setData()`、`replaceData()` 等方法修改内容，但序列化形式和 DOM 类型不同：

- `nodeType()`：`QDomText` 返回 `TextNode`，`QDomCDATASection` 返回 `CDATASectionNode`。
- 输出形式：普通文本会按 XML 规则转义特殊字符；CDATA 被包在 `<![CDATA[...]]>` 中。
- `normalize()`：相邻普通文本节点可以合并；相邻 CDATA 节点不会被合并。
- 内容选择：常规 XML 文本用 `QDomText`；含大量标记字符、且确实要保留原样的文本用 CDATA。

这也意味着不要把两者混作同一种节点。读取 XML 时若业务需要保留 CDATA 的表示形式，而不仅是其中的字符串，遍历时必须检查 `nodeType()`。

## 5. 复制和修改的行为

`QDomCDATASection` 的复制构造与赋值都是浅拷贝：两个 C++ 句柄会指向同一个底层节点。

```cpp
QDomCDATASection first = document.createCDATASection("<a/>");
QDomCDATASection alias = first;
alias.setData("<b/>");
// first.data() 现在也是 "<b/>"
```

需要独立节点时使用 `cloneNode()` 深复制。若只是想修改字符串内容，直接用继承的 `setData()` 或局部编辑 API；没有必要把节点移出再新建。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDomCDATASection()` | 创建空 CDATA 节点句柄 | 实际创建应使用 `QDomDocument::createCDATASection()` |
| 构造 | `QDomCDATASection(const QDomCDATASection &cdataSection)` | 复制另一个 CDATA 节点句柄 | 浅拷贝；两者共享同一个底层节点 |
| 赋值 | `operator=(const QDomCDATASection &other)` | 让当前句柄引用另一个 CDATA 节点 | 不是深复制；独立副本使用 `cloneNode()` |
| 节点类型 | `nodeType() const` | 返回 `QDomNode::CDATASectionNode` | 用于和普通 `TextNode`、`CommentNode` 区分 |
| 继承：读取 | `data() const` | 读取 CDATA 中的原始字符数据 | 返回内容本身，不包含外围的 `<![CDATA[` 和 `]]>` |
| 继承：整体写入 | `setData(const QString &data)` | 替换 CDATA 内容 | 新内容不能直接包含 `]]>`，否则无法形成单一合法 CDATA 段 |
| 继承：长度 | `length() const` | 返回 CDATA 数据长度 | 局部编辑前可用它校验 offset |
| 继承：截取 | `substringData(unsigned long offset, unsigned long count)` | 读取指定范围的 CDATA 字符 | 不改变节点或树结构 |
| 继承：追加 | `appendData(const QString &arg)` | 在 CDATA 尾部追加字符 | 追加后的整体内容仍不能形成 `]]>` |
| 继承：插入 | `insertData(unsigned long offset, const QString &arg)` | 在 CDATA 内指定位置插入字符 | 对外部片段先检查 CDATA 结束分隔符 |
| 继承：删除 | `deleteData(unsigned long offset, unsigned long count)` | 删除一段 CDATA 字符 | 只修改内容，不删除节点 |
| 继承：替换 | `replaceData(unsigned long offset, unsigned long count, const QString &arg)` | 替换一段 CDATA 字符 | 最终数据必须避免 `]]>`；不满足时改用拆分节点或普通文本转义 |
| 继承：拆分 | `splitText(int offset)` | 继承自 `QDomText` 的文本节点拆分接口 | CDATA 需要保留类型与分段边界时不要轻率使用；拆分后应检查实际节点类型和序列化结果 |

---

### 一句话总结

`QDomCDATASection` 用于把带有标记字符的内容按原样嵌入 XML。它不是普通文本的默认替代品，核心限制是不能嵌套、内容不能含 `]]>`，并且相邻 CDATA 节点不会被 `normalize()` 自动合并。
