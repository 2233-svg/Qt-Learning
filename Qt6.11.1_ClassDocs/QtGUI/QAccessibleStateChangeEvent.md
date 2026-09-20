# QAccessibleStateChangeEvent

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleStateChangeEvent`

## 1. 先建立直觉

`QAccessibleStateChangeEvent` 用于告诉辅助技术：某个对象的一个或多个状态位发生了变化。它关心的是“哪些状态位变了”，而不是“对象现在的完整状态是什么”。

典型状态包括焦点、选中、勾选、展开、禁用、不可见、忙碌、只读等。事件发送后，辅助技术会再通过 `QAccessibleInterface::state()` 查询当前状态。

## 2. 类说明

- 头文件：`#include <QAccessibleStateChangeEvent>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QAccessibleEvent`
- 来源对象：可以用 `QObject *` 或 `QAccessibleInterface *` 构造。

构造参数中的 `QAccessible::State` 表示“发生变化的状态位掩码”。它不是新状态的完整副本。

## 3. API 速查

| API | 用途 |
|---|---|
| `QAccessibleStateChangeEvent(object, state)` | 为 QObject 构造状态变化事件。 |
| `QAccessibleStateChangeEvent(iface, state)` | 为可访问接口构造状态变化事件。 |
| `changedStates()` | 返回本次发生变化的状态位集合。 |
| `type()` | 继承自基类，事件类型为状态变化相关类型。 |
| `QAccessible::updateAccessibility()` | 将事件提交给辅助技术。 |

## 4. 关键用法

```cpp
void ToggleChip::setChecked(bool checked)
{
    if (m_checked == checked)
        return;

    m_checked = checked;
    update();

    QAccessible::State changed;
    changed.checked = true; // 表示 checked 这个位发生了变化
    QAccessibleStateChangeEvent event(this, changed);
    QAccessible::updateAccessibility(&event);
}
```

注意 `changed.checked = true` 并不表示“现在一定是选中”。它表示 checked 位改变了。当前到底是选中还是未选中，应由事件之后的 `QAccessibleInterface::state()` 返回。

若对象失去焦点，同样应把 `changed.focused` 设为 true，而不是 false；false 表示该位没有变化，反而会让辅助技术不知道要刷新焦点状态。

## 5. 使用场景

| 状态变化 | 建议 |
|---|---|
| 复选框/开关勾选变化 | 设置 `changed.checked` 或 `changed.checkStateMixed`。 |
| 树节点展开/折叠 | 设置 `changed.expanded` / 相关状态位，并同步子节点可见性事件。 |
| 控件启用/禁用 | 设置 `changed.disabled`。 |
| 对象开始或结束加载 | 设置 `changed.busy`。 |
| 变为只读或可编辑 | 设置 `changed.readOnly` / `editable` 相关位。 |
| 焦点变化 | 常可使用专门的 `Focus` 事件；必要时配合状态变化。 |

## 6. 常见坑与经验

- 不要把完整当前 state 直接作为 changed state 传入。这样会把未变化的 true 位也报告为变化，导致多余甚至错误的朗读。
- 事件应在底层状态改变后发送，让 `state()` 查询得到新状态。
- 多个状态同一次交互中一起变化时，可以在一个事件中设置多个 changed 位。
- 只因 hover、动画或绘制变化而没有语义状态改变时，不应发送该事件。
- 如果状态变化伴随值、文本或结构改变，可能还需要发送更具体的值/文本/表格事件。

## 7. 知识点覆盖

- `QAccessible::State` 完整状态与变化掩码的区别
- checked、focused、expanded、disabled、busy 等常见状态
- 状态事件和接口 `state()` 查询的配合
- 事件发送时机与重复通知控制
- 复合交互中的多状态同步
