# QChildWindowEvent：报告 QWindow 子窗口的加入与移除

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QChildWindowEvent>`  
> 模块：Qt GUI，链接 `Qt6::Gui`  
> 继承：`QEvent`

## 它解决什么问题

当一个 `QWindow` 获得或失去子窗口时，父窗口需要有机会同步原生窗口关系、绘制资源或自定义管理列表。`QChildWindowEvent` 携带这次关系变化中的子窗口指针。

它只对应两种事件类型：

- `QEvent::ChildWindowAdded`
- `QEvent::ChildWindowRemoved`

它不同于 `QObject` 的 `QChildEvent`。本类面向的是 `QWindow` 的窗口层级，而不是任意 `QObject` 的父子关系。

## 实际使用场景

常规窗口程序通常不需要手工处理。需要维护嵌入式子窗口布局、窗口层级资源，或封装一个自定义窗口容器时，可以在父窗口的 `event()` 中识别这两个事件。

```cpp
bool HostWindow::event(QEvent *event)
{
    if (event->type() == QEvent::ChildWindowAdded
        || event->type() == QEvent::ChildWindowRemoved) {
        auto *childEvent = static_cast<QChildWindowEvent *>(event);
        QWindow *child = childEvent->child();

        // 这里只使用 QWindow 的稳定基础能力。
        updateChildWindowRegistry(child, event->type());
        return true;
    }

    return QWindow::event(event);
}
```

实际是否返回 `true` 取决于父类是否还需要处理该事件。若只是观察而非接管逻辑，应在完成自己的同步后调用 `QWindow::event(event)`。

## 最重要的生命周期边界

这类事件发生在派生对象生命周期的敏感阶段：

- 收到 `ChildWindowAdded` 时，子窗口的派生类部分可能尚未完成构造。
- 收到 `ChildWindowRemoved` 时，子窗口的派生类部分可能已经析构。

因此，在两种事件中都只能可靠地把 `child()` 当作 `QWindow`，不能依赖其具体派生类型、成员变量、虚函数覆写或 `dynamic_cast`/`qobject_cast` 结果。更不能在移除事件中访问它的业务状态，或将裸指针缓存起来以后继续使用。

如果业务确实需要处理自定义子窗口的完整状态，应在派生类构造完成后用显式注册机制通知父窗口，并在析构前用明确的解除注册机制处理，而不是借这两个事件猜测对象是否完整。

## 构造和所有权

Qt 框架正常管理这类事件的创建和分发。应用代码一般只读取收到的事件，不应通过手动构造、投递 `QChildWindowEvent` 来伪造父子窗口关系变化；正确做法是改变实际 `QWindow` 父子关系。

`child()` 返回非拥有指针，事件不延长子窗口寿命。事件处理期间也只能按上述构造和析构边界使用它。

## 常见误区

- 将它和 `QChildEvent` 混用，导致处理了 QObject 层级而不是窗口层级。
- 在 `ChildWindowAdded` 回调中调用自定义子类方法，读取到尚未初始化的状态。
- 在 `ChildWindowRemoved` 回调中访问派生类字段，触及已析构的部分。
- 手工投递事件而没有真实改变 `QWindow` 关系，造成内部层级状态不一致。

## API 速查表

| API | 含义 | 重点边界 |
| --- | --- | --- |
| `QChildWindowEvent(QEvent::Type type, QWindow *childWindow)` | 为子窗口变化构造事件。 | `type` 只能是 `QEvent::ChildWindowAdded` 或 `QEvent::ChildWindowRemoved`；通常由框架创建。 |
| `QWindow *child() const` | 返回加入或移除的子窗口。 | 非拥有指针；只可依赖 `QWindow` 基础接口，不能假定派生类已完整构造或仍存活。 |
| 继承的 `QEvent::type() const` | 区分添加与移除事件。 | 先按类型分支，再执行最小化的窗口层级同步。 |
