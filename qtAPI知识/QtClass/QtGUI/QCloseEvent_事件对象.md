# QCloseEvent：让窗口决定是否接受关闭请求

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCloseEvent>`  
> 模块：Qt GUI，链接 `Qt6::Gui`  
> 继承：`QEvent`

## 它解决什么问题

用户点击标题栏关闭按钮、从窗口菜单选择关闭，或代码调用 `QWidget::close()` 时，Qt 不会直接销毁 widget，而是先发送 `QCloseEvent`。接收者通过接受或忽略事件决定这次关闭是否继续。

这使窗口能够在关闭前询问是否保存未保存内容、阻止正在执行关键操作的窗口退出，或在关闭后安排资源释放。

`QCloseEvent` 自身没有新增成员函数；它的全部行为来自 `QEvent` 的接受状态：

- `accept()`：允许关闭。
- `ignore()`：拒绝关闭。
- `isAccepted()`：读取当前决定。

## 默认行为与关闭结果

`QWidget::closeEvent(QCloseEvent *)` 的默认实现会接受事件。事件被接受后，widget 会被隐藏；它**不会默认销毁**。

若 widget 设置了 `Qt::WA_DeleteOnClose` 属性，接受关闭事件后还会被销毁。这对多窗口应用中的独立顶层窗口很方便，但也意味着关闭后保存的裸指针立刻可能悬空。

最后一个顶层窗口关闭时，`QGuiApplication::lastWindowClosed()` 会发出。它不等同于进程必然退出，实际是否退出还取决于应用的 `quitOnLastWindowClosed` 等配置。

## 实际使用场景

典型的是未保存文档的确认逻辑：

```cpp
void EditorWindow::closeEvent(QCloseEvent *event)
{
    if (!document()->isModified()) {
        event->accept();
        return;
    }

    const auto choice = askToSaveChanges();
    if (choice == Save) {
        if (saveDocument())
            event->accept();
        else
            event->ignore();
    } else if (choice == Discard) {
        event->accept();
    } else {
        event->ignore();
    }
}
```

异步保存不能让 `closeEvent()` 等待后台任务结束后再调用同一个事件对象。事件只在当前分发期间有效。正确做法是先 `ignore()`，保存完成后再发起一次新的 `close()` 请求，或在状态机中明确处理待关闭状态。

## 生命周期和边界

不要在 `closeEvent()` 中默认 `delete this`。若需要关闭后销毁，优先使用 `Qt::WA_DeleteOnClose` 或在事件接受后安排明确、安全的对象生命周期策略。直接删除正在处理事件的对象容易让调用栈继续访问已经释放的内存。

同样，不要保存 `QCloseEvent *` 到成员变量或异步 lambda 中。它由 Qt 的事件分发过程管理，处理函数返回后不再有效。

`ignore()` 只是拒绝本次关闭请求，不会隐藏窗口，也不会阻止未来再收到关闭事件。用户下一次点击关闭或代码再次调用 `close()` 时，仍会重新进入 `closeEvent()`。

在 X11 上，窗口管理器理论上可能强制关闭窗口，应用不应把“忽略关闭事件”作为唯一的数据持久化保护。关键数据应在编辑过程中正常保存或具备崩溃恢复策略。

## 常见误区

- 认为接受关闭事件一定销毁窗口。默认只是隐藏，除非设置了 `WA_DeleteOnClose`。
- 用 `setVisible(false)` 代替关闭确认。这样绕开了 `closeEvent()` 的接受/拒绝逻辑。
- 在异步回调中调用已过期的 `QCloseEvent`。
- 拒绝关闭后仍继续执行销毁、释放文档等关闭后逻辑。
- 设置了 `WA_DeleteOnClose` 却继续持有窗口的裸指针。

## API 速查表

| API | 含义 | 重点边界 |
| --- | --- | --- |
| `QCloseEvent()` | 创建关闭事件，初始接受状态由 Qt 事件机制使用。 | 通常由框架创建并发送，业务代码只在处理器中消费。 |
| 继承的 `void accept()` | 同意此次关闭。 | widget 随后隐藏；带 `Qt::WA_DeleteOnClose` 时还会销毁。 |
| 继承的 `void ignore()` | 拒绝此次关闭。 | 只拒绝当前请求，后续仍可再次请求关闭。 |
| 继承的 `bool isAccepted() const` | 查询接收者是否同意关闭。 | 用于需要向父类或协作对象传递关闭决定的场景。 |
| 处理器 `QWidget::closeEvent(QCloseEvent *)` | 接收 widget 关闭请求。 | 需要确认或拦截关闭时重写它；不要保存事件指针。 |
| 触发点 `QWidget::close()` | 程序化发起关闭请求。 | 仍会发送 `QCloseEvent`，可能被 `ignore()` 拒绝。 |
| 属性 `Qt::WA_DeleteOnClose` | 关闭被接受后自动删除 widget。 | 使用后避免继续使用旧裸指针。 |
