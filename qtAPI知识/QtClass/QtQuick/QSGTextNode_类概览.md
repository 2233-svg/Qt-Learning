# QSGTextNode：把已排版文本转换为场景图内容

> Qt 6.11.1 · `#include <QSGTextNode>` · 模块：`Qt6::Quick` · 继承：`QSGTransformNode`

`QSGTextNode` 用于自定义 Qt Quick Item 中的文字绘制。它接收已完成布局的 `QTextLayout` 或 `QTextDocument`，并由场景图后端生成文字、选择区、链接和嵌入图像对应的节点。

## 它解决的问题

直接拿字符串和字体无法处理换行、富文本、文本选择和局部显示。调用方先用 `QTextLayout` 或 `QTextDocument` 排版，再将结果交给 `QSGTextNode`，使自定义 Item 能与 `Text`、`TextEdit`、`TextInput` 使用相同的场景图文字路径。

节点必须通过 `QQuickWindow::createTextNode()` 创建；这是后端适配点。添加前先配置颜色、样式、滤波、渲染类型和视口，因为 `addTextLayout()` 或 `addTextDocument()` 之后再改这些属性，对已加入内容不会生效。

## 用法与边界

```cpp
auto *node = static_cast<QSGTextNode *>(oldNode);
if (!node)
    node = window()->createTextNode();

node->clear();
node->setColor(Qt::white);
node->setTextStyle(QSGTextNode::Normal);
node->addTextLayout(QPointF(8, 6), &layout);
return node;
```

每次内容或布局改变时，先 `clear()`，再重新设置必要属性并添加布局。`selectionStart >= 0` 时，`selectionCount` 个字符将用选择背景色和选择文字色绘制；`lineStart` 与 `lineCount` 可只加入布局的一段行，常用于省略或虚拟化文本。

布局对象仅提供排版数据，不能假设节点永久拥有它；在调用期间应保持有效。所有节点写入仍仅限场景图渲染线程。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QQuickWindow::createTextNode()` | 推荐的创建入口，返回当前后端实现。 |
| `clear()` | 删除此前由布局或文档生成的内容；重建文本前先调用。 |
| `addTextLayout(position, layout, selectionStart, selectionCount, lineStart, lineCount)` | 加入已排版 `QTextLayout`；选择起点小于零表示无选择，负的 `lineCount` 表示到最后一行。 |
| `addTextDocument(position, document, selectionStart, selectionCount)` | 加入 `QTextDocument` 的已排版内容。 |
| `setColor()` / `color()` | 设置或读取正文主色；必须在添加文本前设置。 |
| `setTextStyle()` / `textStyle()` | 设置或读取文字样式，如普通、描边、凸起或凹陷效果。 |
| `setStyleColor()` / `styleColor()` | 设置或读取文字效果使用的颜色。 |
| `setLinkColor()` / `linkColor()` | 设置或读取链接文字颜色。 |
| `setSelectionColor()` / `selectionColor()` | 设置或读取选择区域背景色。 |
| `setSelectionTextColor()` / `selectionTextColor()` | 设置或读取被选中文字颜色。 |
| `setRenderType()` / `renderType()` | 选择文字渲染策略；不同后端的可用性和视觉质量不同。 |
| `setRenderTypeQuality()` / `renderTypeQuality()` | 调整渲染策略的质量参数。 |
| `setFiltering()` / `filtering()` | 设置或读取文本中图像缩放时的纹理滤波。 |
| `setViewport()` / `viewport()` | 设置或读取文字生成/显示使用的视口边界。 |
