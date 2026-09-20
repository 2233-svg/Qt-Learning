# QTextBlockUserData：为单个文本块挂接应用私有数据

> Qt 6.11.1 | `#include <QTextBlockUserData>` | 模块：`Qt6::Gui`

`QTextBlockUserData` 是一个只有虚析构函数的多态基类。它解决的不是“给文本再加一种格式”，而是给某个 `QTextBlock` 附加不会写入文档文本和富文本格式的应用数据。

典型例子是语法高亮器为每行保存分析结果、代码编辑器为段落保存折叠信息或诊断结果、Markdown 编辑器缓存本块的解析节点。这样，文本显示仍由 `QTextDocument` 管理，应用状态则放在自己的派生对象里。

## 正确的所有权模型

数据通过 `QTextBlock::setUserData()` 挂到块上：

```cpp
#include <QTextBlock>
#include <QTextBlockUserData>

class BlockInfo final : public QTextBlockUserData
{
public:
    int parserState = -1;
    bool hasDiagnostic = false;
};

void attachInfo(QTextBlock block)
{
    auto *info = new BlockInfo;
    info->parserState = 7;
    block.setUserData(info);
}
```

调用 `setUserData()` 后，**块取得该指针的所有权**。块被删除、所属文档销毁，或再次用另一个指针设置用户数据时，旧对象会被销毁。因此：

- 传入的对象应在堆上分配，并且只交给一个块。
- 不要再用 `std::unique_ptr`、父子 `QObject` 关系或手工 `delete` 同时管理它。
- `QTextBlock::userData()` 返回的是不拥有所有权的裸指针；下一次文档编辑或替换数据后，不要继续缓存和解引用它。
- 同一个 `QTextBlockUserData *` 不能同时交给两个块，否则会发生重复释放。

它不是 `QObject`，没有信号槽、线程归属或 parent 参数。线程安全也不会因此自动获得：数据跟随 `QTextBlock`，而块和文档的访问必须仍在 `QTextDocument` 的所属线程完成。

## 实际使用方式

读取时通常做一次安全的向下转型：

```cpp
BlockInfo *info = dynamic_cast<BlockInfo *>(block.userData());
if (info && info->hasDiagnostic) {
    // 使用该块当前附带的缓存。
}
```

如果数据只由自己的高亮器创建，也可以使用 `static_cast`，但前提是该块绝不会被其他组件设置成不同派生类型。大型编辑器更稳妥的做法是让一个协调者唯一负责 `setUserData()`，或者把类型标识放进基类。

`QSyntaxHighlighter` 的逐块状态 API (`previousBlockState()` / `setCurrentBlockState()`) 适合一个简单整数状态；需要多个字段或可扩展缓存时，`QTextBlockUserData` 更合适。不要把可重新计算的大型全局索引无节制地塞入每个块，否则每行一个堆对象会成为编辑和内存开销。

## 生命周期与编辑边界

块的文本被改写不一定会立即销毁用户数据；但块合并、删除、重设整个文档、限制最大块数等操作都可能让它消失。用户数据应当能承受“下一次编辑即失效”，其析构函数也不应回调同一个文档进行结构编辑。

若缓存依赖块文本、格式或外部文件版本，应有明确失效策略。仅因为 `QTextBlock` 仍有效，并不表示缓存仍匹配当前文本。

## 常见误区

- **把数据当成持久化文档内容。** `toHtml()`、`toMarkdown()` 和 `toPlainText()` 都不会导出它。
- **传栈对象。** 块最终会删除该指针，栈对象会导致未定义行为。
- **给块设置同一指针两次或多块共享同一指针。** 所有权是唯一的。
- **保存 `userData()` 的裸指针供以后使用。** 一旦块删除或替换数据，指针立即悬空。

## API 速查表

| API | 语义 | 边界与注意点 |
| --- | --- | --- |
| `virtual ~QTextBlockUserData()` | 虚析构函数，供块在不知道派生类型时正确销毁附加数据。 | 实际挂接入口是 `QTextBlock::setUserData()`；设置后所有权转移给块。析构函数应避免重入编辑所属文档。 |

## 小结

`QTextBlockUserData` 是“每个段落的一块私有、非持久化元数据”。只要牢记 `setUserData()` 的唯一所有权和编辑造成的随时失效，它就是为编辑器保存逐行解析缓存的直接工具。
