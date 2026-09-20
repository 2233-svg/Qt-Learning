# QStatusTipEvent

> Qt 6.11.1 · Qt GUI · 来自 `QStatusTipEvent`

## 1. 先建立直觉

`QStatusTipEvent` 携带一条应该显示在状态栏或状态提示区域的短文本。它通常由菜单项、工具栏动作或自定义控件在用户悬停时触发，用来解释“这个操作会做什么”。

它和 tooltip 的定位不同：tooltip 跟随鼠标附近的控件显示，status tip 通常出现在主窗口底部的状态栏，适合不遮挡内容的持续说明。

## 2. 类说明

`QStatusTipEvent` 继承自 `QEvent`，事件类型是 `QEvent::StatusTip`。Widgets 应用可以在主窗口或事件过滤器中处理它，`QMainWindow` 常把状态提示转给 `QStatusBar`。

类说明只用于表明这些 API 来自 `QStatusTipEvent`：文本数据属于这个事件，状态栏如何呈现由接收对象决定。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QStatusTipEvent(tip)` | 构造状态提示事件，携带一条文本。 |
| `tip() const` | 读取要显示的状态提示文本。 |
| `type()` | 来自 `QEvent`，状态提示事件通常为 StatusTip。 |

## 4. 关键用法

### 在主窗口显示状态提示

```cpp
bool MainWindow::event(QEvent *event)
{
    if (event->type() == QEvent::StatusTip) {
        auto *status = static_cast<QStatusTipEvent *>(event);
        ui->statusBar->showMessage(status->tip());
        return true;
    }

    return QMainWindow::event(event);
}
```

实际项目中，`QAction::setStatusTip()` 通常会自动触发这类事件；自定义控件可以通过 `QStatusTipEvent` 参与同一套反馈机制。

### 让状态提示保持短而稳定

状态栏不是帮助文档。提示应说明动作结果，例如“删除选中的文件”，而不是堆叠实现细节。长说明应放在 tooltip、What's This 或帮助页面。

## 5. 使用场景

`QStatusTipEvent` 适合主窗口菜单、工具栏、状态栏、复杂表格命令、设计器工具、文件管理器和编辑器命令提示。

它也适合统一第三方或自定义控件的状态反馈，让用户悬停菜单项和悬停画布工具时都在同一个状态栏区域看到说明。

## 6. 常见坑与经验

不要在每次鼠标移动都手动发送状态提示。通常只在命令或目标变化时更新，避免状态栏闪烁。

不要把富文本或大段帮助塞进 `tip()`。状态栏适合短句。

不要忘记清除旧提示。菜单离开或控件失去 hover 时，可显示默认状态或清空状态栏。

不要和 tooltip 互相覆盖。明确哪个信息放在局部提示，哪个信息放在全局状态栏。

## 7. 知识点覆盖

学习 `QStatusTipEvent` 应覆盖状态栏反馈、`QAction::statusTip`、菜单和工具栏提示、事件转发、短文本设计、tooltip 与 status tip 的分工。
