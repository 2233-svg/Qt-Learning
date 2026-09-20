# QAccessibleTextSelectionEvent：通知文本选区变化

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAccessibleTextSelectionEvent>`  
> 模块：Qt GUI，链接 `Qt6::Gui`  
> 继承：`QAccessibleTextCursorEvent`

## 它解决什么问题

当前插入点位置不足以表达“用户选中了哪段文本”。选择一段文字、取消选择或调整选择范围，会影响屏幕阅读器的反馈、复制命令的上下文和盲文设备的显示。`QAccessibleTextSelectionEvent` 专门描述这种选区变化。

创建该事件后，`type()` 是 `QAccessible::TextSelectionChanged`。它通知的是已经发生的状态改变，不会替控件设置选区。

## 实际使用场景

自定义文档控件在鼠标拖拽、Shift 加方向键、全选、程序选择或清除选择后，需要在其可访问文本状态更新后发出通知。

```cpp
#include <QAccessible>
#include <QAccessibleTextSelectionEvent>

void CodeEditor::selectAccessibleRange(int start, int end)
{
    m_selectionStart = start;
    m_selectionEnd = end;

    QAccessibleTextSelectionEvent event(this, start, end);
    QAccessible::updateAccessibility(&event);
}
```

这里的 `start`、`end` 应来自控件对外公开给 `QAccessibleTextInterface` 的同一套文本坐标，而不是绘制用的行列位置或 UTF-8 字节位置。

## 选区与光标的联动规则

本类继承了光标位置，但构造函数同时设置了默认值：

- 通常 `cursorPosition()` 被设为 `end`。
- 当 `start == -1` 时，`cursorPosition()` 被设为 `0`。

这反映了 Qt 的内部实现，不能把它理解成事件会计算或修改控件的真实插入点。`setSelection()` 之后，继承的 `cursorPosition()` 不会自动重新计算；若需要同时修正事件中的光标位置，必须再调用 `setCursorPosition()`。

`start == -1` 是 Qt 构造函数特别处理的值，常用于表明没有有效选择的通知语义。类本身不会验证其他参数组合，也不会自动排序 `start` 与 `end`。调用方应遵循自身 `QAccessibleTextInterface` 的选区约定，并避免发送一个无法从接口当前状态复现的范围。

## 生命周期与分发

构造函数既可接收 `QObject *`，也可接收 `QAccessibleInterface *`；事件不取得其所有权。将事件作为局部对象传给 `QAccessible::updateAccessibility()` 是常规用法。

标准文本编辑控件已内置无障碍支持。只有自定义或代理实现没有自动通知时才应发送，避免同一选择变化被报告两次。

## API 逐项说明

### 构造函数

`QAccessibleTextSelectionEvent(QAccessibleInterface *iface, int start, int end)` 和对象版本都记录一段新选区。

- 事件类型为 `QAccessible::TextSelectionChanged`。
- `selectionStart()`、`selectionEnd()` 分别保留传入的两个位置。
- 默认光标位置为 `end`，但 `start == -1` 时为 `0`。

### `selectionStart() const` 与 `selectionEnd() const`

分别返回事件中保存的选区起止位置。它们是事件快照，不会从控件重新读取，也不会随 `setCursorPosition()` 改变。

### `setSelection(int start, int end)`

只改写事件的两个选区字段。它不会移动真实选区，也不会更新继承的光标位置，且不进行范围、次序或文本长度校验。

## API 速查表

| API | 含义 | 重点边界 |
| --- | --- | --- |
| `QAccessibleTextSelectionEvent(QAccessibleInterface *iface, int start, int end)` | 为接口创建选区变化通知。 | 接口不被拥有，位置应与可访问文本一致。 |
| `QAccessibleTextSelectionEvent(QObject *object, int start, int end)` | 为对象创建选区变化通知。 | 构造后事件类型为 `TextSelectionChanged`。 |
| `int selectionStart() const` | 读取记录的选区起点。 | 只是事件快照。 |
| `int selectionEnd() const` | 读取记录的选区终点。 | 不应按像素或 UTF-8 字节解释。 |
| `void setSelection(int start, int end)` | 改写事件中的选区范围。 | 不校验范围，不会同步 `cursorPosition()`。 |
| 继承的 `cursorPosition() const` | 读取本事件附带的光标位置。 | 构造时通常为 `end`，`start == -1` 时为 `0`。 |
| 继承的 `setCursorPosition(int)` | 单独改写事件的光标位置。 | 与 `setSelection()` 没有自动联动。 |
| 配套调用 `QAccessible::updateAccessibility(QAccessibleEvent *)` | 分发选区变化通知。 | 先更新控件选择状态，再分发。 |
