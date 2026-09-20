# QTextFormat 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextFormat>`  
> 所属模块：`Qt6::Gui`  
> 类型：隐式共享的值类型

## 1. 它解决什么问题

`QTextFormat` 是 Qt 富文本系统的通用格式属性包。它用 property ID 到 `QVariant` 的映射保存格式；`QTextCharFormat`、`QTextBlockFormat`、`QTextFrameFormat`、`QTextListFormat` 和表格格式都建立在这套存储之上。

它解决“文档内容怎样携带可组合、可复制、可局部覆盖的格式状态”，而不保存文本内容。文本和结构属于 `QTextDocument`，定位与编辑属于 `QTextCursor`，`QTextFormat` 只描述相关范围应如何呈现或解释。

实际场景：

- 编辑器把字体、颜色、链接、段落对齐等属性应用到选区；
- 语法高亮器用 `QTextCharFormat` 描述关键字、注释和错误波浪线；
- 富文本导入器读取通用 `QTextFormat` 后分派为块、字符、列表或框架格式；
- 自定义文本对象在 format 中保存从 `UserProperty` 开始的业务属性。

## 2. 格式类型、属性与转换

`type()` 返回格式类别；`isCharFormat()`、`isBlockFormat()`、`isFrameFormat()` 等是相应类别的快捷判断。`isValid()` 只说明格式类别不是 `InvalidFormat`，不表示已经设置可见属性；`isEmpty()` 只说明没有已存储属性，不能用于判断文本是否为空。

`toCharFormat()`、`toBlockFormat()`、`toFrameFormat()` 等转换返回值对象。转换不会修改原格式，也不会自动验证它适合当前业务语境；应先用对应的 `isXxxFormat()` 判断，或者明确知道来源类型。

`Property` 是底层协议。常用分组包括：

| 属性组 | 代表属性 | 用途 |
| --- | --- | --- |
| 通用 | `BackgroundBrush`、`ForegroundBrush`、`LayoutDirection` | 背景、前景、方向等共享属性。 |
| 块 | `BlockAlignment`、`BlockTopMargin`、`TextIndent` | 段落的对齐、边距、缩进和行高。 |
| 字符 | `FontWeight`、`FontItalic`、`TextUnderlineStyle`、`AnchorHref` | 字体、装饰、超链接和基线。 |
| 列表 / 框架 / 表格 | `ListStyle`、`FrameWidth`、`TableColumns` | 对应具体派生格式的结构性属性。 |
| 图像 | `ImageName`、`ImageWidth`、`ImageMaxWidth` | 文档资源引用及显示约束。 |
| 自定义 | `UserProperty` 及更大值 | 应用或自定义文本对象的扩展字段。 |

不要占用 Qt 预定义 property ID，也不要把 `ObjectIndex`、`ObjectType` 作为普通业务字段。它们参与 `QTextDocument` 的对象查找和内部格式关系；自定义值应从 `UserProperty` 起集中定义。

## 3. 最小使用方式

```cpp
#include <QTextCharFormat>
#include <QTextCursor>

QTextCharFormat emphasis;
emphasis.setForeground(Qt::darkBlue);
emphasis.setFontWeight(QFont::DemiBold);

QTextCursor cursor(document);
cursor.select(QTextCursor::WordUnderCursor);
cursor.mergeCharFormat(emphasis);
```

这里用的是具体的 `QTextCharFormat`。只有格式要在不同具体类别之间传递、检查 property，或为自定义对象携带数据时，才直接以 `QTextFormat` 工作。

## 4. 属性合并和清除的真实语义

`merge(const QTextFormat &other)` 只把 `other` 已拥有的属性写入当前格式；`other` 中不存在的属性不会清除当前属性。因此它适合叠加一层局部覆盖，例如给已有格式添加前景色，而不适合把当前格式精确替换为另一个格式。

要删除一项显式设置，使用 `clearProperty(propertyId)`；`clearForeground()` 和 `clearBackground()` 是对应的便捷函数。清除后通常回退到文档、块或控件提供的继承/默认值，并不等于强制使用某个固定颜色。

属性读取函数会把 `QVariant` 转成目标类型：

- `property()` 保留原始 `QVariant`，最适合自定义 property；
- `intProperty()`、`doubleProperty()`、`boolProperty()`、`stringProperty()`、`brushProperty()`、`colorProperty()`、`penProperty()`、`lengthProperty()` 是便利读取；
- 属性不存在或类型不匹配时，便利函数给出目标类型的默认转换结果，不能仅凭结果值区分“未设置”和“显式设为 0/空”；需要区分时先调用 `hasProperty()`。

## 5. 所有权、线程和生命周期

