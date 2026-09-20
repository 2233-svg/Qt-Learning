# QTextFrame::iterator
> Qt 6.11.1 · Qt GUI · 来自 `QTextFrame::iterator`

## 1. 先建立直觉

`QTextFrame::iterator` 用来遍历一个 frame 的直接内容。每一步要么是一个 `QTextBlock`，要么是一个子 `QTextFrame`。这比单纯遍历文档 block 更能保留富文本结构。

## 2. 类说明

- 头文件：`#include <QTextFrame>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：迭代器值类型
- 来源：`QTextFrame::begin()`、`QTextFrame::end()`

## 3. API 速查

| API | 作用 |
| --- | --- |
| `atEnd()` | 是否到末尾 |
| `currentBlock()` | 当前项若为 block，返回它 |
| `currentFrame()` | 当前项若为 frame，返回它 |
| `parentFrame()` | 被遍历的父 frame |
| `operator++` / `operator--` | 前后移动 |
| `operator==` / `operator!=` | 比较迭代器 |

## 4. 关键用法

```cpp
for (auto it = frame->begin(); !it.atEnd(); ++it) {
    if (QTextFrame *child = it.currentFrame())
        walk(child);
    else if (QTextBlock block = it.currentBlock(); block.isValid())
        exportBlock(block);
}
```

## 5. 使用场景

富文本导出器、文档结构统计、自定义打印、结构检查。

## 6. 常见坑与经验

- `currentBlock()` 和 `currentFrame()` 只有一个会有效。
- 遍历时修改文档结构可能使迭代器失效，先收集再修改更安全。
- 它遍历直接子项，不自动递归进入子 frame。

## 7. 知识点覆盖

frame 内容遍历、block/frame 分支、递归遍历、迭代器失效。
