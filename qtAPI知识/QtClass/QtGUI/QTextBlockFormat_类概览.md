# Qt QTextBlockFormat 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextBlockFormat>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QTextFormat -> QTextBlockFormat`

## 1. 它解决什么问题

`QTextBlockFormat` 描述一个文本块（通常就是一个段落）的排版属性。它只描述“这一段应该怎样排”，不保存段落文字，也不负责把格式应用到文档。真正修改 `QTextDocument` 时，通常由 `QTextCursor::setBlockFormat()` 或 `QTextCursor::mergeBlockFormat()` 使用它。

它适合表达这些信息：

- 段落水平对齐、首行缩进、整体缩进和四周边距；
- 行高策略，例如固定行高、最小行高和按比例行高；
- 标题级别、不可分页拆分、分页前后策略；
- 自定义制表位和列表标记状态。

可以把它和 `QTextCharFormat` 区分开：前者作用于段落盒子的布局，后者作用于选中文本的字体、颜色和下划线。一个段落可以同时拥有两者。

## 2. 典型使用场景

### 2.1 设置编辑器当前段落的排版

```cpp
QTextCursor cursor = editor->textCursor();

QTextBlockFormat format = cursor.blockFormat();
format.setAlignment(Qt::AlignCenter);
format.setTopMargin(8);
format.setBottomMargin(8);
format.setTextIndent(24);

cursor.mergeBlockFormat(format);
editor->setTextCursor(cursor);
```

`mergeBlockFormat()` 只合并格式中已经设置的属性，适合工具栏按钮和“只改对齐、不碰其它段落属性”的操作。若希望用一组完整属性替换当前段落格式，可使用 `setBlockFormat()`。

### 2.2 创建标题、正文和代码段样式

```cpp
QTextCursor cursor(document);
cursor.insertText(QStringLiteral("标题"));

QTextBlockFormat heading;
heading.setHeadingLevel(1);
heading.setAlignment(Qt::AlignLeft);
heading.setBottomMargin(12);
heading.setLineHeight(130, QTextBlockFormat::ProportionalHeight);
cursor.setBlockFormat(heading);
```

标题级别是文档语义信息；它不会自动替你改变字体大小。需要视觉效果时，还要配合 `QTextCharFormat` 设置字体。

### 2.3 控制打印或分页布局

```cpp
QTextBlockFormat format;
format.setPageBreakPolicy(QTextFormat::PageBreak_AlwaysBefore);
format.setNonBreakableLines(true);
```

这些属性主要供文档布局、打印和导出路径参考。把格式放进文档并不等于所有显示控件都会以同样方式分页；分页只有在使用分页布局或打印相关流程时才有意义。

## 3. 对象模型与使用边界

`QTextBlockFormat` 是一个可复制的隐式共享值类型，不是 `QObject`：

- 不需要父对象，也不需要事件循环；
- 可以按值返回、保存到容器或在线程间传递副本；
- 修改副本时 Qt 会执行写时分离，不会直接改掉原来的格式对象；
- 它本身不指向某个段落。只有应用到 `QTextCursor` 或文档后，属性才会影响文本布局；
- 它继承 `QTextFormat` 的属性表，`isValid()` 用于确认格式类型是块格式。

格式数值通常按文档布局坐标理解，实际像素效果还会受到字体、设备缩放、文档布局器和视口宽度影响。负边距、负缩进以及极端行高虽然能写入属性表，但可能造成内容越界或布局结果不直观，应由调用方限制输入。

## 4. 最小可用代码

```cpp
#include <QTextBlockFormat>
#include <QTextCursor>
#include <QTextDocument>

QTextBlockFormat makeBodyFormat()
{
    QTextBlockFormat format;
    format.setAlignment(Qt::AlignLeft);
    format.setLeftMargin(0);
    format.setRightMargin(0);
    format.setTextIndent(24);
    format.setLineHeight(120, QTextBlockFormat::ProportionalHeight);
    return format;
}

void applyBodyFormat(QTextDocument *document)
{
    QTextCursor cursor(document);
    cursor.select(QTextCursor::Document);
    cursor.setBlockFormat(makeBodyFormat());
}
```

