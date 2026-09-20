# QCloseEvent

> Qt 6.11.1 · Qt GUI · 来自 `QCloseEvent`

## 1. 先建立直觉

`QCloseEvent` 是窗口或控件收到“请关闭自己”请求时的确认机会。它不是关闭已经完成后的通知，而是关闭动作真正发生前的最后一道业务判断：保存未提交的数据、询问用户是否放弃修改、阻止不允许关闭的窗口，都在这里完成。

Qt 会把事件送给 `closeEvent()`。如果事件被接受，窗口通常会隐藏；顶层窗口或带有 `WA_DeleteOnClose` 的对象还可能随后销毁。如果事件被忽略，关闭请求被拒绝，窗口保持打开。

## 2. 类说明

`QCloseEvent` 继承自 `QEvent`，自身没有状态读取函数；它的核心状态就是继承来的 accepted 标志。Widgets 常在 `QWidget::closeEvent()` 中处理，窗口对象也可以在 `event()` 中接收 `QEvent::Close`。

类说明只用于表明这个 API 来自 `QCloseEvent`。真正的关闭策略属于接收窗口，不应把“收到关闭事件”误解为“必须销毁对象”。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QCloseEvent()` | 构造一个关闭请求事件，通常用于测试或自定义事件分发。 |
| `accept()` | 接受关闭请求，允许 Qt 继续执行关闭流程。 |
| `ignore()` | 拒绝关闭请求，窗口保持打开。 |
| `isAccepted()` | 查询当前关闭请求是否已被接受。 |
| `type()` | 来自 `QEvent`，通常为 `QEvent::Close`。 |

## 4. 关键用法

### 未保存修改时决定是否关闭

```cpp
void EditorWindow::closeEvent(QCloseEvent *event)
{
    if (!document()->isModified()) {
        event->accept();
        return;
    }

    const auto answer = QMessageBox::question(
        this, tr("保存修改"),
        tr("文档尚未保存，是否保存后关闭？"),
        QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel);

    if (answer == QMessageBox::Save && saveDocument()) {
        event->accept();
    } else if (answer == QMessageBox::Discard) {
        event->accept();
    } else {
        event->ignore();
    }
}
```

关闭策略要覆盖保存失败、用户取消和没有修改三条路径。不要因为弹框返回了 `Save` 就无条件接受，保存失败时应继续阻止关闭。

### 关闭不等于销毁

默认情况下，`QWidget::close()` 通常让窗口隐藏；对象是否销毁取决于父子关系、应用退出流程和 `Qt::WA_DeleteOnClose`。如果还需要恢复窗口状态，不要在 `closeEvent()` 里把“关闭”当成“对象永远不存在”。

### 异步保存不能直接拖住事件

如果保存需要网络或耗时计算，不要在关闭事件里长时间阻塞 GUI 线程。可以先 `ignore()`，启动保存，成功后再次调用 `close()`；否则窗口会保持打开。

## 5. 使用场景

`QCloseEvent` 用于文档编辑器、工程管理器、数据库客户端、播放器、后台任务窗口、设置对话框和多文档界面。任何需要在退出前确认或收尾的窗口都可能用到它。

它也适合统一应用退出策略。`QApplication::closeAllWindows()` 会触发各窗口的关闭判断，某一个窗口忽略事件，就可以阻止整个应用直接退出。

## 6. 常见坑与经验

不要把清理代码只放在析构函数里，窗口被关闭后可能只是隐藏，析构函数并不会立即运行。

不要在 `closeEvent()` 里无条件弹确认框。程序自动关闭、用户已保存、应用正常退出时，重复询问会破坏工作流。

不要忽略保存失败。接受关闭前要确认数据已经落盘，网络同步或外部写入失败时应让用户继续处理。

不要在关闭事件中递归调用 `close()`。需要延迟关闭时先忽略当前事件，等异步流程完成后再发起新的关闭请求。

## 7. 知识点覆盖

学习 `QCloseEvent` 应覆盖关闭请求与对象销毁的区别、事件接受/忽略、未保存修改、应用退出、多窗口关闭、异步保存、`WA_DeleteOnClose`、析构时机和 GUI 线程阻塞风险。
