# QTextBlockGroup：把一组文本块作为文档对象管理

> Qt 6.11.1 | `#include <QTextBlockGroup>` | 模块：`Qt6::Gui`
>
> 继承关系：`QTextObject -> QTextBlockGroup`。直接派生类中最常见的是 `QTextList`。

`QTextBlockGroup` 不是给应用代码直接实例化和填充的容器。它是富文本引擎内部使用的一层抽象：让一个文档对象持续关联一批 `QTextBlock`，并在块插入、移除或格式变化时得到通知。`QTextList` 就借它实现“这些段落属于同一个列表”。

这一区分很重要：`QList<QTextBlock>` 是普通值容器，而 `QTextBlockGroup` 表示文档结构中的关系。块的实际顺序、存在与否和归属都由 `QTextDocument` 的编辑操作决定，不由调用者手工维护。

## 适用场景

- 阅读或扩展 `QTextList` 一类的文档对象时，理解列表成员如何随编辑自动更新。
- 为自定义 `QTextObject`/文档结构做内部扩展，并且确实需要在块归属变化时维护附加状态。
- 常规富文本编辑器中，应使用 `QTextCursor::createList()`、`insertList()` 或 `QTextList`，而不是试图直接使用本类。

## 构造、所有权与访问边界

构造函数和析构函数都是 `protected`，因此应用代码不能直接写 `QTextBlockGroup group(document)`。子类在构造时把目标 `QTextDocument *` 传给基类；对象随文档的对象模型工作，不能把它当成可自由移动、可脱离文档保存的值类型。

`QTextBlockGroup` 禁止复制。`blockList()` 返回的是 `QTextBlock` 值的列表，不是可修改组成员资格的引用；调用后文档仍可能被编辑，返回列表只是取得当时成员的一份快照。

同一个 `QTextDocument` 的编辑、布局和其对象图应在文档所属线程中完成。不要在工作线程持有组对象并同时让 GUI 线程编辑该文档；跨线程传递文本或计算结果，再在文档线程应用。

## 派生类的工作模型

文档引擎会在下列变化发生时调用三个虚函数：

1. 块刚加入该组时调用 `blockInserted()`。
2. 块不再属于该组时调用 `blockRemoved()`。
3. 仍属于该组的块格式变化时调用 `blockFormatChanged()`。

这些是通知钩子，不是供外部代码主动调用的“修改组”接口。重写时应只维护派生类自己的缓存或不变量，避免在回调里再次进行会改变同一文档结构的大规模编辑；否则很容易造成重入、额外通知或失效的块引用。

例如，自定义组若缓存块数，可以在每个钩子里让缓存失效，然后在下一次查询时通过 `blockList()` 重建。不要把 `QTextBlock` 的编号当作永久 ID：插入、删除和 `maximumBlockCount` 截断都会改变编号。

## 常见误区

- **把它当作公开容器。** 它没有公开的 `append()`、`remove()` 或构造入口。改变组关系应通过光标和具体派生类的 API 完成。
- **在回调中保存裸指针。** `QTextBlock` 是轻量值句柄，不是可长期替代文档生命周期的对象；文档删除后，任何相关句柄和组对象都不能再使用。
- **手动调用 `blockInserted()`。** 这只会伪造通知，不会把块加入组。
- **把回调当作跨线程事件。** 它们由文档编辑过程同步触发，线程边界仍由 `QTextDocument` 决定。

## API 速查表

| API | 语义 | 边界与注意点 |
| --- | --- | --- |
| `protected QTextBlockGroup(QTextDocument *document)` | 将派生组绑定到 `document`。 | 仅派生类可调用；`document` 的生命周期必须覆盖组的使用期。 |
| `protected ~QTextBlockGroup()` | 虚析构，允许经基类路径销毁派生对象。 | 不要由应用代码删除文档管理的对象；遵循具体派生类和文档的所有权规则。 |
| `protected virtual void blockInserted(const QTextBlock &block)` | 文档把 `block` 纳入本组后通知派生类。 | 只做轻量同步或缓存失效；不是插入块的命令。 |
| `protected virtual void blockRemoved(const QTextBlock &block)` | `block` 脱离本组时通知派生类。 | 回调后不要假定该块仍在组内，或仍会继续存在。 |
| `protected virtual void blockFormatChanged(const QTextBlock &block)` | 组内块的块格式发生变化时通知派生类。 | 字符格式变化与块格式变化不是一回事；需要哪一种取决于实现目标。 |
| `protected QList<QTextBlock> blockList() const` | 返回当前属于该组的块值列表。 | 结果是快照，不能通过修改列表改变文档；编辑后应重新查询。 |

## 小结

把 `QTextBlockGroup` 看作“文档结构关系的受保护基类”最准确。应用层通常使用它的具体派生类；只有编写派生类时，才需要围绕三个通知钩子和 `blockList()` 建立自己的状态。
