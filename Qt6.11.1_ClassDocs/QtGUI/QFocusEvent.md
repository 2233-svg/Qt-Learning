# QFocusEvent

> Qt 6.11.1 · Qt GUI · 来自 `QFocusEvent`

## 1. 先建立直觉

`QFocusEvent` 描述控件或窗口获得、失去键盘焦点。焦点决定键盘输入送到哪里，也决定 Tab 导航、快捷键覆盖、输入法光标、可访问性提示等行为。

它的重点不是坐标，而是“为什么焦点变了”。用户按 Tab、鼠标点击、弹窗关闭、窗口激活、代码调用 `setFocus()`，都会产生不同的 `Qt::FocusReason`。优秀的控件会根据原因选择不同反馈：键盘进入时显示清晰焦点框，鼠标点击时可能减少干扰。

## 2. 类说明

`QFocusEvent` 继承自 `QEvent`。Widgets 中常通过 `focusInEvent()` 和 `focusOutEvent()` 处理，也可以在通用 `event()` 或事件过滤器里检查 `QEvent::FocusIn` / `QEvent::FocusOut`。

类说明只用于表明这些 API 来自 `QFocusEvent`：是否获得/失去焦点和焦点变化原因属于焦点事件本身；具体控件如何显示焦点、是否接受键盘输入，由控件策略决定。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QFocusEvent(type, reason)` | 构造焦点事件，类型必须是 FocusIn 或 FocusOut。 |
| `gotFocus() const` | 判断事件是否表示获得焦点。 |
| `lostFocus() const` | 判断事件是否表示失去焦点。 |
| `reason() const` | 返回焦点变化原因，如 Tab、Backtab、鼠标、弹窗、窗口激活、其他原因。 |
| `type() const` | 来自 `QEvent`，可直接区分 FocusIn 与 FocusOut。 |

## 4. 关键用法

### 根据焦点进入原因决定视觉反馈

键盘用户需要明显焦点框，鼠标用户有时不需要同样强的提示。

```cpp
void ToolButton::focusInEvent(QFocusEvent *event)
{
    m_showStrongFocus = event->reason() == Qt::TabFocusReason
        || event->reason() == Qt::BacktabFocusReason;
    update();
    QWidget::focusInEvent(event);
}
```

这不是“隐藏焦点”，而是根据输入方式调整反馈强度。可访问性要求高的界面仍应保证焦点可见。

### 失去焦点时提交或取消编辑

编辑控件常在失焦时提交临时值，但要留意弹窗和菜单原因。

```cpp
void InlineEditor::focusOutEvent(QFocusEvent *event)
{
    if (event->reason() == Qt::PopupFocusReason) {
        QWidget::focusOutEvent(event);
        return;
    }

    commitText();
    QWidget::focusOutEvent(event);
}
```

如果用户只是打开补全弹窗或上下文菜单，不一定希望当前编辑立即结束。

### 不要用焦点事件代替启用状态

焦点表示键盘输入目标，不表示控件是否可用、是否选中、鼠标是否悬停。状态之间要分开维护。

## 5. 使用场景

`QFocusEvent` 用于自定义编辑器、表格单元格编辑、属性面板、按钮焦点框、游戏/快捷键面板、无鼠标操作支持、输入法位置更新和可访问性反馈。

它也常用于恢复状态。比如搜索框打开时抢焦点，关闭后把焦点还给之前控件；这类逻辑要尊重焦点原因，避免用户正在键盘导航时突然跳焦点。

在复杂窗口里，焦点事件能帮助你区分“控件内部切换焦点”和“整个窗口失去激活”。前者可能只需提交编辑，后者可能要暂停输入模式或隐藏浮层。

## 6. 常见坑与经验

不要在 `focusInEvent()` 里无条件再调用 `setFocus()`，容易制造焦点震荡。

不要失焦就销毁相关对象，特别是菜单、补全框、弹窗可能临时改变焦点。先看 `reason()`，再决定提交、取消或等待。

不要忘记基类实现。许多控件内部会在焦点事件中维护光标、选择、输入法和样式状态。

不要把鼠标进入和焦点进入混为一谈。鼠标悬停不会自动获得键盘焦点，除非控件或平台策略明确如此。

## 7. 知识点覆盖

学习 `QFocusEvent` 应覆盖键盘焦点、焦点策略、Tab 顺序、焦点原因、焦点框绘制、失焦提交、弹窗焦点、输入法、可访问性、窗口激活与控件焦点的区别。
