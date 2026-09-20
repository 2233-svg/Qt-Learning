<!-- 依据 Qt 6.11.1 头文件 qgraphicsitem.h 整理。 -->

# QGraphicsSimpleTextItem 深入笔记

> 头文件：`#include <QGraphicsSimpleTextItem>`  
> 模块：`Qt6::Widgets`  
> 继承：`QGraphicsItem -> QAbstractGraphicsShapeItem -> QGraphicsSimpleTextItem`

## 1. 它解决什么问题

`QGraphicsSimpleTextItem` 用轻量方式在 Graphics View 中绘制纯文本。它适合节点标题、坐标刻度、状态标签、调试标记等“展示为主、格式简单”的文本。

它不使用 `QTextDocument`，所以没有富文本 HTML、链接、文本光标、选择、输入法编辑或自动按给定宽度排版等能力。需要这些功能时用 `QGraphicsTextItem`。

| 需求 | 选择 |
| --- | --- |
| 简单标签、刻度、短标题、频繁更新的状态文字 | `QGraphicsSimpleTextItem` |
| 富文本、自动换行、链接、可编辑文本、`QTextDocument` | `QGraphicsTextItem` |
| 复杂控件式文本编辑体验 | `QGraphicsProxyWidget` + `QTextEdit` / `QLineEdit` |

它能处理纯文本中的 `\n` 和其它行分隔符，但不会解释 HTML 标签。`"<b>警告</b>"` 会作为字面文本显示，而不是加粗。

## 2. 最小使用路径

```cpp
#include <QGraphicsSimpleTextItem>
#include <QFont>

auto *label = new QGraphicsSimpleTextItem("CPU 72%");

QFont font;
font.setPointSize(11);
font.setBold(true);
label->setFont(font);
label->setBrush(QColor("#234a6d"));
label->setPos(24, 18);

scene->addItem(label);
```

文本内容、字体、brush 和 pen 共同决定实际 `boundingRect()`。设置内容或字体后，无需手动要求 scene 重绘；标准 setter 会更新相应几何和绘制状态。

## 3. 文本、字体、brush 和 pen 各管什么

```cpp
label->setText("连接已断开");
label->setFont(QFont("Microsoft YaHei", 10));
label->setBrush(QColor("#aa3a32"));
label->setPen(Qt::NoPen);
```

- `text`：纯文本内容，可含换行。
- `font`：字体家族、大小、粗细、字距等排版度量。
- `brush`：字形内部填充色或纹理。
- `pen`：字形外轮廓。默认是 `Qt::NoPen`。

给文本加 pen 会绘制每个字形的轮廓。短标题或大字号徽标可以使用；长段文本、复杂虚线、粗描边或高频变更文字会增加绘制成本，通常应只用 brush。

## 4. `boundingRect()` 随文本和字体变化

```cpp
const QRectF bounds = label->boundingRect();
background->setRect(bounds.adjusted(-6, -3, 6, 3));
```

`boundingRect()` 是图元本地坐标中的文本外接范围。它不是 scene 坐标，也不会自动包含你想要的背景留白。做标签背景、选中框或点击热区时，应根据文本边界自行 `adjusted()`。

当图元位置改变时，用 `setPos()`；不要通过给文字开头塞空格、换行或通过修改 font 来“微调位置”。这些做法会破坏布局、翻译和字体切换后的稳定性。

`shape()` 和 `contains()` 基于文本图元的有效形状。场景坐标测试需要先映射：

```cpp
const bool hit = label->contains(
    label->mapFromScene(scenePoint));
```

## 5. 多行不等于富文本布局

```cpp
label->setText("下载中\n42%");
```

这是允许的，但每一行按相同的简单 font/brush/pen 规则绘制。它没有：

- 不同片段不同颜色或字号。
- 自动根据最大宽度换行。
- 段落边距、对齐、列表或图片嵌入。
- 可编辑的光标与文本选择。

如果文本是否换行取决于容器宽度，`QGraphicsSimpleTextItem` 不是正确选择。不要在 resize 中手工插入换行字符模拟排版；使用 `QGraphicsTextItem::setTextWidth()` 和 `QTextDocument` 更可靠。

## 6. 缩放和可读性

文本属于图元几何，view 缩放或 item 缩放时它也会一起缩放。地图、画布和图表中常会遇到“缩小后字太小、放大后字太大”的问题。

可选策略：

- 文本应随内容一起缩放：保持默认变换。
- 文本需要始终面向屏幕、大小稳定：使用 `ItemIgnoresTransformations`，但要注意它与 scene 坐标布局、命中和重叠的关系。
- 标签数量巨大：减少每帧 `setText()` / `setFont()` 次数，按可视范围或缩放级别决定是否显示标签。

不要为了改善缩放清晰度反复创建文本 item。优先让 item 复用，只有内容或样式真正变化时才更新。

