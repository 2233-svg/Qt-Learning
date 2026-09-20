# Qt QTextBlock：访问 QTextDocument 段落块的轻量句柄

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextBlock>`  
> 所属模块：`Qt6::Gui`  
> 继承：无  
> 类型定位：`QTextDocument` 内一个段落块（paragraph block）的值语义访问对象

## 1. 它解决什么问题

`QTextDocument` 不是一条没有结构的长字符串。它由一系列文本块组成，每个块通常对应一个段落，块内部又可以有多个 `QTextFragment` 和多个布局行。`QTextBlock` 就是访问其中一个段落块的轻量句柄。

它适合：

- 按段落遍历文档，而不是每次从头扫描整段字符串；
- 在代码编辑器中读取当前行文本、行号、折叠状态和语法高亮数据；
- 根据块位置创建 `QTextCursor`，执行段落级编辑；
- 查询段落格式、字符格式、文本布局和软换行结果；
- 在 `QSyntaxHighlighter`、自定义文档布局或导出工具中定位块；
- 为块附加折叠信息、诊断结果、解析缓存等 `QTextBlockUserData`。

它不是独立拥有文本的字符串对象，也不是一个可直接编辑内容的模型。`QTextBlock` 保存的是指向文档内部结构的轻量引用；真正修改文本要使用 `QTextCursor` 或 `QTextDocument` 的编辑接口。块会随着文档插入、删除和重排而变化，因此不能把 `position()` 当成永远稳定的 ID。

## 2. 最小用法：按块读取文档

```cpp
#include <QTextBlock>
#include <QTextDocument>

void dumpDocument(const QTextDocument *document)
{
    for (QTextBlock block = document->begin();
         block.isValid();
         block = block.next()) {
        qDebug() << block.blockNumber()
                 << block.position()
                 << block.length()
                 << block.text();
    }
}
```

在实际代码中，`begin()`、`end()`、`next()` 和 `previous()` 都以文档的块结构为边界。`end()` 是一个无效的结束哨兵，不应对它调用 `text()`、`position()`、`layout()` 等需要有效块的函数。

也可以从光标获取当前块：

```cpp
const QTextBlock block = cursor.block();
if (!block.isValid())
    return;

const int offsetInBlock = cursor.position() - block.position();
const QString line = block.text();
```

这里的 `cursor.position()` 是文档绝对位置，`offsetInBlock` 才是相对于当前块的偏移。二者不能直接混用。

## 3. 块、文本和段落分隔符

### `position()`

返回块在文档中的绝对起始位置，单位是 `QString` 使用的 UTF-16 code unit。文档首块通常从位置 `0` 开始，但应用不应只用“第几个字节”理解它。

位置是文档当前状态下的坐标。插入或删除前面的字符后，后续块的位置可能全部改变；如果要长期追踪语义对象，应使用光标、块用户数据、外部模型 ID 或重新定位策略，而不是只保存一个整数。

### `length()`

返回块占用的字符数量，包含块末尾的段落分隔符。这个边界是 `QTextBlock` 和 `QTextDocument` 内部位置计算的重要原因：`text()` 返回的可见文本长度可能比 `length()` 少一个分隔符。

因此，下面两个概念不同：

```cpp
const int textCharacters = block.text().size();
const int documentCharacters = block.length();
Q_ASSERT(documentCharacters >= textCharacters);
```

空段落也有块结构和段落分隔符，不能仅凭 `text().isEmpty()` 认定块无效。

### `contains(int position)`

判断给定文档绝对位置是否落在当前块范围内。位置必须使用同一个文档的坐标体系；把另一个文档的局部索引传进来没有意义。边界位置是否属于块要按块的实际长度理解，编辑操作通常还要特别处理块末段落分隔符，因为它不是 `text()` 返回的普通字符。

### `text()`

返回当前块的文本，不包含块末尾的段落分隔符。它是一个 `QString` 值结果，修改返回值不会修改文档。

需要频繁访问大型文档时，要意识到 `text()` 会生成返回值，虽然 Qt 的隐式共享让复制通常很轻，但对每个块反复做复杂转换仍可能造成成本。若需要编辑，应直接使用光标范围，而不是把整块字符串取出后再猜测如何写回。

## 4. 有效性、比较和生命周期

### `isValid()`

用于判断这个句柄是否指向一个有效块。默认构造的 `QTextBlock`、文档遍历结束后的哨兵，以及文档或块结构已经失效后的句柄，都可能是无效的。

常规访问模式是先检查有效性：

```cpp
QTextBlock block = document->findBlock(position);
if (!block.isValid())
    return;

