# Qt QAccessibleEditableTextInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleEditableTextInterface>`  
> 所属模块：`Qt6::Gui`  
> 定位：允许辅助技术编辑文本内容的纯虚接口

## 1. 它解决什么问题

`QAccessibleEditableTextInterface` 让辅助技术可以对一个真正可编辑的文本对象执行删除、插入和替换。屏幕阅读器的用户可能通过语音、盲文设备或辅助输入法编辑控件内容，而不是通过鼠标和键盘直接操作。

该接口通常与 `QAccessibleTextInterface` 一起实现：

- `QAccessibleTextInterface` 提供文本读取、光标、选择、边界和几何；
- `QAccessibleEditableTextInterface` 提供文本修改；
- `QAccessibleInterface::state()` 应准确报告 `editable`、`readOnly`、`passwordEdit` 等状态。

它不是任意字符串编辑接口。实现不能绕过控件的只读、禁用、输入校验、撤销栈、权限限制或业务规则；辅助技术必须拥有与普通用户相同的编辑能力和限制。

## 2. 偏移量语义

所有位置参数都是文档/文本中的字符偏移，而不是 UTF-8 字节下标、像素坐标或 `QString` 临时切片索引。范围按 `startOffset` 到 `endOffset` 表示，实际实现应与同一对象的 `QAccessibleTextInterface::text()`、`characterCount()`、selection API 采用一致的范围规则。

建议实现时明确采用半开区间 `[startOffset, endOffset)`：

- `startOffset == endOffset` 表示空范围；
- `insertText(offset, text)` 在 `offset` 前插入；
- `deleteText(start, end)` 删除范围内文本；
- `replaceText(start, end, text)` 以 `text` 替换该范围。

Qt 接口不会替你验证越界、负值或反向范围。派生类应安全处理无效输入：可以拒绝操作、裁剪到合法范围或按自身文本模型的明确契约处理，但不能越界访问或造成崩溃。

## 3. 实际使用场景

以下是自定义富文本编辑器中包装已有编辑入口的示意：

```cpp
void EditorAccessible::replaceText(int start, int end,
                                   const QString &text)
{
    if (!editor()->isEnabled() || editor()->isReadOnly())
        return;

    QTextCursor cursor(editor()->document());
    cursor.setPosition(start);
    cursor.setPosition(end, QTextCursor::KeepAnchor);
    cursor.insertText(text);
}
```

真实实现还应处理范围检查、输入法/验证器、撤销命令、富文本格式、光标更新以及 `TextInserted`、`TextRemoved` 或 `TextUpdated` 无障碍事件。不要仅修改底层字符串而绕开编辑器已有的模型通知。

## 4. 状态、线程与通知

只有对象真正可编辑时才应暴露 editable text interface：

- 禁用对象应拒绝修改；
- 只读对象可继续实现文本读取接口，但不应允许编辑；
- 密码框要防止读取接口泄露敏感文本；
- 编辑操作必须在所属 GUI/文档线程执行；
- 成功编辑后，文本内容、selection、cursor 和 undo 状态都必须保持内部一致。

接口没有返回值，因此调用方无法从签名本身区分成功和失败。实现必须把无效输入和不可编辑状态处理为安全的无副作用路径，而不是依赖异常或断言来控制正常业务流程。

## 5. 逐项 API 说明

### `virtual ~QAccessibleEditableTextInterface()`

虚析构函数。接口通常由 `QAccessibleInterface` 实现对象提供；获取到的接口指针是借用，不表示调用方拥有它。

### `virtual void deleteText(int startOffset, int endOffset) = 0`

删除从 `startOffset` 到 `endOffset` 的文本范围。对于空范围，推荐无副作用；对于无效范围，应安全拒绝或按文档模型规范化。

实现应走正常编辑路径，以便触发验证、撤销、文本变化和无障碍更新。不要把删除理解为销毁 QObject 或删除 UI 子对象。

### `virtual void insertText(int offset, const QString &text) = 0`

在 `offset` 位置插入 `text`。空字符串通常可作为无操作处理。

`text` 是 Unicode `QString`，实现应保留其文本语义，而不是误把长度当作 UTF-8 字节数。插入后光标如何移动由控件的正常编辑行为决定，但应与通过键盘输入同样一致。

### `virtual void replaceText(int startOffset, int endOffset, const QString &text) = 0`

删除指定范围并插入替代文本。它在语义上是一个原子编辑请求：实现最好以单个撤销命令、单次模型更新或等价事务执行，而不是让外部观察到不必要的“先全删、再插入”中间状态。

替代文本为空时可等价于删除；空范围配合非空文本可等价于插入。无效范围和只读状态必须安全处理。

## API 速查表

| 类别 | API | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 生命周期 | `~QAccessibleEditableTextInterface()` | 虚析构接口。 | 所有权通常属于 accessible interface 实现。 |
| 编辑 | `deleteText(int, int)` | 删除文本范围。 | 偏移是字符位置；无效范围必须安全处理。 |
| 编辑 | `insertText(int, const QString &)` | 在指定位置插入文本。 | 不以 UTF-8 字节计数；只在可编辑状态下执行。 |
| 编辑 | `replaceText(int, int, const QString &)` | 替换文本范围。 | 应尽量保持为一个逻辑编辑事务。 |

### 一句话总结

`QAccessibleEditableTextInterface` 让辅助技术像普通用户一样修改可编辑文本：位置使用一致的字符偏移，编辑必须尊重禁用/只读/验证/撤销规则，并与文本接口和文本变化事件保持同步。
