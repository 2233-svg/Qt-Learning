# QTextCharFormat：描述一段富文本字符的外观与语义

> Qt 6.11.1 | `#include <QTextCharFormat>` | 模块：`Qt6::Gui`
>
> 继承关系：`QTextFormat -> QTextCharFormat`。派生类包括 `QTextImageFormat` 与 `QTextTableCellFormat`。

`QTextCharFormat` 是富文本文字片段的格式值：字体、颜色、下划线、上下标、超链接、提示文字、文字轮廓，以及表格单元格的行列跨度等都由它描述。它不保存字符，也不会主动改变某份文档；要让格式生效，应把它交给 `QTextCursor`、高亮器或文档插入 API。

它适合富文本编辑器的“加粗所选文本”、语法高亮器的“把关键字涂色”、帮助文档的“生成链接”、公式编辑器的“设置上下标”等场景。

## 值类型与应用方式

`QTextCharFormat` 是隐式共享的值类型。复制、存入容器和按值返回都很便宜；某个副本被修改时会按需分离，修改不会反向改变其它副本或已经写入文档的格式。

最常用的编辑方式是对选区合并格式：

```cpp
QTextCharFormat emphasis;
emphasis.setFontWeight(QFont::Bold);
emphasis.setForeground(QColor("#b42318")); // QTextFormat 的继承 API

QTextCursor cursor = editor->textCursor();
if (cursor.hasSelection())
    cursor.mergeCharFormat(emphasis);
```

`mergeCharFormat()` 只覆盖 `emphasis` 中已设置的属性，适合工具栏按钮。`setCharFormat()` 则把选中区域改成给定格式，更容易清掉原有的局部属性。插入新文本时，`insertText(text, format)` 把格式附到新文本；没有选区时，`setCharFormat()` 还会影响随后输入的字符格式，这一点常被误当成“什么也没发生”。

格式的最终显示还会与 `QTextDocument` 默认字体、块格式、样式表和平台字体回退共同决定。一个 getter 返回默认值，并不一定说明该属性曾被显式设置；若需要辨别“未设置”和“设置为默认”，使用继承的 `QTextFormat::hasProperty()` / `property()`。

## 字体属性与继承

`setFont(font, FontPropertiesAll)` 是默认行为：把 `QFont` 的整组字体属性写进格式。传入 `FontPropertiesSpecifiedOnly` 时，只采用该 `QFont` 中明确指定的属性，未指定的属性继续从文档、块或已有格式继承。后者适合“只改字体族或字号，不意外重置粗细、字距、连字等属性”。

单项 setter（如 `setFontItalic()`）只记录单一属性，通常更适合编辑器命令。Qt 6 中 `fontFamilies()` 与 `fontStyleName()` 的返回类型是 `QVariant`，读取时应按相应内容转换；Qt 7 的接口类型有所调整，跨版本代码不要把它们的返回类型写死。

OpenType 特性和可变字体轴由 `setFontFeatures()`、`setFontVariableAxes()` 提供，均从 Qt 6.11 起可用。标签和值即使能写入格式，也只有当前字体和平台文字引擎支持时才会有可见效果。

## 下划线、基线与链接

`UnderlineStyle` 中 `NoUnderline`、实线、虚线、点线、波浪线等控制绘制样式；`SpellCheckUnderline` 主要用于拼写检查一类的语义标记，不应把它当作跨平台一致的普通装饰。`setFontUnderline(true)` 只是实线下划线的简写；需要颜色或波浪线时使用 `setUnderlineStyle()` 和 `setUnderlineColor()`。

`VerticalAlignment` 的上标、下标是文本布局语义；`setBaselineOffset()`、`setSuperScriptBaseline()`、`setSubScriptBaseline()` 则控制更细的基线偏移。后者的默认值分别是 `0.0`、`50.0` 和约 `16.67`；它们应按字体与排版结果验证，不要把数值当作固定像素。