const QString text = block.text();
```

`isValid()` 只解决“能否访问当前块”这一层问题，并不保证块仍处于你之前保存的文档位置，也不保证它的布局已经完成。

### `operator==` 和 `operator!=`

相等比较判断两个 `QTextBlock` 是否指向同一文档内部块。两个默认构造的无效块通常可比较，但业务上不要把无效块当成一个真实段落。

块对象是轻量值类型，复制它不会复制一份段落文本：

```cpp
QTextBlock copy = block;
Q_ASSERT(copy == block);
```

复制句柄不会冻结块。原文档发生编辑后，两个句柄仍可能同时看到变化，或者一起失效。

### `operator<`

按块的文档位置进行排序。它适合在同一文档内按出现顺序比较；跨不同文档比较没有业务意义，即使实现层面可能返回一个结果，也不要将其作为跨文档排序规则。

## 5. 块遍历和片段遍历

### `next()` / `previous()`

`next()` 返回当前块之后的块，`previous()` 返回之前的块。到达文档边界后会得到无效块：

```cpp
for (QTextBlock block = document->begin();
     block.isValid();
     block = block.next()) {
    // 处理一个段落
}
```

遍历过程中不要在同一循环体内随意通过另一个对象修改文档结构。插入、删除段落会改变后续块的位置和有效性，若必须边遍历边编辑，应使用明确的 `QTextCursor` 策略并重新获取下一块。

### `begin()` / `end()`

这两个函数返回块内部 `QTextFragment` 的迭代器，不是文档块迭代器。`QTextBlock::begin()` 指向块的第一个片段，`end()` 是片段遍历结束位置。

```cpp
for (QTextBlock::iterator it = block.begin(); !it.atEnd(); ++it) {
    const QTextFragment fragment = it.fragment();
    if (!fragment.isValid())
        continue;

    qDebug() << fragment.position()
             << fragment.length()
             << fragment.text()
             << fragment.charFormat();
}
```

片段是连续文本和字符格式的组合。两个相邻文本片段可能因为字符格式不同而分开，即使它们在屏幕上看起来相同；不要把“一个片段”误认为“一个单词”或“一个语法 token”。

迭代器的 `atEnd()` 是推荐的结束判断。不要在结束迭代器上调用 `fragment()`。修改文档后，正在使用的片段迭代器可能失效，应用应重新获取块和迭代器。

## 6. 布局对象与显示几何

### `layout()`

返回负责该块文字排版的 `QTextLayout`。它描述字形、布局行、换行和绘制所需的信息，能回答“这个段落实际被分成几行”“某个位置对应哪一行”等布局问题。

但 `QTextBlock` 的文本数据和布局数据不是同一层：

- 文本改变后，布局可能需要重新生成；
- 文档尚未布局或块无效时，布局指针可能为空；
- 布局受字体、宽度、文档布局和设备条件影响；
- 自定义文档布局负责管理布局生命周期，应用不应擅自删除返回指针。

读取布局前要检查块有效性和指针：

```cpp
if (block.isValid()) {
    if (QTextLayout *layout = block.layout())
        qDebug() << layout->lineCount();
}
```

### `clearLayout()`

清除当前块的布局缓存。它不是删除文本，也不是把段落从文档中移除。通常由文档布局或需要强制重新布局的代码在确认后调用；普通业务代码不应把它当作“刷新文本”的通用按钮，因为清除后还需要合适的布局流程重新计算。

调用后，依赖旧 `QTextLayout` 的指针和布局行对象不能继续当作有效几何数据使用。清除布局也不会自动替应用完成自定义绘制或重排。

## 7. 段落格式、字符格式和高亮格式

### `blockFormat()` / `blockFormatIndex()`

`blockFormat()` 返回段落级 `QTextBlockFormat`，例如对齐、首行缩进、左右边距、段前段后间距和行距。它作用于整个块的段落布局，不是某个字符的颜色。

`blockFormatIndex()` 返回文档内部格式表索引。它适合低层比较、缓存或调试，不应把这个整数当作跨文档稳定 ID；文档编辑和格式合并可能改变内部索引。

### `charFormat()` / `charFormatIndex()`

`charFormat()` 返回块位置对应的字符格式，适合读取默认或起始字符的字符属性。一个块内部可以有多个格式不同的片段，因此不要把它误认为整块每个字符都拥有完全相同的格式。

`charFormatIndex()` 同样是文档内部格式表的索引，只适合在当前文档上下文中使用。若要逐段检查字符样式，应遍历 `QTextFragment`。

### `textFormats()`

返回当前块的格式范围列表，元素类型是 `QTextLayout::FormatRange`。它适合检查布局层面的格式覆盖，例如语法高亮器设置的范围：

```cpp
const QList<QTextLayout::FormatRange> ranges = block.textFormats();
for (const QTextLayout::FormatRange &range : ranges) {
    qDebug() << range.start << range.length << range.format;
}
```

这些范围中的 `start` 是块内偏移。它们是格式描述，不是文本编辑命令；修改返回的列表不会反向改写块。若需要持久化用户编辑格式，应使用 `QTextCursor` 和 `QTextCharFormat`。

## 8. 文本方向和文本列表

### `textDirection()`

返回块的布局方向。它用于判断该块按从左到右还是从右到左的方向排版，特别适合混合阿拉伯文、希伯来文、中文和拉丁文字的编辑器或导出工具。

文本方向不是“字符串是否全部是某种语言”的简单判断，也不是屏幕坐标的正负方向。最终字形排列还会受到 Unicode 双向算法、段落格式和布局器的影响。

### `textList()`

如果块属于某个 `QTextList`，返回对应列表对象；否则返回 `nullptr`。列表对象提供编号、项目符号和列表格式，块本身只表示其中一个列表项目的段落。

不要只检查文本前缀来判断列表编号，因为编号和项目符号通常是布局层生成的，不属于 `block.text()`：

```cpp
if (QTextList *list = block.textList()) {
    const int itemNumber = list->itemNumber(block);
    const QString label = list->itemText(block);
    qDebug() << itemNumber << label;
}
```

## 9. 块用户数据和状态

### `userData()` / `setUserData()`

块可以附加一个 `QTextBlockUserData *`，常见用途包括语法高亮缓存、代码折叠信息、诊断集合和文档分析版本号：

```cpp
class BlockMetadata final : public QTextBlockUserData
{
public:
    int syntaxVersion = 0;
    bool hasError = false;
};

