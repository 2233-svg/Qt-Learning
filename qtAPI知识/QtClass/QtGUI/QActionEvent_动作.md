# QActionEvent：让控件感知动作被添加、移除或更新

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QActionEvent>`  
> 模块：Qt GUI，链接 `Qt6::Gui`  
> 继承：`QEvent`

## 它解决什么问题

`QAction` 可以被加入 `QWidget` 等宿主对象。宿主除了保存动作，还常需把它转化为自己的界面元素，例如工具栏为动作创建工具按钮，菜单根据动作顺序插入菜单项。`QActionEvent` 就是 Qt 在动作关联发生变化时发送给宿主的事件。

它覆盖三种 `QEvent::Type`：

- `QEvent::ActionAdded`
- `QEvent::ActionRemoved`
- `QEvent::ActionChanged`

这不是用户点击动作时的事件。用户触发命令由 `QAction::triggered()` 等信号表达；本类表示的是“宿主的动作列表如何变化”。

## 实际使用场景

大多数应用只需调用 `QWidget::addAction()`、`QMenu::addAction()` 或 `QToolBar::addAction()`，无需手写此类。自定义容器控件若想根据新增、删除和修改的动作同步自己的按钮栏或命令面板，才会重写 `actionEvent()`。

```cpp
void CommandStrip::actionEvent(QActionEvent *event)
{
    switch (event->type()) {
    case QEvent::ActionAdded:
        insertButtonFor(event->action(), event->before());
        break;
    case QEvent::ActionRemoved:
        removeButtonFor(event->action());
        break;
    case QEvent::ActionChanged:
        refreshButtonFor(event->action());
        break;
    default:
        QWidget::actionEvent(event);
        break;
    }
}
```

示例中的 `insertButtonFor()` 必须把空的 `before` 理解为追加到末尾。实践中还应让自定义按钮监听 `QAction::changed()`、`toggled()` 和 `triggered()`，因为一次 `ActionChanged` 不等于动作生命周期结束。

## 构造与生命周期

框架通常负责创建和分发 `QActionEvent`，业务代码不应手工 `postEvent()` 来伪造动作列表变更。正确的来源是调用宿主的添加、插入、删除动作 API。

事件中保存的 `QAction *` 和 `before` 都是非拥有指针。事件本身不负责销毁它们；在 `actionEvent()` 返回后也不应假定这些指针仍适合长期缓存。尤其处理 `ActionRemoved` 时，应从自定义视图中解除关联，而不是删除该动作，除非动作所有权本来就在本控件。

## `before()` 的准确语义

`before()` 只在 `event->type() == QEvent::ActionAdded` 时表示插入位置：新动作应放在 `before()` 返回的动作之前。

- 返回非空指针：插入到该已有动作之前。
- 返回 `nullptr`：追加到该宿主已有动作之后。

对于 `ActionChanged` 和 `ActionRemoved`，`before()` 不应被用于推导顺序。

## 常见误区

- 误把 `ActionChanged` 当作“已触发”。动作属性、可用性或可见性变化都可能产生此事件。
- 手动构造事件来替代 `addAction()`。这样不会同步 Qt 内部的动作关联。
- 在 `ActionRemoved` 中释放 `event->action()`。移出宿主不等于该动作已无其他使用者。
- 忽略 `before() == nullptr`，导致新动作在自定义容器中插到错误位置。

## API 速查表

| API | 含义 | 重点边界 |
| --- | --- | --- |
| `QActionEvent(int type, QAction *action, QAction *before = nullptr)` | 构造一个动作列表变化事件。 | `type` 应为 `ActionAdded`、`ActionRemoved` 或 `ActionChanged`；一般由 Qt 框架创建。 |
| `QAction *action() const` | 返回被添加、移除或修改的动作。 | 返回非拥有指针，不要因处理事件而擅自删除。 |
| `QAction *before() const` | 返回新增动作应插在其前面的动作。 | 只对 `ActionAdded` 有顺序含义；为空表示追加。 |
| 继承的 `QEvent::type() const` | 返回动作变化类型。 | 先据此分支，再解释 `action()` 和 `before()`。 |
| 宿主重写点 `QWidget::actionEvent(QActionEvent *)` | 接收宿主动作列表变化。 | 调用添加、移除 API 触发，不要靠手工投递事件维护状态。 |
