# QTextList
> Qt 6.11.1 · Qt GUI · 来自 `QTextList`

## 1. 先建立直觉

`QTextList` 表示文档里的一个列表对象。列表项是若干 `QTextBlock`，列表对象负责维护它们的顺序和编号格式。列表不是独立字符串容器，而是把已有 block 组织成有序或无序列表。

## 2. 类说明

- 头文件：`#include <QTextList>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QTextBlockGroup`
- 协作类：`QTextListFormat`、`QTextCursor`、`QTextBlock`

## 3. API 速查

| API | 作用 |
| --- | --- |
| `count()` | 列表项数量 |
| `item(int)` | 返回指定项 block |
| `itemNumber(block)` | 返回 block 的序号 |
| `itemText(block)` | 返回带编号或符号的显示文本 |
| `add(block)` | 把 block 加入列表 |
| `remove(block)` / `removeItem(i)` | 移除列表项 |
| `format()` / `setFormat()` | 读取或设置列表格式 |

## 4. 关键用法

```cpp
QTextListFormat fmt;
fmt.setStyle(QTextListFormat::ListDecimal);
QTextList *list = cursor.insertList(fmt);
```

`itemText(block)` 可以得到用于导出或显示的编号前缀。

## 5. 使用场景

富文本编辑器列表功能、导出编号文本、段落加入或移出列表、多级列表基础结构。

## 6. 常见坑与经验

- 移除列表项不会删除 block，只是解除列表关系。
- 列表编号根据当前顺序生成，不要把显示编号当持久数据存储。
- 改 block 结构可能影响列表项数量和顺序。

## 7. 知识点覆盖

列表对象、block 列表项、编号文本、列表格式、加入移除列表。
