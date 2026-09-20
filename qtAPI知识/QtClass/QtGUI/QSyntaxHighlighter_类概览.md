# Qt QSyntaxHighlighter：按文本块增量着色的语法高亮基类

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSyntaxHighlighter>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QObject`  
> 类型定位：绑定到 `QTextDocument` 的抽象语法高亮控制器

## 1. 它解决什么问题

`QSyntaxHighlighter` 把“文档内容”和“编辑器显示样式”分开：文档仍然保存原始字符，语法高亮器则在排版前为每个文本块附加颜色、字体等显示格式。应用只需要实现 `highlightBlock(const QString &text)`，Qt 会在文档初次设置、文本发生变化或主动重高亮时调用它。

它适合：

- 在 `QTextEdit`、`QPlainTextEdit` 中显示 C++、Python、JSON、SQL 或日志；
- 根据关键字、数字、字符串、注释和错误范围提供即时视觉提示；
- 处理多行注释、多行字符串等需要跨块记忆的轻量语法；
- 文档持续编辑，只重新计算受影响区域的编辑器。

它不是编译器，也不是文档变换器。它不会改变 `QTextDocument::toPlainText()` 的结果，不会替编辑器移动光标，也不负责语法树、代码补全、诊断和格式化。复杂语言应把耗时的词法或语法分析放到独立模块，再将分析结果映射到各块；不要在每次 `highlightBlock()` 调用中无条件扫描整个文档。

## 2. 最小实现

```cpp
#include <QRegularExpression>
#include <QSyntaxHighlighter>
#include <QTextCharFormat>

