# QTextCursor
> Qt 6.11.1 · Qt GUI · 来自 `QTextCursor`

## 1. 先建立直觉

`QTextCursor` 是操作 `QTextDocument` 的编辑指针。它同时表示当前位置和可选区，可以插入文本、块、列表、表格、图片、frame，也可以修改字符格式、块格式和选区内容。

它是值类型。复制一个 cursor 不会复制文档，只是得到另一个指向同一文档位置的编辑句柄。

## 2. 类说明

- 头文件：`#include <QTextCursor>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：值类型，引用某个 `QTextDocument`
- 协作类：`QTextDocument`、`QTextBlock`、`QTextTable`、各种 `QText*Format`

cursor 的两个核心概念是 `position()` 和 `anchor()`。没有选区时二者相等；有选区时二者围成选择范围。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `setPosition()` / `position()` / `anchor()` | 定位和选区端点 |
| `movePosition()` | 按字符、词、行、块、文档边界移动 |
| `select()` / `hasSelection()` / `selectionStart()` / `selectionEnd()` | 创建和查询选区 |
| `selectedText()` / `selection()` | 取选区文本或片段 |
| `insertText()` / `insertHtml()` / `insertFragment()` | 插入文本、HTML、文档片段 |
| `insertBlock()` | 插入段落块 |
| `insertImage()` | 插入图片 |
| `insertList()` / `createList()` / `currentList()` | 创建或访问列表 |
| `insertTable()` / `currentTable()` | 创建或访问表格 |
| `insertFrame()` / `currentFrame()` | 创建或访问 frame |
| `removeSelectedText()` / `deleteChar()` / `deletePreviousChar()` | 删除内容 |
| `charFormat()` / `setCharFormat()` / `mergeCharFormat()` | 字符格式 |
| `blockFormat()` / `setBlockFormat()` / `mergeBlockFormat()` | 段落格式 |
| `beginEditBlock()` / `endEditBlock()` | 把多步操作合并为一个撤销命令 |

## 4. 关键用法

合并撤销步骤：

```cpp
QTextCursor c(document);
c.beginEditBlock();
c.insertText("Name: ");
c.insertText(name);
c.insertBlock();
c.endEditBlock();
```

给选区加粗：

```cpp
QTextCharFormat fmt;
fmt.setFontWeight(QFont::Bold);
cursor.mergeCharFormat(fmt);
```

`mergeCharFormat()` 只改指定属性，比 `setCharFormat()` 更适合工具栏按钮。

## 5. 使用场景

- 富文本编辑命令实现。
- 查找替换、自动补全、代码格式化。
- 插入图片、表格、列表、模板片段。
- 对选区批量应用格式。
- 构造文档生成器。

## 6. 常见坑与经验

- `selectedText()` 会用特殊段落分隔符表示换段，不一定等同于普通 `\n`。
- 插入文本会替换当前选区；不想覆盖时先清除选区或移动 cursor。
- 多步命令没有 `beginEditBlock()` 会导致用户需要撤销很多次。
- cursor 位置是文档字符位置，不是屏幕坐标；屏幕坐标要走布局或控件 API。
- 保存 cursor 跨大量编辑后要谨慎，文档变化会影响位置语义。

## 7. 知识点覆盖

本页覆盖：光标位置、选区、文本插入删除、富文本结构插入、字符/块格式、撤销合并、查找替换基础。
