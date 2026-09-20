# QChildWindowEvent

> Qt 6.11.1 · Qt GUI · 来自 `QChildWindowEvent`

## 1. 先建立直觉

`QChildWindowEvent` 表示一个 `QWindow` 被加入或移出另一个窗口的 child-window 关系。它服务于原生窗口层级、嵌入式窗口、子窗口合成和平台窗口管理，不是普通 QWidget 布局变动事件。

简单说，它回答的是“这个窗口树里多了或少了哪个直接子窗口”。如果你在做多窗口渲染、嵌入原生窗口或自己维护窗口树，这个事件能帮助你同步层级、输入路由或资源归属。

## 2. 类说明

`QChildWindowEvent` 继承自 `QEvent`。事件类型通常是 `QEvent::ChildWindowAdded` 或 `QEvent::ChildWindowRemoved`，`child()` 返回发生关系变化的 `QWindow`。

类说明只用于表明这些 API 来自 `QChildWindowEvent`。它描述的是 `QWindow` 层级关系，和 `QObject::childEvent()` 或 `QWidget` 子控件添加/移除不能混为一谈。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QChildWindowEvent(type, childWindow)` | 构造子窗口增加或移除事件。 |
| `child() const` | 返回被加入或移出的直接子 `QWindow`。 |
| `type()` | 来自 `QEvent`，区分 ChildWindowAdded 与 ChildWindowRemoved。 |

## 4. 关键用法

### 维护嵌入窗口登记表

```cpp
bool HostWindow::event(QEvent *event)
{
    if (event->type() == QEvent::ChildWindowAdded) {
        auto *childEvent = static_cast<QChildWindowEvent *>(event);
        m_embeddedWindows.insert(childEvent->child());
        return true;
    }

    if (event->type() == QEvent::ChildWindowRemoved) {
        auto *childEvent = static_cast<QChildWindowEvent *>(event);
        m_embeddedWindows.remove(childEvent->child());
        return true;
    }

    return QWindow::event(event);
}
```

真正项目里，登记表最好配合 `QObject::destroyed` 做兜底，以防对象生命周期和层级变化时序交错。

### 子窗口移除不代表对象立即销毁

`ChildWindowRemoved` 表示 parent-window 关系被解除。子窗口可能仍然存在、转而成为顶层窗口、被重新挂到另一个窗口，或者稍后才销毁。不要在收到移除事件后立刻假设 `child()` 无效。

## 5. 使用场景

`QChildWindowEvent` 适合窗口容器、原生子窗口嵌入、多视图渲染宿主、远程桌面嵌入、游戏工具的独立预览窗口、定制平台窗口管理。

一般 Widgets 应用的主窗口、对话框、布局和子控件不需要直接使用它；那些更多依赖 QWidget 父子关系和布局系统。

## 6. 常见坑与经验

不要把它和 `QChildEvent` 混淆。后者是 QObject 子对象关系事件，前者专门针对 `QWindow`。

不要在 ChildWindowRemoved 时直接 `delete child()`。移除层级关系不等于你拥有并应销毁该窗口。

不要只根据 child-window 事件推导可见性。子窗口可能仍存在但隐藏、最小化或尚未 exposed。

不要忽略平台差异。原生窗口嵌入与子窗口语义在不同平台上可能受窗口管理器和后端限制。

## 7. 知识点覆盖

学习 `QChildWindowEvent` 应覆盖 `QWindow` 父子关系、ChildWindowAdded、ChildWindowRemoved、QObject 子对象区别、原生窗口嵌入、窗口生命周期、平台窗口管理和多窗口渲染。
