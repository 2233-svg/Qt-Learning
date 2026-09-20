# QTextLength
> Qt 6.11.1 · Qt GUI · 来自 `QTextLength`

## 1. 先建立直觉

`QTextLength` 表示富文本布局里的长度约束。它可以是可变长度、固定像素长度，也可以是百分比长度。表格列宽、frame 宽度、图片最大宽度等都会用到它。

## 2. 类说明

- 头文件：`#include <QTextLength>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：小型值类型
- 协作类：`QTextFrameFormat`、`QTextTableFormat`、`QTextImageFormat`

它保存“类型 + 数值”，实际像素值需要结合可用宽度计算。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 默认构造 | 创建 variable length |
| `QTextLength(type, value)` | 指定长度类型和值 |
| `type()` | 返回长度类型 |
| `rawValue()` | 返回原始值 |
| `value(maximumLength)` | 按给定最大长度计算实际值 |

## 4. 类型速查

| 类型 | 含义 |
| --- | --- |
| `VariableLength` | 由布局自动决定 |
| `FixedLength` | 固定长度 |
| `PercentageLength` | 百分比长度，基于可用长度计算 |

## 5. 关键用法

```cpp
QTextLength fixed(QTextLength::FixedLength, 120);
QTextLength half(QTextLength::PercentageLength, 50);

qreal actual = half.value(800); // 400
```

表格列宽：

```cpp
format.setColumnWidthConstraints({
    QTextLength(QTextLength::FixedLength, 80),
    QTextLength(QTextLength::PercentageLength, 100)
});
```

## 6. 使用场景

- 表格列宽约束。
- frame 宽度。
- 图片最大宽度。
- 富文本导入 HTML/CSS 宽度信息。

## 7. 常见坑与经验

- 百分比不是 0 到 1，而是 0 到 100 这样的百分数值。
- `rawValue()` 不等于实际像素，百分比必须调用 `value(maximumLength)`。
- `VariableLength` 交给布局决定，适合不想固定宽度的列或容器。

## 8. 知识点覆盖

本页覆盖：固定/百分比/可变长度、实际值计算、表格列宽、frame 和图片约束。