`QTextCursor::select(QTextCursor::Document)` 会选中文档内容，但块格式作用于选区覆盖到的段落。若只想改当前段落，直接使用当前光标即可。

## 5. 关键语义

### 5.1 对齐的默认值

`alignment()` 读取 `BlockAlignment` 属性。属性未设置或值为 `0` 时，Qt 返回 `Qt::AlignLeft`，所以“没有显式设置对齐”和“读到左对齐”在这个 getter 上不可区分。需要判断是否显式设置时，应通过继承的 `hasProperty(QTextFormat::BlockAlignment)` 查询。

`setAlignment()` 接受 `Qt::Alignment`，可以组合水平、垂直和阅读方向相关标志，但段落布局最常用的是 `Qt::AlignLeft`、`Qt::AlignRight`、`Qt::AlignHCenter` 和 `Qt::AlignJustify`。

### 5.2 四种边距与首行缩进

`topMargin()`、`bottomMargin()`、`leftMargin()` 和 `rightMargin()` 是段落外侧边距；它们会影响段落与相邻内容或边界之间的距离。

`textIndent()` 是首行相对于段落正文起始位置的额外缩进。它和 `leftMargin()` 不是一回事：左边距会影响整个段落，首行缩进只影响第一行。悬挂缩进可以用负的 `textIndent()` 表达，但应确认目标布局器对负值的处理。

### 5.3 `indent()` 是层级，不是长度

`setIndent(int)` 保存的是段落缩进层级，常用于富文本列表、编辑器的增加/减少缩进命令。它不是以像素、点或文档坐标表示的边距；具体层级换算由布局和相关文档功能决定。

如果需要精确控制第一行或整个段落的几何位置，使用 `setTextIndent()` 与四个 margin API，而不是把 `indent()` 当作像素值。

### 5.4 行高计算

`setLineHeight(height, heightType)` 会同时写入行高数值和行高类型。只写其中一个属性，可能得到与预期不一致的结果；推荐总是成对设置。

无参数 `lineHeight()` 只返回保存的数值，不返回最终屏幕行高。布局器在已有脚本行高 `scriptLineHeight` 和缩放系数 `scaling` 下，应使用带参数重载，其计算规则是：

| 类型 | 最终行高 |
| --- | --- |
| `SingleHeight` | `scriptLineHeight`，忽略保存的数值 |
| `ProportionalHeight` | `scriptLineHeight * height / 100` |
| `FixedHeight` | `height * scaling` |
| `MinimumHeight` | `max(scriptLineHeight, height * scaling)` |
| `LineDistanceHeight` | `scriptLineHeight + height * scaling` |

因此：

- 比例值 `120` 表示脚本行高的 120%，不是 `1.2`；
- 固定和最小行高会受 `scaling` 影响；
- `SingleHeight` 下即使设置了一个数值，带参数的 `lineHeight()` 仍返回脚本行高；
- 负数或零可能造成压缩、重叠或被布局器以特殊方式处理，输入控件不应无条件接受。

### 5.5 标题级别

`setHeadingLevel(level)` 保存 HTML/富文本文档意义上的标题层级。它主要用于文档结构、导出和导航语义，不负责自动设置字体。`headingLevel()` 未设置时通常读到 `0`，可将 `0` 理解为“没有标题级别”。

### 5.6 不可拆分行与分页策略

`setNonBreakableLines(true)` 请求布局器不要把该段落的行拆到不同页面。段落本身太高、页面空间不足或目标输出器不支持该约束时，仍不能把它当作绝对保证。

`setPageBreakPolicy()` 使用 `QTextFormat::PageBreakFlags`：

- `PageBreak_Auto`：由布局器自动决定；
- `PageBreak_AlwaysBefore`：要求段落前分页；
- `PageBreak_AlwaysAfter`：要求段落后分页。

这些是标志位，可以按需组合。它们是排版提示，不是 `QTextDocument` 的手动分页 API。

### 5.7 制表位和段落标记

