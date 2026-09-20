# QTextFrameFormat 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextFrameFormat>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QTextFormat`

## 1. 它解决什么问题

`QTextFrameFormat` 描述 `QTextFrame` 的几何与装饰：框架在文本流中的位置、边框、外边距、内边距、宽高和分页策略。它只是一份可复制的格式值，不创建框架，也不负责绘制或装载内容。

适用场景：

- 插入带浅色背景、边框和内边距的富文本提示框；
- 为文档根框架调整整体页边距或可用宽度；
- 为 HTML / Markdown 导入后得到的框架检查浮动、边框或分页属性；
- 给打印文档中的结构段落设定尺寸约束。

## 2. 三层空间不能混淆

```text
outside text flow
  margin | border | padding | frame content
```

- `margin`：框架外侧与周边文档内容的间隔；
- `border`：边框的宽度、画刷与线型；
- `padding`：边框内侧到框架内容的间隔。

`setMargin()` 写入统一外边距；之后通过 `setTopMargin()`、`setLeftMargin()` 等设置单侧值时，布局会以单侧属性为准。读取单侧边距时不要假定它总是与 `margin()` 相同。

## 3. 尺寸、浮动和分页

`width()` / `height()` 返回 `QTextLength`，因此尺寸可以是 `FixedLength`、`PercentageLength` 或由布局决定的 `VariableLength`。`setWidth(qreal)` 和 `setHeight(qreal)` 是固定长度便捷重载；要表达百分比或可变尺寸，传入 `QTextLength`。

格式只是约束或请求，最终几何由文档布局、页面大小、内容和可用宽度共同决定。`InFlow` 表示普通文本流，`FloatLeft` / `FloatRight` 允许后续文本环绕；浮动不是 QWidget 的绝对定位。

`setPageBreakPolicy()` 使用 `QTextFormat::PageBreakFlags` 设置分页偏好。`PageBreak_AlwaysBefore`、`PageBreak_AlwaysAfter` 可组合，但实际分页仍受布局和输出设备限制。

## 4. 应用到文档

```cpp
QTextFrameFormat note;
note.setBackground(QColor("#f6fbff"));
note.setBorder(1.0);
note.setBorderBrush(QColor("#7da7c7"));
note.setBorderStyle(QTextFrameFormat::BorderStyle_Solid);
note.setPadding(8.0);
note.setWidth(QTextLength(QTextLength::PercentageLength, 100));

QTextFrame *frame = cursor.insertFrame(note);
```

从已有框架读取格式后，必须写回才会生效：

```cpp
QTextFrameFormat current = frame->frameFormat();
current.setBottomMargin(12.0);
frame->setFrameFormat(current);
```

## 5. 线程和生命周期

本类是值类型，独立创建和复制没有 QObject 所有权问题。它被用于某个 `QTextFrame` 或 `QTextDocument` 后，写回操作必须在文档所属线程执行。`QTextFrameFormat` 不持有 `QTextFrame *`、图像或任何文档资源。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextFrameFormat()` | 创建框架格式值。 | 初始属性主要由布局默认值解释，不能把未设置视为固定像素值。 |
| `isValid()` | 判断是否为框架格式类别。 | 不表示边框、尺寸或边距已设置。 |
| `setPosition(Position)` / `position()` | 设置或读取 `InFlow`、`FloatLeft`、`FloatRight`。 | 是文本流策略，不是绝对坐标。 |
| `setBorder(qreal)` / `border()` | 设置或读取边框宽度。 | 宽度不等同于 padding 或 margin。 |
| `setBorderBrush()` / `borderBrush()` | 设置或读取边框画刷。 | 画刷可为颜色、渐变或纹理。 |
| `setBorderStyle()` / `borderStyle()` | 设置或读取边框线型。 | `BorderStyle_None` 可使边框不可见，即使仍保存了宽度或画刷。 |
| `setMargin(qreal)` / `margin()` | 设置或读取统一外边距。 | 单侧属性会形成更具体的覆盖。 |
| `setTopMargin()` / `topMargin()` | 设置或读取上外边距。 | 是逻辑排版长度，不是设备像素保证。 |
| `setBottomMargin()` / `bottomMargin()` | 设置或读取下外边距。 | 影响后续内容与框架的距离。 |
| `setLeftMargin()` / `leftMargin()` | 设置或读取左外边距。 | 书写方向和布局仍可能影响最终视觉位置。 |
| `setRightMargin()` / `rightMargin()` | 设置或读取右外边距。 | 不应和浮动方向混为一谈。 |
| `setPadding(qreal)` / `padding()` | 设置或读取边框内边距。 | 为内容留出内部空间，不改变文本内容。 |
| `setWidth(qreal)` | 设置固定宽度。 | 等价于写入 `FixedLength` 的 `QTextLength`。 |
| `setWidth(const QTextLength &)` / `width()` | 设置或读取可变、固定或百分比宽度。 | 百分比的基准由布局可用宽度决定。 |
| `setHeight(qreal)` | 设置固定高度。 | 等价于固定长度 `QTextLength`。 |
| `setHeight(const QTextLength &)` / `height()` | 设置或读取可变、固定或百分比高度。 | 内容、分页与布局可能限制最终结果。 |
| `setPageBreakPolicy(PageBreakFlags)` / `pageBreakPolicy()` | 设置或读取框架前后分页策略。 | 是布局请求；不要假定所有输出设备产生相同分页。 |
| `BorderStyle` | 指定无边框、点线、虚线、实线、双线及凹凸效果。 | 选择由当前文档布局的渲染支持决定。 |
| `Position` | 指定普通流、左浮动或右浮动。 | 浮动不提供固定 x/y 坐标。 |

## 7. 记忆重点

`QTextFrameFormat` 只描述框架。先区分 margin、border、padding，再选择 `QTextLength` 的固定或百分比语义；它必须通过 `QTextFrame::setFrameFormat()` 或 `QTextCursor::insertFrame()` 写入文档才会参与布局。
