# QTextInlineObject 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextInlineObject>`  
> 所属模块：`Qt6::Gui`  
> 类型：由文本布局提供的轻量句柄

## 1. 它解决什么问题

`QTextInlineObject` 表示一行文本中一个内联对象的排版槽位。它让自定义文本对象处理器能查询对象的格式、文本位置和文字方向，并在布局阶段报告对象占用的宽度、上行高度和下行高度。

它最常见于 `QTextObjectInterface::resize()`：应用不直接创建和插入 `QTextInlineObject`，而是 Qt 在文档布局调用自定义对象处理器时传入它。处理器据此决定公式、徽章、附件占位符或其他 `UserObject` 应在文字行中占多大空间。

它不是 QWidget，也不是一个可长期缓存的图元。绘制由 `QTextObjectInterface::drawObject()` 结合 `rect()` 完成。

## 2. 自定义对象中的典型使用

```cpp
void FormulaRenderer::resize(
    QTextDocument *,
    int,
    const QTextFormat &,
    QTextInlineObject &object)
{
    object.setWidth(42);
    object.setAscent(16);
    object.setDescent(5);
}
```

高度由 `ascent() + descent()` 构成。把高度全部放进 ascent 会让对象底部与正文基线关系失真；把它全部放进 descent 又会把正文行向下撑开。应按对象相对基线的真实视觉需求分配两部分。

`rect()` 代表布局为内联对象计算的区域。自定义绘制时使用 Qt 提供的 rect 和 painter，而不要从 `textPosition()` 自行猜测像素坐标。

## 3. 格式、位置和方向

- `textPosition()` 是对象在所在文本布局中的字符位置，不是文档块号或像素 x 坐标；
- `formatIndex()` 是内部格式表索引，只适合当前布局/文档上下文，不能当持久化 ID；
- `format()` 返回格式副本，通常可用 `objectType()` 和自定义 property 判断要绘制什么；
- `textDirection()` 给出对象位置的布局方向，双向文本绘制不能只假定从左到右。

## 4. 有效性、生命周期和线程

默认构造对象无效，`isValid()` 为 `false`。实用对象只由 `QTextLayout` / 文档布局在回调期间提供；当布局被清除、文本或格式改变、文档销毁后，旧句柄不应继续使用。

不要把 `QTextInlineObject` 保存到成员变量、跨事件循环排队使用或传给工作线程。若要缓存，请保存可重建的业务数据和格式 key；下一次布局时从新的回调参数重新计算尺寸。自定义对象的布局和绘制回调应在文档所属线程执行。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextInlineObject()` | 创建无效句柄。 | 不能作为独立内联对象插入或布局。 |
| `isValid()` | 判断是否关联有效文本布局。 | 有效性不跨越布局重建或文档销毁。 |
| `rect()` | 返回对象的布局矩形。 | 使用它绘制；不要用字符位置推导像素坐标。 |
| `width()` / `setWidth(qreal)` | 读取或设置对象占用宽度。 | 通常只在 `resize()` 回调中设置。 |
| `ascent()` / `setAscent(qreal)` | 读取或设置基线上方高度。 | 与 descent 一起决定行高和基线对齐。 |
| `descent()` / `setDescent(qreal)` | 读取或设置基线下方高度。 | 不是总高度；总高度约为 ascent 加 descent。 |
| `height()` | 返回当前对象高度。 | 由布局数据计算，通常反映 ascent 与 descent 的组合。 |
| `textDirection()` | 返回对象位置的文字方向。 | 双向文本绘制、锚点和左右边界应考虑该值。 |
| `textPosition()` | 返回对象的文本位置。 | 是文本坐标，不是像素坐标或稳定业务编号。 |
| `formatIndex()` | 返回内部格式索引。 | 仅在当前文档/布局生命周期内有意义。 |
| `format()` | 返回关联对象格式副本。 | 修改返回格式不会回写文档；用其读取 `objectType` 或自定义属性。 |

## 6. 记忆重点

`QTextInlineObject` 是布局回调中短暂存在的内联占位槽。在 `resize()` 用宽度、ascent、descent 报告几何，在 `drawObject()` 用布局给出的矩形绘制；它不拥有内容，也不能脱离当前布局长期保存。