`setTabPositions()` 保存一份 `QList<QTextOption::Tab>`。传入的列表是值拷贝，调用后修改原列表不会改变格式；`tabPositions()` 返回的列表也应视作副本，修改它不会回写格式，需再次调用 `setTabPositions()`。

制表位的对齐方式、位置和填充字符由 `QTextOption::Tab` 表达。制表位只影响文本布局中的 `\t`，不会把普通空格变成对齐列。

`setMarker()` 保存段落标记状态：

- `NoMarker`：无复选标记；
- `Unchecked`：未选中的标记；
- `Checked`：已选中的标记。

它描述的是块格式中的标记状态，不会自动创建可点击的复选框，也不会自动把段落加入 `QTextList`。

## 6. 与相关 API 的配合

### `QTextCursor::setBlockFormat()` 与 `mergeBlockFormat()`

- `setBlockFormat(format)`：用给定块格式替换选区覆盖段落的块格式；
- `mergeBlockFormat(format)`：把给定格式中存在的属性合并到现有块格式。

工具栏交互通常优先使用合并；导入模板或重置段落时才考虑完整替换。格式对象的属性是否“存在”很重要：getter 返回默认值不代表属性已经存在。

### `QTextBlock::blockFormat()`

从文档读取段落时，`QTextBlock::blockFormat()` 返回该块当前格式的值拷贝。修改返回值只修改副本，必须再通过光标应用回文档。

### `QTextFormat` 属性表

当专用 getter 不足以表达需求时，可以使用继承的 `property()`、`setProperty()`、`hasProperty()` 和 `clearProperty()`。优先使用专用 API，因为它们会表达正确的类型并减少写错属性 ID 的机会。

## 7. 逐项 API 说明

### 成员类型

#### `enum QTextBlockFormat::LineHeightTypes`

行高策略枚举。它与 `setLineHeight(qreal, int)` 配套使用。

| 枚举值 | 含义 |
| --- | --- |
| `SingleHeight` | 使用布局器提供的脚本行高；保存的数值不参与带参数行高计算。 |
| `ProportionalHeight` | 将脚本行高乘以保存值的百分比。`100` 表示原始高度。 |
| `FixedHeight` | 使用保存的固定高度，并乘以布局缩放系数。 |
| `MinimumHeight` | 使用脚本行高和指定最小高度中较大的值。 |
| `LineDistanceHeight` | 在脚本行高上增加指定的额外行距。 |

#### `enum class QTextBlockFormat::MarkerType`

段落复选标记状态。它不是通用项目符号类型；项目符号和编号列表应使用 `QTextListFormat`。

| 枚举值 | 含义 |
| --- | --- |
| `NoMarker` | 不显示复选标记状态。 |
| `Unchecked` | 未选中的标记。 |
| `Checked` | 已选中的标记。 |

### 构造与有效性

#### `QTextBlockFormat::QTextBlockFormat()`

构造一个块格式对象。它不绑定文档或段落，也不会修改任何文本。新对象可以直接配置后交给 `QTextCursor`。

#### `bool QTextBlockFormat::isValid() const`

检查该格式的类型是否为 `QTextFormat::BlockFormat`。正常通过默认构造得到的 `QTextBlockFormat` 是有效的；它与“是否设置了某个属性”是两个概念。可用继承的 `isEmpty()` 判断属性表是否为空。

### 对齐、边距与缩进

#### `void setAlignment(Qt::Alignment alignment)`

设置段落对齐方式。它保存的是标志值；想保留其它块属性时，应通过 `mergeBlockFormat()` 应用。

#### `Qt::Alignment alignment() const`

返回段落对齐方式。未设置时返回 `Qt::AlignLeft`。如需区分“未设置”和“显式左对齐”，使用 `hasProperty(QTextFormat::BlockAlignment)`。

#### `void setTopMargin(qreal margin)`

设置段落上边距。边距单位由文档布局坐标决定，通常可按设备无关的排版单位理解。

#### `qreal topMargin() const`

返回保存的上边距；未设置时通常为 `0`。它不包含字体行高，也不等价于控件的外边距。

