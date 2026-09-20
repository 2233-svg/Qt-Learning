# Qt QHelpEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHelpEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QEvent -> QHelpEvent`  
> 定位：请求显示工具提示或“这是什么”帮助时的位置事件

## 1. 它解决什么问题

`QHelpEvent` 携带一次帮助请求的局部位置和屏幕位置。Widgets 常在收到 `QEvent::ToolTip` 时根据位置决定提示内容，再用 `QToolTip` 在全局位置显示；`QEvent::WhatsThis` 则用于进入“这是什么”帮助路径。

实际场景：

- 表格按单元格显示不同工具提示；
- 图形或画布按图元显示说明；
- 属性面板为禁用选项解释原因；
- 自定义控件提供 `QWhatsThis` 上下文帮助。

它不是帮助文本本身，也不是 `QToolTip` 对象。事件只表达“此位置需要帮助”，展示内容和策略由应用决定。

## 2. 典型入口

```cpp
#include <QHelpEvent>
#include <QToolTip>
#include <QWidget>

bool PropertyView::event(QEvent *event)
{
    if (event->type() == QEvent::ToolTip) {
        auto *helpEvent = static_cast<QHelpEvent *>(event);
        const QString text = tooltipFor(helpEvent->pos());

        if (!text.isEmpty()) {
            QToolTip::showText(helpEvent->globalPos(), text, this);
            return true;
        }

        QToolTip::hideText();
        event->ignore();
        return true;
    }
    return QWidget::event(event);
}
```

`pos()` 用于在接收 widget 内命中测试，`globalPos()` 用于定位 `QToolTip::showText()`。事件指针仅在同步处理期间有效。

## 3. `ToolTip` 与 `WhatsThis`

构造函数允许传入 `QEvent::Type`。正常帮助事件类型应是：

- `QEvent::ToolTip`：短提示文本，通常由停留或鼠标悬停触发；
- `QEvent::WhatsThis`：更长的上下文帮助请求。

不要把两者混用。工具提示应保持简短、即时、与当前位置相关；“这是什么”通常提供更长说明或链接到帮助系统。

若当前点没有帮助内容，隐藏现有 tooltip 并 `ignore()`，让 Qt 有机会继续按默认路由处理，而不是显示上一次遗留的文本。

## 4. 坐标与多屏幕边界

`pos()` 是事件接收 widget 的局部整数坐标，适用于 `childAt()`、表格行列查找和画布命中测试。`globalPos()` 是屏幕或虚拟桌面坐标，适用于弹出帮助 UI。

不要把 `pos()` 直接交给 `QToolTip::showText()`，也不要用 `globalPos()` 做 widget 局部命中。嵌套控件、窗口移动和多屏幕环境都会放大这种错误。

## 5. 生命周期、性能与可访问性

复杂画布的 tooltip 命中测试可能频繁触发，应用应避免在事件中同步读取文件、查询网络或创建昂贵对象。可以缓存描述并只在命中对象改变时更新。

工具提示是鼠标入口之一，不应成为唯一帮助通道。重要说明还应能通过焦点、快捷键、标签或 `QWhatsThis` 路径获得，避免键盘用户无法访问。

## 6. 常见错误

- 用局部 `pos()` 作为 tooltip 的屏幕坐标；
- 当前点无提示时不隐藏旧 tooltip；
- 在回调结束后保存 `QHelpEvent *`；
- 对每次悬停同步执行慢查询；
- 将 `ToolTip` 和 `WhatsThis` 视为同一种内容；
- 只提供悬停帮助，忽略键盘可访问路径。

## 7. 逐项 API 说明

### `QHelpEvent(QEvent::Type type, const QPoint &pos, const QPoint &globalPos)`

构造帮助事件。`type` 正常使用 `ToolTip` 或 `WhatsThis`；`pos` 相对接收 widget，`globalPos` 相对屏幕或虚拟桌面。主要用于测试或事件注入。

### 坐标 API

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `const QPoint &pos() const` | 获取局部帮助位置。 | 用于命中测试。 |
| `int x() const` / `int y() const` | 获取局部位置分量。 | 通常优先使用完整 `pos()`。 |
| `const QPoint &globalPos() const` | 获取屏幕位置。 | `QToolTip::showText()` 的常用参数。 |
| `int globalX() const` / `int globalY() const` | 获取屏幕位置分量。 | 通常优先使用完整 `globalPos()`。 |

### 从 `QEvent` 继承

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `type()` | 区分 `ToolTip` 与 `WhatsThis`。 | 先判断类型再转换事件指针。 |
| `accept()` / `ignore()` | 控制当前帮助请求是否已处理。 | 没有内容时通常隐藏并忽略。 |
| `isAccepted()` | 查询处理状态。 | 不表示 tooltip 是否实际可见。 |

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QHelpEvent(type, pos, globalPos)` | 创建帮助位置事件。 | 类型通常是 `ToolTip` 或 `WhatsThis`。 |
| 位置 | `pos()` | 在控件内定位帮助对象。 | 用于局部命中测试。 |
| 位置 | `globalPos()` | 在屏幕上定位提示 UI。 | 用于 `QToolTip::showText()`。 |
| 分量 | `x()` / `y()` | 读取局部坐标分量。 | 完整点更不易混淆坐标系。 |
| 分量 | `globalX()` / `globalY()` | 读取全局坐标分量。 | 完整点更不易混淆坐标系。 |
| 类型 | `type()` | 区分工具提示和上下文帮助。 | 先判断再处理。 |
| 状态 | `accept()` / `ignore()` | 控制请求传播。 | 无帮助内容时隐藏旧提示。 |

---

### 一句话总结

`QHelpEvent` 用 `pos()` 找到要解释的对象、用 `globalPos()` 定位帮助 UI；工具提示和“这是什么”应走各自合适的内容路径。
