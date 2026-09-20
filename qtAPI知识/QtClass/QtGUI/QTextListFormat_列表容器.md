# QTextListFormat 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextListFormat>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QTextFormat`

## 1. 它解决什么问题

`QTextListFormat` 描述 `QTextList` 的编号或项目符号规则：样式、逻辑缩进、编号前缀、编号后缀和起始编号。它只描述规则，不保存列表项目，也不负责给块插入或删除文本。

适用场景：

- 用 `ListDisc`、`ListDecimal`、字母或罗马数字生成不同层级的列表；
- 把 `1.` 变成 `(1)`、`Step 1:` 等标签风格；
- 让序号从业务要求的数字而非默认首项开始；
- 创建或更新 `QTextList` 前准备一个可复制的格式值。

## 2. 样式、前后缀和编号不是同一件事

`Style` 决定核心标签类型：

| 样式 | 典型效果 |
| --- | --- |
| `ListDisc` / `ListCircle` / `ListSquare` | 实心圆、空心圆、方块项目符号。 |
| `ListDecimal` | 十进制编号。 |
| `ListLowerAlpha` / `ListUpperAlpha` | 小写 / 大写拉丁字母编号。 |
| `ListLowerRoman` / `ListUpperRoman` | 小写 / 大写罗马数字编号。 |
| `ListStyleUndefined` | 未明确指定样式。 |

`numberPrefix()` 和 `numberSuffix()` 包裹编号，例如前缀为 `(`、后缀为 `)` 得到 `(1)`。它们通常只对编号样式有可见意义；给项目符号设置前后缀不应被当作可移植的显示保证。

`start()` / `setStart()` 从 Qt 6.6 起可设置起始编号。它影响列表标签的起点，不是第一个块的文档位置，也不会重排已有正文内容。

## 3. 缩进的边界

`indent()` 是逻辑缩进级别，通常与 `QTextDocument::indentWidth()` 配合形成最终距离。不要传入像素宽度，也不要把它当作 `QTextBlockFormat::leftMargin()` 的替代。

列表嵌套时，格式缩进、块归属和父列表关系共同决定最终层级。仅增大格式 `indent` 不一定会自动把块变成另一份列表的子项；结构调整仍通过 `QTextCursor` 和 `QTextList` 完成。

## 4. 生命周期和线程

这是可复制的值类型，不拥有 `QTextList` 或 `QTextDocument`。可以离线准备、复制和比较。把它用于 `cursor.insertList()` 或 `list->setFormat()` 时，必须在目标文档所属线程执行。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextListFormat()` | 创建列表格式值。 | 初始值未必代表业务想要的标签样式，应显式设置。 |
| `isValid()` | 判断是否为列表格式类别。 | 不表示已选定具体列表样式。 |
| `setStyle(Style)` / `style()` | 设置或读取项目符号/编号样式。 | `ListStyleUndefined` 表示未明确样式。 |
| `setIndent(int)` / `indent()` | 设置或读取逻辑列表缩进级别。 | 不是像素距离，最终距离取决于文档与布局。 |
| `setNumberPrefix()` / `numberPrefix()` | 设置或读取编号前缀。 | 通常配合编号样式使用。 |
| `setNumberSuffix()` / `numberSuffix()` | 设置或读取编号后缀。 | 不修改项目正文。 |
| `setStart(int)` / `start()` | 设置或读取起始编号。 | Qt 6.6 起；不是项目索引或文档位置。 |
| `Style::ListDisc` / `ListCircle` / `ListSquare` | 选择三类项目符号。 | 标签绘制由文档布局决定。 |
| `Style::ListDecimal` | 选择十进制编号。 | 可与 prefix/suffix 组合。 |
| `Style::ListLowerAlpha` / `ListUpperAlpha` | 选择字母编号。 | 标签规则由 Qt 富文本布局实现。 |
| `Style::ListLowerRoman` / `ListUpperRoman` | 选择罗马数字编号。 | 编号范围很大时应验证业务显示需求。 |

## 5. 记忆重点

`QTextListFormat` 是列表标签规则，而不是列表结构。样式决定编号类型，前后缀装饰标签，`start` 决定编号起点，`indent` 只是逻辑级别；真正的项目归属由 `QTextList` 和文档编辑操作决定。
