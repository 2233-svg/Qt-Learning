# QTextInlineObject
> Qt 6.11.1 · Qt GUI · 来自 `QTextInlineObject`

## 1. 先建立直觉

`QTextInlineObject` 表示文本流里的一个内联对象占位，比如自定义公式、标签、控件占位、特殊图标。它出现在 `QTextObjectInterface` 的绘制和尺寸计算流程里。

你通常不主动创建它，而是在自定义 inline object handler 中读取它的格式、位置和尺寸。

## 2. 类说明

- 头文件：`#include <QTextInlineObject>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：值类型句柄
- 协作类：`QTextObjectInterface`、`QTextCharFormat`、`QTextDocument`

内联对象的外观由 `QTextCharFormat::objectType()` 和 format 属性描述，尺寸由 handler 在 `intrinsicSize()` 中提供。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `isValid()` | 对象是否有效 |
| `format()` / `formatIndex()` | 读取字符格式和内部格式索引 |
| `textPosition()` | 对象在文档中的字符位置 |
| `rect()` | 对象布局矩形 |
| `width()` / `ascent()` / `descent()` | 当前尺寸度量 |
| `setWidth()` / `setAscent()` / `setDescent()` | 设置排版度量 |

## 4. 关键用法

在 handler 中绘制：

```cpp
void FormulaObject::drawObject(QPainter *p, const QRectF &rect,
                               QTextDocument *, int, const QTextFormat &format)
{
    p->drawText(rect, format.property(FormulaText).toString());
}
```

`QTextInlineObject` 常用于布局阶段调尺寸；绘制阶段 `drawObject()` 会拿到最终 rect 和 format。

## 5. 使用场景

- 文档中插入公式、mention、tag、彩色 token。
- 自定义 emoji 或图标占位。
- 富文本报表中的内联小组件占位。
- 编辑器里不可拆分的特殊对象。

## 6. 常见坑与经验

- inline object 不是 QWidget，不能直接嵌入真实控件交互。
- 尺寸不稳定会导致反复重新布局。
- `textPosition()` 是占位符位置，不是对象内部内容位置。
- format 属性要自己设计 key，避免和 Qt 内置属性冲突。

## 7. 知识点覆盖

本页覆盖：内联对象、object handler、格式属性、内联尺寸、绘制回调、文档占位符。
