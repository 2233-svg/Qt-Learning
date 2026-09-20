# QAccessibleEvent

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleEvent`

## 1. 先建立直觉

`QAccessibleEvent` 是向平台辅助技术报告“某个可访问对象发生了什么变化”的事件基类。它不是投递给 `QObject::event()` 的普通 Qt 输入事件，而是由应用构造后传给 `QAccessible::updateAccessibility()` 的语义通知。

当值、焦点、名称、选择、可见性或对象结构发生变化时，辅助技术依靠这类事件刷新自己的缓存并向用户反馈。事件类型越具体，读屏和平台就越有机会给出正确体验。

## 2. 类说明

- 头文件：`#include <QAccessibleEvent>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 来源类：无障碍事件基类。
- 常用子类：`QAccessibleValueChangeEvent`、`QAccessibleStateChangeEvent`、文本插入/删除/光标事件、表模型变化事件和公告事件。

优先使用描述性子类。仅在没有专用事件可表达时，才直接构造 `QAccessibleEvent` 并指定 `QAccessible::Event`。

## 3. API 速查

| API | 用途 |
|---|---|
| `QAccessibleEvent(object, type)` | 以 QObject 为来源构造事件，通常开销更低。 |
| `QAccessibleEvent(iface, type)` | 以现成可访问接口为来源构造事件。 |
| `type()` | 读取事件类型。 |
| `object()` | 读取来源 QObject，可能为空。 |
| `accessibleInterface()` | 读取关联接口。 |
| `child()` / `setChild(index)` | 指定发生变化的子对象索引。 |
| `QAccessible::updateAccessibility(event)` | 将事件通知无障碍系统。 |

## 4. 关键用法

```cpp
void CustomList::setCurrentRow(int row)
{
    if (m_currentRow == row)
        return;

    m_currentRow = row;
    update();

    QAccessibleEvent event(this, QAccessible::Selection);
    event.setChild(row);
    QAccessible::updateAccessibility(&event);
}
```

`child` 是可访问树中的子索引，不是模型绝对行号或屏幕位置。若项目视图的可访问子树与模型行不一一对应，直接设置模型行会误导辅助技术；应让事件语义与 `child(index)` / `indexOfChild()` 的实现保持一致。

```cpp
QAccessibleStateChangeEvent event(checkBox, QAccessible::State());
event.changedState().checked = true;
QAccessible::updateAccessibility(&event);
```

状态、数值和文本变化应使用对应子类，因为它们携带更精确的增量数据。只发送笼统 `ObjectShow` 或 `ValueChanged` 会丢失选择范围、插入文本或 state flag 等关键上下文。

## 5. 事件选择参考

| 实际变化 | 优先事件 |
|---|---|
| 滑块、进度、数值编辑器的值 | `QAccessibleValueChangeEvent`。 |
| 勾选、启用、展开、焦点等状态 | `QAccessibleStateChangeEvent` 或 `Focus`。 |
| 文本插入、删除、替换 | 对应文本事件。 |
| 文本光标或选区移动 | `QAccessibleTextCursorEvent` 或选择事件。 |
| 表格/树模型行列改变 | `QAccessibleTableModelChangeEvent`。 |
| 需要临时朗读的异步反馈 | `QAccessibleAnnouncementEvent`。 |
| 对象出现、隐藏、名称改变 | 对应的 `QAccessible::Event`。 |

## 6. 常见坑与经验

- 事件对象可以是栈对象；`updateAccessibility()` 返回后不要保存其指针。
- 不要在每次 `paintEvent()` 中发送事件。绘制不是语义变化，频繁事件会淹没读屏输出。
- 事件要在真实状态改变后发送，使辅助技术查询接口时读到的是新值。
- 来源对象必须在事件处理期间有效；对象删除前不应再发送指向它的事件。
- `QAccessible::isActive()` 可用于跳过昂贵事件数据的组装，但不要以它为由省略 UI 本身的状态更新。
- 无障碍树一般绑定 GUI 对象，跨线程状态更新应回到 GUI 线程再修改对象并发送事件。

## 7. 知识点覆盖

- 无障碍事件与普通 Qt 事件的区别
- 对象、接口与子节点定位
- 事件精确性和平台缓存同步
- 状态、值、文本、表格与公告子事件
- 事件频率、生命周期和 GUI 线程
