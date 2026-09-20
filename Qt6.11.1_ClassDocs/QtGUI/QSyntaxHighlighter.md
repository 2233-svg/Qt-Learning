# QSyntaxHighlighter
> Qt 6.11.1 · Qt GUI · 来自 `QSyntaxHighlighter`

## 1. 先建立直觉

`QSyntaxHighlighter` 是给 `QTextDocument` 做逐块文本高亮的基类。你继承它，实现 `highlightBlock(const QString &text)`，然后对当前文本块调用 `setFormat()` 标记不同范围的颜色、字体或格式。

它不负责编辑器 UI，也不负责解析整份文档；它的工作单位是 `QTextBlock`，通常是一段或一行。

## 2. 类说明

- 头文件：`#include <QSyntaxHighlighter>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QObject`
- 目标对象：`QTextDocument`
- 协作类：`QTextBlock`、`QTextCharFormat`、`QTextBlockUserData`、`QTextEdit`/`QPlainTextEdit`

构造时传 `QTextDocument *` 会安装到该文档；也可以之后用 `setDocument()` 切换。一个 highlighter 同一时间只能服务一个 document。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `QSyntaxHighlighter(QTextDocument*)` | 创建并安装到文档 |
| `QSyntaxHighlighter(QObject*)` | 以 QObject 为 parent；如果 parent 是文本编辑器可安装到其文档 |
| `setDocument()` / `document()` | 切换或读取当前文档 |
| `rehighlight()` | 重新高亮整份文档 |
| `rehighlightBlock(block)` | 重新高亮单个块 |
| `highlightBlock(text)` | 子类必须实现的逐块高亮逻辑 |
| `setFormat(start, count, format/color/font)` | 给当前块指定范围设置格式 |
| `format(position)` | 读取当前块指定位置的格式 |
| `currentBlock()` | 当前正在处理的文本块 |
| `previousBlockState()` / `currentBlockState()` | 多行语法状态读取 |
| `setCurrentBlockState()` | 保存当前块结束状态 |
| `currentBlockUserData()` / `setCurrentBlockUserData()` | 给块绑定自定义缓存数据 |

## 4. 关键用法

简单关键字高亮：

```cpp
void Highlighter::highlightBlock(const QString &text)
{
    QTextCharFormat kw;
    kw.setForeground(Qt::blue);
    kw.setFontWeight(QFont::Bold);

    static const QRegularExpression re("\\b(class|return|if|else)\\b");
    auto it = re.globalMatch(text);
    while (it.hasNext()) {
        const auto m = it.next();
        setFormat(m.capturedStart(), m.capturedLength(), kw);
    }
}
```

多行注释需要 block state：

```cpp
setCurrentBlockState(0);
if (previousBlockState() == InComment)
    continueCommentFromStart(text);
```

状态是整数，你自己定义含义。它让 highlighter 知道上一块是否结束在字符串、注释、预处理续行等上下文中。

## 5. 使用场景

- 代码编辑器语法高亮。
- Markdown、日志、配置文件着色。
- 搜索结果或诊断信息临时标色。
- 括号匹配、缩进层级、折叠信息缓存。
- 教学工具展示 token 分类。

## 6. 常见坑与经验

- `highlightBlock()` 里不要修改文档文本，否则很容易触发递归或状态混乱。
- 只调用 `setFormat()` 改显示格式，不要把它当富文本写入。
- 正则表达式应缓存，不要每个 block 每次都重新构造大量对象。
- 多行语法必须正确设置 block state，否则编辑中间一行时后续块不会得到正确上下文。
- `setCurrentBlockUserData()` 会把所有权交给文档，块删除时自动释放。
- 大文档 `rehighlight()` 可能昂贵，主题变更才适合全量刷新；局部变化优先 `rehighlightBlock()`。

## 7. 知识点覆盖

本页覆盖：逐块高亮、`QTextDocument` 安装、格式范围、正则匹配、多行状态、块用户数据、性能优化、编辑器集成。
