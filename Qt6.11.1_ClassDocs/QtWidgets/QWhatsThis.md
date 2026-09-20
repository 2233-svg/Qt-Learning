# QWhatsThis

> Qt 6.11.1 · Qt Widgets · 来自 `QWhatsThis`

## 1. 先建立直觉

`QWhatsThis` 是 Qt Widgets 的“这是什么？”上下文帮助机制。用户进入该模式后点击某个控件，应用可以展示一段更详细的解释，帮助用户理解这个控件的用途、影响和边界。

它和 `QToolTip` 的差别很明显：tooltip 是短提示，适合解释一个按钮名；What's This 是小型说明，适合解释复杂设置。它也不同于状态栏提示，状态栏更偏即时动作反馈，而 `QWhatsThis` 偏帮助文档的就地入口。

## 2. 类说明

`QWhatsThis` 不是可实例化控件，而是一组静态函数。它负责进入/离开 What's This 模式、显示/隐藏说明文本，并能创建一个标准 `QAction` 供菜单或工具栏触发。

具体帮助文本通常设置在 widget 或 action 上，例如 `QWidget::setWhatsThis()`、`QAction::setWhatsThis()`。`QWhatsThis` 负责模式和弹出展示，文本内容仍由你的界面对象提供。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `createAction(QObject *)` | 创建标准“这是什么？”动作，适合放到帮助菜单或工具栏。 |
| `enterWhatsThisMode()` | 让应用进入 What's This 模式，下一次点击控件时显示对应说明。 |
| `leaveWhatsThisMode()` | 主动退出 What's This 模式。 |
| `inWhatsThisMode()` | 判断当前是否处于 What's This 模式。 |
| `showText(const QPoint &, const QString &, QWidget *)` | 在全局位置显示一段 What's This 文本。 |
| `hideText()` | 隐藏当前显示的 What's This 弹窗。 |
| `QWidget::setWhatsThis()` | 给控件绑定说明文本，和 `QWhatsThis` 配合使用。 |
| `QAction::setWhatsThis()` | 给菜单项或工具栏动作绑定说明文本。 |
| `QEvent::EnterWhatsThisMode` | 进入模式时发给顶层窗口，复杂 UI 可据此调整状态。 |
| `QEvent::LeaveWhatsThisMode` | 离开模式时发给顶层窗口。 |

## 4. 关键用法

给控件设置帮助文本：

```cpp
ui->cacheSizeSpinBox->setWhatsThis(
    tr("Controls how much memory is reserved for recently opened documents. "
       "Larger values make switching faster but increase memory usage."));
```

把标准入口加到菜单：

```cpp
helpMenu->addAction(QWhatsThis::createAction(this));
```

也可以在自己的帮助按钮里直接进入模式：

```cpp
connect(helpButton, &QToolButton::clicked, this, [] {
    QWhatsThis::enterWhatsThisMode();
});
```

## 5. 使用场景

适合解释偏专业的设置项、配置页里不常用但影响较大的参数、图形软件工具选项、管理员控制台中的策略开关、带副作用的高级功能。

不适合放置长篇教程。What's This 文本应该能在当前界面旁边读完；如果需要多步骤教学，应该跳转到帮助文档、引导页或示例工程。

## 6. 常见坑与经验

不要把 tooltip 和 What's This 写成同一句。tooltip 说“这是什么按钮”，What's This 说“什么时候用、改了会怎样”。

`showText()` 的位置是全局坐标，不是控件局部坐标。通常要用 `widget->mapToGlobal()` 计算。

帮助文本也需要维护。配置项改名、默认值变化、风险边界变化时，What's This 比普通 UI 文案更容易被忘掉，但它往往正是用户困惑时会读的内容。
