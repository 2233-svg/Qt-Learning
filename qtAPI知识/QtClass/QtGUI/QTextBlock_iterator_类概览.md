# Qt QTextBlock::iterator：遍历段落内 QTextFragment 的迭代器

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextBlock>`  
> 所属模块：`Qt6::Gui`  
> 继承：无  
> 类型定位：访问一个 `QTextBlock` 内连续文本片段的轻量值类型迭代器

## 1. 它解决什么问题

一个 `QTextBlock` 是一个段落，但段落内部可能因为字体、颜色、链接、下划线、对象替换字符或语法高亮范围而被切成多个 `QTextFragment`。`QTextBlock::iterator` 提供顺序访问这些片段的方式，让应用可以在不手写文档内部位置扫描的情况下读取：

- 每个片段的文档位置和长度；
- 片段文本；
- 片段的 `QTextCharFormat`；
- 片段是否有效，以及片段之间的连续关系。

典型使用场景：

- 导出带字符格式的文档；
- 查找一个段落中不同字体或链接范围；
- 调试 `QTextCursor` 产生的格式分段；
- 在自定义绘制、索引和文本分析中按格式片段读取内容；
- 将 `QTextBlock` 内部结构映射成应用自己的 token 或运行（run）模型。

它不是通用 STL 随机访问迭代器，也不是文本编辑器的字符游标。它只在一个块的片段序列中前后移动，不提供按整数跳跃、解引用运算符或直接修改片段的接口。

## 2. 最小遍历

```cpp
#include <QTextBlock>
#include <QTextDocument>
#include <QTextFragment>

void inspectBlock(const QTextBlock &block)
{
    for (QTextBlock::iterator it = block.begin();
         !it.atEnd();
         ++it) {
        const QTextFragment fragment = it.fragment();
        if (!fragment.isValid())
            continue;

        qDebug() << fragment.position()
                 << fragment.length()
                 << fragment.text()
                 << fragment.charFormat();
    }
}
```

结束条件优先使用 `atEnd()`。只有在确认当前迭代器不是结束位置时，才调用 `fragment()`。空块可能没有有效片段，循环体可以一次都不进入。

`QTextBlock::Iterator` 是同一个类型的别名，在需要兼容 Qt 旧代码时可以使用；新代码通常直接写 `QTextBlock::iterator`，语义更清楚。

## 3. 迭代器指向什么

迭代器内部保存文档结构的轻量位置，不保存一份片段文本副本，也不拥有 `QTextDocument`。`fragment()` 返回一个 `QTextFragment` 值对象，值对象本身仍然依赖原文档内部数据。

一个片段通常代表一段连续字符格式相同的文本，但它不一定是：

- 一个单词；
- 一个 Unicode 图素；
- 一个语法 token；
- 一个屏幕布局行；
- 一个用户明确创建的独立对象。

文档格式范围改变后，相邻片段可能合并或拆分。相同视觉效果也不保证内部一定是同一个片段，反过来，同一个片段也可能包含多个语义 token。

## 4. `begin()` 与 `end()`

### `QTextBlock::begin()`

返回指向当前块第一个片段的迭代器。如果块没有有效片段，返回值可能已经等于 `end()`。

它返回的是当前文档状态下的起点。不要在迭代器创建后修改文档，再假定它仍自动指向原来的片段。

### `QTextBlock::end()`

返回片段序列的结束迭代器。它是哨兵，不代表一个可读取的片段：

```cpp
QTextBlock::iterator it = block.end();
Q_ASSERT(it.atEnd());
// 不要在这里调用 it.fragment()
```

在反向遍历时，只有当序列非空且已经先递减到有效元素时，才能读取片段。对空序列直接执行 `--end()` 不应作为通用安全写法。

## 5. `atEnd()` 与比较

### `atEnd()`

返回迭代器是否到达当前块片段序列末尾。它等价于“当前内部片段位置已经等于结束位置”的查询，是正向遍历最直接的终止条件。

`atEnd()` 不表示原文档已经结束，也不表示当前 `QTextBlock` 无效；它只描述这个迭代器在其所属片段范围内的位置。

### `operator==` / `operator!=`

比较两个迭代器是否位于相同的文档内部位置。可靠比较通常要求它们来自同一个块的 `begin()` / `end()` 序列。不要用来自不同文档的迭代器做业务上的顺序比较，也不要把“文本相等”与“迭代器相等”混为一谈。

迭代器没有 `operator<`，因为它不是为通用排序或随机访问设计的。需要按文本顺序处理时，沿着 `++` 或 `--` 遍历即可。

## 6. `fragment()` 的语义

`fragment()` 返回当前迭代位置的 `QTextFragment`。在有效位置上，它可以用于读取：

```cpp
const QTextFragment fragment = it.fragment();
const int documentStart = fragment.position();
const int length = fragment.length();
const QString text = fragment.text();
const QTextCharFormat format = fragment.charFormat();
```

片段位置是文档绝对位置，片段长度同样使用 Qt 字符串的 UTF-16 code unit。若要得到相对于块的偏移，应使用：

```cpp
const int offsetInBlock = fragment.position() - block.position();
```

`fragment()` 返回值不是可写引用。修改字符格式或文本必须通过 `QTextCursor`，例如选择片段的文档范围后调用 `setCharFormat()` 或 `insertText()`。

当迭代器处于 `end()`、所属块已经失效或文档被修改导致迭代器不再可用时，不应继续读取片段。即使返回了一个默认或无效的 `QTextFragment`，也不应依赖这种状态继续处理。

## 7. 前置和后置递增

### `operator++()`

前置递增把迭代器移动到下一个片段，并返回移动后的迭代器引用：

```cpp
++it;
```

正向遍历中，只有当前迭代器仍在有效范围内时才递增。对结束迭代器继续递增不属于正常使用路径。

### `operator++(int)`

后置递增先返回递增前的副本，再把迭代器移动到下一个片段：

```cpp
const QTextBlock::iterator old = it++;
```

如果不需要旧值，前置递增通常更直接，也避免产生额外的临时值。两者都不会复制片段文本。

## 8. 前置和后置递减

### `operator--()`

前置递减把迭代器移动到前一个片段，并返回移动后的引用。它适合从一个有效片段向前检查格式连续性，或从有效的结束位置开始反向遍历非空序列。

### `operator--(int)`

后置递减返回递减前的副本，再移动到前一个片段：

```cpp
const QTextBlock::iterator old = it--;
```

和递增一样，后置形式只在确实需要旧位置时使用。越过 `begin()`、对默认构造迭代器递减或在文档修改后继续递减都不是可依赖的业务行为。

## 9. 片段遍历和字符格式的关系

片段边界主要由字符格式和文档内部结构决定。例如：

```cpp
QTextCursor cursor(document);
cursor.insertText(QStringLiteral("普通 "));

