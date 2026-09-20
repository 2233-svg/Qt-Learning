# QGraphicsTextItem

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsTextItem`

## 1. 先建立直觉

`QGraphicsTextItem` 是场景中的富文本图元。它基于 `QTextDocument`，可以显示纯文本或 HTML，支持字体、颜色、链接、文本宽度、交互标志，甚至可以作为场景里的可编辑文本框。

它比 `QGraphicsSimpleTextItem` 更强，也更重。短标签用 simple text；需要换行、富文本、链接或编辑时，用 text item。

## 2. 类说明

`QGraphicsTextItem` 继承自 `QGraphicsObject`，因此拥有 QObject、信号槽和属性能力。内部文档可通过 `document()` 访问，也可用 `setDocument()` 替换。

它在图形场景中处理键盘、输入法、鼠标选择、链接点击等复杂文本交互。做可编辑画布文字、注释、富文本标签时非常有用。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsTextItem(parent)` | 创建空文本图元。 |
| `QGraphicsTextItem(QString, parent)` | 创建带文本的图元。 |
| `setPlainText()` / `toPlainText()` | 设置或读取纯文本。 |
| `setHtml()` / `toHtml()` | 设置或读取 HTML。 |
| `setFont()` / `font()` | 设置默认字体。 |
| `setDefaultTextColor()` / `defaultTextColor()` | 设置默认文字颜色。 |
| `setTextWidth()` / `textWidth()` | 设置文本排版宽度，影响换行。 |
| `adjustSize()` | 让 item 尺寸适应文档内容。 |
| `setTextInteractionFlags()` | 控制是否可选择、可编辑、可打开链接。 |
| `setOpenExternalLinks(bool)` | 控制点击链接是否用外部浏览器打开。 |
| `setTextCursor()` / `textCursor()` | 设置或读取当前文本光标。 |
| `document()` / `setDocument()` | 访问或替换底层 `QTextDocument`。 |
| `linkActivated()` | 链接被激活时发出。 |
| `linkHovered()` | 鼠标悬停链接时发出。 |

## 4. 关键用法

显示可换行说明：

```cpp
auto *text = new QGraphicsTextItem;
text->setTextWidth(220);
text->setHtml("<b>Error</b><br/>Connection timed out.");
scene->addItem(text);
```

让文本可编辑：

```cpp
text->setTextInteractionFlags(Qt::TextEditorInteraction);
text->setFlag(QGraphicsItem::ItemIsFocusable);
```

处理链接：

```cpp
text->setOpenExternalLinks(false);
connect(text, &QGraphicsTextItem::linkActivated,
        this, &HelpController::openTopic);
```

## 5. 使用场景

适合富文本标注、可编辑画布文字、流程图说明、节点内多行文本、帮助气泡、带链接的场景说明、图形化文档编辑。

如果只是一个短标题，`QGraphicsSimpleTextItem` 更轻。若要完整文本编辑器体验，普通 `QTextEdit` 或 `QPlainTextEdit` 更成熟。

## 6. 常见坑与经验

可编辑文本需要焦点。忘记 `ItemIsFocusable` 或交互 flags，用户会看到文本但无法输入。

HTML 能力来自 `QTextDocument` 支持的子集，不是浏览器。不要期望完整 CSS/JavaScript/Web 布局。

`setTextWidth()` 很关键。没有宽度时文本可能横向无限延伸，导致场景边界和滚动体验很差。
