# QShowEvent

> Qt 6.11.1 · Qt GUI · 来自 `QShowEvent`

## 1. 先建立直觉

`QShowEvent` 表示控件或窗口正在从隐藏状态进入可见状态。它发生在 `show()`、父控件显示、窗口重新显示等流程中，适合做与“第一次对用户可见”有关的轻量工作。

它不是“窗口已经完成所有渲染”的保证，也不是通用的构造替代品。构造函数适合建立对象不变的结构，`showEvent()` 适合根据当前尺寸、屏幕、DPI 或最新数据调整一次显示状态。

## 2. 类说明

`QShowEvent` 继承自 `QEvent`，自身只有默认构造函数。Widgets 中通常通过 `QWidget::showEvent()` 接收，也可以在 `event()` 中处理 `QEvent::Show`。

类说明只用于表明这个事件类型来自 `QShowEvent`。事件本身不携带“为什么显示”或“显示在哪个屏幕”等额外字段，这些信息要从窗口当前状态和应用上下文中读取。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QShowEvent()` | 构造显示事件，主要用于测试或自定义事件投递。 |
| `accept()` / `ignore()` | 继承自 `QEvent`，设置事件接受状态；通常不用于阻止显示。 |
| `type()` | 继承自 `QEvent`，显示事件通常为 `QEvent::Show`。 |

## 4. 关键用法

### 在显示时根据当前尺寸准备内容

```cpp
void PreviewWidget::showEvent(QShowEvent *event)
{
    if (!m_previewInitialized) {
        rebuildPreview(size());
        m_previewInitialized = true;
    }

    QWidget::showEvent(event);
}
```

如果内容依赖控件最终尺寸，`showEvent()` 往往比构造函数更合适。但要做好重复显示处理，因为窗口隐藏后再次显示也可能再次收到事件。

### 首次显示时启动延迟任务

```cpp
void Dashboard::showEvent(QShowEvent *event)
{
    QWidget::showEvent(event);

    if (!m_loaded) {
        m_loaded = true;
        QTimer::singleShot(0, this, &Dashboard::refreshData);
    }
}
```

把重任务延迟到事件循环下一轮，可以避免阻塞首次显示；真正的网络或计算工作仍应放在合适的异步线程/接口中。

### 显示事件不是阻止显示的入口

如果窗口不应显示，应在调用 `show()` 前检查条件，或在权限、状态和导航层阻止操作。不要依赖 `QShowEvent::ignore()` 作为可靠的“取消显示”机制。

## 5. 使用场景

`QShowEvent` 适合首次可见初始化、懒加载预览、显示后根据屏幕 DPI 调整布局、启动可见窗口才需要的动画、恢复停靠面板状态。

它也适合调试生命周期。通过记录 `showEvent()`、`hideEvent()`、`closeEvent()` 的顺序，可以发现窗口被反复创建、隐藏或显示的问题。

## 6. 常见坑与经验

不要把一次性初始化直接写成每次 `showEvent()` 都执行。对话框反复打开时，这会造成重复连接、重复加载和状态重置。

不要在 `showEvent()` 中同步执行大量工作，否则窗口可能已经设置为可见，却长时间没有响应。

不要忘记调用基类实现。基类可能维护窗口、样式、输入法或子控件状态。

不要用显示事件推断用户一定看到了窗口。窗口可能在屏幕外、被遮挡或尚未完成首次绘制。

## 7. 知识点覆盖

学习 `QShowEvent` 应覆盖显示生命周期、懒加载、首次显示标记、事件循环延迟、重复 show/hide、DPI 与布局、基类事件处理、可见与真正呈现之间的区别。