class JsonHighlighter final : public QSyntaxHighlighter
{
public:
    explicit JsonHighlighter(QTextDocument *document)
        : QSyntaxHighlighter(document)
    {
        keyFormat.setForeground(Qt::darkBlue);
        stringFormat.setForeground(Qt::darkGreen);
        commentFormat.setForeground(Qt::gray);
    }

protected:
    void highlightBlock(const QString &text) override
    {
        const QRegularExpression keyExpression(
            QStringLiteral("\"[^\\\"]+\"(?=\\s*:)"));
        for (auto it = keyExpression.globalMatch(text); it.hasNext();) {
            const QRegularExpressionMatch match = it.next();
            setFormat(match.capturedStart(), match.capturedLength(), keyFormat);
        }

        const QRegularExpression stringExpression(
            QStringLiteral("\"(?:\\\\.|[^\\\"])*\""));
        for (auto it = stringExpression.globalMatch(text); it.hasNext();) {
            const QRegularExpressionMatch match = it.next();
            setFormat(match.capturedStart(), match.capturedLength(), stringFormat);
        }
    }

private:
    QTextCharFormat keyFormat;
    QTextCharFormat stringFormat;
    QTextCharFormat commentFormat;
};
```

把 `QTextDocument *` 传给构造函数后，高亮器立即绑定到该文档。也可以先用 `QObject *` 构造，再用 `setDocument()` 绑定或更换文档。

## 3. 一次回调处理什么

`highlightBlock()` 每次只收到一个 `QTextBlock` 的文本，不会自动提供整个文档。`text` 是该块的字符串，索引和长度使用 Qt 字符串的 UTF-16 code unit 偏移，不是字节偏移，也不是 Unicode code point 数量。

高亮回调期间，下面几个保护成员都针对“当前正在处理的块”：

- `currentBlock()` 返回当前 `QTextBlock`；
- `format(pos)` 查询当前块某个位置的已有高亮格式；
- `previousBlockState()` 读取上一块留下的整数状态；
- `currentBlockState()` 读取当前块已经设置的状态；
- `setCurrentBlockState()` 为后续块保存整数状态；
- `currentBlockUserData()` 读取当前块附加的数据；
- `setCurrentBlockUserData()` 替当前块附加用户数据。

这些函数的“当前块”语境只在高亮回调期间有明确意义。不要把一次回调中的块位置、状态或用户数据假定为之后永远不变；文档编辑可能重排块，Qt 也可能稍后重新调用高亮器。

## 4. `setFormat()` 只改变高亮显示

```cpp
setFormat(start, count, QTextCharFormat());
setFormat(start, count, QColor(Qt::red));
setFormat(start, count, QFontDatabase::systemFont(QFontDatabase::FixedFont));
```

三个重载分别接收 `QTextCharFormat`、`QColor` 和 `QFont`，后两个是便捷写法。它们写入的是高亮器维护的块格式，不是通过 `QTextCursor` 修改文档字符格式的编辑操作，因此不会改变文本内容、撤销栈或 `toHtml()` 中由用户编辑得到的文档语义。

范围应由当前 `text` 产生，并且要正确处理空匹配、负索引和长度边界。多个规则作用于相同位置时，后设置的属性可能覆盖先设置的属性，所以通常先应用较宽的基础规则，再应用需要覆盖它的更具体规则。使用空的 `QTextCharFormat` 可以清除该段高亮器格式，但不能把它当作清除文档全部字符格式的接口。

`format(pos)` 适合在规则需要保留或检查现有高亮时使用。`pos` 是当前块内的位置；它不是整个文档的绝对位置，也不能在没有当前块的普通成员函数中随意调用。

## 5. 用块状态处理多行结构

关键字和单行注释可以只看当前块；多行注释、三引号字符串和跨行转义则需要保存状态：

```cpp
void highlightBlock(const QString &text) override
{
    const QString begin = QStringLiteral("/*");
    const QString end = QStringLiteral("*/");
    int state = previousBlockState() == 1 ? 1 : 0;
    int start = 0;

    while (true) {
        if (state == 0) {
            start = text.indexOf(begin, start);
            if (start < 0)
                break;

            const int close = text.indexOf(end, start + begin.size());
            if (close < 0) {
                setFormat(start, text.size() - start, commentFormat);
                setCurrentBlockState(1);
                return;
            }

            setFormat(start, close + end.size() - start, commentFormat);
            start = close + end.size();
        } else {
            const int close = text.indexOf(end);
            if (close < 0) {
                setFormat(0, text.size(), commentFormat);
                setCurrentBlockState(1);
                return;
            }

            setFormat(0, close + end.size(), commentFormat);
            state = 0;
            start = close + end.size();
        }
    }

    setCurrentBlockState(state);
}
```

`previousBlockState()` 在前一块没有状态时返回 `-1`。应用可以约定 `0` 表示普通状态、`1` 表示处于多行注释等，但这只是应用自己的编码；Qt 不会解释整数含义。每个块结束时应明确设置状态，避免旧状态被错误地延续。

块状态只适合保存小型、可复制的解析状态。不要把大对象、指针图或整个文档的解析结果编码进整数；需要更丰富的块级数据时使用 `QTextBlockUserData`。

## 6. 文档绑定与重高亮

### `setDocument(QTextDocument *doc)`

把高亮器从当前文档解绑并绑定到 `doc`。传入 `nullptr` 表示解绑。绑定关系是高亮器监听文档变化并为其块提供显示格式，不等于把文档的所有权无条件转移给高亮器。

如果构造时使用 `QTextDocument *`，它同时作为 `QObject` 父对象参与对象树管理。高亮器销毁时不会因此把一个并非其子对象的文档强行删除；文档自身的父对象和生命周期仍应由应用设计负责。

更换文档后，后续 `highlightBlock()` 会针对新文档调用。不要在高亮回调中同步销毁当前文档或当前高亮器，也不要从工作线程修改 GUI 线程正在使用的文档。

### `rehighlight()`

请求整个文档重新高亮。适合主题、关键字表、字体颜色或语言模式整体变化的场景。它可能触发大量块处理，不应在每个按键事件后无条件调用，除非文档很小或确实需要全量刷新。

### `rehighlightBlock(const QTextBlock &block)`

只请求指定块重新高亮。传入的块应属于当前绑定文档且 `isValid()` 为 `true`。无效块、来自其他文档的块或已经失效的临时块不应作为有效目标。跨块语义变化时，单独重高亮一个块可能不够，应用应根据状态依赖范围继续处理后续块，或者直接调用 `rehighlight()`。

Qt 会在文档变化时自动安排必要的块重排和重高亮。高亮器的实现应尽量保持确定性和局部性，避免正则表达式在长文本上产生灾难性回溯。

## 7. 块用户数据的所有权

```cpp
class BlockInfo : public QTextBlockUserData
{
public:
    QString foldingLabel;
    bool hasError = false;
};

