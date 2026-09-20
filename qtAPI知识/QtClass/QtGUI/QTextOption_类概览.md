# QTextOption 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextOption>`  
> 所属模块：`Qt6::Gui`  
> 类型：可复制文本布局选项值

## 1. 它解决什么问题

`QTextOption` 为 `QTextLayout` 或 `QTextDocument` 提供段落级通用布局策略：对齐、文字方向、换行方式、制表位、可视化控制符以及设计度量。它不保存文本和格式范围，只描述排版时应采用的规则。

实际场景：

- 自绘文本设置自动换行、断词和对齐；
- 编辑器在“显示空白字符”模式下显示 Tab、段落分隔符和默认不可见字符；
- 日志或代码视图设置固定 Tab 宽度或自定义对齐制表位；
- 为需要稳定度量的打印或导出布局选择设计度量。

## 2. 换行、方向和对齐

`WrapMode` 的选择：

| 模式 | 语义 |
| --- | --- |
| `NoWrap` | 不自动换行。 |
| `WordWrap` | 优先在单词边界换行。 |
| `ManualWrap` | 只按显式换行符断行。 |
| `WrapAnywhere` | 可在任意字符边界换行。 |
| `WrapAtWordBoundaryOrAnywhere` | 优先单词边界，必要时任意位置换行。 |

`setAlignment()` 控制段落在可用行宽中的对齐，`setTextDirection()` 指定布局方向。两者不会改变字符串字符顺序；双向文本的字形顺序、光标移动仍由文本布局算法处理。

## 3. Tab、空白显示和度量

`setTabStopDistance()` 设置重复的固定间距；`setTabArray()` 提供一组传统固定位置；`setTabs()` 使用 `QTextOption::Tab` 表达左、右、居中或分隔符对齐。项目中应选择一套明确策略，不要混合多种 Tab 配置并期待它们简单拼接。

`Flags` 主要服务于编辑器和调试显示：

- `ShowTabsAndSpaces`、`ShowLineAndParagraphSeparators`、`ShowDocumentTerminator` 显示控制字符；
- `ShowDefaultIgnorables` 显示默认不可见 Unicode 字符；
- `IncludeTrailingSpaces` 让末尾空格计入布局相关范围；
- `SuppressColors` 抑制颜色格式；
- `DisableEmojiParsing` 禁用 emoji 解析路径。

这些选项可能影响可见结果与度量，特别是用于截图测试或精确命中时应保持一致。

`useDesignMetrics` 使用字体设计度量而非设备相关度量。适合需要稳定排版比较的场景，但不能和实时屏幕像素度量混为一谈。

## 4. 生命周期和线程

`QTextOption` 是可复制值，不持有 layout、document 或 paint device。可在后台准备副本；把它设置进已有 `QTextLayout` / `QTextDocument` 并触发布局时必须回到对应对象所属线程。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextOption()` | 创建默认文本选项。 | 默认值依版本/布局语境解释；关键策略应显式设置。 |
| `QTextOption(Qt::Alignment)` | 以对齐方式创建选项。 | 只初始化对齐意图，其他选项仍应按需设置。 |
| `setAlignment()` / `alignment()` | 设置或读取行内对齐。 | 不改变字符串内容或文字方向。 |
| `setTextDirection()` / `textDirection()` | 设置或读取段落布局方向。 | 不替代完整 BiDi 算法。 |
| `setWrapMode()` / `wrapMode()` | 设置或读取自动换行策略。 | 改变后需重新布局。 |
| `setFlags()` / `flags()` | 设置或读取控制字符与渲染标志。 | 多个值按 `Flags` 组合；可能改变可见结果和度量。 |
| `setTabStopDistance()` / `tabStopDistance()` | 设置或读取重复 Tab 间隔。 | 使用逻辑排版单位，不是固定设备像素保证。 |
| `setTabArray()` / `tabArray()` | 设置或读取固定 Tab 位置数组。 | 遗留式简单位置列表；与复杂 `Tab` 规则混用前要验证结果。 |
| `setTabs()` / `tabs()` | 设置或读取带类型的制表位。 | `QTextOption::Tab` 支持右、居中和分隔符对齐。 |
| `setUseDesignMetrics()` / `useDesignMetrics()` | 开关设计度量。 | 同一文档/布局生命周期内应保持一致。 |
| `WrapMode` | 定义不换行、按词、仅手动、任意位置或混合换行。 | 选择影响视觉行、大小和命中测试。 |
| `Flag::ShowTabsAndSpaces` | 显示 Tab 和空格标记。 | 通常用于编辑器调试视图。 |
| `Flag::ShowLineAndParagraphSeparators` | 显示行/段落分隔符。 | 可与额外显示空间标志配合。 |
| `Flag::SuppressColors` | 抑制颜色格式。 | 常用于统一或诊断式绘制。 |
| `Flag::ShowDocumentTerminator` / `ShowDefaultIgnorables` | 显示文档结束符或默认不可见字符。 | 改变编辑器可视反馈。 |
| `Flag::DisableEmojiParsing` | 禁用 emoji 解析。 | 应作为明确的排版兼容性策略使用。 |
| `Flag::IncludeTrailingSpaces` | 将行末空格纳入布局相关计算。 | 可能改变选择、宽度或可视化边界。 |

## 5. 记忆重点

`QTextOption` 是文本布局策略集合。换行、方向、对齐和 Tab 必须作为一组规则理解；空白显示与设计度量也会改变最终可见结果，设置到 layout 后要重新布局。
