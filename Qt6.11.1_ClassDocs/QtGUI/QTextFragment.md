# QTextFragment
> Qt 6.11.1 · Qt GUI · 来自 `QTextFragment`

## 1. 先建立直觉

`QTextFragment` 是同一段文本中一段连续、格式一致的字符范围。一个 `QTextBlock` 由多个 fragment 组成，每个 fragment 有自己的 `QTextCharFormat`。

它适合读取文档内部“文字加格式”的最小片段，而不是编辑。编辑仍应通过 `QTextCursor`。

## 2. 类说明

- 头文件：`#include <QTextFragment>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：值类型，引用文档内部片段
- 协作类：`QTextBlock::iterator`、`QTextCharFormat`

fragment 的有效期和文档结构相关。文档被修改后，之前保存的 fragment 句柄应重新获取。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `isValid()` | 是否有效 |
| `text()` | 片段纯文本 |
| `position()` | 片段在文档中的起点 |
| `length()` | 片段长度 |
| `charFormat()` | 片段字符格式 |
| `charFormatIndex()` | 内部格式表索引，主要用于低层优化 |
| `contains(position)` | 指定文档位置是否落在片段内 |

## 4. 关键用法

遍历一个 block 的片段：

```cpp
for (auto it = block.begin(); !(it.atEnd()); ++it) {
    QTextFragment f = it.fragment();
    if (f.isValid())
        qDebug() << f.text() << f.charFormat().fontWeight();
}
```

这比对每个字符查询格式更高效，因为格式相同的连续范围已经被合并。

## 5. 使用场景

- 导出富文本为自定义格式。
- 检查一段文本里哪些区域加粗、着色、链接。
- 自定义绘制或统计格式覆盖范围。
- 语义分析和高亮调试。

## 6. 常见坑与经验

- fragment 是只读观察，不要试图直接改它。
- 一个 block 中相邻文字格式相同可能合并成一个 fragment，格式变化才会切片。
- 文档修改后重新遍历，别长期缓存 fragment。
- `position()` 是文档全局位置，不是 block 内局部位置。

## 7. 知识点覆盖

本页覆盖：格式片段、block 内遍历、字符格式读取、文档位置、富文本导出。
