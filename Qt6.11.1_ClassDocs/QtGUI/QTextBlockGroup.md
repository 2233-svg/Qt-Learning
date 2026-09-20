# QTextBlockGroup
> Qt 6.11.1 · Qt GUI · 来自 `QTextBlockGroup`

## 1. 先建立直觉

`QTextBlockGroup` 是一组 `QTextBlock` 的抽象基类。最常见具体类是 `QTextList`。它提供 block 加入、移除、格式变化时的回调入口。

## 2. 类说明

- 头文件：`#include <QTextBlockGroup>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QTextObject`
- 直接常见子类：`QTextList`

普通应用很少直接使用它，更多是理解列表如何管理多个 block。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `blockList()` | 返回组内 block 列表 |
| `blockInserted(block)` | block 加入时的虚函数回调 |
| `blockRemoved(block)` | block 移除时的虚函数回调 |
| `blockFormatChanged(block)` | block 格式变化时的虚函数回调 |

## 4. 关键用法

多数场景直接使用 `QTextList`：

```cpp
QTextList *list = cursor.currentList();
auto blocks = list ? list->blockList() : QList<QTextBlock>{};
```

## 5. 使用场景

理解 `QTextList` 的实现模型、文档结构调试、扩展 Qt 文本对象时观察 block 变化。

## 6. 常见坑与经验

- 不要把它当通用容器用；它属于文档对象系统。
- `blockList()` 返回的是当前组内 block，文档修改后需要重新读取。
- 直接子类化需求很少，优先使用现有 list/table/frame。

## 7. 知识点覆盖

block group、列表基础、文档对象回调、block 集合管理。
