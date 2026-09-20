# QAccessibleTextCursorEvent

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleTextCursorEvent`

## 1. 先建立直觉

`QAccessibleTextCursorEvent` 用于通知辅助技术：文本对象的插入光标移动到了新的位置。它是多个文本变化事件的基类，文本插入、删除、选区和更新事件都围绕“变化发生后光标在哪里”这个问题展开。

对于屏幕阅读器，光标位置不是装饰性信息。它决定用户继续输入的位置、下一次朗读的上下文，以及文本编辑命令的目标。

## 2. 类说明

- 头文件：`#include <QAccessibleTextCursorEvent>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QAccessibleEvent`
- 派生：`QAccessibleTextInsertEvent`、`QAccessibleTextRemoveEvent`、`QAccessibleTextSelectionEvent`、`QAccessibleTextUpdateEvent`

光标位置使用文本接口的偏移量体系，通常是逻辑文本中的字符位置。它不是像素坐标，也不是 UTF-8 字节下标。

## 3. API 速查

| API | 用途 |
|---|---|
| `QAccessibleTextCursorEvent(object, cursorPos)` | 为 QObject 构造光标变化事件。 |
| `QAccessibleTextCursorEvent(iface, cursorPos)` | 为可访问接口构造光标变化事件。 |
| `cursorPosition()` | 返回事件记录的新光标位置。 |
| `setCursorPosition(position)` | 修改事件中的光标位置。 |
| `QAccessible::updateAccessibility()` | 提交事件给辅助技术。 |

## 4. 关键用法

```cpp
void Editor::setCursorPosition(int position)
{
    position = clampToValidTextOffset(position);
    if (m_cursorPosition == position)
        return;

    m_cursorPosition = position;

    QAccessibleTextCursorEvent event(this, m_cursorPosition);
    QAccessible::updateAccessibility(&event);
}
```

事件应在真实光标状态改变后发送，这样辅助技术随后通过 `QAccessibleTextInterface::cursorPosition()` 查询时能得到同一个位置。

如果一次编辑既改变文本又移动光标，优先使用更具体的插入、删除、选区或更新事件；它们继承本类，也能携带最终光标位置。

## 5. 使用场景

| 场景 | 建议 |
|---|---|
| 用户按左右箭头移动插入点 | 发送文本光标事件。 |
| 鼠标点击文本定位光标 | 发送文本光标事件，必要时更新选区事件。 |
| 输入字符导致光标前进 | 使用 `QAccessibleTextInsertEvent`，并确认最终光标位置。 |
| 删除文本后光标回退 | 使用删除/更新事件，设置最终光标位置。 |
| 只滚动视图但光标未动 | 不发送此事件。 |

## 6. 常见坑与经验

- 光标偏移必须与 `QAccessibleTextInterface::text()`、`characterCount()`、`selection()` 使用同一套逻辑坐标。
- 不要把屏幕 x/y 坐标或 QTextCursor 的内部 block/column 对直接塞进 `cursorPos`。
- 编辑器若支持组合字符、代理项或复杂脚本，光标位置应落在合法文本边界上。
- 光标事件太频繁会造成读屏噪声；只在语义位置真实变化时发送。
- 对象销毁或文本模型重置后，旧光标位置可能不再有效，应先更新模型再发送重置/文本事件。

## 7. 知识点覆盖

- 文本光标事件与文本变化事件的关系
- 逻辑文本偏移和屏幕坐标的区别
- 光标状态查询与事件发送顺序
- 输入、删除、选区和滚动的事件选择
- Unicode 文本边界与编辑器一致性