auto *metadata = new BlockMetadata;
metadata->hasError = block.text().contains(QStringLiteral("TODO"));
block.setUserData(metadata);
```

设置后，数据的所有权交给块和文档生命周期管理。不要在 `setUserData()` 后再次手动删除，也不要把同一个裸指针交给多个块。替换旧数据时，旧数据会按照块数据的生命周期被清理。

用户数据指针不是线程安全的共享存储。若后台分析结果需要回到文档线程，应在正确的线程中更新块数据，并考虑用版本号丢弃过期结果。块删除后，数据对象也不应继续被外部持有。

### `userState()` / `setUserState()`

提供一个整数状态槽，默认未设置时通常以 `-1` 表示。它很适合保存小型状态机值，例如多行注释状态、解析阶段或折叠分类：

```cpp
const int state = block.userState();
block.setUserState(state == 1 ? 0 : 1);
```

状态的数值含义完全由应用定义。不要把指针强行转换成整数，也不要把大规模解析结果塞进一个槽位。`QSyntaxHighlighter` 的 `previousBlockState()` 与块用户状态处于同一类块级状态机制中，使用高亮器时应让高亮器负责设置状态，避免其他代码无意覆盖它。

## 10. 修订号、可见性和行号

### `revision()` / `setRevision()`

修订号是附着在块上的整数标记，适合让自定义布局或分析器记录“这个块对应哪个文本版本”。它不是由 Qt 自动替你维护的全局文档版本，也不是提交系统的 revision ID。

如果应用自己设置修订号，应定义清晰的版本来源和失效规则。文档修改后，旧分析结果可能仍保留在块上；仅比较一个未被可靠更新的 revision 不能证明数据是最新的。

### `isVisible()` / `setVisible()`

块可见性影响文档布局和显示。可见性可以用于代码折叠、隐藏辅助段落或自定义文档视图：

```cpp
block.setVisible(!collapsed);
document->markContentsDirty(block.position(), block.length());
```

改变可见性不会删除文本，也不会改变 `text()`、`position()` 或块编号。应用需要配合文档布局和视图刷新；若折叠状态只属于某一个视图，直接修改文档块可见性可能会影响所有共享该文档的视图，应先确认这是文档级还是视图级需求。

### `blockNumber()` / `firstLineNumber()`

`blockNumber()` 返回块在文档块序列中的编号，通常从 `0` 开始；无效块没有有意义的编号。块编号会因前面的段落插入、删除而变化，不能作为持久 ID。

`firstLineNumber()` 返回该块布局行中的第一行编号。一个块可能因自动换行占据多条布局行，因此块编号和视觉行号不是同一概念。尚未布局、布局被清除或自定义布局尚未更新时，行号信息可能暂时不适合用于屏幕定位。

### `setLineCount()` / `lineCount()`

保存和读取块的布局行数。软换行后，一个段落块可能有多行；这个值服务于文档布局和行号计算，不是 `text().count('\n')` 的结果，因为块本身通常已经以段落边界分开。

普通应用通常读取 `lineCount()`，而不直接维护它。若自定义布局确实需要调用 `setLineCount()`，应在每次宽度、字体、内容或布局规则变化后保持一致，否则 `firstLineNumber()` 和基于行数的滚动定位会变得不可靠。

## 11. 和 QTextCursor 的分工

`QTextBlock` 负责定位和读取，`QTextCursor` 负责编辑和选择。典型的段落级操作是从块起始位置构造光标：

```cpp
QTextCursor cursor(document);
cursor.setPosition(block.position());
cursor.movePosition(QTextCursor::EndOfBlock,
                    QTextCursor::KeepAnchor);