QTextCharFormat emphasis;
emphasis.setFontWeight(QFont::Bold);
cursor.setCharFormat(emphasis);
cursor.insertText(QStringLiteral("加粗"));
```

随后遍历块，通常能看到至少两个格式不同的片段。但应用不能依靠片段数量来判断编辑操作次数，也不能假定每次设置格式都会产生一个新的片段；文档会合并可合并的相邻格式范围。

语法高亮器产生的临时格式范围也可能参与布局格式读取，但“文档字符格式片段”和“`QSyntaxHighlighter` 的块格式”不应简单视为同一持久数据层。需要区分用户编辑样式、块格式和布局高亮范围时，应同时参考 `QTextBlock::textFormats()`、`QTextFragment::charFormat()` 和具体视图行为。

## 10. 文档修改后的失效边界

迭代器不是稳定快照。下列操作都可能让它失效或改变其指向：

- 插入、删除或替换当前块内文本；
- 修改导致片段重新分割的字符格式；
- 删除当前块或合并相邻块；
- 销毁关联的 `QTextDocument`；
- 在其他线程并发修改文档。

安全做法是把片段需要的值复制出来，再进行可能改变文档的操作：

```cpp
const QTextFragment fragment = it.fragment();
const int start = fragment.position();
const int length = fragment.length();
const QString text = fragment.text();

