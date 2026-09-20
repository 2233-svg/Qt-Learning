# Qt QShowEvent：控件或窗口即将显示时的生命周期通知

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QShowEvent>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QEvent`  
> 类型定位：通知 widget/window 显示状态变化的无附加数据事件

## 1. 它解决什么问题

`QShowEvent` 在控件或窗口被显示时作为生命周期通知发送。它没有位置、尺寸、原因等额外字段，信息主要由事件类型和接收对象本身提供。

它适合做“第一次显示前准备”或“重新显示时刷新”的工作，例如：

- 延迟创建昂贵的子控件；
- 在窗口真正显示前刷新一次布局或数据；
- 第一次显示时启动动画、计时器或异步加载；
- 重新显示隐藏的面板时同步状态。

## 2. 构建与基本处理

```cpp
#include <QShowEvent>
#include <QWidget>

class Panel : public QWidget
{
protected:
    void showEvent(QShowEvent *event) override
    {
        if (!initialized) {
            initializeContent();
            initialized = true;
        }

        QWidget::showEvent(event);
    }

private:
    bool initialized = false;
};
```

在普通 Qt 应用中，`QShowEvent` 通常由 `QWidget` 或 `QWindow` 的显示流程创建并发送，应用很少需要手工构造。

## 3. 构造函数

### `QShowEvent::QShowEvent()`

创建一个显示事件。该事件没有公开参数和附加状态，事件类型由 Qt 设置为 show 事件类型。

手工构造主要适合测试派生 widget 的 `showEvent()` 处理。手工发送并不会真正让窗口获得平台可见状态，也不等价于调用 `show()`。

## 4. `showEvent()` 的实际语义

### 4.1 它是通知，不是显示命令

调用：

```cpp
widget->show();
```

才是请求显示。`QShowEvent` 是显示流程中的通知，不应通过接收事件来代替 `show()`。在 `showEvent()` 中调用 `hide()`、`close()` 或再次调用 `show()` 可能改变流程，应明确设计并避免递归。

### 4.2 可能多次收到

控件每次从隐藏状态转为显示状态，都可能收到 `QShowEvent`。不要把它无条件当作“构造后的第一次初始化”。一次性初始化应使用成员标志、延迟初始化函数或构造阶段完成。

### 4.3 父子控件的显示

子控件是否实际可见取决于自身和祖先状态。父窗口显示时，子控件可能参与显示流程；应用不要仅通过一次 child `QShowEvent` 推断完整窗口已经完成平台显示。

## 5. 事件接受状态

`QShowEvent` 继承 `QEvent` 的 accepted 状态，但接受或忽略通常不会阻止控件显示。它的核心作用是通知，而不是提供一个“取消显示”的标准接口。

如果业务需要阻止显示，应在调用 `show()` 前控制状态，或重新设计窗口/控件的可见性流程，而不是依赖 `ignore()`。

## 6. 与相关生命周期事件的区别

| 事件 | 语义 |
| --- | --- |
| `QShowEvent` | 显示流程通知 |
| `QHideEvent` | 隐藏流程通知 |
| `QExposeEvent` | 窗口内容是否暴露给系统/合成器的状态变化 |
| `QResizeEvent` | 几何尺寸变化 |
| `QWindowStateChangeEvent` | 最小化、最大化等窗口状态变化 |

`QShowEvent` 不携带最终尺寸。若需要使用显示后的几何尺寸，可在 `showEvent()` 中读取对象几何，或结合后续 resize/expose 事件处理。

## 7. 生命周期和线程

事件对象由 Qt 在 GUI 线程的事件分发中短时间使用。`showEvent(QShowEvent *)` 返回后，不应保存事件指针。若要异步执行工作，复制所需业务状态，并通过对象生命周期安全的 queued 调用安排。

## 8. 常见使用模式

### 8.1 延迟初始化

```cpp
void SettingsPage::showEvent(QShowEvent *event)
{
    QWidget::showEvent(event);
    refreshFromModel();
}
```

若页面会频繁隐藏和显示，应确保 `refreshFromModel()` 幂等，或只在模型版本发生变化时更新。

### 8.2 首次显示准备

```cpp
void PreviewWindow::showEvent(QShowEvent *event)
{
    if (firstShow) {
        firstShow = false;
        startPreview();
    }
    QWidget::showEvent(event);
}
```

是否先调用基类实现取决于派生类逻辑，但通常应保持基类事件处理链完整，避免改变 QWidget 内部行为。

## 9. 常见误区

- 手工构造 `QShowEvent` 期待窗口真的显示。
- 用 `ignore()` 阻止显示。
- 把每次 show 都当成第一次初始化。
- 把 show 事件当成 resize 或 expose 事件。
- 在事件返回后保存 `QShowEvent *`。
- 在 `showEvent()` 中无条件创建重复计时器或重复连接信号。
- 忘记调用 `QWidget::showEvent(event)` 或对应基类处理。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QShowEvent()` | 创建无附加数据的显示事件 | 手工构造不等于真正显示窗口 |
| 处理 | `QWidget::showEvent(QShowEvent *)` | 接收 widget 显示通知 | 可能多次触发；适合做显示时同步 |
| 状态 | `QEvent::type()` | 判断事件类型 | 不能从中获取尺寸或显示原因 |
| 状态 | `QEvent::accept()` / `ignore()` | 修改事件接受状态 | 通常不能取消显示 |

---

### 一句话总结

`QShowEvent` 是“显示流程发生了”的通知，不是显示命令，也不携带尺寸和原因；重写 `showEvent()` 时应考虑重复显示、父子可见性、基类处理和事件指针的短生命周期。