`QTextFormat` 没有 QObject 归属，是可复制的值对象；复制格式不会复制文档内容，也不会立刻修改任何文档。独立构造、读取和传递格式通常不依赖 GUI 线程。

一旦格式来自 `QTextDocument`，或要通过 `QTextCursor`、`QTextLayout` 写回文档，其访问必须遵守所属文档的线程约束。不要在后台线程同时修改 GUI 线程正在布局或绘制的文档；应传递格式副本和纯数据，再由文档所属线程应用。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextFormat()` | 创建无效通用格式。 | `type()` 为 `InvalidFormat`；不应冒充具体格式。 |
| `QTextFormat(int type)` | 以指定 `FormatType` 创建格式。 | 通常由具体派生格式构造器使用。 |
| `type()` | 返回格式类别。 | 用于分派，不表示属性是否完整。 |
| `isValid()` | 判断类别是否有效。 | 与 `isEmpty()` 含义不同。 |
| `isEmpty()` | 判断是否没有已保存属性。 | 不判断文本、文档或格式类型是否为空。 |
| `isBlockFormat()` / `isCharFormat()` / `isListFormat()` / `isFrameFormat()` | 判断具体格式类别。 | 转换前的首选检查。 |
| `isImageFormat()` / `isTableFormat()` / `isTableCellFormat()` | 判断图像、表格或单元格格式。 | 图像格式也属于字符格式体系。 |
| `toBlockFormat()` / `toCharFormat()` / `toListFormat()` | 转成块、字符或列表值对象。 | 不修改原对象；先确认实际类别。 |
| `toFrameFormat()` / `toImageFormat()` / `toTableFormat()` / `toTableCellFormat()` | 转成框架、图像、表格或单元格值对象。 | 结果只能在对应文档语境中产生预期效果。 |
| `setProperty(int, const QVariant &)` | 写入任意 property 值。 | 自定义 property 从 `UserProperty` 起；值类型要与读取方约定一致。 |
| `setProperty(int, const QList<QTextLength> &)` | 写入长度约束列表。 | 主要供表格列宽等多个 `QTextLength` 属性使用。 |
| `property(int)` | 返回原始 property 值。 | 未设置时是无效 `QVariant`。 |
| `hasProperty(int)` | 判断 property 是否显式存在。 | 用于区分未设置与值恰好为默认值。 |
| `clearProperty(int)` | 删除一项显式属性。 | 删除后通常回退到上层/默认格式。 |
| `properties()` / `propertyCount()` | 取得所有属性副本或属性数。 | 用于调试、复制和通用序列化；不要依赖内部遍历顺序。 |
| `merge(const QTextFormat &other)` | 用 `other` 已存在的属性覆盖当前属性。 | 不会清除当前独有属性，不等同于赋值。 |
| `setBackground()` / `background()` / `clearBackground()` | 设置、读取或清除背景画刷。 | 背景可为颜色、渐变或纹理。 |
| `setForeground()` / `foreground()` / `clearForeground()` | 设置、读取或清除前景画刷。 | 对字符格式通常表现为文字前景色。 |
| `setLayoutDirection()` / `layoutDirection()` | 设置或读取格式级文字方向。 | 仅在格式及布局实际采用该属性时生效。 |
| `setObjectIndex()` / `objectIndex()` | 设置或读取文档对象索引。 | 文档内部关联字段，应用不应手工伪造。 |
| `setObjectType()` / `objectType()` | 设置或读取对象类型。 | 自定义文本对象需与对象接口及 property 协议一致。 |
| `boolProperty()` / `intProperty()` / `doubleProperty()` | 按目标类型读取属性。 | 属性缺失和转换失败通常得到默认转换值；先用 `hasProperty()` 区分。 |
| `stringProperty()` / `colorProperty()` / `brushProperty()` / `penProperty()` | 读取字符串、颜色、画刷或画笔属性。 | 返回的是值副本，修改副本不会回写格式。 |
| `lengthProperty()` / `lengthVectorProperty()` | 读取一个或多个 `QTextLength`。 | `QTextLength` 可为固定值、百分比或可变长度。 |
| `operator QVariant()` | 把格式包装进 `QVariant`。 | 用于模型或通用容器传递，不是文本序列化格式。 |
| `operator==` / `operator!=` | 比较格式类别和已存储属性。 | 相等不代表不同文档默认样式下的渲染完全相同。 |
| `swap(QTextFormat &other)` | 高效交换两个格式对象。 | 两个对象的格式状态整体交换。 |

## 7. 记忆重点

`QTextFormat` 是富文本的通用属性容器。检查类别用 `isXxxFormat()`，判断显式设置用 `hasProperty()`，局部覆盖用 `merge()`，精确替换用赋值；格式可跨线程传递，但把它应用到文档的操作必须回到文档所属线程。
