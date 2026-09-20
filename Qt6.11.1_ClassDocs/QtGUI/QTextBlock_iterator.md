# QTextBlock::iterator
> Qt 6.11.1 · Qt GUI · 来自 `QTextBlock::iterator`

## 1. 先建立直觉

`QTextBlock::iterator` 用来遍历一个文本块中的 `QTextFragment`。每个 fragment 是一段格式一致的文本，因此这个迭代器适合分析一个段落内部的富文本片段。

## 2. 类说明

- 头文件：`#include <QTextBlock>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：迭代器值类型
- 来源：`QTextBlock::begin()`、`QTextBlock::end()`

## 3. API 速查

| API | 作用 |
| --- | --- |
| `atEnd()` | 是否到达末尾 |
| `fragment()` | 当前 fragment |
| `operator++` / `operator--` | 前后移动 |
| `operator==` / `operator!=` | 比较迭代器 |

## 4. 关键用法

```cpp
for (auto it = block.begin(); !it.atEnd(); ++it) {
    QTextFragment frag = it.fragment();
    if (frag.isValid())
        exportSpan(frag.text(), frag.charFormat());
}
```

## 5. 使用场景

导出段落内富文本、检查格式范围、自定义渲染前收集格式片段、语法高亮结果调试。

## 6. 常见坑与经验

- fragment 可能为空或无效，使用前检查。
- 文档修改后迭代器失效，重新从 block 获取。
- 它不是字符级迭代器，格式相同的连续字符会合并。

## 7. 知识点覆盖

block 内 fragment 遍历、格式片段、迭代器失效、富文本导出。