#### `void setBottomMargin(qreal margin)`

设置段落下边距。连续段落的视觉间隔还可能受布局器如何处理相邻边距影响。

#### `qreal bottomMargin() const`

返回保存的下边距；未设置时通常为 `0`。

#### `void setLeftMargin(qreal margin)`

设置段落左边距，影响段落整体起始位置。

#### `qreal leftMargin() const`

返回保存的左边距；未设置时通常为 `0`。

#### `void setRightMargin(qreal margin)`

设置段落右边距，影响段落可用宽度。

#### `qreal rightMargin() const`

返回保存的右边距；未设置时通常为 `0`。

#### `void setTextIndent(qreal indent)`

设置首行缩进。正值通常表示首行向正文区域内缩进，负值可用于悬挂缩进。

#### `qreal textIndent() const`

返回首行缩进值；未设置时通常为 `0`。它与 `indent()` 的层级语义不同。

#### `void setIndent(int indent)`

设置段落缩进层级。它适合编辑器的层级操作和列表语义，不是几何长度。

#### `int indent() const`

返回段落缩进层级；未设置时通常为 `0`。

### 行高与标题

#### `void setLineHeight(qreal height, int heightType)`

同时设置行高数值和 `LineHeightTypes`。`heightType` 应传入本类枚举值。比例类型按百分数解释，不要传 `1.2` 代替 `120`。

#### `qreal lineHeight() const`

返回格式中保存的行高数值，不是经过脚本行高和缩放系数计算后的最终行高。

#### `qreal lineHeight(qreal scriptLineHeight, qreal scaling = 1.0) const`

按照当前行高类型计算实际行高。`scriptLineHeight` 应来自文本布局器，`scaling` 是布局缩放系数。若行高类型不是已知枚举值，Qt 头文件实现返回 `0`，因此不要把任意整数当作自定义类型传入。

#### `int lineHeightType() const`

返回保存的行高类型整数，可与 `LineHeightTypes` 比较。未设置时通常为 `0`，即 `SingleHeight`。

#### `void setHeadingLevel(int level)`

设置标题层级。级别的具体解释由文档格式和导出路径决定；它不自动改变字符格式。

#### `int headingLevel() const`

返回标题层级；未设置时通常为 `0`。

### 分页、标记与制表位

#### `void setNonBreakableLines(bool b)`

设置是否请求保持该段落的所有行在同一页。它只对支持分页的布局流程有意义。

#### `bool nonBreakableLines() const`

返回不可分页拆分请求；未设置时通常为 `false`。

#### `void setPageBreakPolicy(QTextFormat::PageBreakFlags policy)`

设置段落前后分页策略。可使用 `QTextFormat::PageBreak_Auto`、`PageBreak_AlwaysBefore` 和 `PageBreak_AlwaysAfter` 组合标志。

#### `QTextFormat::PageBreakFlags pageBreakPolicy() const`

返回保存的分页标志。该返回值是 Qt flags 类型，应使用 `testFlag()` 或 `operator&` 检查，而不是假设它只有一个枚举值。

#### `void setTabPositions(const QList<QTextOption::Tab> &tabs)`

设置该段落使用的制表位列表。列表按值保存；如果需要清除自定义制表位，可传入空列表。

#### `QList<QTextOption::Tab> tabPositions() const`

返回自定义制表位的副本。空列表表示没有专用制表位；实际布局仍可能有默认制表间距。

#### `void setMarker(QTextBlockFormat::MarkerType marker)`

设置段落标记状态。它只记录状态，是否绘制以及如何交互取决于使用该格式的文档视图或自定义布局代码。

#### `QTextBlockFormat::MarkerType marker() const`

返回段落标记状态；未设置时通常是 `NoMarker`。

## 8. 常见误区与排查顺序