超链接需要至少用 `setAnchor(true)` 标明它是锚点，再用 `setAnchorHref()` 设置目标，或用 `setAnchorNames()` 设置命名锚点。格式本身不会打开 URL；点击、悬停和安全策略由 `QTextBrowser`、编辑器控件或应用代码处理。外来 HTML 的 URL 同样应按应用安全策略过滤。

## 表格跨度与其他属性

`setTableCellRowSpan()` / `setTableCellColumnSpan()` 为表格单元格格式服务。值小于等于 `1` 时 Qt 清除该属性，getter 仍返回 `1`；不要把 `0` 当成“自动跨列”。一般通过 `QTextTableCellFormat` 或表格 API 使用它们，而不是给普通文本设置跨度。

`setToolTip()` 只写入文本格式的提示字符串。是否展示、何时展示由承载文档的视图决定。`setTextOutline()` 给文字描边，复杂字体和小字号下可能明显增加绘制成本。

## 线程与常见误区

格式对象本身是值，不持有 `QObject`。但把它应用到 `QTextDocument` 的操作仍必须在文档所属线程中执行。

- **只修改格式对象却没有应用。** 值类型不会自动影响编辑器。
- **用 `setCharFormat()` 做“加粗”。** 它可能覆盖此前的局部颜色、链接和字体属性；按钮行为通常应合并格式。
- **把 `isValid()` 当作“最终渲染有效”。** 它只说明这是字符格式，字体是否存在、链接能否处理仍是别的问题。
- **把 URL 处理交给格式。** `anchorHref` 是元数据，不是网络请求。

## API 速查表

