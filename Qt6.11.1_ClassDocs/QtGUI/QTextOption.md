# QTextOption
> Qt 6.11.1 · Qt GUI · 来自 `QTextOption`

## 1. 先建立直觉

`QTextOption` 描述文本排版选项：对齐方式、换行模式、文本方向、tab stop、是否显示空白字符、是否使用设计度量等。它经常作为 `QTextDocument` 默认选项或 `QTextLayout` 的排版选项使用。

## 2. 类说明

- 头文件：`#include <QTextOption>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：值类型
- 协作类：`QTextDocument`、`QTextLayout`

它不保存文本，也不保存字体，只控制排版规则。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `setAlignment()` / `alignment()` | 文本对齐 |
| `setWrapMode()` / `wrapMode()` | 换行策略 |
| `setTextDirection()` / `textDirection()` | LTR/RTL/自动方向 |
| `setTabStopDistance()` / `tabStopDistance()` | 默认 tab 宽度 |
| `setTabs()` / `tabs()` | 自定义 tab 数组 |
| `setFlags()` / `flags()` | 控制显示 tab/space、include trailing spaces 等 |
| `setUseDesignMetrics()` / `useDesignMetrics()` | 是否使用字体设计度量 |

## 4. 换行与标志速查

| API/枚举 | 说明 |
| --- | --- |
| `NoWrap` | 不自动换行 |
| `WordWrap` | 单词边界换行 |
| `ManualWrap` | 只按显式换行 |
| `WrapAnywhere` | 任意位置可换行 |
| `WrapAtWordBoundaryOrAnywhere` | 优先单词边界，不行再任意 |
| `ShowTabsAndSpaces` | 显示 tab 和空格标记 |
| `ShowLineAndParagraphSeparators` | 显示换行和段落分隔符 |
| `IncludeTrailingSpaces` | 布局宽度包含行尾空白 |

## 5. 关键用法

代码编辑器常用：

```cpp
QTextOption opt;
opt.setWrapMode(QTextOption::NoWrap);
opt.setTabStopDistance(fontMetrics.horizontalAdvance(' ') * 4);
document->setDefaultTextOption(opt);
```

自绘布局：

```cpp
QTextLayout layout(text, font);
layout.setTextOption(opt);
```

## 6. 使用场景

- 控制 QTextDocument 默认换行和 tab。
- 自绘文本布局。
- 代码编辑器显示空白字符。
- RTL 文本和混合方向文本。
- 打印时控制 trailing spaces 是否计入宽度。

## 7. 常见坑与经验

- tab stop distance 是设备无关坐标中的距离，不是字符数量。
- `NoWrap` 可能让文档理想宽度很大，滚动区域要配合处理。
- 显示空白字符通常用于编辑器，不适合普通富文本阅读。
- `useDesignMetrics` 会影响排版一致性和实际显示度量，跨设备排版时才特别关注。

## 8. 知识点覆盖

本页覆盖：文本对齐、换行模式、tab stop、RTL、空白显示、设计度量、文档和布局选项。
