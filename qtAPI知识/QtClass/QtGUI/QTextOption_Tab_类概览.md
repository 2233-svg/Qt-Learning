# QTextOption::Tab 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextOption>`  
> 所属模块：`Qt6::Gui`  
> 类型：轻量制表位描述结构体

## 1. 它解决什么问题

`QTextOption::Tab` 描述一个带对齐规则的制表位。相较于只给出一串位置的 `tabArray`，它还能表示右对齐、居中对齐，以及按某个分隔符对齐，因此适合金额列、键值列表和简易表格式文本。

它只描述 Tab 的位置与对齐方式，不会插入 `\t` 字符，也不会自动给段落设置 Tab 规则。把它放入列表后，需要用 `QTextOption::setTabs()` 应用到 `QTextLayout` 或文档文本选项。

## 2. 字段和对齐方式

```cpp
QTextOption::Tab amountTab(
    240, QTextOption::DelimiterTab, QChar('.'));
option.setTabs({ amountTab });
```

- `position`：制表位的逻辑位置；
- `type`：`LeftTab`、`RightTab`、`CenterTab` 或 `DelimiterTab`；
- `delimiter`：仅分隔符对齐需要的分隔字符，例如 `.` 或 `:`。

默认构造得到的位置是 `80`，类型是 `LeftTab`，`delimiter` 为空字符。这个 `80` 是默认逻辑位置，不是“80 个空格”或固定设备像素。

`DelimiterTab` 需要文本中实际存在可匹配的分隔符才有可见的特殊对齐效果；没有该字符时，不应假定会产生右对齐或居中对齐的替代行为。

## 3. 生命周期和线程

它是纯值结构体，可复制、可放入 `QList`、可在任何线程准备。应用到文档或 layout 时，仍必须在目标对象所属线程完成。

## API 速查表

| API / 字段 | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `Tab()` | 创建默认制表位。 | `position = 80`，`type = LeftTab`，分隔符为空。 |
| `Tab(qreal pos, TabType type, QChar delimiter = {})` | 以位置、对齐类型和可选分隔符创建。 | delimiter 主要用于 `DelimiterTab`。 |
| `position` | 制表位的逻辑位置。 | 单位由当前文本布局决定，不等于字符列数。 |
| `type` | 制表位的对齐策略。 | `LeftTab`、`RightTab`、`CenterTab`、`DelimiterTab` 语义不同。 |
| `delimiter` | 分隔符对齐所查找的字符。 | 非 `DelimiterTab` 时通常没有作用。 |
| `operator==` | 比较位置、类型和分隔符。 | position 使用 Qt 的模糊浮点比较。 |
| `operator!=` | 判断至少一个字段不同。 | 适合更新检测或测试。 |
| `QTextOption::setTabs()` | 将 Tab 列表应用为布局规则。 | 需设置到目标 layout/document 后重新布局。 |

## 4. 记忆重点

`QTextOption::Tab` 是“位置 + 对齐规则 + 可选分隔符”。它最适合结构化文本的列对齐；默认 `80` 只是逻辑位置，实际效果还取决于 `QTextOption`、文本内容和当前布局宽度。