void highlightBlock(const QString &text) override
{
    auto *info = new BlockInfo;
    info->hasError = text.contains(QStringLiteral("TODO"));
    setCurrentBlockUserData(info);
}
```

`setCurrentBlockUserData()` 把指针交给当前文本块和文档体系管理。新的数据替换旧数据时，旧对象会按 Qt 的块数据生命周期被释放；应用不应在设置后继续手动 `delete`，也不应把同一个指针同时交给多个块。若只是保存很小的状态，整数块状态通常更便宜。

`currentBlockUserData()` 返回当前块数据指针，可能为 `nullptr`。它只在当前块回调语境下有意义，读出的指针也不应跨越文档重写、块销毁或文档线程边界长期保存。

## 8. 性能和线程边界

- `highlightBlock()` 应尽量只扫描当前块，避免每次调用从文档开头重新解析；
- 预先编译并复用 `QRegularExpression`，不要在每个匹配位置重复构造表达式；
- 规则数量很多时，按语言模式或可见范围裁剪工作；
- `rehighlight()` 是全量操作，主题切换时可以接受，但不应作为普通输入路径；
- GUI 文档和高亮器通常属于 GUI 线程，不能让工作线程同时修改或绘制同一份文档；
- 后台线程可以生成不可变的分析结果，回到文档所属线程后再调用重高亮或更新块数据。

语法高亮与布局不是编译器诊断的替代品。高亮规则应允许不完整输入，例如用户正在输入未闭合字符串时，应当给出稳定的中间状态，而不是依赖完整语法才能显示任何颜色。

## 9. 常见误区

### 9.1 以为高亮会修改文本

`setFormat()` 只影响显示格式。需要修改文本必须使用 `QTextCursor` 或文档编辑 API。

### 9.2 把块内索引当成文档绝对位置

`highlightBlock()` 的 `text` 只对应当前块，正则匹配得到的起点和长度只能直接传给当前块的 `setFormat()`。需要文档绝对位置时，要结合 `currentBlock().position()`，但不要把绝对位置直接传给 `setFormat()`。

### 9.3 忘记在多行结构结束后清除状态

如果结束分隔符被找到，应在当前块结束前把状态设置回普通状态，否则后面的块会一直按注释或字符串处理。

### 9.4 在回调中保存裸的当前块指针

`QTextBlock` 是轻量值对象，但它所代表的块仍可能因文档编辑而失效。需要长期追踪时，应根据应用逻辑重新定位，或使用受控的文档位置和版本信息。

### 9.5 每次输入都调用全量 `rehighlight()`

文档较大时会造成输入延迟。优先依赖 Qt 的增量处理，只有全局规则真的变化时才全量重高亮。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QSyntaxHighlighter(QObject *parent)` | 创建未绑定文档的高亮器 | `parent` 只负责 QObject 生命周期 |
| 构造 | `QSyntaxHighlighter(QTextDocument *parent)` | 创建并绑定到文档 | 文档同时作为 QObject 父对象 |
| 析构 | `~QSyntaxHighlighter()` | 销毁高亮器 | 不应在回调中销毁自身 |
| 绑定 | `setDocument(QTextDocument *doc)` | 绑定、更换或解绑文档 | `nullptr` 表示解绑；不等于任意所有权转移 |
| 查询 | `document() const` | 返回当前文档 | 未绑定时返回 `nullptr` |
| 槽 | `rehighlight()` | 全文重新高亮 | 可能处理大量块 |
| 槽 | `rehighlightBlock(const QTextBlock &block)` | 重新高亮一个块 | 块必须有效且属于当前文档 |
| 虚函数 | `highlightBlock(const QString &text)` | 实现单块高亮逻辑 | 抽象接口；参数是当前块文本 |
| 格式 | `setFormat(int, int, const QTextCharFormat &)` | 设置范围格式 | 索引和长度是当前块内 UTF-16 偏移 |
| 格式 | `setFormat(int, int, const QColor &)` | 便捷设置前景色格式 | 只改变高亮显示 |
| 格式 | `setFormat(int, int, const QFont &)` | 便捷设置字体格式 | 不修改文档字符内容 |
| 查询 | `format(int pos) const` | 查询当前块位置的高亮格式 | 只在当前回调语境下有明确意义 |
| 状态 | `previousBlockState() const` | 读取上一块状态 | 无状态时返回 `-1` |
| 状态 | `currentBlockState() const` | 读取当前块状态 | 状态含义由应用定义 |
| 状态 | `setCurrentBlockState(int)` | 保存当前块状态 | 供后续块通过 `previousBlockState()` 读取 |
| 数据 | `setCurrentBlockUserData(QTextBlockUserData *)` | 保存当前块附加数据 | 指针交给文档块生命周期管理 |
| 数据 | `currentBlockUserData() const` | 读取当前块附加数据 | 可能为 `nullptr`，不可随意长期持有 |
| 块 | `currentBlock() const` | 获取正在处理的块 | 只对当前高亮回调有效 |

---

### 一句话总结

`QSyntaxHighlighter` 是绑定 `QTextDocument` 的逐块高亮框架：在 `highlightBlock()` 中用 `setFormat()` 标记当前块，用整数状态或块用户数据传递跨块信息；`rehighlight()` 负责全量刷新，`rehighlightBlock()` 负责局部刷新。它改变显示，不改变文档内容，性能关键在于局部、确定且可增量的规则实现。