// 之后再进行编辑，并重新获取 block.begin()。
```

即便保存了 `QTextFragment` 值，也不能把它当作永久稳定对象；它仍然依赖文档生命周期和当前文档结构。

## 11. 与 QTextCursor 的分工

`QTextBlock::iterator` 适合读取片段；`QTextCursor` 适合按文档位置选择和修改：

```cpp
QTextCursor cursor(document);
cursor.setPosition(fragment.position());
cursor.setPosition(fragment.position() + fragment.length(),
                   QTextCursor::KeepAnchor);
cursor.setCharFormat(newFormat);
```

这段代码把片段范围作为编辑起点，但编辑完成后旧迭代器和旧片段边界可能不再适用。若要处理整块多个片段，通常先收集需要修改的绝对区间，再从后往前编辑，减少前面编辑造成的位置偏移。

## 12. 性能和线程边界

- 迭代器本身很轻，按值复制通常成本很小；
- `fragment().text()` 返回值可能共享字符串数据，但大量转换或持久保存仍会产生成本；
- 不要在每个片段上重新从文档开头查找相同块；
- 需要构建索引时，把片段的必要字段复制到应用数据结构中；
- `QTextDocument`、块、片段和迭代器应在文档所属线程访问；
- 后台分析应使用复制出的字符串和格式值，完成后在正确线程更新文档；
- 修改文档后重新获取迭代器，不要尝试修补旧迭代器。

该迭代器没有并发保护，也没有失效通知。应用必须自己安排读写时序。

## 13. 常见误区

### 13.1 把 `QTextBlock::iterator` 当作字符迭代器

它一次移动一个 `QTextFragment`，不是一次移动一个字符。片段内部仍可能包含很长文本。

### 13.2 在 `end()` 上调用 `fragment()`

`end()` 是哨兵。先检查 `atEnd()`，再读取当前片段。

### 13.3 认为片段等于语法 token

片段边界由文档格式和内部结构决定。语法 token 需要应用自己的词法分析。

### 13.4 遍历时直接编辑文档

编辑可能拆分、合并片段并使迭代器失效。先收集范围，编辑后重新遍历。

### 13.5 跨文档比较迭代器

相等比较只适合相同文档和相同块的迭代序列。跨文档的比较结果没有业务含义。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `iterator()` | 构造默认迭代器 | 不指向有效片段；不能直接读取 |
| 起点 | `QTextBlock::begin() const` | 获取块内第一个片段迭代器 | 空块可能直接等于 `end()` |
| 终点 | `QTextBlock::end() const` | 获取块内结束哨兵 | 不代表有效片段；不能调用 `fragment()` |
| 查询 | `atEnd() const` | 判断是否到达片段末尾 | 只描述当前迭代范围，不是文档结束 |
| 读取 | `fragment() const` | 获取当前 `QTextFragment` | 先确认不在 `end()`；返回值依赖文档 |
| 比较 | `operator==(const iterator &) const` | 判断两个迭代器位置是否相同 | 通常应来自同一块、同一文档 |
| 比较 | `operator!=(const iterator &) const` | 判断两个迭代器位置不同 | 不表示片段文本内容不同 |
| 移动 | `operator++()` | 前置移动到下一个片段 | 不要越过结束位置 |
| 移动 | `operator++(int)` | 后置移动到下一个片段并返回旧副本 | 需要旧位置时使用 |
| 移动 | `operator--()` | 前置移动到上一个片段 | 不要越过起始位置 |
| 移动 | `operator--(int)` | 后置移动到上一个片段并返回旧副本 | 需要旧位置时使用 |
| 别名 | `QTextBlock::Iterator` | `iterator` 的兼容别名 | 新代码通常使用小写类型名 |
| 协作 | `QTextFragment::position()` | 获取片段文档绝对起点 | UTF-16 偏移；编辑后可能变化 |
| 协作 | `QTextFragment::length()` | 获取片段长度 | 不是字节数 |
| 协作 | `QTextFragment::text()` | 获取片段文本 | 返回值；不直接修改文档 |
| 协作 | `QTextFragment::charFormat()` | 获取片段字符格式 | 片段边界不等于语义 token |

---

### 一句话总结

`QTextBlock::iterator` 是段落内部的顺序读取工具：从 `begin()` 走到 `end()`，在有效位置调用 `fragment()` 获取每个 `QTextFragment`。它适合检查文本格式和构建索引，不负责编辑；任何文档修改都可能使迭代器失效，修改后应重新遍历。
