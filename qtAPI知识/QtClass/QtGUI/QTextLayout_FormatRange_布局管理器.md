# QTextLayout::FormatRange 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextLayout>`  
> 所属模块：`Qt6::Gui`  
> 类型：轻量公开结构体

## 1. 它解决什么问题

`QTextLayout::FormatRange` 表示在一段 `QTextLayout` 文本上覆盖一段 `QTextCharFormat`：从 `start` 开始、长度为 `length` 的范围采用 `format`。它专门服务于 layout 的临时排版和绘制覆盖。

常见场景：

- 自绘文本控件给搜索命中项添加背景；
- 绘制选择区、拼写错误下划线或诊断高亮；
- 为不归属 `QTextDocument` 的单段文本添加多段样式；
- 从 `QTextLayout::formats()` 读取当前临时覆盖规则。

它不是 `QTextCursor` 的选区，也不会写回文档。需要永久改变 `QTextDocument` 中字符格式时，使用 `QTextCursor::mergeCharFormat()`、`setCharFormat()` 等编辑 API。

## 2. 三个字段的语义

```cpp
QTextLayout::FormatRange range;
range.start = 7;
range.length = 4;
range.format.setBackground(Qt::yellow);
```

- `start`：范围起点，使用 layout 字符串的文本位置；
- `length`：覆盖的文本长度；
- `format`：要叠加的字符格式值。

位置按 Qt 文本位置计数，不能误当作 UTF-8 字节偏移。必须保证范围落在 `QTextLayout::text()` 的有效边界内；对空文本或零长度范围是否产生可见效果取决于调用上下文，不应用作插入格式的替代。

多个覆盖范围重叠时，最终效果取决于 layout 处理 formats 的顺序和属性合并规则。需要可预测的高亮层级时，应用应减少互相冲突的属性，或在设置前按自己的优先级整理范围。

## 3. 生命周期与线程

结构体自身是可复制值；其中 `QTextCharFormat` 也是值对象。它不持有 layout 或文档，因此可以在后台准备范围列表。

但把范围交给 `QTextLayout::setFormats()`、读取布局结果或绘制的操作，仍必须遵守该 layout 和 painter 的线程边界；不要并发修改同一个 layout 的 formats。

## API 速查表

| API / 字段 | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `start` | 覆盖范围的起始文本位置。 | 是 layout 字符串坐标，不是 UTF-8 字节偏移、像素坐标或文档块号。 |
| `length` | 覆盖范围长度。 | 与 `start` 组合后应处于布局文本有效范围。 |
| `format` | 要叠加的 `QTextCharFormat`。 | 是值副本；修改它不会自动通知已设置的 layout。 |
| `operator==` | 比较起点、长度和格式是否都相等。 | 不比较最终绘制结果或来源 layout。 |
| `operator!=` | 判断两个范围是否至少有一项不同。 | 适合容器更新和测试。 |
| `QTextLayout::setFormats()` | 把范围列表设置到 layout。 | 覆盖是临时布局状态，不修改 `QTextDocument`。 |
| `QTextLayout::formats()` | 读取 layout 当前的范围列表。 | 返回值副本；修改副本后要用 `setFormats()` 写回。 |
| `QTextLayout::clearFormats()` | 移除所有临时格式覆盖。 | 不会清除源字符串或文档中的格式。 |

## 5. 记忆重点

`FormatRange` 是“文本区间 + 临时字符格式”的简单数据结构。它服务于 `QTextLayout` 的绘制，不是编辑命令；`start` 和 `length` 永远按布局文本位置理解。
