# QDomNodeList 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDomNodeList>`  
> 所属模块：`Qt6::Xml`  
> 继承：无

## 它解决什么问题

`QDomNodeList` 表示 DOM 查询得到的一组节点。常见来源有两个：

- `QDomNode::childNodes()`：当前节点的全部直接孩子；
- `QDomDocument::elementsByTagName()` 或 `QDomElement::elementsByTagName()`：按标签名查询得到的元素列表。

它解决的是“拿到一批 DOM 节点并逐个访问”的问题。它本身不负责创建、删除或重排节点；修改 DOM 树要回到 `QDomNode`、`QDomElement`、`QDomDocument` 的编辑 API。

最容易误会的一点是：`QDomNodeList` 是 live list。DOM 规范要求这类列表反映底层文档的变化，因此你改动文档树后，列表内容可能随之更新。它不是 `QVector<QDomNode>` 那样的固定快照。

## 典型使用

```cpp
#include <QDomDocument>
#include <QDomElement>
#include <QDomNodeList>

QDomDocument document;
document.setContent(R"(
    <layout>
        <item name="title"/>
        <item name="body"/>
    </layout>
)");

QDomNodeList items = document.documentElement().elementsByTagName("item");
for (int i = 0; i < items.length(); ++i) {
    QDomElement item = items.item(i).toElement();
    qDebug() << item.attribute("name");
}
```

如果你只想遍历直接子元素，而不是递归找后代元素，不要从 `elementsByTagName()` 拿列表；使用 `firstChildElement()` 加 `nextSiblingElement()` 更准确。

## live list 对代码的影响

因为列表会随底层文档更新，遍历时一边修改文档结构要格外小心。比如你正在按索引遍历一个 `elementsByTagName("item")` 列表，同时删除某些 `item` 节点，后续索引可能看到变化后的列表。

更稳妥的做法是先收集要处理的 `QDomNode` 句柄，或者从后往前处理，或者直接用节点兄弟链遍历并在每次修改前保存 `nextSibling()`。

```cpp
QVector<QDomNode> toRemove;
QDomNodeList items = root.elementsByTagName("item");
for (int i = 0; i < items.length(); ++i) {
    QDomNode item = items.item(i);
    if (item.toElement().attribute("obsolete") == "true")
        toRemove.append(item);
}

for (const QDomNode &item : toRemove)
    item.parentNode().removeChild(item);
```

## Qt 6.9 起的迭代器

Qt 6.9 起，`QDomNodeList` 提供 STL 风格只读迭代器，可以写 range-for。这里的“只读”指不能通过迭代器原地替换列表项，不代表返回的 `QDomNode` 不能改动其底层 DOM 节点。

```cpp
for (const QDomNode &node : items) {
    if (node.isElement())
        qDebug() << node.toElement().tagName();
}
```

