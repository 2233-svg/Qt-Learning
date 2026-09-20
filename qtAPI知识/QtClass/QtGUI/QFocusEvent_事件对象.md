# Qt QFocusEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QFocusEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QEvent -> QFocusEvent`  
> 定位：键盘焦点进入或离开对象时携带原因的事件

## 1. 它解决什么问题

`QFocusEvent` 表示一个对象获得或失去键盘焦点。它让控件根据焦点状态更新视觉反馈、提交或暂存编辑、启动输入法协作，以及根据焦点转移原因调整交互策略。

常见场景：

- `focusInEvent()` 时选中文本、显示焦点环；
- `focusOutEvent()` 时结束临时编辑或隐藏辅助 UI；
- 区分 Tab 键切换、鼠标点击、弹窗抢焦点和活动窗口切换；
- 自定义输入控件与 `QInputMethod` 协作。

失去焦点不等价于用户完成编辑。弹出菜单、切换窗口、程序化 `setFocus()` 都可能产生 `FocusOut`；数据提交仍应依据控件状态和业务规则。

## 2. 事件入口

```cpp
#include <QFocusEvent>
#include <QLineEdit>

class AmountEdit : public QLineEdit
{
protected:
    void focusInEvent(QFocusEvent *event) override
    {
        QLineEdit::focusInEvent(event);
        selectAll();
    }

    void focusOutEvent(QFocusEvent *event) override
    {
        QLineEdit::focusOutEvent(event);
        commitIfAcceptable(event->reason());
    }
};
```

一般先调用基类实现，再添加控件特有逻辑，除非你明确要截断基类焦点行为。事件对象只在回调期间有效；异步处理时复制 `reason()`，而不是保存事件指针。

## 3. `FocusIn`、`FocusOut` 与 `gotFocus()`

构造函数的 `type` 应为 `QEvent::FocusIn` 或 `QEvent::FocusOut`：

- `gotFocus()` 在类型为 `FocusIn` 时返回 true；
- `lostFocus()` 在类型为 `FocusOut` 时返回 true。

这两个函数只是 `type()` 的语义化快捷判断。事件的接受状态不能用来改变 Qt 已经完成的焦点切换；若要控制焦点去向，应在焦点策略、Tab 顺序、事件过滤或编辑器逻辑中处理。

## 4. `reason()` 的语义

`reason()` 返回 `Qt::FocusReason`，说明焦点为何转移。常见值包括：

| 原因 | 典型来源 | 使用建议 |
| --- | --- | --- |
| `MouseFocusReason` | 鼠标点击。 | 可按点击进入的交互习惯设置光标或选择。 |
| `TabFocusReason` / `BacktabFocusReason` | Tab、Shift+Tab 导航。 | 保持键盘导航体验，不依赖鼠标位置。 |
| `ShortcutFocusReason` | 快捷键或助记键。 | 可将焦点移到关联输入控件。 |
| `MenuBarFocusReason` | 菜单栏导航。 | 不要误判为编辑提交。 |
| `PopupFocusReason` | 弹出窗口获取或归还焦点。 | 通常不应因短暂失焦丢弃编辑状态。 |
| `ActiveWindowFocusReason` | 活动窗口变化。 | 可能只是应用切换。 |
| `OtherFocusReason` | 其它或程序化焦点切换。 | 不要做过度具体推断。 |

原因帮助优化体验，但业务正确性不能只依赖它。比如用户鼠标点击另一个字段和窗口失焦都可能需要校验，但失败后的恢复策略可能不同。

## 5. 焦点、可见性和输入法

控件要获得键盘焦点，需要合适的 `focusPolicy`、可见性和可用状态；仅重写 `focusInEvent()` 并不会使它自动可聚焦。父窗口隐藏、控件禁用、删除、弹出模态窗口等也可能造成 `FocusOut`。

自定义文本输入控件应在焦点变化时与输入法状态保持一致，例如通过 `QInputMethod` 更新查询或隐藏候选状态。不要在 `focusOutEvent()` 中假定用户永远已经点击了其他编辑控件。

## 6. 常见错误

- 把每次 `FocusOut` 都当作用户确认并无条件保存；
- 忽略 `PopupFocusReason`，打开补全菜单就丢失编辑；
- 重写回调后不调用基类，破坏选择、输入法或样式行为；
- 用 `accept()` 试图阻止焦点离开；
- 异步保存 `QFocusEvent *`；
- 忘记设置控件焦点策略，却期望收到焦点事件。

## 7. 逐项 API 说明

### `explicit QFocusEvent(QEvent::Type type, Qt::FocusReason reason = Qt::OtherFocusReason)`

构造焦点事件，主要用于测试或自定义事件投递。`type` 只应使用 `FocusIn` 或 `FocusOut`；`reason` 记录转移原因。手动发送事件不会自动改变 Qt 的真实焦点对象。

### 查询 API

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `bool gotFocus() const` | 判断事件是否为 `FocusIn`。 | 等价于比较 `type() == QEvent::FocusIn`。 |
| `bool lostFocus() const` | 判断事件是否为 `FocusOut`。 | 等价于比较 `type() == QEvent::FocusOut`。 |
| `Qt::FocusReason reason() const` | 获取焦点转移原因。 | 用于体验分支，不是业务提交的唯一依据。 |

### 从 `QEvent` 继承

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `type()` | 获取事件类型。 | 正常应为 `FocusIn` 或 `FocusOut`。 |
| `accept()` / `ignore()` | 设置事件处理状态。 | 不会撤销已发生的焦点切换。 |
| `isAccepted()` | 查询事件处理状态。 | 不能替代 `QWidget::hasFocus()`。 |

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QFocusEvent(type, reason)` | 创建焦点事件。 | 手动构造不改变真实焦点。 |
| 判断 | `gotFocus()` | 判断是否获得焦点。 | 等价于 `FocusIn` 类型判断。 |
| 判断 | `lostFocus()` | 判断是否失去焦点。 | 等价于 `FocusOut` 类型判断。 |
| 原因 | `reason()` | 了解为何发生焦点转移。 | 不要作为业务提交唯一条件。 |
| 入口 | `focusInEvent()` | 初始化焦点状态。 | 通常先调用基类。 |
| 入口 | `focusOutEvent()` | 清理或校验编辑状态。 | Popup、窗口切换也会触发。 |
| 状态 | `accept()` / `ignore()` | 设置事件处理状态。 | 不能阻止焦点已经转移。 |

---

### 一句话总结

`QFocusEvent` 描述的是焦点已经如何转移；利用 `reason()` 改善交互，但不要把任何一次失焦简单等同于“用户确认提交”。