1. 先确认格式确实应用到了目标段落。只修改 `QTextBlock::blockFormat()` 的返回值不会改变文档。
2. 需要只改一项属性时使用 `mergeBlockFormat()`，避免 `setBlockFormat()` 覆盖已有段落设置。
3. 检查行高类型和数值是否成对设置，并确认比例值使用百分数。
4. 不要把 `indent()` 当作像素值；精确几何控制使用 margin 和 `textIndent()`。
5. 分页策略在普通屏幕编辑器中可能看不出效果，应在打印或分页布局流程中验证。
6. 判断属性是否显式设置时使用 `hasProperty()`，不要只看 getter 返回的默认值。

## 9. 线程与生命周期

格式对象本身是可复制的值类型，不需要 GUI 线程，也没有 QObject 父子关系。可是，读写它所对应的 `QTextDocument`、`QTextCursor` 和视图时，仍应遵守这些对象各自的线程约束；不要把同一个正在被修改的文档同时交给多个线程。

把格式跨线程传递时传递副本，并在拥有目标文档的线程中应用。`QList<QTextOption::Tab>` 也按值复制，因此不会形成对调用方列表的悬空引用。

## API 速查表
| 类别 | API | 语义速记 | 边界与注意 |
| --- | --- | --- | --- |
| 类型 | `LineHeightTypes` | 定义段落行高算法。 | `ProportionalHeight` 使用百分数；未知整数可能使计算结果为 `0`。 |
| 类型 | `MarkerType` | 定义段落复选标记状态。 | 不等于 `QTextListFormat` 的项目符号。 |
| 构造 | `QTextBlockFormat()` | 创建独立的块格式值对象。 | 不绑定文档，不会自动应用。 |
| 状态 | `isValid()` | 判断格式类型是否为块格式。 | 有效不代表属性已设置。 |
| 对齐 | `setAlignment()` / `alignment()` | 设置或读取段落对齐。 | 未设置的 getter 返回 `Qt::AlignLeft`；用 `hasProperty()` 判断显式设置。 |
| 边距 | `setTopMargin()` / `topMargin()` | 设置或读取上边距。 | 影响段落布局，不是控件外边距。 |
| 边距 | `setBottomMargin()` / `bottomMargin()` | 设置或读取下边距。 | 相邻段落间距由布局器综合处理。 |
| 边距 | `setLeftMargin()` / `leftMargin()` | 设置或读取左边距。 | 影响整个段落。 |
| 边距 | `setRightMargin()` / `rightMargin()` | 设置或读取右边距。 | 影响段落可用宽度。 |
| 缩进 | `setTextIndent()` / `textIndent()` | 设置或读取首行缩进。 | 负值可形成悬挂缩进。 |
| 缩进 | `setIndent()` / `indent()` | 设置或读取缩进层级。 | 不是像素或点数。 |
| 标题 | `setHeadingLevel()` / `headingLevel()` | 保存标题层级语义。 | 不自动改变字体外观。 |
| 行高 | `setLineHeight()` | 同时设置行高值和类型。 | 比例值如 `120` 表示 120%。 |
| 行高 | `lineHeight()` | 读取保存的行高值。 | 不是最终布局行高。 |
| 行高 | `lineHeight(scriptLineHeight, scaling)` | 按类型计算最终行高。 | `scaling` 对固定、最小、额外行距类型生效。 |
| 行高 | `lineHeightType()` | 读取行高类型整数。 | 与 `LineHeightTypes` 配套。 |
| 分页 | `setNonBreakableLines()` / `nonBreakableLines()` | 请求段落行不跨页。 | 仅分页布局或打印流程有意义，不能视为绝对保证。 |
| 分页 | `setPageBreakPolicy()` / `pageBreakPolicy()` | 设置或读取分页 flags。 | 用 `testFlag()` 检查组合值。 |
| 制表位 | `setTabPositions()` / `tabPositions()` | 设置或读取自定义制表位。 | 列表按值复制；只影响文本中的 `\t`。 |
| 标记 | `setMarker()` / `marker()` | 设置或读取复选标记状态。 | 不自动绘制或提供点击行为。 |

---

### 一句话总结

`QTextBlockFormat` 是段落排版的值对象：用它描述块级属性，再通过 `QTextCursor` 应用到文档；处理行高、缩进和分页时，必须区分“保存的属性值”和“布局器计算出的最终结果”。
