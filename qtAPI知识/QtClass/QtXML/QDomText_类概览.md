# Qt QDomText 深入笔记：XML 元素里的普通文本节点

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDomText>`  
> 所属模块：`Qt6::Xml`  
> 继承：`QDomNode -> QDomCharacterData -> QDomText`

`QDomText` 表示 DOM 树中的普通文本节点，也就是 XML 标签之间那段“真正显示或存储的字符”。

```xml
<title>Hello Qt</title>
       ^^^^^^^^
       QDomText
```

它解决的是“把文本作为 XML 树的一部分安全地创建、修改、拆分和序列化”，而不是用字符串拼接 XML。普通文本会在输出 XML 时按规则处理特殊字符；如果要保留一段不希望被当作标记解析的原始文本，应使用 `QDomCDATASection`。

## 1. 不要直接用默认构造来创建内容

默认构造得到的是空的 `QDomText` 句柄。实际创建文本节点应由所属 `QDomDocument` 完成：

```cpp
#include <QDomDocument>
#include <QDomText>

QDomDocument document;
QDomElement title = document.createElement("title");
document.appendChild(title);

QDomText text = document.createTextNode("Rock & Roll");
title.appendChild(text);

qDebug().noquote() << document.toString();
```

输出时，文本中的 `&` 会作为 XML 文本正确转义，而不是把 `& Roll` 当成 XML 结构。`QDomDocument` 才是节点的创建者和整棵树的持有者；`QDomText` 是指向树中节点的轻量句柄。

## 2. `QDomText`、CDATA 和 Comment 的区别

三者都来自字符数据体系，但写入 XML 的语义不同：

- `QDomText`：普通文本，是元素的可解析文本内容，也是最常用的选择。
- `QDomCDATASection`：输出为 `<![CDATA[...]]>`，用于保留可能包含 `<`、`&` 的原始文本片段。
- `QDomComment`：输出为 `<!-- ... -->`，给人看的注释，不属于业务数据。

例如保存一段配置说明、标题、用户名时用 `QDomText`；保存一段嵌入代码、模板或原始表达式且需要 CDATA 语义时才选 `QDomCDATASection`。

## 3. `splitText()` 会修改文档树

`splitText(offset)` 不是简单返回子字符串，而是把一个 DOM 节点拆成相邻的两个 DOM 节点：

```cpp
QDomText text = document.createTextNode("Hello world");
title.appendChild(text);

QDomText tail = text.splitText(5);
```

拆分后的结构是：

```text
<title>
  QDomText("Hello")
  QDomText(" world")
</title>
```

原对象保留前 `offset` 个字符；返回的新 `QDomText` 保存剩余字符，并被插入到原节点之后。它适合富文本式编辑、把命中的关键词从文本节点中切出来后包进新元素、或按结构修改 XML。

调用前要确认 offset 与当前文本长度匹配。若拆完又不需要保留相邻文本节点，可调用其父节点的 `QDomNode::normalize()` 合并相邻文本节点。

## 4. 复制是共享句柄，不是深复制

```cpp
QDomText first = document.createTextNode("draft");
QDomText alias = first;

alias.setData("published");
// first.data() 现在也是 "published"
```

拷贝构造和赋值都是浅拷贝：两个 `QDomText` 对象引用同一个底层 DOM 节点。想获得与原节点脱钩的新节点，要通过 `QDomNode::cloneNode()` 深复制，再用 `toText()` 转回文本句柄。

这点在把节点放进容器或函数返回值时很重要：复制句柄很便宜，但后续改动不是互相独立的。

## 5. 实际修改文本时常用的继承 API

`QDomText` 自己只增加 `splitText()`，文本内容的读写来自 `QDomCharacterData`：

```cpp
text.appendData("!");
text.replaceData(0, 5, "Hi");
const QString firstTwo = text.substringData(0, 2);
```

对“整段替换”使用 `setData()`；对局部编辑使用 `insertData()`、`deleteData()` 或 `replaceData()`。这些操作改变的是当前节点，不会自动生成新节点；需要改变树结构时才使用 `splitText()`、`appendChild()`、`insertBefore()` 等 DOM API。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDomText()` | 创建空文本节点句柄 | 不是创建并挂入文档的常用方式；通常用 `QDomDocument::createTextNode()` |
| 构造 | `QDomText(const QDomText &text)` | 复制另一个文本节点句柄 | 是浅拷贝；两个句柄修改的是同一个底层节点 |
| 赋值 | `operator=(const QDomText &other)` | 让当前句柄指向另一个文本节点 | 同样是浅拷贝；要独立副本使用 `cloneNode()` |
| 节点类型 | `nodeType() const` | 返回 `QDomNode::TextNode` | 用于遍历混合节点树时区分元素、文本、注释与 CDATA |
| 拆分 | `splitText(int offset)` | 把当前文本拆为前后两个相邻 `QDomText` 节点，并返回后半段 | 会修改 DOM 树；原节点保留前半段，offset 应与文本长度匹配 |
| 继承：读取 | `data() const` | 返回当前文本内容 | 来自 `QDomCharacterData`；读取的是节点当前值 |
| 继承：整体写入 | `setData(const QString &data)` | 整段替换文本内容 | 不改变节点在树中的位置，只修改该节点字符 |
| 继承：长度 | `length() const` | 返回文本长度 | 用它校验 `splitText()` 和局部编辑操作的 offset |
| 继承：截取 | `substringData(unsigned long offset, unsigned long count)` | 读取指定范围的文本片段 | 只读，不会拆节点或改文档树 |
| 继承：追加 | `appendData(const QString &arg)` | 在文本尾部追加字符 | 不创建新文本节点 |
| 继承：插入 | `insertData(unsigned long offset, const QString &arg)` | 在文本内部指定位置插入字符 | 只修改当前节点内容；先确认 offset 合法 |
| 继承：删除 | `deleteData(unsigned long offset, unsigned long count)` | 删除文本中的一段字符 | 适合局部编辑；不会删除整个 DOM 节点 |
| 继承：替换 | `replaceData(unsigned long offset, unsigned long count, const QString &arg)` | 替换文本中的一段字符 | 比“先 delete 再 insert”更直接；同样只改当前节点 |

---

### 一句话总结

`QDomText` 是 XML 元素中的普通文字节点。用 `QDomDocument::createTextNode()` 创建它，用 `QDomCharacterData` API 改内容；只有需要把一个节点变成两个相邻节点时，才调用会改变树结构的 `splitText()`。
