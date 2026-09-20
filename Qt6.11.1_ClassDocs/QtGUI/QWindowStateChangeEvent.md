# QWindowStateChangeEvent

> Qt 6.11.1 · Qt GUI · 来自 `QWindowStateChangeEvent`

## 1. 先建立直觉

`QWindowStateChangeEvent` 表示窗口状态发生变化，例如最小化、最大化、全屏或恢复普通窗口。它提供变化前的状态；变化后的状态应从窗口当前的 `windowState()` 或 `windowStates()` 读取。

只看当前状态往往不够。比如当前状态不再包含 `WindowMinimized`，你还需要知道它是从最小化恢复，还是从最大化恢复。比较 old state 和 new state，才能写出正确的暂停、恢复、重排和状态保存逻辑。

## 2. 类说明

`QWindowStateChangeEvent` 继承自 `QEvent`。Widgets 通常在 `changeEvent()` 中检查 `QEvent::WindowStateChange`，`QWindow` 则通过自己的窗口状态变化机制处理。

类说明只用于表明 `oldState()` 来自 `QWindowStateChangeEvent`。新状态不存放在事件对象中，而是以事件处理时窗口的当前状态为准。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `oldState() const` | 返回状态变化前的 `Qt::WindowStates` 位标志组合。 |
| `type()` | 来自 `QEvent`，通常为 `QEvent::WindowStateChange`。 |
| `QWidget::windowState()` | 配合事件读取 Widgets 窗口的当前状态。 |
| `QWindow::windowState()` | 配合事件读取 `QWindow` 的当前状态。 |

## 4. 关键用法

### 通过新旧状态判断最小化与恢复

```cpp
void MainWindow::changeEvent(QEvent *event)
{
    if (event->type() == QEvent::WindowStateChange) {
        auto *stateEvent = static_cast<QWindowStateChangeEvent *>(event);
        const Qt::WindowStates oldState = stateEvent->oldState();
        const Qt::WindowStates newState = windowState();

        const bool wasMinimized = oldState.testFlag(Qt::WindowMinimized);
        const bool isMinimized = newState.testFlag(Qt::WindowMinimized);

        if (!wasMinimized && isMinimized)
            pauseLivePreview();
        else if (wasMinimized && !isMinimized)
            resumeLivePreview();
    }

    QMainWindow::changeEvent(event);
}
```

最小化时暂停昂贵工作，恢复时刷新视图，是最常见的用途之一。

### 最大化和全屏要分别处理

`WindowMaximized` 与 `WindowFullScreen` 是不同状态。最大化通常保留窗口装饰和系统任务栏关系，全屏通常改变更彻底的窗口呈现策略。

```cpp
const bool enteredFullscreen =
    !oldState.testFlag(Qt::WindowFullScreen)
    && windowState().testFlag(Qt::WindowFullScreen);
```

## 5. 使用场景

`QWindowStateChangeEvent` 适合视频播放器、实时监控、图像编辑器、演示模式、游戏工具、主窗口停靠布局和资源敏感的桌面应用。

它也适合窗口布局恢复。用户从最大化回到普通窗口时，可以恢复之前保存的普通几何；进入全屏时可以隐藏工具栏、调整渲染质量或切换快捷键提示。

## 6. 常见坑与经验

不要只看 `oldState()` 或只看当前 `windowState()`。状态变化的意义来自两者比较。

不要假设状态只有一个标志。`Qt::WindowStates` 是位标志组合，窗口可能同时具备多个状态。

不要把最小化当作隐藏。最小化、隐藏、关闭分别走不同生命周期；资源管理策略可以相似，但触发点不同。

不要在 `changeEvent()` 里反复调用 `setWindowState()`，容易造成状态来回切换。需要主动切换时由明确的用户命令或状态机驱动。

## 7. 知识点覆盖

学习 `QWindowStateChangeEvent` 应覆盖窗口状态位标志、最小化、最大化、全屏、状态转换比较、`changeEvent()`、资源暂停恢复、窗口布局保存和隐藏/关闭的生命周期差异。
