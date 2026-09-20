# Qt QAbstractTextDocumentLayout::PaintContext 深入笔记

> 适用版本：Qt 6.11.1  
> 所属类：`QAbstractTextDocumentLayout`  
> 定义位置：`#include <QAbstractTextDocumentLayout>`  
> 定位：一次文档绘制请求的上下文值对象

## 1. 它解决什么问题

`QAbstractTextDocumentLayout::PaintContext` 把绘制时的临时状态集中传给布局。布局不必从控件、光标和调色板对象中读取隐含状态，而是接收一份明确的绘制上下文：

- 当前应显示的光标位置；
- 当前使用的调色板；
- 可以用来减少计算的文档区域；
- 本次绘制需要显示的选区集合。

它不是文档状态，也不是布局缓存。修改 `PaintContext` 只影响这一次 `draw()` 调用，不会改变 `QTextDocument` 中的字符格式、光标或选区。

## 2. 最小使用方式

```cpp
QAbstractTextDocumentLayout::PaintContext context;
context.cursorPosition = cursor.position();
context.palette = widget->palette();
context.clip = exposedDocumentRect;

QAbstractTextDocumentLayout::Selection selection;
selection.cursor = cursor;
selection.format.setBackground(Qt::yellow);
context.selections.append(selection);

layout->draw(painter, context);
```

`clip` 和 `Selection::cursor` 都必须使用布局所理解的文档坐标/文档位置。视图若有滚动和缩放，应在调用布局前通过 painter transform 或坐标映射保持约定一致。

## 3. 默认值与生命周期

默认构造函数把 `cursorPosition` 初始化为 `-1`，把 `selections` 初始化为空；`palette` 使用其默认构造状态，`clip` 也是默认空矩形。

这些默认值有明确含义：

- `cursorPosition == -1`：本次不要求布局绘制文本光标；
- 空 `selections`：没有额外的选区高亮；
- 空 `clip`：没有提供有效的裁剪优化提示，不能简单等价为“文档不可见”；
- 默认 `palette`：由布局和调用者约定如何解释，不能假定一定等于某个控件调色板。

`PaintContext` 是值类型，可以在栈上创建、复制和作为临时值传递。它不拥有光标关联的文档、调色板资源或 painter。

## 4. 成员逐项说明

### `int cursorPosition`

要绘制的文本光标位置，默认值为 `-1`。它是 `QTextDocument` 中的字符位置，不是像素坐标，也不是 `QTextCursor` 对象。

边界：

- `-1` 通常表示不绘制光标；
- 非负值应位于关联文档允许的字符位置范围内；
- 光标位置位于文档末尾时，布局应按自己的插入光标规则计算；
- 如果文档正在变化，位置必须在本次绘制前重新取得，不能长期保存旧位置；
- 是否显示光标、光标宽度和闪烁由布局/控件约定，`PaintContext` 只传位置。

### `QPalette palette`

绘制使用的颜色和角色集合。布局可以用它选择文本、背景、链接、选中状态和禁用状态的颜色。

它是值成员，不是外部 `QPalette` 的引用。调用者可以传入控件调色板，也可以为打印、导出图片或暗色主题构造独立调色板。

不要假设 palette 的某个角色一定有高对比度，也不要仅凭 palette 判断当前是否为选中状态；选区是否存在由 `selections` 描述。

### `QRectF clip`

可选的文档坐标矩形，用于提示布局只需要计算或绘制该区域附近的内容。它主要用于性能优化，不自动设置 `QPainter` 的裁剪区域。

使用时要注意：

- `clip` 的坐标必须与 `draw()` 的文档坐标约定一致；
- painter 自身的 `setClipRect()` 仍然决定实际像素裁剪；
- 空矩形不应直接当作“没有任何内容可画”；
- 布局可以保守地绘制比 clip 更大的区域，但不能漏掉实际需要更新的内容；
- 如果视图发生滚动，不能把视口坐标未经转换直接填入 clip。

### `QList<Selection> selections`

本次绘制要使用的选区描述列表。每个选区包含一个 `QTextCursor` 范围和一个覆盖样式。

列表中的 cursor 只借用它所关联的文档；虽然 `PaintContext` 是值类型，但复制 cursor 不会让被关联的 `QTextDocument` 延长生命周期。文档销毁后，不能继续用包含旧 cursor 的上下文。

多个选区可以重叠。重叠时谁覆盖谁、是否合并背景、文本颜色如何处理由具体布局实现决定；调用者不应依赖未文档化的绘制顺序。若需要确定视觉效果，应用应整理范围并避免不必要的重叠。

## 5. 与 `QAbstractTextDocumentLayout::draw()` 的关系

`PaintContext` 只描述输入，布局仍然负责：

1. 根据 cursor 位置找到插入光标几何；
2. 根据每个选区的 cursor 计算字符范围；
3. 把选区格式叠加到文档格式上；
4. 使用 palette 绘制文本、背景、链接和对象；
5. 根据 clip 跳过明显不需要绘制的块；
6. 遵守 painter 当前的变换和裁剪。

选区格式不会写回文档。比如设置 `format.setBackground(Qt::yellow)` 只会让这次绘制的选区看起来有黄色背景，不会改变 `QTextCursor` 所覆盖文字的永久格式。

## API 速查表

| 成员 | 类型 | 作用 | 默认/边界 |
| --- | --- | --- | --- |
| 构造 | `PaintContext()` | 创建一次绘制上下文。 | `cursorPosition = -1`，选区为空，clip 为空。 |
| 光标 | `cursorPosition` | 指定文本光标的文档位置。 | `-1` 表示不绘制；不是像素坐标。 |
| 颜色 | `palette` | 指定绘制使用的颜色角色。 | 值成员；可用控件或打印专用 palette。 |
| 优化 | `clip` | 提示需要关注的文档矩形。 | 不替代 painter clip；空矩形不能直接等同于无内容。 |
| 高亮 | `selections` | 指定本次绘制的选区列表。 | 不修改文档；cursor 关联文档必须有效。 |

### 一句话总结

`PaintContext` 是一次绘制的“输入快照”：它传递光标、颜色、可见区域提示和临时选区，但不拥有文档、不改变永久格式，也不代替 painter 的实际裁剪状态。