const QString selectedLine = cursor.selectedText();
```

块的 `length()` 包含段落分隔符，而 `EndOfBlock` 的选择语义由光标 API 定义；需要精确删除或替换段落时，应明确是否要连同段落边界一起操作，不要用 `block.text().size()` 盲目推导所有光标范围。

编辑完成后，原先保存的 `QTextBlock`、片段迭代器、布局指针和位置都应重新验证。文档是可变结构，读取句柄不是事务快照。

## 12. 性能、线程和共享文档

- `QTextBlock` 本身很小，按值传递通常比复制整段文本更合适；
- 轻量不等于独立副本，所有访问仍依赖关联文档；
- 不要让一个线程修改文档，另一个线程同时读取块或布局；
- 后台线程可以处理复制出的纯文本，但结果应回到文档所属线程应用；
- 频繁扫描文档时按块遍历，避免每个位置都从 `document->begin()` 重新查找；
- `layout()`、`textFormats()` 和行号信息可能需要文档布局完成后才有稳定意义；
- 文档共享给多个视图时，`setVisible()` 等块属性是共享文档状态，而非单个视图私有状态。

## 13. 常见误区

### 13.1 把 `text().size()` 当成块长度

`length()` 包含段落分隔符，而 `text()` 不包含它。进行绝对位置计算时应根据具体光标 API 的边界语义选择。

### 13.2 把块编号当作稳定 ID

在文档开头插入一个段落后，大量块编号都会改变。持久化对象应另设 ID 或重新定位。

### 13.3 直接修改 `charFormat()` 返回值

格式查询返回的是值，不是可写引用。要修改格式请使用 `QTextCursor::setCharFormat()` 或相应文档编辑 API。

### 13.4 把 `clearLayout()` 当作删除块

它只清理布局缓存。文本仍在，块也仍在。

### 13.5 在文档删除后继续使用块

块句柄不会替你延长文档寿命。文档销毁、结构改变或块删除后都要重新检查 `isValid()`。

### 13.6 认为一个块必然只对应一行

自动换行会让一个段落包含多个 `QTextLayout::FormatRange` 或布局行。块编号是段落编号，不是视觉行号。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QTextBlock()` | 创建无效块句柄 | 不能读取文本或位置 |
| 构造 | `QTextBlock(const QTextBlock &)` | 复制块句柄 | 不复制文本；仍依赖原文档 |
| 赋值 | `operator=(const QTextBlock &)` | 复制块句柄 | 目标指向同一内部块 |
| 有效性 | `isValid() const` | 判断块是否有效 | 不保证位置和布局长期不变 |
| 比较 | `operator==(const QTextBlock &) const` | 判断是否为同一文档块 | 无效块也可比较 |
| 比较 | `operator!=(const QTextBlock &) const` | 不等比较 | 不表示文本内容不同 |
| 排序 | `operator<(const QTextBlock &) const` | 按位置排序 | 只适合比较同一文档内的块 |
| 位置 | `position() const` | 获取文档绝对起始位置 | UTF-16 偏移；编辑后可能变化 |
| 尺寸 | `length() const` | 获取块占用长度 | 包含段落分隔符 |
| 范围 | `contains(int position) const` | 判断位置是否位于块范围 | 参数必须使用同一文档坐标 |
| 文本 | `text() const` | 获取块文本 | 不包含末尾段落分隔符；返回值 |
| 布局 | `layout() const` | 获取 `QTextLayout` | 可能为空；由布局系统管理 |
| 布局 | `clearLayout()` | 清除布局缓存 | 不删除文本；旧布局数据失效 |
| 段落格式 | `blockFormat() const` | 获取块级段落格式 | 影响对齐、缩进、边距等 |
| 格式索引 | `blockFormatIndex() const` | 获取内部块格式索引 | 不是跨文档稳定 ID |
| 字符格式 | `charFormat() const` | 获取块位置对应字符格式 | 不代表整块所有片段都相同 |
| 格式索引 | `charFormatIndex() const` | 获取内部字符格式索引 | 只在当前文档上下文有意义 |
| 范围 | `textFormats() const` | 获取布局格式范围列表 | `start` 是块内偏移；返回值 |
| 方向 | `textDirection() const` | 获取块布局方向 | 受双向文本和段落布局影响 |
| 文档 | `document() const` | 获取关联文档 | 文档可能为空或已失效 |
| 列表 | `textList() const` | 获取所属 `QTextList` | 不属于列表时返回 `nullptr` |
| 用户数据 | `userData() const` | 获取块附加数据 | 指针受块生命周期约束 |
| 用户数据 | `setUserData(QTextBlockUserData *)` | 设置块附加数据 | 所有权转交块；不要重复删除 |
| 状态 | `userState() const` | 获取整数块状态 | 未设置通常为 `-1`；含义由应用定义 |
| 状态 | `setUserState(int)` | 设置整数块状态 | 适合小型状态机，不适合存指针 |
| 版本 | `revision() const` | 获取块修订标记 | 不是自动可靠的全局版本 |
| 版本 | `setRevision(int)` | 设置块修订标记 | 应由应用定义更新规则 |
| 可见性 | `isVisible() const` | 查询块是否可见 | 隐藏不等于删除 |
| 可见性 | `setVisible(bool)` | 设置块可见性 | 可能影响共享文档的所有视图 |
| 编号 | `blockNumber() const` | 获取段落块编号 | 通常从 `0` 开始；编辑后会变化 |
| 行号 | `firstLineNumber() const` | 获取块首个布局行号 | 依赖布局状态；不等于块编号 |
| 行数 | `setLineCount(int)` | 设置布局行数记录 | 通常由自定义布局维护 |
| 行数 | `lineCount() const` | 获取布局行数 | 软换行后可大于一 |
| 片段迭代 | `begin() const` | 获取第一个 `QTextFragment` 迭代器 | 空块可能直接到末尾 |
| 片段迭代 | `end() const` | 获取片段结束迭代器 | 结束迭代器不能调用 `fragment()` |
| 片段后移 | `QTextBlock::iterator::operator++()` | 移到下一个片段 | 修改文档后迭代器可能失效 |
| 片段前移 | `QTextBlock::iterator::operator--()` | 移到上一个片段 | 不能越过有效范围使用 |
| 片段查询 | `QTextBlock::iterator::fragment() const` | 获取当前片段 | 结束位置不可调用 |
| 片段状态 | `QTextBlock::iterator::atEnd() const` | 判断是否到片段末尾 | 推荐的遍历终止条件 |
| 块后移 | `next() const` | 获取下一块 | 末尾返回无效块 |
| 块前移 | `previous() const` | 获取上一块 | 开头返回无效块 |
| 内部索引 | `fragmentIndex() const` | 获取内部片段索引 | 不是持久 token ID |

---

### 一句话总结

`QTextBlock` 是 `QTextDocument` 中一个段落的轻量访问句柄：用 `position()`、`length()` 和 `text()` 读取文档坐标与内容，用 `layout()`、格式和行号 API 连接排版，用 `userData()`、`userState()` 保存块级分析状态。它不拥有独立文本，文档编辑会改变位置、布局和有效性，真正的修改应交给 `QTextCursor`。
