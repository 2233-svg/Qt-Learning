# QIconDragEvent：窗口主图标被拖走的通知

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QIconDragEvent>`  
> 继承：`QEvent`

## 它解决什么问题

`QIconDragEvent` 是一个非常窄的窗口系统事件：它表示**窗口的主图标开始被拖动或被拖离**。其事件类型为 `QEvent::IconDrag`（值为 96）。

它不携带鼠标坐标、MIME 数据、拖放动作、源对象或目标对象，因此它不是通用拖放 API 的替代品。真正的内容拖放使用 `QDrag`、`QDragEnterEvent`、`QDragMoveEvent` 和 `QDropEvent`；主图标拖拽相关通知才使用本类。

## 实际使用场景

这种事件通常只在需要与特定窗口系统行为兼容的低层窗口或部件代码中观察。绝大多数 Qt 应用不会手工创建或处理它。

可能的用途包括：

- 记录窗口管理器发起的主图标拖拽；
- 在遗留桌面环境集成中暂停某个依赖窗口图标的临时操作；
- 在事件过滤器中区分“窗口主图标动作”和应用内容的 `QDrag` 拖放。

能否收到此事件以及主图标拖拽的实际含义，取决于平台窗口系统。跨平台业务功能不能把它作为可靠交互入口。

## 如何识别

由于它没有额外数据，通常只需要检查事件类型：

```cpp
bool WindowEventFilter::eventFilter(QObject *watched, QEvent *event)
{
    if (event->type() == QEvent::IconDrag) {
        // 平台报告窗口主图标被拖动。
        return false;
    }

    return QObject::eventFilter(watched, event);
}
```

如果确实需要转换类型，先检查 `type()`，再做 `static_cast<QIconDragEvent *>`。不要对任意 `QEvent *` 使用 `dynamic_cast` 或未经检查的强制转换。

## 生命周期与接受状态

和其他 Qt 事件一样，事件对象由事件发送机制在派发期间使用，接收方不能保存其裸指针到事件处理函数之外。此类没有自定义载荷，接受或忽略状态来自 `QEvent` 本身。

手工构造 `QIconDragEvent` 只适合测试事件过滤逻辑。构造它不会启动原生窗口图标的拖拽，也不会生成 `QDrag`、MIME 数据或窗口管理器动作。

## 与通用拖放的区别

| 需求 | 应使用的类型 |
| --- | --- |
| 拖动文件、文本、自定义 MIME 数据 | `QDrag` 与 `QMimeData` |
| 处理拖入、移动、放下 | `QDragEnterEvent`、`QDragMoveEvent`、`QDropEvent` |
| 处理拖离目标区域 | `QDragLeaveEvent` |
| 观察窗口主图标被拖动 | `QIconDragEvent` |

`QIconDragEvent` 没有位置和数据，不能据此判断拖到了哪里，也不能通过 `acceptProposedAction()` 决定拖放结果。

## 常见错误

- 把它当作内容拖放的开始事件。
- 期待从它取得 `QMimeData`、鼠标坐标或拖放动作。
- 手工发送它并期待操作系统真的开始拖动窗口图标。
- 假定每个平台都支持并派发该事件。
- 在事件回调之后保存事件指针。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 事件类型 | `QEvent::IconDrag` | 此事件对应的类型值，表示窗口主图标被拖走或开始拖动。 |
| 构造 | `QIconDragEvent()` | 构造一个 `IconDrag` 事件；仅构造事件对象，不启动系统拖拽。 |
| 继承 | `type() const` | 从 `QEvent` 继承；用于先确认是否为 `QEvent::IconDrag`。 |
| 继承 | `accept()` / `ignore()` / `isAccepted()` | 从 `QEvent` 继承的接受状态；本类没有拖放动作协商语义。 |

## 相关类

- `QEvent`：所有 Qt 事件的基类。
- `QDrag`、`QMimeData`：应用内容的主动拖放。
- `QDragEnterEvent`、`QDragMoveEvent`、`QDropEvent`：目标区域的拖放协商事件。

`QIconDragEvent` 的信息量很少，正因为如此，遇到它时应把它理解为窗口系统的状态通知，而不是一套可编排的拖放协议。
