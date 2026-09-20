# QTextItem 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPaintEngine>`  
> 所属模块：`Qt6::Gui`  
> 类型：绘制管线传入的轻量文本运行描述

## 1. 它解决什么问题

`QTextItem` 是 Qt 绘制后端处理一段已经整形完成的文字时使用的只读描述。`QPainter::drawTextItem()` 和 `QPaintEngine::drawTextItem()` 用它把文字、字体度量和文字装饰传给具体绘制引擎。

它解决的是“绘制后端怎样拿到一个文本运行的绘制信息”，不是富文本编辑、文档管理或字符串排版的公共入口。常规应用通常调用 `QPainter::drawText()`、`QTextLayout::draw()` 或控件绘制；只有实现、调试或包装自定义 `QPaintEngine` 时才直接处理 `QTextItem`。

## 2. 实际使用边界

`QTextItem` 没有公开构造函数，应用不能可靠地手工制造一个。Qt 在进入绘制引擎的 `drawTextItem()` 回调时传入它：

```cpp
void MyPaintEngine::drawTextItem(
    const QPointF &position,
    const QTextItem &item)
{
    const QString text = item.text();
    const QFont font = item.font();
    const qreal width = item.width();
    // Render or record this already-prepared text run.
}
```

`position` 是由调用方提供的基线位置；`ascent()` 与 `descent()` 是运行的字体度量，`width()` 是运行的水平宽度。它们不是 `QTextDocument` 的位置、块号或可编辑范围。

## 3. 渲染标志

`RenderFlags` 携带该文本运行的绘制属性：

- `RightToLeft` 表示该运行以从右到左方向绘制；
- `Overline`、`Underline`、`StrikeOut` 表示文字装饰；
- `Dummy` 仅用于标志类型的内部宽度/兼容性处理，不应作为业务渲染语义。

这些标志描述当前运行，并不会替代 `QFont`、`QTextCharFormat` 或完整双向文本算法。自定义绘制引擎应把它们视为绘制输入，而不是重新把整段字符串按字符顺序排版。

## 4. 生命周期和线程

`QTextItem` 是短生命周期的观察参数。只在当前 `drawTextItem()` 调用范围内读取它；不要缓存引用、地址或由它推导出的内部状态。

它没有 QObject 线程归属，但其来源是当前 `QPainter` / `QPaintEngine` 的绘制过程。绘制设备、painter 和 paint engine 必须按其自身线程规则使用，通常不能跨线程共享或并发调用。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `ascent()` | 返回当前文本运行在基线上方的度量。 | 适合确定基线相对的绘制范围；不是文档 y 坐标。 |
| `descent()` | 返回当前文本运行在基线下方的度量。 | 与 ascent 一起描述行内垂直范围。 |
| `width()` | 返回运行的水平绘制宽度。 | 已是排版结果，不要用 `text().size()` 代替。 |
| `text()` | 返回当前运行的字符串。 | 只描述本次绘制运行，可能不是原段落的完整文本。 |
| `font()` | 返回当前运行使用的字体副本。 | 修改副本不会改变已经整形的运行。 |
| `renderFlags()` | 返回文字方向和装饰标志。 | 应配合当前绘制位置和字体处理，不应当作编辑格式 API。 |
| `RenderFlag::RightToLeft` | 标记从右到左运行。 | 双向文本位置和字形顺序不能只按字符串下标推断。 |
| `RenderFlag::Overline` / `Underline` / `StrikeOut` | 标记上划线、下划线或删除线。 | 由具体 paint engine 将其渲染为实际装饰。 |

## 6. 记忆重点

`QTextItem` 是画笔引擎回调中的只读文本运行，不是应用层文本模型。它由 Qt 创建、在一次绘制调用内消费；日常文本绘制优先使用更高层的 `QPainter`、`QTextLayout` 或文档 API。
