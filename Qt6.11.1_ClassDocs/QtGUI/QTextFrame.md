# QTextFrame
> Qt 6.11.1 · Qt GUI · 来自 `QTextFrame`

## 1. 先建立直觉

`QTextFrame` 是 `QTextDocument` 中的块级容器。整份文档有一个 root frame，表格也是一种 frame，普通 frame 可以承载多个 block 和子 frame。它让富文本不只是线性段落，还能有容器、边框、浮动和嵌套结构。

## 2. 类说明

- 头文件：`#include <QTextFrame>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QTextObject`
- 协作类：`QTextFrameFormat`、`QTextCursor`、`QTextDocument`

frame 属于文档内部对象，不应直接 new 后独立使用。通常通过 `QTextCursor::insertFrame()` 创建。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `document()` | 所属文档 |
| `parentFrame()` | 父 frame |
| `childFrames()` | 子 frame 列表 |
| `begin()` / `end()` | 遍历 frame 内容 |
| `firstCursorPosition()` / `lastCursorPosition()` | frame 内首尾 cursor |
| `firstPosition()` / `lastPosition()` | frame 覆盖的文档位置 |
| `frameFormat()` / `setFrameFormat()` | 读取或设置 frame 格式 |

## 4. 关键用法

```cpp
QTextFrameFormat fmt;
fmt.setBorder(1);
fmt.setPadding(6);
QTextFrame *frame = cursor.insertFrame(fmt);
```

遍历 root frame 时，每个节点要么是 block，要么是子 frame。

## 5. 使用场景

- 文档中的提示框、引用框、侧栏。
- 遍历文档结构，区分段落和嵌套 frame。
- 打印报表中的容器分组。
- 自定义导出 HTML/Markdown 时保留结构。

## 6. 常见坑与经验

- frame 内内容遍历要用 `QTextFrame::iterator`，不是只遍历 document block。
- 修改 frame format 会触发布局变化。
- root frame 不等同于第一个段落，它是整篇文档容器。
- 表格是 `QTextTable`，继承 frame，但有专门 API。

## 7. 知识点覆盖

文档 frame 树、root frame、frame 格式、结构遍历、嵌套容器。