需要兼容 Qt 6.8 或更早版本时，应使用 `length()` 和 `item(i)`。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成员类型 | `const_iterator` | Qt 6.9 起提供的只读双向迭代器。 | 不能通过迭代器原地修改列表结构；旧 Qt 版本没有该类型。 |
| 成员类型 | `const_reverse_iterator` | Qt 6.9 起提供的只读反向迭代器。 | 用于反向遍历；仍受 live list 特性影响。 |
| 成员类型 | `const_pointer` | 为 STL 兼容提供的只读指针类型。 | Qt 6.9 起可用，通常不需要直接使用。 |
| 成员类型 | `const_reference` | 为 STL 兼容提供的只读引用类型。 | 与 `reference` 类型相同，因为列表不支持可变迭代器。 |
| 成员类型 | `difference_type` | 为 STL 兼容提供的距离类型。 | 主要供泛型算法使用。 |
| 成员类型 | `pointer` | 为 STL 兼容提供的指针类型。 | 与 `const_pointer` 相同，因为没有可变迭代器。 |
| 成员类型 | `reference` | 为 STL 兼容提供的引用类型。 | 与 `const_reference` 相同。 |
| 成员类型 | `value_type` | 表示列表元素类型。 | 元素是 `QDomNode`。 |
| 构造 | `QDomNodeList()` | 创建空节点列表。 | 空列表常用于占位；真实列表通常由 DOM 查询返回。 |
| 构造 | `QDomNodeList(const QDomNodeList &nodeList)` | 复制节点列表句柄。 | 复制的列表仍指向同一查询结果语义，不是节点快照。 |
| 析构 | `~QDomNodeList()` | 销毁列表句柄。 | 不删除 DOM 节点。 |
| 索引访问 | `at(int index) const` | 返回指定位置节点。 | 等价于 `item(index)`；负数或越界返回空节点。 |
| 迭代 | `begin() const` | 返回正向遍历起点。 | Qt 6.9 起可用；列表没有可变迭代器。 |
| 迭代 | `end() const` | 返回正向遍历终点后一位。 | 与 `begin()` 配对使用。 |
| 迭代 | `rbegin() const` | 返回反向遍历起点。 | Qt 6.9 起可用。 |
| 迭代 | `rend() const` | 返回反向遍历终点后一位。 | 与 `rbegin()` 配对使用。 |
| 迭代 | `cbegin() const` | 返回只读正向遍历起点。 | Qt 6.9 起可用，语义同 `begin()`。 |
| 迭代 | `cend() const` | 返回只读正向遍历终点后一位。 | Qt 6.9 起可用。 |
| 迭代 | `crbegin() const` | 返回只读反向遍历起点。 | Qt 6.9 起可用。 |
| 迭代 | `crend() const` | 返回只读反向遍历终点后一位。 | Qt 6.9 起可用。 |
| 迭代 | `constBegin() const` | Qt 容器风格的只读起点。 | Qt 6.9 起可用；等价于 `cbegin()`。 |
| 迭代 | `constEnd() const` | Qt 容器风格的只读终点后一位。 | Qt 6.9 起可用；等价于 `cend()`。 |
| 计数 | `count() const` | 返回节点数量。 | 等价于 `length()`。 |
| 状态 | `isEmpty() const` | 判断列表是否为空。 | 等价于 `length() == 0`。 |
| 索引访问 | `item(int index) const` | 返回指定索引的节点。 | 负数或越界返回空节点，调用具体 API 前检查 `isNull()` 或类型。 |
| 计数 | `length() const` | 返回列表中的节点数量。 | 对 live list 来说，文档修改后数量可能变化。 |
| 计数 | `size() const` | 返回节点数量。 | 等价于 `length()`，更贴近 Qt 容器命名。 |
| 赋值 | `operator=(const QDomNodeList &other)` | 让当前列表句柄指向另一个列表。 | 不复制节点内容。 |
| 非成员比较 | `operator!=(const QDomNodeList &lhs, const QDomNodeList &rhs)` | 判断两个列表是否不相等。 | 不要用它表达“两个 XML 子树内容不同”的业务判断。 |
| 非成员比较 | `operator==(const QDomNodeList &lhs, const QDomNodeList &rhs)` | 判断两个列表是否相等。 | 比较列表对象语义，不是深度比较每个节点的 XML。 |

## 易错点

1. `QDomNodeList` 是 live list，不是固定数组快照。遍历时修改文档结构，要先想清楚索引变化。
2. `item(i)` 返回的是节点句柄，不是节点副本；修改它可能改到文档树。
3. `childNodes()` 返回直接孩子，可能包含空白文本和注释；`elementsByTagName()` 是按名字递归查后代元素。
4. Qt 6.9 的迭代器只能只读遍历列表结构；要增删改树仍用 DOM 节点 API。

### 一句话总结

`QDomNodeList` 是 DOM 查询结果列表，适合逐个访问节点；它会随底层文档变化而更新，所以遍历和修改 DOM 时要把 live list 语义放在第一位。
