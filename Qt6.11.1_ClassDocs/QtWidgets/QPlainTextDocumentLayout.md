# QPlainTextDocumentLayout

> Qt 6.11.1 · Qt Widgets · 来自 `QPlainTextDocumentLayout`

## 1. 先建立直觉

`QPlainTextDocumentLayout` 是 `QTextDocument` 的纯文本布局实现。它面向大段纯文本、代码、日志这类按块排列的内容，强调滚动和编辑效率，而不是富文本排版能力。

日常使用 `QPlainTextEdit` 时通常不会直接创建它，因为 `QPlainTextEdit` 已经为文档配置了合适的布局。只有在你直接操作 `QTextDocument`，并希望它按纯文本编辑器方式布局时，才需要显式关注这个类。

## 2. 类说明

`QPlainTextDocumentLayout` 继承自 `QAbstractTextDocumentLayout`。它负责计算文本块位置、绘制文档、命中测试、文档尺寸和光标宽度。它不负责编辑命令，也不负责滚动条；这些由 `QPlainTextEdit` 或外层视图处理。

和富文本布局相比，它更适合“很多行、格式相对简单、需要高效滚动”的场景。代码编辑器、日志查看器、大文本预览器都更贴近它的模型。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QPlainTextDocumentLayout(QTextDocument *)` | 为指定文档创建纯文本布局。 |
| `setCursorWidth(int)` / `cursorWidth()` | 设置或读取文本光标宽度，影响插入点显示。 |
| `ensureBlockLayout(const QTextBlock &)` | 确保某个文本块已经完成布局，适合按需计算块几何。 |
| `requestUpdate()` | 请求更新布局/显示，通常由编辑器内部调用。 |
| `blockBoundingRect(const QTextBlock &)` | 返回文本块的布局矩形。 |
| `documentSize()` | 返回整个文档布局尺寸。 |
| `draw(QPainter *, PaintContext)` | 按给定绘图上下文绘制文档内容。 |
| `hitTest(const QPointF &, Qt::HitTestAccuracy)` | 把坐标转换成文档字符位置。 |
| `frameBoundingRect(QTextFrame *)` | 返回 frame 区域；纯文本场景一般较少直接依赖。 |
| `pageCount()` | 返回页数；纯文本布局通常不是分页排版的主角。 |
| `documentChanged(int, int, int)` | 文档内容变化后更新内部布局，子类可重写。 |

## 4. 关键用法

直接给文档设置纯文本布局：

```cpp
auto *document = new QTextDocument(this);
document->setDocumentLayout(new QPlainTextDocumentLayout(document));
document->setPlainText(sourceText);
```

如果你只是创建普通编辑器，更推荐：

```cpp
auto *editor = new QPlainTextEdit(this);
editor->setPlainText(sourceText);
```

后者已经把滚动、光标、选择、撤销、输入法等交互都组合好了。

## 5. 使用场景

适合自定义纯文本编辑器、代码编辑器底层扩展、日志查看器、需要直接绘制 `QTextDocument` 的文本视图，以及需要按文本块计算位置的高级控件。

如果内容包含复杂表格、图片、列表、不同 block frame 或文档级富排版，`QTextDocument` 默认富文本布局更合适；如果只是显示几行不可编辑文本，用 `QLabel` 或 `QPlainTextEdit` 即可。

## 6. 常见坑与经验

不要把它当成“布局管理器”。它布局的是文本文档，不是 widgets。界面控件排列仍然由 `QLayout` 家族负责。

`ensureBlockLayout()` 是面向按需布局的工具，不是刷新整篇文档的万能按钮。需要界面更新时让编辑器或文档的正常更新机制工作。

纯文本布局并不等于没有格式。语法高亮通过 `QSyntaxHighlighter` 改变字符格式，但整体排版仍按纯文本块模型运行。
