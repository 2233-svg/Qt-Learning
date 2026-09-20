# QTextFrame 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextFrame>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QTextObject`

## 1. 它解决什么问题

`QTextFrame` 表示 `QTextDocument` 中一个连续的结构化范围。根框架覆盖整个文档；嵌套框架可以承载一段带边框、边距、浮动策略或独立布局语义的内容。`QTextTable` 也是 `QTextFrame` 的派生类型。

它解决富文本文档中“哪些块和子框架组成一个结构单元”的问题。它不是 QWidget，不会自己显示窗口，也不是普通容器指针：它始终依附于一个 `QTextDocument`，位置和绘制由文档布局处理。

常见场景：

- 从 `rootFrame()` 遍历整份文档的块和嵌套结构；
- 用 `QTextCursor::insertFrame()` 插入带背景、边框或浮动效果的提示区；
- 检查某个文本位置所在的框架，或遍历框架中的块；
- 自定义文档布局通过 `QTextFrameLayoutData` 保存框架的缓存布局数据。

## 2. 创建与遍历

应用通常不直接 `new QTextFrame`，而是从文档取得已有框架，或让光标插入一个：

```cpp
QTextCursor cursor(document);
QTextFrameFormat format;
format.setBorder(1.0);
format.setPadding(8.0);

QTextFrame *frame = cursor.insertFrame(format);
cursor.insertText("A framed note.");
```

迭代器的当前位置只能是块或子框架之一：

```cpp
for (QTextFrame::iterator it = frame->begin(); !it.atEnd(); ++it) {
    if (QTextFrame *child = it.currentFrame()) {
        // A nested frame.
    } else {
        const QTextBlock block = it.currentBlock();
        // A direct block in this frame.
    }
}
```

`end()` 是哨兵，不能解引用。遍历期间修改同一文档结构会使迭代逻辑难以推断；需要编辑时先收集位置或重新开始遍历。

## 3. 位置、格式和布局数据

`firstPosition()` 与 `lastPosition()` 返回文档坐标；它们不是像素坐标，也不能与 `QTextBlock::blockNumber()` 混用。`firstCursorPosition()` 与 `lastCursorPosition()` 返回对应位置的光标值，适合继续用光标编辑或选择范围。

`frameFormat()` 返回 `QTextFrameFormat` 副本。修改副本不会影响文档，必须调用 `setFrameFormat()` 写回：

```cpp
QTextFrameFormat format = frame->frameFormat();
format.setBackground(QColor("#fff8d8"));
format.setBorderStyle(QTextFrameFormat::BorderStyle_Solid);
frame->setFrameFormat(format);
```

`layoutData()` / `setLayoutData()` 是给文档布局实现使用的扩展点。`setLayoutData()` 会把数据对象交给 frame 管理并替换旧数据；传入后调用方不再删除或以所有者身份管理该指针。常规编辑代码不需要使用它。

## 4. 生命周期和线程

通过 `rootFrame()`、`frameAt()`、表格 API 或 `insertFrame()` 获得的框架由文档管理。不要手动 `delete` 这些指针，也不要在文档销毁、清空或删去相关结构之后保留并使用它们。

`QTextFrame` 是 `QObject` 且与文档、布局共享状态。同一份文档及其框架应只在所属线程访问；GUI 编辑器里通常是 GUI 线程。后台分析应复制纯文本或克隆独立文档，而不是传递 `QTextFrame *`。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextFrame(QTextDocument *document)` | 为指定文档构造框架对象。 | 常规代码应通过文档或 `QTextCursor::insertFrame()` 获取。 |
| `~QTextFrame()` | 销毁框架对象。 | 文档管理的框架由文档生命周期处理，调用方不手动删除。 |
| `setFrameFormat(const QTextFrameFormat &format)` | 用完整框架格式更新此框架。 | 参数是值对象；调用后文档重新布局。 |
| `frameFormat()` | 返回当前框架格式副本。 | 修改返回值不会自动写回。 |
| `firstPosition()` / `lastPosition()` | 返回框架覆盖范围的首尾文档位置。 | 是文档字符位置，不是像素位置或块号。 |
| `firstCursorPosition()` / `lastCursorPosition()` | 返回定位到首尾范围的 `QTextCursor`。 | 修改文档后应重新取得需要的边界。 |
| `layoutData()` | 取得框架附带的布局私有数据。 | 返回指针由 frame 管理；主要供自定义布局使用。 |
| `setLayoutData(QTextFrameLayoutData *data)` | 替换框架布局数据。 | frame 接管传入对象所有权；不要重复删除或共享它。 |
| `childFrames()` | 返回直接子框架列表。 | 子框架仍由文档拥有，不含更深层后代。 |
| `parentFrame()` | 返回直接父框架。 | 根框架没有父框架，返回 `nullptr`。 |
| `begin()` / `end()` | 返回框架内容遍历的起点和哨兵。 | 当前项可能是块或子框架；`end()` 不能读取。 |
| `iterator::currentBlock()` | 取得当前直接块。 | 当前项是子框架时不应作为有效块使用。 |
| `iterator::currentFrame()` | 取得当前直接子框架。 | 当前项是块时返回 `nullptr`。 |
| `iterator::parentFrame()` | 返回该迭代器所属框架。 | 不转移框架所有权。 |
| `iterator::atEnd()` | 判断是否到达终点。 | 推荐用作循环条件。 |
| `iterator::operator++()` / `operator--()` | 前进或后退一个块/子框架项。 | 不要越过边界，也不要在结构编辑后依赖旧迭代状态。 |

## 6. 记忆重点

`QTextFrame` 是文档结构树中的范围节点。它管理文档结构和框架格式，不是界面控件；框架指针属于文档，遍历时要区分当前是块还是子框架，位置永远按文档坐标理解。