| API | 语义 | 边界与注意点 |
| --- | --- | --- |
| `QTextCharFormat()` / `isValid()` | 创建字符格式；`isValid()` 判断该 `QTextFormat` 是否为字符格式。 | 新对象可逐项设置；它不会自动附着到文档。 |
| `setFont(const QFont &, FontPropertiesInheritanceBehavior)` / `font()` | 批量设置或取得字体属性。 | 默认 `FontPropertiesAll`；只想写入 `QFont` 明确指定的属性时选 `FontPropertiesSpecifiedOnly`。 |
| `FontPropertiesInheritanceBehavior` | `FontPropertiesSpecifiedOnly` 与 `FontPropertiesAll` 决定 `setFont()` 如何复制属性。 | 它控制格式属性的写入范围，不是字体回退策略。 |
| `setFontFamilies()` / `fontFamilies()` | 设置或读取候选字体族列表。 | Qt 6 getter 为 `QVariant`；平台找不到字体时会回退。 |
| `setFontStyleName()` / `fontStyleName()` | 设置或读取字体样式名称。 | Qt 6 getter 为 `QVariant`；样式名是否存在取决于实际字体。 |
| `setFontPointSize()` / `fontPointSize()` | 设置或读取点大小。 | 与像素大小不同；未设置时应结合继承格式判断。 |
| `setFontWeight()` / `fontWeight()` | 设置或读取字重。 | 使用 `QFont` 的字重常量；不要假设每个字体都有对应粗细。 |
| `setFontItalic()` / `fontItalic()` | 设置或读取斜体。 | 字体可能以合成斜体替代。 |
| `setFontCapitalization()` / `fontCapitalization()` | 设置或读取大小写转换策略。 | 影响显示字形，不会修改文档原始字符。 |
| `setFontLetterSpacingType()` / `fontLetterSpacingType()` | 设置或读取字距单位类型。 | 先确定是绝对还是百分比字距，再设置数值。 |
| `setFontLetterSpacing()` / `fontLetterSpacing()` | 设置或读取字距。 | 小字号和复杂文字脚本中应目测布局结果。 |
| `setFontWordSpacing()` / `fontWordSpacing()` | 设置或读取词间距。 | 对没有空格分词的文字，效果可能有限。 |
| `setFontFixedPitch()` / `fontFixedPitch()` | 设置或读取等宽提示。 | 这是格式属性，不会凭空把比例字体变成真正等宽字体。 |
| `setFontStretch()` / `fontStretch()` | 设置或读取字宽拉伸因子。 | 字体没有对应宽度时，视觉效果与平台相关。 |
| `setFontStyleHint()` / `fontStyleHint()` | 设置或读取字体风格提示。 | `setFontStyleHint()` 同时可设置 `StyleStrategy`，默认策略为 `QFont::PreferDefault`。 |
| `setFontStyleStrategy()` / `fontStyleStrategy()` | 设置或读取字体匹配策略。 | 影响字体选择，不能保证某字体资源存在。 |
| `setFontHintingPreference()` / `fontHintingPreference()` | 设置或读取字形 hinting 偏好。 | 具体效果由平台文字引擎和渲染目标决定。 |
| `setFontKerning()` / `fontKerning()` | 设置或读取字偶距调整开关。 | 关闭 kerning 可能影响排版质量。 |
| `setFontFeatures()` / `fontFeatures()` | 设置或读取 OpenType 特性标签和值。 | Qt 6.11 起提供；字体不支持的特性通常没有可见效果。 |
| `setFontVariableAxes()` / `fontVariableAxes()` | 设置或读取可变字体轴。 | Qt 6.11 起提供；轴标签、范围和支持度来自具体字体。 |
| `setFontUnderline()` / `fontUnderline()` | 设置或查询是否为普通实线下划线。 | 这是 `SingleUnderline` 的简写；复杂样式用下方 API。 |
| `UnderlineStyle` | 下划线样式枚举，包括实线、虚线、点线、波浪线和拼写检查样式。 | `SpellCheckUnderline` 应视为语义标记，外观可因平台而异。 |
| `setUnderlineStyle()` / `underlineStyle()` | 设置或读取下划线样式。 | `NoUnderline` 清除下划线样式。 |
| `setUnderlineColor()` / `underlineColor()` | 设置或读取下划线颜色。 | 没有下划线样式时，该颜色不会形成可见下划线。 |
| `VerticalAlignment` | 文字的正常、上标、下标及行内对齐枚举。 | 上下标与手动基线偏移可以叠加，需避免过度偏移。 |
| `setVerticalAlignment()` / `verticalAlignment()` | 设置或读取垂直对齐。 | 适合语义上下标；精细排版再配合基线 API。 |
| `setBaselineOffset()` / `baselineOffset()` | 设置或读取普通文字基线偏移。 | 默认 `0.0`；数值不是固定像素，应按字体测试。 |
| `setSuperScriptBaseline()` / `superScriptBaseline()` | 设置或读取上标基线位置。 | 默认 `50.0`；用于调整上标布局。 |
| `setSubScriptBaseline()` / `subScriptBaseline()` | 设置或读取下标基线位置。 | 默认约 `16.67`；用于调整下标布局。 |
| `setTextOutline()` / `textOutline()` | 设置或读取文字轮廓 `QPen`。 | 描边会影响绘制成本和小字号清晰度。 |
| `setToolTip()` / `toolTip()` | 设置或读取附在文本上的提示字符串。 | 是否显示由视图控件决定。 |
| `setAnchor()` / `isAnchor()` | 标记或查询字符格式是否为锚点。 | 仅为格式元数据，不能自行处理点击。 |
| `setAnchorHref()` / `anchorHref()` | 设置或读取链接目标。 | URL 的打开、校验和权限由应用实现。 |
| `setAnchorNames()` / `anchorNames()` | 设置或读取命名锚点列表。 | 适合文档内跳转目标；名称冲突由应用内容管理。 |
| `setTableCellRowSpan()` / `tableCellRowSpan()` | 设置或读取表格单元格跨行数。 | 小于等于 `1` 会清除属性，getter 返回 `1`。 |
| `setTableCellColumnSpan()` / `tableCellColumnSpan()` | 设置或读取表格单元格跨列数。 | 小于等于 `1` 会清除属性，getter 返回 `1`。 |

## 小结

`QTextCharFormat` 是“文本片段的格式声明”，而不是编辑命令。用单项属性加 `mergeCharFormat()` 可以稳定地实现编辑器工具栏；涉及链接、字体特性、基线和表格跨度时，则要把格式值、文档布局和承载控件的职责分开看。
