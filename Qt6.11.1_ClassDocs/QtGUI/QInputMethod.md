# QInputMethod

> Qt 6.11.1 · Qt GUI · 来自 `QInputMethod`

## 1. 先建立直觉

`QInputMethod` 是 Qt 对当前平台输入法服务的全局访问对象。它连接当前焦点编辑器、系统输入法、虚拟键盘、候选窗口和输入方向信息。

通常通过 `QGuiApplication::inputMethod()` 获取它，而不是自己 `new` 一个。普通桌面编辑控件很少直接调用它；自定义文本控件、触屏应用、虚拟键盘适配和复杂场景变换下的编辑器，则需要用它刷新查询状态、报告输入项几何或显式请求显示键盘。

## 2. 类说明

`QInputMethod` 继承自 `QObject`，由 Qt GUI 应用管理。它和 `QInputMethodEvent`、`QInputMethodQueryEvent` 配合：事件负责编辑器与输入法交换文字和上下文，`QInputMethod` 负责全局输入法状态与平台 UI。

类说明只用于表明这些 API 来自 `QInputMethod`。不要把它当成某个具体语言输入法实现，也不要手动管理其生命周期。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGuiApplication::inputMethod()` | 取得当前应用的全局输入法对象。 |
| `show()` / `hide()` / `setVisible(bool)` | 请求显示、隐藏虚拟键盘。 |
| `isVisible()` | 查询虚拟键盘是否可见。 |
| `isAnimating()` | 查询虚拟键盘是否正在显示或隐藏动画中。 |
| `keyboardRectangle()` | 返回虚拟键盘在窗口坐标中的几何区域；未知时可能为空。 |
| `cursorRectangle()` | 返回当前输入项光标矩形，候选窗和预测 UI 的定位依据。 |
| `anchorRectangle()` | 返回当前输入项锚点矩形，常对应选择锚点。 |
| `inputItemRectangle()` | 返回输入项自身坐标系下的几何矩形。 |
| `inputItemTransform()` | 返回输入项坐标到窗口坐标的变换。 |
| `inputItemClipRectangle()` | 返回输入项可见裁剪区域，帮助输入法判断可用屏幕空间。 |
| `setInputItemRectangle(rect)` | 报告自定义输入项的本地几何。 |
| `setInputItemTransform(transform)` | 报告自定义输入项到窗口的坐标变换。 |
| `locale()` | 返回当前输入法 locale。 |
| `inputDirection()` | 返回当前输入方向，如左到右或右到左。 |
| `commit()` | 请求输入法提交当前预编辑文本。 |
| `reset()` | 重置输入法组合状态。 |
| `update(queries)` | 通知输入法指定查询项已变化，需要重新向焦点对象查询。 |
| `invokeAction(action, cursorPosition)` | 把点击或上下文菜单等输入法相关操作通知给输入法。 |
| `queryFocusObject(query, argument)` | 静态函数，向当前焦点对象查询输入法数据。 |
| `cursorRectangleChanged()` 等信号 | 输入法几何、语言、可见性和动画状态变化通知。 |

## 4. 关键用法

### 通过全局入口取得对象

```cpp
QInputMethod *inputMethod = QGuiApplication::inputMethod();
connect(inputMethod, &QInputMethod::keyboardRectangleChanged,
        this, &EditorPage::updateKeyboardInsets);
```

不要保存一个自己创建的 `QInputMethod`；应用级对象应始终来自 `QGuiApplication`。

### 虚拟键盘出现时调整可见区域

```cpp
void EditorPage::updateKeyboardInsets()
{
    const QRectF keyboard = QGuiApplication::inputMethod()->keyboardRectangle();
    setBottomInset(keyboard.isEmpty() ? 0 : keyboard.height());
}
```

软键盘不一定停靠在窗口底部，尤其是浮动键盘。应基于 `keyboardRectangle()` 与实际控件几何做交集判断，而不是硬编码屏幕高度。

### 光标移动后主动刷新输入法查询

自定义编辑器在光标、选区、周围文本或输入项变换变化后，应通知输入法重新查询。

```cpp
void CustomEditor::setCursorPosition(int position)
{
    m_cursorPosition = position;
    QGuiApplication::inputMethod()->update(
        Qt::ImCursorRectangle
        | Qt::ImCursorPosition
        | Qt::ImAnchorPosition
        | Qt::ImSurroundingText
        | Qt::ImCurrentSelection);
    update();
}
```

只刷新发生变化的 query，可以减少输入法与编辑器之间的重复工作。

### 打断组合输入前先 commit 或 reset

当用户点击工具栏、切换文档或移动光标时，正在进行的预编辑可能需要处理：

```cpp
QGuiApplication::inputMethod()->commit();
moveCursorTo(targetPosition);
```

`commit()` 尝试把当前组合内容确认进编辑器；`reset()` 则清除输入法状态。选哪个取决于交互语义，不能随意调用导致用户正在输入的内容消失。

### 自定义场景输入项需要报告变换

在 `QGraphicsView`、缩放画布或自定义场景中，输入项的局部坐标不一定等于窗口坐标。此时要更新 `setInputItemRectangle()` 和 `setInputItemTransform()`，否则候选窗可能飘到错误位置。

## 5. 使用场景

`QInputMethod` 适合移动/触屏应用的虚拟键盘避让、自定义文本控件候选窗定位、复杂变换画布中的文本输入、输入法 locale 与方向变化、编辑器切换时的组合文本管理。

它也适合响应软键盘动画。通过 `visibleChanged()`、`animatingChanged()` 和 `keyboardRectangleChanged()`，界面可以平滑调整底部工具栏和滚动位置，而不是等键盘完全出现后突然跳动。

桌面程序若仅使用标准 Qt 文本控件，通常只需让 Qt 自动处理输入法；直接调用 `show()` / `hide()` 不应成为常规焦点管理的替代方案。

## 6. 常见坑与经验

不要在每次点击时强制 `show()` 或 `hide()`。正常焦点切换会由平台自动协调键盘，过度干预会与系统策略冲突。

不要假设 `keyboardRectangle()` 永远非空。没有软键盘、平台无法报告几何、或使用浮动键盘时都可能为空或不规则。

不要忘记 `update()`。自定义编辑器光标已经移动但候选窗仍在旧位置，最常见原因就是没有通知输入法重新查询。

不要在错误时机调用 `reset()`。它会清除正在组合的输入，可能导致用户未确认内容丢失。

不要把 `inputDirection()` 当作整个文档方向。它反映当前输入方向，文档可以包含混合双向文本。

## 7. 知识点覆盖

学习 `QInputMethod` 应覆盖全局输入法服务、虚拟键盘、软键盘避让、键盘动画、候选窗几何、光标与锚点矩形、输入项变换、输入法查询刷新、commit/reset、locale、双向文本和自定义编辑器协议。
