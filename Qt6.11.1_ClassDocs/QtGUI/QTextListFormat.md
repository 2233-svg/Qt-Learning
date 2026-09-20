# QTextListFormat
> Qt 6.11.1 · Qt GUI · 来自 `QTextListFormat`

## 1. 先建立直觉

`QTextListFormat` 描述列表的编号或项目符号样式、缩进、编号前后缀等。它作用在 `QTextList` 上，列表中的每一项本质上仍然是 `QTextBlock`。

## 2. 类说明

- 头文件：`#include <QTextListFormat>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QTextFormat`
- 协作类：`QTextList`、`QTextCursor`

列表样式和段落缩进相关，但它不是普通 `QTextBlockFormat`。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `setStyle()` / `style()` | 设置项目符号或编号样式 |
| `setIndent()` / `indent()` | 列表缩进层级 |
| `setNumberPrefix()` / `numberPrefix()` | 编号前缀 |
| `setNumberSuffix()` / `numberSuffix()` | 编号后缀 |

## 4. 样式速查

| 样式 | 说明 |
| --- | --- |
| `ListDisc` / `ListCircle` / `ListSquare` | 无序列表符号 |
| `ListDecimal` | 1, 2, 3 |
| `ListLowerAlpha` / `ListUpperAlpha` | a, b 或 A, B |
| `ListLowerRoman` / `ListUpperRoman` | 罗马数字 |

## 5. 关键用法

```cpp
QTextListFormat lf;
lf.setStyle(QTextListFormat::ListDecimal);
lf.setIndent(1);
cursor.insertList(lf);
```

自定义编号外观：

```cpp
lf.setNumberPrefix("[");
lf.setNumberSuffix("]");
```

## 6. 使用场景

- Markdown/HTML 列表导入。
- 富文本编辑器的有序/无序列表按钮。
- 报表条目编号。
- 多级列表缩进。

## 7. 常见坑与经验

- 列表项是 block，移动、删除、合并段落都会影响列表结构。
- 缩进层级影响视觉缩进，不等同于嵌套数据结构。
- 列表编号样式不是纯文本，导出纯文本时格式会丢失或被转换。

## 8. 知识点覆盖

本页覆盖：列表样式、编号前后缀、缩进层级、block 和 list 的关系、有序无序列表。
