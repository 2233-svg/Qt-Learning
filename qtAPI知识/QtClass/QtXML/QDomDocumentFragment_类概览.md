# Qt QDomDocumentFragment 深入笔记：临时组装多个 DOM 子节点

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDomDocumentFragment>`  
> 所属模块：`Qt6::Xml`  
> 继承：`QDomNode -> QDomDocumentFragment`

`QDomDocumentFragment` 是 DOM 树操作时的临时容器。它可以先保存一批彼此有顺序的节点，等准备完成后一次性交给目标父节点插入。

它解决的不是“创建 XML 根文档”，而是“要替换或插入一段由多个 sibling 节点组成的内容，又不想在构造过程中反复改动正式树”的问题。

```text
fragment
├─ <item id="a"/>
├─ <item id="b"/>
└─ <!-- generated -->

parent.appendChild(fragment)
        |
        v
parent
├─ <item id="a"/>
├─ <item id="b"/>
└─ <!-- generated -->
```

fragment 本身不会成为 XML 中多出来的一层标签，也不会作为节点留在 parent 下。插入时，Qt 会把它的所有子节点逐一移到目标位置。

## 1. 为什么不用直接连续 `appendChild()`

直接追加当然可以：

```cpp
root.appendChild(document.createElement("item"));
root.appendChild(document.createElement("item"));
```

但当你需要先生成一组节点、检查它们、决定是追加还是替换既有区域，fragment 更清楚：

```cpp
QDomDocumentFragment fragment = document.createDocumentFragment();

for (const QString &name : names) {
    QDomElement item = document.createElement("item");
    item.setAttribute("name", name);
    fragment.appendChild(item);
}

root.appendChild(fragment);
```

代码把“组装新内容”和“提交到正式树”分为两个阶段。若构建过程中发现数据无效，只需丢弃 fragment，不会留下半组装的 child。

## 2. 插入的实际行为：展开并清空

`QDomDocumentFragment` 对四个继承的树操作有特殊规则：

- `appendChild(fragment)`
- `insertBefore(fragment, refChild)`
- `insertAfter(fragment, refChild)`
- `replaceChild(fragment, oldChild)`

Qt 不会插入 fragment 本身，而是把 fragment 的每个 child 移到目标节点。移动完成后，fragment 不再拥有那些 child，因此它会变空。

```cpp
QDomDocumentFragment fragment = document.createDocumentFragment();
fragment.appendChild(document.createElement("first"));
fragment.appendChild(document.createElement("second"));

root.appendChild(fragment);

Q_ASSERT(fragment.firstChild().isNull());
```

不要在插入后还期待从 fragment 继续访问刚才的子节点；应该保留各个节点的句柄，或从新 parent 重新遍历。

## 3. fragment 不必是完整 XML 文档

完整 XML 文档通常只能有一个根 element；fragment 则可以保存多个元素、文本、注释的任意组合，它自身不要求成为可独立序列化的合法 XML 文档。

这使它特别适合：

- 批量插入多条配置项。
- 将占位节点替换为多节点展开内容。
- 先构建一段混合的文字、元素与注释，再一次性放入目标 element。
- 在复杂树修改中暂存刚移除或尚未提交的节点集合。

它不适合拿来替代 `QDomDocument`：没有 document 的工厂方法，就无法正确创建属于同一 DOM 文档的新 element、text 和 comment 节点。

## 4. 创建和复制

用 `QDomDocument::createDocumentFragment()` 创建可用 fragment。默认构造只生成空句柄，不能当作一个已经属于文档的容器来可靠操作。

```cpp
QDomDocumentFragment fragment = document.createDocumentFragment();
```

复制构造和赋值都是浅拷贝，多个 `QDomDocumentFragment` 句柄可指向同一底层 fragment。要做独立副本，使用 `cloneNode()` 深复制。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDomDocumentFragment()` | 创建空 fragment 句柄 | 实际使用应由 `QDomDocument::createDocumentFragment()` 创建，确保节点归属正确 |
| 构造 | `QDomDocumentFragment(const QDomDocumentFragment &documentFragment)` | 复制 fragment 句柄 | 浅拷贝；多个句柄会看到同一批 child 和后续变化 |
| 赋值 | `operator=(const QDomDocumentFragment &other)` | 让当前句柄引用另一个 fragment | 不会复制子树；需要独立内容时用 `cloneNode()` |
| 节点类型 | `nodeType() const` | 返回 `QDomNode::DocumentFragmentNode` | 遍历节点时可用 `isDocumentFragment()` 或该类型识别 |
| 继承：追加 | `appendChild(const QDomNode &newChild)` | 将节点追加到 fragment，或将 fragment 的子节点展开追加到目标节点 | 当参数是 fragment 时，插入的是它的 children，插入后源 fragment 会被清空 |
| 继承：前插 | `insertBefore(const QDomNode &newChild, const QDomNode &refChild)` | 在指定 child 前插入节点或一组 fragment children | `refChild` 必须是目标的直接 child；fragment 被展开而不是作为包装节点插入 |
| 继承：后插 | `insertAfter(const QDomNode &newChild, const QDomNode &refChild)` | 在指定 child 后插入节点或一组 fragment children | `refChild` 为空时等价于追加；插入 fragment 后不要继续从它取原 child |
| 继承：替换 | `replaceChild(const QDomNode &newChild, const QDomNode &oldChild)` | 用新节点或 fragment children 替换一个直接 child | fragment 可把一个节点替换成多个 sibling；保留返回的旧节点句柄以便需要时复用 |

---

### 一句话总结

`QDomDocumentFragment` 是“先组装、后提交”的 DOM 临时容器。它最重要的特性是插入时自动展开子节点并清空自身，因此适合批量插入和多节点替换，不适合被当作 XML 里真实存在的包装节点。
