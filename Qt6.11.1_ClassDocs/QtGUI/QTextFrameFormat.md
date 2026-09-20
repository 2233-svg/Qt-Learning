# QTextFrameFormat
> Qt 6.11.1 · Qt GUI · 来自 `QTextFrameFormat`

## 1. 先建立直觉

`QTextFrameFormat` 描述文档 frame 的盒模型：宽高、边框、padding、margin、位置、分页策略。root frame、普通 frame、表格都属于 frame 体系。

它很像富文本里的块级容器样式。

## 2. 类说明

- 头文件：`#include <QTextFrameFormat>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QTextFormat`
- 协作类：`QTextFrame`、`QTextTableFormat`

frame format 影响容器外观和布局，不影响容器内部字符的字体颜色。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `setWidth()` / `width()` | frame 宽度，支持 `QTextLength` |
| `setHeight()` / `height()` | frame 高度 |
| `setBorder()` / `border()` | 边框宽度 |
| `setBorderBrush()` / `borderBrush()` | 边框画刷 |
| `setBorderStyle()` / `borderStyle()` | 边框样式 |
| `setPadding()` / `padding()` | 内边距 |
| `setMargin()` / `margin()` | 统一外边距 |
| `setTopMargin()` 等 | 单边外边距 |
| `setPosition()` / `position()` | inline、float left/right 等位置 |
| `setPageBreakPolicy()` | 分页控制 |

## 4. 关键用法

插入带边框 frame：

```cpp
QTextFrameFormat ff;
ff.setBorder(1);
ff.setPadding(8);
ff.setMargin(6);
cursor.insertFrame(ff);
```

百分比宽度：

```cpp
ff.setWidth(QTextLength(QTextLength::PercentageLength, 80));
```

## 5. 使用场景

- 富文本中的引用框、提示框、侧栏。
- 报表和打印中的分组容器。
- 表格格式的基础盒模型。
- HTML 导入导出的容器样式。

## 6. 常见坑与经验

- margin 在 frame 外，padding 在内容和边框之间。
- 百分比宽度依赖父 frame 或页面宽度。
- 浮动 frame 对布局影响较复杂，打印前要检查实际效果。
- 表格是特殊 frame，表格专属属性在 `QTextTableFormat`。

## 7. 知识点覆盖

本页覆盖：frame 盒模型、边框、内外边距、宽高、浮动位置、分页控制、容器样式。
