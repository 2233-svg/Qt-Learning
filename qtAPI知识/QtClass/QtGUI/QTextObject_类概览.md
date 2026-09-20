# QTextObject 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextObject>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QObject`

## 1. 它解决什么问题

`QTextObject` 是 `QTextDocument` 中有独立对象身份的结构节点基类。`QTextFrame`、`QTextList` 和 `QTextBlockGroup` 都建立在它之上；它把对象与所属文档、对象格式和内部索引关联起来。

它解决的是“文档中的结构对象如何被文档查找、格式化和管理生命周期”。它不是为应用直接实例化的通用 QObject，也不是自定义内联对象绘制接口；后者使用 `QTextObjectInterface`。

## 2. 格式和索引的语义

`format()` 返回此对象的 `QTextFormat` 副本。派生类通常再转换为具体格式，例如 `QTextFrame::frameFormat()` 和 `QTextList::format()`。修改这份副本不会影响文档；派生类通过受保护的 `setFormat()` 或公开的具体 `setXxxFormat()` 写回。

`formatIndex()` 是文档内部格式表索引，`objectIndex()` 是对象在文档对象表中的索引。两者都可用于调试或配合 `QTextDocument::object()` / `objectForFormat()` 查询，但不是稳定业务 ID，不能写入持久化文件或跨文档比较。

## 3. 文档关系和生命周期

构造函数、析构函数与 `setFormat()` 都是受保护成员，表明它是给 Qt 文档对象体系和派生类使用的基类。`document()` 返回所属文档，但返回指针不转移所有权。

由文档创建或返回的 `QTextObject` 派生对象由文档管理。不要手动删除 `rootFrame()`、`frameAt()`、`object()`、`QTextList *` 等返回对象，也不要在文档修改后把旧对象指针长期缓存。

`QTextObject` 是 QObject；对象和文档应在同一线程访问。信号槽并不解除文档结构的并发读写限制，后台任务应只接收拷贝后的数据或独立克隆文档。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextObject(QTextDocument *)` | 为文档关联一个文本对象基类。 | 受保护；应用通过派生对象或文档 API 使用。 |
| `~QTextObject()` | 销毁对象。 | 受保护；文档管理的对象不可由调用方手动删除。 |
| `document()` | 返回所属文档指针。 | 不转移所有权；文档销毁后指针不能继续使用。 |
| `format()` | 返回对象格式副本。 | 修改副本不回写对象。 |
| `setFormat(const QTextFormat &)` | 更新对象格式。 | 受保护；派生类应使用合适的具体格式并在文档线程调用。 |
| `formatIndex()` | 返回内部格式表索引。 | 仅在当前文档生命周期内有意义，不是业务 ID。 |
| `objectIndex()` | 返回对象表索引。 | 可配合文档查询；删除对象结构后不应缓存或复用。 |

## 4. 记忆重点

`QTextObject` 是文档结构对象的 QObject 基类。应用最常接触它的派生类；格式和索引都是文档内部关系，读取格式得到的是副本，文档拥有对象并规定线程边界。