## 7. 与 `QGraphicsTextItem` 的选择边界

`QGraphicsSimpleTextItem` 不是 `QGraphicsTextItem` 的轻量“编辑模式”，而是完全不同的文本模型：

```text
SimpleTextItem: QString + QFont + pen/brush
TextItem:       QTextDocument + 富文本布局 + 编辑交互
```

一旦需求包含可选择、可编辑、链接、HTML、自动换行、不同样式片段或文档边距，就应直接采用 `QGraphicsTextItem`。后期把大量 SimpleTextItem “补成富文本”通常会导致额外的数据同步和几何修补。

## 8. 类型和框架接口

`type()` 返回 `QGraphicsSimpleTextItem::Type`，值为 `9`。在异构 item 集合中需先比较 `type()`，再转换指针。

`paint()`、`boundingRect()`、`shape()` 和 `contains()` 属于场景绘制与命中流程。`isObscuredBy()`、`opaqueArea()` 用于遮挡优化；受保护 `Extension` API 是框架扩展协议，普通应用不直接调用。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型常量 | `QGraphicsSimpleTextItem::Type = 9` | 标识简单文本图元的运行时类型。 | 用 `type()` 确认后再 `static_cast`。 |
| 构造 | `explicit QGraphicsSimpleTextItem(QGraphicsItem *parent = nullptr)` | 创建空的简单文本图元。 | 后续用 `setText()` 设置内容。 |
| 构造 | `explicit QGraphicsSimpleTextItem(const QString &text, QGraphicsItem *parent = nullptr)` | 用纯文本创建图元。 | HTML 不会被解析；换行字符可用。 |
| 析构 | `~QGraphicsSimpleTextItem()` | 销毁文本图元。 | 由 scene 或图元父子树管理。 |
| 文本读取 | `QString text() const` | 返回当前纯文本。 | 返回内容不包含富文本结构，因为本类没有富文本。 |
| 文本设置 | `void setText(const QString &text)` | 设置纯文本内容。 | 内容会影响边界；频繁大文本更新会增加布局与绘制成本。 |
| 字体读取 | `QFont font() const` | 返回当前字体。 | 字体变化会影响 `boundingRect()`。 |
| 字体设置 | `void setFont(const QFont &font)` | 设置字体样式和度量。 | 用 `setPos()` 做位置调整，不要用字体/空格凑位置。 |
| 绘制边界 | `QRectF boundingRect() const` | 返回文本的本地外接范围。 | 背景和选中留白需自行 `adjusted()`。 |
| 命中 | `QPainterPath shape() const` | 返回文本有效形状路径。 | 精确交互用它；坐标为 item 本地坐标。 |
| 命中 | `bool contains(const QPointF &point) const` | 判断本地点是否命中文本。 | scene 点先 `mapFromScene()`。 |
| 绘制 | `void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)` | 按文本、font、pen/brush 绘制字形。 | 由 Graphics View 调用，不直接从业务代码调用。 |
| 遮挡优化 | `bool isObscuredBy(const QGraphicsItem *item) const` | 判断其它 item 是否遮住文本。 | 不是文本重叠或碰撞检测 API。 |
| 遮挡优化 | `QPainterPath opaqueArea() const` | 返回已知完全不透明区域。 | 用于 scene 绘制优化。 |
| 类型查询 | `int type() const` | 返回 `QGraphicsSimpleTextItem::Type`。 | 用于异构图元集合的类型分派。 |
| 受保护扩展 | `bool supportsExtension(Extension extension) const` | 查询是否支持指定图元扩展。 | Qt 框架协议，普通应用不调用。 |
| 受保护扩展 | `void setExtension(Extension extension, const QVariant &variant)` | 写入扩展数据。 | 仅自定义图元框架扩展时使用。 |
| 受保护扩展 | `QVariant extension(const QVariant &variant) const` | 读取扩展数据。 | 参数和返回语义由具体扩展决定。 |

## 10. 排查清单

1. HTML 标签原样显示：本类只支持纯文本，改用 `QGraphicsTextItem`。
2. 容器变窄时文字不换行：本类没有文本宽度和自动换行，改用 `QGraphicsTextItem`。
3. 修改字符串后背景框尺寸不对：重新读取 `boundingRect()`，不要缓存旧尺寸。
4. 长文本描边后卡顿：移除复杂 pen，只用 brush，或改用更适合的文本实现。
5. scene 坐标点判断失败：先映射到文本 item 本地坐标再 `contains()`。

### 一句话总结

`QGraphicsSimpleTextItem` 是纯文本标签图元：用 `QString + QFont + brush/pen` 快速绘制简单文字，能换行但不做富文本排版；一旦需要文档、编辑或宽度驱动换行，应直接切换到 `QGraphicsTextItem`。
