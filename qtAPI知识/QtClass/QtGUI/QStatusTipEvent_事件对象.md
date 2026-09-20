# Qt QStatusTipEvent：状态提示文本的事件传递

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStatusTipEvent>`  
> 所属模块：`Qt6::Gui`，需要启用 status tip 配置  
> 继承：`QEvent`  
> 类型定位：携带一段状态提示文本的轻量事件对象

## 1. 它解决什么问题

`QStatusTipEvent` 用于把一段状态提示文本沿 Qt 对象事件系统传递给接收者。典型场景是：

- 鼠标悬停到带 `statusTip` 的控件；
- 主窗口或状态栏显示当前控件的操作提示；
- 自定义控件把提示文本交给父对象或窗口处理。

它只携带文本，不负责绘制状态栏，也不决定提示展示位置。`QMainWindow`、`QStatusBar` 或应用自定义事件处理逻辑负责消费这段文本。

## 2. 构建与最小处理

```cpp
#include <QStatusTipEvent>
#include <QWidget>

class ToolButton : public QWidget
{
protected:
    bool event(QEvent *event) override
    {
        if (event->type() == QEvent::StatusTip) {
            const auto *tipEvent =
                static_cast<const QStatusTipEvent *>(event);
            qDebug() << tipEvent->tip();
        }
        return QWidget::event(event);
    }
};
```

实际项目更常使用控件的 `setStatusTip()` 和主窗口状态栏的默认处理，而不是手工创建事件。

## 3. 构造函数

### `explicit QStatusTipEvent(const QString &tip)`

创建一个携带 `tip` 文本的 status tip 事件。文本按值保存，调用方修改原来的 `QString` 不会改变事件内部内容。

```cpp
QStatusTipEvent event(QStringLiteral("打开设置"));
Q_ASSERT(event.tip() == QStringLiteral("打开设置"));
```

手工构造事件不等于把文本显示到状态栏；还需要通过 `QCoreApplication::sendEvent()`、`postEvent()` 或更高层 widget API 发送给接收者。一般业务应使用 `QWidget::setStatusTip()`。

## 4. `tip() const`

```cpp
QString tip() const;
```

返回事件携带的状态提示文本。空字符串可以表示清除当前提示或没有提示，具体显示行为由接收者决定。

返回值是 `QString`，适合复制到异步业务状态；事件对象本身仍只在处理期间有效。

## 5. 与 widget status tip 的关系

控件可以设置：

```cpp
button->setStatusTip(QStringLiteral("保存当前文档"));
```

当 Qt 的 widget 事件和状态提示机制需要传递这段文本时，会使用 status tip 事件。主窗口通常把它显示到状态栏。自定义接收者可以重写 `event()`，在 `QEvent::StatusTip` 分支读取 `tip()`。

`QStatusTipEvent` 不保存产生提示的 widget 指针，也不携带鼠标位置。若应用需要知道来源，应在自己的事件过滤器或对象上下文中关联接收者。

## 6. 接受状态和传播

它继承 `QEvent` 的 accepted 状态。接收者可以接受或忽略事件，具体是否继续传播取决于接收者的事件处理实现。

`accept()` 或 `ignore()` 不会修改 `tip()` 文本，也不会直接控制状态栏的内容。要清除提示，通常由状态栏或窗口逻辑显示空文本，或使用控件自身的状态提示更新流程。

## 7. 生命周期和线程

事件对象通常由 Qt 在 GUI 事件循环中创建和发送，接收者不拥有它。不要保存 `QStatusTipEvent *`，需要延后使用时复制 `tip()`。

状态栏和 widget 通常属于 GUI 线程。不要跨线程直接向 GUI 对象发送并依赖即时显示；跨线程应使用 queued signal/slot 把文本发送到 GUI 线程。

## 8. 常见误区

- 手工构造事件后期待状态栏自动出现文本。
- 把它当成带鼠标坐标的 hover 事件。
- 认为 `ignore()` 一定会清空状态栏。
- 在事件返回后保存事件指针。
- 把空 `tip()` 当成固定的“清除命令”：最终行为由接收者决定。
- 在工作线程直接操作状态栏或 widget。

## API 速查表
| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QStatusTipEvent(const QString &tip)` | 创建带提示文本的事件 | 不会自动显示到状态栏 |
| 查询 | `tip() const` | 获取提示文本 | 空字符串的处理由接收者决定 |
| 事件类型 | `QEvent::StatusTip` | 识别 status tip 事件 | 不携带来源和坐标 |
| 状态 | `accept()` / `ignore()` | 控制事件处理/传播 | 不直接修改提示文本 |
| 高层入口 | `QWidget::setStatusTip()` | 为控件设置状态提示 | 通常优先于手工构造事件 |

---

### 一句话总结

`QStatusTipEvent` 只负责传递状态提示文本：它不绘制状态栏、不携带来源和坐标，也不因手工构造而自动显示；普通应用优先设置 widget 的 `statusTip`，自定义事件处理时读取 `tip()` 并遵守事件对象的短生命周期。
