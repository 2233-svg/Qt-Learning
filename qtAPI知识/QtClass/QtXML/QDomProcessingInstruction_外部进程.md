# QDomProcessingInstruction 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDomProcessingInstruction>`  
> 所属模块：`Qt6::Xml`  
> 继承：`QDomNode`

## 它解决什么问题

`QDomProcessingInstruction` 表示 XML 里的处理指令节点，也就是 `<?target data?>` 这种结构。它用来在 XML 文档中保存给特定处理器看的指令信息，例如：

```xml
<?xml-stylesheet type="text/xsl" href="style.xsl"?>
```

这里 `xml-stylesheet` 是 target，`type="text/xsl" href="style.xsl"` 是 data。处理指令不是元素、不是注释，也不是外部进程管理 API；它只是 DOM 树中的一种节点。

常见用途包括：

- 在 XML 前部保留样式表关联；
- 读写某些旧系统或行业格式要求的处理指令；
- 在不改变元素结构的情况下携带处理器专用元信息。

多数业务 XML 不需要处理指令。只有当格式规范明确要求，或者你要完整保留第三方 XML 文档内容时，才会遇到它。

## 创建与读取

处理指令通常由 `QDomDocument::createProcessingInstruction()` 创建，或者由 `QDomDocument::setContent()` 解析出来。默认构造得到的是空处理指令，不能代表实际的 `<?...?>` 内容。

```cpp
#include <QDomDocument>
#include <QDomProcessingInstruction>

QDomDocument document;

QDomProcessingInstruction style =
    document.createProcessingInstruction(
        "xml-stylesheet",
        "type=\"text/xsl\" href=\"style.xsl\"");

document.appendChild(style);

qDebug() << style.target(); // xml-stylesheet
qDebug() << style.data();   // type="text/xsl" href="style.xsl"
```

如果你从通用节点遍历中遇到处理指令，先用 `isProcessingInstruction()` 判断，再用 `toProcessingInstruction()` 进入本类 API。

```cpp
for (QDomNode node = document.firstChild(); !node.isNull(); node = node.nextSibling()) {
    if (!node.isProcessingInstruction())
        continue;

    QDomProcessingInstruction pi = node.toProcessingInstruction();
    qDebug() << pi.target() << pi.data();
}
```

## target 和 data 的区别

`target()` 是处理指令的目标名，决定“这条指令给谁看”。创建后通过本类没有 setter 修改 target；如果要改 target，通常重新创建一个处理指令节点再替换。

`data()` 是 target 后面的文本内容，可以用 `setData()` 修改。Qt 不会把 data 自动解析成属性键值对，也不会验证它是否符合某个处理器的语法规则。对 `xml-stylesheet` 来说，`type="..." href="..."` 只是字符串；如果你的业务需要解析它，应自行按对应规范处理。

## 与 XML 声明的关系

XML 声明 `<?xml version="1.0" encoding="UTF-8"?>` 在概念上不是普通处理指令。Qt 的 `QDomNode::save()` 为了兼容历史行为，会在序列化文档节点时把名为 `xml` 的处理指令当作声明看待。写新代码时，不要把任意处理指令都当 XML 声明，也不要用处理指令替代正常的元素数据建模。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDomProcessingInstruction()` | 构造空处理指令节点。 | 要创建真实节点，用 `QDomDocument::createProcessingInstruction()`。 |
| 构造 | `QDomProcessingInstruction(const QDomProcessingInstruction &processingInstruction)` | 复制处理指令句柄。 | 浅复制，共享底层 DOM 数据；修改 data 会影响同一节点的其它句柄。 |
| 赋值 | `operator=(const QDomProcessingInstruction &other)` | 让当前句柄指向另一个处理指令。 | 不复制节点内容；需要独立节点时用 `cloneNode(true)`。 |
| 数据读取 | `data() const` | 返回处理指令 target 后面的文本内容。 | 返回的是原始字符串，Qt 不按属性语法解析。 |
| 类型识别 | `nodeType() const` | 返回 `QDomNode::ProcessingInstructionNode`。 | 在通用节点代码中也可用 `isProcessingInstruction()` 判断。 |
| 数据修改 | `setData(const QString &data)` | 修改处理指令的数据文本。 | 只改 data，不改 target；调用方负责保证内容对目标处理器有效。 |
| 目标读取 | `target() const` | 返回处理指令目标名。 | 本类没有 `setTarget()`；要改目标通常重新创建并替换节点。 |

## 易错点

1. 处理指令不是外部进程对象，也不会启动任何程序。它只是 XML 文本中的 `<?target data?>` 节点。
2. `data()` 不等于 XML 属性集合。即使看起来像 `key="value"`，Qt 也只是把它当字符串。
3. 复制 `QDomProcessingInstruction` 仍然共享同一个底层节点，`setData()` 会影响所有指向该节点的句柄。
4. XML 声明和普通处理指令概念不同；不要用处理指令承载本应属于元素和属性的业务数据。

### 一句话总结

`QDomProcessingInstruction` 用来读写 XML 处理指令：`target()` 确定指令交给哪个处理器，`data()` 保存指令正文，`setData()` 只能改正文而不改变目标。
