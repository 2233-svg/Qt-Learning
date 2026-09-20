# QTextBlock
> Qt 6.11.1 · Qt GUI · 来自 `QTextBlock`

## 1. 先建立直觉

`QTextBlock` 表示文档中的一个段落块。对普通文本编辑器来说，它通常对应一行逻辑段落；对富文本来说，它是块格式、用户数据、布局和 fragment 序列的载体。

它是轻量值类型，像一个指向文档内部 block 的句柄。

## 2. 类说明

- 头文件：`#include <QTextBlock>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：值类型，引用 `QTextDocument` 内部块
- 协作类：`QTextDocument`、`QTextCursor`、`QTextLayout`、`QTextBlockUserData`

block 有 `position()`、`length()`、`blockNumber()`、`lineCount()`，也能持有 `QTextBlockFormat`、`QTextCharFormat`、`QTextList` 和自定义 user data。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `isValid()` | 是否指向有效 block |
| `text()` | 读取该块纯文本 |
| `position()` / `length()` | 块在文档中的起点和长度 |
| `blockNumber()` / `firstLineNumber()` | 块号和首行号 |
| `lineCount()` | 布局后的行数 |
| `next()` / `previous()` | 遍历相邻块 |
| `begin()` / `end()` | 遍历块内 fragment |
| `document()` | 所属文档 |
| `layout()` | 块的 `QTextLayout` |
| `textList()` | 所属列表 |
| `blockFormat()` / `charFormat()` | 块格式和默认字符格式 |
| `userData()` / `setUserData()` | 绑定自定义数据，文档接管所有权 |
| `userState()` / `setUserState()` | 保存整数状态，常用于高亮器 |
| `revision()` | 文档修订号相关信息 |

## 4. 关键用法

遍历文档：

```cpp
for (QTextBlock b = doc->begin(); b != doc->end(); b = b.next())
    qDebug() << b.blockNumber() << b.text();
```

在语法高亮中保存状态：

```cpp
setCurrentBlockState(InMultilineComment);
```

之后可通过 `block.userState()` 读取。复杂缓存用 `QTextBlockUserData`。

## 5. 使用场景

- 代码编辑器行号、折叠、断点、诊断标记。
- 逐段导出或分析文档。
- 语法高亮状态、括号缓存。
- 根据 block 查找屏幕布局行。
- 富文本段落级格式处理。

## 6. 常见坑与经验

- block 的 `length()` 包含段落分隔符，常比 `text().length()` 多 1。
- block number 会随插入删除变化，不适合长期当稳定 id。
- `layout()` 依赖文档布局，纯数据处理时可能没有你期望的行信息。
- `userData()` 所有权归文档，别手动 delete。
- `text()` 只给纯文本，不包含 fragment 的格式。

## 7. 知识点覆盖

本页覆盖：文本块、块遍历、位置长度、块布局、fragment 遍历、用户状态、用户数据、行号编辑器基础。
